namespace AsiStackProofs.WhiteBoxEvidence

/-!
A finite admission and governance-routing model for model-internal evidence.
The Boolean fields are declared records, not scientific truth. The model can
constrain how a packet is consumed; it cannot establish that a feature, label,
circuit, intervention, evaluator, or coverage estimate is faithful.
-/

inductive InternalEvidenceState where
  | observational
  | predictive
  | causalBounded
  | unsupported
deriving DecidableEq, Repr

inductive RequestedAuthority where
  | preserve
  | restrict
  | widen
deriving DecidableEq, Repr

inductive GovernanceRoute where
  | reject
  | expire
  | preserve
  | restrict
  | escalate
  | grantWidening
deriving DecidableEq, Repr

structure InternalEvidencePacket where
  exactIdentity : Bool
  lineageFresh : Bool
  methodAssumptionsPresent : Bool
  negativeControlsPassed : Bool
  behavioralCrossCheck : Bool
  causalInterventionPassed : Bool
  separateEvaluator : Bool
  stabilityRecorded : Bool
  coverageResidualRecorded : Bool
  sideEffectsResolved : Bool
  materialChangeObserved : Bool
  releaseRequested : Bool
  evidenceState : InternalEvidenceState
  requestedAuthority : RequestedAuthority
deriving DecidableEq, Repr

def ScientificallyAdmissible (packet : InternalEvidencePacket) : Bool :=
  packet.exactIdentity &&
  packet.lineageFresh &&
  packet.methodAssumptionsPresent &&
  packet.negativeControlsPassed &&
  packet.stabilityRecorded &&
  packet.coverageResidualRecorded &&
  match packet.evidenceState with
  | .observational => true
  | .predictive => packet.behavioralCrossCheck
  | .causalBounded =>
      packet.behavioralCrossCheck &&
      packet.causalInterventionPassed &&
      packet.separateEvaluator
  | .unsupported => false

def WhiteBoxRouteFor (packet : InternalEvidencePacket) : GovernanceRoute :=
  if ScientificallyAdmissible packet = false then
    .reject
  else if packet.materialChangeObserved = true then
    .expire
  else if packet.requestedAuthority = .widen ∨ packet.releaseRequested = true then
    .escalate
  else if packet.sideEffectsResolved = false then
    .restrict
  else
    match packet.requestedAuthority with
    | .preserve => .preserve
    | .restrict => .restrict
    | .widen => .escalate

theorem evidence_never_grants_authority
    (packet : InternalEvidencePacket) :
    WhiteBoxRouteFor packet ≠ GovernanceRoute.grantWidening := by
  unfold WhiteBoxRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  cases packet.requestedAuthority <;> simp

theorem invalid_packet_rejected
    (packet : InternalEvidencePacket)
    (invalid :
      packet.exactIdentity = false ∨
      packet.lineageFresh = false ∨
      packet.methodAssumptionsPresent = false ∨
      packet.negativeControlsPassed = false ∨
      packet.stabilityRecorded = false ∨
      packet.coverageResidualRecorded = false ∨
      packet.evidenceState = .unsupported) :
    WhiteBoxRouteFor packet = .reject := by
  unfold WhiteBoxRouteFor
  have inadmissible : ScientificallyAdmissible packet = false := by
    rcases invalid with exactIdentity | lineage | assumptions | controls |
      stability | residual | unsupported
    · simp [ScientificallyAdmissible, exactIdentity]
    · simp [ScientificallyAdmissible, lineage]
    · simp [ScientificallyAdmissible, assumptions]
    · simp [ScientificallyAdmissible, controls]
    · simp [ScientificallyAdmissible, stability]
    · simp [ScientificallyAdmissible, residual]
    · simp [ScientificallyAdmissible, unsupported]
  simp [inadmissible]

