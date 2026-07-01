namespace AsiStackProofs.ProofCarryingContracts

structure ProofContractReceipt where
  theoremRefsPresent : Bool
  deterministicFieldsPresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def ReceiptBoundaryComplete (receipt : ProofContractReceipt) : Prop :=
  receipt.theoremRefsPresent = true ∧
    receipt.deterministicFieldsPresent = true ∧
      receipt.nonClaimBoundaryPresent = true

def ReadyForDownstreamUse (receipt : ProofContractReceipt) : Prop :=
  ReceiptBoundaryComplete receipt

theorem downstream_ready_receipt_exposes_boundary_fields
    {receipt : ProofContractReceipt} :
    ReadyForDownstreamUse receipt ->
      receipt.theoremRefsPresent = true ∧
        receipt.deterministicFieldsPresent = true ∧
          receipt.nonClaimBoundaryPresent = true := by
  intro ready
  exact ready

theorem downstream_ready_receipt_missing_boundary_field_rejected
    {receipt : ProofContractReceipt} :
    (receipt.theoremRefsPresent = false ∨
      receipt.deterministicFieldsPresent = false ∨
        receipt.nonClaimBoundaryPresent = false) ->
    ¬ ReadyForDownstreamUse receipt := by
  intro missing ready
  unfold ReadyForDownstreamUse at ready
  unfold ReceiptBoundaryComplete at ready
  cases ready with
  | intro theoremRefs rest =>
      cases rest with
      | intro deterministicFields nonClaimBoundary =>
          cases missing with
          | inl missingTheorems =>
              rw [missingTheorems] at theoremRefs
              contradiction
          | inr missingRest =>
              cases missingRest with
              | inl missingDeterministic =>
                  rw [missingDeterministic] at deterministicFields
                  contradiction
              | inr missingNonClaim =>
                  rw [missingNonClaim] at nonClaimBoundary
                  contradiction

structure DownstreamPromotionReview where
  contractReady : Bool
  workloadPresent : Bool
  baselinePresent : Bool
  metricPresent : Bool
  evidenceArtifactPresent : Bool
  promoted : Bool
deriving DecidableEq, Repr

def PromotionEvidenceComplete (review : DownstreamPromotionReview) : Prop :=
  review.workloadPresent = true ∧
    review.baselinePresent = true ∧
      review.metricPresent = true ∧
        review.evidenceArtifactPresent = true

def ConsumerGateValid (review : DownstreamPromotionReview) : Prop :=
  review.promoted = true ->
    review.contractReady = true ∧ PromotionEvidenceComplete review

theorem contract_readiness_alone_cannot_promote_downstream_claim
    {review : DownstreamPromotionReview} :
    ConsumerGateValid review ->
    review.contractReady = true ->
    (review.workloadPresent = false ∨
      review.baselinePresent = false ∨
        review.metricPresent = false ∨
          review.evidenceArtifactPresent = false) ->
    review.promoted = false := by
  intro valid _ready missing
  cases promoted : review.promoted with
  | false => rfl
  | true =>
      have complete := (valid promoted).2
      unfold PromotionEvidenceComplete at complete
      cases missing with
      | inl noWorkload =>
          rw [noWorkload] at complete
          cases complete.1
      | inr rest =>
          cases rest with
          | inl noBaseline =>
              rw [noBaseline] at complete
              cases complete.2.1
          | inr rest =>
              cases rest with
              | inl noMetric =>
                  rw [noMetric] at complete
                  cases complete.2.2.1
              | inr noEvidence =>
                  rw [noEvidence] at complete
                  cases complete.2.2.2

theorem promoted_downstream_claim_without_contract_ready_rejected
    {review : DownstreamPromotionReview} :
    ConsumerGateValid review ->
    review.promoted = true ->
    review.contractReady = false ->
    False := by
  intro valid promoted notReady
  have ready := (valid promoted).1
  rw [notReady] at ready
  contradiction

structure ReceiptConsumerReview where
  receiptAcceptedForConsumer : Bool
  theoremRefsResolved : Bool
  fingerprintMatches : Bool
  contractFresh : Bool
  consumerAllowed : Bool
  unsupportedTransferClaimed : Bool
  nonClaimsPreserved : Bool
deriving DecidableEq, Repr

