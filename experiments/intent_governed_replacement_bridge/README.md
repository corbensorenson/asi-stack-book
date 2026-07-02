# Intent-Governed Replacement Bridge

Run:

```bash
python3 scripts/validate_intent_governed_replacement_bridge.py --write-result
python3 scripts/validate_intent_governed_replacement_bridge.py
```

The result record is written to:

```text
experiments/intent_governed_replacement_bridge/results/2026-07-02-local.json
```

This bridge checks command authority into replacement admission with synthetic
public-safe records only. It is not a deployed parser, dispatcher, replacement
runner, approval service, monitor, rollback service, or support-state
promotion.
