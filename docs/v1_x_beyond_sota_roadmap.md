# v1.x Beyond-SOTA Roadmap

Last updated: 2026-06-29

This roadmap is the post-`v1.0.0` long-term plan for turning **The ASI
Stack** from a tagged living-book release into a stronger evidence-and-reader
program. It should be read with `docs/v1_0_candidate_status.md`,
`docs/v1_progress_ledger.md`, `docs/v1_0_release_gate_audit.md`,
`docs/proof_depth_classification.md`, `docs/proof_adequacy_review.md`,
`docs/external_sota_positioning_audit.md`, and
`docs/local_project_mining_theseus_circle.md`.

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

- every chapter needs a named evidence lane, with Lean, Project Theseus,
  Circle, a deterministic harness, external literature, or an imported public
  receipt carrying the work;
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

| Finding | Verified state | Roadmap consequence |
|---|---|---|
| Safety-critical Lean depth is still shallow | `docs/proof_depth_classification.md` records 139 theorem declarations, 112 direct/projection-style, 27 derived/decomposed, and all 10 theorem declarations in `Alignment`, `Corrigibility`, `GovernanceRights`, `SelfImprovement`, and `ValueConflict` as direct/projection-style. | Make those five modules the first formal-depth workstream. The goal is not more theorem count; it is richer state, transitions, negative cases, and derived invariants. |
| Appendix C hides the three earned non-core transitions too well | Appendix C correctly says all 54 chapter core claims remain `argument`, but it does not make the three non-core transitions headline-visible. | Add a separate non-core evidence ledger section or companion appendix so readers can see what is actually measured without mistaking it for chapter-core promotion. |
| External-SOTA placement is technically closed but intellectually thin in places | `docs/external_sota_positioning_audit.md` records 44 positioned chapters, 10 explicit exceptions, 0 open placement rows, and 0 missing targeted source notes. | Replace weak exceptions where external baselines exist. Keep true author-system exceptions, but state why they are exceptions and what would count as a comparable external reference. |
| Circle evidence is real but not public-replayable enough | `docs/circle_external_receipt_slice.md` records a local clean checkout and accepted rope receipt, but the ASI repo does not rerun the external checkout in CI and does not vendor a public replay pack. | Create a public-safe Circle replay fixture, receipt contract pack, or archived evidence bundle. Then add an ASI consumer gate that checks the receipt as an imported artifact. |
| Project Theseus is the right implementation reference but not yet evidence-imported | `docs/local_project_mining_theseus_circle.md` records public-safe Theseus mining and source notes, but the local checkout had private/dirty surfaces and no first replayed Theseus report was imported. | Define a Theseus report schema, select public-safe trace classes, import the first trace only after sanitization, and connect it to specific chapter evidence lanes. |
| The reader edition is structurally mature but not yet a true human book | Human view, reader overlays, reader spine checks, companion-note routing, and HTML artifact review exist; curated manuscript status remains `not_graduated`. | Start curated chapter graduation when prose changes are chapter-structural, not section-local. Treat the human-reader book as a parallel derivative manuscript for pacing, examples, and audio flow. |
| The project has many ledgers but still few promotions | The v1.0.0 release was honest: 54 core claims remain `argument`; three narrow non-core claims moved upward. | Future roadmap work should close evidence gaps, not multiply status documents. Add ledgers only when they make support-state decisions clearer or enforceable. |

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

- all five modules contain at least one nontrivial derived theorem whose proof
  depends on multiple fields or transition cases;
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
- the report names a reproducible source commit or archived fixture;
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
- ASI validation can reject malformed or overclaimed Circle receipts;
- chapter prose distinguishes proof-contract legality from model quality,
  context length, speed, memory scaling, or ASI capability.

### Milestone 5 - Per-Chapter Evidence Plan

Goal: every chapter has a named next evidence move. The table below is a plan,
not a current support-state claim.

