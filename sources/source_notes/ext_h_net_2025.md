# Source Note: Dynamic Chunking for End-to-End Hierarchical Sequence Modeling

| Field | Value |
|---|---|
| Source ID | `ext_h_net_2025` |
| Ingestion date | 2026-11-02 |
| Primary version | [arXiv:2507.07955v2](https://arxiv.org/html/2507.07955v2) |
| Citation | Hwang, Wang and Gu (2025), H-Net |
| Published / updated | 2025-07-10 / 2025-07-15 |
| Review scope | Sections 2.1–2.4, 3.1 and 4, including dynamic-boundary equations, smoothing and efficiency limitations; arXiv v2. Official goombalab/hnet README inspected for implementation identity only; code/checkpoints not executed. |
| Custody | Public-safe authored note only; raw primary HTML remains in ignored local research cache. |

## Thesis
H-Net learns context-dependent byte-sequence boundaries jointly with a hierarchical autoregressive model, replacing a fixed tokenizer in the reported language-modeling pipeline.

## Mechanisms
Sections 2.1–2.4 nest encoder/main/decoder stages. A router selects boundary vectors, deeper stages process the shorter stream, and smoothing, upsampling and residual paths return to byte resolution. A ratio loss controls chunking pressure. The blocks can use state-space models or attention; H-Net is a global hierarchy, not one replacement mixing layer.

## Evidence
Section 3 reports data/FLOP-matched language-modeling and downstream comparisons, including one- and two-stage variants. This review ran no model or generation benchmark.

## Failure Modes
Section 4 reports implementation-dependent training slowdown up to roughly twice an isotropic model and variable-length memory/batching difficulties. It leaves deeper hierarchies and broad long-context implications open. Learned chunks are not certified concepts, exact compressed artifacts or semantic IR. This remains autoregressive byte prediction, unlike JEPA's representation objective.

## Claims To Add Or Update
Qualify boundary/dechunking state, byte offsets, checkpoint identity and realized cost through the existing Cognitive Kernel ABI. Treat a JEPA/H-Net combination as an untested design possibility, not a reported model.

## Open Questions
When do learned granularity gains survive exact-string tasks, wall-time/tail cost, migration and long-context evaluation?

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Chapter Decision

Update existing owners through `new_paper_triage_scenarios/jepa_platonic_and_hnet_2026_11_02.json`. No new chapter, no claim-core promotion, no local model result.
