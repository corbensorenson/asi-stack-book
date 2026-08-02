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
  receiptCount : Nat := 0
  fallbackCount : Nat := 0
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

structure StateIdentity where
  artifactDigest : Nat
  consumerDigest : Nat
  useDigest : Nat
  policyDigest : Nat
  rightsDigest : Nat
  codecDigest : Nat
  decoderDigest : Nat
  evidenceDigest : Nat
  resultDigest : Nat
deriving DecidableEq, Repr

def stateIdentity (s : State) : StateIdentity :=
  { artifactDigest := s.artifactDigest
    consumerDigest := s.consumerDigest
    useDigest := s.useDigest
    policyDigest := s.policyDigest
    rightsDigest := s.rightsDigest
    codecDigest := s.codecDigest
    decoderDigest := s.decoderDigest
    evidenceDigest := s.evidenceDigest
    resultDigest := s.resultDigest }

def advance : Stage → Stage
  | .registered => .encoded
  | .encoded => .verified
  | .verified => .probed
  | .probed => .fallbackReady
  | .fallbackReady => .admitted
  | .admitted => .consumed
  | .consumed => .closed
  | .closed => .closed

def applyEvent (s : State) (kind : EventKind) (p : Packet) : State × Route :=
  let selectedRoute := route s kind p
  if accepted selectedRoute then
    ({s with
      stage := advance s.stage
      lastEventDigest := p.eventDigest
      receiptCount := s.receiptCount + 1
      fallbackCount := if selectedRoute == .routeToFallback then s.fallbackCount + 1 else s.fallbackCount},
      selectedRoute)
  else (s, selectedRoute)

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

def ArtifactStep (s : State) (e : Event) : Option State :=
  if s.stage = .closed then none
  else if accepted (route s e.kind e.packet) then some (applyEvent s e.kind e.packet).1 else none

def ArtifactRun : State → List Event → Option State
  | state, [] => some state
  | state, event :: tail =>
      match ArtifactStep state event with
      | none => none
      | some next => ArtifactRun next tail

def ArtifactTraceAccepted : State → List Event → Prop
  | _, [] => True
  | state, event :: tail =>
      accepted (route state event.kind event.packet) = true ∧
      ArtifactTraceAccepted (applyEvent state event.kind event.packet).1 tail

theorem accepted_step_is_accepted
    {state next : State} {event : Event}
    (stepped : ArtifactStep state event = some next) :
    accepted (route state event.kind event.packet) = true := by
  unfold ArtifactStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · assumption
    · simp at stepped

theorem accepted_step_applies_event
    {state next : State} {event : Event}
    (stepped : ArtifactStep state event = some next) :
    next = (applyEvent state event.kind event.packet).1 := by
  unfold ArtifactStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · exact Option.some.inj stepped |>.symm
    · simp at stepped

theorem apply_event_preserves_full_identity (state : State) (event : Event) :
    stateIdentity (applyEvent state event.kind event.packet).1 = stateIdentity state := by
  by_cases h : accepted (route state event.kind event.packet) = true <;>
    simp [applyEvent, h, stateIdentity]

theorem accepted_step_preserves_full_identity
    {state next : State} {event : Event}
    (stepped : ArtifactStep state event = some next) :
    stateIdentity next = stateIdentity state := by
  rw [accepted_step_applies_event stepped]
  exact apply_event_preserves_full_identity state event

