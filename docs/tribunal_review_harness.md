# Tribunal Review Harness

Last updated: 2026-06-28

The thirteenth Phase 5 harness checks synthetic tribunal-review fixtures under
`experiments/tribunal_review/`.

## What It Checks

- High-risk and critical reviews must preserve dossier refs, reviewer roles,
  and adversarial probes.
- Accept verdicts must carry evidence refs, findings, and an issued verdict
  state.
- Revise, reject, escalate, or blocked verdicts must preserve required actions
  and constraint effects.
- Substantive dissent must remain visible through unresolved issues and, when
  accepting within scope, constraint effects.
- Prior reviews must carry an unchanged-evidence guard that blocks laundering
  or requires new evidence or corrected mapping.
- Fixtures must deny reviewer-independence, verdict-correctness, runtime, and
  support-state-promotion claims.

## Command

```bash
python3 scripts/validate_tribunal_review.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Tribunal review harness passed: 3 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is `experiments/tribunal_review/results/2026-06-28-local.md`.

## Boundary

This is a synthetic tribunal-review record-discipline slice. It makes part of
the Unified Adaptive Tribunal and Adversarial Review chapter executable at the
record level: dossier boundaries, role separation, adversarial probes, dissent,
prior-review guards, required actions, constraint effects, and non-claims have
to line up.

It is not a reviewer-independence audit, adversarial-review quality result,
consensus-quality result, verdict-correctness result, source-interpretation
review, runtime trace, reader-release review, or proof of whole-system
epistemic correctness. It does not promote Appendix C, prove tribunal quality,
validate deployed AI behavior, or approve reader artifacts.
