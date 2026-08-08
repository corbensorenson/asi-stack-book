# P7.1a W3 Admission-Template Inheritance Guard

Status: **terminal complete** for
`P7.1a-W3-admission-template-inheritance-guard`.

## Result

W3 audits the exact current 84-chapter manifest, separates generated
source/evidence projections from reader-facing prose, centralizes the shared
lifecycle method in Living Book Methodology, and replaces one inherited
ten-chapter scaffold with domain-specific diagrams, interfaces, invariants,
evaluations, evidence plans, tests, summaries, and handoffs.

The editorial narrative projection falls from **812** to **0** distinct repeated 12-grams at a minimum spread of eight chapters; maximum spread moves from **14** to **0**. Exact editorial blocks of at least 24 words across five chapters fall from **0** to **0**.

The raw-QMD diagnostic is also retained (1,921 to 1,032). Its widest families are generated source and P7 evidence reconciliation packets with explicit generator owners; they are
not misreported as reader-facing editorial repetition.

## Method and custody

Normalization is Unicode NFKC with CRLF converted to LF. Tokens use
`[A-Za-z0-9_`'-]+`; n-grams are length 12 and count only
when present in at least eight distinct manifest chapters. The editorial
projection excludes front matter, status/source projections, generated marker
blocks, Markdown tables, and fenced blocks. Diagrams and Codex-test tables are
fingerprinted separately so those exclusions cannot hide copied structure.

All ten repaired chapters retain their manifest source assignments, claim
markers, equations, proof tags, protocol/schema references, evidence level, and
claim label. The semantic queue retires 298 inherited prose-candidate IDs,
adjudicates 770 domain-specific replacements against existing owned atoms,
preserves all 4,064 structured atoms, and leaves zero pending prose candidates.
The packet changes no support, release, or publication state.

## Prospective admission rule

A new or substantially revised chapter may reuse the shared vocabulary only by
linking the methodology owner and supplying its own claim, sources, ownership
boundary, evidence/falsification plan, diagram, test matrix, and handoff. The
tracked copied-scaffold fixture is rejected; the distinct fixture is accepted.
Eighteen negative mutations verify that deleting custody, weakening thresholds,
restoring copied structure, or inventing support cannot pass.

## Reproduction

```bash
python3 scripts/build_p7_1a_w3_inheritance_guard.py
python3 scripts/validate_p7_1a_w3_inheritance_guard.py
python3 scripts/validate_repeated_prose.py
```
