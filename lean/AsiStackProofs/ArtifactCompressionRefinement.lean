namespace AsiStackProofs.ArtifactCompressionRefinement

inductive Stage where
  | registered | encoded | verified | probed | fallbackReady | admitted | consumed | closed
deriving DecidableEq, Repr

inductive EventKind where
  | bindArtifact | recordEncoding | verifyReconstruction | probeConsumer
  | prepareFallback | admitUse | recordConsumption | close
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectIdentitySubstitution | rejectPolicySubstitution
  | rejectDecoderSubstitution | rejectEvidenceSubstitution | rejectEventReplay
  | rejectAuthorityLeak
  | requestFullArtifact | requestManifest | requestUseEnvelope
  | requestAccessPattern | requestConsumer | requestRights | acceptEncoding
  | requestCodecIdentity | requestDecoderIdentity | requestPlatform
  | requestByteAccounting | requestResidual | requestArtifactDigest | acceptVerification
  | requestDecoderDeterminism | blockExactReplay | requestIntegrity
  | requestAdversarialMutation | requestVerificationReceipt | acceptProbe
  | requestTaskProbe | routeToFallback | requestFallbackArtifact
  | requestUtilityEvidence | requestRareCaseCoverage | requestSecurityAndRights | acceptFallbackPrep
  | requestFallbackTrigger | requestFallbackExecution | requestRecoveryReceipt
  | requestCostAccounting | acceptAdmission
  | blockUnqualifiedUse | blockRawRatioPromotion | requestEvidenceTransition
  | requestNonClaims | acceptConsumption
  | requestConsumerAck | requestObservedOutcome | requestFallbackOutcome
  | requestResidualClosure | acceptClosure
  | requestDescendants | requestResultDigest | requestCleanup | acceptClosed
deriving DecidableEq, Repr

structure State where
  stage : Stage
  artifactDigest : Nat
  consumerDigest : Nat
  useDigest : Nat
  policyDigest : Nat
  rightsDigest : Nat
  codecDigest : Nat
  decoderDigest : Nat
  evidenceDigest : Nat
  resultDigest : Nat
  lastEventDigest : Nat
  supportAssigned : Bool := false
  externalEffectCommitted : Bool := false
deriving DecidableEq, Repr

structure Packet where
  artifactDigest : Nat := 5001
  consumerDigest : Nat := 5002
  useDigest : Nat := 5003
  policyDigest : Nat := 5004
  rightsDigest : Nat := 5005
  codecDigest : Nat := 5006
  decoderDigest : Nat := 5007
  evidenceDigest : Nat := 5008
  resultDigest : Nat := 5009
  eventDigest : Nat := 101
  fullArtifact : Bool := true
  manifest : Bool := true
  useEnvelope : Bool := true
  accessPattern : Bool := true
  consumer : Bool := true
  rights : Bool := true
  codecIdentity : Bool := true
  decoderIdentity : Bool := true
  platform : Bool := true
  byteAccounting : Bool := true
  residual : Bool := true
  artifactDigestRecord : Bool := true
  decoderDeterminism : Bool := true
  exactReplayRequired : Bool := false
  exactReplayReady : Bool := true
  integrity : Bool := true
  adversarialMutation : Bool := true
  verificationReceipt : Bool := true
  taskProbeRequired : Bool := true
  taskProbePassed : Bool := true
  fallbackArtifact : Bool := true
  utilityEvidence : Bool := true
  rareCaseCoverage : Bool := true
  securityAndRights : Bool := true
  fallbackTrigger : Bool := true
  fallbackExecuted : Bool := true
  recoveryReceipt : Bool := true
  costAccounting : Bool := true
  qualifiedUse : Bool := true
  rawRatioPromotion : Bool := false
  evidenceTransition : Bool := true
  nonClaims : Bool := true
  consumerAck : Bool := true
  observedOutcome : Bool := true
  fallbackOutcome : Bool := true
  residualClosure : Bool := true
  descendants : Bool := true
  resultDigestBound : Bool := true
  cleanup : Bool := true
  supportPromotionRequested : Bool := false
  externalEffectRequested : Bool := false
deriving DecidableEq, Repr

def expectedKind : Stage → EventKind
  | .registered => .bindArtifact | .encoded => .recordEncoding
  | .verified => .verifyReconstruction | .probed => .probeConsumer
  | .fallbackReady => .prepareFallback | .admitted => .admitUse
  | .consumed => .recordConsumption | .closed => .close

def accepted : Route → Bool
  | .acceptEncoding | .acceptVerification | .acceptProbe | .routeToFallback
  | .acceptFallbackPrep | .acceptAdmission | .acceptConsumption
  | .acceptClosure | .acceptClosed => true
  | _ => false

