# Source Note: OpenAI Codex Work Surfaces

| Field | Value |
|---|---|
| Source ID | `ext_openai_codex_work_surfaces_2026` |
| Source title | OpenAI Codex CLI, IDE, Cloud, and Agent Documentation |
| Ingestion date | 2026-08-08 |
| Source version / URL | official docs at https://learn.chatgpt.com/docs/codex/cli and `openai/codex` commit `dd43a9967ff19ce2b96282d2fd5cbdd2022a9b11` |
| Citation label | OpenAI (2026), Codex Documentation and CLI |
| Published / updated | continuously updated / revision reviewed 2026-08-08 |
| Ingestion basis | Official OpenAI documentation and official open-source CLI repository identity reviewed. Codex behavior or performance was not evaluated for this intake. |

## Thesis

Codex is a current comparator for a coding-agent harness distributed across
local terminal, IDE, cloud, desktop, automation, and integration surfaces. The
important architectural move is from answering about code to holding project
context, editing artifacts, running installed tools, preserving task state, and
supporting repeatable or asynchronous work under configurable permissions.

## Mechanisms

- The CLI inspects repositories, edits files, runs local tools, and composes with scripts and CI.
- IDE and cloud surfaces relocate interaction and execution without making them the same custody boundary.
- Project instructions, skills, plugins, MCP, hooks, worktrees, permissions, sandboxing, review, and non-interactive execution extend the harness around the model.
- Local, cloud, and remote work require explicit treatment of environment, identity, secrets, effects, and returned artifacts.

## Evidence And Limits

- Official documentation describes these current product and developer surfaces.
- The pinned repository identifies one revision of the open-source CLI, not every hosted component.
- This source note does not import any Codex benchmark, safety, productivity, or correctness result.
- Product capabilities can change; the chapter uses them as dated landmarks, not a permanent taxonomy.

## Failure Modes

- Local, cloud, IDE, and automated runs can be conflated despite different custody and permission boundaries.
- CLI source inspection can be overgeneralized to hosted components that were not inspected.

## Claims To Add Or Update

- Use Codex as a multi-surface coding-agent landmark and require explicit identity and authority translation among surfaces.
- Keep official capability descriptions separate from reproduced behavior or outcomes.

## Book Chapters Supported

- `ai-work-surfaces-agent-harnesses-and-organizational-absorption`
- `runtime-adapters-tool-permissions-and-human-approval`

## Open Questions

- Which records preserve custody when a local interactive task becomes cloud or scheduled work?
- How should permission profiles and receipts travel across Codex surfaces without authority widening?
