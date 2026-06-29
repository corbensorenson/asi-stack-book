# Circle Public Consumer Gate

Date: 2026-06-29

This record adds an ASI Stack consumer gate around the external Circle rope
receipt already recorded in `docs/circle_external_receipt_slice.md`. The gate
is public-safe and CI-verifiable inside this repository: it validates a pinned
receipt fixture, checks the theorem IDs and fingerprints carried by the prior
Circle result, and rejects malformed or overclaimed downstream uses.

Accepted fixture:
`experiments/circle_public_replay/fixtures/valid/circle_rope_receipt.consumer.valid.json`

Accepted receipt ID:
`circle.rope.CC-AI-CONTRACT-ROPE-001.public_consumer_gate`

Tracked result:
`experiments/circle_public_replay/results/2026-06-29-local.json`

Validator:
`python3 scripts/validate_circle_public_replay.py`

Accepted public receipt fixture SHA-256:
`7b33bc7059fa8f6b2ed1282ca5b0c4ab7f6f5044c2f834d487bdefbce44969c6`

## Scope

The consumer gate verifies the ASI-side conditions for accepting a proof-contract
receipt as structural evidence:

- Circle source commit: `63b0f511`
- Contract ID: `CC-AI-CONTRACT-ROPE-001`
- Contract family: `rope_position_distinguishability`
- Contract content fingerprint:
  `a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468`
- Receipt content fingerprint:
  `91b72a6dcf821a9733f21800cd1093a3d0665588022031ba72c94893800330c3`
- Normalized request fingerprint:
  `20e68c5f787e267c6611bc57b8d8e98e1cb0f5a74f272379716a5d83e761407d`
- Contract-pack fingerprint:
  `df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`
- Required recommendation ID: `ROPE-USE-D19-MARGIN-FRONTIER`

Required theorem IDs:

- `AIRA-T0058`
- `AIRA-T0059`
- `AIRA-T0171`
- `AIRA-T0172`
- `AIRA-T0239`
- `AIRA-T0240`
- `AIRA-T0241`

Required deterministic fields:

- `d19_proved_request_status=proved`
- `d19_proved_first_channel_bank_transfer=true`
- `real_phase_dirichlet_witness_guardrail=true`

## Negative Controls

The validator rejects four mutation controls:

- digest mismatch;
- missing required theorem ID;
- stale contract fingerprint status;
- unsupported transfer-claim use in the consumer gate.

These controls are the practical point of this lane. They make the receipt
usable as a guarded public fixture rather than a local-only prose summary.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not prove model quality, reasoning ability, context length, speed,
  memory scaling, deployment safety, transfer, or ASI.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Circle Calculus from this repository or vendor the
  external contract pack.
- Does not create a new accepted support-state transition.

## Residuals

The Circle lane is now ASI-side CI-verifiable by public fixture and pinned
digest, but it is still not a vendored upstream Circle contract pack or a clean
Circle replay performed by this repository. Stronger proof-carrying-computation,
cyclic-memory, RoPE, transport, transfer, or model-quality claims still require
fresh replay artifacts, workload baselines, metrics, negative controls, and
accepted evidence-transition records before any support-state promotion.
