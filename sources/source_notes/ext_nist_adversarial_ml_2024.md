# Source Note: NIST Adversarial Machine Learning Taxonomy

| Field | Value |
|---|---|
| Source ID | `ext_nist_adversarial_ml_2024` |
| Source title | Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations |
| Ingestion date | 2026-07-24 |
| Source version / URL | NIST AI 100-2 E2023 final, https://doi.org/10.6028/NIST.AI.100-2e2023 |
| Citation label | Vassilev et al. (2024), NIST AI 100-2 |
| Published | 2024-01-04 |
| DOI | 10.6028/NIST.AI.100-2e2023 |
| Ingestion basis | Official NIST publication page, abstract, scope, taxonomy description, and publication metadata inspected; no attack or mitigation reproduced locally. |

## Thesis

Adversarial machine learning needs shared terminology organized by learning
method, lifecycle stage, attacker goal, attacker knowledge and capability,
attack family, and mitigation. The taxonomy spans predictive and generative
systems and treats mitigation limits and open challenges as part of the field.

## Mechanisms

- Use lifecycle stage, goal, knowledge, capability, and access when declaring a
  model threat rather than naming an attack without a threat model.
- Keep evasion, poisoning, privacy, misuse, trojan/backdoor, and generative
  attack families distinct enough to preserve mechanism and defense scope.
- Treat mitigations as threat-relative controls, not universal guarantees.
- Use the report as a terminology and coverage comparator, not empirical
  evidence that any ASI Stack model is robust.

## Failure Modes

- Claiming robustness without model/checkpoint, attacker, budget, and access.
- Evaluating a defense only against attacks that ignore the defense.
- Collapsing predictive, generative, multimodal, and agentic surfaces.
- Treating a taxonomy or listed mitigation as proof of effectiveness.

## Book Chapters Supported

- `adversarial-machine-learning-and-model-attack-surface`
- Boundary references: `security-kernel-and-digital-scifs`,
  `privacy-data-rights-and-information-flow-governance`, and
  `adversarial-evaluation-sandbagging-and-training-time-deception`

## Claims To Add Or Update

- Every robustness statement should name the model or checkpoint, lifecycle
  stage, attacker goal, knowledge, capability, access, budget, and evaluated
  attack family.
- Mitigation evidence remains bounded to the tested threat model and cannot
  establish general robustness.
- Predictive, generative, multimodal, tool-using, and agentic attack surfaces
  require explicit cross-surface composition tests.

## Open Questions

- Which taxonomy extensions are required for durable memory, autonomous tools,
  model routing, replication, and multi-agent attack chains?
- How should adaptive attackers and mitigation-aware evaluation budgets be
  standardized without making the benchmark itself the only target?
- What recovery evidence is sufficient after poisoning or a persistent
  backdoor affects checkpoints, caches, descendants, and downstream artifacts?

## Evidence boundary

No local evasion, poisoning, backdoor, extraction, inversion, jailbreak,
multimodal, adaptive-attack, defense, recovery, or transfer result is claimed.
The source supports vocabulary and threat-model structure only.
