# Reader-prose quality closure — 2026-08-09

## Outcome

P7.1c now covers all 85 canonical chapters. Every chapter has a current,
manifest-bound editorial packet under
`evidence_quality/reader_prose_quality_packets/`, and
`python3 scripts/validate_p7_1c_reader_prose_quality.py` accepts 85/85 packets
while rejecting five adversarial controls.

This is an editorial closure, not an evidence promotion. Chapter support,
release, deployment, SOTA, AGI, and ASI states do not move.

## What changed in the manuscript

Each chapter now exposes all of the following in reader-visible prose:

1. a short reader claim;
2. an operational rule;
3. a chapter-specific worked decision, failure, trace, or justified existing
   scene;
4. a counterexample or simpler baseline;
5. a formal binding to the unchanged chapter-core claim and support state;
6. an explicit maximum-inference boundary and residual owner.

The pass uses actual repository observations where they exist. Examples include
the KERC `714.0`-versus-`73.25`-byte failure and later N1 competence narrowing,
the Project Theseus artifact-retention run, the exact route-cost ledger, the
one-public-copy recall boundary, the stale-cache winding collision, the
positive/null/inconclusive scientific attempt ledger, and the no-rebuild public
deployment observation. Where no empirical event exists, the chapter uses a
clearly bounded vignette and says so rather than inventing a result.

## Human Reading Path audit

Claude's review correctly identified a template smell: before this closure, all
85 Human Reading Path blocks were between 170 and 180 whitespace-delimited
words. Length alone did not prove semantic duplication, but the near-constant
budget made the blocks feel interchangeable.

The closure keeps the useful reading-path prose and adds one unique **Concrete
lens** to every block, derived from that chapter's counterexample or strongest
simpler baseline. The current audit reports:

- 85 Human Reading Path blocks;
- 85 chapter-specific Concrete lenses;
- 85 unique lens texts;
- zero exact duplicate Human Reading Path blocks;
- 190–216 words per block, mean 204.0, with variation driven by the chapter's
  actual decision rather than a target quota.

The lens is not a new claim. It is a reader orientation that points into the
chapter's digest-bound worked scene and evidence ceiling.

## Caveat and bookkeeping disposition

The remediation does not optimize for fewer caveat phrases. Every packet states
which caveat was consolidated, which distinct limitations remain, and which
tables or inventories stay reader-facing because they carry argument rather
than status bookkeeping. Source roles, proof boundaries, non-claims, equations,
protocol identities, and support ceilings remain preserved.

The claimed improvement is therefore narrower and auditable: the manuscript no
longer asks schemas and disclaimers to carry the whole explanation. It now gives
the reader a concrete system, attempted action, outcome, failed boundary,
fallback or residual, and maximum inference before returning to formal detail.

## Machine checks

- `python3 scripts/validate_p7_1c_reader_prose_quality.py`
- `python3 scripts/build_chapter_substance_contract.py`
- `python3 scripts/validate_chapter_substance_contract.py`
- `python3 scripts/validate_human_reading_paths.py`
- `python3 scripts/validate_reader_spine.py --check`
- `python3 scripts/validate_reader_evidence_boundaries.py --check`
- `python3 scripts/validate_book.py`
- `python3 scripts/validate_publication.py`

The final local publication audit rendered all 98 Quarto pages, including all
85 canonical chapters. A desktop and 390-by-844 mobile browser check confirmed
the landing page, Project Theseus chapter, AI/Human reading-mode switch, unique
Concrete lens, responsive layout, single-H1 structure, and zero broken images
on the inspected surfaces. The rendered tree contained 98 HTML pages and 85
chapter pages. Its internal-link audit checked 11,274 local links; the only
locally absent target was `versions/index.json`, which is deliberately created
by the clean-commit Pages workflow after canonical status and product
projections are built.

The final render, link, Human-view, accessibility, and public-surface checks are
recorded in the publication handoff rather than treated as prose evidence.
