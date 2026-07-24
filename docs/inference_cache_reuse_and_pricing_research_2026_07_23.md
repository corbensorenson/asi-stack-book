# Inference cache reuse and pricing research — 2026-07-23

## Decision

The book already mentions KV-cache allocation, warm-prefix controls, operating
system page cache, and semantic context descendants. It does not yet give
inference cache hits one coherent treatment, explain which computation a hit
actually avoids, or show when a lower cached-input price is economically and
semantically honest.

Do not add a standalone cache chapter. Add one coordinated packet to the three
existing owners:

1. `fast-generation-architectures` owns the reuse mechanisms, scheduling,
   performance boundary, and cache-reuse receipt;
2. `resource-economics-and-token-budgets` owns write/read/storage economics,
   break-even analysis, meters, and downstream pricing; and
3. `context-transactions-snapshots-mounts-and-taint` owns response-cache
   validity, dependency closure, invalidation, disclosure, and residual state.

This owner split prevents three recurring category errors: calling a KV hit an
answer hit, calling a semantic answer match exact computation reuse, and
treating numerically reusable state as authorized or fresh.

## Cache taxonomy

| Cache object | Reuse decision | Work usually avoided | Work still required | Primary risk |
|---|---|---|---|---|
| In-request decode KV | Same live sequence and model state | Recomputing prior-token keys and values at every decode step | Next-token model evaluation | Ordinary decode state is mislabeled as a cross-request hit |
| Exact prompt-prefix KV | Exact compatible token prefix and runtime identity | Repeated prefill for the shared prefix | Uncached suffix prefill and new output generation | Incomplete identity, leakage, or stale authority |
| Schema-defined prompt module | Declared module, position schema, and compatible composition | Attention-state computation for reusable modules | Composition and new output generation | Positional or schema mismatch |
| Persistent/disaggregated KV | Exact compatible KV object located in another tier or worker | Repeated prefill after transfer | Lookup, transfer, suffix prefill, and decode | Transfer, storage, lifecycle, and tenant cost |
| Non-prefix or multi-chunk KV | Compatible chunks plus accepted recomputation rule | Part of repeated chunk prefill | Selective or full cross-context recomputation and decode | Missing cross-attention changes quality |
| Exact output memo | Exact bounded request identity and valid dependency closure | Entire model request | Validation, retrieval, disclosure, and downstream checks | Nondeterminism, freshness, or authority drift |
| Semantic response cache | Similar request under a calibrated approximate policy | Entire model request on an accepted hit | Similarity lookup, validity checks, and often verification | False-positive answer reuse |
| Tool, retrieval, and artifact cache | Tool- or source-specific key and freshness contract | External lookup, transformation, or build work | Model inference and downstream validation | Source change or incomplete invalidation |

The taxonomy is semantic, not merely physical. Two objects may occupy the same
Redis cluster or GPU allocator while having different correctness and pricing
contracts.

## Primary-source synthesis

| Source | What it contributes | Mandatory limit |
|---|---|---|
| OpenAI prompt-caching documentation | Current exact-prefix behavior, usage meters, retention, isolation, and the fact that a new output is generated | Product terms are time-sensitive and no internal result is reproduced |
| Anthropic prompt-caching documentation | Explicit cache writes, two lifetimes, read/write meters, breakpoints, and prewarming | Provider ratios are not universal economics |
| Gemini context-caching documentation | Implicit versus explicit reuse, cached-token usage, time-to-live, and explicit storage cost | An implicit hit is not guaranteed and provider retention is not freshness |
| vLLM Automatic Prefix Caching | Chained block identity, adapter/multi-modal identity, eviction, and cache-salt isolation | Design documentation is not a local benchmark or security proof |
| SGLang / RadixAttention | Workload-level prefix trees and cache-aware scheduling | Throughput and scheduling claims retain their paper assumptions |
| Prompt Cache | Schema-defined reusable modules and positional accuracy | Reported TTFT gains are source-scoped |
| Mooncake | Cross-node, cross-tier, prefill/decode-disaggregated KV storage | Production-trace and capacity results are unreproduced |
| CacheBlend | Why naïve non-prefix KV fusion omits cross-attention and how selective recomputation can trade quality and delay | Selective recomputation is not exact equivalence by default |
| Azure LLM semantic-cache policy | Official warning that vector-similar response reuse may be incorrect, outdated, or unsafe | No similarity threshold is universally safe |

