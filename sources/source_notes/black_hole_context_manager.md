# Source Note: Black Hole Context Manager

| Field | Value |
|---|---|
| Source ID | `black_hole_context_manager` |
| Source title | Black Hole Context Collapse Protocol (BHCCP) |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/14KPQT5d86HaFZzQdUr_Sn5p7-8cscSqIZm5zxkijl-I |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/black_hole_context_manager.txt` (541 lines; approximately 2,131 words). Raw text is not published. |
| Evidence role | Corben-authored pseudocode and context-cache design lineage; not an executable package or production result. |

## Thesis

BHCCP proposes a budgeted, tiered context cache in which chunks carry identity,
content, embeddings, timestamps, placement, cached scores, expiry, and security
metadata. A changing goal representation affects candidate residency; dormant
clusters may move to colder storage and later thaw; protected material follows
a different promotion and expiry path; and factual retrieval remains distinct
from generative reconstruction. The useful idea is reversible, observable
context placement under multiple obligations—not the paper's black-hole
physics metaphor or its single semantic-mass score.

## Version lineage

The cache presents a supposed v5.0 “production-ready gold master” before an
older v4.1 “ready for code” specification. Both are partial Python-like
pseudocode, not a complete importable implementation. v5.0 adds character-
entropy caching, goal-vector-sensitive lazy recomputation, rate limiting,
input length checks, HMAC comparison, a confirmation log, K-means freezing and
thawing, a keyword router, and a turn loop. v4.1 exposes the earlier formulas,
TTL proposal, hot/warm/cold description, and Drifting Needle test. v5.0 controls
conflicts, but neither version justifies its maturity label.

## Mechanisms

- Represent context units with stable IDs, content version, source and rights,
  embedding version, timestamps, placement, access history, expiry, and cached
  policy/evaluation results. Entropy and similarity may be fallible features;
  they are not authority or retention decisions.
- Separate protected constraints, active working material, bulk candidates,
  and durable source storage. Placement tiers are physical or operational
  states, not truth, importance, or permission classes.
- Recompute task-relative relevance when a versioned goal representation
  changes materially. Record the old and new goal basis, evaluator, threshold,
  affected candidates, decision, cost, and residual rather than mutating cache
  priority invisibly.
- Apply hysteresis to cold/warm transitions so marginal score variation does
  not thrash storage and context. Freezing must preserve a resolvable source
  reference, representation lineage, thaw condition, and deletion status.
- Protect low-entropy but high-consequence constraints such as “stop,” “no,”
  exclusions, credentials, and legal boundaries through typed criticality and
  policy, not an epsilon hidden inside a multiplicative score.
- Keep exact/source retrieval, derived summaries, and generative reconstruction
  distinct. A query router can propose a route, but the response must expose
  which representation and evidence path actually supplied the answer.
- Test goal drift with required and forbidden needles, irrelevant distractors,
  changed goals, expiry, contradiction, deletion, source restoration, and
  pressure across storage tiers. Retrieving a secret is not universally a
  success criterion.

## Interfaces and invariants

`context-transactions-snapshots-mounts-and-taint` already owns the complete
mechanism: versioned storage state, snapshots, branch-local writes, cache
invalidation, freeze/thaw, taint, rights, retention, deletion closure, replay,
and residuals. `virtual-context-abi` owns representation and admission;
`durable-semantic-memory-and-world-models` owns durable semantic identity;
`security-kernel-and-digital-scifs` owns protected constraints and authority.

Important invariants are: eviction never means deletion without a deletion
transaction; freezing never means source loss; thawing rechecks current
authority, rights, taint, source version, and task fit; a signature authenticates
bytes and signer under a key rather than content truth; goal similarity cannot
override protected constraints; and a cache hit does not imply current
semantic validity.

## Evidence

The source supplies incomplete pseudocode and a proposed five-phase Drifting
Needle scenario. It provides no tracked package, dependency lock, runnable
entry point, test output, model, embedding corpus, task set, memory trace,
latency or resource measurement, poisoning attack, rights test, deletion test,
security test, independent evaluator, or reproduction. The book already has
stronger authored context-transaction fixtures, but those do not validate this
paper's algorithms or thresholds.

## Failure Modes

- Character-distribution entropy is mistaken for semantic novelty,
  importance, difficulty, or evidence value.
- A dot product is treated as cosine similarity without pinning and checking
  embedding normalization and model/version compatibility.
- One weighted or multiplicative mass score hides non-compensating duties such
  as authority, rights, safety, contradiction, provenance, and retention.
- Goal-vector drift silently reprioritizes or removes evidence needed for a
  later audit, rollback, or user instruction.
- K-means assumes spherical clusters and a fixed `k`; small, rare, or
  adversarial constraints are absorbed into an irrelevant centroid.
- Freeze/thaw thresholds are uncalibrated, distribution-dependent, and prone
  to hysteresis failure or permanent dormancy.
- HMAC proves possession of a key and byte integrity, not administrative
  correctness, content truth, non-replay, freshness, or authorization.
- Repeated confirmation rewards persistence and automation rather than
  comprehension; the sample main loop does not demonstrate the confirmation
  route end to end.
- The pseudocode counts characters as tokens, deletes evicted entries rather
  than durably freezing them, leaves methods and hybrid routing incomplete,
  hardcodes a secret, and does not bind persistent state or concurrency.
- A keyword factual/narrative router misroutes paraphrases and ignores mixed,
  adversarial, or ambiguous requests.
- The Drifting Needle example treats recovery of a literal secret as success,
  conflicting with purpose limitation, credential handling, and deletion.

## Explicitly rejected or bounded claims

- “Production-ready,” “Gold Master,” “final build,” and “ready for code” are
  document labels, not evidence of executable completeness or deployment.
- Lazy score caching is not automatically O(1) amortized system behavior;
  K-means, embedding, serialization, searching, and invalidation costs remain.
- Entropy times relevance is not a general measure of memory importance,
  resistance to compression, or semantic mass.
- Three confirmations across 24 hours do not establish truth, criticality,
  informed consent, or resistance to coercion and replay.
- HMAC, input stripping, length limits, and a request deque do not establish
  poisoning, denial-of-service, prompt-injection, or memory security.
- Hot/warm/cold storage, a vector database, and freeze/thaw pseudocode do not
  establish long-context capability, reliable recall, or safe forgetting.

## Section-family closure

| Section family | Disposition |
|---|---|
| Chunk record and lazy cached score | Integrated in context transactions as versioned representation/evaluator state; entropy and mass remain optional fallible features. |
| Rate limiting and input validation | Retained as ordinary boundary controls, explicitly insufficient for semantic or security claims. |
| HMAC and repeated-confirmation Tier 0 | Corrected into separate authenticity, authority, criticality, evidence, and expiry owners; paper thresholds rejected. |
| K-means dormant manager and hysteresis | Existing freeze/thaw prose owns reversible placement, source recovery, and drift obligations; algorithm is a candidate baseline only. |
| Keyword dual-path router | Existing routing and VCM layers already distinguish retrieval and generation with ambiguity/fallback; keyword implementation retained as a weak baseline. |
| Main loop and budget eviction | Existing transaction chapter owns atomicity, snapshots, invalidation, deletion, and replay that this pseudocode omits. |
| v4.1 formula and TTL corrections | Retained as correction history and failure examples, not canonical algorithms. |
| Drifting Needle validation proposal | Converted to a broader research obligation including forbidden needles, privacy, rights, contradiction, expiry, and deletion. |

## Book Chapters Supported

- `context-transactions-snapshots-mounts-and-taint`
- `virtual-context-abi`
- `durable-semantic-memory-and-world-models`
- `security-kernel-and-digital-scifs`

No new chapter or prose section is warranted. The current context-transaction
and VCM chapters already preserve the useful cache, drift, freeze/thaw, and
route distinctions while repairing the source's incomplete implementation and
security model.

## Claims To Add Or Update

- Retain BHCCP as early context-cache design lineage and a source of explicit
  weak baselines, not as production code or evidence.
- Keep placement, epistemic support, criticality, authority, rights, and
  deletion as separate state dimensions.
- Preserve the corrected Drifting Needle experiment as a future comparative
  workload rather than a one-secret retrieval demonstration.

## Research obligations and falsifiers

1. Implement the candidate cache and strong LRU/LFU, semantic retrieval,
   summary-memory, and transaction-aware baselines under identical models,
   corpora, storage, and budgets.
2. Use natural multi-goal histories with rare constraints, negation,
   contradictions, stale facts, protected data, deletion requests, and delayed
   return to dormant goals.
3. Measure exact and semantic recall, forbidden recall, stale use, provenance,
   rights and deletion compliance, thrashing, latency, bytes moved, compute,
   context tokens, task utility, and recovery together.
4. Ablate entropy, similarity, multiplicative scoring, tier policy, hysteresis,
   route classifier, TTL, protected-constraint handling, and source fallback.
5. Falsify the design if simpler policies match it, if rare critical material
   is lost, if dormant clusters fail to thaw correctly, or if cache savings
   increase stale, unauthorized, or unsupported outputs.

## Open Questions

- Which feature families predict future task value without erasing non-
  compensating safety, rights, and evidence duties?
- How should a system estimate goal drift when a conversation contains several
  concurrent or conflicting goals?
- What guarantees can survive approximate nearest-neighbor indexes, embedding
  upgrades, distributed caches, process crashes, and concurrent writes?
- How should a “forget” request interact with dormant storage, backups,
  summaries, embeddings, and later thaw attempts?
