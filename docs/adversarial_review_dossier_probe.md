# Adversarial Review Dossier Probe

The Adversarial Review Dossier Probe is a deterministic synthetic
review-dossier fixture for the
`spinoza-verification-and-proof-carrying-claims` chapter.

It validates two valid synthetic review dossiers and seven expected-invalid controls.
The valid dossiers cover a scoped acceptance that preserves dissent and
unresolved deployment limits, plus a semantic-mismatch rejection that blocks
support promotion until the claim boundary is rewritten. The controls reject
missing dossier refs, LLM-judge-only acceptance, missing adversarial probes,
dissent whose scope constraint is erased, action verdicts without required
actions, prior-review reuse without an unchanged-evidence guard, and
support-state promotion from the fixture.

Run:

```bash
python3 scripts/validate_adversarial_review_dossier_probe.py
```

The local result record is:

```text
experiments/adversarial_review_dossier/results/2026-07-02-local.json
```

This probe does not prove semantic equivalence, prove reviewer independence,
prove adversarial-probe quality, prove verdict correctness, run an LLM judge,
run a debate system, or promote the chapter support state. In short: no support-state transition.
