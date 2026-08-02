namespace AsiStackProofs.GovernedWorldModels

/-!
A finite custody and routing model for imagined world-model branches.  Every
field is a declared record predicate, not evidence that an observation is true,
a latent state is grounded, a calibration estimate is valid, or an action is
safe.  The model constrains admission and discrepancy handling only.
-/

inductive SupportClass where
  | qualified
  | unsupported
deriving DecidableEq, Repr

inductive RolloutRoute where
  | reject
  | reobserve
  | fallback
  | review
  | admitForPlanning
  | authorizeEffect
deriving DecidableEq, Repr

structure RolloutPacket where
  exactModelIdentity : Bool
  currentModelVersion : Bool
  observationFresh : Bool
  interventionSemanticsBound : Bool
  horizonBound : Bool
  calibrationRecorded : Bool
  supportClass : SupportClass
  materialDisagreement : Bool
  authorityCeilingPreserved : Bool
deriving DecidableEq, Repr

def RolloutRouteFor (packet : RolloutPacket) : RolloutRoute :=
  if packet.exactModelIdentity = false ∨
      packet.interventionSemanticsBound = false ∨
      packet.horizonBound = false ∨
      packet.authorityCeilingPreserved = false then
    .reject
  else if packet.currentModelVersion = false ∨ packet.observationFresh = false then
    .reobserve
  else if packet.supportClass = .unsupported ∨ packet.calibrationRecorded = false then
    .fallback
  else if packet.materialDisagreement = true then
    .review
  else
    .admitForPlanning

theorem rollout_never_authorizes_effect (packet : RolloutPacket) :
    RolloutRouteFor packet ≠ .authorizeEffect := by
  unfold RolloutRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all

theorem unsupported_rollout_no_authority
    (packet : RolloutPacket)
    (invalid :
      packet.currentModelVersion = false ∨
      packet.supportClass = .unsupported ∨
      packet.calibrationRecorded = false ∨
      packet.materialDisagreement = true) :
    RolloutRouteFor packet ≠ .admitForPlanning := by
  unfold RolloutRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all

theorem admitted_rollout_preserves_declared_boundary
    (packet : RolloutPacket)
    (admitted : RolloutRouteFor packet = .admitForPlanning) :
    packet.exactModelIdentity = true ∧
    packet.currentModelVersion = true ∧
    packet.observationFresh = true ∧
    packet.interventionSemanticsBound = true ∧
    packet.horizonBound = true ∧
    packet.calibrationRecorded = true ∧
    packet.supportClass = .qualified ∧
    packet.materialDisagreement = false ∧
    packet.authorityCeilingPreserved = true := by
  unfold RolloutRouteFor at admitted
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  cases support : packet.supportClass <;> simp_all

inductive ResidualRoute where
  | continueModelBased
  | reestimate
  | fallback
  | review
  | safeHold
deriving DecidableEq, Repr

structure RealityResidual where
  material : Bool
  reestimationAvailable : Bool
  fallbackAvailable : Bool
  reviewAvailable : Bool
deriving DecidableEq, Repr

def ResidualRouteFor (residual : RealityResidual) : ResidualRoute :=
  if residual.material = false then
    .continueModelBased
  else if residual.reestimationAvailable = true then
    .reestimate
  else if residual.fallbackAvailable = true then
    .fallback
  else if residual.reviewAvailable = true then
    .review
  else
    .safeHold

theorem reality_residual_forces_route
    (residual : RealityResidual)
    (material : residual.material = true) :
    ResidualRouteFor residual ≠ .continueModelBased := by
  unfold ResidualRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all

theorem material_residual_selects_bounded_response
    (residual : RealityResidual)
    (material : residual.material = true) :
    ResidualRouteFor residual = .reestimate ∨
    ResidualRouteFor residual = .fallback ∨
    ResidualRouteFor residual = .review ∨
    ResidualRouteFor residual = .safeHold := by
  cases hm : residual.material <;>
    cases hre : residual.reestimationAvailable <;>
    cases hfa : residual.fallbackAvailable <;>
    cases hrv : residual.reviewAvailable <;>
    simp_all [ResidualRouteFor]

