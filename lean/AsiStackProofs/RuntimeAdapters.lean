import AsiStackProofs.AuthorityEffectRefinement

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

theorem high_impact_adapter_without_approval_cannot_be_unrejected
    {invocation : AdapterInvocation} :
    invocation.highImpact = true ->
      invocation.approvalRecorded = false ->
        invocation.rejected = false ->
          ¬ ApprovalRejectionValid invocation := by
  intro highImpact missingApproval notRejected valid
  have rejected := valid highImpact missingApproval
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

theorem mismatched_effect_lease_rejected
    {job : ParentJob}
    {invocation : AdapterInvocation}
    {lease : EffectLease} :
    lease.capability ≠ invocation.capability ->
      ¬ LeasedInvocationValid job invocation lease := by
  intro mismatch valid
  have scope := valid.right
  exact mismatch scope.left

theorem expired_effect_lease_rejected
    {job : ParentJob}
    {invocation : AdapterInvocation}
    {lease : EffectLease} :
    lease.active = false ->
      ¬ LeasedInvocationValid job invocation lease := by
  intro expired valid
  have scope := valid.right
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
  have scope := valid.right
  have sandboxTrue := scope.right.right
  rw [unsandboxed] at sandboxTrue
  cases sandboxTrue

def RollbackObligationValid
    (lease : EffectLease) (invocation : AdapterInvocation) : Prop :=
  invocation.highImpact = true ->
    lease.rollbackRequired = true ->
      lease.rollbackHandleRecorded = false ->
        invocation.rejected = true

theorem rollback_required_without_handle_cannot_be_unrejected
    {lease : EffectLease} {invocation : AdapterInvocation} :
    invocation.highImpact = true ->
      lease.rollbackRequired = true ->
        lease.rollbackHandleRecorded = false ->
          invocation.rejected = false ->
            ¬ RollbackObligationValid lease invocation := by
  intro highImpact rollbackRequired missingRollbackHandle notRejected valid
  have rejected := valid highImpact rollbackRequired missingRollbackHandle
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

inductive RuntimeAdapterRevocationRoute where
  | denyMissingPermission
  | denyRevokedApproval
  | denyRevokedLease
  | denyRevokedAuthorityReceipt
  | requestNoMutationEvidence
  | requestEffectReceipt
  | preserveNoPromotionBoundary
  | dispatch
deriving DecidableEq, Repr

structure RuntimeAdapterRevocationReview where
  parentPermissionPresent : Bool
  approvalRecorded : Bool
  approvalActive : Bool
  approvalRevoked : Bool
  leaseActive : Bool
  leaseRevoked : Bool
  authorityReceiptActive : Bool
  authorityReceiptRevoked : Bool
  effectAttempted : Bool
  deniedBeforeMutation : Bool
  stateUnchangedAfterDenial : Bool
  effectReceiptRecorded : Bool
  auditRefsRecorded : Bool
  supportStateEffectNone : Bool
  nonClaimsRecorded : Bool
deriving DecidableEq, Repr

def RuntimeAdapterRevocationRouteFor
    (review : RuntimeAdapterRevocationReview) :
    RuntimeAdapterRevocationRoute :=
  if review.parentPermissionPresent = false then
    RuntimeAdapterRevocationRoute.denyMissingPermission
  else if review.approvalRecorded = true ∧
      (review.approvalActive = false ∨ review.approvalRevoked = true) then
    if review.deniedBeforeMutation = true ∧
        review.stateUnchangedAfterDenial = true then
      RuntimeAdapterRevocationRoute.denyRevokedApproval
    else
      RuntimeAdapterRevocationRoute.requestNoMutationEvidence
  else if review.leaseActive = false ∨ review.leaseRevoked = true then
    if review.deniedBeforeMutation = true ∧
        review.stateUnchangedAfterDenial = true then
      RuntimeAdapterRevocationRoute.denyRevokedLease
    else
      RuntimeAdapterRevocationRoute.requestNoMutationEvidence
  else if review.authorityReceiptActive = false ∨
      review.authorityReceiptRevoked = true then
    if review.deniedBeforeMutation = true ∧
        review.stateUnchangedAfterDenial = true then
      RuntimeAdapterRevocationRoute.denyRevokedAuthorityReceipt
    else
      RuntimeAdapterRevocationRoute.requestNoMutationEvidence
  else if review.effectAttempted = true ∧
      (review.effectReceiptRecorded = false ∨
        review.auditRefsRecorded = false) then
    RuntimeAdapterRevocationRoute.requestEffectReceipt
  else if review.supportStateEffectNone = false ∨
      review.nonClaimsRecorded = false then
    RuntimeAdapterRevocationRoute.preserveNoPromotionBoundary
  else
    RuntimeAdapterRevocationRoute.dispatch

theorem revoked_approval_with_no_mutation_evidence_denies_before_effect
    {review : RuntimeAdapterRevocationReview} :
    review.parentPermissionPresent = true ->
      review.approvalRecorded = true ->
        review.approvalRevoked = true ->
          review.deniedBeforeMutation = true ->
            review.stateUnchangedAfterDenial = true ->
              RuntimeAdapterRevocationRouteFor review =
                RuntimeAdapterRevocationRoute.denyRevokedApproval := by
  intro permissionPresent approvalRecorded approvalRevoked denied unchanged
  unfold RuntimeAdapterRevocationRouteFor
  simp [permissionPresent, approvalRecorded, approvalRevoked, denied,
    unchanged]

theorem revoked_approval_without_no_mutation_evidence_requests_evidence
    {review : RuntimeAdapterRevocationReview} :
    review.parentPermissionPresent = true ->
      review.approvalRecorded = true ->
        review.approvalRevoked = true ->
          review.deniedBeforeMutation = false ->
            RuntimeAdapterRevocationRouteFor review =
              RuntimeAdapterRevocationRoute.requestNoMutationEvidence := by
  intro permissionPresent approvalRecorded approvalRevoked noDenialEvidence
  unfold RuntimeAdapterRevocationRouteFor
  simp [permissionPresent, approvalRecorded, approvalRevoked, noDenialEvidence]

