# Source Note: Virtual Context Memory v1

| Field | Value |
|---|---|
| Source ID | `vcm_public` |
| Source family | Two related papers in one 30,190-word export: the shorter evidence-bearing “A Governed Protocol for Compiled Working Context” public v1 and the denser architecture/research paper “An Evidence-Carrying, Planner-Guided Context Compiler for Long-Horizon Language-Model Agents” |
| Ingestion date | 2026-06-24; section-family fidelity audit completed 2026-07-31 |
| Source version / URL | Public Release v1, June 2026; https://docs.google.com/document/d/1fid_RDNJcY3gM5WfqTpz5RABpzzoehWU4QKGhurRyJM |
| Canonical local cache | `sources/raw/google_docs/vcm_public.txt`; raw text is not published by this note |
| Evidence boundary | The shorter paper reports one reference implementation, conformance artifacts, synthetic/annotated mechanism studies, a conditional activated-fault result, and an uninformative small-model packet pilot. The denser paper is a conceptual architecture and VCM-Bench research program with no new empirical result. No natural long-horizon, frozen-pretrained-model, independent interoperability, production-cost, security, privacy, or broad neighboring-system advantage is established. |

## Thesis

The model's finite context window should be treated as a compiled working cache
over a much larger, versioned, governed semantic address space. Durable memory,
active context, evidence, behavioral authority, action authorization, privacy,
and model/runtime caches are different state. A consumer requests a purpose-
specific representation under an explicit use contract; the system binds
identity, source, loss, authority, snapshot, admission, materialization,
lifecycle, and faults before content becomes model-visible.

The shorter public-v1 paper narrows the claim further. Its affirmative result
is about declared control-plane behavior under synthetic and annotated
conditions, not model accuracy. Rich packet grammar is optional because a
stronger eight-seed small-model pilot failed to reproduce an earlier favorable
ranking. Stable addresses, exact-source escalation, scoped preferences,
negative memory, authenticated obligations, stale-state invalidation, and
explicit infeasibility can still be useful even if the provider-facing packet
is simple.

## Claim Boundary and Variant Status

The first 568 lines are a compact protocol-and-evidence release. The remaining
lines are a broader architectural preprint with more detailed semantic pages,
transactions, paging, runtime, security, algorithms, and evaluation. They are
one author lineage and count once. Where they differ, the shorter public-v1
claim boundary controls empirical interpretation; the denser paper supplies
design and research obligations.

The papers do not claim infinite context, lossless semantic compression,
universal future-query sufficiency, complete discovery, perfect contract
synthesis, model obedience to labels, global deletion, arbitrary KV-block
composition, or replacement of simultaneous global attention. Native long
context and VCM are complementary. VCM may lose on short, one-shot,
globally-coupled, low-reuse, reactive, or poorly predicted work.

“Virtual memory” is an analogy, not equivalence. Byte pages preserve exact
content under mechanical translation. Semantic pages are variably sized,
meaning-dependent, often lossy, and capable of changing control flow. A
model-generated expansion of a summary is a new derivative, not decompression.

## Conceptual Primitives

- **Semantic object and ObjectID.** Stable governable identity independent of
  content version, representation, validation, packet, or physical location.
- **ObjectVersion.** Immutable content and source ancestry at one transaction
  time. Current policy, authorization, validation, serialization, and residency
  remain contextual records.
- **Context cell.** Atomic typed assertion or event retaining source role,
  authority, scope, time, contradiction, and status.
- **Semantic page.** Smallest independently addressable/governable bundle of
  cells for one coherent use; co-access may form composite pages without
  destroying base identity.
- **Virtual address/root/mount.** A principal-qualified namespace, stable
  object, immutable version, and view. Mounting exposes a namespace and
  snapshot; it does not load every descendant or grant use authority.
- **Representation graph.** Partially ordered task-relative views: handle,
  routing capsule, synthesis, evidence bundle, exact excerpts, raw source, and
  runtime materialization. No scalar compression ladder dominates every use.
- **Use contract/operation contract.** Purpose, principal, audience, operation,
  snapshot, source, coverage, exactness, evidence, freshness, valid time,
  disclosure, effects, authority, budget, deadline, safe fallback, and
  uncertainty policy.
- **Representation certificate.** Source versions, transformation, atomic
  claims, omissions, losses, validity, contradictions, permitted/forbidden
  uses, authority ceiling, verifier result, expiry, and fallback. It certifies
  machine-checkable lineage and policy facts, not natural-language truth.
