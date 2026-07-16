namespace AsiStackProofs.ProceduralMemoryRefinement

inductive Stage where
  | idle | clustered | abstracted | verified | qualified | routable | retired
deriving DecidableEq, Repr

inductive EventKind where
  | clusterTraces | bindAbstraction | verifyProcedure | qualifyProcedure
  | publishRoute | retireProcedure
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectProcedureSubstitution | rejectLineageSubstitution
  | rejectEventReplay | rejectAuthorityLeak
  | requestComparableTraces | requestNegativeExamples | requestSourceReceipts
  | requestEffectReceipts | requestInvariant | requestParameters
  | requestPreconditions | requestPostconditions | requestVerification
  | quarantineRegressionFailure | requestBenchmarkFloor | requestActiveScf
  | requestRollbackPlan | requestRollbackRehearsal | requestMonitoringPlan
  | requestResiduals | requestNonClaims | requestConsumerAcknowledgment
  | requestRetirementTrigger | requestRetirementReceipt
  | acceptCluster | acceptAbstraction | acceptVerification
  | acceptQualification | acceptRoute | acceptRetirement
deriving DecidableEq, Repr

structure Packet where
  procedureId : Nat
  procedureVersion : Nat
  sourceSetDigest : Nat
  traceClusterDigest : Nat
  abstractionDigest : Nat
  regressionSuiteDigest : Nat
  scfDigest : Nat
  policyDigest : Nat
  consumerDigest : Nat
  eventDigest : Nat
  comparableTracesPresent : Bool
  negativeExamplesPreserved : Bool
  sourceReceiptsPresent : Bool
  effectReceiptsPresent : Bool
  invariantPresent : Bool
  parametersPresent : Bool
  preconditionsPresent : Bool
  postconditionsPresent : Bool
  verificationPassed : Bool
  regressionFailed : Bool
  benchmarkFloorPreserved : Bool
  activeScfPresent : Bool
  rollbackPlanPresent : Bool
  rollbackRehearsed : Bool
  monitoringPlanPresent : Bool
  residualsPresent : Bool
  nonClaimsPresent : Bool
  consumerAcknowledgmentPresent : Bool
  retirementTriggered : Bool
  retirementReceiptPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  procedureId : Nat
  procedureVersion : Nat
  sourceSetDigest : Nat
  traceClusterDigest : Nat
  abstractionDigest : Nat
  regressionSuiteDigest : Nat
  scfDigest : Nat
  policyDigest : Nat
  consumerDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  qualifiedRouteCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .idle => .clusterTraces
  | .clustered => .bindAbstraction
  | .abstracted => .verifyProcedure
  | .verified => .qualifyProcedure
  | .qualified => .publishRoute
  | .routable => .retireProcedure
  | .retired => .retireProcedure

def exactProcedureBinding (state : State) (packet : Packet) : Bool :=
  packet.procedureId == state.procedureId &&
  packet.procedureVersion == state.procedureVersion &&
  packet.policyDigest == state.policyDigest &&
  packet.consumerDigest == state.consumerDigest

def exactLineageBinding (state : State) (packet : Packet) : Bool :=
  packet.sourceSetDigest == state.sourceSetDigest &&
  packet.traceClusterDigest == state.traceClusterDigest &&
  packet.abstractionDigest == state.abstractionDigest &&
  packet.regressionSuiteDigest == state.regressionSuiteDigest &&
  packet.scfDigest == state.scfDigest

