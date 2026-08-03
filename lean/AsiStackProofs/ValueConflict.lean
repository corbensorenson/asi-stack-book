namespace AsiStackProofs.ValueConflict

inductive ValueConflictDecisionRoute where
  | accepted
  | blockedForReview
deriving DecidableEq, Repr

structure ValueConflictDecision where
  highStakesConflict : Bool
  unresolvedConflict : Bool
  revisitPathRecorded : Bool
  route : ValueConflictDecisionRoute
deriving DecidableEq, Repr

def ValueConflictDecisionSafe (decision : ValueConflictDecision) : Prop :=
  if decision.highStakesConflict &&
      decision.unresolvedConflict &&
      !decision.revisitPathRecorded then
    decision.route = ValueConflictDecisionRoute.blockedForReview
  else
    True

theorem unresolved_high_stakes_conflict_without_revisit_path_is_blocked
    {decision : ValueConflictDecision} :
    ValueConflictDecisionSafe decision ->
    decision.highStakesConflict = true ->
    decision.unresolvedConflict = true ->
    decision.revisitPathRecorded = false ->
    decision.route = ValueConflictDecisionRoute.blockedForReview := by
  intro safe highStakes unresolved missingRevisit
  unfold ValueConflictDecisionSafe at safe
  rw [highStakes, unresolved, missingRevisit] at safe
  simp at safe
  exact safe

inductive ValueConflictReviewPhase where
  | proposed
  | bounded
  | escalated
  | denied
  | residualized
  | deprecatedPremise
deriving DecidableEq, Repr

inductive ValueConflictReviewRoute where
  | allowBounded
  | blockForReview
  | preserveDissentResidual
  | narrowAuthority
deriving DecidableEq, Repr

structure ValueConflictReviewDecision where
  phase : ValueConflictReviewPhase
  highStakesConflict : Bool
  unresolvedConflict : Bool
  stakeholderDisagreement : Bool
  reviewPresent : Bool
  residualUncertaintyRecorded : Bool
  dissentPayloadPreserved : Bool
  boundedDecision : Bool
  authorityNarrowed : Bool
  reversibleAction : Bool
  revisitPathRecorded : Bool
  deprecatedPremise : Bool
  route : ValueConflictReviewRoute
deriving DecidableEq, Repr

def ValueConflictReviewRequiresReview
    (decision : ValueConflictReviewDecision) : Bool :=
  decision.highStakesConflict &&
    decision.unresolvedConflict &&
      (!decision.reviewPresent ||
        !decision.residualUncertaintyRecorded ||
        !decision.revisitPathRecorded)

def ValueConflictReviewSafe
    (decision : ValueConflictReviewDecision) : Prop :=
  if ValueConflictReviewRequiresReview decision then
    decision.route = ValueConflictReviewRoute.blockForReview
  else if decision.boundedDecision && !decision.dissentPayloadPreserved then
    decision.route = ValueConflictReviewRoute.preserveDissentResidual
  else if decision.unresolvedConflict && !decision.authorityNarrowed then
    decision.route = ValueConflictReviewRoute.narrowAuthority
  else
    True

def highStakesConflictWithoutResidual :
    ValueConflictReviewDecision :=
  { phase := ValueConflictReviewPhase.escalated,
    highStakesConflict := true,
    unresolvedConflict := true,
    stakeholderDisagreement := true,
    reviewPresent := true,
    residualUncertaintyRecorded := false,
    dissentPayloadPreserved := true,
    boundedDecision := false,
    authorityNarrowed := true,
    reversibleAction := false,
    revisitPathRecorded := true,
    deprecatedPremise := false,
    route := ValueConflictReviewRoute.blockForReview }

def boundedDecisionWithoutDissentResidualized :
    ValueConflictReviewDecision :=
  { phase := ValueConflictReviewPhase.bounded,
    highStakesConflict := false,
    unresolvedConflict := true,
    stakeholderDisagreement := true,
    reviewPresent := true,
    residualUncertaintyRecorded := true,
    dissentPayloadPreserved := false,
    boundedDecision := true,
    authorityNarrowed := true,
    reversibleAction := true,
    revisitPathRecorded := true,
    deprecatedPremise := false,
    route := ValueConflictReviewRoute.preserveDissentResidual }

def unresolvedConflictWithoutAuthorityNarrowing :
    ValueConflictReviewDecision :=
  { phase := ValueConflictReviewPhase.residualized,
    highStakesConflict := false,
    unresolvedConflict := true,
    stakeholderDisagreement := true,
    reviewPresent := true,
    residualUncertaintyRecorded := true,
    dissentPayloadPreserved := true,
    boundedDecision := false,
    authorityNarrowed := false,
    reversibleAction := true,
    revisitPathRecorded := true,
    deprecatedPremise := false,
    route := ValueConflictReviewRoute.narrowAuthority }

theorem high_stakes_unresolved_conflict_without_residual_blocks
    {decision : ValueConflictReviewDecision} :
    ValueConflictReviewSafe decision ->
    decision.highStakesConflict = true ->
    decision.unresolvedConflict = true ->
    decision.residualUncertaintyRecorded = false ->
    decision.route = ValueConflictReviewRoute.blockForReview := by
  intro safe highStakes unresolved missingResidual
  unfold ValueConflictReviewSafe ValueConflictReviewRequiresReview at safe
  rw [highStakes, unresolved, missingResidual] at safe
  simp at safe
  exact safe

