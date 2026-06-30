# Source Note: Software Magic Grimoire

| Field | Value |
|---|---|
| Source ID | `software_magic_grimoire` |
| Source title | Software Magic Grimoire |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1UjGadqJ3ZiqfLgbac0APtV_OLnlSZAkIW0o0r37YdBo |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/software_magic_grimoire.txt`; raw text is not published. |

## Thesis

Software Magic Grimoire treats engineering vocabulary as operative language. A strong technical word does not merely describe a system; it compresses a mechanism, assigns responsibility, invokes a workflow, exposes a failure shadow, and tells a human or machine what kind of action is now appropriate.

## Mechanisms

- Define "software magic words" by semantic density, operational addressability, placement, adjacency, invocation surface, and failure shadow.
- Organize engineering vocabulary into canonical houses or sigil ranges so words can become reusable control tokens.
- Treat a prompt or instruction as a bounded spell with roles, objectives, context, constraints, procedure, output, verification, and failure behavior.
- Define spell stacks as named queues of spells with handoff artifacts, guards, entry rules, exit rules, loops, recursion, and recovery paths.
- Separate incompatible modes such as discovery, design, implementation, verification, release, and rollback readiness.
- Require loops to advance on evidence and recursion to narrow scope.

## Evidence

- The source is a public-release vocabulary and promptcraft framework with a stack addendum.
- It provides reusable operating forms for prompt discipline, handoffs, guards, verification, and failure behavior.
- It is not an empirical study of prompt performance and does not provide local tests in this repository.

## Failure Modes

- Treating evocative terminology as evidence.
- Packing incompatible cognitive modes into one prompt.
- Advancing between steps without a concrete handoff artifact.
- Looping without a measurable exit condition.
- Recursing without reducing scope or naming a base case.
- Reusing a workflow without versioning its entry, exit, and recovery rules.

## Book Chapters Supported

- `human-intent-as-a-formal-input` (Human Intent as a Formal Input)
- `intent-to-execution-contracts` (Command Contracts: From Intent to Executable Work; includes folded command-contract semantic-interface material)
- `planning-as-a-control-layer` (Planning as a Control Layer: DAGs and Intelligence Arbitrage)
- `labor-os-and-typed-jobs` (Labor OS and Typed Jobs)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)

## Claims To Add Or Update

- Use this source for the book's language-to-operation bridge: commands, contracts, prompts, and workflows should emit artifacts and guards.
- Treat spell-stack forms as author-intent and workflow design vocabulary, not as measured performance evidence.

## Open Questions

- Should the book define a neutral "operation stack" schema derived from spell stacks?
- Which prompt-stack rules should become Codex test-plan requirements for chapter-writing runs?
