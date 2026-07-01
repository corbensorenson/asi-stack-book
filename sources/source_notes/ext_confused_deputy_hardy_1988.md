# Source Note: The Confused Deputy

| Field | Value |
|---|---|
| Source ID | `ext_confused_deputy_hardy_1988` |
| Source title | The Confused Deputy: (or why capabilities might have been invented) |
| Ingestion date | 2026-07-01 |
| Source version / URL | ACM DOI record, https://dl.acm.org/doi/10.1145/54289.871709 |
| Citation label | Hardy (1988), The Confused Deputy |
| Published / updated | 1988-10-01 / 1988-10-01 |
| DOI | 10.1145/54289.871709 |
| Ingestion basis | Public ACM metadata and public instructional mirrors inspected for the confused-deputy external-grounding queue; article not vendored into this repository and no capability system or runtime adapter reproduced. |

## Thesis

The confused-deputy problem is the classic external comparator for authority laundering: one program or service is induced to exercise its own broader authority on behalf of a lower-authority requester. It belongs in System Boundaries and Runtime Adapters because the ASI Stack's authority records are designed to keep the requester's ceiling attached to tool and handoff actions.

## Mechanisms

- Separate an object's designation from the authority needed to affect it.
- Expose the failure that occurs when a deputy uses its own authority instead of the requester's authority.
- Motivate capability-style designs that bind designation and permission more tightly than ambient-authority designs.
- Treat authority provenance as part of the handoff, not as hidden state inside the called tool.

## Evidence

- The source analyzes a classic systems-security failure pattern and capability-security motivation.
- This repository has not implemented the original system, reproduced a capability operating system, or run a live confused-deputy exploit.
- Use this source as external literature for authority-boundary vocabulary, not as proof that ASI Stack runtime adapters resist confused-deputy attacks.

## Failure Modes

- A model or planning layer invokes a tool whose raw authority exceeds the caller's grant.
- A tool treats a user-supplied target, path, URL, source, or handle as sufficient authority to act.
- A runtime adapter checks its own credential but not the caller's authority ceiling, delegation chain, expiry, or effect receipt.
- A successful tool call is later mistaken for evidence that the route was authorized.

## Book Chapters Supported

- `system-boundaries-and-authority` (System Boundaries and Authority)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)

## Claims To Add Or Update

- Use this source to name the confused-deputy lineage behind the ASI Stack's caller-ceiling, delegation-chain, and effect-receipt requirements.
- Keep support state at `argument` until a runtime adapter, approval service, or authority harness demonstrates the relevant denial behavior under recorded commands.
- Do not claim object-capability security, deployed tool enforcement, or confused-deputy resistance from this source note alone.

## Open Questions

- Which runtime-adapter fixture should first model a requester-supplied target that would be valid for the tool but invalid for the requester?
- Should authority receipts require an explicit "authority source" field distinguishing requester, tool, session, project, and governance grants?
- What live tool-call trace would be public-safe enough to test confused-deputy denial without exposing secrets or private paths?
