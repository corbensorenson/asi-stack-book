namespace AsiStackProofs.ContextCertificates

inductive AuthorityLevel where
  | publicUse
  | draftingUse
  | citationUse
  | executionUse
  | restrictedUse
deriving DecidableEq, Repr

def AuthorityLevel.rank : AuthorityLevel -> Nat
  | .publicUse => 0
  | .draftingUse => 1
  | .citationUse => 2
  | .executionUse => 3
  | .restrictedUse => 4

structure ContextCellCertificate where
  derived : Bool
  sourceBindingsDeclared : Bool
  lossContractDeclared : Bool
  permittedUsesDeclared : Bool
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

def CertificateComplete (certificate : ContextCellCertificate) : Prop :=
  certificate.sourceBindingsDeclared = true ∧
    certificate.lossContractDeclared = true ∧
    certificate.permittedUsesDeclared = true

def DerivedCellValid (certificate : ContextCellCertificate) : Prop :=
  certificate.derived = true ->
    CertificateComplete certificate

structure SourceCell where
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

structure SummaryCell where
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

def SummaryRespectsSourceAuthority
    (summary : SummaryCell) (sources : List SourceCell) : Prop :=
  ∀ source, source ∈ sources ->
    summary.authorityCeiling.rank <= source.authorityCeiling.rank

def AuthorityEscalates
    (summary : SummaryCell) (source : SourceCell) : Prop :=
  source.authorityCeiling.rank < summary.authorityCeiling.rank

theorem authority_preservation_rejects_escalating_summary
    {summary : SummaryCell} {sources : List SourceCell} {source : SourceCell} :
    SummaryRespectsSourceAuthority summary sources ->
    source ∈ sources ->
    ¬ AuthorityEscalates summary source := by
  intro respects member escalates
  unfold AuthorityEscalates at escalates
  have bounded :
      summary.authorityCeiling.rank <= source.authorityCeiling.rank :=
    respects source member
  exact (Nat.not_lt_of_ge bounded) escalates

inductive CertificateLifecycleRoute where
  | rejectCertificate
  | requireSourceBindings
  | requireLossContract
  | requirePermittedUses
  | requireAuthorityReview
  | requireOmissionRecord
  | requireScopeReview
  | requireFreshnessReview
  | blockRevokedCertificate
  | quarantineTaintedCertificate
  | requireDeletionClosureEvidence
  | requireVerifierReferences
  | requireConsumerPolicyReview
  | requireEvidenceTransition
  | admitCertificate
deriving DecidableEq, Repr

structure CertificateLifecycleReview where
  wellFormed : Bool
  sourceBindingsDeclared : Bool
  lossContractDeclared : Bool
  permittedUsesDeclared : Bool
  authorityWithinSources : Bool
  omissionsDeclared : Bool
  scopeWithinPermittedUse : Bool
  certificateFresh : Bool
  revoked : Bool
  taintDetected : Bool
  deletionClosureRequired : Bool
  deletionClosureEvidenceDeclared : Bool
  verifierReferencesDeclared : Bool
  consumerUsePermitted : Bool
  supportPromotionRequested : Bool
  evidenceTransitionDeclared : Bool
deriving DecidableEq, Repr

def CertificateLifecycleRouteFor
    (review : CertificateLifecycleReview) : CertificateLifecycleRoute :=
  if review.wellFormed = false then
    CertificateLifecycleRoute.rejectCertificate
  else if review.sourceBindingsDeclared = false then
    CertificateLifecycleRoute.requireSourceBindings
  else if review.lossContractDeclared = false then
    CertificateLifecycleRoute.requireLossContract
  else if review.permittedUsesDeclared = false then
    CertificateLifecycleRoute.requirePermittedUses
  else if review.authorityWithinSources = false then
    CertificateLifecycleRoute.requireAuthorityReview
  else if review.omissionsDeclared = false then
    CertificateLifecycleRoute.requireOmissionRecord
  else if review.scopeWithinPermittedUse = false then
    CertificateLifecycleRoute.requireScopeReview
  else if review.certificateFresh = false then
    CertificateLifecycleRoute.requireFreshnessReview
  else if review.revoked = true then
    CertificateLifecycleRoute.blockRevokedCertificate
  else if review.taintDetected = true then
    CertificateLifecycleRoute.quarantineTaintedCertificate
  else if review.deletionClosureRequired = true ∧
      review.deletionClosureEvidenceDeclared = false then
    CertificateLifecycleRoute.requireDeletionClosureEvidence
  else if review.verifierReferencesDeclared = false then
    CertificateLifecycleRoute.requireVerifierReferences
  else if review.consumerUsePermitted = false then
    CertificateLifecycleRoute.requireConsumerPolicyReview
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionDeclared = false then
    CertificateLifecycleRoute.requireEvidenceTransition
  else
    CertificateLifecycleRoute.admitCertificate

theorem malformed_certificate_rejects
    {review : CertificateLifecycleReview} :
    review.wellFormed = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.rejectCertificate := by
  intro malformed
  unfold CertificateLifecycleRouteFor
  simp [malformed]

