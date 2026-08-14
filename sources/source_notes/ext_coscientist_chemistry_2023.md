# Source Note: Autonomous Chemical Research with Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_coscientist_chemistry_2023` |
| Source title | Autonomous chemical research with large language models |
| Ingestion date | 2026-08-13 |
| Source version / URL | Nature article, https://www.nature.com/articles/s41586-023-06792-0 |
| Citation label | Boiko et al. (2023), Coscientist |
| Published | 2023-12-20 |
| DOI | 10.1038/s41586-023-06792-0 |
| Review state | Passage-reviewed external source for bounded language-model planning and laboratory-tool integration; no chemistry result or autonomy claim has been reproduced locally. |
| Ingestion basis | Official Nature full-text article, including system components, six evaluation tasks, reported demonstrations, human oversight, and limitations. |

## Thesis

Coscientist connects a language-model planner to web and document search, code
execution, and robotic laboratory interfaces. It demonstrates why scientific
governance must distinguish planning competence, API execution, physical
intervention, measurement, and claim adjudication instead of compressing them
into one label such as autonomous scientist.

## Mechanisms

- A planner decomposes goals and invokes search, code, documentation, and
  laboratory tools.
- Evaluations cover synthesis planning, documentation navigation, cloud-lab
  commands, liquid handling, multiple laboratory modules, and reaction
  optimization.
- External documentation and web retrieval ground some planning steps.
- Human researchers oversaw the reported experiments and the bounded equipment
  environment constrained available actions.

## Evidence

The paper reports six families of chemistry tasks and demonstrations involving
robotic equipment and reaction optimization. One synthesis-planning assessment
used subjective scoring, and the paper describes planning errors including an
infeasible nitration proposal. The results are evidence about the reported
system, tasks, and laboratory configuration. They do not establish an
independent general scientist, general laboratory safety, causal discovery, or
transfer beyond the studied chemistry workflows.

## Failure Modes

- Conflating successful tool invocation with a scientifically valid result.
- Hiding technician oversight, permitted recovery, equipment constraints, or
  failed plans behind an autonomy label.
- Treating subjective planning scores as equivalent to experimental evidence.
- Letting a planner expand instrument authority or reinterpret measurements.
- Generalizing from bounded chemistry tasks to domain-general science.

## Book Chapters Supported

- `scientific-discovery-and-experimental-governance`
- Adjacent boundary owners: `runtime-adapters-tool-permissions-and-human-approval`,
  `embodied-agency-real-time-control-and-physical-safety`, and
  `planning-as-a-control-layer`

## Claims To Add Or Update

- Separate proposal, documentation retrieval, code, physical action,
  observation, analysis, and scientific claim authority.
- Preserve human interventions and failed plans as part of the attempt record.
- Evaluate physical-laboratory agents with known-null and known-effect controls,
  calibration challenges, and independent analysis.

## Open Questions

- Which interventions were necessary to recover from model or equipment error?
- How much of the result depends on the exact documentation, API wrapper,
  equipment envelope, and human supervision?
- Can a separate analysis path reproduce the scientific interpretation from raw
  observations?
