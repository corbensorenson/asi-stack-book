# Source Note: Anthropic Claude Code

| Field | Value |
|---|---|
| Source ID | `ext_anthropic_claude_code_2026` |
| Source title | Claude Code Overview and Agentic Harness Documentation |
| Ingestion date | 2026-08-08 |
| Source version / URL | https://code.claude.com/docs/en/how-claude-code-works |
| Citation label | Anthropic (2026), Claude Code Documentation |
| Published / updated | continuously updated / reviewed 2026-08-08 |
| Ingestion basis | Official documentation reviewed. Claude Code was not installed, executed, benchmarked, or security-tested for this intake. |

## Thesis

Claude Code explicitly describes the harness as the tools, context management,
and execution environment around a model. Its gather-context, act, verify loop
and its availability through terminal, IDE, desktop, web, remote control, and
automation make it a direct comparator for work-surface evolution and for the
distinction between model capability and system capability.

## Mechanisms

- File, search, execution, web, and code-intelligence tools create an action loop around the model.
- Project instructions, memory, skills, MCP, hooks, subagents, and teams expand persistence and orchestration.
- Checkpoints, permissions, interruption, and steering provide partial human-control surfaces.
- Local, cloud, and remote-control execution place artifacts and side effects under different operators.

## Evidence And Limits

- Official documentation describes the mechanisms and calls Claude Code an agentic harness.
- Documentation review does not establish complete tool mediation, task success, safe autonomy, or organizational substitution.
- Features and maturity states can change; no historical launch sequence is inferred beyond the reviewed record.

## Failure Modes

- Model capability can be conflated with harness tools, context, permissions, and environment.
- Subagent or team delegation can widen practical reach without a matching accountability record.

## Claims To Add Or Update

- Adopt the explicit model-versus-harness distinction in the work-surface chapter.
- Require delegated workers to inherit no authority beyond the exact parent task.

## Book Chapters Supported

- `ai-work-surfaces-agent-harnesses-and-organizational-absorption`
- `runtime-adapters-tool-permissions-and-human-approval`

## Open Questions

- Which loop state must remain portable across interfaces and execution environments?
- How should subagent and team delegation preserve authority ceilings and accountable ownership?
