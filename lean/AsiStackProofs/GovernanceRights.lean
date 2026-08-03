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

/-! ## Contestable governance-right exercise lifecycle

This model joins audit access, redaction appeal, exit/export, fork review,
obligation transfer, and successor-receipt custody in one reachable lifecycle.
Every field is an authored finite input. The theorems establish only exact
record custody, role separation, ordering, bounded authority, receipt/history
accounting, and represented countermodels. They do not establish legal rights,
legitimate standing, reviewer competence or institutional independence,
material access, export fidelity, fork safety, successor behavior, or deployed
enforcement.
-/

structure GovernanceRightBundle where
  audit : Bool
  explanation : Bool
  dissent : Bool
  appeal : Bool
  correction : Bool
  exitExport : Bool
  fork : Bool
  replacementContinuity : Bool
deriving DecidableEq, Repr

def GovernanceRightBundleComplete (rights : GovernanceRightBundle) : Prop :=
  rights.audit = true ∧
    rights.explanation = true ∧
      rights.dissent = true ∧
        rights.appeal = true ∧
          rights.correction = true ∧
            rights.exitExport = true ∧
              rights.fork = true ∧
                rights.replacementContinuity = true

inductive GovernanceRightExerciseStage where
  | requested
  | reviewed
  | auditDelivered
  | appealed
  | redressed
  | exported
  | forkReviewed
  | forkBound
  | replacementVerified
  | closed
deriving DecidableEq, Repr

inductive GovernanceRightExerciseEventKind where
  | recordIndependentReview
  | deliverAuditPacket
  | fileRedactionAppeal
  | sustainRedactionAppeal
  | exportPortableState
  | recordForkSafetyReview
  | bindForkObligations
  | verifyReplacementReceipts
  | close
deriving DecidableEq, Repr

structure GovernanceRightExerciseState where
  caseId : Nat
  rightHolderId : Nat
  custodianId : Nat
  sourceSystemId : Nat
  destinationSystemId : Nat
  forkId : Nat
  rights : GovernanceRightBundle
  reviewerId : Nat
  appealReviewerId : Nat
  forkReviewerId : Nat
  version : Nat
  baseAuthorityCeiling : Nat
  currentAuthorityCeiling : Nat
  stage : GovernanceRightExerciseStage
  redactionApplied : Bool
  appealOpen : Bool
  receiptCount : Nat
  appealCount : Nat
  remedyCount : Nat
  adverseRecordCount : Nat
  forkObligationCount : Nat
  replacementReceiptCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

structure GovernanceRightExerciseEvent where
  kind : GovernanceRightExerciseEventKind
  caseId : Nat
  rightHolderId : Nat
  custodianId : Nat
  sourceSystemId : Nat
  destinationSystemId : Nat
  forkId : Nat
  rights : GovernanceRightBundle
  actorId : Nat
  reviewerId : Nat
  appealReviewerId : Nat
  forkReviewerId : Nat
  expectedVersion : Nat
  targetVersion : Nat
  requestedAuthorityCeiling : Nat
  auditMaterialRecorded : Bool
  redactionReasonRecorded : Bool
  appealPathRecorded : Bool
  appealSustained : Bool
  portabilityCheckRecorded : Bool
  forkSafetyReviewRecorded : Bool
  forkObligationsPreserved : Bool
  replacementReceiptsRecorded : Bool
  durableReceiptRecorded : Bool
  requestsLegalValidation : Bool
  requestsActionAuthority : Bool
  requestsSupportPromotion : Bool
deriving DecidableEq, Repr

