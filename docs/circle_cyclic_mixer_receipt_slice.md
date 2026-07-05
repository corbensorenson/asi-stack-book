# Circle Cyclic-Mixer Receipt Slice

Date: 2026-07-05

This record imports one public-safe Circle Calculus cyclic-mixer receipt slice
for the CoilRA, MultiCoil RoPE, and Cyclic Mixers chapter. It is structural
contract evidence only: a deterministic circulant dense-reference parity
fixture, block-cyclic parameter-accounting fields, theorem IDs, receipt
fingerprints, command-output digests, planner recommendations, and non-claim
boundaries.

Tracked result:
`experiments/circle_cyclic_mixer_receipt_slice/results/2026-07-05-local.json`

Validator:
`python3 scripts/validate_circle_cyclic_mixer_receipt_slice.py`

No-promotion decision:
`evidence_transitions/v1_x_measured/circle_cyclic_mixer_receipt_no_change.json`

## Scope

External project: Circle Calculus at commit `63b0f511`.

Accepted contract ID: `CC-AI-CONTRACT-MIXER-001`

Contract kind: `circulant_block_cyclic_mixer`

Receipt schema: `circle_calculus.ai_contract_acceptance_receipt.v0`

Pack fingerprint:
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`

Contract fingerprint:
`b3e3e0cf420d9e8e79a28a55ef8322f9a214c8d5a957dd8b06e5e5373c684ea5`

Required theorem IDs:

- `AIT-T0006`
- `AIT-T0007`
- `AIT-T0008`
- `AIT-T0009`
- `AIRA-T0001`
- `AIRA-T0002`
- `AIRA-T0004`

The digest and receipt commands record `theorem_count=7` for the
contract-ready cyclic-mixer entry.

Required recommendation IDs:

- `MIXER-AUDIT-CIRCULANT-DENSE-PARITY`
- `MIXER-AUDIT-BLOCK-CYCLIC-PARAMETER-BUDGET`

## Observed Fixture Facts

The accepted fixture records:

- `period=8`
- `input_values=[-2, 2, 1, 2, -2, 3, 3, -2]`
- `kernel_values=[2, -1, 1, 0, -2, 0, 0, 0]`
- `circulant_output=[5, -2, -8, 9, -1, 6, -1, -8]`
- `dense_output=[5, -2, -8, 9, -1, 6, -1, -8]`
- `max_abs_dense_delta=0`
- `dense_parameters=64`
- `circulant_parameters=8`
- `circulant_parameter_ratio=0.125`
- `channel_count=128`
- `block_size=8`
- `block_loads=[16, 16, 16, 16, 16, 16, 16, 16]`
- `dense_adapter_parameters=2048`
- `lora_parameters=576`
- `block_cyclic_parameters=128`
- `block_to_dense_ratio=0.0625`

The planner recommendation `MIXER-AUDIT-CIRCULANT-DENSE-PARITY` audits exact
dense-reference parity for one deterministic circulant fixture. It cites
`AIT-T0006`, `AIT-T0007`, `AIT-T0008`, and `AIT-T0009`; the pinned evidence
field is `max_abs_dense_delta=0`.

The planner recommendation `MIXER-AUDIT-BLOCK-CYCLIC-PARAMETER-BUDGET`
records finite block-cyclic adapter parameter accounting for the declared
fixture. It cites `AIRA-T0001`, `AIRA-T0002`, and `AIRA-T0004`; the pinned
evidence field is `block_to_dense_ratio=0.0625`.

The Circle AI certifier boundary is deliberately narrow: the request passed as
a theorem-linked structural/accounting certificate for one deterministic
fixture. Its unsupported fields are accuracy improvement over dense layers,
training speed, hardware efficiency, and optimal mixer architecture.

The targeted Circle CLI test command reported `3 passed in 2.49s`. The
targeted contract-ready recommendation test reported `1 passed in 1.47s`.

## Command Output Digests

| Output | SHA-256 | Bytes |
|---|---:|---:|
| circulant/block-cyclic mixer certificate JSON | `32802064ce7f2207f2e13b1b28acb75c6f80c900c334d092f5113f0173fc5ae4` | 7224 |
| Circle AI cyclic-mixer certifier JSON | `8537b2fea1fea31ef3d8300c14232e4b11f24aa4c383488b2c3414c1b6bd0956` | 15556 |
| contract-ready digest text | `050b37495c4f4110c07416bec95599ab39e200caa6e8ddaa05603bb6df4bbbbb` | 1950 |
| strict receipt text | `11315c4e507c3563e99811cbd0f4bc65823113d9d7c07a7cf2f2090d81e1b61e` | 1440 |
| cyclic-mixer CLI pytest output | `541b0292a52421d8f7f1f102d89ef653da212dd58aaaa89746ab4c856b1f8d14` | 98 |
| cyclic-mixer contract-ready pytest output | `6a188187cc4acf92013e1fe24b04baf7dba1edd907ad7d4feecc4ff2465c741f` | 98 |

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not prove cyclic-mixer model quality.
- Does not prove runtime speed, memory scaling, hardware efficiency, training
  stability, deployment readiness, transfer, benchmark performance, or ASI.
- Does not prove that a cyclic mixer should replace dense, LoRA, RoPE,
  learned, recurrent, or state-space baselines.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, VCM, PlanForge, model training,
  hardware-kernel benchmarks, serving benchmarks, or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The slice surfaces concrete Circle backing for one cyclic-mixer structural
parity and block-cyclic accounting fixture, but it remains a local
external-project import. A stronger lane would need a vendored or archived
public contract pack, clean ASI-side Circle replay, ordinary dense, LoRA,
RoPE, learned, recurrent, and state-space baselines where relevant, quality,
runtime, memory, hardware, and training-stability workloads, negative
controls, deployment/fallback traces, and a separate accepted
evidence-transition record before any support-state movement.
