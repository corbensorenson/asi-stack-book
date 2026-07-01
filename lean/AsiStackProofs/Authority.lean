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

theorem valid_authority_decision_has_audit_and_nonclaims
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.auditRefsPresent = true ∧ record.nonClaimsPresent = true := by
  intro valid
  exact valid.1

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

end AsiStackProofs.Authority
