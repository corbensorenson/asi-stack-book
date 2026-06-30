namespace AsiStackProofs.CompactGenerativeSystems

structure CompactGenerativeRecord where
  unresolvedObligations : Bool
  residualRecordsPresent : Bool
  lossyRepresentation : Bool
  markedExact : Bool
  verificationEvidencePresent : Bool
deriving DecidableEq, Repr

def ResidualHonestyValid (record : CompactGenerativeRecord) : Prop :=
  record.unresolvedObligations = true -> record.residualRecordsPresent = true

theorem unresolved_obligations_require_residual_records
    {record : CompactGenerativeRecord} :
    ResidualHonestyValid record ->
    record.unresolvedObligations = true ->
    record.residualRecordsPresent = true := by
  intro valid unresolved
  exact valid unresolved

theorem unresolved_obligations_without_residual_records_rejected
    {record : CompactGenerativeRecord} :
    record.unresolvedObligations = true ->
    record.residualRecordsPresent = false ->
    ¬ ResidualHonestyValid record := by
  intro unresolved missingResidual valid
  have residual := valid unresolved
  rw [missingResidual] at residual
  cases residual

def ExactnessClaimValid (record : CompactGenerativeRecord) : Prop :=
  record.lossyRepresentation = true ->
    record.verificationEvidencePresent = false ->
      record.markedExact = false

theorem lossy_representation_without_verification_cannot_be_marked_exact
    {record : CompactGenerativeRecord} :
    ExactnessClaimValid record ->
    record.lossyRepresentation = true ->
    record.verificationEvidencePresent = false ->
    record.markedExact = false := by
  intro valid lossy missingEvidence
  exact valid lossy missingEvidence

theorem lossy_unverified_representation_marked_exact_rejected
    {record : CompactGenerativeRecord} :
    record.lossyRepresentation = true ->
    record.verificationEvidencePresent = false ->
    record.markedExact = true ->
    ¬ ExactnessClaimValid record := by
  intro lossy missingEvidence exactMarked valid
  have notExact := valid lossy missingEvidence
  rw [exactMarked] at notExact
  cases notExact

end AsiStackProofs.CompactGenerativeSystems