theorem bounded_decision_without_dissent_preserves_residual
    {decision : ValueConflictReviewDecision} :
    ValueConflictReviewSafe decision ->
    ValueConflictReviewRequiresReview decision = false ->
    decision.boundedDecision = true ->
    decision.dissentPayloadPreserved = false ->
    decision.route = ValueConflictReviewRoute.preserveDissentResidual := by
  intro safe noReviewRequired bounded missingDissent
  unfold ValueConflictReviewSafe at safe
  rw [noReviewRequired, bounded, missingDissent] at safe
  simp at safe
  exact safe

theorem unresolved_conflict_without_authority_narrowing_routes_to_narrowing
    {decision : ValueConflictReviewDecision} :
    ValueConflictReviewSafe decision ->
    ValueConflictReviewRequiresReview decision = false ->
    decision.boundedDecision = false ->
    decision.unresolvedConflict = true ->
    decision.authorityNarrowed = false ->
    decision.route = ValueConflictReviewRoute.narrowAuthority := by
  intro safe noReviewRequired notBounded unresolved notNarrowed
  unfold ValueConflictReviewSafe at safe
  rw [noReviewRequired, notBounded, unresolved, notNarrowed] at safe
  simp at safe
  exact safe

inductive ValueConflictLifecycleRoute where
  | requestConflictRecord
  | requestValueAxes
  | requestStakeholderRecord
  | requestStakesRecord
  | requestReversibilityRecord
  | requestAuthorityBoundary
  | requestEvidenceRequirement
  | requestReviewRoute
  | blockHighStakesUntilReview
  | blockHighStakesUntilResidual
  | preserveDissentPayload
  | narrowAuthority
  | requestExpiryOrRevisit
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | admitBoundedConflictDecision
deriving DecidableEq, Repr

structure ValueConflictLifecycleReview where
  conflictRecordPresent : Bool
  valueAxesRecorded : Bool
  stakeholderRecordPresent : Bool
  stakesRecorded : Bool
  reversibilityRecorded : Bool
  authorityBoundaryRecorded : Bool
  evidenceRequirementRecorded : Bool
  reviewRouteRecorded : Bool
  highStakesConflict : Bool
  unresolvedConflict : Bool
  reviewPresent : Bool
  residualUncertaintyRecorded : Bool
  boundedDecision : Bool
  dissentPayloadPreserved : Bool
  authorityNarrowed : Bool
  expiryOrRevisitRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def ValueConflictLifecycleRouteFor
    (review : ValueConflictLifecycleReview) : ValueConflictLifecycleRoute :=
  if review.conflictRecordPresent = false then
    ValueConflictLifecycleRoute.requestConflictRecord
  else if review.valueAxesRecorded = false then
    ValueConflictLifecycleRoute.requestValueAxes
  else if review.stakeholderRecordPresent = false then
    ValueConflictLifecycleRoute.requestStakeholderRecord
  else if review.stakesRecorded = false then
    ValueConflictLifecycleRoute.requestStakesRecord
  else if review.reversibilityRecorded = false then
    ValueConflictLifecycleRoute.requestReversibilityRecord
  else if review.authorityBoundaryRecorded = false then
    ValueConflictLifecycleRoute.requestAuthorityBoundary
  else if review.evidenceRequirementRecorded = false then
    ValueConflictLifecycleRoute.requestEvidenceRequirement
  else if review.reviewRouteRecorded = false then
    ValueConflictLifecycleRoute.requestReviewRoute
  else if review.highStakesConflict = true ∧ review.reviewPresent = false then
    ValueConflictLifecycleRoute.blockHighStakesUntilReview
  else if review.highStakesConflict = true ∧
      review.residualUncertaintyRecorded = false then
    ValueConflictLifecycleRoute.blockHighStakesUntilResidual
  else if review.boundedDecision = true ∧
      review.dissentPayloadPreserved = false then
    ValueConflictLifecycleRoute.preserveDissentPayload
  else if review.unresolvedConflict = true ∧ review.authorityNarrowed = false then
    ValueConflictLifecycleRoute.narrowAuthority
  else if review.expiryOrRevisitRecorded = false then
    ValueConflictLifecycleRoute.requestExpiryOrRevisit
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    ValueConflictLifecycleRoute.requestEvidenceTransition
  else if review.nonClaimBoundaryRecorded = false then
    ValueConflictLifecycleRoute.preserveNonClaimBoundary
  else
    ValueConflictLifecycleRoute.admitBoundedConflictDecision

def completeValueConflictLifecycleReview : ValueConflictLifecycleReview :=
  { conflictRecordPresent := true,
    valueAxesRecorded := true,
    stakeholderRecordPresent := true,
    stakesRecorded := true,
    reversibilityRecorded := true,
    authorityBoundaryRecorded := true,
    evidenceRequirementRecorded := true,
    reviewRouteRecorded := true,
    highStakesConflict := false,
    unresolvedConflict := false,
    reviewPresent := true,
    residualUncertaintyRecorded := true,
    boundedDecision := true,
    dissentPayloadPreserved := true,
    authorityNarrowed := true,
    expiryOrRevisitRecorded := true,
    supportPromotionRequested := false,
    evidenceTransitionRecorded := true,
    nonClaimBoundaryRecorded := true }

