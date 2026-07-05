# Circle Recurrence Receipt Slice

Date: 2026-07-05

This record imports one public-safe Circle Calculus recurrence-schedule receipt
slice for the Coil Attention, Cyclic Memory, and Recurrence Contracts chapter.
It is structural contract evidence only: finite loop-period fields,
active/inactive token work traces, scheduled work-saving accounting,
whole-period shift invariants, theorem IDs, receipt fingerprints,
command-output digests, planner recommendations, and non-claim boundaries.

Tracked result:
`experiments/circle_recurrence_receipt_slice/results/2026-07-05-local.json`

Validator:
`python3 scripts/validate_circle_recurrence_receipt_slice.py`

No-promotion decision:
`evidence_transitions/v1_x_measured/circle_recurrence_receipt_no_change.json`

## Scope

External project: Circle Calculus at commit `63b0f511`.

Accepted contract ID: `CC-AI-CONTRACT-RECURRENCE-001`

Contract kind: `recurrence_schedule`

Receipt schema: `circle_calculus.ai_contract_acceptance_receipt.v0`

Pack fingerprint:
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`

Contract fingerprint:
`571edd5dce4f7b64441806de323295218a3e2293b3b540dd4772ba34b9371515`

Required theorem IDs:

- `AIM-T0026`
- `AIM-T0130`
- `AIM-T0159`

The receipt records `theorem_count=64`, but this ASI-side slice only requires
the three theorem IDs above for the pinned work-schedule and whole-period shift
acceptance boundary.

Required recommendation IDs:

- `RECURRENCE-USE-ACTIVE-TOKEN-WORK-SCHEDULE`
- `RECURRENCE-REUSE-WHOLE-PERIOD-SHIFT`

## Observed Fixture Facts

The accepted fixture records:

- `loop_period=5`
- `sample_index=8`
- `max_loops=7`
- `required_steps=4`
- `exit_step=4`
- `overthinking_boundary=5`
- `active_token_count_trace=[8, 6, 4, 2, 1]`
- `inactive_token_count_trace=[0, 2, 4, 6, 7]`
- `active_token_count_trace_sum=21`
- `inactive_token_count_trace_sum=19`
- `total_active_token_work=21`
- `total_inactive_token_work=19`
- `full_loop_token_work=40`
- `scheduled_work_saving=19`
- `scheduled_work_saving_accounting=true`
- `active_inactive_work_accounting=true`
- `scheduled_work_saving_positive=true`
- `post_period_extension_active_work_unchanged=true`
- `post_period_multi_extension_scheduled_work_saving=43`
- `post_period_multi_extension_active_work_unchanged=true`
- `periodic_shift_base_token=7`
- `periodic_shift_passes=3`
- `periodic_shift_amount=15`
- `periodic_shifted_token=22`
- `periodic_shift_required_steps_invariant=true`
- `periodic_shift_recurrence_budget_invariant=true`
- `periodic_shift_training_free_budget_invariant=true`
- `periodic_shift_exit_step_invariant=true`
- `periodic_shift_overthinking_boundary_invariant=true`
- `periodic_shift_active_at_step_invariant=true`

The planner recommendation `RECURRENCE-USE-ACTIVE-TOKEN-WORK-SCHEDULE` records
a finite default loop schedule with active token work `21`, inactive token work
`19`, scheduled work saving `19`, and multi-extension scheduled work saving
`43`. The recommendation
`RECURRENCE-REUSE-WHOLE-PERIOD-SHIFT` records base token `7`, shift amount
`15`, shifted token `22`, and whole-period shift invariants.

The strict receipt command was accepted with those fields and required
theorem/recommendation IDs. The Circle CLI test command reported
`2 passed in 2.37s`.

## Command Output Digests

| Output | SHA-256 | Bytes |
|---|---:|---:|
| recurrence schedule certificate JSON | `18dec9b030fdae61838ae778c9f22b39f318d7449611244f4e745e7e1d77d9ad` | 38845 |
| Circle AI recurrence certifier JSON | `2a4a40151f7c4ac900bcfcbb3a1f42fe68020c8eae269a523f971af5b794318d` | 58239 |
| contract-ready digest text | `cbb84e6e0fcd374895ed998307380917849d30a1268c211dfa4e43bac1357689` | 4060 |
| strict receipt JSON | `5b1d20752090cda0e4c2d0cf43b22c6832b46db6ae910f98fa3f18a4d47f32fa` | 12285 |
| recurrence CLI pytest output | `4ebae0342e485c764b9428f69b6f0535e7506cc353926f4c51e028fd1052d0d3` | 98 |

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not prove deployed recurrence behavior, reasoning quality, retrieval
  quality, learned-memory behavior, convergence, model quality, context length,
  speed, memory savings, deployment safety, transfer, or ASI.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, VCM, PlanForge, retrieval benchmarks,
  long-context benchmarks, policy-training, serving benchmarks, recurrence
  benchmarks, or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The slice surfaces concrete Circle backing for one recurrence-schedule
structural fixture, but it remains a local external-project import. A stronger
lane would need a vendored or archived public contract pack, clean ASI-side
Circle replay, deployed or replayed recurrence-controller traces, ordinary
attention and recurrence baselines, negative controls, memory-quality and
long-context workloads, and a separate accepted evidence-transition record
before any support-state movement.
