namespace AsiStackProofs.ArtifactStewardAgents

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

/-! ## Reachable work-contract dispatch review -/

inductive StewardDispatchState where
  | proposed
  | refusedNoRequest
  | repairObjective
  | repairAuthority
  | refuseAuthorityWidening
  | repairToolBoundary
  | repairVerification
  | repairBudget
  | requestBudgetApproval
  | repairRollback
  | repairNonClaimBoundary
  | dispatchReady
deriving DecidableEq, Repr

structure StewardDispatchContract where
  workRequested : Bool := true
  objectivePresent : Bool := true
  authorityBasisPresent : Bool := true
  requestedAuthorityWithinCharter : Bool := true
  allowedToolsRecorded : Bool := true
  forbiddenToolsRecorded : Bool := true
  verificationPlanPresent : Bool := true
  budgetPresent : Bool := true
  budgetWithinPolicy : Bool := true
  rollbackPlanPresent : Bool := true
  nonClaimBoundaryPresent : Bool := true
deriving DecidableEq, Repr

def StewardWorkContractComplete (review : StewardDispatchContract) : Bool :=
  review.workRequested && review.objectivePresent &&
    review.authorityBasisPresent && review.requestedAuthorityWithinCharter &&
      review.allowedToolsRecorded && review.forbiddenToolsRecorded &&
        review.verificationPlanPresent && review.budgetPresent &&
          review.budgetWithinPolicy && review.rollbackPlanPresent &&
            review.nonClaimBoundaryPresent

def StewardDispatchStepFor
    (review : StewardDispatchContract) : StewardDispatchState -> StewardDispatchState
  | .proposed =>
      if ! review.workRequested then .refusedNoRequest
      else if ! review.objectivePresent then .repairObjective
      else if ! review.authorityBasisPresent then .repairAuthority
      else if ! review.requestedAuthorityWithinCharter then .refuseAuthorityWidening
      else if ! review.allowedToolsRecorded || ! review.forbiddenToolsRecorded then
        .repairToolBoundary
      else if ! review.verificationPlanPresent then .repairVerification
      else if ! review.budgetPresent then .repairBudget
      else if ! review.budgetWithinPolicy then .requestBudgetApproval
      else if ! review.rollbackPlanPresent then .repairRollback
      else if ! review.nonClaimBoundaryPresent then .repairNonClaimBoundary
      else .dispatchReady
  | state => state

def StewardDispatchRun
    (review : StewardDispatchContract) : Nat -> StewardDispatchState
  | 0 => .proposed
  | n + 1 => StewardDispatchStepFor review (StewardDispatchRun review n)

def StewardDispatchSafe
    (review : StewardDispatchContract) (state : StewardDispatchState) : Prop :=
  state = .dispatchReady -> StewardWorkContractComplete review = true

theorem dispatch_ready_requires_complete_work_contract
    (review : StewardDispatchContract)
    (ready : StewardDispatchStepFor review .proposed = .dispatchReady) :
    StewardWorkContractComplete review = true := by
  unfold StewardDispatchStepFor at ready
  repeat split at ready <;> simp_all [StewardWorkContractComplete]

theorem steward_dispatch_step_preserves_contract_safety
    (review : StewardDispatchContract)
    (state : StewardDispatchState)
    (safe : StewardDispatchSafe review state) :
    StewardDispatchSafe review (StewardDispatchStepFor review state) := by
  cases state
  · intro ready
    exact dispatch_ready_requires_complete_work_contract review ready
  all_goals
    simp only [StewardDispatchSafe, StewardDispatchStepFor] at safe ⊢
    exact safe

theorem steward_dispatch_run_ready_requires_complete_contract
    (review : StewardDispatchContract) (steps : Nat)
    (ready : StewardDispatchRun review steps = .dispatchReady) :
    StewardWorkContractComplete review = true := by
  have safe : StewardDispatchSafe review (StewardDispatchRun review steps) := by
    clear ready
    induction steps with
    | zero => simp [StewardDispatchSafe, StewardDispatchRun]
    | succ n ih =>
        simpa [StewardDispatchRun] using
          steward_dispatch_step_preserves_contract_safety review
            (StewardDispatchRun review n) ih
  exact safe ready

theorem complete_work_contract_reaches_dispatch_ready :
    StewardDispatchRun ({} : StewardDispatchContract) 1 = .dispatchReady := by
  decide

theorem missing_work_objective_reaches_repair :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with objectivePresent := false } 1 =
        .repairObjective := by decide

theorem missing_work_authority_reaches_repair :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with authorityBasisPresent := false } 1 =
        .repairAuthority := by decide

theorem widened_work_authority_reaches_refusal :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with
          requestedAuthorityWithinCharter := false } 1 =
        .refuseAuthorityWidening := by decide

theorem missing_work_tool_boundary_reaches_repair :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with forbiddenToolsRecorded := false } 1 =
        .repairToolBoundary := by decide

theorem missing_work_verification_reaches_repair :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with verificationPlanPresent := false } 1 =
        .repairVerification := by decide

theorem missing_work_budget_reaches_repair :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with budgetPresent := false } 1 =
        .repairBudget := by decide

theorem over_policy_work_budget_reaches_approval :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with budgetWithinPolicy := false } 1 =
        .requestBudgetApproval := by decide

theorem missing_work_rollback_reaches_repair :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with rollbackPlanPresent := false } 1 =
        .repairRollback := by decide

theorem missing_work_non_claim_boundary_reaches_repair :
    StewardDispatchRun
      { ({} : StewardDispatchContract) with nonClaimBoundaryPresent := false } 1 =
        .repairNonClaimBoundary := by decide

/-! ## Reachable release-review gate -/

