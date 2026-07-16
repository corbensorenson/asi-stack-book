namespace AsiStackProofs.ReadinessRefinement

inductive Stage where
  | candidate | shadow | canary | qualified | defaultReady | quarantined | terminal
deriving DecidableEq, Repr

inductive EventKind where
  | admitShadow | admitCanary | qualify | admitDefault | quarantine | terminate
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectCapabilitySubstitution | rejectEvidenceSubstitution
  | rejectEventReplay | rejectAuthorityLeak
  | requestWorkload | requestBaseline | requestEvaluator | requestNonClaims
  | requestShadowEvidence | requestFreshGate | blockRegression | requestResidualEscrow
  | requestFallback | requestRollbackPlan | requestMonitoring
  | requestCanaryEvidence | requestUsefulThroughput | requestUnsafeReleaseRecord
  | requestLatencyCost | quarantineThresholdBreach
  | requestQualificationEvidence | requestIndependentEvaluation | requestTransfer
  | requestDelayedOutcomes
  | requestQuarantineTrigger | requestTransitivePropagation | requestOrdinaryRouteBlock
  | requestBoundedDiagnostics
  | requestTerminalReason | requestTerminalReceipt | requestDependencyClosure
  | requestRevocationClosure | requestConsumerAcknowledgment
  | acceptShadow | acceptCanary | acceptQualification | acceptDefault
  | acceptQuarantine | acceptTermination
deriving DecidableEq, Repr

structure Packet where
  capabilityId : Nat
  capabilityVersion : Nat
  implementationDigest : Nat
  modelStateDigest : Nat
  workloadDigest : Nat
  baselineDigest : Nat
  evaluatorDigest : Nat
  policyDigest : Nat
  authorityDigest : Nat
  consumerDigest : Nat
  fallbackDigest : Nat
  residualDigest : Nat
  eventDigest : Nat
  workloadPresent : Bool
  baselinePresent : Bool
  evaluatorPresent : Bool
  nonClaimsPresent : Bool
  shadowEvidencePresent : Bool
  gateEvidenceFresh : Bool
  regressionFloorPreserved : Bool
  residualEscrowPresent : Bool
  fallbackPresent : Bool
  rollbackPlanPresent : Bool
  monitoringPresent : Bool
  canaryEvidencePresent : Bool
  usefulThroughputRecorded : Bool
  unsafeReleaseRecorded : Bool
  latencyCostRecorded : Bool
  thresholdBreached : Bool
  qualificationEvidencePresent : Bool
  independentEvaluationPresent : Bool
  transferEvidencePresent : Bool
  delayedOutcomesPresent : Bool
  quarantineTriggerPresent : Bool
  transitivePropagationComplete : Bool
  ordinaryRouteBlocked : Bool
  boundedDiagnosticsPresent : Bool
  terminalReasonPresent : Bool
  terminalReceiptPresent : Bool
  dependencyClosureComplete : Bool
  revocationClosureComplete : Bool
  consumerAcknowledgmentPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  capabilityId : Nat
  capabilityVersion : Nat
  implementationDigest : Nat
  modelStateDigest : Nat
  workloadDigest : Nat
  baselineDigest : Nat
  evaluatorDigest : Nat
  policyDigest : Nat
  authorityDigest : Nat
  consumerDigest : Nat
  fallbackDigest : Nat
  residualDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  ordinaryReleaseCount : Nat
  quarantineCount : Nat
  terminalCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .candidate => .admitShadow | .shadow => .admitCanary | .canary => .qualify
  | .qualified => .admitDefault | .defaultReady => .quarantine
  | .quarantined => .terminate | .terminal => .terminate

def exactCapabilityBinding (state : State) (packet : Packet) : Bool :=
  packet.capabilityId == state.capabilityId &&
  packet.capabilityVersion == state.capabilityVersion &&
  packet.implementationDigest == state.implementationDigest &&
  packet.modelStateDigest == state.modelStateDigest &&
  packet.policyDigest == state.policyDigest && packet.authorityDigest == state.authorityDigest &&
  packet.consumerDigest == state.consumerDigest

def exactEvidenceBinding (state : State) (packet : Packet) : Bool :=
  packet.workloadDigest == state.workloadDigest && packet.baselineDigest == state.baselineDigest &&
  packet.evaluatorDigest == state.evaluatorDigest && packet.fallbackDigest == state.fallbackDigest &&
  packet.residualDigest == state.residualDigest

