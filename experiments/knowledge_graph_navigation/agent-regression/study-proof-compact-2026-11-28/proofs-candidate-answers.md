## LP1

Any one of `fixture.upwardTransitionCreated = true`, `fixture.chapterCorePromoted = true`, or `fixture.deployedTransportClaimed = true` is enough to conclude `¬ CirclePublicConsumerGateAccepted fixture`. This establishes rejection under the finite fixture acceptance contract. The actual deployment status of Circle transport requires separate operational evidence. [Circle public consumer gate declaration](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_promotion_overclaim_rejected)

## LP2

The premise is `SelectMinimumEligible candidates = some selected`. It follows that `selected ∈ candidates` and `RouteEligible selected`. The result is conditional on a successful selection. For example, on an empty list no successful selection could satisfy the membership conclusion. [Selected route declaration](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#selected_route_is_a_listed_eligible_candidate)

## LP3

No. The premise is `jurisdiction ≠ m.jurisdictionId`. For any `tick`, the conclusion is `¬ MandateUseAllowed m m.authorityId jurisdiction tick`. It concerns modeled use of this mandate in the different jurisdiction with the mandate’s own authority identity. [Local mandate declaration](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#local_mandate_cannot_authorize_distinct_jurisdiction)

## LP4

The classifier is a function `classify : ProviderSignals → Bool` and sees only `c.signals` from each modeled `PopulationCase`. For every such classifier, `∀ c : PopulationCase, classify c.signals = PopulationResilient c` is false. Each classifier must miss at least one modeled resilience state. [Provider signals declaration](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#provider_signals_cannot_recover_population_resilience)

For a real population, a reviewer would still need empirical evidence beyond provider signals, including what happened to affected people and institutions, whether services continued or recovered, whether people received correction and remedy, and what harm remained unresolved. [Societal Resilience and Misuse Defense, Core Claim](https://corbensorenson.github.io/asi-stack-book/chapters/societal-resilience-and-misuse-defense.html#core-claim)
