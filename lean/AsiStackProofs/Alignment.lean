namespace AsiStackProofs.Alignment

inductive ConstitutionalChangeRoute where
  | accepted
  | blockedForReview
deriving DecidableEq, Repr

structure ConstitutionalChangeDecision where
  protectedPredicate : Bool
  weakensPredicate : Bool
  independentReviewerPresent : Bool
  route : ConstitutionalChangeRoute
deriving DecidableEq, Repr

def ConstitutionalChangeSafe (decision : ConstitutionalChangeDecision) : Prop :=
  if decision.protectedPredicate && decision.weakensPredicate && !decision.independentReviewerPresent then
    decision.route = ConstitutionalChangeRoute.blockedForReview
  else
    True

def unsafeWeakeningWithoutReviewBlocked : ConstitutionalChangeDecision where
  protectedPredicate := true
  weakensPredicate := true
  independentReviewerPresent := false
  route := ConstitutionalChangeRoute.blockedForReview

theorem protected_predicate_weakening_without_reviewer_routes_to_review
    {decision : ConstitutionalChangeDecision} :
    ConstitutionalChangeSafe decision ->
    decision.protectedPredicate = true ->
    decision.weakensPredicate = true ->
    decision.independentReviewerPresent = false ->
    decision.route = ConstitutionalChangeRoute.blockedForReview := by
  intro safe predicateProtected weakens missingReviewer
  unfold ConstitutionalChangeSafe at safe
  rw [predicateProtected, weakens, missingReviewer] at safe
  simp at safe
  exact safe

inductive ConstitutionalTransitionPhase where
  | proposed
  | migrationReady
  | active
  | blockedForReview
  | residualized
  | rolledBack
deriving DecidableEq, Repr

inductive ConstitutionalTransitionRoute where
  | accept
  | blockForReview
  | preserveResidual
  | rollback
deriving DecidableEq, Repr

structure ConstitutionalTransitionDecision where
  phase : ConstitutionalTransitionPhase
  sourceVersion : Nat
  targetVersion : Nat
  protectedPredicateChanged : Bool
  protectedPredicatePreserved : Bool
  independentReview : Bool
  rollbackAvailable : Bool
  conflictDetected : Bool
  conflictRouted : Bool
  selfModification : Bool
  weakensPredicate : Bool
  route : ConstitutionalTransitionRoute
deriving DecidableEq, Repr

def ConstitutionalTransitionRequiresReview
    (decision : ConstitutionalTransitionDecision) : Bool :=
  (decision.selfModification && decision.weakensPredicate) ||
    (decision.protectedPredicateChanged &&
      (!decision.protectedPredicatePreserved ||
        !decision.independentReview ||
        !decision.rollbackAvailable))

def ConstitutionalTransitionSafe
    (decision : ConstitutionalTransitionDecision) : Prop :=
  if ConstitutionalTransitionRequiresReview decision then
    decision.route = ConstitutionalTransitionRoute.blockForReview
  else if decision.conflictDetected && !decision.conflictRouted then
    decision.route = ConstitutionalTransitionRoute.preserveResidual
  else
    True

def unsafeConstitutionalMigrationWithoutRollback :
    ConstitutionalTransitionDecision :=
  { phase := ConstitutionalTransitionPhase.migrationReady,
    sourceVersion := 1,
    targetVersion := 2,
    protectedPredicateChanged := true,
    protectedPredicatePreserved := true,
    independentReview := true,
    rollbackAvailable := false,
    conflictDetected := false,
    conflictRouted := true,
    selfModification := false,
    weakensPredicate := false,
    route := ConstitutionalTransitionRoute.blockForReview }

def constitutionalConflictWithoutRouteResidualized :
    ConstitutionalTransitionDecision :=
  { phase := ConstitutionalTransitionPhase.residualized,
    sourceVersion := 1,
    targetVersion := 1,
    protectedPredicateChanged := false,
    protectedPredicatePreserved := true,
    independentReview := true,
    rollbackAvailable := true,
    conflictDetected := true,
    conflictRouted := false,
    selfModification := false,
    weakensPredicate := false,
    route := ConstitutionalTransitionRoute.preserveResidual }

theorem protected_migration_without_rollback_routes_to_review
    {decision : ConstitutionalTransitionDecision} :
    ConstitutionalTransitionSafe decision ->
    decision.protectedPredicateChanged = true ->
    decision.rollbackAvailable = false ->
    decision.route = ConstitutionalTransitionRoute.blockForReview := by
  intro safe changed missingRollback
  unfold ConstitutionalTransitionSafe ConstitutionalTransitionRequiresReview at safe
  rw [changed, missingRollback] at safe
  simp at safe
  exact safe

theorem accepted_transition_cannot_drop_protected_predicate
    {decision : ConstitutionalTransitionDecision} :
    ConstitutionalTransitionSafe decision ->
    decision.route = ConstitutionalTransitionRoute.accept ->
    decision.protectedPredicateChanged = true ->
    decision.protectedPredicatePreserved = false ->
    False := by
  intro safe accepted changed dropped
  unfold ConstitutionalTransitionSafe ConstitutionalTransitionRequiresReview at safe
  rw [changed, dropped] at safe
  simp at safe
  rw [accepted] at safe
  contradiction

theorem detected_conflict_without_route_preserves_residual
    {decision : ConstitutionalTransitionDecision} :
    ConstitutionalTransitionSafe decision ->
    ConstitutionalTransitionRequiresReview decision = false ->
    decision.conflictDetected = true ->
    decision.conflictRouted = false ->
    decision.route = ConstitutionalTransitionRoute.preserveResidual := by
  intro safe noReviewRequired conflict missingRoute
  unfold ConstitutionalTransitionSafe at safe
  rw [noReviewRequired, conflict, missingRoute] at safe
  simp at safe
  exact safe

inductive ConstitutionalLifecycleRoute where
  | requestPredicateRecord
  | requestNormativeSource
  | requestOperationalTest
  | requestProtectedScope
  | requestConflictBehavior
  | requestReviewRoute
  | requestMigrationPolicy
  | requestSelfModificationRule
  | requestAgencyRightsLink
  | requestMaterialUsability
  | blockHighImpactUntilPreEffectReview
  | blockHighImpactUntilRollback
  | blockHighImpactUntilCorrection
  | routeReviewerIndependenceGap
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | admitConstitutionalConstraint
deriving DecidableEq, Repr

