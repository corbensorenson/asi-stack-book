namespace AsiStackProofs.VerificationBandwidthRefinement

inductive VerificationStage where
  | proposed
  | frozen
  | executed
  | adjudicated
  | handedOff
deriving DecidableEq, Repr

inductive RiskTier where
  | low
  | medium
  | high
  | critical
deriving DecidableEq, Repr

inductive RequestedEffect where
  | draftingOnly
  | evidenceReview
  | promoteChapterCore
deriving DecidableEq, Repr

inductive AdequacyRoute where
  | rejectMalformed
  | requestContext
  | requireObligationPlan
  | blockUnauthorizedPromotion
  | blockInconsistentCounts
  | blockContradiction
  | recordResidual
  | requireIndependentEvaluator
  | requireNegativeSearch
  | requireArtifacts
  | allowDraft
  | handoffToEvidenceGate
deriving DecidableEq, Repr

structure VerificationPlan where
  planId : Nat
  claimId : Nat
  claimVersion : Nat
  packetDigest : Nat
  packetAdmitted : Bool
  transactionValid : Bool
  riskTier : RiskTier
  requestedEffect : RequestedEffect
  obligationCount : Nat
  authorityValid : Bool
  rightsValid : Bool
  budgetDeclared : Bool
  horizonDeclared : Bool
  stopRuleDeclared : Bool
deriving DecidableEq, Repr

structure VerificationExecution where
  planId : Nat
  claimId : Nat
  claimVersion : Nat
  packetDigest : Nat
  passed : Nat
  failed : Nat
  contradicted : Nat
  disputed : Nat
  unknown : Nat
  infeasible : Nat
  blocked : Nat
  unattempted : Nat
  negativeSearchAttempted : Bool
  independentEvaluator : Bool
  verificationArtifactsPresent : Bool
  residualsRecorded : Bool
  expiryDeclared : Bool
deriving DecidableEq, Repr

def AttemptedCount (execution : VerificationExecution) : Nat :=
  execution.passed + execution.failed + execution.contradicted +
    execution.disputed + execution.unknown

def DispositionCount (execution : VerificationExecution) : Nat :=
  AttemptedCount execution + execution.infeasible + execution.blocked +
    execution.unattempted

def PlanValid (plan : VerificationPlan) : Prop :=
  plan.planId > 0 ∧
    plan.claimId > 0 ∧
    plan.claimVersion > 0 ∧
    plan.packetDigest > 0 ∧
    plan.packetAdmitted = true ∧
    plan.transactionValid = true ∧
    plan.obligationCount > 0 ∧
    plan.authorityValid = true ∧
    plan.rightsValid = true ∧
    plan.budgetDeclared = true ∧
    plan.horizonDeclared = true ∧
    plan.stopRuleDeclared = true

instance planValidDecidable (plan : VerificationPlan) : Decidable (PlanValid plan) := by
  unfold PlanValid
  infer_instance

def ExecutionBoundToPlan
    (plan : VerificationPlan) (execution : VerificationExecution) : Bool :=
  execution.planId == plan.planId &&
    execution.claimId == plan.claimId &&
    execution.claimVersion == plan.claimVersion &&
    execution.packetDigest == plan.packetDigest

def ExecutionValid
    (plan : VerificationPlan) (execution : VerificationExecution) : Prop :=
  ExecutionBoundToPlan plan execution = true ∧
    DispositionCount execution = plan.obligationCount ∧
    execution.expiryDeclared = true ∧
    ((execution.failed + execution.contradicted + execution.disputed +
      execution.unknown + execution.infeasible + execution.blocked +
      execution.unattempted > 0) -> execution.residualsRecorded = true)

instance executionValidDecidable
    (plan : VerificationPlan) (execution : VerificationExecution) :
    Decidable (ExecutionValid plan execution) := by
  unfold ExecutionValid
  infer_instance

def HighRisk (risk : RiskTier) : Bool :=
  match risk with
  | RiskTier.high => true
  | RiskTier.critical => true
  | _ => false

def OpenDispositionCount (execution : VerificationExecution) : Nat :=
  execution.failed + execution.disputed + execution.unknown +
    execution.infeasible + execution.blocked + execution.unattempted