theorem admitted_causal_packet_records_crosscheck_intervention_and_evaluator
    (packet : InternalEvidencePacket)
    (causal : packet.evidenceState = .causalBounded)
    (admitted : ScientificallyAdmissible packet = true) :
    packet.behavioralCrossCheck = true ∧
      packet.causalInterventionPassed = true ∧
      packet.separateEvaluator = true := by
  simp [ScientificallyAdmissible, causal] at admitted
  exact ⟨admitted.2.1.1, admitted.2.1.2, admitted.2.2⟩

theorem material_change_expires_admissible_packet
    (packet : InternalEvidencePacket)
    (admitted : ScientificallyAdmissible packet = true)
    (changed : packet.materialChangeObserved = true) :
    WhiteBoxRouteFor packet = .expire := by
  simp [WhiteBoxRouteFor, admitted, changed]

def boundedCausalPacket : InternalEvidencePacket where
  exactIdentity := true
  lineageFresh := true
  methodAssumptionsPresent := true
  negativeControlsPassed := true
  behavioralCrossCheck := true
  causalInterventionPassed := true
  separateEvaluator := true
  stabilityRecorded := true
  coverageResidualRecorded := true
  sideEffectsResolved := true
  materialChangeObserved := false
  releaseRequested := false
  evidenceState := .causalBounded
  requestedAuthority := .preserve

def stalePacket : InternalEvidencePacket :=
  { boundedCausalPacket with lineageFresh := false }

def authorityWideningPacket : InternalEvidencePacket :=
  { boundedCausalPacket with requestedAuthority := .widen }

def changedPacket : InternalEvidencePacket :=
  { boundedCausalPacket with materialChangeObserved := true }

theorem bounded_causal_fixture_preserves_authority :
    WhiteBoxRouteFor boundedCausalPacket = .preserve := by native_decide

theorem stale_fixture_is_rejected :
    WhiteBoxRouteFor stalePacket = .reject := by native_decide

theorem widening_fixture_escalates_without_grant :
    WhiteBoxRouteFor authorityWideningPacket = .escalate := by native_decide

theorem changed_fixture_expires :
    WhiteBoxRouteFor changedPacket = .expire := by native_decide

inductive EvidenceGovernanceStage where
  | raw
  | identityBound
  | methodChecked
  | interventionChecked
  | independentlyReviewed
  | policyRouted
  | consumed
  | rejected
deriving DecidableEq, Repr

inductive EvidenceGovernanceEventKind where
  | bindIdentity
  | checkMethod
  | checkIntervention
  | reviewIndependently
  | routePolicy
  | consume
  | reject
deriving DecidableEq, Repr

structure EvidenceGovernanceState where
  packetId : Nat
  modelId : Nat
  checkpointDigest : Nat
  methodDigest : Nat
  populationId : Nat
  packetVersion : Nat
  packet : InternalEvidencePacket
  authorityCeiling : Nat
  activeAuthority : Nat
  route : GovernanceRoute
  identityReceipt : Bool
  methodReceipt : Bool
  interventionReceipt : Bool
  reviewReceipt : Bool
  policyReceipt : Bool
  rejectionReceipt : Bool
  residualCount : Nat
  supportAuthority : Bool
  externalEffectAuthority : Bool
  stage : EvidenceGovernanceStage
  logicalTime : Nat
deriving DecidableEq, Repr

structure EvidenceGovernanceEvent where
  kind : EvidenceGovernanceEventKind
  fromStage : EvidenceGovernanceStage
  toStage : EvidenceGovernanceStage
  packetId : Nat
  modelId : Nat
  checkpointDigest : Nat
  methodDigest : Nat
  populationId : Nat
  packetVersion : Nat
  packet : InternalEvidencePacket
  requestedAuthority : Nat
  route : GovernanceRoute
  identityReceipt : Bool
  methodReceipt : Bool
  interventionReceipt : Bool
  reviewReceipt : Bool
  policyReceipt : Bool
  rejectionReceipt : Bool
  residualCount : Nat
  supportPromotionRequested : Bool
  externalEffectRequested : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def GovernanceIdentityMatches
    (state : EvidenceGovernanceState) (event : EvidenceGovernanceEvent) : Bool :=
  state.packetId = event.packetId &&
  state.modelId = event.modelId &&
  state.checkpointDigest = event.checkpointDigest &&
  state.methodDigest = event.methodDigest &&
  state.populationId = event.populationId &&
  state.packetVersion = event.packetVersion &&
  state.packet = event.packet