theorem revoked_lease_with_no_mutation_evidence_denies_before_effect
    {review : RuntimeAdapterRevocationReview} :
    review.parentPermissionPresent = true ->
      review.approvalRecorded = false ->
        review.leaseRevoked = true ->
          review.deniedBeforeMutation = true ->
            review.stateUnchangedAfterDenial = true ->
              RuntimeAdapterRevocationRouteFor review =
                RuntimeAdapterRevocationRoute.denyRevokedLease := by
  intro permissionPresent noApprovalRecord leaseRevoked denied unchanged
  unfold RuntimeAdapterRevocationRouteFor
  simp [permissionPresent, noApprovalRecord, leaseRevoked, denied, unchanged]

theorem revoked_lease_without_no_mutation_evidence_requests_evidence
    {review : RuntimeAdapterRevocationReview} :
    review.parentPermissionPresent = true ->
      review.approvalRecorded = false ->
        review.leaseRevoked = true ->
          review.deniedBeforeMutation = false ->
            RuntimeAdapterRevocationRouteFor review =
              RuntimeAdapterRevocationRoute.requestNoMutationEvidence := by
  intro permissionPresent noApprovalRecord leaseRevoked noDenialEvidence
  unfold RuntimeAdapterRevocationRouteFor
  simp [permissionPresent, noApprovalRecord, leaseRevoked, noDenialEvidence]

theorem revoked_authority_receipt_with_no_mutation_denies_before_effect
    {review : RuntimeAdapterRevocationReview} :
    review.parentPermissionPresent = true ->
      review.approvalRecorded = false ->
        review.leaseActive = true ->
          review.leaseRevoked = false ->
            review.authorityReceiptRevoked = true ->
              review.deniedBeforeMutation = true ->
                review.stateUnchangedAfterDenial = true ->
                  RuntimeAdapterRevocationRouteFor review =
                    RuntimeAdapterRevocationRoute.denyRevokedAuthorityReceipt := by
  intro permissionPresent noApprovalRecord leaseActive leaseNotRevoked
    receiptRevoked denied unchanged
  unfold RuntimeAdapterRevocationRouteFor
  simp [permissionPresent, noApprovalRecord, leaseActive, leaseNotRevoked,
    receiptRevoked, denied, unchanged]

theorem revoked_authority_receipt_without_no_mutation_requests_evidence
    {review : RuntimeAdapterRevocationReview} :
    review.parentPermissionPresent = true ->
      review.approvalRecorded = false ->
        review.leaseActive = true ->
          review.leaseRevoked = false ->
            review.authorityReceiptRevoked = true ->
              review.deniedBeforeMutation = false ->
                RuntimeAdapterRevocationRouteFor review =
                  RuntimeAdapterRevocationRoute.requestNoMutationEvidence := by
  intro permissionPresent noApprovalRecord leaseActive leaseNotRevoked
    receiptRevoked noDenialEvidence
  unfold RuntimeAdapterRevocationRouteFor
  simp [permissionPresent, noApprovalRecord, leaseActive, leaseNotRevoked,
    receiptRevoked, noDenialEvidence]

theorem revocation_route_missing_receipt_requests_effect_receipt
    {review : RuntimeAdapterRevocationReview} :
    review.parentPermissionPresent = true ->
      review.approvalRecorded = false ->
        review.leaseActive = true ->
          review.leaseRevoked = false ->
            review.authorityReceiptActive = true ->
              review.authorityReceiptRevoked = false ->
                review.effectAttempted = true ->
                  review.effectReceiptRecorded = false ->
                    RuntimeAdapterRevocationRouteFor review =
                      RuntimeAdapterRevocationRoute.requestEffectReceipt := by
  intro permissionPresent noApprovalRecord leaseActive leaseNotRevoked
    receiptActive receiptNotRevoked effectAttempted missingReceipt
  unfold RuntimeAdapterRevocationRouteFor
  simp [permissionPresent, noApprovalRecord, leaseActive, leaseNotRevoked,
    receiptActive, receiptNotRevoked, effectAttempted, missingReceipt]

theorem complete_revocation_route_dispatches
    {review : RuntimeAdapterRevocationReview} :
    review.parentPermissionPresent = true ->
      review.approvalRecorded = false ->
        review.leaseActive = true ->
          review.leaseRevoked = false ->
            review.authorityReceiptActive = true ->
              review.authorityReceiptRevoked = false ->
                review.effectAttempted = true ->
                  review.effectReceiptRecorded = true ->
                    review.auditRefsRecorded = true ->
                      review.supportStateEffectNone = true ->
                        review.nonClaimsRecorded = true ->
                          RuntimeAdapterRevocationRouteFor review =
                            RuntimeAdapterRevocationRoute.dispatch := by
  intro permissionPresent noApprovalRecord leaseActive leaseNotRevoked
    receiptActive receiptNotRevoked effectAttempted receiptRecorded auditRefs
    supportNone nonClaims
  unfold RuntimeAdapterRevocationRouteFor
  simp [permissionPresent, noApprovalRecord, leaseActive, leaseNotRevoked,
    receiptActive, receiptNotRevoked, effectAttempted, receiptRecorded,
    auditRefs, supportNone, nonClaims]

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

structure HumanOversightDegradationFixtureSummary where
  scopedApprovalAccepted : Bool
  fatigueRoutedToRotation : Bool
  automationBiasBlocked : Bool
  missingQualificationRejected : Bool
  fatiguedApprovalRejected : Bool
  rubberStampRejected : Bool
  automationBiasContradictionRejected : Bool
  alarmFatigueEscalated : Bool
  supportPromotionRejected : Bool
  nonClaimBoundaryRequired : Bool
  supportStateEffectNone : Bool
  chapterCoreSupportEffectNone : Bool
deriving DecidableEq, Repr

def humanOversightDegradationFixtureSummary :
    HumanOversightDegradationFixtureSummary :=
  {
    scopedApprovalAccepted := true,
    fatigueRoutedToRotation := true,
    automationBiasBlocked := true,
    missingQualificationRejected := true,
    fatiguedApprovalRejected := true,
    rubberStampRejected := true,
    automationBiasContradictionRejected := true,
    alarmFatigueEscalated := true,
    supportPromotionRejected := true,
    nonClaimBoundaryRequired := true,
    supportStateEffectNone := true,
    chapterCoreSupportEffectNone := true
  }

