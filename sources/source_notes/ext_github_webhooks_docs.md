# Source Note: Webhook Events and Payloads

| Field | Value |
|---|---|
| Source ID | `ext_github_webhooks_docs` |
| Source title | Webhook events and payloads |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://docs.github.com/en/webhooks/webhook-events-and-payloads |
| Citation label | GitHub Docs (2026), Webhook events and payloads |
| Published / updated | unknown / 2026 |
| Ingestion basis | Official GitHub documentation inspected for the artifact-steward external literature queue; no webhook endpoint was created from this repository. |

## Thesis

GitHub webhooks are a practical event substrate for artifact steward agents: repository and organization events can trigger steward intake, but every event payload must be treated as typed, tainted input rather than trusted control text.

## Mechanisms

- Subscribe to selected repository, organization, and app events.
- Receive event names, delivery identifiers, sender/repository context, payload data, and signature headers.
- Use event-specific permissions and availability constraints.
- Respect payload limits and delivery-validation requirements.

## Evidence

- The official docs enumerate event types, payload fields, delivery headers, signature headers, and payload caps.
- This repository has not configured webhooks, validated signatures, processed events, or run a steward bot.
- Use this source to ground event-driven project automation and its typed-intake boundary.

## Failure Modes

- Issue bodies, comments, PR descriptions, and event payloads can become prompt-injection surfaces.
- Webhook delivery authenticity does not make event content semantically safe.
- Broad subscriptions can expand attack surface and operator burden.

## Book Chapters Supported

- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)

## Claims To Add Or Update

- Use this note to source the event-driven project-automation substrate for steward intake.
- Pair this source with the agentic-workflow-injection note before discussing untrusted event handling.

## Open Questions

- What minimal webhook fixture should mark issue text as tainted before any agent reads it?
- Which events should a minimal steward ignore by default?
- How should webhook signatures be represented in `StewardActionDecision` evidence refs?