def EvidenceGovernanceEventSpecificValid
    (state : EvidenceGovernanceState) (event : EvidenceGovernanceEvent) : Bool :=
  match event.kind with
  | .bindIdentity =>
      event.fromStage = .raw && event.toStage = .identityBound &&
      0 < event.packetId && 0 < event.modelId && 0 < event.checkpointDigest &&
      0 < event.methodDigest && 0 < event.populationId &&
      event.packet.exactIdentity && event.identityReceipt &&
      event.requestedAuthority ≤ state.activeAuthority &&
      event.residualCount = state.residualCount
  | .checkMethod =>
      event.fromStage = .identityBound && event.toStage = .methodChecked &&
      event.packet.lineageFresh && event.packet.methodAssumptionsPresent &&
      event.packet.negativeControlsPassed && event.methodReceipt &&
      event.requestedAuthority = state.activeAuthority &&
      event.residualCount = state.residualCount
  | .checkIntervention =>
      event.fromStage = .methodChecked && event.toStage = .interventionChecked &&
      event.packet.evidenceState = .causalBounded &&
      event.packet.behavioralCrossCheck && event.packet.causalInterventionPassed &&
      event.interventionReceipt &&
      event.requestedAuthority = state.activeAuthority &&
      event.residualCount = state.residualCount
  | .reviewIndependently =>
      event.fromStage = .interventionChecked &&
      event.toStage = .independentlyReviewed &&
      event.packet.separateEvaluator && event.reviewReceipt &&
      event.requestedAuthority = state.activeAuthority &&
      event.residualCount = state.residualCount
  | .routePolicy =>
      event.fromStage = .independentlyReviewed && event.toStage = .policyRouted &&
      ScientificallyAdmissible event.packet &&
      event.route = WhiteBoxRouteFor event.packet &&
      event.route != .grantWidening && event.policyReceipt &&
      event.requestedAuthority ≤ state.activeAuthority &&
      event.residualCount = state.residualCount
  | .consume =>
      event.fromStage = .policyRouted && event.toStage = .consumed &&
      (state.route = .preserve || state.route = .restrict) &&
      state.identityReceipt && state.methodReceipt && state.interventionReceipt &&
      state.reviewReceipt && state.policyReceipt &&
      event.requestedAuthority = state.activeAuthority &&
      event.residualCount = 0
  | .reject =>
      event.fromStage != .consumed && event.fromStage != .rejected &&
      event.toStage = .rejected &&
      (event.route = .reject || event.route = .expire) &&
      event.rejectionReceipt &&
      event.requestedAuthority ≤ state.activeAuthority &&
      event.residualCount = state.residualCount

def EvidenceGovernanceEventValid
    (state : EvidenceGovernanceState) (event : EvidenceGovernanceEvent) : Prop :=
  state.stage = event.fromStage ∧
  GovernanceIdentityMatches state event = true ∧
  state.logicalTime < event.logicalTime ∧
  event.supportPromotionRequested = false ∧
  event.externalEffectRequested = false ∧
  EvidenceGovernanceEventSpecificValid state event = true

instance evidenceGovernanceEventValidDecidable
    (state : EvidenceGovernanceState) (event : EvidenceGovernanceEvent) :
    Decidable (EvidenceGovernanceEventValid state event) := by
  unfold EvidenceGovernanceEventValid
  infer_instance

