# Source Note: Nous Research Hermes Agent

| Field | Value |
|---|---|
| Source ID | `ext_hermes_agent_2026` |
| Source title | Hermes Agent: Learning, Memory, Tools, and Security Architecture |
| Ingestion date | 2026-08-08 |
| Source version / URL | `NousResearch/hermes-agent` commit `238351a60ce689e1c460fabf5b3f50e3b06b44bd`; https://github.com/NousResearch/hermes-agent |
| Citation label | Nous Research (2026), Hermes Agent |
| Published / updated | repository created 2025-07-22 / revision reviewed 2026-08-08 |
| License | MIT, as identified by the official repository |
| Ingestion basis | Official repository README and canonical architecture, skills, persistent-memory, and security documentation reviewed. The software and its tests were not run here. |

## Thesis

Hermes Agent is a current implementation comparator for separating compact
always-present memory, searchable session history, on-demand procedural skills,
tool execution, and human-gated mutation. It demonstrates that an agent can
write reusable procedures while also exposing why procedure creation is not by
itself evidence of correctness or safe self-improvement.

## Mechanisms

- The agent loop coordinates provider selection, prompt construction, tool
  execution, retry, fallback, compression, callbacks, and persistence.
- Persistent `MEMORY.md` and `USER.md` snapshots are bounded and distinct from
  SQLite/FTS5 session search over historical messages.
- Skills use progressive disclosure and can be created, patched, rewritten, or
  deleted by the agent as procedural memory.
- An optional skill-write approval mode stages mutations for durable diff review
  before application; skill installation also records source hashes and scan
  findings.
- Security controls include user authorization, dangerous-command approval,
  file-write restrictions, container isolation, credential filtering, context
  scanning, cross-session isolation, and input validation.

## Evidence

- The reviewed official documentation specifies the listed architecture and
  policy surfaces at the pinned revision.
- The documentation distinguishes bounded always-in-context memory from
  on-demand session search and longer procedural skills.
- This repository did not run Hermes Agent, evaluate learned procedures, test
  poisoning resistance, inspect real approval decisions, or reproduce security,
  memory, cost, or utility results.

## Failure Modes

- A successful trajectory can encode a brittle or unsafe procedure.
- Direct skill writes can bypass independent regression, readiness, and rollback
  review; optional write approval reduces but does not remove that risk.
- Frozen prompt memory can preserve stale, contradictory, or poisoned content.
- Command-pattern approval and container isolation are partial controls, not a
  proof of complete effect mediation.

## Book Chapters Supported

- `ai-work-surfaces-agent-harnesses-and-organizational-absorption`
- `procedural-memory-and-cognitive-loop-closure`
- `durable-semantic-memory-and-knowledge-lattices`
- `runtime-adapters-tool-permissions-and-human-approval`

## Claims To Add Or Update

- Use Hermes as a concrete procedural-memory comparator: trajectory-derived
  knowledge can become a skill, but safe promotion additionally needs evidence,
  version identity, regression, approval, rollback, and retirement contracts.
- Preserve the distinction among compact semantic memory, searchable history,
  and load-on-demand procedures.

## Open Questions

- What evidence threshold should govern autonomous skill creation and patching?
- How should a staged skill mutation bind the trajectory, model, tools, tests,
  reviewer, rollback state, and future revalidation trigger?
- Which memory facts require temporal validity, contradiction, provenance, and
  downstream-use receipts beyond injection scanning?
