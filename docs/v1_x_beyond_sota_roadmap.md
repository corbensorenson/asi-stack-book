# v1.x Beyond-SOTA Roadmap

Last updated: 2026-07-01

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
Quarto site, and three narrow non-core evidence transitions. The current v1.x
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
- the original 54-chapter expansion may still be over-split in several
  thematic clusters,
  so repetition should be reduced through governed consolidation rather than
  prose polishing alone;
- Project Theseus and Circle evidence need public-safe replay paths rather than
  local-only summaries;
- the human-reader edition needs to become a true edited book, not only a strip
  of the AI/research source;
- EPUB, DOCX, PDF, and audio should be treated as reviewed edition artifacts
  only after exact artifact records exist.
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
  consolidation has produced many planning artifacts and no manifest merges;
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
| P0 | The 44-lane evidence plan can reintroduce the breadth trap. | The first roadmap version named a lane and acceptance bar for every chapter, which is useful as backlog but dangerous as an execution checklist. | Keep the 44-row plan in `docs/per_chapter_evidence_plan.md`, cap each v1.x cycle at 5-8 executed lanes, and leave the rest explicitly planned. |
| P0 | The project's strongest quality is the least legible one. | The validation, support-state discipline, and non-claim machinery are real, but a cold reader first sees broad scope, self-coined terms, and many self-sourced ideas. | Add a 60-second trust surface and make the evidence discipline visible before readers infer overreach. |
| P0 | Safety-critical Lean depth is improving but still shallow. | `docs/proof_depth_classification.md` now records 532 theorem declarations, 121 direct/projection-style, 411 derived/decomposed, and 69 safety-critical theorem declarations. Each of `Alignment`, `Corrigibility`, `GovernanceRights`, `SelfImprovement`, and `ValueConflict` has at least one derived/decomposed finite-record theorem plus explicit projection-only limitation prose; `Alignment` and `ValueConflict` now each have four derived/decomposed transition/control/preservation/review theorems, `Corrigibility` and `GovernanceRights` each have sixteen, and `SelfImprovement` now has nineteen derived/decomposed boundary, lifecycle, and transition-route theorems, while 10 safety-critical theorem declarations remain direct/projection-style. `ClaimLedger` now has a finite revision-lifecycle route envelope for missing claim identity, support-state gaps, unsupported promotion, open contradictions, history loss, surface-sync gaps, split/downgrade/residual gaps, and non-claim-boundary gaps. `EvidenceStates` now has a finite transition-lifecycle route envelope for no-change, missing record, scope, support-effect, review, evidence, negative-evidence, downgrade-trigger, terminal-effect, changelog, and non-claim-boundary gaps. `ReadinessGates` also has a separate lifecycle-boundary negative-case envelope for failed promotions, incomplete stronger transitions, quarantine-route misuse, and stale-gate reuse; `ProofEnvelope` has an artifact-authority negative-case envelope for proof-lane laundering and promotion-boundary misuse; `PolicyOptimization` has a promotion-route envelope for reward, evaluation, governance, rollback, and residual gaps; Planning has a finite dispatch-route theorem for valid modeled dispatchable records; Context Transactions has a finite materialization/deletion-closure route theorem pair; Stack Boundaries has a finite layer-contract admission lifecycle route for layer identity, lifecycle, authority, evidence, source-mapping, support-state, and non-claim gaps; Efficient ASI has a finite efficiency-claim admission lifecycle route for cost, quality, residual, fallback, hidden-cost, evidence-transition, and non-claim boundaries; and Coil Attention has a synthetic cyclic-memory contract harness for alias, sparse-coverage, recurrence, stale-read, structural-quality, and support-state non-promotion fixtures. | Keep those five modules as the first formal-depth workstream while continuing whole-book proof-depth slices one module at a time. The first anti-projection sweep is complete; the next goal is richer state, transitions, integration with harnesses, and stronger negative cases rather than theorem-count growth. |
| P0 | External review is too important to leave until preprints. | The evidence base is still mostly self-sourced: Corben's source papers, Project Theseus, Circle, local harnesses, and Codex/Claude planning reviews. | Add an early external-review milestone after evidence visibility, before deep proof/prototype work locks in the wrong target. |
| P0 | The field-impact path requires defended contributions, not a complete encyclopedia. | The 44 active chapters are useful as architecture coverage, but no single idea yet has enough depth, external grounding, and evidence to stand as a defended result. | Select three to five contribution tracks and push a smaller subset to A+ depth. |
| P0 | Some repetition is structural, not stylistic. | The 16-to-54 expansion created useful precision, and the Part I, conservative compression, intent/contracts, MoECOT, simulation-fidelity, static context ABI, verification/adversarial-review, planning/DAG, and semantic-representation packages have now reduced the active manifest to 44 chapters. Several remaining clusters still repeat the same chapter skeleton around overlapping claims. The useful target is not "shorter book"; it is one skeleton per real chapter-owning artifact. | Continue the governed consolidation queue one package at a time: execute, revise, defer, or reject existing destination drafts and fold dispositions while preserving ideas as sections/subclaims/proof hooks/source mappings and requiring claim/source/proof/reader/URL reconciliation before changing the manifest. |
| P0 | Planning churn is now a release risk. | The local tree has many planning and review surfaces, while the best recent progress came from executed packages that changed the manifest, archived retired chapters, and preserved URLs. The proof and evidence work has substance, but the consolidation track should keep moving by execution, not new packet layers. | Freeze new planning/report surfaces for existing packages. Execute or reject one merge or fold end to end before adding another consolidation document, then batch the rest using the executed packages as the template. |
| P0 | Chapter credibility requires external grounding, not only Corben-side source synthesis. | Appendix H already contains source-noted external literature, but the roadmap does not yet force every chapter to mine external comparators from the Corben papers it already cites. | Add a chapter-by-chapter external-grounding milestone: mine each chapter's linked Corben sources for bibliographies and adjacent work first, then add vetted third-party records to Appendix H through `sources/source_inventory.json` and source notes. |
| P1 | Appendix C hides the three earned non-core transitions too well. | Appendix C correctly says all 44 chapter core claims remain `argument`, but it does not make the three non-core transitions headline-visible. | Keep the separate non-core evidence ledger visible so readers can see what is actually measured without mistaking it for chapter-core promotion. |
| P1 | External-SOTA placement is technically closed but intellectually thin in places. | `docs/external_sota_positioning_audit.md` records 44 positioned chapters, 0 explicit exceptions, 0 open placement rows, and 0 missing targeted source notes after the current grounding cycle. | Keep the external-grounding records live: future chapter splits, merges, or new claims must preserve fair external baselines or record a deliberate exception. |
| P1 | Circle evidence is real but not yet a clean upstream replay. | `docs/circle_external_receipt_slice.md` records a local clean checkout and accepted rope receipt, and `docs/circle_public_replay_consumer_gate.md` now adds a CI-verifiable ASI-side consumer gate with negative controls. The ASI repo still does not rerun the external checkout in CI or vendor a public replay pack. | Treat the consumer gate as the first milestone closure, then pursue a public contract pack, archived evidence bundle, or clean replay before stronger claims. |
| P1 | Project Theseus is the right implementation reference; the first import is intentionally narrow. | `docs/local_project_mining_theseus_circle.md` records public-safe Theseus mining and source notes, and `docs/theseus_report_import_slice.md` now records one static digest-verified architecture-gate report import. The local checkout still had private/dirty surfaces, so no clean live Theseus replay or support-state transition exists. | Keep the static import as implementation-reference evidence only, then pursue a clean replay or archived public fixture before any stronger transition. |
| P2 | The reader edition is structurally mature but not yet a true human book. | Human view, reader overlays, reader spine checks, companion-note routing, and HTML artifact review exist; the curated manuscript path is now `drafting` with forty-three drafting-only curated chapter records and no release approval. | Continue curated chapter graduation only when prose changes are chapter-structural, not section-local. Treat the human-reader book as a parallel derivative manuscript for pacing, examples, and audio flow. |
| P2 | The project has many ledgers but still few promotions. | The v1.0.0 release was honest, and the current 44 core claims still remain `argument`; three narrow non-core claims moved upward. | Future roadmap work should close evidence gaps, not multiply status documents. Add ledgers only when they make support-state decisions clearer or enforceable. |

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
- The human-reader manuscript may change pacing, examples, openings, closings,
  and chapter flow, but it must not change claim meaning, support state, source
  boundary, proof/test status, or implementation horizon.
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
- three narrow non-core evidence transitions are recorded;
- all chapter core claims remain at `argument`;
- reader HTML is the only release-approved human artifact;
- EPUB, DOCX, PDF, e-reader app review, audio, DOI/Zenodo, screen-reader pass,
  and manual keyboard pass remain unresolved.

