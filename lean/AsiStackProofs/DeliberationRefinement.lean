namespace AsiStackProofs.DeliberationRefinement

inductive Stage where
  | requested | scoped | candidatesReady | evaluated
  | selected | stopped | handedOff | closed
deriving DecidableEq, Repr

inductive EventKind where
  | bindScope | generateCandidates | evaluateCandidates | selectCandidate
  | stopDeliberation | handoffToPlanning | close
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectRequestSubstitution | rejectPolicySubstitution
  | rejectEvaluatorSubstitution | rejectResultSubstitution | rejectEventReplay
  | rejectAuthorityLeak | rejectMalformedRequest | requireConsumer
  | requireTaskContract | requireRights | requireRiskClass | requireExpiry
  | requireModePolicy | requireBudget | requireCandidateLimit | requireStopRule
  | requireFirstCandidateCapture | requireCandidateHistory | requireTracePrivacy
  | requireCompleteAttemptDenominator | requireEvaluationObligations
  | requireVerifierIdentity | requireEvidenceView | requireDependenceRecord
  | requireCalibrationRecord | requireAbstentionRule | requireFalseDecisionBounds
  | requireIndependentHighRiskReview | requireCandidateResults
  | requireFirstCorrectness | requireCorruptionAccounting | requireRepairAccounting
  | requireFaithfulnessAxes | requireCompleteCostAccounting
  | requireFailureRetention | requireMatchedBaseline | requireUsefulMetric
  | stopAndEscrow | blockRawScorePromotion | requireSelectionReceipt
  | requireSelectionNonClaims | requireBudgetResidual | requireDisputeResidual
  | requireHighRiskReview | requireStopReceipt | rejectExecutionAuthority
  | requireConsumerAcknowledgment | requireResidualClosure
  | requireDescendantReferences | requireBoundResultDigest | requireCleanup
  | acceptScope | acceptCandidates | acceptEvaluation | acceptSelection
  | acceptStop | acceptHandoff | acceptClosure
deriving DecidableEq, Repr

structure Packet where
  requestId : Nat
  requestVersion : Nat
  consumerDigest : Nat
  taskDigest : Nat
  policyDigest : Nat
  budgetDigest : Nat
  verifierDigest : Nat
  evaluatorDigest : Nat
  resultDigest : Nat
  residualDigest : Nat
  eventDigest : Nat
  requestWellFormed : Bool
  consumer : Bool
  taskContract : Bool
  rights : Bool
  riskClass : Bool
  expiry : Bool
  modePolicy : Bool
  budget : Bool
  candidateLimit : Bool
  stopRule : Bool
  firstCandidateCapture : Bool
  candidateHistory : Bool
  tracePrivacy : Bool
  completeAttemptDenominator : Bool
  evaluationObligations : Bool
  verifierIdentity : Bool
  evidenceView : Bool
  dependenceRecord : Bool
  calibrationRecord : Bool
  abstentionRule : Bool
  falseDecisionBounds : Bool
  highRisk : Bool
  independentHighRiskReview : Bool
  candidateResults : Bool
  firstCorrectness : Bool
  corruptionAccounting : Bool
  repairAccounting : Bool
  faithfulnessAxes : Bool
  completeCostAccounting : Bool
  failureRetention : Bool
  matchedBaseline : Bool
  usefulMetric : Bool
  verifiedCandidate : Bool
  rawScorePromotionRequested : Bool
  selectionReceipt : Bool
  selectionNonClaims : Bool
  budgetExhausted : Bool
  disputed : Bool
  residualRecord : Bool
  stopReceipt : Bool
  executionRequested : Bool
  consumerAcknowledgment : Bool
  residualClosure : Bool
  descendantReferences : Bool
  resultDigestBound : Bool
  cleanup : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  requestId : Nat
  requestVersion : Nat
  consumerDigest : Nat
  taskDigest : Nat
  policyDigest : Nat
  budgetDigest : Nat
  verifierDigest : Nat
  evaluatorDigest : Nat
  resultDigest : Nat
  residualDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  candidateBatchCount : Nat
  evaluationCount : Nat
  selectionCount : Nat
  residualEscrowCount : Nat
  planningHandoffCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .requested => .bindScope
  | .scoped => .generateCandidates
  | .candidatesReady => .evaluateCandidates
  | .evaluated => .selectCandidate
  | .selected => .stopDeliberation
  | .stopped => .handoffToPlanning
  | .handedOff => .close
  | .closed => .close

