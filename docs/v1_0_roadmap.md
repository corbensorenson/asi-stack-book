# v1.0 Roadmap

Last updated: 2026-06-28

This roadmap is the execution surface for moving **The ASI Stack** from the current v1.0 candidate state toward a reviewed v1.0 evidence release and human-reader release path.

The live AI/research book remains the canonical architecture, evidence, source, proof, schema, and release-control source. The normal reader manuscript can eventually become a curated parallel derivative source for prose, pacing, chapter flow, and human-consumption packaging. It is parallel but not equal: it may diverge from the live/research text for readability, but it must inherit claim text, support states, source boundaries, proof/test status, implementation horizons, and release records from the live book unless a deliberate reconciliation step updates both surfaces.

Use this file as the goal target for long-running improvement work. Use `book_structure.json` for ordering, `docs/book_outline.md` for drafting/proof/source scope, and `docs/v1_0_focus_audit.md` for the current-state audit.

## Inputs Reconciled

This roadmap reconciles:

- the current repository state during the 2026-06-28 extended v1.0 improvement run;
- `docs/v1_0_focus_audit.md`;
- the external Claude review supplied by Corben as planning input;
- local verification of Claude's concrete claims against the current tree.

Claude's review is useful as an editorial and hygiene review, not as source evidence. It should not be quoted as an external authority in the book.

## What Had Teeth

| Finding | Current verification | Roadmap treatment |
|---|---:|---|
| Mechanical `Operating mechanism:` recap lists in `Beyond the State of the Art` sections | 0 after Phase 1 pass; 26 before pass | Phase 1 rewrote these into mature-product prose and added a guard so the pattern cannot return. |
| Repeated `remains a target architecture, not a current-result claim` disclaimer | 0 after Phase 1 pass; 42 before pass | Phase 1 preserved the non-claim boundary with chapter-specific language. |
| Repeated `keeps ... honest` construction | 0 after Phase 1 pass; 9 before pass by regex | Phase 1 replaced the reusable cadence with mechanism-specific prose and added a guard. |
| Reader/ebook should not inherit all live-book uniformity | Structurally true by design | Phase 2. Review generated reader edition, then graduate toward a curated parallel reader manuscript when prose divergence becomes too large for overlays. |
| Manifest claim/support defaults should not hide source-of-truth state | Resolved for the current chapter set: all 54 chapter records now declare explicit `claim_label` and `evidence_level` fields, and `schemas/book_structure.schema.json` records the whole-file manifest shape | Phase 0 guardrail. `scripts/add_chapter.py` creates explicit fields for new chapters, and `scripts/validate_book.py` validates `book_structure.json` against the schema before semantic source/proof checks. |
| Local repo cleanup via `git gc` | Local hygiene only | Optional local maintenance; do not treat as book quality work. |

## What Is Already Resolved Or Not Actionable

| Finding | Current status |
|---|---|
| Unfinished `"The result is"` pass | Resolved in current `main`; `validate_repeated_prose.py` now rejects the phrase and current chapters have 0 hits. |
| Source notes, external appendix split, Lean toolchain, CI gates, proof imports, generated appendices | Resolved before this roadmap; do not re-spend effort unless a validator fails or new source/proof work changes the surface. |
| `validate_proof_artifact_audit.py` and `validate_source_evidence_audit.py` silently writing files | Not reproduced. Both default to check mode and write only with `--write`; CI runs them in check mode. |
| Stale deployed appendix set | Not a current blocker. Current Pages runs are checked before commits, and local render validates the A-K appendix surface. |
| `validate_live_human_view.py` needing a fresh `_site` | Resolved as local hygiene. CI orders render before this check, and the validator now preflights missing, incomplete, or stale `_site` output with a render-first diagnostic. |

## Phase 0 - Operating Discipline

Status: active and ongoing.

Purpose: keep the repo honest while work continues.

Tasks:

- Check the prior GitHub Pages run before each new commit.
- Keep raw/private source exports out of the public repo.
- Keep all 54 core claims at `argument` unless an accepted evidence transition justifies a narrower promotion.
- Keep every manifest chapter record explicit about `claim_label` and `evidence_level`; missing or invalid values fail the book validator.
- Do not report reader, ebook, document, PDF, or audio artifacts unless that exact artifact was generated, reviewed where required, and recorded.
- Keep `book_structure.json` and `docs/book_outline.md` as source-of-truth surfaces.
- Update `appendices/F_changelog.qmd` for meaningful roadmap, source, claim, proof, reader, release, or validation changes.