def ReceiptConsumerGateValid (review : ReceiptConsumerReview) : Prop :=
  review.receiptAcceptedForConsumer = true ->
    review.theoremRefsResolved = true ∧
      review.fingerprintMatches = true ∧
        review.contractFresh = true ∧
          review.consumerAllowed = true ∧
            review.unsupportedTransferClaimed = false ∧
              review.nonClaimsPreserved = true

theorem consumer_gate_acceptance_with_stale_or_unsupported_receipt_rejected
    {review : ReceiptConsumerReview} :
    review.receiptAcceptedForConsumer = true ->
    (review.theoremRefsResolved = false ∨
      review.fingerprintMatches = false ∨
        review.contractFresh = false ∨
          review.consumerAllowed = false ∨
            review.unsupportedTransferClaimed = true ∨
              review.nonClaimsPreserved = false) ->
    ¬ ReceiptConsumerGateValid review := by
  intro accepted missing valid
  unfold ReceiptConsumerGateValid at valid
  have complete := valid accepted
  cases complete with
  | intro refsResolved rest =>
      cases rest with
      | intro fingerprintOk rest =>
          cases rest with
          | intro fresh rest =>
              cases rest with
              | intro allowed rest =>
                  cases rest with
                  | intro noUnsupported nonClaims =>
                      cases missing with
                      | inl refsMissing =>
                          rw [refsMissing] at refsResolved
                          contradiction
                      | inr restMissing =>
                          cases restMissing with
                          | inl fingerprintMissing =>
                              rw [fingerprintMissing] at fingerprintOk
                              contradiction
                          | inr restMissing =>
                              cases restMissing with
                              | inl stale =>
                                  rw [stale] at fresh
                                  contradiction
                              | inr restMissing =>
                                  cases restMissing with
                                  | inl notAllowed =>
                                      rw [notAllowed] at allowed
                                      contradiction
                                  | inr restMissing =>
                                      cases restMissing with
                                      | inl unsupported =>
                                          rw [unsupported] at noUnsupported
                                          contradiction
                                      | inr nonClaimsMissing =>
                                          rw [nonClaimsMissing] at nonClaims
                                          contradiction

structure ReceiptReplayReview where
  replayMarkedPassing : Bool
  replayCommandPresent : Bool
  sourceDigestMatches : Bool
  receiptFingerprintMatches : Bool
  deterministicFieldsRecomputed : Bool
  theoremRefsPresent : Bool
deriving DecidableEq, Repr

def ReceiptReplayValid (review : ReceiptReplayReview) : Prop :=
  review.replayMarkedPassing = true ->
    review.replayCommandPresent = true ∧
      review.sourceDigestMatches = true ∧
        review.receiptFingerprintMatches = true ∧
          review.deterministicFieldsRecomputed = true ∧
            review.theoremRefsPresent = true

theorem passing_replay_without_replay_artifacts_rejected
    {review : ReceiptReplayReview} :
    review.replayMarkedPassing = true ->
    (review.replayCommandPresent = false ∨
      review.sourceDigestMatches = false ∨
        review.receiptFingerprintMatches = false ∨
          review.deterministicFieldsRecomputed = false ∨
            review.theoremRefsPresent = false) ->
    ¬ ReceiptReplayValid review := by
  intro passing missing valid
  unfold ReceiptReplayValid at valid
  have complete := valid passing
  cases complete with
  | intro commandPresent rest =>
      cases rest with
      | intro sourceDigestOk rest =>
          cases rest with
          | intro fingerprintOk rest =>
              cases rest with
              | intro fieldsRecomputed theoremRefsPresent =>
                  cases missing with
                  | inl commandMissing =>
                      rw [commandMissing] at commandPresent
                      contradiction
                  | inr restMissing =>
                      cases restMissing with
                      | inl sourceDigestMissing =>
                          rw [sourceDigestMissing] at sourceDigestOk
                          contradiction
                      | inr restMissing =>
                          cases restMissing with
                          | inl fingerprintMissing =>
                              rw [fingerprintMissing] at fingerprintOk
                              contradiction
                          | inr restMissing =>
                              cases restMissing with
                              | inl fieldsMissing =>
                                  rw [fieldsMissing] at fieldsRecomputed
                                  contradiction
                              | inr theoremRefsMissing =>
                                  rw [theoremRefsMissing] at theoremRefsPresent
                                  contradiction

end AsiStackProofs.ProofCarryingContracts
