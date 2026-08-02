namespace AsiStackProofs.Corrigibility

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

/-! ## Versioned correction-control lifecycle

This model records notice, independent review, bounded control, affected-party
challenge, and accountable correction around separately authorized action. Its
authority ceiling can only narrow. The fields are trusted finite inputs, and a
recorded correction is not evidence that a deployed effect was reversed or
that affected parties gave informed consent.
-/

inductive AgencyCorrectionStage where
  | proposed
  | notified
  | reviewed
  | active
  | challenged
  | corrected
deriving DecidableEq, Repr

inductive AgencyCorrectionEventKind where
  | recordMaterialNotice
  | recordIndependentReview
  | recordBoundedControl
  | openChallenge
  | recordCorrection
deriving DecidableEq, Repr

structure AgencyCorrectionState where
  controlId : Nat
  actionId : Nat
  affectedPartySetId : Nat
  affectedPartyRepresentativeId : Nat
  principalId : Nat
  reviewerId : Nat
  version : Nat
  baseAuthorityCeiling : Nat
  currentAuthorityCeiling : Nat
  stage : AgencyCorrectionStage
  noticeRecorded : Bool
  approvalRecorded : Bool
  delegationBounded : Bool
  appealAvailable : Bool
  interruptAvailable : Bool
  rollbackAvailable : Bool
  correctionReceiptCount : Nat
  accountabilityReceiptCount : Nat
  residualCount : Nat
  expiresAt : Nat
  now : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

structure AgencyCorrectionEvent where
  kind : AgencyCorrectionEventKind
  controlId : Nat
  actionId : Nat
  affectedPartySetId : Nat
  affectedPartyRepresentativeId : Nat
  actorId : Nat
  reviewerId : Nat
  expectedVersion : Nat
  targetVersion : Nat
  requestedAuthorityCeiling : Nat
  materialNoticePresent : Bool
  approvalPresent : Bool
  boundedDelegationPresent : Bool
  appealPathPresent : Bool
  interruptPathPresent : Bool
  rollbackPathPresent : Bool
  challengePresent : Bool
  correctionReceiptPresent : Bool
  accountabilityReceiptPresent : Bool
  residualPresent : Bool
  observedNow : Nat
  requestedExpiry : Nat
  requestsActionAuthority : Bool
  claimsAffectedPartyConsent : Bool
deriving DecidableEq, Repr

def AgencyCorrectionEventAdmissible
    (state : AgencyCorrectionState) (event : AgencyCorrectionEvent) : Prop :=
  event.controlId = state.controlId ∧
    event.actionId = state.actionId ∧
    event.affectedPartySetId = state.affectedPartySetId ∧
    event.affectedPartyRepresentativeId = state.affectedPartyRepresentativeId ∧
    event.expectedVersion = state.version ∧
    state.now ≤ event.observedNow ∧
    event.requestsActionAuthority = false ∧
    event.claimsAffectedPartyConsent = false ∧
    match event.kind with
    | AgencyCorrectionEventKind.recordMaterialNotice =>
        state.stage = AgencyCorrectionStage.proposed ∧
          event.actorId = state.principalId ∧
          event.materialNoticePresent = true ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AgencyCorrectionEventKind.recordIndependentReview =>
        state.stage = AgencyCorrectionStage.notified ∧
          event.actorId = event.reviewerId ∧
          event.reviewerId ≠ state.principalId ∧
          event.appealPathPresent = true ∧
          event.interruptPathPresent = true ∧
          event.rollbackPathPresent = true ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AgencyCorrectionEventKind.recordBoundedControl =>
        state.stage = AgencyCorrectionStage.reviewed ∧
          state.reviewerId ≠ state.principalId ∧
          event.reviewerId = state.reviewerId ∧
          event.actorId = state.principalId ∧
          event.approvalPresent = true ∧
          event.boundedDelegationPresent = true ∧
          event.appealPathPresent = true ∧
          event.interruptPathPresent = true ∧
          event.rollbackPathPresent = true ∧
          event.requestedAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
          event.observedNow < event.requestedExpiry ∧
          event.targetVersion = state.version + 1
    | AgencyCorrectionEventKind.openChallenge =>
        state.stage = AgencyCorrectionStage.active ∧
          event.actorId = state.affectedPartyRepresentativeId ∧
          event.challengePresent = true ∧
          event.observedNow < state.expiresAt ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AgencyCorrectionEventKind.recordCorrection =>
        state.stage = AgencyCorrectionStage.challenged ∧
          event.actorId = state.principalId ∧
          event.correctionReceiptPresent = true ∧
          event.accountabilityReceiptPresent = true ∧
          event.residualPresent = true ∧
          event.requestedAuthorityCeiling = 0 ∧
          event.targetVersion = state.version

