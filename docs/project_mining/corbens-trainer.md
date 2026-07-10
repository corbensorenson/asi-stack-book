# Corben's Trainer Project Mining Dossier

Date: 2026-07-10

Project: local historical project `Corben's Trainer` (private source checkout; path intentionally omitted)

Pinned revision: `59a57333b819a64f2ed70c077c4dbdb917337b1c`

## Executive conclusion

Corben's Trainer is best understood as an epistemic control plane for model
development. It does not primarily implement a new model architecture. It
defines typed contracts around datasets, environments, executors, training
plans, campaigns, checkpoints, benchmarks, claims, evidence, promotion, and
operator reports, then delegates actual project-specific training and inference
to adapters. That division is highly relevant to the ASI Stack: a system that
can improve itself needs a durable institution for deciding what was run, what
changed, what evidence is admissible, and which candidate—if any—may advance.

The project contains unusually strong positive mechanisms:

- manifest and registry assets for datasets, environments, benchmarks, rules,
  claims, executors, training plans, RL plans, and campaign DAGs;
- content-addressed artifacts, run-role bindings, lineage edges, immutable run
  journals, evidence graphs, and deterministic research ledgers;
- separate internal-evaluation, blind-holdout, and public-claim modes;
- explicit benchmark authenticity states and later quarantine sidecars;
- learning-evidence gates that require real updates, optimizer steps, losses,
  validation metrics, and nonzero checkpoint deltas;
- durable campaign sessions with retry history, failure retention, backup
  recovery, continuation limits, and invalidation records;
- a trainer-first adapter doctrine that keeps project-shaped compatibility at
  the edge rather than in the central schema;
- resource, accelerator, budget, sweep, campaign, checkpoint, and report
  surfaces broad enough to support a future evidence-gated improvement loop.

The retained implementation and artifacts also expose several high-value
failure modes that the book should turn into explicit invariants:

- a missing benchmark seed falls back to a hash of the run ID, so distinct run
  names can masquerade as distinct experimental seeds;
- all 173 retained run records have a null typed `seed`, and all have a null
  `code_snapshot`, even though claim evaluation can still count repetitions;
- a pre-training field called `dataset_checksum` is a 64-bit stable hash of the
  dataset ID, not a digest of dataset content, while `dataset_pin_verified` can
  still be true;
- the registry “overlap scan” checks whether declared benchmark identifiers are
  covered by exclusion declarations; it does not scan sample contents;
- 29 runs were retroactively quarantined for using synthetic placeholder
  benchmark fixtures, yet a `candidate.current` promotion label still points at
  one of those runs;
- three external-looking claims were recorded as `Promote` before every one of
  their used evidence runs was quarantined;
- asynchronous checkpoint worker errors can be discarded before a failed
  marker is written, and queue idleness does not prove checkpoint success;
- campaign-session journals use a non-cryptographic 64-bit hash chain and can
  compact away their earlier prefix;
- the SQLite schema stores rich relationships but declares no foreign-key
  relationships, and a promotion label may omit the promoted artifact ID;
- a 48,000-row training corpus is reproducibly pinned, but its contamination
  fields are populated by construction rather than sample comparison, and its
  deterministic validation split can share generators and template families
  with training.

These are not reasons to discard the project. They make it a particularly
useful source for the book's distinction between evidence-shaped structure and
end-to-end epistemic validity. The central design lesson is: the control plane
must derive every public claim from transitive, revocable, independently
identified evidence—not merely from the presence of manifests, repeated run
IDs, green fields, or report files.

The project does not establish model superiority, authentic external benchmark
performance, production training reliability, decontaminated data, independent
evaluation, safety, AGI, or ASI.

## Snapshot identity and source boundary

The repository is on branch `main` at commit
`59a57333b819a64f2ed70c077c4dbdb917337b1c`, dated 2026-05-12 with subject
`Back up current corbens-trainer state`. The worktree is clean. The repository
contains one reachable commit and records an origin for
`corbensorenson/corbens-trainer` on GitHub. A one-commit history pins the
present tree but supplies little development-history provenance.

