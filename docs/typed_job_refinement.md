# Typed-job versioned execution and closure refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`AsiStackProofs.TypedJobRefinement` replaces a valid-record projection and two
generic fixture-summary bridges with a reachable seven-stage lifecycle: idle,
contract-locked, authorized, dispatched, executed, adjudicated, and closed. It
binds exact job/version, parent contract, plan node, authority, permission,
lease, scheduler, consumer, and event identities. Admission requires contract
lock, approval when required, permissions, an active lease, a scheduler slot,
and an explicit dispatch request. Execution preserves retry identity and
authority, makes cancellation visible, and requires output artifacts and an
audit trail. Adjudication requires verification, completion and replay
receipts, and residual ownership; closure requires consumer acknowledgment.

`python3 scripts/validate_typed_job_refinement.py` independently recomputes all
twenty-eight routes, consumes the exact two-valid/seven-invalid delivery and
two-valid/nine-invalid durable-lifecycle suites, executes the six-event
witness, and rejects all 42 mutations.

## Exact boundary

This is finite authored structured-record evidence. It does not establish
scheduler quality, worker or model capability, task success, output truth,
verification soundness, idempotence in fact, approval-service correctness,
permission enforcement, lease-service correctness, cancellation efficacy,
retry recovery, artifact truth, audit completeness, completion-receipt or
replay correctness, consumer behavior, usefulness, cost advantage, causality,
safety, deployment, reproduction, or transfer. The closed record creates no
support movement, evidence promotion, external effect, release authority, SOTA
result, AGI claim, or ASI claim.
