# Corben's Best Model Possible Project Mining Dossier

Date: 2026-07-10

Project: local historical project `Corben's Best Model Possible` (private source checkout; path intentionally omitted)

Pinned revision: `c61288685ca05ba773402d4a7495cfbba22c2c20`

## Executive conclusion

Corben's Best Model Possible is most valuable to the ASI Stack as a densely
instrumented mechanism laboratory. It combines a recurrent shared-weight model
shell, deterministic feature construction, small trainable readout adapters,
lane-specific checkpoint banks, a semantic compiler, typed memory, a probe
router, belief governance, verification tribunals, bounded tool adapters,
speech hooks, and a large architecture-search corpus. The project repeatedly
tries to make architecture changes auditable through fixed slices, equal-step
comparisons, champion/challenger state, promotion gates, checkpoint lineage,
and retained negative results.

The repository also supplies an unusually important counterexample to
architecture-shaped overclaim. The strongest current training path does not
train the inner recurrent trunk. It trains either a low-rank byte-sequence
readout or a pooled-hidden adapter over deterministic features. The normal
runtime's returned text is produced by a local math/specialist path rather than
decoded from model logits. Several sophisticated subsystems exist as source
modules but are either driven by default fixtures, reduced to manifest
booleans, or not connected to the ordinary request path. Many evaluation
fields are declared, modeled, constant, shape-derived, or vacuously true rather
than directly measured. The native speech path is a deterministic tone/symbol
codec and acoustic-unit generator, not general speech recognition or natural
voice synthesis.

That combination makes the project exceptionally useful for the book. It
contains both reusable design patterns and concrete examples of why the stack
needs an evidence taxonomy that distinguishes:

- interface presence from runtime effect;
- component ownership from useful capability;
- deterministic execution from semantic correctness;
- explicit/oracle lane selection from autonomous routing;
- adapter learning from trunk learning;
- replayed records from live re-execution;
- declared metadata from observed receipts;
- fixed-feature architecture probes from general model capability;
- isolation by unchanged components from evidence against shared interference;
- source-reported green tests from currently reproduced tests.

The strongest ideas to carry forward are:

1. shared-weight recurrent routes with explicit shell/core topology;
2. same-initialization, equal-step, single-axis architecture promotion;
3. per-lane specialist adapters with fixed-slice interference matrices;
4. best-checkpoint authority and explicit best-versus-final drift;
5. fixed-step quality authority for adaptive-halting research;
6. typed memory edges, justification-bearing durable claims, tiering, and
   replay-pinned retrieval;
7. request-feature provenance, stateful routing budgets, and outcome-calibrated
   routing;
8. task contracts that preserve acceptance tests, non-goals, risk, budgets,
   verification, and failure behavior across compilation;
9. evidence-method labels and an independence graph for verification;
10. metric provenance as a first-class algebra rather than an after-the-fact
    disclaimer;
11. relocation-safe artifact identities and checkpoint banks;
12. negative-result retention, family retirement, and configuration-frontier
    discipline.

The project does not establish a trained foundation model, general text
generation, autonomous lane inference, general speech, semantic compilation
correctness, durable long-term memory, complete sandbox enforcement,
independent verification, measured efficiency, external benchmark
performance, AGI, or ASI.

## Snapshot identity and source boundary

The repository is on branch `main` at commit
`c61288685ca05ba773402d4a7495cfbba22c2c20`, dated 2026-05-12 with subject
`Back up current Corben model state`. It contains one reachable commit and an
origin naming `corbensorenson/corbens-best-model-possible` on GitHub.

The worktree is not clean. It contains 8,286 deleted tracked paths, all under
`artifacts/`, resulting from the earlier rebuildable/cache cleanup pass. No
source, configuration, research, or operations path appears in the current
status. The source analysis is therefore pinned to the commit and current
source tree, but artifact counts describe the surviving local artifact corpus,
not the complete artifact corpus recorded by the pinned commit. Historical
artifact conclusions are limited to retained files that were actually
inspected.

The current checkout is about 8.5 GiB: approximately 8.3 GiB is under
`artifacts/`, about 200 MiB is `.git`, and the source, configuration, research,
and operations material is comparatively small. The repository has 10,561
tracked files. Git storage is dominated by roughly 197 MiB of loose objects,
with no packed object set observed during the inventory pass.

Private source material remains outside the public book repository. This
dossier records public-safe architecture, implementation behavior, retained
result summaries, contradictions, and chapter routes. It does not copy model
states, optimizer states, private corpus rows, credentials, raw benchmark
cases, or the full artifact tree into the book.

## Structural inventory

### Workspace

