# Source Note: Context Engineer / Manhattan Protocol

| Field | Value |
|---|---|
| Source ID | `context_engineer` |
| Source title | The Manhattan Protocol: Context Engineering for High-Agency Systems |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1xXP364s9IZ4DFmRHTmBELviRQkJcQ55McIUokioRFdo |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/context_engineer.txt` (300 lines; approximately 2,580 words). Raw text is not published. |
| Evidence role | Corben-authored design lineage with unverified synthetic benchmark claims. |

## Thesis

The durable thesis is that context should be treated as a governed information
supply chain rather than a prompt-sized dump. A context compiler between a
planner and a worker selects, transforms, labels, and delivers a task-relative
mission brief under purpose, clearance, authority, provenance, loss, tool, and
egress constraints. Sensitive work can run inside a declared compartment, but
isolation, sanitization, declassification, zeroization, and global-memory
commit are separate operations and must each state their real enforcement and
residual limits.

## Version lineage

The cache contains an initial version 1.0 and a later version 3.2 plus launch
copy. Version 3.2 adds diagrams, calls its MCP use a proposed custom extension,
states software-only limitations, acknowledges summarization loss, and reports
a 50-run synthetic benchmark. It controls terminology, but it does not supply
the benchmark harness, outputs, seeds, prompt/model versions, evaluator code,
or independent review. The launch thread repeats the same claims and is not an
additional source.

## Mechanisms

- Put a context governor between plan construction and execution. It compiles
  an environment but does not inherit planning, evidence, or effect authority.
- Maintain distinct archive, derived semantic, and hot materialized states.
  Each representation needs source lineage, version, loss, invalidation,
  retention, and deletion semantics; “cold,” “warm,” and “hot” are placement
  states, not epistemic grades.
- Produce a structured Mission Brief with task identity, admitted and omitted
  shards, clearance and taint, constraints, allowed tools, purpose, expiry,
  source references, transformation lineage, and residual adequacy. A summary
  cannot silently replace its sources.
- Treat a Model Context Protocol server or similar interface as transport and
  discovery machinery. A proposed `clearance_level`, `context_shards`, or
  `memory_mask` extension has meaning only when an enforcement point validates
  it; protocol fields do not create confidentiality.
- For sensitive tasks, use an explicit compartment lifecycle: request,
  clearance check, admission, spawn, inject, execute, mediate effects and
  egress, sanitize, declassify or refuse, commit or abort, zeroize at a stated
  grade, revoke, audit, and retain residuals.
- Commit a derived result into wider memory only through a separate
  declassification and memory-write decision. The worker must not decide that
  its own output is safe merely because literal secret strings were removed.
- Measure context compilation jointly on task utility, missing constraints,
  contradiction retention, privacy and rights, leakage, latency, cost,
  availability, recovery, and reviewer burden.

## Interfaces and invariants

`virtual-context-abi` owns task-relative materialization, representations,
adequacy, and source-bound context certificates. `context-transactions-
snapshots-mounts-and-taint` owns snapshots, mounts, taint, commit/abort,
invalidation, and deletion closure. `security-kernel-and-digital-scifs` owns
authority leases, isolation grades, complete mediation, declassification,
zeroization, revocation, recovery, and incident residuals.

The invariants are: context structure never grants authority; clearance labels
require enforcement; source references survive compression; omissions remain
visible; sanitization is not declassification; deletion receipts do not prove
physical erasure; a compartment does not imply side-channel safety; and a
smaller prompt is not automatically a better or safer one.

## Evidence

The source supplies architecture prose, JSON and Mermaid-like illustrations,
a compartment sequence, cited inspiration, a proposed MCP extension, one
limitations section, and source-reported synthetic numbers: 18.4% versus 7.2%
hallucination, 100% versus below 0.1% leak probability, $2.40 versus $0.35 per
run, and about 210 ms overhead over 50 claimed runs. None is reproduced here.
The source does not provide a frozen corpus, exact task instances, prompts,
model revision, decoding configuration, context budgets, attack suite,
evaluator calibration, confidence intervals, raw runs, code, or independent
replication. The figures are not book evidence.

## Failure Modes

- Context dumping is replaced by summary dumping, with critical facts,
  qualifiers, contradictions, or exclusions removed.
- A low-cost briefer becomes a single high-impact semantic bottleneck.
- Clearance fields or memory masks are descriptive metadata rather than
  enforced access and attention boundaries.
- A protocol extension is described as if it were part of standard MCP or as
  if transport interoperability implied policy enforcement.
- Literal redaction misses semantic disclosure, encodings, indirect
  inference, tool outputs, errors, logs, caches, timing, or descendant state.
- Zeroization claims exceed what the runtime, allocator, accelerator, storage,
  operating system, snapshots, backups, or provider can establish.
- “Read down, write up” is applied as a slogan without an explicit information-
  flow model, integrity policy, downgrade route, or trusted declassifier.
- Optimization for token savings removes verification, provenance, or reviewer
  context and is counted as improvement.
- A secure compartment destroys task utility or availability, causing an
  undocumented fallback to shared context.

## Explicitly rejected or bounded claims

- Archive capacity is finite and operationally constrained; “infinite
  capacity” is rhetoric.
- Ring Attention is a distributed attention mechanism, not by itself physical
  isolation, a memory mask, a secure wipe, or a SCIF.
- Context minimization does not itself eliminate hallucination or context
  bleeding.
- Regex and entropy scans are narrow detectors, not kernel-level semantic
  non-disclosure.
- The source does not establish a 40–60% or 61% hallucination reduction, a 90%
  token reduction, an 85% cost reduction, below-0.1% leakage, near-zero
  leakage, 210-ms general overhead, or consumer-GPU performance.
- A software process cannot claim permanent or atomic physical erasure without
  a threat-model-appropriate mechanism and evidence.
- The Manhattan Project analogy supplies no security, governance, or ethical
  evidence and should not control the book's terminology.

## Section-family closure

| Source family | Disposition |
|---|---|
| Need-to-know problem and Context Engineer role | Already integrated in Virtual Context and Security Kernel as a compiler with no authority expansion. |
| Vault, Refinery, Switchboard, and mission briefs | Already integrated as versioned representations, derived packets, transport, certificates, loss and omission records. |
| MCP extension and context-as-code object | Retained as protocol-design lineage; the book requires enforcement outside the field names. |
| Digital SCIF lifecycle | Already integrated in the Security Kernel's stronger request-through-recovery transaction. |
| Synthetic benchmark table | Retained only as an unverified source report; it cannot support a claim. |
| Information-flow and anti-leak section | Integrated with corrections for taint, complete egress, declassification, side channels, and detector limits. |
| Summarization-loss limitation and critical bypass | Integrated as adequacy, protected constraints, fallback, source restoration, and residual obligations; raw constants do not bypass authority or rights. |
| References, video suggestion, and launch thread | Citation leads and promotional duplication only; no distinct idea or evidence. |

## Book Chapters Supported

- `virtual-context-abi`
- `context-transactions-snapshots-mounts-and-taint`
- `security-kernel-and-digital-scifs`

No new chapter or new prose is required: the three receiving chapters already
state the source's complete useful model in stronger, less promotional terms.

## Claims To Add Or Update

- Retain this source as context-supply-chain and compartment-lifecycle design
  lineage with exact passage mappings.
- Keep the distinction between context transformation, sanitization,
  declassification, memory commit, and physical zeroization explicit.
- Do not promote any reported synthetic benchmark, protocol-standard,
  isolation, leakage, or erasure claim.

## Research obligations and falsifiers

1. Freeze natural and adversarial multi-agent tasks with exact source universe,
   sensitive assets, required constraints, threat model, contexts, model and
   tool versions, budgets, and release criteria.
2. Compare shared context, ordinary retrieval, human-authored briefs,
   automated briefs, and the full governed transaction at matched budgets.
3. Inject rare constraints, contradictions, semantic secrets, indirect leaks,
   prompt attacks, tool-output attacks, logging and cache channels, stale
   clearances, and declassification ambiguity.
4. Measure useful success, unsupported output, omission, disclosure, false
   blocking, latency, cost, availability, recovery, and human burden together.
5. Falsify the mechanism if a simpler access-control plus retrieval baseline
   performs as well, if briefing loss dominates, or if unmodeled egress defeats
   the claimed isolation boundary.

## Open Questions

- Which context fields must be enforced by the protocol endpoint, runtime,
  reference monitor, storage service, or publication gate?
- How should a context compiler expose uncertainty about omitted material
  without recreating the original context dump?
- What isolation and zeroization grades are meaningful across local RAM,
  accelerator memory, managed APIs, browser agents, logs, and backups?
- When does a sanitized derivative remain too semantically revealing to
  declassify or commit into broader memory?
