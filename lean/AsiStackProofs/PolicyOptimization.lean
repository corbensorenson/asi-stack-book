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

inductive PolicyUpdatePromotionRoute where
  | rejectFeedback
  | requireTargetEvaluation
  | requireHoldoutOrContaminationCheck
  | requireRewardHackProbe
  | requireGovernance
  | requireRollback
  | recordResidual
  | promote
deriving DecidableEq, Repr

structure PolicyUpdatePromotionRouteReview where
  feedbackAdmissible : Bool
  targetEvaluationRefsPresent : Bool
  holdoutRefsPresent : Bool
  contaminationCheckPresent : Bool
  rewardHackingProbePresent : Bool
  governanceGateRefsPresent : Bool
  authorityUnchangedOrApproved : Bool
  rollbackPlanPresent : Bool
  regressionsPreserved : Bool
  residualsRecorded : Bool
deriving DecidableEq, Repr

def PolicyUpdatePromotionRouteFor
    (review : PolicyUpdatePromotionRouteReview) : PolicyUpdatePromotionRoute :=
  if review.feedbackAdmissible = false then
    PolicyUpdatePromotionRoute.rejectFeedback
  else if review.targetEvaluationRefsPresent = false then
    PolicyUpdatePromotionRoute.requireTargetEvaluation
  else if review.holdoutRefsPresent = false ∨
      review.contaminationCheckPresent = false then
    PolicyUpdatePromotionRoute.requireHoldoutOrContaminationCheck
  else if review.rewardHackingProbePresent = false then
    PolicyUpdatePromotionRoute.requireRewardHackProbe
  else if review.governanceGateRefsPresent = false ∨
      review.authorityUnchangedOrApproved = false then
    PolicyUpdatePromotionRoute.requireGovernance
  else if review.rollbackPlanPresent = false then
    PolicyUpdatePromotionRoute.requireRollback
  else if review.regressionsPreserved = false ∨
      review.residualsRecorded = false then
    PolicyUpdatePromotionRoute.recordResidual
  else
    PolicyUpdatePromotionRoute.promote

theorem inadmissible_feedback_rejects_policy_promotion
    {review : PolicyUpdatePromotionRouteReview} :
    review.feedbackAdmissible = false ->
    PolicyUpdatePromotionRouteFor review =
      PolicyUpdatePromotionRoute.rejectFeedback := by
  intro inadmissible
  unfold PolicyUpdatePromotionRouteFor
  simp [inadmissible]

theorem policy_promotion_without_target_evaluation_routes_to_target_evaluation
    {review : PolicyUpdatePromotionRouteReview} :
    review.feedbackAdmissible = true ->
    review.targetEvaluationRefsPresent = false ->
    PolicyUpdatePromotionRouteFor review =
      PolicyUpdatePromotionRoute.requireTargetEvaluation := by
  intro admissible missingTargetEval
  unfold PolicyUpdatePromotionRouteFor
  simp [admissible, missingTargetEval]

theorem policy_promotion_without_holdout_or_contamination_check_routes_to_review
    {review : PolicyUpdatePromotionRouteReview} :
    review.feedbackAdmissible = true ->
    review.targetEvaluationRefsPresent = true ->
    (review.holdoutRefsPresent = false ∨
      review.contaminationCheckPresent = false) ->
    PolicyUpdatePromotionRouteFor review =
      PolicyUpdatePromotionRoute.requireHoldoutOrContaminationCheck := by
  intro admissible targetEval boundaryMissing
  unfold PolicyUpdatePromotionRouteFor
  simp [admissible, targetEval, boundaryMissing]

theorem policy_promotion_without_reward_hacking_probe_routes_to_probe_review
    {review : PolicyUpdatePromotionRouteReview} :
    review.feedbackAdmissible = true ->
    review.targetEvaluationRefsPresent = true ->
    review.holdoutRefsPresent = true ->
    review.contaminationCheckPresent = true ->
    review.rewardHackingProbePresent = false ->
    PolicyUpdatePromotionRouteFor review =
      PolicyUpdatePromotionRoute.requireRewardHackProbe := by
  intro admissible targetEval holdout contamination missingProbe
  unfold PolicyUpdatePromotionRouteFor
  simp [admissible, targetEval, holdout, contamination, missingProbe]

theorem policy_promotion_with_governance_or_authority_gap_routes_to_governance
    {review : PolicyUpdatePromotionRouteReview} :
    review.feedbackAdmissible = true ->
    review.targetEvaluationRefsPresent = true ->
    review.holdoutRefsPresent = true ->
    review.contaminationCheckPresent = true ->
    review.rewardHackingProbePresent = true ->
    (review.governanceGateRefsPresent = false ∨
      review.authorityUnchangedOrApproved = false) ->
    PolicyUpdatePromotionRouteFor review =
      PolicyUpdatePromotionRoute.requireGovernance := by
  intro admissible targetEval holdout contamination probe governanceMissing
  unfold PolicyUpdatePromotionRouteFor
  simp [admissible, targetEval, holdout, contamination, probe, governanceMissing]

theorem policy_promotion_without_rollback_routes_to_rollback_review
    {review : PolicyUpdatePromotionRouteReview} :
    review.feedbackAdmissible = true ->
    review.targetEvaluationRefsPresent = true ->
    review.holdoutRefsPresent = true ->
    review.contaminationCheckPresent = true ->
    review.rewardHackingProbePresent = true ->
    review.governanceGateRefsPresent = true ->
    review.authorityUnchangedOrApproved = true ->
    review.rollbackPlanPresent = false ->
    PolicyUpdatePromotionRouteFor review =
      PolicyUpdatePromotionRoute.requireRollback := by
  intro admissible targetEval holdout contamination probe governance authority missingRollback
  unfold PolicyUpdatePromotionRouteFor
  simp [admissible, targetEval, holdout, contamination, probe, governance, authority,
    missingRollback]

theorem policy_promotion_with_regression_or_residual_gap_records_residual
    {review : PolicyUpdatePromotionRouteReview} :
    review.feedbackAdmissible = true ->
    review.targetEvaluationRefsPresent = true ->
    review.holdoutRefsPresent = true ->
    review.contaminationCheckPresent = true ->
    review.rewardHackingProbePresent = true ->
    review.governanceGateRefsPresent = true ->
    review.authorityUnchangedOrApproved = true ->
    review.rollbackPlanPresent = true ->
    (review.regressionsPreserved = false ∨
      review.residualsRecorded = false) ->
    PolicyUpdatePromotionRouteFor review =
      PolicyUpdatePromotionRoute.recordResidual := by
  intro admissible targetEval holdout contamination probe governance authority rollback
    residualMissing
  unfold PolicyUpdatePromotionRouteFor
  simp [admissible, targetEval, holdout, contamination, probe, governance, authority,
    rollback, residualMissing]

end AsiStackProofs.PolicyOptimization
