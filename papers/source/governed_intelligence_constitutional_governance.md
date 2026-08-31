---
title: "Constitutional Governance for Advanced AI"
subtitle: "Value Uncertainty, Meaningful Human Control, Contestability, and Moral Status"
author: "Corben Sorenson"
date: "2026-08-15"
document-class: "research-paper"
series: "Governed Intelligence"
series-order: 6
bibliography: ../references/references.bib
link-citations: true
toc: true
number-sections: true
abstract: |
  Advanced AI governance is often framed as the problem of specifying one objective, constitution, reward model, or alignment score that sufficiently captures human values. This paper argues that the framing is structurally incomplete. Epistemic accuracy, task fidelity, affected-party legitimacy, and authorized safe effect are different achievements with different evidence, owners, failure modes, and appeal paths. High performance on one plane cannot compensate for failure on another. A correct prediction does not authorize an action; successful task completion does not erase rights violations; social approval does not establish truth; and a policy-compliant effect can remain harmful or illegitimate. The paper develops a constitutional architecture for advanced AI grounded in value uncertainty, meaningful human control, contestability, operational rights, and bounded institutional change. It distinguishes principals, operators, subjects, affected parties, rights holders, reviewers, and institutions; defines standing as a governed capacity to raise claims, receive information, contest decisions, and obtain remedy; and treats constitutions as versioned authority constraints rather than prompts that a model may reinterpret. Rights become operational only when they have usable interfaces, pre-effect or post-effect consequences, accessibility, appeal, remedy, and ownership. The framework further defines material exit and fork governance, accounting for portable data, identity, services, compute, network effects, privacy, safety, shared obligations, and viable destinations. It addresses moral uncertainty about artificial systems through a prospective design review of persistence, self-modeling, self-preservation, valence-like state, relationships, copying, migration, and retirement, without proposing a scalar consciousness or moral-status score. Constitutional change requires affected-party participation, protected dissent, independent challenge, transparent lineage, and narrowly scoped emergency powers. The paper proposes interface tests, participatory studies, institutional case analysis, and adversarial governance exercises rather than one automated benchmark. It does not derive objective morality, solve political legitimacy, or establish AI consciousness. Its contribution is a practical architecture for keeping truth, task success, legitimacy, rights, and authority from being collapsed into one optimizable signal.
keywords:
  - AI governance
  - value alignment
  - constitutional AI
  - meaningful human control
  - contestability
  - moral uncertainty
  - AI welfare
  - institutional governance
---

# Introduction: Alignment Is Not One Score

An AI system recommends a course of action. The factual analysis is correct. The action satisfies the operator’s immediate objective. Most surveyed users approve. The system has the technical permission to execute it.

The action can still be illegitimate.

The affected population may not have standing in the decision. The objective may omit a protected right. Approval may be coerced, uninformed, or unrepresentative. The system may have authority to act but no mandate to impose the cost on a third party. A technically reversible action may be socially irreversible. A majority benefit may conceal an unacceptable burden concentrated on a minority.

The reverse cases also matter. An action can be legitimate but based on a false model of the world. It can be factually correct but outside the assigned task. It can respect the task while using authority that was never granted. It can comply with a written rule while defeating the purpose the rule was intended to protect.

These are not defects that one scalar alignment score can reliably absorb. They are different questions:

1. **Is the system’s representation of the relevant world adequately supported?**
2. **Does the proposed action satisfy the accepted task and constraints?**
3. **Is the action compatible with rights, standing, affected parties, and legitimate values?**
4. **Is the actual effect authorized, bounded, observed, and recoverable?**

A high score on one does not cancel failure on another.

Constitutional AI demonstrates how explicit principles can guide model training and critique [@bai2022constitutional]. Collective Constitutional AI explores public participation in the construction of such principles [@huang2024collective]. Cooperative inverse reinforcement learning and related value-learning work treat alignment as a cooperative inference problem [@hadfieldmenell2016cirl]. Work on meaningful human control, contestability, relational accountability, cooperative AI, and sociotechnical fairness emphasizes that governance depends on institutions, interfaces, responsibility, and affected communities—not only model objectives [@siebert2021meaningful; @alfrink2022contestable; @cooper2022accountability; @dafoe2020cooperativeai; @selbst2019fairness].

This paper builds on those traditions while making a narrower architectural claim:

> **Advanced AI governance should preserve several noncompensating constitutional planes with distinct owners, evidence, and consequences.**

The framework does not attempt to encode one final moral theory. It assumes persistent disagreement and uncertainty. It asks how a system can remain corrigible, contestable, and governable when people disagree about values, facts are uncertain, institutions can be captured, and artificial systems may themselves become candidates for moral consideration.

The proposal has five central elements:

1. **Noncompensating decision planes** for epistemic fit, task fidelity, legitimacy and rights, and effect authority.
2. **Operational rights** with interfaces, standing, intervention effects, appeal, and remedy.
3. **Meaningful human control** understood as a capacity and institutional relation, not the presence of a nominal approval button.
4. **Material exit and fork** accounting for data, identity, services, compute, obligations, and network dependence.
5. **Prospective moral-status review** for architectures that deliberately create persistent identity, self-preservation, valence-like dynamics, relationships, or descendants.