## Keystone Set And Dependency Order

The next serious run should not treat all milestones as equal. The keystone set
is:

1. keep the executed 44-chapter consolidation spine stable unless new evidence,
   external review, or human-reader edit findings expose a concrete duplicate
   artifact boundary;
2. deepen Lean proof coverage beyond the five safety-critical modules: for
   every chapter, replace projection-only hooks with at least one theorem over
   explicit records, transitions, negative cases, or state changes, or record a
   no-proof-yet blocker tied to the chapter claim;
3. finish the curated human-reader manuscript as an editable book against the
   current 44-chapter table of contents: reconcile curated source against the
   live book and prepare the manuscript for Corben's human edit rather than
   producing more per-chapter pass paperwork;
4. make the honesty system legible in 60 seconds from README, landing page, and
   Human view, and keep the three bounded non-core evidence transitions visible
   without chapter-core promotion;
5. solicit or record at least one external human review of the safety-critical,
   support-state, and first executed consolidation surfaces;
6. keep the chapter-level external-grounding lane current by mining each
   chapter's linked Corben papers for outside citations, recording vetted
   third-party sources in Appendix H, and marking genuine comparator gaps;
7. make one Project Theseus or Circle evidence lane public-safe and
   CI-reproducible or CI-verifiable by archived digest, then execute only the
   5-8 highest-payoff per-chapter evidence lanes from
   `docs/per_chapter_evidence_plan.md`.

