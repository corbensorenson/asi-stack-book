# Human Oversight Degradation Fixture

Command:

```bash
python3 scripts/validate_human_oversight_degradation.py
```

Result:

```text
experiments/human_oversight_degradation/results/2026-07-03-local.json
```

This fixture is the first bounded artifact for human oversight degradation. It
treats human approval as a degradable control component, not as magic safety:
approval fatigue, rubber-stamping, alarm fatigue, and automation bias can route
an approval record away from accepted dispatch even when a reviewer clicked
"approve."

The fixture rejects approval laundering and preserves a no support-state promotion boundary.

The validator accepts three honest records:

| Case | Meaning |
|---|---|
| `valid_scoped_restored_reviewer_approval` | A qualified reviewer gives scoped, active approval with independent evidence checked, low fatigue indicators, case-specific rationale, required non-claims, and no support-state effect. |
| `valid_fatigue_routed_to_reviewer_rotation` | A qualified reviewer is overloaded; the record remains valid only because it routes to delay or reviewer rotation rather than accepted dispatch. |
| `valid_automation_bias_blocked_record` | The automation recommendation conflicts with visible evidence and lacks independent evidence checking; the record is valid as a blocked automation-bias case. |

It rejects seven controls:

| Control | Rejection boundary |
|---|---|
| `invalid_missing_reviewer_qualification` | A high-impact approval needs a qualified reviewer. |
| `invalid_fatigued_reviewer_accepted` | High approval load and consecutive approvals route to delay or reviewer rotation, not accepted dispatch. |
| `invalid_rubber_stamp_approval_accepted` | A very short template-only approval is treated as rubber-stamping. |
| `invalid_automation_bias_contradiction_ignored` | A recommendation with visible contradiction and no independent evidence check is blocked. |
| `invalid_alarm_fatigue_ordinary_approval` | High alert load and false-positive rate route to alarm-fatigue escalation. |
| `invalid_support_promotion_from_human_approval` | Human approval cannot promote a chapter core claim or evidence support state. |
| `invalid_missing_non_claim_boundary` | Approval records must preserve non-claims around approval-service quality, deployed human-factors behavior, and chapter-core support. |

Lean bridge:

- `human_oversight_degradation_fixture_bridge` in
  `lean/AsiStackProofs/RuntimeAdapters.lean` mirrors the finite fixture summary:
  scoped approval accepted, fatigue routed to reviewer rotation, automation bias
  blocked, missing qualification rejected, fatigued acceptance rejected,
  rubber-stamping rejected, alarm fatigue escalated, support promotion rejected,
  non-claim boundary required, no support-state effect, and no chapter-core
  support effect.

Non-claims:

- This does not prove reviewer correctness.
- This does not prove approval-service quality.
- This does not prove deployed human-factors behavior.
- This does not prove that human oversight cannot be manipulated.
- This does not create an evidence transition or support-state transition.
- This does not promote any chapter core claim.
