# Project Mining Dossier: Compiled Cognitive Architecture

Date opened: 2026-07-10
Project source: local private worktree, read-only for this mining pass
Pinned snapshot: `bd9afd16fe5b11c68f8c495f85ad117cc61ccfc8` on `main`
Source policy: public-safe notes only; raw project files remain outside this
repository

This dossier separates architecture value from implementation evidence and
from project aspiration. CCA is especially valuable because it is both a
convergence design and a record of where sophisticated governance machinery
did and did not produce honest capability.

## Repository posture

The repository describes an eleven-crate Rust system with a small neural core,
an external knowledge substrate, a semantic language and compiler, epistemic
governance, self-modification gates, training/evaluation machinery, and a Lean
workspace. The pinned commit contains 62,835 tracked files and about 404,000
Rust lines across the eleven crates. The source tree also contains extensive
config, test, report, dataset, benchmark, and training surfaces.

The active plan is newer and more reliable for current-state claims than the
whitepaper. The whitepaper says the ten architectural invariants had not yet
been machine checked, while the pinned repository contains a later Lean model,
proof sources, a theorem-to-Rust mapping, and a proof-obligation registry. The
two records are temporal snapshots, not interchangeable status statements.

## Primary material inspected

- `docs/cca.md`: full architecture, limitations, implementation table, resource
  estimates, and formal definitions.
- `cca_asi_plan.md`: active truth/transfer/decode closure plan and saved artifact
  references.
- `claude_asi_plan.md`: external audit memo covering loss/capability divergence,
  contamination, proxy mismatch, retry behavior, and lineage failures.
- `docs/cca_future_path.md`: predecessor-port inventory, sovereign mesh,
  product envelopes, and forward path.
- `docs/workspace_hygiene_policy.md`: canonical-versus-ephemeral storage policy.
- `docs/corbens_trainer_sovereign_shadow_conversion.md`: derived-control-plane
  and native-claim-authority boundary.
- Core Rust types and public surfaces across `cca-core`, `cca-lattice`,
  `cca-synapse`, `cca-sbl`, `cca-compiler`, `cca-governance`, `cca-self-mod`,
  `cca-perceptual`, `cca-training`, `cca-api`, and `cca-cli`.
- `formal/`: compact Lean model, invariant proofs, contract mapping, runtime
  mapping, and proof-obligation registry.
- Top-level storage composition, large files, Git object statistics, and
  reachable historical blobs.

## Architecture mined for the book

### 1. The system boundary is a compiler-governed cognitive stack

CCA treats the manifest, registries, semantic contracts, compiler passes, and
evidence gates as authority. Runtime artifacts are compiled consequences, not
editable sources of truth. This strengthens the ASI Stack distinction between
model capability, system authority, and deployment state.

Useful addition: define a **compiler-first execution law** for the integrated
architecture. Every durable behavior needs a source artifact; every promoted
change needs replay and rollback lineage; every expensive path needs a cheap
probe and a fail-closed exit.

### 2. Durable semantic memory is distinct from context materialization

The Dynamic Knowledge Lattice proposes coordinate-addressed nodes, a finite
typed-edge ontology, explicit epistemic commitment, justification edges,
append-only supersession/invalidation, tiered storage, and learned navigation.
This is not the same boundary as the Virtual Context ABI. The lattice owns
durable semantic state and navigation; the ABI owns which versioned,
authority-bounded representation may be materialized for a consumer.

Potential chapter boundary: **Durable Semantic Memory and Knowledge
Lattices**. The decision is deferred until BeastBrain is mined because CCA
identifies BeastBrain as the primary implementation lineage for the lattice and
Portia navigation.

### 3. Semantic Base Language is an authority-bearing IR, not prompt syntax

CCA's SBL combines typed semantic primitives, relations, invocation opcodes,
ambiguity slots, strict versus exploratory modes, keyword invariance,
deterministic serialization, effect declarations, runtime bindings, and
execution receipts. The book should emphasize that an AI IR must preserve
obligations, ambiguity, effects, authority, and provenance—not merely normalize
text into JSON.

### 4. Cognitive compilation produces a trace bundle, not just an answer

