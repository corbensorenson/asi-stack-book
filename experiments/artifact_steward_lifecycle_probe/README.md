# Artifact Steward Lifecycle Probe

This experiment directory stores a public-safe deterministic probe for the Artifact Steward Agents chapter.

- Runner: `scripts/run_artifact_steward_lifecycle_probe.py`
- Validator: `scripts/validate_artifact_steward_lifecycle_probe.py`
- Result: `results/2026-07-02-local.json`

The probe checks two valid routes and six expected-invalid controls:

- `valid_clean_release_review_proposal`
- `valid_sunset_review_route`
- `invalid_tainted_event_without_review`
- `invalid_over_policy_treasury_spend`
- `invalid_contribution_governance_laundering`
- `invalid_unscoped_federation_contract`
- `invalid_release_without_gate_evidence`
- `invalid_sunset_criteria_ordinary_work`

This is a no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim.
