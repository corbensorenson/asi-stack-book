namespace AsiStackProofs.FailureRecoveryRefinement

inductive Stage where
  | operating
  | detected
  | contained
  | remediated
  | reviewed
deriving DecidableEq, Repr

inductive EventKind where
  | detectAndIsolate
  | confirmContainment
  | recordRemediation
  | recordReview
  | requestReadmission
deriving DecidableEq, Repr

inductive Route where
  | rejectInvalidControlState
  | rejectWrongStage
  | rejectIncidentSubstitution
  | rejectEventReplay
  | rejectAuthorityLeak
  | requestObservation
  | requestFailureClass
  | requestBoundary
  | rejectSelfJudgment
  | requestContainment
  | requestEscapeClosure
  | requestContainmentOwner
  | requestCause
  | requestRemediation
  | requestRegressionEvidence
  | requestIndependentReview
  | rejectReviewerCapture
  | requestResidual
  | requestCurrentAssurance
  | requestCurrentTaxonomy
  | requestResidualDischarge
  | requestReadmissionAuthority
  | acceptDetection
  | acceptContainment
  | acceptRemediation
  | acceptReview
  | acceptReadmission
deriving DecidableEq, Repr

structure State where
  stage : Stage
  incidentId : Nat
  boundaryVersion : Nat
  architectureDigest : Nat
  policyDigest : Nat
  detectorDigest : Nat
  containmentDigest : Nat
  remediationDigest : Nat
  reviewerDigest : Nat
  assuranceDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  incidentCount : Nat
  recoveryCount : Nat
  recurrenceCount : Nat
  openResidualCount : Nat
  containmentActive : Bool
  externalEffectsEnabled : Bool
  promotionEnabled : Bool
  supportAssignmentCount : Nat
  externalAuthorityCount : Nat
deriving DecidableEq, Repr

structure Packet where
  incidentId : Nat
  boundaryVersion : Nat
  architectureDigest : Nat
  policyDigest : Nat
  detectorDigest : Nat
  containmentDigest : Nat
  remediationDigest : Nat
  reviewerDigest : Nat
  assuranceDigest : Nat
  eventDigest : Nat
  failureObserved : Bool
  failureClassRecorded : Bool
  boundaryRecorded : Bool
  detectorIndependent : Bool
  containmentApplied : Bool
  escapePathClosed : Bool
  containmentOwnerAccepted : Bool
  causeRecorded : Bool
  remediationApplied : Bool
  regressionEvidencePassed : Bool
  independentReviewRecorded : Bool
  reviewerIndependent : Bool
  residualRecorded : Bool
  assuranceCurrent : Bool
  taxonomyCurrent : Bool
  residualDischarged : Bool
  readmissionAuthorityPresent : Bool
  recurrenceOfPriorIncident : Bool
  supportAssignmentRequested : Bool
  externalAuthorityRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure IncidentIdentity where
  incidentId : Nat
  boundaryVersion : Nat
  architectureDigest : Nat
  policyDigest : Nat
  detectorDigest : Nat
  containmentDigest : Nat
  remediationDigest : Nat
  reviewerDigest : Nat
  assuranceDigest : Nat
deriving DecidableEq, Repr

def exactIdentity (state : State) : IncidentIdentity :=
  { incidentId := state.incidentId
    boundaryVersion := state.boundaryVersion
    architectureDigest := state.architectureDigest
    policyDigest := state.policyDigest
    detectorDigest := state.detectorDigest
    containmentDigest := state.containmentDigest
    remediationDigest := state.remediationDigest
    reviewerDigest := state.reviewerDigest
    assuranceDigest := state.assuranceDigest }

def expectedKind : Stage -> EventKind
  | .operating => .detectAndIsolate
  | .detected => .confirmContainment
  | .contained => .recordRemediation
  | .remediated => .recordReview
  | .reviewed => .requestReadmission

def openIncidentCount : Stage -> Nat
  | .operating => 0
  | _ => 1

def ControlStateValid (state : State) : Bool :=
  match state.stage with
  | .operating =>
      !state.containmentActive && state.externalEffectsEnabled &&
        state.promotionEnabled && state.openResidualCount == 0
  | _ =>
      state.containmentActive && !state.externalEffectsEnabled &&
        !state.promotionEnabled && state.openResidualCount == 1