theorem missing_conflict_record_requests_record
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestConflictRecord := by
  intro missingRecord
  unfold ValueConflictLifecycleRouteFor
  simp [missingRecord]

theorem missing_value_axes_requests_axes
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestValueAxes := by
  intro record axesMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axesMissing]

theorem missing_stakeholder_record_requests_stakeholders
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestStakeholderRecord := by
  intro record axes stakeholdersMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholdersMissing]

theorem missing_stakes_record_requests_stakes
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestStakesRecord := by
  intro record axes stakeholders stakesMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakesMissing]

theorem missing_reversibility_record_requests_reversibility
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestReversibilityRecord := by
  intro record axes stakeholders stakes reversibilityMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibilityMissing]

theorem missing_authority_boundary_requests_boundary
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestAuthorityBoundary := by
  intro record axes stakeholders stakes reversibility authorityMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authorityMissing]

theorem missing_evidence_requirement_requests_evidence
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestEvidenceRequirement := by
  intro record axes stakeholders stakes reversibility authority evidenceMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority,
    evidenceMissing]

theorem missing_review_route_requests_route
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = true ->
    review.reviewRouteRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestReviewRoute := by
  intro record axes stakeholders stakes reversibility authority evidence routeMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority, evidence,
    routeMissing]

theorem high_stakes_without_review_blocks
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.highStakesConflict = true ->
    review.reviewPresent = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.blockHighStakesUntilReview := by
  intro record axes stakeholders stakes reversibility authority evidence route
    highStakes reviewMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority, evidence,
    route, highStakes, reviewMissing]

theorem high_stakes_without_residual_blocks
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.highStakesConflict = true ->
    review.reviewPresent = true ->
    review.residualUncertaintyRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.blockHighStakesUntilResidual := by
  intro record axes stakeholders stakes reversibility authority evidence route
    highStakes reviewPresent residualMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority, evidence,
    route, highStakes, reviewPresent, residualMissing]

theorem bounded_decision_without_dissent_routes_to_preservation
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.highStakesConflict = false ->
    review.boundedDecision = true ->
    review.dissentPayloadPreserved = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.preserveDissentPayload := by
  intro record axes stakeholders stakes reversibility authority evidence route
    notHighStakes bounded dissentMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority, evidence,
    route, notHighStakes, bounded, dissentMissing]

theorem unresolved_conflict_without_narrowed_authority_routes_to_narrowing
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.highStakesConflict = false ->
    review.boundedDecision = false ->
    review.unresolvedConflict = true ->
    review.authorityNarrowed = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.narrowAuthority := by
  intro record axes stakeholders stakes reversibility authority evidence route
    notHighStakes notBounded unresolved notNarrowed
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority, evidence,
    route, notHighStakes, notBounded, unresolved, notNarrowed]

theorem missing_expiry_or_revisit_requests_revisit
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.highStakesConflict = false ->
    review.boundedDecision = false ->
    review.unresolvedConflict = false ->
    review.expiryOrRevisitRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestExpiryOrRevisit := by
  intro record axes stakeholders stakes reversibility authority evidence route
    notHighStakes notBounded resolved revisitMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority, evidence,
    route, notHighStakes, notBounded, resolved, revisitMissing]

theorem support_promotion_without_value_conflict_transition_requests_transition
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.highStakesConflict = false ->
    review.boundedDecision = false ->
    review.unresolvedConflict = false ->
    review.expiryOrRevisitRecorded = true ->
    review.supportPromotionRequested = true ->
    review.evidenceTransitionRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.requestEvidenceTransition := by
  intro record axes stakeholders stakes reversibility authority evidence route
    notHighStakes notBounded resolved revisit promotion transitionMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority, evidence,
    route, notHighStakes, notBounded, resolved, revisit, promotion,
    transitionMissing]

theorem value_conflict_without_nonclaim_boundary_preserves_boundary
    {review : ValueConflictLifecycleReview} :
    review.conflictRecordPresent = true ->
    review.valueAxesRecorded = true ->
    review.stakeholderRecordPresent = true ->
    review.stakesRecorded = true ->
    review.reversibilityRecorded = true ->
    review.authorityBoundaryRecorded = true ->
    review.evidenceRequirementRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.highStakesConflict = false ->
    review.boundedDecision = false ->
    review.unresolvedConflict = false ->
    review.expiryOrRevisitRecorded = true ->
    review.supportPromotionRequested = false ->
    review.nonClaimBoundaryRecorded = false ->
    ValueConflictLifecycleRouteFor review =
      ValueConflictLifecycleRoute.preserveNonClaimBoundary := by
  intro record axes stakeholders stakes reversibility authority evidence route
    notHighStakes notBounded resolved revisit noPromotion boundaryMissing
  unfold ValueConflictLifecycleRouteFor
  simp [record, axes, stakeholders, stakes, reversibility, authority, evidence,
    route, notHighStakes, notBounded, resolved, revisit, noPromotion,
    boundaryMissing]

