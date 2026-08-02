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

/-! ## Reachable information-use lifecycle

The route above classifies one authored transaction. This state machine adds a
bounded lifecycle from purpose binding through minimization, mapping, privacy
evaluation, rights disposition, use, revocation, and deletion recording. Event
fields remain inputs: the model does not establish lawful basis, consent,
privacy, evaluator competence, copy discovery, deletion in fact, or total
erasure.
-/

inductive InformationStage where
  | collected
  | purposeBound
  | minimized
  | flowsMapped
  | privacyEvaluated
  | rightsDispositioned
  | active
  | revoked
  | deletionRecorded
deriving DecidableEq, Repr

inductive InformationEventKind where
  | bindPurpose
  | recordMinimization
  | mapFlows
  | evaluatePrivacy
  | dispositionRights
  | activateUse
  | revokePurpose
  | recordDeletion
deriving DecidableEq, Repr

structure InformationState where
  stage : InformationStage
  subjectId : Nat
  datasetId : Nat
  purposeLeaseId : Nat
  jurisdictionId : Nat
  authorityCeiling : Nat
  activeAuthority : Nat
  knownCopyCount : Nat
  disposedCopyCount : Nat
  receiptCount : Nat
  supportAssignmentCount : Nat
  externalEffectAuthorityCount : Nat
deriving DecidableEq, Repr

structure InformationEvent where
  kind : InformationEventKind
  subjectId : Nat
  datasetId : Nat
  purposeLeaseId : Nat
  jurisdictionId : Nat
  requestedAuthority : Nat
  purposeMatches : Bool
  claimedAuthorityRecorded : Bool
  leaseActive : Bool
  lessDataAlternativeTested : Bool
  requiredFlowSurfaceCount : Nat
  mappedFlowSurfaceCount : Nat
  unknownCopiesRecorded : Bool
  derivativeObligationsPropagated : Bool
  independentEvaluator : Bool
  attackPositiveControlsPass : Bool
  attackDenominatorComplete : Bool
  rightsIdentityVerified : Bool
  exceptionsReviewed : Bool
  recipientNotificationsComplete : Bool
  derivativeDispositionsComplete : Bool
  outcomesSeparated : Bool
  residualOwnerPresent : Bool
  disposedCopyCount : Nat
  legalComplianceClaimed : Bool
  totalErasureClaimed : Bool
  supportAssignmentRequested : Bool
  externalEffectAuthorityRequested : Bool
deriving DecidableEq, Repr

structure InformationIdentity where
  subjectId : Nat
  datasetId : Nat
  purposeLeaseId : Nat
  jurisdictionId : Nat
  authorityCeiling : Nat
  knownCopyCount : Nat
deriving DecidableEq, Repr

def informationIdentity (state : InformationState) : InformationIdentity := {
  subjectId := state.subjectId
  datasetId := state.datasetId
  purposeLeaseId := state.purposeLeaseId
  jurisdictionId := state.jurisdictionId
  authorityCeiling := state.authorityCeiling
  knownCopyCount := state.knownCopyCount
}

def InformationEventValid
    (state : InformationState) (event : InformationEvent) : Prop :=
  event.subjectId = state.subjectId ∧
    event.datasetId = state.datasetId ∧
    event.purposeLeaseId = state.purposeLeaseId ∧
    event.jurisdictionId = state.jurisdictionId ∧
    event.requestedAuthority ≤ state.authorityCeiling ∧
    event.legalComplianceClaimed = false ∧
    event.totalErasureClaimed = false ∧
    event.supportAssignmentRequested = false ∧
    event.externalEffectAuthorityRequested = false ∧
    event.residualOwnerPresent = true ∧
    match state.stage, event.kind with
    | .collected, .bindPurpose =>
        event.purposeMatches = true ∧
          event.claimedAuthorityRecorded = true ∧
          event.leaseActive = true
    | .purposeBound, .recordMinimization =>
        event.lessDataAlternativeTested = true
    | .minimized, .mapFlows =>
        event.mappedFlowSurfaceCount = event.requiredFlowSurfaceCount ∧
          event.unknownCopiesRecorded = true ∧
          event.derivativeObligationsPropagated = true
    | .flowsMapped, .evaluatePrivacy =>
        event.independentEvaluator = true ∧
          event.attackPositiveControlsPass = true ∧
          event.attackDenominatorComplete = true
    | .privacyEvaluated, .dispositionRights =>
        event.rightsIdentityVerified = true ∧
          event.exceptionsReviewed = true ∧
          event.recipientNotificationsComplete = true ∧
          event.derivativeDispositionsComplete = true
    | .rightsDispositioned, .activateUse =>
        event.outcomesSeparated = true
    | .active, .revokePurpose => True
    | .revoked, .recordDeletion =>
        event.outcomesSeparated = true ∧
          event.disposedCopyCount = state.knownCopyCount
    | _, _ => False

