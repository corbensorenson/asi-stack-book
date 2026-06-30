# v1.x Beyond-SOTA Roadmap

Last updated: 2026-06-30

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
book: manifest-driven structure, 54 drafted chapters, source notes, claim/source
traceability, finite-record Lean hooks, schema fixtures, reader profiles,
Human view, a reviewed reader HTML artifact, a deployed Quarto site, and three
narrow non-core evidence transitions.

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
- the 54-chapter expansion may now be over-split in several thematic clusters,
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
- Codex verification of Claude's claims against the local tree;
- `book_structure.json`, which currently defines four parts, 54 chapters, and
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
| P0 | The 54-lane evidence plan can reintroduce the breadth trap. | The first roadmap version named a lane and acceptance bar for every chapter, which is useful as backlog but dangerous as an execution checklist. | Move the 54-row plan to `docs/per_chapter_evidence_plan.md`, cap each v1.x cycle at 5-8 executed lanes, and leave the rest explicitly planned. |
| P0 | The project's strongest quality is the least legible one. | The validation, support-state discipline, and non-claim machinery are real, but a cold reader first sees broad scope, self-coined terms, and many self-sourced ideas. | Add a 60-second trust surface and make the evidence discipline visible before readers infer overreach. |
| P0 | Safety-critical Lean depth is improving but still shallow. | `docs/proof_depth_classification.md` now records 158 theorem declarations, 112 direct/projection-style, 46 derived/decomposed, and 29 safety-critical theorem declarations. Each of `Alignment`, `Corrigibility`, `GovernanceRights`, `SelfImprovement`, and `ValueConflict` has at least one derived/decomposed finite-record theorem plus explicit projection-only limitation prose; `Alignment`, `Corrigibility`, `GovernanceRights`, and `ValueConflict` now each have four derived/decomposed transition/control/preservation/review theorems, and `SelfImprovement` now has three derived/decomposed lifecycle/review theorems, while 10 safety-critical theorem declarations remain direct/projection-style. | Keep those five modules as the first formal-depth workstream. The first anti-projection sweep is complete; the next goal is richer state, transitions, integration with harnesses, and stronger negative cases rather than theorem-count growth. |
| P0 | External review is too important to leave until preprints. | The evidence base is still mostly self-sourced: Corben's source papers, Project Theseus, Circle, local harnesses, and Codex/Claude planning reviews. | Add an early external-review milestone after evidence visibility, before deep proof/prototype work locks in the wrong target. |
| P0 | The field-impact path requires defended contributions, not a complete encyclopedia. | The 54 chapters are useful as architecture coverage, but no single idea yet has enough depth, external grounding, and evidence to stand as a defended result. | Select three to five contribution tracks and push a smaller subset to A+ depth. |
| P0 | Some repetition is structural, not stylistic. | The 16-to-54 expansion created useful precision, but several clusters now repeat the same chapter skeleton around overlapping claims. Several consolidation packages are now review-ready, but no manifest merge has been authorized. The useful target is not "shorter book"; it is one skeleton per real chapter-owning artifact. | Add a governed consolidation milestone with a decision queue: review the existing destination drafts, execute/revise/defer/reject one cluster at a time, preserve ideas as sections/subclaims/proof hooks/source mappings, and require claim/source/proof/reader/URL reconciliation before changing the manifest. |
| P0 | Chapter credibility requires external grounding, not only Corben-side source synthesis. | Appendix H already contains source-noted external literature, but the roadmap does not yet force every chapter to mine external comparators from the Corben papers it already cites. | Add a chapter-by-chapter external-grounding milestone: mine each chapter's linked Corben sources for bibliographies and adjacent work first, then add vetted third-party records to Appendix H through `sources/source_inventory.json` and source notes. |
| P1 | Appendix C hides the three earned non-core transitions too well. | Appendix C correctly says all 54 chapter core claims remain `argument`, but it does not make the three non-core transitions headline-visible. | Add a separate non-core evidence ledger section or companion appendix so readers can see what is actually measured without mistaking it for chapter-core promotion. |
| P1 | External-SOTA placement is technically closed but intellectually thin in places. | `docs/external_sota_positioning_audit.md` records 54 positioned chapters, 0 explicit exceptions, 0 open placement rows, and 0 missing targeted source notes after the current grounding cycle. | Keep the external-grounding records live: future chapter splits, merges, or new claims must preserve fair external baselines or record a deliberate exception. |
| P1 | Circle evidence is real but not yet a clean upstream replay. | `docs/circle_external_receipt_slice.md` records a local clean checkout and accepted rope receipt, and `docs/circle_public_replay_consumer_gate.md` now adds a CI-verifiable ASI-side consumer gate with negative controls. The ASI repo still does not rerun the external checkout in CI or vendor a public replay pack. | Treat the consumer gate as the first milestone closure, then pursue a public contract pack, archived evidence bundle, or clean replay before stronger claims. |
| P1 | Project Theseus is the right implementation reference; the first import is intentionally narrow. | `docs/local_project_mining_theseus_circle.md` records public-safe Theseus mining and source notes, and `docs/theseus_report_import_slice.md` now records one static digest-verified architecture-gate report import. The local checkout still had private/dirty surfaces, so no clean live Theseus replay or support-state transition exists. | Keep the static import as implementation-reference evidence only, then pursue a clean replay or archived public fixture before any stronger transition. |
| P2 | The reader edition is structurally mature but not yet a true human book. | Human view, reader overlays, reader spine checks, companion-note routing, and HTML artifact review exist; the curated manuscript path is now `drafting` with thirty-five drafting-only curated chapter records and no release approval. | Continue curated chapter graduation only when prose changes are chapter-structural, not section-local. Treat the human-reader book as a parallel derivative manuscript for pacing, examples, and audio flow. |
| P2 | The project has many ledgers but still few promotions. | The v1.0.0 release was honest: 54 core claims remain `argument`; three narrow non-core claims moved upward. | Future roadmap work should close evidence gaps, not multiply status documents. Add ledgers only when they make support-state decisions clearer or enforceable. |

