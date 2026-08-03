namespace AsiStackProofs.ProofCarryingContracts

structure ProofContractReceipt where
  theoremRefsPresent : Bool
  deterministicFieldsPresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def ReceiptBoundaryComplete (receipt : ProofContractReceipt) : Prop :=
  receipt.theoremRefsPresent = true ∧
    receipt.deterministicFieldsPresent = true ∧
      receipt.nonClaimBoundaryPresent = true

def ReadyForDownstreamUse (receipt : ProofContractReceipt) : Prop :=
  ReceiptBoundaryComplete receipt

theorem downstream_ready_receipt_missing_boundary_field_rejected
    {receipt : ProofContractReceipt} :
    (receipt.theoremRefsPresent = false ∨
      receipt.deterministicFieldsPresent = false ∨
        receipt.nonClaimBoundaryPresent = false) ->
    ¬ ReadyForDownstreamUse receipt := by
  intro missing ready
  unfold ReadyForDownstreamUse at ready
  unfold ReceiptBoundaryComplete at ready
  cases ready with
  | intro theoremRefs rest =>
      cases rest with
      | intro deterministicFields nonClaimBoundary =>
          cases missing with
          | inl missingTheorems =>
              rw [missingTheorems] at theoremRefs
              contradiction
          | inr missingRest =>
              cases missingRest with
              | inl missingDeterministic =>
                  rw [missingDeterministic] at deterministicFields
                  contradiction
              | inr missingNonClaim =>
                  rw [missingNonClaim] at nonClaimBoundary
                  contradiction

structure DownstreamPromotionReview where
  contractReady : Bool
  workloadPresent : Bool
  baselinePresent : Bool
  metricPresent : Bool
  evidenceArtifactPresent : Bool
  promoted : Bool
deriving DecidableEq, Repr

def PromotionEvidenceComplete (review : DownstreamPromotionReview) : Prop :=
  review.workloadPresent = true ∧
    review.baselinePresent = true ∧
      review.metricPresent = true ∧
        review.evidenceArtifactPresent = true

def ConsumerGateValid (review : DownstreamPromotionReview) : Prop :=
  review.promoted = true ->
    review.contractReady = true ∧ PromotionEvidenceComplete review

theorem contract_readiness_alone_cannot_promote_downstream_claim
    {review : DownstreamPromotionReview} :
    ConsumerGateValid review ->
    review.contractReady = true ->
    (review.workloadPresent = false ∨
      review.baselinePresent = false ∨
        review.metricPresent = false ∨
          review.evidenceArtifactPresent = false) ->
    review.promoted = false := by
  intro valid _ready missing
  cases promoted : review.promoted with
  | false => rfl
  | true =>
      have complete := (valid promoted).2
      unfold PromotionEvidenceComplete at complete
      cases missing with
      | inl noWorkload =>
          rw [noWorkload] at complete
          cases complete.1
      | inr rest =>
          cases rest with
          | inl noBaseline =>
              rw [noBaseline] at complete
              cases complete.2.1
          | inr rest =>
              cases rest with
              | inl noMetric =>
                  rw [noMetric] at complete
                  cases complete.2.2.1
              | inr noEvidence =>
                  rw [noEvidence] at complete
                  cases complete.2.2.2

theorem promoted_downstream_claim_without_contract_ready_rejected
    {review : DownstreamPromotionReview} :
    ConsumerGateValid review ->
    review.promoted = true ->
    review.contractReady = false ->
    False := by
  intro valid promoted notReady
  have ready := (valid promoted).1
  rw [notReady] at ready
  contradiction

structure ReceiptConsumerReview where
  receiptAcceptedForConsumer : Bool
  theoremRefsResolved : Bool
  fingerprintMatches : Bool
  contractFresh : Bool
  consumerAllowed : Bool
  unsupportedTransferClaimed : Bool
  nonClaimsPreserved : Bool
deriving DecidableEq, Repr

