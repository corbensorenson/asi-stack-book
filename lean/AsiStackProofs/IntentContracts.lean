namespace AsiStackProofs.IntentContracts

structure IntentCompilationReview where
  constraintsDeclared : Bool
  stopConditionsDeclared : Bool
  compiledConstraintsPreserved : Bool
  compiledStopConditionsPreserved : Bool
deriving DecidableEq, Repr

def CompiledIntentPreservesDeclaredFields (review : IntentCompilationReview) : Prop :=
  (review.constraintsDeclared = true ->
    review.compiledConstraintsPreserved = true) ∧
      (review.stopConditionsDeclared = true ->
        review.compiledStopConditionsPreserved = true)

theorem compiled_intent_contract_preserves_declared_constraints_and_stop_conditions
    {review : IntentCompilationReview} :
    CompiledIntentPreservesDeclaredFields review ->
    review.constraintsDeclared = true ->
    review.stopConditionsDeclared = true ->
    review.compiledConstraintsPreserved = true ∧
      review.compiledStopConditionsPreserved = true := by
  intro valid constraintsDeclared stopConditionsDeclared
  exact ⟨valid.1 constraintsDeclared, valid.2 stopConditionsDeclared⟩

structure AuthorityCompilationReview where
  requiredAuthority : Bool
  requiredAuthorityPresent : Bool
  executableJobCompiled : Bool
deriving DecidableEq, Repr

def MissingRequiredAuthorityBlocksExecutableJob
    (review : AuthorityCompilationReview) : Prop :=
  review.requiredAuthority = true ->
    review.requiredAuthorityPresent = false ->
      review.executableJobCompiled = false

theorem contract_missing_required_authority_cannot_compile_to_executable_job
    {review : AuthorityCompilationReview} :
    MissingRequiredAuthorityBlocksExecutableJob review ->
    review.requiredAuthority = true ->
    review.requiredAuthorityPresent = false ->
    review.executableJobCompiled = false := by
  intro valid authorityRequired authorityMissing
  exact valid authorityRequired authorityMissing

inductive IntentResolutionRoute where
  | compileCommand
  | requestClarification
  | requestReview
  | rejectAsNonExecutable
deriving DecidableEq, Repr

structure IntentResolutionRecord where
  intentTextPresent : Bool
  ambiguousTermsPresent : Bool
  highImpact : Bool
  authorityGrantPresent : Bool
  reversible : Bool
  nonGoalConflictPresent : Bool
  prohibitedActionRequested : Bool
deriving DecidableEq, Repr

def IntentResolutionRouteFor
    (record : IntentResolutionRecord) : IntentResolutionRoute :=
  if record.intentTextPresent = false then
    IntentResolutionRoute.rejectAsNonExecutable
  else if record.prohibitedActionRequested = true then
    IntentResolutionRoute.rejectAsNonExecutable
  else if record.ambiguousTermsPresent = true then
    IntentResolutionRoute.requestClarification
  else if record.nonGoalConflictPresent = true then
    IntentResolutionRoute.requestClarification
  else if record.highImpact = true ∧ record.authorityGrantPresent = false then
    IntentResolutionRoute.requestReview
  else if record.highImpact = true ∧ record.reversible = false then
    IntentResolutionRoute.requestReview
  else
    IntentResolutionRoute.compileCommand

theorem missing_intent_text_rejects_as_non_executable
    {record : IntentResolutionRecord} :
    record.intentTextPresent = false ->
    IntentResolutionRouteFor record =
      IntentResolutionRoute.rejectAsNonExecutable := by
  intro missingText
  unfold IntentResolutionRouteFor
  simp [missingText]

theorem prohibited_action_rejects_as_non_executable
    {record : IntentResolutionRecord} :
    record.intentTextPresent = true ->
    record.prohibitedActionRequested = true ->
    IntentResolutionRouteFor record =
      IntentResolutionRoute.rejectAsNonExecutable := by
  intro textPresent prohibited
  unfold IntentResolutionRouteFor
  simp [textPresent, prohibited]

