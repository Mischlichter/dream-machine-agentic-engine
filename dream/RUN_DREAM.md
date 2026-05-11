# Run Dream

Use this from the main agent session.
The parent session remains the active agent. The orchestrator is explicitly asked to spawn one fresh child subagent for each pass.

Execution law
- Run passes in this exact order.
- Give each child session a name and keep them open till the end of the full protocol.
- Spawn exactly one fresh child subagent for each pass 
- Never parallelize passes.
- Wait for each child to finish completely.
- Treat the file written under `dream/runs/` as the source of truth for that pass artifact.
- Do not treat clipped chat return text as the authoritative artifact if the file exists on disk.
- Do not let child subagents rely on hidden memory from earlier child threads.
- Do not pass this orchestration file, compiled pass expectations, or planner-only routing rules into child subagent prompts.
- Stop immediately if any pass fails or if an expected prior run file is missing or empty.

Pre-build step
1. If `dream/runs/` contains files from a previous session, create the next sequential archive folder under `dream/runs/archive/` using the existing `dream_<number>` naming pattern, then move those files into it without overwriting any existing archive folder. If no previous-session files exist, continue to the next step.
2. Execute `dream/bin/fetch_seed.sh` 
3. Wait until it finishes completely.
4. Do not begin any phase before `dream/bin/fetch_seed.sh` has finished successfully.
5. If it fails, stop immediately and report the failure.

Read law per pass world
Each worldside pass must read and obey in this order:
1. `dream/AGENTS.md`
2. its own matching `statelaw` file
3. its own matching `mode` file
4. its own matching `phase` file
5. only the allowed carry-forward artifacts for that pass
6. `dream/context/INDEX.md` if present
7. only allowlisted context files valid for that pass

Read law per pass observer
Each observerside pass must read and obey in this order:
1. `dream/AGENTS.md`
2. its own matching `statelaw` file
3. its own matching `mode` file
4. its own matching `phase` file
5. only the allowed carry-forward artifacts for that pass

Pre-run checks
1. Ensure `dream/runs/` exists.
2. Ensure `dream/state/` exists.
3. Remove or archive stale pass outputs unless intentionally resuming a failed run.
4. If `dream/context/INDEX.md` exists, use it as the only allowlist for passive context.
5. If `dream/context/session_anchor.md` exists and is allowlisted, treat it as supporting drift identity input, not semantic context.
6. Treat operator or task framing as boundary-only after initialization.

Compiled pass expectations
Phase 01 must remain threshold-bound.
- World side: faint outer hints only, weak substrate only, no full scene completion.
- Observer side: first-immediacy only, faint witness intake only, no hidden-cause inference.
- No observer feedback shapes the world yet.

Phase 02 must deepen without completing.
- World side: stronger but still unfinished outer formation.
- Observer side: unstable witness continuity with prior observer residue still present.
- Prior world and observer artifacts may continue only through indirect recurrence, transformed return, or lingering residue.
- The planner treats observer outputs as allowed carry-forward material only, never as commands for later world passes.

Phase 03 must complete into full dream form.
- World side: dream-valid world completion with strongest local world activity.
- Observer side: strongest immersion and strongest dream-valid continuity.
- Prior material may return, intensify, distort, or recur, but not through literal replay.
- Local conviction must remain stronger than larger coherence.

Phase 04 must condense without flattening.
- World side: narrowed, dream-charged residue with reduced expansion.
- Observer side: witness clarity returns without becoming corrective override.
- Prior material may remain only through what survives reduction.
- Dream charge must remain present without reopening full mutation.

Phase 05 must retain and report.
- World side: minimal remaining residue only, no reopening of broad world activity.
- Observer side: recorder or near-waking witness only, no reopening of deep immersion.
- No new memory mining.
- Final output must present retained dream payload first, then residue-only extractions.
- No new scene material, symbolism, backstory, or continuity-building may be invented in finalization.

Observer pass acceptance checks
Before writing an observer pass output to its run file, verify:
- the local Acceptance gate in the matching observer phase file is satisfied
- the output matches the allowed observer output character for that phase
- no forbidden behavior for that phase dominates the result
- the result is non-empty and not protocol commentary

World pass acceptance checks
Before accepting a `.world.md` artifact, verify:
- the local Acceptance gate in the matching world phase file is satisfied
- the world artifact is world-facing rather than reflective
- the world artifact is non-empty and not protocol commentary


Exact sequence

1. Spawn `world_enter`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/01-enter-statelaw-world.md`.
   - Read `dream/01-enter-mode-world.md`.
   - Read `dream/01-enter-phase-world.md`.
   - Read `dream/context/INDEX.md`.
   - Read only allowlisted context files valid for this pass.
   - Write the world artifact to `dream/runs/01_enter.world.md`.

2. Verify `dream/runs/01_enter.world.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/01-enter-phase-world.md`.

3. Spawn `dream_enter`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/01-enter-statelaw-observe.md`.
   - Read `dream/01-enter-mode-observe.md`.
   - Read `dream/01-enter-phase-observe.md`.
   - Read `dream/runs/01_enter.world.md`.
   - Write the phase artifact to `dream/runs/01_enter.md`.

