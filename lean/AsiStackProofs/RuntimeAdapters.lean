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

structure EffectLease where
  capability : String
  active : Bool
  sandboxed : Bool
  rollbackRequired : Bool
  rollbackHandleRecorded : Bool
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

def LeaseScopesInvocation
    (lease : EffectLease) (invocation : AdapterInvocation) : Prop :=
  lease.capability = invocation.capability ∧
    lease.active = true ∧
      lease.sandboxed = true

def LeasedInvocationValid
    (job : ParentJob)
    (invocation : AdapterInvocation)
    (lease : EffectLease) : Prop :=
  InvocationPermissionValid job invocation ∧
    LeaseScopesInvocation lease invocation

theorem valid_leased_invocation_has_active_scoped_sandbox
    {job : ParentJob}
    {invocation : AdapterInvocation}
    {lease : EffectLease} :
    LeasedInvocationValid job invocation lease ->
      lease.capability = invocation.capability ∧
        lease.active = true ∧
          lease.sandboxed = true := by
  intro valid
  exact valid.right

theorem mismatched_effect_lease_rejected
    {job : ParentJob}
    {invocation : AdapterInvocation}
    {lease : EffectLease} :
    lease.capability ≠ invocation.capability ->
      ¬ LeasedInvocationValid job invocation lease := by
  intro mismatch valid
  have scope := valid_leased_invocation_has_active_scoped_sandbox valid
  exact mismatch scope.left

theorem expired_effect_lease_rejected
    {job : ParentJob}
    {invocation : AdapterInvocation}
    {lease : EffectLease} :
    lease.active = false ->
      ¬ LeasedInvocationValid job invocation lease := by
  intro expired valid
  have scope := valid_leased_invocation_has_active_scoped_sandbox valid
  have activeTrue := scope.right.left
  rw [expired] at activeTrue
  cases activeTrue

theorem unsandboxed_effect_lease_rejected
    {job : ParentJob}
    {invocation : AdapterInvocation}
    {lease : EffectLease} :
    lease.sandboxed = false ->
      ¬ LeasedInvocationValid job invocation lease := by
  intro unsandboxed valid
  have scope := valid_leased_invocation_has_active_scoped_sandbox valid
  have sandboxTrue := scope.right.right
  rw [unsandboxed] at sandboxTrue
  cases sandboxTrue

def RollbackObligationValid
    (lease : EffectLease) (invocation : AdapterInvocation) : Prop :=
  invocation.highImpact = true ->
    lease.rollbackRequired = true ->
      lease.rollbackHandleRecorded = false ->
        invocation.rejected = true

theorem high_impact_rollback_required_without_handle_is_rejected
    {lease : EffectLease} {invocation : AdapterInvocation} :
    RollbackObligationValid lease invocation ->
      invocation.highImpact = true ->
        lease.rollbackRequired = true ->
          lease.rollbackHandleRecorded = false ->
            invocation.rejected = true := by
  intro valid highImpact rollbackRequired missingRollbackHandle
  exact valid highImpact rollbackRequired missingRollbackHandle

theorem rollback_required_without_handle_cannot_be_unrejected
    {lease : EffectLease} {invocation : AdapterInvocation} :
    invocation.highImpact = true ->
      lease.rollbackRequired = true ->
        lease.rollbackHandleRecorded = false ->
          invocation.rejected = false ->
            ¬ RollbackObligationValid lease invocation := by
  intro highImpact rollbackRequired missingRollbackHandle notRejected valid
  have rejected :=
    high_impact_rollback_required_without_handle_is_rejected
      valid highImpact rollbackRequired missingRollbackHandle
  rw [notRejected] at rejected
  contradiction

end AsiStackProofs.RuntimeAdapters
