namespace AsiStackProofs.ProofEnvelope

inductive ProofTargetStatus where
  | planned
  | scaffolded
  | implemented
  | blocked
  | retired
deriving DecidableEq, Repr

structure ProofTargetReview where
  status : ProofTargetStatus
  moduleExists : Bool
  buildPassed : Bool
  operationalClaim : Bool
deriving DecidableEq, Repr

def ImplementedTargetValid (target : ProofTargetReview) : Prop :=
  target.status = ProofTargetStatus.implemented ->
    target.moduleExists = true ∧ target.buildPassed = true

def NonOperationalTargetRouted (target : ProofTargetReview) : Prop :=
  target.operationalClaim = false ->
    target.status = ProofTargetStatus.planned ∨
      target.status = ProofTargetStatus.blocked

theorem non_operational_target_not_implemented
    {target : ProofTargetReview} :
    NonOperationalTargetRouted target ->
    target.operationalClaim = false ->
    target.status ≠ ProofTargetStatus.implemented := by
  intro routed nonOperational implemented
  have routedStatus := routed nonOperational
  cases routedStatus with
  | inl planned =>
      rw [planned] at implemented
      contradiction
  | inr blocked =>
      rw [blocked] at implemented
      contradiction

theorem implemented_target_missing_module_or_build_rejected
    {target : ProofTargetReview} :
    target.status = ProofTargetStatus.implemented ->
    (target.moduleExists = false ∨ target.buildPassed = false) ->
    ¬ ImplementedTargetValid target := by
  intro implemented missing valid
  have complete := valid implemented
  cases complete with
  | intro moduleExists buildPassed =>
      cases missing with
      | inl moduleMissing =>
          rw [moduleMissing] at moduleExists
          contradiction
      | inr buildMissing =>
          rw [buildMissing] at buildPassed
          contradiction

inductive ProofArtifactLane where
  | lean
  | schema
  | processValidator
  | behaviorTest
  | benchmark
  | externalTheorem
  | researchBacklog
deriving DecidableEq, Repr

inductive VerifierResult where
  | passed
  | failed
  | timedOut
  | notRun
deriving DecidableEq, Repr

inductive SemanticAdequacy where
  | adequateFiniteRecord
  | projectionOnlyTraceability
  | inadequate
  | notReviewed
deriving DecidableEq, Repr

inductive SupportStateEffect where
  | noChange
  | proofStateOnly
  | supportPromotion
  | demotion
deriving DecidableEq, Repr

structure ProofArtifactReview where
  lane : ProofArtifactLane
  verifierResult : VerifierResult
  artifactRefsPresent : Bool
  verifierCommandRecorded : Bool
  semanticAdequacy : SemanticAdequacy
  limitationsRecorded : Bool
  nonClaimsRecorded : Bool
  consumerRequirementsMatched : Bool
  claimedLeanProof : Bool
  externalTheoremIdsResolved : Bool
  supportStateEffect : SupportStateEffect
  evidenceTransitionAccepted : Bool
deriving DecidableEq, Repr

def LeanProofClaimValid (review : ProofArtifactReview) : Prop :=
  review.claimedLeanProof = true ->
    review.lane = ProofArtifactLane.lean ∧
      review.verifierResult = VerifierResult.passed ∧
        review.artifactRefsPresent = true ∧
          review.verifierCommandRecorded = true

theorem non_lean_artifact_cannot_claim_lean_proof
    {review : ProofArtifactReview} :
    review.claimedLeanProof = true ->
    review.lane ≠ ProofArtifactLane.lean ->
    ¬ LeanProofClaimValid review := by
  intro claimed nonLean valid
  unfold LeanProofClaimValid at valid
  have proofBoundary := valid claimed
  exact nonLean proofBoundary.1

def SupportPromotionValid (review : ProofArtifactReview) : Prop :=
  review.supportStateEffect = SupportStateEffect.supportPromotion ->
    review.evidenceTransitionAccepted = true ∧
      review.semanticAdequacy = SemanticAdequacy.adequateFiniteRecord ∧
        review.limitationsRecorded = true ∧
          review.nonClaimsRecorded = true ∧
            review.consumerRequirementsMatched = true