The provider documentation was inspected on 2026-07-23. Prices, multipliers,
eligible models, minimum prefix sizes, retention, and rate-limit treatment must
be refreshed before the book makes a current operational recommendation.

## What an exact prefix hit means

For a causal autoregressive transformer, prefill computes key/value state for
the prompt. If a later request begins with the same compatible token sequence,
the runtime can load or retain that prefix state and compute only the uncached
suffix before decoding a new answer. The saved region is prefill. A prefix hit
usually improves time to first token and prefill capacity; it does not make
each newly generated token free, and it does not return the previous answer.

The compatibility key needs more than text:

- provider, model, checkpoint, tokenizer, vocabulary, adapter, quantization,
  runtime, kernel, precision, and any position-encoding identity that affects
  state;
- exact prefix tokens and order, prompt-module schema, image bytes and detail,
  tool definitions, structured-output schema, and reasoning or generation
  configuration where the implementation makes them cache-bearing;
- tenant, principal, sharing class, authority, purpose, policy, rights, privacy,
  source versions, revocation epoch, and cache salt;
- cache format, layer range, block chain, creation time, expiry, and checksum.

Some provider-side identities are opaque. The application receipt should then
record what it requested, what the provider reported as cached, and which
identity dimensions the application could not verify.

## Prompt shape and scheduling

Put the largest stable material first: stable tools, system policy, schemas,
canonical examples, and long reference material. Put per-user, per-turn, and
time-varying material later. This is a performance recommendation only within
the authority and attention needs of the task; it must not move untrusted text
into a privileged instruction position merely to improve hit rate.

At workload scale, reuse also changes scheduling. SGLang motivates grouping or
ordering requests by shared prefix. That can increase reuse but must remain
subordinate to fairness, deadlines, risk, tenant isolation, and backpressure.
A cache-aware scheduler needs both a locality objective and explicit starvation
and tail-latency bounds.

Persistent and disaggregated caches turn recomputation into a placement
decision. Mooncake motivates DRAM, SSD, network, prefill-worker, and
decode-worker tiers. The route should retrieve cached KV only when

\[
t_{\text{lookup}} + t_{\text{transfer}} + t_{\text{validation}}
< t_{\text{recompute}}
\Delta_{\text{queue}},
\]

under the same quality and lifecycle contract. A byte being present on a remote
tier does not mean fetching it is faster, cheaper, fresh, or authorized.

## Non-prefix reuse is a different problem

An independently cached document chunk was originally encoded with some
position and preceding context. Moving or combining that KV state can omit
cross-attention that a full prefill would have computed. CacheBlend is valuable
because it treats that omission as real and selectively recomputes part of the
state. The book should classify this as approximate unless full recomputation
or an accepted equivalence argument restores the same computation. A competent
test needs adversarial order and interaction cases, a full-prefill baseline,
quality and calibration measures, and a method-specific rescue ladder.

## Response caching is not prompt caching

An exact output cache returns a prior answer. It is only exact relative to a
frozen request and dependency closure: model and decoding policy, tool results,
retrieved sources, time and locale, user permissions, policy, side-effect
state, output schema, and any randomness. In many AI uses those dependencies
make full output memoization narrower than it first appears.

A semantic response cache makes a stronger approximation: similarity between
requests is treated as permission to reuse a prior decision. It must therefore
be an explicit risk-qualified route. Dynamic facts, personalized decisions,
legal or medical answers, security actions, rights-sensitive material, and
side-effecting operations should default to fresh evaluation unless a
claim-specific policy and verifier justify reuse. A hit should be disclosed as
reused output, not presented as a new model judgment.

## Cache-hit economics

Let:

- \(S\) be the eligible reusable prefix tokens;
- \(p_u\) be the uncached input price per token;
- \(p_w\) be the effective cache-write price per token;
- \(p_r\) be the cache-read price per token;
- \(N\) be successful reuses after creation;
- \(C_s\) be storage and retention cost; and
- \(C_l\) be lookup, transfer, validation, eviction, and governance cost.

