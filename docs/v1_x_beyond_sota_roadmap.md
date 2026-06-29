# v1.x Beyond-SOTA Roadmap

Last updated: 2026-06-29

This roadmap is the post-`v1.0.0` long-term plan for turning **The ASI
Stack** from a tagged living-book release into a stronger evidence-and-reader
program. It should be read with `docs/v1_0_candidate_status.md`,
`docs/v1_progress_ledger.md`, `docs/v1_0_release_gate_audit.md`,
`docs/proof_depth_classification.md`, `docs/proof_adequacy_review.md`,
`docs/external_sota_positioning_audit.md`, and
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
- Project Theseus and Circle evidence need public-safe replay paths rather than
  local-only summaries;
- the human-reader edition needs to become a true edited book, not only a strip
  of the AI/research source;
- EPUB, DOCX, PDF, and audio should be treated as reviewed edition artifacts
  only after exact artifact records exist.

## Inputs Reconciled

This roadmap reconciles:

- the current repository state after the tagged `v1.0.0` living-book release;
- the current Claude review supplied by Corben as planning input;
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
| P0 | Safety-critical Lean depth is still shallow. | `docs/proof_depth_classification.md` records 139 theorem declarations, 112 direct/projection-style, 27 derived/decomposed, and all 10 theorem declarations in `Alignment`, `Corrigibility`, `GovernanceRights`, `SelfImprovement`, and `ValueConflict` as direct/projection-style. | Make those five modules the first formal-depth workstream. The goal is not more theorem count; it is richer state, transitions, negative cases, and derived invariants. |
| P0 | External review is too important to leave until preprints. | The evidence base is still mostly self-sourced: Corben's source papers, Project Theseus, Circle, local harnesses, and Codex/Claude planning reviews. | Add an early external-review milestone after evidence visibility, before deep proof/prototype work locks in the wrong target. |
| P1 | Appendix C hides the three earned non-core transitions too well. | Appendix C correctly says all 54 chapter core claims remain `argument`, but it does not make the three non-core transitions headline-visible. | Add a separate non-core evidence ledger section or companion appendix so readers can see what is actually measured without mistaking it for chapter-core promotion. |
| P1 | External-SOTA placement is technically closed but intellectually thin in places. | `docs/external_sota_positioning_audit.md` records 44 positioned chapters, 10 explicit exceptions, 0 open placement rows, and 0 missing targeted source notes. | Replace weak exceptions where external baselines exist. Keep true author-system exceptions, but state why they are exceptions and what would count as a comparable external reference. |
| P1 | Circle evidence is real but not public-replayable enough. | `docs/circle_external_receipt_slice.md` records a local clean checkout and accepted rope receipt, but the ASI repo does not rerun the external checkout in CI and does not vendor a public replay pack. | Create a public-safe Circle replay fixture, receipt contract pack, or archived evidence bundle that CI can verify by replay or digest. |
| P1 | Project Theseus is the right implementation reference but not yet evidence-imported. | `docs/local_project_mining_theseus_circle.md` records public-safe Theseus mining and source notes, but the local checkout had private/dirty surfaces and no first replayed Theseus report was imported. | Define a Theseus report schema, select public-safe trace classes, import the first trace only after sanitization, and connect it to specific chapter evidence lanes. |
| P2 | The reader edition is structurally mature but not yet a true human book. | Human view, reader overlays, reader spine checks, companion-note routing, and HTML artifact review exist; curated manuscript status remains `not_graduated`. | Start curated chapter graduation when prose changes are chapter-structural, not section-local. Treat the human-reader book as a parallel derivative manuscript for pacing, examples, and audio flow. |
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
- The human-reader manuscript may change pacing, examples, openings, closings,
  and chapter flow, but it must not change claim meaning, support state, source
  boundary, proof/test status, or implementation horizon.
- Audio and e-reader artifacts should come after reader-prose review, not
  before it.
