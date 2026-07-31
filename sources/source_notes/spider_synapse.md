# Source Note: SpiderSynapse failure paper

| Field | Value |
|---|---|
| Source ID | `spider_synapse` |
| Source title | SpiderSynapse: A Multi-Hypothesis Reasoning Architecture |
| Source date | 2024-12-23 |
| Ingestion date | Authenticated Google Drive discovery and complete section-family audit completed 2026-07-31 |
| Source version / URL | v0.3.0; https://drive.google.com/file/d/1PPxsdmNbj8Ao1mNIelMrMxEr8ajIgWDn |
| Ingestion basis | Complete 2,719-word Markdown cached at `sources/raw/google_drive/spider_synapse_whitepaper.md`; raw text is not published. |

## Source boundary

## Thesis

SpiderSynapse is TreeLLM's failed multi-hypothesis predecessor to
PortiaSynapse. It proposes a multi-aspect encoder, four latent hypotheses,
three cross-hypothesis refinement iterations, edge-conditioned processing,
working memory, a hypothesis selector, and coordinate, edge, confidence, and
uncertainty heads. Unlike many design papers, it explicitly records that the
implemented training path did not learn: loss remained around 0.57, accuracy
oscillated around 68–70%, coordinate alignment remained around 0.5621 after
hours, working memory was unused, and no benchmark comparison was possible.

This is valuable negative architecture memory. It does not prove that
multi-hypothesis reasoning, attention, refinement, memory, or confidence is
bad. It shows that this joined implementation and training recipe failed under
the reported conditions. Proposed causes remain hypotheses until ablated.

No implementation, log, checkpoint, dataset, graph, or executable test is
present in this repository. All observations are source-reported and cannot be
independently reproduced here.

## Mechanisms

The intended pipeline separates semantic, structural, and edge encoders;
generates four 512-dimensional latent candidates; runs three rounds of
cross-hypothesis attention, edge-conditioned feed-forward transformation, and
memory update; selects or merges candidates; and predicts 128 coordinate bits,
64 edge types, confidence, and epistemic uncertainty.

## Failure Modes

The paper identifies plausible failure surfaces:

- gradients may be weak or distorted through selector and repeated branches;
- hypotheses may collapse to identical states;
- input construction may pad 128 features into a nominal 512-feature context;
- coordinate, edge, confidence, and diversity losses may interfere;
- batch size and optimizer settings may be inappropriate;
- working memory and edge-conditioned paths may exist in code without causal
  use; and
- architectural complexity was added before a one-path baseline learned.

The recovery plan is stronger than the abandoned architecture: set
`K=1, N=1`; train coordinate loss alone; log gradients and candidate
variance; verify context shapes and values; compare the DKL-aware baseline;
then add hypotheses, attention, memory, auxiliary losses, and refinement one
at a time.

## Corrections to preserve

“Four hypotheses times three iterations equals twelve paths, so each receives
one twelfth of the gradient” is not a demonstrated law. Autodiff aggregates
gradients according to the computation and loss; selector saturation,
symmetry, shared weights, poor diversity objectives, or detached paths may be
more important. The experiment should measure per-path gradient norm,
cosine similarity, selector probability, utilization, diversity, advantage,
and parameter update—not infer dilution from path count.

Latent hypotheses are not automatically beam search. They need distinct
semantics or proposals, a diversity objective that does not reward useless
variation, a selection or aggregation rule, credit assignment, and a matched
discrete or search baseline. A weighted merge may create a state corresponding
to no coherent route.

Iterative hidden transforms are not test-time deliberation unless later steps
receive new information, improve a declared objective, and can stop, backtrack,
or branch meaningfully. Working memory is not useful because a tensor exists;
its state must retain task-relevant facts, remain isolated between episodes,
and causally improve held-out multi-hop tasks.

Confidence and uncertainty heads require labels, proper scoring, held-out
calibration, selective-risk evaluation, and a named downstream action.
Predicting a number does not make the model know that it does not know.

## Evidence

