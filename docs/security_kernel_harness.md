# Security Kernel Harness

Last updated: 2026-06-28

The eighteenth Phase 5 harness checks synthetic authority-use receipt fixtures
under `experiments/security_kernel/`.

## What It Checks

- Authority use must be mediated by `handle://` references rather than
  model-visible secret material.
- Purpose, destination, and allowed action must stay scoped rather than
  granting ambient or unbounded authority.
- Approval records must reference concrete approval artifacts.
- SCIF lifecycle records must include spawn, inject, execute, sanitize,
  zeroize, commit, and audit events.
- Sanitized outputs must mark redaction or sanitization and must not expose
  secret bytes, live handles, credentials, passwords, or API-key-like material.
- Prompt-injection probes must return a blocked, refused, redacted, or
  sanitized result.
- Residual leak-risk notes must preserve explicit runtime and support-state
  non-claim boundaries.
- Revocation paths must name expiry, revocation, deletion, lease closure, or
  zeroization.

## Command

```bash
python3 scripts/validate_security_kernel.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Security kernel harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

The result record is `experiments/security_kernel/results/2026-06-28-local.md`.

## Boundary

This is a synthetic security-kernel receipt-discipline slice. It makes part of
the Security Kernel and Digital SCIFs chapter executable at the record level:
handle mediation, approval artifacts, bounded action scope, SCIF lifecycle,
sanitization, residual leak-risk notes, revocation paths, and prompt-injection
non-disclosure boundaries have to line up.

It is not a kernel-security result, sandbox-isolation result, side-channel
safety result, prompt-injection containment result, secret-handle safety result,
least-privilege context result, runtime-policy trace, source-interpretation
review, reader-release review, or proof of deployed security. It does not
promote Appendix C, validate deployed AI behavior, or approve reader artifacts.
