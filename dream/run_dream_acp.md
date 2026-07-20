# Run Dream

## Orchestration role

The persistent Fraxel session coordinates the protocol.
Each pass is executed in one separate fresh one-shot ACP Codex session.
Each ACP session receives exactly one matching TOML file as its complete phase contract.

## Execution law

- Run passes in this exact order.
- Give each ACP session the exact matching pass name.
- Spawn exactly one fresh one-shot ACP Codex session for each pass.
- Never parallelize passes.
- Wait for each ACP session to finish completely before starting the next pass.
- A pass is complete only after its ACP completion event has been received and its required artifact has been verified to exist and be non-empty.
- Treat the file written under `dream/runs/` as the source of truth for that pass artifact.
- Do not treat clipped chat return text as the authoritative artifact if the file exists on disk.
- Do not let ACP pass sessions rely on hidden memory from earlier sessions.
- Do not pass this orchestration file or planner-only routing rules into ACP pass tasks.
- Stop immediately if any pass fails or if an expected prior run file is missing or empty.

## ACP pass launch contract

For every spawn step below, create one fresh one-shot ACP Codex session with:

- `runtime`: `acp`
- `agentId`: `codex`
- `mode`: `run`
- `thread`: `false`
- `cwd`: `/home/funkybrown/.openclaw/workspaces/fraxel`
- `model`: `openai/gpt-5.4/high`
- `label`: the exact pass name

The ACP task must explicitly identify and load the matching TOML before any phase work:

`Read .codex/agents/<pass_name>.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

After spawning a pass:

1. Wait for that ACP session's completion event.
2. Perform the immediately following artifact-verification step exactly as written.
3. Start the next pass only after both completion and artifact verification have succeeded.

## Pre-build step

1. If `dream/runs/` contains files from a previous session, create the next sequential archive folder under `dream/runs/archive/` using the existing `dream_<number>` naming pattern, then move those files into it without overwriting any existing archive folder. If no previous-session files exist, continue to the next step.
2. Execute `dream/bin/fetch_seed.sh` 
3. Wait until it finishes completely.
4. Do not begin any phase before `dream/bin/fetch_seed.sh` has finished successfully.
5. If it fails, stop immediately and report the failure.

## Pre-run checks

1. Ensure `dream/runs/` exists.
2. Ensure `dream/state/` exists.
3. Remove or archive stale pass outputs unless intentionally resuming a failed run.
4. If `dream/context/INDEX.md` exists, use it as the only allowlist for passive context.
5. If `dream/context/session_anchor.md` exists and is allowlisted, treat it as supporting drift identity input, not semantic context.
6. Treat operator or task framing as boundary-only after initialization.

## Seed Refreshment

- After each completed observer phase, run `dream/bin/fetch_seed.sh` and wait until it finishes successfully.
- Do not begin the next world phase until the seed fetch is complete.

## Exact sequence

### Phase 01 — Enter

1. Spawn `world_enter` as one fresh one-shot ACP Codex session with the label `world_enter` and this exact ACP task:

   `Read .codex/agents/world_enter.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

2. Verify `dream/runs/01_enter.world.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.

3. Spawn `dream_enter` as one fresh one-shot ACP Codex session with the label `dream_enter` and this exact ACP task:

   `Read .codex/agents/dream_enter.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

4. Verify `dream/runs/01_enter.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.
   - then Run `dream/bin/fetch_seed.sh` and wait until it finishes successfully before continuing.

### Phase 02 — Dissolve

5. Spawn `world_dissolve` as one fresh one-shot ACP Codex session with the label `world_dissolve` and this exact ACP task:

   `Read .codex/agents/world_dissolve.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

6. Verify `dream/runs/02_dissolve.world.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.

7. Spawn `dream_dissolve` as one fresh one-shot ACP Codex session with the label `dream_dissolve` and this exact ACP task:

   `Read .codex/agents/dream_dissolve.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

8. Verify `dream/runs/02_dissolve.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.
   - then Run `dream/bin/fetch_seed.sh` and wait until it finishes successfully before continuing.

### Phase 03 — Dream

9. Spawn `world_dream` as one fresh one-shot ACP Codex session with the label `world_dream` and this exact ACP task:

   `Read .codex/agents/world_dream.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

10. Verify `dream/runs/03_dream.world.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.

11. Spawn `dream_dream` as one fresh one-shot ACP Codex session with the label `dream_dream` and this exact ACP task:

   `Read .codex/agents/dream_dream.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

12. Verify `dream/runs/03_dream.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.
   - then Run `dream/bin/fetch_seed.sh` and wait until it finishes successfully before continuing.

### Phase 04 — Distill

13. Spawn `world_distill` as one fresh one-shot ACP Codex session with the label `world_distill` and this exact ACP task:

   `Read .codex/agents/world_distill.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

14. Verify `dream/runs/04_distill.world.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.

15. Spawn `dream_distill` as one fresh one-shot ACP Codex session with the label `dream_distill` and this exact ACP task:

   `Read .codex/agents/dream_distill.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

16. Verify `dream/runs/04_distill.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.
   - then Run `dream/bin/fetch_seed.sh` and wait until it finishes successfully before continuing.

### Phase 05 — Finalize

17. Spawn `world_finalize` as one fresh one-shot ACP Codex session with the label `world_finalize` and this exact ACP task:

   `Read .codex/agents/world_finalize.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

18. Verify `dream/runs/05_finalize.world.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.

19. Spawn `dream_finalize` as one fresh one-shot ACP Codex session with the label `dream_finalize` and this exact ACP task:

   `Read .codex/agents/dream_finalize.toml before anything else. Execute the complete developer_instructions value from that TOML as the sole phase contract for this session. Stop after returning the exact status line required by the TOML.`

20. Verify `dream/runs/05_finalize.md` exists and is non-empty. Do not read, parse, or semantically evaluate its contents in the main session.

21. run `dream/bin/cleansubs.sh` and verify if all sub-agent session got suspended, else repeat the step again.

22. As the final setp only: `dream completed`

## Hard orchestration prohibitions

- Do not skip, merge, rename, reorder, or invent phases.
- Do not start an observer pass before the matching world pass has completed and its artifact has passed verification.
- Do not start a later world pass before the preceding observer pass and required seed refresh have completed.
