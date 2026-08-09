# Source Note: elizaOS Agent Runtime

| Field | Value |
|---|---|
| Source ID | `ext_elizaos_agent_runtime_2026` |
| Source title | elizaOS Agent Runtime and Scenario Runner |
| Ingestion date | 2026-08-08 |
| Source version / URL | `elizaOS/eliza` commit `1232c982c1594d2438a8a53b02e41a9ba86664aa`; https://github.com/elizaOS/eliza |
| Citation label | elizaOS contributors (2026), elizaOS Agent Runtime |
| Published / updated | repository created 2024-07-09 / revision reviewed 2026-08-08 |
| License | MIT, as identified by the official repository |
| Ingestion basis | Official repository README, core-runtime README and documentation, scenario-runner README, security architecture, and sandbox guide reviewed. The software and its tests were not run here. |

## Thesis

elizaOS is a current implementation comparator for a modular agent runtime in
which plugins contribute actions, providers, evaluators, services, models,
routes, events, tests, and views. A particularly valuable contribution to this
book is its concrete separation among context supply, action execution,
post-turn evaluation, long-running services, diagnostic scenarios, and
provider qualification.

## Mechanisms

- `AgentRuntime` owns lifecycle, plugin loading, the message loop, memory, state,
  and component registration.
- Actions pair applicability validation with an execution handler; providers
  supply context; evaluators process conversation data and memory; services own
  background integrations.
- The scenario runner drives a real runtime through message, action, API, and
  scheduler turns with per-turn and final assertions.
- Provider-qualified evidence is explicitly separated from ordinary in-process
  diagnostics: an external controller closes a content-hashed manifest,
  observes production ingress and durable effects, and verifies signed results.
- Security and sandbox documentation identify guarded network, command,
  configuration, plugin-install, host-access, and execution boundaries.

## Evidence

- The reviewed repository contains canonical documentation and implementation
  surfaces for the mechanisms above at the pinned revision.
- The scenario-runner documentation explicitly separates ordinary in-process
  diagnostics from provider-qualified evidence and conservatively records
  exactly-once as false while idempotency and readback reduce ambiguity.
- This repository did not install elizaOS, execute its scenario runner, inspect
  deployed traces, reproduce tests, or audit its security controls.

## Failure Modes

These are general risks when any modular agent runtime is composed into a
larger governed system; they are not findings that elizaOS exhibits each
failure.

- Component composition needs an end-to-end record joining authority, effect,
  observation, and terminal disposition when the deployment requires it.
- In-process assertions and provider-qualified evidence retain distinct roles.
- Sandbox and permission guarantees depend on the deployed enforcement path,
  so documentation review alone does not establish complete mediation.
- Rich trajectory capture benefits from explicit custody and redaction
  boundaries when sensitive context or externally observed effects are in
  scope.

## Book Chapters Supported

- `ai-work-surfaces-agent-harnesses-and-organizational-absorption`
- `runtime-adapters-tool-permissions-and-human-approval`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Use elizaOS as an implementation comparator for typed runtime components and
  for the distinction between diagnostic scenario execution and independently
  qualified provider evidence.
- Preserve the book's end-to-end requirement that component validation,
  permission, execution, observation, and promotion remain separate records.

## Open Questions

- Which plugin lifecycle events need one cross-component turn identity?
- What external observer set is sufficient for each effect family?
- How should scenario qualification bind deployment, principal, connector,
  capability, durable readback, cost, and unresolved residuals?
