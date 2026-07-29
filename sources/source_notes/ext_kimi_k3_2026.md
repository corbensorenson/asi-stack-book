# Source Note: Kimi K3 — Open Frontier Intelligence

| Field | Value |
|---|---|
| Source ID | `ext_kimi_k3_2026` |
| Ingestion date | 2026-07-28 |
| Source | Kimi Team, arXiv:2607.24653, https://arxiv.org/abs/2607.24653; official architecture summary, https://github.com/MoonshotAI/Kimi-K3 |
| Ingestion basis | Primary technical report and official architecture table reviewed for KDA, Gated MLA, Attention Residuals, Stable LatentMoE, Quantile Balancing, SiTU-GLU, Per-Head Muon, context, sparsity, and quantization. Code, weights, training data, checkpoints, and evaluations were not reproduced. |

## Thesis

Kimi K3 is a source-reported 2.8-trillion-total-parameter, 104-billion-active
Mixture-of-Experts system whose architecture combines Kimi Delta Attention
(KDA), Gated Multi-head Latent Attention, Attention Residuals (AttnRes), Stable
LatentMoE, and a smooth bounded SiTU-GLU activation. The report attributes an
approximately 2.5-fold scaling-efficiency improvement over Kimi K2 to the
combined architecture, data, training, and systems stack. That aggregate result
does not identify the causal contribution of any one mechanism and is not local
evidence.

## Mechanisms

- KDA and Gated MLA form a 3:1 hybrid attention stack in the reported model,
  targeting long-context recurrent efficiency while retaining periodic global
  attention.
- AttnRes lets a layer selectively combine outputs from earlier layers or
  blocks instead of receiving only the immediately preceding residual stream.
- Stable LatentMoE routes a lower-dimensional expert branch while retaining
  full-width shared experts. Quantile Balancing uses expert-score quantiles to
  control load without the conventional auxiliary balancing loss.
- SiTU-GLU smooths and bounds the SwiGLU pathway to improve source-reported
  numerical stability at extreme scale.
- Per-Head Muon partitions eligible attention projection matrices by head
  before Newton--Schulz orthogonalization, rather than treating the complete
  projection as one matrix.
- Quantization-aware post-training uses MXFP4 weights and MXFP8 activations in
  the reported deployment stack.

## Evidence And Limits

The official report supplies one integrated frontier-scale system and its
provider-run evaluations. It does not provide a matched public ablation that
isolates every mechanism at small scale, on Apple MLX, at 512-token context, or
in a 57M-parameter dense/shared-trunk regime. Its million-token and 896-expert
choices are therefore not direct prescriptions for Project Theseus.

The source-reported scaling-efficiency gain is configuration-bound. It cannot
be used as evidence that KDA, AttnRes, Stable LatentMoE, Quantile Balancing,
SiTU-GLU, Per-Head Muon, or quantization will improve another model unless a
matched local experiment attributes that result.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`: hybrid
  recurrent/global attention and cross-layer residual routing as current
  substrate candidates.
- `routing-heads-and-specialist-cores`: low-dimensional expert routing,
  full-width shared experts, and score-quantile load balancing.
- `governed-model-training-distributed-optimization-and-scaling`: Per-Head
  Muon, numerical-stability mechanisms, and algorithm/system co-design.

No new chapter is warranted. The source strengthens existing boundaries.

## Project Theseus Triage

- **Bounded immediate candidate:** compare Per-Head Muon with the existing
  correctly scaled full-matrix Muon and AdamW on the existing source-disjoint
  midscale optimizer rung. Require equal data, positions, tuning opportunity,
  checkpoint state, total wall time, and weak-arm rules. The old full-matrix
  Muon loss is not evidence against the per-head variant.
- **Prospective topology candidates:** AttnRes and SiTU-GLU may receive small
  matched learnability, stability, and time-to-quality canaries in isolated
  successor lineages. Adoption would invalidate current checkpoint
  compatibility and therefore needs a material win before restarting the
  campaign.
- **Scope-deferred for campaign one:** KDA/Gated-MLA hybrid attention is aimed
  at context lengths far beyond Theseus's fixed 512-token maximum; Stable
  LatentMoE and Quantile Balancing assume a many-expert learned router that the
  current independently trained arm design does not have; MXFP4/MXFP8 lacks a
  qualified M1 MLX training route. These are explicit incompatibility
  dispositions, not scientific falsifications.
- **Already corroborated:** the K3 report's cosine-schedule choice agrees with
  the existing Theseus cosine schedule and creates no new experiment by itself.

## Failure Modes

- **Component-attribution failure:** treating the reported integrated
  approximately 2.5-fold scaling-efficiency result as evidence for any one of
  KDA, AttnRes, LatentMoE, Quantile Balancing, SiTU-GLU, Per-Head Muon, or
  quantization.
- **Transfer failure:** assuming a mechanism demonstrated inside a 2.8T-total,
  104B-active, million-token, 896-expert system will retain its benefit in a
  57M-class, 512-token, Apple-MLX training regime.
- **Accounting failure:** comparing quality or asymptotic compute while
  omitting routing, memory traffic, expert balancing, persistent state,
  checkpoint expansion, quantization conversion, wall time, or recovery cost.
- **Benchmark-authority failure:** treating provider-run evaluations as an
  independent reproduction, a safety result, or permission to admit benchmark
  content into Theseus training.
- **Compatibility laundering:** calling an incompatible campaign-one mechanism
  disproved, or adopting it without a separately qualified successor topology
  and prospective decision rule.

## Claims To Add Or Update

- In `replaceable-cognitive-substrates-beyond-transformer-monoculture`, record
  KDA/Gated-MLA hybrid attention and AttnRes as current source-reported
  substrate patterns whose system-level value remains configuration-bound.
- In `routing-heads-and-specialist-cores`, add Stable LatentMoE and Quantile
  Balancing as examples of lower-dimensional expert routing and balancing
  mechanisms that still require matched load, quality, and total-cost tests.
- In `governed-model-training-distributed-optimization-and-scaling`, add
  Per-Head Muon and SiTU-GLU as bounded optimizer and numerical-stability
  candidates, with equal-tuning and full-state comparison requirements.
- Preserve `argument` support for all three chapter cores. These updates route
  a current primary source; they do not establish superiority, transfer,
  reproduction, safety, or a Project Theseus selection.

## Open Questions

- Does Per-Head Muon change the time-to-quality or weak-arm behavior of the
  existing small Theseus Muon implementation after its extra partitioning cost?
- Can block-level AttnRes improve a 57M-class model enough to repay additional
  state, bandwidth, and checkpoint complexity on unified-memory Apple silicon?
- Does SiTU-GLU improve finite-precision stability where Theseus currently has
  no observed activation-instability wall?
- At what context length would a faithful KDA implementation outrun MLX
  attention on this host after kernel, state, and replay costs are included?

## Non-Claims

- No Kimi K3 result has been independently reproduced.
- No Kimi K3 benchmark is admitted as Theseus training data or capability
  evidence.
- No K3 mechanism is selected for Theseus by this source review.
- No source-reported gain transfers across scale, data, hardware, optimizer, or
  context without a matched local result.
