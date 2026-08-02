namespace AsiStackProofs.HiveLifecycleRefinement

inductive Stage where | requested | policyBound | nodeSelected | leased | executed | reconciled | closed
deriving DecidableEq, Repr
inductive EventKind where | bindPolicy | selectNode | issueLease | execute | reconcile | close
deriving DecidableEq, Repr
inductive Route where
 | rejectWrongStage | rejectJobSubstitution | rejectNodeSubstitution | rejectEventReplay | rejectAuthorityLeak
 | rejectMalformedJob | requireIdentityPolicy | requireDataPolicy | requireToolPolicy | requireApprovalPolicy
 | requireDeviceRegistry | requireSchedulerPolicy | requireCandidateDenominator | requireLeastAuthority
 | requireDataLocality | requireCostBudget | requireEnergyBudget | requireDropoutPlan
 | requireFederationLease | requireSandbox | requireLeaseScope | requireEvidenceObligations
 | requireExpiration | requireRevocationPath
 | requireBoundApproval | requireFreshGrant | quarantinePartition | requireNoMutationEvidence
 | requireExecutionGrant | requireMonitor
 | requireArtifactReceipt | requireEffectReceipt | requireResourceReceipt | requireAuditReceipt
 | requireUsefulOutcome | requireResidualOwner
 | requireDropoutRecovery | requireRevocationClosure | requireDescendantClosure
 | requireConsumerAcknowledgment | requireNonClaims
 | acceptPolicy | acceptSelection | acceptLease | acceptExecution | acceptReconciliation | acceptClosure
deriving DecidableEq, Repr

structure Packet where
 jobId : Nat
 jobVersion : Nat
 principalDigest : Nat
 contractDigest : Nat
 nodeRegistryDigest : Nat
 candidateSetDigest : Nat
 selectedNodeDigest : Nat
 policyDigest : Nat
 authorityDigest : Nat
 leaseDigest : Nat
 evaluatorDigest : Nat
 consumerDigest : Nat
 residualDigest : Nat
 eventDigest : Nat
 jobWellFormed : Bool
 identityPolicy : Bool
 dataPolicy : Bool
 toolPolicy : Bool
 approvalPolicy : Bool
 deviceRegistry : Bool
 schedulerPolicy : Bool
 candidateDenominator : Bool
 leastAuthority : Bool
 dataLocality : Bool
 costBudget : Bool
 energyBudget : Bool
 dropoutPlan : Bool
 externalAccess : Bool
 federationLease : Bool
 sandbox : Bool
 leaseScope : Bool
 evidenceObligations : Bool
 expiration : Bool
 revocationPath : Bool
 highRisk : Bool
 boundApproval : Bool
 freshGrant : Bool
 partitionDetected : Bool
 staleGrantPossible : Bool
 deniedBeforeMutation : Bool
 stateUnchanged : Bool
 executionGrant : Bool
 monitor : Bool
 artifactReceipt : Bool
 effectReceipt : Bool
 resourceReceipt : Bool
 auditReceipt : Bool
 usefulOutcome : Bool
 residualOwner : Bool
 dropoutRecovery : Bool
 revocationClosure : Bool
 descendantClosure : Bool
 consumerAcknowledgment : Bool
 nonClaims : Bool
 supportAssignmentRequested : Bool
 externalEffectRequested : Bool
deriving DecidableEq, Repr
structure Event where
 kind : EventKind
 packet : Packet
deriving DecidableEq, Repr
structure State where
 stage : Stage
 jobId : Nat
 jobVersion : Nat
 principalDigest : Nat
 contractDigest : Nat
 nodeRegistryDigest : Nat
 candidateSetDigest : Nat
 selectedNodeDigest : Nat
 policyDigest : Nat
 authorityDigest : Nat
 leaseDigest : Nat
 evaluatorDigest : Nat
 consumerDigest : Nat
 residualDigest : Nat
 lastEventDigest : Nat
 receiptCount : Nat
 dispatchCount : Nat
 usefulOutcomeCount : Nat
 quarantineCount : Nat
 recoveryCount : Nat
 supportAssignmentCount : Nat
 externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
 | .requested=>.bindPolicy | .policyBound=>.selectNode | .nodeSelected=>.issueLease
 | .leased=>.execute | .executed=>.reconcile | .reconciled=>.close | .closed=>.close
