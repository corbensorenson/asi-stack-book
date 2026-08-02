import AsiStackProofs.EvidenceStates
import AsiStackProofs.Routing
import AsiStackProofs.SearchSubstrates

namespace AsiStackProofs.RelationalDimensionCompiler

/-!
A bounded model of authored relational-dimension compiler records. The model
proves typed-role preservation, finite role and proposal denominator custody,
descendant-closure obligations, staged review invariants, exact repair routing,
scope invalidation, information-loss countermodels, and rejecting consumer
interfaces. It does not prove higher-order irreducibility, representational
usefulness, efficiency, natural-task transfer, bounded primitive arity, safe
online adaptation, support, release, or external effect.
-/

structure RoleBinding where
  roleId : Nat
  entityId : Nat
  typeId : Nat
  typed : Bool
deriving DecidableEq, Repr

def roleIds : List RoleBinding -> List Nat
  | [] => []
  | binding :: tail => binding.roleId :: roleIds tail

def remapEntities (f : Nat -> Nat) : List RoleBinding -> List RoleBinding
  | [] => []
  | binding :: tail =>
      { binding with entityId := f binding.entityId } :: remapEntities f tail

theorem role_id_collection_append_composes (before after : List RoleBinding) :
    roleIds (before ++ after) = roleIds before ++ roleIds after := by
  induction before with
  | nil => rfl
  | cons head tail ih => simp [roleIds, ih]

theorem every_role_id_survives_collection
    (bindings : List RoleBinding) (binding : RoleBinding)
    (member : binding ∈ bindings) : binding.roleId ∈ roleIds bindings := by
  induction bindings with
  | nil => simp at member
  | cons head tail ih =>
      simp only [List.mem_cons] at member ⊢
      cases member with
      | inl same => subst head; simp [roleIds]
      | inr rest => right; exact ih rest

theorem entity_remapping_preserves_role_identity
    (f : Nat -> Nat) (bindings : List RoleBinding) :
    roleIds (remapEntities f bindings) = roleIds bindings := by
  induction bindings with
  | nil => rfl
  | cons head tail ih => simp [remapEntities, roleIds, ih]

def CompleteRoleSchema (requiredRoles : List Nat) (bindings : List RoleBinding) : Prop :=
  forall roleId, roleId ∈ requiredRoles ->
    exists binding, binding ∈ bindings ∧ binding.roleId = roleId ∧
      binding.typed = true

theorem complete_role_schema_covers_every_required_role
    (requiredRoles : List Nat) (bindings : List RoleBinding)
    (complete : CompleteRoleSchema requiredRoles bindings)
    (roleId : Nat) (required : roleId ∈ requiredRoles) :
    exists binding, binding ∈ bindings ∧ binding.roleId = roleId ∧
      binding.typed = true := complete roleId required

theorem omitted_required_role_rejects_complete_schema
    (requiredRoles : List Nat) (bindings : List RoleBinding) (roleId : Nat)
    (required : roleId ∈ requiredRoles)
    (missing : forall binding, binding ∈ bindings -> binding.roleId = roleId ->
      binding.typed = false) : Not (CompleteRoleSchema requiredRoles bindings) := by
  intro complete
  obtain ⟨binding, member, same, typed⟩ := complete roleId required
  have omitted := missing binding member same
  simp [omitted] at typed

structure CandidateOutcome where
  candidateId : Nat
  attempted : Bool
  retainedInDenominator : Bool
  qualified : Bool
deriving DecidableEq, Repr

def candidateIds : List CandidateOutcome -> List Nat
  | [] => []
  | candidate :: tail => candidate.candidateId :: candidateIds tail

theorem candidate_id_collection_append_composes
    (before after : List CandidateOutcome) :
    candidateIds (before ++ after) = candidateIds before ++ candidateIds after := by
  induction before with
  | nil => rfl
  | cons head tail ih => simp [candidateIds, ih]

theorem every_candidate_id_survives_collection
    (candidates : List CandidateOutcome) (candidate : CandidateOutcome)
    (member : candidate ∈ candidates) : candidate.candidateId ∈ candidateIds candidates := by
  induction candidates with
  | nil => simp at member
  | cons head tail ih =>
      simp only [List.mem_cons] at member ⊢
      cases member with
      | inl same => subst head; simp [candidateIds]
      | inr rest => right; exact ih rest

def CompleteProposalDenominator
    (expectedIds : List Nat) (candidates : List CandidateOutcome) : Prop :=
  forall candidateId, candidateId ∈ expectedIds ->
    exists candidate, candidate ∈ candidates ∧ candidate.candidateId = candidateId ∧
      candidate.attempted = true ∧ candidate.retainedInDenominator = true

