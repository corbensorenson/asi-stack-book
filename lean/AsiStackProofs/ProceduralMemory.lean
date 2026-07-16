namespace AsiStackProofs.ProceduralMemory

structure GeneratedToolRecordReview where
  generatedTool : Bool
  sourceTracesPresent : Bool
  parametersPresent : Bool
  verificationResultRecorded : Bool
deriving DecidableEq, Repr

def GeneratedToolHasClosureArtifacts
    (review : GeneratedToolRecordReview) : Prop :=
  review.generatedTool = true ->
    review.sourceTracesPresent = true ∧
      review.parametersPresent = true ∧
        review.verificationResultRecorded = true

theorem generated_tool_missing_closure_artifact_rejected
    {review : GeneratedToolRecordReview} :
    review.generatedTool = true ->
      (review.sourceTracesPresent = false ∨
        review.parametersPresent = false ∨
          review.verificationResultRecorded = false) ->
        ¬ GeneratedToolHasClosureArtifacts review := by
  intro generated missingArtifact valid
  have closure := valid generated
  cases missingArtifact with
  | inl missingSourceTraces =>
      rw [missingSourceTraces] at closure
      cases closure.1
  | inr rest =>
      cases rest with
      | inl missingParameters =>
          rw [missingParameters] at closure
          cases closure.2.1
      | inr missingVerification =>
          rw [missingVerification] at closure
          cases closure.2.2

structure RegressionPromotionReview where
  regressionFailed : Bool
  routableStatusPromoted : Bool
deriving DecidableEq, Repr

def FailedRegressionBlocksRoutablePromotion
    (review : RegressionPromotionReview) : Prop :=
  review.regressionFailed = true ->
    review.routableStatusPromoted = false

theorem failed_regression_with_routable_promotion_rejected
    {review : RegressionPromotionReview} :
    review.regressionFailed = true ->
      review.routableStatusPromoted = true ->
        ¬ FailedRegressionBlocksRoutablePromotion review := by
  intro failed promoted valid
  have blocked := valid failed
  rw [promoted] at blocked
  contradiction

inductive ProcedureLifecycleState where
  | candidate
  | loopCluster
  | toolCandidate
  | verified
  | routable
  | quarantined
  | retired
deriving DecidableEq, Repr

def ProcedureLifecycleState.canRequestRoutable :
    ProcedureLifecycleState -> Bool
  | .verified => true
  | .routable => true
  | _ => false

inductive ProcedureLifecycleRoute where
  | collectComparableTraces
  | preserveNegativeExamples
  | recordClosureArtifacts
  | runVerification
  | quarantineRegressionFailure
  | preserveBenchmarkFloor
  | requireActiveScf
  | retireTriggeredTool
  | requireMonitoringPlan
  | preserveResiduals
  | preserveNonClaims
  | requireVerifiedSourceState
  | admitTransition
deriving DecidableEq, Repr

structure ProcedureTransitionReview where
  fromState : ProcedureLifecycleState
  requestedState : ProcedureLifecycleState
  comparableTraceClusterPresent : Bool
  negativeExamplesPreserved : Bool
  closureArtifactsPresent : Bool
  verificationPassed : Bool
  regressionFailed : Bool
  benchmarkFloorPreserved : Bool
  scfActive : Bool
  retirementTriggered : Bool
  monitoringPlanPresent : Bool
  residualsPreserved : Bool
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def ProcedureLifecycleRouteFor
    (review : ProcedureTransitionReview) : ProcedureLifecycleRoute :=
  if review.requestedState = ProcedureLifecycleState.routable then
    if review.comparableTraceClusterPresent = false then
      ProcedureLifecycleRoute.collectComparableTraces
    else if review.negativeExamplesPreserved = false then
      ProcedureLifecycleRoute.preserveNegativeExamples
    else if review.closureArtifactsPresent = false then
      ProcedureLifecycleRoute.recordClosureArtifacts
    else if review.verificationPassed = false then
      ProcedureLifecycleRoute.runVerification
    else if review.regressionFailed = true then
      ProcedureLifecycleRoute.quarantineRegressionFailure
    else if review.benchmarkFloorPreserved = false then
      ProcedureLifecycleRoute.preserveBenchmarkFloor
    else if review.scfActive = false then
      ProcedureLifecycleRoute.requireActiveScf
    else if review.retirementTriggered = true then
      ProcedureLifecycleRoute.retireTriggeredTool
    else if review.monitoringPlanPresent = false then
      ProcedureLifecycleRoute.requireMonitoringPlan
    else if review.residualsPreserved = false then
      ProcedureLifecycleRoute.preserveResiduals
    else if review.nonClaimsPresent = false then
      ProcedureLifecycleRoute.preserveNonClaims
    else if review.fromState.canRequestRoutable = false then
      ProcedureLifecycleRoute.requireVerifiedSourceState
    else
      ProcedureLifecycleRoute.admitTransition
  else if review.requestedState = ProcedureLifecycleState.verified then
    if review.closureArtifactsPresent = false then
      ProcedureLifecycleRoute.recordClosureArtifacts
    else if review.verificationPassed = false then
      ProcedureLifecycleRoute.runVerification
    else if review.nonClaimsPresent = false then
      ProcedureLifecycleRoute.preserveNonClaims
    else
      ProcedureLifecycleRoute.admitTransition
  else if review.requestedState = ProcedureLifecycleState.quarantined then
    if review.regressionFailed = true ∨ review.verificationPassed = false then
      ProcedureLifecycleRoute.admitTransition
    else
      ProcedureLifecycleRoute.quarantineRegressionFailure
  else if review.requestedState = ProcedureLifecycleState.retired then
    if review.retirementTriggered = true then
      ProcedureLifecycleRoute.admitTransition
    else
      ProcedureLifecycleRoute.retireTriggeredTool
  else
    ProcedureLifecycleRoute.admitTransition

