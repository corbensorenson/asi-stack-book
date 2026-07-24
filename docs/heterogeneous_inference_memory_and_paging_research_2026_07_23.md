# Heterogeneous Inference Memory and Paging Research

Date: 2026-07-23
Status: research intake and reader-prose integration complete; policy, validator, planner, and empirical packet queued behind the active Round 17 sequence
Support effect: none
Chapter-admission effect: none

## Decision

Do not add a new chapter.

The material belongs to an existing-owner packet led by
`fast-generation-architectures`. That chapter already owns generation-route
latency, throughput, cache, bandwidth, and fallback accounting and already
contains the PagedAttention comparator. Four adjacent owners receive bounded
handoffs:

- `personal-compute-hives-and-federated-edge-intelligence` owns the
  consumer-device profile and admission of a memory policy on a particular
  machine;
- `resource-economics-and-token-budgets` owns I/O, energy, endurance, latency,
  and displaced-capacity accounting;
- `model-weight-custody-and-hardware-roots-of-trust` owns exact weight-page
  identity, integrity, encryption, recovery, sanitization, and descendant
  custody; and
- `replaceable-cognitive-substrates-beyond-transformer-monoculture` owns the
  requirement that page granularity and prediction policy adapt to dense,
  sparse, MoE, recurrent, state-space, and future substrates.

The Virtual Context ABI should receive only an explicit boundary note:
semantic context pages are governed information objects, while weight, KV,
activation, and expert pages are physical runtime objects. Similar paging
vocabulary does not make their identity, authority, eviction, or correctness
contracts interchangeable.

The initial intake was research-only. On 2026-07-23, the owner expressly
commissioned the reader prose, and the five owner sections plus the Virtual
Context boundary were written and source-reconciled as a bounded exception to
the Round 17 sequencing rule. No chapter owner was created, no support state
changed, and the policy, validation, planner, hardware, and empirical work
remain deferred.

## What the source family actually covers

“Paging a large model” is not one mechanism. The book should keep at least five
objects and three memory tiers distinct.

| Object | Typical lifetime | Exact or approximate variants | Principal risk |
|---|---|---|---|
| Model-weight pages | checkpoint or adapter version | exact shards; quantized or sparse approximations | every decode step may rescan more bytes than the storage path can supply |
| KV-cache pages | request, prefix, or session | exact offload; eviction, quantization, token selection, or reconstruction | long context and batching grow transient state; a wrong fetch can change output |
| Activation pages | layer or microbatch | recompute, checkpoint, compress, or spill | transfer and recomputation can erase the apparent memory saving |
| Expert/neuron pages | route or token | exact expert load; predicted hot/cold activation; sparse execution | misprediction, architecture dependence, and hidden accuracy loss |
| Draft/verifier state | speculative generation step | exact target plus approximate draft | acceptance and rollback costs can dominate the claimed speedup |

The relevant hierarchy is usually accelerator memory to host DRAM to
NVMe/SSD. A future policy may add remote memory or compute-enabled storage, but
those are separate transfer, authority, and failure domains.

## Primary-source synthesis

