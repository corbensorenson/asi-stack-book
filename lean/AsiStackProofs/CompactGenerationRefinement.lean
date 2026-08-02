namespace AsiStackProofs.CompactGenerationRefinement

inductive Stage where
  | requested | sourceBound | generated | verified | residualized
  | published | migrated | consumed | closed
deriving DecidableEq, Repr

inductive EventKind where
  | bindSource | generate | verify | residualize
  | publish | migrate | consume | close
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectRepresentationSubstitution | rejectConsumerSubstitution
  | rejectResultDigestSubstitution | rejectEventReplay | rejectAuthorityLeak
  | rejectMalformedRequest | requireSourceArtifact | requireSourceDigest | requireRights
  | requireVersionedContract | requireCompressionBoundary | requireConsumerPolicy
  | requireGenerator | requireSeedOrLaw | requireSearchBound | requireGeneratedArtifact
  | requireGenerationCost | blockLossyExactness | requireVerifierIdentity
  | requireIndependentEvaluator | requireObservedReconstruction | requireExecutableFallback
  | requireVerifierCost | requireObligationScan | requireResidualRecord
  | requireResidualOwner | requireResidualBurden | blockZeroResidualOverclaim
  | requireSourceProvenance | requireTotalCost | requireFallbackReceipt
  | requireArtifactReceipt | requireBoundResultDigests | requireEvidenceTransition
  | requirePublicationNonClaims | requireProvenanceIdentity | requireProvenanceContent
  | requireGroundingEvaluator | requireMigrationRecord | requireReferenceContinuity
  | requireConsumerMap | requireConsumerAcknowledgment | requirePolicyCompatibility
  | requireDownstreamEvaluation | requireUtilityMeasurement | requireResidualClosure
  | requireChainIntegrity | requireDescendantReferences | requireCleanup
  | requireFinalNonClaims | acceptSourceBinding | acceptGeneration
  | acceptVerification | activateFallback | acceptResidualization
  | acceptPublication | acceptMigration | acceptConsumption | acceptClosure
deriving DecidableEq, Repr

structure Packet where
  representationId : Nat
  representationVersion : Nat
  sourceDigest : Nat
  contractDigest : Nat
  generatorDigest : Nat
  targetDigest : Nat
  verifierDigest : Nat
  residualLedgerDigest : Nat
  consumerDigest : Nat
  resultSetDigest : Nat
  eventDigest : Nat
  requestWellFormed : Bool
  sourceArtifactPresent : Bool
  sourceDigestBound : Bool
  rightsBound : Bool
  versionedContract : Bool
  compressionBoundary : Bool
  consumerPolicy : Bool
  generatorPresent : Bool
  seedOrLawPresent : Bool
  searchBound : Bool
  generatedArtifactPresent : Bool
  generationCostRecorded : Bool
  lossyRepresentation : Bool
  exactClaim : Bool
  verifierIdentity : Bool
  independentEvaluator : Bool
  observedReconstruction : Bool
  targetDigestMatches : Bool
  verificationPassed : Bool
  fallbackExecutable : Bool
  fullSourcePreserved : Bool
  verifierCostRecorded : Bool
  obligationScan : Bool
  unresolvedObligations : Bool
  residualRecordPresent : Bool
  residualOwner : Bool
  residualBurdenRecorded : Bool
  declaredZeroResidual : Bool
  sourceProvenance : Bool
  totalCostRecorded : Bool
  fallbackReceipt : Bool
  artifactReceipt : Bool
  resultDigestsBound : Bool
  supportPromotionRequested : Bool
  evidenceTransitionPresent : Bool
  publicationNonClaims : Bool
  semanticNodeUsed : Bool
  provenanceIdentity : Bool
  provenanceContent : Bool
  groundingEvaluator : Bool
  hierarchyChanged : Bool
  migrationRecord : Bool
  priorReferencesPreserved : Bool
  supersessionRecorded : Bool
  consumerMap : Bool
  consumerAcknowledgment : Bool
  policyCompatible : Bool
  downstreamEvaluation : Bool
  utilityMeasured : Bool
  residualClosedOrEscrowed : Bool
  chainIntegrity : Bool
  descendantReferences : Bool
  cleanup : Bool
  finalNonClaims : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  representationId : Nat
  representationVersion : Nat
  sourceDigest : Nat
  contractDigest : Nat
  generatorDigest : Nat
  targetDigest : Nat
  verifierDigest : Nat
  residualLedgerDigest : Nat
  consumerDigest : Nat
  resultSetDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  generationCount : Nat
  verificationCount : Nat
  fallbackCount : Nat
  migrationCount : Nat
  consumptionCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .requested => .bindSource | .sourceBound => .generate | .generated => .verify
  | .verified => .residualize | .residualized => .publish | .published => .migrate
  | .migrated => .consume | .consumed => .close | .closed => .close