The snapshot contains 626 tracked files and is about 765 MiB. Approximate
top-level contributions include 539 MiB under retained artifacts, 128 MiB under
examples, 44 MiB under crates, and 53 MiB under `.git`. No more storage cleanup
was performed after the user redirected the work to idea mining.

Private project material remains outside the public book repository. This
dossier records public-safe mechanisms, counts, contradictions, and book
routes. It does not copy raw benchmark cases, model weights, credentials,
private logs, or the retained artifact database into the book.

## Structural inventory

### Rust workspace

The Rust 2024 workspace contains 14 crates and about 84,461 Rust source lines.
The largest surfaces are approximately:

- CLI: 23,265 lines;
- training and campaign orchestration: 17,579 lines;
- typed schemas: 9,208 lines;
- reporting and operator views: 8,155 lines.

The remaining crates cover core identities and evidence structures, artifacts,
registry, executor, benchmark, RL, UI, resources, and related integration
surfaces. The workspace forbids unsafe Rust and configures strict Clippy rules,
including denied `unwrap` and `dbg` use. Source contains 285 Rust test
attributes.

A current offline workspace test attempt routed build output to `/private/tmp`
but stopped before compilation because the local Cargo cache did not contain
the `time` dependency. No pass count is inferred. Test-shaped retained
artifacts and source tests are therefore implementation references, not a
reproduced green workspace.

### Manifest and registry surface

The project defines typed assets for:

- datasets, mixture bundles, provenance, governance, snapshot pins,
  decontamination declarations, quality filters, streaming shards, and cache
  policy;
- environments, compatibility modes, deterministic replay expectations,
  modalities, and evaluation-only state;
- benchmark assets, scoring rules, claims, holdouts, evaluation modes,
  authenticity state, evidence-materialization policy, and runtime
  capabilities;
- training plans, learning-evidence requirements, fixed budgets, seeds,
  checkpoints, resource profiles, optimization strategies, and external
  backends;
- RL plans, environment bindings, replay, collection, policy update, and
  health audit;
- campaign runtimes and dependency-ordered stages from preparation through
  training, evaluation, holdout, and export;
- executors, source snapshot policy, workspace policy, accelerator support,
  and artifact contracts.

This is a concrete example of “experiment constitutionalism”: the admissible
experiment is compiled from typed, versioned policy rather than assembled from
unrecorded shell conventions.

### Retained artifact corpus

The inspected artifact tree contains roughly 16,490 files, including:

- 13,525 JSON files and 303 JSONL files;
- 173 `run_record.json` files;
- 150 run journals and 150 evidence bundles;
- 81 indexed checkpoints;
- 15 claim evaluations;
- 29 active `integrity_quarantine.json` sidecars;
- 8 evidence graphs and 8 research ledgers;
- 2 pairwise comparison JSON files;
- thousands of checkpoint-path files and model-state fragments.

The SQLite artifact index contains 1,515 artifacts, 2,159 run-artifact
bindings, 1,054 lineage edges, 150 run directories, 150 run journals, 150
evidence bundles, 81 checkpoints, zero aliases, and one promotion label.
Recorded lineage relations include 717 `derived_from`, 310 `produced_from`,
and 27 `included_in_evidence_bundle` edges.

These counts show that the evidence plane was exercised. They do not establish
that every recorded object is authentic, complete, or suitable for a public
claim.

## Architecture mined for the book

### 1. Treat the trainer as an epistemic institution, not a loss-loop wrapper

The project separates model-specific computation from the system that governs
it. The trainer owns identities, admissibility, scheduling, budgets, evidence,
checkpoint roles, comparison, claim evaluation, and reports. An external
adapter owns the actual project kernel. This is a stronger architecture than a
monolithic training script because the improvement loop can change model
implementation without silently changing the meaning of evidence.

