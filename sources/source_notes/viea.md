# Source Note: Verified Intent-to-Execution Architecture

| Field | Value |
|---|---|
| Source ID | `viea` |
| Source title | Verified Intent-to-Execution Architecture |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public Release v1.0, May 2026; https://docs.google.com/document/d/1SDu8MWw4dOpFqwLqA8vpE1rV98O2_GeJgVlgb6R9GsM |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/viea.txt`; raw text is not published. |

## Thesis

VIEA frames advanced AI as an intent-to-execution system rather than a response generator. Human intent should become structured command contracts, durable artifacts, specialist-routed work, verified outputs, runtime execution, feedback, residuals, tools, benchmarks, and regression coverage.

## Mechanisms

- Structured command layer with role, objective, context, constraints, procedure, output contract, verification, and failure behavior.
- Artifact graph for claims, requirements, critiques, releases, feedback, tools, benchmarks, and residuals.
- Claim and verification ledger that separates verified, speculative, unsupported, contradicted, and experiment-required statements.
- Orchestrator/router, specialist modules, workflow-to-tool compiler, evaluation ratchet, runtime adapters, and feedback loop.
- Rule of durability: important responses become artifacts, repeated work becomes tools, claims receive support states, failures become residuals, and mastered capabilities become regression coverage.

## Evidence

- The source is an architecture proposal and systems framework, not a completed deployment report.
- It supplies concrete subsystem definitions, vertical-slice implementation guidance, and repeated benchmark/residual discipline.
- Reported mechanisms should be treated as design sources until corresponding code, tests, or execution logs are added to the book repo.

## Failure Modes

- Treating generated text as execution.
- Losing artifacts, constraints, source evidence, residuals, or deployment feedback across turns.
- Re-performing repeated workflows instead of compiling verified reusable tools.
- Claim support inflation when evidence is missing.

## Book Chapters Supported

- ASI Is a Stack, Not a Model
- Human Intent as a Formal Input
- Intent-to-Execution Contracts
- Command Contracts and Semantic Interfaces
- Artifact Graphs, Audit Logs, and Replay
- Runtime Adapters, Tool Permissions, and Human Approval
- Integrated Reference Architecture

## Claims To Add Or Update

- Use VIEA as the main execution spine connecting intent, artifacts, routing, verification, runtime adapters, and feedback.
- Keep any VIEA-derived claim at `source-derived` only after the specific source passage is mapped in Appendix C.
- Treat implementation and benchmark claims as unproven until matching artifacts exist in `experiments/`, `test_results/`, or inspected external repos.

## Open Questions

- Which VIEA subsystems become executable schemas in Appendix D first?
- Which one vertical slice should be the first prototype-backed demonstration?
- Which runtime targets should remain speculative until source-backed examples exist?