def exactRepresentation (s : State) (p : Packet) : Bool :=
  p.representationId == s.representationId &&
  p.representationVersion == s.representationVersion &&
  p.sourceDigest == s.sourceDigest && p.contractDigest == s.contractDigest &&
  p.generatorDigest == s.generatorDigest && p.targetDigest == s.targetDigest &&
  p.verifierDigest == s.verifierDigest &&
  p.residualLedgerDigest == s.residualLedgerDigest

def exactConsumer (s : State) (p : Packet) : Bool :=
  p.consumerDigest == s.consumerDigest

def exactResults (s : State) (p : Packet) : Bool :=
  p.resultSetDigest == s.resultSetDigest

def routeFor (s : State) (e : Event) : Route :=
  if e.kind != expectedKind s.stage then .rejectWrongStage
  else if !exactRepresentation s e.packet then .rejectRepresentationSubstitution
  else if !exactConsumer s e.packet then .rejectConsumerSubstitution
  else if !exactResults s e.packet then .rejectResultDigestSubstitution
  else if e.packet.eventDigest == s.lastEventDigest then .rejectEventReplay
  else if e.packet.externalEffectRequested then .rejectAuthorityLeak
  else match s.stage with
  | .requested =>
      if !e.packet.requestWellFormed then .rejectMalformedRequest
      else if !e.packet.sourceArtifactPresent then .requireSourceArtifact
      else if !e.packet.sourceDigestBound then .requireSourceDigest
      else if !e.packet.rightsBound then .requireRights
      else if !e.packet.versionedContract then .requireVersionedContract
      else if !e.packet.compressionBoundary then .requireCompressionBoundary
      else if !e.packet.consumerPolicy then .requireConsumerPolicy
      else .acceptSourceBinding
  | .sourceBound =>
      if !e.packet.generatorPresent then .requireGenerator
      else if !e.packet.seedOrLawPresent then .requireSeedOrLaw
      else if !e.packet.searchBound then .requireSearchBound
      else if !e.packet.generatedArtifactPresent then .requireGeneratedArtifact
      else if !e.packet.generationCostRecorded then .requireGenerationCost
      else .acceptGeneration
  | .generated =>
      if e.packet.lossyRepresentation && e.packet.exactClaim then .blockLossyExactness
      else if !e.packet.verifierIdentity then .requireVerifierIdentity
      else if !e.packet.independentEvaluator then .requireIndependentEvaluator
      else if !e.packet.observedReconstruction then .requireObservedReconstruction
      else if (e.packet.exactClaim && !e.packet.targetDigestMatches) ||
          !e.packet.verificationPassed then
        if e.packet.fallbackExecutable && e.packet.fullSourcePreserved then
          .activateFallback
        else .requireExecutableFallback
      else if !e.packet.verifierCostRecorded then .requireVerifierCost
      else .acceptVerification
  | .verified =>
      if !e.packet.obligationScan then .requireObligationScan
      else if e.packet.unresolvedObligations && !e.packet.residualRecordPresent then
        .requireResidualRecord
      else if e.packet.unresolvedObligations && !e.packet.residualOwner then
        .requireResidualOwner
      else if e.packet.unresolvedObligations && !e.packet.residualBurdenRecorded then
        .requireResidualBurden
      else if e.packet.unresolvedObligations && e.packet.declaredZeroResidual then
        .blockZeroResidualOverclaim
      else if !e.packet.sourceProvenance then .requireSourceProvenance
      else if !e.packet.totalCostRecorded then .requireTotalCost
      else if s.fallbackCount > 0 && !e.packet.fallbackReceipt then .requireFallbackReceipt
      else .acceptResidualization
  | .residualized =>
      if !e.packet.artifactReceipt then .requireArtifactReceipt
      else if !e.packet.resultDigestsBound then .requireBoundResultDigests
      else if e.packet.supportPromotionRequested && !e.packet.evidenceTransitionPresent then
        .requireEvidenceTransition
      else if !e.packet.publicationNonClaims then .requirePublicationNonClaims
      else .acceptPublication
  | .published =>
      if e.packet.semanticNodeUsed && !e.packet.provenanceIdentity then
        .requireProvenanceIdentity
      else if e.packet.semanticNodeUsed && !e.packet.provenanceContent then
        .requireProvenanceContent
      else if e.packet.semanticNodeUsed && !e.packet.groundingEvaluator then
        .requireGroundingEvaluator
      else if e.packet.hierarchyChanged && !e.packet.migrationRecord then
        .requireMigrationRecord
      else if e.packet.hierarchyChanged &&
          !(e.packet.priorReferencesPreserved || e.packet.supersessionRecorded) then
        .requireReferenceContinuity
      else if e.packet.hierarchyChanged && !e.packet.consumerMap then .requireConsumerMap
      else .acceptMigration
  | .migrated =>
      if !e.packet.consumerAcknowledgment then .requireConsumerAcknowledgment
      else if !e.packet.policyCompatible then .requirePolicyCompatibility
      else if !e.packet.downstreamEvaluation then .requireDownstreamEvaluation
      else if !e.packet.utilityMeasured then .requireUtilityMeasurement
      else .acceptConsumption
  | .consumed =>
      if !e.packet.residualClosedOrEscrowed then .requireResidualClosure
      else if !e.packet.chainIntegrity then .requireChainIntegrity
      else if !e.packet.descendantReferences then .requireDescendantReferences
      else if !e.packet.cleanup then .requireCleanup
      else if !e.packet.finalNonClaims then .requireFinalNonClaims
      else .acceptClosure
  | .closed => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptSourceBinding | .acceptGeneration | .acceptVerification | .activateFallback
  | .acceptResidualization | .acceptPublication | .acceptMigration
  | .acceptConsumption | .acceptClosure => true
  | _ => false