def ReceiptConsumerGateValid (review : ReceiptConsumerReview) : Prop :=
  review.receiptAcceptedForConsumer = true ->
    review.theoremRefsResolved = true ∧
      review.fingerprintMatches = true ∧
        review.contractFresh = true ∧
          review.consumerAllowed = true ∧
            review.unsupportedTransferClaimed = false ∧
              review.nonClaimsPreserved = true

theorem consumer_gate_acceptance_with_stale_or_unsupported_receipt_rejected
    {review : ReceiptConsumerReview} :
    review.receiptAcceptedForConsumer = true ->
    (review.theoremRefsResolved = false ∨
      review.fingerprintMatches = false ∨
        review.contractFresh = false ∨
          review.consumerAllowed = false ∨
            review.unsupportedTransferClaimed = true ∨
              review.nonClaimsPreserved = false) ->
    ¬ ReceiptConsumerGateValid review := by
  intro accepted missing valid
  unfold ReceiptConsumerGateValid at valid
  have complete := valid accepted
  cases complete with
  | intro refsResolved rest =>
      cases rest with
      | intro fingerprintOk rest =>
          cases rest with
          | intro fresh rest =>
              cases rest with
              | intro allowed rest =>
                  cases rest with
                  | intro noUnsupported nonClaims =>
                      cases missing with
                      | inl refsMissing =>
                          rw [refsMissing] at refsResolved
                          contradiction
                      | inr restMissing =>
                          cases restMissing with
                          | inl fingerprintMissing =>
                              rw [fingerprintMissing] at fingerprintOk
                              contradiction
                          | inr restMissing =>
                              cases restMissing with
                              | inl stale =>
                                  rw [stale] at fresh
                                  contradiction
                              | inr restMissing =>
                                  cases restMissing with
                                  | inl notAllowed =>
                                      rw [notAllowed] at allowed
                                      contradiction
                                  | inr restMissing =>
                                      cases restMissing with
                                      | inl unsupported =>
                                          rw [unsupported] at noUnsupported
                                          contradiction
                                      | inr nonClaimsMissing =>
                                          rw [nonClaimsMissing] at nonClaims
                                          contradiction

structure ReceiptReplayReview where
  replayMarkedPassing : Bool
  replayCommandPresent : Bool
  sourceDigestMatches : Bool
  receiptFingerprintMatches : Bool
  deterministicFieldsRecomputed : Bool
  theoremRefsPresent : Bool
deriving DecidableEq, Repr

def ReceiptReplayValid (review : ReceiptReplayReview) : Prop :=
  review.replayMarkedPassing = true ->
    review.replayCommandPresent = true ∧
      review.sourceDigestMatches = true ∧
        review.receiptFingerprintMatches = true ∧
          review.deterministicFieldsRecomputed = true ∧
            review.theoremRefsPresent = true

theorem passing_replay_without_replay_artifacts_rejected
    {review : ReceiptReplayReview} :
    review.replayMarkedPassing = true ->
    (review.replayCommandPresent = false ∨
      review.sourceDigestMatches = false ∨
        review.receiptFingerprintMatches = false ∨
          review.deterministicFieldsRecomputed = false ∨
            review.theoremRefsPresent = false) ->
    ¬ ReceiptReplayValid review := by
  intro passing missing valid
  unfold ReceiptReplayValid at valid
  have complete := valid passing
  cases complete with
  | intro commandPresent rest =>
      cases rest with
      | intro sourceDigestOk rest =>
          cases rest with
          | intro fingerprintOk rest =>
              cases rest with
              | intro fieldsRecomputed theoremRefsPresent =>
                  cases missing with
                  | inl commandMissing =>
                      rw [commandMissing] at commandPresent
                      contradiction
                  | inr restMissing =>
                      cases restMissing with
                      | inl sourceDigestMissing =>
                          rw [sourceDigestMissing] at sourceDigestOk
                          contradiction
                      | inr restMissing =>
                          cases restMissing with
                          | inl fingerprintMissing =>
                              rw [fingerprintMissing] at fingerprintOk
                              contradiction
                          | inr restMissing =>
                              cases restMissing with
                              | inl fieldsMissing =>
                                  rw [fieldsMissing] at fieldsRecomputed
                                  contradiction
                              | inr theoremRefsMissing =>
                                  rw [theoremRefsMissing] at theoremRefsPresent
                                  contradiction

