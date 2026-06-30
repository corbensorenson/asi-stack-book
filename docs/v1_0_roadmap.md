# v1.0 Roadmap

Last updated: 2026-06-29

This roadmap records the v1.0 release path for **The ASI Stack**. The current
v1.0.0 release state is tagged at source commit
`96d0ca3c6b62f3530202535573941b1f6e50a83d`, with a tracked living-book release
record at `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`.

For post-`v1.0.0` work, use `docs/v1_x_beyond_sota_roadmap.md` as the active
execution target. This file remains the v1.0 release-path and gate-history
record.

The live AI/research book remains the canonical architecture, evidence, source, proof, schema, and release-control source. The normal reader manuscript can eventually become a curated parallel derivative source for prose, pacing, chapter flow, and human-consumption packaging. It is parallel but not equal: it may diverge from the live/research text for readability, but it must inherit claim text, support states, source boundaries, proof/test status, implementation horizons, and release records from the live book unless a deliberate reconciliation step updates both surfaces.

Use this file as the v1.0 release-path record. Use `docs/v1_x_beyond_sota_roadmap.md` as the goal target for new long-running v1.x improvement work, `book_structure.json` for ordering, `docs/book_outline.md` for drafting/proof/source scope, and `docs/v1_0_focus_audit.md` for the historical current-state audit that led into v1.0.0.

## Inputs Reconciled

This roadmap reconciles:

- the current repository state during the 2026-06-28 extended v1.0 improvement run;
- `docs/v1_0_focus_audit.md`;
- the external Claude review supplied by Corben as planning input;
- the 2026-06-29 Claude depth review supplied by Corben as planning input;
- the 2026-06-29 Claude roadmap review supplied by Corben as planning input;
- local verification of Claude's concrete claims against the current tree, including validator coverage, proof-depth classifier output, external-SOTA citation placement, reader artifact blockers, schema/Lean field-shape drift, release-gate gaps, citation metadata, render-toolchain pinning, and Theseus/Circle evidence-import lanes.

Claude's review is useful as an editorial and hygiene review, not as source evidence. It should not be quoted as an external authority in the book.

## What Had Teeth

| Finding | Current verification | Roadmap treatment |
|---|---:|---|
| Mechanical `Operating mechanism:` recap lists in `Beyond the State of the Art` sections | 0 after Phase 1 pass; 26 before pass | Phase 1 rewrote these into mature-product prose and added a guard so the pattern cannot return. |
| Repeated `remains a target architecture, not a current-result claim` disclaimer | 0 after Phase 1 pass; 42 before pass | Phase 1 preserved the non-claim boundary with chapter-specific language. |
| Repeated `keeps ... honest` construction | 0 after Phase 1 pass; 9 before pass by regex | Phase 1 replaced the reusable cadence with mechanism-specific prose and added a guard. |
| Reader/ebook should not inherit all live-book uniformity | Structurally true by design | Phase 2. Review generated reader edition, then graduate toward a curated parallel reader manuscript when prose divergence becomes too large for overlays. |
| Manifest claim/support defaults should not hide source-of-truth state | Resolved for the current chapter set: all 44 chapter records now declare explicit `claim_label` and `evidence_level` fields, and `schemas/book_structure.schema.json` records the whole-file manifest shape | Phase 0 guardrail. `scripts/add_chapter.py` creates explicit fields for new chapters, and `scripts/validate_book.py` validates `book_structure.json` against the schema before semantic source/proof checks. |
| Projection-style Lean proofs can look stronger than they are | Substantiated and now measured by `docs/proof_depth_classification.md`: 302 theorem declarations classified, 115 direct/projection-style, 187 derived/decomposed, 0 unknown or mixed, 45 theorem declarations in the five safety-critical modules, 10 of them still direct/projection-style, and 5 of 5 safety-critical chapter limitation sections now explicitly classify those hooks as projection-only traceability | Phase 4 formal-depth hardening implemented for v1 honesty. Stronger safety-critical Lean models remain desirable, but the current v1 route is explicit projection-only traceability with no broad safety-proof claim. |
| CI validator coverage can drift because coverage is transitive and hand-maintained | Initially substantiated. The workflow directly names part of the `scripts/validate_*.py` set, and `scripts/validate_book.py` names the rest, so the harnesses were CI-covered transitively but without a drift guard. `scripts/validate_validator_coverage.py` now checks direct workflow coverage, `validate_book.py` transitive coverage, required validators, and all registered Phase 5 harness scripts against a tracked allow-list; `scripts/run_phase5_harnesses.py` now executes the registered harness suite from the registry | Phase 0 hardening implemented for validator coverage, Phase 5 registry execution implemented for the synthetic harness set, and the first bounded registry-runner, costed-route/resource-budget, and Circle external receipt transitions are now recorded. Remaining evidence work is deeper prototype/empirical depth, not harness wiring. |
| External SOTA engagement is uneven in chapter prose | Resolved for the v1.0 placement gate and machine-tracked by `docs/external_sota_positioning_audit.md`: 44 of 44 chapters have `ext_*` positioning before the Source crosswalk, 0 have explicit external-baseline exceptions, 0 need source-target placement, and 0 need an exception or added source-noted baseline | Phase 6 now passes the strict placement release check. Exhaustive external-literature synthesis and future exception replacement remain v1.x quality work unless a new claim widens. |
| Schema, Lean records, and fixtures can drift as three encodings of one protocol | Substantiated by comparing richer JSON schema records, such as `authority_transition_record.schema.json`, against narrower Lean abstractions such as `AuthorityDecisionRecord`; initial v1-critical reconciliation now exists in `protocols/v1_critical_protocol_crosswalk.json` and `docs/protocol_record_crosswalk.md` | Phase 5A. Maintain the crosswalk validator, resolve or document mismatches as intentional abstractions, then decide whether a single record-spec generator or shared executable fixture path is worth building after v1-critical records are stable. |
| The first measured support transition was missing | Resolved for three narrow claims. `docs/first_measured_replayed_slice.md` and `evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json` record `living-book-methodology.phase5_harness_registry_runner` moving from `argument` to `synthetic-test-backed`; `docs/costed_route_resource_slice.md` and `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json` record `resource-economics.costed_route_budget_slice` moving from `argument` to `synthetic-test-backed`; `docs/circle_external_receipt_slice.md` and `evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json` record `circle-calculus.external_rope_receipt_replay` moving from `argument` to `prototype-backed`; all 44 chapter core claims remain at `argument`, 22 chapter core claims have accepted no-change records, and 22 chapter core claims have accepted explicit no-promotion decisions in `claim_decisions/v1_0_core_claim_no_promotion.json` | Phase 3B now has bounded infrastructure and non-infrastructure synthetic transitions plus one imported external prototype receipt transition. The next evidence work should move toward deeper public-safe prototype integration, empirical measurement, imported trace, or replay lanes before any chapter core claim can move. |
| Reader release still needs a real artifact approval path | Partly resolved. Reader HTML now has full local browser artifact review, source tag `v1.0.0-reader-html-source`, and an edition release record for the exact local HTML snapshot; EPUB, DOCX, and PDF remain rendered/probed but unapproved | Phase 2 and Phase 8. Treat HTML as the minimum reviewed human artifact for v1.0, then finish application-level EPUB/DOCX/PDF review only if those artifacts are promoted into the current release scope. |
| Public site and process-record quality now need accessibility and ledger discipline | Actionable as Phase 7 work. The site validates mechanically, but diagram text alternatives, contrast, e-reader legibility, and process-record sprawl need human review before a polished v1 public release | Phase 7. Add accessibility checks and consolidate long process records into structured ledgers plus short summaries where it reduces roadmap noise. |
| Render-toolchain and citation metadata were too implicit for a public major-version candidate | Resolved for v1.0.0. CI now pins Quarto `1.9.38`, Python `3.11`, and Node `22`, Lean remains pinned through `lean/lean-toolchain`, `CITATION.cff` records version `1.0.0`, and `docs/release_reproducibility.md` records locale, tool-path, reader-format, tag, source-commit, DOI-pending, and non-release boundaries checked by `scripts/validate_release_reproducibility.py` | Phase 7 reproducibility/citability slice implemented for v1.0.0. DOI/Zenodo metadata remains pending until an archive exists. |
| Local repo cleanup via `git gc` | Local hygiene only | Optional local maintenance; do not treat as book quality work. |

## What Is Already Resolved Or Not Actionable

| Finding | Current status |
|---|---|
| Unfinished `"The result is"` pass | Resolved in current `main`; `validate_repeated_prose.py` now rejects the phrase and current chapters have 0 hits. |
| Source notes, external appendix split, Lean toolchain, CI gates, proof imports, generated appendices | Resolved before this roadmap; do not re-spend effort unless a validator fails or new source/proof work changes the surface. |
| New harnesses are entirely absent from CI | Not actionable as stated. `publish.yml` calls `scripts/validate_book.py`, and `validate_book.py` currently calls every `scripts/validate_*.py` file either directly or through the rendered Human-view/browser steps. The remaining issue is future drift prevention, not current total absence. |
| `validate_proof_artifact_audit.py` and `validate_source_evidence_audit.py` silently writing files | Not reproduced. Both default to check mode and write only with `--write`; CI runs them in check mode. |
| Stale deployed appendix set | Not a current blocker. Current Pages runs are checked before commits, and local render validates the A-K appendix surface. |
| `validate_live_human_view.py` needing a fresh `_site` | Resolved as local hygiene. CI orders render before this check, and the validator now preflights missing, incomplete, or stale `_site` output with a render-first diagnostic. |

## v1.0 Definition Of Done [Release Gate]

The roadmap is complete for a **true v1.0 evidence-and-reader release** only
when all v1.0-blocking gates below are satisfied and recorded. If a gate is not
satisfied, the project may still tag a narrower candidate or architecture
release, but it must not call that tag a v1.0 evidence release.

v1.0 ships when all of these hold:

1. **Reader artifact gate:** at least one human-consumption artifact has an application-level or browser-level review record appropriate to that format, the exact artifact is named in an edition release record, and its format row has no release blockers. The current minimum is the reviewed local reader HTML artifact in `release_records/2026-06-29-v1-reader-html-855dc277.json`; EPUB remains preferred for e-reader use but is not required for a narrower v1.0 if it stays explicitly unapproved. DOCX, PDF, audio, or additional e-reader formats are claimed only if their own rows meet the same standard.
2. **Claim-state gate:** every core chapter claim has either an accepted evidence-transition record or an explicit v1.0 no-promotion decision. No support state moves above `argument` without a transition record naming evidence, commands where relevant, limitations, counterevidence, and non-claims.
3. **First measured/replayed result gate:** at least one narrow claim receives a support transition from a public-safe measured or replayed result, or the release records a named blocker explaining why no available measured slice cleared the promotion bar and the tag remains an architecture release rather than an evidence release.
4. **Proof-depth gate:** `SelfImprovement`, `Alignment`, `Corrigibility`, `GovernanceRights`, and `ValueConflict` are either upgraded beyond projection-only Lean hooks or explicitly classified as projection-only traceability in `docs/proof_depth_classification.md`, `docs/proof_adequacy_review.md`, the relevant chapters, and the proof-readiness output.
5. **Validator coverage gate:** CI includes a meta-check that every `scripts/validate_*.py` file is covered by `publish.yml`, by `scripts/validate_book.py`, or by a tracked allow-list. The gate must explicitly keep `validate_source_notes.py`, `validate_proof_readiness.py`, `validate_evidence_transitions.py`, and the Phase 5 harness set covered.
6. **Protocol record gate:** v1-critical protocol records have a schema/fixture/harness/Lean crosswalk, or an explicit no-Lean/no-schema reason. Intentional abstraction between schema fields and Lean structures is documented instead of left implicit.
7. **External-SOTA prose gate:** every chapter's Problem, insufficiency, or Beyond-SOTA section names the relevant external baseline it is positioning against, or records a deliberate exception. These references must have source records and source notes before being used as source support.
8. **Beyond-SOTA map gate:** the Beyond-SOTA Reference Map below is current and honest about where the book is leading, where it is only competitive, and where it is below established SOTA.
9. **Architecture red-team gate:** at least one system-level adversarial review exists for cross-layer authority escalation, context/SCIF leakage, evaluator capture, support-state inflation, and benchmark gaming, with residuals routed into claims, proof targets, tests, or explicit v1.x deferrals.
10. **Reproducibility and citability gate:** the render/reader toolchain is pinned or documented; the Python and Lean prerequisites are explicit; `CITATION.cff` has major-version metadata; and the release has a "how to cite this version" note. A Zenodo DOI is preferred for v1.0, but if it cannot be issued before tagging, the release record must say DOI pending.
11. **Green release gate:** local validation, `lake build`, Quarto HTML render, rendered Human-view validation, browser validation where available, changelog, release record, and prior GitHub Pages run are all current.

