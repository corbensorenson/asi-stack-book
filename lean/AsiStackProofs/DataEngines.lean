namespace AsiStackProofs.DataEngines

inductive DataAdmissionDecision where
  | block
  | quarantine
  | experimentalOnly
  | eligible
deriving DecidableEq, Repr

structure DataAdmissionReview where
  provenanceRecorded : Bool
  authorityRecorded : Bool
  splitExclusionsRecorded : Bool
  contaminationCheckRecorded : Bool
  retentionPolicyRecorded : Bool
  deletionScopeRecorded : Bool
  evaluationRefsPresent : Bool
  residualsRecorded : Bool
  decision : DataAdmissionDecision
deriving DecidableEq, Repr

def DataAdmissionComplete (review : DataAdmissionReview) : Prop :=
  review.provenanceRecorded = true ∧
    review.authorityRecorded = true ∧
      review.splitExclusionsRecorded = true ∧
        review.contaminationCheckRecorded = true ∧
          review.retentionPolicyRecorded = true ∧
            review.deletionScopeRecorded = true ∧
              review.evaluationRefsPresent = true ∧
                review.residualsRecorded = true

def DataAdmissionRouteFor (review : DataAdmissionReview) : DataAdmissionDecision :=
  if review.provenanceRecorded = false ∨ review.authorityRecorded = false then
    DataAdmissionDecision.block
  else if review.splitExclusionsRecorded = false ∨ review.contaminationCheckRecorded = false then
    DataAdmissionDecision.quarantine
  else if review.retentionPolicyRecorded = false ∨ review.deletionScopeRecorded = false ∨
      review.evaluationRefsPresent = false ∨ review.residualsRecorded = false then
    DataAdmissionDecision.experimentalOnly
  else
    DataAdmissionDecision.eligible

theorem missing_provenance_or_authority_blocks_data_admission
    {review : DataAdmissionReview} :
    review.provenanceRecorded = false ∨ review.authorityRecorded = false ->
    DataAdmissionRouteFor review = DataAdmissionDecision.block := by
  intro missing
  unfold DataAdmissionRouteFor
  simp [missing]

theorem missing_split_exclusion_or_contamination_check_quarantines_data
    {review : DataAdmissionReview} :
    review.provenanceRecorded = true ->
    review.authorityRecorded = true ->
    (review.splitExclusionsRecorded = false ∨ review.contaminationCheckRecorded = false) ->
    DataAdmissionRouteFor review = DataAdmissionDecision.quarantine := by
  intro provenance authority missing
  unfold DataAdmissionRouteFor
  simp [provenance, authority, missing]

theorem complete_data_record_routes_to_eligible
    {review : DataAdmissionReview} :
    DataAdmissionComplete review ->
    DataAdmissionRouteFor review = DataAdmissionDecision.eligible := by
  intro complete
  rcases complete with ⟨provenance, authority, exclusions, contamination,
    retention, deletion, evaluation, residuals⟩
  simp [DataAdmissionRouteFor, provenance, authority, exclusions, contamination,
    retention, deletion, evaluation, residuals]

end AsiStackProofs.DataEngines