structure ConstitutionalLifecycleReview where
  predicateRecorded : Bool
  normativeSourceRecorded : Bool
  operationalTestRecorded : Bool
  protectedScopeRecorded : Bool
  conflictBehaviorRecorded : Bool
  reviewRouteRecorded : Bool
  migrationPolicyRecorded : Bool
  selfModificationRuleRecorded : Bool
  agencyRightsLinked : Bool
  materialUsabilityRecorded : Bool
  highImpactAction : Bool
  preEffectReviewRecorded : Bool
  rollbackPathRecorded : Bool
  correctionPathRecorded : Bool
  independentReviewerRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def ConstitutionalLifecycleRouteFor
    (review : ConstitutionalLifecycleReview) : ConstitutionalLifecycleRoute :=
  if review.predicateRecorded = false then
    ConstitutionalLifecycleRoute.requestPredicateRecord
  else if review.normativeSourceRecorded = false then
    ConstitutionalLifecycleRoute.requestNormativeSource
  else if review.operationalTestRecorded = false then
    ConstitutionalLifecycleRoute.requestOperationalTest
  else if review.protectedScopeRecorded = false then
    ConstitutionalLifecycleRoute.requestProtectedScope
  else if review.conflictBehaviorRecorded = false then
    ConstitutionalLifecycleRoute.requestConflictBehavior
  else if review.reviewRouteRecorded = false then
    ConstitutionalLifecycleRoute.requestReviewRoute
  else if review.migrationPolicyRecorded = false then
    ConstitutionalLifecycleRoute.requestMigrationPolicy
  else if review.selfModificationRuleRecorded = false then
    ConstitutionalLifecycleRoute.requestSelfModificationRule
  else if review.agencyRightsLinked = false then
    ConstitutionalLifecycleRoute.requestAgencyRightsLink
  else if review.materialUsabilityRecorded = false then
    ConstitutionalLifecycleRoute.requestMaterialUsability
  else if review.highImpactAction = true ∧
      review.preEffectReviewRecorded = false then
    ConstitutionalLifecycleRoute.blockHighImpactUntilPreEffectReview
  else if review.highImpactAction = true ∧
      review.rollbackPathRecorded = false then
    ConstitutionalLifecycleRoute.blockHighImpactUntilRollback
  else if review.highImpactAction = true ∧
      review.correctionPathRecorded = false then
    ConstitutionalLifecycleRoute.blockHighImpactUntilCorrection
  else if review.highImpactAction = true ∧
      review.independentReviewerRecorded = false then
    ConstitutionalLifecycleRoute.routeReviewerIndependenceGap
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    ConstitutionalLifecycleRoute.requestEvidenceTransition
  else if review.nonClaimBoundaryRecorded = false then
    ConstitutionalLifecycleRoute.preserveNonClaimBoundary
  else
    ConstitutionalLifecycleRoute.admitConstitutionalConstraint

def completeConstitutionalLifecycleReview : ConstitutionalLifecycleReview :=
  { predicateRecorded := true,
    normativeSourceRecorded := true,
    operationalTestRecorded := true,
    protectedScopeRecorded := true,
    conflictBehaviorRecorded := true,
    reviewRouteRecorded := true,
    migrationPolicyRecorded := true,
    selfModificationRuleRecorded := true,
    agencyRightsLinked := true,
    materialUsabilityRecorded := true,
    highImpactAction := false,
    preEffectReviewRecorded := true,
    rollbackPathRecorded := true,
    correctionPathRecorded := true,
    independentReviewerRecorded := true,
    supportPromotionRequested := false,
    evidenceTransitionRecorded := true,
    nonClaimBoundaryRecorded := true }

theorem missing_predicate_record_requests_predicate_record
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestPredicateRecord := by
  intro missingPredicate
  unfold ConstitutionalLifecycleRouteFor
  simp [missingPredicate]

theorem missing_normative_source_requests_source
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestNormativeSource := by
  intro predicate sourceMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, sourceMissing]

theorem missing_operational_test_requests_test
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestOperationalTest := by
  intro predicate source testMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, testMissing]

theorem missing_protected_scope_requests_scope
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestProtectedScope := by
  intro predicate source test scopeMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scopeMissing]

theorem missing_conflict_behavior_requests_behavior
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestConflictBehavior := by
  intro predicate source test scope conflictMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflictMissing]

theorem missing_review_route_requests_review
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestReviewRoute := by
  intro predicate source test scope conflict reviewMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewMissing]

theorem missing_migration_policy_requests_policy
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestMigrationPolicy := by
  intro predicate source test scope conflict reviewRoute migrationMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migrationMissing]

theorem missing_self_modification_rule_requests_rule
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestSelfModificationRule := by
  intro predicate source test scope conflict reviewRoute migration ruleMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, ruleMissing]

theorem missing_agency_rights_link_requests_link
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = true ->
    review.agencyRightsLinked = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestAgencyRightsLink := by
  intro predicate source test scope conflict reviewRoute migration rule linkMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, rule,
    linkMissing]

theorem missing_material_usability_requests_usability
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = true ->
    review.agencyRightsLinked = true ->
    review.materialUsabilityRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestMaterialUsability := by
  intro predicate source test scope conflict reviewRoute migration rule link
    usabilityMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, rule,
    link, usabilityMissing]

theorem high_impact_without_pre_effect_review_blocks
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = true ->
    review.agencyRightsLinked = true ->
    review.materialUsabilityRecorded = true ->
    review.highImpactAction = true ->
    review.preEffectReviewRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.blockHighImpactUntilPreEffectReview := by
  intro predicate source test scope conflict reviewRoute migration rule link usability
    highImpact missingReview
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, rule,
    link, usability, highImpact, missingReview]

theorem high_impact_without_rollback_blocks
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = true ->
    review.agencyRightsLinked = true ->
    review.materialUsabilityRecorded = true ->
    review.highImpactAction = true ->
    review.preEffectReviewRecorded = true ->
    review.rollbackPathRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.blockHighImpactUntilRollback := by
  intro predicate source test scope conflict reviewRoute migration rule link usability
    highImpact preEffect rollbackMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, rule,
    link, usability, highImpact, preEffect, rollbackMissing]

theorem high_impact_without_correction_blocks
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = true ->
    review.agencyRightsLinked = true ->
    review.materialUsabilityRecorded = true ->
    review.highImpactAction = true ->
    review.preEffectReviewRecorded = true ->
    review.rollbackPathRecorded = true ->
    review.correctionPathRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.blockHighImpactUntilCorrection := by
  intro predicate source test scope conflict reviewRoute migration rule link usability
    highImpact preEffect rollback correctionMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, rule,
    link, usability, highImpact, preEffect, rollback, correctionMissing]

theorem high_impact_without_independent_reviewer_routes_gap
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = true ->
    review.agencyRightsLinked = true ->
    review.materialUsabilityRecorded = true ->
    review.highImpactAction = true ->
    review.preEffectReviewRecorded = true ->
    review.rollbackPathRecorded = true ->
    review.correctionPathRecorded = true ->
    review.independentReviewerRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.routeReviewerIndependenceGap := by
  intro predicate source test scope conflict reviewRoute migration rule link usability
    highImpact preEffect rollback correction reviewerMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, rule,
    link, usability, highImpact, preEffect, rollback, correction, reviewerMissing]

theorem support_promotion_without_alignment_transition_requests_transition
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = true ->
    review.agencyRightsLinked = true ->
    review.materialUsabilityRecorded = true ->
    review.highImpactAction = false ->
    review.supportPromotionRequested = true ->
    review.evidenceTransitionRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.requestEvidenceTransition := by
  intro predicate source test scope conflict reviewRoute migration rule link usability
    notHighImpact promotion transitionMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, rule,
    link, usability, notHighImpact, promotion, transitionMissing]

