# Intent Re-contract Trigger Probe

This directory contains the public-safe local result for the Intent re-contract trigger probe.

Run:

```bash
python3 scripts/run_intent_recontract_probe.py --write-result
python3 scripts/validate_intent_recontract_probe.py
```

Current result:

- `results/2026-07-02-local.json`

The result records `valid_no_material_delta_continue`, `valid_publication_surface_delta_recontracts`, and seven expected-invalid controls: `invalid_authority_delta_without_recontract`, `invalid_private_source_delta_without_recontract`, `invalid_stop_condition_erasure_without_recontract`, `invalid_evidence_bar_weakening_without_recontract`, `invalid_affected_party_widening_without_recontract`, `invalid_means_expansion_without_recontract`, and `invalid_support_state_promotion_without_recontract`.

This is a no natural-language-intent-understanding, deployed-parser-quality, deployed-authority-extraction, prompt-injection-containment, runtime-dispatch, approval-service, user-satisfaction, or support-state-promotion claim.
