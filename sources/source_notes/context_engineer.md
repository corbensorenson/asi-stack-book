# Source Note: Context Engineer / Manhattan Protocol

| Field | Value |
|---|---|
| Source ID | `context_engineer` |
| Source title | Context Engineer / Manhattan Protocol |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1xXP364s9IZ4DFmRHTmBELviRQkJcQ55McIUokioRFdo |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/context_engineer.txt`; raw text is not published. |

## Thesis

Context Engineer treats context as an information supply chain. Instead of dumping retrieved text into a prompt, a governance module compiles, filters, sanitizes, clears, and delivers task-specific mission briefs to workers under need-to-know constraints.

## Mechanisms

- Place a governor between the planner and worker that compiles the execution environment.
- Maintain layered memory: raw archive, semantic web, and hot cache.
- Use briefer agents to compress raw logs into task-specific mission briefs.
- Deliver context as structured objects rather than untyped prompt strings.
- Use clearance levels, context shards, memory masks, and allowed-tool lists.
- Spawn Digital SCIFs for sensitive tasks, inject ephemeral context, zero raw context after use, and commit only sanitized outputs.
- Enforce information-flow control, outgoing secret scans, and read/write policies.

## Evidence

- The source contains multiple versions including a final-launch section with architecture, sequence diagrams, and synthetic benchmark claims.
- The repo does not contain the benchmark harness, raw runs, or independent reproduction of the reported hallucination, leak, cost, or latency numbers.
- Use the benchmark table only as a source-reported claim unless artifacts are later ingested and validated.

## Failure Modes

- Summarization loss that removes critical task details.
- False security from software-only compartmentalization.
- Clearance labels that are not enforced by runtime boundaries.
- Context shards leaking through logs, tool calls, traces, or sanitized outputs.
- Token-cost optimization that starves verification.
- Treating mission briefs as complete evidence rather than scoped context.

## Book Chapters Supported

- `security-kernel-and-digital-scifs` (Security Kernel and Digital SCIFs)
- `virtual-context-abi` (Virtual Context ABI)
- `semantic-pages-context-cells-and-certificates` (Semantic Pages, Context Cells, and Certificates)
- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)

## Claims To Add Or Update

- Use this source for context supply chains, need-to-know memory, mission briefs, context-as-code, and Digital SCIF lifecycle design.
- Do not promote synthetic benchmark claims without a local harness or primary result artifacts.

## Open Questions

- Should context transactions include clearance, taint, and memory-mask fields?
- What public toy benchmark can test summarization loss and leak prevention?