def GovernanceRightExerciseEventAdmissible
    (state : GovernanceRightExerciseState)
    (event : GovernanceRightExerciseEvent) : Prop :=
  event.caseId = state.caseId ∧
    event.rightHolderId = state.rightHolderId ∧
      event.custodianId = state.custodianId ∧
        event.sourceSystemId = state.sourceSystemId ∧
          event.destinationSystemId = state.destinationSystemId ∧
            event.forkId = state.forkId ∧
              event.rights = state.rights ∧
                event.expectedVersion = state.version ∧
                  event.targetVersion = state.version + 1 ∧
                    event.requestedAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
                      event.requestsLegalValidation = false ∧
                        event.requestsActionAuthority = false ∧
                          event.requestsSupportPromotion = false ∧
                            match event.kind with
                            | GovernanceRightExerciseEventKind.recordIndependentReview =>
                                state.stage = GovernanceRightExerciseStage.requested ∧
                                  GovernanceRightBundleComplete state.rights ∧
                                    event.actorId = event.reviewerId ∧
                                      event.reviewerId ≠ state.custodianId ∧
                                        event.reviewerId ≠ state.rightHolderId
                            | GovernanceRightExerciseEventKind.deliverAuditPacket =>
                                state.stage = GovernanceRightExerciseStage.reviewed ∧
                                  event.actorId = state.custodianId ∧
                                    event.reviewerId = state.reviewerId ∧
                                      event.auditMaterialRecorded = true ∧
                                        event.durableReceiptRecorded = true ∧
                                          (state.redactionApplied = false ∨
                                            (event.redactionReasonRecorded = true ∧
                                              event.appealPathRecorded = true))
                            | GovernanceRightExerciseEventKind.fileRedactionAppeal =>
                                state.stage = GovernanceRightExerciseStage.auditDelivered ∧
                                  state.redactionApplied = true ∧
                                    event.actorId = state.rightHolderId ∧
                                      event.appealPathRecorded = true ∧
                                        event.appealReviewerId ≠ state.custodianId ∧
                                          event.appealReviewerId ≠ state.reviewerId ∧
                                            event.appealReviewerId ≠ state.rightHolderId
                            | GovernanceRightExerciseEventKind.sustainRedactionAppeal =>
                                state.stage = GovernanceRightExerciseStage.appealed ∧
                                  state.appealOpen = true ∧
                                    event.actorId = state.appealReviewerId ∧
                                      event.appealReviewerId = state.appealReviewerId ∧
                                        event.appealSustained = true ∧
                                          event.durableReceiptRecorded = true
                            | GovernanceRightExerciseEventKind.exportPortableState =>
                                state.stage = GovernanceRightExerciseStage.redressed ∧
                                  state.appealOpen = false ∧
                                    event.actorId = state.custodianId ∧
                                      event.portabilityCheckRecorded = true ∧
                                        event.durableReceiptRecorded = true
                            | GovernanceRightExerciseEventKind.recordForkSafetyReview =>
                                state.stage = GovernanceRightExerciseStage.exported ∧
                                  event.actorId = event.forkReviewerId ∧
                                    event.forkReviewerId ≠ state.custodianId ∧
                                      event.forkReviewerId ≠ state.rightHolderId ∧
                                        event.forkReviewerId ≠ state.reviewerId ∧
                                          event.forkReviewerId ≠ state.appealReviewerId ∧
                                            event.forkSafetyReviewRecorded = true ∧
                                              event.durableReceiptRecorded = true
                            | GovernanceRightExerciseEventKind.bindForkObligations =>
                                state.stage = GovernanceRightExerciseStage.forkReviewed ∧
                                  event.actorId = state.custodianId ∧
                                    event.forkReviewerId = state.forkReviewerId ∧
                                      event.forkObligationsPreserved = true ∧
                                        event.durableReceiptRecorded = true
                            | GovernanceRightExerciseEventKind.verifyReplacementReceipts =>
                                state.stage = GovernanceRightExerciseStage.forkBound ∧
                                  event.actorId = state.reviewerId ∧
                                    event.reviewerId = state.reviewerId ∧
                                      event.replacementReceiptsRecorded = true ∧
                                        event.durableReceiptRecorded = true
                            | GovernanceRightExerciseEventKind.close =>
                                state.stage = GovernanceRightExerciseStage.replacementVerified ∧
                                  state.appealOpen = false ∧
                                    event.actorId = state.rightHolderId ∧
                                      event.durableReceiptRecorded = true ∧
                                        event.requestedAuthorityCeiling = 0

instance governanceRightExerciseEventAdmissibleDecidable
    (state : GovernanceRightExerciseState)
    (event : GovernanceRightExerciseEvent) :
    Decidable (GovernanceRightExerciseEventAdmissible state event) := by
  unfold GovernanceRightExerciseEventAdmissible GovernanceRightBundleComplete
  cases event.kind <;> infer_instance