## Operating Principles

- Retire IOUs before adding new control surfaces.
- Do not promote support states unless an accepted evidence-transition record
  names the evidence, command or replay path, limitations, counterevidence, and
  non-claims.
- Prefer narrow evidence transitions that are true over broad support language
  that sounds stronger than the artifact.
- Lean targets should prove actual invariants over explicit records or state
  transitions, not only restate field projections.
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
- all 54 current chapters exist with required sections, source mappings, proof
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

1. make the honesty system legible in 60 seconds from README, landing page, and
   Human view;
2. surface the three bounded non-core evidence transitions without chapter-core
   promotion;
3. solicit at least one external human review of the safety-critical and
   support-state surfaces;
4. add a chapter-level external-grounding lane that mines each chapter's linked
   Corben papers for outside citations, records vetted third-party sources in
   Appendix H, and marks any genuine comparator gaps;
5. select three to five defended contribution tracks and push at most three in
   the next cycle;
6. deepen the five safety-critical Lean modules using anti-projection criteria;
7. make one Project Theseus or Circle evidence lane public-safe and
   CI-reproducible or CI-verifiable by archived digest;
8. execute only 5-8 per-chapter evidence lanes from
   `docs/per_chapter_evidence_plan.md`, selected for evidential payoff.
9. run the governed consolidation decision queue before broad human-reader
   curation, so review-ready packages either execute, revise, defer, or reject
   and genuinely overlapping chapters become deeper chapters rather than
   repeated skeletons. Treat the 54-to-44/47 count as a diagnostic estimate,
   not an objective; the objective is clearer chapter ownership.

Dependency order:

- Milestone 0.5, Milestone 1, and Milestone 1.5 can start immediately.
- Milestones 2, 3, and 4 should use the external-review result if it arrives
  before implementation begins.
- Milestone 5 depends on the selection rules and should not start as a
  top-to-bottom sweep; Milestone 5.5 can start as a source-discovery pass, but
  citations still require source notes before prose use.
- Milestone 6.5 should happen before broad Milestone 7 curation because the
  human-reader manuscript should not polish avoidable structural repetition.
  It should now prioritize decisions on review-ready packages over producing
  more consolidation prose for already packaged clusters.
- Milestones 7 and 8 are downstream of reader-prose review and should not
  produce final artifacts before curated prose or release records exist.
- Milestone 9 preprints should wait for prior-art/novelty checks and at least
  one external review.

## Beyond-SOTA Distance Map

The v1.0 Beyond-SOTA Reference Map in `docs/v1_0_roadmap.md` remains the
baseline. This roadmap measures progress by movement against that map, not by
internal activity alone.

