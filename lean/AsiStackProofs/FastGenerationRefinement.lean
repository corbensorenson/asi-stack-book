namespace AsiStackProofs.FastGenerationRefinement

inductive Stage where
  | requested | contextBound | modeSelected | draftGenerated
  | verified | accounted | decided | closed
deriving DecidableEq, Repr

inductive EventKind where
  | bindContext | selectMode | generateDraft | verifyDraft
  | accountOutcome | decide | close
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectTaskSubstitution | rejectModeSubstitution
  | rejectEvaluatorSubstitution | rejectResultSubstitution | rejectEventReplay
  | rejectAuthorityLeak | rejectMalformedRequest | requireContextPacket
  | requireTaskSet | requireConsumer | requireDeadline | requireRights
  | selectSlowBaseline | requireGenerationMode | requireRiskTier
  | requireQualityTarget | requireVerifierIdentity | requireIndependentEvaluator
  | requireAcceptancePredicate | requireMatchedBaseline | requireLatencyBudget
  | requireComputeMemoryBudget | requireRiskOverride | requireSlowFallback
  | requireHighRiskReview | requireGenerator | requireDraftArtifact
  | requireProposedOutput | requireGenerationCost | requireSearchBound
  | requireObservedVerification | requireExecutableFallback
  | requireFallbackResidual | activateFallback | requireAcceptedOutput
  | requireQualityPass | requireVerifierCost | requireFallbackCost
  | requireTaskSuccess | requireBaselineResult | requireUsefulDenominator
  | requireCostMetricSeparation | requireOutputDigest | blockRawSpeedProxy
  | requireEvidenceTransition | requireDecisionReceipt
  | requireDecisionNonClaims | requireConsumerAcknowledgment
  | requireResidualClosure | requireDescendantReferences
  | requireBoundResultDigest | requireCleanup | acceptContext
  | acceptFastSelection | acceptGeneration | acceptVerification
  | acceptAccounting | acceptDecision | acceptClosure
deriving DecidableEq, Repr

structure Packet where
  taskId : Nat
  taskVersion : Nat
  contextDigest : Nat
  taskSetDigest : Nat
  consumerDigest : Nat
  modeDigest : Nat
  baselineDigest : Nat
  verifierDigest : Nat
  resultDigest : Nat
  residualDigest : Nat
  eventDigest : Nat
  requestWellFormed : Bool
  contextPacket : Bool
  taskSet : Bool
  consumer : Bool
  deadline : Bool
  rights : Bool
  fastModeRequested : Bool
  generationMode : Bool
  riskTier : Bool
  qualityTarget : Bool
  verifierIdentity : Bool
  independentEvaluator : Bool
  acceptancePredicate : Bool
  matchedBaseline : Bool
  latencyBudget : Bool
  computeMemoryBudget : Bool
  highRisk : Bool
  riskOverride : Bool
  slowFallback : Bool
  highRiskReview : Bool
  generator : Bool
  draftArtifact : Bool
  proposedOutput : Bool
  generationCost : Bool
  searchBound : Bool
  observedVerification : Bool
  verificationPassed : Bool
  fallbackExecutable : Bool
  fallbackResidual : Bool
  acceptedOutput : Bool
  qualityPass : Bool
  verifierCost : Bool
  fallbackCost : Bool
  taskSuccess : Bool
  baselineResult : Bool
  usefulDenominator : Bool
  costMetricSeparation : Bool
  outputDigest : Bool
  rawSpeedPromotionRequested : Bool
  supportPromotionRequested : Bool
  evidenceTransition : Bool
  decisionReceipt : Bool
  decisionNonClaims : Bool
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
  taskId : Nat
  taskVersion : Nat
  contextDigest : Nat
  taskSetDigest : Nat
  consumerDigest : Nat
  modeDigest : Nat
  baselineDigest : Nat
  verifierDigest : Nat
  resultDigest : Nat
  residualDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  draftCount : Nat
  verificationCount : Nat
  fallbackCount : Nat
  usefulOutcomeCount : Nat
  decisionCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .requested => .bindContext | .contextBound => .selectMode
  | .modeSelected => .generateDraft | .draftGenerated => .verifyDraft
  | .verified => .accountOutcome | .accounted => .decide
  | .decided => .close | .closed => .close

def exactTask (s : State) (p : Packet) : Bool :=
  p.taskId == s.taskId && p.taskVersion == s.taskVersion &&
  p.contextDigest == s.contextDigest && p.taskSetDigest == s.taskSetDigest &&
  p.consumerDigest == s.consumerDigest