theorem missing_source_bindings_require_source_bindings
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireSourceBindings := by
  intro wellFormed missingBindings
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, missingBindings]

theorem missing_loss_contract_requires_loss_contract
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireLossContract := by
  intro wellFormed bindingsDeclared missingLoss
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, missingLoss]

theorem missing_permitted_uses_require_use_contract
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requirePermittedUses := by
  intro wellFormed bindingsDeclared lossDeclared missingUses
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, missingUses]

theorem authority_escape_requires_certificate_authority_review
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireAuthorityReview := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityEscape
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityEscape]

theorem undeclared_omissions_require_omission_record
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireOmissionRecord := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    missingOmissions
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, missingOmissions]

theorem out_of_scope_certificate_requires_scope_review
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireScopeReview := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeEscape
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeEscape]

theorem stale_certificate_requires_freshness_review
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = true ->
    review.certificateFresh = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireFreshnessReview := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeWithin stale
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeWithin, stale]

theorem revoked_certificate_blocks_admission
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = true ->
    review.certificateFresh = true ->
    review.revoked = true ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.blockRevokedCertificate := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeWithin fresh revoked
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeWithin, fresh, revoked]

theorem tainted_certificate_quarantines
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = true ->
    review.certificateFresh = true ->
    review.revoked = false ->
    review.taintDetected = true ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.quarantineTaintedCertificate := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeWithin fresh notRevoked tainted
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeWithin, fresh, notRevoked,
    tainted]

theorem deletion_closure_request_requires_declared_evidence
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = true ->
    review.certificateFresh = true ->
    review.revoked = false ->
    review.taintDetected = false ->
    review.deletionClosureRequired = true ->
    review.deletionClosureEvidenceDeclared = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireDeletionClosureEvidence := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeWithin fresh notRevoked clean deletionRequired
    missingDeletionEvidence
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeWithin, fresh, notRevoked,
    clean, deletionRequired, missingDeletionEvidence]

theorem missing_verifier_references_require_verifier_refs
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = true ->
    review.certificateFresh = true ->
    review.revoked = false ->
    review.taintDetected = false ->
    review.deletionClosureRequired = false ->
    review.verifierReferencesDeclared = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireVerifierReferences := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeWithin fresh notRevoked clean deletionNotRequired
    missingVerifiers
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeWithin, fresh, notRevoked,
    clean, deletionNotRequired, missingVerifiers]

theorem unpermitted_consumer_use_requires_policy_review
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = true ->
    review.certificateFresh = true ->
    review.revoked = false ->
    review.taintDetected = false ->
    review.deletionClosureRequired = false ->
    review.verifierReferencesDeclared = true ->
    review.consumerUsePermitted = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireConsumerPolicyReview := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeWithin fresh notRevoked clean deletionNotRequired
    verifiersDeclared useNotPermitted
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeWithin, fresh, notRevoked,
    clean, deletionNotRequired, verifiersDeclared, useNotPermitted]

theorem support_promotion_requires_evidence_transition
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = true ->
    review.certificateFresh = true ->
    review.revoked = false ->
    review.taintDetected = false ->
    review.deletionClosureRequired = false ->
    review.verifierReferencesDeclared = true ->
    review.consumerUsePermitted = true ->
    review.supportPromotionRequested = true ->
    review.evidenceTransitionDeclared = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.requireEvidenceTransition := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeWithin fresh notRevoked clean deletionNotRequired
    verifiersDeclared usePermitted promotionRequested missingTransition
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeWithin, fresh, notRevoked,
    clean, deletionNotRequired, verifiersDeclared, usePermitted,
    promotionRequested, missingTransition]

theorem complete_certificate_lifecycle_review_admits
    {review : CertificateLifecycleReview} :
    review.wellFormed = true ->
    review.sourceBindingsDeclared = true ->
    review.lossContractDeclared = true ->
    review.permittedUsesDeclared = true ->
    review.authorityWithinSources = true ->
    review.omissionsDeclared = true ->
    review.scopeWithinPermittedUse = true ->
    review.certificateFresh = true ->
    review.revoked = false ->
    review.taintDetected = false ->
    review.deletionClosureRequired = false ->
    review.verifierReferencesDeclared = true ->
    review.consumerUsePermitted = true ->
    review.supportPromotionRequested = false ->
    CertificateLifecycleRouteFor review =
      CertificateLifecycleRoute.admitCertificate := by
  intro wellFormed bindingsDeclared lossDeclared usesDeclared authorityWithin
    omissionsDeclared scopeWithin fresh notRevoked clean deletionNotRequired
    verifiersDeclared usePermitted noPromotion
  unfold CertificateLifecycleRouteFor
  simp [wellFormed, bindingsDeclared, lossDeclared, usesDeclared,
    authorityWithin, omissionsDeclared, scopeWithin, fresh, notRevoked,
    clean, deletionNotRequired, verifiersDeclared, usePermitted, noPromotion]

end AsiStackProofs.ContextCertificates
