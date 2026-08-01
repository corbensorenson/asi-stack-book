# Proof-model dossier: inner-alignment-mesa-optimization-and-learned-objective-integrity

This dossier records the chapter's bounded formal model, independent consumer,
and exact nonclaims. It is proof accounting, not learned-objective evidence or a
support transition.

## Targets

| Target | Semantic role | Current disposition |
|---|---|---|
| `lean:inner_alignment.behavior_does_not_identify_objective` | Constructive finite non-identification result | Retain as a narrow impossibility theorem |
| `lean:inner_alignment.hypothesis_review_lifecycle` | Reachable hypothesis, evidence, use, handoff, and invalidation discipline | Retain as a bounded lifecycle refinement |

## Current model

`AsiStackProofs.LearnedObjectiveIntegrity` contains two authored policy worlds
with the same compliant observation trace, distinct objective-hypothesis labels,
and different actions under one separating opportunity. It proves that no
deterministic function of the shared trace can identify both labels correctly.
The labels are model inputs, not discovered facts about a trained system.

The module also defines eight reachable stages: scoped, hypotheses bound,
evidence bound, intervention reviewed, mitigation reviewed, use bound, handed
off, and invalidated. Seven accepted transitions preserve exact model, target,
signal-lineage, hypothesis-set, evidence-plan, use-envelope, reviewer, consumer,
residual, and protocol identity. Rejected transitions preserve the entire state.
The accepted route records one bounded handoff and one descendant invalidation
without changing support-assignment or external-authority counters.

The independently encoded consumer is
`scripts/validate_learned_objective_integrity.py`. It reproduces the
non-identification witness and accepted lifecycle, then rejects 59 wrong-stage,
identity, replay, certainty-laundering, missing-evidence, missing-control,
mitigation, use-boundary, and invalidation mutations with exact state
preservation.

## Exact boundary

The model assumes that all digests, hypothesis counts, evidence-lane presence,
competence controls, intervention sealing, opportunity relevance, positive
controls, evaluator and monitor independence, disagreement records, mitigation
outcomes, residuals, authority limits, rollback routes, reviews, and descendant
records are truthful. It does not identify an actual learned objective, detect
mesa-optimization, goal misgeneralization, deception, or gradient hacking,
establish evaluator competence, prove mitigation removal, measure false
positives or negatives, validate deployment behavior, establish alignment or
safety, authorize release, or support claims about AGI or ASI.

Those outcomes remain assigned to the chapter's competent empirical campaign
and Project Theseus integration. The formal increment has
`support_state_effect=none`; chapter support remains `argument`.
