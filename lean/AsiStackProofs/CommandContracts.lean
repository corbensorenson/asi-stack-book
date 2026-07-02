namespace AsiStackProofs.CommandContracts

structure CommandContractFields where
  objectivePresent : Bool
  constraintsPresent : Bool
  outputContractPresent : Bool
  verificationPresent : Bool
  failureBehaviorPresent : Bool
deriving DecidableEq, Repr

def CommandContractComplete (fields : CommandContractFields) : Prop :=
  fields.objectivePresent = true ∧
    fields.constraintsPresent = true ∧
      fields.outputContractPresent = true ∧
        fields.verificationPresent = true ∧
          fields.failureBehaviorPresent = true

theorem valid_command_contract_contains_required_interface_fields
    {fields : CommandContractFields} :
    CommandContractComplete fields ->
    fields.objectivePresent = true ∧
      fields.constraintsPresent = true ∧
        fields.outputContractPresent = true ∧
          fields.verificationPresent = true ∧
            fields.failureBehaviorPresent = true := by
  intro complete
  exact complete

theorem missing_required_field_blocks_complete_command_contract
    {fields : CommandContractFields} :
    (fields.objectivePresent = false ∨
      fields.constraintsPresent = false ∨
        fields.outputContractPresent = false ∨
          fields.verificationPresent = false ∨
            fields.failureBehaviorPresent = false) ->
    ¬ CommandContractComplete fields := by
  intro missing complete
  unfold CommandContractComplete at complete
  cases missing with
  | inl objectiveMissing =>
      rw [objectiveMissing] at complete
      cases complete.1
  | inr rest =>
      cases rest with
      | inl constraintsMissing =>
          rw [constraintsMissing] at complete
          cases complete.2.1
      | inr rest =>
          cases rest with
          | inl outputMissing =>
              rw [outputMissing] at complete
              cases complete.2.2.1
          | inr rest =>
              cases rest with
              | inl verificationMissing =>
                  rw [verificationMissing] at complete
                  cases complete.2.2.2.1
              | inr failureMissing =>
                  rw [failureMissing] at complete
                  cases complete.2.2.2.2

structure ConstraintOverrideReview where
  explicitConstraintPresent : Bool
  hiddenOrConflictingInstructionPresent : Bool
  hiddenOverrideAccepted : Bool
deriving DecidableEq, Repr

def ExplicitConstraintPrecedence (review : ConstraintOverrideReview) : Prop :=
  review.explicitConstraintPresent = true ->
    review.hiddenOrConflictingInstructionPresent = true ->
      review.hiddenOverrideAccepted = false

theorem hidden_or_conflicting_instruction_cannot_override_explicit_constraint
    {review : ConstraintOverrideReview} :
    ExplicitConstraintPrecedence review ->
    review.explicitConstraintPresent = true ->
    review.hiddenOrConflictingInstructionPresent = true ->
    review.hiddenOverrideAccepted = false := by
  intro valid explicitPresent hiddenPresent
  exact valid explicitPresent hiddenPresent

theorem accepted_hidden_override_violates_explicit_constraint_precedence
    {review : ConstraintOverrideReview} :
    review.explicitConstraintPresent = true ->
    review.hiddenOrConflictingInstructionPresent = true ->
    review.hiddenOverrideAccepted = true ->
    ¬ ExplicitConstraintPrecedence review := by
  intro explicitPresent hiddenPresent overrideAccepted precedence
  have rejected := precedence explicitPresent hiddenPresent
  rw [overrideAccepted] at rejected
  cases rejected

inductive FieldConfidence where
  | confirmed
  | policyImposed
  | sourceDerived
  | defaulted
  | inferred
  | missing
deriving DecidableEq, Repr

def FieldConfidence.dispatchEligible : FieldConfidence -> Bool
  | .confirmed => true
  | .policyImposed => true
  | .sourceDerived => true
  | .defaulted => true
  | .inferred => false
  | .missing => false

