# Source Note: Corben's Trainer Project

| Field | Value |
|---|---|
| Source ID | `corbens_trainer_project` |
| Source title | Corben's Trainer epistemic training and evaluation control plane |
| Ingestion date | 2026-07-10 |
| Source version / URL | `local-project:corbens-trainer@59a57333b819a64f2ed70c077c4dbdb917337b1c` |
| Citation label | Sorenson (2026), Corben's Trainer (pinned local project snapshot) |
| Source policy | Local private cache; public-safe note only; raw project and artifact trees are not copied into this repository. |
| Ingestion basis | README and architecture documents, workspace manifests, typed schemas, registry, trainer, benchmark, artifact, core, report, CLI and UI source, retained run/session/artifact database records, benchmark authenticity and quarantine records, claim evaluations, corpus provenance, and a current offline test attempt. External dependencies, real training, hardware accelerators, external benchmark suites, and end-to-end public claims were not reproduced. |

## Thesis

Corben's Trainer is an implementation reference for governing model-development
experiments as typed, artifact-bearing, evidence-gated transactions. Its
strongest contributions are manifest compilation, trainer/backend separation,
durable campaigns, content-addressed artifacts, learning-truth gates, benchmark
mode and authenticity separation, evidence graphs, and report derivation from
run facts. Its retained artifacts also show why these interfaces must enforce
real seed identity, content pins, sample-level decontamination, transitive
quarantine, and acknowledged checkpoint completion.

## Snapshot posture

The source is pinned at Git commit
`59a57333b819a64f2ed70c077c4dbdb917337b1c` on branch `main`. The worktree is
clean, the repository has one reachable commit, and the origin names the
`corbensorenson/corbens-trainer` GitHub repository. The snapshot has 626 tracked
files and is about 765 MiB, dominated by 539 MiB of retained artifacts and 128
MiB of examples.

The Rust 2024 workspace contains 14 crates, about 84,461 Rust source lines, and
285 test attributes. A current offline workspace test attempt stopped before
compilation because the Cargo cache lacked the `time` dependency. No current
workspace pass is claimed.

## Primary material inspected

- Root README, trainer plan, architecture and integration documents, TODO, and
  example plans.
- Workspace, schema, registry, executor, resource, training/campaign, RL,
  benchmark, artifact, core evidence, report, CLI, and UI source.
- Retained SQLite artifact index and run/artifact/session file trees.
- Run records, journals, evidence bundles, evidence graphs, research ledgers,
  claim evaluations, integrity quarantines, comparisons, checkpoints, and
  session failure histories.
- Benchmark registry fixtures, authenticity audit behavior, imported LongCoT
  material, and external benchmark-labelled runs.
- `corben_frontier_multilane.v2` JSONL, provenance, registry record,
  materializer, split policy, quality metadata, and content digest.
- Current offline Cargo test attempt with build products directed outside the
  project tree.

## Mechanisms

### Typed epistemic control plane

- Versioned dataset, environment, benchmark, rule, claim, executor, training,
  RL, holdout, resource, and campaign assets.
- Registry validation and plan compilation.
- Trainer-first doctrine: core policy and evidence stay generic; project code
  adapts at controlled edges.
- External backends for real project training and inference, plus explicitly
  demonstrative adapters.

### Campaign and learning governance

- Dependency-ordered campaign stages with retry, failure, checkpoint,
  invalidation, continuation, and terminal state.
- Atomic-ish session-state replacement with temporary file, `sync_all`, backup,
  rename, load validation, and backup recovery.
- Learning-evidence policy requiring truth report, parameter updates, optimizer
  steps, step agreement, losses, validation metrics, checkpoint delta, and
  optional proxy rejection.
- Holdout watchdogs with score floors and regression limits.

### Artifacts and evidence

- SHA-256 content-addressed blobs.
- Run-artifact role bindings, lineage edges, checkpoint ledger, evidence bundle
  index, and immutable run journals.
- Evidence graph and deterministic research ledger materialization.
- Claim policy over asset versions, public-claim mode, repeated seeds,
  thresholds, confidence intervals, and time to quality.