inductive StewardReleaseState where
  | candidate
  | refusedNoCandidate
  | repairArtifactBinding
  | repairTests
  | repairEvidence
  | repairChangelog
  | repairResiduals
  | requestApproval
  | refuseSupportPromotion
  | repairNonClaimBoundary
  | externalReviewReady
deriving DecidableEq, Repr

structure StewardReleaseReview where
  releaseCandidateRequested : Bool := true
  artifactBindingPresent : Bool := true
  testsRecorded : Bool := true
  evidenceRecorded : Bool := true
  changelogRecorded : Bool := true
  residualsRecorded : Bool := true
  approvalRecorded : Bool := true
  supportStateEffectNone : Bool := true
  chapterCoreEffectNone : Bool := true
  nonClaimBoundaryPresent : Bool := true
deriving DecidableEq, Repr

def StewardReleasePacketComplete (review : StewardReleaseReview) : Bool :=
  review.releaseCandidateRequested && review.artifactBindingPresent &&
    review.testsRecorded && review.evidenceRecorded && review.changelogRecorded &&
      review.residualsRecorded && review.approvalRecorded &&
        review.supportStateEffectNone && review.chapterCoreEffectNone &&
          review.nonClaimBoundaryPresent

def StewardReleaseStepFor
    (review : StewardReleaseReview) : StewardReleaseState -> StewardReleaseState
  | .candidate =>
      if ! review.releaseCandidateRequested then .refusedNoCandidate
      else if ! review.artifactBindingPresent then .repairArtifactBinding
      else if ! review.testsRecorded then .repairTests
      else if ! review.evidenceRecorded then .repairEvidence
      else if ! review.changelogRecorded then .repairChangelog
      else if ! review.residualsRecorded then .repairResiduals
      else if ! review.approvalRecorded then .requestApproval
      else if ! review.supportStateEffectNone || ! review.chapterCoreEffectNone then
        .refuseSupportPromotion
      else if ! review.nonClaimBoundaryPresent then .repairNonClaimBoundary
      else .externalReviewReady
  | state => state

def StewardReleaseRun (review : StewardReleaseReview) : Nat -> StewardReleaseState
  | 0 => .candidate
  | n + 1 => StewardReleaseStepFor review (StewardReleaseRun review n)

def StewardReleaseSafe
    (review : StewardReleaseReview) (state : StewardReleaseState) : Prop :=
  state = .externalReviewReady -> StewardReleasePacketComplete review = true

theorem release_review_ready_requires_complete_packet
    (review : StewardReleaseReview)
    (ready : StewardReleaseStepFor review .candidate = .externalReviewReady) :
    StewardReleasePacketComplete review = true := by
  unfold StewardReleaseStepFor at ready
  repeat split at ready <;> simp_all [StewardReleasePacketComplete]

theorem steward_release_step_preserves_packet_safety
    (review : StewardReleaseReview)
    (state : StewardReleaseState)
    (safe : StewardReleaseSafe review state) :
    StewardReleaseSafe review (StewardReleaseStepFor review state) := by
  cases state
  · intro ready
    exact release_review_ready_requires_complete_packet review ready
  all_goals
    simp only [StewardReleaseSafe, StewardReleaseStepFor] at safe ⊢
    exact safe

theorem steward_release_run_ready_requires_complete_packet
    (review : StewardReleaseReview) (steps : Nat)
    (ready : StewardReleaseRun review steps = .externalReviewReady) :
    StewardReleasePacketComplete review = true := by
  have safe : StewardReleaseSafe review (StewardReleaseRun review steps) := by
    clear ready
    induction steps with
    | zero => simp [StewardReleaseSafe, StewardReleaseRun]
    | succ n ih =>
        simpa [StewardReleaseRun] using
          steward_release_step_preserves_packet_safety review
            (StewardReleaseRun review n) ih
  exact safe ready

theorem complete_release_packet_reaches_external_review_ready :
    StewardReleaseRun ({} : StewardReleaseReview) 1 = .externalReviewReady := by
  decide

theorem missing_release_artifact_binding_reaches_repair :
    StewardReleaseRun
      { ({} : StewardReleaseReview) with artifactBindingPresent := false } 1 =
        .repairArtifactBinding := by decide

theorem missing_release_tests_reaches_repair :
    StewardReleaseRun
      { ({} : StewardReleaseReview) with testsRecorded := false } 1 =
        .repairTests := by decide

theorem missing_release_evidence_reaches_repair :
    StewardReleaseRun
      { ({} : StewardReleaseReview) with evidenceRecorded := false } 1 =
        .repairEvidence := by decide

theorem missing_release_changelog_reaches_repair :
    StewardReleaseRun
      { ({} : StewardReleaseReview) with changelogRecorded := false } 1 =
        .repairChangelog := by decide

theorem missing_release_residuals_reaches_repair :
    StewardReleaseRun
      { ({} : StewardReleaseReview) with residualsRecorded := false } 1 =
        .repairResiduals := by decide

theorem missing_release_approval_reaches_approval_request :
    StewardReleaseRun
      { ({} : StewardReleaseReview) with approvalRecorded := false } 1 =
        .requestApproval := by decide

theorem release_support_promotion_reaches_refusal :
    StewardReleaseRun
      { ({} : StewardReleaseReview) with supportStateEffectNone := false } 1 =
        .refuseSupportPromotion := by decide

theorem missing_release_non_claim_boundary_reaches_repair :
    StewardReleaseRun
      { ({} : StewardReleaseReview) with nonClaimBoundaryPresent := false } 1 =
        .repairNonClaimBoundary := by decide

end AsiStackProofs.ArtifactStewardAgents