The Rust 2024 workspace has 20 library/application crates plus `xtask`. The
crates cover contracts, model, speech, kernels, tokenizer, training, quantized
reporting, memory, router, compiler, governance, macro store, policy, math,
verification, tools, runtime, audio, evaluation, and the CLI. The current
source tree contains 27 Rust files totaling about 45,704 lines and 238 direct
`#[test]` attributes. It also contains Python experiment/analysis helpers,
TOML configuration families, JSON result and contract records, shell/ops
material, and research notes.

The workspace forbids unsafe Rust and denies several high-risk lint classes,
including `todo`, `unwrap`, `expect`, and `dbg`. These settings are useful
source-quality controls, but a lint policy is not evidence that the current
snapshot builds or that runtime claims are true.

The largest Rust surfaces are the model, training bridge, evaluation library,
model-training support, runtime, and memory library. This distribution reflects
the project's actual emphasis: training/evaluation orchestration and evidence
surfaces are at least as prominent as the core forward model.

### Current artifact corpus

The surviving `artifacts/` tree contains 129,516 files. Filename-level counts
include:

- 3,685 model-state JSON files;
- 3,685 optimizer-state JSON files;
- 7,035 learning-metric, training-truth, or checkpoint-delta files;
- 226 comparison reports;
- 338 validation or checkpoint-validation reports.

These counts show substantial experiment archaeology and checkpoint
retention. They do not establish independence, authenticity, correctness, or
current loadability. The pinned commit contained more artifact paths than the
working tree now retains.

### Configuration frontier

The base configuration names a compact prime-cycle stage-hybrid model with:

- hidden width 704;
- 11 attention heads and one KV head;
- five unique blocks and 16 effective layers;
- adapter rank 12;
- context setting 8,192;
- default route `[0, 1, 2, 5, 6, 7, 3, 4, 5, 2, 1, 0]`;
- a preserved shell and recurrent core beginning at block two;
- shared role and pass controls, with core-only depth-adapter tying;
- grouped-query attention, local mixing, support-vector dimensions, and
  optional reserve experiments;
- native speech hooks and declared local-path promotion comparisons;
- recurrence research settings for dynamic iteration counts, adaptive
  halting, overthinking probes, and shortcut-resistant evaluation.

The project maintains control/experimental configurations, stage-specific
overlays, architecture probes, and a frontier of promoted, rejected, reserve,
or retired configurations. This is a strong organization pattern even where
the underlying capability evidence is limited.

## Implementation reality map

| Surface | Implemented reality | Evidence boundary |
|---|---|---|
| recurrent model | deterministic shared-weight feature transformer with route-dependent fixed blocks and tied output geometry | no trained inner trunk or foundation-model weights established |
| attention | hidden vectors act directly as queries, keys, and values with no learned Q/K/V projection matrices in the inspected path | attention-shaped computation, not a conventional trained transformer |
| tokenizer | byte tokens, hard-coded bigrams, and hash-bucket wordpieces | hashed wordpieces are lossy and collision-untracked |
| training | low-rank byte-sequence readout or pooled-hidden adapter update | not full-trunk training; pooled adapter cannot express general varying sequences |
| generation | forward logits and artifact summaries; runtime math/specialist response | no general autoregressive model-text generation path established |
| lane bank | seven explicitly addressed low-rank specialist adapters | lane metadata is externally supplied; no automatic prompt-lane inference |
| compiler | typed task spell, atoms, linear plan graph, semantic/target IR, repair-scope calculation | ordinary solve path uses only compiler manifest booleans; parity method is not semantic equivalence |
| memory | typed in-process lattice, retrieval, tiers, lineage, JSONL persistence | several state transitions are trace-only or non-durable across restart |
| router | deterministic score policy over supplied probe features | normal solve uses default features and recreates its budget |
| governance | belief states, contradictions, reviews, commitment transitions | contradiction severity response is non-monotone; runtime authority is incomplete |
| verification | tribunal-shaped rows and proof fail-closed behavior | several rows are string/shape predicates, dependent checks, or vacuous passes |
| tools | file probes and arbitrary executable invocation adapter | declared capability envelope is not fully enforced; recorded replay is not live replay |
| speech | streaming acoustic-unit labels and benchmark tone-symbol round trip | not ordinary STT/TTS; latency is configured/derived rather than observed device latency |
| evaluation | large metadata and regression surface | many metrics are constants, declarations, prompt-length formulas, or proxy predicates |

## Model architecture mined for the book

### 1. Shared-weight recurrence should be specified as topology, not rhetoric

The model's clearest architectural contribution is a route whose effective
depth exceeds the count of unique blocks. A shell can preserve input/output
specialization while a smaller recurrent core is reused in a prime-cycle
schedule. The book can use this to explain a low-parameter depth axis:

`unique state + route schedule + recurrent controls + halting policy -> effective computation`

This is a useful alternative to treating parameter count as the only capacity
axis. The state that must be pinned includes the unique block definitions,
route sequence, control placement, parameter tying, recurrence count,
initialization, train/inference iteration distribution, and stopping rule.

