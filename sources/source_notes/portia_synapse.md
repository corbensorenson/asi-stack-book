# Source Note: PortiaSynapse v1.1.0

| Field | Value |
|---|---|
| Source ID | `portia_synapse` |
| Source title | PortiaSynapse: A Cognitive Spider Architecture for DKL Navigation |
| Source date | 2024-12-23 (source metadata) |
| Ingestion date | Authenticated Google Drive discovery and complete section-family audit completed 2026-07-31 |
| Source version / URL | v1.1.0; https://drive.google.com/file/d/1ZnsE0rAC8YdiMFeo3N4kWEU8keTthF9v |
| Ingestion basis | Complete 6,906-word Markdown cached at `sources/raw/google_drive/portia_synapse_whitepaper.md`; raw text is not published. |

## Source boundary

PortiaSynapse is a direct TreeLLM successor artifact. It replaces the failed
SpiderSynapse while preserving the Dynamic Knowledge Lattice, 512-dimensional
`RichContext`, 128-bit coordinate prediction, typed-edge prediction,
working-memory, confidence, reasoning-chain, and drop-in Synapse interface.
The separate `spider_synapse` paper is the negative predecessor and is not
independent support for Portia.

The paper claims an approximately 2,535-line implementation, 24 passing tests,
full training integration, and several completed milestones. This repository
does not contain or execute that implementation. The document also contradicts
itself: the top says 24 tests, Appendix C enumerates 22, and an earlier
milestone says 15; “implemented and tested” coexists with an unfinished full
integration milestone and unrun comparative benchmarks. The implementation
and tests are therefore source-reported. Passing unit or one-step training
tests would establish neither learning, calibration, multi-hop reasoning,
route quality, DKL utility, nor benchmark transfer.

The document date is internally suspect. It says 2024-12-23 while the failed
Spider paper says December 23, 2025 and the surrounding TreeLLM lineage is
dated late 2025. This note preserves the source metadata without resolving the
chronology.

## Thesis

Portia's durable thesis is methodological: begin with the simplest
interface-compatible learner that can demonstrate a real learning signal;
admit coordinate, edge, memory, confidence, and branching mechanisms in
phases; instrument each component; stop on unhealthy gradients, activations,
or plateaus; and preserve an executable fallback.

The proposed model accepts a five-part context—coordinate bits, content
embedding, edge distribution, neighbor summary, and modulation—and applies a
gated Scout transform, a Focus/working-memory block, two residual refinement
blocks, and coordinate, edge, and confidence heads. It is intended to replace
the approximately 500K-parameter DKL-aware baseline while staying simpler than
the failed four-hypothesis Spider architecture.

The architecture is a useful candidate, but the paper does not demonstrate
that its biological analogy, attention, memory, refinement, confidence, or
larger parameter count causes better outcomes.

## Mechanisms

### Stable replacement boundary

Portia retains the `RichContext -> {coordinate, edge type, confidence}`
interface and proposes a `SynapseCore`, `TrainableSynapse`,
`ChainTrainable`, and `DiagnosticSynapse` trait split plus a name-based
registry. This is the strongest architectural contribution. Candidate
routers can be swapped without changing DKL storage or Navigator consumers,
and an unavailable Portia route falls back to `generate_smart()`.

The interface still needs model/version identity, graph and ontology epoch,
context schema, memory/session identity, route policy, calibration population,
authority ceiling, cost envelope, output residuals, and rollback. A
drop-in type match does not establish behavioral substitutability.

### Context contract

The five `RichContext` fields make graph state visible to the learner:
128 coordinate bits, 128 content features, 64 edge-distribution features, 128
neighbor-summary features, and 64 modulation features. Each field needs a
versioned construction rule, missingness state, normalization, provenance,
rights, temporal scope, and leakage audit. Bit or vector dimensions are not
semantics by themselves. Neighbor averages can erase rare but decisive
relations, edge distributions can expose gold structure, and modulation
heuristics can encode answer shortcuts.

### Scout, Focus, refinement, and heads

The Scout is a pre-norm gated MLP with a residual connection. It selects
features; it does not emit or verify a multi-hop route plan, so “scout before
commit” remains an analogy until a prospective path artifact and committed-hop
comparison exist.

The Focus block claims self-attention over context dimensions and gated
working memory. In the displayed pseudocode, a `[batch, 512]` tensor is
projected to Q/K/V and multiplied by the transpose. Unless reshaped, that
operation attends across batch examples, not feature dimensions. It risks
cross-example leakage and makes behavior batch-composition dependent. This is
an implementation question, not proof that the hidden code has the same bug,
but it is a mandatory audit target.

The `RwLock<Tensor>` makes shared memory mutation data-race controlled; it
does not make memory semantically thread-safe. Request, conversation, user,
batch, train/eval, reset, checkpoint, and rollback boundaries need explicit
ownership. A global mutable tensor can leak one request into another, serialize
throughput, or let evaluation inherit training or prior-query state.