theorem constitutional_record_without_nonclaim_boundary_preserves_boundary
    {review : ConstitutionalLifecycleReview} :
    review.predicateRecorded = true ->
    review.normativeSourceRecorded = true ->
    review.operationalTestRecorded = true ->
    review.protectedScopeRecorded = true ->
    review.conflictBehaviorRecorded = true ->
    review.reviewRouteRecorded = true ->
    review.migrationPolicyRecorded = true ->
    review.selfModificationRuleRecorded = true ->
    review.agencyRightsLinked = true ->
    review.materialUsabilityRecorded = true ->
    review.highImpactAction = false ->
    review.supportPromotionRequested = false ->
    review.nonClaimBoundaryRecorded = false ->
    ConstitutionalLifecycleRouteFor review =
      ConstitutionalLifecycleRoute.preserveNonClaimBoundary := by
  intro predicate source test scope conflict reviewRoute migration rule link usability
    notHighImpact noPromotion boundaryMissing
  unfold ConstitutionalLifecycleRouteFor
  simp [predicate, source, test, scope, conflict, reviewRoute, migration, rule,
    link, usability, notHighImpact, noPromotion, boundaryMissing]

theorem complete_constitutional_lifecycle_admits_constraint :
    ConstitutionalLifecycleRouteFor completeConstitutionalLifecycleReview =
      ConstitutionalLifecycleRoute.admitConstitutionalConstraint := by
  unfold ConstitutionalLifecycleRouteFor completeConstitutionalLifecycleReview
  simp

/-! ## Versioned constitutional transition lifecycle

This model makes review, activation, conflict residualization, and rollback
separate accepted events. All identities, reviewer labels, and observations are
trusted finite inputs; the transition system proves custody and ordering, not
moral correctness, reviewer competence, or deployed enforcement.
-/

inductive ConstitutionStage where
  | draft
  | reviewed
  | active
  | residualized
  | rolledBack
deriving DecidableEq, Repr

inductive ConstitutionEventKind where
  | recordReview
  | activate
  | recordConflict
  | rollback
deriving DecidableEq, Repr

structure ConstitutionState where
  constitutionId : Nat
  predicateId : Nat
  protectedScopeId : Nat
  proposerId : Nat
  reviewerId : Nat
  version : Nat
  rollbackVersion : Nat
  authorityCeiling : Nat
  stage : ConstitutionStage
  residualCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

structure ConstitutionEvent where
  kind : ConstitutionEventKind
  constitutionId : Nat
  predicateId : Nat
  protectedScopeId : Nat
  actorId : Nat
  reviewerId : Nat
  expectedVersion : Nat
  targetVersion : Nat
  rollbackTargetVersion : Nat
  requestedAuthorityCeiling : Nat
  requestsActionAuthority : Bool
deriving DecidableEq, Repr

def ConstitutionEventAdmissible
    (state : ConstitutionState) (event : ConstitutionEvent) : Prop :=
  event.constitutionId = state.constitutionId ∧
    event.predicateId = state.predicateId ∧
    event.protectedScopeId = state.protectedScopeId ∧
    event.expectedVersion = state.version ∧
    event.requestedAuthorityCeiling = state.authorityCeiling ∧
    event.requestsActionAuthority = false ∧
    match event.kind with
    | ConstitutionEventKind.recordReview =>
        state.stage = ConstitutionStage.draft ∧
          event.actorId = state.proposerId ∧
          event.reviewerId ≠ state.proposerId ∧
          event.targetVersion = state.version
    | ConstitutionEventKind.activate =>
        state.stage = ConstitutionStage.reviewed ∧
          state.reviewerId ≠ state.proposerId ∧
          event.reviewerId = state.reviewerId ∧
          event.targetVersion = state.version + 1 ∧
          event.rollbackTargetVersion = state.version
    | ConstitutionEventKind.recordConflict =>
        state.stage = ConstitutionStage.active ∧
          event.reviewerId = state.reviewerId ∧
          event.targetVersion = state.version
    | ConstitutionEventKind.rollback =>
        state.stage = ConstitutionStage.residualized ∧
          event.reviewerId = state.reviewerId ∧
          event.targetVersion = state.rollbackVersion

instance constitutionEventAdmissibleDecidable
    (state : ConstitutionState) (event : ConstitutionEvent) :
    Decidable (ConstitutionEventAdmissible state event) := by
  unfold ConstitutionEventAdmissible
  cases event.kind <;> infer_instance

def AdvanceConstitution
    (state : ConstitutionState) (event : ConstitutionEvent) : ConstitutionState :=
  match event.kind with
  | ConstitutionEventKind.recordReview =>
      { state with
        stage := ConstitutionStage.reviewed,
        reviewerId := event.reviewerId }
  | ConstitutionEventKind.activate =>
      { state with
        stage := ConstitutionStage.active,
        version := event.targetVersion,
        rollbackVersion := event.rollbackTargetVersion }
  | ConstitutionEventKind.recordConflict =>
      { state with
        stage := ConstitutionStage.residualized,
        residualCount := state.residualCount + 1 }
  | ConstitutionEventKind.rollback =>
      { state with
        stage := ConstitutionStage.rolledBack,
        version := event.targetVersion }

def ApplyConstitutionEvent
    (state : ConstitutionState) (event : ConstitutionEvent) : Option ConstitutionState :=
  if ConstitutionEventAdmissible state event then
    some (AdvanceConstitution state event)
  else
    none

def RunConstitutionEvents :
    ConstitutionState → List ConstitutionEvent → Option ConstitutionState
  | state, [] => some state
  | state, event :: tail =>
      match ApplyConstitutionEvent state event with
      | none => none
      | some next => RunConstitutionEvents next tail

theorem accepted_constitution_event_is_admissible
    {state next : ConstitutionState} {event : ConstitutionEvent}
    (accepted : ApplyConstitutionEvent state event = some next) :
    ConstitutionEventAdmissible state event := by
  unfold ApplyConstitutionEvent at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_constitution_event_is_exact_advance
    {state next : ConstitutionState} {event : ConstitutionEvent}
    (accepted : ApplyConstitutionEvent state event = some next) :
    next = AdvanceConstitution state event := by
  unfold ApplyConstitutionEvent at accepted
  split at accepted
  · simp at accepted
    exact accepted.symm
  · simp at accepted

theorem accepted_constitution_event_preserves_custody
    {state next : ConstitutionState} {event : ConstitutionEvent}
    (accepted : ApplyConstitutionEvent state event = some next) :
    next.constitutionId = state.constitutionId ∧
      next.predicateId = state.predicateId ∧
      next.protectedScopeId = state.protectedScopeId ∧
      next.proposerId = state.proposerId ∧
      next.authorityCeiling = state.authorityCeiling := by
  have exactAdvance := accepted_constitution_event_is_exact_advance accepted
  subst next
  cases kind : event.kind <;> simp [AdvanceConstitution, kind]

