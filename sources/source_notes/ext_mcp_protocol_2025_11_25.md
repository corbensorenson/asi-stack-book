# Source Note: Model Context Protocol Specification, revision 2025-11-25

| Field | Value |
|---|---|
| Source ID | `ext_mcp_protocol_2025_11_25` |
| Source title | Model Context Protocol Specification, revision 2025-11-25 |
| Ingestion date | 2026-07-10 |
| Source version / URL | Released revision 2025-11-25, https://modelcontextprotocol.io/specification/2025-11-25 |
| Citation label | Model Context Protocol (2025), Specification revision 2025-11-25 |
| Refresh basis | Official MCP specification/blog checked on 2026-07-10. The 2026-07-28 revision was still labeled a release candidate, so this note keeps 2025-11-25 as the latest released revision. |

## Thesis

MCP provides a versioned agent-to-tool context protocol with negotiated
capabilities and modular lifecycle, authorization, elicitation, and task
surfaces. Protocol conformance does not establish principal identity,
delegated authority, tool truth, effect safety, or task correctness.

## Mechanisms

- Version and negotiate client/server capabilities and lifecycle behavior.
- Keep authorization and discovery rules distinct from tool/resource/prompt
  message shape.
- Support bounded interactive elicitation and longer-running task surfaces
  without treating either as implicit effect authority.
- Evolve through dated revisions and explicit compatibility boundaries.

## Evidence and Limits

The official project identifies 2025-11-25 as a released specification and a
2026-07-28 revision as a release candidate as of this inspection. This book has
not implemented or audited an MCP client, server, authorization flow,
elicitation exchange, task, tool invocation, or deployment.

## Failure Modes

- Treating negotiated capability as permission for a material effect.
- Treating protocol-valid output as a truthful or independently observed receipt.
- Following a release-candidate surface as if it were the latest stable contract.
- Losing principal, audience, expiry, revocation, residual, or rollback state at the protocol boundary.

## Book Chapters Supported

- `inter-stack-protocols-identity-and-economic-exchange`

## Claims To Add Or Update

- Use the latest released revision for protocol positioning while recording the
  newer release candidate as volatile context only.
- Keep protocol shape separate from authority, evidence, effect observation,
  residuals, and rollback.

## Open Questions

- Which 2026-07-28 release-candidate features will remain in the final revision?
- What bounded conformance fixture can test version, authority, and effect-receipt separation without implying tool trust?
