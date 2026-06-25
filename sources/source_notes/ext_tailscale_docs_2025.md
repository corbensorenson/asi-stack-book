# Source Note: What is Tailscale?

| Field | Value |
|---|---|
| Source ID | `ext_tailscale_docs_2025` |
| Source title | What is Tailscale? |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://tailscale.com/docs/concepts/what-is-tailscale |
| Citation label | Tailscale Docs (2025), What is Tailscale? |
| Published / updated | unknown / 2025-09-30 |
| Ingestion basis | Official public documentation inspected for the Personal Compute Hives external literature queue; no Tailscale deployment or security test was run from this repository. |

## Thesis

Tailscale belongs in the hive chapter as an adjacent networking substrate: it shows a practical pattern for identity-based, encrypted connectivity across devices and networks, but it is not itself a personal AI hive.

## Mechanisms

- Represent a private device network as a tailnet.
- Use identity and access policy as a connectivity boundary.
- Prefer encrypted point-to-point connections where possible.
- Reduce the operational burden of connecting machines across NATs, firewalls, and locations.
- Support personal, homelab, edge, CI/CD, and organization-scale use cases.

## Evidence

- The official docs describe Tailscale as a zero-trust connectivity platform using WireGuard-based encrypted links and peer-to-peer mesh behavior where possible.
- This repository has not deployed Tailscale, audited its implementation, measured network performance, or verified security properties.
- Use this source for the networking-adjacency pattern only: logical hive reachability still needs separate ASI Stack authority, data, approval, and audit records.

## Failure Modes

- Network reachability can be mistaken for execution authority.
- Easy connectivity can expand blast radius if data, tool, and identity policies are weak.
- A mesh network does not by itself solve scheduling, family governance, rented-node isolation, or VCM taint.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use this note to ground the external-literature discussion of private overlay connectivity and identity-based networking.
- Do not cite this source as evidence that a hive scheduler, approval gate, child portal, or federation protocol is safe.

## Open Questions

- Which local fixture should separate hive network reachability from authority grants?
- How should tailnet-like device identity map into `DeviceResourceCard`, `PortalCard`, and revocation records?
- What is the minimum network smoke test for a future prototype without exposing private machines?