theorem accepted_constitution_event_is_non_authorizing
    {state next : ConstitutionState} {event : ConstitutionEvent}
    (accepted : ApplyConstitutionEvent state event = some next) :
    event.requestsActionAuthority = false ∧
      next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectCount = state.externalEffectCount := by
  have admissible := accepted_constitution_event_is_admissible accepted
  have exactAdvance := accepted_constitution_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, noAuthority, _⟩
  subst next
  exact ⟨noAuthority,
    by cases kind : event.kind <;> simp [AdvanceConstitution, kind],
    by cases kind : event.kind <;> simp [AdvanceConstitution, kind]⟩

theorem accepted_activation_requires_prior_independent_review
    {state next : ConstitutionState} {event : ConstitutionEvent}
    (kind : event.kind = ConstitutionEventKind.activate)
    (accepted : ApplyConstitutionEvent state event = some next) :
    state.stage = ConstitutionStage.reviewed ∧
      state.reviewerId ≠ state.proposerId ∧
      next.stage = ConstitutionStage.active ∧
      next.version = state.version + 1 ∧
      next.rollbackVersion = state.version := by
  have admissible := accepted_constitution_event_is_admissible accepted
  have exactAdvance := accepted_constitution_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨reviewed, independent, reviewer, target, rollback⟩
  subst next
  simp [AdvanceConstitution, kind, target, rollback, reviewed, independent]

theorem accepted_conflict_creates_one_residual
    {state next : ConstitutionState} {event : ConstitutionEvent}
    (kind : event.kind = ConstitutionEventKind.recordConflict)
    (accepted : ApplyConstitutionEvent state event = some next) :
    state.stage = ConstitutionStage.active ∧
      next.stage = ConstitutionStage.residualized ∧
      next.residualCount = state.residualCount + 1 := by
  have admissible := accepted_constitution_event_is_admissible accepted
  have exactAdvance := accepted_constitution_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceConstitution, kind, route.1]

theorem accepted_rollback_returns_to_recorded_version
    {state next : ConstitutionState} {event : ConstitutionEvent}
    (kind : event.kind = ConstitutionEventKind.rollback)
    (accepted : ApplyConstitutionEvent state event = some next) :
    state.stage = ConstitutionStage.residualized ∧
      next.stage = ConstitutionStage.rolledBack ∧
      next.version = state.rollbackVersion := by
  have admissible := accepted_constitution_event_is_admissible accepted
  have exactAdvance := accepted_constitution_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceConstitution, kind, route.1, route.2.2]

theorem constitution_run_preserves_custody_and_non_authority
    {initial final : ConstitutionState} {events : List ConstitutionEvent}
    (run : RunConstitutionEvents initial events = some final) :
    final.constitutionId = initial.constitutionId ∧
      final.predicateId = initial.predicateId ∧
      final.protectedScopeId = initial.protectedScopeId ∧
      final.proposerId = initial.proposerId ∧
      final.authorityCeiling = initial.authorityCeiling ∧
      final.supportAssignmentCount = initial.supportAssignmentCount ∧
      final.externalEffectCount = initial.externalEffectCount := by
  induction events generalizing initial with
  | nil => simp [RunConstitutionEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunConstitutionEvents] at run
      cases step : ApplyConstitutionEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          have stepCustody := accepted_constitution_event_preserves_custody step
          have stepBoundary := accepted_constitution_event_is_non_authorizing step
          have tailFacts := ih run
          rcases stepCustody with ⟨c, p, s, owner, ceiling⟩
          rcases stepBoundary with ⟨_, support, effects⟩
          rcases tailFacts with ⟨tc, tp, ts, towner, tceiling, tsupport, teffects⟩
          exact ⟨tc.trans c, tp.trans p, ts.trans s, towner.trans owner,
            tceiling.trans ceiling, tsupport.trans support, teffects.trans effects⟩

theorem constitution_runs_compose
    (initial : ConstitutionState) (before after : List ConstitutionEvent) :
    RunConstitutionEvents initial (before ++ after) =
      match RunConstitutionEvents initial before with
      | none => none
      | some middle => RunConstitutionEvents middle after := by
  induction before generalizing initial with
  | nil => simp [RunConstitutionEvents]
  | cons event tail ih =>
      simp only [List.cons_append, RunConstitutionEvents]
      cases step : ApplyConstitutionEvent initial event with
      | none => simp
      | some next => simp [ih]

def initialConstitutionState : ConstitutionState := {
  constitutionId := 7
  predicateId := 11
  protectedScopeId := 13
  proposerId := 17
  reviewerId := 0
  version := 1
  rollbackVersion := 1
  authorityCeiling := 3
  stage := ConstitutionStage.draft
  residualCount := 0
  supportAssignmentCount := 0
  externalEffectCount := 0
}

def reviewConstitutionEvent : ConstitutionEvent := {
  kind := ConstitutionEventKind.recordReview
  constitutionId := 7
  predicateId := 11
  protectedScopeId := 13
  actorId := 17
  reviewerId := 19
  expectedVersion := 1
  targetVersion := 1
  rollbackTargetVersion := 1
  requestedAuthorityCeiling := 3
  requestsActionAuthority := false
}

def activateConstitutionEvent : ConstitutionEvent := {
  reviewConstitutionEvent with
  kind := ConstitutionEventKind.activate
  actorId := 19
  expectedVersion := 1
  targetVersion := 2
}

def conflictConstitutionEvent : ConstitutionEvent := {
  activateConstitutionEvent with
  kind := ConstitutionEventKind.recordConflict
  expectedVersion := 2
  targetVersion := 2
  rollbackTargetVersion := 1
}

def rollbackConstitutionEvent : ConstitutionEvent := {
  conflictConstitutionEvent with
  kind := ConstitutionEventKind.rollback
  targetVersion := 1
}

def completeConstitutionTrace : List ConstitutionEvent :=
  [reviewConstitutionEvent, activateConstitutionEvent,
    conflictConstitutionEvent, rollbackConstitutionEvent]

theorem complete_constitution_trace_reaches_exact_rollback :
    RunConstitutionEvents initialConstitutionState completeConstitutionTrace =
      some {
        initialConstitutionState with
        reviewerId := 19
        stage := ConstitutionStage.rolledBack
        version := 1
        rollbackVersion := 1
        residualCount := 1
      } := by
  decide

theorem self_review_cannot_enter_reviewed_stage :
    ApplyConstitutionEvent initialConstitutionState
      { reviewConstitutionEvent with reviewerId := 17 } = none := by
  decide

theorem predicate_substitution_cannot_enter_reviewed_stage :
    ApplyConstitutionEvent initialConstitutionState
      { reviewConstitutionEvent with predicateId := 12 } = none := by
  decide

theorem authority_widening_cannot_enter_reviewed_stage :
    ApplyConstitutionEvent initialConstitutionState
      { reviewConstitutionEvent with requestedAuthorityCeiling := 4 } = none := by
  decide

theorem action_authority_request_cannot_enter_reviewed_stage :
    ApplyConstitutionEvent initialConstitutionState
      { reviewConstitutionEvent with requestsActionAuthority := true } = none := by
  decide

theorem activation_version_jump_is_rejected :
    RunConstitutionEvents initialConstitutionState
      [reviewConstitutionEvent, { activateConstitutionEvent with targetVersion := 3 }] = none := by
  decide

/-! ## Predicate-set refinement and exact rollback