- The roadmap must be able to lose: claims can be demoted or refuted, chapters
  can be merged or cut, and reviewer/prior-art findings can redirect work.

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

1. surface the three bounded non-core evidence transitions without chapter-core
   promotion;
2. solicit at least one external human review of the safety-critical and
   support-state surfaces;
3. deepen the five safety-critical Lean modules using anti-projection criteria;
4. make one Project Theseus or Circle evidence lane public-safe and
   CI-reproducible or CI-verifiable by archived digest;
5. execute only 5-8 per-chapter evidence lanes from
   `docs/per_chapter_evidence_plan.md`, selected for evidential payoff.

Dependency order:

- Milestone 1 and Milestone 1.5 can start immediately.
- Milestones 2, 3, and 4 should use the external-review result if it arrives
  before implementation begins.
- Milestone 5 depends on the selection rules and should not start as a
  top-to-bottom sweep.
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
| External literature/novelty | Placement gate passes, but some exceptions and novelty questions remain. | Replace weak exceptions, perform prior-art checks before preprints, and record where the project is competitive, below SOTA, or genuinely novel. |

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
- do not execute a lane only because it appears early in manifest order.

Acceptance bar:

- `docs/per_chapter_evidence_plan.md` remains current with all 54 chapter lanes;
- the active v1.x cycle names the 5-8 selected lanes and explicitly leaves all
  others planned;
- any executed lane records command/replay path, negative controls where
  applicable, non-claims, and support-state effect;
- unexecuted lanes do not create fixtures, pass/fail claims, or support-state
  pressure.

### Milestone 6 - External-SOTA Exception Replacement

Goal: move from "placement gate passes" to "external engagement is strong
enough for serious readers."

Tasks:

- Review the 10 exception chapters from
  `docs/external_sota_positioning_audit.md`.
- For each exception, choose one:
  - add source-noted external baselines and in-prose positioning;
  - keep a true exception with a clear reason;
  - split the chapter's claim if part of it has external comparators and part
    of it is author-originated architecture.
- Prioritize likely replaceable exceptions:
  - `constitutional-alignment-substrate`;
  - `moral-uncertainty-and-value-conflict`;
  - `security-kernel-and-digital-scifs`;
  - `unified-adaptive-tribunal-and-adversarial-review`;
  - `coil-attention-cyclic-memory-and-recurrence-contracts`;
  - `coilra-multicoil-rope-and-cyclic-mixers`.
- Preserve true author-system exceptions only when no fair external baseline is
  currently sourced.

Acceptance bar:

- every exception has an explicit rationale and next source target;
- chapters with available literature stop relying on exception status;
- source notes exist before prose uses new external baselines.

### Milestone 7 - Curated Human-Reader Manuscript

Goal: make the normal reader version a book someone would enjoy reading or
listening to, while preserving the live book as the research/evidence source.

Tasks:

- Select a pilot set for curated graduation:
  - `asi-is-a-stack-not-a-model`;
  - `the-efficient-asi-hypothesis`;
  - `human-intent-as-a-formal-input`;
  - `recursive-self-improvement-boundaries`;
  - `circle-calculus-and-proof-carrying-ai-contracts`;
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
- Human view and generated reader edition still preserve support-state
  boundaries.

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
| Non-core evidence visibility | Appendix C or sibling surface names the three current non-core transitions and keeps all 54 core claims at `argument` unless separately promoted. | Readers cannot tell what evidence exists. |
| Early external review | At least one external review record exists, or a dated blocker records outreach and scope. | The release remains self-reviewed. |
| Safety-critical Lean depth | Five targeted modules include `derived_or_decomposed` theorem coverage, anti-projection conclusions, and negative cases, or a release record explicitly keeps them projection-only. | Formal layer remains v1.0-depth. |
| Public replay/import | At least one Theseus or Circle lane is CI-replayed or CI-verifiable by pinned digest with negative controls. | Imported evidence remains local-summary only. |
| Chapter-lane cap | The release names 5-8 executed chapter lanes and leaves the rest planned; no 54-lane synthetic sweep is claimed. | Breadth trap not controlled. |
| External-SOTA distance | The release updates distance from SOTA, not only internal activity. | "Beyond-SOTA" remains unaudited. |
| Negative-outcome handling | Failed, demoted, refuted, merged, or retired lanes are recorded instead of hidden. | Evidence process is monotonic and biased. |
| Human-reader quality | Curated reader pilot or explicit deferral exists; any released artifact has an exact release record. | Human edition remains a generated projection only. |
| Artifact honesty | EPUB/DOCX/PDF/audio/DOI are claimed only if exact artifacts or archive identifiers exist. | Artifact or archive claim would be fabricated. |

