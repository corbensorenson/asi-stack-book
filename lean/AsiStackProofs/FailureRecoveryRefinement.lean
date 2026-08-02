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
  | rejectWrongStage
  | rejectIncidentSubstitution
  | rejectEventReplay
  | rejectAuthorityLeak
  | requestObservation
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
  recoveryCount : Nat
  recurrenceCount : Nat
  containmentActive : Bool
  externalEffectsEnabled : Bool
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
  if kind = expectedKind state.stage then
    if identityMatches state packet = false then .rejectIncidentSubstitution
    else if packet.eventDigest = state.lastEventDigest then .rejectEventReplay
    else if packet.supportAssignmentRequested || packet.externalAuthorityRequested then
      .rejectAuthorityLeak
    else match state.stage with
    | .operating =>
      if packet.failureObserved = false then .requestObservation
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
       recoveryCount := state.recoveryCount + (if route = .acceptReadmission then 1 else 0)
       recurrenceCount := state.recurrenceCount +
         (if route = .acceptDetection && packet.recurrenceOfPriorIncident then 1 else 0)
       containmentActive := route != .acceptReadmission
       externalEffectsEnabled := route = .acceptReadmission }, route)
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

theorem accepted_detection_disables_effects_and_activates_containment
    (state : State) (kind : EventKind) (packet : Packet)
    (h : routeFor state kind packet = .acceptDetection) :
    (applyEvent state kind packet).1.externalEffectsEnabled = false ∧
      (applyEvent state kind packet).1.containmentActive = true := by
  simp [applyEvent, h, accepted]

theorem accepted_readmission_requires_complete_review
    (state : State) (kind : EventKind) (packet : Packet)
    (stageReviewed : state.stage = .reviewed)
    (kindReadmission : kind = .requestReadmission)
    (h : routeFor state kind packet = .acceptReadmission) :
    identityMatches state packet = true ∧
      packet.assuranceCurrent = true ∧
      packet.taxonomyCurrent = true ∧
      packet.readmissionAuthorityPresent = true ∧
      packet.supportAssignmentRequested = false ∧
      packet.externalAuthorityRequested = false := by
  have boolTrue {value : Bool} (notFalse : ¬ value = false) : value = true := by
    cases value <;> simp_all
  have boolFalse {value : Bool} (notTrue : ¬ value = true) : value = false := by
    cases value <;> simp_all
  have identity : identityMatches state packet = true := by
    by_cases missing : identityMatches state packet = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, missing] at h
    · exact boolTrue missing
  have freshEvent : ¬ packet.eventDigest = state.lastEventDigest := by
    intro replay
    simp [routeFor, expectedKind, stageReviewed, kindReadmission, identity, replay] at h
  have noSupportRequest : packet.supportAssignmentRequested = false := by
    by_cases requested : packet.supportAssignmentRequested = true
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, identity, freshEvent,
        requested] at h
    · exact boolFalse requested
  have noExternalRequest : packet.externalAuthorityRequested = false := by
    by_cases requested : packet.externalAuthorityRequested = true
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, identity, freshEvent,
        noSupportRequest, requested] at h
    · exact boolFalse requested
  have currentAssurance : packet.assuranceCurrent = true := by
    by_cases stale : packet.assuranceCurrent = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, identity, freshEvent,
        noSupportRequest, noExternalRequest, stale] at h
    · exact boolTrue stale
  have currentTaxonomy : packet.taxonomyCurrent = true := by
    by_cases stale : packet.taxonomyCurrent = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, identity, freshEvent,
        noSupportRequest, noExternalRequest, currentAssurance, stale] at h
    · exact boolTrue stale
  have readmissionAuthority : packet.readmissionAuthorityPresent = true := by
    by_cases missing : packet.readmissionAuthorityPresent = false
    · simp [routeFor, expectedKind, stageReviewed, kindReadmission, identity, freshEvent,
        noSupportRequest, noExternalRequest, currentAssurance, currentTaxonomy,
        missing] at h
    · exact boolTrue missing
  exact ⟨identity, currentAssurance, currentTaxonomy, readmissionAuthority,
    noSupportRequest, noExternalRequest⟩

def canonicalState (stage : Stage) : State :=
  { stage := stage, incidentId := 41, boundaryVersion := 3,
    architectureDigest := 101, policyDigest := 102, detectorDigest := 103,
    containmentDigest := 104, remediationDigest := 105, reviewerDigest := 106,
    assuranceDigest := 107, lastEventDigest := 0, receiptCount := 0,
    recoveryCount := 0, recurrenceCount := 0,
    containmentActive := stage != .operating,
    externalEffectsEnabled := stage = .operating,
    supportAssignmentCount := 0, externalAuthorityCount := 0 }

def canonicalPacket (eventDigest : Nat) : Packet :=
  { incidentId := 41, boundaryVersion := 3, architectureDigest := 101,
    policyDigest := 102, detectorDigest := 103, containmentDigest := 104,
    remediationDigest := 105, reviewerDigest := 106, assuranceDigest := 107,
    eventDigest := eventDigest, failureObserved := true, detectorIndependent := true,
    containmentApplied := true, escapePathClosed := true,
    containmentOwnerAccepted := true, causeRecorded := true,
    remediationApplied := true, regressionEvidencePassed := true,
    independentReviewRecorded := true, reviewerIndependent := true,
    residualRecorded := true, assuranceCurrent := true, taxonomyCurrent := true,
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
  s5.stage = .operating ∧ s5.receiptCount = 5 ∧ s5.recoveryCount = 1 ∧
    s5.containmentActive = false ∧ s5.externalEffectsEnabled = true ∧
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
  s6.stage = .detected ∧ s6.receiptCount = 6 ∧ s6.recoveryCount = 1 ∧
    s6.recurrenceCount = 1 ∧ s6.containmentActive = true ∧
    s6.externalEffectsEnabled = false ∧ s6.supportAssignmentCount = 0 ∧
    s6.externalAuthorityCount = 0 := by
  native_decide

end AsiStackProofs.FailureRecoveryRefinement
