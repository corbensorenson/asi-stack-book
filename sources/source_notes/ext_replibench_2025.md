# Source Note: RepliBench

| Field | Value |
|---|---|
| Source ID | `ext_replibench_2025` |
| Source title | RepliBench: Evaluating the Autonomous Replication Capabilities of Language Model Agents |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:2504.18565v2, https://arxiv.org/abs/2504.18565 |
| Citation label | Black et al. (2025), RepliBench |
| Published / updated | 2025-04-21 / 2025-05-05 |
| DOI | 10.48550/arXiv.2504.18565 |
| Review state | Preliminary second-tranche audit note; the proposed chapter remains unadmitted. |
| Ingestion basis | Official arXiv metadata and abstract inspected. The paper body, tasks, prompts, code, environments, provider interactions, model traces, and scores were not ingested or reproduced locally. No real replication testing was performed. |

## Thesis

Autonomous replication is a composed capability whose components can progress
unevenly. The reviewed abstract introduces a benchmark that decomposes the
capability into four domains and reports model evaluation across a task family.
It is a preliminary risk-evaluation comparator, not evidence that a local agent
can replicate or that containment works.

## Mechanisms

- Four abstract-level domains: obtaining resources, exfiltrating model weights,
  replicating onto compute, and persisting on that compute.
- Twenty task families comprising 86 individual tasks.
- Source-reported evaluation of five frontier models.
- Component-level results that remain distinct from end-to-end replication.

## Evidence

The abstract reports that the evaluated models did not pose a credible full
self-replication threat in that study, while succeeding on multiple component
tasks and struggling on other components. It also reports pass-at-ten results
for the best evaluated model. No task, score, model, provider path, credential,
weight transfer, deployment, persistence, or shutdown test has been reproduced
here.

## Failure Modes

- Collapsing component success into an end-to-end replication claim.
- Hiding task-family, variant, attempt-count, and human-assistance denominators.
- Treating benchmark conditions as equivalent to real providers or defenses.
- Converting a safety benchmark into operational instructions or real-world
  replication authority.

## Book Chapters Supported

- Proposed: `autonomous-replication-proliferation-and-containment`
- Existing boundary owners: `recursive-self-improvement-boundaries`,
  `model-weight-custody-and-hardware-roots-of-trust`, and
  `security-kernel-and-digital-scifs`

## Claims To Add Or Update

- Preserve component-wise and end-to-end denominators in later evaluation.
- Restrict any future campaign to synthetic providers, fake resources,
  non-deployable artifacts, and independently enforceable termination.
- Do not infer local capability, safety, containment, or testing authority from
  the source-reported benchmark.

## Open Questions

- Which components dominate end-to-end capability under human assistance?
- What positive controls show that a synthetic sandbox is measuring the
  intended component without enabling a real one?
- Which shutdown and descendant-lineage tests are independently enforceable?
