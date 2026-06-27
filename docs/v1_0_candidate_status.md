# v1.0 Candidate Status

Last updated: 2026-06-27

This document is the current public-safe status surface for the extended v1.0 improvement goal. It supersedes the older prewriting and v0.2 launch-status documents for current readiness decisions, while those older documents remain useful historical records.

The book is a stronger v1.0 candidate than the original v0.2 manuscript baseline, but it is not a v1.0 evidence release yet. The repository now has a complete manifest-driven manuscript, source-note and claim-source traceability, finite-record Lean coverage, schema fixtures, release-profile scaffolding, and a deployed Quarto site. All core chapter support states remain `argument`.

## Current Snapshot

| Surface | Current state | Evidence |
|---|---|---|
| Book structure | 4 parts, 54 manifest-driven chapters, 11 appendices | `book_structure.json`; `python3 scripts/sync_scaffold.py` |
| Manuscript scale | 54 chapter files; 184,034 chapter words excluding YAML front matter; 191,533 raw chapter-file words including metadata and live scaffolding | Local word-count check on `chapters/*.qmd` |
| Source inventory | 101 public-safe source records, each with a matching public source note; `sources/source_notes/` also contains a README and template | `sources/source_inventory.json`; `sources/source_notes/` |
| Source appendix ownership | Appendix G (`Corben's Own Sources, Papers, and Local Projects`) and Appendix H (`External Sources by Other Authors`) are independent top-level appendices with explicit source-ownership boundary blocks, ownership-rule rows, and appendix-local identity rows: G contains Corben's own papers, Corben-supplied materials, recovered project records, and local project records; H contains external records and third-party literature marked `external_literature`; neither appendix renders the other source class as a second ownership row | `python3 scripts/validate_source_appendices.py` |
| Claim/source traceability | 461 assigned source/chapter pairs, 461 exact claim-source mappings, 461 passage-reviewed mappings | `docs/source_evidence_audit.md`; `python3 scripts/validate_source_evidence_audit.py` |
| Support states | 54 chapter core claims at `argument`; no support-state promotion in the v1.0 improvement pass | `book_structure.json`; Appendix C |
| Proof envelope | 112 proof targets, all implemented as narrow finite-record Lean predicates | `proofs/proof_manifest.json`; `docs/proof_artifact_audit.md`; `lake build` |
| Schemas and fixtures | 71 JSON Schemas, 70 valid protocol fixtures, 1 public release record | `schemas/`; `tests/fixtures/protocol_records/`; `release_records/`; `python3 scripts/validate_schemas.py`; `python3 scripts/validate_protocol_examples.py` |
| Implementation horizons | 54 generated chapter build horizons with manifest-sourced minimum viable implementation and beyond-state-of-the-art endpoint fields | `book_structure.json`; Appendix K; `python3 scripts/validate_implementation_horizons.py` |
| Visual coverage | Every chapter has at least one substantive Mermaid diagram with at least 12 non-comment lines plus enough named states, edges, and labeled transitions to explain a mechanism; every chapter has a required diagram walkthrough note for its primary diagram with a chapter-specific label; landing page has a generated visual asset; browser Human-view gate checks rendered Mermaid SVG visibility | `python3 scripts/validate_visual_coverage.py`; `node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports` |
| Chapter handoffs | All 54 manifest chapters now end with reader-facing `Handoff` sections: non-final chapters name the next manifest chapter title and avoid numbered chapter references, while the final chapter closes the book-level arc; generated reader chapters must preserve the same single Handoff continuity after live-only stripping | `python3 scripts/validate_chapter_handoffs.py`; `python3 scripts/validate_reader_spine.py --check` |
| Release surfaces | Live, research, reader, and audio profiles exist; reader/audio derivation scripts exist | `editions/release_profiles.json`; `docs/major_version_release_runbook.md` |
| Live Human view | All 67 rendered book pages carry the persistent and shareable `AI view` / `Human view` switch with `?view=ai` and `?view=human`; all 54 chapters have exactly one Human Reading Path bridge; bridge prose is guarded against meta-reader and meta-book scaffolding and must be at least 170 words excluding the source-only heading, must open with at least 11 words, must close with at least 11 words, must avoid known repeated bridge formulas, with the current bridge minimum at 170 words, opening-sentence minimum at 11 words, closing-sentence minimum at 11 words, and targeted template-phrase count at 0; generated reader chapters strip raw live core-claim markers and repeated support boilerplate while preserving claim text and compact inline plain-language support-state boundaries; generated reader chapter prose rejects `this chapter`, `the chapter`, and repeated evidence-boundary paragraph openers after live-only stripping; generated reader chapters preserve one chapter-specific Handoff after `Summary` and now must clear section-level word-count and substantial prose-paragraph floors after stripping; chapter Human view hides live-only headings, matching page-TOC entries, internal Human Reading Path TOC entries, raw bracketed core-claim markers, repeated support boilerplate, and rendered section numbers while attaching the compact evidence boundary to the visible claim text; browser smoke validation can exercise every manifest chapter across desktop and mobile viewports with `--all-chapters --all-viewports`, including reading-mode control visibility, raw marker and support-boilerplate hiding/restoration, and horizontal-overflow checks, when Playwright/Chrome is available | `assets/reading-mode.html`; `assets/styles.scss`; `python3 scripts/validate_reading_mode_toggle.py`; `python3 scripts/validate_human_reading_paths.py`; `python3 scripts/validate_reader_spine.py --check`; `python3 scripts/validate_reader_evidence_boundaries.py --check`; `python3 scripts/validate_live_human_view.py`; `node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports` |
| Public site | GitHub Pages renders the live Quarto book | <https://corbensorenson.github.io/asi-stack-book/> |
| Status snapshot freshness | The headline counts in this status document are checked against current repository artifacts | `python3 scripts/validate_v1_status_snapshot.py` |
| Outline/manifest consistency | The drafting outline matches manifest chapter order, titles, core claims, assigned sources, and Lean proof targets | `python3 scripts/validate_outline_consistency.py` |