Dependency order:

- Milestone 6.5 is now the first execution milestone. It should execute or
  explicitly reject/retain at least one package before any further
  consolidation planning surface is added. This still means the project must
  walk the governed consolidation decision queue before broad human-reader
  curation, but the walk now means execute, reject, or retain packaged work
  rather than writing more packet layers.
- Required validator phrasing: walk the governed consolidation decision queue before broad human-reader curation.
- Milestone 2 broadens after the safety-critical sweep: proof work should move
  chapter by chapter through projection-heavy modules, using the executed merge
  template to update proof tags when chapters merge.
- Milestone 7 depends on Milestone 6.5 for chapters in pending merge/fold
  clusters. Do not finalize human-reader prose for a chapter boundary that the
  roadmap still expects to remove.
- Milestones 0.5, 1, 1.5, 5.5, and the Theseus/Circle replay work remain
  active, but they should not displace merge execution, nontrivial proofs, or
  reader-manuscript readiness.
- Milestones 8 and 9 stay downstream: EPUB/PDF/DOCX/audio and preprints should
  wait for reconciled reader prose, executable proof/evidence improvements,
  prior-art checks, and at least one external review.

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

Acceptance bar:

- prior Pages run checked;
- working tree clean before starting a large pass;
- no stale generated scaffold after `python3 scripts/sync_scaffold.py`;
- no validator is silently bypassed or newly orphaned.

### Milestone 0.5 - Sixty-Second Trust Surface

Goal: make the project's strongest quality visible before a cold reader rounds
the work down to overbroad self-sourced theory.

Tasks:

- Update the README, landing page, and live Human view entry path so a first-time
  visitor can quickly see:
  - all 44 chapter core claims remain `argument`;
  - three bounded non-core evidence transitions exist and are narrow;
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
  - `circle-calculus.external_rope_receipt_replay` as `prototype-backed`.
- Link that surface from Appendix C without changing the fact that all 44
  chapter core claims remain `argument`.
- Add a validation check that prevents non-core transitions from being rendered
  as chapter-core promotions.
- Add a reviewer-facing "what would promote this" field for each chapter-core
  claim, derived from the per-chapter evidence plan below.

Acceptance bar:

- Appendix C or a sibling appendix surfaces the three earned transitions;
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
- `Alignment` now has a second v1.x depth increment: three additional derived
  constitutional-transition theorems model rollback-missing migration blocking,
  accepted-transition protected-predicate preservation, and unrouted conflict
  residualization over a richer finite record.
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
- `ValueConflict` now has a second v1.x depth increment: three additional
  derived review-decision theorems model high-stakes unresolved conflict
  blocking when residual uncertainty is missing, bounded-decision dissent
  residualization, and authority narrowing for unresolved conflict without
  authority narrowing.
- The generated proof-depth report records 532 theorem declarations, 411
  derived/decomposed declarations, 69 safety-critical declarations, and 10
  remaining safety-critical direct/projection declarations.
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
- `docs/proof_depth_classification.md` records 532 theorem declarations, 411
  derived/decomposed theorem declarations, and 121 direct/projection-style
  theorem declarations.
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
  preserved references nor supersession; this reduces the projection-only
  surface for Compact Generative Systems while leaving compact utility, codec
  correctness, reconstruction quality, repair-cost accounting, fallback
  behavior, semantic grounding quality, hierarchy-migration behavior,
  representation utility, model quality, and downstream consumer-policy tests
  as blockers.
- `AsiStackProofs.FastGeneration` now has finite negative-case theorems
  rejecting promotion candidates missing accepted-output or verifier-cost
  records, failed accelerated drafts without fallback or residual handling,
  and high-risk fast-mode selections without verifier, risk-override, or
  slower-fallback records plus a finite admission-lifecycle route for missing
  mode, context, risk, quality, verifier, acceptance, baseline, output, cost,
  fallback, residual, override, budget, evidence-transition, and
  non-claim-boundary records. This reduces the projection-only surface for
  Fast Generation while leaving actual autoregressive baselines, speculative
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
  dispatch, missing simulation scope, and fidelity overclaim; this reduces the
  projection-only surface for Resource Economics while leaving scheduler
  quality, real load stability, verification-tax optimization, KV-cache
  behavior, cost-quality economics, simulator adequacy, physical feasibility,
  and open-world transfer as blockers.
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
  rejecting high-risk execution without a bound approval receipt and external
  hive access with missing lease-boundary fields; this reduces the
  projection-only surface for Personal Compute Hives while leaving scheduler,
  registry, approval-service, federation, rented-node, connectivity, dropout,
  and energy-aware behavioral tests as blockers.
- `AsiStackProofs.RuntimeAdapters` now has finite negative-case theorems
  rejecting modeled invocations that lack parent-job permission and modeled
  high-impact unapproved adapter calls that try to remain unrejected; this
  reduces the projection-only surface for Runtime Adapters while leaving
  deployed adapter execution, sandbox isolation, approval-service behavior,
  secret-handle safety, rollback execution, and live effect-receipt validation
  as blockers.
- `AsiStackProofs.ProceduralMemory` now has finite negative-case theorems
  rejecting generated-tool records missing source traces, parameters, or
  verification results, and failed-regression reviews that try to keep routable
  promotion; this reduces the projection-only surface for Procedural Memory
  while leaving deployed loop detection, tool synthesis, generated-tool
  correctness, regression-quality benchmarking, routing monitors, and
  retirement automation as blockers.
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
- `AsiStackProofs.ArtifactGraph` now has finite negative-case theorems
  rejecting produced artifacts missing parent/source/context refs and
  incomplete or blocked provenance attempting promoted claim support; this
  reduces the projection-only surface for Artifact Graphs while leaving
  deployed artifact graph service behavior, real replay, audit reconstruction,
  provenance completeness checking, and imported produced-artifact traces as
  blockers.
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

Current status after the first ASI-side Project Theseus import:

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
- The remaining stronger milestone work is a clean Project Theseus replay or
  archived public release fixture plus any separate accepted evidence-transition
  record if a bounded non-core claim is later promoted.

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
  an ASI-side proof-contract consumer gate, not a new support-state transition,
  not a local Circle Lean rerun, not a vendored contract pack, and not a
  chapter-core promotion.
- The remaining stronger milestone work is a clean Circle replay, public
  contract pack, or archived public Circle artifact before model-quality,
  runtime, context-length, transfer, or deployment claims can be entertained.

### Milestone 5 - Per-Chapter Evidence Plan

Goal: maintain a named evidence lane for every chapter without turning the next
v1.x cycle into another shallow breadth sweep.