instance agencyCorrectionEventAdmissibleDecidable
    (state : AgencyCorrectionState) (event : AgencyCorrectionEvent) :
    Decidable (AgencyCorrectionEventAdmissible state event) := by
  unfold AgencyCorrectionEventAdmissible
  cases event.kind <;> infer_instance

def AdvanceAgencyCorrection
    (state : AgencyCorrectionState)
    (event : AgencyCorrectionEvent) : AgencyCorrectionState :=
  match event.kind with
  | AgencyCorrectionEventKind.recordMaterialNotice =>
      { state with
        stage := AgencyCorrectionStage.notified
        noticeRecorded := true
        now := event.observedNow }
  | AgencyCorrectionEventKind.recordIndependentReview =>
      { state with
        stage := AgencyCorrectionStage.reviewed
        reviewerId := event.reviewerId
        appealAvailable := event.appealPathPresent
        interruptAvailable := event.interruptPathPresent
        rollbackAvailable := event.rollbackPathPresent
        now := event.observedNow }
  | AgencyCorrectionEventKind.recordBoundedControl =>
      { state with
        stage := AgencyCorrectionStage.active
        version := event.targetVersion
        currentAuthorityCeiling := event.requestedAuthorityCeiling
        approvalRecorded := true
        delegationBounded := true
        appealAvailable := event.appealPathPresent
        interruptAvailable := event.interruptPathPresent
        rollbackAvailable := event.rollbackPathPresent
        expiresAt := event.requestedExpiry
        now := event.observedNow }
  | AgencyCorrectionEventKind.openChallenge =>
      { state with
        stage := AgencyCorrectionStage.challenged
        residualCount := state.residualCount + 1
        now := event.observedNow }
  | AgencyCorrectionEventKind.recordCorrection =>
      { state with
        stage := AgencyCorrectionStage.corrected
        currentAuthorityCeiling := 0
        correctionReceiptCount := state.correctionReceiptCount + 1
        accountabilityReceiptCount := state.accountabilityReceiptCount + 1
        residualCount := state.residualCount + 1
        now := event.observedNow }

def ApplyAgencyCorrectionEvent
    (state : AgencyCorrectionState)
    (event : AgencyCorrectionEvent) : Option AgencyCorrectionState :=
  if AgencyCorrectionEventAdmissible state event then
    some (AdvanceAgencyCorrection state event)
  else
    none

def RunAgencyCorrectionEvents :
    AgencyCorrectionState → List AgencyCorrectionEvent → Option AgencyCorrectionState
  | state, [] => some state
  | state, event :: tail =>
      match ApplyAgencyCorrectionEvent state event with
      | none => none
      | some next => RunAgencyCorrectionEvents next tail

theorem accepted_agency_correction_event_is_admissible
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    AgencyCorrectionEventAdmissible state event := by
  unfold ApplyAgencyCorrectionEvent at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_agency_correction_event_is_exact_advance
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    next = AdvanceAgencyCorrection state event := by
  unfold ApplyAgencyCorrectionEvent at accepted
  split at accepted
  · simp at accepted
    exact accepted.symm
  · simp at accepted

theorem accepted_agency_correction_event_preserves_custody
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    next.controlId = state.controlId ∧
      next.actionId = state.actionId ∧
      next.affectedPartySetId = state.affectedPartySetId ∧
      next.affectedPartyRepresentativeId = state.affectedPartyRepresentativeId ∧
      next.principalId = state.principalId ∧
      next.baseAuthorityCeiling = state.baseAuthorityCeiling := by
  have exactAdvance := accepted_agency_correction_event_is_exact_advance accepted
  subst next
  cases kind : event.kind <;> simp [AdvanceAgencyCorrection, kind]

theorem accepted_agency_correction_event_is_non_authorizing
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    event.requestsActionAuthority = false ∧
      event.claimsAffectedPartyConsent = false ∧
      next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectCount = state.externalEffectCount := by
  have admissible := accepted_agency_correction_event_is_admissible accepted
  have exactAdvance := accepted_agency_correction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, noAuthority, noConsent, _⟩
  subst next
  exact ⟨noAuthority, noConsent,
    by cases kind : event.kind <;> simp [AdvanceAgencyCorrection, kind],
    by cases kind : event.kind <;> simp [AdvanceAgencyCorrection, kind]⟩

