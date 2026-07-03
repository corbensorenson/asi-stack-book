namespace AsiStackProofs.PersonalComputeHives

structure HiveAdmissionReview where
  schedulerAdmitted : Bool
  identityPolicyPassed : Bool
  dataPolicyPassed : Bool
  toolPolicyPassed : Bool
  federationPolicyPassed : Bool
  approvalPolicyPassed : Bool
deriving DecidableEq, Repr

def SchedulerAdmissionRequiresPolicyChecks
    (review : HiveAdmissionReview) : Prop :=
  review.schedulerAdmitted = true ->
    review.identityPolicyPassed = true ∧
      review.dataPolicyPassed = true ∧
        review.toolPolicyPassed = true ∧
          review.federationPolicyPassed = true ∧
            review.approvalPolicyPassed = true

theorem admitted_hive_job_has_identity_data_tool_federation_and_approval_checks
    {review : HiveAdmissionReview} :
    SchedulerAdmissionRequiresPolicyChecks review ->
    review.schedulerAdmitted = true ->
      review.identityPolicyPassed = true ∧
        review.dataPolicyPassed = true ∧
          review.toolPolicyPassed = true ∧
            review.federationPolicyPassed = true ∧
              review.approvalPolicyPassed = true := by
  intro valid admitted
  exact valid admitted

structure FasterNodePolicyReview where
  fasterNodeForbiddenByPolicy : Bool
  fasterNodeSelected : Bool
deriving DecidableEq, Repr

def ForbiddenFasterNodeIsRejected
    (review : FasterNodePolicyReview) : Prop :=
  review.fasterNodeForbiddenByPolicy = true ->
    review.fasterNodeSelected = false

theorem faster_forbidden_node_cannot_be_selected
    {review : FasterNodePolicyReview} :
    ForbiddenFasterNodeIsRejected review ->
    review.fasterNodeForbiddenByPolicy = true ->
      review.fasterNodeSelected = false := by
  intro valid forbidden
  exact valid forbidden

structure HighRiskApprovalReview where
  highRiskJob : Bool
  approvalRequired : Bool
  boundApprovalReceiptPresent : Bool
  jobExecuted : Bool
deriving DecidableEq, Repr

def HighRiskJobRequiresBoundApproval
    (review : HighRiskApprovalReview) : Prop :=
  review.highRiskJob = true ->
    review.approvalRequired = true ->
      review.jobExecuted = true ->
        review.boundApprovalReceiptPresent = true

theorem high_risk_hive_job_without_bound_approval_cannot_execute
    {review : HighRiskApprovalReview} :
    HighRiskJobRequiresBoundApproval review ->
    review.highRiskJob = true ->
      review.approvalRequired = true ->
        review.jobExecuted = true ->
          review.boundApprovalReceiptPresent = true := by
  intro valid highRisk approvalRequired executed
  exact valid highRisk approvalRequired executed

theorem high_risk_hive_job_missing_bound_approval_rejected
    {review : HighRiskApprovalReview} :
    review.highRiskJob = true ->
      review.approvalRequired = true ->
        review.jobExecuted = true ->
          review.boundApprovalReceiptPresent = false ->
            ¬ HighRiskJobRequiresBoundApproval review := by
  intro highRisk approvalRequired executed missingReceipt valid
  have receipt :=
    high_risk_hive_job_without_bound_approval_cannot_execute
      valid highRisk approvalRequired executed
  rw [missingReceipt] at receipt
  contradiction

structure FederationLeaseReview where
  externalAccessGranted : Bool
  activeLeasePresent : Bool
  scopeRecorded : Bool
  sandboxRecorded : Bool
  evidenceObligationsRecorded : Bool
  expirationRecorded : Bool
  revocationPathRecorded : Bool
deriving DecidableEq, Repr

def ExternalAccessRequiresLeaseBoundary
    (review : FederationLeaseReview) : Prop :=
  review.externalAccessGranted = true ->
    review.activeLeasePresent = true ∧
      review.scopeRecorded = true ∧
        review.sandboxRecorded = true ∧
          review.evidenceObligationsRecorded = true ∧
            review.expirationRecorded = true ∧
              review.revocationPathRecorded = true

