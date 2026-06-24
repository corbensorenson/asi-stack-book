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

end AsiStackProofs.CommandContracts
