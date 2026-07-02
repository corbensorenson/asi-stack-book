# Policy Optimization Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `policy-optimization-and-learning-from-feedback`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source:
`build/reader_edition/chapters/policy-optimization-and-learning-from-feedback.qmd`

Curated prose draft:
`editions/reader_manuscript/v1_0/chapters/policy-optimization-and-learning-from-feedback.qmd`

Evidence references: `docs/curated_reader_policy_optimization_prose_pass.md`,
`schemas/policy_optimization_record.schema.json`,
`scripts/validate_benchmark_antigoodhart.py`,
`experiments/benchmark_antigoodhart/`, and
`lean/AsiStackProofs/PolicyOptimization.lean`.

This note helps e-reader and audio review for the Policy Optimization chapter.
It does not replace the chapter prose or the curated prose draft.
Meaning-critical limits must still stay in the reader spine: a policy update is
a governed behavior-change lease, reward is not truth, and local fixtures/proofs
do not prove training improvement, reward quality, or reward-hacking safety.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
why the chapter treats learning from feedback as a controlled change to a
bounded policy. The question is not "did the score go up?" It is what behavior
changed, which feedback was admissible, what reward boundary applied, what
authority changed, which holdouts and regressions survived, and how rollback
works.

## Dense Material Routed Here

| Dense item | Plain meaning | Boundary |
|---|---|---|
| Policy Optimization Record | The record for target policy, old/new behavior, feedback source, reward boundary, update family, drift bound, holdouts, regressions, probes, authority effect, rollback, monitor window, residuals, and non-claims. | It controls update meaning; it does not prove the update improved the model. |
| Reward or preference boundary | The scope in which a score, preference, process reward, verifier reward, or feedback signal is allowed to count. | Reward is a proxy, not truth or authority. |
| Reward-hacking probe | A negative check for shortcuts, proxy gaming, hidden authority expansion, or evidence laundering. | Passing a small probe is not general reward-hacking resistance. |
| Holdout and regression refs | The tests that keep the update from improving one visible metric while damaging hidden behavior. | They are scoped evidence, not universal safety. |
| Authority effect | Whether the update changes what the policy is allowed to do. | Learning may not silently widen authority. |
| Rollback and monitor window | The bounded path for canarying, observing, downgrading, or undoing the update. | A rollback plan is not proof that rollback succeeded in deployment. |

## Main Spine Must Keep

The reader chapter should not move these boundaries exclusively into companion
material:

- reward, preference, verifier, and benchmark signals are scoped proxies;
- policy updates must preserve authority ceilings unless a governance record
  explicitly changes them;
- method families such as PPO-like, DPO-like, GRPO-like, RLVR-like,
  context-policy, router-policy, verifier-policy, and custom control-policy
  updates are orientation, not local reproduction;
- local artifacts check synthetic cross-record gate behavior and finite Lean
  predicates only;
- no local policy training, model improvement, RLHF reproduction, reward-model
  validation, benchmark improvement, reward-hacking solution, rollback success,
  policy safety, deployment result, or support-state promotion is claimed.

## Audio Treatment

In an audio script, do not read the whole method-family list as a taxonomy
chapter. Narrate policy optimization as a behavior-change lease:

- identify the policy being changed;
- identify the feedback and its boundary;
- prove the reward is not being treated as truth;
- preserve authority and rollback;
- promote only through scoped evidence packets.

Detailed update fields, method names, and fixture lists can be routed to this
companion note. The main audio should keep the ordinary reader focused on the
boundary between learning and uncontrolled drift.

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim local policy training, model improvement,
  RLHF reproduction, reward-model validation, reward quality, benchmark
  improvement, reward-hacking resistance, policy safety, route-quality
  improvement, context-selection quality, rollback success, deployment result,
  or governed self-improvement.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.
