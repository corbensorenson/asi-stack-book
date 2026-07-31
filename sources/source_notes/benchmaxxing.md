# Source Note: Benchmaxxing

| Field | Value |
|---|---|
| Source ID | `benchmaxxing` |
| Source title | Benchmaxxing: The Performance Ratchet |
| Author / release | Corben Sorenson; public release v1.0, May 2026 |
| Ingestion basis | Complete local raw cache at `sources/raw/google_docs/benchmaxxing.txt`; section-family fidelity audit completed 2026-07-31 |
| Source status | Conceptual development methodology and benchmark-governance proposal |
| Evidence boundary | Architecture prose, compact formal sketches, benchmark/model ledger templates, examples, research questions, failure mitigations, and a six-phase implementation roadmap. No benchmark registry, model ledger, live or private holdout, contamination audit, benchmark mutation, empirical run, architecture comparison, transfer result, or independent reproduction is present. |

## Thesis

Benchmaxxing treats AI development as a **performance ratchet** rather than a
sequence of leaderboard wins. A manageable system faces a benchmark frontier;
developers preserve complete residuals, test instrument, data, training, and
inference hypotheses; a valid saturated frontier becomes a regression floor;
a harder frontier supplies new pressure; and architecture changes only when a
residual-specific missing-mechanism hypothesis survives cheaper explanations.

The ratchet needs three properties. **Lock-in** preserves capabilities that
were actually established. **Frontier pressure** keeps current instruments
unsaturated and diagnostic. **Escalation discipline** prevents unnecessary
complexity and false architecture conclusions. The governing idea is not that
benchmarks define intelligence. Benchmarks are temporary, claim-scoped pressure
surfaces whose role changes as exposure, model capability, residual value,
noise, and real-world relevance change.

The paper's strongest contribution is the joined distinction among benchmark
saturation, a model-development wall, and architecture limitation. Saturation
is a property of an instrument's remaining information value. A wall is lack
of improvement on an instrument still capable of measuring the target.
Architecture limitation is a causal diagnosis reached only after fair tests of
instrument, data, training, and inference alternatives. A score alone proves
none of the three.

## Claim Boundary and Cross-Paper Relationship

Benchmaxxing overlaps with Ratcheting Modular Intelligence (RMI), Cognitive
Loop Closure, Octopus Router, and the book's later evidence program. These are
related Corben-authored lineages, not independent corroboration.

- Benchmaxxing owns the detailed benchmark lifecycle, saturation signals,
  benchmark portfolio, wall taxonomy, anti-Goodhart controls, benchmark/model
  ledgers, and architecture-escalation rule.
- RMI embeds this benchmark ratchet in a broader pressure-to-structure loop,
  adds proceduralization and bridge-frontier levels, residual custody,
  threshold-decay safeguards, and system/tool/residual ledgers.
- Cognitive Loop Closure owns the trajectory-to-tool compiler and verification
  lifecycle that can become an inference or procedural intervention.
- Octopus Router owns routed specialist topology and lifecycle, one possible
  architecture response to a diagnosed residual.
- The canonical Benchmark Ratchets chapter adds stronger construct validity,
  output binding, selection lineage, evaluator independence, complete cost,
  evidence-state, rights, privacy, safety, and promotion boundaries developed
  after this paper.

The paper references scaling laws, Chinchilla, HELM, METR, Humanity's Last
Exam, SWE-bench, benchmark mutation, Goodhart's law, and label-error work.
Those references motivate the method; they do not establish every historical
or current example by this local note. External sources remain separately
inventoried and passage-reviewed where used in the book.

The paper does not claim that benchmarks perfectly measure intelligence;
higher scores always imply real capability; architecture should never change
early; data can solve every wall; scaling laws suffice; saturation proves
mastery; all benchmarks should be public; one benchmark defines progress;
anti-Goodhart controls eliminate gaming; or benchmark results replace
deployment evidence.

## Formal Object Model

The paper decomposes a developed system as
`M_t = (A_t, theta_t, D_t, I_t)`: architecture/model class, trained parameters,
training and post-training data, and inference procedure including tools,
memory, search, and scaffolding. The benchmark frontier is a set `B_t`, and
performance is a vector `S(M_t, B_t)`, not inherently one scalar.

