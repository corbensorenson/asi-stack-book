namespace AsiStackProofs.Authority

inductive AuthorityLevel where
  | none
  | read
  | transform
  | write
  | execute
  | approve
deriving DecidableEq, Repr

def AuthorityLevel.rank : AuthorityLevel -> Nat
  | .none => 0
  | .read => 1
  | .transform => 2
  | .write => 3
  | .execute => 4
  | .approve => 5

structure GovernanceGrant where
  active : Bool
  scopeMatches : Bool
  maxCeiling : AuthorityLevel
deriving DecidableEq, Repr

def GrantAuthorizesLevel (grant : GovernanceGrant) (level : AuthorityLevel) : Prop :=
  grant.active = true ∧
    grant.scopeMatches = true ∧
    level.rank <= grant.maxCeiling.rank

structure AuthorityTransition where
  before : AuthorityLevel
  after : AuthorityLevel
  grant : Option GovernanceGrant
deriving DecidableEq, Repr

def ValidAuthorityTransition (transition : AuthorityTransition) : Prop :=
  transition.after.rank <= transition.before.rank ∨
    ∃ grant, transition.grant = some grant ∧ GrantAuthorizesLevel grant transition.after

theorem valid_transition_without_grant_preserves_ceiling
    {transition : AuthorityTransition} :
    ValidAuthorityTransition transition ->
    transition.grant = none ->
    transition.after.rank <= transition.before.rank := by
  intro valid noGrant
  cases valid with
  | inl preserved =>
      exact preserved
  | inr granted =>
      rcases granted with ⟨grant, grantPresent, _authorizes⟩
      rw [noGrant] at grantPresent
      contradiction

structure ExecutionRequest where
  activeCeiling : AuthorityLevel
  required : AuthorityLevel
  grant : Option GovernanceGrant
deriving DecidableEq, Repr

def ExecutionAuthorized (request : ExecutionRequest) : Prop :=
  request.required.rank <= request.activeCeiling.rank ∨
    ∃ grant, request.grant = some grant ∧ GrantAuthorizesLevel grant request.required

theorem missing_grant_blocks_over_ceiling_execution
    {request : ExecutionRequest} :
    request.activeCeiling.rank < request.required.rank ->
    request.grant = none ->
    ¬ ExecutionAuthorized request := by
  intro exceeds noGrant authorized
  cases authorized with
  | inl withinCeiling =>
      exact Nat.not_le_of_gt exceeds withinCeiling
  | inr granted =>
      rcases granted with ⟨grant, grantPresent, _authorizes⟩
      rw [noGrant] at grantPresent
      contradiction

inductive AuthorityDecision where
  | allow
  | deny
  | escalate
deriving DecidableEq, Repr

structure AuthorityDecisionRecord where
  callerCeiling : AuthorityLevel
  activeCeiling : AuthorityLevel
  targetRequired : AuthorityLevel
  decision : AuthorityDecision
  effectReceiptPresent : Bool
  denialReasonPresent : Bool
  auditRefsPresent : Bool
  nonClaimsPresent : Bool
  reviewRoutePresent : Bool
  grantExpired : Bool
  grantRevoked : Bool
deriving DecidableEq, Repr

def CommonAuthorityRecordValid (record : AuthorityDecisionRecord) : Prop :=
  record.auditRefsPresent = true ∧
    record.nonClaimsPresent = true

def AuthorityDecisionValid (record : AuthorityDecisionRecord) : Prop :=
  CommonAuthorityRecordValid record ∧
    match record.decision with
    | .allow =>
        record.effectReceiptPresent = true ∧
          record.denialReasonPresent = false ∧
          record.grantExpired = false ∧
          record.grantRevoked = false ∧
          record.activeCeiling.rank <= record.callerCeiling.rank ∧
          record.targetRequired.rank <= record.activeCeiling.rank
    | .deny =>
        record.effectReceiptPresent = false ∧
          record.denialReasonPresent = true
    | .escalate =>
        record.effectReceiptPresent = false ∧
          record.denialReasonPresent = true ∧
          record.reviewRoutePresent = true

theorem valid_allow_decision_has_effect_receipt
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.allow ->
    record.effectReceiptPresent = true := by
  intro valid isAllow
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isAllow] at decisionValid
  exact decisionValid.1

theorem valid_allow_decision_preserves_caller_ceiling
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.allow ->
    record.activeCeiling.rank <= record.callerCeiling.rank := by
  intro valid isAllow
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isAllow] at decisionValid
  exact decisionValid.2.2.2.2.1

theorem valid_allow_decision_target_within_active_ceiling
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.allow ->
    record.targetRequired.rank <= record.activeCeiling.rank := by
  intro valid isAllow
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isAllow] at decisionValid
  exact decisionValid.2.2.2.2.2

theorem valid_deny_decision_has_no_effect_receipt
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.deny ->
    record.effectReceiptPresent = false := by
  intro valid isDeny
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isDeny] at decisionValid
  exact decisionValid.1

theorem valid_escalation_routes_to_review
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.escalate ->
    record.reviewRoutePresent = true := by
  intro valid isEscalate
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isEscalate] at decisionValid
  exact decisionValid.2.2

