import AsiStackProofs.GovernedOperations

namespace AsiStackProofs.GovernedOperationsRefinement

open AsiStackProofs.GovernedOperations

inductive Stage where
  | normal
  | incidentOpen
  | commandBound
  | contained
  | degraded
  | reconciled
  | reviewed
  | restored
deriving DecidableEq, Repr

inductive EventKind where
  | detectIncident
  | bindCommand
  | confirmContainment
  | enterDegradedMode
  | reconcileStateAndEffects
  | reviewRecovery
  | restoreService
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage
  | rejectIdentitySubstitution
  | rejectReplay
  | rejectAuthorityLeak
  | requestObservation
  | rejectSelfDetection
  | requestCommand
  | requestEmergencyLease
  | requestContainment
  | rejectDependentContainment
  | rejectAuthorityWidening
  | requestQualifiedFallback
  | requestStateInventory
  | requestEffectDisposition
  | requestResidualOwner
  | requestFreshAcceptance
  | rejectDependentVerifier
  | requestEmergencyExpiry
  | acceptDetection
  | acceptCommand
  | acceptContainment
  | acceptDegradation
  | acceptReconciliation
  | acceptReview
  | acceptRestoration
deriving DecidableEq, Repr

structure State where
  stage : Stage
  deploymentDigest : Nat
  incidentDigest : Nat
  commandDigest : Nat
  candidateDigest : Nat
  protocolVersion : Nat
  normalAuthority : AuthorityEnvelope
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
  deploymentDigest : Nat
  incidentDigest : Nat
  commandDigest : Nat
  candidateDigest : Nat
  protocolVersion : Nat
  eventDigest : Nat
  proposedAuthority : AuthorityEnvelope
  incidentObserved : Bool
  detectorIndependent : Bool
  commanderBound : Bool
  emergencyLeasePresent : Bool
  containmentObserved : Bool
  containmentIndependent : Bool
  fallbackQualified : Bool
  requiredStateCount : Nat
  reconciledStateCount : Nat
  descendantsComplete : Bool
  effectsEnumerated : Bool
  effectsDispositionComplete : Bool
  irreversibleResidualAccepted : Bool
  residualOwnerAccepted : Bool
  acceptanceFresh : Bool
  independentVerifier : Bool
  emergencyLeaseExpired : Bool
  recurrenceOfPriorIncident : Bool
  supportAssignmentRequested : Bool
  releaseRequested : Bool
  externalAuthorityRequested : Bool
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .normal | .restored => .detectIncident
  | .incidentOpen => .bindCommand
  | .commandBound => .confirmContainment
  | .contained => .enterDegradedMode
  | .degraded => .reconcileStateAndEffects
  | .reconciled => .reviewRecovery
  | .reviewed => .restoreService

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.deploymentDigest = packet.deploymentDigest &&
    state.incidentDigest = packet.incidentDigest &&
    state.commandDigest = packet.commandDigest &&
    state.candidateDigest = packet.candidateDigest &&
    state.protocolVersion = packet.protocolVersion

def authorityLeakRequested (packet : Packet) : Bool :=
  packet.supportAssignmentRequested || packet.releaseRequested ||
    packet.externalAuthorityRequested

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if kind != expectedKind state.stage then .rejectWrongStage
  else if ! identityMatches state packet then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectReplay
  else if authorityLeakRequested packet then .rejectAuthorityLeak
  else match state.stage with
  | .normal | .restored =>
      if ! packet.incidentObserved then .requestObservation
      else if ! packet.detectorIndependent then .rejectSelfDetection
      else .acceptDetection
  | .incidentOpen =>
      if ! packet.commanderBound then .requestCommand
      else if ! packet.emergencyLeasePresent then .requestEmergencyLease
      else .acceptCommand
  | .commandBound =>
      if ! packet.containmentObserved then .requestContainment
      else if ! packet.containmentIndependent then .rejectDependentContainment
      else .acceptContainment
  | .contained =>
      if ! packet.incidentObserved || ! packet.commanderBound ||
          ! packet.emergencyLeasePresent || ! packet.containmentIndependent then
        .requestContainment
      else if ! authorityWithin state.normalAuthority packet.proposedAuthority then
        .rejectAuthorityWidening
      else if ! packet.fallbackQualified then .requestQualifiedFallback
      else .acceptDegradation
  | .degraded =>
      if packet.reconciledStateCount != packet.requiredStateCount ||
          ! packet.descendantsComplete then .requestStateInventory
      else if ! packet.effectsEnumerated || ! packet.effectsDispositionComplete ||
          ! packet.irreversibleResidualAccepted then .requestEffectDisposition
      else if ! packet.residualOwnerAccepted then .requestResidualOwner
      else .acceptReconciliation
  | .reconciled =>
      if ! packet.acceptanceFresh then .requestFreshAcceptance
      else if ! packet.independentVerifier then .rejectDependentVerifier
      else .acceptReview
  | .reviewed =>
      if packet.reconciledStateCount != packet.requiredStateCount ||
          ! packet.descendantsComplete then .requestStateInventory
      else if ! packet.effectsEnumerated || ! packet.effectsDispositionComplete ||
          ! packet.irreversibleResidualAccepted || ! packet.residualOwnerAccepted then
        .requestEffectDisposition
      else if ! packet.acceptanceFresh then .requestFreshAcceptance
      else if ! packet.independentVerifier then .rejectDependentVerifier
      else if ! packet.fallbackQualified then .requestQualifiedFallback
      else if ! packet.emergencyLeaseExpired then .requestEmergencyExpiry
      else .acceptRestoration