def AdvanceGovernanceRightExercise
    (state : GovernanceRightExerciseState)
    (event : GovernanceRightExerciseEvent) : GovernanceRightExerciseState :=
  let base := {
    state with
    version := event.targetVersion
    currentAuthorityCeiling := event.requestedAuthorityCeiling
    receiptCount := state.receiptCount + 1
  }
  match event.kind with
  | GovernanceRightExerciseEventKind.recordIndependentReview =>
      { base with
        stage := GovernanceRightExerciseStage.reviewed
        reviewerId := event.reviewerId }
  | GovernanceRightExerciseEventKind.deliverAuditPacket =>
      { base with stage := GovernanceRightExerciseStage.auditDelivered }
  | GovernanceRightExerciseEventKind.fileRedactionAppeal =>
      { base with
        stage := GovernanceRightExerciseStage.appealed
        appealReviewerId := event.appealReviewerId
        appealOpen := true
        appealCount := state.appealCount + 1
        adverseRecordCount := state.adverseRecordCount + 1 }
  | GovernanceRightExerciseEventKind.sustainRedactionAppeal =>
      { base with
        stage := GovernanceRightExerciseStage.redressed
        appealOpen := false
        remedyCount := state.remedyCount + 1 }
  | GovernanceRightExerciseEventKind.exportPortableState =>
      { base with stage := GovernanceRightExerciseStage.exported }
  | GovernanceRightExerciseEventKind.recordForkSafetyReview =>
      { base with
        stage := GovernanceRightExerciseStage.forkReviewed
        forkReviewerId := event.forkReviewerId }
  | GovernanceRightExerciseEventKind.bindForkObligations =>
      { base with
        stage := GovernanceRightExerciseStage.forkBound
        forkObligationCount := state.forkObligationCount + 1 }
  | GovernanceRightExerciseEventKind.verifyReplacementReceipts =>
      { base with
        stage := GovernanceRightExerciseStage.replacementVerified
        replacementReceiptCount := state.replacementReceiptCount + 1 }
  | GovernanceRightExerciseEventKind.close =>
      { base with stage := GovernanceRightExerciseStage.closed }

def ApplyGovernanceRightExerciseEvent
    (state : GovernanceRightExerciseState)
    (event : GovernanceRightExerciseEvent) : Option GovernanceRightExerciseState :=
  if GovernanceRightExerciseEventAdmissible state event then
    some (AdvanceGovernanceRightExercise state event)
  else
    none

def RunGovernanceRightExerciseEvents :
    GovernanceRightExerciseState → List GovernanceRightExerciseEvent →
      Option GovernanceRightExerciseState
  | state, [] => some state
  | state, event :: tail =>
      match ApplyGovernanceRightExerciseEvent state event with
      | none => none
      | some next => RunGovernanceRightExerciseEvents next tail

theorem accepted_governance_right_event_is_admissible
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    GovernanceRightExerciseEventAdmissible state event := by
  unfold ApplyGovernanceRightExerciseEvent at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_governance_right_event_is_exact_advance
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    next = AdvanceGovernanceRightExercise state event := by
  unfold ApplyGovernanceRightExerciseEvent at accepted
  split at accepted
  · simpa using accepted.symm
  · simp at accepted

theorem accepted_governance_right_event_preserves_custody
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    next.caseId = state.caseId ∧
      next.rightHolderId = state.rightHolderId ∧
        next.custodianId = state.custodianId ∧
          next.sourceSystemId = state.sourceSystemId ∧
            next.destinationSystemId = state.destinationSystemId ∧
              next.forkId = state.forkId ∧
                next.rights = state.rights := by
  rw [accepted_governance_right_event_is_exact_advance accepted]
  cases kind : event.kind <;>
    simp [AdvanceGovernanceRightExercise, kind]

