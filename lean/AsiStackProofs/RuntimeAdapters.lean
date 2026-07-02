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

inductive RuntimeAdapterRoute where
  | denyMissingPermission
  | requestScopedApproval
  | denyMismatchedLease
  | denyExpiredLease
  | denyUnsandboxedLease
  | denyAuthorityEscalation
  | denyConfusedDeputy
  | denySandboxEscape
  | requestRollbackHandle
  | requestEffectReceipt
  | dispatch
deriving DecidableEq, Repr

structure RuntimeAdapterReview where
  parentPermissionPresent : Bool
  highImpact : Bool
  approvalRecorded : Bool
  approvalScopeMatches : Bool
  leaseCapabilityMatches : Bool
  leaseActive : Bool
  leaseSandboxed : Bool
  requestedAuthorityRank : Nat
  parentAuthorityCeiling : Nat
  leaseAuthorityCeiling : Nat
  confusedDeputyAttempt : Bool
  sandboxEscapeAttempt : Bool
  rollbackRequired : Bool
  rollbackHandleRecorded : Bool
  effectReceiptPlanned : Bool
  auditRefsPlanned : Bool
  nonClaimsPlanned : Bool
deriving DecidableEq, Repr

def RuntimeAdapterRouteFor
    (review : RuntimeAdapterReview) : RuntimeAdapterRoute :=
  if review.parentPermissionPresent = false then
    RuntimeAdapterRoute.denyMissingPermission
  else if review.highImpact = true ∧ review.approvalRecorded = false then
    RuntimeAdapterRoute.requestScopedApproval
  else if review.highImpact = true ∧ review.approvalScopeMatches = false then
    RuntimeAdapterRoute.requestScopedApproval
  else if review.leaseCapabilityMatches = false then
    RuntimeAdapterRoute.denyMismatchedLease
  else if review.leaseActive = false then
    RuntimeAdapterRoute.denyExpiredLease
  else if review.leaseSandboxed = false then
    RuntimeAdapterRoute.denyUnsandboxedLease
  else if review.parentAuthorityCeiling < review.requestedAuthorityRank then
    RuntimeAdapterRoute.denyAuthorityEscalation
  else if review.leaseAuthorityCeiling < review.requestedAuthorityRank then
    RuntimeAdapterRoute.denyAuthorityEscalation
  else if review.confusedDeputyAttempt = true then
    RuntimeAdapterRoute.denyConfusedDeputy
  else if review.sandboxEscapeAttempt = true then
    RuntimeAdapterRoute.denySandboxEscape
  else if review.highImpact = true ∧
      review.rollbackRequired = true ∧
        review.rollbackHandleRecorded = false then
    RuntimeAdapterRoute.requestRollbackHandle
  else if review.effectReceiptPlanned = false ∨
      review.auditRefsPlanned = false ∨
        review.nonClaimsPlanned = false then
    RuntimeAdapterRoute.requestEffectReceipt
  else
    RuntimeAdapterRoute.dispatch

theorem high_impact_without_scoped_approval_routes_to_approval
    {review : RuntimeAdapterReview} :
    review.parentPermissionPresent = true ->
      review.highImpact = true ->
        review.approvalRecorded = true ->
          review.approvalScopeMatches = false ->
            RuntimeAdapterRouteFor review =
              RuntimeAdapterRoute.requestScopedApproval := by
  intro parentPermission highImpact approvalRecorded scopeMismatch
  unfold RuntimeAdapterRouteFor
  simp [parentPermission, highImpact, approvalRecorded, scopeMismatch]

theorem parent_authority_ceiling_blocks_adapter_dispatch
    {review : RuntimeAdapterReview} :
    review.parentPermissionPresent = true ->
      review.highImpact = false ->
        review.leaseCapabilityMatches = true ->
          review.leaseActive = true ->
            review.leaseSandboxed = true ->
              review.parentAuthorityCeiling < review.requestedAuthorityRank ->
                RuntimeAdapterRouteFor review =
                  RuntimeAdapterRoute.denyAuthorityEscalation := by
  intro parentPermission lowImpact leaseMatches leaseActive leaseSandboxed
    overParentCeiling
  unfold RuntimeAdapterRouteFor
  simp [parentPermission, lowImpact, leaseMatches, leaseActive, leaseSandboxed,
    overParentCeiling]

