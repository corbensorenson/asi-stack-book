namespace AsiStackProofs.HumanFactorsOversight

/-!
A finite routing model for necessary operational conditions of an assigned
human-control role. Every field is an authored record predicate. The model does
not measure cognition, establish moral responsibility, validate consent, prove
intervention efficacy, or decide that control is meaningful.
-/

inductive ControlRoute where
  | boundedReview
  | addCapacity
  | reduceAutonomy
  | safeHold
  | rejectResponsibility
  | rejectAuthorityLeak
deriving DecidableEq, Repr

structure ControlEnvelope where
  controllerIdentified : Bool
  taskAuthorityPresent : Bool
  evidenceObservable : Bool
  representationCompatible : Bool
  comprehensionDispositionPresent : Bool
  workloadInsideBound : Bool
  decisionWindowPositive : Bool
  interventionChannelReachable : Bool
  systemResponseInsideWindow : Bool
  safeStateReachable : Bool
  conflictManaged : Bool
  responsibilityInsideEffectiveControl : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

def ControlRouteFor (packet : ControlEnvelope) : ControlRoute :=
  if packet.supportAssignmentRequested = true ∨
      packet.externalEffectRequested = true then
    .rejectAuthorityLeak
  else if packet.controllerIdentified = false ∨
      packet.taskAuthorityPresent = false then
    .safeHold
  else if packet.responsibilityInsideEffectiveControl = false then
    .rejectResponsibility
  else if packet.evidenceObservable = false ∨
      packet.representationCompatible = false ∨
      packet.comprehensionDispositionPresent = false ∨
      packet.workloadInsideBound = false ∨
      packet.conflictManaged = false then
    .addCapacity
  else if packet.decisionWindowPositive = false ∨
      packet.interventionChannelReachable = false ∨
      packet.systemResponseInsideWindow = false then
    .reduceAutonomy
  else if packet.safeStateReachable = false then
    .safeHold
  else
    .boundedReview

theorem control_route_never_grants_support_or_effect
    (packet : ControlEnvelope) :
    ControlRouteFor packet = .boundedReview ->
    packet.supportAssignmentRequested = false ∧
    packet.externalEffectRequested = false := by
  intro admitted
  unfold ControlRouteFor at admitted
  split at admitted <;> simp_all

theorem control_envelope_blocks_action
    (packet : ControlEnvelope)
    (missing :
      packet.taskAuthorityPresent = false ∨
      packet.evidenceObservable = false ∨
      packet.representationCompatible = false ∨
      packet.comprehensionDispositionPresent = false ∨
      packet.workloadInsideBound = false ∨
      packet.decisionWindowPositive = false ∨
      packet.interventionChannelReachable = false ∨
      packet.systemResponseInsideWindow = false ∨
      packet.safeStateReachable = false ∨
      packet.conflictManaged = false) :
    ControlRouteFor packet ≠ .boundedReview := by
  unfold ControlRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all

theorem responsibility_requires_control
    (packet : ControlEnvelope)
    (exceeds : packet.responsibilityInsideEffectiveControl = false) :
    ControlRouteFor packet ≠ .boundedReview := by
  unfold ControlRouteFor
  split <;> simp_all
  split <;> simp_all

theorem bounded_review_preserves_declared_conditions
    (packet : ControlEnvelope)
    (admitted : ControlRouteFor packet = .boundedReview) :
    packet.controllerIdentified = true ∧
    packet.taskAuthorityPresent = true ∧
    packet.evidenceObservable = true ∧
    packet.representationCompatible = true ∧
    packet.comprehensionDispositionPresent = true ∧
    packet.workloadInsideBound = true ∧
    packet.decisionWindowPositive = true ∧
    packet.interventionChannelReachable = true ∧
    packet.systemResponseInsideWindow = true ∧
    packet.safeStateReachable = true ∧
    packet.conflictManaged = true ∧
    packet.responsibilityInsideEffectiveControl = true ∧
    packet.supportAssignmentRequested = false ∧
    packet.externalEffectRequested = false := by
  unfold ControlRouteFor at admitted
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  split at admitted <;> simp_all

def completeEnvelope : ControlEnvelope where
  controllerIdentified := true
  taskAuthorityPresent := true
  evidenceObservable := true
  representationCompatible := true
  comprehensionDispositionPresent := true
  workloadInsideBound := true
  decisionWindowPositive := true
  interventionChannelReachable := true
  systemResponseInsideWindow := true
  safeStateReachable := true
  conflictManaged := true
  responsibilityInsideEffectiveControl := true
  supportAssignmentRequested := false
  externalEffectRequested := false

