# MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models

| Field | Value |
|---|---|
| Source ID | `ext_mirabench_2026` |

Tianzhuo Yang, Zihan Shen, Zirui Mi, Zhaoyi Zhang, Jiayi Zhou, Jiaming Ji, Juntao Dai, Jiawei Chen, Boyuan Chen, Yaodong Yang. [Primary paper, arXiv 2605.29360v1](https://arxiv.org/html/2605.29360v1).

## Thesis

Action-conditioned prediction can look physically plausible even when it ignores the command or a failure.

## Mechanisms

Pair predictions from the same initial scene under different commands, including an action expected to fail.

## Evidence

Twelve model configurations and over 16,000 human judgments informed tests of physical consistency, command fidelity and optimism under failure-inducing actions.

## Failure Modes

Action-following and optimism perturbation tests. Predicted episodes can expose errors in the simulator. Physical control needs separate closed-loop evidence.

## Book Chapters Supported

- `governed-world-models-and-reality-grounding` — [Change the command in the same scene](https://corbensorenson.github.io/asi-stack-book/chapters/governed-world-models-and-reality-grounding.html#change-the-command-in-the-same-scene)

## Claims To Add Or Update

Test failure-inducing commands before handing a learned world model a planning role.

## Open Questions

Does a simulator that anticipates failure also improve decisions on an observed physical trajectory?
