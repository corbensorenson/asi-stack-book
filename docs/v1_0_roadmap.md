# v1.0 Roadmap

Last updated: 2026-06-28

This roadmap is the execution surface for moving **The ASI Stack** from the current v1.0 candidate state toward a reviewed v1.0 evidence release and human-reader release path.

The live AI/research book remains the canonical architecture, evidence, source, proof, schema, and release-control source. The normal reader manuscript can eventually become a curated parallel derivative source for prose, pacing, chapter flow, and human-consumption packaging. It is parallel but not equal: it may diverge from the live/research text for readability, but it must inherit claim text, support states, source boundaries, proof/test status, implementation horizons, and release records from the live book unless a deliberate reconciliation step updates both surfaces.

Use this file as the goal target for long-running improvement work. Use `book_structure.json` for ordering, `docs/book_outline.md` for drafting/proof/source scope, and `docs/v1_0_focus_audit.md` for the current-state audit.

## Inputs Reconciled

This roadmap reconciles:

- the current repository state after commit `67911895`;
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
| Local repo cleanup via `git gc` | Local hygiene only | Optional local maintenance; do not treat as book quality work. |

## What Is Already Resolved Or Not Actionable

| Finding | Current status |
|---|---|
| Unfinished `"The result is"` pass | Resolved in current `main`; `validate_repeated_prose.py` now rejects the phrase and current chapters have 0 hits. |
| Source notes, external appendix split, Lean toolchain, CI gates, proof imports, generated appendices | Resolved before this roadmap; do not re-spend effort unless a validator fails or new source/proof work changes the surface. |
| `validate_proof_artifact_audit.py` and `validate_source_evidence_audit.py` silently writing files | Not reproduced. Both default to check mode and write only with `--write`; CI runs them in check mode. |
| Stale deployed appendix set | Not a current blocker. Current Pages runs are checked before commits, and local render validates the A-K appendix surface. |
| `validate_live_human_view.py` needing a fresh `_site` | Real but minor. CI orders render before this check. A clearer local error message is optional Phase 7 hygiene. |

## Phase 0 - Operating Discipline

Status: active and ongoing.

Purpose: keep the repo honest while work continues.

Tasks:

- Check the prior GitHub Pages run before each new commit.
- Keep raw/private source exports out of the public repo.
- Keep all 54 core claims at `argument` unless an accepted evidence transition justifies a narrower promotion.
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

Status: started. The generated reader baseline was produced and recorded in `docs/reader_manuscript_review.md`; full 54-chapter human continuity review, reader overlays, rendered reader artifacts, and release records remain open.

Purpose: turn the mechanically valid Human view and generated reader source into a reviewed human-reader manuscript path.

Tasks:

1. Generate the reader edition with `python3 scripts/build_reader_edition.py`. Baseline generated on 2026-06-28: 54 chapters, 59 files, 275 live-only sections removed, 54 human-only bridges unwrapped, 54 raw core-claim markers removed, 50 support-boilerplate passages humanized, 60 reader scaffold terms humanized, and 0 active reader-overlay operations applied.
2. Review `build/reader_edition/READER_RELEASE_CHECKLIST.md`, `companion_notes.md`, and `reader_delta_report.md`. Initial review recorded in `docs/reader_manuscript_review.md`.
3. Read the generated reader manuscript for continuity, pacing, duplicated live-book scaffolding, missing transitions, and caveats that became too thin after stripping.
4. Apply human-reader-only deltas through `editions/reader_overlays/` only when the change should not alter AI/research view.
5. Apply canonical prose edits when the improvement belongs in all views.
6. Render reader HTML, EPUB, and DOCX when ready; attempt PDF only when local dependencies support it.
7. Record actual render outcomes without claiming publication until review and release records exist.

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

Status: initial pilot complete. Four no-change evidence-transition records were added under `evidence_transitions/v1_0_pilot/`, summarized in `docs/evidence_transition_pilot.md`, and validated by `scripts/validate_evidence_transitions.py`. All four reviewed claims remain at `argument`.

Purpose: prove that the claim/evidence system can move claims conservatively, or explicitly decide not to move them.

Initial candidates:

- `evidence-states-and-claim-discipline`
- `living-book-methodology`
- `executable-specifications-and-lean-proof-envelope`
- generated source appendix ownership and implementation-horizon mechanics, scoped as book-method claims only

Tasks:

1. Pick 3-5 narrow claims. Initial pilot selected `evidence-states-and-claim-discipline.core`, `living-book-methodology.core`, `executable-specifications-and-lean-proof-envelope.core`, and `open-research-agenda-and-bibliography-plan.core`.
2. Review exact source passages, repository artifacts, commands, and limitations. Initial pilot reviewed repository artifacts, validators, proof audit, source appendix mechanics, and known limitations; it did not claim independent source-interpretation review.
3. Create or update evidence transition records. Initial pilot added four JSON records under `evidence_transitions/v1_0_pilot/`.
4. Record non-promotion decisions where evidence remains insufficient. Initial pilot records all four as no-change decisions that remain at `argument`.
5. Update Appendix C only after a transition is accepted. No Appendix C support-state update was made because no upward transition was accepted.

Acceptance criteria:

- No broad AI, safety, capability, or deployment claim is promoted.
- Every proposed movement has a recorded basis and limitation.
- Negative or insufficient findings are preserved.

## Phase 4 - Proof Adequacy Review

Status: planned.

Purpose: distinguish "Lean build passes" from "this is the right formalization."

Tasks:

1. Review all 112 Lean proof targets.
2. Classify each target as adequate finite-record invariant, useful-but-too-narrow, needs richer state-machine semantics, needs executable tests first, or should remain research agenda.
3. Update `proofs/proof_triage.json`, `docs/proof_artifact_audit.md`, chapters, and Appendix E only where the review justifies it.
4. Add or revise Lean code only where a stronger operational predicate is clear.

Acceptance criteria:

- A public-safe proof adequacy review exists.
- `cd lean && lake build` passes.
- Proof text and chapter limitation prose still do not overclaim.

## Phase 5 - First Real Test Harnesses

Status: planned.

Purpose: move beyond schema shape validation into executable behavior checks.

Start with small deterministic tests that help many chapters:

| Harness | Primary chapters |
|---|---|
| Support-state transition checker | Evidence states; claim ledgers; benchmark ratchets; living-book methodology |
| Authority non-escalation and permission receipts | System boundaries; security kernel; runtime adapters; labor OS |
| Plan graph and execution-contract tests | Intent contracts; command contracts; planning; PlanForge; cognitive compilation |
| Context admission versus adequacy tests | Virtual Context ABI; semantic pages; context transactions; verification bandwidth |
| Readiness gate and residual escrow tests | Routing; readiness gates; MoECOT; prototype roadmap; recursive self-improvement |
| Benchmark ratchet anti-Goodhart tests | Benchmark ratchets; policy optimization; artifact steward agents |

Acceptance criteria:

- Tests have commands, fixtures, environment notes, result records, and non-claims.
- Failed or inconclusive tests remain visible.
- Appendix E and relevant chapters distinguish fixture validation from behavior validation.

## Phase 6 - External Literature Backfill

Status: planned.

Purpose: ground the architecture against third-party literature where outside readers will expect comparison.

Priority queues:

1. Alignment, corrigibility, power-seeking, and control.
2. AI governance, evaluations, deployment policy, incident response, and model evals.
3. Planning, task decomposition, HTN, behavior trees, GOAP, TAMP, and agent orchestration.
4. RAG, memory systems, context engineering, long-context evaluation, and context compilation.
5. Formal methods, proof assistants, proof-carrying code, runtime assurance, and contract verification.
6. Mixture-of-experts, routing, modular agents, and model/system routing.
7. Compression, representation learning, program synthesis, and residual/error accounting.
8. Benchmark science, contamination, saturation, hidden tests, and eval gaming.

Acceptance criteria:

- No source is cited from memory.
- Each used source has a source record, source note, chapter assignment, and support boundary.
- External literature remains separate from Corben/local sources in Appendix H.

## Phase 7 - Visual, Site, And Local-Hygiene Review

Status: planned.

Purpose: improve trust and usability after the manuscript voice and evidence path are stronger.

Tasks:

- Manual diagram audit for overloaded or low-legibility Mermaid diagrams.
- Mobile and desktop Human-view inspection.
- Landing page status and trust review.
- Table overflow check for appendices.
- Optional clearer `validate_live_human_view.py` error when `_site` is missing or stale.
- Optional local `git gc` if loose-object warnings recur.

Acceptance criteria:

- Visual changes do not imply unrecorded proof, benchmark, or runtime behavior.
- Browser validation passes after render.
- Public-site status remains honest about candidate versus evidence release.

## Phase 8 - Major Version Reader And Audio Packaging

Status: future, blocked on reviewed reader manuscript.

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
