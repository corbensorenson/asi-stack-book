# Source Note: Corben's Best Model Possible Project

| Field | Value |
|---|---|
| Source ID | `corbens_best_model_possible_project` |
| Source title | Corben's Best Model Possible recurrent-model and mechanism laboratory |
| Ingestion date | 2026-07-10 |
| Source version / URL | `local-project:corbens-best-model-possible@c61288685ca05ba773402d4a7495cfbba22c2c20` |
| Citation label | Sorenson (2026), Corben's Best Model Possible (pinned local project snapshot) |
| Source policy | Local private cache; public-safe note only; raw source, checkpoint, optimizer, corpus, and artifact trees are not copied into this repository. |
| Ingestion basis | README and research notes, Rust workspace and configurations, model/tokenizer/training/runtime/compiler/memory/router/governance/verification/tool/speech/evaluation source, retained lane-bank/checkpoint/comparison/validation artifacts, and current offline build attempts. External dependencies, training, hardware acceleration, external benchmark suites, and end-to-end model capability were not reproduced. |

## Thesis

The project is a rich implementation and negative-case reference for
shared-weight recurrent topology, fixed-feature adapter learning, lane-specific
checkpoint banks, champion/challenger architecture search, semantic task
contracts, typed memory, routing, governance, verification, tools, and speech.
Its primary book value is the contrast between sophisticated interfaces and
their actual causal effect. It motivates machine-readable distinctions between
fixed and trainable state, labeled specialist selection and autonomous routing,
record playback and live replay, named transitions and durable effects,
component ownership and useful capability, and measured metrics versus
declared, modeled, constant, proxy, fixture, or vacuous values.

## Snapshot posture

The source is pinned at Git commit
`c61288685ca05ba773402d4a7495cfbba22c2c20` on branch `main`, dated 2026-05-12.
The repository has one reachable commit and an origin for
`corbensorenson/corbens-best-model-possible`.

The worktree contains 8,286 deleted tracked artifact paths left by the earlier
cleanup pass, with no source/configuration/research path in current status.
Source analysis is pinned to the commit. Counts and conclusions about retained
results cover only the surviving artifact corpus and are not a complete census
of the pinned commit's artifacts.

The checkout is about 8.5 GiB, dominated by about 8.3 GiB of retained
artifacts. The Rust 2024 workspace contains 20 crates plus `xtask`, 27 Rust
files, about 45,704 Rust lines, and 238 direct test attributes. The surviving
artifact tree contains 129,516 files, including 3,685 model-state files, 3,685
optimizer-state files, 7,035 truth/learning/delta files, 226 comparison
reports, and 338 validation reports.

## Primary material inspected

- Root README, TODO/research log, workspace manifest, toolchain declaration,
  base model/training configuration, architecture-frontier configurations, and
  operations material.
- Model topology, deterministic feature construction, tokenizer, trainable
  readout, pooled adapter, recurrence, checkpoint, runtime, CLI, and trainer
  bridge source.
- Semantic compiler and TaskIR, memory lattice and persistence, probe router,
  governance, macro store, policy, proof/verification tribunal, tool adapters,
  audio/speech, and evaluation source.
- Promoted seven-lane adapter bank, composition metadata, lane scans,
  checkpoint markers, validation reports, training truth/metrics, and research
  summaries.
- Current offline Cargo resolution attempts using build output outside the
  project directory.

## Mechanisms

### Recurrent topology and experimental discipline

- Five unique blocks with a 16-effective-layer claim, explicit route sequence,
  preserved shell, shared recurrent core, tied controls, and reserve families.
- Dynamic recurrence research with iteration-distribution mismatch checks,
  KL/entropy halting, patience, fixed-step and latency-matched references, and
  first-hit/last-correct overthinking telemetry.
- Frozen control and mutable experimental arms, single-axis challengers,
  same-budget/equal-step comparisons, stage overlays, promotion/reset behavior,
  negative-result retention, and family retirement.
- Checkpoint composition with explicit base, candidate, alpha, and optimizer
  moment policy.

### Trainable state and specialists

- Deterministically generated token embeddings, feature blocks, controls, and
  tied output geometry.
- Frozen inner trunk in the serious path; implemented updates are low-rank
  byte-sequence readout or pooled-hidden adapter.
- Approximate 93,496-scalar low-rank readout at base dimensions, dominated by a
  65,536-value position-specific byte-bias table.
- Seven explicitly addressed lane adapters for code, instruction, math, paper,
  proof, semantic compiler, and tool/API tasks.
- Fixed validation offsets and lane regression matrices.
- Explicit bank truth note denying automatic prompt-lane inference or trained
  trunk routing.

### Compiler and runtime contracts

