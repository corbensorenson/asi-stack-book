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

theorem runtime_core_promotion_missing_evidence_rejected
    {review : RuntimeCorePromotionReview} :
    review.runtimeCorePromotion = true ->
      (review.readinessEvidenceRefsPresent = false ∨
        review.regressionEvidenceRefsPresent = false ∨
          review.replayEvidenceRefsPresent = false) ->
        ¬ RuntimeCorePromotionHasEvidenceRefs review := by
  intro promoted missingEvidence valid
  have required := valid promoted
  cases missingEvidence with
  | inl missingReadiness =>
      rw [missingReadiness] at required
      cases required.1
  | inr rest =>
      cases rest with
      | inl missingRegression =>
          rw [missingRegression] at required
          cases required.2.1
      | inr missingReplay =>
          rw [missingReplay] at required
          cases required.2.2

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

theorem unavailable_text_only_with_promotion_above_argument_rejected
    {review : RuntimeClaimSourceReview} :
    review.sourcedOnlyFromUnavailableText = true ->
      review.promotedAboveArgument = true ->
        ¬ UnavailableTextOnlyBlocksPromotionAboveArgument review := by
  intro sourceOnly promoted valid
  have blocked := valid sourceOnly
  rw [promoted] at blocked
  contradiction

end AsiStackProofs.MoECOTRuntime