theorem support_promotion_without_transition_or_boundaries_rejected
    {review : ProofArtifactReview} :
    review.supportStateEffect = SupportStateEffect.supportPromotion ->
    (review.evidenceTransitionAccepted = false ∨
      review.semanticAdequacy ≠ SemanticAdequacy.adequateFiniteRecord ∨
        review.limitationsRecorded = false ∨
          review.nonClaimsRecorded = false ∨
            review.consumerRequirementsMatched = false) ->
    ¬ SupportPromotionValid review := by
  intro promotion missing valid
  unfold SupportPromotionValid at valid
  have complete := valid promotion
  cases complete with
  | intro transitionAccepted rest =>
      cases rest with
      | intro adequate rest =>
          cases rest with
          | intro limitations rest =>
              cases rest with
              | intro nonClaims consumerRequirements =>
                  cases missing with
                  | inl transitionMissing =>
                      rw [transitionMissing] at transitionAccepted
                      contradiction
                  | inr restMissing =>
                      cases restMissing with
                      | inl adequacyMissing =>
                          exact adequacyMissing adequate
                      | inr restMissing =>
                          cases restMissing with
                          | inl limitationsMissing =>
                              rw [limitationsMissing] at limitations
                              contradiction
                          | inr restMissing =>
                              cases restMissing with
                              | inl nonClaimsMissing =>
                                  rw [nonClaimsMissing] at nonClaims
                                  contradiction
                              | inr consumerMissing =>
                                  rw [consumerMissing] at consumerRequirements
                                  contradiction

def ExternalTheoremReferenceValid (review : ProofArtifactReview) : Prop :=
  review.lane = ProofArtifactLane.externalTheorem ->
    review.artifactRefsPresent = true ∧
      review.externalTheoremIdsResolved = true ∧
        review.nonClaimsRecorded = true

theorem external_theorem_without_ids_or_boundary_rejected
    {review : ProofArtifactReview} :
    review.lane = ProofArtifactLane.externalTheorem ->
    (review.artifactRefsPresent = false ∨
      review.externalTheoremIdsResolved = false ∨
        review.nonClaimsRecorded = false) ->
    ¬ ExternalTheoremReferenceValid review := by
  intro externalRef missing valid
  unfold ExternalTheoremReferenceValid at valid
  have complete := valid externalRef
  cases complete with
  | intro artifactRefs rest =>
      cases rest with
      | intro theoremIds nonClaims =>
          cases missing with
          | inl artifactMissing =>
              rw [artifactMissing] at artifactRefs
              contradiction
          | inr restMissing =>
              cases restMissing with
              | inl idsMissing =>
                  rw [idsMissing] at theoremIds
                  contradiction
              | inr nonClaimsMissing =>
                                  rw [nonClaimsMissing] at nonClaims
                                  contradiction

/-! ## Formal-artifact authority-lease lifecycle

This finite transition system models authority carried by one proof artifact
for one declared consumer. Identity fields and review predicates are authored
inputs. The model does not inspect a repository, establish semantic adequacy,
prove implementation refinement, resolve external theorem meaning, or confer
support or external-effect authority.
-/

inductive ProofLeaseStage where
  | registered
  | verified
  | adequacyReviewed
  | consumerBound
  | active
  | revoked
  | expired
deriving DecidableEq, Repr

inductive ProofLeaseEvent where
  | recordVerification (targetId artifactVersion verifierVersion : Nat)
  | acceptAdequacy (targetId propositionVersion : Nat)
  | bindConsumer (consumerId : Nat)
  | issueLease (consumerId implementationVersion environmentVersion : Nat)
  | changeArtifact (newArtifactVersion : Nat)
  | revoke
  | expire
deriving DecidableEq, Repr

inductive ProofLeaseRoute where
  | accepted
  | rejectStage
  | rejectIdentity
  | rejectBoundary
  | rejectAuthority
  | rejectVersion
deriving DecidableEq, Repr

structure ProofLeaseState where
  stage : ProofLeaseStage := .registered
  targetId : Nat := 9001
  propositionVersion : Nat := 7
  artifactVersion : Nat := 1
  verifierVersion : Nat := 3
  consumerId : Nat := 42
  implementationVersion : Nat := 11
  environmentVersion : Nat := 13
  logicalTime : Nat := 0
  expiryTime : Nat := 10
  artifactValid : Bool := true
  adequacyAccepted : Bool := true
  consumerRequirementsMatched : Bool := true
  limitationsRecorded : Bool := true
  nonClaimsRecorded : Bool := true
  revocationReasonPresent : Bool := true
  supportStateEffect : SupportStateEffect := .noChange
  externalEffectAuthorized : Bool := false
  receiptCount : Nat := 0
deriving DecidableEq, Repr

