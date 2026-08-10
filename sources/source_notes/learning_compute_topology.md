# Source Note: Learning–Compute Topology

| Field | Value |
|---|---|
| Source ID | `learning_compute_topology` |
| Source title | *Learning–Compute Topology: Formalizing the Causal Organization of Adaptive Systems* |
| Author / date | Corben Sorenson; August 9, 2026; version 1.0 |
| Ingestion date | 2026-08-09 |
| Supplied archive | `Learning_Compute_Topology_Paper_v1_0.zip`; SHA-256 `c99490686f8aab5372efb2048d3d447a6cfc4e2c611eb0e7fb25791a5b574d12`; 5,232,467 bytes |
| Canonical manuscript | `sources/raw/corben_papers/learning_compute_topology/package_v1_0/paper/Learning_Compute_Topology.md`; SHA-256 `4fd869f01f4c0782e6e2f1d657b6c84e87ced82e652126aae395123a04fac712`; 129,274 bytes |
| Presentation copy | `sources/raw/corben_papers/learning_compute_topology/package_v1_0/paper/Learning_Compute_Topology.docx`; SHA-256 `ded442614e647cfbc885c83f52edf5b530aebccada503e588e654bf17b300501` |
| Preparation report | `supplement/lct_prep_v0_1/PREP_REPORT.md`; SHA-256 `22500dccfbb8369abfecc0cf7826030ec6547b82fb7ec72ae1b82548c4e46f92` |
| Tree-shaking memo | `supplement/lct_prep_v0_1/tree_shaking/TREE_SHAKING_MEMO.md`; SHA-256 `9db0b71598bb39037bbb2f3a5b4ae31e2051329cf64104fe196a45ab8424105d` |
| Package integrity | All 127 files named by `MANIFEST_SHA256.txt` matched their recorded SHA-256 digests. Archive paths were checked before extraction; no absolute or parent-traversal member was present. |
| Executable check | `python3 -m unittest discover -s tests -v` in `supplement/lct_prep_v0_1` passed 11 of 11 tests on 2026-08-09. This checks only the bounded reference package. |
| Ingestion basis | Complete local archive: paper, 13 figures, bibliography, claims map, reproducibility guide, formal specifications, executable examples, normalized outputs, schedules, tests, toy/analytical data, quality reports, and auxiliary design memos. |

## Thesis

Model architecture describes how a model computes a function. Execution
topology describes how a fixed computation is placed, scheduled, sharded, and
communicated. Neither fully describes the causal organization of adaptation.
The paper introduces **Learning–Compute Topology (LCT)** for the missing layer:
the persistent adaptive identities in a learning system and the typed routes by
which evidence, judgement, credit, state, artifacts, control, and authority
change those identities over time.

Its central distinction is:

```text
learning-process topology
    -- semantic compiler --> execution topology
    -- placement/runtime --> physical compute topology
    -- receipts/leakage --> learning-process controller
```

The same accelerators can realize a single data-parallel adaptive identity, a
federation of locally persistent identities, a population search, a
branch–validate–integrate process, or a modular composition. Conversely, one
declared learning process can have several physical realizations with different
work, span, communication, staleness, energy, failure, and information-loss
profiles. Treating all of these as merely “serial” or “parallel” erases the
distinctions that determine what can be discovered, evaluated, retained,
integrated, rolled back, or destroyed.

The book-level implication is architectural: substrate replaceability must
extend above neural blocks and below governance. An ASI stack should be able to
change not only weights, modules, and routes but also the topology of its
learning process, while keeping semantic contracts, authority, provenance,
resource accounting, and rollback explicit.

## Claim Boundary and Status

The package uses five materially different evidence labels and the book must
preserve them:

1. **Proved under a stated model.** Seven propositions establish bounded
   representation and information constraints. They are not universal theorems
   about all learning systems.
2. **Implemented in a bounded prototype.** LCT-IR parsing, finite validation,
   normalization, abstract compilation, scheduling, trace simulation, and nine
   executable encodings are present. This is not a neural-training framework.
3. **Scoped manual comparison.** A 30-mechanism coverage matrix and a
   19-framework capability matrix show discriminative reach within the coded
   sample. They are not proofs of literature completeness or global novelty.
4. **Analytical or toy illustration.** Six phase diagrams demonstrate how
   regime hypotheses can be expressed. They are not fitted frontier-model
   results.
