namespace AsiStackProofs.GovernanceRights

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

structure TheseusGovernanceRightsReceiptSuiteSummary where
  triggerGreen : Bool
  governanceFixtureCount : Nat
  governancePassedCount : Nat
  constitutionalFixtureCount : Nat
  constitutionalPassedCount : Nat
  governanceRightRecordCount : Nat
  constitutionalPredicateRecordCount : Nat
  evidenceTransitionRecordCount : Nat
  artifactGraphRecordCount : Nat
  failureBoundaryRecordCount : Nat
  publicTrainingRowsWritten : Nat
  externalInferenceCalls : Nat
  fallbackReturnCount : Nat
  hardGapCount : Nat
  warningCount : Nat
  rawPrivatePayloadCopied : Bool
  pathFieldsRedacted : Bool
  chapterCorePromotionClaimed : Bool
  constitutionalChapterCorePromotionClaimed : Bool
  legalRightsClaimed : Bool
  institutionalGovernanceClaimed : Bool
  moralCorrectnessClaimed : Bool
  reviewerIndependenceClaimed : Bool
  deployedRuntimeEnforcementClaimed : Bool
  cleanLiveTheseusReplayClaimed : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def TheseusGovernanceRightsReceiptSuiteCarriesRecords
    (summary : TheseusGovernanceRightsReceiptSuiteSummary) : Prop :=
  summary.triggerGreen = true ∧
    summary.governanceFixtureCount = 4 ∧
      summary.governancePassedCount = 4 ∧
        summary.constitutionalFixtureCount = 4 ∧
          summary.constitutionalPassedCount = 4 ∧
            summary.governanceRightRecordCount = 4 ∧
              summary.constitutionalPredicateRecordCount = 4 ∧
                summary.evidenceTransitionRecordCount = 8 ∧
                  summary.artifactGraphRecordCount = 8 ∧
                    summary.failureBoundaryRecordCount = 8

def TheseusGovernanceRightsReceiptSuitePublicSafe
    (summary : TheseusGovernanceRightsReceiptSuiteSummary) : Prop :=
  summary.publicTrainingRowsWritten = 0 ∧
    summary.externalInferenceCalls = 0 ∧
      summary.fallbackReturnCount = 0 ∧
        summary.hardGapCount = 0 ∧
          summary.warningCount = 0 ∧
            summary.rawPrivatePayloadCopied = false ∧
              summary.pathFieldsRedacted = true

def TheseusGovernanceRightsReceiptSuitePreservesBoundaries
    (summary : TheseusGovernanceRightsReceiptSuiteSummary) : Prop :=
  summary.chapterCorePromotionClaimed = false ∧
    summary.constitutionalChapterCorePromotionClaimed = false ∧
      summary.legalRightsClaimed = false ∧
        summary.institutionalGovernanceClaimed = false ∧
          summary.moralCorrectnessClaimed = false ∧
            summary.reviewerIndependenceClaimed = false ∧
              summary.deployedRuntimeEnforcementClaimed = false ∧
                summary.cleanLiveTheseusReplayClaimed = false ∧
                  summary.nonClaimBoundaryRecorded = true

def TheseusGovernanceRightsReceiptSuiteImportValid
    (summary : TheseusGovernanceRightsReceiptSuiteSummary) : Prop :=
  TheseusGovernanceRightsReceiptSuiteCarriesRecords summary ∧
    TheseusGovernanceRightsReceiptSuitePublicSafe summary ∧
      TheseusGovernanceRightsReceiptSuitePreservesBoundaries summary

def theseusGovernanceRightsReceiptSuiteImportFixture :
    TheseusGovernanceRightsReceiptSuiteSummary := {
  triggerGreen := true
  governanceFixtureCount := 4
  governancePassedCount := 4
  constitutionalFixtureCount := 4
  constitutionalPassedCount := 4
  governanceRightRecordCount := 4
  constitutionalPredicateRecordCount := 4
  evidenceTransitionRecordCount := 8
  artifactGraphRecordCount := 8
  failureBoundaryRecordCount := 8
  publicTrainingRowsWritten := 0
  externalInferenceCalls := 0
  fallbackReturnCount := 0
  hardGapCount := 0
  warningCount := 0
  rawPrivatePayloadCopied := false
  pathFieldsRedacted := true
  chapterCorePromotionClaimed := false
  constitutionalChapterCorePromotionClaimed := false
  legalRightsClaimed := false
  institutionalGovernanceClaimed := false
  moralCorrectnessClaimed := false
  reviewerIndependenceClaimed := false
  deployedRuntimeEnforcementClaimed := false
  cleanLiveTheseusReplayClaimed := false
  nonClaimBoundaryRecorded := true
}

theorem theseus_governance_rights_receipt_suite_import_fixture_valid :
    TheseusGovernanceRightsReceiptSuiteImportValid
      theseusGovernanceRightsReceiptSuiteImportFixture := by
  simp [
    TheseusGovernanceRightsReceiptSuiteImportValid,
    TheseusGovernanceRightsReceiptSuiteCarriesRecords,
    TheseusGovernanceRightsReceiptSuitePublicSafe,
    TheseusGovernanceRightsReceiptSuitePreservesBoundaries,
    theseusGovernanceRightsReceiptSuiteImportFixture,
  ]

theorem theseus_governance_rights_receipt_suite_import_core_promotion_rejected :
    ¬ TheseusGovernanceRightsReceiptSuiteImportValid
      { theseusGovernanceRightsReceiptSuiteImportFixture with
        chapterCorePromotionClaimed := true } := by
  intro valid
  simp [
    TheseusGovernanceRightsReceiptSuiteImportValid,
    TheseusGovernanceRightsReceiptSuiteCarriesRecords,
    TheseusGovernanceRightsReceiptSuitePublicSafe,
    TheseusGovernanceRightsReceiptSuitePreservesBoundaries,
    theseusGovernanceRightsReceiptSuiteImportFixture,
  ] at valid

theorem theseus_governance_rights_receipt_suite_import_legal_rights_overclaim_rejected :
    ¬ TheseusGovernanceRightsReceiptSuiteImportValid
      { theseusGovernanceRightsReceiptSuiteImportFixture with
        legalRightsClaimed := true } := by
  intro valid
  simp [
    TheseusGovernanceRightsReceiptSuiteImportValid,
    TheseusGovernanceRightsReceiptSuiteCarriesRecords,
    TheseusGovernanceRightsReceiptSuitePublicSafe,
    TheseusGovernanceRightsReceiptSuitePreservesBoundaries,
    theseusGovernanceRightsReceiptSuiteImportFixture,
  ] at valid

end AsiStackProofs.GovernanceRights