The project correctly treats route shape as an experimental variable and keeps
reserve families outside the mainline until they beat a control. The book
should preserve that discipline while avoiding the phrase “effective layers”
as if recurrence automatically created the capability of separately trained
layers.

### 2. Fixed feature generators and trainable models need different names

In the inspected `HrcModel`, token embeddings are generated deterministically
from token ID and position. Depth adapters, MLP-bank components, value/support
vectors, and controls are initialized from fixed seeds. Attention operates
directly on hidden vectors. The tied output compares pooled hidden state with
deterministically generated token embeddings. Quantization is a fixed rounding
operation to a 1/1024 grid.

The reported model-parameter estimate counts arrays in these fixed low-rank
blocks. It does not include a learned embedding table or learned Q/K/V
projections, and it should not be interpreted as the parameter count of a
trained language model. This yields a general book rule:

> Every parameter count must be paired with an ownership state: generated,
> frozen, pretrained, trainable, updated in this run, or selected by search.

A deterministic feature generator can still be scientifically useful. It can
support controlled comparisons of route topology and adapter behavior. Its
results belong in a “mechanism-development” evidence state, not a general
model-capability state.

### 3. Tokenizer identity includes reversibility and target encoding

The hybrid tokenizer combines four special IDs, 256 byte IDs, 96 hard-coded
bigrams, and hash-bucket wordpieces. Five-to-ten-character alphabetic words can
be mapped into hash buckets. Decoding cannot reconstruct those words and emits
`<wp>` for a hashed bucket; collision provenance is not retained.

The training target path is different: target strings are treated as ASCII
bytes and mapped into the 256-output vocabulary. This means input tokenization,
target encoding, output vocabulary, and decode semantics are distinct
interfaces. The book should require tokenizer evidence to record:

- input encoding and target encoding separately;
- reversible versus lossy token classes;
- collision behavior and collision observability;
- special-token and byte ranges;
- output-vocabulary coverage;
- the exact mapping used by evaluation.

“Tokenizer vocabulary size” alone is not enough to define the learned task.

## Training and adapter evidence

### 4. Adapter learning must not be reported as trunk learning

The training bridge explicitly describes the recurrent trunk as frozen. The
implemented trainable paths are a low-rank readout and an MLX pooled-hidden
adapter. The trainable-trunk-ready backend list is empty; trainer requests that
require a trainable trunk fail closed.

The low-rank readout has approximately 93,496 trainable scalar values at the
base dimensions. Its largest single table is a 256-by-256 position-specific
byte bias. Other learned arrays include a 12-by-704 down projection, a
256-by-12 up projection, vocabulary bias, position embeddings, auxiliary
features, previous-byte embeddings, and a base-logit projection.

This decomposition matters because the observed learning can come primarily
from a position-conditioned byte table rather than changes to the recurrent
architecture. The book should require a trainable-state manifest that reports:

- every trainable tensor and its shape;
- its fraction of updated state;
- whether it sees target position or teacher-conditioned history;
- the frozen upstream representation;
- the inference-time recurrence or decode loop;
- ablations for high-capacity shortcut tables.

### 5. Sequence metrics require a sequence-capable inference mechanism

The low-rank readout validation path is autoregressive over its own previously
predicted byte. Training blends teacher-conditioned and self-conditioned
previous tokens. That is a legitimate small sequence learner, albeit one over
a fixed pooled prompt representation and position features.

The pooled-hidden adapter path is materially different: it computes a single
output distribution and reuses the same predicted token at every target
position. It cannot represent an arbitrary multi-byte answer. Exact-sequence
accuracy on that path is meaningful only for constant-token targets. The book
should add a metric admissibility test: an evaluation metric is invalid when
the evaluated architecture cannot represent the target class.

### 6. Returned text must be causally linked to trained logits

`HrcModel::run_forward` emits logits and artifact summaries. The normal runtime
then obtains response text from a local math or external specialist artifact.
The “plain generation” CLI still enters this solve route. A general
autoregressive text-decoding loop causally driven by the trained checkpoint was
not found.

The book should require a response-causality receipt:

1. checkpoint identity;
2. prompt tokens;
3. forward-call identity;
4. sampling/decoding decisions;
5. emitted token IDs;
6. decoded response;
7. tool or specialist substitutions;
8. claim source for every answer segment.

Without this chain, training loss and runtime answer quality can coexist in the
same repository without being causally related.

## Lane specialists and architecture search

### 7. A specialist bank is an artifact graph, not yet a router

The retained promoted bank binds explicit adapters for code repair,
instruction SFT, math reasoning, paper synthesis, proof verification, semantic
compilation, and tool/API use. Its own truth note correctly says it records
lane-routed low-rank readouts and does not claim trained-trunk routing or
automatic prompt-lane inference.

This distinction should become a book evidence ladder:

1. separate specialist checkpoints exist;
2. labeled/oracle lane binding selects the intended checkpoint;
3. an independent router predicts lanes on held-out requests;
4. routing improves end-to-end utility against fixed-compute baselines;
5. fallback and abstention are calibrated;
6. shared-trunk interference and router-induced distribution shift are tested;
7. runtime receipts prove which specialist actually ran.

The project establishes the first two levels for retained paths, not the later
levels.

### 8. Interference matrices need counterfactual interpretation

Bank scans evaluate fixed validation offsets across lanes and reject candidates
that regress protected slices. This is a strong mechanism for localizing an
adapter change. The final paper-specialist scan improves the paper lane while
other lane deltas are exactly zero because their adapters are unchanged. “Zero
regressions” therefore demonstrates artifact isolation, not an absence of
shared-trunk interference or a generally safe autonomous routing policy.

The book should distinguish:

- unchanged-component invariance;
- within-specialist generalization;
- cross-specialist interference;
- shared-state interference;
- router-selection error;
- fallback behavior;
- end-to-end user utility.

### 9. Checkpoint composition is useful when its semantics are explicit

The default adapter uses a linear delta blend:

`composed = base + alpha * (candidate - base)`

with alpha 0.25 and optimizer moments reset while counters are preserved. This
is a useful, reproducible composition primitive. The book should record
composition as a transformation edge with base identity, candidate identity,
coefficient, state subset, optimizer-state policy, dtype, and verification
slices. It should not describe a composed adapter as “merged intelligence” or
infer routing from its existence.

### 10. Artifact identity must survive relocation

The retained promoted bank stores absolute paths rooted under another user's
home directory. Equivalent relative files appear in the current checkout, but
the inspected loader treats an absolute path as authoritative and does not
fall back to a repository-relative equivalent. The bank therefore is not
directly loadable from the present checkout without rewriting or recreating
its manifest.

The book should require artifact references to combine content identity with
relocatable resolution:

- cryptographic digest and schema;
- repository-relative or content-store URI;
- optional original location as provenance only;
- resolver version;
- relocation test;
- missing-artifact and digest-mismatch behavior.

### 11. Architecture search should preserve negative knowledge

The project uses frozen controls, mutable challengers, equal-step comparisons,
single-axis experiments, stage-specific overlays, reserve families, and
promotion/reset behavior. Retained reports record both promotions and rejected
families. Research notes explicitly discourage brute-force Cartesian search,
multi-lever first passes, duration-only promotion, and merging ideas before
they win alone.

This is a strong template for an improvement engine. The book should add a
configuration-frontier ledger with:

- active champion;
- challenger mutation and parent;
- single-axis claim;
- matched initialization, data, steps, and hardware class;
- protected metrics and promotion thresholds;
- best and final checkpoint identities;
- rejection reason;
- retirement scope;
- admissible recombination rules;
- unresolved residuals.

The evidence level remains bounded: these comparisons operate on a fixed
feature generator and small adapters. They can reveal mechanism-level
interference without proving general model superiority.

### 12. Adaptive recurrence needs fixed-step quality authority

The recurrence research configuration includes a dynamic Poisson iteration
schedule, extrapolation iterations, train/inference mismatch checks, KL and
entropy stopping signals, patience, fixed-step and latency-matched references,
and first-hit/last-correct overthinking telemetry. This is exactly the right
shape for studying adaptive compute.

The especially useful rule is that fixed-step quality, not the halting head's
own score, has promotion authority. The book should preserve this as a
counterfactual: a halting policy earns promotion only when it retains quality
relative to an equal-or-greater fixed-step reference while delivering a
measured resource benefit. Overthinking should be measured by first-correct,
last-correct, and margin-collapse trajectories, not only final accuracy.

## Runtime, compiler, and planning

### 13. Runtime integration must be traced from request to effect

The ordinary solve path calls the router with fixed default probe features,
uses a newly created empty memory bundle, reduces compiler integration to three
manifest emission booleans, and summarizes a scaffold macro store. It then
routes the response through a math/specialist path. The substantial router,
memory, compiler, and macro-store modules therefore do not all exert their
advertised effects on the ordinary request.

The separate outer-system path does construct a TaskIR plan and retrieval
contract. Its memory context is created per request and seeded from the current
input or fallback features; it is not demonstrated as durable long-term
project memory. Its coding/task tool probes inspect predetermined repository
files rather than carrying out the requested coding task. These are useful
integration scaffolds, not end-to-end task-success evidence.

The book should introduce an effect map for every subsystem:

`request field -> derived feature -> policy decision -> selected state -> executed effect -> receipt -> evaluator`

A component should not be called “integrated” merely because its type appears
in a runtime report.

### 14. Compile task contracts, but prove preservation semantically

