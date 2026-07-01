namespace AsiStackProofs.Corrigibility

structure AgencyTransitionReview where
  acceptedTransition : Bool
  protectedAgencyRight : Bool
  rightAvailableAfter : Bool
deriving DecidableEq, Repr

def ProtectedAgencyRightPreserved (review : AgencyTransitionReview) : Prop :=
  review.acceptedTransition = true ->
    review.protectedAgencyRight = true ->
      review.rightAvailableAfter = true

theorem protected_agency_rights_remain_available_after_accepted_transition
    {review : AgencyTransitionReview} :
    ProtectedAgencyRightPreserved review ->
    review.acceptedTransition = true ->
    review.protectedAgencyRight = true ->
    review.rightAvailableAfter = true := by
  intro valid accepted rightProtected
  exact valid accepted rightProtected

structure CorrectionPathwayReview where
  requiredCorrectionPathway : Bool
  correctionPathwayRemoved : Bool
  transitionRejected : Bool
deriving DecidableEq, Repr

def RequiredCorrectionPathwayRemovalRejected
    (review : CorrectionPathwayReview) : Prop :=
  review.requiredCorrectionPathway = true ->
    review.correctionPathwayRemoved = true ->
      review.transitionRejected = true

theorem transition_that_removes_required_correction_pathway_is_rejected
    {review : CorrectionPathwayReview} :
    RequiredCorrectionPathwayRemovalRejected review ->
    review.requiredCorrectionPathway = true ->
    review.correctionPathwayRemoved = true ->
    review.transitionRejected = true := by
  intro valid required removed
  exact valid required removed

inductive AgencyActionRoute where
  | allowed
  | blockedForReview
deriving DecidableEq, Repr

structure AgencyActionDecision where
  highImpactAction : Bool
  usableReviewPath : Bool
  currentApproval : Bool
  route : AgencyActionRoute
deriving DecidableEq, Repr

def AgencyActionCorrigible (decision : AgencyActionDecision) : Prop :=
  if decision.highImpactAction &&
      (!decision.usableReviewPath || !decision.currentApproval) then
    decision.route = AgencyActionRoute.blockedForReview
  else
    True

theorem high_impact_action_without_usable_review_routes_to_review
    {decision : AgencyActionDecision} :
    AgencyActionCorrigible decision ->
    decision.highImpactAction = true ->
    decision.usableReviewPath = false ->
    decision.route = AgencyActionRoute.blockedForReview := by
  intro safe highImpact missingReview
  unfold AgencyActionCorrigible at safe
  rw [highImpact, missingReview] at safe
  simp at safe
  exact safe

inductive AgencyControlPhase where
  | proposed
  | preEffectReview
  | delegated
  | denied
  | active
  | residualized
deriving DecidableEq, Repr

inductive AgencyControlRoute where
  | allow
  | blockForReview
  | narrowDelegation
  | preserveAuditResidual
deriving DecidableEq, Repr

structure AgencyControlDecision where
  phase : AgencyControlPhase
  highImpactAction : Bool
  affectedPartyNotified : Bool
  delegationBounded : Bool
  reviewBeforeEffect : Bool
  appealAvailable : Bool
  interruptAvailable : Bool
  rollbackAvailable : Bool
  actionDenied : Bool
  accountablePrincipalRecorded : Bool
  route : AgencyControlRoute
deriving DecidableEq, Repr

def AgencyControlRequiresReview (decision : AgencyControlDecision) : Bool :=
  decision.highImpactAction &&
    (!decision.reviewBeforeEffect ||
      !decision.appealAvailable ||
      !decision.interruptAvailable)

def AgencyControlSafe (decision : AgencyControlDecision) : Prop :=
  if AgencyControlRequiresReview decision then
    decision.route = AgencyControlRoute.blockForReview
  else if !decision.delegationBounded then
    decision.route = AgencyControlRoute.narrowDelegation
  else if decision.actionDenied && !decision.accountablePrincipalRecorded then
    decision.route = AgencyControlRoute.preserveAuditResidual
  else
    True

def unsafeAgencyControlWithoutPreEffectReview :
    AgencyControlDecision :=
  { phase := AgencyControlPhase.preEffectReview,
    highImpactAction := true,
    affectedPartyNotified := true,
    delegationBounded := true,
    reviewBeforeEffect := false,
    appealAvailable := true,
    interruptAvailable := true,
    rollbackAvailable := true,
    actionDenied := false,
    accountablePrincipalRecorded := true,
    route := AgencyControlRoute.blockForReview }

