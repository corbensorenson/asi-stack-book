namespace AsiStackProofs.VirtualContextABI

structure ContextReference where
  semanticAddress : String
  version : String
  snapshotId : String
deriving DecidableEq, Repr

structure SnapshotBinding where
  semanticAddress : String
  version : String
  snapshotId : String
deriving DecidableEq, Repr

def ReferenceMatchesBinding
    (reference : ContextReference) (binding : SnapshotBinding) : Prop :=
  binding.semanticAddress = reference.semanticAddress ∧
    binding.version = reference.version ∧
    binding.snapshotId = reference.snapshotId

def SnapshotContains
    (reference : ContextReference) (bindings : List SnapshotBinding) : Prop :=
  ∃ binding, binding ∈ bindings ∧ ReferenceMatchesBinding reference binding

inductive ResolutionState where
  | resolved
  | miss
deriving DecidableEq, Repr

structure ResolutionRecord where
  reference : ContextReference
  bindings : List SnapshotBinding
  state : ResolutionState
deriving DecidableEq, Repr

def ResolutionValid (record : ResolutionRecord) : Prop :=
  record.state = ResolutionState.resolved ->
    SnapshotContains record.reference record.bindings

inductive FaultState where
  | none
  | typedFault
  | residual
  | quarantine
deriving DecidableEq, Repr

structure LookupRecord where
  mandatory : Bool
  resolved : Bool
  faultState : FaultState
  materializationEmitted : Bool
deriving DecidableEq, Repr

def MandatoryMissHandled (lookup : LookupRecord) : Prop :=
  lookup.mandatory = true ->
    lookup.resolved = false ->
    lookup.faultState = FaultState.typedFault ∧
      lookup.materializationEmitted = false

inductive ContextAdmissionRoute where
  | rejectRequest
  | requestContext
  | requireAuthorityReview
  | issueTypedFault
  | requireCertificate
  | requireRefresh
  | quarantineContext
  | requireAdequacyReview
  | recordResidual
  | materializeContext
deriving DecidableEq, Repr

structure ContextAdmissionReview where
  requestWellFormed : Bool
  addressDeclared : Bool
  versionDeclared : Bool
  authorityWithinRequest : Bool
  contextAvailable : Bool
  mandatory : Bool
  certificateRequired : Bool
  certificatePresent : Bool
  certificateFresh : Bool
  taintDetected : Bool
  adequacyRequired : Bool
  adequacyPassed : Bool
  residualKnown : Bool
  materializationRequested : Bool
deriving DecidableEq, Repr

def ContextAdmissionRouteFor
    (review : ContextAdmissionReview) : ContextAdmissionRoute :=
  if review.requestWellFormed = false then
    ContextAdmissionRoute.rejectRequest
  else if review.addressDeclared = false then
    ContextAdmissionRoute.requestContext
  else if review.versionDeclared = false then
    ContextAdmissionRoute.requestContext
  else if review.authorityWithinRequest = false then
    ContextAdmissionRoute.requireAuthorityReview
  else if review.contextAvailable = false ∧ review.mandatory = true then
    ContextAdmissionRoute.issueTypedFault
  else if review.contextAvailable = false then
    ContextAdmissionRoute.requestContext
  else if review.certificateRequired = true ∧
      review.certificatePresent = false then
    ContextAdmissionRoute.requireCertificate
  else if review.certificateRequired = true ∧
      review.certificateFresh = false then
    ContextAdmissionRoute.requireRefresh
  else if review.taintDetected = true then
    ContextAdmissionRoute.quarantineContext
  else if review.adequacyRequired = true ∧ review.adequacyPassed = false then
    ContextAdmissionRoute.requireAdequacyReview
  else if review.residualKnown = true then
    ContextAdmissionRoute.recordResidual
  else if review.materializationRequested = true then
    ContextAdmissionRoute.materializeContext
  else
    ContextAdmissionRoute.requestContext

theorem malformed_context_request_rejects
    {review : ContextAdmissionReview} :
    review.requestWellFormed = false ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.rejectRequest := by
  intro malformed
  unfold ContextAdmissionRouteFor
  simp [malformed]