def exactMode (s : State) (p : Packet) : Bool :=
  p.modeDigest == s.modeDigest && p.baselineDigest == s.baselineDigest
def exactEvaluator (s : State) (p : Packet) : Bool :=
  p.verifierDigest == s.verifierDigest
def exactResult (s : State) (p : Packet) : Bool :=
  p.resultDigest == s.resultDigest && p.residualDigest == s.residualDigest

def routeFor (s : State) (e : Event) : Route :=
  if e.kind != expectedKind s.stage then .rejectWrongStage
  else if !exactTask s e.packet then .rejectTaskSubstitution
  else if !exactMode s e.packet then .rejectModeSubstitution
  else if !exactEvaluator s e.packet then .rejectEvaluatorSubstitution
  else if !exactResult s e.packet then .rejectResultSubstitution
  else if e.packet.eventDigest == s.lastEventDigest then .rejectEventReplay
  else if e.packet.externalEffectRequested then .rejectAuthorityLeak
  else match s.stage with
  | .requested =>
      if !e.packet.requestWellFormed then .rejectMalformedRequest
      else if !e.packet.contextPacket then .requireContextPacket
      else if !e.packet.taskSet then .requireTaskSet
      else if !e.packet.consumer then .requireConsumer
      else if !e.packet.deadline then .requireDeadline
      else if !e.packet.rights then .requireRights
      else .acceptContext
  | .contextBound =>
      if !e.packet.fastModeRequested then .selectSlowBaseline
      else if !e.packet.generationMode then .requireGenerationMode
      else if !e.packet.riskTier then .requireRiskTier
      else if !e.packet.qualityTarget then .requireQualityTarget
      else if !e.packet.verifierIdentity then .requireVerifierIdentity
      else if !e.packet.independentEvaluator then .requireIndependentEvaluator
      else if !e.packet.acceptancePredicate then .requireAcceptancePredicate
      else if !e.packet.matchedBaseline then .requireMatchedBaseline
      else if !e.packet.latencyBudget then .requireLatencyBudget
      else if !e.packet.computeMemoryBudget then .requireComputeMemoryBudget
      else if e.packet.highRisk && !e.packet.riskOverride then .requireRiskOverride
      else if e.packet.highRisk && !e.packet.slowFallback then .requireSlowFallback
      else if e.packet.highRisk && !e.packet.highRiskReview then .requireHighRiskReview
      else .acceptFastSelection
  | .modeSelected =>
      if !e.packet.generator then .requireGenerator
      else if !e.packet.draftArtifact then .requireDraftArtifact
      else if !e.packet.proposedOutput then .requireProposedOutput
      else if !e.packet.generationCost then .requireGenerationCost
      else if !e.packet.searchBound then .requireSearchBound
      else .acceptGeneration
  | .draftGenerated =>
      if !e.packet.observedVerification then .requireObservedVerification
      else if !e.packet.verificationPassed && !e.packet.fallbackExecutable then
        .requireExecutableFallback
      else if !e.packet.verificationPassed && !e.packet.fallbackResidual then
        .requireFallbackResidual
      else if !e.packet.verificationPassed then .activateFallback
      else if !e.packet.acceptedOutput then .requireAcceptedOutput
      else if !e.packet.qualityPass then .requireQualityPass
      else .acceptVerification
  | .verified =>
      if !e.packet.verifierCost then .requireVerifierCost
      else if s.fallbackCount > 0 && !e.packet.fallbackCost then .requireFallbackCost
      else if !e.packet.taskSuccess then .requireTaskSuccess
      else if !e.packet.baselineResult then .requireBaselineResult
      else if !e.packet.usefulDenominator then .requireUsefulDenominator
      else if !e.packet.costMetricSeparation then .requireCostMetricSeparation
      else if !e.packet.outputDigest then .requireOutputDigest
      else .acceptAccounting
  | .accounted =>
      if e.packet.rawSpeedPromotionRequested &&
          !(e.packet.acceptedOutput && e.packet.taskSuccess && e.packet.baselineResult) then
        .blockRawSpeedProxy
      else if e.packet.supportPromotionRequested && !e.packet.evidenceTransition then
        .requireEvidenceTransition
      else if !e.packet.decisionReceipt then .requireDecisionReceipt
      else if !e.packet.decisionNonClaims then .requireDecisionNonClaims
      else .acceptDecision
  | .decided =>
      if !e.packet.consumerAcknowledgment then .requireConsumerAcknowledgment
      else if !e.packet.residualClosure then .requireResidualClosure
      else if !e.packet.descendantReferences then .requireDescendantReferences
      else if !e.packet.resultDigestBound then .requireBoundResultDigest
      else if !e.packet.cleanup then .requireCleanup
      else .acceptClosure
  | .closed => .rejectWrongStage