- Operator summaries, failure diagnoses, comparisons, and wedge aggregates
  derived from retained facts.

### Benchmark governance

- Separate benchmark assets, rule assets, evaluation modes, claims, and
  evidence-materialization policy.
- Internal-evaluation, blind-holdout, and public-claim modes.
- Authenticity classification and placeholder-fixture detection.
- Integrity quarantine sidecars and report-level exclusion of quarantined runs.

### Dataset and resource governance

- Dataset taxonomy, provenance, license, cleaning, snapshot, dedup,
  contamination declaration, protected exclusions, quality, streaming, cache,
  and mixture fields.
- Resource profiles and accelerator resolution for CUDA, ROCm, MLX, and CPU.
- Fixed budgets, repeated-seed policies, sweeps, campaign DAGs, checkpointing,
  and complexity/quality gates.

## Retained corpus observations

- 173 run records, 150 journals, 150 evidence bundles, 81 indexed checkpoints,
  15 claim evaluations, 29 active quarantines, 8 evidence graphs, 8 research
  ledgers, and 2 pairwise comparisons.
- SQLite contains 1,515 artifacts, 2,159 run bindings, 1,054 lineage edges, and
  one promotion label.
- The only retained promotion label is `candidate.current`; it points to a
  later-quarantined Terminal-Bench-labelled run and does not identify an
  artifact.
- All 173 run records have null typed seed and code snapshot fields.
- All 150 journals have null code and source-snapshot digests.
- Twenty-nine quarantines cite synthetic placeholder benchmark fixtures.
- HumanEval+-, IFEval-, and Terminal-Bench-labelled claims recorded `Promote`
  before all five evidence runs used by each were quarantined.
- Report aggregation now excludes active quarantines, but canonical claim and
  promotion state was not transitively revoked.

## Evidence

### Experimental identity

When benchmark metadata lacks a seed, evidence collection hashes the run ID and
uses that value as the seed. Distinct run names can therefore satisfy the
repetition count without distinct stochastic interventions. Retained typed seed
fields are null. Reproducibility, repeated execution, and independent sampling
must remain distinct evidence states.

### Dataset verification

The generic preflight calls a 64-bit hash of the dataset ID a `sha256:`
`dataset_checksum`; nonemptiness contributes to `dataset_pin_verified`. Registry
admission verifies required declarations, not the actual local bytes. The
48,000-row frontier corpus separately has a real matching SHA-256 digest, but
that stronger fact is not what the generic field computes.

The registry overlap scan checks whether benchmark identifier strings are
covered by declared exclusion or canary lists. It does not scan sample content.
Declaration coverage is valuable but is not sample-level decontamination.

### Corpus quality

The frontier corpus contains 43,200 training and 4,800 validation rows across
seven task lanes. Its content digest matches provenance and it is marked
internal-only. The validation set is normally selected every tenth row from the
same generators, so it is reproducible but not demonstrably independent. The
materializer writes clean contamination fields by construction, and its
quality metadata records suspicious answer endings without making them a hard
gate. Absolute machine-specific source paths remain in provenance fields.

### Benchmark authenticity

Many registry entries behind industry benchmark names are three-row starter
fixtures lacking official provenance. Later source introduces authenticity
states and quarantines. The correction is positive evidence of governance
evolution; it does not retroactively validate earlier scores.

### Promotion and revocation

Claim evaluation checks run validity, asset versions, mode, distinct seed
values, mean, interval width, and target. It does not consume quarantine state.
The CLI writes `candidate.current` on promotion. The later report layer can
reject quarantined runs, but no automatic closure revokes the claim evaluation
and database label. Promotion must be a revocable lease over an exact artifact,
not a stale run pointer.

### Checkpoint durability

The async checkpoint worker has staging and completion records, but the worker
discards the returned result. Early errors can occur before the failed-marker
branch, and `wait_for_idle` checks queue count rather than terminal success.
Checkpoint and progress JSONL appends rewrite the whole file. A book-grade
checkpoint protocol needs per-request acknowledged terminal outcomes and
restart reconciliation.

### Audit-chain semantics