Exit criteria:

- Working tree clean before starting a major pass.
- Prior Pages run checked.
- No generated scaffold drift after `python3 scripts/sync_scaffold.py`.

## Phase 1 - Reader-Visible Voice And De-Templating

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

## Phase 2 - Reviewed Reader Manuscript Path

Status: started. The generated reader baseline was produced and recorded in
`docs/reader_manuscript_review.md`; the active semantic reader-overlay log is
recorded in `docs/reader_overlay_pilot.md` with 33 active operations for Human
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
`docs/reader_chapter_review_matrix.md` with 54 `reviewed` chapters, 0
`spot_checked` chapters, 0 `not_started` chapters, 20 chapters carrying active
reader overlays, 54 no-immediate-action decisions, 3 companion-note candidates,
and 1 curated-manuscript candidate. `docs/reader_format_dry_run.md` records a
local HTML/EPUB/DOCX render dry run, basic structural artifact inspection, and
UTF-8 PDF probe with ignored snapshots; and
`docs/reader_artifact_layout_review.md` records representative PDF sampling and
a broader 28 page-view HTML layout/navigation probe. The tracked format-review
ledger is recorded in
`editions/reader_manuscript/v1_0/format_review_matrix.json` and summarized in
`docs/reader_format_review_matrix.md`; it keeps HTML, EPUB, DOCX, and PDF
unapproved until full format review and an edition release record exist, with
EPUB and DOCX also blocked on application/e-reader inspection. The full generated-reader chapter-text review queue
is complete for the current 54 chapters. `docs/reader_companion_note_routing_review.md`
and `editions/reader_manuscript/v1_0/companion_note_routing.json` now record
chapter-level companion-note routing for the three proof/governance chapters
flagged by the review matrix, and generated reader/audio companion notes consume
that routing manifest. Broader EPUB/DOCX/PDF artifact inspection, curated
reader-manuscript graduation, audio review, and release records remain open.
The future curated-source path is now governed by
`editions/reader_manuscript/v1_0/curation_contract.json` and
`docs/curated_reader_source_contract.md`, which require curated chapter records
to name generated baselines, live-source refs, claim boundaries, implementation
horizons, curation scopes, meaning-preservation checks, release blockers, and
canonical-change requirements before any manually edited reader chapter can
become release input.

Purpose: turn the mechanically valid Human view and generated reader source into a reviewed human-reader manuscript path.

Tasks:

1. Generate the reader edition with `python3 scripts/build_reader_edition.py`. The initial baseline generated on 2026-06-28 had 54 chapters, 59 files, 275 live-only sections removed, 54 human-only bridges unwrapped, 54 raw core-claim markers removed, 50 support-boilerplate passages humanized, 60 reader scaffold terms humanized, and no active reader overlays. The current generated check applies 33 active reader-overlay operations.
2. Review `build/reader_edition/READER_RELEASE_CHECKLIST.md`, `companion_notes.md`, and `reader_delta_report.md`. Initial review recorded in `docs/reader_manuscript_review.md`.
3. Read the generated reader manuscript for continuity, pacing, duplicated live-book scaffolding, missing transitions, and caveats that became too thin after stripping.
4. Apply human-reader-only deltas through `editions/reader_overlays/` only when the change should not alter AI/research view.
5. Apply canonical prose edits when the improvement belongs in all views.
6. Render reader HTML, EPUB, and DOCX when ready; attempt PDF only when local dependencies support it.
7. Record actual render outcomes without claiming publication until review and release records exist. The first local dry run rendered HTML, EPUB, and DOCX, snapshotted them under ignored `build/reader_edition/format_artifacts/`, and passed basic structural inspection. The isolated PDF probe failed without explicit locale settings but rendered when `LANG` and `LC_ALL` were set to `en_US.UTF-8`. Representative PDF sampling and a broader HTML layout/navigation probe exist, but no EPUB e-reader inspection, DOCX application inspection, full manual PDF layout review, or release record exists.

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
- `editions/reader_overlays/v1_0/chapters/semantic-representation-and-tree-structured-models.json` carries two active reader-only section replacements that convert the `Mechanism` lifecycle material and `Interfaces` consumer-policy table into narrative prose while preserving the mechanism diagram.
- The overlay set exercises the intended divergence path: Human view and generated reader editions receive calmer book prose, while AI view and canonical chapter source keep the original live/research scaffold, tables, and evidence surfaces.
- The overlay set is not a reviewed reader release, ebook artifact, audio artifact, support-state promotion, source-derived evidence update, proof result, benchmark result, or runtime result.

