namespace AsiStackProofs.CyclicMixers

structure CyclicMixerClaimReview where
  structuralInvariantRecorded : Bool
  qualityClaimSeparate : Bool
  runtimeClaimSeparate : Bool
  memoryClaimSeparate : Bool
  parameterClaimSeparate : Bool
deriving DecidableEq, Repr

def StructuralClaimSeparated (review : CyclicMixerClaimReview) : Prop :=
  review.structuralInvariantRecorded = true ∧
    review.qualityClaimSeparate = true ∧
      review.runtimeClaimSeparate = true ∧
        review.memoryClaimSeparate = true ∧
          review.parameterClaimSeparate = true

theorem cyclic_mixer_claim_records_structure_separately_from_quality_runtime_memory_and_parameters
    {review : CyclicMixerClaimReview} :
    StructuralClaimSeparated review ->
    review.structuralInvariantRecorded = true ∧
      review.qualityClaimSeparate = true ∧
        review.runtimeClaimSeparate = true ∧
          review.memoryClaimSeparate = true ∧
            review.parameterClaimSeparate = true := by
  intro separated
  exact separated

structure CyclicSubstratePromotionReview where
  baselineRefsPresent : Bool
  tradeoffMetricsRecorded : Bool
  substratePromoted : Bool
deriving DecidableEq, Repr

def BaselinesAndTradeoffsRequired (review : CyclicSubstratePromotionReview) : Prop :=
  review.substratePromoted = true ->
    review.baselineRefsPresent = true ∧
      review.tradeoffMetricsRecorded = true

theorem cyclic_substrate_promotion_requires_baselines_and_tradeoff_metrics
    {review : CyclicSubstratePromotionReview} :
    BaselinesAndTradeoffsRequired review ->
    review.substratePromoted = true ->
    review.baselineRefsPresent = true ∧
      review.tradeoffMetricsRecorded = true := by
  intro valid promoted
  exact valid promoted

end AsiStackProofs.CyclicMixers
