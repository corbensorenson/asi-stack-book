namespace AsiStackProofs.PrototypeRoadmap

structure PhaseUnlockReview where
  dependentPhaseUnlocked : Bool
  acceptanceGatesDeclared : Bool
  acceptanceGatesPassed : Bool
deriving DecidableEq, Repr

def PhaseUnlockValid (review : PhaseUnlockReview) : Prop :=
  review.dependentPhaseUnlocked = true ->
    review.acceptanceGatesDeclared = true ∧
      review.acceptanceGatesPassed = true

theorem roadmap_phase_unlock_requires_passing_acceptance_gates
    {review : PhaseUnlockReview} :
    PhaseUnlockValid review ->
    review.dependentPhaseUnlocked = true ->
      review.acceptanceGatesDeclared = true ∧
        review.acceptanceGatesPassed = true := by
  intro valid unlocked
  exact valid unlocked

structure PhaseClaimPromotionReview where
  milestoneReached : Bool
  claimPromotionAccepted : Bool
  evidenceArtifactsPresent : Bool
deriving DecidableEq, Repr

def PhaseMilestonePromotionValid (review : PhaseClaimPromotionReview) : Prop :=
  review.milestoneReached = true ->
    review.claimPromotionAccepted = true ->
      review.evidenceArtifactsPresent = true

theorem phase_milestone_cannot_promote_claim_without_evidence_artifacts
    {review : PhaseClaimPromotionReview} :
    PhaseMilestonePromotionValid review ->
    review.milestoneReached = true ->
    review.evidenceArtifactsPresent = false ->
      review.claimPromotionAccepted = false := by
  intro valid reached noEvidence
  cases promoted : review.claimPromotionAccepted with
  | false =>
      rfl
  | true =>
      have evidence := valid reached promoted
      rw [noEvidence] at evidence
      contradiction

theorem accepted_phase_claim_promotion_requires_evidence_artifacts
    {review : PhaseClaimPromotionReview} :
    PhaseMilestonePromotionValid review ->
    review.milestoneReached = true ->
    review.claimPromotionAccepted = true ->
      review.evidenceArtifactsPresent = true := by
  intro valid reached accepted
  exact valid reached accepted

end AsiStackProofs.PrototypeRoadmap