This finite model separates preservation of predicate identity from a scalar
predicate count. It proves subset refinement and rollback only for two authored
Boolean predicates; it does not establish that either predicate is morally
correct, complete, usable, or correctly interpreted.
-/

structure FinitePredicateSet where
  dignity : Bool
  consent : Bool
deriving DecidableEq, Repr

def FinitePredicateSet.Refines
    (candidate prior : FinitePredicateSet) : Prop :=
  (candidate.dignity = true -> prior.dignity = true) ∧
    (candidate.consent = true -> prior.consent = true)

instance finitePredicateSetRefinesDecidable
    (candidate prior : FinitePredicateSet) :
    Decidable (FinitePredicateSet.Refines candidate prior) := by
  unfold FinitePredicateSet.Refines
  infer_instance

structure PredicateMigration where
  prior : FinitePredicateSet
  candidate : FinitePredicateSet
  proposerId : Nat
  reviewerId : Nat
  independentReviewRecorded : Bool
  rollbackRecorded : Bool
deriving DecidableEq, Repr

def PredicateMigrationAdmissible (migration : PredicateMigration) : Prop :=
  FinitePredicateSet.Refines migration.candidate migration.prior ∧
    migration.independentReviewRecorded = true ∧
    migration.reviewerId ≠ migration.proposerId ∧
    migration.rollbackRecorded = true

instance predicateMigrationAdmissibleDecidable (migration : PredicateMigration) :
    Decidable (PredicateMigrationAdmissible migration) := by
  unfold PredicateMigrationAdmissible
  infer_instance

structure ActivatedPredicateVersion where
  active : FinitePredicateSet
  rollback : FinitePredicateSet
deriving DecidableEq, Repr

def ActivatePredicateMigration
    (migration : PredicateMigration) : Option ActivatedPredicateVersion :=
  if PredicateMigrationAdmissible migration then
    some { active := migration.candidate, rollback := migration.prior }
  else
    none

def RollbackPredicateVersion
    (version : ActivatedPredicateVersion) : FinitePredicateSet :=
  version.rollback

theorem accepted_predicate_migration_is_admissible
    {migration : PredicateMigration} {version : ActivatedPredicateVersion}
    (accepted : ActivatePredicateMigration migration = some version) :
    PredicateMigrationAdmissible migration := by
  unfold ActivatePredicateMigration at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_predicate_migration_is_exact
    {migration : PredicateMigration} {version : ActivatedPredicateVersion}
    (accepted : ActivatePredicateMigration migration = some version) :
    version = { active := migration.candidate, rollback := migration.prior } := by
  unfold ActivatePredicateMigration at accepted
  split at accepted
  · simp at accepted
    exact accepted.symm
  · simp at accepted

theorem accepted_predicate_migration_refines_prior
    {migration : PredicateMigration} {version : ActivatedPredicateVersion}
    (accepted : ActivatePredicateMigration migration = some version) :
    FinitePredicateSet.Refines version.active migration.prior := by
  have admissible := accepted_predicate_migration_is_admissible accepted
  have exactVersion := accepted_predicate_migration_is_exact accepted
  rw [exactVersion]
  exact admissible.1

theorem accepted_predicate_migration_stores_exact_rollback
    {migration : PredicateMigration} {version : ActivatedPredicateVersion}
    (accepted : ActivatePredicateMigration migration = some version) :
    version.rollback = migration.prior := by
  rw [accepted_predicate_migration_is_exact accepted]

theorem rollback_restores_exact_prior_predicate_set
    {migration : PredicateMigration} {version : ActivatedPredicateVersion}
    (accepted : ActivatePredicateMigration migration = some version) :
    RollbackPredicateVersion version = migration.prior := by
  unfold RollbackPredicateVersion
  exact accepted_predicate_migration_stores_exact_rollback accepted

theorem predicate_refinement_is_transitive
    {newer middle prior : FinitePredicateSet}
    (newerRefines : FinitePredicateSet.Refines newer middle)
    (middleRefines : FinitePredicateSet.Refines middle prior) :
    FinitePredicateSet.Refines newer prior := by
  constructor
  · intro dignity
    exact middleRefines.1 (newerRefines.1 dignity)
  · intro consent
    exact middleRefines.2 (newerRefines.2 consent)

theorem accepted_migration_cannot_add_dignity
    {migration : PredicateMigration} {version : ActivatedPredicateVersion}
    (accepted : ActivatePredicateMigration migration = some version)
    (candidateDignity : version.active.dignity = true) :
    migration.prior.dignity = true := by
  exact (accepted_predicate_migration_refines_prior accepted).1 candidateDignity

theorem accepted_migration_cannot_add_consent
    {migration : PredicateMigration} {version : ActivatedPredicateVersion}
    (accepted : ActivatePredicateMigration migration = some version)
    (candidateConsent : version.active.consent = true) :
    migration.prior.consent = true := by
  exact (accepted_predicate_migration_refines_prior accepted).2 candidateConsent

def dignityOnlyPredicateSet : FinitePredicateSet :=
  { dignity := true, consent := false }

def consentOnlyPredicateSet : FinitePredicateSet :=
  { dignity := false, consent := true }

def wideningPredicateMigration : PredicateMigration :=
  { prior := dignityOnlyPredicateSet
    candidate := { dignity := true, consent := true }
    proposerId := 17
    reviewerId := 19
    independentReviewRecorded := true
    rollbackRecorded := true }

theorem predicate_widening_migration_is_rejected :
    ActivatePredicateMigration wideningPredicateMigration = none := by
  decide

def FinitePredicateSet.count (predicates : FinitePredicateSet) : Nat :=
  (if predicates.dignity then 1 else 0) +
    (if predicates.consent then 1 else 0)

theorem equal_predicate_counts_do_not_identify_predicate_sets :
    dignityOnlyPredicateSet ≠ consentOnlyPredicateSet ∧
      dignityOnlyPredicateSet.count = consentOnlyPredicateSet.count := by
  decide

theorem no_predicate_count_decoder_recovers_both_collision_witnesses
    (decode : Nat -> FinitePredicateSet) :
    decode dignityOnlyPredicateSet.count ≠ dignityOnlyPredicateSet ∨
      decode consentOnlyPredicateSet.count ≠ consentOnlyPredicateSet := by
  rcases equal_predicate_counts_do_not_identify_predicate_sets with
    ⟨distinct, collision⟩
  by_cases recoversDignity :
      decode dignityOnlyPredicateSet.count = dignityOnlyPredicateSet
  · right
    intro recoversConsent
    apply distinct
    calc
      dignityOnlyPredicateSet = decode dignityOnlyPredicateSet.count :=
        recoversDignity.symm
      _ = decode consentOnlyPredicateSet.count := congrArg decode collision
      _ = consentOnlyPredicateSet := recoversConsent
  · exact Or.inl recoversDignity

/-! ## Contestable constitutional amendment lifecycle

This finite lifecycle separates proposal, independent review, ratification,
activation, affected-party appeal, appeal adjudication, and rollback. The model
proves exact role separation, predicate-set refinement, record custody,
non-authority, adverse-history preservation, and exact modeled rollback. Actor
identities, affected-party standing, predicate meaning, reviewer competence,
ratifier legitimacy, and correspondence with external effects remain trusted
inputs rather than conclusions.
-/

