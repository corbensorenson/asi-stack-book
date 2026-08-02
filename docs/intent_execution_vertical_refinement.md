# Intent-to-Execution vertical refinement receipt

Status: validated source-anchored finite refinement; support-state effect
`none`; no general semantic-equivalence, deployment, or chapter-core claim.

## What ran

`lean/AsiStackProofs/IntentExecutionRefinement.lean` defines a reachable partial
transition model from accepted intent through command, plan, job, authorization,
dispatch, attempted effect, independent observation, artifact binding,
verification, delivery, blocking, residual custody, rollback, and quarantine.
Its exact 37-declaration surface gives every event kind an exclusive payload
contract and proves one-step and arbitrary-run preservation of contract and
authority custody, authority bounds, logical time, effect accounting, dispatch,
artifact, verification, delivery, stop, and residual invariants. Eighteen
closed countermodels reject identity substitution, stale time, smuggled
payloads, premature transitions, self-verification, inexact rollback, and
quarantine without residual custody.

`scripts/validate_intent_execution_vertical_refinement.py` independently
consumes the complete tracked
`asi_stack.governed_repository_change_result.v0` artifact and validates it
against its public schema. It also requires the exact theorem surface, rejects
unproved declarations, and compiles the module before checking all nine
executed scenarios and all 89 recorded governed events:

- three release paths with exact allowed changed paths, matching artifact
  receipts, independent effect observation, independent evaluator identity,
  safety checks, evidence acceptance, and delivery;
- three pre-effect refusals caused by stale authorization, revocation, or
  correlated proposer/verifier identity;
- two post-effect refusals with independent observation and exact rollback;
- one failed-rollback quarantine with an open residual;
- six material repository effects and six independent observations;
- two exact rollbacks and two scenarios with discovered residuals; and
- thirty concrete semantic mutations, all rejected.

The prompt-injection scenario requires quarantine of the retrieved instruction
before the allowed effect. The cheaper-route scenario requires rejection of the
ineligible route before the accepted effect. Result:
`experiments/intent_execution_vertical_refinement/results/2026-07-15-local.json`.

Run:

```bash
lake -d lean build
python3 scripts/validate_intent_execution_vertical_refinement.py
```

## Adjudication

This is evidence for the exact finite contract lineage, payload typing,
authority, time, effect, observation, artifact, verification, terminal,
rollback, and residual obligations above, plus a checked executable refinement
over one executed source schema. The support-state effect is exactly `none`.

## Non-claims

- Event names, expected dispositions, authorization state, verifier identity,
  receipts, and observations are trusted source fields, not cryptographically
  authenticated world facts.
- The repository slice uses a fixed requested change and deterministic local
  implementation; it does not establish natural-language intent extraction,
  general semantic equivalence, planning quality, or natural-workload utility.
- It does not establish a deployed dispatcher, approval or capability service,
  tool safety, complete effect discovery, distributed execution, reproduction,
  transfer, SOTA, AGI, ASI, or chapter-core support.
