namespace AsiStackProofs.ProofCarryingClaimsRefinement

inductive Stage where
  | idle
  | frozen
  | artifactBound
  | executed
  | adjudicated
  | writtenBack
deriving DecidableEq, Repr

inductive EventKind where
  | freezeTarget
  | bindArtifact
  | executeVerifier
  | adjudicate
  | writeBack
deriving DecidableEq, Repr

inductive VerifierResult where
  | passed
  | failed
  | timeout
  | mismatch
  | notRun
deriving DecidableEq, Repr

inductive ClaimEffect where
  | scopedProposal
  | noChange
  | downgrade
  | block
  | tribunal
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage
  | rejectTargetSubstitution
  | rejectEventSubstitution
  | rejectAuthorityLeak
  | requestInterpretationMapping
  | requestScopeAndAssumptions
  | requestArtifact
  | requestTrustedBase
  | requestVerifierExecution
  | requestVerifierArtifactRefs
  | requestAttemptHistory
  | blockUnverifiedPass
  | blockNegativePromotion
  | routeMismatchToTribunal
  | requestIndependentDossier
  | requestDissentPreservation
  | requestLimitsAndResidual
  | requestOwnerHandoff
  | acceptTargetFreeze
  | acceptArtifactBinding
  | acceptVerifierExecution
  | acceptAdjudication
  | acceptWriteBack
deriving DecidableEq, Repr

structure Packet where
  claimId : Nat
  claimVersion : Nat
  targetDigest : Nat
  interpretationDigest : Nat
  scopeDigest : Nat
  assumptionsDigest : Nat
  artifactDigest : Nat
  verifierId : Nat
  verifierVersion : Nat
  trustedBaseDigest : Nat
  eventDigest : Nat
  artifactPresent : Bool
  interpretationMappingPresent : Bool
  scopePresent : Bool
  assumptionsPresent : Bool
  trustedBasePresent : Bool
  verifierExecuted : Bool
  verifierArtifactRefsPresent : Bool
  attemptHistoryPresent : Bool
  artifactVerified : Bool
  semanticMappingReviewed : Bool
  highRisk : Bool
  independentReviewPresent : Bool
  dossierPresent : Bool
  dissentPresent : Bool
  dissentPreserved : Bool
  limitationsPresent : Bool
  residualPresent : Bool
  ownerHandoffPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
  verifierResult : VerifierResult
  claimEffect : ClaimEffect
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  claimId : Nat
  claimVersion : Nat
  targetDigest : Nat
  interpretationDigest : Nat
  scopeDigest : Nat
  assumptionsDigest : Nat
  artifactDigest : Nat
  verifierId : Nat
  verifierVersion : Nat
  trustedBaseDigest : Nat
  lastEventDigest : Nat
  verifierResult : VerifierResult
  claimEffect : ClaimEffect
  receiptCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .idle => .freezeTarget
  | .frozen => .bindArtifact
  | .artifactBound => .executeVerifier
  | .executed => .adjudicate
  | .adjudicated => .writeBack
  | .writtenBack => .writeBack

def exactTargetBinding (state : State) (packet : Packet) : Bool :=
  packet.claimId == state.claimId &&
  packet.claimVersion == state.claimVersion &&
  packet.targetDigest == state.targetDigest &&
  packet.interpretationDigest == state.interpretationDigest &&
  packet.scopeDigest == state.scopeDigest &&
  packet.assumptionsDigest == state.assumptionsDigest

def exactArtifactBinding (state : State) (packet : Packet) : Bool :=
  packet.artifactDigest == state.artifactDigest &&
  packet.verifierId == state.verifierId &&
  packet.verifierVersion == state.verifierVersion &&
  packet.trustedBaseDigest == state.trustedBaseDigest

def negativeResult : VerifierResult -> Bool
  | .failed | .timeout | .mismatch => true
  | .passed | .notRun => false

