# Circle Contract-Pack Archive

This fixture directory vendors a bounded public-safe Circle contract-pack
snapshot from Circle commit `63b0f511` for ASI-side digest verification.

Archived pack:
`fixtures/circle_ai_contract_pack.63b0f511.json`

Acceptance-policy report:
`fixtures/circle_ai_acceptance_policy_report.63b0f511.json`

Validator:
`python3 scripts/validate_circle_contract_pack_archive.py`

The Circle contract-pack archive records 9 archived contracts with internal
pack fingerprint
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`.
The raw archived pack file SHA-256 is
`b5488c93109ef120b97fdea7bd5d5605f32b2618c6cbfb9dde9a3328652551c4`.
The stable JSON SHA-256 is
`10e2dc51e9a6fe2591b2878a293dfdaa2fecf7a2ff588954495f429082724891`.

The acceptance-policy report records 4 acceptance-policy receipts with raw
report file SHA-256
`f1671f5cecdee311185f7e4508b21c139d4ae4bd1fa9610a12827f4d31c7985a`
and stable JSON SHA-256
`6f49d87702e1d9e078c806778abfcdfd0efdc762d263a973b78f0b9c15c491a6`.

Tracked contracts:

- `CC-AI-CONTRACT-ROPE-001`:
  `a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468`
- `CC-AI-CONTRACT-KV-001`:
  `bfebf150ce45d1eb124ea553bf2ba8c62008751ebec9f8600b83cc09e0526a46`
- `CC-AI-CONTRACT-SPARSE-001`:
  `c23809cef9b821b1e4f9cabf53fcac724a0757bf3f86594e1d12710fe0cd9ec1`
- `CC-AI-CONTRACT-RECURRENCE-001`:
  `571edd5dce4f7b64441806de323295218a3e2293b3b540dd4772ba34b9371515`
- `CC-AI-CONTRACT-FANOUT-001`:
  `d4c878563747da9c9f1f55cd689f04e2a0a8e31ce9429a138341ec4e27ee3799`
- `CC-AI-CONTRACT-MEMORY-001`:
  `a25d841aff585b59519919cad25d89a3f76cd8ddb11fb1549d593f7f2f09c62a`
- `CC-AI-CONTRACT-PHASE-FEATURE-001`:
  `4b562beab64ec863903e4267f50c90049f0d3fa612f6c1bb2f06ad07e821ffd7`
- `CC-AI-CONTRACT-MIXER-001`:
  `b3e3e0cf420d9e8e79a28a55ef8322f9a214c8d5a957dd8b06e5e5373c684ea5`
- `CC-AI-CONTRACT-SEED-RULE-001`:
  `836594a5f1d448900797e595cb98f0e476c0b9cbd7365fe333cf7ae2622f13c5`

The archived pack declares `public_safe_fixture`.

Non-claims: this fixture does not promote any chapter core claim, does not
create a support-state transition, does not rerun Circle Lean, does not prove
deployed proof-contract transport, and does not prove model quality, context
length, runtime speed, memory scaling, deployment safety, transfer, safety, or
ASI. The accepted no-promotion decision is
`evidence_transitions/v1_x_measured/circle_contract_pack_archive_no_change.json`.