def qualifiedPacket : RolloutPacket where
  exactModelIdentity := true
  currentModelVersion := true
  observationFresh := true
  interventionSemanticsBound := true
  horizonBound := true
  calibrationRecorded := true
  supportClass := .qualified
  materialDisagreement := false
  authorityCeilingPreserved := true

def stalePacket : RolloutPacket :=
  { qualifiedPacket with currentModelVersion := false }

def unsupportedPacket : RolloutPacket :=
  { qualifiedPacket with supportClass := .unsupported }

def materialResidual : RealityResidual where
  material := true
  reestimationAvailable := false
  fallbackAvailable := false
  reviewAvailable := false

theorem qualified_fixture_admits_for_planning :
    RolloutRouteFor qualifiedPacket = .admitForPlanning := by native_decide

theorem stale_fixture_requires_reobservation :
    RolloutRouteFor stalePacket = .reobserve := by native_decide

theorem unsupported_fixture_falls_back :
    RolloutRouteFor unsupportedPacket = .fallback := by native_decide

theorem material_fixture_holds_safely :
    ResidualRouteFor materialResidual = .safeHold := by native_decide

/-!
The transaction lifecycle below strengthens the static packet classifiers into
a temporal custody contract. It does not model prediction quality or execute an
action. In particular, a planning handoff is not effect authority, and an
effect can enter the record only as an independently observed actuality.
-/

inductive LifecycleStage where
  | awaitingObservation
  | observationBound
  | modelBound
  | branchQualified
  | planningHandoff
  | effectObserved
  | reconciled
deriving DecidableEq, Repr

inductive LifecycleEventKind where
  | bindObservation
  | bindModel
  | qualifyBranch
  | handoffForPlanning
  | recordObservedEffect
  | reconcileResidual
deriving DecidableEq, Repr

inductive LifecycleRoute where
  | rejectWrongStage
  | rejectIdentitySubstitution
  | rejectEventReplay
  | rejectAuthorityLaundering
  | requestAdmittedObservation
  | requestFreshObservation
  | rejectImaginationAsObservation
  | requestBoundModel
  | requestCurrentModel
  | requestInterventionSemantics
  | requestBoundHorizon
  | requestCalibration
  | requestQualifiedSupport
  | requestDisagreementDisposition
  | requestObservationLineage
  | requestImaginedLabel
  | requestBoundedPlannerUse
  | requestActionReceipt
  | requestIndependentEffectObservation
  | requestActualityLabel
  | requestResidual
  | requestResidualResponse
  | requestResidualOwner
  | acceptObservation
  | acceptModel
  | acceptBranch
  | acceptPlanningHandoff
  | acceptEffectObservation
  | acceptReconciliation
deriving DecidableEq, Repr

structure LifecycleState where
  stage : LifecycleStage
  modelIdentity : Nat
  modelVersion : Nat
  observationDigest : Nat
  branchDigest : Nat
  actionDigest : Nat
  effectDigest : Nat
  authorityCeiling : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  planningHandoffCount : Nat
  observedEffectCount : Nat
  reconciliationCount : Nat
  supportAssignmentCount : Nat
  effectAuthorityCount : Nat
deriving DecidableEq, Repr

structure LifecyclePacket where
  modelIdentity : Nat
  modelVersion : Nat
  observationDigest : Nat
  branchDigest : Nat
  actionDigest : Nat
  effectDigest : Nat
  authorityCeiling : Nat
  eventDigest : Nat
  observationAdmitted : Bool
  observationFresh : Bool
  observationMarkedActual : Bool
  modelCheckpointBound : Bool
  modelCurrent : Bool
  interventionSemanticsBound : Bool
  horizonBound : Bool
  calibrationCurrent : Bool
  supportQualified : Bool
  materialDisagreement : Bool
  disagreementDispositionPresent : Bool
  branchDerivedFromObservation : Bool
  branchMarkedImagined : Bool
  plannerUseBounded : Bool
  actionReceiptPresent : Bool
  effectIndependentlyObserved : Bool
  effectMarkedActual : Bool
  residualComputed : Bool
  materialResidual : Bool
  residualResponseSelected : Bool
  residualOwnerPresent : Bool
  supportAssignmentRequested : Bool
  executionAuthorityRequested : Bool
