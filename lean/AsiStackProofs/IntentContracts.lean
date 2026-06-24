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

end AsiStackProofs.IntentContracts