- **ValidationID.** Content-addressed assessment of one representation against
  one obligation under a snapshot, policy, authorization view, time, and
  validator profile.
- **ContextPacket/PacketID.** Logical admitted set before provider adaptation,
  including protected/optional entries, unresolved items, and snapshot.
- **MaterializationID.** Actual messages, bytes, tokens, ordered prefix, latent
  object, or KV/runtime state keyed to serializer/provider/model/tokenizer/
  role/policy/principal/redaction/permission/snapshot dependencies.
- **Role-indexed obligation.** `CONTROL`, `EVIDENCE`, `QUOTATION`, `DATA`, or
  `ACTION`, each with different exactness, authority, and live-authorization
  rules.
- **Protected minimum set.** Authorized system policy, active request, task
  objective/plan frontier, hard constraints, corrections, commitments,
  procedures, and evidence obligations that must fit before discretionary
  optimization.
- **Semantic page fault.** Exact-source, evidence, freshness, contradiction,
  capability, representation, deadline, unrecoverable-detail, or other typed
  miss with a safe escalation or explicit non-success result.
- **Context map/C-TLB.** Small routing structure or translation cache for nearby
  handles and resolved versions; a performance aid, not semantic authority.
- **Task snapshot/branch.** Versioned coherent read view with read-your-writes,
  copy-on-write alternatives, causal ordering, commit, rollback, merge, and
  invalidation duties.
- **Decision-time feature manifest.** Immutable record of information actually
  observable when retention, compression, or prefetch was chosen; later
  outcomes are attached separately.

## Mechanisms

### Four planes and a bounded trust split

The architecture separates a **ledger plane** for immutable objects, versions,
relations, validation, capability, retention, and materialization state; a
fallible **judgment plane** for segmentation, discovery, contract derivation,
semantic coverage, contradiction, and review; a smaller deterministic **kernel
plane** for authenticated obligations, authorization, snapshots, bounded
selection, fault filtering, signed messages, and coherence; and a **model
plane** that consumes a packet and proposes outputs or actions. External effects
pass through a live authority gate.

This avoids two trust errors. Moving fallible semantic judgment behind a
deterministic API does not make it correct. Conversely, semantic fallibility
does not remove the value of deterministic identity, authority, snapshot, and
state-transition enforcement. The trusted computing base includes kernel,
cryptography, policy combination, coherence, and selected storage primitives;
the trusted judgment base is larger and explicitly error-prone.

### Authenticated contract stabilization

A provisional contract is not allowed to accumulate every retrieved item's
self-declared importance. Discovery proposes candidate obligations; source and
issuer bindings determine whether they can be protected; contract strengthening
is a partial order over coverage, exactness, freshness, authority, evidence,
and effects; and bounded iterations either stabilize or return uncertainty.
Content cannot self-designate mandatory, pinned, trusted, privileged, or
behavioral. A retrieved instruction stays data unless an authorized
transformation and issuer/policy decision changes its role.

Adequacy and admission are separate. Adequacy asks whether a representation
satisfies an obligation under its snapshot and use contract. Admission decides
whether it may enter the packet and with which effects, expiry, and fallback.
An adequate quotation can be denied for privacy; an admitted planning summary
can remain inadequate for citation; unknown evidence cannot become final by
being present.

### Joint protected compilation

The compiler builds policy/request/task lanes, derives the protected set, and
resolves the cheapest eligible representation for each obligation. It first
tests whether the full protected set fits all token, latency, interference,
privacy, and runtime budgets. If not, it returns explicit unsafe fit or unknown
feasibility rather than dropping a mandatory page. Only the remaining capacity
is allocated among optional candidates by marginal value after dependency,
conflict, rights, capability, taint, freshness, and snapshot checks.

The selection record keeps the candidate and omitted frontier, protected and
optional entries, solver status, optimality status, costs, and unresolved
items. A timeout is not proof of infeasibility. `PROVEN_INFEASIBLE`,
`FEASIBILITY_UNKNOWN`, feasible-best-effort, bounded-gap, and proven-optimal
states remain distinct.

### Evidence-carrying derivation and lifecycle

The write path captures immutable events and exact spans; segments and types
cells; binds provenance; detects support, contradiction, qualification,
supersession, and rejection; creates provisional pages; generates several
representations; verifies claim coverage, negation, scope, time, contradiction,
and declared loss; applies purpose, sensitivity, sharing, retention, and
execution governance; commits versions and graph edges atomically; and
invalidates descendants and caches.

