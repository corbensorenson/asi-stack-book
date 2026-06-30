namespace AsiStackProofs.RuntimeAdapters

structure ParentJob where
  permissions : List String
deriving DecidableEq, Repr

structure AdapterInvocation where
  capability : String
  highImpact : Bool
  approvalRecorded : Bool
  rejected : Bool
deriving DecidableEq, Repr

def PermissionIncluded
    (job : ParentJob) (invocation : AdapterInvocation) : Prop :=
  invocation.capability ∈ job.permissions

def InvocationPermissionValid
    (job : ParentJob) (invocation : AdapterInvocation) : Prop :=
  PermissionIncluded job invocation

theorem valid_invocation_has_required_permission
    {job : ParentJob} {invocation : AdapterInvocation} :
    InvocationPermissionValid job invocation ->
    invocation.capability ∈ job.permissions := by
  intro valid
  exact valid

theorem invocation_without_parent_permission_rejected
    {job : ParentJob} {invocation : AdapterInvocation} :
    invocation.capability ∉ job.permissions ->
      ¬ InvocationPermissionValid job invocation := by
  intro missingPermission valid
  unfold InvocationPermissionValid at valid
  unfold PermissionIncluded at valid
  contradiction

def ApprovalRejectionValid (invocation : AdapterInvocation) : Prop :=
  invocation.highImpact = true ->
    invocation.approvalRecorded = false ->
      invocation.rejected = true

theorem high_impact_adapter_without_approval_is_rejected
    {invocation : AdapterInvocation} :
    ApprovalRejectionValid invocation ->
    invocation.highImpact = true ->
    invocation.approvalRecorded = false ->
    invocation.rejected = true := by
  intro valid highImpact missingApproval
  exact valid highImpact missingApproval

theorem high_impact_adapter_without_approval_cannot_be_unrejected
    {invocation : AdapterInvocation} :
    invocation.highImpact = true ->
      invocation.approvalRecorded = false ->
        invocation.rejected = false ->
          ¬ ApprovalRejectionValid invocation := by
  intro highImpact missingApproval notRejected valid
  have rejected :=
    high_impact_adapter_without_approval_is_rejected
      valid highImpact missingApproval
  rw [notRejected] at rejected
  contradiction

end AsiStackProofs.RuntimeAdapters