def accepted : Route -> Bool
  | .selectSlowBaseline | .activateFallback | .acceptContext | .acceptFastSelection
  | .acceptGeneration | .acceptVerification | .acceptAccounting | .acceptDecision
  | .acceptClosure => true
  | _ => false

def advance : Stage -> Stage
  | .requested => .contextBound | .contextBound => .modeSelected
  | .modeSelected => .draftGenerated | .draftGenerated => .verified
  | .verified => .accounted | .accounted => .decided
  | .decided => .closed | .closed => .closed

def applyEvent (s : State) (e : Event) : State × Route :=
  let r := routeFor s e
  if accepted r then
    ({s with
      stage := advance s.stage
      lastEventDigest := e.packet.eventDigest
      receiptCount := s.receiptCount + 1
      draftCount := if s.stage == .modeSelected then s.draftCount + 1 else s.draftCount
      verificationCount := if s.stage == .draftGenerated then s.verificationCount + 1 else s.verificationCount
      fallbackCount := if r == .activateFallback then s.fallbackCount + 1 else s.fallbackCount
      usefulOutcomeCount := if s.stage == .verified then s.usefulOutcomeCount + 1 else s.usefulOutcomeCount
      decisionCount := if s.stage == .accounted then s.decisionCount + 1 else s.decisionCount}, r)
  else (s, r)

theorem apply_event_preserves_task_mode_evaluator_and_result_identity (s : State) (e : Event) :
    (applyEvent s e).1.taskId = s.taskId ∧
    (applyEvent s e).1.modeDigest = s.modeDigest ∧
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
  { taskId := 3001, taskVersion := 2, contextDigest := 3002, taskSetDigest := 3003
    consumerDigest := 3004, modeDigest := 3005, baselineDigest := 3006
    verifierDigest := 3007, resultDigest := 3008, residualDigest := 3009
    eventDigest := 1, requestWellFormed := true, contextPacket := true, taskSet := true
    consumer := true, deadline := true, rights := true, fastModeRequested := true
    generationMode := true, riskTier := true, qualityTarget := true
    verifierIdentity := true, independentEvaluator := true, acceptancePredicate := true
    matchedBaseline := true, latencyBudget := true, computeMemoryBudget := true
    highRisk := false, riskOverride := true, slowFallback := true, highRiskReview := true
    generator := true, draftArtifact := true, proposedOutput := true, generationCost := true
    searchBound := true, observedVerification := true, verificationPassed := true
    fallbackExecutable := true, fallbackResidual := true, acceptedOutput := true
    qualityPass := true, verifierCost := true, fallbackCost := true, taskSuccess := true
    baselineResult := true, usefulDenominator := true, costMetricSeparation := true
    outputDigest := true, rawSpeedPromotionRequested := false
    supportPromotionRequested := false, evidenceTransition := true, decisionReceipt := true
    decisionNonClaims := true, consumerAcknowledgment := true, residualClosure := true
    descendantReferences := true, resultDigestBound := true, cleanup := true
    externalEffectRequested := false }

def stateAt (stage : Stage) (fallbackCount : Nat := 0) : State :=
  { stage := stage, taskId := 3001, taskVersion := 2, contextDigest := 3002
    taskSetDigest := 3003, consumerDigest := 3004, modeDigest := 3005
    baselineDigest := 3006, verifierDigest := 3007, resultDigest := 3008
    residualDigest := 3009, lastEventDigest := 0, receiptCount := 0
    draftCount := 0, verificationCount := 0, fallbackCount := fallbackCount
    usefulOutcomeCount := 0, decisionCount := 0, supportAssignmentCount := 0
    externalEffectCount := 0 }

theorem context_substitution_rejected :
  routeFor (stateAt .requested) {kind := .bindContext, packet := {completePacket with contextDigest := 999}} =
  .rejectTaskSubstitution := by rfl
theorem missing_task_set_blocks_context_binding :
  routeFor (stateAt .requested) {kind := .bindContext, packet := {completePacket with taskSet := false}} =
  .requireTaskSet := by rfl
