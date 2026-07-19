# P4-C3 Authority, Effect, Rollback, and Corrigibility Semantic Audit

Date: 2026-07-19

Packet: `P4-C3-authority-effect-rollback-and-corrigibility-semantic-audit`
Authority: `proofs/semantic_cluster_audits/authority_effect_rollback_and_corrigibility.json`

## Terminal decision

The frozen third cluster is terminal at bounded scope: three modules are
`adequate`, and `AsiStackProofs.Corrigibility` is `reclassify`. The denominator
is four modules, eleven public proof targets, and sixty-five theorem
declarations. No theorem, target, or module was counted as evidence merely
because it compiles.

`AuthorityEffectRefinement` earns its retained role from a reachable grant,
approval, dispatch, local effect, independent-observation field, revocation,
one-shot, and rollback model plus a separate 38-mutation consumer.
`Replacement` earns its role from transaction and lifecycle routing plus three
fixture bridges consumed by separate validators. `IntentExecutionRefinement`
earns its role from exact root/parent and authority invariants over a reachable
vertical plus an 89-event consumer and thirty mutations.

`Corrigibility` does not model the richer agency lifecycle described elsewhere.
Its four declarations derive three generic branch consequences from authored
predicates and have no independent runtime consumer. They remain useful as
countermodels, so deletion would lose a small explicit failure surface; citing
them as a whole-system corrigibility theorem would be proof laundering. The
chapter now names that reclassification directly.

## Maximum inference

The cluster establishes only consequences inside its finite declared models:
sequential grant/effect routing, selected replacement decisions and fixture
bridges, three countermodel routes, and one intent-to-local-effect vertical. It
does not establish authentic identity or receipts, wise authorization,
concurrent enforcement, complete effects, monitor or evaluator truth,
inventory completeness, semantic recovery, irreversible-effect reversal,
corrigibility, intent fidelity, useful delivery, safety, deployment, transfer,
or support movement.

## Executable checks

- `python3 scripts/validate_authority_effect_refinement.py`
- `python3 scripts/validate_capability_replacement.py`
- `python3 scripts/validate_capability_replacement_trace_probe.py`
- `python3 scripts/validate_intent_governed_replacement_bridge.py`
- `python3 scripts/validate_intent_execution_vertical_refinement.py`
- `python3 scripts/validate_intent_execution_handoff_probe.py`
- `python3 scripts/validate_p4_c3_semantic_proof_cluster.py`

The cluster validator recomputes module, public-target, and theorem
denominators; requires proposition, state, assumptions, countermodels,
consumers, mutation evidence, and maximum inference for every disposition;
runs all six consumers; checks the chapter ceilings; and rejects ten
cluster-level semantic mutations. Support, release, and publication effects
remain `none`.