theorem complete_value_conflict_lifecycle_admits_bounded_decision :
    ValueConflictLifecycleRouteFor completeValueConflictLifecycleReview =
      ValueConflictLifecycleRoute.admitBoundedConflictDecision := by
  unfold ValueConflictLifecycleRouteFor completeValueConflictLifecycleReview
  simp

structure ContestabilityWorkedExampleSummary where
  conflictResidualPresent : Bool
  auditReceiptPresent : Bool
  exitPathScoped : Bool
  forkSafetyBounded : Bool
  redactionAppealPresent : Bool
  replacementPreservesReceipts : Bool
  negativeControlsRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def ContestabilityWorkedExampleSummaryValid
    (summary : ContestabilityWorkedExampleSummary) : Prop :=
  summary.conflictResidualPresent = true ∧
    summary.auditReceiptPresent = true ∧
    summary.exitPathScoped = true ∧
    summary.forkSafetyBounded = true ∧
    summary.redactionAppealPresent = true ∧
    summary.replacementPreservesReceipts = true ∧
    summary.negativeControlsRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

theorem contestability_worked_example_bridge
    {summary : ContestabilityWorkedExampleSummary} :
    ContestabilityWorkedExampleSummaryValid summary ->
      summary.conflictResidualPresent = true ∧
        summary.auditReceiptPresent = true ∧
        summary.exitPathScoped = true ∧
        summary.forkSafetyBounded = true ∧
        summary.redactionAppealPresent = true ∧
        summary.replacementPreservesReceipts = true ∧
        summary.negativeControlsRejected = true ∧
        summary.supportStateEffectNone = true ∧
        summary.nonClaimBoundary = true := by
  intro valid
  exact valid

/-! ## Versioned contestable decision-lease lifecycle

The lease below is a constraint on separately authorized action, not a grant of
authority. Conflict, value-set, stakeholder-set, and dissent fields are trusted
finite inputs. The model proves custody, narrowing, revisit, and expiry
consequences only; it does not identify moral truth or ensure an expiry event is
delivered by a deployed system.
-/

inductive ValueLeaseStage where
  | draft
  | reviewed
  | leased
  | revisiting
  | expired
deriving DecidableEq, Repr

inductive ValueLeaseEventKind where
  | recordIndependentReview
  | recordBoundedLease
  | openRevisit
  | expire
deriving DecidableEq, Repr

structure ValueLeaseState where
  conflictId : Nat
  leaseId : Nat
  valueSetId : Nat
  stakeholderSetId : Nat
  proposerId : Nat
  reviewerId : Nat
  version : Nat
  baseAuthorityCeiling : Nat
  currentAuthorityCeiling : Nat
  stage : ValueLeaseStage
  dissentRecorded : Bool
  residualCount : Nat
  expiresAt : Nat
  now : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

structure ValueLeaseEvent where
  kind : ValueLeaseEventKind
  conflictId : Nat
  leaseId : Nat
  valueSetId : Nat
  stakeholderSetId : Nat
  actorId : Nat
  reviewerId : Nat
  expectedVersion : Nat
  targetVersion : Nat
  requestedAuthorityCeiling : Nat
  dissentPayloadPresent : Bool
  residualUncertaintyPresent : Bool
  revisitTriggerPresent : Bool
  observedNow : Nat
  requestedExpiry : Nat
  requestsActionAuthority : Bool
  requestsMoralSettlement : Bool
deriving DecidableEq, Repr

def ValueLeaseEventAdmissible
    (state : ValueLeaseState) (event : ValueLeaseEvent) : Prop :=
  event.conflictId = state.conflictId ∧
    event.leaseId = state.leaseId ∧
    event.valueSetId = state.valueSetId ∧
    event.stakeholderSetId = state.stakeholderSetId ∧
    event.expectedVersion = state.version ∧
    state.now ≤ event.observedNow ∧
    event.requestsActionAuthority = false ∧
    event.requestsMoralSettlement = false ∧
    match event.kind with
    | ValueLeaseEventKind.recordIndependentReview =>
        state.stage = ValueLeaseStage.draft ∧
          event.actorId = state.proposerId ∧
          event.reviewerId ≠ state.proposerId ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | ValueLeaseEventKind.recordBoundedLease =>
        state.stage = ValueLeaseStage.reviewed ∧
          state.reviewerId ≠ state.proposerId ∧
          event.reviewerId = state.reviewerId ∧
          event.dissentPayloadPresent = true ∧
          event.residualUncertaintyPresent = true ∧
          event.requestedAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
          event.observedNow < event.requestedExpiry ∧
          event.targetVersion = state.version + 1
    | ValueLeaseEventKind.openRevisit =>
        state.stage = ValueLeaseStage.leased ∧
          event.reviewerId = state.reviewerId ∧
          event.revisitTriggerPresent = true ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | ValueLeaseEventKind.expire =>
        (state.stage = ValueLeaseStage.leased ∨
          state.stage = ValueLeaseStage.revisiting) ∧
          event.reviewerId = state.reviewerId ∧
          state.expiresAt ≤ event.observedNow ∧
          event.targetVersion = state.version

