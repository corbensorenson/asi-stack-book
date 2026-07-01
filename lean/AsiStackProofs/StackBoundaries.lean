namespace AsiStackProofs.StackBoundaries

structure Layer where
  hasExternalActionAuthority : Bool
deriving DecidableEq, Repr

structure Handoff where
  authorized : Bool
deriving DecidableEq, Repr

inductive LayerOutput where
  | internalArtifact
  | externalAction (handoff : Handoff)
deriving DecidableEq, Repr

def ExternalActionAllowed (layer : Layer) : LayerOutput -> Prop
  | .internalArtifact => True
  | .externalAction handoff =>
      layer.hasExternalActionAuthority = true ∨ handoff.authorized = true

theorem layer_without_external_authority_requires_authorized_handoff
    {layer : Layer} {handoff : Handoff} :
    layer.hasExternalActionAuthority = false ->
    ExternalActionAllowed layer (.externalAction handoff) ->
    handoff.authorized = true := by
  intro noAuthority allowed
  cases allowed with
  | inl hasAuthority =>
      rw [noAuthority] at hasAuthority
      contradiction
  | inr authorized =>
      exact authorized

structure StackTraceStep where
  layer : Layer
  output : LayerOutput
deriving DecidableEq, Repr

def StackTraceValid (trace : List StackTraceStep) : Prop :=
  ∀ step, step ∈ trace -> ExternalActionAllowed step.layer step.output

theorem valid_stack_trace_rejects_unauthorized_external_handoff
    {trace : List StackTraceStep} {layer : Layer} {handoff : Handoff} :
    ({ layer := layer, output := .externalAction handoff } : StackTraceStep) ∈ trace ->
    layer.hasExternalActionAuthority = false ->
    handoff.authorized = false ->
    ¬ StackTraceValid trace := by
  intro present noAuthority unauthorized validTrace
  unfold StackTraceValid at validTrace
  have allowed :=
    validTrace ({ layer := layer, output := .externalAction handoff } : StackTraceStep) present
  have authorized :=
    layer_without_external_authority_requires_authorized_handoff noAuthority allowed
  rw [unauthorized] at authorized
  contradiction

inductive AuthorityLevel where
  | none
  | read
  | write
  | execute
  | admin
deriving DecidableEq, Repr

def AuthorityLevel.rank : AuthorityLevel -> Nat
  | .none => 0
  | .read => 1
  | .write => 2
  | .execute => 3
  | .admin => 4

structure HandoffRequest where
  callerCeiling : AuthorityLevel
  requested : AuthorityLevel
deriving DecidableEq, Repr

def HandoffAccepted (request : HandoffRequest) : Prop :=
  request.requested.rank <= request.callerCeiling.rank

theorem handoff_exceeding_caller_ceiling_rejected
    {request : HandoffRequest} :
    request.callerCeiling.rank < request.requested.rank ->
    ¬ HandoffAccepted request := by
  intro exceeds accepted
  exact Nat.not_le_of_gt exceeds accepted

inductive LayerContractAdmissionRoute where
  | noLayerContractRequested
  | requestLayerIdentity
  | requestLifecycleState
  | requestOwner
  | requestResponsibility
  | requestInputArtifacts
  | requestOutputArtifacts
  | requestAuthorityCeiling
  | requestHandoffProtocol
  | requestInvariant
  | requestFailureMode
  | requestEvidenceGate
  | blockExternalActionBoundary
  | requestSourceMapping
  | requestSupportBoundary
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | admitLayerContract
deriving DecidableEq, Repr