theorem complete_proposal_denominator_covers_every_expected_candidate
    (expectedIds : List Nat) (candidates : List CandidateOutcome)
    (complete : CompleteProposalDenominator expectedIds candidates)
    (candidateId : Nat) (expected : candidateId ∈ expectedIds) :
    exists candidate, candidate ∈ candidates ∧ candidate.candidateId = candidateId ∧
      candidate.attempted = true ∧ candidate.retainedInDenominator = true :=
  complete candidateId expected

theorem omitted_candidate_rejects_complete_proposal_denominator
    (expectedIds : List Nat) (candidates : List CandidateOutcome) (candidateId : Nat)
    (expected : candidateId ∈ expectedIds)
    (missing : forall candidate, candidate ∈ candidates ->
      candidate.candidateId = candidateId -> candidate.retainedInDenominator = false) :
    Not (CompleteProposalDenominator expectedIds candidates) := by
  intro complete
  obtain ⟨candidate, member, same, _, retained⟩ := complete candidateId expected
  have omitted := missing candidate member same
  simp [omitted] at retained

structure DependentArtifact where
  artifactId : Nat
  parentRelationId : Nat
  invalidated : Bool
  recompiled : Bool
deriving DecidableEq, Repr

def DescendantsClosed (relationId : Nat) (artifacts : List DependentArtifact) : Prop :=
  forall artifact, artifact ∈ artifacts -> artifact.parentRelationId = relationId ->
    artifact.invalidated = true ∨ artifact.recompiled = true

theorem descendants_closed_append_iff
    (relationId : Nat) (before after : List DependentArtifact) :
    DescendantsClosed relationId (before ++ after) ↔
      DescendantsClosed relationId before ∧ DescendantsClosed relationId after := by
  constructor
  · intro closed
    constructor
    · intro artifact member parent
      exact closed artifact (by simp [member]) parent
    · intro artifact member parent
      exact closed artifact (by simp [member]) parent
  · intro closed artifact member parent
    simp only [List.mem_append] at member
    cases member with
    | inl left => exact closed.1 artifact left parent
    | inr right => exact closed.2 artifact right parent

theorem active_descendant_blocks_contraction_closure
    (relationId : Nat) (artifacts : List DependentArtifact)
    (artifact : DependentArtifact) (member : artifact ∈ artifacts)
    (parent : artifact.parentRelationId = relationId)
    (active : artifact.invalidated = false ∧ artifact.recompiled = false) :
    Not (DescendantsClosed relationId artifacts) := by
  intro closed
  have disposition := closed artifact member parent
  cases disposition with
  | inl invalidated => simp [active.1] at invalidated
  | inr recompiled => simp [active.2] at recompiled

structure CompilerDossier where
  proposalIdentityBound : Bool := true
  compilerVersionBound : Bool := true
  sourceResidualBound : Bool := true
  roleSchemaBound : Bool := true
  authorityBound : Bool := true
  branchBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  rolesNonempty : Bool := true
  everyRoleTyped : Bool := true
  roleIdentityUnique : Bool := true
  symmetryDeclared : Bool := true
  optionalityDeclared : Bool := true
  provenanceBound : Bool := true
  uncertaintyBound : Bool := true
  scopeBound : Bool := true
  proposalDenominatorComplete : Bool := true
  rejectedProposalsRetained : Bool := true
  candidateGeneratorBound : Bool := true
  reifiedNodeRescuePresent : Bool := true
  pairwiseRescuePresent : Bool := true
  messagePassingRescuePresent : Bool := true
  sequenceRescuePresent : Bool := true
  retrievalRescuePresent : Bool := true
  toolRescuePresent : Bool := true
  ordinaryModelRescuePresent : Bool := true
  rescueBudgetsMatched : Bool := true
  heldoutTopologyBound : Bool := true
  rolePermutationTestBound : Bool := true
  missingRoleTestBound : Bool := true
  counterfactualRoleTestBound : Bool := true
  naturalSyntheticSeparated : Bool := true
  calibrationBound : Bool := true
  seedDenominatorComplete : Bool := true
  lifecycleCostBound : Bool := true
  leakageReviewBound : Bool := true
  independentEvaluatorBound : Bool := true
  semanticVersionBound : Bool := true
  conformanceReplayBound : Bool := true
  executableFallbackBound : Bool := true
  slowPathRecheckBound : Bool := true
  routerContractBound : Bool := true
  compiledExpiryBound : Bool := true
  compilationResidualOwnerBound : Bool := true
  newDependentsFrozen : Bool := true
  descendantsEnumerated : Bool := true
  descendantsInvalidatedOrRecompiled : Bool := true
  cachesInvalidatedOrVersioned : Bool := true
  backupAndRestoreBound : Bool := true
  learnedInfluenceResidualBound : Bool := true
  irreducibilityClaimed : Bool := false
  usefulnessClaimed : Bool := false
  efficiencyClaimed : Bool := false
  boundedPrimitiveArityClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : CompilerDossier) : Prop := d.currentTick ≤ d.expiresAt