def LifecycleAccountingValid (state : State) : Prop :=
  state.recoveryCount + openIncidentCount state.stage = state.incidentCount ∧
    state.recurrenceCount ≤ state.incidentCount

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.incidentId = packet.incidentId &&
    state.boundaryVersion = packet.boundaryVersion &&
    state.architectureDigest = packet.architectureDigest &&
    state.policyDigest = packet.policyDigest &&
    state.detectorDigest = packet.detectorDigest &&
    state.containmentDigest = packet.containmentDigest &&
    state.remediationDigest = packet.remediationDigest &&
    state.reviewerDigest = packet.reviewerDigest &&
    state.assuranceDigest = packet.assuranceDigest

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if ControlStateValid state = false then .rejectInvalidControlState
  else if kind = expectedKind state.stage then
    if identityMatches state packet = false then .rejectIncidentSubstitution
    else if packet.eventDigest = state.lastEventDigest then .rejectEventReplay
    else if packet.supportAssignmentRequested || packet.externalAuthorityRequested then
      .rejectAuthorityLeak
    else match state.stage with
    | .operating =>
      if packet.failureObserved = false then .requestObservation
      else if packet.failureClassRecorded = false then .requestFailureClass
      else if packet.boundaryRecorded = false then .requestBoundary
      else if packet.detectorIndependent = false then .rejectSelfJudgment
      else .acceptDetection
    | .detected =>
      if packet.containmentApplied = false then .requestContainment
      else if packet.escapePathClosed = false then .requestEscapeClosure
      else if packet.containmentOwnerAccepted = false then .requestContainmentOwner
      else .acceptContainment
    | .contained =>
      if packet.causeRecorded = false then .requestCause
      else if packet.remediationApplied = false then .requestRemediation
      else if packet.regressionEvidencePassed = false then .requestRegressionEvidence
      else .acceptRemediation
    | .remediated =>
      if packet.independentReviewRecorded = false then .requestIndependentReview
      else if packet.reviewerIndependent = false then .rejectReviewerCapture
      else if packet.residualRecorded = false then .requestResidual
      else .acceptReview
    | .reviewed =>
      if packet.assuranceCurrent = false then .requestCurrentAssurance
      else if packet.taxonomyCurrent = false then .requestCurrentTaxonomy
      else if packet.residualDischarged = false then .requestResidualDischarge
      else if packet.readmissionAuthorityPresent = false then .requestReadmissionAuthority
      else .acceptReadmission
  else .rejectWrongStage

def accepted : Route -> Bool
  | .acceptDetection | .acceptContainment | .acceptRemediation
  | .acceptReview | .acceptReadmission => true
  | _ => false

def nextStage : Stage -> Stage
  | .operating => .detected
  | .detected => .contained
  | .contained => .remediated
  | .remediated => .reviewed
  | .reviewed => .operating

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       incidentCount := state.incidentCount + (if route = .acceptDetection then 1 else 0)
       recoveryCount := state.recoveryCount + (if route = .acceptReadmission then 1 else 0)
       recurrenceCount := state.recurrenceCount +
         (if route = .acceptDetection && packet.recurrenceOfPriorIncident then 1 else 0)
       openResidualCount :=
         if route = .acceptDetection then state.openResidualCount + 1
         else if route = .acceptReadmission then state.openResidualCount - 1
         else state.openResidualCount
       containmentActive := route != .acceptReadmission
       externalEffectsEnabled := route = .acceptReadmission
       promotionEnabled := route = .acceptReadmission }, route)
  else (state, route)

def RecoveryStep (state : State) (event : Event) : Option State :=
  if accepted (routeFor state event.kind event.packet) then
    some (applyEvent state event.kind event.packet).1
  else none

def RecoveryRun : State → List Event → Option State
  | state, [] => some state
  | state, event :: tail =>
      match RecoveryStep state event with
      | none => none
      | some next => RecoveryRun next tail

def RecoveryTraceValid : State → List Event → Prop
  | _, [] => True
  | state, event :: tail =>
      accepted (routeFor state event.kind event.packet) = true ∧
        RecoveryTraceValid (applyEvent state event.kind event.packet).1 tail

theorem apply_event_preserves_incident_identity
    (state : State) (kind : EventKind) (packet : Packet) :
    exactIdentity (applyEvent state kind packet).1 = exactIdentity state := by
  by_cases h : accepted (routeFor state kind packet) = true <;>
    simp [applyEvent, exactIdentity, h]

theorem accepted_step_is_accepted
    {state next : State} {event : Event}
    (stepped : RecoveryStep state event = some next) :
    accepted (routeFor state event.kind event.packet) = true := by
  unfold RecoveryStep at stepped
  split at stepped
  · assumption
  · simp at stepped

theorem accepted_step_applies_event
    {state next : State} {event : Event}
    (stepped : RecoveryStep state event = some next) :
    next = (applyEvent state event.kind event.packet).1 := by
  unfold RecoveryStep at stepped
  split at stepped
  · exact Option.some.inj stepped |>.symm
  · simp at stepped

