# Source Note: Compiled Cognitive Architecture Project

| Field | Value |
|---|---|
| Source ID | `cca_project` |
| Source title | Compiled Cognitive Architecture project |
| Ingestion date | 2026-07-10 |
| Source version / URL | `local-project:cca@bd9afd16fe5b11c68f8c495f85ad117cc61ccfc8` |
| Citation label | Corben Dredge, Compiled Cognitive Architecture (pinned local project snapshot) |
| Source policy | Local private cache; public-safe note only; raw project tree is not copied into this repository. |
| Ingestion basis | Architecture documents, active plan, external audit memo, Rust contract surfaces, configuration, formal sources, and storage/history inventory inspected. Expensive training, benchmarks, and full-workspace tests were not rerun. |

## Thesis

CCA proposes that a general-intelligence system should externalize durable
knowledge, compile intent through a typed semantic IR, govern commitments and
revision explicitly, and restrict self-improvement to evidence-gated,
replayable changes over declared mutable state. Its strongest contribution to
the book is not a claim of achieved AGI or ASI. It is a convergence
implementation reference plus a detailed negative record showing how training,
proxy, adapter, lineage, and closure metrics can disagree.

## Mechanisms

- Manifest-governed separation between protected governance state and mutable
  capability state.
- Dynamic Knowledge Lattice with typed edges, justification/provenance,
  append-only supersession/invalidation, tiered storage, and Portia-style
  learned navigation.
- Semantic Base Language with typed primitives, relations, explicit ambiguity,
  deterministic encoding, invocation effects, runtime bindings, and receipts.
- Five-stage cognitive compiler with typed semantic atoms, capability-tier
  routing, pass hashes, verification, bounded repair, target IR, and trace
  bundles.
- Seven epistemic commitment/lifecycle states, explicit justification kinds,
  bounded contradiction revision, quarantine, and non-overwriting lineage.
- Bounded tribunal topology, dissent preservation, shadow-to-enforcement
  anti-expert routing, and a no-silent-veto rule.
- Self-modification as a validated manifest transaction with contamination
  controls, promotion states, rollback, and growth guard.
- Benchmark truth contracts binding case identity, raw output, checkpoint,
  tokenizer, runtime path, contamination state, closure eligibility, and
  scoreboard authority.
- Proxy-to-benchmark trace records, retry-lineage ceilings, progress
  heartbeats, partial checkpoints, and fail-closed closure/postmortem states.
- Compact Lean model plus theorem-to-runtime mapping and proof-obligation
  registry.
- Sovereign device-mesh design separating interface, accelerator, storage, and
  coordinator roles.
- Four seed-entity compression classes with distinct reconstruction and
  residual requirements.

## Evidence reviewed

- The pinned tree contains Rust types, schemas, validators, tests, CLI/runtime
  surfaces, training/evaluation configurations, Lean sources, and mapping
  records corresponding to many proposed mechanisms.
- The formal workspace models and proves finite properties over a compact
  abstraction. It does not prove the full Rust system, semantic adequacy,
  bypass absence, model quality, or safety.
- The active plan and review memo record falling training loss without honest
  benchmark lift, proxy/benchmark divergence, contaminated or layer-mismatched
  score families, runtime/decode failures, and fail-closed repairs.
- These project-reported artifacts were not replayed from the book repository.
  They remain local-project implementation context until a scoped reproduction
  or accepted evidence transition exists.

## Failure Modes

- Treating lower training loss or higher proxy score as capability evidence.
- Allowing side reports or adapter scores to outrank the canonical closure and
  lineage gate.
- Repeating materially identical failed runs until a favorable number appears.
- Counting repair-primary, cached, contaminated, malformed, or task-mismatched
  outputs as native capability.
- Treating theorem count, theorem naming, or source hashing as proof of broad
  runtime semantics.
- Assuming a modeled read-only partition cannot be bypassed by unmodeled code.
- Expanding infrastructure and contract count faster than the central
  capability bottleneck is resolved.
- Allowing build caches, environments, duplicate checkpoints, vendored mirrors,
  and generated blobs to exhaust storage or enter Git history.

