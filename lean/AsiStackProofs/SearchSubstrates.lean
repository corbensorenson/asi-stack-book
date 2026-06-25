namespace AsiStackProofs.SearchSubstrates

structure SubstrateAdoptionRecord where
  baselineRefsPresent : Bool
  measuredTargetDeclared : Bool
  falsificationCriterionDeclared : Bool
deriving DecidableEq, Repr

def AdoptionFieldsComplete (record : SubstrateAdoptionRecord) : Prop :=
  record.baselineRefsPresent = true ∧
    record.measuredTargetDeclared = true ∧
      record.falsificationCriterionDeclared = true

theorem substrate_adoption_record_includes_baseline_measured_target_and_falsification
    {record : SubstrateAdoptionRecord} :
    AdoptionFieldsComplete record ->
    record.baselineRefsPresent = true ∧
      record.measuredTargetDeclared = true ∧
        record.falsificationCriterionDeclared = true := by
  intro complete
  exact complete

inductive AdoptionState where
  | exploratory
  | blocked
  | canary
  | qualified
  | retired
  | refuted
deriving DecidableEq, Repr

def NonCoreState : AdoptionState -> Prop
  | .exploratory => True
  | .blocked => True
  | .canary => True
  | .retired => True
  | .refuted => True
  | .qualified => False

structure SubstratePromotionReview where
  passingEvidence : Bool
  adoptionState : AdoptionState
deriving DecidableEq, Repr

def UnprovenSubstrateRemainsNonCore (review : SubstratePromotionReview) : Prop :=
  review.passingEvidence = false -> NonCoreState review.adoptionState

theorem substrate_without_passing_evidence_remains_non_core
    {review : SubstratePromotionReview} :
    UnprovenSubstrateRemainsNonCore review ->
    review.passingEvidence = false ->
      NonCoreState review.adoptionState := by
  intro valid noEvidence
  exact valid noEvidence

def CoreAdoptionValid (review : SubstratePromotionReview) : Prop :=
  review.adoptionState = AdoptionState.qualified -> review.passingEvidence = true

theorem qualified_substrate_requires_passing_evidence
    {review : SubstratePromotionReview} :
    CoreAdoptionValid review ->
    review.adoptionState = AdoptionState.qualified ->
      review.passingEvidence = true := by
  intro valid qualified
  exact valid qualified

end AsiStackProofs.SearchSubstrates