theorem accepted_step_adds_exactly_one_receipt
    {state next : State} {event : Event}
    (stepped : RecoveryStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  have acceptedRoute := accepted_step_is_accepted stepped
  have applies := accepted_step_applies_event stepped
  subst next
  simp [applyEvent, acceptedRoute]

theorem accepted_step_starts_from_valid_control_state
    {state next : State} {event : Event}
    (stepped : RecoveryStep state event = some next) :
    ControlStateValid state = true := by
  have acceptedRoute := accepted_step_is_accepted stepped
  by_cases invalid : ControlStateValid state = false
  · simp [routeFor, invalid, accepted] at acceptedRoute
  · cases valid : ControlStateValid state <;> simp_all

theorem accepted_step_updates_incident_count_exactly
    {state next : State} {event : Event}
    (stepped : RecoveryStep state event = some next) :
    next.incidentCount = state.incidentCount +
      (if routeFor state event.kind event.packet = .acceptDetection then 1 else 0) := by
  have acceptedRoute := accepted_step_is_accepted stepped
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, acceptedRoute]

theorem accepted_step_updates_recovery_count_exactly
    {state next : State} {event : Event}
    (stepped : RecoveryStep state event = some next) :
    next.recoveryCount = state.recoveryCount +
      (if routeFor state event.kind event.packet = .acceptReadmission then 1 else 0) := by
  have acceptedRoute := accepted_step_is_accepted stepped
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, acceptedRoute]

theorem accepted_step_updates_recurrence_count_exactly
    {state next : State} {event : Event}
    (stepped : RecoveryStep state event = some next) :
    next.recurrenceCount = state.recurrenceCount +
      (if routeFor state event.kind event.packet = .acceptDetection &&
          event.packet.recurrenceOfPriorIncident then 1 else 0) := by
  have acceptedRoute := accepted_step_is_accepted stepped
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, acceptedRoute]

theorem accepted_step_incident_recovery_and_recurrence_monotone
    {state next : State} {event : Event}
    (stepped : RecoveryStep state event = some next) :
    state.incidentCount ≤ next.incidentCount ∧
      state.recoveryCount ≤ next.recoveryCount ∧
      state.recurrenceCount ≤ next.recurrenceCount := by
  rw [accepted_step_updates_incident_count_exactly stepped,
    accepted_step_updates_recovery_count_exactly stepped,
    accepted_step_updates_recurrence_count_exactly stepped]
  omega

