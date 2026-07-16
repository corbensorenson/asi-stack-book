# Model-adequacy dossier: Typed-job refinement

## Ownership

- Chapter: `labor-os-and-typed-jobs`
- Frozen targets: all five `lean:jobs.lifecycle.*` targets
- Stronger model: `lean/AsiStackProofs/TypedJobRefinement.lean`
- Independent consumer: `scripts/validate_typed_job_refinement.py`
- Result: `experiments/typed_job_refinement/results/2026-07-15-local.json`
- Support-state effect: exactly `none`

## Reachable model

The model owns one job-specific event sequence from exact contract and plan-node
lock through authorization, dispatch, represented execution, adjudication, and
consumer-acknowledged closure. It represents approval, permissions, leases,
scheduler admission, retry identity, authority preservation, cancellation,
artifacts, audit trails, verification, completion, replay, residual ownership,
and acknowledgment without treating any field as proof that the corresponding
service or real-world effect worked.

## Consequences, countermodels, and consumer

General consequences preserve job, contract, plan, authority, permission, and
lease identity and prevent support assignment or external-effect counts from
changing. Each accepted step adds exactly one receipt. Countermodels reject
identity substitution, replay, authority leakage, unlocked contracts, approval
bypass, missing permission or lease, scheduler and dispatch gaps, retry without
idempotency, retry authority widening, unacknowledged cancellation, output
after acknowledged cancellation, missing artifacts or audit, unverified
adjudication, missing completion/replay/residual custody, and unacknowledged
closure. A six-event witness reaches closure with one represented execution
observation, six receipts, zero assigned support, and zero external effects.

The independent consumer covers all twenty-eight routes, consumes the exact
2/7 delivery and 2/9 durable-lifecycle suites, and rejects 42 mutations across
identity, sequencing, authority, approval, permission, lease, retry,
cancellation, artifact, audit, verification, receipt, replay, residual, and
consumer boundaries.

## Assumptions, exclusions, and adequacy verdict

Identifiers, digests, approval flags, permission and lease facts, scheduler
availability, retry/idempotency declarations, cancellation acknowledgments,
artifact/audit presence, verification results, receipts, replay references,
residual owners, and consumer acknowledgments are trusted inputs. The model is
adequate for the exact represented lifecycle, route priority, identity custody,
receipt accounting, and authority separation. It is inadequate for scheduler
quality, worker or model competence, task success, output truth, verification
soundness, idempotence in fact, enforcement, durable recovery, cancellation
efficacy, receipt/replay truth, natural workloads, useful throughput, costs,
causality, safety, deployment, reproduction, transfer, SOTA, AGI, ASI, or
chapter-core support.

## Disposition

Retire the valid-transition record projection and the two generic fixture-
summary projections in `AsiStackProofs.TypedJobs`. Retain the exact approval
countermodel, twelve finite execution routes, and eleven durable-lifecycle
countermodels/witnesses at bounded legacy scope. Move all five public targets
to the refinement module. No support state changes.