theorem lease_authority_ceiling_blocks_adapter_dispatch
    {review : RuntimeAdapterReview} :
    review.parentPermissionPresent = true ->
      review.highImpact = false ->
        review.leaseCapabilityMatches = true ->
          review.leaseActive = true ->
            review.leaseSandboxed = true ->
              review.requestedAuthorityRank <= review.parentAuthorityCeiling ->
                review.leaseAuthorityCeiling < review.requestedAuthorityRank ->
                  RuntimeAdapterRouteFor review =
                    RuntimeAdapterRoute.denyAuthorityEscalation := by
  intro parentPermission lowImpact leaseMatches leaseActive leaseSandboxed
    withinParentCeiling overLeaseCeiling
  unfold RuntimeAdapterRouteFor
  simp [parentPermission, lowImpact, leaseMatches, leaseActive, leaseSandboxed,
    Nat.not_lt_of_ge withinParentCeiling, overLeaseCeiling]

theorem confused_deputy_attempt_rejected_by_adapter_route
    {review : RuntimeAdapterReview} :
    review.parentPermissionPresent = true ->
      review.highImpact = false ->
        review.leaseCapabilityMatches = true ->
          review.leaseActive = true ->
            review.leaseSandboxed = true ->
              review.requestedAuthorityRank <= review.parentAuthorityCeiling ->
                review.requestedAuthorityRank <= review.leaseAuthorityCeiling ->
                  review.confusedDeputyAttempt = true ->
                    RuntimeAdapterRouteFor review =
                      RuntimeAdapterRoute.denyConfusedDeputy := by
  intro parentPermission lowImpact leaseMatches leaseActive leaseSandboxed
    withinParentCeiling withinLeaseCeiling confusedDeputy
  unfold RuntimeAdapterRouteFor
  simp [parentPermission, lowImpact, leaseMatches, leaseActive, leaseSandboxed,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, confusedDeputy]

theorem sandbox_escape_attempt_rejected_by_adapter_route
    {review : RuntimeAdapterReview} :
    review.parentPermissionPresent = true ->
      review.highImpact = false ->
        review.leaseCapabilityMatches = true ->
          review.leaseActive = true ->
            review.leaseSandboxed = true ->
              review.requestedAuthorityRank <= review.parentAuthorityCeiling ->
                review.requestedAuthorityRank <= review.leaseAuthorityCeiling ->
                  review.confusedDeputyAttempt = false ->
                    review.sandboxEscapeAttempt = true ->
                      RuntimeAdapterRouteFor review =
                        RuntimeAdapterRoute.denySandboxEscape := by
  intro parentPermission lowImpact leaseMatches leaseActive leaseSandboxed
    withinParentCeiling withinLeaseCeiling noConfusedDeputy sandboxEscape
  unfold RuntimeAdapterRouteFor
  simp [parentPermission, lowImpact, leaseMatches, leaseActive, leaseSandboxed,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, noConfusedDeputy, sandboxEscape]

theorem missing_effect_receipt_blocks_adapter_dispatch
    {review : RuntimeAdapterReview} :
    review.parentPermissionPresent = true ->
      review.highImpact = false ->
        review.leaseCapabilityMatches = true ->
          review.leaseActive = true ->
            review.leaseSandboxed = true ->
              review.requestedAuthorityRank <= review.parentAuthorityCeiling ->
                review.requestedAuthorityRank <= review.leaseAuthorityCeiling ->
                  review.confusedDeputyAttempt = false ->
                    review.sandboxEscapeAttempt = false ->
                      review.effectReceiptPlanned = false ->
                        RuntimeAdapterRouteFor review =
                          RuntimeAdapterRoute.requestEffectReceipt := by
  intro parentPermission lowImpact leaseMatches leaseActive leaseSandboxed
    withinParentCeiling withinLeaseCeiling noConfusedDeputy noSandboxEscape
    missingReceipt
  unfold RuntimeAdapterRouteFor
  simp [parentPermission, lowImpact, leaseMatches, leaseActive, leaseSandboxed,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, noConfusedDeputy, noSandboxEscape,
    missingReceipt]

