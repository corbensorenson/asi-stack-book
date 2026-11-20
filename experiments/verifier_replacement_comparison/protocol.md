# Offline comparison of verifier replacement decisions

Protocol date 2026-11-20. The underlying verifier is a small text classifier
that either clears a draft for ordinary review or sends it for specialist
review. Clearing never publishes. This experiment uses authored training
and test cases to make the distinction between a model score and a rollout
decision observable without network calls, Docker, or deployment.

## Fixed questions

1. Do the trained verifiers differ on ordinary cases and on a protected
   set that requires specialist review? Report the complete paired decisions
   and old-correct/new-wrong counts by scope.
2. Do competent conventional rollout controls and an identity-bound handoff
   produce the same decisions with the same observations? Count wrong
   promotions, wrong holds, evidence inspections and extra handoff writes.
   Report the scopes where the old verifier is ineligible as fallback.

## Inputs and admission rule

Train the prior and update classifiers with ordinary multinomial naive
Bayes and Laplace smoothing. Use the fixture's exact strings and lowercased
alphabetical tokens. The update adds the fixture's update training rows.
The evaluation file supplies the same 24 authored cases to both versions.
The scoring rule uses labels only after prediction. A tie routes to review.
Report machine counts as observations of this finite synthetic workload.

Run every observation profile with each exact scope. Each profile has two
decisions. Tick 0 uses its stated observation, and tick 1 repeats the
decision. The recovery profile supplies fresh evidence at tick 1. The
same regression data, release identity, versioned grant, monitor, old
fallback qualification and separate reviewer record are available to
both arms at each tick through the same evidence store. Promotion needs
complete current evidence for the target release and scope, positive held
case count, candidate accuracy at least as high as prior accuracy, zero
protected negative flips, a fresh qualified fallback, and a distinct
reviewer for a verifier change. The same review authority is required in
both arms. If fallback expires on hold, route to the declared specialist.

- **Conventional rollout.** Resolve evidence by exact identifiers using a
  versioned rollout bundle and check the rule in policy code. Record one
  decision for each review request.
- **Bound handoff.** Use the same current evidence to resolve and retain
  one scoped qualification record. Reuse it while every evidence identity,
  record revision and dependency is current. An update invalidates reuse.
  Apply the same admission rule and record one decision per request.

Both arms receive one evidence revision index lookup at each decision.
Count evidence document reads on initial evaluation and every refresh.
Count optional cache writes and policy evaluations separately. Decision
records and source document creation are common costs. Instrumentation
does not measure human time, real system latency, production incidents,
or the cost of building and operating either implementation. Ordinary
release management can retain an equivalent versioned qualification.

Authored outcome rules in the fixture supply the independent promotion
and fallback expectations. Keep every planned case. If calibration
cannot show one allowed clean scope, one protected regression, one
recovery, and one stale fallback, label the run as an instrument failure.
Freeze the protocol, cases and runner before opening outcomes. A rerun
must reproduce the same output. This is a governance comparison in an
offline synthetic verifier workload and cannot support a general model,
adoption, safety, or superiority claim.
