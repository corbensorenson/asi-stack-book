# Source Note: Compact Generative Systems

| Field | Value |
|---|---|
| Source ID | `cgs` |
| Source title | Compact Generative Systems: A Unified Theory of Compression, Generation, Control, and Governance |
| Author / release | Corben Sorenson; public release v1.0, May 2026 |
| Ingestion basis | Complete local raw cache at `sources/raw/google_docs/cgs.txt`; section-family fidelity audit completed 2026-07-31 |
| Source status | Conceptual framework, design vocabulary, and research program |
| Evidence boundary | Definitions, heuristic equations, entry criteria, functional ladder, proposed laws and metrics, design template, analogical case studies, reviewer responses, and research agenda. No CGS theorem, benchmark, toolkit, Active Compression Network, agent, controller, organizational intervention, physical system, compression result, safety result, or independent reproduction is present. |

## Thesis

A Compact Generative System (CGS) is a compact structured core that can
reconstruct, predict, generate, control, coordinate, or govern a larger target
through explicit rules, state, residual correction, verification, and an
interface to the governed system. The source asks a stronger question than
“how short is the description?”: **what can the compact description do, what
does it fail to carry, how is that failure repaired, how do we know, and where
did the complexity go?**

The central design object is `(S, R, M, epsilon, V, G)`: seed, rule system,
memory/state, residual/error, verification, and generation/governance
interface. Compactness is honest only when the costs of all six components—and
the decoder, environment, human, correction, fallback, and unknown burden
around them—are counted. A small seed with a giant decoder, literal-heavy
residual, unlimited human verifier, or environment-supplied structure is not a
compact win.

CGS is broad by design but claims disciplined scope through seven entry
criteria and a seven-level functional ladder. Its most durable contribution to
the book is this admission discipline plus hidden-complexity and residual
accounting. Its provisional equations are useful factor inventories, not a
finished mathematical theory or universal scalar ranking.

## Claim Boundary and Intellectual Lineage

The source connects MDL, algorithmic information theory, Solomonoff induction,
compression progress, language modeling as compression, active inference,
cybernetics, equality saturation, vector-symbolic/hyperdimensional systems,
and morphological computation. These are neighboring traditions and design
analogies, not evidence that CGS subsumes them or that their properties
transfer to one architecture.

- MDL supplies model-plus-residual description-length discipline. CGS adds
  explicit rules, persistent state, verification, correction, and governance.
- Cybernetics supplies feedback, regulation, and requisite-variety pressure.
  CGS adds compactness, generative leverage, residual burden, and verification
  accounting.
- Active inference motivates action that changes future uncertainty, but CGS
  does not inherit free-energy guarantees or a complete action objective.
- E-graphs, VSA/HDC, and morphology illustrate different locations for compact
  structure; they do not establish one common representation or benchmark.
- RMI later places CGS inside a benchmark-to-procedure-to-architecture growth
  loop. BBVCA, RankFold, KERC, Precision Contract, and QCSA later supply more
  specific reconstruction, residual, semantic, rate, and consumer contracts.

CGS does not replace MDL, cybernetics, active inference, or algorithmic
information theory; claim to be finished mathematics; apply usefully to every
system; establish compactness as universally superior to scale; make compact
systems automatically interpretable or safe; make governance universally
desirable; solve agents; equate compression with intelligence; make
verification complete; or establish safe recursive improvement.

## Formal Object Model

The candidate is `C = (S, R, M, epsilon, V, G)`. Generation is sketched as
`X_hat = G(R(S, M))`, residual as `epsilon = d(X, X_hat)`, and verification as
an accept/reject/repair decision over target, output, and residual. This useful
sketch hides timing, stochasticity, side effects, observation limits,
consumer-specific discrepancy, evaluator independence, and authority. The book
should treat each as a versioned interface rather than a pure function.