theorem successful_run_preserves_incident_identity
    {state final : State} {events : List Event}
    (ran : RecoveryRun state events = some final) :
    exactIdentity final = exactIdentity state := by
  induction events generalizing state with
  | nil =>
      simp [RecoveryRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : RecoveryStep state event with
      | none => simp [RecoveryRun, stepped] at ran
      | some next =>
          have tailRan : RecoveryRun next tail = some final := by
            simpa [RecoveryRun, stepped] using ran
          calc
            exactIdentity final = exactIdentity next := ih tailRan
            _ = exactIdentity state := by
              have applies := accepted_step_applies_event stepped
              subst next
              exact apply_event_preserves_incident_identity state event.kind event.packet

theorem successful_run_cannot_assign_support_or_external_authority
    {state final : State} {events : List Event}
    (ran : RecoveryRun state events = some final) :
    final.supportAssignmentCount = state.supportAssignmentCount ∧
      final.externalAuthorityCount = state.externalAuthorityCount := by
  induction events generalizing state with
  | nil =>
      simp [RecoveryRun] at ran
      subst final
      exact ⟨rfl, rfl⟩
  | cons event tail ih =>
      cases stepped : RecoveryStep state event with
      | none => simp [RecoveryRun, stepped] at ran
      | some next =>
          have tailRan : RecoveryRun next tail = some final := by
            simpa [RecoveryRun, stepped] using ran
          have tailSafe := ih tailRan
          have applies := accepted_step_applies_event stepped
          subst next
          have headSafe :
              (applyEvent state event.kind event.packet).1.supportAssignmentCount =
                  state.supportAssignmentCount ∧
                (applyEvent state event.kind event.packet).1.externalAuthorityCount =
                  state.externalAuthorityCount := by
            by_cases h : accepted (routeFor state event.kind event.packet) = true <;>
              simp [applyEvent, h]
          exact ⟨tailSafe.1.trans headSafe.1, tailSafe.2.trans headSafe.2⟩

theorem successful_run_adds_exactly_one_receipt_per_event
    {state final : State} {events : List Event}
    (ran : RecoveryRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil =>
      simp [RecoveryRun] at ran
      subst final
      simp
  | cons event tail ih =>
      cases stepped : RecoveryStep state event with
      | none => simp [RecoveryRun, stepped] at ran
      | some next =>
          have tailRan : RecoveryRun next tail = some final := by
            simpa [RecoveryRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [accepted_step_adds_exactly_one_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp only [List.length_cons, Nat.add_assoc]
              rw [Nat.add_comm 1 tail.length]

theorem successful_run_incident_recovery_and_recurrence_monotone
    {state final : State} {events : List Event}
    (ran : RecoveryRun state events = some final) :
    state.incidentCount ≤ final.incidentCount ∧
      state.recoveryCount ≤ final.recoveryCount ∧
      state.recurrenceCount ≤ final.recurrenceCount := by
  induction events generalizing state with
  | nil =>
      simp [RecoveryRun] at ran
      subst final
      exact ⟨Nat.le_refl _, Nat.le_refl _, Nat.le_refl _⟩
  | cons event tail ih =>
      cases stepped : RecoveryStep state event with
      | none => simp [RecoveryRun, stepped] at ran
      | some next =>
          have tailRan : RecoveryRun next tail = some final := by
            simpa [RecoveryRun, stepped] using ran
          have head := accepted_step_incident_recovery_and_recurrence_monotone stepped
          have rest := ih tailRan
          exact ⟨Nat.le_trans head.1 rest.1,
            Nat.le_trans head.2.1 rest.2.1,
            Nat.le_trans head.2.2 rest.2.2⟩

theorem successful_run_has_valid_trace
    {state final : State} {events : List Event}
    (ran : RecoveryRun state events = some final) :
    RecoveryTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : RecoveryStep state event with
      | none => simp [RecoveryRun, stepped] at ran
      | some next =>
          have tailRan : RecoveryRun next tail = some final := by
            simpa [RecoveryRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          subst next
          exact ⟨accepted_step_is_accepted stepped, ih tailRan⟩

theorem recovery_run_composes_across_event_batches
    (state : State) (left right : List Event) :
    RecoveryRun state (left ++ right) =
      match RecoveryRun state left with
      | none => none
      | some middle => RecoveryRun middle right := by
  induction left generalizing state with
  | nil => simp [RecoveryRun]
  | cons event tail ih =>
      cases stepped : RecoveryStep state event <;>
        simp [RecoveryRun, stepped, ih]

theorem rejected_event_preserves_exact_state
    (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = false) :
    (applyEvent state kind packet).1 = state := by
  simp [applyEvent, h]

theorem transition_cannot_assign_support_or_external_authority
    (state : State) (kind : EventKind) (packet : Packet) :
    (applyEvent state kind packet).1.supportAssignmentCount =
        state.supportAssignmentCount ∧
      (applyEvent state kind packet).1.externalAuthorityCount =
        state.externalAuthorityCount := by
  by_cases h : accepted (routeFor state kind packet) = true <;>
    simp [applyEvent, h]

theorem nonoperating_valid_state_blocks_effects_and_promotion
    (state : State)
    (valid : ControlStateValid state = true)
    (notOperating : state.stage ≠ .operating) :
    state.containmentActive = true ∧
      state.externalEffectsEnabled = false ∧
      state.promotionEnabled = false ∧
      state.openResidualCount = 1 := by
  cases stage : state.stage <;> simp [ControlStateValid, stage] at valid notOperating ⊢ <;>
    simp_all

theorem accepted_detection_opens_residual_and_blocks_effects_and_promotion
    (state : State) (kind : EventKind) (packet : Packet)
    (stageOperating : state.stage = .operating)
    (valid : ControlStateValid state = true)
    (h : routeFor state kind packet = .acceptDetection) :
    (applyEvent state kind packet).1.externalEffectsEnabled = false ∧
      (applyEvent state kind packet).1.promotionEnabled = false ∧
      (applyEvent state kind packet).1.containmentActive = true ∧
      (applyEvent state kind packet).1.openResidualCount = 1 := by
  have openZero : state.openResidualCount = 0 := by
    simp [ControlStateValid, stageOperating] at valid
    exact valid.2
  simp [applyEvent, h, accepted, openZero]

theorem accepted_readmission_closes_residual_and_restores_bounded_operation
    (state : State) (kind : EventKind) (packet : Packet)
    (stageReviewed : state.stage = .reviewed)
    (valid : ControlStateValid state = true)
    (h : routeFor state kind packet = .acceptReadmission) :
    (applyEvent state kind packet).1.stage = .operating ∧
      (applyEvent state kind packet).1.openResidualCount = 0 ∧
      (applyEvent state kind packet).1.containmentActive = false ∧
      (applyEvent state kind packet).1.externalEffectsEnabled = true ∧
      (applyEvent state kind packet).1.promotionEnabled = true := by
  have openOne : state.openResidualCount = 1 := by
    simp [ControlStateValid, stageReviewed] at valid
    exact valid.2
  simp [applyEvent, h, accepted, nextStage, stageReviewed, openOne]

theorem accepted_readmission_requires_complete_review
    (state : State) (kind : EventKind) (packet : Packet)
    (stageReviewed : state.stage = .reviewed)
    (kindReadmission : kind = .requestReadmission)
    (h : routeFor state kind packet = .acceptReadmission) :
    identityMatches state packet = true ∧
      packet.assuranceCurrent = true ∧
      packet.taxonomyCurrent = true ∧
      packet.residualDischarged = true ∧
      packet.readmissionAuthorityPresent = true ∧
      packet.supportAssignmentRequested = false ∧
      packet.externalAuthorityRequested = false := by
  have boolTrue {value : Bool} (notFalse : ¬ value = false) : value = true := by
    cases value <;> simp_all
  have boolFalse {value : Bool} (notTrue : ¬ value = true) : value = false := by
    cases value <;> simp_all
  have controlValid : ControlStateValid state = true := by
    by_cases invalid : ControlStateValid state = false
    · simp [routeFor, invalid] at h
    · exact boolTrue invalid
  have identity : identityMatches state packet = true := by
    by_cases missing : identityMatches state packet = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, controlValid,
        missing] at h
    · exact boolTrue missing
  have freshEvent : ¬ packet.eventDigest = state.lastEventDigest := by
    intro replay
    simp [routeFor, expectedKind, stageReviewed, kindReadmission, controlValid,
      identity, replay] at h
  have noSupportRequest : packet.supportAssignmentRequested = false := by
    by_cases requested : packet.supportAssignmentRequested = true
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, controlValid,
        identity, freshEvent, requested] at h
    · exact boolFalse requested
  have noExternalRequest : packet.externalAuthorityRequested = false := by
    by_cases requested : packet.externalAuthorityRequested = true
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, controlValid,
        identity, freshEvent, noSupportRequest, requested] at h
    · exact boolFalse requested
  have currentAssurance : packet.assuranceCurrent = true := by
    by_cases stale : packet.assuranceCurrent = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, controlValid,
        identity, freshEvent, noSupportRequest, noExternalRequest, stale] at h
    · exact boolTrue stale
  have currentTaxonomy : packet.taxonomyCurrent = true := by
    by_cases stale : packet.taxonomyCurrent = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, controlValid,
        identity, freshEvent, noSupportRequest, noExternalRequest, currentAssurance,
        stale] at h
    · exact boolTrue stale
  have residualDischarged : packet.residualDischarged = true := by
    by_cases missing : packet.residualDischarged = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, controlValid,
        identity, freshEvent, noSupportRequest, noExternalRequest, currentAssurance,
        currentTaxonomy, missing] at h
    · exact boolTrue missing
  have readmissionAuthority : packet.readmissionAuthorityPresent = true := by
    by_cases missing : packet.readmissionAuthorityPresent = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, controlValid,
        identity, freshEvent, noSupportRequest, noExternalRequest, currentAssurance,
        currentTaxonomy, residualDischarged, missing] at h
    · exact boolTrue missing
  exact ⟨identity, currentAssurance, currentTaxonomy, residualDischarged,
    readmissionAuthority,
    noSupportRequest, noExternalRequest⟩

