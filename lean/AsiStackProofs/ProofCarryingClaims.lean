namespace AsiStackProofs.ProofCarryingClaims

structure FormalTierClaimReview where
  formalSupportTier : Bool
  validJustificationArtifactRef : Bool
deriving DecidableEq, Repr

def FormalTierHasJustificationArtifact
    (review : FormalTierClaimReview) : Prop :=
  review.formalSupportTier = true ->
    review.validJustificationArtifactRef = true

theorem formal_support_tier_requires_valid_justification_artifact
    {review : FormalTierClaimReview} :
    FormalTierHasJustificationArtifact review ->
    review.formalSupportTier = true ->
    review.validJustificationArtifactRef = true := by
  intro valid formalTier
  exact valid formalTier

structure FailedVerifierPromotionReview where
  verifierFailed : Bool
  claimDowngradedOrBlocked : Bool
  claimPromoted : Bool
deriving DecidableEq, Repr

def FailedVerifierBlocksPromotion
    (review : FailedVerifierPromotionReview) : Prop :=
  review.verifierFailed = true ->
    review.claimDowngradedOrBlocked = true ∧
      review.claimPromoted = false

theorem failed_verifier_result_downgrades_or_blocks_claim_promotion
    {review : FailedVerifierPromotionReview} :
    FailedVerifierBlocksPromotion review ->
    review.verifierFailed = true ->
    review.claimDowngradedOrBlocked = true ∧
      review.claimPromoted = false := by
  intro valid failed
  exact valid failed

end AsiStackProofs.ProofCarryingClaims
