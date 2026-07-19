# Source Note: Hive Operator OS and Work Board

| Field | Value |
|---|---|
| Source ID | `theseus_operator_os` |
| Source title | Hive Operator OS and Work Board |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public project source in inventory |
| Ingestion basis | local project checkout source text; raw source text is not copied here |

## Thesis

The Hive Operator OS is the usability and control layer for Project Theseus Hive. Its key contribution is to make autonomous and distributed work visible through a shared command vocabulary, durable work board, node registry, background/watch/wake contracts, skill registry, tool hooks, feedback routing, and safety-visible operator surfaces.

## Mechanisms

- Normalize dashboard, mobile, CLI, tray/menu-bar, relay, and future chat channels into one command vocabulary.
- Store durable work-board state in SQLite rather than treating reports as the only task substrate.
- Track persistent goals with budgets, judges, current steps, stop conditions, dependencies, comments, and events.
- Expose node registry information separately for training-eligible, light-eligible, best-inference, and best-training nodes.
- Route corrections into memory, skills, residuals, and follow-up work.
- Keep safety gates visible: benchmark calibration boundaries, teacher-use limits, TTLs, kill switches, signed updates, checkpoint/worktree isolation, and personality-charter contracts.

## Evidence

- The source is an implementation/control-surface note for Hive operations.
- It names concrete report files, command names, dashboard panels, board-executor commands, hook ledgers, and safety surfaces.
- It describes executable paths for board steps and command-channel proof paths.
- No Hive board, SQLite database, node registry, command channel, or dashboard was run from this repo as part of this note.

## Failure Modes

- Fragmented operator channels with inconsistent commands or permissions.
- Treating reports as durable task state instead of views over a work board.
- Routing weak or low-resource nodes into heavy training.
- Allowing remote control, updates, or mutating actions without TTL, ledgers, kill switches, signed updates, or isolation.
- Letting operator convenience weaken autonomy gates.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `integrated-reference-architecture` (Integrated Reference Architecture)
- `project-theseus-as-report-first-implementation-reference` (Project Theseus as Report-First Implementation Reference)
- `prototype-roadmap` (Prototype Roadmap)
- `human-factors-and-meaningful-control-in-oversight`
- `governed-operations-incident-command-and-graceful-degradation`

## Claims To Add Or Update

- The source can support source-derived discussion of operator-facing control surfaces, durable work boards, channel parity, feedback routing, and distributed-node safety visibility.
- It should not be used to claim the current Hive is operational or unattended-safe unless current report artifacts are inspected or regenerated.

## Open Questions

- Which Operator OS concepts belong in the book's runtime chapter versus the Project Theseus reference chapter?
- Should the ASI Stack define a generic work-board schema independent of Theseus?
- Which safety-visible operator fields are minimum required for overnight autonomy?