The paper sketches per-benchmark saturation through a threshold or small
improvement across repeated cycles with overlapping uncertainty. It then writes
suite saturation as the product of per-benchmark flags. That expression is a
compact intuition, not an adequate admission rule: it omits task weights,
critical vetoes, subgroup floors, construct drift, contamination, evaluator
capacity, transfer, and uncertainty dependence. The book should preserve the
signal family while replacing the naive product with a consumer-scoped vector
decision.

A wall is sketched as near-zero change despite interventions on data, training,
and inference. Architecture change is justified when reasonable interventions
under the old architecture remain below an improvement tolerance while the new
architecture clears it. This is useful only prospectively. “Reasonable” needs
frozen budgets, tuning parity, stopping rules, seeds, controls, and skipped-
level justifications; otherwise the new method can receive more engineering,
data, compute, or evaluator access than the old one.

The minimal ratchet rule requires frontier gain greater than `epsilon` and
regression loss below `delta`. The rule is again a skeleton: safety vetoes,
tails, uncertainty, retained utility, calibration, rights, costs, and
irreversible effects cannot be traded away through one aggregate delta.

## Conceptual Primitives

- **Benchmark frontier:** current unsaturated instrument set intended to expose
  meaningful capability residuals.
- **Performance ratchet:** transition that improves a frontier while retaining
  the exact established obligations of prior instruments.
- **Saturation:** loss of useful development gradient due to ceiling,
  clustering, noise, ambiguity, contamination, narrowness, weak transfer,
  Goodhart pressure, or low residual value.
- **Wall:** persistent lack of improvement on a still-valid, unsaturated
  instrument under a prospectively adequate intervention campaign.
- **Residual report:** item-, category-, step-, brittleness-, ambiguity-,
  knowledge-, instruction-, horizon-, tool-, and evaluator-level failure map.
- **Capability narrative:** bounded prose describing population, conditions,
  reliability, tools, horizon, exclusions, and remaining failures rather than
  allowing a score to impersonate a capability.
- **Frontier benchmark:** hard, discriminative pressure surface.
- **Diagnostic benchmark:** instrument designed to distinguish failure causes.
- **Regression benchmark:** former frontier retained to guard a scoped floor.
- **Live benchmark:** refreshed population intended to reduce staleness and
  direct style overfitting.
- **Retired benchmark:** instrument retained for lineage but denied current
  steering or promotion authority.
- **Benchmark ledger:** lifecycle, construct, quality, exposure, transfer,
  cost, refresh, and retirement record for one instrument.
- **Model ledger:** versioned record of `(A, theta, D, I)`, results, residuals,
  floors, costs, safety, and current limiting hypothesis.

## Mechanisms

### Eight-stage ratchet loop

The source begins with the smallest plausible system so failures remain easier
to train, inspect, debug, ablate, compare, and modify. “Smallest” is a
development heuristic, not proof that the target is representable; the target-
capacity gate must still reject an architecture that cannot express the task.

An initial portfolio combines unit, diagnostic, capability, integration,
stress, efficiency, and safety instruments. Data improvement precedes
architecture novelty: coverage, labels, curriculum, negative examples,
synthetic data, filtering, balancing, task formatting, preference data, and
tool demonstrations are tested against a frozen evaluation boundary. Each run
produces residuals rather than only a score.

The wall is then diagnosed through benchmark, data, training, inference, and
architecture interventions. Saturated benchmarks move to a regression suite;
persisting valid residuals motivate escalation; and the next frontier becomes
longer, more realistic, hidden, live, adversarial, multimodal, shifted,
resource-constrained, or safety-sensitive. Prior floors remain attached to the
successor.

### Diagnostic ladder

The original five-level ladder is:

1. audit labels, solvability, prompt clarity, metric alignment,
   contamination, difficulty, breadth, and transfer;
2. improve data coverage, labels, negatives, diversity, curriculum, balance,
   synthetic cases, failure examples, and demonstrations;
3. test loss, optimizer, schedule, post-training, RL, curriculum,
   distillation, regularization, and sampling;
4. test compute, search, tools, retrieval, memory, planning, verification,
   self-consistency, and agent scaffolding; and