Automated continuity audit:

- `python3 scripts/audit_reader_continuity.py --write` generated `docs/reader_continuity_audit.md` from a temporary reader-edition workspace.
- The audit measures 54 reader chapters, 121,727 reader words, 33 active/applied reader-overlay operations, 0 table rows, 58 Mermaid diagrams, 0 non-Mermaid code blocks, 0 paragraphs at or above 160 words, and 0 repeated first-sentence stems under the current heuristic.
- It identifies 0 high-priority and 3 medium-priority heuristic review chapters. The remaining rows are a triage queue for manual reader review, not defects and not evidence of release readiness.
- The audit is not a reviewed reader release, ebook artifact, audio artifact, support-state promotion, source-derived evidence update, proof result, benchmark result, runtime result, or substitute for reading the manuscript.
- `docs/reader_continuity_review.md` records the first manual decisions for the three medium-priority rows. The two proof-heavy chapters are no-action for now with companion-note/glossary candidates, and the long Artifact Steward chapter is retained with future curated-reader compression as a possible release-editing task.

Chapter review matrix:

- `python3 scripts/sync_reader_chapter_review_matrix.py --write` generated `editions/reader_manuscript/v1_0/chapter_review_matrix.json` and `docs/reader_chapter_review_matrix.md` from the manifest order plus current reader-overlay counts.
- The matrix currently records 54 chapter rows: 54 `reviewed` rows from the full generated-reader chapter-text review passes, 0 `spot_checked` rows, 0 `not_started` rows, 20 chapters with active reader overlays, 54 no-immediate-action decisions, 3 companion-note candidates, and 1 curated-manuscript candidate.
- All rows retain reader-release and format-artifact blockers. The full chapter-text review blocker is cleared for every current chapter, but the matrix is still a review queue, not a reviewed reader release.
- The matrix keeps the future curated reader manuscript path dynamic: chapter IDs, part order, live files, generated-reader file paths, and overlay counts sync from `book_structure.json` and overlay files, while review status and disposition remain explicit reader-review decisions.
- `editions/reader_manuscript/v1_0/reconciliation_report.md` now provides the dormant reconciliation template for future curated reader chapters, including generated-reader baselines, live-source refs, divergence summaries, blocked evidence divergence, and release blockers.
- `editions/reader_manuscript/v1_0/curation_contract.json` now provides the dormant curated-source contract for future reader chapters, including required record fields, allowed prose divergence, blocked evidence divergence, meaning-preservation checks, pre-release blockers, and validation commands.
- `docs/curated_reader_graduation_review.md` records the current graduation decision: do not create curated reader source for v1.0 yet; keep generated reader source plus overlays, with Artifact Steward Agents retained as the first curated-manuscript candidate.

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

## Phase 3 - Evidence Transition Pilot

Status: initial pilot complete and extended. Ten no-change evidence-transition records are recorded under `evidence_transitions/v1_0_pilot/`, summarized in `docs/evidence_transition_pilot.md`, and validated by `scripts/validate_evidence_transitions.py`. All ten reviewed claims remain at `argument`.

Purpose: prove that the claim/evidence system can move claims conservatively, or explicitly decide not to move them.

Initial candidates:

- `evidence-states-and-claim-discipline`
- `living-book-methodology`
- `executable-specifications-and-lean-proof-envelope`
- generated source appendix ownership and implementation-horizon mechanics, scoped as book-method claims only

Tasks:

1. Pick narrow claims. Initial pilot selected `evidence-states-and-claim-discipline.core`, `living-book-methodology.core`, `executable-specifications-and-lean-proof-envelope.core`, and `open-research-agenda-and-bibliography-plan.core`; later extensions added `system-boundaries-and-authority.core` after the Authority proof follow-through, `planning-as-a-control-layer.core` after the Planning proof follow-through, `virtual-context-abi.core` after the context admission/adequacy harness, `benchmark-ratchets-and-anti-goodhart-evidence.core` after the benchmark anti-Goodhart harness, `runtime-adapters-tool-permissions-and-human-approval.core` after the runtime-adapter permission harness, and `readiness-gates-residual-escrow-and-quarantine.core` after the readiness/residual gate harness.
2. Review exact source passages, repository artifacts, commands, and limitations. Initial pilot reviewed repository artifacts, validators, proof audit, source appendix mechanics, and known limitations; it did not claim independent source-interpretation review.
3. Create or update evidence transition records. The pilot now has ten JSON records under `evidence_transitions/v1_0_pilot/`.
4. Record non-promotion decisions where evidence remains insufficient. The pilot records all ten as no-change decisions that remain at `argument`.
5. Update Appendix C only after a transition is accepted. No Appendix C support-state update was made because no upward transition was accepted.

Acceptance criteria:

- No broad AI, safety, capability, or deployment claim is promoted.
- Every proposed movement has a recorded basis and limitation.
- Negative or insufficient findings are preserved.

## Phase 4 - Proof Adequacy Review

Status: initial review complete, with four follow-through increments recorded. `docs/proof_adequacy_review.md` classifies all 112 Lean targets while preserving support-state boundaries; `AsiStackProofs.Authority` now includes a record-aware allow/deny/escalate authority decision envelope, `AsiStackProofs.Planning` now includes a plan-control record envelope for modeled dispatchable, blocked, and replanned records, `AsiStackProofs.ClaimLedger` and `AsiStackProofs.ProofCarryingClaims` now include finite ledger/proof-carrying record envelopes, and Runtime Adapters now has a synthetic permission/approval/receipt harness. System Boundaries, Planning, Claim Ledgers, Spinoza, and Runtime Adapters remain `useful but too narrow` because deployed enforcement, runtime traces, planner quality, claim extraction, contradiction detection, verifier quality, sandbox behavior, approval-service behavior, and richer integration behavior remain unproven.

Purpose: distinguish "Lean build passes" from "this is the right formalization."

Tasks:

1. Review all 112 Lean proof targets. Initial review completed in `docs/proof_adequacy_review.md`.
2. Classify each target as adequate finite-record invariant, useful-but-too-narrow, needs richer state-machine semantics, needs executable tests first, or should remain research agenda. Current target counts after the Runtime Adapter harness follow-through are 8 adequate finite-record, 28 useful-but-too-narrow, 20 richer-semantics-needed, 40 executable-tests-needed, 10 empirical/baseline-tests-needed, and 6 research-agenda-until-artifact-import.
3. Update `proofs/proof_triage.json`, `docs/proof_artifact_audit.md`, chapters, and Appendix E only where the review justifies it. The follow-through increments updated Lean code, the proof audit, chapter limitation prose, roadmap/status surfaces, and no-change evidence records without changing proof tags or support states.
4. Add or revise Lean code only where a stronger operational predicate is clear. The current Lean follow-through increments are `AsiStackProofs.Authority` and `AsiStackProofs.Planning`; both remain finite-record envelopes. Runtime Adapters changed through a synthetic harness, not a new Lean predicate.

Acceptance criteria:

- A public-safe proof adequacy review exists.
- `cd lean && lake build` passes.
- Proof text and chapter limitation prose still do not overclaim.

## Phase 5 - First Real Test Harnesses

