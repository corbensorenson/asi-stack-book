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

end AsiStackProofs.PersonalComputeHives
