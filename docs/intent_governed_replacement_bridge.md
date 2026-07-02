# Intent-Governed Replacement Bridge

This note records a deterministic synthetic bridge between the Command
Contracts chapter and the Capability Replacement and Rollback chapter.

Command:

```bash
python3 scripts/validate_intent_governed_replacement_bridge.py
```

Generated result:

```text
experiments/intent_governed_replacement_bridge/results/2026-07-02-local.json
```

The bridge validates two valid synthetic bridge traces and six
expected-invalid controls. The valid traces show:

- a command-authorized replacement request that can enter `canary_only`;
- a default-replacement request that is blocked when the required approval
  receipt is absent.

Expected-invalid controls reject:

| Control | Rejection reason |
|---|---|
| `invalid_missing_intent_reference` | Replacement admission lacks an intent contract reference. |
| `invalid_authority_widening_from_intent` | Replacement authority exceeds the intent authority ceiling. |
| `invalid_stop_condition_erasure` | Stop conditions fail to survive into the replacement transaction. |
| `invalid_default_without_approval_but_promoted` | Default promotion proceeds without the required approval receipt. |
| `invalid_missing_rollback_owner` | Rollback ownership is absent. |
| `invalid_support_promotion_overclaim` | The bridge claims a support-state effect. |

This is a bridge over public-safe synthetic records. It does not parse
natural-language intent, execute deployed replacement behavior, prove
approval-service enforcement, prove regression-suite quality or monitor
quality, execute production rollback, promote any chapter core claim, or
create a support-state transition. In short: no support-state transition.