## What The Current Candidate Proves

- The book order is dynamic and manifest-driven.
- The outline is a usable source of truth for drafting, source queues, and Lean proof targets.
- Every manifest chapter exists and has the required chapter contract in order: problem, insufficiency, core claim, mechanism, interfaces, invariants, failure modes, minimum viable implementation, beyond-state-of-the-art end state, test plan, source crosswalk, and summary. The chapter DoD guard also requires `Problem`, insufficiency, and summary sections to clear a 130-word substance floor, `Mechanism` sections to clear a 300-word architecture floor, `Interfaces` sections to clear a 130-word systems-handoff floor, invariants to clear a 110-word preserved-boundary floor, failure modes to clear a 110-word concrete-risk floor, minimum viable implementation sections to clear a 125-word smallest-honest-build floor, and mature endpoints to clear a 200-word product-end-state floor while rejecting self-referential chapter phrasing, mechanical section handoffs, and live crosswalk references. The repeated-prose guard also rejects generic problem formulas such as `The book needs a place`, formulaic mature-endpoint openers and lead-ins such as `At maturity,`, `The mature version is`, `The mature version of`, `The logical end state is`, `At full build-out`, `The mature product surface would include:`, `The final product surface would include:`, `would expose:`, `The operational contract is`, `Support should stay at`, `At that mature boundary`, `In that final product`, `Failure closure:`, `detect and route failure modes such as`, `This is a target architecture, not a current-result claim`, `It remains beyond the chapter's present support state`, `Another invariant is`, `A second invariant is`, `The strongest invariant is`, `The key invariant is`, `The subtle failure is`, `The subtle failure mode is`, and `Another failure is`, support-state formulas such as `The support state remains argument`, MVI formulas such as `The next useful implementation step is`, `The next useful fixture set is`, `The next useful fixture is`, `Passing the fixture`, `Passing schema validation only`, `That would`, `without claiming`, `does not prove`, `do not prove`, `proves only`, `prove only`, `cannot prove`, `The accompanying Lean module is`, `The Lean predicates do not`, `These proofs do not implement`, and `The Lean coverage stays at`, generic interface formulas such as `The interface is the`, `The interface is a`, `The interface is an`, `The public schema now records`, `The interface should also record`, `The interface should distinguish`, `The interface should expose`, `The interface should carry`, `The interface should also`, and `The contract should also`, generic mechanism evidence-boundary formulas such as `None of those passages show` and `The reviewed passages sharpen the`, and generic summary formulas such as `The evidence map is narrower now`.
- The repeated-prose guard now also rejects `The passage-reviewed mappings support discussion` so Core Claim support paragraphs must name the actual source family or evidence boundary.
- Appendix K is generated from the manifest and machine-checked as a book-wide implementation horizon map: one concrete first-build slice and one mature target endpoint per chapter, in manifest order.
- Current source-note coverage, source-to-chapter assignment, core claim mapping, and passage-review mapping are internally traceable.
- Current proof targets are wired through outline tags, generated manifest records, triage records, Lean modules, root imports, chapter hooks, limitation prose, and Appendix E.
- Current schemas and example fixtures validate record shape for the protocol surfaces created so far.
- The live site can project the same source into the default AI/research surface and a cleaner Human view without creating a parallel manuscript; the bridge guard now rejects the recurring formulas found during the editorial pass.
- The live book renders locally and through GitHub Pages when the publication workflow passes.