def canonicalState (stage : Stage) : State :=
  { stage := stage, incidentId := 41, boundaryVersion := 3,
    architectureDigest := 101, policyDigest := 102, detectorDigest := 103,
    containmentDigest := 104, remediationDigest := 105, reviewerDigest := 106,
    assuranceDigest := 107, lastEventDigest := 0, receiptCount := 0,
    incidentCount := openIncidentCount stage, recoveryCount := 0,
    recurrenceCount := 0, openResidualCount := openIncidentCount stage,
    containmentActive := stage != .operating,
    externalEffectsEnabled := stage = .operating,
    promotionEnabled := stage = .operating,
    supportAssignmentCount := 0, externalAuthorityCount := 0 }

def canonicalPacket (eventDigest : Nat) : Packet :=
  { incidentId := 41, boundaryVersion := 3, architectureDigest := 101,
    policyDigest := 102, detectorDigest := 103, containmentDigest := 104,
    remediationDigest := 105, reviewerDigest := 106, assuranceDigest := 107,
    eventDigest := eventDigest, failureObserved := true,
    failureClassRecorded := true, boundaryRecorded := true,
    detectorIndependent := true,
    containmentApplied := true, escapePathClosed := true,
    containmentOwnerAccepted := true, causeRecorded := true,
    remediationApplied := true, regressionEvidencePassed := true,
    independentReviewRecorded := true, reviewerIndependent := true,
    residualRecorded := true, assuranceCurrent := true, taxonomyCurrent := true,
    residualDischarged := true,
    readmissionAuthorityPresent := true, recurrenceOfPriorIncident := false,
    supportAssignmentRequested := false, externalAuthorityRequested := false }

theorem missing_escape_closure_blocks_containment :
    routeFor (canonicalState .detected) .confirmContainment
      { canonicalPacket 2 with escapePathClosed := false } = .requestEscapeClosure := by
  rfl

theorem captured_reviewer_blocks_review :
    routeFor (canonicalState .remediated) .recordReview
      { canonicalPacket 4 with reviewerIndependent := false } = .rejectReviewerCapture := by
  rfl

theorem stale_assurance_blocks_readmission :
    routeFor (canonicalState .reviewed) .requestReadmission
      { canonicalPacket 5 with assuranceCurrent := false } = .requestCurrentAssurance := by
  rfl