The book should define a trainer control plane with at least:

1. immutable experiment identity;
2. source, configuration, data, environment, and evaluator snapshots;
3. typed resource and authority budgets;
4. a stateful campaign DAG;
5. artifact and checkpoint lineage;
6. benchmark authenticity and visibility mode;
7. claim-specific evidence selection;
8. promotion, quarantine, revocation, and rollback state;
9. views derived from canonical run facts;
10. explicit non-claims and unresolved residuals.

The project phrase “trainer-first” is useful: legacy repositories should adapt
at stable ports, while the control plane should not accumulate one-off fields
for every old project. That principle also protects the meaning of evidence
from adapter-specific convenience behavior.

### 2. Compile experiments from typed assets

Datasets, benchmarks, rules, claims, executors, and plans are separately
identified. That separation matters. A benchmark dataset is not the scoring
rule; a scoring rule is not the publication policy; a training dataset is not
its provenance declaration; an executor is not a claim; and a plan is not a
completed run.

The book should present an experiment compiler that rejects incompatible asset
combinations before execution and emits canonical plan JSON. Every compiled
experiment should expose its exact asset versions, migration path, evaluator
identity, visibility mode, expected artifact roles, and allowable claim scope.

### 3. Campaigns need durable stage state and bounded continuation

The campaign runtime models preparation, input materialization, supervised
warm-start, RL collection, RL update, internal benchmark, holdout benchmark,
and export as ordered stages. Session state retains completed stages, cached
outputs, checkpoints, failures, retries, invalidations, continuation count,
quality history, readiness, and terminal transitions.

Session persistence writes a temporary file, flushes and `sync_all`s it, keeps
a backup of the previous primary, and renames the temporary file into place.
Load validates a journal hash chain and can recover from the backup. This is a
strong minimum pattern for long-running improvement campaigns.

The retained 38 top-level session states include completed, failed, running,
and older states without a current terminal value. Failures are not erased.
Examples include:

- 27 recorded attempts rejecting warm-start stages because the backend did not
  emit `training_truth_report.json`;
- RL updates rejected for missing a positive checkpoint delta, followed by a
  later attempt rejected for a missing truth report;
- environment health audits rejecting a compatibility-mode mismatch and a
  deterministic-replay mismatch;
- materialization stages timing out while preserving observed queue state;
- holdout watchdogs rejecting scores below declared floors, including retained
  scores of 0.6137 against 0.6500 and 0.6200 against 0.7200.

The lesson is broader than retry support. A campaign should preserve the
failure as evidence, distinguish retryable execution failure from epistemic
rejection, invalidate dependent stages, and spend a bounded continuation
budget. Repeatedly retrying a deterministic evidence failure without changing
its cause is not new evidence.

### 4. Prove that learning occurred before accepting a training stage

The learning-evidence policy is one of the strongest reusable mechanisms. For
warm-start and RL-update stages it can require:

- a backend truth report declaring actual training and applied parameter
  updates;
- an optimizer-step curve and a positive integral optimizer-step count;
- `step_accounting.json` with a positive increment and consistent global step;
- exact agreement between optimizer-step count and the step increment;
- finite training loss, validation loss, and bounded validation accuracy;
- a positive checkpoint or parameter delta;
- explicit rejection of proxy-derived signals.

The retained failures demonstrate that these checks are active in the runtime,
not only described in documentation. This should become a book invariant:
“training completed” is an inadmissible state unless the system can distinguish
parameter-changing learning from orchestration success, replay, fixed metrics,
or a copied checkpoint.

The contract should be strengthened further by binding every truth field to an
artifact digest and, where feasible, recomputing step and checkpoint deltas
outside the backend. A backend-authored Boolean is a claim to verify, not the
verification itself.

### 5. Separate run facts from operator views

The reporting crate materializes summaries, failure diagnoses, wedge
aggregates, comparison reports, dashboards, and UI state from retained run
facts. This is an important book pattern: different views should not carry
independent truth. They should be projections over the same canonical,
versioned evidence graph.