| Dimension | Current distance from SOTA | v1.x movement target |
|---|---|---|
| Formal verification | Below full functional-correctness work; currently broad finite-record hooks with many projections. | Become competitive with lightweight state-specification practice for five safety-critical modules: explicit states, transitions, negative cases, and derived invariants. |
| Living evidence methodology | Structurally strong but still mostly self-sourced and ledger-heavy. | Become externally reviewable: visible non-core evidence, exact non-claims, public replay or CI-verifiable digests, and no hidden promotion. |
| Governance/safety architecture | Coherent argument-level stack, not deployed safety validation. | Strengthen through external review, safety-critical Lean envelopes, and at least one reproducible implementation trace. |
| Routing/resource efficiency | One bounded synthetic selector slice; below real routing SOTA and no deployed scheduler evidence. | Extend only if a public fixture or trace includes baseline, negative control, quality/adequacy, cost, residuals, and replay. |
| Compression/representation | Mostly architecture and source synthesis; Circle receipt is structural, not model-quality evidence. | Add one narrow artifact-compression, representation-preservation, or proof-contract lane with negative controls before stronger claims. |
| Human/AI dual-edition publishing | Unusual and promising scaffold with reviewed reader HTML; not yet a polished human book or audio edition. | Graduate selected reader chapters into curated prose and approve artifacts only through exact release records. |
| External literature/novelty | Placement gate now records 54/54 positioned chapters and 0 explicit external-baseline exceptions, but novelty questions and the depth of external engagement still remain. Some chapters can still read as Corben-originated nomenclature before readers see enough related outside literature. | Maintain the per-chapter external-grounding pack, keep mining citations inside each chapter's linked Corben papers, replace any future or regressed weak exception with source-noted literature where possible, perform prior-art checks before preprints, and record where the project is competitive, below SOTA, or genuinely novel. |
| Structural cohesion | The manifest is dynamic and complete, but the 54-chapter shape may preserve too much skeleton-level repetition in overlapping clusters. | Decide the review-ready consolidation packages in priority order, starting with the alignment/governance pilot, then continue only when claim identity, source mappings, proof hooks, reader overlays, URL/history treatment, and handoffs stay intact. |

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
  review. It preserves the harder gap that no chapter core claim has yet been
  truly demoted or refuted.
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
  - all 54 chapter core claims remain `argument`;
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
- Link that surface from Appendix C without changing the fact that all 54
  chapter core claims remain `argument`.
- Add a validation check that prevents non-core transitions from being rendered
  as chapter-core promotions.
- Add a reviewer-facing "what would promote this" field for each chapter-core
  claim, derived from the per-chapter evidence plan below.

Acceptance bar:

- Appendix C or a sibling appendix surfaces the three earned transitions;
- the chapter-core matrix still reports 54 `argument` support states;
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
- The generated proof-depth report records 158 theorem declarations, 46
  derived/decomposed declarations, 29 safety-critical declarations, and 10
  remaining safety-critical direct/projection declarations.
- The relevant chapter limitation sections now state what these finite-record
  proofs do and do not justify.
- No chapter core claim support state moved above `argument`; the next formal
  step is richer lifecycle/review semantics and tighter links to replayed
  harnesses, not broad safety language.

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

The full 54-row backlog lives in `docs/per_chapter_evidence_plan.md`. Treat that
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

- `docs/per_chapter_evidence_plan.md` remains current with all 54 chapter lanes;
- the active v1.x cycle names the 5-8 selected lanes and explicitly leaves all
  others planned;
- any executed lane records command/replay path, negative controls where
  applicable, non-claims, and support-state effect;
- unexecuted lanes do not create fixtures, pass/fail claims, or support-state
  pressure.

Current status for the initial v1.x active evidence cycle:

- `docs/v1_x_active_evidence_cycle.md` selects seven chapter lanes:
  `evidence-states-and-claim-discipline`,
  `recursive-self-improvement-boundaries`,
  `resource-economics-and-token-budgets`,
  `circle-calculus-and-proof-carrying-ai-contracts`,
  `executable-specifications-and-lean-proof-envelope`,
  `project-theseus-as-report-first-implementation-reference`, and
  `living-book-methodology`.
- The remaining forty-seven manifest chapter lanes are explicitly planned-only
  for this cycle.
- `scripts/validate_v1_x_active_evidence_cycle.py` enforces the selected-lane
  count, checks that selected plus planned-only lanes cover all 54 manifest
  chapters exactly once, and requires the current no-chapter-core-promotion
  boundary.

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

- Aggressive consolidation could move the current 54-chapter shape toward
  roughly 44 deeper chapters.
- Conservative consolidation could leave the book closer to 47 chapters by
  keeping technique-owning chapters such as RankFold/NeuralFold separate.
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
- The Part I pilot is now `review_ready`, meaning destination drafts exist but
  require an execute, revise, defer, or reject decision plus execution of the
  retired-URL treatment required by
  `docs/chapter_consolidation_url_history_policy.md` before any canonical
  chapter identity changes.
