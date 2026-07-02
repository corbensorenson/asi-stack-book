# Source Note: Temporal Documentation - What is Temporal?

| Field | Value |
|---|---|
| Source ID | `ext_temporal_docs` |
| Source title | Temporal Documentation: What is Temporal? |
| Ingestion date | 2026-07-02 |
| Source version / URL | https://docs.temporal.io/temporal |
| Citation label | Temporal Documentation (2026), What is Temporal? |
| Published / updated | unknown / 2026 |
| Ingestion basis | Official public documentation inspected for the Labor OS external literature queue; no Temporal service, workflow, worker, namespace, or event-history replay was run from this repository. |

## Thesis

Temporal is the closest durable-execution comparator for the Labor OS chapter because it treats application workflows as long-running, recoverable executions with recorded event histories. It supplies useful vocabulary for durability, worker processes, workflow state, failure recovery, and long-lived orchestration, while leaving ASI Stack-specific authority, approval, claim-ledger, and evidence-readiness semantics unimplemented.

## Mechanisms

- Run durable workflow executions through a Temporal service and worker processes.
- Preserve workflow progress through event histories.
- Resume, recover, and react to external events in long-running workflows.
- Separate workflow orchestration from activities and worker-hosted application code.
- Treat failure handling as part of the runtime substrate rather than ad hoc application glue.

## Evidence

- The official documentation frames Temporal as a runtime for durable function executions and workflow executions.
- The documentation ties durable execution to recorded workflow event history and failure recovery.
- This repository has not installed Temporal, encoded Labor OS typed jobs as Temporal workflows, run workers, inspected event histories, or replayed Temporal executions.
- Use this source as durable-execution comparator vocabulary only.

## Failure Modes

- Durable execution can preserve progress without preserving ASI Stack authority, approval, or evidence-state boundaries.
- A workflow can complete in a durable runtime while still lacking claim-ledger links, completion receipts, residual ownership, or proof-carrying evidence.
- Long-running orchestration can hide governance gaps if job records do not carry explicit permission and approval envelopes.

## Book Chapters Supported

- `labor-os-and-typed-jobs` (Labor OS and Typed Jobs)

## Claims To Add Or Update

- Position Labor OS typed jobs against durable workflow runtimes: Temporal already solves important failure-recovery and event-history problems, while Labor OS adds typed authority, approvals, artifact/evidence receipts, and promotion boundaries for AI work.
- Do not claim a Temporal integration, durable Labor OS runtime, workflow replay, event-history equivalence, or scheduler correctness.

## Open Questions

- Which `TypedJob` fields would compile naturally into a Temporal workflow, activity, task queue, and event-history record?
- What extra receipt fields would be needed so a Temporal-backed job can become evidence-ready in the ASI Stack?
- Can future prototypes replay Temporal event histories into the artifact graph without losing approval and residual semantics?
