# Circle Cyclic Memory Receipt Slice

Date: 2026-07-02

This record imports one public-safe Circle Calculus cyclic-memory receipt slice
for the Coil Attention, Cyclic Memory, and Recurrence Contracts chapter. It is
structural contract evidence only: residue, winding, alias class, finite slot
load, theorem IDs, receipt fingerprints, command-output digests, and non-claim
boundaries.

Tracked result:
`experiments/circle_cyclic_memory_receipt_slice/results/2026-07-02-local.json`

Validator:
`python3 scripts/validate_circle_cyclic_memory_receipt_slice.py`

## Scope

External project: Circle Calculus at commit `63b0f511`.

Accepted contract ID: `CC-AI-CONTRACT-MEMORY-001`

Contract kind: `cyclic_memory_residue_winding`

Receipt schema: `circle_calculus.ai_contract_acceptance_receipt.v0`

Pack fingerprint:
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`

Contract fingerprint:
`a25d841aff585b59519919cad25d89a3f76cd8ddb11fb1549d593f7f2f09c62a`

Required theorem IDs:

- `AIM-T0001`
- `AIM-T0002`
- `AIM-T0004`
- `AIM-T0005`

Required recommendation IDs:

- `MEMORY-ATTACH-WINDING-ALIAS-PROVENANCE`
- `MEMORY-AUDIT-FINITE-ALIAS-LOAD`

## Observed Fixture Facts

The accepted fixture records:

- `bank_size=8`
- `event_index=23`
- `event_count=32`
- `residue_slot=7`
- `winding=2`
- `same_residue_events=[7, 15, 23, 31]`
- `same_residue_windings=[0, 1, 2, 3]`
- `max_alias_load=4`
- `slot_loads=[4, 4, 4, 4, 4, 4, 4, 4]`

The strict receipt command was accepted with those fields and required
theorem/recommendation IDs. The Circle CLI test command reported
`3 passed in 2.51s`.

## Command Output Digests

| Output | SHA-256 | Bytes |
|---|---:|---:|
| cyclic-memory certificate JSON | `67d4a8f79a3e12e673e35f979360d168a62522e99e1b76c190d0ecd3020d1bf9` | 5630 |
| contract-ready digest text | `e87f0835f24fca86c62b028582e40ed2792be9581da0f8fe3d972168d9e0fafc` | 895 |
| strict receipt JSON | `4efa49e37b258c58a67fd6915ff26772bd53cff4937329f9382c98530c39426e` | 3924 |
| cyclic-memory CLI pytest output | `657b1e3ad1e0cd9c3ab032ed29b580e716a78fc082f3d3517dffc07f7ce070a6` | 98 |

## Discarded Attempts

- The first script invocation omitted `PYTHONPATH=.` and failed with
  `ModuleNotFoundError: No module named 'circle_math'`. The corrected command
  succeeded and is the recorded evidence command.
- A local `shasum` attempt inherited unsupported `C.UTF-8` locale settings.
  The final output digests were computed after setting `en_US.UTF-8` and using
  Python `hashlib`.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not prove retrieval quality, reasoning quality, model quality, context
  length, speed, memory scaling, throughput, paging correctness, deployment
  safety, transfer, or ASI.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, VCM, PlanForge, retrieval benchmarks,
  long-context benchmarks, policy-training, or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The slice surfaces concrete Circle backing for one cyclic-memory
residue/winding fixture, but it remains a local external-project import. A
stronger lane would need a vendored or archived public contract pack, clean
ASI-side Circle replay, downstream workload baselines, memory/retrieval
metrics, negative controls, and a separate accepted evidence-transition record
before any support-state movement.