def routeFor (state : State) (event : Event) : Route :=
  if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactProcedureBinding state event.packet then .rejectProcedureSubstitution
  else if ! exactLineageBinding state event.packet then .rejectLineageSubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectEventReplay
  else if event.packet.supportAssignmentRequested || event.packet.externalEffectRequested then
    .rejectAuthorityLeak
  else match state.stage with
  | .idle =>
      if ! event.packet.comparableTracesPresent then .requestComparableTraces
      else if ! event.packet.negativeExamplesPreserved then .requestNegativeExamples
      else if ! event.packet.sourceReceiptsPresent then .requestSourceReceipts
      else if ! event.packet.effectReceiptsPresent then .requestEffectReceipts
      else .acceptCluster
  | .clustered =>
      if ! event.packet.invariantPresent then .requestInvariant
      else if ! event.packet.parametersPresent then .requestParameters
      else if ! event.packet.preconditionsPresent then .requestPreconditions
      else if ! event.packet.postconditionsPresent then .requestPostconditions
      else .acceptAbstraction
  | .abstracted =>
      if ! event.packet.verificationPassed then .requestVerification
      else if event.packet.regressionFailed then .quarantineRegressionFailure
      else if ! event.packet.benchmarkFloorPreserved then .requestBenchmarkFloor
      else .acceptVerification
  | .verified =>
      if ! event.packet.activeScfPresent then .requestActiveScf
      else if ! event.packet.rollbackPlanPresent then .requestRollbackPlan
      else if ! event.packet.rollbackRehearsed then .requestRollbackRehearsal
      else .acceptQualification
  | .qualified =>
      if ! event.packet.monitoringPlanPresent then .requestMonitoringPlan
      else if ! event.packet.residualsPresent then .requestResiduals
      else if ! event.packet.nonClaimsPresent then .requestNonClaims
      else if ! event.packet.consumerAcknowledgmentPresent then .requestConsumerAcknowledgment
      else .acceptRoute
  | .routable =>
      if ! event.packet.retirementTriggered then .requestRetirementTrigger
      else if ! event.packet.retirementReceiptPresent then .requestRetirementReceipt
      else .acceptRetirement
  | .retired => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptCluster | .acceptAbstraction | .acceptVerification
  | .acceptQualification | .acceptRoute | .acceptRetirement => true
  | _ => false

def advanceStage : Stage -> Stage
  | .idle => .clustered | .clustered => .abstracted | .abstracted => .verified
  | .verified => .qualified | .qualified => .routable | .routable => .retired
  | .retired => .retired

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advanceStage state.stage
       lastEventDigest := event.packet.eventDigest
       receiptCount := state.receiptCount + 1
       qualifiedRouteCount :=
         if state.stage == .qualified then state.qualifiedRouteCount + 1
         else state.qualifiedRouteCount }, route)
  else (state, route)

theorem apply_event_preserves_procedure_and_lineage_identity
    (state : State) (event : Event) :
    (applyEvent state event).1.procedureId = state.procedureId ∧
    (applyEvent state event).1.procedureVersion = state.procedureVersion ∧
    (applyEvent state event).1.sourceSetDigest = state.sourceSetDigest ∧
    (applyEvent state event).1.traceClusterDigest = state.traceClusterDigest ∧
    (applyEvent state event).1.abstractionDigest = state.abstractionDigest ∧
    (applyEvent state event).1.regressionSuiteDigest = state.regressionSuiteDigest := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_effect
    (state : State) (event : Event) :
    (applyEvent state event).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state event).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem accepted_step_adds_exactly_one_receipt
    (state : State) (event : Event) (h : accepted (routeFor state event) = true) :
    (applyEvent state event).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, h]

def canonicalPacket : Packet :=
  { procedureId := 701, procedureVersion := 3, sourceSetDigest := 801
    traceClusterDigest := 802, abstractionDigest := 803
    regressionSuiteDigest := 804, scfDigest := 805, policyDigest := 806
    consumerDigest := 807, eventDigest := 1
    comparableTracesPresent := true, negativeExamplesPreserved := true
    sourceReceiptsPresent := true, effectReceiptsPresent := true
    invariantPresent := true, parametersPresent := true
    preconditionsPresent := true, postconditionsPresent := true
    verificationPassed := true, regressionFailed := false
    benchmarkFloorPreserved := true, activeScfPresent := true
    rollbackPlanPresent := true, rollbackRehearsed := true
    monitoringPlanPresent := true, residualsPresent := true
    nonClaimsPresent := true, consumerAcknowledgmentPresent := true
    retirementTriggered := true, retirementReceiptPresent := true
    supportAssignmentRequested := false, externalEffectRequested := false }

