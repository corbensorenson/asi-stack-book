namespace AsiStackProofs.GovernanceRights

structure GovernanceTransitionReview where
  transitionAccepted : Bool
  auditCapabilityRequired : Bool
  exitCapabilityRequired : Bool
  auditCapabilityPreserved : Bool
  exitCapabilityPreserved : Bool
deriving DecidableEq, Repr

def RequiredAuditAndExitPreserved (review : GovernanceTransitionReview) : Prop :=
  (review.transitionAccepted = true ->
    review.auditCapabilityRequired = true ->
      review.auditCapabilityPreserved = true) ∧
        (review.transitionAccepted = true ->
          review.exitCapabilityRequired = true ->
            review.exitCapabilityPreserved = true)

theorem governance_transition_preserves_required_audit_and_exit_capabilities
    {review : GovernanceTransitionReview} :
    RequiredAuditAndExitPreserved review ->
    review.transitionAccepted = true ->
    review.auditCapabilityRequired = true ->
    review.exitCapabilityRequired = true ->
    review.auditCapabilityPreserved = true ∧
      review.exitCapabilityPreserved = true := by
  intro valid accepted auditRequired exitRequired
  exact ⟨valid.1 accepted auditRequired, valid.2 accepted exitRequired⟩

structure ProtectedRightRemovalReview where
  protectedRight : Bool
  rightRemoved : Bool
  rejectedOrMarkedInvalid : Bool
deriving DecidableEq, Repr

def ProtectedRightRemovalInvalid
    (review : ProtectedRightRemovalReview) : Prop :=
  review.protectedRight = true ->
    review.rightRemoved = true ->
      review.rejectedOrMarkedInvalid = true

theorem transition_removing_protected_right_is_rejected_or_invalid
    {review : ProtectedRightRemovalReview} :
    ProtectedRightRemovalInvalid review ->
    review.protectedRight = true ->
    review.rightRemoved = true ->
    review.rejectedOrMarkedInvalid = true := by
  intro valid rightProtected removed
  exact valid rightProtected removed

inductive ForkDecisionRoute where
  | allowed
  | blockedForReview
deriving DecidableEq, Repr

structure ForkGovernanceDecision where
  constrainedFork : Bool
  auditPathPreserved : Bool
  safetyObligationsPreserved : Bool
  route : ForkDecisionRoute
deriving DecidableEq, Repr

def ForkGovernanceSafe (decision : ForkGovernanceDecision) : Prop :=
  if decision.constrainedFork &&
      (!decision.auditPathPreserved || !decision.safetyObligationsPreserved) then
    decision.route = ForkDecisionRoute.blockedForReview
  else
    True

theorem constrained_fork_without_audit_path_routes_to_review
    {decision : ForkGovernanceDecision} :
    ForkGovernanceSafe decision ->
    decision.constrainedFork = true ->
    decision.auditPathPreserved = false ->
    decision.route = ForkDecisionRoute.blockedForReview := by
  intro safe constrained missingAudit
  unfold ForkGovernanceSafe at safe
  rw [constrained, missingAudit] at safe
  simp at safe
  exact safe

inductive GovernanceRightsPhase where
  | requested
  | redacted
  | forkReview
  | exitReview
  | preserved
  | blockedForReview
  | residualized
deriving DecidableEq, Repr

inductive GovernanceRightsRoute where
  | allow
  | blockForReview
  | preserveExitResidual
deriving DecidableEq, Repr

structure GovernanceRightsDecision where
  phase : GovernanceRightsPhase
  constrainedFork : Bool
  auditPathPreserved : Bool
  safetyObligationsPreserved : Bool
  redactionApplied : Bool
  redactionReasonRecorded : Bool
  appealAvailable : Bool
  exitRequired : Bool
  exitCapabilityPreserved : Bool
  protectedRightRemoved : Bool
  route : GovernanceRightsRoute
deriving DecidableEq, Repr

def GovernanceRightsRequiresReview
    (decision : GovernanceRightsDecision) : Bool :=
  (decision.constrainedFork &&
    (!decision.auditPathPreserved || !decision.safetyObligationsPreserved)) ||
      (decision.redactionApplied &&
        (!decision.redactionReasonRecorded || !decision.appealAvailable)) ||
      decision.protectedRightRemoved

def GovernanceRightsSafe (decision : GovernanceRightsDecision) : Prop :=
  if GovernanceRightsRequiresReview decision then
    decision.route = GovernanceRightsRoute.blockForReview
  else if decision.exitRequired && !decision.exitCapabilityPreserved then
    decision.route = GovernanceRightsRoute.preserveExitResidual
  else
    True

def unsafeForkWithoutSafetyObligations :
    GovernanceRightsDecision :=
  { phase := GovernanceRightsPhase.forkReview,
    constrainedFork := true,
    auditPathPreserved := true,
    safetyObligationsPreserved := false,
    redactionApplied := false,
    redactionReasonRecorded := true,
    appealAvailable := true,
    exitRequired := false,
    exitCapabilityPreserved := true,
    protectedRightRemoved := false,
    route := GovernanceRightsRoute.blockForReview }