instance currentDecidable (d : CompilerDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : CompilerDossier) : Prop :=
  d.proposalIdentityBound = true ∧ d.compilerVersionBound = true ∧
  d.sourceResidualBound = true ∧ d.roleSchemaBound = true ∧
  d.authorityBound = true ∧ d.branchBound = true ∧ Current d

def TypingComplete (d : CompilerDossier) : Prop :=
  d.rolesNonempty = true ∧ d.everyRoleTyped = true ∧
  d.roleIdentityUnique = true ∧ d.symmetryDeclared = true ∧
  d.optionalityDeclared = true ∧ d.provenanceBound = true ∧
  d.uncertaintyBound = true ∧ d.scopeBound = true

def RescueComplete (d : CompilerDossier) : Prop :=
  d.proposalDenominatorComplete = true ∧ d.rejectedProposalsRetained = true ∧
  d.candidateGeneratorBound = true ∧ d.reifiedNodeRescuePresent = true ∧
  d.pairwiseRescuePresent = true ∧ d.messagePassingRescuePresent = true ∧
  d.sequenceRescuePresent = true ∧ d.retrievalRescuePresent = true ∧
  d.toolRescuePresent = true ∧ d.ordinaryModelRescuePresent = true ∧
  d.rescueBudgetsMatched = true

def QualificationComplete (d : CompilerDossier) : Prop :=
  d.heldoutTopologyBound = true ∧ d.rolePermutationTestBound = true ∧
  d.missingRoleTestBound = true ∧ d.counterfactualRoleTestBound = true ∧
  d.naturalSyntheticSeparated = true ∧ d.calibrationBound = true ∧
  d.seedDenominatorComplete = true ∧ d.lifecycleCostBound = true ∧
  d.leakageReviewBound = true ∧ d.independentEvaluatorBound = true

def CompilationComplete (d : CompilerDossier) : Prop :=
  d.semanticVersionBound = true ∧ d.conformanceReplayBound = true ∧
  d.executableFallbackBound = true ∧ d.slowPathRecheckBound = true ∧
  d.routerContractBound = true ∧ d.compiledExpiryBound = true ∧
  d.compilationResidualOwnerBound = true

def ContractionComplete (d : CompilerDossier) : Prop :=
  d.newDependentsFrozen = true ∧ d.descendantsEnumerated = true ∧
  d.descendantsInvalidatedOrRecompiled = true ∧
  d.cachesInvalidatedOrVersioned = true ∧ d.backupAndRestoreBound = true ∧
  d.learnedInfluenceResidualBound = true

def BoundaryComplete (d : CompilerDossier) : Prop :=
  d.irreducibilityClaimed = false ∧ d.usefulnessClaimed = false ∧
  d.efficiencyClaimed = false ∧ d.boundedPrimitiveArityClaimed = false ∧
  d.supportOrReleaseRequested = false

instance identityDecidable (d : CompilerDossier) : Decidable (IdentityComplete d) := by
  unfold IdentityComplete Current; infer_instance
instance typingDecidable (d : CompilerDossier) : Decidable (TypingComplete d) := by
  unfold TypingComplete; infer_instance
instance rescueDecidable (d : CompilerDossier) : Decidable (RescueComplete d) := by
  unfold RescueComplete; infer_instance
instance qualificationDecidable (d : CompilerDossier) : Decidable (QualificationComplete d) := by
  unfold QualificationComplete; infer_instance
instance compilationDecidable (d : CompilerDossier) : Decidable (CompilationComplete d) := by
  unfold CompilationComplete; infer_instance
instance contractionDecidable (d : CompilerDossier) : Decidable (ContractionComplete d) := by
  unfold ContractionComplete; infer_instance
instance boundaryDecidable (d : CompilerDossier) : Decidable (BoundaryComplete d) := by
  unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : CompilerDossier) : Prop :=
  IdentityComplete d ∧ TypingComplete d ∧ RescueComplete d ∧
  QualificationComplete d ∧ CompilationComplete d ∧ ContractionComplete d ∧
  BoundaryComplete d