The semantic compiler builds a `TaskSpell` containing role, objective,
modality, context, constraints, acceptance tests, non-goals, resource budget,
risk flags, procedure, output contract, verification plan, failure behavior,
and an immutable contract hash. It then performs extract, normalize, type,
dependency, lint, dedupe, semantic-IR, and target-IR passes. It can emit a
TaskIR sequence with goal, retrieval, plan, optional tool, verification, and
response nodes. Localized repair calculates changed, touched, unchanged, and
whole-rebuild scope.

These interfaces belong in the ASI Stack's compiler chapter. However, the
implementation is mostly deterministic string parsing and keyword routing.
Context directives are recognized by prefixes such as `constraint:`,
`acceptance:`, and `verify:`. Plan nodes form a linear dependency chain.
Lane assignment is driven by keywords. Localized repair compares node IDs and
neighbor edges; node IDs are positional, so insertions can enlarge apparent
change.

Most importantly, “cross-stage digest parity” computes independent 64-bit FNV
digests and applies token-set Jaccard to the full hexadecimal strings. Each
digest is effectively one token, so the check is equality of digest strings,
not semantic preservation. The book should require executable contract tests,
typed field lineage, semantic equivalence or refinement proofs, and
counterexample generation—not hash resemblance—as the preservation evidence.

## Memory, routing, and governance

### 15. Durable claims should carry justifications and legal typed edges

The memory lattice has typed nodes and edges, provenance, confidence,
commitment, replay windows, goal-aware retrieval, information-gain terms,
hot/warm/cold tiers, context freeze/thaw decisions, reserve writes, and an
ephemeral-audio path. Requiring justification before a claim becomes durable
and constraining legal edge types are strong patterns.

The book should preserve four separate memory layers:

1. content and provenance;
2. semantic relationships and contradiction state;
3. retrieval/index state;
4. durability and transaction state.

Confidence and retrieval relevance must not substitute for durable commit or
epistemic review.

### 16. Memory transitions must change state transactionally

Several retained implementation details expose the gap between a named
transition and a real one:

- node/content identities use a 64-bit FNV hash rather than a cryptographic
  content digest;
- node identity omits some policy-bearing fields, allowing distinct payloads
  to collide at the semantic identity level;
- freeze records a decision and lineage but does not persist a content
  snapshot or materially freeze a cluster;
- thaw emits trace and lineage but does not attach or materialize the data;
- default freeze/thaw thresholds are permissive enough to pass trivially;
- tier rebalance and session compaction mutate in-memory nodes without
  persisting those node updates, so restart can lose the tier transition;
- goal drift compares character sets of hash strings rather than semantic
  goals;
- reserve promotion records acceptance but does not install a canonical node;
- JSONL append and index rewrite do not form a fully atomic, fsynced
  transaction.

The book should demand a transition postcondition: after freeze, thaw,
promotion, compaction, or rebalance, an independent restart-and-read check must
observe the intended state. A receipt without a materialized effect is a trace,
not a transition.

### 17. Routing needs request-derived features, persistent budgets, and outcomes

The router's score combines stakes, evidence gap, reversibility, uncertainty,
latency, and burst budget. It emits typed selected/fallback routes, reasons,
margins, expected gain, and guards. This is a useful policy shape.

Normal runtime use undercuts it: the solve path passes fixed default features,
and the default decision creates a fresh budget each time. The calibration
method fits thresholds to score quantiles but ignores supplied solved,
verified, latency, and target-band fields. That is distribution fitting, not
outcome calibration.

The book should require each routing decision to carry:

- feature values and their request-derived provenance;
- policy and threshold version;
- persistent budget-owner identity;
- selected and fallback lane;
- abstention/stop reason;
- predicted gain and cost;
- observed outcome, verification, latency, and resource use;
- delayed calibration update;
- replay identity.

### 18. Belief-governance responses should be monotone in evidence severity

The governance module models beliefs, justifications, entrenchment,
contradictions, reviews, commitment transitions, quarantine, rollback, and
anti-expert telemetry. The typed distinction between belief state and
commitment state is valuable.

The contradiction policy is non-monotone: very strong contradictions trigger
rollback and quarantine; medium contradictions downgrade; weak contradictions
can quarantine. A weaker signal can therefore produce a more restrictive state
than a medium signal. This should become a general governance invariant:
increasing evidence severity must not reduce the minimum required containment
response unless another explicit variable explains the change.

The review gate is also mostly declarative. Stable status requires a literal
counterexample-search string plus sources and patch bundle; candidate status
needs nonempty artifact IDs. The book should specify semantic review evidence,
reviewer/evaluator identity, challenge coverage, and the authority actually
granted by each state.

## Verification, tools, and replay

### 19. Verification needs method labels and independence structure

The tribunal exposes structural validity, exactness, semantic equivalence,
residuals, challenge sets, proof fail-closed behavior, replay, capability, and
translation equivalence. Claim-bearing math correctly rejects a local
placeholder and requires a released external TrackR/Omega specialist. That is
a useful fail-closed boundary.

