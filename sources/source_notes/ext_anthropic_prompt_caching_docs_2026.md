# Source Note: Anthropic Prompt Caching

| Field | Value |
|---|---|
| Source ID | `ext_anthropic_prompt_caching_docs_2026` |
| Source title | Prompt caching |
| Ingestion date | 2026-07-23 |
| Source version / URL | Current official documentation inspected 2026-07-23, https://platform.claude.com/docs/en/build-with-claude/prompt-caching |
| Ingestion basis | Official product and API documentation; no provider-internal implementation, bill, latency result, or cache behavior was independently reproduced. |

## Thesis

Stable prompt prefixes, including tools, system instructions, and prior
messages, can be written to a temporary cache and read by later requests. Cache
creation, lifetime, and reads are explicit economic objects rather than a free
side effect.

## Mechanisms

- Prefix matching with automatic or explicit cache breakpoints.
- Five-minute and one-hour cache lifetimes.
- Separate cache-creation and cache-read token accounting.
- Prewarming and lifetime refresh behavior under the documented contract.

## Evidence

The official documentation currently prices a five-minute write at 1.25 times
base input, a one-hour write at 2 times base input, and a hit at 0.1 times base
input. Those ratios and eligible models are time-sensitive provider terms, not
universal cache economics. No local workload reproduces them.

## Failure Modes

- Writing expensive cache entries that are never reused.
- Setting breakpoints after volatile content.
- Treating a refreshed lifetime as source-data freshness.
- Confusing the cache lifetime with a right to retain or reuse the material.
- Generalizing provider-specific prices to a self-hosted system.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`
- `context-transactions-snapshots-mounts-and-taint`

## Claims To Add Or Update

- Charge cache creation and reads separately.
- Evaluate lifetime choice against expected reuse and invalidation.
- Preserve prefix order as part of the cache identity.
- Report prewarming as paid work even when no user-visible answer is produced.

## Open Questions

- What reuse distribution makes each lifetime economical?
- How should source corrections and authority revocations override a provider
  lifetime?
- Which workload layouts preserve reuse without making prompts harder to govern?
