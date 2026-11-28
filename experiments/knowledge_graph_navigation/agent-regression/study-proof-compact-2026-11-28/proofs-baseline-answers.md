## LP1

Each assertion independently suffices for rejection: `fixture.upwardTransitionCreated = true`, `fixture.chapterCorePromoted = true`, or `fixture.deployedTransportClaimed = true`. The conclusion is `¬ CirclePublicConsumerGateAccepted fixture` for that finite fixture. The actual deployment status of Circle transport remains unresolved by this statement. [Circle public consumer gate declaration](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_promotion_overclaim_rejected)

## LP2

The premise is `SelectMinimumEligible candidates = some selected`. It yields both `selected ∈ candidates` and `RouteEligible selected`. This is a guarantee conditional on a successful return. Existence of a successful selection for every input list is outside its scope. [Listed eligible candidate declaration](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#selected_route_is_a_listed_eligible_candidate)

## LP3

No. Given `jurisdiction ≠ m.jurisdictionId`, the theorem concludes `¬ MandateUseAllowed m m.authorityId jurisdiction tick`. The negative conclusion applies to use of this mandate in the distinct jurisdiction with its own authority ID, for any modeled `tick`. It is scoped to the modeled permission predicate for that mandate. [Distinct jurisdiction declaration](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#local_mandate_cannot_authorize_distinct_jurisdiction)

## LP4

The Boolean classifier sees only `c.signals : ProviderSignals` for each modeled `PopulationCase`. For every classifier of type `ProviderSignals → Bool`, the theorem rules out `∀ c : PopulationCase, classify c.signals = PopulationResilient c`. Each such classifier misses at least one modeled case. [Provider signals declaration](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#provider_signals_cannot_recover_population_resilience)

A real-population review still needs empirical evidence beyond provider telemetry about the affected people, copied artifacts, and other institutions. The reviewer would track resistance and absorption, service continuity and restoration, harmed-party recovery and remedy, public correction, adaptation, and unresolved harm across the affected paths. [Societal resilience core claim](https://corbensorenson.github.io/asi-stack-book/chapters/societal-resilience-and-misuse-defense.html#core-claim)