theorem external_hive_access_requires_lease_scope_sandbox_evidence_expiration_and_revocation
    {review : FederationLeaseReview} :
    ExternalAccessRequiresLeaseBoundary review ->
    review.externalAccessGranted = true ->
      review.activeLeasePresent = true ∧
        review.scopeRecorded = true ∧
          review.sandboxRecorded = true ∧
            review.evidenceObligationsRecorded = true ∧
              review.expirationRecorded = true ∧
                review.revocationPathRecorded = true := by
  intro valid granted
  exact valid granted

theorem external_hive_access_missing_lease_boundary_rejected
    {review : FederationLeaseReview} :
    review.externalAccessGranted = true ->
      (review.activeLeasePresent = false ∨
        review.scopeRecorded = false ∨
          review.sandboxRecorded = false ∨
            review.evidenceObligationsRecorded = false ∨
              review.expirationRecorded = false ∨
                review.revocationPathRecorded = false) ->
        ¬ ExternalAccessRequiresLeaseBoundary review := by
  intro granted missing valid
  have boundary :=
    external_hive_access_requires_lease_scope_sandbox_evidence_expiration_and_revocation
      valid granted
  cases boundary with
  | intro lease rest =>
      cases rest with
      | intro scope rest =>
          cases rest with
          | intro sandbox rest =>
              cases rest with
              | intro evidence rest =>
                  cases rest with
                  | intro expiration revocation =>
                      cases missing with
                      | inl missingLease =>
                          rw [missingLease] at lease
                          contradiction
                      | inr restMissing =>
                          cases restMissing with
                          | inl missingScope =>
                              rw [missingScope] at scope
                              contradiction
                          | inr restMissing =>
                              cases restMissing with
                              | inl missingSandbox =>
                                  rw [missingSandbox] at sandbox
                                  contradiction
                              | inr restMissing =>
                                  cases restMissing with
                                  | inl missingEvidence =>
                                      rw [missingEvidence] at evidence
                                      contradiction
                                  | inr restMissing =>
                                      cases restMissing with
                                      | inl missingExpiration =>
                                          rw [missingExpiration] at expiration
                                          contradiction
                                      | inr missingRevocation =>
                                          rw [missingRevocation] at revocation
                                          contradiction

inductive HiveWorkAdmissionRoute where
  | rejectMalformedJob
  | requireIdentityPolicy
  | requireDataPolicy
  | requireToolPolicy
  | requireDeviceRegistry
  | requireSchedulerPolicy
  | requirePortalApproval
  | requireFederationLease
  | requireSandboxRecord
  | requireCostBudget
  | requireEnergyBudget
  | requireDropoutPlan
  | requireAuditReceipt
  | requireResidualOwner
  | requireEvidenceTransition
  | admitHiveWork
deriving DecidableEq, Repr

structure HiveWorkAdmissionReview where
  jobWellFormed : Bool
  identityPolicyPassed : Bool
  dataPolicyPassed : Bool
  toolPolicyPassed : Bool
  deviceRegistryReady : Bool
  schedulerPolicyPassed : Bool
  highRiskJob : Bool
  portalApprovalPresent : Bool
  externalHiveAccessRequested : Bool
  federationLeasePresent : Bool
  sandboxRecordPresent : Bool
  costBudgetRecorded : Bool
  energyBudgetRecorded : Bool
  dropoutPlanRecorded : Bool
  auditReceiptPlanned : Bool
  residualOwnerRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
deriving DecidableEq, Repr

