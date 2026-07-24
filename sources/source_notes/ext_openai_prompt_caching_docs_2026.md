# Source Note: OpenAI Prompt Caching

| Field | Value |
|---|---|
| Source ID | `ext_openai_prompt_caching_docs_2026` |
| Source title | Prompt Caching |
| Ingestion date | 2026-07-23 |
| Source version / URL | Current official documentation inspected 2026-07-23, https://developers.openai.com/api/docs/guides/prompt-caching |
| Ingestion basis | Official product and API documentation; no provider-internal implementation, bill, latency result, or cache behavior was independently reproduced. |

## Thesis

Exact reusable prompt prefixes can avoid repeated prefill work. The provider
exposes cached and cache-write token accounting so a caller can distinguish
ordinary input from reused input, but each request still generates a new
output.

## Mechanisms

- Automatic exact-prefix matching above documented token thresholds.
- Routing hints and explicit breakpoints for improving reusable-prefix locality.
- Separate usage fields for cached reads and, on supported models, cache writes.
- Bounded retention and organization-level isolation.

## Evidence

The documentation specifies current public API behavior. On the current
GPT-5.6 family, cache creation and cache reads have distinct billing treatment;
cached input is reported in usage metadata. Exact product multipliers, eligible
models, thresholds, and lifetimes are time-sensitive. No repository artifact
reproduces provider latency, cost, capacity, or isolation.

## Failure Modes

- Calling a generated response an output-cache hit when only prefill state was reused.
- Placing volatile content before the stable prefix and destroying reuse.
- Assuming cached tokens do not count toward rate limits or capacity.
- Omitting model, tokenizer, tool, image, schema, tenant, or policy identity
  from a cache-eligibility record.
- Treating provider isolation and retention text as a proof of the book's own
  implementation.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`
- `context-transactions-snapshots-mounts-and-taint`

## Claims To Add Or Update

- Separate prefill-state reuse from answer reuse.
- Make provider-reported read and write meters part of the request receipt.
- Price cached input from observed usage rather than an expected hit.
- Bind reuse to the exact identity and retention contract in force.

## Open Questions

- How stable are hit rate and time-to-first-token under mixed tenants and load?
- Which request fields invalidate provider-side reuse for each model family?
- How should a downstream service share savings without misrepresenting capacity
  or rate-limit costs?
