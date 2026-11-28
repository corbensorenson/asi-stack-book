# PA1

**Decision:** Service restoration alone does not justify closing the incident or claiming population recovery. Harmed-party recovery, including whether promised remedies were actually delivered, must remain distinct from service recovery. The chapter's worked dossier records containment, service recovery, and harmed-party recovery as observed while all three enumerated incident paths remain open; an owned residual and recurrence plan are still necessary. A still-needed remedy therefore cannot be erased by a green provider dashboard. The exact sufficient closure predicate was not recovered within the open limit.

**Application citation and scope:** [Societal Resilience and Misuse Defense, §17.7.1, “Worked incident boundary: the service is restored, three paths remain”](https://corbensorenson.github.io/asi-stack-book/chapters/societal-resilience-and-misuse-defense.html#worked-incident-boundary-the-service-is-restored-three-paths-remain). This is an authored finite dossier: closure is proved only over enumerated paths, promised remedies must be counted separately from observed delivery, and unreachable people remain a coverage uncertainty.

**Exact declaration:** [SocietalResilienceReview.lean, L450, pinned commit da9bd7c](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/SocietalResilienceReview.lean#L450):

```lean
theorem provider_signals_cannot_recover_population_resilience
    (classify : ProviderSignals -> Bool) :
    Not (forall c : PopulationCase, classify c.signals = PopulationResilient c)
```

Every classifier using only those provider signals fails on at least one modeled population case. The chapter explains the collision: identical provider signals can accompany opposite population-recovery states. This establishes insufficiency in the authored model, not an empirical impossibility theorem about every real provider or population.

# PA2

**Decision:** Acceptance of the modeled secret injection does not establish that a controller sensed oscillation or stopped because of it. A stop record can establish a recorded stop; an available trace can support only observations actually captured by its instruments. Neither fact alone identifies the cause of the stop.

**Exact Lean boundary:** [SecurityKernel.lean, L817, `accepted_secret_injection_is_scoped_mediated_and_preexpiry`](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/SecurityKernel.lean#L817). Given `event.kind = AuthorityTransactionEventKind.injectSecret` and `ApplyAuthorityTransactionEvent state event = some next`, its conclusion is:

```lean
state.stage = AuthorityTransactionStage.leased ∧
  event.actorId = state.kernelId ∧
  event.contextScoped = true ∧
  event.boundaryMediated = true ∧
  event.substitutionAuthorized = true ∧
  event.observedNow < state.expiresAt ∧
  next.stage = AuthorityTransactionStage.injected
```

The [declaration export](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#accepted_secret_injection_is_scoped_mediated_and_preexpiry) explicitly places sensor coverage outside this proposition. It proves modeled transaction conditions, not detection, causal attribution, or deployed safety.

**Evidence needed / reviewer disposition:** A causal claim would require an instrument capable of observing the alleged oscillation, a trace tying that observation to the controller's detection and stop decision, and a comparison or intervention that distinguishes detection from alternative stop causes. If the decisive instrument was absent, withhold the causal release claim, record the missing observation, and obtain an instrumented replay or further evidence. These are reviewer recommendations inferred from the proof boundary; the requested controller-specific application passage was not located.

**Related application guidance actually recovered:** [Perception, Sensor Fusion, and Observation Trust](https://corbensorenson.github.io/asi-stack-book/chapters/perception-sensor-fusion-and-observation-trust.html), paragraph beginning “The first claim-bearing campaign”: use independent ground truth, frozen faults and positive controls; a failed positive control or inactive route makes a null result instrument-inadequate. This supports treating inadequate instrumentation as an evidence limitation, but does not resolve the missing controller-specific guidance or establish what any particular stop event contained.

# PA3

**Decision:** The consumer cannot yet use the receipt. A finite theorem and matching fingerprint leave replay state and expiry unresolved. The chapter's “Operational rule” requires resolution of theorem identity, assumptions, source and toolchain, fingerprints, replay state, expiry, and non-claims before use. See [Circle Calculus and Proof-Carrying AI Contracts, Operational rule and adjoining proof-authority discussion](https://corbensorenson.github.io/asi-stack-book/chapters/circle-calculus-and-proof-carrying-ai-contracts.html).

**Exact consumer-gate declaration:** [ProofCarryingContracts.lean, L270](https://github.com/corbensorenson/asi-stack-book/blob/da9bd7cd2ae33b7935a7e67047b2cd054e11d8aa/lean/AsiStackProofs/ProofCarryingContracts.lean#L270):

```lean
theorem circle_public_consumer_gate_promotion_overclaim_rejected
    {fixture : CirclePublicConsumerGateFixture} :
    (fixture.upwardTransitionCreated = true ∨
      fixture.chapterCorePromoted = true ∨
        fixture.deployedTransportClaimed = true) ->
    ¬ CirclePublicConsumerGateAccepted fixture
```

**Scope and additional justification:** This rejects those three overclaims in the finite fixture; it does not itself prove better model behavior or directly encode the chapter's entire operational rule. The chapter separates structural proof authority from consumer authority: model-quality and operational claims need separately justified workloads, baselines, metrics, and evidence artifacts. Resolving replay and expiry would address receipt readiness, but would still leave empirical behavior improvement to be demonstrated in the relevant workload and comparison.

# PA4

**Decision:** A cheaper route that fails quality is not a counterexample. The selector's minimum is conditional on eligibility: the selected route is listed and eligible, and its complete modeled seven-class total is no greater than that of every eligible authored candidate. A failed-quality candidate is outside that comparison. The other cheaper countermodel named by the Reader is an **unauthorized route**.

**Citations and formal scope:** [Human Reader, Unit 2, paragraph beginning “The finite AsiStackProofs.Efficiency model”](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-02-the-efficient-asi-hypothesis.html) names both cheaper unauthorized and failed-quality countermodels. [The Efficient ASI Hypothesis, “Finite minimum selector” and adjoining formal-responsibility discussion](https://corbensorenson.github.io/asi-stack-book/chapters/the-efficient-asi-hypothesis.html) states the eligibility-conditioned minimum and limits it to authored candidates and declared costs. The exact Lean declaration, identifier, source line, and eligibility definition were not recovered; the relevant condition above is the chapter's description of the Lean guarantee, not a quotation of Lean syntax.

**Production saving:** The finite guarantee leaves candidate-search completeness and the empirical truth of cost and quality declarations open. A production claim needs a matched task contract and authority ceiling, measured preservation of quality, and actual total costs that include verification, fallback, review, repair, and recovery. The Reader's opening cached-answer example shows why fewer calls and lower accelerator time alone can hide later repair costs; its route-ledger paragraph calls for predicted and actual costs, rejected alternatives, verification, fallback, residuals, and final disposition. The canonical chapter explicitly leaves measured efficiency, cost-estimate accuracy, and model quality unresolved by its finite selector and synthetic probe.
