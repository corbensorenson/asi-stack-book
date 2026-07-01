namespace AsiStackProofs.FailureModes

structure ComponentRecord where
  requiredInvariantHolds : Bool
  authorityBounded : Bool
deriving DecidableEq, Repr

def PromotionAllowed (component : ComponentRecord) : Prop :=
  component.requiredInvariantHolds = true ∧
    component.authorityBounded = true

def GovernanceFailure (component : ComponentRecord) : Prop :=
  component.requiredInvariantHolds = false ∨
    component.authorityBounded = false

theorem failed_required_invariant_blocks_promotion
    {component : ComponentRecord} :
    component.requiredInvariantHolds = false ->
    ¬ PromotionAllowed component := by
  intro failed promoted
  unfold PromotionAllowed at promoted
  rw [failed] at promoted
  cases promoted.1

theorem unbounded_authority_detected_as_governance_failure
    {component : ComponentRecord} :
    component.authorityBounded = false ->
    GovernanceFailure component := by
  intro unbounded
  exact Or.inr unbounded

inductive FailureIncidentRoute where
  | ordinaryOperation
  | escalateAuthorityReview
  | quarantineContext
  | freezeEvaluator
  | blockClaimPromotion
deriving DecidableEq, Repr

structure FailureIncidentRecord where
  authorityOverCeiling : Bool
  contextTainted : Bool
  contextAuthorityGrantPresent : Bool
  evaluatorModifiedBySubject : Bool
  claimPromotionRequested : Bool
  verificationPassed : Bool
deriving DecidableEq, Repr

def FailureIncidentRouteFor (incident : FailureIncidentRecord) : FailureIncidentRoute :=
  if incident.authorityOverCeiling = true then
    FailureIncidentRoute.escalateAuthorityReview
  else if incident.contextTainted = true ∧ incident.contextAuthorityGrantPresent = false then
    FailureIncidentRoute.quarantineContext
  else if incident.evaluatorModifiedBySubject = true then
    FailureIncidentRoute.freezeEvaluator
  else if incident.claimPromotionRequested = true ∧ incident.verificationPassed = false then
    FailureIncidentRoute.blockClaimPromotion
  else
    FailureIncidentRoute.ordinaryOperation

theorem authority_over_ceiling_routes_to_review
    {incident : FailureIncidentRecord} :
    incident.authorityOverCeiling = true ->
    FailureIncidentRouteFor incident = FailureIncidentRoute.escalateAuthorityReview := by
  intro overCeiling
  unfold FailureIncidentRouteFor
  simp [overCeiling]

theorem tainted_context_without_authority_grant_quarantines
    {incident : FailureIncidentRecord} :
    incident.authorityOverCeiling = false ->
    incident.contextTainted = true ->
    incident.contextAuthorityGrantPresent = false ->
    FailureIncidentRouteFor incident = FailureIncidentRoute.quarantineContext := by
  intro withinCeiling tainted noGrant
  unfold FailureIncidentRouteFor
  simp [withinCeiling, tainted, noGrant]

theorem subject_modified_evaluator_freezes_review
    {incident : FailureIncidentRecord} :
    incident.authorityOverCeiling = false ->
    incident.contextTainted = false ->
    incident.evaluatorModifiedBySubject = true ->
    FailureIncidentRouteFor incident = FailureIncidentRoute.freezeEvaluator := by
  intro withinCeiling cleanContext evaluatorModified
  unfold FailureIncidentRouteFor
  simp [withinCeiling, cleanContext, evaluatorModified]

theorem unverified_claim_promotion_blocks
    {incident : FailureIncidentRecord} :
    incident.authorityOverCeiling = false ->
    incident.contextTainted = false ->
    incident.evaluatorModifiedBySubject = false ->
    incident.claimPromotionRequested = true ->
    incident.verificationPassed = false ->
    FailureIncidentRouteFor incident = FailureIncidentRoute.blockClaimPromotion := by
  intro withinCeiling cleanContext evaluatorStable promotionRequested verificationFailed
  unfold FailureIncidentRouteFor
  simp [withinCeiling, cleanContext, evaluatorStable, promotionRequested, verificationFailed]

inductive FailureRecurrenceRoute where
  | noFailureRecorded
  | requestFailureClass
  | requestBoundary
  | requestReceipt
  | requestOwner
  | requestContainment
  | requestResidual
  | requestLearningPath
  | requestNormalizationGuard
  | escalateRecurringFailure
  | escalateSevereIrreversibleFailure
  | blockPromotionUntilReview
  | quarantineEscapePath
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | closeFailureRecord
deriving DecidableEq, Repr