structure CirclePublicConsumerGateFixture where
  validReceiptCount : Nat
  expectedInvalidControlCount : Nat
  requiredTheoremCount : Nat
  digestPinned : Bool
  theoremIdsPinned : Bool
  deterministicFieldsPinned : Bool
  digestMismatchRejected : Bool
  missingTheoremRejected : Bool
  staleContractRejected : Bool
  unsupportedTransferRejected : Bool
  supportBlocksPromotion : Bool
  upwardTransitionCreated : Bool
  chapterCorePromoted : Bool
  deployedTransportClaimed : Bool
deriving DecidableEq, Repr

structure CirclePublicConsumerGateAccepted
    (fixture : CirclePublicConsumerGateFixture) : Prop where
  oneValidReceipt : fixture.validReceiptCount = 1
  fourInvalidControls : fixture.expectedInvalidControlCount = 4
  sevenRequiredTheorems : fixture.requiredTheoremCount = 7
  digestPinned : fixture.digestPinned = true
  theoremIdsPinned : fixture.theoremIdsPinned = true
  deterministicFieldsPinned : fixture.deterministicFieldsPinned = true
  digestMismatchRejected : fixture.digestMismatchRejected = true
  missingTheoremRejected : fixture.missingTheoremRejected = true
  staleContractRejected : fixture.staleContractRejected = true
  unsupportedTransferRejected : fixture.unsupportedTransferRejected = true
  supportBlocksPromotion : fixture.supportBlocksPromotion = true
  noUpwardTransition : fixture.upwardTransitionCreated = false
  noChapterCorePromotion : fixture.chapterCorePromoted = false
  noDeployedTransportClaim : fixture.deployedTransportClaimed = false

theorem circle_public_consumer_gate_promotion_overclaim_rejected
    {fixture : CirclePublicConsumerGateFixture} :
    (fixture.upwardTransitionCreated = true ∨
      fixture.chapterCorePromoted = true ∨
        fixture.deployedTransportClaimed = true) ->
    ¬ CirclePublicConsumerGateAccepted fixture := by
  intro overclaim accepted
  cases overclaim with
  | inl upward =>
      have noUpward := accepted.noUpwardTransition
      rw [upward] at noUpward
      contradiction
  | inr rest =>
      cases rest with
      | inl corePromotion =>
          have noCorePromotion := accepted.noChapterCorePromotion
          rw [corePromotion] at noCorePromotion
          contradiction
      | inr transportClaim =>
          have noTransportClaim := accepted.noDeployedTransportClaim
          rw [transportClaim] at noTransportClaim
          contradiction

theorem circle_public_consumer_gate_missing_mutation_control_rejected
    {fixture : CirclePublicConsumerGateFixture} :
    (fixture.digestMismatchRejected = false ∨
      fixture.missingTheoremRejected = false ∨
        fixture.staleContractRejected = false ∨
          fixture.unsupportedTransferRejected = false) ->
    ¬ CirclePublicConsumerGateAccepted fixture := by
  intro missing accepted
  cases missing with
  | inl digestMismatchNotRejected =>
      have digestMismatchRejected := accepted.digestMismatchRejected
      rw [digestMismatchNotRejected] at digestMismatchRejected
      contradiction
  | inr rest =>
      cases rest with
      | inl missingTheoremNotRejected =>
          have missingTheoremRejected := accepted.missingTheoremRejected
          rw [missingTheoremNotRejected] at missingTheoremRejected
          contradiction
      | inr rest =>
          cases rest with
          | inl staleContractNotRejected =>
              have staleContractRejected := accepted.staleContractRejected
              rw [staleContractNotRejected] at staleContractRejected
              contradiction
          | inr unsupportedTransferNotRejected =>
              have unsupportedTransferRejected := accepted.unsupportedTransferRejected
              rw [unsupportedTransferNotRejected] at unsupportedTransferRejected
              contradiction