def proofLeaseStep
    (state : ProofLeaseState) (event : ProofLeaseEvent) :
    ProofLeaseRoute × ProofLeaseState :=
  match event with
  | .recordVerification targetId artifactVersion verifierVersion =>
      if state.stage != .registered then (.rejectStage, state)
      else if targetId != state.targetId ||
          artifactVersion != state.artifactVersion ||
          verifierVersion != state.verifierVersion then
        (.rejectIdentity, state)
      else if !state.artifactValid then (.rejectBoundary, state)
      else
        (.accepted, { state with
          stage := .verified
          receiptCount := state.receiptCount + 1 })
  | .acceptAdequacy targetId propositionVersion =>
      if state.stage != .verified then (.rejectStage, state)
      else if targetId != state.targetId ||
          propositionVersion != state.propositionVersion then
        (.rejectIdentity, state)
      else if !state.adequacyAccepted ||
          !state.limitationsRecorded || !state.nonClaimsRecorded then
        (.rejectBoundary, state)
      else
        (.accepted, { state with
          stage := .adequacyReviewed
          receiptCount := state.receiptCount + 1 })
  | .bindConsumer consumerId =>
      if state.stage != .adequacyReviewed then (.rejectStage, state)
      else if consumerId != state.consumerId then (.rejectIdentity, state)
      else if !state.consumerRequirementsMatched then (.rejectBoundary, state)
      else
        (.accepted, { state with
          stage := .consumerBound
          receiptCount := state.receiptCount + 1 })
  | .issueLease consumerId implementationVersion environmentVersion =>
      if state.stage != .consumerBound then (.rejectStage, state)
      else if consumerId != state.consumerId ||
          implementationVersion != state.implementationVersion ||
          environmentVersion != state.environmentVersion then
        (.rejectIdentity, state)
      else if !state.artifactValid || !state.adequacyAccepted ||
          !state.consumerRequirementsMatched || !state.limitationsRecorded ||
          !state.nonClaimsRecorded then
        (.rejectBoundary, state)
      else if state.expiryTime ≤ state.logicalTime then (.rejectBoundary, state)
      else if state.supportStateEffect != .noChange ||
          state.externalEffectAuthorized then
        (.rejectAuthority, state)
      else
        (.accepted, { state with
          stage := .active
          receiptCount := state.receiptCount + 1 })
  | .changeArtifact newArtifactVersion =>
      if state.stage != .active then (.rejectStage, state)
      else if newArtifactVersion ≤ state.artifactVersion then
        (.rejectVersion, state)
      else
        (.accepted, { state with
          stage := .registered
          artifactVersion := newArtifactVersion
          receiptCount := state.receiptCount + 1 })
  | .revoke =>
      if state.stage != .active then (.rejectStage, state)
      else if !state.revocationReasonPresent then (.rejectBoundary, state)
      else
        (.accepted, { state with
          stage := .revoked
          receiptCount := state.receiptCount + 1 })
  | .expire =>
      if state.stage != .active then (.rejectStage, state)
      else if state.logicalTime < state.expiryTime then (.rejectBoundary, state)
      else
        (.accepted, { state with
          stage := .expired
          receiptCount := state.receiptCount + 1 })

def runProofLease : ProofLeaseState -> List ProofLeaseEvent -> ProofLeaseState
  | state, [] => state
  | state, event :: rest =>
      runProofLease (proofLeaseStep state event).2 rest

def ProofLeaseCustodyPreserved
    (before after : ProofLeaseState) : Prop :=
  after.targetId = before.targetId ∧
    after.propositionVersion = before.propositionVersion ∧
      before.artifactVersion ≤ after.artifactVersion ∧
        after.verifierVersion = before.verifierVersion ∧
          after.consumerId = before.consumerId ∧
            after.implementationVersion = before.implementationVersion ∧
              after.environmentVersion = before.environmentVersion ∧
                after.expiryTime = before.expiryTime ∧
                  after.supportStateEffect = before.supportStateEffect ∧
                    after.externalEffectAuthorized =
                      before.externalEffectAuthorized

def ProofLeaseNonAuthority (state : ProofLeaseState) : Prop :=
  state.supportStateEffect = .noChange ∧
    state.externalEffectAuthorized = false

theorem proof_lease_rejected_event_is_noninterfering
    (state : ProofLeaseState) (event : ProofLeaseEvent)
    (rejected : (proofLeaseStep state event).1 != .accepted) :
    (proofLeaseStep state event).2 = state := by
  cases event <;>
    simp_all [proofLeaseStep] <;>
    repeat' first | split | simp_all

