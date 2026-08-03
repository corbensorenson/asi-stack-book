namespace AsiStackProofs.ObservationTrust

inductive Hypothesis where
  | obstacle
  | clearPath
  | unknown
deriving DecidableEq, Repr

structure ChannelEvidence where
  channelDigest : Nat
  dependenceRoot : Nat
  hypothesis : Hypothesis
  fresh : Bool
  calibrated : Bool
  lineagePresent : Bool
  clockPoseAligned : Bool
deriving DecidableEq, Repr

inductive PairDisposition where
  | inadmissible
  | disagreement
  | correlatedAgreement
  | independentAgreement
deriving DecidableEq, Repr

def usable (channel : ChannelEvidence) : Bool :=
  channel.fresh && channel.calibrated && channel.lineagePresent &&
    channel.clockPoseAligned

def classifyPair (left right : ChannelEvidence) : PairDisposition :=
  if ! usable left || ! usable right then .inadmissible
  else if left.hypothesis != right.hypothesis then .disagreement
  else if left.dependenceRoot == right.dependenceRoot then .correlatedAgreement
  else .independentAgreement

def independentEvidenceCount : PairDisposition -> Nat
  | .inadmissible => 0
  | .disagreement => 0
  | .correlatedAgreement => 1
  | .independentAgreement => 2

theorem eligible_agreement_with_same_root_is_correlated
    (left right : ChannelEvidence)
    (leftUsable : usable left = true)
    (rightUsable : usable right = true)
    (sameHypothesis : left.hypothesis = right.hypothesis)
    (sameRoot : left.dependenceRoot = right.dependenceRoot) :
    classifyPair left right = .correlatedAgreement := by
  simp [classifyPair, leftUsable, rightUsable, sameHypothesis, sameRoot]

theorem declared_same_root_agreement_counts_one
    (left right : ChannelEvidence)
    (leftUsable : usable left = true)
    (rightUsable : usable right = true)
    (sameHypothesis : left.hypothesis = right.hypothesis)
    (sameRoot : left.dependenceRoot = right.dependenceRoot) :
    independentEvidenceCount (classifyPair left right) = 1 := by
  rw [eligible_agreement_with_same_root_is_correlated left right leftUsable
    rightUsable sameHypothesis sameRoot]
  rfl

theorem eligible_agreement_with_distinct_roots_is_independent
    (left right : ChannelEvidence)
    (leftUsable : usable left = true)
    (rightUsable : usable right = true)
    (sameHypothesis : left.hypothesis = right.hypothesis)
    (distinctRoots : left.dependenceRoot ≠ right.dependenceRoot) :
    classifyPair left right = .independentAgreement := by
  simp [classifyPair, leftUsable, rightUsable, sameHypothesis, distinctRoots]

theorem eligible_disagreement_is_preserved
    (left right : ChannelEvidence)
    (leftUsable : usable left = true)
    (rightUsable : usable right = true)
    (differentHypotheses : left.hypothesis ≠ right.hypothesis) :
    classifyPair left right = .disagreement := by
  simp [classifyPair, leftUsable, rightUsable, differentHypotheses]

def cameraA : ChannelEvidence :=
  { channelDigest := 11, dependenceRoot := 7, hypothesis := .obstacle,
    fresh := true, calibrated := true, lineagePresent := true,
    clockPoseAligned := true }

def cameraBSharedEncoder : ChannelEvidence :=
  { channelDigest := 12, dependenceRoot := 7, hypothesis := .obstacle,
    fresh := true, calibrated := true, lineagePresent := true,
    clockPoseAligned := true }

def lidarIndependent : ChannelEvidence :=
  { channelDigest := 13, dependenceRoot := 9, hypothesis := .obstacle,
    fresh := true, calibrated := true, lineagePresent := true,
    clockPoseAligned := true }

def lidarDisagrees : ChannelEvidence :=
  { lidarIndependent with hypothesis := .clearPath }

theorem correlated_pair_witness_counts_one_independent_item :
    classifyPair cameraA cameraBSharedEncoder = .correlatedAgreement ∧
    independentEvidenceCount (classifyPair cameraA cameraBSharedEncoder) = 1 := by
  decide

theorem independent_pair_witness_counts_two_independent_items :
    classifyPair cameraA lidarIndependent = .independentAgreement ∧
    independentEvidenceCount (classifyPair cameraA lidarIndependent) = 2 := by
  decide

