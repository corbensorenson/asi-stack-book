# VCM Resolver/Certificate Probe

This experiment directory stores a deterministic public-safe probe for the Virtual Context ABI chapter.

- Runner: `scripts/run_vcm_resolver_certificate_probe.py`
- Validator: `scripts/validate_vcm_resolver_certificate_probe.py`
- Result: `results/2026-07-02-local.json`

The probe checks two valid routes and nine expected-invalid controls:

- `valid_resolver_materialization_receipt`
- `valid_mandatory_miss_typed_fault`
- `invalid_address_mismatch_materialization_denied`
- `invalid_version_mismatch_materialization_denied`
- `invalid_snapshot_mismatch_materialization_denied`
- `invalid_mount_policy_denied`
- `invalid_lease_expired_reuse_blocked`
- `invalid_certificate_source_binding_mismatch_denied`
- `invalid_certificate_authority_escalation_denied`
- `invalid_certificate_truthfulness_overclaim_denied`
- `invalid_summary_fidelity_omission_denied`

This is a no deployed-resolver, memory-store, context-compiler, open-domain-summary-fidelity, certificate-truthfulness, transaction-isolation, deletion-enforcement, model-facing-context-quality, VCM-Bench, leak-prevention, or support-state-promotion claim.
