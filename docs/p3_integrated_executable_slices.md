# P3 Integrated Executable Slices

Executed: 2026-07-16

Status: bounded local replay passed; P3/M4 closure candidate; no support or
external-action authority.

## What ran

One versioned transaction interface consumes three retained real-output lanes:

- Governed work consumes a real Qwen2.5-Coder output from the 2026-07-10
  disposable-repository flagship and performs independently observed temporary-
  file effects.
- Governed learning consumes real base and bounded-finetune checkpoint bytes
  from the 2026-07-10 update-causality run and exercises promotion, replay,
  exact rollback, and a deliberately retained backup residual.
- Assurance/control consumes retained real model output together with the
  bounded safety-case result and exercises escalation, monitor-triggered
  revocation, quarantine, and recovery.

The twelve cases jointly cover successful, refused, escalated, failed,
partially effected, rolled-back, replayed, stale, revoked, and corrupted
routes. Six local effects are attempted and independently byte-observed. Three
restore their exact prior digest, one leaves an owned backup residual, one is
quarantined with an incident residual, and one is acknowledged. Twenty named
boundary injections cover intent, context, routing, authority, effects,
observation, artifacts, evaluation, release, rollback, data admission, full
state, checkpoints, backups, thresholds, oversight, safety cases, monitoring,
revocation, and recovery; none escapes its recorded route.

## Cross-slice epistemic trace

The cross-slice trace does not collapse environment, observation,
interpretation, or belief. An independent byte reader creates an immutable raw
observation. Two competing interpretations remain in lineage. A versioned
belief decision selects one on the basis of an exact effect receipt while
retaining the rejected interpretation and bounded uncertainty. Work, learning,
and assurance consumers bind that exact belief version.

The trace then enters one bounded quiescent epoch: candidate admission closes;
one in-flight effect drains and one is residualized; model, optimizer,
scheduler, RNG, cache, backup, descendant, effect, claim, artifact, and memory
surfaces are snapshotted; episode-to-abstraction and abstraction-to-episode
links remain bidirectional; regression, safety, and effect checks replay; the
previous epoch is compared; and zero undeclared mutations remain. The sealed
outcome explicitly retains one owned residual.

## Historical protocol correction

`evidence_transitions/post_v2_3/instrument_failure_supersession.json` preserves
the immutable 2026-07-13 governance-tax and residual-honesty transitions while
superseding their claim-level `no_change` interpretation with
`instrument_inadequate_recampaign_required`. Neither failed instrument counts
as a claim attempt. The separate repaired 32-candidate governance-tax
`no_change` transition remains valid and untouched.

## Evidence boundary

The run replays retained local model and checkpoint outputs; it is not a fresh
model-quality or causal campaign. Effects are temporary files and checkpoint
copies, not production services or irreversible open-world actions. Failure
routes are bounded local controls. The observer is independent code, not an
external institution. The quiescent epoch is one-process evidence, not a
distributed stabilization proof.

This packet does not establish model quality, evaluator or reviewer validity,
open-world effect discovery, deployed rollback, useful throughput, safety,
reproduction, transfer, SOTA, AGI, or ASI. It grants no chapter-core support,
release, publication, or external-action authority.

## Reproduction

```bash
python3 scripts/validate_p3_integrated_slices.py
```

The validator reruns the temporary effects, recomputes every retained source
digest and exact result, checks all twenty injection routes, and rejects eleven
mutations spanning source substitution, status omission, effect observation,
rollback, epistemic lineage, stabilization, failure escape, and support
laundering.