theorem disagreement_witness_is_not_collapsed_into_agreement :
    classifyPair cameraA lidarDisagrees = .disagreement ∧
    independentEvidenceCount (classifyPair cameraA lidarDisagrees) = 0 := by
  decide

inductive Stage where
  | captured
  | identitiesBound
  | dependenceBound
  | pairReviewed
  | useBound
  | handedOff
  | invalidated
deriving DecidableEq, Repr

inductive EventKind where
  | bindIdentities
  | bindDependence
  | reviewPair
  | bindUse
  | handoffObservation
  | invalidateForChange
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage
  | rejectIdentitySubstitution
  | rejectReplay
  | rejectAuthorityLeak
  | rejectTruthOverclaim
  | requestSensorIdentity
  | requestCalibration
  | requestClockPose
  | requestLineage
  | requestFreshness
  | requestDependenceRoots
  | requestCommonCauseReview
  | requestPairClassification
  | requestEvidenceCountMatch
  | rejectCorrelatedInflation
  | requestDisagreementPreservation
  | requestBoundedAuthority
  | requestExpiry
  | requestFallback
  | requestResidualOwner
  | requestConsumer
  | requestMaximumInference
  | requestIndependentReview
  | requestMaterialChange
  | requestDescendantInvalidation
  | requestOrdinaryRouteBlock
  | requestRereviewRoute
  | acceptIdentities
  | acceptDependence
  | acceptPairReview
  | acceptUseBinding
  | acceptHandoff
  | acceptInvalidation
deriving DecidableEq, Repr

structure Packet where
  observationDigest : Nat
  channelSetDigest : Nat
  calibrationDigest : Nat
  clockPoseDigest : Nat
  dependenceDigest : Nat
  hypothesisDigest : Nat
  consumerDigest : Nat
  residualDigest : Nat
  protocolVersion : Nat
  eventDigest : Nat
  pairDisposition : PairDisposition
  computedIndependentCount : Nat
  requestedIndependentCount : Nat
  sensorIdentityPresent : Bool
  calibrationPresent : Bool
  clockPosePresent : Bool
  lineagePresent : Bool
  fresh : Bool
  dependenceRootsDeclared : Bool
  commonCauseReviewed : Bool
  pairClassificationPresent : Bool
  evidenceCountMatchesClassification : Bool
  disagreementPreserved : Bool
  authorityBounded : Bool
  expiryPresent : Bool
  fallbackPresent : Bool
  residualOwnerPresent : Bool
  consumerPresent : Bool
  maximumInferencePresent : Bool
  independentReview : Bool
  materialChangeRecorded : Bool
  descendantsInvalidated : Bool
  ordinaryRouteBlocked : Bool
  rereviewRoutePresent : Bool
  environmentalTruthAsserted : Bool
  independenceBeyondModelAsserted : Bool
  supportAssignmentRequested : Bool
  externalAuthorityRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  observationDigest : Nat
  channelSetDigest : Nat
  calibrationDigest : Nat
  clockPoseDigest : Nat
  dependenceDigest : Nat
  hypothesisDigest : Nat
  consumerDigest : Nat
  residualDigest : Nat
  protocolVersion : Nat
  pairDisposition : PairDisposition
  computedIndependentCount : Nat
  requestedIndependentCount : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  handoffCount : Nat
  invalidationCount : Nat
  supportAssignmentCount : Nat
  externalAuthorityCount : Nat
deriving DecidableEq, Repr

structure ObservationIdentity where
  observationDigest : Nat
  channelSetDigest : Nat
  calibrationDigest : Nat
  clockPoseDigest : Nat
  dependenceDigest : Nat
  hypothesisDigest : Nat
  consumerDigest : Nat
  residualDigest : Nat
  protocolVersion : Nat
  pairDisposition : PairDisposition
  computedIndependentCount : Nat
  requestedIndependentCount : Nat
deriving DecidableEq, Repr

def observationIdentity (state : State) : ObservationIdentity :=
  { observationDigest := state.observationDigest
    channelSetDigest := state.channelSetDigest
    calibrationDigest := state.calibrationDigest
    clockPoseDigest := state.clockPoseDigest
    dependenceDigest := state.dependenceDigest
    hypothesisDigest := state.hypothesisDigest
    consumerDigest := state.consumerDigest
    residualDigest := state.residualDigest
    protocolVersion := state.protocolVersion
    pairDisposition := state.pairDisposition
    computedIndependentCount := state.computedIndependentCount
    requestedIndependentCount := state.requestedIndependentCount }