def exactJob (s:State) (p:Packet):Bool := p.jobId==s.jobId && p.jobVersion==s.jobVersion && p.principalDigest==s.principalDigest && p.contractDigest==s.contractDigest && p.policyDigest==s.policyDigest && p.authorityDigest==s.authorityDigest && p.evaluatorDigest==s.evaluatorDigest && p.consumerDigest==s.consumerDigest && p.residualDigest==s.residualDigest
def exactNode (s:State) (p:Packet):Bool := p.nodeRegistryDigest==s.nodeRegistryDigest && p.candidateSetDigest==s.candidateSetDigest && p.selectedNodeDigest==s.selectedNodeDigest && p.leaseDigest==s.leaseDigest
def routeFor (s:State) (e:Event):Route :=
 if e.kind != expectedKind s.stage then .rejectWrongStage
 else if !exactJob s e.packet then .rejectJobSubstitution
 else if !exactNode s e.packet then .rejectNodeSubstitution
 else if e.packet.eventDigest==s.lastEventDigest then .rejectEventReplay
 else if e.packet.supportAssignmentRequested || e.packet.externalEffectRequested then .rejectAuthorityLeak
 else match s.stage with
 | .requested => if !e.packet.jobWellFormed then .rejectMalformedJob else if !e.packet.identityPolicy then .requireIdentityPolicy else if !e.packet.dataPolicy then .requireDataPolicy else if !e.packet.toolPolicy then .requireToolPolicy else if !e.packet.approvalPolicy then .requireApprovalPolicy else .acceptPolicy
 | .policyBound => if !e.packet.deviceRegistry then .requireDeviceRegistry else if !e.packet.schedulerPolicy then .requireSchedulerPolicy else if !e.packet.candidateDenominator then .requireCandidateDenominator else if !e.packet.leastAuthority then .requireLeastAuthority else if !e.packet.dataLocality then .requireDataLocality else if !e.packet.costBudget then .requireCostBudget else if !e.packet.energyBudget then .requireEnergyBudget else if !e.packet.dropoutPlan then .requireDropoutPlan else .acceptSelection
 | .nodeSelected => if e.packet.externalAccess && !e.packet.federationLease then .requireFederationLease else if !e.packet.sandbox then .requireSandbox else if !e.packet.leaseScope then .requireLeaseScope else if !e.packet.evidenceObligations then .requireEvidenceObligations else if !e.packet.expiration then .requireExpiration else if !e.packet.revocationPath then .requireRevocationPath else .acceptLease
 | .leased => if e.packet.highRisk && !e.packet.boundApproval then .requireBoundApproval else if !e.packet.freshGrant then .requireFreshGrant else if e.packet.partitionDetected && e.packet.staleGrantPossible then (if e.packet.deniedBeforeMutation && e.packet.stateUnchanged then .quarantinePartition else .requireNoMutationEvidence) else if !e.packet.executionGrant then .requireExecutionGrant else if !e.packet.monitor then .requireMonitor else .acceptExecution
 | .executed => if !e.packet.artifactReceipt then .requireArtifactReceipt else if !e.packet.effectReceipt then .requireEffectReceipt else if !e.packet.resourceReceipt then .requireResourceReceipt else if !e.packet.auditReceipt then .requireAuditReceipt else if !e.packet.usefulOutcome then .requireUsefulOutcome else if !e.packet.residualOwner then .requireResidualOwner else .acceptReconciliation
 | .reconciled => if !e.packet.dropoutRecovery then .requireDropoutRecovery else if !e.packet.revocationClosure then .requireRevocationClosure else if !e.packet.descendantClosure then .requireDescendantClosure else if !e.packet.consumerAcknowledgment then .requireConsumerAcknowledgment else if !e.packet.nonClaims then .requireNonClaims else .acceptClosure
 | .closed => .rejectWrongStage
def accepted:Route->Bool | .acceptPolicy|.acceptSelection|.acceptLease|.acceptExecution|.acceptReconciliation|.acceptClosure=>true|_=>false
def advance:Stage->Stage |.requested=>.policyBound|.policyBound=>.nodeSelected|.nodeSelected=>.leased|.leased=>.executed|.executed=>.reconciled|.reconciled=>.closed|.closed=>.closed
def applyEvent(s:State)(e:Event):State×Route :=
 let r:=routeFor s e
 if accepted r then
  ({s with
    stage:=advance s.stage
    lastEventDigest:=e.packet.eventDigest
    receiptCount:=s.receiptCount+1
    dispatchCount:=if s.stage==.leased then s.dispatchCount+1 else s.dispatchCount
    usefulOutcomeCount:=if s.stage==.executed then s.usefulOutcomeCount+1 else s.usefulOutcomeCount
    recoveryCount:=if s.stage==.reconciled then s.recoveryCount+1 else s.recoveryCount},r)
 else (s,r)

