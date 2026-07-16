# Source Note: Benchmaxxing

| Field | Value |
|---|---|
| Source ID | `benchmaxxing` |
| Source title | Benchmaxxing: The Performance Ratchet |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public Release v1.0, May 2026; Google Docs raw cache |
| Ingestion basis | local raw cache at `sources/raw/google_docs/benchmaxxing.txt` |

## Thesis

Benchmaxxing frames AI development as a performance ratchet: evaluate against a benchmark frontier, improve data/training/inference/tools while progress remains possible, promote saturated benchmarks to regression status, diagnose walls, and change architecture only when simpler interventions no longer move the frontier. Benchmarks are temporary pressure surfaces, not permanent definitions of intelligence.

## Mechanisms

- Maintain a benchmark lifecycle with frontier, diagnostic, regression, retired, and live benchmarks.
- Diagnose walls as data-limited, training-limited, inference-limited, benchmark-limited, or architecture-limited.
- Use benchmark ledgers and model ledgers to preserve what changed, why it changed, and which residuals remain.
- Apply anti-Goodhart safeguards: rotation, private holdouts, benchmark mutation, multi-metric evaluation, transfer checks, contamination audits, and capability narratives.
- Treat architecture change as a hypothesis justified by residual evidence, not as the first response to a disappointing score.

## Evidence

- The source is a conceptual framework and development methodology.
- It contains source-reported references to scaling laws, compute-optimal training, HELM-style evaluation, long-horizon task measurement, Humanity's Last Exam, SWE-bench benchmark changes, benchmark mutation, Goodhart risk, and label-error concerns.
- It provides examples for coding agents, knowledge/reasoning benchmarks, and long-horizon agents.
- No benchmark harness, benchmark mutation, or empirical run was performed in this repo as part of this note.

## Failure Modes

- Benchmark gaming, leaderboard addiction, and overfitting to benchmark style.
- Premature architecture escalation before data, training, or inference interventions are exhausted.
- Benchmark stagnation and regression blindness.
- Evaluation noise, contamination, weak transfer, and safety neglect.

## Book Chapters Supported

- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `capability-replacement-and-rollback` (Capability Replacement and Rollback)
- `recursive-self-improvement-boundaries` (Recursive Self-Improvement Boundaries)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores; includes folded MoECOT Runtime Crosswalk)
- `replaceable-cognitive-substrates-beyond-transformer-monoculture` (Replaceable Cognitive Substrates: Beyond Transformer Monoculture)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `capability-thresholds-and-deployment-commitments` (Capability Thresholds and Deployment Commitments)
- `safety-cases-and-structured-assurance` (Safety Cases and Structured Assurance)
- `adversarial-evaluation-sandbagging-and-training-time-deception` (Adversarial Evaluation, Sandbagging, and Training-Time Deception)
- `open-ended-improvement-engines` (Open-Ended Improvement Engines)
- `fast-generation-architectures` (Fast Generation Architectures)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `integrated-reference-architecture` (Integrated Reference Architecture)
- `prototype-roadmap` (Prototype Roadmap)
- `living-book-methodology` (Living Book Methodology)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Benchmaxxing can support source-derived claims about benchmark lifecycle, wall diagnosis, anti-Goodhart safeguards, and architecture-change discipline after specific claims are mapped.
- Use Benchmaxxing to require accepted-output, task-success, repair-cost, regression, and holdout measurements before any fast-generation mode is treated as an improvement.
- Use Benchmaxxing to define benchmark, regression, holdout, saturation, and anti-Goodhart inputs for policy-update evaluation records; do not treat benchmark pressure itself as proof of reward quality.
- Use its baseline, coverage, regression, and residual vocabulary for a threshold commitment's assessment inputs; it does not set a threshold, establish a crossing, verify a safeguard, or authorize deployment.
- Use its benchmark lifecycle, regression, residual, and anti-Goodhart vocabulary as bounded case-reference inputs; it does not construct a safety case, establish evidence adequacy, safety, readiness, or release authority.
- It should not be used to claim that any particular model, prototype, or chapter benchmark has passed unless the benchmark run is recorded separately.

## Open Questions

- Which book-level Codex tests should be structured as benchmark-ratchet fixtures?
- How should the book distinguish source-reported benchmark claims from locally reproduced results?
- Which benchmark-ledger schema fields are necessary for the first executable protocol draft?
