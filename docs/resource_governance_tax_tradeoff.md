# Resource Governance-Tax Trade-Off Model

Status: bounded deterministic fixture, local-only result.

Validation command:

```bash
python3 scripts/validate_resource_governance_tax_tradeoff.py
```

Tracked result:

- `experiments/resource_governance_tax_tradeoff/results/2026-07-03-local.json`

## Purpose

This fixture gives the Resource Economics chapter a first bounded answer to
the idea-depth question "when does the governance tax pay for itself?" It
models three valid route-selection scenarios and five expected-invalid
controls. Each route prices visible cost, verification cost, protected review
cost, reviewer burden, expected error cost, fallback cost, and residual
discharge cost.

The fixture intentionally permits one low-risk shortcut:
`valid_low_risk_shortcut_allowed`. Governance is not treated as a universal
tax that must always be paid. A shortcut can win when the task has no required
protected gate and its full cost remains lower after residuals, fallback, and
review burden are counted.

The fixture also records two cases where the governance tax pays for itself:
`valid_high_risk_governance_pays` and
`valid_hidden_residual_flips_selection`. In the first, high risk makes hidden
error, fallback, and residual costs dominate the apparently cheaper route. In
the second, the shortcut has lower visible cost, but full-cost accounting flips
the selection once hidden residual discharge and reviewer burden are priced.

## Negative Controls

The expected-invalid controls reject:

- `invalid_tax_erasure_selected_shortcut`: selecting a shortcut when governed
  full cost is lower.
- `invalid_protected_gate_deleted`: making governance cheap by deleting a
  required protected review gate.
- `invalid_residual_unpriced`: omitting residual discharge cost and selecting
  the shortcut.
- `invalid_support_state_promotion`: using the fixture shape to attempt a
  support-state or chapter-core promotion.
- `invalid_missing_comparator`: claiming a trade-off without both governed and
  ungoverned comparators.

## Lean Alignment

The result carries a finite Lean alignment record for
`lean:resource.governance_tax.tradeoff_bridge` in
`AsiStackProofs.ResourceEconomics`. The corresponding theorem refs are:

- `resource_governance_tax_tradeoff_fixture_valid`
- `resource_governance_tax_tradeoff_shows_governance_can_pay`
- `resource_governance_tax_tradeoff_allows_low_risk_shortcut`
- `resource_governance_tax_tradeoff_preserves_no_promotion_boundary`

These theorems align only the bounded fixture summary: three valid scenarios,
five rejected controls, two governed selections, one allowed shortcut,
protected-gate deletion rejection, residual-pricing requirement, reviewer
burden pricing, and no support-state or chapter-core promotion.

## Weakening Condition

The governance-tax argument weakens if hidden review, fallback, residual, or
reviewer-burden costs do not change route choice, or if protected gates can be
deleted without a recorded residual and rejection.

## Non-Claims

- This fixture does not prove deployed scheduler behavior.
- This fixture does not measure real verification tax.
- This fixture does not prove economic optimality.
- This fixture does not promote the Resource Economics chapter core claim.
- This fixture does not create a support-state transition.
