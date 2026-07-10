# Source Note: Agent2Agent Protocol Specification, version 0.3.0

| Field | Value |
|---|---|
| Source ID | `ext_a2a_protocol_0_3_0` |
| Source title | Agent2Agent Protocol Specification, version 0.3.0 |
| Ingestion date | 2026-07-10 |
| Source version / URL | Version 0.3.0, https://a2a-protocol.org/v0.3.0/specification/ |
| Citation label | A2A Protocol (v0.3.0), Specification |
| Published / updated | Versioned specification / inspected 2026-07-10 |
| Ingestion basis | Official specification inspected for agent cards, capability discovery, delegated tasks, message/artifact exchange, transport requirements, and interoperability framing. No ASI Stack A2A peer, delegated task, credential, payment, or effect route ran. |

## Thesis

A2A defines a common interaction model for independent, potentially opaque AI
agent systems to discover capabilities, delegate work, exchange context and
artifacts, and manage tasks. Interoperability does not establish a peer's
identity, authority, reliability, truthfulness, security, or safety.

## Mechanisms

- Publish an Agent Card with service URLs and declared capabilities for discovery.
- Exchange task and message state over a selected HTTP(S)-based transport.
- Define JSON-RPC, gRPC, and HTTP+JSON/REST transport options with normative
  message and behavior requirements where a transport is implemented.
- Keep remote agent internals opaque while allowing a bounded task interaction.

## Evidence

- The official specification defines the stated discovery, task, transport, and
  interoperability mechanisms.
- It does not provide a complete identity, delegated-authority, economic
  settlement, truthful-result, or execution-safety guarantee.
- This repository has not deployed, interoperated with, or evaluated an A2A
  agent, task, card, artifact, or transport.

## Failure Modes

- Treating an Agent Card's self-description as verified competence or authority.
- Forwarding a principal's approval or credential across a delegation chain
  without scope, expiry, audience, and revocation checks.
- Treating task completion state or an exchanged artifact as proof of a correct
  result or authorized external effect.
- Losing residual, dispute, or accountability information between a remote task
  and the local approval or release decision.

## Book Chapters Supported

- `inter-stack-protocols-identity-and-economic-exchange` (Inter-Stack Protocols, Identity, and Economic Exchange)

## Claims To Add Or Update

- Use A2A as a scoped comparator for agent discovery, remote task routing,
  transport choice, and exchanged task/artifact records.
- Require a governed stack to attach local identity, authority, receipt,
  residual, and revocation checks rather than inheriting them from an Agent Card.
- Do not claim local A2A conformance, peer verification, delegation security,
  task correctness, payment, or safety.

## Open Questions

- Which Agent Card fields should be treated as discoverable declarations rather
  than trusted authority inputs?
- What public-safe fixture can show that a revoked or audience-mismatched
  delegated request cannot reach a local runtime adapter?