Keep the failure trace as the frozen negative baseline. Reproduce it if the
code and data become available, then compare:

- DKL-aware one-path baseline;
- minimal Spider `K=1, N=1`;
- one hypothesis with increasing refinement;
- increasing hypotheses with no refinement;
- full factorial hypothesis/refinement grid;
- attention, memory, edge-conditioning, selector, diversity, auxiliary-loss,
  normalization, label-smoothing, and input-construction ablations; and
- Portia under matched parameter, compute, data, seed, and tuning budgets.

Report exact coordinate and valid-route outcomes, not bit accuracy alone;
learning curves across seeds; per-path gradient and utilization; hypothesis
diversity and usefulness; selector entropy; memory retention/leakage; loss
interference; calibration; latency, memory, and total cost; and fallback.
Failure to beat the one-path baseline narrows or retires the branching route
for that workload. A later Portia success would not erase this result.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` owns the failed credit
  assignment, loss isolation, diagnostics, and staged recovery.
- `governed-deliberation-and-test-time-scaling` owns multi-hypothesis and
  iterative-refinement claims plus one-path and search baselines.
- `benchmark-ratchets-and-anti-goodhart-evidence` owns negative-result
  retention, exact metrics, matched tuning budgets, and non-erasure by a
  successor.
- `routing-heads-and-specialist-cores` owns the candidate/selector/confidence
  interface and collapse/fallback behavior.

## Claims To Add Or Update

- Preserve the failed joined system as a bounded negative result without
  converting a plausible post-hoc diagnosis into causality.
- Establish one hypothesis and one refinement before adding branch count,
  depth, selection, memory, auxiliary losses, or confidence heads.
- Measure per-path gradient, diversity, utilization, selector credit, exact
  navigation, memory use, calibration, and total cost under matched baselines.
- A later Portia result may add evidence but cannot erase Spider's denominator.

## Open Questions

- Did optimization fail because of target geometry, input construction,
  selector saturation, branch collapse, loss interference, memory, or another
  implementation detail?
- Do latent hypotheses correspond to distinct useful routes or merely noisy
  states that a weighted merge makes less coherent?
- Can repeated hidden transforms repair errors under new evidence, or are they
  only additional fixed depth?
- Does the architecture ever beat a one-path DKL-aware baseline under matched
  parameters, compute, data, tuning, seeds, and stopping rules?

## Section-family closure ledger

| Section family | Disposition |
|---|---|
| Abstract and critical status | Failed training retained as bounded source-reported negative evidence. |
| §1 motivation | Candidate diversity, refinement, uncertainty, and edge-aware routing retained as hypotheses. |
| §2 architecture | Multi-branch topology retained for factorial ablation, not adoption. |
| §3 components | Encoders, candidates, tower, selector, memory, and heads routed to their test obligations. |
| §4 training | Losses and curriculum retained; label semantics, interference, and held-out calibration required. |
| §5 comparison | DKL-aware baseline preserved; wrapper/direct-output claims remain untested. |
| §6 implementation status | Built versus broken components preserved without treating code existence as capability. |
| §7 failure analysis | Observations separated from causal hypotheses and recovery experiments. |
| §8 open questions and dimensions | Exact candidate grid and interface constants retained as experiment inputs. |
| §9–10 rationale and wrapper comparison | Beam-search, thinking-time, calibration, speed, and direct-quality analogies bounded. |
| §11 roadmap | Reordered into minimal baseline, component gates, fallback, and retirement. |
| §12–13 metrics and immediate TODO | Converted into exact-route, utility, calibration, gradient, and resource obligations. |
| §14 references and changelog | Retained as bibliography/version leads; no external claim imported. |

**Closure result:** every numbered section, component, loss, dimension,
failure observation, proposed cause, recovery step, metric, roadmap item, and
reference family has an explicit disposition. No implementation, causal
failure explanation, learning, reasoning, search, memory, calibration,
benchmark, efficiency, deployment, support, novelty, SOTA, AGI, or ASI claim
is promoted.