Exact decode reconstructs retained bytes. Semantic materialization consults
sources to build a use-specific derivative. The elementary future-query result
states that a strict lossy summary cannot answer every unknown query that can
distinguish source states. Safe strict compression therefore retains or
addresses stronger source material, restricts the supported future-use family,
or returns unrecoverable detail. Unsupported reconstruction is not a fourth
option.

Contradictions remain represented rather than averaged. Rejected alternatives
remain negative memory with scoped reasons. A stale source marks dependent
summaries, certificates, indexes, packets, and caches dirty. Deletion follows
known descendants and records residue; it does not claim universal erasure or
model unlearning.

### Planner-guided residency and semantic faults

The CMMU resolves aliases to immutable versions, checks capability/purpose/
provenance/time/taint, chooses an eligible representation and physical source,
consults a C-TLB, initiates fetch/verification/materialization/tokenization/KV
work, stages pages outside model-visible context, handles faults, tracks task
working sets/thrashing, invalidates stale caches, and records promotion,
pinning, eviction, denial, and deletion.

Plan nodes forecast likely page, representation, deadline, and probability.
Prefetch compares avoidable fault latency against fetch/materialization,
pollution, privacy, cancellation, and exposure costs. Staging remains invisible
until address, capability, provenance, freshness, snapshot, representation,
dependency, relevance, and budget gates pass. Branch changes cancel losing
fetches and purge disallowed staged material.

Eviction is not LRU alone. It considers reuse, reacquisition, catastrophic-loss
prevention, staleness, contradiction, privacy, interference, dependencies,
granularity, and resurface budgets. Thrashing is repeated re-fault, turnover,
transfer, and lack of task progress. A larger native window reduces some faults
but does not replace identity, authority, lifecycle, or selection policy.

### Decision-time observability

Retention, compression, page-boundary, and prefetch policies may learn from
later outcomes, but online evaluation freezes what was observable at decision
time. Future queries, answers, gold evidence, dependency labels, and
post-decision page boundaries are stored separately. The original manifest is
never rewritten to include hindsight.

This blocks a common false result: a “memory policy” that appears predictive
because its summaries, value labels, page boundaries, or retention features
encode the benchmark's later question. Blind deployable performance and a
future-aware oracle upper bound are both useful, but their gap must remain
visible.

### Transactions, context switch, and runtime coherence

Immutable events feed versioned materialized views. Each task pins a snapshot,
receives read-your-writes, and may branch copy-on-write. Atomic commits include
new pages, relations, certificates, governance, invalidation, and audit.
Distributed agents retain causal order and conflicts; they do not silently
last-write-win semantic disagreement.

A context switch checkpoints the active frontier and dirty state, records
pending tools and commitments, unpins task-local pages, mounts an immutable
destination root, loads manifests and capabilities, builds a plan and working-
set forecast, stages likely pages, compiles the first packet, and retains a
return continuation. Restart recovery replays authoritative ledger events and
enumerates uncommitted or lossy state.

Runtime materializations are disposable. A reusable prefix/KV object binds the
complete ordered prefix and positions, model, tokenizer, adapter, policy,
principal, permission, redaction, snapshot, and source/representation versions.
Compatibility does not establish truth or authorization; invalidation must
reach every dependent cache.

### Wire protocol and conformance

The shorter paper proposes signed envelopes, audience binding, replay
protection, downgrade resistance, version/feature negotiation, canonical
serialization, redacted public faults, and registries for operations, packet
profiles, serializers, validators, transformations, and optional features.
Unknown critical fields fail closed. A cached content read rechecks current
release authority.

One implementation and its positive/negative vectors provide constructive
conformance evidence only. Interoperability needs a second implementation,
cross-language canonicalization, mutation tests, fuzzing, and signed vectors.
The export describes a release package, but the repository does not contain or
verify that complete VCM package.

## Interfaces and Outcome Algebra

The six identities—object, version, representation, validation, packet, and
materialization—prevent policy or cache state from masquerading as semantic
content. Dynamic operations then return orthogonal state:

| Dimension | Source vocabulary | Question answered |
|---|---|---|
| adequacy | `SATISFIED`, `UNSATISFIED`, `UNKNOWN` | Does this representation meet this obligation? |
| admission | `FINAL`, `PROVISIONAL`, `DEFERRED`, `REJECTED` | May it enter this packet under current policy? |
| feasibility | `FEASIBLE`, `PROVEN_INFEASIBLE`, `FEASIBILITY_UNKNOWN` | Can the protected compilation fit? |
| optimality | `PROVEN_OPTIMAL`, `BOUNDED_GAP`, `BEST_EFFORT`, `NOT_APPLICABLE` | What is known about selector quality? |
| compilation | ready/provisional packet, ask, abstain, deny, unsafe fit, unknown, retry | What should the caller do now? |
| lifecycle | validated, stale/dirty, invalid, purged | Can an existing representation or cache still be used? |

VCM owns the static source-to-packet contract and protocol. Context Transactions
own commits, snapshots, branches, taint, invalidation, and deletion. Durable
Memory owns semantic object/relation identity. Planning owns explicit future
demand. Verification Bandwidth owns claim-specific adequacy. Security/Privacy/
Rights own capabilities, exposure, declassification, and retention. Runtime
Adapters own current action authorization and effects. Artifact Graphs own
lineage and replay. Evidence owners alone change claim support.

## Assumptions and Invariants

- Every model-visible durable span resolves to an immutable page version and
  provenance role.
- Every derived view declares source bindings, loss, omissions, use contracts,
  authority ceiling, validity, fallback, and verifier.
- Content cannot grant itself control, pinning, trust, privilege, evidence
  standing, or action authority.
- Processing exposure, output influence, evidential use, behavioral influence,
  and external authorization are separately recorded.
- Every task pins a snapshot and every materialization binds policy,
  authorization, principal, redaction, serializer, model, tokenizer, and role
  layout where material.
- Conflicts are represented, adjudicated, or explicitly excluded; they are not
  averaged into one fluent synthesis.
- Protected obligations are admitted before discretionary optimization; a
  mandatory overflow yields explicit unsafe fit or unknown feasibility.
- Staged pages remain non-model-visible until promotion gates pass.
- Current tool/effect authority is checked live and cannot be inferred from
  remembered permission.
- Lossy materialization never calls itself exact decode and never invents
  omitted detail without a source.
- Learned scoring operates inside identity, authority, snapshot, deletion, and
  future-information barriers.
- Low retrieval frequency alone cannot authorize permanent deletion.
- Runtime caches are disposable projections and cannot serve as sole
  provenance, truth, authority, or durable memory.

## Evidence

The shorter public-v1 paper reports five evidence levels: specification,
single-implementation conformance, mechanism isolation, controlled model
learnability, and external validity. It reaches the first three affirmatively;
its level-four model-facing pilot is an uninformative non-replication; it does
not reach external validity.

Its governance fault-injection study activates one of seven modeled faults on
every trial: authority laundering, replay after revocation, stale derivative
reuse, self-promoting obligations, deletion residue, timeout mislabeled as
infeasibility, and a combined authorization/invalidation check-use race. Across
20 paired seeds and 10,000 activated-fault trials per seed, the paper reports
mean severity-weighted unsafe rates of 77.51% for a typed compiler, 3.29% for a
point-hardened typed compiler, and 0.44% for VCM Core. On the combined race it
reports 44.60%, 15.87%, and 0%. With 5% source-authority label error, VCM rises
to 2.00%.

That is narrow synthetic mechanism evidence under activated faults and mostly
oracle source-authority labels. It does not estimate fault prevalence, validate
the semantic front end, prove natural model behavior, or establish production
safety. The most useful causal claim is that cross-layer binding can prevent a
modeled check-use race that isolated fixes miss under the study's assumptions.

Other source-reported studies show tradeoffs rather than broad wins:
authenticated stabilization reduces false protected obligations while losing
some recall/availability; bounded solver runs show why timeouts remain
`FEASIBILITY_UNKNOWN`; an influence pilot has moderate precision and low recall
and supports conservative privacy propagation only; a 100,000-event synthetic
collection study reduces retained records without establishing resumption or
audit sufficiency; and the conformance suite checks declared protocol
properties for one implementation.

The small model-facing pilot is deliberately retained. An earlier favorable
result was not reproduced by an eight-seed stronger study: accuracy stayed near
floor, five of eight paired seeds tied between the strong typed composite and
full VCM, and paired tests did not support a reliable packet ranking. It tests
closed-vocabulary learnability in a tiny model trained on each policy, not
zero-shot instruction-tuned models, natural histories, or free generation. It
is evidence that the ranking is unknown, not that VCM packets fail generally.