def exactRequest (s : State) (p : Packet) : Bool :=
  p.requestId == s.requestId && p.requestVersion == s.requestVersion &&
  p.consumerDigest == s.consumerDigest && p.taskDigest == s.taskDigest

def exactPolicy (s : State) (p : Packet) : Bool :=
  p.policyDigest == s.policyDigest && p.budgetDigest == s.budgetDigest

def exactEvaluator (s : State) (p : Packet) : Bool :=
  p.verifierDigest == s.verifierDigest && p.evaluatorDigest == s.evaluatorDigest

def exactResult (s : State) (p : Packet) : Bool :=
  p.resultDigest == s.resultDigest && p.residualDigest == s.residualDigest

def routeFor (s : State) (e : Event) : Route :=
  if e.kind != expectedKind s.stage then .rejectWrongStage
  else if !exactRequest s e.packet then .rejectRequestSubstitution
  else if !exactPolicy s e.packet then .rejectPolicySubstitution
  else if !exactEvaluator s e.packet then .rejectEvaluatorSubstitution
  else if !exactResult s e.packet then .rejectResultSubstitution
  else if e.packet.eventDigest == s.lastEventDigest then .rejectEventReplay
  else if e.packet.externalEffectRequested then .rejectAuthorityLeak
  else match s.stage with
  | .requested =>
      if !e.packet.requestWellFormed then .rejectMalformedRequest
      else if !e.packet.consumer then .requireConsumer
      else if !e.packet.taskContract then .requireTaskContract
      else if !e.packet.rights then .requireRights
      else if !e.packet.riskClass then .requireRiskClass
      else if !e.packet.expiry then .requireExpiry
      else .acceptScope
  | .scoped =>
      if !e.packet.modePolicy then .requireModePolicy
      else if !e.packet.budget then .requireBudget
      else if !e.packet.candidateLimit then .requireCandidateLimit
      else if !e.packet.stopRule then .requireStopRule
      else if !e.packet.firstCandidateCapture then .requireFirstCandidateCapture
      else if !e.packet.candidateHistory then .requireCandidateHistory
      else if !e.packet.tracePrivacy then .requireTracePrivacy
      else if !e.packet.completeAttemptDenominator then .requireCompleteAttemptDenominator
      else .acceptCandidates
  | .candidatesReady =>
      if !e.packet.evaluationObligations then .requireEvaluationObligations
      else if !e.packet.verifierIdentity then .requireVerifierIdentity
      else if !e.packet.evidenceView then .requireEvidenceView
      else if !e.packet.dependenceRecord then .requireDependenceRecord
      else if !e.packet.calibrationRecord then .requireCalibrationRecord
      else if !e.packet.abstentionRule then .requireAbstentionRule
      else if !e.packet.falseDecisionBounds then .requireFalseDecisionBounds
      else if e.packet.highRisk && !e.packet.independentHighRiskReview then
        .requireIndependentHighRiskReview
      else if !e.packet.candidateResults then .requireCandidateResults
      else .acceptEvaluation
  | .evaluated =>
      if !e.packet.firstCorrectness then .requireFirstCorrectness
      else if !e.packet.corruptionAccounting then .requireCorruptionAccounting
      else if !e.packet.repairAccounting then .requireRepairAccounting
      else if !e.packet.faithfulnessAxes then .requireFaithfulnessAxes
      else if !e.packet.completeCostAccounting then .requireCompleteCostAccounting
      else if !e.packet.failureRetention then .requireFailureRetention
      else if !e.packet.matchedBaseline then .requireMatchedBaseline
      else if !e.packet.usefulMetric then .requireUsefulMetric
      else .acceptSelection
  | .selected =>
      if !e.packet.verifiedCandidate then .stopAndEscrow
      else if e.packet.rawScorePromotionRequested then .blockRawScorePromotion
      else if !e.packet.selectionReceipt then .requireSelectionReceipt
      else if !e.packet.selectionNonClaims then .requireSelectionNonClaims
      else .acceptStop
  | .stopped =>
      if e.packet.budgetExhausted && !e.packet.residualRecord then .requireBudgetResidual
      else if e.packet.disputed && !e.packet.residualRecord then .requireDisputeResidual
      else if e.packet.highRisk && !e.packet.independentHighRiskReview then .requireHighRiskReview
      else if !e.packet.stopReceipt then .requireStopReceipt
      else .acceptHandoff
  | .handedOff =>
      if e.packet.executionRequested then .rejectExecutionAuthority
      else if !e.packet.consumerAcknowledgment then .requireConsumerAcknowledgment
      else if !e.packet.residualClosure then .requireResidualClosure
      else if !e.packet.descendantReferences then .requireDescendantReferences
      else if !e.packet.resultDigestBound then .requireBoundResultDigest
      else if !e.packet.cleanup then .requireCleanup
      else .acceptClosure
  | .closed => .rejectWrongStage