5. **Hypothesized or conjectured.** Adaptive causal refinement, integration
   forests, knowledge placement, salvage, evaluator ecologies,
   topology-conditioned scaling, morphology laws, and ABVI require competent
   empirical tests.

The source does **not** establish a universal canonical representation, an
optimal topology, a complete primitive set, practical benefit on real neural
training, a safety guarantee, causal identifiability without assumptions,
superior scaling, autonomous topology control, state-of-the-art performance,
AGI, or ASI.

## Conceptual Primitives and Distinctions

- **Adaptive state** includes any persistent state modified by learning:
  weights, optimizer state, learned memory, curricula, evaluators, archives,
  controller policy, routing state, or learned tools. It is wider than model
  parameters.
- **Adaptive identity** is a versioned state-bearing entity that can diverge,
  persist, and affect later behavior. The identity, divergence, persistence,
  and consequence tests prevent a transient worker replica from being
  miscounted as an independent learner.
- **Evidence** is observed information; **judgement** evaluates evidence;
  **credit** assigns adaptive responsibility; **adaptation** changes persistent
  state. A reward, gradient, and parameter update are not interchangeable.
- **Fork** creates alternative descendant identities. **Decomposition** creates
  specialized parts that remain jointly composed. This separates exploration
  lineages from modular architecture.
- **Integration** is typed: selection, parameter/state merge, gradient
  aggregation, distillation, ensemble, modular composition, synchronization,
  archive, transfer, or retirement have different semantics and failure modes.
- **Resolution contract** states what is considered an identity, event,
  interface, observable, cost, and hidden state at a chosen scale.
- **Template topology** declares what could exist; **active topology** records
  what currently exists; **trace topology** records what happened;
  **counterfactual rewrite space** records permitted changes.
- **Multiplex semantic topology** admits different partially overlapping graphs
  for evidence, judgement, credit, adaptive state, artifacts, control, and
  authority. One unlabeled graph is usually insufficient.
- **Learning Causal Normal Form (LCNF)** exposes typed causal roles so systems
  with similar graph silhouettes but different learning semantics can be
  compared.
- **Realization leakage** is a semantic or statistical change introduced while
  compiling a learning process onto hardware: staleness, compression,
  quantization, dropped messages, numerical order, partial failures, or
  scheduler-dependent selection.

## Mechanisms

The formal learning-process object is a typed, open, stochastic, dynamically
rewritable hypergraph with stores and interfaces, event hyperedges, store and
port types, state spaces, deterministic or stochastic transition kernels,
conflict, permitted rewrite rules, cost, authority/provenance, observables, and
a resolution contract. Hyperedges allow one event to consume and produce
several typed stores without pretending the interaction is pairwise.

LCT-IR separates nine store classes: `adaptive`, `evidence`, `judgement`,
`credit`, `artifact`, `resource`, `control`, `authority`, and `static`. Its core
operator vocabulary includes instantiate, observe, evaluate, assign-credit,
update, fork, aggregate, synchronize, select, merge, distill, compose,
transfer, archive, restore, retire, route, allocate, rewire, checkpoint, emit,
and pure computation. The paper specifies `decompose` and `externalize` as v0.2
additions and adds reversibility and retained-knowledge-destination
declarations; these are not fully demonstrated by the v0.1 reference compiler.
The validator enforces explicit adaptive versions,
producers, identity creation, integration operators, delayed feedback,
held-out-evidence use, authority for sensitive writes, and declared compute
guarantees.

LCNF normalization performs a bounded sequence: select a resolution contract;
expand hidden adaptive state; make evidence, judgement, and credit paths
explicit; split generic integration into a typed operator; expose lifecycle and
feedback; collapse only interface-sufficient subgraphs; canonicalize names and
ordering; and emit a provenance-bearing normal form. Its equivalence hierarchy
keeps structural, lineage, trace, stochastic, behavioral, learning, execution,
resource, deployment, and authority equivalence distinct.

The semantic compiler maps an LCT program to execution operations and then to
physical placement. A **semantic firewall** prevents the compute planner from
silently changing identity, evaluation, credit, integration, retention, or
authority semantics. Semantics-preserving process superoptimization may change
schedule or placement within the contract. Topology synthesis deliberately
changes learning semantics and therefore requires a new contract and
evaluation.

The paper then derives a measurement vocabulary:

- causal, adaptive, epistemic, commitment, evaluator, and deployment widths;
- effective breadth rather than raw branch count;
- learning bandwidth across evidence, judgement, credit, update, and
  integration channels;
- integration retention;
- topological regret from choosing the wrong process organization;
- dimensionless control coordinates for communication, heterogeneity,
  evaluator strength, compatibility, integration capacity, and reversibility.

The retained-learning thesis is a capacity-matched pipeline. Discovery,
evaluation, and integration capacities form successive semantic cuts, so
increasing branch count alone cannot overcome a weak evaluator or lossy
integrator. This motivates causal-identity refinement, typed synchronization,
higher-order integration forests, commitment annealing, knowledge placement,
salvage-before-retirement, and diverse anchored evaluator ecologies.

The second-pass review recovered several ideas that the first chapter draft had
compressed too aggressively. The core paper supplies causally identifiable
topology interventions, topology-conditioned scaling, the morphology
conjecture, and stratified reflexive control. The tree-shaking memo separately
extends the design space with joint Candidate–Evaluator–Integrator allocation,
semantic compute placement, topology portfolios with stateful migration,
topology distillation, a topology atlas and learned topology prior, and
proof-carrying topology rewrites. The latter set is retained as a lower-
confidence research program: it is not part of the tested v0.1 compiler and
must not be reported as a result of the formal propositions.

The chapter now also preserves the paper's six-axis scientific object
(topology, operational geometry, dynamics, semantics, schedule, and substrate),
four process views (template, active, realized trace, and counterfactual rewrite
space), A–E conformance ladder, ten-way equivalence hierarchy, and proposed
dimensionless control coordinates. These details matter because each blocks a
specific false substitution: connectivity for dynamics, template for history,
parsing for synthesis, task behavior for lineage or authority, and a formula
for a calibrated control signal.

## Interfaces, Artifacts, and State Machines

The canonical artifacts are an LCT-IR program, resolution contract, typed store
and operator declarations, authority and provenance records, rewrite policy,
active-topology snapshot, trace, normalized LCNF projection, equivalence claim,
compiler contract, physical schedule, realization-leakage receipt, cost record,
validation bundle, archive record, and topology-controller decision.

The topology lifecycle is not a single train/deploy transition. Adaptive
identities may be instantiated, forked, updated, synchronized, evaluated,
selected, merged, distilled, composed, transferred, archived, restored, or
retired. Integration can remain reversible through an archive or modular
composition before progressing toward more destructive distillation or merge.
Topology rewrites require authority and should preserve their triggering
evidence, alternatives, predicted benefit, cost, validation, counterfactual,
and rollback path.

The proposed **Adaptive Branch–Validate–Integrate (ABVI)** topology has a stable
base, localized branch controller, candidate identities, designed
differentiation, evaluator allocation, validation bundles, typed integration
planner, shadow branches, archive, and topology-regret monitor. It branches only
when uncertainty, novelty, incompatibility, or expected option value justifies
the cost; assigns evaluator effort to candidate uncertainty and impact; and
chooses selection, merge, distillation, composition, archive, or retirement by
compatibility and deployment constraints.

## Assumptions, Invariants, and Conditional Results

1. **Series–parallel obstruction.** Finite serial and parallel composition does
   not represent every finite causal order; the proof uses the standard
   four-element N-shaped obstruction. This establishes incompleteness of that
   vocabulary, not completeness of LCT.
2. **Fork option-capacity result.** Under the stated conditional-independence
   model, copying one state into several descendants creates option capacity but
   no conditional information. Diversity requires differentiated evidence,
   stochasticity, objectives, environments, or constraints.
3. **Bounded representation theorem.** A finite, bounded, explicit-state
   learning class admits trace-faithful LCT encoding. Hidden state, unbounded
   creation, continuous-time processes, and inaccessible environment dynamics
   remain outside the theorem as stated.
4. **Exact coarse-graining.** A subgraph can be replaced exactly when its
   interface is sufficient for downstream observables under the stated
   conditional-independence condition. Otherwise coarse-graining is lossy and
   must declare what is lost.
5. **Evaluator-information bound.** Candidate selection error is lower-bounded
   by a Fano-style relation between candidate identity and evaluator
   observation. It is not a claim that one particular evaluator is optimal.
6. **Integration-capacity bound.** Exact retention of independently varying
   branch capabilities requires sufficient integration output capacity. A
   fixed-capacity integrator cannot losslessly preserve arbitrary independent
   discoveries.