| Source | Mechanism worth retaining | Boundary that must remain visible |
|---|---|---|
| AirLLM | Split a model into layer shards, keep roughly one layer on the GPU, prefetch the next shard, and optionally compress storage representation. | Official implementation claims, not an independent paper reproduction. “Fits in VRAM” says nothing about usable latency, storage bandwidth, SSD endurance, model quality, or failure recovery. |
| DeepSpeed Inference | Treat GPU, CPU, and NVMe as a heterogeneous inference hierarchy for dense and sparse Transformer models. | Source-reported scale and throughput remain hardware, configuration, model, and workload specific. |
| FlexGen | Jointly plan tensor placement and access across GPU, CPU, and disk; use batching and optional 4-bit weights/cache for latency-insensitive throughput. | Its target workload is explicitly latency-insensitive batched generation. A batch-amortized throughput result is not an interactive-latency result. |
| Hugging Face Accelerate | Current implementation reality for automatic or explicit GPU/CPU/disk device maps and memory-mapped disk tensors. | The documentation notes sequential dispatch, unoptimized model parallelism, absent weight prefetch in the described path, and potentially very slow disk offload. Capability is not qualification. |
| llama.cpp | Current implementation reality for memory mapping, DirectIO, CPU/GPU layer placement, MoE CPU placement, and KV-cache offload/type controls. | Operating-system page-cache behavior, load mode, quantization, KV placement, and tensor placement are separate knobs; benchmark all exact settings. |
| LLM in a flash | Use a flash-aware cost model, reduce bytes transferred, and increase contiguous read size through windowing and row-column bundling. | Sparsity-aware selective loading is not exact dense layer streaming; reported speedups are against the paper’s naive baselines and hardware setting. |
| PowerInfer | Exploit source-reported power-law neuron locality: keep hot neurons on GPU, cold neurons on CPU, and predict activation. | This is architecture- and predictor-dependent approximate sparse execution, not a general exact paging result. |
| PagedAttention | Page dynamically growing KV state to reduce fragmentation and duplication and improve batching. | It is KV-cache allocation inside serving, not SSD weight paging, semantic context paging, or proof of answer quality. |
| vAttention | Preserve contiguous virtual KV addresses while dynamically mapping physical GPU memory with CUDA virtual memory APIs. | It is an important counterexample to assuming non-contiguous PagedAttention-style layouts are always the right abstraction. |
| InfiniGen | Use a partial next-layer rehearsal to speculate important tokens and prefetch selected host-resident KV entries. | A predicted subset introduces accuracy, miss, fallback, and architecture-specific evidence obligations. |
| SpeCache | Keep the complete KV cache in CPU memory, retain a low-bit importance copy in VRAM, and prefetch predicted next-step KV pairs. | “Complete cache in host memory” does not make each GPU step exact unless the selection, fetch, miss, and fallback path is demonstrated. |
| SpecOffload | Compose model offloading with speculative decoding and place a draft model in otherwise underused GPU capacity. | This is speculative decoding plus offloading, not speculative page prediction. Its planner and acceptance behavior require separate measurement. |
| ATSInfer | Very recent tensor-granular static placement plus load-aware dynamic transfer and asynchronous CPU-GPU coordination on consumer devices. | It is a July 2026 preprint reviewed at abstract level only. Its reported gains require full-paper review and independent reproduction before use beyond roadmap design. |

## Terminology the book should standardize

- **Residency:** where an exact object is currently stored.
- **Placement:** the planned steady-state assignment of objects to tiers.
- **Offload:** movement or execution outside the primary accelerator.
- **Demand paging:** fetch after a required object is identified.
- **Prefetch:** fetch before the object blocks execution.
- **Speculative paging:** predict a future required physical page or page set,
  start the fetch early, and preserve an exact miss/fallback path.
- **Speculative decoding:** propose future tokens with a draft mechanism and
  verify them with the target model.
- **Approximate paging policy:** reduces or transforms fetched state through
  sparsity, selection, compression, quantization, eviction, or reconstruction.
- **Exact paging policy:** changes residency and schedule without changing the
  mathematical state consumed by the model, modulo explicitly recorded
  numerical-layout effects.

The manuscript must not use “speculative paging” as a synonym for speculative
decoding. InfiniGen and SpeCache predict KV fetches; SpecOffload composes
offloading with draft-token speculation; AirLLM’s next-layer prefetch is a
mostly deterministic pipeline rather than learned speculation.

## Required physical-memory policy

Create a versioned `Heterogeneous Inference Memory Policy` with:

1. exact model, tokenizer, adapter, quantization, tensor-layout, runtime,
   kernel, driver, operating-system, filesystem, storage-device, and hardware
   identities;
2. separate object classes for weights, KV state, activations, experts,
   recurrent state, draft state, metadata, and recovery state;
3. per-class page or shard identity containing object version, layer or module,
   tensor range, shape, dtype, compression, checksum, and authority;
4. tier capacities, reserved floors, bandwidth, latency, concurrency, thermal,
   energy, endurance, and failure assumptions;
5. placement, eviction, prefetch, prediction, admission, backpressure,
   fallback, and recovery policies;
6. explicit exact-versus-approximate status for every transformation;
7. correctness checks for page identity, freshness, completeness, numerical
   equivalence, isolation, and request ownership;
8. prediction confidence, prefetch precision/recall, late-fetch and unused-fetch
   rates, miss penalties, and an exact recovery route;
9. separate prefill, decode, batch, long-context, prefix-reuse, MoE, and
   interruption workload policies;
10. resource and lifecycle receipts covering bytes by tier, page faults,
    transfer overlap, stalls, compute utilization, first-token latency,
    inter-token latency, throughput, tail latency, energy, temperature,
    SSD read/write amplification, wear proxy, cost, and failure recovery; and