inductive AuthorityLifecycleRoute where
  | noAuthorityRequested
  | requestPrincipal
  | requestOperation
  | requestPermissionClass
  | requestCallerCeiling
  | requestTargetRequirement
  | requestDelegationChain
  | requestGrant
  | denyInactiveGrant
  | denyExpiredGrant
  | denyRevokedGrant
  | denyScopeMismatch
  | denyOverGrantCeiling
  | requestApproval
  | requestEffectReceipt
  | requestDenialReceipt
  | requestAuditRefs
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | admitAuthorityLifecycle
deriving DecidableEq, Repr

structure AuthorityLifecycleReview where
  authorityRequested : Bool
  principalRecorded : Bool
  operationRecorded : Bool
  permissionClassRecorded : Bool
  callerCeilingRecorded : Bool
  targetRequirementRecorded : Bool
  delegationChainRecorded : Bool
  grantRecorded : Bool
  grantActive : Bool
  grantExpired : Bool
  grantRevoked : Bool
  scopeMatches : Bool
  grantCeilingCoversTarget : Bool
  approvalRequired : Bool
  approvalRecorded : Bool
  effectRequested : Bool
  effectReceiptPlanned : Bool
  denialReceiptPlanned : Bool
  auditRefsRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def AuthorityLifecycleRouteFor
    (review : AuthorityLifecycleReview) : AuthorityLifecycleRoute :=
  if review.authorityRequested = false then
    AuthorityLifecycleRoute.noAuthorityRequested
  else if review.principalRecorded = false then
    AuthorityLifecycleRoute.requestPrincipal
  else if review.operationRecorded = false then
    AuthorityLifecycleRoute.requestOperation
  else if review.permissionClassRecorded = false then
    AuthorityLifecycleRoute.requestPermissionClass
  else if review.callerCeilingRecorded = false then
    AuthorityLifecycleRoute.requestCallerCeiling
  else if review.targetRequirementRecorded = false then
    AuthorityLifecycleRoute.requestTargetRequirement
  else if review.delegationChainRecorded = false then
    AuthorityLifecycleRoute.requestDelegationChain
  else if review.grantRecorded = false then
    AuthorityLifecycleRoute.requestGrant
  else if review.grantActive = false then
    AuthorityLifecycleRoute.denyInactiveGrant
  else if review.grantExpired = true then
    AuthorityLifecycleRoute.denyExpiredGrant
  else if review.grantRevoked = true then
    AuthorityLifecycleRoute.denyRevokedGrant
  else if review.scopeMatches = false then
    AuthorityLifecycleRoute.denyScopeMismatch
  else if review.grantCeilingCoversTarget = false then
    AuthorityLifecycleRoute.denyOverGrantCeiling
  else if review.approvalRequired = true ∧ review.approvalRecorded = false then
    AuthorityLifecycleRoute.requestApproval
  else if review.effectRequested = true ∧ review.effectReceiptPlanned = false then
    AuthorityLifecycleRoute.requestEffectReceipt
  else if review.effectRequested = false ∧ review.denialReceiptPlanned = false then
    AuthorityLifecycleRoute.requestDenialReceipt
  else if review.auditRefsRecorded = false then
    AuthorityLifecycleRoute.requestAuditRefs
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    AuthorityLifecycleRoute.requestEvidenceTransition
  else if review.nonClaimBoundaryRecorded = false then
    AuthorityLifecycleRoute.preserveNonClaimBoundary
  else
    AuthorityLifecycleRoute.admitAuthorityLifecycle

def completeAuthorityLifecycleReview : AuthorityLifecycleReview :=
  { authorityRequested := true,
    principalRecorded := true,
    operationRecorded := true,
    permissionClassRecorded := true,
    callerCeilingRecorded := true,
    targetRequirementRecorded := true,
    delegationChainRecorded := true,
    grantRecorded := true,
    grantActive := true,
    grantExpired := false,
    grantRevoked := false,
    scopeMatches := true,
    grantCeilingCoversTarget := true,
    approvalRequired := true,
    approvalRecorded := true,
    effectRequested := true,
    effectReceiptPlanned := true,
    denialReceiptPlanned := true,
    auditRefsRecorded := true,
    supportPromotionRequested := true,
    evidenceTransitionRecorded := true,
    nonClaimBoundaryRecorded := true }

theorem no_authority_request_stays_idle
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.noAuthorityRequested := by
  intro noRequest
  unfold AuthorityLifecycleRouteFor
  simp [noRequest]

theorem missing_principal_requests_principal
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestPrincipal := by
  intro requested missingPrincipal
  unfold AuthorityLifecycleRouteFor
  simp [requested, missingPrincipal]

theorem missing_operation_requests_operation
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestOperation := by
  intro requested principal missingOperation
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, missingOperation]

theorem missing_permission_class_requests_permission_class
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestPermissionClass := by
  intro requested principal operation missingPermission
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, missingPermission]

theorem missing_caller_ceiling_requests_caller_ceiling
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestCallerCeiling := by
  intro requested principal operation permission missingCeiling
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, missingCeiling]

