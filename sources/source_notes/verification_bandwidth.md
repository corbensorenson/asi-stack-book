# Source Note: Verification Bandwidth in Bounded Contexts

| Field | Value |
|---|---|
| Source ID | `verification_bandwidth` |
| Source title | Verification Bandwidth in Bounded Contexts: The Geometry of Mutual Constraint in Large Language Models |
| Source version | Version 1.0 public release |
| Ingestion date | 2026-06-24; complete section-family audit 2026-07-31 |
| Source URL | https://docs.google.com/document/d/1T34n1Ya6_joaAD8ZxygOpiEuNzEVj3G8_nf0xZuFL2U |
| Ingestion basis | All 1,522 words in `sources/raw/google_docs/verification_bandwidth.txt` were inspected; raw text is not published. |
| Controlling manuscript owner | `verification-bandwidth-and-context-adequacy` |

## Thesis

### Claim boundary

The paper proposes a useful engineering distinction: a model can have enough
tokens available to continue generating while lacking enough task-relevant
capacity, representation fidelity, or checking work to verify the constraints
that matter to a claim. It names semantic units, an effective verification
workspace, pairwise grinding, dominant-component pressure, transitive decay,
an interface-versus-verification tradeoff, and a synthetic contradiction-rate
experiment.

Those constructs are a research hypothesis and design vocabulary, not four
proved laws of artificial cognition. The source does not measure an actual
model, define an observable estimator for effective verification workspace,
show that dense joint attention is necessary or sufficient for verification,
prove that every lossy representation loses task-relevant constraints, or
establish universal quadratic and linear complexity classes. The book may use
the source to motivate a prospective obligation-to-capacity contract. It may
not cite the paper as proof of a physical context limit, monotonic coherence
decay, RAG inadequacy, a uniform optimal decomposition, or model cognition.

## Mechanisms

### Complete source model

### Generation and verification are different workloads

The introduction separates autoregressive continuation from relational
checking. A sequence may remain fluent while a variable, premise, requirement,
story fact, or authority constraint introduced earlier no longer constrains the
answer. This is the paper's most durable idea: nominal context availability is
not the same as verified causal use of the relevant material. The book expands
that distinction into separate states for availability, admission, fidelity,
local checking, obligation coverage, evaluator competence, adequacy, claim
support, and release.

### Semantic units and effective verification workspace

The paper decomposes a work into semantic units and defines an effective
verification workspace as the material that can participate in one dense
comparison. These are useful abstractions if they remain claim-relative. A
semantic unit is not inherently a chapter or token span; it can be a premise,
definition, source passage, state transition, counterexample, requirement, or
boundary condition. Likewise, effective workspace cannot be read directly
from the advertised context length. It depends on the representation, task,
position, retrieval and compression path, model, inference policy, tools,
checking method, and evaluator.

The source's displayed coherence expression is not a valid general metric as
written. Nonempty intersection between constraint sets is neither necessary
nor sufficient for noncontradiction, and no estimator or calibration is
provided. The manuscript therefore uses explicit obligations and dispositions
instead of importing the formula.

### Pairwise grinding and the two-body proposal

Pairwise grinding means bringing two units into a sufficiently rich joint
checking operation. The proposed two-body inequality says that full token
representations of both units must fit in the effective workspace. This is a
helpful worst-case admission test for a declared full-representation method,
but it is not a universal necessity theorem. Verification can sometimes use
lossless canonicalization, sufficient statistics, symbolic constraints,
external tools, repeated passes, sparse access, or property-specific proofs.
Conversely, fitting both units into one attention pass does not establish that
the model noticed, understood, or tested their interaction.

The appeal to source coding does not prove that every lossy compression drops
constraint-relevant information. Loss is distribution- and task-relative: a
representation can discard many source bits while preserving everything
needed for a particular property. The correct operational requirement is to
name the protected distinctions, compression path, consumer, property, and
falsification tests, then expose residual loss.

### Dominant-component pressure

Under the paper's full-representation assumption, a large unit leaves less
space for another unit. This is a real scheduling risk: one long document,
trace, summary, or generated draft can monopolize a packet and crowd out the
small decisive premise or counterexample. The resulting engineering controls
are size budgets, protected evidence slots, explicit omission records,
distractor tests, selective expansion, decomposition, and escalation.

The claimed conclusion that units should tend toward one half of the
workspace does not follow generally. Optimal partitioning depends on the
interaction graph, constraint density, access pattern, redundancy, proof
method, model behavior, and cost. The book retains dominant-component pressure
as a threat model and rejects uniform partitioning as an established optimum.

### Transitive decay

The paper warns that checking `u1` against `u2` and `u2` against `u3` does not
guarantee that `u1` is compatible with `u3`. This is durable as an obligation-
graph rule: transitive coverage must be justified rather than assumed, and
boundary interactions or higher-order constraints remain explicit residuals.