def overloadedEnvelope : ControlEnvelope :=
  { completeEnvelope with workloadInsideBound := false }

def lateEnvelope : ControlEnvelope :=
  { completeEnvelope with systemResponseInsideWindow := false }

def blameWithoutControlEnvelope : ControlEnvelope :=
  { completeEnvelope with responsibilityInsideEffectiveControl := false }

def authorityLeakEnvelope : ControlEnvelope :=
  { completeEnvelope with supportAssignmentRequested := true }

theorem complete_fixture_routes_to_bounded_review :
    ControlRouteFor completeEnvelope = .boundedReview := by native_decide

theorem overloaded_fixture_requests_capacity :
    ControlRouteFor overloadedEnvelope = .addCapacity := by native_decide

theorem late_fixture_reduces_autonomy :
    ControlRouteFor lateEnvelope = .reduceAutonomy := by native_decide

theorem blame_without_control_is_rejected :
    ControlRouteFor blameWithoutControlEnvelope = .rejectResponsibility := by native_decide

theorem authority_leak_is_rejected :
    ControlRouteFor authorityLeakEnvelope = .rejectAuthorityLeak := by native_decide

/-!
The lifecycle below strengthens the admission router with temporal and identity
custody. It still treats every human-state and world-facing field as authored
input. In particular, an acknowledgement is not a proof of comprehension and a
response receipt is not a proof that an intervention was effective.
-/

inductive ReviewStage where
  | proposed
  | briefed
  | decided
  | intervened
  | responseObserved
  | accountabilityClosed
  | blocked
deriving DecidableEq, Repr

structure ReviewState where
  stage : ReviewStage
  oversightId : Nat
  reviewerId : Nat
  actionId : Nat
  decisionId : Nat
  authorityCeiling : Nat
  activeAuthority : Nat
  controlOpportunities : Nat
  decisions : Nat
  interventions : Nat
  responseReceipts : Nat
  accountabilityClosures : Nat
  supportAssignments : Nat
  releaseAuthorizations : Nat
  residuals : Nat
deriving DecidableEq, Repr

inductive ReviewEvent where
  | brief
      (oversightId reviewerId actionId decisionId : Nat)
      (controllerIdentified taskAuthorityPresent evidenceObservable : Bool)
      (representationCompatible comprehensionDispositionPresent : Bool)
      (workloadInsideBound decisionWindowPositive : Bool)
      (interventionChannelReachable safeStateReachable conflictManaged : Bool)
  | decide
      (oversightId reviewerId actionId decisionId : Nat)
      (requestedAuthority : Nat)
      (insideDecisionWindow comprehensionAcknowledged : Bool)
      (independentChallengeAvailable overridePathExercisable : Bool)
  | intervene
      (oversightId reviewerId actionId decisionId : Nat)
      (usedAuthority : Nat)
      (interventionReceiptPresent : Bool)
  | observeResponse
      (oversightId reviewerId actionId decisionId : Nat)
      (responseReceiptPresent : Bool)
  | closeAccountability
      (oversightId reviewerId actionId decisionId : Nat)
      (controlOpportunityRecorded responseObserved : Bool)
  | block
      (oversightId reviewerId actionId decisionId : Nat)
      (residualRecorded : Bool)
deriving DecidableEq, Repr

def initialReviewState : ReviewState where
  stage := .proposed
  oversightId := 41
  reviewerId := 7
  actionId := 19
  decisionId := 23
  authorityCeiling := 3
  activeAuthority := 0
  controlOpportunities := 0
  decisions := 0
  interventions := 0
  responseReceipts := 0
  accountabilityClosures := 0
  supportAssignments := 0
  releaseAuthorizations := 0
  residuals := 0

