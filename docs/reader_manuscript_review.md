# Reader Manuscript Review Baseline

Last updated: 2026-06-28

This note records the current Phase 2 reader-manuscript baseline for the v1.0 roadmap. It is a review-control document, not a reader release record.

## Generated Baseline

Command run:

```bash
python3 scripts/build_reader_edition.py
```

Generated workspace:

- `build/reader_edition/`
- 54 chapters
- 59 generated files
- target formats listed by profile: HTML, EPUB, PDF, DOCX
- 275 live-only sections removed
- 54 human-only bridges unwrapped
- 54 raw core-claim markers removed
- 50 repeated support-boilerplate passages humanized
- 60 reader scaffold terms humanized
- 25 active reader-overlay operations applied

Generated review files inspected:

- `build/reader_edition/READER_RELEASE_CHECKLIST.md`
- `build/reader_edition/companion_notes.md`
- `build/reader_edition/reader_delta_report.md`

Representative generated chapters spot-read:

- `build/reader_edition/chapters/asi-is-a-stack-not-a-model.qmd`
- `build/reader_edition/chapters/human-intent-as-a-formal-input.qmd`
- `build/reader_edition/chapters/system-boundaries-and-authority.qmd`
- `build/reader_edition/chapters/evidence-states-and-claim-discipline.qmd`
- `build/reader_edition/chapters/agency-dignity-and-corrigibility.qmd`
- `build/reader_edition/chapters/personal-compute-hives-and-federated-edge-intelligence.qmd`
- `build/reader_edition/chapters/command-contracts-and-semantic-interfaces.qmd`
- `build/reader_edition/chapters/planning-as-a-control-layer.qmd`
- `build/reader_edition/chapters/verification-bandwidth-and-context-adequacy.qmd`
- `build/reader_edition/chapters/labor-os-and-typed-jobs.qmd`
- `build/reader_edition/chapters/runtime-adapters-tool-permissions-and-human-approval.qmd`
- `build/reader_edition/chapters/policy-optimization-and-learning-from-feedback.qmd`
- `build/reader_edition/chapters/artifact-steward-agents-and-living-project-governance.qmd`
- `build/reader_edition/chapters/semantic-representation-and-tree-structured-models.qmd`
- `build/reader_edition/chapters/fast-generation-architectures.qmd`
- `build/reader_edition/chapters/rankfold-neuralfold-and-artifact-compression.qmd`
- `build/reader_edition/chapters/circle-calculus-and-proof-carrying-ai-contracts.qmd`
- `build/reader_edition/chapters/generate-verify-repair-compression.qmd`
- `build/reader_edition/chapters/open-research-agenda-and-bibliography-plan.qmd`

## What Is Working

- The generated reader source now has a coherent front door for the book: the first chapter opens as architecture prose rather than live scaffold.
- The Human Intent reader overlay converts the intent-intake state table into narrative prose while keeping the canonical AI/research intake-state matrix and intent-contract boundary in the live source.
- The System Boundaries reader overlay converts the permission-class table into narrative prose while keeping the canonical AI/research permission taxonomy and authority-transition boundary in the live source.
- The Evidence States reader overlay converts the claim-source contribution table into narrative prose while keeping the canonical AI/research source-boundary matrix and support-state discipline in the live source.
- The Personal Compute Hives reader overlay converts four table-heavy sections into narrative prose for Human view and generated reader editions while keeping the canonical AI/research tables in the live source.
- The Policy Optimization reader overlay converts method-family and external-literature tables into narrative prose while keeping the canonical AI/research comparison tables in the live source.
- The Artifact Steward Agents reader overlay converts autonomy, treasury, and project-object tables into narrative prose while keeping the canonical AI/research matrices in the live source.
- The Semantic Representation reader overlay converts lifecycle and consumer-policy tables into narrative prose while keeping the canonical AI/research mechanism and record vocabulary in the live source.
- The Command Contracts reader overlay converts validation-state and field-status tables into narrative prose while keeping the canonical AI/research state matrix and command-record vocabulary in the live source.
- The Planning reader overlay converts the plan-node lifecycle-state table into narrative prose while keeping the canonical AI/research state matrix and planning-control boundary in the live source.
- The Verification Bandwidth reader overlay converts the adequacy-state table into narrative prose while keeping the canonical AI/research adequacy-state matrix and context/claim verification boundary in the live source.
- The Runtime Adapters reader overlay converts the effect-receipt field table into narrative prose while keeping the canonical AI/research receipt-field matrix and effect-boundary vocabulary in the live source.
- The Fast Generation reader overlay converts metric-code and taxonomy-table material into narrative prose while keeping the canonical AI/research formulas and generation-mode matrix in the live source.
- The RankFold/NeuralFold reader overlay converts the artifact-compression admission-state table into narrative prose while keeping the canonical AI/research state taxonomy and probe/fallback boundary in the live source.
- The Labor OS reader overlay converts the typed-job lifecycle-state table into narrative prose while keeping the canonical AI/research lifecycle matrix in the live source.
- The Circle Contracts reader overlay converts the proof-receipt lifecycle table into narrative prose while keeping the canonical AI/research receipt-state matrix in the live source.
- Human Reading Path bridges survive as ordinary prose, and reader-spine validation confirms all 54 chapters preserve Handoff continuity.
- Raw core-claim markers and repeated support boilerplate are stripped or humanized while the evidence boundary remains visible in the Core Claim prose.
- Source crosswalks, Codex test plans, drafting guardrails, and most live/research scaffolding are removed from the reader source.
- The reader delta workflow is in the correct shape: tracked overlays are the editable reader-delta source; generated reader files and generated delta reports are disposable review output.