def advance : Stage -> Stage
  | .requested => .sourceBound | .sourceBound => .generated | .generated => .verified
  | .verified => .residualized | .residualized => .published | .published => .migrated
  | .migrated => .consumed | .consumed => .closed | .closed => .closed

def applyEvent (s : State) (e : Event) : State × Route :=
  let r := routeFor s e
  if accepted r then
    ({s with
      stage := advance s.stage
      lastEventDigest := e.packet.eventDigest
      receiptCount := s.receiptCount + 1
      generationCount := if s.stage == .sourceBound then s.generationCount + 1 else s.generationCount
      verificationCount := if s.stage == .generated then s.verificationCount + 1 else s.verificationCount
      fallbackCount := if r == .activateFallback then s.fallbackCount + 1 else s.fallbackCount
      migrationCount := if s.stage == .published then s.migrationCount + 1 else s.migrationCount
      consumptionCount := if s.stage == .migrated then s.consumptionCount + 1 else s.consumptionCount}, r)
  else (s, r)

structure StateIdentity where
  representationId : Nat
  representationVersion : Nat
  sourceDigest : Nat
  contractDigest : Nat
  generatorDigest : Nat
  targetDigest : Nat
  verifierDigest : Nat
  residualLedgerDigest : Nat
  consumerDigest : Nat
  resultSetDigest : Nat
deriving DecidableEq, Repr

def stateIdentity (s : State) : StateIdentity :=
  { representationId := s.representationId
    representationVersion := s.representationVersion
    sourceDigest := s.sourceDigest
    contractDigest := s.contractDigest
    generatorDigest := s.generatorDigest
    targetDigest := s.targetDigest
    verifierDigest := s.verifierDigest
    residualLedgerDigest := s.residualLedgerDigest
    consumerDigest := s.consumerDigest
    resultSetDigest := s.resultSetDigest }

def CompactStep (s : State) (e : Event) : Option State :=
  if s.stage = .closed then none
  else if accepted (routeFor s e) then some (applyEvent s e).1 else none

def CompactRun : State -> List Event -> Option State
  | state, [] => some state
  | state, event :: tail =>
      match CompactStep state event with
      | none => none
      | some next => CompactRun next tail

def CompactTraceAccepted : State -> List Event -> Prop
  | _, [] => True
  | state, event :: tail =>
      accepted (routeFor state event) = true ∧
      CompactTraceAccepted (applyEvent state event).1 tail

theorem accepted_step_is_accepted
    {state next : State} {event : Event}
    (stepped : CompactStep state event = some next) :
    accepted (routeFor state event) = true := by
  unfold CompactStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · assumption
    · simp at stepped