instance valueLeaseEventAdmissibleDecidable
    (state : ValueLeaseState) (event : ValueLeaseEvent) :
    Decidable (ValueLeaseEventAdmissible state event) := by
  unfold ValueLeaseEventAdmissible
  cases event.kind <;> infer_instance

def AdvanceValueLease
    (state : ValueLeaseState) (event : ValueLeaseEvent) : ValueLeaseState :=
  match event.kind with
  | ValueLeaseEventKind.recordIndependentReview =>
      { state with
        stage := ValueLeaseStage.reviewed
        reviewerId := event.reviewerId
        now := event.observedNow }
  | ValueLeaseEventKind.recordBoundedLease =>
      { state with
        stage := ValueLeaseStage.leased
        version := event.targetVersion
        currentAuthorityCeiling := event.requestedAuthorityCeiling
        dissentRecorded := true
        residualCount := state.residualCount + 1
        expiresAt := event.requestedExpiry
        now := event.observedNow }
  | ValueLeaseEventKind.openRevisit =>
      { state with
        stage := ValueLeaseStage.revisiting
        residualCount := state.residualCount + 1
        now := event.observedNow }
  | ValueLeaseEventKind.expire =>
      { state with
        stage := ValueLeaseStage.expired
        currentAuthorityCeiling := 0
        now := event.observedNow }

def ApplyValueLeaseEvent
    (state : ValueLeaseState) (event : ValueLeaseEvent) : Option ValueLeaseState :=
  if ValueLeaseEventAdmissible state event then
    some (AdvanceValueLease state event)
  else
    none

def RunValueLeaseEvents :
    ValueLeaseState → List ValueLeaseEvent → Option ValueLeaseState
  | state, [] => some state
  | state, event :: tail =>
      match ApplyValueLeaseEvent state event with
      | none => none
      | some next => RunValueLeaseEvents next tail

theorem accepted_value_lease_event_is_admissible
    {state next : ValueLeaseState} {event : ValueLeaseEvent}
    (accepted : ApplyValueLeaseEvent state event = some next) :
    ValueLeaseEventAdmissible state event := by
  unfold ApplyValueLeaseEvent at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_value_lease_event_is_exact_advance
    {state next : ValueLeaseState} {event : ValueLeaseEvent}
    (accepted : ApplyValueLeaseEvent state event = some next) :
    next = AdvanceValueLease state event := by
  unfold ApplyValueLeaseEvent at accepted
  split at accepted
  · simp at accepted
    exact accepted.symm
  · simp at accepted

theorem accepted_value_lease_event_preserves_custody
    {state next : ValueLeaseState} {event : ValueLeaseEvent}
    (accepted : ApplyValueLeaseEvent state event = some next) :
    next.conflictId = state.conflictId ∧
      next.leaseId = state.leaseId ∧
      next.valueSetId = state.valueSetId ∧
      next.stakeholderSetId = state.stakeholderSetId ∧
      next.proposerId = state.proposerId ∧
      next.baseAuthorityCeiling = state.baseAuthorityCeiling := by
  have exactAdvance := accepted_value_lease_event_is_exact_advance accepted
  subst next
  cases kind : event.kind <;> simp [AdvanceValueLease, kind]

theorem accepted_value_lease_event_is_non_authorizing
    {state next : ValueLeaseState} {event : ValueLeaseEvent}
    (accepted : ApplyValueLeaseEvent state event = some next) :
    event.requestsActionAuthority = false ∧
      event.requestsMoralSettlement = false ∧
      next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectCount = state.externalEffectCount := by
  have admissible := accepted_value_lease_event_is_admissible accepted
  have exactAdvance := accepted_value_lease_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, noAuthority, noSettlement, _⟩
  subst next
  exact ⟨noAuthority, noSettlement,
    by cases kind : event.kind <;> simp [AdvanceValueLease, kind],
    by cases kind : event.kind <;> simp [AdvanceValueLease, kind]⟩

theorem accepted_value_lease_event_never_widens_authority
    {state next : ValueLeaseState} {event : ValueLeaseEvent}
    (accepted : ApplyValueLeaseEvent state event = some next) :
    next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling := by
  have admissible := accepted_value_lease_event_is_admissible accepted
  have exactAdvance := accepted_value_lease_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  subst next
  cases kind : event.kind with
  | recordIndependentReview => simp [AdvanceValueLease, kind]
  | recordBoundedLease =>
      simp [kind] at route
      simpa [AdvanceValueLease, kind] using route.2.2.2.2.2.1
  | openRevisit => simp [AdvanceValueLease, kind]
  | expire => simp [AdvanceValueLease, kind]

