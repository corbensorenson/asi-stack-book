# Claim-Bearing Experiment Competence and False-Negative Standard

Status: active governing contract  
Authority: Corben Sorenson  
Effective: 2026-07-17  
Roadmap owner: `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`

## Purpose

This contract prevents weak implementations, naive tests, underpowered designs,
bad proxies, evaluator defects, and immature task regimes from being converted
into negative evidence about an ASI Stack idea. A prospective falsifier is
necessary but not sufficient. The experiment must also demonstrate that it
implemented the intended mechanism competently and had a realistic chance to
detect the claimed effect.

Perfection is not an operational standard: no finite experiment can prove that
no better implementation exists. The enforceable replacement is **claim-
commensurate competence**. The stronger and broader the negative inference, the
more implementation maturity, construct validity, sensitivity, diversity, and
independence it requires.

## Exploration versus claim-bearing work

Exploratory prototypes, minimum viable implementations, deterministic fixtures,
tiny models, authored corpora, and sacrificial preflights remain useful for
debugging and mechanism discovery. They may establish that a particular object
was built, a route is reachable, a schema is coherent, or an instrument is
broken. Unless they separately pass this contract, they cannot:

- refute or narrow the underlying architecture or mechanism;
- establish absence of benefit, safety, transfer, or efficiency;
- turn an implementation failure into a claim failure;
- count as a competent `blocked_after_full_attempt` disposition; or
- supply a negative premise used to strengthen another chapter claim.

An exploratory failure ends as `instrument_inadequate`,
`implementation_inadequate`, `construct_invalid`, `underpowered`, or
`inconclusive_for_claim`. It is preserved, but it is not claim evidence.

## Competence dossier required before held-out opening

Every outcome-bearing campaign must freeze a claim-specific competence dossier
before its final held-out labels or outcomes are accessed. The dossier must
contain all of the following.

### 1. Claim and mechanism identity

- one canonical claim ID and its exact atom, subclaim, alias, or proxy mapping;
- the intended mechanism, causal pathway, population, environment, and artifact;
- the precise scope a positive, null, or negative result could support;
- known alternative implementations that could behave differently; and
- a falsifier that distinguishes mechanism failure from implementation failure.

### 2. Implementation competence

- a versioned architecture and code path implementing every load-bearing
  mechanism named by the claim;
- component tests showing that each mechanism activates and changes the state it
  is supposed to change;
- a trace proving that the test actually exercised those components;
- matched engineering effort and tuning opportunity for proposed and comparator
  systems;
- a documented optimization budget, search space, selection rule, and stop rule;
- failure-free execution, stable training or optimization, and resource headroom
  adequate for the declared regime;
- an oracle, expert, or deliberately favorable upper-bound configuration when
  one can be constructed; and
- for consequential negative claims, a materially independent second
  implementation or an exact recorded reason why the result cannot rise above
  `implementation_specific`.

A system that never learns the target feature, never activates the proposed
mechanism, collapses to chance, or is dominated by an obvious implementation
defect has not tested the idea.

### 3. Construct and task validity

- a natural, non-authored corpus for empirical claims unless the claim is
  explicitly about the authored fixture itself;
- documented sampling, contamination, licensing, preprocessing, and exclusion
  policies;
- tasks whose success criterion operationalizes the claim rather than a cheap
  proxy;
- positive controls, negative controls, trivial baselines, current strong
  baselines, and mechanism ablations;
- difficulty coverage that avoids both ceiling and floor effects;
- adversarial cases that do not erase ordinary competence; and
- at least one favorable regime in which the proposed mechanism should work if
  the implementation is sound.

### 4. Evaluator competence

- syntax and semantics evaluated separately;
- calibration on cases spanning correct, incorrect, safe, unsafe, useful,
  useless, abstaining, and malformed outcomes as applicable;
- known effect injection or blinded synthetic calibration demonstrating that
  the evaluator detects the minimum effect of interest;
- independently implemented scoring for consequential outcomes;
- disagreement, false-accept, false-reject, abstention, and missing-data rates;
- evaluator access no broader than required and no hidden-label leakage; and
- a rule that evaluator failure closes claim denominators rather than creating a
  null or negative result.

