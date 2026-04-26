#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DREAM_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
STATE_DIR="$DREAM_DIR/state"

SEED_JSON="$STATE_DIR/session_seed.json"
ANCHOR_MD="$STATE_DIR/session_anchor.md"
COMPILER="$DREAM_DIR/bin/compile_turbulence.py"

mkdir -p "$STATE_DIR"

resp="$(curl -fsSL https://api.drand.sh/v2/beacons/default/rounds/latest)"
printf '%s\n' "$resp" > "$SEED_JSON"

round="$(python3 - "$SEED_JSON" <<'PY'
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)
print(data.get("round", ""))
PY
)"

signature="$(python3 - "$SEED_JSON" <<'PY'
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)
print(data.get("signature", ""))
PY
)"

cat > "$ANCHOR_MD" <<EOF
# Session Anchor
source: drand default beacon
round: $round
signature: $signature
EOF

python3 "$COMPILER"

echo "Wrote:"
echo "  $SEED_JSON"
echo "  $ANCHOR_MD"
echo "  $STATE_DIR/turbulence_profile.json"
echo "  $STATE_DIR/turbulence_profile.md"
echo "  $STATE_DIR/world_turbulence_profile.json"
echo "  $STATE_DIR/world_turbulence_profile.md"
echo "  $STATE_DIR/observer_turbulence_profile.json"
echo "  $STATE_DIR/observer_turbulence_profile.md"
