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

inductive BenchmarkLifecycle where
  | candidate
  | frontier
  | regressionFloor
  | contaminated
  | retired
deriving DecidableEq, Repr

inductive RatchetDecision where
  | keepFrontier
  | promoteReadiness
  | moveToRegressionFloor
  | quarantine
  | blockPromotion
deriving DecidableEq, Repr

structure RatchetDecisionReview where
  lifecycle : BenchmarkLifecycle
  benchmarkSaturated : Bool
  contaminationSuspected : Bool
  transferOrMutationCheckPresent : Bool
  regressionRecordsPreserved : Bool
  negativeResultsPreserved : Bool
  decision : RatchetDecision
deriving DecidableEq, Repr

def RatchetDecisionAccepted (review : RatchetDecisionReview) : Prop :=
  match review.decision with
  | .promoteReadiness =>
      review.regressionRecordsPreserved = true ∧
        review.transferOrMutationCheckPresent = true ∧
          review.negativeResultsPreserved = true ∧
            review.contaminationSuspected = false
  | .moveToRegressionFloor =>
      review.benchmarkSaturated = true ∧
        review.regressionRecordsPreserved = true
  | .quarantine =>
      review.contaminationSuspected = true
  | .blockPromotion => True
  | .keepFrontier => True

theorem accepted_readiness_promotion_requires_transfer_negative_and_regression_records
    {review : RatchetDecisionReview} :
    RatchetDecisionAccepted review ->
    review.decision = RatchetDecision.promoteReadiness ->
    review.transferOrMutationCheckPresent = true ∧
      review.negativeResultsPreserved = true ∧
        review.regressionRecordsPreserved = true := by
  intro accepted promoted
  unfold RatchetDecisionAccepted at accepted
  rw [promoted] at accepted
  exact And.intro accepted.2.1 (And.intro accepted.2.2.1 accepted.1)

theorem accepted_saturated_floor_requires_regression_records
    {review : RatchetDecisionReview} :
    RatchetDecisionAccepted review ->
    review.decision = RatchetDecision.moveToRegressionFloor ->
    review.benchmarkSaturated = true ∧
      review.regressionRecordsPreserved = true := by
  intro accepted floor
  unfold RatchetDecisionAccepted at accepted
  rw [floor] at accepted
  exact accepted

theorem contaminated_review_cannot_promote_readiness
    {review : RatchetDecisionReview} :
    RatchetDecisionAccepted review ->
    review.contaminationSuspected = true ->
    review.decision = RatchetDecision.promoteReadiness ->
    False := by
  intro accepted contaminated promoted
  unfold RatchetDecisionAccepted at accepted
  rw [promoted] at accepted
  simp [contaminated] at accepted

structure AntiGoodhartFixtureBridgeSummary where
  validFixtureCount : Nat
  expectedInvalidFixtureCount : Nat
  promotionReadyValidCount : Nat
  regressionFloorValidCount : Nat
  missingGoodhartChecksRejected : Bool
  policyFromBlockedRatchetRejected : Bool
  rewardAsTruthRejected : Bool
  saturatedPromotionRejected : Bool
  releaseWithoutApprovalRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def AntiGoodhartFixtureBridgeValid
    (summary : AntiGoodhartFixtureBridgeSummary) : Prop :=
  summary.validFixtureCount = 2 ∧
    summary.expectedInvalidFixtureCount = 5 ∧
    summary.promotionReadyValidCount = 1 ∧
    summary.regressionFloorValidCount = 1 ∧
    summary.missingGoodhartChecksRejected = true ∧
    summary.policyFromBlockedRatchetRejected = true ∧
    summary.rewardAsTruthRejected = true ∧
    summary.saturatedPromotionRejected = true ∧
    summary.releaseWithoutApprovalRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

def benchmarkAntiGoodhartFixtureBridge :
    AntiGoodhartFixtureBridgeSummary :=
  { validFixtureCount := 2,
    expectedInvalidFixtureCount := 5,
    promotionReadyValidCount := 1,
    regressionFloorValidCount := 1,
    missingGoodhartChecksRejected := true,
    policyFromBlockedRatchetRejected := true,
    rewardAsTruthRejected := true,
    saturatedPromotionRejected := true,
    releaseWithoutApprovalRejected := true,
    supportStateEffectNone := true,
    nonClaimBoundary := true }

theorem benchmark_antigoodhart_fixture_bridge_valid :
    AntiGoodhartFixtureBridgeValid benchmarkAntiGoodhartFixtureBridge := by
  simp [AntiGoodhartFixtureBridgeValid, benchmarkAntiGoodhartFixtureBridge]

theorem benchmark_antigoodhart_fixture_bridge_has_expected_controls :
    benchmarkAntiGoodhartFixtureBridge.missingGoodhartChecksRejected = true ∧
      benchmarkAntiGoodhartFixtureBridge.policyFromBlockedRatchetRejected = true ∧
      benchmarkAntiGoodhartFixtureBridge.rewardAsTruthRejected = true ∧
      benchmarkAntiGoodhartFixtureBridge.saturatedPromotionRejected = true ∧
      benchmarkAntiGoodhartFixtureBridge.releaseWithoutApprovalRejected = true := by
  simp [benchmarkAntiGoodhartFixtureBridge]

theorem benchmark_antigoodhart_fixture_bridge_preserves_no_support_promotion :
    benchmarkAntiGoodhartFixtureBridge.supportStateEffectNone = true ∧
      benchmarkAntiGoodhartFixtureBridge.nonClaimBoundary = true := by
  simp [benchmarkAntiGoodhartFixtureBridge]

end AsiStackProofs.BenchmarkRatchets
