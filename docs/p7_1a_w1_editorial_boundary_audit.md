# P7.1a W1 Editorial Boundary Audit

Status: **terminal complete** for
`P7.1a-W1-template-centralization-and-boundary-coverage`.

## Result

The 55 activation-era chapters no longer repeat the two large evidence-method
templates. One canonical contract now lives in
[Living Book Methodology](../chapters/living-book-methodology.qmd#chapter-evidence-packet-contract),
and each historical chapter keeps a compact projection containing only its
identity, counts, evidence lanes, strongest bundle, controls, transitions,
maximum inference, and replay burden. The immutable activation packets remain
pinned in the P7 lineage record; the live projections have a separate digest
and rejecting validator.

Using one declared 12-gram tokenizer against commit `941858574` and the current
55-chapter set, repeated 12-grams appearing in at least eight chapters fell
from 1,142 to 728 (36.25%). Word tokens now total 396,944 versus the 412,044
baseline (3.66% lower).
The roadmap's older frozen count was 1,364; that number is retained as
historical provenance rather than silently presented as reproducible under the
current tokenizer. Maximum spread remains 55 because compact table field names
and one link to the canonical method intentionally remain shared. This packet
is only W1, so it does not claim the full P7.1a 15–25% reader-spine reduction.

## Boundary repairs

- Retired-chapter archive bookkeeping moved out of the openings of
  `virtual-context-abi`, `intent-to-execution-contracts`, and
  `spinoza-verification-and-proof-carrying-claims` into named end provenance
  notes.
- Scalable Oversight now has a named epistemic-security and persuasion-defense
  section grounded in three bounded source notes and the existing frozen
  persuasion-theater atom.
- Failure Modes now has a named gradual-disempowerment and option-value-loss
  section grounded in a passage-reviewed arXiv v2 source note and routed to two
  existing frozen atoms. It does not mutate the protected 3,745-atom terminal
  denominator.

## Meaning and inference custody

The generator keeps every chapter-specific terminal count, core state,
attempted and missing lane, bundle scope, negative control, accepted transition,
maximum inference, and reproduction burden. The canonical method states why a
family-level success cannot fill an atom-specific gap or promote a chapter.
No terminal atom row, equation, source assignment, proof boundary, accepted
transition, or chapter-core support state was deleted or promoted by this
edit.

The persuasion sources support evaluation design, not a general persuasion or
mitigation claim. The gradual-disempowerment source supports a systemic-risk
obligation map, not inevitability, probability, timing, validated indicators,
or intervention efficacy. Both sections state these non-claims directly.

## Reproduction

Run:

```bash
python3 scripts/validate_p7_1a_w1_editorial_boundary_audit.py
python3 scripts/validate_repeated_prose.py
python3 scripts/validate_p7_book_evidence_reconciliation.py
```

The first validator recomputes the before/after repetition denominator, checks
the protected atom ledger, verifies packet fields, source assignments, named
sections, non-claims, and consolidation-note placement, and rejects registered
mutations.