def HiveWorkAdmissionRouteFor
    (review : HiveWorkAdmissionReview) : HiveWorkAdmissionRoute :=
  if review.jobWellFormed = false then
    HiveWorkAdmissionRoute.rejectMalformedJob
  else if review.identityPolicyPassed = false then
    HiveWorkAdmissionRoute.requireIdentityPolicy
  else if review.dataPolicyPassed = false then
    HiveWorkAdmissionRoute.requireDataPolicy
  else if review.toolPolicyPassed = false then
    HiveWorkAdmissionRoute.requireToolPolicy
  else if review.deviceRegistryReady = false then
    HiveWorkAdmissionRoute.requireDeviceRegistry
  else if review.schedulerPolicyPassed = false then
    HiveWorkAdmissionRoute.requireSchedulerPolicy
  else if review.highRiskJob = true ∧
      review.portalApprovalPresent = false then
    HiveWorkAdmissionRoute.requirePortalApproval
  else if review.externalHiveAccessRequested = true ∧
      review.federationLeasePresent = false then
    HiveWorkAdmissionRoute.requireFederationLease
  else if review.externalHiveAccessRequested = true ∧
      review.sandboxRecordPresent = false then
    HiveWorkAdmissionRoute.requireSandboxRecord
  else if review.costBudgetRecorded = false then
    HiveWorkAdmissionRoute.requireCostBudget
  else if review.energyBudgetRecorded = false then
    HiveWorkAdmissionRoute.requireEnergyBudget
  else if review.dropoutPlanRecorded = false then
    HiveWorkAdmissionRoute.requireDropoutPlan
  else if review.auditReceiptPlanned = false then
    HiveWorkAdmissionRoute.requireAuditReceipt
  else if review.residualOwnerRecorded = false then
    HiveWorkAdmissionRoute.requireResidualOwner
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    HiveWorkAdmissionRoute.requireEvidenceTransition
  else
    HiveWorkAdmissionRoute.admitHiveWork

theorem malformed_hive_job_rejected
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.rejectMalformedJob := by
  intro malformed
  unfold HiveWorkAdmissionRouteFor
  simp [malformed]

theorem missing_hive_identity_policy_requires_identity_policy
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireIdentityPolicy := by
  intro wellFormed missingIdentity
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, missingIdentity]

theorem missing_hive_data_policy_requires_data_policy
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireDataPolicy := by
  intro wellFormed identityPassed missingData
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, missingData]

theorem missing_hive_tool_policy_requires_tool_policy
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireToolPolicy := by
  intro wellFormed identityPassed dataPassed missingTool
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, missingTool]

theorem missing_hive_device_registry_requires_registry
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireDeviceRegistry := by
  intro wellFormed identityPassed dataPassed toolPassed missingRegistry
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, missingRegistry]

theorem missing_hive_scheduler_policy_requires_scheduler_policy
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireSchedulerPolicy := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    missingSchedulerPolicy
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    missingSchedulerPolicy]

theorem high_risk_hive_job_without_portal_approval_requires_approval
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = true ->
    review.portalApprovalPresent = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requirePortalApproval := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed highRisk missingApproval
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, highRisk, missingApproval]

theorem external_hive_access_without_lease_requires_federation_lease
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = true ->
    review.federationLeasePresent = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireFederationLease := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk externalAccess missingLease
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, externalAccess, missingLease]

theorem external_hive_access_without_sandbox_requires_sandbox_record
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = true ->
    review.federationLeasePresent = true ->
    review.sandboxRecordPresent = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireSandboxRecord := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk externalAccess leasePresent missingSandbox
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, externalAccess, leasePresent, missingSandbox]

theorem missing_hive_cost_budget_requires_cost_budget
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = false ->
    review.costBudgetRecorded = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireCostBudget := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk noExternal missingCost
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, noExternal, missingCost]

theorem missing_hive_energy_budget_requires_energy_budget
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = false ->
    review.costBudgetRecorded = true ->
    review.energyBudgetRecorded = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireEnergyBudget := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk noExternal costRecorded missingEnergy
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, noExternal, costRecorded, missingEnergy]

theorem missing_hive_dropout_plan_requires_dropout_plan
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = false ->
    review.costBudgetRecorded = true ->
    review.energyBudgetRecorded = true ->
    review.dropoutPlanRecorded = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireDropoutPlan := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk noExternal costRecorded energyRecorded
    missingDropout
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, noExternal, costRecorded, energyRecorded,
    missingDropout]

theorem missing_hive_audit_receipt_requires_receipt_plan
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = false ->
    review.costBudgetRecorded = true ->
    review.energyBudgetRecorded = true ->
    review.dropoutPlanRecorded = true ->
    review.auditReceiptPlanned = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireAuditReceipt := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk noExternal costRecorded energyRecorded
    dropoutRecorded missingReceipt
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, noExternal, costRecorded, energyRecorded,
    dropoutRecorded, missingReceipt]