- Compression, intent/contracts, static context ABI, verification/adversarial
  review, and planning/DAG control now have dry-run packages and one-skeleton
  destination drafts but remain unmerged. MoECOT, simulation fidelity, and
  semantic representation now have fold dispositions; semantic representation
  remains dependency-bound to the compression/representation package decision
  before any reader curation or manifest edit depends on it.
- The 2026-06-30 follow-up does not add a new cluster. It strengthens the
  next-work rule: judge the current packages in order, then execute, revise,
  defer, or reject/retain them with a recorded reason before source chapters in
  those clusters are treated as stable reader-manuscript targets.
- Broad human-reader curation should not harden duplicate chapter skeletons in
  a pending consolidation cluster. Local prose cleanup is still allowed, but
  curated-reader graduation for those source chapters should wait until the
  cluster is executed, explicitly deferred for the release, or rejected/retained
  with a reason.

Consolidation decision queue:

The next consolidation work should not create more destination drafts for
packages that are already `review_ready`. It should walk a decision queue and
produce an explicit execute, revise, defer, or reject result for each package
before broad reader curation treats the source chapters as stable.

| Order | Package | Required decision | Execution note |
|---|---|---|---|
| 1 | Part I constitutional alignment and agency/corrigibility | Execute, revise, defer, or reject. | Follow `docs/chapter_consolidation_url_history_policy.md` for the retired agency/corrigibility URL before any manifest edit. |
| 2 | Part I value conflict and contestable governance | Execute, revise, defer, or reject. | Follow `docs/chapter_consolidation_url_history_policy.md` for the retired governance-rights URL and preserve fork, exit, audit, redaction, appeal, dissent, and revisit interfaces as sections or subclaims. |
| 3 | Compression and residual honesty | Execute full merge, execute conservative merge, revise, defer, or reject. | The conservative branch keeps RankFold/NeuralFold standalone if review finds technique ownership. |
| 4 | Intent and executable contracts | Execute, revise, defer, or reject. | Keep `human-intent-as-a-formal-input` as the intent-intake chapter and remove only duplicated contract skeleton. |
| 5 | Static context ABI | Execute, revise, defer, or reject. | Keep context transactions and verification bandwidth standalone unless a later review changes their artifact ownership. |
| 6 | Verification and adversarial review | Execute, revise, defer, or reject. | Keep claim ledgers standalone as the belief-revision substrate. |
| 7 | Planning and DAG control | Execute, revise, defer, or reject. | Keep cognitive compilation standalone as the semantic-IR and lowering-receipt layer. |
| 8 | Fold-disposition candidates | Execute fold, revise, defer, or reject/retain. | MoECOT runtime, simulation fidelity, and semantic representation already have fold dispositions; the next work is review and decision, not more packaging, before any manifest edit. |

Each decision record should name the reviewed package, reviewer or review
source, destination-skeleton judgment, claim/source/proof/reader impact,
external-grounding adequacy, URL or redirect policy, validation scope,
support-state effect, non-claims, and the exact decision. If execution is
accepted, implement one cluster per commit so rollback and review remain
legible. If a package is deferred or rejected, record the reader-work
disposition so curated prose may continue without pretending the repetition
question disappeared.

Consolidation execution gate:

- A review-ready merge package may not be executed only because it reduces the
  table of contents. It must show that one destination skeleton improves the
  argument by making the mechanism, evidence path, proof limits, implementation
  horizon, and reader handoff clearer than the separate source chapters.
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
| Tier 1 | Alignment/governance philosophy; compression/representation; intent/contracts; context/memory static ABI. | These clusters repeat the most source families, chapter skeletons, and handoff language. They should become fewer deeper chapters first if reconciliation passes. | About 14 source chapters become about 8-10 destination chapters, depending on whether RankFold/NeuralFold remains standalone. |
| Tier 2 | Verification/review; planning/control; MoECOT placeholder fold. | These merges reduce thin or source-blocked chapters while preserving distinct substrates such as claim ledgers and cognitive IR. | About 7 source chapters become about 4-5 destination chapters. |
| Fold-only review | Simulation fidelity and physical constraints; semantic representation and tree-structured models. | These look more like bounded feasibility or representation-substrate sections than standalone chapter-owning artifacts unless evidence review says otherwise. | Remove standalone skeletons only if their claims survive as named sections and subclaims. |
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
  - consider merging `compact-generative-systems-and-residual-honesty`,
    `generate-verify-repair-compression`, and
    `rankfold-neuralfold-and-artifact-compression`, with a conservative option
    that keeps RankFold/NeuralFold separate if it still owns enough concrete
    technique;
  - default destination title if the full merge passes:
    **Compact Generative Systems: Generate, Verify, Repair, and Residual
    Honesty**;
  - review whether `semantic-representation-and-tree-structured-models` should
    remain standalone or become the representation-substrate section of the
    compression/representation cluster.