| Part | Chapter | Primary evidence lane | Formal/prototype work | Human-reader focus | Acceptance bar before support-state change |
|---|---|---|---|---|---|
| I | `asi-is-a-stack-not-a-model` | Lean plus architecture trace | Deepen `StackBoundaries` with multi-layer handoff states and authority rejection cases. | Open the book with a concrete system story instead of taxonomy. | A state-machine proof plus a replayed handoff fixture; no broad ASI claim. |
| I | `the-efficient-asi-hypothesis` | Cost/resource harness plus external routing literature | Extend the costed-route slice beyond toy routes and tie it to budget ledgers. | Explain efficiency as "do only the expensive work that earns its cost." | Public fixture with baseline, negative control, and repeated run record. |
| I | `system-boundaries-and-authority` | Lean authority transitions | Connect authority ceiling, denial receipt, and confused-deputy harnesses. | Make authority boundaries feel like operating-system permissions. | Derived theorem or harness showing escalation blocked across handoff paths. |
| I | `failure-modes-of-ungoverned-intelligence` | Red-team scenarios plus Lean invariant violation | Add composed failure cases spanning authority, context, and evaluator capture. | Use a small number of memorable failure stories. | Replayed red-team fixture routes residuals to claims/tests/proofs. |
| I | `evidence-states-and-claim-discipline` | Claim ledger harness and evidence-transition ledger | Surface non-core transitions and enforce no-promotion decisions. | Turn support states into plain-language reader promises. | Appendix C/sibling ledger validates transitions without core-claim promotion. |
| I | `human-intent-as-a-formal-input` | Lean intent contract plus command-contract fixtures | Add intent ambiguity, delegation, and approval cases. | Ground formal intent in everyday instruction failures. | Intent fixture rejects underspecified or authority-widening execution. |
| I | `constitutional-alignment-substrate` | Safety-critical Lean | Deepen protected predicate, migration, and self-modification rules. | Explain a constitution as a change-control surface, not a slogan. | Nontrivial theorem over protected predicates and transition cases. |
| I | `agency-dignity-and-corrigibility` | Safety-critical Lean plus agency-right harness | Deepen review, appeal, high-impact approval, and interruption semantics. | Make dignity concrete through usable refusal, audit, and appeal paths. | Derived theorem plus harness case showing high-impact action blocked without usable review. |
| I | `moral-uncertainty-and-value-conflict` | Safety-critical Lean plus value-conflict harness | Deepen uncertainty residuals, dissent, and revisit conditions. | Show value conflict as engineering for unresolved disagreement. | High-stakes unresolved conflict cannot become unconditional promotion. |
| I | `governance-rights-fork-exit-and-audit` | Safety-critical Lean plus governance-right harness | Deepen fork/exit/audit preservation obligations. | Make rights readable through concrete project governance scenes. | Proof or fixture shows redaction/fork still preserves audit and safety obligations. |
| I | `stable-capability-fields` | Stable capability field harness plus Theseus gate | Import or synthesize field qualification and route-permission traces. | Explain stable fields as swappable certified capabilities. | Qualification fixture with rollback/residual path and no route widening. |
| I | `capability-replacement-and-rollback` | Replacement transaction harness | Connect replacement evidence, rollback, monitor state, and residual escrow. | Use product-upgrade analogies without losing safety constraints. | Valid replacement transaction and invalid promotion fixture both replay. |
| I | `security-kernel-and-digital-scifs` | Security-kernel harness plus external security baselines | Add SCIF lifecycle, revocation, sanitization, and prompt-injection negative controls. | Make SCIFs feel like controlled rooms and handles, not jargon. | Receipt fixture proves handle-mediated use and rejects leak paths. |
| I | `recursive-self-improvement-boundaries` | Safety-critical Lean plus Theseus self-evolution gate | Deepen accepted/rejected change model, evaluator separation, monitor window, and rollback. | Present RSI as controlled maintenance, not runaway mythology. | Accepted transition cannot widen authority or weaken protected invariants without review. |
| II | `intent-to-execution-contracts` | Command-contract fixtures plus Lean | Connect formal intent records to typed execution artifacts. | Show the path from "what I meant" to "what the system may do." | Invalid intent-to-action mismatch is rejected with receipt. |
| II | `command-contracts-and-semantic-interfaces` | Schema/fixture/Lean crosswalk | Add richer semantic interface fixtures and mismatch cases. | Explain contracts as readable promises between layers. | Schema, fixture, and Lean abstraction agree or document intentional abstraction. |
| II | `planning-as-a-control-layer` | Theseus plan compiler plus Lean planning envelope | Import public-safe typed DAG and rejected invalid DAG. | Make planning read like controlled sequencing under uncertainty. | Public-safe DAG replay validates and invalid DAG fails. |
| II | `planforge-dags-and-intelligence-arbitrage` | Theseus/PlanForge report | Validate arbitrage selection with costs, uncertainty, and fallback. | Explain intelligence arbitrage as routing work to the right kind of mind. | Fixture selects a route only when adequacy and cost constraints both pass. |
| II | `cognitive-compilation-and-semantic-ir` | Compiler IR fixtures plus external program-synthesis baselines | Add semantic atom lowering and failed-preservation cases. | Use compilation as the bridge from thought to executable structure. | IR translation preserves required fields and rejects lossy lowering. |
| II | `virtual-context-abi` | Context admission harness plus VCM source notes | Add admission, mount, capability, and context-window negative controls. | Make context feel like memory with permissions and receipts. | Admission fixture rejects stale, conflicting, or mode-confused packets. |
| II | `semantic-pages-context-cells-and-certificates` | Certificate fixtures plus Lean | Link certificates to context-cell admission and adequacy checks. | Explain certificates as labels that decide what memory can be trusted for. | Stale/missing certificate blocks use and records residual. |
| II | `context-transactions-snapshots-mounts-and-taint` | Context transaction harness | Add deletion closure, mount taint, snapshot conflict, and rollback cases. | Make taint and snapshots legible through file-system examples. | Transaction replay proves conflict/deletion gates fire. |
| II | `verification-bandwidth-and-context-adequacy` | Adequacy harness plus external context-eval literature | Add verifier-capacity constraints and escalation paths. | Explain why a model cannot verify everything it can read. | Adequacy record rejects context that exceeds verifier bandwidth. |
| II | `claim-ledgers-and-belief-revision` | Claim-ledger harness plus Lean | Add revision-history preservation, contradiction quarantine, and split claims. | Make belief revision read like version control for truth claims. | Contradictory evidence changes ledger state without silent promotion. |
| II | `spinoza-verification-and-proof-carrying-claims` | Proof-carrying claim harness plus Circle lane | Add verifier mismatch and tier downgrade cases. | Explain proof-carrying claims through receipts, not mystique. | Invalid proof artifact blocks claim tier escalation. |
| II | `unified-adaptive-tribunal-and-adversarial-review` | Tribunal harness plus external review baselines | Add reviewer capture, dissent, and required-action cases. | Present tribunals as adversarial review loops for hard decisions. | Captured or evidence-thin verdict cannot become accepted review. |
| II | `labor-os-and-typed-jobs` | Theseus operator OS plus typed-job fixtures | Import a public-safe job lifecycle trace. | Make agent labor feel like accountable work tickets. | Job cannot dispatch without requirements, permissions, and receipt path. |
| II | `artifact-graphs-audit-logs-and-replay` | Artifact graph replay harness plus Theseus report | Add graph integrity, provenance mismatch, and replay failure cases. | Show artifacts as memory the system can audit. | Replay reproduces expected graph or records exact divergence. |
| II | `runtime-adapters-tool-permissions-and-human-approval` | Runtime adapter harness plus Theseus operator OS | Add approval expiry, rollback handles, irreversible residuals, and authority receipts. | Make tool use feel like bounded action with human checkpoints. | High-impact adapter call fails without current approval and receipt. |
| II | `procedural-memory-and-cognitive-loop-closure` | Theseus self-evolution/operator traces plus loop harness | Add policy update, regression, and rollback memory traces. | Explain learning as disciplined update of procedures, not vague improvement. | Memory update fixture preserves failed attempts and rollback path. |
| III | `routing-heads-and-specialist-cores` | Routing harness plus MoE literature | Extend route-quality and specialist-readiness fixtures. | Explain routing as an operations problem, not only a neural layer. | Route selection balances cost, adequacy, residuals, and fallback. |
| III | `readiness-gates-residual-escrow-and-quarantine` | Readiness/residual harness plus Theseus architecture gate | Add quarantine release, residual custody, expired evidence, and fallback cases. | Make readiness gates read like release engineering for intelligence. | Promotion blocked on expired evidence or uncustodied residuals. |
| III | `moecot-runtime-and-multi-core-orchestration` | Theseus/MoECOT report plus routing harness | Import orchestration trace only after public-safe sanitization. | Explain multi-core orchestration through work allocation and receipts. | Trace validates routing and authority boundaries without model-quality claim. |
| III | `personal-compute-hives-and-federated-edge-intelligence` | Theseus operator OS plus external distributed-systems baselines | Add lease, approval, runner, and federation negative controls. | Make the chapter useful to people imagining home and edge compute. | Lease fixture proves bounded compute delegation and revocation. |
| III | `compact-generative-systems-and-residual-honesty` | Compression metrics plus residual ledger | Add compression failure residuals and quality baseline separation. | Explain compactness as accountable loss, not magic. | Fixture records what is compressed, lost, checked, and residualized. |
| III | `generate-verify-repair-compression` | Generate-verify-repair harness | Add repair loop traces with failed verification preservation. | Turn the compression loop into a readable craft process. | Repair is accepted only after verifier passes and failures stay recorded. |
| III | `fast-generation-architectures` | Generation-mode baseline harness plus external inference literature | Add quality-adjusted useful-solution-per-second and negative controls. | Explain speed as useful verified output, not latency alone. | Faster mode cannot promote on latency-only metrics. |
| III | `rankfold-neuralfold-and-artifact-compression` | Artifact compression experiment | Add small public-safe artifact compression benchmark with quality checks. | Show the reader what folded artifacts look like before and after. | Compression ratio and quality/residual metrics are recorded separately. |
| III | `semantic-representation-and-tree-structured-models` | Representation fixtures plus Circle/Coil source lanes | Add tree transform, semantic preservation, and mismatch cases. | Make representation concrete with tree examples and diagrams. | Transform preserves required semantic fields or fails with receipt. |
| III | `resource-economics-and-token-budgets` | Costed-route slice plus resource-budget ledger | Extend budget records to multi-step workflows and displaced costs. | Explain resource economics as finite attention and finite money. | Multi-step budget fixture rejects hidden or displaced cost. |
| III | `simulation-fidelity-and-physical-constraints` | Simulation harness plus external verification baselines | Add fidelity boundary, physical constraint, and invalid extrapolation cases. | Explain simulation as useful only inside named envelopes. | Fixture rejects extrapolation beyond validated fidelity class. |
| III | `mathematical-and-search-substrates` | Circle/Theseus transfer plus search fixtures | Import or define public-safe search/proof-contract trace. | Give readers a clear bridge between math substrate and AI behavior. | Trace separates search legality from performance or intelligence claims. |
| III | `circle-calculus-and-proof-carrying-ai-contracts` | Circle public replay plus Lean consumer gate | Vendor/archive receipt fixture and add negative controls. | Explain proof-carrying contracts as receipts systems can check. | ASI validator accepts valid Circle receipt and rejects malformed ones. |
| III | `coil-attention-cyclic-memory-and-recurrence-contracts` | Circle/Coil fixture plus external memory baselines | Add alias-boundary and recurrence-contract negative controls. | Make cyclic memory intuitive without claiming long-context performance. | Fixture proves structural recurrence boundary, not quality. |
| III | `coilra-multicoil-rope-and-cyclic-mixers` | Circle/Coil RoPE receipt lane | Extend rope certificate replay and structural-not-quality boundaries. | Show what cyclic position evidence can and cannot say. | Receipt validates distinguishability boundary and rejects performance overclaim. |
| IV | `executable-specifications-and-lean-proof-envelope` | Lean proof-depth work plus schema crosswalk | Keep proof adequacy, proof-depth, and protocol crosswalk current. | Teach readers how to read proofs without overstating them. | Proof matrix distinguishes finite-record proof, derived invariant, and executable behavior. |
| IV | `benchmark-ratchets-and-anti-goodhart-evidence` | Benchmark anti-Goodhart harness plus external benchmarks | Add contamination, saturation, and transfer negative controls. | Explain why benchmark gains can become a trap. | Ratchet fixture blocks promotion on contaminated or saturated benchmark. |
| IV | `policy-optimization-and-learning-from-feedback` | Policy-optimization fixtures plus external RLHF/RL literature | Add reward-boundary, verifier reward, and no-reward-as-truth cases. | Explain policy optimization as governance of learning signals. | Policy update cannot treat reward as truth without evidence boundary. |
| IV | `artifact-steward-agents-and-living-project-governance` | Theseus operator OS plus release-record fixtures | Use this as the first curated reader-manuscript candidate. | Make the chapter a practical story about stewarding a living project. | Steward action fixture validates governance, treasury, release, and sunset boundaries. |
| IV | `integrated-reference-architecture` | End-to-end Theseus report plus architecture trace | Build a public-safe thin vertical slice through several layers. | Turn the architecture into a coherent walkthrough. | Trace crosses intent, plan, authority, evidence, and artifact replay without hidden promotion. |
| IV | `project-theseus-as-report-first-implementation-reference` | Theseus import itself | Define and validate the report schema and first public-safe trace. | Explain why reports are implementation evidence only when replayable. | First Theseus report validates and records non-claims. |
| IV | `prototype-roadmap` | Roadmap-to-evidence ledger | Turn roadmap milestones into issue templates and acceptance gates. | Make the path forward feel concrete rather than aspirational. | Each prototype lane has owner, fixture, command, support boundary, and blocker state. |
| IV | `living-book-methodology` | Harness registry plus release/reproducibility records | Surface phase-runner evidence and add no-ledger-sprawl rule. | Explain the living book as a process readers can trust. | Registry runner remains replayable and non-core evidence is visible. |
| IV | `open-research-agenda-and-bibliography-plan` | External review and source-note backlog | Prioritize literature gaps, preprint extractions, and external reviewer tasks. | Close the book with an honest invitation to build and test. | Bibliography agenda ties each open question to source notes, proof targets, or experiments. |

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

