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
