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

end AsiStackProofs.ArtifactStewardAgents
