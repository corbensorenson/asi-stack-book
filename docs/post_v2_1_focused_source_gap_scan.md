# Post-v2.1 Focused Primary-Source Gap Scan

Recorded: 2026-07-11

State: completed before final preregistration and before outcome visibility

This scan tested whether the P1–P3 designs omitted modern comparison points
that would invalidate an endpoint, control, or interpretation. It used primary
paper/proceedings records and retained older sources only when they define a
necessary systems boundary. No source result is treated as a local result.

## P1 — governed usefulness and rollback

| Source | What it adds | Design disposition |
|---|---|---|
| [AgentDojo](https://arxiv.org/abs/2406.13352) | Joint realistic-task/security evaluation over untrusted tool data and adaptive attacks | Already covered by separate usefulness/security endpoints, taint, attack families, and no model-as-evaluator boundary; no endpoint change |
| [Claw-SWE-Bench](https://arxiv.org/abs/2606.12344) | Fixed harness/workspace/patch/evaluator/budget contracts and explicit harness-versus-model cost effects | Reinforces matched model/tool surfaces and governance-cost reporting; current preprint results are not imported |
| [TxFS](https://www.usenix.org/conference/atc18/presentation/hu) | ACID transaction, isolation, durability, crash-consistency, and journal-capacity boundaries | Adds a non-claim: P1 snapshot restoration is not a transactional-filesystem or crash-safety result |

P1 remains interpretable as a finite local transaction study. The scan forbids
using exact directory restoration to claim filesystem ACID, crash recovery, or
general coding-agent capability.

## P2 — ambiguous routing and deliberation

| Source | What it adds | Design disposition |
|---|---|---|
| [RouteLLM](https://arxiv.org/abs/2406.18665) | Cost-quality routing, router overhead, and severe OOD sensitivity | Already covered by cost, route regret, held-out ambiguity, and family/band slices; interpretation must foreground the synthetic distribution |
| [Compute-optimal test-time scaling](https://arxiv.org/abs/2408.03314) | Difficulty-dependent allocation, verifier search, proposal revision, matched compute, and search failure regimes | Existing adaptive/fixed/overcompute/verifier-disabled arms and corruption endpoint remain appropriate |
| [Don't Hallucinate, Abstain](https://aclanthology.org/2024.acl-long.786/) | Knowledge-gap abstention and limits of self-reflection/held-out calibration | Reinforces coverage-risk and clarification/abstention separation; model agreement remains non-independent |

P2 therefore retains its endpoints. It must report router overhead, fallback and
abstention coverage, initially-correct corruption, evaluator disagreement, and
OOD/family slices together; no accuracy-only conclusion is permitted.

## P3 — update and unlearning causality

| Source | What it adds | Design disposition |
|---|---|---|
| [MUSE](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4556f5398bd2c61bd7500e306b4e560a-Abstract-Conference.html) | Six-way separation of memorization, privacy, utility, scale, and sequential sustainability | Reinforces the four preregistered claim partitions and adds explicit non-transfer to 7B LMs |
| [Weak-measures position paper](https://arxiv.org/abs/2410.02879) | Benign perturbations, forget/retain dependencies, target ambiguity, and query overfitting | Requires mutation-sensitive interpretation and blocks favorable benchmark-score language |
| [OpenUnlearning](https://proceedings.neurips.cc/paper_files/paper/2025/hash/3e4a38f228427ab819ba7899003a44b1-Abstract-Datasets_and_Benchmarks_Track.html) | Unified method/metric execution and meta-evaluation of metric faithfulness | Makes evaluator/metric validity an explicit residual; does not expand the frozen arm set |

P3 remains a small causal state-management experiment. Behavioral cohort
change, influence/privacy evidence, lineage propagation, and storage erasure
remain separate. The immutable public-safe source corpus makes storage erasure
false by construction, and no legal or privacy compliance inference is allowed.

## Corpus and endpoint decision

The scan found no source that requires changing the already amended counts,
splits, arms, budgets, primary endpoints, thresholds, or stop rules. It did
strengthen interpretation boundaries and the later chapter-integration queue.
Six source records and six full source notes were added with chapter targets;
AgentDojo, RouteLLM, and compute-optimal test-time scaling were already present
and were re-audited rather than duplicated. All nine selected sources appear in the generated
external-source appendix and can enter chapter prose only through the M4
claim/evidence reconciliation.

## Non-claims

- Literature coverage is focused, not exhaustive or systematic-review evidence.
- Source publication does not establish local reproduction or transfer.
- A current preprint is a comparison point, not settled evidence.
- The scan does not execute a model, open an outcome, close a residual, or move
  a support state.