This pattern is partly realized. The report layer excludes actively
quarantined runs from aggregate industry comparisons and can override a
promotion-looking result with `Reject`. The underlying claim evaluation and
database promotion label, however, remain stale. Derived views are only safe
when invalidation propagates to every dependent canonical state—not merely to
the newest presentation layer.

### 6. Build a content-addressed artifact graph

The artifact store hashes payload bytes with SHA-256, stores blobs by digest,
binds artifacts to runs with typed roles, records lineage edges, indexes
checkpoints and evidence bundles, and refuses to rewrite an existing run
journal with different content. This is a strong implementation reference for
the ASI Stack artifact-graph chapter.

The book should retain the following distinctions:

- blob identity: what bytes exist;
- semantic role: why the run used those bytes;
- run binding: which execution produced or consumed them;
- lineage edge: what transformation connects artifacts;
- checkpoint entry: at which step and score a state was captured;
- evidence inclusion: which artifacts support which claim;
- promotion pointer: which exact artifact is eligible for which route.

The last item is under-specified in the snapshot: `promotion_labels` permits a
null artifact ID, and the only retained `candidate.current` label has one. A
run-level pointer is not enough when a run can contain multiple checkpoints,
reports, and later-invalidated evidence.

### 7. Evidence graphs should be transitive and revocable

The project materializes evidence graphs and deterministic research ledgers.
This is exactly the right direction. A public claim should be a node whose
support can be traversed to benchmark asset, rule, run, model artifact, source
snapshot, data snapshot, environment, and evaluator.

The retained external-benchmark episode supplies the crucial missing rule.
Twenty-nine runs were later quarantined with the reason “synthetic placeholder
benchmark fixture cannot support apples-to-apples comparison.” Three claims had
already recorded `Promote` decisions using five such runs each:

- HumanEval+-labelled coding evidence: 5 of 5 used runs quarantined;
- IFEval-labelled task evidence: 5 of 5 used runs quarantined;
- Terminal-Bench-core-labelled task evidence: 5 of 5 used runs quarantined.

The SQLite `candidate.current` label still points to the first Terminal-Bench
claim run, with no artifact ID. The report layer sees the quarantine, but the
claim evaluation and promotion label do not automatically revoke.

The book should specify transitive invalidation:

```text
source/fixture invalidated
  -> benchmark run invalid
  -> evidence bundle invalid
  -> uncertainty summary stale
  -> claim decision revoked
  -> promotion lease revoked
  -> default-route candidate quarantined
  -> dependent comparisons and reports rematerialized
```

Revocation must be a first-class transaction with reason, effective time,
affected-node closure, reviewer, replacement state, and replayable receipt.

### 8. A run ID is not an experimental seed

Claim evaluation requires a minimum number of distinct `EvidenceRun.seed`
values. When benchmark outcome metadata does not contain a parseable seed, the
CLI substitutes `stable_hash(run_id)`. Different run IDs therefore satisfy the
distinct-seed check even if the model, data order, evaluator, and computation
are identical.

This is observable in the retained corpus:

- all 173 `run_record.json` typed seed fields are null;
- all 173 typed code snapshots are null;
- 150 journals exist, but all 150 have null code digests and source-snapshot
  digests;
- only 23 unique numeric scores appear among 150 scored runs, with many
  repeated identical values;
- promotion decisions can nevertheless report five or six repeated seeds and
  extremely narrow or zero-width intervals.

The book should define experimental independence as a recorded intervention,
not metadata diversity. A valid repetition records the actual random seed,
data-order seed, sampler state, initialization state, nondeterminism policy,
source/config/model/evaluator digests, and a declared independence group. If
the system is deterministic, multiple identical replays establish
reproducibility, not sampling uncertainty.

### 9. Benchmark registry presence is not benchmark readiness