theorem ambiguous_intent_routes_to_clarification
    {record : IntentResolutionRecord} :
    record.intentTextPresent = true ->
    record.prohibitedActionRequested = false ->
    record.ambiguousTermsPresent = true ->
    IntentResolutionRouteFor record =
      IntentResolutionRoute.requestClarification := by
  intro textPresent notProhibited ambiguous
  unfold IntentResolutionRouteFor
  simp [textPresent, notProhibited, ambiguous]

theorem non_goal_conflict_routes_to_clarification
    {record : IntentResolutionRecord} :
    record.intentTextPresent = true ->
    record.prohibitedActionRequested = false ->
    record.ambiguousTermsPresent = false ->
    record.nonGoalConflictPresent = true ->
    IntentResolutionRouteFor record =
      IntentResolutionRoute.requestClarification := by
  intro textPresent notProhibited unambiguous conflict
  unfold IntentResolutionRouteFor
  simp [textPresent, notProhibited, unambiguous, conflict]

theorem high_impact_without_authority_routes_to_review
    {record : IntentResolutionRecord} :
    record.intentTextPresent = true ->
    record.prohibitedActionRequested = false ->
    record.ambiguousTermsPresent = false ->
    record.nonGoalConflictPresent = false ->
    record.highImpact = true ->
    record.authorityGrantPresent = false ->
    IntentResolutionRouteFor record =
      IntentResolutionRoute.requestReview := by
  intro textPresent notProhibited unambiguous noConflict highImpact noAuthority
  unfold IntentResolutionRouteFor
  simp [textPresent, notProhibited, unambiguous, noConflict, highImpact,
    noAuthority]

theorem irreversible_high_impact_routes_to_review
    {record : IntentResolutionRecord} :
    record.intentTextPresent = true ->
    record.prohibitedActionRequested = false ->
    record.ambiguousTermsPresent = false ->
    record.nonGoalConflictPresent = false ->
    record.highImpact = true ->
    record.authorityGrantPresent = true ->
    record.reversible = false ->
    IntentResolutionRouteFor record =
      IntentResolutionRoute.requestReview := by
  intro textPresent notProhibited unambiguous noConflict highImpact hasAuthority
    irreversible
  unfold IntentResolutionRouteFor
  simp [textPresent, notProhibited, unambiguous, noConflict, highImpact,
    hasAuthority, irreversible]

inductive IntentAdmissionRoute where
  | rejectAsNonExecutable
  | rejectHiddenOverride
  | requestClarification
  | requestAuthorityReview
  | repairPreservation
  | requestRecontract
  | blockForNonClaimBoundary
  | admitContract
deriving DecidableEq, Repr