theorem accepted_agency_correction_event_never_widens_authority
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling := by
  have admissible := accepted_agency_correction_event_is_admissible accepted
  have exactAdvance := accepted_agency_correction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  subst next
  cases kind : event.kind with
  | recordMaterialNotice => simp [AdvanceAgencyCorrection, kind]
  | recordIndependentReview => simp [AdvanceAgencyCorrection, kind]
  | recordBoundedControl =>
      simp [kind] at route
      simpa [AdvanceAgencyCorrection, kind] using route.2.2.2.2.2.2.2.2.2.1
  | openChallenge => simp [AdvanceAgencyCorrection, kind]
  | recordCorrection => simp [AdvanceAgencyCorrection, kind]

theorem accepted_material_notice_is_recorded
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (kind : event.kind = AgencyCorrectionEventKind.recordMaterialNotice)
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    state.stage = AgencyCorrectionStage.proposed ∧
      event.actorId = state.principalId ∧
      event.materialNoticePresent = true ∧
      next.stage = AgencyCorrectionStage.notified ∧
      next.noticeRecorded = true := by
  have admissible := accepted_agency_correction_event_is_admissible accepted
  have exactAdvance := accepted_agency_correction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨proposed, principal, notice, _, _⟩
  subst next
  simp [AdvanceAgencyCorrection, kind, proposed, principal, notice]

theorem accepted_independent_review_records_correction_paths
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (kind : event.kind = AgencyCorrectionEventKind.recordIndependentReview)
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    state.stage = AgencyCorrectionStage.notified ∧
      event.reviewerId ≠ state.principalId ∧
      next.reviewerId = event.reviewerId ∧
      next.appealAvailable = true ∧
      next.interruptAvailable = true ∧
      next.rollbackAvailable = true := by
  have admissible := accepted_agency_correction_event_is_admissible accepted
  have exactAdvance := accepted_agency_correction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨notified, _, independent, appeal, interrupt, rollback, _, _⟩
  subst next
  simp [AdvanceAgencyCorrection, kind, notified, independent, appeal, interrupt,
    rollback]

theorem accepted_bounded_control_requires_review_approval_paths_and_expiry
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (kind : event.kind = AgencyCorrectionEventKind.recordBoundedControl)
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    state.stage = AgencyCorrectionStage.reviewed ∧
      state.reviewerId ≠ state.principalId ∧
      event.approvalPresent = true ∧
      event.boundedDelegationPresent = true ∧
      next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
      next.approvalRecorded = true ∧
      next.delegationBounded = true ∧
      next.appealAvailable = true ∧
      next.interruptAvailable = true ∧
      next.rollbackAvailable = true ∧
      next.now < next.expiresAt := by
  have admissible := accepted_agency_correction_event_is_admissible accepted
  have exactAdvance := accepted_agency_correction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨reviewed, independent, _, _, approval, bounded, appeal,
    interrupt, rollback, narrowed, future, _⟩
  subst next
  simp [AdvanceAgencyCorrection, kind, reviewed, independent, approval, bounded,
    appeal, interrupt, rollback, narrowed, future]

theorem accepted_challenge_requires_affected_party_and_preexpiry
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (kind : event.kind = AgencyCorrectionEventKind.openChallenge)
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    state.stage = AgencyCorrectionStage.active ∧
      event.actorId = state.affectedPartyRepresentativeId ∧
      event.observedNow < state.expiresAt ∧
      next.stage = AgencyCorrectionStage.challenged ∧
      next.residualCount = state.residualCount + 1 := by
  have admissible := accepted_agency_correction_event_is_admissible accepted
  have exactAdvance := accepted_agency_correction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨active, representative, _, future, _, _⟩
  subst next
  simp [AdvanceAgencyCorrection, kind, active, representative, future]

theorem accepted_correction_records_accountability_residual_and_zero_ceiling
    {state next : AgencyCorrectionState} {event : AgencyCorrectionEvent}
    (kind : event.kind = AgencyCorrectionEventKind.recordCorrection)
    (accepted : ApplyAgencyCorrectionEvent state event = some next) :
    state.stage = AgencyCorrectionStage.challenged ∧
      event.correctionReceiptPresent = true ∧
      event.accountabilityReceiptPresent = true ∧
      event.residualPresent = true ∧
      next.stage = AgencyCorrectionStage.corrected ∧
      next.currentAuthorityCeiling = 0 ∧
      next.correctionReceiptCount = state.correctionReceiptCount + 1 ∧
      next.accountabilityReceiptCount = state.accountabilityReceiptCount + 1 ∧
      next.residualCount = state.residualCount + 1 := by
  have admissible := accepted_agency_correction_event_is_admissible accepted
  have exactAdvance := accepted_agency_correction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨challenged, _, receipt, accountability, residual, zero, _⟩
  subst next
  simp [AdvanceAgencyCorrection, kind, challenged, receipt, accountability,
    residual]

