namespace AsiStackProofs.ArtifactGraph

inductive ProvenanceStatus where
  | complete
  | incomplete
  | missing
  | blocked
deriving DecidableEq, Repr

structure ArtifactRecord where
  produced : Bool
  parentJobPresent : Bool
  sourceRefsPresent : Bool
  contextRefsPresent : Bool
  provenanceStatus : ProvenanceStatus
deriving DecidableEq, Repr

def ProducedArtifactTraceable (record : ArtifactRecord) : Prop :=
  record.produced = true ->
    record.parentJobPresent = true ∧
      record.sourceRefsPresent = true ∧
        record.contextRefsPresent = true

theorem produced_artifact_records_parent_job_and_context_refs
    {record : ArtifactRecord} :
    ProducedArtifactTraceable record ->
    record.produced = true ->
      record.parentJobPresent = true ∧
        record.sourceRefsPresent = true ∧
          record.contextRefsPresent = true := by
  intro traceable produced
  exact traceable produced

def RequiredProvenanceComplete (record : ArtifactRecord) : Prop :=
  record.parentJobPresent = true ∧
    record.sourceRefsPresent = true ∧
      record.contextRefsPresent = true ∧
        record.provenanceStatus = ProvenanceStatus.complete

def PromotedClaimSupportAllowed (record : ArtifactRecord) : Prop :=
  record.produced = true ∧ RequiredProvenanceComplete record

theorem missing_required_provenance_blocks_promoted_claim_support
    {record : ArtifactRecord} :
    (record.parentJobPresent = false ∨
      record.sourceRefsPresent = false ∨
        record.contextRefsPresent = false ∨
          record.provenanceStatus = ProvenanceStatus.missing) ->
    ¬ PromotedClaimSupportAllowed record := by
  intro missing promoted
  unfold PromotedClaimSupportAllowed RequiredProvenanceComplete at promoted
  cases missing with
  | inl parentMissing =>
      rw [parentMissing] at promoted
      cases promoted.2.1
  | inr rest =>
      cases rest with
      | inl sourceMissing =>
          rw [sourceMissing] at promoted
          cases promoted.2.2.1
      | inr rest =>
          cases rest with
          | inl contextMissing =>
              rw [contextMissing] at promoted
              cases promoted.2.2.2.1
          | inr statusMissing =>
              rw [statusMissing] at promoted
              cases promoted.2.2.2.2

end AsiStackProofs.ArtifactGraph
