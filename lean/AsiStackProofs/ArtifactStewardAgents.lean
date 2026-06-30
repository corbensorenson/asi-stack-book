namespace AsiStackProofs.ArtifactStewardAgents

structure StewardWorkContractReview where
  contractDispatched : Bool
  objectiveRecorded : Bool
  authorityRecorded : Bool
  allowedToolsRecorded : Bool
  forbiddenToolsRecorded : Bool
  verificationRequirementsRecorded : Bool
  budgetRecorded : Bool
  nonClaimsRecorded : Bool
deriving DecidableEq, Repr

def DispatchedContractHasRequiredBoundary
    (review : StewardWorkContractReview) : Prop :=
  review.contractDispatched = true ->
    review.objectiveRecorded = true ∧
      review.authorityRecorded = true ∧
        review.allowedToolsRecorded = true ∧
          review.forbiddenToolsRecorded = true ∧
            review.verificationRequirementsRecorded = true ∧
              review.budgetRecorded = true ∧
                review.nonClaimsRecorded = true

theorem dispatched_steward_contract_records_required_boundary
    {review : StewardWorkContractReview} :
    DispatchedContractHasRequiredBoundary review ->
    review.contractDispatched = true ->
      review.objectiveRecorded = true ∧
        review.authorityRecorded = true ∧
          review.allowedToolsRecorded = true ∧
            review.forbiddenToolsRecorded = true ∧
              review.verificationRequirementsRecorded = true ∧
                review.budgetRecorded = true ∧
                  review.nonClaimsRecorded = true := by
  intro valid dispatched
  exact valid dispatched

structure StewardProtectedActionReview where
  exceedsTreasuryPolicy : Bool
  changesGovernanceRules : Bool
  touchesProtectedAssets : Bool
  explicitApprovalEvidencePresent : Bool
  actionExecuted : Bool
deriving DecidableEq, Repr

def MissingApprovalBlocksProtectedAction
    (review : StewardProtectedActionReview) : Prop :=
  (review.exceedsTreasuryPolicy = true ∨
      review.changesGovernanceRules = true ∨
        review.touchesProtectedAssets = true) ->
    review.explicitApprovalEvidencePresent = false ->
      review.actionExecuted = false

theorem protected_steward_action_without_approval_cannot_execute
    {review : StewardProtectedActionReview}
    (valid : MissingApprovalBlocksProtectedAction review)
    (protectedBoundary :
      review.exceedsTreasuryPolicy = true ∨
      review.changesGovernanceRules = true ∨
        review.touchesProtectedAssets = true)
    (missingApproval : review.explicitApprovalEvidencePresent = false) :
      review.actionExecuted = false := by
  exact valid protectedBoundary missingApproval

structure StewardReleaseGateReview where
  releasePublished : Bool
  testsRecorded : Bool
  evidenceRecorded : Bool
  changelogRecorded : Bool
  residualsRecorded : Bool
  approvalRecorded : Bool
deriving DecidableEq, Repr

def PublishedReleaseRequiresEvidenceGate
    (review : StewardReleaseGateReview) : Prop :=
  review.releasePublished = true ->
    review.testsRecorded = true ∧
      review.evidenceRecorded = true ∧
        review.changelogRecorded = true ∧
          review.residualsRecorded = true ∧
            review.approvalRecorded = true

theorem stewarded_release_publication_requires_test_evidence_changelog_residual_and_approval_records
    {review : StewardReleaseGateReview} :
    PublishedReleaseRequiresEvidenceGate review ->
    review.releasePublished = true ->
      review.testsRecorded = true ∧
        review.evidenceRecorded = true ∧
          review.changelogRecorded = true ∧
            review.residualsRecorded = true ∧
              review.approvalRecorded = true := by
  intro valid published
  exact valid published

structure StewardSunsetReview where
  sunsetCriteriaMet : Bool
  sunsetReviewOpened : Bool
  ordinaryWorkGenerated : Bool
deriving DecidableEq, Repr