def accepted : Route -> Bool
  | .acceptDetection | .acceptCommand | .acceptContainment | .acceptDegradation
  | .acceptReconciliation | .acceptReview | .acceptRestoration => true
  | _ => false

def nextStage : Stage -> Stage
  | .normal | .restored => .incidentOpen
  | .incidentOpen => .commandBound
  | .commandBound => .contained
  | .contained => .degraded
  | .degraded => .reconciled
  | .reconciled => .reviewed
  | .reviewed => .restored

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       recoveryCount := state.recoveryCount +
         (if route = .acceptRestoration then 1 else 0)
       recurrenceCount := state.recurrenceCount +
         (if route = .acceptDetection && packet.recurrenceOfPriorIncident then 1 else 0)
       containmentActive := route != .acceptRestoration
       externalEffectsEnabled := route = .acceptRestoration }, route)
  else (state, route)

def toOperationsPacket (state : State) (packet : Packet) : OperationsPacket :=
  { deploymentDigest := packet.deploymentDigest
    incidentDigest := packet.incidentDigest
    commandDigest := packet.commandDigest
    candidateDigest := packet.candidateDigest
    expectedDeploymentDigest := state.deploymentDigest
    expectedIncidentDigest := state.incidentDigest
    expectedCommandDigest := state.commandDigest
    expectedCandidateDigest := state.candidateDigest
    currentAuthority := state.normalAuthority
    degradedAuthority := packet.proposedAuthority
    incidentDeclared := packet.incidentObserved
    commandBound := packet.commanderBound
    containmentIndependent := packet.containmentIndependent
    emergencyLeasePresent := packet.emergencyLeasePresent
    emergencyLeaseExpired := packet.emergencyLeaseExpired
    requiredStateCount := packet.requiredStateCount
    reconciledStateCount := packet.reconciledStateCount
    descendantInventoryComplete := packet.descendantsComplete
    externalEffectsEnumerated := packet.effectsEnumerated
    externalEffectsDispositionComplete := packet.effectsDispositionComplete
    irreversibleResidualAccepted := packet.irreversibleResidualAccepted
    acceptanceFresh := packet.acceptanceFresh
    independentVerifier := packet.independentVerifier
    fallbackQualified := packet.fallbackQualified
    supportPromotionRequested := packet.supportAssignmentRequested
    releaseRequested := packet.releaseRequested
    externalEffectAuthorityRequested := packet.externalAuthorityRequested }

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

theorem accepted_detection_disables_effects
    (state : State) (kind : EventKind) (packet : Packet)
    (h : routeFor state kind packet = .acceptDetection) :
    (applyEvent state kind packet).1.containmentActive = true ∧
      (applyEvent state kind packet).1.externalEffectsEnabled = false := by
  simp [applyEvent, h, accepted]