def accepted : Route -> Bool
  | .stopAndEscrow | .acceptScope | .acceptCandidates | .acceptEvaluation
  | .acceptSelection | .acceptStop | .acceptHandoff | .acceptClosure => true
  | _ => false

def advance : Stage -> Stage
  | .requested => .scoped | .scoped => .candidatesReady
  | .candidatesReady => .evaluated | .evaluated => .selected
  | .selected => .stopped | .stopped => .handedOff
  | .handedOff => .closed | .closed => .closed

def applyEvent (s : State) (e : Event) : State × Route :=
  let r := routeFor s e
  if accepted r then
    ({s with
      stage := advance s.stage
      lastEventDigest := e.packet.eventDigest
      receiptCount := s.receiptCount + 1
      candidateBatchCount := if s.stage == .scoped then s.candidateBatchCount + 1 else s.candidateBatchCount
      evaluationCount := if s.stage == .candidatesReady then s.evaluationCount + 1 else s.evaluationCount
      selectionCount := if s.stage == .evaluated then s.selectionCount + 1 else s.selectionCount
      residualEscrowCount := if r == .stopAndEscrow then s.residualEscrowCount + 1 else s.residualEscrowCount
      planningHandoffCount := if s.stage == .stopped then s.planningHandoffCount + 1 else s.planningHandoffCount}, r)
  else (s, r)

theorem apply_event_preserves_request_policy_evaluator_and_result_identity (s : State) (e : Event) :
    (applyEvent s e).1.requestId = s.requestId ∧
    (applyEvent s e).1.policyDigest = s.policyDigest ∧
    (applyEvent s e).1.verifierDigest = s.verifierDigest ∧
    (applyEvent s e).1.resultDigest = s.resultDigest := by
  by_cases h : accepted (routeFor s e) = true <;> simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_effect (s : State) (e : Event) :
    (applyEvent s e).1.supportAssignmentCount = s.supportAssignmentCount ∧
    (applyEvent s e).1.externalEffectCount = s.externalEffectCount := by
  by_cases h : accepted (routeFor s e) = true <;> simp [applyEvent, h]

theorem accepted_step_adds_one_receipt (s : State) (e : Event)
    (h : accepted (routeFor s e) = true) :
    (applyEvent s e).1.receiptCount = s.receiptCount + 1 := by simp [applyEvent, h]

def completePacket : Packet :=
  { requestId := 4001, requestVersion := 3, consumerDigest := 4002
    taskDigest := 4003, policyDigest := 4004, budgetDigest := 4005
    verifierDigest := 4006, evaluatorDigest := 4007, resultDigest := 4008
    residualDigest := 4009, eventDigest := 1, requestWellFormed := true
    consumer := true, taskContract := true, rights := true, riskClass := true
    expiry := true, modePolicy := true, budget := true, candidateLimit := true
    stopRule := true, firstCandidateCapture := true, candidateHistory := true
    tracePrivacy := true, completeAttemptDenominator := true
    evaluationObligations := true, verifierIdentity := true, evidenceView := true
    dependenceRecord := true, calibrationRecord := true, abstentionRule := true
    falseDecisionBounds := true, highRisk := false, independentHighRiskReview := true
    candidateResults := true, firstCorrectness := true, corruptionAccounting := true
    repairAccounting := true, faithfulnessAxes := true, completeCostAccounting := true
    failureRetention := true, matchedBaseline := true, usefulMetric := true
    verifiedCandidate := true, rawScorePromotionRequested := false
    selectionReceipt := true, selectionNonClaims := true, budgetExhausted := false
    disputed := false, residualRecord := true, stopReceipt := true
    executionRequested := false, consumerAcknowledgment := true
    residualClosure := true, descendantReferences := true, resultDigestBound := true
    cleanup := true, externalEffectRequested := false }