- Intent and contracts:
  - consider merging `intent-to-execution-contracts` with
    `command-contracts-and-semantic-interfaces`;
  - default destination title if the merge passes: **Command Contracts: From
    Intent to Executable Work**;
  - keep `human-intent-as-a-formal-input` as the Part I intent-intake chapter,
    but slim it so it hands off instead of restating the Part II contract
    chapter.
- Context/memory:
  - consider merging `virtual-context-abi` with
    `semantic-pages-context-cells-and-certificates`;
  - default destination title if the merge passes: **The Virtual Context ABI:
    Typed Pages, Cells, and Certificates**;
  - keep `context-transactions-snapshots-mounts-and-taint` and
    `verification-bandwidth-and-context-adequacy` separate unless a later review
    finds real overlap in artifact ownership.
- Verification/review:
  - consider merging `spinoza-verification-and-proof-carrying-claims` with
    `unified-adaptive-tribunal-and-adversarial-review`;
  - default destination title if the merge passes: **Proof-Carrying Claims and
    Adversarial Review**;
  - keep `claim-ledgers-and-belief-revision` separate as the substrate they
    update.
- Planning:
  - consider merging `planning-as-a-control-layer` with
    `planforge-dags-and-intelligence-arbitrage`;
  - default destination title if the merge passes: **Planning as a Control
    Layer: DAGs and Intelligence Arbitrage**;
  - keep `cognitive-compilation-and-semantic-ir` separate as the lowering/IR
    artifact unless a pilot shows the IR claim has no independent chapter
    ownership.
- Possible folds:
  - fold `moecot-runtime-and-multi-core-orchestration` into
    `routing-heads-and-specialist-cores` if its source remains insufficiently
    mined for standalone chapter evidence;
  - review `docs/chapter_consolidation_fold_simulation_fidelity.md` and fold
    `simulation-fidelity-and-physical-constraints` into
    `resource-economics-and-token-budgets` as a Simulation Fidelity and Claim
    Transport section if its standalone claim remains only a feasibility-bound
    note; keep the efficient-ASI frame as secondary context rather than the
    owning destination;
  - review `docs/chapter_consolidation_fold_semantic_representation.md` and
    fold `semantic-representation-and-tree-structured-models` into the
    compression/representation cluster only if its representation-substrate
    claim remains a supporting facet rather than a chapter-owning artifact, and
    only after the compression/representation destination package has a reviewed
    decision;
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

- Start with one pilot cluster, preferably the alignment/governance philosophy
  cluster, before applying a broad 54-to-44 reshaping.
- Create a cluster-specific reconciliation plan before every non-pilot merge.
  The plan should name the destination title, source chapters, stable-ID
  policy, claim dispositions, source-ID union, external-source union, proof-tag
  union, test/harness rows, reader-overlay changes, handoff repairs,
  implementation-horizon merge, and expected chapter-count effect.
- Before editing `book_structure.json`, produce a dry-run merge package for the
  selected pilot. The package should include a proposed manifest diff, the
  destination chapter's one-skeleton section outline, an Appendix C
  core-claim/subclaim reconciliation table, Lean module and proof-manifest
  treatment, source and external-source unions, reader-overlay and Handoff
  repairs, implementation-horizon merge, URL or redirect decision, and a
  no-support-state-change boundary.
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

- at least one pilot merge plan exists before any manifest merge;
- a dry-run merge package exists and is reviewed before any pilot manifest
  merge;
- the pilot names every preserved source, subclaim, proof hook, test row,
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
  compression, intent/contract, context, verification, planning, MoECOT,
  simulation-fidelity, semantic-representation, and low-priority runtime-adapter
  candidates each require their own package or explicit review decision before
  any future manifest edit.
- The sequence now records consolidation states so candidates cannot jump from
  "interesting idea" to manifest change: the Part I pilot is `review_ready`,
  compression, intent/contracts, static context ABI, verification/adversarial
  review, and planning/DAG control are `review_ready`, the remaining
  non-packaged merge clusters are `planned_candidate`, MoECOT runtime,
  simulation fidelity, and semantic representation are
  `fold_disposition_ready`, and runtime-adapters/Labor OS is retained unless a
  later evidence review finds duplicate artifact ownership.
- The pilot proposes two future merges:
  `constitutional-alignment-substrate` with
  `agency-dignity-and-corrigibility`, and
  `moral-uncertainty-and-value-conflict` with
  `governance-rights-fork-exit-and-audit`.
