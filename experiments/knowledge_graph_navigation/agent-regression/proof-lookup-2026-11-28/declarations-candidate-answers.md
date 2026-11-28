# PD1

For `event.kind = AuthorityTransactionEventKind.injectSecret` and acceptance `ApplyAuthorityTransactionEvent state event = some next`, the proposition requires the prior stage `state.stage = AuthorityTransactionStage.leased` and the resulting stage `next.stage = AuthorityTransactionStage.injected`. The modeled actor is the kernel: `event.actorId = state.kernelId`. The three Boolean conditions are `event.contextScoped = true`, `event.boundaryMediated = true`, and `event.substitutionAuthorized = true`. The time inequality is `event.observedNow < state.expiresAt`.

Acceptance establishes those conditions within the modeled transaction. It cannot establish coverage of a deployed sensor; sensor coverage is outside the proposition and needs separate observational evidence.

Exact citation: [accepted_secret_injection_is_scoped_mediated_and_preexpiry](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#accepted_secret_injection_is_scoped_mediated_and_preexpiry), with [pinned Lean declaration, SecurityKernel.lean L817](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/SecurityKernel.lean#L817).

# PD2

The minimum-cost proposition permits the tie. It neither forces a unique winner nor specifies how ties are broken. Its inequality is `selected.cost.total ≤ candidate.cost.total`; equality satisfies it.

The selection hypothesis is `SelectMinimumEligible candidates = some selected`. For every comparison route `candidate`, the comparison requires both `candidate ∈ candidates` and `RouteEligible candidate`. Thus the guarantee is minimum modeled total cost among eligible members of that same finite list. It does not establish measured production cost or optimality over unlisted routes.

Exact citation: [selected_route_has_minimum_modeled_cost](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#selected_route_has_minimum_modeled_cost), with [pinned Lean declaration, Efficiency.lean L175](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/Efficiency.lean#L175).

# PD3

The participation declaration takes `classify : ParticipationSignals -> Bool`. For a `RepresentationCase` it would have to match `RepresentativeEnough c`, but rejects the universal guarantee `forall c : RepresentationCase, classify c.signals = RepresentativeEnough c`: the declaration concludes `Not` of that statement. Identical participation signals can conceal different modeled representation states.

The commitment declaration takes `classify : CommitmentSignals -> Bool`. For an `EnforcementCase` it would have to match `EffectiveEnforcement c`, but rejects the universal guarantee `forall c : EnforcementCase, classify c.signals = EffectiveEnforcement c`, again by concluding `Not` of that statement. Modeled commitment signals cannot recover effective enforcement in every encoded case.

These are negative results about classifiers limited to their respective signals in finite models. They do not show that every individual classification is wrong. A reviewer still needs independent evidence about actual lawful authority, representativeness, enforcement efficacy, remedy, public legitimacy, geopolitical stability, and safety; these declarations establish none of those institutional outcomes.

Exact citations: [participation_signals_cannot_recover_representation](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#participation_signals_cannot_recover_representation), with [pinned InstitutionalLegitimacyReview.lean L442](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/InstitutionalLegitimacyReview.lean#L442); and [commitment_signals_cannot_recover_effective_enforcement](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#commitment_signals_cannot_recover_effective_enforcement), with [pinned InstitutionalLegitimacyReview.lean L463](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/InstitutionalLegitimacyReview.lean#L463). Both exports also cite the institutional-outcomes scope passage at [what the current work can establish](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-08-institutions-coordination-and-societal-resilience.html#what-the-current-work-can-establish).

# PD4

`circle_public_consumer_gate_missing_mutation_control_rejected` settles this case: `fixture.unsupportedTransferRejected = false` satisfies the fourth disjunct of its antecedent, so it concludes `¬ CirclePublicConsumerGateAccepted fixture`. The other disjuncts test whether `digestMismatchRejected`, `missingTheoremRejected`, or `staleContractRejected` is false; their values are unnecessary for this conclusion.

`circle_public_consumer_gate_promotion_overclaim_rejected` requires at least one of `upwardTransitionCreated = true`, `chapterCorePromoted = true`, or `deployedTransportClaimed = true`. All three are false here, so its antecedent does not hold. That implication cannot settle this case or establish acceptance from the absence of promotion flags.

The result concerns the finite fixture acceptance contract. Fixture flags cannot establish that the four mutation trials actually ran; execution remains a separate observation requiring run evidence.

Exact citations: [circle_public_consumer_gate_missing_mutation_control_rejected](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_missing_mutation_control_rejected), with [pinned ProofCarryingContracts.lean L293](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/ProofCarryingContracts.lean#L293); and [circle_public_consumer_gate_promotion_overclaim_rejected](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_promotion_overclaim_rejected), with [pinned ProofCarryingContracts.lean L270](https://github.com/corbensorenson/asi-stack-book/blob/9f84414daa945f96077b962fc882b3fa3dd172d4/lean/AsiStackProofs/ProofCarryingContracts.lean#L270).