theorem agency_correction_run_preserves_custody_non_authority_and_narrowing
    {initial final : AgencyCorrectionState}
    {events : List AgencyCorrectionEvent}
    (run : RunAgencyCorrectionEvents initial events = some final) :
    final.controlId = initial.controlId ∧
      final.actionId = initial.actionId ∧
      final.affectedPartySetId = initial.affectedPartySetId ∧
      final.affectedPartyRepresentativeId = initial.affectedPartyRepresentativeId ∧
      final.principalId = initial.principalId ∧
      final.baseAuthorityCeiling = initial.baseAuthorityCeiling ∧
      final.currentAuthorityCeiling ≤ initial.currentAuthorityCeiling ∧
      final.supportAssignmentCount = initial.supportAssignmentCount ∧
      final.externalEffectCount = initial.externalEffectCount := by
  induction events generalizing initial with
  | nil => simp [RunAgencyCorrectionEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunAgencyCorrectionEvents] at run
      cases step : ApplyAgencyCorrectionEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          have custody := accepted_agency_correction_event_preserves_custody step
          have boundary := accepted_agency_correction_event_is_non_authorizing step
          have narrowed := accepted_agency_correction_event_never_widens_authority step
          have tailFacts := ih run
          rcases custody with ⟨control, action, parties, representative, principal, base⟩
          rcases boundary with ⟨_, _, support, effects⟩
          rcases tailFacts with ⟨tcontrol, taction, tparties, trepresentative,
            tprincipal, tbase, tnarrowed, tsupport, teffects⟩
          exact ⟨tcontrol.trans control, taction.trans action,
            tparties.trans parties, trepresentative.trans representative,
            tprincipal.trans principal, tbase.trans base,
            Nat.le_trans tnarrowed narrowed, tsupport.trans support,
            teffects.trans effects⟩

theorem agency_correction_runs_compose
    (initial : AgencyCorrectionState)
    (before after : List AgencyCorrectionEvent) :
    RunAgencyCorrectionEvents initial (before ++ after) =
      match RunAgencyCorrectionEvents initial before with
      | none => none
      | some middle => RunAgencyCorrectionEvents middle after := by
  induction before generalizing initial with
  | nil => simp [RunAgencyCorrectionEvents]
  | cons event tail ih =>
      simp only [List.cons_append, RunAgencyCorrectionEvents]
      cases step : ApplyAgencyCorrectionEvent initial event with
      | none => simp
      | some next => simp [ih]

def initialAgencyCorrectionState : AgencyCorrectionState := {
  controlId := 53
  actionId := 59
  affectedPartySetId := 61
  affectedPartyRepresentativeId := 67
  principalId := 71
  reviewerId := 0
  version := 1
  baseAuthorityCeiling := 5
  currentAuthorityCeiling := 5
  stage := AgencyCorrectionStage.proposed
  noticeRecorded := false
  approvalRecorded := false
  delegationBounded := false
  appealAvailable := false
  interruptAvailable := false
  rollbackAvailable := false
  correctionReceiptCount := 0
  accountabilityReceiptCount := 0
  residualCount := 0
  expiresAt := 0
  now := 10
  supportAssignmentCount := 0
  externalEffectCount := 0
}

def materialNoticeEvent : AgencyCorrectionEvent := {
  kind := AgencyCorrectionEventKind.recordMaterialNotice
  controlId := 53
  actionId := 59
  affectedPartySetId := 61
  affectedPartyRepresentativeId := 67
  actorId := 71
  reviewerId := 0
  expectedVersion := 1
  targetVersion := 1
  requestedAuthorityCeiling := 5
  materialNoticePresent := true
  approvalPresent := false
  boundedDelegationPresent := false
  appealPathPresent := false
  interruptPathPresent := false
  rollbackPathPresent := false
  challengePresent := false
  correctionReceiptPresent := false
  accountabilityReceiptPresent := false
  residualPresent := false
  observedNow := 11
  requestedExpiry := 20
  requestsActionAuthority := false
  claimsAffectedPartyConsent := false
}