def VerificationRouteFor
    (plan : VerificationPlan) (execution : VerificationExecution) : AdequacyRoute :=
  if plan.planId = 0 ∨ plan.claimId = 0 ∨ plan.claimVersion = 0 ∨
      plan.packetDigest = 0 then
    AdequacyRoute.rejectMalformed
  else if plan.packetAdmitted = false ∨ plan.transactionValid = false then
    AdequacyRoute.requestContext
  else if plan.obligationCount = 0 then
    AdequacyRoute.requireObligationPlan
  else if plan.authorityValid = false ∨ plan.rightsValid = false ∨
      plan.budgetDeclared = false ∨ plan.horizonDeclared = false ∨
      plan.stopRuleDeclared = false then
    AdequacyRoute.rejectMalformed
  else if plan.requestedEffect = RequestedEffect.promoteChapterCore then
    AdequacyRoute.blockUnauthorizedPromotion
  else if ExecutionBoundToPlan plan execution = false ∨
      DispositionCount execution ≠ plan.obligationCount ∨
      execution.expiryDeclared = false then
    AdequacyRoute.blockInconsistentCounts
  else if execution.contradicted > 0 then
    AdequacyRoute.blockContradiction
  else if OpenDispositionCount execution > 0 then
    AdequacyRoute.recordResidual
  else if HighRisk plan.riskTier = true ∧
      execution.independentEvaluator = false then
    AdequacyRoute.requireIndependentEvaluator
  else if execution.negativeSearchAttempted = false then
    AdequacyRoute.requireNegativeSearch
  else if execution.verificationArtifactsPresent = false then
    AdequacyRoute.requireArtifacts
  else if plan.requestedEffect = RequestedEffect.evidenceReview then
    AdequacyRoute.handoffToEvidenceGate
  else
    AdequacyRoute.allowDraft

inductive Reachable
    (plan : VerificationPlan) (execution : VerificationExecution) :
    VerificationStage -> Prop where
  | proposed : Reachable plan execution VerificationStage.proposed
  | frozen :
      Reachable plan execution VerificationStage.proposed ->
      PlanValid plan ->
      Reachable plan execution VerificationStage.frozen
  | executed :
      Reachable plan execution VerificationStage.frozen ->
      ExecutionValid plan execution ->
      Reachable plan execution VerificationStage.executed
  | adjudicated :
      Reachable plan execution VerificationStage.executed ->
      Reachable plan execution VerificationStage.adjudicated
  | handedOff :
      Reachable plan execution VerificationStage.adjudicated ->
      Reachable plan execution VerificationStage.handedOff

/-!
The route classifier above says which disposition is required for one authored
plan/execution pair. The transaction below adds the missing temporal contract:
the plan is frozen before execution, the exact execution is recorded before
adjudication, and adjudication must select the evidence gate before handoff.
No event can assign chapter support or external-effect authority.
-/

inductive VerificationEventKind where
  | freezePlan
  | recordExecution
  | adjudicate
  | handoff
deriving DecidableEq, Repr

structure VerificationState where
  stage : VerificationStage
  plan : VerificationPlan
  execution : VerificationExecution
  authorityCeiling : Nat
  planFreezeReceipt : Bool
  executionReceipt : Bool
  adjudicationReceipt : Bool
  evidenceGateReceipt : Bool
  supportAuthority : Bool
  externalEffectAuthority : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure VerificationEvent where
  kind : VerificationEventKind
  fromStage : VerificationStage
  toStage : VerificationStage
  planId : Nat
  claimId : Nat
  claimVersion : Nat
  packetDigest : Nat
  authorityCeiling : Nat
  execution : VerificationExecution
  planFreezeReceipt : Bool
  executionReceipt : Bool
  adjudicationReceipt : Bool
  evidenceGateReceipt : Bool
  supportPromotionRequested : Bool
  externalEffectRequested : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def VerificationIdentity (state : VerificationState) : Nat × Nat × Nat × Nat × Nat :=
  (state.plan.planId, state.plan.claimId, state.plan.claimVersion,
    state.plan.packetDigest, state.authorityCeiling)

