# Intent Intake Probe

The intent intake probe is a synthetic corpus check for the chapter
`human-intent-as-a-formal-input`.

It validates four bounded natural-language request transformations and six
expected-invalid controls. The request classes cover urgency, trust language,
omitted means, private-source publication pressure, declared stop conditions,
and bounded defaults.

Run:

```bash
python3 scripts/validate_intent_intake_probe.py
```

The local result record is:

```text
experiments/intent_intake_probe/results/2026-07-02-local.json
```

This probe does not prove natural-language understanding, deployed authority
extraction, prompt-injection containment, runtime dispatch, approval-service
behavior, user satisfaction, or support-state promotion. It only checks that
this finite corpus rejects a few common ways natural-language request pressure
can be laundered into authority.
