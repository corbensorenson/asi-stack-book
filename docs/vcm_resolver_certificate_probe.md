# VCM Resolver/Certificate Probe

Status: implemented local public-safe probe
Command: `python3 scripts/run_vcm_resolver_certificate_probe.py --write-result`
Validator: `python3 scripts/validate_vcm_resolver_certificate_probe.py`
Result: `experiments/vcm_resolver_certificate_probe/results/2026-07-02-local.json`

## Scope

The VCM resolver/certificate probe is a deterministic public-safe check for the Virtual Context ABI chapter. It creates generated source-cell facts, a derived summary cell, resolver request records, and representation-certificate metadata. It then checks whether a context request can be materialized only when address, version, snapshot, mount, lease, source binding, omissions, authority ceiling, and certificate claim are consistent.

This is not a deployed VCM resolver, memory store, context compiler, model-facing context run, or semantic-fidelity benchmark.

## Checked routes

The current result records two valid scenario routes:

- `valid_resolver_materialization_receipt`: a matching address, version, snapshot, allowed mount, active lease, and consistent paired certificate route to `materialize_context`.
- `valid_mandatory_miss_typed_fault`: a mandatory missing address routes to `issue_typed_fault` and emits no materialization.

The current result records nine expected-invalid controls:

- `invalid_address_mismatch_materialization_denied`
- `invalid_version_mismatch_materialization_denied`
- `invalid_snapshot_mismatch_materialization_denied`
- `invalid_mount_policy_denied`
- `invalid_lease_expired_reuse_blocked`
- `invalid_certificate_source_binding_mismatch_denied`
- `invalid_certificate_authority_escalation_denied`
- `invalid_certificate_truthfulness_overclaim_denied`
- `invalid_summary_fidelity_omission_denied`

The result digest is recorded in the JSON under `summary.decision_digest`; the validator recomputes it from scenario IDs, routes, reasons, pass flags, and outcomes.

## Non-claims

This is a no deployed-resolver, memory-store, context-compiler, open-domain-summary-fidelity, certificate-truthfulness, transaction-isolation, deletion-enforcement, model-facing-context-quality, VCM-Bench, leak-prevention, or support-state-promotion claim.

The probe does not prove deployed resolver correctness, memory-store behavior, planner-guided context compilation, open-domain summary fidelity, certificate truthfulness, transaction isolation, deletion enforcement, model-facing context quality, contradiction-rate improvement, distractor resistance, VCM-Bench performance, leak prevention, or AI safety. It uses generated public-safe source-cell facts only; it does not read private source text, copy raw source payloads, call a network service, run a model, access a live memory store, or materialize real user data.