def route (s : State) (kind : EventKind) (p : Packet) : Route :=
  if kind != expectedKind s.stage then .rejectWrongStage
  else if p.artifactDigest != s.artifactDigest || p.consumerDigest != s.consumerDigest || p.useDigest != s.useDigest then .rejectIdentitySubstitution
  else if p.policyDigest != s.policyDigest || p.rightsDigest != s.rightsDigest then .rejectPolicySubstitution
  else if p.codecDigest != s.codecDigest || p.decoderDigest != s.decoderDigest then .rejectDecoderSubstitution
  else if p.evidenceDigest != s.evidenceDigest || p.resultDigest != s.resultDigest then .rejectEvidenceSubstitution
  else if p.eventDigest = s.lastEventDigest then .rejectEventReplay
  else if p.supportPromotionRequested || p.externalEffectRequested then .rejectAuthorityLeak
  else match s.stage with
  | .registered =>
      if !p.fullArtifact then .requestFullArtifact else if !p.manifest then .requestManifest
      else if !p.useEnvelope then .requestUseEnvelope else if !p.accessPattern then .requestAccessPattern
      else if !p.consumer then .requestConsumer else if !p.rights then .requestRights else .acceptEncoding
  | .encoded =>
      if !p.codecIdentity then .requestCodecIdentity else if !p.decoderIdentity then .requestDecoderIdentity
      else if !p.platform then .requestPlatform else if !p.byteAccounting then .requestByteAccounting
      else if !p.residual then .requestResidual else if !p.artifactDigestRecord then .requestArtifactDigest else .acceptVerification
  | .verified =>
      if !p.decoderDeterminism then .requestDecoderDeterminism
      else if p.exactReplayRequired && !p.exactReplayReady then .blockExactReplay
      else if !p.integrity then .requestIntegrity else if !p.adversarialMutation then .requestAdversarialMutation
      else if !p.verificationReceipt then .requestVerificationReceipt else .acceptProbe
  | .probed =>
      if !p.taskProbeRequired then .requestTaskProbe
      else if !p.taskProbePassed then
        if p.fallbackArtifact then .routeToFallback else .requestFallbackArtifact
      else if !p.utilityEvidence then .requestUtilityEvidence else if !p.rareCaseCoverage then .requestRareCaseCoverage
      else if !p.securityAndRights then .requestSecurityAndRights else .acceptFallbackPrep
  | .fallbackReady =>
      if !p.fallbackTrigger then .requestFallbackTrigger else if !p.fallbackExecuted then .requestFallbackExecution
      else if !p.recoveryReceipt then .requestRecoveryReceipt else if !p.costAccounting then .requestCostAccounting else .acceptAdmission
  | .admitted =>
      if !p.qualifiedUse then .blockUnqualifiedUse else if p.rawRatioPromotion then .blockRawRatioPromotion
      else if !p.evidenceTransition then .requestEvidenceTransition else if !p.nonClaims then .requestNonClaims else .acceptConsumption
  | .consumed =>
      if !p.consumerAck then .requestConsumerAck else if !p.observedOutcome then .requestObservedOutcome
      else if !p.fallbackOutcome then .requestFallbackOutcome else if !p.residualClosure then .requestResidualClosure else .acceptClosure
  | .closed =>
      if !p.descendants then .requestDescendants else if !p.resultDigestBound then .requestResultDigest
      else if !p.cleanup then .requestCleanup else .acceptClosed

def completeState (selectedStage : Stage) : State where
  stage := selectedStage
  artifactDigest := 5001
  consumerDigest := 5002
  useDigest := 5003
  policyDigest := 5004
  rightsDigest := 5005
  codecDigest := 5006
  decoderDigest := 5007
  evidenceDigest := 5008
  resultDigest := 5009
  lastEventDigest := 0

def completePacket : Packet := {}

theorem complete_packet_has_no_support_or_effect_authority :
    completePacket.supportPromotionRequested = false ∧
    completePacket.externalEffectRequested = false := by decide

theorem failed_probe_with_fallback_routes_to_fallback :
    route (completeState .probed) .probeConsumer
      { completePacket with taskProbePassed := false } = .routeToFallback := by native_decide

theorem failed_probe_without_fallback_requests_artifact :
    route (completeState .probed) .probeConsumer
      { completePacket with taskProbePassed := false, fallbackArtifact := false } = .requestFallbackArtifact := by native_decide

theorem exact_replay_without_readiness_blocks_use :
    route (completeState .verified) .verifyReconstruction
      { completePacket with exactReplayRequired := true, exactReplayReady := false } = .blockExactReplay := by native_decide

theorem raw_ratio_cannot_promote_admitted_artifact :
    route (completeState .admitted) .admitUse
      { completePacket with rawRatioPromotion := true } = .blockRawRatioPromotion := by native_decide

theorem missing_evidence_transition_blocks_consumption :
    route (completeState .admitted) .admitUse
      { completePacket with evidenceTransition := false } = .requestEvidenceTransition := by native_decide

theorem exact_use_lifecycle_routes_to_closed :
    route (completeState .registered) .bindArtifact completePacket = .acceptEncoding ∧
    route (completeState .encoded) .recordEncoding completePacket = .acceptVerification ∧
    route (completeState .verified) .verifyReconstruction completePacket = .acceptProbe ∧
    route (completeState .probed) .probeConsumer completePacket = .acceptFallbackPrep ∧
    route (completeState .fallbackReady) .prepareFallback completePacket = .acceptAdmission ∧
    route (completeState .admitted) .admitUse completePacket = .acceptConsumption ∧
    route (completeState .consumed) .recordConsumption completePacket = .acceptClosure ∧
    route (completeState .closed) .close completePacket = .acceptClosed := by native_decide

theorem failed_probe_lifecycle_has_executable_fallback_without_support :
    route (completeState .probed) .probeConsumer
      { completePacket with taskProbePassed := false } = .routeToFallback ∧
    route (completeState .fallbackReady) .prepareFallback completePacket = .acceptAdmission ∧
    completePacket.supportPromotionRequested = false ∧ completePacket.externalEffectRequested = false := by native_decide

end AsiStackProofs.ArtifactCompressionRefinement
