# v1.0 Release Preparation Review

Last updated: 2026-06-28

This review records a Phase 8 preparation pass for major-version reader, ebook,
document, PDF, and audio packaging. It does not create a release and does not
claim that any human-edition artifact is ready for publication. It was updated
after the opening-chapter, Personal Compute Hives, Policy Optimization,
Artifact Steward Agents, Semantic Representation, and Command Contracts reader
overlays, plus the Efficient ASI, Generate-Verify-Repair, Fast Generation, RankFold/NeuralFold, Mathematical and Search Substrates, Executable Specifications, Human Intent, System Boundaries, Evidence States, Verification Bandwidth, Planning, Runtime Adapters, Labor OS, and Circle Contracts reader
overlays, so the current overlay state is not mistaken for a released reader
manuscript.

## Commands Run

```bash
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/build_reader_edition.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
python3 scripts/render_reader_formats.py --output build/reader_edition_pdf_probe --formats pdf
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --output build/reader_edition_pdf_probe_utf8 --formats pdf
python3 scripts/build_audio_script.py --check
```

Results:

- Release profile validation passed.
- Reader spine validation passed for 54 chapters, with minimum reader-spine
  chapter length 1,963 words.
- Reader evidence-boundary validation passed for 54 chapters.
- Reader overlay validation now passes with 33 active operations and 33 applied
  operations. The reader overlay log is recorded separately in
  `docs/reader_overlay_pilot.md`.
- Reader edition check passed for 54 chapters and 59 files; 275 live-only
  sections would be removed, 60 reader scaffold terms would be humanized, and 33
  reader overlay operations would apply.
- Reader format render check passed for target formats `html`, `epub`, and
  `docx` as a readiness check.
- Reader format dry run passed locally for `html`, `epub`, and `docx`; the
  generated report is
  `build/reader_edition/reader_render_report.json`, and
  `docs/reader_format_dry_run.md` records the public-safe summary. The report
  recorded 59 rendered reader-site HTML artifacts, 1 EPUB artifact, and 1 DOCX
  artifact; the fixed HTML snapshot preserves 81 rendered site files and
  dependencies under `build/reader_edition/format_artifacts/`. These snapshots
  are ignored review outputs, not release artifacts.
- Reader format artifact inspection passed for the local snapshots: 59 rendered
  reader-site HTML files, 54 chapter HTML files, no live-only heading or raw
  core-claim marker leaks detected in reader-site HTML, 62 EPUB XHTML entries,
  60 EPUB image entries, and 59 DOCX media entries. The ignored local report is
  `build/reader_edition/reader_artifact_inspection_report.json`.
- The isolated PDF probe without explicit locale settings failed inside the
  LuaLaTeX path with a locale-data error and automatic package-install failure.
  The UTF-8 locale retry rendered one ignored local PDF snapshot at
  `build/reader_edition_pdf_probe_utf8/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf`.
  Local `pdfinfo` reported 574 letter-size pages, 8.0 MB, unencrypted, produced
  by LuaTeX-1.24.0; local text extraction found the title and compact
  evidence-boundary text.
- `docs/reader_artifact_layout_review.md` records representative PDF layout
  sampling and a broader local HTML layout/navigation probe. Sampled PDF pages
  1, 21, 25, and 527 showed no obvious clipping. After fixing HTML preservation
  to copy the complete `_reader_site` tree, the broader HTML probe exercised 28
  page-view pairs across 14 reader surfaces at desktop and mobile widths, with
  styles loaded and no page-level horizontal overflow at the inspected
  viewports.
- Audio script check passed for 59 script files generated for review.
- `docs/reader_continuity_review.md` records first manual decisions for the
  three medium-priority reader-continuity audit rows. This is a triage review,
  not a reader-release approval.
- `docs/reader_chapter_review_matrix.md` records the manifest-synced
  54-chapter reader-review queue: 54 `reviewed`, 0 `spot_checked`, 0
  `not_started`, 20 active-overlay chapters, 54 no-immediate-action decisions,
  3 companion-note candidates, 1 curated-manuscript candidate, and release
  blockers on every row until release records and artifact review exist.

## Current Release State

- The live book remains the canonical source.
- Existing tracked release records do not include a reviewed reader-edition
  release, ebook release, document release, PDF release, or audiobook release.
- Generated reader and audio workspaces under `build/` are ignored review
  workspaces, not durable release artifacts.
- The local reader-format dry run demonstrates that HTML, EPUB, and DOCX can
  render from the current generated reader source on this machine and pass basic
  structural inspection. The isolated PDF probe demonstrates that PDF can render
  locally when `LANG` and `LC_ALL` are set to `en_US.UTF-8`. None of those
  artifacts is approved for publication, and no audio artifact was attempted in
  that dry run.
- The v1.0 reader overlay set now has opening-chapter, Personal Compute Hives,
  Human Intent, System Boundaries, Evidence States, Verification Bandwidth, Command Contracts, Planning, Runtime Adapters, Labor OS, Circle Contracts, Efficient ASI, Generate-Verify-Repair, Fast Generation, RankFold/NeuralFold, Mathematical and Search Substrates, Executable Specifications, Policy
  Optimization, Artifact Steward Agents, and Semantic Representation operations.
  They are reader-only semantic deltas, not a reviewed reader release.
- The reader chapter review matrix is a release-control queue only. It preserves
  manifest chapter identity, current overlay counts, and review blockers; the
  full 54-chapter generated-reader chapter-text review queue is complete, but
  the matrix is not a reader release record and does not make any artifact
  release-ready.

## Blockers Before Major-Version Packaging

1. A validated live-book candidate needs to be selected and tagged.
2. The generated reader manuscript has release-grade chapter-text review records
   for all 54 chapters, but every row still carries release-record or
   artifact-review blockers.
3. Reader-only prose needs curated overlays or a future curated parallel
   derivative manuscript where generated stripping is not enough.
4. The local HTML, EPUB, DOCX, and PDF snapshots still need broader manual
   layout/navigation inspection and full reader-manuscript review before any
   release record can name them as reviewed artifacts; PDF also needs the
   explicit UTF-8 locale environment in this local setup.
5. An edition release record must list exact produced artifacts, commands,
   review state, failures, and residuals.
6. Audio scripts need human review of diagrams, tables, code, schemas, source
   IDs, proof-adjacent material, and pronunciation before any MP3, M4B, or
   audio-embedded EPUB work.

## Non-Claims

- No v1.0 tag was created in this pass.
- The dry run produced ignored local HTML, EPUB, DOCX, and PDF snapshots for
  review, but no EPUB, DOCX, PDF, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB
  artifact is claimed as published or release-ready.
- No reader release, audiobook release, or edition release record is complete.
- Passing readiness and structural artifact checks does not prove human
  editorial quality, layout quality, source interpretation, proof adequacy,
  benchmark behavior, or any chapter claim.