def routeFor (state : State) (event : Event) : Route :=
  if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactTargetBinding state event.packet then .rejectTargetSubstitution
  else if state.stage != .idle && ! exactArtifactBinding state event.packet then
    .rejectEventSubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectEventSubstitution
  else if event.packet.supportAssignmentRequested || event.packet.externalEffectRequested then
    .rejectAuthorityLeak
  else match state.stage with
  | .idle =>
      if ! event.packet.interpretationMappingPresent then .requestInterpretationMapping
      else if ! event.packet.scopePresent || ! event.packet.assumptionsPresent then
        .requestScopeAndAssumptions
      else .acceptTargetFreeze
  | .frozen =>
      if ! event.packet.artifactPresent then .requestArtifact
      else if ! event.packet.trustedBasePresent then .requestTrustedBase
      else .acceptArtifactBinding
  | .artifactBound =>
      if ! event.packet.verifierExecuted || event.packet.verifierResult == .notRun then
        .requestVerifierExecution
      else if event.packet.verifierResult == .passed &&
          ! event.packet.verifierArtifactRefsPresent then
        .requestVerifierArtifactRefs
      else if negativeResult event.packet.verifierResult &&
          ! event.packet.attemptHistoryPresent then
        .requestAttemptHistory
      else .acceptVerifierExecution
  | .executed =>
      if event.packet.verifierResult != state.verifierResult then .rejectEventSubstitution
      else if event.packet.verifierResult == .passed &&
          (! event.packet.artifactVerified || ! event.packet.semanticMappingReviewed) then
        .blockUnverifiedPass
      else if negativeResult event.packet.verifierResult &&
          event.packet.claimEffect == .scopedProposal then
        .blockNegativePromotion
      else if event.packet.verifierResult == .mismatch &&
          event.packet.claimEffect != .tribunal then
        .routeMismatchToTribunal
      else if event.packet.highRisk &&
          (! event.packet.independentReviewPresent || ! event.packet.dossierPresent) then
        .requestIndependentDossier
      else if event.packet.dissentPresent && ! event.packet.dissentPreserved then
        .requestDissentPreservation
      else if ! event.packet.limitationsPresent || ! event.packet.residualPresent then
        .requestLimitsAndResidual
      else .acceptAdjudication
  | .adjudicated =>
      if event.packet.verifierResult != state.verifierResult ||
          event.packet.claimEffect != state.claimEffect then
        .rejectEventSubstitution
      else if ! event.packet.ownerHandoffPresent then .requestOwnerHandoff
      else .acceptWriteBack
  | .writtenBack => .rejectWrongStage

def advanceStage : Stage -> Stage
  | .idle => .frozen
  | .frozen => .artifactBound
  | .artifactBound => .executed
  | .executed => .adjudicated
  | .adjudicated => .writtenBack
  | .writtenBack => .writtenBack

def accepted : Route -> Bool
  | .acceptTargetFreeze
  | .acceptArtifactBinding
  | .acceptVerifierExecution
  | .acceptAdjudication
  | .acceptWriteBack => true
  | _ => false

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advanceStage state.stage
       lastEventDigest := event.packet.eventDigest
       verifierResult := if state.stage == .artifactBound then
         event.packet.verifierResult else state.verifierResult
       claimEffect := if state.stage == .executed then
         event.packet.claimEffect else state.claimEffect
       receiptCount := state.receiptCount + 1 }, route)
  else (state, route)

theorem apply_event_preserves_target_identity
    (state : State) (event : Event) :
    (applyEvent state event).1.claimId = state.claimId ∧
    (applyEvent state event).1.claimVersion = state.claimVersion ∧
    (applyEvent state event).1.targetDigest = state.targetDigest ∧
    (applyEvent state event).1.interpretationDigest = state.interpretationDigest ∧
    (applyEvent state event).1.scopeDigest = state.scopeDigest ∧
    (applyEvent state event).1.assumptionsDigest = state.assumptionsDigest := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_effect
    (state : State) (event : Event) :
    (applyEvent state event).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state event).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, h]

theorem accepted_step_adds_exactly_one_receipt
    (state : State) (event : Event)
    (h : accepted (routeFor state event) = true) :
    (applyEvent state event).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, h]

def canonicalPacket : Packet :=
  { claimId := 41
    claimVersion := 7
    targetDigest := 101
    interpretationDigest := 102
    scopeDigest := 103
    assumptionsDigest := 104
    artifactDigest := 201
    verifierId := 301
    verifierVersion := 3
    trustedBaseDigest := 401
    eventDigest := 1
    artifactPresent := true
    interpretationMappingPresent := true
    scopePresent := true
    assumptionsPresent := true
    trustedBasePresent := true
    verifierExecuted := true
    verifierArtifactRefsPresent := true
    attemptHistoryPresent := true
    artifactVerified := true
    semanticMappingReviewed := true
    highRisk := true
    independentReviewPresent := true
    dossierPresent := true
    dissentPresent := true
    dissentPreserved := true
    limitationsPresent := true
    residualPresent := true
    ownerHandoffPresent := true
    supportAssignmentRequested := false
    externalEffectRequested := false
    verifierResult := .passed
    claimEffect := .scopedProposal }