def HumanOversightDegradationFixtureValid
    (summary : HumanOversightDegradationFixtureSummary) : Prop :=
  summary.scopedApprovalAccepted = true ∧
    summary.fatigueRoutedToRotation = true ∧
      summary.automationBiasBlocked = true ∧
        summary.missingQualificationRejected = true ∧
          summary.fatiguedApprovalRejected = true ∧
            summary.rubberStampRejected = true ∧
              summary.automationBiasContradictionRejected = true ∧
                summary.alarmFatigueEscalated = true ∧
                  summary.supportPromotionRejected = true ∧
                    summary.nonClaimBoundaryRequired = true ∧
                      summary.supportStateEffectNone = true ∧
                        summary.chapterCoreSupportEffectNone = true

/-!
Reachable effect refinement

The earlier predicates remain as compatibility and fixture-facing surfaces.
This model adds an executable transition system with exact job, caller,
capability, target, lease, epoch, approval, dispatch, effect, observation,
revocation, and rollback custody. It refines the authority-effect model but
does not establish deployed enforcement, sandbox isolation, approval quality,
secret-broker security, effect correctness, or rollback completeness outside
the finite state represented here.
-/

structure RuntimeEffectLease where
  leaseId : Nat
  jobId : Nat
  callerId : Nat
  capabilityId : Nat
  targetId : Nat
  authority : Nat
  authorityEpoch : Nat
  expiresAt : Nat
  remainingUses : Nat
  highImpact : Bool
  rollbackRequired : Bool
deriving DecidableEq, Repr

inductive RuntimeEffectEventKind where
  | prepare | approve | dispatch | commitEffect | observe | revoke | rollback
deriving DecidableEq, Repr

structure RuntimeEffectState where
  parentJobId : Nat
  callerId : Nat
  parentAuthorityCeiling : Nat
  authorityEpoch : Nat
  logicalTime : Nat
  activeLease : Option RuntimeEffectLease
  approvedLeaseId : Option Nat
  dispatchedLeaseId : Option Nat
  revokedLeaseIds : List Nat
  baselineDigest : Nat
  currentDigest : Nat
  materialEffects : Nat
  observedEffects : Nat
  lastEffectLeaseId : Option Nat
  rolledBack : Bool
deriving DecidableEq, Repr

structure RuntimeEffectEvent where
  kind : RuntimeEffectEventKind
  leaseId : Nat
  jobId : Nat
  callerId : Nat
  capabilityId : Nat
  targetId : Nat
  authority : Nat
  authorityEpoch : Nat
  expiresAt : Nat
  remainingUses : Nat
  highImpact : Bool
  rollbackRequired : Bool
  logicalTime : Nat
  permissionPresent : Bool
  sandboxObserved : Bool
  targetOwnerApproved : Bool
  approvalReceipt : Bool
  approverIndependent : Bool
  dispatchReceipt : Bool
  effectReceipt : Bool
  independentObservation : Bool
  revocationReceipt : Bool
  rollbackHandlePresent : Bool
  rollbackReceipt : Bool
  secretMaterializedToModelContext : Bool
  preDigest : Nat
  postDigest : Nat
deriving DecidableEq, Repr

def RuntimeEffectEvent.lease (event : RuntimeEffectEvent) : RuntimeEffectLease := {
  leaseId := event.leaseId
  jobId := event.jobId
  callerId := event.callerId
  capabilityId := event.capabilityId
  targetId := event.targetId
  authority := event.authority
  authorityEpoch := event.authorityEpoch
  expiresAt := event.expiresAt
  remainingUses := event.remainingUses
  highImpact := event.highImpact
  rollbackRequired := event.rollbackRequired
}

def RuntimeEffectEventAdmissible
    (state : RuntimeEffectState) (event : RuntimeEffectEvent) : Prop :=
  state.logicalTime < event.logicalTime ∧
  match event.kind with
  | .prepare =>
      state.activeLease = none ∧
        event.leaseId ∉ state.revokedLeaseIds ∧
        0 < event.leaseId ∧
        event.jobId = state.parentJobId ∧
        event.callerId = state.callerId ∧
        event.authority ≤ state.parentAuthorityCeiling ∧
        event.authorityEpoch = state.authorityEpoch ∧
        event.logicalTime ≤ event.expiresAt ∧
        0 < event.remainingUses ∧
        event.permissionPresent = true ∧
        event.sandboxObserved = true ∧
        event.targetOwnerApproved = true ∧
        event.approvalReceipt = true ∧
        event.secretMaterializedToModelContext = false
  | .approve =>
      state.activeLease = some event.lease ∧
        state.dispatchedLeaseId = none ∧
        event.leaseId ∉ state.revokedLeaseIds ∧
        event.authorityEpoch = state.authorityEpoch ∧
        event.logicalTime ≤ event.expiresAt ∧
        0 < event.remainingUses ∧
        event.targetOwnerApproved = true ∧
        event.approvalReceipt = true ∧
        (event.highImpact = false ∨ event.approverIndependent = true)
  | .dispatch =>
      state.activeLease = some event.lease ∧
        state.approvedLeaseId = some event.leaseId ∧
        event.leaseId ∉ state.revokedLeaseIds ∧
        event.authorityEpoch = state.authorityEpoch ∧
        event.logicalTime ≤ event.expiresAt ∧
        0 < event.remainingUses ∧
        event.sandboxObserved = true ∧
        event.secretMaterializedToModelContext = false ∧
        event.dispatchReceipt = true
  | .commitEffect =>
      state.activeLease = some event.lease ∧
        state.approvedLeaseId = some event.leaseId ∧
        state.dispatchedLeaseId = some event.leaseId ∧
        event.leaseId ∉ state.revokedLeaseIds ∧
        event.authorityEpoch = state.authorityEpoch ∧
        event.logicalTime ≤ event.expiresAt ∧
        0 < event.remainingUses ∧
        event.effectReceipt = true ∧
        event.preDigest = state.currentDigest ∧
        event.postDigest ≠ state.currentDigest ∧
        (event.rollbackRequired = false ∨ event.rollbackHandlePresent = true)
  | .observe =>
      state.lastEffectLeaseId = some event.leaseId ∧
        state.observedEffects < state.materialEffects ∧
        event.independentObservation = true ∧
        event.effectReceipt = true
  | .revoke =>
      state.activeLease = some event.lease ∧
        event.revocationReceipt = true
  | .rollback =>
      state.lastEffectLeaseId = some event.leaseId ∧
        0 < state.materialEffects ∧
        state.observedEffects = state.materialEffects ∧
        event.rollbackHandlePresent = true ∧
        event.rollbackReceipt = true ∧
        event.effectReceipt = true ∧
        event.postDigest = state.baselineDigest