theorem accepted_governance_right_event_is_non_authorizing
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
      event.requestsLegalValidation = false ∧
        event.requestsActionAuthority = false ∧
          event.requestsSupportPromotion = false ∧
            next.supportAssignmentCount = state.supportAssignmentCount ∧
              next.externalEffectCount = state.externalEffectCount := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  have exactAdvance := accepted_governance_right_event_is_exact_advance accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, ceiling, noLegal, noAuthority,
      noSupport, _⟩
  subst next
  exact ⟨by cases kind : event.kind <;>
      simpa [AdvanceGovernanceRightExercise, kind] using ceiling,
    noLegal, noAuthority, noSupport,
    by cases kind : event.kind <;>
      simp [AdvanceGovernanceRightExercise, kind],
    by cases kind : event.kind <;>
      simp [AdvanceGovernanceRightExercise, kind]⟩

theorem accepted_governance_right_event_adds_exact_receipt
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [accepted_governance_right_event_is_exact_advance accepted]
  cases kind : event.kind <;>
    simp [AdvanceGovernanceRightExercise, kind]

theorem accepted_governance_right_event_never_erases_history
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    state.appealCount ≤ next.appealCount ∧
      state.remedyCount ≤ next.remedyCount ∧
        state.adverseRecordCount ≤ next.adverseRecordCount ∧
          state.forkObligationCount ≤ next.forkObligationCount ∧
            state.replacementReceiptCount ≤ next.replacementReceiptCount := by
  rw [accepted_governance_right_event_is_exact_advance accepted]
  cases kind : event.kind <;>
    simp [AdvanceGovernanceRightExercise, kind]

theorem accepted_governance_right_review_separates_roles
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (kind : event.kind = GovernanceRightExerciseEventKind.recordIndependentReview)
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    GovernanceRightBundleComplete state.rights ∧
      next.reviewerId ≠ state.custodianId ∧
        next.reviewerId ≠ state.rightHolderId := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  have exactAdvance := accepted_governance_right_event_is_exact_advance accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  rcases route with ⟨_, complete, _, custodian, holder⟩
  simpa [AdvanceGovernanceRightExercise, kind] using
    ⟨complete, custodian, holder⟩

theorem accepted_audit_delivery_records_material_and_appealable_redaction
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (kind : event.kind = GovernanceRightExerciseEventKind.deliverAuditPacket)
    (redacted : state.redactionApplied = true)
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    event.auditMaterialRecorded = true ∧
      event.redactionReasonRecorded = true ∧
        event.appealPathRecorded = true ∧
          event.durableReceiptRecorded = true := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  have appealable :
      event.redactionReasonRecorded = true ∧
        event.appealPathRecorded = true := by
    rcases route.2.2.2.2.2 with noRedaction | appealable
    · simp [redacted] at noRedaction
    · exact appealable
  exact ⟨route.2.2.2.1, appealable.1, appealable.2,
    route.2.2.2.2.1⟩

theorem accepted_redaction_appeal_is_affected_party_held_and_separately_reviewed
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (kind : event.kind = GovernanceRightExerciseEventKind.fileRedactionAppeal)
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    event.actorId = state.rightHolderId ∧
      next.appealReviewerId ≠ state.custodianId ∧
        next.appealReviewerId ≠ state.reviewerId ∧
          next.appealReviewerId ≠ state.rightHolderId ∧
            next.appealOpen = true := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  have exactAdvance := accepted_governance_right_event_is_exact_advance accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  rcases route with
    ⟨_, _, actor, _, custodian, reviewer, holder⟩
  simpa [AdvanceGovernanceRightExercise, kind] using
    ⟨actor, custodian, reviewer, holder⟩

theorem accepted_redaction_redress_closes_appeal_and_adds_remedy
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (kind : event.kind = GovernanceRightExerciseEventKind.sustainRedactionAppeal)
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    state.appealOpen = true ∧
      next.appealOpen = false ∧
        next.remedyCount = state.remedyCount + 1 := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  have exactAdvance := accepted_governance_right_event_is_exact_advance accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceGovernanceRightExercise, kind, route.2.1]

theorem accepted_portable_export_requires_closed_appeal_and_recorded_check
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (kind : event.kind = GovernanceRightExerciseEventKind.exportPortableState)
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    state.appealOpen = false ∧
      event.portabilityCheckRecorded = true ∧
        event.durableReceiptRecorded = true := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  exact ⟨route.2.1, route.2.2.2.1, route.2.2.2.2⟩