Status: initial harness set complete and extended. Eight synthetic or deterministic harnesses are implemented: the support-state transition harness in `scripts/validate_support_state_transitions.py`, documented in `docs/support_state_transition_harness.md`; the authority transition harness in `scripts/validate_authority_transitions.py`, documented in `docs/authority_transition_harness.md`; the plan-execution contract harness in `scripts/validate_plan_execution_contracts.py`, documented in `docs/plan_execution_contract_harness.md`; the runtime adapter permission harness in `scripts/validate_runtime_adapter_permissions.py`, documented in `docs/runtime_adapter_permission_harness.md`; the context admission/adequacy harness in `scripts/validate_context_admission_adequacy.py`, documented in `docs/context_admission_adequacy_harness.md`; the readiness/residual gate harness in `scripts/validate_readiness_residual_gates.py`, documented in `docs/readiness_residual_harness.md`; the benchmark anti-Goodhart harness in `scripts/validate_benchmark_antigoodhart.py`, documented in `docs/benchmark_antigoodhart_harness.md`; and the generation mode baseline harness in `scripts/validate_generation_mode_baselines.py`, documented in `docs/generation_mode_baseline_harness.md`. All eight are backed by valid plus expected-invalid fixtures under `experiments/`, wired into `scripts/validate_book.py`, and registered in `experiments/phase5_harness_registry.json`; `python3 scripts/validate_phase5_harness_registry.py` checks their docs, commands, fixture counts, result records, Appendix E rows, public status references, primary chapter mappings, and non-claim boundaries. No live support state changed.

Purpose: move beyond schema shape validation into executable behavior checks.

Start with small deterministic tests that help many chapters:

| Harness | Primary chapters |
|---|---|
| Support-state transition checker | Evidence states; claim ledgers; benchmark ratchets; living-book methodology |
| Authority non-escalation and permission receipts | System boundaries; security kernel; runtime adapters; labor OS |
| Plan graph and execution-contract tests | Intent contracts; command contracts; planning; PlanForge; cognitive compilation |
| Runtime adapter permission and approval tests | Runtime adapters; security kernel; Labor OS; artifact graphs |
| Context admission versus adequacy tests | Virtual Context ABI; semantic pages; context transactions; verification bandwidth |
| Readiness gate and residual escrow tests | Routing; readiness gates; MoECOT; prototype roadmap; recursive self-improvement |
| Benchmark ratchet anti-Goodhart tests | Benchmark ratchets; policy optimization; artifact steward agents |
| Generation mode baseline accounting tests | Fast generation architectures; efficient ASI hypothesis; resource economics |

Acceptance criteria:

- Tests have commands, fixtures, environment notes, result records, and non-claims.
- Failed or inconclusive tests remain visible.
- Appendix E and relevant chapters distinguish fixture validation from behavior validation.
- The Phase 5 harness registry validates that the initial harness set stays wired across scripts, docs, fixtures, result records, Appendix E, and public status pages.

Initial completion:

- `python3 scripts/validate_support_state_transitions.py` passed locally on 2026-06-28 with 2 valid fixtures and 2 expected-invalid fixtures.
- The result record is `experiments/support_state_transitions/results/2026-06-28-local.md`.
- The harness is a gate-semantics test only. It does not promote Appendix C, validate source interpretation, prove proof adequacy, or exercise AI runtime behavior.
- `python3 scripts/validate_authority_transitions.py` passed locally on 2026-06-28 with 3 valid fixtures and 3 expected-invalid fixtures.
- The result record is `experiments/authority_transitions/results/2026-06-28-local.md`.
- The authority harness checks synthetic non-escalation, permission-separation, denial-receipt, approval-escalation, and confused-deputy shortcut behavior only. It does not prove deployed authorization enforcement, runtime adapter safety, secret handling, revocation propagation, or support-state promotion.
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
- `python3 scripts/validate_benchmark_antigoodhart.py` passed locally on 2026-06-28 with 2 valid fixtures and 5 expected-invalid fixtures.
- The result record is `experiments/benchmark_antigoodhart/results/2026-06-28-local.md`.
- The benchmark anti-Goodhart harness checks synthetic benchmark-ratchet, policy-optimization, and steward-action consistency only. It does not prove benchmark quality, hidden-holdout integrity, contamination detection, transfer performance, policy-training quality, reward-hacking resistance, steward-agent behavior, release safety, or support-state promotion.
- `python3 scripts/validate_generation_mode_baselines.py` passed locally on 2026-06-28 with 2 valid fixtures and 4 expected-invalid fixtures.
- The result record is `experiments/generation_mode_baselines/results/2026-06-28-local.md`.
- The generation mode baseline harness checks deterministic generation-mode and resource-budget fixture accounting for run, baseline, and negative-control refs, useful-solution-per-second plus quality and residual metrics, fallback behavior, resource-budget alignment, latency-only proxy rejection, and no-promotion boundaries only. It does not prove generation speed, speculative decoding quality, diffusion generation quality, KV-cache throughput, routing quality, useful-solution-per-second performance, model quality, runtime behavior, or support-state promotion.
- `python3 scripts/validate_phase5_harness_registry.py` records the eight-harness set in `experiments/phase5_harness_registry.json` and validates traceability across command scripts, fixture counts, public harness docs, result records, Appendix E, the v1.0 status/roadmap surfaces, primary chapter IDs, and `scripts/validate_book.py`.
- The registry is evidence plumbing only. It does not rerun the harnesses, prove runtime behavior, validate benchmark quality, or promote any support state.