deriving DecidableEq, Repr

def expectedLifecycleKind : LifecycleStage -> LifecycleEventKind
  | .awaitingObservation => .bindObservation
  | .observationBound => .bindModel
  | .modelBound => .qualifyBranch
  | .branchQualified => .handoffForPlanning
  | .planningHandoff => .recordObservedEffect
  | .effectObserved => .reconcileResidual
  | .reconciled => .bindObservation

def lifecycleIdentityMatches (state : LifecycleState) (packet : LifecyclePacket) : Bool :=
  state.modelIdentity = packet.modelIdentity &&
    state.modelVersion = packet.modelVersion &&
    state.observationDigest = packet.observationDigest &&
    state.branchDigest = packet.branchDigest &&
    state.actionDigest = packet.actionDigest &&
    state.effectDigest = packet.effectDigest &&
    state.authorityCeiling = packet.authorityCeiling

def lifecycleRouteFor
    (state : LifecycleState) (kind : LifecycleEventKind)
    (packet : LifecyclePacket) : LifecycleRoute :=
  if kind != expectedLifecycleKind state.stage then .rejectWrongStage
  else if lifecycleIdentityMatches state packet = false then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectEventReplay
  else if packet.supportAssignmentRequested || packet.executionAuthorityRequested then
    .rejectAuthorityLaundering
  else match state.stage with
  | .awaitingObservation | .reconciled =>
      if packet.observationAdmitted = false then .requestAdmittedObservation
      else if packet.observationFresh = false then .requestFreshObservation
      else if packet.observationMarkedActual = false then .rejectImaginationAsObservation
      else .acceptObservation
  | .observationBound =>
      if packet.modelCheckpointBound = false then .requestBoundModel
      else if packet.modelCurrent = false then .requestCurrentModel
      else .acceptModel
  | .modelBound =>
      if packet.interventionSemanticsBound = false then .requestInterventionSemantics
      else if packet.horizonBound = false then .requestBoundHorizon
      else if packet.calibrationCurrent = false then .requestCalibration
      else if packet.supportQualified = false then .requestQualifiedSupport
      else if packet.materialDisagreement && packet.disagreementDispositionPresent = false then
        .requestDisagreementDisposition
      else if packet.branchDerivedFromObservation = false then .requestObservationLineage
      else if packet.branchMarkedImagined = false then .requestImaginedLabel
      else .acceptBranch
  | .branchQualified =>
      if packet.plannerUseBounded = false then .requestBoundedPlannerUse
      else .acceptPlanningHandoff
  | .planningHandoff =>
      if packet.actionReceiptPresent = false then .requestActionReceipt
      else if packet.effectIndependentlyObserved = false then .requestIndependentEffectObservation
      else if packet.effectMarkedActual = false then .requestActualityLabel
      else .acceptEffectObservation
  | .effectObserved =>
      if packet.residualComputed = false then .requestResidual
      else if packet.materialResidual && packet.residualResponseSelected = false then
        .requestResidualResponse
      else if packet.residualOwnerPresent = false then .requestResidualOwner
      else .acceptReconciliation

def lifecycleAccepted : LifecycleRoute -> Bool
  | .acceptObservation | .acceptModel | .acceptBranch | .acceptPlanningHandoff
  | .acceptEffectObservation | .acceptReconciliation => true
  | _ => false

def nextLifecycleStage : LifecycleStage -> LifecycleStage
  | .awaitingObservation | .reconciled => .observationBound
  | .observationBound => .modelBound
  | .modelBound => .branchQualified
  | .branchQualified => .planningHandoff
  | .planningHandoff => .effectObserved
  | .effectObserved => .reconciled