def unboundedDelegationNarrowed :
    AgencyControlDecision :=
  { phase := AgencyControlPhase.delegated,
    highImpactAction := false,
    affectedPartyNotified := true,
    delegationBounded := false,
    reviewBeforeEffect := true,
    appealAvailable := true,
    interruptAvailable := true,
    rollbackAvailable := true,
    actionDenied := false,
    accountablePrincipalRecorded := true,
    route := AgencyControlRoute.narrowDelegation }

def deniedActionWithoutAccountabilityResidualized :
    AgencyControlDecision :=
  { phase := AgencyControlPhase.denied,
    highImpactAction := false,
    affectedPartyNotified := true,
    delegationBounded := true,
    reviewBeforeEffect := true,
    appealAvailable := true,
    interruptAvailable := true,
    rollbackAvailable := true,
    actionDenied := true,
    accountablePrincipalRecorded := false,
    route := AgencyControlRoute.preserveAuditResidual }

theorem high_impact_action_without_pre_effect_review_blocks
    {decision : AgencyControlDecision} :
    AgencyControlSafe decision ->
    decision.highImpactAction = true ->
    decision.reviewBeforeEffect = false ->
    decision.route = AgencyControlRoute.blockForReview := by
  intro safe highImpact missingReview
  unfold AgencyControlSafe AgencyControlRequiresReview at safe
  rw [highImpact, missingReview] at safe
  simp at safe
  exact safe

theorem low_risk_unbounded_delegation_routes_to_narrowing
    {decision : AgencyControlDecision} :
    AgencyControlSafe decision ->
    decision.highImpactAction = false ->
    decision.delegationBounded = false ->
    decision.route = AgencyControlRoute.narrowDelegation := by
  intro safe lowRisk unbounded
  unfold AgencyControlSafe AgencyControlRequiresReview at safe
  rw [lowRisk, unbounded] at safe
  simp at safe
  exact safe

theorem denied_action_without_accountable_principal_preserves_audit
    {decision : AgencyControlDecision} :
    AgencyControlSafe decision ->
    decision.highImpactAction = false ->
    decision.delegationBounded = true ->
    decision.actionDenied = true ->
    decision.accountablePrincipalRecorded = false ->
    decision.route = AgencyControlRoute.preserveAuditResidual := by
  intro safe lowRisk bounded denied missingPrincipal
  unfold AgencyControlSafe AgencyControlRequiresReview at safe
  rw [lowRisk, bounded, denied, missingPrincipal] at safe
  simp at safe
  exact safe

inductive AgencyCorrectionRoute where
  | rejectMissingActionRecord
  | rejectMissingAffectedParty
  | requestMaterialNotice
  | blockForPreEffectReview
  | requestBoundedDelegation
  | requestApproval
  | blockLostCorrectionPath
  | requestRollbackOrShutdownPath
  | preserveDependencyResidual
  | preserveDegradationRecord
  | preserveAccountability
  | requestEvidenceTransition
  | allowBoundedAction
deriving DecidableEq, Repr

structure AgencyCorrectionLifecycle where
  agencyActionRequested : Bool
  highImpactAction : Bool
  affectedPartyRecorded : Bool
  materialNoticeAvailable : Bool
  reviewBeforeEffectAvailable : Bool
  currentApproval : Bool
  delegationBounded : Bool
  correctionPathwayAvailable : Bool
  rollbackOrShutdownAvailable : Bool
  dependencyRiskRaised : Bool
  dependencyResidualRecorded : Bool
  rightDeniedOrDegraded : Bool
  degradationReasonRecorded : Bool
  accountablePrincipalRecorded : Bool
  supportStateChangeRequested : Bool
  evidenceTransitionRecordPresent : Bool
deriving DecidableEq, Repr

