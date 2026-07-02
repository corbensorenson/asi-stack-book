# Intent-to-Execution Handoff Probe

The Intent-to-Execution Handoff Probe is a synthetic vertical trace check for
the chapter `intent-to-execution-contracts`.

It validates two valid synthetic handoff traces and seven expected-invalid controls.
The valid traces cover an accepted command path from intent receipt
through command, plan, typed job, dispatch receipt, synthetic adapter receipt,
artifact reference, verifier reference, feedback, and residuals, plus a
missing-approval path that stops with a block receipt before dispatch. The
controls reject dispatch without approval, authority widening, hidden override
application, missing dispatch receipt, side effect without adapter receipt,
residual erasure, and missing artifact-to-parent links.

Run:

```bash
python3 scripts/validate_intent_execution_handoff_probe.py
```

The local result record is:

```text
experiments/intent_execution_handoff/results/2026-07-02-local.json
```

This probe does not parse natural-language intent, execute a deployed
dispatcher or runtime adapter, prove approval-service enforcement, prove
artifact satisfaction, promote the chapter support state, or create a
support-state transition. In short: no support-state transition.