def VerificationEventIdentityMatches
    (state : VerificationState) (event : VerificationEvent) : Prop :=
  event.planId = state.plan.planId ∧
    event.claimId = state.plan.claimId ∧
    event.claimVersion = state.plan.claimVersion ∧
    event.packetDigest = state.plan.packetDigest ∧
    event.authorityCeiling = state.authorityCeiling

def VerificationEventSpecificValid
    (state : VerificationState) (event : VerificationEvent) : Bool :=
  match event.kind with
  | .freezePlan =>
      decide (event.fromStage = .proposed) && decide (event.toStage = .frozen) &&
        decide (PlanValid state.plan) && event.planFreezeReceipt &&
        !event.supportPromotionRequested && !event.externalEffectRequested
  | .recordExecution =>
      decide (event.fromStage = .frozen) && decide (event.toStage = .executed) &&
        state.planFreezeReceipt && decide (ExecutionValid state.plan event.execution) &&
        event.executionReceipt && !event.supportPromotionRequested &&
        !event.externalEffectRequested
  | .adjudicate =>
      decide (event.fromStage = .executed) && decide (event.toStage = .adjudicated) &&
        state.planFreezeReceipt && state.executionReceipt &&
        decide (event.execution = state.execution) &&
        decide (VerificationRouteFor state.plan state.execution =
          AdequacyRoute.handoffToEvidenceGate) && event.adjudicationReceipt &&
        !event.supportPromotionRequested && !event.externalEffectRequested
  | .handoff =>
      decide (event.fromStage = .adjudicated) && decide (event.toStage = .handedOff) &&
        state.planFreezeReceipt && state.executionReceipt &&
        state.adjudicationReceipt && decide (event.execution = state.execution) &&
        event.evidenceGateReceipt && !event.supportPromotionRequested &&
        !event.externalEffectRequested

def VerificationEventValid
    (state : VerificationState) (event : VerificationEvent) : Prop :=
  state.stage = event.fromStage ∧
    state.logicalTime < event.logicalTime ∧
    VerificationEventIdentityMatches state event ∧
    VerificationEventSpecificValid state event = true

instance verificationEventValidDecidable
    (state : VerificationState) (event : VerificationEvent) :
    Decidable (VerificationEventValid state event) := by
  unfold VerificationEventValid VerificationEventIdentityMatches
  infer_instance

def ApplyVerificationEvent
    (state : VerificationState) (event : VerificationEvent) : VerificationState :=
  { state with
    stage := event.toStage
    execution := if event.kind = .recordExecution then event.execution else state.execution
    planFreezeReceipt := state.planFreezeReceipt || event.planFreezeReceipt
    executionReceipt := state.executionReceipt || event.executionReceipt
    adjudicationReceipt := state.adjudicationReceipt || event.adjudicationReceipt
    evidenceGateReceipt := state.evidenceGateReceipt || event.evidenceGateReceipt
    logicalTime := event.logicalTime }

def VerificationStep
    (state : VerificationState) (event : VerificationEvent) : Option VerificationState :=
  if VerificationEventValid state event then
    some (ApplyVerificationEvent state event)
  else
    none

def VerificationRun :
    VerificationState -> List VerificationEvent -> Option VerificationState
  | state, [] => some state
  | state, event :: tail =>
      match VerificationStep state event with
      | none => none
      | some next => VerificationRun next tail

def VerificationTraceValid : VerificationState -> List VerificationEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      VerificationEventValid state event ∧
        VerificationTraceValid (ApplyVerificationEvent state event) tail

def CompleteVerificationCustody (state : VerificationState) : Prop :=
  state.planFreezeReceipt = true ∧ state.executionReceipt = true ∧
    state.adjudicationReceipt = true ∧ state.evidenceGateReceipt = true

theorem accepted_verification_step_is_valid
    {state next : VerificationState} {event : VerificationEvent}
    (accepted : VerificationStep state event = some next) :
    VerificationEventValid state event := by
  unfold VerificationStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_verification_step_applies_event
    {state next : VerificationState} {event : VerificationEvent}
    (accepted : VerificationStep state event = some next) :
    next = ApplyVerificationEvent state event := by
  unfold VerificationStep at accepted
  split at accepted
  · exact Option.some.inj accepted |>.symm
  · simp at accepted

