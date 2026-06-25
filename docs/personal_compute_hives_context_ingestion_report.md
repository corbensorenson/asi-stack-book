# Personal Compute Hives Context Ingestion Report

Date: 2026-06-25

## Provenance

- Local browser discussion packet: `sources/inbox/personal_compute_hives_browser_note_2026-06-25/`
- Public chapter added: `personal-compute-hives-and-federated-edge-intelligence`
- Placement: Part III - Routing, Compression, Representation, and Substrates, after `moecot-runtime-and-multi-core-orchestration`

## Public handling

The packet was treated as author-intent and planning context only. The public chapter does not quote the private browser discussion verbatim, does not cite it as evidence, and does not use it to promote any claim support state.

## Material extracted

- The need for a governed personal/project compute substrate spanning phones, laptops, desktops, NAS devices, old machines, family/project devices, and temporary rented nodes.
- The distinction between portals, workers, stores, rented nodes, project hives, and federation leases.
- The core invariant that reachability is not authority.
- The need for device resource cards, job contracts, policy-first scheduling, approval receipts, revocation paths, and audit replay.
- Failure modes around botnet dynamics, surveillance, data leakage, wrong-device scheduling, identity confusion, and unmanaged memory accumulation.

## Evidence boundary

- Record-shape schemas and fixtures were later added for `DeviceResourceCard`, `PortalCard`, `HiveJobContract`, `HiveJobBid`, `HiveSchedulingDecision`, `HiveApprovalReceipt`, and `HiveFederationLease`; narrow finite Lean predicates were implemented for policy-before-optimization admission, faster-forbidden-node rejection, approval gating, and federation-lease boundaries.
- No personal hive implementation, scheduler, network overlay, rented-node sandbox, family-governance policy engine, live device registry, or behavioral scheduling test was run.
- External source records and conservative source notes now exist for selected adjacent systems: Tailscale, Kubernetes, K3s, Nomad, Ray Core, BOINC, Syncthing, IPFS, Akash, Golem, and GitHub self-hosted runners.
- Those external notes ground nearby tooling patterns only; they do not prove that the proposed personal hive exists, is safe, or has been tested.
- The chapter remains `Design rationale` with `argument` support.

## Follow-up queue

- Add public source records and source notes for remaining substrate topics: secret-management systems, sandbox runtimes, family safety/tutoring systems, local-first databases, and privacy-preserving computation.
- Add behavioral scheduler and rented-node denial tests before claiming any policy-first scheduling behavior beyond finite record predicates.
