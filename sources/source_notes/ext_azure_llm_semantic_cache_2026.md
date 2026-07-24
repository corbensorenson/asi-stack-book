# Source Note: Azure LLM Semantic Cache Lookup Policy

| Field | Value |
|---|---|
| Source ID | `ext_azure_llm_semantic_cache_2026` |
| Source title | Azure API Management LLM semantic cache lookup policy |
| Ingestion date | 2026-07-23 |
| Source version / URL | Current official documentation inspected 2026-07-23, https://learn.microsoft.com/en-ie/azure/api-management/llm-semantic-cache-lookup-policy |
| Ingestion basis | Official product documentation; no local semantic-cache deployment or quality result. |

## Thesis

A semantic response cache uses vector similarity to decide whether a prior
answer may satisfy a new request. That is approximate decision reuse, not an
exact prefix-computation hit, and the documentation explicitly warns that a
hit can be incorrect, outdated, or unsafe.

## Mechanisms

- Embed a request and search cached requests by vector similarity.
- Use a configurable similarity threshold.
- Partition lookup with vary-by values.
- Return a stored model response on a qualifying hit.

## Evidence

The documentation specifies policy behavior and a correctness warning. It does
not establish a universally safe similarity threshold, semantic equivalence,
freshness, or cost benefit.

## Failure Modes

- False-positive similarity returns the wrong answer.
- Dynamic, personal, time-sensitive, or authority-sensitive questions reuse stale output.
- Prompt injection or poisoned answers spread through the cache.
- Tenant or policy partitions are incomplete.
- Users cannot tell that no new model evaluation occurred.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`
- `context-transactions-snapshots-mounts-and-taint`

## Claims To Add Or Update

- Treat semantic hits as an explicit approximate route with risk-class admission.
- Bind source, tenant, authority, policy, time, and answer dependencies to each entry.
- Disclose answer reuse and preserve a fallback to fresh evaluation.

## Open Questions

- Which task classes, if any, admit safe semantic response reuse?
- How should similarity thresholds be calibrated against harmful false positives?
- Can an independent verifier make semantic hits useful without spending the saved cost?