theorem accepted_step_applies_event
    {state next : State} {event : Event}
    (stepped : CompactStep state event = some next) :
    next = (applyEvent state event).1 := by
  unfold CompactStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · exact Option.some.inj stepped |>.symm
    · simp at stepped

theorem apply_event_preserves_full_identity (state : State) (event : Event) :
    stateIdentity (applyEvent state event).1 = stateIdentity state := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, h, stateIdentity]

theorem accepted_step_preserves_full_identity
    {state next : State} {event : Event}
    (stepped : CompactStep state event = some next) :
    stateIdentity next = stateIdentity state := by
  rw [accepted_step_applies_event stepped]
  exact apply_event_preserves_full_identity state event

theorem accepted_step_preserves_support_and_external_effect_counts
    {state next : State} {event : Event}
    (stepped : CompactStep state event = some next) :
    next.supportAssignmentCount = state.supportAssignmentCount ∧
    next.externalEffectCount = state.externalEffectCount := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_step_adds_exactly_one_receipt
    {state next : State} {event : Event}
    (stepped : CompactStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_step_advances_stage
    {state next : State} {event : Event}
    (stepped : CompactStep state event = some next) :
    next.stage = advance state.stage := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem apply_event_fallback_count_monotone (state : State) (event : Event) :
    state.fallbackCount ≤ (applyEvent state event).1.fallbackCount := by
  cases routed : routeFor state event <;>
    simp [applyEvent, routed, accepted]

theorem accepted_step_fallback_count_monotone
    {state next : State} {event : Event}
    (stepped : CompactStep state event = some next) :
    state.fallbackCount ≤ next.fallbackCount := by
  rw [accepted_step_applies_event stepped]
  exact apply_event_fallback_count_monotone state event

theorem accepted_run_preserves_full_identity
    {state final : State} {events : List Event}
    (ran : CompactRun state events = some final) :
    stateIdentity final = stateIdentity state := by
  induction events generalizing state with
  | nil => simp [CompactRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : CompactStep state event with
      | none => simp [CompactRun, stepped] at ran
      | some next =>
          have tailRan : CompactRun next tail = some final := by
            simpa [CompactRun, stepped] using ran
          exact (ih tailRan).trans (accepted_step_preserves_full_identity stepped)

theorem accepted_run_preserves_support_count
    {state final : State} {events : List Event}
    (ran : CompactRun state events = some final) :
    final.supportAssignmentCount = state.supportAssignmentCount := by
  induction events generalizing state with
  | nil => simp [CompactRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : CompactStep state event with
      | none => simp [CompactRun, stepped] at ran
      | some next =>
          have tailRan : CompactRun next tail = some final := by
            simpa [CompactRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_step_preserves_support_and_external_effect_counts stepped).1

theorem accepted_run_preserves_external_effect_count
    {state final : State} {events : List Event}
    (ran : CompactRun state events = some final) :
    final.externalEffectCount = state.externalEffectCount := by
  induction events generalizing state with
  | nil => simp [CompactRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : CompactStep state event with
      | none => simp [CompactRun, stepped] at ran
      | some next =>
          have tailRan : CompactRun next tail = some final := by
            simpa [CompactRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_step_preserves_support_and_external_effect_counts stepped).2

theorem accepted_run_accounts_exact_receipts
    {state final : State} {events : List Event}
    (ran : CompactRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil => simp [CompactRun] at ran; subst final; simp
  | cons event tail ih =>
      cases stepped : CompactStep state event with
      | none => simp [CompactRun, stepped] at ran
      | some next =>
          have tailRan : CompactRun next tail = some final := by
            simpa [CompactRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [accepted_step_adds_exactly_one_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem accepted_run_fallback_count_monotone
    {state final : State} {events : List Event}
    (ran : CompactRun state events = some final) :
    state.fallbackCount ≤ final.fallbackCount := by
  induction events generalizing state with
  | nil => simp [CompactRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : CompactStep state event with
      | none => simp [CompactRun, stepped] at ran
      | some next =>
          have tailRan : CompactRun next tail = some final := by
            simpa [CompactRun, stepped] using ran
          exact Nat.le_trans (accepted_step_fallback_count_monotone stepped) (ih tailRan)

theorem accepted_run_has_accepted_trace
    {state final : State} {events : List Event}
    (ran : CompactRun state events = some final) :
    CompactTraceAccepted state events := by
  induction events generalizing state with
  | nil => simp [CompactTraceAccepted]
  | cons event tail ih =>
      cases stepped : CompactStep state event with
      | none => simp [CompactRun, stepped] at ran
      | some next =>
          have tailRan : CompactRun next tail = some final := by
            simpa [CompactRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          subst next
          exact ⟨accepted_step_is_accepted stepped, ih tailRan⟩

theorem compact_run_append
    (state middle : State) (left right : List Event)
    (leftRan : CompactRun state left = some middle) :
    CompactRun state (left ++ right) = CompactRun middle right := by
  induction left generalizing state with
  | nil => simp [CompactRun] at leftRan; subst middle; rfl
  | cons event tail ih =>
      cases stepped : CompactStep state event with
      | none => simp [CompactRun, stepped] at leftRan
      | some next =>
          have tailRan : CompactRun next tail = some middle := by
            simpa [CompactRun, stepped] using leftRan
          simpa [CompactRun, stepped] using ih next tailRan

theorem closed_state_accepts_no_event
    {state : State} (closed : state.stage = .closed) (event : Event) :
    CompactStep state event = none := by
  simp [CompactStep, closed]

theorem apply_event_preserves_bound_representation_and_result_identity (s : State) (e : Event) :
    (applyEvent s e).1.representationId = s.representationId ∧
    (applyEvent s e).1.sourceDigest = s.sourceDigest ∧
    (applyEvent s e).1.targetDigest = s.targetDigest ∧
    (applyEvent s e).1.resultSetDigest = s.resultSetDigest := by
  by_cases h : accepted (routeFor s e) = true <;> simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_effect (s : State) (e : Event) :
    (applyEvent s e).1.supportAssignmentCount = s.supportAssignmentCount ∧
    (applyEvent s e).1.externalEffectCount = s.externalEffectCount := by
  by_cases h : accepted (routeFor s e) = true <;> simp [applyEvent, h]

theorem accepted_step_adds_one_receipt (s : State) (e : Event)
    (h : accepted (routeFor s e) = true) :
    (applyEvent s e).1.receiptCount = s.receiptCount + 1 := by
  simp [applyEvent, h]

def completePacket : Packet :=
  { representationId := 2001, representationVersion := 3, sourceDigest := 2002
    contractDigest := 2003, generatorDigest := 2004, targetDigest := 2005
    verifierDigest := 2006, residualLedgerDigest := 2007, consumerDigest := 2008
    resultSetDigest := 2009, eventDigest := 1, requestWellFormed := true
    sourceArtifactPresent := true, sourceDigestBound := true, rightsBound := true
    versionedContract := true, compressionBoundary := true, consumerPolicy := true
    generatorPresent := true, seedOrLawPresent := true, searchBound := true
    generatedArtifactPresent := true, generationCostRecorded := true
    lossyRepresentation := false, exactClaim := true, verifierIdentity := true
    independentEvaluator := true, observedReconstruction := true
    targetDigestMatches := true, verificationPassed := true
    fallbackExecutable := true, fullSourcePreserved := true, verifierCostRecorded := true
    obligationScan := true, unresolvedObligations := true, residualRecordPresent := true
    residualOwner := true, residualBurdenRecorded := true, declaredZeroResidual := false
    sourceProvenance := true, totalCostRecorded := true, fallbackReceipt := true
    artifactReceipt := true, resultDigestsBound := true
    supportPromotionRequested := false, evidenceTransitionPresent := true
    publicationNonClaims := true, semanticNodeUsed := true, provenanceIdentity := true
    provenanceContent := true, groundingEvaluator := true, hierarchyChanged := true
    migrationRecord := true, priorReferencesPreserved := true
    supersessionRecorded := false, consumerMap := true, consumerAcknowledgment := true
    policyCompatible := true, downstreamEvaluation := true, utilityMeasured := true
    residualClosedOrEscrowed := true, chainIntegrity := true
    descendantReferences := true, cleanup := true, finalNonClaims := true
    externalEffectRequested := false }

def stateAt (stage : Stage) : State :=
  { stage := stage, representationId := 2001, representationVersion := 3
    sourceDigest := 2002, contractDigest := 2003, generatorDigest := 2004
    targetDigest := 2005, verifierDigest := 2006, residualLedgerDigest := 2007
    consumerDigest := 2008, resultSetDigest := 2009, lastEventDigest := 0
    receiptCount := 0, generationCount := 0, verificationCount := 0
    fallbackCount := 0, migrationCount := 0, consumptionCount := 0
    supportAssignmentCount := 0, externalEffectCount := 0 }

theorem fallback_receipt_required_after_activated_fallback :
    routeFor {stateAt .verified with fallbackCount := 1}
      {kind := .residualize, packet := {completePacket with fallbackReceipt := false}} =
      .requireFallbackReceipt := by rfl

theorem source_substitution_rejected :
    routeFor (stateAt .requested)
      {kind := .bindSource, packet := {completePacket with sourceDigest := 999}} =
      .rejectRepresentationSubstitution := by rfl
theorem missing_rights_blocks_source_binding :
    routeFor (stateAt .requested)
      {kind := .bindSource, packet := {completePacket with rightsBound := false}} =
      .requireRights := by rfl
theorem missing_generated_artifact_blocks_generation :
    routeFor (stateAt .sourceBound)
      {kind := .generate, packet := {completePacket with generatedArtifactPresent := false}} =
      .requireGeneratedArtifact := by rfl
theorem lossy_exactness_is_blocked_before_verification :
    routeFor (stateAt .generated)
      {kind := .verify, packet := {completePacket with lossyRepresentation := true}} =
      .blockLossyExactness := by rfl
theorem reconstruction_mismatch_activates_preserved_source_fallback :
    routeFor (stateAt .generated)
      {kind := .verify, packet := {completePacket with targetDigestMatches := false}} =
      .activateFallback := by rfl
theorem reconstruction_mismatch_without_executable_fallback_is_blocked :
    routeFor (stateAt .generated)
      {kind := .verify, packet := {completePacket with targetDigestMatches := false, fallbackExecutable := false}} =
      .requireExecutableFallback := by rfl
theorem unresolved_obligation_without_owner_blocks_residualization :
    routeFor (stateAt .verified)
      {kind := .residualize, packet := {completePacket with residualOwner := false}} =
      .requireResidualOwner := by rfl
theorem result_digest_substitution_blocks_publication :
    routeFor (stateAt .residualized)
      {kind := .publish, packet := {completePacket with resultSetDigest := 999}} =
      .rejectResultDigestSubstitution := by rfl
theorem support_promotion_without_transition_blocks_publication :
    routeFor (stateAt .residualized)
      {kind := .publish, packet := {completePacket with supportPromotionRequested := true, evidenceTransitionPresent := false}} =
      .requireEvidenceTransition := by rfl
theorem semantic_node_without_provenance_identity_blocks_migration :
    routeFor (stateAt .published)
      {kind := .migrate, packet := {completePacket with provenanceIdentity := false}} =
      .requireProvenanceIdentity := by rfl
theorem hierarchy_change_without_reference_continuity_blocks_migration :
    routeFor (stateAt .published)
      {kind := .migrate, packet := {completePacket with priorReferencesPreserved := false, supersessionRecorded := false}} =
      .requireReferenceContinuity := by rfl
theorem incompatible_consumer_policy_blocks_consumption :
    routeFor (stateAt .migrated)
      {kind := .consume, packet := {completePacket with policyCompatible := false}} =
      .requirePolicyCompatibility := by rfl
theorem broken_residual_chain_blocks_closure :
    routeFor (stateAt .consumed)
      {kind := .close, packet := {completePacket with chainIntegrity := false}} =
      .requireChainIntegrity := by rfl

def event (kind : EventKind) (digest : Nat) (packet : Packet := completePacket) : Event :=
  {kind := kind, packet := {packet with eventDigest := digest}}

theorem fallback_lifecycle_reaches_closed_without_support_or_effect_authority :
  let s0 := stateAt .requested
  let s1 := (applyEvent s0 (event .bindSource 1)).1
  let s2 := (applyEvent s1 (event .generate 2)).1
  let s3 := (applyEvent s2 (event .verify 3 {completePacket with verificationPassed := false})).1
  let s4 := (applyEvent s3 (event .residualize 4)).1
  let s5 := (applyEvent s4 (event .publish 5)).1
  let s6 := (applyEvent s5 (event .migrate 6)).1
  let s7 := (applyEvent s6 (event .consume 7)).1
  let s8 := (applyEvent s7 (event .close 8)).1
  s8.stage = .closed ∧ s8.receiptCount = 8 ∧ s8.generationCount = 1 ∧
  s8.verificationCount = 1 ∧ s8.fallbackCount = 1 ∧ s8.migrationCount = 1 ∧
  s8.consumptionCount = 1 ∧ s8.supportAssignmentCount = 0 ∧
  s8.externalEffectCount = 0 := by native_decide

end AsiStackProofs.CompactGenerationRefinement