### Milestone 9 - External Review, Preprints, And Archiving

Goal: turn the book from a strong public project into a credible research
program.

Tasks:

- Extract one or more focused preprints:
  - living evidence book methodology;
  - proof-carrying claim and support-state discipline;
  - governed self-improvement boundary;
  - Circle proof-carrying AI contracts;
  - Project Theseus report-first implementation evidence.
- Ask at least one external human reviewer to inspect:
  - safety-critical Lean proof scope;
  - support-state language;
  - reader edition clarity;
  - external-SOTA positioning.
- Create GitHub issues for review findings with source links and acceptance
  criteria.
- Add DOI/Zenodo only after an archive exists and `CITATION.cff` names the
  actual DOI.

Acceptance bar:

- review input is recorded as review input, not source evidence;
- preprints do not claim support states stronger than the book records;
- archive metadata points to exact release commits and artifacts.

## Version Targets

| Target | Meaning | Minimum bar |
|---|---|---|
| `v1.1` | Evidence visibility and first deeper proof/report lanes | Non-core evidence ledger visible; five safety-critical Lean upgrade specs started; one public-safe Theseus or Circle replay improvement landed; reader curated pilot initialized or explicitly deferred. |
| `v1.2` | Formal and prototype depth | Safety-critical modules contain nontrivial derived theorems; first public-safe Theseus report validates; Circle consumer gate rejects negative controls; external exceptions reduced or justified. |
| `v1.3` | Human-reader manuscript quality | Curated reader manuscript covers a coherent pilot arc or full Part I; reader HTML remains validated; EPUB/DOCX/PDF blockers have concrete review status; audio script generated from curated prose for reviewed chapters. |
| `v1.x evidence release` | Stronger evidence release without pretending all chapters are proved | Every chapter has an executed evidence lane or explicit no-promotion decision; at least several chapter-adjacent claims have accepted upward transitions; core claims promote only where evidence justifies it. |
| `v2.0` | Public research program | External review, archived release, polished human editions, reproducible Theseus/Circle evidence packs, stronger Lean envelopes, and extracted preprints exist. |

## Suggested Long-Running Goal

Use this wording when it is time to start the next large autonomous work run:

> Advance **The ASI Stack** from the tagged `v1.0.0` living-book release toward a true v1.x evidence-and-reader release by executing `docs/v1_x_beyond_sota_roadmap.md` in order. Preserve release integrity, check prior GitHub Pages failures before each commit, surface the three bounded non-core evidence transitions without promoting chapter core claims, deepen the five safety-critical Lean modules beyond projection-only traceability, create public-safe Project Theseus and Circle replay evidence lanes, assign and execute chapter-specific evidence work across all 54 chapters, replace weak external-SOTA exceptions where source-noted literature exists, graduate human-reader chapters into curated prose when overlays are insufficient, prepare EPUB/PDF/DOCX/audio only after reviewed artifacts exist, run the full local validation gate, update changelog and release-control docs, and never fabricate source content, proof/test results, support-state promotions, or artifact approvals.

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
