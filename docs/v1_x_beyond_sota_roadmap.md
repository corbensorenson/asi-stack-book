# v1.x Beyond-SOTA Roadmap

Last updated: 2026-07-04

This roadmap is the post-`v1.0.0` long-term plan for turning **The ASI
Stack** from a tagged living-book release into a stronger evidence-and-reader
program. It should be read with `docs/v1_0_candidate_status.md`,
`docs/v1_progress_ledger.md`, `docs/v1_0_release_gate_audit.md`,
`docs/proof_depth_classification.md`, `docs/proof_adequacy_review.md`,
`docs/external_sota_positioning_audit.md`,
`docs/a_plus_quality_scorecard.md`, and
`docs/local_project_mining_theseus_circle.md`. The full per-chapter evidence
backlog lives in `docs/per_chapter_evidence_plan.md`, and the v1.0
Beyond-SOTA reference map in `docs/v1_0_roadmap.md` remains the baseline for
measuring movement relative to external state of the art.

The live AI/research book remains canonical for chapter identity, claim text,
support states, source boundaries, proof and test status, implementation
horizons, and release records. The normal reader manuscript may become a
curated parallel derivative prose source, but it is not equal authority for
evidence or claims.

## Purpose

The v1.0.0 release proved that the repository can function as a public living
book: manifest-driven structure, the original 54 drafted chapters, source
notes, claim/source traceability, finite-record Lean hooks, schema fixtures,
reader profiles, Human view, a reviewed reader HTML artifact, a deployed
Quarto site, and six narrow non-core evidence transitions. The current v1.x
working table of contents has since consolidated to 44 active manifest
chapters through governed execution packages.

The next phase should not spend another cycle proving that the scaffold exists.
It should retire the important IOUs:

- every chapter needs a named evidence lane, but only a small number of
  high-payoff lanes should execute in a given v1.x cycle;
- the five safety-critical Lean modules need real semantic depth beyond
  projection-only traceability;
- the bounded non-core evidence transitions need to be easy to discover without
  implying chapter-core promotion;
- every chapter needs a real external-grounding pass so Corben-originated
  nomenclature is related to known papers, standards, benchmarks, and adjacent
  systems before readers are asked to accept the stack vocabulary;
- the executed 44-chapter spine should remain stable unless new source,
  evidence, reviewer, or reader-edit findings expose a concrete duplicate
  artifact boundary;
- Project Theseus and Circle evidence need public-safe replay paths rather than
  local-only summaries;
- the human-reader edition needs to become a true edited book, not only a strip
  of the AI/research source;
- the human-reader edition also needs authored vision, voice, and selection:
  evidence discipline can make the book honest, but it does not by itself make
  the book memorable, beautiful, or unmistakably authored;
- EPUB, DOCX, PDF, and audio should be treated as reviewed edition artifacts
  only after exact artifact records exist.
- retired public chapter URLs from the consolidation must stay preserved by
  guarded historical stubs rather than policy-only promises.
- the project's discipline must become legible in the first minute of a cold
  read, because hidden rigor does not protect the work from a theory-of-everything
  silhouette.

After the 2026-06-30 execution review, the roadmap also has a sharper rule:
planning surfaces are no longer the bottleneck. The next work should change
the book, proof workspace, manifests, evidence fixtures, or reader artifacts
directly. New reports, scorecards, dry-runs, destination drafts, and review
packets are disallowed unless they are required by a validator, release gate,
external reviewer, or an executed merge/evidence/proof change. The default next
action is implementation.

## Inputs Reconciled

This roadmap reconciles:

- the current repository state after the tagged `v1.0.0` living-book release;
- the current Claude review supplied by Corben as planning input;
- the 2026-06-29 consolidation critique supplied by Corben, which argues for
  re-consolidating over-split chapter clusters while preserving every useful
  idea as a section, subclaim, proof hook, or source mapping, and the follow-up
  note that the repeated 13-section chapter skeleton is now the main reader
  burden in several clusters;
- the 2026-06-30 pasted consolidation follow-up, which confirms that the
  consolidation direction has teeth but should now move through decisions on
  already packaged merge and fold candidates rather than another broad
  planning pass or a direct 54-to-44 manifest edit;
- the 2026-06-30 execution review supplied by Corben, which credits the real
  proof-depth and Theseus/Circle evidence progress but flags that
  consolidation had produced many planning artifacts and no manifest merges at
  that checkpoint;
- the 2026-07-01 craft-and-voice review supplied by Corben, which separates
  scientific validation from literary/artifact quality and correctly flags that
  Codex can prepare structure, continuity, visual craft, and authorial handoff
  surfaces, but cannot fabricate Corben's lived voice, personal lessons, or
  conviction;
- the calibrated 2026-07-01 chapter-by-chapter external-review pass in
  `docs/CHAPTER_REVIEWS.md`, which covers all 44 chapters and both live and
  reader versions while explicitly correcting its own proxy errors: low
  `ext_` count means external-anchoring depth, not missing positioning; low
  theorem count means narrow coverage, not weak proof; and planned-test counts
  are qualitative signals until rechecked chapter by chapter;
- the 2026-07-02 direction update from Corben, which supersedes the earlier
  voice-gating framing: Codex must push all prose — live/research edition and
  human-reader edition — to what a demanding editor would call finished, with
  no work items left waiting on Corben; Corben performs one final editing pass
  at the end over a complete book, as polish rather than as a release
  dependency; the external-review lane is parked as user-owned; and the target
  is A+ on every graded dimension for both editions of every chapter;
- the 2026-07-03 idea-focused Claude review supplied by Corben, which correctly
  shifts the ideas/synthesis gap from "add more topics" to "make each signature
  idea analytically load-bearing": crisp statement, closest-prior-art delta,
  non-obvious consequence, strongest objection, and an artifact-backed answer
  path;
- Codex verification of Claude's claims against the local tree;
- `book_structure.json`, which currently defines four parts, 44 chapters, and
  11 appendices;
- `docs/book_outline.md`, which remains the drafting, source, and proof target
  source of truth;
- the current reader-manuscript, reader-overlay, format-review, proof-depth,
  source-readiness, external-SOTA, and release-gate ledgers.

Claude's review is useful planning input. It is not source evidence and should
not be quoted in the book as an external authority.

## Findings With Teeth

| Priority | Finding | Verified state | Roadmap consequence |
|---|---|---|---|
| P0 | The 44-lane evidence plan can reintroduce the breadth trap. | The first roadmap version named a lane and acceptance bar for every chapter, which is useful as backlog but dangerous as an execution checklist. | Keep the 44-row plan in `docs/per_chapter_evidence_plan.md`, execute one flagship measured lane first, allow at most two direct supporting lanes, and leave the rest explicitly planned. |
| P0 | The project's strongest quality is the least legible one. | The validation, support-state discipline, and non-claim machinery are real, but a cold reader first sees broad scope, self-coined terms, and many self-sourced ideas. | Add a 60-second trust surface and make the evidence discipline visible before readers infer overreach. |
| P0 | Formal proof count is no longer the bottleneck; executable-model depth is. | `docs/proof_depth_classification.md` now records 994 theorem declarations, 183 direct/projection-style, 807 derived/decomposed, 4 unknown/mixed, and 103 safety-critical theorem declarations after the Resource aggregate flagship invariant pass, Theseus/Fast support-lane aggregate bridge, Capability replacement identity-sequence bridge, Resource governance-tax trade-off bridge, receipt repository audit bridge, claim-state transition bridge, Circle public consumer-gate fixture bridge, residual-ledger storage/replay bridge, Artifact Graphs live attestation bridge, and Artifact Graphs randomized artifact attestation audit bridge. The first anti-projection sweep is real, but most theorems still verify finite records and decision routes rather than traces of a running system. | Stop optimizing for theorem-count growth. Pick one proof/evidence bridge and prove a property over transitions or fixture equivalence, then run the same cases through the executable harness where possible. |
| P0 | External review is too important to leave until preprints. | The evidence base is still mostly self-sourced: Corben's source papers, Project Theseus, Circle, local harnesses, and Codex/Claude planning reviews. | 2026-07-02 direction: this lane is parked as user-owned for Codex execution. The public request issue and dated outreach blocker remain the sequencing record; they prevent other milestones from waiting, but they are not accepted external-review evidence. Codex must not schedule outreach work, must not gate any other milestone on review, and spends cycles here only if Corben supplies a review to ingest. |
| P0 | The field-impact path requires defended contributions, not a complete encyclopedia. | The 44 active chapters are useful as architecture coverage, and several ideas now have bounded fixtures, source-noted positioning, or first local closures; none has yet reached full defended-contribution state with live/external replay, prior-art-reviewed novelty posture, and release-quality reader integration. | Keep three to five contribution tracks selected, keep at most three active deep-work tracks, and push the next artifact where a selected track and a signature idea can both move one execution state to the right. |
| P0 | The Ideas grade will not improve through more nomenclature. | The contribution novelty ledger exists, and verification bandwidth, residual honesty, receipt faithfulness, epistemic trusted computing base, human oversight degradation, governance economics, partitioned authority, and stable identity now have first bounded closures or explicit ownership routes; several still lack live/external evidence, source-reviewed novelty posture, or strongest-objection treatment in chapter and reader prose. | Treat "idea depth" as an artifact gate: one signature idea per cycle gets live prose, reader prose, ledger/source deltas, a proof/evidence artifact or dated blocker, and explicit non-claims. Do not close an idea with a roadmap note or standalone audit. |
| P0 | Human-reader excellence is a separate axis from evidence validation. | The project can be scientifically honest while still reading like a templated architecture reference; the curated reader chapters are reconciled for prose meaning, but the manuscript remains unreleased, not format-reviewed, and still needs book-level continuity, visual polish, e-reader/audio treatment, and release approval. | Add a craft-and-authorial-distillation milestone: keep the live research spine intact, but make the reader manuscript carry a single thesis, a narrative arc, signature ideas, crafted examples, and finished authored prose written by Codex to its own editorial ceiling; Corben's edit comes last as polish, not as a dependency (2026-07-02 direction). |
| P0 | Codex must not counterfeit the author's presence. | Agent-written first-person lessons, personal stakes, scars, or hard-won conviction would be fabricated unless Corben supplies them. | Codex must not fabricate first-person biography, invented anecdotes, or claimed personal history — that rule stands. But per the 2026-07-02 direction it must also not leave slots or placeholders: write finished third-person prose whose conviction, specificity, and stakes stand without personal anecdote, and keep any optional first-person enrichment points in a sidecar queue rather than as gaps in the manuscript. Nothing in the reader edition may remain unfinished on the grounds that the author will fill it in. |
| P0 | The consolidation problem is mostly executed; the remaining risk is linkrot and reopening churn. | The manifest is 44 chapters, the executed fold packages preserve source/proof/reader lineage, ten retired public slugs have historical HTML stubs, and `validate_chapter_consolidation_sequence.py` now guards those stubs directly. | Keep the 44-chapter spine stable. Do not reopen consolidation unless a named external review, source, evidence lane, or reader edit shows a specific chapter boundary is weaker than a destination. |
| P0 | Planning churn is now a release risk. | The local tree already has enough roadmap, review, scorecard, grounding, and release surfaces to execute. The best recent progress changed proof code, manifests, stubs, reader source, and evidence fixtures. | New reports are out of scope unless required by a validator, release record, external reviewer response, or an executed proof/evidence/reader/artifact change. Default to code, proof, source, evidence, reader, or artifact work. |
| P0 | The chapter-by-chapter review should become a burn-down queue, not another grade sheet. | `docs/CHAPTER_REVIEWS.md` identifies concrete per-chapter weaknesses after self-auditing its proxies. Codex verified the two manifest proof-mapping bugs: `personal-compute-hives-and-federated-edge-intelligence` and `artifact-steward-agents-and-living-project-governance` had missing chapter-level `lean_module` values despite on-disk Lean modules with 22 and 16 theorem/lemma declarations. | Keep the review as planning input only, track every chapter weakness in the roadmap burn-down below, and execute fixes as proof, source-note, evidence-import, reader-prose, or manifest changes. The two `lean_module` mappings are fixed in `book_structure.json` in the current workset; no support state moves. |
| P0 | The project needs one real measured result more than another internal sweep. | The current six upward transitions are narrow non-core lanes. The first bounded empirical local selector lane now exists for `resource-economics.scoped_workflow_trace_route_selector`, with a baseline, negative control, residuals, and an accepted transition; no 44 chapter core claims have moved above `argument`, and no deployed or externally reviewed architecture claim has moved. | Keep deepening evidence through one selected lane per cycle: either move another narrow lane through accepted transition review or record an explicit no-promotion decision, then pursue live/external replay before any chapter-core support-state movement. |
| P0 | Chapter credibility requires external grounding, not only Corben-side source synthesis. | Appendix H already contains source-noted external literature, but the roadmap does not yet force every chapter to mine external comparators from the Corben papers it already cites. | Add a chapter-by-chapter external-grounding milestone: mine each chapter's linked Corben sources for bibliographies and adjacent work first, then add vetted third-party records to Appendix H through `sources/source_inventory.json` and source notes. |
| P1 | Appendix C hides the earned non-core transitions too well. | Appendix C correctly says all 44 chapter core claims remain `argument`, but it does not make the six non-core transitions headline-visible. | Keep the separate non-core evidence ledger visible so readers can see what is actually measured without mistaking it for chapter-core promotion. |
| P1 | External-SOTA placement is technically closed but intellectually thin in places. | `docs/external_sota_positioning_audit.md` records 44 positioned chapters, 0 explicit exceptions, 0 open placement rows, and 0 missing targeted source notes after the current grounding cycle. | Keep the external-grounding records live: future chapter splits, merges, or new claims must preserve fair external baselines or record a deliberate exception. |
| P1 | Circle evidence is real but not yet a clean upstream replay. | `docs/circle_external_receipt_slice.md` records a local clean checkout and accepted rope receipt, `docs/circle_public_replay_consumer_gate.md` adds a CI-verifiable ASI-side consumer gate with negative controls, and `evidence_transitions/v1_x_measured/circle_public_consumer_gate_no_change.json` records that gate as an accepted `blocks_promotion` no-change decision. The ASI repo still does not rerun the external checkout in CI or vendor a public replay pack. | Treat the consumer gate and no-promotion decision as accountability closure, then pursue a public contract pack, archived evidence bundle, or clean replay before stronger claims. |
| P1 | Project Theseus is the right implementation reference; the first imports are intentionally narrow. | `docs/local_project_mining_theseus_circle.md` records public-safe Theseus mining and source notes; `docs/theseus_report_import_slice.md` records one static digest-verified architecture-gate report import; `docs/theseus_generation_mode_import_slice.md` records one static digest-verified generation-mode import; `docs/theseus_support_replay_probe.md` records a local replay of both ASI-side validators with command-output and artifact digests; `docs/theseus_public_task_bundle_import.md` records one bounded public task-bundle summary import with 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 task-level regressions, visible artifact gaps, and seven expected-invalid controls; `docs/theseus_fast_support_lane_run.md` records the selected Theseus/Fast support-lane aggregate `theseus-fast-support-lane-2026-07-03-local` with 4 command replays, 16 tracked artifact digests, 68 public task records, 14 expected-invalid or rejected controls, 2 accepted no-promotion decisions, and `theseusFastSupportAggregateFixture`; and `evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json` records the accepted no-promotion decision. The local checkout still had private/dirty surfaces, so no clean live Theseus replay or upward support-state transition exists, and the import/aggregate do not prove model quality or promote any chapter core claim. | Keep the static imports, support probe, public task-bundle import, and selected support-lane aggregate as implementation-reference evidence only, keep no-promotion decisions visible, then pursue a clean replay or archived public fixture with environment notes, publication permission, missing-artifact closure, and external review before any stronger transition. |
| P2 | The reader edition is structurally mature but not yet a true human book. | Human view, reader overlays, reader spine checks, companion-note routing, and HTML artifact review exist; the current reader projection has 73 active/applied overlay operations across 30 chapters, 0 high-priority and 0 medium-priority heuristic review rows, and 0 generated-reader paragraphs at or above 160 words. The curated manuscript path is still overall `drafting`, but now has 44 active curated chapter records with 0 drafting and 44 reconciled for prose meaning, no active manifest chapter missing a curated reader file, a validated reader handoff contract for thesis/arcs/signature ideas/voice slots, and all ten current key-figure targets backed by draft live-chapter assets, text-equivalent chapter anchors, curated reader-manuscript placements, rendered curated-reader HTML DOM checks with captions, alt text, responsive classes, copied SVGs, non-claim boundaries checked by `scripts/validate_reader_key_figures.py` and `scripts/validate_reader_key_figure_html_probe.py`, a measured contrast/readability gate checked by `python3 scripts/validate_reader_key_figure_contrast.py` with result `editions/reader_manuscript/v1_0/key_figure_contrast_manifest.json`, a source-geometry review checked by `python3 scripts/validate_reader_key_figure_geometry.py` with result `editions/reader_manuscript/v1_0/key_figure_geometry_manifest.json`, a source-level visual identity review checked by `python3 scripts/validate_reader_visual_identity.py` with result `editions/reader_manuscript/v1_0/visual_identity_manifest.json`, a source-level accessibility/navigation review checked by `python3 scripts/validate_reader_accessibility_navigation.py` with result `editions/reader_manuscript/v1_0/accessibility_navigation_manifest.json`, an automated curated-reader HTML keyboard traversal review checked by `python3 scripts/validate_reader_keyboard_navigation.py` with result `editions/reader_manuscript/v1_0/keyboard_navigation_manifest.json`, a keyboard-only evidence decision checked by `python3 scripts/validate_reader_keyboard_only_decision.py` with result `editions/reader_manuscript/v1_0/keyboard_only_decision_manifest.json`, an automated curated-reader HTML accessibility-tree release-preparation probe checked by `python3 scripts/validate_reader_accessibility_tree.py` with result `editions/reader_manuscript/v1_0/accessibility_tree_manifest.json`, a local EPUB/DOCX/PDF package/text probe checked by `python3 scripts/validate_reader_key_figure_format_probe.py` with result `editions/reader_manuscript/v1_0/key_figure_format_probe_manifest.json`, an automated PNG raster fallback probe checked by `python3 scripts/validate_reader_key_figure_raster_probe.py` with result `editions/reader_manuscript/v1_0/key_figure_raster_manifest.json`, an EPUB key-figure XHTML layout probe checked by `python3 scripts/validate_reader_key_figure_epub_layout.py` with result `editions/reader_manuscript/v1_0/key_figure_epub_layout_manifest.json`, a PDF key-figure caption-page layout probe checked by `python3 scripts/validate_reader_key_figure_pdf_layout.py` with result `editions/reader_manuscript/v1_0/key_figure_pdf_layout_manifest.json`, a DOCX-to-PDF key-figure title-page layout probe checked by `python3 scripts/validate_reader_key_figure_docx_layout.py` with result `editions/reader_manuscript/v1_0/key_figure_docx_layout_manifest.json`, a shared live/curated presentation layer in `assets/styles.scss` with `assets/skip-link.html`, and draft spoken/e-reader summaries in `editions/reader_manuscript/v1_0/companion_notes/key-figures.md` now routed into generated audio companion notes by `scripts/build_audio_script.py`. `docs/curated_reader_html_artifact_browser_review.md` now records a full local browser viability review of the tracked curated-reader HTML workspace with 98 of 98 page-view pairs passing, including 10 rendered key figures across 20 desktop/mobile figure page-view pairs with 0 failures, and all curated release blockers preserved. The format probe records 10 matched EPUB SVG titles, 10 DOCX figure stems, and 10 PDF draft-caption matches; the geometry review records 10 content-bound checks, 10 text-anchor checks, and 22.0 px minimum content edge margin; the visual identity review records 10 key figures, 54 combined colors, 5 non-neutral color families, and minimum text contrast ratio 5.19; the accessibility/navigation review records 44 one-H1 chapters, 44 handoff sections, 10 draft figure alt texts, 10 figure boundary paragraphs, 0 live-marker leaks, and 0 raw core-claim marker leaks; the keyboard traversal review records 49 pages, 98 desktop/mobile page-view pairs, 0 failed pairs, 98 skip-link activations, 98 main-content routes, and 0 keyboard-trap candidates; the keyboard-only evidence decision records `accepted_keyboard_only_evidence_for_release_preparation`, clears only `manual_keyboard_only_review_not_completed`, and preserves 9 blockers including screen-reader review, WCAG conformance, reader release approval, and audio gates; the accessibility-tree probe records 49 pages, 98 desktop/mobile page-view pairs, 0 failed pairs, 98 accessibility-tree page-view pairs, 0 unnamed interactive elements, 0 image alt failures, 0 table header failures, and 0 duplicate-ID hits; the raster review records 10 generated PNG fallbacks, 10 standard 1200 x 760 canvases, 99.954% minimum opaque pixel coverage, 27.64 minimum luminance standard deviation, and 116 minimum quantized colors; the EPUB key-figure layout review records 10 XHTML entries, 20 desktop/e-reader-like browser page-view pairs, 0 failures, 5,476 minimum body text characters, 23 minimum alt-text words, 10 px maximum horizontal overflow, and 0 image failures; the PDF key-figure layout review records 10 caption pages, 10 caption-page rasters, 165.878 pt minimum caption margin, 3.36% minimum page ink, 0.0% maximum near-edge ink, and 14.2 minimum luminance standard deviation; the Chromium PDF viewer smoke review records 2 nonblank viewer screenshots and 4.479% changed pixels after scroll; the DOCX key-figure layout review records 10 title pages, 10 title-page rasters, 72.1 pt minimum title margin, 9.53% minimum page ink, 0.0% maximum near-edge ink, and 37.95 minimum luminance standard deviation. The figures remain draft reader aids, the measured SVG contrast/readability gate is not final-art approval, the source-geometry review is not raster review, the curated HTML review is not a release record, the shared figure styling, browser layout checks, source-level visual identity review, source-level accessibility/navigation review, automated keyboard traversal review, accessibility-tree release-preparation probe, automated PNG raster review, EPUB key-figure layout review, PDF key-figure layout review, Chromium PDF viewer smoke review, and DOCX key-figure layout review are not final-art approval, manual aesthetic review, dedicated e-reader device review, e-reader application approval, final PDF figure/readability release review, Word review, LibreOffice GUI review, Google Docs review, screen-reader review, WCAG conformance, e-reader/app review, or reader release approval, the keyboard-only evidence decision clears only `manual_keyboard_only_review_not_completed` and is not screen-reader review, WCAG conformance, e-reader/app review, or reader release approval, the format-package probe is not EPUB/DOCX/PDF approval, the companion note is not narration or e-reader approval, the generated audio companion routing is not audiobook approval, and there is still no release approval. | Treat chapter-level prose reconciliation as complete, then focus on release-quality artifact work: book-level continuity, format-specific review, manual figure-artifact polish, audio/e-reader flow, screen-reader/WCAG review where release scope demands it, and an edition release record. Keep the human-reader book as a parallel derivative manuscript for pacing, examples, visual aids, and audio flow. |
| P2 | Aesthetic craft is still mostly "clean Quarto," not a designed artifact. | The site, diagrams, and format paths are functional and validated; ten reader-handoff key figures now have draft SVG assets, accessibility-oriented prose equivalents, validator-checked placements, rendered browser checks, audio/e-reader companion summaries, a measured contrast/readability gate with minimum text contrast ratio 5.19, minimum flow-line contrast ratio 3.96, minimum marker contrast ratio 3.96, minimum SVG text size 15 px, a source-geometry review with 10 content-bound checks, 10 text-anchor checks, and 22.0 px minimum content edge margin, a source-level visual identity review with 54 combined colors and 5 non-neutral color families, a local EPUB/DOCX/PDF package/text survival probe, an automated PNG raster fallback probe with 10 standard 1200 x 760 rendered fallbacks, 27.64 minimum luminance standard deviation, and 116 minimum quantized colors, a local EPUB key-figure XHTML layout probe with 10 XHTML entries, 20 desktop/e-reader-like browser page-view pairs, 0 failures, 10 px maximum horizontal overflow, and 0 image failures, a local PDF key-figure layout probe with 10 caption pages, 165.878 pt minimum caption margin, 3.36% minimum page ink, 0.0% maximum near-edge ink, and 14.2 minimum luminance standard deviation, a Chromium PDF viewer smoke review with 2 nonblank screenshots and 4.479% changed pixels after scroll, and a local DOCX key-figure layout probe with 10 title pages, 72.1 pt minimum title margin, 9.53% minimum page ink, 0.0% maximum near-edge ink, and 37.95 minimum luminance standard deviation. They remain draft reader aids rather than release-reviewed art. | Fold visual identity and figure craft into the reader-artifact milestone: key figures should be intentional, accessible, stable across web, EPUB, PDF, DOCX, and audio companion treatment, and reviewed as artifacts before reader release. The remaining figure blockers are manual aesthetic judgment, real e-reader/app/PDF/DOCX inspection, dedicated e-reader device/application review, Word/LibreOffice GUI/Google Docs review, final PDF figure/readability release review, and release-record approval, not source-level contrast, source-geometry review, source-level visual identity review, automated raster fallback smoke review, EPUB XHTML key-figure browser-report probe, PDF caption-page layout probe, Chromium PDF viewer smoke review, DOCX converted-layout probe, or package/text survival. |
| P2 | The project has many ledgers but still few promotions. | The v1.0.0 release was honest, and the current 44 core claims still remain `argument`; six narrow non-core claims moved upward, including the finite synthetic load-smoothing selector and local empirical scoped-route selector transitions. | Future roadmap work should close evidence gaps, not multiply status documents. Add ledgers only when they make support-state decisions clearer or enforceable. |

## 2026-07-02 Review Reconciliation

Corben supplied a follow-up Claude review after the 79-commit execution round.
Codex also rechecked the local tree at `8092c9cb9` before editing this
roadmap. The findings with teeth are:

- The cognitive-compilation trace harness and stack-layer traceability audit
  are no longer in-flight blockers; both are committed, pushed, locally
  validated, and the latest completed GitHub Pages run is green.
- `python3 scripts/validate_chapter_review_burndown.py` passes and proves that
  the burn-down covers 44 manifest chapters, but the roadmap still needs
  accounting discipline: rows marked `partially executed` should not stay
  vague after an artifact closes a closure class. Future row edits must either
  name the closing artifact, name the remaining closure class, or record a
  dated blocker.
- `python3 scripts/validate_proof_depth.py` now classifies 994 theorem
  declarations, including 807 derived/decomposed declarations and 183 direct
  or projection-style declarations. The counts are stronger than the older
  roadmap snapshot, but the direction remains the same: do not chase theorem
  count; chase executable-model bridges, transition properties, and negative
  cases that matter.
- The former Part I proof-coverage stragglers are no longer count/depth
  stragglers at the finite-record level: `AsiStackProofs.IntentContracts`
  now records 22 theorem declarations with expanded intent-admission route
  coverage, and `AsiStackProofs.Replacement` now records replacement-lifecycle
  route coverage plus an intent-governed replacement bridge. Their remaining
  blockers are executable and behavioral: natural-language intent parsing,
  authority-extraction quality, end-to-end stop-condition preservation,
  deployed replacement execution, live monitor-window evidence, real regression
  quality, and rollback execution.
- The two named external-grounding stragglers have been narrowed. Efficient ASI
  now has source-noted comparator grounding across sparse/distributed MoE,
  learned/query routing, prompt compression, fast generation, and benchmark
  pressure. Intent-to-Execution now has comparator grounding across
  reasoning/action traces, planning-language and HTN decomposition, durable
  workflows, DAG orchestration, BPMN process notation, high-level system
  modeling, and specification/verification-condition practice. Their remaining
  blockers are no longer citation breadth by default; they are planned tests,
  replayed vertical traces, parser/dispatcher behavior, route-quality evidence,
  residual accounting, and utility-preserving compression evidence.
- The ten draft SVG key figures are now embedded in live chapters and
  embedded/adapted in the curated reader manuscript with captions, alt text,
  and non-claim boundaries. `scripts/validate_reader_key_figures.py` makes that
  placement and metadata state part of the validation gate, and
  `scripts/validate_reader_key_figure_html_probe.py` renders the tracked
  curated reader manuscript and checks the resulting HTML DOM for image refs,
  copied SVG assets, alt text, captions, responsive classes, and non-claim
  boundary paragraphs. `scripts/validate_reader_key_figure_contrast.py` now
  adds a measured source-SVG contrast/readability gate with tracked result
  `editions/reader_manuscript/v1_0/key_figure_contrast_manifest.json`, and
  `scripts/validate_reader_key_figure_format_probe.py` records package/text
  survival for the current ignored EPUB, DOCX, and PDF artifacts with 10 EPUB
  SVG title matches, 10 DOCX figure-stem matches, and 10 PDF draft-caption
  matches. `scripts/validate_reader_key_figure_epub_layout.py` records a local
  EPUB XHTML key-figure layout probe with 10 XHTML entries, 20 desktop/e-reader-like
  browser page-view pairs, 0 failures, 10 px maximum horizontal overflow, and 0
  image failures. The remaining blocker is not placement, source contrast,
  rendered DOM presence, package/text survival, or local EPUB XHTML browser-report
  layout; it is visual polish, dedicated e-reader/app/PDF/DOCX inspection, audio
  integration, and release review before any
  human-review-ready figure-artifact claim.
- The Integrated Reference Architecture row now has validated fixtures, a
  narrative showpiece, and an actual local command replay: the Resource
  flagship lane validator replay emits a Reference Trace Record with output
  digest, artifact bundle, and the blocked-authority fixture as stop-condition
  reference. The remaining blocker is no longer craft prose or local replay;
  it is a live or externally replayed runtime trace with real layer handoffs.
- The Resource Economics flagship lane now has one accepted narrow non-core
  transition plus explicit accepted no-change/no-promotion records for the
  workflow-trace, local-replay, workload-quality, load-stability, and CI-cost
  sublanes. The next evidence decision should not be another local probe by
  default; it should bring in a stronger live/external workload artifact or
  keep the blockers visible.
- Chapter growth is now a craft risk. Local word counts show the largest live
  chapters are Compact Generative Systems (6,849 body words), Resource
  Economics (6,585), Personal Compute Hives (6,146), and Artifact Steward
  Agents (5,805), with median chapter body length around 3,943 words. Evidence
  detail is valid, but the human-reader pass should move bulky tables,
  validator minutiae, or repeated caveats to appendices/companion surfaces when
  doing so preserves evidence boundaries. The active watchlist now has explicit
  drafting companion-note routing: Planning, Routing Heads, Personal Compute
  Hives, Compact Generative Systems, Fast Generation, Resource Economics,
  Circle, CoilRA, Executable Specifications, Policy Optimization, Artifact
  Steward Agents, and Project Theseus. The remaining blocker is release-level
  review of those notes and format/audio treatment, not missing routing
  decisions for these chapters.
- Projection-style theorem declarations increased with fixture bridges. That
  is acceptable only while the classifier and chapter limitation prose keep
  projection bridges visibly distinct from substantive invariants.
- Project Theseus had the same hidden-foundation-evidence problem Circle had:
  the static architecture-gate import, generation-mode import, support replay
  probe, digests, counts, and negative/no-promotion result existed, but the
  chapter still read too abstractly. This update adds
  `python3 scripts/validate_theseus_concrete_evidence_surface.py` and surfaces
  those public-safe facts while preserving `argument` support, support-state
  effect `none` for the replay probe, and no live-Theseus/model-quality/speed
  claims.
- The command-authority-to-replacement seam now has an executable bridge. This
  update adds `python3
  scripts/validate_intent_governed_replacement_bridge.py`, result
  `experiments/intent_governed_replacement_bridge/results/2026-07-02-local.json`,
  and Lean target `lean:replacement.intent_governed.bridge` for two valid
  synthetic bridge traces and six expected-invalid controls. It closes a
  narrow IntentContracts/Replacement bridge class while preserving no parser,
  deployed dispatcher, approval-service, replacement execution, rollback
  execution, monitor-quality, regression-suite-quality, support-state
  promotion, or evidence-transition claim.

## 2026-07-02 Direction Update - Finish Without Waiting

Corben's direction, superseding every earlier voice-gating and review-gating
statement in this file:

1. **No work item may wait on Corben.** Codex pushes all prose — the
   AI/research edition and the human-reader edition — to what a demanding
   editor would call finished. Corben performs one final editing pass at the
   very end over a complete book. That pass is polish, not a release
   dependency, and it is not a reason to leave any sentence, section, figure,
   or edition unfinished.
2. **The no-fabrication rule stands, resolved by craft rather than by gaps.**
   Codex never invents Corben's first-person experience, biography, lessons,
   or convictions. It also never leaves a slot: it writes finished third-person
   prose that carries conviction, stakes, and specificity without personal
   anecdote. Optional first-person enrichment points live in one sidecar queue
   (`editions/reader_manuscript/v1_0/` handoff surfaces), never as holes in the
   manuscript.
3. **The external-review lane is parked as user-owned.** The public request
   issue and the dated outreach blocker are the standing Codex-execution
   record, not an accepted external review. Codex does not schedule outreach,
   does not gate milestones on review, and touches the lane only to ingest a
   review Corben supplies.
4. **The bar is A+ on every graded dimension, for both editions of every
   chapter.** Breadth and depth are both required; the unglamorous chapters
   get the same standard as the showpieces. Nothing is deferred on the theory
   that a human will finish it.

## Grade-To-A-Plus Map

The 2026-07-02 planning review graded the project A− overall. The 2026-07-04
self-review keeps the composite at the upper edge of A− after the idea-depth
execution round: reader arcs, sidecar voice conversion, first empirical
transition, core-claim disposition records, novelty ledger, and multiple
signature-idea fixtures now exist, but the human edition is not release-
recorded and the record-reality/receipt-faithfulness argument still needs
stronger live/external attestation or an explicit split decision. This map
turns each graded dimension into the work that closes the distance to A+. It
is an execution compass, not a claim surface; nothing here promotes a support
state.

| Dimension | Current grade | A+ bar | Work that closes the gap |
|---|---|---|---|
| Engineering / tooling / discipline | A | Gates stay green, fast, and drift-proof while the surface grows; no new ledgers unless a validator or release record requires them. | Maintenance only. Keep the full gate under a small time budget; keep validator-coverage and scaffold-drift checks green; resist probe sprawl (prefer deepening an existing lane over adding a new shape probe). |
| Epistemic honesty | A+ | Already at bar. | Preserve it through every change below; no-promotion decisions and negative results stay first-class. |
| Formal layer | A− | Executable-model depth, not count: properties over *sequences* of transitions, Lean/Python fixture equivalence on shared fixtures, and adversarial negative cases tied to live evidence lanes; projection bridges stay labeled. | The Capability replacement identity-sequence bridge, Context Transaction sequence bridge, and Resource CI failure-classification bridge are the current concrete movements from trace-summary alignment toward executable evidence invariants: Python fixtures and Lean summaries now agree on bounded canary/rollback identity, bounded ordered context read/write/taint sequences, and finite CI publication-metadata failure classification with no-promotion boundaries. Next cycles should deepen one of these toward live/external replay, real regression or memory-store evidence, monitor-window evidence, rollback dry-run evidence, external attestation, or stronger Theseus/Circle public fixtures rather than adding another field-presence bridge. |
| Evidence / validated substance | B+ | A steady cadence of *accepted* narrow transitions earned by real measurements and imports — refusals recorded honestly, but the ladder visibly climbs; every chapter's named evidence lane eventually executes. | Strengthen one selected measured, replay, or import lane per cycle to an accepted narrow transition or explicit no-promotion decision. Load-stability and workload-quality now have accepted narrow transitions, including the first empirical-test-backed local selector transition, so the next cycle should either deepen them toward live/external review or select the next public-safe Circle/Theseus/fixture lane. Keep the flagship-first pacing (one flagship, at most two supporting lanes) so the 44-lane plan never becomes a breadth trap. |
| External grounding | A− | 44/44 positioned with genuine depth everywhere: each load-bearing chapter names its comparators in prose and its `ext_` records carry source notes; no chapter reads as self-coined nomenclature. | Continue the per-chapter grounding lane through the burn-down; when a chapter's comparator set is thin, mine its linked Corben papers' bibliographies first, then add vetted third-party records through the inventory and Appendix H. |
| Writing / craft (live edition) | A− | Every part carries at least one showpiece-caliber section; the largest chapters carry their evidence without sprawl; zero template residue or merge seams anywhere. | Execute the chapter-length watchlist (move bulky tables, validator minutiae, and repeated caveats to companion/live-only surfaces where evidence boundaries allow). Extend the showpiece-trace standard to one anchor section per part. |
| Human reader edition | A− | Every one of the 44 reader chapters reads at the level of the current best ones; thesis, part arcs, and signature ideas are realized in the prose itself (not only in the handoff manifest); figures are polished per format; the edition is built, format-validated, and release-recorded. **This is the largest single gap and the first priority.** | Convert chapter-level reconciliation progress into release-quality reader artifacts: all 44 curated reader records are now reconciled for prose meaning and the legacy voice slots are sidecar-only, but release approval, format review, edition release records, figure artifact review, visual identity, and book-level final polish remain open. Keep the reader-continuity queue at 0 high-priority and 0 medium-priority rows through reviewed decisions or artifact-backed edits, and keep the 73 active overlay operations synchronized across live Human view and generated reader editions. Realize the thesis and part arcs in actual openings, endings, and transitions. Then build HTML/EPUB/DOCX (PDF where local dependencies allow), run the format validators and application-level checks the format-review matrix already defines, including its six current blocked curated-candidate rows, and produce an edition release record. "Drafting" must become reviewed release artifacts or stay visibly blocked. |
| Ideas / synthesis | A− | Every signature idea meets the four-part criterion (crisp statement, audited prior-art delta, one non-obvious consequence, strongest objection answered in place); the missing keystone concepts exist in the corpus; the governance pattern is named once as the core contribution; a contribution ledger audits novelty claims like evidence claims. | Execute the **Idea Depth Program** section as an artifact gate, not as another report: verification bandwidth, residual honesty, receipt faithfulness, epistemic trusted computing base, human oversight degradation, and verification-tax/governance economics now have first bounded closures, and pattern-language integration now has the owner spine, first control-boundary local-delta slice, and broader local-delta slice across planning, context, routing, compression, and self-improvement. The current validator-checked contribution novelty ledger has 9 signature-idea rows; nested keystones advance those rows unless a future validator-backed ledger expansion admits a distinct new contribution. Next, preserve local-delta discipline while pursuing live or externally reviewable residual-ledger storage/replay, receipt attestation/audit evidence, approval-workflow reviewer-degradation evidence, live or externally reviewable governance-tax workload evidence, and source-noted prior-art or external review before stronger pattern-language novelty language. Add keystone concepts only through the normal manifest/outline/evidence-lane process, with chapter-ownership tests before any new chapter. Maintain `docs/contribution_novelty_ledger.md` / `.json` as the novelty-positioning gate. |

Priority order when a run cannot do everything:

1. Human reader edition to finished and release-recorded (largest gap).
2. Record-reality / receipt faithfulness: strengthen the existing Artifact
   Graphs owner section into a showpiece argument and pursue live/external
   attestation or a dated split decision if ownership fails the split test.
3. Evidence cadence: one accepted narrow transition plus the next real
   Circle/Theseus import.
4. One executable-model proof bridge tied to a live evidence lane.
5. Burn-down truth maintenance: reconcile Milestone 2.5 rows against artifacts
   that already exist, in both directions, before starting new rows.
6. Idea Depth Program: move one signature idea through chapter prose, reader
   prose, contribution-ledger delta, analytic consequence, proof/evidence
   artifact or dated blocker, and explicit non-claims.
7. Status-surface sprawl: shorten validator-enforced status cells by moving
   long enumerations into generated ledgers, starting with Proof envelope.
8. Live-edition craft: chapter-length watchlist and per-part showpiece
   sections.
9. Maintenance of the dimensions already at grade.

## Operating Principles

- Retire IOUs before adding new control surfaces.
- Implementation beats another planning layer. Do not add a new roadmap,
  review packet, scorecard, destination draft, dry-run, or status report for a
  package that already has one unless an executed change, validator, release
  record, or external-review response requires it.
- Do not promote support states unless an accepted evidence-transition record
  names the evidence, command or replay path, limitations, counterevidence, and
  non-claims.
- Prefer narrow evidence transitions that are true over broad support language
  that sounds stronger than the artifact.
- Accepted no-promotion records may clarify an existing planned-only fixture,
  import, or proof boundary without selecting that chapter as an active
  evidence lane. They count as accountability work, not as upward support
  movement, and must not be used to evade the flagship lane cap.
- Lean targets should prove actual invariants over explicit records or state
  transitions, not only restate field projections.
- Every chapter should ultimately have at least one nontrivial Lean theorem or
  an explicit no-proof-yet blocker. A chapter's existing target may remain a
  traceability hook only when the roadmap records what would make it substantive.
- Project Theseus and Circle imports should be public-safe, reproducible, and
  routed through ASI Stack consumer gates before they are cited as prototype
  evidence.
- External literature should be source-noted before it is used in chapter prose
  or claim support.
- Consolidation should remove repeated skeletons, not ideas. A merged chapter
  preserves distinct mechanisms as sections, subclaims, source mappings, proof
  hooks, and implementation horizons unless a separate claim decision retires
  them.
- External-source backfill starts from the sources already attached to each
  chapter: mine the bibliographies, footnotes, citations, and adjacent terms in
  the linked Corben papers before broad web searching.
- Appendix H is generated from `sources/source_inventory.json`; do not hand-add
  citations directly to the generated appendix. Add external records, source
  notes, and chapter targets first, then regenerate the scaffold.
- Every load-bearing argument needs a visible evidence path: Lean, Project
  Theseus, Circle, source-noted external literature, external review, or an
  explicit no-promotion blocker. A path is not a proof until the artifact exists
  and the relevant validator or review record passes.
- Every signature idea needs a consequence that could be wrong: a bound,
  trade-off, impossibility, falsifiable prediction, or explicit weakening test.
  A prescription is not idea-depth closure until the book states what would
  change, fail, or become more expensive if the idea is true.
- The human-reader manuscript may change pacing, examples, openings, closings,
  and chapter flow, but it must not change claim meaning, support state, source
  boundary, proof/test status, or implementation horizon.
- The reader manuscript should be allowed to distill and select. The live
  AI/research book can keep the complete 44-chapter architecture; the human
  edition should make the essential thesis, stakes, and signature ideas
  impossible to miss.
- Do not invent first-person authorial experience, personal project history,
  emotional stakes, or claims about what Corben learned. Write finished
  third-person prose instead, and record optional author-enrichment questions in
  the sidecar queue rather than leaving reader-manuscript holes.
- Proof depth, source coverage, and validation count are not substitutes for
  craft. They protect honesty; they do not by themselves create narrative arc,
  beauty, memorability, or authorial presence.
- Audio and e-reader artifacts should come after reader-prose review, not
  before it.
- The roadmap must be able to lose: claims can be demoted or refuted, chapters
  can be merged or cut, and reviewer/prior-art findings can redirect work.
- The cold-read surface matters: readers should see what is validated, what is
  only argued, and what is explicitly unproven before they meet the broadest
  speculative architecture.

## What Is Settled From v1.0.0

Do not reopen these unless a validator fails or a new change touches them:

- public repository and GitHub Pages site exist;
- Quarto scaffold and manifest-driven order work;
- `book_structure.json` and `docs/book_outline.md` are the source-of-truth
  surfaces;
- Appendix G and Appendix H are correctly split between Corben-owned sources
  and external sources;
- all 44 current chapters exist with required sections, source mappings, proof
  hooks, implementation horizons, diagrams, and Human Reading Path bridges;
- source notes exist for current assigned source records;
- source-to-chapter and claim-source mappings are complete for the current
  manifest;
- six narrow non-core evidence transitions are recorded;
- all chapter core claims remain at `argument`;
- the v1.0 generated-reader local HTML snapshot is the only release-approved
  human-consumption artifact; the newer curated-reader HTML browser review is a
  viability review only and is not a release record;
- EPUB publication approval, DOCX, PDF, audio, DOI/Zenodo, screen-reader pass,
  and manual keyboard pass remain unresolved.

## Keystone Set And Dependency Order

The next serious run should not treat all milestones as equal. The keystone set
is:

1. keep the executed 44-chapter consolidation spine stable unless new evidence,
   external review, or human-reader edit findings expose a concrete duplicate
   artifact boundary;
2. execute one measured evidence lane with a baseline, negative control,
   residual accounting, reproducible command, and evidence-transition decision;
3. keep the external-review lane parked as user-owned: the public request and
   dated outreach blocker are the standing record; do not schedule outreach or
   gate anything on review (2026-07-02 direction);
4. finish the curated human-reader manuscript as a finished book against the
   current 44-chapter table of contents: reconcile curated source against the
   live book and push every chapter's reader prose to Codex's own editorial
   ceiling — Corben's edit comes last as polish, not as a handoff dependency;
5. execute the authorial craft pass directly: one book-level thesis, part-level
   arcs, 8-12 signature ideas, and chapter-specific openings and endings
   written to finished quality in third person, with optional first-person
   enrichment points kept in a sidecar queue rather than as gaps
   (2026-07-02 direction);
6. make the honesty system legible in 60 seconds from README, landing page, and
   Human view, and keep the six bounded non-core evidence transitions visible
   without chapter-core promotion;
7. keep the chapter-level external-grounding lane current by mining each
   chapter's linked Corben papers for outside citations, recording vetted
   third-party sources in Appendix H, and marking genuine comparator gaps;
8. advance idea depth as chapter/evidence work: one signature idea per cycle
   must update the live chapter, curated reader chapter, outline, contribution
   novelty ledger, proof/evidence artifact or dated blocker, and limitation
   prose together;
9. deepen proof work by building one transition-system or fixture-equivalence
   bridge, not by adding another broad theorem-count sweep;
10. make one Project Theseus or Circle evidence lane public-safe and
   CI-reproducible or CI-verifiable by archived digest when it directly supports
   an executed evidence lane.

Dependency order:

- Retired URL preservation is now an operating guard, not a roadmap blocker:
  `scripts/validate_chapter_consolidation_sequence.py` checks the ten historical
  stubs and their canonical targets.
- Milestone 7 curated reader completion and Milestone 5 measured evidence now
  outrank new consolidation, proof-count, or audit sweeps. Milestone 1.5 is
  parked as user-owned and outranks nothing.
- Milestone 7.5 authorial craft is downstream of the evidence boundaries but
  upstream of any claim that the human-reader edition is release-ready. Per the
  2026-07-02 direction, Codex executes the craft pass itself to finished
  quality; Corben's final edit is polish, not a release dependency, and no
  reader chapter may remain below finished quality while waiting for it.
- Milestone 2 should target one executable-model bridge at a time: a state
  transition invariant, Lean/Python fixture equivalence, or trace property that
  strengthens a selected evidence lane.
- Milestone 6.5 is dormant unless a concrete duplicate-boundary finding appears
  from source ingestion, evidence work, external review, or Corben's human-reader
  edits.
- Milestone 8 (EPUB/PDF/DOCX/audio) waits only on reconciled, finished reader
  prose and format review — the existing dated outreach blocker already
  satisfies any review precondition, so no artifact work waits on external
  review (2026-07-02 direction). Milestone 9 preprint/archive work stays
  downstream of prior-art checks and remains user-triggered.

## Beyond-SOTA Distance Map

The v1.0 Beyond-SOTA Reference Map in `docs/v1_0_roadmap.md` remains the
baseline. This roadmap measures progress by movement against that map, not by
internal activity alone.

| Dimension | Current distance from SOTA | v1.x movement target |
|---|---|---|
| Formal verification | Below full functional-correctness work; currently broad finite-record hooks with many projections. | Become competitive with lightweight state-specification practice for five safety-critical modules: explicit states, transitions, negative cases, and derived invariants. |
| Living evidence methodology | Structurally strong but still mostly self-sourced and ledger-heavy. | Become externally reviewable: visible non-core evidence, exact non-claims, public replay or CI-verifiable digests, and no hidden promotion. |
| Governance/safety architecture | Coherent argument-level stack, not deployed safety validation. | Strengthen through external review, safety-critical Lean envelopes, and at least one reproducible implementation trace. |
| Routing/resource efficiency | One bounded synthetic selector slice plus a synthetic routing decision lease harness; still below real routing SOTA, learned-router quality, deployed authority enforcement, and scheduler/load evidence. | Extend only if a public fixture or trace includes baseline, negative control, quality/adequacy, cost, residuals, source-state boundaries, and replay. |
| Compression/representation | Mostly architecture and source synthesis; Circle receipt is structural, not model-quality evidence. | Add one narrow artifact-compression, representation-preservation, or proof-contract lane with negative controls before stronger claims. |
| Human/AI dual-edition publishing | Unusual and promising scaffold with reviewed reader HTML; not yet a polished human book or audio edition. | Graduate selected reader chapters into curated prose and approve artifacts only through exact release records. |
| Authorial craft and artifact beauty | Current public site is clean and disciplined, but not yet a crafted technical-book object with unmistakable authorial presence, distilled signature ideas, and designed figures. | Turn the reader manuscript into a deliberate book: one thesis, part arcs, memorable phrases, finished third-person prose, optional sidecar author-enrichment prompts, designed key figures, and format-specific review without weakening evidence boundaries. |
| External literature/novelty | Placement gate now records 44/44 positioned chapters and 0 explicit external-baseline exceptions, but novelty questions and the depth of external engagement still remain. Some chapters can still read as Corben-originated nomenclature before readers see enough related outside literature. | Maintain the per-chapter external-grounding pack, keep mining citations inside each chapter's linked Corben papers, replace any future or regressed weak exception with source-noted literature where possible, perform prior-art checks before preprints, and record where the project is competitive, below SOTA, or genuinely novel. |
| Structural cohesion | The manifest is dynamic and complete, and the active shape is now 44 chapters after the executed consolidation packages and folds. The known packaged queue is resolved for the current table of contents; future duplicate-boundary findings should be handled as concrete evidence or reader-edit issues, not new planning churn. | Keep the 44-chapter spine stable for proof, evidence, and reader work; reopen consolidation only when a specific chapter boundary becomes weaker than a named destination. |

## Defended Contribution Tracks

The book remains broad, but v1.x should be deep. Use
`docs/a_plus_quality_scorecard.md` as the scorecard for selecting contribution
tracks. The next cycle should choose at most three of these for deep work:

| Track | Why it matters | A+ evidence bar |
|---|---|---|
| Living evidence book methodology | This is currently the strongest and most distinctive contribution. | External review, visible non-core evidence, release-gate record, validation instructions, and no-claim enforcement. |
| Claim support states and evidence laundering prevention | This turns epistemic honesty into an engineering surface. | Appendix C linkage, non-core evidence ledger, demotion/refutation path, and prior-art comparison to model cards, datasheets, reproducibility checklists, and proof-carrying code where relevant. |
| Governed self-improvement boundary | This is the most safety-critical architecture claim. | Safety-critical Lean depth, negative case, external safety review, and a public-safe Theseus architecture-gate trace or explicit blocker. |
| Proof-carrying claims and proof-carrying AI contracts | This connects the book's evidence discipline to Circle and proof-carrying computation. | Public Circle replay or CI-verifiable receipt digest, malformed receipt negative controls, and clear separation between proof legality and model quality. |
| Costed routing, residual accounting, and resource discipline | This is one of the few areas with an existing measured slice. | Extend the synthetic slice or record a public-safe trace with baseline, negative control, adequacy, cost, residuals, and no economic overclaim. |

Do not pick a track because it sounds most ambitious. Pick it because the next
evidence artifact is public-safe, externally positionable, and capable of
failing.

Current status for defended contribution focus:

- `docs/defended_contribution_tracks.md` selects five v1.x contribution tracks
  and marks three as deep-work tracks for the current cycle: living evidence
  book methodology, governed self-improvement boundary, and proof-carrying
  claims/contracts.
- `docs/defended_contribution_prior_art_positioning.md` now positions those
  five selected tracks against source-noted external comparators, including
  documentation/reproducibility, proof-carrying-code, Lean, corrigibility,
  shutdown, power-seeking, extreme-risk evaluation, risk-management,
  governance, sparse-routing, learned-routing, and cost/quality routing
  literature. It does not prove novelty, create external review, or move
  support states.
- `docs/evidence_laundering_prevention_case_studies.md` records three live
  no-promotion examples for the claim-support/evidence-laundering track:
  Theseus static import, Circle public consumer gate, and reader HTML artifact
  review. It also records one live count-surface narrowing in
  `claim_revisions/v1_x/manifest_core_claim_count_narrowing.json`, while
  preserving the harder gap that no chapter core claim has yet been truly
  demoted or refuted.
- The remaining two selected tracks, claim-support/evidence-laundering
  prevention and costed routing/resource discipline, remain selected-supporting
  tracks rather than simultaneous deep campaigns.
- `scripts/validate_defended_contribution_tracks.py` enforces the three-to-five
  selected-track gate, the at-most-three deep-work-track cap, the active-cycle
  lane anchors, and the no-chapter-core-promotion boundary.

2026-07-03 idea-focus hardening:

- Defended contribution tracks and signature-idea rows are related but not
  identical. The contribution tracks choose which public research programs the
  release defends; the signature-idea rows choose which intellectual mechanisms
  the book makes load-bearing. When they diverge, choose work that advances both
  one state to the right, or record why the current artifact can only advance
  one side without pretending it closes the other.
- The default next idea-depth order is: receipt faithfulness / record-reality
  gap, residual honesty, human oversight degradation, verification tax /
  governance economics, support-state ladder / evidence-state soundness, then
  stable capability identity and bounded self-improvement. A run may skip
  ahead only when the earlier lane lacks a public-safe artifact path and
  records a dated blocker naming the missing artifact.
- Every idea-depth closure must leave the strongest objection and the weakening
  condition in chapter prose, not only in the novelty ledger. The human-reader
  version must preserve that objection in ordinary book language, because an
  idea that is only defensible in a private ledger will still read as renamed
  prior art.
- New signature ideas are admitted only when they own a distinct interface,
  invariant, proof/evidence lane, source comparator set, and reader throughline,
  or when admitting them absorbs and shortens existing material. Otherwise they
  remain local deltas inside the existing owner chapters.
- Future idea-focused reviews from Claude, ChatGPT, Corben, or external
  reviewers should be reconciled against the dispatch table below before any
  new taxonomy, scorecard, or chapter proposal is created. If a critique names
  a gap already represented by a signature-idea row, the next action is the
  row's next closure artifact: live prose, reader prose, source/prior-art
  delta, proof/evidence movement, no-promotion decision, or dated blocker.

2026-07-04 idea-review reconciliation:

- Claude's idea-focused diagnosis has teeth, but the current roadmap already
  contains its load-bearing concepts: the governed-cognition pattern language,
  receipt faithfulness / record-reality gap, epistemic trusted computing base,
  human oversight degradation, governance economics, partitioned authority,
  stable identity, and bounded self-improvement. The next work is therefore
  execution against the dispatch table, not another idea inventory.
- Treat bounded fixtures as necessary scaffolding, not as defended
  contributions. Once a row has a bounded fixture or local repository trace,
  the next closure must move one state to the right - live/external replay,
  source-reviewed novelty posture, stronger verifier-independence evidence,
  or a dated blocker naming the exact missing artifact.
- The answer to "one meta-idea in many costumes" is not to invent more terms.
  It is to keep the pattern-language owner spine explicit, make non-owner
  chapters honest local deltas, and only admit a new signature idea when it
  changes chapter prose, reader prose, prior-art positioning, and the next
  proof/evidence artifact path.
- The remaining idea-quality risk is under-answering consequences, not missing
  labels. Support-state discipline therefore needs a truth-maintenance or
  belief-revision-quality test case: a true demotion, refutation, or claim
  narrowing caused by failed evidence, prior art, or review. More no-promotion
  examples alone do not close the evidence-state soundness idea.
- The novelty audit must be allowed to lose. If source-noted prior art
  subsumes a claimed delta, the closure is not to preserve the term with
  better rhetoric; it is to narrow the claimed contribution, change the chapter
  role to pattern application or bridge work where appropriate, update the
  contribution ledger confidence state, and keep the idea honest in both live
  and reader prose.

## Idea Depth Program - Ideas To A-Plus

Added 2026-07-03 from Corben's direct question: why Ideas was graded B+, and
what raises it. After the 2026-07-04 idea-depth execution round, the roadmap
grades Ideas/Synthesis at A−: the diagnosis has been materially answered, but
not yet defended at A+ because receipt faithfulness still needs a stronger
owner-section treatment plus live/external attestation or an explicit split
decision. Current purpose: keep the idea critique from becoming another essay.
This program complements the Defended Contribution Tracks above: the tracks
pick *which* contributions get deep evidence; this program defines what
intellectual depth means for the ideas themselves and forces that depth into
chapters, source notes, proof/evidence artifacts, and the contribution ledger.
It changes prose, structure, and argument only - it promotes no support state.

### Why Ideas Was B+ (the standing diagnosis)

1. One meta-idea in many costumes: the governance pattern (typed record +
   lifecycle + authority ceiling + evidence gate + receipt + rollback) is
   applied across most chapters; the book has roughly eight independent
   load-bearing insights and ~thirty pattern applications.
2. Prescriptive, not analytic: chapters produce requirements, rarely
   consequences (bounds, trade-offs, impossibilities, falsifiable
   predictions).
3. The best ideas began too qualitative. Verification bandwidth, residual
   honesty, verification tax/governance economics, and stable capability
   identity now have first bounded closures, but bounded self-improvement and
   live/external versions of the closed ideas still need sharper transition
   traces, public-safe workloads, or defended external review.
4. The central objection is no longer absent, but it is still underanswered
   beyond bounded records: a capable system could satisfy every gate while its
   receipts fail to correspond to reality. The receipt-faithfulness fixture
   gives a first adversarial record-level answer; the remaining A+ work is
   chapter ownership, live or externally reviewable attestation/audit evidence,
   verifier-quality review, and limits written plainly in the chapters.
5. Novelty is no longer completely unaudited: the contribution novelty ledger
   exists. The remaining risk is ledger/chapter separation - a novelty row
   that never changes the chapter can still leave readers seeing only renamed
   prior art. The next work must move ledger deltas into prose, sources, and
   proof/evidence lanes, or narrow the novelty claim when the ledger finds no
   distinct delta.

### Signature-idea upgrade queue (ranked)

1. **Verification bandwidth** → first closure exists: the deterministic
   capacity model and Lean fixture bridge now state the record-level
   long-context-theater pressure without making an empirical model-quality
   claim. The next honest artifact is not another capacity sketch; it is a
   contradiction-rate or distractor-resistance benchmark, replayed
   adequacy-classifier trace, or independent review record with logged prompts,
   baselines, negative controls, and residual accounting.
2. **The governance pattern itself** → the owner-spine and local-delta passes
   now name it once, explicitly, as the book's core contribution — a pattern
   language for governed cognition — and keep non-owner chapters from claiming
   independent novelty for ordinary pattern applications. The next honest
   artifact is source-noted prior-art review, external review, or preservation
   of local-delta discipline during substantive chapter edits; do not create a
   standalone pattern-audit report unless a validator requires it.
3. **Verification tax / governance economics** → first bounded closure exists:
   `python3 scripts/validate_resource_governance_tax_tradeoff.py` records the
   first bounded governance-tax trade-off model, with three valid modeled
   scenarios, five expected-invalid controls, two cases where full-cost
   accounting selects governance, one low-risk shortcut that remains allowed,
   Lean bridge `lean:resource.governance_tax.tradeoff_bridge`, and explicit
   no economic-optimality, deployed-scheduler, real-tax-measurement,
   chapter-core-promotion, or support-state-transition claims. The next honest
   artifact is a live or externally reviewable workload, source-noted economic
   comparator pack, or dated blocker, not another synthetic trade-off sketch.
4. **Residual honesty** → first three closures exist: the record-level
   conservation fixture accepts accepted, deferred, and discharged residual
   records while rejecting hidden, erased, unowned, support-promoting, and
   zero-residual overclaim controls, and the real repository residual-ledger
   trace in `experiments/residual_ledger_trace/results/2026-07-03-local.json`
   reads current Resource flagship, Resource workflow, Compact GVR, and
   Readiness artifacts to keep residualized deferrals, displaced costs, repair
   residuals, readiness escrow, rejected hidden burdens, and no-promotion
   decisions visible. The bounded residual-ledger storage/replay fixture in
   `experiments/residual_ledger_storage_replay/results/2026-07-04-local.json`
   replays four append-only residual events with owner handoff, discharge
   review, workload context, digest-chain construction, five expected-invalid
  controls, and a `blocks_promotion` no-change decision. This is not live or deployed residual-ledger evidence. The next honest
   artifact is live or externally reviewable residual-ledger storage/replay
   evidence, tamper/adversarial replay, or independent review, not another
   local fixture.
5. **Support-state ladder / evidence-state soundness** → first bridge closure
   exists: `python3 scripts/validate_claim_state_transition_bridge.py` records
   synthetic claim narrowing, support downgrade, and terminal refutation cases
   plus six expected-invalid controls for missing negative evidence, missing
   downgrade trigger, missing terminal effect, support-promotion laundering,
   erased non-claims, and claimed live-core movement, with Lean bridge
   `lean:evidence.claim_state.transition_bridge`. The next honest artifact is
   a real demotion, refutation, or claim narrowing caused by failed evidence,
   prior art, or review, or independent review of the ladder; do not redo the
   same synthetic bridge.
6. **Stable capability fields** → first bounded closure exists through the
   capability-replacement identity-sequence bridge; the next honest artifact is
   live or externally reviewable replacement replay, regression-floor evidence,
   monitor-window evidence, rollback dry-run evidence, evaluator-independence
   review, or a stronger Theseus/Circle public fixture. Do not spend the next
   pass only repeating the Ship-of-Theseus metaphor.
7. **Bounded self-improvement** → finite proof coverage exists, but the
   corrigibility-capability trade-off still needs to be stated as a crisp,
   arguable consequence and paired with a transition-system invariant, clean
   Theseus replay, archived public fixture, external review, or dated blocker.

The A+ criterion for every signature idea: a crisp statement, an audited
delta versus closest prior art, at least one non-obvious consequence (bound,
trade-off, impossibility, or falsifiable prediction), and its strongest
objection stated and answered in place.

Idea-depth state progression: `absent_or_scattered` -> `owned_argument` ->
`bounded_fixture_or_source_pack` -> `live_or_external_replay` ->
`defended_contribution`. These are execution states, not support-state labels.
After an idea is present in live prose, reader prose, outline routing,
contribution-ledger rows, and a bounded fixture, future work must not restart
at discovery or chapter-placement debate. It must name the next state to the
right and implement that state, or record a dated blocker. In this roadmap,
`missing_argument` means missing as a defended open-world argument or
contribution result; it does not mean the idea is absent from the corpus.
Same-state expansion counts only when it closes a different named artifact
boundary, such as moving from a synthetic fixture to a real repository trace.
Repeating the same class of local fixture over the same evidence surface is
maintenance, not idea-depth progress.

Analytic consequence rule: every signature-idea closure must name both the
consequence and the weakening condition. Examples: the verification-bandwidth
idea weakens if logged contradiction or distractor probes do not show the
claimed review bottleneck; the verification-tax idea weakens if hidden review,
fallback, and residual costs do not change the route choice; residual honesty
weakens if residual ledgers cannot preserve owner handoff and discharge review
under replay. A future run should prefer one consequence with an executable or
source-noted test over three new terms.

Consequence artifact shapes:

| Consequence shape | Honest artifact | Weakening condition to record |
|---|---|---|
| Capacity bound | Deterministic model plus logged replay or benchmark with baseline, negative control, and residual accounting. | The replay does not expose the predicted bottleneck, or the result depends only on an arbitrary fixture constant. |
| Trade-off model | Route decision or workload model that prices risk, hidden verification cost, fallback behavior, reviewer burden, and residual discharge. | Total cost, risk, or residual burden does not change the selected route, or the model omits the displaced work. |
| Impossibility or limit claim | Finite counterexample set, adversarial fixture, or proof obligation that names the assumptions under which the limit holds. | A weaker assumption set admits the desired behavior, or the counterexample only rejects malformed records. |
| Falsifiable prediction | Public-safe trace or external import with logged prompts/inputs, outcome criteria, comparator, and no-promotion boundary. | The comparator matches or beats the predicted behavior, or the trace cannot be replayed. |
| Faithfulness or identity thesis | Transition trace, attestation/audit replay, verifier-independence check, or replacement sequence with rollback and regression-floor evidence. | The system can satisfy the record shape while breaking reality correspondence, identity continuity, or rollback guarantees. |

Execution order from here:

1. **Pattern-language integration**: preserve the completed owner spine, first
   control-boundary slice, and broader planning/context/routing/compression/
   self-improvement local-delta slice. Future work should add a new local
   delta only when a chapter truly owns a distinct mechanism, and should route
   stronger novelty language through source-noted prior-art or external review.
   This stays closed by chapter edits, outline edits, reader edits, and
   contribution-ledger alignment, not by a standalone audit. This remains a
   high-priority idea-depth guardrail because it turns the repeated
   record/lifecycle/ceiling/gate/receipt/rollback pattern into an explicit
   contribution while preventing every chapter from pretending to be a separate
   novelty claim.
2. **Receipt faithfulness beyond fixture shape**: current ownership is
   section-owned in Artifact Graphs, with back-propagation into Proof-Carrying
   Claims, Integrated Reference Architecture, and Recursive Self-Improvement.
   The 2026-07-04 owner-section pass now makes Artifact Graphs carry the
   record-reality objection, bounded answer, weakening condition, and
   no-deployed-faithfulness boundary in both live and curated reader prose.
   The current local movement now includes a deterministic pseudo-random
   multi-artifact repository audit; the next movement is deployed or
   externally reviewable attestation/audit, verifier-quality evidence,
   trust-base storage/replay, or a challenge source outside this repository.
   Split into a new chapter only if
   later evidence shows the section-level treatment creates duplication, buries
   a distinct evidence lane, or makes the surrounding chapters longer and less
   clear.
3. **Epistemic trusted computing base**: first finite-record fixture now
   exists at `experiments/epistemic_tcb/results/2026-07-03-local.json`,
   guarded by `python3 scripts/validate_epistemic_trusted_computing_base.py`.
   It specifies minimal trusted core fields, root-of-trust refs,
   trust-propagation rule, recursion stop condition, verifier independence
   state, outside-the-TCB residuals, and non-claims while rejecting
   verifier-trust laundering. Remaining work is live or externally reviewable
   verifier-quality, trust-base storage/replay, and audit behavior.
4. **Human oversight degradation**: first finite-record closure now exists at
   `experiments/human_oversight_degradation/results/2026-07-03-local.json`,
   guarded by `python3 scripts/validate_human_oversight_degradation.py` and
   source-noted against human-factors automation literature. It treats approval
   fatigue, rubber-stamping, alarm fatigue, and automation bias as component
   failure modes rather than magic human safety. The accepted no-promotion
   decision at
   `evidence_transitions/v1_x_measured/human_oversight_degradation_no_change.json`
   now blocks approval-workflow, reviewer-correctness, alert-quality,
   deployed-human-factors, runtime-adapter-safety, and chapter-core promotion
   claims until stronger evidence exists. Remaining work is live or
   externally reviewable approval-workflow evidence with reviewer-load fields,
   independent-evidence checks, reviewer-rotation behavior, alert-quality
   evidence, privacy boundaries, and independent review.
5. **Governance economics, stable identity, and bounded improvement**:
   verification tax/governance economics now has its first bounded trade-off
   model, and SCF identity-under-replacement has its first bounded replacement
   sequence bridge. Do not redo the bounded governance-tax model or the bounded
   identity-sequence bridge unless the next change brings live/external replay,
   public-safe workload evidence, real regression-floor evidence,
   monitor-window evidence, rollback dry-run evidence, source-noted
   comparator grounding, or a dated blocker. Bounded self-improvement still
   needs the corrigibility-capability trade-off stated as an arguable claim
   and paired with a transition-system invariant or replayable public fixture.

No future idea-depth cycle should spend its main work budget only selecting
between chapter and section placement. If the default owner below is adequate,
ship the section/prose/outline/ledger/proof-routing change there; create a new
chapter only when the ownership test shows that doing so shortens or
disambiguates the surrounding chapters.

### Idea-depth chapter roles

The book does not need every chapter to pretend it is an independent novelty
claim. A+ idea quality means each chapter is honest about its role:

- **Signature-idea owner**: a chapter that must carry a crisp idea statement,
  prior-art delta, non-obvious consequence, strongest objection, artifact path,
  reader version, and non-claims.
- **Pattern application**: a chapter that applies the governed-cognition
  record/lifecycle/ceiling/gate/receipt/rollback pattern to a concrete layer
  and should state only the local mechanism delta, not inflate itself into a
  new contribution.
- **Bridge chapter**: a chapter whose value is the interface between two
  layers; it closes by executable handoff traces, proof bridges, or evidence
  imports, not by adding more terminology.
- **Evidence carrier**: a chapter that is currently important because it owns a
  validator, fixture, replay, import, no-promotion decision, or release gate;
  its prose should make the artifact understandable without turning artifact
  shape into support-state strength.
- **Reader synthesis chapter**: a chapter that earns its place by making the
  architecture legible to humans; it may compress evidence detail into
  companion surfaces, but it may not alter claim meaning.

Future chapter edits should state the role implicitly through prose and
explicitly in the outline only when the role affects proof, evidence, or reader
work. A chapter can change roles when a new artifact lands, but role drift is
not a reason to create a new report.

### Idea-depth closure packet

An idea-depth pass is a book change, not a thought exercise. Each pass should
produce one coherent closure packet over one signature idea unless the same
artifact genuinely closes two rows. The packet should touch existing source-of-
truth surfaces before adding any new document:

- the owner live chapter states the idea, closest-prior-art delta,
  consequence, weakening condition, strongest objection, and limitation in
  ordinary chapter prose;
- the curated reader chapter makes the same idea memorable without changing
  claim meaning, support state, proof/test status, implementation horizon, or
  source boundary;
- `docs/book_outline.md` records the chapter role, source queue, proof target,
  evidence lane, and any ownership decision;
- `docs/contribution_novelty_ledger.json` and the generated ledger prose name
  the comparator IDs, delta, confidence state, strongest objection, non-claims,
  and next artifact;
- any new comparator enters through `sources/source_inventory.json` and
  `sources/source_notes/` before it appears in chapter prose;
- the proof/evidence artifact is a Lean theorem, Python validator, public-safe
  Theseus/Circle import, measured replay, accepted transition, no-promotion
  decision, or dated blocker with exact missing conditions;
- Appendix C, proof-adequacy surfaces, release/status surfaces, and limitation
  prose are updated only if their source-of-record meaning actually changes;
- `appendices/F_changelog.qmd` and the relevant validators record the executed
  change.

The packet fails if it only renames the idea, adds a ledger row without prose,
adds a chapter paragraph without source/proof/evidence routing, or creates a
new audit surface when the existing chapter, outline, ledger, source note,
fixture, transition, or blocker can carry the decision.

The packet must also be willing to reduce ambition. If a closest-prior-art
pass shows that the project has a useful synthesis but not a distinct
contribution, the correct closure is a narrower chapter claim, lower ledger
confidence, clearer comparator language, and a role change from signature idea
to pattern application or bridge chapter where warranted.

### Idea-depth dispatch table

Use this table as the execution surface for the Ideas/Synthesis grade. Closing
a row means changing the owner chapters, reader manuscript, contribution
ledger, and proof/evidence surfaces together. A roadmap sentence, score change,
or standalone audit does not close a row.

| Signature idea | Owner surfaces | Current honest state | Next A+ closure | Does not count |
|---|---|---|---|---|
| Verification bandwidth | `verification-bandwidth-and-context-adequacy`, Evidence States, Proof Envelope | Capacity-model and contradiction-probe fixtures exist; empirical contradiction-rate, distractor-resistance, and adequacy-classifier evidence remain open. | Run or import a benchmark/replay with logged prompts, baselines, negative controls, residual accounting, and non-claims; fold the consequence into live and reader prose without support-state promotion. | Another capacity sketch, a larger context-window discussion, or a theorem that only restates fixture fields. |
| Pattern language for governed cognition | Opening stack chapter, Integrated Reference Architecture, Living Book Methodology; first non-owner control-boundary slice in Authority, Evidence States, Claim Ledgers, Artifact Graphs, Runtime Adapters, and Readiness Gates; broader local-delta slice in Planning, Virtual Context ABI, Routing Heads, Compact Generative Systems, and Recursive Self-Improvement | Owner-spine integration, the first control-boundary local-delta slice, and the broader local-delta slice are now integrated: the opener names the pattern, Integrated Reference Architecture applies it at trace scale, Living Book Methodology applies it reflexively to book changes, Authority owns can/may ceilings, Evidence States owns claim movement, Claim Ledgers owns belief continuity, Artifact Graphs owns record-reality, Runtime Adapters owns effect leases, Readiness owns routability, Planning owns obligation ordering, Virtual Context ABI owns governed addressability, Routing owns capability leasing, Compact Generative Systems owns residual custody, and Recursive Self-Improvement owns promotion legitimacy under self-reference. The contribution novelty ledger records this as positioning rather than novelty proof. | Preserve the local-delta discipline in future chapter/outline/reader edits and pursue source-noted prior-art or external review before stronger pattern-language novelty language. | A standalone pattern report, blanket novelty language, adding new terminology to every chapter, or treating each pattern application as an independent contribution. |
| Verification tax and governance economics | Resource Economics, Fast Generation, Readiness/Residual Escrow | The first bounded governance-tax trade-off model now exists: `python3 scripts/validate_resource_governance_tax_tradeoff.py` prices risk, route quality, hidden verification and fallback cost, reviewer burden, residual discharge, protected-gate deletion rejection, and low-risk shortcut allowance, with Lean bridge `lean:resource.governance_tax.tradeoff_bridge`; the Resource CI profile now also has `lean:resources.ci_failure_classification.fixture_bridge` for finite publication-pipeline failure classification and no-promotion accounting. These are synthetic or metadata-bound and do not measure real verification tax, prove scheduler behavior, prove economic optimality, or promote the Resource Economics core claim. | Move from modeled trade-off and CI metadata to a live or externally reviewable workload, public-safe workload-quality replay, source-noted economic comparator pack, or dated blocker with route quality, hidden cost, fallback behavior, reviewer burden, residual discharge, and non-claims preserved. | Redoing the bounded governance-tax model, cost-only speedups, no-op validator timing, CI deploy metadata treated as workload evidence, or ignoring displaced verification work. |
| Residual honesty | Compact Generative Systems, Resource Economics, Readiness/Residual Escrow | Residual-conservation fixture, real repository residual-ledger trace, and bounded residual-ledger storage/replay fixture exist; live/deployed storage and replay remain unproven. | Produce live or externally reviewable residual-ledger storage/replay with owner handoff, discharge review, workload context, tamper/adversarial replay behavior, independent review, and explicit no-promotion or transition decision. | Another local trace or local fixture over the same evidence surface, rhetorical "nothing disappears" prose, or residual fields without replay behavior. |
| Support-state ladder / evidence-state soundness (Support-state discipline) | Evidence States, Claim Ledgers, Appendix C, Living Book Methodology | Ledger completeness, no-promotion decisions, accepted-transition audits, the contribution novelty ledger, and the first claim-state transition bridge now exist; the bridge records bounded synthetic narrowing, downgrade, and refutation cases with rejected support-laundering/live-claim-movement controls, but no live chapter core claim has been narrowed, demoted, deprecated, or refuted. | Record a real demotion/refutation/narrowing case caused by failed evidence, prior art, or review, or obtain independent review of the ladder's claim-state soundness and limits. | More examples of no-promotion alone, redoing the same synthetic claim-state transition bridge, moving wording without changing a claim decision artifact, or citing AGM/truth-maintenance literature without an ASI Stack claim-state movement. |
| Stable capability identity | Stable Capability Fields, Capability Replacement, Project Theseus | SCF lifecycle and replacement fixtures exist, and the Capability replacement identity-sequence bridge now gives the first bounded sequence invariant over canary and rollback: one field identity, failed-monitor default blocking, prior restoration, authority preservation, residual ownership, rejected sequence controls, and no support-state promotion. This is still not a defended open-world transition theory. | Move from the bounded identity sequence toward live or externally reviewable replacement replay, real regression-floor preservation, monitor-window evidence, rollback dry-run evidence, evaluator-independence review, and Theseus/Circle-public fixture ties. | More versioning metaphors, single-state qualification checks, or redoing the same synthetic identity sequence without stronger replay/evidence. |
| Bounded self-improvement | Recursive Self-Improvement, Capability Replacement, Project Theseus | Safety-critical finite-record proof coverage exists; clean Theseus replay and live improvement trace remain open. | Pair a transition-system invariant with a clean Theseus replay or archived public fixture that shows evaluator independence, authority ceiling, rollback, monitor window, and non-claims. | More theorem count, self-improvement prose, or private/dirty project summaries. |
| Human oversight degradation | Runtime Adapters, Human Intent, Evidence States | Finite fixture, human-factors grounding, and accepted `blocks_promotion` no-change decision exist; deployed or externally reviewable approval-workflow evidence remains open. | Produce approval-workflow traces with reviewer-load fields, independent-evidence checks, reviewer rotation, alert-quality evidence, privacy boundary, residuals, and independent review before any upward support movement. | Treating human approval as inherently safe, adding more approval fields, citing automation literature without adapter evidence, or counting the no-promotion decision as an active upward lane. |
| Record-reality gap | Artifact Graphs, Proof-Carrying Claims, Integrated Reference Architecture, Bounded Self-Improvement | Receipt-faithfulness and epistemic-TCB fixtures exist; the receipt-faithfulness fixture now has accepted no-promotion decision `evidence_transitions/v1_x_measured/artifact_receipt_faithfulness_no_change.json` for receipt-shape overclaims, and the epistemic-TCB fixture now has accepted no-promotion decision `evidence_transitions/v1_x_measured/artifact_epistemic_tcb_fixture_no_change.json` for verifier-trust overclaims. The receipt repository audit checks selected real repository receipt records at `experiments/receipt_repository_audit/results/2026-07-03-local.json`, the deterministic challenge checks `experiments/receipt_repository_audit/results/2026-07-04-challenge.json`, and accepted no-promotion decision `evidence_transitions/v1_x_measured/artifact_receipt_repository_audit_challenge_no_change.json` records the audit/challenge as a `blocks_promotion` boundary for receipt-reality overclaims. The record-reality sequence bridge at `experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json` checks one stale/partial/fresh replay sequence with four rejected controls and accepted no-promotion decision `evidence_transitions/v1_x_measured/artifact_record_reality_sequence_no_change.json`, the live artifact attestation probe at `experiments/artifact_live_attestation/results/2026-07-04-local.json` checks one current produced artifact through filesystem bytes, git object bytes, command replay, independent observer routes, a trap receipt, attestation limits, and seven mutation controls, the randomized artifact attestation audit at `experiments/artifact_randomized_attestation/results/2026-07-04-local.json` checks four deterministic-seed selected public-safe repository artifacts through 12 filesystem/git/command observation routes, four rejected trap receipts, and eight mutation controls, and the GitHub Pages CI attestation at `experiments/artifact_github_pages_ci_attestation/results/2026-07-05-local.json` records GitHub Actions run `28733145259` completing the `Publish Quarto site` workflow on `main` with successful source validation, Lean build, HTML render, live Human view validation, browser Human-view smoke test, Pages artifact upload, and deploy for commit `fdff2c1cb0a100e4c68099adc5128d3b461384fd`. Accepted no-promotion decision `evidence_transitions/v1_x_measured/artifact_github_pages_ci_attestation_no_change.json` records the CI service run as a `blocks_promotion` side lane only. Live and curated Artifact Graphs prose now carry the record-reality owner section and an explicit authority ladder: stored receipt, inspectable artifact, reviewable artifact, overclaim blocker, authority-affecting record, objection, bounded answer, weakening condition, limits of traps/cross-checks/attestation, receipt-faithfulness no-promotion boundary, repository audit/challenge no-promotion boundary, record-reality sequence no-promotion boundary, live local probe, randomized local audit, GitHub Pages CI attestation boundary, epistemic-TCB no-promotion boundary, and no-deployed-faithfulness boundary. Open-world receipt faithfulness, independent external human review, reader release approval, deployed attestation behavior, and verifier correctness remain unproven. | Keep Artifact Graphs as the current owner; do not split into a new manifest-backed chapter unless later evidence shows the section-level treatment creates duplication, buries a distinct evidence lane, or makes adjacent chapters less clear. The next artifact route is deployed or externally reviewable attestation/audit replay beyond CI service status, independent verifier-quality, trust-base storage/replay, challenge sources outside this repository, and incentive-limit evidence. | Schema-valid receipts, self-checking by the same component, unbounded attestation language, trust-base naming without roots and residuals, CI service status treated as external human review or reader release approval, another repository-only audit over the same records without stronger external/deployed replay/evidence, or adding a new chapter that only repeats the Artifact Graphs owner material. |

Nested keystone responsibilities are not extra signature-idea rows unless the
contribution ledger is deliberately expanded and its validator updated.
Epistemic trusted computing base work currently advances the record-reality
gap; partitioned authority advances inter-stack/distributed governance work;
interpretability-as-evidence advances support-state soundness; constitutional
amendment legitimacy advances bounded self-improvement and constitutional
alignment. Treat them as first-class book work through the ownership table
below, but do not count them as A+ idea-depth closures unless they update the
owner chapter, reader chapter, outline route, source/prior-art position, proof
or evidence artifact, non-claims, and the relevant ledger state.

### Idea-depth acceptance gate

An idea-depth row is not closed by better naming. It is closed only when one
signature idea has all of the following in the same coherent change set or in
clearly linked artifacts:

- live/research chapter prose that states the idea, its prior-art delta, its
  non-obvious consequence, and the strongest objection without support-state
  inflation;
- a stated weakening condition: what result, replay failure, prior-art finding,
  reviewer objection, or missing artifact would force the idea to narrow,
  demote, or stay argument-level;
- human-reader prose that makes the same idea memorable in ordinary book
  language without changing claim meaning or fabricating Corben's first-person
  experience;
- a current `docs/contribution_novelty_ledger.json` row with source-noted
  comparators, confidence state, next artifact, and non-claims;
- either a proof/evidence artifact (Lean theorem, Python validator, public-safe
  Theseus/Circle import, measured replay, source-note pack, or evidence
  transition/no-promotion record) or a dated blocker explaining exactly why no
  honest artifact can be produced yet;
- chapter limitation prose and release/status surfaces that keep the idea from
  becoming a deployed-safety, model-quality, benchmark, external-review,
  novelty-proof, or support-state claim;
- relevant validators, changelog, and render checks updated.

Work at most one signature idea to this gate per autonomous cycle unless the
same artifact truly closes two rows. Verification bandwidth and residual
honesty now have first record-level closures, residual honesty also has a first
real repository residual-ledger trace and a bounded storage/replay fixture with
no-promotion decision, and receipt faithfulness now has both a
first bounded adversarial fixture with accepted no-promotion decision
`evidence_transitions/v1_x_measured/artifact_receipt_faithfulness_no_change.json`
and a first receipt repository audit at
`experiments/receipt_repository_audit/results/2026-07-03-local.json`. The next
idea-depth closure should either move residual honesty beyond local repository
traces and bounded replay fixtures into live/external storage-and-replay
evidence, move receipt faithfulness
beyond finite synthetic records and repository-only tracked digest checks into
live/external attestation-and-audit evidence, or close the next signature
idea's prior-art delta and objection in chapter prose.

Do not redo bounded fixtures just because the roadmap still names an idea as
argument-level. If a row already has a finite fixture, repository audit, or
source pack, the next acceptable movement is live/external evidence, a stronger
transition trace, a source-noted analytic consequence, an accepted no-promotion
decision, or a dated blocker that names the exact missing artifact.

### Missing keystone concepts (ranked, with routing)

Here "missing" means missing from the defended-contribution layer, not absent
from the manuscript. Receipt faithfulness, the epistemic trusted computing
base, and human oversight degradation now have owner chapters, reader prose,
outline routing, source or comparator grounding, bounded fixtures, and
non-claim boundaries. Their remaining gap is the harder one: live/external
evidence, verifier or reviewer quality, replayable attestations, and defended
argument-level consequences that survive the strongest objection.

1. **Receipt faithfulness / the record-reality gap** — current ownership is
   Artifact Graphs, with back-propagation into Evidence States,
   Proof-Carrying Claims, Integrated Reference Architecture, and Bounded
   Self-Improvement. A dedicated chapter is allowed only if a split test shows
   it would shorten, absorb, or disambiguate existing material instead of
   repeating the Artifact Graphs owner section. This is the
   architecture's answer to "can records bind a capable optimizer":
   attestation, trap fixtures, randomized deep audits, cross-examination
   between independent components, incentive design — each with limits. The
   minimum artifact is now implemented as the receipt-faithfulness adversarial fixture:
   `python3 scripts/validate_receipt_faithfulness.py` writes
   `experiments/receipt_faithfulness/results/2026-07-03-local.json` and checks
   three bounded valid records plus six expected-invalid controls, including a
   shape-valid but reality-false receipt, a trap-receipt negative control,
   missing independent cross-check routes, same-component self-check laundering,
   unbounded attestation, and support promotion from receipt shape. The next
   repository-level artifact is also implemented as the receipt repository
   audit: `python3 scripts/validate_receipt_repository_audit.py` writes
   `experiments/receipt_repository_audit/results/2026-07-03-local.json` after
   checking selected real repository receipt surfaces, tracked digest integrity,
   command pass records, Circle external rope receipt fingerprints, non-claims,
   and no support-state promotion. The challenge, live probe, and randomized
   local audit are also implemented:
   `python3 scripts/validate_receipt_repository_challenge.py` writes
   `experiments/receipt_repository_audit/results/2026-07-04-challenge.json`,
   `python3 scripts/validate_artifact_live_attestation_probe.py` writes
   `experiments/artifact_live_attestation/results/2026-07-04-local.json`, and
   `python3 scripts/validate_artifact_randomized_attestation_audit.py` writes
   `experiments/artifact_randomized_attestation/results/2026-07-04-local.json`
   after checking four deterministic-seed selected public-safe repository
   artifacts through filesystem bytes, git object bytes, command replay, trap
   receipts, attestation limits, and eight mutation controls. Remaining work:
   deployed or externally reviewable attestation/audit behavior, independent
   verifier-quality review, trust-base storage/replay, incentive analysis, and
   a section-versus-split stress test only if the owner section starts hiding a
   distinct evidence lane. Current status is
   `randomized_artifact_attestation_backed_not_open_world`; these fixtures,
   audits, challenge, and local attestation probes do not prove open-world
   receipt faithfulness, deployed attestation, deployed audit behavior,
   external project truth, or chapter-core support.
2. **The epistemic trusted computing base** — chapter-worthy if the ownership
   test later shows it should stand alone; who verifies the verifier and where
   recursion bottoms out; unifies security-kernel, tribunal, and
   evidence-discipline material into a minimal-trusted-core thesis. The first
   artifact is now implemented as the epistemic trusted computing base fixture:
   `python3 scripts/validate_epistemic_trusted_computing_base.py` writes
   `experiments/epistemic_tcb/results/2026-07-03-local.json` and checks three
   bounded valid records plus six expected-invalid controls for missing root
   of trust, verifier-trust laundering, unbounded trust propagation, missing
   recursion stop, erased outside-TCB residuals, and support promotion from
   trust-base shape. Remaining work: chapter-ownership decision, live or
   externally reviewable verifier-quality evidence, trust-base storage/replay
   behavior, audit-log durability evidence, and an explicit policy-correctness
   boundary. The fixture does not prove verifier correctness, deployed
   trust-base behavior, open-world receipt faithfulness, or chapter-core
   support.
3. **Human oversight degradation** — chapter-worthy if the ownership test later
   shows it should stand alone; approval fatigue, rubber-stamping, alarm
   fatigue, and automation bias; treat the human approver as a component with
   failure modes, grounded in human-factors literature. The first artifact is
   now implemented as the Human oversight degradation fixture:
   `python3 scripts/validate_human_oversight_degradation.py` writes
   `experiments/human_oversight_degradation/results/2026-07-03-local.json` and
   checks three bounded valid records plus seven expected-invalid controls for
   missing reviewer qualification, fatigued approval acceptance,
   rubber-stamped approval, automation-bias contradiction, alarm fatigue,
   support promotion from approval shape, and missing non-claim boundaries.
   Remaining work: chapter-ownership decision, live or externally reviewable
   approval-workflow traces, reviewer-load and reviewer-rotation evidence,
   independent-evidence-check behavior, alert-quality evidence, and an explicit
   reviewer-surveillance/privacy boundary. The fixture does not prove reviewer
   correctness, approval-service quality, deployed human-factors behavior, tool
   safety, or chapter-core support.
4. **Inter-stack governance** — chapter-worthy if scope allows; contracts,
   trust establishment, and collusion between independent governed stacks.
5. **Interpretability as an evidence class** — major section in
   evidence-states (a white-box rung in the support ladder).
6. **Governance under partition** — major section in personal-compute-hives
   (revocation propagation, grant/effect races, authority consistency —
   CAP-for-authority).
7. **Constitutional amendment legitimacy** — major section in
   constitutional-alignment (who may amend, by what process, what makes it
   legitimate rather than merely gated).

New chapters enter through the normal manifest, outline, source-queue, proof-
target, and evidence-lane process like every existing chapter; both editions
receive finished prose per the 2026-07-02 direction. The spine-stability rule
permits these as named-finding additions only after the ownership test shows a
distinct interface, invariant, artifact type, evidence lane, proof family, and
reader throughline; it forbids churn, not growth.

Keystone insertion rule: prefer a major section inside the strongest existing
chapter when the concept sharpens an existing artifact boundary; create a new
chapter only when it owns a distinct interface, invariant, artifact type,
evidence lane, proof family, implementation horizon, and reader throughline.
Any new keystone chapter must also identify what existing chapter text it
absorbs, shortens, or disambiguates so the book does not grow by simply adding
another full skeleton.

Ownership decision output: receipt faithfulness is currently owned by Artifact
Graphs for the next implementation pass. The epistemic trusted computing base
and human oversight degradation still use the default owner table below unless
a future split test proves a standalone chapter would reduce duplication and
clarify a distinct evidence lane. The next change that touches any row must do
one of three things: integrate the concept as a major section with outline
source/proof rows in the owning chapter; add a manifest-backed chapter through
the normal `book_structure.json` and scaffold process after the split test; or
record a dated no-new-chapter decision naming the owner chapter and remaining
blocker. A passing validator, ledger row, or prose mention alone is not enough
to settle ownership.

Current ownership table for the next implementation pass:

| Concept | Current owner / split condition | Minimum next book change | Minimum next artifact route |
|---|---|---|---|
| Receipt faithfulness / record-reality gap | Current owner: `artifact-graphs-audit-logs-and-replay`, with back-references from Proof-Carrying Claims, Integrated Reference Architecture, and Bounded Self-Improvement. Split only if later evidence shows the upgraded owner section creates duplication, hides a distinct evidence lane, or makes adjacent chapters less clear. | Owner-section treatment now integrated in live and curated reader prose: explicit authority ladder, objection, bounded answer, limits of attestation/traps/cross-checks, repository receipt audit/challenge route, local live artifact attestation probe, deterministic pseudo-random multi-artifact repository audit, epistemic-TCB limit, weakening condition, and no-deployed-faithfulness boundary. Preserve this as section-owned unless a future split test is artifact-backed. | Deployed or externally reviewable attestation/audit replay, independent verifier-quality record, trust-base storage/replay evidence, external/randomized challenge source outside this repository, or dated blocker. |
| Epistemic trusted computing base | `security-kernel-and-digital-scifs` and `artifact-graphs-audit-logs-and-replay`, with constitutional amendment legitimacy routed through Constitutional Alignment when authority change is involved. | State the minimal trusted core, recursion stop, trust propagation, outside-TCB residuals, and verifier-correctness non-claim without implying that a finite fixture proves open-world trust. Accepted no-promotion decision `evidence_transitions/v1_x_measured/artifact_epistemic_tcb_fixture_no_change.json` now makes the finite fixture a blocking decision for verifier-trust overclaims, not support-state movement. | Trust-base storage/replay evidence, verifier-independence check, audit-log durability probe, or dated blocker. |
| Human oversight degradation | `runtime-adapters-tool-permissions-and-human-approval`, with support-state implications routed through Evidence States and intent implications routed through Human Intent. | Treat reviewer fatigue, rubber-stamping, alarm fatigue, automation bias, reviewer privacy, and reviewer-rotation limits as component failure modes in live and reader prose. | Approval-workflow trace with reviewer-load fields, independent-evidence checks, alert-quality evidence, privacy boundary, no-promotion decision, or dated blocker. |
| Inter-stack governance | `scf-control-plane-routing-and-coherence`, Personal Compute Hives, and Security Kernel unless a distinct cross-stack contract interface emerges. | Define trust establishment, collusion risk, contract handoff, and revocation between independent governed stacks without implying a deployed ecosystem. | Public-safe contract fixture, cross-stack attestation trace, collusion negative control, or dated blocker. |
| Interpretability as an evidence class | Evidence States, with downstream mentions in Proof-Carrying Claims and Benchmark Ratchets. | First source-noted pass now adds Transformer Circuits and monosemantic feature-decomposition comparators, plus live and curated reader prose that treats interpretability as a scoped evidence role rather than a magic support state; no circuit analysis, sparse-autoencoder run, model-transparency result, or support-state promotion is claimed. | Mechanistic-evidence admissibility fixture, interpretability evidence-packet schema/rule with negative controls, downstream Proof-Carrying/Benchmark mentions, or dated blocker. |
| Governance under partition | Personal Compute Hives and Runtime Adapters. | First bounded closure now exists: live and curated reader prose state grant/effect races, stale grants, revocation-delay quarantine, fresh authority receipt requirements, residual ownership, and CAP-style authority consistency limits in the hives/runtime boundary; `python3 scripts/validate_partitioned_authority_fixture.py` records the finite partitioned-authority fixture at `experiments/partitioned_authority/results/2026-07-03-local.json` with 3 valid records and 6 expected-invalid controls. Accepted no-promotion decision `evidence_transitions/v1_x_measured/partitioned_authority_fixture_no_change.json` now records that this finite fixture blocks deployed partition-tolerance, distributed-consensus, availability, runtime-adapter-enforcement, revocation-propagation, hive-scheduler, rented-node-sandbox, family-governance, network-overlay, security, privacy, benchmark, and chapter-core promotion claims. It is source-noted against `ext_cap_theorem_gilbert_lynch_2002` and does not prove deployed partition tolerance, distributed consensus, availability, runtime adapter enforcement, revocation propagation, or support-state movement. | Move from finite records to a live or externally reviewable grant/revocation propagation trace, partition/reconciliation replay, independent authority-service review, or dated blocker; do not redo the same finite fixture without stronger partition evidence. |
| Constitutional amendment legitimacy | Constitutional Alignment and Recursive Self-Improvement. | Define who may amend the constitution, what makes amendment legitimate rather than merely gated, and how amendment residuals are recorded. | Amendment workflow fixture, authority-ceiling proof route, external governance comparator notes, or dated blocker. |

The section-level rows above are first-class book work, not optional footnotes,
but they should close inside the named owner chapters unless a future artifact
proves that a standalone chapter would reduce duplication or clarify a
distinct boundary. A pass over any of them must update live prose, curated
reader prose, outline routing, source/proof/evidence routing, and non-claims
together; a new roadmap note alone is not movement.

### Contribution ledger

Implemented artifact: `docs/contribution_novelty_ledger.md` and
`docs/contribution_novelty_ledger.json`, guarded by
`python3 scripts/validate_contribution_novelty_ledger.py`, now audit novelty
claims the way the evidence ledger audits empirical claims: for each signature
idea and coined term — claimed contribution, closest prior art
(source-noted), the delta, non-obvious consequence, strongest objection,
confidence, and next artifact. The ledger is linked from the sixty-second
trust surface. Novelty claims without a ledger row do not belong in reader
prose. Ledger rows are not success badges: they may record a narrowing,
demotion, or "useful synthesis but not distinct contribution" finding when
closest prior art is stronger than the current ASI Stack delta.

## Milestone Plan

### Milestone 0 - Release-Preserving Discipline

Goal: make every future long run safe to start, stop, resume, and audit.

Tasks:

- Check the previous GitHub Pages run before each commit.
- Keep raw source exports, local build outputs, `_site`, `.quarto`, `.lake`, and
  generated reader/audio artifacts out of git unless a specific release record
  authorizes them.
- Keep `appendices/F_changelog.qmd` updated for meaningful roadmap, proof,
  source, evidence, reader, or release changes.
- Run the relevant validators before committing. For broad changes, use the
  full gate in the README.
- Keep `docs/v1_0_roadmap.md` as release-history context and use this file as
  the v1.x execution target.
- Keep retired chapter URL stubs guarded by
  `python3 scripts/validate_chapter_consolidation_sequence.py`.
- Reject new roadmap/report surfaces for existing work unless they are attached
  to an executed proof, evidence, source, reader, artifact, release, or external
  review change.

Acceptance bar:

- prior Pages run checked;
- working tree clean before starting a large pass;
- no stale generated scaffold after `python3 scripts/sync_scaffold.py`;
- no validator is silently bypassed or newly orphaned;
- the ten retired consolidation URLs remain preserved by historical stubs.

### Milestone 0.5 - Sixty-Second Trust Surface

Goal: make the project's strongest quality visible before a cold reader rounds
the work down to overbroad self-sourced theory.

Tasks:

- Update the README, landing page, and live Human view entry path so a first-time
  visitor can quickly see:
  - all 44 chapter core claims remain `argument`;
  - six bounded non-core evidence transitions exist and are narrow;
  - Lean coverage is broad but still shallow in safety-critical areas;
  - Project Theseus and Circle are related project lanes, not independent
    third-party evidence unless imported through a public-safe replay gate;
  - external review is requested, pending, or recorded;
  - the project is a research program and living evidence system, not a
    validated ASI implementation.
- Add a short "What this is / what this is not / what is currently evidenced"
  block to the public entry surfaces.
- Link directly to Appendix C, the non-core evidence ledger once created,
  proof-depth classification, release-gate audit, and v1.x roadmap.
- Keep the tone sober: no hype, no grandiosity, no implication that the stack
  already works as a deployed system.

Acceptance bar:

- a skeptical reader can identify the project status and non-claims from the
  README or landing page without opening internal docs;
- the entry surface names the strongest contribution as the living evidence
  methodology, not generic ASI capability;
- validation still passes and no support-state or artifact claim changes.

### Milestone 1 - Evidence Discoverability And Claim-State Clarity

Goal: make the current evidence state obvious to humans, AIs, and reviewers.

Tasks:

- Add a non-core evidence ledger surface that names:
  - `living-book-methodology.phase5_harness_registry_runner` as
    `synthetic-test-backed`;
  - `resource-economics.costed_route_budget_slice` as
    `synthetic-test-backed`;
  - `resource-economics.finite_burst_load_smoothing_selector` as
    `synthetic-test-backed`;
  - `circle-calculus.external_rope_receipt_replay` as `prototype-backed`.
  - `compact-generative-systems.compact_gvr_receipt_slice` as
    `synthetic-test-backed`.
- Link that surface from Appendix C without changing the fact that all 44
  chapter core claims remain `argument`.
- Add a validation check that prevents non-core transitions from being rendered
  as chapter-core promotions.
- Add a reviewer-facing "what would promote this" field for each chapter-core
  claim, derived from the per-chapter evidence plan below.

Acceptance bar:

- Appendix C or a sibling appendix surfaces the five earned transitions;
- the chapter-core matrix still reports 44 `argument` support states;
- validation rejects accidental chapter-core promotion language.

### Milestone 1.5 - Early External Review

Goal: reduce self-sourcing before the roadmap spends months optimizing the
wrong target.

Tasks:

- Ask at least one external human reviewer with relevant safety, formal-methods,
  governance, or AI-systems expertise to review:
  - the five safety-critical chapter claims and Lean limitation language;
  - support-state language in Appendix C and the non-core evidence ledger;
  - the v1.x Beyond-SOTA Distance Map;
  - one representative Human view chapter.
- Record reviewer input as review input, not source evidence.
- Convert actionable findings into GitHub issues or roadmap tasks with
  acceptance criteria.
- Explicitly record if the reviewer thinks a thesis is wrong, already solved,
  too weakly sourced, or not novel.

Acceptance bar:

- at least one review record exists, or a dated blocker records who was asked
  and why review has not yet happened;
- review findings are routed to proof, source, chapter, reader, or evidence
  tasks;
- no reviewer comment is treated as proof, citation, or support-state evidence
  unless it is backed by independently source-noted material.

Current status:

- Public request issue #1 is open, with supplemental consolidation and full
  consolidation request updates recorded under `external_reviews/request_updates/`.
- `external_reviews/blockers/no_named_external_reviewer_2026-07-01.json` records
  the current dated blocker: the public request is open, but no named
  independent reviewer response has been accepted and no direct outreach target
  has been authorized.
- The blocker has no source-evidence, support-state, artifact-release, or
  evidence-transition effect. Actionable routing remains pending until an
  accepted review record exists.
- 2026-07-02 direction: this milestone is **parked as user-owned**. The open
  public request plus the dated blocker satisfy the roadmap sequencing bar for
  Codex work, but they are not accepted external-review evidence. Codex must
  not schedule outreach work, must not gate any other milestone or artifact on
  external review, and returns to this lane only to ingest a review that Corben
  supplies.

### Milestone 2 - Safety-Critical Lean Depth

Goal: move the five safety-critical Lean modules from projection-only hooks
toward meaningful formal envelopes.

Priority modules:

| Module | Chapter | Current issue | v1.x proof target |
|---|---|---|---|
| `AsiStackProofs.Alignment` | `constitutional-alignment-substrate` | Projection-only constitutional traceability. | Model constitution versioning, protected predicates, conflict routing, and forbidden self-modification weakening. Prove that accepted transitions preserve protected predicates or route to review. |
| `AsiStackProofs.Corrigibility` | `agency-dignity-and-corrigibility` | Projection-only agency/corrigibility predicates. | Model interruptibility, appeal, delegation bounds, and approval timing. Prove that high-impact action requires usable review and that denial paths preserve auditability. |
| `AsiStackProofs.GovernanceRights` | `governance-rights-fork-exit-and-audit` | Projection-only right records. | Model exit, fork, audit, redaction, appeal, and preservation obligations. Prove that constrained forks retain safety obligations and audit paths. |
| `AsiStackProofs.SelfImprovement` | `recursive-self-improvement-boundaries` | Projection-only self-improvement boundary. | Model candidate change, evaluator independence, protected invariant set, rollback path, monitor window, and authority ceiling. Prove that accepted self-improvement cannot widen authority or weaken protected invariants without explicit blocked/review state. |
| `AsiStackProofs.ValueConflict` | `moral-uncertainty-and-value-conflict` | Projection-only conflict classification. | Model multi-axis conflicts, stakeholder records, uncertainty residuals, dissent, revisit conditions, and constrained decisions. Prove that unresolved high-stakes conflicts cannot collapse into unconditional promotion. |

Rules:

- Add richer records only when they are used by at least one theorem or harness.
- Prefer small derived theorems over large theatrical statements.
- Keep limitation prose updated in the relevant chapters and Appendix E.
- Do not claim deployed safety. These are formal envelopes over declared
  records.

Acceptance bar:

- all five modules contain at least one theorem classified
  `derived_or_decomposed` by `scripts/validate_proof_depth.py`;
- the new theorem's conclusion is not a stored Boolean field or direct
  projection of the input record;
- each module adds at least one negative case: a record, transition, or fixture
  that violates the intended invariant and is rejected or blocked;
- proof-depth classification shows improvement for the targeted theorem set;
- chapter limitation sections state exactly what the new proofs do and do not
  justify.

Current status after the first v1.x safety-critical proof-depth sweep:

- `Alignment`, `Corrigibility`, `GovernanceRights`, `SelfImprovement`, and
  `ValueConflict` each have at least one derived/decomposed finite-record
  theorem with a rejected or blocked negative case.
- `Alignment` now has a third v1.x depth increment: the constitutional
  lifecycle-admission route adds derived route theorems for missing predicate,
  source, operational-test, protected-scope, conflict-behavior, review,
  migration, self-modification, agency-rights, material-usability,
  pre-effect-review, rollback, correction, reviewer-independence,
  evidence-transition, and non-claim-boundary records on top of the earlier
  constitutional-transition theorems for rollback-missing migration blocking,
  accepted-transition protected-predicate preservation, and unrouted conflict
  residualization.
- `Corrigibility` now has a second v1.x depth increment: three additional
  derived agency-control theorems model high-impact action blocking when
  pre-effect review is missing, low-risk unbounded-delegation narrowing, and
  audit-residual preservation when a denied action lacks an accountable
  principal.
- `GovernanceRights` now has a second v1.x depth increment: three additional
  derived governance-rights theorems model constrained-fork blocking when
  safety obligations are missing, redaction blocking when appeal is missing,
  and exit-residual preservation when exit capability is not preserved.
- `SelfImprovement` now has a second v1.x depth increment: two additional
  derived lifecycle/review theorems model evaluator-missing protected lifecycle
  blocking and canary-monitor rollback over a richer finite record.
- `ValueConflict` now has a third v1.x depth increment: the value-conflict
  lifecycle-admission route adds derived route theorems for missing conflict
  records, value axes, stakeholder records, stakes, reversibility, authority
  boundaries, evidence requirements, review routes, high-stakes review,
  residual uncertainty, dissent preservation, authority narrowing,
  expiry/revisit records, evidence-transition records, and non-claim
  boundaries on top of the earlier review-decision theorems for residual
  blocking, dissent residualization, and authority narrowing.
- The generated proof-depth report records 994 theorem declarations, 807
  derived/decomposed declarations, 4 unknown/mixed declarations, 103
  safety-critical declarations, and 11 remaining safety-critical
  direct/projection declarations.
- The relevant chapter limitation sections now state what these finite-record
  proofs do and do not justify.
- No chapter core claim support state moved above `argument`; the next formal
  step is richer lifecycle/review semantics and tighter links to replayed
  harnesses, not broad safety language.

#### Milestone 2B - Whole-Book Proof Attack

Goal: every chapter should have a proof path with more substance than a
projection hook, or a visible blocker explaining why that chapter cannot yet be
formalized honestly.

Current proof status:

- `proofs/proof_manifest.json` records implemented proof targets across all 44
  manifest chapters after the executed fold packages preserved MoECOT,
  simulation-fidelity, command-contract, PlanForge, and semantic-representation
  proof tags in their destinations.
- `docs/proof_depth_classification.md` records 994 theorem declarations, 807
  derived/decomposed theorem declarations, 183 direct/projection-style theorem
  declarations, and 4 unknown/mixed theorem declarations.
- `AsiStackProofs.StackBoundaries` now has a finite trace-level unauthorized
  external-handoff rejection theorem and a finite layer-contract admission
  lifecycle route for the opening stack chapter, which moves that module
  further into the whole-book proof-depth campaign without implying
  whole-stack safety, deployed layer enforcement, source-to-layer completeness,
  runtime authority behavior, support-state promotion, or model capability.
- `AsiStackProofs.ProofEnvelope` now has finite negative-case theorems
  rejecting implemented proof targets with missing module/build records,
  non-Lean artifacts presented as Lean proofs, support-state promotion without
  accepted transition plus adequacy and boundary records, and external-theorem
  references without artifact refs, resolved theorem IDs, or non-claim
  boundaries; this improves the proof-envelope chapter while leaving semantic
  adequacy review, filesystem discovery, external theorem validation, source
  interpretation, and support-state promotion as blockers.
- `AsiStackProofs.Efficiency` now has finite negative-case theorems rejecting
  minimum-viable route claims when a lower-cost authorized quality-preserving
  candidate is present and rejecting open-obligation promotion without a
  residual record; this reduces the projection-only surface for the Efficient
  ASI chapter while leaving route-search completeness, cost-estimate accuracy,
  quality evaluation, residual-burden measurement, measured efficiency, and
  compression utility as blockers.
- `AsiStackProofs.CompactGenerativeSystems`,
  `AsiStackProofs.GenerateVerifyRepair`, and
  `AsiStackProofs.SemanticRepresentation` now have finite negative-case
  theorems rejecting missing residual records, lossy exactness overclaim,
  mismatched exact reconstruction, failed-verification promotion, grounded
  semantic nodes without provenance, and hierarchy updates with neither
  preserved references nor supersession, plus a finite compact-admission route
  for source artifact, compression-boundary, residual, lossy-exactness,
  reconstruction-evidence, fallback, verifier-cost, semantic-provenance,
  hierarchy-migration, evidence-transition, and non-claim-boundary gaps; this
  reduces the projection-only surface for Compact Generative Systems while
  leaving compact utility, codec correctness, reconstruction quality,
  repair-cost accounting, fallback behavior, semantic grounding quality,
  hierarchy-migration behavior, representation utility, model quality, and
  downstream consumer-policy tests as blockers.
- `AsiStackProofs.FastGeneration` now has finite negative-case theorems
  rejecting promotion candidates missing accepted-output or verifier-cost
  records, failed accelerated drafts without fallback or residual handling,
  and high-risk fast-mode selections without verifier, risk-override, or
  slower-fallback records plus a finite admission-lifecycle route for missing
  mode, context, risk, quality, verifier, acceptance, baseline, output, cost,
  fallback, residual, override, budget, evidence-transition, and
  non-claim-boundary records, plus a public Theseus import fixture bridge that
  rejects boundary-gate failure and missing-report-ref overclaims. This reduces
  the projection-only surface for Fast Generation while leaving actual
  autoregressive baselines, speculative
  decoding runs, diffusion runs, early-exit runs, state-space runs, KV-cache
  serving traces, risk-classifier behavior, route-selector behavior,
  speed-quality measurements, and useful-solution-per-second evidence as
  blockers.
- `AsiStackProofs.PolicyOptimization` now has finite negative-case theorems
  rejecting policy promotion without holdout refs or contamination checks,
  reward-proxy improvement used as sole evidence without target evaluation,
  authority-expanding updates without governance approval or rollback, and
  route-level policy-promotion paths with inadmissible feedback, missing target
  evaluation, missing reward-hacking probes, governance or authority gaps,
  missing rollback, or regression/residual gaps;
  this reduces the projection-only surface for Policy Optimization while
  leaving actual policy-update workloads, preference or reward data,
  reward-quality studies, reward-hacking probes, holdout operations,
  contamination detectors, rollback dry runs, deployment monitoring, and
  policy-safety evidence as blockers.
- `AsiStackProofs.CommandContracts` now has finite negative-case theorems
  rejecting complete command-contract status with missing required fields and
  accepted hidden overrides under explicit-constraint precedence; this reduces
  the projection-only surface for Command Contracts while leaving parser
  correctness, prompt-injection resistance, approval enforcement, deployed
  dispatcher behavior, tool-effect control, and runtime execution as blockers.
- `AsiStackProofs.BibliographyPlan` now has finite negative-case theorems
  rejecting source-derived claims without source notes or ingested artifacts
  and accepted new-source assignments to nonexistent chapters; this reduces the
  projection-only surface for Open Research Agenda while leaving citation
  accuracy, external-literature completeness, source-interpretation quality,
  public-release permission, and live new-paper triage quality as blockers.
- `AsiStackProofs.ResourceEconomics` and
  `AsiStackProofs.SimulationFidelity` now have finite negative-case theorems
  rejecting disabled required budget gates, high-risk insufficient-budget
  dispatch, missing simulation scope, and fidelity overclaim. Resource
  Economics also has a finite bridge over the four-route costed selector
  fixture, proving the bounded route eligible, rejecting the failed-verification
  and hidden-residual controls, and showing the selected route is lowest-cost
  among modeled eligible routes. This reduces the projection-only surface for
  Resource Economics while leaving scheduler
  quality, real load stability, verification-tax optimization, KV-cache
  behavior, cost-quality economics, simulator adequacy, physical feasibility,
  route-search completeness, and open-world transfer as blockers.
- `AsiStackProofs.ContextTransactions` now has a finite transaction-route
  review model for snapshot presence and freshness, source/target branch
  matching, mount repair, taint review, deleted-cell materialization, committed
  read visibility, replay boundaries, support-transition boundaries, and
  non-claim boundaries; it rejects missing or stale snapshots, branch leaks,
  unrepaired mount faults, taint without declassification, deleted-cell
  materialization without closure, invisible committed reads, missing replay
  boundaries, unsupported support-promotion attempts, and missing non-claim
  boundaries while admitting one complete modeled committed read. The bounded
  context-transaction sequence bridge adds 2 valid ordered sequence fixtures, 4
  expected-invalid controls, read-after-write checks, replay-boundary checks,
  taint-blocking checks, invalid-control rejection, and a finite Lean summary
  with no chapter-core support promotion. This reduces the projection-only
  surface for Context Transactions while leaving deployed memory-store behavior,
  runtime branch isolation, mount visibility, deletion-closure execution,
  declassification quality, replay services, poisoning resistance, VCM
  conformance, and benchmark behavior as blockers.
- `AsiStackProofs.ArtifactCompression` now has finite negative-case theorems
  for failed-probe/no-fallback use and missing residual/fallback metadata
  promotion plus a finite admission-lifecycle route for preserved-artifact,
  manifest, use-envelope, access-pattern, admission-state, decoder-readiness,
  exact-replay, failed-probe, fallback-artifact, residual-metadata,
  utility-evidence, evidence-transition, and non-claim-boundary gaps. This
  improves proof depth for RankFold/NeuralFold while leaving compression-ratio,
  decoder, behavioral fallback, and downstream-utility tests as the chapter's
  real blockers.
- `AsiStackProofs.ProofCarryingContracts` now has finite negative-case
  theorems for downstream-ready receipts missing theorem refs, deterministic
  fields, or non-claim boundaries; promoted downstream claims without contract
  readiness; stale or unsupported consumer-gate acceptance; and passing replay
  status without replay command, source digest, receipt fingerprint,
  recomputed deterministic fields, or theorem refs. This reduces the
  projection-only surface for Circle proof-carrying contracts while leaving
  theorem-id resolution, clean replay from this repo, vendored contract packs,
  transfer approval, downstream workloads, and support-state review as
  blockers.
- `AsiStackProofs.SearchSubstrates` now has finite negative-case theorems for
  missing adoption fields, unproven qualified states, qualified states without
  passing evidence, unmeasured or blocked consumer-axis reliance, and
  incomplete canary evidence packets; this reduces the projection-only surface
  for Mathematical/Search Substrates while leaving substrate A/B runs,
  representation-efficiency benchmarks, CoilMoECOT benchmarks, Mamba
  comparisons, Circle substrate-sidecar evidence, Theseus transfer consumers,
  workload reports, and falsification review as blockers.
- `AsiStackProofs.CoilAttentionMemory` now has finite negative-case theorems
  for hidden aliasing, structure-only retrieval-quality promotion, recurrence
  admission without work-budget/exit/fallback records, and stale reads admitted
  as fresh without residual escrow; this reduces the projection-only surface
  for Coil Attention while leaving real memory traces, sparse-coverage cases,
  recurrence schedules, stale-read probes, Circle/Theseus consumer gates,
  retrieval-quality tests, long-context tests, and learned-model behavior as
  blockers.
- `AsiStackProofs.CyclicMixers` now has finite negative-case theorems for
  missing claim partitions, missing baselines or tradeoff metrics,
  residue/winding alias gaps, incomplete tradeoff packets, and hardware
  mismatches without refusal paths; this reduces the projection-only surface
  for CoilRA/MultiCoil/cyclic mixers while leaving RoPE certifier replay,
  cyclic mixer benchmarks, MLX experiments, hardware-kernel benchmarks,
  downstream quality evaluations, baseline matrices, and result records as
  blockers.
- `AsiStackProofs.LivingBook` now has finite negative-case theorems for missing
  drafting artifacts, unsynced structural updates, release readiness without
  validation/changelog/residual records, and derived artifacts without
  source/review/support-state boundaries; this reduces the projection-only
  surface for Living Book Methodology while leaving manuscript-quality review,
  source-interpretation review, reader/ebook/PDF/DOCX/audio approval, external
  site availability, and human editorial judgment as separate blockers.
- `AsiStackProofs.TheseusReference` now has finite negative-case theorems for
  dashboard-only implementation-reference claims, accepted promotions with
  missing or failing gates, incomplete imported report bundles, replay-readiness
  gaps, and private-payload/support-overclaim publication boundaries; this
  reduces the projection-only surface for Project Theseus while leaving live
  report-bundle import, replay execution, work-board audits, artifact-gap
  audits, self-evolution ladder audits, and public support-state transition
  review as separate blockers.
- `AsiStackProofs.ProofCarryingClaims` now has finite negative-case theorems
  rejecting passed verifier records without verifier artifact refs and negative
  verifier results that try to produce scoped updates; this reduces the
  projection-only surface for Proof-Carrying Claims while leaving theorem
  validity, citation accuracy, semantic equivalence, verifier quality, and
  deployed review behavior as blockers.
- `AsiStackProofs.Tribunal` now has finite negative-case theorems rejecting
  high-risk accepted verdicts without adversarial probes or
  reviewer-independence records, accepted prior-review reuse without an
  unchanged-evidence guard, and action-requiring verdicts without required
  actions or constraint effects; this reduces the projection-only surface for
  the folded tribunal review lane while leaving reviewer-independence quality,
  adversarial-probe quality, prior-review semantic adequacy, verdict
  correctness, action enforcement, and deployed tribunal behavior as blockers.
- `AsiStackProofs.PersonalComputeHives` now has finite negative-case theorems
  rejecting high-risk execution without a bound approval receipt, external
  hive access with missing lease-boundary fields, and incomplete hive-work
  admission reviews; this reduces the
  projection-only surface for Personal Compute Hives while leaving scheduler,
  registry, approval-service, federation, rented-node, connectivity, dropout,
  receipt replay, residual-ledger, and energy-aware behavioral tests as blockers.
- `AsiStackProofs.RuntimeAdapters` now has finite negative-case and route
  theorems rejecting modeled invocations that lack parent-job permission,
  high-impact unapproved or underscoped-approved adapter calls, mismatched
  effect leases, expired or revoked effect leases, unsandboxed effect leases,
  over-ceiling requested authority, confused-deputy attempts, sandbox-escape
  attempts, high-impact rollback-required calls without rollback handles, and
  missing effect-receipt/audit/non-claim records; it also proves one complete
  low-impact reviewed invocation routes to dispatch. The effect-replay bridge
  now also routes missing permission, expired approval, missing no-mutation
  evidence, inexact rollback, missing receipts, repository/network side
  effects, and support-state effects away from accepted replay while accepting
  only a complete rollback-exact public-safe replay. The revocation-route
  bridge now also routes revoked approvals, leases, and authority receipts
  away from dispatch unless no-mutation denial evidence exists. This reduces
  the projection-only surface for Runtime Adapters while leaving deployed
  adapter execution, real sandbox isolation, approval-service behavior,
  secret-handle safety, deployed revocation propagation, rollback execution in
  target services, and live effect-receipt validation as blockers.
- `AsiStackProofs.StableCapabilityFields` now has a finite lifecycle-state
  transition relation over shadow, canary, qualified, default, deprecated,
  retired, and quarantined records. The new transition theorems require field
  identity preservation, forward lifecycle or quarantine paths, evidence and
  rollback for canary transitions, evidence and regression floors for
  qualification, full readiness for default promotion, and notice/receipt
  records for deprecation and retirement. The chapter still needs deployed
  route validation, evaluator-integrity measurement, real regression
  preservation, terminal-state governance, lifecycle enforcement, and rollback
  execution.
- `AsiStackProofs.ReadinessGates` now has a finite lifecycle-transition
  relation over candidate, shadow, canary, qualified, default-ready,
  quarantined, retired, and superseded records. The new transition theorems
  require forward/terminal paths, fresh gate evidence, residual escrow,
  fallback paths, expiry records, regression floors, authority scope, route
  permissions, supersession records, and retirement receipts where applicable.
  The chapter still needs deployed lifecycle transition execution, residual
  ledger storage, live quarantine routing, gate-quality checks, terminal-state
  governance, MoECOT replay, benchmark evidence, and current-readiness
  evidence.
- `AsiStackProofs.ProceduralMemory` now has finite generated-tool,
  failed-regression, lifecycle-route, and fixture-bridge coverage. Its derived
  theorems reject modeled routable transitions missing comparable trace
  clusters, negative examples, closure artifacts, verification, clean
  regressions, benchmark floor, active SCF target, retirement handling,
  monitoring plans, residuals, non-claims, or verified source state, and they
  admit the valid routable, quarantined, and retired synthetic fixture shapes.
  This reduces the projection-only surface for Procedural Memory while leaving
  deployed loop detection, tool synthesis, generated-tool correctness,
  regression-quality benchmarking, routing monitors, and retirement automation
  as blockers.
- `AsiStackProofs.Routing` and `AsiStackProofs.MoECOTRuntime` now have finite
  negative-case theorems rejecting selected routes missing authority/readiness,
  runtime-core promotions missing readiness/regression/replay evidence, and
  unavailable-text-only runtime claims that try to promote above `argument`;
  this reduces the projection-only surface for Routing Heads while leaving
  learned-router quality, route-quality measurement, deployed authority
  enforcement, runtime route execution, MoECOT replay, orchestration
  benchmarks, and specialist-quality tests as blockers.
- `AsiStackProofs.ReadinessGates` now has finite negative-case theorems
  rejecting promoted decisions with failed required gates, accepted stronger
  transitions missing fresh evidence, residual escrow, fallback, or expiry
  records, quarantined ordinary routing or diagnostic routing without fallback,
  and stale gate reuse without rerun or residual records; this reduces the
  projection-only surface for Readiness Gates while leaving gate-quality
  measurement, lifecycle-engine behavior, residual-ledger storage, live
  quarantine routing, rollback execution, MoECOT replay, current-readiness
  checks, and benchmark quality as blockers.
- `AsiStackProofs.ArtifactGraph` now has finite provenance, replay-grade,
  claim/test-link, stale-certificate, promotion, non-claim,
  artifact-admission route, and replay-packet bridge coverage. Its derived
  theorems reject modeled artifacts missing parent/source/context/transaction/
  certificate/tool/claim/test/audit/replay/evidence/non-claim fields,
  insufficient replay grade, stale certificates, and blocked promotion, while
  admitting complete non-promoted or approved-promoted records. The new
  replay-packet bridge mirrors the synthetic harness shape for parent-job
  mismatches, missing audit chains, byte-exact missing-observation blockers,
  support-review transaction validation, partial-replay promotion blocking,
  record-only partial replay, and complete bounded-review admission. This
  reduces the projection-only surface for Artifact Graphs while leaving
  deployed artifact graph service behavior, real replay, audit reconstruction,
  provenance completeness checking, and imported produced-artifact traces as
  blockers.
- The latest proof-coverage increment closed the named finite-record proof
  gap for `AsiStackProofs.IntentContracts` and `AsiStackProofs.Replacement`.
  Intent now has admission-route coverage for hidden overrides, unresolved
  ambiguity, constraint precedence, stop conditions, authority ceilings,
  preservation gaps, re-contract triggers, and non-claim boundaries.
  Replacement now has lifecycle-route coverage for identity mismatch, stale
  evidence, regression floors, canaries, monitor windows, rollback handles,
  irreversible-effect ownership, residual ownership, deprecation, retirement,
  and non-claim boundaries. Do not reopen these as theorem-count tasks unless
  a reviewer finds a specific missing invariant; the next work is executable
  parser/authority/re-contract tests and replacement trace/monitor/rollback
  evidence.
- The safety-critical modules have real derived/decomposed depth now, but many
  non-safety-critical chapters still have only traceability-style projection
  hooks.

Execution rule:

- Work through projection-heavy modules in contribution order, not alphabetical
  order: consolidation pilot chapters first, then active evidence-cycle
  chapters, then proof-carrying/evidence chapters, then remaining Part II and
  Part III modules.
- For each chapter, add or revise at least one theorem so it reasons over an
  explicit record, transition, negative case, blocked state, authority ceiling,
  readiness gate, residual path, replay receipt, or support-state boundary.
- When a chapter is merged, move the proof tags to the destination chapter and
  keep source module names only where they still clarify a distinct proof
  family.
- If a theorem would merely restate a field projection, replace the target or
  record a no-proof-yet blocker in `docs/proof_adequacy_review.md` rather than
  adding cosmetic formalism.
- Keep chapter limitation prose aligned with the theorem's actual model. Do not
  turn finite-record proofs into deployed runtime, model-quality, source
  interpretation, benchmark, or safety claims.

Acceptance bar:

- every manifest chapter has at least one theorem classified
  `derived_or_decomposed` or an explicit no-proof-yet blocker tied to the
  chapter's core claim;
- projection-only theorem counts decrease release over release;
- `lake build`, `python3 scripts/validate_proof_depth.py`,
  `python3 scripts/sync_proof_manifest.py --check`, and the full book gate pass;
- Appendix E and chapter proof-limit prose are updated when a proof's meaning
  changes;
- no support state moves unless a separate accepted evidence-transition record
  justifies it.

### Milestone 2.5 - Chapter-by-Chapter Masterwork Burn-Down

Goal: convert the calibrated 44-chapter external-review pass into executed
chapter work. This is not another scorecard. It is the concrete burn-down queue
for making the weakest chapter surfaces as proved, grounded, voiced, and
evidence-aware as the strongest ones.

Source review:

- `docs/CHAPTER_REVIEWS.md` is reviewer guidance only. It is not source
  evidence, not an external citation, not a proof result, and not a
  support-state transition.
- The human-reader comments in that review are seam/opening samples, not a full
  line edit of every reader chapter. Treat them as useful smoke tests for reader
  flow, not as release approval, final prose review, or proof that a chapter is
  ready for Corben's edit.
- Treat "light anchoring" as a request to deepen tracked source-note links and
  name prior-art families already adjacent to the chapter, not as permission to
  add placeholder citations.
- Treat "narrow proof coverage" as a request for more scenarios, transition
  invariants, negative cases, or Lean/Python fixture-equivalence bridges, not as
  a claim that existing proofs are unsound.
- Re-read the full chapter, its source queue, Appendix C row, proof module,
  harnesses, and reader projection before editing prose or tests.

Current status from this review:

- The two verified chapter-level proof-mapping bugs are fixed in
  `book_structure.json`: `personal-compute-hives-and-federated-edge-intelligence`
  now names `AsiStackProofs.PersonalComputeHives`, and
  `artifact-steward-agents-and-living-project-governance` now names
  `AsiStackProofs.ArtifactStewardAgents`. This exposes existing module
  ownership; it does not create new theorem results or support-state movement.
- `docs/CHAPTER_REVIEWS.md` should remain a living reviewer-input document only
  when a real reviewer supplies a new pass. Do not churn it after every small
  chapter edit.
- `python3 scripts/validate_chapter_review_burndown.py` now guards this
  roadmap section against dropped manifest chapters, stale chapter IDs,
  placeholder work cells, loss of the review calibration notes, and unverified
  Circle wording. This is a coverage guard for the work queue only; it does not
  grade chapters, create source evidence, or close any row.

Burn-down status semantics:

- `open`: the review weakness is still broad and no artifact-backed closure has
  narrowed it yet.
- `partially executed`: at least one real proof, source, evidence, reader, or
  manifest change has narrowed the weakness, but the row still names concrete
  remaining work.
- `blocked`: the next honest closure requires unavailable source text, private
  project artifacts, hardware, external review, or Corben authorial input; the
  blocker must be dated and specific.
- `closed by artifact`: allowed only when the row names the closing artifact or
  validation path and there is no remaining review weakness of that class. Do
  not use this status for a row that merely has better prose or a roadmap note.

Masterwork closure gates:

| Gate | What it closes | Required evidence of closure |
|---|---|---|
| Proof coverage | Reviewer notes about narrow proof surface, missing adversarial scenarios, weak lifecycle coverage, or projection-heavy formality. | Lean/Python proof or fixture artifacts that add a transition invariant, negative case, fixture bridge, or boundary theorem; updated proof-limit prose; `lake build` and proof-depth validation. |
| Test or measured evidence | Reviewer notes about planned tests, Theseus/Circle/RankFold facts left in the basement, or empirical claims that remain fixture-only. | A committed public-safe replay, measurement, digest-verifiable import, or recorded no-promotion decision with baseline/negative controls where relevant, residuals, non-claims, and validators. |
| External grounding | Reviewer notes about lightly anchored external lineage or missing named prior art. | Source-noted records in `sources/source_inventory.json` and `sources/source_notes/`, regenerated Appendix H, and chapter prose that names the comparator without treating it as validation of the ASI Stack. |
| Reader craft | Reviewer notes about recap-like Beyond-SOTA sections, visible merge scaffolds, generic phrasing, undersold contribution, or weak human-version payoff. | Live and curated reader prose edits that preserve claim meaning, support states, source boundaries, proof/test status, implementation horizons, and the no-fabricated-first-person boundary. |
| Project-evidence surfacing | Reviewer notes that Circle, Theseus, RankFold, or the book's proof layer is described abstractly despite real artifacts. | Source-verified or digest-verifiable artifact details in the chapter, validator-backed non-claims, and an explicit boundary between structural/proof evidence and model-quality, deployment, or chapter-core support claims. |
| Recorded blocker | Reviewer notes that cannot yet close because of private source text, unavailable local artifacts, hardware, external review, or Corben authorial input. | A dated blocker naming the exact missing condition and the reason the chapter should not be cosmetically rewritten around the gap. |

Priority order:

1. Fix metadata and visibility bugs first.
2. Expand safety-critical proof coverage where AI can act, route, replace,
   remember, or promote: Runtime Adapters, Stable Capability Fields, Readiness
   Gates, Context Transactions, Compact Generative Systems, Artifact Graphs,
   Procedural Memory, and Planning.
3. Surface real Circle/Theseus/project evidence where it already exists before
   writing new synthetic fixtures.
4. Backfill external anchoring through `sources/source_inventory.json` and
   source notes only after reading the source.
5. Improve reader prose and Beyond-SOTA sections where the review found recap,
   merge seams, or undersold contribution.

Execution batches:

- Batch 0, row selection and accounting: pick one row, choose one closure class,
  make an artifact-backed change, then update only that row's remaining-work
  text and the changelog. Do not open a second review pass or a new report when
  a proof, source note, evidence fixture, reader prose edit, or blocker record
  would move the row directly.
- Batch 1, proof and action-boundary depth: finish the already-started proof
  coverage campaign for Context Transactions, Artifact Graphs, Procedural
  Memory, Planning, Compact Generative Systems, Resource Economics, and any
  remaining safety-adjacent route/lifecycle modules. A batch item is not done
  until `lake build`, proof-depth validation, affected chapter limitation
  prose, and proof-artifact audit updates pass.
- Batch 2, real project evidence surfacing: pull only verified, public-safe
  Circle, Theseus, RankFold, or local harness facts into the chapters that
  currently abstract them away. Prefer replay or digest-verifiable imports
  with negative controls; otherwise record a blocker instead of polishing
  prose around unavailable evidence.
- Batch 3, external grounding: for the lightly anchored chapters, mine the
  chapter's attached Corben sources first, add external inventory/source-note
  records, regenerate generated appendices, and only then revise chapter prose.
- Batch 4, human-reader craft: after proof/evidence/source boundaries are
  current for a chapter, smooth merge scaffolds, rewrite recap-like
  Beyond-SOTA sections, sharpen signature language, and write the chapter's
  conviction and stakes to finished third-person quality; log any optional
  first-person enrichment point in the sidecar queue instead of leaving a
  slot in the prose (2026-07-02 direction).

Do not mark a burn-down row complete in prose. Mark it complete only through
the artifact that closes it: a proof commit, source-note/inventory commit,
evidence-transition or no-promotion record, chapter/reader prose commit, or a
recorded blocker with the validator or source condition that blocks execution.

Closure classes:

- `proof-coverage`: add or revise Lean/Python proof and fixture artifacts so
  the chapter covers another real scenario, transition invariant, negative
  case, bridge, or boundary; update chapter proof-limit prose and run the
  proof gate.
- `test-or-evidence`: run or import a public-safe test, measurement, replay, or
  digest-verifiable project artifact with baseline or negative controls where
  relevant; record residuals, non-claims, and any no-promotion decision.
- `external-grounding`: add source-noted external records through
  `sources/source_inventory.json` and `sources/source_notes/` before revising
  prose; regenerate generated appendices instead of hand-editing citations.
- `reader-craft`: revise live or curated reader prose only after claim,
  source, proof, and test boundaries are current; smooth merge scaffolds,
  sharpen Beyond-SOTA sections, write finished third-person conviction and
  stakes, and route optional first-person enrichment questions to the sidecar
  queue rather than leaving placeholders.
- `recorded-blocker`: when the honest closure requires unavailable source
  text, private project artifacts, external review, local hardware, or Corben
  authorial input, record the blocker with the exact missing condition and do
  not rewrite prose to hide the gap.

Future autonomous runs should select rows by the cheapest honest closure class,
not by chapter order. Prefer rows where an existing proof module, public-safe
Circle/Theseus/RankFold artifact, source note, or reader manuscript file can be
changed immediately. Leave rows open when only a new opinion, score, or
review paragraph would change.

Rows that already say "partially executed" still remain open until their
remaining work is closed by one of the gates above. Rows that appear "fine" or
"solid" still need preservation work when future edits touch them: keep the
source boundary crisp, prevent reader-version drift, and add blockers rather
than smoothing over unevidenced gaps.

Per-chapter burn-down:

| Chapter | Weakness to overcome | Required roadmap work |
|---|---|---|
| `asi-is-a-stack-not-a-model` | Beyond-SOTA previously restated the core thesis more than it argued against alternative framings, and opener traceability audits were still planned. | Partially executed: added live and curated reader mature-endpoint prose that contrasts the ASI Stack against scale-only systems, generic agent loops, and compound/modular AI systems, while preserving the source-noted comparator boundary for MRKL, LLM-agent surveys, cognitive architectures, and layered control. This pass added `python3 scripts/validate_stack_layer_traceability.py`, which checks the layer-boundary fixture, six assigned source mappings, Appendix A source-to-layer visibility, Appendix C claim/support labels, and no-promotion markers. Remaining work: implement contract-change triage and concrete integration-pressure traces before claiming that stack separation survives runtime, prototype, or multi-agent pressure. |
| `the-efficient-asi-hypothesis` | Previously had light anchoring to efficient-inference/routing literature and a generic "operating system" mature-endpoint opener. | Partially executed: live, curated reader, outline, source-inventory targets, and source notes now connect Efficient ASI to sparse/distributed MoE (`ext_sparse_moe_2017`, `ext_gshard_2020`, `ext_switch_transformer_2021`, `ext_expert_choice_routing_2022`, `ext_moe_llm_survey_2024`), query/learned routing (`ext_frugalgpt_2023`, `ext_hybrid_llm_2024`, `ext_routellm_2024`), prompt compression (`ext_longllmlingua_2023`), fast generation (`ext_speculative_decoding_2022`, `ext_multi_token_prediction_2024`, `ext_medusa_2024`, `ext_eagle_2024`), and benchmark pressure (`ext_bigbench_2022`), while the Beyond-SOTA endpoint now reads as a governed route economy. Added `python3 scripts/validate_efficiency_route_search_probe.py`, `docs/efficiency_route_search_probe.md`, `experiments/efficiency_route_search/results/2026-07-02-local.json`, and Lean bridge `lean:efficiency.route_search.probe_fixture_bridge` for 2 bounded synthetic route traces and 6 expected-invalid controls covering minimum verified route selection, hidden-cost class auditing, erased residual rejection, compression-utility overclaim rejection, authority-bypass rejection, and negative-control presence. This records no route-search completeness, cost-estimate accuracy, measured efficiency, model-quality, compression-utility, benchmark, or support-state claim. Remaining work: real route-search completeness evidence, calibrated cost estimates, measured route-quality evidence, benchmark performance, and downstream utility-preserving compression tests before stronger evidence claims. |
| `system-boundaries-and-authority` | Object-capability/confused-deputy lineage was not explicit enough despite strong authority proof coverage. | Partially executed: added source-noted external grounding through Saltzer-Schroeder protection principles, Levy capability-system boundaries, and Hardy's confused-deputy problem; live and curated reader prose now connect caller ceilings, delegation chains, expiry, and effect receipts to that lineage, and the runtime-adapter permission harness now adds expected-invalid ambient-authority confused-deputy and revoked-receipt probes. Added the authority revocation propagation trace, guarded by `python3 scripts/validate_authority_revocation_trace.py`, with result artifact `experiments/authority_revocation_trace/results/2026-07-03-local.json`, covering over-ceiling denial, revoked authority receipt blocking, expired approval no-mutation evidence, SCIF inactive approval blocking, reference-trace authority blockers, no support-state promotion, and no deployed revocation claim. Accepted no-promotion decision `evidence_transitions/v1_x_measured/authority_revocation_trace_no_change.json` now records that this cross-artifact trace blocks deployed authorization enforcement, live revocation propagation, runtime adapter enforcement, approval-service quality, sandbox isolation, tool-wrapper security, safety, and chapter-core promotion claims; it does not prove deployed revocation propagation. The 2026-07-03 pattern-language local-delta pass now adds live, curated reader, outline, and contribution-ledger alignment that names Authority as the can/may ceiling and durable denial/revocation owner. Remaining work: run deployed/live adapter denial traces, live/deployed revocation-propagation service behavior, and tool-wrapper security checks before stronger claims. |
| `failure-modes-of-ungoverned-intelligence` | Stack failure vocabulary is not mapped tightly enough to established AI-safety failure taxonomies. | Partially executed: added source-noted external grounding through `ext_concrete_ai_safety_2016`, `ext_goal_misgeneralization_2022`, `ext_learned_optimization_risks_2019`, `ext_optimal_policies_power_2019`, and `ext_goodhart_variants_2018`; the chapter now maps named stack failure modes to accident-risk, goal-misgeneralization, learned-optimization, power-seeking, and Goodhart/proxy-failure families without promoting support state. The Failure taxonomy detector and mitigation-boundary probe now adds a deterministic synthetic failure-taxonomy detector fixture, `python3 scripts/validate_failure_taxonomy_detector_probe.py`, with two valid synthetic failure incidents, seven expected-invalid controls, result artifact `experiments/failure_taxonomy_detector/results/2026-07-02-local.json`, Lean bridge `lean:failure.taxonomy.detector_probe_bridge`, and no support-state promotion. Remaining work: deployed detector traces, runtime authority/context/evaluator/claim-verifier behavior, real recurrence detection, mitigation-effectiveness evidence, prevention evidence, and external review before stronger detection or prevention claims; the detector probe remains synthetic-record and finite-Lean coverage only. |
| `evidence-states-and-claim-discipline` | The chapter undersells the novelty of support-state discipline. | Closed by artifact for the reviewer weakness in the 2026-07-03 burn-down reconciliation: live and curated reader prose now frame support-state discipline as the book's methodological claim-control contribution paired with Living Book Methodology, and the chapter/outline/source notes position it against source-noted model-card, datasheet, ML reproducibility-review, and proof-carrying-code comparators without support-state promotion. The Evidence bundle completeness and changelog-consistency probe adds a deterministic synthetic evidence-bundle fixture, `python3 scripts/validate_evidence_bundle_completeness_probe.py`, with two valid synthetic evidence bundles, seven expected-invalid controls, result artifact `experiments/evidence_bundle_completeness/results/2026-07-02-local.json`, Lean bridge `lean:evidence.bundle.completeness_probe_bridge`, and no support-state promotion. The Claim ledger completeness audit adds a real Appendix C audit, `python3 scripts/validate_claim_ledger_completeness_audit.py`, with 44 manifest chapter core claims, 44 Appendix C rows, seven expected-invalid mutation controls, result artifact `experiments/claim_ledger_completeness/results/2026-07-02-local.json`, Lean bridge `lean:evidence.claim_ledger.completeness_audit_bridge`, and no support-state promotion. The Accepted live transition review audit adds a real accepted-transition audit, `python3 scripts/validate_accepted_transition_review_audit.py`, with 44 accepted transition records, six bounded non-core upward transitions, no accepted upward chapter-core transition, the accepted no-promotion ledger, seven expected-invalid mutation controls, result artifact `experiments/accepted_transition_review/results/2026-07-02-local.json`, Lean bridge `lean:evidence.accepted_transition.review_audit_bridge`, and no support-state promotion. Reader-only overlays now replace the generated reader/Human-view field-list `Interfaces` and dense `Minimum Viable Implementation` harness inventory, moving the generated-reader heuristic row from medium to low priority, dropping dense-term hits from 123 to 95, and removing its one long paragraph while preserving the canonical AI/research record fields and audit details. The 2026-07-03 pattern-language local-delta pass now adds live, curated reader, outline, and contribution-ledger alignment that names Evidence States as the claim-movement owner. Follow-on stronger-evidence blockers are preserved outside this closed burn-down weakness: external review quality, claim truth, source interpretation adequacy, independent reviewer independence, and any new chapter-core support-state transition remain outside these audits. |
| `human-intent-as-a-formal-input` | Foundational chapter still needs planned behavioral tests and deeper external grounding; the prior `IntentContracts` proof-depth gap is closed at the finite-record level but not at deployed-intake level. | Partially executed: added intent-origin preservation checks to the synthetic plan-execution contract harness, now 3 valid and 10 expected-invalid fixtures after the field-confidence and inferred-authority expansion, including unresolved-ambiguity dispatch, unrejected-hidden-override, and authority-widening-from-intent probes; added expanded `AsiStackProofs.IntentContracts` admission-route coverage for hidden override rejection, unresolved ambiguity, constraint-precedence and preservation gaps, missing stop conditions, missing or widened authority, downstream re-contract triggers, missing non-claim boundaries, and complete admission; added `python3 scripts/validate_intent_intake_probe.py`, `docs/intent_intake_probe.md`, `experiments/intent_intake_probe/results/2026-07-02-local.json`, and Lean bridge `lean:intent.intake.probe_fixture_bridge` for a finite raw-request corpus with 4 valid bounded-request scenarios and 6 expected-invalid controls covering urgency, trust, vague broad-means requests, private-source publication pressure, declared stop conditions, and bounded-default non-authority; added the Intent re-contract trigger probe, guarded by `python3 scripts/validate_intent_recontract_probe.py`, with `valid_no_material_delta_continue`, `valid_publication_surface_delta_recontracts`, and seven expected-invalid controls for `invalid_authority_delta_without_recontract`, `invalid_private_source_delta_without_recontract`, `invalid_stop_condition_erasure_without_recontract`, `invalid_evidence_bar_weakening_without_recontract`, `invalid_affected_party_widening_without_recontract`, `invalid_means_expansion_without_recontract`, and `invalid_support_state_promotion_without_recontract`. This records no natural-language-intent-understanding, deployed-parser-quality, deployed-authority-extraction, prompt-injection-containment, runtime-dispatch, approval-service, user-satisfaction, or support-state-promotion claim. Remaining work: implement a real/deployed natural-language ambiguity parser, authority-extraction quality tests against broader corpora, end-to-end runtime stop-condition preservation, deployed prompt-injection containment, approval-service behavior checks, and deeper source-noted links to instruction-following, preference elicitation, and RLHF-intent literature before stronger evidence claims. |
| `constitutional-alignment-substrate` | Source lineage can read metaphysical if not labeled tightly. | Partially executed: added the Metaphysics lineage boundary audit, guarded by `python3 scripts/validate_alignment_metaphysics_boundary.py`, with result artifact `experiments/constitutional_alignment_metaphysics_boundary/results/2026-07-02-local.json`. The audit checks the live chapter, curated reader chapter, selected source notes, outline, roadmap, changelog, and manifest so metaphysical and consciousness language stays labeled as lineage, interpretation, speculation, or design rationale rather than becoming proof, enforcement authority, or support-state evidence. Remaining work: add deeper machine-ethics/value-alignment grounding only from source notes, external safety review, deployed predicate behavior, rights-usability tests, reviewer-quality evidence, and red-team traces before stronger claims; no support-state promotion. |
| `moral-uncertainty-and-value-conflict` | Value conflict needed a concrete rights-as-interface example rather than only abstract conflict vocabulary. | Partially executed: added the Contestability worked example fixture, guarded by `python3 scripts/validate_contestability_worked_example.py`, for `contestability://synthetic-care-memory-export-001`, a synthetic care-memory export scenario spanning value-conflict residuals, redacted audit packet, scoped exit path, safety-limited fork boundary, redaction appeal, replacement-preserved receipts, seven expected-invalid mutation controls, result record `experiments/contestability_worked_example/results/2026-07-02-local.json`, and Lean bridge `lean:values.conflict.contestability_example_bridge`. Live and curated reader prose now use the same care-memory export example to show how audit, exit, fork, and redaction appeal stay technical interfaces rather than moral settlement. Remaining work: deeper source-noted social-choice, preference-aggregation, and mechanism-design positioning; reviewer-quality evidence; real rights-interface usability; legal/institutional review; safe-fork review; deployed contestability traces; and any accepted evidence-transition review before stronger claims. |
| `stable-capability-fields` | Central primitive had narrower lifecycle proof coverage than its importance warrants. | Partially executed: added a finite SCF lifecycle state-machine proof lane for shadow/canary/qualified/default/deprecated/retired plus quarantine, including field-identity preservation, qualification evidence, regression-floor, authority-ceiling, rollback-readiness, deprecation-notice, and retirement-receipt negative cases. Added `python3 scripts/validate_scf_lifecycle_trace.py`, `docs/scf_lifecycle_trace_probe.md`, `experiments/scf_lifecycle_trace/results/2026-07-02-local.json`, and Lean bridge `lean:scf.lifecycle.trace_fixture_bridge` for a deterministic lifecycle trace with 2 valid traces and 6 expected-invalid controls covering forward lifecycle, incident quarantine, identity drift, default-without-regression, default authority expansion, retired restart, deprecation without notice, and retirement without receipt. This records no deployed route validation, evaluator-integrity measurement, real regression preservation, rollback execution, production lifecycle enforcement, or support-state promotion. Remaining work: deployed route validation, evaluator-integrity measurement, real regression preservation, terminal-state governance, lifecycle enforcement, and rollback execution. |
| `capability-replacement-and-rollback` | Deployment/MLOps prior art was lightly anchored and runtime replacement evidence remains missing; the prior `Replacement` proof-depth gap is closed at the finite-record level but not at deployed replacement level. | Partially executed: added source-noted external grounding through Argo Rollouts progressive delivery, Fowler/Hodgson feature toggles, Google Cloud MLOps continuous delivery, and Kubernetes Deployments rollout history/rollback; added synthetic capability-replacement fixtures for model-rollout data/schema/model/serving/monitor gates, baseline regression floors, monitor-trigger rollback conditions, and irreversible-effect ownership; added expanded `AsiStackProofs.Replacement` lifecycle-route coverage for identity mismatch, stale evidence, regression-floor failure, canary scope, failed canary, missing monitor window, monitor incident, rollback handle, rollback dry run, irreversible-effect ownership, residual owner, deprecation, retirement, non-claim boundaries, and complete default commit; added the Capability replacement trace probe, a deterministic replacement trace guarded by `python3 scripts/validate_capability_replacement_trace_probe.py`, with baseline implementation, non-default canary, two valid synthetic replacement transactions, three expected-invalid controls for authority widening, failed regression, and missing rollback, monitor-triggered rollback, rollback dry run, residuals, result record `experiments/capability_replacement_trace/results/2026-07-02-local.json`, and Lean bridge `lean:replacement.transaction.trace_probe_bridge`; added the Capability replacement identity sequence bridge in the same validator/result, with four rejected sequence controls and Lean bridge `lean:replacement.identity_sequence.invariant_bridge` for preserved field identity across canary/rollback, failed-monitor default blocking, prior implementation restoration, authority-envelope preservation, residual-owner preservation, no support-state effect, and non-claim boundary; added the Intent-governed replacement bridge, guarded by `python3 scripts/validate_intent_governed_replacement_bridge.py`, with result record `experiments/intent_governed_replacement_bridge/results/2026-07-02-local.json`, two valid synthetic bridge traces, six expected-invalid controls, and Lean bridge `lean:replacement.intent_governed.bridge` for command authority into replacement admission, default-without-approval blocking, authority-widening rejection, stop-condition-erasure rejection, rollback-owner requirement, and support-promotion overclaim. This records no deployed replacement behavior, no production rollback, no approval-service proof, no monitor-quality or regression-suite-quality result, and no support-state promotion. Remaining work: build any future deployed Argo/Kubernetes/ML pipeline prototype, live model-monitor trace, real regression suite, production rollback dry run, and externally reviewable replacement trace before claiming implementation. |
| `security-kernel-and-digital-scifs` | Planned prompt-injection containment and least-privilege tests remain high-value blockers. | Partially executed: expanded the synthetic security-kernel harness to 3 valid and 8 expected-invalid fixtures, adding expired-approval refusal and overbroad-SCIF-context rejection on top of existing prompt-injection, secret-visible-output, ambient-authority, missing-approval, missing-residual, and missing-zeroize negatives; added a Resource Budget Ledger expected-invalid fixture that rejects a critical dispatch whose apparent savings come from dropping SCIF isolation, approval, audit logging, and sanitization; added the SCIF sanitized commit replay probe, guarded by `python3 scripts/validate_security_scif_commit_probe.py`, with `valid_sanitized_commit_replay`, `valid_prompt_injection_blocked_commit`, and six expected-invalid controls for `invalid_unsanitized_secret_commit_blocked`, `invalid_handle_leak_commit_blocked`, `invalid_missing_zeroize_commit_blocked`, `invalid_overbroad_context_commit_blocked`, `invalid_unapproved_destination_commit_blocked`, and `invalid_missing_residual_commit_blocked`. This records no deployed-kernel, sandbox-isolation, side-channel-safety, prompt-injection-containment, secret-handle-safety, approval-service, least-privilege-context, privacy, security, or support-state-promotion claim. Accepted no-promotion decision `evidence_transitions/v1_x_measured/security_scif_commit_probe_no_change.json` now records that this probe blocks deployed-kernel, sandbox-isolation, side-channel-safety, prompt-injection-containment, secret-handle-safety, approval-service, least-privilege-context, privacy, security, and chapter-core promotion claims. Remaining work: add deployed/live kernel, sandbox, side-channel, approval-service, least-privilege context, real secret-handle, runtime prompt-injection containment, and runtime budget-enforcement evidence before stronger claims; keep SCIF wording grounded as compartment discipline rather than a deployed isolation guarantee. |
| `recursive-self-improvement-boundaries` | Some behavioral tests remained planned and external RSI/evaluator-capture anchoring can deepen. | Partially executed: upgraded `self_improvement_transition.schema.json`, `python3 scripts/validate_self_improvement_boundaries.py`, and the synthetic fixture set to require `boundary_delta_review`, `verification_budget_preservation`, and `gate_freshness`; the harness now passes with 3 valid and 10 expected-invalid fixtures, rejecting boundary-delta laundering, verification/security/rollback/human-review budget cuts, stale-gate promotion without rerun, sole-self-evaluation, authority widening, missing rollback, unreviewed canary, invariant weakening, and support-promotion overclaim. Updated the live and curated reader chapters, outline, manifest, and `docs/self_improvement_boundary_harness.md`; result record: `experiments/self_improvement_boundaries/results/2026-07-02-local.md`. Remaining work: deeper source-noted RSI, self-improvement, mesa-optimization, evaluator-capture, and STOP-adjacent literature; deployed protected-invariant behavior; live boundary-delta review; actual verification-budget preservation; fresh Theseus/current-readiness gate replay; live rollback; external safety review; and any accepted evidence-transition review before stronger claims. |
| `intent-to-execution-contracts` | Typed-workflow/API-contract anchoring was light and the "three lanes" merge scaffold was visible. | Partially executed: live mechanism prose and curated reader opening now describe one continuous command-contract flow from accepted intent receipt through field provenance, authority, handoff, dispatch, jobs, artifacts, verification, feedback, residuals, and non-claims; live, curated reader, outline, source-inventory targets, and source notes now connect the chapter to ReAct reasoning/action traces, PDDL planning-domain/problem notation, SHOP2 HTN decomposition, Temporal durable workflows, Airflow DAG orchestration, BPMN process notation, TLA+ high-level system modeling, and Dafny specification/verification-condition discipline. The Intent-to-execution handoff probe now adds a deterministic synthetic vertical handoff fixture, `python3 scripts/validate_intent_execution_handoff_probe.py`, with two valid synthetic handoff traces, seven expected-invalid controls, a result artifact at `experiments/intent_execution_handoff/results/2026-07-02-local.json`, and no support-state promotion. The Intent-governed replacement bridge now adds a downstream authority-consumer fixture, `python3 scripts/validate_intent_governed_replacement_bridge.py`, with two valid synthetic bridge traces, six expected-invalid controls, result artifact `experiments/intent_governed_replacement_bridge/results/2026-07-02-local.json`, and no parser, deployed dispatcher, approval-service, replacement-execution, rollback-execution, support-state-promotion, or evidence-transition claim. Remaining work: parser/dispatcher behavior tests, approval enforcement, semantic and authority-extraction quality tests, runtime side-effect enforcement, and live or externally replayed vertical traces before stronger command-contract claims; field-confidence audit, inferred-authority dispatch blocking, the handoff probe, and the replacement bridge remain synthetic-record and finite-Lean coverage only. |
| `planning-as-a-control-layer` | Central merged chapter has stronger plan-graph finite proof coverage, but planned behavioral tests and runtime traces remain missing. | Partially executed: added a finite plan-graph admission route in `AsiStackProofs.Planning` for command-contract acceptance, decomposition, acyclicity, dependency order, authority inheritance, context demand, adequacy contract, verification plan, dispatch gate, dispatch receipt, replanning controls, residual register, and non-claim boundary gaps. The Planning scheduler-state probe adds a deterministic synthetic scheduler-state fixture, `python3 scripts/validate_planning_scheduler_state_probe.py`, with two valid synthetic scheduler traces, seven expected-invalid controls, a result artifact at `experiments/planning_scheduler_state/results/2026-07-02-local.json`, a Lean bridge, and no support-state promotion. Accepted no-promotion decision `evidence_transitions/v1_x_measured/planning_scheduler_state_probe_no_change.json` now records that this scheduler-state fixture blocks deployed-planner, deployed-scheduler, decomposition-quality, context-demand-prediction, route-quality, selected-tier-adequacy, scheduler-optimality, runtime-replanning, live-feedback, benchmark, model-quality, safety, ASI, and chapter-core promotion claims. The Planning runtime-replan delta audit now adds a deterministic synthetic runtime-replan delta audit through `python3 scripts/validate_planning_runtime_replan_delta.py`, result artifact `experiments/planning_runtime_replan_delta/results/2026-07-02-local.json`, two valid synthetic runtime-replan traces, nine expected-invalid controls, and Lean bridge `lean:planning.runtime_replan.delta_audit_bridge` for authority preservation, stop-condition preservation, affected-subgraph scope, context/verification deltas, residual ownership, blocked-authority no-dispatch, support-effect none, and non-claim boundaries. Accepted no-promotion decision `evidence_transitions/v1_x_measured/planning_runtime_replan_delta_no_change.json` now records that this runtime-replan fixture blocks deployed-planner, runtime-scheduler, decomposition-quality, context-demand-prediction, route-quality, selected-tier-adequacy, scheduler-optimality, live-feedback, deployed-runtime-replanning, benchmark, model-quality, safety, ASI, and chapter-core promotion claims. Remaining work: implement decomposition-quality, context-demand prediction, selected-tier adequacy, route-quality, scheduler-optimality, deployed scheduler, live feedback handling, and deployed runtime-replanning tests with real or replayed traces before stronger claims; both Planning probes remain deterministic synthetic record and finite-Lean coverage only, with no support-state promotion. |
| `cognitive-compilation-and-semantic-ir` | Program-synthesis, IR, and translation-validation lineage needed clearer external grounding, and planned repair/audit tests needed an executable gate. | Partially executed: DreamCoder already grounds program-synthesis/library-learning vocabulary, and the previous pass added source-noted LLVM IR, MLIR, and translation-validation comparators; live/reader chapters and outline now tie the compiler analogy to typed IR, verifier boundaries, dialects, progressive lowering, lowering receipts, and per-translation source-target validation rather than metaphor alone. This pass added `python3 scripts/validate_cognitive_compilation_traces.py`, with 2 valid and 4 expected-invalid hand-authored source-plan/semantic-atom/lowering-receipt/target-audit/repair-trace fixtures for receipt representation, obligation preservation, localized repair scope, syntactic-pass laundering rejection, and no-promotion boundaries. Remaining work: implement a source-plan parser, concrete target artifact validators, real target-lowering behavior, localized-repair benchmark, direct-generation quality/cost comparison, LLVM/MLIR or translation-validation integration if warranted, and any accepted evidence transition before stronger compiler claims. |
| `virtual-context-abi` | Minor merge-scaffold residue around the "four lanes" framing, plus planned resolver/certificate fixture tests left in the outline. | Partially executed: live mechanism prose and curated reader opening now describe one continuous ABI flow from context request to materialization receipt, typed object, representation certificate, and fault/adequacy handoff; `docs/curated_reader_virtual_context_abi_prose_pass.md` records the meaning-preservation boundary. Added the VCM resolver/certificate probe, guarded by `python3 scripts/validate_vcm_resolver_certificate_probe.py`, with `valid_resolver_materialization_receipt`, `valid_mandatory_miss_typed_fault`, and nine expected-invalid controls for `invalid_address_mismatch_materialization_denied`, `invalid_version_mismatch_materialization_denied`, `invalid_snapshot_mismatch_materialization_denied`, `invalid_mount_policy_denied`, `invalid_lease_expired_reuse_blocked`, `invalid_certificate_source_binding_mismatch_denied`, `invalid_certificate_authority_escalation_denied`, `invalid_certificate_truthfulness_overclaim_denied`, and `invalid_summary_fidelity_omission_denied`. A reader-only overlay now replaces the retained `Representation examples` and `Interfaces` tables in Human view and generated reader output, dropping the generated-reader heuristic row from high to low while preserving the canonical AI/research tables. Remaining work: deployed resolver conformance, live memory-store behavior, broader summary-fidelity evaluation, open-domain certificate truthfulness, transaction/deletion enforcement, model-facing context quality, VCM-Bench or comparable benchmark evidence, leak-prevention tests, and preservation of ABI/certificate/refusal boundaries. Current probe is a no deployed-resolver, memory-store, context-compiler, open-domain-summary-fidelity, certificate-truthfulness, transaction-isolation, deletion-enforcement, model-facing-context-quality, VCM-Bench, leak-prevention, or support-state-promotion claim. |
| `context-transactions-snapshots-mounts-and-taint` | Rich formal mechanism had narrow proof coverage for snapshot, branch, mount, taint, and deletion boundaries. | Partially executed: added a finite transaction-route review model with derived theorems for missing/stale snapshots, branch leaks, unrepaired mount faults, taint without declassification, deleted-cell materialization without closure, invisible committed reads, missing replay boundaries, unsupported support promotion, missing non-claim boundaries, and complete committed-read admission. Added the bounded context-transaction sequence bridge, guarded by `python3 scripts/validate_context_transaction_sequence_bridge.py`, with 2 valid ordered sequence fixtures, 4 expected-invalid controls, read-after-write checks, replay-boundary checks, taint-blocking checks, invalid-control rejection, result artifact `experiments/context_transaction_sequence_bridge/results/2026-07-04-local.md`, and Lean bridge `lean:vcm.transactions.sequence_fixture_bridge` for sequence-summary alignment and no chapter-core support promotion. A reader-only overlay now replaces the generated reader/Human-view `Minimum Viable Implementation` transaction-field and route-review inventory, removing the generated-reader long paragraph while preserving the canonical AI/research fixture, Lean route model, synthetic memory-store rehearsal, sequence bridge, and non-claim boundaries. Remaining work: live or externally replayable transactional memory traces, runtime branch isolation, mount visibility, deployed deletion closure, declassification-quality review, replay service behavior, poisoning resistance, VCM conformance, and benchmark evidence. |
| `verification-bandwidth-and-context-adequacy` | Strong idea could carry empirical adequacy tests and sharper framing. | Partially executed: added the Verification bandwidth contradiction probe, a deterministic synthetic contradiction and adequacy fixture guarded by `python3 scripts/validate_verification_bandwidth_probe.py`, with result artifact `experiments/verification_bandwidth/results/2026-07-02-local.json`, two valid synthetic adequacy traces, seven expected-invalid controls, a Lean bridge at `lean:verification_bandwidth.contradiction_probe_fixture_bridge`, and no support-state promotion. This sharpens "long-context theater" into a concrete record boundary for summary-derived promotion, dominant-distractor misses, high-risk inadequate context, schema-mode empirical overclaiming, ignored negative evidence, unidentified semantic units, and fixture-driven support promotion. Added the Verification bandwidth capacity model, a deterministic synthetic record-level model guarded by `python3 scripts/validate_verification_bandwidth_capacity_model.py`, with result artifact `experiments/verification_bandwidth_capacity/results/2026-07-03-local.json`, three valid capacity traces, five expected-invalid controls, a 12-unit all-pairwise case with 66 modeled obligations, 18 checked obligations, and 48 residual obligations, a named-decomposition trace with 24 modeled obligations, and Lean bridge theorem `verification_bandwidth_capacity_model_fixture_bridge`. This records no support-state promotion and no model-verification-bandwidth law, contradiction-rate-performance, adequacy-classifier, deployed-long-context-failure, or evidence-transition claim. Remaining work: real contradiction-rate measurement, distractor-resistance benchmark, adequacy-classifier validation, deployed claim-ledger or escalation traces, and external review before stronger evidence claims. |
| `claim-ledgers-and-belief-revision` | Belief-revision lineage was lightly anchored. | Partially executed: added source-noted AGM belief revision, Doyle-style truth maintenance, and de Kleer-style assumption-based truth-maintenance comparators, alongside the existing ALCE, Self-RAG, and CheckList sources; live and curated reader prose now position claim-ledger revision as a bridge from formal belief change and maintained reasons to publication support states, surface synchronization, contradiction links, revision history, and release gates. This pass expanded `python3 scripts/validate_claim_ledger_revision.py` to 5 valid fixture(s) and 7 expected-invalid fixture(s), with semantic-variant merge boundaries, assumption-context dependency preservation, broader-variant laundering rejection, contested-assumption erasure rejection, unsynchronized variant-surface rejection, result record `experiments/claim_ledger_revision/results/2026-07-02-local.md`, and Lean bridge `lean:claims.ledger.semantic_assumption_fixture_bridge`. This records no semantic-equivalence proof, assumption-context completeness proof, open-domain claim extraction, contradiction-quality result, deployed belief-engine behavior, or support-state promotion. The 2026-07-03 pattern-language local-delta pass now adds live, curated reader, outline, and contribution-ledger alignment that names Claim Ledgers as the belief-state continuity owner rather than a restatement of Evidence States. Remaining work: implement open-domain claim extraction, contradiction-quality tests, semantic-equivalence-quality review, assumption-context-completeness review, and a deployed or replayed belief-revision engine before stronger evidence claims. |
| `spinoza-verification-and-proof-carrying-claims` | Proof-carrying, autoformalization, LLM-judge, debate, and historical "Spinoza" naming needed outside-reader grounding. | Partially executed: added source-noted autoformalization, AI safety debate, and LLM-as-judge comparators alongside existing proof-carrying-code, Lean, and contestable-AI sources; live and curated reader prose now separate proof artifacts, informal-to-formal interpretation risk, adversarial review, model-graded review, judge bias/calibration, contestability, and no-promotion boundaries, and the visible chapter title already uses `Proof-Carrying Claims and Adversarial Review` rather than foregrounding `Spinoza`. The Adversarial review dossier and verdict-quality probe now adds a deterministic synthetic review-dossier fixture, `python3 scripts/validate_adversarial_review_dossier_probe.py`, with two valid synthetic review dossiers, seven expected-invalid controls, result artifact `experiments/adversarial_review_dossier/results/2026-07-02-local.json`, Lean bridge `lean:spinoza.adversarial_review.dossier_probe_bridge`, and no support-state promotion. A reader-only overlay now replaces the retained `Interfaces` field table in Human view and generated reader output, dropping the final high-priority generated-reader heuristic row to medium while preserving the canonical AI/research table and support boundaries. Remaining work: real verifier-output tier assignment, semantic-equivalence checks, LLM-judge bias controls, debate/reviewer-independence measurements, adversarial-probe-quality tests, and real reproducible dossier/verdict-quality evidence before stronger claims; the dossier probe remains synthetic-record and finite-Lean coverage only. |
| `labor-os-and-typed-jobs` | Durable-execution/workflow-orchestration anchoring and planned tests need completion. | Partially executed: added source-noted external comparators for Temporal durable execution, Airflow DAG orchestration, BPMN process notation, and Kubernetes Jobs batch lifecycle; live/reader chapters and outline now distinguish durable workflow completion, DAG task runs, process notation, and batch-job terminal states from ASI Stack evidence-ready typed jobs. The Typed job delivery and evidence-readiness probe now adds a deterministic synthetic typed-job delivery fixture, `python3 scripts/validate_typed_job_delivery_probe.py`, with two valid synthetic typed-job traces, seven expected-invalid controls, result artifact `experiments/typed_job_delivery/results/2026-07-02-local.json`, Lean bridge `lean:jobs.lifecycle.delivery_probe_fixture_bridge`, and no support-state promotion. The Typed job durable lifecycle probe now adds a deterministic synthetic durable lifecycle fixture, `python3 scripts/validate_typed_job_durable_lifecycle_probe.py`, with two valid synthetic durable lifecycle traces, nine expected-invalid controls, result artifact `experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json`, Lean bridge `lean:jobs.lifecycle.durable_lifecycle_probe_bridge`, and no support-state promotion. Accepted no-promotion decision `evidence_transitions/v1_x_measured/typed_job_durable_lifecycle_probe_no_change.json` now records that this durable lifecycle fixture blocks deployed scheduler, durable workflow recovery, permission-enforcement, approval-service, adapter-runner, completion-receipt service, replay-engine, workflow-trace, benchmark, model-quality, safety, ASI, and chapter-core promotion claims. Remaining work: deployed lifecycle checker, tool-permission enforcement service, approval service, adapter runner, completion-receipt service, replay engine, durable workflow recovery, deployed scheduler, live or externally replayed workflow traces, and broader runtime evidence before claiming a working Labor OS runtime or stronger support state. |
| `artifact-graphs-audit-logs-and-replay` | Provenance/replay proof coverage was narrow; finite route and replay-packet coverage is now broader than the deployed evidence. | Partially executed: added provenance closure, replay-grade sufficiency, claim/test-link integrity, stale-certificate, non-claim, blocked-promotion, complete-admission route theorems, and a replay-packet bridge for parent-job mismatch, missing audit chain, byte-exact missing observation, stale certificate, support-review transaction validation, partial-replay promotion blocking, record-only partial replay, and complete bounded-review cases. The receipt-faithfulness fixture added a finite record-reality negative-control lane; the receipt repository audit now adds `python3 scripts/validate_receipt_repository_audit.py`, `experiments/receipt_repository_audit/results/2026-07-03-local.json`, and Lean bridge `lean:artifacts.graph.receipt_repository_audit_fixture_bridge` for four selected repository receipt surfaces, tracked digest integrity, command pass records, Circle external rope receipt fingerprints, non-claim boundaries, and five expected-invalid controls covering missing artifacts, stale digests, failed commands, missing non-claims, and support-promotion overclaims; the receipt repository challenge now adds `python3 scripts/validate_receipt_repository_challenge.py`, `experiments/receipt_repository_audit/results/2026-07-04-challenge.json`, and Lean bridge `lean:artifacts.graph.receipt_repository_challenge_fixture_bridge` for a deterministic challenge with three tracked-digest challenges, one Circle external fingerprint challenge, and five expected-invalid controls covering digest mismatch, missing artifact, external fingerprint mismatch, missing non-claims, and support-promotion overclaim; the live artifact attestation probe now adds `python3 scripts/validate_artifact_live_attestation_probe.py`, `experiments/artifact_live_attestation/results/2026-07-04-local.json`, no-change decision `evidence_transitions/v1_x_measured/artifact_live_attestation_no_change.json`, and Lean bridge `lean:artifacts.graph.live_attestation_probe_bridge` as a local live repository attestation for one current produced artifact checked through filesystem bytes, git object bytes, command replay, independent observer routes, a trap receipt, attestation limits, no upward transition, and seven mutation controls; the randomized artifact attestation audit now adds `python3 scripts/validate_artifact_randomized_attestation_audit.py`, `experiments/artifact_randomized_attestation/results/2026-07-04-local.json`, no-change decision `evidence_transitions/v1_x_measured/artifact_randomized_attestation_no_change.json`, and Lean bridge `lean:artifacts.graph.randomized_attestation_audit_bridge` for a deterministic pseudo-random sample of four public-safe repository artifacts checked through filesystem bytes, git object bytes, command replay, trap receipts, attestation limits, and eight mutation controls; the record-reality sequence bridge now adds `python3 scripts/validate_artifact_graph_record_reality_sequence.py`, `experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json`, accepted no-promotion decision `evidence_transitions/v1_x_measured/artifact_record_reality_sequence_no_change.json`, and Lean bridge `lean:artifacts.graph.record_reality_sequence_bridge` for one valid stale/partial/fresh replay sequence and four expected-invalid controls covering stale-certificate promotion, restoration without fresh replay, missing non-claims, support-review without replay-validated transaction, fresh-replay restoration after blocked eligibility, no support-state effect, no upward support-state transition, and no chapter-core support effect; and the epistemic trusted computing base fixture now adds `python3 scripts/validate_epistemic_trusted_computing_base.py`, `experiments/epistemic_tcb/results/2026-07-03-local.json`, accepted no-promotion decision `evidence_transitions/v1_x_measured/artifact_epistemic_tcb_fixture_no_change.json`, and Lean bridge `lean:artifacts.graph.epistemic_tcb_fixture_bridge` for three bounded trust-base records and six expected-invalid controls covering missing root of trust, verifier-trust laundering, unbounded trust propagation, missing recursion stop, erased outside-TCB residuals, support promotion from trust-base shape, no upward support-state transition, and no chapter-core support effect. Accepted no-promotion decisions now cover the record-reality sequence bridge, epistemic-TCB fixture, live artifact attestation probe, and randomized artifact attestation audit. A reader-only overlay now replaces the generated reader/Human-view `Minimum Viable Implementation` harness inventory, moving the generated-reader heuristic row from medium to low priority, dropping dense-term hits from 50 to 48, and removing its one long paragraph while preserving the canonical AI/research proof, harness, replay, and non-claim details. The 2026-07-03 pattern-language local-delta pass now adds live, curated reader, outline, and contribution-ledger alignment that names Artifact Graphs as the record-reality and replay-grade owner. Remaining work: pursue richer produced-artifact traces, deployed artifact graph service behavior, real replay, audit reconstruction, provenance-completeness checking, deployed or externally reviewable attestation/audit behavior, live/external trust-base storage/replay, verifier-quality evidence, external/randomized challenges outside this repository, and audit-log durability before stronger claims. |
| `runtime-adapters-tool-permissions-and-human-approval` | Safety-critical action boundary had too few adversarial proof scenarios relative to its role as the external-effect boundary. | Partially executed: added a finite runtime-adapter route model for scoped approval, effect-lease scope/expiry/sandbox, parent and lease authority ceilings, confused-deputy rejection, sandbox-escape rejection, rollback-handle requests, effect-receipt/audit/non-claim blockers, and complete low-impact dispatch; expanded the runtime-adapter permission harness to 2 valid and 7 expected-invalid fixtures with harness-only authority probes for ambient-authority confused-deputy attempts and revoked authority receipts. Added the Runtime adapter effect replay probe, guarded by `python3 scripts/validate_runtime_adapter_effect_probe.py`, with result record `experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json`: `valid_low_impact_local_write_effect_replay` dispatches one generated public-safe temp-file write outside the repository, records pre/post/rollback hashes, verifies rollback-exact restoration, and rejects `invalid_missing_permission_no_mutation` plus `invalid_expired_approval_no_mutation` before mutation with `support_state_effect=none`. Accepted no-promotion decision `evidence_transitions/v1_x_measured/runtime_adapter_effect_probe_no_change.json` now records that this effect replay blocks deployed adapter, sandbox, approval-service, secret-handle, revocation, policy-enforcement, rollback-service, benchmark, runtime-security, model-behavior, and chapter-core promotion claims. Added Lean bridge `lean:runtime.adapters.effect_replay_fixture_bridge` for finite replay routing over missing permission, expired approval, missing no-mutation evidence, inexact rollback, missing receipts, repository/network side effects, support-state effects, and complete rollback-exact public-safe replay acceptance. Added the Runtime adapter adversarial boundary probe, guarded by `python3 scripts/validate_runtime_adapter_adversarial_boundary_probe.py`, with result record `experiments/runtime_adapter_adversarial_boundary/results/2026-07-02-local.json`: two valid synthetic adapter boundary reviews and twelve expected-invalid controls for confused-deputy parent mismatch, parent authority ceiling overrun, lease authority ceiling overrun, approval scope mismatch, expired approval, sandbox escape path, secret materialized into model-visible context, missing rollback handle, missing effect receipt, missing audit refs, support-state promotion, and missing non-claim boundary. Accepted no-promotion decision `evidence_transitions/v1_x_measured/runtime_adapter_adversarial_boundary_no_change.json` now records that this adversarial boundary fixture blocks deployed adapter, sandbox, approval-service, secret-handle, policy-enforcement, rollback-service, revocation-propagation, security-review, benchmark, runtime-security, and chapter-core promotion claims. Added Lean bridge `lean:runtime.adapters.adversarial_boundary_probe_bridge` for deterministic synthetic runtime-adapter adversarial boundary fixture coverage with no support-state promotion. Added Lean bridge `lean:runtime.adapters.revocation_route_bridge` for finite revocation routing: revoked approvals, revoked leases, and revoked authority receipts route away from dispatch only when denial-before-mutation and unchanged-state evidence exist, and otherwise request no-mutation evidence; complete non-revoked records preserve receipt, audit, support-state, and non-claim boundaries. Added the Human oversight degradation fixture, guarded by `python3 scripts/validate_human_oversight_degradation.py`, with result record `experiments/human_oversight_degradation/results/2026-07-03-local.json`: three valid finite records and seven expected-invalid controls for approval fatigue, rubber-stamping, alarm fatigue, automation bias, missing reviewer qualification, support-state promotion from approval shape, and missing non-claim boundaries. Added accepted no-promotion decision `evidence_transitions/v1_x_measured/human_oversight_degradation_no_change.json`, which blocks approval-workflow, reviewer-correctness, alert-quality, deployed-human-factors, runtime-adapter-safety, and chapter-core promotion claims while preserving `argument` support. Added Lean bridge `lean:runtime.adapters.human_oversight_degradation_fixture_bridge` and four source-noted human-factors comparators while preserving the no approval-service-quality, reviewer-correctness, alert-quality, deployed-human-factors, support-state-promotion, and chapter-core-support boundary. Reconciled the cross-boundary partitioned-authority fixture into this row: `python3 scripts/validate_partitioned_authority_fixture.py` records `experiments/partitioned_authority/results/2026-07-03-local.json` with three valid finite records and six expected-invalid controls for stale grants, revocation-delay quarantine, fresh authority receipt requirements, grant/effect race residual ownership, no-mutation evidence, CAP-style authority consistency boundaries, support-state non-promotion, and no deployed partition tolerance, distributed consensus, availability, runtime-adapter enforcement, or revocation-propagation claim. Accepted no-promotion decision `evidence_transitions/v1_x_measured/partitioned_authority_fixture_no_change.json` now records that this partitioned-authority fixture blocks deployed partition-tolerance, distributed-consensus, availability, runtime-adapter-enforcement, revocation-propagation, hive-scheduler, rented-node-sandbox, family-governance, network-overlay, security, privacy, benchmark, and chapter-core promotion claims. A reader-only overlay now replaces the generated reader/Human-view `Minimum Viable Implementation` harness inventory, moving the generated-reader heuristic row from medium to low priority, dropping dense-term hits from 71 to 49, and removing its one long paragraph while preserving the canonical AI/research proof, harness, effect-replay, adversarial-boundary, and non-claim details. The 2026-07-03 pattern-language local-delta pass now adds live, curated reader, outline, and contribution-ledger alignment that names Runtime Adapters as the external-effect lease owner. Remaining work: executable/live deployed adapter harness, real sandbox isolation, approval-service behavior, reviewer-quality evidence, reviewer-rotation traces, alert-quality evidence, privacy-reviewed workflow traces, secret-handle safety, rollback execution in target services, deployed revocation propagation, live partitioned-authority grant/revocation traces, live effect-receipt validation, real policy-enforcement checks, security review, and broader harness parity. |
| `procedural-memory-and-cognitive-loop-closure` | Narrow proof coverage and external tool-synthesis/skill-library anchoring are partially addressed; deployed loop evidence remains missing. | Partially executed: added promotion-gating, regression-preservation, lifecycle-route, and synthetic-fixture bridge theorems for routable, quarantined, and retired procedure states; added source-noted MemGPT, Toolformer, Voyager, and DreamCoder comparators for memory tiers, learned API/tool use, executable-code skill libraries, and program-synthesis library learning. Remaining work: build deployed or replayed loop-detection, tool-synthesis, generated-tool correctness, routing-monitor, regression-quality, and retirement-automation evidence before stronger claims. |
| `routing-heads-and-specialist-cores` | Strong chapter with remaining planned tests. | Partially executed: the synthetic routing decision lease harness is guarded by `python3 scripts/validate_routing_decision_lease.py`, records `experiments/routing_decision_lease/results/2026-07-01-local.md`, and checks 3 valid plus 7 expected-invalid route packets for least-capable adequate selection, overprivileged rejection, selected-route authority-envelope containment, missing-readiness fallback, expired-lease residualization, selected-specialist registration, rejected-candidate evidence, residual ownership, MoECOT source-boundary non-claims, and an authority-widening grant rejected because `granted_authority_subset` exceeds the selected specialist registry envelope. Accepted no-promotion decision `evidence_transitions/v1_x_measured/routing_decision_lease_no_change.json` now records that this harness blocks learned-router, route-quality, deployed authority-enforcement, specialist-quality, MoECOT replay, orchestration benchmark, and chapter-core promotion claims. The proof lane names `lean:routing.specialists.decision_lifecycle_route` in `AsiStackProofs.Routing` for finite routing-decision lifecycle outcomes only. Remaining work: real routing tasks, learned-router or policy-router code, route-quality measurement, imported MoECOT replay packets, orchestration benchmarks, and deployed authority enforcement; avoid turning route-quality fixtures into learned-router, route-quality, MoECOT replay, benchmark, or support-state claims. |
| `readiness-gates-residual-escrow-and-quarantine` | Lifecycle control plane deserved broader transition proof coverage. | Partially executed: added a finite readiness lifecycle-transition relation for candidate, shadow, canary, qualified, default-ready, quarantined, retired, and superseded records, with hard requirements for evidence freshness, residual escrow, fallback, expiry, regression floor, authority scope, route permission, supersession record, and retirement receipt. Added the Readiness lifecycle probe, a deterministic synthetic readiness lifecycle fixture guarded by `python3 scripts/validate_readiness_lifecycle_probe.py`, with six valid synthetic transitions, twelve expected-invalid controls, Lean bridge `lean:readiness.gates.lifecycle_probe_bridge`, no evidence transition, and no support-state promotion. Accepted no-promotion decision `evidence_transitions/v1_x_measured/readiness_lifecycle_probe_no_change.json` now records that this readiness lifecycle fixture blocks deployed readiness-engine, lifecycle-execution, residual-ledger-storage, live-quarantine-routing, gate-quality, terminal-governance, rollback-execution, runtime-monitoring, MoECOT-replay, benchmark, current-readiness, and chapter-core promotion claims. A reader-only overlay now replaces the generated reader/Human-view `Minimum Viable Implementation` harness inventory with reader prose about the readiness record, schema boundary, residual-gate harness, lifecycle probe, Lean finite predicates, and non-claim boundary; the readiness key-figure explanation is split into shorter reader paragraphs, moving the generated-reader heuristic row from medium to low priority and removing its remaining long paragraph without changing figure status or support boundaries. The 2026-07-03 pattern-language local-delta pass now adds live, curated reader, outline, and contribution-ledger alignment that names Readiness as the routability owner. Remaining work: deployed lifecycle transition execution, residual-ledger storage, live quarantine routing, gate-quality checks, terminal-state governance, MoECOT replay, benchmark evidence, and current-readiness evidence before stronger claims. |
| `personal-compute-hives-and-federated-edge-intelligence` | Ambitious, sprawling chapter with many planned tests and formerly missing chapter-level Lean module mapping. | Partially executed: metadata mapping and proof-hook surfaces are fixed, and `python3 scripts/validate_hive_admission.py` now checks 2 valid and 8 expected-invalid synthetic hive admission fixtures for policy-first scheduling, data locality/rented-node denial, approval receipts, guardian portal routing, sandboxed federation lease boundaries, job bidding, energy/dropout residuals, audit evidence refs, and support-state non-promotion. Reconciled the partitioned-authority closure artifact into the Hives row: `python3 scripts/validate_partitioned_authority_fixture.py` records `experiments/partitioned_authority/results/2026-07-03-local.json` with three valid finite records and six expected-invalid controls for stale grants, revocation-delay quarantine, fresh authority receipt requirements, grant/effect race residual ownership, no-mutation evidence, CAP-style authority consistency boundaries, support-state non-promotion, and no deployed partition tolerance, distributed consensus, availability, runtime-adapter enforcement, or revocation-propagation claim; proof audit names `lean:personal_hives.partitioned_authority.fixture_bridge` in `AsiStackProofs.PersonalComputeHives`. Accepted no-promotion decision `evidence_transitions/v1_x_measured/partitioned_authority_fixture_no_change.json` now records that this finite hives/runtime fixture blocks deployed partition-tolerance, distributed-consensus, availability, runtime-adapter-enforcement, revocation-propagation, hive-scheduler, rented-node-sandbox, family-governance, network-overlay, security, privacy, benchmark, and chapter-core promotion claims. Remaining work: live scheduler/device-registry/network-overlay/approval-service/family-governance/rented-node-sandbox/federation/dropout-recovery/energy-measurement evidence, cross-router connectivity, portal continuity, live or externally reviewable partitioned-authority grant/revocation traces, and any privacy/security claims before stronger support. Keep speculative product vocabulary bounded to synthetic-record and finite-proof evidence until those blockers close. |
| `compact-generative-systems-and-residual-honesty` | Longest chapter has broader finite proof coverage after the compact-admission route, but many planned behavioral tests remain. | Partially executed: added finite residual/exactness negative cases plus a compact-admission route for source artifact, compression-boundary, residual, lossy-exactness, reconstruction-evidence, fallback, verifier-cost, semantic-provenance, hierarchy-migration, evidence-transition, non-claim-boundary, and complete-admission outcomes. The Compact GVR synthetic slice accepts one bounded compact receipt and rejects three GVR controls. The Residual honesty conservation fixture adds `python3 scripts/validate_residual_honesty_conservation.py`, result `experiments/residual_honesty_conservation/results/2026-07-03-local.json`, and Lean bridge `residual_honesty_conservation_fixture_bridge` for 3 valid synthetic residual records and 5 expected-invalid controls covering hidden, erased, unowned, support-promoting, and zero-residual-overclaim residual laundering. The real repository residual-ledger trace adds `python3 scripts/validate_residual_ledger_trace.py`, result `experiments/residual_ledger_trace/results/2026-07-03-local.json`, and Lean bridge `residual_ledger_trace_surface_bridge` over current Resource, Compact GVR, and Readiness artifacts. The bounded residual-ledger storage/replay fixture adds `python3 scripts/validate_residual_ledger_storage_replay.py`, result `experiments/residual_ledger_storage_replay/results/2026-07-04-local.json`, no-change decision `evidence_transitions/v1_x_measured/residual_ledger_storage_replay_no_change.json`, and Lean bridge `residual_ledger_storage_replay_bridge` for 4 append-only replay entries, owner handoff, discharge review, workload context, digest-chain construction, and 5 expected-invalid controls. Remaining work: live or externally reviewable residual-ledger storage/replay, tamper/adversarial replay behavior, fallback behavior, reconstruction-quality, repair-cost, bounded-search, semantic grounding, hierarchy-revision, representation-utility, consumer-policy, and downstream utility tests; import real compression/repair measurements only from inspected CGS/BBVCA/RankFold artifacts. Current fixtures do not prove all residuals are observable, prove safety, validate deployed residual-ledger behavior, prove live residual detection, or promote the chapter core claim. |
| `fast-generation-architectures` | Excellent external grounding and one public-safe Theseus generation-mode negative-promotion import, but public speed-quality tests are still planned. | Partially executed: added the Fast generation public-safe task bundle, guarded by `python3 scripts/validate_fast_generation_task_bundle.py`, with result `fast_generation_task_bundle_2026_07_02_local`. The bundle compares `route://autoregressive-reference`, `route://fast-template-verified`, and `route://latency-only-proxy` over four deterministic receipt tasks; the verified route passes 4/4 tasks at 264 deterministic cost units versus baseline 632, while the cheaper latency-only proxy is rejected at 176 cost units for verifier, fallback, residual, and support-state failures. Added accepted no-promotion decision `evidence_transitions/v1_x_measured/fast_generation_task_bundle_no_change.json`, which blocks model-speed, useful-solution-per-second model performance, serving-throughput, route-selector adequacy, benchmark, model-quality, deployed-routing, and chapter-core promotion claims. Added Lean bridge `lean:fast_generation.task_bundle_fixture_bridge`. Added the bounded Theseus public task-bundle import, guarded by `python3 scripts/validate_theseus_public_task_bundle_import.py`, with 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 task-level regressions, 18 benchmark gates, 19 residuals, visible artifact gaps, and clean-live-replay non-claim boundaries; `evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json` now records the accepted no-promotion decision for that import. Added the selected Theseus/Fast support-lane aggregate, guarded by `python3 scripts/validate_theseus_fast_support_lane.py`, with result `theseus-fast-support-lane-2026-07-03-local`, 4 command replays, 16 tracked artifact digests, 68 public task records, 14 expected-invalid or rejected controls, 2 accepted no-promotion decisions, and Lean fixture `theseusFastSupportAggregateFixture`; it does not prove clean live Project Theseus replay, does not prove model quality, does not promote any chapter core claim, and does not create support-state promotion. Reader-only overlays now replace the generated reader/Human-view metric framing, taxonomy, and `Minimum Viable Implementation` harness inventory, moving the generated-reader heuristic row from medium to low priority, dropping dense-term hits from 41 to 36, and removing its one long paragraph while preserving the canonical AI/research formulas, comparison matrix, fixture counts, Theseus import boundary, task-bundle accounting, and non-claim details. This is no model-speed or deployment claim, no useful-solution-per-second model claim, no reproduced speculative decoding/MTP/diffusion/KV-cache/serving result, and no support-state promotion. Remaining work: real autoregressive/speculative/MTP/diffusion/hybrid/KV-cache benchmarks, actual route-selector behavior, clean Theseus replay or archived public task-bundle release fixture, verifier-quality evidence, fallback execution, serving-memory measurements, and accepted upward evidence-transition review before stronger claims. |
| `rankfold-neuralfold-and-artifact-compression` | Real compression implementation evidence is not surfaced enough. | Partially executed: added the RankFold public-safe replay probe (`python3 scripts/validate_rankfold_public_safe_probe.py`, `docs/rankfold_public_safe_probe.md`, and `experiments/rankfold_public_safe_probe/results/2026-07-02-local.json`) for a fresh local RankFold pack/verify/list/unpack replay over a generated 3,936-byte synthetic text fixture. The probe records `RAW0` / `Raw (stored)`, roundtrip-exact digest preservation, no compression advantage, a license-disabled NeuralFold boundary, and a rejected single-byte archive mutation. Also added a public-safe RankFold artifact import for three existing local `.rfa` archive observations over a 100,000,000-byte decoded artifact digest (`2b49720ec4d78c3c9fabaee6e4179a5e997302b3a70029f30f2d582218c024a8`), archive byte ratios up to 2.76634019 decoded/archive, `rfa verify` summaries of 1 OK, 0 failed, one unencrypted PACK0 stream, and `NEURAL0` inspect metadata, guarded by `python3 scripts/validate_rankfold_artifact_import.py`. Added explicit no-promotion decisions in `evidence_transitions/v1_x_measured/rankfold_public_safe_replay_probe_no_change.json` and `evidence_transitions/v1_x_measured/rankfold_artifact_import_no_change.json`; both remain `argument` and `blocks_promotion`. The artifact import does not prove RankFold codec correctness and does not promote the RankFold chapter core claim. A reader-only overlay now replaces the retained source-support table in Human view and generated reader output, dropping the generated-reader heuristic row from high to low while preserving the canonical AI/research table. These records do not prove NeuralFold compression, compression advantage, downstream utility, fallback execution, deployed compression behavior, or chapter-core support-state promotion. Remaining work: licensed/enabled NeuralFold or other real compression reproduction from source input, decoder-correctness proof beyond one tiny RAW0 roundtrip and recorded local decoded digest observations, fallback-execution evidence, downstream-utility probes, corpus/baseline benchmark review, and any support-state transition before stronger compression claims. |
| `resource-economics-and-token-budgets` | Proof coverage is modest for chapter weight and load-stability tests remain planned. | Partially executed: extended the capacity-smoothing harness to 3 valid and 6 expected-invalid toy traces for reviewer-capacity arithmetic, protected-review overhead, displaced-review-cost residualization, low-risk review hoarding, erased protected overhead, over-admission, overclaim, and support-state non-promotion; added a finite Lean bridge for the reviewer-capacity trace and three negative cases; extended the Resource workflow trace to 1 valid and 5 expected-invalid fixtures by adding an over-budget aggregate resource-bill control plus a matching Lean summary guard and result-control-name validation; extended the resource budget ledger harness to 6 valid and 7 expected-invalid fixtures with deterministic KV-cache/serving-memory accounting separation and throughput-to-quality overclaim rejection plus a finite Lean serving-memory guard; added a local five-sample measured workload-quality probe that selects a scoped workflow-trace validator over a broader Resource live-probe baseline by median elapsed time and rejects a cheaper no-op success-text negative control; added a local synthetic load-stability probe that selects protected capacity smoothing over an admit-arrivals baseline in a finite 10-task burst-review workload, residualizes 7 selected deferrals, rejects a cheaper review-erasure negative control, and checks a finite Lean fixture bridge; added accepted no-change/no-promotion records for the workflow-trace, local-replay, workload-quality, load-stability, and CI-cost sublanes; added a one-command aggregate flagship replay that reruns 10 Resource validators, checks 26 tracked artifact digests, composes 3 accepted non-core transitions with the chapter-core no-change decision and 5 sublane no-promotion records, and now checks `lean:resources.flagship.aggregate_invariant` / `resourceFlagshipLaneAggregateFixture` for matching aggregate counts, preserved negative controls, residuals, non-claims, and no-core-promotion/no-new-transition guards; added the bounded governance-tax trade-off model and `lean:resource.governance_tax.tradeoff_bridge` to price modeled risk, hidden verification/fallback cost, reviewer burden, residual discharge, protected-gate deletion rejection, and low-risk shortcut allowance without promotion. Remaining work: live or externally reviewable workload-quality review beyond the local repository task, production scheduler logs beyond CI metadata, measured displaced-cost accounting, live or externally reviewed load-stability workload, live or externally reviewable governance-tax workload evidence, physical-feasibility review, real KV-cache/serving-memory measurement, and measured simulation outputs before stronger claims. |
| `mathematical-and-search-substrates` | Umbrella chapter risks repeating Circle/coil specifics. | Partially executed: added the Substrate adoption trace, guarded by `python3 scripts/validate_substrate_adoption_trace.py`, with result `experiments/substrate_adoption_trace/results/2026-07-02-local.json`. The trace validates `valid_exploratory_registration`, `valid_structural_only_receipt`, `valid_consumer_axis_blocked`, and `valid_negative_control_retirement`, plus eight expected-invalid controls for missing baseline, missing falsification condition, theorem spillover into a route, unmeasured-axis routing, failed-control promotion, missing fallback, support-promotion overclaim, and missing non-claim boundary. Added Lean bridge `lean:substrates.search.adoption_trace_bridge` for finite trace-summary acceptance, axis-laundering rejection, failed-control/fallback/no-promotion boundary preservation, and non-claim alignment. This keeps the chapter focused on adoption discipline rather than Circle/coil performance: no substrate A/B test, representation-efficiency result, search-quality result, routing-quality result, compression-quality result, model-quality result, runtime result, Circle/CoilMoECOT/Mamba/TreeLLM/Theseus substrate-adoption validation, support-state transition, or chapter-core promotion exists. Remaining work: real baseline-symmetric substrate workloads, representation-efficiency benchmarks, cyclic/coil sidecar tests, sequence-substrate comparisons, transfer consumers, adoption-review records, and evidence-transition review before stronger claims. |
| `circle-calculus-and-proof-carrying-ai-contracts` | The chapter abstracts away from Circle's most concrete proved results. | Partially executed: the chapter now surfaces source-verified, public-safe Circle evidence for commit `63b0f511`, `CC-AI-CONTRACT-ROPE-001`, requested margin `1/328459`, `theorem_count 55`, ready digest `fields=31 missing=0 theorems=75`, the seven checked theorem IDs, fingerprints, the ASI consumer gate, and non-claims, guarded by `python3 scripts/validate_circle_concrete_evidence_surface.py`. `AsiStackProofs.ProofCarryingContracts` now adds `lean:circle_contracts.public_consumer_gate.fixture_bridge` for one valid receipt, four rejected mutation controls, seven required theorem IDs, pinned digest fields, blocked support movement, no chapter-core promotion, and no deployed-transport claim. Reader-only overlays now replace the dense `Concrete Circle Receipt Boundary`, proof-receipt lifecycle, `Interfaces`, and `Minimum Viable Implementation` reader/Human-view sections, dropping the generated-reader heuristic row from high to medium and the dense-hit count from 175 to 136 while preserving the canonical live evidence table, proof-contract field inventory, implementation details, and mechanism diagram in AI view. The 2026-07-04 reader follow-up aligns the curated reader manuscript, live Human-view overlay, companion note, reader manifest, reconciliation report, and review matrix with the public consumer-gate Lean fixture bridge without approving a reader release or changing support states. Remaining work: clean Circle replay from this repo, vendored or archived public contract pack, theorem-id resolution from local artifacts, and do not use trichotomy/undecided-interval language unless Circle artifacts explicitly verify that phrasing. |
| `coil-attention-cyclic-memory-and-recurrence-contracts` | Specialist chapter is sound but needed concrete Circle backing. | Partially executed: added the Circle cyclic-memory receipt slice for commit `63b0f511`, contract `CC-AI-CONTRACT-MEMORY-001`, kind `cyclic_memory_residue_winding`, theorem IDs `AIM-T0001`, `AIM-T0002`, `AIM-T0004`, `AIM-T0005`, recommendations `MEMORY-ATTACH-WINDING-ALIAS-PROVENANCE` and `MEMORY-AUDIT-FINITE-ALIAS-LOAD`, `same_residue_events=[7, 15, 23, 31]`, `same_residue_windings=[0, 1, 2, 3]`, `max_alias_load=4`, strict receipt fingerprint `a25d841aff585b59519919cad25d89a3f76cd8ddb11fb1549d593f7f2f09c62a`, Circle CLI output `3 passed in 2.51s`, and validator `python3 scripts/validate_circle_cyclic_memory_receipt_slice.py`. It does not promote any chapter core claim, does not create a support-state transition, and does not prove retrieval quality, task quality, model quality, context length, speed, memory scaling, deployment safety, transfer, or ASI. Remaining work: clean ASI-side Circle replay or archived public contract pack, KV-cache/sparse/recurrence receipt imports if needed, learned-memory workloads, retrieval-quality baselines, long-context benchmarks, transfer consumers, and any accepted evidence-transition review before stronger claims. |
| `coilra-multicoil-rope-and-cyclic-mixers` | Planned tests and exact-collision proof results need better surfacing. | Partially executed: the chapter now surfaces the recorded Circle RoPE receipt boundary as diagnostic structural evidence only, including `evidence.exact_discrete_pass=true` and `evidence.total_bank_collision_pair_count=0`, guarded by `python3 scripts/validate_circle_concrete_evidence_surface.py`. Remaining work: implement planned RoPE/cyclic-mixer tests and add baseline-symmetric workload evidence before any model-quality, context-length, runtime, memory, hardware, transfer, deployment, or support-state claim. |
| `executable-specifications-and-lean-proof-envelope` | Proof-governance chapter needed to show the book's real proof layer more concretely. | Partially executed: added Proof-depth surface synchronization guarded by `python3 scripts/validate_proof_depth_surface.py`; the live chapter, reader chapter, outline, and roadmap now expose the current validator-reported proof-depth snapshot. Current proof-depth snapshot: 201 proof targets, 54 Lean modules, 999 theorem declarations, 811 derived/decomposed, 184 direct/projection, 4 unknown/mixed, and 5/5 safety-critical chapter classifications present. The chapter explains derived/decomposed versus direct/projection labels and projection-only traceability, using the book's Lean layer as a worked proof-etiquette example. A reader-only overlay now replaces dense Interfaces and Minimum Viable Implementation proof-envelope inventory prose in Human view and generated reader output, dropping the generated-reader heuristic score from 9 to 7 while preserving the canonical AI/research details, rendered mechanism diagram, and support boundaries. The semantic proof adequacy review is now validator-checked by `python3 scripts/validate_proof_adequacy_review.py` against the 201-target manifest and no-promotion boundary language. This does not prove broad semantic adequacy, does not validate source interpretation, does not prove deployed enforcement, and does not promote proof-envelope support. Remaining work: upgrade high-value projection hooks where the proof model is too shallow and add consumer-gate receipts before stronger formal-methods claims. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | Proof coverage was narrow and Theseus benchmark practice is under-surfaced. | Partially executed: added the Benchmark anti-Goodhart fixture bridge, guarded by `python3 scripts/validate_benchmark_fixture_bridge.py`, with 2 valid fixtures, 5 expected-invalid controls, one promotion-ready synthetic path, one saturated-regression-floor path, result record `experiments/benchmark_antigoodhart/results/2026-07-02-fixture-bridge.json`, and `lean:benchmarks.ratchet.fixture_bridge` in `AsiStackProofs.BenchmarkRatchets`. This proves only finite synthetic fixture-summary alignment and no-support-promotion boundaries. Remaining work: ground public-calibration locks, honest weak scores, residual escrow, benchmark-state transitions, and source-reported or current Theseus benchmark practice in verified Theseus artifacts or an explicit replay/import blocker before stronger claims. |
| `policy-optimization-and-learning-from-feedback` | Planned optimizer/training tests remain, but the rollback-demo gap is now partially closed. | Partially executed: added the Policy update lease probe, a deterministic policy-update lease fixture guarded by `python3 scripts/validate_policy_update_lease_probe.py`, with six synthetic router-policy samples, five candidate policies, one source-grounded canary kept experimental, three expected-invalid controls for reward-only proxy, authority expansion, and missing rollback, holdout checks, contamination check, reward-hacking probes, unchanged authority, rollback dry run, residuals, result record `experiments/policy_update_lease/results/2026-07-02-local.json`, and Lean bridge `lean:policy_optimization.lease_probe_fixture_bridge`. This records no optimizer, no deployed canary, no live rollback, no route-quality or reward-quality result, and no support-state promotion. Remaining work: DPO/offline preference baseline, PPO or online RL baseline, GRPO/RLOO toy verifier reward, verifier reward-loop evidence, latency/reasoning-budget preservation study, router-policy or context-policy training/simulation beyond deterministic fixture, reward-quality studies, real holdout/contamination operations, deployed monitoring, and accepted evidence-transition review before stronger claims. |
| `artifact-steward-agents-and-living-project-governance` | Former chapter-level Lean module mapping bug hid a distinctive steward proof lane from the chapter metadata. | Partially executed: metadata mapping is fixed, the steward proof lane is surfaced as seven manifest/outline/chapter proof targets, and the Artifact steward lifecycle probe is recorded in `docs/artifact_steward_lifecycle_probe.md`, guarded by `python3 scripts/validate_artifact_steward_lifecycle_probe.py`, and summarized at `experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json`. It checks `valid_clean_release_review_proposal`, `valid_sunset_review_route`, and six expected-invalid controls for `invalid_tainted_event_without_review`, `invalid_over_policy_treasury_spend`, `invalid_contribution_governance_laundering`, `invalid_unscoped_federation_contract`, `invalid_release_without_gate_evidence`, and `invalid_sunset_criteria_ordinary_work`; proof targets in `AsiStackProofs.ArtifactStewardAgents` cover finite work-contract, treasury-boundary, release-gate, sunset-review, lifecycle-route, contribution-ledger, and federation-contract envelopes. Remaining work: polish the chapter around bounded continuity, federation, treasury, release gate, sunset, and stewardship evidence; add real executable event-taint workflow, treasury/governance engine, contribution-ledger service, federation harness, release runner, sunset protocol, and behavioral steward-loop tests before stronger claims. Current probe is a no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim; it also does not prove legal authority, treasury safety, governance correctness, capture resistance, release safety, federation safety, or project quality. |
| `integrated-reference-architecture` | Reads more like recap than showpiece. | Partially executed: live and curated reader prose now include the narrative showpiece trace, using the validated approved fixture to follow `intent://human-book-maintenance-request` through command contract, plan, context packet, bounded route, argument-only claim, fixture-only work order, audit log, record-shape evidence update, residual deltas, and `scf://no-promotion-review`, and using the blocked fixture to show denied runtime authority, blocked work, authority-denial audit, blocked-path evidence, stop conditions, and promotion blockers. The replay lane adds `python3 scripts/run_reference_trace_replay.py --write-result` and `python3 scripts/validate_reference_trace_replay.py`, producing `experiments/reference_trace/replay_results/2026-07-02-resource-flagship.json`: an actual local replay of `python3 scripts/validate_resource_flagship_lane.py` with output digest, tracked artifact bundle, Reference Trace Record, and blocked-authority stop-condition attachment. A reader-only overlay now replaces the dense showpiece-hop table in Human view and generated reader output, dropping the generated-reader heuristic row from high to medium while preserving the canonical AI/research table. Remaining work: produce a live or externally replayed runtime trace with real layer handoffs before claiming runtime integration, live artifact continuity, deployed authority-stop behavior, model quality, benchmark quality, scheduler behavior, economic outcomes, or support-state promotion. |
| `project-theseus-as-report-first-implementation-reference` | Described Theseus abstractly instead of showing its real public-safe substance. | Partially executed: the live and curated reader chapters now surface the public-safe architecture-gate import, generation-mode import, support replay probe, report-bundle audit, public task-bundle import, selected Theseus/Fast support-lane aggregate, `14/14` gate summary, `18` modes, `13` comparisons, zero hard gaps, zero promotable comparisons, useful-solution-per-second `0.0`, 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 task-level regressions, 18 benchmark gates, 19 residuals, digests, output digests, 7 expected-invalid bundle-audit controls, 7 expected-invalid public-task-bundle controls, 8 crosswalk rows, visible artifact gaps, support-state effect `none`, clean live Theseus replay remains unclaimed, and non-claims, guarded by `python3 scripts/validate_theseus_concrete_evidence_surface.py`, `python3 scripts/validate_theseus_report_bundle_audit.py`, `python3 scripts/validate_theseus_public_task_bundle_import.py`, and `python3 scripts/validate_theseus_fast_support_lane.py`. Added accepted no-promotion decision `evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json`, which blocks clean-live-replay, model-quality, benchmark-superiority, generation-speed, useful-solution-per-second, support-state, deployment, self-evolution, and chapter-core promotion claims. Added support aggregate result `theseus-fast-support-lane-2026-07-03-local`, which checks 4 command replays, 16 tracked artifact digests, 68 public task records, 14 expected-invalid or rejected controls, 2 accepted no-promotion decisions, and `theseusFastSupportAggregateFixture`; it does not prove clean live Project Theseus replay, does not prove model quality, does not promote any chapter core claim, and does not create support-state promotion. A reader-only overlay now replaces the dense Minimum Viable Implementation import inventory in Human view and generated reader output, dropping the generated-reader continuity row from medium to low while preserving the canonical AI/research evidence details and non-claims. Remaining work: clean live Theseus replay or archived public fixture, current work-board import, missing-artifact/publication-permission closure, and external review before any stronger support or deployed Theseus claim; the task-bundle import and support aggregate do not prove model quality. |
| `prototype-roadmap` | Solid roadmap chapter had a small planned-test tail around phase acceptance and dependency gates. | Partially executed: added the Prototype phase gate harness, guarded by `python3 scripts/validate_prototype_phase_gates.py`, with result `prototype_phase_gates_2026_07_02_local` at `experiments/prototype_phase_gates/results/2026-07-02-local.json`. The harness implements `Phase acceptance checklist` and `Dependency gate review` with 2 public-safe valid fixtures and 6 expected-invalid controls for phase acceptance, research-only phase debt, missing required artifacts, dependency inversion, self-improvement without an independent evaluator, support promotion without an evidence-transition record, phase debt without retirement, and missing non-claim boundaries. Added Lean bridge `lean:roadmap.phases.fixture_gate_bridge` for finite fixture-summary acceptance, missing-non-claim rejection, no support-state promotion, and no phase-completion claim. Remaining work: real phase execution packets, deployed build-controller behavior, benchmark evidence, full evidence-state audit over phase packets, external review, and any support-state transition before stronger roadmap claims. |
| `living-book-methodology` | The demonstrated living-book method is undersold. | Partially executed: live and curated reader prose now pair Living Book Methodology with Evidence States as the book's methodological contribution, emphasizing manifest-driven source of truth, source queues, claim/evidence ledgers, proof manifests, release records, reader-edition derivation, and non-claims; source notes and generated source ledgers now position the chapter against literate programming, Jupyter Book-style executable books, Quarto Books, governance lifecycle reporting, transparent evaluation, living benchmarks, and contamination warnings. Implement and preserve the explicit living-book change-packet record through `schemas/living_book_change_packet.schema.json`, `python3 scripts/validate_living_book_change_packets.py`, three valid synthetic packets, six expected-invalid controls, result record `experiments/living_book_change_packets/results/2026-07-02-local.md`, and Lean boundary `lean:living_book.methodology.change_packet_boundary`. Remaining work: use change packets on future substantive updates, seek external methodology review, and avoid treating packet validation as manuscript-quality, source-interpretation, release-approval, future-agent-correctness, or support-state evidence. |
| `open-research-agenda-and-bibliography-plan` | Backmatter role is appropriate, but source ownership must stay crisp. | Partially executed: live and curated reader prose now add a source-ownership closing rule that routes Corben-authored, Corben-supplied, recovered, and local-project material through Appendix G and source notes; outside literature through Appendix H and source notes; project artifacts through replay, digest, fixture, or blocker records; and claim-strength changes through Appendix C and evidence-transition decisions before prose changes. Remaining work: rehearse live new-paper intake against a real user-provided AI paper or artifact, normalize direct citations, reproduce/import benchmark or project artifacts where public-safe, and keep future-source triage from becoming a generic bibliography list. |

Acceptance bar:

- each row has either an executed commit, an explicit blocker, or an active
  issue/roadmap subtask before the next major release;
- `python3 scripts/validate_chapter_review_burndown.py` passes, proving only
  that every current manifest chapter has a calibrated roadmap row and that no
  row uses placeholder or stale chapter language;
- proof rows run `lake build`, `scripts/validate_proof_depth.py`, and relevant
  fixture validators;
- source rows add or update source notes before chapter prose uses the source;
- evidence-import rows include replay/digest, baseline or negative controls
  where relevant, residuals, and non-claims;
- reader/craft rows update the Human view/reader manuscript without fabricating
  Corben's first-person voice or support-state movement;
- no row is marked complete merely because the roadmap names it.

### Milestone 3 - Project Theseus Evidence Import

Goal: turn Project Theseus from a mined source family into a public-safe,
replayable implementation-evidence lane.

Tasks:

- Define `schemas/theseus_report.schema.json` for public-safe Theseus reports:
  report ID, source repo/ref, tool version, input class, generated artifact
  refs, gate decisions, failed attempts, residuals, redactions, replay command,
  and non-claims.
- Add public-safe fixtures under `experiments/theseus_import/`.
- Write `scripts/validate_theseus_report.py`.
- Select a first narrow trace, preferably one of:
  - plan compiler produces typed DAG plus rejected invalid DAG;
  - architecture gate blocks unsafe self-evolution;
  - operator OS records approval, receipt, and rollback handle;
  - Circle transfer lane emits a proof-contract receipt.
- Import only sanitized traces that can be committed publicly.
- Route the first accepted transition to a non-core claim before chapter-core
  promotion is considered.

Acceptance bar:

- a public-safe report fixture validates locally and in the full book gate;
- the report names a reproducible source commit, pinned public release, or
  archived fixture digest;
- CI either replays the fixture directly or verifies the pinned archived digest
  and expected public-safe result;
- at least one chapter source crosswalk can point to the report as implementation
  evidence without overclaiming;
- any support-state transition remains narrow and recorded.

Current status after the first two ASI-side Project Theseus imports:

- `schemas/theseus_report.schema.json` defines the public-safe Project Theseus
  report contract.
- `experiments/theseus_import/fixtures/valid/architecture_gate_public_report.valid.json`
  imports a sanitized static architecture-gate report summary from the local
  Project Theseus checkpoint at commit `1ad88a22`.
- The imported source artifact is pinned by SHA-256
  `7994e2909029644d6073289d8c9c59f774473f366a1c8cbda5943326f28518b2`, and
  the public ASI fixture is pinned by SHA-256
  `c33ea5d8d466e394ac556eebd623fb0eb43f601d79ea5f66021ec57762751923`.
- `scripts/validate_theseus_report.py` validates the report, verifies the
  digest boundary, requires `14/14` architecture gates, and rejects expected
  invalid mutations for digest mismatch, private-payload copying, and support
  promotion overclaim.
- `docs/theseus_report_import_slice.md` records the exact import boundary:
  useful as implementation-reference evidence, not a clean live Theseus rerun,
  not a support-state transition, and not a chapter-core promotion.
- `schemas/theseus_generation_mode_import.schema.json` defines the public-safe
  Project Theseus generation-mode gate import contract.
- `experiments/theseus_generation_mode_import/fixtures/valid/generation_mode_gate_public_summary.valid.json`
  imports a sanitized static generation-mode gate summary from the local
  Project Theseus checkout at commit `1ad88a22`.
- The imported generation-mode source report is pinned by SHA-256
  `a711d0dbca9779f26d4b0a63db18ce1fc574ade47a262f5140a9a7b6d325e90b`, and
  the public ASI fixture is pinned by SHA-256
  `0a101d427d51029ba7a0aaaaf4329cb47e96400cd21fc284123e366fb309d709`.
- `scripts/validate_theseus_generation_mode_import.py` validates the summary,
  requires 18 modes, 13 comparisons, zero hard gaps, zero modes with missing
  report refs, five hard boundary gates passing, zero promotable comparisons,
  zero useful-solution-per-second, and rejects expected-invalid mutations for
  hard boundary-gate failure, private-payload copying, missing-report-ref
  overclaim, support promotion overclaim, raw-speed promotion, and useful-speed
  overclaim.
- The same validator now checks a finite `AsiStackProofs.FastGeneration` Lean
  fixture bridge for the public summary fields and theorem names, including
  all-gates-passed and zero-missing-report-ref guards, so the imported
  no-promotion counts cannot drift from the book-side proof layer without
  failing validation.
- `docs/theseus_generation_mode_import_slice.md` records the exact import
  boundary: useful as implementation-reference and negative promotion evidence,
  not a clean live Theseus rerun, not a generation-speed result, not a
  support-state transition, and not a chapter-core promotion.
- `scripts/run_theseus_support_replay_probe.py --write-result` and
  `scripts/validate_theseus_support_replay_probe.py` now record and validate a
  local support replay probe over the two public-safe Project Theseus import
  validators, with command-output digests, elapsed records, tracked artifact
  hashes, and explicit no-transition boundaries.
- `docs/theseus_support_replay_probe.md` records the exact probe boundary:
  reproducibility and accounting over static imports only, not a clean live
  Theseus replay, not a public task-bundle run, not external review, not a
  generation-speed or useful-solution-per-second result, and not a
  support-state transition.
- `scripts/validate_theseus_report_bundle_audit.py` now validates a public-safe
  report-bundle audit fixture with 1 valid fixture, 7 expected-invalid controls,
  2 replay-ready rows, 1 blocked replay row, 8 crosswalk rows, 5 gate mappings,
  6 visible artifact gaps, and 6 intervention-ladder levels.
- `docs/theseus_report_bundle_audit.md` records the exact audit boundary:
  repository fixture discipline only, not a clean live Theseus replay, not an
  imported live report bundle, not a public task-bundle run, not a benchmark,
  not external review, and not a support-state transition.
- `docs/theseus_public_task_bundle_import.md` records the bounded public
  task-bundle summary import `theseus_public_task_bundle_import_2026_07_03_local`:
  64 public BigCodeBench metadata-only tasks, 0 public training rows, 0
  external inference calls, 0 task-level regressions, 18 benchmark gates, 19
  residuals, visible artifact gaps, seven expected-invalid controls, and a
  finite `AsiStackProofs.TheseusReference` bridge. Clean live Theseus replay
  remains unclaimed, and the import does not prove model quality, benchmark
  superiority, generation speed, useful-solution-per-second improvement, or
  support-state promotion.
- `docs/theseus_fast_support_lane_run.md` records the selected Theseus/Fast
  support-lane aggregate `theseus-fast-support-lane-2026-07-03-local`:
  `python3 scripts/validate_theseus_fast_support_lane.py` reruns the Theseus
  generation-mode import, Theseus support replay probe, Theseus public
  task-bundle import, and Fast Generation task-bundle validators, checks 16
  tracked artifact digests, 68 public task records, 14 expected-invalid or
  rejected controls, 2 accepted no-promotion decisions, and
  `theseusFastSupportAggregateFixture`, and preserves that the aggregate does
  not prove clean live Project Theseus replay, does not prove model quality,
  does not promote any chapter core claim, and does not create support-state
  promotion.
- The remaining stronger milestone work is a clean Project Theseus replay or
  archived public release fixture, current work-board import, missing-artifact
  and private/publication permission closure, external review, plus any
  separate accepted evidence-transition record if a bounded non-core claim is
  later promoted.

### Milestone 4 - Circle Public Replay And Consumer Gate

Goal: make the Circle evidence lane replayable from the ASI Stack repo or from
a stable public archive.

Tasks:

- Create a public Circle contract pack or fixture that includes only safe
  receipt inputs, theorem IDs, digest fields, and expected validation results.
- Decide whether the ASI repo vendors the pack, fetches a pinned public release,
  or records an archived artifact digest.
- Extend `scripts/validate_circle_external_receipt_slice.py` or add a new
  consumer-gate validator that checks the imported artifact against the ASI
  proof-contract expectations.
- Add negative controls: missing theorem ID, digest mismatch, stale contract,
  and unsupported transfer claim.
- Route any stronger transition through evidence-transition review.

Acceptance bar:

- the Circle lane is no longer only a local summary;
- CI either replays the public-safe Circle fixture directly or verifies a pinned
  archived artifact digest plus expected receipt result;
- ASI validation can reject malformed or overclaimed Circle receipts;
- chapter prose distinguishes proof-contract legality from model quality,
  context length, speed, memory scaling, or ASI capability.

Current status after the first ASI-side Circle consumer gate:

- `experiments/circle_public_replay/fixtures/valid/circle_rope_receipt.consumer.valid.json`
  records a public consumer-gate receipt fixture for
  `CC-AI-CONTRACT-ROPE-001`.
- The fixture is pinned by SHA-256
  `7b33bc7059fa8f6b2ed1282ca5b0c4ab7f6f5044c2f834d487bdefbce44969c6`.
- `scripts/validate_circle_public_replay.py` validates the receipt against
  `schemas/proof_contract_receipt_record.schema.json`, requires the seven
  recorded Circle theorem IDs, checks the pinned contract and receipt
  fingerprints, and rejects expected invalid mutations for digest mismatch,
  missing theorem ID, stale contract status, and unsupported transfer claim.
- `docs/circle_public_replay_consumer_gate.md` records the boundary: useful as
  an ASI-side proof-contract consumer gate, with
  `evidence_transitions/v1_x_measured/circle_public_consumer_gate_no_change.json`
  now recording an accepted `blocks_promotion` no-change decision; it is not an
  upward support-state transition, not a local Circle Lean rerun, not a vendored
  contract pack, and not a chapter-core promotion.
- The remaining stronger milestone work is a clean Circle replay, public
  contract pack, or archived public Circle artifact before model-quality,
  runtime, context-length, transfer, or deployment claims can be entertained.

### Milestone 5 - Flagship Measured Evidence Lane

Goal: move from internally validated record discipline to one reproducible
architecture-relevant result.

The full 44-row backlog lives in `docs/per_chapter_evidence_plan.md`. Treat that
file as a menu of possible lanes, not as a checklist to complete in one run.
The next cycle should execute one flagship measured lane first, with at most
two supporting lanes if they are direct dependencies. The rest stay `planned,
not executed` with no fixture built and no implied support-state movement.

Selection rule:

- prefer an efficiency, routing, compression, context, or proof-contract lane
  where a baseline and negative control can run locally;
- choose lanes where public-safe, reproducible, non-self-sourced or externally
  reviewable evidence is achievable now;
- prefer load-bearing chapters that constrain many later chapters;
- prefer lanes that can reject negative controls, not merely accept happy paths;
- prefer lanes that reduce self-sourcing by importing public Theseus/Circle
  artifacts, external review, or source-noted prior art;
- require every selected lane to name the strongest current proof/evidence path
  for its load-bearing claim: Lean theorem, Theseus replay/report, Circle
  receipt, external literature, external review, or explicit no-promotion
  blocker;
- do not execute a lane only because it appears early in manifest order.

Acceptance bar:

- `docs/per_chapter_evidence_plan.md` remains current with all 44 chapter lanes;
- the active v1.x cycle names one flagship lane, any direct supporting lanes,
  and explicitly leaves all others planned;
- the flagship lane records command/replay path, baseline, negative control,
  residuals, non-claims, and support-state effect;
- unexecuted lanes do not create fixtures, pass/fail claims, or support-state
  pressure.

Current status for the focused v1.x active evidence cycle:

- `docs/v1_x_active_evidence_cycle.md` now selects three chapter lanes:
  flagship `resource-economics-and-token-budgets` plus direct support lanes
  `project-theseus-as-report-first-implementation-reference` and
  `fast-generation-architectures`.
- The remaining forty-one manifest chapter lanes are explicitly planned-only
  for this cycle.
- `scripts/validate_v1_x_active_evidence_cycle.py` enforces the selected-lane
  set, checks that selected plus planned-only lanes cover all 44 manifest
  chapters exactly once, requires the one-flagship/two-support boundary, and
  preserves the no-chapter-core-promotion boundary.
- The Resource Economics costed-route lane now has a four-route one-command
  replay: an adequate overkill baseline remains eligible, the selected bounded
  route remains the lowest-cost eligible route, a cheaper failed-verification
  route is rejected, and a cheaper hidden-residual route is rejected despite
  surface verification passing. The same validator now checks the finite Lean
  fixture against the public JSON costs, selected route, negative controls, and
  eligibility fields, including the finite selector-state trace theorem
  `costed_route_fixture_trace_selects_lowest_eligible_route`. The trace proves
  the replay ends with the selected route after seeing two eligible routes and
  rejecting two cheaper controls. The tracked result now exposes the
  field-level Python/Lean alignment directly: constructors, route costs,
  verification/adequacy/promotion/dispatch/residual/fallback/non-claim
  booleans, eligibility decisions, and selector-trace expectations. This is the
  current flagship measured lane while preserving the non-core
  `synthetic-test-backed` scope and no chapter-core promotion.
- `docs/resource_workflow_trace.md` adds the next deterministic public trace
  for the same flagship lane: `python3 scripts/validate_resource_workflow_trace.py`
  checks 1 valid and 5 expected-invalid multi-step workflow fixtures for
  selected-route cost recomputation, high-risk-first scheduler ordering,
  protected review overhead, displaced-cost residual ownership,
  capacity-budget-overrun rejection, physical-feasibility overclaim rejection,
  and no-promotion boundaries. This
  validator also checks the public result against a finite
  `AsiStackProofs.ResourceEconomics` workflow-trace fixture, and the tracked
  result now exposes trace-property Python/Lean alignment fields and checked
  theorem names. The Lean fixture carries finite dispatch events whose costs,
  review minutes, and verification minutes roll up to the public summary, whose
  order keeps the protected high-risk release gate before lower-risk work, and
  whose selected events preserve protected-overhead, residual-ownership, and
  non-claim guard flags; the Python/Lean alignment now also carries the
  over-budget aggregate-resource-bill rejection. This still does not prove
  deployed scheduler behavior,
  model quality, TokenMana or PlanForge behavior, economic outcomes, simulator
  adequacy, or physical feasibility.
- `docs/resource_live_probe.md` adds a local command-replay probe for the
  flagship lane: `python3 scripts/run_resource_live_probe.py --write-result`
  records five Resource Economics validator replays with exit codes, elapsed
  milliseconds, command-output digests, and tracked artifact hashes, while
  `python3 scripts/validate_resource_live_probe.py` replays the commands and
  checks the no-transition boundary. This improves reproducibility and drift
  detection for the Resource Economics evidence surface, but it remains local
  repository evidence only: it is not a deployed scheduler log, live workload
  quality review, human-repair measurement, physical-feasibility review,
  simulator-adequacy result, or support-state transition.
- `docs/resource_workload_quality_probe.md` adds a local five-sample measured
  workload-quality route choice for the same lane:
  `python3 scripts/run_resource_workload_quality_probe.py --write-result`
  records an eligible broader Resource live-probe baseline, a selected scoped
  Resource workflow-trace validator, and a cheaper no-op success-text negative
  control. `python3 scripts/validate_resource_workload_quality_probe.py`
  replays the route commands, checks five-sample medians, output digests, and
  tracked artifacts, verifies that the selected route preserves the required
  quality surface for the scoped task, and rejects the cheaper no-op route. This
  is repeated local repository-task evidence only: it is not a stable-speedup result,
  deployed scheduler result, TokenMana or PlanForge result, model-quality
  result, economic outcome, physical-feasibility result, external review, or
  support-state transition.
- `docs/resource_load_stability_probe.md` adds a local synthetic load-stability
  workload probe for the same lane:
  `python3 scripts/run_resource_load_stability_probe.py --write-result`
  records a finite 10-task burst-review workload, an admit-arrivals baseline
  with 5 overload units, a selected protected capacity-smoothing route with
  0 overload units and 7 residualized deferrals, and a cheaper review-erasure
  negative control with 3 protected-review violations and hidden deferrals.
  `python3 scripts/validate_resource_load_stability_probe.py` recomputes the
  deterministic result, checks tracked artifact hashes, verifies the finite
  `AsiStackProofs.ResourceEconomics` fixture bridge, and enforces no-promotion
  boundaries. This is local synthetic workload evidence only: it is not a
  TokenMana result, PlanForge result, deployed scheduler result, production
  queue trace, real load-stability result, human-productivity result,
  economic outcome, external review, or support-state transition.
- `docs/resource_ci_cost_profile.md` adds a CI publication cost profile for
  the same lane: `python3 scripts/build_resource_ci_cost_profile.py --write-result`
  records eight actual GitHub Pages workflow runs, eight completed runs, five
  successful completed runs, three classified GitHub Pages deploy-service
  failures, a 131-second recovery boundary, finite Lean classifier alignment,
  and publication-duration metrics, while
  `python3 scripts/validate_resource_ci_cost_profile.py` validates the recorded
  timestamps, durations, failure classification, repair boundary, source
  commands, and non-claims offline. This is real publication-pipeline metadata,
  but it remains a repository operations trace: it does not prove deployed
  resource scheduling, workload quality, model quality, economic outcomes,
  physical feasibility, simulator adequacy, or support-state movement.
- `docs/resource_flagship_lane_run.md` adds a one-command aggregate replay for
  the same flagship lane: `python3 scripts/run_resource_flagship_lane.py --write-result`
  runs the costed-route, workflow-trace, budget-ledger, capacity-smoothing,
  live-probe, workload-quality, load-stability, CI-cost, simulation-transfer,
  and evidence-transition validators, records command-output digests and 26
  tracked artifact hashes in
  `experiments/resource_flagship_lane/results/2026-07-01-local.json`, and
  `python3 scripts/validate_resource_flagship_lane.py` replays the validators
  before accepting the record. The result now also carries aggregate
  Python/Lean alignment through `lean:resources.flagship.aggregate_invariant`
  and `resourceFlagshipLaneAggregateFixture`: 10 command replays, 26 tracked
  artifacts, 3 accepted narrow transitions, 5 no-promotion decisions,
  preserved negative controls, residuals, non-claims, and no-core-promotion/
  no-new-transition guards. This is an aggregate local replay gate, not a new
  measured lane, support-state transition, external review, deployed scheduler
  result, production workload, artifact approval, model-quality result, or
  economic outcome.
- The simulation-transfer boundary harness remains folded into Resource
  Economics as a support boundary: it rejects missing fidelity, unbounded world
  transfer, missing resource bills, missing bottleneck residuals, ignored
  instrumentation, and support-state promotion, but it does not create a new
  evidence transition.
- The Compact GVR synthetic slice is an executed chapter-review burn-down item
  for Compact Generative Systems rather than a new broad active-cycle sweep:
  `python3 scripts/validate_compact_gvr_slice.py` recomputes five public-safe
  compact-generation receipt records, compares a 368-byte literal baseline to a
  78-byte exact repeat-generator-plus-repair receipt, rejects lossy exactness,
  negative-rate/no-fallback, and bounded-search-overrun controls, checks a
  finite `AsiStackProofs.CompactGenerativeSystems` fixture bridge, and accepts
  only the non-core `compact-generative-systems.compact_gvr_receipt_slice`
  transition as `synthetic-test-backed`. The chapter core claim remains
  `argument`, and real codec/generator/verifier, corpus, fallback execution,
  semantic utility, model quality, and downstream utility evidence remain open.
- The Residual honesty conservation fixture is an idea-depth and chapter-review
  burn-down item for Compact Generative Systems rather than a new support-state
  transition: `python3 scripts/validate_residual_honesty_conservation.py`
  recomputes three valid synthetic residual records and five expected-invalid
  controls for hidden, erased, unowned, support-promoting, and
  zero-residual-overclaim controls, writes result
  `experiments/residual_honesty_conservation/results/2026-07-03-local.json`,
  and checks the finite Lean bridge
  `residual_honesty_conservation_fixture_bridge`. It gives residual honesty a
  first record-level conservation fixture while preserving no proof that all
  residuals are observable, no safety proof, no deployed residual-ledger
  behavior, and no chapter-core promotion.
- The real residual-ledger trace is now executed as a Compact Generative Systems
  idea-depth and burn-down item without creating a support-state transition:
  `python3 scripts/validate_residual_ledger_trace.py`
  reads existing Resource flagship, Resource workflow, Compact GVR, and
  Readiness artifacts, writes
  `experiments/residual_ledger_trace/results/2026-07-03-local.json`, and
  checks the finite Lean bridge `residual_ledger_trace_surface_bridge`. The
  trace keeps residualized deferrals, displaced costs, repair residuals,
  readiness escrow, rejected hidden burdens, and no-promotion decisions visible
  across Resource flagship, Compact GVR, and Readiness artifacts. It does not
  prove deployed residual-ledger behavior, safety, model quality, benchmark
  performance, or chapter-core support. Boundary phrase: does not prove deployed residual-ledger behavior.
- The bounded residual-ledger storage replay is now executed as a Compact
  Generative Systems idea-depth and burn-down item without creating a support-
  state transition: `python3 scripts/validate_residual_ledger_storage_replay.py`
  writes `experiments/residual_ledger_storage_replay/results/2026-07-04-local.json`,
  records no-change decision
  `evidence_transitions/v1_x_measured/residual_ledger_storage_replay_no_change.json`,
  and checks the finite Lean bridge `residual_ledger_storage_replay_bridge`.
  The fixture replays four append-only residual events, preserves owner handoff,
  requires discharge review, keeps workload context, computes a digest chain,
  rejects five invalid controls, and records `blocks_promotion`. It is not live or deployed residual-ledger evidence and does not prove safety, model quality,
  benchmark performance, or chapter-core support.
- The Project Theseus generation-mode import is a direct support lane connected
  to Fast Generation and the Project Theseus implementation-reference chapter:
  the imported gate records 18 modes, 13 comparisons, zero hard gaps, zero
  modes with missing report refs, five passing hard boundaries, five accepted
  span-speed lifts, zero useful-solution-per-second, and zero promotable
  comparisons. The ASI-side validator checks the public summary against a
  finite `AsiStackProofs.FastGeneration` fixture and rejects failed hard
  boundary gates and missing-report-ref overclaims. This closes the immediate
  "raw speed is not evidence" gap without claiming a speed-quality result, live
  Theseus replay, public benchmark run, or chapter-core support-state movement.
- `docs/theseus_support_replay_probe.md` adds a local replay-accounting probe
  for the same support surface: the runner executes the architecture-gate import
  validator and the generation-mode import validator, records output digests and
  tracked artifact hashes, and the validator replays both commands before the
  full book gate passes. This improves drift detection for the Project Theseus
  support lane without claiming a clean live Theseus run, public task bundle,
  model-quality result, generation-speed result, external review, or
  support-state transition.
- `docs/theseus_fast_support_lane_run.md` composes that support surface with
  the Theseus public task-bundle import and the Fast Generation task bundle:
  `python3 scripts/validate_theseus_fast_support_lane.py` checks
  `theseus-fast-support-lane-2026-07-03-local`, 4 command replays, 16 tracked
  artifact digests, 68 public task records, 14 expected-invalid or rejected
  controls, 2 accepted no-promotion decisions, and
  `theseusFastSupportAggregateFixture`. This aggregate does not prove clean
  live Project Theseus replay, does not prove model quality, does not promote
  any chapter core claim, does not prove generation speed, and does not create
  support-state promotion. Do not keep producing local Theseus/Fast aggregate
  variants unless they replace a local surface with live, externally
  reviewable, or materially stronger public-safe evidence.
- The next evidence work should deepen the flagship Resource Economics lane by
  replacing repeated local workload-quality evidence, local synthetic
  load-stability evidence, local command replay, and CI publication metadata
  with live or externally reviewable workload-quality review, production
  scheduler logs, measured displaced-cost accounting, live or externally
  reviewed load-stability evidence, physical-feasibility review, and measured
  simulation outputs before opening a new active cycle.
- The measured Resource sublanes now have explicit support-state decisions
  recorded in the aggregate flagship result and evidence-transition files:
  the costed-route and finite burst load-smoothing selector slices have
  accepted narrow non-core transitions, while the workload-quality probe,
  load-stability probe, live-probe replay, CI-cost profile, and workflow trace
  have accepted no-change/no-promotion records. Do not keep producing
  additional local probes unless they replace a local surface with live,
  externally reviewable, or materially stronger measured evidence.

### Milestone 5.5 - Chapter External Grounding And Citation Backfill

Goal: make every chapter credible to readers who already know the surrounding
AI, formal-methods, governance, distributed-systems, or machine-learning
literature.

This milestone is about relation and citation first, not support-state
promotion. It should make clear which ASI Stack terms are Corben's synthesis
vocabulary and which outside ideas, papers, standards, or systems they connect
to.

Tasks:

- For each chapter, load the chapter's `source_ids` from `book_structure.json`
  and its source queue from `docs/book_outline.md`.
- Mine the linked Corben papers first for bibliographies, footnotes, citation
  lists, named algorithms, standards, benchmarks, systems, and neighboring
  research terms.
- For every candidate external source, decide whether it is:
  - a direct comparator or baseline;
  - a prior-art source for an old idea used by the chapter;
  - a neighboring concept that helps readers orient;
  - a future-review lead that should stay in backlog;
  - out of scope or too weak to cite.
- Add accepted third-party sources through `sources/source_inventory.json` with
  `priority: external_literature`, stable IDs, bibliographic metadata where
  known, chapter targets, and public-safe URLs.
- Create or update `sources/source_notes/<source-id>.md` before using the source
  in prose or claim-support language.
- Regenerate Appendix H with `python3 scripts/sync_scaffold.py`; do not edit the
  generated appendix by hand.
- Update chapter source crosswalks and external-SOTA positioning only after the
  source note exists.
- For each chapter, record at least one source-noted external comparator,
  baseline, adjacent literature family, or explicit no-fair-comparator
  exception.
- Connect each load-bearing argument to at least one intended evidence path:
  Lean proof, Project Theseus report/replay, Circle receipt, source-noted
  literature, external review, or no-promotion blocker.
- Treat the former top grounding backlog as narrowed: `the-efficient-asi-hypothesis`
  and `intent-to-execution-contracts` now have source-noted comparator
  expansions. Future work on those rows should default to tests, replay, or
  evidence-path blockers unless a missing comparator is discovered during a
  concrete implementation lane.

Acceptance bar:

- every chapter has a chapter-level external-grounding status: `source-noted`,
  `candidate backlog`, or `explicit exception`;
- Appendix H contains every accepted third-party source through generated
  inventory rows, and Appendix G remains Corben/local only;
- no new citation appears in chapter prose without a source note or recorded
  blocker;
- no external source is treated as reproduced, locally verified, or
  support-state-promoting unless a separate evidence-transition record justifies
  that move;
- the per-chapter evidence plan names proof/evidence routes rather than leaving
  claims as pure prose.

### Milestone 6 - External-SOTA Exception Replacement

Goal: move from "placement gate passes" to "external engagement is strong
enough for serious readers."

Tasks:

- Use the chapter external-grounding pass as the candidate source pool.
- Review `docs/external_sota_positioning_audit.md` for any current or future
  exception rows, regressed positioning rows, or weakly defended comparator
  placements.
- For each current or future exception/backlog row, choose one:
  - add source-noted external baselines and in-prose positioning;
  - keep a true exception with a clear reason;
  - split the chapter's claim if part of it has external comparators and part
    of it is author-originated architecture.
- Prioritize replacement only after a source-noted external comparator exists.
  Do not create placeholder citations merely to avoid exception language; a
  deliberate exception is better than an invented baseline.
- Replaced exception status in this cycle:
  - `asi-is-a-stack-not-a-model` now has source-noted comparators
    `ext_mrkl_systems_2022`, `ext_llm_agents_survey_2023`,
    `ext_standard_model_mind_2017`, and
    `ext_subsumption_architecture_1986`.
  - `constitutional-alignment-substrate` now has source-noted comparators
    `ext_constitutional_ai_2022` and
    `ext_collective_constitutional_ai_2024`;
  - `moral-uncertainty-and-value-conflict` now has source-noted comparators
    `ext_reinforcement_learning_moral_uncertainty_2020` and
    `ext_contestable_ai_design_2022`;
  - `unified-adaptive-tribunal-and-adversarial-review` now has source-noted
    positioning through `ext_contestable_ai_design_2022`.
  - `security-kernel-and-digital-scifs` now has source-noted comparators
    `ext_owasp_llm_top_10_2025`,
    `ext_nist_zero_trust_architecture_2020`, and
    `ext_saltzer_schroeder_protection_1975`.
  - `coil-attention-cyclic-memory-and-recurrence-contracts` now has
    source-noted comparators `ext_transformer_xl_2019`,
    `ext_compressive_transformer_2019`, and `ext_retnet_2023`.
  - `coilra-multicoil-rope-and-cyclic-mixers` now has source-noted
    comparators `ext_roformer_rope_2021`, `ext_lora_2021`,
    `ext_mamba_2023`, and `ext_retnet_2023`.
  - `human-intent-as-a-formal-input` now has source-noted comparators
    `ext_goal_oriented_requirements_engineering_2001`,
    `ext_cooperative_inverse_rl_2016`, and
    `ext_deep_rl_human_preferences_2017`.
  - `stable-capability-fields` now has source-noted comparators
    `ext_capability_based_computer_systems_1984`,
    `ext_semver_2_0_0`, and `ext_slsa_v1_0`.
  - `project-theseus-as-report-first-implementation-reference` now has
    source-noted comparators `ext_model_cards_2019`,
    `ext_datasheets_datasets_2021`,
    `ext_factsheets_ai_services_2019`, and
    `ext_ml_reproducibility_program_2021`.
- Continue mining for stronger social-choice, value-pluralism, legal-process,
  governance-rule, and stack-architecture baselines before any future claim
  split or merge.
- The current audit has no explicit external-baseline exceptions. Future
  author-system exceptions remain allowed only when no fair external baseline is
  currently sourced and the chapter records why.

Acceptance bar:

- every exception has an explicit rationale and next source target;
- chapters with available literature stop relying on exception status;
- source notes exist before prose uses new external baselines.

### Milestone 6.5 - Governed Chapter Consolidation

Goal: reduce structural repetition by merging genuinely overlapping chapters
into fewer deeper chapters while preserving every useful idea, source boundary,
claim boundary, proof hook, and reader path.

Current execution state:

- The Part I 4-to-2 pilot, conservative compression merge, intent/contracts
  merge, MoECOT runtime fold, simulation-fidelity fold, static Context ABI
  merge, verification/adversarial-review merge, planning/DAG consolidation,
  and semantic-representation fold have executed through canonical surfaces.
- The current manifest has 44 chapters, with retired source slugs preserved
  through historical stubs, source chapters archived where appropriate,
  reader-draft history preserved, and no support-state promotion from
  consolidation.
- No new consolidation dry-run, destination-draft, decision-review, scorecard,
  packet, or roadmap-analysis document should be created for an already
  packaged cluster. Future consolidation work is allowed only when new
  evidence, external review, reader-edit findings, or a concrete duplicate
  artifact boundary justifies a new execute/reject decision.
- Any future execution still means changing the canonical surfaces:
  `book_structure.json`, `docs/book_outline.md`, destination chapter files,
  source queues, Appendix C, Appendix K, proof-manifest routing, handoffs,
  reader-manuscript records, URL/history treatment, changelog, and validators
  in one coherent package.
- Existing planning docs stay as archival review inputs, but they should stop
  growing. The current product should now move through proof depth, evidence
  replay, external grounding, and curated-reader prose, not another
  consolidation-planning layer.

This is not a deletion pass and not a mandate to hit a target chapter count.
The attached consolidation critique is useful planning input, but it is not
source evidence and should not override the manifest until a merge pilot passes
the reconciliation checks below.

Decision from the 2026-06-29 consolidation review: the critique is right about
the main failure mode. Several chapters are not wrong as ideas; they are weak
as separate rendered skeletons because they repeat the same Problem,
Insufficiency, Mechanism, Interface, Evidence, and Handoff moves around adjacent
claims. The right response is re-consolidation into chapter-owning artifacts,
not deletion, prose-only tightening, or a blind chapter-count target.

Diagnostic target shape:

- Aggressive consolidation was originally framed as moving the 54-chapter shape
  toward roughly 44 deeper chapters.
- Conservative consolidation was originally framed as leaving the book closer
  to 47 chapters by keeping technique-owning chapters such as
  RankFold/NeuralFold separate. The current executed path has reached 44 active
  chapters while retaining RankFold/NeuralFold, folding MoECOT into Routing,
  folding simulation fidelity into Resource Economics, folding the standalone
  command-contract skeleton into Intent-to-Execution as **Command Contracts:
  From Intent to Executable Work**, folding semantic page/certificate mechanics
  into the Virtual Context ABI, and merging adversarial review into the
  proof-carrying-claims chapter.
- Historical diagnostic phrase preserved for validation: conservative
  consolidation has moved past the original 47-chapter diagnostic shape to the
  current 44-chapter manifest; the count remains a diagnostic, not a success
  metric.
- Neither count is a success metric. The success metric is less repeated
  skeleton, stronger chapter ownership, preserved source/proof/claim coverage,
  and better reader flow.

Follow-up review outcome:

- The re-consolidation idea is accepted as a real roadmap improvement. It
  targets structural repetition created by over-splitting, not book length for
  its own sake.
- The implementation discipline from the critique is also accepted: a merged
  chapter must have one chapter skeleton, not two or three complete source
  chapter skeletons pasted together. Preserved ideas should become named
  mechanisms, sections, subclaims, proof hooks, source rows, examples, or
  implementation-horizon facets inside the destination chapter.
- The roadmap response is stateful consolidation, not an immediate manifest
  edit: every cluster must move through a recorded state such as
  `planned_candidate`, `fold_review_candidate`, `dry_run_packaged`,
  `review_ready`, `fold_disposition_ready`, `executed`,
  `deferred_for_release`, or `rejected_or_retained`.
- Appendix C reconciliation, source-ID union, Lean/proof-tag union, fixture
  treatment, reader-overlay treatment, and URL/redirect policy are not cleanup
  chores after a merge. They are merge preconditions.
- The Part I pilot, conservative compression merge, intent/contracts merge,
  MoECOT runtime fold, simulation-fidelity fold, static Context ABI merge,
  verification/adversarial-review merge, planning/DAG control consolidation,
  and semantic-representation fold are now executed history with retired-URL
  treatment recorded in `docs/chapter_consolidation_url_history_policy.md` and
  `docs/chapter_history_ledger.md`.
- The 2026-06-30 follow-up does not add a new cluster. Its current rule is now
  stability, not more packaging: broad human-reader curation may proceed on the
  44-chapter spine, while future consolidation requires a concrete new
  source/evidence/reviewer/reader-edit finding and the same execute, revise,
  defer, or reject/retain record discipline before any manifest edit.

Attachment-specific verdict:

- The latest proposal is right about the highest-leverage edit: collapse
  duplicated chapter skeletons where adjacent chapters are trying to carry one
  architectural artifact, then reinvest the saved space in mechanisms, negative
  cases, external positioning, proof limits, and reader flow.
- The proposal is not accepted as a chapter-count target or a direct cut list.
  A 44-ish table of contents is useful as a pressure test; the current
  44-chapter manifest is still correct when each chapter owns a distinct
  artifact, interface, proof family, evidence lane, implementation horizon, or
  reader throughline.
- The strongest near-term action has moved past consolidation packaging: the
  project should keep those executed decisions stable unless new evidence or
  reader-edit findings expose a concrete duplicate boundary, and spend the next
  cycles on proof depth, evidence replay, external grounding, and curated human
  prose.
- A merge that only shortens the book fails. A merge succeeds only when the
  destination chapter becomes easier to argue, cite, prove around, test, and
  read than the separate chapters.

Consolidation decision queue:

The existing packaged queue has been resolved for the current manifest. The
next consolidation work should not create more destination drafts for packages
that are already executed or retained. It should create a new decision only
when a concrete later finding changes chapter ownership.

| Order | Package | Required decision | Execution note |
|---|---|---|---|
| 1 | Part I constitutional alignment and agency/corrigibility | Executed. | Retired agency/corrigibility slug preserved; agency/corrigibility survives as sections, subclaims, proof hooks, and reader path in the destination chapter. |
| 2 | Part I value conflict and contestable governance | Executed. | Retired governance-rights slug preserved; fork, exit, audit, redaction, appeal, dissent, and revisit interfaces survive as sections and subclaims. |
| 3 | Compression and residual honesty | Conservative merge executed. | Generate-Verify-Repair folded into Compact Generative Systems; RankFold/NeuralFold retained as a standalone technique chapter. |
| 4 | Intent and executable contracts | Executed. | `intent-to-execution-contracts` is now **Command Contracts: From Intent to Executable Work**; `human-intent-as-a-formal-input` remains the separate intent-intake chapter, and the retired command-contract URL is preserved as history. |
| 5 | Static context ABI | Executed. | Semantic pages and context-cell certificate material folded into the Virtual Context ABI; context transactions and verification bandwidth remain standalone. |
| 6 | Verification and adversarial review | Executed. | Tribunal review folded into Proof-Carrying Claims and Adversarial Review; claim ledgers remain the belief-revision substrate. |
| 7 | Planning and DAG control | Executed. | PlanForge folded into Planning as a Control Layer; cognitive compilation remains the semantic-IR and lowering-receipt layer. |
| 8 | Fold-disposition candidates | Executed or retained. | MoECOT runtime, simulation fidelity, and semantic representation folds have executed; Runtime Adapters and Labor OS are retained as separate artifact owners unless later evidence changes that boundary. |

Any future decision record should name the reviewed package, reviewer or review
source, destination-skeleton judgment, claim/source/proof/reader impact,
external-grounding adequacy, URL or redirect policy, validation scope,
support-state effect, non-claims, and the exact decision. If execution is
accepted, implement one cluster per commit so rollback and review remain
legible. If a package is deferred or rejected, record the reader-work
disposition so curated prose may continue without pretending the repetition
question disappeared.

Cluster decision scorecard:

| Check | Execute signal | Revise, defer, or reject signal |
|---|---|---|
| Chapter ownership | The destination owns one artifact, interface, proof family, evidence lane, implementation horizon, or reader throughline more clearly than the source chapters. | The source chapters still own distinct artifacts or the destination becomes a generic umbrella. |
| Skeleton removal | One Problem, Insufficiency, Mechanism, Interfaces, Invariants, Failure Modes, MVI, Beyond-SOTA, Test Plan, Source Crosswalk, Summary, and Handoff path can carry the whole argument. | The draft reads like two or three full chapters pasted under one heading. |
| Claim reconciliation | One destination core claim is narrower or clearer, and folded claims survive as subclaims, sections, proof hooks, source rows, or explicit retirements. | Core-claim meaning broadens, subclaims disappear, or support-state pressure appears without new evidence. |
| Evidence and proof routing | Lean modules, harness rows, source notes, external comparators, negative cases, and no-promotion blockers become easier to see. | Proof tags, harnesses, external baselines, or source queues become harder to locate or weaker to audit. |
| Reader value | The merge reduces repeated exposition and makes the human-reader path smoother without hiding evidence boundaries. | The merge saves pages but makes the concept harder to understand, cite, or listen to. |
| Release hygiene | URL/history policy, handoff repairs, reader-overlay or curated-reader repairs, Appendix C, Appendix K, scaffold sync, validation, and changelog can ship in one reviewable commit. | The merge would leave stale URLs, orphaned chapter IDs, broken handoffs, unreviewed reader deltas, or ambiguous generated state. |

Consolidation execution gate:

- A review-ready merge package may not be executed only because it reduces the
  table of contents. It must show that one destination skeleton improves the
  argument by making the mechanism, evidence path, proof limits, implementation
  horizon, and reader handoff clearer than the separate source chapters.
- A review-ready merge package also may not be stalled by asking for another
  abstract decision surface. If the existing package identifies the source,
  proof, claim, reader, URL, and validation effects, the next action is a
  manifest-changing execution commit or an explicit rejection/retention with a
  concrete loss reason.
- Before a source chapter inside a pending package graduates into the curated
  reader manuscript, the package needs one of three recorded stability
  outcomes: `executed`, `deferred_for_release`, or
  `rejected_or_retained`. A revise decision means the package is still pending.
  Without a stability outcome, only local prose cleanup is allowed.
- A deferred package must say why the current release is allowed to keep the
  duplicate skeletons, what reader confusion remains, and when the decision
  should be revisited.
- A rejected or retained package must name the distinct artifact, proof lane,
  evidence lane, implementation horizon, or reader throughline that justifies
  keeping the chapters separate.
- An executed package must include the manifest edit, outline update, Appendix
  C reconciliation, Appendix K implementation-horizon reconciliation, proof
  manifest handling, source-union handling, reader-overlay or curated-reader
  repair, URL/history treatment, scaffold sync, validation output, and a
  changelog entry in the same reviewable change set.

Decision rubric:

- A chapter is chapter-owning when it owns a distinct artifact, interface,
  evidence lane, proof family, implementation horizon, or reader throughline
  that would become weaker if buried.
- A chapter is a consolidation candidate when most of its reader-visible load
  repeats another chapter's source family, claim motion, mechanism, interface,
  failure modes, implementation horizon, and handoff while adding only a
  supporting facet.
- A merge is justified only if the destination draft reduces repeated skeleton
  load and increases mechanism depth, external positioning, proof specificity,
  negative-case treatment, or reader clarity.
- A merge is rejected or deferred when the proposed destination loses a useful
  artifact boundary, makes claim ownership less legible, weakens proof/evidence
  routing, or merely compresses the table of contents without improving the
  argument.

Execution tiers:

| Tier | Candidate work | Why it matters | Expected shape effect |
|---|---|---|---|
| Executed packages | Alignment/governance philosophy; compression/representation; intent/contracts; context/memory static ABI; verification/review; planning/control; MoECOT runtime; simulation fidelity; semantic representation. | These packages reduced repeated skeletons while preserving source mappings, proof hooks, implementation horizons, URL history, and no-support-state-change boundaries. | Current canonical spine is 44 chapters; the next quality work should deepen those chapters rather than re-plan the same packages. |
| Future-only review | Any later duplicate-boundary finding, including a possible runtime-adapter/Labor OS revisit. | Future consolidation is justified only by new source/evidence/reviewer/reader-edit findings that show a chapter no longer owns a distinct artifact, proof lane, evidence lane, implementation horizon, or reader throughline. | One package per commit only if the destination is stronger, not merely shorter. |
| Protected set | Theseus, Circle/coil, the mathematical/search umbrella for now, recursive self-improvement, execution artifacts, evidence discipline, security kernel, benchmark ratchets, living-book methodology, and other high-ownership chapters listed below. | These chapters own distinct artifacts, proof paths, evidence lanes, or release machinery. | No merge unless later source/evidence review shows duplicate artifact ownership. |

Candidate clusters to review:

- Alignment/governance philosophy:
  - consider merging `constitutional-alignment-substrate` with
    `agency-dignity-and-corrigibility`;
  - consider merging `moral-uncertainty-and-value-conflict` with
    `governance-rights-fork-exit-and-audit`;
  - preserve protected predicates, agency/corrigibility interfaces,
    value-conflict records, fork/exit/audit rights, and dissent/revisit paths as
    sections or subclaims.
- Compression/representation:
  - executed: `generate-verify-repair-compression` is folded into
    `compact-generative-systems-and-residual-honesty`, while
    `rankfold-neuralfold-and-artifact-compression` remains a standalone retained
    technique chapter;
  - executed destination title:
    **Compact Generative Systems: Generate, Verify, Repair, and Residual
    Honesty**;
  - executed: `semantic-representation-and-tree-structured-models` is folded
    into the compact-generative destination as **Semantic Representation
    Leasing**, with semantic-node records, source mappings, proof hooks, reader
    overlay retirement, URL history, and restoration conditions preserved.
- Intent and contracts:
  - executed: `command-contracts-and-semantic-interfaces` is folded into
    `intent-to-execution-contracts`, now titled **Command Contracts: From
    Intent to Executable Work**;
  - keep `human-intent-as-a-formal-input` as the Part I intent-intake chapter,
    with its handoff aimed at the Part II command-contract chapter rather than
    repeating that chapter's execution skeleton.
- Context/memory:
  - executed: `semantic-pages-context-cells-and-certificates` is folded into
    `virtual-context-abi`, now titled **The Virtual Context ABI: Typed Pages,
    Cells, and Certificates**;
  - preserve semantic pages, context cells, certificate truthfulness, source
    bindings, omissions, authority ceilings, loss contracts, permitted uses,
    and stale-certificate blockers as destination sections, source rows, and
    proof tags rather than a second rendered skeleton;
  - keep `context-transactions-snapshots-mounts-and-taint` and
    `verification-bandwidth-and-context-adequacy` separate unless a later review
    finds real overlap in artifact ownership.
- Verification/review:
  - executed: `unified-adaptive-tribunal-and-adversarial-review` is folded
    into `spinoza-verification-and-proof-carrying-claims`, now titled
    **Proof-Carrying Claims and Adversarial Review**;
  - preserve tribunal dossiers, adversarial probes, dissent, required actions,
    verdict constraints, unchanged-evidence guards, source mappings, proof
    hooks, and reader lineage inside the destination chapter rather than a
    second rendered skeleton;
  - keep `claim-ledgers-and-belief-revision` separate as the substrate they
    update.
- Planning:
  - executed: `planforge-dags-and-intelligence-arbitrage` is folded into
    `planning-as-a-control-layer`, now titled **Planning as a Control Layer:
    DAGs and Intelligence Arbitrage**;
  - preserve DAG scheduling, dependency ordering, capability tiers,
    intelligence arbitrage, adequacy contracts, cost-quality ledgers,
    escalation paths, residuals, source mappings, proof hooks, fixture rows,
    URL history, and reader lineage inside the destination chapter rather than
    a second rendered skeleton;
  - keep `cognitive-compilation-and-semantic-ir` separate as the lowering/IR
    and semantic-receipt artifact.
- Possible folds:
  - executed: `moecot-runtime-and-multi-core-orchestration` is folded into
    `routing-heads-and-specialist-cores` until public-safe runtime, replay,
    benchmark, and corroboration evidence make a standalone chapter
    chapter-owning again;
  - executed: `simulation-fidelity-and-physical-constraints` is folded into
    `resource-economics-and-token-budgets` as a Simulation Fidelity and Claim
    Transport section until public-safe simulator artifacts,
    physical-computation audits, fidelity calibration, benchmark-transfer
    negative cases, or independent review make a standalone chapter
    chapter-owning again;
  - executed: `semantic-representation-and-tree-structured-models` is folded
    into `compact-generative-systems-and-residual-honesty` as Semantic
    Representation Leasing until public-safe semantic-graph evidence, hierarchy
    revision harnesses, representation-utility benchmarks, or independent review
    make a standalone chapter chapter-owning again;
  - treat any possible `runtime-adapters-tool-permissions-and-human-approval`
    fold into `labor-os-and-typed-jobs` as low priority and permissible only if
    the permission/tool-interface surface stops owning a distinct artifact.

Protected standalone chapters unless a later evidence review contradicts them:

- `asi-is-a-stack-not-a-model`;
- `the-efficient-asi-hypothesis`;
- `system-boundaries-and-authority`;
- `failure-modes-of-ungoverned-intelligence`;
- `evidence-states-and-claim-discipline`;
- `stable-capability-fields`;
- `capability-replacement-and-rollback`;
- `security-kernel-and-digital-scifs`;
- `recursive-self-improvement-boundaries`;
- `verification-bandwidth-and-context-adequacy`;
- `claim-ledgers-and-belief-revision`;
- `readiness-gates-residual-escrow-and-quarantine`;
- the execution cluster unless a specific duplicate artifact is identified:
  `labor-os-and-typed-jobs`, `artifact-graphs-audit-logs-and-replay`,
  `runtime-adapters-tool-permissions-and-human-approval`, and
  `procedural-memory-and-cognitive-loop-closure`;
- Circle/coil chapters for now:
  `circle-calculus-and-proof-carrying-ai-contracts`,
  `coil-attention-cyclic-memory-and-recurrence-contracts`, and
  `coilra-multicoil-rope-and-cyclic-mixers`;
- `mathematical-and-search-substrates`, because it is the umbrella touching the
  Circle/coil/search substrate family and should not be deduplicated until the
  Circle/coil evidence lane is reviewed explicitly;
- `benchmark-ratchets-and-anti-goodhart-evidence`;
- `project-theseus-as-report-first-implementation-reference`;
- `artifact-steward-agents-and-living-project-governance`;
- `executable-specifications-and-lean-proof-envelope`;
- `integrated-reference-architecture`;
- `prototype-roadmap`;
- `living-book-methodology`;
- `open-research-agenda-and-bibliography-plan`.

Merge checklist:

- Start with the alignment/governance philosophy pilot, because it already has
  the dry-run packages, destination drafts, URL policy, and release-stability
  caveat needed to execute.
- For non-pilot packages, reuse the existing dry-run packages and destination
  drafts. Do not create a second planning layer unless execution exposes a
  missing field that blocks a validator.
- Before editing `book_structure.json`, perform a final inline reconciliation
  pass inside the execution commit: destination title, source chapters,
  stable-ID policy, claim dispositions, source-ID union, external-source union,
  proof-tag union, test/harness rows, reader-overlay changes, handoff repairs,
  implementation-horizon merge, URL or redirect decision, and expected
  chapter-count effect.
- For every proposed merge, write a claim-reconciliation plan before editing
  `book_structure.json`: the merged chapter gets one core claim; retained
  chapter claims become subclaims, sections, source-crosswalk rows, proof hooks,
  or explicit no-promotion/retirement decisions.
- Preserve source IDs by unioning `source_ids` and updating source loading
  queues in `docs/book_outline.md`.
- Preserve Lean proof modules and proof tags unless a proof target is explicitly
  retired with a reason.
- Preserve implementation horizons by combining the smallest honest MVI and the
  mature endpoint into one coherent chapter horizon.
- Update Human Reading Path prose, Handoff sections, reader overlays, reader
  review matrices, chapter external-grounding status, external-SOTA positioning,
  Appendix C, Appendix K, proof manifests, and changelog after any manifest
  merge.
- Collapse the chapter skeleton once. Do not paste two full Problem,
  Insufficiency, Mechanism, Interfaces, Invariants, Failure Modes, MVI, Mature
  Endpoint, Test Plan, Source Crosswalk, and Summary sections back to back.
- The merged chapter should be deeper than either input chapter: use the saved
  space for sharper mechanisms, concrete fixtures, negative cases, external
  positioning, proof limitations, and a clearer reader-facing throughline.
- Each package should name the repeated skeleton load it removes and how the
  saved space will be reinvested. Acceptable reinvestment includes deeper
  mechanism exposition, external comparator treatment, negative controls,
  proof-limit discussion, concrete examples, implementation traces, or better
  reader continuity.
- Record why the destination chapter is stronger by the rubric above: what
  artifact boundary is preserved, what repeated skeleton load is removed, what
  proof/evidence path becomes clearer, and what reader confusion is reduced.
- Keep stable slug IDs only when continuity is stronger than renaming; otherwise
  record redirects and handoff repair needs before changing file paths.
- If a chapter is folded rather than merged, record the surviving section,
  preserved subclaims, preserved source/proof hooks, and no-promotion boundary
  explicitly. A fold must not become silent deletion.

Acceptance bar:

- at least one pilot manifest merge executes before another consolidation
  planning packet is added for an existing package;
- the execution commit names every preserved source, subclaim, proof hook, test row,
  implementation horizon, reader overlay, and handoff change;
- `python3 scripts/chapter_adjacency_report.py` is used before and after a
  manifest merge;
- `python3 scripts/sync_scaffold.py`,
  `python3 scripts/sync_proof_manifest.py`, Appendix C generation, reader
  checks, and Quarto render pass after the merge;
- no idea is removed merely to reduce chapter count;
- no support state, source-derived claim, proof result, or test result is
  fabricated by the consolidation.

Current status:

- `docs/chapter_consolidation_pilot_plan.md` records the first pilot plan for
  the Part I alignment/governance philosophy cluster.
- `docs/chapter_consolidation_sequence.md` records the full governed sequence
  for the latest 54-to-44/47 critique: the Part I pilot stays first, while the
  intent/contract, context, verification, planning, semantic-representation,
  and low-priority runtime-adapter
  candidates each require their own package or explicit review decision before
  any future manifest edit.
- The sequence now records consolidation states so candidates cannot jump from
  "interesting idea" to manifest change: the Part I pilot, conservative
  compression merge, MoECOT runtime fold, simulation-fidelity fold,
  intent/contracts, static context ABI, verification/adversarial review,
  planning/DAG control, and semantic representation are `executed`; and
  runtime-adapters/Labor
  OS is
  `rejected_or_retained` unless a later evidence review finds duplicate
  artifact ownership. The latest attachment does not add another merge
  package; it reinforces the duty to decide the existing queue.
- The pilot executed two merges:
  `constitutional-alignment-substrate` absorbed
  `agency-dignity-and-corrigibility`, and
  `moral-uncertainty-and-value-conflict` absorbed
  `governance-rights-fork-exit-and-audit`.
- The roadmap now records a tiered consolidation sequence and diagnostic target
  shape: an aggressive pass may land near 44 chapters, while a conservative
  pass may land near 47, but the count is only a diagnostic for repetition
  reduction and never a reason to drop an idea; the current executed manifest
  now has 44 chapters after the semantic-representation fold.
- `scripts/validate_chapter_consolidation_sequence.py` keeps the sequence
  visible from the roadmap, README, publication readiness, and repository map
  while confirming the canonical manifest now has 44 chapters.
- The latest 54-to-44 consolidation critique is accepted as roadmap guidance,
  not as a direct manifest-edit instruction. Its strongest recommendation is
  sequencing: resolve the highest-repetition merge pilot before broad
  reader-manuscript curation, then apply the same reconciliation discipline to
  the compression, intent/contract, context, verification, planning, and
  fold-only clusters only if the pilot shows that depth and readability improve.
- The latest pasted consolidation note has been re-reviewed against the current
  roadmap and has teeth: the repetition problem is mostly skeleton duplication
  across adjacent chapter-owning claims, not bad ideas. It does not require a
  new chapter cluster beyond the existing decision queue. Its useful force is
  to keep the project walking execute, revise, defer, or reject decisions for
  the already packaged clusters instead of continuing to create abstract
  consolidation plans.
- The 2026-06-30 attachment review reinforces that the 54-to-44/47 target is
  diagnostic, not a mandate. The roadmap should now spend consolidation effort
  on reviewed decisions for the existing packages, beginning with the Part I
  alignment/governance pilot, and should only edit `book_structure.json` after
  a package clears the claim/source/proof/reader reconciliation gate. A
  successful merge must improve chapter ownership and reader flow while
  preserving Appendix C rows, source unions, Lean modules, proof tags,
  implementation horizons, reader paths, URL history, and no-promotion
  boundaries.
- The initial external-grounding precondition for the two destination chapters
  is improved by source notes for Constitutional AI, Collective Constitutional
  AI, reinforcement learning under moral uncertainty, and contestable AI, but
  the manifest should not merge chapters until claim/source/proof/reader
  reconciliation passes.
- `scripts/validate_chapter_consolidation_pilot_plan.py` verifies that the plan
  preserves all four source chapter IDs, required source IDs, required Lean
  proof tags, no-manifest-edit language, no-support-state-change language, both
  dry-run packages, and both destination drafts.
- `docs/chapter_consolidation_dry_run_constitutional_alignment.md` records the
  dry-run merge package for the `constitutional-alignment-substrate` plus
  `agency-dignity-and-corrigibility` pilot destination, including the
  illustrative manifest diff, one-skeleton outline, Appendix C row plan,
  source/proof/test/reader/handoff reconciliation, implementation-horizon
  merge, URL policy, validation commands, and no-support-state-change boundary.
- `docs/chapter_consolidation_dry_run_contestable_governance.md` records the
  dry-run merge package for the `moral-uncertainty-and-value-conflict` plus
  `governance-rights-fork-exit-and-audit` pilot destination, including the
  illustrative manifest diff, one-skeleton outline, Appendix C row plan,
  source/proof/test/reader/handoff reconciliation, implementation-horizon
  merge, URL policy, validation commands, and no-support-state-change boundary.
- Both dry-run packages are now covered by
  `scripts/validate_chapter_consolidation_pilot_plan.py`.
- `docs/chapter_consolidation_dry_run_compression.md` records the first
  non-pilot dry-run package, for **Compact Generative Systems: Generate,
  Verify, Repair, and Residual Honesty**. It proposes keeping
  `compact-generative-systems-and-residual-honesty` as the continuity ID,
  folding `generate-verify-repair-compression`, and either folding or retaining
  `rankfold-neuralfold-and-artifact-compression` depending on whether review
  finds distinct technique ownership. Its semantic-representation exclusion is
  now historical: `docs/chapter_consolidation_fold_semantic_representation.md`
  records the later executed fold into the compact-generative destination.
- `docs/chapter_consolidation_destination_draft_compression.md` now records the
  historical destination draft for the executed conservative **Compact
  Generative Systems: Generate, Verify, Repair, and Residual Honesty** merge.
  Active status now lives in the manifest, outline, URL history policy,
  chapter-history ledger, Appendix C, proof manifest, and reader records.
- `docs/chapter_consolidation_dry_run_intent_contracts.md` records the Tier 1C
  dry-run package for **Command Contracts: From Intent to Executable Work**. It
  proposes keeping `intent-to-execution-contracts` as the continuity ID,
  folding `command-contracts-and-semantic-interfaces`, and keeping
  `human-intent-as-a-formal-input` standalone as the raw-intent intake,
  ambiguity, authority-extraction, bounded-default, re-contract, and
  stop-condition chapter.
- `docs/chapter_consolidation_destination_draft_intent_contracts.md` now
  records the historical destination draft for the executed **Command
  Contracts: From Intent to Executable Work** merge. Active status now lives in
  the manifest, outline, URL history policy, chapter-history ledger, Appendix
  C, proof manifest, and reader records.
- `docs/chapter_consolidation_dry_run_context_abi.md` records the Tier 1D
  dry-run package for **The Virtual Context ABI: Typed Pages, Cells, and
  Certificates**. The package has now executed: `virtual-context-abi` remains
  the continuity ID, `semantic-pages-context-cells-and-certificates` is
  preserved as typed-page and certificate subclaims, and
  `context-transactions-snapshots-mounts-and-taint`,
  `verification-bandwidth-and-context-adequacy`, and
  `claim-ledgers-and-belief-revision` remain standalone.
- `docs/chapter_consolidation_destination_draft_context_abi.md` records the
  destination draft used for the executed Context ABI merge; active status now
  lives in the manifest, outline, URL history policy, chapter-history ledger,
  Appendix C, proof manifest, and reader records.
- `docs/chapter_consolidation_dry_run_verification_review.md` records the Tier
  2A dry-run package for **Proof-Carrying Claims and Adversarial Review**. It
  has now executed: `spinoza-verification-and-proof-carrying-claims` remains
  the continuity ID, `unified-adaptive-tribunal-and-adversarial-review` is
  preserved as tribunal and adversarial-review subclaims, and
  `claim-ledgers-and-belief-revision` remains the durable claim substrate.
- `docs/chapter_consolidation_destination_draft_verification_review.md` now
  records the historical destination draft for the executed **Proof-Carrying
  Claims and Adversarial Review** merge. Active status now lives in the
  manifest, outline, URL history policy, chapter-history ledger, Appendix C,
  proof manifest, and reader records.
- `docs/chapter_consolidation_dry_run_planning_dag.md` records the Tier 2B
  dry-run package for **Planning as a Control Layer: DAGs and Intelligence
  Arbitrage**. It has now executed: `planning-as-a-control-layer` remains the
  continuity ID, `planforge-dags-and-intelligence-arbitrage` is preserved as
  DAG scheduling and intelligence-arbitrage subclaims, and
  `cognitive-compilation-and-semantic-ir` remains standalone as the semantic IR
  and lowering-receipt chapter.
- `docs/chapter_consolidation_destination_draft_planning_dag.md` now records
  the historical destination draft for the executed **Planning as a Control
  Layer: DAGs and Intelligence Arbitrage** merge. Active status now lives in
  the manifest, outline, URL history policy, chapter-history ledger, Appendix
  C, proof manifest, and reader records.
- `docs/chapter_consolidation_release_stability_review.md` records the current
  consolidation queue state: executed packages are historical, and any
  remaining deferred package must still pass source/proof/claim/reader/URL
  reconciliation before a manifest change. `docs/chapter_consolidation_decision_review.md`
  remains the historical Part I pilot decision surface, and
  `docs/chapter_consolidation_url_history_policy.md` records the public URL
  and history treatment required in any future execution commit. Human-reader
  curation may proceed outside the pending Part I merge cluster.
- The latest re-consolidation proposal is accepted as directionally correct,
  but the roadmap response is not another abstract plan and not an immediate
  54-to-44 manifest edit. The two useful pilot artifacts are review-ready
  destination chapter drafts written as one chapter with one skeleton, followed
  by a decision to execute, defer, or reject each merge.
- The latest pasted consolidation recommendation reinforces the existing queue
  rather than changing it: alignment/governance philosophy, compression and
  residual honesty, intent/contracts, static context ABI, verification/review,
  planning/DAG control, MoECOT runtime, simulation fidelity, and semantic
  representation have executed through governed packages. The roadmap accepts
  the recommendation's central
  rule that every accepted package must collapse duplicated skeletons while
  preserving ideas as sections, subclaims, proof hooks, source mappings,
  implementation horizons, reader paths, or explicit no-promotion/retirement
  decisions.
- `docs/chapter_consolidation_destination_draft_constitutional_alignment.md`
  now records the historical destination draft for the executed
  **Constitutional Alignment: Agency, Dignity, and Corrigibility** merge.
- `docs/chapter_consolidation_destination_draft_contestable_governance.md`
  now records the historical destination draft for the executed **Moral
  Uncertainty, Value Conflict, and Contestable Governance** merge.
- `docs/chapter_consolidation_external_review_packet.md` now gives reviewers a
  focused decision surface for the pilot: execute, revise, defer, or reject
  each proposed merge, while preserving the boundary that review input is not
  evidence, proof, artifact approval, or support-state movement.
- `docs/chapter_consolidation_full_review_packet.md` now gives reviewers a
  full decision-queue surface for all review-ready merge packages and fold
  dispositions, including the five non-pilot destination drafts and the three
  fold-disposition packages. It now also asks reviewers to apply the 54-to-44/47
  critique as a one-skeleton depth test by naming the repeated skeleton load
  removed and the mechanism, negative-control, external-positioning,
  proof-limit, implementation-trace, example, or reader-continuity work where
  the saved space should be reinvested. It is a request surface only: no
  external review has been accepted, no package is authorized, no manifest edit
  is made, and no support state moves.
- `docs/chapter_consolidation_release_stability_review.md` is now historical
  release-control context. The packages it once deferred have either executed
  or been retained in the current 44-chapter manifest, with URL stubs and
  chapter-history records preserving retired public slugs.
- The executed fold histories remain recorded in
  `docs/chapter_consolidation_fold_moecot_runtime.md`,
  `docs/chapter_consolidation_fold_simulation_fidelity.md`, and
  `docs/chapter_consolidation_fold_semantic_representation.md`; these are
  historical evidence of the fold decisions, not open merge tickets.
- The roadmap no longer treats consolidation as the main work item. The active
  work is proof depth, evidence replay, external grounding maintenance,
  reader-manuscript curation, authorial craft, and artifact review on the
  stable 44-chapter spine.
- Future consolidation is allowed only when a new source, evidence result,
  reviewer finding, or Corben reader-edit finding identifies a concrete
  duplicate artifact boundary. If that happens, use the same one-package,
  one-commit reconciliation discipline; do not reopen the old queue or target a
  chapter count.

### Milestone 7 - Curated Human-Reader Manuscript

Goal: make the normal reader version a book someone would enjoy reading or
listening to, while preserving the live book as the research/evidence source.

Execution pivot:

- Stop treating first-pass curated chapters as the finish line. The manuscript
  is not human-edit ready until consolidation decisions have been reflected in
  the reader table of contents, every active chapter has curated prose that can
  stand without placeholders, and a book-level continuity edit has removed
  repeated scaffolding and repaired transitions.
- The next reader task is not another review report. All 44 active manifest
  chapters now have tracked curated reader files; the Part I, Part II, Part
  III, and Part IV have all 44 records reconciled for
  prose meaning, and
  `scripts/build_curated_reader_edition.py --check` verifies that those files
  assemble into a renderable local Quarto review workspace. The remaining work
  is release-quality book-level continuity editing, exact format artifact review,
  optional sidecar author-enrichment routing, and edition release recording, not
  coverage bookkeeping.
- Human-reader source may become a parallel derivative prose source for
  pacing, examples, openings, closings, and audio flow, but the live book
  remains authority for claims, support states, source boundaries, proof/test
  status, implementation horizons, and release records.
- The reader manuscript is not final merely because every chapter has a
  drafting file. It needs a book-level thesis, part-level narrative arcs,
  chapter-specific stakes, memorable repeatable ideas, finished third-person
  prose, and an explicit no-fabricated-first-person boundary before it is ready
  for serious human review.

Tasks:

- Select a consolidation-aware pilot set for curated graduation. Protected
  standalone chapters may graduate when overlays are too small; source chapters
  inside any future merge or fold package should either edit the active
  destination chapter directly or record a scoped/deferred caveat; do not leave
  reader work idle just because a structural question exists:
  - `asi-is-a-stack-not-a-model`;
  - `the-efficient-asi-hypothesis`;
  - `system-boundaries-and-authority`;
  - `failure-modes-of-ungoverned-intelligence`;
  - `evidence-states-and-claim-discipline`;
  - `human-intent-as-a-formal-input`;
  - `security-kernel-and-digital-scifs`;
  - `stable-capability-fields`;
  - `capability-replacement-and-rollback`;
  - `readiness-gates-residual-escrow-and-quarantine`;
  - `context-transactions-snapshots-mounts-and-taint`;
  - `verification-bandwidth-and-context-adequacy`;
  - `claim-ledgers-and-belief-revision`;
  - `labor-os-and-typed-jobs`;
  - `artifact-graphs-audit-logs-and-replay`;
  - `runtime-adapters-tool-permissions-and-human-approval`;
  - `procedural-memory-and-cognitive-loop-closure`;
  - `benchmark-ratchets-and-anti-goodhart-evidence`;
  - `policy-optimization-and-learning-from-feedback`;
  - `integrated-reference-architecture`;
  - `project-theseus-as-report-first-implementation-reference`;
  - `prototype-roadmap`;
  - `living-book-methodology`;
  - `open-research-agenda-and-bibliography-plan`;
  - `recursive-self-improvement-boundaries`;
  - `circle-calculus-and-proof-carrying-ai-contracts`;
  - `executable-specifications-and-lean-proof-envelope`;
  - `artifact-steward-agents-and-living-project-governance`.
- Use `scripts/init_curated_reader_chapter.py --chapter-id <id>` in dry-run
  mode before creating any curated chapter.
- Use `scripts/build_curated_reader_edition.py --check` after curated-reader
  edits, and use `python3 scripts/build_curated_reader_edition.py --output
  build/curated_reader_edition` plus `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
  quarto render build/curated_reader_edition --to html` plus
  `node scripts/validate_reader_html_artifact_browser.js --strict --site
  build/curated_reader_edition/_reader_site --manifest
  build/curated_reader_edition/reader_manifest.json --report
  build/curated_reader_edition/curated_reader_html_browser_report.json` for
  local source-level review. This proves renderability and local browser
  viability of the tracked curated source only; it does not approve a reader
  artifact or clear release blockers.
- Graduate only chapters where overlays are too small for the required edit:
  new openings, reordered examples, sustained analogies, narrative continuity,
  section compression, or audio pacing.
- For each curated chapter, record:
  - generated reader baseline;
  - live source commit or tag;
  - curation scope;
  - divergence summary;
  - meaning-preservation checks;
  - canonical-source changes required;
  - active release blockers.
- Add a "reader promise" note to each curated chapter: what a human should
  understand after reading it, without changing claim support.
- With consolidation execution reflected in the current table of contents, run a
  book-level reader edit over the destination table of contents, not the old
  pre-consolidation 54-chapter shape. This pass should remove duplicated
  introductions, repair part transitions, normalize examples, and push the
  prose to finished quality; Corben's later editing notes are polish over a
  complete book, not a stage the prose waits for (2026-07-02 direction).
- During the book-level continuity edit, maintain the sidecar enrichment
  queue: where author-supplied first-person lessons, hard-won opinions,
  project history, or personal stakes could later enrich a passage, record the
  location and a candidate question there — while writing the passage itself
  to finished third-person quality, never fabricating the first person.
- Distill the full 44-chapter architecture into 8-12 signature ideas that recur
  deliberately across the reader manuscript, landing page, preface, part
  openings, chapter endings, diagrams, and audio script treatment.
- Treat cuts, demotions, and shorter reader pathways as reader-edition
  selection only unless the live evidence source also changes through a
  manifest or claim decision.

Acceptance bar:

- curated chapters validate against
  `scripts/validate_reader_manuscript_manifest.py`;
- reconciliation report records no hidden claim changes;
- each curated chapter is either outside pending consolidation clusters or
  records a scoped/deferred handoff caveat;
- Human view and generated reader edition still preserve support-state
  boundaries.
- a human-edit handoff packet exists with the current table of contents,
  known repetition debt, unresolved evidence blockers, and per-chapter
  finished-quality status; no chapter is held below finished quality waiting
  for the human edit (2026-07-02 direction).
- the sidecar enrichment queue records optional author-enrichment locations
  without leaving manuscript gaps, and no agent-invented first-person material
  is presented as Corben's experience;
- the reader manuscript has a book-level thesis, part arcs, a named set of
  recurring signature ideas, chapter-specific stakes/payoffs, key-figure
  targets with draft assets, text-equivalent chapter anchors, validator-checked
  reader-manuscript placements, and a sidecar enrichment queue without changing
  evidence boundaries.

Current status:

- `editions/reader_manuscript/v1_0/manifest.json` is in `drafting` status with
  44 active curated chapter records after the Part I, conservative compression,
  intent/contracts, MoECOT, simulation-fidelity, static Context ABI,
  verification/adversarial-review, planning/DAG, semantic-representation fold,
  Compact Generative Systems pass, and RankFold/NeuralFold pass. Retired standalone
  curated drafts are archived under
  `editions/reader_manuscript/v1_0/archive/retired_chapters/` and are
  historical reference only.
- The same manifest now carries a validated `reader_handoff_contract` with one
  book-level thesis, four part arcs, ten recurring signature ideas, ten
  key-figure targets with draft assets, text-equivalent chapter anchors, and
  curated reader-manuscript placements, twelve legacy voice-pass IDs converted
  into the optional sidecar queue
  `editions/reader_manuscript/v1_0/author_enrichment_queue.json`, and
  per-chapter stakes/payoffs. Each former voice-pass record now has a sidecar
  ref, `release_blocking: false`, and `manuscript_gap_status:
  no_gap_finished_third_person`; `scripts/validate_reader_manuscript_manifest.py`
  checks those fields and the matching sidecar records. This closes the
  machine-checkable handoff metadata, optional author-enrichment queue, draft
  key-figure placement, and rendered HTML DOM gap, but it does not approve the
  prose, fabricate authorial experience, visually review the figures as final
  art, or create an edition release artifact.
- `scripts/build_curated_reader_edition.py --check` now validates that the
  tracked curated reader manuscript maps to the 44 active manifest chapters,
  preserves the required release blockers, and can be assembled as Quarto
  source. A local review build rendered successfully to HTML at
  `build/curated_reader_edition/_reader_site/index.html`, and
  `node scripts/validate_reader_html_artifact_browser.js --strict --site
  build/curated_reader_edition/_reader_site --manifest
  build/curated_reader_edition/reader_manifest.json --report
  build/curated_reader_edition/curated_reader_html_browser_report.json` passed
  98 page-view pairs across 49 pages. The build report preserves
  `review_required` status and all 44 `format_artifact_not_reviewed` and
  `reader_release_record_not_created` blockers after source-level
  reconciliation approval.
- The current curated set follows the consolidation-aware curation gate:
  protected standalone chapters may continue toward human-edit readiness;
  chapters inside remaining deferred merge/fold packages must keep scoped
  caveats; executed destinations should carry the folded material as sections,
  not resurrect retired reader chapters.
- The detailed active queue is enforced by
  `editions/reader_manuscript/v1_0/manifest.json`,
  `editions/reader_manuscript/v1_0/chapter_review_matrix.json`, and
  `docs/reader_chapter_review_matrix.md`; the roadmap should not duplicate the
  full chapter catalog.
- `editions/reader_manuscript/v1_0/chapters/asi-is-a-stack-not-a-model.qmd`
  now has a reconciled curated reader prose pass for the current source.
- `docs/curated_reader_asi_stack_prose_pass.md` records the curation scope,
  meaning-preservation checks, non-claims, remaining blockers, and
  reconciliation status for that pass.
- `editions/reader_manuscript/v1_0/chapters/the-efficient-asi-hypothesis.qmd`
  now has a reconciled curated reader prose pass for the current source.
- `docs/curated_reader_efficient_asi_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, and remaining
  blockers plus reconciliation status for that pass.
- `editions/reader_manuscript/v1_0/chapters/system-boundaries-and-authority.qmd`
  now has a reconciled curated reader prose pass for the current source.
- `docs/curated_reader_system_boundaries_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, no-deployed-enforcement boundary, and reconciliation status for
  that pass.
- `editions/reader_manuscript/v1_0/chapters/failure-modes-of-ungoverned-intelligence.qmd`
  now has a reconciled curated reader prose pass for the current source.
- `docs/curated_reader_failure_modes_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, remaining blockers,
  and no scenario-coverage or deployed detection/prevention boundary for that
  pass, plus reconciliation status.
- `editions/reader_manuscript/v1_0/chapters/evidence-states-and-claim-discipline.qmd`
  now has a reconciled curated reader prose pass for the current source.
- `docs/curated_reader_evidence_states_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, no-support-state-movement boundary, and reconciliation status for
  that pass.
- `editions/reader_manuscript/v1_0/chapters/human-intent-as-a-formal-input.qmd`
  now has a reconciled curated reader prose pass for the current source.
- `docs/curated_reader_human_intent_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, remaining blockers,
  current Constitutional Alignment handoff, and reconciliation status for that
  pass.
- `editions/reader_manuscript/v1_0/chapters/intent-to-execution-contracts.qmd`
  now has a curated prose pass for **Command Contracts: From Intent to
  Executable Work** from the generated reader baseline as a drafting source
  only. The former standalone command-contract curated draft is archived as
  historical reference; active reader work routes through this destination
  chapter.
- `docs/curated_reader_intent_execution_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and consolidation caveat for that pass, including no deployed
  intent-to-execution runtime, parser correctness, planner quality, command
  compiler correctness, approval enforcement, runtime adapter safety, tool
  execution, artifact acceptance, replayed vertical slice, behavioral
  execution test, benchmark performance, ReAct reproduction, MoECOT runtime
  reproduction, support-state movement, reader-release approval, or merge/fold
  decision.
- `docs/curated_reader_command_contracts_prose_pass.md` now records archived
  reader-lineage notes for the retired standalone command-contract draft and
  points active curation back to
  `editions/reader_manuscript/v1_0/chapters/intent-to-execution-contracts.qmd`.
- `editions/reader_manuscript/v1_0/chapters/planning-as-a-control-layer.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only. It is the active curated destination for the executed
  planning/DAG package; the archived PlanForge reader draft is lineage, not a
  separate current reader chapter.
- `docs/curated_reader_planning_control_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and consolidation caveat for that pass, including no deployed
  planner behavior, decomposition accuracy, dependency soundness, scheduler
  correctness, context-demand prediction, runtime replanning, dispatch safety,
  parser behavior, tool execution, runtime adapter safety, approval-service
  behavior, ReAct reproduction, Tree-of-Thoughts reproduction, PDDL/SHOP2/TAMP
  implementation, AutoGen reproduction, PlanForge runtime behavior, MoECOT
  runtime behavior, benchmark performance, support-state movement,
  reader-release approval, or additional merge/fold decision.
- `editions/reader_manuscript/v1_0/archive/retired_chapters/planforge-dags-and-intelligence-arbitrage.qmd`
  preserves the retired PlanForge reader draft for history after the executed
  planning/DAG merge.
- `docs/curated_reader_planforge_dag_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and archived reader lineage for that pass, including no deployed
  PlanForge behavior, scheduler correctness, route-selection quality,
  selected-tier adequacy, cost savings, cost-quality dominance, decomposition
  accuracy, dependency inference quality, parser behavior, runtime replanning,
  dispatch safety, tool execution, runtime adapter safety, approval-service
  behavior, AutoGen reproduction, MoECOT runtime behavior, PDDL/SHOP2/TAMP
  implementation, behavior-tree implementation, Tree-of-Thoughts reproduction,
  benchmark performance, support-state movement, reader-release approval, or
  merge/fold decision.
- `editions/reader_manuscript/v1_0/chapters/virtual-context-abi.qmd` now has a
  curated prose pass for the executed merged Context ABI destination. It
  preserves typed page, context cell, and certificate material from the retired
  semantic-pages source chapter without treating the reader manuscript as an
  evidence authority.
- `docs/curated_reader_virtual_context_abi_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and consolidation caveat for that pass, including no deployed VCM
  behavior, resolver correctness, context compiler correctness,
  snapshot-service behavior, adequacy-classifier quality, materialization
  correctness, summary fidelity, contradiction-rate reduction, distractor
  resistance, leak prevention, Digital SCIF behavior, transactional
  memory-store behavior, VCM-Bench performance, model-facing context quality,
  MoECOT runtime behavior, source-interpretation adequacy, support-state
  movement, reader-release approval, or merge/fold decision.
- `editions/reader_manuscript/v1_0/archive/retired_chapters/semantic-pages-context-cells-and-certificates.qmd`
  preserves the historical semantic-pages reader lineage after execution of
  the static Context ABI merge. It is not an active reader-manuscript chapter
  and should not receive further curation unless the retired chapter is later
  restored by an explicit manifest decision.
- `docs/curated_reader_semantic_pages_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and consolidation caveat for that pass, including no semantic
  summary-fidelity evaluation, certificate-truthfulness checking,
  omission-completeness checking, open-domain autoformalization,
  source-interpretation adequacy, VCM-Bench performance, model-facing context
  quality, leak prevention, contradiction-rate reduction, Context Engineer
  benchmark reproduction, deployed Digital SCIF behavior, source-reported
  benchmark reproduction, support-state movement, reader-release approval, or
  merge/fold decision.
- `editions/reader_manuscript/v1_0/chapters/constitutional-alignment-substrate.qmd`
  is now the active curated destination for **Constitutional Alignment:
  Agency, Dignity, and Corrigibility**. The former
  `agency-dignity-and-corrigibility` reader draft is archived as historical
  lineage, active reader work must stay on the destination chapter, and the
  current destination chapter is reconciled for prose meaning.
- `editions/reader_manuscript/v1_0/chapters/moral-uncertainty-and-value-conflict.qmd`
  is now the active curated destination for **Moral Uncertainty, Value
  Conflict, and Contestable Governance**. The former
  `governance-rights-fork-exit-and-audit` reader draft is archived as
  historical lineage, active reader work must stay on the destination chapter,
  and the current destination chapter is reconciled for prose meaning.
- `editions/reader_manuscript/v1_0/chapters/security-kernel-and-digital-scifs.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_security_kernel_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and no deployed-security, sandbox-isolation, side-channel,
  prompt-injection-containment, OWASP-conformance, or NIST-zero-trust
  implementation boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/stable-capability-fields.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_stable_capability_fields_prose_pass.md` records the
  curation scope, reader promise, meaning-preservation checks, non-claims,
  remaining blockers, and no deployed route-validation, authority-enforcement,
  replacement-safety, rollback-execution, SLSA-workflow, SemVer-checker,
  object-capability-implementation, or MoECOT-runtime-reproduction boundary
  for that pass.
- `editions/reader_manuscript/v1_0/chapters/capability-replacement-and-rollback.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_capability_replacement_prose_pass.md` records the
  curation scope, reader promise, meaning-preservation checks, non-claims,
  remaining blockers, and no deployed replacement-behavior, real-regression-
  suite-quality, monitor-window-success, evaluator-integrity-enforcement,
  authority-enforcement, rollback-execution, MoECOT-runtime-reproduction, or
  implemented-corrigibility boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/routing-heads-and-specialist-cores.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_routing_heads_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, the now-executed MoECOT Runtime Crosswalk fold, and no
  routing-accuracy, learned-router-quality, specialist-adequacy,
  deployed-authority-enforcement, route-quality-dominance, MoECOT-runtime,
  current-Theseus-runtime, or release boundary for that pass.
- `editions/reader_manuscript/v1_0/archive/retired_chapters/moecot-runtime-and-multi-core-orchestration.qmd`
  preserves the standalone MoECOT curated reader draft as historical reference
  only. Active reader work now targets
  `routing-heads-and-specialist-cores` and its folded MoECOT Runtime Crosswalk.
- `docs/curated_reader_moecot_runtime_prose_pass.md` remains the historical
  curation record for that archived draft, including no MoECOT runtime
  execution, benchmark reproduction, replay correctness, current report-bundle
  verification, worker/core balance trace, isolation result, specialist
  adequacy, routing quality, model quality, current Theseus runtime behavior,
  support-state movement, or reader-release approval.
- `editions/reader_manuscript/v1_0/chapters/readiness-gates-residual-escrow-and-quarantine.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_readiness_gates_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and no deployed readiness-engine, residual-ledger-storage,
  benchmark-quality, live-quarantine-routing, gate-expiry-enforcement,
  live-rerouting, current-Theseus-runtime, MoECOT-replay, or release boundary
  for that pass.
- `editions/reader_manuscript/v1_0/chapters/cognitive-compilation-and-semantic-ir.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only. This chapter remains protected as a standalone
  semantic-IR and lowering chapter outside pending merge packages.
- `docs/curated_reader_cognitive_compilation_prose_pass.md` records the
  curation scope, reader promise, meaning-preservation checks, non-claims,
  remaining blockers, and no source-plan parser, target-lowering correctness,
  compiler correctness, localized-repair performance, artifact-validator
  adequacy, quality improvement, cost improvement, deployed compiler behavior,
  or support-state movement boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/context-transactions-snapshots-mounts-and-taint.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only. This chapter remains protected as a standalone
  transaction-memory chapter outside the pending static context ABI merge.
- `docs/curated_reader_context_transactions_prose_pass.md` records the
  curation scope, reader promise, meaning-preservation checks, non-claims,
  remaining blockers, and no deployed memory-store, read-your-writes,
  branch-isolation, mount-visibility, replay, poisoning-resistance,
  side-channel-defense, VCM-conformance, Digital-SCIF-implementation,
  context-manager-benchmark, or support-state movement boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/verification-bandwidth-and-context-adequacy.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only. This chapter remains protected as a standalone
  generation-versus-verification and context-adequacy chapter outside the
  pending static context ABI merge.
- `docs/curated_reader_verification_bandwidth_prose_pass.md` records the
  curation scope, reader promise, meaning-preservation checks, non-claims,
  remaining blockers, and no measured model verification-bandwidth,
  contradiction-rate, distractor-resistance, summary-fidelity,
  adequacy-classifier, deployed-VCM, deployed-escalation, or support-state
  movement boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/claim-ledgers-and-belief-revision.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_claim_ledgers_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, remaining blockers,
  and no claim-extraction, contradiction-detection, semantic-equivalence,
  citation-correctness, belief-engine, deployed-epistemic-correctness, or
  support-state-movement boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/spinoza-verification-and-proof-carrying-claims.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only. It is the active curated destination for the executed
  verification/adversarial-review package; the archived UAT reader draft is
  lineage, not a separate current reader chapter.
- `docs/curated_reader_spinoza_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, remaining blockers,
  and consolidation caveat for that pass, including no theorem-validity result,
  verifier-quality result, citation-accuracy result, semantic-equivalence
  result, open-domain autoformalization, proof generation,
  source-interpretation adequacy, Proof-Carrying Code implementation,
  GenesisCode implementation, TreeLLM implementation, runtime behavior,
  deployed contradiction detection, whole-system epistemic correctness,
  support-state movement, reader-release approval, or additional merge/fold
  decision.
- `editions/reader_manuscript/v1_0/chapters/unified-adaptive-tribunal-and-adversarial-review.qmd`
  is no longer an active curated chapter after the executed
  verification/adversarial-review merge; the UAT prose pass remains historical
  reader-lineage context only.
- `docs/curated_reader_uat_prose_pass.md` records the curation scope, reader
  promise, meaning-preservation checks, non-claims, remaining blockers, and
  archived reader lineage for that pass, including no reviewer-independence
  result, adversarial-probe-quality result, consensus-quality result,
  verdict-correctness result, human-adjudication-quality result,
  tribunal-quality result, deployed-contestability result,
  institutional-adequacy result, source-interpretation adequacy, Talos runtime
  behavior, Spinoza verifier behavior, verification-bandwidth benchmark
  behavior, Coherence Exchange implementation, multi-reviewer UAT pipeline
  behavior, support-state movement, reader-release approval, or merge/fold
  decision.
- `editions/reader_manuscript/v1_0/chapters/labor-os-and-typed-jobs.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only. This chapter remains protected as a standalone
  execution-boundary chapter outside pending merge packages.
- `docs/curated_reader_labor_os_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, remaining blockers,
  and no scheduler, permission-service, approval-service, adapter-runner,
  replay-system, Talos-runtime, MoECOT-runtime, AutoGen, SWE-bench, benchmark,
  security-result, or support-state movement boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/artifact-graphs-audit-logs-and-replay.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only. This chapter remains protected as a standalone
  execution-continuity and artifact-evidence chapter outside pending merge
  packages.
- `docs/curated_reader_artifact_graphs_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and no artifact-graph-service, replay-engine, audit-reconstruction,
  produced-artifact-completeness, provenance-completeness, benchmark,
  security-result, proof-carrying-code, SWE-bench, AutoGen, MoECOT-runtime, or
  support-state movement boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/recursive-self-improvement-boundaries.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_recursive_self_improvement_prose_pass.md` records the
  curation scope, reader promise, meaning-preservation checks, non-claims, and
  remaining blockers for that pass.
- `editions/reader_manuscript/v1_0/chapters/circle-calculus-and-proof-carrying-ai-contracts.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_circle_contracts_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, and remaining
  blockers for that pass.
- `editions/reader_manuscript/v1_0/chapters/executable-specifications-and-lean-proof-envelope.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_executable_specs_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, and remaining
  blockers for that pass.
- `editions/reader_manuscript/v1_0/chapters/artifact-steward-agents-and-living-project-governance.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_artifact_steward_prose_pass.md` records the curation
  scope, meaning-preservation checks, non-claims, and remaining blockers for
  that pass.
- `editions/reader_manuscript/v1_0/chapters/open-research-agenda-and-bibliography-plan.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_open_research_agenda_prose_pass.md` records the
  curation scope, reader promise, meaning-preservation checks, non-claims,
  remaining blockers, and no citation-normalization, external-literature-
  completeness, benchmark-reproduction, artifact-reproduction, live-new-paper-
  triage, public-release-permission, external-review, or support-state movement
  boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/fast-generation-architectures.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_fast_generation_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and no local fast-decoding, mode-selector, useful-solution-per-
  second, accepted-token, external-method reproduction, serving-throughput,
  KV-cache audit, quality-improvement, memory-savings, route-promotion, or
  support-state movement boundary for that pass.
- The twelve dense companion-note candidates now have drafting companion notes
  under `editions/reader_manuscript/v1_0/companion_notes/`: Planning controlled
  dispatch, Routing Heads route leases, Personal Compute Hives policy-first
  placement, Compact Generative Systems residual honesty, Fast Generation
  accepted-output accounting, Resource Economics protected-cost lanes, Circle
  proof receipts, CoilRA cyclic-substrate adoption, executable-specification
  proof lanes, Policy Optimization behavior-change leases, artifact-steward
  project objects, and Project Theseus report-first evidence. These notes
  support e-reader and audio treatment without moving meaning-critical
  planning, routing, hive, compression, speed, resource, proof, cyclic-substrate,
  policy, governance, implementation-reference, release, or non-claim limits
  out of the reader spine.
- `editions/reader_manuscript/v1_0/reconciliation_report.md` records the
  chapter-level reconciliation statuses, and
  `docs/reader_chapter_reconciliation_approval.md` records source-level
  reconciliation approval for all 44 current curated chapters. The chapter
  records still keep `reader_release_record_not_created` and
  `format_artifact_not_reviewed` blockers active.
- No curated reader chapter is release-approved, and generated reader HTML
  remains the only reviewed reader artifact. The curated reader manuscript now
  has a renderable local HTML review path, but that path is not a release
  record, not format approval, and not support-state movement.
- The previous Compact Generative Systems and RankFold/NeuralFold gaps now have
  curated reader files plus prose-pass reconciliation notes. This closes the
  active-file coverage gap, but it does not approve the reader
  manuscript, artifact formats, support-state movement, codec claims, or semantic
  representation claims.

### Milestone 7.5 - Authorial Voice, Distillation, And Narrative Arc

Goal: make the human-reader book feel like an authored technical work rather
than a validated architecture template, while preserving the live book as the
canonical evidence surface.

Tasks:

- State the single book thesis in first-paragraph language and propagate that
  thesis through the preface, landing page, reader opening, part openings, and
  final chapter without making a stronger evidence claim.
- Select 8-12 signature ideas that the book should make memorable, such as
  governed authority, evidence laundering, support-state discipline, stack-not-
  model, verification bandwidth, residual honesty, stable capability fields,
  proof-carrying claims, and bounded self-improvement. Hone their wording in
  reader prose, chapter endings, diagrams, and audio treatment so they become
  reusable concepts rather than a glossary dump.
- Build a part-level narrative arc:
  - Part I: why unbounded intelligence fails as a systems object;
  - Part II: how intent becomes governed work;
  - Part III: how efficiency and representation improve without losing
    evidence;
  - Part IV: how the system proves, ships, reviews, and revises itself.
- Replace template-like reader openings and closings with chapter-specific
  stakes, examples, tensions, and payoffs. Keep repeated evidence boundaries in
  compact form, but stop repeating the same rhetorical motion.
- Write every chapter's conviction, stakes, and payoff to finished quality in
  third person; never invent first-person experience. Where Corben's lived
  project experience could later enrich a passage, record the location and a
  candidate question in the sidecar enrichment queue — but the prose at that
  location must already stand as finished without it (2026-07-02 direction).
- Identify any chapter material that belongs in the live AI/research view but
  should be shortened, moved to companion notes, or summarized in the human
  reader path. This is reader-edition selection, not live-source deletion.
- Tie figure craft to the narrative arc: key figures should carry the book's
  core ideas visually rather than merely restating section headings. The
  current ten reader-handoff figure targets now have draft SVG assets,
  text-equivalent chapter anchors, and validator-checked live/reader placements;
  the remaining work is visual polish, format-specific inspection, and release
  review.

Acceptance bar:

- The reader manuscript has one explicit thesis, part arcs, recurring
  signature ideas, chapter-specific stakes/payoffs, key-figure targets with
  draft assets, text-equivalent chapter anchors, and validator-checked
  reader-manuscript placements — realized in the prose itself, at finished
  quality, with zero empty slots or placeholders (2026-07-02 direction).
- The optional enrichment queue is a sidecar record of locations where
  author-supplied first-person material could later be added; the manuscript
  is complete and finished without any of them.
- No agent-generated prose claims Corben's personal experience, intent, or
  belief unless the source is author-supplied or explicitly approved.
- The live book still owns claim meaning, support states, source boundaries,
  proof/test status, implementation horizons, and release records.
- The craft pass improves reader flow without weakening non-claims, hiding
  evidence limits, or implying that argument-level architecture has been
  validated.

Current status:

- Partially executed. The reader-manuscript manifest now records and validates
  the thesis, part arcs, recurring signature ideas, key-figure targets with
  draft assets, text-equivalent chapter anchors, validator-checked
  reader-manuscript placements, chapter-level stakes/payoffs, and twelve
  optional author-enrichment sidecar entries converted from the legacy
  voice-pass slots. This is handoff and enrichment structure only; it is not
  source evidence, external review, support-state evidence, final figure
  review, authorial approval, release approval, or permission to fabricate
  first-person material.
- The current curated reader manuscript remains pre-release and `drafting` as
  an edition status, but chapter-level prose reconciliation is complete across
  all 44 active records. Per the 2026-07-02 direction, the enrichment queue
  stays a sidecar, the manuscript carries no empty author-voice slots, and
  graduation out of `drafting` now waits on release-quality continuity,
  format-specific review, exact artifacts, and an edition release record, not
  author-supplied voice language.
- `docs/curated_reader_html_artifact_browser_review.md` now records a full
  local browser viability review of the tracked curated reader manuscript
  rendered through
  `build/curated_reader_edition/format_artifacts/html/_reader_site`: 49 pages,
  two viewports, 98 of 98 page-view pairs passing, 10 rendered key figures
  across 20 desktop/mobile figure page-view pairs with 0 failures, exact
  ignored-snapshot
  digest
  `2ca82608207741a56a861da7d32f4d8c7e7a25dc390df3836dca11560b19ce34`, and
  all 44 `format_artifact_not_reviewed` and
  `reader_release_record_not_created` blockers preserved after source-level
  reconciliation approval. This closes a render/browser-viability uncertainty for
  the curated manuscript, not the release-quality continuity, format-review,
  figure-artifact, e-reader/audio, or edition-release gates.
- The ten draft key figures are now embedded/adapted into the curated reader
  manuscript where they serve the reader arc, not only the live AI/research
  chapters. Each placement carries a caption, alt text, and a non-claim
  boundary; `scripts/validate_reader_key_figures.py` checks the source state,
  `scripts/validate_reader_key_figure_contrast.py` checks source-SVG contrast
  and readability, and `scripts/validate_reader_key_figure_html_probe.py`
  checks rendered curated-reader HTML DOM presence for all ten, and
  `scripts/validate_reader_key_figure_format_probe.py` checks the current
  ignored EPUB/DOCX/PDF packages for key-figure title/stem/caption survival.
  `scripts/validate_reader_key_figure_geometry.py` records
  `editions/reader_manuscript/v1_0/key_figure_geometry_manifest.json` and
  `docs/reader_key_figure_geometry_review.md`: 10 content-bound checks, 10
  text-anchor checks, minimum visible text nodes 25, minimum visible rectangles
  7, minimum visible connector paths 8, and 22.0 px minimum content edge
  margin. This closes CI-friendly source-geometry review only, not raster
  review, manual aesthetic judgment, e-reader/app review, final figure-art
  approval, or reader release approval.
  `scripts/validate_reader_visual_identity.py` now records
  `editions/reader_manuscript/v1_0/visual_identity_manifest.json` and
  `docs/reader_visual_identity_review.md`: 10 key figures, 54 combined colors,
  5 non-neutral color families, minimum text contrast ratio 5.19, minimum
  flow-line contrast ratio 3.96, minimum marker contrast ratio 3.96, and
  minimum SVG text size 15 px. This closes source-level visual-system review
  only, not manual aesthetic judgment, e-reader/app review, final figure-art
  approval, or reader release approval. Remaining work is manual rendered
  visual inspection, visual figure polish, real e-reader/app/DOCX inspection,
  final PDF figure/readability release review, audio-specific inspection, and
  release review before any human-review-ready figure-artifact claim.
- `scripts/validate_reader_accessibility_navigation.py` now records
  `editions/reader_manuscript/v1_0/accessibility_navigation_manifest.json` and
  `docs/reader_accessibility_navigation_review.md`: 44 curated reader chapters,
  44 one-H1 chapter sources, 44 handoff sections, 10 draft figure alt texts, 10
  figure boundary paragraphs, 0 live-marker leaks, and 0 raw core-claim marker
  leaks. This closes source-level accessibility/navigation review only, not
  keyboard-only review, screen-reader review, WCAG conformance, e-reader review,
  audiobook review, final figure-artifact approval, or reader release approval.
- `scripts/validate_reader_keyboard_navigation.py` now records
  `editions/reader_manuscript/v1_0/keyboard_navigation_manifest.json` and
  `docs/reader_keyboard_navigation_review.md`: 49 curated reader HTML pages, 98
  desktop/mobile page-view pairs, 0 failed pairs, 98 skip-link activations, 98
  main-content routes, 98 navigation reach observations, 98 search reach
  observations, and 0 keyboard-trap candidates. This closes automated local
  Chromium keyboard traversal review only, not manual keyboard-only review,
  screen-reader review, WCAG conformance, e-reader review, audiobook review,
  final figure-artifact approval, or reader release approval.
- `scripts/validate_reader_keyboard_only_decision.py` now records
  `editions/reader_manuscript/v1_0/keyboard_only_decision_manifest.json` and
  `docs/reader_keyboard_only_decision.md`: `accepted_keyboard_only_evidence_for_release_preparation`,
  98 keyboard page-view pairs, 0 keyboard failures, 0 keyboard-trap candidates,
  98 accessibility-tree page-view pairs, 0 unnamed interactive elements, and 0
  duplicate-ID hits. This clears only `manual_keyboard_only_review_not_completed`
  for the current curated reader HTML candidate; screen-reader review, WCAG
  conformance, reader release approval, e-reader/application release, and audio
  release blockers remain open.
- `scripts/validate_reader_accessibility_tree.py` now records
  `editions/reader_manuscript/v1_0/accessibility_tree_manifest.json` and
  `docs/reader_accessibility_tree_review.md`: 49 curated reader HTML pages, 98
  desktop/mobile page-view pairs, 0 failed pairs, 98 accessibility-tree
  page-view pairs, 0 unnamed interactive elements, 0 image alt failures, 0
  table-header failures, and 0 duplicate-ID hits. This closes automated local
  Chromium accessibility-tree release-preparation review only, not manual
  keyboard-only review, screen-reader review, WCAG conformance, e-reader
  review, audiobook review, final figure-artifact approval, or reader release
  approval.
- `scripts/validate_reader_key_figure_raster_probe.py` now records
  `editions/reader_manuscript/v1_0/key_figure_raster_manifest.json` and
  `docs/reader_key_figure_raster_review.md`: 10 generated PNG fallbacks, 10
  standard 1200 x 760 canvases, 99.954% minimum opaque pixel coverage, 27.64
  minimum luminance standard deviation, 116 minimum quantized colors, and
  per-artifact SHA-256 digests. This closes automated raster fallback smoke
  review only, not manual aesthetic review, e-reader visual review, DOCX/PDF
  application review, final figure-artifact approval, or reader release
  approval.
- `scripts/validate_reader_key_figure_epub_layout.py` now records
  `editions/reader_manuscript/v1_0/key_figure_epub_layout_manifest.json` and
  `docs/reader_key_figure_epub_layout_review.md`: 10 key-figure XHTML entries,
  20 desktop/e-reader-like browser page-view pairs, 0 failed pairs, 5,476
  minimum body text characters, 23 minimum alt-text words, 10 px maximum
  horizontal overflow, 0 image failures, 10 figure boundaries, and 10 release
  boundaries. This closes automated local EPUB XHTML key-figure browser-report
  layout review only, not dedicated e-reader device review, e-reader
  application approval, final figure-artifact approval, visual identity
  approval, or reader release approval.
- `scripts/validate_reader_key_figure_pdf_layout.py` now records
  `editions/reader_manuscript/v1_0/key_figure_pdf_layout_manifest.json` and
  `docs/reader_key_figure_pdf_layout_review.md`: 10 key-figure caption pages,
  10 caption-page rasters, 10 standard 612 x 792 page rasters, 165.878 pt
  minimum caption margin, 3.36% minimum page ink, 0.0% maximum near-edge ink,
  and 14.2 minimum luminance standard deviation. This closes automated local
  PDF key-figure caption-page layout smoke review only, not manual
  page-by-page PDF review, final figure-artifact approval,
  visual identity approval, or reader release approval.
- `scripts/validate_reader_key_figure_docx_layout.py` now records
  `editions/reader_manuscript/v1_0/key_figure_docx_layout_manifest.json` and
  `docs/reader_key_figure_docx_layout_review.md`: 10 key-figure title pages,
  10 title-page rasters, 10 standard 612 x 792 page rasters, 72.1 pt minimum
  title margin, 9.53% minimum page ink, 0.0% maximum near-edge ink, and 37.95
  minimum luminance standard deviation. This closes automated local
  DOCX-to-PDF key-figure title-page layout smoke review only, not Word review,
  LibreOffice GUI review, Google Docs review, manual document review, final
  figure-artifact approval, visual identity approval, or reader release
  approval.
- `scripts/validate_reader_final_figure_artifact_review.py` now records
  `editions/reader_manuscript/v1_0/final_figure_artifact_review_manifest.json`
  and `docs/reader_final_figure_artifact_review.md`: 10 key figures, 10
  content-bound checks, 10 alt texts, 10 PNG raster fallbacks, 20 EPUB layout
  page-view pairs with 0 failures, 10 PDF caption/raster pages, and 10 DOCX
  title/raster pages. This aggregate review clears only the current
  `final_figure_artifact_review_not_completed` blocker; it does not approve
  the reader edition, e-reader/application review, manual keyboard-only
  review, screen-reader review, WCAG conformance, audio, publication, or any
  support-state movement.
- `scripts/validate_reader_docx_application_decision.py` now records
  `editions/reader_manuscript/v1_0/docx_application_decision_manifest.json`
  and `docs/reader_docx_application_decision.md`: the current curated DOCX
  release-preparation gate accepts repaired DOCX XML/relationship checks,
  LibreOffice headless Writer conversion/raster evidence, DOCX key-figure
  layout evidence, the final figure-artifact review, and the Pages-readable
  text fallback as enough to clear only
  `docx_application_review_not_completed`. This does not claim Word,
  LibreOffice GUI, or Google Docs approval and does not approve DOCX
  publication or reader release.
- `docs/curated_reader_format_artifact_probe.md` and
  `editions/reader_manuscript/v1_0/curated_format_probe_manifest.json` now
  record that the tracked curated reader manuscript rendered locally to HTML,
  EPUB, DOCX, and PDF and passed structural inspection: 49 HTML files, 44
  chapter HTML files, 52 EPUB XHTML entries, 61 DOCX PNG media entries, and a
  506-page PDF with sample pages rendered to PNG. The curated DOCX/PDF renderer
  now generates ten temporary PNG fallbacks from the tracked SVG key figures
  inside the ignored build workspace, and the PDF renderer also generates 50
  temporary Chrome-screenshot Mermaid fallbacks from the rendered HTML pages.
  It restores the source workspace after rendering, preserves browser-rendered
  Mermaid labels in PDF, and eliminates SVG-conversion warnings. The repaired
  EPUB package audit now checks all 52 XHTML entries, 49 packaged content XHTML
  entries, OPF/nav counts, required reader text markers, live-marker leakage,
  raw core-claim marker leakage, and internal links with 0 unresolved internal
  hrefs, 0 XML parse errors, 0 bare class attributes, and 0
  paragraph-wrapped figure tag hits. The Chromium EPUB XHTML browser review now
  checks 104 page-view pairs with 0 failures and 0 px maximum element overflow,
  and the EPUB key-figure layout probe checks 10 key-figure XHTML entries, 20
  desktop/e-reader-like page-view pairs, 0 key-figure browser failures, 10 px
  maximum horizontal overflow, and 0 image failures. The Apple Books EPUB
  application review now opens the repaired EPUB digest, renders chapter 1
  without the earlier XML error banner, advances to a figure page, opens the
  table of contents, and clears only `app_or_ereader_review_not_completed`.
  The repaired DOCX package audit now checks document XML, required
  reader text markers, media entries, relationship targets, live-marker
  leakage, raw core-claim marker leakage, and internal relationship targets with
  0 raw `.qmd` relationship targets and 0 unresolved internal relationship
  targets. The LibreOffice headless DOCX review now converts the repaired DOCX
  to a 504-page tagged PDF, checks 1,028,304 extracted text characters,
  raster-checks 504 converted pages, and records 0 blank, 0 low-ink, and 0
  near-edge converted-page rasters while preserving Word, LibreOffice GUI, or
  Google Docs review as release blockers. The DOCX key-figure layout probe
  checks 10 title pages, 10 title-page rasters, 72.1 pt minimum title margin,
  9.53% minimum page ink, 0.0% maximum near-edge ink, and 37.95 minimum
  luminance standard deviation while still preserving Word, LibreOffice GUI,
  Google Docs, and manual document review as release blockers. The PDF visual raster audit now
  renders all 506 pages at 72 dpi with
  0 blank pages, 1 low-ink page, and 0 near-edge pages. The PDF extracted-text
  reading-flow review now checks 506 text pages, 506 nonempty text pages, 44
  ordered chapter headings, 3 ordered appendix headings, and 0 replacement
  characters. The PDF page-by-page release-preparation review now checks 506
  page rows, 506 text pages, 506 word-box pages, 506 raster pages, 0 failed
  pages, 0 blank pages, 0 near-edge pages, 0 out-of-bounds word-box pages, and
  one accepted low-ink page, closing the current candidate's
  `manual_pdf_page_by_page_review_not_completed` blocker while preserving
  reader release approval. The aggregate final figure-artifact review checks
  the ten key figures across source, raster, EPUB, PDF, and DOCX evidence and
  clears only `final_figure_artifact_review_not_completed`. The PDF
  key-figure layout probe checks 10 caption
  pages, 10 caption-page rasters, 165.878 pt minimum caption margin, 3.36%
  minimum page ink, 0.0% maximum near-edge ink, and 14.2 minimum luminance
  standard deviation. The Chromium PDF viewer smoke review records 2 nonblank
  viewer screenshots and 4.479% changed pixels after scroll. EPUB publication,
  DOCX publication, PDF, and audio artifacts still remain unapproved until
  reader release approval, audio file generation, pronunciation/listening
  review, chapter-marker timecoding, audio-embedded EPUB packaging, and an
  edition release record exist; the separate DOCX application-evidence decision
  closes only the DOCX application-review blocker, the separate audio narration
  treatment review closes only the script-level narration-treatment blocker,
  and the separate audio metadata review closes only the metadata blocker.
- Add a chapter-length and evidence-placement pass before Corben's human
  review. The biggest live chapters should keep evidence boundaries intact but
  move bulky tables, validator minutiae, or repeated caveats into appendices,
  companion notes, or live-book-only sections where that improves ordinary
  reading. Planning, Routing Heads, Personal Compute Hives, Compact Generative
  Systems, Fast Generation, Resource Economics, Circle, CoilRA, Executable
  Specifications, Policy Optimization, Artifact Steward Agents, and Project
  Theseus now have drafting companion-note routes for e-reader/audio density
  support. Future watchlist work should inspect any newly enlarged chapter that
  crosses the same density threshold, but the named current watchlist no longer
  has a missing companion-routing decision.

### Milestone 8 - Visual, Ebook, PDF, DOCX, And Audio Quality

Goal: make the major-version human artifacts pleasant, navigable, and honest.

Tasks:

- Continue using Human view for casual web readers.
- Treat reader HTML as the reviewed baseline artifact until EPUB, DOCX, PDF,
  and audio have exact release records.
- Add chapter-level diagrams only when they clarify mechanisms, not as
  decoration.
- Create a small visual identity for the book: consistent type scale,
  figure-treatment rules, color/contrast choices, source-note styling, and
  diagram conventions that work on the live site and in exported reader
  artifacts.
- Upgrade the most important architecture figures beyond default Mermaid when
  the figure carries the thesis, a layer contract, an evidence lifecycle, or a
  reader-navigation burden. Use accessible HTML/SVG/Mermaid or generated
  bitmap figures only when they remain inspectable and have text equivalents.
- For EPUB:
  - keep the Apple Books application review current for the exact repaired
    EPUB digest, and rerun it after EPUB-affecting changes;
  - check navigation, source cards, images, tables, and long code/proof blocks;
  - record the exact artifact digest.
- For PDF:
  - complete page-by-page or systematic sampled layout review;
  - check diagram overflow, table breaks, source appendices, and mobile-unfriendly
    artifacts;
  - keep print claims out unless actual print review happens.
- For DOCX:
  - complete application-level review, not only structural conversion.
- For audio:
  - build scripts from curated reader prose, not the raw AI/research scaffold;
  - add pronunciation and equation/proof reading rules;
  - keep companion notes separate from the main listening flow;
  - record exact MP3/M4B/audio-embedded EPUB artifacts only after generation and
    review.

Acceptance bar:

- no format row is marked release-approved without an edition release record;
- audio scripts preserve implementation horizons and evidence boundaries;
- visual assets have text equivalents or walkthrough notes;
- the key figures and public theme look intentionally authored rather than
  merely generated by default Quarto styling.

Current status:

- `scripts/build_audio_script.py --check` generates 49 review-script files
  from the tracked curated reader manuscript and verifies that every chapter
  script preserves both implementation-horizon sections.
- The tracked curated reader manuscript now has a full local HTML browser
  viability review recorded in
  `docs/curated_reader_html_artifact_browser_review.md`: the rendered ignored
  snapshot under
  `build/curated_reader_edition/format_artifacts/html/_reader_site` opened 49
  pages across desktop and mobile widths, passed 98 of 98 page-view checks,
  and has deterministic directory digest
  `2ca82608207741a56a861da7d32f4d8c7e7a25dc390df3836dca11560b19ce34`. This
  is review input for release-quality artifact work; it does not mark the
  curated reader edition, refreshed HTML, EPUB, DOCX, PDF, e-reader, or audio
  release-approved.
- Ten draft key-figure assets tied to the reader handoff contract now exist and
  are embedded in live chapters and the curated reader manuscript:
  `asi-stack-control-plane.svg`,
  `authority-to-effect-path.svg`, `evidence-state-ladder.svg`,
  `intent-to-artifact-trace.svg`, `context-transaction-lifecycle.svg`,
  `readiness-residual-quarantine-map.svg`,
  `route-selection-budget-tradeoff.svg`,
  `compression-and-generation-acceptance.svg`,
  `cyclic-substrate-adoption-gate.svg`, and
  `living-book-release-pipeline.svg`. They have text-equivalent live-chapter
  reading notes plus reader-manuscript captions, alt text, and non-claim
  boundaries checked by `scripts/validate_reader_key_figures.py`, source-SVG
  contrast/readability checked by
  `scripts/validate_reader_key_figure_contrast.py`, package/text survival in
  the current ignored EPUB/DOCX/PDF artifacts checked by
  `scripts/validate_reader_key_figure_format_probe.py`, source-geometry checked
  by `scripts/validate_reader_key_figure_geometry.py` with 10 content-bound
  checks, 10 text-anchor checks, and 22.0 px minimum content edge margin, and
  source-level visual identity checked by `scripts/validate_reader_visual_identity.py` with
  10 key figures, 54 combined colors, 5 non-neutral color families, minimum
  text contrast ratio 5.19, minimum flow-line contrast ratio 3.96, minimum
  marker contrast ratio 3.96, and minimum SVG text size 15 px, and automated
  PNG fallback raster review checked by
  `scripts/validate_reader_key_figure_raster_probe.py` with 10 standard 1200 x
  760 canvases, 99.954% minimum opaque pixel coverage, 27.64 minimum luminance
  standard deviation, and 116 minimum quantized colors, and EPUB key-figure
  XHTML layout checked by `scripts/validate_reader_key_figure_epub_layout.py`
  with 10 XHTML entries, 20 desktop/e-reader-like browser page-view pairs, 0
  failed pairs, 10 px maximum horizontal overflow, and 0 image failures, and PDF key-figure
  caption-page layout checked by
  `scripts/validate_reader_key_figure_pdf_layout.py` with 10 caption pages, 10
  caption-page rasters, 165.878 pt minimum caption margin, 3.36% minimum page
  ink, 0.0% maximum near-edge ink, and 14.2 minimum luminance standard
  deviation, and DOCX-to-PDF key-figure title-page layout checked by
  `scripts/validate_reader_key_figure_docx_layout.py` with 10 title pages, 10
  title-page rasters, 72.1 pt minimum title margin, 9.53% minimum page ink,
  0.0% maximum near-edge ink, and 37.95 minimum luminance standard deviation.
  The results are
  recorded in `docs/reader_key_figure_artifact_review.md`,
  `docs/reader_key_figure_format_probe.md`, and
  `docs/reader_key_figure_geometry_review.md`, and
  `docs/reader_visual_identity_review.md`, and
  `docs/reader_key_figure_raster_review.md`, and
  `docs/reader_key_figure_epub_layout_review.md`, and
  `docs/reader_key_figure_pdf_layout_review.md`, and
  `docs/reader_key_figure_docx_layout_review.md`. They remain
  `draft_not_release_reviewed` with no new
  support-state, enforcement, security, proof, test, external-review, or
  artifact-release effect. Current blocker: manual aesthetic judgment, figure
  polish, e-reader visual review beyond the Apple Books smoke/application path
  where release scope demands it, final PDF figure/readability release review,
  and release review still need to happen before any approved reader-figure
  artifact claim. Word/LibreOffice GUI/Google Docs review remains optional
  stronger evidence, not a claimed completed review.
- `docs/reader_accessibility_navigation_review.md` and
  `editions/reader_manuscript/v1_0/accessibility_navigation_manifest.json`
  now record a source-level reader accessibility/navigation review for the
  curated manuscript: 44 chapter files, 44 one-H1 chapters, 44 handoff
  sections, 10 draft figure alt texts, 10 figure boundary paragraphs, 0
  live-marker leaks, and 0 raw core-claim marker leaks. This is a source gate
  only; it does not itself clear keyboard-only, screen-reader, WCAG conformance,
  or release approval.
- `docs/reader_keyboard_navigation_review.md`,
  `editions/reader_manuscript/v1_0/keyboard_navigation_manifest.json`,
  `docs/reader_accessibility_tree_review.md`, and
  `editions/reader_manuscript/v1_0/accessibility_tree_manifest.json` now
  record automated rendered-HTML release-preparation checks for the current
  curated reader artifact: 98 desktop/mobile page-view pairs, 0 keyboard
  traversal failures, 98 skip-link activations, 98 main-content routes, 0
  keyboard-trap candidates, 98 accessibility-tree page-view pairs, 0 unnamed
  interactive elements, 0 image-alt failures, 0 table-header failures, and 0
  duplicate-ID hits. These automated Chromium checks feed the separate
  keyboard-only evidence decision, which clears only `manual_keyboard_only_review_not_completed`;
  screen-reader review, WCAG conformance review, e-reader review, audiobook
  review, and reader release approval remain open.
- The generated audio workspace now includes `pronunciation_glossary.md` and
  `proof_equation_reading_rules.md`. The latter is a required review artifact
  for theorem IDs, equations, support states, proof statuses, schema fields,
  hashes, and negative controls; it does not approve narration or any audio
  artifact.
- The generated audio companion notes now route the ten tracked key-figure
  spoken-summary rows from
  `editions/reader_manuscript/v1_0/companion_notes/key-figures.md` into the
  ignored audio review workspace, with drafting status and non-claim boundaries
  preserved. This is audio/e-reader review scaffolding, not narration approval
  or final figure-artifact approval.
- `editions/reader_manuscript/v1_0/audio_script_probe_manifest.json`,
  `docs/reader_audio_script_probe_manifest.md`, and
  `scripts/validate_reader_audio_script_probe_manifest.py` now record and
  validate the tracked local audio-script probe: 49 script files, preserved
  implementation horizons, 5 table treatment notes, 50 Mermaid diagram notes,
  11 image notes, 10 key-figure spoken-summary rows, and MP3/M4B/
  audio-embedded EPUB targets still marked `target_not_generated`.
  `scripts/build_audio_script.py` now emits scripts in manifest reading order
  rather than alphabetical filesystem order, and
  `scripts/validate_reader_audio_script_reading_flow.py` records the automated
  reading-flow check: 49 script files, 49 ordered marker rows, 49 untimecoded
  `TBD` marker rows, 66 narration notes, 1,070,046 checked text characters, 44
  chapter scripts with implementation horizons, 0 live/research marker hits, 0
  raw core-claim marker hits, and audio targets still not generated. This is
  not narration quality review, pronunciation review, chapter timecoding, an
  audiobook, audio generation, or an audio release record.
  `scripts/validate_reader_audio_narration_treatment.py` now records the
  script-level narration treatment review in
  `docs/reader_audio_narration_treatment_review.md` and
  `editions/reader_manuscript/v1_0/audio_narration_treatment_review_manifest.json`,
  clearing only `narration_quality_review_not_completed` for the current
  blocked candidate. Audio files, spot/listening review, chapter-marker
  timecoding, audio-embedded EPUB packaging, the audio edition release record,
  and audiobook approval remain open. `scripts/validate_reader_audio_metadata_review.py`
  records the metadata-only review in `docs/reader_audio_metadata_review.md`
  and `editions/reader_manuscript/v1_0/audio_metadata_review_manifest.json`,
  clearing only `audio_metadata_not_reviewed` while preserving all artifact,
  timing, listening, packaging, and audio-release blockers.

### Milestone 9 - Prior Art, Preprints, And Archiving

Goal: turn the book from a strong public project into a credible research
program without repackaging already-known work as novelty.

Tasks:

- Before drafting a preprint, write a prior-art/novelty assessment for the
  candidate contribution. The assessment must name what is old, what is
  integrated from existing practice, what is new in this project, and what
  remains only argument-level.
- Extract one or more focused preprints:
  - living evidence book methodology;
  - proof-carrying claim and support-state discipline;
  - governed self-improvement boundary;
  - Circle proof-carrying AI contracts;
  - Project Theseus report-first implementation evidence.
- Use the early external-review milestone to choose which preprints are worth
  writing first.
- Add DOI/Zenodo only after an archive exists and `CITATION.cff` names the
  actual DOI.

Acceptance bar:

- every candidate preprint has a prior-art/novelty note before drafting;
- preprints do not claim support states stronger than the book records;
- archive metadata points to exact release commits and artifacts.

## Negative Outcomes And Demotion

The roadmap must improve correctness, not only add material. Treat these as
valid successful outcomes:

Current status: `docs/evidence_laundering_prevention_case_studies.md` records
three no-promotion examples that resisted evidence or artifact laundering, plus
one live claim-surface narrowing record for the obsolete 54-to-current-44
manifest count boundary. This is useful progress, but it is not a true
chapter-core demotion/refutation record. The first real chapter-core demotion,
refutation, retirement, or claim-narrowing event still needs to be recorded
when evidence justifies it.

- A chapter core claim can stay at `argument`, move downward to `unsupported`,
  become `refuted`, or split into narrower claims if evidence fails.
- A chapter can be substantially rewritten, merged, or removed if external
  review or prior-art work shows that its thesis is wrong, already solved, or
  not chapter-owning.
- A planned evidence lane can be retired when it cannot produce public-safe,
  reproducible, or externally reviewable evidence.
- A proof target can be retired or replaced if it only encourages projection
  proofs or formalizes the wrong boundary.
- A reader-chapter curation can be rejected if it changes claim meaning,
  support-state meaning, source boundaries, proof/test status, or implementation
  horizons.

Recording rule:

- demotions use the existing support-state vocabulary and evidence-transition
  or claim-decision records;
- refutations name the source, proof, test, reviewer finding, or failed replay
  that caused the change;
- chapter merges/removals update `book_structure.json`, `docs/book_outline.md`,
  handoffs, source notes, Appendix C, and the changelog;
- no negative result is hidden by simply leaving a lane unexecuted.

## v1.x Evidence Release Gate

A future v1.x evidence-and-reader release should not ship until these gates are
explicitly passed or explicitly scoped out in a release record.

| Gate | Required evidence | Release blocker if missing |
|---|---|---|
| Prior CI gate | Previous GitHub Pages run checked, local validation run, and no known failed prior run ignored. | Do not commit or tag until the prior failure is fixed or scoped. |
| Execution-over-reports gate | Any new roadmap, report, review packet, or scorecard is paired with an executed proof, evidence, source, reader, artifact, release, or external-review change, or is explicitly required by a validator. | The project is spending cycles on planning surfaces instead of changing artifacts. |
| Retired URL preservation | The ten retired consolidation URLs have static historical stubs with refresh/canonical targets into active manifest chapters, guarded by `scripts/validate_chapter_consolidation_sequence.py`. | Public links from the pre-consolidation book can silently rot. |
| Sixty-second trust surface | README and landing page make current evidence, non-claims, proof limits, source-ownership boundaries, reader-release boundaries, and external-review status legible quickly, with `scripts/validate_trust_surface.py` checking the counts and links against current artifacts. | Cold readers cannot distinguish disciplined research program from overbroad theory, or stale public counts can launder evidence scope. |
| Non-core evidence visibility | Appendix C or sibling surface names the six current non-core transitions and keeps all 44 core claims at `argument` unless separately promoted. | Readers cannot tell what evidence exists. |
| Early external review | At least one external review record exists, or a dated blocker records outreach and scope. | The release remains self-reviewed. |
| Defended contribution focus | The release names three to five contribution tracks and at most three deep-work tracks for the cycle. | The project remains broad without defended results. |
| Safety-critical Lean depth | Five targeted modules include `derived_or_decomposed` theorem coverage, anti-projection conclusions, and negative cases, or a release record explicitly keeps them projection-only. | Formal layer remains v1.0-depth. |
| Flagship measured result | At least one selected evidence lane has a one-command reproducible run with baseline, negative control, residuals, non-claims, and an accepted transition or explicit no-promotion decision. | The project remains internally disciplined but does not show an architecture-relevant result. |
| Public replay/import | At least one Theseus or Circle lane is CI-replayed or CI-verifiable by pinned digest with negative controls, when relevant to the selected evidence lane. | Imported evidence remains local-summary only. |
| Chapter-lane cap | The release names one flagship lane plus at most two supporting lanes and leaves the rest planned; no 44-lane synthetic sweep is claimed. | Breadth trap not controlled. |
| Per-chapter external grounding | Every chapter has source-noted external comparators, candidate backlog, or an explicit exception; accepted third-party records appear in generated Appendix H. | The book still reads as self-sourced nomenclature. |
| Proof/evidence coverage | Each executed lane names whether its strongest evidence path is Lean, Theseus, Circle, external literature, external review, or an explicit no-promotion blocker. | Arguments remain prose-only without a testable support route. |
| External-SOTA distance | The release updates distance from SOTA, not only internal activity. | "Beyond-SOTA" remains unaudited. |
| Consolidation stability | The 44-chapter spine remains stable unless a source, evidence, reviewer, or reader-edit finding justifies a specific boundary change; any retired URL remains preserved. | The project reopens structural churn without evidence. |
| Negative-outcome handling | Failed, demoted, refuted, merged, or retired lanes are recorded instead of hidden. | Evidence process is monotonic and biased. |
| Authorial craft and distillation | The reader manuscript has a single thesis, part arcs, recurring signature ideas, chapter-specific openings/closings, designed key figures, and finished third-person prose with a sidecar enrichment queue and zero manuscript gaps — no fabricated first-person material anywhere. | Human edition remains a template-shaped derivative and cannot be honestly called final-quality. |
| Human-reader quality | Every curated reader chapter reads at finished quality, the edition is built and release-recorded, and any released artifact has an exact release record; Corben's final edit is polish over the complete book, not a gate (2026-07-02 direction). | Human edition remains a generated projection only. |
| Artifact honesty | EPUB/DOCX/PDF/audio/DOI are claimed only if exact artifacts or archive identifiers exist. | Artifact or archive claim would be fabricated. |
| Traceability closure | Reader, live, source, claim, proof, evidence, figure, format, and release records agree for every released artifact, with stale counts caught by validators. | A chapter or artifact looks finished but cannot be traced back to its source, proof, evidence, release, and non-claim records. |
| Designed-publication polish | Public site, Human view, reader artifacts, figures, navigation, accessibility checks, and companion/audio routing are reviewed as publication design, not only as successful renders. | The project passes build/render checks but still feels like default Quarto or a validator dump. |

## Logical Conclusion - What Finished Means

Added 2026-07-03. A living book never "ends," so its logical conclusion is two
things, not one: a **complete-book state** that each major release can be
audited against, and a **steady operating state** that keeps the book alive
indefinitely after that bar is met. Every milestone above serves one of the
five tests below. When all five pass, the project has reached its logical
conclusion and transitions to maintenance cadence; until then, the remaining
distance is the backlog.

### Test 1 - Complete chapters (both editions, all 44)

Every chapter — not a subset — has:

- finished live/research prose with its evidence surfaces, limitation
  language, and showpiece-caliber anchor sections;
- finished reader prose realizing the thesis, part arc, signature ideas, and
  chapter-specific stakes/payoffs, with zero slots, placeholders, or
  template residue;
- deep external grounding: named comparators in prose backed by source-noted
  `ext_` records, or a recorded deliberate exception;
- formal backing that is either executable-model grade (transition-system
  invariant, trace property, or fixture equivalence) or explicitly classified
  as finite-record/projection with matching limitation prose;
- an executed evidence lane: an accepted narrow transition, or a recorded
  no-promotion decision backed by a real measurement or digest-verified
  import — "planned" is not an end state for any lane;
- polished figures with text equivalents placed in both editions, and
  companion/audio treatment for its dense material.

### Test 2 - Complete editions and artifacts

- The live site, Human view, curated reader edition, EPUB, DOCX, and PDF
  (where local dependencies allow) are built, format-reviewed at application
  level, and release-recorded; audio scripts are reviewed and audio artifacts
  are produced and release-recorded or explicitly deferred with a dated
  record.
- Retired URLs remain stub-guarded; the sixty-second trust surface, non-core
  evidence ledger, and release records stay accurate at every release.
- Visual identity is reviewed as a designed artifact, not only validated as
  rendering.

### Test 3 - Complete evidence program

- All 44 named per-chapter evidence lanes in
  `docs/per_chapter_evidence_plan.md` have executed at least once under
  flagship pacing (one flagship plus at most two supporting lanes per cycle —
  completion comes from steady cycles, never from a synthetic sweep).
- Every chapter core claim has an explicit disposition: promoted above
  `argument` through accepted evidence-transition records, or retained at
  `argument` with a standing statement of exactly what evidence would move
  it. No silent stalls. The current source of record is
  `claim_decisions/v1_x_core_claim_dispositions.json`, with the generated
  reviewer surface at `docs/core_claim_disposition_ledger.md`.
- Project Theseus and Circle evidence used by the book is CI-replayable or
  digest-verifiable from public-safe artifacts.

### Test 4 - Complete formal program

- Every safety-critical module carries executable-model-grade backing or an
  explicit projection-only classification mirrored in chapter prose.
- v1-critical protocol records have Lean/Python fixture-equivalence checks or
  a recorded reason one lane does not apply.
- The proof-adequacy review, proof-depth classification, and proof manifest
  agree with each other and with the rendered book.

### Test 5 - Steady operating state (the living conclusion)

- The new-paper intake, source-note, changelog, evidence-transition, and
  release loops are documented well enough that any future run can operate
  the book indefinitely without re-deriving process.
- The Milestone 2.5 burn-down carries zero open rows without dated blockers,
  and stays truthful under the reconciliation rule below.
- Major versions are tagged, release-recorded, and archived (DOI/archive
  metadata when Corben triggers it); the book absorbs new sources and new
  evidence through the intake loop without structural churn.

### A+ Completion Execution Lattice (standing, added 2026-07-03)

The five tests above define the end state. This lattice defines the execution
shape that gets there without another round of planning churn. Future runs
should close these lanes as artifacts, not as new reviews.

| Lane | A+ closure artifact | Do not count as closure |
|---|---|---|
| Burn-down truth | Milestone 2.5 rows are reconciled against existing artifacts first, with each row closed by artifact or dated to one remaining blocker. | A refreshed review paragraph, grade, or status note. |
| Reader manuscript | All 44 curated reader chapters are reconciled, legacy voice-pass slots are converted into optional non-blocking sidecar enrichment prompts, the Part III/IV arcs are edited, and the edition has a release record naming exact built artifacts and blockers. | Generated reader projection, local render success, or `drafting` files. |
| Contribution focus | Three to five defended contribution tracks stay selected, at most three are active deep-work tracks, and each active track has a concrete next evidence/proof/source artifact that either advances a named signature idea or records why the track's next artifact is different. | Treating all 44 chapters as simultaneous flagship campaigns, or maintaining contribution-track and signature-idea lists that do not constrain implementation choices. |
| Idea depth | One signature idea per cycle closes as an idea-depth closure packet: live chapter prose, curated reader prose, outline role/evidence routing, contribution novelty ledger, source-noted comparators, analytic consequence with weakening condition, strongest objection answered in chapter prose, proof/evidence artifact or dated blocker, and limitation/non-claim updates. | A novelty-ledger row, stronger terminology, a clever chapter phrase, or standalone idea audit that does not change chapters, reader prose, evidence, proof, limitations, and the next executable artifact path. |
| Evidence disposition | Every chapter core claim has a standing disposition record: accepted transition, explicit no-promotion decision, demotion/refutation, or exactly what evidence would move it. | Implied status from prose, validator count, or source assignment. |
| Formal depth | Safety-critical and v1-critical lanes either reach executable-model grade through transition invariants, trace properties, or Lean/Python fixture-equivalence checks, or carry projection-only limitation prose that matches the proof-adequacy review. | More theorem declarations that restate field presence or expand coverage without richer semantics. |
| External grounding | Each chapter has source-noted comparators in prose, a candidate backlog, or a deliberate exception, with accepted third-party records entering through `sources/source_inventory.json`, source notes, and generated Appendix H. | Placeholder citations, bibliography-only mentions, or private conversation context. |
| Theseus/Circle/public replay | Project evidence used for stronger claims is CI-replayable, CI-verifiable by pinned digest, or explicitly blocked by a public-safety/private-artifact constraint. | Local memory of a run, source-reported claims, or artifact names without replay/digest checks. |
| Publication artifacts | Live site, Human view, curated reader HTML, EPUB, DOCX, PDF, and audio/script paths are reviewed at the application level and release-recorded with exact artifact digests, or deferred with dated blockers. | Format probes, successful conversion, or target rows that imply artifacts exist. |
| Visual and accessibility polish | Key figures, theme, navigation, alt text, text equivalents, screen-reader/keyboard checks, and e-reader/audio companion treatment have review records before release approval. | Default Quarto styling, render success, or diagram presence alone. |
| Public repo hygiene | Generated clutter remains ignored, tracked files stay intentional, stale counts are validator-checked, and README/landing/status surfaces match release records before a public tag. | A clean local working tree without checking public-facing counts and artifacts. |

When a lane is already represented by an existing document, validator, manifest,
or release record, update that artifact directly. Add a new surface only when no
existing artifact can carry the decision without ambiguity.

### Burn-down truth rule (standing, added 2026-07-03)

The burn-down previously under-reported progress for three consecutive review
rounds. The current table is reconciled against existing artifacts as 1
`closed by artifact` row and 43 explicit `partially executed` rows with named
remaining work. The standing rule: **reconciling Milestone 2.5 against existing artifacts is the
required first commit of any run that touches reader, proof, or evidence
surfaces.** A batch whose closure classes all have named artifacts must be
marked `closed by artifact` in that same run, or carry a dated blocker naming
the one closure class that remains. A tracker that understates progress is a
defect with the same severity as one that overstates it.

### Clean-handoff rule (standing, added 2026-07-04)

The claim-state-transition-bridge increment exposed the cost of leaving an
artifact half-wired: proof manifests, Lean code, validators, proof-count
surfaces, and rendered Human-view checks all have to move together. The
standing rule: **never end a run with failing validators or an uncommitted
increment.** When the budget is running out, finishing or cleanly reverting the
in-flight increment outranks starting anything new; regenerate enforced status
fragments, run the full gate, render if public surfaces changed, and commit.
A red gate at handoff costs the next run its first hours and makes the tree
unreviewable. The claim-state-transition-bridge increment is now the example of
the desired closure state: validator wired, result recorded, proof and
adequacy surfaces synchronized, local render checked, and no support-state or
live-core-claim movement asserted.

### Status-surface sprawl rule (standing, added 2026-07-04)

Validator-enforced status fragments have grown pathological: when an enforced
fragment exceeds roughly one hundred words, restructure it into a generated
count-plus-ledger-link form (the detailed enumeration lives in a generated
ledger document; the status cell carries counts and a link), updating the
enforcing validators in the same commit. Executed so far: the Proof envelope
cell now points to `docs/proof_envelope_status_ledger.md`; the former
multi-thousand-character `v1_0_candidate_status.md` "Test harnesses" cell now
points to `docs/test_harness_status_ledger.md`; the release-surface detail now
points to `docs/release_surface_status_ledger.md`; and the oversized
`Non-infrastructure measured slice` row now points to
`docs/non_infrastructure_measured_slice_status_ledger.md`, generated by
`python3 scripts/validate_non_infrastructure_measured_slice_status_ledger.py --write`
and the former `Project Theseus static import lane` row now points to
`docs/project_theseus_static_import_status_ledger.md`, generated by
`python3 scripts/validate_project_theseus_static_import_status_ledger.py --write`;
the former `Compact GVR synthetic slice` row now points to
`docs/compact_gvr_status_ledger.md`, generated by
`python3 scripts/validate_compact_gvr_status_ledger.py --write`;
the former `Live Human view` row now points to
`docs/live_human_view_status_ledger.md`, generated by
`python3 scripts/validate_live_human_view_status_ledger.py --write`; and the
former overlong `Support states` row now delegates core coverage, core
disposition, non-core upward transition, and no-promotion side-lane detail to
`docs/core_claim_transition_coverage.md`, `docs/core_claim_disposition_ledger.md`,
and `docs/non_core_evidence_ledger.md`. These ledgers are enforced through
`validate_v1_status_snapshot.py` plus
`validate_book.py`. Continue applying this pattern to any future
validator-enforced status row that grows past compact status-summary size.

### Remaining distance as of 2026-07-04

- Test 1: reader arc reconciliation is complete across all 44 active curated
  reader chapters, and the twelve legacy voice-pass slots are converted into
  optional non-blocking sidecar enrichment entries. Live-edition chapter-length
  watchlist, release-quality continuity polish, exact format review, and a
  release-approval record remain open; the current blocked candidate record
  keeps those blockers explicit without promoting the manuscript to release.
- Test 2: one blocked curated-reader release-candidate record now exists beyond
  the 2026-06-29 approved generated-reader HTML record. It names exact current
  local HTML/EPUB/DOCX/PDF/e-reader/audio blockers without approving or
  publishing artifacts. The current curated reader manuscript now has a
  refreshed local HTML/EPUB/DOCX/PDF structural probe with 49 HTML files, 52
  EPUB XHTML entries, 61 DOCX PNG media entries, 0 SVG conversion warnings, and
  a 506-page PDF sample-page render with 50 Chrome-screenshot Mermaid
  fallbacks. Its repaired-package EPUB audit checks all
  XHTML content/navigation links with 0 unresolved internal hrefs, and its
  Chromium EPUB XHTML browser review checks 104 page-view pairs with 0 failures,
  and its EPUB key-figure layout review checks 10 key-figure XHTML entries, 20
  desktop/e-reader-like page-view pairs, 0 key-figure browser failures, 10 px
  maximum horizontal overflow, and 0 image failures. The Apple Books EPUB
  application review opens the repaired EPUB digest, renders chapter 1 without
  the earlier XML error banner, advances to a figure page, opens the table of
  contents, and clears only `app_or_ereader_review_not_completed`; EPUB still
  remains unreleased until reader release approval and an edition release
  record exist. Its
  repaired-package DOCX audit checks document
  XML/media/relationships with 0 raw `.qmd` relationship targets, and its
  LibreOffice headless DOCX review converts 504 pages with 0 blank, 0 low-ink,
  and 0 near-edge converted-page rasters, but DOCX still remains probe-level
  until Word, LibreOffice GUI, Google Docs review, or an explicit release
  decision and an edition release record exist. Its DOCX key-figure layout
  review checks 10 title pages, 10 title-page rasters, 72.1 pt minimum title
  margin, 9.53% minimum page ink, 0.0% maximum near-edge ink, and 37.95
  minimum luminance standard deviation while preserving Word, LibreOffice GUI,
  Google Docs, and manual document review as release blockers. Its PDF visual raster audit
  renders all 506 pages with 0 blank pages, 1 low-ink page, and 0 near-edge
  pages; its PDF extracted-text reading-flow review checks 506 nonempty text
  pages, 44 ordered chapter headings, 3 ordered appendix headings, and 0
  replacement characters. Its PDF key-figure layout review checks 10
  key-figure caption pages, 10 caption-page rasters, 165.878 pt minimum
  caption margin, 3.36% minimum page ink, 0.0% maximum near-edge ink, and 14.2
  minimum luminance standard deviation. Its Chromium PDF viewer smoke review
  records 2 nonblank viewer screenshots and 4.479% changed pixels after scroll.
  Its PDF page-by-page release-preparation review checks 506 page rows, 0
  failed pages, 0 blank pages, 0 near-edge pages, 0 out-of-bounds word-box
  pages, and one accepted low-ink page, closing the current candidate's
  `manual_pdf_page_by_page_review_not_completed` blocker while preserving
  reader release approval. Its aggregate final figure-artifact review records
  10 key figures, 10 content-bound checks, 10 alt texts, 10 PNG raster
  fallbacks, 20 EPUB layout page-view pairs with 0 failures, 10 PDF
  caption/raster pages, and 10 DOCX title/raster pages, clearing only
  `final_figure_artifact_review_not_completed`. PDF remains probe-level until
  an edition release record exists; audio now has
  automated script reading-flow/order review with 49 ordered marker rows and 66
  narration notes, plus accepted script-level narration treatment and accepted
  metadata review, but it remains blocked on pronunciation/listening review,
  chapter-marker timecoding, generated audio artifacts, audio-embedded EPUB
  checks, and an edition release record; source-geometry review now exists with 10
  content-bound checks, 10 text-anchor checks, and 22.0 px minimum content edge
  margin; source-level visual identity review now exists with 10 key figures,
  54 combined colors, 5 non-neutral color families, and minimum text contrast
  5.19, but visual identity remains blocked on manual rendered visual
  inspection, manual aesthetic judgment, e-reader visual review beyond the
  Apple Books smoke/application path, and reader release approval.
  Source-level accessibility/navigation review now exists with 44 one-H1
  chapters, 44 handoff sections, 10 draft figure alt texts, 10 figure boundary
  paragraphs, 0 live-marker leaks, and 0 raw core-claim marker leaks, but it
  remains source-level. Automated Chromium keyboard traversal now exists with
  98 desktop/mobile page-view pairs, 98 skip-link activations, 98 main-content
  routes, and 0 keyboard-trap candidates. The keyboard-only evidence decision
  now clears only `manual_keyboard_only_review_not_completed`; screen-reader
  review, WCAG conformance review, audiobook review, and reader release
  approval remain open. Automated Chromium
  accessibility-tree release-preparation review now exists with 98
  desktop/mobile page-view pairs, 0 failures, 98 accessibility-tree page-view
  pairs, 0 unnamed interactive elements, 0 image-alt failures, 0 table-header
  failures, and 0 duplicate-ID hits. By itself it does not clear
  screen-reader review, WCAG conformance review, e-reader review, audiobook
  review, or reader release approval; the separate keyboard-only evidence
  decision clears only the current keyboard-only blocker.
  Automated PNG raster fallback review now exists
  with 10 generated fallbacks, 10 standard 1200 x 760 canvases, 99.954%
  minimum opaque pixel coverage, 27.64 minimum luminance standard deviation,
  and 116 minimum quantized colors. The aggregate final figure-artifact
  release-preparation review now exists in
  `docs/reader_final_figure_artifact_review.md` with status
  `passed_final_figure_artifact_release_preparation_review`, covers all ten
  key figures, and clears only the current candidate's
  `final_figure_artifact_review_not_completed` blocker; manual aesthetic
  judgment, e-reader visual review beyond the Apple Books smoke/application
  path, DOCX/PDF application review, and reader release approval remain open.
- Test 3: 6 accepted narrow transitions, including the finite synthetic
  load-smoothing selector transition and the local empirical scoped-route
  selector transition; most chapter evidence lanes have not yet executed.
  Core-claim dispositions are now recorded per chapter in
  `claim_decisions/v1_x_core_claim_dispositions.json` and rendered in
  `docs/core_claim_disposition_ledger.md`; the remaining work is executing
  those lanes, not discovering what would move them. The Artifact Graphs
  record-reality side lane now also has a public deployed-site attestation at
  `experiments/artifact_public_site_attestation/results/2026-07-05-live.json`;
  it is an accepted no-promotion served-page observation only, not deployed
  attestation behavior, open-world receipt faithfulness, reader release
  approval, external human review, or chapter-core support.
- Test 4: first fixture-equivalence, memory-store, and identity-sequence
  bridges exist; most safety-critical modules remain finite-record grade with
  correct labeling.
- Test 5: Milestone 2.5 burn-down accounting is current for this pass: all 44
  rows carry either `closed by artifact` or explicit `partially executed`
  status with named remaining work; intake and release loops exist and are
  validated; DOI/archive remains user-triggered and pending.
- Cross-project (2026-07-04): Project Theseus's roadmap now carries a
  Fourth-Pass AI Book Parity Addendum (Theseus-Hive `roadmap.md`) committing
  Theseus to implement every book mechanism as the exemplar repo, with a
  two-way contract: Theseus consumes the book's schemas/fixtures as a
  conformance suite, and emits standard public-safe evidence packs plus one
  real end-to-end reference trace (intent through improvement gate with real
  layer handoffs) for the book to import. When those exports land, route them
  through Milestone 3 import gates and the integrated-reference chapter's
  open live-trace ask; they are the designated path for several Test 3/Test 4
  closures. Governance-tax measurements from real Theseus runs are the
  designated empirical evidence for the resource-economics governance-tax
  lane.

### 2026-07-04 evening review findings (standing until closed)

1. **Validator execution semantics (immediate closure plus standing rule).**
   The evening review found a real gate hole: `validate_prototype_phase_gates.py`
   failed standalone after curated-reader prose polish removed a raw result
   identifier, while the orchestrated suite still passed because file-reference
   mentions were counted as coverage. Close the trigger by making
   `validate_validator_coverage.py` count actual CI commands or
   `run_validator(...)` calls, wiring executable missing validators into
   `scripts/validate_book.py`, preserving explicit reasons for the two
   artifact-producing local DOCX/PDF review validators that should not rerun
   on every CI pass, and restoring a plain-language reader evidence sentence
   for the curated prototype-roadmap chapter. The standing policy is now:
   every validator must be executed by the orchestrator, executed directly in
   CI, or allow-listed with a specific artifact/dependency reason; curated
   reader validators that enforce evidence text must accept a defined
   reader-form equivalent rather than forcing raw result IDs into human prose.
   Audit future curated prose passes for the same polish-versus-evidence
   collision before treating a green gate as release evidence.
2. **Release unblock ladder.** The blocked curated-reader release candidate
   (`release_records/2026-07-05-v1-curated-reader-blocked-d81d505a.json`) is
   the close-out queue; work it in order and flip the record from blocked to
   approved when it empties. The first preparation rung is closed by
   `python3 scripts/validate_reader_human_consumption_gate.py`,
   `editions/reader_manuscript/v1_0/human_consumption_gate_manifest.json`,
   and `docs/reader_human_consumption_gate_review.md`: ebook layout,
   diagram/image readiness, bedtime readability, and companion-note routing
   are `pass_pre_release_review` for release preparation only. The PDF
   page-by-page preparation rung is closed by
   `python3 scripts/validate_curated_reader_pdf_page_review.py --write-manifest`,
   `editions/reader_manuscript/v1_0/pdf_page_review_manifest.json`, and
   `docs/curated_reader_pdf_page_review.md`: all 506 pages have text,
   word-box, and raster rows, with 0 failed pages, 0 blank pages, 0 near-edge
   pages, 0 out-of-bounds word-box pages, and one accepted low-ink page. This
   clears only the current candidate's
   `manual_pdf_page_by_page_review_not_completed` blocker. The final
   figure-artifact preparation rung is closed by
   `python3 scripts/validate_reader_final_figure_artifact_review.py`,
   `editions/reader_manuscript/v1_0/final_figure_artifact_review_manifest.json`,
   and `docs/reader_final_figure_artifact_review.md`: the aggregate gate
   records 10 key figures, 10 content-bound checks, 10 alt texts, 10 PNG
   fallbacks, 20 EPUB layout page-view pairs with 0 failures, 10 PDF
   caption/raster pages, and 10 DOCX title/raster pages, clearing only
   `final_figure_artifact_review_not_completed`. The chapter reconciliation
   approval rung is closed by
   `python3 scripts/validate_reader_chapter_reconciliation_approval.py`,
   `editions/reader_manuscript/v1_0/chapter_reconciliation_approval_manifest.json`,
   and `docs/reader_chapter_reconciliation_approval.md`: all 44 curated reader
   chapter records are reconciled, full-review rows are present, curated files
   exist, and the approval clears only `curated_reconciliation_not_approved`.
   The audio narration-treatment rung is closed by
   `python3 scripts/validate_reader_audio_narration_treatment.py`,
   `editions/reader_manuscript/v1_0/audio_narration_treatment_review_manifest.json`,
   and `docs/reader_audio_narration_treatment_review.md`: the script-level
   treatment review checks 49 ordered scripts, 66 narration notes, 1,070,046
   text characters, and 10 draft key-figure spoken summaries, clearing only
   `narration_quality_review_not_completed`. The audio metadata rung is closed
   by `python3 scripts/validate_reader_audio_metadata_review.py`,
   `editions/reader_manuscript/v1_0/audio_metadata_review_manifest.json`, and
   `docs/reader_audio_metadata_review.md`: it records title, version, source
   commit/tag, script digest, narrator/tooling boundary, and rights-statement
   fields, clearing only `audio_metadata_not_reviewed`. The reader
   release-candidate bridge is closed by
   `python3 scripts/validate_reader_release_candidate_bridge.py`, result
   `experiments/reader_release_candidate_bridge/results/2026-07-05-local.json`,
   and Lean tag
   `lean:living_book.methodology.reader_release_candidate_bridge`: local format
   evidence routes the current candidate to screen-reader/WCAG review rather
   than release approval, while synthetic controls reject audio-missing,
   approval-missing, support-promotion, and missing-non-claim overclaims. This
   closes a proof/evidence boundary only; it clears no release blocker and
   does not approve curated reader HTML, EPUB, DOCX, PDF, e-reader, audio, or
   the reader edition. The active release queue is now:
   complete manual keyboard-only, screen-reader, and WCAG review where release
   scope requires it; complete audio file generation, pronunciation/listening
   review, chapter-marker timecoding, audio-embedded EPUB packaging, and
   audio-edition gates where audio scope requires them;
   reconcile any remaining release-scope e-reader visual review beyond the
   Apple Books application path; and issue the approved or still-blocked
   edition release record. The DOCX application-evidence decision is closed
   for this candidate and clears only `docx_application_review_not_completed`.
   Publication/tagging of the approved artifacts remains a user-triggered act,
   like DOI; producing the approved record does not wait on anyone.
3. **Evidence ladder static at 6 for two decision-heavy rounds.** The 19 new
   no-promotion decisions are correct refusals, but the cadence rule needs an
   ascent path executed, not only guarded: the named next accepted-transition
   candidates are live or externally reviewable residual-ledger
   storage/replay, receipt-attestation/audit evidence, or the first Theseus
   parity imports (governance-tax measurement, reference-trace export) under
   the cross-project contract above.
4. **Gate operations note.** The orchestrated gate (`validate_book.py`) is
   the canonical local gate; one-by-one loops over the full validator set are
   not an operational mode and now exceed interactive budgets. Keep the
   orchestrator complete (finding 1) rather than making the loop fast.

## Version Targets

| Target | Position vs SOTA | Minimum bar |
|---|---|---|
| `v1.1` | Moves from internal release hygiene toward externally reviewable evidence process. | Retired URL stubs are guarded; sixty-second trust surface exists and is validator-checked; non-core evidence ledger visible; one external review request, response, or dated blocker is recorded; one flagship measured lane is selected with baseline/negative-control design. |
| `v1.2` | Moves from internal discipline to a reproducible architecture-relevant result. | The flagship measured lane has a one-command run, baseline, negative control, residuals, non-claims, and an accepted evidence transition or explicit no-promotion decision; any Theseus/Circle import used by the lane is CI-verifiable by digest or replay. |
| `v1.3` | Moves formal layer from finite-record routing toward executable-model practice. | One selected proof/evidence lane has a transition-system invariant, trace property, or Lean/Python fixture-equivalence check; theorem-count growth alone does not satisfy the target. |
| `v1.4` | Moves reader surface from generated projection to a finished human manuscript. | Curated reader manuscript follows the stable 44-chapter table of contents; every reader chapter reads at the level of the current best ones; the book-level thesis, part arcs, signature ideas, and chapter stakes/payoffs are realized in the prose itself; key figures are placed with text equivalents and validator-checked placements; the optional enrichment queue is a sidecar with zero manuscript gaps; reader HTML remains validated; and the edition is built and release-recorded with EPUB/DOCX/PDF blockers reduced to format-review items only (2026-07-02 direction: nothing waits on Corben). |
| `v1.5` | Moves the human edition from clean technical prose toward a crafted artifact. | Key figures have moved beyond draft coverage into visual review, visual identity, EPUB/DOCX/PDF layout probes, audio-script treatment, and companion-note routing are reviewed enough to show exactly what remains before a polished major reader release. |
| `v1.x evidence release` | Becomes stronger than v1.0.0 by evidence depth, not by blanket coverage. | The v1.x release gate passes; one flagship measured lane has executed evidence or an explicit no-promotion decision; every chapter has external-grounding status; core claims promote only where evidence-transition records justify it. |
| `v2.0` | Becomes a public research program with external scrutiny, archived artifacts, and reproducible evidence packs. | External review, archived release, polished human editions, reproducible Theseus/Circle evidence packs, stronger executable-model proofs, prior-art-reviewed preprints, and DOI/archive metadata exist. |
| `v2.x` | Operates as a living research program on steady cadence. | Each cycle executes flagship-paced evidence lanes toward Test 3 completion, deepens formal backing toward Test 4, absorbs new sources through the intake loop, keeps both editions release-current, and keeps the burn-down truthful under the standing rule; no cycle ships planning surfaces without executed change. |
| `v3.0 complete book` | Reaches the project's logical conclusion as defined above. | All five Logical Conclusion tests pass: every chapter complete in both editions, all editions and artifacts release-recorded, all 44 evidence lanes executed with explicit core-claim dispositions, the formal program complete, and the steady operating state documented — after which the project runs in maintenance cadence and major releases are archived as they occur. |

## Suggested Long-Running Goal

Use this wording when it is time to start the next large autonomous work run:

2026-07-03 goal note: the Idea Depth clause below is read together with the
dispatch table above. Do not redo the bounded governance-tax model; the next
governance-economics movement must be live or externally reviewable workload
evidence, a source-noted economic comparator pack, or a dated blocker with the
missing artifact named.

> Execute the v1.x roadmap for **The ASI Stack** in implementation-first mode with the Grade-To-A-Plus Map as the priority compass, the Logical Conclusion section as the completion compass, and the A+ Completion Execution Lattice as the anti-diffusion rule: the target is A+ on every graded dimension for both editions of every chapter, the end state is the five Logical Conclusion tests, and per the 2026-07-02 direction nothing waits on Corben — his editing pass comes last, over a finished book. Standing first action of every run, before any new work: reconcile the Milestone 2.5 burn-down against artifacts that already exist, in both directions — any batch whose closure classes all have named artifacts must be marked closed by artifact in that same run, or carry a dated blocker naming the one remaining closure class. First priority: finish the human-reader edition. Treat chapter-level prose reconciliation and legacy voice-pass conversion as artifact-backed, then move to release-quality continuity polish, table-density/long-paragraph cleanup, figure polish, audio/e-reader flow, and exact format review so all 44 reader chapters read at the level of the current best ones; realize the thesis, part arcs, and 8-12 signature ideas in the prose itself (openings, endings, transitions), writing conviction and stakes to finished quality in third person; never invent first-person experience, personal conviction, or authorial lessons. Then build the edition — HTML, EPUB, DOCX, and PDF where local dependencies allow — run the format validators and application-level checks the format-review matrix defines, including the current six-row curated-candidate blocker queue, and produce an edition release record so "drafting" becomes a release state. Second priority: evidence cadence. Strengthen one selected measured, replay, or import lane per cycle to an accepted narrow non-core transition or explicit no-promotion decision; accepted no-promotion records over existing planned-only fixtures may reduce ambiguity, but they must not be counted as active-lane selection or upward support movement. Load-stability and workload-quality already have accepted narrow transitions, so the next cycle should either deepen them toward live/external review or select the next public-safe Circle/Theseus/fixture lane. Import the next public-safe Circle or Theseus result CI-verifiable by digest or replay, record demotions, rejections, and no-promotion decisions honestly, and keep `claim_decisions/v1_x_core_claim_dispositions.json` current so core-claim dispositions are now recorded per chapter rather than inferred from scattered surfaces. Third: build one executable-model proof bridge tied to a live evidence lane — a transition-system invariant, trace property, or Lean/Python fixture-equivalence check — instead of chasing theorem count; do not redo the Capability replacement identity-sequence bridge, which already covers the first bounded field-identity canary/rollback sequence, unless the next change brings live/external replay, real regression-floor evidence, monitor-window evidence, rollback dry-run evidence, or a stronger Theseus/Circle public fixture. Fourth: advance the Idea Depth Program as an artifact gate, not a planning lane — do not redo the verification-bandwidth capacity model, residual-conservation fixture, residual-ledger storage/replay fixture, receipt-faithfulness fixture, epistemic-TCB fixture, human-oversight degradation fixture, partitioned-authority fixture, owner-spine pattern-language integration, first control-boundary pattern-language slice, broader planning/context/routing/compression/self-improvement local-delta slice, or bounded stable-identity sequence bridge already implemented; next preserve local-delta discipline and work the next signature ideas one execution state to the right, preferring receipt faithfulness / record-reality gap, residual honesty, human oversight degradation, verification tax / governance economics, support-state ladder / evidence-state soundness, then stable identity and bounded self-improvement unless an earlier lane records a dated public-safety or missing-artifact blocker. Move from owned argument or bounded fixture toward live/external residual-ledger storage and replay, live/external receipt attestation and audit behavior, live/external approval-workflow reviewer-degradation evidence, live/external governance-tax workload evidence, true demotion/refutation/narrowing cases or claim-state transition bridges, live/external replacement replay, live/external partitioned-authority grant/revocation traces, source-noted prior-art/external review for pattern-language novelty, or a dated blocker naming the exact missing artifact. Each closure requires live prose, reader prose, source-noted prior-art delta, contribution-ledger update, analytic consequence with weakening condition, strongest objection answered in chapter prose, proof/evidence artifact or dated blocker, and explicit non-claims. For receipt faithfulness/record-reality, treat Artifact Graphs as the current owner: strengthen it into the showpiece record-reality section in both editions, then split into a new manifest-backed chapter only if the section-level treatment fails the split test by creating duplication, burying a distinct evidence lane, or making adjacent chapters less clear. Route the epistemic trusted computing base, human oversight degradation, and the remaining section-level additions through the normal manifest/outline/evidence-lane process, creating a new chapter only when the ownership test is passed and the addition shortens, absorbs, or disambiguates existing material rather than adding another skeleton. Fifth: execute the live-edition craft watchlist — move bulky tables, validator minutiae, and repeated caveats to companion or live-only surfaces where evidence boundaries allow, and bring one anchor section per part to showpiece-trace caliber. Close lattice lanes through existing artifacts whenever possible: contribution-track records, contribution novelty ledger rows, source notes, Appendix H, proof adequacy, evidence transitions, reader manifests, format-review matrices, release records, figure reviews, and trust surfaces. Keep the executed 44-chapter spine stable and retired URLs stub-guarded; keep the sixty-second trust surface and non-core evidence ledger accurate; keep the external-review lane parked as user-owned (the dated blocker is the standing record — schedule no outreach and gate nothing on it); do not create new planning/report surfaces unless a validator, release record, or executed change requires them; continue the status-surface sprawl rule only when a validator-enforced cell grows beyond compact status-summary size, moving that detail into a generated ledger in the same implementation commit. Before every commit, check the latest completed GitHub Pages run; run the relevant local validation gate, Lean build when proof code changes, and Quarto render for changed public surfaces; commit and push coherent increments. Never fabricate source content, citations, proof results, test results, support-state promotions, external-review records, authorial voice, personal experience, artifact approvals, deployment readiness, model quality, benchmark performance, or completed ebook/PDF/DOCX/audio artifacts.

## Non-Claims

- This roadmap does not promote any chapter core claim above `argument`.
- This roadmap does not prove ASI capability, model quality, runtime safety,
  deployment readiness, benchmark performance, economic outcome, source
  interpretation, or transfer.
- This roadmap does not add new external sources, prove every argument, or
  promote citation candidates into evidence before source notes and transition
  records exist.
- This roadmap now records the first public-safe Project Theseus static import,
  but it does not create a clean live Theseus replay, public Circle replay pack,
  EPUB, PDF, DOCX, audio artifact, DOI, Zenodo archive, external review record,
  or support-state promotion.
- This roadmap does not make curated reader prose equal authority beside the
  live AI/research book.
- This roadmap does not claim the book is already a final-quality authored
  work, and it does not authorize Codex to fabricate Corben's voice, personal
  history, lived lessons, or convictions.