Next Phase 5 evidence work should move from synthetic record gates toward replayable empirical slices or imported prototype traces where the source artifacts are available and public-safe.

## Phase 6 - External Literature Backfill

Status: started across all priority queues. Initial backfill passes added fifty-nine primary external source records and source notes across alignment/control, AI governance/evaluation, planning/agent control, retrieval/context, formal methods, routing/MoE, compression/representation, and benchmark science, summarized in `docs/external_literature_backfill_phase6.md`. The planning slice now includes ReAct, Tree of Thoughts, PDDL, SHOP2, Integrated TAMP, behavior trees, GOAP/F.E.A.R., and AutoGen as comparison vocabulary only. The retrieval/context slice now includes RAG, Lost in the Middle, MemGPT, LongBench, RULER, ALCE, Self-RAG, and LongLLMLingua as context-interface, citation-support, adaptive-retrieval, long-context-evaluation, and prompt-compression vocabulary only. The formal-methods slice now includes proof-carrying code, TLA+, Lean theorem proving, Dafny, Reluplex, Black-Box Simplex, Copilot, and PRISM as proof, specification, property-verification, runtime-assurance, monitor-generation, and probabilistic-model-checking vocabulary only. The routing/MoE slice now includes sparse MoE, GShard, Switch Transformers, Expert Choice Routing, Mixtral, an MoE-in-LLMs survey, FrugalGPT, Hybrid LLM, and RouteLLM as model-routing, task-routing, cost-quality routing, and learned-router vocabulary only. The compression slice now includes Deep Compression, LoRA, knowledge distillation, GPTQ, QLoRA, DreamCoder, Information Bottleneck, MDL, and CodeBLEU as compression, adaptation, program-synthesis, residual-accounting, and artifact-metric vocabulary only. The benchmark-science slice now includes MMLU, BIG-bench, HELM, GPQA, SWE-bench, LiveBench, Dynabench, CheckList, benchmark-contamination work, and Goodhart variants as benchmark-design, dynamic-evaluation, contamination, behavioral-testing, and anti-Goodhart vocabulary only. No claim support state, reproduction result, compliance claim, imported formal artifact, proof-assistant import, verifier run, planner run, motion-planning run, context benchmark run, citation-evaluation run, context-compression run, runtime-assurance case study, generated monitor, probabilistic model-checking run, route benchmark, router training, MoE training or inference run, compression experiment, program-synthesis run, information-bottleneck or MDL scorer implementation, CodeBLEU run, dynamic benchmark run, behavioral-test run, contamination audit, Goodhart taxonomy over local tests, finetuning run, benchmark run, or evidence transition changed.

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

## Phase 7 - Visual, Site, And Local-Hygiene Review

Status: started. The first rendered-site and visual audit is recorded in `docs/site_visual_phase7_review.md`; automated visual coverage, rendered Human-view validation, all-chapter/all-viewport browser validation, and a mobile screenshot review of the densest diagrams passed after Mermaid diagrams gained contained mobile scrolling. A second local browser probe after the Phase 6 source expansion checked the landing page, fast-generation and recursive-improvement chapters, and Appendices A/C/H at desktop and mobile sizes with zero page-level horizontal overflow and visible reading-mode toggles. A follow-up probe after the source inventory reached 160 records found Appendix F overflow from long inline `code` spans, added scoped inline-code wrapping in `assets/styles.scss`, and rechecked the landing page, dense chapters, and Appendices A/C/F/H/K with zero page-level horizontal overflow at desktop and mobile sizes. Optional splitting of the fast-generation and recursive-improvement diagrams remains open for reader-release review.

