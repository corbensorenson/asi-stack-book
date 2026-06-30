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

end AsiStackProofs.CommandContracts
