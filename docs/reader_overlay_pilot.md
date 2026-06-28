# Reader Overlay Log

Last updated: 2026-06-28

This note records the active v1.0 semantic reader-overlay work. It is a reader-prose control record, not a reader release record.

## Scope

The initial pilot added two active operations under `editions/reader_overlays/v1_0/chapters/asi-is-a-stack-not-a-model.json`:

- `v1_0.asi_stack_not_model.problem_reader_replace` replaces the generated-reader and live Human-view `Problem` section for `chapters/asi-is-a-stack-not-a-model.qmd`.
- `v1_0.asi_stack_not_model.summary_reader_replace` replaces the generated-reader and live Human-view `Summary` section for the same chapter.

The next reader-continuity pass added four active operations under `editions/reader_overlays/v1_0/chapters/personal-compute-hives-and-federated-edge-intelligence.json`:

- `v1_0.personal_compute_hives.owned_substrate_reader_replace` replaces the generated-reader and live Human-view `Owned substrate and device roles` section.
- `v1_0.personal_compute_hives.hive_objects_reader_replace` replaces the generated-reader and live Human-view `Hive objects` section.
- `v1_0.personal_compute_hives.job_classes_reader_replace` replaces the generated-reader and live Human-view `Job classes and federation modes` section.
- `v1_0.personal_compute_hives.hive_memory_reader_replace` replaces the generated-reader and live Human-view `Hive memory` section.

The following reader-continuity pass added two active operations under `editions/reader_overlays/v1_0/chapters/policy-optimization-and-learning-from-feedback.json`:

- `v1_0.policy_optimization.method_families_reader_replace` replaces the generated-reader and live Human-view `Method families` section.
- `v1_0.policy_optimization.external_literature_reader_replace` replaces the generated-reader `source-reviewed external literature` section and uses `Source-noted external literature` as a live-source heading alias for Human view.

The next reader-continuity pass added two active operations under `editions/reader_overlays/v1_0/chapters/artifact-steward-agents-and-living-project-governance.json`:

- `v1_0.artifact_stewards.autonomy_treasury_reader_replace` replaces the generated-reader and live Human-view `Autonomy and treasury modes` section.
- `v1_0.artifact_stewards.project_objects_reader_replace` replaces the generated-reader and live Human-view `Project objects` section.

The following reader-continuity pass added two active operations under `editions/reader_overlays/v1_0/chapters/semantic-representation-and-tree-structured-models.json`:

- `v1_0.semantic_representation.mechanism_lifecycle_reader_replace` replaces the generated-reader and live Human-view `Semantic node lifecycle` subsection while preserving the mechanism diagram.
- `v1_0.semantic_representation.interfaces_reader_replace` replaces the generated-reader and live Human-view `Interfaces` section.

The next reader-continuity pass added two active operations under `editions/reader_overlays/v1_0/chapters/command-contracts-and-semantic-interfaces.json`:

- `v1_0.command_contracts.validation_states_reader_replace` replaces the generated-reader and live Human-view `Command contract validation states` subsection while preserving the mechanism diagram.
- `v1_0.command_contracts.interfaces_reader_replace` replaces the generated-reader and live Human-view `Interfaces` section.

The following reader-continuity pass added two active operations under `editions/reader_overlays/v1_0/chapters/fast-generation-architectures.json`:

- `v1_0.fast_generation.insufficiency_reader_replace` replaces the generated-reader and live Human-view `Why existing approaches are insufficient` section.
- `v1_0.fast_generation.taxonomy_reader_replace` replaces the generated-reader and live Human-view `Generation-mode taxonomy` section.

The next reader-continuity pass added one active operation under `editions/reader_overlays/v1_0/chapters/labor-os-and-typed-jobs.json`:

- `v1_0.labor_os.lifecycle_states_reader_replace` replaces the generated-reader and live Human-view `Typed job lifecycle states` subsection while preserving the mechanism diagram.

The following reader-continuity pass added one active operation under `editions/reader_overlays/v1_0/chapters/circle-calculus-and-proof-carrying-ai-contracts.json`:

- `v1_0.circle_contracts.receipt_lifecycle_reader_replace` replaces the generated-reader and live Human-view `Proof receipt lifecycle` subsection while preserving the mechanism diagram.

The canonical chapter source remains unchanged. AI view keeps the original live/research prose, source mappings, claim labels, support state, proof hooks, test-plan surface, and source crosswalk. Human view and generated reader editions receive the reader-only section prose through the same tracked overlay payload.

## Why These Overlays Exist

The v1.0 roadmap allows the normal reader edition to diverge from the AI/research source for pacing, prose flow, and relaxed reading, while keeping the live book canonical for claims, support states, source boundaries, proof/test status, implementation horizons, and release records. These overlays exercise that path on the opening chapter and on the first table-heavy reader-continuity target before scaling chapter-by-chapter reader editing.

The opening chapter is a good pilot because it has high reader-framing value and low claim risk. The overlay does not change the core claim. It rewrites the first problem statement and closing summary into calmer book prose so the Human view can begin as a readable book while the AI/research view remains a full architecture workbench.

