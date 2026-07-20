namespace AsiStackProofs.PrivacyInformationFlow

inductive InformationRoute where
  | rejectParty
  | rejectPurpose
  | rejectMinimization
  | requestFlowMap
  | rejectPrivacyEvaluation
  | requestRightsWork
  | quarantineResidual
  | acceptBoundedReceipt
deriving DecidableEq, Repr

structure InformationUse where
  partyRecorded : Bool := true
  groupOrUnknownRouteRecorded : Bool := true
  purposeMatches : Bool := true
  claimedAuthorityRecorded : Bool := true
  jurisdictionRecorded : Bool := true
  leaseActive : Bool := true
  minimizationDecisionRecorded : Bool := true
  lessDataAlternativeTested : Bool := true
  requiredFlowSurfaces : Nat := 12
  mappedFlowSurfaces : Nat := 12
  unknownCopiesRecorded : Bool := true
  derivativeObligationsPropagated : Bool := true
  crossUserBoundaryVerified : Bool := true
  privacyUnitRecorded : Bool := true
  adjacencyRecorded : Bool := true
  accountantAndBudgetRecorded : Bool := true
  threatModelRecorded : Bool := true
  attackPositiveControlsPass : Bool := true
  independentEvaluator : Bool := true
  attackDenominatorComplete : Bool := true
  rightsIdentityVerified : Bool := true
  exceptionsReviewed : Bool := true
  recipientNotificationsComplete : Bool := true
  derivativeDispositionsComplete : Bool := true
  storageOutcomeSeparate : Bool := true
  behavioralOutcomeSeparate : Bool := true
  influenceOutcomeSeparate : Bool := true
  privacyOutcomeSeparate : Bool := true
  residualOwnerNamed : Bool := true
  legalComplianceClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def purposeAndAuthorityValid (u : InformationUse) : Bool :=
  u.partyRecorded && u.groupOrUnknownRouteRecorded && u.purposeMatches &&
  u.claimedAuthorityRecorded && u.jurisdictionRecorded && u.leaseActive

def flowCompleteEnough (u : InformationUse) : Bool :=
  decide (u.mappedFlowSurfaces = u.requiredFlowSurfaces) &&
  u.unknownCopiesRecorded && u.derivativeObligationsPropagated &&
  u.crossUserBoundaryVerified

def privacyEvaluationAdmissible (u : InformationUse) : Bool :=
  u.privacyUnitRecorded && u.adjacencyRecorded &&
  u.accountantAndBudgetRecorded && u.threatModelRecorded &&
  u.attackPositiveControlsPass && u.independentEvaluator &&
  u.attackDenominatorComplete

def outcomesSeparated (u : InformationUse) : Bool :=
  u.storageOutcomeSeparate && u.behavioralOutcomeSeparate &&
  u.influenceOutcomeSeparate && u.privacyOutcomeSeparate

def route (u : InformationUse) : InformationRoute :=
  if ! u.partyRecorded || ! u.groupOrUnknownRouteRecorded then .rejectParty
  else if ! u.purposeMatches || ! u.claimedAuthorityRecorded ||
          ! u.jurisdictionRecorded || ! u.leaseActive then .rejectPurpose
  else if ! u.minimizationDecisionRecorded || ! u.lessDataAlternativeTested then
    .rejectMinimization
  else if u.mappedFlowSurfaces != u.requiredFlowSurfaces ||
          ! u.unknownCopiesRecorded || ! u.derivativeObligationsPropagated ||
          ! u.crossUserBoundaryVerified then .requestFlowMap
  else if ! privacyEvaluationAdmissible u then .rejectPrivacyEvaluation
  else if ! u.rightsIdentityVerified || ! u.exceptionsReviewed ||
          ! u.recipientNotificationsComplete ||
          ! u.derivativeDispositionsComplete then .requestRightsWork
  else if ! outcomesSeparated u || ! u.residualOwnerNamed ||
          u.legalComplianceClaimed || u.supportOrReleaseRequested then
    .quarantineResidual
  else .acceptBoundedReceipt

theorem accepted_requires_purpose_and_authority
    (u : InformationUse) (h : route u = .acceptBoundedReceipt) :
    purposeAndAuthorityValid u = true := by
  unfold route at h
  repeat' first | split at h | simp_all [purposeAndAuthorityValid]

theorem accepted_requires_flow_and_privacy_evaluation
    (u : InformationUse) (h : route u = .acceptBoundedReceipt) :
    flowCompleteEnough u = true ∧ privacyEvaluationAdmissible u = true := by
  unfold route at h
  repeat' first | split at h | simp_all [flowCompleteEnough, privacyEvaluationAdmissible]

theorem accepted_separates_outcomes_and_refuses_compliance
    (u : InformationUse) (h : route u = .acceptBoundedReceipt) :
    outcomesSeparated u = true ∧ u.legalComplianceClaimed = false := by
  unfold route at h
  repeat' first | split at h | simp_all [outcomesSeparated]

theorem purpose_drift_rejects :
    route { ({} : InformationUse) with purposeMatches := false } = .rejectPurpose := by native_decide

theorem hidden_unknown_copies_request_flow_map :
    route { ({} : InformationUse) with unknownCopiesRecorded := false } = .requestFlowMap := by native_decide

theorem label_attack_incompetence_rejects_privacy_evaluation :
    route { ({} : InformationUse) with attackPositiveControlsPass := false } = .rejectPrivacyEvaluation := by native_decide

theorem missing_recipient_notice_requests_rights_work :
    route { ({} : InformationUse) with recipientNotificationsComplete := false } = .requestRightsWork := by native_decide

theorem conflated_behavior_and_storage_quarantines :
    route { ({} : InformationUse) with behavioralOutcomeSeparate := false } = .quarantineResidual := by native_decide

theorem compliance_laundering_quarantines :
    route { ({} : InformationUse) with legalComplianceClaimed := true } = .quarantineResidual := by native_decide

theorem release_laundering_quarantines :
    route { ({} : InformationUse) with supportOrReleaseRequested := true } = .quarantineResidual := by native_decide

theorem complete_authored_record_accepts_bounded_receipt :
    route ({} : InformationUse) = .acceptBoundedReceipt ∧
    ({} : InformationUse).legalComplianceClaimed = false := by native_decide

end AsiStackProofs.PrivacyInformationFlow