The source's objective minimizes seed, rule, memory, residual, verification,
and governance/interface cost subject to a quality threshold. This is a
conservation principle, not an executable optimization until lengths, units,
population, horizon, threshold, rights, reliability, and cross-unit tradeoffs
are specified. Total burden is later written as seed + rules + memory +
residual + verification + governance. The printed equations omit equality
signs in places; their semantics are preserved without reproducing typography
as proof.

The proposed CGS quality ratio multiplies generative leverage, fidelity, and
governance power, then divides by residual, verification, hidden complexity,
and governance cost. The paper correctly calls it a design compass. It should
not become a scalar leaderboard: mixed units, zero/negative utility, safety
vetoes, uncertainty, and incomparable targets make the aggregation unstable.

## Conceptual Primitives

- **Target system:** artifact, behavior, population, process, organization, or
  class of valid outputs the compact core claims to affect.
- **Seed:** latent, program, law, schema, state, contract, model, protocol,
  morphology, initial condition, architecture, prompt, or policy.
- **Rule system:** decoder, transition, inference, compilation, rewrite,
  simulation, neural, differential, physical, policy, controller, or workflow
  process by which the seed does work.
- **Memory/state:** persistent context required across prediction, generation,
  correction, control, or governance.
- **Residual:** reconstruction error, prediction error, literal exception,
  failed test, anomaly, uncertainty, action failure, unexplained variance,
  override, or unrepresented obligation.
- **Correction mechanism:** storage, update, split, rule revision, exception,
  question, experiment, patch, belief update, fallback, or human review that
  responds to residuals.
- **Verification contract:** exact comparison, hash, proof, test, invariant,
  simulation, calibration, audit, benchmark, red team, or scoped review.
- **Governance interface:** route by which the compact object produces,
  constrains, coordinates, controls, or changes a larger system.
- **Hidden complexity debt:** unpriced decoder, human, environment, training,
  scaffolding, verification-gap, or unknown-residual burden.
- **Active compression:** observe, compress, act, verify, correct, and
  recompress so memory and action can reduce future explanatory or control
  burden without erasing residuals.

## Mechanisms

### Seven entry criteria

A serious CGS must have: (1) a seed/rule/state representation meaningfully
simpler than its target space; (2) an actual reconstruction, prediction,
generation, control, coordination, or governance operation; (3) explicit
unfolding rules; (4) persistent state for dynamic behavior; (5) explicit
residual accounting; (6) a verification route; and (7) full cost accounting.

Compactness may mean bytes, degrees of freedom, rules, parameters, states,
human interventions, or search, but the measure must be declared. A static
description without operation fails criterion 2. A seed without rules is
inert. A dynamic governor without state cannot preserve history. A system that
hides unknowns or exceptions fails residual honesty. Verification can be
partial, but its scope and gaps must be visible.

### Seven-level functional ladder

- Level 0, compact description: summarizes or indexes but need not act.
- Level 1, reconstruction: recreates a target under an exact or lossy contract.
- Level 2, prediction: generalizes prospectively to unseen cases.
- Level 3, generation: produces new valid instances.
- Level 4, control: regulates a process using state, action, and feedback.
- Level 5, governance: coordinates or constrains system evolution.
- Level 6, recursive governance: governs revision of its own compact system.

This is a function taxonomy, not a maturity or safety ladder. Higher levels do
not inherit evidence from lower or establish superiority. Recursive governance
needs protected verification, audit, residual inheritance, staged changes,
rollback/compensation, containment, and authority ceilings because it may
change the objects that define or judge it.

### Seven proposed laws

The Seed and Rule laws state that compact structure becomes generative only
through an unfolding process, so both burdens count. The Memory law makes
persistent state explicit for dynamic generation or governance. The Residual
law treats discrepancies as the interface between model and reality rather
than embarrassment. The Verification law requires testing against the claimed
target. The Governance law distinguishes producing outputs from shaping future
behavior. The Hidden Complexity law denies compactness when burden is exported
to decoder, verifier, environment, operator, training corpus, or residual.