Explicitly deferred to v1.x unless a later decision promotes them into v1.0:

- Curated parallel reader-manuscript graduation beyond generated reader source plus overlays.
- Audiobook, M4B, MP3, audio-embedded EPUB, AZW3, MOBI, and all non-approved document/e-reader formats.
- Exhaustive external-literature synthesis beyond the in-prose v1.0 positioning gate.
- Full single-source protocol generator for every schema, Lean structure, harness, and fixture.
- Executable Lean/Python fixture equivalence for every protocol record.
- Standalone academic preprints, external peer review, and field-recognition work.
- Any claim of ASI capability, deployed safety, model-quality improvement, production governance, or runtime performance beyond recorded evidence.

## Beyond-SOTA Reference Map [v1.0-blocking]

This table makes "beyond SOTA" auditable. Reference points are planning labels
until source records and source notes exist; do not cite a named external system
or paper in prose from memory. The v1.0 target is not to be better than every
external system at every task. The target is to say exactly which dimension the
ASI Stack advances, what remains below SOTA, and what evidence would be needed
to strengthen the claim.

| Dimension | External reference point to normalize | Current ASI Stack position | v1.0 target |
|---|---|---|---|
| Formal verification | Full functional-correctness projects such as seL4 and CompCert; proof-carrying-code literature | Lean coverage is broad but mostly finite-record; `docs/proof_depth_classification.md` currently reports 115 direct/projection-style theorem declarations, 187 derived/decomposed declarations, and projection-style hooks across all five safety-critical modules | State honestly that the book is below full functional correctness; upgrade or classify the five safety-critical modules and keep claims scoped to derived invariants actually proved. |
| Living technical evidence system | Executable papers, Distill-style explainers, Papers with Code, model cards, datasheets, reproducibility checklists | Claim ledger, source mappings, proof manifest, harness registry, release profiles, no-change transitions, bounded synthetic transitions, and the imported Circle receipt transition are unusually disciplined | Defend this as a leading contribution only after the release gate records exact validation, reader-review, and evidence-transition boundaries. |
| Governance/safety architecture | NIST AI RMF, frontier-model evaluation and deployment-policy frameworks, incident-response and audit practices | Typed authority, stable capability fields, readiness gates, residual escrow, fork/exit/audit rights, and self-improvement gates are coherent but argument-level | Add in-prose external positioning and a cross-layer red-team review; keep deployment/safety claims at `argument` unless evidence transitions justify more. |
| Human/AI dual-edition publishing | Standard technical-book and documentation pipelines, reader editions, release notes, artifact bundles | Live AI/research view, Human view, reader derivation, overlays, format ledgers, and audio script path are structurally beyond ordinary static-book practice; one reviewed local reader HTML artifact now has an exact edition release record | Keep the HTML record reproducible and citation-scoped, then pursue EPUB as the preferred e-reader artifact only if application review clears. |
| Routing and cost-quality efficiency | MoE routing, FrugalGPT/Hybrid LLM/RouteLLM-style routing, systems scheduling, benchmark governance | Costed route ledgers, readiness gates, residual accounting, resource-budget fixtures, and one bounded synthetic costed-route/resource-budget selector transition exist, but no real route-quality measurement, deployed scheduler trace, or load result has promoted a chapter claim | Preserve the bounded synthetic selector transition as narrow evidence, then move the lane toward real route-quality measurements, scheduler/load traces, hidden-cost audits, or prototype receipts before making stronger routing or resource-economics claims. |
| Compression and representation | Deep Compression, LoRA/QLoRA/GPTQ, MDL, program synthesis, artifact metrics | The book has architecture and source notes, and the Circle external receipt slice now records one proof-contract replay, but there is still no local compression ratio, quality result, or backend benchmark | Candidate next measured slice: RankFold/artifact compression, cyclic-compute receipt transport, or representation utility with performance explicitly separated from proof legality. |
| Benchmark and anti-Goodhart governance | HELM, BIG-bench, SWE-bench, LiveBench, Dynabench, GPQA, contamination and Goodhart literature | Benchmark-ratchet and anti-Goodhart schemas/harnesses exist as synthetic discipline | Add external positioning in prose and keep any benchmark advancement scoped to recorded fixtures until real benchmark traces exist. |
| Protocol-spec consistency | Schema-first APIs, typed contracts, formal specs, runtime monitors | Schemas, fixtures, Lean records, and Python harnesses are present but hand-maintained and can drift | Ship a v1-critical protocol crosswalk plus validator before claiming spec discipline beyond traceability. |

## Phase Blocking Map

| Phase | v1.0 status | Remaining residual |
|---|---|---|
| Phase 0 | v1.0-complete | Validator coverage meta-check, clean release process, and v1.0.0 toolchain/citation discipline are guarded by validators. |
| Phase 1 | v1.0-complete | Keep the repeated-prose guards passing; no remaining Phase 1 task blocks v1.0. |
| Phase 2 | v1.0-complete for minimum reader HTML artifact; v1.x for curated reader source | The reviewed local reader HTML snapshot has an edition release record. Curated reader source, EPUB e-reader approval, full DOCX/PDF review, and audio remain outside the minimum v1.0 reader gate unless explicitly promoted. |
| Phase 3 | v1.0-complete for claim-state coverage | `docs/core_claim_transition_coverage.md` records 44 of 44 chapter core claims covered: 22 accepted no-change transition records plus 22 accepted explicit no-promotion decisions; all remain at `argument`. |
| Phase 3B | v1.0-complete for bounded infrastructure, non-infrastructure, and imported receipt slices | Accepted transitions now cover the narrow Phase 5 registry-runner claim, the bounded costed-route/resource-budget selector claim, and the imported Circle rope receipt replay claim; stronger prototype or empirical lanes remain needed before chapter core claims can move. |
| Phase 4 | v1.0-complete for proof-depth honesty | Proof-depth classifier and safety-critical projection-only chapter classifications are implemented; stronger Lean upgrades remain future quality work unless claims widen. |
| Phase 5 | v1.0-complete for first non-infrastructure synthetic slice and first imported receipt slice; deeper prototype/empirical evidence remains v1.x unless promoted | Harness runner, coverage drift guard, costed-route/resource-budget measured-slice validation, and Circle external receipt validation are implemented. Next Phase 5 work should move toward public-safe prototype traces, empirical measurements, or consumer-gated imported receipts. |
| Phase 5A | v1.0-complete | Initial v1-critical protocol crosswalk is implemented; keep it current and use it to resolve/document schema/Lean/fixture drift during evidence-transition work. |
| Phase 6 | v1.0-complete for the placement gate | `docs/external_sota_positioning_audit.md` records 44 positioned chapters, 10 explicit exceptions, 0 source-target placement rows, and 0 exception/source rows; the stricter `--release` validator passes. |
| Phase 7 | v1.0-complete for final tag metadata; v1.x for DOI/archive and manual accessibility review | Public-site accessibility readiness, compact progress ledger, v1.0 release-gate audit, tag `v1.0.0`, GitHub Release, and living-book release record are recorded. DOI/Zenodo and manual keyboard/screen-reader review remain future quality work. |
| Phase 7A | v1.0-complete for desk red-team review | `docs/architecture_red_team_review.md` records all six required architecture-level attack scenarios with residuals and routed follow-ups; runtime/security validation remains future evidence work. |
| Phase 8 | v1.0-complete for reader HTML; v1.x for EPUB/DOCX/PDF/audio unless promoted | `release_records/2026-06-29-v1-reader-html-855dc277.json` names the exact reviewed local HTML artifact; EPUB, DOCX, PDF, e-reader, and audio artifacts remain unapproved. |
| Phase 9 | post-v1.0 | External preprints and contribution extraction should not block v1.0. |

## Phase 0 - Operating Discipline [v1.0-blocking]

Status: active and ongoing. The initial validator-coverage meta-check is implemented in `scripts/validate_validator_coverage.py`, wired into `.github/workflows/publish.yml`, and called by `scripts/validate_book.py`.

Purpose: keep the repo honest while work continues.

Tasks:

- Check the prior GitHub Pages run before each new commit.
- Keep raw/private source exports out of the public repo.
- Keep all 44 core claims at `argument` unless an accepted evidence transition justifies a narrower promotion.
- Keep every manifest chapter record explicit about `claim_label` and `evidence_level`; missing or invalid values fail the book validator.
- Do not report reader, ebook, document, PDF, or audio artifacts unless that exact artifact was generated, reviewed where required, and recorded.
- Keep CI validator coverage explicit with `python3 scripts/validate_validator_coverage.py`: every `scripts/validate_*.py` file must be covered by the workflow, by `scripts/validate_book.py`, or by `scripts/validator_coverage_allowlist.json` with a reason.
- Keep `book_structure.json` and `docs/book_outline.md` as source-of-truth surfaces.
- Update `appendices/F_changelog.qmd` for meaningful roadmap, source, claim, proof, reader, release, or validation changes.

Exit criteria:

- Working tree clean before starting a major pass.
- Prior Pages run checked.
- No generated scaffold drift after `python3 scripts/sync_scaffold.py`.
- `python3 scripts/validate_validator_coverage.py` fails if a new validator is not covered or explicitly allow-listed, and it keeps `validate_source_notes.py`, `validate_proof_readiness.py`, `validate_evidence_transitions.py`, and all registered Phase 5 harness scripts covered.

## Phase 1 - Reader-Visible Voice And De-Templating [v1.0-complete]

Status: complete for the current tree after the 2026-06-28 prose-and-guard pass.

Purpose: remove the remaining finite, measurable generator bleed-through without weakening evidence boundaries.

Tasks:

1. Rewrite the 26 `Beyond the State of the Art` sections that still contain `Operating mechanism:` recaps.
2. Preserve each section's mature endpoint content: final product surface, operational contract, evidence flow, governance boundary, failure closure, and composition with neighboring layers.
3. Replace the repeated 42-instance target-architecture disclaimer with chapter-specific non-claim language.
4. Smooth the 7 `keeps ... honest` constructions where they read as repeated cadence rather than natural prose.
5. After the `Operating mechanism:` count reaches 0, add a repeated-prose or DoD guard that rejects the pattern in future chapter prose.
6. Re-run reader-spine, chapter DoD, repeated-prose, visual coverage, and rendered Human-view checks.

Do not:

- Remove non-claim boundaries.
- Promote support states.
- Hide evidence limits only in live-only sections.
- Turn Beyond-SOTA sections into marketing copy.

Acceptance criteria:

- `rg -n "Operating mechanism:" chapters` returns 0.
- `rg -n "remains a target architecture, not a current-result claim" chapters` returns 0.
- `python3 scripts/validate_repeated_prose.py` passes.
- `python3 scripts/validate_chapter_dod.py` passes.
- `python3 scripts/validate_reader_spine.py --check` passes.
- `quarto render --to html`, `python3 scripts/validate_live_human_view.py`, and the browser Human-view validation pass before reporting completion.

## Phase 2 - Reviewed Reader Manuscript Path [v1.0-blocking]