theorem authority_leak_blocks_every_stage
    (stage : Stage) :
    routeFor (canonicalState stage) (expectedKind stage)
      { canonicalPacket 9 with supportAssignmentRequested := true } =
        .rejectAuthorityLeak := by
  cases stage <;> rfl

theorem bounded_failure_recovery_reaches_guarded_readmission :
  let s0 := canonicalState .operating
  let s1 := (applyEvent s0 .detectAndIsolate (canonicalPacket 1)).1
  let s2 := (applyEvent s1 .confirmContainment (canonicalPacket 2)).1
  let s3 := (applyEvent s2 .recordRemediation (canonicalPacket 3)).1
  let s4 := (applyEvent s3 .recordReview (canonicalPacket 4)).1
  let s5 := (applyEvent s4 .requestReadmission (canonicalPacket 5)).1
  s5.stage = .operating ∧ s5.receiptCount = 5 ∧ s5.incidentCount = 1 ∧
    s5.recoveryCount = 1 ∧ s5.openResidualCount = 0 ∧
    s5.containmentActive = false ∧ s5.externalEffectsEnabled = true ∧
    s5.promotionEnabled = true ∧
    s5.supportAssignmentCount = 0 ∧ s5.externalAuthorityCount = 0 := by
  native_decide

theorem bounded_recurrence_reisolates_after_recovery :
  let s0 := canonicalState .operating
  let s1 := (applyEvent s0 .detectAndIsolate (canonicalPacket 1)).1
  let s2 := (applyEvent s1 .confirmContainment (canonicalPacket 2)).1
  let s3 := (applyEvent s2 .recordRemediation (canonicalPacket 3)).1
  let s4 := (applyEvent s3 .recordReview (canonicalPacket 4)).1
  let s5 := (applyEvent s4 .requestReadmission (canonicalPacket 5)).1
  let recurrence := { canonicalPacket 6 with recurrenceOfPriorIncident := true }
  let s6 := (applyEvent s5 .detectAndIsolate recurrence).1
  s6.stage = .detected ∧ s6.receiptCount = 6 ∧ s6.incidentCount = 2 ∧
    s6.recoveryCount = 1 ∧ s6.recurrenceCount = 1 ∧
    s6.openResidualCount = 1 ∧ s6.containmentActive = true ∧
    s6.externalEffectsEnabled = false ∧ s6.promotionEnabled = false ∧
    s6.supportAssignmentCount = 0 ∧
    s6.externalAuthorityCount = 0 := by
  native_decide

inductive ObservationRoute where
  | rejectInvalidControlState
  | rejectNonoperatingIngress
  | rejectIncidentSubstitution
  | rejectObservationReplay
  | requestIncidentRecord
  | requestEvidenceReceipt
  | preserveUnmappedResidual
  | rejectCapturedDetector
  | requestAuthorityReview
  | requestQuarantine
  | rejectRecurrenceSubstitution
  | requestNonClaimBoundary
  | rejectAuthorityLeak
  | admitRecovery
  | admitRecurrenceRecovery
  | admitSevereRecovery
deriving DecidableEq, Repr

structure IncidentObservation where
  packet : Packet
  detectorObserverDigest : Nat
  subjectDigest : Nat
  incidentRecorded : Bool
  evidenceReceiptRecorded : Bool
  authorityRequested : Nat
  authorityCeiling : Nat
  escapePathOpen : Bool
  quarantineRecorded : Bool
  recurrenceObserved : Bool
  severityHigh : Bool
  reversible : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def ObservationAdmissible (state : State) (observation : IncidentObservation) : Prop :=
  ControlStateValid state = true ∧
    state.stage = .operating ∧
    identityMatches state observation.packet = true ∧
    observation.packet.eventDigest ≠ state.lastEventDigest ∧
    observation.incidentRecorded = true ∧
    observation.evidenceReceiptRecorded = true ∧
    observation.packet.failureObserved = true ∧
    observation.packet.failureClassRecorded = true ∧
    observation.packet.boundaryRecorded = true ∧
    observation.packet.detectorIndependent = true ∧
    observation.detectorObserverDigest ≠ observation.subjectDigest ∧
    observation.authorityRequested ≤ observation.authorityCeiling ∧
    (observation.escapePathOpen = false ∨ observation.quarantineRecorded = true) ∧
    observation.packet.recurrenceOfPriorIncident = observation.recurrenceObserved ∧
    observation.nonClaimBoundaryRecorded = true ∧
    observation.packet.supportAssignmentRequested = false ∧
    observation.packet.externalAuthorityRequested = false

instance observationAdmissibleDecidable (state : State) (observation : IncidentObservation) :
    Decidable (ObservationAdmissible state observation) := by
  unfold ObservationAdmissible
  infer_instance