The decisive next campaign freezes the protocol before annotation; uses at
least two frozen instruction-tuned families, natural or independently authored
long histories, free outputs, matched sources/tokens, strong typed memory plus
compiler, and released close neighbors; attributes errors by stage; and charges
full operational cost. It separately measures discovery, contract
understatement, adequacy errors, mandatory admission, model compliance,
evidence fidelity, stale use, security/privacy, review burden, latency, storage,
maintenance, and developer cost.

The denser VCM-Bench program adds baselines for full context, truncation,
rolling summaries, lexical/dense/hybrid RAG, active retrieval, simple typed
memory, persistent agent memory, learned memory policies, semantic paging,
programmable compilers, provenance-tiered systems, hierarchical/portable
memory, prompt compression, runtime paging, and oracle upper bounds. Metrics
cover task quality, mandatory-state survival at the use point, continuity,
context efficiency, fault/recovery latency, prefetch regret, interference,
thrashing, derivation fidelity, future-information leakage, authority,
staleness, attack success, privacy, consistency, runtime, energy, and total
complexity. Decision rules use a Pareto frontier rather than one weighted score.

## Failure Modes

- Stable object identity points to the wrong or poisoned semantic object.
- Source identity or authority is mislabeled and the kernel faithfully enforces
  the wrong contract.
- Discovery misses a required object, so no downstream fault can recover it.
- Contract synthesis understates exactness, freshness, evidence, authority, or
  conflict closure.
- A summary loses negation, quantification, modality, temporal scope,
  attribution, rejected alternatives, or source role.
- A fluent derivative self-promotes into evidence, control, preference, or
  current permission.
- Protected lanes are stuffed by untrusted text or cause denial of service.
- A selector times out and reports infeasibility or silently drops mandatory
  state.
- A rich solver ties a simpler typed baseline while costing more to build,
  maintain, audit, and recover.
- A large window contains required information but the model ignores it or
  optional pages interfere with use.
- Predictive staging leaks private existence/access patterns, loads losing
  branches, misses deadlines, or pollutes attention after unsafe promotion.
- A future-query label, answer, page boundary, or dependency annotation leaks
  into an online memory decision.
- LRU/frequency permanently buries unfamiliar but catastrophic-loss-preventing
  pages; overbroad anti-starvation retains everything.
- Page boundaries drift with co-access optimization and destroy human-
  understandable identity or audit.
- Model-generated “decompression” fabricates missing source detail.
- Incompatible prefix/KV objects are reused across model, tokenizer, adapter,
  policy, principal, permission, redaction, position, or snapshot.
- Concurrent agents create write skew, lost contradiction, mixed versions,
  causal inversion, or last-write-wins semantic corruption.
- Deletion removes a row but leaves summaries, indexes, embeddings, staging,
  caches, logs, backups, shared pages, exports, adapters, or model influence.
- Fine-grained influence heuristics miss semantic leakage; processing exposure
  is mistaken for observed output influence.
- Signed protocol shape, hashes, or a passing vector are mistaken for
  semantic correctness or interoperability.
- Fault-detail filtering hides too much from an authorized debugger or leaks
  object existence to an unauthorized caller.
- Memory becomes surveillance, lock-in, or persistent manipulation despite
  high recall because user inspection, scope, correction, export, and deletion
  authority are inadequate.

## Cross-Paper Synthesis

- QCSA supplies stable identity/plural address/epoch/certificate mechanics;
  VCM supplies packet materialization and use contracts.
- KERC supplies representation-aware Kernel packets and residual state; VCM
  supplies source fallback, exact-object escalation, and transaction epochs.
- Cognitive Compilation supplies typed lowering/trace/repair; VCM is the
  source-to-working-context ABI used by compiler and runtime consumers.
- Talos supplies typed jobs and execution custody; VCM prevents a job's context
  handle or cached packet from minting authority.
- Spinoza and Claim Ledgers own proposition state and revision; representation
  certificates cannot settle claim truth.
- Context Engineer and Ladon/Manhattan supply context supply-chain and blind-use
  lineage; VCM adds identity, adequacy, snapshot, and typed fault contracts.
- Fast Generation owns physical weight/KV/prefix paging and serving economics;
  VCM owns semantic source identity and the validity key joining that state.