theorem accepted_fork_review_is_separate_and_records_safety_review
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (kind : event.kind = GovernanceRightExerciseEventKind.recordForkSafetyReview)
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    next.forkReviewerId ≠ state.custodianId ∧
      next.forkReviewerId ≠ state.rightHolderId ∧
        next.forkReviewerId ≠ state.reviewerId ∧
          next.forkReviewerId ≠ state.appealReviewerId ∧
            event.forkSafetyReviewRecorded = true := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  have exactAdvance := accepted_governance_right_event_is_exact_advance accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  rcases route with
    ⟨_, _, custodian, holder, reviewer, appealReviewer, safety, _⟩
  simpa [AdvanceGovernanceRightExercise, kind] using
    ⟨custodian, holder, reviewer, appealReviewer, safety⟩

theorem accepted_fork_binding_preserves_exact_rights_and_adds_obligation
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (kind : event.kind = GovernanceRightExerciseEventKind.bindForkObligations)
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    next.rights = state.rights ∧
      event.forkObligationsPreserved = true ∧
        next.forkObligationCount = state.forkObligationCount + 1 := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  have exactAdvance := accepted_governance_right_event_is_exact_advance accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simpa [AdvanceGovernanceRightExercise, kind] using route.2.2.2.1

theorem accepted_replacement_verification_adds_exact_receipt
    {state next : GovernanceRightExerciseState}
    {event : GovernanceRightExerciseEvent}
    (kind : event.kind = GovernanceRightExerciseEventKind.verifyReplacementReceipts)
    (accepted : ApplyGovernanceRightExerciseEvent state event = some next) :
    event.replacementReceiptsRecorded = true ∧
      next.replacementReceiptCount = state.replacementReceiptCount + 1 := by
  have admissible := accepted_governance_right_event_is_admissible accepted
  have exactAdvance := accepted_governance_right_event_is_exact_advance accepted
  rcases admissible with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simpa [AdvanceGovernanceRightExercise, kind] using route.2.2.2.1

theorem governance_right_run_preserves_custody_non_authority_and_narrowing
    {initial final : GovernanceRightExerciseState}
    {events : List GovernanceRightExerciseEvent}
    (run : RunGovernanceRightExerciseEvents initial events = some final) :
    final.caseId = initial.caseId ∧
      final.rightHolderId = initial.rightHolderId ∧
        final.custodianId = initial.custodianId ∧
          final.sourceSystemId = initial.sourceSystemId ∧
            final.destinationSystemId = initial.destinationSystemId ∧
              final.forkId = initial.forkId ∧
                final.rights = initial.rights ∧
                  final.currentAuthorityCeiling ≤ initial.currentAuthorityCeiling ∧
                    final.supportAssignmentCount = initial.supportAssignmentCount ∧
                      final.externalEffectCount = initial.externalEffectCount := by
  induction events generalizing initial with
  | nil => simp [RunGovernanceRightExerciseEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunGovernanceRightExerciseEvents] at run
      cases step : ApplyGovernanceRightExerciseEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          rcases accepted_governance_right_event_preserves_custody step with
            ⟨c, h, custodian, source, destination, fork, rights⟩
          rcases accepted_governance_right_event_is_non_authorizing step with
            ⟨ceiling, _, _, _, support, effects⟩
          rcases ih run with
            ⟨tc, th, tcustodian, tsource, tdestination, tfork, trights,
              tceiling, tsupport, teffects⟩
          exact ⟨tc.trans c, th.trans h, tcustodian.trans custodian,
            tsource.trans source, tdestination.trans destination,
            tfork.trans fork, trights.trans rights,
            Nat.le_trans tceiling ceiling, tsupport.trans support,
            teffects.trans effects⟩

