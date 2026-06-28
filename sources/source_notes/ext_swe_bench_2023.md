# Source Note: SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

| Field | Value |
|---|---|
| Source ID | `ext_swe_bench_2023` |
| Source title | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2310.06770, https://arxiv.org/abs/2310.06770 |
| Citation label | Jimenez et al. (2023), SWE-bench |
| Published / updated | 2023-10-10 / 2024-11-11 |
| DOI | 10.48550/arXiv.2310.06770 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the benchmark-science literature queue; paper not vendored into this repository and no SWE-bench evaluation reproduced. |

## Thesis

SWE-bench belongs in the benchmark, artifact-graph, Labor OS, and prototype-roadmap chapters as an external benchmark reference for real-world software issue resolution. It gives the ASI Stack a concrete comparison point for long-context code understanding, repository-scale edits, execution-environment interaction, and patch acceptance.

## Mechanisms

- Draw software-engineering problems from real GitHub issues and pull requests.
- Ask a model or agent to edit a codebase to resolve the issue.
- Require coordination across files, functions, classes, and execution feedback in the source setting.
- Evaluate resolution against issue-specific tests or acceptance criteria rather than generic code-generation completion alone.

## Evidence

- The source reports benchmark construction, model baselines, and issue-resolution difficulty.
- This repository has not run SWE-bench, solved any benchmark issue, reproduced model scores, or connected Codex edits to a tracked SWE-bench result.
- Use this source as real-world software-evaluation vocabulary, not as local evidence for Labor OS or artifact-steward performance.

## Failure Modes

- Passing a software benchmark can reward narrow patching without proving broader governance, rollback, or artifact lineage.
- Real-world issue benchmarks can still age, leak, or become optimized by benchmark-specific tooling.
- Code changes need replayable logs, tests, and artifact records before they support claims about autonomous work quality.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `artifact-graphs-audit-logs-and-replay` (Artifact Graphs, Audit Logs, and Replay)
- `labor-os-and-typed-jobs` (Labor OS and Typed Jobs)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to ground real-world software-engineering benchmark vocabulary.
- Do not claim local SWE-bench performance, issue-resolution capability, or benchmark reproduction.
- Keep support state at `argument` until command logs, environment records, test results, and accepted evidence transitions exist.

## Open Questions

- Which artifact-graph fields are required to replay a code-agent patch attempt?
- How should Labor OS distinguish an accepted patch from a governed, reversible, auditable job?
- What benchmark ratchet would prevent overfitting to public issue-resolution tasks?
