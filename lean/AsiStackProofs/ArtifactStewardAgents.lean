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

inductive StewardContributionRoute where
  | requestLedgerRepair
  | rejectCollapsedGovernance
  | requestEvidenceTransition
  | acceptLedger
deriving DecidableEq, Repr

structure StewardContributionLedgerReview where
  ledgerEntryProposed : Bool
  authorshipCreditRecorded : Bool
  reviewCreditRecorded : Bool
  evidenceCreditRecorded : Bool
  compensationRecorded : Bool
  reputationSignalRecorded : Bool
  governanceEffectRecorded : Bool
  conflictDisclosureRecorded : Bool
  collapsedScoreUsedForGovernance : Bool
  supportStateChangeRequested : Bool
  evidenceTransitionRecordPresent : Bool
deriving DecidableEq, Repr

def StewardContributionRouteFor
    (review : StewardContributionLedgerReview) : StewardContributionRoute :=
  if review.ledgerEntryProposed = false then
    StewardContributionRoute.requestLedgerRepair
  else if review.authorshipCreditRecorded = false then
    StewardContributionRoute.requestLedgerRepair
  else if review.reviewCreditRecorded = false then
    StewardContributionRoute.requestLedgerRepair
  else if review.evidenceCreditRecorded = false then
    StewardContributionRoute.requestLedgerRepair
  else if review.compensationRecorded = false then
    StewardContributionRoute.requestLedgerRepair
  else if review.reputationSignalRecorded = false then
    StewardContributionRoute.requestLedgerRepair
  else if review.governanceEffectRecorded = false then
    StewardContributionRoute.requestLedgerRepair
  else if review.conflictDisclosureRecorded = false then
    StewardContributionRoute.requestLedgerRepair
  else if review.collapsedScoreUsedForGovernance = true then
    StewardContributionRoute.rejectCollapsedGovernance
  else if
      review.supportStateChangeRequested = true &&
        review.evidenceTransitionRecordPresent = false then
    StewardContributionRoute.requestEvidenceTransition
  else
    StewardContributionRoute.acceptLedger

theorem missing_authorship_credit_routes_to_ledger_repair
    {review : StewardContributionLedgerReview} :
    review.ledgerEntryProposed = true ->
    review.authorshipCreditRecorded = false ->
      StewardContributionRouteFor review =
        StewardContributionRoute.requestLedgerRepair := by
  intro proposed missingAuthorship
  simp [StewardContributionRouteFor, proposed, missingAuthorship]

theorem collapsed_contribution_score_cannot_drive_governance_effect
    {review : StewardContributionLedgerReview} :
    review.ledgerEntryProposed = true ->
    review.authorshipCreditRecorded = true ->
    review.reviewCreditRecorded = true ->
    review.evidenceCreditRecorded = true ->
    review.compensationRecorded = true ->
    review.reputationSignalRecorded = true ->
    review.governanceEffectRecorded = true ->
    review.conflictDisclosureRecorded = true ->
    review.collapsedScoreUsedForGovernance = true ->
      StewardContributionRouteFor review =
        StewardContributionRoute.rejectCollapsedGovernance := by
  intro proposed authorship reviewCredit evidenceCredit compensation reputation governance conflict collapsed
  simp [
    StewardContributionRouteFor,
    proposed,
    authorship,
    reviewCredit,
    evidenceCredit,
    compensation,
    reputation,
    governance,
    conflict,
    collapsed,
  ]

theorem support_state_change_without_transition_requests_evidence_transition
    {review : StewardContributionLedgerReview} :
    review.ledgerEntryProposed = true ->
    review.authorshipCreditRecorded = true ->
    review.reviewCreditRecorded = true ->
    review.evidenceCreditRecorded = true ->
    review.compensationRecorded = true ->
    review.reputationSignalRecorded = true ->
    review.governanceEffectRecorded = true ->
    review.conflictDisclosureRecorded = true ->
    review.collapsedScoreUsedForGovernance = false ->
    review.supportStateChangeRequested = true ->
    review.evidenceTransitionRecordPresent = false ->
      StewardContributionRouteFor review =
        StewardContributionRoute.requestEvidenceTransition := by
  intro proposed authorship reviewCredit evidenceCredit compensation reputation governance conflict
    notCollapsed supportChange missingTransition
  simp [
    StewardContributionRouteFor,
    proposed,
    authorship,
    reviewCredit,
    evidenceCredit,
    compensation,
    reputation,
    governance,
    conflict,
    notCollapsed,
    supportChange,
    missingTransition,
  ]

theorem separated_contribution_ledger_without_support_change_accepts
    {review : StewardContributionLedgerReview} :
    review.ledgerEntryProposed = true ->
    review.authorshipCreditRecorded = true ->
    review.reviewCreditRecorded = true ->
    review.evidenceCreditRecorded = true ->
    review.compensationRecorded = true ->
    review.reputationSignalRecorded = true ->
    review.governanceEffectRecorded = true ->
    review.conflictDisclosureRecorded = true ->
    review.collapsedScoreUsedForGovernance = false ->
    review.supportStateChangeRequested = false ->
      StewardContributionRouteFor review =
        StewardContributionRoute.acceptLedger := by
  intro proposed authorship reviewCredit evidenceCredit compensation reputation governance conflict
    notCollapsed noSupportChange
  simp [
    StewardContributionRouteFor,
    proposed,
    authorship,
    reviewCredit,
    evidenceCredit,
    compensation,
    reputation,
    governance,
    conflict,
    notCollapsed,
    noSupportChange,
  ]

