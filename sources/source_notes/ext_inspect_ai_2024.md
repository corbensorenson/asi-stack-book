# Source Note: Inspect AI: Framework for Large Language Model Evaluations

| Field | Value |
|---|---|
| Source ID | `ext_inspect_ai_2024` |
| Source title | Inspect AI: Framework for Large Language Model Evaluations |
| Ingestion date | 2026-07-10 |
| Source version / URL | Official documentation, https://inspect.aisi.org.uk/ |
| Citation label | UK AI Security Institute (2024), Inspect AI |
| Published / updated | 2024-05 / 2026-07-10 |
| Ingestion basis | Metadata-first intake from the official documentation record and repository inventory; this repository has not run Inspect AI. |

## Thesis

Inspect AI is a framework comparator for composable evaluation tasks, datasets, solvers, scorers, agents, tools, logs, and sandboxes.

## Mechanisms

- The inventory identifies the framework’s composable evaluation and logged-agent surfaces.
- It is routed to runtime effects, benchmarks, capability commitments, and adversarial evaluation.

## Evidence

- Framework availability or a passing task does not establish benchmark validity, coverage, local execution, safety, or deployment readiness.
- No local Inspect configuration, task, result, or sandbox trace was inspected in this increment.

## Failure Modes

- Treating an evaluation harness as a validated evaluation program.
- Conflating a task pass with broad capability or safety assurance.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `capability-thresholds-and-deployment-commitments`
- `adversarial-evaluation-sandbagging-and-training-time-deception`

## Claims To Add Or Update

- Use as an evaluation-framework comparator, while retaining explicit workload, baseline, and independence requirements.

## Open Questions

- Which public-safe task and scorer fixtures could demonstrate the book’s evidence contract without overstating coverage?
