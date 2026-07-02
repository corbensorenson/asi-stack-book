namespace AsiStackProofs.ValueConflict

structure ConflictDecisionReview where
  unresolvedProtectedConflict : Bool
  decisionMade : Bool
  residualConflictRecordPresent : Bool
deriving DecidableEq, Repr

def UnresolvedConflictCarriesResidual
    (review : ConflictDecisionReview) : Prop :=
  review.unresolvedProtectedConflict = true ->
    review.decisionMade = true ->
      review.residualConflictRecordPresent = true

theorem decision_with_unresolved_protected_conflict_carries_residual_record
    {review : ConflictDecisionReview} :
    UnresolvedConflictCarriesResidual review ->
    review.unresolvedProtectedConflict = true ->
    review.decisionMade = true ->
    review.residualConflictRecordPresent = true := by
  intro valid unresolved decided
  exact valid unresolved decided

structure HighStakesConflictReview where
  highStakesConflict : Bool
  requiredReviewPresent : Bool
  decisionAccepted : Bool
deriving DecidableEq, Repr

def HighStakesReviewRequired (review : HighStakesConflictReview) : Prop :=
  review.highStakesConflict = true ->
    review.requiredReviewPresent = false ->
      review.decisionAccepted = false

theorem high_stakes_conflict_cannot_bypass_required_review
    {review : HighStakesConflictReview} :
    HighStakesReviewRequired review ->
    review.highStakesConflict = true ->
    review.requiredReviewPresent = false ->
    review.decisionAccepted = false := by
  intro valid highStakes missingReview
  exact valid highStakes missingReview

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

end AsiStackProofs.ValueConflict