The project later introduces authenticity states such as external comparison
candidate, external missing provenance, and authentic ready. This repairs an
earlier tendency to place tiny starter fixtures behind industry benchmark
names.

At least the HumanEval+ and LongCoT lanes include stronger pinned upstream or
imported material. The retained LongCoT holdout bundle contains 1,995 rows, a
matching digest, and `seen_in_training=0`. By contrast, many other external
registry entries resolve to three-row scaffolds with one train, one internal,
and one holdout row, missing provenance, placeholder signatures, and even
training exposure.

The book should require an authenticity admission state machine:

- `name_only`;
- `schema_scaffold`;
- `fixture_smoke_only`;
- `external_missing_provenance`;
- `official_source_pinned`;
- `official_harness_verified`;
- `authentic_internal_eval_ready`;
- `authentic_public_comparison_ready`;
- `quarantined` or `retired`.

Only the last ready state appropriate to the claim may admit external
comparison. A registry entry is discoverability, not readiness.

### 10. Separate benchmark assets, rules, visibility, and claims

The project distinguishes benchmark asset versions, rule versions,
internal-evaluation mode, blind-holdout mode, public-claim mode, and claim
policy. This is a strong anti-Goodhart pattern because changes in cases,
scoring, visibility, or publication intent can be versioned independently.

The snapshot contains only one retained blind-holdout run versus 64 internal
evaluation, 58 public-claim, and 50 training records. The type exists, but the
corpus does not show broad blind-holdout practice. The book should therefore
separate interface presence from operational coverage and require hidden-case
custody, answer visibility, workspace policy, and evaluator separation to be
evidenced per run.

### 11. Dataset declarations are not sample-level decontamination

The registry strongly validates the presence of dataset taxonomy, provenance,
governance, declared benchmark exclusions, fail-closed flags, snapshot pins,
license posture, cleaning recipes, and decontamination recipes. These are
useful admission contracts.

But `overlap_scan_dataset` iterates a list of benchmark ID strings and checks
whether those strings—or declared aliases—are listed in the dataset's exclusion
or canary declarations. It does not compare training samples with benchmark or
holdout contents. Calling this an overlap scan risks turning declaration
coverage into empirical decontamination evidence.

The book should define two different receipts:

- declaration coverage: every protected benchmark and holdout has a declared
  policy and fail-closed route;
- empirical overlap analysis: sample or representation comparison, algorithm
  and threshold, corpus and benchmark digests, matches, review, removals,
  residual risk, and rerun identity.

Neither substitutes for the other.

### 12. Dataset pins must digest content, not labels

`pre_training_verify` emits `dataset_checksum` as a hexadecimal 64-bit
`stable_hash` of the dataset ID, prefixed with `sha256:`. The field is nonempty,
so `dataset_pin_verified` starts true, then remains true if registry declaration
checks pass. This is neither a SHA-256 content digest nor verification that the
registered pin matches local bytes.

The current 48,000-row `corben_frontier_multilane.v2.jsonl` does have a real
OpenSSL SHA-256 digest matching its registry and provenance record. That is a
positive artifact. The generic preflight field does not consume that digest.

The book should prohibit algorithm-name laundering in identity fields. A
content pin must include algorithm, full digest, byte length, canonicalization,
artifact location, and a verification receipt produced from the bytes actually
used by the run. A dataset-ID fingerprint should be called an ID fingerprint.

### 13. Reproducible corpus generation can still leak across splits

The retained frontier corpus has 48,000 unique JSONL rows: 43,200 training and
4,800 validation. Approximate lane counts are:

- 9,600 code repair;
- 9,600 math reasoning;
- 8,000 instruction SFT;
- 6,000 tool/API use;
- 5,600 proof verification;
- 5,600 semantic compiler;
- 3,600 paper synthesis.

The source mix includes 3,999 pinned OpenAssistant rows, 4,001 deterministic
project instruction rows, 36,400 deterministic local transforms, and 3,600
paper transforms. Its recorded SHA-256 digest matches the actual file, and it
is correctly marked internal-training-only rather than public-claim-ready.