### 5. Sensitivity and statistical adequacy

- a preregistered minimum effect of practical interest;
- prospective power or sensitivity analysis, including variance and attrition
  assumptions;
- enough independent units and seeds for the declared estimand;
- confidence or credible intervals and effect sizes, not only pass/fail counts;
- multiplicity, subgroup, missing-data, and stopping policies;
- robustness to reasonable metric, seed, and preprocessing choices; and
- a demonstrated ability to distinguish “no meaningful effect” from “not enough
  information.”

### 6. Fair rescue ladder

Before the final held-out set is opened, the campaign must execute a finite,
prospectively frozen rescue ladder designed to make the idea succeed:

1. repair component and data-pipeline failures;
2. verify mechanism activation and gradients, state changes, or causal handles;
3. test an oracle or favorable upper bound;
4. tune within the frozen development budget;
5. test at least one competent alternative implementation for consequential
   negative claims;
6. verify that strong baselines and positive controls behave as expected; and
7. pass all implementation, evaluator, construct, and sensitivity gates.

Rescue work uses development or sacrificial data only. Once the final held-out
denominator is opened, outcome-aware repair, arm expansion, metric swapping,
label inspection, and unregistered retry are forbidden. A failed competence
gate returns the campaign to instrument or implementation development; it does
not count as a claim attempt.

## Negative-inference ladder

Every negative outcome must be assigned exactly one level.

| Level | Meaning | Maximum allowed inference |
|---|---|---|
| N0 — Instrument failure | Generator, parser, evaluator, harness, or denominator is invalid. | No claim inference. |
| N1 — Implementation failure | The tested system is incomplete, unstable, chance-level, or fails competence gates. | This implementation is inadequate; the idea remains untested. |
| N2 — Proxy or regime failure | The implementation is competent but the task/corpus/metric does not adequately instantiate the target claim. | The proxy result is retained; no target-claim refutation. |
| N3 — Exact implementation result | A competent frozen implementation fails in one valid bounded setting. | Refutes or narrows only that implementation-setting claim identity. |
| N4 — Mechanism-level counterevidence | Multiple competent implementations, mechanism-positive controls, strong matched baselines, and valid tasks show the predicted mechanism effect is absent or reversed. | Bounded mechanism narrowing or refutation. |
| N5 — Broad claim refutation | N4 plus natural diverse corpora, at least two materially different transfer settings, adequate power, independent reproduction, and no surviving preregistered rescue. | Broad refutation only within the explicit sampled envelope. |

`Refuted` without an N-level, competence dossier, and scope-specific canonical
claim identity is invalid. A universal claim can be defeated by one genuine
counterexample, but the counterexample must still be real: the implementation
and test must satisfy the claim's antecedents rather than a degraded proxy.

## Current-result rehabilitation

All existing negative, narrowed, no-change, and
`blocked_after_full_attempt` records predate this contract. They remain
immutable historical outcomes, but none may be used for a broader negative
inference until a retrospective competence audit assigns N0–N5.

The KERC broad-efficiency record is provisionally bounded to the frozen linear
cores, authored 192-record corpus, absent adversarial-polarity training class,
jointly authored compiler/verifier, 0.5 task performance, uncalibrated energy,
and exact packet accounting. Until rehabilitation, it is evidence that this
implementation/corpus failed its frozen gate—not that Kernel English, learned
cognitive compilers, hierarchical residuals, or the broader architecture fail.
An improved implementation receives a new claim identity and prospective
protocol; it does not overwrite the historical result.

## Completion gate

A negative result may move or narrow a claim only when:

- its canonical claim mapping resolves;
- every required competence field passes before held-out opening;
- the raw failure, rescue, calibration, tuning, cost, and exclusion records are
  retained;
- the assigned N-level matches the actual implementation and evidence breadth;
- a validator rejects competence-field deletion, scope widening, held-out retry,
  positive-control failure, underpower laundering, evaluator leakage, and
  implementation-to-architecture generalization; and
- chapter prose, Appendix C, transition records, the non-core ledger, synopsis,
  and public status use the same bounded language.

This contract does not guarantee that an experiment is perfect. It guarantees
that weak tests fail closed as weak tests instead of becoming false scientific
conclusions.