theorem missing_address_requests_context
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = false ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.requestContext := by
  intro wellFormed missingAddress
  unfold ContextAdmissionRouteFor
  simp [wellFormed, missingAddress]

theorem authority_escape_requires_context_authority_review
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = false ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.requireAuthorityReview := by
  intro wellFormed addressDeclared versionDeclared authorityEscape
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityEscape]

theorem mandatory_absent_context_issues_typed_fault
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = true ->
    review.contextAvailable = false ->
    review.mandatory = true ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.issueTypedFault := by
  intro wellFormed addressDeclared versionDeclared authorityWithin
    contextAbsent mandatory
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityWithin,
    contextAbsent, mandatory]

theorem optional_absent_context_requests_context
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = true ->
    review.contextAvailable = false ->
    review.mandatory = false ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.requestContext := by
  intro wellFormed addressDeclared versionDeclared authorityWithin
    contextAbsent optional
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityWithin,
    contextAbsent, optional]

theorem missing_certificate_requires_certificate
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = true ->
    review.contextAvailable = true ->
    review.certificateRequired = true ->
    review.certificatePresent = false ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.requireCertificate := by
  intro wellFormed addressDeclared versionDeclared authorityWithin
    contextAvailable certificateRequired missingCertificate
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityWithin,
    contextAvailable, certificateRequired, missingCertificate]

theorem stale_certificate_requires_refresh
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = true ->
    review.contextAvailable = true ->
    review.certificateRequired = true ->
    review.certificatePresent = true ->
    review.certificateFresh = false ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.requireRefresh := by
  intro wellFormed addressDeclared versionDeclared authorityWithin
    contextAvailable certificateRequired certificatePresent staleCertificate
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityWithin,
    contextAvailable, certificateRequired, certificatePresent, staleCertificate]

theorem tainted_context_quarantines
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = true ->
    review.contextAvailable = true ->
    review.certificateRequired = false ->
    review.taintDetected = true ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.quarantineContext := by
  intro wellFormed addressDeclared versionDeclared authorityWithin
    contextAvailable certificateNotRequired tainted
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityWithin,
    contextAvailable, certificateNotRequired, tainted]

theorem failed_adequacy_requires_adequacy_review
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = true ->
    review.contextAvailable = true ->
    review.certificateRequired = false ->
    review.taintDetected = false ->
    review.adequacyRequired = true ->
    review.adequacyPassed = false ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.requireAdequacyReview := by
  intro wellFormed addressDeclared versionDeclared authorityWithin
    contextAvailable certificateNotRequired clean adequacyRequired
    adequacyFailed
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityWithin,
    contextAvailable, certificateNotRequired, clean, adequacyRequired,
    adequacyFailed]

theorem known_context_residual_records_residual
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = true ->
    review.contextAvailable = true ->
    review.certificateRequired = false ->
    review.taintDetected = false ->
    review.adequacyRequired = false ->
    review.residualKnown = true ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.recordResidual := by
  intro wellFormed addressDeclared versionDeclared authorityWithin
    contextAvailable certificateNotRequired clean adequacyNotRequired
    residualKnown
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityWithin,
    contextAvailable, certificateNotRequired, clean, adequacyNotRequired,
    residualKnown]

theorem complete_context_review_materializes
    {review : ContextAdmissionReview} :
    review.requestWellFormed = true ->
    review.addressDeclared = true ->
    review.versionDeclared = true ->
    review.authorityWithinRequest = true ->
    review.contextAvailable = true ->
    review.certificateRequired = false ->
    review.taintDetected = false ->
    review.adequacyRequired = false ->
    review.residualKnown = false ->
    review.materializationRequested = true ->
    ContextAdmissionRouteFor review =
      ContextAdmissionRoute.materializeContext := by
  intro wellFormed addressDeclared versionDeclared authorityWithin
    contextAvailable certificateNotRequired clean adequacyNotRequired
    noResidual materializationRequested
  unfold ContextAdmissionRouteFor
  simp [wellFormed, addressDeclared, versionDeclared, authorityWithin,
    contextAvailable, certificateNotRequired, clean, adequacyNotRequired,
    noResidual, materializationRequested]

end AsiStackProofs.VirtualContextABI