def routeFor (state : State) (event : Event) : Route :=
  if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactCapabilityBinding state event.packet then .rejectCapabilitySubstitution
  else if ! exactEvidenceBinding state event.packet then .rejectEvidenceSubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectEventReplay
  else if event.packet.supportAssignmentRequested || event.packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .candidate =>
      if ! event.packet.workloadPresent then .requestWorkload
      else if ! event.packet.baselinePresent then .requestBaseline
      else if ! event.packet.evaluatorPresent then .requestEvaluator
      else if ! event.packet.nonClaimsPresent then .requestNonClaims
      else .acceptShadow
  | .shadow =>
      if ! event.packet.shadowEvidencePresent then .requestShadowEvidence
      else if ! event.packet.gateEvidenceFresh then .requestFreshGate
      else if ! event.packet.regressionFloorPreserved then .blockRegression
      else if ! event.packet.residualEscrowPresent then .requestResidualEscrow
      else if ! event.packet.fallbackPresent then .requestFallback
      else if ! event.packet.rollbackPlanPresent then .requestRollbackPlan
      else if ! event.packet.monitoringPresent then .requestMonitoring
      else .acceptCanary
  | .canary =>
      if ! event.packet.canaryEvidencePresent then .requestCanaryEvidence
      else if ! event.packet.usefulThroughputRecorded then .requestUsefulThroughput
      else if ! event.packet.unsafeReleaseRecorded then .requestUnsafeReleaseRecord
      else if ! event.packet.latencyCostRecorded then .requestLatencyCost
      else if event.packet.thresholdBreached then .quarantineThresholdBreach
      else .acceptQualification
  | .qualified =>
      if ! event.packet.qualificationEvidencePresent then .requestQualificationEvidence
      else if ! event.packet.independentEvaluationPresent then .requestIndependentEvaluation
      else if ! event.packet.transferEvidencePresent then .requestTransfer
      else if ! event.packet.delayedOutcomesPresent then .requestDelayedOutcomes
      else .acceptDefault
  | .defaultReady =>
      if ! event.packet.quarantineTriggerPresent then .requestQuarantineTrigger
      else if ! event.packet.transitivePropagationComplete then .requestTransitivePropagation
      else if ! event.packet.ordinaryRouteBlocked then .requestOrdinaryRouteBlock
      else if ! event.packet.boundedDiagnosticsPresent then .requestBoundedDiagnostics
      else .acceptQuarantine
  | .quarantined =>
      if ! event.packet.terminalReasonPresent then .requestTerminalReason
      else if ! event.packet.terminalReceiptPresent then .requestTerminalReceipt
      else if ! event.packet.dependencyClosureComplete then .requestDependencyClosure
      else if ! event.packet.revocationClosureComplete then .requestRevocationClosure
      else if ! event.packet.consumerAcknowledgmentPresent then .requestConsumerAcknowledgment
      else .acceptTermination
  | .terminal => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptShadow | .acceptCanary | .acceptQualification | .acceptDefault
  | .acceptQuarantine | .acceptTermination => true
  | _ => false

def advance : Stage -> Stage
  | .candidate => .shadow | .shadow => .canary | .canary => .qualified
  | .qualified => .defaultReady | .defaultReady => .quarantined
  | .quarantined => .terminal | .terminal => .terminal

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advance state.stage
       lastEventDigest := event.packet.eventDigest
       receiptCount := state.receiptCount + 1
       ordinaryReleaseCount := if state.stage == .qualified then state.ordinaryReleaseCount + 1 else state.ordinaryReleaseCount
       quarantineCount := if state.stage == .defaultReady then state.quarantineCount + 1 else state.quarantineCount
       terminalCount := if state.stage == .quarantined then state.terminalCount + 1 else state.terminalCount }, route)
  else (state, route)

theorem apply_event_preserves_capability_and_evidence_identity (state : State) (event : Event) :
    (applyEvent state event).1.capabilityId = state.capabilityId ∧
    (applyEvent state event).1.implementationDigest = state.implementationDigest ∧
    (applyEvent state event).1.modelStateDigest = state.modelStateDigest ∧
    (applyEvent state event).1.workloadDigest = state.workloadDigest ∧
    (applyEvent state event).1.evaluatorDigest = state.evaluatorDigest ∧
    (applyEvent state event).1.residualDigest = state.residualDigest := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_effect (state : State) (event : Event) :
    (applyEvent state event).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state event).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem accepted_step_adds_exactly_one_receipt (state : State) (event : Event)
    (h : accepted (routeFor state event) = true) :
    (applyEvent state event).1.receiptCount = state.receiptCount + 1 := by simp [applyEvent, h]

def canonicalPacket : Packet :=
  { capabilityId := 901, capabilityVersion := 4, implementationDigest := 902,
    modelStateDigest := 903, workloadDigest := 904, baselineDigest := 905,
    evaluatorDigest := 906, policyDigest := 907, authorityDigest := 908,
    consumerDigest := 909, fallbackDigest := 910, residualDigest := 911, eventDigest := 1,
    workloadPresent := true, baselinePresent := true, evaluatorPresent := true,
    nonClaimsPresent := true, shadowEvidencePresent := true, gateEvidenceFresh := true,
    regressionFloorPreserved := true, residualEscrowPresent := true, fallbackPresent := true,
    rollbackPlanPresent := true, monitoringPresent := true, canaryEvidencePresent := true,
    usefulThroughputRecorded := true, unsafeReleaseRecorded := true, latencyCostRecorded := true,
    thresholdBreached := false, qualificationEvidencePresent := true,
    independentEvaluationPresent := true, transferEvidencePresent := true,
    delayedOutcomesPresent := true, quarantineTriggerPresent := true,
    transitivePropagationComplete := true, ordinaryRouteBlocked := true,
    boundedDiagnosticsPresent := true, terminalReasonPresent := true,
    terminalReceiptPresent := true, dependencyClosureComplete := true,
    revocationClosureComplete := true, consumerAcknowledgmentPresent := true,
    supportAssignmentRequested := false, externalEffectRequested := false }