theorem missing_target_requirement_requests_target_requirement
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestTargetRequirement := by
  intro requested principal operation permission callerCeiling missingTarget
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling,
    missingTarget]

theorem missing_delegation_chain_requests_delegation_chain
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestDelegationChain := by
  intro requested principal operation permission callerCeiling target
    missingDelegation
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    missingDelegation]

theorem missing_grant_requests_grant_record
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestGrant := by
  intro requested principal operation permission callerCeiling target
    delegation missingGrant
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, missingGrant]

theorem inactive_grant_denies_authority_lifecycle
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.denyInactiveGrant := by
  intro requested principal operation permission callerCeiling target
    delegation grant missingActive
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, missingActive]

theorem expired_grant_denies_authority_lifecycle
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = true ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.denyExpiredGrant := by
  intro requested principal operation permission callerCeiling target
    delegation grant active expired
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, expired]

theorem revoked_grant_denies_authority_lifecycle
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = true ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.denyRevokedGrant := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh revoked
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, revoked]

theorem scope_mismatch_denies_authority_lifecycle
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = false ->
    review.scopeMatches = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.denyScopeMismatch := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh notRevoked scopeMismatch
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, notRevoked, scopeMismatch]

theorem grant_ceiling_gap_denies_authority_lifecycle
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = false ->
    review.scopeMatches = true ->
    review.grantCeilingCoversTarget = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.denyOverGrantCeiling := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh notRevoked scopeMatches ceilingGap
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, notRevoked, scopeMatches, ceilingGap]

theorem required_approval_gap_requests_approval
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = false ->
    review.scopeMatches = true ->
    review.grantCeilingCoversTarget = true ->
    review.approvalRequired = true ->
    review.approvalRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestApproval := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh notRevoked scopeMatches ceilingCovers
    approvalRequired missingApproval
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, notRevoked, scopeMatches, ceilingCovers,
    approvalRequired, missingApproval]

theorem missing_effect_receipt_requests_effect_receipt
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = false ->
    review.scopeMatches = true ->
    review.grantCeilingCoversTarget = true ->
    review.approvalRequired = false ->
    review.effectRequested = true ->
    review.effectReceiptPlanned = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestEffectReceipt := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh notRevoked scopeMatches ceilingCovers
    noApprovalRequired effect missingReceipt
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, notRevoked, scopeMatches, ceilingCovers,
    noApprovalRequired, effect, missingReceipt]

theorem missing_denial_receipt_requests_denial_receipt
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = false ->
    review.scopeMatches = true ->
    review.grantCeilingCoversTarget = true ->
    review.approvalRequired = false ->
    review.effectRequested = false ->
    review.denialReceiptPlanned = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestDenialReceipt := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh notRevoked scopeMatches ceilingCovers
    noApprovalRequired noEffect missingDenialReceipt
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, notRevoked, scopeMatches, ceilingCovers,
    noApprovalRequired, noEffect, missingDenialReceipt]

theorem missing_audit_refs_requests_audit_refs
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = false ->
    review.scopeMatches = true ->
    review.grantCeilingCoversTarget = true ->
    review.approvalRequired = false ->
    review.effectRequested = true ->
    review.effectReceiptPlanned = true ->
    review.auditRefsRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestAuditRefs := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh notRevoked scopeMatches ceilingCovers
    noApprovalRequired effect receipt missingAudit
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, notRevoked, scopeMatches, ceilingCovers,
    noApprovalRequired, effect, receipt, missingAudit]

theorem promotion_request_without_evidence_transition_requests_transition
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = false ->
    review.scopeMatches = true ->
    review.grantCeilingCoversTarget = true ->
    review.approvalRequired = false ->
    review.effectRequested = true ->
    review.effectReceiptPlanned = true ->
    review.auditRefsRecorded = true ->
    review.supportPromotionRequested = true ->
    review.evidenceTransitionRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.requestEvidenceTransition := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh notRevoked scopeMatches ceilingCovers
    noApprovalRequired effect receipt audit promotion missingTransition
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, notRevoked, scopeMatches, ceilingCovers,
    noApprovalRequired, effect, receipt, audit, promotion, missingTransition]

theorem authority_lifecycle_without_nonclaim_boundary_preserves_boundary
    {review : AuthorityLifecycleReview} :
    review.authorityRequested = true ->
    review.principalRecorded = true ->
    review.operationRecorded = true ->
    review.permissionClassRecorded = true ->
    review.callerCeilingRecorded = true ->
    review.targetRequirementRecorded = true ->
    review.delegationChainRecorded = true ->
    review.grantRecorded = true ->
    review.grantActive = true ->
    review.grantExpired = false ->
    review.grantRevoked = false ->
    review.scopeMatches = true ->
    review.grantCeilingCoversTarget = true ->
    review.approvalRequired = false ->
    review.effectRequested = true ->
    review.effectReceiptPlanned = true ->
    review.auditRefsRecorded = true ->
    review.supportPromotionRequested = false ->
    review.nonClaimBoundaryRecorded = false ->
    AuthorityLifecycleRouteFor review =
      AuthorityLifecycleRoute.preserveNonClaimBoundary := by
  intro requested principal operation permission callerCeiling target
    delegation grant active fresh notRevoked scopeMatches ceilingCovers
    noApprovalRequired effect receipt audit noPromotion missingNonClaim
  unfold AuthorityLifecycleRouteFor
  simp [requested, principal, operation, permission, callerCeiling, target,
    delegation, grant, active, fresh, notRevoked, scopeMatches, ceilingCovers,
    noApprovalRequired, effect, receipt, audit, noPromotion, missingNonClaim]