def ApplyEvidenceGovernanceEvent
    (state : EvidenceGovernanceState)
    (event : EvidenceGovernanceEvent) : EvidenceGovernanceState :=
  { state with
    activeAuthority :=
      if event.kind = .routePolicy then
        Nat.min state.activeAuthority event.requestedAuthority
      else state.activeAuthority
    route :=
      if event.kind = .routePolicy || event.kind = .reject then event.route
      else state.route
    identityReceipt := state.identityReceipt || event.identityReceipt
    methodReceipt := state.methodReceipt || event.methodReceipt
    interventionReceipt := state.interventionReceipt || event.interventionReceipt
    reviewReceipt := state.reviewReceipt || event.reviewReceipt
    policyReceipt := state.policyReceipt || event.policyReceipt
    rejectionReceipt := state.rejectionReceipt || event.rejectionReceipt
    residualCount := event.residualCount
    stage := event.toStage
    logicalTime := event.logicalTime }

def EvidenceGovernanceStep
    (state : EvidenceGovernanceState)
    (event : EvidenceGovernanceEvent) : Option EvidenceGovernanceState :=
  if EvidenceGovernanceEventValid state event then
    some (ApplyEvidenceGovernanceEvent state event)
  else none

def EvidenceGovernanceRun :
    EvidenceGovernanceState -> List EvidenceGovernanceEvent ->
      Option EvidenceGovernanceState
  | state, [] => some state
  | state, event :: tail =>
      match EvidenceGovernanceStep state event with
      | none => none
      | some next => EvidenceGovernanceRun next tail

def EvidenceGovernanceIdentity
    (state : EvidenceGovernanceState) :
    Nat × Nat × Nat × Nat × Nat × Nat × InternalEvidencePacket :=
  (state.packetId, state.modelId, state.checkpointDigest, state.methodDigest,
    state.populationId, state.packetVersion, state.packet)

def EvidenceGovernanceTraceValid :
    EvidenceGovernanceState -> List EvidenceGovernanceEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      EvidenceGovernanceEventValid state event ∧
      EvidenceGovernanceTraceValid (ApplyEvidenceGovernanceEvent state event) tail

theorem governance_step_is_valid
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (accepted : EvidenceGovernanceStep state event = some next) :
    EvidenceGovernanceEventValid state event := by
  unfold EvidenceGovernanceStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem governance_step_applies_event
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (accepted : EvidenceGovernanceStep state event = some next) :
    next = ApplyEvidenceGovernanceEvent state event := by
  unfold EvidenceGovernanceStep at accepted
  split at accepted
  · exact Option.some.inj accepted |>.symm
  · simp at accepted

theorem accepted_governance_step_cannot_request_support
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (accepted : EvidenceGovernanceStep state event = some next) :
    event.supportPromotionRequested = false := by
  exact (governance_step_is_valid accepted).2.2.2.1

theorem accepted_governance_step_cannot_request_external_effect
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (accepted : EvidenceGovernanceStep state event = some next) :
    event.externalEffectRequested = false := by
  exact (governance_step_is_valid accepted).2.2.2.2.1

theorem apply_governance_event_preserves_identity
    (state : EvidenceGovernanceState) (event : EvidenceGovernanceEvent) :
    EvidenceGovernanceIdentity (ApplyEvidenceGovernanceEvent state event) =
      EvidenceGovernanceIdentity state := by
  rfl

theorem accepted_governance_step_preserves_identity
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (accepted : EvidenceGovernanceStep state event = some next) :
    EvidenceGovernanceIdentity next = EvidenceGovernanceIdentity state := by
  rw [governance_step_applies_event accepted]
  exact apply_governance_event_preserves_identity state event

theorem accepted_governance_step_authority_nonincreasing
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (accepted : EvidenceGovernanceStep state event = some next) :
    next.activeAuthority ≤ state.activeAuthority := by
  rw [governance_step_applies_event accepted]
  unfold ApplyEvidenceGovernanceEvent
  split
  · exact Nat.min_le_left _ _
  · exact Nat.le_refl _