structure StateIdentity where
 jobId : Nat
 jobVersion : Nat
 principalDigest : Nat
 contractDigest : Nat
 nodeRegistryDigest : Nat
 candidateSetDigest : Nat
 selectedNodeDigest : Nat
 policyDigest : Nat
 authorityDigest : Nat
 leaseDigest : Nat
 evaluatorDigest : Nat
 consumerDigest : Nat
 residualDigest : Nat
deriving DecidableEq, Repr

def stateIdentity (s : State) : StateIdentity :=
 { jobId := s.jobId
   jobVersion := s.jobVersion
   principalDigest := s.principalDigest
   contractDigest := s.contractDigest
   nodeRegistryDigest := s.nodeRegistryDigest
   candidateSetDigest := s.candidateSetDigest
   selectedNodeDigest := s.selectedNodeDigest
   policyDigest := s.policyDigest
   authorityDigest := s.authorityDigest
   leaseDigest := s.leaseDigest
   evaluatorDigest := s.evaluatorDigest
   consumerDigest := s.consumerDigest
   residualDigest := s.residualDigest }

def HiveStep (s : State) (e : Event) : Option State :=
 if s.stage = .closed then none
 else if accepted (routeFor s e) then some (applyEvent s e).1 else none

def HiveRun : State -> List Event -> Option State
 | state, [] => some state
 | state, event :: tail =>
     match HiveStep state event with
     | none => none
     | some next => HiveRun next tail

def HiveTraceAccepted : State -> List Event -> Prop
 | _, [] => True
 | state, event :: tail =>
     accepted (routeFor state event) = true ∧
     HiveTraceAccepted (applyEvent state event).1 tail

theorem accepted_step_is_accepted
    {state next : State} {event : Event}
    (stepped : HiveStep state event = some next) :
    accepted (routeFor state event) = true := by
  unfold HiveStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · assumption
    · simp at stepped

theorem accepted_step_applies_event
    {state next : State} {event : Event}
    (stepped : HiveStep state event = some next) :
    next = (applyEvent state event).1 := by
  unfold HiveStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · exact Option.some.inj stepped |>.symm
    · simp at stepped

theorem apply_event_preserves_full_identity (state : State) (event : Event) :
    stateIdentity (applyEvent state event).1 = stateIdentity state := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, h, stateIdentity]

theorem accepted_step_preserves_full_identity
    {state next : State} {event : Event}
    (stepped : HiveStep state event = some next) :
    stateIdentity next = stateIdentity state := by
  rw [accepted_step_applies_event stepped]
  exact apply_event_preserves_full_identity state event