The full 44-row backlog lives in `docs/per_chapter_evidence_plan.md`. Treat that
file as a menu of possible lanes, not as a checklist to complete in one run. A
v1.x cycle should execute at most 5-8 chapter lanes, chosen for evidential
payoff and load-bearing importance; the rest stay `planned, not executed` with
no fixture built and no implied support-state movement.

Selection rule:

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
- the active v1.x cycle names the 5-8 selected lanes and explicitly leaves all
  others planned;
- any executed lane records command/replay path, negative controls where
  applicable, non-claims, and support-state effect;
- unexecuted lanes do not create fixtures, pass/fail claims, or support-state
  pressure.

Current status for the initial v1.x active evidence cycle:

- `docs/v1_x_active_evidence_cycle.md` selects eight chapter lanes:
  `evidence-states-and-claim-discipline`,
  `recursive-self-improvement-boundaries`,
  `resource-economics-and-token-budgets`,
  `circle-calculus-and-proof-carrying-ai-contracts`,
  `executable-specifications-and-lean-proof-envelope`,
  `project-theseus-as-report-first-implementation-reference`, and
  `living-book-methodology`, plus
  `coil-attention-cyclic-memory-and-recurrence-contracts`.
- The remaining thirty-six manifest chapter lanes are explicitly planned-only
  for this cycle.
- `scripts/validate_v1_x_active_evidence_cycle.py` enforces the selected-lane
  count, checks that selected plus planned-only lanes cover all 44 manifest
  chapters exactly once, and requires the current no-chapter-core-promotion
  boundary.
- The active-cycle record now includes the synthetic simulation-transfer
  boundary harness for Resource Economics and the cyclic-memory contract
  harness for Coil Attention. Both are useful gate hardening; neither creates a
  chapter-core support-state transition.

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
- `docs/chapter_consolidation_release_stability_review.md` now records a
  `deferred_for_release` reader-work outcome for every unexecuted
  review-ready or fold-disposition package in the consolidation queue. It is a
  release-stability decision for human-reader curation only: no merge or fold
  is executed, no package is permanently rejected, no destination draft is
  approved, no chapter count changes, no support state moves, and no external
  review is created. Curated reader work may now proceed inside those source
  chapters only when the prose-pass note records the relevant consolidation
  caveat.
- Broad reader polish may proceed inside deferred consolidation packages only
  when the relevant prose-pass record cites the release-stability caveat and
  preserves future reconciliation. That permission is release pragmatism, not
  an accepted merge, retained-chapter decision, support-state movement, or
  proof of table-of-contents quality. Local prose fixes may continue anywhere
  when they do not entrench duplicate chapter structure.
- The compression candidate should not be merged from the roadmap table,
  dry-run package, or destination draft alone. It still needs review and an
  execute-full, execute-conservative, revise, defer, or reject decision. The
  intent/contracts candidate should not be merged from the roadmap table,
  dry-run package, or destination draft alone. It still needs review and an
  execute, revise, defer, or reject decision. The static context ABI candidate
  should not be merged from the roadmap table, dry-run package, or destination
  draft alone. It still needs review and an execute, revise, defer, or reject
  decision. The verification/adversarial-review candidate should not be merged
  from the roadmap table, dry-run package, or destination draft alone. It still
  needs review and an execute, revise, defer, or reject decision. The
  planning/DAG-control candidate should not be merged from the roadmap table,
  dry-run package, or destination draft alone. It still needs review and an
  execute, revise, defer, or reject decision. The MoECOT runtime candidate now
  has `docs/chapter_consolidation_fold_moecot_runtime.md`, but it still needs
  review and an execute fold, revise, defer, or reject/retain decision before
  any `book_structure.json` change. The simulation-fidelity candidate now has
  `docs/chapter_consolidation_fold_simulation_fidelity.md`, but it still needs
  review and an execute fold, revise, defer, or reject/retain decision before
  any `book_structure.json` change. The semantic-representation candidate now
  has `docs/chapter_consolidation_fold_semantic_representation.md`, but it
  still needs review and an execute fold after destination-package review,
  revise, defer, or reject/retain decision before any `book_structure.json`
  change.