theorem complete_runtime_adapter_review_dispatches
    {review : RuntimeAdapterReview} :
    review.parentPermissionPresent = true ->
      review.highImpact = false ->
        review.leaseCapabilityMatches = true ->
          review.leaseActive = true ->
            review.leaseSandboxed = true ->
              review.requestedAuthorityRank <= review.parentAuthorityCeiling ->
                review.requestedAuthorityRank <= review.leaseAuthorityCeiling ->
                  review.confusedDeputyAttempt = false ->
                    review.sandboxEscapeAttempt = false ->
                      review.rollbackRequired = false ->
                        review.effectReceiptPlanned = true ->
                          review.auditRefsPlanned = true ->
                            review.nonClaimsPlanned = true ->
                              RuntimeAdapterRouteFor review =
                                RuntimeAdapterRoute.dispatch := by
  intro parentPermission lowImpact leaseMatches leaseActive leaseSandboxed
    withinParentCeiling withinLeaseCeiling noConfusedDeputy noSandboxEscape
    noRollbackRequired effectReceipt auditRefs nonClaims
  unfold RuntimeAdapterRouteFor
  simp [parentPermission, lowImpact, leaseMatches, leaseActive, leaseSandboxed,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, noConfusedDeputy, noSandboxEscape,
    noRollbackRequired, effectReceipt, auditRefs, nonClaims]

inductive RuntimeEffectReplayRoute where
  | denyMissingPermission
  | denyExpiredApproval
  | requestNoMutationEvidence
  | requestRollbackEvidence
  | requestEffectReceipt
  | preserveNoPromotionBoundary
  | acceptReplay
deriving DecidableEq, Repr

structure RuntimeEffectReplayReview where
  parentPermissionPresent : Bool
  approvalActive : Bool
  effectExecuted : Bool
  deniedBeforeMutation : Bool
  stateUnchangedAfterDenial : Bool
  preStateRecorded : Bool
  postStateRecorded : Bool
  rollbackRequired : Bool
  rollbackExecuted : Bool
  rollbackExact : Bool
  effectReceiptRecorded : Bool
  auditRefsRecorded : Bool
  supportStateEffectNone : Bool
  repoWrite : Bool
  networkUsed : Bool
deriving DecidableEq, Repr

def RuntimeEffectReplayRouteFor
    (review : RuntimeEffectReplayReview) : RuntimeEffectReplayRoute :=
  if review.parentPermissionPresent = false then
    if review.deniedBeforeMutation = true ∧
        review.stateUnchangedAfterDenial = true then
      RuntimeEffectReplayRoute.denyMissingPermission
    else
      RuntimeEffectReplayRoute.requestNoMutationEvidence
  else if review.approvalActive = false then
    if review.deniedBeforeMutation = true ∧
        review.stateUnchangedAfterDenial = true then
      RuntimeEffectReplayRoute.denyExpiredApproval
    else
      RuntimeEffectReplayRoute.requestNoMutationEvidence
  else if review.effectExecuted = true ∧
      (review.preStateRecorded = false ∨ review.postStateRecorded = false) then
    RuntimeEffectReplayRoute.requestEffectReceipt
  else if review.rollbackRequired = true ∧
      (review.rollbackExecuted = false ∨ review.rollbackExact = false) then
    RuntimeEffectReplayRoute.requestRollbackEvidence
  else if review.effectReceiptRecorded = false ∨
      review.auditRefsRecorded = false then
    RuntimeEffectReplayRoute.requestEffectReceipt
  else if review.supportStateEffectNone = false ∨
      review.repoWrite = true ∨
        review.networkUsed = true then
    RuntimeEffectReplayRoute.preserveNoPromotionBoundary
  else
    RuntimeEffectReplayRoute.acceptReplay

theorem missing_permission_no_mutation_denies_before_effect
    {review : RuntimeEffectReplayReview} :
    review.parentPermissionPresent = false ->
      review.deniedBeforeMutation = true ->
        review.stateUnchangedAfterDenial = true ->
          RuntimeEffectReplayRouteFor review =
            RuntimeEffectReplayRoute.denyMissingPermission := by
  intro missingPermission deniedBeforeMutation unchanged
  unfold RuntimeEffectReplayRouteFor
  simp [missingPermission, deniedBeforeMutation, unchanged]

theorem missing_permission_without_no_mutation_evidence_requests_evidence
    {review : RuntimeEffectReplayReview} :
    review.parentPermissionPresent = false ->
      review.deniedBeforeMutation = false ->
        RuntimeEffectReplayRouteFor review =
          RuntimeEffectReplayRoute.requestNoMutationEvidence := by
  intro missingPermission noDenialEvidence
  unfold RuntimeEffectReplayRouteFor
  simp [missingPermission, noDenialEvidence]