Session journals use a 64-bit non-cryptographic hash chain. They can compact by
discarding an old prefix without a retained segment anchor. This is useful
corruption detection, not a cryptographic or complete-history guarantee.

### Database constraints

The artifact database enables the SQLite foreign-key pragma, but the inspected
schema declares no `REFERENCES` constraints. Promotion labels may have null
artifact IDs. Relationship integrity is therefore primarily application-
enforced.

### Strong fail-closed evidence

Retained session histories show active rejection of:

- missing backend training-truth reports;
- missing positive checkpoint deltas;
- environment compatibility mismatch;
- deterministic replay mismatch;
- materialization timeouts;
- holdout scores below declared floors.

This supports the narrow claim that these rejection paths were exercised in
the retained snapshot. It does not prove all training or promotion paths fail
closed.

## Claims To Add Or Update

1. Trainer as a separate epistemic institution around mutable model kernels.
2. Experiment constitutionalism through typed, compiled assets.
3. Durable campaigns with bounded continuation, failure retention, and
   dependent-stage invalidation.
4. Learning-truth contracts that separate orchestration completion from actual
   parameter-changing learning.
5. Content-addressed artifact graphs with roles and lineage.
6. Run-fact-derived operator views.
7. Benchmark asset/rule/mode/claim separation.
8. Benchmark authenticity state rather than registry-name readiness.
9. Actual experimental seed identity rather than run-ID diversity.
10. Transitive quarantine, revocation, and promotion-lease invalidation.
11. Declaration coverage versus empirical decontamination.
12. Content digest versus identifier fingerprint.
13. Reproducible split versus independent split.
14. Acknowledged asynchronous checkpoint outcomes.
15. Hash-chain threat models and compaction anchors.
16. Requested, resolved, and observed resource receipts.
17. External backend sovereignty through thin adapters.
18. Complexity governance for the control plane itself.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`

Primary existing routes:

- `evidence-states-and-claim-discipline`
- `artifact-graphs-audit-logs-and-replay`
- `integrated-reference-architecture`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `recursive-self-improvement-boundaries`
- `open-ended-improvement-engines`
- `system-boundaries-and-authority`
- `security-kernel-and-digital-scifs`
- `resource-economics-and-token-budgets`
- `readiness-gates-residual-escrow-and-quarantine`
- `procedural-memory-and-cognitive-loop-closure`
- `artifact-steward-agents-and-living-project-governance`

No new chapter is proposed yet. The epistemic-control-plane concept should be
deduplicated after Corben's Best Model Possible is mined.

## Failure Modes

- Letting a run identifier substitute for an actual stochastic seed or code
  snapshot.
- Treating registry declarations or benchmark names as content-level
  provenance, authenticity, or decontamination evidence.
- Promoting an artifact through a stale claim record after a linked run or
  fixture has been quarantined.
- Treating queued checkpoint work, a content address, or a hash chain as a
  complete durability, crash-safety, or tamper-evidence guarantee.

## Open Questions

- Can the trainer's generic dataset preflight bind declarations to the actual
  local bytes for every admitted dataset rather than an identifier-derived
  fingerprint?
- Can claim evaluation and promotion consume transitive quarantine state and
  bind a revocable lease to an exact artifact?
- Can checkpoint completion be made acknowledged and restart-reconciled for
  every request rather than inferred from queue idleness?
- Which current external-backend and holdout workflows can be reproduced with
  pinned code, content, seed, and environment identity?

## Evidence State

This is a local private implementation reference. It is eligible for
claim-specific source review and chapter argument, but it does not promote a
chapter-core support state. Reproduced workspace tests, independent literature,
authentic benchmark replay, transitive revocation tests, content-pin
verification, and publication permission remain blockers.

## Non-claims

- No model-quality or external benchmark claim is accepted.
- Quarantined runs do not support industry comparison.
- Run-ID hashes are not treated as real seeds.
- Registry declarations are not treated as content-level decontamination.
- The frontier corpus is not claimed clean, independent, or semantically
  diverse.
- A content-addressed store is not claimed crash-safe or tamper-proof.
- The Rust workspace is not claimed currently green.
- No production reliability, safety, AGI, ASI, or support-state promotion is
  claimed.