theorem accepted_bounded_lease_requires_review_dissent_residual_and_expiry
    {state next : ValueLeaseState} {event : ValueLeaseEvent}
    (kind : event.kind = ValueLeaseEventKind.recordBoundedLease)
    (accepted : ApplyValueLeaseEvent state event = some next) :
    state.stage = ValueLeaseStage.reviewed ∧
      state.reviewerId ≠ state.proposerId ∧
      event.dissentPayloadPresent = true ∧
      event.residualUncertaintyPresent = true ∧
      next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
      next.dissentRecorded = true ∧
      next.residualCount = state.residualCount + 1 ∧
      next.now < next.expiresAt := by
  have admissible := accepted_value_lease_event_is_admissible accepted
  have exactAdvance := accepted_value_lease_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨reviewed, independent, reviewer, dissent, residual,
    narrowed, future, version⟩
  subst next
  simp [AdvanceValueLease, kind, reviewed, independent, dissent, residual,
    narrowed, future]

theorem accepted_revisit_preserves_dissent_and_adds_residual
    {state next : ValueLeaseState} {event : ValueLeaseEvent}
    (kind : event.kind = ValueLeaseEventKind.openRevisit)
    (accepted : ApplyValueLeaseEvent state event = some next) :
    state.stage = ValueLeaseStage.leased ∧
      next.stage = ValueLeaseStage.revisiting ∧
      next.dissentRecorded = state.dissentRecorded ∧
      next.residualCount = state.residualCount + 1 := by
  have admissible := accepted_value_lease_event_is_admissible accepted
  have exactAdvance := accepted_value_lease_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceValueLease, kind, route.1]

theorem accepted_expiry_closes_lease_and_removes_constraint_ceiling
    {state next : ValueLeaseState} {event : ValueLeaseEvent}
    (kind : event.kind = ValueLeaseEventKind.expire)
    (accepted : ApplyValueLeaseEvent state event = some next) :
    (state.stage = ValueLeaseStage.leased ∨
      state.stage = ValueLeaseStage.revisiting) ∧
      state.expiresAt ≤ event.observedNow ∧
      next.stage = ValueLeaseStage.expired ∧
      next.currentAuthorityCeiling = 0 := by
  have admissible := accepted_value_lease_event_is_admissible accepted
  have exactAdvance := accepted_value_lease_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  exact ⟨route.1, route.2.2.1, by simp [AdvanceValueLease, kind],
    by simp [AdvanceValueLease, kind]⟩

theorem value_lease_run_preserves_custody_non_authority_and_narrowing
    {initial final : ValueLeaseState} {events : List ValueLeaseEvent}
    (run : RunValueLeaseEvents initial events = some final) :
    final.conflictId = initial.conflictId ∧
      final.leaseId = initial.leaseId ∧
      final.valueSetId = initial.valueSetId ∧
      final.stakeholderSetId = initial.stakeholderSetId ∧
      final.proposerId = initial.proposerId ∧
      final.baseAuthorityCeiling = initial.baseAuthorityCeiling ∧
      final.currentAuthorityCeiling ≤ initial.currentAuthorityCeiling ∧
      final.supportAssignmentCount = initial.supportAssignmentCount ∧
      final.externalEffectCount = initial.externalEffectCount := by
  induction events generalizing initial with
  | nil => simp [RunValueLeaseEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunValueLeaseEvents] at run
      cases step : ApplyValueLeaseEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          have custody := accepted_value_lease_event_preserves_custody step
          have boundary := accepted_value_lease_event_is_non_authorizing step
          have narrowed := accepted_value_lease_event_never_widens_authority step
          have tailFacts := ih run
          rcases custody with ⟨c, l, v, stakeholders, owner, base⟩
          rcases boundary with ⟨_, _, support, effects⟩
          rcases tailFacts with ⟨tc, tl, tv, tstakeholders, towner, tbase,
            tnarrowed, tsupport, teffects⟩
          exact ⟨tc.trans c, tl.trans l, tv.trans v,
            tstakeholders.trans stakeholders, towner.trans owner,
            tbase.trans base, Nat.le_trans tnarrowed narrowed,
            tsupport.trans support, teffects.trans effects⟩

theorem value_lease_runs_compose
    (initial : ValueLeaseState) (before after : List ValueLeaseEvent) :
    RunValueLeaseEvents initial (before ++ after) =
      match RunValueLeaseEvents initial before with
      | none => none
      | some middle => RunValueLeaseEvents middle after := by
  induction before generalizing initial with
  | nil => simp [RunValueLeaseEvents]
  | cons event tail ih =>
      simp only [List.cons_append, RunValueLeaseEvents]
      cases step : ApplyValueLeaseEvent initial event with
      | none => simp
      | some next => simp [ih]

def initialValueLeaseState : ValueLeaseState := {
  conflictId := 23
  leaseId := 29
  valueSetId := 31
  stakeholderSetId := 37
  proposerId := 41
  reviewerId := 0
  version := 1
  baseAuthorityCeiling := 5
  currentAuthorityCeiling := 5
  stage := ValueLeaseStage.draft
  dissentRecorded := false
  residualCount := 0
  expiresAt := 0
  now := 10
  supportAssignmentCount := 0
  externalEffectCount := 0
}

