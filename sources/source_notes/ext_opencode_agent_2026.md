# Source Note: OpenCode Agent

| Field | Value |
|---|---|
| Source ID | `ext_opencode_agent_2026` |
| Source title | OpenCode Open-Source Coding Agent |
| Ingestion date | 2026-08-08 |
| Source version / URL | `anomalyco/opencode` commit `38e10eb1408feb700021b8e8766fb0ab41bf84e2`; https://opencode.ai/docs |
| Citation label | OpenCode contributors (2026), OpenCode |
| Published / updated | repository revision reviewed 2026-08-08 |
| Ingestion basis | Official documentation and official repository identity reviewed. The software and its tests were not run. |

## Thesis

OpenCode is a current open-source comparator for a model-provider-flexible
coding harness available through terminal, desktop, and IDE surfaces. Its
explicit plan/build modes, project instruction file, tool use, undo/redo, and
share controls show how harness policy and interaction state can remain distinct
from the selected model provider.

## Mechanisms

- Terminal, desktop, and IDE surfaces operate against a project.
- `AGENTS.md` carries repository-specific instructions.
- Plan mode disables changes; build mode can implement them.
- Undo, redo, and opt-in sharing expose recovery and collaboration controls.

## Evidence And Limits

- The reviewed sources document these mechanisms at the pinned revision.
- This repository did not execute OpenCode, inspect its runtime, or test provider parity, permissions, undo integrity, privacy, or task quality.
- Provider flexibility is an interface property, not proof that models or deployments are equivalent.

## Failure Modes

- Plan/build mode can be mistaken for a complete permission system.
- Model-provider substitution can change behavior while the harness identity appears stable.

## Claims To Add Or Update

- Use OpenCode as a pinned open-source comparator for provider-flexible, multi-surface agent work.
- Keep provider portability distinct from behavioral equivalence and authority portability.

## Book Chapters Supported

- `ai-work-surfaces-agent-harnesses-and-organizational-absorption`
- `runtime-adapters-tool-permissions-and-human-approval`

## Open Questions

- Which harness guarantees can remain invariant when the model provider changes?
- What must a shared-session receipt disclose without leaking sensitive project context?
