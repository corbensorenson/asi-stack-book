namespace AsiStackProofs.BenchmarkRatchets

structure CapabilityPromotionReview where
  capabilityPromotion : Bool
  benchmarkEvidencePresent : Bool
  regressionRecordsPreserved : Bool
deriving DecidableEq, Repr

def CapabilityPromotionHasBenchmarkAndRegressionEvidence
    (review : CapabilityPromotionReview) : Prop :=
  review.capabilityPromotion = true ->
    review.benchmarkEvidencePresent = true ∧
      review.regressionRecordsPreserved = true

theorem capability_promotion_requires_benchmark_evidence_and_preserved_regressions
    {review : CapabilityPromotionReview} :
    CapabilityPromotionHasBenchmarkAndRegressionEvidence review ->
    review.capabilityPromotion = true ->
    review.benchmarkEvidencePresent = true ∧
      review.regressionRecordsPreserved = true := by
  intro valid promoted
  exact valid promoted

structure SaturatedBenchmarkPromotionReview where
  benchmarkSaturated : Bool
  soleEvidenceForHigherReadiness : Bool
  higherReadinessPromoted : Bool
deriving DecidableEq, Repr

def SaturatedBenchmarkAloneBlocksHigherReadinessPromotion
    (review : SaturatedBenchmarkPromotionReview) : Prop :=
  review.benchmarkSaturated = true ->
    review.soleEvidenceForHigherReadiness = true ->
      review.higherReadinessPromoted = false

theorem saturated_benchmark_alone_cannot_promote_higher_readiness
    {review : SaturatedBenchmarkPromotionReview} :
    SaturatedBenchmarkAloneBlocksHigherReadinessPromotion review ->
    review.benchmarkSaturated = true ->
    review.soleEvidenceForHigherReadiness = true ->
    review.higherReadinessPromoted = false := by
  intro valid saturated soleEvidence
  exact valid saturated soleEvidence

end AsiStackProofs.BenchmarkRatchets