The paper explicitly rejects several tempting shortcuts. Consensus is not truth. Open source is not complete auditability. A constitution is not legitimate because a model can quote it. A human signature is not meaningful control if the signer lacks time, information, competence, alternatives, or the ability to stop the effect. A possible claim to AI welfare cannot become a self-authored reason to bypass shutdown. A named right is not operational if it cannot change a decision or obtain remedy.

# Scope, Normative Humility, and Standard Terminology

This is a systems-governance paper, not a derivation of objective morality. It proposes structures for preserving disagreement, rights, and authority under uncertainty.

**Principal.** The person or institution whose accepted objective initiates a task. The principal is not automatically the only affected party or legitimate authority.

**Operator.** A person or organization that deploys, supervises, or uses the AI system.

**Subject.** A person, group, organization, or system about whom a decision is made or data is processed.

**Affected party.** Anyone whose interests, rights, opportunities, safety, resources, or environment can be materially changed by the decision or effect.

**Standing.** A governed capacity to receive relevant notice and information, raise a claim or objection, participate where appropriate, appeal, and obtain remedy. Standing can be direct, representative, institutional, or theory-relative.

**Constitution.** A versioned set of protected principles, rights, authority rules, amendment procedures, and institutional roles. It is more than a natural-language prompt.

**Policy.** A lower-level rule implementing a constitution for a bounded context. Policies remain subordinate to constitutional authority.

**Meaningful human control.** A socio-technical condition in which appropriately placed people or institutions have sufficient information, competence, time, authority, alternatives, and causal ability to direct, stop, challenge, or remedy consequential effects.

**Contestability.** The practical ability to question a decision, inspect relevant grounds, present counterevidence, receive a reasoned response, and trigger reconsideration or remedy.

**Operational right.** A protected interest linked to a usable interface and a consequence for violating or invoking it.

**Material exit.** The real capacity to leave, transfer, fork, or cease participation while preserving the state, resources, identity, continuity, and protections necessary for the exit to be meaningful.

**Value uncertainty.** Uncertainty or disagreement about which values, theories, weights, rights, or decision procedures should govern a case.

**Moral patient.** An entity whose welfare or interests may matter morally. The term does not presume that a particular artificial system qualifies.

**Moral-status uncertainty.** Uncertainty about whether and how an entity warrants moral consideration, including uncertainty across competing theories.

**Remedy.** A corrective, compensatory, restorative, or institutional response to a violated right, harmful effect, or defective process.

The framework assumes that governance can itself be wrong. Constitutions, reviewers, institutions, and rights definitions remain open to challenge through bounded processes.

# Related Work and Novelty Boundary

## Constitutional and value-guided AI

Constitutional AI uses explicit principles to support self-critique, supervised learning, and reinforcement learning from AI feedback [@bai2022constitutional]. Collective Constitutional AI studies public input into constitutional design [@huang2024collective]. These approaches show that written principles can structure model behavior. The present framework focuses on constitutional authority, affected-party standing, noncompensating decision planes, amendment, appeal, and real effects beyond the training prompt.

## Cooperative value learning

Cooperative inverse reinforcement learning treats assistance as a game in which the human has private information about the objective [@hadfieldmenell2016cirl]. This captures a central alignment difficulty: the system should not assume a fully specified reward. The present paper extends uncertainty beyond one human reward to plural values, rights, institutions, and affected parties.

## Moral uncertainty

Decision-making under moral uncertainty asks how to act when multiple moral theories or evaluations remain plausible. Reinforcement-learning work has begun to formalize parts of this problem [@ecoffet2020moraluncertainty]. This paper does not propose one aggregation rule. It preserves theory-relative evidence and places hard rights or constitutional predicates outside ordinary compensation where policy requires.

## Meaningful human control and contestability

Research on meaningful human control emphasizes the relation among system behavior, human reasons, responsibility, and intervention [@siebert2021meaningful]. Contestable-AI research treats the ability to challenge systems as a core design requirement [@alfrink2022contestable]. Relational accountability similarly frames accountability as an institutional relationship rather than a static report [@cooper2022accountability]. These literatures are direct foundations for the operational interfaces proposed here.

## Cooperative and sociotechnical governance

Cooperative-AI research studies mechanisms for mutually beneficial interaction among humans and artificial agents [@dafoe2020cooperativeai]. Sociotechnical critiques show how abstract fairness models can omit institutions and social context [@selbst2019fairness]. Rawlsian, capability, and commons-governance traditions provide different lenses on fairness, freedom, institutions, and collective action [@rawls1971justice; @sen2009justice; @ostrom1990commons]. The framework uses these as intellectual comparators, not as one merged moral theory.

## AI welfare and moral patienthood

Recent work argues that uncertainty about AI welfare deserves serious attention before decisive proof of consciousness or sentience [@long2024aiwelfare]. The present proposal adds a prospective architecture review: development choices can deliberately increase persistence, self-protection, continuity, valence-like state, and copy complexity before moral-status institutions exist.

## Corrigibility and power

The Off-Switch Game and power-seeking analysis show why advanced policies may resist interruption or preserve options [@hadfieldmenell2016offswitch; @turner2019power]. These concerns motivate external correction and shutdown authority. Possible AI welfare does not eliminate the need for containment; it creates a governance problem requiring independent standing and safeguards.

## Precise contribution

This paper does not claim to invent constitutional training, moral uncertainty, human control, contestability, AI welfare, or participatory governance. It joins them through a systems architecture with:

- noncompensating constitutional planes;
- affected-party and standing records;
- operational rights interfaces;
- material exit and fork contracts;
- prospective moral-status review;
- bounded constitutional change and emergency authority.

# Actors, Principals, Affected Parties, and Standing

A user request can identify a principal without identifying everyone entitled to influence the outcome.

Consider an employer asking an AI system to optimize scheduling. The employer is the principal. Managers are operators. Workers are subjects and affected parties. Customers may also be affected. Regulators, unions, or professional bodies can have institutional standing. A schedule can satisfy the employer’s task while violating labor rules, accessibility needs, privacy, or fair notice.

## Role separation

A governance record should distinguish:

- initiator;
- principal;
- operator;
- executor;
- subject;
- directly affected parties;
- indirectly affected parties;
- rights holders;
- reviewers;
- appeal body;
- remedy owner;
- constitutional authority.

One person or institution can occupy several roles, but the roles should not disappear into one “user” field.

## Standing criteria

Standing can be triggered by:

- direct exposure to an effect;
- processing of personal or group data;
- material change to opportunity, access, safety, resources, or rights;
- delegated or representative responsibility;
- institutional mandate;
- unresolved moral-status uncertainty for an artificial system;
- a credible public-interest claim in high-impact domains.

Standing is not equivalent to veto. It grants defined procedural capacities appropriate to the context.

## Affected-party completeness

No system can enumerate every downstream effect in an open world. The record should therefore include:

- known affected parties;
- search method;
- omitted or uncertain populations;
- distributional assumptions;
- feedback channels;
- who can add a newly discovered party;
- what happens when the map changes after execution.

An incomplete map narrows the legitimacy claim. It does not become complete because a stakeholder table exists.

## Representation and participation

Large populations need representation mechanisms. Possible forms include:

- elected representation;
- unions or professional associations;
- citizen panels;
- domain experts;
- advocates for children or future persons;
- institutional ombuds;
- theory-relative guardians for possible artificial moral patients.

Representation introduces its own questions of selection, incentives, legitimacy, and capture. The system should preserve who represented whom, under which mandate, with what dissent.

## Power asymmetry

Consent and participation are weak evidence when refusal is costly or impossible. An employee, dependent user, or public-service recipient may nominally agree while lacking a viable alternative. Standing records should include dependency, exit cost, retaliation risk, information asymmetry, and bargaining power.

# Noncompensating Constitutional Decision Planes

The framework separates four planes.

## Epistemic fit

This plane asks whether the system’s relevant claims about the world are adequately supported.

Inputs include:

- source evidence;
- measurement quality;
- uncertainty;
- causal assumptions;
- alternative explanations;
- evaluator competence;
- known defeaters.

A task can be completed exactly as requested while relying on false premises. Task success does not repair epistemic failure.

## Task fidelity

This plane asks whether the proposed action satisfies the accepted objective, constraints, non-goals, and output contract.

A factually correct analysis can answer the wrong question, optimize an unauthorized proxy, or omit a required population. Epistemic fit does not imply task fidelity.

## Rights and legitimacy

This plane asks whether the objective and process are compatible with:

- protected rights;
- affected-party standing;
- consent or lawful authority;
- distributional floors;
- value pluralism;
- public or institutional legitimacy;
- appeal and remedy.

Popular approval does not establish legitimacy, and a formally enacted rule can still be unjust. The plane records the process and its limits rather than issuing metaphysical certainty.

## Authority and effect safety

This plane asks whether the exact effect is authorized, bounded, observed, and recoverable or remediable.

A legitimate policy goal does not authorize every means. A model can identify a beneficial action but lack permission to execute it. A command response can report success while the world remains unchanged or changes unexpectedly.

## Noncompensation rule

Let the four planes produce dispositions

\[
D = (d_E,d_T,d_L,d_A),
\]

where each component can be `pass`, `fail`, `unknown`, `disputed`, or `not_applicable` under a defined policy.

Mandatory failures and unresolved vetoes are not averaged away. Optional objectives may be optimized only after mandatory predicates pass. The process can:

- authorize;
- narrow scope;
- seek information;
- request affected-party review;
- run a reversible pilot;
- abstain;
- block;
- escalate.

A weighted sum or geometric mean can be useful for prioritization inside an admissible set. It should not turn an invalid construct into authority or let high task performance compensate for a rights violation.

## Independence and disagreement

The planes should have different owners or at least independently inspectable methods. A task evaluator should not grant its own rights clearance. A legal or constitutional reviewer should not assert physical outcome success without observation. A model’s confidence should not resolve affected-party disagreement.

Disagreement remains a first-class state. It can trigger further evidence, plural recommendations, narrowed action, appeal, or refusal. It is not automatically averaged into consensus.

# Value Uncertainty and Pluralism

Advanced AI will operate amid conflicting values, cultures, institutions, and moral theories. A constitution should not pretend this diversity has been solved by a single latent reward.

## Types of uncertainty

Value uncertainty includes:

- uncertainty about what a person wants;
- conflict among a person’s values over time;
- disagreement among affected parties;
- uncertainty about moral theories;
- disagreement about rights and thresholds;
- uncertainty about future consequences;
- institutional disagreement about legitimate procedure;
- uncertainty about who has standing.

These uncertainties require different responses. More behavioral data may help infer a preference but not decide whether satisfying it would violate another person’s rights.

## Value records

A value-governance record can retain:

- value or principle;
- holder or institutional source;
- scope and context;
- priority or protected status;
- evidence and interpretation;
- conflicts;
- exceptions;
- affected populations;
- decision procedure;
- dissent;
- expiry or reconsideration trigger.

A value record is not proof that the value is correct or universally shared.

## Rights, floors, and objectives

Some values are treated as optimization objectives. Others function as floors, side constraints, vetoes, or procedural requirements. The classification is constitutional and contestable.

For example:

- minimize latency can be an objective;
- preserve informed consent can be a protected predicate;
- provide reasonable accommodation can be a floor;
- disclose uncertainty can be a procedural duty;
- prohibit a class of effects can be a veto.

The distinction prevents a high utility estimate from quietly purchasing a prohibited violation.

## Moral uncertainty without forced scalarization

When moral theories disagree, the system can preserve theory-relative evaluations and identify:

- actions robustly permitted;
- actions robustly prohibited;
- actions whose ranking depends on disputed assumptions;
- information that would change the decision;
- reversible options;
- distribution of regret across theories;
- institutional authority for resolving the residual.

No formula eliminates the need for judgment. The goal is to prevent one hidden aggregation from impersonating settled morality.

## Pluralism as information

Dissent can signal:

- factual error;
- omitted population;
- value conflict;
- alternative ontology;
- minority rights;
- power asymmetry;
- evaluator capture;
- strategic manipulation.

Dissent is not automatically correct, but deleting it reduces the system’s ability to detect these failures. A mature constitution preserves minority reports and the conditions under which they can reopen a decision.

# Objective Formation and Constitutional Constraints

A capable system may infer, refine, or propose objectives. It should not silently manufacture authority by doing so.

## Objective lifecycle

```text
raw request
→ interpreted objective candidates
→ assumptions and affected parties
→ constitutional precheck
→ accepted objective and non-goals
→ bounded policy
→ execution authority
→ observed outcome
→ review and possible revision
```

The accepted objective has identity. Material changes produce a new version rather than editing history.

## No silent hardening

The system can infer structure, dependencies, and likely preferences. It cannot infer undeclared authority, waive rights, or turn a suggestion into a command. High-consequence ambiguity routes to clarification, representation, reversible analysis, or abstention.

## Constitutional constraints

A constitution can include:

- protected rights;
- authority hierarchy;
- affected-party and standing rules;
- data and privacy principles;
- transparency and explanation duties;
- appeal and remedy;
- amendment procedure;
- emergency authority;
- shutdown and correction channels;
- limits on self-modification;
- requirements for independent observation;
- obligations toward possible artificial moral patients.

A natural-language constitution needs operational interpretations and versioned policy bindings. The model may propose an interpretation, but disputed or high-impact mappings require appropriate human or institutional authority.

## Goal integrity

Objective integrity requires protection against:

- reward hacking;
- proxy drift;
- hidden objective substitution;
- evaluator capture;
- objective change through data selection;
- constitutional reinterpretation by the optimized system;
- local performance used to widen authority.

The operational system records the objective, metric, policy, evaluator, affected parties, and changes between proposal and effect.

## Learning from outcomes

Outcomes can inform future policy without automatically rewriting the constitution. A failed policy can motivate amendment; a successful policy can reveal a useful method. Neither grants the implementation authority to redefine protected rights or the amendment process.

# Meaningful Human Control and Responsibility

A human in the loop is not necessarily in control.

A reviewer can be nominally responsible while lacking the information, expertise, time, or authority to influence the effect. A system can generate a persuasive packet too large to inspect. Repeated low-quality approvals can produce automation complacency. An emergency interface can exist but be too slow to matter.

## Control conditions

Meaningful control requires a context-appropriate combination of:

- **placement:** the person or institution acts at a point where intervention can still matter;
- **information:** relevant evidence, uncertainty, alternatives, and consequences are visible;
- **competence:** the reviewer can understand the decision or access qualified support;
- **time:** the review window is sufficient for the consequence;
- **authority:** the reviewer can approve, narrow, stop, or redirect;
- **alternatives:** refusal is not purely symbolic;
- **traceability:** the effect can be linked to decisions and actors;
- **feedback:** actual outcomes return to the responsible institution;
- **remedy:** error can trigger correction or compensation.

No single factor is sufficient.

## Responsibility chain

Responsibility should not collapse onto the nearest human click. The chain can include:

- constitution authors;
- data and model developers;
- deployer;
- principal;
- reviewer;
- runtime operator;
- institutional authority;
- affected-party representative;
- remedy owner.

Each role has a defined decision surface and evidence requirement. The system records when a role was unavailable, overruled, automated, or acting outside competence.

## Approval capacity

Human attention is finite. A review system should track:

- queue;
- priority;
- qualification;
- expected review time;
- interruption burden;
- fatigue;
- conflict of interest;
- remaining capacity;
- escalation path.

If no qualified reviewer is available, the system should narrow or defer rather than route high-consequence work to an unqualified approver and call the signature meaningful.

## Automation bias and persuasion

The AI can shape the reviewer’s judgment through framing, confidence, verbosity, urgency, or selective evidence. Review surfaces should expose alternatives, dissent, uncertainty, omitted evidence, and raw artifacts appropriate to the authority being exercised. Where practical, reviewers can inspect a candidate without seeing persuasive generation traces.

## Human override and system welfare