def lifecycleStep
    (state : LifecycleState) (kind : LifecycleEventKind)
    (packet : LifecyclePacket) : Option LifecycleState :=
  let route := lifecycleRouteFor state kind packet
  if lifecycleAccepted route then
    some { state with
      stage := nextLifecycleStage state.stage
      lastEventDigest := packet.eventDigest
      receiptCount := state.receiptCount + 1
      planningHandoffCount := state.planningHandoffCount +
        (if kind = .handoffForPlanning then 1 else 0)
      observedEffectCount := state.observedEffectCount +
        (if kind = .recordObservedEffect then 1 else 0)
      reconciliationCount := state.reconciliationCount +
        (if kind = .reconcileResidual then 1 else 0) }
  else none

structure LifecycleEvent where
  kind : LifecycleEventKind
  packet : LifecyclePacket
deriving DecidableEq, Repr

def lifecycleRun : LifecycleState -> List LifecycleEvent -> Option LifecycleState
  | state, [] => some state
  | state, event :: rest =>
      match lifecycleStep state event.kind event.packet with
      | none => none
      | some next => lifecycleRun next rest

theorem rejected_lifecycle_event_preserves_exact_state
    (state : LifecycleState) (kind : LifecycleEventKind) (packet : LifecyclePacket)
    (rejected : lifecycleAccepted (lifecycleRouteFor state kind packet) = false) :
    lifecycleStep state kind packet = none := by
  simp [lifecycleStep, rejected]