11. expiry, invalidation, crash recovery, revocation, sanitization, and residual
    ownership for pages, caches, shards, replicas, and transformed descendants.

## Invariants

- A page hit is valid only for the exact object version, request or sharing
  scope, layout, precision, and authority.
- No cache or prefetch reuse may cross a tenant, model, adapter, tokenizer,
  rights, taint, or revocation boundary without an explicit compatible lease.
- Exact residency changes and approximate state changes are evaluated as
  different arms.
- A prediction miss must not silently change model state. It stalls, fetches,
  recomputes, or routes to an explicit approximate arm.
- A prefetch win is counted only after unused reads, cache pollution, evictions,
  extra energy, transfer contention, and tail regressions are charged.
- “The model loads” and “a token was emitted” are not useful-inference
  qualification.
- SSD capacity does not imply SSD bandwidth, endurance, thermal stability,
  crash consistency, integrity, or acceptable latency.
- Quantization and sparse activation need quality-sensitive evaluation and may
  not inherit correctness from an exact paging baseline.
- Prefill and decode are different workloads; batch throughput may not stand in
  for interactive latency.
- Page-layout choices must remain compatible with the kernels actually used;
  vAttention prevents the book from treating one non-contiguous layout as
  universally optimal.
- Recovery must cover incomplete transfers, torn or corrupted shards, stale
  caches, process crashes, storage loss, out-of-space, and fallback failure.

## False-negative-resistant evaluation

The implementation packet must not run a naive one-off “large model on small
GPU” demo and call a slow result a refutation. It must first prove that each arm
is a competent implementation for its own mechanism.

### Hardware matrix

At minimum record:

- one low-VRAM discrete-GPU machine with fast NVMe and sufficient host RAM;
- one low-VRAM machine where host RAM is also constrained enough to exercise
  disk residency;
- one unified-memory or CPU-first consumer comparator when available; and
- measured sequential and random storage bandwidth, PCIe bandwidth, host-memory
  bandwidth, filesystem/page-cache behavior, thermal state, and power policy.

Unavailable hardware classes receive an honest deferred disposition, not a
simulated performance result presented as measured.

### Model and workload matrix

Use at least two dense model sizes relative to VRAM and one sparse/MoE or
activation-sparse candidate when a competent implementation exists. Separate:

- cold start, warm start, and steady state;
- short interactive batch-1 prompts;
- latency-insensitive batches;
- long prefill and long decode;
- repeated-prefix/cache-reuse workloads;
- concurrent requests with different lengths;
- interruption, cancellation, and recovery; and
- adversarial predictor/locality shifts.

### Matched arms

1. smallest fully resident model that meets the task contract;
2. CPU-only or unified-memory baseline;
3. ordinary partial CPU/GPU offload;
4. AirLLM-style layer streaming;
5. FlexGen-style planned heterogeneous placement when reproducible;
6. PagedAttention or equivalent KV serving baseline;
7. contiguous-virtual-memory KV alternative where supported;
8. exact full-host-KV offload;
9. InfiniGen/SpeCache-style predicted KV prefetch;
10. sparse hot/cold neuron or expert placement where architecture-compatible;
11. speculative-decoding-plus-offload composition; and
12. conservative fallback with prediction disabled.

Arms that combine quantization, sparsity, paging, scheduling, and speculative
decoding require factorial ablations or an explicit inability-to-isolate
residual. Do not credit a compound result to paging alone.

### Metrics and admission gates

Report median and tail first-token latency, inter-token latency, end-to-end
latency, tokens per second, requests per second, useful accepted task success,
quality and exactness, peak VRAM/RAM, bytes read and written per generated
token, transfer overlap, page-fault/miss behavior, prefetch precision and
recall, cache pollution, compute utilization, energy, thermal throttling,
storage wear proxy, startup conversion/storage amplification, crash recovery,
and total cost.

A route is admitted only for the workload region where it is jointly competent
on task quality, latency or throughput objective, memory ceiling, stability,
recovery, and lifecycle cost. No universal “best paging method” claim is
allowed.

## Chapter implementation packet — manuscript slice completed 2026-07-23

### Fast Generation Architectures — primary owner

Add a substantial section titled **Heterogeneous inference memory: residency,
paging, and prediction**. It should:

- separate weight, KV, activation, expert, recurrent, and draft state;
- compare layer streaming, planned placement, demand paging, virtual-memory KV
  allocation, predictive KV prefetch, sparse hot/cold placement, and
  speculative-decoding/offload composition;
