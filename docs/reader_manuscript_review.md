# Reader Manuscript Review Baseline

Last updated: 2026-07-04

This note records the current Phase 2 reader-manuscript baseline for the v1.0 roadmap. It is a review-control document, not a reader release record.

## Generated Baseline

Command run:

```bash
python3 scripts/build_reader_edition.py
```

Generated workspace:

- `build/reader_edition/`
- 44 chapters
- 49 generated files
- target formats listed by profile: HTML, EPUB, PDF, DOCX
- 224 live-only sections removed
- 44 human-only bridges unwrapped
- 44 raw core-claim markers removed
- 39 repeated support-boilerplate passages humanized
- 61 reader scaffold terms humanized
- 74 active reader-overlay operations applied; 2 retired semantic-representation
  operations skipped after the fold

Generated review files inspected:

- `build/reader_edition/READER_RELEASE_CHECKLIST.md`
- `build/reader_edition/companion_notes.md`
- `build/reader_edition/reader_delta_report.md`

Representative generated chapters spot-read:

- `build/reader_edition/chapters/asi-is-a-stack-not-a-model.qmd`
- `build/reader_edition/chapters/the-efficient-asi-hypothesis.qmd`
- `build/reader_edition/chapters/human-intent-as-a-formal-input.qmd`
- `build/reader_edition/chapters/system-boundaries-and-authority.qmd`
- `build/reader_edition/chapters/evidence-states-and-claim-discipline.qmd`
- `build/reader_edition/chapters/constitutional-alignment-substrate.qmd`
- `build/reader_edition/chapters/personal-compute-hives-and-federated-edge-intelligence.qmd`
- `build/reader_edition/chapters/intent-to-execution-contracts.qmd`
- `build/reader_edition/chapters/planning-as-a-control-layer.qmd`
- `build/reader_edition/chapters/verification-bandwidth-and-context-adequacy.qmd`
- `build/reader_edition/chapters/labor-os-and-typed-jobs.qmd`
- `build/reader_edition/chapters/runtime-adapters-tool-permissions-and-human-approval.qmd`
- `build/reader_edition/chapters/policy-optimization-and-learning-from-feedback.qmd`
- `build/reader_edition/chapters/artifact-steward-agents-and-living-project-governance.qmd`
- `build/reader_edition/chapters/compact-generative-systems-and-residual-honesty.qmd`
- `build/reader_edition/chapters/fast-generation-architectures.qmd`
- `build/reader_edition/chapters/rankfold-neuralfold-and-artifact-compression.qmd`
- `build/reader_edition/chapters/mathematical-and-search-substrates.qmd`
- `build/reader_edition/chapters/circle-calculus-and-proof-carrying-ai-contracts.qmd`
- `build/reader_edition/chapters/executable-specifications-and-lean-proof-envelope.qmd`
- `build/reader_edition/chapters/open-research-agenda-and-bibliography-plan.qmd`

## What Is Working