theorem missing_hive_residual_owner_requires_residual_owner
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = false ->
    review.costBudgetRecorded = true ->
    review.energyBudgetRecorded = true ->
    review.dropoutPlanRecorded = true ->
    review.auditReceiptPlanned = true ->
    review.residualOwnerRecorded = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireResidualOwner := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk noExternal costRecorded energyRecorded
    dropoutRecorded receiptPlanned missingResidualOwner
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, noExternal, costRecorded, energyRecorded,
    dropoutRecorded, receiptPlanned, missingResidualOwner]

theorem hive_support_promotion_requires_evidence_transition
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = false ->
    review.costBudgetRecorded = true ->
    review.energyBudgetRecorded = true ->
    review.dropoutPlanRecorded = true ->
    review.auditReceiptPlanned = true ->
    review.residualOwnerRecorded = true ->
    review.supportPromotionRequested = true ->
    review.evidenceTransitionRecorded = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.requireEvidenceTransition := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk noExternal costRecorded energyRecorded
    dropoutRecorded receiptPlanned residualOwner promotionRequested
    missingTransition
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, noExternal, costRecorded, energyRecorded,
    dropoutRecorded, receiptPlanned, residualOwner, promotionRequested,
    missingTransition]

theorem complete_hive_work_admission_review_admits
    {review : HiveWorkAdmissionReview} :
    review.jobWellFormed = true ->
    review.identityPolicyPassed = true ->
    review.dataPolicyPassed = true ->
    review.toolPolicyPassed = true ->
    review.deviceRegistryReady = true ->
    review.schedulerPolicyPassed = true ->
    review.highRiskJob = false ->
    review.externalHiveAccessRequested = false ->
    review.costBudgetRecorded = true ->
    review.energyBudgetRecorded = true ->
    review.dropoutPlanRecorded = true ->
    review.auditReceiptPlanned = true ->
    review.residualOwnerRecorded = true ->
    review.supportPromotionRequested = false ->
    HiveWorkAdmissionRouteFor review =
      HiveWorkAdmissionRoute.admitHiveWork := by
  intro wellFormed identityPassed dataPassed toolPassed registryReady
    schedulerPassed notHighRisk noExternal costRecorded energyRecorded
    dropoutRecorded receiptPlanned residualOwner noPromotion
  unfold HiveWorkAdmissionRouteFor
  simp [wellFormed, identityPassed, dataPassed, toolPassed, registryReady,
    schedulerPassed, notHighRisk, noExternal, costRecorded, energyRecorded,
    dropoutRecorded, receiptPlanned, residualOwner, noPromotion]

inductive PartitionedAuthorityRoute where
  | quarantinePendingSync
  | requestFreshAuthorityReceipt
  | requestNoMutationEvidence
  | preserveNoPromotionBoundary
  | dispatch
deriving DecidableEq, Repr

structure PartitionedAuthorityReview where
  partitionDetected : Bool
  grantSeenAtRequester : Bool
  revocationSeenAtEffectSite : Bool
  staleGrantPossible : Bool
  freshAuthorityReceipt : Bool
  effectAttempted : Bool
  deniedBeforeMutation : Bool
  stateUnchangedAfterDenial : Bool
  residualOwnerRecorded : Bool
  auditRefsRecorded : Bool
  supportStateEffectNone : Bool
  nonClaimsRecorded : Bool
deriving DecidableEq, Repr

def PartitionedAuthorityRouteFor
    (review : PartitionedAuthorityReview) :
    PartitionedAuthorityRoute :=
  if review.partitionDetected = true ∧
      (review.staleGrantPossible = true ∨
        review.revocationSeenAtEffectSite = false) then
    if review.deniedBeforeMutation = true ∧
        review.stateUnchangedAfterDenial = true ∧
          review.residualOwnerRecorded = true then
      PartitionedAuthorityRoute.quarantinePendingSync
    else
      PartitionedAuthorityRoute.requestNoMutationEvidence
  else if review.grantSeenAtRequester = true ∧
      review.freshAuthorityReceipt = false then
    PartitionedAuthorityRoute.requestFreshAuthorityReceipt
  else if review.effectAttempted = true ∧
      review.auditRefsRecorded = false then
    PartitionedAuthorityRoute.requestNoMutationEvidence
  else if review.supportStateEffectNone = false ∨
      review.nonClaimsRecorded = false then
    PartitionedAuthorityRoute.preserveNoPromotionBoundary
  else
    PartitionedAuthorityRoute.dispatch