- Task spell with role, objective, modality, context, constraints, acceptance
  tests, non-goals, risk, budgets, procedure, output contract, verification,
  failure behavior, and immutable contract hash.
- Extract/normalize/type/dependency/lint/dedupe passes, semantic and target IR,
  TaskIR, retrieval node, tool node, verification node, and localized repair
  scope.
- Separate ordinary solve and outer-system paths.
- Fail-closed external specialist requirement for claim-bearing math.

### Memory, routing, and governance

- Typed memory nodes and edges, justification requirement for durable claims,
  replay windows, goal-aware retrieval, information gain, hot/warm/cold tiers,
  freeze/thaw decisions, reserve writes, and ephemeral audio treatment.
- Router over stakes, evidence gap, reversibility, uncertainty, latency, and
  burst budget with selected/fallback routes and typed reasons.
- Belief, contradiction, review, entrenchment, commitment, downgrade,
  quarantine, rollback, and anti-expert telemetry surfaces.

### Verification, tools, evaluation, and speech

- Tribunal rows for structure, exactness, semantics, residuals, challenges,
  proof, replay, capability, and translation.
- File tools and a generic executable tool with capability declarations.
- Evaluation metadata for execution, tools, memory, tribunal, hardware,
  replay, capability density, compounding, regressions, and speech.
- Local acoustic feature processing, benchmark tone-symbol codec, tone-based
  synthesis, alignment/stability metadata, and first-party ownership report.

## Evidence

### Model and training truth

The inspected model path is a deterministic feature generator, not a trained
foundation-model trunk. Token embeddings and feature blocks are derived from
fixed seeds. Hidden vectors serve directly as attention queries, keys, and
values. Quantization is deterministic rounding. The output uses tied generated
embeddings.

The trainer bridge states that the HRC/prime-cycle trunk is frozen. The list of
trainable-trunk-ready backends is empty, and serious plans can fail closed when
trainable trunk state is required. Low-rank validation is autoregressive over
previous predicted bytes. The pooled adapter repeats one predicted token for
all target positions, so general exact-sequence claims are inadmissible for that
path.

Runtime responses are produced through local math/specialist logic rather than
a general checkpoint-driven autoregressive decoder. Training metrics therefore
do not establish general text generation or causal improvement of returned
answers.

### Tokenizer truth

The tokenizer combines special IDs, bytes, hard-coded bigrams, and hashed
wordpiece buckets. Hashed words decode as `<wp>` and collisions are not tracked.
Training targets use an ASCII-byte mapping distinct from input tokenization.
Tokenizer size, target vocabulary, and reversible decode must be treated as
separate facts.

### Adapter-bank truth

The promoted bank contains seven lane-specific adapter bindings and a default
linear-delta composition. It requires explicit lane metadata. It does not
implement automatic lane inference. Several stored paths are absolute paths
under another user's home directory; the inspected resolver does not relocate
those references automatically, so the promoted bank is not directly portable
from the current checkout.

A retained paper-specialist scan reports local validation loss improvements on
the paper lane and bank mean. Other lane deltas are zero because those adapters
were unchanged. This is evidence of artifact isolation under explicit lane
binding, not autonomous routing or absence of shared-trunk interference.

### Integration truth

The ordinary solve path uses default router probe features, a fresh empty
memory bundle, compiler emission booleans, and a scaffold macro-store summary.
The outer-system path constructs actual TaskIR and retrieval structures, but
memory is per-request and coding/task tools inspect predetermined repository
files rather than execute the requested task. Interface presence and runtime
effect are therefore separate evidence states.

### Compiler truth

Compiler directives are prefix- and keyword-driven, and the plan graph is
primarily linear. “Cross-stage digest parity” computes FNV digests and compares
their full hex strings using token-set Jaccard, effectively an equality check on
unrelated hash values rather than semantic preservation. Localized repair uses
positional node identities and adjacency. These are useful scaffolds but do not
establish semantic compilation correctness or proof of intent preservation.

### Memory truth

Typed edges and justification gates are useful. Several named transitions do
not establish durable effects: freeze/thaw can be trace-only; tier updates can
be lost across restart; reserve promotion does not install canonical content;
defaults are permissive; goal drift compares hash-character sets; and JSONL
plus index updates are not a fully atomic, fsynced transaction. Node identity
uses a 64-bit non-cryptographic hash and excludes some policy fields.

### Router and governance truth

The router is a substantial deterministic policy when supplied real features.
Normal solve supplies defaults and recreates the budget. Its calibration method
fits score quantiles while ignoring outcome fields, so it is not outcome
calibration. Governance exposes strong types, but contradiction response is
non-monotone and review evidence is largely string/artifact-presence based.

### Verification, tool, and replay truth