However:

- validation is generally every tenth row from the same generators rather than
  a source-, family-, time-, or task-disjoint split;
- the materializer writes `protected_holdout_overlap=false`, empty benchmark
  IDs, and empty contamination tags without content-level comparison;
- marker-string filtering is not equivalent to benchmark decontamination;
- the quality gate records 1,260 suspicious instruction-SFT endings but does
  not fail on them;
- uniqueness and exact-answer-cap ratios do not establish semantic diversity;
- retained source paths include absolute `/Users/adimus/...` locations,
  weakening portability and disclosing a machine-specific lineage detail.

The book should distinguish reproducibility, syntactic diversity, semantic
diversity, split independence, provenance, and contamination evidence.

### 14. Async checkpoint completion needs an acknowledged result

The asynchronous checkpoint manager stages payload and metadata, emits progress
events, writes a content-addressed checkpoint, attaches it to the run, updates
the checkpoint ledger, and commits a completion marker via rename. This is a
useful pattern for separating training latency from persistence.

The worker loop discards the `Result` returned by
`process_checkpoint_request`, decrements the pending counter, and exposes
`wait_for_idle` as a Boolean on pending count. Errors that occur before the
inner blob-write match—opening the store, making directories, writing staging
files, or appending early progress—can therefore disappear without a failed
marker. “Idle” means no queued work, not that every request succeeded.

The checkpoint JSONL and progress JSONL writers also read the entire current
file and rewrite it on every append. They are not durable append transactions.

The book should require one terminal acknowledgement per request ID:

- committed artifact ID and digest;
- explicit failed state and error digest;
- timeout/unknown state that blocks campaign completion;
- reconciliation scan after restart;
- request-result channel or durable completion index;
- atomic or append-safe journal behavior;
- a campaign gate over acknowledged outcomes, not queue emptiness.

### 15. Hash chains need a threat model and an anchor

Campaign journals chain entries with a 64-bit stable hash. This detects some
accidental mutation and supports backup validation. It is not a cryptographic
audit chain, and journal compaction can retain only the newest half or third of
entries without an explicit anchor for the removed prefix.

The book should distinguish:

- corruption detection;
- tamper evidence;
- non-repudiation;
- external anchoring;
- complete history versus compacted state;
- replay sufficiency.

Compaction should emit a signed or content-addressed segment root, prior-root
reference, retained range, removal policy, and evidence-preservation decision.

### 16. Resource plans need observed receipts

The trainer includes resource profiles and accelerator planning across CUDA,
ROCm, MLX, and CPU, as well as checkpoint, queue, wall-clock, seed, and campaign
budgets. This is a strong resource-economics interface.

A plan's requested machine is not evidence of the machine used. The artifact
corpus includes historical fingerprints and plans from different moments. The
book should bind requested resource, resolved resource, observed hardware,
driver/runtime versions, fallback path, throttling, actual utilization, and
cost/energy receipts to the run. A silent CPU or lower-memory fallback changes
time-to-quality and can change scientific comparability.

### 17. Improvement search needs fixed budgets and evaluator independence

The project contains campaign DAGs, fixed-budget plans, repeated-seed policies,
sweeps, ASHA/PBT-like strategies, Pareto and complexity considerations, and an
advisor ladder. These are useful ingredients for open-ended improvement.

They do not by themselves solve evaluator capture. Advisors from the same model
family at different parameter sizes may share failure modes; the candidate,
trainer, evaluator, and promotion process can still be organizationally
correlated. The book should require conflict records, evaluator diversity,
candidate-blind scoring where appropriate, baseline preservation, complexity
penalties, and a promotion authority outside the candidate's writable state.

### 18. Central control planes need their own complexity budget

The large CLI, training, schema, and report modules show a natural risk: the
control plane can become a second monolith. Stable schemas help, but a 23,000-
line CLI and 17,000-line orchestration crate make policy, I/O, command
presentation, and compatibility hard to audit independently.