theorem partitioned_stale_authority_with_no_mutation_quarantines
    {review : PartitionedAuthorityReview} :
    review.partitionDetected = true ->
      review.staleGrantPossible = true ->
        review.deniedBeforeMutation = true ->
          review.stateUnchangedAfterDenial = true ->
            review.residualOwnerRecorded = true ->
              PartitionedAuthorityRouteFor review =
                PartitionedAuthorityRoute.quarantinePendingSync := by
  intro partitionDetected staleGrant denied unchanged residualOwner
  unfold PartitionedAuthorityRouteFor
  simp [partitionDetected, staleGrant, denied, unchanged, residualOwner]

theorem partitioned_stale_authority_without_no_mutation_requests_evidence
    {review : PartitionedAuthorityReview} :
    review.partitionDetected = true ->
      review.staleGrantPossible = true ->
        review.deniedBeforeMutation = false ->
          PartitionedAuthorityRouteFor review =
            PartitionedAuthorityRoute.requestNoMutationEvidence := by
  intro partitionDetected staleGrant missingDenial
  unfold PartitionedAuthorityRouteFor
  simp [partitionDetected, staleGrant, missingDenial]

theorem healed_partition_with_stale_grant_requires_fresh_receipt
    {review : PartitionedAuthorityReview} :
    review.partitionDetected = false ->
      review.grantSeenAtRequester = true ->
        review.freshAuthorityReceipt = false ->
          PartitionedAuthorityRouteFor review =
            PartitionedAuthorityRoute.requestFreshAuthorityReceipt := by
  intro noPartition grantSeen staleReceipt
  unfold PartitionedAuthorityRouteFor
  simp [noPartition, grantSeen, staleReceipt]

structure PartitionedAuthorityFixtureSummary where
  partitionRevocationQuarantined : Bool
  healedPartitionRequiresFreshReceipt : Bool
  freshReceiptDispatchBounded : Bool
  staleGrantDispatchRejected : Bool
  grantEffectRaceRejected : Bool
  mutationWithoutNoMutationEvidenceRejected : Bool
  residualOwnerRequired : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
  deployedPartitionToleranceNotClaimed : Bool
deriving DecidableEq, Repr

def partitionedAuthorityFixtureSummary :
    PartitionedAuthorityFixtureSummary where
  partitionRevocationQuarantined := true
  healedPartitionRequiresFreshReceipt := true
  freshReceiptDispatchBounded := true
  staleGrantDispatchRejected := true
  grantEffectRaceRejected := true
  mutationWithoutNoMutationEvidenceRejected := true
  residualOwnerRequired := true
  supportStateEffectNone := true
  nonClaimBoundary := true
  deployedPartitionToleranceNotClaimed := true

def PartitionedAuthorityFixtureValid
    (summary : PartitionedAuthorityFixtureSummary) : Prop :=
  summary.partitionRevocationQuarantined = true ∧
    summary.healedPartitionRequiresFreshReceipt = true ∧
      summary.freshReceiptDispatchBounded = true ∧
        summary.staleGrantDispatchRejected = true ∧
          summary.grantEffectRaceRejected = true ∧
            summary.mutationWithoutNoMutationEvidenceRejected = true ∧
              summary.residualOwnerRequired = true ∧
                summary.supportStateEffectNone = true ∧
                  summary.nonClaimBoundary = true ∧
                    summary.deployedPartitionToleranceNotClaimed = true

theorem partitioned_authority_fixture_bridge :
    PartitionedAuthorityFixtureValid partitionedAuthorityFixtureSummary := by
  unfold PartitionedAuthorityFixtureValid
  unfold partitionedAuthorityFixtureSummary
  simp

end AsiStackProofs.PersonalComputeHives
