# Source Note: Measuring AI Ability to Complete Long Software Tasks

| Field | Value |
|---|---|
| Source ID | `ext_metr_time_horizons_2025` |
| Source title | Measuring AI Ability to Complete Long Software Tasks |
| Ingestion date | 2026-07-10 |
| Source version / URL | arXiv:2503.14499v3, https://arxiv.org/abs/2503.14499 |
| Citation label | Kwa et al. (2025), Measuring AI Ability to Complete Long Software Tasks |
| Published / updated | 2025-03-18 / 2026-02-25 |
| DOI | 10.48550/arXiv.2503.14499 |
| Ingestion basis | Primary arXiv HTML paper inspected for its task-completion-time-horizon definition, task and human-baseline setup, evaluation limitations, and scope of extrapolation. No model, agent scaffold, human baseline, task suite, time-horizon estimate, or reported result was reproduced in this repository. |

## Thesis

The paper proposes an evaluation-specific 50%-task-completion time horizon: the
human time associated with tasks an agent completes at a 50% success rate. It
uses selected software and research-engineering task suites and human baselines
to make capability comparisons more interpretable than isolated benchmark
scores. The paper also states important task-distribution, context, human
baseline, and external-validity limitations, so its metric is not a general
autonomy, job-replacement, safety, or deployment measure.

## Mechanisms

- Define task completion against a specified success probability and a measured
  human baseline rather than treating agent wall-clock duration as the metric.
- Estimate a horizon from task families, task attempts, success observations,
  and declared model-agent scaffolding.
- Compare alternative human baselines and document how context, task definition,
  and scoring change the interpretation of a horizon.
- Separate a measured current-task result from extrapolation about future task
  distributions or capability trends.

## Evidence

- The primary paper reports time-horizon measurements and comparisons under its
  selected tasks, human baselines, agent scaffolds, success definition, and
  statistical analysis.
- It explicitly discusses limitations of external validity, task distributions,
  context effects, human baselining, elicitation, and extrapolation.
- This repository has not run a time-horizon evaluation, timed humans, measured
  an agent's autonomous task completion, reproduced a trend, or adopted a
  reported value as a threshold. The source is a measurement-design comparator
  only.

## Failure Modes

- A task-horizon estimate can be treated as a general autonomy, economic, or
  deployment claim outside its task and success envelope.
- Human baselines with different context or role knowledge can change the
  apparent task length and make cross-study threshold comparisons misleading.
- A threshold can be triggered by a noisy, stale, or under-elicited evaluation
  without recording uncertainty, coverage, or a re-evaluation condition.
- A trend extrapolation can be mistaken for evidence that a future capability
  crossing has already occurred.

## Book Chapters Supported

- `capability-thresholds-and-deployment-commitments` (Capability Thresholds and Deployment Commitments)

## Claims To Add Or Update

- Use this note for evaluation-envelope, human-baseline, success-probability,
  uncertainty, coverage-date, and re-evaluation vocabulary in threshold records.
- Treat time horizon as one scoped capability measurement that may inform a
  declared commitment; it is not the threshold system itself.
- Do not claim a local time horizon, autonomy level, general capability,
  dangerous-capability profile, safeguard sufficiency, safety, or ASI.

## Open Questions

- Which public-safe task families could support an ASI Stack threshold fixture
  without confusing task length with general autonomy?
- How should a threshold record preserve competing human baselines, evaluation
  context, uncertainty, and recency rather than one scalar headline?
- Which threshold decision must be blocked when the evaluation's scope is not
  comparable to the commitment it would trigger?