7. **Semantic-cut bound.** In a staged Markov pipeline with no side channel,
   retained information is bounded by the weakest discovery, evaluation, or
   integration cut. Real systems with side channels require a richer graph.

The package preserves adaptive-version uniqueness, typed producer/consumer
compatibility, explicit identity creation, explicit integration semantics,
versioned feedback, protected held-out evidence, topology-change authority,
and declared realization guarantees as validator invariants.

## Algorithms and Implementation Program

The supplement contains a Python package with an IR loader, type checker,
normalizer, compiler, scheduler, simulator, CLI, JSON schema, EBNF grammar,
LCNF specification, ABVI specification, proposition document, terminology,
coverage and novelty matrices, nine executable encodings, normalized outputs,
compiled schedules, tests, and phase-diagram data.

The bounded reference pipeline is:

```text
LCT-IR document
-> schema and semantic validation
-> LCNF normalization
-> abstract operator compilation
-> dependency scheduling
-> trace simulation
-> normalized IR, schedule, trace, and diagnostic receipts
```

The package reports bounded conformance at levels A–C, with selected checks
from D; it does not implement E-level synthesis. It also lacks a neural
backend, distributed runtime, compiler correctness proof, online controller,
learned topology search, production authority system, and real hardware cost
model.

The experimental program correctly separates two questions that are often
confounded: hold learning topology constant while changing physical compute,
and hold compute constant while changing learning topology. Further experiments
compare identical graph silhouettes with different semantics, measure effective
breadth, scale evaluator channels, test higher-order integration, vary adaptive
identity resolution, match semantic bottlenecks, place knowledge, salvage
retired branches, compare synchronization layers, and test reversible
integration under distribution shift.

## Evidence

The complete package contains 42 references, 13 manuscript figures, two
tables, seven formal propositions, a 30-family manual coverage matrix, a
19-framework novelty-capability matrix, 9 executable canonical examples,
11 passing unit tests, normalized outputs, abstract schedules, six
toy/analytical phase studies, and quality/audit receipts. The checksum manifest
verified all 127 named package files.

The strongest evidence is structural rather than performance-based:

- the propositions establish limited mathematical boundaries under explicit
  assumptions;
- the implementation demonstrates that the proposed IR can represent,
  validate, normalize, and schedule a bounded set of examples;
- the coverage matrix shows the vocabulary distinguishes many familiar
  mechanisms in the hand-coded sample;
- the phase diagrams make regime hypotheses concrete enough to falsify.

None of these establishes that LCT improves a real learning system. The paper's
own claim-and-evidence map is therefore imported as an evidence-state boundary,
not merely as supporting material.

## Evaluation, Falsifiers, and Competing Baselines

The book should retain the paper's seven framework-level falsifiers:

- **primitive-set failure:** important adaptive behavior cannot be represented
  without arbitrary opaque escape hatches;
- **canonicality failure:** normalization is unstable or analyst-dependent;
- **equivalence failure:** systems declared equivalent differ on protected
  traces or outcomes;
- **cost-model failure:** compiled costs fail to predict relevant physical
  behavior;
- **predictive failure:** topology metrics do not explain or predict outcomes
  beyond standard task, model, optimizer, and hardware variables;
- **generative failure:** the formalism cannot produce useful organizations not
  already obvious from named algorithms;
- **controller failure:** adaptive rewrites cost more, destabilize more, or
  improve less than fixed competent baselines.

Competent comparisons include standard data-parallel training, local SGD,
federated averaging, population-based training, evolutionary strategies,
branch–train–merge, ensembles, model soups, distillation, mixture-of-experts,
modular composition, league training, POET/MAP-Elites-style populations,
fixed-topology ABVI ablations, conventional distributed IRs, and ordinary
workflow DAGs. Fair experiments must match total accelerator time, evaluator
queries, communication, storage, wall time, model calls, data access, tuning,
and human review. Raw branch count is not a valid compute match.

## Failure Modes

- Counting replicas or correlated descendants as independent learning breadth.
- Confusing data parallelism with multiple adaptive identities.
- Treating rewards, losses, gradients, votes, and validation certificates as
  one generic edge.
- Hiding merge, selection, distillation, composition, synchronization, archive,
  and retirement behind a generic “combine” node.
