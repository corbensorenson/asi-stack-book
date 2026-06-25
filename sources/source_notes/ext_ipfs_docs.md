# Source Note: IPFS Documentation and Project Site

| Field | Value |
|---|---|
| Source ID | `ext_ipfs_docs` |
| Source title | IPFS Documentation and Project Site |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://ipfs.tech/ |
| Citation label | IPFS Project Site |
| Published / updated | unknown / unknown |
| Ingestion basis | Official IPFS project site and documentation inspected for the Personal Compute Hives external literature queue; no IPFS node, gateway, pinning service, or content-addressed storage workflow was configured from this repository. |

## Thesis

IPFS is relevant to Personal Compute Hives because it supplies vocabulary for content-addressed, peer-to-peer data location and retrieval. It is useful for artifact identity, distributed retrieval, and content-addressed storage discussion, but it does not by itself provide privacy, VCM revocation, authority control, family policy, or safe federation.

## Mechanisms

- Address content by identifiers derived from content rather than only by server location.
- Retrieve data through peer-to-peer participation and provider discovery.
- Separate content identity from a single hosting location.
- Support distributed artifact publication and retrieval patterns.
- Expose a substrate candidate for artifact bundles, public caches, and reproducible references.

## Evidence

- The official IPFS project material presents IPFS as peer-to-peer content delivery built around content addressing.
- This repository has not run an IPFS node, pinned content, tested gateway behavior, audited privacy properties, or measured retrieval reliability.
- Use this source for content-addressing and decentralized retrieval vocabulary only.

## Failure Modes

- Content addressing does not mean a user is authorized to read, retain, or redistribute the content.
- Public peer-to-peer retrieval can create privacy, discovery, availability, moderation, and deletion complications.
- VCM revocation, taint, and source adequacy do not automatically propagate through content-addressed storage.
- Gateway access can reintroduce centralized availability, trust, logging, or policy assumptions.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use this note to ground the external content-addressed storage queue for hive artifact bundles, public caches, and reproducible references.
- Do not claim IPFS solves private hive memory, child privacy, deletion, source revocation, or authority control.

## Open Questions

- Which hive artifacts should be content-addressed, and which must remain local or encrypted?
- How should VCM revocation records interact with immutable or widely cached content identifiers?
- Should public project hives use content addressing for artifact bundles while keeping private context outside the public address space?
