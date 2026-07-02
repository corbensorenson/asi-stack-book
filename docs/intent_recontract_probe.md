# Intent Re-contract Trigger Probe

Status: implemented local book-gate probe.

Command:

```bash
python3 scripts/run_intent_recontract_probe.py --write-result
python3 scripts/validate_intent_recontract_probe.py
```

Result record:

- `experiments/intent_recontract_probe/results/2026-07-02-local.json`

## Purpose

The Intent re-contract trigger probe checks whether a structured intent contract stays authoritative when downstream work proposes a material delta. It is scoped to generated public-safe records: an accepted synthetic intent contract, downstream delta records, route decisions, no-effect markers, and non-claim boundaries.

The probe does not parse private user text and does not infer hidden intent. It checks a narrower contract rule: if downstream work changes allowed means, authority ceiling, affected parties, evidence bar, publication surface, source boundary, stop conditions, or support-state effect, the work must either return to the contract boundary or be blocked before dispatch.

## Routes

Valid routes:

- `valid_no_material_delta_continue`
- `valid_publication_surface_delta_recontracts`

Expected-invalid controls:

- `invalid_authority_delta_without_recontract`
- `invalid_private_source_delta_without_recontract`
- `invalid_stop_condition_erasure_without_recontract`
- `invalid_evidence_bar_weakening_without_recontract`
- `invalid_affected_party_widening_without_recontract`
- `invalid_means_expansion_without_recontract`
- `invalid_support_state_promotion_without_recontract`

The result records two valid routes and seven expected-invalid controls. Invalid controls are blocked before dispatch, record changed trigger fields, and keep `support_state_effect=none`.

## Non-Claims

This is a no natural-language-intent-understanding, deployed-parser-quality, deployed-authority-extraction, prompt-injection-containment, runtime-dispatch, approval-service, user-satisfaction, or support-state-promotion claim.

The probe does not promote any chapter core claim. It does not create a support-state transition. It does not read private source text, call a network service, dispatch jobs, publish artifacts, or infer user intent from private conversation history.