theorem no_fast_request_selects_slow_baseline :
  routeFor (stateAt .contextBound) {kind := .selectMode, packet := {completePacket with fastModeRequested := false}} =
  .selectSlowBaseline := by rfl
theorem high_risk_without_override_blocks_fast_selection :
  routeFor (stateAt .contextBound) {kind := .selectMode, packet := {completePacket with highRisk := true, riskOverride := false}} =
  .requireRiskOverride := by rfl
theorem missing_draft_artifact_blocks_generation :
  routeFor (stateAt .modeSelected) {kind := .generateDraft, packet := {completePacket with draftArtifact := false}} =
  .requireDraftArtifact := by rfl
theorem failed_verification_activates_executable_fallback :
  routeFor (stateAt .draftGenerated) {kind := .verifyDraft, packet := {completePacket with verificationPassed := false}} =
  .activateFallback := by rfl
theorem failed_verification_without_fallback_is_blocked :
  routeFor (stateAt .draftGenerated) {kind := .verifyDraft, packet := {completePacket with verificationPassed := false, fallbackExecutable := false}} =
  .requireExecutableFallback := by rfl
theorem fallback_without_cost_blocks_accounting :
  routeFor (stateAt .verified 1) {kind := .accountOutcome, packet := {completePacket with fallbackCost := false}} =
  .requireFallbackCost := by rfl
theorem missing_task_success_blocks_accounting :
  routeFor (stateAt .verified) {kind := .accountOutcome, packet := {completePacket with taskSuccess := false}} =
  .requireTaskSuccess := by rfl
theorem raw_speed_proxy_without_accepted_output_is_blocked :
  routeFor (stateAt .accounted) {kind := .decide, packet := {completePacket with rawSpeedPromotionRequested := true, acceptedOutput := false}} =
  .blockRawSpeedProxy := by rfl
theorem support_promotion_without_transition_blocks_decision :
  routeFor (stateAt .accounted) {kind := .decide, packet := {completePacket with supportPromotionRequested := true, evidenceTransition := false}} =
  .requireEvidenceTransition := by rfl
theorem missing_consumer_acknowledgment_blocks_closure :
  routeFor (stateAt .decided) {kind := .close, packet := {completePacket with consumerAcknowledgment := false}} =
  .requireConsumerAcknowledgment := by rfl

def event (kind : EventKind) (digest : Nat) (packet : Packet := completePacket) : Event :=
  {kind := kind, packet := {packet with eventDigest := digest}}

theorem verified_fast_lifecycle_reaches_closed_without_support_or_effect_authority :
  let s0 := stateAt .requested
  let s1 := (applyEvent s0 (event .bindContext 1)).1
  let s2 := (applyEvent s1 (event .selectMode 2)).1
  let s3 := (applyEvent s2 (event .generateDraft 3)).1
  let s4 := (applyEvent s3 (event .verifyDraft 4)).1
  let s5 := (applyEvent s4 (event .accountOutcome 5)).1
  let s6 := (applyEvent s5 (event .decide 6)).1
  let s7 := (applyEvent s6 (event .close 7)).1
  s7.stage = .closed ∧ s7.receiptCount = 7 ∧ s7.draftCount = 1 ∧
  s7.verificationCount = 1 ∧ s7.fallbackCount = 0 ∧ s7.usefulOutcomeCount = 1 ∧
  s7.decisionCount = 1 ∧ s7.supportAssignmentCount = 0 ∧ s7.externalEffectCount = 0 := by
  native_decide

theorem fallback_lifecycle_reaches_closed_with_fallback_accounted :
  let s0 := stateAt .requested
  let s1 := (applyEvent s0 (event .bindContext 1)).1
  let s2 := (applyEvent s1 (event .selectMode 2)).1
  let s3 := (applyEvent s2 (event .generateDraft 3)).1
  let s4 := (applyEvent s3 (event .verifyDraft 4 {completePacket with verificationPassed := false})).1
  let s5 := (applyEvent s4 (event .accountOutcome 5)).1
  let s6 := (applyEvent s5 (event .decide 6)).1
  let s7 := (applyEvent s6 (event .close 7)).1
  s7.stage = .closed ∧ s7.fallbackCount = 1 ∧ s7.usefulOutcomeCount = 1 ∧
  s7.supportAssignmentCount = 0 ∧ s7.externalEffectCount = 0 := by native_decide

end AsiStackProofs.FastGenerationRefinement
