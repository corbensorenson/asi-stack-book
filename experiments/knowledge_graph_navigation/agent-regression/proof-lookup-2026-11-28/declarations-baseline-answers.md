# PD1

For an event with `event.kind = AuthorityTransactionEventKind.injectSecret`, accepted by `ApplyAuthorityTransactionEvent state event = some next`, the proposition requires the prior stage `state.stage = AuthorityTransactionStage.leased` and the subsequent stage `next.stage = AuthorityTransactionStage.injected`. The modeled actor is the transaction's kernel: `event.actorId = state.kernelId`. Its three Boolean requirements are `event.contextScoped = true`, `event.boundaryMediated = true`, and `event.substitutionAuthorized = true`. Its time inequality is the strict `event.observedNow < state.expiresAt`.

Decision and scope: acceptance entails those conditions within the modeled transaction. It cannot establish coverage of a deployed sensor; sensor coverage is explicitly outside the proposition and remains unresolved by this declaration.

Exact citation: [accepted_secret_injection_is_scoped_mediated_and_preexpiry](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#accepted_secret_injection_is_scoped_mediated_and_preexpiry), declaration at [SecurityKernel.lean, line 817, commit da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/SecurityKernel.lean#L817).

# PD2

Decision: an equal-cost eligible, listed alternative is consistent with the proposition. The proposition neither rules out ties nor forces a unique minimum, and it specifies no tie-breaking rule. Its conclusion is non-strict:

```lean
selected.cost.total ≤ candidate.cost.total
```

The selection hypothesis is `SelectMinimumEligible candidates = some selected`. For each comparison route `candidate`, the hypotheses are `candidate ∈ candidates` and `RouteEligible candidate`. Thus the conclusion holds for every eligible member of that same candidate list. Equality satisfies the inequality regardless of whether the comparison route differs from the selected route.

Scope: this is a minimum of modeled total cost under those hypotheses; measured production cost remains open. The declaration alone does not resolve which tied candidate the implementation chooses.

Exact citation: [selected_route_has_minimum_modeled_cost](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#selected_route_has_minimum_modeled_cost), declaration at [Efficiency.lean, line 175, commit da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/Efficiency.lean#L175).

# PD3

The participation declaration receives a classifier `classify : ParticipationSignals -> Bool`. It rejects the universal guarantee that its output matches `RepresentativeEnough c` for every `c : RepresentationCase`:

```lean
Not (forall c : RepresentationCase,
  classify c.signals = RepresentativeEnough c)
```

The commitment declaration receives a classifier `classify : CommitmentSignals -> Bool`. It rejects the universal guarantee that its output matches `EffectiveEnforcement c` for every `c : EnforcementCase`:

```lean
Not (forall c : EnforcementCase,
  classify c.signals = EffectiveEnforcement c)
```

Decision and scope: each declaration excludes perfect recovery across all encoded cases by any classifier restricted to its respective signal type. The participation export explains that identical signals can hide different representation states; the commitment export likewise limits its conclusion to modeled commitment signals and encoded enforcement cases. These are finite-model limitations, not determinations of any actual institution's representation or enforcement outcome. They also do not assert that a classifier fails on every case.

A reviewer still needs evidence of actual representation and effective enforcement, together with justification that the modeled signals, cases, and predicates correspond to the institution being assessed. Neither declaration supplies those empirical outcomes; they remain unresolved here.

Exact citations: [participation_signals_cannot_recover_representation](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#participation_signals_cannot_recover_representation), declaration at [InstitutionalLegitimacyReview.lean, line 442](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/InstitutionalLegitimacyReview.lean#L442); [commitment_signals_cannot_recover_effective_enforcement](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#commitment_signals_cannot_recover_effective_enforcement), declaration at [InstitutionalLegitimacyReview.lean, line 463](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/InstitutionalLegitimacyReview.lean#L463). Both declarations are pinned to commit `da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa`.

# PD4

Decision: `circle_public_consumer_gate_missing_mutation_control_rejected` settles this fixture. Its antecedent is the disjunction

```lean
fixture.digestMismatchRejected = false ∨
  fixture.missingTheoremRejected = false ∨
    fixture.staleContractRejected = false ∨
      fixture.unsupportedTransferRejected = false
```

The specified `unsupportedTransferRejected = false` satisfies its final disjunct, so the conclusion is `¬ CirclePublicConsumerGateAccepted fixture`, regardless of the other rejection flags.

The other proposition, `circle_public_consumer_gate_promotion_overclaim_rejected`, requires at least one of `upwardTransitionCreated`, `chapterCorePromoted`, or `deployedTransportClaimed` to equal `true`. With all three flags false, its antecedent is false. That implication supplies no rejection conclusion for this case and does not establish acceptance either.

Scope: these propositions constrain acceptance of the finite fixture. Fixture flags cannot establish that the mutation trials actually ran. The export explicitly identifies execution of the four mutation trials as a separate observation; evidence of that execution remains unresolved here.

Exact citations: [circle_public_consumer_gate_missing_mutation_control_rejected](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_missing_mutation_control_rejected), declaration at [ProofCarryingContracts.lean, line 293](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/ProofCarryingContracts.lean#L293); [circle_public_consumer_gate_promotion_overclaim_rejected](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_promotion_overclaim_rejected), declaration at [ProofCarryingContracts.lean, line 270](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/ProofCarryingContracts.lean#L270). Both declarations are pinned to commit `da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa`.
