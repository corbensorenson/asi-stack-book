# Source Note: Oh My Pi Coding Agent

| Field | Value |
|---|---|
| Source ID | `ext_oh_my_pi_agent_2026` |
| Source title | Oh My Pi Terminal Coding Agent and Tool Harness |
| Ingestion date | 2026-08-08 |
| Source version / URL | `can1357/oh-my-pi` commit `896bf5f33e0b67bdd0cf951c82739a28e75d0823`; https://github.com/can1357/oh-my-pi |
| Citation label | Oh My Pi contributors (2026), Oh My Pi |
| Published / updated | repository revision reviewed 2026-08-08 |
| Ingestion basis | Official repository README and selected canonical documentation reviewed. The software, claims, and tests were not run or reproduced. |

## Thesis

Oh My Pi, commonly invoked as `omp`, is a current comparator for a terminal
coding harness that concentrates editing, code intelligence, shell, browser,
subagents, memory, provider switching, review, and collaboration into one work
surface. It illustrates both the leverage and trusted-computing-base growth that
follow when a harness absorbs more of the developer toolchain.

## Mechanisms

- Hash-anchored edits reject stale anchors before applying a patch.
- LSP, shell, browser, Python, review, subagent, and memory tools widen the loop.
- Provider abstraction and session handoff separate model selection from some harness state.
- Agent hub, advisor, hooks, and collaboration expose multi-agent and human-steering surfaces.

## Evidence And Limits

- The reviewed official repository documents these mechanisms at the pinned revision.
- Reported token, performance, security, or quality claims were not reproduced and are not imported.
- This repository did not run `omp`, inspect traces, test hash anchors, audit its sandbox, or evaluate collaboration privacy.
- A richer harness can increase leverage and attack surface simultaneously; neither outcome is assumed here.

## Failure Modes

- Integrated tool breadth can enlarge the trusted computing base and common failure surface.
- Model handoff, collaboration, or subagent fan-out can blur identity, context lineage, and authority.

## Claims To Add Or Update

- Use Oh My Pi as a pinned comparator for toolchain absorption into a terminal harness.
- Treat hash anchors, collaboration, provider handoff, and subagents as mechanisms to evaluate rather than reproduced guarantees.

## Book Chapters Supported

- `ai-work-surfaces-agent-harnesses-and-organizational-absorption`
- `runtime-adapters-tool-permissions-and-human-approval`

## Open Questions

- Which harness components belong inside the trusted computing base?
- How should model handoff preserve context lineage without transferring hidden authority?
