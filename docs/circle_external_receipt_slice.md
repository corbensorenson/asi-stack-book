# Circle External Receipt Slice

Date: 2026-06-29

This record documents the first imported external prototype receipt slice for
the v1.0 candidate. It records a public-safe summary of local commands run in
the external Circle Calculus checkout, then scopes the support effect to one
narrow claim about replaying and accepting a Circle rope-position contract
receipt. The external project is not vendored into this repository, and this
record does not make the ASI Stack book depend on a private local path during
CI.

Accepted narrow claim: `circle-calculus.external_rope_receipt_replay`

Claim: A local external Circle Calculus checkout at commit `63b0f511` can build
its `Circle` Lean target, certify the rope position distinguishability contract,
emit a ready digest and accepted receipt for `CC-AI-CONTRACT-ROPE-001`, and pass
the selected public-safe receipt/contract test batch recorded in the result
file.

Support transition: `argument` to `prototype-backed`

Transition record:
`evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json`

Tracked result:
`experiments/circle_external_receipt_slice/results/2026-06-29-local.json`

## Local Provenance

External checkout: `/Users/corbensorenson/Documents/circle math`

External checkout commit: `63b0f511`

External checkout state after the corrected commands: clean worktree.

The external project was selected for this slice because the Circle checkout was
clean and replayable for the scoped receipt command set. Project Theseus was not
selected for this first imported slice because the inspected local checkout had
dirty and untracked files plus private-data surfaces that made it less suitable
for a public-safe v1.0 receipt import.

## Commands And Observed Results

```bash
lake build Circle
```

Observed result: `Build completed successfully (2624 jobs).`

```bash
python3 scripts/circle_ai_certify.py rope --model-config examples/circle_ai_model_configs/standard_rope_config.json --requested-margin 1/328459 --format json --require-status proved --require-decision passed --require-assurance mixed_theorem_and_computation --require-passed
```

Observed result: `status` was `proved`, `request_passed` was `true`, the
decision verdict was `passed`, assurance was
`mixed_theorem_and_computation`, `theorem_count` was 55, and all theorem IDs
were proved. The receipt content fingerprint was
`91b72a6dcf821a9733f21800cd1093a3d0665588022031ba72c94893800330c3`;
the normalized request fingerprint was
`20e68c5f787e267c6611bc57b8d8e98e1cb0f5a74f272379716a5d83e761407d`;
the contract-pack fingerprint was
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`.

```bash
PYTHONPATH=. python3 scripts/circle_ai_contract_ready.py --kind rope_position_distinguishability --digest --include-recommendations
```

Observed result: `circle AI contract digest ok:
rope_position_distinguishability`; `id=CC-AI-CONTRACT-ROPE-001 ready=True
fields=31 missing=0 theorems=75`.

Relevant digest fields included
`evidence.d19_proved_request_status="proved"`,
`evidence.d19_proved_first_channel_bank_transfer=true`,
`evidence.real_phase_dirichlet_witness_guardrail=true`,
`evidence.exact_discrete_pass=true`, and
`evidence.total_bank_collision_pair_count=0`. The digest also surfaced the
recommendation `ROPE-USE-D19-MARGIN-FRONTIER`.

```bash
PYTHONPATH=. python3 scripts/circle_ai_contract_ready.py --kind rope_position_distinguishability --receipt --format json --field d19_proved_request_status --field d19_proved_first_channel_bank_transfer --field real_phase_dirichlet_witness_guardrail --require-theorem AIRA-T0058 --require-theorem AIRA-T0059 --require-theorem AIRA-T0171 --require-theorem AIRA-T0172 --require-theorem AIRA-T0239 --require-theorem AIRA-T0240 --require-theorem AIRA-T0241 --require-recommendation ROPE-USE-D19-MARGIN-FRONTIER
```

Observed result: the receipt was accepted. The receipt schema was
`circle_calculus.ai_contract_acceptance_receipt.v0`; the contract ID was
`CC-AI-CONTRACT-ROPE-001`; the kind was
`rope_position_distinguishability`; the schema ID was
`circle_calculus.ai_contract_pack.v0`; the pack fingerprint was
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`;
and the contract fingerprint was
`a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468`.

Required theorem IDs:

- `AIRA-T0058`
- `AIRA-T0059`
- `AIRA-T0171`
- `AIRA-T0172`
- `AIRA-T0239`
- `AIRA-T0240`
- `AIRA-T0241`

Required recommendation ID: `ROPE-USE-D19-MARGIN-FRONTIER`

Accepted evidence fields:

- `d19_proved_request_status`: `proved`
- `d19_proved_first_channel_bank_transfer`: `true`
- `real_phase_dirichlet_witness_guardrail`: `true`

```bash
PYTHONPATH=. python3 -m pytest tests/test_check_circle_ai_receipt.py tests/test_check_circle_ai_certification_bundle.py tests/test_check_circle_ai_receipt_replay.py tests/test_check_circle_ai_contract_runner.py tests/test_downstream_ci_accept_circle_ai_contracts.py tests/test_theseus_hive_ai_contracts.py tests/test_circle_ai_contract_ready_cli.py tests/test_circle_ai_contract_pack.py -q
```

Observed result: `145 passed in 718.24s (0:11:58)`.

## Discarded Attempts

- A first pytest command named
  `tests/test_check_circle_ai_contract_pack.py`, which was not present in the
  external checkout. Pytest reported the missing path and no tests ran. This was
  a procedural command-selection error, not evidence.
- A first ready-digest command omitted `PYTHONPATH=.` and failed with
  `ModuleNotFoundError: No module named 'circle_math'`. The corrected command
  succeeded and is the recorded evidence command.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not prove model quality, reasoning ability, context length, speed,
  memory scaling, deployment safety, transfer, or ASI.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, Talos, VCM, PlanForge, compression,
  routing, benchmark, policy-training, or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The next Circle-related evidence increment should either vendor a public
contract pack, add an explicit public replay fixture, or route a proof-contract
receipt through an ASI Stack consumer gate. Broader proof-carrying-computation,
cyclic-memory, RoPE, or model-quality claims still require separate evidence
records, exact commands, source boundaries, negative controls where applicable,
and accepted transitions before any chapter core claim can move above
`argument`.