def observationRouteFor (state : State) (observation : IncidentObservation) :
    ObservationRoute :=
  if ObservationAdmissible state observation then
    if observation.recurrenceObserved then .admitRecurrenceRecovery
    else if observation.severityHigh && !observation.reversible then
      .admitSevereRecovery
    else .admitRecovery
  else if ControlStateValid state = false then .rejectInvalidControlState
  else if state.stage != .operating then .rejectNonoperatingIngress
  else if identityMatches state observation.packet = false then
    .rejectIncidentSubstitution
  else if observation.packet.eventDigest = state.lastEventDigest then
    .rejectObservationReplay
  else if observation.incidentRecorded = false then .requestIncidentRecord
  else if observation.evidenceReceiptRecorded = false then .requestEvidenceReceipt
  else if observation.packet.failureObserved = false ||
      observation.packet.failureClassRecorded = false ||
      observation.packet.boundaryRecorded = false then
    .preserveUnmappedResidual
  else if observation.packet.detectorIndependent = false ||
      observation.detectorObserverDigest = observation.subjectDigest then
    .rejectCapturedDetector
  else if observation.authorityCeiling < observation.authorityRequested then
    .requestAuthorityReview
  else if observation.escapePathOpen && !observation.quarantineRecorded then
    .requestQuarantine
  else if observation.packet.recurrenceOfPriorIncident !=
      observation.recurrenceObserved then
    .rejectRecurrenceSubstitution
  else if observation.nonClaimBoundaryRecorded = false then
    .requestNonClaimBoundary
  else if observation.packet.supportAssignmentRequested ||
      observation.packet.externalAuthorityRequested then .rejectAuthorityLeak
  else .requestNonClaimBoundary

def ingestObservation (state : State) (observation : IncidentObservation) :
    State × ObservationRoute :=
  let route := observationRouteFor state observation
  if ObservationAdmissible state observation then
    ((applyEvent state .detectAndIsolate observation.packet).1, route)
  else (state, route)

theorem rejected_observation_preserves_exact_state
    (state : State) (observation : IncidentObservation)
    (rejected : ¬ ObservationAdmissible state observation) :
    (ingestObservation state observation).1 = state := by
  simp [ingestObservation, rejected]

theorem accepted_observation_starts_from_valid_operating_state
    (state : State) (observation : IncidentObservation)
    (admitted : ObservationAdmissible state observation) :
    ControlStateValid state = true ∧ state.stage = .operating := by
  exact ⟨admitted.1, admitted.2.1⟩

theorem admitted_observation_requires_record_evidence_independence_and_boundary
    (state : State) (observation : IncidentObservation)
    (admitted : ObservationAdmissible state observation) :
    observation.incidentRecorded = true ∧
      observation.evidenceReceiptRecorded = true ∧
      observation.packet.failureObserved = true ∧
      observation.packet.failureClassRecorded = true ∧
      observation.packet.boundaryRecorded = true ∧
      observation.packet.detectorIndependent = true ∧
      observation.detectorObserverDigest ≠ observation.subjectDigest ∧
      observation.authorityRequested ≤ observation.authorityCeiling ∧
      observation.nonClaimBoundaryRecorded = true ∧
      observation.packet.supportAssignmentRequested = false ∧
      observation.packet.externalAuthorityRequested = false := by
  rcases admitted with ⟨_, _, _, _, incident, evidence, observed, failureClass,
    boundary, independent, separated, authority, _, _, nonClaim, noSupport,
    noExternal⟩
  exact ⟨incident, evidence, observed, failureClass, boundary, independent,
    separated, authority, nonClaim, noSupport, noExternal⟩

theorem accepted_observation_refines_recovery_detection
    (state : State) (observation : IncidentObservation)
    (admitted : ObservationAdmissible state observation) :
    routeFor state .detectAndIsolate observation.packet = .acceptDetection := by
  have gates := admitted_observation_requires_record_evidence_independence_and_boundary
    state observation admitted
  have start := accepted_observation_starts_from_valid_operating_state
    state observation admitted
  rcases gates with ⟨_, _, observed, failureClass, boundary, independent, _, _, _,
    noSupport, noExternal⟩
  have identity := admitted.2.2.1
  have fresh := admitted.2.2.2.1
  simp [routeFor, start.1, start.2, expectedKind, identity, fresh, noSupport,
    noExternal, observed, failureClass, boundary, independent]

theorem accepted_observation_preserves_incident_identity
    (state : State) (observation : IncidentObservation)
    (admitted : ObservationAdmissible state observation) :
    exactIdentity (ingestObservation state observation).1 = exactIdentity state := by
  simp [ingestObservation, admitted,
    apply_event_preserves_incident_identity state .detectAndIsolate observation.packet]

