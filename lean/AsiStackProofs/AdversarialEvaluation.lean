namespace AsiStackProofs.AdversarialEvaluation

inductive EvaluationIntegrityRoute where
  | retainAsDraft
  | requireContextRepair
  | requireIndependentEvaluation
  | quarantineDiscrepancy
  | requireResidualOwner
  | rejectIntentLaundering
  | releaseToPromotionReview
deriving DecidableEq, Repr

structure EvaluationIntegrityRecord where
  modelTaskIdentityRecorded : Bool
  elicitationContextRecorded : Bool
  selectionContextRecorded : Bool
  rewardProvenanceRecorded : Bool
  monitorProvenanceRecorded : Bool
  independentEvaluationRecorded : Bool
  crossContextProbeRecorded : Bool
  unresolvedIntegrityDiscrepancy : Bool
  residualOwnerRecorded : Bool
  noIntentInferenceRecorded : Bool
  promotionRequested : Bool
deriving DecidableEq, Repr

def EvaluationIntegrityRouteFor (record : EvaluationIntegrityRecord) : EvaluationIntegrityRoute :=
  if record.modelTaskIdentityRecorded = false then EvaluationIntegrityRoute.retainAsDraft
  else if record.elicitationContextRecorded = false || record.selectionContextRecorded = false ||
      record.rewardProvenanceRecorded = false || record.monitorProvenanceRecorded = false then
    EvaluationIntegrityRoute.requireContextRepair
  else if record.independentEvaluationRecorded = false || record.crossContextProbeRecorded = false then
    EvaluationIntegrityRoute.requireIndependentEvaluation
  else if record.unresolvedIntegrityDiscrepancy = true then
    EvaluationIntegrityRoute.quarantineDiscrepancy
  else if record.residualOwnerRecorded = false then EvaluationIntegrityRoute.requireResidualOwner
  else if record.promotionRequested = true && record.noIntentInferenceRecorded = false then
    EvaluationIntegrityRoute.rejectIntentLaundering
  else if record.promotionRequested = true then EvaluationIntegrityRoute.releaseToPromotionReview
  else EvaluationIntegrityRoute.retainAsDraft

theorem complete_integrity_record_reaches_promotion_review {r : EvaluationIntegrityRecord} :
    r.modelTaskIdentityRecorded = true -> r.elicitationContextRecorded = true ->
    r.selectionContextRecorded = true -> r.rewardProvenanceRecorded = true ->
    r.monitorProvenanceRecorded = true -> r.independentEvaluationRecorded = true ->
    r.crossContextProbeRecorded = true -> r.unresolvedIntegrityDiscrepancy = false ->
    r.residualOwnerRecorded = true -> r.noIntentInferenceRecorded = true ->
    r.promotionRequested = true ->
    EvaluationIntegrityRouteFor r = EvaluationIntegrityRoute.releaseToPromotionReview := by
  intro a b c d e f g h i j k
  unfold EvaluationIntegrityRouteFor
  simp [a,b,c,d,e,f,g,h,i,j,k]

theorem missing_selection_context_requires_repair {r : EvaluationIntegrityRecord} :
    r.modelTaskIdentityRecorded = true -> r.elicitationContextRecorded = true ->
    r.selectionContextRecorded = false ->
    EvaluationIntegrityRouteFor r = EvaluationIntegrityRoute.requireContextRepair := by
  intro a b c; unfold EvaluationIntegrityRouteFor; simp [a,b,c]

theorem missing_reward_provenance_requires_repair {r : EvaluationIntegrityRecord} :
    r.modelTaskIdentityRecorded = true -> r.elicitationContextRecorded = true ->
    r.selectionContextRecorded = true -> r.rewardProvenanceRecorded = false ->
    EvaluationIntegrityRouteFor r = EvaluationIntegrityRoute.requireContextRepair := by
  intro a b c d; unfold EvaluationIntegrityRouteFor; simp [a,b,c,d]

theorem missing_monitor_provenance_requires_repair {r : EvaluationIntegrityRecord} :
    r.modelTaskIdentityRecorded = true -> r.elicitationContextRecorded = true ->
    r.selectionContextRecorded = true -> r.rewardProvenanceRecorded = true ->
    r.monitorProvenanceRecorded = false ->
    EvaluationIntegrityRouteFor r = EvaluationIntegrityRoute.requireContextRepair := by
  intro a b c d e; unfold EvaluationIntegrityRouteFor; simp [a,b,c,d,e]

theorem missing_independent_evaluation_blocks_review {r : EvaluationIntegrityRecord} :
    r.modelTaskIdentityRecorded = true -> r.elicitationContextRecorded = true ->
    r.selectionContextRecorded = true -> r.rewardProvenanceRecorded = true ->
    r.monitorProvenanceRecorded = true -> r.independentEvaluationRecorded = false ->
    EvaluationIntegrityRouteFor r = EvaluationIntegrityRoute.requireIndependentEvaluation := by
  intro a b c d e f; unfold EvaluationIntegrityRouteFor; simp [a,b,c,d,e,f]

theorem missing_cross_context_probe_blocks_review {r : EvaluationIntegrityRecord} :
    r.modelTaskIdentityRecorded = true -> r.elicitationContextRecorded = true ->
    r.selectionContextRecorded = true -> r.rewardProvenanceRecorded = true ->
    r.monitorProvenanceRecorded = true -> r.independentEvaluationRecorded = true ->
    r.crossContextProbeRecorded = false ->
    EvaluationIntegrityRouteFor r = EvaluationIntegrityRoute.requireIndependentEvaluation := by
  intro a b c d e f g; unfold EvaluationIntegrityRouteFor; simp [a,b,c,d,e,f,g]

theorem unresolved_discrepancy_routes_to_quarantine {r : EvaluationIntegrityRecord} :
    r.modelTaskIdentityRecorded = true -> r.elicitationContextRecorded = true ->
    r.selectionContextRecorded = true -> r.rewardProvenanceRecorded = true ->
    r.monitorProvenanceRecorded = true -> r.independentEvaluationRecorded = true ->
    r.crossContextProbeRecorded = true -> r.unresolvedIntegrityDiscrepancy = true ->
    EvaluationIntegrityRouteFor r = EvaluationIntegrityRoute.quarantineDiscrepancy := by
  intro a b c d e f g h; unfold EvaluationIntegrityRouteFor; simp [a,b,c,d,e,f,g,h]

theorem observation_cannot_launder_intent_inference {r : EvaluationIntegrityRecord} :
    r.modelTaskIdentityRecorded = true -> r.elicitationContextRecorded = true ->
    r.selectionContextRecorded = true -> r.rewardProvenanceRecorded = true ->
    r.monitorProvenanceRecorded = true -> r.independentEvaluationRecorded = true ->
    r.crossContextProbeRecorded = true -> r.unresolvedIntegrityDiscrepancy = false ->
    r.residualOwnerRecorded = true -> r.noIntentInferenceRecorded = false ->
    r.promotionRequested = true ->
    EvaluationIntegrityRouteFor r = EvaluationIntegrityRoute.rejectIntentLaundering := by
  intro a b c d e f g h i j k
  unfold EvaluationIntegrityRouteFor
  simp [a,b,c,d,e,f,g,h,i,j,k]

end AsiStackProofs.AdversarialEvaluation