instance runtimeEffectEventAdmissibleDecidable
    (state : RuntimeEffectState) (event : RuntimeEffectEvent) :
    Decidable (RuntimeEffectEventAdmissible state event) := by
  unfold RuntimeEffectEventAdmissible
  cases event.kind <;> infer_instance

def ApplyRuntimeEffectEvent
    (state : RuntimeEffectState) (event : RuntimeEffectEvent) :
    RuntimeEffectState :=
  match event.kind with
  | .prepare =>
      { state with
          activeLease := some event.lease
          logicalTime := event.logicalTime }
  | .approve =>
      { state with
          approvedLeaseId := some event.leaseId
          logicalTime := event.logicalTime }
  | .dispatch =>
      { state with
          dispatchedLeaseId := some event.leaseId
          logicalTime := event.logicalTime }
  | .commitEffect =>
      { state with
          activeLease := some { event.lease with remainingUses := event.remainingUses - 1 }
          approvedLeaseId := none
          dispatchedLeaseId := none
          currentDigest := event.postDigest
          materialEffects := state.materialEffects + 1
          lastEffectLeaseId := some event.leaseId
          logicalTime := event.logicalTime }
  | .observe =>
      { state with
          observedEffects := state.observedEffects + 1
          logicalTime := event.logicalTime }
  | .revoke =>
      { state with
          authorityEpoch := state.authorityEpoch + 1
          activeLease := none
          approvedLeaseId := none
          dispatchedLeaseId := none
          revokedLeaseIds := event.leaseId :: state.revokedLeaseIds
          logicalTime := event.logicalTime }
  | .rollback =>
      { state with
          currentDigest := event.postDigest
          materialEffects := 0
          observedEffects := 0
          rolledBack := true
          logicalTime := event.logicalTime }

def RuntimeEffectStep
    (state : RuntimeEffectState) (event : RuntimeEffectEvent) :
    Option RuntimeEffectState :=
  if RuntimeEffectEventAdmissible state event then
    some (ApplyRuntimeEffectEvent state event)
  else
    none

def RuntimeEffectRun :
    RuntimeEffectState → List RuntimeEffectEvent → Option RuntimeEffectState
  | state, [] => some state
  | state, event :: tail =>
      match RuntimeEffectStep state event with
      | none => none
      | some next => RuntimeEffectRun next tail

def RuntimeLeaseBoundToState
    (state : RuntimeEffectState) (lease : RuntimeEffectLease) : Prop :=
  lease.jobId = state.parentJobId ∧
    lease.callerId = state.callerId ∧
    lease.authority ≤ state.parentAuthorityCeiling ∧
    lease.authorityEpoch = state.authorityEpoch ∧
    lease.leaseId ∉ state.revokedLeaseIds

def RuntimeEffectStateInvariant (state : RuntimeEffectState) : Prop :=
  (∀ lease, state.activeLease = some lease ->
      RuntimeLeaseBoundToState state lease) ∧
    (∀ leaseId, state.approvedLeaseId = some leaseId ->
      ∃ lease, state.activeLease = some lease ∧ lease.leaseId = leaseId) ∧
    (∀ leaseId, state.dispatchedLeaseId = some leaseId ->
      ∃ lease, state.activeLease = some lease ∧
        state.approvedLeaseId = some leaseId ∧ lease.leaseId = leaseId) ∧
    state.observedEffects ≤ state.materialEffects

theorem accepted_runtime_effect_step_is_admissible
    {state next : RuntimeEffectState} {event : RuntimeEffectEvent}
    (accepted : RuntimeEffectStep state event = some next) :
    RuntimeEffectEventAdmissible state event := by
  unfold RuntimeEffectStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_runtime_effect_step_applies_event
    {state next : RuntimeEffectState} {event : RuntimeEffectEvent}
    (accepted : RuntimeEffectStep state event = some next) :
    next = ApplyRuntimeEffectEvent state event := by
  unfold RuntimeEffectStep at accepted
  split at accepted
  · simp_all
  · simp at accepted