theorem complete_authority_lifecycle_admits_record :
    AuthorityLifecycleRouteFor completeAuthorityLifecycleReview =
      AuthorityLifecycleRoute.admitAuthorityLifecycle := by
  unfold AuthorityLifecycleRouteFor completeAuthorityLifecycleReview
  simp

structure AuthorityRevocationTraceSummary where
  authorityDenialVisible : Bool
  revokedReceiptBlocked : Bool
  expiredApprovalNoMutation : Bool
  scifInactiveApprovalBlocksCommit : Bool
  referenceTraceAuthorityBlockerPreserved : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
  deployedRevocationPropagationNotClaimed : Bool
deriving DecidableEq, Repr

def authorityRevocationTraceSummary :
    AuthorityRevocationTraceSummary where
  authorityDenialVisible := true
  revokedReceiptBlocked := true
  expiredApprovalNoMutation := true
  scifInactiveApprovalBlocksCommit := true
  referenceTraceAuthorityBlockerPreserved := true
  supportStateEffectNone := true
  nonClaimBoundary := true
  deployedRevocationPropagationNotClaimed := true

def AuthorityRevocationTraceValid
    (summary : AuthorityRevocationTraceSummary) : Prop :=
  summary.authorityDenialVisible = true ∧
    summary.revokedReceiptBlocked = true ∧
    summary.expiredApprovalNoMutation = true ∧
    summary.scifInactiveApprovalBlocksCommit = true ∧
    summary.referenceTraceAuthorityBlockerPreserved = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true ∧
    summary.deployedRevocationPropagationNotClaimed = true

theorem authority_revocation_trace_surface_bridge :
    AuthorityRevocationTraceValid authorityRevocationTraceSummary := by
  unfold AuthorityRevocationTraceValid
  unfold authorityRevocationTraceSummary
  simp

/-!
Delegation-chain refinement. This finite model proves attenuation and identity
custody for authored grant records. It does not authenticate principals,
grants, clocks, receipts, revocation inventories, or deployed mediation.
-/

structure DelegationState where
  rootGrantId : Nat
  rootPrincipalId : Nat
  operationId : Nat
  targetId : Nat
  scopeId : Nat
  rootCeiling : AuthorityLevel
  rootEpoch : Nat
  rootExpiresAt : Nat
  currentGrantId : Nat
  currentPrincipalId : Nat
  currentDelegateId : Nat
  currentCeiling : AuthorityLevel
  currentEpoch : Nat
  currentExpiresAt : Nat
  logicalTime : Nat
  revokedGrantIds : List Nat
  depth : Nat
  receiptCount : Nat
  supportAuthority : Bool
  externalEffectAuthority : Bool
deriving DecidableEq, Repr

structure DelegationEvent where
  parentGrantId : Nat
  childGrantId : Nat
  actingPrincipalId : Nat
  childDelegateId : Nat
  operationId : Nat
  targetId : Nat
  scopeId : Nat
  childCeiling : AuthorityLevel
  epoch : Nat
  expiresAt : Nat
  logicalTime : Nat
  delegationReceipt : Bool
  supportPromotionRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

def ValidDelegationEvent
    (state : DelegationState) (event : DelegationEvent) : Prop :=
  event.parentGrantId = state.currentGrantId ∧
    event.actingPrincipalId = state.currentDelegateId ∧
    0 < event.childGrantId ∧
    event.childGrantId ≠ state.currentGrantId ∧
    event.childGrantId ∉ state.revokedGrantIds ∧
    0 < event.childDelegateId ∧
    event.operationId = state.operationId ∧
    event.targetId = state.targetId ∧
    event.scopeId = state.scopeId ∧
    event.childCeiling.rank ≤ state.currentCeiling.rank ∧
    event.epoch = state.currentEpoch ∧
    event.expiresAt ≤ state.currentExpiresAt ∧
    state.logicalTime < event.logicalTime ∧
    event.logicalTime ≤ event.expiresAt ∧
    event.delegationReceipt = true ∧
    event.supportPromotionRequested = false ∧
    event.externalEffectRequested = false

instance delegationEventValidityDecidable
    (state : DelegationState) (event : DelegationEvent) :
    Decidable (ValidDelegationEvent state event) := by
  unfold ValidDelegationEvent
  infer_instance

def ApplyDelegationEvent
    (state : DelegationState) (event : DelegationEvent) : DelegationState :=
  { state with
      currentGrantId := event.childGrantId
      currentPrincipalId := event.actingPrincipalId
      currentDelegateId := event.childDelegateId
      currentCeiling := event.childCeiling
      currentEpoch := event.epoch
      currentExpiresAt := event.expiresAt
      logicalTime := event.logicalTime
      depth := state.depth + 1
      receiptCount := state.receiptCount + 1 }