## Version Targets

| Target | Position vs SOTA | Minimum bar |
|---|---|---|
| `v1.1` | Moves from internal release hygiene toward externally reviewable evidence process. | Non-core evidence ledger visible; early external review requested or recorded; per-chapter evidence plan split out with 5-8 lane cap; safety-critical proof specs include anti-projection and negative-case criteria. |
| `v1.2` | Moves formal layer from projection-heavy traceability toward lightweight state-specification practice for safety-critical modules. | Five safety-critical modules gain `derived_or_decomposed` theorem coverage, anti-projection conclusions, and negative cases; first public-safe Theseus or Circle lane is CI-replayed or CI-verifiable by digest. |
| `v1.3` | Moves reader surface from generated projection toward a curated human manuscript while preserving live-book evidence authority. | Curated reader manuscript covers a coherent pilot arc or explicitly defers with blockers; reader HTML remains validated; EPUB/DOCX/PDF blockers have concrete review status; audio script uses curated prose only where reviewed. |
| `v1.x evidence release` | Becomes stronger than v1.0.0 by evidence depth, not by blanket coverage. | The v1.x release gate passes; 5-8 selected chapter lanes have executed evidence or explicit no-promotion decisions; core claims promote only where evidence-transition records justify it. |
| `v2.0` | Becomes a public research program with external scrutiny, archived artifacts, and reproducible evidence packs. | External review, archived release, polished human editions, reproducible Theseus/Circle evidence packs, stronger Lean envelopes, prior-art-reviewed preprints, and DOI/archive metadata exist. |

## Suggested Long-Running Goal

Use this wording when it is time to start the next large autonomous work run:

> Advance **The ASI Stack** from the tagged `v1.0.0` living-book release toward a true v1.x evidence-and-reader release by executing `docs/v1_x_beyond_sota_roadmap.md` in dependency order. Preserve release integrity, check prior GitHub Pages failures before each commit, surface the three bounded non-core evidence transitions without promoting chapter core claims, solicit or record an early external human review, deepen the five safety-critical Lean modules with anti-projection criteria and negative cases, create at least one public-safe Project Theseus or Circle replay lane that CI can replay or verify by pinned digest, select only 5-8 high-payoff chapter lanes from `docs/per_chapter_evidence_plan.md` for execution while leaving the rest planned, replace weak external-SOTA exceptions where source-noted literature exists, record negative outcomes and demotions honestly, graduate human-reader chapters into curated prose when overlays are insufficient, prepare EPUB/PDF/DOCX/audio only after reviewed artifacts exist, run the full local validation gate, update changelog and release-control docs, and never fabricate source content, proof/test results, support-state promotions, or artifact approvals.

## Non-Claims

- This roadmap does not promote any chapter core claim above `argument`.
- This roadmap does not prove ASI capability, model quality, runtime safety,
  deployment readiness, benchmark performance, economic outcome, source
  interpretation, or transfer.
- This roadmap does not create a public-safe Project Theseus import, public
  Circle replay pack, EPUB, PDF, DOCX, audio artifact, DOI, Zenodo archive, or
  external review record.
- This roadmap does not make curated reader prose equal authority beside the
  live AI/research book.