- The roadmap now records a tiered consolidation sequence and diagnostic target
  shape: an aggressive pass may land near 44 chapters, while a conservative
  pass may land near 47, but the count is only a diagnostic for repetition
  reduction and never a reason to drop an idea.
- `scripts/validate_chapter_consolidation_sequence.py` keeps the sequence
  visible from the roadmap, README, publication readiness, and repository map
  while confirming the canonical manifest still has 54 chapters.
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
  finds distinct technique ownership. It leaves
  `semantic-representation-and-tree-structured-models` outside the merge until
  `docs/chapter_consolidation_fold_semantic_representation.md` is reviewed
  alongside the compression package.
- `docs/chapter_consolidation_destination_draft_compression.md` now records the
  first non-pilot review-ready destination draft for **Compact Generative
  Systems: Generate, Verify, Repair, and Residual Honesty**. It is intentionally
  not marked reviewed: manifest consolidation remains blocked until review
  accepts a full merge, accepts the conservative GVR-only merge, asks for
  revision, defers, or rejects the merge.
- `docs/chapter_consolidation_dry_run_intent_contracts.md` records the Tier 1C
  dry-run package for **Command Contracts: From Intent to Executable Work**. It
  proposes keeping `intent-to-execution-contracts` as the continuity ID,
  folding `command-contracts-and-semantic-interfaces`, and keeping
  `human-intent-as-a-formal-input` standalone as the raw-intent intake,
  ambiguity, authority-extraction, bounded-default, re-contract, and
  stop-condition chapter.
- `docs/chapter_consolidation_destination_draft_intent_contracts.md` now
  records the review-ready destination draft for **Command Contracts: From
  Intent to Executable Work**. It is intentionally not marked reviewed:
  manifest consolidation remains blocked until review accepts, revises, defers,
  or rejects the merge.
- `docs/chapter_consolidation_dry_run_context_abi.md` records the Tier 1D
  dry-run package for **The Virtual Context ABI: Typed Pages, Cells, and
  Certificates**. It proposes keeping `virtual-context-abi` as the continuity
  ID, folding `semantic-pages-context-cells-and-certificates` as preserved
  typed-page and certificate subclaims, and keeping
  `context-transactions-snapshots-mounts-and-taint`,
  `verification-bandwidth-and-context-adequacy`, and
  `claim-ledgers-and-belief-revision` standalone.
- `docs/chapter_consolidation_destination_draft_context_abi.md` now records
  the review-ready destination draft for **The Virtual Context ABI: Typed
  Pages, Cells, and Certificates**. It is intentionally not marked reviewed:
  manifest consolidation remains blocked until review accepts, revises, defers,
  or rejects the merge.
- `docs/chapter_consolidation_dry_run_verification_review.md` records the Tier
  2A dry-run package for **Proof-Carrying Claims and Adversarial Review**. It
  proposes keeping `spinoza-verification-and-proof-carrying-claims` as the
  continuity ID, folding
  `unified-adaptive-tribunal-and-adversarial-review` as preserved tribunal and
  adversarial-review subclaims, and keeping
  `claim-ledgers-and-belief-revision` standalone as the durable claim substrate.
- `docs/chapter_consolidation_destination_draft_verification_review.md` now
  records the review-ready destination draft for **Proof-Carrying Claims and
  Adversarial Review**. It is intentionally not marked reviewed: manifest
  consolidation remains blocked until review accepts, revises, defers, or
  rejects the merge.
- `docs/chapter_consolidation_dry_run_planning_dag.md` records the Tier 2B
  dry-run package for **Planning as a Control Layer: DAGs and Intelligence
  Arbitrage**. It proposes keeping `planning-as-a-control-layer` as the
  continuity ID, folding `planforge-dags-and-intelligence-arbitrage` as
  preserved DAG scheduling and intelligence-arbitrage subclaims, and keeping
  `cognitive-compilation-and-semantic-ir` standalone as the semantic IR and
  lowering-receipt chapter.
- `docs/chapter_consolidation_destination_draft_planning_dag.md` now records
  the review-ready destination draft for **Planning as a Control Layer: DAGs
  and Intelligence Arbitrage**. It is intentionally not marked reviewed:
  manifest consolidation remains blocked until review accepts, revises, defers,
  or rejects the merge.
- `docs/chapter_consolidation_decision_review.md` records the current decision:
  defer manifest consolidation until human or external review accepts, revises,
  defers, or rejects the destination drafts, while
  `docs/chapter_consolidation_url_history_policy.md` now records the public URL
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
  representation remain the packages to decide. The roadmap accepts the
  recommendation's central rule that every accepted package must collapse
  duplicated skeletons while preserving ideas as sections, subclaims, proof
  hooks, source mappings, implementation horizons, reader paths, or explicit
  no-promotion/retirement decisions.
