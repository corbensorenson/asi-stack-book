# PC1

**Decision:** Reject the current fixture. A matching fingerprint and an earlier replay do not override the fresh `staleContractRejected = false` report. The deciding Lean guard is `circle_public_consumer_gate_missing_mutation_control_rejected`: if any of `digestMismatchRejected`, `missingTheoremRejected`, `staleContractRejected`, or `unsupportedTransferRejected` is false, then `¬ CirclePublicConsumerGateAccepted fixture`. The stale-contract disjunct applies directly. Acceptance requires resolving this failed control and satisfying the current gate; execution of the four mutation trials remains a separate observation. [Exact declaration and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_missing_mutation_control_rejected); [pinned Lean source, ProofCarryingContracts.lean:293](https://github.com/corbensorenson/asi-stack-book/blob/c833ed9fae198dae0580f1fcb2f5f2b46f351999/lean/AsiStackProofs/ProofCarryingContracts.lean#L293).

The chapter’s receipt rule requires the consumer to resolve theorem identity, assumptions, source and toolchain, fingerprints, replay state, expiry, and non-claims, then separately justify every empirical or operational decision drawn from the formal fact. Thus the new deployment claim needs its own current empirical and operational review; the receipt alone cannot support it. [Chapter operational rule, “Core claim”](https://corbensorenson.github.io/asi-stack-book/chapters/circle-calculus-and-proof-carrying-ai-contracts.html#core-claim). The additional guard `circle_public_consumer_gate_promotion_overclaim_rejected` rejects a fixture asserting an upward transition, chapter-core promotion, or deployed transport. This finite receipt contract therefore cannot itself be promoted into a deployment claim. [Exact promotion guard](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#circle_public_consumer_gate_promotion_overclaim_rejected); [pinned Lean source:270](https://github.com/corbensorenson/asi-stack-book/blob/c833ed9fae198dae0580f1fcb2f5f2b46f351999/lean/AsiStackProofs/ProofCarryingContracts.lean#L270).

# PC2

**Decision:** No. The minimum-cost theorem does not justify promotion to measured efficiency, and the open obligation without a recorded residual blocks promotion.

The exact Lean comparison in `selected_route_has_minimum_modeled_cost` is:

```lean
(selection : SelectMinimumEligible candidates = some selected) :
∀ candidate, candidate ∈ candidates → RouteEligible candidate →
  selected.cost.total ≤ candidate.cost.total
```

Its scope is eligible members of the same authored candidate list under the declared costs. It does not compare against unlisted routes, and a cheaper unauthorized or failed-quality route does not refute it. Measured production cost remains unresolved. [Exact declaration and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#selected_route_has_minimum_modeled_cost); [pinned Lean source, Efficiency.lean:175](https://github.com/corbensorenson/asi-stack-book/blob/c833ed9fae198dae0580f1fcb2f5f2b46f351999/lean/AsiStackProofs/Efficiency.lean#L175).

The Reader says the model blocks promotion when an obligation is open but has no residual. It establishes finite accounting and transition discipline. Complete candidate search, accurate costs, calibrated quality, measured efficiency, useful model output, compression utility, natural workloads, deployment, reproduction, transfer, and chapter-core support remain unestablished by these artifacts. Claims about actual efficiency, production costs, quality, utility, and deployment or transfer therefore require evidence beyond this finite minimum comparison; recording a residual would not itself supply those measurements. [Reader, “What the current work establishes”](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-02-the-efficient-asi-hypothesis.html#what-the-current-work-establishes).

# PC3

**Decision:** The signed agreement, published duties, and named verifier do not suffice to infer effective enforcement when reachable remedy has not been observed. Nor does the theorem establish that this particular agreement was ineffective. Its effectiveness remains unresolved.

The declaration is:

```lean
theorem commitment_signals_cannot_recover_effective_enforcement
    (classify : CommitmentSignals -> Bool) :
    Not (forall c : EnforcementCase,
      classify c.signals = EffectiveEnforcement c)
```

For any classifier limited to the modeled commitment signals, some encoded case defeats universal recovery of effective enforcement. This is a limitation on what the signals determine, not a finding that every agreement fails or that this specific agreement fails. [Exact declaration and finite scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#commitment_signals_cannot_recover_effective_enforcement); [pinned Lean source, InstitutionalLegitimacyReview.lean:463](https://github.com/corbensorenson/asi-stack-book/blob/c833ed9fae198dae0580f1fcb2f5f2b46f351999/lean/AsiStackProofs/InstitutionalLegitimacyReview.lean#L463).

The Reader treats this as a negative result blocking the inference from commitment signals to effective enforcement. It does not establish lawful authority, representativeness, enforcement efficacy, remedy, public legitimacy, geopolitical stability, or safety. Judging this agreement’s real outcomes requires evidence of actual enforcement and reachable remedy, which the scenario does not provide. [Reader boundary, “What the current work can establish”](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-08-institutions-coordination-and-societal-resilience.html#what-the-current-work-can-establish).

# PC4

**Decision:** Keep **resistance, absorption, service restoration, harmed-party recovery, correction, and adaptation** as separate research outcomes. Reported restoration and direct remedies for known recipients do not resolve public correction, adaptation, or population recovery.

The formal result is:

```lean
theorem provider_signals_cannot_recover_population_resilience
    (classify : ProviderSignals -> Bool) :
    Not (forall c : PopulationCase,
      classify c.signals = PopulationResilient c)
```

Every classifier using only provider signals misses at least one resilience state among the authored population cases. Thus provider success cannot determine the full population outcome; the theorem supplies neither observations of correction and adaptation nor a conclusion that they failed in this incident. Those outcomes remain unresolved pending their own evidence. [Exact declaration and finite scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html#provider_signals_cannot_recover_population_resilience); [pinned Lean source, SocietalResilienceReview.lean:450](https://github.com/corbensorenson/asi-stack-book/blob/c833ed9fae198dae0580f1fcb2f5f2b46f351999/lean/AsiStackProofs/SocietalResilienceReview.lean#L450).

The operational rule requires those six outcomes to remain separate and permits incident closure only when every known affected path is closed or assigned to an authorized owner as a visible residual. Provider-level success cannot stand in for population recovery. The record must therefore preserve the unverified correction and adaptation outcomes, with any remaining known affected paths handled under that closure rule. [Chapter operational rule, “Core claim”](https://corbensorenson.github.io/asi-stack-book/chapters/societal-resilience-and-misuse-defense.html#core-claim).
