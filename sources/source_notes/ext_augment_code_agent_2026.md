# Source Note: Augment Code Agent

| Field | Value |
|---|---|
| Source ID | `ext_augment_code_agent_2026` |
| Source title | Augment Code Agent Documentation |
| Ingestion date | 2026-08-08 |
| Source version / URL | https://docs.augmentcode.com/using-augment/agent |
| Citation label | Augment Documentation (2026), Using Agent |
| Published / updated | continuously updated / reviewed 2026-08-08 |
| Ingestion basis | Official documentation reviewed. No Augment execution, checkpoint recovery, permission test, or comparative evaluation was run. |

## Thesis

Augment provides a bounded example of the transition from an IDE side panel
that explains and proposes changes to an agent mode that plans, edits multiple
files, invokes terminal and MCP tools, records checkpoints, exposes diffs, and
can pause for approval. The relevant lesson is not that side panels are obsolete;
it is that one visual surface can carry multiple authority modes.

## Mechanisms

- Chat proposes or applies selected changes, while Agent implements multi-step work.
- Quick Ask constrains the system to read-only tools.
- Agent and Agent Auto distinguish approval-paused from more independent execution.
- Diffs, terminal output, integration results, checkpoints, stop, and steering controls support review and recovery.

## Evidence And Limits

- Official documentation describes the listed modes and controls.
- This repository did not run the product or verify checkpoint, approval, isolation, or recovery behavior.
- Product documentation does not establish complete mediation, correctness, productivity, or safe autonomy.

## Failure Modes

- A visual mode switch can conceal a material authority change.
- Checkpoints can be treated as complete rollback even when external effects escape workspace restoration.

## Claims To Add Or Update

- Use Augment to distinguish chat, read-only inquiry, approval-paused execution, and automatic execution within one interface.
- Preserve the boundary between workspace checkpoints and effect-complete recovery.

## Book Chapters Supported

- `ai-work-surfaces-agent-harnesses-and-organizational-absorption`
- `runtime-adapters-tool-permissions-and-human-approval`

## Open Questions

- Can mode transitions be represented as explicit authority changes rather than interface state alone?
- Which artifacts must survive when work moves from chat to agent mode and back?