## Book Chapters Supported

- `asi-is-a-stack-not-a-model`
- `the-efficient-asi-hypothesis`
- `system-boundaries-and-authority`
- `evidence-states-and-claim-discipline`
- `scalable-oversight-and-adversarial-ai-control`
- `stable-capability-fields`
- `capability-replacement-and-rollback`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `model-weight-custody-and-hardware-roots-of-trust`
- `recursive-self-improvement-boundaries`
- `human-intent-as-a-formal-input`
- `intent-to-execution-contracts`
- `planning-as-a-control-layer`
- `cognitive-compilation-and-semantic-ir`
- `virtual-context-abi`
- `context-transactions-snapshots-mounts-and-taint`
- `claim-ledgers-and-belief-revision`
- `spinoza-verification-and-proof-carrying-claims`
- `artifact-graphs-audit-logs-and-replay`
- `procedural-memory-and-cognitive-loop-closure`
- `routing-heads-and-specialist-cores`
- `readiness-gates-residual-escrow-and-quarantine`
- `personal-compute-hives-and-federated-edge-intelligence`
- `compact-generative-systems-and-residual-honesty`
- `governed-deliberation-and-test-time-scaling`
- `rankfold-neuralfold-and-artifact-compression`
- `resource-economics-and-token-budgets`
- `executable-specifications-and-lean-proof-envelope`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `capability-thresholds-and-deployment-commitments`
- `policy-optimization-and-learning-from-feedback`
- `data-engines-continual-learning-and-unlearning`
- `artifact-steward-agents-and-living-project-governance`
- `integrated-reference-architecture`
- `prototype-roadmap`
- `open-research-agenda-and-bibliography-plan`

## Claims To Add Or Update

- Add closure-authority inheritance: failed canonical closure forces all
  derived/partial score surfaces to remain non-claim.
- Add optimizer-to-capability trace discipline: objective/loss evidence must be
  linked through checkpoint, tokenizer, runtime path, raw output, verifier, and
  suite closure before it supports a capability claim.
- Add retry-lineage ceilings as anti-Goodhart and resource-governance controls.
- Add no-silent-veto and dissent-preservation requirements to governed
  deliberation.
- Add semantic-depth and abstraction-map fields to proof/runtime coupling.
- Add durable semantic-memory versus context-materialization separation; defer
  the new-chapter decision until BeastBrain is mined.
- Use protected governance state and role separation only as bounded
  implementation-reference context for weight-custody records; do not treat CCA
  as evidence of weight custody, attestation, confidential inference, or
  security effectiveness.
- Use typed provenance, append-only supersession/invalidation, source hashes,
  pass hashes, trace bundles, and closure/lineage discipline only as bounded
  implementation-reference context for AI supply-chain records; do not treat CCA
  as evidence of AI BOM completeness, artifact integrity, supplier trust,
  signing, verification, revocation, security effectiveness, or compliance.
- Use CCA as a convergence implementation reference without treating its
  benchmark, efficiency, safety, or AGI/ASI claims as book-verified results.

## Open Questions

- Which lattice and Portia mechanisms are native CCA work versus direct
  BeastBrain ports, and which project owns primary provenance?
- Which MoECOT contracts are duplicated, superseded, or materially changed in
  CCA?
- Which saved artifact families are claim-bearing by their own policy and have
  enough retained inputs for independent replay?
- Which Lean-to-Rust mappings have meaningful semantic coupling rather than
  identifier or shape coupling?
- Should the book add a dedicated durable semantic-memory chapter after the
  cross-project provenance pass?

## Non-claims

- This note does not claim CCA is AGI, ASI, safe, corrigible, competitive, or
  production ready.
- It does not reproduce training, benchmark, speech, code, math, routing,
  compression, mesh, or self-improvement results.
- It does not establish open-domain knowledge-lattice quality, semantic
  extraction correctness, belief-revision correctness, reviewer independence,
  or runtime enforcement completeness.
- It does not promote any ASI Stack claim support state.