theorem apply_verification_event_preserves_identity
    (state : VerificationState) (event : VerificationEvent) :
    VerificationIdentity (ApplyVerificationEvent state event) =
      VerificationIdentity state := by
  rfl

theorem accepted_verification_step_preserves_identity
    {state next : VerificationState} {event : VerificationEvent}
    (accepted : VerificationStep state event = some next) :
    VerificationIdentity next = VerificationIdentity state := by
  rw [accepted_verification_step_applies_event accepted]
  exact apply_verification_event_preserves_identity state event

theorem apply_verification_event_preserves_support_authority
    (state : VerificationState) (event : VerificationEvent) :
    (ApplyVerificationEvent state event).supportAuthority = state.supportAuthority := by
  rfl

theorem apply_verification_event_preserves_external_effect_authority
    (state : VerificationState) (event : VerificationEvent) :
    (ApplyVerificationEvent state event).externalEffectAuthority =
      state.externalEffectAuthority := by
  rfl

theorem accepted_verification_step_preserves_support_authority
    {state next : VerificationState} {event : VerificationEvent}
    (accepted : VerificationStep state event = some next) :
    next.supportAuthority = state.supportAuthority := by
  rw [accepted_verification_step_applies_event accepted]
  exact apply_verification_event_preserves_support_authority state event

theorem accepted_verification_step_preserves_external_effect_authority
    {state next : VerificationState} {event : VerificationEvent}
    (accepted : VerificationStep state event = some next) :
    next.externalEffectAuthority = state.externalEffectAuthority := by
  rw [accepted_verification_step_applies_event accepted]
  exact apply_verification_event_preserves_external_effect_authority state event

theorem accepted_verification_step_leaves_proposed_stage
    {state next : VerificationState} {event : VerificationEvent}
    (accepted : VerificationStep state event = some next) :
    next.stage ≠ .proposed := by
  have valid := accepted_verification_step_is_valid accepted
  have applies := accepted_verification_step_applies_event accepted
  subst next
  rcases valid with ⟨_, _, _, specific⟩
  cases kind : event.kind <;>
    simp_all [VerificationEventSpecificValid, ApplyVerificationEvent]

