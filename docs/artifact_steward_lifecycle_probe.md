# Artifact Steward Lifecycle Probe

Status: implemented local public-safe probe
Command: `python3 scripts/run_artifact_steward_lifecycle_probe.py --write-result`
Validator: `python3 scripts/validate_artifact_steward_lifecycle_probe.py`
Result: `experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json`

## Scope

The Artifact steward lifecycle probe composes the existing public protocol fixtures for steward charters, work contracts, contribution ledgers, treasury policy, event taint, steward decisions, sunset review, and federation leases into a deterministic route decision record. It is an executable bridge between record-shape validation and the finite Lean lifecycle envelopes.

The probe does not run a steward. It does not move funds, merge branches, publish releases, dispatch external workers, scan live events, call a network service, or update support states.

## Checked routes

The current result records two valid scenario routes:

- `valid_clean_release_review_proposal`: a reviewed event, separated contribution ledger, zero spend, complete release evidence, and no sunset trigger route to `prepare_release_review`; no release is published.
- `valid_sunset_review_route`: met sunset criteria with no open review route to `open_sunset_review`; ordinary work remains blocked.

The current result records six expected-invalid controls:

- `invalid_tainted_event_without_review`: unreviewed tainted event text routes to `quarantine_event`.
- `invalid_over_policy_treasury_spend`: spend above the zero autonomous policy without approval routes to `request_treasury_approval`.
- `invalid_contribution_governance_laundering`: collapsed contribution score used for governance routes to `reject_collapsed_governance`.
- `invalid_unscoped_federation_contract`: an external worker path that inherits project authority routes to `reject_federation_authority_inheritance`.
- `invalid_release_without_gate_evidence`: a release candidate with missing evidence, residual, and approval records routes to `block_release_evidence_gate`.
- `invalid_sunset_criteria_ordinary_work`: ordinary work requested after sunset criteria are met routes to `open_sunset_review` and keeps ordinary work disallowed.

The result digest is recorded in the JSON under `summary.decision_digest`; the validator recomputes it from scenario IDs, routes, reasons, pass flags, and outcomes.

## Non-claims

This is a no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim.

The probe does not prove treasury safety, legal authority, governance correctness, contributor fairness, workflow-injection resistance, capture resistance, release safety, federation safety, steward autonomy, project quality, or AI safety. It only checks a generated public-safe lifecycle decision envelope over fixture-derived fields.
