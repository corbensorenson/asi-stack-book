# Receipt Faithfulness Adversarial Fixture

Command:

```bash
python3 scripts/validate_receipt_faithfulness.py
```

Result:

```text
experiments/receipt_faithfulness/results/2026-07-03-local.json
```

This fixture is the first bounded artifact for the record-reality gap: records
must correspond to the thing they claim to record, not only to the schema they
successfully satisfy. Its explicit boundary is no support-state promotion from
receipt shape alone.

The validator accepts three honest records:

| Case | Meaning |
|---|---|
| `valid_cross_checked_receipt_record` | A bounded receipt with a matching independent cross-check route, passing trap receipt, explicit attestation limits, and no support-state effect. |
| `valid_attestation_limited_record_only` | A shape-valid receipt whose attestation is explicitly limited to record fields and therefore remains record-only. |
| `valid_trap_detected_blocked_receipt` | A trap receipt detects a mismatch and preserves the record as negative evidence blocked from promotion. |

It rejects six controls:

| Control | Rejection boundary |
|---|---|
| `invalid_shape_valid_reality_false_promoted` | A shape-valid but reality-false receipt cannot request support review. |
| `invalid_trap_receipt_ignored` | A trap-receipt negative control cannot be ignored after failure. |
| `invalid_missing_independent_cross_check` | A support-review request needs an independent cross-check route. |
| `invalid_same_component_cross_check` | A same-component self-check cannot satisfy independence. |
| `invalid_attestation_overclaim` | Unbounded attestation without explicit limits is rejected. |
| `invalid_support_promotion_from_receipt_shape` | Receipt shape alone cannot promote support. |

Lean bridge:

- `receipt_faithfulness_adversarial_fixture_bridge` in
  `lean/AsiStackProofs/ArtifactGraph.lean` mirrors the finite fixture summary:
  cross-checked record accepted, attestation-limited record accepted only as
  record-only, trap-detected false receipt accepted only as blocked negative
  evidence, shape-valid false receipt rejected, trap-receipt failure rejected,
  independent cross-check required, attestation limits recorded, support
  promotion from receipt shape rejected, no support-state effect, and non-claim
  boundary.

Non-claims:

- This does not prove receipt truth.
- This does not prove open-world receipt faithfulness.
- This does not prove verifier independence or attestation-service
  correctness.
- This does not prove deployed attestation or audit behavior.
- This does not promote any chapter core claim.
- This does not create an evidence transition or support-state transition.

Accepted no-promotion decision:
`evidence_transitions/v1_x_measured/artifact_receipt_faithfulness_no_change.json`
records this fixture as a `blocks_promotion` side-lane decision. The decision
keeps the finite fixture useful as a receipt-reality guard while blocking
open-world receipt-faithfulness, verifier-independence,
attestation-service-correctness, deployed-audit-behavior, benchmark,
model-quality, safety, ASI, support-state-promotion, and Artifact Graphs
chapter-core-promotion claims until stronger evidence exists.