structure FailureRecurrenceReview where
  failureRecorded : Bool
  failureClassRecorded : Bool
  boundaryRecorded : Bool
  receiptRecorded : Bool
  ownerRecorded : Bool
  containmentRecorded : Bool
  residualRecorded : Bool
  learningPathRecorded : Bool
  normalizationGuardRecorded : Bool
  recurrenceObserved : Bool
  severityHigh : Bool
  reversible : Bool
  promotionRequested : Bool
  reviewRecorded : Bool
  escapePathOpen : Bool
  quarantineRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def FailureRecurrenceRouteFor
    (review : FailureRecurrenceReview) : FailureRecurrenceRoute :=
  if review.failureRecorded = false then
    FailureRecurrenceRoute.noFailureRecorded
  else if review.failureClassRecorded = false then
    FailureRecurrenceRoute.requestFailureClass
  else if review.boundaryRecorded = false then
    FailureRecurrenceRoute.requestBoundary
  else if review.receiptRecorded = false then
    FailureRecurrenceRoute.requestReceipt
  else if review.ownerRecorded = false then
    FailureRecurrenceRoute.requestOwner
  else if review.containmentRecorded = false then
    FailureRecurrenceRoute.requestContainment
  else if review.residualRecorded = false then
    FailureRecurrenceRoute.requestResidual
  else if review.learningPathRecorded = false then
    FailureRecurrenceRoute.requestLearningPath
  else if review.normalizationGuardRecorded = false then
    FailureRecurrenceRoute.requestNormalizationGuard
  else if review.recurrenceObserved = true ∧ review.reviewRecorded = false then
    FailureRecurrenceRoute.escalateRecurringFailure
  else if review.severityHigh = true ∧ review.reversible = false ∧
      review.reviewRecorded = false then
    FailureRecurrenceRoute.escalateSevereIrreversibleFailure
  else if review.promotionRequested = true ∧ review.reviewRecorded = false then
    FailureRecurrenceRoute.blockPromotionUntilReview
  else if review.escapePathOpen = true ∧ review.quarantineRecorded = false then
    FailureRecurrenceRoute.quarantineEscapePath
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    FailureRecurrenceRoute.requestEvidenceTransition
  else if review.nonClaimBoundaryRecorded = false then
    FailureRecurrenceRoute.preserveNonClaimBoundary
  else
    FailureRecurrenceRoute.closeFailureRecord

def completeFailureRecurrenceReview : FailureRecurrenceReview :=
  { failureRecorded := true,
    failureClassRecorded := true,
    boundaryRecorded := true,
    receiptRecorded := true,
    ownerRecorded := true,
    containmentRecorded := true,
    residualRecorded := true,
    learningPathRecorded := true,
    normalizationGuardRecorded := true,
    recurrenceObserved := false,
    severityHigh := false,
    reversible := true,
    promotionRequested := false,
    reviewRecorded := true,
    escapePathOpen := false,
    quarantineRecorded := true,
    supportPromotionRequested := false,
    evidenceTransitionRecorded := true,
    nonClaimBoundaryRecorded := true }

theorem no_failure_record_stays_idle
    {review : FailureRecurrenceReview} :
    review.failureRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.noFailureRecorded := by
  intro noFailure
  unfold FailureRecurrenceRouteFor
  simp [noFailure]

theorem missing_failure_class_requests_class
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestFailureClass := by
  intro failure missingClass
  unfold FailureRecurrenceRouteFor
  simp [failure, missingClass]

theorem missing_boundary_requests_boundary
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestBoundary := by
  intro failure failureClass boundaryMissing
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundaryMissing]

theorem missing_receipt_requests_receipt
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestReceipt := by
  intro failure failureClass boundary missingReceipt
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, missingReceipt]

theorem missing_owner_requests_owner
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestOwner := by
  intro failure failureClass boundary receipt missingOwner
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, missingOwner]

theorem missing_containment_requests_containment
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestContainment := by
  intro failure failureClass boundary receipt owner missingContainment
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, missingContainment]

theorem missing_residual_requests_residual
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestResidual := by
  intro failure failureClass boundary receipt owner containment missingResidual
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, missingResidual]

theorem missing_learning_path_requests_learning_path
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = true ->
    review.learningPathRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestLearningPath := by
  intro failure failureClass boundary receipt owner containment residual missingLearning
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, residual,
    missingLearning]