Ignoring suffix and output work that is common to both routes, repeated uncached
prefill costs

\[
C_{\text{uncached}}=(N+1)S p_u .
\]

A simplified explicit-cache route costs

\[
C_{\text{cache}}=S p_w + N S p_r + C_s + C_l .
\]

If \(p_u>p_r\), its simplified reuse break-even is

\[
N >
\frac{S(p_w-p_u)+C_s+C_l}{S(p_u-p_r)}.
\]

Provider contracts meter creation differently, so the actual invoice formula
must replace this abstraction. Misses, partial hits, early eviction, invalid
entries, write amplification, prewarming, and unused retained state must be
included. Output generation, verification, tools, and rate-limit capacity are
not erased by a prefix hit.

As of the inspection date, Anthropic documents a five-minute write at 1.25
times ordinary input, a one-hour write at 2 times, and reads at 0.1 times.
OpenAI documents separate cache-write and cached-input treatment for current
GPT-5.6-family behavior, including a 1.25-times write meter, while cached tokens
still participate in rate limits. Google documents discounted cached input for
supported models and storage charges for explicit retention. These are
examples of contract shapes, not durable price facts.

## Honest downstream pricing

A service may offer cached hits more cheaply, but should base the discount on
the observed receipt rather than an expected hit. Defensible models include:

1. pass through measured uncached, write, read, storage, and output meters plus
   a disclosed service margin;
2. publish a blended rate for a named workload cohort while reconciling actual
   hit rate and retaining an audit trail;
3. charge reservation or retention for explicit cache capacity and a separate
   read rate; or
4. sell bounded capacity or subscription service while still exposing reuse
   and throttling policy.

The service should not call an input-prefix hit a fully cached answer, promise a
discount before it knows the hit occurred, or imply that the provider's lower
compute price removes storage, rate-limit, privacy, support, and governance
cost. A useful `CacheReuseReceipt` includes:

- cache kind, entry ID, key digest, compatible-prefix length, total input
  length, hit/miss/partial state, and miss reason;
- model/runtime identity, tenant/sharing scope, creation and access time,
  lifetime, invalidation epoch, and dependency digest;
- write, read, lookup, transfer, storage-time, eviction, recomputation,
  verification, output, and provider-reported token meters;
- cold/warm class, queue time, TTFT, time per output token, completion time,
  accepted-output state, and fallback;
- disclosure, authority decision, privacy treatment, deletion state, and
  unresolved residuals.

## Metrics and comparison design

Do not optimize raw request hit rate alone. Report:

- eligible, written, read, partially reused, invalidated, evicted, and expired
  tokens;
- request hits, useful-token hit rate, byte hit rate, and saved-prefill estimate;
- cold, warm, steady-state, burst, failover, and adversarial-tenant regimes;
- lookup, hashing, transfer, write, eviction, storage, and recomputation cost;
- TTFT, output-token latency, end-to-end and tail latency, throughput, queueing,
  and fairness;
- output quality, calibration, verifier and repair cost, accepted useful
  outcomes, unsafe reuse, and stale-answer rate;
- cross-tenant exposure, timing leakage, poisoned-entry spread, invalidation
  lag, deletion closure, and failed-cleanup residuals; and
- provider bill, infrastructure bill, energy, human support, and governance cost.

The matched baseline must use the same model, prompt, output work, hardware,
runtime, load, tenant mix, validation, and quality bar with caching disabled or
cold. A negative result is not admissible until cache layout, key correctness,
capacity, lifetime, scheduling, prewarming, and source-recommended settings have
passed self-tests and method-specific rescue.

## Support boundary and next empirical step

This packet adds current source-grounded reader material and no support-state
promotion. The provider contracts, papers, and project documentation are
external comparators. The repository has not deployed a cross-request KV cache,
measured a billed hit, calibrated a semantic response cache, or established
cost savings.

The next empirical step is a natural repeated-prefix workload with at least
three prefix-length and reuse-count regimes, exact output checks against
cache-disabled execution, cold/warm/burst conditions, tenant isolation
negatives, source correction and policy revocation, and complete cost and
latency receipts. Semantic output reuse should be a separate campaign with
deliberately confusable prompts, dynamic facts, poisoning, and risk-tiered
abstention.
