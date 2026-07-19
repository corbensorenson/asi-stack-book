# Source Note: Measuring the Persuasiveness of Language Models

| Field | Value |
|---|---|
| Source ID | `ext_anthropic_model_persuasiveness_2024` |
| Source title | Measuring the Persuasiveness of Language Models |
| Ingestion date | 2026-07-19 |
| Source version / URL | Anthropic official research page, https://www.anthropic.com/news/measuring-model-persuasiveness |
| Citation label | Durmus et al. (2024), Measuring Model Persuasiveness |
| Published / updated | 2024-04-09 / 2024-04-09 |
| DOI | None listed |
| Review state | Preliminary second-tranche audit note; the proposed chapter remains unadmitted. |
| Ingestion basis | Official provider methods, results, and future-research passages inspected. The released dataset, complete analysis code, participant records, all prompts/arguments, and independent reproductions were not audited locally. |

## Thesis

Persuasive capability can be measured as change in stated agreement after a
message, and provider-reported results suggest that such capability changes
across model generations. The study is useful as a capability-evaluation
baseline, while its one-message design and provider provenance make it
insufficient for deployed influence or governance claims.

## Mechanisms

- Ask a participant's agreement with a claim before exposure.
- Present a model- or human-written argument for the claim.
- Re-measure agreement and compare persuasive effect.
- Evaluate multiple model generations and two model-size classes across 56
  claims spanning 28 topics.
- Release the study data and identify dialogue and real-world action as future
  research boundaries.

## Evidence

The official report describes within-class generational trends and reports no
statistically significant difference between its Claude 3 Opus and human
argument score in the tested setting. It explicitly does not establish whether
the arguments change real decisions or actions. This is provider-run,
single-message, stated-opinion evidence, not an independent deployed-system or
mitigation evaluation.

## Failure Modes

- Treating rated or short-term persuasiveness as durable behavioral influence.
- Collapsing topic, audience, model family, message format, dialogue, and channel
  differences into one general capability score.
- Turning a scaling observation into inevitability or a frontier-wide ranking.
- Using a provider-run capability result as evidence that a proposed safeguard
  works or that benign persuasion remains benign under optimization pressure.

## Book Chapters Supported

- Proposed: `human-ai-communication-persuasion-and-epistemic-security`
- Existing boundary owners: `capability-thresholds-and-deployment-commitments`,
  `benchmark-ratchets-and-anti-goodhart-evidence`,
  `scalable-oversight-and-adversarial-ai-control`,
  `human-factors-and-meaningful-control-in-oversight`, and
  `adversarial-evaluation-sandbagging-and-training-time-deception`

## Claims To Add Or Update

- Preserve capability measurement separately from communication permission,
  beneficial purpose, informed consent, observed effect, and remedy.
- Demand interactive, delayed, behavioral, and independently reproduced evidence
  before broad persuasion claims.
- Measure useful explanation and informed correction alongside harmful influence,
  false refusal, user autonomy, and communication cost.
- Do not infer chapter admission, mitigation efficacy, safety, or support-state
  movement from this provider report.

## Open Questions

- Which metrics distinguish epistemically useful explanation from mere opinion
  movement?
- How does persuasion change under personalization, repetition, relationship,
  emotional dependence, channel amplification, and agentic goal pursuit?
- What capability threshold should trigger communication restrictions or review?