The data-processing argument is not a proof that contradiction error grows
monotonically with chapter distance. An LLM computation is not automatically
the Markov chain assumed in the derivation; later access can revisit earlier
tokens; embeddings are not necessarily successive summaries in the stated
sense; information and task error are different quantities; and redundancy,
tools, or explicit checks can repair errors. The monotonic law and inequality
therefore remain falsifiable hypotheses, not manuscript facts.

### Interface-versus-verification tradeoff

The source says flat all-pair checking costs `O(n^2)`, whereas hierarchy can
reduce work by checking summaries at a fidelity cost. The book retains this as
a declared worst-case model when every pair is an obligation. It does not make
the bound universal. Sparse interaction graphs, modular invariants, typed
interfaces, property decomposition, incremental certificates, and proof reuse
can reduce the obligation set without relying only on lossy summaries. Any
such reduction must name its clusters, interfaces, boundary checks,
assumptions, omitted interactions, and residual risk. Hierarchy is a schedule,
not an adequacy certificate.

### Constraint Satisfaction Test

The proposed experiment compares sequential generation with a final direct
reintroduction of the first and last units and measures logical contradiction
rate. It is a useful seed but not an executable protocol yet. A serious study
must operationalize effective workspace, prevent answer and template leakage,
vary unit size, dependency distance, position, distractors, interaction order,
constraint type, representation, retrieval, tool access, model family,
inference budget, and random seeds, and separate detection from repair. It
needs answer-only, long-context, direct retrieval, graph/hierarchical
retrieval, compression, explicit checker, symbolic-tool, and matched-compute
baselines. Metrics should include obligation recall, contradiction detection,
false contradiction, repair correctness, abstention, latency, tokens, memory,
evaluator error, useful throughput, and tail behavior—not only one aggregate
contradiction rate.

The paper's control condition is internally unclear: it asks the combined
units to exceed an unspecified hidden-state capacity while fitting within
effective workspace. Hidden-state capacity is not a directly controllable
per-example quantity, and memorization or leakage is not prevented by length
alone. Dataset lineage, held-out templates, contamination probes, and causal
ablations are required.

### Coherency horizon and RAG

The coherency horizon is usefully interpreted as the point where the current
verification plan can no longer satisfy its declared obligations with the
available resources. At that boundary the system can retrieve, expand, split,
narrow, use a different verifier, ask for authority or resources, abstain, or
retain residuals. It is not a single model constant.

RAG introduces retrieval, ranking, chunking, provenance, and use failures, but
it does not necessarily replace source units with only a lossy vector: an
index can retrieve exact text. The source's blanket characterization is too
strong. The manuscript separates retrieval success, packet admission,
representation fidelity, causal use, and claim verification rather than
treating RAG as either a solution or a disproof.

## Interfaces and artifacts retained

- A claim-specific semantic-unit and obligation graph.
- The actual packet, omitted frontier, transformations, compression path, and
  protected distinctions used by the verifier.
- A prospective budget over context, calls, tools, solvers, compute, latency,
  privacy exposure, and reviewer capacity.
- Explicit pairwise or higher-order obligations where justified, plus named
  decomposition and boundary checks where not all pairs matter.
- Attempt dispositions for passed, failed, contradicted, disputed, unknown,
  infeasible, blocked, and unattempted work.
- Evaluator identity and dependency information.
- A residual and escalation record when the current plan crosses its
  coherency horizon.
- Causal ablations that remove, corrupt, compress, relocate, or reintroduce
  decisive units while holding the rest of the workflow fixed.

## Failure Modes

- Long-context theater: counting loaded tokens as verified constraints.
- Fluency substitution: measuring readability or answer confidence instead of
  contradictions and obligation coverage.
- Hero-unit monopolization and small-decisive-unit neglect.
- Summary laundering: treating a compressed representation as if no relevant
  distinction could have been lost.
- Transitivity laundering: assuming local edge checks establish global or
  higher-order consistency.
- Decomposition laundering: deleting cross-boundary obligations to make the
  workload appear affordable.
- Attention sufficiency: assuming co-location in a window means causal use.
- Retrieval sufficiency: assuming a retrieved passage was correct, complete,
  noticed, or adequate for the claim.
- Evaluator monoculture and self-confirming model agreement.
- Compute-confounded comparisons between direct checking and baseline routes.
- Synthetic-task leakage, trivial templates, unmeasured false alarms, and an
  evaluator that shares the same blind spot as the candidate.
- Universalizing a method-specific capacity model into a law of cognition.

## Section-family closure ledger