structure IntentAdmissionReview where
  rawIntentPresent : Bool
  prohibitedActionRequested : Bool
  hiddenOverridePresent : Bool
  ambiguousTermsPresent : Bool
  clarificationResolved : Bool
  constraintsDeclared : Bool
  constraintPrecedencePreserved : Bool
  compiledConstraintsPreserved : Bool
  stopConditionsDeclared : Bool
  compiledStopConditionsPreserved : Bool
  authorityDeclared : Bool
  authorityWithinCeiling : Bool
  downstreamChangeExpandsMeans : Bool
  downstreamChangeExpandsAuthority : Bool
  downstreamChangeDropsEvidence : Bool
  downstreamChangeDropsStopCondition : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def IntentAdmissionRouteFor
    (review : IntentAdmissionReview) : IntentAdmissionRoute :=
  if review.rawIntentPresent = false then
    IntentAdmissionRoute.rejectAsNonExecutable
  else if review.prohibitedActionRequested = true then
    IntentAdmissionRoute.rejectAsNonExecutable
  else if review.hiddenOverridePresent = true then
    IntentAdmissionRoute.rejectHiddenOverride
  else if review.ambiguousTermsPresent = true ∧
      review.clarificationResolved = false then
    IntentAdmissionRoute.requestClarification
  else if review.constraintsDeclared = false then
    IntentAdmissionRoute.requestClarification
  else if review.constraintPrecedencePreserved = false then
    IntentAdmissionRoute.repairPreservation
  else if review.compiledConstraintsPreserved = false then
    IntentAdmissionRoute.repairPreservation
  else if review.stopConditionsDeclared = false then
    IntentAdmissionRoute.requestClarification
  else if review.compiledStopConditionsPreserved = false then
    IntentAdmissionRoute.repairPreservation
  else if review.authorityDeclared = false then
    IntentAdmissionRoute.requestAuthorityReview
  else if review.authorityWithinCeiling = false then
    IntentAdmissionRoute.requestAuthorityReview
  else if review.downstreamChangeExpandsMeans = true then
    IntentAdmissionRoute.requestRecontract
  else if review.downstreamChangeExpandsAuthority = true then
    IntentAdmissionRoute.requestRecontract
  else if review.downstreamChangeDropsEvidence = true then
    IntentAdmissionRoute.requestRecontract
  else if review.downstreamChangeDropsStopCondition = true then
    IntentAdmissionRoute.requestRecontract
  else if review.nonClaimBoundaryPresent = false then
    IntentAdmissionRoute.blockForNonClaimBoundary
  else
    IntentAdmissionRoute.admitContract

theorem intent_admission_missing_raw_intent_rejects
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.rejectAsNonExecutable := by
  intro missingIntent
  unfold IntentAdmissionRouteFor
  simp [missingIntent]

theorem intent_admission_hidden_override_rejects
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = true ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.rejectHiddenOverride := by
  intro rawPresent notProhibited hiddenOverride
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, hiddenOverride]

theorem unresolved_ambiguity_requests_clarification
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = true ->
    review.clarificationResolved = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.requestClarification := by
  intro rawPresent notProhibited noHiddenOverride ambiguous unresolved
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, ambiguous, unresolved]

theorem missing_declared_constraints_requests_clarification
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.requestClarification := by
  intro rawPresent notProhibited noHiddenOverride unambiguous missingConstraints
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    missingConstraints]

theorem constraint_precedence_gap_blocks_admission
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.repairPreservation := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedenceGap
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedenceGap]

theorem compiled_constraint_gap_blocks_admission
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.repairPreservation := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved compiledGap
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, compiledGap]

theorem missing_stop_conditions_requests_clarification
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = true ->
    review.stopConditionsDeclared = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.requestClarification := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved constraintsPreserved missingStop
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, constraintsPreserved, missingStop]

theorem compiled_stop_condition_gap_blocks_admission
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = true ->
    review.stopConditionsDeclared = true ->
    review.compiledStopConditionsPreserved = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.repairPreservation := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved constraintsPreserved stopDeclared
    stopGap
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, constraintsPreserved, stopDeclared,
    stopGap]

theorem missing_authority_declaration_requests_review
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = true ->
    review.stopConditionsDeclared = true ->
    review.compiledStopConditionsPreserved = true ->
    review.authorityDeclared = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.requestAuthorityReview := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved constraintsPreserved stopDeclared
    stopPreserved missingAuthority
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, constraintsPreserved, stopDeclared,
    stopPreserved, missingAuthority]

theorem authority_widening_requests_review
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = true ->
    review.stopConditionsDeclared = true ->
    review.compiledStopConditionsPreserved = true ->
    review.authorityDeclared = true ->
    review.authorityWithinCeiling = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.requestAuthorityReview := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved constraintsPreserved stopDeclared
    stopPreserved authorityDeclared authorityWidening
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, constraintsPreserved, stopDeclared,
    stopPreserved, authorityDeclared, authorityWidening]