- Data Engines and Loop Closure own learned retention, contamination, full-
  state update, rollback, and unlearning beyond one VCM decision manifest.

## Book Chapters Supported

- `failure-modes-of-ungoverned-intelligence`
- `virtual-context-abi`
- `durable-semantic-memory-and-knowledge-lattices`
- `context-transactions-snapshots-mounts-and-taint`
- `verification-bandwidth-and-context-adequacy`
- `claim-ledgers-and-belief-revision`
- `fast-generation-architectures`
- `coil-attention-cyclic-memory-and-recurrence-contracts`
- `policy-optimization-and-learning-from-feedback`
- `personal-compute-hives-and-federated-edge-intelligence`
- `inter-stack-protocols-identity-and-economic-exchange`
- `artifact-steward-agents-and-living-project-governance`
- `integrated-reference-architecture`
- `prototype-roadmap`
- `open-research-agenda-and-bibliography-plan`

## Claims To Add Or Update

- Separate ledger, judgment, kernel, and model planes so deterministic policy
  enforcement never launders fallible semantic judgments.
- Preserve six identities—object, version, representation, validation, packet,
  and materialization—through every source-to-context route.
- Keep adequacy, admission, feasibility, optimality, compilation, and lifecycle
  outcomes orthogonal; a timeout cannot become unsafe fit or infeasibility.
- Treat decision-time observability as a memory-policy validity condition and
  keep future-aware oracle labels separate from deployable policies.
- Distinguish exact decode, semantic materialization, source escalation, and
  unrecoverable detail.
- Treat protected compilation as safety-constrained allocation: mandatory
  obligations cannot be outbid by optional relevance.
- Treat semantic and runtime memory as linked but non-equivalent; physical
  cache reuse never grants epistemic or behavioral authority.
- Preserve the activated-fault result only as conditional source-reported
  synthetic mechanism evidence and the packet pilot as an uninformative
  non-replication.
- Prefer the minimal Core when optional paging, transactions, prediction,
  native caches, or review cannot justify their independent cost.

## Open Questions

- How can discovery recall and contract understatement be measured on natural
  histories without annotating the test set into the online memory policy?
- Which representation certificates can be validated independently enough to
  catch shared semantic errors?
- What is the smallest protected-set solver that preserves honest unknown
  feasibility and gives useful deadline behavior?
- How should globally coupled phases be detected before paging causes failure?
- Can learned page boundaries improve reuse without breaking stable identity,
  provenance, and human audit?
- Which information-flow and causal tests separate processing exposure from
  output and action influence?
- Can multiple implementations agree on canonical records and faults while
  using different stores, languages, models, and runtime caches?
- How should deletion closure extend to adapters, learned policies, models,
  external effects, and encrypted backups?
- What user interface makes mounts, scopes, summaries, omissions, conflicts,
  corrections, and deletion understandable without overwhelming the user?
- Where does full VCM beat a strong simple typed compiler after all maintenance,
  review, privacy, storage, recovery, and developer costs are charged?

## Section-Family Coverage

