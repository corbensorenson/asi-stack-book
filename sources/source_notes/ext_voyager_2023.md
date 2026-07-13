# Source Note: Voyager: An Open-Ended Embodied Agent with Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_voyager_2023` |
| Source title | Voyager: An Open-Ended Embodied Agent with Large Language Models |
| Ingestion date | 2026-07-01 |
| Source version / URL | arXiv:2305.16291, https://arxiv.org/abs/2305.16291 |
| Citation label | Wang et al. (2023), Voyager |
| Published / updated | 2023-05-25 / 2023-10-19 |
| DOI | 10.48550/arXiv.2305.16291 |
| Ingestion basis | Full primary arXiv paper reviewed for automatic-curriculum inputs, code skill-library storage and retrieval, iterative execution feedback, self-verification, stop behavior, baselines, ablations, transfer tests, costs, inaccuracies, and hallucination limits. The codebase, prompts, Minecraft environment, model calls, skill library, and evaluations are not imported or reproduced. |

## Thesis

Voyager belongs in the procedural-memory comparison set as an external reference for an agent that grows an executable-code skill library through open-ended embodied interaction. It helps ground the ASI Stack's "procedure foundry" language against a concrete adjacent pattern: curriculum, skill library, environment feedback, execution errors, and self-verification.

## Mechanisms

- Use an automatic curriculum to drive exploration.
- Store and retrieve complex behaviors in an ever-growing executable-code skill library.
- Incorporate environment feedback, execution errors, and self-verification into iterative program improvement.
- Transfer the learned skill library to a new Minecraft world in the source setting.
- Condition curriculum generation on current agent state plus completed and
  failed tasks; abandon a task after the reported bounded refinement attempts.
- Retrieve top related skills through description embeddings and compose them
  into new executable programs under a high-level control API.

## Evidence

- The source reports Minecraft results including broader item discovery, travel, tech-tree progress, and skill-library transfer in its own setup.
- The paper compares adapted ReAct, Reflexion, and AutoGPT baselines in
  MineDojo, reports three-trial tech-tree and new-world task results, and
  separately ablates curriculum, library, execution feedback, errors,
  self-verification, and model choice.
- The action interface uses Mineflayer's high-level APIs and text state rather
  than raw 3D perception or low-level sensorimotor control; the comparison is
  bounded to that abstraction.
- This repository has not run Voyager, imported its code or prompts, reproduced Minecraft tasks, validated its skill library, or compared ASI Stack procedural memory against Voyager.
- Use this source for skill-library and lifelong-learning vocabulary, not as evidence that the ASI Stack has deployed loop closure or learned tools.

## Failure Modes

- Open-ended skill accumulation can hide stale, overbroad, or unsafe procedures if skill cards lack regression floors and retirement triggers.
- Executable-code skills can become ambient authority unless runtime adapters and routing leases bound when they may run.
- Environment-specific successes can be overgeneralized if negative examples and transfer failures are not preserved.
- The same model family helps generate tasks, code, and success judgments, so
  self-verification is useful feedback rather than independent qualification.
- The paper reports expensive model dependence, stuck tasks, hallucinated
  impossible items or APIs, and occasional self-verification failures.

## Book Chapters Supported

- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `open-ended-improvement-engines` (Open-Ended Improvement Engines)

## Claims To Add Or Update

- Use Voyager to compare the ASI Stack procedure-foundry target against external skill-library and embodied lifelong-learning work.
- Keep support at `argument` unless local trace mining, tool synthesis, regression checks, routing receipts, or accepted evidence transitions exist.
- Use Voyager as a scoped comparator for curriculum, skill-library, and iterative-improvement interfaces; do not treat its self-verification as independent evaluation of a governed improvement engine.
- Do not claim local Voyager reproduction, Minecraft performance, skill-library transfer, autonomous discovery, model-quality improvement, or deployed procedural memory.

## Open Questions

- Which artifact graph record should preserve a generated skill's source traces, code revisions, execution errors, and self-verification attempts?
- What readiness gate should decide when a skill library entry becomes routable outside the environment where it was learned?
- How should benchmark ratchets distinguish genuine skill transfer from overfitting to one environment's affordances?
