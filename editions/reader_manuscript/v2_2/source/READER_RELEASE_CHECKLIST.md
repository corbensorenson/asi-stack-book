# Reader Release Checklist

Status: generated checklist for major-version reader review.

This workspace is derived from the living book. It is not the canonical source and it is not a published reader edition until review, renders, and release records say so.

## Generated Source

- Profile: `reader_release`
- Chapters: 55
- Files: 60
- Target formats: html, epub, pdf, docx
- Live-only sections removed: 279
- AI-only fenced blocks removed: 62
- Human-only fenced blocks unwrapped: 110
- Reader scaffold terms humanized: 47
- Reader overlay manifest: `editions/reader_overlays/v1_0/manifest.json`
- Reader overlay operations applied: 75
- Reader delta report: `reader_delta_report.md`
- Reader-spine validator: `scripts/validate_reader_spine.py`
- Handoff word floor: 45

## Required Gate

- [ ] python3 scripts/build_reader_edition.py --check
- [ ] python3 scripts/sync_reader_overlay_asset.py --check
- [ ] python3 scripts/validate_reader_overlays.py --check
- [ ] python3 scripts/validate_human_reading_paths.py
- [ ] python3 scripts/validate_reader_evidence_boundaries.py --check
- [ ] python3 scripts/validate_reader_spine.py --check
- [ ] python3 scripts/render_reader_formats.py --check
- [ ] reader manuscript is manually reviewed for narrative continuity
- [ ] EPUB render passes
- [ ] DOCX render passes
- [ ] PDF render passes only when PDF dependencies are available
- [ ] reader release record states which formats were actually rendered

## Reader Review

- [ ] Read the generated manuscript for chapter-to-chapter continuity.
- [ ] Confirm every generated chapter has exactly one `Handoff` section after `Summary`.
- [ ] Confirm non-final Handoffs name the next manifest chapter title and the final Handoff closes the book-level arc.
- [ ] Check that meaning-critical caveats and support-state limits remain in ordinary prose.
- [ ] Check that stripped source crosswalks, proof hooks, and guardrails did not leave broken transitions.
- [ ] Review the generated reader delta report and confirm any overlay operations are intentional for this major version.
- [ ] Confirm generated reader source and `reader_delta_report.md` were not edited as canonical source for prose changes.
- [ ] Check that glossary, Corben corpus/local-project appendix, and separate external-literature appendix are sufficient for interested human readers.
- [ ] Review `companion_notes.md` for omitted dense material and e-reader/audio companion needs.
- [ ] Record residuals and non-claims in an edition release record.

## E-Reader And Document Checks

- [ ] EPUB opens in at least one e-reader application or device with readable tables, figures, and diagrams.
- [ ] PDF render is attempted only when local PDF dependencies are available and is checked for page breaks, figure sizing, and table overflow.
- [ ] DOCX opens with headings, figures, tables, and bibliography in usable form.
- [ ] Reader HTML is spot-checked for stripped live-only scaffolding, navigation, and image paths.
- [ ] Images and diagrams remain readable in the reader artifact or have a clear companion-note route for audio.
- [ ] Any optional AZW3, MOBI, Markdown, or plain-text derivative is generated from the reviewed reader source or reviewed EPUB and listed separately in the release record.

## Human Reader Quality Floor

- [ ] The generated reader manuscript should feel like a continuous book, not an exported research notebook.
- [ ] Chapter openings and summaries should carry transitions after live-only scaffolding is stripped.
- [ ] Tables, schemas, and proof-adjacent material should remain only when they help a human reader; otherwise move detail to live or companion material.
- [ ] Images and diagrams should be readable on an e-reader-sized viewport or have a companion route for audio.
- [ ] The reader release should preserve uncertainty and evidence limits without repeating source-management machinery in every chapter.

## Major-Version Human Bundle

- Canonical reader profile: `reader_release`
- [ ] Confirm this reader workspace was generated from the tagged live-book state.
- [ ] Confirm any optional e-reader conversion starts from the reviewed reader source or reviewed EPUB.
- [ ] Keep audio packaging in a separate audio-release record unless that package has its own reviewed script and artifacts.

### Human Quality Gates

- [ ] The manuscript reads as one continuous book after live-only scaffolding is stripped.
- [ ] Meaning-critical caveats and uncertainty remain in the reader spine.
- [ ] Images and diagrams are readable on an e-reader-sized surface or have companion-note treatment.
- [ ] Dense tables, schemas, proof hooks, source IDs, and release machinery are omitted, summarized, or moved to companion material unless they are essential to the human argument.
- [ ] The release record names exactly which artifacts exist and which targets remain unattempted, failed, or not applicable.

## Optional Downstream Formats

- [ ] markdown
- [ ] plain text
- [ ] mobi or azw3 converted from a reviewed EPUB with an external tool

## Artifact Status Discipline

- [ ] Treat every listed format as `target_not_rendered` until its specific render command succeeds.
- [ ] Record EPUB, PDF, DOCX, HTML, AZW3, MOBI, Markdown, or plain-text artifacts only in an edition release record that names the actual path or URI.
- [ ] Keep audio and audio-embedded EPUB work out of the reader release unless a separate audio release record covers it.

## Non-Claims

- This checklist does not claim EPUB, PDF, DOCX, AZW3, MOBI, or audio artifacts exist.
- This checklist does not promote any live-book claim support state.
- The live book remains the source of truth after any reader derivative is produced.