def expectedKind : Stage -> EventKind
  | .captured => .bindIdentities
  | .identitiesBound => .bindDependence
  | .dependenceBound => .reviewPair
  | .pairReviewed => .bindUse
  | .useBound => .handoffObservation
  | .handedOff => .invalidateForChange
  | .invalidated => .invalidateForChange

def exactBinding (state : State) (packet : Packet) : Bool :=
  packet.observationDigest == state.observationDigest &&
  packet.channelSetDigest == state.channelSetDigest &&
  packet.calibrationDigest == state.calibrationDigest &&
  packet.clockPoseDigest == state.clockPoseDigest &&
  packet.dependenceDigest == state.dependenceDigest &&
  packet.hypothesisDigest == state.hypothesisDigest &&
  packet.consumerDigest == state.consumerDigest &&
  packet.residualDigest == state.residualDigest &&
  packet.protocolVersion == state.protocolVersion &&
  packet.pairDisposition == state.pairDisposition &&
  packet.computedIndependentCount == state.computedIndependentCount &&
  packet.requestedIndependentCount == state.requestedIndependentCount

def routeFor (state : State) (event : Event) : Route :=
  if state.stage == .invalidated then .rejectWrongStage
  else if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactBinding state event.packet then .rejectIdentitySubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectReplay
  else if event.packet.supportAssignmentRequested ||
      event.packet.externalAuthorityRequested then .rejectAuthorityLeak
  else if event.packet.environmentalTruthAsserted ||
      event.packet.independenceBeyondModelAsserted then .rejectTruthOverclaim
  else match state.stage with
  | .captured =>
      if ! event.packet.sensorIdentityPresent then .requestSensorIdentity
      else if ! event.packet.calibrationPresent then .requestCalibration
      else if ! event.packet.clockPosePresent then .requestClockPose
      else if ! event.packet.lineagePresent then .requestLineage
      else if ! event.packet.fresh then .requestFreshness
      else .acceptIdentities
  | .identitiesBound =>
      if ! event.packet.dependenceRootsDeclared then .requestDependenceRoots
      else if ! event.packet.commonCauseReviewed then .requestCommonCauseReview
      else .acceptDependence
  | .dependenceBound =>
      if ! event.packet.pairClassificationPresent then .requestPairClassification
      else if ! event.packet.evidenceCountMatchesClassification then
        .requestEvidenceCountMatch
      else if event.packet.pairDisposition = .correlatedAgreement &&
          event.packet.computedIndependentCount > 1 then .rejectCorrelatedInflation
      else if event.packet.pairDisposition = .disagreement &&
          ! event.packet.disagreementPreserved then .requestDisagreementPreservation
      else .acceptPairReview
  | .pairReviewed =>
      if event.packet.requestedIndependentCount >
          event.packet.computedIndependentCount then .rejectCorrelatedInflation
      else if ! event.packet.authorityBounded then .requestBoundedAuthority
      else if ! event.packet.expiryPresent then .requestExpiry
      else if ! event.packet.fallbackPresent then .requestFallback
      else if ! event.packet.residualOwnerPresent then .requestResidualOwner
      else .acceptUseBinding
  | .useBound =>
      if ! event.packet.consumerPresent then .requestConsumer
      else if ! event.packet.maximumInferencePresent then .requestMaximumInference
      else if ! event.packet.independentReview then .requestIndependentReview
      else .acceptHandoff
  | .handedOff =>
      if ! event.packet.materialChangeRecorded then .requestMaterialChange
      else if ! event.packet.descendantsInvalidated then .requestDescendantInvalidation
      else if ! event.packet.ordinaryRouteBlocked then .requestOrdinaryRouteBlock
      else if ! event.packet.rereviewRoutePresent then .requestRereviewRoute
      else .acceptInvalidation
  | .invalidated => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptIdentities | .acceptDependence | .acceptPairReview
  | .acceptUseBinding | .acceptHandoff | .acceptInvalidation => true
  | _ => false

def advance : Stage -> Stage
  | .captured => .identitiesBound
  | .identitiesBound => .dependenceBound
  | .dependenceBound => .pairReviewed
  | .pairReviewed => .useBound
  | .useBound => .handedOff
  | .handedOff => .invalidated
  | .invalidated => .invalidated

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advance state.stage
       lastEventDigest := event.packet.eventDigest
       receiptCount := state.receiptCount + 1
       handoffCount := state.handoffCount + (if route = .acceptHandoff then 1 else 0)
       invalidationCount := state.invalidationCount +
         (if route = .acceptInvalidation then 1 else 0) }, route)
  else (state, route)