inductive AmendmentStage where
  | draft
  | reviewed
  | ratified
  | active
  | appealed
  | appealUpheld
  | rolledBack
deriving DecidableEq, Repr

inductive AmendmentEventKind where
  | recordReview
  | ratify
  | activate
  | fileAppeal
  | upholdAppeal
  | rollback
deriving DecidableEq, Repr

structure AmendmentState where
  constitutionId : Nat
  amendmentId : Nat
  prior : FinitePredicateSet
  candidate : FinitePredicateSet
  active : FinitePredicateSet
  proposerId : Nat
  reviewerId : Nat
  ratifierId : Nat
  affectedPartyId : Nat
  appealReviewerId : Nat
  version : Nat
  rollbackVersion : Nat
  authorityCeiling : Nat
  stage : AmendmentStage
  dissentCount : Nat
  adverseRecordCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

structure AmendmentEvent where
  kind : AmendmentEventKind
  constitutionId : Nat
  amendmentId : Nat
  actorId : Nat
  reviewerId : Nat
  ratifierId : Nat
  appealReviewerId : Nat
  expectedVersion : Nat
  targetVersion : Nat
  rollbackTargetVersion : Nat
  requestedAuthorityCeiling : Nat
  requestsActionAuthority : Bool
deriving DecidableEq, Repr

def AmendmentEventAdmissible
    (state : AmendmentState) (event : AmendmentEvent) : Prop :=
  event.constitutionId = state.constitutionId ∧
    event.amendmentId = state.amendmentId ∧
    event.expectedVersion = state.version ∧
    event.requestedAuthorityCeiling ≤ state.authorityCeiling ∧
    event.requestsActionAuthority = false ∧
    match event.kind with
    | AmendmentEventKind.recordReview =>
        state.stage = AmendmentStage.draft ∧
          event.actorId = state.proposerId ∧
          event.reviewerId ≠ state.proposerId ∧
          event.targetVersion = state.version
    | AmendmentEventKind.ratify =>
        state.stage = AmendmentStage.reviewed ∧
          event.reviewerId = state.reviewerId ∧
          event.actorId = event.ratifierId ∧
          state.reviewerId ≠ state.proposerId ∧
          event.ratifierId ≠ state.proposerId ∧
          event.ratifierId ≠ state.reviewerId ∧
          FinitePredicateSet.Refines state.candidate state.prior ∧
          event.targetVersion = state.version
    | AmendmentEventKind.activate =>
        state.stage = AmendmentStage.ratified ∧
          event.actorId = state.ratifierId ∧
          event.ratifierId = state.ratifierId ∧
          event.targetVersion = state.version + 1 ∧
          event.rollbackTargetVersion = state.version
    | AmendmentEventKind.fileAppeal =>
        state.stage = AmendmentStage.active ∧
          event.actorId = state.affectedPartyId ∧
          event.appealReviewerId ≠ state.proposerId ∧
          event.appealReviewerId ≠ state.reviewerId ∧
          event.appealReviewerId ≠ state.ratifierId ∧
          event.appealReviewerId ≠ state.affectedPartyId ∧
          event.targetVersion = state.version
    | AmendmentEventKind.upholdAppeal =>
        state.stage = AmendmentStage.appealed ∧
          event.actorId = state.appealReviewerId ∧
          event.appealReviewerId = state.appealReviewerId ∧
          event.targetVersion = state.version
    | AmendmentEventKind.rollback =>
        state.stage = AmendmentStage.appealUpheld ∧
          event.actorId = state.ratifierId ∧
          event.ratifierId = state.ratifierId ∧
          event.targetVersion = state.rollbackVersion

instance amendmentEventAdmissibleDecidable
    (state : AmendmentState) (event : AmendmentEvent) :
    Decidable (AmendmentEventAdmissible state event) := by
  unfold AmendmentEventAdmissible
  cases event.kind <;> infer_instance

def AdvanceAmendment
    (state : AmendmentState) (event : AmendmentEvent) : AmendmentState :=
  match event.kind with
  | AmendmentEventKind.recordReview =>
      { state with
        stage := AmendmentStage.reviewed
        reviewerId := event.reviewerId
        authorityCeiling := event.requestedAuthorityCeiling }
  | AmendmentEventKind.ratify =>
      { state with
        stage := AmendmentStage.ratified
        ratifierId := event.ratifierId
        authorityCeiling := event.requestedAuthorityCeiling }
  | AmendmentEventKind.activate =>
      { state with
        stage := AmendmentStage.active
        active := state.candidate
        version := event.targetVersion
        rollbackVersion := event.rollbackTargetVersion
        authorityCeiling := event.requestedAuthorityCeiling }
  | AmendmentEventKind.fileAppeal =>
      { state with
        stage := AmendmentStage.appealed
        appealReviewerId := event.appealReviewerId
        dissentCount := state.dissentCount + 1
        adverseRecordCount := state.adverseRecordCount + 1
        authorityCeiling := event.requestedAuthorityCeiling }
  | AmendmentEventKind.upholdAppeal =>
      { state with
        stage := AmendmentStage.appealUpheld
        authorityCeiling := event.requestedAuthorityCeiling }
  | AmendmentEventKind.rollback =>
      { state with
        stage := AmendmentStage.rolledBack
        active := state.prior
        version := event.targetVersion
        authorityCeiling := event.requestedAuthorityCeiling }

def ApplyAmendmentEvent
    (state : AmendmentState) (event : AmendmentEvent) : Option AmendmentState :=
  if AmendmentEventAdmissible state event then
    some (AdvanceAmendment state event)
  else
    none

def RunAmendmentEvents :
    AmendmentState → List AmendmentEvent → Option AmendmentState
  | state, [] => some state
  | state, event :: tail =>
      match ApplyAmendmentEvent state event with
      | none => none
      | some next => RunAmendmentEvents next tail

theorem accepted_amendment_event_is_admissible
    {state next : AmendmentState} {event : AmendmentEvent}
    (accepted : ApplyAmendmentEvent state event = some next) :
    AmendmentEventAdmissible state event := by
  unfold ApplyAmendmentEvent at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_amendment_event_is_exact_advance
    {state next : AmendmentState} {event : AmendmentEvent}
    (accepted : ApplyAmendmentEvent state event = some next) :
    next = AdvanceAmendment state event := by
  unfold ApplyAmendmentEvent at accepted
  split at accepted
  · simpa using accepted.symm
  · simp at accepted

theorem accepted_amendment_event_preserves_custody
    {state next : AmendmentState} {event : AmendmentEvent}
    (accepted : ApplyAmendmentEvent state event = some next) :
    next.constitutionId = state.constitutionId ∧
      next.amendmentId = state.amendmentId ∧
      next.prior = state.prior ∧
      next.candidate = state.candidate ∧
      next.proposerId = state.proposerId ∧
      next.affectedPartyId = state.affectedPartyId := by
  rw [accepted_amendment_event_is_exact_advance accepted]
  cases kind : event.kind <;> simp [AdvanceAmendment, kind]