- explain why bandwidth and arithmetic intensity make some methods
  batch-friendly but interactive-latency hostile;
- introduce the physical-memory policy and exact/approximate boundary;
- add a worked example from checkpoint shards on SSD through a request closure;
- add the matched-arm evaluation matrix and promotion limits; and
- preserve PagedAttention versus vAttention as a live design alternative.

### Personal Compute Hives — consumer admission handoff

Add **Memory-tier admission inside a worker**:

- publish a worker memory/storage capability card;
- reject policies whose largest indivisible object does not fit the execution
  tier;
- bind storage, RAM, accelerator, thermal, battery, and concurrency ceilings;
- distinguish “runnable” from interactive, batch, and background qualification;
- fail closed on unknown storage integrity, insufficient scratch space, or
  unusable recovery; and
- route jobs to the least-authority adequate model and machine before paging a
  much larger model merely because the SSD has capacity.

### Resource Economics — full lifecycle accounting

Add **The I/O roofline and the price of virtual VRAM**:

- derive bytes-per-token lower bounds for weight streaming;
- distinguish random and sequential I/O and page-cache effects;
- charge shard conversion, duplicate storage, cold starts, unused prefetch,
  cache pollution, energy, thermal throttling, and storage wear;
- plot quality/latency/throughput/memory/cost frontiers rather than VRAM alone;
- treat capacity, bandwidth, latency, and endurance as separate resources; and
- retain workload-specific admission instead of a single ranking.

### Model-Weight Custody — storage integrity handoff

Add **Paged weight custody**:

- content-address and checksum every transformed shard;
- bind parent checkpoint, adapter, quantization, layout, and runtime
  compatibility;
- preserve encryption and key lifecycle for SSD-resident pages;
- make partial conversion and out-of-space states recoverable;
- include page-cache, scratch, backup, and deleted-original behavior in the
  derivative closure; and
- distinguish cache eviction, file deletion, cryptographic erasure,
  sanitization, and recipient recall.

### Replaceable Cognitive Substrates — architecture handoff

Add **Paging policy is substrate-specific**:

- dense Transformers favor predictable layer/KV structure;
- sparse/MoE systems add expert activation prediction and cold-expert fallback;
- recurrent and state-space systems move different state and may reduce KV
  pressure without eliminating weight traffic;
- architecture-specific locality predictors must be evaluated under shift; and
- the Cognitive Kernel ABI should expose memory objects and costs without
  forcing every substrate into Transformer layer or KV terminology.

### Explicit no-change owners

- `virtual-context-abi`: add only the semantic-versus-physical page boundary.
- `governed-model-training-distributed-optimization-and-scaling`: keep
  inference paging separate from optimizer/gradient/checkpoint offload; cite
  training systems only when that distinction is being taught.
- `compact-generative-systems-and-residual-honesty`: no separate source packet;
  it already owns hidden reconstruction and compression burden.

## Terminal artifacts

The future packet is terminal only when all of the following exist and pass:

1. source records, notes, manifest assignments, outline queues, Appendix H, and
   chapter source crosswalks are synchronized;
2. the five owner edits and Virtual Context boundary are reader-complete;
3. `schemas/heterogeneous_inference_memory_policy.schema.json`;
4. at least two valid policies and rejecting fixtures for wrong shard identity,
   stale KV ownership, hidden approximation, missing miss fallback, capacity
   overcommit, absent scratch/recovery, unbounded prefetch, missing I/O or wear
   accounting, and support overclaim;
5. an independent schema/policy validator;
6. a hardware characterization receipt and workload manifest;
7. a dry-run planner that emits placement, transfer, and fallback decisions
   without claiming performance;
8. a competent benchmark protocol with preregistered rescue and disqualification
   rules;
9. measured empirical receipts only if suitable hardware, models, and
   implementations are actually available;
10. a chapter/outline/glossary/Appendix C/H/reader reconciliation packet;
11. a W3 inheritance check and current atom projection; and
12. explicit nonclaims for unrun methods, unavailable hardware, unreproduced
    source results, transfer, deployment, support, SOTA, AGI, and ASI.

## Source status

The research packet reviewed public primary-paper abstracts/metadata and
official implementation documentation on 2026-07-23. Reported performance
numbers remain source-reported. Full-paper passage review and independent
reproduction are required before empirical use. The July 2026 ATSInfer record
is especially provisional because of its recency.
