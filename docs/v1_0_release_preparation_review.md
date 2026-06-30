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
python3 scripts/validate_reader_epub_probe_manifest.py
python3 scripts/validate_reader_docx_probe_manifest.py
python3 scripts/sync_reader_format_review_matrix.py --check
python3 scripts/render_reader_formats.py --output build/reader_edition_pdf_probe --formats pdf
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --output build/reader_edition_pdf_probe_utf8 --formats pdf
python3 scripts/build_audio_script.py --check
```

Results:

- Release profile validation passed.
- Reader spine validation passed for 46 chapters, with minimum reader-spine
  chapter length 2,042 words.
- Reader evidence-boundary validation passed for 46 chapters.
- Reader overlay validation now passes with 33 active operations and 33 applied
  operations. The reader overlay log is recorded separately in
  `docs/reader_overlay_pilot.md`.
- Reader edition check passed for 46 chapters and 51 files; 234 live-only
  sections would be removed, 58 reader scaffold terms would be humanized, and 33
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
  62 EPUB image entries, EPUB OPF metadata title `The ASI Stack`, creator
  `Corben Sorenson`, language `en-US`, and 61 DOCX media entries. The ignored
  local report is `build/reader_edition/reader_artifact_inspection_report.json`.
- The refreshed EPUB snapshot has a tracked metadata/source-spine probe:
  9,078,787 bytes, 130 zip entries, 62 XHTML entries, 62 image entries, 126 OPF
  items, 62 OPF itemrefs, 866 navigation hrefs, `en-US` language metadata, and
  sampled reader-note, evidence-boundary, and source-card XHTML entries. The
  tracked summary is `docs/reader_epub_probe_manifest.md`; no e-reader
  application review has been completed.
- The refreshed DOCX snapshot converted through the documents-skill
  `render_docx.py` path backed by headless LibreOffice into a 514-page,
  8,190,162-byte probe PDF with 514 page images. Representative pages 1, 25,
  447, 472, 474, and 514 were visually sampled, including source-card appendix
  pages and the final external citation policy. The tracked summary is
  `docs/reader_docx_probe_manifest.md`.
- The isolated PDF probe without explicit locale settings failed inside the
  LuaLaTeX path with a locale-data error and automatic package-install failure.
  The UTF-8 locale retry rendered one ignored local PDF snapshot at
  `build/reader_edition_pdf_probe_utf8/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf`.
  Local `pdfinfo` reported 535 letter-size pages, 8,613,924 bytes,
  unencrypted, produced by LuaTeX-1.24.0; local text extraction found the title
  and compact evidence-boundary text plus source-card appendix markers. The tracked summary is
  `docs/reader_pdf_probe_manifest.md`.
- `docs/reader_artifact_layout_review.md` records representative PDF layout
  sampling and a broader local HTML layout/navigation probe. Sampled PDF pages
  1, 21, 25, 474, 497, 499, and 535 showed readable title, reader-note,
  opening-chapter, generated source-card appendix, and final-policy pages.
  The generated reader source now converts Appendix G and Appendix H wide
  source tables into source cards before PDF rendering. After fixing HTML preservation to copy the
  complete `_reader_site` tree, the broader HTML probe exercised 28 page-view
  pairs across 14 reader surfaces at desktop and mobile widths, with styles
  loaded and no page-level horizontal overflow at the inspected viewports.
- `docs/reader_format_review_matrix.md` records the synced format-review
  ledger: 4 format rows, the HTML row release-approved against
  `release_records/2026-06-29-v1-reader-html-855dc277.json`, 3 remaining
  full-format-review blockers, 1 application/e-reader blocker, and 1
  full-PDF-layout blocker. EPUB has a metadata/source-spine probe but remains
  blocked until application/e-reader review happens; DOCX and PDF remain
  probe/spot-check artifacts only.
- Audio script check passed for 51 script files generated for review.
- `docs/reader_continuity_review.md` records first manual decisions for the
  three medium-priority reader-continuity audit rows. This is a triage review,
  not a reader-release approval.
- `docs/reader_chapter_review_matrix.md` records the manifest-synced
  46-chapter reader-review queue: 46 `reviewed`, 0 `spot_checked`, 0
  `not_started`, 20 active-overlay chapters, 46 no-immediate-action decisions,
  3 companion-note candidates, 43 curated-manuscript candidates, and release
  blockers on every row until release records and artifact review exist.

## Current Release State

- The live book remains the canonical source.
- Existing tracked release records do not include a reviewed reader-edition
  release, ebook release, document release, PDF release, or audiobook release.
- Generated reader and audio workspaces under `build/` are ignored review
  workspaces, not durable release artifacts.
- The local reader-format dry run demonstrates that HTML, EPUB, and DOCX can
  render from the current generated reader source on this machine and pass basic
  structural inspection. The EPUB probe demonstrates that the current generated
  EPUB carries explicit `en-US` metadata and sampled reader/source-card spine
  text. The DOCX conversion probe demonstrates that the current generated DOCX
  can convert through the local headless LibreOffice path for a representative
  visual spot check. The isolated PDF probe demonstrates that PDF can render
  locally when `LANG` and `LC_ALL` are set to `en_US.UTF-8`, and the refreshed
  PDF spot check samples the generated source-card replacement for Appendix G
  and Appendix H. None of those artifacts is approved for publication, and no
  audio artifact was attempted in that dry run.
- The v1.0 reader overlay set now has opening-chapter, Personal Compute Hives,
  Human Intent, System Boundaries, Evidence States, Verification Bandwidth, Command Contracts, Planning, Runtime Adapters, Labor OS, Circle Contracts, Efficient ASI, Generate-Verify-Repair, Fast Generation, RankFold/NeuralFold, Mathematical and Search Substrates, Executable Specifications, Policy
  Optimization, Artifact Steward Agents, and Semantic Representation operations.
  They are reader-only semantic deltas, not a reviewed reader release.
- The reader chapter review matrix is a release-control queue only. It preserves
  manifest chapter identity, current overlay counts, and review blockers; the
  full 46-chapter generated-reader chapter-text review queue is complete, but
  the matrix is not a reader release record and does not make any artifact
  release-ready.
- The reader format review matrix is also a release-control queue only. It
  records local render and inspection evidence for HTML, EPUB, DOCX, and PDF,
  including EPUB metadata/source-spine sampling and representative EPUB/DOCX/PDF spot checks, and it keeps every format
  unapproved until format-specific blockers and the edition release record are
  reconciled.
- `docs/reader_companion_note_routing_review.md` and
  `editions/reader_manuscript/v1_0/companion_note_routing.json` now record
  reader/e-reader/audio companion-note routing for the three dense
  proof/governance chapters flagged by the review matrix. Generated reader and
  audio companion notes consume that routing, but it does not clear release
  records, format-artifact review, audio-script review, or curated
  reconciliation blockers.

## Blockers Before Major-Version Packaging

1. A validated live-book candidate needs to be selected and tagged.
2. The generated reader manuscript has release-grade chapter-text review records
   for all 46 chapters, but every row still carries release-record or
   artifact-review blockers.
3. Reader-only prose needs curated overlays or a future curated parallel
   derivative manuscript where generated stripping is not enough.
4. Companion-note routing has been recorded for the current three dense
   proof/governance candidates, but companion notes still need release review
   before e-reader, audio, or audio-embedded EPUB artifacts can rely on them.
5. The local HTML, EPUB, DOCX, and PDF snapshots still need broader manual
   layout/navigation inspection and full reader-manuscript review before any
   release record can name them as reviewed artifacts; EPUB still needs
   application/e-reader review, DOCX still needs full application review if it
   will be released as a document artifact, and PDF still needs full
   page-by-page layout review plus the explicit UTF-8 locale environment in
   this local setup.
6. The format-review matrix must be updated from actual review evidence rather
   than inferred from successful renders; no row is release-approved today.
7. An edition release record must list exact produced artifacts, commands,
   review state, failures, and residuals.
8. Audio scripts need human review of diagrams, tables, code, schemas, source
   IDs, proof-adjacent material, and pronunciation before any MP3, M4B, or
   audio-embedded EPUB work.

## Non-Claims

- No v1.0 tag was created in this pass.
- The dry run produced ignored local HTML, EPUB, DOCX, and PDF snapshots for
  review, but no EPUB, DOCX, PDF, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB
  artifact is claimed as published or release-ready.
- No reader release, audiobook release, or edition release record is complete.
- The reader format review matrix is not an edition release record and does not
  approve HTML, EPUB, DOCX, PDF, e-reader conversion, audio, or audio-embedded
  EPUB artifacts.
- Passing readiness and structural artifact checks does not prove human
  editorial quality, layout quality, source interpretation, proof adequacy,
  benchmark behavior, or any chapter claim.