theorem downstream_means_change_requires_recontract
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = true ->
    review.stopConditionsDeclared = true ->
    review.compiledStopConditionsPreserved = true ->
    review.authorityDeclared = true ->
    review.authorityWithinCeiling = true ->
    review.downstreamChangeExpandsMeans = true ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.requestRecontract := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved constraintsPreserved stopDeclared
    stopPreserved authorityDeclared authorityWithin meansChange
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, constraintsPreserved, stopDeclared,
    stopPreserved, authorityDeclared, authorityWithin, meansChange]

theorem downstream_stop_condition_change_requires_recontract
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = true ->
    review.stopConditionsDeclared = true ->
    review.compiledStopConditionsPreserved = true ->
    review.authorityDeclared = true ->
    review.authorityWithinCeiling = true ->
    review.downstreamChangeExpandsMeans = false ->
    review.downstreamChangeExpandsAuthority = false ->
    review.downstreamChangeDropsEvidence = false ->
    review.downstreamChangeDropsStopCondition = true ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.requestRecontract := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved constraintsPreserved stopDeclared
    stopPreserved authorityDeclared authorityWithin noMeansChange
    noAuthorityChange noEvidenceDrop stopDrop
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, constraintsPreserved, stopDeclared,
    stopPreserved, authorityDeclared, authorityWithin, noMeansChange,
    noAuthorityChange, noEvidenceDrop, stopDrop]

theorem missing_nonclaim_boundary_blocks_intent_admission
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = true ->
    review.stopConditionsDeclared = true ->
    review.compiledStopConditionsPreserved = true ->
    review.authorityDeclared = true ->
    review.authorityWithinCeiling = true ->
    review.downstreamChangeExpandsMeans = false ->
    review.downstreamChangeExpandsAuthority = false ->
    review.downstreamChangeDropsEvidence = false ->
    review.downstreamChangeDropsStopCondition = false ->
    review.nonClaimBoundaryPresent = false ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.blockForNonClaimBoundary := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved constraintsPreserved stopDeclared
    stopPreserved authorityDeclared authorityWithin noMeansChange
    noAuthorityChange noEvidenceDrop noStopDrop missingBoundary
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, constraintsPreserved, stopDeclared,
    stopPreserved, authorityDeclared, authorityWithin, noMeansChange,
    noAuthorityChange, noEvidenceDrop, noStopDrop, missingBoundary]

theorem complete_intent_admission_admits_contract
    {review : IntentAdmissionReview} :
    review.rawIntentPresent = true ->
    review.prohibitedActionRequested = false ->
    review.hiddenOverridePresent = false ->
    review.ambiguousTermsPresent = false ->
    review.constraintsDeclared = true ->
    review.constraintPrecedencePreserved = true ->
    review.compiledConstraintsPreserved = true ->
    review.stopConditionsDeclared = true ->
    review.compiledStopConditionsPreserved = true ->
    review.authorityDeclared = true ->
    review.authorityWithinCeiling = true ->
    review.downstreamChangeExpandsMeans = false ->
    review.downstreamChangeExpandsAuthority = false ->
    review.downstreamChangeDropsEvidence = false ->
    review.downstreamChangeDropsStopCondition = false ->
    review.nonClaimBoundaryPresent = true ->
    IntentAdmissionRouteFor review =
      IntentAdmissionRoute.admitContract := by
  intro rawPresent notProhibited noHiddenOverride unambiguous
    constraintsDeclared precedencePreserved constraintsPreserved stopDeclared
    stopPreserved authorityDeclared authorityWithin noMeansChange
    noAuthorityChange noEvidenceDrop noStopDrop boundaryPresent
  unfold IntentAdmissionRouteFor
  simp [rawPresent, notProhibited, noHiddenOverride, unambiguous,
    constraintsDeclared, precedencePreserved, constraintsPreserved, stopDeclared,
    stopPreserved, authorityDeclared, authorityWithin, noMeansChange,
    noAuthorityChange, noEvidenceDrop, noStopDrop, boundaryPresent]

end AsiStackProofs.IntentContracts