The five-stage extraction/normalization/typing/optimization/verification model
is already adjacent to the book's compiler chapter. CCA adds a concrete bundle
shape: source plan, semantic IR DAG, target IR, ordered pass hashes, route
decisions, verification report, repair actions, and deterministic trace-bundle
hash. This is a strong implementation-reference pattern for lowering receipts.

### 5. Intelligence arbitrage is a typed routing decision

CCA routes semantic atoms to scriptable, moderate, advanced, or deliberative
tiers. The reusable principle is not the claimed efficiency percentage; it is
that a plan atom declares capability need, cost, preconditions, postconditions,
and effects before routing. Cheap deterministic execution is preferred when it
can honestly satisfy the atom.

### 6. Epistemic commitment needs lifecycle, justification, and bounded repair

CCA's seven states—Certified, NormAnchored, ProcedureBacked, Hypothesis,
Quarantined, Superseded, Retracted—combine evidence class with lifecycle. The
book should not import them blindly into its existing support-state taxonomy,
but should mine three mechanisms:

- justification kind is separate from current belief lifecycle;
- contradiction repair has explicit primary-retraction and dependency-hop
  budgets, with unresolved residue quarantined;
- prior nodes are not silently edited; supersession and invalidation remain in
  lineage.

### 7. Dissent and vetoes must remain inspectable

CCA's tribunal records topology, roles, cycle caps, participation, dissent, and
failure states. Its anti-expert path moves through shadow, advisory, and
governed enforcement and forbids silent veto. The book can strengthen both
governed deliberation and scalable oversight with the invariant that a safety
or contradiction detector cannot quietly erase a candidate branch; it must
emit a scoped, reviewable disposition.

### 8. Self-modification is a transaction over mutable capability state

The reusable pattern is manifest-diff self-modification with a read-only
governance partition, contamination-isolated evaluation, staged promotion,
rollback, and growth guard. The strong claim that arbitrary capability growth
cannot weaken oversight is not established by this repository. The useful
book claim is narrower: modeled self-mod operations can be restricted to a
declared mutable partition, and runtime admission can fail closed when a diff
touches protected fields or lacks evidence.

### 9. Formal coupling needs a semantic-depth audit

CCA maps Lean theorem names to Rust contract surfaces and hashes source/mapping
artifacts into a coupling record. This is valuable. The proof sources also show
why theorem presence is not enough: the Lean model is deliberately compact;
some properties are true by construction or by simplified definitions. For
example, DAG acyclicity is modeled as every edge satisfying `from < to`, and
advantage normalization is modeled as replacing all values with zero.

Book addition: a proof-coupling record should carry not only theorem, module,
build, and runtime surface, but also abstraction map, semantic depth, trusted
assumptions, excluded behavior, and a negative statement of what the theorem
does not establish.

### 10. Benchmark truth is a first-class architecture layer

CCA contains explicit contracts for case identity, raw outputs, closure
eligibility, runtime binding, checkpoint/tokenizer hashes, contamination,
truth-audit verdicts, proxy-to-benchmark traces, retry lineage, and scoreboard
overlays. These should strengthen the book's benchmark-ratchet chapter.

The most important rule is inheritance: when the canonical closure gate fails,
side reports, partial bundles, and attractive component scores must inherit
`claim_ready=false`. A report cannot regain claim authority merely because it
was produced by a different adapter or summary path.

### 11. Training evidence must cross the capability boundary

CCA records large loss reduction while honest benchmarks remain near zero.
Proxy metrics also rose while benchmark outputs did not. The project therefore
supplies a strong negative lesson: optimization evidence is not capability
evidence. A training claim needs a same-lineage chain from dataset and
objective, through checkpoint and tokenizer, through runtime decode, to raw
task output, verifier, suite closure, and regression decision.

### 12. Retry policy is part of epistemic governance

Twenty-one-plus retries of materially identical failures were correctly
identified as search-for-a-better-number behavior. The book should treat retry
ceilings as anti-Goodhart controls: repeated identical reason codes stop the
family, preserve all attempts, and require a new diagnosis or intervention
before more compute is authorized.

