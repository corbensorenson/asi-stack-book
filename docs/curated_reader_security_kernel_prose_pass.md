# Curated Reader Prose Pass: Security Kernel and Digital SCIFs

Last updated: 2026-07-02

Chapter ID: `security-kernel-and-digital-scifs`

Curated reader file:
`editions/reader_manuscript/v1_0/chapters/security-kernel-and-digital-scifs.qmd`

## Reader Promise

A human reader should leave this chapter understanding that security in the ASI
Stack is a least-exposure operating discipline: models may request and reason
about privileged work, but secrets and protected authority should move through
handles, leases, compartments, receipts, sanitization, and revocation rather
than ordinary model-visible context.

## Scope

This pass turns the generated reader baseline for Security Kernel and Digital
SCIFs into a first booklike curated reader draft. It is a reader-prose
derivative only.

Allowed curation scopes used:

- chapter opening and closing;
- pacing;
- paragraph ordering;
- section flow;
- transition prose;
- sentence-level voice;
- chapter compression.

Proof/test boundary clarification is recorded as meaning preservation, not as
permission to change proof or test status.

## What Changed

- Reworked the opening around the question of what a new capability can touch,
  not only what it can do.
- Reframed the chapter around least exposure, handle leases, Digital SCIF
  lifecycle, Authority Use Receipts, and sanitized commits.
- Preserved the security-kernel Mermaid sequence and made the diagram's "map of
  absence" role explicit for human readers.
- Clarified that OWASP, NIST Zero Trust, and Saltzer-Schroeder are external
  comparators, not conformance evidence.
- Preserved the live chapter's current evidence boundary: synthetic
  security-kernel receipt checks and finite Lean predicates support record
  discipline only; the receipt checks now include expired-approval and
  overbroad-SCIF-context negative fixtures, and the Resource Budget Ledger
  harness now includes a security-overhead erasure negative fixture, but they
  do not prove deployed containment, sandbox isolation, side-channel
  resistance, prompt-injection containment, runtime policy behavior, runtime
  budget enforcement, or source interpretation.
- Preserved the core claim, minimum viable implementation, beyond-state-of-the-
  art endpoint, and handoff into Recursive Self-Improvement Boundaries.
- Added a 2026-07-02 handle-and-SCIF scenario around summarizing a private
  source folder, separating handle visibility, scoped read requests,
  compartment admission, prompt-injection handling, sanitized commits,
  zeroization/expiry receipts, residual leak risk, and support-state non-claims.

## Meaning Preservation Checks

| Check | Result |
|---|---|
| Core claim meaning preserved | Pass. The curated draft keeps the claim that sensitive context and privileged actions should be mediated by kernel-like security mechanisms and compartmentalized Digital SCIFs. |
| Support-state boundary preserved | Pass. The curated draft states that the live book keeps the claim at `argument` support. |
| Source boundary preserved | Pass. No new source IDs, source facts, citations, or external claims were introduced by this pass; external security sources remain comparators only. |
| Proof/test status preserved | Pass. The curated draft keeps the boundary that current synthetic harnesses and finite Lean predicates prove receipt discipline only, not runtime security containment. |
| Implementation horizon preserved | Pass. The minimum viable implementation remains fake-secret/receipt validation and public-safe toy traces; the mature endpoint remains an unvalidated least-exposure operating layer. |
| Release blockers preserved | Pass. No reader release record, format review, reconciliation approval, EPUB, DOCX, PDF, HTML, or audio artifact is approved by this pass. |

## Non-Claims

- This pass does not change the live AI/research chapter.
- This pass does not change `book_structure.json`.
- This pass does not alter Appendix C, source assignments, proof targets, test
  statuses outside the security-kernel reader reconciliation, implementation
  horizons, or release records.
- This pass does not approve the curated chapter for reader release.
- This pass does not create EPUB, DOCX, PDF, HTML, audio, or audio-embedded EPUB
  artifacts.
- This pass does not promote any chapter core claim or non-core claim.
- This pass does not claim OWASP conformance, NIST zero-trust implementation,
  Saltzer-Schroeder completeness, deployed security-kernel behavior, sandbox
  isolation, side-channel resistance, prompt-injection containment,
  deployed approval-expiry enforcement, least-privilege context behavior,
  secret-handle safety, runtime budget enforcement, security economics, or
  runtime policy enforcement, privacy protection, approval-service behavior, or
  support-state promotion.

## Remaining Blockers

- `reader_release_record_not_created`
- `format_artifact_not_reviewed`
- `curated_reconciliation_not_approved`

Before this curated source can be release input, the reader manuscript needs a
full reconciliation pass against the live chapter, generated baseline,
support-state boundaries, implementation horizons, and exact rendered reader
artifacts.