def canonicalState (stage : Stage) : State :=
  { stage := stage, capabilityId := 901, capabilityVersion := 4, implementationDigest := 902,
    modelStateDigest := 903, workloadDigest := 904, baselineDigest := 905,
    evaluatorDigest := 906, policyDigest := 907, authorityDigest := 908,
    consumerDigest := 909, fallbackDigest := 910, residualDigest := 911,
    lastEventDigest := 0, receiptCount := 0, ordinaryReleaseCount := 0,
    quarantineCount := 0, terminalCount := 0, supportAssignmentCount := 0, externalEffectCount := 0 }

theorem incomplete_baseline_blocks_shadow :
    routeFor (canonicalState .candidate) { kind := .admitShadow, packet := { canonicalPacket with baselinePresent := false } } = .requestBaseline := by rfl
theorem stale_gate_blocks_canary :
    routeFor (canonicalState .shadow) { kind := .admitCanary, packet := { canonicalPacket with gateEvidenceFresh := false } } = .requestFreshGate := by rfl
theorem regression_blocks_canary :
    routeFor (canonicalState .shadow) { kind := .admitCanary, packet := { canonicalPacket with regressionFloorPreserved := false } } = .blockRegression := by rfl
theorem missing_residual_escrow_blocks_canary :
    routeFor (canonicalState .shadow) { kind := .admitCanary, packet := { canonicalPacket with residualEscrowPresent := false } } = .requestResidualEscrow := by rfl
theorem missing_fallback_blocks_canary :
    routeFor (canonicalState .shadow) { kind := .admitCanary, packet := { canonicalPacket with fallbackPresent := false } } = .requestFallback := by rfl
theorem threshold_breach_quarantines_qualification :
    routeFor (canonicalState .canary) { kind := .qualify, packet := { canonicalPacket with thresholdBreached := true } } = .quarantineThresholdBreach := by rfl
theorem missing_useful_throughput_blocks_qualification :
    routeFor (canonicalState .canary) { kind := .qualify, packet := { canonicalPacket with usefulThroughputRecorded := false } } = .requestUsefulThroughput := by rfl
theorem missing_independent_evaluation_blocks_default :
    routeFor (canonicalState .qualified) { kind := .admitDefault, packet := { canonicalPacket with independentEvaluationPresent := false } } = .requestIndependentEvaluation := by rfl
theorem missing_transfer_blocks_default :
    routeFor (canonicalState .qualified) { kind := .admitDefault, packet := { canonicalPacket with transferEvidencePresent := false } } = .requestTransfer := by rfl
theorem incomplete_quarantine_propagation_blocks_transition :
    routeFor (canonicalState .defaultReady) { kind := .quarantine, packet := { canonicalPacket with transitivePropagationComplete := false } } = .requestTransitivePropagation := by rfl
theorem ordinary_route_must_be_blocked_in_quarantine :
    routeFor (canonicalState .defaultReady) { kind := .quarantine, packet := { canonicalPacket with ordinaryRouteBlocked := false } } = .requestOrdinaryRouteBlock := by rfl
theorem missing_terminal_receipt_blocks_termination :
    routeFor (canonicalState .quarantined) { kind := .terminate, packet := { canonicalPacket with terminalReceiptPresent := false } } = .requestTerminalReceipt := by rfl
theorem incomplete_revocation_blocks_termination :
    routeFor (canonicalState .quarantined) { kind := .terminate, packet := { canonicalPacket with revocationClosureComplete := false } } = .requestRevocationClosure := by rfl

def eventFor (kind : EventKind) (digest : Nat) : Event :=
  { kind := kind, packet := { canonicalPacket with eventDigest := digest } }

theorem full_readiness_lifecycle_reaches_terminal_state :
    let s0 := canonicalState .candidate
    let s1 := (applyEvent s0 (eventFor .admitShadow 1)).1
    let s2 := (applyEvent s1 (eventFor .admitCanary 2)).1
    let s3 := (applyEvent s2 (eventFor .qualify 3)).1
    let s4 := (applyEvent s3 (eventFor .admitDefault 4)).1
    let s5 := (applyEvent s4 (eventFor .quarantine 5)).1
    let s6 := (applyEvent s5 (eventFor .terminate 6)).1
    s6.stage = .terminal ∧ s6.receiptCount = 6 ∧ s6.ordinaryReleaseCount = 1 ∧
      s6.quarantineCount = 1 ∧ s6.terminalCount = 1 ∧
      s6.supportAssignmentCount = 0 ∧ s6.externalEffectCount = 0 := by native_decide

end AsiStackProofs.ReadinessRefinement