- Allowing the hardware planner to change learning semantics without a new
  contract.
- Branching without differentiated evidence, objectives, environments, or
  stochasticity, producing expensive copies rather than discoveries.
- Scaling candidates while leaving evaluation or integration as the bottleneck.
- Premature irreversible integration that destroys option value.
- Archive growth without revival, retention, privacy, or deletion policy.
- Resolution contracts chosen after results to manufacture desired identities
  or causal stories.
- Controller reward hacking, topology thrashing, oscillatory split/merge
  behavior, or local cost optimization that harms retained learning.
- Treating a neat normal form as the true causal model despite hidden state or
  inadequate observables.

## Threats, Misuse, and Governance Costs

Topology creates attack surfaces that model-centric governance can miss:

- **Sybil breadth:** many nominal branches disguise one correlated source of
  evidence or control;
- **evaluator monoculture:** shared weaknesses let diverse-looking candidates
  pass through one proxy bottleneck;
- **merge-order and higher-order attacks:** individually acceptable branches
  become harmful only under a particular integration order or combination;
- **provenance laundering:** state or artifacts cross identities while losing
  lineage and rights constraints;
- **branch starvation and controller capture:** resource allocation prevents
  alternatives from becoming competitive;
- **archive erasure and rollback denial:** destructive integration removes the
  evidence and state required to reverse a change;
- **held-out leakage:** evaluation evidence becomes an adaptation channel;
- **reflexive escalation:** a controller rewrites the evaluator, authority, or
  controller that constrains it.

Mitigation requires stratified authority, independent evaluator anchors,
correlation-aware breadth, provenance-preserving transformations, immutable
decision and trace receipts, budgeted experimentation, archive/deletion policy,
bounded rewrite leases, oscillation limits, canaries, and rollback. These add
storage, evaluator, compute, latency, and human-governance costs that must be
reported with capability results.

## Book Chapters Supported

| Chapter | Distinct transfer | Source locus | Boundary |
|---|---|---|---|
| `learning-compute-topology-and-adaptive-process-architecture` | Owns the four-topology distinction, adaptive identity, multiplex semantics, LCT-IR, LCNF, bounded propositions, semantic compiler firewall, metrics, derived process designs, ABVI, and falsification program. | Sections 1–19; Appendices A–E; supplement | New chapter remains `argument`; bounded formal and executable artifacts do not establish empirical usefulness. |
| `governed-model-training-distributed-optimization-and-scaling` | Separates data/execution parallelism from adaptive plurality; adds semantic compilation, realization leakage, and matched process-vs-compute experiments. | Sections 2, 8–9, 15 | Does not show better optimizer or distributed-training performance. |
| `replaceable-cognitive-substrates-beyond-transformer-monoculture` | Extends substrate replacement from model blocks to learning-process organizations and their compiler contracts. | Sections 2.3, 8, 11, 18 | LCT is a process formalism, not a replacement neural architecture. |
| `routing-heads-and-specialist-cores` | Distinguishes token/task routing from evidence, judgement, credit, state, control, and authority routing. | Sections 2.4, 4, 5.5, 11.3 | Does not validate a learned router or specialist architecture. |
| `policy-optimization-and-learning-from-feedback` | Separates evaluator topology from credit topology and exposes evaluator-information bottlenecks. | Sections 4.3, 7.5, 10, 11.8 | Does not supply a reward model or policy-improvement result. |
| `data-engines-continual-learning-and-unlearning` | Adds adaptive-identity lineage, archive/restore/retire, reversible integration, knowledge placement, and erasure boundaries. | Sections 4, 11.2, 11.6–11.7, 11.9, 16.6 | Behavioral forgetting, influence removal, privacy erasure, and storage deletion remain distinct and untested. |
| `open-ended-improvement-engines` | Adds topology-conditioned search, higher-order integration, adaptive identity resolution, salvage, ABVI, and morphology hypotheses. | Sections 11–12, 15 | No open-ended improvement or recursive self-improvement result. |
| `resource-economics-and-token-budgets` | Adds topology-aware accounting for evaluation, communication, storage, integration, work/span, and option value. | Sections 8.3, 10, 15.3 | Toy cost models do not predict production economics. |
| `multi-agent-dynamics-collective-intelligence-and-systemic-risk` | Separates many agents from many adaptive identities and adds lineage, conflict, higher-order compatibility, and evaluator ecology. | Sections 4.2, 4.7–4.8, 5.5, 11.4, 11.8 | Does not establish cooperation, equilibrium, or anti-collusion results. |
| `adversarial-evaluation-sandbagging-and-training-time-deception` | Adds evaluator-channel capacity, monoculture risk, semantic-cut attacks, Sybil breadth, and held-out leakage. | Sections 7.5, 7.7, 11.8, 16 | Information bounds do not guarantee robust evaluation. |
| `integrated-reference-architecture` | Inserts a governed learning-process compiler/control plane between training policy and execution infrastructure. | Sections 8, 12–13, 16 | This is an interface addition, not an integrated deployment result. |