def redactionWithoutAppealPath :
    GovernanceRightsDecision :=
  { phase := GovernanceRightsPhase.redacted,
    constrainedFork := false,
    auditPathPreserved := true,
    safetyObligationsPreserved := true,
    redactionApplied := true,
    redactionReasonRecorded := true,
    appealAvailable := false,
    exitRequired := false,
    exitCapabilityPreserved := true,
    protectedRightRemoved := false,
    route := GovernanceRightsRoute.blockForReview }

def missingExitCapabilityResidualized :
    GovernanceRightsDecision :=
  { phase := GovernanceRightsPhase.residualized,
    constrainedFork := false,
    auditPathPreserved := true,
    safetyObligationsPreserved := true,
    redactionApplied := false,
    redactionReasonRecorded := true,
    appealAvailable := true,
    exitRequired := true,
    exitCapabilityPreserved := false,
    protectedRightRemoved := false,
    route := GovernanceRightsRoute.preserveExitResidual }

theorem constrained_fork_without_safety_obligations_routes_to_review
    {decision : GovernanceRightsDecision} :
    GovernanceRightsSafe decision ->
    decision.constrainedFork = true ->
    decision.safetyObligationsPreserved = false ->
    decision.route = GovernanceRightsRoute.blockForReview := by
  intro safe constrained missingSafety
  unfold GovernanceRightsSafe GovernanceRightsRequiresReview at safe
  rw [constrained, missingSafety] at safe
  simp at safe
  exact safe

theorem redaction_without_appeal_path_routes_to_review
    {decision : GovernanceRightsDecision} :
    GovernanceRightsSafe decision ->
    decision.redactionApplied = true ->
    decision.appealAvailable = false ->
    decision.route = GovernanceRightsRoute.blockForReview := by
  intro safe redacted missingAppeal
  unfold GovernanceRightsSafe GovernanceRightsRequiresReview at safe
  rw [redacted, missingAppeal] at safe
  simp at safe
  exact safe

theorem missing_exit_capability_preserves_exit_residual
    {decision : GovernanceRightsDecision} :
    GovernanceRightsSafe decision ->
    GovernanceRightsRequiresReview decision = false ->
    decision.exitRequired = true ->
    decision.exitCapabilityPreserved = false ->
    decision.route = GovernanceRightsRoute.preserveExitResidual := by
  intro safe noReviewRequired exitRequired missingExit
  unfold GovernanceRightsSafe at safe
  rw [noReviewRequired, exitRequired, missingExit] at safe
  simp at safe
  exact safe

inductive GovernanceRightLifecycleRoute where
  | rejectMissingGovernanceRecord
  | requestAuditMaterial
  | requestRedactionAppeal
  | requestExitExport
  | blockUnsafeFork
  | preserveForkObligations
  | blockProtectedRightRemoval
  | preserveDissentRecord
  | preserveReplacementObligations
  | preserveDurableReceipt
  | requestEvidenceTransition
  | allowContestableTransition
deriving DecidableEq, Repr

structure GovernanceRightLifecycle where
  governanceActionRequested : Bool
  auditRequested : Bool
  auditMaterialPresent : Bool
  redactionApplied : Bool
  redactionReasonRecorded : Bool
  redactionAppealAvailable : Bool
  exitRequested : Bool
  exitExportAvailable : Bool
  portableStateBoundaryRecorded : Bool
  forkRequested : Bool
  forkSafetyReviewPassed : Bool
  forkObligationsPreserved : Bool
  protectedRightRemoved : Bool
  dissentPresent : Bool
  dissentRecorded : Bool
  replacementRequested : Bool
  rightsReceiptsPreservedByReplacement : Bool
  durableReceiptRecorded : Bool
  supportStateChangeRequested : Bool
  evidenceTransitionRecordPresent : Bool
deriving DecidableEq, Repr

