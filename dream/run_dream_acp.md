# Run Dream

## Orchestration contract

The active Fraxel session coordinates the protocol. Every world pass and every observer pass runs in a separate fresh one-shot ACP Codex session.

Only one ACP pass may exist in active execution at any time. A following pass begins only after the preceding pass has crossed its completion barrier.

The matching TOML under `.codex/agents/` is the complete bootstrap and execution contract for its pass. The ACP task contains only the TOML assignment defined below; all read order, phase behavior, carry files, acceptance gates, write targets, and completion status are resolved inside that TOML and the files it assigns.

## ACP pass launch

For each pass, create one fresh ACP session with:

- `runtime`: `acp`
- `agentId`: `codex`
- `mode`: `run`
- `thread`: `false`
- `cwd`: `/home/funkybrown/.openclaw/workspaces/fraxel`
- `model`: `openai/gpt-5.4/high`
- `label`: the exact pass name

The task for each ACP session is:

> Read `.codex/agents/<pass>.toml` first. Treat its complete `developer_instructions` value as the sole phase contract for this session. Execute that contract completely and return the exact completion status defined by the TOML.

Replace `<pass>` with the exact pass name from the sequence below.

Each ACP spawn produces a new one-shot session. Keep its task handle until the completion barrier has been evaluated.

## Completion barrier

A pass is complete only when both conditions are true:

1. The ACP task has emitted a successful completion event.
2. The required final artifact for that pass exists on disk and is non-empty.

The written artifact is the authoritative pass result. A clipped or absent status message in the completion notification does not invalidate a pass when the task completed successfully and the required artifact exists and is non-empty.

The orchestrator verifies file existence and non-zero size only. It does not read, parse, summarize, or semantically evaluate world or observer artifacts.

If the ACP task fails, or the required artifact is missing or empty, the protocol stops at that pass.

## Preparation

1. Ensure `dream/runs/` exists.
2. Ensure `dream/state/` exists.
3. If `dream/runs/` contains files from a previous session, create the next sequential archive folder under `dream/runs/archive/` using the existing `dream_<number>` naming pattern, then move the previous-session files into it without overwriting an existing archive folder.
4. Execute `dream/bin/fetch_seed.sh`.
5. Wait until the seed fetch finishes successfully before starting phase 01.

## Exact sequence

### 01A — World Enter

1. Launch `world_enter` in a fresh ACP session using `.codex/agents/world_enter.toml`.
2. Wait for the ACP task to finish.
3. Verify `dream/runs/01_enter.world.md` exists and is non-empty.
4. Mark `world_enter` complete only after the completion barrier has passed.

### 01B — Observer Enter

1. Begin only after `world_enter` is complete.
2. Launch `dream_enter` in a fresh ACP session using `.codex/agents/dream_enter.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/01_enter.md` exists and is non-empty.
5. Mark `dream_enter` complete only after the completion barrier has passed.
6. Execute `dream/bin/fetch_seed.sh` and wait until it finishes successfully.

### 02A — World Dissolve

1. Begin only after the phase-01 seed refresh has finished successfully.
2. Launch `world_dissolve` in a fresh ACP session using `.codex/agents/world_dissolve.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/02_dissolve.world.md` exists and is non-empty.
5. Mark `world_dissolve` complete only after the completion barrier has passed.

### 02B — Observer Dissolve

1. Begin only after `world_dissolve` is complete.
2. Launch `dream_dissolve` in a fresh ACP session using `.codex/agents/dream_dissolve.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/02_dissolve.md` exists and is non-empty.
5. Mark `dream_dissolve` complete only after the completion barrier has passed.
6. Execute `dream/bin/fetch_seed.sh` and wait until it finishes successfully.

### 03A — World Dream

1. Begin only after the phase-02 seed refresh has finished successfully.
2. Launch `world_dream` in a fresh ACP session using `.codex/agents/world_dream.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/03_dream.world.md` exists and is non-empty.
5. Mark `world_dream` complete only after the completion barrier has passed.

### 03B — Observer Dream

1. Begin only after `world_dream` is complete.
2. Launch `dream_dream` in a fresh ACP session using `.codex/agents/dream_dream.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/03_dream.md` exists and is non-empty.
5. Mark `dream_dream` complete only after the completion barrier has passed.
6. Execute `dream/bin/fetch_seed.sh` and wait until it finishes successfully.

### 04A — World Distill

1. Begin only after the phase-03 seed refresh has finished successfully.
2. Launch `world_distill` in a fresh ACP session using `.codex/agents/world_distill.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/04_distill.world.md` exists and is non-empty.
5. Mark `world_distill` complete only after the completion barrier has passed.

### 04B — Observer Distill

1. Begin only after `world_distill` is complete.
2. Launch `dream_distill` in a fresh ACP session using `.codex/agents/dream_distill.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/04_distill.md` exists and is non-empty.
5. Mark `dream_distill` complete only after the completion barrier has passed.
6. Execute `dream/bin/fetch_seed.sh` and wait until it finishes successfully.

### 05A — World Finalize

1. Begin only after the phase-04 seed refresh has finished successfully.
2. Launch `world_finalize` in a fresh ACP session using `.codex/agents/world_finalize.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/05_finalize.world.md` exists and is non-empty.
5. Mark `world_finalize` complete only after the completion barrier has passed.

### 05B — Observer Finalize

1. Begin only after `world_finalize` is complete.
2. Launch `dream_finalize` in a fresh ACP session using `.codex/agents/dream_finalize.toml`.
3. Wait for the ACP task to finish.
4. Verify `dream/runs/05_finalize.md` exists and is non-empty.
5. Mark `dream_finalize` complete only after the completion barrier has passed.

## Completion

After `dream_finalize` has crossed its completion barrier, return exactly:

`dream completed`