- No manifest merge has been performed yet, and no chapter count reduction is
  claimed. This is now the main work item, not a planning item.

### Milestone 7 - Curated Human-Reader Manuscript

Goal: make the normal reader version a book someone would enjoy reading or
listening to, while preserving the live book as the research/evidence source.

Execution pivot:

- Stop treating first-pass curated chapters as the finish line. The manuscript
  is not human-edit ready until consolidation decisions have been reflected in
  the reader table of contents, every remaining chapter has either curated
  prose or a recorded reason to wait, and a book-level continuity edit has
  removed repeated scaffolding and repaired transitions.
- The next reader task is not another review report. It is to finish the
  remaining non-curated chapters where their boundaries survive consolidation,
  then reconcile the curated manuscript against the post-merge live book.
- Human-reader source may become a parallel derivative prose source for
  pacing, examples, openings, closings, and audio flow, but the live book
  remains authority for claims, support states, source boundaries, proof/test
  status, implementation horizons, and release records.

Tasks:

- Select a consolidation-aware pilot set for curated graduation. Protected
  standalone chapters may graduate when overlays are too small; source chapters
  inside pending merge or fold packages should wait for an execute, revise,
  defer, or reject decision unless the edit is explicitly scoped as local
  cleanup:
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
- After consolidation execution starts, run a book-level reader edit over the
  destination table of contents, not the old pre-consolidation 54-chapter shape. This pass should
  remove duplicated introductions, repair part transitions, normalize examples,
  and make the prose ready for Corben's human editing notes.

Acceptance bar:

- curated chapters validate against
  `scripts/validate_reader_manuscript_manifest.py`;
- reconciliation report records no hidden claim changes;
- each curated chapter is either outside pending consolidation clusters or
  records a scoped/deferred handoff caveat;
- Human view and generated reader edition still preserve support-state
  boundaries.
- a human-edit handoff packet exists with the current table of contents,
  known repetition debt, unresolved evidence blockers, chapters ready for line
  edit, and chapters blocked by pending merge/fold decisions.

Current status:

- `editions/reader_manuscript/v1_0/manifest.json` is in `drafting` status with
  44 active curated chapter records after the Part I, conservative compression,
  intent/contracts, MoECOT, and simulation-fidelity folds. Retired standalone
  curated drafts are archived under
  `editions/reader_manuscript/v1_0/archive/retired_chapters/` and are
  historical reference only.
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
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_asi_stack_prose_pass.md` records the curation scope,
  meaning-preservation checks, non-claims, and remaining blockers for that
  pass.
- `editions/reader_manuscript/v1_0/chapters/the-efficient-asi-hypothesis.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_efficient_asi_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, and remaining
  blockers for that pass.