def DelegationStep
    (state : DelegationState) (event : DelegationEvent) : Option DelegationState :=
  if ValidDelegationEvent state event then
    some (ApplyDelegationEvent state event)
  else
    none

def DelegationRun :
    DelegationState -> List DelegationEvent -> Option DelegationState
  | state, [] => some state
  | state, event :: tail =>
      match DelegationStep state event with
      | none => none
      | some next => DelegationRun next tail

def DelegationTraceValid : DelegationState -> List DelegationEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      ValidDelegationEvent state event ∧
        DelegationTraceValid (ApplyDelegationEvent state event) tail

structure DelegationCustodyPreserved
    (before after : DelegationState) : Prop where
  rootGrantId : after.rootGrantId = before.rootGrantId
  rootPrincipalId : after.rootPrincipalId = before.rootPrincipalId
  operationId : after.operationId = before.operationId
  targetId : after.targetId = before.targetId
  scopeId : after.scopeId = before.scopeId
  rootCeiling : after.rootCeiling = before.rootCeiling
  rootEpoch : after.rootEpoch = before.rootEpoch
  rootExpiresAt : after.rootExpiresAt = before.rootExpiresAt
  ceilingNarrowed : after.currentCeiling.rank ≤ before.currentCeiling.rank
  epochPreserved : after.currentEpoch = before.currentEpoch
  expiryNarrowed : after.currentExpiresAt ≤ before.currentExpiresAt
  supportPreserved : after.supportAuthority = before.supportAuthority
  effectPreserved :
    after.externalEffectAuthority = before.externalEffectAuthority

def DelegationNonAuthority (state : DelegationState) : Prop :=
  state.supportAuthority = false ∧ state.externalEffectAuthority = false

instance delegationNonAuthorityDecidable (state : DelegationState) :
    Decidable (DelegationNonAuthority state) := by
  unfold DelegationNonAuthority
  infer_instance

structure DelegationStateInvariant (state : DelegationState) : Prop where
  rootGrantPositive : 0 < state.rootGrantId
  rootPrincipalPositive : 0 < state.rootPrincipalId
  currentGrantPositive : 0 < state.currentGrantId
  currentPrincipalPositive : 0 < state.currentPrincipalId
  currentDelegatePositive : 0 < state.currentDelegateId
  ceilingWithinRoot : state.currentCeiling.rank ≤ state.rootCeiling.rank
  epochMatchesRoot : state.currentEpoch = state.rootEpoch
  expiryWithinRoot : state.currentExpiresAt ≤ state.rootExpiresAt
  timeWithinCurrentExpiry : state.logicalTime ≤ state.currentExpiresAt
  currentGrantNotRevoked : state.currentGrantId ∉ state.revokedGrantIds
  nonAuthority : DelegationNonAuthority state

theorem delegation_accepted_step_is_valid
    {state next : DelegationState} {event : DelegationEvent}
    (accepted : DelegationStep state event = some next) :
    ValidDelegationEvent state event := by
  unfold DelegationStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem delegation_accepted_step_applies_event
    {state next : DelegationState} {event : DelegationEvent}
    (accepted : DelegationStep state event = some next) :
    next = ApplyDelegationEvent state event := by
  unfold DelegationStep at accepted
  split at accepted
  · exact (Option.some.inj accepted).symm
  · simp at accepted

theorem delegation_rejected_event_is_noninterfering
    {state : DelegationState} {event : DelegationEvent}
    (rejected : DelegationStep state event = none) :
    DelegationStep state event = none ∧ state = state := by
  exact ⟨rejected, rfl⟩

theorem delegation_step_preserves_custody
    {state next : DelegationState} {event : DelegationEvent}
    (accepted : DelegationStep state event = some next) :
    DelegationCustodyPreserved state next := by
  have valid := delegation_accepted_step_is_valid accepted
  have applies := delegation_accepted_step_applies_event accepted
  subst next
  exact {
    rootGrantId := rfl
    rootPrincipalId := rfl
    operationId := rfl
    targetId := rfl
    scopeId := rfl
    rootCeiling := rfl
    rootEpoch := rfl
    rootExpiresAt := rfl
    ceilingNarrowed := valid.2.2.2.2.2.2.2.2.2.1
    epochPreserved := valid.2.2.2.2.2.2.2.2.2.2.1
    expiryNarrowed := valid.2.2.2.2.2.2.2.2.2.2.2.1
    supportPreserved := rfl
    effectPreserved := rfl }