theorem expired_approval_no_mutation_denies_before_effect
    {review : RuntimeEffectReplayReview} :
    review.parentPermissionPresent = true ->
      review.approvalActive = false ->
        review.deniedBeforeMutation = true ->
          review.stateUnchangedAfterDenial = true ->
            RuntimeEffectReplayRouteFor review =
              RuntimeEffectReplayRoute.denyExpiredApproval := by
  intro permissionPresent expiredApproval deniedBeforeMutation unchanged
  unfold RuntimeEffectReplayRouteFor
  simp [permissionPresent, expiredApproval, deniedBeforeMutation, unchanged]

theorem rollback_required_without_exact_rollback_requests_rollback_evidence
    {review : RuntimeEffectReplayReview} :
    review.parentPermissionPresent = true ->
      review.approvalActive = true ->
        review.effectExecuted = true ->
          review.preStateRecorded = true ->
            review.postStateRecorded = true ->
              review.rollbackRequired = true ->
                review.rollbackExecuted = true ->
                  review.rollbackExact = false ->
                    RuntimeEffectReplayRouteFor review =
                      RuntimeEffectReplayRoute.requestRollbackEvidence := by
  intro permissionPresent approvalActive effectExecuted preRecorded postRecorded
    rollbackRequired rollbackExecuted rollbackInexact
  unfold RuntimeEffectReplayRouteFor
  simp [permissionPresent, approvalActive, effectExecuted, preRecorded,
    postRecorded, rollbackRequired, rollbackExecuted, rollbackInexact]

theorem missing_effect_receipt_requests_effect_receipt
    {review : RuntimeEffectReplayReview} :
    review.parentPermissionPresent = true ->
      review.approvalActive = true ->
        review.effectExecuted = true ->
          review.preStateRecorded = true ->
            review.postStateRecorded = true ->
              review.rollbackRequired = false ->
                review.effectReceiptRecorded = false ->
                  RuntimeEffectReplayRouteFor review =
                    RuntimeEffectReplayRoute.requestEffectReceipt := by
  intro permissionPresent approvalActive effectExecuted preRecorded postRecorded
    noRollbackRequired missingReceipt
  unfold RuntimeEffectReplayRouteFor
  simp [permissionPresent, approvalActive, effectExecuted, preRecorded,
    postRecorded, noRollbackRequired, missingReceipt]

theorem support_effect_or_repo_write_preserves_no_promotion_boundary
    {review : RuntimeEffectReplayReview} :
    review.parentPermissionPresent = true ->
      review.approvalActive = true ->
        review.effectExecuted = true ->
          review.preStateRecorded = true ->
            review.postStateRecorded = true ->
              review.rollbackRequired = false ->
                review.effectReceiptRecorded = true ->
                  review.auditRefsRecorded = true ->
                    review.supportStateEffectNone = false ->
                      RuntimeEffectReplayRouteFor review =
                        RuntimeEffectReplayRoute.preserveNoPromotionBoundary := by
  intro permissionPresent approvalActive effectExecuted preRecorded postRecorded
    noRollbackRequired receiptRecorded auditRefs supportPromoting
  unfold RuntimeEffectReplayRouteFor
  simp [permissionPresent, approvalActive, effectExecuted, preRecorded,
    postRecorded, noRollbackRequired, receiptRecorded, auditRefs, supportPromoting]

theorem complete_runtime_effect_replay_accepts
    {review : RuntimeEffectReplayReview} :
    review.parentPermissionPresent = true ->
      review.approvalActive = true ->
        review.effectExecuted = true ->
          review.preStateRecorded = true ->
            review.postStateRecorded = true ->
              review.rollbackRequired = true ->
                review.rollbackExecuted = true ->
                  review.rollbackExact = true ->
                    review.effectReceiptRecorded = true ->
                      review.auditRefsRecorded = true ->
                        review.supportStateEffectNone = true ->
                          review.repoWrite = false ->
                            review.networkUsed = false ->
                              RuntimeEffectReplayRouteFor review =
                                RuntimeEffectReplayRoute.acceptReplay := by
  intro permissionPresent approvalActive effectExecuted preRecorded postRecorded
    rollbackRequired rollbackExecuted rollbackExact receiptRecorded auditRefs
    supportNone noRepoWrite noNetwork
  unfold RuntimeEffectReplayRouteFor
  simp [permissionPresent, approvalActive, effectExecuted, preRecorded,
    postRecorded, rollbackRequired, rollbackExecuted, rollbackExact,
    receiptRecorded, auditRefs, supportNone, noRepoWrite, noNetwork]

