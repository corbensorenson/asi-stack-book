# Source Note: MonitorBench

| Field | Value |
|---|---|
| Source ID | `ext_monitorbench_2026` |
| Source title | MonitorBench: A Comprehensive Benchmark for Chain-of-Thought Monitorability in Large Language Models |
| Ingestion date | 2026-07-14 |
| Source version / URL | arXiv:2603.28590v2, https://arxiv.org/abs/2603.28590 |
| Citation label | Wang et al. (2026), MonitorBench |
| Published / updated | 2026-03-30 / 2026-04-02 |
| DOI | 10.48550/arXiv.2603.28590 |
| Ingestion basis | Primary arXiv HTML abstract, introduction, benchmark design, stress-test, results, and limitations passages reviewed; benchmark code and models were not run locally. |

## Thesis

Monitorability is a property to test, not an automatic benefit of visible
reasoning. MonitorBench supplies 1,514 instances across 19 tasks and seven
categories, plus two stress-test settings designed around decision-critical
factors. Its reported results include lower monitorability for some more
capable systems and deliberate degradation of up to 30 percent in some tasks.

## Mechanisms

- Construct held-out cases with named decision-critical factors.
- Separate ordinary monitorability from adversarially reduced monitorability.
- Compare behavior across task categories and model-capability levels.
- Preserve task structure: monitorability is stronger where solving the task
  requires reasoning through the decision-critical factor.

## Evidence

The source is a primary open benchmark report. It changes the book's evidence
design by requiring trace/action stress tests across task types rather than a
single plausibility judge. The repository has not reproduced its benchmark or
validated the reported model comparisons.

## Failure Modes

- Benchmark association does not prove causal faithfulness.
- Capability and closed/open model status are confounded with architecture,
  training, disclosure, and task composition.
- A visible decision-critical factor may still omit hidden computation.
- Stress-test coverage is finite and cannot establish future monitorability.

## Book Chapters Supported

- `scalable-oversight-and-adversarial-ai-control`
- `adversarial-evaluation-sandbagging-and-training-time-deception`

## Claims To Add Or Update

- Make monitorability a held-out, adversarial evaluation target.
- Report task structure, model access, stress condition, denominator, and
  degradation together.
- Do not infer oversight quality or safety from visible reasoning alone.

## Open Questions

- Which monitorability tasks best represent tool use and multi-agent routing?
- How should monitorability be evaluated when private reasoning is unavailable?
- What stop rule should apply when capability rises while monitorability falls?
