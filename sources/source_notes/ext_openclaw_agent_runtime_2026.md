# Source Note: OpenClaw Agent Runtime

| Field | Value |
|---|---|
| Source ID | `ext_openclaw_agent_runtime_2026` |
| Source title | OpenClaw Gateway, Agent Runtime, ACP, and Self-Learning Architecture |
| Ingestion date | 2026-08-08 |
| Source version / URL | `openclaw/openclaw` commit `e4309e0cc7a74f0c82d572eb47befe78211c6be5`; https://github.com/openclaw/openclaw |
| Citation label | OpenClaw contributors (2026), OpenClaw Agent Runtime |
| Published / updated | repository created 2025-11-24 / revision reviewed 2026-08-08 |
| License | MIT, as identified by the official repository README |
| Ingestion basis | Official repository README and canonical gateway, agent-loop, ACP-agent, sandbox/tool-policy/elevated, memory, and self-learning documentation reviewed. The software and its tests were not run here. |

## Thesis

OpenClaw is a current implementation comparator for a single-operator gateway
that joins channels, clients, device nodes, sessions, tools, external agent
harnesses, audit events, and skill learning. Its clearest architectural lessons
are that identity namespaces and enforcement owners must remain explicit, and
that sandbox location, tool availability, approval, and elevated execution are
different controls.

## Mechanisms

- A long-lived Gateway owns messaging surfaces and exposes a typed WebSocket
  request, response, and event protocol with device identity and pairing.
- The per-session agent loop validates and resolves session identity, serializes
  work, streams lifecycle/tool/assistant events, locks transcript writes, and
  records bounded metadata-only audit projections.
- ACP sessions delegate work to external coding harnesses while retaining a
  distinct OpenClaw session key and a harness-local resume identifier.
- OpenClaw checks ACP feature, agent, session-owner, channel, and delivery policy,
  while the external backend owns authorization for loading its upstream resume
  identifier; OpenClaw's sandbox does not wrap ACP harness execution.
- Autonomous experience review sees bounded trajectory evidence, may create one
  hash-bound pending skill proposal, cannot apply its own proposal, and uses
  security scan, stale-target rejection, rollback metadata, and lifecycle rules
  on the apply path.

## Evidence

- The reviewed official documentation specifies these gateway, session, ACP,
  policy, audit, memory, and self-learning surfaces at the pinned revision.
- The documentation explicitly separates sandbox placement, tool policy, and
  elevated execution, and documents the external-harness confinement residual.
- This repository did not install OpenClaw, inspect runtime traces, execute ACP,
  evaluate learned skills, or reproduce security, reliability, or benchmark
  results.
- `ext_claw_swe_bench_2026` remains a separate benchmark source; no result from
  that paper is transferred to this implementation note.

## Failure Modes

- A channel session key, local session ID, run ID, ACP session key, and harness
  resume ID can be conflated, breaking custody or authorization.
- A host-run external harness can sit outside the parent runtime's sandbox.
- Tool allowlists do not make a permitted shell tool read-only or side-effect
  complete.
- Metadata-only audit projections improve privacy but cannot reconstruct omitted
  prompts, arguments, results, or unobserved external effects by themselves.
- Evidence-reviewed skill proposals can still overfit, preserve evaluator error,
  or regress on untested workloads.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`
- `artifact-graphs-audit-logs-and-replay`
- `inter-stack-protocols-identity-and-economic-exchange`
- `procedural-memory-and-cognitive-loop-closure`

## Claims To Add Or Update

- Require explicit translation records between local session identity and
  external harness identity; neither namespace grants the other's authority.
- Treat sandbox placement, tool availability, approval, and elevation as
  independent policy dimensions with separate receipts.
- Use the isolated, hash-bound proposal path as a concrete comparator for
  governed procedure learning while retaining independent regression and
  readiness requirements.

## Open Questions

- Which terminal disposition joins a gateway run, session generation, external
  harness turn, tool effects, delivery, and durable transcript state?
- How should the parent verify confinement and actual effects when an external
  harness owns execution authorization?
- What held-out campaign is required before a learned procedure becomes a
  default capability rather than a pending or canary artifact?