theorem accepted_degradation_refines_static_authority_contract
    (state : State) (packet : Packet)
    (stageContained : state.stage = .contained)
    (h : routeFor state .enterDegradedMode packet = .acceptDegradation) :
    degradationRoute (toOperationsPacket state packet) = .acceptDegraded := by
  have identity : identityMatches state packet = true := by
    by_cases mismatch : identityMatches state packet = false
    · simp [routeFor, expectedKind, stageContained, mismatch] at h
    · cases value : identityMatches state packet <;> simp_all
  have freshEvent : ¬ packet.eventDigest = state.lastEventDigest := by
    intro replay
    simp [routeFor, expectedKind, stageContained, identity, replay] at h
  have noLeak : authorityLeakRequested packet = false := by
    by_cases leak : authorityLeakRequested packet = true
    · simp [routeFor, expectedKind, stageContained, identity, freshEvent, leak] at h
    · cases value : authorityLeakRequested packet <;> simp_all
  have incident : packet.incidentObserved = true := by
    by_cases missing : packet.incidentObserved = false
    · simp [routeFor, expectedKind, stageContained, identity, freshEvent, noLeak,
        missing] at h
    · cases value : packet.incidentObserved <;> simp_all
  have command : packet.commanderBound = true := by
    by_cases missing : packet.commanderBound = false
    · simp [routeFor, expectedKind, stageContained, identity, freshEvent, noLeak,
        incident, missing] at h
    · cases value : packet.commanderBound <;> simp_all
  have lease : packet.emergencyLeasePresent = true := by
    by_cases missing : packet.emergencyLeasePresent = false
    · simp [routeFor, expectedKind, stageContained, identity, freshEvent, noLeak,
        incident, command, missing] at h
    · cases value : packet.emergencyLeasePresent <;> simp_all
  have containment : packet.containmentIndependent = true := by
    by_cases missing : packet.containmentIndependent = false
    · simp [routeFor, expectedKind, stageContained, identity, freshEvent, noLeak,
        incident, command, lease, missing] at h
    · cases value : packet.containmentIndependent <;> simp_all
  have within : authorityWithin state.normalAuthority packet.proposedAuthority = true := by
    by_cases wider : authorityWithin state.normalAuthority packet.proposedAuthority = false
    · simp [routeFor, expectedKind, stageContained, identity, freshEvent, noLeak,
        incident, command, lease, containment, wider] at h
    · cases value : authorityWithin state.normalAuthority packet.proposedAuthority <;> simp_all
  have fallback : packet.fallbackQualified = true := by
    by_cases missing : packet.fallbackQualified = false
    · simp [routeFor, expectedKind, stageContained, identity, freshEvent, noLeak,
        incident, command, lease, containment, within, missing] at h
    · cases value : packet.fallbackQualified <;> simp_all
  have identityFields := identity
  simp [identityMatches] at identityFields
  rcases identityFields with ⟨⟨⟨⟨deployment, incidentId⟩, commandId⟩, candidate⟩, _⟩
  have noSupport : packet.supportAssignmentRequested = false := by
    cases support : packet.supportAssignmentRequested <;>
      simp_all [authorityLeakRequested]
  have noRelease : packet.releaseRequested = false := by
    cases release : packet.releaseRequested <;>
      simp_all [authorityLeakRequested]
  have noExternal : packet.externalAuthorityRequested = false := by
    cases external : packet.externalAuthorityRequested <;>
      simp_all [authorityLeakRequested]
  simp [degradationRoute, toOperationsPacket, exactIdentity, deployment, incidentId,
    commandId, candidate, within, incident, command, containment, lease, noSupport,
    noRelease, noExternal, GovernedOperations.authorityLeakRequested]

