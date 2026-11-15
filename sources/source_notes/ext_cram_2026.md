# Source Note: Classical Energies Learn to Reason 1,000× Faster than Looped Models

| Field | Value |
|---|---|
| Source ID | `ext_cram_2026` |
| Authors | Benjamin Hoover, Hugh Blayney, and James C. R. Whittington |
| Primary source | [arXiv:2611.17309v1](https://arxiv.org/html/2611.17309v1), November 12, 2026 |
| Ingestion date | 2026-11-14 |
| Review scope | §§3–5, Figures 2–4, Tables 1–3, and Appendices C, D, E and F as relevant to the chapter passages. Selected release records were read at commit `62bbe830c7d6f87f2ba18f30a28039258b986454`. |

## Mechanism

Compact Reasoning Associative Memory (CRAM) uses a Hopfield–Tank energy with costs for cell values and pairs of values. Pseudolikelihood fits the costs by comparing each correct value with substitutions while the rest of the solution stays fixed. Sudoku uses full pair tables, digit relabeling, and sparsity regularization. Inference clamps clues and searches in four chains with stochastic single-cell moves. Maze-Unique ties costs within a local window, fixes walls and endpoints, and starts from all open cells so that moves prune dead ends.

## Reported evidence and accounting

- Table 2 and §4.1 report 99.996% on 412,786 held-out Sudoku-Extreme puzzles and 100% on 1,000 Maze-Unique mazes, averaged over three training seeds. The release guide gives Sudoku solve counts of 412,768, 412,770, and 412,769. The authors report zero wrong threshold stops and 51 budget exhaustions across those three Sudoku evaluations.
- The preprint's 42 ms and 132 ms H200 fit times use a warmed process. The looped-model fits use a cold process. Appendix C.2 describes the timing boundary, including threshold fitting and exclusions such as evaluation, file reads, saving, and CUDA context startup. The released aggregate cold H200 fit fields are about 0.59 s and 0.72 s. Several baseline accuracies in Table 2 come from the original publications where the authors' reruns scored lower.
- Figure 2's 282× ratio compares counted inference arithmetic at matched Sudoku accuracy against the lowest-work tested looped baseline at its highest-accuracy setting, EBR. Counts include all chains and failed searches. The accounting assigns zero FLOPs to comparisons, indexing, data movement, and random draws, so a deployment would still measure elapsed latency.
- Hand-set costs with the same search solve every test Sudoku and unique-path maze. Table 3 evaluates N-Queens and graph coloring separately, with a diversity measure as well as correctness. On ten-vertex graph coloring EBR has higher reported coverage than learned CRAM. Appendix C records post-test reporting choices for the N-Queens recipe.

## Failure modes and scope

The energy, initialization, update rule, and stopping policy jointly define the solver. On Maze-Unique development instances, the empty board has lower energy than the solution. Global minimization of that learned score alone would favor an invalid answer. In Sudoku, scant training data yields incorrect solutions in the authors' low-data experiment. Appendix E's non-increasing energy result is for the fixed-parameter, fixed-temperature deterministic continuous dynamics. The stochastic, finite-budget searches require separate empirical checks.

Appendix F uses a distinct 29-parameter Maze-Hard variant with a designed distance-like latent field and learned directional preferences. It matches 999 of 1,000 labeled paths in each run. The labels select one shortest path using a fixed neighbor order. All three fits accept the same incorrect board with a six-cell dead end. Check path validity and shortest path length independently of the model's stopping test, and report canonical path agreement separately when the output contract requires it.

For deployment comparison, separate the learned specialist, the hand-set energy with its search, and a rule-aware solver such as breadth-first search for unit-cost maze edges. The last is a proposed control. CRAM's reported comparison is against self-contained recurrent reasoners and its own hand-set variant.

## Book chapters supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- Reader Unit 19 uses the reported maze failure as an example of checking a specialist's answer.

## Released documentation and timing records

- [Reproduction guide](https://github.com/Prefrontal-AI/CRAM/blob/62bbe830c7d6f87f2ba18f30a28039258b986454/REPRODUCING.md)
- [Sudoku-Extreme fit record](https://github.com/Prefrontal-AI/CRAM/blob/62bbe830c7d6f87f2ba18f30a28039258b986454/experiments/runs/table/sudoku-extreme__cram-0-fit.json)
- [Maze-Unique fit record](https://github.com/Prefrontal-AI/CRAM/blob/62bbe830c7d6f87f2ba18f30a28039258b986454/experiments/runs/table/maze-unique__cram-sgd-fg.json)