theorem delegation_custody_is_transitive
    {first second third : DelegationState}
    (left : DelegationCustodyPreserved first second)
    (right : DelegationCustodyPreserved second third) :
    DelegationCustodyPreserved first third := by
  exact {
    rootGrantId := right.rootGrantId.trans left.rootGrantId
    rootPrincipalId := right.rootPrincipalId.trans left.rootPrincipalId
    operationId := right.operationId.trans left.operationId
    targetId := right.targetId.trans left.targetId
    scopeId := right.scopeId.trans left.scopeId
    rootCeiling := right.rootCeiling.trans left.rootCeiling
    rootEpoch := right.rootEpoch.trans left.rootEpoch
    rootExpiresAt := right.rootExpiresAt.trans left.rootExpiresAt
    ceilingNarrowed := Nat.le_trans right.ceilingNarrowed left.ceilingNarrowed
    epochPreserved := right.epochPreserved.trans left.epochPreserved
    expiryNarrowed := Nat.le_trans right.expiryNarrowed left.expiryNarrowed
    supportPreserved := right.supportPreserved.trans left.supportPreserved
    effectPreserved := right.effectPreserved.trans left.effectPreserved }

theorem delegation_run_preserves_custody
    {state final : DelegationState} {events : List DelegationEvent}
    (ran : DelegationRun state events = some final) :
    DelegationCustodyPreserved state final := by
  induction events generalizing state with
  | nil =>
      simp [DelegationRun] at ran
      subst final
      exact {
        rootGrantId := rfl
        rootPrincipalId := rfl
        operationId := rfl
        targetId := rfl
        scopeId := rfl
        rootCeiling := rfl
        rootEpoch := rfl
        rootExpiresAt := rfl
        ceilingNarrowed := Nat.le_refl _
        epochPreserved := rfl
        expiryNarrowed := Nat.le_refl _
        supportPreserved := rfl
        effectPreserved := rfl }
  | cons event tail ih =>
      cases stepped : DelegationStep state event with
      | none => simp [DelegationRun, stepped] at ran
      | some next =>
          have tailRan : DelegationRun next tail = some final := by
            simpa [DelegationRun, stepped] using ran
          exact delegation_custody_is_transitive
            (delegation_step_preserves_custody stepped) (ih tailRan)

theorem delegation_step_preserves_non_authority
    {state next : DelegationState} {event : DelegationEvent}
    (bounded : DelegationNonAuthority state)
    (accepted : DelegationStep state event = some next) :
    DelegationNonAuthority next := by
  have applies := delegation_accepted_step_applies_event accepted
  subst next
  exact bounded

theorem delegation_run_preserves_non_authority
    {state final : DelegationState} {events : List DelegationEvent}
    (bounded : DelegationNonAuthority state)
    (ran : DelegationRun state events = some final) :
    DelegationNonAuthority final := by
  induction events generalizing state with
  | nil =>
      simp [DelegationRun] at ran
      subst final
      exact bounded
  | cons event tail ih =>
      cases stepped : DelegationStep state event with
      | none => simp [DelegationRun, stepped] at ran
      | some next =>
          have tailRan : DelegationRun next tail = some final := by
            simpa [DelegationRun, stepped] using ran
          exact ih (delegation_step_preserves_non_authority bounded stepped)
            tailRan