## Automated Continuity Audit

The current generated reader source now has a deterministic heuristic audit at `docs/reader_continuity_audit.md`, generated by:

```bash
python3 scripts/audit_reader_continuity.py --write
```

The audit currently measures 54 reader chapters, 59 generated files, 121,729 reader words, 25 active and applied reader-overlay operations, 21 table rows, 58 Mermaid diagrams, 0 non-Mermaid code blocks, 0 paragraphs at or above 160 words, and 0 repeated first-sentence stems under the current eight-word heuristic. It identifies 3 high-priority heuristic review chapters, mostly where generated reader chapters still carry table-heavy or dense technical material.

This is review triage, not manual review. It creates a queue for the chapter-by-chapter human pass and helps decide whether a finding should become a canonical prose edit, reader-only overlay, companion-note treatment, or no action.

## Residuals

- The generated manuscript has not received a full 54-chapter human continuity review. It is mechanically valid, not release-reviewed.
- The prose is still derived from the live AI/research book. It reads better than the live scaffold, but many chapters still carry technical interfaces, minimum-field lists, Mermaid diagrams, and implementation language that may need compression, rephrasing, or companion-note treatment for relaxed reading.
- Some reader chapters still contain useful but dense schema-like material. A final human edition should decide chapter by chapter whether to retain it, summarize it, move it to companion material, or leave it only in the live/research book.
- The original baseline had zero active overlay operations. That baseline has been superseded by the opening-chapter, Human Intent, System Boundaries, Evidence States, Personal Compute Hives, Command Contracts, Planning, Verification Bandwidth, Runtime Adapters, Labor OS, Circle Contracts, Fast Generation, RankFold/NeuralFold, Policy Optimization, Artifact Steward Agents, and Semantic Representation reader-overlay operations in `docs/reader_overlay_pilot.md`; broader reader-only prose pacing, example insertion, and section-flow edits remain open.
- No EPUB, PDF, DOCX, AZW3, MOBI, Markdown, plain-text, audio, or audio-embedded EPUB artifact has been rendered, reviewed, or released in this pass.
- No curated parallel reader manuscript exists yet. Graduation from generated source plus overlays remains a future decision once reader-only edits become too substantial for overlays.
- The automated continuity audit is current, but it does not replace the full 54-chapter human read.

## Next Review Pass

The next Phase 2 pass should:

1. Read the generated reader manuscript chapter by chapter for continuity, pacing, duplicated explanations, missing transitions, and e-reader readability.
2. Classify each finding as a canonical live-book edit, a reader-only overlay, companion-note treatment, or no action.
3. Add reader-only semantic deltas under `editions/reader_overlays/v1_0/` only when the live AI/research source should not change.
4. Keep evidence boundaries, support states, implementation horizons, and non-claims inherited from the live book.
5. Render reader HTML, EPUB, and DOCX only after the manuscript review is recorded. Attempt PDF only when local dependencies support it.
6. Generate audio-script review output only after the reader manuscript is reviewed.

## Non-Claims

- This baseline does not claim a reviewed reader release exists.
- This baseline does not claim any ebook, document, PDF, audio, or audio-embedded EPUB artifact exists.
- This baseline does not promote any claim support state.
- The live AI/research book remains canonical for claims, support states, source boundaries, proof/test status, implementation horizons, and release records.
