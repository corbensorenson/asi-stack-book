# Source Note: K3s - Lightweight Kubernetes

| Field | Value |
|---|---|
| Source ID | `ext_k3s_docs_2026` |
| Source title | K3s: Lightweight Kubernetes |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://docs.k3s.io/ |
| Citation label | K3s Documentation (2026), Lightweight Kubernetes |
| Published / updated | unknown / 2026-06-15 |
| Ingestion basis | Official public documentation inspected for the Personal Compute Hives external literature queue; no K3s installation was performed from this repository. |

## Thesis

K3s is a useful edge and homelab reference because it compresses Kubernetes into a lighter operational package. It is relevant to the hive build ladder, but it still does not encode ASI Stack authority or family-governance semantics.

## Mechanisms

- Package a compliant Kubernetes distribution as a small binary or minimal container image.
- Target edge, homelab, IoT, CI, single-board computer, air-gapped, and embedded deployments.
- Use lightweight defaults and bundled components for cluster creation.
- Reduce operational complexity relative to full Kubernetes in small environments.

## Evidence

- The official docs describe K3s as lightweight Kubernetes intended for edge-like and constrained settings.
- This repository has not installed K3s, joined nodes, deployed workloads, or tested air-gapped behavior.
- Use this source to ground the "small cluster / edge substrate" candidate in the hive chapter.

## Failure Modes

- Lightweight orchestration still may be too heavy for phones, tablets, and casual family devices.
- K3s can run jobs, but it does not decide which jobs are lawful, private, age-appropriate, or evidence-sufficient.
- Edge convenience can hide update, credential, and network-boundary risks.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use this source as a concrete candidate for home/workshop/site hive infrastructure.
- Keep claims about personal-hive safety, scheduler quality, and user benefit at `argument` until prototypes or tests exist.

## Open Questions

- Could an MVP hive use K3s only for stable always-on nodes while phones remain portals?
- What admission controls would encode `HiveJobContract` policy?
- How should K3s node labels map to device trust and data classes?