def validRoutableWithNegativeExamplesReview : ProcedureTransitionReview :=
  { fromState := ProcedureLifecycleState.verified
    requestedState := ProcedureLifecycleState.routable
    comparableTraceClusterPresent := true
    negativeExamplesPreserved := true
    closureArtifactsPresent := true
    verificationPassed := true
    regressionFailed := false
    benchmarkFloorPreserved := true
    scfActive := true
    retirementTriggered := false
    monitoringPlanPresent := true
    residualsPreserved := true
    nonClaimsPresent := true }

def validFailedRegressionQuarantinedReview : ProcedureTransitionReview :=
  { fromState := ProcedureLifecycleState.toolCandidate
    requestedState := ProcedureLifecycleState.quarantined
    comparableTraceClusterPresent := true
    negativeExamplesPreserved := true
    closureArtifactsPresent := true
    verificationPassed := false
    regressionFailed := true
    benchmarkFloorPreserved := false
    scfActive := true
    retirementTriggered := false
    monitoringPlanPresent := true
    residualsPreserved := true
    nonClaimsPresent := true }

def validRetiredStalePreconditionReview : ProcedureTransitionReview :=
  { fromState := ProcedureLifecycleState.routable
    requestedState := ProcedureLifecycleState.retired
    comparableTraceClusterPresent := true
    negativeExamplesPreserved := true
    closureArtifactsPresent := true
    verificationPassed := true
    regressionFailed := false
    benchmarkFloorPreserved := false
    scfActive := false
    retirementTriggered := true
    monitoringPlanPresent := true
    residualsPreserved := true
    nonClaimsPresent := true }

theorem routable_missing_comparable_traces_collects_traces
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = false ->
        ProcedureLifecycleRouteFor review =
          ProcedureLifecycleRoute.collectComparableTraces := by
  intro routable missingTraces
  unfold ProcedureLifecycleRouteFor
  simp [routable, missingTraces]

theorem routable_missing_negative_examples_preserves_examples
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = false ->
          ProcedureLifecycleRouteFor review =
            ProcedureLifecycleRoute.preserveNegativeExamples := by
  intro routable tracesPresent missingExamples
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, missingExamples]

theorem routable_missing_closure_artifacts_records_artifacts
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = false ->
            ProcedureLifecycleRouteFor review =
              ProcedureLifecycleRoute.recordClosureArtifacts := by
  intro routable tracesPresent examplesPresent missingClosure
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, missingClosure]

theorem routable_failed_verification_runs_verification
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = false ->
              ProcedureLifecycleRouteFor review =
                ProcedureLifecycleRoute.runVerification := by
  intro routable tracesPresent examplesPresent closurePresent failedVerification
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    failedVerification]

theorem routable_failed_regression_routes_quarantine
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = true ->
              review.regressionFailed = true ->
                ProcedureLifecycleRouteFor review =
                  ProcedureLifecycleRoute.quarantineRegressionFailure := by
  intro routable tracesPresent examplesPresent closurePresent verificationPassed
    regressionFailed
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    verificationPassed, regressionFailed]

theorem routable_missing_benchmark_floor_preserves_floor
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = true ->
              review.regressionFailed = false ->
                review.benchmarkFloorPreserved = false ->
                  ProcedureLifecycleRouteFor review =
                    ProcedureLifecycleRoute.preserveBenchmarkFloor := by
  intro routable tracesPresent examplesPresent closurePresent verificationPassed
    regressionClean missingFloor
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    verificationPassed, regressionClean, missingFloor]