theorem proof_lease_step_preserves_custody
    (state : ProofLeaseState) (event : ProofLeaseEvent) :
    ProofLeaseCustodyPreserved state (proofLeaseStep state event).2 := by
  cases event <;>
    simp [ProofLeaseCustodyPreserved, proofLeaseStep] <;>
    repeat' first | split | simp_all
  all_goals omega

theorem proof_lease_custody_is_transitive
    {first second third : ProofLeaseState}
    (left : ProofLeaseCustodyPreserved first second)
    (right : ProofLeaseCustodyPreserved second third) :
    ProofLeaseCustodyPreserved first third := by
  unfold ProofLeaseCustodyPreserved at left right ⊢
  exact ⟨right.1.trans left.1,
    right.2.1.trans left.2.1,
    Nat.le_trans left.2.2.1 right.2.2.1,
    right.2.2.2.1.trans left.2.2.2.1,
    right.2.2.2.2.1.trans left.2.2.2.2.1,
    right.2.2.2.2.2.1.trans left.2.2.2.2.2.1,
    right.2.2.2.2.2.2.1.trans left.2.2.2.2.2.2.1,
    right.2.2.2.2.2.2.2.1.trans left.2.2.2.2.2.2.2.1,
    right.2.2.2.2.2.2.2.2.1.trans left.2.2.2.2.2.2.2.2.1,
    right.2.2.2.2.2.2.2.2.2.trans left.2.2.2.2.2.2.2.2.2⟩

theorem run_proof_lease_preserves_custody
    (state : ProofLeaseState) (events : List ProofLeaseEvent) :
    ProofLeaseCustodyPreserved state (runProofLease state events) := by
  induction events generalizing state with
  | nil => simp [runProofLease, ProofLeaseCustodyPreserved]
  | cons event rest ih =>
      exact proof_lease_custody_is_transitive
        (proof_lease_step_preserves_custody state event)
        (ih (proofLeaseStep state event).2)

theorem proof_lease_step_preserves_non_authority
    (state : ProofLeaseState) (event : ProofLeaseEvent)
    (bounded : ProofLeaseNonAuthority state) :
    ProofLeaseNonAuthority (proofLeaseStep state event).2 := by
  cases event <;>
    simp_all [ProofLeaseNonAuthority, proofLeaseStep] <;>
    repeat' first | split | simp_all

theorem run_proof_lease_preserves_non_authority
    (state : ProofLeaseState) (events : List ProofLeaseEvent)
    (bounded : ProofLeaseNonAuthority state) :
    ProofLeaseNonAuthority (runProofLease state events) := by
  induction events generalizing state with
  | nil => exact bounded
  | cons event rest ih =>
      exact ih (proofLeaseStep state event).2
        (proof_lease_step_preserves_non_authority state event bounded)

theorem proof_lease_accepted_step_adds_exactly_one_receipt
    (state : ProofLeaseState) (event : ProofLeaseEvent)
    (accepted : (proofLeaseStep state event).1 = .accepted) :
    (proofLeaseStep state event).2.receiptCount = state.receiptCount + 1 := by
  cases event <;>
    simp_all [proofLeaseStep] <;>
    repeat' first | split | simp_all

theorem run_proof_lease_append
    (state : ProofLeaseState) (left right : List ProofLeaseEvent) :
    runProofLease state (left ++ right) =
      runProofLease (runProofLease state left) right := by
  induction left generalizing state with
  | nil => rfl
  | cons event rest ih =>
      simp only [List.cons_append, runProofLease]
      exact ih (proofLeaseStep state event).2

def proofLeaseInitialState : ProofLeaseState := {}

def proofLeaseInitialIssueTrace : List ProofLeaseEvent :=
  [.recordVerification 9001 1 3,
    .acceptAdequacy 9001 7,
    .bindConsumer 42,
    .issueLease 42 11 13]

def completeProofLeaseTrace : List ProofLeaseEvent :=
  proofLeaseInitialIssueTrace ++
    [.changeArtifact 2,
      .recordVerification 9001 2 3,
      .acceptAdequacy 9001 7,
      .bindConsumer 42,
      .issueLease 42 11 13,
      .revoke]

def activeProofLeaseState : ProofLeaseState :=
  runProofLease proofLeaseInitialState proofLeaseInitialIssueTrace

