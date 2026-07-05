# Circle KV-Cache Receipt Slice

Date: 2026-07-05

This record imports one public-safe Circle Calculus KV-cache ring-buffer
receipt slice for the Coil Attention, Cyclic Memory, and Recurrence Contracts
chapter. It is structural contract evidence only: bounded ring-buffer
freshness, request-window fields, stale-token diagnostics, sink/rolling-window
policy fields, theorem IDs, receipt fingerprints, command-output digests, and
non-claim boundaries.

Tracked result:
`experiments/circle_kv_cache_receipt_slice/results/2026-07-05-local.json`

Validator:
`python3 scripts/validate_circle_kv_cache_receipt_slice.py`

No-promotion decision:
`evidence_transitions/v1_x_measured/circle_kv_cache_receipt_no_change.json`

## Scope

External project: Circle Calculus at commit `63b0f511`.

Accepted contract ID: `CC-AI-CONTRACT-KV-001`

Contract kind: `kv_cache_ring_buffer`

Receipt schema: `circle_calculus.ai_contract_acceptance_receipt.v0`

Pack fingerprint:
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`

Contract fingerprint:
`bfebf150ce45d1eb124ea553bf2ba8c62008751ebec9f8600b83cc09e0526a46`

Required theorem IDs:

- `AIM-T0103`
- `AIM-T0104`
- `AIM-T0149`

The receipt records `theorem_count=54`, but this ASI-side slice only requires
the three theorem IDs above for the pinned stale-token and sink-window
acceptance boundary.

Required recommendation IDs:

- `KV-DROP-STALE-REQUEST-TOKEN`
- `KV-USE-SINK-ROLLING-WINDOW-REQUEST`

## Observed Fixture Facts

The accepted fixture records:

- `cache_size=16`
- `current=31`
- `token=20`
- `slot=4`
- `current_slot=15`
- `lag=11`
- `retained=true`
- `next_overwrite_token=36`
- `live_window_start=16`
- `live_window_length=16`
- `batch_tokens=[20, 24, 29, 31]`
- `batch_slots=[4, 8, 13, 15]`
- `all_non_future=true`
- `all_retained=true`
- `tokens_distinct=true`
- `slots_distinct=true`
- `ordered_live_window_subrequest=true`
- `duplicate_free_live_window_subrequest=true`
- `stale_requested_count=0`
- `sink_tokens=[0, 1, 2, 3]`
- `sink_tokens_retained_by_policy=true`
- `sink_window_exact_policy=true`
- `sink_window_tokens_distinct=true`
- `sink_prefix_disjoint_from_live_window=true`
- `sink_tokens_outside_ordinary_rolling_window=true`
- `request_token_count=20`
- `request_token_count_bound=20`
- `stale_probe_first_stale_token=12`

The planner recommendation `KV-DROP-STALE-REQUEST-TOKEN` identifies stale
target token `12` and next same-slot overwrite token `28`. The recommendation
`KV-USE-SINK-ROLLING-WINDOW-REQUEST` records `cache_size=16`, `current=31`,
`sink_size=4`, `request_token_count=20`, and `request_token_count_bound=20`.

The strict receipt command was accepted with those fields and required
theorem/recommendation IDs. The Circle CLI test command reported
`5 passed in 1.27s`.

## Command Output Digests

| Output | SHA-256 | Bytes |
|---|---:|---:|
| KV-cache certificate JSON | `0651d42d9b3c5d8820d747018faff75e83ecd97bc973ac384ae10d1e6ada40f1` | 14268 |
| Circle AI KV-cache certifier JSON | `169999b3c44aa082acf0cb8410ce3d921d16d20c486397a79197ae36c761ef4f` | 28336 |
| contract-ready digest text | `18dec02ed8d5f967f985ff0fc883cf90e0ee9b4d69d714fc4a8de84b07c69547` | 3035 |
| strict receipt JSON | `d75246f822d76c52d56521b7911e374f6f559526417b4857bea39da7cf89c100` | 8266 |
| KV-cache CLI pytest output | `87fa9996a06e4107cc2e24a8aaa2f3681b65f05c9783972fe74cd0d508fab8fb` | 98 |

## Discarded Attempts

- The first `kv_cache_certify.py` invocation omitted required `--cache-size`,
  `--current`, and `--token` arguments. The corrected command supplied the
  bounded fixture arguments and succeeded.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not prove deployed KV-cache behavior, serving throughput, memory
  savings, paging correctness, retrieval quality, reasoning quality, model
  quality, context length, speed, deployment safety, transfer, or ASI.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, VCM, PlanForge, retrieval benchmarks,
  long-context benchmarks, policy-training, serving benchmarks, paging
  benchmarks, or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The slice surfaces concrete Circle backing for one KV-cache ring-buffer
structural fixture, but it remains a local external-project import. A stronger
lane would need a vendored or archived public contract pack, clean ASI-side
Circle replay, deployed or replayed serving traces, memory and paging
measurements, retrieval-quality workloads, ordinary KV-cache baselines,
negative controls, and a separate accepted evidence-transition record before
any support-state movement.