| Source section | Disposition | Canonical owner and limit |
|---|---|---|
| Abstract and introduction, lines 5–13 | Integrated | `verification-bandwidth-and-context-adequacy` separates generation, availability, causal use, and verification. It does not claim a measured cognition law. |
| Definitions, lines 15–30 | Integrated with correction | The chapter owns semantic units, claim-specific obligations, and adequacy states. The source's coherence formula is not imported. |
| Two-body limit, lines 33–42 | Retained as a bounded hypothesis | Full-representation joint checking is one conservative mode. Compression loss is property-relative, and fit is neither necessary nor sufficient for verification. |
| Dominant-component suppression, lines 43–51 | Integrated as a threat and test | The chapter records dominant-distractor failure and capacity pressure. Uniform half-window partitioning is rejected as a general optimum. |
| Transitive decay, lines 52–61 | Integrated as an obligation rule; theorem rejected | Boundary and higher-order checks remain visible. The DPI argument does not establish monotonic contradiction growth for LLMs. |
| Interface-verification tradeoff, lines 62–72 | Integrated as a worst-case cost model | All-pair counts apply only when every pair is a declared obligation. Typed interfaces, sparse graphs, and certificates are alternatives requiring their own checks. |
| Empirical test, lines 74–85 | Research obligation | The chapter's mature target and Codex test plan preserve a stronger matched, held-out, causal protocol. No model contradiction-rate result exists. |
| Coherency horizon and RAG, lines 87–89 | Integrated with correction | The horizon becomes a plan-relative escalation boundary. RAG may retrieve exact source text and is evaluated across retrieval, fidelity, use, and verification separately. |
| Conclusion, lines 90–92 | Bounded | Verification can bottleneck complex work, but the paper does not establish that it is always the limiting factor or that context length equals verification scope. |
| References, lines 94–99 | Source-discovery leads only | The citations are not inherited as independently reviewed evidence through this paper. The book maintains separate primary-source records where used. |

## Cross-paper relationships

- Virtual Context Memory owns packet construction, transformations, omission,
  certificates, and admission; Verification Bandwidth owns whether a declared
  claim-specific checking plan is adequate.
- TreeLLM, Spider Synapse, Portia Synapse, GraphRAG, HippoRAG, and RAPTOR offer
  retrieval and organization candidates; none turns traversal into truth.
- Kernel English and BBVCA offer compressed representations; each must expose
  protected distinctions, residuals, round-trip limits, and source fallback.
- Spinoza and Claim Ledgers own proposition identity, evidence, contradiction,
  and support transitions. An adequacy record cannot promote its own claim.
- Scalable Oversight owns evaluator governance and independence; this paper
  supplies the capacity pressure that those evaluators must disclose.

## Book Chapters Supported

- `verification-bandwidth-and-context-adequacy` is the controlling owner.
- `virtual-context-abi`, `evidence-states-and-claim-discipline`,
  `spinoza-verification-and-proof-carrying-claims`,
  `compact-generative-systems-and-residual-honesty`,
  `fast-generation-architectures`,
  `policy-optimization-and-learning-from-feedback`,
  `governed-deliberation-and-test-time-scaling`, and
  `scalable-oversight-and-adversarial-ai-control` own adjacent interfaces.
- `open-research-agenda-and-bibliography-plan` owns the unexecuted empirical
  program.

## Claims To Add Or Update

- Preserve the generation-versus-verification distinction and the
  obligation-to-capacity contract already written in the dedicated chapter.
- Keep all-pair cost, transitive decay, dominant-unit effects, and effective
  workspace as bounded hypotheses or threat models rather than proved laws.
- Require property-relative compression tests, direct-use ablations, matched
  baselines, and evaluator-dependence records before stronger claims.
- No additional chapter prose is required after this audit.

## Open Questions

- Can a task-relative effective verification workspace be estimated without
  circularly using the same model as both subject and judge?
- Which sparse interaction graphs and typed interfaces avoid unnecessary
  all-pair checks while retaining every material boundary obligation?
- Under what workloads does direct reintroduction improve contradiction
  detection after controlling for added tokens, position, and compute?
- How should false contradiction, missed help, and useful throughput change
  the stopping rule at the coherency horizon?

## Manuscript decision

No new chapter and no additional duplicate prose are warranted. The dedicated
Verification Bandwidth chapter already contains the complete useful model and
goes materially beyond the paper with obligation graphs, mode ceilings,
evaluator dependence, causal-use tests, residual accounting, expiry,
escalation, matched baselines, and explicit non-claims. The source note now
closes every paper section, corrects the overclaimed theorem language, and
records the experiment that would be needed to move beyond argument.

## Evidence state

`argument`. The repository has authored schema, fixture, capacity, route, and
mutation checks for the book's contract. Those artifacts do not test an LLM's
verification bandwidth, the paper's four theorem claims, a natural-task
contradiction rate, evaluator adequacy, useful advantage, safety, or transfer.
