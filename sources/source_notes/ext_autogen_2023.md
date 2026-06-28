# Source Note: AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation

| Field | Value |
|---|---|
| Source ID | `ext_autogen_2023` |
| Source title | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2308.08155, https://arxiv.org/abs/2308.08155 |
| Citation label | Wu et al. (2023), AutoGen |
| Published / updated | 2023-08-16 / 2023-10-03 |
| DOI | 10.48550/arXiv.2308.08155 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the planning/agent-orchestration literature queue; framework code, example applications, and evaluations are not imported into this repository. |

## Thesis

AutoGen belongs in the planning, labor, runtime-adapter, and artifact-graph chapters as an external reference for multi-agent conversation orchestration. It helps the ASI Stack compare typed job contracts and runtime receipts against a framework vocabulary where agents converse, use tools, include humans, and follow programmable interaction patterns.

## Mechanisms

- Build LLM applications from multiple conversable agents.
- Let agents operate with combinations of LLMs, human inputs, and tools.
- Define interaction behavior with natural language or code.
- Use a generic framework across tasks with different application complexity and model capacity.
- Evaluate example applications across domains such as coding, question answering, online decision-making, mathematics, and operations research.

## Evidence

- The source reports framework design and empirical studies in its own example applications.
- This repository has not run AutoGen, imported its examples, reproduced its evaluations, or compared it to MoECOT, Labor OS, or PlanForge on shared tasks.
- Use the source as external orchestration vocabulary, not as evidence that ASI Stack multi-agent execution works.

## Failure Modes

- Multi-agent conversation can hide authority transfer, tool permission, and evidence provenance unless every action has a receipt.
- Natural-language interaction patterns can blur typed job boundaries and make replay difficult.
- Framework success on example applications cannot be imported into ASI Stack runtime, labor, or artifact-governance claims without reproduced traces.

## Book Chapters Supported

- `planning-as-a-control-layer` (Planning as a Control Layer)
- `labor-os-and-typed-jobs` (Labor OS and Typed Jobs)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `artifact-graphs-audit-logs-and-replay` (Artifact Graphs, Audit Logs, and Replay)

## Claims To Add Or Update

- Use this note to compare ASI Stack typed execution surfaces against multi-agent conversation orchestration.
- Do not claim AutoGen behavior, benchmark performance, or tool-safety properties for the ASI Stack.
- Keep support state at `argument` until imported traces, fixtures, harnesses, or accepted evidence transitions exist.

## Open Questions

- Which Labor OS typed-job fixture can model a multi-agent conversation without losing authority and evidence fields?
- What replay log should distinguish useful agent collaboration from uncontrolled delegation?
- How should human-in-the-loop conversation patterns map to approval receipts and residual ledgers?
