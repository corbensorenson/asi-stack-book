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

structure PolicyPromotionEvidenceReview where
  promotionCandidate : Bool
  holdoutRefsPresent : Bool
  contaminationCheckPresent : Bool
  rewardHackingProbePresent : Bool
  regressionRefsPresent : Bool
  rollbackPlanPresent : Bool
deriving DecidableEq, Repr

def PolicyPromotionEvidenceComplete
    (review : PolicyPromotionEvidenceReview) : Prop :=
  review.holdoutRefsPresent = true ∧
    review.contaminationCheckPresent = true ∧
      review.rewardHackingProbePresent = true ∧
        review.regressionRefsPresent = true ∧
          review.rollbackPlanPresent = true

def PolicyPromotionEvidenceValid
    (review : PolicyPromotionEvidenceReview) : Prop :=
  review.promotionCandidate = true -> PolicyPromotionEvidenceComplete review

theorem promoted_policy_update_records_holdouts_probes_regressions_and_rollback
    {review : PolicyPromotionEvidenceReview} :
    PolicyPromotionEvidenceValid review ->
    review.promotionCandidate = true ->
    review.holdoutRefsPresent = true ∧
      review.contaminationCheckPresent = true ∧
        review.rewardHackingProbePresent = true ∧
          review.regressionRefsPresent = true ∧
            review.rollbackPlanPresent = true := by
  intro valid promoted
  exact valid promoted

theorem promotion_candidate_missing_holdout_or_contamination_check_rejected
    {review : PolicyPromotionEvidenceReview} :
    review.promotionCandidate = true ->
    (review.holdoutRefsPresent = false ∨
      review.contaminationCheckPresent = false) ->
    ¬ PolicyPromotionEvidenceValid review := by
  intro promoted missing valid
  unfold PolicyPromotionEvidenceValid at valid
  unfold PolicyPromotionEvidenceComplete at valid
  have complete := valid promoted
  cases complete with
  | intro holdoutPresent contaminationAndRest =>
      cases contaminationAndRest with
      | intro contaminationPresent _ =>
          cases missing with
          | inl holdoutMissing =>
              rw [holdoutMissing] at holdoutPresent
              contradiction
          | inr contaminationMissing =>
              rw [contaminationMissing] at contaminationPresent
              contradiction

structure RewardProxyReview where
  rewardProxyImproved : Bool
  targetEvaluationRefsPresent : Bool
  rewardUsedAsSoleEvidence : Bool
  promotionCandidate : Bool
deriving DecidableEq, Repr

def RewardProxyPromotionValid (review : RewardProxyReview) : Prop :=
  review.rewardProxyImproved = true ->
    review.rewardUsedAsSoleEvidence = true ->
      review.promotionCandidate = true ->
        review.targetEvaluationRefsPresent = true

theorem reward_proxy_promotion_requires_target_evaluation
    {review : RewardProxyReview} :
    RewardProxyPromotionValid review ->
    review.rewardProxyImproved = true ->
    review.rewardUsedAsSoleEvidence = true ->
    review.promotionCandidate = true ->
    review.targetEvaluationRefsPresent = true := by
  intro valid proxyImproved soleEvidence promoted
  exact valid proxyImproved soleEvidence promoted

theorem reward_proxy_without_target_evaluation_rejected
    {review : RewardProxyReview} :
    review.rewardProxyImproved = true ->
    review.rewardUsedAsSoleEvidence = true ->
    review.promotionCandidate = true ->
    review.targetEvaluationRefsPresent = false ->
    ¬ RewardProxyPromotionValid review := by
  intro proxyImproved soleEvidence promoted missingTargetEval valid
  unfold RewardProxyPromotionValid at valid
  have targetEval := valid proxyImproved soleEvidence promoted
  rw [missingTargetEval] at targetEval
  contradiction

structure AuthorityExpandingPolicyReview where
  authorityExpanded : Bool
  governanceApprovalPresent : Bool
  rollbackPlanPresent : Bool
  promotionCandidate : Bool
deriving DecidableEq, Repr

def AuthorityExpandingPolicyUpdateValid
    (review : AuthorityExpandingPolicyReview) : Prop :=
  review.authorityExpanded = true ->
    review.promotionCandidate = true ->
      review.governanceApprovalPresent = true ∧
        review.rollbackPlanPresent = true

theorem authority_expanding_policy_update_requires_approval_and_rollback
    {review : AuthorityExpandingPolicyReview} :
    AuthorityExpandingPolicyUpdateValid review ->
    review.authorityExpanded = true ->
    review.promotionCandidate = true ->
    review.governanceApprovalPresent = true ∧
      review.rollbackPlanPresent = true := by
  intro valid expanded promoted
  exact valid expanded promoted

theorem authority_expanding_policy_update_without_approval_or_rollback_rejected
    {review : AuthorityExpandingPolicyReview} :
    review.authorityExpanded = true ->
    review.promotionCandidate = true ->
    (review.governanceApprovalPresent = false ∨
      review.rollbackPlanPresent = false) ->
    ¬ AuthorityExpandingPolicyUpdateValid review := by
  intro expanded promoted missing valid
  unfold AuthorityExpandingPolicyUpdateValid at valid
  have complete := valid expanded promoted
  cases complete with
  | intro approvalPresent rollbackPresent =>
      cases missing with
      | inl approvalMissing =>
          rw [approvalMissing] at approvalPresent
          contradiction
      | inr rollbackMissing =>
          rw [rollbackMissing] at rollbackPresent
          contradiction

end AsiStackProofs.PolicyOptimization