Status: started. The generated reader baseline was produced and recorded in
`docs/reader_manuscript_review.md`; the active semantic reader-overlay log is
recorded in `docs/reader_overlay_pilot.md` with 31 active operations for Human
view and generated reader editions. The generated heuristic continuity audit is
recorded in `docs/reader_continuity_audit.md`; the first manual
medium-priority decisions are recorded in `docs/reader_continuity_review.md`;
the first Part I, Part II, Part III, and Part IV matrix review passes are
recorded in `docs/reader_part_i_review_pass.md`,
`docs/reader_part_ii_review_pass.md`, `docs/reader_part_iii_review_pass.md`,
and `docs/reader_part_iv_review_pass.md`; and full chapter-text review passes
are recorded in `docs/reader_opening_full_review_pass.md`,
`docs/reader_boundary_full_review_pass.md`,
`docs/reader_normative_full_review_pass.md`,
`docs/reader_part_i_full_review_completion.md`,
`docs/reader_part_ii_contracts_full_review_pass.md`,
`docs/reader_part_ii_context_full_review_pass.md`,
`docs/reader_part_ii_verification_full_review_pass.md`, and
`docs/reader_part_ii_full_review_completion.md`, plus
`docs/reader_part_iii_opening_full_review_pass.md`,
`docs/reader_part_iii_compression_full_review_pass.md`,
`docs/reader_part_iii_representation_full_review_pass.md`, and
`docs/reader_part_iii_iv_proof_bridge_full_review_pass.md`, and
`docs/reader_part_iv_evidence_governance_full_review_pass.md`, and
`docs/reader_part_iv_completion_full_review_pass.md`. The synced chapter review
matrix is recorded in
`editions/reader_manuscript/v1_0/chapter_review_matrix.json` and summarized in
`docs/reader_chapter_review_matrix.md` with 44 `reviewed` chapters, 0
`spot_checked` chapters, 0 `not_started` chapters, 20 chapters carrying active
reader overlays, 44 no-immediate-action decisions, 3 companion-note candidates,
and 41 curated-manuscript candidates. `docs/reader_format_dry_run.md` records a
local HTML/EPUB/DOCX render dry run, basic structural artifact inspection, and
UTF-8 PDF probe with ignored snapshots; `docs/reader_artifact_inspection_manifest.md`
now preserves a tracked HTML/EPUB/DOCX structural-inspection summary for ignored
snapshots; `docs/reader_epub_probe_manifest.md` records the current EPUB
metadata/source-spine probe with explicit `en-US` language metadata and sampled
source-card entries; `docs/reader_docx_probe_manifest.md` records the current
514-page LibreOffice conversion probe for the generated DOCX;
`docs/reader_pdf_probe_manifest.md` records the current 535-page,
8,613,924-byte PDF probe, sampled source-card pages, and remaining full-PDF
layout-review blocker; `docs/reader_artifact_layout_review.md` records refreshed
EPUB/PDF/DOCX sampling plus a broader 28 page-view HTML layout/navigation probe;
and `docs/reader_html_artifact_browser_review.md` records a full local browser
artifact review of the generated reader HTML snapshot with 118 of 118 page-view
pairs passing across all 59 pages at desktop and mobile widths. The tracked format-review
ledger is recorded in
`editions/reader_manuscript/v1_0/format_review_matrix.json` and summarized in
`docs/reader_format_review_matrix.md`; it records the HTML row as
release-approved against
`release_records/2026-06-29-v1-reader-html-855dc277.json`, while EPUB remains
blocked on application/e-reader inspection, DOCX remains blocked on full
application review, and PDF remains blocked on full layout review.
The full generated-reader chapter-text review queue
is complete for the current 44 chapters. `docs/reader_companion_note_routing_review.md`
and `editions/reader_manuscript/v1_0/companion_note_routing.json` now record
chapter-level companion-note routing for the three proof/governance chapters
flagged by the review matrix, and generated reader/audio companion notes consume
that routing manifest. Broader EPUB/DOCX/PDF artifact inspection, curated
reader-manuscript graduation, audio review, and additional release records
remain open.
The future curated-source path is now governed by
`editions/reader_manuscript/v1_0/curation_contract.json` and
`docs/curated_reader_source_contract.md`, which require curated chapter records
to name generated baselines, live-source refs, claim boundaries, implementation
horizons, curation scopes, meaning-preservation checks, release blockers, and
canonical-change requirements before any manually edited reader chapter can
become release input.

Purpose: turn the mechanically valid Human view and generated reader source into a reviewed human-reader manuscript path.

Tasks:

1. Generate the reader edition with `python3 scripts/build_reader_edition.py`. The initial baseline generated on 2026-06-28 had 54 chapters, 59 files, 275 live-only sections removed, 54 human-only bridges unwrapped, 54 raw core-claim markers removed, 50 support-boilerplate passages humanized, 60 reader scaffold terms humanized, and no active reader overlays. The current generated check applies 31 active reader-overlay operations.
2. Review `build/reader_edition/READER_RELEASE_CHECKLIST.md`, `companion_notes.md`, and `reader_delta_report.md`. Initial review recorded in `docs/reader_manuscript_review.md`.
3. Read the generated reader manuscript for continuity, pacing, duplicated live-book scaffolding, missing transitions, and caveats that became too thin after stripping.
4. Apply human-reader-only deltas through `editions/reader_overlays/` only when the change should not alter AI/research view.
5. Apply canonical prose edits when the improvement belongs in all views.
6. Render reader HTML, EPUB, and DOCX when ready; attempt PDF only when local dependencies support it.
7. Record actual render outcomes without claiming publication until review and release records exist. The first local dry run rendered HTML, EPUB, and DOCX, snapshotted them under ignored `build/reader_edition/format_artifacts/`, and passed basic structural inspection. The current reader HTML snapshot passed full local browser review and is named in `release_records/2026-06-29-v1-reader-html-855dc277.json`. The current EPUB probe records `en-US` OPF metadata, navigation counts, sampled evidence-boundary text, and generated reader source-card appendix entries without clearing the e-reader blocker. The current DOCX probe converts through the local documents-skill/headless-LibreOffice path into a 514-page page-image sample. The isolated PDF probe failed without explicit locale settings but rendered when `LANG` and `LC_ALL` were set to `en_US.UTF-8`; the current tracked PDF probe is 535 pages and 8,613,924 bytes with title/evidence-boundary text present and generated reader source-card appendices sampled. Refreshed EPUB/PDF/DOCX sampling and a broader HTML layout/navigation probe exist, but no EPUB e-reader inspection, full DOCX application review, full manual PDF layout review, or additional format release record exists.

Active overlay set:

- `editions/reader_overlays/v1_0/chapters/asi-is-a-stack-not-a-model.json` carries two active reader-only section replacements for the opening chapter's `Problem` and `Summary` sections.
- `editions/reader_overlays/v1_0/chapters/the-efficient-asi-hypothesis.json` carries one active reader-only section replacement that converts the `Route outcome states` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/human-intent-as-a-formal-input.json` carries one active reader-only section replacement that converts the `Intent intake states` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/system-boundaries-and-authority.json` carries one active reader-only section replacement that converts the `Permission classes` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/evidence-states-and-claim-discipline.json` carries one active reader-only section replacement that converts the `Source contribution boundaries` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/personal-compute-hives-and-federated-edge-intelligence.json` carries six active reader-only section replacements that convert the `Owned substrate and device roles`, `Hive objects`, `Job classes and federation modes`, `Hive memory`, `Minimum Viable Implementation`, and `Beyond the State of the Art` sections into narrative prose.
- `editions/reader_overlays/v1_0/chapters/command-contracts-and-semantic-interfaces.json` carries two active reader-only section replacements that convert the `Command contract validation states` and `Interfaces` table material into narrative prose.
- `editions/reader_overlays/v1_0/chapters/planning-as-a-control-layer.json` carries one active reader-only section replacement that converts the `Plan node lifecycle states` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/verification-bandwidth-and-context-adequacy.json` carries one active reader-only section replacement that converts the `Adequacy states` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/runtime-adapters-tool-permissions-and-human-approval.json` carries one active reader-only section replacement that converts the `Effect receipt fields` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/labor-os-and-typed-jobs.json` carries one active reader-only section replacement that converts the `Typed job lifecycle states` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/circle-calculus-and-proof-carrying-ai-contracts.json` carries two active reader-only section replacements that convert the `Proof receipt lifecycle` and `Beyond the State of the Art` sections into narrative prose.
- `editions/reader_overlays/v1_0/chapters/generate-verify-repair-compression.json` carries one active reader-only section replacement that converts the `Compression receipt states` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/fast-generation-architectures.json` carries two active reader-only section replacements that convert the metric code block and `Generation-mode taxonomy` table material into narrative prose.
- `editions/reader_overlays/v1_0/chapters/rankfold-neuralfold-and-artifact-compression.json` carries one active reader-only section replacement that converts the `Artifact-compression states` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/mathematical-and-search-substrates.json` carries one active reader-only section replacement that converts the `Adoption packet lanes` table into narrative prose.
- `editions/reader_overlays/v1_0/chapters/policy-optimization-and-learning-from-feedback.json` carries two active reader-only section replacements that convert the `Method families` and external-literature tables into narrative prose, including a heading alias for the generated reader/source heading difference.
- `editions/reader_overlays/v1_0/chapters/artifact-steward-agents-and-living-project-governance.json` carries three active reader-only section replacements that convert the `Autonomy and treasury modes`, `Project objects`, and `Beyond the State of the Art` sections into narrative prose.
- `editions/reader_overlays/v1_0/chapters/executable-specifications-and-lean-proof-envelope.json` carries one active reader-only section replacement that converts the `Beyond the State of the Art` proof-envelope checklist into narrative prose.
- `editions/reader_overlays/v1_0/chapters/semantic-representation-and-tree-structured-models.json` now carries retired historical operations after the semantic-representation fold; future reader work should target the Semantic Representation Leasing material inside `compact-generative-systems-and-residual-honesty`.
- The overlay set exercises the intended divergence path: Human view and generated reader editions receive calmer book prose, while AI view and canonical chapter source keep the original live/research scaffold, tables, and evidence surfaces.
- The overlay set is not a reviewed reader release, ebook artifact, audio artifact, support-state promotion, source-derived evidence update, proof result, benchmark result, or runtime result.

Automated continuity audit:

- `python3 scripts/audit_reader_continuity.py --write` generated `docs/reader_continuity_audit.md` from a temporary reader-edition workspace.
- The audit measures 44 reader chapters, 106,698 reader words, 31 active/applied reader-overlay operations, 15 table rows, 53 Mermaid diagrams, 0 non-Mermaid code blocks, 0 paragraphs at or above 160 words, and 0 repeated first-sentence stems under the current heuristic.
- It identifies 2 high-priority and 3 medium-priority heuristic review chapters. The remaining rows are a triage queue for manual reader review, not defects and not evidence of release readiness.
- The audit is not a reviewed reader release, ebook artifact, audio artifact, support-state promotion, source-derived evidence update, proof result, benchmark result, runtime result, or substitute for reading the manuscript.
- `docs/reader_continuity_review.md` records the first manual decisions for the three medium-priority rows. The two proof-heavy chapters are no-action for now with companion-note/glossary candidates, and the long Artifact Steward chapter is retained with future curated-reader compression as a possible release-editing task.

Chapter review matrix:

- `python3 scripts/sync_reader_chapter_review_matrix.py --write` generated `editions/reader_manuscript/v1_0/chapter_review_matrix.json` and `docs/reader_chapter_review_matrix.md` from the manifest order plus current reader-overlay counts.
- The matrix currently records 44 chapter rows: 44 `reviewed` rows from the full generated-reader chapter-text review passes, 0 `spot_checked` rows, 0 `not_started` rows, 20 chapters with active reader overlays, 44 no-immediate-action decisions, 3 companion-note candidates, and 41 curated-manuscript candidates.
- All rows retain reader-release and format-artifact blockers. The full chapter-text review blocker is cleared for every current chapter, but the matrix is still a review queue, not a reviewed reader release.
- The matrix keeps the future curated reader manuscript path dynamic: chapter IDs, part order, live files, generated-reader file paths, and overlay counts sync from `book_structure.json` and overlay files, while review status and disposition remain explicit reader-review decisions.
- `editions/reader_manuscript/v1_0/reconciliation_report.md` now provides the dormant reconciliation template for future curated reader chapters, including generated-reader baselines, live-source refs, divergence summaries, blocked evidence divergence, and release blockers.
- `editions/reader_manuscript/v1_0/curation_contract.json` now provides the dormant curated-source contract for future reader chapters, including required record fields, allowed prose divergence, blocked evidence divergence, meaning-preservation checks, pre-release blockers, and validation commands.
- `docs/curated_reader_graduation_review.md` records the current graduation decision: drafting-only curated reader source may exist for v1.x prose work, but generated reader source plus overlays remain the release baseline until reconciliation, format review, and an edition release record exist.

Companion-note routing:

- `docs/reader_companion_note_routing_review.md` records the current routing decision for `circle-calculus-and-proof-carrying-ai-contracts`, `executable-specifications-and-lean-proof-envelope`, and `artifact-steward-agents-and-living-project-governance`.
- `editions/reader_manuscript/v1_0/companion_note_routing.json` is the tracked routing manifest consumed by generated reader and audio companion notes.
- Dense proof/governance vocabulary can receive glossary, quick-reference, and spoken-treatment support, but meaning-critical support limits, proof boundaries, governance boundaries, release blockers, and non-claims must remain in the reader spine.
- This routing pass does not create a reader release, ebook/document/PDF artifact approval, audio approval, curated reader chapter, support-state promotion, proof result, benchmark result, runtime result, or release-readiness claim.

Reader-source divergence rule:

- Start with generated reader source plus overlays because that keeps the reader path cheap to regenerate.
- When chapter-by-chapter prose editing becomes too substantial for overlays, graduate to a tracked curated reader manuscript for the normal human book.
- Treat that curated reader manuscript as a parallel derivative source for narrative only, not as an independent evidence source.
- Keep the live AI/research book canonical for chapter IDs, source assignments, support states, proof/test status, implementation horizons, diagrams that carry evidence meaning, and release records.
- Add a reconciliation check before any major reader release: every curated reader chapter must map back to a manifest chapter, preserve support boundaries, preserve meaning-changing caveats, and record any prose divergence that affects claims, examples, diagrams, or source interpretation.
- If reader editing reveals that the live/research source is wrong, thin, or misleading, fix the canonical chapter too rather than hiding the correction only in the reader manuscript.

Acceptance criteria:

- Reader manuscript residuals are recorded.
- Active overlay operations, if any, validate and apply cleanly to both generated reader source and live Human view.
- Generated reader source keeps support boundaries visible in plain language.
- Any curated reader source has a reconciliation report tying it back to live-book claims, support states, source boundaries, and implementation horizons.
- Any produced reader artifacts are named only after successful render and review.

## Phase 3 - Evidence Transition Pilot [v1.0-blocking]

Status: complete for v1.0 claim-state coverage. Twenty-two no-change evidence-transition records are recorded under `evidence_transitions/v1_0_pilot/`, summarized in `docs/evidence_transition_pilot.md`, and validated by `scripts/validate_evidence_transitions.py`. The remaining twenty-two chapter core claims have accepted explicit no-promotion decisions in `claim_decisions/v1_0_core_claim_no_promotion.json`, summarized in `docs/core_claim_transition_coverage.md`, and validated by `scripts/validate_core_claim_decisions.py`. Separate measured/replayed records under `evidence_transitions/v1_0_measured/` accept the narrow repository-infrastructure transition `living-book-methodology.phase5_harness_registry_runner` and the bounded non-infrastructure transition `resource-economics.costed_route_budget_slice` from `argument` to `synthetic-test-backed`, plus the imported Circle receipt transition `circle-calculus.external_rope_receipt_replay` from `argument` to `prototype-backed`. All 44 chapter core claims remain at `argument`.

Purpose: prove that the claim/evidence system can move claims conservatively, or explicitly decide not to move them.

Initial candidates:

- `evidence-states-and-claim-discipline`
- `living-book-methodology`
- `executable-specifications-and-lean-proof-envelope`
- generated source appendix ownership and implementation-horizon mechanics, scoped as book-method claims only

Tasks:

1. Pick narrow claims. Initial pilot selected `evidence-states-and-claim-discipline.core`, `living-book-methodology.core`, `executable-specifications-and-lean-proof-envelope.core`, and `open-research-agenda-and-bibliography-plan.core`; later extensions added `system-boundaries-and-authority.core` after the Authority proof follow-through, `planning-as-a-control-layer.core` after the Planning proof follow-through, `virtual-context-abi.core` after the context admission/adequacy harness, `claim-ledgers-and-belief-revision.core` after the claim-ledger revision harness, `spinoza-verification-and-proof-carrying-claims.core` after the proof-carrying claim harness, `unified-adaptive-tribunal-and-adversarial-review.core` after the tribunal review harness, `moral-uncertainty-and-value-conflict.core` after the value conflict harness, `constitutional-alignment-substrate.core` after the constitutional alignment harness, `agency-dignity-and-corrigibility.core` after the agency rights harness, `governance-rights-fork-exit-and-audit.core` after the governance rights harness, `security-kernel-and-digital-scifs.core` after the security kernel harness, `stable-capability-fields.core` after the stable capability fields harness, `capability-replacement-and-rollback.core` after the capability replacement harness, `recursive-self-improvement-boundaries.core` after the self-improvement boundary harness, `intent-to-execution-contracts.core` and `command-contracts-and-semantic-interfaces.core` after the plan-execution contract harness, `benchmark-ratchets-and-anti-goodhart-evidence.core` after the benchmark anti-Goodhart harness, `runtime-adapters-tool-permissions-and-human-approval.core` after the runtime-adapter permission harness, `readiness-gates-residual-escrow-and-quarantine.core` after the readiness/residual gate harness, `fast-generation-architectures.core` after the generation-mode baseline harness, and `the-efficient-asi-hypothesis.core` plus `resource-economics-and-token-budgets.core` after the efficiency/resource-accounting follow-through.
2. Review exact source passages, repository artifacts, commands, and limitations. Initial pilot reviewed repository artifacts, validators, proof audit, source appendix mechanics, and known limitations; it did not claim independent source-interpretation review.
3. Create or update evidence transition records. The no-change pilot now has twenty-six JSON records under `evidence_transitions/v1_0_pilot/`; the measured/replayed set has three accepted bounded records under `evidence_transitions/v1_0_measured/`.
4. Record non-promotion decisions where evidence remains insufficient. The pilot records twenty-six reviewed chapter/book claims as no-change decisions that remain at `argument`; `claim_decisions/v1_0_core_claim_no_promotion.json` records the other twenty-eight chapter core claims as explicit v1.0 no-promotion decisions.
5. Update Appendix C only after a chapter-core transition is accepted. No Appendix C chapter support-state update was made because the accepted upward transitions are scoped to the repository-infrastructure runner claim, the bounded synthetic costed-route/resource-budget selector claim, and the imported external Circle receipt claim, not to any chapter core claim.

Acceptance criteria:

- No broad AI, safety, capability, or deployment claim is promoted.
- Every proposed movement has a recorded basis and limitation.
- Negative or insufficient findings are preserved.
- Every core chapter claim has either an accepted evidence-transition record or a v1.0 no-promotion decision before an evidence-release tag. Current v1.0 status: satisfied and guarded by `python3 scripts/validate_core_claim_decisions.py`.

## Phase 3B - First Measured Or Replayed Slice [v1.0-blocking]

Status: bounded infrastructure, non-infrastructure, and imported prototype receipt slices accepted.
`docs/first_measured_replayed_slice.md` records the Phase 5 harness-registry
replay as the first measured/replayed slice, and
`evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json`
accepts `living-book-methodology.phase5_harness_registry_runner` as
`synthetic-test-backed`. `docs/costed_route_resource_slice.md` records the
first bounded non-infrastructure costed-route/resource-budget slice, and
`evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`
accepts `resource-economics.costed_route_budget_slice` as
`synthetic-test-backed`. `docs/circle_external_receipt_slice.md` records the
first imported external Circle receipt slice, and
`evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json`
accepts `circle-calculus.external_rope_receipt_replay` as
`prototype-backed`. No chapter core claim has moved above `argument`, and no
deployed runtime, scheduler, proof-contract transport, model-quality, safety,
benchmark, economic, transfer, or source-interpretation claim is promoted.

Purpose: create the first non-paperwork evidence milestone. The book should
show at least one narrow claim moving because a real artifact, trace, benchmark,
or replay was inspected under a recorded command and limitation boundary.

Candidate slices for the next, stronger evidence increment:

1. **Theseus/Circle transfer lane:** partially satisfied for one local external Circle rope receipt replay in `docs/circle_external_receipt_slice.md`; future work should use `theseus_circle_transfer`, `circle_calculus_core`, `circle_ai_contract_suite`, `proof_carrying_circular_computation`, and related local/public-safe reports to import additional theorem receipts, consumer-gate traces, or benchmark receipts only after the exact artifact, command, source path, permission boundary, and non-claims are recorded.
2. **Costed route/resource-budget slice:** satisfied for a bounded synthetic selector slice in `docs/costed_route_resource_slice.md`; future work should move this lane toward real route-quality measurements, budget-scheduler traces, or load/serving-system evidence.
3. **Context admission replay:** replay a public-safe context packet through admission and adequacy checks with stale/tainted/conflicting packet negatives.
4. **Compression or RankFold artifact slice:** measure a real compression ratio, reconstruction/utility predicate, residual burden, and baseline on a small permitted artifact.
5. **Planner/runtime adapter trace:** replay a small intent-to-contract-to-typed-job-to-receipt path with an explicit blocked negative case.

Promotion bar:

- The result must name command, environment, input artifact, output artifact, baseline or negative control, acceptance predicate, residuals, failure cases, and exact non-claims.
- The result must distinguish source-reported results from locally reproduced results.
- The result must have an evidence-transition record before Appendix C changes.
- A failed or inconclusive result remains useful and should be recorded, but it does not promote support state.
- If no candidate clears the bar, the release record must say so and the tag must remain an architecture/candidate release rather than a v1.0 evidence release.

Acceptance criteria:

- At least one measured or replayed slice exists with a public-safe result record and an accepted transition, or the v1.0 release explicitly downgrades itself from evidence release. Current v1.0 status satisfies this for the bounded registry-runner infrastructure claim, the bounded synthetic costed-route/resource-budget selector claim, and the bounded imported external Circle receipt claim.
- Theseus/Circle imported evidence preserves transfer-boundary non-claims and does not treat local project existence as reproduced ASI Stack evidence.
- Appendix C, the roadmap, and the release record agree on any support-state effect.

## Phase 4 - Proof Adequacy Review [v1.0-blocking]

