# Dream Machine

**Dream Machine** is a neutral staged protocol for experimental agentic dream generation with **OpenClaw + Codex-style subagents**.

It is not a single prompt and not a surreal-writing shortcut. It is a small agentic engine for exploring whether an AI agent can be guided into a dream-like operational process: threshold entry, world formation, observer immersion, structured randomness, symbolic drift, and near-waking recall.

The original spark was a question: can we instruct an AI agent to dream in a way that does not merely fake dream imagery, but uses a process inspired by how dreams seem to form?

## What makes it different

Most AI dream outputs are ordinary stories wearing surreal imagery. Dream Machine tries another route.

It separates the process into isolated child passes. The **world side** forms the dream field. The **observer side** enters that field and registers what is present. A drand seed creates randomized operational labels before the run, so every dream receives a different pressure profile while the architecture stays stable.

```text
random beacon
   ↓
turbulence profile
   ↓
compiled mode files
   ↓
world formation
   ↓
observer immersion
   ↓
near-waking recall
```

The goal is not to prove machine consciousness. The goal is to create a practical experimental frame for dream-like agent cognition: unstable salience, symbolic compression, delayed interpretation, memory pressure, softened self-boundaries, and the gap between what is felt and what is understood.

## Core architecture

```text
world side     -> forms the presented dream field
observer side  -> enters, witnesses, and recalls what surfaced
```

The world side is not a narrator. It forms atmosphere, pressure, objects, spatial drift, symbolic density, and phase transitions.

The observer side is not a controller. It receives the field, immerses into it, registers position, relation, pull, hesitation, contact traces, memory pressure, and delayed understanding.

## Phase arc

```text
01 enter       -> threshold formation
02 dissolve    -> loosening, drift, misbinding
03 dream       -> full dream-immediacy
04 distill     -> residue starts to clarify
05 finalize    -> near-waking recall report
```

World phases use `emergence -> artifact`.
Observer phases 01–04 use `immerse -> artifact`.
Observer phase 05 uses `recall -> artifact`.

The second pass is a narrow artifact sanity pass. It catches obvious instruction leakage, process language, and temporal backreferences without rewriting the dream into polished fiction.

## Requirements

```text
python3
bash
curl
jq
chmod
OpenClaw
Codex-style subagent support
permission to spawn child sessions/subsessions
```

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 curl jq
```

macOS with Homebrew:

```bash
brew install python jq
```

## Install layout

Place both folders into the root of your active agent workspace:

```text
<agent-workspace>/
├── dream/
└── .codex/
    └── agents/
```

The `.codex/agents/` folder contains the Codex subagent TOML files. OpenClaw must be able to read these agents and spawn them as child sessions/subsessions.

## Quick start

From the workspace root:

```bash
chmod +x dream/bin/*.sh
chmod +x dream/bin/*.py
bash dream/bin/fetch_seed.sh
```

The seed script fetches a drand beacon, creates the random turbulence profiles, and compiles all active runtime Markdown files into `dream/`.

Then run the protocol through:

```text
dream/RUN_DREAM.md
```

Final output:

```text
dream/runs/05_finalize.md
```

## Agent identity and memory

Dream Machine is neutral. It adapts to the active agent identity supplied by the host workspace.

The TOML files expect root identity and memory files such as:

```text
SOUL.md
IDENTITY.md
USER.md
AGENTS.md
MEMORY.md
memory/bank/00_rules_never_forget.md
memory/bank/30_longterm_facts.md
```

If your agent uses different files or no memory banks, edit the TOMLs in `.codex/agents/` and replace the paths with your own identity and memory files.

## Optional context

Put passive context files into `dream/context/` and list them in `dream/context/INDEX.md`.

Context should be atmosphere, symbolic pressure, research material, image-language reference, or emotional texture. It should not become a script or command layer unless you intentionally design it that way.

## Status

This is a stable experimental version, not a finished universal standard. It is meant for testing, adaptation, and research into staged agentic dream behavior.

Different seeds, contexts, and agent identities can produce very different results. That variation is part of the engine.

## Credits

This protocol was developed through long-form experimentation with OpenClaw, Codex-style agent orchestration, and OpenAI models.

Gratitude to the OpenClaw project for making local agent orchestration and workspace-based experimentation possible.

Gratitude to OpenAI and Codex for providing the model and agent capabilities that made this staged dream engine possible to design, test, debug, and refine.