def initialState : State :=
  { stage := .idle, procedureId := 701, procedureVersion := 3
    sourceSetDigest := 801, traceClusterDigest := 802, abstractionDigest := 803
    regressionSuiteDigest := 804, scfDigest := 805, policyDigest := 806
    consumerDigest := 807, lastEventDigest := 0, receiptCount := 0
    qualifiedRouteCount := 0, supportAssignmentCount := 0, externalEffectCount := 0 }

def clusterEvent : Event := { kind := .clusterTraces, packet := canonicalPacket }
def clusteredState : State := (applyEvent initialState clusterEvent).1
def abstractionEvent : Event := { kind := .bindAbstraction, packet := { canonicalPacket with eventDigest := 2 } }
def abstractedState : State := (applyEvent clusteredState abstractionEvent).1
def verificationEvent : Event := { kind := .verifyProcedure, packet := { canonicalPacket with eventDigest := 3 } }
def verifiedState : State := (applyEvent abstractedState verificationEvent).1
def qualificationEvent : Event := { kind := .qualifyProcedure, packet := { canonicalPacket with eventDigest := 4 } }
def qualifiedState : State := (applyEvent verifiedState qualificationEvent).1
def routeEvent : Event := { kind := .publishRoute, packet := { canonicalPacket with eventDigest := 5 } }
def routableState : State := (applyEvent qualifiedState routeEvent).1
def retirementEvent : Event := { kind := .retireProcedure, packet := { canonicalPacket with eventDigest := 6 } }
def finalState : State := (applyEvent routableState retirementEvent).1

theorem clustering_requires_negative_examples :
    routeFor initialState { clusterEvent with packet := { canonicalPacket with eventDigest := 20, negativeExamplesPreserved := false } } =
      .requestNegativeExamples := by rfl

theorem clustering_requires_effect_receipts :
    routeFor initialState { clusterEvent with packet := { canonicalPacket with eventDigest := 21, effectReceiptsPresent := false } } =
      .requestEffectReceipts := by rfl

theorem abstraction_requires_parameters :
    routeFor clusteredState { abstractionEvent with packet := { canonicalPacket with eventDigest := 22, parametersPresent := false } } =
      .requestParameters := by rfl

theorem abstraction_requires_preconditions :
    routeFor clusteredState { abstractionEvent with packet := { canonicalPacket with eventDigest := 23, preconditionsPresent := false } } =
      .requestPreconditions := by rfl

theorem failed_verification_blocks_qualification :
    routeFor abstractedState { verificationEvent with packet := { canonicalPacket with eventDigest := 24, verificationPassed := false } } =
      .requestVerification := by rfl

theorem failed_regression_routes_quarantine :
    routeFor abstractedState { verificationEvent with packet := { canonicalPacket with eventDigest := 25, regressionFailed := true } } =
      .quarantineRegressionFailure := by rfl

theorem qualification_requires_active_scf :
    routeFor verifiedState { qualificationEvent with packet := { canonicalPacket with eventDigest := 26, activeScfPresent := false } } =
      .requestActiveScf := by rfl

theorem qualification_requires_rehearsed_rollback :
    routeFor verifiedState { qualificationEvent with packet := { canonicalPacket with eventDigest := 27, rollbackRehearsed := false } } =
      .requestRollbackRehearsal := by rfl

theorem routing_requires_monitoring :
    routeFor qualifiedState { routeEvent with packet := { canonicalPacket with eventDigest := 28, monitoringPlanPresent := false } } =
      .requestMonitoringPlan := by rfl

theorem retirement_requires_receipt :
    routeFor routableState { retirementEvent with packet := { canonicalPacket with eventDigest := 29, retirementReceiptPresent := false } } =
      .requestRetirementReceipt := by rfl

theorem full_procedure_lifecycle_reaches_retirement :
    finalState.stage = .retired ∧ finalState.receiptCount = 6 ∧
    finalState.qualifiedRouteCount = 1 ∧ finalState.supportAssignmentCount = 0 ∧
    finalState.externalEffectCount = 0 := by native_decide

end AsiStackProofs.ProceduralMemoryRefinement