5. change architecture through a named missing mechanism such as recurrence,
   hierarchy, modularity, native retrieval/tools, perception, state-space,
   symbolic, planner/verifier, or long-horizon state machinery.

RMI later extends this with proceduralization and bridge-frontier stages. The
book should retain the expanded ladder but attribute the original five levels
correctly. The order is a rebuttable default, not a ritual: a broken instrument
must be repaired before training; a critical hazard can stop the campaign; an
inexpressible target may justify immediate redesign. Every skip needs a reason.

Architecture change becomes a prospective hypothesis: missing mechanism `X`
should improve residual class `B` while preserving regression set `R`. The
comparison freezes accessible information, budgets, evaluator, task identity,
and tuning opportunity or accounts for their differences. A bundled change
cannot establish which component broke the wall.

### Benchmark lifecycle and multi-rate portfolio

Frontier, diagnostic, regression, retired, and live are distinct lifecycle
roles. The paper also layers the portfolio by cadence: fast inner-loop probes,
medium diagnostics, expensive frontiers, live external work, and separate
safety/misuse evaluations. The canonical book expands that set with private
and temporal holdouts, public calibration, contamination review, quarantine,
blocked, and historical states.

Role transitions are governed rather than automatic. Frontier-to-regression
promotion preserves only the construct and conditions actually established.
Retirement remains visible and names whether contamination, noise, narrowness,
ease, misleading incentives, or cost destroyed current value. A live benchmark
needs a sampling frame, rights, versioning, adjudication, and drift controls;
freshness alone does not establish validity.

### Saturation vector

The source provides six useful saturation signals: ceiling performance, model
clustering, noise dominance, weak transfer, contamination risk, and low
residual value. Several should appear together before reclassification. A
benchmark can be hard yet saturated if failures teach nothing, or easy in the
aggregate yet unsaturated for a critical tail. Saturation therefore needs
confidence intervals, subgroup/task-family analysis, evaluator sensitivity,
exposure history, transfer, cost, and a decision about prohibited uses after
role change.

### Anti-Goodhart portfolio

The seven safeguards are rotation across public/private/live/human/adversarial/
real work; private holdouts; semantics-preserving benchmark mutation; plural
accuracy, robustness, calibration, latency, cost, memory, safety, consistency,
transfer, preference, interpretability, and horizon metrics; transfer checks;
contamination audits; and capability narratives.

Mutation must not quietly change the construct or difficulty. Private status
is not permanent—queries, reviewer feedback, tuning, or repeated submissions
consume secrecy. Multi-metric reporting is not license to average away a veto.
A capability narrative is itself bounded by the underlying instrument and must
state failures, not market the score.

### Linked ledgers

The Benchmark Ledger records name, capability/construct, type or lifecycle
role, saturation vector, contamination risk, label/test quality, transfer
evidence, runtime/compute/review cost, refresh date, regression value, and
retirement criteria. The book should add version, population/sampling frame,
evaluator, public-exposure budget, uncertainty, rights, prohibited uses, and
capability narrative.

The Model Ledger records version, architecture, data, training process,
inference process, full portfolio scores, residual map, regression state, cost
profile, safety profile, and next wall. The book should add checkpoint/runtime
identity, raw-output binding, seed and retry lineage, baselines, selections and
failures, and exact benchmark-ledger version. Joining the two ledgers prevents
a result from floating free of the system and instrument that produced it.

## Interfaces and State Transitions

The core interface is a Benchmark Instrument Lease joined to a Model/System
Ledger and raw Run Records. It supplies bounded measurement input to Evidence
States, Readiness, Safety Cases, Routing, Training, Policy Optimization,
Recursive Improvement, Resource Economics, and the Living Book. It does not
itself authorize support movement or deployment.

Instrument state can move among candidate, diagnostic, frontier, public
calibration, private/temporal holdout, live, regression floor, contamination
review, quarantine, blocked, retired, and historical. The graph is not
monotonic: evaluator change, exposure, task drift, label defects, cost, or
consumer change can narrow, quarantine, or retire an instrument. Reopening a
retired instrument requires a new version and justification, not silent reuse.

System state advances only when the frontier gain, inherited floors, safety
profile, complete cost, uncertainty, negative cases, and decision authority
all satisfy their separate contracts. Saturation changes the instrument's
role; it does not promote the model's claim by itself.