Two residual FFN blocks provide additional fixed compute. They do not perform
trial and error in the ordinary sense because no action is executed and no new
observation arrives between blocks. The book calls this fixed refinement until
an ablation shows an iterative causal signature.

Coordinate, edge, and confidence heads are appropriately separate outputs.
They still need joint consistency: a predicted edge must exist and be legal
from the current object, the coordinate must identify or retrieve an allowed
target, and confidence must refer to a named event such as exact route success,
task success, or safe abstention.

## The Portia correction ladder

The paper's phase order is sound in spirit:

1. coordinate-only sanity check;
2. add typed-edge prediction;
3. add Focus and working memory for multi-hop tasks;
4. add confidence calibration;
5. run the complete pipeline and comparative suite.

This becomes stronger when phases advance by held-out evidence rather than
fixed percentages of training. “Finite loss,” “one step works,” or “outputs
are in [0,1]” are smoke checks, not admission gates. Each phase freezes the
prior baseline, adds one component, runs repeated seeds and held-out graph
partitions, requires a minimum effect with uncertainty, retains regressions,
and rolls back if the component does not improve its intended axis after total
cost.

The diagnostics—per-layer gradient norms, activation statistics, separate
coordinate/edge/confidence losses, and calibration bins—are useful. Hardcoded
thresholds such as `1e-7`, `100`, 500 steps, 0.01 activation deviation,
or 1,000-step loss decline are initial alarms, not universal health criteria.
They must be calibrated by dtype, optimizer, scale, layer type, task, and known
healthy/failed runs.

## Metric and training corrections

### Coordinate accuracy

The paper reports or targets bit-level accuracy on 128-bit HLSH coordinates.
Bit accuracy is not exact coordinate accuracy, semantic-neighbor accuracy, or
route success. An 85% average bit score can still identify no exact node, and
class imbalance or shared prefixes can make a trivial predictor look strong.
Evaluation needs exact-id accuracy, top-k retrieval, semantic distance under a
validated HLSH metric, edge-valid route accuracy, complete-path success,
downstream answer utility, abstention, and calibration for each event.

Binary cross-entropy over coordinate bits also assumes that independent bit
errors form a meaningful semantic loss. That conflicts with the claim that
hierarchical prefixes and graph locality carry structured meaning. Compare
bitwise BCE with contrastive, metric, candidate-ranking, and typed
edge-conditioned objectives under the same graph and compute.

### Edge and confidence labels

Reasoning chains built from random walks, known Q&A paths, and definition
edges can leak the desired route through edge distributions or graph
construction. Split by object families, relations, connected components,
sources, temporal epochs, and path templates; keep answer nodes and aliases
from crossing partitions; include several valid paths, false short paths,
missing edges, contradictions, and abstention cases.

Confidence trained by mean squared error against “was correct” is useful only
if correctness is defined at the consumer event. Calibrating against per-bit
accuracy can look excellent while exact route or answer success is poor.
Report reliability diagrams, ECE/MCE plus proper scores, selective-risk and
coverage curves, subgroup calibration, drift, and calibration after routing
or fallback. Confidence may request review; it cannot grant truth or write
authority.

### Claims about the Spider failure

The source attributes the predecessor's plateau to gradient dilution,
hypothesis collapse, post-norm, label smoothing, batch size, and premature
complexity. Hypothesis collapse and the failed training trace are observations
reported by the sources. “Each of twelve paths gets one twelfth of the
learning signal,” label smoothing caused the plateau, and pre-norm or a larger
batch repairs the failure are causal stories that need isolated ablations.
Branching does not mechanically divide every gradient equally, and removing
hypotheses trades search diversity for optimization simplicity.

## Failure Modes

The main unresolved failures are false confidence from bit-level metrics,
batch-coupled Focus computation, cross-request mutable-memory leakage,
deterministic fallback masking, graph-structure leakage, weak or conflicting
test provenance, fixed schedule progression without learned competence, and a
causal repair story that was not isolated from the many simultaneous changes.

## Evidence

Freeze the DKL-aware predecessor, minimal linear/recurrent baselines, the
failed Spider variant, and Portia component ablations under the same data,
graph, seeds, optimizer search budget, parameters or compute, and stopping
rules. Run:

- coordinate-only, coordinate+edge, +Focus, +memory, +refinement, +confidence,
  and full Portia;
- one versus two refinement blocks;
- memory reset/persist/no-memory and cross-request leakage probes;
- feature-gating versus ordinary MLP;
- the intended attention operation versus batch-shuffled and batch-size
  controls;
- bitwise BCE versus candidate-ranking or graph-metric objectives;
- one-path versus cautiously added multi-path routes with per-path gradients,
  diversity, utilization, and selector credit;
- deterministic engines and fallback disabled/enabled so they cannot mask
  Portia utility; and
- graph mutation, missing edges, contradictory paths, ontology migration,
  unseen relation types, stale coordinates, poisoning, and distribution shift.

