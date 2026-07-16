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

end AsiStackProofs.VerificationBandwidthRefinement