## Claims To Add Or Update

- Add a chapter-level argument claim that an architecture capable of changing
  only weights or neural blocks is not yet architecturally self-improving; it
  also needs a governed way to represent, compare, compile, test, and roll back
  changes to the organization of learning.
- Add the narrower formal claim that serial and parallel composition are not
  causally complete for finite partial orders, with the exact N-obstruction
  scope.
- Add the distinction that forking increases option capacity but does not by
  itself increase conditional information.
- Add the weakest-semantic-cut argument: retained learning is limited by
  discovery, evaluator, and integration bottlenecks, subject to the staged
  no-side-channel assumptions.
- Update distributed-training prose so accelerator or worker multiplicity is
  never used as a proxy for adaptive plurality.
- Update routing prose so the routed object and semantic edge type are always
  named.
- Update continual-learning prose with reversible integration and explicit
  archive, restore, retirement, provenance, and deletion contracts.
- Update open-ended-improvement prose with topology synthesis as a distinct
  action from semantics-preserving process optimization.
- Add realization-leakage receipts to the integrated architecture and resource
  accounting.

## Cross-Paper Synthesis and Tensions

- **Stable Capability Fields and QCSA.** Stable interfaces can name capabilities
  while LCT names the changing adaptive process that creates, qualifies, and
  replaces their implementations. LCT should not dissolve the stable external
  contract into a mutable topology.
- **Reflexive Router and Octopus Router.** These papers motivate dynamic routing;
  LCT clarifies that routing evidence, judgement, credit, state, control, and
  authority are different operations. A router that treats them identically is
  under-typed.
- **TreeLLM and Portia Synapse.** Branch lineage, archive, validation, and
  integration become explicit LCT identities and edges. The synthesis avoids
  importing tree metaphors as evidence that branching helps.
- **Relational Dimension Compiler.** Higher-order integration hyperrelations
  connect naturally to relational arity. LCT owns adaptive process causality;
  RDC owns typed relational representation and compilation. Neither should
  annex the other.
- **Regret Engine.** Topological regret concerns the cost of the chosen learning
  organization; governed counterfactual regret concerns decision-time-fair
  alternatives for actions and policies. They may share ledgers but must retain
  distinct comparators and authorities.
- **Precision Contract.** LCT realization contracts need explicit numerical,
  approximation, staleness, compression, and equivalence tolerances rather than
  a generic “semantics preserving” label.
- **VCM and context systems.** Learned memory is adaptive state, while context
  caches can be evidence or artifacts. Misclassifying one as the other hides
  update and deletion obligations.
- **Theseus and the integrated stack.** LCT supplies a semantic process plane
  above the execution planner. Theseus can compile and govern it only after the
  topology contract, evidence state, authority, and rollback conditions are
  explicit.

## Section-Family Coverage