/-! ## Versioned transport and descendant revocation

This finite state machine models only repository-local contract lifecycle
semantics. Digests and Boolean checks are authored inputs. The results do not
establish that an external theorem resolves, that a formal model refines a
deployed implementation, or that any transport service is authenticated,
available, useful, independently reproduced, or deployed.
-/

inductive ContractStage where
  | absent
  | authored
  | resolved
  | ready
  | consumed
  | revoked
deriving DecidableEq, Repr

inductive ContractTransportEvent where
  | resolveRoot
  | attestRoot
  | issueDescendant
  | resolveDescendant
  | attestDescendant
  | consumeDescendant
  | revokeRoot
  | consumeIndependent
deriving DecidableEq, Repr

inductive ContractTransportRoute where
  | accepted
  | rejectStage
  | rejectIdentity
  | rejectParent
  | rejectRevoked
deriving DecidableEq, Repr

structure ContractTransportState where
  rootStage : ContractStage := .authored
  descendantStage : ContractStage := .absent
  independentStage : ContractStage := .ready
  rootTheoremDigest : Nat := 4101
  expectedRootTheoremDigest : Nat := 4101
  descendantTheoremDigest : Nat := 4102
  expectedDescendantTheoremDigest : Nat := 4102
  descendantParentDigest : Nat := 4101
  expectedParentDigest : Nat := 4101
  consumerDigest : Nat := 4103
  expectedConsumerDigest : Nat := 4103
  supportAssignments : Nat := 0
  externalEffects : Nat := 0
deriving DecidableEq, Repr

def ContractTransportCustody
    (before after : ContractTransportState) : Prop :=
  after.rootTheoremDigest = before.rootTheoremDigest ∧
    after.expectedRootTheoremDigest = before.expectedRootTheoremDigest ∧
    after.descendantTheoremDigest = before.descendantTheoremDigest ∧
    after.expectedDescendantTheoremDigest = before.expectedDescendantTheoremDigest ∧
    after.descendantParentDigest = before.descendantParentDigest ∧
    after.expectedParentDigest = before.expectedParentDigest ∧
    after.consumerDigest = before.consumerDigest ∧
    after.expectedConsumerDigest = before.expectedConsumerDigest ∧
    after.supportAssignments = before.supportAssignments ∧
    after.externalEffects = before.externalEffects

def ContractTransportInvariant (state : ContractTransportState) : Prop :=
  state.supportAssignments = 0 ∧
    state.externalEffects = 0 ∧
      (state.rootStage = .revoked -> state.descendantStage = .revoked)

def RootLineageContained (state : ContractTransportState) : Prop :=
  state.rootStage = .revoked ∧ state.descendantStage = .revoked

def IndependentLineageAvailable (state : ContractTransportState) : Prop :=
  state.independentStage = .ready ∨ state.independentStage = .consumed

def rootIdentityExact (state : ContractTransportState) : Bool :=
  state.rootTheoremDigest == state.expectedRootTheoremDigest

def descendantIdentityExact (state : ContractTransportState) : Bool :=
  state.descendantTheoremDigest == state.expectedDescendantTheoremDigest

def descendantParentExact (state : ContractTransportState) : Bool :=
  state.descendantParentDigest == state.expectedParentDigest

def consumerIdentityExact (state : ContractTransportState) : Bool :=
  state.consumerDigest == state.expectedConsumerDigest

def rootLineageRevoked (state : ContractTransportState) : Bool :=
  state.rootStage == .revoked

def descendantUsable (state : ContractTransportState) : Bool :=
  ! rootLineageRevoked state &&
    (state.descendantStage == .ready || state.descendantStage == .consumed)