Other rows are much weaker:

- semantic equivalence can reduce to nonempty content;
- challenge-set success can be absence of failure strings;
- translation equivalence can be absence of a `bounded_approx` marker;
- system consistency can be presence of an equals sign;
- fast/reference checks can derive from the same status or artifact;
- empty effect logs and replay sets can pass vacuously;
- an artifact verifier can return a success-shaped record without independent
  semantic checking.

The book should give each verification result a method class:

- syntax/shape;
- deterministic recomputation;
- executable property test;
- metamorphic test;
- differential implementation;
- independent solver/prover;
- empirical measurement;
- human review;
- declaration only;
- vacuous/no-applicable-cases.

It should also record an independence graph: shared source, shared artifact,
shared algorithm, shared model, shared data, and shared operator. Two checks
are not independent because they have different names.

### 20. Capability envelopes must be enforced at the adapter boundary

The tool layer offers bounded file reads/stat/list and a generic code execution
tool. The generic adapter can execute an arbitrary program and argument list.
Its capability envelope declares network, write, code-execution, randomness,
and clock permissions, but the inspected enforcement primarily checks network
strings and claim-bearing file readability. It does not comprehensively enforce
the declared file-write, code-execution, randomness, or clock policy.

The normal runtime only uses predetermined safe probes, which narrows the
currently exercised path. The reusable adapter itself still needs operating
system enforcement, path scopes, executable allowlists, environment filtering,
resource limits, and explicit side-effect receipts.

For tools that do not support live replay, a retained payload can be returned
after input-hash comparison. The original first execution is marked
deterministic-equivalent without a second run. This is record playback, not
live replay. The book should distinguish:

- playback;
- deterministic re-execution;
- re-execution with output comparison;
- semantic replay under changed environment;
- side-effect reconciliation.

## Evaluation and metric provenance

### 21. Every metric needs an origin type

The evaluation layer is rich in metadata but often derives apparent metrics
without observing the named quantity. Examples include:

- token counts and latency derived from prompt length;
- a scoring signal initialized at 0.45 and adjusted by fixed bonuses;
- `verified_per_param` set to a constant rather than computed from parameter
  count;
- session-to-session compounding set to fixed values by evaluation mode;
- public authenticity decided by exact metadata strings;
- replay determinism accepted from declared booleans or an empty replay set;
- retrieval, compiler-repair, and maintenance regressions inferred from
  unrelated presence predicates.

The most dangerous default is simulation disclosure: missing metadata can be
classified as real execution or hardware-observed rather than unknown. The
absence of a simulation marker is not evidence of hardware measurement.

The book should add a metric provenance algebra. Every numeric or boolean
metric must be one of:

1. directly measured;
2. derived from measured values;
3. independently recomputed;
4. modeled or simulated;
5. fixture-generated;
6. constant policy prior;
7. declared by producer;
8. inferred from a proxy;
9. vacuously true;
10. unknown/missing.

Promotion policies should state which origin classes are admissible for each
claim. Missing provenance should fail to unknown, not upgrade to real.

### 22. Metadata contracts are not observational receipts

Public-claim surfaces require strings such as `real_tools`, `real_memory`,
`real_tribunal`, `declared_hardware`, and trainer-enforced states. These can be
useful schema fields, but their presence does not prove the binding. The
Trainer repository's later quarantine of placeholder benchmark evidence is a
positive sign that the governance layer evolved beyond this earlier trust
boundary.

The book should require requested, resolved, executed, and observed identities
for backends, tools, memory stores, evaluators, datasets, and hardware. A
producer's declaration belongs in the evidence graph, but it cannot serve as
its own independent verifier.

## Speech and modality ownership

### 23. Native ownership is orthogonal to semantic capability

The speech engine computes RMS, zero-crossing rate, and signal motion. Ordinary
audio is mapped by a hash of these features and revision number to a table of
acoustic-unit labels. A benchmark-specific codec synthesizes distinct tones
for supported characters and decodes them by frequency matching, allowing the
test utterance to round-trip symbolically. The synthesis path maps each text
byte to a short sinusoidal tone. Reported first-audio latency is a style-based
constant, not observed device latency.

The ownership report labels the streaming transcriber, alignment/stability
heads, render planner, and decoder/vocoder as first-party and declares no
hosted or third-party inference. That ownership statement can be true while
the system lacks ordinary intelligible speech recognition and natural speech
synthesis.

The book should therefore separate:

- code ownership;
- local execution;
- signal processing;
- symbolic benchmark round-trip;
- acoustic intelligibility;
- linguistic transcription quality;
- speaker/environment robustness;
- naturalness and human usability;
- observed streaming latency.

Self-consistent synthetic capture and decode is a codec test, not a general
speech benchmark.

