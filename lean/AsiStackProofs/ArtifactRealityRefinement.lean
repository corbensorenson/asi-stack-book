namespace AsiStackProofs.ArtifactRealityRefinement

inductive Stage where
  | idle
  | registered
  | provenanceBound
  | replayValidated
  | realityCrossChecked
  | trustBound
  | admitted
deriving DecidableEq, Repr

inductive EventKind where
  | registerArtifact
  | bindProvenance
  | validateReplay
  | crossCheckReality
  | bindTrustBase
  | admitArtifact
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage
  | rejectArtifactSubstitution
  | rejectLineageSubstitution
  | rejectEventReplay
  | rejectAuthorityLeak
  | requestArtifactRecord
  | requestParentJob
  | requestSourceAndContext
  | requestTransactionAndCertificate
  | requestToolClaimAndTestLinks
  | requestAuditTrail
  | requestReplayMetadata
  | requestReplayGrade
  | requestReplayLimits
  | requestActiveCertificate
  | requestReplayValidation
  | requestObservedArtifact
  | requestIndependentCrossCheck
  | requestTrapChallenge
  | requestAttestationLimits
  | requestTrustedCore
  | requestRootOfTrust
  | requestIndependentVerifier
  | requestRecursionStop
  | requestOutsideTcbResidual
  | requestRevocationClosure
  | requestConsumerAcknowledgment
  | acceptRegistration
  | acceptProvenanceBinding
  | acceptReplayValidation
  | acceptRealityCrossCheck
  | acceptTrustBinding
  | acceptAdmission
deriving DecidableEq, Repr

structure Packet where
  artifactId : Nat
  artifactVersion : Nat
  contentDigest : Nat
  parentJobDigest : Nat
  sourceDigest : Nat
  contextDigest : Nat
  transactionDigest : Nat
  certificateDigest : Nat
  toolDigest : Nat
  claimDigest : Nat
  testDigest : Nat
  policyDigest : Nat
  consumerDigest : Nat
  eventDigest : Nat
  artifactPresent : Bool
  producedArtifact : Bool
  parentJobPresent : Bool
  sourceRefsPresent : Bool
  contextRefsPresent : Bool
  transactionRefsPresent : Bool
  certificateRefsPresent : Bool
  toolRefsPresent : Bool
  claimLinksPresent : Bool
  testLinksPresent : Bool
  auditTrailPresent : Bool
  replayMetadataPresent : Bool
  replayGradeSufficient : Bool
  replayLimitsPresent : Bool
  certificateActive : Bool
  replayValidated : Bool
  observedArtifactPresent : Bool
  independentCrossCheckMatched : Bool
  trapChallengePassed : Bool
  attestationLimitsPresent : Bool
  trustedCorePresent : Bool
  rootOfTrustPresent : Bool
  independentVerifierPresent : Bool
  recursionStopPresent : Bool
  outsideTcbResidualPresent : Bool
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
  artifactId : Nat
  artifactVersion : Nat
  contentDigest : Nat
  parentJobDigest : Nat
  sourceDigest : Nat
  contextDigest : Nat
  transactionDigest : Nat
  certificateDigest : Nat
  toolDigest : Nat
  claimDigest : Nat
  testDigest : Nat
  policyDigest : Nat
  consumerDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  realityObservationCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .idle => .registerArtifact
  | .registered => .bindProvenance
  | .provenanceBound => .validateReplay
  | .replayValidated => .crossCheckReality
  | .realityCrossChecked => .bindTrustBase
  | .trustBound => .admitArtifact
  | .admitted => .admitArtifact

def exactArtifactBinding (state : State) (packet : Packet) : Bool :=
  packet.artifactId == state.artifactId &&
  packet.artifactVersion == state.artifactVersion &&
  packet.contentDigest == state.contentDigest &&
  packet.policyDigest == state.policyDigest &&
  packet.consumerDigest == state.consumerDigest

def exactLineageBinding (state : State) (packet : Packet) : Bool :=
  packet.parentJobDigest == state.parentJobDigest &&
  packet.sourceDigest == state.sourceDigest &&
  packet.contextDigest == state.contextDigest &&
  packet.transactionDigest == state.transactionDigest &&
  packet.certificateDigest == state.certificateDigest &&
  packet.toolDigest == state.toolDigest &&
  packet.claimDigest == state.claimDigest &&
  packet.testDigest == state.testDigest

