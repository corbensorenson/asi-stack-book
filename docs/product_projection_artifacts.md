# Executable Product Projections

Last updated: 2026-07-10

The three product contracts now produce concrete, generated navigation
artifacts rather than only describing intended audiences. They still share the
canonical Quarto chapters, source inventory, claim records, proofs, tests, and
release state. No projection is allowed to become a second authority.

## Narrative technical book

`products/narrative_product_spine.json` defines a 15-chapter thesis-to-method
route. It is deliberately within the review recommendation's 12–15 chapter
range. Each selected chapter has one canonical core-claim reference, reader
question, running example, strongest objection, failure story, evidence that
would change the conclusion, and handoff. The reader generator can materialize
the bounded candidate with:

```bash
python3 scripts/build_reader_edition.py \
  --narrative-spine products/narrative_product_spine.json \
  --output build/narrative_product
```

The generated orientation is derivative editorial navigation. It adds no
evidence and changes no support state. The other 39 chapters remain visible in
the architecture reference and are not rejected or deleted. The candidate is
not a reviewed reader release; continuity, repetition, accessibility, figure,
format, and independent editorial review still apply.

## Architecture reference specification

The generated architecture route is a complete 54-chapter lookup index in
canonical manifest order. Every row carries the canonical chapter and
core-claim identity plus its assignment to one of the three defended
contributions. Protocol schemas, implementation horizons, and the glossary
remain supporting routes. Completeness of the index does not establish a
deployed implementation or architecture quality.

## Evidence, proof, and release registry

The evidence route begins from the canonical status and groups claim, source,
proof, test, replay, release, review, and residual surfaces. Repository-backed
JSON and Markdown records are copied into the projection as content-addressed
snapshots with SHA-256 digests; rendered Quarto pages remain links to their
owning public surfaces. A snapshot proves byte identity only, not claim truth,
reviewer competence, or open-world record faithfulness.

## Build and release integration

After a clean Quarto render and canonical-status build, release CI runs:

```bash
python3 scripts/build_product_projections.py \
  --output _site/products \
  --status _site/status/canonical-public-status.json
```

The product pages are therefore created before the moving `/latest/` mirror
and tested-site bundle are hashed. The deployment workflow still consumes only
the exact tested bundle; it does not rebuild product pages.

## Validation boundary

`scripts/validate_product_projections.py` regenerates all projections and the
bounded reader source in temporary workspaces. It checks canonical order,
complete routing, generated orientation fields, source digests, canonical
counts, and unchanged `argument` support. Four mutation controls reject a
16-chapter narrative, a missing strongest objection, out-of-order selection,
and a changed evidence snapshot. With `--site _site`, it also checks the
rendered canonical-status binding, product manifests and pages, every chapter
target, every rendered evidence route, content-addressed snapshots, and the
presence of the product manifest inside the moving `/latest/` mirror.

These controls establish projection consistency. They are not independent
editorial review, artifact approval, empirical architecture evidence, or a
chapter-core support transition.