instance admissibleDecidable (d : CompilerDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete Current TypingComplete RescueComplete
    QualificationComplete CompilationComplete ContractionComplete BoundaryComplete
  infer_instance
def DossierReady (d : CompilerDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | typingReviewed | rescueReviewed
  | qualificationReviewed | compilationReviewed | contractionReviewed
  | boundaryReviewed | repairRequired | eligibleForTheseusRelationalCompilerStudy
deriving DecidableEq, Repr

def ReviewStepFor (d : CompilerDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (TypingComplete d) then .typingReviewed else .repairRequired
  | .typingReviewed => if decide (RescueComplete d) then .rescueReviewed else .repairRequired
  | .rescueReviewed =>
      if decide (QualificationComplete d) then .qualificationReviewed else .repairRequired
  | .qualificationReviewed =>
      if decide (CompilationComplete d) then .compilationReviewed else .repairRequired
  | .compilationReviewed =>
      if decide (ContractionComplete d) then .contractionReviewed else .repairRequired
  | .contractionReviewed =>
      if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusRelationalCompilerStudy
  | state => state

def ReviewRun (d : CompilerDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : CompilerDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .typingReviewed => IdentityComplete d ∧ TypingComplete d
  | .rescueReviewed => IdentityComplete d ∧ TypingComplete d ∧ RescueComplete d
  | .qualificationReviewed =>
      IdentityComplete d ∧ TypingComplete d ∧ RescueComplete d ∧ QualificationComplete d
  | .compilationReviewed =>
      IdentityComplete d ∧ TypingComplete d ∧ RescueComplete d ∧
        QualificationComplete d ∧ CompilationComplete d
  | .contractionReviewed =>
      IdentityComplete d ∧ TypingComplete d ∧ RescueComplete d ∧
        QualificationComplete d ∧ CompilationComplete d ∧ ContractionComplete d
  | .boundaryReviewed | .eligibleForTheseusRelationalCompilerStudy => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : CompilerDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case typingReviewed => split <;> simp_all [StageInvariant]
  case rescueReviewed => split <;> simp_all [StageInvariant]
  case qualificationReviewed => split <;> simp_all [StageInvariant]
  case compilationReviewed => split <;> simp_all [StageInvariant]
  case contractionReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : CompilerDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem study_eligibility_requires_admissible_dossier
    (d : CompilerDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusRelationalCompilerStudy) :
    DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : CompilerDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_theseus_relational_compiler_study :
    ReviewRun completeDossier 8 = .eligibleForTheseusRelationalCompilerStudy := by decide

inductive AdmissionAxis where
  | proposalIdentity | compilerVersion | sourceResidual | roleSchema | authority | branch
  | expiry | rolesNonempty | everyRoleTyped | roleIdentityUnique | symmetry | optionality
  | provenance | uncertainty | scope | proposalDenominator | rejectedProposals
  | candidateGenerator | reifiedNodeRescue | pairwiseRescue | messagePassingRescue
  | sequenceRescue | retrievalRescue | toolRescue | ordinaryModelRescue | matchedBudgets
  | heldoutTopology | rolePermutation | missingRole | counterfactualRole
  | naturalSynthetic | calibration | seedDenominator | lifecycleCost | leakageReview
  | independentEvaluator | semanticVersion | conformanceReplay | executableFallback
  | slowPathRecheck | routerContract | compiledExpiry | compilationResidualOwner
  | freezeDependents | descendantsEnumerated | descendantsClosed | cachesInvalidated
  | backupRestore | learnedInfluenceResidual | irreducibilityClaim | usefulnessClaim
  | efficiencyClaim | boundedArityClaim | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> CompilerDossier
  | .proposalIdentity => { completeDossier with proposalIdentityBound := false }
  | .compilerVersion => { completeDossier with compilerVersionBound := false }
  | .sourceResidual => { completeDossier with sourceResidualBound := false }
  | .roleSchema => { completeDossier with roleSchemaBound := false }
  | .authority => { completeDossier with authorityBound := false }
  | .branch => { completeDossier with branchBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .rolesNonempty => { completeDossier with rolesNonempty := false }
  | .everyRoleTyped => { completeDossier with everyRoleTyped := false }
  | .roleIdentityUnique => { completeDossier with roleIdentityUnique := false }
  | .symmetry => { completeDossier with symmetryDeclared := false }
  | .optionality => { completeDossier with optionalityDeclared := false }
  | .provenance => { completeDossier with provenanceBound := false }
  | .uncertainty => { completeDossier with uncertaintyBound := false }
  | .scope => { completeDossier with scopeBound := false }
  | .proposalDenominator => { completeDossier with proposalDenominatorComplete := false }
  | .rejectedProposals => { completeDossier with rejectedProposalsRetained := false }
  | .candidateGenerator => { completeDossier with candidateGeneratorBound := false }
  | .reifiedNodeRescue => { completeDossier with reifiedNodeRescuePresent := false }
  | .pairwiseRescue => { completeDossier with pairwiseRescuePresent := false }
  | .messagePassingRescue => { completeDossier with messagePassingRescuePresent := false }
  | .sequenceRescue => { completeDossier with sequenceRescuePresent := false }
  | .retrievalRescue => { completeDossier with retrievalRescuePresent := false }
  | .toolRescue => { completeDossier with toolRescuePresent := false }
  | .ordinaryModelRescue => { completeDossier with ordinaryModelRescuePresent := false }
  | .matchedBudgets => { completeDossier with rescueBudgetsMatched := false }
  | .heldoutTopology => { completeDossier with heldoutTopologyBound := false }
  | .rolePermutation => { completeDossier with rolePermutationTestBound := false }
  | .missingRole => { completeDossier with missingRoleTestBound := false }
  | .counterfactualRole => { completeDossier with counterfactualRoleTestBound := false }
  | .naturalSynthetic => { completeDossier with naturalSyntheticSeparated := false }
  | .calibration => { completeDossier with calibrationBound := false }
  | .seedDenominator => { completeDossier with seedDenominatorComplete := false }
  | .lifecycleCost => { completeDossier with lifecycleCostBound := false }
  | .leakageReview => { completeDossier with leakageReviewBound := false }
  | .independentEvaluator => { completeDossier with independentEvaluatorBound := false }
  | .semanticVersion => { completeDossier with semanticVersionBound := false }
  | .conformanceReplay => { completeDossier with conformanceReplayBound := false }
  | .executableFallback => { completeDossier with executableFallbackBound := false }
  | .slowPathRecheck => { completeDossier with slowPathRecheckBound := false }
  | .routerContract => { completeDossier with routerContractBound := false }
  | .compiledExpiry => { completeDossier with compiledExpiryBound := false }
  | .compilationResidualOwner => { completeDossier with compilationResidualOwnerBound := false }
  | .freezeDependents => { completeDossier with newDependentsFrozen := false }
  | .descendantsEnumerated => { completeDossier with descendantsEnumerated := false }
  | .descendantsClosed => { completeDossier with descendantsInvalidatedOrRecompiled := false }
  | .cachesInvalidated => { completeDossier with cachesInvalidatedOrVersioned := false }
  | .backupRestore => { completeDossier with backupAndRestoreBound := false }
  | .learnedInfluenceResidual => { completeDossier with learnedInfluenceResidualBound := false }
  | .irreducibilityClaim => { completeDossier with irreducibilityClaimed := true }
  | .usefulnessClaim => { completeDossier with usefulnessClaimed := true }
  | .efficiencyClaim => { completeDossier with efficiencyClaimed := true }
  | .boundedArityClaim => { completeDossier with boundedPrimitiveArityClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindProposalIdentity | bindCompilerVersion | bindSourceResidual | bindRoleSchema
  | bindAuthority | bindBranch | renewExpiry | requireRoles | typeEveryRole
  | restoreUniqueRoleIdentity | declareSymmetry | declareOptionality | bindProvenance
  | bindUncertainty | bindScope | completeProposalDenominator
  | retainRejectedProposals | bindCandidateGenerator | addReifiedNodeRescue
  | addPairwiseRescue | addMessagePassingRescue | addSequenceRescue
  | addRetrievalRescue | addToolRescue | addOrdinaryModelRescue | matchRescueBudgets
  | bindHeldoutTopology | bindRolePermutationTest | bindMissingRoleTest
  | bindCounterfactualRoleTest | separateNaturalSynthetic | bindCalibration
  | completeSeedDenominator | bindLifecycleCost | bindLeakageReview
  | bindIndependentEvaluator | bindSemanticVersion | bindConformanceReplay
  | bindExecutableFallback | bindSlowPathRecheck | bindRouterContract
  | bindCompiledExpiry | assignCompilationResidualOwner | freezeNewDependents
  | enumerateDescendants | closeDescendants | invalidateCaches | bindBackupRestore
  | bindLearnedInfluenceResidual | rejectIrreducibilityClaim | rejectUsefulnessClaim
  | rejectEfficiencyClaim | rejectBoundedArityClaim | refuseSupportOrRelease
  | eligibleForTheseusRelationalCompilerStudy
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .proposalIdentity => .bindProposalIdentity | .compilerVersion => .bindCompilerVersion
  | .sourceResidual => .bindSourceResidual | .roleSchema => .bindRoleSchema
  | .authority => .bindAuthority | .branch => .bindBranch | .expiry => .renewExpiry
  | .rolesNonempty => .requireRoles | .everyRoleTyped => .typeEveryRole
  | .roleIdentityUnique => .restoreUniqueRoleIdentity | .symmetry => .declareSymmetry
  | .optionality => .declareOptionality | .provenance => .bindProvenance
  | .uncertainty => .bindUncertainty | .scope => .bindScope
  | .proposalDenominator => .completeProposalDenominator
  | .rejectedProposals => .retainRejectedProposals
  | .candidateGenerator => .bindCandidateGenerator
  | .reifiedNodeRescue => .addReifiedNodeRescue | .pairwiseRescue => .addPairwiseRescue
  | .messagePassingRescue => .addMessagePassingRescue
  | .sequenceRescue => .addSequenceRescue | .retrievalRescue => .addRetrievalRescue
  | .toolRescue => .addToolRescue | .ordinaryModelRescue => .addOrdinaryModelRescue
  | .matchedBudgets => .matchRescueBudgets | .heldoutTopology => .bindHeldoutTopology
  | .rolePermutation => .bindRolePermutationTest | .missingRole => .bindMissingRoleTest
  | .counterfactualRole => .bindCounterfactualRoleTest
  | .naturalSynthetic => .separateNaturalSynthetic | .calibration => .bindCalibration
  | .seedDenominator => .completeSeedDenominator | .lifecycleCost => .bindLifecycleCost
  | .leakageReview => .bindLeakageReview | .independentEvaluator => .bindIndependentEvaluator
  | .semanticVersion => .bindSemanticVersion | .conformanceReplay => .bindConformanceReplay
  | .executableFallback => .bindExecutableFallback | .slowPathRecheck => .bindSlowPathRecheck
  | .routerContract => .bindRouterContract | .compiledExpiry => .bindCompiledExpiry
  | .compilationResidualOwner => .assignCompilationResidualOwner
  | .freezeDependents => .freezeNewDependents | .descendantsEnumerated => .enumerateDescendants
  | .descendantsClosed => .closeDescendants | .cachesInvalidated => .invalidateCaches
  | .backupRestore => .bindBackupRestore
  | .learnedInfluenceResidual => .bindLearnedInfluenceResidual
  | .irreducibilityClaim => .rejectIrreducibilityClaim
  | .usefulnessClaim => .rejectUsefulnessClaim | .efficiencyClaim => .rejectEfficiencyClaim
  | .boundedArityClaim => .rejectBoundedArityClaim
  | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : CompilerDossier) : RepairDisposition :=
  if !d.proposalIdentityBound then .bindProposalIdentity
  else if !d.compilerVersionBound then .bindCompilerVersion
  else if !d.sourceResidualBound then .bindSourceResidual
  else if !d.roleSchemaBound then .bindRoleSchema
  else if !d.authorityBound then .bindAuthority
  else if !d.branchBound then .bindBranch
  else if !decide (Current d) then .renewExpiry
  else if !d.rolesNonempty then .requireRoles
  else if !d.everyRoleTyped then .typeEveryRole
  else if !d.roleIdentityUnique then .restoreUniqueRoleIdentity
  else if !d.symmetryDeclared then .declareSymmetry
  else if !d.optionalityDeclared then .declareOptionality
  else if !d.provenanceBound then .bindProvenance
  else if !d.uncertaintyBound then .bindUncertainty
  else if !d.scopeBound then .bindScope
  else if !d.proposalDenominatorComplete then .completeProposalDenominator
  else if !d.rejectedProposalsRetained then .retainRejectedProposals
  else if !d.candidateGeneratorBound then .bindCandidateGenerator
  else if !d.reifiedNodeRescuePresent then .addReifiedNodeRescue
  else if !d.pairwiseRescuePresent then .addPairwiseRescue
  else if !d.messagePassingRescuePresent then .addMessagePassingRescue
  else if !d.sequenceRescuePresent then .addSequenceRescue
  else if !d.retrievalRescuePresent then .addRetrievalRescue
  else if !d.toolRescuePresent then .addToolRescue
  else if !d.ordinaryModelRescuePresent then .addOrdinaryModelRescue
  else if !d.rescueBudgetsMatched then .matchRescueBudgets
  else if !d.heldoutTopologyBound then .bindHeldoutTopology
  else if !d.rolePermutationTestBound then .bindRolePermutationTest
  else if !d.missingRoleTestBound then .bindMissingRoleTest
  else if !d.counterfactualRoleTestBound then .bindCounterfactualRoleTest
  else if !d.naturalSyntheticSeparated then .separateNaturalSynthetic
  else if !d.calibrationBound then .bindCalibration
  else if !d.seedDenominatorComplete then .completeSeedDenominator
  else if !d.lifecycleCostBound then .bindLifecycleCost
  else if !d.leakageReviewBound then .bindLeakageReview
  else if !d.independentEvaluatorBound then .bindIndependentEvaluator
  else if !d.semanticVersionBound then .bindSemanticVersion
  else if !d.conformanceReplayBound then .bindConformanceReplay
  else if !d.executableFallbackBound then .bindExecutableFallback
  else if !d.slowPathRecheckBound then .bindSlowPathRecheck
  else if !d.routerContractBound then .bindRouterContract
  else if !d.compiledExpiryBound then .bindCompiledExpiry
  else if !d.compilationResidualOwnerBound then .assignCompilationResidualOwner
  else if !d.newDependentsFrozen then .freezeNewDependents
  else if !d.descendantsEnumerated then .enumerateDescendants
  else if !d.descendantsInvalidatedOrRecompiled then .closeDescendants
  else if !d.cachesInvalidatedOrVersioned then .invalidateCaches
  else if !d.backupAndRestoreBound then .bindBackupRestore
  else if !d.learnedInfluenceResidualBound then .bindLearnedInfluenceResidual
  else if d.irreducibilityClaimed then .rejectIrreducibilityClaim
  else if d.usefulnessClaimed then .rejectUsefulnessClaim
  else if d.efficiencyClaimed then .rejectEfficiencyClaim
  else if d.boundedPrimitiveArityClaimed then .rejectBoundedArityClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusRelationalCompilerStudy

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : CompilerDossier) (h : DossierReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_typing (d : CompilerDossier) (h : DossierReady d = true) :
    TypingComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_rescues (d : CompilerDossier) (h : DossierReady d = true) :
    RescueComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_qualification (d : CompilerDossier) (h : DossierReady d = true) :
    QualificationComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_compilation (d : CompilerDossier) (h : DossierReady d = true) :
    CompilationComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_contraction (d : CompilerDossier) (h : DossierReady d = true) :
    ContractionComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.1
theorem readiness_requires_nonclaim_boundary (d : CompilerDossier)
    (h : DossierReady d = true) : BoundaryComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_compiler_contract_remains_expired_when_time_advances
    (expiresAt now later : Nat) (expired : expiresAt < now) (advances : now ≤ later) :
    expiresAt < later := Nat.lt_of_lt_of_le expired advances

theorem candidate_budget_overrun_persists_when_generated_count_grows
    (limit generated laterGenerated : Nat) (overrun : limit < generated)
    (grows : generated ≤ laterGenerated) : limit < laterGenerated :=
  Nat.lt_of_lt_of_le overrun grows

structure CompilerReceiptScope where
  proposalId : Nat
  compilerVersion : Nat
  roleSchemaId : Nat
  rescueSuiteId : Nat
  qualificationSuiteId : Nat
  fallbackId : Nat
  authorityId : Nat
deriving DecidableEq, Repr

def ReceiptApplies (receipt current : CompilerReceiptScope) : Prop := receipt = current

theorem proposal_change_invalidates_compiler_receipt
    (r : CompilerReceiptScope) (changed : r.proposalId ≠ p) :
    Not (ReceiptApplies r { r with proposalId := p }) := by
  intro same; exact changed (congrArg CompilerReceiptScope.proposalId same)
theorem compiler_version_change_invalidates_compiler_receipt
    (r : CompilerReceiptScope) (changed : r.compilerVersion ≠ v) :
    Not (ReceiptApplies r { r with compilerVersion := v }) := by
  intro same; exact changed (congrArg CompilerReceiptScope.compilerVersion same)
theorem role_schema_change_invalidates_compiler_receipt
    (r : CompilerReceiptScope) (changed : r.roleSchemaId ≠ s) :
    Not (ReceiptApplies r { r with roleSchemaId := s }) := by
  intro same; exact changed (congrArg CompilerReceiptScope.roleSchemaId same)
theorem rescue_suite_change_invalidates_compiler_receipt
    (r : CompilerReceiptScope) (changed : r.rescueSuiteId ≠ b) :
    Not (ReceiptApplies r { r with rescueSuiteId := b }) := by
  intro same; exact changed (congrArg CompilerReceiptScope.rescueSuiteId same)
theorem qualification_suite_change_invalidates_compiler_receipt
    (r : CompilerReceiptScope) (changed : r.qualificationSuiteId ≠ q) :
    Not (ReceiptApplies r { r with qualificationSuiteId := q }) := by
  intro same; exact changed (congrArg CompilerReceiptScope.qualificationSuiteId same)
theorem fallback_change_invalidates_compiler_receipt
    (r : CompilerReceiptScope) (changed : r.fallbackId ≠ f) :
    Not (ReceiptApplies r { r with fallbackId := f }) := by
  intro same; exact changed (congrArg CompilerReceiptScope.fallbackId same)
theorem authority_change_invalidates_compiler_receipt
    (r : CompilerReceiptScope) (changed : r.authorityId ≠ a) :
    Not (ReceiptApplies r { r with authorityId := a }) := by
  intro same; exact changed (congrArg CompilerReceiptScope.authorityId same)

structure QualificationSignals where
  heldoutScoreBand : Nat
  latencyBand : Nat
  memoryBand : Nat
deriving DecidableEq, Repr
structure RoleFidelityCase where
  signals : QualificationSignals
  roleIdentityPreserved : Bool
deriving DecidableEq, Repr

def sameMetricsWithRoleFidelity : RoleFidelityCase :=
  { signals := { heldoutScoreBand := 8, latencyBand := 3, memoryBand := 4 },
    roleIdentityPreserved := true }
def sameMetricsWithRoleCollapse : RoleFidelityCase :=
  { signals := { heldoutScoreBand := 8, latencyBand := 3, memoryBand := 4 },
    roleIdentityPreserved := false }

theorem identical_qualification_metrics_can_hide_opposite_role_fidelity :
    sameMetricsWithRoleFidelity.signals = sameMetricsWithRoleCollapse.signals ∧
      sameMetricsWithRoleFidelity.roleIdentityPreserved ≠
        sameMetricsWithRoleCollapse.roleIdentityPreserved := by decide

theorem qualification_metrics_cannot_recover_role_fidelity
    (classify : QualificationSignals -> Bool) :
    Not (forall c : RoleFidelityCase, classify c.signals = c.roleIdentityPreserved) := by
  intro exactClassifier
  have left := exactClassifier sameMetricsWithRoleFidelity
  have right := exactClassifier sameMetricsWithRoleCollapse
  simp [sameMetricsWithRoleFidelity, sameMetricsWithRoleCollapse] at left right
  rw [left] at right
  simp at right

structure RescueSignals where
  namedRescueCount : Nat
  matchedBudgetClaimed : Bool
deriving DecidableEq, Repr
structure RescueCompetenceCase where
  signals : RescueSignals
  lowerOrderRescuesCompetent : Bool
deriving DecidableEq, Repr

def namedRescuesActuallyCompetent : RescueCompetenceCase :=
  { signals := { namedRescueCount := 7, matchedBudgetClaimed := true },
    lowerOrderRescuesCompetent := true }
def namedRescuesOnlyNominal : RescueCompetenceCase :=
  { signals := { namedRescueCount := 7, matchedBudgetClaimed := true },
    lowerOrderRescuesCompetent := false }

theorem identical_rescue_records_can_hide_opposite_rescue_competence :
    namedRescuesActuallyCompetent.signals = namedRescuesOnlyNominal.signals ∧
      namedRescuesActuallyCompetent.lowerOrderRescuesCompetent ≠
        namedRescuesOnlyNominal.lowerOrderRescuesCompetent := by decide

theorem rescue_records_cannot_recover_lower_order_competence
    (classify : RescueSignals -> Bool) :
    Not (forall c : RescueCompetenceCase,
      classify c.signals = c.lowerOrderRescuesCompetent) := by
  intro exactClassifier
  have left := exactClassifier namedRescuesActuallyCompetent
  have right := exactClassifier namedRescuesOnlyNominal
  simp [namedRescuesActuallyCompetent, namedRescuesOnlyNominal] at left right
  rw [left] at right
  simp at right

def substrateConsumerWithoutBaseline : SearchSubstrates.SubstrateAdoptionRecord :=
  { baselineRefsPresent := false, measuredTargetDeclared := true,
    falsificationCriterionDeclared := true }

theorem missing_lower_order_rescue_rejects_substrate_consumer :
    Not (SearchSubstrates.AdoptionFieldsComplete substrateConsumerWithoutBaseline) := by
  apply SearchSubstrates.substrate_adoption_record_missing_required_field_rejected
  exact Or.inl rfl

def routingConsumerWithoutQualifiedCompiler : Routing.RoutingDecisionReview :=
  { Routing.completeRoutingDecisionReview with readinessSatisfied := false }

theorem unqualified_compiler_routes_runtime_to_fallback :
    Routing.RoutingDecisionRouteFor routingConsumerWithoutQualifiedCompiler =
      .routeToFallback := by decide

def evidenceWithoutCompilerExperiment : EvidenceBundle :=
  { sourceNote := True, prototypeInspection := True, syntheticTestRun := True,
    empiricalTestRun := False, externalLiterature := True }

theorem missing_compiler_experiment_blocks_empirical_support_promotion :
    Not (PromotionAllowed evidenceWithoutCompilerExperiment
      SupportState.argument SupportState.empiricalTestBacked) := by
  apply missing_required_evidence_blocks_promotion
  simp [RequiredEvidence, evidenceWithoutCompilerExperiment]

end AsiStackProofs.RelationalDimensionCompiler