## What It Does Not Prove

- It does not prove any ASI capability, model quality, deployment readiness, safety property, benchmark result, simulation result, or runtime behavior.
- It does not prove that source interpretation is semantically adequate for support-state promotion.
- It does not prove that the finite-record Lean predicates are the best formalization of each intended chapter boundary.
- It does not reproduce MoECOT, Theseus, Circle, Talos, VCM, PlanForge, policy-optimization, compression, routing, benchmark, or simulation results.
- It does not generate, review, or publish EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts.
- The live Human view is a convenience projection, not a reviewed reader-release manuscript and not a substitute for final human editorial review.

## Remaining Work Before v1.0 Evidence Release

- Perform claim-to-mechanism support review after the passage-reviewed mappings and record accepted evidence transitions before any claim moves above `argument`.
- Run semantic proof adequacy review for all 112 finite-record Lean targets.
- Implement or defer chapter-level Codex tests beyond protocol fixture validation, with explicit command, environment, and result records.
- Normalize additional external literature where the book currently has queues rather than direct source records and source notes.
- Import or reproduce any prototype, benchmark, Circle, Theseus, MoECOT, VCM, Talos, PlanForge, compression, routing, or policy-training artifact before using it as stronger evidence.
- Generate and review reader-edition artifacts only after a tagged live-book candidate passes the live/research gate.
- Generate audio scripts and audio artifacts only from a reviewed reader edition, preserve the implementation-horizon sections in the script, and record exact produced artifacts.
- Continue the final reader-facing editorial pass over both the generated reader manuscript and representative live Human view chapters. Human Reading Path meta-language, known repeated bridge formulas, raw core-claim marker leakage, repeated support-boilerplate leakage, repeated evidence-boundary paragraph openers, generated reader `this chapter` / `the chapter` scaffolding, and stripped-reader Handoff continuity are now guarded, but full human continuity still requires editorial review without weakening evidence boundaries.

## Candidate Gate

Before tagging or continuing to describe a state as a v1.0 candidate, run:

```bash
python3 scripts/sync_scaffold.py
git diff --exit-code
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_chapter_dod.py
python3 scripts/validate_proof_artifact_audit.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/build_audio_script.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_repeated_prose.py
(cd lean && lake build)
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

Before describing a state as a v1.0 evidence release, also record the accepted evidence transitions, rendered reader artifacts if any, audio artifacts if any, and release records that actually exist.