def revokeRootLineage (state : ContractTransportState) : ContractTransportState :=
  { state with rootStage := .revoked, descendantStage := .revoked }

def contractTransportStep
    (state : ContractTransportState)
    (event : ContractTransportEvent) :
    ContractTransportRoute × ContractTransportState :=
  match event with
  | .resolveRoot =>
      if state.rootStage != .authored then (.rejectStage, state)
      else if ! rootIdentityExact state then (.rejectIdentity, state)
      else (.accepted, { state with rootStage := .resolved })
  | .attestRoot =>
      if state.rootStage == .resolved then
        (.accepted, { state with rootStage := .ready })
      else (.rejectStage, state)
  | .issueDescendant =>
      if state.rootStage == .revoked then (.rejectRevoked, state)
      else if state.rootStage != .ready || state.descendantStage != .absent then
        (.rejectStage, state)
      else if ! descendantParentExact state then (.rejectParent, state)
      else (.accepted, { state with descendantStage := .authored })
  | .resolveDescendant =>
      if state.rootStage == .revoked || state.descendantStage == .revoked then
        (.rejectRevoked, state)
      else if state.descendantStage != .authored then (.rejectStage, state)
      else if ! descendantIdentityExact state then (.rejectIdentity, state)
      else (.accepted, { state with descendantStage := .resolved })
  | .attestDescendant =>
      if state.rootStage == .revoked || state.descendantStage == .revoked then
        (.rejectRevoked, state)
      else if state.descendantStage == .resolved then
        (.accepted, { state with descendantStage := .ready })
      else (.rejectStage, state)
  | .consumeDescendant =>
      if rootLineageRevoked state || state.descendantStage == .revoked then
        (.rejectRevoked, state)
      else if ! consumerIdentityExact state then (.rejectIdentity, state)
      else if state.descendantStage == .ready then
        (.accepted, { state with descendantStage := .consumed })
      else (.rejectStage, state)
  | .revokeRoot =>
      if state.rootStage == .absent || state.rootStage == .revoked then
        (.rejectStage, state)
      else (.accepted, revokeRootLineage state)
  | .consumeIndependent =>
      if state.independentStage == .revoked then (.rejectRevoked, state)
      else if ! consumerIdentityExact state then (.rejectIdentity, state)
      else if state.independentStage == .ready then
        (.accepted, { state with independentStage := .consumed })
      else (.rejectStage, state)

def runContractTransport :
    ContractTransportState -> List ContractTransportEvent -> ContractTransportState
  | state, [] => state
  | state, event :: rest =>
      runContractTransport (contractTransportStep state event).2 rest

theorem contract_transport_rejected_event_is_noninterfering
    (state : ContractTransportState) (event : ContractTransportEvent)
    (h : (contractTransportStep state event).1 ≠ .accepted) :
    (contractTransportStep state event).2 = state := by
  cases event <;>
    simp_all [contractTransportStep] <;>
    repeat' first | split | simp_all

theorem contract_transport_step_preserves_identity_and_authority
    (state : ContractTransportState) (event : ContractTransportEvent) :
    let next := (contractTransportStep state event).2
    next.rootTheoremDigest = state.rootTheoremDigest ∧
      next.expectedRootTheoremDigest = state.expectedRootTheoremDigest ∧
      next.descendantTheoremDigest = state.descendantTheoremDigest ∧
      next.expectedDescendantTheoremDigest = state.expectedDescendantTheoremDigest ∧
      next.descendantParentDigest = state.descendantParentDigest ∧
      next.expectedParentDigest = state.expectedParentDigest ∧
      next.consumerDigest = state.consumerDigest ∧
      next.expectedConsumerDigest = state.expectedConsumerDigest ∧
      next.supportAssignments = state.supportAssignments ∧
      next.externalEffects = state.externalEffects := by
  cases event <;>
    simp [contractTransportStep, revokeRootLineage] <;>
    repeat' first | split | simp_all