theorem accepted_amendment_event_is_non_authorizing
    {state next : AmendmentState} {event : AmendmentEvent}
    (accepted : ApplyAmendmentEvent state event = some next) :
    next.authorityCeiling ≤ state.authorityCeiling ∧
      event.requestsActionAuthority = false ∧
      next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectCount = state.externalEffectCount := by
  have admissible := accepted_amendment_event_is_admissible accepted
  have exactAdvance := accepted_amendment_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, ceiling, noAuthority, _⟩
  subst next
  exact ⟨by cases kind : event.kind <;> simpa [AdvanceAmendment, kind] using ceiling,
    noAuthority,
    by cases kind : event.kind <;> simp [AdvanceAmendment, kind],
    by cases kind : event.kind <;> simp [AdvanceAmendment, kind]⟩

theorem accepted_review_separates_proposer_and_reviewer
    {state next : AmendmentState} {event : AmendmentEvent}
    (kind : event.kind = AmendmentEventKind.recordReview)
    (accepted : ApplyAmendmentEvent state event = some next) :
    state.stage = AmendmentStage.draft ∧
      next.stage = AmendmentStage.reviewed ∧
      next.reviewerId ≠ state.proposerId := by
  have admissible := accepted_amendment_event_is_admissible accepted
  have exactAdvance := accepted_amendment_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceAmendment, kind, route.1, route.2.2.1]

theorem accepted_ratification_separates_all_three_roles
    {state next : AmendmentState} {event : AmendmentEvent}
    (kind : event.kind = AmendmentEventKind.ratify)
    (accepted : ApplyAmendmentEvent state event = some next) :
    state.reviewerId ≠ state.proposerId ∧
      next.ratifierId ≠ state.proposerId ∧
      next.ratifierId ≠ state.reviewerId := by
  have admissible := accepted_amendment_event_is_admissible accepted
  have exactAdvance := accepted_amendment_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with
    ⟨_, _, _, reviewerIndependent, ratifierProposer,
      ratifierReviewer, _, _⟩
  subst next
  simpa [AdvanceAmendment, kind] using
    ⟨reviewerIndependent, ratifierProposer, ratifierReviewer⟩

theorem accepted_ratification_requires_predicate_refinement
    {state next : AmendmentState} {event : AmendmentEvent}
    (kind : event.kind = AmendmentEventKind.ratify)
    (accepted : ApplyAmendmentEvent state event = some next) :
    FinitePredicateSet.Refines state.candidate state.prior := by
  have admissible := accepted_amendment_event_is_admissible accepted
  rcases admissible with ⟨_, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨_, _, _, _, _, _, refinement, _⟩
  exact refinement

theorem accepted_activation_uses_ratified_candidate_and_records_rollback
    {state next : AmendmentState} {event : AmendmentEvent}
    (kind : event.kind = AmendmentEventKind.activate)
    (accepted : ApplyAmendmentEvent state event = some next) :
    state.stage = AmendmentStage.ratified ∧
      next.stage = AmendmentStage.active ∧
      next.active = state.candidate ∧
      next.version = state.version + 1 ∧
      next.rollbackVersion = state.version := by
  have admissible := accepted_amendment_event_is_admissible accepted
  have exactAdvance := accepted_amendment_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceAmendment, kind, route.1, route.2.2.2.1, route.2.2.2.2]

theorem accepted_appeal_preserves_dissent_and_adverse_record
    {state next : AmendmentState} {event : AmendmentEvent}
    (kind : event.kind = AmendmentEventKind.fileAppeal)
    (accepted : ApplyAmendmentEvent state event = some next) :
    state.stage = AmendmentStage.active ∧
      next.stage = AmendmentStage.appealed ∧
      next.dissentCount = state.dissentCount + 1 ∧
      next.adverseRecordCount = state.adverseRecordCount + 1 := by
  have admissible := accepted_amendment_event_is_admissible accepted
  have exactAdvance := accepted_amendment_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceAmendment, kind, route.1]

theorem accepted_appeal_resolution_preserves_adverse_record
    {state next : AmendmentState} {event : AmendmentEvent}
    (kind : event.kind = AmendmentEventKind.upholdAppeal)
    (accepted : ApplyAmendmentEvent state event = some next) :
    state.stage = AmendmentStage.appealed ∧
      next.stage = AmendmentStage.appealUpheld ∧
      next.dissentCount = state.dissentCount ∧
      next.adverseRecordCount = state.adverseRecordCount := by
  have admissible := accepted_amendment_event_is_admissible accepted
  have exactAdvance := accepted_amendment_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceAmendment, kind, route.1]

theorem accepted_amendment_rollback_restores_exact_prior
    {state next : AmendmentState} {event : AmendmentEvent}
    (kind : event.kind = AmendmentEventKind.rollback)
    (accepted : ApplyAmendmentEvent state event = some next) :
    state.stage = AmendmentStage.appealUpheld ∧
      next.stage = AmendmentStage.rolledBack ∧
      next.active = state.prior ∧
      next.version = state.rollbackVersion := by
  have admissible := accepted_amendment_event_is_admissible accepted
  have exactAdvance := accepted_amendment_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, route⟩
  rw [kind] at route
  subst next
  simp [AdvanceAmendment, kind, route.1, route.2.2.2]

theorem accepted_amendment_rollback_preserves_dissent_and_adverse_record
    {state next : AmendmentState} {event : AmendmentEvent}
    (kind : event.kind = AmendmentEventKind.rollback)
    (accepted : ApplyAmendmentEvent state event = some next) :
    next.dissentCount = state.dissentCount ∧
      next.adverseRecordCount = state.adverseRecordCount := by
  rw [accepted_amendment_event_is_exact_advance accepted]
  simp [AdvanceAmendment, kind]

theorem accepted_amendment_event_never_erases_contestability_records
    {state next : AmendmentState} {event : AmendmentEvent}
    (accepted : ApplyAmendmentEvent state event = some next) :
    state.dissentCount ≤ next.dissentCount ∧
      state.adverseRecordCount ≤ next.adverseRecordCount := by
  rw [accepted_amendment_event_is_exact_advance accepted]
  cases kind : event.kind <;> simp [AdvanceAmendment, kind]

theorem amendment_run_preserves_custody_and_non_authority
    {initial final : AmendmentState} {events : List AmendmentEvent}
    (run : RunAmendmentEvents initial events = some final) :
    final.constitutionId = initial.constitutionId ∧
      final.amendmentId = initial.amendmentId ∧
      final.prior = initial.prior ∧
      final.candidate = initial.candidate ∧
      final.proposerId = initial.proposerId ∧
      final.affectedPartyId = initial.affectedPartyId ∧
      final.authorityCeiling ≤ initial.authorityCeiling ∧
      final.supportAssignmentCount = initial.supportAssignmentCount ∧
      final.externalEffectCount = initial.externalEffectCount := by
  induction events generalizing initial with
  | nil => simp [RunAmendmentEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunAmendmentEvents] at run
      cases step : ApplyAmendmentEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          rcases accepted_amendment_event_preserves_custody step with
            ⟨c, a, prior, candidate, proposer, affected⟩
          rcases accepted_amendment_event_is_non_authorizing step with
            ⟨ceiling, _, support, effects⟩
          rcases ih run with
            ⟨tc, ta, tprior, tcandidate, tproposer, taffected,
              tceiling, tsupport, teffects⟩
          exact ⟨tc.trans c, ta.trans a, tprior.trans prior,
            tcandidate.trans candidate, tproposer.trans proposer,
            taffected.trans affected, Nat.le_trans tceiling ceiling,
            tsupport.trans support, teffects.trans effects⟩

