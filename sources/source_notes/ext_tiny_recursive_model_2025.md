# Source Note: Tiny Recursive Model

| Field | Value |
|---|---|
| Source ID | `ext_tiny_recursive_model_2025` |
| Source title | Less is More: Recursive Reasoning with Tiny Networks |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2510.04871v1, https://arxiv.org/abs/2510.04871 |
| Ingestion basis | Primary preprint abstract and architecture/evaluation descriptions reviewed; no checkpoint or benchmark reproduced. |

## Thesis

A two-layer, weight-tied Tiny Recursive Model can iteratively refine latent
reasoning and output states and reports strong results on narrow structured
puzzle tasks with far fewer parameters than large language-model comparators.

## Mechanisms

- One small network reused across recursive refinement steps.
- Separate latent reasoning state and predicted-output state.
- Test-time sampling and aggregation in the reported evaluation pipeline.

## Evidence

The source reports Sudoku, Maze, and ARC-AGI results. The repository has not
reproduced its data pipeline, checkpoint, augmentation, sampling, voting,
latency, memory, or transfer behavior.

## Failure Modes

- Parameter count can hide augmentation, sampling, voting, and task-specific encoding.
- Puzzle success can be mistaken for language, world-model, or general-agent capability.
- Nominal recursion depth can exceed effective useful computation depth.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Treat tiny weight-tied recursion as a tournament lane, not as proof of OneCell.
- Preregister task-identity, augmentation, sampling, vote, recursion-depth, and total-cost ablations.

## Open Questions

- Does useful recursive refinement transfer beyond task-specific puzzle representations?
- Can a fixed tiny core improve without answer-bearing adapters or growing hidden compute?