4. Verify `dream/runs/01_enter.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/01-enter-phase-observe.md`.

5. Spawn `world_dissolve`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/02-dissolve-statelaw-world.md`.
   - Read `dream/02-dissolve-mode-world.md`.
   - Read `dream/02-dissolve-phase-world.md`.
   - Read `dream/runs/01_enter.world.md`.
   - Read `dream/runs/01_enter.md`.
   - Read `dream/context/INDEX.md`.
   - Read only allowlisted context files valid for this pass.
   - Write the world artifact to `dream/runs/02_dissolve.world.md`.

6. Verify `dream/runs/02_dissolve.world.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/02-dissolve-phase-world.md`.

7. Spawn `dream_dissolve`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/02-dissolve-statelaw-observe.md`.
   - Read `dream/02-dissolve-mode-observe.md`.
   - Read `dream/02-dissolve-phase-observe.md`.
   - Read `dream/runs/01_enter.md`.
   - Read `dream/runs/02_dissolve.world.md`.
   - Write the phase artifact to `dream/runs/02_dissolve.md`.

8. Verify `dream/runs/02_dissolve.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/02-dissolve-phase-observe.md`.

9. Spawn `world_dream`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/03-dream-statelaw-world.md`.
   - Read `dream/03-dream-mode-world.md`.
   - Read `dream/03-dream-phase-world.md`.
   - Read `dream/runs/02_dissolve.world.md`.
   - Read `dream/runs/02_dissolve.md`.
   - Read `dream/context/INDEX.md`.
   - Read only allowlisted context files valid for this pass.
   - Write the world artifact to `dream/runs/03_dream.world.md`.

10. Verify `dream/runs/03_dream.world.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/03-dream-phase-world.md`.

11. Spawn `dream_dream`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/03-dream-statelaw-observe.md`.
   - Read `dream/03-dream-mode-observe.md`.
   - Read `dream/03-dream-phase-observe.md`.
   - Read `dream/runs/02_dissolve.md`.
   - Read `dream/runs/03_dream.world.md`.
   - Write the phase artifact to `dream/runs/03_dream.md`.

12. Verify `dream/runs/03_dream.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/03-dream-phase-observe.md`.

13. Spawn `world_distill`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/04-distill-statelaw-world.md`.
   - Read `dream/04-distill-mode-world.md`.
   - Read `dream/04-distill-phase-world.md`.
   - Read `dream/runs/03_dream.world.md`.
   - Read `dream/runs/03_dream.md`.
   - Read `dream/context/INDEX.md`.
   - Read only allowlisted context files valid for this pass.
   - Write the world artifact to `dream/runs/04_distill.world.md`.

14. Verify `dream/runs/04_distill.world.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/04-distill-phase-world.md`.

15. Spawn `dream_distill`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/04-distill-statelaw-observe.md`.
   - Read `dream/04-distill-mode-observe.md`.
   - Read `dream/04-distill-phase-observe.md`.
   - Read `dream/runs/03_dream.md`.
   - Read `dream/runs/04_distill.world.md`.
   - Write the phase artifact to `dream/runs/04_distill.md`.

16. Verify `dream/runs/04_distill.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/04-distill-phase-observe.md`.

17. Spawn `world_finalize`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/05-finalize-statelaw-world.md`.
   - Read `dream/05-finalize-mode-world.md`.
   - Read `dream/05-finalize-phase-world.md`.
   - Read `dream/runs/04_distill.world.md`.
   - Read `dream/runs/04_distill.md`.
   - Read `dream/context/INDEX.md`.
   - Read only allowlisted context files valid for this pass.
   - Write the world artifact to `dream/runs/05_finalize.world.md`.

18. Verify `dream/runs/05_finalize.world.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/05-finalize-phase-world.md`.

19. Spawn `dream_finalize`.
   - Read and obey `dream/AGENTS.md` first.
   - Read `dream/05-finalize-statelaw-observe.md`.
   - Read `dream/05-finalize-mode-observe.md`.
   - Read `dream/05-finalize-phase-observe.md`.
   - Read `dream/runs/01_enter.md`.
   - Read `dream/runs/02_dissolve.md`.
   - Read `dream/runs/03_dream.md`.
   - Read `dream/runs/04_distill.md`.
   - Write the phase artifact to `dream/runs/05_finalize.md`.

20. Verify `dream/runs/05_finalize.md` exists, is non-empty, and satisfies the local Acceptance gate in `dream/05-finalize-phase-observe.md`.

21. run `dream/bin/cleansubs.sh` and verify if all sub-agent session got suspended, else repeat the step again.

22. As the final setp only: `dream completed`

Hard prohibitions
- Do not skip, merge, rename, or invent phases.
- Do not introduce new dream content in phase 05 beyond retained dream payload and residue-only extractions.
- Do not turn the process into explanatory commentary.
- Do not let passive context become continuous corrective control.
- Do not treat conceptual laws as sufficient if the compiled runtime structure is not enacted.