The book should apply the same governed-replacement discipline to the trainer:
module ownership, policy kernels separated from adapters and views, schema
evolution tests, contract fixtures, dependency-direction checks, and a
complexity budget for every new project integration.

## Evidence audit

### What the snapshot strongly supports

- The typed control-plane architecture exists in substantial Rust source.
- Manifests and registry validation cover a broad training/evaluation surface.
- Retained artifacts show campaigns, runs, checkpoints, evidence bundles,
  reports, failures, quarantines, claim evaluations, and lineage being written.
- Learning-evidence and holdout-watchdog checks fail closed in retained session
  histories.
- Content-addressed SHA-256 blobs and a relationship index exist.
- Report materialization excludes active quarantines from aggregate industry
  candidate selection.
- At least one large local corpus has a reproducible content digest matching its
  registry/provenance record.
- LongCoT retained material is materially stronger than the three-row external
  starter fixtures.

### What is source-reported or not reproduced

- Workspace test results, because the offline build lacked the cached `time`
  dependency before compilation.
- Real external adapter execution against all referenced projects.
- Authentic public benchmark performance.
- Long-duration training stability or resource efficiency.
- End-to-end restart recovery under crash or disk fault.
- Cross-platform CUDA/ROCm/MLX behavior.
- Independent evaluator or reviewer operation.

### Contradictions and integrity gaps

- Quarantined evidence still has stale `Promote` claim files and a stale
  `candidate.current` database pointer.
- Repetition identity can be synthesized from run IDs.
- Typed seed and code snapshot identity are missing from every retained run
  record inspected.
- Journal seed values are sometimes derived rather than experimental facts.
- Dataset preflight mislabels an ID hash as a SHA-256 checksum.
- Declaration coverage is presented as an overlap scan.
- External benchmark names were attached to placeholder fixtures before later
  authenticity repair.
- Async checkpoint queue completion does not prove success.
- Rich SQLite relations are application-enforced rather than protected by
  declared foreign keys.

## Cross-project lineage

Corben's Trainer is a control-plane convergence point for several older
projects:

- CCA appears as a vectorized RL environment adapter and health-audited
  compatibility target;
- MoECOT supplies an evidence-run adapter and informs manifest-first
  orchestration;
- Corben's Best Model Possible supplies the real training/inference kernel
  targeted by the Corben backend scripts and current plans;
- broader Corben project sources are transformed into training data and
  benchmark contracts.

The book should distinguish inherited terminology, adapter support, and
independent implementation. A type named for a project is not evidence that the
whole upstream architecture was integrated or evaluated.

## Book crosswalk

### Existing chapters to strengthen

`evidence-states-and-claim-discipline`

- experimental independence versus run-ID diversity;
- support invalidation and revocation;
- learning-truth evidence versus stage completion;
- missing source/config/code identities as promotion blockers.

`artifact-graphs-audit-logs-and-replay`

- content-addressed blobs, run-role bindings, lineage, immutable journals,
  evidence graphs, research ledgers, checkpoint acknowledgements, recovery,
  compaction anchors, and result-derived views.

`benchmark-ratchets-and-anti-goodhart-evidence`

- benchmark asset/rule/mode/claim separation;
- authenticity state machine;
- public, internal, and blind modes;
- placeholder quarantine;
- transitive revocation;
- holdout watchdogs and uncertainty discipline.

`ai-supply-chain-integrity-and-lifecycle-provenance`

- dataset, source, model, executor, evaluator, and artifact pins;
- distinction between identifier fingerprints and content digests;
- declaration coverage versus content-level decontamination;
- provenance portability and artifact-role completeness.

`recursive-self-improvement-boundaries`

- trainer as promotion institution;
- candidate/evaluator/promotion separation;
- fixed budgets, canary state, rollback, quarantine, and complexity acceptance;
- no candidate promotion from candidate-authored evidence alone.