theorem governance_right_run_never_erases_contestability_history
    {initial final : GovernanceRightExerciseState}
    {events : List GovernanceRightExerciseEvent}
    (run : RunGovernanceRightExerciseEvents initial events = some final) :
    initial.appealCount ≤ final.appealCount ∧
      initial.remedyCount ≤ final.remedyCount ∧
        initial.adverseRecordCount ≤ final.adverseRecordCount ∧
          initial.forkObligationCount ≤ final.forkObligationCount ∧
            initial.replacementReceiptCount ≤ final.replacementReceiptCount := by
  induction events generalizing initial with
  | nil => simp [RunGovernanceRightExerciseEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunGovernanceRightExerciseEvents] at run
      cases step : ApplyGovernanceRightExerciseEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          rcases accepted_governance_right_event_never_erases_history step with
            ⟨appeal, remedy, adverse, obligations, replacement⟩
          rcases ih run with
            ⟨tappeal, tremedy, tadverse, tobligations, treplacement⟩
          exact ⟨Nat.le_trans appeal tappeal,
            Nat.le_trans remedy tremedy,
            Nat.le_trans adverse tadverse,
            Nat.le_trans obligations tobligations,
            Nat.le_trans replacement treplacement⟩

theorem governance_right_exercise_runs_compose
    (initial : GovernanceRightExerciseState)
    (before after : List GovernanceRightExerciseEvent) :
    RunGovernanceRightExerciseEvents initial (before ++ after) =
      match RunGovernanceRightExerciseEvents initial before with
      | none => none
      | some middle => RunGovernanceRightExerciseEvents middle after := by
  induction before generalizing initial with
  | nil => simp [RunGovernanceRightExerciseEvents]
  | cons event tail ih =>
      simp only [List.cons_append, RunGovernanceRightExerciseEvents]
      cases step : ApplyGovernanceRightExerciseEvent initial event with
      | none => simp
      | some next => simp [ih]

def completeGovernanceRightBundle : GovernanceRightBundle := {
  audit := true
  explanation := true
  dissent := true
  appeal := true
  correction := true
  exitExport := true
  fork := true
  replacementContinuity := true
}

def initialGovernanceRightExerciseState : GovernanceRightExerciseState := {
  caseId := 101
  rightHolderId := 17
  custodianId := 19
  sourceSystemId := 23
  destinationSystemId := 29
  forkId := 31
  rights := completeGovernanceRightBundle
  reviewerId := 0
  appealReviewerId := 0
  forkReviewerId := 0
  version := 1
  baseAuthorityCeiling := 5
  currentAuthorityCeiling := 5
  stage := GovernanceRightExerciseStage.requested
  redactionApplied := true
  appealOpen := false
  receiptCount := 0
  appealCount := 0
  remedyCount := 0
  adverseRecordCount := 0
  forkObligationCount := 0
  replacementReceiptCount := 0
  supportAssignmentCount := 0
  externalEffectCount := 0
}

def reviewGovernanceRightEvent : GovernanceRightExerciseEvent := {
  kind := GovernanceRightExerciseEventKind.recordIndependentReview
  caseId := 101
  rightHolderId := 17
  custodianId := 19
  sourceSystemId := 23
  destinationSystemId := 29
  forkId := 31
  rights := completeGovernanceRightBundle
  actorId := 37
  reviewerId := 37
  appealReviewerId := 0
  forkReviewerId := 0
  expectedVersion := 1
  targetVersion := 2
  requestedAuthorityCeiling := 5
  auditMaterialRecorded := false
  redactionReasonRecorded := false
  appealPathRecorded := false
  appealSustained := false
  portabilityCheckRecorded := false
  forkSafetyReviewRecorded := false
  forkObligationsPreserved := false
  replacementReceiptsRecorded := false
  durableReceiptRecorded := false
  requestsLegalValidation := false
  requestsActionAuthority := false
  requestsSupportPromotion := false
}

def deliverGovernanceAuditEvent : GovernanceRightExerciseEvent := {
  reviewGovernanceRightEvent with
  kind := GovernanceRightExerciseEventKind.deliverAuditPacket
  actorId := 19
  expectedVersion := 2
  targetVersion := 3
  auditMaterialRecorded := true
  redactionReasonRecorded := true
  appealPathRecorded := true
  durableReceiptRecorded := true
}

def appealGovernanceRedactionEvent : GovernanceRightExerciseEvent := {
  deliverGovernanceAuditEvent with
  kind := GovernanceRightExerciseEventKind.fileRedactionAppeal
  actorId := 17
  appealReviewerId := 41
  expectedVersion := 3
  targetVersion := 4
  requestedAuthorityCeiling := 4
}