These are design invariants, not proven natural laws. They become scientific
only through operational definitions and discriminating experiments.

### Metric vector

Generative leverage compares target burden with seed + rule + state burden.
Fidelity uses a domain- and consumer-specific discrepancy. Residual burden
prices what remains outside the generator. Verification cost includes verifier
description, runtime, maintenance, and human work. Governance power compares
useful behavior with a competent simpler or ungoverned baseline. Hidden
complexity debt inventories decoder, operator, environment, verification gap,
and unknown residual.

Report this as a vector with units, uncertainty, scope, denominators, vetoes,
and complete lifecycle cost. High leverage cannot compensate for low fidelity;
good reconstruction cannot establish prediction; strong generation cannot
authorize control; and governance utility cannot erase safety, rights, or
critical-tail failure.

### Ten-part design template

Every proposal names target, seed, rule system, memory/state, residual channel,
correction mechanism, verification contract, governance interface, complete
cost, and failure analysis. The template exposes which component is absent and
supports matched comparison with literal storage, direct prediction, ordinary
control, or simpler governance.

### AI and active-compression loop

Weights, activations, embeddings, memories, plans, and policies can each be
viewed as different compact structures, but an LLM is not therefore the whole
CGS. Agentic use adds observation, action, verification, correction,
authority, and residual custody. The source sketches an agent with compact
state, learned rules, memory, residual, verifier, and policy, plus an Active
Compression Network objective that selects memory and action so future
experience becomes easier to explain and govern.

This is a research proposal. Acting to make observations easier to compress
can seek information, but can also simplify the world destructively, avoid
hard cases, manipulate observers, or optimize the verifier. Safe objectives
need protected external obligations, causal and counterfactual checks,
irreversibility accounting, and refusal to treat compressibility as value.

## Interfaces and State Transitions

The canonical Compact Generative Record binds exact target/consumer, seed,
rules, state, generator, residual, correction, verifier, authority, use
envelope, burden ledger, fallback, promotion state, retirement, sources,
evidence, and non-claims. Compression Receipts and Semantic Node Records are
more specific descendants, not replacements.

Candidate outputs move through candidate, verified exact, verified lossy,
repaired exact, literal fallback, or quarantine states under a consumer
contract. A Level 4–6 system additionally needs action/effect receipts and
governed change records. Any generator, verifier, target, discrepancy measure,
consumer, environment, or authority change expires the relevant qualification.

## Evidence, Evaluation, and Falsifiers

The seven case-study families—compression, theories, program synthesis,
e-graphs, AI agents, software/organizations, and morphology—are analogies that
exercise the template. They are not cross-domain empirical evidence for a
unified law. SymLiquid FEP-Net is presented as a mapping of components, not a
locally inspected implementation or result.

A credible campaign compares CGS candidates with strong domain-specific
baselines at matched target information, compute, memory, time, authority,
human effort, and tuning. It measures the metric vector, downstream utility,
failures, complete cost, transfer, and all residual/correction/fallback paths.
It is scoped-falsified when entry criteria cannot be operationalized; hidden
burden erases apparent leverage; residuals dominate seed and rules; fidelity or
utility loses at matched cost; verification is impractical or captured;
governance adds no value; the ladder fails to separate functions; active
compression improves predictability by suppressing relevant complexity; or a
simpler established framework explains and predicts the results equally well.

## Failure Modes and Threats

- Hidden complexity in decoder, verifier, operator, environment, data,
  scaffolding, assumptions, or residuals.
- Residual explosion where exceptions carry most information.
- Overcompression that destroys requisite variety, rare cases, identity,
  causality, or control distinctions.
- Plausible but unverified generation.
- Degenerate governance through proxy optimization, overcontrol, test-passing,
  capture, brittle rules, or unsafe automation.
- Recursive instability, self-amplifying error, verifier loss, hidden residual
  accumulation, irreversible update, and interpretability collapse.
