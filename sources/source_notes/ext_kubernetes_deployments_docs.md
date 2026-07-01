# Source Note: Kubernetes Documentation - Deployments

| Field | Value |
|---|---|
| Source ID | `ext_kubernetes_deployments_docs` |
| Source title | Kubernetes Documentation: Deployments |
| Ingestion date | 2026-07-01 |
| Source version / URL | https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ |
| Citation label | Kubernetes Documentation, Deployments |
| Published / updated | unknown / unknown |
| Ingestion basis | Official public Kubernetes documentation inspected for rollout history and rollback vocabulary; no Kubernetes cluster, Deployment object, ReplicaSet, rollout history, or rollback command was run from this repository. |

## Thesis

Kubernetes Deployments provide a familiar external comparator for rollout status, rollout history, revision metadata, and rollback to a previous stable revision. The replacement chapter should use Kubernetes as baseline deployment-control vocabulary while making clear that ASI replacement requires more than restoring a ReplicaSet: semantic field identity, authority ceilings, evaluator independence, state-migration solvency, residual ownership, and support-state discipline.

## Mechanisms

- Manage a desired Deployment state through a controller.
- Track rollout status and progress.
- Keep revision history so operators can inspect previous rollout revisions.
- Roll back a Deployment to a previous or specified stable revision.
- Use annotations or tooling to preserve change-cause context for revisions.

## Evidence

- The public documentation describes Deployment rollout status, automatic stopping behavior for some bad rollouts, rollout history inspection, revision details, and rollback to prior revisions.
- It gives rollback commands and shows that revision history can be inspected before choosing a rollback target.
- This repository has not created a Deployment, observed rollout status, inspected live history, or executed `kubectl rollout undo`.

## Failure Modes

- Deployment rollback can be mistaken for semantic rollback when state, external effects, or model behavior cannot be reverted by restoring a prior workload.
- Revision history can omit the evidence needed for capability identity, authority, evaluator independence, and residual accountability.
- A controller can stop or roll back a workload without proving the upstream candidate was evaluated correctly.
- Cluster-level rollback does not by itself settle user-visible harm, data migration, or downstream artifact contamination.

## Book Chapters Supported

- `capability-replacement-and-rollback` (Capability Replacement and Rollback)

## Claims To Add Or Update

- Use this note to ground rollout history, revision, stable prior, and rollback vocabulary.
- Contrast Kubernetes rollback with the ASI Stack rollback receipt, which also names reversible fields, irreversible effects, trigger conditions, ownership, and support-state effects.
- Do not claim Kubernetes integration, deployment-controller behavior, or live rollback evidence.

## Open Questions

- Which rollback-receipt fields are analogous to Deployment revision history, and which must remain ASI-specific?
- Should future replacement fixtures include a separate `change_cause` field for human-readable audit context?
- How should rollback receipts represent non-reversible external effects after a successful workload rollback?
