# Source Note: PDDL: The Planning Domain Definition Language

| Field | Value |
|---|---|
| Source ID | `ext_pddl_1998` |
| Source title | PDDL: The Planning Domain Definition Language |
| Ingestion date | 2026-06-28 |
| Source version / URL | Technical report PDF, https://www.cs.cmu.edu/~mmv/planning/readings/98aips-PDDL.pdf |
| Citation label | McDermott et al. (1998), PDDL |
| Published / updated | 1998 / not recorded |
| DOI | not recorded |
| Ingestion basis | Primary technical-report PDF and bibliographic metadata inspected for the planning/control literature queue; report not vendored into this repository and no planner run reproduced. |

## Thesis

PDDL belongs in the planning and cognitive-compilation chapters as an external reference for separating a planning domain, a concrete problem, and planner-comparable action descriptions. It helps the ASI Stack distinguish a plan-interface language from a planner implementation or successful execution.

## Mechanisms

- Separate domain descriptions from problem descriptions so multiple planning instances can share a domain vocabulary.
- Represent action schemas, preconditions, effects, types, constants, predicates, and goals in a planner-readable notation.
- Encourage empirical comparison by giving planners comparable problem sets and notations.
- Keep syntax and intended semantics distinct from any particular planner's search quality, execution safety, or authority model.

## Evidence

- The source is a planning-language definition and competition-interface artifact.
- This repository has not run a PDDL planner, imported benchmark domains, translated PlanForge records to PDDL, or reproduced any planning result.
- Use this source for external modeling vocabulary around typed planning interfaces, not as evidence that ASI Stack planning works.

## Failure Modes

- A syntactically valid planning model can still omit authority, context, residual, rollback, or verification constraints.
- Benchmark-comparable notation can be mistaken for task adequacy.
- A planner language can make a plan look executable even when the runtime, tool permissions, or evidence requirements are absent.

## Book Chapters Supported

- `planning-as-a-control-layer` (Planning as a Control Layer: DAGs and Intelligence Arbitrage)
- `intent-to-execution-contracts` (Command Contracts: From Intent to Executable Work)
- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)

## Claims To Add Or Update

- Use this note to compare PlanForge and semantic IR records against external planning-language/interface discipline.
- Do not claim that the ASI Stack implements PDDL, validates PDDL domains, or reproduces any IPC benchmark.
- Keep support state at `argument` until translation fixtures, planner runs, or accepted evidence transitions exist.

## Open Questions

- What is the smallest PlanForge-to-planning-language fixture that preserves authority and residual fields?
- Which PDDL-like boundaries are useful for semantic IR without dropping governance metadata?
- How should a planning-language adapter reject models that omit verification and rollback obligations?
