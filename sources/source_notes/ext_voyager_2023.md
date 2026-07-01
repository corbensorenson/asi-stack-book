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
| Ingestion basis | Primary arXiv metadata and abstract inspected for the procedural-memory, routing, and benchmark-ratchet comparator queue; paper, codebase, prompts, Minecraft environment, skill library, and evaluations are not imported into this repository. |

## Thesis

Voyager belongs in the procedural-memory comparison set as an external reference for an agent that grows an executable-code skill library through open-ended embodied interaction. It helps ground the ASI Stack's "procedure foundry" language against a concrete adjacent pattern: curriculum, skill library, environment feedback, execution errors, and self-verification.

## Mechanisms

- Use an automatic curriculum to drive exploration.
- Store and retrieve complex behaviors in an ever-growing executable-code skill library.
- Incorporate environment feedback, execution errors, and self-verification into iterative program improvement.
- Transfer the learned skill library to a new Minecraft world in the source setting.

## Evidence

- The source reports Minecraft results including broader item discovery, travel, tech-tree progress, and skill-library transfer in its own setup.
- This repository has not run Voyager, imported its code or prompts, reproduced Minecraft tasks, validated its skill library, or compared ASI Stack procedural memory against Voyager.
- Use this source for skill-library and lifelong-learning vocabulary, not as evidence that the ASI Stack has deployed loop closure or learned tools.

## Failure Modes

- Open-ended skill accumulation can hide stale, overbroad, or unsafe procedures if skill cards lack regression floors and retirement triggers.
- Executable-code skills can become ambient authority unless runtime adapters and routing leases bound when they may run.
- Environment-specific successes can be overgeneralized if negative examples and transfer failures are not preserved.

## Book Chapters Supported

- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use Voyager to compare the ASI Stack procedure-foundry target against external skill-library and embodied lifelong-learning work.
- Keep support at `argument` unless local trace mining, tool synthesis, regression checks, routing receipts, or accepted evidence transitions exist.
- Do not claim local Voyager reproduction, Minecraft performance, skill-library transfer, autonomous discovery, model-quality improvement, or deployed procedural memory.

## Open Questions

- Which artifact graph record should preserve a generated skill's source traces, code revisions, execution errors, and self-verification attempts?
- What readiness gate should decide when a skill library entry becomes routable outside the environment where it was learned?
- How should benchmark ratchets distinguish genuine skill transfer from overfitting to one environment's affordances?