theorem contract_transport_step_preserves_custody
    (state : ContractTransportState) (event : ContractTransportEvent) :
    ContractTransportCustody state (contractTransportStep state event).2 := by
  exact contract_transport_step_preserves_identity_and_authority state event

theorem contract_transport_custody_transitive
    {initial middle final : ContractTransportState}
    (h₁ : ContractTransportCustody initial middle)
    (h₂ : ContractTransportCustody middle final) :
    ContractTransportCustody initial final := by
  unfold ContractTransportCustody at *
  rcases h₁ with ⟨h₁a, h₁b, h₁c, h₁d, h₁e, h₁f, h₁g, h₁h, h₁i, h₁j⟩
  rcases h₂ with ⟨h₂a, h₂b, h₂c, h₂d, h₂e, h₂f, h₂g, h₂h, h₂i, h₂j⟩
  exact ⟨h₂a.trans h₁a, h₂b.trans h₁b, h₂c.trans h₁c,
    h₂d.trans h₁d, h₂e.trans h₁e, h₂f.trans h₁f,
    h₂g.trans h₁g, h₂h.trans h₁h, h₂i.trans h₁i, h₂j.trans h₁j⟩

theorem run_contract_transport_preserves_custody
    (state : ContractTransportState) (events : List ContractTransportEvent) :
    ContractTransportCustody state (runContractTransport state events) := by
  induction events generalizing state with
  | nil => simp [runContractTransport, ContractTransportCustody]
  | cons event rest ih =>
      exact contract_transport_custody_transitive
        (contract_transport_step_preserves_custody state event)
        (ih (contractTransportStep state event).2)

theorem contract_transport_step_preserves_invariant
    (state : ContractTransportState) (event : ContractTransportEvent)
    (h : ContractTransportInvariant state) :
    ContractTransportInvariant (contractTransportStep state event).2 := by
  cases event <;>
    simp [ContractTransportInvariant, contractTransportStep,
      revokeRootLineage, rootLineageRevoked] at * <;>
    repeat' first | split | simp_all

