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

theorem grounded_semantic_node_has_provenance_link
    {record : SemanticNodeRecord} :
    GroundedNodeHasProvenance record ->
    record.groundingState = GroundingState.grounded ->
    record.provenanceLinkCount > 0 := by
  intro valid grounded
  exact valid grounded

structure HierarchyUpdateRecord where
  updateApplied : Bool
  priorReferencesPreserved : Bool
  supersessionRecorded : Bool
deriving DecidableEq, Repr

def HierarchyUpdateAccounted (record : HierarchyUpdateRecord) : Prop :=
  record.priorReferencesPreserved = true ∨ record.supersessionRecorded = true

def HierarchyUpdateValid (record : HierarchyUpdateRecord) : Prop :=
  record.updateApplied = true -> HierarchyUpdateAccounted record

theorem hierarchy_update_preserves_references_or_records_supersession
    {record : HierarchyUpdateRecord} :
    HierarchyUpdateValid record ->
    record.updateApplied = true ->
    record.priorReferencesPreserved = true ∨ record.supersessionRecorded = true := by
  intro valid applied
  exact valid applied

end AsiStackProofs.SemanticRepresentation