The Personal Compute Hives overlays convert four dense generated-reader tables into narrative prose while preserving the canonical AI/research tables in the live source. They reduce the generated reader manuscript's table load without claiming that the hive scheduler, federation protocol, approval path, or memory topology has been implemented.

The Policy Optimization overlays convert method-family, target-policy, training-mode, and external-literature tables into narrative prose while preserving the canonical AI/research tables in the live source. They reduce the generated reader manuscript's table load without claiming that any PPO, DPO, GRPO, RLVR, router-policy, context-policy, verifier-policy, execution-policy, or reasoning-budget training run has been performed.

The Artifact Steward Agents overlays convert autonomy, treasury, and project-object tables into narrative prose while preserving the canonical AI/research matrices in the live source. They reduce the generated reader manuscript's table load without claiming that a steward bot, treasury engine, event-taint workflow, governance runner, release runner, or project federation harness exists.

The Semantic Representation overlays convert the semantic-node lifecycle and consumer-policy tables into narrative prose while preserving the canonical AI/research mechanism, record vocabulary, and Mermaid gate. They reduce the generated reader manuscript's table load without claiming a TreeLLM implementation, semantic graph implementation, grounding benchmark, hierarchy-revision result, representation-utility result, consumer-policy harness, or support-state promotion.

The Command Contracts overlays convert command validation-state and field-status tables into narrative prose while preserving the canonical AI/research command contract vocabulary, state matrix, and interface fields. They reduce the generated reader manuscript's table load without claiming a parser, prompt-injection defense, dispatcher, command-system implementation, override-test result, field-confidence audit, authority-inference block result, or support-state promotion.

The Fast Generation overlays convert the metric code block and generation-mode taxonomy table into narrative prose while preserving the canonical AI/research formulas, comparison matrix, and mode vocabulary. They reduce generated reader code/table load without claiming an autoregressive baseline, speculative decoding run, multi-token prediction result, diffusion result, early-exit result, state-space result, KV-cache benchmark, hybrid-generation result, speed-quality benchmark, or support-state promotion.

The Labor OS overlay converts the typed-job lifecycle-state table into narrative prose while preserving the canonical AI/research state matrix, lifecycle vocabulary, and execution boundary. It reduces the generated reader manuscript's table load without claiming a scheduler, permission service, approval service, adapter runner, completion-receipt implementation, replay system, lifecycle harness result, or support-state promotion.

The Circle Contracts overlay converts the proof-receipt lifecycle table into narrative prose while preserving the canonical AI/research receipt-state matrix and proof/consumer authority boundary. It reduces the generated reader manuscript's table load without claiming Circle theorem replay, theorem-id resolution, receipt replay, fingerprint validation, generated contract packs, downstream model-quality evidence, or support-state promotion.

## Review Contract

Reviewers should compare the generated `build/reader_edition/reader_delta_report.md` against the tracked operation file. The delta report should show both operation digests and before/after excerpts after `python3 scripts/build_reader_edition.py` runs.

For live-site review, `assets/reader-overlays.html` should be regenerated from the overlay source with `python3 scripts/sync_reader_overlay_asset.py`, and browser validation should confirm the embedded operation count is processed in Human view.

## Local Validation

Current local results for this overlay set:

- `python3 scripts/sync_reader_overlay_asset.py` regenerated `assets/reader-overlays.html` with 18 active operations.
- `python3 scripts/build_reader_edition.py` regenerated `build/reader_edition/`; `reader_delta_report.md` records 18 active and 18 applied operations.
- `python3 scripts/sync_reader_overlay_asset.py --check` passed with 18 active operations.
- `python3 scripts/validate_reader_overlays.py --check` passed with 18 active operations and 18 applied operations.
- `python3 scripts/build_reader_edition.py --check` passed for 54 chapters, 59 files, 275 stripped live-only sections, 60 humanized reader-scaffold terms, and 18 reader overlay operations applied.
- `python3 scripts/validate_reader_spine.py --check` passed for 54 chapters, with minimum reader-spine length 1,957 words.
- `python3 scripts/validate_reader_evidence_boundaries.py --check` passed for 54 chapters.
- `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html` completed and wrote `_site/index.html`.
- `python3 scripts/validate_live_human_view.py` passed for 67 rendered book pages and 54 rendered chapter pages.
- `node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports` passed for 112 rendered page-view pairs.

## Non-Claims

- This pilot is not a reviewed reader manuscript.
- This pilot is not an EPUB, DOCX, PDF, audiobook, audio-embedded EPUB, or edition release.
- This pilot does not introduce new source-derived claims.
- This pilot does not promote any support state.
- This pilot does not claim proof adequacy, benchmark behavior, runtime behavior, or implementation completion.

## Remaining Work

- Review the generated reader delta report after each overlay edit.
- Expand reader-only overlays only where the live AI/research source should remain unchanged.
- Make canonical chapter edits when reader review reveals a problem that also affects AI/research readers.
- Graduate to a curated parallel reader manuscript only when overlays become too large or too numerous to remain a clean semantic delta layer.