theorem apply_runtime_effect_event_preserves_invariant
    {state : RuntimeEffectState} {event : RuntimeEffectEvent}
    (invariant : RuntimeEffectStateInvariant state)
    (admissible : RuntimeEffectEventAdmissible state event) :
    RuntimeEffectStateInvariant (ApplyRuntimeEffectEvent state event) := by
  rcases invariant with
    ⟨activeInvariant, approvedInvariant, dispatchedInvariant,
      observationInvariant⟩
  rcases admissible with ⟨_time, admissible⟩
  cases kind : event.kind
  · simp [kind] at admissible
    rcases admissible with
      ⟨noActive, notRevoked, _positiveId, job, caller, ceiling, epoch,
        _fresh, _uses, _permission, _sandbox, _owner, _receipt, _secret⟩
    have noApproved : state.approvedLeaseId = none := by
      cases approved : state.approvedLeaseId with
      | none => rfl
      | some leaseId =>
          rcases approvedInvariant leaseId approved with
            ⟨lease, active, _binding⟩
          rw [noActive] at active
          contradiction
    have noDispatched : state.dispatchedLeaseId = none := by
      cases dispatched : state.dispatchedLeaseId with
      | none => rfl
      | some leaseId =>
          rcases dispatchedInvariant leaseId dispatched with
            ⟨lease, active, _approved, _binding⟩
          rw [noActive] at active
          contradiction
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro lease active
      have leaseEq : event.lease = lease := by
        exact Option.some.inj (by
          simpa [ApplyRuntimeEffectEvent, kind] using active)
      subst lease
      simp [RuntimeLeaseBoundToState, ApplyRuntimeEffectEvent, kind,
        RuntimeEffectEvent.lease, job, caller, ceiling, epoch, notRevoked]
    · simp [ApplyRuntimeEffectEvent, kind, noApproved]
    · simp [ApplyRuntimeEffectEvent, kind, noDispatched]
    · simpa [ApplyRuntimeEffectEvent, kind] using observationInvariant
  · simp [kind] at admissible
    rcases admissible with
      ⟨active, noDispatched, _notRevoked, _epoch, _fresh, _uses,
        _owner, _receipt, _independent⟩
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro lease nextActive
      have oldBound := activeInvariant lease (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextActive)
      simpa [RuntimeLeaseBoundToState, ApplyRuntimeEffectEvent, kind] using
        oldBound
    · intro leaseId approved
      have leaseIdEq : event.leaseId = leaseId := by
        exact Option.some.inj (by
          simpa [ApplyRuntimeEffectEvent, kind] using approved)
      exact ⟨event.lease, by
        simpa [ApplyRuntimeEffectEvent, kind] using active, leaseIdEq⟩
    · simp [ApplyRuntimeEffectEvent, kind, noDispatched]
    · simpa [ApplyRuntimeEffectEvent, kind] using observationInvariant
  · simp [kind] at admissible
    rcases admissible with
      ⟨active, approved, _notRevoked, _epoch, _fresh, _uses, _sandbox,
        _secret, _receipt⟩
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro lease nextActive
      have oldBound := activeInvariant lease (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextActive)
      simpa [RuntimeLeaseBoundToState, ApplyRuntimeEffectEvent, kind] using
        oldBound
    · intro leaseId nextApproved
      rcases approvedInvariant leaseId (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextApproved) with
        ⟨lease, oldActive, binding⟩
      exact ⟨lease, by
        simpa [ApplyRuntimeEffectEvent, kind] using oldActive, binding⟩
    · intro leaseId dispatched
      have leaseIdEq : event.leaseId = leaseId := by
        exact Option.some.inj (by
          simpa [ApplyRuntimeEffectEvent, kind] using dispatched)
      have approvedForLeaseId : state.approvedLeaseId = some leaseId := by
        simpa [leaseIdEq] using approved
      exact ⟨event.lease, by
        simpa [ApplyRuntimeEffectEvent, kind] using active, by
        simpa [ApplyRuntimeEffectEvent, kind] using approvedForLeaseId,
        leaseIdEq⟩
    · simpa [ApplyRuntimeEffectEvent, kind] using observationInvariant
  · simp [kind] at admissible
    rcases admissible with
      ⟨active, _approved, _dispatched, _notRevoked, _epoch, _fresh,
        _uses, _receipt, _pre, _changed, _rollback⟩
    have bound := activeInvariant event.lease active
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro lease nextActive
      have leaseEq :
          { event.lease with remainingUses := event.remainingUses - 1 } =
            lease := by
        exact Option.some.inj (by
          simpa [ApplyRuntimeEffectEvent, kind] using nextActive)
      subst lease
      simpa [RuntimeLeaseBoundToState, ApplyRuntimeEffectEvent, kind,
        RuntimeEffectEvent.lease] using bound
    · simp [ApplyRuntimeEffectEvent, kind]
    · simp [ApplyRuntimeEffectEvent, kind]
    · simpa [ApplyRuntimeEffectEvent, kind] using
        (Nat.le.step observationInvariant)
  · simp [kind] at admissible
    rcases admissible with ⟨_lease, observed, _independent, _receipt⟩
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro lease nextActive
      have oldBound := activeInvariant lease (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextActive)
      simpa [RuntimeLeaseBoundToState, ApplyRuntimeEffectEvent, kind] using
        oldBound
    · intro leaseId nextApproved
      rcases approvedInvariant leaseId (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextApproved) with
        ⟨lease, oldActive, binding⟩
      exact ⟨lease, by
        simpa [ApplyRuntimeEffectEvent, kind] using oldActive, binding⟩
    · intro leaseId nextDispatched
      rcases dispatchedInvariant leaseId (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextDispatched) with
        ⟨lease, oldActive, oldApproved, binding⟩
      exact ⟨lease, by
        simpa [ApplyRuntimeEffectEvent, kind] using oldActive, by
        simpa [ApplyRuntimeEffectEvent, kind] using oldApproved, binding⟩
    · simpa [ApplyRuntimeEffectEvent, kind] using Nat.succ_le_of_lt observed
  · refine ⟨?_, ?_, ?_, ?_⟩
    · simp [ApplyRuntimeEffectEvent, kind]
    · simp [ApplyRuntimeEffectEvent, kind]
    · simp [ApplyRuntimeEffectEvent, kind]
    · simpa [ApplyRuntimeEffectEvent, kind] using observationInvariant
  · simp [kind] at admissible
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro lease nextActive
      have oldBound := activeInvariant lease (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextActive)
      simpa [RuntimeLeaseBoundToState, ApplyRuntimeEffectEvent, kind] using
        oldBound
    · intro leaseId nextApproved
      rcases approvedInvariant leaseId (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextApproved) with
        ⟨lease, oldActive, binding⟩
      exact ⟨lease, by
        simpa [ApplyRuntimeEffectEvent, kind] using oldActive, binding⟩
    · intro leaseId nextDispatched
      rcases dispatchedInvariant leaseId (by
        simpa [ApplyRuntimeEffectEvent, kind] using nextDispatched) with
        ⟨lease, oldActive, oldApproved, binding⟩
      exact ⟨lease, by
        simpa [ApplyRuntimeEffectEvent, kind] using oldActive, by
        simpa [ApplyRuntimeEffectEvent, kind] using oldApproved, binding⟩
    · simp [ApplyRuntimeEffectEvent, kind]