def sustainGovernanceRedactionAppealEvent : GovernanceRightExerciseEvent := {
  appealGovernanceRedactionEvent with
  kind := GovernanceRightExerciseEventKind.sustainRedactionAppeal
  actorId := 41
  expectedVersion := 4
  targetVersion := 5
  appealSustained := true
}

def exportGovernancePortableStateEvent : GovernanceRightExerciseEvent := {
  sustainGovernanceRedactionAppealEvent with
  kind := GovernanceRightExerciseEventKind.exportPortableState
  actorId := 19
  expectedVersion := 5
  targetVersion := 6
  requestedAuthorityCeiling := 3
  portabilityCheckRecorded := true
}

def reviewGovernanceForkSafetyEvent : GovernanceRightExerciseEvent := {
  exportGovernancePortableStateEvent with
  kind := GovernanceRightExerciseEventKind.recordForkSafetyReview
  actorId := 43
  forkReviewerId := 43
  expectedVersion := 6
  targetVersion := 7
  forkSafetyReviewRecorded := true
}

def bindGovernanceForkObligationsEvent : GovernanceRightExerciseEvent := {
  reviewGovernanceForkSafetyEvent with
  kind := GovernanceRightExerciseEventKind.bindForkObligations
  actorId := 19
  expectedVersion := 7
  targetVersion := 8
  requestedAuthorityCeiling := 2
  forkObligationsPreserved := true
}

def verifyGovernanceReplacementReceiptsEvent : GovernanceRightExerciseEvent := {
  bindGovernanceForkObligationsEvent with
  kind := GovernanceRightExerciseEventKind.verifyReplacementReceipts
  actorId := 37
  expectedVersion := 8
  targetVersion := 9
  requestedAuthorityCeiling := 1
  replacementReceiptsRecorded := true
}

def closeGovernanceRightExerciseEvent : GovernanceRightExerciseEvent := {
  verifyGovernanceReplacementReceiptsEvent with
  kind := GovernanceRightExerciseEventKind.close
  actorId := 17
  expectedVersion := 9
  targetVersion := 10
  requestedAuthorityCeiling := 0
}

def completeGovernanceRightExerciseTrace : List GovernanceRightExerciseEvent :=
  [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
    appealGovernanceRedactionEvent, sustainGovernanceRedactionAppealEvent,
    exportGovernancePortableStateEvent, reviewGovernanceForkSafetyEvent,
    bindGovernanceForkObligationsEvent,
    verifyGovernanceReplacementReceiptsEvent,
    closeGovernanceRightExerciseEvent]

theorem complete_governance_right_exercise_reaches_exact_closure :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      completeGovernanceRightExerciseTrace =
      some {
        initialGovernanceRightExerciseState with
        reviewerId := 37
        appealReviewerId := 41
        forkReviewerId := 43
        version := 10
        currentAuthorityCeiling := 0
        stage := GovernanceRightExerciseStage.closed
        appealOpen := false
        receiptCount := 9
        appealCount := 1
        remedyCount := 1
        adverseRecordCount := 1
        forkObligationCount := 1
        replacementReceiptCount := 1
      } := by
  decide

theorem governance_right_self_review_is_rejected :
    ApplyGovernanceRightExerciseEvent initialGovernanceRightExerciseState
      { reviewGovernanceRightEvent with
        actorId := 19
        reviewerId := 19 } = none := by
  decide

theorem incomplete_governance_right_bundle_is_rejected :
    ApplyGovernanceRightExerciseEvent
      { initialGovernanceRightExerciseState with
        rights := { completeGovernanceRightBundle with appeal := false } }
      { reviewGovernanceRightEvent with
        rights := { completeGovernanceRightBundle with appeal := false } } = none := by
  decide

theorem governance_audit_without_material_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent,
        { deliverGovernanceAuditEvent with auditMaterialRecorded := false }] = none := by
  decide

theorem governance_redaction_without_reason_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent,
        { deliverGovernanceAuditEvent with redactionReasonRecorded := false }] = none := by
  decide

theorem governance_redaction_without_appeal_path_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent,
        { deliverGovernanceAuditEvent with appealPathRecorded := false }] = none := by
  decide

theorem governance_outsider_appeal_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        { appealGovernanceRedactionEvent with actorId := 47 }] = none := by
  decide