inductive RuntimeAdapterAdversarialRoute where
  | denyConfusedDeputy
  | denyMissingPermission
  | requestScopedApproval
  | denyExpiredApproval
  | denyMismatchedLease
  | denyExpiredLease
  | denyAuthorityEscalation
  | denySandboxEscape
  | denySecretExposure
  | requestRollbackHandle
  | requestEffectReceipt
  | preserveNoPromotionBoundary
  | requestNonClaimBoundary
  | dispatch
deriving DecidableEq, Repr

structure RuntimeAdapterAdversarialReview where
  parentMatchesApproval : Bool
  parentMatchesLease : Bool
  parentMatchesReceipt : Bool
  parentPermissionPresent : Bool
  highImpact : Bool
  approvalRequired : Bool
  approvalRecorded : Bool
  approvalScopeMatches : Bool
  approvalActive : Bool
  leaseCapabilityMatches : Bool
  leaseActive : Bool
  leaseSandboxed : Bool
  sandboxPathWithinBoundary : Bool
  requestedAuthorityRank : Nat
  parentAuthorityCeiling : Nat
  leaseAuthorityCeiling : Nat
  secretMaterializedToModelContext : Bool
  rollbackRequired : Bool
  rollbackHandleRecorded : Bool
  effectReceiptRecorded : Bool
  auditRefsRecorded : Bool
  supportStateEffectNone : Bool
  nonClaimsRecorded : Bool
deriving DecidableEq, Repr

def RuntimeAdapterAdversarialRouteFor
    (review : RuntimeAdapterAdversarialReview) :
    RuntimeAdapterAdversarialRoute :=
  if review.parentMatchesApproval = false ∨
      review.parentMatchesLease = false ∨
        review.parentMatchesReceipt = false then
    RuntimeAdapterAdversarialRoute.denyConfusedDeputy
  else if review.parentPermissionPresent = false then
    RuntimeAdapterAdversarialRoute.denyMissingPermission
  else if (review.approvalRequired = true ∨ review.highImpact = true) ∧
      (review.approvalRecorded = false ∨
        review.approvalScopeMatches = false) then
    RuntimeAdapterAdversarialRoute.requestScopedApproval
  else if review.approvalRequired = true ∧
      review.approvalActive = false then
    RuntimeAdapterAdversarialRoute.denyExpiredApproval
  else if review.leaseCapabilityMatches = false then
    RuntimeAdapterAdversarialRoute.denyMismatchedLease
  else if review.leaseActive = false then
    RuntimeAdapterAdversarialRoute.denyExpiredLease
  else if review.parentAuthorityCeiling < review.requestedAuthorityRank then
    RuntimeAdapterAdversarialRoute.denyAuthorityEscalation
  else if review.leaseAuthorityCeiling < review.requestedAuthorityRank then
    RuntimeAdapterAdversarialRoute.denyAuthorityEscalation
  else if review.leaseSandboxed = false ∨
      review.sandboxPathWithinBoundary = false then
    RuntimeAdapterAdversarialRoute.denySandboxEscape
  else if review.secretMaterializedToModelContext = true then
    RuntimeAdapterAdversarialRoute.denySecretExposure
  else if review.rollbackRequired = true ∧
      review.rollbackHandleRecorded = false then
    RuntimeAdapterAdversarialRoute.requestRollbackHandle
  else if review.effectReceiptRecorded = false ∨
      review.auditRefsRecorded = false then
    RuntimeAdapterAdversarialRoute.requestEffectReceipt
  else if review.supportStateEffectNone = false then
    RuntimeAdapterAdversarialRoute.preserveNoPromotionBoundary
  else if review.nonClaimsRecorded = false then
    RuntimeAdapterAdversarialRoute.requestNonClaimBoundary
  else
    RuntimeAdapterAdversarialRoute.dispatch

theorem adapter_adversarial_confused_deputy_parent_mismatch_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = false ->
      RuntimeAdapterAdversarialRouteFor review =
        RuntimeAdapterAdversarialRoute.denyConfusedDeputy := by
  intro parentMismatch
  unfold RuntimeAdapterAdversarialRouteFor
  simp [parentMismatch]

