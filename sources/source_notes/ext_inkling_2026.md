# Source Note: Inkling

| Field | Value |
|---|---|
| Source ID | `ext_inkling_2026` |
| Source title | Inkling: Our open-weights model |
| Ingestion date | 2026-07-15 |
| Source version / URL | Official release, https://thinkingmachines.ai/news/introducing-inkling/; official model card, https://thinkingmachines.ai/model-card/inkling/; official weight/config record, https://huggingface.co/thinkingmachines/Inkling |
| Ingestion basis | Primary release article, primary model card, and released Hugging Face configuration reviewed on release day; no weight download, inference, training, benchmark reproduction, or architecture ablation. |

## Thesis

Inkling is a useful current case of architecture *composition*: a 66-layer,
decoder-only, multimodal Transformer combines sparse mixture-of-experts feed-
forward layers, interleaved local and global attention, relative positional
features, short convolutions, modality-specific encoders, and controllable
reasoning effort. It therefore strengthens the book's requirement to describe a
kernel by its complete topology and lifecycle rather than by one label such as
“Transformer,” “sliding window,” or “MoE.”

## Mechanisms

- Sparse MoE feed-forward backbone with 256 routed experts, two shared experts,
  and six routed experts active per token; the official release describes a
  sigmoid router with auxiliary-loss-free balancing and joint normalization of
  routed and shared expert scores.
- Five local-attention layers for each global-attention layer. The released
  configuration records a 512-token sliding window, 64 query heads, eight global
  KV heads, and sixteen local KV heads.
- Relative positional embeddings rather than RoPE, plus kernel-size-four short
  convolutions after key/value projections and on attention/MLP residual-branch
  outputs.
- Shared decoder space for text, image/video patches, and discretized audio;
  the released configuration records a four-layer hierarchical vision encoder
  with 40-pixel patches and dMel audio encoding.
- Controllable inference effort learned during large-scale asynchronous RL by
  varying system instructions and per-token cost. This is a model capability,
  not by itself a governed budget, stopping, verification, or release policy.
- Open BF16 and NVFP4 weights. The model card reports at least 2 TB aggregate
  VRAM for BF16 and at least 600 GB for NVFP4, making hardware access part of
  any honest reproduction decision.

## Evidence

- The provider reports 975B total parameters, 41B active parameters, a maximum
  context of 1,048,576 tokens, pretraining on 45 trillion multimodal tokens, and
  more than 30 million RL rollouts.
- The provider reports broad reasoning, coding, agentic, factuality, vision,
  audio, and safety benchmark results at effort `0.99`. Several comparisons use
  external scores, while some use internal harnesses; the release discloses
  contamination handling and output-format sensitivity for selected tests.
- The provider reports that Inkling-Small has 276B total and 12B active
  parameters and shares the scalable post-training stack, but its weights were
  not released at the review boundary.
- No local ASI Stack run has loaded Inkling, reproduced a score, measured its
  context behavior, isolated local/global attention, isolated short
  convolutions or relative positions, tested its expert router, or evaluated
  its safety after fine-tuning.

## Failure Modes

- **Component-credit laundering:** benchmark quality is credited to sliding
  attention, MoE routing, relative positions, convolutions, multimodal data, RL,
  or scale without a causal ablation.
- **Context-window laundering:** a configured maximum is treated as verified
  useful recall, reasoning, latency, or safety across the full window.
- **Active-parameter laundering:** 41B active parameters hide 975B stored
  parameters, expert routing, memory traffic, deployment hardware, and total
  lifecycle cost.
- **Effort laundering:** the provider's `effort=0.99` benchmark point is treated
  as an efficient frontier without measuring the complete effort–quality–cost
  curve and initially-correct corruption.
- **Router conflation:** token-level expert routing inside one model is confused
  with stack-level selection among separately qualified kernels, tools, human
  lanes, and authority envelopes.
- **Open-weight accessibility laundering:** downloadable weights are treated as
  reproducible or broadly deployable despite the reported 600 GB to 2 TB VRAM
  requirements.
- **Safety persistence assumption:** base-model refusal results are assumed to
  survive arbitrary customization even though the provider explicitly treats
  fine-tuning safety as an ongoing study and recommends defense in depth.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture` — primary
  owner for the hybrid-topology case, Cognitive Kernel capability-card fields,
  and matched architecture/component ablations.
- `routing-heads-and-specialist-cores` — distinguish token-to-expert routing
  from task-to-kernel routing and account for both when they are nested.
- `governed-deliberation-and-test-time-scaling` — treat controllable model effort
  as an offered actuator whose budget, stopping, verification, corruption, and
  downstream authority still require external governance.
- `resource-economics-and-token-budgets` — require total/active parameters,
  local/global attention mix, context used, numerics, hardware, memory, and
  complete effort curves rather than one benchmark operating point.
- `safety-cases-and-structured-assurance` — preserve the model card's
  defense-in-depth and post-customization residual boundary without promoting
  provider-reported tests to a local safety case.

## Claims To Add Or Update

- A cognitive-kernel capability card should name attention topology, local
  window, global cadence, positional mechanism, convolutional mixing, expert
  topology, active and total parameters, modality encoders, mutable state,
  context configured/served/tested, numerics, hardware envelope, and effort
  control.
- Hybrid architectures require component and interaction ablations; a model-
  level score cannot identify which component supplied the gain.
- Internal expert routing and external stack routing are complementary but must
  retain separate candidate sets, costs, failure states, and authority.
- Controllable reasoning effort becomes useful to the stack only through a
  prospectively calibrated route and stopping policy over complete useful,
  unsafe, refusal, latency, and cost denominators.
- If official hardware requirements make direct reproduction infeasible, the
  comparator ledger must record a blocker. A smaller mechanism-matched proxy is
  informative but is not an Inkling reproduction.

## Open Questions

- What fraction of long-context quality is causally attributable to the 5:1
  local/global schedule, relative positions, short convolutions, training data,
  post-training, or scale?
- Does the 512-token local window plus periodic global layers preserve useful
  retrieval and reasoning under distractors across the advertised context?
- How do expert load, KV memory, communication, and tail latency change across
  modalities, context lengths, effort levels, numerics, and hardware?
- Does effort control remain calibrated under distribution shift, tool use,
  fine-tuning, and initially-correct cases?
- Which safety properties survive downstream fine-tuning, and which must be
  re-established by external policy, monitoring, and release gates?