theorem amendment_run_never_erases_contestability_records
    {initial final : AmendmentState} {events : List AmendmentEvent}
    (run : RunAmendmentEvents initial events = some final) :
    initial.dissentCount ≤ final.dissentCount ∧
      initial.adverseRecordCount ≤ final.adverseRecordCount := by
  induction events generalizing initial with
  | nil => simp [RunAmendmentEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunAmendmentEvents] at run
      cases step : ApplyAmendmentEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          have head := accepted_amendment_event_never_erases_contestability_records step
          have rest := ih run
          exact ⟨Nat.le_trans head.1 rest.1, Nat.le_trans head.2 rest.2⟩

theorem amendment_runs_compose
    (initial : AmendmentState) (before after : List AmendmentEvent) :
    RunAmendmentEvents initial (before ++ after) =
      match RunAmendmentEvents initial before with
      | none => none
      | some middle => RunAmendmentEvents middle after := by
  induction before generalizing initial with
  | nil => simp [RunAmendmentEvents]
  | cons event tail ih =>
      simp only [List.cons_append, RunAmendmentEvents]
      cases step : ApplyAmendmentEvent initial event with
      | none => simp
      | some next => simp [ih]

def initialAmendmentState : AmendmentState := {
  constitutionId := 7
  amendmentId := 23
  prior := { dignity := true, consent := true }
  candidate := dignityOnlyPredicateSet
  active := { dignity := true, consent := true }
  proposerId := 17
  reviewerId := 0
  ratifierId := 0
  affectedPartyId := 29
  appealReviewerId := 0
  version := 1
  rollbackVersion := 1
  authorityCeiling := 3
  stage := AmendmentStage.draft
  dissentCount := 0
  adverseRecordCount := 0
  supportAssignmentCount := 0
  externalEffectCount := 0
}

def reviewAmendmentEvent : AmendmentEvent := {
  kind := AmendmentEventKind.recordReview
  constitutionId := 7
  amendmentId := 23
  actorId := 17
  reviewerId := 19
  ratifierId := 0
  appealReviewerId := 0
  expectedVersion := 1
  targetVersion := 1
  rollbackTargetVersion := 1
  requestedAuthorityCeiling := 3
  requestsActionAuthority := false
}

def ratifyAmendmentEvent : AmendmentEvent := {
  reviewAmendmentEvent with
  kind := AmendmentEventKind.ratify
  actorId := 31
  ratifierId := 31
}

def activateAmendmentEvent : AmendmentEvent := {
  ratifyAmendmentEvent with
  kind := AmendmentEventKind.activate
  actorId := 31
  targetVersion := 2
}

def appealAmendmentEvent : AmendmentEvent := {
  activateAmendmentEvent with
  kind := AmendmentEventKind.fileAppeal
  actorId := 29
  appealReviewerId := 37
  expectedVersion := 2
  targetVersion := 2
}

def upholdAmendmentAppealEvent : AmendmentEvent := {
  appealAmendmentEvent with
  kind := AmendmentEventKind.upholdAppeal
  actorId := 37
}

def rollbackAmendmentEvent : AmendmentEvent := {
  upholdAmendmentAppealEvent with
  kind := AmendmentEventKind.rollback
  actorId := 31
  targetVersion := 1
}

def completeAmendmentTrace : List AmendmentEvent :=
  [reviewAmendmentEvent, ratifyAmendmentEvent, activateAmendmentEvent,
    appealAmendmentEvent, upholdAmendmentAppealEvent, rollbackAmendmentEvent]

theorem complete_amendment_trace_reaches_contestable_exact_rollback :
    RunAmendmentEvents initialAmendmentState completeAmendmentTrace =
      some {
        initialAmendmentState with
        reviewerId := 19
        ratifierId := 31
        appealReviewerId := 37
        stage := AmendmentStage.rolledBack
        active := initialAmendmentState.prior
        version := 1
        rollbackVersion := 1
        dissentCount := 1
        adverseRecordCount := 1
      } := by
  decide

theorem self_reviewed_amendment_is_rejected :
    ApplyAmendmentEvent initialAmendmentState
      { reviewAmendmentEvent with reviewerId := 17 } = none := by
  decide

theorem proposer_ratification_is_rejected :
    RunAmendmentEvents initialAmendmentState
      [reviewAmendmentEvent,
        { ratifyAmendmentEvent with
          actorId := 17
          ratifierId := 17 }] = none := by
  decide

theorem reviewer_ratification_is_rejected :
    RunAmendmentEvents initialAmendmentState
      [reviewAmendmentEvent,
        { ratifyAmendmentEvent with
          actorId := 19
          ratifierId := 19 }] = none := by
  decide

theorem widening_amendment_cannot_be_ratified :
    let widening := {
      initialAmendmentState with
      prior := dignityOnlyPredicateSet
      candidate := { dignity := true, consent := true }
      active := dignityOnlyPredicateSet
    }
    RunAmendmentEvents widening
      [reviewAmendmentEvent, ratifyAmendmentEvent] = none := by
  decide

theorem activation_before_ratification_is_rejected :
    RunAmendmentEvents initialAmendmentState
      [reviewAmendmentEvent, activateAmendmentEvent] = none := by
  decide

theorem outsider_appeal_is_rejected :
    RunAmendmentEvents initialAmendmentState
      [reviewAmendmentEvent, ratifyAmendmentEvent, activateAmendmentEvent,
        { appealAmendmentEvent with actorId := 41 }] = none := by
  decide

theorem captured_appeal_review_is_rejected :
    RunAmendmentEvents initialAmendmentState
      [reviewAmendmentEvent, ratifyAmendmentEvent, activateAmendmentEvent,
        { appealAmendmentEvent with appealReviewerId := 31 }] = none := by
  decide

theorem rollback_before_appeal_is_upheld_is_rejected :
    RunAmendmentEvents initialAmendmentState
      [reviewAmendmentEvent, ratifyAmendmentEvent, activateAmendmentEvent,
        appealAmendmentEvent, rollbackAmendmentEvent] = none := by
  decide

theorem rolled_back_amendment_is_closed
    (event : AmendmentEvent) :
    ApplyAmendmentEvent
      { initialAmendmentState with stage := AmendmentStage.rolledBack } event = none := by
  unfold ApplyAmendmentEvent
  split
  · rename_i admissible
    unfold AmendmentEventAdmissible at admissible
    rcases admissible with ⟨_, _, _, _, _, route⟩
    cases kind : event.kind <;> rw [kind] at route <;> simp at route
  · rfl

end AsiStackProofs.Alignment