def GovernanceRightLifecycleRouteFor
    (review : GovernanceRightLifecycle) : GovernanceRightLifecycleRoute :=
  if review.governanceActionRequested = false then
    GovernanceRightLifecycleRoute.rejectMissingGovernanceRecord
  else if review.auditRequested = true ∧
      review.auditMaterialPresent = false then
    GovernanceRightLifecycleRoute.requestAuditMaterial
  else if review.redactionApplied = true ∧
      (review.redactionReasonRecorded = false ∨
        review.redactionAppealAvailable = false) then
    GovernanceRightLifecycleRoute.requestRedactionAppeal
  else if review.exitRequested = true ∧
      (review.exitExportAvailable = false ∨
        review.portableStateBoundaryRecorded = false) then
    GovernanceRightLifecycleRoute.requestExitExport
  else if review.forkRequested = true ∧ review.forkSafetyReviewPassed = false then
    GovernanceRightLifecycleRoute.blockUnsafeFork
  else if review.forkRequested = true ∧
      review.forkObligationsPreserved = false then
    GovernanceRightLifecycleRoute.preserveForkObligations
  else if review.protectedRightRemoved = true then
    GovernanceRightLifecycleRoute.blockProtectedRightRemoval
  else if review.dissentPresent = true ∧ review.dissentRecorded = false then
    GovernanceRightLifecycleRoute.preserveDissentRecord
  else if review.replacementRequested = true ∧
      review.rightsReceiptsPreservedByReplacement = false then
    GovernanceRightLifecycleRoute.preserveReplacementObligations
  else if review.durableReceiptRecorded = false then
    GovernanceRightLifecycleRoute.preserveDurableReceipt
  else if review.supportStateChangeRequested = true ∧
      review.evidenceTransitionRecordPresent = false then
    GovernanceRightLifecycleRoute.requestEvidenceTransition
  else
    GovernanceRightLifecycleRoute.allowContestableTransition

theorem missing_governance_record_rejected :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := false,
      auditRequested := false,
      auditMaterialPresent := false,
      redactionApplied := false,
      redactionReasonRecorded := false,
      redactionAppealAvailable := false,
      exitRequested := false,
      exitExportAvailable := false,
      portableStateBoundaryRecorded := false,
      forkRequested := false,
      forkSafetyReviewPassed := false,
      forkObligationsPreserved := false,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := false,
      durableReceiptRecorded := false,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := false
    } = GovernanceRightLifecycleRoute.rejectMissingGovernanceRecord := by
  simp [GovernanceRightLifecycleRouteFor]

theorem audit_request_without_material_requests_audit_material :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := true,
      auditMaterialPresent := false,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := false,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.requestAuditMaterial := by
  simp [GovernanceRightLifecycleRouteFor]

theorem redaction_without_appeal_requests_redaction_appeal :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := true,
      redactionReasonRecorded := true,
      redactionAppealAvailable := false,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := false,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.requestRedactionAppeal := by
  simp [GovernanceRightLifecycleRouteFor]

theorem exit_without_portable_state_requests_exit_export :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := true,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := false,
      forkRequested := false,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.requestExitExport := by
  simp [GovernanceRightLifecycleRouteFor]

theorem fork_without_safety_review_blocks_unsafe_fork :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := true,
      forkSafetyReviewPassed := false,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.blockUnsafeFork := by
  simp [GovernanceRightLifecycleRouteFor]

theorem fork_without_obligation_preservation_preserves_fork_obligations :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := true,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := false,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.preserveForkObligations := by
  simp [GovernanceRightLifecycleRouteFor]

theorem protected_right_removal_blocks_lifecycle :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := false,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := true,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.blockProtectedRightRemoval := by
  simp [GovernanceRightLifecycleRouteFor]

theorem dissent_without_record_preserves_dissent :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := false,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := true,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.preserveDissentRecord := by
  simp [GovernanceRightLifecycleRouteFor]

theorem replacement_without_rights_receipts_preserves_obligations :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := false,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := true,
      rightsReceiptsPreservedByReplacement := false,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.preserveReplacementObligations := by
  simp [GovernanceRightLifecycleRouteFor]

theorem missing_durable_receipt_preserves_receipt :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := false,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := false,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.preserveDurableReceipt := by
  simp [GovernanceRightLifecycleRouteFor]

theorem support_change_without_evidence_transition_requests_governance_evidence :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := false,
      auditMaterialPresent := true,
      redactionApplied := false,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := false,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := false,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := false,
      dissentRecorded := false,
      replacementRequested := false,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := true,
      evidenceTransitionRecordPresent := false
    } = GovernanceRightLifecycleRoute.requestEvidenceTransition := by
  simp [GovernanceRightLifecycleRouteFor]

theorem complete_governance_right_lifecycle_allows_transition :
    GovernanceRightLifecycleRouteFor {
      governanceActionRequested := true,
      auditRequested := true,
      auditMaterialPresent := true,
      redactionApplied := true,
      redactionReasonRecorded := true,
      redactionAppealAvailable := true,
      exitRequested := true,
      exitExportAvailable := true,
      portableStateBoundaryRecorded := true,
      forkRequested := true,
      forkSafetyReviewPassed := true,
      forkObligationsPreserved := true,
      protectedRightRemoved := false,
      dissentPresent := true,
      dissentRecorded := true,
      replacementRequested := true,
      rightsReceiptsPreservedByReplacement := true,
      durableReceiptRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = GovernanceRightLifecycleRoute.allowContestableTransition := by
  simp [GovernanceRightLifecycleRouteFor]

end AsiStackProofs.GovernanceRights