inductive StewardFederationRoute where
  | reject
  | requestContract
  | requestApproval
  | requestEvidenceBundle
  | dispatchScoped
deriving DecidableEq, Repr

structure StewardFederationContractReview where
  federationRequested : Bool
  workContractPresent : Bool
  workerAuthorityBounded : Bool
  allowedToolsRecorded : Bool
  forbiddenToolsRecorded : Bool
  dataClassAllowed : Bool
  budgetWithinPolicy : Bool
  evidenceBundleRequired : Bool
  workerReceivesProjectAuthority : Bool
  externalSpendRequested : Bool
  approvalPresent : Bool
deriving DecidableEq, Repr

def StewardFederationRouteFor
    (review : StewardFederationContractReview) : StewardFederationRoute :=
  if review.federationRequested = false then
    StewardFederationRoute.reject
  else if review.workContractPresent = false then
    StewardFederationRoute.requestContract
  else if review.workerReceivesProjectAuthority = true then
    StewardFederationRoute.reject
  else if review.workerAuthorityBounded = false then
    StewardFederationRoute.reject
  else if review.allowedToolsRecorded = false then
    StewardFederationRoute.requestContract
  else if review.forbiddenToolsRecorded = false then
    StewardFederationRoute.requestContract
  else if review.dataClassAllowed = false then
    StewardFederationRoute.reject
  else if review.budgetWithinPolicy = false then
    StewardFederationRoute.requestApproval
  else if review.externalSpendRequested = true && review.approvalPresent = false then
    StewardFederationRoute.requestApproval
  else if review.evidenceBundleRequired = false then
    StewardFederationRoute.requestEvidenceBundle
  else
    StewardFederationRoute.dispatchScoped

theorem federation_without_work_contract_requests_contract
    {review : StewardFederationContractReview} :
    review.federationRequested = true ->
    review.workContractPresent = false ->
      StewardFederationRouteFor review =
        StewardFederationRoute.requestContract := by
  intro requested missingContract
  simp [StewardFederationRouteFor, requested, missingContract]

theorem federated_worker_cannot_inherit_project_authority
    {review : StewardFederationContractReview} :
    review.federationRequested = true ->
    review.workContractPresent = true ->
    review.workerReceivesProjectAuthority = true ->
      StewardFederationRouteFor review = StewardFederationRoute.reject := by
  intro requested contractPresent inheritsAuthority
  simp [StewardFederationRouteFor, requested, contractPresent, inheritsAuthority]

theorem external_federation_spend_without_approval_routes_to_approval
    {review : StewardFederationContractReview} :
    review.federationRequested = true ->
    review.workContractPresent = true ->
    review.workerReceivesProjectAuthority = false ->
    review.workerAuthorityBounded = true ->
    review.allowedToolsRecorded = true ->
    review.forbiddenToolsRecorded = true ->
    review.dataClassAllowed = true ->
    review.budgetWithinPolicy = true ->
    review.externalSpendRequested = true ->
    review.approvalPresent = false ->
      StewardFederationRouteFor review =
        StewardFederationRoute.requestApproval := by
  intro requested contractPresent noInheritedAuthority bounded allowedTools forbiddenTools dataAllowed
    budgetOk spend missingApproval
  simp [
    StewardFederationRouteFor,
    requested,
    contractPresent,
    noInheritedAuthority,
    bounded,
    allowedTools,
    forbiddenTools,
    dataAllowed,
    budgetOk,
    spend,
    missingApproval,
  ]

theorem complete_scoped_federation_dispatches
    {review : StewardFederationContractReview} :
    review.federationRequested = true ->
    review.workContractPresent = true ->
    review.workerReceivesProjectAuthority = false ->
    review.workerAuthorityBounded = true ->
    review.allowedToolsRecorded = true ->
    review.forbiddenToolsRecorded = true ->
    review.dataClassAllowed = true ->
    review.budgetWithinPolicy = true ->
    review.externalSpendRequested = false ->
    review.evidenceBundleRequired = true ->
      StewardFederationRouteFor review =
        StewardFederationRoute.dispatchScoped := by
  intro requested contractPresent noInheritedAuthority bounded allowedTools forbiddenTools dataAllowed
    budgetOk noSpend evidenceRequired
  simp [
    StewardFederationRouteFor,
    requested,
    contractPresent,
    noInheritedAuthority,
    bounded,
    allowedTools,
    forbiddenTools,
    dataAllowed,
    budgetOk,
    noSpend,
    evidenceRequired,
  ]

end AsiStackProofs.ArtifactStewardAgents