structure LayerContractAdmissionReview where
  contractRequested : Bool
  layerIdRecorded : Bool
  lifecycleStateRecorded : Bool
  ownerRecorded : Bool
  responsibilityRecorded : Bool
  inputArtifactsRecorded : Bool
  outputArtifactsRecorded : Bool
  authorityCeilingRecorded : Bool
  handoffProtocolRecorded : Bool
  invariantRecorded : Bool
  failureModeRecorded : Bool
  evidenceGateRecorded : Bool
  externalActionPossible : Bool
  externalActionAuthorityRecorded : Bool
  authorizedHandoffRecorded : Bool
  sourceMappingRecorded : Bool
  supportStateEffectRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def LayerContractAdmissionRouteFor
    (review : LayerContractAdmissionReview) :
    LayerContractAdmissionRoute :=
  if review.contractRequested = false then
    .noLayerContractRequested
  else if review.layerIdRecorded = false then
    .requestLayerIdentity
  else if review.lifecycleStateRecorded = false then
    .requestLifecycleState
  else if review.ownerRecorded = false then
    .requestOwner
  else if review.responsibilityRecorded = false then
    .requestResponsibility
  else if review.inputArtifactsRecorded = false then
    .requestInputArtifacts
  else if review.outputArtifactsRecorded = false then
    .requestOutputArtifacts
  else if review.authorityCeilingRecorded = false then
    .requestAuthorityCeiling
  else if review.handoffProtocolRecorded = false then
    .requestHandoffProtocol
  else if review.invariantRecorded = false then
    .requestInvariant
  else if review.failureModeRecorded = false then
    .requestFailureMode
  else if review.evidenceGateRecorded = false then
    .requestEvidenceGate
  else if review.externalActionPossible = true ∧
      review.externalActionAuthorityRecorded = false ∧
        review.authorizedHandoffRecorded = false then
    .blockExternalActionBoundary
  else if review.sourceMappingRecorded = false then
    .requestSourceMapping
  else if review.supportStateEffectRecorded = false then
    .requestSupportBoundary
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    .requestEvidenceTransition
  else if review.nonClaimBoundaryRecorded = false then
    .preserveNonClaimBoundary
  else
    .admitLayerContract

def completeLayerContractAdmissionReview :
    LayerContractAdmissionReview := {
  contractRequested := true
  layerIdRecorded := true
  lifecycleStateRecorded := true
  ownerRecorded := true
  responsibilityRecorded := true
  inputArtifactsRecorded := true
  outputArtifactsRecorded := true
  authorityCeilingRecorded := true
  handoffProtocolRecorded := true
  invariantRecorded := true
  failureModeRecorded := true
  evidenceGateRecorded := true
  externalActionPossible := false
  externalActionAuthorityRecorded := true
  authorizedHandoffRecorded := true
  sourceMappingRecorded := true
  supportStateEffectRecorded := true
  supportPromotionRequested := false
  evidenceTransitionRecorded := true
  nonClaimBoundaryRecorded := true
}

theorem no_layer_contract_request_stays_idle :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        contractRequested := false } =
      .noLayerContractRequested := by
  simp [LayerContractAdmissionRouteFor]

theorem missing_layer_identity_requests_identity :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        layerIdRecorded := false } =
      .requestLayerIdentity := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_lifecycle_state_requests_lifecycle :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        lifecycleStateRecorded := false } =
      .requestLifecycleState := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_owner_requests_owner :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        ownerRecorded := false } =
      .requestOwner := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_responsibility_requests_responsibility :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        responsibilityRecorded := false } =
      .requestResponsibility := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_input_artifacts_requests_input_artifacts :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        inputArtifactsRecorded := false } =
      .requestInputArtifacts := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_output_artifacts_requests_output_artifacts :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        outputArtifactsRecorded := false } =
      .requestOutputArtifacts := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_authority_ceiling_requests_ceiling :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        authorityCeilingRecorded := false } =
      .requestAuthorityCeiling := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_handoff_protocol_requests_protocol :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        handoffProtocolRecorded := false } =
      .requestHandoffProtocol := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_invariant_requests_invariant :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        invariantRecorded := false } =
      .requestInvariant := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_failure_mode_requests_failure_mode :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        failureModeRecorded := false } =
      .requestFailureMode := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_evidence_gate_requests_evidence_gate :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        evidenceGateRecorded := false } =
      .requestEvidenceGate := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem possible_external_action_without_authority_or_handoff_blocks_contract :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        externalActionPossible := true
        externalActionAuthorityRecorded := false
        authorizedHandoffRecorded := false } =
      .blockExternalActionBoundary := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_source_mapping_requests_mapping :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        sourceMappingRecorded := false } =
      .requestSourceMapping := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem missing_support_state_effect_requests_boundary :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        supportStateEffectRecorded := false } =
      .requestSupportBoundary := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem promotion_request_without_stack_evidence_transition_requests_transition :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        supportPromotionRequested := true
        evidenceTransitionRecorded := false } =
      .requestEvidenceTransition := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem layer_contract_without_nonclaim_boundary_preserves_boundary :
    LayerContractAdmissionRouteFor
      { completeLayerContractAdmissionReview with
        nonClaimBoundaryRecorded := false } =
      .preserveNonClaimBoundary := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

theorem complete_layer_contract_admission_allows_contract :
    LayerContractAdmissionRouteFor completeLayerContractAdmissionReview =
      .admitLayerContract := by
  simp [LayerContractAdmissionRouteFor, completeLayerContractAdmissionReview]

end AsiStackProofs.StackBoundaries
