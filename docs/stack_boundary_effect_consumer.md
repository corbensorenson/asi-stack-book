# Reachable stack-boundary authority/effect consumer receipt

Status: validated local finite consumer; support-state effect `none`; no
deployed-authority or chapter-core support claim.

## What ran

`lean/AsiStackProofs/StackBoundaries.lean` now separates three narrow reusable
order lemmas from a reachable boundary transition model. The model represents
a request, target-owner authorization, receipt-bound dispatch, material effect,
independent observation, revocation, denial, and exact rollback. An accepted
authorization cannot exceed the caller ceiling. An accepted material effect
requires a live same-epoch grant, an earlier dispatch receipt, and a grant that
has not been revoked.

`scripts/validate_stack_boundary_effect_consumer.py` independently reimplements
the finite decisions. It consumes all six tracked authority-transition fixtures
and binds its runtime adjudication to the existing local runtime-adapter effect
probe and five-entry revocation trace. The stored result covers:

- eighteen generated layer-contract route cases, all matching the declared
  priority-ordered admission outcome;
- six authority fixtures: three accepted and three rejected;
- three accepted runtime paths and ten accepted events;
- one material local temp-file effect, one independent observation, and one
  exact local rollback;
- two pre-effect denial paths with no mutation;
- five revocation-trace entries; and
- twelve targeted semantic mutations, all rejected.

The result is stored at
`experiments/stack_boundary_effect/results/2026-07-15-local.json` and validates
against `schemas/stack_boundary_effect_consumer.schema.json`.

Run:

```bash
lake -d lean build
python3 scripts/validate_stack_boundary_effect_consumer.py
```

## Adjudication

This closes the bounded proposition that the declared reachable model and its
independent consumer reject authority widening, effect without dispatch custody,
and post-revocation effect, while the source-anchored nominal path reaches an
observed effect and exact rollback. The consumer also preserves the behavior of
the eighteen priority-ordered layer-contract cases after physically retiring
their theorem-per-record normalizations from the live Lean surface; their frozen
rationalization lineage remains available in the proof registry.

The consumer uses existing local runtime evidence rather than claiming that its
synthetic decision paths constitute a deployed authority system. The exact
support-state effect is `none`.

## Non-claims

- The authority fixtures and decision paths are synthetic. They do not
  establish deployed authority enforcement or real target-owner control.
- Grant, owner, receipt, observer, epoch, revocation, and exact-rollback fields
  are trusted inputs. Their authenticity and complete effect discovery are not
  proved.
- The one executed effect is a local temporary-file effect. Exact rollback is
  established only for that contained path, not for hidden, distributed, or
  irreversible effects.
- The model excludes distributed clocks, partitions, retries, delegation-chain
  compromise, security, natural-workload usefulness, reproduction, transfer,
  SOTA, AGI, and ASI.
