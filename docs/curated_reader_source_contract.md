# Curated Reader Source Contract

Last updated: 2026-06-28

This document explains the machine-readable contract in
`editions/reader_manuscript/v1_0/curation_contract.json`. It is the rule for
the future point where the normal human-reader book stops being only generated
reader source plus semantic overlays and starts carrying manually edited chapter
files.

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
- a divergence summary;
- meaning-preservation checks;
- active release blockers;
- whether a canonical live-source change is required.

`python3 scripts/validate_reader_manuscript_manifest.py` enforces this contract.

## Release Boundary

The curation contract is not a reader release record. A curated manuscript can
become release input only after reconciliation, format artifact review, and a
specific edition release record exist.