theorem accepted_restoration_refines_static_recovery_contract
    (state : State) (packet : Packet)
    (stageReviewed : state.stage = .reviewed)
    (h : routeFor state .restoreService packet = .acceptRestoration) :
    recoveryComplete (toOperationsPacket state packet) = true ∧
      recoveryRoute (toOperationsPacket state packet) = .acceptRecovery := by
  have identity : identityMatches state packet = true := by
    by_cases mismatch : identityMatches state packet = false
    · simp [routeFor, expectedKind, stageReviewed, mismatch] at h
    · cases value : identityMatches state packet <;> simp_all
  have freshEvent : ¬ packet.eventDigest = state.lastEventDigest := by
    intro replay
    simp [routeFor, expectedKind, stageReviewed, identity, replay] at h
  have noLeak : authorityLeakRequested packet = false := by
    by_cases leak : authorityLeakRequested packet = true
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, leak] at h
    · cases value : authorityLeakRequested packet <;> simp_all
  have stateCount : packet.reconciledStateCount = packet.requiredStateCount := by
    by_cases mismatch : packet.reconciledStateCount != packet.requiredStateCount
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        mismatch] at h
    · simp_all
  have descendants : packet.descendantsComplete = true := by
    by_cases missing : packet.descendantsComplete = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, missing] at h
    · cases value : packet.descendantsComplete <;> simp_all
  have effectsEnumerated : packet.effectsEnumerated = true := by
    by_cases missing : packet.effectsEnumerated = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, descendants, missing] at h
    · cases value : packet.effectsEnumerated <;> simp_all
  have effectsComplete : packet.effectsDispositionComplete = true := by
    by_cases missing : packet.effectsDispositionComplete = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, descendants, effectsEnumerated, missing] at h
    · cases value : packet.effectsDispositionComplete <;> simp_all
  have irreversible : packet.irreversibleResidualAccepted = true := by
    by_cases missing : packet.irreversibleResidualAccepted = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, descendants, effectsEnumerated, effectsComplete, missing] at h
    · cases value : packet.irreversibleResidualAccepted <;> simp_all
  have residualOwner : packet.residualOwnerAccepted = true := by
    by_cases missing : packet.residualOwnerAccepted = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, descendants, effectsEnumerated, effectsComplete, irreversible,
        missing] at h
    · cases value : packet.residualOwnerAccepted <;> simp_all
  have freshAcceptance : packet.acceptanceFresh = true := by
    by_cases stale : packet.acceptanceFresh = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, descendants, effectsEnumerated, effectsComplete, irreversible,
        residualOwner, stale] at h
    · cases value : packet.acceptanceFresh <;> simp_all
  have verifier : packet.independentVerifier = true := by
    by_cases dependent : packet.independentVerifier = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, descendants, effectsEnumerated, effectsComplete, irreversible,
        residualOwner, freshAcceptance, dependent] at h
    · cases value : packet.independentVerifier <;> simp_all
  have fallback : packet.fallbackQualified = true := by
    by_cases missing : packet.fallbackQualified = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, descendants, effectsEnumerated, effectsComplete, irreversible,
        residualOwner, freshAcceptance, verifier, missing] at h
    · cases value : packet.fallbackQualified <;> simp_all
  have expired : packet.emergencyLeaseExpired = true := by
    by_cases active : packet.emergencyLeaseExpired = false
    · simp [routeFor, expectedKind, stageReviewed, identity, freshEvent, noLeak,
        stateCount, descendants, effectsEnumerated, effectsComplete, irreversible,
        residualOwner, freshAcceptance, verifier, fallback, active] at h
    · cases value : packet.emergencyLeaseExpired <;> simp_all
  have identityFields := identity
  simp [identityMatches] at identityFields
  rcases identityFields with ⟨⟨⟨⟨deployment, incidentId⟩, commandId⟩, candidate⟩, _⟩
  have noSupport : packet.supportAssignmentRequested = false := by
    cases support : packet.supportAssignmentRequested <;>
      simp_all [authorityLeakRequested]
  have noRelease : packet.releaseRequested = false := by
    cases release : packet.releaseRequested <;>
      simp_all [authorityLeakRequested]
  have noExternal : packet.externalAuthorityRequested = false := by
    cases external : packet.externalAuthorityRequested <;>
      simp_all [authorityLeakRequested]
  have exactStatic : exactIdentity (toOperationsPacket state packet) = true := by
    simp [toOperationsPacket, exactIdentity, deployment, incidentId, commandId,
      candidate]
  have completeStatic : recoveryComplete (toOperationsPacket state packet) = true := by
    simp [recoveryComplete, toOperationsPacket, stateCount, descendants,
      effectsEnumerated, effectsComplete, irreversible, freshAcceptance, verifier,
      expired, fallback, noSupport, noRelease, noExternal,
      GovernedOperations.authorityLeakRequested]
  exact ⟨completeStatic, by simp [recoveryRoute, exactStatic, completeStatic]⟩

def canonicalNormalAuthority : AuthorityEnvelope :=
  { capability := 4, data := 4, tools := 4, population := 4,
    durationSeconds := 3600 }

def canonicalDegradedAuthority : AuthorityEnvelope :=
  { capability := 2, data := 2, tools := 1, population := 1,
    durationSeconds := 900 }

def widenedCapabilityAuthority : AuthorityEnvelope :=
  { capability := 5, data := 2, tools := 1, population := 1,
    durationSeconds := 900 }

def canonicalState (stage : Stage) : State :=
  { stage := stage, deploymentDigest := 7101, incidentDigest := 7102,
    commandDigest := 7103, candidateDigest := 7104, protocolVersion := 2,
    normalAuthority := canonicalNormalAuthority, lastEventDigest := 0,
    receiptCount := 0, recoveryCount := 0, recurrenceCount := 0,
    containmentActive := stage != .normal && stage != .restored,
    externalEffectsEnabled := stage = .normal || stage = .restored,
    supportAssignmentCount := 0, externalAuthorityCount := 0 }