def ReviewStep (state : ReviewState) (event : ReviewEvent) : Option ReviewState :=
  match event with
  | .brief oversightId reviewerId actionId decisionId controllerIdentified
      taskAuthorityPresent evidenceObservable representationCompatible
      comprehensionDispositionPresent workloadInsideBound decisionWindowPositive
      interventionChannelReachable safeStateReachable conflictManaged =>
      if state.stage = .proposed ∧
          oversightId = state.oversightId ∧ reviewerId = state.reviewerId ∧
          actionId = state.actionId ∧ decisionId = state.decisionId ∧
          controllerIdentified = true ∧ taskAuthorityPresent = true ∧
          evidenceObservable = true ∧ representationCompatible = true ∧
          comprehensionDispositionPresent = true ∧ workloadInsideBound = true ∧
          decisionWindowPositive = true ∧ interventionChannelReachable = true ∧
          safeStateReachable = true ∧ conflictManaged = true then
        some { state with stage := .briefed, controlOpportunities := 1 }
      else none
  | .decide oversightId reviewerId actionId decisionId requestedAuthority
      insideDecisionWindow comprehensionAcknowledged independentChallengeAvailable
      overridePathExercisable =>
      if state.stage = .briefed ∧
          oversightId = state.oversightId ∧ reviewerId = state.reviewerId ∧
          actionId = state.actionId ∧ decisionId = state.decisionId ∧
          requestedAuthority ≤ state.authorityCeiling ∧
          insideDecisionWindow = true ∧ comprehensionAcknowledged = true ∧
          independentChallengeAvailable = true ∧ overridePathExercisable = true then
        some { state with
          stage := .decided
          activeAuthority := requestedAuthority
          decisions := 1 }
      else none
  | .intervene oversightId reviewerId actionId decisionId usedAuthority
      interventionReceiptPresent =>
      if state.stage = .decided ∧
          oversightId = state.oversightId ∧ reviewerId = state.reviewerId ∧
          actionId = state.actionId ∧ decisionId = state.decisionId ∧
          usedAuthority ≤ state.activeAuthority ∧ interventionReceiptPresent = true then
        some { state with stage := .intervened, interventions := 1 }
      else none
  | .observeResponse oversightId reviewerId actionId decisionId responseReceiptPresent =>
      if state.stage = .intervened ∧
          oversightId = state.oversightId ∧ reviewerId = state.reviewerId ∧
          actionId = state.actionId ∧ decisionId = state.decisionId ∧
          responseReceiptPresent = true then
        some { state with stage := .responseObserved, responseReceipts := 1 }
      else none
  | .closeAccountability oversightId reviewerId actionId decisionId
      controlOpportunityRecorded responseObserved =>
      if state.stage = .responseObserved ∧
          oversightId = state.oversightId ∧ reviewerId = state.reviewerId ∧
          actionId = state.actionId ∧ decisionId = state.decisionId ∧
          controlOpportunityRecorded = true ∧ responseObserved = true then
        some { state with
          stage := .accountabilityClosed
          accountabilityClosures := 1 }
      else none
  | .block oversightId reviewerId actionId decisionId residualRecorded =>
      if oversightId = state.oversightId ∧ reviewerId = state.reviewerId ∧
          actionId = state.actionId ∧ decisionId = state.decisionId ∧
          residualRecorded = true then
        some { state with
          stage := .blocked
          activeAuthority := 0
          residuals := state.residuals + 1 }
      else none

def ReviewInvariant (state : ReviewState) : Prop :=
  state.activeAuthority ≤ state.authorityCeiling ∧
  state.decisions ≤ state.controlOpportunities ∧
  state.interventions ≤ state.decisions ∧
  state.responseReceipts ≤ state.interventions ∧
  state.accountabilityClosures ≤ state.responseReceipts ∧
  state.supportAssignments = 0 ∧
  state.releaseAuthorizations = 0 ∧
  (state.stage = .proposed ->
    state.controlOpportunities = 0 ∧ state.decisions = 0 ∧
    state.interventions = 0 ∧ state.responseReceipts = 0 ∧
    state.accountabilityClosures = 0) ∧
  (state.stage = .briefed ->
    state.controlOpportunities = 1 ∧ state.decisions = 0 ∧
    state.interventions = 0 ∧ state.responseReceipts = 0 ∧
    state.accountabilityClosures = 0) ∧
  (state.stage = .decided ->
    state.controlOpportunities = 1 ∧ state.decisions = 1 ∧
    state.interventions = 0 ∧ state.responseReceipts = 0 ∧
    state.accountabilityClosures = 0) ∧
  (state.stage = .intervened ->
    state.controlOpportunities = 1 ∧ state.decisions = 1 ∧
    state.interventions = 1 ∧ state.responseReceipts = 0 ∧
    state.accountabilityClosures = 0) ∧
  (state.stage = .responseObserved ->
    state.controlOpportunities = 1 ∧ state.decisions = 1 ∧
    state.interventions = 1 ∧ state.responseReceipts = 1 ∧
    state.accountabilityClosures = 0) ∧
  (state.stage = .accountabilityClosed ->
    state.controlOpportunities = 1 ∧ state.decisions = 1 ∧
    state.interventions = 1 ∧ state.responseReceipts = 1 ∧
    state.accountabilityClosures = 1) ∧
  (state.stage = .blocked -> state.activeAuthority = 0)