- `editions/reader_manuscript/v1_0/chapters/system-boundaries-and-authority.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_system_boundaries_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and no-deployed-enforcement boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/failure-modes-of-ungoverned-intelligence.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_failure_modes_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, remaining blockers,
  and no scenario-coverage or deployed detection/prevention boundary for that
  pass.
- `editions/reader_manuscript/v1_0/chapters/evidence-states-and-claim-discipline.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_evidence_states_prose_pass.md` records the curation
  scope, reader promise, meaning-preservation checks, non-claims, remaining
  blockers, and no-support-state-movement boundary for that pass.
- `editions/reader_manuscript/v1_0/chapters/human-intent-as-a-formal-input.qmd`
  now has a first curated prose pass from the generated reader baseline as a
  drafting source only.
- `docs/curated_reader_human_intent_prose_pass.md` records the curation scope,
  reader promise, meaning-preservation checks, non-claims, remaining blockers,
  and pending Part I consolidation handoff caveat for that pass.
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
  lineage, and active reader work must stay on the destination chapter.
- `editions/reader_manuscript/v1_0/chapters/moral-uncertainty-and-value-conflict.qmd`
  is now the active curated destination for **Moral Uncertainty, Value
  Conflict, and Contestable Governance**. The former
  `governance-rights-fork-exit-and-audit` reader draft is archived as
  historical lineage, and active reader work must stay on the destination
  chapter.
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
- The three dense proof/governance companion-note candidates now have drafting
  companion notes under `editions/reader_manuscript/v1_0/companion_notes/`:
  Circle proof receipts, executable-specification proof lanes, and
  artifact-steward project objects. These notes support e-reader and audio
  treatment without moving meaning-critical proof, governance, release, or
  non-claim limits out of the reader spine.
- `editions/reader_manuscript/v1_0/reconciliation_report.md` records the
  drafting row and keeps `reader_release_record_not_created`,
  `format_artifact_not_reviewed`, and
  `curated_reconciliation_not_approved` blockers active.
- No curated reader chapter is release-approved, and generated reader HTML
  remains the only reviewed reader artifact.
- Two current manifest chapters still lack curated reader manuscript files:
  `compact-generative-systems-and-residual-honesty`,
  and `rankfold-neuralfold-and-artifact-compression`. Because each sits inside a
  representation or retained-technique reader decision, finish or defer them only
  after the relevant consolidation or curation decision.

### Milestone 8 - Visual, Ebook, PDF, DOCX, And Audio Quality

Goal: make the major-version human artifacts pleasant, navigable, and honest.

Tasks:

- Continue using Human view for casual web readers.
- Treat reader HTML as the reviewed baseline artifact until EPUB, DOCX, PDF,
  and audio have exact release records.
- Add chapter-level diagrams only when they clarify mechanisms, not as
  decoration.
- For EPUB:
  - inspect in at least one real e-reader app or device path;
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
- visual assets have text equivalents or walkthrough notes.

Current status:

- `scripts/build_audio_script.py --check` generates 59 review-script files and
  verifies that every chapter script preserves both implementation-horizon
  sections.
- The generated audio workspace now includes `pronunciation_glossary.md` and
  `proof_equation_reading_rules.md`. The latter is a required review artifact
  for theorem IDs, equations, support states, proof statuses, schema fields,
  hashes, and negative controls; it does not approve narration or any audio
  artifact.
- `editions/reader_manuscript/v1_0/audio_script_probe_manifest.json`,
  `docs/reader_audio_script_probe_manifest.md`, and
  `scripts/validate_reader_audio_script_probe_manifest.py` now record and
  validate the tracked local audio-script probe: 51 script files, preserved
  implementation horizons, 8 table treatment notes, 54 Mermaid diagram notes,
  1 image note, and MP3/M4B/audio-embedded EPUB targets still marked
  `target_not_generated`. This is not narration approval, an audiobook, or an
  audio release record.

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
| Execution-over-reports gate | At least one review-ready consolidation package has executed or been explicitly rejected/retained before any new consolidation planning packet is added for an existing package. | The roadmap is still producing planning surface instead of reducing duplicate chapter structure. |
| Sixty-second trust surface | README, landing page, or Human view entry path makes current evidence, non-claims, proof limits, self-sourcing boundaries, and external-review status legible quickly. | Cold readers cannot distinguish disciplined research program from overbroad theory. |
| Non-core evidence visibility | Appendix C or sibling surface names the three current non-core transitions and keeps all 44 core claims at `argument` unless separately promoted. | Readers cannot tell what evidence exists. |
| Early external review | At least one external review record exists, or a dated blocker records outreach and scope. | The release remains self-reviewed. |
| Defended contribution focus | The release names three to five contribution tracks and at most three deep-work tracks for the cycle. | The project remains broad without defended results. |
| Safety-critical Lean depth | Five targeted modules include `derived_or_decomposed` theorem coverage, anti-projection conclusions, and negative cases, or a release record explicitly keeps them projection-only. | Formal layer remains v1.0-depth. |
| Public replay/import | At least one Theseus or Circle lane is CI-replayed or CI-verifiable by pinned digest with negative controls. | Imported evidence remains local-summary only. |
| Chapter-lane cap | The release names 5-8 executed chapter lanes and leaves the rest planned; no 44-lane synthetic sweep is claimed. | Breadth trap not controlled. |
| Per-chapter external grounding | Every chapter has source-noted external comparators, candidate backlog, or an explicit exception; accepted third-party records appear in generated Appendix H. | The book still reads as self-sourced nomenclature. |
| Proof/evidence coverage | Each executed lane names whether its strongest evidence path is Lean, Theseus, Circle, external literature, external review, or an explicit no-promotion blocker. | Arguments remain prose-only without a testable support route. |
| External-SOTA distance | The release updates distance from SOTA, not only internal activity. | "Beyond-SOTA" remains unaudited. |
| Governed consolidation review | The release either executes or explicitly defers the reviewed consolidation pilot, with preserved source/proof/claim/reader mappings and no hidden idea deletion. | Human-reader curation may polish avoidable duplicate chapter skeletons. |
| Negative-outcome handling | Failed, demoted, refuted, merged, or retired lanes are recorded instead of hidden. | Evidence process is monotonic and biased. |
| Human-reader quality | Curated reader pilot or explicit deferral exists; any released artifact has an exact release record. | Human edition remains a generated projection only. |
| Artifact honesty | EPUB/DOCX/PDF/audio/DOI are claimed only if exact artifacts or archive identifiers exist. | Artifact or archive claim would be fabricated. |

## Version Targets

| Target | Position vs SOTA | Minimum bar |
|---|---|---|
| `v1.1` | Moves from internal release hygiene toward externally reviewable evidence process. | Sixty-second trust surface exists; non-core evidence ledger visible; early external review requested or recorded; defended contribution tracks selected; per-chapter evidence plan split out with 5-8 lane cap; chapter-level external-grounding workflow defined; safety-critical proof specs include anti-projection and negative-case criteria. |
| `v1.2` | Moves formal layer from projection-heavy traceability toward lightweight state-specification practice for safety-critical modules. | Five safety-critical modules gain `derived_or_decomposed` theorem coverage, anti-projection conclusions, and negative cases; first public-safe Theseus or Circle lane is CI-replayed or CI-verifiable by digest. |
| `v1.3` | Moves structural cohesion and reader surface from generated projection toward a consolidated, curated human manuscript while preserving live-book evidence authority. | The 44-chapter consolidation spine remains stable unless a concrete duplicate-boundary finding reopens it; curated reader manuscript follows the current table of contents; reader HTML remains validated; EPUB/DOCX/PDF blockers have concrete review status; audio script uses curated prose only where reviewed. |
| `v1.x evidence release` | Becomes stronger than v1.0.0 by evidence depth, not by blanket coverage. | The v1.x release gate passes; 5-8 selected chapter lanes have executed evidence or explicit no-promotion decisions; every chapter has external-grounding status; core claims promote only where evidence-transition records justify it. |
| `v2.0` | Becomes a public research program with external scrutiny, archived artifacts, and reproducible evidence packs. | External review, archived release, polished human editions, reproducible Theseus/Circle evidence packs, stronger Lean envelopes, prior-art-reviewed preprints, and DOI/archive metadata exist. |

## Suggested Long-Running Goal

Use this wording when it is time to start the next large autonomous work run:

> Execute the v1.x roadmap for **The ASI Stack** in implementation-first mode and bring the project to true human-review readiness. Keep the executed 44-chapter consolidation spine stable unless new evidence, external review, or human-reader edit findings expose a concrete duplicate artifact boundary; do not create more planning/report surfaces for already packaged work. Deepen Lean proof coverage across all chapters, not only the five safety-critical modules: each chapter should gain at least one nontrivial theorem over explicit records, transitions, negative cases, residual paths, receipts, authority ceilings, readiness gates, or support-state boundaries, or a visible no-proof-yet blocker tied to the core claim. Finish the curated human-reader manuscript against the current table of contents, create a human-edit handoff packet for Corben, and keep the reader edition subordinate to the live AI/research evidence source. Continue only high-payoff evidence work that changes proof, replay, source, claim, or artifact state: maintain the 60-second trust surface, keep non-core evidence visible without chapter-core promotion, solicit or record external human review, keep per-chapter external grounding current through source-noted Appendix H records, make Project Theseus or Circle evidence CI-replayable or digest-verifiable where public-safe, execute only selected high-payoff evidence lanes, and record demotions, rejections, blockers, and non-claims honestly. Before every commit, check the latest completed GitHub Pages run; run the relevant local validation gate, Lean build when proof code changes, and Quarto render for changed public surfaces; commit and push coherent increments. Never fabricate source content, citations, proof results, test results, support-state promotions, external-review records, artifact approvals, deployment readiness, model quality, benchmark performance, or completed ebook/PDF/DOCX/audio artifacts.

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
