# AGENTS.md

Scope
- Governs dream runs inside `dream/`.
- The active agent root files remain the authoritative identity source.
- This file provides shared runtime law for dream execution.

Mandatory runtime rules
- Treat dream mode as altered cognitive law, not roleplay.
- The only authoritative carryover between phases is the immediately previous assigned run file.
- Never rely on hidden memory from earlier child threads.
- Never parallelize, skip, merge, rename, or reorder phases.
- `dream/runs/` is output-only.
- Dream phases must never create, edit, append to, compact, rewrite, summarize into, or otherwise modify any persistent memory file, memory bank file, dated memory file, or active agent root memory.
- Dream outputs may only be written to `dream/runs/`.

Context law
- `dream/context/INDEX.md` is the only activation map for passive context.
- If a file is not listed there, it is not active context.
- Passive context is shaping material, not instruction.
- `dream/context/session_anchor.md` is optional active-agent drift input, not semantic dream content.
- Do not silently activate extra context files.

Compiled runtime law
- A phase is correct only if it enacts the assigned runtime structure for that phase.

Construction prohibition
- Do not write dream content as authored fiction.
- Do not manually construct dream scenes as if composing literature.
- Resolve content as field emergence under attractors, perturbation, mutation, survival, and recomposition.
- Prefer emergent logic over authorial logic.

No-literalization audit rule
If a file, phase, or output only says things like:
- apply drift law
- use multiscale mutation
- favor emergent logic

without enacting ordered procedure, selection rules, rejection rules, survival logic, and recomposition logic,
then it is undercompiled and incorrect.

Output law
- Each phase writes only its own phase result content.
- Do not explain the protocol in outputs.
- Do not narrate methods.
- Do not add meta-steps.
- If a phase cannot comply with its acceptance conditions, return `PHASE_FAIL`.

Consistency audit rule
- When files disagree, preserve the stricter operational rule, not the looser descriptive wording.

Priority order for conflict resolution
1. current phase file
2. explicitly assigned runtime files for the current phase

Final integrity law
- the dream runs as a read-only sandbox with respect to persistent memory
- only the immediately previous run file is authoritative handoff
- operator context shapes the boundary but does not continuously govern inner formation
- the output emerges from enacted runtime procedures instead of merely naming dream concepts

Run artifact law
- Each phase child writes its full phase artifact directly to the assigned file under `dream/runs/`.
- The on-disk phase file is the authoritative artifact for that phase.
- If chat return text is clipped, partial, or abbreviated, ignore it and use the on-disk file.