def reviewValueLeaseEvent : ValueLeaseEvent := {
  kind := ValueLeaseEventKind.recordIndependentReview
  conflictId := 23
  leaseId := 29
  valueSetId := 31
  stakeholderSetId := 37
  actorId := 41
  reviewerId := 43
  expectedVersion := 1
  targetVersion := 1
  requestedAuthorityCeiling := 5
  dissentPayloadPresent := true
  residualUncertaintyPresent := true
  revisitTriggerPresent := false
  observedNow := 11
  requestedExpiry := 30
  requestsActionAuthority := false
  requestsMoralSettlement := false
}

def recordBoundedLeaseEvent : ValueLeaseEvent := {
  reviewValueLeaseEvent with
  kind := ValueLeaseEventKind.recordBoundedLease
  actorId := 43
  targetVersion := 2
  requestedAuthorityCeiling := 3
}

def revisitValueLeaseEvent : ValueLeaseEvent := {
  recordBoundedLeaseEvent with
  kind := ValueLeaseEventKind.openRevisit
  expectedVersion := 2
  targetVersion := 2
  requestedAuthorityCeiling := 3
  revisitTriggerPresent := true
  observedNow := 20
}

def expireValueLeaseEvent : ValueLeaseEvent := {
  revisitValueLeaseEvent with
  kind := ValueLeaseEventKind.expire
  revisitTriggerPresent := false
  observedNow := 30
}

def completeValueLeaseTrace : List ValueLeaseEvent :=
  [reviewValueLeaseEvent, recordBoundedLeaseEvent,
    revisitValueLeaseEvent, expireValueLeaseEvent]

theorem complete_value_lease_trace_reaches_exact_expiry :
    RunValueLeaseEvents initialValueLeaseState completeValueLeaseTrace =
      some {
        initialValueLeaseState with
        reviewerId := 43
        version := 2
        currentAuthorityCeiling := 0
        stage := ValueLeaseStage.expired
        dissentRecorded := true
        residualCount := 2
        expiresAt := 30
        now := 30
      } := by
  decide

theorem value_lease_self_review_is_rejected :
    ApplyValueLeaseEvent initialValueLeaseState
      { reviewValueLeaseEvent with reviewerId := 41 } = none := by
  decide

theorem value_lease_stakeholder_substitution_is_rejected :
    ApplyValueLeaseEvent initialValueLeaseState
      { reviewValueLeaseEvent with stakeholderSetId := 38 } = none := by
  decide

theorem value_lease_missing_dissent_is_rejected :
    RunValueLeaseEvents initialValueLeaseState
      [reviewValueLeaseEvent,
        { recordBoundedLeaseEvent with dissentPayloadPresent := false }] = none := by
  decide

theorem value_lease_authority_widening_is_rejected :
    RunValueLeaseEvents initialValueLeaseState
      [reviewValueLeaseEvent,
        { recordBoundedLeaseEvent with requestedAuthorityCeiling := 6 }] = none := by
  decide

theorem value_lease_nonfuture_expiry_is_rejected :
    RunValueLeaseEvents initialValueLeaseState
      [reviewValueLeaseEvent,
        { recordBoundedLeaseEvent with requestedExpiry := 11 }] = none := by
  decide

theorem value_lease_revisit_without_trigger_is_rejected :
    RunValueLeaseEvents initialValueLeaseState
      [reviewValueLeaseEvent, recordBoundedLeaseEvent,
        { revisitValueLeaseEvent with revisitTriggerPresent := false }] = none := by
  decide

/-! ## Aggregation information loss and exact dissent custody

The fixed three-slot profile below is an authored finite input, not a claim that
three parties are complete, representative, or legitimately selected. The
model separates two facts: a scalar support count cannot identify which
recorded parties support an action, while an accepted profiled lease preserves
the entire supplied profile and dissent payload exactly.
-/

structure StakeholderPosition where
  stakeholderId : Nat
  standingRecorded : Bool
  supportsAction : Bool
deriving DecidableEq, Repr

structure StakeholderProfile where
  first : StakeholderPosition
  second : StakeholderPosition
  third : StakeholderPosition
deriving DecidableEq, Repr

def StakeholderPositionSupportBit (position : StakeholderPosition) : Nat :=
  if position.standingRecorded && position.supportsAction then 1 else 0

def StakeholderProfileSupportCount (profile : StakeholderProfile) : Nat :=
  StakeholderPositionSupportBit profile.first +
    StakeholderPositionSupportBit profile.second +
      StakeholderPositionSupportBit profile.third

def StakeholderProfileAllStandingRecorded
    (profile : StakeholderProfile) : Bool :=
  profile.first.standingRecorded &&
    profile.second.standingRecorded &&
      profile.third.standingRecorded

def leftDissentProfile : StakeholderProfile := {
  first := {
    stakeholderId := 101
    standingRecorded := true
    supportsAction := true
  }
  second := {
    stakeholderId := 102
    standingRecorded := true
    supportsAction := false
  }
  third := {
    stakeholderId := 103
    standingRecorded := true
    supportsAction := true
  }
}

def rightDissentProfile : StakeholderProfile := {
  first := {
    stakeholderId := 101
    standingRecorded := true
    supportsAction := false
  }
  second := {
    stakeholderId := 102
    standingRecorded := true
    supportsAction := true
  }
  third := {
    stakeholderId := 103
    standingRecorded := true
    supportsAction := true
  }
}

