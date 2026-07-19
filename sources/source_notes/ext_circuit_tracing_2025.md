# Source Note: Circuit Tracing

| Field | Value |
|---|---|
| Source ID | `ext_circuit_tracing_2025` |
| Source title | Circuit Tracing: Revealing Computational Graphs in Language Models |
| Ingestion date | 2026-07-19 |
| Source version / URL | 2025-03-27, https://transformer-circuits.pub/2025/attribution-graphs/methods.html |
| Citation label | Ameisen et al. (2025), Circuit Tracing |
| Published / updated | 2025-03-27 / 2025-03-27 |
| DOI | not recorded |
| Ingestion basis | Primary methods article and official open-source announcement inspected; code, replacement models, and interventions were not run locally. |

## Thesis

Circuit tracing constructs prompt-local attribution graphs through a sparse
cross-layer replacement model and then tests graph hypotheses with
perturbations. It is a strong comparator for model-internal evidence because it
keeps approximation error, pruning, local scope, and mechanistic faithfulness
visible instead of equating a readable graph with the original model.

## Mechanisms

- Replace MLP computation with jointly trained cross-layer transcoder features.
- Freeze selected nonlinearities and form prompt-local attribution graphs.
- Preserve reconstruction-error nodes and prune large graphs for inspection.
- Test graph predictions through activation perturbations.
- Evaluate replacement-model fidelity separately from graph readability.

## Evidence

The article reports quantitative replacement-model and attribution-graph
evaluation plus bounded case studies. The repository has not reproduced the
method or inspected a local model. This is external positioning, not evidence
that any ASI Stack component is understood or safe.

## Failure Modes

- Replacement-model behavior can diverge from the underlying model.
- Frozen attention patterns omit why attention moved information.
- Reconstruction error, pruning, labels, and prompt selection can create a
  plausible but incomplete causal story.
- A successful local intervention can be overgeneralized to other prompts,
  checkpoints, models, or deployment conditions.

## Book Chapters Supported

- Proposed: `white-box-evidence-interpretability-and-activation-governance`
- Existing boundary owners: `evidence-states-and-claim-discipline`,
  `adversarial-evaluation-sandbagging-and-training-time-deception`

## Claims To Add Or Update

- Require model/checkpoint, layer, prompt population, extraction method,
  approximation error, pruning rule, intervention, comparator, and maximum
  inference in every white-box evidence packet.
- Treat attribution graphs as hypotheses about scoped mechanisms, not whole-
  model explanations.
- Separate observation from activation intervention and activation authority.

## Open Questions

- What faithfulness threshold makes a white-box record admissible for a claim?
- Which negative controls detect explanation laundering through readable graphs?
- How should intervention side effects and activation rollback be recorded?