| Source section family | Actual owner or disposition |
|---|---|
| Shorter §§1–2 | Virtual Context ABI/source note: claim boundary, minimal Core, four planes, read path, features, invariants, and typed outcomes integrated. |
| Shorter §3 | source note: Project Atlas walkthrough retained as an illustrative state/context scenario, not model evidence. |
| Shorter §4 | source note/external grounding: compositional novelty boundary retained; cited neighbors require independent primary-source notes before novelty claims. |
| Shorter §5 | Virtual Context ABI/Verification Bandwidth: six identities, role-indexed contracts, adequacy/admission, stabilization, evidence/exposure/influence/authority separation integrated. |
| Shorter §6 | Virtual Context ABI/Fast Generation: representation graph, protected joint compilation, semantic faults, packet profiles, prediction, and native materializations integrated. |
| Shorter §7 | Context Transactions/Data Engines: immutable versions, snapshots, invalidation, deletion residues, recovery, and collection boundaries integrated. |
| Shorter §8 | Virtual Context ABI/source note: signed envelopes, registries, version negotiation, canonicalization, redacted faults, release checks, and second-implementation requirement retained. |
| Shorter §9 | Security/Privacy/source note: TCB/judgment-base split, malicious content/principals, planner manipulation, probing, replay/downgrade/cache/label/storage threats and exclusions retained. |
| Shorter §10.1–10.3 | source note and evidence owners: evidence ladder, exact conditional synthetic fault rates, label-error sensitivity, solver/influence/collection/conformance boundaries retained without broad promotion. |
| Shorter §10.4 | Virtual Context ABI/source note: eight-seed packet-format non-replication retained as unknown ranking, not negative proof. |
| Shorter §§11–14 | Virtual Context ABI/Mature Target/Open Research: frozen natural campaign, simpler baseline, falsifiers, Core-first discipline, limitations, and conclusion integrated. |
| Shorter Appendices A–B | Virtual Context ABI/Verification Bandwidth: record and outcome families integrated; full normative schemas remain implementation obligations. |
| Shorter Appendix C | source note/Artifact Steward: claimed release-package contents retained as source-reported; complete package and immutable deposit are not present or verified here. |
| Shorter references | external-source backlog: related-work candidates retained but not treated as independently passage-reviewed by this source audit. |
| Denser §§1–3 | Virtual Context ABI/source note: broad architecture, requirements, deployment regimes, threat model, related work, and precise compositional novelty retained. |
| Denser §4 | Virtual Context ABI: cell/page/address/root, page state, representation graph, use contract, exact/materialized distinction, future-query theorem, importance/risk/anti-starvation, authority, and compiler formal model integrated. |
| Denser §5 | Virtual Context ABI/Context Transactions: ledger, taxonomy, namespace/mounts, CMMU, compiler, governance kernel, and physical hierarchy integrated. |
| Denser §6 | Durable Memory/Context Transactions: ten-stage write path, certificates, verification, specialized representations, revaluation, contradictions, invalidation, and deletion closure integrated. |
| Denser §7 | Virtual Context ABI/Fast Generation/Planning: plan-guided staging, promotion, faults, switching, eviction/recompression, thrashing, outcome adaptation, and trace integrated. |
| Denser §8 | Context Transactions: event sourcing, task snapshots, atomic commit/rollback, causal ordering, copy-on-write branches, cache coherence, and recovery integrated. |
| Denser §9 | Security/Privacy/Runtime: execution classes, write/read promotion security, capability mounts, taint, privacy-aware prefetch, scoped personalization, staleness, user control, and eleven governance invariants integrated. |
| Denser §10 | source note and failure owners: complete failure inventory and explicit no-universal-codec/planning/global-attention/verifier-correlation/economic limits retained. |
| Denser §11 | Prototype/Integrated Architecture/source note: service/store/hardware/native model/runtime cache/learned policy/interoperability/deployment/conformance designs retained as implementation obligations. |
| Denser §12 | Open Research/Benchmark/Resource owners: VCM-Bench RQs, hypotheses, baselines, tracks, adversarial continuity case, metrics, ablations, protocol, Pareto decisions, and falsifiers retained. |
| Denser §§13–14 | canonical chapters/source note: retrieval-to-residency, transcript-to-state, effective working context, constrained allocation, memory-as-control-flow, epistemic humility, open problems, broader implications, and conclusion integrated. |
| Denser Appendix A | source note/schema owners: complete semantic-page example retained as proposed portable contract, not an implemented standard. |
| Denser Appendix B | Virtual Context ABI/Data Engines/Planning/Context Transactions: compile, prefetch, commit, and observability-safe revaluation algorithms integrated as proposed reference procedures. |
| Denser Appendix C | canonical chapters/source note: all nineteen invariants reconciled; no conformance claim inferred. |
| Denser Appendix D and references | source note/glossary/external backlog: terminology and citations retained without importing novelty or neighbor results. |

## Closure Status

**Section-family audit complete as of 2026-07-31.** Both the shorter
evidence-bearing public release and the denser architecture paper terminate in
reader-facing integration, explicit variant reconciliation, public-safe note
retention, concrete implementation/evaluation work, or an explicit non-claim.
The existing VCM, transactions, adequacy, memory, security, runtime, resource,
and learning chapters already owned most mechanisms. This pass restores the
missing four-plane trust split, complete outcome algebra, decision-time
observability barrier, and exact evidence/non-replication interpretation rather
than adding a duplicate chapter.

Closure establishes no natural long-horizon advantage, model-facing packet
advantage, open-world discovery, contract correctness, summary fidelity,
deployed resolver, transaction isolation, deletion/unlearning, cache safety,
security, privacy, interoperability, production cost, deployment, support,
SOTA, AGI, or ASI result. Reopen on material source, implementation-artifact,
or receiving-chapter drift.