| Source family | Disposition |
|---|---|
| Status, introduction, contributions, non-claims | New chapter framing and claim boundary. |
| Serial/parallel distinctions, model vs process architecture, multiplex graphs | New chapter core; distributed-training and routing upgrades. |
| Related work and novelty boundary | New chapter prior-art boundary; bibliography remains external-source leads, not inherited support. |
| Ontology and terminology | New chapter definitions; glossary candidates; routing, continual-learning, and multi-agent upgrades. |
| Formal LCT object, typed hyperedges, stores, operators, rules, conformance | New chapter formal substrate and executable-status section. |
| LCNF, equivalence, coarse-graining, examples | New chapter comparison method and falsification boundary. |
| Seven propositions and theorem program | New chapter bounded-results table; proof backlog retains unproved extensions. |
| Learning-to-compute realization, leakage, firewall, superoptimization/synthesis | New chapter and integrated-architecture/distributed-training/resource upgrades. |
| Canonical mechanism encodings and coverage study | New chapter comparison table; manual-study limit retained. |
| Width, breadth, bandwidth, retention, regret, control coordinates | New chapter metrics; resource and evaluation upgrades. |
| Eleven derived consequences | New chapter design space; targeted upgrades to continual learning, open-endedness, routing, evaluation, and multi-agent dynamics. |
| ABVI | New chapter reference architecture, explicitly hypothetical. |
| Reference implementation and compiler | New chapter executable vertical slice; exact 11-test receipt and limitations retained. |
| Analytical/toy phase diagrams | New chapter hypothesis illustrations; no empirical promotion. |
| Experiments, budget accounting, baselines, falsifiers | New chapter argument-exit program and roadmap work. |
| Safety, authority, attack surfaces | New chapter plus adversarial-evaluation and integrated-governance upgrades. |
| Limitations, discussion, conclusion | New chapter non-claims and research handoff. |
| Glossary and operator appendix | Source note, chapter terminology, and public original-paper library. |
| Claims/evidence map, citation files, reproducibility guide, license, checksums | Provenance panel, source boundaries, public paper library, and package receipt. |
| LCT-IR/LCNF/ABVI specs, grammar, schema, code, examples, tests, schedules | New chapter implementation section and future governed executable artifact intake. |
| Coverage/novelty matrices | New chapter scoped comparison; independent coding remains open. |
| Tree-shaking memo | Derived-idea integration and explicit rejection of redundant labels. |
| Quality reports and visual QA | Custody context only; they do not validate scientific claims. |

### Second-pass completeness audit

| Previously compressed item | Reader-facing disposition after audit | Evidence boundary |
|---|---|---|
| Six-axis process description and four temporal views | Added beside the four-topology distinction. | Definitions only. |
| v0.2 `decompose` / `externalize`, reversibility, knowledge destination | Added to LCT-IR with an explicit v0.1 implementation boundary. | Specified, not fully compiled. |
| Conformance A–E | Added as a graded capability table. | Package is bounded A–C plus selected D checks. |
| Ten equivalence relations | Restored in the LCNF section. | A declared comparison vocabulary, not verified equivalence. |
| Dimensionless control coordinates | Added with the decision question for each coordinate. | Proposed estimators; no calibrated controller. |
| Causally identifiable topology experiments | Added to the derived-design section. | Experimental method, not a causal result. |
| Candidate–Evaluator–Integrator allocation | Added as a supplement-derived active-design hypothesis. | Tree-shaking memo; unimplemented. |
| Semantic compute placement | Added with matched fault-injection tests. | Tree-shaking memo; unimplemented. |
| Topology-conditioned scaling and morphology | Added as a falsifiable frontier and morphology conjecture. | No fitted scaling law. |
| Portfolio migration, topology distillation, atlas/prior, proof-carrying rewrites | Added as a lower-confidence long-horizon program. | Supplemental concepts, not paper results. |
| Stratified reflexive control | Added with levels 0–3 and slower authority at higher levels. | Governance design, not a safety guarantee. |
| Six phase studies | Added as a table of regime questions and missing natural evidence. | Toy or analytical values only. |
| Twelve proposed experiments | Preserved as four preregistered experiment families. | Research program only. |

Every substantive family terminates in chapter prose, an adjacent-chapter
upgrade, a preserved source boundary, or a named research obligation. No family
is left only in the inventory.

## Open Questions

- Can independent annotators normalize the same natural learning system to
  equivalent LCNF without excessive discretion?
- Which minimal primitives survive adversarial examples and genuinely new
  learning mechanisms?
- Can realization leakage be measured well enough to predict when hardware
  mapping changes the scientific conclusion?
- Do topology variables explain outcomes after controlling for model,
  optimizer, data, evaluator, tuning, and total resources?
- When is adaptive identity refinement worth its statistical and systems cost?
- Can evaluator diversity increase information without merely multiplying
  correlated proxies?
- Which integration operators preserve complementary capability under fixed
  deployment budgets and distribution shift?
- Can ABVI beat fixed competent baselines on preregistered multimodal regimes
  without hidden evaluator or tuning advantages?
- How should archives satisfy rollback, privacy, retention, rights, storage,
  and unlearning obligations simultaneously?
- Can a topology controller improve process organization without reward
  hacking, oscillation, authority escalation, or unsafe self-rewrite?
