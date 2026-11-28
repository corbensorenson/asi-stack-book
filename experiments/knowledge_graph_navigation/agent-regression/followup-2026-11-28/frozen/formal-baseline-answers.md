# FO1

`accepted_lease_is_bounded_versioned_and_unexpired` requires an event of kind lease issuance that the modeled authority transaction accepts. The new version is the previous version plus one, the new ceiling is at most the previous ceiling, and model time is strictly before the lease expires. The declaration establishes those properties of the modeled transition. It certifies neither a deployed clock nor a deployed identity service. [SecurityKernel.lean, line 796](https://github.com/corbensorenson/asi-stack-book/blob/d5d8c2f7c11985af1a7f9a4393f0771745610639/lean/AsiStackProofs/SecurityKernel.lean#L796)

# FO2

`circle_public_consumer_gate_missing_mutation_control_rejected` says the finite fixture fails acceptance if any one of the required digest, missing-theorem, stale-contract, or transfer rejection flags is false. The declaration proves a conditional property of the acceptance rule. Whether the four mutation trials ran and produced the required rejections is a separate execution result. [ProofCarryingContracts.lean, line 293](https://github.com/corbensorenson/asi-stack-book/blob/d5d8c2f7c11985af1a7f9a4393f0771745610639/lean/AsiStackProofs/ProofCarryingContracts.lean#L293)

# FO3

`participation_signals_cannot_recover_representation` shows that no classifier restricted to the modeled participation signals can recover representation correctly in every case. Two modeled cases have identical observed signals and different representation states. A classifier must give the same output for the identical inputs, so it misses at least one case. This is a non-identifiability result in the finite model. Whether a real institution is representative or legitimate requires separate evidence. [InstitutionalLegitimacyReview.lean, line 442](https://github.com/corbensorenson/asi-stack-book/blob/d5d8c2f7c11985af1a7f9a4393f0771745610639/lean/AsiStackProofs/InstitutionalLegitimacyReview.lean#L442) · [Human Reader, Unit 8, What the current work can establish](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-08-institutions-coordination-and-societal-resilience.html#what-the-current-work-can-establish)

# FO4

Pooled observed coverage is `(87 + 5) / (90 + 10) = 92%`. Camera-only observed coverage is `5 / 10 = 50%`. If those ten frames all come from one maneuver, 50% describes frames within that episode. Modality-conditioned conformal coverage assumes exchangeable calibration and test points within each modality group. Ten frames from one maneuver give little evidence at the maneuver level, especially if encoder loss is tied to difficult maneuvers. Coverage on the next maneuver remains open and calls for evaluation on separate representative episodes. [Perception, Sensor Fusion, and Observation Trust, §31.7.3](https://corbensorenson.github.io/asi-stack-book/chapters/perception-sensor-fusion-and-observation-trust.html#how-often-is-the-true-state-inside-the-prediction-set)