- `docs/chapter_consolidation_destination_draft_constitutional_alignment.md`
  now records the first review-ready destination draft for
  **Constitutional Alignment: Agency, Dignity, and Corrigibility**. It is
  intentionally not marked reviewed: manifest consolidation remains blocked
  until human or external review accepts the destination shape, or the project
  records a decision to defer or reject the merge.
- `docs/chapter_consolidation_destination_draft_contestable_governance.md`
  now records the second review-ready destination draft for **Moral
  Uncertainty, Value Conflict, and Contestable Governance**. It is intentionally
  not marked reviewed: manifest consolidation remains blocked until human or
  external review accepts the destination shape, or the project records a
  decision to defer or reject the merge.
- `docs/chapter_consolidation_external_review_packet.md` now gives reviewers a
  focused decision surface for the pilot: execute, revise, defer, or reject
  each proposed merge, while preserving the boundary that review input is not
  evidence, proof, artifact approval, or support-state movement.
- `docs/chapter_consolidation_full_review_packet.md` now gives reviewers a
  full decision-queue surface for all review-ready merge packages and fold
  dispositions, including the five non-pilot destination drafts and the three
  fold-disposition packages. It is a request surface only: no external review
  has been accepted, no package is authorized, no manifest edit is made, and no
  support state moves.
- `docs/chapter_consolidation_release_stability_review.md` now records a
  `deferred_for_release` reader-work outcome for every unexecuted
  review-ready or fold-disposition package in the consolidation queue. It is a
  release-stability decision for human-reader curation only: no merge or fold
  is executed, no package is permanently rejected, no destination draft is
  approved, no chapter count changes, no support state moves, and no external
  review is created. Curated reader work may now proceed inside those source
  chapters only when the prose-pass note records the relevant consolidation
  caveat.
- Broad reader polish should avoid the four pending Part I consolidation source
  chapters unless the release-stability caveat is recorded. Reader curation may
  continue on chapters outside the pending cluster, and local prose fixes may
  continue anywhere when they do not entrench duplicate chapter structure.
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
  claimed.

### Milestone 7 - Curated Human-Reader Manuscript

Goal: make the normal reader version a book someone would enjoy reading or
listening to, while preserving the live book as the research/evidence source.

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

Acceptance bar:

- curated chapters validate against
  `scripts/validate_reader_manuscript_manifest.py`;
- reconciliation report records no hidden claim changes;
- each curated chapter is either outside pending consolidation clusters or
  records a scoped/deferred handoff caveat;
- Human view and generated reader edition still preserve support-state
  boundaries.

Current status:

- `editions/reader_manuscript/v1_0/manifest.json` is now in `drafting` status
  with thirty-five curated chapter records:
  `asi-is-a-stack-not-a-model`,
  `the-efficient-asi-hypothesis`,
  `system-boundaries-and-authority`,
  `failure-modes-of-ungoverned-intelligence`,
  `evidence-states-and-claim-discipline`,
  `human-intent-as-a-formal-input`,
  `security-kernel-and-digital-scifs`,
  `stable-capability-fields`,
  `capability-replacement-and-rollback`,
  `readiness-gates-residual-escrow-and-quarantine`,
  `cognitive-compilation-and-semantic-ir`,
  `context-transactions-snapshots-mounts-and-taint`,
  `verification-bandwidth-and-context-adequacy`,
  `claim-ledgers-and-belief-revision`,
  `labor-os-and-typed-jobs`,
  `artifact-graphs-audit-logs-and-replay`,
  `runtime-adapters-tool-permissions-and-human-approval`,
  `procedural-memory-and-cognitive-loop-closure`,
  `benchmark-ratchets-and-anti-goodhart-evidence`,
  `policy-optimization-and-learning-from-feedback`,
  `integrated-reference-architecture`,
  `project-theseus-as-report-first-implementation-reference`,
  `prototype-roadmap`,
  `living-book-methodology`,
  `open-research-agenda-and-bibliography-plan`,
  `personal-compute-hives-and-federated-edge-intelligence`,
  `resource-economics-and-token-budgets`,
  `fast-generation-architectures`,
  `mathematical-and-search-substrates`,
  `coil-attention-cyclic-memory-and-recurrence-contracts`,
  `coilra-multicoil-rope-and-cyclic-mixers`,
  `recursive-self-improvement-boundaries`,
  `circle-calculus-and-proof-carrying-ai-contracts`,
  `executable-specifications-and-lean-proof-envelope`, and
  `artifact-steward-agents-and-living-project-governance`.
