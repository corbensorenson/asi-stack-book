# Formal-Methods External Review Packet

Status: ready for assignment; no reviewer assigned. Last updated: 2026-07-10.

## Reviewer capacity and independence

Use the `formal_methods_reviewer` capacity role. The reviewer should have
practical proof-assistant or formal-specification experience and enough trace,
state-machine, or concurrency background to distinguish theorem validity from
semantic adequacy. Record identity or anonymized expertise, conflicts, project
independence, current load, response window, and review-quality measurement
state. The author and AI collaborators are proposers, not independent reviewers.

## Review boundary

This is a semantic-adequacy review, not a request to confirm that `lake build`
passes. A valid Lean theorem may formalize the wrong property, omit a relevant
state, assume away concurrency, or exceed what runtime logs establish. Review
input may narrow prose, add counterexamples, create theorem work, or block a
claim. It is not itself proof evidence or a support transition.

## Required artifacts

1. `lean/AsiStackProofs/GovernedRepositoryTrace.lean`
2. `docs/governed_trace_invariants.md`
3. `experiments/governed_trace_invariants/results/2026-07-10-local.json`
4. `experiments/governed_repository_change_slice/results/2026-07-10-local.json`
5. `scripts/run_governed_trace_invariants.py`
6. `scripts/validate_governed_trace_invariants.py`
7. `docs/proof_adequacy_review.md` and `docs/proof_depth_classification.md`
8. `proofs/proof_manifest.json` and `proofs/proof_triage.json`

## Required questions

1. Do authority monotonicity, revocation-before-effect, evidence integrity, and
   residual conservation match their prose definitions, or merely the fixture?
2. Is the revocation-wins tie rule represented at the right event/time layer?
   Give a counterexample involving clock skew, partial order, or concurrent effect.
3. Which assumptions are hidden in total ordering, finite identities, complete
   event visibility, trusted logs, and residual enumeration?
4. Can any theorem pass after an effect that should be unauthorized, a forged
   evidence transition, or residual deletion? Show the smallest countermodel.
5. Which properties are safety invariants, liveness properties, refinement
   relations, audit checks, or only schema predicates?
6. Does the Python-log/Lean-fixture linkage establish correspondence or only
   matching constants? Identify any semantic gap.
7. Which one theorem or model change would most increase adequacy without
   implying deployed enforcement?
8. Which public proof headline should be narrowed, demoted, or rewritten?

## Adversarial review prompts

- Reorder concurrent revocation and effect events without changing timestamps.
- Omit one unseen residual and ask whether conservation can detect absence.
- Preserve evidence-record shape while substituting an invalid measurement.
- Reuse an authority grant after expiry through a new identifier or delegated path.
- Make the Lean predicate true while the operational interpretation is false.

## Severity and disposition rubric

| Severity | Meaning | Default route |
|---|---|---|
| Critical | Public theorem/prose relationship permits a materially false assurance claim. | Block headline; narrow claim; add regression immediately. |
| High | Core invariant omits a realistic counterexample or relies on an undisclosed assumption. | Add model/test work and residual; prevent adequacy claim. |
| Medium | Scope, naming, or correspondence is ambiguous but bounded. | Clarify prose/spec and add a targeted control. |
| Low | Editorial, maintainability, or proof-organization improvement. | Backlog with rationale. |

Allowed dispositions are `accept`, `accept_with_narrowing`, `revise`, `block`,
or `reject_finding_with_reason`. Silence is not acceptance.

## Required response record

For every finding provide: finding ID, severity, exact file/theorem/line or
record, claim challenged, assumption or counterexample, artifacts inspected,
recommended disposition, suggested regression or theorem, residual if not
fixed, and attribution boundary. End with overall adequacy limits and explicit
non-claims. Route the result through the external-review intake schema.

## Non-claims

- Packet readiness is not independent review.
- A review response is not automatically proof, runtime evidence, or support.
- Formal adequacy would not establish deployed enforcement, log completeness,
  empirical validity, model quality, safety, or ASI.