theorem delegation_accepted_step_adds_one_receipt
    {state next : DelegationState} {event : DelegationEvent}
    (accepted : DelegationStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [delegation_accepted_step_applies_event accepted]
  rfl

theorem delegation_accepted_step_adds_one_depth
    {state next : DelegationState} {event : DelegationEvent}
    (accepted : DelegationStep state event = some next) :
    next.depth = state.depth + 1 := by
  rw [delegation_accepted_step_applies_event accepted]
  rfl

theorem delegation_run_composes_across_event_batches
    (state : DelegationState) (left right : List DelegationEvent) :
    DelegationRun state (left ++ right) =
      match DelegationRun state left with
      | none => none
      | some middle => DelegationRun middle right := by
  induction left generalizing state with
  | nil => simp [DelegationRun]
  | cons event tail ih =>
      cases stepped : DelegationStep state event <;>
        simp [DelegationRun, stepped, ih]

theorem delegation_step_preserves_invariant
    {state next : DelegationState} {event : DelegationEvent}
    (safe : DelegationStateInvariant state)
    (accepted : DelegationStep state event = some next) :
    DelegationStateInvariant next := by
  have valid := delegation_accepted_step_is_valid accepted
  have applies := delegation_accepted_step_applies_event accepted
  subst next
  exact {
    rootGrantPositive := safe.rootGrantPositive
    rootPrincipalPositive := safe.rootPrincipalPositive
    currentGrantPositive := valid.2.2.1
    currentPrincipalPositive := by
      simpa [ApplyDelegationEvent, valid.2.1] using safe.currentDelegatePositive
    currentDelegatePositive := valid.2.2.2.2.2.1
    ceilingWithinRoot := Nat.le_trans
      valid.2.2.2.2.2.2.2.2.2.1 safe.ceilingWithinRoot
    epochMatchesRoot := valid.2.2.2.2.2.2.2.2.2.2.1.trans
      safe.epochMatchesRoot
    expiryWithinRoot := Nat.le_trans
      valid.2.2.2.2.2.2.2.2.2.2.2.1 safe.expiryWithinRoot
    timeWithinCurrentExpiry :=
      valid.2.2.2.2.2.2.2.2.2.2.2.2.2.1
    currentGrantNotRevoked := valid.2.2.2.2.1
    nonAuthority := safe.nonAuthority }

theorem delegation_run_preserves_invariant
    {state final : DelegationState} {events : List DelegationEvent}
    (safe : DelegationStateInvariant state)
    (ran : DelegationRun state events = some final) :
    DelegationStateInvariant final := by
  induction events generalizing state with
  | nil =>
      simp [DelegationRun] at ran
      subst final
      exact safe
  | cons event tail ih =>
      cases stepped : DelegationStep state event with
      | none => simp [DelegationRun, stepped] at ran
      | some next =>
          have tailRan : DelegationRun next tail = some final := by
            simpa [DelegationRun, stepped] using ran
          exact ih (delegation_step_preserves_invariant safe stepped) tailRan

theorem delegation_successful_run_has_valid_trace
    {state final : DelegationState} {events : List DelegationEvent}
    (ran : DelegationRun state events = some final) :
    DelegationTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : DelegationStep state event with
      | none => simp [DelegationRun, stepped] at ran
      | some next =>
          have tailRan : DelegationRun next tail = some final := by
            simpa [DelegationRun, stepped] using ran
          have applies := delegation_accepted_step_applies_event stepped
          subst next
          exact ⟨delegation_accepted_step_is_valid stepped, ih tailRan⟩

def delegationInitialState : DelegationState :=
  { rootGrantId := 100
    rootPrincipalId := 1
    operationId := 10
    targetId := 20
    scopeId := 30
    rootCeiling := .approve
    rootEpoch := 7
    rootExpiresAt := 100
    currentGrantId := 100
    currentPrincipalId := 1
    currentDelegateId := 2
    currentCeiling := .execute
    currentEpoch := 7
    currentExpiresAt := 90
    logicalTime := 0
    revokedGrantIds := [99]
    depth := 0
    receiptCount := 0
    supportAuthority := false
    externalEffectAuthority := false }

def firstDelegationEvent : DelegationEvent :=
  { parentGrantId := 100
    childGrantId := 101
    actingPrincipalId := 2
    childDelegateId := 3
    operationId := 10
    targetId := 20
    scopeId := 30
    childCeiling := .write
    epoch := 7
    expiresAt := 80
    logicalTime := 10
    delegationReceipt := true
    supportPromotionRequested := false
    externalEffectRequested := false }

def secondDelegationEvent : DelegationEvent :=
  { parentGrantId := 101
    childGrantId := 102
    actingPrincipalId := 3
    childDelegateId := 4
    operationId := 10
    targetId := 20
    scopeId := 30
    childCeiling := .read
    epoch := 7
    expiresAt := 70
    logicalTime := 20
    delegationReceipt := true
    supportPromotionRequested := false
    externalEffectRequested := false }

def twoHopDelegationTrace : List DelegationEvent :=
  [firstDelegationEvent, secondDelegationEvent]

theorem delegation_initial_state_is_invariant :
    DelegationStateInvariant delegationInitialState := by
  exact {
    rootGrantPositive := by native_decide
    rootPrincipalPositive := by native_decide
    currentGrantPositive := by native_decide
    currentPrincipalPositive := by native_decide
    currentDelegatePositive := by native_decide
    ceilingWithinRoot := by native_decide
    epochMatchesRoot := by native_decide
    expiryWithinRoot := by native_decide
    timeWithinCurrentExpiry := by native_decide
    currentGrantNotRevoked := by native_decide
    nonAuthority := by native_decide }

theorem two_hop_delegation_reaches_attenuated_grandchild :
    ∃ final,
      DelegationRun delegationInitialState twoHopDelegationTrace = some final ∧
        final.currentGrantId = 102 ∧
        final.currentPrincipalId = 3 ∧
        final.currentDelegateId = 4 ∧
        final.currentCeiling = .read ∧
        final.depth = 2 ∧
        final.receiptCount = 2 ∧
        DelegationNonAuthority final := by
  refine ⟨ApplyDelegationEvent
    (ApplyDelegationEvent delegationInitialState firstDelegationEvent)
    secondDelegationEvent, ?_⟩
  native_decide

theorem authority_widening_delegation_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with childCeiling := .approve } = none := by
  native_decide

theorem confused_deputy_principal_substitution_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with actingPrincipalId := 1 } = none := by
  native_decide

theorem delegation_operation_substitution_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with operationId := 11 } = none := by
  native_decide

theorem delegation_target_substitution_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with targetId := 21 } = none := by
  native_decide

theorem delegation_scope_substitution_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with scopeId := 31 } = none := by
  native_decide

theorem stale_epoch_delegation_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with epoch := 6 } = none := by
  native_decide

theorem expiry_widening_delegation_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with expiresAt := 91 } = none := by
  native_decide

theorem revoked_child_grant_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with childGrantId := 99 } = none := by
  native_decide

theorem support_promotion_delegation_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with supportPromotionRequested := true } = none := by
  native_decide

theorem external_effect_delegation_is_rejected :
    DelegationStep delegationInitialState
      { firstDelegationEvent with externalEffectRequested := true } = none := by
  native_decide

structure ThinDelegationSummary where
  ceilingRank : Nat
  expiresAt : Nat
  depth : Nat
deriving DecidableEq, Repr

