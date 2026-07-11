# Source Note: Don't Hallucinate, Abstain

| Field | Value |
|---|---|
| Source ID | `ext_dont_hallucinate_abstain_2024` |
| Source title | Don't Hallucinate, Abstain: Identifying LLM Knowledge Gaps via Multi-LLM Collaboration |
| Ingestion date | 2026-07-11 |
| Source version / URL | ACL 2024, https://aclanthology.org/2024.acl-long.786/ |
| Citation label | Feng et al. (2024), Don't Hallucinate, Abstain |
| Published / updated | 2024-08 / 2024-08 |
| DOI | 10.18653/v1/2024.acl-long.786 |
| Ingestion basis | Primary ACL abstract and paper metadata reviewed; models, prompts, and reported improvements were not reproduced. |

## Thesis

Knowledge gaps persist, self-reflection and held-out calibration can fail, and
abstention quality can benefit from separately probed evidence or model views.

## Mechanisms

- Calibration/adaptation baselines for abstention.
- Cooperative and competitive model probing for knowledge gaps.
- Abstain-accuracy evaluation across multiple QA domains.

## Evidence

The paper reports improvements in its models and tasks. P2's single-model
candidate pool is not a reproduction or independent multi-model panel.

## Failure Modes

Collaborating models share blind spots; extra calls increase cost; calibration
can overfit held-out sets; abstention can become useless over-refusal.

## Book Chapters Supported

- `routing-heads-and-specialist-cores`
- `readiness-gates-residual-escrow-and-quarantine`
- `verification-bandwidth-and-context-adequacy`

## Claims To Add Or Update

Measure abstention risk, coverage, and useful release together; do not treat
model agreement as independent truth.

## Open Questions

- Which abstention signals remain calibrated under adversarial ambiguity?
- When is clarification preferable to abstention?