Report learning curves and uncertainty across seeds; parameter changes;
gradient and activation health; exact coordinate, edge-valid route, full path,
task, and abstention outcomes; calibration for each outcome; memory retention
and contamination; latency and tails; memory/storage/I/O; fallback and
adversary cost; and total governance burden. A separate evaluator should
inspect traces without gold routes. A result only supports the exact graph,
model, workload, and consumer tested.

## Biological analogy boundary

The Portia-spider discussion is design inspiration, not a transfer result.
Detour behavior does not prove the model plans; small animal brains do not
prove that five million parameters suffice; path integration in physical space
does not validate HLSH navigation; and naming components Scout or Focus does
not reproduce animal cognition. The cited biological and ML references require
their own primary-source verification before publication claims rely on them.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` owns the stable Synapse interface,
  coordinate/edge/confidence outputs, fallback, and candidate comparison.
- `policy-optimization-and-learning-from-feedback` owns phased admission,
  gradient/activation diagnostics, objective choice, credit assignment, and
  calibration training.
- `governed-deliberation-and-test-time-scaling` owns single- versus
  multi-path refinement, working-memory use, stop policy, and causal ablations.
- `benchmark-ratchets-and-anti-goodhart-evidence` owns bit-accuracy traps,
  held-out graph splits, smoke-test versus learning evidence, and matched
  evaluation.
- `durable-semantic-memory-and-knowledge-lattices` owns the RichContext/DKL
  snapshot and mutable-memory isolation boundary.
- `stable-capability-fields` may use the trait/registry pattern as a
  replaceable implementation example, but source compatibility is not
  qualification.

No new chapter is warranted. Portia is the missing implementation-shaped
successor to TreeLLM, not a new top-level architecture layer.

## Claims To Add Or Update

- Replacement-compatible learned routes require semantic compatibility,
  snapshot and codec binding, diagnostic visibility, fallback, and behavioral
  qualification—not only a shared trait or tensor shape.
- Training phases should advance on held-out evidence gates and component
  causality rather than elapsed percentages.
- Confidence must be calibrated to an exact route, task, or release event;
  coordinate-bit averages cannot stand in for navigation success.
- Mutable reasoning memory requires request, user, session, epoch, reset,
  replay, rights, and deletion semantics beyond concurrency safety.

## Open Questions

- Does the displayed Focus operation attend across examples in a batch, and do
  outputs change with unrelated batch neighbors?
- Which Portia component, if any, causally improves exact DKL navigation over
  capacity- and compute-matched simple baselines?
- Can RichContext remain stable across graph and codec migration without
  leaking target structure or collapsing distinct semantic objects?
- What exact test manifest explains the source's 15, 22, and 24 test counts?

## Section-family closure ledger

| Section family | Disposition |
|---|---|
| Abstract and integration table | Successor relation and interface retained; “actually trains,” explainability, and calibration bounded. |
| §1 Portia analogy and Spider comparison | Simplicity/phase lesson retained; biological analogy and causal repair claims bounded. |
| §2 architecture | RichContext, Scout, Focus, memory, refinement, and three heads routed to existing owners. |
| §3 component pseudocode | Pre-norm/residual/gating candidates retained; attention-axis, shared-memory, and fixed-refinement defects made explicit audit targets. |
| §4 training | Five phases, diagnostics, objectives, and ReasoningChain schema retained; fixed thresholds and data leakage require calibration and controls. |
| §5 predecessor comparison | Negative lineage retained; DKL-aware, Spider, and Portia become matched baselines rather than claimed ranking. |
| §6 DKL integration | Typed edges, fallback/adversary path, and answer traversal retained; toy route is illustrative only. |
| §7 roadmap | Smoke checks separated from learning and benchmark gates; unfinished integration preserved. |
| §8 dimensions and counts | Interface dimensions and parameter estimates retained as source-reported design values. |
| §9 success metrics | Converted into exact-route/task/calibration/resource evaluation obligations; source figures not imported. |
| §10 future work | Multi-hypothesis, Graph Mamba, adaptive refinement, conversation memory, and personality remain optional candidates behind ablations. |
| §11 references | Retained as bibliography leads requiring primary-source verification. |
| §12 changelog | Preserved as source lineage; version chronology remains unresolved. |
| Appendix A | Biological inspiration retained with explicit non-transfer boundary. |
| Appendix B | Spider failure lessons retained; causal explanations require isolated ablation. |
| Appendix C | Implementation/test/API claims preserved as source-reported; contradictory test counts and incomplete benchmarking block promotion. |

**Closure result:** every numbered section, appendix, component, data
structure, phase, loss, diagnostic, test family, integration interface,
success metric, future extension, and claimed implementation state has an
explicit disposition. No implementation, test, learning, route, memory,
attention, refinement, calibration, benchmark, latency, resource, biological,
deployment, support, novelty, SOTA, AGI, or ASI result is promoted.
