# Artifact Steward Lifecycle Probe

Status: implemented local public-safe probe
Command: `python3 scripts/run_artifact_steward_lifecycle_probe.py --write-result`
Validator: `python3 scripts/validate_artifact_steward_lifecycle_probe.py`
Result: `experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json`

## Scope

The Artifact steward lifecycle probe composes the existing public protocol fixtures for steward charters, work contracts, contribution ledgers, treasury policy, event taint, steward decisions, sunset review, and federation leases into a deterministic route decision record. It is an executable bridge between record-shape validation and the finite Lean lifecycle envelopes.

The probe does not run a steward. It does not move funds, merge branches, publish releases, dispatch external workers, scan live events, call a network service, or update support states.

## Checked routes

The current result records three valid scenario routes:

- `valid_bounded_work_dispatch_proposal`: a complete bounded work contract routes to `prepare_bounded_work_dispatch`; no worker or tool is executed.
- `valid_clean_release_review_proposal`: a reviewed event, separated contribution ledger, zero spend, complete release evidence, and no sunset trigger route to `prepare_release_review`; no release is published.
- `valid_sunset_review_route`: met sunset criteria with no open review route to `open_sunset_review`; ordinary work remains blocked.

The current result records 23 expected-invalid controls. Six preserve the
original lifecycle boundaries:

- `invalid_tainted_event_without_review`: unreviewed tainted event text routes to `quarantine_event`.
- `invalid_over_policy_treasury_spend`: spend above the zero autonomous policy without approval routes to `request_treasury_approval`.
- `invalid_contribution_governance_laundering`: collapsed contribution score used for governance routes to `reject_collapsed_governance`.
- `invalid_unscoped_federation_contract`: an external worker path that inherits project authority routes to `reject_federation_authority_inheritance`.
- `invalid_release_without_gate_evidence`: a release candidate with missing evidence, residual, and approval records routes first to `repair_release_evidence`.
- `invalid_sunset_criteria_ordinary_work`: ordinary work requested after sunset criteria are met routes to `open_sunset_review` and keeps ordinary work disallowed.

Nine work-contract controls independently remove objective, authority basis,
authority containment, the tool boundary, verification, budget presence,
budget-policy compliance, rollback, or the non-claim boundary. Each reaches
the exact repair, refusal, or approval state named by the Lean transition
model. Eight release controls independently remove artifact binding, tests,
evidence, changelog, residuals, approval, the no-promotion boundary, or the
non-claim boundary. None can reach external-review readiness.

The validator independently re-encodes those seventeen new boundary mutations
and checks all 37 theorem declarations in
`AsiStackProofs.ArtifactStewardAgents`. The arbitrary-length Lean run
invariants establish that a dispatch-ready or external-review-ready state can
be reached only from a complete modeled packet. Those states are review
eligibility only; neither transition system contains an execution or
publication state.

The result digest is recorded in the JSON under `summary.decision_digest`; the validator recomputes it from scenario IDs, routes, reasons, pass flags, and outcomes.

## Non-claims

This is a no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim.

The probe does not prove treasury safety, legal authority, governance correctness, contributor fairness, workflow-injection resistance, capture resistance, release safety, federation safety, steward autonomy, project quality, or AI safety. It only checks a generated public-safe lifecycle decision envelope over fixture-derived fields.