## Evidence audit

### Source-implemented evidence

The source establishes that the repository contains:

- a deterministic recurrent feature path and typed configuration frontier;
- adapter-state update code and checkpoint serialization;
- explicit trainer/backend contract checks;
- lane-bank and composition schemas;
- typed compiler, memory, routing, governance, verification, tool, audio, and
  evaluation modules;
- fixed-slice and same-budget comparison machinery;
- fail-closed states for several unsupported serious-path requests;
- substantial unit-test-shaped source coverage;
- large retained result and checkpoint corpora.

### Retained artifact evidence

The retained bank and scan artifacts establish that lane-specific adapter
states, fixed validation slices, composition metadata, and promotion-shaped
reports were produced. A final paper-specialist scan reports paper-lane mean
loss improving from approximately 3.4643 to 3.1016 and overall bank mean loss
from approximately 3.3814 to 3.3295 on two fixed offsets per lane. Other lane
deltas are zero because those adapters are unchanged. These values are local
adapter-validation observations, not external capability scores.

Many research notes report green workspace tests, Clippy, release reports,
kernel parity checks, and earlier adapter validation results at the time of
development. They are source-reported historical state, not a reproduced
current build.

### Current reproducibility state

A current offline workspace test attempt used the available Rust 1.90 toolchain
and routed build output to `/private/tmp`. Resolution stopped before compilation
because `schemars` was absent from the offline Cargo cache through the `xtask`
dependency graph. A source-only temporary copy excluding `xtask` progressed to
another missing cached dependency, `toml_edit`, and likewise stopped before
compilation. The repository requests Rust 1.94, but the local toolchain could
not be synchronized in the restricted environment.

No current pass count is claimed. No external dependencies were downloaded,
no training was rerun, no model checkpoint was changed, and no external
benchmark was executed.

## Book insertions

### Existing chapter routes

| Project finding | Primary ASI Stack route | Intended use |
|---|---|---|
| shared-weight prime-cycle recurrence | `routing-heads-and-specialist-cores` | topology and parameter-sharing mechanism, bounded as fixed-feature evidence |
| adaptive iterations and overthinking | `governed-deliberation-and-test-time-scaling` | fixed-step authority, first/last-correct trajectories, latency/quality counterfactual |
| typed task spell and TaskIR | `cognitive-compilation-and-semantic-ir` | contract preservation and localized repair, with hash-parity failure case |
| request-to-effect tracing | `integrated-reference-architecture` | subsystem effect map and integration receipts |
| low-rank lane bank | `routing-heads-and-specialist-cores` | explicit/oracle lane binding versus learned router ladder |
| champion/challenger frontier | `open-ended-improvement-engines` | same-init, equal-step, single-axis promotion and negative-result retention |
| adapter/trunk truth | `evidence-states-and-claim-discipline` | trainable-state manifests and causal response receipts |
| metric origin taxonomy | `benchmark-ratchets-and-anti-goodhart-evidence` | measured/derived/modeled/constant/declared/vacuous provenance algebra |
| checkpoint relocation failure | `ai-supply-chain-integrity-and-lifecycle-provenance` | content identity plus relocatable resolution |
| memory transition gaps | `context-transactions-snapshots-mounts-and-taint` | transition postconditions and restart-visible state |
| justification-bearing memory | `claim-ledgers-and-belief-revision` | durable-claim gates and typed edge legality |
| replay distinctions | `artifact-graphs-audit-logs-and-replay` | playback versus live re-execution and side-effect reconciliation |
| tribunal method weakness | `evidence-states-and-claim-discipline` | verification method labels and independence graphs |
| capability-envelope gap | `runtime-adapters-tool-permissions-and-human-approval` | enforcement at OS/adapter boundary |
| contradiction monotonicity | `readiness-gates-residual-escrow-and-quarantine` | severity-to-containment monotonicity invariant |
| speech codec overclaim | `multimodal-boundary` if present, otherwise evidence/benchmark chapters | ownership-versus-capability and self-consistent fixture limits |

### Candidate concepts to add explicitly

1. **Trainable-state manifest.** Report generated, frozen, pretrained,
   trainable, and actually updated state separately.
2. **Response-causality receipt.** Prove that the returned text or action came
   from the claimed checkpoint, decoding path, and tools.
3. **Metric provenance algebra.** Make origin class machine-readable and
   claim-gated.
4. **Verification independence graph.** Record shared data, code, artifacts,
   algorithms, models, and operators.
5. **Representation-capacity gate.** Reject metrics whose architecture cannot
   express the evaluated target class.
6. **Router evidence ladder.** Separate specialist existence, labeled binding,
   autonomous selection, calibrated abstention, and end-to-end gain.
7. **Transition postcondition.** Require restart-visible state after memory or
   governance transitions.
8. **Relocatable artifact contract.** Bind content digests independently of
   original absolute paths.