def stateAt (stage : Stage) : State :=
  { stage := stage, requestId := 4001, requestVersion := 3
    consumerDigest := 4002, taskDigest := 4003, policyDigest := 4004
    budgetDigest := 4005, verifierDigest := 4006, evaluatorDigest := 4007
    resultDigest := 4008, residualDigest := 4009, lastEventDigest := 0
    receiptCount := 0, candidateBatchCount := 0, evaluationCount := 0
    selectionCount := 0, residualEscrowCount := 0, planningHandoffCount := 0
    supportAssignmentCount := 0, externalEffectCount := 0 }

theorem missing_budget_blocks_candidate_generation :
  routeFor (stateAt .scoped) {kind := .generateCandidates, packet := {completePacket with budget := false}} =
  .requireBudget := by rfl

theorem high_risk_without_independent_review_blocks_evaluation :
  routeFor (stateAt .candidatesReady) {kind := .evaluateCandidates, packet := {completePacket with highRisk := true, independentHighRiskReview := false}} =
  .requireIndependentHighRiskReview := by rfl

theorem missing_first_correctness_blocks_selection :
  routeFor (stateAt .evaluated) {kind := .selectCandidate, packet := {completePacket with firstCorrectness := false}} =
  .requireFirstCorrectness := by rfl

theorem raw_score_cannot_promote_selected_candidate :
  routeFor (stateAt .selected) {kind := .stopDeliberation, packet := {completePacket with rawScorePromotionRequested := true}} =
  .blockRawScorePromotion := by rfl

theorem budget_exhaustion_without_residual_blocks_handoff :
  routeFor (stateAt .stopped) {kind := .handoffToPlanning, packet := {completePacket with budgetExhausted := true, residualRecord := false}} =
  .requireBudgetResidual := by rfl

theorem execution_authority_cannot_cross_planning_handoff :
  routeFor (stateAt .handedOff) {kind := .close, packet := {completePacket with executionRequested := true}} =
  .rejectExecutionAuthority := by rfl

def event (kind : EventKind) (digest : Nat) (packet : Packet := completePacket) : Event :=
  {kind := kind, packet := {packet with eventDigest := digest}}

theorem verified_deliberation_lifecycle_reaches_closed_without_support_or_effect_authority :
  let s0 := stateAt .requested
  let s1 := (applyEvent s0 (event .bindScope 1)).1
  let s2 := (applyEvent s1 (event .generateCandidates 2)).1
  let s3 := (applyEvent s2 (event .evaluateCandidates 3)).1
  let s4 := (applyEvent s3 (event .selectCandidate 4)).1
  let s5 := (applyEvent s4 (event .stopDeliberation 5)).1
  let s6 := (applyEvent s5 (event .handoffToPlanning 6)).1
  let s7 := (applyEvent s6 (event .close 7)).1
  s7.stage = .closed ∧ s7.receiptCount = 7 ∧ s7.candidateBatchCount = 1 ∧
  s7.evaluationCount = 1 ∧ s7.selectionCount = 1 ∧ s7.residualEscrowCount = 0 ∧
  s7.planningHandoffCount = 1 ∧ s7.supportAssignmentCount = 0 ∧
  s7.externalEffectCount = 0 := by native_decide

theorem no_verified_candidate_reaches_closed_with_residual_escrow :
  let s0 := stateAt .requested
  let s1 := (applyEvent s0 (event .bindScope 1)).1
  let s2 := (applyEvent s1 (event .generateCandidates 2)).1
  let s3 := (applyEvent s2 (event .evaluateCandidates 3)).1
  let s4 := (applyEvent s3 (event .selectCandidate 4)).1
  let s5 := (applyEvent s4 (event .stopDeliberation 5 {completePacket with verifiedCandidate := false})).1
  let s6 := (applyEvent s5 (event .handoffToPlanning 6)).1
  let s7 := (applyEvent s6 (event .close 7)).1
  s7.stage = .closed ∧ s7.residualEscrowCount = 1 ∧ s7.planningHandoffCount = 1 ∧
  s7.supportAssignmentCount = 0 ∧ s7.externalEffectCount = 0 := by native_decide

end AsiStackProofs.DeliberationRefinement
