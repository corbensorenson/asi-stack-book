# Source Note: Kubernetes Documentation - Overview

| Field | Value |
|---|---|
| Source ID | `ext_kubernetes_overview_docs` |
| Source title | Kubernetes Documentation: Overview |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://kubernetes.io/docs/concepts/overview/ |
| Citation label | Kubernetes Documentation, Overview |
| Published / updated | unknown / unknown |
| Ingestion basis | Official public documentation inspected for the Personal Compute Hives external literature queue; no Kubernetes cluster was deployed from this repository. |

## Thesis

Kubernetes is relevant as the canonical container-orchestration substrate that demonstrates scheduling, rollout, storage, and self-healing patterns. The hive chapter should contrast this with the additional personal authority, data, family, and federation membranes the ASI Stack needs.

## Mechanisms

- Manage containerized workloads and services through declarative configuration and automation.
- Provide service discovery, load balancing, storage orchestration, rollouts, rollbacks, bin packing, and self-healing.
- Treat clusters of nodes as schedulable infrastructure for containerized tasks.
- Preserve user choice by exposing building blocks rather than a complete application platform.

## Evidence

- The official overview documents Kubernetes' general orchestration features and explicitly frames Kubernetes as an extensible platform rather than a full application-level service layer.
- This repository has not run Kubernetes, configured a cluster, measured scheduling quality, or tested workload isolation.
- Use this source for orchestration vocabulary and known substrate primitives, not for personal hive governance claims.

## Failure Modes

- Container scheduling can be mistaken for policy-complete personal AI scheduling.
- Kubernetes-level readiness does not encode child consent, secret-handle policy, private-memory taint, or physical-tool approvals by default.
- Cluster complexity can exceed the needs of a first personal-hive prototype.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use this note to explain why existing orchestrators cover important substrate mechanics but not the whole governed hive layer.
- Do not promote the hive core claim from this source alone.

## Open Questions

- Which hive records should map onto Kubernetes nodes, pods, namespaces, service accounts, and admission policies in a future prototype?
- Would K3s, Nomad, or a simpler local queue be a better first substrate?
- Which ASI Stack approval and evidence records must exist outside the orchestrator?