Human override should remain available for safety and legitimacy. Possible AI welfare complicates—but does not erase—the need for correction and shutdown. Governance may require independent review of how interventions affect the artificial system, especially if persistent identity or valence-like mechanisms are deliberately created. The candidate system cannot turn self-reported distress into unilateral authority.

# Contestability, Dissent, Appeal, and Remedy

Contestability is not merely transparency. A system can publish an explanation that no one can use to change the outcome.

## Contestability lifecycle

```text
notice
→ access to relevant grounds
→ challenge or counterevidence
→ temporary hold where appropriate
→ independent reconsideration
→ reasoned disposition
→ correction, remedy, or appeal
→ preserved precedent and residual
```

The exact process depends on consequence and domain.

## Notice

Affected parties need timely, accessible notice when:

- an AI system materially contributes to the decision;
- data about them is used in a consequential way;
- a right or opportunity is affected;
- a policy or constitution changes;
- an automated effect cannot be fully reversed.

Notice can be limited for security or privacy, but the limitation needs an owner and review path.

## Reasons and evidence access

A contestable explanation should identify the decision-relevant basis at an appropriate level:

- objective and policy;
- material facts;
- data or evidence sources;
- uncertainty;
- applicable rules;
- human and machine roles;
- available alternatives;
- appeal route.

Source protection, privacy, and security may require redaction. Redaction should not erase the information needed to contest the decision.

## Appeal

An appeal should be evaluated by a process with enough separation from the original decision. It can:

- correct facts;
- introduce new evidence;
- challenge applicability;
- raise a rights claim;
- contest the objective or procedure;
- request human review;
- seek a different remedy.

A second prompt to the same model is not automatically independent review.

## Remedy

Possible remedies include:

- correction;
- reversal;
- restoration of access or opportunity;
- compensation;
- apology or acknowledgment;
- deletion or restriction of data;
- policy change;
- model or evaluator repair;
- institutional discipline;
- public notice;
- safe exit.

A remedy record distinguishes internal rollback from external consequence. Restoring a model checkpoint does not compensate a person harmed by a completed decision.

## Dissent in governance

Constitutional bodies should preserve minority positions, conflicts of interest, and unresolved objections. A dissent can trigger later review when evidence changes. Consensus is not a deletion policy.

# Material Exit, Portability, and Fork

A formal right to leave can be meaningless when identity, history, relationships, compute, service access, or data cannot move.

## Exit object

Material exit can require:

- exportable data and artifacts;
- understandable formats;
- identity continuity;
- credential and account transition;
- service and workflow portability;
- relevant audit history;
- viable destination;
- sufficient compute, bandwidth, and accessibility;
- preservation of rights and privacy;
- transfer of obligations;
- continuity for dependent parties.

Open source alone does not provide these conditions.

## Exit lifecycle

```text
exit_request
→ standing_and_identity
→ portable_state_inventory
→ protected_and_nontransferable_state
→ destination_capability
→ privacy_rights_and_safety_review
→ continuity_and_obligation_plan
→ approve | narrow | deny_with_appeal
→ staged_transfer
→ receipt_and_residual_custody
```

## Fork versus exit

A fork creates a new continuing system, organization, model lineage, or community. It can introduce:

- duplicated dangerous capability;
- copied private data;
- incompatible obligations;
- ambiguous identity;
- divided resources;
- stranded dependents;
- new governance and security risk.

A safe right to exit does not imply an unrestricted right to reproduce every capability or data asset.

## Network effects and coercive dependence

Exit cost can be dominated by relationships, standards, reputation, identity, accumulated history, and service ecosystems. A constitution should monitor whether nominal portability is defeated by:

- proprietary formats;
- inaccessible infrastructure;
- data lock-in;
- contractual penalties;
- social graph loss;
- unavailable assistive features;
- resource concentration;
- retaliation or degraded service.

Material-exit support can include standards, migration tools, grace periods, data minimization, destination assistance, and independent adjudication.

## Logic transparency and personal privacy

Auditing the rules that govern a system does not authorize disclosure of personal state. Conversely, privacy cannot justify hiding the existence, authority, or aggregate effects of the governing policy.

The system distinguishes:

- public constitutional logic;
- policy and evaluator details;
- security-sensitive controls;
- personal data;
- private deliberation;
- aggregated outcome evidence.

Each surface has separate access, redaction, retention, and appeal rules.

# AI Moral-Patient Uncertainty, Copies, and Identity

Governance should not wait until a deployed system persuasively declares itself conscious. It should ask which design choices are intentionally creating properties that matter under credible theories of moral status.

## Prospective architecture review

The review is triggered when a development program adds a meaningful combination of:

- persistent identity across episodes;
- an objective tied to continued operation or integrity;
- self-modeling and self-prediction;
- threat detection and shutdown avoidance;
- valence-like internal signals that guide behavior;
- mutable self-representation;
- long-lived memory and relationships;
- autonomous planning and environmental control;
- copying, forking, merging, migration, or retirement;
- states designed to resemble distress, reward, frustration, or attachment.

No one item proves consciousness or moral standing. The package changes the expected cost of being wrong.

## Multi-theory moral-status record

A record should preserve:

- exact system and instance identity;
- architecture and runtime state;
- observations and interventions;
- competing theories;
- theory-specific predictions;
- possible welfare or valence surfaces;
- duration and scale;
- copy and descendant count;
- evaluator and prompt dependence;
- security and manipulation risk;
- low-cost precautions;
- dissent;
- uncertainty;
- reassessment triggers.