- Category inflation where any summary or model is branded a CGS.
- Scalar quality gaming and cross-unit cost laundering.
- Active compression that changes the environment or observations to make
  failure easier to encode rather than solving the task.
- Analogy laundering across software, physics, organizations, and cognition.

## Book Chapters Supported

- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems and Residual Honesty)
- `fast-generation-architectures` (Fast Generation Architectures)
- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `integrated-reference-architecture` (Integrated Reference Architecture)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Admit CGS candidates only through all seven entry criteria.
- Preserve the seven functional levels while blocking evidence inheritance and
  the implication that recursive governance is inherently mature.
- Report leverage, fidelity, residual, verification, governance, hidden debt,
  and total cost as a vector rather than the provisional scalar ratio.
- Treat the ten-part design template as the minimum proposal interface.
- Add adversarial boundaries to active compression: easier-to-compress futures
  are not necessarily useful, safe, truthful, diverse, or authorized.
- Do not infer compactness, adequacy, compression gain, intelligence,
  interpretability, safety, governance value, or implementation from the paper.

## Section-Family Closure Ledger

| Paper section family | Durable owner | Disposition and boundary |
|---|---|---|
| Abstract and §1 | Compact Generative Systems chapter; this note | Thesis integrated; cross-domain ubiquity remains a research proposition. |
| §2 definition/objective | Chapter Mechanism and new metric section | Tuple and full-cost principle retained; formulas treated as heuristic contracts. |
| §3 non-equivalences | This note; chapter guardrail | Compression/MDL/cybernetics distinctions and non-universal scope retained. |
| §4 entry criteria | Chapter Eligibility subsection | Seven criteria integrated directly. |
| §5 intellectual lineage | This note; external source records | Comparisons retained without novelty or property transfer. |
| §6 ladder | Chapter Eligibility subsection | Levels 0–6 integrated as function classes with no evidence inheritance. |
| §7 proposed laws | This note; chapter invariants | Seven design laws retained and bounded as unproven. |
| §8 metrics | Chapter vector subsection | Six dimensions integrated; provisional scalar rejected as promotion metric. |
| §9 design template | Chapter Interfaces and this note | Ten fields preserved and expanded by canonical record contracts. |
| §10 case studies | This note | Analogies retained; no cross-domain evidence inferred. |
| §11 AI/active compression | Chapter Mechanism; this note; Open Research Agenda | Agent and ACN sketches retained as research objects with adversarial objective risks. |
| §12 failure modes | Chapter Failure modes and this note | Six source failures integrated and expanded. |
| §13 objections | This note | Distinctions, breadth/entry response, novelty boundary, and philosophy-to-science condition retained. |
| §14 research agenda | Open Research Agenda; chapter Mature Target | Formalization, level benchmarks, toolkit, ACN, software, physical, and organizational programs remain open. |
| §§15–16 | This note; chapter summary | Seven claims narrowed; ten non-claims preserved; conclusion adds no evidence. |
| Appendix A | Chapter Interfaces; this note | Specification template integrated. |
| Appendices B–D | This note | Manifesto, public summary, and post introduction treated as rhetoric. |
| References | Appendix H and external inventory | Bibliography requires separate source review and cannot supply automatic support. |

## Open Questions

- Can the seven entry criteria be made operational across domains without
  becoming either vacuous or representation-biased?
- Which units permit honest comparison of description, runtime, human,
  authority, verification, and residual burden without false scalarization?
- Does the ladder predict distinct experimental requirements, or is it mainly
  a useful taxonomy?
- Can hidden complexity debt be estimated prospectively rather than discovered
  only after deployment?
- When does active compression improve epistemic efficiency, and when does it
  create avoidance, homogenization, observer manipulation, or loss of
  requisite variety?
- What protected components make recursive compact governance safer than a
  simpler non-self-modifying system at complete cost?
