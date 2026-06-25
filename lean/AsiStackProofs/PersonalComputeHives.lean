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

end AsiStackProofs.PersonalComputeHives