def ObservationStep (state : State) (event : Event) : Option State :=
  if accepted (routeFor state event) then
    some (applyEvent state event).1
  else none

def ObservationRun : State → List Event → Option State
  | state, [] => some state
  | state, event :: tail =>
      match ObservationStep state event with
      | none => none
      | some next => ObservationRun next tail

def ProcessObservationEvent (state : State) (event : Event) : State × Bool :=
  match ObservationStep state event with
  | none => (state, false)
  | some next => (next, true)

def ObservationTraceValid : State → List Event → Prop
  | _, [] => True
  | state, event :: tail =>
      accepted (routeFor state event) = true ∧
        ObservationTraceValid (applyEvent state event).1 tail

theorem rejected_event_preserves_exact_state (state : State) (event : Event)
    (rejected : accepted (routeFor state event) = false) :
    (applyEvent state event).1 = state := by
  simp [applyEvent, rejected]

theorem apply_event_preserves_observation_identity (state : State) (event : Event) :
    (applyEvent state event).1.observationDigest = state.observationDigest ∧
    (applyEvent state event).1.channelSetDigest = state.channelSetDigest ∧
    (applyEvent state event).1.dependenceDigest = state.dependenceDigest ∧
    (applyEvent state event).1.hypothesisDigest = state.hypothesisDigest ∧
    (applyEvent state event).1.protocolVersion = state.protocolVersion := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_authority
    (state : State) (event : Event) :
    (applyEvent state event).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state event).1.externalAuthorityCount = state.externalAuthorityCount := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem apply_event_preserves_exact_observation_identity
    (state : State) (event : Event) :
    observationIdentity (applyEvent state event).1 = observationIdentity state := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, observationIdentity, h]

theorem accepted_observation_step_is_accepted
    {state next : State} {event : Event}
    (stepped : ObservationStep state event = some next) :
    accepted (routeFor state event) = true := by
  unfold ObservationStep at stepped
  split at stepped
  · assumption
  · simp at stepped

theorem accepted_observation_step_applies_event
    {state next : State} {event : Event}
    (stepped : ObservationStep state event = some next) :
    next = (applyEvent state event).1 := by
  unfold ObservationStep at stepped
  split at stepped
  · exact Option.some.inj stepped |>.symm
  · simp at stepped

theorem accepted_observation_step_preserves_exact_identity
    {state next : State} {event : Event}
    (stepped : ObservationStep state event = some next) :
    observationIdentity next = observationIdentity state := by
  rw [accepted_observation_step_applies_event stepped]
  exact apply_event_preserves_exact_observation_identity state event