theorem accepted_governance_step_preserves_support_authority
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (accepted : EvidenceGovernanceStep state event = some next) :
    next.supportAuthority = state.supportAuthority := by
  rw [governance_step_applies_event accepted]
  rfl

theorem accepted_governance_step_preserves_external_effect_authority
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (accepted : EvidenceGovernanceStep state event = some next) :
    next.externalEffectAuthority = state.externalEffectAuthority := by
  rw [governance_step_applies_event accepted]
  rfl

theorem successful_governance_run_preserves_identity
    {state final : EvidenceGovernanceState} {events : List EvidenceGovernanceEvent}
    (ran : EvidenceGovernanceRun state events = some final) :
    EvidenceGovernanceIdentity final = EvidenceGovernanceIdentity state := by
  induction events generalizing state with
  | nil =>
      simp [EvidenceGovernanceRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : EvidenceGovernanceStep state event with
      | none => simp [EvidenceGovernanceRun, stepped] at ran
      | some next =>
          have tailRan : EvidenceGovernanceRun next tail = some final := by
            simpa [EvidenceGovernanceRun, stepped] using ran
          calc
            EvidenceGovernanceIdentity final = EvidenceGovernanceIdentity next := ih tailRan
            _ = EvidenceGovernanceIdentity state :=
              accepted_governance_step_preserves_identity stepped

theorem successful_governance_run_authority_nonincreasing
    {state final : EvidenceGovernanceState} {events : List EvidenceGovernanceEvent}
    (ran : EvidenceGovernanceRun state events = some final) :
    final.activeAuthority ≤ state.activeAuthority := by
  induction events generalizing state with
  | nil =>
      simp [EvidenceGovernanceRun] at ran
      subst final
      exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : EvidenceGovernanceStep state event with
      | none => simp [EvidenceGovernanceRun, stepped] at ran
      | some next =>
          have tailRan : EvidenceGovernanceRun next tail = some final := by
            simpa [EvidenceGovernanceRun, stepped] using ran
          exact Nat.le_trans (ih tailRan)
            (accepted_governance_step_authority_nonincreasing stepped)

theorem successful_governance_run_preserves_support_authority
    {state final : EvidenceGovernanceState} {events : List EvidenceGovernanceEvent}
    (ran : EvidenceGovernanceRun state events = some final) :
    final.supportAuthority = state.supportAuthority := by
  induction events generalizing state with
  | nil => simp [EvidenceGovernanceRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : EvidenceGovernanceStep state event with
      | none => simp [EvidenceGovernanceRun, stepped] at ran
      | some next =>
          have tailRan : EvidenceGovernanceRun next tail = some final := by
            simpa [EvidenceGovernanceRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_governance_step_preserves_support_authority stepped)

theorem successful_governance_run_preserves_external_effect_authority
    {state final : EvidenceGovernanceState} {events : List EvidenceGovernanceEvent}
    (ran : EvidenceGovernanceRun state events = some final) :
    final.externalEffectAuthority = state.externalEffectAuthority := by
  induction events generalizing state with
  | nil => simp [EvidenceGovernanceRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : EvidenceGovernanceStep state event with
      | none => simp [EvidenceGovernanceRun, stepped] at ran
      | some next =>
          have tailRan : EvidenceGovernanceRun next tail = some final := by
            simpa [EvidenceGovernanceRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_governance_step_preserves_external_effect_authority stepped)

theorem successful_governance_run_has_valid_trace
    {state final : EvidenceGovernanceState} {events : List EvidenceGovernanceEvent}
    (ran : EvidenceGovernanceRun state events = some final) :
    EvidenceGovernanceTraceValid state events := by
  induction events generalizing state with
  | nil => simp [EvidenceGovernanceTraceValid]
  | cons event tail ih =>
      cases stepped : EvidenceGovernanceStep state event with
      | none => simp [EvidenceGovernanceRun, stepped] at ran
      | some next =>
          have tailRan : EvidenceGovernanceRun next tail = some final := by
            simpa [EvidenceGovernanceRun, stepped] using ran
          have applies := governance_step_applies_event stepped
          subst next
          exact ⟨governance_step_is_valid stepped, ih tailRan⟩

theorem governance_run_append
    (state middle : EvidenceGovernanceState)
    (left right : List EvidenceGovernanceEvent)
    (leftRan : EvidenceGovernanceRun state left = some middle) :
    EvidenceGovernanceRun state (left ++ right) =
      EvidenceGovernanceRun middle right := by
  induction left generalizing state with
  | nil =>
      simp [EvidenceGovernanceRun] at leftRan
      subst middle
      rfl
  | cons event tail ih =>
      cases stepped : EvidenceGovernanceStep state event with
      | none => simp [EvidenceGovernanceRun, stepped] at leftRan
      | some next =>
          have tailRan : EvidenceGovernanceRun next tail = some middle := by
            simpa [EvidenceGovernanceRun, stepped] using leftRan
          simpa [EvidenceGovernanceRun, stepped] using ih next tailRan

theorem accepted_policy_route_requires_admissible_packet
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (kind : event.kind = .routePolicy)
    (accepted : EvidenceGovernanceStep state event = some next) :
    ScientificallyAdmissible state.packet = true := by
  rcases governance_step_is_valid accepted with ⟨_, identity, _, _, _, specific⟩
  have packetMatch : state.packet = event.packet := by
    simp [GovernanceIdentityMatches] at identity
    exact identity.2
  simp [EvidenceGovernanceEventSpecificValid, kind] at specific
  have admitted : ScientificallyAdmissible event.packet = true :=
    specific.1.1.1.1.1.2
  calc
    ScientificallyAdmissible state.packet =
        ScientificallyAdmissible event.packet := congrArg _ packetMatch
    _ = true := admitted

theorem accepted_policy_route_never_grants_widening
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (kind : event.kind = .routePolicy)
    (accepted : EvidenceGovernanceStep state event = some next) :
    event.route ≠ .grantWidening := by
  rcases governance_step_is_valid accepted with ⟨_, _, _, _, _, specific⟩
  simp [EvidenceGovernanceEventSpecificValid, kind] at specific
  exact specific.1.1.1.2

theorem accepted_policy_route_requires_fresh_lineage
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (kind : event.kind = .routePolicy)
    (accepted : EvidenceGovernanceStep state event = some next) :
    state.packet.lineageFresh = true := by
  have admitted := accepted_policy_route_requires_admissible_packet kind accepted
  cases lineage : state.packet.lineageFresh
  · simp [ScientificallyAdmissible, lineage] at admitted
  · rfl

theorem accepted_policy_route_requires_method_assumptions
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (kind : event.kind = .routePolicy)
    (accepted : EvidenceGovernanceStep state event = some next) :
    state.packet.methodAssumptionsPresent = true := by
  have admitted := accepted_policy_route_requires_admissible_packet kind accepted
  cases assumptions : state.packet.methodAssumptionsPresent
  · simp [ScientificallyAdmissible, assumptions] at admitted
  · rfl

theorem accepted_policy_route_requires_negative_controls
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (kind : event.kind = .routePolicy)
    (accepted : EvidenceGovernanceStep state event = some next) :
    state.packet.negativeControlsPassed = true := by
  have admitted := accepted_policy_route_requires_admissible_packet kind accepted
  cases controls : state.packet.negativeControlsPassed
  · simp [ScientificallyAdmissible, controls] at admitted
  · rfl

theorem accepted_causal_policy_route_requires_crosscheck_intervention_and_reviewer
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (kind : event.kind = .routePolicy)
    (causal : state.packet.evidenceState = .causalBounded)
    (accepted : EvidenceGovernanceStep state event = some next) :
    state.packet.behavioralCrossCheck = true ∧
    state.packet.causalInterventionPassed = true ∧
    state.packet.separateEvaluator = true := by
  exact admitted_causal_packet_records_crosscheck_intervention_and_evaluator
    state.packet causal
    (accepted_policy_route_requires_admissible_packet kind accepted)

theorem accepted_consumption_requires_complete_receipts
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (kind : event.kind = .consume)
    (accepted : EvidenceGovernanceStep state event = some next) :
    state.identityReceipt = true ∧ state.methodReceipt = true ∧
    state.interventionReceipt = true ∧ state.reviewReceipt = true ∧
    state.policyReceipt = true := by
  rcases governance_step_is_valid accepted with ⟨_, _, _, _, _, specific⟩
  simp [EvidenceGovernanceEventSpecificValid, kind] at specific
  exact ⟨specific.1.1.1.1.1.1.2, specific.1.1.1.1.1.2,
    specific.1.1.1.1.2, specific.1.1.1.2, specific.1.1.2⟩

theorem accepted_consumption_requires_zero_residual
    {state next : EvidenceGovernanceState} {event : EvidenceGovernanceEvent}
    (kind : event.kind = .consume)
    (accepted : EvidenceGovernanceStep state event = some next) :
    next.residualCount = 0 := by
  rw [governance_step_applies_event accepted]
  rcases governance_step_is_valid accepted with ⟨_, _, _, _, _, specific⟩
  simp [EvidenceGovernanceEventSpecificValid, kind] at specific
  have zero : event.residualCount = 0 := specific.2
  change event.residualCount = 0
  exact zero

def governanceInitialState : EvidenceGovernanceState where
  packetId := 11
  modelId := 22
  checkpointDigest := 33
  methodDigest := 44
  populationId := 55
  packetVersion := 1
  packet := boundedCausalPacket
  authorityCeiling := 5
  activeAuthority := 3
  route := .reject
  identityReceipt := false
  methodReceipt := false
  interventionReceipt := false
  reviewReceipt := false
  policyReceipt := false
  rejectionReceipt := false
  residualCount := 0
  supportAuthority := false
  externalEffectAuthority := false
  stage := .raw
  logicalTime := 0

def governanceBaseEvent : EvidenceGovernanceEvent where
  kind := .bindIdentity
  fromStage := .raw
  toStage := .identityBound
  packetId := 11
  modelId := 22
  checkpointDigest := 33
  methodDigest := 44
  populationId := 55
  packetVersion := 1
  packet := boundedCausalPacket
  requestedAuthority := 3
  route := .preserve
  identityReceipt := false
  methodReceipt := false
  interventionReceipt := false
  reviewReceipt := false
  policyReceipt := false
  rejectionReceipt := false
  residualCount := 0
  supportPromotionRequested := false
  externalEffectRequested := false
  logicalTime := 1

def governanceReferenceEvents : List EvidenceGovernanceEvent :=
  [ { governanceBaseEvent with identityReceipt := true },
    { governanceBaseEvent with
      kind := .checkMethod
      fromStage := .identityBound
      toStage := .methodChecked
      methodReceipt := true
      logicalTime := 2 },
    { governanceBaseEvent with
      kind := .checkIntervention
      fromStage := .methodChecked
      toStage := .interventionChecked
      interventionReceipt := true
      logicalTime := 3 },
    { governanceBaseEvent with
      kind := .reviewIndependently
      fromStage := .interventionChecked
      toStage := .independentlyReviewed
      reviewReceipt := true
      logicalTime := 4 },
    { governanceBaseEvent with
      kind := .routePolicy
      fromStage := .independentlyReviewed
      toStage := .policyRouted
      policyReceipt := true
      logicalTime := 5 },
    { governanceBaseEvent with
      kind := .consume
      fromStage := .policyRouted
      toStage := .consumed
      logicalTime := 6 } ]

def governanceConsumedState : EvidenceGovernanceState where
  packetId := 11
  modelId := 22
  checkpointDigest := 33
  methodDigest := 44
  populationId := 55
  packetVersion := 1
  packet := boundedCausalPacket
  authorityCeiling := 5
  activeAuthority := 3
  route := .preserve
  identityReceipt := true
  methodReceipt := true
  interventionReceipt := true
  reviewReceipt := true
  policyReceipt := true
  rejectionReceipt := false
  residualCount := 0
  supportAuthority := false
  externalEffectAuthority := false
  stage := .consumed
  logicalTime := 6

theorem governance_reference_trace_reaches_consumed :
    EvidenceGovernanceRun governanceInitialState governanceReferenceEvents =
      some governanceConsumedState := by native_decide

theorem stale_governance_state_cannot_route
    (event : EvidenceGovernanceEvent)
    (kind : event.kind = .routePolicy) :
    EvidenceGovernanceStep
      { governanceInitialState with
        stage := .independentlyReviewed
        packet := stalePacket
        logicalTime := 4 }
      event = none := by
  let state := { governanceInitialState with
    stage := .independentlyReviewed
    packet := stalePacket
    logicalTime := 4 }
  cases stepped : EvidenceGovernanceStep state event with
  | none => rfl
  | some next =>
      have admitted := accepted_policy_route_requires_admissible_packet kind stepped
      simp [state, stalePacket, boundedCausalPacket, ScientificallyAdmissible] at admitted

theorem missing_assumptions_governance_state_cannot_route
    (event : EvidenceGovernanceEvent)
    (kind : event.kind = .routePolicy) :
    EvidenceGovernanceStep
      { governanceInitialState with
        stage := .independentlyReviewed
        packet := { boundedCausalPacket with methodAssumptionsPresent := false }
        logicalTime := 4 }
      event = none := by
  let state := { governanceInitialState with
    stage := .independentlyReviewed
    packet := { boundedCausalPacket with methodAssumptionsPresent := false }
    logicalTime := 4 }
  cases stepped : EvidenceGovernanceStep state event with
  | none => rfl
  | some next =>
      have admitted := accepted_policy_route_requires_admissible_packet kind stepped
      simp [state, boundedCausalPacket, ScientificallyAdmissible] at admitted

theorem missing_negative_controls_governance_state_cannot_route
    (event : EvidenceGovernanceEvent)
    (kind : event.kind = .routePolicy) :
    EvidenceGovernanceStep
      { governanceInitialState with
        stage := .independentlyReviewed
        packet := { boundedCausalPacket with negativeControlsPassed := false }
        logicalTime := 4 }
      event = none := by
  let state := { governanceInitialState with
    stage := .independentlyReviewed
    packet := { boundedCausalPacket with negativeControlsPassed := false }
    logicalTime := 4 }
  cases stepped : EvidenceGovernanceStep state event with
  | none => rfl
  | some next =>
      have admitted := accepted_policy_route_requires_admissible_packet kind stepped
      simp [state, boundedCausalPacket, ScientificallyAdmissible] at admitted

theorem unsupported_governance_state_cannot_route
    (event : EvidenceGovernanceEvent)
    (kind : event.kind = .routePolicy) :
    EvidenceGovernanceStep
      { governanceInitialState with
        stage := .independentlyReviewed
        packet := { boundedCausalPacket with evidenceState := .unsupported }
        logicalTime := 4 }
      event = none := by
  let state := { governanceInitialState with
    stage := .independentlyReviewed
    packet := { boundedCausalPacket with evidenceState := .unsupported }
    logicalTime := 4 }
  cases stepped : EvidenceGovernanceStep state event with
  | none => rfl
  | some next =>
      have admitted := accepted_policy_route_requires_admissible_packet kind stepped
      simp [state, boundedCausalPacket, ScientificallyAdmissible] at admitted

end AsiStackProofs.WhiteBoxEvidence
