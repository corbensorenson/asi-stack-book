# Intent-to-Execution vertical refinement receipt

Status: validated source-anchored finite refinement; support-state effect
`none`; no general semantic-equivalence, deployment, or chapter-core claim.

## What ran

`lean/AsiStackProofs/IntentExecutionRefinement.lean` defines a reachable partial
transition model from accepted intent through command, plan, job, authorization,
dispatch, attempted effect, independent observation, artifact binding,
verification, delivery, blocking, residual custody, rollback, and quarantine.
Every accepted step joins the same root contract and exact parent artifact,
cannot widen authority, and cannot apply a hidden override. Dispatch requires
approval and a dispatch receipt; effect requires prior dispatch; delivery
requires verification and complete effect observation.

`scripts/validate_intent_execution_vertical_refinement.py` independently
consumes the complete tracked
`asi_stack.governed_repository_change_result.v0` artifact and validates it
against its public schema. It checks all nine executed scenarios and all 89
recorded governed events:

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

This replaces two assumption-restating theorem declarations with a reachable
vertical transition relation and a checked executable refinement over one
executed source schema. It is evidence for the exact local contract lineage,
authority, effect, observation, artifact, verification, terminal, rollback,
and residual obligations above. The support-state effect is exactly `none`.

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