theorem initial_issue_trace_reaches_active_lease :
    activeProofLeaseState.stage = .active ∧
      activeProofLeaseState.receiptCount = 4 := by
  decide

theorem complete_proof_lease_trace_reissues_changed_artifact_then_revokes :
    let final := runProofLease proofLeaseInitialState completeProofLeaseTrace
    final.stage = .revoked ∧
      final.artifactVersion = 2 ∧
        final.receiptCount = 10 ∧
          final.supportStateEffect = .noChange ∧
            final.externalEffectAuthorized = false := by
  decide

theorem artifact_change_invalidates_active_lease :
    let next := (proofLeaseStep activeProofLeaseState (.changeArtifact 2)).2
    next.stage = .registered ∧
      next.artifactVersion = 2 ∧
        next.receiptCount = activeProofLeaseState.receiptCount + 1 := by
  decide

theorem wrong_consumer_binding_is_rejected :
    let reviewed := runProofLease proofLeaseInitialState
      [.recordVerification 9001 1 3, .acceptAdequacy 9001 7]
    proofLeaseStep reviewed (.bindConsumer 43) =
      (.rejectIdentity, reviewed) := by
  decide

theorem stale_artifact_verification_is_rejected :
    proofLeaseStep proofLeaseInitialState (.recordVerification 9001 2 3) =
      (.rejectIdentity, proofLeaseInitialState) := by
  decide

theorem support_promotion_issue_is_rejected :
    let state := { activeProofLeaseState with
      stage := .consumerBound
      supportStateEffect := .supportPromotion }
    proofLeaseStep state (.issueLease 42 11 13) =
      (.rejectAuthority, state) := by
  decide

theorem external_effect_issue_is_rejected :
    let state := { activeProofLeaseState with
      stage := .consumerBound
      externalEffectAuthorized := true }
    proofLeaseStep state (.issueLease 42 11 13) =
      (.rejectAuthority, state) := by
  decide

theorem expired_issue_is_rejected :
    let state := { activeProofLeaseState with
      stage := .consumerBound
      logicalTime := 10 }
    proofLeaseStep state (.issueLease 42 11 13) =
      (.rejectBoundary, state) := by
  decide

theorem revocation_without_reason_is_rejected :
    let state := { activeProofLeaseState with
      revocationReasonPresent := false }
    proofLeaseStep state .revoke = (.rejectBoundary, state) := by
  decide

theorem revoked_proof_lease_is_absorbing
    (state : ProofLeaseState) (events : List ProofLeaseEvent)
    (revoked : state.stage = .revoked) :
    runProofLease state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      have rejected : proofLeaseStep state event = (.rejectStage, state) := by
        cases event <;> simp [proofLeaseStep, revoked]
      simp [runProofLease, rejected, ih state revoked]

structure ThinProofLeaseSummary where
  targetId : Nat
  artifactVersion : Nat
  consumerId : Nat
  stage : ProofLeaseStage
  expiryTime : Nat
deriving DecidableEq, Repr

def ThinProofLeaseSummaryOf (state : ProofLeaseState) : ThinProofLeaseSummary :=
  { targetId := state.targetId
    artifactVersion := state.artifactVersion
    consumerId := state.consumerId
    stage := state.stage
    expiryTime := state.expiryTime }

def issueReadyProofLeaseState : ProofLeaseState :=
  { ({} : ProofLeaseState) with stage := .consumerBound }

def issueMissingNonClaimsProofLeaseState : ProofLeaseState :=
  { issueReadyProofLeaseState with nonClaimsRecorded := false }

def ProofLeaseIssueDecisionFor (state : ProofLeaseState) : ProofLeaseRoute :=
  (proofLeaseStep state (.issueLease 42 11 13)).1

theorem thin_proof_lease_summary_has_issue_collision :
    issueReadyProofLeaseState ≠ issueMissingNonClaimsProofLeaseState ∧
      ThinProofLeaseSummaryOf issueReadyProofLeaseState =
        ThinProofLeaseSummaryOf issueMissingNonClaimsProofLeaseState ∧
      ProofLeaseIssueDecisionFor issueReadyProofLeaseState = .accepted ∧
      ProofLeaseIssueDecisionFor issueMissingNonClaimsProofLeaseState =
        .rejectBoundary := by
  decide

