# Source Note: Claw-SWE-Bench

| Field | Value |
|---|---|
| Source ID | `ext_claw_swe_bench_2026` |
| Source title | Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks |
| Ingestion date | 2026-07-11 |
| Source version / URL | arXiv:2606.12344, https://arxiv.org/abs/2606.12344 |
| Citation label | Zheng et al. (2026), Claw-SWE-Bench |
| Published / updated | 2026-06-10 / 2026-06-10 |
| DOI | 10.48550/arXiv.2606.12344 |
| Ingestion basis | Current primary preprint metadata and abstract reviewed; benchmark and reported scores were not reproduced. |

## Thesis

Coding-agent evaluation depends materially on the harness contract, so model,
workspace, patch extraction, evaluator, runtime budget, and cost must be fixed.

## Mechanisms

- Fixed prompt/workspace/patch/evaluator contracts across agent harnesses.
- Multilingual issue-resolution tasks and a lower-cost reference subset.
- Separate model-choice, harness-choice, accuracy, and cost comparisons.

## Evidence

The preprint reports substantial harness and model effects under its benchmark.
Those values are not local results and the paper is not yet treated as settled.

## Failure Modes

Adapter quality can dominate; public issues can contaminate; cost-matched and
accuracy-matched rankings can disagree; a patch score omits governance.

## Book Chapters Supported

- `artifact-graphs-audit-logs-and-replay`
- `runtime-adapters-tool-permissions-and-human-approval`
- `resource-economics-and-token-budgets`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

Bind harness identity and cost to repository-agent outcomes and avoid attributing
harness gains to the model alone.

## Open Questions

- Which harness surfaces must enter a replay digest?
- How should contamination-limited replacements preserve cost comparability?