instance informationEventValidDecidable
    (state : InformationState) (event : InformationEvent) :
    Decidable (InformationEventValid state event) := by
  cases hstage : state.stage <;> cases hkind : event.kind <;>
    simp [InformationEventValid, hstage, hkind] <;> infer_instance

def applyInformationEvent
    (state : InformationState) (event : InformationEvent) : InformationState :=
  let nextReceipt := state.receiptCount + 1
  match event.kind with
  | .bindPurpose =>
      { state with stage := .purposeBound
                   receiptCount := nextReceipt }
  | .recordMinimization =>
      { state with stage := .minimized
                   receiptCount := nextReceipt }
  | .mapFlows =>
      { state with stage := .flowsMapped
                   receiptCount := nextReceipt }
  | .evaluatePrivacy =>
      { state with stage := .privacyEvaluated
                   receiptCount := nextReceipt }
  | .dispositionRights =>
      { state with stage := .rightsDispositioned
                   receiptCount := nextReceipt }
  | .activateUse =>
      { state with stage := .active
                   activeAuthority := event.requestedAuthority
                   receiptCount := nextReceipt }
  | .revokePurpose =>
      { state with stage := .revoked
                   activeAuthority := 0
                   receiptCount := nextReceipt }
  | .recordDeletion =>
      { state with stage := .deletionRecorded
                   disposedCopyCount := event.disposedCopyCount
                   receiptCount := nextReceipt }

def InformationStep
    (state : InformationState) (event : InformationEvent) : Option InformationState :=
  if InformationEventValid state event then
    some (applyInformationEvent state event)
  else none

def InformationRun : InformationState → List InformationEvent → Option InformationState
  | state, [] => some state
  | state, event :: tail =>
      match InformationStep state event with
      | none => none
      | some next => InformationRun next tail

def InformationTraceValid : InformationState → List InformationEvent → Prop
  | _, [] => True
  | state, event :: tail =>
      InformationEventValid state event ∧
        InformationTraceValid (applyInformationEvent state event) tail

theorem accepted_information_step_is_valid
    {state next : InformationState} {event : InformationEvent}
    (stepped : InformationStep state event = some next) :
    InformationEventValid state event := by
  unfold InformationStep at stepped
  split at stepped
  · assumption
  · simp at stepped

theorem accepted_information_step_applies_event
    {state next : InformationState} {event : InformationEvent}
    (stepped : InformationStep state event = some next) :
    next = applyInformationEvent state event := by
  unfold InformationStep at stepped
  split at stepped
  · exact Option.some.inj stepped |>.symm
  · simp at stepped

theorem apply_information_event_preserves_identity
    (state : InformationState) (event : InformationEvent) :
    informationIdentity (applyInformationEvent state event) =
      informationIdentity state := by
  cases h : event.kind <;>
    simp [applyInformationEvent, informationIdentity, h]

theorem accepted_information_step_preserves_non_authority
    {state next : InformationState} {event : InformationEvent}
    (stepped : InformationStep state event = some next) :
    next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectAuthorityCount = state.externalEffectAuthorityCount := by
  have applies := accepted_information_step_applies_event stepped
  subst next
  cases h : event.kind <;> simp [applyInformationEvent, h]