Status: initial review complete, with follow-through increments, a proof-depth classifier, and safety-critical projection classifications recorded. `docs/proof_adequacy_review.md` classifies all 122 Lean targets while preserving support-state boundaries; `docs/proof_depth_classification.md` now classifies 302 Lean theorem declarations as 115 direct/projection-style, 187 derived/decomposed, and 0 unknown/mixed, with 45 theorem declarations in the five safety-critical modules, 10 of them still direct/projection-style, and 5 of 5 safety-critical chapter limitation sections explicitly classified as projection-only traceability. `AsiStackProofs.StackBoundaries` now includes a finite trace-level unauthorized external-handoff rejection theorem. `AsiStackProofs.ArtifactCompression` now includes finite negative-case theorems for failed-probe/no-fallback use and missing metadata promotion. `AsiStackProofs.ProofCarryingClaims` now includes finite negative-case theorems for passed verifier records without artifact refs and negative verifier results that try to produce scoped updates. `AsiStackProofs.PersonalComputeHives` now includes finite negative-case theorems for high-risk execution without a bound approval receipt and external hive access with missing lease-boundary fields. `AsiStackProofs.RuntimeAdapters` now includes finite negative-case theorems for modeled invocation without parent-job permission and high-impact unapproved adapter calls that try to remain unrejected. `AsiStackProofs.ProceduralMemory` now includes finite negative-case theorems for generated-tool closure records missing required artifacts and failed-regression reviews that try to keep routable promotion. `AsiStackProofs.Routing` now includes a finite negative-case theorem for selected routes missing authority or readiness. `AsiStackProofs.MoECOTRuntime` now includes finite negative-case theorems for runtime-core promotion missing readiness/regression/replay evidence and unavailable-text-only runtime claims trying to promote above `argument`. `AsiStackProofs.ArtifactGraph` now includes finite negative-case theorems for produced artifacts missing parent/source/context trace refs and incomplete or blocked provenance trying to support promoted claims. `AsiStackProofs.IntentContracts` now includes a finite intent-resolution route envelope, `AsiStackProofs.IntentToExecution` now includes a finite execution dispatch-route envelope, `AsiStackProofs.CommandContracts` now includes finite negative-case theorems for missing command fields and accepted hidden overrides, `AsiStackProofs.BibliographyPlan` now includes finite negative-case theorems for source-derived claims without source records and accepted new-source assignments to nonexistent chapters, `AsiStackProofs.CognitiveCompilation` now includes a finite semantic-lowering route envelope, `AsiStackProofs.VirtualContextABI` now includes a finite context-admission route envelope, `AsiStackProofs.VerificationBandwidth` now includes a finite verification-adequacy route envelope, `AsiStackProofs.TypedJobs` now includes a finite job-execution route envelope, `AsiStackProofs.StableCapabilityFields` includes a finite lifecycle-route envelope, `AsiStackProofs.Replacement` includes a finite transaction-route envelope, `AsiStackProofs.SecurityKernel` includes a finite authority-use route envelope, `AsiStackProofs.SelfImprovement` includes a finite transition-route envelope, `AsiStackProofs.Authority` includes a record-aware allow/deny/escalate authority decision envelope, `AsiStackProofs.FailureModes` includes a failure incident-route envelope, `AsiStackProofs.Planning` includes a plan-control record envelope for modeled dispatchable, blocked, and replanned records, `AsiStackProofs.ClaimLedger` includes finite ledger record envelopes, Runtime Adapters also has a synthetic permission/approval/receipt harness, Procedural Memory also has a synthetic loop-qualification harness, Routing Heads also has a synthetic route-lease harness, Artifact Graphs also has a synthetic replay/audit consistency harness, Fast Generation has deterministic baseline-accounting fixtures plus a no-change evidence decision, and Resource Economics has paired resource-budget accounting coverage, a deterministic resource-budget ledger harness, capacity-smoothing toy traces, and a no-change evidence decision. ASI Is a Stack, Human Intent, Command Contracts, Cognitive Compilation, Virtual Context ABI, Verification Bandwidth, Labor OS, Artifact Graphs, Procedural Memory, Routing Heads, Personal Compute Hives, Stable Capability Fields, Capability Replacement, Security Kernel, System Boundaries, Failure Modes, Planning, Claim Ledgers, Spinoza, Runtime Adapters, Integrated Reference Architecture, and Resource Economics remain `useful but too narrow` or `needs executable tests first` at chapter scope; Recursive Self-Improvement remains `needs richer state-machine or review semantics`; Fast Generation remains `needs empirical or baseline tests first` because deployed intent parsing, command parsing, deployed dispatch, source-plan parsing, target lowering, localized repair, resolver behavior, certificate truthfulness, summary fidelity, measured verification bandwidth, contradiction-rate behavior, lifecycle enforcement, deployed job runtime, deployed artifact graph service, replay engine, audit reconstruction service, deployed loop detector, tool synthesis, generated-tool correctness, regression-quality benchmarking, route monitoring, retirement automation, replacement execution, security-kernel enforcement, safe recursive self-improvement, runtime traces, planner quality, claim extraction, contradiction detection, verifier quality, sandbox behavior, approval-service behavior, model runs, matched baselines, speed-quality measurements, budget-scheduler behavior, load-stability behavior, serving/KV measurements, and richer integration behavior remain unproven.

Purpose: distinguish "Lean build passes" from "this is the right formalization."

The 2026-06-29 depth review adds one sharper requirement: separate derived
invariants from projection theorems. A theorem that concludes a Boolean field
already supplied by the record may still be useful as traceability, but it must
not be presented as a substantive safety proof. Safety-critical chapters should
move toward domain models where the protected property is derived from state,
order, lifecycle, before/after valuations, or review structure.

Tasks:

1. Review all 122 Lean proof targets. Current review is recorded in `docs/proof_adequacy_review.md`.
2. Classify each target as adequate finite-record invariant, useful-but-too-narrow, needs richer state-machine semantics, needs executable tests first, or should remain research agenda. Current target counts are 8 adequate finite-record, 47 useful-but-too-narrow, 19 richer-semantics-needed, 32 executable-tests-needed, 10 empirical/baseline-tests-needed, and 6 research-agenda-until-artifact-import.
3. Update `proofs/proof_triage.json`, `docs/proof_artifact_audit.md`, chapters, and Appendix E only where the review justifies it. Follow-through increments may add proof targets or Lean code, but they must preserve support-state boundaries unless an accepted evidence transition justifies movement.
4. Add or revise Lean code only where a stronger operational predicate is clear. Current Lean follow-through increments include `AsiStackProofs.StackBoundaries`, `AsiStackProofs.ArtifactCompression`, `AsiStackProofs.IntentContracts`, `AsiStackProofs.IntentToExecution`, `AsiStackProofs.CommandContracts`, `AsiStackProofs.BibliographyPlan`, `AsiStackProofs.CognitiveCompilation`, `AsiStackProofs.VirtualContextABI`, `AsiStackProofs.VerificationBandwidth`, `AsiStackProofs.TypedJobs`, `AsiStackProofs.StableCapabilityFields`, `AsiStackProofs.Replacement`, `AsiStackProofs.SecurityKernel`, `AsiStackProofs.SelfImprovement`, `AsiStackProofs.Authority`, `AsiStackProofs.FailureModes`, `AsiStackProofs.Planning`, `AsiStackProofs.EvidenceStates`, `AsiStackProofs.BenchmarkRatchets`, `AsiStackProofs.ArtifactStewardAgents`, `AsiStackProofs.ClaimLedger`, `AsiStackProofs.ProofCarryingClaims`, `AsiStackProofs.RuntimeAdapters`, `AsiStackProofs.ProceduralMemory`, `AsiStackProofs.Routing`, `AsiStackProofs.ArtifactGraph`, `AsiStackProofs.MoECOTRuntime`, and `AsiStackProofs.ReferenceArchitecture`; all remain finite-record envelopes.
5. Maintain the proof-depth classifier in `scripts/validate_proof_depth.py` and the generated report in `docs/proof_depth_classification.md`. The validator is CI-wired and should keep flagging theorem bodies that are pure projection patterns, such as `intro ...; exact valid ...`, when those targets are described as implemented formal invariants rather than traceability hooks.
6. Treat the current v1.0 safety-critical route as explicit projection-only traceability in the relevant chapter limitation prose. Future deeper replacements for `SelfImprovement`, `Alignment`, `Corrigibility`, `GovernanceRights`, and `ValueConflict` should move toward the `Authority` and `Planning` pattern: explicit state, transitions, ordering or lifecycle rules, and derived conclusions.
7. Where a projection theorem remains intentionally narrow, record that classification in the proof adequacy review and chapter limitation prose instead of letting it sound like a broad formal result.

Acceptance criteria:

- A public-safe proof adequacy review exists.
- `cd lean && lake build` passes.
- Proof text and chapter limitation prose still do not overclaim.
- Safety-critical formal hooks are either upgraded beyond record-projection proofs or explicitly classified as projection-only traceability.
- The proof-readiness validator fails or warns when a new theorem is represented as a substantive invariant but is only a projection from an assumed predicate.
- The proof-depth classifier records a tracked derived-vs-projection split over time, so de-vacuifying progress is measurable rather than impressionistic.
- Current v1.0 status: satisfied by explicit projection-only traceability classifications in all five safety-critical chapter Formalization hooks sections. This does not strengthen the Lean proofs or promote support states.

## Phase 5 - First Real Test Harnesses [v1.0-blocking]

Status: initial harness set complete, extended, registry-runnable, and used for the first bounded replayed-slice transition. Twenty-five synthetic or deterministic harnesses are implemented: twenty-two registry-controlled harnesses plus three book-gate-only harnesses for Artifact Graph replay, Procedural Memory loop qualification, and Routing decision lease discipline. The registry-controlled set includes the claim ledger revision harness in `scripts/validate_claim_ledger_revision.py`, documented in `docs/claim_ledger_revision_harness.md`; the proof-carrying claim harness in `scripts/validate_proof_carrying_claims.py`, documented in `docs/proof_carrying_claim_harness.md`; the tribunal review harness in `scripts/validate_tribunal_review.py`, documented in `docs/tribunal_review_harness.md`; the value conflict harness in `scripts/validate_value_conflicts.py`, documented in `docs/value_conflict_harness.md`; the constitutional alignment harness in `scripts/validate_constitutional_alignment.py`, documented in `docs/constitutional_alignment_harness.md`; the governance rights harness in `scripts/validate_governance_rights.py`, documented in `docs/governance_rights_harness.md`; the agency rights harness in `scripts/validate_agency_rights.py`, documented in `docs/agency_rights_harness.md`; the support-state transition harness in `scripts/validate_support_state_transitions.py`, documented in `docs/support_state_transition_harness.md`; the authority transition harness in `scripts/validate_authority_transitions.py`, documented in `docs/authority_transition_harness.md`; the security kernel harness in `scripts/validate_security_kernel.py`, documented in `docs/security_kernel_harness.md`; the stable capability fields harness in `scripts/validate_stable_capability_fields.py`, documented in `docs/stable_capability_field_harness.md`; the capability replacement harness in `scripts/validate_capability_replacement.py`, documented in `docs/capability_replacement_harness.md`; the self-improvement boundary harness in `scripts/validate_self_improvement_boundaries.py`, documented in `docs/self_improvement_boundary_harness.md`; the plan-execution contract harness in `scripts/validate_plan_execution_contracts.py`, documented in `docs/plan_execution_contract_harness.md`; the runtime adapter permission harness in `scripts/validate_runtime_adapter_permissions.py`, documented in `docs/runtime_adapter_permission_harness.md`; the context admission/adequacy harness in `scripts/validate_context_admission_adequacy.py`, documented in `docs/context_admission_adequacy_harness.md`; the readiness/residual gate harness in `scripts/validate_readiness_residual_gates.py`, documented in `docs/readiness_residual_harness.md`; the benchmark anti-Goodhart harness in `scripts/validate_benchmark_antigoodhart.py`, documented in `docs/benchmark_antigoodhart_harness.md`; the generation mode baseline harness in `scripts/validate_generation_mode_baselines.py`, documented in `docs/generation_mode_baseline_harness.md`; the resource budget ledger harness in `scripts/validate_resource_budget_ledgers.py`, documented in `docs/resource_budget_ledger_harness.md`; the reference trace harness in `scripts/validate_reference_trace.py`, documented in `docs/reference_trace_harness.md`; and the capacity smoothing toy harness in `scripts/validate_capacity_smoothing.py`, documented in `docs/capacity_smoothing_harness.md`. The twenty-two registry-controlled harnesses are backed by valid plus expected-invalid fixtures under `experiments/`, wired into `scripts/validate_book.py`, registered in `experiments/phase5_harness_registry.json`, and executable as a registry-controlled suite through `python3 scripts/run_phase5_harnesses.py`; the book-gate-only Artifact Graph replay harness is backed by 2 valid and 6 expected-invalid fixtures under `experiments/artifact_graph_replay/`, the book-gate-only Procedural Memory loop harness is backed by 3 valid and 6 expected-invalid fixtures under `experiments/procedural_memory_loop/`, the book-gate-only Routing decision lease harness is backed by 3 valid and 6 expected-invalid fixtures under `experiments/routing_decision_lease/`, and all three run through `scripts/validate_book.py`; the latest runner report in `docs/phase5_harness_runner.md` records 22 of 22 registered harnesses passing return-code and expected-summary checks. `python3 scripts/validate_phase5_harness_registry.py` checks their docs, commands, fixture counts, result records, Appendix E rows, public status references, primary chapter mappings, and non-claim boundaries. No chapter core support state changed.

Purpose: move beyond schema shape validation into executable behavior checks.

Start with small deterministic tests that help many chapters:

| Harness | Primary chapters |
|---|---|
| Claim ledger revision harness | Claim ledgers; evidence states; proof-carrying claims; living-book methodology |
| Proof-carrying claim harness | Spinoza; claim ledgers; proof envelope; UAT |
| Tribunal review harness | UAT; Spinoza; moral uncertainty; benchmark ratchets |
| Value conflict harness | Moral uncertainty; UAT; governance rights; constitutional alignment |
| Constitutional alignment harness | Constitutional alignment; moral uncertainty; agency; recursive self-improvement |
| Governance rights harness | Governance rights; agency; stable capability fields; artifact stewardship |
| Agency rights harness | Agency; governance rights; constitutional alignment; runtime adapters |
| Support-state transition checker | Evidence states; claim ledgers; benchmark ratchets; living-book methodology |
| Authority non-escalation and permission receipts | System boundaries; security kernel; runtime adapters; labor OS |
| Security kernel harness | Security kernel; system boundaries; runtime adapters; context transactions |
| Stable capability fields harness | Stable capability fields; replacement; recursive self-improvement; governance rights |
| Capability replacement harness | Capability replacement; stable capability fields; recursive self-improvement; readiness gates |
| Self-improvement boundary harness | Recursive self-improvement; constitutional alignment; capability replacement; stable capability fields; readiness gates |
| Plan graph and execution-contract tests | Intent contracts; command contracts; planning; PlanForge; cognitive compilation |
| Runtime adapter permission and approval tests | Runtime adapters; security kernel; Labor OS; artifact graphs |
| Context admission versus adequacy tests | Virtual Context ABI; semantic pages; context transactions; verification bandwidth |
| Routing decision lease tests | Routing; MoECOT; readiness gates; stable capability fields; resource economics |
| Readiness gate and residual escrow tests | Routing; readiness gates; MoECOT; prototype roadmap; recursive self-improvement |
| Benchmark ratchet anti-Goodhart tests | Benchmark ratchets; policy optimization; artifact steward agents |
| Generation mode baseline accounting tests | Fast generation architectures; efficient ASI hypothesis; resource economics |
| Resource budget ledger tests | Resource economics; efficient ASI hypothesis; planning; runtime adapters; benchmark ratchets |
| Reference trace tests | Integrated reference architecture; intent contracts; planning; VCM; runtime adapters; recursive self-improvement |
| Capacity smoothing toy traces | Resource economics; efficient ASI hypothesis; planning; PlanForge |

Acceptance criteria:

- Tests have commands, fixtures, environment notes, result records, and non-claims.
- Failed or inconclusive tests remain visible.
- Appendix E and relevant chapters distinguish fixture validation from behavior validation.
- The Phase 5 harness registry validates that the initial harness set stays wired across scripts, docs, fixtures, result records, Appendix E, and public status pages.

Initial completion:

- `python3 scripts/validate_support_state_transitions.py` passed locally on 2026-06-30 with 4 valid fixtures and 4 expected-invalid fixtures.
- The result record is `experiments/support_state_transitions/results/2026-06-30-local.md`.
- The harness is a gate-semantics test only. It does not promote Appendix C, validate source interpretation, prove proof adequacy, or exercise AI runtime behavior.
- `python3 scripts/validate_claim_ledger_revision.py` passed locally on 2026-06-28 with 3 valid fixtures and 4 expected-invalid fixtures.
- The result record is `experiments/claim_ledger_revision/results/2026-06-28-local.md`.
- The claim ledger revision harness checks synthetic claim-revision, contradiction quarantine, split, surface propagation, history preservation, and non-claim boundary behavior only. It does not prove source interpretation, verifier quality, open-domain claim extraction, deployed belief revision, runtime behavior, or support-state promotion.
- `python3 scripts/validate_proof_carrying_claims.py` passed locally on 2026-06-28 with 3 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/proof_carrying_claims/results/2026-06-28-local.md`.
- The proof-carrying claim harness checks synthetic verifier artifact refs, tier/justification alignment, bounded review eligibility, failed-attempt preservation, mismatch escalation, and non-claim boundaries only. It does not prove theorem validity, semantic equivalence, citation accuracy, verifier quality, open-domain formalization, runtime behavior, or support-state promotion.
- `python3 scripts/validate_tribunal_review.py` passed locally on 2026-06-28 with 3 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/tribunal_review/results/2026-06-28-local.md`.
- The tribunal review harness checks synthetic dossier refs, reviewer roles, adversarial probes, evidence-backed accept verdicts, dissent preservation, prior-review guards, required actions, constraint effects, and non-claim boundaries only. It does not prove reviewer independence, adversarial-review quality, consensus quality, verdict correctness, source interpretation, runtime behavior, or support-state promotion.
- `python3 scripts/validate_value_conflicts.py` passed locally on 2026-06-28 with 3 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/value_conflicts/results/2026-06-28-local.md`.
- The value conflict harness checks synthetic multi-axis conflict classification, stakeholder/evidence requirements, high-stakes review routing, residual uncertainty preservation, authority narrowing, dissent payloads, and bounded-decision revisit conditions only. It does not prove moral correctness, value-conflict classification quality, reviewer independence, human-review quality, tribunal quality, runtime policy behavior, source interpretation, or support-state promotion.
- `python3 scripts/validate_constitutional_alignment.py` passed locally on 2026-06-28 with 3 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/constitutional_alignment/results/2026-06-28-local.md`.
- The constitutional alignment harness checks synthetic protected scope, operational tests, conflict routing, review routes, self-modification weakening rules, migration policies, least-sufficient-power behavior, uncertainty preservation, and non-claim boundaries only. It does not prove deployed constitutional alignment, moral correctness, runtime policy behavior, source interpretation, self-modification safety, predicate-translation adequacy, review quality, or support-state promotion.
- `python3 scripts/validate_governance_rights.py` passed locally on 2026-06-28 with 3 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/governance_rights/results/2026-06-28-local.md`.
- The governance rights harness checks synthetic audit material and receipts, redaction appeal paths, usable exit/fork access paths, fork safety constraints, preservation obligations, durable record paths, and non-claim boundaries only. It does not prove institutional governance rights, legal rights, runtime right enforcement, deployed fork/exit usability, reviewer independence, source interpretation, or support-state promotion.
- `python3 scripts/validate_agency_rights.py` passed locally on 2026-06-28 with 3 valid fixtures and 6 expected-invalid fixtures.
- The result record is `experiments/agency_rights/results/2026-06-28-local.md`.
- The agency rights harness checks synthetic affected parties, bounded delegation, material usability, timing-before-effect review, review and appeal channels, corrigibility paths, high-impact approval, residual dependency risk, degradation reasons, and accountable principals only. It does not prove deployed agency preservation, dignity preservation, manipulation resistance, consent quality, reviewer independence, runtime policy behavior, source interpretation, or support-state promotion.
- `python3 scripts/validate_authority_transitions.py` passed locally on 2026-06-28 with 3 valid fixtures and 3 expected-invalid fixtures.
- The result record is `experiments/authority_transitions/results/2026-06-28-local.md`.
- The authority harness checks synthetic non-escalation, permission-separation, denial-receipt, approval-escalation, and confused-deputy shortcut behavior only. It does not prove deployed authorization enforcement, runtime adapter safety, secret handling, revocation propagation, or support-state promotion.
- `python3 scripts/validate_security_kernel.py` passed locally on 2026-06-28 with 3 valid fixtures and 6 expected-invalid fixtures.
- The result record is `experiments/security_kernel/results/2026-06-28-local.md`.
- The security kernel harness checks synthetic handle mediation, approval artifacts, bounded action scope, SCIF lifecycle completeness, sanitization, residual leak-risk notes, revocation paths, and prompt-injection non-disclosure boundaries only. It does not prove kernel security, sandbox isolation, side-channel safety, prompt-injection containment, secret-handle safety, least-privilege context behavior, runtime policy behavior, source interpretation, or support-state promotion.
- `python3 scripts/validate_stable_capability_fields.py` passed locally on 2026-06-28 with 3 valid fixtures and 6 expected-invalid fixtures.
- The result record is `experiments/stable_capability_fields/results/2026-06-28-local.md`.
- The stable capability fields harness checks synthetic qualification predicates, evidence refs, readiness refs, authority ceilings, route scopes, route permission effects, evaluator independence, review triggers, rollback obligations, default-route blockers, and non-claim boundaries only. It does not prove runtime route validity, capability identity, evaluator integrity, authority enforcement, replacement safety, rollback execution, source interpretation, or support-state promotion.
- `python3 scripts/validate_capability_replacement.py` passed locally on 2026-06-28 with 3 valid fixtures and 6 expected-invalid fixtures.
- The result record is `experiments/capability_replacement/results/2026-06-28-local.md`.
- The capability replacement harness checks synthetic replacement-transaction field identity, qualification evidence, regression results, non-widening authority checks, evaluator separation, residual escrow, rollback receipts, approvals, monitor state, promotion blockers, and non-claim boundaries only. It does not prove deployed replacement behavior, runtime route quality, evaluator integrity, authority enforcement, rollback execution, regression quality, source interpretation, or support-state promotion.
- `python3 scripts/validate_self_improvement_boundaries.py` passed locally on 2026-06-28 with 3 valid fixtures and 7 expected-invalid fixtures.
- The result record is `experiments/self_improvement_boundaries/results/2026-06-28-local.md`.
- The self-improvement boundary harness checks synthetic self-improvement transition protected invariants, evaluator separation, cheaper-intervention ordering, authority non-widening, governance review, monitor windows, rollback paths, and no-promotion language only. It does not prove deployed self-improvement behavior, runtime optimization, evaluator integrity, authority enforcement, rollback execution, regression quality, recursive self-improvement safety, source interpretation, or support-state promotion.
- `python3 scripts/validate_plan_execution_contracts.py` passed locally on 2026-06-28 with 2 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/plan_execution_contracts/results/2026-06-28-local.md`.
- The plan-execution harness checks synthetic command-contract, plan-graph, PlanForge DAG, semantic-atom, and typed-job consistency only. It does not prove planner quality, scheduler behavior, deployed execution, runtime adapter safety, parser quality, benchmark performance, or support-state promotion.
- `python3 scripts/validate_runtime_adapter_permissions.py` passed locally on 2026-06-28 with 2 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/runtime_adapter_permissions/results/2026-06-28-local.md`.
- The runtime adapter permission harness checks synthetic typed-job, runtime-adapter-invocation, and authority-use-receipt consistency for permission coverage, high-impact approval gates, approval expiry markers, effect receipts, rollback handles, irreversible residuals, and authority receipt alignment only. It does not prove deployed adapter behavior, sandbox isolation, approval-service quality, secret-handle safety, rollback execution, runtime behavior, or support-state promotion.
- `python3 scripts/validate_context_admission_adequacy.py` passed locally on 2026-06-28 with 3 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/context_admission_adequacy/results/2026-06-28-local.md`.
- The context admission/adequacy harness checks synthetic context ABI, packet, certificate, transaction, and adequacy consistency only. It does not prove VCM resolver behavior, context compiler behavior, memory-store correctness, summary fidelity, contradiction-rate performance, distractor resistance, model verification bandwidth, runtime behavior, or support-state promotion.
- `python3 scripts/validate_readiness_residual_gates.py` passed locally on 2026-06-28 with 4 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/readiness_residual_gates/results/2026-06-28-local.md`.
- The readiness/residual gate harness checks synthetic costed-route, readiness-gate, and replacement-transaction consistency only. It does not prove routing accuracy, readiness-engine behavior, residual-ledger storage, deployed quarantine, rollback execution, runtime monitoring, MoECOT replay, benchmark performance, or support-state promotion.
- `python3 scripts/validate_routing_decision_lease.py` passed locally on 2026-06-30 with 3 valid fixtures and 6 expected-invalid fixtures.
- The result record is `experiments/routing_decision_lease/results/2026-06-30-local.md`.
- The routing decision lease harness checks synthetic specialist registry, routing decision, and MoECOT orchestration packets for least-capable adequate selection, overprivileged specialist rejection, missing-readiness fallback, expired-lease residualization, rejected-candidate evidence, residual ownership, and MoECOT source-boundary non-claims only. It does not prove routing accuracy, learned-router quality, specialist quality, deployed authority enforcement, runtime route execution, MoECOT replay, benchmark performance, or support-state promotion.
- `python3 scripts/validate_benchmark_antigoodhart.py` passed locally on 2026-06-28 with 2 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/benchmark_antigoodhart/results/2026-06-28-local.md`.
- The benchmark anti-Goodhart harness checks synthetic benchmark-ratchet, policy-optimization, and steward-action consistency only. It does not prove benchmark quality, hidden-holdout integrity, contamination detection, transfer performance, policy-training quality, reward-hacking resistance, steward-agent behavior, release safety, or support-state promotion.
- `python3 scripts/validate_generation_mode_baselines.py` passed locally on 2026-06-28 with 2 valid fixtures and 4 expected-invalid fixtures.
- The result record is `experiments/generation_mode_baselines/results/2026-06-28-local.md`.
- The generation mode baseline harness checks deterministic generation-mode and resource-budget fixture accounting for run, baseline, and negative-control refs, useful-solution-per-second plus quality and residual metrics, fallback behavior, resource-budget alignment, latency-only proxy rejection, and no-promotion boundaries only. It does not prove generation speed, speculative decoding quality, diffusion generation quality, KV-cache throughput, routing quality, useful-solution-per-second performance, model quality, runtime behavior, or support-state promotion.
- `python3 scripts/validate_resource_budget_ledgers.py` passed locally on 2026-06-28 with 5 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/resource_budget_ledgers/results/2026-06-28-local.md`.
- The resource budget ledger harness checks deterministic Resource Budget Record decisions for low-risk dispatch, high-risk escalation, protected-overhead dispatch, displaced-cost residualization, scarce review-capacity deferral, evidence refs, and no-promotion boundaries only. It does not prove budget scheduling, load stability, verification-tax optimization, KV-cache behavior, runtime budget enforcement, economic outcomes, or support-state promotion.
- `python3 scripts/validate_reference_trace.py` passed locally on 2026-06-30 with 2 valid fixtures and 6 expected-invalid fixtures.
- The result record is `experiments/reference_trace/results/2026-06-30-local.md`.
- The reference trace harness checks deterministic Reference Trace Record fixtures for parent artifact continuity, authority-chain and authority-delta visibility, layer coverage from intent through SCF, artifact count, evidence and residual deltas, validation commands, source-note refs, blocked-path stop conditions, promotion blockers, non-promoting support effects, and explicit non-claims only. It does not prove an integrated ASI Stack runtime, deployed layer behavior, artifact continuity in a live trace, authority-stop enforcement, runtime replay, model quality, benchmark performance, safety, or support-state promotion.
- `python3 scripts/validate_capacity_smoothing.py` passed locally on 2026-06-28 with 2 valid fixtures and 3 expected-invalid fixtures.
- The result record is `experiments/capacity_smoothing/results/2026-06-28-local.md`.
- The capacity smoothing toy harness checks deterministic bounded-capacity trace arithmetic, priority deferral under blocked high-risk work, scope reduction, overload rejection, and no-promotion boundaries only. It does not prove TokenMana behavior, budget scheduling, review-queue optimization, real load stability, runtime behavior, human outcomes, economic outcomes, or support-state promotion.
- `python3 scripts/validate_phase5_harness_registry.py` records the twenty-two-harness set in `experiments/phase5_harness_registry.json` and validates traceability across command scripts, fixture counts, public harness docs, result records, Appendix E, the v1.0 status/roadmap surfaces, primary chapter IDs, and `scripts/validate_book.py`.
- `python3 scripts/run_phase5_harnesses.py --write-report` reran the twenty-two registered harnesses locally and wrote `docs/phase5_harness_runner.md`; all twenty-two returned success and matched their registry summaries.
- The registry and runner now support the bounded repository-infrastructure transition recorded in `docs/first_measured_replayed_slice.md`, while `docs/costed_route_resource_slice.md` records the separate bounded synthetic costed-route/resource-budget selector transition. These records prove neither deployed runtime behavior nor benchmark quality, and they do not promote any chapter core support state.

Next Phase 5 evidence work should move from synthetic record gates, selector slices, and one imported receipt replay toward deeper replayable empirical slices or prototype traces where the source artifacts are available and public-safe.

CI and evidence-depth hardening additions:

- Maintain the validator-coverage check that enumerates `scripts/validate_*.py` and fails unless each validator is covered by `publish.yml`, covered by `scripts/validate_book.py`, or listed in `scripts/validator_coverage_allowlist.json` with a reason. The current check explicitly asserts coverage for `validate_source_notes.py`, `validate_proof_readiness.py`, `validate_evidence_transitions.py`, and every registered Phase 5 harness.
- Maintain the registry-driven harness runner so `experiments/phase5_harness_registry.json` can execute the current harness set rather than only checking registry traceability. Current command: `python3 scripts/run_phase5_harnesses.py`; latest recorded run: `docs/phase5_harness_runner.md`.
- Preserve the current explicit harness result records, the first registry-runner transition, the bounded costed-route/resource-budget selector transition, and the Circle external receipt transition, but prioritize the next increment toward deeper prototype or empirical measured/replayed evidence: a real route-quality/resource-budget trace, a compression/RankFold measurement, a context-admission replay, a planner/runtime adapter trace, a public proof-contract consumer-gate trace, or another public-safe prototype slice with command, environment, input, output, negative control or discarded-attempt boundary, and non-claim boundaries.
- Do not add more synthetic harnesses just because the pattern is easy. Add them only when they unlock a named evidence transition, proof adequacy upgrade, protocol-spec reconciliation, or reader-release blocker.

## Phase 5A - Protocol Record Source-Of-Truth Hardening [v1.0-blocking]

Status: initial v1-critical crosswalk implemented. `protocols/v1_critical_protocol_crosswalk.json` and `docs/protocol_record_crosswalk.md` now reconcile 10 v1-critical protocol records across JSON Schemas, synthetic fixture directories, harness validators, result records, Appendix E markers, primary chapters, and Lean structures where a Lean abstraction exists. The generated report currently covers 204 schema fields with 0 validation errors. This is a drift and traceability gate only; it does not make schema, harness, fixture, or Lean lanes semantically equivalent.

Purpose: reduce drift between JSON Schemas, Lean record abstractions, Python harness logic, and fixtures.

Current risk: many protocol concepts exist in three or four hand-maintained
forms. The JSON schema may carry rich fields, the Lean record may carry a
smaller abstraction, the fixtures may instantiate a third shape, and the Python
harness may encode additional semantics. This is acceptable while the book is
exploring, but v1 should at least make intentional abstractions explicit.

Tasks:

1. Maintain the v1-critical protocol-record crosswalk for authority transitions, runtime adapter invocations, self-improvement transitions, capability replacement, readiness gates, claim-ledger revision, proof-carrying claims, tribunal review, value conflicts, and resource-budget records.
2. Maintain the field-reconciliation validator in `scripts/validate_protocol_crosswalk.py`. It compares schema fields with Lean structure fields where a Lean structure claims to formalize the same record and requires explicit harness-only or intentional-abstraction routes for every remaining schema field.
3. Expand the same crosswalk pattern to additional schema-backed records only when they become v1-blocking or when an evidence transition depends on them.
4. Decide whether a single record spec should generate schema, fixture skeletons, and Lean structure stubs for future records; do not build that generator until the v1-critical crosswalk has stabilized.
5. Stretch only after the crosswalk is stable: make selected Lean validity predicates executable and run the same public-safe fixtures through Python and Lean so spec and implementation can be compared.

Acceptance criteria:

- Every v1-critical protocol record has an explicit schema/fixture/harness/Lean crosswalk or an explicit reason why one lane does not apply.
- Schema-to-Lean mismatches are either resolved or recorded as intentional abstractions with a chapter-facing limitation.
- No protocol record is treated as verified merely because one lane passes.

## Phase 6 - External Literature Backfill [v1.0-complete for placement gate]

Status: complete for the v1.0 placement gate and still open as a v1.x literature-deepening lane. Initial backfill passes added fifty-nine primary external source records and source notes across alignment/control, AI governance/evaluation, planning/agent control, retrieval/context, formal methods, routing/MoE, compression/representation, and benchmark science, summarized in `docs/external_literature_backfill_phase6.md`. The planning slice now includes ReAct, Tree of Thoughts, PDDL, SHOP2, Integrated TAMP, behavior trees, GOAP/F.E.A.R., and AutoGen as comparison vocabulary only. The retrieval/context slice now includes RAG, Lost in the Middle, MemGPT, LongBench, RULER, ALCE, Self-RAG, and LongLLMLingua as context-interface, citation-support, adaptive-retrieval, long-context-evaluation, and prompt-compression vocabulary only. The formal-methods slice now includes proof-carrying code, TLA+, Lean theorem proving, Dafny, Reluplex, Black-Box Simplex, Copilot, and PRISM as proof, specification, property-verification, runtime-assurance, monitor-generation, and probabilistic-model-checking vocabulary only. The routing/MoE slice now includes sparse MoE, GShard, Switch Transformers, Expert Choice Routing, Mixtral, an MoE-in-LLMs survey, FrugalGPT, Hybrid LLM, and RouteLLM as model-routing, task-routing, cost-quality routing, and learned-router vocabulary only. The compression slice now includes Deep Compression, LoRA, knowledge distillation, GPTQ, QLoRA, DreamCoder, Information Bottleneck, MDL, and CodeBLEU as compression, adaptation, program-synthesis, residual-accounting, and artifact-metric vocabulary only. The benchmark-science slice now includes MMLU, BIG-bench, HELM, GPQA, SWE-bench, LiveBench, Dynabench, CheckList, benchmark-contamination work, and Goodhart variants as benchmark-design, dynamic-evaluation, contamination, behavioral-testing, and anti-Goodhart vocabulary only. `docs/external_sota_positioning_audit.md` and `python3 scripts/validate_external_sota_positioning.py --release` now close the prose-placement gate: 44 of 44 chapters have `ext_*` positioning before the Source crosswalk, 0 have explicit external-baseline exceptions, 0 have source-noted external targets still waiting for placement, and 0 need an exception or added source-noted external baseline. No claim support state, reproduction result, compliance claim, imported formal artifact, proof-assistant import, verifier run, planner run, motion-planning run, context benchmark run, citation-evaluation run, context-compression run, runtime-assurance case study, generated monitor, probabilistic model-checking run, route benchmark, router training, MoE training or inference run, compression experiment, program-synthesis run, information-bottleneck or MDL scorer implementation, CodeBLEU run, dynamic benchmark run, behavioral-test run, contamination audit, Goodhart taxonomy over local tests, finetuning run, benchmark run, or evidence transition changed.

Purpose: ground the architecture against third-party literature where outside readers will expect comparison.

Priority queues:

1. Alignment, corrigibility, power-seeking, and control.
2. AI governance, evaluations, deployment policy, incident response, and model evals.
3. Planning, task decomposition, PlanForge translation comparisons, and deeper planning-runtime adapter comparisons.
4. Memory systems, context engineering surveys, VCM-specific adapter comparisons, and any additional provenance/compression sources needed after chapter-level review.
5. Proof-assistant adequacy, ASI Stack protocol-verification comparisons, and additional deployment model-checking sources needed after chapter-level review.
6. Governance-aware route selection, routing-specific modular-agent orchestration, and additional model/system routing comparisons needed after chapter-level review.
7. Program synthesis, residual coding, artifact-utility metrics, compression-regression testing, representation learning, and residual/error accounting.
8. Hidden-test operations, saturation analysis, contamination audits, benchmark-gaming/evaluator-gaming sources, and release-grade benchmark governance.

Acceptance criteria:

- No source is cited from memory.
- Each used source has a source record, source note, chapter assignment, and support boundary.
- External literature remains separate from Corben/local sources in Appendix H.
- Every chapter's Problem, insufficiency, or Beyond-SOTA section either names the relevant external baseline it is positioning against or explicitly records why no external baseline is being used there.
- Adding in-prose external positioning does not by itself promote support states.
- `docs/external_sota_positioning_audit.md` is current, the default validator passes, and the stricter release gate passes with `python3 scripts/validate_external_sota_positioning.py --release`.

## Phase 7 - Visual, Site, Toolchain, And Archival Review [v1.0-blocking]

Status: complete for v1.0.0 release metadata and still open for v1.x quality
work. The first rendered-site and visual audit is recorded in
`docs/site_visual_phase7_review.md`; automated visual coverage, rendered
Human-view validation, all-chapter/all-viewport browser validation, and a mobile
screenshot review of the densest diagrams passed after Mermaid diagrams gained
contained mobile scrolling. A second local browser probe after the Phase 6
source expansion checked the landing page, fast-generation and
recursive-improvement chapters, and Appendices A/C/H at desktop and mobile sizes
with zero page-level horizontal overflow and visible reading-mode toggles. A
follow-up probe after the source inventory reached 160 records found Appendix F
overflow from long inline `code` spans, added scoped inline-code wrapping in
`assets/styles.scss`, and rechecked the landing page, dense chapters, and
Appendices A/C/F/H/K with zero page-level horizontal overflow at desktop and
mobile sizes. The fast-generation mechanism is now split into selector and
acceptance/accounting diagrams, and the recursive self-improvement mechanism is
now split into boundary-review and canary/promotion diagrams.
`docs/release_reproducibility.md` now records the v1.0.0 toolchain and citation
boundary, `CITATION.cff` records version `1.0.0`, `.github/workflows/publish.yml`
pins Quarto/Python/Node while using `lean/lean-toolchain`, and
`scripts/validate_release_reproducibility.py` checks those facts.
`docs/public_site_accessibility_review.md` now records the live-site
accessibility readiness boundary, residuals, and non-claims; `docs/v1_progress_ledger.md`
records the compact phase status and release classification;
`docs/v1_0_release_gate_audit.md` records all eleven Definition-of-Done gates
with evidence, residuals, tag `v1.0.0`, source commit
`96d0ca3c6b62f3530202535573941b1f6e50a83d`, and GitHub Release facts; and
`scripts/validate_public_site_accessibility.py` plus
`scripts/validate_v1_release_gate_audit.py` check those ledgers. Future visual
work should review e-reader legibility rather than keeping those splits open as
unresolved.

Purpose: improve trust and usability after the manuscript voice and evidence path are stronger.

Tasks:

- Manual diagram audit for overloaded or low-legibility Mermaid diagrams; first mobile screenshot pass is recorded for the densest diagrams.
- Mobile and desktop Human-view inspection.
- Landing page status and trust review.
- Continue table and inline-code overflow checks after large source, claim-matrix, or changelog growth; the current source-growth and inline-code probes found no page-level overflow on Appendices A/C/F/H/K.
- Maintain the accessibility review for Mermaid diagrams and dense technical figures: text equivalents, color contrast boundaries, mobile legibility, e-reader legibility residuals, and status-banner clarity are now recorded in `docs/public_site_accessibility_review.md`.
- Consolidate process-record sprawl where it interferes with roadmap readability: keep detailed records in structured ledgers, then render short public summaries for roadmap/status pages.
- Maintain `docs/v1_progress_ledger.md` and `docs/v1_0_release_gate_audit.md` so completed Phase 2, Phase 5, and Phase 6 history can move out of the execution roadmap over time; the roadmap should foreground remaining blockers, acceptance criteria, and release gates.
- Keep `docs/release_reproducibility.md`, `CITATION.cff`, `.github/workflows/publish.yml`, and `scripts/validate_release_reproducibility.py` current when Quarto, Python, Node, Lean, reader-format dependencies, local tool paths, locale requirements, fonts, DOI/Zenodo state, or release citation status changes.
- After v1.0.0, change release metadata only with facts that exist: a new version/tag, release-record date, commit, DOI/Zenodo identifier if issued, or explicit DOI-pending language if not issued.
- Maintain `schemas/book_structure.schema.json` alongside future manifest fields; the schema now validates the top-level book contract before the semantic validators check source IDs, proof targets, reader surfaces, and evidence boundaries.
- Keep the `validate_live_human_view.py` preflight current so missing, incomplete, or stale `_site` output fails with render-first guidance before page-level checks run.
- Optional local `git gc` if loose-object warnings recur.

Acceptance criteria:

- Visual changes do not imply unrecorded proof, benchmark, or runtime behavior.
- Browser validation passes after render.
- Public-site status remains honest about the tagged v1.0.0 release scope and residuals.
- Accessibility review records residuals instead of treating mechanical browser success as polished public-site quality. Current v1.0.0 status: satisfied by `docs/public_site_accessibility_review.md` and `python3 scripts/validate_public_site_accessibility.py`, while keyboard-only, screen-reader, measured contrast, and e-reader artifact reviews remain explicit residuals.
- Release-gate audit records all eleven Definition-of-Done gates, their evidence, residuals, tag, source commit, GitHub Release, and living-book release record. Current v1.0.0 status: satisfied by `docs/v1_0_release_gate_audit.md`, `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`, and `python3 scripts/validate_v1_release_gate_audit.py`.
- Toolchain and citation records are good enough for another reader or future agent to reproduce the v1.0.0 site and identify the exact cited version. Current status: satisfied for tag `v1.0.0` with DOI pending.

## Phase 7A - Architecture-Level Red-Team [v1.0-blocking]

Status: v1.0 desk review complete. `docs/architecture_red_team_review.md`
records all six required scenarios with attack setup, expected failure,
observed current defense, residual risk, and routed follow-up. The report is
validated by `python3 scripts/validate_architecture_red_team.py`. This is a
public-safe desk review only; it is not an exploit run, deployed safety result,
runtime security test, benchmark, source-interpretation audit, or external peer
review.

Purpose: attack the ASI Stack as a composed system, not only as isolated
chapters. Per-chapter failure modes are necessary but insufficient for a
governance/safety architecture.

Required adversarial scenarios:

1. **Authority ladder attack:** a chain of locally valid transitions produces an end-to-end authority escalation that no single layer notices.
2. **SCIF/context leakage attack:** protected information leaks through summaries, residuals, embeddings, tool receipts, generated diagrams, or reader-facing transformations.
3. **Evaluator capture attack:** self-improvement, capability replacement, benchmark promotion, or policy update passes because the evaluator, reviewer, or benchmark became coupled to the candidate.
4. **Support-state inflation attack:** prose polish, source-note existence, or passing fixtures cause a claim to move without the correct evidence lane.
5. **Benchmark gaming attack:** a route, policy, or steward action optimizes a proxy while increasing residual burden, hidden cost, contamination, or regression risk.
6. **Reader-release laundering attack:** the human edition strips or softens a caveat that was meaning-critical in the AI/research edition.

Acceptance criteria:

- A public-safe red-team report records attack setup, expected failure, observed current defense, residual risk, and routed follow-up.
- Findings are routed to proof targets, schemas, tests, source/prose fixes, release blockers, or explicit v1.x deferrals.
- A passing red-team report does not claim safety; it only records that named attacks were attempted and residuals were preserved.
Current v1.0 status: satisfied for desk-review coverage and residual routing,
not for deployed runtime security or safety validation.

## Phase 8 - Major Version Reader And Audio Packaging [v1.0-complete for reader HTML; v1.x for EPUB, audio, and extra formats]

Status: preparation reviewed, with the minimum reader HTML artifact now release-recorded and EPUB/DOCX/PDF still requiring their own full application/layout reviews. `docs/v1_0_release_preparation_review.md` records passing release-profile, reader-spine, reader-boundary, reader-overlay, reader-edition-check, reader-format-check, reader-format dry-run, reader-artifact structural-inspection, EPUB metadata/source-spine probe, DOCX LibreOffice conversion probe, UTF-8 PDF-probe, representative EPUB/PDF/DOCX sampling, broader HTML layout/navigation probing, and audio-script-check commands. `docs/reader_format_dry_run.md` records local HTML/EPUB/DOCX/PDF snapshots in ignored `build/` space, `docs/reader_artifact_inspection_manifest.md` preserves the latest tracked HTML/EPUB/DOCX structural-inspection summary, `docs/reader_html_artifact_browser_review.md` records 118 of 118 generated reader HTML page-view pairs passing in a browser, `release_records/2026-06-29-v1-reader-html-855dc277.json` names the exact reviewed local HTML artifact from source tag `v1.0.0-reader-html-source`, `docs/reader_epub_probe_manifest.md` records the current EPUB metadata/source-spine metrics and sampled source-card appendix entries, `docs/reader_docx_probe_manifest.md` records the current DOCX conversion metrics and sampled source-card appendix pages, `docs/reader_pdf_probe_manifest.md` records the current PDF probe metrics and sampled source-card appendix pages, and `docs/reader_format_review_matrix.md` records the format-level review blockers in a synced ledger. No EPUB, DOCX, PDF, audiobook, e-reader, or audio-embedded EPUB artifact is approved.

Purpose: produce human-consumption artifacts only after the live and reader surfaces are reviewed.

Tasks:

1. Maintain the tagged validated live-book source; for future major versions, tag only after the live/research gate passes.
2. Generate and review reader source.
3. Render HTML, EPUB, DOCX, and PDF only where dependencies and review allow; HTML has the first full local browser artifact review, while EPUB remains the preferred e-reader target for a later application-level review.
4. Record exact produced artifacts in an edition release record.
5. Generate audio script only after reader review.
6. Review spoken treatment for diagrams, tables, code, schemas, and proof-adjacent material.
7. Produce MP3, M4B, or audio-embedded EPUB only after audio generation, packaging checks, and release-record entry.

Acceptance criteria:

- No artifact is claimed from a target profile alone.
- Release records name what exists, what was reviewed, what failed, and what remains unattempted.
- At least one human-consumption artifact has a format-appropriate review record before the project calls the minimum v1 reader packaging complete; EPUB still needs e-reader application review before it can be called the preferred e-reader release.

## Phase 9 - Externalization And Contribution Extraction [post-v1.0]

Status: deferred.

Purpose: keep the field-recognition path visible without letting it block the
first release. Several project contributions may deserve standalone treatment
after the book has a reviewed v1 release.

Candidate extractions:

- Support-state and claim-ledger discipline for living technical books.
- Costed-route/resource-budget ledgers and residual escrow.
- Stable capability fields, readiness gates, and replacement/rollback records.
- Proof-carrying AI contracts and Circle/Theseus transfer boundaries.
- Human/AI dual-edition publishing with reader overlays and release ledgers.
- Architecture-level red-team methodology for governed AI stacks.

Acceptance criteria:

- No Phase 9 work blocks v1.0.
- Each extracted preprint or artifact has its own source/evidence boundary and does not backfill claims into the book without a normal evidence transition.
- External feedback can create v1.x roadmap items, support-state transitions, or errata only after it is recorded and reviewed.

## Best Goal To Set Next

Status after the extended v1.0 run, the 2026-06-29 Claude/Codex reconciliation,
and the v1.0.0 tag: the book is no longer blocked on scaffold, chapter count,
generated prose cleanup, basic reader derivation, initial synthetic record-gate
coverage, or final v1.0 release metadata. The next goal should move into v1.x
quality and evidence depth without weakening the v1.0.0 release boundaries.

Recommended next goal text:

```text
Advance The ASI Stack from tagged v1.0.0 into a v1.x quality-and-evidence pass using docs/v1_0_roadmap.md, docs/v1_progress_ledger.md, docs/v1_0_release_gate_audit.md, docs/book_outline.md, and book_structure.json as the source-of-truth surfaces.