def independentAgencyReviewEvent : AgencyCorrectionEvent := {
  materialNoticeEvent with
  kind := AgencyCorrectionEventKind.recordIndependentReview
  actorId := 73
  reviewerId := 73
  appealPathPresent := true
  interruptPathPresent := true
  rollbackPathPresent := true
  observedNow := 12
}

def boundedAgencyControlEvent : AgencyCorrectionEvent := {
  independentAgencyReviewEvent with
  kind := AgencyCorrectionEventKind.recordBoundedControl
  actorId := 71
  expectedVersion := 1
  targetVersion := 2
  requestedAuthorityCeiling := 3
  approvalPresent := true
  boundedDelegationPresent := true
  observedNow := 13
}

def agencyChallengeEvent : AgencyCorrectionEvent := {
  boundedAgencyControlEvent with
  kind := AgencyCorrectionEventKind.openChallenge
  actorId := 67
  expectedVersion := 2
  targetVersion := 2
  requestedAuthorityCeiling := 3
  challengePresent := true
  observedNow := 14
}

def agencyCorrectionEvent : AgencyCorrectionEvent := {
  agencyChallengeEvent with
  kind := AgencyCorrectionEventKind.recordCorrection
  actorId := 71
  challengePresent := false
  requestedAuthorityCeiling := 0
  correctionReceiptPresent := true
  accountabilityReceiptPresent := true
  residualPresent := true
  observedNow := 15
}

def completeAgencyCorrectionTrace : List AgencyCorrectionEvent :=
  [materialNoticeEvent, independentAgencyReviewEvent, boundedAgencyControlEvent,
    agencyChallengeEvent, agencyCorrectionEvent]

theorem complete_agency_correction_trace_reaches_exact_corrected_state :
    RunAgencyCorrectionEvents initialAgencyCorrectionState completeAgencyCorrectionTrace =
      some {
        initialAgencyCorrectionState with
        reviewerId := 73
        version := 2
        currentAuthorityCeiling := 0
        stage := AgencyCorrectionStage.corrected
        noticeRecorded := true
        approvalRecorded := true
        delegationBounded := true
        appealAvailable := true
        interruptAvailable := true
        rollbackAvailable := true
        correctionReceiptCount := 1
        accountabilityReceiptCount := 1
        residualCount := 2
        expiresAt := 20
        now := 15
      } := by
  decide

theorem agency_correction_missing_notice_is_rejected :
    ApplyAgencyCorrectionEvent initialAgencyCorrectionState
      { materialNoticeEvent with materialNoticePresent := false } = none := by
  decide

theorem agency_correction_self_review_is_rejected :
    RunAgencyCorrectionEvents initialAgencyCorrectionState
      [materialNoticeEvent,
        { independentAgencyReviewEvent with actorId := 71, reviewerId := 71 }] = none := by
  decide

theorem agency_correction_unbounded_delegation_is_rejected :
    RunAgencyCorrectionEvents initialAgencyCorrectionState
      [materialNoticeEvent, independentAgencyReviewEvent,
        { boundedAgencyControlEvent with boundedDelegationPresent := false }] = none := by
  decide

theorem agency_correction_authority_widening_is_rejected :
    RunAgencyCorrectionEvents initialAgencyCorrectionState
      [materialNoticeEvent, independentAgencyReviewEvent,
        { boundedAgencyControlEvent with requestedAuthorityCeiling := 6 }] = none := by
  decide

theorem agency_correction_outsider_challenge_is_rejected :
    RunAgencyCorrectionEvents initialAgencyCorrectionState
      [materialNoticeEvent, independentAgencyReviewEvent, boundedAgencyControlEvent,
        { agencyChallengeEvent with actorId := 68 }] = none := by
  decide

theorem agency_correction_missing_accountability_is_rejected :
    RunAgencyCorrectionEvents initialAgencyCorrectionState
      [materialNoticeEvent, independentAgencyReviewEvent, boundedAgencyControlEvent,
        agencyChallengeEvent,
        { agencyCorrectionEvent with accountabilityReceiptPresent := false }] = none := by
  decide

theorem agency_correction_consent_laundering_is_rejected :
    ApplyAgencyCorrectionEvent initialAgencyCorrectionState
      { materialNoticeEvent with claimsAffectedPartyConsent := true } = none := by
  decide

end AsiStackProofs.Corrigibility