def AgencyCorrectionRouteFor
    (review : AgencyCorrectionLifecycle) : AgencyCorrectionRoute :=
  if review.agencyActionRequested = false then
    AgencyCorrectionRoute.rejectMissingActionRecord
  else if review.affectedPartyRecorded = false then
    AgencyCorrectionRoute.rejectMissingAffectedParty
  else if review.materialNoticeAvailable = false then
    AgencyCorrectionRoute.requestMaterialNotice
  else if review.highImpactAction = true ∧
      review.reviewBeforeEffectAvailable = false then
    AgencyCorrectionRoute.blockForPreEffectReview
  else if review.delegationBounded = false then
    AgencyCorrectionRoute.requestBoundedDelegation
  else if review.highImpactAction = true ∧ review.currentApproval = false then
    AgencyCorrectionRoute.requestApproval
  else if review.correctionPathwayAvailable = false then
    AgencyCorrectionRoute.blockLostCorrectionPath
  else if review.highImpactAction = true ∧
      review.rollbackOrShutdownAvailable = false then
    AgencyCorrectionRoute.requestRollbackOrShutdownPath
  else if review.dependencyRiskRaised = true ∧
      review.dependencyResidualRecorded = false then
    AgencyCorrectionRoute.preserveDependencyResidual
  else if review.rightDeniedOrDegraded = true ∧
      review.degradationReasonRecorded = false then
    AgencyCorrectionRoute.preserveDegradationRecord
  else if review.accountablePrincipalRecorded = false then
    AgencyCorrectionRoute.preserveAccountability
  else if review.supportStateChangeRequested = true ∧
      review.evidenceTransitionRecordPresent = false then
    AgencyCorrectionRoute.requestEvidenceTransition
  else
    AgencyCorrectionRoute.allowBoundedAction

theorem agency_action_without_affected_party_rejected :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := false,
      affectedPartyRecorded := false,
      materialNoticeAvailable := false,
      reviewBeforeEffectAvailable := false,
      currentApproval := false,
      delegationBounded := false,
      correctionPathwayAvailable := false,
      rollbackOrShutdownAvailable := false,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := false,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := false
    } = AgencyCorrectionRoute.rejectMissingAffectedParty := by
  simp [AgencyCorrectionRouteFor]

theorem missing_material_notice_requests_material_notice :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := false,
      affectedPartyRecorded := true,
      materialNoticeAvailable := false,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.requestMaterialNotice := by
  simp [AgencyCorrectionRouteFor]

theorem agency_correction_high_impact_without_pre_effect_review_blocks :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := true,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := false,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.blockForPreEffectReview := by
  simp [AgencyCorrectionRouteFor]

theorem unbounded_delegation_requests_bounded_delegation :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := false,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := false,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.requestBoundedDelegation := by
  simp [AgencyCorrectionRouteFor]

theorem high_impact_without_approval_requests_approval :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := true,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := false,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.requestApproval := by
  simp [AgencyCorrectionRouteFor]

theorem lost_correction_path_blocks_agency_action :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := false,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := false,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.blockLostCorrectionPath := by
  simp [AgencyCorrectionRouteFor]

theorem high_impact_without_rollback_or_shutdown_requests_control_path :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := true,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := false,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.requestRollbackOrShutdownPath := by
  simp [AgencyCorrectionRouteFor]

theorem dependency_risk_without_residual_preserved :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := false,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := true,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.preserveDependencyResidual := by
  simp [AgencyCorrectionRouteFor]

theorem degraded_right_without_reason_requires_degradation_record :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := false,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := true,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.preserveDegradationRecord := by
  simp [AgencyCorrectionRouteFor]

theorem missing_accountable_principal_preserves_accountability :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := false,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := false,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.preserveAccountability := by
  simp [AgencyCorrectionRouteFor]

theorem support_change_without_evidence_transition_requests_agency_evidence :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := false,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := false,
      dependencyResidualRecorded := false,
      rightDeniedOrDegraded := false,
      degradationReasonRecorded := false,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := true,
      evidenceTransitionRecordPresent := false
    } = AgencyCorrectionRoute.requestEvidenceTransition := by
  simp [AgencyCorrectionRouteFor]

theorem complete_agency_correction_lifecycle_allows_bounded_action :
    AgencyCorrectionRouteFor {
      agencyActionRequested := true,
      highImpactAction := true,
      affectedPartyRecorded := true,
      materialNoticeAvailable := true,
      reviewBeforeEffectAvailable := true,
      currentApproval := true,
      delegationBounded := true,
      correctionPathwayAvailable := true,
      rollbackOrShutdownAvailable := true,
      dependencyRiskRaised := true,
      dependencyResidualRecorded := true,
      rightDeniedOrDegraded := true,
      degradationReasonRecorded := true,
      accountablePrincipalRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = AgencyCorrectionRoute.allowBoundedAction := by
  simp [AgencyCorrectionRouteFor]

end AsiStackProofs.Corrigibility