theorem missing_normalization_guard_requests_guard
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = true ->
    review.learningPathRecorded = true ->
    review.normalizationGuardRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestNormalizationGuard := by
  intro failure failureClass boundary receipt owner containment residual learning
    missingGuard
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, residual,
    learning, missingGuard]

theorem recurring_failure_without_review_escalates
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = true ->
    review.learningPathRecorded = true ->
    review.normalizationGuardRecorded = true ->
    review.recurrenceObserved = true ->
    review.reviewRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.escalateRecurringFailure := by
  intro failure failureClass boundary receipt owner containment residual learning guard
    recurrence noReview
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, residual,
    learning, guard, recurrence, noReview]

theorem severe_irreversible_failure_without_review_escalates
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = true ->
    review.learningPathRecorded = true ->
    review.normalizationGuardRecorded = true ->
    review.recurrenceObserved = false ->
    review.severityHigh = true ->
    review.reversible = false ->
    review.reviewRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.escalateSevereIrreversibleFailure := by
  intro failure failureClass boundary receipt owner containment residual learning guard
    noRecurrence severe irreversible noReview
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, residual,
    learning, guard, noRecurrence, severe, irreversible, noReview]

theorem promotion_request_without_review_blocks_promotion
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = true ->
    review.learningPathRecorded = true ->
    review.normalizationGuardRecorded = true ->
    review.recurrenceObserved = false ->
    review.severityHigh = false ->
    review.promotionRequested = true ->
    review.reviewRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.blockPromotionUntilReview := by
  intro failure failureClass boundary receipt owner containment residual learning guard
    noRecurrence notSevere promotion noReview
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, residual,
    learning, guard, noRecurrence, notSevere, promotion, noReview]

theorem open_escape_path_without_quarantine_quarantines
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = true ->
    review.learningPathRecorded = true ->
    review.normalizationGuardRecorded = true ->
    review.recurrenceObserved = false ->
    review.severityHigh = false ->
    review.promotionRequested = false ->
    review.escapePathOpen = true ->
    review.quarantineRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.quarantineEscapePath := by
  intro failure failureClass boundary receipt owner containment residual learning guard
    noRecurrence notSevere noPromotion escapeOpen noQuarantine
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, residual,
    learning, guard, noRecurrence, notSevere, noPromotion, escapeOpen,
    noQuarantine]

theorem support_promotion_without_failure_evidence_transition_requests_transition
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = true ->
    review.learningPathRecorded = true ->
    review.normalizationGuardRecorded = true ->
    review.recurrenceObserved = false ->
    review.severityHigh = false ->
    review.promotionRequested = false ->
    review.escapePathOpen = false ->
    review.supportPromotionRequested = true ->
    review.evidenceTransitionRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.requestEvidenceTransition := by
  intro failure failureClass boundary receipt owner containment residual learning guard
    noRecurrence notSevere noPromotion noEscape supportPromotion
    missingTransition
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, residual,
    learning, guard, noRecurrence, notSevere, noPromotion, noEscape,
    supportPromotion, missingTransition]

theorem failure_record_without_nonclaim_boundary_preserves_boundary
    {review : FailureRecurrenceReview} :
    review.failureRecorded = true ->
    review.failureClassRecorded = true ->
    review.boundaryRecorded = true ->
    review.receiptRecorded = true ->
    review.ownerRecorded = true ->
    review.containmentRecorded = true ->
    review.residualRecorded = true ->
    review.learningPathRecorded = true ->
    review.normalizationGuardRecorded = true ->
    review.recurrenceObserved = false ->
    review.severityHigh = false ->
    review.promotionRequested = false ->
    review.escapePathOpen = false ->
    review.supportPromotionRequested = false ->
    review.nonClaimBoundaryRecorded = false ->
    FailureRecurrenceRouteFor review =
      FailureRecurrenceRoute.preserveNonClaimBoundary := by
  intro failure failureClass boundary receipt owner containment residual learning guard
    noRecurrence notSevere noPromotion noEscape noSupportPromotion
    missingNonClaim
  unfold FailureRecurrenceRouteFor
  simp [failure, failureClass, boundary, receipt, owner, containment, residual,
    learning, guard, noRecurrence, notSevere, noPromotion, noEscape,
    noSupportPromotion, missingNonClaim]

theorem complete_failure_record_closes_record :
    FailureRecurrenceRouteFor completeFailureRecurrenceReview =
      FailureRecurrenceRoute.closeFailureRecord := by
  unfold FailureRecurrenceRouteFor completeFailureRecurrenceReview
  simp

end AsiStackProofs.FailureModes