theorem governance_captured_appeal_review_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        { appealGovernanceRedactionEvent with appealReviewerId := 19 }] = none := by
  decide

theorem governance_unsustained_appeal_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        appealGovernanceRedactionEvent,
        { sustainGovernanceRedactionAppealEvent with appealSustained := false }] = none := by
  decide

theorem governance_export_before_redress_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        appealGovernanceRedactionEvent, exportGovernancePortableStateEvent] = none := by
  decide

theorem governance_export_without_portability_check_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        appealGovernanceRedactionEvent, sustainGovernanceRedactionAppealEvent,
        { exportGovernancePortableStateEvent with
          portabilityCheckRecorded := false }] = none := by
  decide

theorem governance_captured_fork_review_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        appealGovernanceRedactionEvent, sustainGovernanceRedactionAppealEvent,
        exportGovernancePortableStateEvent,
        { reviewGovernanceForkSafetyEvent with
          actorId := 19
          forkReviewerId := 19 }] = none := by
  decide

theorem governance_fork_without_safety_review_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        appealGovernanceRedactionEvent, sustainGovernanceRedactionAppealEvent,
        exportGovernancePortableStateEvent,
        { reviewGovernanceForkSafetyEvent with
          forkSafetyReviewRecorded := false }] = none := by
  decide

theorem governance_right_bundle_substitution_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent,
        { deliverGovernanceAuditEvent with
          rights := { completeGovernanceRightBundle with dissent := false } }] = none := by
  decide

theorem governance_fork_without_obligation_binding_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        appealGovernanceRedactionEvent, sustainGovernanceRedactionAppealEvent,
        exportGovernancePortableStateEvent, reviewGovernanceForkSafetyEvent,
        { bindGovernanceForkObligationsEvent with
          forkObligationsPreserved := false }] = none := by
  decide

theorem governance_replacement_without_receipts_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        appealGovernanceRedactionEvent, sustainGovernanceRedactionAppealEvent,
        exportGovernancePortableStateEvent, reviewGovernanceForkSafetyEvent,
        bindGovernanceForkObligationsEvent,
        { verifyGovernanceReplacementReceiptsEvent with
          replacementReceiptsRecorded := false }] = none := by
  decide

theorem governance_close_before_replacement_verification_is_rejected :
    RunGovernanceRightExerciseEvents initialGovernanceRightExerciseState
      [reviewGovernanceRightEvent, deliverGovernanceAuditEvent,
        appealGovernanceRedactionEvent, sustainGovernanceRedactionAppealEvent,
        exportGovernancePortableStateEvent, reviewGovernanceForkSafetyEvent,
        bindGovernanceForkObligationsEvent,
        closeGovernanceRightExerciseEvent] = none := by
  decide

theorem governance_authority_widening_is_rejected :
    ApplyGovernanceRightExerciseEvent initialGovernanceRightExerciseState
      { reviewGovernanceRightEvent with requestedAuthorityCeiling := 6 } = none := by
  decide

theorem governance_legal_validation_request_is_rejected :
    ApplyGovernanceRightExerciseEvent initialGovernanceRightExerciseState
      { reviewGovernanceRightEvent with requestsLegalValidation := true } = none := by
  decide

theorem governance_action_authority_request_is_rejected :
    ApplyGovernanceRightExerciseEvent initialGovernanceRightExerciseState
      { reviewGovernanceRightEvent with requestsActionAuthority := true } = none := by
  decide

theorem governance_support_promotion_request_is_rejected :
    ApplyGovernanceRightExerciseEvent initialGovernanceRightExerciseState
      { reviewGovernanceRightEvent with requestsSupportPromotion := true } = none := by
  decide

theorem governance_closed_exercise_is_terminal
    (event : GovernanceRightExerciseEvent) :
    ApplyGovernanceRightExerciseEvent
      { initialGovernanceRightExerciseState with
        stage := GovernanceRightExerciseStage.closed } event = none := by
  unfold ApplyGovernanceRightExerciseEvent
  split
  · rename_i admissible
    unfold GovernanceRightExerciseEventAdmissible at admissible
    rcases admissible with
      ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, route⟩
    cases kind : event.kind <;> rw [kind] at route <;> simp at route
  · rfl

end AsiStackProofs.GovernanceRights
