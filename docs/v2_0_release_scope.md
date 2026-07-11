# v2.0.0 Release Scope

Last updated: 2026-07-10

The completed major release is the canonical live/research HTML book only.
This is a deliberate product decision, not a failed-format euphemism.

## Included

- the exact 67-page Quarto HTML site built from the tagged source commit;
- AI and Human reading modes over the same 54 active chapters;
- narrative, architecture-reference, evidence-registry, source, proof, test,
  status, license, and release surfaces linked from that site;
- one content-addressed GitHub Release archive for `v2.0.0`, redownloaded and
  SHA-256 verified; and
- mutable `/latest/` deployment that identifies the same tagged release at the
  moment of publication without being represented as immutable storage.

## Excluded formats

EPUB, DOCX, PDF, AZW3, MOBI, MP3, M4B, audio-embedded EPUB, and a separate
reader-manuscript HTML release are not v2.0.0 artifacts. The tracked 44-chapter
curated reader workspace is historically useful but does not match the active
54-chapter spine, and the existing e-reader/document/audio probes do not amount
to full final-format inspection. Creating those files merely to enlarge the
release would violate the rule that only rendered and inspected formats exist.

They may become later versioned products only after their active-spine source,
application-specific inspection, accessibility, layout, narration, rights, and
release-record gates pass.

## Identity

- Title: *The ASI Stack: A Governed Systems Architecture for Advanced AI, with
  ASI as the Stress Case*
- Version/tag: `v2.0.0`
- Historical title lineage: v1.0.0 used *The ASI Stack: A Systems Architecture
  for Governed, Efficient, Self-Improving AI*.
- License routing: `licensing/final_release_rights_routing.json`.
- Immutable archive: published from the exact tested tag-bound bundle at
  SHA-256 `5772aa8e47df279bbb38e38b2a3564489f6b3f3f65f8ff2df373f318e2c9eaf9`;
  no v1.0.0 site archive is backfilled.