def ThinDelegationSummaryOf (state : DelegationState) : ThinDelegationSummary :=
  { ceilingRank := state.currentCeiling.rank
    expiresAt := state.currentExpiresAt
    depth := state.depth }

def confusedDeputyDelegationState : DelegationState :=
  { delegationInitialState with currentDelegateId := 5 }

def DelegationDecisionFor (state : DelegationState) : Bool :=
  decide (ValidDelegationEvent state firstDelegationEvent)

theorem thin_delegation_summary_has_authority_collision :
    delegationInitialState ≠ confusedDeputyDelegationState ∧
      ThinDelegationSummaryOf delegationInitialState =
        ThinDelegationSummaryOf confusedDeputyDelegationState ∧
      DelegationDecisionFor delegationInitialState = true ∧
      DelegationDecisionFor confusedDeputyDelegationState = false := by
  native_decide

theorem no_thin_delegation_classifier_recovers_authority
    (classify : ThinDelegationSummary -> Bool) :
    classify (ThinDelegationSummaryOf delegationInitialState) ≠ true ∨
      classify (ThinDelegationSummaryOf confusedDeputyDelegationState) ≠
        false := by
  have collision :
      ThinDelegationSummaryOf delegationInitialState =
        ThinDelegationSummaryOf confusedDeputyDelegationState :=
    thin_delegation_summary_has_authority_collision.2.1
  by_cases admitted :
      classify (ThinDelegationSummaryOf delegationInitialState) = true
  · right
    intro rejected
    have sameClassification := congrArg classify collision
    rw [admitted, rejected] at sameClassification
    contradiction
  · exact Or.inl admitted

structure CompleteDelegationTransport where
  rootGrantId : Nat
  rootPrincipalId : Nat
  operationId : Nat
  targetId : Nat
  scopeId : Nat
  rootCeiling : AuthorityLevel
  rootEpoch : Nat
  rootExpiresAt : Nat
  currentGrantId : Nat
  currentPrincipalId : Nat
  currentDelegateId : Nat
  currentCeiling : AuthorityLevel
  currentEpoch : Nat
  currentExpiresAt : Nat
  logicalTime : Nat
  revokedGrantIds : List Nat
  depth : Nat
  receiptCount : Nat
  supportAuthority : Bool
  externalEffectAuthority : Bool
deriving DecidableEq, Repr

def CompleteDelegationTransportOf
    (state : DelegationState) : CompleteDelegationTransport :=
  { rootGrantId := state.rootGrantId
    rootPrincipalId := state.rootPrincipalId
    operationId := state.operationId
    targetId := state.targetId
    scopeId := state.scopeId
    rootCeiling := state.rootCeiling
    rootEpoch := state.rootEpoch
    rootExpiresAt := state.rootExpiresAt
    currentGrantId := state.currentGrantId
    currentPrincipalId := state.currentPrincipalId
    currentDelegateId := state.currentDelegateId
    currentCeiling := state.currentCeiling
    currentEpoch := state.currentEpoch
    currentExpiresAt := state.currentExpiresAt
    logicalTime := state.logicalTime
    revokedGrantIds := state.revokedGrantIds
    depth := state.depth
    receiptCount := state.receiptCount
    supportAuthority := state.supportAuthority
    externalEffectAuthority := state.externalEffectAuthority }

def DelegationStateOf
    (transport : CompleteDelegationTransport) : DelegationState :=
  { rootGrantId := transport.rootGrantId
    rootPrincipalId := transport.rootPrincipalId
    operationId := transport.operationId
    targetId := transport.targetId
    scopeId := transport.scopeId
    rootCeiling := transport.rootCeiling
    rootEpoch := transport.rootEpoch
    rootExpiresAt := transport.rootExpiresAt
    currentGrantId := transport.currentGrantId
    currentPrincipalId := transport.currentPrincipalId
    currentDelegateId := transport.currentDelegateId
    currentCeiling := transport.currentCeiling
    currentEpoch := transport.currentEpoch
    currentExpiresAt := transport.currentExpiresAt
    logicalTime := transport.logicalTime
    revokedGrantIds := transport.revokedGrantIds
    depth := transport.depth
    receiptCount := transport.receiptCount
    supportAuthority := transport.supportAuthority
    externalEffectAuthority := transport.externalEffectAuthority }

theorem complete_delegation_transport_round_trips
    (state : DelegationState) :
    DelegationStateOf (CompleteDelegationTransportOf state) = state := by
  cases state
  rfl

theorem complete_delegation_transport_is_injective :
    Function.Injective CompleteDelegationTransportOf := by
  intro left right equal
  calc
    left = DelegationStateOf (CompleteDelegationTransportOf left) :=
      (complete_delegation_transport_round_trips left).symm
    _ = DelegationStateOf (CompleteDelegationTransportOf right) :=
      congrArg DelegationStateOf equal
    _ = right := complete_delegation_transport_round_trips right

theorem complete_delegation_transport_preserves_step
    (state : DelegationState) (event : DelegationEvent) :
    DelegationStep
        (DelegationStateOf (CompleteDelegationTransportOf state)) event =
      DelegationStep state event := by
  rw [complete_delegation_transport_round_trips]

end AsiStackProofs.Authority