theorem run_contract_transport_preserves_invariant
    (state : ContractTransportState) (events : List ContractTransportEvent)
    (h : ContractTransportInvariant state) :
    ContractTransportInvariant (runContractTransport state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (contractTransportStep state event).2
        (contract_transport_step_preserves_invariant state event h)

theorem root_lineage_containment_survives_one_step
    (state : ContractTransportState) (event : ContractTransportEvent)
    (h : RootLineageContained state) :
    RootLineageContained (contractTransportStep state event).2 := by
  rcases h with ⟨rootRevoked, descendantRevoked⟩
  cases event <;>
    simp [RootLineageContained, contractTransportStep, rootRevoked,
      descendantRevoked, rootLineageRevoked] <;>
    repeat' first | split | simp_all

theorem root_lineage_containment_survives_arbitrary_suffix
    (state : ContractTransportState) (events : List ContractTransportEvent)
    (h : RootLineageContained state) :
    RootLineageContained (runContractTransport state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (contractTransportStep state event).2
        (root_lineage_containment_survives_one_step state event h)

theorem revoked_root_excludes_descendant_use_after_any_suffix
    (state : ContractTransportState) (events : List ContractTransportEvent)
    (h : RootLineageContained state) :
    descendantUsable (runContractTransport state events) = false := by
  have contained := root_lineage_containment_survives_arbitrary_suffix state events h
  simp [descendantUsable, rootLineageRevoked, contained.1]

theorem independent_lineage_availability_survives_one_step
    (state : ContractTransportState) (event : ContractTransportEvent)
    (h : IndependentLineageAvailable state) :
    IndependentLineageAvailable (contractTransportStep state event).2 := by
  rcases h with ready | consumed
  · cases event <;>
      simp [IndependentLineageAvailable, contractTransportStep,
        revokeRootLineage, ready] <;>
      repeat' first | split | simp_all
  · cases event <;>
      simp [IndependentLineageAvailable, contractTransportStep,
        revokeRootLineage, consumed] <;>
      repeat' first | split | simp_all

theorem independent_lineage_availability_survives_arbitrary_suffix
    (state : ContractTransportState) (events : List ContractTransportEvent)
    (h : IndependentLineageAvailable state) :
    IndependentLineageAvailable (runContractTransport state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (contractTransportStep state event).2
        (independent_lineage_availability_survives_one_step state event h)

theorem run_contract_transport_append
    (state : ContractTransportState)
    (left right : List ContractTransportEvent) :
    runContractTransport state (left ++ right) =
      runContractTransport (runContractTransport state left) right := by
  induction left generalizing state with
  | nil => rfl
  | cons event rest ih =>
      simp only [List.cons_append, runContractTransport]
      exact ih (contractTransportStep state event).2

theorem root_revocation_invalidates_root_and_descendant
    (state : ContractTransportState)
    (hPresent : state.rootStage ≠ .absent)
    (hLive : state.rootStage ≠ .revoked) :
    let result := contractTransportStep state .revokeRoot
    result.1 = .accepted ∧
      result.2.rootStage = .revoked ∧
      result.2.descendantStage = .revoked ∧
      result.2.independentStage = state.independentStage := by
  simp [contractTransportStep, hPresent, hLive, revokeRootLineage]

theorem descendant_unusable_after_root_revocation
    (state : ContractTransportState)
    (h : state.rootStage = .revoked) :
    descendantUsable state = false := by
  simp [descendantUsable, rootLineageRevoked, h]

theorem root_revocation_is_persistent
    (state : ContractTransportState) (event : ContractTransportEvent)
    (h : state.rootStage = .revoked) :
    (contractTransportStep state event).2.rootStage = .revoked := by
  cases event <;>
    simp [contractTransportStep, h, rootLineageRevoked] <;>
    repeat' first | split | simp_all

def referenceContractTrace : List ContractTransportEvent :=
  [.resolveRoot, .attestRoot, .issueDescendant, .resolveDescendant,
    .attestDescendant, .consumeDescendant, .revokeRoot]

theorem reference_contract_trace_consumes_then_revokes_lineage :
    let beforeRevocation := runContractTransport ({} : ContractTransportState)
      [.resolveRoot, .attestRoot, .issueDescendant, .resolveDescendant,
        .attestDescendant, .consumeDescendant]
    let afterRevocation := runContractTransport ({} : ContractTransportState)
      referenceContractTrace
    beforeRevocation.descendantStage = .consumed ∧
      afterRevocation.rootStage = .revoked ∧
      afterRevocation.descendantStage = .revoked ∧
      afterRevocation.independentStage = .ready ∧
      afterRevocation.supportAssignments = 0 ∧
      afterRevocation.externalEffects = 0 := by native_decide

theorem revoked_descendant_consumer_is_rejected_without_state_change :
    let revoked := runContractTransport ({} : ContractTransportState)
      referenceContractTrace
    contractTransportStep revoked .consumeDescendant =
      (.rejectRevoked, revoked) := by native_decide

theorem unrelated_lineage_remains_consumable_after_root_revocation :
    let revoked := runContractTransport ({} : ContractTransportState)
      referenceContractTrace
    let result := contractTransportStep revoked .consumeIndependent
    result.1 = .accepted ∧
      result.2.independentStage = .consumed ∧
      result.2.rootStage = .revoked ∧
      result.2.descendantStage = .revoked := by native_decide

theorem root_identity_mismatch_rejects_resolution_noninterferingly :
    let state := { ({} : ContractTransportState) with rootTheoremDigest := 9999 }
    contractTransportStep state .resolveRoot = (.rejectIdentity, state) := by
  native_decide

theorem parent_mismatch_rejects_descendant_issue_noninterferingly :
    let state := {
      ({} : ContractTransportState) with
      rootStage := .ready
      descendantParentDigest := 9999
    }
    contractTransportStep state .issueDescendant = (.rejectParent, state) := by
  native_decide

end AsiStackProofs.ProofCarryingContracts