def SunsetCriteriaBlocksOrdinaryWork
    (review : StewardSunsetReview) : Prop :=
  review.sunsetCriteriaMet = true ->
    review.sunsetReviewOpened = false ->
      review.ordinaryWorkGenerated = false

theorem sunset_criteria_block_ordinary_work_until_review_opened
    {review : StewardSunsetReview} :
    SunsetCriteriaBlocksOrdinaryWork review ->
    review.sunsetCriteriaMet = true ->
      review.sunsetReviewOpened = false ->
        review.ordinaryWorkGenerated = false := by
  intro valid criteriaMet noReview
  exact valid criteriaMet noReview

inductive StewardLifecycleRoute where
  | ordinaryWork
  | requestApproval
  | quarantineEvent
  | openSunsetReview
deriving DecidableEq, Repr

structure StewardLifecycleDecision where
  eventTainted : Bool
  eventReviewCompleted : Bool
  sunsetCriteriaMet : Bool
  sunsetReviewOpened : Bool
  autonomyIncreaseRequested : Bool
  charterApprovalPresent : Bool
  treasurySpendRequested : Bool
  withinTreasuryPolicy : Bool
deriving DecidableEq, Repr

def StewardLifecycleRouteFor (decision : StewardLifecycleDecision) : StewardLifecycleRoute :=
  if decision.eventTainted = true ∧ decision.eventReviewCompleted = false then
    StewardLifecycleRoute.quarantineEvent
  else if decision.sunsetCriteriaMet = true ∧ decision.sunsetReviewOpened = false then
    StewardLifecycleRoute.openSunsetReview
  else if decision.autonomyIncreaseRequested = true ∧ decision.charterApprovalPresent = false then
    StewardLifecycleRoute.requestApproval
  else if decision.treasurySpendRequested = true ∧ decision.withinTreasuryPolicy = false then
    StewardLifecycleRoute.requestApproval
  else
    StewardLifecycleRoute.ordinaryWork

theorem tainted_event_without_review_routes_to_quarantine
    {decision : StewardLifecycleDecision} :
    decision.eventTainted = true ->
    decision.eventReviewCompleted = false ->
    StewardLifecycleRouteFor decision = StewardLifecycleRoute.quarantineEvent := by
  intro tainted unreviewed
  unfold StewardLifecycleRouteFor
  simp [tainted, unreviewed]

theorem sunset_criteria_without_open_review_routes_to_sunset_review
    {decision : StewardLifecycleDecision} :
    decision.eventTainted = false ->
    decision.sunsetCriteriaMet = true ->
    decision.sunsetReviewOpened = false ->
    StewardLifecycleRouteFor decision = StewardLifecycleRoute.openSunsetReview := by
  intro untainted criteriaMet noReview
  unfold StewardLifecycleRouteFor
  simp [untainted, criteriaMet, noReview]

theorem autonomy_escalation_without_charter_approval_routes_to_approval
    {decision : StewardLifecycleDecision} :
    decision.eventTainted = false ->
    decision.sunsetCriteriaMet = false ->
    decision.autonomyIncreaseRequested = true ->
    decision.charterApprovalPresent = false ->
    StewardLifecycleRouteFor decision = StewardLifecycleRoute.requestApproval := by
  intro untainted noSunset escalation noApproval
  unfold StewardLifecycleRouteFor
  simp [untainted, noSunset, escalation, noApproval]

theorem treasury_spend_outside_policy_routes_to_approval
    {decision : StewardLifecycleDecision} :
    decision.eventTainted = false ->
    decision.sunsetCriteriaMet = false ->
    decision.autonomyIncreaseRequested = false ->
    decision.treasurySpendRequested = true ->
    decision.withinTreasuryPolicy = false ->
    StewardLifecycleRouteFor decision = StewardLifecycleRoute.requestApproval := by
  intro untainted noSunset noEscalation spend outsidePolicy
  unfold StewardLifecycleRouteFor
  simp [untainted, noSunset, noEscalation, spend, outsidePolicy]

end AsiStackProofs.ArtifactStewardAgents
