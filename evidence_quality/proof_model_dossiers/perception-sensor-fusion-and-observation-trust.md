# Proof-model dossier: perception-sensor-fusion-and-observation-trust

This dossier records bounded dependence accounting and observation-record
custody. It is proof accounting, not sensor evidence or a support transition.

## Targets

| Target | Semantic role | Current disposition |
|---|---|---|
| `lean:perception.correlated_agreement_no_independent_promotion` | Universal finite pair classification plus correlated, independent, and disagreement witnesses | Retain as a narrow evidence-accounting theorem |
| `lean:perception.observation_review_lifecycle` | Reachable identity, dependence, pair-review, use, handoff, and invalidation discipline | Retain as a bounded lifecycle refinement |

## Current model

`AsiStackProofs.ObservationTrust` defines channel records containing a
hypothesis, declared dependence root, freshness, calibration, lineage, and
clock/pose status. A universal classifier returns inadmissible, disagreement,
correlated agreement, or independent agreement. Under its explicit
assumptions, same-root agreement has independent-evidence count one,
distinct-root agreement has count two, and differing hypotheses remain
disagreement. Concrete witnesses establish that all three branches are
reachable.

The module also defines seven stages: captured, identities bound, dependence
bound, pair reviewed, use bound, handed off, and invalidated. Six accepted
transitions preserve exact observation, channel-set, calibration, clock/pose,
dependence, hypothesis, consumer, residual, protocol, pair-classification, and
evidence-count identity. Total step/run semantics extend those properties to
arbitrary accepted finite runs, add exact receipt accounting, extract valid
traces, compose across event batches, preserve rejected state, and make
invalidation terminal for every modeled event and nonempty suffix. A correlated
pair cannot satisfy a two-item use request, and accepted events do not change
support-assignment or external-authority counters.

A separate finite dependence model distinguishes a pairwise root summary from
the global common-cause state. Two cases have the same distinct-root pair and
opposite global-independence decisions. The resulting universal impossibility
theorem establishes that no classifier over the root pair alone is exact for
every modeled case. It does not discover causal structure or validate any root.

The independently encoded consumer is
`scripts/validate_observation_trust.py`. It reproduces the three pair branches
and complete lifecycle, recompiles the exact 32-theorem surface, checks all
seven prefix/suffix compositions, rejects 46 wrong-stage, identity, replay,
custody, count-inflation, disagreement, use, handoff, and invalidation mutations
with exact state preservation, passes 13 pair-classification controls, rejects
all six event kinds after invalidation, and reconstructs twelve
same-summary/opposite-common-cause controls.

## Exact boundary

The model assumes that channel eligibility fields, dependence roots,
hypotheses, digests, classification, counts, common-cause review, authority
bounds, expiry, fallback, residual ownership, independent review, and material
change records are truthful. It does not discover real dependence, establish
calibration or synchronization, identify environmental truth, detect spoofing
or corruption, measure fusion quality, prove causal grounding, validate an
evaluator, authorize physical action, establish robustness or safety, or
support claims about AGI or ASI.

Those outcomes remain assigned to the chapter's natural and adversarial sensor
campaign and Project Theseus integration. The formal increment has
`support_state_effect=none`; chapter support remains `argument`.
