# Source Note: Agent2Agent Protocol Specification, version 1.0.0

| Field | Value |
|---|---|
| Source ID | `ext_a2a_protocol_1_0_0` |
| Source title | Agent2Agent Protocol Specification, version 1.0.0 |
| Ingestion date | 2026-07-10 |
| Source version / URL | Latest released version 1.0.0, https://a2a-protocol.org/latest/specification/ |
| Citation label | A2A Protocol (v1.0.0), Specification |
| Refresh basis | Official specification inspected on 2026-07-10; it labels 1.0.0 as the latest released version and 0.3.0 as a previous version. |

## Thesis

A2A 1.0 defines a layered interaction model for independent opaque agents:
canonical data objects, abstract operations, and concrete protocol bindings.
Discovery and interoperability still do not establish peer competence,
identity truth, delegated authority, result truth, or safe execution.

## Mechanisms

- Publish Agent Cards and versioned discovery information.
- Exchange tasks, messages, parts, and artifacts through abstract operations.
- Bind operations through JSON-RPC, gRPC, or HTTP+JSON/REST while preserving
  canonical data semantics.
- Use explicit version negotiation, authorization scoping, interoperability
  testing, and security considerations.

## Evidence and Limits

The official specification labels 1.0.0 as the latest released version. This
repository has not run an A2A peer, card, task, message, artifact, binding,
authorization flow, interoperability test, or security evaluation.

## Failure Modes

- Treating an Agent Card as verified competence or authority.
- Treating task completion or artifact delivery as independent effect evidence.
- Forwarding credentials or approvals without audience, scope, expiry, and revocation checks.
- Assuming binding interoperability implies semantic agreement or safe action.

## Book Chapters Supported

- `inter-stack-protocols-identity-and-economic-exchange`

## Claims To Add Or Update

- Position A2A 1.0 as the current agent-to-agent comparator.
- Require local identity, authority, evidence, residual, dispute, and revocation
  controls around protocol-valid remote interactions.

## Open Questions

- Which A2A 1.0 binding gives the smallest public-safe interoperability fixture?
- How should a local stack invalidate Agent Card and delegated-task authority after policy or credential change?