def routeFor (state : State) (event : Event) : Route :=
  if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactArtifactBinding state event.packet then .rejectArtifactSubstitution
  else if ! exactLineageBinding state event.packet then .rejectLineageSubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectEventReplay
  else if event.packet.supportAssignmentRequested || event.packet.externalEffectRequested then
    .rejectAuthorityLeak
  else match state.stage with
  | .idle =>
      if ! event.packet.artifactPresent || ! event.packet.producedArtifact then
        .requestArtifactRecord
      else if ! event.packet.parentJobPresent then .requestParentJob
      else .acceptRegistration
  | .registered =>
      if ! event.packet.sourceRefsPresent || ! event.packet.contextRefsPresent then
        .requestSourceAndContext
      else if ! event.packet.transactionRefsPresent ||
          ! event.packet.certificateRefsPresent then .requestTransactionAndCertificate
      else if ! event.packet.toolRefsPresent || ! event.packet.claimLinksPresent ||
          ! event.packet.testLinksPresent then .requestToolClaimAndTestLinks
      else if ! event.packet.auditTrailPresent then .requestAuditTrail
      else .acceptProvenanceBinding
  | .provenanceBound =>
      if ! event.packet.replayMetadataPresent then .requestReplayMetadata
      else if ! event.packet.replayGradeSufficient then .requestReplayGrade
      else if ! event.packet.replayLimitsPresent then .requestReplayLimits
      else if ! event.packet.certificateActive then .requestActiveCertificate
      else if ! event.packet.replayValidated then .requestReplayValidation
      else .acceptReplayValidation
  | .replayValidated =>
      if ! event.packet.observedArtifactPresent then .requestObservedArtifact
      else if ! event.packet.independentCrossCheckMatched then .requestIndependentCrossCheck
      else if ! event.packet.trapChallengePassed then .requestTrapChallenge
      else if ! event.packet.attestationLimitsPresent then .requestAttestationLimits
      else .acceptRealityCrossCheck
  | .realityCrossChecked =>
      if ! event.packet.trustedCorePresent then .requestTrustedCore
      else if ! event.packet.rootOfTrustPresent then .requestRootOfTrust
      else if ! event.packet.independentVerifierPresent then .requestIndependentVerifier
      else if ! event.packet.recursionStopPresent then .requestRecursionStop
      else if ! event.packet.outsideTcbResidualPresent then .requestOutsideTcbResidual
      else .acceptTrustBinding
  | .trustBound =>
      if ! event.packet.revocationClosureComplete then .requestRevocationClosure
      else if ! event.packet.consumerAcknowledgmentPresent then
        .requestConsumerAcknowledgment
      else .acceptAdmission
  | .admitted => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptRegistration
  | .acceptProvenanceBinding
  | .acceptReplayValidation
  | .acceptRealityCrossCheck
  | .acceptTrustBinding
  | .acceptAdmission => true
  | _ => false

def advanceStage : Stage -> Stage
  | .idle => .registered
  | .registered => .provenanceBound
  | .provenanceBound => .replayValidated
  | .replayValidated => .realityCrossChecked
  | .realityCrossChecked => .trustBound
  | .trustBound => .admitted
  | .admitted => .admitted

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advanceStage state.stage
       lastEventDigest := event.packet.eventDigest
       receiptCount := state.receiptCount + 1
       realityObservationCount :=
         if state.stage == .replayValidated then state.realityObservationCount + 1
         else state.realityObservationCount }, route)
  else (state, route)

theorem apply_event_preserves_artifact_and_lineage_identity
    (state : State) (event : Event) :
    (applyEvent state event).1.artifactId = state.artifactId ∧
    (applyEvent state event).1.artifactVersion = state.artifactVersion ∧
    (applyEvent state event).1.contentDigest = state.contentDigest ∧
    (applyEvent state event).1.parentJobDigest = state.parentJobDigest ∧
    (applyEvent state event).1.sourceDigest = state.sourceDigest ∧
    (applyEvent state event).1.contextDigest = state.contextDigest ∧
    (applyEvent state event).1.transactionDigest = state.transactionDigest ∧
    (applyEvent state event).1.certificateDigest = state.certificateDigest := by
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
  { artifactId := 801
    artifactVersion := 5
    contentDigest := 901
    parentJobDigest := 902
    sourceDigest := 903
    contextDigest := 904
    transactionDigest := 905
    certificateDigest := 906
    toolDigest := 907
    claimDigest := 908
    testDigest := 909
    policyDigest := 910
    consumerDigest := 911
    eventDigest := 1
    artifactPresent := true
    producedArtifact := true
    parentJobPresent := true
    sourceRefsPresent := true
    contextRefsPresent := true
    transactionRefsPresent := true
    certificateRefsPresent := true
    toolRefsPresent := true
    claimLinksPresent := true
    testLinksPresent := true
    auditTrailPresent := true
    replayMetadataPresent := true
    replayGradeSufficient := true
    replayLimitsPresent := true
    certificateActive := true
    replayValidated := true
    observedArtifactPresent := true
    independentCrossCheckMatched := true
    trapChallengePassed := true
    attestationLimitsPresent := true
    trustedCorePresent := true
    rootOfTrustPresent := true
    independentVerifierPresent := true
    recursionStopPresent := true
    outsideTcbResidualPresent := true
    revocationClosureComplete := true
    consumerAcknowledgmentPresent := true
    supportAssignmentRequested := false
    externalEffectRequested := false }

