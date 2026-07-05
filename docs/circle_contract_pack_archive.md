# Circle Contract-Pack Archive

Date: 2026-07-05

This record archives a public-safe generated Circle AI contract pack inside
The ASI Stack repository. It closes the most concrete part of the Milestone 4
gap: the Circle lane is no longer only a local summary or a single ASI-side
consumer fixture. The repo now carries a pinned contract-pack artifact and a
bounded acceptance-policy report that can be verified without reading a private
local checkout.

Archived pack:
`experiments/circle_contract_pack_archive/fixtures/circle_ai_contract_pack.63b0f511.json`

Acceptance-policy report:
`experiments/circle_contract_pack_archive/fixtures/circle_ai_acceptance_policy_report.63b0f511.json`

Tracked result:
`experiments/circle_contract_pack_archive/results/2026-07-05-local.json`

Validator:
`python3 scripts/validate_circle_contract_pack_archive.py`

## Archive Scope

- Source project: Circle Calculus
- Source commit: `63b0f511`
- Pack status: `public_safe_fixture`
- Circle internal pack fingerprint:
  `df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`
- Raw archived pack file SHA-256:
  `b5488c93109ef120b97fdea7bd5d5605f32b2618c6cbfb9dde9a3328652551c4`
- Stable JSON pack SHA-256:
  `10e2dc51e9a6fe2591b2878a293dfdaa2fecf7a2ff588954495f429082724891`
- Raw acceptance-policy report file SHA-256:
  `f1671f5cecdee311185f7e4508b21c139d4ae4bd1fa9610a12827f4d31c7985a`
- Stable JSON report SHA-256:
  `6f49d87702e1d9e078c806778abfcdfd0efdc762d263a973b78f0b9c15c491a6`

The archive contains 9 archived contracts. The bounded acceptance-policy
report contains 4 acceptance-policy receipts for the flagship policy subset.

## Contract Fingerprints

| Kind | Contract ID | Contract fingerprint | Theorem count |
|---|---:|---:|---:|
| `rope_position_distinguishability` | `CC-AI-CONTRACT-ROPE-001` | `a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468` | 75 |
| `kv_cache_ring_buffer` | `CC-AI-CONTRACT-KV-001` | `bfebf150ce45d1eb124ea553bf2ba8c62008751ebec9f8600b83cc09e0526a46` | 54 |
| `sparse_attention_coverage` | `CC-AI-CONTRACT-SPARSE-001` | `c23809cef9b821b1e4f9cabf53fcac724a0757bf3f86594e1d12710fe0cd9ec1` | 141 |
| `recurrence_schedule` | `CC-AI-CONTRACT-RECURRENCE-001` | `571edd5dce4f7b64441806de323295218a3e2293b3b540dd4772ba34b9371515` | 64 |
| `strided_candidate_fanout` | `CC-AI-CONTRACT-FANOUT-001` | `d4c878563747da9c9f1f55cd689f04e2a0a8e31ce9429a138341ec4e27ee3799` | 4 |
| `cyclic_memory_residue_winding` | `CC-AI-CONTRACT-MEMORY-001` | `a25d841aff585b59519919cad25d89a3f76cd8ddb11fb1549d593f7f2f09c62a` | 4 |
| `multicoil_phase_feature` | `CC-AI-CONTRACT-PHASE-FEATURE-001` | `4b562beab64ec863903e4267f50c90049f0d3fa612f6c1bb2f06ad07e821ffd7` | 5 |
| `circulant_block_cyclic_mixer` | `CC-AI-CONTRACT-MIXER-001` | `b3e3e0cf420d9e8e79a28a55ef8322f9a214c8d5a957dd8b06e5e5373c684ea5` | 7 |
| `seed_rule_exact_regeneration` | `CC-AI-CONTRACT-SEED-RULE-001` | `836594a5f1d448900797e595cb98f0e476c0b9cbd7365fe333cf7ae2622f13c5` | 32 |

## Checks

`python3 scripts/validate_circle_contract_pack_archive.py` checks:

- the raw archive file SHA-256 and stable JSON SHA-256 for both artifacts;
- the Circle-declared `sha256-json-v1` pack fingerprint;
- all 9 archived contracts, their IDs, contract fingerprints, and theorem
  counts;
- the 4 acceptance-policy receipts, accepted status, pack fingerprint, and
  recommendation count;
- public-safety hygiene for local paths, file URIs, localhost references, and
  obvious secret markers;
- five expected-invalid controls: pack fingerprint mismatch, contract
  fingerprint mismatch, unsafe local-path injection, rejected acceptance
  report, and acceptance-report pack mismatch.

## Accepted No-Promotion Decision

`evidence_transitions/v1_x_measured/circle_contract_pack_archive_no_change.json`
records this as an accepted `blocks_promotion` side-lane decision for
`circle-calculus.contract_pack_archive`. It is useful because the ASI Stack
repo can now verify an archived public-safe Circle pack by digest and boundary
checks, but it does not create an upward support-state transition.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not rerun Circle Lean or certify Circle from this repository.
- Does not prove deployed proof-contract transport.
- Does not prove model quality, reasoning ability, context length, runtime
  speed, memory scaling, deployment safety, transfer, safety, or ASI.
- Does not replace a future clean Circle replay, workload baseline, deployment
  trace, external audit, or accepted upward evidence-transition record.

## Residuals

The archive satisfies the public-safe contract-pack/artifact branch of the
Circle replay milestone. The stronger remaining work is still a clean Circle
replay from this repository or from a stable public release, plus any downstream
transport trace, workload/baseline metrics, and independent review needed for a
narrow upward evidence transition.