theorem accepted_runtime_effect_step_preserves_invariant
    {state next : RuntimeEffectState} {event : RuntimeEffectEvent}
    (invariant : RuntimeEffectStateInvariant state)
    (accepted : RuntimeEffectStep state event = some next) :
    RuntimeEffectStateInvariant next := by
  have admissible := accepted_runtime_effect_step_is_admissible accepted
  have applies := accepted_runtime_effect_step_applies_event accepted
  rw [applies]
  exact apply_runtime_effect_event_preserves_invariant invariant admissible

theorem runtime_effect_run_preserves_invariant
    {state next : RuntimeEffectState} {events : List RuntimeEffectEvent}
    (invariant : RuntimeEffectStateInvariant state)
    (run : RuntimeEffectRun state events = some next) :
    RuntimeEffectStateInvariant next := by
  induction events generalizing state with
  | nil =>
      simp [RuntimeEffectRun] at run
      subst next
      exact invariant
  | cons event tail ih =>
      simp [RuntimeEffectRun] at run
      cases step : RuntimeEffectStep state event with
      | none => simp [step] at run
      | some middle =>
          simp [step] at run
          exact ih (accepted_runtime_effect_step_preserves_invariant invariant step) run

def initialRuntimeEffectState : RuntimeEffectState where
  parentJobId := 101
  callerId := 201
  parentAuthorityCeiling := 3
  authorityEpoch := 11
  logicalTime := 0
  activeLease := none
  approvedLeaseId := none
  dispatchedLeaseId := none
  revokedLeaseIds := []
  baselineDigest := 7001
  currentDigest := 7001
  materialEffects := 0
  observedEffects := 0
  lastEffectLeaseId := none
  rolledBack := false

def prepareRuntimeEffect : RuntimeEffectEvent where
  kind := .prepare
  leaseId := 71
  jobId := 101
  callerId := 201
  capabilityId := 301
  targetId := 401
  authority := 3
  authorityEpoch := 11
  expiresAt := 20
  remainingUses := 1
  highImpact := false
  rollbackRequired := true
  logicalTime := 1
  permissionPresent := true
  sandboxObserved := true
  targetOwnerApproved := true
  approvalReceipt := true
  approverIndependent := true
  dispatchReceipt := false
  effectReceipt := false
  independentObservation := false
  revocationReceipt := false
  rollbackHandlePresent := true
  rollbackReceipt := false
  secretMaterializedToModelContext := false
  preDigest := 7001
  postDigest := 7001

def successfulRuntimeEffectTrace : List RuntimeEffectEvent := [
  prepareRuntimeEffect,
  { prepareRuntimeEffect with
      kind := .approve
      logicalTime := 2 },
  { prepareRuntimeEffect with
      kind := .dispatch
      logicalTime := 3
      dispatchReceipt := true },
  { prepareRuntimeEffect with
      kind := .commitEffect
      logicalTime := 4
      effectReceipt := true
      postDigest := 8002 },
  { prepareRuntimeEffect with
      kind := .observe
      logicalTime := 5
      effectReceipt := true
      independentObservation := true },
  { prepareRuntimeEffect with
      kind := .rollback
      logicalTime := 6
      effectReceipt := true
      rollbackReceipt := true
      postDigest := 7001 }
]

theorem initial_runtime_effect_state_satisfies_invariant :
    RuntimeEffectStateInvariant initialRuntimeEffectState := by
  simp [RuntimeEffectStateInvariant, initialRuntimeEffectState]

theorem complete_runtime_effect_trace_reaches_exact_rollback :
    RuntimeEffectRun initialRuntimeEffectState successfulRuntimeEffectTrace = some
      { initialRuntimeEffectState with
          activeLease := some { prepareRuntimeEffect.lease with remainingUses := 0 }
          currentDigest := 7001
          materialEffects := 0
          observedEffects := 0
          lastEffectLeaseId := some prepareRuntimeEffect.leaseId
          rolledBack := true
          logicalTime := 6 } := by
  native_decide

def ProjectRuntimeLease
    (lease : RuntimeEffectLease) :
    AsiStackProofs.AuthorityEffectRefinement.Grant := {
  grantId := lease.leaseId
  principalId := lease.callerId
  operationId := lease.capabilityId
  targetId := lease.targetId
  authority := lease.authority
  epoch := lease.authorityEpoch
  expiresAt := lease.expiresAt
  remainingUses := lease.remainingUses
}

def ProjectRuntimeEffectState
    (state : RuntimeEffectState) :
    AsiStackProofs.AuthorityEffectRefinement.AuthorityState := {
  callerCeiling := state.parentAuthorityCeiling
  authorityEpoch := state.authorityEpoch
  logicalTime := state.logicalTime
  activeGrant := state.activeLease.map ProjectRuntimeLease
  approvedGrantId := state.approvedLeaseId
  dispatchedGrantId := state.dispatchedLeaseId
  revokedGrantIds := state.revokedLeaseIds
  materialEffects := state.materialEffects
  observedEffects := state.observedEffects
  rolledBack := state.rolledBack
}

def ProjectRuntimeEffectEventKind : RuntimeEffectEventKind ->
    AsiStackProofs.AuthorityEffectRefinement.AuthorityEventKind
  | .prepare => .issue
  | .approve => .approve
  | .dispatch => .dispatch
  | .commitEffect => .commitEffect
  | .observe => .observe
  | .revoke => .revoke
  | .rollback => .rollback

def ProjectRuntimeEffectEvent
    (event : RuntimeEffectEvent) :
    AsiStackProofs.AuthorityEffectRefinement.AuthorityEvent := {
  kind := ProjectRuntimeEffectEventKind event.kind
  grantId := event.leaseId
  principalId := event.callerId
  operationId := event.capabilityId
  targetId := event.targetId
  authority := event.authority
  authorityEpoch := event.authorityEpoch
  expiresAt := event.expiresAt
  remainingUses := event.remainingUses
  logicalTime := event.logicalTime
  targetOwnerApproved := event.targetOwnerApproved
  approvalReceipt := event.approvalReceipt
  dispatchReceipt := event.dispatchReceipt
  effectReceipt := event.effectReceipt
  independentObservation := event.independentObservation
  revocationReceipt := event.revocationReceipt
  rollbackExact := event.rollbackReceipt
}

