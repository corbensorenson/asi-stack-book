namespace AsiStackProofs.ReferenceArchitecture

inductive ReferenceTraceRoute where
  | acceptedTrace
  | repairParentage
  | repairAuthorityDelta
  | preserveResidual
  | blockForGovernance
  | requireValidation
deriving DecidableEq, Repr

structure ReferenceTraceRouteReview where
  parentArtifactsComplete : Bool
  authorityDeltasPresent : Bool
  residualDeltasPresent : Bool
  governanceGateRequired : Bool
  governanceGatePresent : Bool
  validationCommandPresent : Bool
deriving DecidableEq, Repr

def ReferenceTraceRouteFor (review : ReferenceTraceRouteReview) : ReferenceTraceRoute :=
  if review.parentArtifactsComplete = false then
    ReferenceTraceRoute.repairParentage
  else if review.authorityDeltasPresent = false then
    ReferenceTraceRoute.repairAuthorityDelta
  else if review.residualDeltasPresent = false then
    ReferenceTraceRoute.preserveResidual
  else if review.governanceGateRequired = true ∧ review.governanceGatePresent = false then
    ReferenceTraceRoute.blockForGovernance
  else if review.validationCommandPresent = false then
    ReferenceTraceRoute.requireValidation
  else
    ReferenceTraceRoute.acceptedTrace

theorem trace_missing_parent_artifacts_routes_to_parentage_repair
    {review : ReferenceTraceRouteReview} :
    review.parentArtifactsComplete = false ->
    ReferenceTraceRouteFor review = ReferenceTraceRoute.repairParentage := by
  intro missingParentage
  unfold ReferenceTraceRouteFor
  simp [missingParentage]

theorem trace_missing_authority_deltas_routes_to_authority_repair
    {review : ReferenceTraceRouteReview} :
    review.parentArtifactsComplete = true ->
    review.authorityDeltasPresent = false ->
    ReferenceTraceRouteFor review = ReferenceTraceRoute.repairAuthorityDelta := by
  intro parentagePresent missingAuthorityDeltas
  unfold ReferenceTraceRouteFor
  simp [parentagePresent, missingAuthorityDeltas]

theorem trace_missing_residual_deltas_routes_to_residual_preservation
    {review : ReferenceTraceRouteReview} :
    review.parentArtifactsComplete = true ->
    review.authorityDeltasPresent = true ->
    review.residualDeltasPresent = false ->
    ReferenceTraceRouteFor review = ReferenceTraceRoute.preserveResidual := by
  intro parentagePresent authorityDeltasPresent missingResidualDeltas
  unfold ReferenceTraceRouteFor
  simp [parentagePresent, authorityDeltasPresent, missingResidualDeltas]

theorem trace_missing_required_governance_gate_blocks_trace
    {review : ReferenceTraceRouteReview} :
    review.parentArtifactsComplete = true ->
    review.authorityDeltasPresent = true ->
    review.residualDeltasPresent = true ->
    review.governanceGateRequired = true ->
    review.governanceGatePresent = false ->
    ReferenceTraceRouteFor review = ReferenceTraceRoute.blockForGovernance := by
  intro parentagePresent authorityDeltasPresent residualDeltasPresent gateRequired gateMissing
  unfold ReferenceTraceRouteFor
  simp [parentagePresent, authorityDeltasPresent, residualDeltasPresent, gateRequired, gateMissing]

theorem trace_missing_validation_command_requires_validation
    {review : ReferenceTraceRouteReview} :
    review.parentArtifactsComplete = true ->
    review.authorityDeltasPresent = true ->
    review.residualDeltasPresent = true ->
    review.governanceGateRequired = false ->
    review.validationCommandPresent = false ->
    ReferenceTraceRouteFor review = ReferenceTraceRoute.requireValidation := by
  intro parentagePresent authorityDeltasPresent residualDeltasPresent gateNotRequired missingValidation
  unfold ReferenceTraceRouteFor
  simp [parentagePresent, authorityDeltasPresent, residualDeltasPresent, gateNotRequired, missingValidation]

end AsiStackProofs.ReferenceArchitecture