### 13. Operational liveness belongs in evidence records

CCA distinguishes training improvement with missing bundle closure from
training-process failure. It records progress heartbeats, partial checkpoints,
loss snapshots, stale thresholds, stage gates, and fail-closed postmortems.
This belongs in artifact stewardship: a long run is not one opaque job but a
sequence of inspectable liveness and closure states.

### 14. Sovereign compute is an architectural constraint

CCA's mesh model separates interface, accelerator, storage, and coordinator
roles across owner-controlled devices, with direct-first encrypted transport,
checkpoint migration, work stealing, data locality, and revocable peer
identity. This gives the personal-compute-hives chapter a concrete role and
transport crosswalk without proving that the mesh has been deployed.

### 15. Seed entities separate compression classes

CCA distinguishes identity handles, referential lossless seeds, constructive
semantic seeds, and predictive bounded seeds. This is valuable for the compact
generative systems and artifact-compression chapters because each class has
different reconstruction dependencies, determinism, residual, and governance
requirements.

## Exact chapter crosswalk

| CCA finding | Primary ASI Stack destination | Secondary destinations | Evidence boundary |
|---|---|---|---|
| Compiler-first execution law | `integrated-reference-architecture` | `cognitive-compilation-and-semantic-ir`, `system-boundaries-and-authority` | Design and source implementation reference; no end-to-end ASI result |
| Dynamic Knowledge Lattice | proposed `durable-semantic-memory-and-knowledge-lattices` | `virtual-context-abi`, `context-transactions-snapshots-mounts-and-taint` | Chapter decision waits for BeastBrain provenance |
| SBL ambiguity/effect/receipt contracts | `cognitive-compilation-and-semantic-ir` | `human-intent-as-a-formal-input`, `intent-to-execution-contracts` | Implemented Rust record surfaces do not establish semantic extraction quality |
| Typed atom tier routing | `planning-as-a-control-layer` | `routing-heads-and-specialist-cores`, `resource-economics-and-token-budgets` | No reproduced efficiency result |
| Seven-tier commitments and bounded revision | `claim-ledgers-and-belief-revision` | `evidence-states-and-claim-discipline`, `readiness-gates-residual-escrow-and-quarantine` | Taxonomy and code reference; no open-domain belief correctness |
| Tribunal dissent and no-silent-veto | `governed-deliberation-and-test-time-scaling` | `scalable-oversight-and-adversarial-ai-control`, `moral-uncertainty-and-value-conflict` | Finite modeled controls; no reviewer independence or decision-quality result |
| Protected manifest partition | `recursive-self-improvement-boundaries` | `stable-capability-fields`, `capability-replacement-and-rollback` | Narrow record/runtime boundary only |
| Lean-to-Rust coupling | `executable-specifications-and-lean-proof-envelope` | `safety-cases-and-structured-assurance` | Compact model proofs; no whole-system safety proof |
| Benchmark truth overlays and closure inheritance | `benchmark-ratchets-and-anti-goodhart-evidence` | `evidence-states-and-claim-discipline`, `capability-thresholds-and-deployment-commitments` | Source-reported/local-project artifacts, not reproduced by the book repo |
| Proxy/benchmark divergence | `benchmark-ratchets-and-anti-goodhart-evidence` | `policy-optimization-and-learning-from-feedback` | Negative implementation lesson; exact runs not replayed here |
| Retry lineage ceilings | `benchmark-ratchets-and-anti-goodhart-evidence` | `artifact-steward-agents-and-living-project-governance` | Governance pattern, not a universal threshold result |
| Long-run heartbeats and closure state | `artifact-steward-agents-and-living-project-governance` | `artifact-graphs-audit-logs-and-replay` | Record-shape and project-history context |
| Sovereign device mesh | `personal-compute-hives-and-federated-edge-intelligence` | `security-kernel-and-digital-scifs`, `integrated-reference-architecture` | Forward design; deployment not established |
| Four seed-entity classes | `compact-generative-systems-and-residual-honesty` | `rankfold-neuralfold-and-artifact-compression` | Architecture taxonomy; compression gains unverified |
| Local data/RL/federated training surfaces | `policy-optimization-and-learning-from-feedback` | `data-engines-continual-learning-and-unlearning` | Code/config inventory, not capability or safety evidence |