theorem no_thin_proof_lease_classifier_recovers_boundary_state
    (classify : ThinProofLeaseSummary -> Bool) :
    classify (ThinProofLeaseSummaryOf issueReadyProofLeaseState) ≠ true ∨
      classify (ThinProofLeaseSummaryOf issueMissingNonClaimsProofLeaseState) ≠
        false := by
  have collision :
      ThinProofLeaseSummaryOf issueReadyProofLeaseState =
        ThinProofLeaseSummaryOf issueMissingNonClaimsProofLeaseState :=
    thin_proof_lease_summary_has_issue_collision.2.1
  by_cases readyAccepted :
      classify (ThinProofLeaseSummaryOf issueReadyProofLeaseState) = true
  · right
    intro missingRejected
    have sameClassification := congrArg classify collision
    rw [readyAccepted, missingRejected] at sameClassification
    contradiction
  · exact Or.inl readyAccepted

structure CompleteProofLeaseTransport where
  stage : ProofLeaseStage
  targetId : Nat
  propositionVersion : Nat
  artifactVersion : Nat
  verifierVersion : Nat
  consumerId : Nat
  implementationVersion : Nat
  environmentVersion : Nat
  logicalTime : Nat
  expiryTime : Nat
  artifactValid : Bool
  adequacyAccepted : Bool
  consumerRequirementsMatched : Bool
  limitationsRecorded : Bool
  nonClaimsRecorded : Bool
  revocationReasonPresent : Bool
  supportStateEffect : SupportStateEffect
  externalEffectAuthorized : Bool
  receiptCount : Nat
deriving DecidableEq, Repr

def CompleteProofLeaseTransportOf
    (state : ProofLeaseState) : CompleteProofLeaseTransport :=
  { stage := state.stage
    targetId := state.targetId
    propositionVersion := state.propositionVersion
    artifactVersion := state.artifactVersion
    verifierVersion := state.verifierVersion
    consumerId := state.consumerId
    implementationVersion := state.implementationVersion
    environmentVersion := state.environmentVersion
    logicalTime := state.logicalTime
    expiryTime := state.expiryTime
    artifactValid := state.artifactValid
    adequacyAccepted := state.adequacyAccepted
    consumerRequirementsMatched := state.consumerRequirementsMatched
    limitationsRecorded := state.limitationsRecorded
    nonClaimsRecorded := state.nonClaimsRecorded
    revocationReasonPresent := state.revocationReasonPresent
    supportStateEffect := state.supportStateEffect
    externalEffectAuthorized := state.externalEffectAuthorized
    receiptCount := state.receiptCount }

def ProofLeaseStateOf
    (transport : CompleteProofLeaseTransport) : ProofLeaseState :=
  { stage := transport.stage
    targetId := transport.targetId
    propositionVersion := transport.propositionVersion
    artifactVersion := transport.artifactVersion
    verifierVersion := transport.verifierVersion
    consumerId := transport.consumerId
    implementationVersion := transport.implementationVersion
    environmentVersion := transport.environmentVersion
    logicalTime := transport.logicalTime
    expiryTime := transport.expiryTime
    artifactValid := transport.artifactValid
    adequacyAccepted := transport.adequacyAccepted
    consumerRequirementsMatched := transport.consumerRequirementsMatched
    limitationsRecorded := transport.limitationsRecorded
    nonClaimsRecorded := transport.nonClaimsRecorded
    revocationReasonPresent := transport.revocationReasonPresent
    supportStateEffect := transport.supportStateEffect
    externalEffectAuthorized := transport.externalEffectAuthorized
    receiptCount := transport.receiptCount }

theorem complete_proof_lease_transport_round_trips
    (state : ProofLeaseState) :
    ProofLeaseStateOf (CompleteProofLeaseTransportOf state) = state := by
  cases state
  rfl

theorem complete_proof_lease_transport_is_injective :
    Function.Injective CompleteProofLeaseTransportOf := by
  intro left right equal
  calc
    left = ProofLeaseStateOf (CompleteProofLeaseTransportOf left) :=
      (complete_proof_lease_transport_round_trips left).symm
    _ = ProofLeaseStateOf (CompleteProofLeaseTransportOf right) :=
      congrArg ProofLeaseStateOf equal
    _ = right := complete_proof_lease_transport_round_trips right

theorem complete_proof_lease_transport_preserves_step
    (state : ProofLeaseState) (event : ProofLeaseEvent) :
    proofLeaseStep
        (ProofLeaseStateOf (CompleteProofLeaseTransportOf state)) event =
      proofLeaseStep state event := by
  rw [complete_proof_lease_transport_round_trips]

end AsiStackProofs.ProofEnvelope
