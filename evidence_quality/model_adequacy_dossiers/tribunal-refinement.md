# Model-adequacy dossier: Tribunal refinement

## Ownership

- Chapter: `spinoza-verification-and-proof-carrying-claims`
- Frozen targets: both `lean:tribunal.review.*` targets
- Stronger model: `lean/AsiStackProofs/TribunalRefinement.lean`
- Independent consumer: `scripts/validate_tribunal_refinement.py`
- Result: `experiments/tribunal_refinement/results/2026-07-15-local.json`
- Support-state effect: exactly `none`

## Reachable model

The model owns arbitrary finite lists of case-specific Tribunal events from
review request through versioned dossier/evidence binding, bounded panel
execution, verdict issue, consumer acknowledgment, and appeal resolution. It represents panel methods,
independence groups, shared-evidence risk, falsification, abstention, veto,
dissent, changed-evidence reuse, actions, constraints, residuals, appeal,
support-owner handoff, and consumer custody without treating any field as proof
of reviewer competence or verdict truth.

## Consequences, countermodels, and consumer

Nineteen exact declarations preserve all ten represented case, target,
evidence, dossier, panel, policy, consumer, and verdict-version identities and
prevent changes to support-assignment or external-effect counts across every
finite event list. Rejected events preserve exact state, accepted steps advance
and add exactly one receipt, event batches compose, and appeal-resolved states
absorb every suffix. Countermodels reject case,
evidence, verdict, and event substitution; missing review, dossier, evidence,
probe, panel size, independence graph, shared-evidence disclosure,
falsification, abstention, veto, dissent, actions, constraints, residual,
appeal, owner handoff, or consumer acknowledgment; changed-evidence reuse;
default approval; unresolved appeal; and authority leakage. A six-event witness
reaches appeal resolution with zero assigned support and zero external effects.

The independent consumer recompiles the exact nineteen-theorem surface, covers
all twenty-eight routes, consumes the exact 3/5 tribunal-review fixtures and
1/11 method-independence lifecycle, and rejects 45 mutations across those
boundaries, including an explicit action-required packet whose verdict label is
otherwise non-action-bearing.

## Assumptions, exclusions, and adequacy verdict

Identifiers, digests, evidence-version facts, method labels, reviewer and
independence-group counts, graph acyclicity, shared-evidence disclosure,
falsification, abstention, veto, dissent, actions, constraints, residuals,
appeal, owner handoff, and consumer acknowledgment are trusted inputs. The
model is adequate for the exact represented finite-run lifecycle, route
priority, rejection noninterference, composition, terminal closure, versioned
custody, no-default discipline, and authority separation. It is
inadequate for reviewer competence, independence in fact, error decorrelation,
dossier completeness, evidence truth, probe efficacy, verdict correctness,
legitimacy, fairness, action or appeal quality, claim truth, evidence adequacy,
usefulness, causality, safety, costs, natural workloads, deployment,
reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.

## Disposition

Retire the two assumption-restating policy projections and eight literal route
normalizations in `AsiStackProofs.Tribunal`. Retain the three general finite
countermodels for missing probes/recorded independence, unchanged-evidence
guards, and action/constraint records. Move both public targets to the
refinement module. No support state changes.