## Evidence, Evaluation, and Falsifiers

The source is a conceptual framework. Its examples—coding benchmarks, the
MMLU-to-GPQA-to-HLE progression, and increasing long-horizon task length—are
illustrative. They do not establish that the sequence is monotonic, that every
later benchmark measures a strict superset, or that one architecture advanced
because of the proposed ladder.

A faithful implementation needs prospective benchmark and model ledgers; raw
runs; public, hidden/temporal, mutated, transfer, safety, and regression sets;
strong matched interventions at each ladder level; repeated seeds;
uncertainty; complete selection and failure denominators; exact cost; and an
independent evaluator. It should test whether residual diagnoses predict which
intervention succeeds better than strong baselines or expert judgment.

The program is weakened or falsified in a scoped regime if:

- saturation labels are unstable across seeds, evaluator versions, or modest
  population changes;
- low residual value fails to predict that a new frontier is more informative;
- benchmark-to-regression transitions do not preserve useful capabilities;
- the diagnostic ladder repeatedly attributes walls to the wrong component;
- architecture changes succeed equally without the named residual mechanism;
- cheaper interventions were under-tuned or under-resourced relative to the
  architecture candidate;
- hidden, live, mutation, or transfer checks fail despite public gains;
- capability narratives overpredict real workflow performance;
- the multi-rate portfolio costs more than its decision value;
- safety, subgroup, tail, or retained-capability regressions are hidden by the
  aggregate ratchet thresholds; or
- retirement and contamination decisions can be bypassed by renaming an
  instrument or model.

## Failure Modes and Threats

- Benchmark gaming and style overfitting without capability transfer.
- Leaderboard addiction and score-to-capability marketing.
- Premature architecture escalation and novelty bias.
- Benchmark nostalgia or stagnation after saturation.
- Regression blindness and forgotten prior floors.
- Noisy labels, flawed tests, ambiguous prompts, weak metrics, or evaluator
  ceilings mistaken for model failure.
- Public/private boundary erosion through tuning, repeated submissions, or
  review feedback.
- Benchmark mutation that changes the target rather than testing robustness.
- Multi-metric scalarization that compensates for safety or critical-tail
  failure.
- Inadequate target capacity, making a model look bad on an impossible output
  contract.
- Bundled intervention confounding and unequal engineering or compute.
- Retry, checkpoint, or selection laundering.
- Capability progress outrunning safety and misuse evaluation.
- Retired instruments reappearing without inherited defects and exposure.

## Book Chapters Supported

- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `capability-replacement-and-rollback` (Capability Replacement and Rollback)
- `recursive-self-improvement-boundaries` (Recursive Self-Improvement Boundaries)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `replaceable-cognitive-substrates-beyond-transformer-monoculture` (Replaceable Cognitive Substrates: Beyond Transformer Monoculture)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `capability-thresholds-and-deployment-commitments` (Capability Thresholds and Deployment Commitments)
- `safety-cases-and-structured-assurance` (Safety Cases and Structured Assurance)
- `adversarial-evaluation-sandbagging-and-training-time-deception` (Adversarial Evaluation, Sandbagging, and Training-Time Deception)
- `open-ended-improvement-engines` (Open-Ended Improvement Engines)
- `fast-generation-architectures` (Fast Generation Architectures)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `integrated-reference-architecture` (Integrated Reference Architecture)
- `prototype-roadmap` (Prototype Roadmap)
- `living-book-methodology` (Living Book Methodology)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)
- `dangerous-capability-domains-and-misuse-uplift` (Dangerous Capability Domains and Misuse Uplift)

## Claims To Add Or Update

- Keep saturation, wall, and architecture limitation as separate decisions.
- Represent saturation as a vector of ceiling, separation, uncertainty, noise,
  exposure, transfer, and residual-value signals, not one threshold.
- Freeze `(architecture, parameters, data, inference)` and intervention budgets
  so wall diagnosis can identify a causal component.
- Treat the benchmark portfolio as a multi-rate control system with governed
  role transitions and explicit retirement.
- Join benchmark and model ledgers; add a bounded capability narrative to every
  material score.