`open-ended-improvement-engines`

- campaign DAGs, sweep strategies, Pareto selection, advisor ladders, and
  bounded continuation;
- failure retention and search residuals.

`system-boundaries-and-authority`

- trainer ownership versus external backend ownership;
- adapter contracts, authority ceilings, and project sovereignty.

`resource-economics-and-token-budgets`

- requested versus resolved versus observed resources;
- accelerator fallback receipts, queue budgets, and time-to-quality.

`artifact-steward-agents-and-living-project-governance`

- source-of-truth views, stale state, migration, revocation, and central
  control-plane complexity budgets.

### Proposed boundary decision

No new chapter is proposed from this project alone. “Epistemic control plane”
is a useful unifying concept, but its mechanisms already belong across evidence
states, artifact graphs, benchmark ratchets, supply-chain provenance,
self-improvement, resource economics, and project governance. A dedicated
training-control-plane chapter should only be reconsidered after mining
Corben's Best Model Possible and deduplicating against the complete chapter
spine.

## Minimum viable implementation for the mined idea

A book-grade minimum trainer control plane would:

1. compile a typed dataset, executor, training plan, benchmark asset, scoring
   rule, and claim policy into canonical JSON;
2. hash the actual source, config, data, model, environment, and evaluator bytes
   or immutable references used;
3. run one bounded training update and independently verify optimizer steps,
   loss movement, and checkpoint delta;
4. persist the checkpoint content-addressably with an acknowledged terminal
   result;
5. evaluate it in an authenticated internal benchmark and a separately
   custodied holdout;
6. materialize an evidence graph and claim decision;
7. quarantine one upstream artifact and prove transitive claim and promotion
   revocation;
8. resume after a forced interruption without losing or silently duplicating a
   stage;
9. render all operator views from the same canonical facts;
10. emit explicit non-claims for every untested external or deployment surface.

## Beyond the state of the art

The mature endpoint is a proof-carrying improvement institution. Every training
proposal is a typed transaction. Its source, data, compute, evaluator,
authority, budget, model, and expected evidence are frozen before execution.
Every mutation produces content-addressed lineage and learning-effect receipts.
Every evaluation is authenticity-qualified, visibility-scoped, contamination-
aware, and evaluator-separated. Every promotion is a revocable lease over one
exact artifact and route, with an automatically computed invalidation closure.
Every failure becomes a reusable residual. The system can change adapters,
models, data, and search strategies without changing the semantic contract by
which an improvement is admitted.

This endpoint is architectural. Corben's Trainer does not demonstrate it end to
end.

## Residual work

- Mine Corben's Best Model Possible and trace which trainer contracts are
  actually satisfied by the current backend.
- Complete symbol and artifact provenance across CCA, MoECOT, BeastBrain,
  BugBrain, Trainer, and Best Model.
- Add independent literature for experiment tracking, dataset contamination,
  benchmark governance, statistical repetition, crash consistency, and model
  promotion/revocation.
- Reproduce the Rust workspace tests after dependencies are restored without
  writing build products into the project tree.
- Design a mutation test for transitive quarantine and promotion revocation.
- Test actual content-digest verification in preflight and distinguish it from
  registry declaration validation.
- Test checkpoint worker failures before staging, during append, and after blob
  insertion.
- Inspect whether newly unzipped projects repair or reproduce these gaps.

## Non-claims

This mining pass does not claim that:

- the trainer produced a better model;
- retained external benchmark scores are authentic or comparable;
- five run IDs are five independent random seeds;
- the 48,000-row corpus is decontaminated or semantically diverse;
- every dataset, source, code, evaluator, or environment snapshot is pinned;
- checkpoint persistence is crash-safe under all failure points;
- the artifact graph is tamper-proof;
- the Rust workspace currently passes;
- the trainer is production-ready, safe, independently governed, AGI, or ASI;
- any chapter-core support state should be promoted from this local project.
