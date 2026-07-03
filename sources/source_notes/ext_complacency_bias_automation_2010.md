# Source Note: Complacency and Bias in Human Use of Automation: An Attentional Integration

| Field | Value |
|---|---|
| Source ID | `ext_complacency_bias_automation_2010` |
| Source title | Complacency and Bias in Human Use of Automation: An Attentional Integration |
| Ingestion date | 2026-07-03 |
| Source version / URL | https://pubmed.ncbi.nlm.nih.gov/21077562/ |
| Citation label | Parasuraman and Manzey (2010), Complacency and Bias in Human Use of Automation |
| Published / updated | 2010 |
| DOI | 10.1177/0018720810376055 |
| Ingestion basis | Primary metadata/abstract record inspected; paper not vendored or reproduced. |

## Thesis

Human oversight degradation has an attention component. Parasuraman and Manzey
connect automation complacency and automation bias, including omission and
commission errors around imperfect decision aids. For the ASI Stack, that
supports treating approval fatigue, rubber-stamping, and recommendation
overreliance as adapter failure modes that must route to delay, rotation,
independent checking, or blocked dispatch.

## Mechanisms

- Automation complacency can appear under workload and divided-attention
  conditions.
- Automation bias can lead people to omit checks or commit to a flawed
  recommendation.
- A runtime adapter should not accept approval when visible contradictory
  evidence has not been independently checked.

## Evidence

The source is external human-factors literature. This book uses it for
source-grounded comparator context only; no local human-subjects study,
approval-service benchmark, or deployed reviewer-quality result is claimed.

## Failure Modes

- Reviewer accepts the system recommendation without checking independent
  evidence.
- Alerts become background noise and reviewers stop treating them as meaningful.
- Short, template-only approvals masquerade as reviewed decisions.
- The book accidentally promotes approval-service quality from a fixture shape.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`
- `human-intent-as-a-formal-input`
- `evidence-states-and-claim-discipline`

## Claims To Add Or Update

- Add automation bias and complacency controls to the runtime-adapter human
  approval boundary.
- Use reviewer degradation as a source-grounded reason to preserve no-claim
  boundaries around human approval.

## Open Questions

- What independent-evidence check is adequate for different adapter risk tiers?
- How can the stack measure approval fatigue without overfitting to superficial
  review-time metrics?
