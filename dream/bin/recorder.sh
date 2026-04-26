#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DREAM_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
RUNS_DIR="$DREAM_DIR/runs"
LOG_DIR="$RUNS_DIR/logs"
FINAL_FILE="$RUNS_DIR/05_finalize.md"

mkdir -p "$LOG_DIR"

START_TS="$(date +%s)"
LOG_FILE="$LOG_DIR/dream-run-$(date +%F-%H%M%S).log"
PID_FILE="$LOG_DIR/.dream_log_recorder.pid"
META_FILE="$LOG_DIR/.dream_log_recorder.meta"

openclaw logs --follow --local-time > "$LOG_FILE" 2>&1 &
LOGGER_PID=$!

printf '%s\n' "$LOGGER_PID" > "$PID_FILE"
printf 'start_ts=%s\nlog_file=%s\n' "$START_TS" "$LOG_FILE" > "$META_FILE"

cleanup() {
  if kill -0 "$LOGGER_PID" 2>/dev/null; then
    kill "$LOGGER_PID" 2>/dev/null || true
    wait "$LOGGER_PID" 2>/dev/null || true
  fi
  rm -f "$PID_FILE"
}

trap cleanup EXIT

echo "[dream-log] recorder started: $LOG_FILE"
echo "[dream-log] pid: $LOGGER_PID"
echo "[dream-log] waiting for fresh finalize file..."

while true; do
  if [[ -f "$FINAL_FILE" ]]; then
    if stat -c %Y "$FINAL_FILE" >/dev/null 2>&1; then
      FILE_TS="$(stat -c %Y "$FINAL_FILE")"
    else
      FILE_TS="$(stat -f %m "$FINAL_FILE")"
    fi
    if [[ "$FILE_TS" -gt "$START_TS" ]]; then
      echo "[dream-log] detected fresh finalize file: $FINAL_FILE"
      break
    fi
  fi
  sleep 2
done

echo "[dream-log] stopping recorder"
cleanup
trap - EXIT

echo "[dream-log] done"