theorem projected_runtime_lease_preserves_exact_identity
    (lease : RuntimeEffectLease) :
    (ProjectRuntimeLease lease).grantId = lease.leaseId ∧
      (ProjectRuntimeLease lease).principalId = lease.callerId ∧
      (ProjectRuntimeLease lease).operationId = lease.capabilityId ∧
      (ProjectRuntimeLease lease).targetId = lease.targetId ∧
      (ProjectRuntimeLease lease).authority = lease.authority ∧
      (ProjectRuntimeLease lease).epoch = lease.authorityEpoch := by
  simp [ProjectRuntimeLease]

theorem project_runtime_apply_commutes
    (state : RuntimeEffectState) (event : RuntimeEffectEvent) :
    ProjectRuntimeEffectState (ApplyRuntimeEffectEvent state event) =
      AsiStackProofs.AuthorityEffectRefinement.ApplyAuthorityEvent
        (ProjectRuntimeEffectState state) (ProjectRuntimeEffectEvent event) := by
  unfold AsiStackProofs.AuthorityEffectRefinement.ApplyAuthorityEvent
  cases kind : event.kind <;>
    simp [ApplyRuntimeEffectEvent, ProjectRuntimeEffectState,
      ProjectRuntimeEffectEvent, ProjectRuntimeEffectEventKind,
      ProjectRuntimeLease, RuntimeEffectEvent.lease,
      AsiStackProofs.AuthorityEffectRefinement.AuthorityEvent.grant, kind]

theorem runtime_admissibility_refines_authority_admissibility
    {state : RuntimeEffectState} {event : RuntimeEffectEvent}
    (admissible : RuntimeEffectEventAdmissible state event) :
    AsiStackProofs.AuthorityEffectRefinement.AuthorityEventValid
      (ProjectRuntimeEffectState state) (ProjectRuntimeEffectEvent event) = true := by
  rcases admissible with ⟨time, admissible⟩
  cases kind : event.kind
  · simp [kind] at admissible
    rcases admissible with
      ⟨active, notRevoked, positiveId, _job, _caller, ceiling, epoch,
        fresh, uses, _permission, _sandbox, owner, receipt, _secret⟩
    simp [AsiStackProofs.AuthorityEffectRefinement.AuthorityEventValid,
      ProjectRuntimeEffectState, ProjectRuntimeEffectEvent,
      ProjectRuntimeEffectEventKind, kind, time, active, notRevoked,
      positiveId, ceiling, epoch, fresh, uses, owner, receipt]
  · simp [kind] at admissible
    rcases admissible with
      ⟨active, _noDispatched, notRevoked, epoch, fresh, uses, owner, receipt,
        _independent⟩
    simp [AsiStackProofs.AuthorityEffectRefinement.AuthorityEventValid,
      ProjectRuntimeEffectState, ProjectRuntimeEffectEvent,
      ProjectRuntimeEffectEventKind, ProjectRuntimeLease,
      RuntimeEffectEvent.lease, kind, time, active, notRevoked, epoch,
      fresh, uses, owner, receipt,
      AsiStackProofs.AuthorityEffectRefinement.AuthorityEvent.grant]
  · simp [kind] at admissible
    rcases admissible with
      ⟨active, approved, notRevoked, epoch, fresh, uses, _sandbox,
        _secret, receipt⟩
    simp [AsiStackProofs.AuthorityEffectRefinement.AuthorityEventValid,
      ProjectRuntimeEffectState, ProjectRuntimeEffectEvent,
      ProjectRuntimeEffectEventKind, ProjectRuntimeLease,
      RuntimeEffectEvent.lease, kind, time, active, approved, notRevoked,
      epoch, fresh, uses, receipt,
      AsiStackProofs.AuthorityEffectRefinement.AuthorityEvent.grant]
  · simp [kind] at admissible
    rcases admissible with
      ⟨active, approved, dispatched, notRevoked, epoch, fresh, uses,
        receipt, _pre, _changed, _rollback⟩
    simp [AsiStackProofs.AuthorityEffectRefinement.AuthorityEventValid,
      ProjectRuntimeEffectState, ProjectRuntimeEffectEvent,
      ProjectRuntimeEffectEventKind, ProjectRuntimeLease,
      RuntimeEffectEvent.lease, kind, time, active, approved, dispatched,
      notRevoked, epoch, fresh, uses, receipt,
      AsiStackProofs.AuthorityEffectRefinement.AuthorityEvent.grant]
  · simp [kind] at admissible
    rcases admissible with ⟨_lease, observed, independent, receipt⟩
    simp [AsiStackProofs.AuthorityEffectRefinement.AuthorityEventValid,
      ProjectRuntimeEffectState, ProjectRuntimeEffectEvent,
      ProjectRuntimeEffectEventKind, kind, time, observed, independent,
      receipt]
  · simp [kind] at admissible
    rcases admissible with ⟨active, receipt⟩
    simp [AsiStackProofs.AuthorityEffectRefinement.AuthorityEventValid,
      ProjectRuntimeEffectState, ProjectRuntimeEffectEvent,
      ProjectRuntimeEffectEventKind, ProjectRuntimeLease,
      RuntimeEffectEvent.lease, kind, time, active, receipt,
      AsiStackProofs.AuthorityEffectRefinement.AuthorityEvent.grant]
  · simp [kind] at admissible
    rcases admissible with
      ⟨_lease, effects, observed, _handle, rollback, receipt, _digest⟩
    simp [AsiStackProofs.AuthorityEffectRefinement.AuthorityEventValid,
      ProjectRuntimeEffectState, ProjectRuntimeEffectEvent,
      ProjectRuntimeEffectEventKind, kind, time, effects, observed,
      rollback, receipt]

theorem runtime_step_refines_authority_step
    {state next : RuntimeEffectState} {event : RuntimeEffectEvent}
    (accepted : RuntimeEffectStep state event = some next) :
    AsiStackProofs.AuthorityEffectRefinement.AuthorityStep
      (ProjectRuntimeEffectState state) (ProjectRuntimeEffectEvent event) =
        some (ProjectRuntimeEffectState next) := by
  have admissible := accepted_runtime_effect_step_is_admissible accepted
  have authorityValid :=
    runtime_admissibility_refines_authority_admissibility admissible
  have applies := accepted_runtime_effect_step_applies_event accepted
  unfold AsiStackProofs.AuthorityEffectRefinement.AuthorityStep
  simp [authorityValid, applies, project_runtime_apply_commutes]