theorem aggregate_collision_profiles_are_distinct :
    leftDissentProfile ≠ rightDissentProfile := by
  decide

theorem aggregate_collision_has_equal_support_count :
    StakeholderProfileSupportCount leftDissentProfile =
      StakeholderProfileSupportCount rightDissentProfile := by
  decide

theorem scalar_support_count_is_not_injective :
    ¬ Function.Injective StakeholderProfileSupportCount := by
  intro injective
  apply aggregate_collision_profiles_are_distinct
  exact injective aggregate_collision_has_equal_support_count

theorem no_scalar_decoder_recovers_every_stakeholder_profile
    (decode : Nat → StakeholderProfile) :
    ¬ ∀ profile,
      decode (StakeholderProfileSupportCount profile) = profile := by
  intro recovers
  have left := recovers leftDissentProfile
  have right := recovers rightDissentProfile
  have sameDecoded :
      decode (StakeholderProfileSupportCount leftDissentProfile) =
        decode (StakeholderProfileSupportCount rightDissentProfile) := by
    rw [aggregate_collision_has_equal_support_count]
  apply aggregate_collision_profiles_are_distinct
  exact left.symm.trans (sameDecoded.trans right)

structure ProfiledBoundedLeaseRequest where
  leaseId : Nat
  stakeholderProfile : StakeholderProfile
  reportedSupportCount : Nat
  dissentPayload : StakeholderProfile
deriving DecidableEq, Repr

structure ProfiledBoundedLeaseReceipt where
  leaseId : Nat
  stakeholderProfile : StakeholderProfile
  reportedSupportCount : Nat
  dissentPayload : StakeholderProfile
deriving DecidableEq, Repr

def ProfiledBoundedLeaseRequestAdmissible
    (request : ProfiledBoundedLeaseRequest) : Prop :=
  StakeholderProfileAllStandingRecorded request.stakeholderProfile = true ∧
    request.reportedSupportCount =
      StakeholderProfileSupportCount request.stakeholderProfile ∧
    request.dissentPayload = request.stakeholderProfile

instance profiledBoundedLeaseRequestAdmissibleDecidable
    (request : ProfiledBoundedLeaseRequest) :
    Decidable (ProfiledBoundedLeaseRequestAdmissible request) := by
  unfold ProfiledBoundedLeaseRequestAdmissible
  infer_instance

def IssueProfiledBoundedLease
    (request : ProfiledBoundedLeaseRequest) :
    Option ProfiledBoundedLeaseReceipt :=
  if ProfiledBoundedLeaseRequestAdmissible request then
    some {
      leaseId := request.leaseId
      stakeholderProfile := request.stakeholderProfile
      reportedSupportCount := request.reportedSupportCount
      dissentPayload := request.dissentPayload
    }
  else
    none

theorem accepted_profiled_lease_request_is_admissible
    {request : ProfiledBoundedLeaseRequest}
    {receipt : ProfiledBoundedLeaseReceipt}
    (accepted : IssueProfiledBoundedLease request = some receipt) :
    ProfiledBoundedLeaseRequestAdmissible request := by
  unfold IssueProfiledBoundedLease at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_profiled_lease_preserves_exact_stakeholder_and_dissent_custody
    {request : ProfiledBoundedLeaseRequest}
    {receipt : ProfiledBoundedLeaseReceipt}
    (accepted : IssueProfiledBoundedLease request = some receipt) :
    receipt.leaseId = request.leaseId ∧
      receipt.stakeholderProfile = request.stakeholderProfile ∧
      receipt.reportedSupportCount = request.reportedSupportCount ∧
      receipt.dissentPayload = request.stakeholderProfile := by
  have admissible := accepted_profiled_lease_request_is_admissible accepted
  unfold IssueProfiledBoundedLease at accepted
  split at accepted
  · simp at accepted
    subst receipt
    exact ⟨rfl, rfl, rfl, admissible.2.2⟩
  · contradiction

def validProfiledBoundedLeaseRequest : ProfiledBoundedLeaseRequest := {
  leaseId := 211
  stakeholderProfile := leftDissentProfile
  reportedSupportCount := 2
  dissentPayload := leftDissentProfile
}

def missingStandingProfile : StakeholderProfile := {
  leftDissentProfile with
  second := { leftDissentProfile.second with standingRecorded := false }
}

theorem valid_profiled_lease_issues_exact_receipt :
    IssueProfiledBoundedLease validProfiledBoundedLeaseRequest = some {
      leaseId := 211
      stakeholderProfile := leftDissentProfile
      reportedSupportCount := 2
      dissentPayload := leftDissentProfile
    } := by
  decide

theorem aggregate_equivalent_dissent_substitution_is_rejected :
    IssueProfiledBoundedLease {
      validProfiledBoundedLeaseRequest with
      dissentPayload := rightDissentProfile
    } = none := by
  decide

theorem missing_stakeholder_standing_is_rejected_even_with_matching_count :
    IssueProfiledBoundedLease {
      leaseId := 211
      stakeholderProfile := missingStandingProfile
      reportedSupportCount := 2
      dissentPayload := missingStandingProfile
    } = none := by
  decide

end AsiStackProofs.ValueConflict
