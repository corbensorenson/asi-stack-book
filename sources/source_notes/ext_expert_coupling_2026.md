# Expert Coupling in MoE Pretraining: Reducing All-to-All Overhead with Correlated Placement and Token Shuffling

| Field | Value |
|---|---|
| Source ID | `ext_expert_coupling_2026` |

Radha Gulhane, Quentin Anthony, Beren Millidge. [Primary paper, arXiv 2610.09372v1](https://arxiv.org/html/2610.09372v1).

## Thesis

Expert placement and dispatch can exploit repeated co-selection without changing routing weights.

## Mechanisms

Co-locate frequently co-selected experts and send a token once to each device that hosts its selected experts.

## Evidence

Reported communication speedups reached 2.63× and whole-step speedup reached 1.41× on the tested MI300X cluster.

## Failure Modes

Megatron-LM placement and dispatch experiments. The study used one 12-layer model, top-2 and top-6 routing and 2.1B training tokens. Gains depend on traffic, layout and load.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling` — [Place four experts on two devices](../../chapters/governed-model-training-distributed-optimization-and-scaling.qmd#place-four-experts-on-two-devices)

## Claims To Add Or Update

Attribute all-to-all savings separately from training-step savings when evaluating expert placement.

## Open Questions

How often must experts move once the routing distribution changes?