theorem accepted_observation_step_adds_one_receipt
    {state next : State} {event : Event}
    (stepped : ObservationStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  have acceptedStep := accepted_observation_step_is_accepted stepped
  rw [accepted_observation_step_applies_event stepped]
  simp [applyEvent, acceptedStep]

theorem rejected_observation_step_preserves_exact_state
    (state : State) (event : Event)
    (rejected : ObservationStep state event = none) :
    ProcessObservationEvent state event = (state, false) := by
  simp [ProcessObservationEvent, rejected]

theorem successful_observation_run_preserves_exact_identity
    {state final : State} {events : List Event}
    (ran : ObservationRun state events = some final) :
    observationIdentity final = observationIdentity state := by
  induction events generalizing state with
  | nil =>
      simp [ObservationRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : ObservationStep state event with
      | none => simp [ObservationRun, stepped] at ran
      | some next =>
          have tailRan : ObservationRun next tail = some final := by
            simpa [ObservationRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_observation_step_preserves_exact_identity stepped)

theorem successful_observation_run_preserves_non_authority
    {state final : State} {events : List Event}
    (ran : ObservationRun state events = some final) :
    final.supportAssignmentCount = state.supportAssignmentCount ∧
      final.externalAuthorityCount = state.externalAuthorityCount := by
  induction events generalizing state with
  | nil =>
      simp [ObservationRun] at ran
      subst final
      exact ⟨rfl, rfl⟩
  | cons event tail ih =>
      cases stepped : ObservationStep state event with
      | none => simp [ObservationRun, stepped] at ran
      | some next =>
          have tailRan : ObservationRun next tail = some final := by
            simpa [ObservationRun, stepped] using ran
          have rest := ih tailRan
          have applies := accepted_observation_step_applies_event stepped
          have head := apply_event_cannot_assign_support_or_external_authority state event
          rw [← applies] at head
          exact ⟨rest.1.trans head.1, rest.2.trans head.2⟩

theorem successful_observation_run_accounts_receipts
    {state final : State} {events : List Event}
    (ran : ObservationRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil =>
      simp [ObservationRun] at ran
      subst final
      simp
  | cons event tail ih =>
      cases stepped : ObservationStep state event with
      | none => simp [ObservationRun, stepped] at ran
      | some next =>
          have tailRan : ObservationRun next tail = some final := by
            simpa [ObservationRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [accepted_observation_step_adds_one_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp [Nat.add_comm, Nat.add_left_comm]

theorem successful_observation_run_has_valid_trace
    {state final : State} {events : List Event}
    (ran : ObservationRun state events = some final) :
    ObservationTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : ObservationStep state event with
      | none => simp [ObservationRun, stepped] at ran
      | some next =>
          have tailRan : ObservationRun next tail = some final := by
            simpa [ObservationRun, stepped] using ran
          have applies := accepted_observation_step_applies_event stepped
          exact ⟨accepted_observation_step_is_accepted stepped, by
            simpa [applies] using ih tailRan⟩

theorem observation_runs_compose
    {state middle final : State} {front back : List Event}
    (first : ObservationRun state front = some middle)
    (second : ObservationRun middle back = some final) :
    ObservationRun state (front ++ back) = some final := by
  induction front generalizing state middle with
  | nil =>
      simp [ObservationRun] at first
      subst middle
      exact second
  | cons event tail ih =>
      cases stepped : ObservationStep state event with
      | none => simp [ObservationRun, stepped] at first
      | some next =>
          have tailFirst : ObservationRun next tail = some middle := by
            simpa [ObservationRun, stepped] using first
          simpa [ObservationRun, stepped] using ih tailFirst second

theorem invalidated_observation_state_rejects_every_event
    (state : State) (event : Event) (invalidated : state.stage = .invalidated) :
    accepted (routeFor state event) = false := by
  simp [routeFor, invalidated, accepted]

theorem invalidated_observation_state_has_no_nonempty_run
    (state : State) (event : Event) (tail : List Event)
    (invalidated : state.stage = .invalidated) :
    ObservationRun state (event :: tail) = none := by
  have rejected := invalidated_observation_state_rejects_every_event
    state event invalidated
  simp [ObservationRun, ObservationStep, rejected]

structure GlobalDependenceCase where
  leftRoot : Nat
  rightRoot : Nat
  commonCausePresent : Bool
deriving DecidableEq, Repr

def pairRootSummary (case : GlobalDependenceCase) : Nat × Nat :=
  (case.leftRoot, case.rightRoot)

def globalIndependenceAdmitted (case : GlobalDependenceCase) : Bool :=
  !(case.leftRoot == case.rightRoot) && !case.commonCausePresent

def distinctRootsNoCommonCause : GlobalDependenceCase :=
  { leftRoot := 7, rightRoot := 9, commonCausePresent := false }

def distinctRootsSharedCommonCause : GlobalDependenceCase :=
  { leftRoot := 7, rightRoot := 9, commonCausePresent := true }

theorem pairwise_root_summary_collides_across_global_common_cause :
    pairRootSummary distinctRootsNoCommonCause =
        pairRootSummary distinctRootsSharedCommonCause ∧
      distinctRootsNoCommonCause ≠ distinctRootsSharedCommonCause := by
  decide

theorem exact_common_cause_state_separates_pairwise_root_collision :
    globalIndependenceAdmitted distinctRootsNoCommonCause = true ∧
      globalIndependenceAdmitted distinctRootsSharedCommonCause = false := by
  decide

theorem no_exact_global_independence_classifier_from_pairwise_roots_only :
    ¬ ∃ classify : (Nat × Nat) → Bool,
      ∀ case : GlobalDependenceCase,
        classify (pairRootSummary case) = globalIndependenceAdmitted case := by
  intro ⟨classify, exact⟩
  have clear := exact distinctRootsNoCommonCause
  have shared := exact distinctRootsSharedCommonCause
  have collision := pairwise_root_summary_collides_across_global_common_cause
  have separated := exact_common_cause_state_separates_pairwise_root_collision
  rw [separated.1] at clear
  rw [separated.2] at shared
  rw [collision.1] at clear
  simp_all

def canonicalPacket : Packet :=
  { observationDigest := 801, channelSetDigest := 802,
    calibrationDigest := 803, clockPoseDigest := 804,
    dependenceDigest := 805, hypothesisDigest := 806,
    consumerDigest := 807, residualDigest := 808, protocolVersion := 1,
    eventDigest := 1, pairDisposition := .correlatedAgreement,
    computedIndependentCount := 1, requestedIndependentCount := 1,
    sensorIdentityPresent := true, calibrationPresent := true,
    clockPosePresent := true, lineagePresent := true, fresh := true,
    dependenceRootsDeclared := true, commonCauseReviewed := true,
    pairClassificationPresent := true, evidenceCountMatchesClassification := true,
    disagreementPreserved := true, authorityBounded := true,
    expiryPresent := true, fallbackPresent := true, residualOwnerPresent := true,
    consumerPresent := true, maximumInferencePresent := true,
    independentReview := true, materialChangeRecorded := true,
    descendantsInvalidated := true, ordinaryRouteBlocked := true,
    rereviewRoutePresent := true, environmentalTruthAsserted := false,
    independenceBeyondModelAsserted := false, supportAssignmentRequested := false,
    externalAuthorityRequested := false }

def canonicalState (stage : Stage) : State :=
  { stage := stage, observationDigest := 801, channelSetDigest := 802,
    calibrationDigest := 803, clockPoseDigest := 804,
    dependenceDigest := 805, hypothesisDigest := 806,
    consumerDigest := 807, residualDigest := 808, protocolVersion := 1,
    pairDisposition := .correlatedAgreement, computedIndependentCount := 1,
    requestedIndependentCount := 1, lastEventDigest := 0, receiptCount := 0,
    handoffCount := 0, invalidationCount := 0, supportAssignmentCount := 0,
    externalAuthorityCount := 0 }

def eventFor (kind : EventKind) (digest : Nat) : Event :=
  { kind := kind, packet := { canonicalPacket with eventDigest := digest } }

theorem inflated_correlated_evidence_is_rejected :
    let state := { canonicalState .dependenceBound with
      computedIndependentCount := 2 }
    routeFor state
      { kind := .reviewPair,
        packet := { canonicalPacket with computedIndependentCount := 2 } } =
      .rejectCorrelatedInflation := by
  rfl

theorem correlated_pair_cannot_satisfy_two_item_use_request :
    let state := { canonicalState .pairReviewed with
      requestedIndependentCount := 2 }
    routeFor state
      { kind := .bindUse,
        packet := { canonicalPacket with requestedIndependentCount := 2 } } =
      .rejectCorrelatedInflation := by
  rfl

theorem erased_disagreement_blocks_pair_review :
    let state := { canonicalState .dependenceBound with
      pairDisposition := .disagreement, computedIndependentCount := 0 }
    routeFor state
      { kind := .reviewPair,
        packet := { canonicalPacket with
          pairDisposition := PairDisposition.disagreement
          computedIndependentCount := 0
          disagreementPreserved := false } } =
      .requestDisagreementPreservation := by
  rfl

theorem environmental_truth_overclaim_is_rejected :
    routeFor (canonicalState .useBound)
      { kind := .handoffObservation,
        packet := { canonicalPacket with environmentalTruthAsserted := true } } =
      .rejectTruthOverclaim := by
  rfl

theorem stale_descendants_block_invalidation :
    routeFor (canonicalState .handedOff)
      { kind := .invalidateForChange,
        packet := { canonicalPacket with descendantsInvalidated := false } } =
      .requestDescendantInvalidation := by
  rfl

theorem full_observation_lifecycle_reaches_invalidated_state :
    let s0 := canonicalState .captured
    let s1 := (applyEvent s0 (eventFor .bindIdentities 1)).1
    let s2 := (applyEvent s1 (eventFor .bindDependence 2)).1
    let s3 := (applyEvent s2 (eventFor .reviewPair 3)).1
    let s4 := (applyEvent s3 (eventFor .bindUse 4)).1
    let s5 := (applyEvent s4 (eventFor .handoffObservation 5)).1
    let s6 := (applyEvent s5 (eventFor .invalidateForChange 6)).1
    s6.stage = .invalidated ∧ s6.receiptCount = 6 ∧
      s6.handoffCount = 1 ∧ s6.invalidationCount = 1 ∧
      s6.supportAssignmentCount = 0 ∧ s6.externalAuthorityCount = 0 := by
  native_decide

end AsiStackProofs.ObservationTrust