Proof fail-closed behavior is a positive mechanism. Other tribunal rows can be
shape/string predicates, share the same evidence source, or pass vacuously.
The generic code tool can execute an arbitrary program, while the declared
capability envelope is not comprehensively enforced at the operating-system
boundary. Retained payload replay for non-live tools is playback after input
hash comparison, not re-execution and comparison.

### Metric provenance truth

Some apparent latency/token metrics are prompt-length formulas; scoring and
compounding fields contain fixed bonuses or constants; `verified_per_param` is
not derived from an inspected parameter count; public authenticity relies on
metadata strings; empty replay can pass; and missing simulation metadata can
default to real/hardware-shaped classifications. These observations motivate a
machine-readable origin class for every metric.

### Speech truth

Ordinary audio becomes feature-hashed acoustic-unit labels. A benchmark capture
encodes characters as distinct tones and decodes them by frequency matching.
Synthesis maps text bytes to short tones. First-audio latency is a configured
style constant. The code is first-party and local, but the retained evidence
does not establish ordinary speech recognition, natural synthesis, or measured
device latency.

## Claims To Add Or Update

### Recommended additions

- Trainable-state manifest: generated, frozen, pretrained, trainable, and
  actually updated tensors.
- Response-causality receipt from checkpoint and prompt through decode and tool
  substitutions to final response.
- Metric provenance algebra: measured, derived, recomputed, modeled, fixture,
  constant, declared, proxy, vacuous, or unknown.
- Verification-method labels and independence graph.
- Representation-capacity gate for evaluation metrics.
- Specialist/router evidence ladder from checkpoint existence to autonomous,
  calibrated, end-to-end routing.
- Transaction postconditions and restart-visible validation for named memory
  transitions.
- Relocatable artifact identity using content digests rather than authoritative
  absolute paths.
- Negative-knowledge configuration frontier with retirement and recombination
  constraints.
- Ownership/capability matrix for local and first-party components.
- Fixed-step quality authority and first/last-correct trajectories for adaptive
  recurrence.
- Request-feature provenance, persistent budget ownership, and outcome-linked
  router calibration.

## Book Chapters Supported

- `routing-heads-and-specialist-cores`
- `system-boundaries-and-authority`
- `security-kernel-and-digital-scifs`
- `governed-deliberation-and-test-time-scaling`
- `cognitive-compilation-and-semantic-ir`
- `integrated-reference-architecture`
- `open-ended-improvement-engines`
- `recursive-self-improvement-boundaries`
- `evidence-states-and-claim-discipline`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `artifact-graphs-audit-logs-and-replay`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `claim-ledgers-and-belief-revision`
- `spinoza-verification-and-proof-carrying-claims`
- `context-transactions-snapshots-mounts-and-taint`
- `runtime-adapters-tool-permissions-and-human-approval`
- `readiness-gates-residual-escrow-and-quarantine`
- `executable-specifications-and-lean-proof-envelope`
- `intent-to-execution-contracts`

No project-specific chapter is recommended. A separate metric-provenance or
causal-capability-receipt boundary remains deferred until cross-project
deduplication.

## Failure Modes

- Fixed, deterministically generated state can be described with model-shaped
  language that obscures the absence of trained trunk weights.
- Adapter learning and runtime answer production are not causally connected by
  a general checkpoint-driven decode path.
- Position-specific byte bias can provide a high-capacity shortcut.
- A pooled adapter is evaluated with a sequence metric despite emitting one
  repeated token distribution.
- Specialist-bank selection depends on explicit lane metadata rather than a
  held-out autonomous router.
- Zero deltas on unchanged lane adapters can be narrated as zero interference.
- Absolute checkpoint paths prevent artifact relocation.
- Ordinary runtime use reduces router, memory, compiler, and macro-store
  subsystems to default, empty, boolean, or scaffold states.
- Digest equality is labeled cross-stage semantic parity.
- Named memory transitions can emit traces without durable material effects.
- Router budgets are recreated and calibration ignores outcomes.
- Contradiction response is non-monotone in evidence strength.
- Verification and replay can be string/shape based, dependent, playback-only,
  or vacuously true.
- Capability declarations are not comprehensively enforced by the operating
  system boundary.
- Missing simulation metadata can default to real-execution classifications.
- First-party speech ownership can be mistaken for ordinary STT/TTS capability.

## Book Chapters Supported