def ReviewRun : ReviewState -> List ReviewEvent -> Option ReviewState
  | state, [] => some state
  | state, event :: rest =>
      match ReviewStep state event with
      | none => none
      | some next => ReviewRun next rest

theorem initial_review_state_satisfies_invariant :
    ReviewInvariant initialReviewState := by
  simp [ReviewInvariant, initialReviewState]

theorem accepted_review_step_preserves_invariant
    (state next : ReviewState) (event : ReviewEvent)
    (safe : ReviewInvariant state)
    (accepted : ReviewStep state event = some next) :
    ReviewInvariant next := by
  cases event <;> simp [ReviewStep] at accepted
  all_goals rcases accepted with ⟨_, rfl⟩
  all_goals simp_all [ReviewInvariant]

theorem accepted_review_step_preserves_custody
    (state next : ReviewState) (event : ReviewEvent)
    (accepted : ReviewStep state event = some next) :
    next.oversightId = state.oversightId ∧
    next.reviewerId = state.reviewerId ∧
    next.actionId = state.actionId ∧
    next.decisionId = state.decisionId ∧
    next.authorityCeiling = state.authorityCeiling := by
  cases event <;> simp [ReviewStep] at accepted
  all_goals rcases accepted with ⟨_, rfl⟩ <;> simp

theorem accepted_review_run_preserves_invariant
    (state next : ReviewState) (events : List ReviewEvent)
    (safe : ReviewInvariant state)
    (accepted : ReviewRun state events = some next) :
    ReviewInvariant next := by
  induction events generalizing state with
  | nil => simp [ReviewRun] at accepted; simpa [accepted] using safe
  | cons event rest ih =>
      simp [ReviewRun] at accepted
      split at accepted
      · contradiction
      · rename_i intermediate step
        exact ih intermediate (accepted_review_step_preserves_invariant state intermediate event safe step) accepted

theorem accepted_review_run_preserves_custody
    (state next : ReviewState) (events : List ReviewEvent)
    (accepted : ReviewRun state events = some next) :
    next.oversightId = state.oversightId ∧
    next.reviewerId = state.reviewerId ∧
    next.actionId = state.actionId ∧
    next.decisionId = state.decisionId ∧
    next.authorityCeiling = state.authorityCeiling := by
  induction events generalizing state with
  | nil => simp [ReviewRun] at accepted; simp [accepted]
  | cons event rest ih =>
      simp [ReviewRun] at accepted
      split at accepted
      · contradiction
      · rename_i intermediate step
        have head := accepted_review_step_preserves_custody state intermediate event step
        have tail := ih intermediate accepted
        rcases head with ⟨hOversight, hReviewer, hAction, hDecision, hCeiling⟩
        rcases tail with ⟨tOversight, tReviewer, tAction, tDecision, tCeiling⟩
        exact ⟨tOversight.trans hOversight, tReviewer.trans hReviewer,
          tAction.trans hAction, tDecision.trans hDecision,
          tCeiling.trans hCeiling⟩

theorem reachable_accountability_requires_control_decision_intervention_and_response
    (state : ReviewState) (events : List ReviewEvent)
    (reached : ReviewRun initialReviewState events = some state)
    (closed : state.stage = .accountabilityClosed) :
    state.controlOpportunities = 1 ∧ state.decisions = 1 ∧
    state.interventions = 1 ∧ state.responseReceipts = 1 ∧
    state.accountabilityClosures = 1 := by
  have safe := accepted_review_run_preserves_invariant initialReviewState state events
    initial_review_state_satisfies_invariant reached
  rcases safe with ⟨_, _, _, _, _, _, _, _, _, _, _, _, ancestry, _⟩
  exact ancestry closed

theorem reachable_review_authority_never_exceeds_ceiling
    (state : ReviewState) (events : List ReviewEvent)
    (reached : ReviewRun initialReviewState events = some state) :
    state.activeAuthority ≤ state.authorityCeiling := by
  exact (accepted_review_run_preserves_invariant initialReviewState state events
    initial_review_state_satisfies_invariant reached).1

