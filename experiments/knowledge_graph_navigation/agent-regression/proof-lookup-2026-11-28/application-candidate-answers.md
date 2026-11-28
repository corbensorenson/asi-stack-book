# PA1

Service restoration alone does not permit closure. The incident may close only when every known affected path is closed or assigned to an authorized owner as a visible residual. Thus the harmed group's outstanding remedy must either be completed or remain visibly assigned under that rule. Harmed-party recovery must remain distinct from service restoration; resistance, absorption, correction, and adaptation are also separate outcomes. See the societal-resilience chapter's [core claim and operational rule](https://corbensorenson.github.io/asi-stack-book/chapters/societal-resilience-and-misuse-defense.html#core-claim).

The exact declaration [provider_signals_cannot_recover_population_resilience](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#provider_signals_cannot_recover_population_resilience) states:

```lean
theorem provider_signals_cannot_recover_population_resilience
    (classify : ProviderSignals -> Bool) :
    Not (forall c : PopulationCase, classify c.signals = PopulationResilient c)
```

For the authored population cases, every classifier using only provider signals misses at least one modeled resilience state. Provider status therefore cannot establish population recovery. This is a finite modeled information boundary, not a measurement that this particular harmed group has recovered. [Pinned Lean source, SocietalResilienceReview.lean:450](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/SocietalResilienceReview.lean#L450).

# PA2

Comparing the release note with the stop event and available sensor trace can support the observed sequence. It does not by itself establish that safe oscillation detection caused the stop. That causal claim needs a different observation establishing what actually triggered the stop. If the decisive instrument was missing, the reviewer must keep the causal question open. This is the Reader's explicit [application guidance, “Verification Starts with Obligations”](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-15-verification-bandwidth-claim-ledgers-and-proof.html#verification-starts-with-obligations).

The Lean boundary is [accepted_secret_injection_is_scoped_mediated_and_preexpiry](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#accepted_secret_injection_is_scoped_mediated_and_preexpiry), [SecurityKernel.lean:817](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/SecurityKernel.lean#L817). Given `event.kind = AuthorityTransactionEventKind.injectSecret` and `ApplyAuthorityTransactionEvent state event = some next`, it entails a leased prior stage, the kernel actor, context scoping, boundary mediation, authorized substitution, `event.observedNow < state.expiresAt`, and an injected next stage. Sensor coverage is outside the proposition. Acceptance therefore supplies no proof of oscillation detection, stop causation, or the release note's safety claim; those remain unresolved without the relevant observations.

# PA3

No. A finite theorem and matching fingerprint do not yet authorize use of the receipt while replay state and expiry remain unresolved. The chapter's [core operational rule](https://corbensorenson.github.io/asi-stack-book/chapters/circle-calculus-and-proof-carrying-ai-contracts.html#core-claim) requires resolving theorem identity, assumptions, source and toolchain, fingerprints, replay state, expiry, and non-claims before use. Every empirical or operational decision derived from the formal fact needs separate justification. Claiming better model behavior therefore requires empirical evidence supporting that particular improvement, together with justification that it applies to the intended setting; the finite theorem alone does not supply it.

An exact consumer-gate declaration is [circle_public_consumer_gate_missing_mutation_control_rejected](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_missing_mutation_control_rejected):

```lean
theorem circle_public_consumer_gate_missing_mutation_control_rejected
    {fixture : CirclePublicConsumerGateFixture} :
    (fixture.digestMismatchRejected = false ∨
      fixture.missingTheoremRejected = false ∨
        fixture.staleContractRejected = false ∨
          fixture.unsupportedTransferRejected = false) ->
    ¬ CirclePublicConsumerGateAccepted fixture
```

Its scope is rejection of a finite fixture when any listed mutation-control flag is false; actual execution of the four mutation trials is a separate observation. It does not establish improved model behavior. [Pinned Lean source, ProofCarryingContracts.lean:293](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/ProofCarryingContracts.lean#L293).

# PA4

No. A cheaper route that fails quality is outside the eligible alternatives covered by the guarantee. The exact condition in [selected_route_has_minimum_modeled_cost](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#selected_route_has_minimum_modeled_cost) is:

```lean
(selection : SelectMinimumEligible candidates = some selected) :
∀ candidate, candidate ∈ candidates → RouteEligible candidate →
  selected.cost.total ≤ candidate.cost.total
```

The alternative must belong to the same candidate list and satisfy `RouteEligible`; the conclusion compares declared modeled totals. [Pinned Lean source, Efficiency.lean:175](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/Efficiency.lean#L175).

The Reader explicitly names both cheaper failed-quality and cheaper **unauthorized** countermodels. It limits the result to authored finite candidates and declared costs, and says the artifacts do not establish complete search, accurate costs, calibrated quality, measured efficiency, useful output, natural workloads, deployment, reproduction, or transfer. See [“What the Current Work Establishes,” §2.18](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-02-the-efficient-asi-hypothesis.html#what-the-current-work-establishes).

Accordingly, a production-saving claim still needs a measured comparison on the intended production workload, showing lower actual cost for useful, quality-qualified, authorized work under comparable requirements, with evidence that the model's costs and quality criteria apply there. That is an empirical requirement inferred from the stated limits; the finite selector theorem does not establish such a saving.