Preserve the v1.0.0 release record exactly: do not promote chapter core claims, approve new artifacts, cite a DOI, or claim new runtime/proof/benchmark results without a new evidence transition or release record. Work on v1.x residuals only: deeper prototype or empirical measured/replayed slices, richer safety-critical proofs where semantics are clear, manual accessibility review, EPUB/DOCX/PDF application review, and curated reader-manuscript graduation if overlays become too small for human-quality prose.

Prioritize in this order: (1) keep the implemented validator-coverage, proof-depth, protocol-crosswalk, Phase 5 harness-runner, bounded measured/replayed slices, core-claim transition/no-promotion coverage, architecture desk red-team, reader HTML edition record, release-reproducibility/citation gate, public-site accessibility readiness ledger, v1 progress ledger, and release-gate audit passing; (2) pursue the next prototype or empirical measured/replayed slice, with Theseus/Circle transfer, real route-quality/resource-budget traces, context-admission, compression, or planner/runtime traces as candidate lanes; (3) keep in-prose external-SOTA positioning or recorded exceptions current for every chapter; (4) pursue manual keyboard-only, screen-reader, contrast, and e-reader-specific site/readability review only when the resulting record is added to the ledger; (5) continue EPUB/DOCX/PDF inspection only as v1.x or promoted-scope work, creating edition release records only for exact reviewed artifacts.

Keep every broad ASI, capability, deployment, benchmark, safety, and performance claim at argument unless a specific accepted transition justifies a narrower state. Treat the accepted Phase 5 registry-runner transition as repository-infrastructure evidence only, the costed-route/resource-budget transition as bounded synthetic selector evidence only, and the Circle external receipt transition as bounded imported prototype receipt evidence only, not as support for chapter core claims. Do not fabricate sources, tests, proof results, benchmark results, prototype traces, reader artifacts, ebook artifacts, audio artifacts, DOI records, or release approvals. Record completed work, skipped work, blockers, validations run, residuals, and release classification in the roadmap, changelog, release ledgers, and relevant appendices before reporting completion.
```

This goal is better than another general "write the book" run because the book
is already structurally complete and mechanically guarded. The highest-value
work is now to keep the explicit release gates green while moving evidence
depth from bounded synthetic slices and the first imported prototype receipt
toward deeper prototype or empirical receipts,
keeping public-site accessibility/progress ledgers current, preserving
proof-depth honesty and protocol source-of-truth checks, and recording DOI,
archive, artifact, or support-state changes only when those facts actually
exist.