- Preserve the expanded RMI ladder while attributing the original five-level
  instrument/data/training/inference/architecture ladder to Benchmaxxing.
- Do not infer a benchmark pass, model improvement, architecture need, transfer,
  safety, readiness, or support transition from this paper.

## Section-Family Closure Ledger

| Paper section family | Durable owner | Disposition and boundary |
|---|---|---|
| Abstract and §1 | Benchmark Ratchets problem and mechanism; this note | Pressure-to-regression thesis integrated; current examples remain source-reported context. |
| §2 definition, ratchet, saturation, wall | Benchmark Ratchets new saturation/wall subsection | Distinctions and three ratchet properties integrated; formulas remain heuristic skeletons. |
| §3 eight-stage method | Benchmark Ratchets mechanism; source note | Small-system observability, portfolio, residuals, diagnosis, lock-in, and frontier expansion retained. |
| §4 formal model | Benchmark Ratchets saturation/wall subsection; note | `(A, theta, D, I)`, vector scores, saturation, wall, and ratchet sketches preserved with missing-assumption critique. |
| §5 diagnostic ladder | Benchmark Ratchets residual-specific intervention section | Original five levels attributed; expanded RMI ladder remains canonical. |
| §6 lifecycle | Benchmark Ratchets portfolio/lifecycle sections | Frontier, diagnostic, regression, retired, and live roles integrated and expanded. |
| §7 anti-Goodhart safeguards | Benchmark Ratchets mechanism/invariants | Rotation, private holdouts, mutation, plural metrics, transfer, contamination, and narratives retained. |
| §8 portfolio design | Benchmark Ratchets multi-rate portfolio | Cadence and role matrix integrated; safety remains separately vetoed. |
| §9 saturation signals | Benchmark Ratchets saturation/wall subsection | Six signals integrated as a vector; no universal 95% threshold adopted. |
| §10 wall diagnosis | Benchmark Ratchets intervention section and note | Symptoms/treatments retained as hypotheses, not validated classifiers. |
| §11 architecture discipline | Benchmark Ratchets intervention and saturation sections | Prospective residual-specific mechanism claim and matched comparison boundary integrated. |
| §12 protocol and ledgers | Benchmark Ratchets Interfaces | Four-set protocol generalized; benchmark/model ledger join and ratchet rule integrated. |
| §13 beyond accuracy | Benchmark Ratchets lifecycle/invariants | Plural accuracy, reliability, calibration, robustness, resource, autonomy, transfer, safety, and human-usefulness axes retained. |
| §§14–16 examples | Source note; external source records | Coding, knowledge, and time-horizon ladders retained as illustrations only. |
| §17 failure modes | Benchmark Ratchets Failure modes | Eight source failures integrated and expanded with current evidence threats. |
| §18 research agenda | Open Research Agenda; Benchmark Ratchets argument-exit campaign | Saturation, frontier construction, diagnosis, transfer, mutation, cost, and safety questions remain open obligations. |
| §19 implementation roadmap | Prototype Roadmap; Benchmark Ratchets MVI | Six phases preserved as implementation ordering; none is reported complete by this source. |
| §§20–21 claims, non-claims, conclusion | This note; chapter guardrail and summary | Claims narrowed to design propositions; all ten non-claims retained. |
| Appendices A–C | Benchmark Ratchets mechanism and Interfaces; schema research | Checklist and ledger fields integrated; templates are not executable records. |
| Appendices D–E | This note | Public summary and manifesto treated as rhetoric, not distinct evidence or mechanisms. |
| References | External source inventory and Appendix H | Use only through separately reviewed external records; bibliography is not automatic support. |

## Open Questions

- Can independent evaluators reliably distinguish saturation from an
  instrument defect and from a system wall before outcome inspection?
- What minimum tuning and budget parity makes a lower-level intervention an
  adequate attempt rather than a straw baseline?
- How should residual information value be measured without rewarding a
  benchmark for producing endless but irrelevant errors?
- Which lifecycle transitions should be reversible, and what exposure or
  contamination permanently prevents return to private/frontier status?
- How should capability narratives be scored for calibration against later
  live-task outcomes?
- Does the diagnostic ladder improve research efficiency and causal diagnosis
  over strong expert practice after its governance cost is included?
