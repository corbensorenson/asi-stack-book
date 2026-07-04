# Claim-State Transition Bridge

This note records the bounded claim-state transition bridge for Evidence States
and Claim Discipline.

Command:

```bash
python3 scripts/validate_claim_state_transition_bridge.py
```

Result record:
`experiments/claim_state_transition_bridge/results/2026-07-04-local.json`.

Lean bridge:
`lean:evidence.claim_state.transition_bridge` in
`AsiStackProofs.EvidenceStates`.

## What It Checks

The bridge is a deterministic synthetic fixture over negative evidence
outcomes. It accepts three modeled claim-state movements:

- `valid_scope_narrowing_after_failed_mapping`: a failed source mapping narrows
  the claim while keeping support at `argument`.
- `valid_downgrade_after_failed_replay`: a failed replay downgrades a synthetic
  test-backed support state back to `argument`.
- `valid_terminal_refutation_after_counterexample`: a counterexample records a
  terminal refutation effect.

It rejects six mutation controls:

- `invalid_narrowing_without_negative_evidence`
- `invalid_downgrade_without_trigger`
- `invalid_refutation_without_terminal_effect`
- `invalid_support_promotion_laundered_as_narrowing`
- `invalid_missing_nonclaim_boundary`
- `invalid_live_claim_movement_claimed`

## Why It Matters

The support-state ladder is not only a promotion ladder. It must also show how
failed evidence narrows, downgrades, or refutes a claim without turning the
same record into an upward support move. This bridge checks that the modeled
negative-evidence path has three properties:

- negative evidence is required before a narrowing, downgrade, or refutation
  case can pass;
- support promotion laundering is rejected when a narrowing record tries to
  raise support;
- live chapter core claims remain unchanged by the synthetic fixture.

## Boundary

This is a finite synthetic record bridge. It does not demote, deprecate, or
refute any live chapter core claim. It does not prove source interpretation
adequacy, reviewer correctness, deployed belief-revision behavior, or
open-world evidence-state soundness. It does not create a support-state
promotion.

The weakening condition is explicit: the support-state ladder soundness
argument weakens if failed evidence cannot produce a recorded narrowing,
downgrade, or refutation without also allowing support promotion, live-claim
movement, or erased non-claims.
