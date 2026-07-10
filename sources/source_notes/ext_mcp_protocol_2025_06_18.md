# Source Note: Model Context Protocol Specification, revision 2025-06-18

| Field | Value |
|---|---|
| Source ID | `ext_mcp_protocol_2025_06_18` |
| Source title | Model Context Protocol Specification, revision 2025-06-18 |
| Ingestion date | 2026-07-10 |
| Source version / URL | Protocol Revision 2025-06-18, https://modelcontextprotocol.io/specification/2025-06-18/basic/index |
| Citation label | Model Context Protocol (2025), Specification revision 2025-06-18 |
| Published / updated | 2025-06-18 / 2025-06-18 |
| Ingestion basis | Official specification inspected for base JSON-RPC messages, lifecycle management, capability negotiation, session control, modular client/server features, and schema source-of-truth framing. No ASI Stack MCP client, server, session, authorization flow, or tool action ran. |

## Thesis

MCP provides a modular protocol boundary for clients and servers to negotiate
capabilities and exchange structured interactions. It is a communication
specification, not a general identity, authorization, task-completion, payment,
or safety guarantee.

## Mechanisms

- Define a base JSON-RPC message layer and lifecycle management for connection
  initialization, capability negotiation, and session control.
- Separate optional server features, client features, authorization framing, and
  utilities so implementations can state what they actually support.
- Publish TypeScript and generated JSON schemas as the protocol's message and
  structure source of truth.

## Evidence

- The official specification defines the stated protocol layers and schema
  source-of-truth boundary.
- It does not prescribe a complete cross-stack identity, delegation, receipt,
  settlement, or governance system.
- This repository has not implemented, exercised, secured, or audited an MCP
  client/server exchange.

## Failure Modes

- Treating capability negotiation as authority to perform an effect.
- Passing an unbound principal, credential, budget, or policy decision through a
  structurally valid message.
- Treating an MCP response as evidence that a remote claim, artifact, or task
  result is true.
- Assuming a schema or protocol revision makes an implementation secure or
  interoperable in its actual deployment context.

## Book Chapters Supported

- `inter-stack-protocols-identity-and-economic-exchange` (Inter-Stack Protocols, Identity, and Economic Exchange)

## Claims To Add Or Update

- Use MCP as a scoped comparator for versioned message, lifecycle, capability,
  session, and schema fields at the agent-to-tool boundary.
- Require a cross-stack contract to bind protocol shape separately from
  principal, authority, preconditions, receipt, residual, and budget records.
- Do not claim local MCP conformance, authorization correctness, tool security,
  task completion, identity verification, payment, or safety.

## Open Questions

- Which MCP messages should a public-safe inter-stack fixture model without
  implying that a remote tool is trustworthy?
- How should a capability-negotiation result expire or be invalidated after a
  policy, credential, artifact, or endpoint change?
