# Expert Coupling in MoE Pretraining: Reducing All-to-All Overhead with Correlated Placement and Token Shuffling

Radha Gulhane, Quentin Anthony, Beren Millidge. [Primary paper, arXiv 2610.09372v1](https://arxiv.org/html/2610.09372v1).

## Mechanism and evidence

Co-locate frequently co-selected experts and send a token once to each device that hosts its selected experts.

Reported communication speedups reached 2.63× and whole-step speedup reached 1.41× on the tested MI300X cluster.

## Reviewed passage and limits

Megatron-LM placement and dispatch experiments. The study used one 12-layer model, top-2 and top-6 routing and 2.1B training tokens. Gains depend on traffic, layout and load.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