theorem accepted_lifecycle_event_adds_one_receipt
    {state next : LifecycleState} {kind : LifecycleEventKind} {packet : LifecyclePacket}
    (accepted : lifecycleStep state kind packet = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  by_cases h : lifecycleAccepted (lifecycleRouteFor state kind packet) = true
  · simp [lifecycleStep, h] at accepted
    subst next
    rfl
  · simp [lifecycleStep, h] at accepted

theorem accepted_lifecycle_event_preserves_identity
    {state next : LifecycleState} {kind : LifecycleEventKind} {packet : LifecyclePacket}
    (accepted : lifecycleStep state kind packet = some next) :
    next.modelIdentity = state.modelIdentity ∧
      next.modelVersion = state.modelVersion ∧
      next.observationDigest = state.observationDigest ∧
      next.branchDigest = state.branchDigest ∧
      next.actionDigest = state.actionDigest ∧
      next.effectDigest = state.effectDigest := by
  by_cases h : lifecycleAccepted (lifecycleRouteFor state kind packet) = true
  · simp [lifecycleStep, h] at accepted
    subst next
    simp
  · simp [lifecycleStep, h] at accepted

theorem lifecycle_event_cannot_assign_support_or_effect_authority
    {state next : LifecycleState} {kind : LifecycleEventKind} {packet : LifecyclePacket}
    (accepted : lifecycleStep state kind packet = some next) :
    next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.effectAuthorityCount = state.effectAuthorityCount := by
  by_cases h : lifecycleAccepted (lifecycleRouteFor state kind packet) = true
  · simp [lifecycleStep, h] at accepted
    subst next
    simp
  · simp [lifecycleStep, h] at accepted

theorem lifecycle_event_preserves_authority_ceiling
    {state next : LifecycleState} {kind : LifecycleEventKind} {packet : LifecyclePacket}
    (accepted : lifecycleStep state kind packet = some next) :
    next.authorityCeiling = state.authorityCeiling := by
  by_cases h : lifecycleAccepted (lifecycleRouteFor state kind packet) = true
  · simp [lifecycleStep, h] at accepted
    subst next
    rfl
  · simp [lifecycleStep, h] at accepted

theorem accepted_planning_handoff_does_not_record_effect
    {state next : LifecycleState} {packet : LifecyclePacket}
    (accepted : lifecycleStep state .handoffForPlanning packet = some next) :
    next.observedEffectCount = state.observedEffectCount := by
  by_cases h : lifecycleAccepted
      (lifecycleRouteFor state .handoffForPlanning packet) = true
  · simp [lifecycleStep, h] at accepted
    subst next
    rfl
  · simp [lifecycleStep, h] at accepted

theorem accepted_effect_record_requires_independent_actuality
    {state next : LifecycleState} {packet : LifecyclePacket}
    (stage : state.stage = .planningHandoff)
    (accepted : lifecycleStep state .recordObservedEffect packet = some next) :
    packet.actionReceiptPresent = true ∧
      packet.effectIndependentlyObserved = true ∧
      packet.effectMarkedActual = true := by
  have routeAccepted : lifecycleAccepted
      (lifecycleRouteFor state .recordObservedEffect packet) = true := by
    cases routed : lifecycleAccepted
        (lifecycleRouteFor state .recordObservedEffect packet) with
    | false => simp [lifecycleStep, routed] at accepted
    | true => rfl
  cases actionReceipt : packet.actionReceiptPresent with
  | false =>
      have rejected : lifecycleAccepted
          (lifecycleRouteFor state .recordObservedEffect packet) = false := by
        by_cases identity : lifecycleIdentityMatches state packet = false <;>
          by_cases replay : packet.eventDigest = state.lastEventDigest <;>
          by_cases leak : packet.supportAssignmentRequested = true ∨
            packet.executionAuthorityRequested = true <;>
          simp [lifecycleRouteFor, stage, expectedLifecycleKind, actionReceipt,
            identity, replay, leak, lifecycleAccepted]
      simp_all
  | true =>
      cases independent : packet.effectIndependentlyObserved with
      | false =>
          have rejected : lifecycleAccepted
              (lifecycleRouteFor state .recordObservedEffect packet) = false := by
            by_cases identity : lifecycleIdentityMatches state packet = false <;>
              by_cases replay : packet.eventDigest = state.lastEventDigest <;>
              by_cases leak : packet.supportAssignmentRequested = true ∨
                packet.executionAuthorityRequested = true <;>
              simp [lifecycleRouteFor, stage, expectedLifecycleKind, actionReceipt,
                independent, identity, replay, leak, lifecycleAccepted]
          simp_all
      | true =>
          cases actuality : packet.effectMarkedActual with
          | false =>
              have rejected : lifecycleAccepted
                  (lifecycleRouteFor state .recordObservedEffect packet) = false := by
                by_cases identity : lifecycleIdentityMatches state packet = false <;>
                  by_cases replay : packet.eventDigest = state.lastEventDigest <;>
                  by_cases leak : packet.supportAssignmentRequested = true ∨
                    packet.executionAuthorityRequested = true <;>
                  simp [lifecycleRouteFor, stage, expectedLifecycleKind, actionReceipt,
                    independent, actuality, identity, replay, leak, lifecycleAccepted]
              simp_all
          | true => exact ⟨rfl, rfl, rfl⟩

theorem successful_lifecycle_run_preserves_identity
    {state final : LifecycleState} {events : List LifecycleEvent}
    (ran : lifecycleRun state events = some final) :
    final.modelIdentity = state.modelIdentity ∧
      final.modelVersion = state.modelVersion ∧
      final.observationDigest = state.observationDigest ∧
      final.branchDigest = state.branchDigest ∧
      final.actionDigest = state.actionDigest ∧
      final.effectDigest = state.effectDigest := by
  induction events generalizing state with
  | nil => simp [lifecycleRun] at ran; simp_all
  | cons event rest ih =>
      cases stepped : lifecycleStep state event.kind event.packet with
      | none => simp [lifecycleRun, stepped] at ran
      | some next =>
          have tailRan : lifecycleRun next rest = some final := by
            simpa [lifecycleRun, stepped] using ran
          have head := accepted_lifecycle_event_preserves_identity stepped
          have tail := ih tailRan
          exact ⟨tail.1.trans head.1,
            tail.2.1.trans head.2.1,
            tail.2.2.1.trans head.2.2.1,
            tail.2.2.2.1.trans head.2.2.2.1,
            tail.2.2.2.2.1.trans head.2.2.2.2.1,
            tail.2.2.2.2.2.trans head.2.2.2.2.2⟩

theorem successful_lifecycle_run_preserves_non_authority
    {state final : LifecycleState} {events : List LifecycleEvent}
    (ran : lifecycleRun state events = some final) :
    final.supportAssignmentCount = state.supportAssignmentCount ∧
      final.effectAuthorityCount = state.effectAuthorityCount := by
  induction events generalizing state with
  | nil => simp [lifecycleRun] at ran; simp_all
  | cons event rest ih =>
      cases stepped : lifecycleStep state event.kind event.packet with
      | none => simp [lifecycleRun, stepped] at ran
      | some next =>
          have tailRan : lifecycleRun next rest = some final := by
            simpa [lifecycleRun, stepped] using ran
          have head := lifecycle_event_cannot_assign_support_or_effect_authority stepped
          have tail := ih tailRan
          exact ⟨tail.1.trans head.1, tail.2.trans head.2⟩

theorem successful_lifecycle_run_preserves_authority_ceiling
    {state final : LifecycleState} {events : List LifecycleEvent}
    (ran : lifecycleRun state events = some final) :
    final.authorityCeiling = state.authorityCeiling := by
  induction events generalizing state with
  | nil => simp [lifecycleRun] at ran; simp_all
  | cons event rest ih =>
      cases stepped : lifecycleStep state event.kind event.packet with
      | none => simp [lifecycleRun, stepped] at ran
      | some next =>
          have tailRan : lifecycleRun next rest = some final := by
            simpa [lifecycleRun, stepped] using ran
          exact (ih tailRan).trans (lifecycle_event_preserves_authority_ceiling stepped)

theorem lifecycle_run_composes_across_event_batches
    (state : LifecycleState) (left right : List LifecycleEvent) :
    lifecycleRun state (left ++ right) =
      match lifecycleRun state left with
      | none => none
      | some middle => lifecycleRun middle right := by
  induction left generalizing state with
  | nil => simp [lifecycleRun]
  | cons event rest ih =>
      cases stepped : lifecycleStep state event.kind event.packet <;>
        simp [lifecycleRun, stepped, ih]

def canonicalLifecycleState : LifecycleState :=
  { stage := .awaitingObservation
    modelIdentity := 401
    modelVersion := 7
    observationDigest := 402
    branchDigest := 403
    actionDigest := 404
    effectDigest := 405
    authorityCeiling := 2
    lastEventDigest := 0
    receiptCount := 0
    planningHandoffCount := 0
    observedEffectCount := 0
    reconciliationCount := 0
    supportAssignmentCount := 0
    effectAuthorityCount := 0 }

def canonicalLifecyclePacket (eventDigest : Nat) : LifecyclePacket :=
  { modelIdentity := 401
    modelVersion := 7
    observationDigest := 402
    branchDigest := 403
    actionDigest := 404
    effectDigest := 405
    authorityCeiling := 2
    eventDigest := eventDigest
    observationAdmitted := true
    observationFresh := true
    observationMarkedActual := true
    modelCheckpointBound := true
    modelCurrent := true
    interventionSemanticsBound := true
    horizonBound := true
    calibrationCurrent := true
    supportQualified := true
    materialDisagreement := false
    disagreementDispositionPresent := true
    branchDerivedFromObservation := true
    branchMarkedImagined := true
    plannerUseBounded := true
    actionReceiptPresent := true
    effectIndependentlyObserved := true
    effectMarkedActual := true
    residualComputed := true
    materialResidual := true
    residualResponseSelected := true
    residualOwnerPresent := true
    supportAssignmentRequested := false
    executionAuthorityRequested := false }

def lifecycleEvent (kind : LifecycleEventKind) (digest : Nat) : LifecycleEvent :=
  { kind := kind, packet := canonicalLifecyclePacket digest }

def canonicalLifecycle : List LifecycleEvent :=
  [ lifecycleEvent .bindObservation 1,
    lifecycleEvent .bindModel 2,
    lifecycleEvent .qualifyBranch 3,
    lifecycleEvent .handoffForPlanning 4,
    lifecycleEvent .recordObservedEffect 5,
    lifecycleEvent .reconcileResidual 6 ]

theorem complete_world_model_lifecycle_reconciles_without_authority :
    lifecycleRun canonicalLifecycleState canonicalLifecycle = some
      { canonicalLifecycleState with
        stage := .reconciled
        lastEventDigest := 6
        receiptCount := 6
        planningHandoffCount := 1
        observedEffectCount := 1
        reconciliationCount := 1 } := by native_decide

theorem stale_observation_blocks_lifecycle :
    lifecycleRouteFor canonicalLifecycleState .bindObservation
      { canonicalLifecyclePacket 1 with observationFresh := false } =
        .requestFreshObservation := by native_decide

theorem imagined_branch_cannot_launder_as_observation :
    lifecycleRouteFor canonicalLifecycleState .bindObservation
      { canonicalLifecyclePacket 1 with observationMarkedActual := false } =
        .rejectImaginationAsObservation := by native_decide

theorem stale_model_blocks_lifecycle :
    let state := { canonicalLifecycleState with stage := .observationBound }
    lifecycleRouteFor state .bindModel
      { canonicalLifecyclePacket 2 with modelCurrent := false } = .requestCurrentModel := by
  native_decide

theorem unsupported_branch_blocks_qualification :
    let state := { canonicalLifecycleState with stage := .modelBound }
    lifecycleRouteFor state .qualifyBranch
      { canonicalLifecyclePacket 3 with supportQualified := false } =
        .requestQualifiedSupport := by native_decide

theorem unresolved_model_disagreement_blocks_qualification :
    let state := { canonicalLifecycleState with stage := .modelBound }
    lifecycleRouteFor state .qualifyBranch
      { { canonicalLifecyclePacket 3 with materialDisagreement := true } with
        disagreementDispositionPresent := false } = .requestDisagreementDisposition := by
  native_decide

theorem unbounded_planner_use_blocks_handoff :
    let state := { canonicalLifecycleState with stage := .branchQualified }
    lifecycleRouteFor state .handoffForPlanning
      { canonicalLifecyclePacket 4 with plannerUseBounded := false } =
        .requestBoundedPlannerUse := by native_decide

theorem planning_handoff_cannot_launder_execution_authority :
    let state := { canonicalLifecycleState with stage := .branchQualified }
    lifecycleRouteFor state .handoffForPlanning
      { canonicalLifecyclePacket 4 with executionAuthorityRequested := true } =
        .rejectAuthorityLaundering := by native_decide

theorem missing_action_receipt_blocks_effect_record :
    let state := { canonicalLifecycleState with stage := .planningHandoff }
    lifecycleRouteFor state .recordObservedEffect
      { canonicalLifecyclePacket 5 with actionReceiptPresent := false } =
        .requestActionReceipt := by native_decide

theorem self_observed_effect_blocks_actuality_record :
    let state := { canonicalLifecycleState with stage := .planningHandoff }
    lifecycleRouteFor state .recordObservedEffect
      { canonicalLifecyclePacket 5 with effectIndependentlyObserved := false } =
        .requestIndependentEffectObservation := by native_decide

theorem missing_residual_blocks_reconciliation :
    let state := { canonicalLifecycleState with stage := .effectObserved }
    lifecycleRouteFor state .reconcileResidual
      { canonicalLifecyclePacket 6 with residualComputed := false } = .requestResidual := by
  native_decide

theorem unowned_residual_blocks_reconciliation :
    let state := { canonicalLifecycleState with stage := .effectObserved }
    lifecycleRouteFor state .reconcileResidual
      { canonicalLifecyclePacket 6 with residualOwnerPresent := false } =
        .requestResidualOwner := by native_decide

end AsiStackProofs.GovernedWorldModels