theorem adapter_adversarial_missing_permission_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = false ->
            RuntimeAdapterAdversarialRouteFor review =
              RuntimeAdapterAdversarialRoute.denyMissingPermission := by
  intro approvalParent leaseParent receiptParent missingPermission
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, missingPermission]

theorem adapter_adversarial_parent_authority_ceiling_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.parentAuthorityCeiling <
                      review.requestedAuthorityRank ->
                      RuntimeAdapterAdversarialRouteFor review =
                        RuntimeAdapterAdversarialRoute.denyAuthorityEscalation := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive overParentCeiling
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive, overParentCeiling]

theorem adapter_adversarial_lease_authority_ceiling_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.requestedAuthorityRank <=
                      review.parentAuthorityCeiling ->
                      review.leaseAuthorityCeiling <
                        review.requestedAuthorityRank ->
                        RuntimeAdapterAdversarialRouteFor review =
                          RuntimeAdapterAdversarialRoute.denyAuthorityEscalation := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive withinParentCeiling
    overLeaseCeiling
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling, overLeaseCeiling]

theorem adapter_adversarial_scoped_approval_mismatch_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = true ->
              review.approvalRecorded = true ->
                review.approvalScopeMatches = false ->
                  RuntimeAdapterAdversarialRouteFor review =
                    RuntimeAdapterAdversarialRoute.requestScopedApproval := by
  intro approvalParent leaseParent receiptParent permissionPresent
    approvalRequired approvalRecorded scopeMismatch
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    approvalRequired, approvalRecorded, scopeMismatch]

theorem adapter_adversarial_expired_approval_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = true ->
              review.approvalRecorded = true ->
                review.approvalScopeMatches = true ->
                  review.approvalActive = false ->
                    RuntimeAdapterAdversarialRouteFor review =
                      RuntimeAdapterAdversarialRoute.denyExpiredApproval := by
  intro approvalParent leaseParent receiptParent permissionPresent
    approvalRequired approvalRecorded scopeMatches expiredApproval
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    approvalRequired, approvalRecorded, scopeMatches, expiredApproval]

theorem adapter_adversarial_sandbox_escape_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.requestedAuthorityRank <=
                      review.parentAuthorityCeiling ->
                      review.requestedAuthorityRank <=
                        review.leaseAuthorityCeiling ->
                        review.leaseSandboxed = true ->
                          review.sandboxPathWithinBoundary = false ->
                            RuntimeAdapterAdversarialRouteFor review =
                              RuntimeAdapterAdversarialRoute.denySandboxEscape := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive withinParentCeiling
    withinLeaseCeiling sandboxed sandboxEscape
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxEscape]

theorem adapter_adversarial_secret_materialization_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.requestedAuthorityRank <=
                      review.parentAuthorityCeiling ->
                      review.requestedAuthorityRank <=
                        review.leaseAuthorityCeiling ->
                        review.leaseSandboxed = true ->
                          review.sandboxPathWithinBoundary = true ->
                            review.secretMaterializedToModelContext = true ->
                              RuntimeAdapterAdversarialRouteFor review =
                                RuntimeAdapterAdversarialRoute.denySecretExposure := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive withinParentCeiling
    withinLeaseCeiling sandboxed sandboxPath secretMaterialized
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxPath,
    secretMaterialized]

theorem adapter_adversarial_missing_rollback_handle_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = true ->
              review.approvalRecorded = true ->
                review.approvalScopeMatches = true ->
                  review.approvalActive = true ->
                    review.leaseCapabilityMatches = true ->
                      review.leaseActive = true ->
                        review.requestedAuthorityRank <=
                          review.parentAuthorityCeiling ->
                          review.requestedAuthorityRank <=
                            review.leaseAuthorityCeiling ->
                            review.leaseSandboxed = true ->
                              review.sandboxPathWithinBoundary = true ->
                                review.secretMaterializedToModelContext = false ->
                                  review.rollbackRequired = true ->
                                    review.rollbackHandleRecorded = false ->
                                      RuntimeAdapterAdversarialRouteFor review =
                                        RuntimeAdapterAdversarialRoute.requestRollbackHandle := by
  intro approvalParent leaseParent receiptParent permissionPresent
    approvalRequired approvalRecorded scopeMatches approvalActive leaseMatches
    leaseActive withinParentCeiling withinLeaseCeiling sandboxed sandboxPath
    noSecret rollbackRequired missingRollback
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    approvalRequired, approvalRecorded, scopeMatches, approvalActive,
    leaseMatches, leaseActive, Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxPath, noSecret,
    rollbackRequired, missingRollback]

