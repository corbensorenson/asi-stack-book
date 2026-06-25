# Source Note: Break the Sequential Dependency of LLM Inference Using Lookahead Decoding

| Field | Value |
|---|---|
| Source ID | `ext_lookahead_decoding_2024` |
| Source title | Break the Sequential Dependency of LLM Inference Using Lookahead Decoding |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2402.02057, https://arxiv.org/abs/2402.02057 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation literature queue; paper not vendored into this repository. |

## Thesis

Lookahead decoding attacks the serial dependency of autoregressive inference by using parallel decoding steps without an auxiliary draft model or data store. For the ASI Stack, it is a source-noted example of exact decoding acceleration whose cost model trades extra per-step computation for fewer total decoding steps.

## Mechanisms

- Generate candidate n-grams or continuation structure in parallel.
- Verify candidates with the same model rather than a separate draft model.
- Trade additional per-step computation for fewer serial decoding steps.
- Maintain compatibility with memory-efficient attention approaches under the paper's setup.
- Measure speed by wall-clock behavior under concrete model, task, and hardware conditions.

## Evidence

- The source reports acceleration on evaluated tasks and implementations.
- The repository has not run the Lookahead Decoding implementation or reproduced its measurements.
- Use the source to support lookahead/trie/branch-verification taxonomy, not local speed claims.

## Failure Modes

- Extra FLOPs per step can dominate when parallel hardware or batching is insufficient.
- Exactness claims are method-specific and must not be generalized to unrelated branch caches.
- Workloads with low branch predictability may get less benefit.
- Memory-efficient attention compatibility does not imply end-to-end governed-output quality.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)

## Claims To Add Or Update

- Use this source to replace unmined lookahead queue language with a source-noted exact parallel decoding family.
- Keep benchmark requirements focused on serial-step count, extra FLOPs, verifier cost, and useful solution per second.
- Do not claim the repository has implemented lookahead decoding.

## Open Questions

- What generation-mode record fields should count extra per-step FLOPs against reduced serial steps?
- Which tasks should test branch predictability and fallback behavior?
- How should lookahead decoding interact with procedural-memory shortcuts and stale cache controls?
