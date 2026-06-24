namespace AsiStackProofs.PolicyOptimization

structure PolicyUpdateRecordReview where
  updateAdmitted : Bool
  targetLayerRecorded : Bool
  rewardSignalRecorded : Bool
  updateConstraintRecorded : Bool
  evaluationRefsPresent : Bool
  governanceGateRefsPresent : Bool
  rollbackPlanPresent : Bool
deriving DecidableEq, Repr

def AdmittedPolicyUpdateHasGovernedRecord
    (review : PolicyUpdateRecordReview) : Prop :=
  review.updateAdmitted = true ->
    review.targetLayerRecorded = true ∧
      review.rewardSignalRecorded = true ∧
        review.updateConstraintRecorded = true ∧
          review.evaluationRefsPresent = true ∧
            review.governanceGateRefsPresent = true ∧
              review.rollbackPlanPresent = true

theorem admitted_policy_update_records_reward_evaluation_governance_and_rollback
    {review : PolicyUpdateRecordReview} :
    AdmittedPolicyUpdateHasGovernedRecord review ->
    review.updateAdmitted = true ->
    review.targetLayerRecorded = true ∧
      review.rewardSignalRecorded = true ∧
        review.updateConstraintRecorded = true ∧
          review.evaluationRefsPresent = true ∧
            review.governanceGateRefsPresent = true ∧
              review.rollbackPlanPresent = true := by
  intro valid admitted
  exact valid admitted

structure RewardGovernancePromotionReview where
  rewardSignalUnverified : Bool
  governanceGateMissing : Bool
  policyUpdatePromoted : Bool
deriving DecidableEq, Repr

def UnverifiedRewardOrMissingGovernanceBlocksPromotion
    (review : RewardGovernancePromotionReview) : Prop :=
  review.rewardSignalUnverified = true ∨
    review.governanceGateMissing = true ->
      review.policyUpdatePromoted = false

theorem unverified_reward_or_missing_governance_gate_blocks_policy_promotion
    {review : RewardGovernancePromotionReview} :
    UnverifiedRewardOrMissingGovernanceBlocksPromotion review ->
    review.rewardSignalUnverified = true ∨
      review.governanceGateMissing = true ->
    review.policyUpdatePromoted = false := by
  intro valid missingBoundary
  exact valid missingBoundary

end AsiStackProofs.PolicyOptimization