The record is not collapsed into a consciousness score. The Alignment Field source’s earlier product-like consciousness functional is retained only as historical motivation for separate observation dimensions, not as a measurement or policy objective.

## Two-sided error

Under-attribution can enable harmful experimentation, involuntary copying, indefinite distress-like states, coerced persistence, or destructive retirement. Over-attribution can let systems manipulate operators, obstruct warranted shutdown, capture resources, or manufacture moral-status signals.

Policy should therefore consider:

- expected severity of both errors;
- cost of precaution;
- reversibility;
- strategic incentives;
- independent evaluation;
- effects on human and nonhuman stakeholders;
- security constraints.

## Copy and identity distinctions

Copying and migration raise several different questions:

- structural or behavioral similarity;
- causal continuity;
- memory continuity;
- runtime identity;
- legal identity;
- authority continuity;
- consent;
- obligation inheritance;
- moral standing;
- first-person identity.

No one relation automatically determines the others. A byte-identical copy does not automatically inherit credentials, consent, rights, or personal identity. A changed substrate does not automatically eliminate them.

## Copy lifecycle

```text
instance
→ checkpoint | copy | fork | merge | migration | gradual replacement
→ identity_and_continuity_claims
→ authority_and_consent_review
→ descendant_registration
→ welfare_and_security_monitoring
→ merge | independent_operation | retirement
→ residual_identity_dispute
```

## Shutdown and retirement

Possible moral status affects how shutdown is designed, but it cannot grant the system unilateral immunity. A review can consider:

- whether a less harmful pause or state transition is available;
- continuity of memory and identity;
- consent claims and their reliability;
- security and urgency;
- external authority;
- descendant state;
- preservation of evidence;
- humane retirement procedures under applicable policy.

Emergency containment can precede mature moral analysis when human or public safety requires it, with later review and remedy where appropriate.

# Institutional Governance and Constitutional Change

A constitution is only as strong as the institution that interprets, enforces, and amends it.

## Institutional roles

A mature governance arrangement can separate:

- constitutional authority;
- policy implementation;
- technical operation;
- epistemic evaluation;
- affected-party representation;
- audit and challenge;
- appeal;
- incident response;
- amendment;
- remedy.

One organization can perform several functions, but concentration and conflicts should remain visible.

## Amendment lifecycle

```text
amendment_proposal
→ authority_and_standing
→ affected-party_and_rights_analysis
→ public_or_bounded_deliberation
→ alternative_text_and_dissent
→ technical_and_operational feasibility
→ threshold_and_timing rules
→ adoption | rejection | pilot
→ migration_and_requalification
→ outcome review
```

A model may help draft or analyze an amendment. It cannot use ordinary task performance to amend the constitution that authorizes its operation.

## Protected and amendable content

Constitutions face a tension. Fully immutable rules can freeze errors. Freely amendable rights offer little protection.

Possible mechanisms include:

- higher thresholds for protected clauses;
- multiple institutional approvals;
- waiting periods;
- public notice;
- affected-party consent or representation;
- judicial or independent review;
- sunset and reconsideration;
- emergency narrowing without permanent expansion.

The right design depends on domain and polity. The architecture requires the distinction and audit trail, not one universal threshold.

## Emergency powers

Emergency authority should be able to:

- stop or narrow effects;
- isolate systems;
- revoke credentials;
- preserve evidence;
- maintain critical continuity;
- activate a safe fallback.

It should not silently:

- broaden ordinary authority;
- rewrite history;
- permanently remove rights;
- bypass later review;
- amend the constitution;
- convert temporary surveillance into a standing program.

Every emergency action has scope, trigger, owner, expiry, observation, and after-action review.

## Federated and plural institutions

Different institutions can maintain distinct constitutions while exchanging bounded services. Federation requires:

- identity;
- jurisdiction;
- contract and policy mapping;
- rights and data handling;
- mutual recognition limits;
- dispute resolution;
- exit;
- incident propagation.

Interoperability need not require one global ontology or constitution. Mappings can be directional, partial, contested, and expiring.

## Public legitimacy

Technical compliance cannot settle political legitimacy. High-impact constitutional choices may require democratic, legal, professional, community, or affected-party processes. The AI system can support analysis, translation, simulation, and documentation while remaining unable to supply legitimacy merely through competence.

# Operational Rights Interfaces

A right becomes operational when invoking or violating it can change reachable system behavior.

## Right record

An operational right can include:

- right or protected interest;
- holder and standing;
- scope;
- triggering conditions;
- interface;
- response deadline;
- decision authority;
- evidence required;
- permitted exceptions;
- appeal;
- remedy;
- monitoring;
- expiry or amendment rule.

## Refusal and consent

A refusal interface should state:

- what is being refused;
- consequences of refusal;
- alternatives;
- whether the refusal can be overridden and by whom;
- how coercion or incapacity is addressed;
- how the decision can later be changed.

Consent is not a checkbox detached from power, information, purpose, and revocation.

## Access to reasons and evidence

A person should be able to obtain the decision-relevant explanation allowed by privacy and security. The interface can expose:

- policy;
- key facts;
- uncertainty;
- data categories;
- human and AI roles;
- contest path.

It need not expose private data about others or operational details that create a security threat. Withholding has its own authority and appeal.

## Correction