- The generated reader source now has a coherent front door for the book: the first chapter opens as architecture prose rather than live scaffold.
- The Efficient ASI reader overlay converts the route-outcome state table into narrative prose while keeping the canonical AI/research efficiency-accounting matrix and cost/quality/residual boundary in the live source.
- The Human Intent reader overlay converts the intent-intake state table into narrative prose while keeping the canonical AI/research intake-state matrix and intent-contract boundary in the live source.
- The System Boundaries reader overlay converts the permission-class table into narrative prose while keeping the canonical AI/research permission taxonomy and authority-transition boundary in the live source.
- The Evidence States reader overlay converts the claim-source contribution table into narrative prose while keeping the canonical AI/research source-boundary matrix and support-state discipline in the live source.
- The Personal Compute Hives reader overlays convert four table-heavy sections plus the minimum and mature endpoint sections into narrative prose for Human view and generated reader editions while keeping the canonical AI/research tables, implementation ladder, and protocol checklist in the live source.
- The Policy Optimization reader overlay converts method-family and external-literature tables into narrative prose while keeping the canonical AI/research comparison tables in the live source.
- The Artifact Steward Agents reader overlays convert autonomy, treasury, project-object, and mature stewardship endpoint material into narrative prose while keeping the canonical AI/research matrices and lifecycle-control checklist in the live source.
- Semantic Representation is now folded into Compact Generative Systems as Semantic Representation Leasing; its standalone reader overlay is retired, and future reader work should edit the compact chapter's reader path rather than a second semantic-representation chapter.
- The Command Contracts reader overlay converts validation-state and field-status tables into narrative prose while keeping the canonical AI/research state matrix and command-record vocabulary in the live source.
- The Planning reader overlay converts the plan-node lifecycle-state table into narrative prose while keeping the canonical AI/research state matrix and planning-control boundary in the live source.
- The Verification Bandwidth reader overlay converts the adequacy-state table into narrative prose while keeping the canonical AI/research adequacy-state matrix and context/claim verification boundary in the live source.
- The Runtime Adapters reader overlay converts the effect-receipt field table into narrative prose while keeping the canonical AI/research receipt-field matrix and effect-boundary vocabulary in the live source.
- The Fast Generation reader overlay converts metric-code and taxonomy-table material into narrative prose while keeping the canonical AI/research formulas and generation-mode matrix in the live source.
- The Generate-Verify-Repair reader overlay converts the compression-receipt state table into narrative prose while keeping the canonical AI/research receipt-state matrix and exactness/repair/fallback boundary in the live source.
- The RankFold/NeuralFold reader overlay converts the artifact-compression admission-state table into narrative prose while keeping the canonical AI/research state taxonomy and probe/fallback boundary in the live source.
- The Mathematical and Search Substrates reader overlay converts the substrate-adoption lane table into narrative prose while keeping the canonical AI/research promotion-blocker matrix and optional-substrate adoption boundary in the live source.
- The Labor OS reader overlay converts the typed-job lifecycle-state table into narrative prose while keeping the canonical AI/research lifecycle matrix in the live source.
- The Circle Contracts reader overlays convert the proof-receipt lifecycle and mature proof-contract transport sections into narrative prose while keeping the canonical AI/research receipt-state matrix and target transport checklist in the live source.
- The Executable Specifications reader overlay converts the mature proof-envelope target checklist into narrative prose while keeping the canonical AI/research proof/spec registry and semantic-adequacy requirements in the live source.
- Human Reading Path bridges survive as ordinary prose, and reader-spine validation confirms all 44 chapters preserve Handoff continuity.
- Raw core-claim markers and repeated support boilerplate are stripped or humanized while the evidence boundary remains visible in the Core Claim prose.
- Source crosswalks, Codex test plans, drafting guardrails, and most live/research scaffolding are removed from the reader source.
- The reader delta workflow is in the correct shape: tracked overlays are the editable reader-delta source; generated reader files and generated delta reports are disposable review output.

## Automated Continuity Audit

The current generated reader source now has a deterministic heuristic audit at `docs/reader_continuity_audit.md`, generated by:

```bash
python3 scripts/audit_reader_continuity.py --write
```

The audit currently measures 44 reader chapters, 49 generated files, 117,713 reader words, 74 active and applied reader-overlay operations, 0 table rows, 53 Mermaid diagrams, 0 non-Mermaid code blocks, 0 paragraphs at or above 160 words, and 0 repeated first-sentence stems under the current eight-word heuristic. It identifies 0 high-priority and 0 medium-priority heuristic review chapters; the remaining queue is low-priority continuity review, not release approval.

This is review triage, not manual review. It creates a queue for the chapter-by-chapter human pass and helps decide whether a finding should become a canonical prose edit, reader-only overlay, companion-note treatment, or no action.

## Medium-Priority Manual Review

The current generated continuity audit has no high-priority or medium-priority heuristic rows. Four formerly active medium-priority rows have been read, classified, or handled in `docs/reader_continuity_review.md`.

- `executable-specifications-and-lean-proof-envelope`: no additional overlay now; the dense vocabulary is necessary proof-envelope language, and future reader release work should consider companion-note or glossary treatment rather than deleting the proof-lane distinctions.
- `circle-calculus-and-proof-carrying-ai-contracts`: no additional overlay now; the dense terms preserve the theorem-linked receipt versus model-quality boundary, and future reader release work should consider companion-note or glossary treatment.
- `artifact-steward-agents-and-living-project-governance`: retain current reader chapter; the long governance chapter carries central stewardship, treasury, worker-federation, contribution-ledger, event-taint, and sunset concepts. Future curated reader work may compress the implementation ladder or route parts to companion material.
- `compact-generative-systems-and-residual-honesty`: handled by a 2026-07-04 reader-only overlay tightening pass that reduced repeated receipt, record, and residual terminology while keeping exactness, fallback, consumer-policy, Lean/GVR, non-claim, and support-state boundaries visible.
- `artifact-graphs-audit-logs-and-replay`: handled by 2026-07-04 reader-only overlays for the record-reality Mechanism and strongest-objection sections, preserving independent observation, trap checks, challenge/replay routes, trust-base limits, remaining uncertainty, and no-promotion boundaries while keeping the generated reader queue at 0 high and 0 medium rows.

This manual pass does not make the reader manuscript release-reviewed. It only records that the medium-priority rows already reviewed are not immediate blockers for the generated reader path.

## Chapter Review Matrix

The durable Phase 2 queue now lives in
`editions/reader_manuscript/v1_0/chapter_review_matrix.json`, with the public
summary at `docs/reader_chapter_review_matrix.md`. Generate or validate it with:

```bash
python3 scripts/sync_reader_chapter_review_matrix.py --write
python3 scripts/sync_reader_chapter_review_matrix.py --check
```

The current matrix records 44 manifest-aligned chapter rows: 44 `reviewed`
rows from `docs/reader_opening_full_review_pass.md`,
`docs/reader_boundary_full_review_pass.md`, and
`docs/reader_normative_full_review_pass.md`, and
`docs/reader_part_i_full_review_completion.md`, plus
`docs/reader_part_ii_contracts_full_review_pass.md`,
`docs/reader_part_ii_context_full_review_pass.md`,
`docs/reader_part_ii_verification_full_review_pass.md`, and
`docs/reader_part_ii_full_review_completion.md`, plus
`docs/reader_part_iii_opening_full_review_pass.md`,
`docs/reader_part_iii_compression_full_review_pass.md`,
`docs/reader_part_iii_representation_full_review_pass.md`,
`docs/reader_part_iii_iv_proof_bridge_full_review_pass.md`, and
`docs/reader_part_iv_evidence_governance_full_review_pass.md`, and
`docs/reader_part_iv_completion_full_review_pass.md`. It has 0 `spot_checked`
rows, 0 `not_started` rows, 19 chapters with active reader overlays, 44 no-immediate-action decisions, 3 companion-note
candidates, and 44 curated-manuscript candidates. The reviewed rows have cleared
the `full_chapter_review_not_recorded` blocker, but all rows still retain
release blockers until reader release records and format artifact review exist.
The matrix is a chapter-text review queue and release-control surface, not a
reader release or format-artifact approval.

## Residuals

- The generated manuscript now has full chapter-text review records for all 44 chapters. That completes the generated-reader chapter-text queue, but it does not create a tagged reader release, a curated parallel reader manuscript, or reviewed format artifacts.
- The prose is still derived from the live AI/research book. It reads better than the live scaffold, but many chapters still carry technical interfaces, minimum-field lists, Mermaid diagrams, and implementation language that may need compression, rephrasing, or companion-note treatment for relaxed reading.
- Some reader chapters still contain useful but dense schema-like material. The current three companion-note candidates now have routing decisions in `docs/reader_companion_note_routing_review.md` and `editions/reader_manuscript/v1_0/companion_note_routing.json`, plus drafting companion notes under `editions/reader_manuscript/v1_0/companion_notes/`; a final human edition still needs release review before any generated companion notes, e-reader notes, or audio treatment can be approved.
- The original baseline had zero active overlay operations. That baseline has been superseded by the opening-chapter, Efficient ASI, Human Intent, System Boundaries, Evidence States, Personal Compute Hives, Command Contracts, Planning, Verification Bandwidth, Runtime Adapters, Labor OS, Circle Contracts, Generate-Verify-Repair, Fast Generation, RankFold/NeuralFold, Mathematical and Search Substrates, Policy Optimization, Artifact Steward Agents, and Executable Specifications reader-overlay operations in `docs/reader_overlay_pilot.md`; the standalone Semantic Representation overlay operations are retired after the fold, and broader reader-only prose pacing, example insertion, and section-flow edits remain open.
- No EPUB, PDF, DOCX, AZW3, MOBI, Markdown, plain-text, audio, or audio-embedded EPUB artifact has been rendered, reviewed, or released in this pass.
- No curated parallel reader manuscript exists yet. Graduation from generated source plus overlays remains a future decision once reader-only edits become too substantial for overlays.
- The automated continuity audit, reader chapter review matrix, and reader format review matrix are current, but none of them replaces reader-release records, broader layout/navigation review, curated-manuscript reconciliation, application/e-reader inspection, or format artifact approval.

## Next Review Pass

The next Phase 2 pass should:

1. Move from generated-reader chapter-text review into release-focused human-edition work: curated prose decisions, layout/navigation inspection, companion-note release review, and e-reader readability.
2. Classify each finding as a canonical live-book edit, a reader-only overlay, companion-note treatment, or no action.
3. Add reader-only semantic deltas under `editions/reader_overlays/v1_0/` only when the live AI/research source should not change.
4. Keep evidence boundaries, support states, implementation horizons, and non-claims inherited from the live book.
5. Render reader HTML, EPUB, and DOCX only after the manuscript review is recorded. Attempt PDF only when local dependencies support it, then update `editions/reader_manuscript/v1_0/format_review_matrix.json` from actual format-review evidence rather than render success alone.
6. Generate audio-script review output only after the reader manuscript is reviewed.

## Non-Claims

- This baseline does not claim a reviewed reader release exists.
- This baseline does not claim any ebook, document, PDF, audio, or audio-embedded EPUB artifact exists.
- This baseline does not promote any claim support state.
- The live AI/research book remains canonical for claims, support states, source boundaries, proof/test status, implementation horizons, and release records.