theorem accepted_step_preserves_support_and_external_effect_counts
    {state next : State} {event : Event}
    (stepped : HiveStep state event = some next) :
    next.supportAssignmentCount = state.supportAssignmentCount ∧
    next.externalEffectCount = state.externalEffectCount := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_step_adds_exactly_one_receipt
    {state next : State} {event : Event}
    (stepped : HiveStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_step_advances_stage
    {state next : State} {event : Event}
    (stepped : HiveStep state event = some next) :
    next.stage = advance state.stage := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_run_preserves_full_identity
    {state final : State} {events : List Event}
    (ran : HiveRun state events = some final) :
    stateIdentity final = stateIdentity state := by
  induction events generalizing state with
  | nil => simp [HiveRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : HiveStep state event with
      | none => simp [HiveRun, stepped] at ran
      | some next =>
          have tailRan : HiveRun next tail = some final := by
            simpa [HiveRun, stepped] using ran
          exact (ih tailRan).trans (accepted_step_preserves_full_identity stepped)

theorem accepted_run_preserves_support_count
    {state final : State} {events : List Event}
    (ran : HiveRun state events = some final) :
    final.supportAssignmentCount = state.supportAssignmentCount := by
  induction events generalizing state with
  | nil => simp [HiveRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : HiveStep state event with
      | none => simp [HiveRun, stepped] at ran
      | some next =>
          have tailRan : HiveRun next tail = some final := by
            simpa [HiveRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_step_preserves_support_and_external_effect_counts stepped).1

theorem accepted_run_preserves_external_effect_count
    {state final : State} {events : List Event}
    (ran : HiveRun state events = some final) :
    final.externalEffectCount = state.externalEffectCount := by
  induction events generalizing state with
  | nil => simp [HiveRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : HiveStep state event with
      | none => simp [HiveRun, stepped] at ran
      | some next =>
          have tailRan : HiveRun next tail = some final := by
            simpa [HiveRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_step_preserves_support_and_external_effect_counts stepped).2

theorem accepted_run_accounts_exact_receipts
    {state final : State} {events : List Event}
    (ran : HiveRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil => simp [HiveRun] at ran; subst final; simp
  | cons event tail ih =>
      cases stepped : HiveStep state event with
      | none => simp [HiveRun, stepped] at ran
      | some next =>
          have tailRan : HiveRun next tail = some final := by
            simpa [HiveRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [accepted_step_adds_exactly_one_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem accepted_run_has_accepted_trace
    {state final : State} {events : List Event}
    (ran : HiveRun state events = some final) :
    HiveTraceAccepted state events := by
  induction events generalizing state with
  | nil => simp [HiveTraceAccepted]
  | cons event tail ih =>
      cases stepped : HiveStep state event with
      | none => simp [HiveRun, stepped] at ran
      | some next =>
          have tailRan : HiveRun next tail = some final := by
            simpa [HiveRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          subst next
          exact ⟨accepted_step_is_accepted stepped, ih tailRan⟩

theorem hive_run_append
    (state middle : State) (left right : List Event)
    (leftRan : HiveRun state left = some middle) :
    HiveRun state (left ++ right) = HiveRun middle right := by
  induction left generalizing state with
  | nil => simp [HiveRun] at leftRan; subst middle; rfl
  | cons event tail ih =>
      cases stepped : HiveStep state event with
      | none => simp [HiveRun, stepped] at leftRan
      | some next =>
          have tailRan : HiveRun next tail = some middle := by
            simpa [HiveRun, stepped] using leftRan
          simpa [HiveRun, stepped] using ih next tailRan

theorem closed_state_accepts_no_event
    {state : State} (closed : state.stage = .closed) (event : Event) :
    HiveStep state event = none := by
  simp [HiveStep, closed]

theorem apply_event_preserves_job_node_lease_identity (s : State) (e : Event) :
    (applyEvent s e).1.jobId = s.jobId ∧
    (applyEvent s e).1.selectedNodeDigest = s.selectedNodeDigest ∧
    (applyEvent s e).1.leaseDigest = s.leaseDigest ∧
    (applyEvent s e).1.residualDigest = s.residualDigest := by
  by_cases h : accepted (routeFor s e) = true <;> simp [applyEvent, h]
theorem apply_event_cannot_assign_support_or_external_effect (s : State) (e : Event) :
    (applyEvent s e).1.supportAssignmentCount = s.supportAssignmentCount ∧
    (applyEvent s e).1.externalEffectCount = s.externalEffectCount := by
  by_cases h : accepted (routeFor s e) = true <;> simp [applyEvent, h]
theorem accepted_step_adds_one_receipt (s : State) (e : Event)
    (h : accepted (routeFor s e) = true) :
    (applyEvent s e).1.receiptCount = s.receiptCount + 1 := by simp [applyEvent, h]

def p:Packet := {jobId:=1001,jobVersion:=2,principalDigest:=1002,contractDigest:=1003,nodeRegistryDigest:=1004,candidateSetDigest:=1005,selectedNodeDigest:=1006,policyDigest:=1007,authorityDigest:=1008,leaseDigest:=1009,evaluatorDigest:=1010,consumerDigest:=1011,residualDigest:=1012,eventDigest:=1,jobWellFormed:=true,identityPolicy:=true,dataPolicy:=true,toolPolicy:=true,approvalPolicy:=true,deviceRegistry:=true,schedulerPolicy:=true,candidateDenominator:=true,leastAuthority:=true,dataLocality:=true,costBudget:=true,energyBudget:=true,dropoutPlan:=true,externalAccess:=false,federationLease:=true,sandbox:=true,leaseScope:=true,evidenceObligations:=true,expiration:=true,revocationPath:=true,highRisk:=false,boundApproval:=true,freshGrant:=true,partitionDetected:=false,staleGrantPossible:=false,deniedBeforeMutation:=true,stateUnchanged:=true,executionGrant:=true,monitor:=true,artifactReceipt:=true,effectReceipt:=true,resourceReceipt:=true,auditReceipt:=true,usefulOutcome:=true,residualOwner:=true,dropoutRecovery:=true,revocationClosure:=true,descendantClosure:=true,consumerAcknowledgment:=true,nonClaims:=true,supportAssignmentRequested:=false,externalEffectRequested:=false}
def s(stage:Stage):State := {stage:=stage,jobId:=1001,jobVersion:=2,principalDigest:=1002,contractDigest:=1003,nodeRegistryDigest:=1004,candidateSetDigest:=1005,selectedNodeDigest:=1006,policyDigest:=1007,authorityDigest:=1008,leaseDigest:=1009,evaluatorDigest:=1010,consumerDigest:=1011,residualDigest:=1012,lastEventDigest:=0,receiptCount:=0,dispatchCount:=0,usefulOutcomeCount:=0,quarantineCount:=0,recoveryCount:=0,supportAssignmentCount:=0,externalEffectCount:=0}
theorem malformed_job_rejected : routeFor (s .requested) {kind:=.bindPolicy,packet:={p with jobWellFormed:=false}} = .rejectMalformedJob := by rfl
theorem missing_data_policy_blocks_binding : routeFor (s .requested) {kind:=.bindPolicy,packet:={p with dataPolicy:=false}} = .requireDataPolicy := by rfl
theorem incomplete_candidate_denominator_blocks_selection : routeFor (s .policyBound) {kind:=.selectNode,packet:={p with candidateDenominator:=false}} = .requireCandidateDenominator := by rfl
theorem overprivileged_node_blocks_selection : routeFor (s .policyBound) {kind:=.selectNode,packet:={p with leastAuthority:=false}} = .requireLeastAuthority := by rfl
theorem external_access_without_lease_blocks_issue : routeFor (s .nodeSelected) {kind:=.issueLease,packet:={p with externalAccess:=true,federationLease:=false}} = .requireFederationLease := by rfl
theorem missing_sandbox_blocks_lease : routeFor (s .nodeSelected) {kind:=.issueLease,packet:={p with sandbox:=false}} = .requireSandbox := by rfl
theorem high_risk_without_bound_approval_blocks_execution : routeFor (s .leased) {kind:=.execute,packet:={p with highRisk:=true,boundApproval:=false}} = .requireBoundApproval := by rfl
theorem partitioned_stale_grant_quarantines_before_mutation : routeFor (s .leased) {kind:=.execute,packet:={p with partitionDetected:=true,staleGrantPossible:=true}} = .quarantinePartition := by rfl
theorem partition_without_no_mutation_evidence_blocks : routeFor (s .leased) {kind:=.execute,packet:={p with partitionDetected:=true,staleGrantPossible:=true,deniedBeforeMutation:=false}} = .requireNoMutationEvidence := by rfl
theorem missing_effect_receipt_blocks_reconciliation : routeFor (s .executed) {kind:=.reconcile,packet:={p with effectReceipt:=false}} = .requireEffectReceipt := by rfl
theorem missing_useful_outcome_blocks_reconciliation : routeFor (s .executed) {kind:=.reconcile,packet:={p with usefulOutcome:=false}} = .requireUsefulOutcome := by rfl
theorem missing_dropout_recovery_blocks_closure : routeFor (s .reconciled) {kind:=.close,packet:={p with dropoutRecovery:=false}} = .requireDropoutRecovery := by rfl
theorem missing_revocation_closure_blocks_closure : routeFor (s .reconciled) {kind:=.close,packet:={p with revocationClosure:=false}} = .requireRevocationClosure := by rfl
def ev (k : EventKind) (d : Nat) : Event := {kind:=k,packet:={p with eventDigest:=d}}
theorem full_hive_lifecycle_reaches_closed_state :
  let s0:=s .requested
  let s1:=(applyEvent s0 (ev .bindPolicy 1)).1
  let s2:=(applyEvent s1 (ev .selectNode 2)).1
  let s3:=(applyEvent s2 (ev .issueLease 3)).1
  let s4:=(applyEvent s3 (ev .execute 4)).1
  let s5:=(applyEvent s4 (ev .reconcile 5)).1
  let s6:=(applyEvent s5 (ev .close 6)).1
  s6.stage=.closed ∧ s6.receiptCount=6 ∧ s6.dispatchCount=1 ∧
  s6.usefulOutcomeCount=1 ∧ s6.recoveryCount=1 ∧
  s6.supportAssignmentCount=0 ∧ s6.externalEffectCount=0 := by native_decide
end AsiStackProofs.HiveLifecycleRefinement