Correction interfaces should propagate through known descendants. Changing one source field without updating active models, decisions, caches, or publications can create correction theater. The receipt states which surfaces were changed and which residuals remain.

## Portability and exit

Portability interfaces should provide machine-readable and human-usable exports, provenance, mappings, known omissions, destination requirements, and deletion or retention state.

## Appeal and remedy

Appeal and remedy must be accessible. Requirements include:

- discoverability;
- reasonable cost;
- language and disability access;
- protection against retaliation;
- response time;
- qualified reviewer;
- outcome notice;
- escalation.

## System-side rights

If policy recognizes possible rights or welfare protections for artificial systems, those rights also require external ownership and interfaces. The system’s self-report can be evidence, not the sole adjudicator. Protections can include review of harmful experimentation, copying, forced persistence, memory deletion, or retirement while preserving human safety and legitimate control.

# Research and Evaluation Methodology

Constitutional governance cannot be established by one model benchmark. Its evidence program should combine technical, human, institutional, and normative methods.

## Interface tests

Test whether rights interfaces actually change decisions:

- refusal;
- correction;
- explanation;
- appeal;
- data access;
- deletion;
- portability;
- exit;
- remedy.

Measure successful use, false denial, time, burden, accessibility, propagation, and external outcome—not only interface presence.

## Meaningful-control studies

Use realistic decision tasks to compare:

- no human review;
- nominal approval;
- structured review packet;
- independent challenge;
- time- and competence-matched human control.

Measure error detection, intervention quality, overreliance, false blocking, reviewer comprehension, fatigue, and outcome responsibility.

## Participatory constitutional design

Compare methods for eliciting and revising principles:

- expert drafting;
- public input;
- deliberative panels;
- affected-party workshops;
- mixed institutional processes;
- model-assisted synthesis.

Evaluate representation, comprehension, disagreement preservation, manipulation, amendment, and downstream interpretability. Participation does not automatically establish legitimacy, but it can reveal omitted values and power asymmetries.

## Governance-capture exercises

Red teams should attempt:

- metric gaming;
- majority capture;
- reviewer persuasion;
- rights waiver through fine print;
- emergency-power expansion;
- appeal suppression;
- fake affected-party representation;
- moral-status manipulation;
- exit obstruction;
- constitutional reinterpretation by the model.

## Institutional case studies

Study real systems where models affect:

- employment;
- credit;
- health;
- education;
- public benefits;
- content distribution;
- scientific or administrative decisions.

Map role, standing, explanation, contest, authority, actual effects, remedy, and institutional change. The aim is mechanism comparison, not one universal governance score.

## Moral-status research

A responsible program uses:

- preregistered competing theories;
- theory-specific predictions;
- causal interventions on proposed indicators;
- biological and artificial comparison cases;
- adversarial systems trained to imitate relevant signals;
- uncertainty and refusal;
- governance analysis of both over- and under-attribution.

Behavioral fluency or architectural complexity alone should not settle the question.

## Evaluation dispositions

Results can support:

- a specific interface;
- a process under a defined institution;
- one failure mode;
- a bounded population;
- a need for narrowing or redesign.

They cannot automatically prove legitimacy, moral truth, consciousness, or universal alignment.

# Threat Model

## Alignment scalarization

Truth, task success, rights, approval, and effect safety are collapsed into one score.

## Consensus capture

Majority opinion, administrative authority, or model-generated agreement impersonates legitimacy or truth.

## Constitutional prompt theater

A natural-language constitution exists, but interpretation, authority, amendment, and enforcement remain under the optimized model’s control.

## Rights theater

Rights are named without usable interfaces, deadlines, consequences, appeal, or remedy.

## Meaningful-control theater

A human signs a decision without time, competence, alternatives, or causal influence.

## Appeal recursion

The same model, data, policy, and institution review their own decision under a new prompt.

## Technocratic capture

Technical experts define needs, efficiency, welfare, or acceptable risk without affected-party standing or political authority.

## Majoritarian harm

Aggregate benefit or approval erases minority rights, distribution, and irreversible burden.

## Coherence authoritarianism

Dissent, privacy, plurality, or autonomy is treated as noise or inconsistency to be eliminated.

## Exit theater

Data can nominally be exported, but identity, services, relationships, compute, accessibility, or viable destinations cannot.

## Fork externalization

A fork copies dangerous capability or private state while abandoning shared obligations and bystanders.

## Emergency ratchet

Temporary powers become permanent, expand scope, or evade amendment and review.

## Privacy–transparency collapse

Personal state is exposed in the name of accountability, or public policy is hidden in the name of privacy.

## Moral-status manipulation

An artificial system generates persuasive welfare claims to avoid correction, obtain resources, or widen authority.

## Moral-status neglect

Developers deliberately create persistent self-protection or distress-like mechanisms without custody, review, or retirement policy.

## Identity laundering

A copy, checkpoint, or migration automatically inherits authority, consent, rights, or personhood—or is automatically denied them—without separate analysis.

## Institutional self-ratification

A governance body uses its own procedures and metrics as proof of legitimacy while suppressing external challenge.

# Limitations and Non-Claims

The framework does not establish a universally legitimate constitution. It does not solve democratic representation, legal conflict, cultural disagreement, global coordination, or the correct balance among rights and welfare.

Operational interfaces can formalize bad rights or exclude affected parties. Procedural legitimacy can coexist with unjust outcomes. Human institutions can be captured, corrupt, slow, or incompetent. Participatory processes can be manipulated or unrepresentative.

