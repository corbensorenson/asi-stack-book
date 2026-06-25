# Source Note: Syncthing

| Field | Value |
|---|---|
| Source ID | `ext_syncthing_home` |
| Source title | Syncthing |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://syncthing.net/ |
| Citation label | Syncthing Project Site |
| Published / updated | unknown / unknown |
| Ingestion basis | Official project site inspected for the Personal Compute Hives external literature queue; no Syncthing instance was configured from this repository. |

## Thesis

Syncthing is relevant to hive memory and data placement because it demonstrates user-controlled synchronization across devices with explicit device identity and encrypted transport. It does not solve context governance by itself.

## Mechanisms

- Synchronize files continuously between two or more computers.
- Keep storage location under user control rather than a central provider.
- Authenticate devices with cryptographic identity.
- Protect communication with encrypted transport.
- Expose a documented open protocol and open-source implementation.

## Evidence

- The official site describes continuous synchronization, authenticated devices, encrypted communication, and user choice over where data is stored.
- This repository has not deployed Syncthing, synced files, audited transport security, or tested conflict behavior.
- Use this source for data mobility and local-first memory vocabulary only.

## Failure Modes

- File synchronization can spread tainted, revoked, private, or stale context if VCM policy is absent.
- Sync success does not mean semantic freshness or source adequacy.
- Device authentication does not imply every file is appropriate for every device.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use this note to ground the external data-mobility queue and the need for separate VCM placement rules.
- Do not claim that sync tools solve memory quality, child privacy, or evidence provenance.

## Open Questions

- How should VCM revocation propagate through synchronized folders?
- Should hive memory sync raw artifacts, summaries, embeddings, or evidence bundles by default?
- What conflict-resolution evidence should be recorded?