Purpose: improve trust and usability after the manuscript voice and evidence path are stronger.

Tasks:

- Manual diagram audit for overloaded or low-legibility Mermaid diagrams; first mobile screenshot pass is recorded for the densest diagrams.
- Mobile and desktop Human-view inspection.
- Landing page status and trust review.
- Continue table and inline-code overflow checks after large source, claim-matrix, or changelog growth; the current source-growth and inline-code probes found no page-level overflow on Appendices A/C/F/H/K.
- Maintain `schemas/book_structure.schema.json` alongside future manifest fields; the schema now validates the top-level book contract before the semantic validators check source IDs, proof targets, reader surfaces, and evidence boundaries.
- Keep the `validate_live_human_view.py` preflight current so missing, incomplete, or stale `_site` output fails with render-first guidance before page-level checks run.
- Optional local `git gc` if loose-object warnings recur.

Acceptance criteria:

- Visual changes do not imply unrecorded proof, benchmark, or runtime behavior.
- Browser validation passes after render.
- Public-site status remains honest about candidate versus evidence release.

## Phase 8 - Major Version Reader And Audio Packaging

Status: preparation reviewed; still future and blocked on reader release records and artifact review. `docs/v1_0_release_preparation_review.md` records passing release-profile, reader-spine, reader-boundary, reader-overlay, reader-edition-check, reader-format-check, reader-format dry-run, reader-artifact structural-inspection, UTF-8 PDF-probe, representative PDF sampling, broader HTML layout/navigation probing, and audio-script-check commands. `docs/reader_format_dry_run.md` records local HTML/EPUB/DOCX/PDF snapshots in ignored `build/` space, and `docs/reader_format_review_matrix.md` now records the format-level review blockers in a synced ledger, but no tag, reviewed reader release, full manual layout approval, audiobook, or edition release record was produced.

Purpose: produce human-consumption artifacts only after the live and reader surfaces are reviewed.

Tasks:

1. Tag a validated live-book candidate.
2. Generate and review reader source.
3. Render HTML, EPUB, DOCX, and PDF only where dependencies and review allow.
4. Record exact produced artifacts in an edition release record.
5. Generate audio script only after reader review.
6. Review spoken treatment for diagrams, tables, code, schemas, and proof-adjacent material.
7. Produce MP3, M4B, or audio-embedded EPUB only after audio generation, packaging checks, and release-record entry.

Acceptance criteria:

- No artifact is claimed from a target profile alone.
- Release records name what exists, what was reviewed, what failed, and what remains unattempted.

## Best Goal To Set Next

Recommended goal text:

```text
Run an extended roadmap-driven v1.0 completion pass on The ASI Stack using docs/v1_0_roadmap.md as the primary execution plan, docs/v1_0_focus_audit.md as the current-state audit, docs/book_outline.md as the drafting/proof/source source of truth, and book_structure.json as the manifest source of truth.

Start with Phase 1: remove the remaining reader-visible generator bleed-through by rewriting the 26 Beyond the State of the Art sections that contain Operating mechanism recaps, varying the repeated target-architecture non-claim boundary across the 42 affected chapters, smoothing remaining repeated honesty cadence, and then adding a guard so those patterns cannot return. Preserve every evidence boundary and do not promote support states.

After Phase 1 passes validation, proceed through the roadmap in order as far as the run can honestly get: reviewed reader manuscript path, reader-source divergence planning, evidence-transition pilot, proof adequacy review, first executable test harnesses, external literature backfill, visual/site review, and major-version release preparation. The normal reader version may eventually graduate from generated output plus overlays into a curated parallel derivative manuscript for human prose, but it must remain subordinate to the live AI/research book for claims, source boundaries, support states, proof/test status, implementation horizons, and release records. Do not fabricate sources, tests, proof results, benchmark results, reader artifacts, ebook artifacts, or audio artifacts. Record all completed work, skipped work, blockers, validations run, and residuals in the roadmap, changelog, and relevant appendices before reporting completion.
```

This goal is better than "write the whole book" now because the book is already structurally complete and long. The next leverage point is to make the existing book read less generated, then move from validated mechanics toward reviewed reader quality and accepted evidence.