- `routing-heads-and-specialist-cores`
- `system-boundaries-and-authority`
- `governed-deliberation-and-test-time-scaling`
- `cognitive-compilation-and-semantic-ir`
- `integrated-reference-architecture`
- `open-ended-improvement-engines`
- `recursive-self-improvement-boundaries`
- `evidence-states-and-claim-discipline`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `artifact-graphs-audit-logs-and-replay`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `claim-ledgers-and-belief-revision`
- `context-transactions-snapshots-mounts-and-taint`
- `runtime-adapters-tool-permissions-and-human-approval`
- `readiness-gates-residual-escrow-and-quarantine`
- `executable-specifications-and-lean-proof-envelope`
- `intent-to-execution-contracts`

## Claims To Add Or Update

These are argument-level design claims for later drafting, not promoted
empirical support:

1. Parameter counts should identify generated, frozen, pretrained, trainable,
   and actually updated state.
2. A capability claim needs a causal receipt from checkpoint and request through
   decode, tools, and substitutions to the returned result.
3. A specialist bank, oracle lane binding, autonomous routing, calibrated
   fallback, and end-to-end routing gain are separate evidence states.
4. Evaluation metrics are inadmissible when the evaluated architecture cannot
   represent the target class.
5. Every metric should expose whether it is measured, derived, recomputed,
   modeled, fixture-generated, constant, declared, proxy, vacuous, or unknown.
6. Verification strength depends on method and independence, not the number or
   names of tribunal rows.
7. Freeze, thaw, promotion, compaction, and replay require material
   postconditions that survive restart.
8. Artifact identity must be content-addressed and relocation-safe.
9. Adaptive-compute promotion should be governed by fixed-step quality and
   measured resource counterfactuals.
10. First-party ownership and local execution do not establish semantic task
    capability.

## Formal semantic-depth boundary

- Named proof or tribunal rows, schema presence, shape validation, fixture
  playback, live executable replay, and a causally bound implementation are
  distinct depth lanes.
- Vacuous or empty-case checks are an attractive invalid proof surface: a green
  verifier row is not semantically adequate when the modeled case cannot fail
  or does not bind the runtime path being claimed.
- The project's offline build failures and missing dependencies preserve an
  implementation-binding residual; source structure cannot substitute for a
  current executable observation.

## Open Questions

- Which recurrence, memory, compiler, tribunal, and governance concepts
  originated in this project versus CCA, MoECOT, BeastBrain, or BugBrain?
- How much of the low-rank validation signal remains after removing the
  position-specific byte-bias table?
- Can any surviving checkpoint be relocated and loaded without rewriting its
  bank manifest?
- Does checkpoint perturbation causally alter decoded runtime response text?
- Can a held-out router outperform a single adapter without oracle lane labels?
- Which memory transitions remain observable after process restart?
- Which tribunal rows survive adversarial semantic counterexamples?
- Can every evaluation field be assigned a machine-readable metric-origin
  class without ambiguity?
- What natural-audio and human-intelligibility results exist, if any, outside
  the retained tone-codec fixtures?
- Which source-reported green checks can be reproduced with the requested
  toolchain and pinned dependencies?

## Failure Modes

- Treating fixed generated features, a frozen trunk, or adapter-only updates as
  evidence of general model learning or capability improvement.
- Calling explicitly labeled lane selection autonomous routing or calibrated
  specialization.
- Treating playback, shape checks, or vacuous tribunal rows as live replay,
  independent verification, or durable semantic preservation.
- Allowing permissive defaults, absolute artifact paths, non-atomic memory
  transitions, or missing-data classifications to silently widen a claim.
- Reporting derived, proxy, fixture, constant, or declared metrics as measured
  model, hardware, speech, efficiency, or benchmark results.

## Validation posture

Source contains many tests and research notes report historically green tests,
Clippy, release reports, and kernel parity. A current offline test attempt
stopped before compilation because cached dependencies were missing. A
source-only temporary workspace without `xtask` reached a second missing
dependency. The requested Rust toolchain was not available locally in the
restricted environment. No current pass count is inferred.

## Promotion blockers

- incomplete surviving artifact corpus relative to the pinned commit;
- no reproduced current build or tests;
- frozen deterministic trunk and adapter-only learning;
- no general checkpoint-driven text-generation path;
- explicit/oracle lane binding rather than autonomous routing;
- absolute, non-relocatable checkpoint paths;
- fixture/default/empty integration on ordinary runtime paths;
- semantic-preservation and memory-durability gaps;
- incomplete capability-envelope enforcement and replay semantics;
- mixed metric provenance and unsafe missing-data defaults;
- speech codec evidence rather than general speech evidence;
- missing independent literature, evaluation, and publication permission.

## Non-claims

This source note does not establish model capability, full-trunk learning,
general generation, autonomous routing, external benchmark success, semantic
compiler correctness, durable memory, safe arbitrary tool execution,
deterministic live replay, natural speech, measured efficiency, recursive
compounding, safety, AGI, ASI, or a support-state transition.
