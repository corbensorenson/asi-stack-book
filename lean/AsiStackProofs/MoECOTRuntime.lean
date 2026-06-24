namespace AsiStackProofs.MoECOTRuntime

structure RuntimeCorePromotionReview where
  runtimeCorePromotion : Bool
  readinessEvidenceRefsPresent : Bool
  regressionEvidenceRefsPresent : Bool
  replayEvidenceRefsPresent : Bool
deriving DecidableEq, Repr

def RuntimeCorePromotionHasEvidenceRefs
    (review : RuntimeCorePromotionReview) : Prop :=
  review.runtimeCorePromotion = true ->
    review.readinessEvidenceRefsPresent = true ∧
      review.regressionEvidenceRefsPresent = true ∧
        review.replayEvidenceRefsPresent = true

theorem runtime_core_promotion_requires_readiness_regression_and_replay_evidence
    {review : RuntimeCorePromotionReview} :
    RuntimeCorePromotionHasEvidenceRefs review ->
    review.runtimeCorePromotion = true ->
    review.readinessEvidenceRefsPresent = true ∧
      review.regressionEvidenceRefsPresent = true ∧
        review.replayEvidenceRefsPresent = true := by
  intro valid promoted
  exact valid promoted

structure RuntimeClaimSourceReview where
  sourcedOnlyFromUnavailableText : Bool
  promotedAboveArgument : Bool
deriving DecidableEq, Repr

def UnavailableTextOnlyBlocksPromotionAboveArgument
    (review : RuntimeClaimSourceReview) : Prop :=
  review.sourcedOnlyFromUnavailableText = true ->
    review.promotedAboveArgument = false

theorem runtime_claim_from_unavailable_text_only_cannot_promote_above_argument
    {review : RuntimeClaimSourceReview} :
    UnavailableTextOnlyBlocksPromotionAboveArgument review ->
    review.sourcedOnlyFromUnavailableText = true ->
    review.promotedAboveArgument = false := by
  intro valid sourceOnly
  exact valid sourceOnly

end AsiStackProofs.MoECOTRuntime
