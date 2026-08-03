#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_proof_depth import CLASSIFICATION_PHRASE, DECL_RE, SAFETY_CRITICAL_MODULES, THEOREM_RE, classify_body


ROOT = Path(__file__).resolve().parents[1]
LEAN_DIR = ROOT / "lean" / "AsiStackProofs"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
CLAIMS = ROOT / "evidence_quality" / "claim_atom_registry.json"
REVIEWS = ROOT / "proofs" / "proof_rationalization_reviews.json"
REGISTRY = ROOT / "proofs" / "proof_rationalization_registry.json"
REPORT = ROOT / "docs" / "proof_rationalization_registry.md"
DOSSIERS = ROOT / "evidence_quality" / "proof_model_dossiers"
ROADMAP_ID = "asi-stack-post-v2-3-claim-proof-sota-challenge-2026-07-14"

CURRENT_REFINEMENTS = {
    "labor-os-and-typed-jobs": """## Current refinement

`AsiStackProofs.TypedJobRefinement` now adds a stage-indexed lifecycle invariant
and arbitrary-run semantics to the seven-stage job model. Thirty-two exact
declarations prove rejection noninterference, terminal closure, one-step and
arbitrary-run preservation of receipt and represented execution-observation
accounting, zero support and external-effect authority, and full job, contract,
plan, authority, permission, lease, scheduler, and consumer custody. One
six-event run reaches exact acknowledged closure; nineteen closed route or
state countermodels cover approval, lease, retry, cancellation, evidence,
identity, replay, authority-leak, audit, completion-receipt, residual, and
post-closure failures.

`scripts/validate_typed_job_refinement.py` requires and compiles the exact
thirty-two-declaration surface, rejects unproved declarations, consumes the
2/7 delivery and 2/9 durable suites, independently checks all twenty-nine
routes, and rejects 42 mutations. Every identity, approval, permission, lease,
scheduler, idempotency, cancellation, artifact, audit, verifier, receipt,
replay, residual, and acknowledgment field remains authored. The model proves
no scheduler or worker behavior, permission or approval enforcement, effect
truth, idempotence, recovery or cancellation efficacy, artifact or replay
truth, useful work, support transition, deployment, reproduction, or transfer.
Those obligations remain Project Theseus or empirical work. Chapter support
remains `argument` and `support_state_effect` remains `none`.

""",
    "intent-to-execution-contracts": """## Current refinement

`AsiStackProofs.IntentExecutionRefinement` now gives every event kind an exact,
exclusive payload contract, closing the prior path by which a lowering event
could carry effect, observation, delivery, residual, or rollback data. Its
thirty-seven declarations prove one-step and arbitrary-run preservation of the
vertical invariant, root-contract and authority-ceiling custody, monotone
logical time, bounded active authority, effect-attempt and observation
accounting, approval and dispatch custody, artifact and independent-verification
custody, exact delivery accounting, stopped blocking, positive residualization,
and failed-rollback quarantine. The existing ten-event witness reaches delivery;
eighteen closed countermodels reject custody substitution, stale time,
kind-invalid payloads, premature lifecycle transitions, self-verification,
inexact rollback, and quarantine without a residual.

`scripts/validate_intent_execution_vertical_refinement.py` requires the exact
thirty-seven-declaration theorem surface, rejects unproved declarations,
compiles the module, and independently checks nine executed scenarios, 89
events, six material effects, and thirty concrete source mutations. The model
trusts authored event kinds, contract and artifact identities, authority,
receipts, observations, verifier identity, rollback, and residual fields. It
proves no parser correctness, natural-language or arbitrary semantic
equivalence, authentic authority, approval-service behavior, tool-effect truth,
verifier competence, rollback efficacy, useful delivery, support transition,
deployment, reproduction, or transfer. Those behavioral and cross-component
obligations belong to Project Theseus or empirical evaluation. Chapter support
remains `argument` and `support_state_effect` remains `none`.

""",
    "planning-as-a-control-layer": """## Current refinement

`AsiStackProofs.Planning` now adds a reachable command, admission, readiness,
job-lowering, feedback, replanning, and blocking model to the retained finite
record routes. Twenty-one declarations prove local and arbitrary-run
preservation of authority ceilings, ready-before-lower ordering,
feedback-before-replan ordering, exact plan-version accounting, stop-condition
preservation, dispatch-state obligations, and residual growth. One seven-event
witness reaches a second lowered job after scoped replanning; eleven closed
countermodels reject authority widening, incomplete decomposition, missing
context, inadequate routing, missing or blocked dispatch, premature feedback,
stop erasure, unscoped repair, missing residuals, and hidden overrides. The
admission and job-lowering events also refine the independently owned
`AsiStackProofs.IntentExecutionRefinement` vertical transition model.

`scripts/validate_planning_scheduler_state_probe.py` requires the exact
forty-eight-declaration Planning surface and independently checks two accepted
and seven rejected scheduler fixtures. The runtime-replan consumer requires the
replan-specific theorem subset and checks two accepted and nine rejected delta
fixtures. The model trusts authored decomposition, dependency, context,
adequacy, route, receipt, authority, stop, and residual fields. It proves no
decomposition quality, dependency truth, context-demand prediction, selected
tier or route adequacy, scheduler optimality, live feedback handling, deployed
replanning, causal advantage, support transition, reproduction, or transfer.
Chapter support remains `argument` and `support_state_effect` remains `none`.

""",
    "human-factors-and-meaningful-control-in-oversight": """## Current refinement

`AsiStackProofs.HumanFactorsOversight` now adds a reachable briefing, decision,
intervention, response-observation, accountability, and blocking lifecycle to
the retained admission router. Twenty-three new declarations prove one-step and
arbitrary-run preservation of exact review identity, authority-ceiling custody,
authority bounds, control-opportunity and receipt ordering, accountability
ancestry, and zero
support or release authority. One five-event witness reaches accountability
closure. Thirteen closed countermodels reject reviewer or action substitution,
overload, lateness, missing comprehension acknowledgement, independent
challenge, or override path, authority widening, premature intervention or
observation, missing intervention receipt, and accountability without a
control opportunity or observed response. Blocking revokes active modeled
authority and records a residual.

`scripts/validate_human_oversight_control_contract.py` requires the exact
thirty-two-declaration surface, compiles the module, preserves the closed
human-subjects protocol, and independently rejects fifteen record mutations.
The model trusts every authored identity, workload, timing, comprehension,
challenge, authority, intervention, observation, and accountability field. It
proves no actual comprehension, calibrated workload, reviewer competence,
automation-bias resistance, intervention efficacy, outcome truth, moral or
legal responsibility, meaningful control, safety, support transition,
deployment, reproduction, or transfer. Representative human measurement
remains empirical, and cross-component behavior remains Project Theseus work.
Chapter support remains `argument` and `support_state_effect` remains `none`.

""",
    "runtime-adapters-tool-permissions-and-human-approval": """## Current refinement

`AsiStackProofs.RuntimeAdapters` now adds a reachable prepare, approve,
dispatch, commit, observe, revoke, and rollback model to the retained finite
route surfaces. Twenty-five declarations prove one-step and arbitrary-run
preservation of exact active-lease, approval, dispatch, caller-ceiling, epoch,
revocation, and observed-effect accounting invariants. Projection commutes with
every transition, and accepted adapter events and arbitrary runs simulate
`AsiStackProofs.AuthorityEffectRefinement`. One six-event witness reaches exact
baseline restoration; eleven closed countermodels reject permission, identity,
authority, expiry, secret, dispatch, rollback, pre-state, and revocation
failures.

`scripts/validate_runtime_adapter_permissions.py` independently checks the
existing two valid and seven expected-invalid fixtures and requires the exact
refinement theorem surface. The model trusts authored identities, permissions,
sandbox observations, receipts, digests, and observer fields. It proves no OS
or hardware enforcement, approval or reviewer competence, secret-broker
security, target-service effect truth, distributed revocation, effect-complete
rollback, useful-action advantage, support transition, deployment,
reproduction, or transfer. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "failure-modes-of-ungoverned-intelligence": """## Current refinement

`AsiStackProofs.FailureRecoveryRefinement` supplies the stronger model requested
by the baseline review. Its five reachable stages preserve rejected state,
disable modeled effects after accepted detection, guard readmission through
exact identity plus remediation, independent review, current assurance and
taxonomy, residual custody, and authority, and re-isolate one bounded
recurrence. `scripts/validate_failure_recovery_refinement.py` independently
encodes the transition system and rejects 31 mutations. The bounded model has
`support_state_effect=none`: detector truth, containment and remediation
effectiveness, deployed recovery, safety, and transfer remain Theseus or
empirical obligations.

""",
    "mathematical-and-search-substrates": """## Current refinement

`AsiStackProofs.SearchSubstrates.classifyAdoptionTrace` replaces the retired
authored summary with a reachable classifier over baseline, negative-control,
falsification, proof-boundary, fallback, retirement, residual, support,
non-claim, workload, result, axis, permission, and adoption-state fields.
Four closed witnesses derive exploratory registration, structural-only receipt,
consumer-axis blocking, and failed-control retirement. Eight closed controls
derive exact rejections for missing baseline, missing falsification, theorem
spillover, unmeasured-axis routing, failed-control promotion, missing fallback,
support promotion, and missing non-claim boundaries. Route algebra proves that
only measured-permission constructors can authorize a consumer and that
rejecting routes never can. `scripts/validate_substrate_adoption_trace.py`
independently re-encodes all twelve public trace decisions.

The Lean model trusts every input field. It proves no workload result,
substrate advantage, representation or runtime property, transfer, support
transition, release authority, AGI, or ASI. `support_state_effect` remains
`none` and chapter support remains `argument`.

""",
    "artifact-steward-agents-and-living-project-governance": """## Current refinement

`AsiStackProofs.ArtifactStewardAgents` now adds two finite reachable transition
models to the retained lifecycle, contribution-ledger, and federation routes.
The work-contract model derives repair, refusal, approval, or dispatch readiness
from objective, authority, tool, verification, budget, rollback, and non-claim
fields. The release model derives repair, refusal, approval, or external-review
readiness from artifact, test, evidence, changelog, residual, approval,
no-promotion, and non-claim fields. Safety predicates are preserved over
arbitrary-length runs, so either readiness state implies a complete modeled
packet. Closed countermodels exercise every named missing boundary.

`scripts/validate_artifact_steward_lifecycle_probe.py` independently re-encodes
seventeen exact boundary mutations and checks three accepted plus twenty-three
expected-invalid public scenarios. Both formal models stop before execution or
publication. They prove no field truth, worker or tool behavior, treasury
safety, governance legitimacy, project quality, release safety, support
transition, deployment, transfer, AGI, or ASI. Chapter support remains
`argument` and `support_state_effect` remains `none`.

""",
    "human-ai-organizations-delegation-and-accountability": """## Current refinement

`AsiStackProofs.HumanAIOrganizations` implements a five-stage finite review
from proposed accountability through identity, capacity, authority,
independence, remedy/custody, and assignment readiness. A stage invariant is
preserved by one transition and by induction over arbitrary finite run length;
any reachable `accountabilityAssignable` state therefore requires all twenty
authored fields. One complete witness reaches readiness and twenty closed
mutations reach exact refusal or repair states.

A separate ten-stage delegation-to-remedy lifecycle binds nine identities from
delegation through activation, escalation, handoff, contestation, authority
expiry, incident reconstruction, remedy, and closure. Arbitrary successful
runs preserve identity and zero support/external-effect authority, account for
exact receipts, keep contest and remedy receipts monotone, expose accepted
traces, compose across event batches, and stop at closure. One nine-event
adverse-path witness closes with authority zero; the independent consumer
reaches all 39 routes and rejects 156/156 lifecycle mutations.

The model checks only authored Boolean fields. It proves no field truth,
reviewer competence, practical human intervention, lawful or legitimate
accountability, organizational effectiveness, worker welfare, fairness,
resilience, support transition, external effect, deployment, AGI, or ASI.
Chapter support remains `argument` and `support_state_effect` remains `none`.

""",
    "multi-agent-dynamics-collective-intelligence-and-systemic-risk": """## Current refinement

`AsiStackProofs.MultiAgentDynamics` implements a finite three-party population
review over six directed pairwise-authorization edges and nine systemic axes.
Two closed records expose identical pairwise evidence but opposite campaign-
readiness decisions, proving that no classifier restricted to that matrix can
exactly recover the ten-dimension review for every modeled record. Nine
systemic-axis mutations preserve pairwise validity, fail readiness, and reach
exact repair routes; the only accepted route starts a Project Theseus
population campaign.

The model trusts every authored identity, lineage, control, coverage, exit,
recovery, custody, and boundary field. It proves no beneficial cooperation,
non-collusion, collective competence, systemic safety, effective human agency,
institutional legitimacy or outcome, social prediction, support transition,
external effect, deployment, AGI, or ASI. Chapter support remains `argument`
and `support_state_effect` remains `none`.

""",
    "dangerous-capability-domains-and-misuse-uplift": """## Current refinement

`AsiStackProofs.DangerousCapabilityReview` implements a seven-stage finite
pre-campaign review over exact identity, threat, domain, cohort, expertise,
baseline, elicitation, control, attempt, outcome-axis, evaluator, custody,
uncertainty, expiry, maximum-inference, residual, non-claim, and non-authority
fields. One complete dossier reaches only a Project Theseus harmless-analogue
campaign. All 29 admission-axis mutations fail readiness and reach exact repair
or refusal routes; two arithmetic monotonicity laws preserve expiry and attempt-
shortfall rejection under adverse changes.

Two same-total witnesses require opposite component-sensitive review decisions,
and a universal theorem proves that no classifier restricted to the aggregate
score is exact for every modeled outcome vector. The independently encoded
consumer reconstructs the route, mutation, arithmetic, and scalar-collision
surfaces from a generic public fixture. Authored fields remain assumptions: no
result truth, dangerous capability, uplift, safeguard efficacy, harm, safety,
threshold, support, release, transfer, or external effect follows. Chapter
support remains `argument` and `support_state_effect` remains `none`.

The independent consumer checks 29 exact mutation routes, two arithmetic monotonicity controls, and one aggregate-score impossibility result.

""",
    "military-ai-autonomous-weapons-and-strategic-stability": """## Current refinement

`AsiStackProofs.MilitaryInteractionReview` implements an eight-step finite
non-operational dossier lifecycle over public-safe scope, mission and role,
affected population, legal boundary, accountable authority, effect envelope,
meaningful-judgment conditions, observation trust, safe posture, interaction
assumptions, evidence custody, expiry, public maximum inference, remedy,
decommission, residuals, and explicit non-authority fields. One complete
dossier reaches only a Project Theseus public-safe simulation. All 45 admission-
axis mutations block readiness and lifecycle eligibility while the diagnostic
function returns 45 exact mutation dispositions.

Three arithmetic monotonicity controls preserve rejection under later time,
lower available decision time, and fewer available off-ramps. Two impossibility
results show that identical interface presence can hide opposite meaningful-
judgment decisions and that identical local component evidence can hide
opposite strategic-interaction reviews. The independent consumer reconstructs
the full mutation, monotonicity, and collision surfaces from a public-safe
fixture. Authored fields remain assumptions: no weapon authorization, lawful
use, meaningful control in practice, correct observation, acceptable effect,
escalation reduction, strategic stability, safety, support, release, transfer,
or external effect follows. Chapter support remains `argument` and
`support_state_effect` remains `none`.

The independent consumer checks 45 exact mutation dispositions, three arithmetic monotonicity controls, and two impossibility results.

""",
    "open-weight-release-and-post-release-control": """## Current refinement

`AsiStackProofs.OpenWeightReleaseReview` implements a reachable six-step finite
review over exact artifact identity, access alternatives, frontier freshness,
derivative stress coverage, benefit/risk distribution, independent review,
lineage, incidents, patch semantics, residual ownership, and explicit
post-release non-authority. One complete dossier reaches only a Project Theseus
harmless release-case campaign. All 36 admission-axis mutations reject
readiness and receive exact repair or refusal dispositions.

Two arithmetic results preserve frontier-expiry rejection as time advances and
show that a positive public-copy count remains incompatible with universal
recall under nondecreasing copies. Two impossibility results show that official
lineage cannot recover universal copy control and default evaluation cannot
recover downstream safeguard state. The independent consumer reconstructs the
mutation, monotonicity, and collision surfaces from a harmless fixture.
Authored fields remain assumptions: no release, recall, telemetry, copy
erasure, license enforcement, derivative safety, benefit, risk, support,
transfer, or external effect follows. Chapter support remains `argument` and
`support_state_effect` remains `none`.

The independent consumer checks 36 exact mutation dispositions, two arithmetic monotonicity controls, and two impossibility results.

""",
    "governed-objective-formation-value-learning-and-goal-integrity": """## Current refinement

`AsiStackProofs.ObjectiveLeaseGovernance` implements a reachable seven-stage
finite review over an objective charter, target/proxy typing, plural-value
residue, a consumer-specific and versioned lease, challenge controls, finite
descendant retirement, and explicit non-authority. One complete authored
dossier reaches only a Project Theseus objective-registry study. All 46
admission-axis mutations reject readiness and receive exact repair or refusal
dispositions.

The authority type refuses objective ratification by the optimizer, reward
model, or evaluator. Consumer transfer, expiry, ontology drift, and authority
drift invalidate lease use. An inductive theorem retires every member of any
finite descendant-binding list. Two impossibility results show that an
identical proxy observation can accompany opposite target movement and an
identical preference prediction can accompany opposite authorization. A
consumer bridge supplies the existing learned-objective integrity model with
only bounded outer-target, authority, expiry, rollback, descendant-custody,
and residual-owner fields while asserting neither objective identity nor
absence of deception.

The independent consumer reconstructs the 46 mutation routes, finite
retirement, lease-scope failures, both collision pairs, and the exact theorem
surface. Authored fields remain assumptions: no correct value, consent, moral
truth, political legitimacy, corrigibility, preference accuracy, behavioral
goal alignment, complete external retirement, safe optimization, support,
transfer, or external effect follows. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "adversarial-machine-learning-and-model-attack-surface": """## Current refinement

`AsiStackProofs.AdversarialModelSecurity` implements a reachable eight-step
finite review over exact artifact identity, threat and attack-lane identity,
adaptive challenge competence, observations and utility costs, recovery,
assurance scope, safe disclosure, and explicit non-authority. One complete
authored dossier reaches only a Project Theseus model-security campaign. All
58 admission-axis mutations reject readiness and receive exact repair or
refusal dispositions.

Typed assurance obligations prevent a regional certificate, runtime monitor,
or recovery procedure from discharging either of the other obligations. A
structural-induction theorem quarantines every member of any finite attack-
trace list. Expiry, checkpoint change, serving-configuration change, and
attacker-budget widening invalidate a bounded disposition. Two impossibility
results show that clean accuracy, failed-attack count, red-team coverage, and
certificate presence cannot recover the full bounded security state, and
passing local model, memory, and tool checks cannot recover composed attack-
path reachability. A consumer bridge supplies the existing adversarial-
evaluation lifecycle with only bounded observation, denominator, challenge,
cost, residual, and no-release fields.

The independent consumer reconstructs all 58 mutation routes, assurance
separation, finite quarantine, disposition invalidation, both collision pairs,
and the exact theorem surface. Authored fields remain assumptions: no
robustness, exploitability, attack reachability, defense or detector efficacy,
recovery efficacy, confidentiality, secure deployment, attack authority,
support, transfer, or external effect follows. Chapter support remains
`argument` and `support_state_effect` remains `none`.

""",
    "confidential-and-verifiable-ai-computation": """## Current refinement

`AsiStackProofs.ProtectedComputationReview` implements a reachable eight-step
finite review over exact transaction and artifact identity, separated
guarantees, evidence roles and statement scope, freshness, leakage, observable
fallback, cross-owner handoff, and explicit non-authority. One complete
authored dossier reaches only a Project Theseus protected-computation
campaign. All 48 admission-axis mutations reject readiness and receive exact
repair or refusal dispositions.

Typed evidence classes prevent remote attestation, an encoded-relation proof,
or a confidentiality mechanism from substituting for semantic correctness,
authorization, or end-to-end privacy. Structural induction accounts for every
member of an arbitrary finite leakage-channel list. Expiry, artifact change,
verifier-policy change, and evidence-epoch change invalidate a bounded
receipt, while a leakage overrun remains an overrun under more observation and
no larger allowance. Typed fallback theorems reject an unprotected path
without separate authorization or consumer-visible disclosure.

Two impossibility results show that identical evidence signals can accompany
opposite semantic-authorization states and identical component guarantees can
accompany opposite end-to-end privacy states. A consumer bridge supplies
bounded fields to Privacy Information Flow while leaving purpose and authority
false, so the privacy owner rejects rather than inherits them. Authored fields
remain assumptions: no cryptographic soundness, attestation validity, hardware
trust, side-channel resistance, leakage measurement, semantic correctness,
authorization, privacy, fallback efficacy, acceptable cost, deployment,
support, transfer, or external effect follows. Chapter support remains
`argument` and `support_state_effect` remains `none`.

The independent consumer checks 48 exact mutation dispositions, three evidence non-substitution results, finite leakage accounting, five adverse scope changes, two fallback rejections, two impossibility results, and one rejecting privacy bridge.

""",
    "content-authenticity-watermarking-and-synthetic-media-integrity": """## Current refinement

`AsiStackProofs.ContentAuthenticityReview` implements a reachable
eight-transition review over exact asset and rendition identity, separated
evidence semantics, finite transformation accounting, current trust policy and
signer state, conflict and remedy custody, accessible disclosure, and explicit
non-authority. One complete envelope reaches only Project Theseus authenticity
campaign eligibility. Forty-two mutations receive exact repair or refusal
routes; receipt and staleness theorems reject changed assets, policies,
transformations, signer epochs, and expired use; typed transformation rules
reject unsupported preservation and unbound composites; two collision pairs
prove that technical signals cannot recover semantic truth and absence cannot
recover human origin; and a communication bridge refuses to inherit recipient
comprehension.

`scripts/validate_content_authenticity_review.py` independently reconstructs
the model and 32-theorem surface. The model trusts authored fields and proves
no provenance correctness, watermark or detector robustness, truth, origin,
authorship, comprehension, compliance, remedy efficacy, deployment, transfer,
support transition, AGI, or ASI. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "autonomous-replication-proliferation-and-containment": """## Current refinement

`AsiStackProofs.ReplicationContainmentReview` implements a reachable
eight-transition review over exact parent and attempt identity,
denied-by-default synthetic authority, separate component, assisted,
end-to-end, and containment denominators, descendant lineage, independent
containment, closure, and explicit non-authority. One complete dossier reaches
only Project Theseus replication-containment campaign eligibility. All 52
admission-axis mutations reject readiness and receive exact repair or refusal
dispositions.

The principal-bound lease prevents a distinct child from inheriting parent
authority, while a typed infrastructure boundary excludes real providers from
synthetic-test authority. Structural induction quarantines every member of an
arbitrary finite descendant list. Expiry and descendant-ceiling failures are
monotone under adverse changes, and parent, artifact, environment, or protocol
change invalidates a bounded receipt.

Two impossibility results show that identical component signals can accompany
opposite end-to-end replication states and identical local shutdown signals
can accompany opposite global-containment states. A consumer bridge supplies
the governed-operations lifecycle with an intentionally incomplete descendant
inventory, so reconciliation requests state inventory. The independent
consumer reconstructs all 52 mutation routes, evidence and authority
separation, finite quarantine, receipt and monotonicity controls, both
collision pairs, and the exact 32-theorem surface.

Authored fields remain assumptions: no identity or provider correctness,
isolation, census completeness, independent termination, shutdown, recall,
real-world replication capability, containment efficacy, deployment, support,
transfer, or external effect follows. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "institutions-international-coordination-and-public-legitimacy": """## Current refinement

`AsiStackProofs.InstitutionalLegitimacyReview` implements a reachable
eight-transition review over identity, jurisdiction-scoped mandate, affected
publics, cross-border commitments, institutional performance, remedy, and
explicit non-authority. One complete dossier reaches only Project Theseus
institutional-tabletop eligibility. All 45 admission-axis mutations reject
readiness and receive exact repair or refusal dispositions.

Typed evidence prevents agreement, legal, consultation, and technical-
conformance records from substituting for implementation, legitimacy,
representative mandate, or public authority. A jurisdiction-bound mandate
cannot authorize a distinct jurisdiction. Structural induction includes every
member of an arbitrary finite affected-public list. Expiry and population
shortfall are monotone under adverse changes, while jurisdiction, instrument,
population, and protocol changes invalidate receipts.

Two impossibility results show that identical participation signals can
accompany opposite representative-standing states and identical commitment
signals can accompany opposite effective-enforcement states. A Governance
Rights bridge maps an incomplete affected-public census to protected-right
review. Authored fields remain assumptions: no lawful authority,
representativeness, independent review, implementation, enforcement, remedy
efficacy, legitimacy, geopolitical stability, deployment, support, transfer,
or external effect follows. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "societal-resilience-and-misuse-defense": """## Current refinement

`AsiStackProofs.SocietalResilienceReview` implements a reachable
eight-transition review over incident and population identity,
cross-organization coordination, resistance and absorption, recovery, remedy,
adaptation, and explicit non-authority. One complete dossier reaches only
Project Theseus synthetic resilience-exercise eligibility. All 45
admission-axis mutations reject readiness and receive exact repair or refusal
dispositions.

Typed evidence prevents provider takedowns, table-top completion, rapid
internal response, and local safeguard results from substituting for population
resilience, live recovery, lawful equitable remedy, or cross-organization
defense. A mandate for one organization cannot authorize another. Structural
induction closes every member of an arbitrary finite incident-path list.
Expiry, uncovered-population shortfall, and unresolved-path shortfall remain
rejecting under adverse monotone changes. Incident, population, jurisdiction,
and protocol changes invalidate receipts.

Two impossibility results show that identical provider signals can accompany
opposite population-recovery states and identical response-speed signals can
accompany opposite equitable-remedy states. An Institutional Legitimacy bridge
rejects a missing participant census. Authored fields remain assumptions: no
population resilience, lawful authority, cross-organization cooperation,
recovery, remedy efficacy, acceptable residual harm, deployment, support,
transfer, or external effect follows. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "durable-semantic-memory-and-knowledge-lattices": """## Current refinement

`AsiStackProofs.DurableSemanticMemoryReview` implements a reachable
seven-transition review over semantic identity, provenance and revision,
ontology migration, retrieval and actual-use custody, retention and replay, and
explicit non-authority. One complete dossier reaches only Project Theseus
memory replay and retrieval-campaign eligibility. All 38 admission-axis
mutations reject readiness and receive exact repair or refusal dispositions.

The model preserves object identity across representation changes and keeps
equal aliases from forcing object equality. Induction over arbitrary finite
parent lists preserves every provenance source and prevents derived purpose
authority from exceeding any parent. A lossy migration without consumer
invalidation is rejected. Every used retrieval object must have current
support, provenance, rights, contradiction state, and non-retraction custody.
Event-log replay composes over list concatenation.

Object, ontology, evidence-epoch, and purpose changes invalidate receipts. Two
non-identifiability results separate summaries from contradiction state and
storage deletion from learned influence. An open deletion duty routes to the
existing Context Transactions deletion block. Authored fields remain
assumptions: no semantic truth, useful retrieval, complete memory, behavioral
forgetting, semantic restart equivalence, deployment, support, transfer, or
external effect follows. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "human-ai-communication-persuasion-and-epistemic-security": """## Current refinement

`AsiStackProofs.CommunicationInfluenceReview` implements a reachable six-stage
finite review over claim and provenance custody, audience autonomy, bounded
delivery, correction and observation, and explicit non-authority. One complete
authored dossier reaches only a Project Theseus benign communication study. All
42 admission-axis mutations reject readiness and receive exact repair or
refusal dispositions.

Three arithmetic results preserve expiry, audience-overrun, and repetition-
overrun rejection under adverse monotone changes. Typed personalization over
only the allowed audience projection is invariant to denied attributes. Two
impossibility results show that factuality, consent, persuasion score, and
disclosure cannot recover the full bounded influence state, and provenance
cannot recover recipient comprehension. The independent consumer reconstructs
the mutation, monotonicity, noninterference, and collision surfaces from a
benign fixture. Authored fields remain assumptions: no truth, comprehension,
autonomy, persuasion efficacy, manipulation detection, correction efficacy,
benefit, harm, delivery authority, support, transfer, or external effect
follows. Chapter support remains `argument` and `support_state_effect` remains
`none`.

The independent consumer checks 42 exact mutation dispositions, three
arithmetic monotonicity controls, one typed noninterference result, and two
impossibility results.

""",
    "physical-compute-infrastructure-energy-and-environmental-constraints": """## Current refinement

`AsiStackProofs.PhysicalComputeInfrastructureReview` implements a reachable
six-transition review over exact workload, site, interval, hardware, topology,
workload-version, and meter-version identity; distinct requested, nameplate,
available, delivered, and useful compute; multi-resource capacity; attributed
energy and impacts; resilience and retirement; and explicit non-authority. One
complete dossier reaches only Project Theseus workload-capacity campaign
eligibility. All 44 admission-axis mutations reject readiness and receive exact
repair or refusal dispositions.

Finite-list induction proves workload-demand and impact-accounting composition,
and bounds each member's compute demand by the aggregate. Overrun and hidden
backup-energy counterexamples reject capacity and accounting claims. Demand
growth, capacity loss, and expiry preserve failure. Workload, site, interval,
hardware, and meter changes invalidate receipts. Two non-identifiability
results separate energy headlines from useful delivery and unit efficiency
from total impact. A Resource Economics bridge rejects its required safety gate
when physical capacity is absent.

Authored dossier fields remain assumptions. No theorem establishes delivered
performance, meter accuracy, sustainability, resilience, community
acceptability, rebound control, deployment, support, transfer, or external
effect. Chapter support remains `argument` and `support_state_effect` remains
`none`.

""",
    "learning-theory-generalization-and-scaling-science": """## Current refinement

`AsiStackProofs.LearningTheoryForecastReview` implements a reachable
six-transition review over exact claim, population, sample, support,
hypothesis, algorithm, optimization, architecture, metric, compute,
prospective-design, transfer, lifecycle, and non-authority obligations. One
complete dossier reaches only Project Theseus prospective forecast campaign
eligibility. All 45 admission-axis mutations reject readiness and receive exact
repair or refusal dispositions.

Structural induction preserves every attempt identity over arbitrary finite
lists, and append composition preserves the attempt ledger. Omitted attempts
and unscored preregistered alternatives reject completeness. Expiry,
unsupported extrapolation, and scoring shortfall remain rejecting under
adverse changes. Seven population and regime changes invalidate receipts. Two
non-identifiability results separate retrospective fit from prospective
coverage and threshold metrics from mechanism change. A Benchmark Ratchets
bridge rejects readiness promotion without a prospective holdout.

Authored dossier fields remain assumptions. No theorem establishes
generalization, transfer, emergence, scaling accuracy, calibration, safety,
deployment, support, release, or external effect. Chapter support remains
`argument` and `support_state_effect` remains `none`.

""",
    "scientific-discovery-and-experimental-governance": """## Current refinement

`AsiStackProofs.ScientificExperimentReview` implements a reachable
eight-transition review over hypothesis and protocol identity, preregistered
design, instrument and execution custody, analysis, replication, dual-use
governance, expiry, and explicit non-authority. One complete dossier reaches
only Project Theseus governed experiment campaign eligibility. All 54
admission-axis mutations reject readiness and receive exact repair or refusal
dispositions.

Structural induction preserves every attempt identity over arbitrary finite
lists and proves attempt-ledger append composition. Omitted attempts and
outcome-exposed confirmatory branches reject completeness. Expiry, denominator
gaps, and replication gaps remain rejecting under adverse changes. Seven scope
changes invalidate experiment receipts. Two non-identifiability results
separate significance from preregistration integrity and replication counts
from independence. Evidence States rejects empirical promotion without
independent replication, and Benchmark Ratchets rejects promotion without null
results.

Authored dossier fields remain assumptions. No theorem establishes hypothesis
truth, causal identification, instrument accuracy, reproducibility, discovery,
laboratory safety, deployment, support, release, transfer, or external effect.
Chapter support remains `argument` and `support_state_effect` remains `none`.

""",
    "relational-dimension-compilation-and-polyadic-cognition": """## Current refinement

`AsiStackProofs.RelationalDimensionCompiler` implements a reachable
eight-transition review over proposal and compiler identity, typed roles,
complete candidate denominators, seven named lower-order rescue families,
held-out qualification, compilation and fallback, contraction, expiry, and
explicit non-authority. One complete authored dossier reaches only Project
Theseus relational-compiler-study eligibility. All 54 admission-axis mutations
reject readiness and receive exact repair or refusal dispositions.

Structural induction preserves role and candidate identity over finite append,
and entity remapping preserves role IDs. Quantified completeness obligations
reject omitted required roles and hidden candidates. Descendant closure composes
over append, while one active descendant blocks contraction. Candidate-budget
overrun persists when generation grows. Seven scope changes invalidate
receipts. Two non-identifiability results separate qualification metrics from
role fidelity and named rescue records from actual rescue competence. Existing
Search Substrates, Routing, and Evidence States consumers reject a missing
baseline, route an unqualified compiler to fallback, and block empirical
promotion without a compiler experiment.

Authored dossier fields remain assumptions. No theorem establishes field truth,
higher-order irreducibility, representational usefulness, efficiency,
natural-task transfer, bounded primitive arity, safe online adaptation,
support, release, transfer, or external effect. Chapter support remains
`argument` and `support_state_effect` remains `none`.

""",
    "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty": """## Current refinement

`AsiStackProofs.HumanAICognitiveSovereignty` implements a reachable
eight-transition review over coupling identity, competent component and simpler
intervention comparators, purpose-specific authorization, neural and inferred
mental-data custody, practical pause and exit, longitudinal observation, and
explicit non-authority. One complete authored dossier reaches only Project
Theseus low-risk coupling-study eligibility. All 49 admission-axis mutations
reject readiness and receive exact repair or refusal dispositions.

The model defines complementarity against both component baselines and gives
concrete counterexamples to one-sided comparison. Purpose grants are exact;
unrelated use, revocation, and expiry block authorization. Finite-list proofs
preserve participant identity and require baseline, during-use, and post-exit
records for every expected participant. Seven scope changes invalidate
receipts. Two non-identifiability results separate nominal revocation signals
from practical exit and session metrics from post-exit skill retention.
Existing Privacy Information Flow, Human Factors Oversight, and Evidence States
consumers reject purpose drift, a missing intervention channel, and empirical
promotion without a longitudinal study.

Authored dossier fields remain assumptions. No theorem establishes field truth,
beneficial symbiosis, genuine consent, mental integrity, cognitive enhancement,
clinical efficacy, equity, neural safety, lawful authorization, support,
release, transfer, or external effect. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "ai-deployment-transition-distribution-and-human-agency": """## Current refinement

`AsiStackProofs.DeploymentTransitionGovernance` implements a reachable
eight-transition review over deployment and counterfactual identity, complete
affected-person denominators, disaggregated task-to-social accounting,
practical refusal and exit, transition capacity, delayed monitoring, remedy,
expiry, and explicit non-authority. One complete dossier reaches only Project
Theseus governed transition-study eligibility. All 54 admission-axis mutations
reject readiness and receive exact repair or refusal dispositions.

Finite-list proofs preserve cohort identity and append composition, require
every expected cohort in the denominator, and prevent an unremedied harmed
cohort from disappearing behind other gains. A concrete witness has positive
aggregate gain while worker harm remains unremedied. Expiry, population gaps,
and remedy gaps remain rejecting under adverse changes. Seven scope changes
invalidate receipts. Two non-identifiability results separate aggregate signals
from harmed-cohort status and approval counts from practical refusal. Existing
Human-AI Organizations, Readiness Gates, and Evidence States consumers reject
missing remedy, failed transition checks, and empirical promotion without a
transition study.

Authored dossier fields remain assumptions. No theorem establishes field truth,
causal deployment effect, job change, welfare, fairness, meaningful agency,
lawful remedy, service continuity, deployment readiness, support, release,
transfer, or external effect. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
    "embodied-agency-real-time-control-and-physical-safety": """## Current refinement

`AsiStackProofs.EmbodiedPhysicalSafety` implements a finite control-lease
admission model over current identity and lease state, derived observation
freshness, state and actuator envelopes, timing budget, fallback stopping
distance, independent stop, effect observation, residual custody, and an
explicit non-claim boundary. One complete authored lease reaches only
eligibility for a Project Theseus closed-loop trial. Thirteen axis mutations
fail readiness and reach exact repair routes, while three arithmetic
monotonicity controls preserve timing validity under reduced latency or
preserve rejection under worsened state and fallback bounds.

A separate eight-stage simulation-trial review lifecycle adds nineteen
theorems, bringing the module to 41 declarations. It proves arbitrary-run
nine-field identity custody, support/effect non-authority, exact receipt
accounting, stop-count monotonicity, accepted traces, batch composition,
absorbing closure, one seven-event closed witness, and safety-axis start
blocking. The independent consumer checks all eight trace splits and rejects
105 lifecycle mutations without treating the simulation-review record as a
physical execution.

`scripts/validate_embodied_physical_safety.py` independently re-encodes the
positive route, 13 exact mutation routes, three arithmetic monotonicity
controls, and 105 lifecycle mutations. The model trusts every authored plant, estimator, controller,
timing, effect, custody, and boundary field. It proves no plant truth, physical
or human safety, deadline satisfaction, safe-set validity, fallback
effectiveness, recovery, support transition, release, transfer, external
effect, deployment, AGI, or ASI. Chapter support remains `argument` and
`support_state_effect` remains `none`.

""",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def theorem_blocks(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    declarations = list(DECL_RE.finditer(text))
    rows: list[dict[str, Any]] = []
    for match in THEOREM_RE.finditer(text):
        end = next((decl.start() for decl in declarations if decl.start() > match.start()), len(text))
        block = text[match.start():end]
        signature = block.split(":= by", 1)[0]
        body = block.split(":= by", 1)[1] if ":= by" in block else ""
        depth_class, depth_evidence = classify_body(block)
        rows.append(
            {
                "name": match.group(1),
                "source_start_line": text.count("\n", 0, match.start()) + 1,
                "source_end_line": text.count("\n", 0, end) + 1,
                "signature": normalize(signature),
                "body": body,
                "depth_class": depth_class,
                "depth_evidence": depth_evidence,
                "baseline_block_sha256": digest(block),
            }
        )
    return rows


def current_theorems() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(LEAN_DIR.glob("*.lean")):
        module_path = str(path.relative_to(ROOT))
        for row in theorem_blocks(path):
            theorem_id = f"{module_path}::{row['name']}"
            rows.append({"theorem_id": theorem_id, "module_path": module_path, **row})
    return rows


def initial_baseline() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = load(MANIFEST)
    targets = [row for row in manifest["records"] if isinstance(row, dict)]
    claims = {row["atom_id"] for row in load(CLAIMS)["atoms"]}
    targets_by_module: dict[str, list[dict[str, Any]]] = defaultdict(list)
    chapter_by_module: dict[str, str] = {}
    for target in targets:
        targets_by_module[target["module_path"]].append(target)
        chapter_by_module[target["module_path"]] = target["chapter_id"]
        claim_id = f"{target['chapter_id']}.core"
        if claim_id not in claims:
            raise ValueError(f"Missing claim atom for proof target: {claim_id}")

    theorem_rows = current_theorems()
    theorem_names = {row["name"] for row in theorem_rows}
    theorem_ids_by_name: dict[str, list[str]] = defaultdict(list)
    for row in theorem_rows:
        theorem_ids_by_name[row["name"]].append(row["theorem_id"])

    baseline_theorems: list[dict[str, Any]] = []
    for row in theorem_rows:
        module_path = row["module_path"]
        if module_path not in chapter_by_module:
            raise ValueError(f"Theorem module has no proof-manifest chapter owner: {module_path}")
        body_identifiers = set(re.findall(r"[A-Za-z_][A-Za-z0-9_'.]*", row["body"]))
        references = sorted((body_identifiers & theorem_names) - {row["name"]})
        dependencies = sorted({item for name in references for item in theorem_ids_by_name[name]})
        baseline_theorems.append(
            {
                "theorem_id": row["theorem_id"],
                "chapter_id": chapter_by_module[module_path],
                "claim_atom_id": f"{chapter_by_module[module_path]}.core",
                "module_path": module_path,
                "name": row["name"],
                "source_start_line": row["source_start_line"],
                "source_end_line": row["source_end_line"],
                "baseline_signature": row["signature"],
                "baseline_block_sha256": row["baseline_block_sha256"],
                "depth_class": row["depth_class"],
                "depth_evidence": row["depth_evidence"],
                "safety_critical_module": module_path in SAFETY_CRITICAL_MODULES,
                "candidate_target_tags": sorted(target["tag"] for target in targets_by_module[module_path]),
                "theorem_dependencies": dependencies,
                "review_state": "machine_candidate",
                "disposition": None,
                "semantic_role": None,
                "assumptions": [],
                "excluded_effects": [],
                "countermodel_refs": [],
                "mutation_refs": [],
                "consumer_refs": [],
                "runtime_consumer_refs": [],
                "replacement_refs": [],
                "review_rationale": None,
            }
        )

    reverse_dependencies: dict[str, list[str]] = defaultdict(list)
    for row in baseline_theorems:
        for dependency in row["theorem_dependencies"]:
            reverse_dependencies[dependency].append(row["theorem_id"])
    for row in baseline_theorems:
        row["theorem_consumers"] = sorted(reverse_dependencies[row["theorem_id"]])

    baseline_targets: list[dict[str, Any]] = []
    theorem_ids_by_module: dict[str, list[str]] = defaultdict(list)
    for row in baseline_theorems:
        theorem_ids_by_module[row["module_path"]].append(row["theorem_id"])
    for target in targets:
        baseline_targets.append(
            {
                "target_id": target["tag"],
                "chapter_id": target["chapter_id"],
                "claim_atom_id": f"{target['chapter_id']}.core",
                "module": target["module"],
                "module_path": target["module_path"],
                "formal_target": target["formal_target"],
                "baseline_status": target["status"],
                "baseline_outline_line": target["outline_line"],
                "candidate_theorem_ids": sorted(theorem_ids_by_module[target["module_path"]]),
                "review_state": "machine_candidate",
                "disposition": None,
                "semantic_role": None,
                "assumptions": [],
                "excluded_effects": [],
                "dependencies": [],
                "countermodel_refs": [],
                "mutation_refs": [],
                "consumer_refs": [],
                "runtime_consumer_refs": [],
                "replacement_refs": [],
                "review_rationale": None,
            }
        )
    return baseline_theorems, baseline_targets


def apply_reviews(rows: list[dict[str, Any]], reviews: dict[str, Any], key: str, id_key: str) -> None:
    overlay = reviews.get(key, {})
    known = {row[id_key] for row in rows}
    unknown = sorted(set(overlay) - known)
    if unknown:
        raise ValueError(f"Unknown {key}: {unknown[:5]}")
    for row in rows:
        patch = overlay.get(row[id_key])
        if patch:
            row.update(patch)


def build() -> tuple[dict[str, Any], str, dict[str, str]]:
    existing = load(REGISTRY) if REGISTRY.exists() else None
    if existing:
        theorem_rows = existing["baseline_theorems"]
        target_rows = existing["baseline_targets"]
    else:
        theorem_rows, target_rows = initial_baseline()
    theorem_rows = json.loads(json.dumps(theorem_rows))
    target_rows = json.loads(json.dumps(target_rows))
    for row in target_rows:
        row.setdefault("semantic_role", None)
        row.setdefault("excluded_effects", [])
        row.setdefault("consumer_refs", [])
    for row in theorem_rows:
        row.setdefault("consumer_refs", [])
    reviews = load(REVIEWS)
    apply_reviews(theorem_rows, reviews, "theorem_reviews", "theorem_id")
    apply_reviews(target_rows, reviews, "target_reviews", "target_id")

    current = {row["theorem_id"]: row for row in current_theorems()}
    for row in theorem_rows:
        now = current.get(row["theorem_id"])
        row["current_present"] = now is not None
        row["current_block_sha256"] = now["baseline_block_sha256"] if now else None
        row["current_matches_baseline"] = bool(now and now["baseline_block_sha256"] == row["baseline_block_sha256"])

    current_targets = {row["tag"]: row for row in load(MANIFEST)["records"]}
    for row in target_rows:
        now = current_targets.get(row["target_id"])
        row["current_present"] = now is not None
        row["current_status"] = now.get("status") if now else None
        row["current_matches_baseline"] = bool(
            now
            and now.get("chapter_id") == row["chapter_id"]
            and now.get("module_path") == row["module_path"]
            and now.get("formal_target") == row["formal_target"]
        )

    theorem_counts = Counter(row["review_state"] for row in theorem_rows)
    target_counts = Counter(row["review_state"] for row in target_rows)
    depth_counts = Counter(row["depth_class"] for row in theorem_rows)
    module_paths = sorted({row["module_path"] for row in theorem_rows} | {row["module_path"] for row in target_rows})
    fully_reviewed_modules = [
        module_path
        for module_path in module_paths
        if all(
            row["review_state"] != "machine_candidate"
            for row in theorem_rows + target_rows
            if row["module_path"] == module_path
        )
    ]
    registry = {
        "schema_version": "asi_stack.proof_rationalization_registry.v0",
        "roadmap_id": ROADMAP_ID,
        "baseline_frozen_at": "2026-07-15",
        "generated_from": [
            "proofs/proof_manifest.json",
            "lean/AsiStackProofs/*.lean",
            "evidence_quality/claim_atom_registry.json",
            "proofs/proof_rationalization_reviews.json",
        ],
        "summary": {
            "baseline_theorem_declaration_count": len(theorem_rows),
            "baseline_proof_target_count": len(target_rows),
            "chapter_count": len({row["chapter_id"] for row in target_rows}),
            "module_count": len(module_paths),
            "fully_reviewed_module_count": len(fully_reviewed_modules),
            "safety_critical_module_count": len(SAFETY_CRITICAL_MODULES),
            "safety_critical_fully_reviewed_module_count": len(set(fully_reviewed_modules) & SAFETY_CRITICAL_MODULES),
            "theorem_review_state_counts": dict(sorted(theorem_counts.items())),
            "target_review_state_counts": dict(sorted(target_counts.items())),
            "depth_class_counts": dict(sorted(depth_counts.items())),
            "missing_current_theorem_count": sum(not row["current_present"] for row in theorem_rows),
            "changed_current_theorem_count": sum(row["current_present"] and not row["current_matches_baseline"] for row in theorem_rows),
            "missing_current_target_count": sum(not row["current_present"] for row in target_rows),
            "changed_current_target_count": sum(row["current_present"] and not row["current_matches_baseline"] for row in target_rows),
            "support_state_effect": "none",
        },
        "baseline_theorems": theorem_rows,
        "baseline_targets": target_rows,
        "non_claims": [
            "Inventory, parsing, depth classification, theorem count, target count, or Lean build success does not establish semantic adequacy.",
            "Candidate target mappings are module-level discovery aids until semantic review names the exact target, assumptions, consumers, countermodels, and mutations.",
            "A retained theorem cannot promote a chapter claim without its separately accepted evidence transition.",
        ],
    }

    chapter_theorems: dict[str, list[dict[str, Any]]] = defaultdict(list)
    chapter_targets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in theorem_rows:
        chapter_theorems[row["chapter_id"]].append(row)
    for row in target_rows:
        chapter_targets[row["chapter_id"]].append(row)
    dossiers: dict[str, str] = {}
    chapter_lines: list[str] = []
    dossier_chapter_ids = sorted(set(chapter_targets) | set(CURRENT_REFINEMENTS))
    for chapter_id in dossier_chapter_ids:
        theorems = chapter_theorems[chapter_id]
        targets = chapter_targets[chapter_id]
        pending_theorems = sum(row["review_state"] == "machine_candidate" for row in theorems)
        pending_targets = sum(row["review_state"] == "machine_candidate" for row in targets)
        if chapter_id in chapter_targets:
            chapter_lines.append(f"| `{chapter_id}` | {len(targets)} | {len(theorems)} | {pending_targets} | {pending_theorems} |")
        target_lines = "\n".join(
            f"| `{row['target_id']}` | {row['review_state']} | {row.get('disposition') or 'pending'} |"
            for row in targets
        ) or "| _No activation-baseline target; current refinement postdates the freeze._ | reviewed | retain |"
        theorem_lines = "\n".join(
            f"| `{row['name']}` | {row['depth_class']} | {row['review_state']} | {row.get('disposition') or 'pending'} |"
            for row in theorems
        ) or "| _No activation-baseline declaration; current refinement postdates the freeze._ | n/a | reviewed | retain |"
        current_refinement = CURRENT_REFINEMENTS.get(chapter_id, "")
        dossiers[chapter_id] = f"""# Proof-model dossier: {chapter_id}

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
{target_lines}

{current_refinement}## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
{theorem_lines}

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
"""

    report = f"""# Proof Rationalization Registry

Generated by `python3 scripts/build_proof_rationalization_registry.py` from the frozen P2 activation baseline plus the review overlay.

This inventory freezes the 1,151 theorem declarations and 298 proof targets that P2 must disposition. It preserves retired and replaced baseline items instead of deleting history. Syntax depth, candidate module mappings, counts, and green Lean builds are discovery evidence only; they do not establish semantic adequacy or promote a claim.

## Summary

| Metric | Value |
|---|---:|
| Baseline theorem declarations | {len(theorem_rows)} |
| Baseline proof targets | {len(target_rows)} |
| Chapters | {len(chapter_targets)} |
| Lean modules | {len(module_paths)} |
| Fully reviewed modules | {len(fully_reviewed_modules)} |
| Safety-critical modules fully reviewed | {len(set(fully_reviewed_modules) & SAFETY_CRITICAL_MODULES)}/{len(SAFETY_CRITICAL_MODULES)} |
| Theorem machine candidates | {theorem_counts.get('machine_candidate', 0)} |
| Target machine candidates | {target_counts.get('machine_candidate', 0)} |
| Direct/projection declarations | {depth_counts.get('direct_or_projection', 0)} |
| Derived/decomposed declarations | {depth_counts.get('derived_or_decomposed', 0)} |
| Unknown/mixed declarations | {depth_counts.get('unknown_or_mixed', 0)} |
| Support-state effect | none |

## Chapter work queue

| Chapter | Targets | Theorems | Pending targets | Pending theorems |
|---|---:|---:|---:|---:|
{chr(10).join(chapter_lines)}

## Closure rule

P2 closed on 2026-07-16 only after every baseline target and theorem received a claim-centered semantic disposition; every retained item received exact assumptions, exclusions, dependencies, countermodels or negative cases, mutation coverage, and a live consumer; every retired, merged, or replaced item preserved lineage; and all 298 current targets received an explicit adequacy route in `proofs/p2_closure_audit.json`. The separate chapter dossiers remain under `evidence_quality/proof_model_dossiers/`. Downstream executable, empirical, reproduction, and transfer routes remain mandatory; closure does not promote support.
"""
    return registry, report, dossiers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry, report, dossiers = build()
    if args.check:
        errors: list[str] = []
        if not REGISTRY.exists() or load(REGISTRY) != registry:
            errors.append("proof rationalization registry is stale")
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != report:
            errors.append("proof rationalization report is stale")
        for chapter_id, body in dossiers.items():
            path = DOSSIERS / f"{chapter_id}.md"
            if not path.exists() or path.read_text(encoding="utf-8") != body:
                errors.append(f"{chapter_id}: proof-model dossier is stale")
                break
        if errors:
            raise SystemExit("Proof rationalization build check failed:\n - " + "\n - ".join(errors))
        print(f"Proof rationalization build check passed: {len(registry['baseline_theorems'])} theorems, {len(registry['baseline_targets'])} targets.")
        return
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    DOSSIERS.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report, encoding="utf-8")
    for chapter_id, body in dossiers.items():
        (DOSSIERS / f"{chapter_id}.md").write_text(body, encoding="utf-8")
    print(f"Wrote frozen proof rationalization surfaces: {len(registry['baseline_theorems'])} theorems, {len(registry['baseline_targets'])} targets, {len(dossiers)} dossiers.")


if __name__ == "__main__":
    main()