inductive FieldConfidenceRoute where
  | requireObjectiveConfidence
  | requireConstraintConfidence
  | requireAuthorityConfidence
  | requireOutputConfidence
  | requireVerificationConfidence
  | requireFailureConfidence
  | dispatchAllowed
  | noDispatchRequested
deriving DecidableEq, Repr

structure FieldConfidenceReview where
  objective : FieldConfidence
  constraints : FieldConfidence
  authority : FieldConfidence
  output : FieldConfidence
  verification : FieldConfidence
  failureBehavior : FieldConfidence
  dispatchRequested : Bool
deriving DecidableEq, Repr

def FieldConfidenceRouteFor
    (review : FieldConfidenceReview) : FieldConfidenceRoute :=
  if review.objective.dispatchEligible = false then
    FieldConfidenceRoute.requireObjectiveConfidence
  else if review.constraints.dispatchEligible = false then
    FieldConfidenceRoute.requireConstraintConfidence
  else if review.authority.dispatchEligible = false then
    FieldConfidenceRoute.requireAuthorityConfidence
  else if review.output.dispatchEligible = false then
    FieldConfidenceRoute.requireOutputConfidence
  else if review.verification.dispatchEligible = false then
    FieldConfidenceRoute.requireVerificationConfidence
  else if review.failureBehavior.dispatchEligible = false then
    FieldConfidenceRoute.requireFailureConfidence
  else if review.dispatchRequested = true then
    FieldConfidenceRoute.dispatchAllowed
  else
    FieldConfidenceRoute.noDispatchRequested

theorem inferred_authority_confidence_requires_authority_confidence
    {review : FieldConfidenceReview} :
    review.objective = FieldConfidence.confirmed ->
      review.constraints = FieldConfidence.confirmed ->
        review.authority = FieldConfidence.inferred ->
          FieldConfidenceRouteFor review =
            FieldConfidenceRoute.requireAuthorityConfidence := by
  intro objectiveConfirmed constraintsConfirmed inferredAuthority
  unfold FieldConfidenceRouteFor
  simp [objectiveConfirmed, constraintsConfirmed, inferredAuthority,
    FieldConfidence.dispatchEligible]

theorem missing_output_confidence_requires_output_confidence
    {review : FieldConfidenceReview} :
    review.objective = FieldConfidence.confirmed ->
      review.constraints = FieldConfidence.confirmed ->
        review.authority = FieldConfidence.confirmed ->
          review.output = FieldConfidence.missing ->
            FieldConfidenceRouteFor review =
              FieldConfidenceRoute.requireOutputConfidence := by
  intro objectiveConfirmed constraintsConfirmed authorityConfirmed missingOutput
  unfold FieldConfidenceRouteFor
  simp [objectiveConfirmed, constraintsConfirmed, authorityConfirmed,
    missingOutput, FieldConfidence.dispatchEligible]

theorem complete_field_confidence_allows_dispatch
    {review : FieldConfidenceReview} :
    review.objective = FieldConfidence.confirmed ->
      review.constraints = FieldConfidence.policyImposed ->
        review.authority = FieldConfidence.confirmed ->
          review.output = FieldConfidence.confirmed ->
            review.verification = FieldConfidence.confirmed ->
              review.failureBehavior = FieldConfidence.confirmed ->
                review.dispatchRequested = true ->
                  FieldConfidenceRouteFor review =
                    FieldConfidenceRoute.dispatchAllowed := by
  intro objectiveConfirmed constraintsPolicy authorityConfirmed outputConfirmed
    verificationConfirmed failureConfirmed dispatchRequested
  unfold FieldConfidenceRouteFor
  simp [objectiveConfirmed, constraintsPolicy, authorityConfirmed,
    outputConfirmed, verificationConfirmed, failureConfirmed, dispatchRequested,
    FieldConfidence.dispatchEligible]

end AsiStackProofs.CommandContracts