## Negative lessons and non-claims

1. Falling loss did not imply benchmark capability.
2. Proxy lift did not imply transfer; the recorded trace verdict identified a
   benchmark/runtime path mismatch.
3. Historical HumanEval+ and GSM8K rows were contaminated or otherwise
   non-claim; speech adapter success conflicted with failed claim lineage.
4. Repaired or shortcut-produced answers cannot become native capability
   evidence merely because they score.
5. A correct task signature or AST-valid program is still not task competence.
6. Formal theorem counts do not measure semantic adequacy or runtime coverage.
7. A read-only field in a modeled transition does not prove an implementation
   cannot bypass the transition layer.
8. Infrastructure breadth can coexist with a central capability bottleneck.
9. Repeated retries and duplicated checkpoints can consume storage and create
   selection pressure without producing knowledge.
10. Disk exhaustion terminated staged work; storage policy is therefore part
    of operational readiness, not housekeeping.

## Storage and bloat audit

Initial apparent size: **64.45 GiB**. After the user's cleanup-first pass, the
working tree is about **21.5 GiB**; no further cleanup is in scope while idea
mining is active.

| Path family | Size | Classification | Current recommendation |
|---|---:|---|---|
| `target_workspace/` | 41.63 GiB | rebuildable Rust output | Highest-confidence reclaim after recording toolchain/lockfile and confirming no accepted evidence points into binaries |
| three `.venv*` directories | 2.81 GiB | rebuildable environments | Recreate from pinned requirements; do not include in archival source ZIP |
| `.git/` | 8.66 GiB | historical, but polluted by generated binaries | Preserve before any rewrite; omit from a lean source snapshot or keep as a separate Git bundle |
| `third_party/` | 6.64 GiB | vendored benchmarks, datasets, RL envs | Replace with upstream URL/commit/LFS manifest where possible; retain unique patches separately |
| `artifacts/` | 4.68 GiB | mixed evidence and repeated checkpoints | Keep accepted summaries, configs, raw outputs required for claims, and selected checkpoints; deduplicate or archive repeated smoke weights only after hash/lineage review |
| docs/config/crates/formal/scripts | tens of MiB | unique source | retain |

The canonical `target_workspace/` and two untracked disposable benchmark
environments were removed after tracked-file and reproducibility checks. The
tracked `.venv-bench312`, Git history, third-party sources, and mixed evidence
artifacts remain untouched.

### Git-history finding

The reachable Git object graph includes `target_workspace`, worker target
directories, compiled `.rlib`/binary files, virtual-environment libraries, and
third-party generated material. The largest current packs are measured in
gigabytes. `git gc` cannot remove reachable objects. Meaningful repository
shrinkage requires one of:

1. a fresh clean-history source mirror from the pinned snapshot;
2. a backed-up `git filter-repo`/equivalent history rewrite removing generated
   paths and large blobs; or
3. preservation of full history as a separate bundle while daily work uses a
   filtered mirror.

All three require deliberate user approval and backup verification.

### Artifact duplication finding

Many training-smoke directories contain pairs of 136,373,012-byte
`.safetensors` files, and `artifacts/training_runtime/` contains numerous
same-sized checkpoints. Equal size does not prove equality. A content-hash and
lineage pass is still required before deduplication.

## Remaining work before CCA is fully mined

- Complete symbol-level classification of lattice, governance, self-mod,
  training, and benchmark contract families.
- Inspect accepted versus diagnostic artifact families and verify which saved
  reports are internally consistent without rerunning expensive training.
- Hash repeated checkpoints and separate exact duplicates from distinct model
  states.
- Inventory unique third-party patches and pinned upstream identities.
- Compare the pinned source against BeastBrain, MoECOT, BugBrain, and Corben's
  Trainer once those projects are available, so inherited ideas are not double
  counted as independent support.
- Decide whether the durable semantic memory boundary merits a new chapter
  after BeastBrain is mined.
- Add exact claim-level source mappings only after the cross-project
  deduplication pass.
