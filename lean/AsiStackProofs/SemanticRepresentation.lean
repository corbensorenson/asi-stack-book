namespace AsiStackProofs.SemanticRepresentation

inductive GroundingState where
  | grounded
  | partiallyGrounded
  | speculative
  | deprecated
  | superseded
deriving DecidableEq, Repr

structure SemanticNodeRecord where
  groundingState : GroundingState
  provenanceLinkCount : Nat
deriving DecidableEq, Repr

def GroundedNodeHasProvenance (record : SemanticNodeRecord) : Prop :=
  record.groundingState = GroundingState.grounded -> record.provenanceLinkCount > 0

theorem grounded_semantic_node_without_provenance_rejected
    {record : SemanticNodeRecord} :
    record.groundingState = GroundingState.grounded ->
    record.provenanceLinkCount = 0 ->
    ¬ GroundedNodeHasProvenance record := by
  intro grounded noProvenance valid
  have provenance := valid grounded
  rw [noProvenance] at provenance
  cases provenance

structure HierarchyUpdateRecord where
  updateApplied : Bool
  priorReferencesPreserved : Bool
  supersessionRecorded : Bool
deriving DecidableEq, Repr

def HierarchyUpdateAccounted (record : HierarchyUpdateRecord) : Prop :=
  record.priorReferencesPreserved = true ∨ record.supersessionRecorded = true

def HierarchyUpdateValid (record : HierarchyUpdateRecord) : Prop :=
  record.updateApplied = true -> HierarchyUpdateAccounted record

theorem hierarchy_update_without_references_or_supersession_rejected
    {record : HierarchyUpdateRecord} :
    record.updateApplied = true ->
    record.priorReferencesPreserved = false ->
    record.supersessionRecorded = false ->
    ¬ HierarchyUpdateValid record := by
  intro applied referencesMissing supersessionMissing valid
  have accounted := valid applied
  cases accounted with
  | inl referencesPreserved =>
      rw [referencesMissing] at referencesPreserved
      cases referencesPreserved
  | inr supersessionRecorded =>
      rw [supersessionMissing] at supersessionRecorded
      cases supersessionRecorded

end AsiStackProofs.SemanticRepresentation
