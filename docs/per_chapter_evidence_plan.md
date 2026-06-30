# Per-Chapter Evidence Plan

Last updated: 2026-06-30

This file is the 50-chapter evidence-lane backlog for **The ASI Stack**. It is
an execution menu, not a checklist. It names plausible next evidence moves so a
future goal can choose a small number of high-payoff lanes without inventing a
fresh plan from scratch.

Execution rule: a v1.x cycle should execute at most 5-8 chapter lanes. The
remaining lanes stay `planned, not executed`; they must not receive synthetic
fixtures, pass/fail status, or support-state pressure merely for coverage.
The active cycle selection is recorded in
`docs/v1_x_active_evidence_cycle.md`: seven lanes are selected and the other
forty-three remain planned-only.

Selection criteria:

- real public-safe replay or measurement is achievable;
- the chapter is load-bearing for many later claims;
- the lane can include a negative control or rejection case;
- the evidence reduces self-sourcing through external review, external
  literature, public Theseus/Circle artifacts, or CI-verifiable archived
  fixtures;
- the lane names the chapter's current or needed external-grounding status:
  source-noted comparator, candidate backlog, or explicit exception;
- the lane names the strongest intended proof/evidence path for its
  load-bearing argument: Lean, Project Theseus, Circle, source-noted literature,
  external review, or explicit no-promotion blocker;
- the work can produce a narrow evidence transition without implying broad ASI,
  model-quality, safety, benchmark, transfer, or deployment claims.

Support-state rule: this plan does not promote any chapter core claim above
`argument`. A support-state change requires an accepted evidence-transition
record.

External-grounding rule: before adding new outside citations to chapter prose,
mine the chapter's linked Corben papers for bibliographies, footnotes, named
systems, algorithms, standards, and adjacent terms. Accepted third-party sources
must enter through `sources/source_inventory.json`, receive a source note, and
then appear in generated Appendix H. External citation can contextualize an
argument, but it is not a Lean proof, Project Theseus replay, Circle receipt, or
support-state transition by itself.

| Part | Chapter | Primary evidence lane | Formal/prototype work | Human-reader focus | Acceptance bar before support-state change |
|---|---|---|---|---|---|
| I | `asi-is-a-stack-not-a-model` | Lean plus architecture trace | Deepen `StackBoundaries` with multi-layer handoff states and authority rejection cases. | Open the book with a concrete system story instead of taxonomy. | A state-machine proof plus a replayed handoff fixture; no broad ASI claim. |
| I | `the-efficient-asi-hypothesis` | Cost/resource harness plus external routing literature | Extend the costed-route slice beyond toy routes and tie it to budget ledgers. | Explain efficiency as "do only the expensive work that earns its cost." | Public fixture with baseline, negative control, and repeated run record. |
| I | `system-boundaries-and-authority` | Lean authority transitions | Connect authority ceiling, denial receipt, and confused-deputy harnesses. | Make authority boundaries feel like operating-system permissions. | Derived theorem or harness showing escalation blocked across handoff paths. |
| I | `failure-modes-of-ungoverned-intelligence` | Red-team scenarios plus Lean invariant violation | Add composed failure cases spanning authority, context, and evaluator capture. | Use a small number of memorable failure stories. | Replayed red-team fixture routes residuals to claims/tests/proofs. |
| I | `evidence-states-and-claim-discipline` | Claim ledger harness and evidence-transition ledger | Surface non-core transitions and enforce no-promotion decisions. | Turn support states into plain-language reader promises. | Appendix C/sibling ledger validates transitions without core-claim promotion. |
| I | `human-intent-as-a-formal-input` | Lean intent contract plus command-contract fixtures | Add intent ambiguity, delegation, and approval cases. | Ground formal intent in everyday instruction failures. | Intent fixture rejects underspecified or authority-widening execution. |
| I | `constitutional-alignment-substrate` | Safety-critical Lean plus agency-right harness | Deepen protected predicate, migration, self-modification, review, appeal, high-impact approval, and interruption semantics. | Explain a constitution as a change-control surface that keeps dignity concrete through usable refusal, audit, appeal, rollback, and correction paths. | Nontrivial theorem plus harness case showing protected predicates and high-impact human-control paths survive transition or block action. |
| I | `moral-uncertainty-and-value-conflict` | Safety-critical Lean plus value-conflict and governance-right harnesses | Deepen uncertainty residuals, dissent, revisit conditions, fork/exit/audit preservation, redaction, and appeal obligations. | Show value conflict as engineering for unresolved disagreement with usable governance handles. | High-stakes unresolved conflict cannot become unconditional promotion, and proof or fixture shows redaction/fork still preserves audit and safety obligations. |
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
| III | `routing-heads-and-specialist-cores` | Routing harness plus MoE literature and folded MoECOT runtime crosswalk | Extend route-quality, specialist-readiness, and public-safe orchestration-record fixtures without treating MoECOT source reports as reproduced runtime evidence. | Explain routing as an operations problem, not only a neural layer, and show the MoECOT Runtime Crosswalk as a receipt shape rather than a standalone proof. | Route selection balances cost, adequacy, residuals, fallback, source-state partitions, and replay blockers without model-quality or runtime-execution claims. |
| III | `readiness-gates-residual-escrow-and-quarantine` | Readiness/residual harness plus Theseus architecture gate | Add quarantine release, residual custody, expired evidence, and fallback cases. | Make readiness gates read like release engineering for intelligence. | Promotion blocked on expired evidence or uncustodied residuals. |
| III | `personal-compute-hives-and-federated-edge-intelligence` | Theseus operator OS plus external distributed-systems baselines | Add lease, approval, runner, and federation negative controls. | Make the chapter useful to people imagining home and edge compute. | Lease fixture proves bounded compute delegation and revocation. |
| III | `compact-generative-systems-and-residual-honesty` | Compression metrics, residual ledger, and generate/verify/repair harness | Add compression failure residuals, repair loop traces, failed-verification preservation, and quality baseline separation. | Explain compactness and repair as accountable loss, not magic. | Fixture records what is compressed, lost, checked, repaired, residualized, or rejected before any compactness claim promotes. |
| III | `fast-generation-architectures` | Generation-mode baseline harness plus external inference literature | Add quality-adjusted useful-solution-per-second and negative controls. | Explain speed as useful verified output, not latency alone. | Faster mode cannot promote on latency-only metrics. |
| III | `rankfold-neuralfold-and-artifact-compression` | Artifact compression experiment | Add small public-safe artifact compression benchmark with quality checks. | Show the reader what folded artifacts look like before and after. | Compression ratio and quality/residual metrics are recorded separately. |
| III | `semantic-representation-and-tree-structured-models` | Representation fixtures plus Circle/Coil source lanes | Add tree transform, semantic preservation, and mismatch cases. | Make representation concrete with tree examples and diagrams. | Transform preserves required semantic fields or fails with receipt. |
| III | `resource-economics-and-token-budgets` | Costed-route slice, resource-budget ledger, folded simulation harness, and external verification baselines | Extend budget records to multi-step workflows, displaced costs, fidelity boundaries, physical constraints, and invalid extrapolation cases. | Explain resource economics as finite attention, finite money, and claim transport through named simulation envelopes. | Multi-step budget fixture rejects hidden or displaced cost, and simulation fixture rejects extrapolation beyond validated fidelity class. |
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