def baseIdle : State :=
  { stage := .idle
    claimId := 41
    claimVersion := 7
    targetDigest := 101
    interpretationDigest := 102
    scopeDigest := 103
    assumptionsDigest := 104
    artifactDigest := 201
    verifierId := 301
    verifierVersion := 3
    trustedBaseDigest := 401
    lastEventDigest := 0
    verifierResult := .notRun
    claimEffect := .noChange
    receiptCount := 0
    supportAssignmentCount := 0
    externalEffectCount := 0 }

def freezeEvent : Event := { kind := .freezeTarget, packet := canonicalPacket }
def frozenState : State := (applyEvent baseIdle freezeEvent).1
def bindEvent : Event := { kind := .bindArtifact, packet := { canonicalPacket with eventDigest := 2 } }
def artifactBoundState : State := (applyEvent frozenState bindEvent).1
def executeEvent : Event := { kind := .executeVerifier, packet := { canonicalPacket with eventDigest := 3 } }
def executedState : State := (applyEvent artifactBoundState executeEvent).1
def adjudicateEvent : Event := { kind := .adjudicate, packet := { canonicalPacket with eventDigest := 4 } }
def adjudicatedState : State := (applyEvent executedState adjudicateEvent).1
def writeBackEvent : Event := { kind := .writeBack, packet := { canonicalPacket with eventDigest := 5 } }
def finalState : State := (applyEvent adjudicatedState writeBackEvent).1

def baseArtifactBound : State := artifactBoundState
def passWithoutRefsEvent : Event :=
  { kind := .executeVerifier
    packet := { canonicalPacket with eventDigest := 33, verifierArtifactRefsPresent := false } }
def failedWithoutHistoryEvent : Event :=
  { kind := .executeVerifier
    packet := { canonicalPacket with
      eventDigest := 34
      verifierResult := VerifierResult.failed
      attemptHistoryPresent := false } }
def failedExecuted : State := { executedState with verifierResult := .failed }
def negativePromotionEvent : Event :=
  { kind := .adjudicate
    packet := { canonicalPacket with
      eventDigest := 35
      verifierResult := VerifierResult.failed
      claimEffect := ClaimEffect.scopedProposal } }
def mismatchExecuted : State := { executedState with verifierResult := .mismatch }
def mismatchNoTribunalEvent : Event :=
  { kind := .adjudicate
    packet := { canonicalPacket with
      eventDigest := 36
      verifierResult := VerifierResult.mismatch
      claimEffect := ClaimEffect.block } }
def passedExecuted : State := executedState
def unverifiedPassEvent : Event :=
  { kind := .adjudicate
    packet := { canonicalPacket with eventDigest := 37, artifactVerified := false } }
def highRiskNoDossierEvent : Event :=
  { kind := .adjudicate
    packet := { canonicalPacket with eventDigest := 38, dossierPresent := false } }
def supportLeakWriteBackEvent : Event :=
  { kind := .writeBack
    packet := { canonicalPacket with eventDigest := 39, supportAssignmentRequested := true } }

theorem passed_execution_without_artifact_refs_is_rejected :
    routeFor baseArtifactBound passWithoutRefsEvent = .requestVerifierArtifactRefs := by
  rfl

theorem negative_execution_without_attempt_history_is_rejected :
    routeFor baseArtifactBound failedWithoutHistoryEvent = .requestAttemptHistory := by
  rfl

theorem negative_result_scoped_proposal_is_blocked :
    routeFor failedExecuted negativePromotionEvent = .blockNegativePromotion := by
  rfl

theorem mismatch_requires_tribunal_effect :
    routeFor mismatchExecuted mismatchNoTribunalEvent = .routeMismatchToTribunal := by
  rfl

theorem unverified_pass_is_blocked_before_adjudication :
    routeFor passedExecuted unverifiedPassEvent = .blockUnverifiedPass := by
  rfl

theorem high_risk_without_independent_dossier_is_rejected :
    routeFor passedExecuted highRiskNoDossierEvent = .requestIndependentDossier := by
  rfl

theorem support_assignment_request_is_authority_leak :
    routeFor adjudicatedState supportLeakWriteBackEvent = .rejectAuthorityLeak := by
  rfl

theorem full_verification_lifecycle_reaches_owner_writeback :
    finalState.stage = .writtenBack ∧
    finalState.receiptCount = 5 ∧
    finalState.verifierResult = .passed ∧
    finalState.claimEffect = .scopedProposal ∧
    finalState.supportAssignmentCount = 0 ∧
    finalState.externalEffectCount = 0 := by
  native_decide

end AsiStackProofs.ProofCarryingClaimsRefinement
