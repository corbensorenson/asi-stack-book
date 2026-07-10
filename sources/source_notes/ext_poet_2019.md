# Source Note: Paired Open-Ended Trailblazer

| Field | Value |
|---|---|
| Source ID | `ext_poet_2019` |
| Source title | Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions |
| Ingestion date | 2026-07-10 |
| Source version / URL | arXiv:1901.01753v3, https://arxiv.org/abs/1901.01753 |
| Citation label | Wang et al. (2019), Paired Open-Ended Trailblazer |
| Published / updated | 2019-01-07 / 2019-02-21 |
| DOI | 10.48550/arXiv.1901.01753 |
| Ingestion basis | Primary arXiv paper inspected for paired environment generation, agent optimization, cross-environment transfer, experimental controls, and scope limits. No environment, agent, transfer process, or result was reproduced in this repository. |

## Thesis

POET is a specified open-ended reinforcement-learning procedure that couples
the generation of new environments with optimization of agents that solve
them. It maintains multiple environment-agent pairings and permits solutions
to transfer between environments when they perform better, rather than treating
one fixed task distribution as the entire curriculum.

## Mechanisms

- Generate child environments from eligible parent environments under a
  configured representation and mutation process.
- Optimize an agent for each retained environment and keep multiple
  environment-solution pairings active.
- Evaluate candidate transfers from other environments and replace a local
  solution when the transferred solution performs better in the target
  environment.
- Apply the paper's task-specific eligibility and capacity controls rather than
  assuming every generated environment is useful or solvable.

## Evidence

- The primary paper reports results in its specified BipedalWalker-derived
  environment family and compares POET with named control procedures in that
  setting.
- Its results concern the paper's encoded environments, optimization method,
  transfer procedure, seeds, and evaluation protocol. They do not demonstrate
  general open-ended intelligence, safe self-improvement, or a universally
  valid curriculum.
- This repository has not generated environments, optimized agents, replayed
  transfer, or tested POET's controls. The source is a mechanism comparator for
  a governed improvement-engine design, not local evidence.

## Failure Modes

- A generated-task distribution can optimize novelty or difficulty proxies
  while losing the intended task, safety, or resource boundary.
- Cross-task transfer can carry stale, unsafe, or overprivileged procedures
  into a new context without independent qualification.
- A population archive can conceal selection bias, evaluator capture, or
  unowned failed candidates if rejected routes and residuals are discarded.

## Book Chapters Supported

- `open-ended-improvement-engines` (Open-Ended Improvement Engines)

## Claims To Add Or Update

- Use POET as a comparator for the paired generator-and-solver pattern, not as
  evidence that an ASI Stack system can improve indefinitely or safely.
- Require generated-task provenance, admission criteria, independent
  evaluation, authority boundaries, residual retention, and rollback before a
  candidate artifact becomes routable or promotable.
- Do not claim local POET reproduction, cross-domain transfer, environment
  generation quality, capability growth, safety, or ASI.

## Open Questions

- What public-safe record can separate a task-generator novelty score from a
  justified improvement objective?
- How should a transfer candidate preserve provenance, permissions, failed
  evaluations, and a rollback path across task contexts?
- Which independent evaluator can test an improvement engine without becoming
  a training-time optimization target?