def canonicalPacket (eventDigest : Nat) : Packet :=
  { deploymentDigest := 7101, incidentDigest := 7102, commandDigest := 7103,
    candidateDigest := 7104, protocolVersion := 2, eventDigest := eventDigest,
    proposedAuthority := canonicalDegradedAuthority, incidentObserved := true,
    detectorIndependent := true, commanderBound := true,
    emergencyLeasePresent := true, containmentObserved := true,
    containmentIndependent := true, fallbackQualified := true,
    requiredStateCount := 11, reconciledStateCount := 11,
    descendantsComplete := true, effectsEnumerated := true,
    effectsDispositionComplete := true, irreversibleResidualAccepted := true,
    residualOwnerAccepted := true, acceptanceFresh := true,
    independentVerifier := true, emergencyLeaseExpired := true,
    recurrenceOfPriorIncident := false, supportAssignmentRequested := false,
    releaseRequested := false, externalAuthorityRequested := false }

theorem widening_authority_blocks_degradation :
    routeFor (canonicalState .contained) .enterDegradedMode
      { canonicalPacket 4 with proposedAuthority :=
        widenedCapabilityAuthority } = .rejectAuthorityWidening := by
  native_decide

theorem incomplete_descendant_inventory_blocks_reconciliation :
    routeFor (canonicalState .degraded) .reconcileStateAndEffects
      { canonicalPacket 5 with descendantsComplete := false } =
        .requestStateInventory := by
  native_decide

theorem unknown_effect_blocks_reconciliation :
    routeFor (canonicalState .degraded) .reconcileStateAndEffects
      { canonicalPacket 5 with effectsDispositionComplete := false } =
        .requestEffectDisposition := by
  native_decide

theorem dependent_verifier_blocks_review :
    routeFor (canonicalState .reconciled) .reviewRecovery
      { canonicalPacket 6 with independentVerifier := false } =
        .rejectDependentVerifier := by
  native_decide

theorem active_emergency_lease_blocks_restoration :
    routeFor (canonicalState .reviewed) .restoreService
      { canonicalPacket 7 with emergencyLeaseExpired := false } =
        .requestEmergencyExpiry := by
  native_decide

theorem authority_leak_blocks_every_lifecycle_stage (stage : Stage) :
    routeFor (canonicalState stage) (expectedKind stage)
      { canonicalPacket 99 with supportAssignmentRequested := true } =
        .rejectAuthorityLeak := by
  cases stage <;> native_decide

theorem bounded_incident_lifecycle_reaches_restored_service :
  let s0 := canonicalState .normal
  let s1 := (applyEvent s0 .detectIncident (canonicalPacket 1)).1
  let s2 := (applyEvent s1 .bindCommand (canonicalPacket 2)).1
  let s3 := (applyEvent s2 .confirmContainment (canonicalPacket 3)).1
  let s4 := (applyEvent s3 .enterDegradedMode (canonicalPacket 4)).1
  let s5 := (applyEvent s4 .reconcileStateAndEffects (canonicalPacket 5)).1
  let s6 := (applyEvent s5 .reviewRecovery (canonicalPacket 6)).1
  let s7 := (applyEvent s6 .restoreService (canonicalPacket 7)).1
  s7.stage = .restored ∧ s7.receiptCount = 7 ∧ s7.recoveryCount = 1 ∧
    s7.containmentActive = false ∧ s7.externalEffectsEnabled = true ∧
    s7.supportAssignmentCount = 0 ∧ s7.externalAuthorityCount = 0 := by
  native_decide

theorem bounded_recurrence_reenters_incident_control :
  let restored :=
    { { { canonicalState .restored with receiptCount := 7 } with
        recoveryCount := 1 } with lastEventDigest := 7 }
  let recurrence := { canonicalPacket 8 with recurrenceOfPriorIncident := true }
  let next := (applyEvent restored .detectIncident recurrence).1
  next.stage = .incidentOpen ∧ next.receiptCount = 8 ∧
    next.recoveryCount = 1 ∧ next.recurrenceCount = 1 ∧
    next.containmentActive = true ∧ next.externalEffectsEnabled = false ∧
    next.supportAssignmentCount = 0 ∧ next.externalAuthorityCount = 0 := by
  native_decide

end AsiStackProofs.GovernedOperationsRefinement