theorem accepted_step_preserves_non_authority
    {state next : State} {event : Event}
    (stepped : ArtifactStep state event = some next) :
    next.supportAssigned = state.supportAssigned ∧
    next.externalEffectCommitted = state.externalEffectCommitted := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_step_adds_exactly_one_receipt
    {state next : State} {event : Event}
    (stepped : ArtifactStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_step_advances_stage
    {state next : State} {event : Event}
    (stepped : ArtifactStep state event = some next) :
    next.stage = advance state.stage := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem apply_event_fallback_count_monotone (state : State) (event : Event) :
    state.fallbackCount ≤ (applyEvent state event.kind event.packet).1.fallbackCount := by
  cases routed : route state event.kind event.packet <;>
    simp [applyEvent, routed, accepted]

theorem accepted_step_fallback_count_monotone
    {state next : State} {event : Event}
    (stepped : ArtifactStep state event = some next) :
    state.fallbackCount ≤ next.fallbackCount := by
  rw [accepted_step_applies_event stepped]
  exact apply_event_fallback_count_monotone state event

theorem accepted_run_preserves_full_identity
    {state final : State} {events : List Event}
    (ran : ArtifactRun state events = some final) :
    stateIdentity final = stateIdentity state := by
  induction events generalizing state with
  | nil => simp [ArtifactRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ArtifactStep state event with
      | none => simp [ArtifactRun, stepped] at ran
      | some next =>
          have tailRan : ArtifactRun next tail = some final := by
            simpa [ArtifactRun, stepped] using ran
          exact (ih tailRan).trans (accepted_step_preserves_full_identity stepped)

theorem accepted_run_preserves_support
    {state final : State} {events : List Event}
    (ran : ArtifactRun state events = some final) :
    final.supportAssigned = state.supportAssigned := by
  induction events generalizing state with
  | nil => simp [ArtifactRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ArtifactStep state event with
      | none => simp [ArtifactRun, stepped] at ran
      | some next =>
          have tailRan : ArtifactRun next tail = some final := by
            simpa [ArtifactRun, stepped] using ran
          exact (ih tailRan).trans (accepted_step_preserves_non_authority stepped).1

theorem accepted_run_preserves_external_effect
    {state final : State} {events : List Event}
    (ran : ArtifactRun state events = some final) :
    final.externalEffectCommitted = state.externalEffectCommitted := by
  induction events generalizing state with
  | nil => simp [ArtifactRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ArtifactStep state event with
      | none => simp [ArtifactRun, stepped] at ran
      | some next =>
          have tailRan : ArtifactRun next tail = some final := by
            simpa [ArtifactRun, stepped] using ran
          exact (ih tailRan).trans (accepted_step_preserves_non_authority stepped).2

theorem accepted_run_accounts_exact_receipts
    {state final : State} {events : List Event}
    (ran : ArtifactRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil => simp [ArtifactRun] at ran; subst final; simp
  | cons event tail ih =>
      cases stepped : ArtifactStep state event with
      | none => simp [ArtifactRun, stepped] at ran
      | some next =>
          have tailRan : ArtifactRun next tail = some final := by
            simpa [ArtifactRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [accepted_step_adds_exactly_one_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem accepted_run_fallback_count_monotone
    {state final : State} {events : List Event}
    (ran : ArtifactRun state events = some final) :
    state.fallbackCount ≤ final.fallbackCount := by
  induction events generalizing state with
  | nil => simp [ArtifactRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : ArtifactStep state event with
      | none => simp [ArtifactRun, stepped] at ran
      | some next =>
          have tailRan : ArtifactRun next tail = some final := by
            simpa [ArtifactRun, stepped] using ran
          exact Nat.le_trans (accepted_step_fallback_count_monotone stepped) (ih tailRan)

theorem accepted_run_has_accepted_trace
    {state final : State} {events : List Event}
    (ran : ArtifactRun state events = some final) :
    ArtifactTraceAccepted state events := by
  induction events generalizing state with
  | nil => simp [ArtifactTraceAccepted]
  | cons event tail ih =>
      cases stepped : ArtifactStep state event with
      | none => simp [ArtifactRun, stepped] at ran
      | some next =>
          have tailRan : ArtifactRun next tail = some final := by
            simpa [ArtifactRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          subst next
          exact ⟨accepted_step_is_accepted stepped, ih tailRan⟩

theorem artifact_run_append
    (state middle : State) (left right : List Event)
    (leftRan : ArtifactRun state left = some middle) :
    ArtifactRun state (left ++ right) = ArtifactRun middle right := by
  induction left generalizing state with
  | nil => simp [ArtifactRun] at leftRan; subst middle; rfl
  | cons event tail ih =>
      cases stepped : ArtifactStep state event with
      | none => simp [ArtifactRun, stepped] at leftRan
      | some next =>
          have tailRan : ArtifactRun next tail = some middle := by
            simpa [ArtifactRun, stepped] using leftRan
          simpa [ArtifactRun, stepped] using ih next tailRan

theorem closed_state_accepts_no_event
    {state : State} (closed : state.stage = .closed) (event : Event) :
    ArtifactStep state event = none := by
  simp [ArtifactStep, closed]

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

def eventAt (kind : EventKind) (digest : Nat) (selectedPacket : Packet := completePacket) : Event :=
  { kind := kind, packet := {selectedPacket with eventDigest := digest} }

def exactLifecycleEvents : List Event :=
  [eventAt .bindArtifact 101,
   eventAt .recordEncoding 102,
   eventAt .verifyReconstruction 103,
   eventAt .probeConsumer 104,
   eventAt .prepareFallback 105,
   eventAt .admitUse 106,
   eventAt .recordConsumption 107]

def fallbackLifecycleEvents : List Event :=
  [eventAt .bindArtifact 101,
   eventAt .recordEncoding 102,
   eventAt .verifyReconstruction 103,
   eventAt .probeConsumer 104 {completePacket with taskProbePassed := false},
   eventAt .prepareFallback 105,
   eventAt .admitUse 106,
   eventAt .recordConsumption 107]

def exactLifecycleFinal : State :=
  {completeState .closed with lastEventDigest := 107, receiptCount := 7}

def fallbackLifecycleFinal : State :=
  {completeState .closed with lastEventDigest := 107, receiptCount := 7, fallbackCount := 1}

theorem exact_lifecycle_reaches_closed_with_receipts :
    ArtifactRun (completeState .registered) exactLifecycleEvents = some exactLifecycleFinal := by
  native_decide

theorem failed_probe_lifecycle_reaches_closed_with_one_fallback :
    ArtifactRun (completeState .registered) fallbackLifecycleEvents = some fallbackLifecycleFinal := by
  native_decide

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
