# Security Kernel Harness

Last updated: 2026-08-02

The eighteenth Phase 5 harness checks synthetic authority-use receipt fixtures
under `experiments/security_kernel/`.

## What It Checks

- Authority use must be mediated by `handle://` references rather than
  model-visible secret material.
- Purpose, destination, and allowed action must stay scoped rather than
  granting ambient, unbounded, or all-context authority.
- Approval records must reference concrete approval artifacts and must not be
  expired, revoked, stale, superseded, or reused.
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
- The Lean module must compile with the exact 23-theorem transaction-lifecycle
  surface.
- An independently implemented eight-event transaction must preserve exact
  identity, non-authority, a non-increasing ceiling, sanitization before
  independent declassification, zeroization before commit, and exact finite
  descendant revocation.
- Nine lifecycle mutations must reject stale version, ambient context,
  unmediated or expired injection, raw-secret output, self-declassification,
  premature commit, partial descendant revocation, and security-claim
  laundering.

## Command

```bash
python3 scripts/validate_security_kernel.py
```

## Current Local Result

The 2026-08-02 local revalidation passed:

```text
Security kernel harness passed: 3 valid fixture(s), 8 expected-invalid fixture(s). Security kernel formal binding passed: 2 retained authority-route theorem binding(s), 23 transaction-lifecycle theorem(s), 8 accepted event(s), and 9 rejecting lifecycle control(s).
```

The result lineage remains in
`experiments/security_kernel/results/2026-07-01-local.md`, with the dated
2026-08-02 lifecycle revalidation appended rather than replacing the original
fixture result.

## Boundary

This is a synthetic security-kernel receipt-discipline slice. It makes part of
the Security Kernel and Digital SCIFs chapter executable at the record level:
handle mediation, approval artifacts, approval-expiry refusal, bounded action
scope, overbroad-SCIF-context refusal, SCIF lifecycle, sanitization, residual
leak-risk notes, revocation paths, and prompt-injection non-disclosure
boundaries have to line up.

It is not a kernel-security result, sandbox-isolation result, side-channel
safety result, prompt-injection containment result, secret-handle safety result,
deployed approval-expiry enforcement, least-privilege context result,
sanitizer or declassifier competence, effect-complete runtime revocation,
security-overhead budget-preservation result, runtime-policy trace,
source-interpretation review, reader-release review, or proof of deployed
security. It does not promote Appendix C, validate deployed AI behavior, or
approve reader artifacts.
