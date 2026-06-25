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

end AsiStackProofs.PersonalComputeHives