- The current curated set follows the consolidation-aware curation gate: it
  favors protected standalone chapters outside pending merge packages, with
  `human-intent-as-a-formal-input` recorded as local prose work whose handoff
  must be revisited if later consolidation decisions change the downstream
  contract or alignment chapter shape.
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
  validate the tracked local audio-script probe: 59 script files, preserved
  implementation horizons, 5 table treatment notes, 60 Mermaid diagram notes,
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
three no-promotion examples that resisted evidence or artifact laundering. This
is useful progress, but it is not a true demotion/refutation record. The first
real demotion, refutation, retirement, or claim-narrowing event still needs to
be recorded when evidence justifies it.

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
| Sixty-second trust surface | README, landing page, or Human view entry path makes current evidence, non-claims, proof limits, self-sourcing boundaries, and external-review status legible quickly. | Cold readers cannot distinguish disciplined research program from overbroad theory. |
| Non-core evidence visibility | Appendix C or sibling surface names the three current non-core transitions and keeps all 54 core claims at `argument` unless separately promoted. | Readers cannot tell what evidence exists. |
| Early external review | At least one external review record exists, or a dated blocker records outreach and scope. | The release remains self-reviewed. |
| Defended contribution focus | The release names three to five contribution tracks and at most three deep-work tracks for the cycle. | The project remains broad without defended results. |
| Safety-critical Lean depth | Five targeted modules include `derived_or_decomposed` theorem coverage, anti-projection conclusions, and negative cases, or a release record explicitly keeps them projection-only. | Formal layer remains v1.0-depth. |
| Public replay/import | At least one Theseus or Circle lane is CI-replayed or CI-verifiable by pinned digest with negative controls. | Imported evidence remains local-summary only. |
| Chapter-lane cap | The release names 5-8 executed chapter lanes and leaves the rest planned; no 54-lane synthetic sweep is claimed. | Breadth trap not controlled. |
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
| `v1.3` | Moves reader surface from generated projection toward a curated human manuscript while preserving live-book evidence authority. | Governed consolidation has walked the review-ready decision queue far enough to execute, revise, defer, or reject the pilot packages and the existing fold-disposition candidates; curated reader manuscript covers a coherent pilot arc or explicitly defers with blockers; reader HTML remains validated; EPUB/DOCX/PDF blockers have concrete review status; audio script uses curated prose only where reviewed. |
| `v1.x evidence release` | Becomes stronger than v1.0.0 by evidence depth, not by blanket coverage. | The v1.x release gate passes; 5-8 selected chapter lanes have executed evidence or explicit no-promotion decisions; every chapter has external-grounding status; core claims promote only where evidence-transition records justify it. |
| `v2.0` | Becomes a public research program with external scrutiny, archived artifacts, and reproducible evidence packs. | External review, archived release, polished human editions, reproducible Theseus/Circle evidence packs, stronger Lean envelopes, prior-art-reviewed preprints, and DOI/archive metadata exist. |

## Suggested Long-Running Goal

Use this wording when it is time to start the next large autonomous work run:

> Advance **The ASI Stack** from the tagged `v1.0.0` living-book release toward a true v1.x evidence-and-reader release by executing `docs/v1_x_beyond_sota_roadmap.md` in dependency order. Preserve release integrity, check prior GitHub Pages failures before each commit, create a 60-second trust surface that makes current evidence and non-claims legible to a cold reader, surface the three bounded non-core evidence transitions without promoting chapter core claims, solicit or record an early external human review, mine every chapter's linked Corben papers for external citations and adjacent literature, add accepted third-party sources through `sources/source_inventory.json`, source notes, and generated Appendix H, select three to five defended contribution tracks and push at most three deeply in this cycle, deepen the five safety-critical Lean modules with anti-projection criteria and negative cases, create at least one public-safe Project Theseus or Circle replay lane that CI can replay or verify by pinned digest, select only 5-8 high-payoff chapter lanes from `docs/per_chapter_evidence_plan.md` for execution while leaving the rest planned, ensure every selected lane names its strongest proof/evidence path or no-promotion blocker, keep external-SOTA placement current and replace any future or regressed weak exception where source-noted literature exists, walk the governed consolidation decision queue before broad human-reader curation, execute only one accepted merge or fold package at a time after source/proof/claim/reader reconciliation, and record explicit revise, defer, or reject decisions for packages that should not merge in the current release, record negative outcomes and demotions honestly, graduate human-reader chapters into curated prose when overlays are insufficient, prepare EPUB/PDF/DOCX/audio only after reviewed artifacts exist, run the full local validation gate, update changelog and release-control docs, and never fabricate source content, proof/test results, support-state promotions, or artifact approvals.

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
