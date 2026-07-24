# Source Note: Gemini Context Caching

| Field | Value |
|---|---|
| Source ID | `ext_gemini_context_caching_docs_2026` |
| Source title | Context caching |
| Ingestion date | 2026-07-23 |
| Source version / URL | Current official documentation inspected 2026-07-23, https://ai.google.dev/gemini-api/docs/caching |
| Ingestion basis | Official product and API documentation; no provider-internal implementation, bill, latency result, or cache behavior was independently reproduced. |

## Thesis

Repeated large prefixes can be reused implicitly or stored explicitly for a
declared lifetime. Cached-token reporting and explicit storage charges make
reuse, retention, and pricing separate decisions.

## Mechanisms

- Implicit common-prefix caching on supported Gemini model families.
- Explicit cached content with a configured time-to-live.
- Cached-token usage reporting.
- Storage charging for explicit retention.

## Evidence

The documentation describes current eligible models, token thresholds, usage
fields, and lifetime semantics. Current Google pricing material reports a
discounted cached-input meter and storage charges, but terms are model- and
date-specific. No repository result reproduces hit rate, latency, billing, or
retention behavior.

## Failure Modes

- Treating implicit caching as guaranteed.
- Paying storage for an entry with low reuse.
- Confusing provider retention with application freshness or legal authority.
- Failing to place shared content before per-request content.
- Comparing discounted input alone while omitting storage, lookup, and misses.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`
- `context-transactions-snapshots-mounts-and-taint`

## Claims To Add Or Update

- Distinguish opportunistic implicit reuse from explicit retained cache state.
- Include storage-time and cache-creation costs in break-even analysis.
- Treat provider usage metadata as evidence of a billed hit, not proof of
  application-level validity.

## Open Questions

- When does explicit retention outperform opportunistic implicit caching?
- How should application invalidation race with provider time-to-live?
- Which cached modalities carry additional privacy or deletion obligations?
