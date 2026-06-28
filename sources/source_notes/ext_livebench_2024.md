# Source Note: LiveBench: A Challenging, Contamination-Limited LLM Benchmark

| Field | Value |
|---|---|
| Source ID | `ext_livebench_2024` |
| Source title | LiveBench: A Challenging, Contamination-Limited LLM Benchmark |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2406.19314, https://arxiv.org/abs/2406.19314 |
| Citation label | White et al. (2024), LiveBench |
| Published / updated | 2024-06-27 / 2025-04-18 |
| DOI | 10.48550/arXiv.2406.19314 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the benchmark-science literature queue; paper not vendored into this repository and no LiveBench evaluation reproduced. |

## Thesis

LiveBench belongs in the benchmark, evidence-state, living-book, and open-research chapters as an external benchmark reference for contamination-limited, frequently updated evaluation. It helps the ASI Stack articulate why static benchmark scores decay and why living evaluation surfaces need objective scoring and update discipline.

## Mechanisms

- Add and update questions on a recurring basis from recent information sources.
- Score answers automatically against objective ground-truth values rather than relying solely on LLM judges or crowdsourced preference.
- Cover multiple task categories, including math, coding, reasoning, language, instruction following, and data analysis.
- Release questions, code, and model answers in the source benchmark's own workflow.

## Evidence

- The source reports a live benchmark design and evaluated model results in its own setting.
- This repository has not run LiveBench, reproduced any model score, audited monthly updates, or connected ASI Stack benchmark ratchets to LiveBench.
- Use this source as external living-benchmark vocabulary, not as evidence that this book's tests are contamination-proof.

## Failure Modes

- Monthly updates reduce but do not eliminate all contamination, selection, or task-design risks.
- Objective scoring can still miss governance, evidence-use, or context-adequacy failures outside the task format.
- A living benchmark needs versioned records, update logs, and stale-score invalidation before scores can support claims.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `living-book-methodology` (Living Book Methodology)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use this note to ground contamination-limited and living-benchmark vocabulary.
- Do not claim LiveBench reproduction, contamination-proof local tests, or benchmark-score evidence.
- Keep support state at `argument` until local benchmark versions, command logs, and evidence transitions exist.

## Open Questions

- What benchmark-version record should invalidate stale ASI Stack scores?
- How should living-book releases disclose benchmark age, contamination risk, and retest obligations?
- Which objective scoring patterns could transfer to claim-ledger or reader-release validation?