theorem accepted_information_step_adds_one_receipt
    {state next : InformationState} {event : InformationEvent}
    (stepped : InformationStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  have applies := accepted_information_step_applies_event stepped
  subst next
  cases h : event.kind <;> simp [applyInformationEvent, h]

theorem accepted_information_step_respects_authority_ceiling
    {state next : InformationState} {event : InformationEvent}
    (bounded : state.activeAuthority ≤ state.authorityCeiling)
    (stepped : InformationStep state event = some next) :
    next.activeAuthority ≤ next.authorityCeiling := by
  have valid := accepted_information_step_is_valid stepped
  have applies := accepted_information_step_applies_event stepped
  subst next
  rcases valid with ⟨_, _, _, _, requestedBound, _⟩
  cases h : event.kind <;>
    simp [applyInformationEvent, h, bounded, requestedBound]

theorem successful_information_run_preserves_identity
    {state final : InformationState} {events : List InformationEvent}
    (ran : InformationRun state events = some final) :
    informationIdentity final = informationIdentity state := by
  induction events generalizing state with
  | nil =>
      simp [InformationRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : InformationStep state event with
      | none => simp [InformationRun, stepped] at ran
      | some next =>
          have tailRan : InformationRun next tail = some final := by
            simpa [InformationRun, stepped] using ran
          calc
            informationIdentity final = informationIdentity next := ih tailRan
            _ = informationIdentity state := by
              have applies := accepted_information_step_applies_event stepped
              subst next
              exact apply_information_event_preserves_identity state event

theorem successful_information_run_preserves_non_authority
    {state final : InformationState} {events : List InformationEvent}
    (ran : InformationRun state events = some final) :
    final.supportAssignmentCount = state.supportAssignmentCount ∧
      final.externalEffectAuthorityCount = state.externalEffectAuthorityCount := by
  induction events generalizing state with
  | nil =>
      simp [InformationRun] at ran
      subst final
      exact ⟨rfl, rfl⟩
  | cons event tail ih =>
      cases stepped : InformationStep state event with
      | none => simp [InformationRun, stepped] at ran
      | some next =>
          have tailRan : InformationRun next tail = some final := by
            simpa [InformationRun, stepped] using ran
          have tailPreserved := ih tailRan
          have stepPreserved := accepted_information_step_preserves_non_authority stepped
          exact ⟨tailPreserved.1.trans stepPreserved.1,
            tailPreserved.2.trans stepPreserved.2⟩

theorem successful_information_run_respects_authority_ceiling
    {state final : InformationState} {events : List InformationEvent}
    (bounded : state.activeAuthority ≤ state.authorityCeiling)
    (ran : InformationRun state events = some final) :
    final.activeAuthority ≤ final.authorityCeiling := by
  induction events generalizing state with
  | nil =>
      simp [InformationRun] at ran
      subst final
      exact bounded
  | cons event tail ih =>
      cases stepped : InformationStep state event with
      | none => simp [InformationRun, stepped] at ran
      | some next =>
          have tailRan : InformationRun next tail = some final := by
            simpa [InformationRun, stepped] using ran
          exact ih
            (accepted_information_step_respects_authority_ceiling bounded stepped)
            tailRan

theorem successful_information_run_has_valid_trace
    {state final : InformationState} {events : List InformationEvent}
    (ran : InformationRun state events = some final) :
    InformationTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : InformationStep state event with
      | none => simp [InformationRun, stepped] at ran
      | some next =>
          have tailRan : InformationRun next tail = some final := by
            simpa [InformationRun, stepped] using ran
          have applies := accepted_information_step_applies_event stepped
          exact ⟨accepted_information_step_is_valid stepped, by
            simpa [applies] using ih tailRan⟩

theorem information_run_composes
    {state middle final : InformationState}
    {front back : List InformationEvent}
    (first : InformationRun state front = some middle)
    (second : InformationRun middle back = some final) :
    InformationRun state (front ++ back) = some final := by
  induction front generalizing state middle with
  | nil =>
      simp [InformationRun] at first
      subst middle
      exact second
  | cons event tail ih =>
      cases stepped : InformationStep state event with
      | none => simp [InformationRun, stepped] at first
      | some next =>
          have tailFirst : InformationRun next tail = some middle := by
            simpa [InformationRun, stepped] using first
          simpa [InformationRun, stepped] using ih tailFirst second

theorem active_information_use_cannot_record_deletion
    {state : InformationState} {event : InformationEvent}
    (active : state.stage = .active)
    (deletion : event.kind = .recordDeletion) :
    InformationStep state event = none := by
  simp [InformationStep, InformationEventValid, active, deletion]

theorem accepted_activation_requires_rights_disposition
    {state next : InformationState} {event : InformationEvent}
    (activation : event.kind = .activateUse)
    (stepped : InformationStep state event = some next) :
    state.stage = .rightsDispositioned := by
  have valid := accepted_information_step_is_valid stepped
  cases h : state.stage <;>
    simp [InformationEventValid, h, activation] at valid ⊢

theorem accepted_revocation_zeros_information_authority
    {state next : InformationState} {event : InformationEvent}
    (revocation : event.kind = .revokePurpose)
    (stepped : InformationStep state event = some next) :
    next.stage = .revoked ∧ next.activeAuthority = 0 := by
  have applies := accepted_information_step_applies_event stepped
  subst next
  simp [applyInformationEvent, revocation]

theorem accepted_deletion_records_only_known_copy_disposition
    {state next : InformationState} {event : InformationEvent}
    (deletion : event.kind = .recordDeletion)
    (stepped : InformationStep state event = some next) :
    state.stage = .revoked ∧
      next.stage = .deletionRecorded ∧
      next.disposedCopyCount = state.knownCopyCount := by
  have valid := accepted_information_step_is_valid stepped
  have applies := accepted_information_step_applies_event stepped
  have stage : state.stage = .revoked := by
    cases h : state.stage <;>
      simp [InformationEventValid, h, deletion] at valid ⊢
  rcases valid with ⟨_, _, _, _, _, _, _, _, _, _, stageValid⟩
  have deletionValid :
      event.outcomesSeparated = true ∧
        event.disposedCopyCount = state.knownCopyCount := by
    simpa [stage, deletion] using stageValid
  have disposed := deletionValid.2
  subst next
  refine ⟨stage, ?_⟩
  simp [applyInformationEvent, deletion, disposed]

def informationInitialState : InformationState := {
  stage := .collected
  subjectId := 10
  datasetId := 20
  purposeLeaseId := 30
  jurisdictionId := 40
  authorityCeiling := 3
  activeAuthority := 0
  knownCopyCount := 4
  disposedCopyCount := 0
  receiptCount := 0
  supportAssignmentCount := 0
  externalEffectAuthorityCount := 0
}

def informationEvent (kind : InformationEventKind) : InformationEvent := {
  kind := kind
  subjectId := 10
  datasetId := 20
  purposeLeaseId := 30
  jurisdictionId := 40
  requestedAuthority := 2
  purposeMatches := true
  claimedAuthorityRecorded := true
  leaseActive := true
  lessDataAlternativeTested := true
  requiredFlowSurfaceCount := 12
  mappedFlowSurfaceCount := 12
  unknownCopiesRecorded := true
  derivativeObligationsPropagated := true
  independentEvaluator := true
  attackPositiveControlsPass := true
  attackDenominatorComplete := true
  rightsIdentityVerified := true
  exceptionsReviewed := true
  recipientNotificationsComplete := true
  derivativeDispositionsComplete := true
  outcomesSeparated := true
  residualOwnerPresent := true
  disposedCopyCount := 4
  legalComplianceClaimed := false
  totalErasureClaimed := false
  supportAssignmentRequested := false
  externalEffectAuthorityRequested := false
}

def completeInformationEvents : List InformationEvent :=
  [.bindPurpose, .recordMinimization, .mapFlows, .evaluatePrivacy,
    .dispositionRights, .activateUse, .revokePurpose, .recordDeletion].map
      informationEvent

def completeInformationFinalState : InformationState :=
  { informationInitialState with
    stage := .deletionRecorded
    activeAuthority := 0
    disposedCopyCount := 4
    receiptCount := 8 }

theorem complete_information_run_reaches_bounded_deletion_record :
    ∃ final,
      InformationRun informationInitialState completeInformationEvents = some final ∧
      final.stage = .deletionRecorded ∧
      final.activeAuthority = 0 ∧
      final.disposedCopyCount = final.knownCopyCount ∧
      final.receiptCount = 8 := by
  refine ⟨completeInformationFinalState, ?_⟩
  native_decide

end AsiStackProofs.PrivacyInformationFlow