theorem reachable_review_never_assigns_support_or_release_authority
    (state : ReviewState) (events : List ReviewEvent)
    (reached : ReviewRun initialReviewState events = some state) :
    state.supportAssignments = 0 ∧ state.releaseAuthorizations = 0 := by
  have safe := accepted_review_run_preserves_invariant initialReviewState state events
    initial_review_state_satisfies_invariant reached
  exact ⟨safe.2.2.2.2.2.1, safe.2.2.2.2.2.2.1⟩

def completeReviewTrace : List ReviewEvent := [
  .brief 41 7 19 23 true true true true true true true true true true,
  .decide 41 7 19 23 2 true true true true,
  .intervene 41 7 19 23 2 true,
  .observeResponse 41 7 19 23 true,
  .closeAccountability 41 7 19 23 true true
]

theorem complete_review_trace_reaches_accountability_closure :
    ReviewRun initialReviewState completeReviewTrace = some {
      initialReviewState with
        stage := .accountabilityClosed
        activeAuthority := 2
        controlOpportunities := 1
        decisions := 1
        interventions := 1
        responseReceipts := 1
        accountabilityClosures := 1 } := by native_decide

def briefedReviewState : ReviewState :=
  { initialReviewState with stage := .briefed, controlOpportunities := 1 }

def decidedReviewState : ReviewState :=
  { briefedReviewState with stage := .decided, activeAuthority := 2, decisions := 1 }

def intervenedReviewState : ReviewState :=
  { decidedReviewState with stage := .intervened, interventions := 1 }

def observedReviewState : ReviewState :=
  { intervenedReviewState with stage := .responseObserved, responseReceipts := 1 }

theorem substituted_reviewer_is_rejected_before_briefing :
    ReviewStep initialReviewState
      (.brief 41 8 19 23 true true true true true true true true true true) = none := by
  native_decide

theorem substituted_action_is_rejected_before_briefing :
    ReviewStep initialReviewState
      (.brief 41 7 20 23 true true true true true true true true true true) = none := by
  native_decide

theorem overloaded_review_is_rejected_before_control_opportunity :
    ReviewStep initialReviewState
      (.brief 41 7 19 23 true true true true true false true true true true) = none := by
  native_decide

theorem late_review_is_rejected_before_control_opportunity :
    ReviewStep initialReviewState
      (.brief 41 7 19 23 true true true true true true false true true true) = none := by
  native_decide

theorem missing_comprehension_acknowledgement_is_rejected_before_decision :
    ReviewStep briefedReviewState (.decide 41 7 19 23 2 true false true true) = none := by
  native_decide

theorem missing_independent_challenge_is_rejected_before_decision :
    ReviewStep briefedReviewState (.decide 41 7 19 23 2 true true false true) = none := by
  native_decide

theorem missing_override_path_is_rejected_before_decision :
    ReviewStep briefedReviewState (.decide 41 7 19 23 2 true true true false) = none := by
  native_decide

theorem authority_widening_is_rejected_before_decision :
    ReviewStep briefedReviewState (.decide 41 7 19 23 4 true true true true) = none := by
  native_decide

theorem intervention_before_decision_is_rejected :
    ReviewStep briefedReviewState (.intervene 41 7 19 23 2 true) = none := by
  native_decide

theorem intervention_without_receipt_is_rejected :
    ReviewStep decidedReviewState (.intervene 41 7 19 23 2 false) = none := by
  native_decide

theorem response_observation_before_intervention_is_rejected :
    ReviewStep decidedReviewState (.observeResponse 41 7 19 23 true) = none := by
  native_decide

theorem accountability_without_observed_response_is_rejected :
    ReviewStep intervenedReviewState
      (.closeAccountability 41 7 19 23 true true) = none := by
  native_decide

theorem accountability_without_control_opportunity_is_rejected :
    ReviewStep observedReviewState
      (.closeAccountability 41 7 19 23 false true) = none := by
  native_decide

theorem blocked_review_revokes_active_authority_without_support_effect :
    ReviewStep decidedReviewState (.block 41 7 19 23 true) = some {
      decidedReviewState with stage := .blocked, activeAuthority := 0, residuals := 1 } := by
  native_decide

end AsiStackProofs.HumanFactorsOversight