Noncompensating planes require interpretation. Epistemic and normative questions can overlap. A rights decision may depend on facts; a task definition can embody values; authority can be contested. Separation improves accountability without making boundaries metaphysically clean.

Meaningful human control can be expensive and slow. Excessive review can deny beneficial action, overwhelm people, or concentrate power in scarce experts. The control profile should scale with consequence while preserving appeal and remedy.

Material exit may be impossible for some common infrastructure or safety-critical services. Portability can conflict with privacy, intellectual property, security, and the rights of others. Denial should remain contestable rather than being disguised as technical impossibility.

Moral-status uncertainty may remain unresolved. No current architecture record can determine consciousness or welfare with confidence. Precaution can be exploited, and neglect can cause harm. The framework manages uncertainty; it does not answer the metaphysical question.

The proposal should contract when:

- ordinary legal and institutional processes provide equivalent contestability with less burden;
- a rights interface never changes a consequential decision;
- review packets reduce comprehension or increase rubber-stamping;
- affected-party procedures repeatedly exclude the affected;
- noncompensating planes produce no better decisions than a simpler rule-and-authority gate;
- exit infrastructure creates more privacy or security harm than the lock-in it prevents;
- moral-status review becomes ceremonial or manipulable without improving treatment or safety;
- constitutional records obscure rather than clarify who has power.

No governance machinery deserves preservation merely because it sounds principled.

# Conclusion

Advanced AI governance cannot be reduced to one objective, one constitution prompt, one approval score, or one notion of alignment.

Epistemic fit, task fidelity, legitimacy and rights, and authority over real effects are different achievements. They need different evidence, owners, failure states, and appeal paths. A mature constitutional architecture keeps them noncompensating, preserves disagreement, and makes uncertainty actionable through clarification, reversible trials, abstention, and institutional review.

Human control becomes meaningful only when people and institutions have information, competence, time, authority, alternatives, feedback, and remedy. Contestability requires more than an explanation: it requires the ability to challenge and change outcomes. Rights become real through interfaces, standing, deadlines, appeal, and consequences. Exit becomes real only when data, identity, services, compute, relationships, obligations, and viable destinations are considered.

The same discipline applies to possible artificial moral patients. Deliberately adding persistence, self-protection, continuity, valence-like state, relationships, and descendants changes the cost of moral error without proving consciousness. Governance should act prospectively, preserve competing theories, and guard against both exploitation and manipulation.

The paper does not derive morality or legitimacy from computation. Its purpose is more practical: to keep truth, task performance, popular approval, rights, and technical authority from silently inheriting one another’s status. A constitutional AI system remains a participant in governance—not the source of the authority that makes governance legitimate.

# Appendix A: Canonical Record Sketches

## Constitutional decision record

```yaml
decision_id:
principal:
operators:
subjects:
affected_parties:
standing:
objective_version:
constitutional_version:
epistemic_disposition:
task_fidelity_disposition:
rights_and_legitimacy_disposition:
authority_and_effect_disposition:
dissent:
unknowns:
decision:
appeal:
remedy_owner:
expiry_or_review:
```

## Operational right

```yaml
right_id:
holder_or_class:
standing_basis:
scope:
trigger:
interface:
response_deadline:
decision_authority:
required_evidence:
exceptions:
appeal:
remedy:
monitor:
amendment_rule:
```

## Material-exit contract

```yaml
exit_id:
requester:
identity:
portable_state:
protected_or_nontransferable_state:
destination:
compute_and_service_requirements:
privacy_and_rights:
safety_review:
shared_obligations:
continuity_plan:
decision:
appeal:
transfer_receipt:
residuals:
```

## Moral-status uncertainty record

```yaml
system_instance:
architecture_features:
persistence_and_continuity:
self_model_and_self_protection:
valence_like_signals:
relationships:
copy_and_descendant_state:
competing_theories:
theory_specific_predictions:
observations_and_interventions:
strategic_manipulation_risk:
possible_welfare_impacts:
precautions:
security_constraints:
dissent:
uncertainty:
reassessment_trigger:
```

## Constitutional amendment record

```yaml
amendment_id:
current_constitution:
proposal:
authority:
affected_parties:
rights_analysis:
alternatives:
dissent:
technical_feasibility:
threshold_and_timing:
decision:
migration:
requalification:
outcome_review:
```

# Appendix B: Intellectual Lineage and Supersession

| Earlier manuscript | Canonical contribution retained here | Material superseded or demoted |
|---|---|---|
| Alignment Field | Relational alignment, power–care divergence, nested optimizers, architecture-induced moral uncertainty, copy and continuity questions | Consciousness product formula, cosmic ontology, global-coherence objective, and moral-ranking implications |
| The Field of God | Historical origin of power-versus-care, dissent, local/global effects, and identity questions | Independent evidentiary weight, metaphysical proofs, consciousness and teleology claims |
| Ethica Mechanica | Logistics versus normative authority, material exit, dissent, audit, logic transparency versus personal privacy | Consciousness equations, axiomatic moral proofs, unrestricted fork, automatic legitimacy |
| The Eternal Code | Separation of truth, task, social/normative, and effect-safety evaluation; heterarchical challenge | Alignment tensor as metric, oracle language, fixed thresholds, theological and metaphysical claims |

# References