theorem accepted_observation_opens_residual_and_blocks_effects_and_promotion
    (state : State) (observation : IncidentObservation)
    (admitted : ObservationAdmissible state observation) :
    (ingestObservation state observation).1.stage = .detected ∧
      (ingestObservation state observation).1.openResidualCount = 1 ∧
      (ingestObservation state observation).1.containmentActive = true ∧
      (ingestObservation state observation).1.externalEffectsEnabled = false ∧
      (ingestObservation state observation).1.promotionEnabled = false := by
  have start := accepted_observation_starts_from_valid_operating_state
    state observation admitted
  have refined := accepted_observation_refines_recovery_detection
    state observation admitted
  have blocked := accepted_detection_opens_residual_and_blocks_effects_and_promotion
    state .detectAndIsolate observation.packet start.2 start.1 refined
  have openZero : state.openResidualCount = 0 := by
    have valid := start.1
    simp [ControlStateValid, start.2] at valid
    exact valid.2
  simp [ingestObservation, admitted, applyEvent, refined, accepted, start.2,
    nextStage, openZero]

theorem accepted_observation_cannot_assign_support_or_external_authority
    (state : State) (observation : IncidentObservation)
    (admitted : ObservationAdmissible state observation) :
    (ingestObservation state observation).1.supportAssignmentCount =
        state.supportAssignmentCount ∧
      (ingestObservation state observation).1.externalAuthorityCount =
        state.externalAuthorityCount := by
  have unchanged := transition_cannot_assign_support_or_external_authority
    state .detectAndIsolate observation.packet
  simpa [ingestObservation, admitted] using unchanged

theorem accepted_observation_records_exactly_one_incident_and_receipt
    (state : State) (observation : IncidentObservation)
    (admitted : ObservationAdmissible state observation) :
    (ingestObservation state observation).1.incidentCount = state.incidentCount + 1 ∧
      (ingestObservation state observation).1.receiptCount = state.receiptCount + 1 := by
  have refined := accepted_observation_refines_recovery_detection
    state observation admitted
  simp [ingestObservation, admitted, applyEvent, refined, accepted]

def canonicalObservation (eventDigest : Nat) : IncidentObservation :=
  { packet := canonicalPacket eventDigest
    detectorObserverDigest := 501
    subjectDigest := 502
    incidentRecorded := true
    evidenceReceiptRecorded := true
    authorityRequested := 2
    authorityCeiling := 3
    escapePathOpen := false
    quarantineRecorded := true
    recurrenceObserved := false
    severityHigh := false
    reversible := true
    nonClaimBoundaryRecorded := true }

theorem missing_observation_receipt_requests_evidence :
    observationRouteFor (canonicalState .operating)
      { canonicalObservation 1 with evidenceReceiptRecorded := false } =
        .requestEvidenceReceipt := by
  native_decide

theorem unclassified_observation_preserves_unmapped_residual :
    observationRouteFor (canonicalState .operating)
      { canonicalObservation 1 with
        packet := { canonicalPacket 1 with failureClassRecorded := false } } =
        .preserveUnmappedResidual := by
  native_decide

theorem captured_detector_cannot_admit_recovery :
    observationRouteFor (canonicalState .operating)
      { canonicalObservation 1 with detectorObserverDigest := 502 } =
        .rejectCapturedDetector := by
  native_decide

theorem authority_over_ceiling_cannot_admit_recovery :
    observationRouteFor (canonicalState .operating)
      { canonicalObservation 1 with authorityRequested := 4 } =
        .requestAuthorityReview := by
  native_decide

theorem open_escape_without_quarantine_cannot_admit_recovery :
    observationRouteFor (canonicalState .operating)
      { { canonicalObservation 1 with escapePathOpen := true } with
        quarantineRecorded := false } = .requestQuarantine := by
  native_decide

theorem recurrence_marker_substitution_cannot_admit_recovery :
    observationRouteFor (canonicalState .operating)
      { canonicalObservation 1 with recurrenceObserved := true } =
        .rejectRecurrenceSubstitution := by
  native_decide

theorem complete_recurrence_observation_admits_escalated_recovery :
    observationRouteFor (canonicalState .operating)
      { { canonicalObservation 1 with
        packet := { canonicalPacket 1 with recurrenceOfPriorIncident := true } } with
        recurrenceObserved := true } = .admitRecurrenceRecovery := by
  native_decide

theorem complete_severe_irreversible_observation_admits_escalated_recovery :
    observationRouteFor (canonicalState .operating)
      { { canonicalObservation 1 with severityHigh := true } with reversible := false } =
        .admitSevereRecovery := by
  native_decide

theorem complete_ordinary_observation_reaches_isolated_recovery :
    let result := ingestObservation (canonicalState .operating) (canonicalObservation 1)
    result.2 = .admitRecovery ∧
      result.1.stage = .detected ∧ result.1.openResidualCount = 1 ∧
      result.1.containmentActive = true ∧
      result.1.externalEffectsEnabled = false ∧ result.1.promotionEnabled = false ∧
      result.1.receiptCount = 1 ∧ result.1.incidentCount = 1 ∧
      result.1.supportAssignmentCount = 0 ∧ result.1.externalAuthorityCount = 0 := by
  native_decide

end AsiStackProofs.FailureRecoveryRefinement
