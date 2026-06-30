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

end AsiStackProofs.IntentContracts
