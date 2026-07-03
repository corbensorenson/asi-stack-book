# Epistemic Trusted Computing Base Fixture

Command:

```bash
python3 scripts/validate_epistemic_trusted_computing_base.py
```

Result:

```text
experiments/epistemic_tcb/results/2026-07-03-local.json
```

This fixture is the first bounded artifact for the epistemic trusted computing
base. It asks where verification trust bottoms out, how trust is delegated, and
what remains outside the trusted core. Its explicit boundary is no support-state
promotion from a well-shaped trust-base record.

The fixture rejects verifier-trust laundering and preserves a no support-state promotion boundary.

The validator accepts three honest records:

| Case | Meaning |
|---|---|
| `valid_minimal_epistemic_tcb_record` | A bounded trust-base record with named root policy, artifact graph, independent verifier, append-only audit log, recursion stop condition, outside-TCB residuals, and no support-state effect. |
| `valid_delegated_verifier_record_only` | A delegated verifier can be recorded when a consumer policy checks the delegation receipt and the result remains record-only. |
| `valid_outside_tcb_blocked_record` | A self-verifier route can be preserved as a blocked negative record when it explicitly says the verifier is outside the trusted core and cannot promote support. |

It rejects six controls:

| Control | Rejection boundary |
|---|---|
| `invalid_missing_root_of_trust` | A support-review request needs a named root of trust. |
| `invalid_self_verifier_laundering` | A claim producer cannot verify itself into support review. |
| `invalid_unbounded_trust_propagation` | Ambient trust and unbounded propagation are rejected. |
| `invalid_no_recursion_stop_condition` | The trust chain must say where recursion stops. |
| `invalid_outside_tcb_residual_erased` | Assumptions and outside-core duties cannot be erased. |
| `invalid_support_promotion_from_tcb_shape` | A trust-base record shape cannot promote chapter-core support. |

Lean bridge:

- `epistemic_tcb_fixture_bridge` in
  `lean/AsiStackProofs/ArtifactGraph.lean` mirrors the finite fixture summary:
  minimal trust base accepted, delegated verifier record accepted only as
  record-only, outside-TCB self-verifier path accepted only as blocked, missing
  root of trust rejected, self-verifier laundering rejected, unbounded trust
  rejected, missing recursion stop rejected, erased residuals rejected,
  support promotion from trust-base shape rejected, no support-state effect,
  and non-claim boundary.

Non-claims:

- This does not prove verifier correctness.
- This does not prove an open-world epistemic trusted computing base.
- This does not prove deployed trust-base behavior.
- This does not prove audit-log durability, policy correctness, or verifier
  independence outside the finite records.
- This does not create an evidence transition or support-state transition.
- This does not promote any chapter core claim.