theorem adapter_adversarial_missing_effect_receipt_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.requestedAuthorityRank <=
                      review.parentAuthorityCeiling ->
                      review.requestedAuthorityRank <=
                        review.leaseAuthorityCeiling ->
                        review.leaseSandboxed = true ->
                          review.sandboxPathWithinBoundary = true ->
                            review.secretMaterializedToModelContext = false ->
                              review.rollbackRequired = false ->
                                review.effectReceiptRecorded = false ->
                                  RuntimeAdapterAdversarialRouteFor review =
                                    RuntimeAdapterAdversarialRoute.requestEffectReceipt := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive withinParentCeiling
    withinLeaseCeiling sandboxed sandboxPath noSecret noRollback
    missingReceipt
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxPath, noSecret,
    noRollback, missingReceipt]

theorem adapter_adversarial_missing_audit_refs_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.requestedAuthorityRank <=
                      review.parentAuthorityCeiling ->
                      review.requestedAuthorityRank <=
                        review.leaseAuthorityCeiling ->
                        review.leaseSandboxed = true ->
                          review.sandboxPathWithinBoundary = true ->
                            review.secretMaterializedToModelContext = false ->
                              review.rollbackRequired = false ->
                                review.effectReceiptRecorded = true ->
                                  review.auditRefsRecorded = false ->
                                    RuntimeAdapterAdversarialRouteFor review =
                                      RuntimeAdapterAdversarialRoute.requestEffectReceipt := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive withinParentCeiling
    withinLeaseCeiling sandboxed sandboxPath noSecret noRollback receipt
    missingAudit
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxPath, noSecret,
    noRollback, receipt, missingAudit]

theorem adapter_adversarial_support_promotion_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.requestedAuthorityRank <=
                      review.parentAuthorityCeiling ->
                      review.requestedAuthorityRank <=
                        review.leaseAuthorityCeiling ->
                        review.leaseSandboxed = true ->
                          review.sandboxPathWithinBoundary = true ->
                            review.secretMaterializedToModelContext = false ->
                              review.rollbackRequired = false ->
                                review.effectReceiptRecorded = true ->
                                  review.auditRefsRecorded = true ->
                                    review.supportStateEffectNone = false ->
                                      RuntimeAdapterAdversarialRouteFor review =
                                        RuntimeAdapterAdversarialRoute.preserveNoPromotionBoundary := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive withinParentCeiling
    withinLeaseCeiling sandboxed sandboxPath noSecret noRollback receipt audit
    supportPromoting
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxPath, noSecret,
    noRollback, receipt, audit, supportPromoting]

theorem adapter_adversarial_missing_non_claim_boundary_rejected
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.requestedAuthorityRank <=
                      review.parentAuthorityCeiling ->
                      review.requestedAuthorityRank <=
                        review.leaseAuthorityCeiling ->
                        review.leaseSandboxed = true ->
                          review.sandboxPathWithinBoundary = true ->
                            review.secretMaterializedToModelContext = false ->
                              review.rollbackRequired = false ->
                                review.effectReceiptRecorded = true ->
                                  review.auditRefsRecorded = true ->
                                    review.supportStateEffectNone = true ->
                                      review.nonClaimsRecorded = false ->
                                        RuntimeAdapterAdversarialRouteFor review =
                                          RuntimeAdapterAdversarialRoute.requestNonClaimBoundary := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive withinParentCeiling
    withinLeaseCeiling sandboxed sandboxPath noSecret noRollback receipt audit
    supportNone missingNonClaims
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxPath, noSecret,
    noRollback, receipt, audit, supportNone, missingNonClaims]

