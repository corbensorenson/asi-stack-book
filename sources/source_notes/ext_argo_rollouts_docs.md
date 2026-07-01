# Source Note: Argo Rollouts Documentation - Kubernetes Progressive Delivery Controller

| Field | Value |
|---|---|
| Source ID | `ext_argo_rollouts_docs` |
| Source title | Argo Rollouts Documentation: Kubernetes Progressive Delivery Controller |
| Ingestion date | 2026-07-01 |
| Source version / URL | https://argo-rollouts.readthedocs.io/en/stable/ |
| Citation label | Argo Rollouts Documentation, Kubernetes Progressive Delivery Controller |
| Published / updated | unknown / unknown |
| Ingestion basis | Official public documentation inspected for progressive-delivery vocabulary; no Argo Rollouts controller, Kubernetes cluster, rollout object, metric query, promotion, or rollback was run from this repository. |

## Thesis

Argo Rollouts is a strong external comparator for the rollout side of the replacement chapter. It gives the book known engineering vocabulary for blue-green rollout, canary rollout, traffic shaping, analysis, automated promotion, automated rollback, manual judgment, and blast-radius control. The ASI Stack replacement transaction should import the discipline of scoped exposure and rollback evidence while adding field identity, authority ceilings, evaluator independence, residual inheritance, and support-state accounting.

## Mechanisms

- Represent a rollout as a controller-managed transition from a stable version to a new version.
- Use blue-green and canary strategies to separate preview/canary traffic from default traffic.
- Use weighted traffic shifting and metrics analysis to drive promotion or rollback decisions.
- Treat automated promotion and automated rollback as controller features, not as proof that every rollout is safe.
- Keep analysis and manual judgment visible as part of the transition path.

## Evidence

- The public documentation describes Argo Rollouts as a Kubernetes controller and CRD set for advanced deployment patterns, including blue-green, canary, canary analysis, experimentation, and progressive delivery.
- The documentation positions rolling updates as limited when deeper checks, traffic-flow control, external metrics, blast-radius control, or automated rollback are required.
- This repository has not installed Argo Rollouts, created a Rollout resource, queried metrics, executed an abort, or replayed a controller rollback.

## Failure Modes

- Progressive-delivery language can be mistaken for actual deployment evidence.
- Traffic shifting and metric analysis do not by themselves enforce authority ceilings, evaluator independence, semantic field identity, residual ownership, or support-state boundaries.
- Automated rollback can still be unavailable or misleading if state migration, external effects, trigger conditions, or ownership are not recorded.
- Kubernetes application rollout concepts do not directly solve model replacement, tool replacement, policy replacement, or recursive self-improvement safety.

## Book Chapters Supported

- `capability-replacement-and-rollback` (Capability Replacement and Rollback)

## Claims To Add Or Update

- Use this note to ground the chapter's canary, blue-green, progressive-delivery, metric-analysis, automated-promotion, and automated-rollback vocabulary.
- State that ASI Stack replacement transactions are stricter than rollout controllers because they also track field identity, authority, evaluator independence, residuals, and evidence support.
- Do not promote the replacement chapter above `argument` support from this source alone.

## Open Questions

- Which replacement-transaction fields should map onto rollout strategy, traffic weight, metric analysis, promotion, abort, and rollback fields in a future prototype?
- Which metrics would be legitimate for ASI replacement canaries, and which would create Goodhart pressure?
- How should a replacement transaction distinguish application rollback from semantic capability rollback when state or external effects cannot be fully reversed?