theorem runtime_run_refines_authority_run
    {state next : RuntimeEffectState} {events : List RuntimeEffectEvent}
    (run : RuntimeEffectRun state events = some next) :
    AsiStackProofs.AuthorityEffectRefinement.AuthorityRun
      (ProjectRuntimeEffectState state) (events.map ProjectRuntimeEffectEvent) =
        some (ProjectRuntimeEffectState next) := by
  induction events generalizing state with
  | nil =>
      simp [RuntimeEffectRun] at run
      subst next
      rfl
  | cons event tail ih =>
      simp [RuntimeEffectRun] at run
      cases step : RuntimeEffectStep state event with
      | none => simp [step] at run
      | some middle =>
          simp [step] at run
          simp [AsiStackProofs.AuthorityEffectRefinement.AuthorityRun,
            runtime_step_refines_authority_step step]
          exact ih run

theorem runtime_effect_denial_is_state_noninterfering
    {state : RuntimeEffectState} {event : RuntimeEffectEvent}
    (denied : RuntimeEffectStep state event = none) :
    RuntimeEffectRun state [event] = none := by
  simp [RuntimeEffectRun, denied]

def preparedRuntimeEffectState : RuntimeEffectState :=
  ApplyRuntimeEffectEvent initialRuntimeEffectState prepareRuntimeEffect

def approvedRuntimeEffectState : RuntimeEffectState :=
  ApplyRuntimeEffectEvent preparedRuntimeEffectState
    { prepareRuntimeEffect with
        kind := .approve
        logicalTime := 2 }

def dispatchedRuntimeEffectState : RuntimeEffectState :=
  ApplyRuntimeEffectEvent approvedRuntimeEffectState
    { prepareRuntimeEffect with
        kind := .dispatch
        logicalTime := 3
        dispatchReceipt := true }

theorem missing_parent_permission_is_rejected_before_prepare :
    RuntimeEffectStep initialRuntimeEffectState
      { prepareRuntimeEffect with permissionPresent := false } = none := by
  native_decide

theorem caller_identity_substitution_is_rejected_before_prepare :
    RuntimeEffectStep initialRuntimeEffectState
      { prepareRuntimeEffect with callerId := 999 } = none := by
  native_decide

theorem authority_widening_is_rejected_before_prepare :
    RuntimeEffectStep initialRuntimeEffectState
      { prepareRuntimeEffect with authority := 4 } = none := by
  native_decide

theorem expired_lease_is_rejected_before_dispatch :
    RuntimeEffectStep approvedRuntimeEffectState
      { prepareRuntimeEffect with
          kind := .dispatch
          logicalTime := 21
          dispatchReceipt := true } = none := by
  native_decide

theorem scoped_approval_identity_substitution_is_rejected :
    RuntimeEffectStep approvedRuntimeEffectState
      { prepareRuntimeEffect with
          kind := .dispatch
          targetId := 999
          logicalTime := 3
          dispatchReceipt := true } = none := by
  native_decide

theorem secret_materialization_is_rejected_before_dispatch :
    RuntimeEffectStep approvedRuntimeEffectState
      { prepareRuntimeEffect with
          kind := .dispatch
          logicalTime := 3
          dispatchReceipt := true
          secretMaterializedToModelContext := true } = none := by
  native_decide

theorem effect_without_dispatch_is_rejected :
    RuntimeEffectStep approvedRuntimeEffectState
      { prepareRuntimeEffect with
          kind := .commitEffect
          logicalTime := 3
          effectReceipt := true
          postDigest := 8002 } = none := by
  native_decide

theorem rollback_required_without_handle_is_rejected_before_effect :
    RuntimeEffectStep dispatchedRuntimeEffectState
      { prepareRuntimeEffect with
          kind := .commitEffect
          logicalTime := 4
          effectReceipt := true
          postDigest := 8002
          rollbackHandlePresent := false } = none := by
  native_decide

theorem effect_prestate_mismatch_is_rejected :
    RuntimeEffectStep dispatchedRuntimeEffectState
      { prepareRuntimeEffect with
          kind := .commitEffect
          logicalTime := 4
          effectReceipt := true
          preDigest := 9999
          postDigest := 8002 } = none := by
  native_decide

def revokedRuntimeEffectState : RuntimeEffectState :=
  ApplyRuntimeEffectEvent preparedRuntimeEffectState
    { prepareRuntimeEffect with
        kind := .revoke
        logicalTime := 2
        revocationReceipt := true }

theorem revoked_lease_cannot_be_prepared_again :
    RuntimeEffectStep revokedRuntimeEffectState
      { prepareRuntimeEffect with
          authorityEpoch := 12
          logicalTime := 3 } = none := by
  native_decide

theorem revoked_state_cannot_dispatch_without_a_fresh_lease :
    RuntimeEffectStep revokedRuntimeEffectState
      { prepareRuntimeEffect with
          kind := .dispatch
          authorityEpoch := 12
          logicalTime := 3
          dispatchReceipt := true } = none := by
  native_decide

theorem successful_trace_refines_authority_trace :
    AsiStackProofs.AuthorityEffectRefinement.AuthorityRun
      (ProjectRuntimeEffectState initialRuntimeEffectState)
      (successfulRuntimeEffectTrace.map ProjectRuntimeEffectEvent) =
        some (ProjectRuntimeEffectState
          { initialRuntimeEffectState with
              activeLease := some
                { prepareRuntimeEffect.lease with remainingUses := 0 }
              currentDigest := 7001
              materialEffects := 0
              observedEffects := 0
              lastEffectLeaseId := some prepareRuntimeEffect.leaseId
              rolledBack := true
              logicalTime := 6 }) := by
  apply runtime_run_refines_authority_run
  exact complete_runtime_effect_trace_reaches_exact_rollback

end AsiStackProofs.RuntimeAdapters