def initialState : State :=
  { stage := .idle
    artifactId := 801
    artifactVersion := 5
    contentDigest := 901
    parentJobDigest := 902
    sourceDigest := 903
    contextDigest := 904
    transactionDigest := 905
    certificateDigest := 906
    toolDigest := 907
    claimDigest := 908
    testDigest := 909
    policyDigest := 910
    consumerDigest := 911
    lastEventDigest := 0
    receiptCount := 0
    realityObservationCount := 0
    supportAssignmentCount := 0
    externalEffectCount := 0 }

def registerEvent : Event := { kind := .registerArtifact, packet := canonicalPacket }
def registeredState : State := (applyEvent initialState registerEvent).1
def bindEvent : Event := { kind := .bindProvenance, packet := { canonicalPacket with eventDigest := 2 } }
def provenanceState : State := (applyEvent registeredState bindEvent).1
def replayEvent : Event := { kind := .validateReplay, packet := { canonicalPacket with eventDigest := 3 } }
def replayState : State := (applyEvent provenanceState replayEvent).1
def realityEvent : Event := { kind := .crossCheckReality, packet := { canonicalPacket with eventDigest := 4 } }
def realityState : State := (applyEvent replayState realityEvent).1
def trustEvent : Event := { kind := .bindTrustBase, packet := { canonicalPacket with eventDigest := 5 } }
def trustState : State := (applyEvent realityState trustEvent).1
def admitEvent : Event := { kind := .admitArtifact, packet := { canonicalPacket with eventDigest := 6 } }
def finalState : State := (applyEvent trustState admitEvent).1

def missingParentEvent : Event :=
  { kind := .registerArtifact, packet := { canonicalPacket with eventDigest := 20, parentJobPresent := false } }
def missingTransactionEvent : Event :=
  { kind := .bindProvenance, packet := { canonicalPacket with eventDigest := 21, transactionRefsPresent := false } }
def missingAuditEvent : Event :=
  { kind := .bindProvenance, packet := { canonicalPacket with eventDigest := 22, auditTrailPresent := false } }
def staleCertificateReplayEvent : Event :=
  { kind := .validateReplay, packet := { canonicalPacket with eventDigest := 23, certificateActive := false } }
def incompleteReplayEvent : Event :=
  { kind := .validateReplay, packet := { canonicalPacket with eventDigest := 24, replayValidated := false } }
def missingObservationEvent : Event :=
  { kind := .crossCheckReality, packet := { canonicalPacket with eventDigest := 25, observedArtifactPresent := false } }
def missingIndependentCheckEvent : Event :=
  { kind := .crossCheckReality, packet := { canonicalPacket with eventDigest := 26, independentCrossCheckMatched := false } }
def unboundedAttestationEvent : Event :=
  { kind := .crossCheckReality, packet := { canonicalPacket with eventDigest := 27, attestationLimitsPresent := false } }
def selfVerifierEvent : Event :=
  { kind := .bindTrustBase, packet := { canonicalPacket with eventDigest := 28, independentVerifierPresent := false } }
def missingRecursionStopEvent : Event :=
  { kind := .bindTrustBase, packet := { canonicalPacket with eventDigest := 29, recursionStopPresent := false } }
def incompleteRevocationEvent : Event :=
  { kind := .admitArtifact, packet := { canonicalPacket with eventDigest := 30, revocationClosureComplete := false } }

theorem produced_artifact_requires_parent_job :
    routeFor initialState missingParentEvent = .requestParentJob := by rfl

theorem provenance_requires_transaction_and_certificate_links :
    routeFor registeredState missingTransactionEvent = .requestTransactionAndCertificate := by rfl

theorem provenance_requires_audit_trail :
    routeFor registeredState missingAuditEvent = .requestAuditTrail := by rfl

theorem stale_certificate_blocks_replay_validation :
    routeFor provenanceState staleCertificateReplayEvent = .requestActiveCertificate := by rfl

theorem incomplete_replay_blocks_reality_review :
    routeFor provenanceState incompleteReplayEvent = .requestReplayValidation := by rfl

theorem reality_review_requires_observed_artifact :
    routeFor replayState missingObservationEvent = .requestObservedArtifact := by rfl

theorem reality_review_requires_independent_cross_check :
    routeFor replayState missingIndependentCheckEvent = .requestIndependentCrossCheck := by rfl

theorem attestation_must_preserve_limits :
    routeFor replayState unboundedAttestationEvent = .requestAttestationLimits := by rfl

theorem trust_binding_rejects_self_verifier_laundering :
    routeFor realityState selfVerifierEvent = .requestIndependentVerifier := by rfl

theorem trust_binding_requires_recursion_stop :
    routeFor realityState missingRecursionStopEvent = .requestRecursionStop := by rfl

theorem admission_requires_revocation_closure :
    routeFor trustState incompleteRevocationEvent = .requestRevocationClosure := by rfl

theorem full_artifact_reality_lifecycle_reaches_admission :
    finalState.stage = .admitted ∧
    finalState.receiptCount = 6 ∧
    finalState.realityObservationCount = 1 ∧
    finalState.supportAssignmentCount = 0 ∧
    finalState.externalEffectCount = 0 := by
  native_decide

end AsiStackProofs.ArtifactRealityRefinement