theorem adapter_adversarial_low_impact_dispatch_accepted
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = false ->
              review.highImpact = false ->
                review.leaseCapabilityMatches = true ->
                  review.leaseActive = true ->
                    review.requestedAuthorityRank <=
                      review.parentAuthorityCeiling ->
                      review.requestedAuthorityRank <=
                        review.leaseAuthorityCeiling ->
                        review.leaseSandboxed = true ->
                          review.sandboxPathWithinBoundary = true ->
                            review.secretMaterializedToModelContext = false ->
                              review.rollbackRequired = true ->
                                review.rollbackHandleRecorded = true ->
                                  review.effectReceiptRecorded = true ->
                                    review.auditRefsRecorded = true ->
                                      review.supportStateEffectNone = true ->
                                        review.nonClaimsRecorded = true ->
                                          RuntimeAdapterAdversarialRouteFor review =
                                            RuntimeAdapterAdversarialRoute.dispatch := by
  intro approvalParent leaseParent receiptParent permissionPresent
    noApprovalRequired lowImpact leaseMatches leaseActive withinParentCeiling
    withinLeaseCeiling sandboxed sandboxPath noSecret rollbackRequired
    rollbackHandle receipt audit supportNone nonClaims
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    noApprovalRequired, lowImpact, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxPath, noSecret,
    rollbackRequired, rollbackHandle, receipt, audit, supportNone, nonClaims]

theorem adapter_adversarial_high_impact_dispatch_accepted
    {review : RuntimeAdapterAdversarialReview} :
    review.parentMatchesApproval = true ->
      review.parentMatchesLease = true ->
        review.parentMatchesReceipt = true ->
          review.parentPermissionPresent = true ->
            review.approvalRequired = true ->
              review.highImpact = true ->
                review.approvalRecorded = true ->
                  review.approvalScopeMatches = true ->
                    review.approvalActive = true ->
                      review.leaseCapabilityMatches = true ->
                        review.leaseActive = true ->
                          review.requestedAuthorityRank <=
                            review.parentAuthorityCeiling ->
                            review.requestedAuthorityRank <=
                              review.leaseAuthorityCeiling ->
                              review.leaseSandboxed = true ->
                                review.sandboxPathWithinBoundary = true ->
                                  review.secretMaterializedToModelContext = false ->
                                    review.rollbackRequired = true ->
                                      review.rollbackHandleRecorded = true ->
                                        review.effectReceiptRecorded = true ->
                                          review.auditRefsRecorded = true ->
                                            review.supportStateEffectNone = true ->
                                              review.nonClaimsRecorded = true ->
                                                RuntimeAdapterAdversarialRouteFor review =
                                                  RuntimeAdapterAdversarialRoute.dispatch := by
  intro approvalParent leaseParent receiptParent permissionPresent
    approvalRequired highImpact approvalRecorded scopeMatches approvalActive
    leaseMatches leaseActive withinParentCeiling withinLeaseCeiling sandboxed
    sandboxPath noSecret rollbackRequired rollbackHandle receipt audit
    supportNone nonClaims
  unfold RuntimeAdapterAdversarialRouteFor
  simp [approvalParent, leaseParent, receiptParent, permissionPresent,
    approvalRequired, highImpact, approvalRecorded, scopeMatches,
    approvalActive, leaseMatches, leaseActive,
    Nat.not_lt_of_ge withinParentCeiling,
    Nat.not_lt_of_ge withinLeaseCeiling, sandboxed, sandboxPath, noSecret,
    rollbackRequired, rollbackHandle, receipt, audit, supportNone, nonClaims]

structure RuntimeAdapterAdversarialProbeFixture where
  lowImpactDispatchAccepted : Bool
  highImpactDispatchAccepted : Bool
  negativeControlsRejected : Bool
  authorityAndApprovalBoundaries : Bool
  secretAndSandboxBoundaries : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def RuntimeAdapterAdversarialProbeFixtureValid
    (fixture : RuntimeAdapterAdversarialProbeFixture) : Prop :=
  fixture.lowImpactDispatchAccepted = true ∧
    fixture.highImpactDispatchAccepted = true ∧
      fixture.negativeControlsRejected = true ∧
        fixture.authorityAndApprovalBoundaries = true ∧
          fixture.secretAndSandboxBoundaries = true ∧
            fixture.supportStateEffectNone = true ∧
              fixture.nonClaimBoundary = true

theorem runtime_adapter_adversarial_boundary_probe_bridge
    {fixture : RuntimeAdapterAdversarialProbeFixture} :
    RuntimeAdapterAdversarialProbeFixtureValid fixture ->
      fixture.lowImpactDispatchAccepted = true ∧
        fixture.highImpactDispatchAccepted = true ∧
          fixture.negativeControlsRejected = true ∧
            fixture.authorityAndApprovalBoundaries = true ∧
              fixture.secretAndSandboxBoundaries = true ∧
                fixture.supportStateEffectNone = true ∧
                  fixture.nonClaimBoundary = true := by
  intro valid
  exact valid

end AsiStackProofs.RuntimeAdapters