theorem routable_missing_active_scf_requires_scf
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = true ->
              review.regressionFailed = false ->
                review.benchmarkFloorPreserved = true ->
                  review.scfActive = false ->
                    ProcedureLifecycleRouteFor review =
                      ProcedureLifecycleRoute.requireActiveScf := by
  intro routable tracesPresent examplesPresent closurePresent verificationPassed
    regressionClean floorPreserved missingScf
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    verificationPassed, regressionClean, floorPreserved, missingScf]

theorem routable_retirement_trigger_routes_retirement
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = true ->
              review.regressionFailed = false ->
                review.benchmarkFloorPreserved = true ->
                  review.scfActive = true ->
                    review.retirementTriggered = true ->
                      ProcedureLifecycleRouteFor review =
                        ProcedureLifecycleRoute.retireTriggeredTool := by
  intro routable tracesPresent examplesPresent closurePresent verificationPassed
    regressionClean floorPreserved scfActive retirementTriggered
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    verificationPassed, regressionClean, floorPreserved, scfActive,
    retirementTriggered]

theorem routable_missing_monitoring_plan_requires_monitoring
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = true ->
              review.regressionFailed = false ->
                review.benchmarkFloorPreserved = true ->
                  review.scfActive = true ->
                    review.retirementTriggered = false ->
                      review.monitoringPlanPresent = false ->
                        ProcedureLifecycleRouteFor review =
                          ProcedureLifecycleRoute.requireMonitoringPlan := by
  intro routable tracesPresent examplesPresent closurePresent verificationPassed
    regressionClean floorPreserved scfActive noRetirement missingMonitoring
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    verificationPassed, regressionClean, floorPreserved, scfActive,
    noRetirement, missingMonitoring]

theorem routable_missing_residuals_preserves_residuals
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = true ->
              review.regressionFailed = false ->
                review.benchmarkFloorPreserved = true ->
                  review.scfActive = true ->
                    review.retirementTriggered = false ->
                      review.monitoringPlanPresent = true ->
                        review.residualsPreserved = false ->
                          ProcedureLifecycleRouteFor review =
                            ProcedureLifecycleRoute.preserveResiduals := by
  intro routable tracesPresent examplesPresent closurePresent verificationPassed
    regressionClean floorPreserved scfActive noRetirement monitoringPresent
    missingResiduals
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    verificationPassed, regressionClean, floorPreserved, scfActive,
    noRetirement, monitoringPresent, missingResiduals]

theorem routable_missing_non_claims_preserves_non_claims
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = true ->
              review.regressionFailed = false ->
                review.benchmarkFloorPreserved = true ->
                  review.scfActive = true ->
                    review.retirementTriggered = false ->
                      review.monitoringPlanPresent = true ->
                        review.residualsPreserved = true ->
                          review.nonClaimsPresent = false ->
                            ProcedureLifecycleRouteFor review =
                              ProcedureLifecycleRoute.preserveNonClaims := by
  intro routable tracesPresent examplesPresent closurePresent verificationPassed
    regressionClean floorPreserved scfActive noRetirement monitoringPresent
    residualsPresent missingNonClaims
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    verificationPassed, regressionClean, floorPreserved, scfActive,
    noRetirement, monitoringPresent, residualsPresent, missingNonClaims]

theorem unverified_source_state_cannot_become_routable
    {review : ProcedureTransitionReview} :
    review.requestedState = ProcedureLifecycleState.routable ->
      review.comparableTraceClusterPresent = true ->
        review.negativeExamplesPreserved = true ->
          review.closureArtifactsPresent = true ->
            review.verificationPassed = true ->
              review.regressionFailed = false ->
                review.benchmarkFloorPreserved = true ->
                  review.scfActive = true ->
                    review.retirementTriggered = false ->
                      review.monitoringPlanPresent = true ->
                        review.residualsPreserved = true ->
                          review.nonClaimsPresent = true ->
                            review.fromState.canRequestRoutable = false ->
                              ProcedureLifecycleRouteFor review =
                                ProcedureLifecycleRoute.requireVerifiedSourceState := by
  intro routable tracesPresent examplesPresent closurePresent verificationPassed
    regressionClean floorPreserved scfActive noRetirement monitoringPresent
    residualsPresent nonClaims sourceNotVerified
  unfold ProcedureLifecycleRouteFor
  simp [routable, tracesPresent, examplesPresent, closurePresent,
    verificationPassed, regressionClean, floorPreserved, scfActive,
    noRetirement, monitoringPresent, residualsPresent, nonClaims,
    sourceNotVerified]

end AsiStackProofs.ProceduralMemory
