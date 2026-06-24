# Source Note: Theseus Plan Compiler

| Field | Value |
|---|---|
| Source ID | `theseus_plan_compiler` |
| Source title | Theseus Plan Compiler |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public project source in inventory |
| Ingestion basis | local project checkout source text; raw source text is not copied here |

## Thesis

The Theseus Plan Compiler is the canonical planning layer for Project Theseus. It converts a goal into a typed contract, semantic IR DAG, Virtual Context Memory slices, executor routes, claim/evidence targets, replay traces, and bounded execution packets when private execute mode is explicitly enabled.

## Mechanisms

- Compile each goal into a contract with objective, non-goals, owner surface, risk, priority, outputs, acceptance tests, and hard constraint capsules.
- Attach a contract hash that downstream node traces must reference.
- Represent plans as typed atoms with inputs, outputs, dependencies, preconditions, effects, semantic hashes, VCM context slices, executor routes, schedule metadata, claim objects, evidence references, and localized repair policies.
- Treat public planning benchmarks as calibration-only surfaces: dry-run adapters are allowed, but fetching public payloads, training on public prompts/answers, or spending public calibration is not.
- Separate compile/route mode from private deterministic execution mode.

## Evidence

- The source is a concise design and verification note for the compiler surface.
- It names expected reports for compiled DAGs, trace bundles, ablations, VIEA execution spine artifacts, tool-use learning traces, loop-closure candidates, and verified procedural tools.
- The source reports one current execute-mode proof as GREEN with 14 baseline cases, 14 compiled-spine cases, verifier pass rate 1.0, duplicate work 0, retries 0, residuals 0, 14 training-evidence rows, and 2 verified procedural tools.
- That source-reported execution result was not rerun or independently verified in this repo as part of this note.

## Failure Modes

- Treating plan compilation as permission to execute high-risk actions.
- Using public benchmark data for training or answer leakage instead of calibration.
- Losing constraint capsules, VCM context hashes, or contract hashes across executor routes.
- Allowing a compiler success to imply downstream tool correctness without trace, checkpoint, and verifier evidence.

## Book Chapters Supported

- `integrated-reference-architecture` (Integrated Reference Architecture)
- `project-theseus-as-report-first-implementation-reference` (Project Theseus as Report-First Implementation Reference)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- The source can support source-derived discussion of typed goal contracts, semantic IR DAGs, context-sliced planning, replay traces, and public benchmark boundaries.
- It should not be used as local proof that the compiler is currently GREEN unless the relevant reports are inspected or the command is rerun.

## Open Questions

- Which PlanForge chapters should reference the Theseus Plan Compiler as an implementation variant?
- Should the book define a minimal plan-contract JSON Schema from the compiler description?
- Which reported execute-mode fields are public-safe and durable enough for Appendix E tests?