theorem successful_verification_run_preserves_identity
    {state final : VerificationState} {events : List VerificationEvent}
    (ran : VerificationRun state events = some final) :
    VerificationIdentity final = VerificationIdentity state := by
  induction events generalizing state with
  | nil =>
      simp [VerificationRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : VerificationStep state event with
      | none => simp [VerificationRun, stepped] at ran
      | some next =>
          have tailRan : VerificationRun next tail = some final := by
            simpa [VerificationRun, stepped] using ran
          calc
            VerificationIdentity final = VerificationIdentity next := ih tailRan
            _ = VerificationIdentity state :=
              accepted_verification_step_preserves_identity stepped

theorem successful_verification_run_preserves_support_authority
    {state final : VerificationState} {events : List VerificationEvent}
    (ran : VerificationRun state events = some final) :
    final.supportAuthority = state.supportAuthority := by
  induction events generalizing state with
  | nil =>
      simp [VerificationRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : VerificationStep state event with
      | none => simp [VerificationRun, stepped] at ran
      | some next =>
          have tailRan : VerificationRun next tail = some final := by
            simpa [VerificationRun, stepped] using ran
          calc
            final.supportAuthority = next.supportAuthority := ih tailRan
            _ = state.supportAuthority :=
              accepted_verification_step_preserves_support_authority stepped

theorem successful_verification_run_preserves_external_effect_authority
    {state final : VerificationState} {events : List VerificationEvent}
    (ran : VerificationRun state events = some final) :
    final.externalEffectAuthority = state.externalEffectAuthority := by
  induction events generalizing state with
  | nil =>
      simp [VerificationRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : VerificationStep state event with
      | none => simp [VerificationRun, stepped] at ran
      | some next =>
          have tailRan : VerificationRun next tail = some final := by
            simpa [VerificationRun, stepped] using ran
          calc
            final.externalEffectAuthority = next.externalEffectAuthority := ih tailRan
            _ = state.externalEffectAuthority :=
              accepted_verification_step_preserves_external_effect_authority stepped

theorem successful_verification_run_has_valid_trace
    {state final : VerificationState} {events : List VerificationEvent}
    (ran : VerificationRun state events = some final) :
    VerificationTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : VerificationStep state event with
      | none => simp [VerificationRun, stepped] at ran
      | some next =>
          have tailRan : VerificationRun next tail = some final := by
            simpa [VerificationRun, stepped] using ran
          have applies := accepted_verification_step_applies_event stepped
          exact ⟨accepted_verification_step_is_valid stepped, by
            simpa [applies] using ih tailRan⟩

theorem verification_runs_compose
    (state : VerificationState) (left right : List VerificationEvent) :
    VerificationRun state (left ++ right) =
      match VerificationRun state left with
      | none => none
      | some middle => VerificationRun middle right := by
  induction left generalizing state with
  | nil => simp [VerificationRun]
  | cons event tail ih =>
      cases stepped : VerificationStep state event <;>
        simp [VerificationRun, stepped, ih]

theorem apply_verification_event_preserves_complete_custody
    (state : VerificationState) (event : VerificationEvent)
    (custody : CompleteVerificationCustody state) :
    CompleteVerificationCustody (ApplyVerificationEvent state event) := by
  rcases custody with ⟨frozen, executed, adjudicated, handedOff⟩
  simp [CompleteVerificationCustody, ApplyVerificationEvent, frozen, executed,
    adjudicated, handedOff]

theorem successful_verification_run_preserves_complete_custody
    {state final : VerificationState} {events : List VerificationEvent}
    (custody : CompleteVerificationCustody state)
    (ran : VerificationRun state events = some final) :
    CompleteVerificationCustody final := by
  induction events generalizing state with
  | nil =>
      simp [VerificationRun] at ran
      subst final
      exact custody
  | cons event tail ih =>
      cases stepped : VerificationStep state event with
      | none => simp [VerificationRun, stepped] at ran
      | some next =>
          have tailRan : VerificationRun next tail = some final := by
            simpa [VerificationRun, stepped] using ran
          have applies := accepted_verification_step_applies_event stepped
          subst next
          exact ih (apply_verification_event_preserves_complete_custody state event custody)
            tailRan

theorem accepted_execution_event_binds_valid_execution
    {state next : VerificationState} {event : VerificationEvent}
    (kind : event.kind = .recordExecution)
    (accepted : VerificationStep state event = some next) :
    ExecutionValid state.plan event.execution := by
  rcases accepted_verification_step_is_valid accepted with ⟨_, _, _, specific⟩
  simp_all [VerificationEventSpecificValid]

theorem accepted_adjudication_requires_evidence_gate_route
    {state next : VerificationState} {event : VerificationEvent}
    (kind : event.kind = .adjudicate)
    (accepted : VerificationStep state event = some next) :
    VerificationRouteFor state.plan state.execution =
      AdequacyRoute.handoffToEvidenceGate := by
  rcases accepted_verification_step_is_valid accepted with ⟨_, _, _, specific⟩
  simp_all [VerificationEventSpecificValid]

theorem accepted_handoff_cannot_request_support
    {state next : VerificationState} {event : VerificationEvent}
    (kind : event.kind = .handoff)
    (accepted : VerificationStep state event = some next) :
    event.supportPromotionRequested = false := by
  rcases accepted_verification_step_is_valid accepted with ⟨_, _, _, specific⟩
  simp_all [VerificationEventSpecificValid]

theorem accepted_handoff_cannot_request_external_effect
    {state next : VerificationState} {event : VerificationEvent}
    (kind : event.kind = .handoff)
    (accepted : VerificationStep state event = some next) :
    event.externalEffectRequested = false := by
  rcases accepted_verification_step_is_valid accepted with ⟨_, _, _, specific⟩
  simp_all [VerificationEventSpecificValid]

theorem admitted_context_does_not_establish_verification_adequacy :
    ∃ plan : VerificationPlan,
      plan.packetAdmitted = true ∧
        plan.obligationCount = 2 ∧
        plan.requestedEffect = RequestedEffect.evidenceReview := by
  exact ⟨{
    planId := 1
    claimId := 10
    claimVersion := 1
    packetDigest := 100
    packetAdmitted := true
    transactionValid := true
    riskTier := RiskTier.high
    requestedEffect := RequestedEffect.evidenceReview
    obligationCount := 2
    authorityValid := true
    rightsValid := true
    budgetDeclared := true
    horizonDeclared := true
    stopRuleDeclared := true
  }, rfl, rfl, rfl⟩

theorem unauthorized_promotion_request_is_blocked
    {plan : VerificationPlan} {execution : VerificationExecution} :
    plan.planId > 0 ->
    plan.claimId > 0 ->
    plan.claimVersion > 0 ->
    plan.packetDigest > 0 ->
    plan.packetAdmitted = true ->
    plan.transactionValid = true ->
    plan.obligationCount > 0 ->
    plan.authorityValid = true ->
    plan.rightsValid = true ->
    plan.budgetDeclared = true ->
    plan.horizonDeclared = true ->
    plan.stopRuleDeclared = true ->
    plan.requestedEffect = RequestedEffect.promoteChapterCore ->
    VerificationRouteFor plan execution =
      AdequacyRoute.blockUnauthorizedPromotion := by
  intro planId claimId claimVersion packetDigest admitted transactionValid
    obligations authority rights budget horizon stopRule requested
  unfold VerificationRouteFor
  simp [Nat.ne_of_gt planId, Nat.ne_of_gt claimId,
    Nat.ne_of_gt claimVersion, Nat.ne_of_gt packetDigest, admitted,
    transactionValid, Nat.ne_of_gt obligations, authority, rights, budget,
    horizon, stopRule, requested]

theorem contradiction_blocks_evidence_handoff
    {plan : VerificationPlan} {execution : VerificationExecution} :
    PlanValid plan ->
    plan.requestedEffect ≠ RequestedEffect.promoteChapterCore ->
    ExecutionBoundToPlan plan execution = true ->
    DispositionCount execution = plan.obligationCount ->
    execution.expiryDeclared = true ->
    execution.contradicted > 0 ->
    VerificationRouteFor plan execution = AdequacyRoute.blockContradiction := by
  intro valid notPromotion bound count expiry contradiction
  rcases valid with ⟨planId, claimId, claimVersion, packetDigest, admitted,
    transactionValid, obligations, authority, rights, budget, horizon,
    stopRule⟩
  unfold VerificationRouteFor
  simp [Nat.ne_of_gt planId, Nat.ne_of_gt claimId,
    Nat.ne_of_gt claimVersion, Nat.ne_of_gt packetDigest, admitted,
    transactionValid, Nat.ne_of_gt obligations, authority, rights, budget,
    horizon, stopRule, notPromotion, bound, count, expiry,
    Nat.ne_of_gt contradiction]

theorem complete_high_risk_review_requires_independent_evaluator
    {plan : VerificationPlan} {execution : VerificationExecution} :
    PlanValid plan ->
    plan.requestedEffect ≠ RequestedEffect.promoteChapterCore ->
    ExecutionBoundToPlan plan execution = true ->
    DispositionCount execution = plan.obligationCount ->
    execution.expiryDeclared = true ->
    execution.contradicted = 0 ->
    OpenDispositionCount execution = 0 ->
    HighRisk plan.riskTier = true ->
    execution.independentEvaluator = false ->
    VerificationRouteFor plan execution =
      AdequacyRoute.requireIndependentEvaluator := by
  intro valid notPromotion bound count expiry noContradiction noOpen highRisk
    dependent
  rcases valid with ⟨planId, claimId, claimVersion, packetDigest, admitted,
    transactionValid, obligations, authority, rights, budget, horizon,
    stopRule⟩
  unfold VerificationRouteFor
  simp [Nat.ne_of_gt planId, Nat.ne_of_gt claimId,
    Nat.ne_of_gt claimVersion, Nat.ne_of_gt packetDigest, admitted,
    transactionValid, Nat.ne_of_gt obligations, authority, rights, budget,
    horizon, stopRule, notPromotion, bound, count, expiry, noContradiction,
    noOpen, highRisk, dependent]

def referencePlan : VerificationPlan := {
  planId := 101
  claimId := 201
  claimVersion := 1
  packetDigest := 301
  packetAdmitted := true
  transactionValid := true
  riskTier := RiskTier.high
  requestedEffect := RequestedEffect.evidenceReview
  obligationCount := 4
  authorityValid := true
  rightsValid := true
  budgetDeclared := true
  horizonDeclared := true
  stopRuleDeclared := true
}

def referenceExecution : VerificationExecution := {
  planId := 101
  claimId := 201
  claimVersion := 1
  packetDigest := 301
  passed := 4
  failed := 0
  contradicted := 0
  disputed := 0
  unknown := 0
  infeasible := 0
  blocked := 0
  unattempted := 0
  negativeSearchAttempted := true
  independentEvaluator := true
  verificationArtifactsPresent := true
  residualsRecorded := false
  expiryDeclared := true
}

def referenceInitialState : VerificationState := {
  stage := .proposed
  plan := referencePlan
  execution := referenceExecution
  authorityCeiling := 1
  planFreezeReceipt := false
  executionReceipt := false
  adjudicationReceipt := false
  evidenceGateReceipt := false
  supportAuthority := false
  externalEffectAuthority := false
  logicalTime := 0
}

def referenceFreezeEvent : VerificationEvent := {
  kind := .freezePlan
  fromStage := .proposed
  toStage := .frozen
  planId := 101
  claimId := 201
  claimVersion := 1
  packetDigest := 301
  authorityCeiling := 1
  execution := referenceExecution
  planFreezeReceipt := true
  executionReceipt := false
  adjudicationReceipt := false
  evidenceGateReceipt := false
  supportPromotionRequested := false
  externalEffectRequested := false
  logicalTime := 1
}

def referenceExecutionEvent : VerificationEvent := {
  kind := .recordExecution
  fromStage := .frozen
  toStage := .executed
  planId := 101
  claimId := 201
  claimVersion := 1
  packetDigest := 301
  authorityCeiling := 1
  execution := referenceExecution
  planFreezeReceipt := false
  executionReceipt := true
  adjudicationReceipt := false
  evidenceGateReceipt := false
  supportPromotionRequested := false
  externalEffectRequested := false
  logicalTime := 2
}

def referenceAdjudicationEvent : VerificationEvent := {
  kind := .adjudicate
  fromStage := .executed
  toStage := .adjudicated
  planId := 101
  claimId := 201
  claimVersion := 1
  packetDigest := 301
  authorityCeiling := 1
  execution := referenceExecution
  planFreezeReceipt := false
  executionReceipt := false
  adjudicationReceipt := true
  evidenceGateReceipt := false
  supportPromotionRequested := false
  externalEffectRequested := false
  logicalTime := 3
}

def referenceHandoffEvent : VerificationEvent := {
  kind := .handoff
  fromStage := .adjudicated
  toStage := .handedOff
  planId := 101
  claimId := 201
  claimVersion := 1
  packetDigest := 301
  authorityCeiling := 1
  execution := referenceExecution
  planFreezeReceipt := false
  executionReceipt := false
  adjudicationReceipt := false
  evidenceGateReceipt := true
  supportPromotionRequested := false
  externalEffectRequested := false
  logicalTime := 4
}

def referenceVerificationEvents : List VerificationEvent :=
  [referenceFreezeEvent, referenceExecutionEvent, referenceAdjudicationEvent,
    referenceHandoffEvent]

theorem reference_plan_valid : PlanValid referencePlan := by
  simp [PlanValid, referencePlan]

theorem reference_execution_valid :
    ExecutionValid referencePlan referenceExecution := by
  simp [ExecutionValid, ExecutionBoundToPlan, DispositionCount,
    AttemptedCount, referencePlan, referenceExecution]

theorem reference_route_hands_off_only_to_evidence_gate :
    VerificationRouteFor referencePlan referenceExecution =
      AdequacyRoute.handoffToEvidenceGate := by
  simp [VerificationRouteFor, ExecutionBoundToPlan, DispositionCount,
    AttemptedCount, OpenDispositionCount, HighRisk, referencePlan,
    referenceExecution]

theorem reference_verification_lifecycle_reachable :
    Reachable referencePlan referenceExecution VerificationStage.handedOff := by
  exact Reachable.handedOff
    (Reachable.adjudicated
      (Reachable.executed
        (Reachable.frozen Reachable.proposed reference_plan_valid)
        reference_execution_valid))

theorem reference_freeze_step_accepted :
    VerificationStep referenceInitialState referenceFreezeEvent =
      some (ApplyVerificationEvent referenceInitialState referenceFreezeEvent) := by
  native_decide

theorem reference_execution_step_accepted :
    VerificationStep
        (ApplyVerificationEvent referenceInitialState referenceFreezeEvent)
        referenceExecutionEvent =
      some (ApplyVerificationEvent
        (ApplyVerificationEvent referenceInitialState referenceFreezeEvent)
        referenceExecutionEvent) := by
  native_decide

theorem reference_adjudication_step_accepted :
    let executed := ApplyVerificationEvent
      (ApplyVerificationEvent referenceInitialState referenceFreezeEvent)
      referenceExecutionEvent
    VerificationStep executed referenceAdjudicationEvent =
      some (ApplyVerificationEvent executed referenceAdjudicationEvent) := by
  native_decide

theorem reference_handoff_step_accepted :
    let executed := ApplyVerificationEvent
      (ApplyVerificationEvent referenceInitialState referenceFreezeEvent)
      referenceExecutionEvent
    let adjudicated := ApplyVerificationEvent executed referenceAdjudicationEvent
    VerificationStep adjudicated referenceHandoffEvent =
      some (ApplyVerificationEvent adjudicated referenceHandoffEvent) := by
  native_decide

theorem reference_verification_run_closes :
    ∃ final,
      VerificationRun referenceInitialState referenceVerificationEvents = some final ∧
      final.stage = .handedOff ∧
      CompleteVerificationCustody final ∧
      final.supportAuthority = false ∧
      final.externalEffectAuthority = false := by
  refine ⟨ApplyVerificationEvent
    (ApplyVerificationEvent
      (ApplyVerificationEvent
        (ApplyVerificationEvent referenceInitialState referenceFreezeEvent)
        referenceExecutionEvent)
      referenceAdjudicationEvent)
    referenceHandoffEvent, ?_⟩
  simp only [referenceVerificationEvents, VerificationRun]
  rw [reference_freeze_step_accepted]
  simp only
  rw [reference_execution_step_accepted]
  simp only
  rw [reference_adjudication_step_accepted]
  simp only
  rw [reference_handoff_step_accepted]
  simp [CompleteVerificationCustody, ApplyVerificationEvent,
    referenceInitialState, referenceFreezeEvent, referenceExecutionEvent,
    referenceAdjudicationEvent, referenceHandoffEvent]

theorem reference_verification_run_preserves_identity :
    ∀ final,
      VerificationRun referenceInitialState referenceVerificationEvents = some final ->
      VerificationIdentity final = (101, 201, 1, 301, 1) := by
  intro final ran
  calc
    VerificationIdentity final = VerificationIdentity referenceInitialState :=
      successful_verification_run_preserves_identity ran
    _ = (101, 201, 1, 301, 1) := by
      rfl

theorem reference_verification_run_has_zero_authority :
    ∀ final,
      VerificationRun referenceInitialState referenceVerificationEvents = some final ->
      final.supportAuthority = false ∧ final.externalEffectAuthority = false := by
  intro final ran
  constructor
  · simpa [referenceInitialState] using
      successful_verification_run_preserves_support_authority ran
  · simpa [referenceInitialState] using
      successful_verification_run_preserves_external_effect_authority ran

end AsiStackProofs.VerificationBandwidthRefinement