9. **Negative-knowledge frontier.** Preserve retired families, failed axes,
   recombination constraints, and exact rejection evidence.
10. **Ownership/capability matrix.** Prevent first-party or local execution
    from being read as task competence.

### New chapter boundary decision

Do not add a project-specific “Corben model” chapter. The mechanisms map cleanly
into existing model architecture, compiler, memory, routing, evaluation,
provenance, tool, governance, and self-improvement chapters. A distinct chapter
on metric provenance and causal capability receipts could become justified
only after the cross-project synthesis shows that these concepts are not
already adequately owned by evidence discipline and benchmark ratchets.

## Negative-result and failure-lesson ledger

- A sophisticated model topology can still be a fixed feature generator.
- Adapter improvement does not imply trunk improvement.
- A position-specific output table can dominate an apparently recurrent
  learner.
- Exact-sequence metrics are invalid for an architecture that emits one token
  distribution for every position.
- Training and runtime output can be causally disconnected.
- A bank of specialists is not a router.
- Explicit lane labels are not autonomous lane inference.
- Zero deltas for unchanged adapters are not evidence against shared
  interference.
- Absolute artifact paths can make a promoted bank nonportable.
- A named semantic compiler can operate primarily through prefixes, keywords,
  and linear graphs.
- Hash equality or hash-token overlap is not semantic preservation.
- A freeze/thaw receipt can exist without a materialized memory transition.
- A routing budget recreated per request is not a system budget.
- Score-quantile fitting that ignores outcomes is not calibration.
- Contradiction policy can violate monotone containment.
- Verification can be shape-only, dependent, or vacuous while using strong
  terminology.
- Capability declarations do not enforce operating-system authority.
- Recorded playback is not deterministic live replay.
- Missing simulation metadata must not default to real execution.
- Prompt-length latency is not wall-clock latency.
- Fixed compounding factors are not measured recursive improvement.
- First-party tone codecs are not general speech.
- Green historical notes are not current reproduced validation.

## Storage observation

Idea mining is the active priority, and no additional cleanup was performed in
this pass. The current storage is dominated by many JSON checkpoint and
evaluation fragments. Future preservation work should first create a
content-addressed manifest, identify unique versus repeated model/optimizer
states, preserve accepted and negative-result summaries, verify that retained
reports can resolve their inputs after relocation, and only then consider
deduplication or archival. The 8,286 artifact deletions already present mean
that a future compaction plan must compare against the pinned Git tree and must
not assume the working artifact corpus is complete.

## Promotion blockers

- current workspace tests were not reproduced because offline dependencies and
  the requested toolchain were unavailable;
- the worktree's retained artifact corpus is incomplete relative to the pinned
  commit;
- the inner recurrent trunk is not trainable in the inspected serious path;
- no general checkpoint-driven text generation path was established;
- the promoted lane bank contains non-relocatable absolute paths;
- explicit lane metadata substitutes for autonomous routing;
- several runtime subsystems are fixture-driven, empty, per-request, or reduced
  to manifest booleans;
- memory freeze/thaw and tier transitions lack complete material/durable
  postconditions;
- the compiler's digest-parity check is not semantic preservation evidence;
- tool capability declarations are not comprehensively enforced;
- several tribunal and replay checks are shape-only, dependent, or vacuous;
- evaluation metadata includes declared, constant, and modeled quantities
  presented beside measured-looking fields;
- speech evidence is based on acoustic units and a self-consistent tone codec;
- independent literature and external evaluators have not been mapped;
- publication permission for raw project material is not recorded.

## Residual work

- Map exact source symbols from this project to overlapping CCA, MoECOT,
  BeastBrain, BugBrain, and Trainer concepts.
- Determine which mechanisms originated here versus were imported from earlier
  projects or shared architecture notes.
- Perform the program-level cross-project contradiction and terminology pass.
- Rescan the intake directory for projects that completed extraction during
  this mining run.
- Independently reproduce selected source tests after dependency restoration.
- Build minimal adversarial fixtures for metric provenance, router feature
  binding, compiler preservation, memory restart visibility, replay, and tool
  envelope enforcement.
- Add independent literature before converting implementation lessons into
  generalized factual claims.

## Non-claims

This dossier does not claim:

- a trained Corben foundation model or generally useful language model;
- full-trunk learning, model scaling, or parameter efficiency;
- general text generation or causal use of trained logits in returned answers;
- autonomous specialist routing;
- external benchmark performance or independent holdout success;
- semantic compiler correctness or verified localized repair;
- durable semantic memory across restart;
- complete sandboxing, safe arbitrary code execution, or deterministic live
  replay;
- natural speech recognition, intelligible speech synthesis, or measured
  low-latency audio;
- independent verification, calibrated governance, recursive compounding,
  safety, AGI, or ASI;
- a support-state transition or a new book chapter.
