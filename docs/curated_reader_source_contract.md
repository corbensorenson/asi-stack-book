# Curated Reader Source Contract

Last updated: 2026-07-05

This document explains the machine-readable contract in
`editions/reader_manuscript/v1_0/curation_contract.json`. It is the rule for
the future point where the normal human-reader book stops being only generated
reader source plus semantic overlays and starts carrying manually edited chapter
files.

The same validator also checks the reader handoff contract embedded in
`editions/reader_manuscript/v1_0/manifest.json`. That handoff contract records
the book-level human-reader thesis, part arcs, recurring signature ideas,
key-figure targets, converted optional author-enrichment prompts, and
per-chapter stakes/payoffs. It is editorial scaffolding for review, not a reader
release record.

## Relationship To The Live Book

Curated reader chapters may become a parallel derivative prose source. They are
not equal authority beside the live AI/research book.

The live book remains canonical for:

- manifest chapter identity and ordering;
- claim text meaning and support-state meaning;
- source boundaries and source assignments;
- proof/test status and unrun-result boundaries;
- minimum viable implementation and beyond-state-of-the-art implementation horizons;
- release records and artifact approval.

If reader editing discovers a problem in the live chapter, the live chapter must
be fixed and validated. The reader manuscript should not hide a canonical
correction inside a human-only derivative.

## Allowed Divergence

Curated reader prose may improve pacing, openings, closings, examples,
transitions, paragraph ordering, section flow, companion-note integration,
sentence-level voice, and chapter compression.

Those changes are allowed because they improve how a person reads the book.
They do not create new evidence and do not change the architecture's recorded
claim state.

## Blocked Divergence

Curated reader prose must not change claim meaning, support-state meaning,
source-boundary meaning, proof/test status, implementation status, non-claim
boundaries, release-artifact existence, or manifest chapter identity.

When a human-reader edit would change meaning, it needs one of two outcomes:
fix the live AI/research chapter too, or reject the change as a reader-only
presentation edit.

## Required Chapter Record

Every future curated chapter record must name:

- the manifest `chapter_id` and current title;
- the curated chapter file under `editions/reader_manuscript/v1_0/chapters/`;
- the generated reader baseline reference;
- the live source commit or tag reference;
- the claim-boundary and implementation-horizon references;
- the allowed curation scope used by the edit;
- chapter-specific reader stakes and reader payoff;
- the optional author-enrichment slot IDs that may later guide Corben-supplied first-person additions;
- a divergence summary;
- meaning-preservation checks;
- active release blockers;
- whether a canonical live-source change is required.

`python3 scripts/validate_reader_manuscript_manifest.py` enforces this contract.
It also requires the top-level handoff contract to preserve its single thesis,
part arcs, 8-12 signature ideas, 8-12 key-figure targets, and 8-12 optional
author-enrichment records with sidecar refs, non-blocking release status, and
no permission to fabricate first-person experience.

To initialize a future curated chapter without hand-building the record, first
generate the reader baseline, then run the initializer in dry-run mode:

```bash
python3 scripts/build_reader_edition.py
python3 scripts/init_curated_reader_chapter.py --chapter-id artifact-steward-agents-and-living-project-governance
```

Add `--write` only after review decides that overlays are too small for the
intended human-reader edit. The initializer copies the generated reader chapter
as a drafting baseline, records the live-source commit, adds the required
release blockers, and leaves reconciliation incomplete until a later review
approves it.

## Release Boundary

The curation contract is not a reader release record. A curated manuscript can
become release input only after reconciliation approval, format artifact
review, and a specific edition release record exist.

The current v1.0 curated reader source records reconciliation approval in
`docs/reader_chapter_reconciliation_approval.md` and
`editions/reader_manuscript/v1_0/chapter_reconciliation_approval_manifest.json`.
That approval clears only `curated_reconciliation_not_approved`; it does not
approve HTML, EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts.
