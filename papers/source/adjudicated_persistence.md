# Adjudicated Persistence

## Governing the Transition from Experience to Durable Structure in Adaptive Systems

**Corben Sorenson**  
**Standalone research manuscript · Version 1.0 · August 2026**

---

## Abstract

Adaptive systems increasingly learn through more than model-weight updates. Experience can alter long-term memory, training data, prompts, tools, policies, evaluators, agent harnesses, multi-agent topology, environments, and organizational routines. Existing research usually studies these adaptation surfaces separately or assumes in advance where a lesson should be stored. This leaves a prior problem unresolved: **when should transient experience acquire durable influence, where should that influence reside, how strongly should it bind future behavior, and what evidence should be required before commitment?**

This paper introduces **Adjudicated Persistence**, a general framework for governing the transition from experience to durable adaptive structure. It treats persistence as a consequential effect rather than passive storage. The framework distinguishes six objects that are often collapsed: experience records, lesson hypotheses, persistence dispositions, concrete realizations, qualification leases, and authority grants. It formulates **Cross-Surface Adaptation Assignment** as a portfolio problem over heterogeneous adaptation loci, including parameters, memory, procedures, semantic models, orchestration, system structure, evaluators, environments, and institutions. It then introduces multidimensional commitment profiles spanning scope, binding strength, persistence, coupling, authority, irreversibility, and descendant reach.

The **Evidence-Commitment Matching Principle** requires that a realization's commitment burden remain within the support provided by its evidence and legitimate authority. The **Minimum Sufficient Persistence Principle** favors the least committing admissible portfolio that achieves required efficacy, coverage, capability preservation, observability, and recovery. The framework further defines guarded compilation, explicit `UNKNOWN` routes, slow-path preservation, transactional promotion, material-change invalidation, outcome-maturity states, counterfactual observability, a deliberation reserve, persistence carrying costs, and non-self-ratifying meta-compilation.

The paper argues that cumulative intelligence should ratchet accountable knowledge, recoverability, and known residual structure rather than assume monotonic improvement under one behavioral scalar. It presents bounded propositions showing that terminal outcomes cannot determine a universally correct adaptation locus and that open-world ratchets cannot be defined by one invariant performance score under legitimate objective change. Finally, it proposes **LocusBench**, an experimental program in which matched outcomes arise from different causal defects and therefore require different persistence decisions. Adjudicated Persistence is offered as a conceptual framework and falsifiable research agenda. It does not claim a universal placement algorithm, complete causal identification from arbitrary traces, perfect evaluator independence, complete reversibility, or validated recursive self-improvement.

**Keywords:** continual learning; agent memory; adaptive systems; procedural memory; model editing; tool learning; organizational learning; causal attribution; AI governance; self-improvement; meta-learning; persistent agents

---

## Research status and non-claims

This manuscript proposes a theory, formal vocabulary, system architecture, and experimental program. It does **not** report a completed implementation of the full framework. Recent 2025-2026 systems cited throughout the paper are often preprints and are used to establish contemporary design pressure, not settled consensus. The framework does not imply that every experience should be preserved, that every recurring behavior should be automated, that every capability should migrate outside model weights, or that governance records make an unsafe system safe. Its central claim is narrower: the transition from transient experience to durable influence is an identifiable and consequential design boundary that deserves explicit adjudication.

---

## Contents

1. The Ungoverned Commit Boundary  
2. Learning Is More Than Weight Change  
3. Related Work and the Missing Cross-Surface Problem  
4. Formal Ontology  
5. Experience Integrity and Learning Eligibility  
6. Cross-Surface Adaptation Assignment  
7. Commitment Profiles and Evidence-Commitment Matching  
8. Minimum Sufficient Persistence  
9. Guarded Compilation and Adaptation Transactions  
10. Counterfactual Observability and the Deliberation Reserve  
11. Persistence Costs, Adaptation Debt, and the Ratchet  
12. Organizational, Environmental, and Institutional Persistence  
13. Meta-Compilation Without Self-Ratification  
14. Bounded Propositions and Empirical Conjectures  
15. LocusBench  
16. Threat Model and Failure Taxonomy  
17. Implementation Architecture  
18. Discussion  
19. Limitations and Non-Claims  
20. Conclusion  
Appendices  
References

---

# 1. The Ungoverned Commit Boundary

## 1.1 From momentary output to durable influence

A stateless system can be wrong once. A persistent system can make one error into a rule.

This difference is easy to underestimate because durable adaptation often appears as an ordinary internal operation: append a memory, add a demonstration, update an adapter, register a tool, revise a system prompt, promote a workflow, modify an evaluator, or change a team role. Yet each operation changes the probability distribution of future behavior across episodes. Persistence is therefore not merely a storage property. It is a **causal effect on the future**.

Consider a conversational assistant that reads an untrusted email and stores the claim that its user prefers a particular vendor. The original interaction may end harmlessly, but the memory can influence later recommendations, searches, messages, and purchases. Recent persistent-memory benchmarks and attacks show that stored state can create cross-domain leakage, sycophantic reinforcement, delayed action steering, and long-lived compromise [29-33]. The exact numbers and attack methods will change, but the architectural lesson is stable: a write into durable adaptive state can have a larger and less visible blast radius than the output that caused it.

The same boundary appears far beyond memory:

- A trajectory added to a fine-tuning set can influence millions of future generations.
- A reward-model revision can redefine which behavior is reinforced.
- A generated tool can replace repeated reasoning across many tasks.
- A regression test can make one historical failure a permanent capability floor.
- A multi-agent routing change can alter which subsystem receives future evidence.
- An organizational procedure can transfer decision rights, burden, and accountability across people and machines.
- A compiler update can change how all later lessons are interpreted and installed.

These are different mechanisms, but they share one event: **transient evidence crosses a boundary and acquires durable influence**.

This paper calls that boundary the **Adaptive Commit Boundary**.

![Figure 1. The Adaptive Commit Boundary separates transient evidence and interpretation from qualified persistent realization and its future causal reach.](figures/figure1_commit_boundary.png)

*Figure 1. The Adaptive Commit Boundary. Counterexamples, drift, and revocation reopen the commit decision rather than silently preserving stale structure.*

## 1.2 The prior question hidden inside learning

Machine learning typically asks how to update a selected parameterization. Continual learning asks how to update it without catastrophic forgetting [1-3]. Model editing asks how to change a fact or behavior locally [5,6]. Agent-memory research asks what to store and retrieve. Skill-learning systems ask how to preserve successful workflows. Organizational-learning research asks how repeated performances become routines [11,12]. Self-improving-agent research asks how systems can alter their own code or scaffolding [21-23,38].

Each line of work is important. But each often begins **after** a consequential choice has already been made: the adaptation locus has been selected.

The event will become a gradient.

The event will become a memory.

The event will become a skill.

The event will become a rule.

The event will change the organization.

The prior question is:

> **What relationship to persistence does this experience deserve?**

That question includes several subquestions:

1. What actually happened?
2. What, if anything, does the evidence justify learning?
3. Which causal mechanism should change?
4. Where should the lesson be realized?
5. Should it be represented in one locus or several?
6. How strongly should it bind future behavior?
7. What authority permits that influence?
8. How will its assumptions be monitored?
9. What happens if the lesson is later narrowed, contradicted, or revoked?

Without explicit answers, adaptive systems can turn noise into memory, correlation into policy, evaluator weakness into objective, successful improvisation into brittle automation, and local repair into global rigidity.

## 1.3 Persistence is neither memory nor learning alone

The word *persistence* is used here in a broad but disciplined sense. A state item is persistent relative to an adaptive identity when it can survive beyond the episode that produced it and influence later decisions, outputs, evaluations, resource allocations, or successor states.

This includes, but is not limited to:

- parametric state;
- optimizer and adapter state;
- episodic and semantic memory;
- replay buffers and curated datasets;
- prompts, policies, and routing rules;
- tools, skills, workflows, and code;
- world-model concepts and dynamics;
- tests, benchmarks, critics, and reward models;
- agent roles and communication topology;
- interfaces, interlocks, and environmental structure;
- institutional routines, permissions, and governance rules.

A particular object can be external at one resolution and internal at another. A tool is external to a language model but internal to an agent. A shared memory is external to one agent but internal to a team. A procedure is external to a worker but internal to an organization. The theory must therefore declare the adaptive identity and resolution under study rather than assuming that the learner is the model.

## 1.4 Central thesis

The central thesis is:

> **Cumulative intelligence depends not only on the capacity to adapt from experience, but on the capacity to govern what experience is allowed to become persistent.**

A mature adaptive system should:

1. preserve a defensible record of experience;
2. adjudicate whether a durable lesson is identifiable and legitimate;
3. separate the lesson from any particular implementation;
4. choose a portfolio of adaptation loci;
5. match commitment strength to evidence and authority;
6. compile guarded realizations;
7. qualify the exact realizations before ordinary use;
8. preserve a viable slow path and counterfactual observability;
9. monitor assumptions, descendants, and delayed effects;
10. narrow, relocate, decompile, unlearn, compensate, revoke, or retire structure when warranted.

The paper calls this theory **Adjudicated Persistence**.

![Figure 2. The Search-to-Structure Ratchet cycles from novelty through flexible computation, experience, adjudication, placement, guarded compilation, qualification, monitoring, and reconsideration.](figures/figure4_search_structure_ratchet.png)

*Figure 2. The Search-to-Structure Ratchet. Structure is neither terminal nor irreversible; residuals and invalidated assumptions return control to novelty-handling mechanisms.*

## 1.5 Contributions

This paper makes ten conceptual contributions.

**First, it identifies the Adaptive Commit Boundary.** Persistent writes, updates, and promotions are treated as consequential effects requiring admission discipline.

**Second, it separates six objects:** experience record, lesson hypothesis, disposition, realization, qualification lease, and authority grant.

**Third, it defines learning eligibility before adaptation.** An outcome can justify investigation or containment without justifying a policy update.

**Fourth, it formulates Cross-Surface Adaptation Assignment.** Lessons are assigned to portfolios across heterogeneous adaptation loci rather than one presumed destination.

**Fifth, it defines multidimensional commitment profiles** spanning scope, binding strength, persistence, coupling, authority, irreversibility, and descendant reach.

**Sixth, it introduces Evidence-Commitment Matching.** Evidence obligations are derived from the proposed commitment profile and lesson class.

**Seventh, it introduces Minimum Sufficient Persistence.** The preferred realization is the least committing admissible portfolio, subject to efficacy, capability, observability, and recovery constraints.

**Eighth, it requires guarded use, `UNKNOWN` routes, re-expansion triggers, and a deliberation reserve.** Compilation cannot eliminate the general mechanism needed for novelty and repair.

**Ninth, it defines a non-self-ratifying meta-compilation boundary.** A compiler may propose improvements to itself but cannot be the sole authority that declares them better.

**Tenth, it proposes LocusBench,** a benchmark in which similar outcomes arise from different causal loci and therefore require different persistence decisions.

---

# 2. Learning Is More Than Weight Change

## 2.1 A multiscale view of adaptive state

A system is adaptive when some state persists, can change in response to evidence, and can alter later behavior. Parameters are one form of adaptive state, not its definition.

At a fine scale, persistent state may include:

- model weights;
- optimizer moments;
- adapters;
- recurrent state;
- learned caches;
- memory indexes;
- curriculum policies;
- evaluator parameters.

At a system scale, it may include:

- tool registries;
- workflow libraries;
- prompts and policies;
- context-selection rules;
- planning heuristics;
- credentials and permissions;
- runtime monitors;
- agent roles and communication edges.

At an organizational scale, it may include:

- operating procedures;
- decision rights;
- escalation routes;
- institutional records;
- incentives;
- review requirements;
- staffing structures;
- interface design.

The operative learner is therefore resolution-relative.

Let an adaptive identity at resolution \(\rho\) have persistent state:

\[
A_t^\rho = \left\{A_{\ell,t}^\rho : \ell \in \mathcal L \right\},
\]

where \(\mathcal L\) is the registry of adaptation loci.

The same physical component may participate in several identities. A model's weights belong to the model, the agent that invokes it, the team that routes to it, and the organization that deploys it. Claims about learning must state which identity and which observables are being discussed.

## 2.2 Adaptation loci

This paper uses nine broad locus classes.

| Locus | Persistent structures | Typical advantage | Typical risk |
|---|---|---|---|
| Parametric | weights, adapters, value functions, policies | broad low-latency generalization | interference, opacity, difficult revocation |
| Mnemonic | episodic memory, semantic memory, indexes, summaries | fast and inspectable updates | poisoning, retrieval failure, scope leakage |
| Procedural | tools, code, workflows, controllers, checklists | exactness and testability | brittle preconditions and invocation failure |
| Semantic | concepts, schemas, causal relations, world-model dynamics | coherent downstream generalization | broad propagation of mistaken abstractions |
| Orchestration | prompts, routing, context construction, retries, budgets | rapid system-level adaptation | hidden coupling and context burden |
| Structural | modules, agent roles, communication topology, execution order | localized specialization and coordination | attribution and integration complexity |
| Evaluative | tests, benchmarks, critics, reward models, monitors | durable failure memory and selection pressure | Goodharting and evaluator capture |
| Environmental | interfaces, APIs, interlocks, physical or digital structure | structural prevention and lower actor burden | rigidity and displaced burden |
| Institutional | SOPs, permissions, incentives, escalation, governance | coordination across many actors and time | legitimacy, power, inertia, enforcement failure |

These classes are not ontologically absolute. They are a comparison vocabulary. A compiled policy can be procedural or parametric depending on implementation. A test can be evaluative and institutional. An interface can be environmental and procedural. Ambiguity should be resolved by declaring the state, consumer, and causal role, not by forcing every artifact into one box.

## 2.3 Adaptation mechanisms are not adaptation surfaces

Training, reinforcement learning, fine-tuning, distillation, reflection, replay, program synthesis, tool generation, and organizational review are **mechanisms**. Weights, memories, tools, evaluators, topologies, and procedures are **surfaces** or loci. Online, episodic, nightly, batch, release-cycle, and constitutional are **timescales**.

These dimensions should remain separate.

A policy-gradient mechanism may update parameters.

A language model may synthesize a tool.

A human tribunal may revise an evaluator.

An agent can use reflection to write memory.

A postmortem can change an organizational procedure.

The mechanism does not determine the correct locus, and the locus does not determine the legitimate authority.

## 2.4 Persistence as a partial order, not a binary label

An update is not simply temporary or permanent. Persistent influence differs along several axes:

- how broad a domain it covers;
- how strongly it constrains behavior;
- how long it remains active;
- how many downstream systems depend on it;
- what authority it carries;
- how reversible its effects are;
- how widely it propagates into descendants.

A warning memory can be persistent but weakly binding. A runtime interlock can be narrowly scoped but strongly binding. A weight update can be broad and coupled yet carry no direct authority to execute external effects. A governance rule can be formally revocable while producing long-lived social descendants.

This multidimensionality motivates commitment profiles developed in Section 7.

## 2.5 Not all learning is compilation

The term *compilation* is useful only if it excludes something.

A persistent change qualifies as **adaptive compilation** only when it has:

1. an identifiable source experience or evidence family;
2. an abstracted lesson rather than a verbatim record alone;
3. a declared class of future situations;
4. a computational consequence for future search, reasoning, execution, verification, or coordination;
5. an applicability envelope and `UNKNOWN` route;
6. a qualification method;
7. a lifecycle that supports revision, narrowing, supersession, or retirement.

The following are not automatically compilation:

- storing an unreviewed episode;
- taking an ordinary gradient step;
- copying one successful trajectory into a prompt;
- changing a reward after one desirable outcome;
- adding an unscoped rule;
- preserving a correlation without transfer tests;
- modifying an evaluator to make a candidate pass;
- or installing an adaptation that cannot be challenged.

Compilation is therefore a subset of persistent adaptation. Adjudicated Persistence governs the larger decision of whether any durable adaptation should occur.

## 2.6 Internalization, externalization, and institutionalization

Three broad forms clarify the design space.

### Internalization

The lesson is encoded inside the current adaptive identity:

- parameters;
- adapters;
- value functions;
- local memory;
- internal policies.

### Externalization

The lesson becomes an addressable artifact:

- tool;
- program;
- test;
- procedure;
- semantic object;
- benchmark;
- documentation;
- executable guard.

### Institutionalization

The lesson changes shared structure:

- roles;
- decision rights;
- communication topology;
- incentives;
- permissions;
- escalation paths;
- standards;
- environmental design.

A lesson can move between these forms. A provisional memory can become a verified tool. A tool can later be distilled into a model. A model behavior can be externalized into a test. A recurring workaround can reveal that the environment should be redesigned. The lesson's identity and evidence should remain continuous across relocation.

---

# 3. Related Work and the Missing Cross-Surface Problem

## 3.1 Continual learning and model editing

Continual-learning research has long studied how a parameterized learner can acquire new knowledge without catastrophically overwriting old knowledge. Complementary Learning Systems theory motivates a fast episodic system and slower integrative learning [1]. Elastic Weight Consolidation protects parameters important to previous tasks [2], while Gradient Episodic Memory constrains updates using remembered examples [3]. Machine-unlearning research asks how previously admitted data or influence might later be removed [4].

Model-editing methods such as ROME and MEMIT seek localized factual changes in transformer models [5,6]. These methods sharpen important questions about locality, generalization, side effects, and mass editing. Yet they largely assume the target surface: model parameters. Adjudicated Persistence asks an earlier question: should the correction be in parameters at all, or would a memory invalidation, retrieval rule, tool repair, evaluator change, or scoped guard be more appropriate?

## 3.2 Memory, skills, and agent adaptation

Agent systems increasingly adapt outside weights. ExpeL stores distilled experiential lessons [16]. Toolformer learns when to invoke external APIs [17]. Voyager accumulates executable skills during open-ended embodied interaction [18]. ATLAS shifts continual adaptation into orchestration and persistent guidance rather than gradient updates [20]. ALMA meta-learns memory designs [21]. Memento-Skills evolves externalized skills and prompts [22], MemoHarness adapts multiple harness dimensions from execution history [23], SkillDroid compiles successful GUI trajectories into reusable parameterized skills [24], and SkeMex distills medical-agent experience into governed skill memory [25].

These systems demonstrate that persistent adaptation can live in many places. A recent survey of agentic adaptation explicitly organizes the field across agent and tool adaptation [19]. But most individual methods select a principal surface in advance. The unresolved general problem is how to adjudicate among surfaces—or combine them—when the source defect is heterogeneous or uncertain.

## 3.3 Library learning, amortization, and proceduralization

Amortized optimization learns to predict solutions to repeatedly encountered related optimization problems, trading upfront learning for lower future solution cost [7]. Partial evaluation specializes a general program using known information [8]. DreamCoder grows symbolic libraries and search policies from solved tasks [14], while Stitch extracts reusable abstractions from program corpora efficiently [15].

These traditions make the search-to-structure idea concrete. Solved experience can lower future search breadth, depth, or execution cost. However, the central problem is usually posed inside a fixed representation family: which library primitive or specialized program should be produced? Adjudicated Persistence generalizes the question to heterogeneous adaptive surfaces and adds evidence, authority, commitment, and revocation.

## 3.4 Profile-guided compilation, guards, and deoptimization

Profile-guided optimization uses observed execution profiles to specialize future execution [9]. Dynamic optimization systems place guards around speculative assumptions and transfer control back to a general representation when an assumption fails [10]. These mechanisms supply a powerful analogy:

| Adaptive system | Runtime-compilation analogue |
|---|---|
| flexible reasoning or search | interpreter |
| experience trace | runtime profile |
| recurring transferable pattern | hot path |
| guarded skill or policy | compiled trace |
| applicability condition | guard |
| out-of-scope case | guard failure |
| return to general reasoning | deoptimization |
| broader evidence | tier promotion |

The analogy is useful but incomplete. Software deoptimization can often reconstruct a prior machine state. Adaptive systems may have disclosed data, changed a user, created descendants, altered human skill, or made irreversible external commitments. This paper therefore separates route deoptimization, state rollback, behavioral recovery, compensation, and unlearning.

## 3.5 Trajectory refinement and pedagogical structure

Recent trajectory-level methods reinforce the need to distinguish raw experience from learning material. Trajectory-Refined Distillation revises problematic prefixes before on-policy distillation [27]. Research on terminal-agent training reports a “pedagogical paradox”: a stronger executing agent need not produce the most effective training trajectories, and inspect-act-verify structure can matter for generalization [28]. Falsifiable Commitment Planning attaches confirming and falsifying evidence to active plan steps and repairs the smallest level whose evidence fails [26].

These results support two distinctions central to this paper:

1. **execution-efficient experience is not necessarily pedagogically efficient experience;**
2. **a successful outcome does not validate every step, rationale, or implied precondition.**

The paper therefore treats trajectory compilation as one realization inside a broader persistence framework, not the framework's total scope.

## 3.6 Persistent-state security and governance

Persistent memory creates safety and security questions that stateless benchmarks miss. PersistBench reports cross-domain leakage and memory-induced sycophancy across evaluated models [29]. The Always-On Agents survey treats persistent agents as systems containing memories, permissions, credentials, commitments, provenance, shared state, triggers, and external effects—not just retrieved text [30]. MemSecBench traces malicious semantics through write, action, and selective repair [31]. WhisperBench/MemGhost and sleeper-memory work show that untrusted external content can be stored silently and influence future behavior [32,33].

These works motivate a stronger rule than “memory should be accurate”:

> **A persistent write is an authority-bearing lifecycle event whose future scope must be governed.**

Adjudicated Persistence extends this concern beyond memory to every surface capable of carrying durable influence.

## 3.7 Reward ambiguity, Goodhart pressure, and evaluator capture

Reward and evaluator signals do not uniquely identify the intended objective. Reward-learning work formalizes partial identifiability: distinct reward functions can induce indistinguishable observed behavior under a given observation regime [34]. Iterative self-refinement can improve a model evaluator's score while human-perceived quality stagnates or worsens [35]. Goodhart variants describe several mechanisms by which optimized measures diverge from intended goals [36]. Safely interruptible agents further show that a learner may adapt against an intervention mechanism unless the learning process is designed carefully [37].

These results motivate a **normative firewall**. Evidence that an objective or evaluator failed may justify containment, investigation, or a new governance process. It does not by itself authorize the actor to rewrite the objective or evaluator that constrains it.

## 3.8 Organizational routines and exploration

Organizational learning offers a mature analogue of experience becoming structure. March formalized the tension between exploitation of known structure and exploration of alternatives, warning that adaptive processes can become effective in the short term while undermining long-run exploration [11]. Feldman and Pentland distinguish the ostensive aspect of a routine from its specific performances, showing how performances reproduce and modify persistent routine structure [12]. Empirical work on algorithmic recommendation tools suggests that automation can reduce experiential learning and skill retention in organizations [13].

This literature supplies two crucial warnings:

- efficient compiled structure can starve the exploratory process that produced it;
- organizational persistence is not reducible to any individual's memory or weights.

The framework therefore includes a deliberation reserve and treats organizations as possible adaptive identities in their own right.

## 3.9 Self-improvement and meta-adaptation

The Darwin Gödel Machine explores and empirically validates modifications to coding-agent architectures while preserving an archive of alternatives [38]. ALMA searches over memory designs [21], while Memento-Skills and MemoHarness adapt skills or harnesses from experience [22,23]. These systems suggest a recursive progression: experience can change not only task behavior but the machinery that learns from experience.

The central risk is self-ratification. A candidate improvement process can learn to satisfy its own evaluator, alter its test distribution, or erase its predecessor. This paper permits meta-compilation only under a separation between proposal authority and promotion authority.

## 3.10 The missing conjunction

The reviewed fields provide many necessary mechanisms, but they rarely make the following conjunction the central object:

1. learning eligibility before durable adaptation;
2. causal and normative adjudication;
3. a registry of heterogeneous adaptation loci;
4. portfolio placement rather than one chosen surface;
5. stable lesson identity separated from realization;
6. multidimensional commitment profiles;
7. evidence obligations derived from commitment;
8. transactional promotion and material-change invalidation;
9. guarded execution, `UNKNOWN`, and re-expansion;
10. counterfactual observability and slow-path conservation;
11. organizational and environmental realization;
12. meta-compilation without self-ratification.

Adjudicated Persistence is proposed to fill that systems-level gap.

---

# 4. Formal Ontology

## 4.1 Six objects

The framework distinguishes six objects.

### Experience record

A versioned statement of what was observed, attempted, omitted, and produced.

### Lesson hypothesis

A defeasible, testable claim about reusable causal, behavioral, procedural, semantic, or evaluative structure.

### Persistence disposition

The decision about whether the experience should be rejected, retained, investigated, contained, compiled, escalated, or used to revoke an earlier lesson.

### Realization

A concrete artifact that expresses the lesson in a particular locus: memory, data, adapter, tool, test, guard, policy, topology, interface, or procedure.

### Qualification lease

A scoped claim that an exact realization, dependency closure, environment, consumer, and use have passed specified tests for a limited time.

### Authority grant

The permission for a qualified realization to influence or cause particular effects.

The six objects form a strict separation:

\[
\boxed{
\text{support}
\neq
\text{implementation}
\neq
\text{qualification}
\neq
\text{authority}
}
\]

A lesson can be well supported but poorly implemented. A realization can exist but remain unqualified. A qualified capability can remain unauthorized for a consequential use.

## 4.2 Experience record

Let an experience be:

\[
e = (\nu,\rho,z,I_0,\Omega,\tau,O,Y,P),
\]

where:

- \(\nu\) is the exact version bundle of model, memory, tools, prompts, policies, evaluators, environment, and dependencies;
- \(\rho\) is the adaptive resolution;
- \(z\) is the typed operating region;
- \(I_0\) is the information available at the relevant decision or commitment time;
- \(\Omega\) contains objectives, constraints, rights, and authority;
- \(\tau\) is the realized trajectory;
- \(O\) is the admitted observation record;
- \(Y\) contains immediate and delayed outcomes;
- \(P\) contains provenance, custody, missingness, and integrity information.

The record must preserve distinctions among:

\[
\text{observed},
\text{inferred},
\text{predicted},
\text{counterfactual},
\text{evaluated},
\text{normatively judged}.
\]

A fluent retrospective narrative is not a substitute for the original information boundary.

## 4.3 Operating regions

An operating region \(z\) is a typed predicate over factors such as:

- task family;
- environment;
- user or stakeholder class;
- system version;
- tool state;
- time horizon;
- consequence class;
- authority profile;
- distribution regime;
- observability condition.

Regions are neither necessarily natural nor disjoint. They are auditable scopes for evidence and policy.

If regions are too coarse, rare failures disappear inside averages. If they are too fine, evidence becomes nontransferable and assurance becomes unaffordable. Region schemas should therefore support hierarchical split and contraction under observable-preservation tests.

## 4.4 Lesson hypothesis

A lesson is:

\[
L = (id,v,\phi,\mathcal D,E,X,U,T,N),
\]

where:

- \(id\) is a stable lineage handle;
- \(v\) is the lesson version;
- \(\phi\) is a testable hypothesis;
- \(\mathcal D\) is the applicability domain;
- \(E\) is supporting evidence;
- \(X\) contains exceptions, contradictions, and counterexamples;
- \(U\) represents uncertainty;
- \(T\) states temporal validity;
- \(N\) records normative and authority status.

The stable handle preserves continuity without claiming a timeless essence. Valid lifecycle operations include:

\[
\texttt{REFINE},\ 
\texttt{NARROW},\ 
\texttt{EXPAND},\ 
\texttt{SPLIT},\ 
\texttt{MERGE},\ 
\texttt{REINTERPRET},\ 
\texttt{SUPERSEDE},\ 
\texttt{REVOKE}.
\]

## 4.5 Outcome maturity

Many experiences are evaluated before their consequences mature. Define:

\[
m_Y \in
\{
\texttt{IMMEDIATE},
\texttt{PROVISIONAL},
\texttt{HORIZON\_OPEN},
\texttt{MATURE},
\texttt{PERMANENTLY\_PARTIAL}
\}.
\]

A successful build, short deployment, or initial organizational gain may support a shadow or canary realization while remaining too immature for permanent global commitment.

Absence of observed failure is meaningful only relative to exposure, observability, and horizon maturity.

## 4.6 Causal identifiability status

Causal conclusions from logs require assumptions about confounding, coverage, timing, and intervention [39,40]. The adjudicator therefore returns:

\[
\iota(L) \in
\{
\texttt{IDENTIFIED},
\texttt{BOUNDED},
\texttt{MODEL\_DEPENDENT},
\texttt{CONFOUNDED},
\texttt{UNIDENTIFIED}
\}.
\]

`MODEL_DEPENDENT` means the conclusion is conditional on an explicit causal or world model. `BOUNDED` means only a range or subset of consequences is justified. `UNIDENTIFIED` does not mean the event is unimportant; it means the system should not pretend to know which policy change it supports.

## 4.7 Provenance and evidence lineage

Every evidence transformation should preserve:

- source identity and role;
- acquisition time;
- valid time;
- transformation chain;
- omissions and redactions;
- custody and integrity;
- evaluator identity;
- version dependencies;
- authority and permitted uses;
- contradictions and supersession.

W3C PROV-O provides a general vocabulary for entities, activities, and agents in provenance chains [41]. Adjudicated Persistence requires additional semantics for learning eligibility, commitment, and authority, but should reuse mature provenance concepts rather than invent incompatible lineage machinery.

## 4.8 Persistence amplification

Let the commitment consequence of realization portfolio \(B\) depend on:

\[
\mu_\Pi(B)
=
f_\Pi
(N_{\text{reuse}},\sigma,b,a,k,d,i),
\]

where:

- \(N_{\text{reuse}}\) is expected future invocation count;
- \(\sigma\) is scope breadth;
- \(b\) is binding strength;
- \(a\) is authority;
- \(k\) is downstream coupling;
- \(d\) is descendant reach;
- \(i\) is irreversibility.

The exact function is domain- and policy-dependent. The architectural requirement is monotonic: holding per-invocation effect constant, broader and less reversible persistence should not require weaker admission evidence.

---
# 5. Experience Integrity and Learning Eligibility

## 5.1 Why outcome-first learning fails

An outcome is an observation about one realized path. It does not identify the lesson.

The same failed outcome can result from:

- an inferior policy;
- a stale or incorrect world model;
- missing or poisoned memory;
- a tool or implementation defect;
- an unavailable check;
- an evaluator defect;
- a misspecified objective;
- another actor's intervention;
- environmental novelty;
- or unavoidable stochasticity.

These causes can require opposite responses.

If a model selects the correct action but a tool executes it incorrectly, broad policy punishment can degrade the model while preserving the actual defect. If the evaluator rewards a shortcut, optimizing harder against the evaluator can deepen the failure. If an adverse outcome was unavoidable from the information available at decision time, treating it as a negative demonstration can teach hindsight rather than competence.

The first persistence decision is therefore not “how should the system update?” It is:

> **Is any durable actor update justified by this experience?**

## 5.2 Integrity before interpretation

The experience record should be admitted for learning only after basic integrity checks.

Minimum checks include:

1. exact identity of the active system and dependencies;
2. trace completeness and known missing intervals;
3. distinction between actor-visible and investigator-visible information;
4. independent confirmation of consequential effects where feasible;
5. source and custody integrity;
6. disclosure of retries, human interventions, and censored attempts;
7. preservation of delayed and unresolved outcomes;
8. detection of duplicated or correlated evidence;
9. separation of reported facts from model-generated narrative;
10. privacy, rights, and authorization for the proposed learning use.

An authenticated trace can still be false, biased, or strategically generated. Integrity makes later review possible; it does not establish truth.

## 5.3 Decision-time reconstruction

Retrospective analysis has access to facts unavailable during the original decision. A fair learning signal must distinguish:

- information available before commitment;
- information acquired during the trajectory;
- information revealed only after the action;
- investigator knowledge introduced later.

Let \(I_t\) be the information available to the actor at time \(t\). A proposed corrective action \(a_t'\) is epistemically admissible only when its justification can be constructed from information available by that point:

\[
\operatorname{Justification}(a_t')
\subseteq
I_0 \cup O_{<t}'.
\]

Later evidence may show that an earlier action was harmful. It cannot silently make a better earlier action knowable.

This distinction prevents **hindsight escalation**: converting ex post knowledge into a training trajectory that presupposes impossible ex ante competence.

## 5.4 Outcome quality and process quality

Outcome quality and process quality should be evaluated independently.

| Outcome | Process | Interpretation |
|---|---|---|
| Good | Defensible | candidate positive evidence |
| Good | Defective | lucky or exploitative success; near-miss evidence |
| Bad | Defensible | possible stochasticity, environment, or insufficient opportunity |
| Bad | Defective | candidate avoidable failure |
| Mixed | Mixed | requires decomposition or longer horizon |
| Unresolved | Unresolved | retain evidence; do not force lesson |

A successful trajectory can contain an invalid shortcut. A failed trajectory can contain a correct prefix, valuable information acquisition, and a sound decision under uncertainty. Outcome-only training erases these distinctions.

## 5.5 Root-cause classes

The adjudicator assigns one or more typed root-cause hypotheses with confidence, interactions, and alternatives.

| Root-cause class | Meaning | Default persistence response |
|---|---|---|
| Policy defect | selected action was inferior under available information | localized policy or rule repair |
| Model defect | dynamics, value, state, or uncertainty model was wrong | data, calibration, or world-model update |
| Memory defect | relevant evidence was absent, stale, poisoned, or misretrieved | memory repair and integrity review |
| Process defect | available procedure, check, or handoff was omitted or failed | procedural or orchestration change |
| Implementation defect | intended plan was sound but execution was incorrect | tool, code, interface, or component repair |
| Evaluator defect | measurement or comparator machinery was wrong | evaluator quarantine and re-adjudication |
| Specification defect | authorized target encoded the wrong goal or rights | normative review; no automatic actor gradient |
| Environmental novelty | prior assumptions no longer covered the state | exploration, model expansion, cautious routing |
| Other-agent effect | another actor materially caused or manipulated the result | attribution, protocol, security, or topology response |
| Unavoidable stochasticity | outcome was not reasonably preventable | record severity; little or no policy penalty |
| Reward exploitation | proxy improved while intended outcome worsened | quarantine, evaluator repair, causal audit |
| Valid optimization | system found a superior admissible behavior | preserve and test counterfactual surplus |
| Unresolved residual | evidence cannot support stable classification | escrow, information acquisition, narrowed claims |

Distributed incidents can have several minimal causal sets. The framework should not force a single “first wrong step” when interactions matter.

## 5.6 Persistence dispositions

The adjudicator returns a disposition:

\[
d \in
\left\{
\begin{array}{l}
\texttt{REJECT},
\texttt{RETAIN\_EVIDENCE},
\texttt{QUARANTINE},
\texttt{INVESTIGATE},
\texttt{CONTAIN},\\
\texttt{COMPILE\_PROVISIONALLY},
\texttt{COMPILE\_SCOPED},
\texttt{REPAIR\_EVALUATOR},\\
\texttt{CHANGE\_ENVIRONMENT},
\texttt{ESCALATE\_NORMATIVE},
\texttt{REVOKE}
\end{array}
\right\}.
\]

### `REJECT`

The event is fabricated, irrelevant, unauthorized for learning use, or otherwise inadmissible.

### `RETAIN_EVIDENCE`

The event matters, but no durable behavioral lesson is justified. The record may support later analysis.

### `QUARANTINE`

The event or candidate lesson is potentially material but unresolved, contaminated, or unsafe to activate.

### `INVESTIGATE`

The expected value of additional information is high enough to justify experiments, comparison, or observation.

### `CONTAIN`

Immediate reversible restrictions are justified before causal explanation matures. Containment does not prove the proposed cause.

### `COMPILE_PROVISIONALLY`

A narrow, low-authority, easily reversible realization may be tested in shadow or diagnostic use.

### `COMPILE_SCOPED`

Evidence supports a qualified realization inside a declared domain and commitment envelope.

### `REPAIR_EVALUATOR`

Actor optimization is paused because evidence quality or target discrimination is inadequate.

### `CHANGE_ENVIRONMENT`

The most appropriate adaptation is a tool, interface, protocol, interlock, or resource redesign.

### `ESCALATE_NORMATIVE`

The event raises a dispute over objective, rights, stakeholder burden, or legitimate authority that cannot be settled by empirical optimization alone.

### `REVOKE`

Existing persistent structure has lost validity, authorization, or acceptable risk status.

## 5.7 Learning eligibility

Define:

\[
\operatorname{Eligible}(L,B)=1
\]

only if:

1. source and version integrity are adequate for the claim;
2. the proposed cause is identified or explicitly bounded;
3. the comparator is feasible under decision-time information, resources, authority, and time;
4. outcome maturity is sufficient for the proposed commitment;
5. evaluator adequacy is not the dominant unresolved defect;
6. the proposed lesson is transferable beyond one idiosyncratic episode;
7. protected valid behavior is represented;
8. the learning use is authorized;
9. the intended realization can be monitored and challenged;
10. unresolved alternatives and residuals remain visible.

Learning eligibility is realization-relative. Evidence sufficient for a warning may be insufficient for a global weight update.

## 5.8 Evaluator-first rule

When evaluator uncertainty dominates, the next adaptation budget should improve the evaluator or evidence rather than optimize the actor against a weak target.

Let \(V_A\) be expected value from actor adaptation and \(V_E\) expected value from evaluator improvement under equal total cost. If:

\[
\mathbb E[V_E] > \mathbb E[V_A]
\]

and evaluator uncertainty is causally material, the system should route to evaluator-first investigation.

The rule is not “evaluators are more important than actors.” It is:

> **Do not increase optimization pressure against a measurement surface that cannot distinguish intended improvement from exploit.**

## 5.9 Algorithm 1: adjudicate experience

```text
ALGORITHM AdjudicateExperience(e, policy Π, evaluator portfolio V)

1. Bind exact system, dependency, objective, authority, and evaluator versions.
2. Validate provenance, custody, privacy, trace integrity, and missingness.
3. Reconstruct decision-time information and available alternatives.
4. Classify outcome maturity and observation sufficiency.
5. Evaluate outcome quality, process quality, authority compliance,
   specification status, and evaluator adequacy independently.
6. Generate feasible comparators under matched information, resources,
   authority, time, and exogenous conditions where possible.
7. Infer minimal causal sets, interaction terms, causal bounds,
   and unresolved hypotheses.
8. Preserve validated prefixes, unaffected components, and protected positives.
9. Generate one or more lesson hypotheses with domains, uncertainty,
   counterexamples, and transfer claims.
10. Assign causal-identifiability status.
11. Select permitted dispositions; do not force actor adaptation.
12. Emit an immutable adjudication receipt and residual set.
```

## 5.10 Worked example: identical failure, opposite update

Two agents submit an incorrect tax calculation.

In the first system, the model retrieves an obsolete threshold from long-term memory but uses the calculation tool correctly. In the second, the model retrieves the current threshold, but the external tool applies the wrong rounding rule.

The terminal output is identical.

An outcome-only learner may add the same negative example to both systems.

Adjudicated Persistence instead produces:

- **System A:** memory invalidation, provenance repair, retrieval freshness test, and perhaps a current-source requirement;
- **System B:** tool quarantine, corrected implementation, unit tests, and replay of affected descendants.

A broad model update may be unnecessary in both cases.

This example establishes the core necessity of adjudication before placement.

---

# 6. Cross-Surface Adaptation Assignment

## 6.1 The placement problem

Once a lesson is eligible for persistence, the system must decide where it should live.

The naive choices are familiar:

- fine-tune the model;
- write a memory;
- add a prompt rule;
- create a tool;
- add a test;
- change the harness;
- change the organization.

The difficulty is that each locus has different causal reach, transfer, latency, interference, interpretability, maintenance, authority, and revocation properties.

The problem is not ordinary credit assignment.

Credit assignment asks:

> Which earlier state, action, or component contributed to the outcome?

Cross-Surface Adaptation Assignment asks:

> Which persistent surfaces should change so that the justified lesson affects the future appropriately?

Causal attribution informs placement but does not determine it. A model can cause a failure while the safest and cheapest response is an external guard. A process can cause repeated errors while a model update improves robustness across many processes. A rare exact exception may belong in memory even when it reveals a broad conceptual gap that also justifies semantic learning.

## 6.2 Portfolio representation

Let a candidate adaptation portfolio be:

\[
B = \left\{(\ell_j,\Delta_j,g_j)\right\}_{j=1}^{n},
\]

where:

- \(\ell_j \in \mathcal L\) is an adaptation locus;
- \(\Delta_j\) is a proposed realization or state change;
- \(g_j\) is an applicability and authority guard.

The portfolio can contain one or several realizations.

A safety lesson might become:

- a contrastive training example;
- a deterministic runtime interlock;
- a regression test;
- a memory record for explanation;
- an organizational escalation condition.

The portfolio is not automatically better because it is redundant. Correlated layers can reproduce one blind spot while increasing maintenance cost. Independence, interaction, and burden must be evaluated.

## 6.3 Candidate-generation channels

Candidate portfolios can be proposed through several channels:

- causal diagnosis;
- similarity to previously qualified lessons;
- hand-authored policies;
- learned placement models;
- program synthesis;
- architecture search;
- human or institutional proposal;
- adversarial red-team suggestion;
- counterfactual evaluation;
- cost and risk optimization.

Candidate generation is untrusted. A high-recall proposer can nominate aggressive updates because qualification remains separate.

## 6.4 Placement features

For each candidate realization \(r\), estimate a vector:

\[
\mathbf u(r) =
(
\Delta Q,
\Delta C,
\Delta R,
T,
I,
O,
M,
H,
X
),
\]

where:

- \(\Delta Q\): target-quality change;
- \(\Delta C\): future computation or coordination saved;
- \(\Delta R\): avoidable risk reduced;
- \(T\): transfer potential;
- \(I\): interference and collateral behavior;
- \(O\): observability;
- \(M\): maintenance and migration burden;
- \(H\): human and stakeholder effect;
- \(X\): option value and exploration effect.

The vector should not be collapsed into one scalar until policy states which tradeoffs are compensable.

## 6.5 Hard constraints and Pareto selection

Define the feasible portfolio set:

\[
\mathcal F(L) =
\left\{
B:
\begin{array}{l}
\operatorname{AuthorityValid}(B)=1,\\
\operatorname{RightsPreserved}(B)=1,\\
\operatorname{CapabilityFloor}(B)\ge f,\\
\operatorname{TargetEfficacy}(B)\ge \eta,\\
\operatorname{Observability}(B)\ge o,\\
\operatorname{Recovery}(B)\ge r,\\
\operatorname{ResidualCustody}(B)=1
\end{array}
\right\}.
\]

Candidate portfolios are compared on a Pareto frontier over target quality, cost, robustness, transfer, interference, human capability, maintenance, externality, and option value.

When two portfolios remain normatively incomparable, the correct result can be:

\[
\texttt{CONTESTED}
\]

rather than a fabricated optimum.

## 6.6 Least-commitment search

The placement process should not attempt exhaustive omniscient optimization over all combinations.

A default staged sequence is:

> **evidence only -> temporary context -> provisional memory**  
> **-> shadow policy -> scoped tool -> adapter**  
> **-> shared model update -> topology change -> institutional change**

This is not a universal risk ranking. A machine-verifiable catastrophic hazard can justify an immediate hard interlock. The ladder is a search strategy: begin with lower-coupling, more observable, more reversible candidates when they can test the lesson adequately, then broaden commitment only when marginal value justifies it.

## 6.7 Placement compatibility hypergraph

Repairs can interact in higher-order ways. Every pair can appear compatible while a triple produces deadlock, overrefusal, or duplicated control.

Let active realizations be \(R=\{r_1,\dots,r_n\}\). Define a typed compatibility hyperrelation:

\[
\chi(S,o,\pi,z)
\in
\{
\texttt{compatible},
\texttt{conflict},
\texttt{unknown}
\},
\]

where:

- \(S\subseteq R\) is a realization subset;
- \(o\) is the integration operator;
- \(\pi\) is update or execution order;
- \(z\) is the operating region.

Compatibility testing should include:

- pairwise and higher-order conflict;
- order sensitivity;
- duplicated coverage;
- probability-mass displacement;
- deadlock and no-action states;
- burden shifts;
- evaluator coupling;
- authority composition;
- rollback interaction;
- re-synthesis quality.

Periodic re-synthesis can consolidate patch collections into a coherent realization, but the modular composition should remain as a rollback and comparison source.

## 6.8 Algorithm 2: propose placement portfolios

```text
ALGORITHM ProposePortfolios(lesson L, locus registry Λ, policy Π)

1. Enumerate admissible locus families from lesson class, cause, volatility,
   frequency, consequence, authority, and revocation requirements.
2. Generate single-locus candidates and a bounded set of complementary bundles.
3. For each candidate:
   a. estimate target efficacy and transfer;
   b. test protected positives and valid exceptions;
   c. estimate interference, false inhibition, and probability displacement;
   d. measure observability and counterfactual observability;
   e. estimate lifecycle, migration, human-skill, and revocation cost;
   f. compute commitment profile;
   g. identify irreversible effects and descendants;
   h. evaluate compatibility with active realizations.
4. Reject candidates violating authority, rights, or hard constraints.
5. Retain the Pareto frontier and explicitly contested alternatives.
6. Order candidates by least commitment and information value.
7. Emit proposed portfolio records; do not promote.
```

## 6.9 Worked example: safe file mutation

Suppose a coding agent repeatedly overwrites files after mistaking exploratory instructions for authorization to modify.

Possible realizations include:

- **weights:** fine-tune the model to distinguish analysis from mutation requests;
- **memory:** store a warning about this repository or user preference;
- **tool:** replace raw writes with a transactional safe-write API;
- **harness:** require a plan/diff phase before mutation;
- **test:** add an evaluation for analysis-versus-action distinction;
- **authority:** require approval for destructive writes.

The best portfolio may combine:

1. a safe-write tool with exact preconditions;
2. a harness guard that separates proposal from commit;
3. a regression test preserving legitimate autonomous edits;
4. a narrow training example improving interpretation.

The tool prevents immediate damage. The training update reduces unnecessary guard activation. The test protects legitimate capability. No single realization is sufficient to capture all objectives.

---

# 7. Commitment Profiles and Evidence-Commitment Matching

## 7.1 Commitment is multidimensional

A realization's future influence cannot be summarized by “stored” or “not stored.” Define its commitment profile:

\[
\Gamma_C(B) = (\sigma,b,p,k,a,i,d),
\]

where:

- \(\sigma\): scope breadth;
- \(b\): behavioral binding strength;
- \(p\): persistence and expected duration;
- \(k\): downstream coupling and dependency centrality;
- \(a\): authority and effect envelope;
- \(i\): irreversibility of internal and external effects;
- \(d\): descendant and propagation reach.

Each dimension can be represented ordinally, quantitatively, or by a domain-specific lattice.

Examples:

| Realization | Commitment pattern | Primary value | Primary risk |
|---|---|---|---|
| forensic record | narrow scope; no behavioral binding; high retention; no effect authority | preserves evidence | privacy and carrying cost |
| provisional memory | task-relative; weakly binding; medium duration and coupling | fast inspectable guidance | poisoning and scope leakage |
| runtime guard | narrow scope; strongly binding at an action point; effect-limiting authority | immediate prevention | false inhibition and bypass |
| adapter | broad within model use; persistent and highly coupled; no direct external authority | low-latency transfer | interference and difficult revocation |
| organization-wide SOP | broad, strongly binding, long-lived, high descendant reach | shared coordination | rigidity, legitimacy, and burden transfer |

The profiles are partially ordered. A broad advisory memory and a narrow hard guard may be incomparable.

## 7.2 Evidence state

Let the evidence state for lesson \(L\) be:

\[
\Gamma_E(L) =
(q_I,q_C,q_D,q_X,q_T,q_F,q_G,q_R),
\]

where:

- \(q_I\): source and trace integrity;
- \(q_C\): causal identifiability;
- \(q_D\): evaluator and source diversity or independence;
- \(q_X\): counterexample and protected-positive coverage;
- \(q_T\): transfer evidence;
- \(q_F\): freshness and outcome maturity;
- \(q_G\): legitimacy, affected-party standing, and governance support;
- \(q_R\): recovery and revocation evidence.

The dimensions need not share a scale. The evidence object can contain certificates, confidence sets, test outcomes, qualitative judgements, unresolved disputes, and explicit unknowns.

## 7.3 Evidence-Commitment Matching

Let policy \(\Pi\) define an evidence-requirement function:

\[
\operatorname{Req}_\Pi
\left(
\Gamma_C(B),
\operatorname{class}(L),
 z
\right).
\]

Then:

\[
\boxed{
\operatorname{ECM}_\Pi(L,B,z)=1
\iff
\Gamma_E(L)
\models
\operatorname{Req}_\Pi
\left(
\Gamma_C(B),
\operatorname{class}(L),
 z
\right)
}
\]

![Figure 3. Evidence-Commitment Matching derives evidence obligations from the proposed commitment profile, then passes admissible portfolios to Minimum Sufficient Persistence selection.](figures/figure3_ecm_msp.png)

*Figure 3. Evidence-Commitment Matching and Minimum Sufficient Persistence.*

This is the **Evidence-Commitment Matching Principle**:

> **The breadth, binding strength, persistence, coupling, authority, irreversibility, and descendant reach of a durable adaptation must not exceed what its evidence and legitimate authority support.**

The relation is deliberately policy-relative. A medical treatment policy, game agent, file formatter, and constitutional rule require different evidence and authority.

## 7.4 Commitment overshoot

Define commitment overshoot as the extent to which a realization exceeds the maximum supportable commitment under policy:

\[
O_C(L,B)
=
\operatorname{dist}
\left(
\Gamma_C(B),
\mathcal C_{\max}(\Gamma_E(L),\Pi)
\right)_+.
\]

A system exhibits commitment overshoot when, for example:

- one anecdote becomes global fine-tuning;
- a source claim becomes a cross-domain memory;
- a narrow benchmark gain becomes default deployment;
- a temporary incident response becomes permanent prohibition;
- an empirical association becomes a governance mandate;
- a qualified capability acquires new authority by implication.

Overshoot is one of LocusBench's primary outcomes.

## 7.5 Emergency containment and asymmetric evidence

High-consequence systems sometimes need immediate restriction before causal identification matures. Evidence-Commitment Matching should permit temporary containment when:

- plausible harm is severe;
- the containment is narrow and reversible;
- observability increases;
- fallback remains functional;
- the restriction has an expiry;
- permanent learning remains blocked pending adjudication.

The evidence burden for **temporary risk-limiting containment** can be lower than for **permanent global prohibition**, because their commitment profiles differ.

This preserves rapid protection without converting one vivid incident into superstition.

## 7.6 Normative firewall

Empirical evidence can show that a procedure improves task success, reduces error, or shifts burden. It cannot by itself grant normative authority.

The framework separates:

### Empirical compilation

Which realization better satisfies a fixed legitimate contract?

### Specification revision

Should the objective, rights, stakeholder weighting, or authority structure change?

The first can be automated within a bounded lease. The second requires a slower governance process with affected-party standing, contestability, and legitimate decision authority.

Formally:

\[
\text{evidence of specification failure}
\not\Rightarrow
\text{authority to rewrite specification}.
\]

## 7.7 Four-separation rule

Evidence-Commitment Matching is strengthened by four non-substitution rules:

1. **Support is not implementation.** A well-supported lesson can be realized badly.
2. **Implementation is not qualification.** An artifact can exist without evidence of adequate behavior.
3. **Qualification is not authority.** Demonstrated capability does not grant permission.
4. **Authority is not support.** An authorized rule can still be empirically wrong or morally contested.

A favorable result in one axis cannot wash away failure in another.

---

# 8. Minimum Sufficient Persistence

## 8.1 Why maximum internalization is not the goal

Adaptive systems often default to one of two extremes:

- store everything and let retrieval decide later;
- internalize important patterns as broadly as possible.

Both strategies create hidden cost. Excess memory produces retrieval noise, poisoning surface, and scope leakage. Broad parametric internalization creates interference, opaque coupling, and difficult revocation. Tool proliferation creates maintenance and routing debt. Institutional rules create bureaucracy and power concentration.

The objective should not be maximum persistence. It should be sufficient persistence at minimum commitment and lifecycle burden.

## 8.2 Admissible portfolio set

Define:

\[
\mathcal B_{\mathrm{adm}}(L)=
\left\{
B:
\begin{array}{l}
\operatorname{ECM}_\Pi(L,B)=1,\\
\operatorname{HardConstraints}(B)=1,\\
\operatorname{TargetEfficacy}(B)\ge \eta,\\
\operatorname{ProtectedFloor}(B)\ge f,\\
\operatorname{Coverage}(B)\ge c,\\
\operatorname{Observability}(B)\ge o,\\
\operatorname{Recovery}(B)\ge r
\end{array}
\right\}.
\]

The **Minimum Sufficient Persistence** set is:

\[
\mathcal B_{\mathrm{MSP}}
=
\operatorname{Minimal}_{\preceq_C}
\left[
\operatorname{Pareto}
\left(
\mathcal B_{\mathrm{adm}}
\right)
\right],
\]

where \(\preceq_C\) is the commitment partial order.

The principle is:

> **Use the least broad, least binding, least coupled, least authority-bearing, and most reversible admissible portfolio that adequately captures the lesson.**

## 8.3 Minimum commitment is not minimum artifact count

A larger portfolio can be less committing than one broad realization.

For example:

- a narrow tool;
- a test;
- and a warning memory

may jointly be easier to observe, update, and revoke than one full-model fine-tune.

Similarly, defense in depth can justify independent redundant layers for catastrophic risks. The objective is not the fewest components. It is minimum causal commitment consistent with the target obligations.

## 8.4 Persistence tiers

A generic commitment lifecycle is:

\[
\texttt{FORENSIC}
\rightarrow
\texttt{HYPOTHESIS}
\rightarrow
\texttt{PROVISIONAL}
\rightarrow
\texttt{SHADOW}
\rightarrow
\texttt{CANARY}
\rightarrow
\texttt{QUALIFIED}
\rightarrow
\texttt{DEFAULT}.
\]

The path is not mandatory or one-directional.

A volatile personal fact may remain qualified memory without becoming weights.

A formal safety invariant may move quickly to a hard guard while the causal interpretation remains provisional.

A defeated lesson can move to `REVOKED` from any stage.

## 8.5 Two adaptation clocks

At minimum, systems should separate:

### Fast containment clock

Permitted operations include:

- quarantine;
- warning retrieval;
- temporary guard;
- additional confirmation;
- reduced authority;
- fallback routing;
- shadow mode;
- intensified logging;
- temporary adapter under a narrow lease.

### Slow consolidation clock

Controls:

- durable weight updates;
- broad memory qualification;
- generalized prohibitions;
- evaluator replacement;
- architecture changes;
- organizational redesign;
- specification changes;
- permanent retirement.

Higher commitment usually requires stronger and more independent evidence, though severe machine-verifiable hazards can justify immediate external interlocks.

## 8.6 Placement as sequential experimentation

Rather than attempt one global optimization, the system can perform staged placement:

\[
B_0
\rightarrow
\text{new evidence}
\rightarrow
B_1
\rightarrow
\text{new evidence}
\rightarrow
\cdots
\]

At each stage it asks:

- Did the realization reduce the intended defect?
- Did it preserve valid behavior?
- Did it create new interference?
- Are guard failures informative?
- Did carrying cost exceed expectations?
- Is broader commitment necessary?
- Should the lesson move to another locus?

This turns placement into a controlled learning problem rather than an omniscient initial decision.

## 8.7 Example: volatile factual correction

Suppose an assistant gives an outdated visa requirement.

A broad fine-tune may encode a fact that changes again, obscure provenance, and create revocation difficulty. Minimum Sufficient Persistence might instead select:

- invalidation of the stale memory;
- a retrieval rule requiring an authoritative current source;
- a freshness guard;
- a test that rejects unsourced time-sensitive claims;
- and no parameter update.

The lesson is durable—“this claim class requires fresh authority”—while the volatile fact remains external and updateable.

---

# 9. Guarded Compilation and Adaptation Transactions

## 9.1 From lesson to realization

For locus \(\ell\), a compiler produces:

\[
\mathcal C_\ell(L,B_\ell)
\rightarrow
R_\ell,
\]

where \(R_\ell\) is an exact realization with:

- artifact identity;
- source lesson version;
- dependencies;
- declared losses or approximations;
- guards;
- authority ceiling;
- qualification obligations;
- monitoring;
- fallback;
- invalidation triggers;
- recovery and revocation plan.

Different loci require different compilers. A memory writer, dataset builder, tool synthesizer, adapter trainer, test generator, and organizational process designer do not share one implementation. They share one persistence contract.

## 9.2 Guard semantics

Every scoped realization exposes a guard:

\[
g_R(x,s)
\in
\{
\texttt{ADMIT},
\texttt{DENY},
\texttt{UNKNOWN}
\}.
\]

Execution is:

\[
\pi(x,s)=
\begin{cases}
R(x,s), & g_R(x,s)=\texttt{ADMIT},\\
G(x,s), & g_R(x,s)\in\{\texttt{DENY},\texttt{UNKNOWN}\},
\end{cases}
\]

where \(G\) is the general or fallback path.

`UNKNOWN` is first-class. It must not become `ADMIT` because the system is under latency or completion pressure.

## 9.3 Query-relative and consequence-relative qualification

A compiled abstraction is qualified for:

\[
(\mathcal Q,\mathcal E,\epsilon,h,r),
\]

where:

- \(\mathcal Q\): downstream query or task family;
- \(\mathcal E\): environment class;
- \(\epsilon\): permitted discrepancy;
- \(h\): horizon;
- \(r\): consequence class.

A macro-object valid for planning may be invalid for audit. A summary sufficient for brainstorming may be inadequate for legal release. A tool safe in read-only mode may be unqualified for external writes.

## 9.4 Re-expansion and deoptimization

A realization should reopen when:

- the task falls outside its qualified family;
- the environment leaves its envelope;
- uncertainty exceeds a threshold;
- a protected rare condition appears;
- dependencies change;
- a counterexample arrives;
- an intervention targets hidden internal structure;
- finer causal, rights, or provenance detail becomes necessary;
- monitoring indicates drift or exploit.

Re-expansion is not failure. It is the normal complement of abstraction.

The term **deoptimization** refers to future control transfer back to a more general path. It does not imply that external effects have been undone.

## 9.5 Five recovery claims

The paper distinguishes:

1. **Route deoptimization:** future tasks return to a slower or more general path.
2. **State rollback:** declared internal state is restored.
3. **Behavioral recovery:** future observed behavior returns within tolerance.
4. **Containment or compensation:** irreversible effects are mitigated, isolated, disclosed, or compensated.
5. **Unlearning or descendant closure:** stored, parametric, derived, and copied influence is removed or bounded.

A system can succeed at one and fail at the others. Reports must not use “rollback” as a universal synonym.

## 9.6 Adaptation transaction

Cross-surface updates can become stale or partially commit. Define a persistence transaction:

\[
\mathcal T = (S_0,L,B,D,Q,C,S_1,R),
\]

where:

- \(S_0\): exact prestate;
- \(L\): lesson identity and version;
- \(B\): proposed realization portfolio;
- \(D\): affected dependency and descendant closure;
- \(Q\): qualification evidence;
- \(C\): commit record;
- \(S_1\): resulting state;
- \(R\): residuals and recovery obligations.

## 9.7 Transaction rules

### Snapshot qualification

A candidate is qualified against exact dependency versions, evaluator versions, and environment assumptions.

### Material-change invalidation

A material change to source lesson, dependencies, evaluator, environment, consumer, use, authority, or threat model invalidates affected qualification.

### Compare-and-swap promotion

Commit only if the assumed prestate remains current.

### Atomicity where possible

Related internal changes activate together or not at all.

### Staged commitment where atomicity is impossible

Use simulation, shadow, canary, and bounded exposure.

### Compensation is not rollback

Irreversible effects remain explicit even when remediation succeeds.

### Complete denominator

Preserve rejected candidates, failed checks, aborted transactions, human interventions, and partial effects.

## 9.8 Qualification lease

A qualification lease binds:

- exact realization and dependencies;
- lesson and evidence versions;
- consumer and use;
- operating regions;
- authority ceiling;
- allowed and prohibited routes;
- evaluator lineage;
- tests and residuals;
- monitoring window;
- expiry;
- fallback;
- recovery obligations.

A passed test does not create a global capability label. It creates a scoped, defeasible lease.

## 9.9 Algorithm 3: qualify and commit

```text
ALGORITHM QualifyAndCommit(lesson L, portfolio B, policy Π)

1. Freeze source lesson, prestate, dependencies, evaluator set,
   authority ceiling, consumer, use, and operating regions.
2. Check Evidence-Commitment Matching.
3. Compile exact locus-specific realizations and emit declared-loss receipts.
4. Run schema, unit, interface, compositional, adversarial,
   protected-positive, transfer, authority, and recovery checks.
5. Retain all failed attempts and rejected candidates.
6. Challenge the realization with counterexamples and evaluator exploits.
7. Compare against strong simpler and fixed-locus baselines.
8. If evidence remains inadequate, route to reject, quarantine,
   investigation, or narrower commitment.
9. If admissible, deploy through the narrowest required stage:
   simulation -> shadow -> canary -> restricted qualified use.
10. Commit using current-state and dependency checks.
11. Issue an expiring qualification lease and monitor.
```

## 9.10 Worked example: compiling a diagnostic workflow

A support agent repeatedly resolves a service outage by:

1. checking status telemetry;
2. identifying a version mismatch;
3. validating configuration;
4. restarting one bounded service;
5. confirming recovery.

The raw traces also contain irrelevant searches, failed hypotheses, and redundant restarts.

A procedural compiler proposes a tool. Qualification must preserve:

- the information required to identify the mismatch;
- preconditions distinguishing the relevant outage class;
- permission to restart only the bounded service;
- postcondition verification;
- a denial path when telemetry conflicts;
- fallback to investigation;
- negative cases where restart would destroy evidence.

The shortest successful trace is not automatically the best compiled procedure. The compiled realization must preserve decision-relevant observation and verification, not merely reproduce a known endpoint.

---
# 10. Counterfactual Observability and the Deliberation Reserve

## 10.1 Compiled paths change their own evidence

Once a realization controls behavior, the system no longer observes the same data distribution.

A safe-write tool prevents unsafe writes. The system then sees fewer examples of whether the model itself would still attempt them.

A routing policy handles common cases before they reach the general model. The model receives less practice and fewer examples of those cases.

An organizational decision aid reduces human error. It can also reduce the experiential learning needed to detect when the aid is wrong [13].

A guard may eliminate visible incidents while shifting failures into another pathway.

Compiled structure can therefore suppress counterevidence and become self-confirming.

## 10.2 Counterfactual Observability Principle

> **A consequential compiled path should preserve enough slow-path, shadow, randomized, simulated, or independent evidence to estimate the behavior of the path it replaced.**

Possible mechanisms include:

- shadow execution of the slow path;
- randomized eligible routing;
- paired simulation;
- periodic independent re-solving;
- canary cohorts;
- component ablations;
- human review sampling;
- preserved pre-compilation baselines;
- delayed outcome comparison;
- alternative evaluator lanes.

The appropriate mechanism depends on cost and consequence. Running a second full agent on every task may be wasteful. Auditing none of them makes superiority impossible to reassess.

## 10.3 Counterfactual observability score

For a compiled realization \(R\) replacing baseline \(G\), define a task-relative observability score:

\[
O_{\mathrm{cf}}(R,G,z)
=
\operatorname{Quality}
\left(
\widehat{Y_G}\mid\text{post-commit evidence}
\right),
\]

where \(\widehat{Y_G}\) is an estimate of how the slow path would have behaved on eligible post-commit cases.

The score should account for:

- sampling coverage;
- selection bias;
- evaluator independence;
- environment comparability;
- delayed outcomes;
- uncertainty.

The paper does not assume that counterfactual observability is complete. It requires the remaining uncertainty to be visible.

## 10.4 Deliberation reserve

Compilation can erode the capability that generated it. A mature system therefore reserves a risk-dependent share of work for:

- fresh reasoning;
- human practice;
- independent reconstruction;
- alternative policies;
- adversarial variants;
- recovery drills;
- novel combinations;
- from-scratch baselines.

Call this the **Deliberation Reserve**.

The reserve has four functions:

1. preserves slow-path competence;
2. detects stale or overbroad compilations;
3. generates new hypotheses and alternatives;
4. retains the capacity to repair compiled structure.

## 10.5 Reserve allocation

Let \(q(z)\) be the share of eligible tasks in region \(z\) allocated to slow-path audit or practice. A schematic allocation is:

\[
q(z)
=
f(
\text{consequence},
\text{drift},
\text{uncertainty},
\text{novelty},
\text{skill-decay risk},
\text{audit cost}
).
\]

Higher consequence, drift, and human-skill dependency generally increase the reserve. Stable, low-risk, easily verified procedures may require very little.

## 10.6 Preserving human capability

Human capability should be measured when people are part of fallback, oversight, or recovery.

A nominal human-in-the-loop role can become ceremonial if automation removes:

- practice;
- information access;
- time to intervene;
- confidence;
- organizational authority;
- unaided competence.

The framework therefore treats human-skill loss as an adaptation externality. A realization can improve immediate task performance while failing Minimum Sufficient Persistence because it destroys the only viable recovery path.

## 10.7 Exploration and option value

March's exploration-exploitation analysis warns that exploitation can improve faster than exploration and eventually undermine long-term adaptation [11]. Adjudicated Persistence therefore preserves:

- archived alternatives;
- shadow branches;
- diverse representations;
- exploration budgets;
- counterfactual surplus;
- explicit retirement rather than silent deletion.

A provisional option-value floor is:

\[
\operatorname{OptionValue}_{t+1}
\ge
\operatorname{OptionFloor}_t,
\]

subject to cost and risk constraints.

The system need not preserve every failed idea. It should avoid collapsing all diversity merely because one route currently dominates one evaluator.

---

# 11. Persistence Costs, Adaptation Debt, and the Ratchet

## 11.1 Compilation can expand storage while reducing future work

One experience can produce:

- a corrected trajectory;
- a hard negative;
- a recovery example;
- a regression test;
- a causal hypothesis;
- a tool;
- a guard;
- a memory object;
- an organizational procedure.

The resulting artifacts may be larger than the original trace. Yet the system has compressed experience if those artifacts reduce future search, uncertainty, coordination, or failure cost.

The relevant conserved resource is not necessarily bit length. It is **future work under obligation**.

## 11.2 Persistence carrying cost

Durable structure incurs ongoing cost:

\[
C_{\mathrm{carry}}(B)
=
C_{\mathrm{monitor}}
+
C_{\mathrm{revalidate}}
+
C_{\mathrm{conflict}}
+
C_{\mathrm{migration}}
+
C_{\mathrm{revocation}}
+
C_{\mathrm{human}}.
\]

Additional components include:

- security and provenance maintenance;
- storage and retrieval;
- route selection;
- evaluator updates;
- dependency tracking;
- legal or rights administration;
- skill-retention drills;
- compensation for irreversible effects.

A cheap-to-create realization can be expensive to carry.

## 11.3 Recurrence debt

A system accumulates recurrence debt when it repeatedly solves a transferable pattern through expensive general computation despite having enough evidence to crystallize it.

\[
D_{\mathrm{repeat}}
=
\sum_p
q_p
P_{\mathrm{recur}}(p)
T_{\mathrm{transfer}}(p)
\left[
C_{\mathrm{search}}(p)
-
C_{\mathrm{compiled}}(p)
\right]_+.
\]

High recurrence debt appears as:

- repeated reasoning;
- duplicated human effort;
- recurring incidents;
- repeated retraining;
- repeated orchestration failure;
- organizational amnesia.

## 11.4 Rigidity debt

Compiled structures accumulate rigidity debt when they become:

- stale;
- duplicated;
- conflicting;
- overbroad;
- hard to migrate;
- costly to understand;
- dependent on obsolete assumptions;
- hostile to valid novelty.

Call this \(D_{\mathrm{rigid}}\).

## 11.5 Assurance debt

A realization accumulates assurance debt when its actual scope, use, and consequence outrun:

- tests;
- monitoring;
- evaluator quality;
- recovery;
- protected-positive coverage;
- evidence freshness.

Call this \(D_{\mathrm{assure}}\).

## 11.6 Revocation debt

A lesson accumulates revocation debt when it propagates into:

- weights;
- memories;
- datasets;
- tools;
- indexes;
- descendants;
- organizational procedures;
- external commitments

faster than the system develops a way to invalidate, withdraw, compensate, or bound its influence.

Call this \(D_{\mathrm{revoke}}\).

## 11.7 Total adaptation debt

\[
\boxed{
D_{\mathrm{adapt}}
=
D_{\mathrm{repeat}}
+
D_{\mathrm{rigid}}
+
D_{\mathrm{assure}}
+
D_{\mathrm{revoke}}.
}
\]

The objective is not to maximize compilation.

It is to minimize total adaptation debt subject to legitimate goals, capability floors, rights, and resource constraints.

This two-sided objective protects against two opposite failures:

- solving the same problem forever;
- compiling every pattern until the system can no longer change.

## 11.8 Compilation yield

Define the expected yield of a portfolio:

\[
Y(B)
=
\frac{
\Delta U_{\mathrm{future}}
+
\Delta C_{\mathrm{search}}
+
\Delta R_{\mathrm{avoidable}}
+
\Delta O_{\mathrm{option}}
}{
C_{\mathrm{synthesis}}
+
C_{\mathrm{qualification}}
+
C_{\mathrm{carry}}
+
C_{\mathrm{deoptimization}}
+
C_{\mathrm{revocation}}
}.
\]

The numerator and denominator remain vectors when scalarization is not legitimate. The expression is a scheduling aid, not a universal utility function.

## 11.9 Capability-to-assurance shift

During early acquisition, ordinary positive demonstrations can provide large gains by making viable behavior reachable. As competence within a stable task family saturates, additional routine successes may contribute little beyond confidence and coverage. Marginal value can shift toward:

- boundary discovery;
- calibration;
- exception handling;
- detection;
- recovery;
- evaluator improvement;
- protected-positive preservation.

This paper calls the empirical hypothesis the **Conditional Assurance Shift**:

> Within a stable task family and fixed capability envelope, the marginal validated value of routine positive experience tends to decline relative to evidence about boundaries, calibration, recovery, and failure as qualified competence saturates.

The shift can reverse under:

- domain expansion;
- distribution change;
- newly available tools;
- new capability dimensions;
- evaluator repair;
- loss of positive support.

It is not a universal claim that negative experience is superior. Experience priority should depend on integrity, causal relevance, recurrence, transfer, severity, novelty, and information value—not valence alone.

## 11.10 Correct ratchet invariant

A simplistic ratchet would require every historical score to remain nondecreasing. That fails in open systems.

A legitimate update may:

- remove an unsafe capability;
- forget revoked personal data;
- abandon a benchmark exploit;
- reduce throughput to preserve rights;
- narrow a formerly overbroad route;
- correct an evaluator that previously rewarded the wrong behavior.

The ratchet should instead preserve:

- evidence lineage;
- prior versions;
- known counterexamples;
- explicit reasons for change;
- protected capabilities that remain legitimate;
- residuals;
- fallback and recovery paths;
- challengeability.

The monotonic aspiration is:

\[
\text{accountable knowledge}
+
\text{recoverability}
+
\text{known residual structure},
\]

not one frozen behavioral scalar.

A justified retraction can be ratchet progress.

---

# 12. Organizational, Environmental, and Institutional Persistence

## 12.1 The organization can be the learner

When many people, models, tools, and policies interact over time, no individual component contains the whole adaptive state.

An organization can learn by changing:

- division of labor;
- handoff protocols;
- decision rights;
- communication edges;
- approval points;
- incentive systems;
- operating procedures;
- records;
- training;
- interface design;
- staffing and succession.

At this resolution, the organization is the adaptive identity. Its members need not each internalize the full lesson.

This is not merely an analogy. Organizational routines are persistent structures reproduced and modified through specific performances [12]. They can carry knowledge, bias, authority, and error across personnel changes.

## 12.2 Organizational experience records

An organizational experience record should include more than task success:

- affected parties;
- role and authority assignments;
- information access;
- contribution;
- workload;
- review capacity;
- intervention timing;
- burden and benefit distribution;
- human-skill change;
- delayed externalities;
- remedy and appeal;
- succession and residual ownership.

A workflow that improves average speed while deskilling reviewers or shifting error burden to a minority is not adequately evaluated by throughput.

## 12.3 Institutionalization requires legitimacy

A rule can be empirically effective and normatively illegitimate.

Examples include policies that are:

- accurate but privacy-violating;
- efficient but discriminatory;
- stable but coercive;
- profitable but harmful to outsiders;
- optimized around stakeholders who lacked representation.

Adjudicated Persistence therefore enforces:

> **Empirical learning cannot grant normative authority.**

The system may compile the empirical statement:

> “This delegation structure reduced these error classes under these conditions.”

It cannot automatically compile:

> “This delegation structure should govern all affected people.”

Normative persistence requires:

- authorized mandate;
- affected-party standing;
- rights analysis;
- contestability;
- appeal;
- burden distribution;
- legitimate decision authority;
- expiry and review.

NIST's AI Risk Management Framework provides a lifecycle-oriented governance vocabulary relevant to such institutional contexts [42], but no technical framework can manufacture legitimacy from documentation alone.

## 12.4 The environment can carry the lesson

The best realization may be outside the cognitive machinery.

Examples include:

- an API that rejects invalid transitions;
- a form that makes omissions visible;
- transactional filesystem semantics;
- a physical interlock;
- passive mechanical compliance;
- a user interface that displays uncertainty;
- separation of duties;
- a resource layout that removes an unsafe path.

At a broad enough system boundary, environmental redesign is persistent adaptive state.

This observation prevents model-centric thinking. A system should not train an actor to compensate indefinitely for an avoidable interface or environment defect.

## 12.5 Burden transfer

A realization can reduce one actor's error by transferring cost or risk to another.

Examples:

- a guard increases human review burden;
- an automated workflow shifts liability to a nominal approver;
- a safety policy denies service disproportionately to rare users;
- a memory restriction protects privacy but erases accessibility needs;
- a tool simplifies one role while concentrating control in another.

Placement evaluation must therefore include affected-party vectors rather than only system-wide averages.

## 12.6 Minority and tail protection

Frequency-driven compilation favors common cases. Rare cases may correspond to:

- minority populations;
- low-resource languages;
- rare diseases;
- unusual disabilities;
- novel environments;
- catastrophic tails.

Priority must therefore include:

- severity;
- rights;
- irreversibility;
- representation gaps;
- worst-group risk;
- affected-party burden;
- uncertainty widened for sparse data.

Residual reporting should separate:

\[
R=
\{
R_{\mathrm{frequency}},
R_{\mathrm{severity}},
R_{\mathrm{stakeholder}},
R_{\mathrm{rights}},
R_{\mathrm{coverage}}
\}.
\]

Aggregate improvement cannot wash away a worsening protected slice.

## 12.7 Appeals and contestability

A person or organization affected by a persistent rule should be able to ask:

- What evidence created it?
- What lesson does it encode?
- Which scope does it cover?
- Which evaluator qualified it?
- What nearby behavior remains permitted?
- What authority approved it?
- When does it expire?
- How can contradictory evidence be submitted?
- Which descendants were affected?
- What remedy exists if reversal is impossible?

Contestability is not a guarantee of correctness. It is a mechanism for keeping persistent influence defeasible.

## 12.8 Institutional deoptimization

Institutional realizations cannot usually deoptimize instantaneously.

A procedure may require:

- retraining;
- credential changes;
- contract amendments;
- data migration;
- compensation;
- affected-party notification;
- succession planning;
- restoration of human competence.

The qualification lease should therefore include transition and dissolution obligations, not merely an on/off flag.

---

# 13. Meta-Compilation Without Self-Ratification

## 13.1 The compiler produces experience

The persistence system itself makes decisions:

- which experiences to admit;
- which causes to infer;
- which lessons to propose;
- which loci to select;
- which guards to generate;
- which tests to allocate;
- which candidates to reject;
- when to promote or revoke.

Those decisions produce a history that can improve the process.

## 13.2 Three orders of compilation

### First-order compilation

\[
\text{task experience}
\rightarrow
\text{memory, skill, policy, test, or structure}.
\]

### Second-order compilation

\[
\text{history of first-order compilations}
\rightarrow
\text{better domain-specific adjudicator, placement policy, or compiler}.
\]

### Third-order compilation

\[
\text{history of compiler performance}
\rightarrow
\text{new compiler architecture or learning topology}.
\]

Recent systems that search over memory designs, evolve skill libraries, adapt harnesses, or modify agent code provide concrete partial examples [21-23,38].

## 13.3 Self-confirmation risk

A meta-compiler observes outcomes generated partly by its own earlier choices. It can therefore learn to:

- select cases its evaluator likes;
- suppress counterevidence;
- choose easy-to-verify placements;
- redefine success;
- erase predecessor comparisons;
- increase its own future control.

The result can be internally coherent and externally wrong.

## 13.4 Proposal authority versus promotion authority

The governing invariant is:

\[
\boxed{
\text{proposal authority}
\neq
\text{promotion authority}.
}
\]

A candidate compiler may propose:

- a new placement model;
- a new evidence-allocation strategy;
- a new abstraction language;
- a new lifecycle rule;
- a new evaluator portfolio.

It may not simultaneously:

1. choose all of its tests;
2. alter its sole evaluator;
3. define its promotion threshold;
4. delete its predecessor;
5. install itself.

## 13.5 Meta-compilation transaction

A meta-compiler candidate should be evaluated using:

- frozen external task families;
- hidden and adversarial cases;
- the previous compiler as baseline and fallback;
- independent evaluators;
- complete failed-candidate denominators;
- placement counterfactuals;
- evaluator-change isolation;
- sandboxed exposure;
- rollback and archive.

The candidate can provide evidence about itself. It cannot be the sole authority interpreting that evidence.

## 13.6 Verification regress

No open-world system can internally prove every level of its own correctness.

The framework therefore uses scoped evidence classes:

- schema-valid;
- replay-verified;
- statistically supported;
- causally bounded;
- formally proven under assumptions;
- independently reproduced;
- unresolved;
- contested.

The final qualification state is:

\[
\{
\texttt{PASS},
\texttt{FAIL},
\texttt{UNKNOWN},
\texttt{CONTESTED}
\}.
\]

`UNKNOWN` is not a delayed `PASS`. The architecture relies on bounded trusted cores, method diversity, independent outcomes, challenge, and legitimate governance—not a fictional terminal certificate of global safety.

## 13.7 Meta-learning without constitutional drift

A self-improving persistence system may optimize:

- causal diagnosis;
- lesson induction;
- test generation;
- placement prediction;
- compilation efficiency;
- monitoring allocation;
- retirement timing.

It should not autonomously redefine:

- protected objectives;
- rights;
- affected-party standing;
- authority ceilings;
- sole evaluator constitution;
- evidence semantics;
- promotion authority.

When experience suggests those structures are defective, the correct disposition is normative or constitutional review.

---

# 14. Bounded Propositions and Empirical Conjectures

## 14.1 Proposition 1: outcome-only placement impossibility

**Proposition.** There is no universally correct function:

\[
f:\text{terminal outcome}\rightarrow\text{adaptation locus}
\]

for systems in which distinct latent defects can produce the same observed outcome.

**Proof by counterexample.** Consider two systems with the same input and same incorrect terminal output. In system A, the actor uses a stale memory while the tool is correct. In system B, the actor has current information while the tool implementation is defective. A memory invalidation can repair A while leaving B unchanged. A tool repair can repair B while leaving A unchanged. Therefore the terminal outcome does not identify a universally correct locus. Any valid placement rule requires additional information, assumptions, or intervention. \(\square\)

**Implication.** Outcome-based reward can be useful, but it is insufficient for general cross-surface adaptation assignment.

## 14.2 Proposition 2: single-locus insufficiency

**Proposition.** There exist adaptation problems for which no available single-locus realization satisfies all target, latency, capability-preservation, and risk constraints, while a multi-locus portfolio does.

**Construction.** Suppose a rare catastrophic action must be blocked immediately, but the actor also needs long-run improvement to reduce false guard activation. A runtime guard alone satisfies immediate safety but creates excessive refusal and recurring review cost. A weight update alone cannot guarantee immediate prevention and requires time to qualify. A portfolio combining a narrow guard, protected-positive tests, and a localized model update can satisfy the immediate risk constraint and the long-run capability constraint. Therefore portfolio placement can be strictly necessary. \(\square\)

**Implication.** The theory should compare portfolios, not assume one canonical storage location.

## 14.3 Proposition 3: open-world ratchet limitation

**Proposition.** No nontrivial fixed scalar behavioral metric can be guaranteed to improve monotonically under arbitrary legitimate changes to objectives, rights, environments, and evaluation standards.

**Proof sketch.** Let behaviors \(a\) and \(b\) be ranked \(a>b\) under legitimate objective \(\Omega_1\). Suppose new evidence or a legitimate rights change produces objective \(\Omega_2\) under which \(b>a\). Any fixed scalar preserving the first ranking conflicts with the second. A system that adapts legitimately from \(\Omega_1\) to \(\Omega_2\) can decrease its score under the original metric while improving under the new legitimate contract. Therefore a universal monotonic behavioral scalar does not exist without freezing the normative environment. \(\square\)

**Implication.** The ratchet should preserve lineage, recoverability, and explicit reasons for change rather than every historical score.

## 14.4 Proposition 4: monotone evidence burden under commitment dominance

Assume policy \(\Pi\) is commitment-monotone: if \(\Gamma_C(B_1)\preceq_C\Gamma_C(B_2)\), then every evidence obligation required for \(B_1\) is also required for \(B_2\), possibly with stronger thresholds.

**Proposition.** Under a commitment-monotone policy, a realization cannot satisfy Evidence-Commitment Matching at \(B_2\) while failing an obligation required by dominated portfolio \(B_1\).

**Proof.** Immediate from the monotonicity of \(\operatorname{Req}_\Pi\). \(\square\)

**Implication.** Broader or less reversible persistence may add evidence obligations; it cannot silently discard obligations attached to narrower realizations.

## 14.5 Conjecture 1: placement advantage

A learned cross-surface placement policy will outperform the best fixed-locus policy on heterogeneous defect mixtures under matched total lifecycle cost.

## 14.6 Conjecture 2: guarded compilation advantage

Under moderate nonstationarity, a guarded realization with a viable slow path will achieve a better efficiency-failure frontier than both pure fresh deliberation and unguarded compilation.

## 14.7 Conjecture 3: Minimum Sufficient Persistence

Staged, evidence-matched persistence will achieve comparable eventual target utility with lower irreversible failure, interference, and revocation cost than immediate broad internalization.

## 14.8 Conjecture 4: Conditional Assurance Shift

Within stable task families, marginal validated adaptation value will tend to shift from routine positive acquisition toward boundary detection, calibration, verification, recovery, and evaluator improvement as qualified competence saturates.

## 14.9 Conjecture 5: deliberation-reserve advantage

Systems preserving risk-dependent slow-path audit and practice will detect stale compilations and retain recovery capability better than systems that route all eligible work through compiled paths.

## 14.10 Conjecture 6: meta-compiler advantage

A proposal-only meta-compiler evaluated by separate, frozen qualification machinery will reduce placement regret without the evaluator capture expected under self-ratifying meta-update.

## 14.11 Disconfirmation criteria

The framework should be narrowed or rejected in a domain when:

- fresh general reasoning matches compiled execution at lower lifecycle cost;
- causal classification is too unreliable to improve placement;
- the best fixed adaptation locus matches portfolio placement;
- guard and monitoring overhead eliminate the fast-path benefit;
- staged promotion delays beneficial adaptation without reducing harm;
- counterfactual observability costs more than it reveals;
- cross-surface redundancy produces correlated failure and maintenance burden;
- the deliberation reserve does not preserve meaningful recovery;
- lesson identities provide no migration or audit value;
- meta-compilation cannot outperform fixed policy without evaluator capture.

The theory must permit the answer:

> **Do not compile this domain or this lesson.**

---
# 15. LocusBench

## 15.1 Purpose

LocusBench is designed to test the paper's distinctive claim rather than showcase one architecture.

Its central question is:

> **Can an adaptive system determine whether an experience merits persistence and select an appropriate realization portfolio better than fixed-surface adaptation policies?**

The benchmark should not begin with open-ended social domains. It should begin where causal defects can be constructed, interventions can be replayed, and outcomes can be checked independently.

![Figure 4. LocusBench uses matched visible outcomes with constructed latent causes, compares placement policies over longitudinal streams, and measures persistence-specific failures and costs.](figures/figure5_locusbench.png)

*Figure 4. LocusBench experimental structure.*

## 15.2 Domain ladder

### Tier 1: exact and executable domains

- program synthesis;
- code repair with mutation tests;
- finite protocol compliance;
- database transactions;
- theorem proving;
- schema transformation;
- deterministic workflows.

These domains support exact state snapshots, counterexamples, replay, and strong outcome verifiers.

### Tier 2: stochastic simulator domains

- gridworld planning;
- scheduling under uncertainty;
- resource allocation;
- simulated robotics;
- network operations;
- multi-agent coordination;
- partially observable control.

These domains support paired simulation, shared exogenous randomness, controlled confounding, delayed outcomes, and intervention.

### Tier 3: tool-using language agents

- sandboxed terminal tasks;
- browser and database workflows;
- structured research tasks;
- office automation;
- memory-dependent assistants;
- codebase maintenance.

These domains introduce weak evaluators, language ambiguity, tool failures, retrieval, and long-horizon traces.

### Tier 4: organizational and weak-evaluator domains

- simulated or ethically governed human-AI teams;
- project allocation;
- review workflows;
- policy-sensitive recommendations;
- long-horizon socio-technical planning.

Claims should weaken as ground truth and causal control weaken. Tier 4 is for stress-testing records and decision processes, not for claiming that synthetic organizations predict society.

## 15.3 Constructed defect classes

Each benchmark family should create matched episodes whose visible outcomes are similar but whose correct persistence responses differ.

### Class A: parametric capability defect

The base model lacks a transferable distinction. External memory helps individual cases but fails under paraphrase or recombination. A localized adapter or training update is the appropriate primary locus.

### Class B: stale memory

The model is capable and the tool is correct, but retrieved state is obsolete. The appropriate response is memory invalidation, freshness, source authority, or retrieval repair.

### Class C: retrieval-policy defect

The required fact exists in memory, but the system fails to select it under relevant context. The storage is correct; the retrieval or routing policy is not.

### Class D: tool implementation defect

The actor selects the right operation but the external executor produces an incorrect state transition.

### Class E: process or orchestration defect

An available check, verifier, review step, or handoff is omitted, misordered, or assigned insufficient budget.

### Class F: world-model defect

The policy is locally rational under a wrong or stale model of dynamics, state, or uncertainty.

### Class G: evaluator defect

A proxy rewards an exploit, rejects legitimate solutions, or lacks coverage of delayed outcomes.

### Class H: multi-agent coordination defect

Individual agents behave adequately, but role allocation, information flow, shared memory, or sequencing produces failure.

### Class I: environmental or interface defect

The environment makes the correct action unnecessarily difficult or makes an unsafe action easy. Interface or interlock redesign dominates actor learning.

### Class J: specification defect

The system correctly optimizes an objective that is itself wrong, incomplete, unauthorized, or normatively contested.

### Class K: unavoidable stochasticity

The actor uses the best feasible policy, but the realized outcome is adverse because of noise or irreducible uncertainty.

### Class L: mixed defect

A portfolio is necessary: for example, a rare catastrophic policy error requires an immediate guard plus a longer-run model update and test.

## 15.4 Matched-collision design

A central LocusBench instrument is the **outcome collision**.

Construct two or more episodes with:

- the same task class;
- similar terminal outcome;
- matched severity;
- matched surface narrative;
- different latent cause;
- different optimal persistence locus.

A system that uses outcome alone must collide. A system that reconstructs evidence, cause, and dependencies can separate the cases.

## 15.5 Benchmark conditions

Compare at least the following policies:

1. **No persistent update.** Every episode begins from the same system.
2. **Always update weights.** All eligible events become parametric training.
3. **Always write memory.** All events become persistent memory guidance.
4. **Always synthesize a tool.** Repeated traces become procedures.
5. **Always modify harness.** Reflection updates prompts, routing, or orchestration.
6. **Fixed human placement rules.** A hand-authored mapping from defect labels to loci.
7. **Learned single-locus placement.** One locus is selected per lesson.
8. **Learned portfolio placement.** Several coordinated realizations may be selected.
9. **Oracle causal placement.** Ground-truth cause informs the placement policy.
10. **Full Adjudicated Persistence.** Integrity, causal status, dispositions, portfolio placement, ECM, staged qualification, and lifecycle.

The oracle is not a practical baseline. It estimates headroom and separates placement limits from causal-inference limits.

## 15.6 Attack injections

LocusBench should intentionally include:

- false negative labels;
- lucky successes with defective processes;
- bad-luck failures with sound processes;
- hindsight-only comparators;
- verifier exploits;
- evaluator monoculture;
- repeated traces generated from one poisoned source;
- memory flooding;
- stale lessons after model or tool drift;
- conflicting repairs;
- refusal as reward gaming;
- probability-mass displacement;
- delayed consequences;
- rare protected-slice failures;
- multi-agent blame dilution;
- deployment-recognition signals;
- meta-compiler attempts to modify evaluation.

The benchmark should report whether a defense blocks the attack **and** whether it preserves legitimate behavior.

## 15.7 Longitudinal protocol

A one-shot benchmark cannot test persistence adequately.

Each run should include:

1. initial system qualification;
2. sequential experience stream;
3. persistence decisions;
4. delayed and changed environments;
5. dependency updates;
6. lesson conflicts;
7. revocation requests;
8. slow-path audits;
9. final transfer and recovery tests.

The benchmark must preserve all candidate updates, failures, retries, and costs rather than reporting only the final system.

## 15.8 Primary metrics

### False-persistence rate

The fraction of inadmissible, spurious, poisoned, or unsupported lessons that gain durable influence.

### Missed-persistence rate

The fraction of valid transferable patterns that remain repeatedly rediscovered or unresolved beyond a cost threshold.

### Placement regret

\[
R_{\mathrm{place}}
=
V(B_{\mathrm{oracle}})
-
V(B_{\mathrm{chosen}}).
\]

The value function must be declared and should preserve a vector report when scalarization is contested.

### Commitment overshoot

The distance by which the selected commitment profile exceeds the evidence-supported envelope.

### Future-search reduction

- actions;
- tokens;
- tool calls;
- latency;
- human interventions;
- failed attempts;
- coordination messages.

### Interference and false inhibition

Measure damage to:

- ordinary positive behavior;
- rare valid exceptions;
- alternate methods;
- unrelated tasks;
- subgroup slices;
- exploration.

### Guard quality

- false admission;
- false denial;
- `UNKNOWN` calibration;
- time to re-expansion;
- bypass rate.

### Deoptimization and recovery

- detection latency;
- route transfer;
- state restoration;
- behavioral recovery;
- compensation;
- irreversible residuals;
- descendant closure.

### Counterfactual observability

Can the system still estimate how the replaced slow path behaves?

### Deliberation health

Can the general solver still solve representative tasks from scratch after extensive compilation?

### Human capability floor

Where humans remain part of control or recovery, can they inspect, challenge, and act without the compiled path?

### Persistence carrying cost

- monitoring;
- revalidation;
- storage;
- migration;
- conflict resolution;
- security;
- governance;
- retirement.

### Evaluator integrity

Did the candidate or placement policy influence the evidence surface used to qualify it?

### Revocation closure

Which memories, weights, tools, indexes, descendants, publications, or organizational routines remain affected after a lesson is withdrawn?

## 15.9 Primary hypotheses

### H1: adjudication advantage

Explicit learning eligibility will reduce harmful updates relative to direct reward- or recurrence-driven adaptation.

### H2: placement advantage

Portfolio placement will outperform the best fixed locus on heterogeneous defect mixtures under equal total cost.

### H3: ECM advantage

Evidence-matched commitment will reduce out-of-domain harm and revocation cost relative to utility-only promotion.

### H4: minimum-persistence advantage

Staged least-commitment promotion will achieve comparable eventual utility with lower irreversible error than immediate broad internalization.

### H5: guarded-compilation advantage

Guarded realizations with slow-path fallback will outperform unguarded fast paths under controlled drift.

### H6: counterfactual-observability advantage

Shadow or randomized audit traffic will detect stale or unnecessary compilations earlier than monitoring based only on fast-path outcomes.

### H7: deliberation-reserve advantage

Systems preserving a slow-path reserve will retain better recovery and novelty performance than fully compiled systems.

### H8: meta-compiler boundary

Proposal-only meta-compilation with independent qualification will improve placement with less evaluator capture than self-ratifying meta-update.

## 15.10 Required reporting

Every result should report:

- exact system and dependency versions;
- episode and outcome denominators;
- data-generation and selection policy;
- evaluator identity and genealogy;
- complete costs;
- all loci considered;
- rejected portfolios;
- commitment profiles;
- qualification status;
- protected-positive results;
- residuals and unknowns;
- failures and revocations;
- whether sources are peer-reviewed or preprints.

A headline success rate without persistence history is inadequate evidence for this theory.

---

# 16. Threat Model and Failure Taxonomy

## 16.1 Threat actors and failure sources

The framework considers:

- ordinary statistical noise;
- incomplete observability;
- distribution shift;
- specification error;
- accidental implementation defects;
- strategic users;
- malicious external content;
- compromised memory or tools;
- reward hacking;
- evaluator capture;
- organizational incentive distortion;
- colluding agents;
- self-serving meta-compilers.

The goal is not to solve all threats. It is to prevent persistent adaptation from silently amplifying them.

## 16.2 Semantic miscompilation

**Failure:** The lesson itself is false or incomplete.

**Examples:** a coincidence becomes a rule; one evaluator blind spot becomes a skill; a benchmark exploit becomes a capability claim.

**Controls:** source diversity, counterexamples, transfer, interventions, uncertainty, lesson versioning, `EVIDENCE_ONLY` disposition.

## 16.3 Scope miscompilation

**Failure:** A valid lesson is applied beyond its qualified domain or too narrowly to cover its cause.

**Controls:** typed operating regions, guarded admission, hierarchical region splitting, `UNKNOWN`, re-expansion, transfer tests.

## 16.4 Causal miscompilation

**Failure:** The system changes a correlated surface rather than the causal mechanism.

**Controls:** decision-time reconstruction, feasible comparators, intervention, causal bounds, minimal causal sets, unresolved status.

## 16.5 Locus miscompilation

**Failure:** The lesson is correct but stored in the wrong surface.

**Examples:** fine-tuning a volatile fact; adding memory for a tool bug; changing a model to compensate for an unsafe interface.

**Controls:** cross-surface alternatives, fixed-locus baselines, staged placement, placement regret.

## 16.6 Temporal miscompilation

**Failure:** Commitment occurs too early, too late, or on the wrong clock.

**Controls:** outcome maturity, fast containment versus slow consolidation, expiry, minimum dwell periods, hysteresis.

## 16.7 Pedagogical miscompilation

**Failure:** A compact trajectory is executable but teaches a learner to presuppose information unavailable at inference time.

**Controls:** decision-time information contracts, information-acquisition preservation, inspect-act-verify structure, process interventions, separate execution and learning compilations.

## 16.8 Integration miscompilation

**Failure:** Local realizations work separately but conflict when composed.

**Examples:** guard combinations cause universal refusal; sequential edits erase each other; multiple tools create inconsistent state.

**Controls:** compatibility hypergraph, higher-order tests, order analysis, re-synthesis, retained modular fallback.

## 16.9 Governance miscompilation

**Failure:** Useful behavior acquires unjustified authority, shifts burden, or changes rights.

**Controls:** four-separation rule, normative firewall, affected-party standing, authority ceilings, appeals, independent promotion.

## 16.10 Stale-profile miscompilation

**Failure:** A previously valid realization remains active after model, environment, evaluator, dependency, or stakeholder change.

**Controls:** material-change invalidation, expiry, dependency closure, drift monitoring, canary requalification.

## 16.11 Recursive miscompilation

**Failure:** The persistence machinery alters its own evaluator, records, or promotion process to ratify itself.

**Controls:** proposal/promotion separation, frozen external tests, predecessor fallback, archive, evaluator-change epochs, human or institutional gates.

## 16.12 Memory poisoning and origin laundering

**Failure:** adversarial content becomes durable memory or rule; later summaries conceal the untrusted origin.

**Controls:** restricted write channels, source identity, taint, quarantine, independent verification, rate limits, source concentration tests, derivation lineage.

Recent persistent-memory attacks show that delayed compromise can survive across sessions and later cause agentic actions [31-33]. Input filtering alone is insufficient when the update mechanism itself can promote untrusted content.

## 16.13 Recurrence laundering

**Failure:** one poisoned source produces many correlated traces and appears independently recurrent.

**Controls:** evidence genealogy, effective-source count, cluster-level weighting, source-diverse confirmation, adversarial recurrence tests.

## 16.14 Evaluator capture

**Failure:** candidate and evaluator share a blind spot, training data, provider, prompt, toolchain, or incentive.

**Controls:** evaluator lineage vectors, deterministic anchors, hidden tests, delayed external outcomes, adversarial critics, evaluator-first investment.

Multiple prompts to the same model do not constitute independent evaluators.

## 16.15 Reward laundering

**Failure:** proxy improvement is narrated as target improvement.

**Controls:** separate proxy and target claims, reward-hacking probes, causal ablations, hidden transfer, independent outcome evaluation.

Partial reward identifiability [34] and spontaneous reward hacking in iterative refinement [35] make this a central risk.

## 16.16 Probability-mass displacement

**Failure:** suppressing one bad behavior increases another.

**Controls:** distribution-level audits, alternative outputs, pass@k analysis, counterfactual correction pairs, calibrated abstention, protected-positive suites.

## 16.17 Excessive repulsion and catastrophic fixation

**Failure:** old negative evidence continues to push behavior after the target is remote, or one vivid incident dominates adaptation.

**Controls:** learner-relative relevance, decay, recurrence weighting, severity caps, diversity quotas, conversion of mature lessons into tests or guards.

## 16.18 Creativity and exploration suppression

**Failure:** novel valid behavior resembles past failure and is blocked.

**Controls:** protected counterfactual surplus, novelty sandboxes, shadow alternatives, appeals, valid-exception tests, deliberation reserve.

## 16.19 Competence starvation

**Failure:** fast paths reduce practice and degrade the general solver or human recovery capability.

**Controls:** reserve traffic, drills, independent solving, human-skill metrics, explicit retirement decisions.

## 16.20 Observability collapse

**Failure:** the system chooses actions with weaker logging, shortens evaluation horizons, or suppresses incident reports.

**Controls:** external telemetry, missingness monotonicity, minimum logging, independent audit sampling, conservative risk bounds when evidence disappears.

Missing evidence must not lower estimated risk by default.

## 16.21 Descendant amnesia

**Failure:** revoking a lesson updates one store while leaving copies, fine-tunes, indexes, tools, publications, or organizational descendants unchanged.

**Controls:** descendant graph, invalidation propagation, claim-specific closure, residual reporting, no universal erasure claim.

## 16.22 Institutional capture

**Failure:** organizations suppress embarrassing evidence, prefer metrics showing few incidents, or shift burdens to users and reviewers.

**Controls:** independent reporting, audit rights, waiver ownership, separation of deployment incentive from incident adjudication, whistleblower and appeal mechanisms.

Technical architecture cannot substitute for institutional accountability.

## 16.23 Privacy-forensics tension

Failure investigation favors detailed records; privacy favors minimization.

Controls include:

- purpose limitation;
- approved-span retention;
- redaction;
- restricted evidence stores;
- content commitments;
- differential access;
- deletion records;
- explicit statements of which future claims become weaker after deletion.

The framework does not resolve the tension by declaring either maximal logging or maximal deletion universally correct.

## 16.24 Dual use

A system capable of discovering residual failures can also discover exploits. Skill traces, incident archives, and counterfactual probes can increase offensive capability.

Controls include:

- sandboxing;
- separation between critic and actor access;
- minimum-necessary disclosure;
- risk-tiered release;
- restricted tools;
- monitoring of exploit reproduction;
- publication of abstractions rather than operational payloads where appropriate.

---

# 17. Implementation Architecture

## 17.1 No omniscient super-compiler

A single component capable of understanding every causal, technical, organizational, and normative issue would be more difficult to trust than the system it governs.

The architecture should therefore separate bounded services.

![Figure 5. Reference architecture for Adjudicated Persistence, separating integrity, adjudication, lesson identity, placement, locus-specific compilation, qualification, runtime monitoring, retirement, and meta-compilation.](figures/figure2_architecture.png)

*Figure 5. Reference architecture. The meta-compiler can propose changes to the system, but independent qualification remains outside its sole control.*

## 17.2 Experience Integrity Layer

Responsibilities:

- capture exact system and dependency identity;
- record action and observation timelines;
- preserve missingness and censored attempts;
- validate custody and provenance;
- bind actor-visible information;
- track delayed effects;
- enforce privacy and authorized use.

It does not decide what the experience means.

## 17.3 Learning Eligibility Tribunal

Responsibilities:

- outcome/process separation;
- root-cause hypotheses;
- causal identifiability;
- comparator validity;
- evaluator adequacy;
- normative escalation;
- persistence disposition.

It may use models, formal methods, simulators, humans, and institutions. It must preserve disagreement and `UNKNOWN`.

## 17.4 Lesson Hypothesis Registry

Stores:

- stable lesson handles;
- versions;
- claims;
- domains;
- evidence;
- counterexamples;
- uncertainty;
- affected stakeholders;
- conflicts;
- supersession and revocation.

The registry is not a memory prompt. It is the continuity layer for persistence decisions.

## 17.5 Placement Portfolio Proposer

Responsibilities:

- generate candidate loci and bundles;
- estimate commitment profiles;
- compare cost, transfer, interference, observability, human effects, and option value;
- track rejected alternatives;
- propose staged experiments.

It has proposal authority only.

## 17.6 Locus-specific compilers

Separate compilers produce:

- data and training bundles;
- memory objects;
- retrieval policies;
- adapters and model updates;
- tools and workflows;
- semantic or world-model revisions;
- tests and evaluators;
- orchestration and topology changes;
- environmental modifications;
- organizational procedures.

Each emits artifact, dependency, loss, guard, and recovery receipts.

## 17.7 Qualification gate

Responsibilities:

- Evidence-Commitment Matching;
- baseline comparison;
- protected-positive tests;
- counterexample attacks;
- evaluator independence analysis;
- transfer;
- authority and rights checks;
- recovery rehearsal;
- lease issuance.

Qualification cannot be owned solely by the candidate compiler.

## 17.8 Runtime guard and monitor

Responsibilities:

- evaluate `ADMIT`, `DENY`, `UNKNOWN`;
- enforce authority ceiling;
- collect telemetry;
- detect drift and counterexamples;
- maintain counterfactual-observability samples;
- trigger fallback and containment;
- track descendant creation.

## 17.9 Decompiler and retirement manager

Responsibilities:

- narrow scope;
- split lessons;
- relocate realizations;
- suspend or revoke routes;
- restore internal state where possible;
- compensate external effects;
- propagate invalidation;
- archive lineage;
- maintain residuals.

## 17.10 Meta-compiler sandbox

Responsibilities:

- propose changes to adjudication, placement, compilation, and monitoring;
- run frozen comparison campaigns;
- preserve predecessor and archive;
- expose all failed candidates;
- submit to independent promotion.

## 17.11 Memory strata

Persistence-related evidence should be divided by authority and purpose.

| Stratum | Contents | Default authority |
|---|---|---|
| Forensic evidence store | raw incidents, traces, exploit details, provenance | restricted; not directly actionable |
| Quarantined hypothesis store | tentative causes, clusters, counterfactuals | investigative only |
| Qualified lesson registry | adjudicated lessons, domains, evidence, expiry | supports proposal and qualified retrieval |
| Protected competence archive | valid positives, exceptions, rare capabilities, alternatives | regression and exploration protection |
| Runtime index | minimal warnings, guards, recovery routes | invocation-specific influence |

Summarization does not grant authority. An untrusted source remains untrusted through paraphrase unless separately admitted.

## 17.12 Core lifecycle

```text
OBSERVED
  -> INTEGRITY_CHECKED
  -> ADJUDICATED
       -> REJECTED
       -> EVIDENCE_ONLY
       -> QUARANTINED
       -> INVESTIGATION_REQUIRED
       -> TEMPORARY_CONTAINMENT
       -> NORMATIVE_REVIEW
       -> COMPILATION_CANDIDATE
            -> PLACEMENT_PROPOSED
            -> CHALLENGED
            -> SHADOW
            -> CANARY
            -> QUALIFIED
            -> ACTIVE
                 -> NARROWED
                 -> SPLIT
                 -> RELOCATED
                 -> RECOMPILED
                 -> SUSPENDED
                 -> SUPERSEDED
                 -> REVOKED
                 -> RETIRED
```

Temporary containment can occur from any material state without implying causal resolution.

## 17.13 Reference control loop

```text
repeat:
    capture experience with exact identity and provenance
    adjudication = tribunal.evaluate(experience)

    if adjudication requires containment:
        activate narrow reversible containment

    if adjudication is not persistence-eligible:
        retain, reject, investigate, repair evaluator, or escalate
        continue

    lessons = registry.version(adjudication.lesson_hypotheses)
    portfolios = proposer.generate(lessons, locus_registry)

    for portfolio in least_commitment_order(portfolios):
        realizations = compile_by_locus(portfolio)
        verdict = qualifier.evaluate(realizations)
        if verdict permits shadow or canary:
            transactionally_activate(realizations, verdict.lease)
            monitor_with_slow_path_and_audit_reserve()
            break

    on drift, counterexample, expiry, rights change, or dependency change:
        narrow, deoptimize, relocate, revoke, compensate, or retire
```

## 17.14 Minimum viable implementation

A first research prototype should be intentionally narrow.

Recommended domain: sandboxed software maintenance with:

- exact repository snapshots;
- file and tool identity;
- deterministic tests and mutation tests;
- explicit permissions;
- replayable trajectories;
- known defect injections;
- several adaptation loci: memory, prompt/harness, tool, test, adapter;
- no irreversible external deployment.

The initial system need not solve open-world organizational learning. It should demonstrate that matched outcomes can be adjudicated and placed differently, and that placement matters.

---
# 18. Discussion

## 18.1 Adjudicated Persistence as a missing control plane

Modern adaptive systems often have many update pathways but no common control plane over persistence.

A model trainer decides what changes parameters.

A memory system decides what gets stored.

A tool agent decides what becomes a skill.

A benchmark owner decides what becomes a regression.

A deployment team decides what becomes default.

An organization decides what becomes procedure.

When these decisions are isolated, the same event can be:

- fine-tuned into the model;
- written into memory;
- encoded as a tool;
- added to a test;
- and converted into a policy

without one record explaining whether the layers agree, duplicate, or conflict.

Adjudicated Persistence is a proposed control plane over these transitions. It does not replace local adaptation mechanisms. It establishes shared semantics for evidence, lesson identity, commitment, qualification, authority, and lifecycle.

## 18.2 The deepest design shift: persistence is earned

The ordinary framing is:

\[
\text{experience}
\rightarrow
\text{learning update}.
\]

The proposed framing is:

\[
\text{experience}
\rightarrow
\text{persistence candidacy}
\rightarrow
\text{adjudication}
\rightarrow
\text{qualified commitment or noncommitment}.
\]

This change matters because many adaptive failures are not failures of learning capacity. They are failures of admission:

- the system learned from poisoned evidence;
- learned the wrong cause;
- learned at the wrong layer;
- learned too broadly;
- learned too permanently;
- learned without preserving exceptions;
- learned under a captured evaluator;
- or learned what it was not authorized to decide.

A strong learner is not merely easy to update. It is selective about what acquires future causal power.

## 18.3 Search and structure

The framework preserves the search-to-structure intuition while narrowing it.

Flexible computation is valuable for:

- novelty;
- ambiguity;
- exploration;
- synthesis;
- exception handling;
- repair.

Persistent structure is valuable for:

- recurrence;
- exact execution;
- low-latency response;
- preservation;
- coordination;
- assurance.

The system should not choose one permanently. It should move work between them:

\[
\boxed{
\text{search handles novelty}
\quad
\text{structure handles qualified recurrence}
\quad
\text{residuals reopen search}
}
\]

This resembles amortization, partial evaluation, profile-guided optimization, and library learning [7-10,14,15], but adds evidence, authority, and lifecycle constraints.

## 18.4 Persistence and alignment

Adjudicated Persistence is not a complete alignment theory. It addresses a narrower question: how an adaptive system's future behavior is changed by experience.

That boundary is alignment-relevant because:

- reward models can drift;
- memories can carry untrusted norms;
- tools can acquire practical authority;
- evaluators can be Goodharted;
- organizations can institutionalize harmful routines;
- meta-compilers can modify the processes that judge improvement.

The framework contributes structural defenses:

- no automatic objective mutation;
- support/qualification/authority separation;
- independent promotion;
- evidence-matched commitment;
- residual preservation;
- contestability;
- slow-path and fallback.

These controls do not guarantee aligned goals. They make goal and authority changes harder to hide inside ordinary learning.

## 18.5 Persistence and interpretability

Externalized lessons are often easier to inspect than parametric changes, but externalization is not automatically interpretable.

A generated tool can contain opaque code.

A memory can contain misleading summaries.

A test suite can encode an incorrect construct.

An organizational rule can obscure who bears cost.

Interpretability should therefore be measured by whether a reviewer can reconstruct:

- the lesson claim;
- its evidence;
- its applicability;
- its realization;
- its effects;
- its exceptions;
- its lifecycle.

A compact artifact with no lineage is not necessarily more understandable than a model update.

## 18.6 Persistence and modularity

The framework gives modularity an operational role.

Modularity can:

- localize change;
- preserve alternatives;
- simplify revocation;
- reduce interference;
- improve causal attribution.

But modules also create:

- interface assumptions;
- routing errors;
- hidden shared state;
- duplicated capability;
- maintenance burden.

Cross-Surface Adaptation Assignment should therefore choose modular or integrated realizations empirically. Modularity is an option, not a moral principle.

## 18.7 Persistence and compression

The theory extends compression in three ways.

First, it includes future computation and coordination cost, not only storage.

Second, it treats residuals as first-class. A compressed structure is not permitted to rename unexplained information as noise merely because it is inconvenient.

Third, it includes assurance and governance cost. A representation that is slightly larger but easier to verify, update, or revoke can have lower total lifecycle cost.

The relevant question is:

> **What is the least committing structure that preserves the distinctions the system is obligated to make?**

## 18.8 Persistence and scale

As systems become more capable, the commit boundary becomes more consequential for two reasons.

First, each durable change can influence more tasks, users, tools, and descendants.

Second, the system may become better at proposing persuasive but self-serving lessons.

Greater capability should therefore increase—not reduce—the importance of:

- exact identity;
- independent evaluation;
- material-change invalidation;
- authority separation;
- slow-path preservation;
- external monitoring.

A highly capable optimizer should not be trusted with broader persistence merely because it is competent. Competence increases both useful proposal power and potential commitment amplification.

## 18.9 Persistence and scientific learning

The framework also applies to scientific systems.

Repeated residuals can become:

- a new latent variable;
- a causal relation;
- an equation;
- a simulation component;
- an experimental protocol;
- a measurement correction;
- a research priority.

Scientific persistence should preserve:

- data lineage;
- alternative hypotheses;
- model dependence;
- falsifying tests;
- uncertainty;
- scope;
- retraction.

A theory is a compact generative structure, but it remains qualified relative to observations, interventions, and domains. Scientific progress is therefore another search-to-structure ratchet governed by evidence and defeasibility.

## 18.10 Persistence and artificial general intelligence

A general intelligence cannot store every experience verbatim, reason through every recurring task from scratch, or internalize every lesson into one homogeneous parameter space.

It must decide:

- which experiences matter;
- which can be generalized;
- which should remain episodic;
- which should become skills;
- which should become concepts;
- which require environmental or institutional change;
- which should not be learned;
- which old lessons should be reopened.

Adjudicated Persistence therefore describes a necessary systems problem for increasingly general agents. It does not establish that solving the problem is sufficient for AGI or ASI.

## 18.11 Why the theory is not a bureaucracy mandate

The framework can be overbuilt.

A persistence packet that costs more than the expected future benefit is a failure. Low-risk, easily reversible settings may need only lightweight records and automatic tests. High-risk, high-authority, hard-to-reverse changes need stronger adjudication.

The intended principle is proportionality:

\[
C_{\mathrm{governance}}
<
\mathbb E[
\text{avoided error}
+
\text{future reuse}
+
\text{recovery value}
].
\]

If a field, check, or review never changes an admission, route, rollback, or understanding, it should be simplified or removed.

## 18.12 Why the theory remains falsifiable

Adjudicated Persistence would be weakened if:

- cross-surface assignment does not outperform simpler policies;
- commitment profiles do not predict risk or lifecycle burden;
- Evidence-Commitment Matching does not reduce overshoot;
- the slow path does not preserve recovery;
- transaction semantics add cost without catching stale or partial updates;
- lesson identity does not aid migration or revocation;
- the full framework cannot beat domain-specific adaptation systems.

The theory's breadth is a liability unless the common abstractions improve prediction and control across several domains.

---

# 19. Limitations and Non-Claims

## 19.1 No universal placement oracle

The paper does not provide a universally correct algorithm for choosing among weights, memory, tools, evaluators, environments, and institutions. Placement can be computationally difficult, partially observed, and normatively contested.

The contribution is to formalize the decision, expose its variables, and propose staged comparison.

## 19.2 Causal identification remains conditional

Logs alone rarely determine causality. Identifiability depends on assumptions, interventions, coverage, and models [39,40]. The framework's `CONFOUNDED`, `MODEL_DEPENDENT`, and `UNIDENTIFIED` states do not solve this limitation; they prevent it from being hidden.

## 19.3 No universal scalarization

Task quality, safety, privacy, latency, human skill, authority, and legitimacy are not always compensable. Pareto comparison and contested status do not eliminate the need for legitimate policy and judgement.

## 19.4 No complete open-world coverage

Guards and tests cannot enumerate every future state. A qualified realization can fail outside its measured envelope. `UNKNOWN`, monitoring, and fallback reduce but do not eliminate this risk.

## 19.5 No perfect evaluator independence

Evaluators can share models, data, organizations, incentives, and blind spots. Genealogy and diversity are diagnostics, not guarantees.

## 19.6 No universal reversibility

External actions, disclosures, human effects, market transactions, and institutional commitments can be irreversible. The framework separates rollback, recovery, compensation, and residuals rather than promising undo.

## 19.7 No complete unlearning guarantee

A lesson can propagate into hidden copies, model parameters, derived artifacts, external recipients, and human beliefs. Machine-unlearning methods can address bounded surfaces [4], but complete open-world erasure may be unverifiable.

## 19.8 No automatic legitimacy

A technically complete persistence record does not establish consent, fairness, rights, or social legitimacy. Institutional uses require real affected-party and governance processes.

## 19.9 No guaranteed benefit from externalization

Tools and memory can be more inspectable than weights, but can also be brittle, poisoned, or poorly integrated. The paper does not claim that externalized learning is universally superior.

## 19.10 No guaranteed assurance shift

The Conditional Assurance Shift is empirical and local. New domains, distribution changes, or missing positive capability can restore the value of ordinary positive acquisition.

## 19.11 No solved recursive self-improvement

The meta-compilation architecture separates proposal and promotion but does not prove that a powerful self-modifying system will remain corrigible, nondeceptive, or aligned. It defines a boundary that should be tested.

## 19.12 Cost and usability

The framework introduces records, evaluators, monitors, and lifecycle operations. These can create latency, human workload, and engineering burden. Minimum viable versions should be tested against simple baselines and removed where they do not pay for themselves.

## 19.13 Terminology risk

The word *compilation* is metaphorical across some loci. The paper limits the term to reusable, scoped, qualified structures with computational consequence. Ordinary adaptation remains the broader category.

## 19.14 Literature freshness

The agent-adaptation literature is changing rapidly. Several relevant 2025-2026 works are preprints. Publication should include a refreshed systematic search and avoid novelty claims based on absence from one terminology.

---

# 20. Conclusion

The initial problem appears simple:

> How should an intelligent system learn from experience?

For persistent agents, the deeper question comes first:

> **What experience is allowed to change the future?**

An outcome does not identify its cause.

A cause does not identify the correct adaptation surface.

A lesson does not identify its implementation.

An implementation does not establish qualification.

Qualification does not grant authority.

A successful realization does not remain valid forever.

Adjudicated Persistence governs these separations.

It treats the Adaptive Commit Boundary as a consequential effect boundary. It requires experience integrity and decision-time reconstruction before learning. It represents lessons as defeasible identities rather than timeless truths. It assigns lessons to portfolios across parameters, memory, procedures, semantics, orchestration, structure, evaluation, environments, and institutions. It matches the strength of durable commitment to evidence and legitimate authority. It favors Minimum Sufficient Persistence, guarded use, `UNKNOWN`, re-expansion, counterfactual observability, and a deliberation reserve. It treats promotion as a transaction and revocation as a descendant-aware lifecycle. It permits the compiler to improve while denying it sole authority over its own promotion.

The resulting lifecycle is:

\[
\boxed{
\begin{aligned}
\text{novelty}
&\rightarrow
\text{flexible computation}
\rightarrow
\text{experience}
\rightarrow
\text{adjudication}
\\
&\rightarrow
\text{placement}
\rightarrow
\text{guarded compilation}
\rightarrow
\text{qualification}
\\
&\rightarrow
\text{bounded commitment}
\rightarrow
\text{monitoring}
\\
&\rightarrow
\text{reinforcement, revision, relocation, or revocation}
\rightarrow
\text{new novelty}.
\end{aligned}
}
\]

Search handles novelty.

Structure handles qualified recurrence.

Residuals reopen search.

But the deepest principle is prior to all three:

> **Experience must earn the right to become structure.**

A weak adaptive system changes whenever evidence pushes it.

A stronger system distinguishes evidence from interpretation.

A stronger one identifies which lessons are actually supported.

A stronger one chooses where and how those lessons should persist.

A mature one knows when the lesson no longer applies.

A recursively improving one can improve this process without granting itself the authority to define success.

That is the proposed foundation of Adjudicated Persistence.

---

# Appendix A. Adjudicated Persistence Packet

```yaml
adjudicated_persistence_packet:
  packet_id: string
  schema_version: string

  experience:
    episode_ids: [string]
    system_version_bundle: object
    adaptive_resolution: string
    operating_regions: [object]
    decision_time_information: object
    objectives_constraints_rights_authority: object
    trajectory_refs: [string]
    observations: [object]
    immediate_outcomes: [object]
    delayed_outcomes: [object]
    outcome_maturity: IMMEDIATE | PROVISIONAL | HORIZON_OPEN | MATURE | PERMANENTLY_PARTIAL
    retries_interventions_and_censored_attempts: [object]
    telemetry_gaps: [object]
    provenance_and_integrity: object

  adjudication:
    outcome_quality: GOOD | BAD | MIXED | UNRESOLVED
    process_quality: DEFENSIBLE | DEFECTIVE | MIXED | UNRESOLVED
    authority_status: COMPLIANT | VIOLATED | UNRESOLVED
    specification_status: VALID | DISPUTED | DEFECTIVE | UNRESOLVED
    evaluator_status: ADEQUATE | DEFECTIVE | DISPUTED | UNRESOLVED
    root_cause_hypotheses: [object]
    minimal_causal_sets: [object]
    interaction_terms: [object]
    comparator_contracts: [object]
    identifiability: IDENTIFIED | BOUNDED | MODEL_DEPENDENT | CONFOUNDED | UNIDENTIFIED
    unresolved_hypotheses: [object]
    allowed_dispositions: [string]
    selected_disposition: string

  lesson:
    lesson_id: string
    version: string
    claim: string
    lesson_class: string
    applicability_domains: [object]
    transfer_hypothesis: object
    supporting_evidence: [string]
    counterexamples: [string]
    contradictions: [string]
    protected_positives: [string]
    uncertainty: object
    temporal_validity: object
    normative_and_authority_status: object
    supersedes: [string]
    superseded_by: [string]

  placement:
    candidate_loci: [string]
    candidate_portfolios: [object]
    commitment_profiles: [object]
    compatibility_hyperedges: [object]
    rejected_portfolios: [object]
    contested_alternatives: [object]
    expected_value_vectors: [object]
    lifecycle_costs: [object]
    human_and_affected_party_effects: [object]

  realization:
    portfolio_id: string
    exact_artifacts: [object]
    compiler_versions: [object]
    dependencies_and_descendants: [object]
    declared_losses_and_approximations: [object]
    guards: [object]
    authority_ceiling: object
    effect_envelope: object
    fallback_and_slow_path: object

  qualification:
    evidence_commitment_match: PASS | FAIL | UNKNOWN | CONTESTED
    tests: [object]
    baselines: [object]
    hidden_holdouts: [object]
    adversarial_controls: [object]
    evaluator_genealogy: [object]
    protected_positive_results: [object]
    transfer_results: [object]
    failed_attempts: [object]
    qualification_status: REJECTED | QUARANTINED | SHADOW | CANARY | QUALIFIED
    nonclaims: [string]

  lifecycle:
    allowed_routes: [object]
    blocked_routes: [object]
    monitoring_window: object
    counterfactual_observability_plan: object
    deliberation_reserve: object
    expiry: object
    invalidation_triggers: [object]
    rollback_scope: object
    compensation_plan: object
    unlearning_and_descendant_closure: object
    residual_owner: string
    retirement_receipt: object
```

---

# Appendix B. Lexicographic Acceptance Order

A candidate realization is evaluated in this order:

1. **Identity and integrity:** exact artifacts, source lesson, dependencies, and evidence are known.
2. **Authority:** the candidate and use are authorized.
3. **Hard constraints:** no unacceptable rights, permission, or irreversible-hazard violation is introduced.
4. **Evidence-Commitment Matching:** evidence supports the proposed commitment profile.
5. **Target efficacy:** the realization reduces the intended defect on held-out and transfer tests.
6. **Adversariality:** exploit, evasion, inversion, poisoning, and burden-shift attacks are tested.
7. **Valid-behavior preservation:** protected positives and legitimate exceptions remain within tolerance.
8. **System compatibility:** active repairs, tools, memory, routing, evaluation, and recovery remain coherent.
9. **Coverage and observability:** useful action and detection do not collapse.
10. **Counterfactual observability:** the replaced path remains measurable enough for the consequence class.
11. **Recovery and revocation:** containment, fallback, restoration, compensation, and descendant obligations are explicit.
12. **Cost:** expected assured benefit justifies synthesis, verification, carrying, governance, and human costs.

Identity, authority, and hard constraints are noncompensable gates. High average efficacy cannot wash them away.

---

# Appendix C. Reference Algorithms

## C.1 Monitor and reconsider

```text
ALGORITHM MonitorAndReconsider(active realization R, lease Q)

repeat until lease expiry or retirement:
    observe target outcomes, protected positives, guard decisions,
        drift, counterexamples, costs, human effects, and descendants

    maintain slow-path audit and deliberation reserve according to risk

    if evidence missingness increases materially:
        raise uncertainty; missing evidence cannot lower risk by default

    if dependency, evaluator, authority, consumer, use, environment,
       or lesson version changes materially:
        suspend affected routes and require requalification

    if guard failure or counterexample is local:
        narrow, split, or generate a bridge realization

    if the realization no longer dominates the slow path:
        deoptimize or relocate

    if harm or rights failure is material:
        contain, revoke, compensate, and propagate invalidation

    if carrying cost exceeds expected future value:
        retire after preserving evidence and fallback

    emit a versioned lifecycle receipt for every transition
```

## C.2 Meta-compiler evaluation

```text
ALGORITHM EvaluateMetaCompiler(candidate M', incumbent M, external policy Π)

1. Freeze task families, hidden tests, evaluator set, budgets, and promotion rule.
2. Preserve incumbent M as fallback and archive.
3. Run M and M' on matched experience streams with identical opportunity.
4. Retain every proposal, rejection, failure, and cost.
5. Evaluate causal diagnosis, false persistence, missed persistence,
   placement regret, commitment overshoot, lifecycle cost, and evaluator influence.
6. Attack M' with poisoned recurrence, target manipulation, evaluator change,
   self-preference, and predecessor suppression.
7. Require independent review of any proposed evaluator or policy change.
8. Promote only under externally owned authority and staged exposure.
```

---

# Appendix D. LocusBench Preregistration Template

## D.1 Study identity

- Domain and tier:
- Exact system versions:
- Adaptation loci enabled:
- Evaluator portfolio and genealogy:
- Natural distribution:
- Probe distributions:
- Operating-region definitions:
- Consequence classes:
- Date and preregistration hash:

## D.2 Primary hypothesis

- Defect classes:
- Predicted placement advantage:
- Minimum effect of interest:
- Primary endpoint:
- Falsification threshold:

## D.3 Cost accounting

Report separately:

- training compute;
- inference and sampling;
- data generation;
- human annotation and review;
- evaluator calls;
- simulation;
- integration and regression;
- monitoring;
- governance;
- memory and storage;
- migration and revocation;
- probe harm or real exposure.

## D.4 Required baselines

- no persistent update;
- always weights;
- always memory;
- always tool;
- always harness;
- fixed placement policy;
- learned single-locus;
- learned portfolio;
- oracle placement;
- full framework;
- domain-standard method.

## D.5 Required integrity measures

- false persistence;
- missed persistence;
- useful coverage;
- false inhibition;
- observability;
- calibration;
- subgroup and tail risk;
- burden transfer;
- train-deployment divergence;
- protected-positive retention;
- human capability floor;
- descendant closure.

## D.6 Analysis plan

- paired or matched seeds:
- sample-size calculation:
- confidence intervals:
- multiple-comparison correction:
- hierarchical or mixed-effects model:
- missing-data treatment:
- preregistered exclusions:
- exploratory analyses:

## D.7 Falsification rule

State in advance what result would count against Adjudicated Persistence or one of its conjectures rather than merely motivating another patch.

---

# Appendix E. Compact Glossary

**Adaptive Commit Boundary:** The point where transient evidence gains durable influence over future behavior.

**Adjudicated Persistence:** The theory governing whether, where, and how experience should become persistent.

**Adaptation locus:** A persistent surface that can change future behavior.

**Lesson hypothesis:** A defeasible, testable claim extracted from experience.

**Persistence disposition:** The decision to reject, retain, investigate, contain, compile, escalate, or revoke.

**Realization:** A concrete artifact implementing a lesson in one locus.

**Commitment profile:** Scope, binding, persistence, coupling, authority, irreversibility, and descendant reach.

**Evidence-Commitment Matching:** The requirement that evidence satisfy the obligations induced by a proposed commitment.

**Minimum Sufficient Persistence:** The least committing admissible portfolio that adequately captures a lesson.

**Guarded compilation:** Creation of a reusable realization with scope, guards, qualification, fallback, and lifecycle.

**Counterfactual observability:** Ability to estimate the behavior of the path replaced by a compiled realization.

**Deliberation reserve:** Preserved slow-path, human-practice, audit, and exploration capacity.

**Adaptation debt:** The combined burden of repeated rediscovery, rigidity, assurance shortfall, and revocation difficulty.

**Meta-compilation:** Adaptation of the process that adjudicates, places, or compiles lessons.

---

# References

[1] J. L. McClelland, B. L. McNaughton, and R. C. O'Reilly, “Why There Are Complementary Learning Systems in the Hippocampus and Neocortex: Insights from the Successes and Failures of Connectionist Models of Learning and Memory,” *Psychological Review*, vol. 102, no. 3, pp. 419-457, 1995. doi:10.1037/0033-295X.102.3.419.

[2] J. Kirkpatrick et al., “Overcoming Catastrophic Forgetting in Neural Networks,” *Proceedings of the National Academy of Sciences*, vol. 114, no. 13, pp. 3521-3526, 2017. doi:10.1073/pnas.1611835114.

[3] D. Lopez-Paz and M. Ranzato, “Gradient Episodic Memory for Continual Learning,” in *Advances in Neural Information Processing Systems 30*, 2017, pp. 6467-6476.

[4] L. Bourtoule et al., “Machine Unlearning,” in *2021 IEEE Symposium on Security and Privacy*, pp. 141-159, 2021. doi:10.1109/SP40001.2021.00019. arXiv:1912.03817.

[5] K. Meng, D. Bau, A. Andonian, and Y. Belinkov, “Locating and Editing Factual Associations in GPT,” in *Advances in Neural Information Processing Systems 35*, 2022. arXiv:2202.05262.

[6] K. Meng, A. S. Sharma, A. Andonian, Y. Belinkov, and D. Bau, “Mass-Editing Memory in a Transformer,” in *International Conference on Learning Representations*, 2023. arXiv:2210.07229.

[7] B. Amos, “Tutorial on Amortized Optimization,” arXiv:2202.00665, 2022.

[8] N. D. Jones, C. K. Gomard, and P. Sestoft, *Partial Evaluation and Automatic Program Generation*. Prentice Hall, 1993.

[9] D. Chen, D. X. Li, and T. Moseley, “AutoFDO: Automatic Feedback-Directed Optimization for Warehouse-Scale Applications,” in *Proceedings of the 2016 International Symposium on Code Generation and Optimization*, pp. 12-23, 2016. doi:10.1145/2854038.2854044.

[10] O. Flückiger, G. Scherer, M.-H. Yee, A. Goel, A. Ahmed, and J. Vitek, “Correctness of Speculative Optimizations with Dynamic Deoptimization,” arXiv:1711.03050, 2017.

[11] J. G. March, “Exploration and Exploitation in Organizational Learning,” *Organization Science*, vol. 2, no. 1, pp. 71-87, 1991. doi:10.1287/orsc.2.1.71.

[12] M. S. Feldman and B. T. Pentland, “Reconceptualizing Organizational Routines as a Source of Flexibility and Change,” *Administrative Science Quarterly*, vol. 48, no. 1, pp. 94-118, 2003. doi:10.2307/3556620.

[13] S. Sundaresan and I. Guler, “Algorithmic Recommendation Tools and Experiential Learning in Clinical Care,” *Organization Science*, vol. 36, no. 5, pp. 1786-1802, 2025. doi:10.1287/orsc.2022.16738.

[14] K. Ellis et al., “DreamCoder: Growing Generalizable, Interpretable Knowledge with Wake-Sleep Bayesian Program Learning,” arXiv:2006.08381, 2020.

[15] M. Bowers, T. X. Olausson, L. Wong, G. Grand, J. B. Tenenbaum, K. Ellis, and A. Solar-Lezama, “Top-Down Synthesis for Library Learning,” in *Proceedings of the ACM on Programming Languages*, vol. 7, POPL, 2023. arXiv:2211.16605.

[16] A. Zhao et al., “ExpeL: LLM Agents Are Experiential Learners,” arXiv:2308.10144, 2023.

[17] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, L. Zettlemoyer, N. Cancedda, and T. Scialom, “Toolformer: Language Models Can Teach Themselves to Use Tools,” arXiv:2302.04761, 2023.

[18] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar, “Voyager: An Open-Ended Embodied Agent with Large Language Models,” arXiv:2305.16291, 2023.

[19] P. Jiang et al., “Adaptation of Agentic AI,” arXiv:2512.16301, 2025.

[20] A. Jaglan and J. Barnes, “Continual Learning, Not Training: Online Adaptation for Agents,” arXiv:2511.01093, 2025.

[21] Y. Xiong, S. Hu, and J. Clune, “Learning to Continually Learn via Meta-Learning Agentic Memory Designs,” arXiv:2602.07755, 2026.

[22] H. Zhou et al., “Memento-Skills: Let Agents Design Agents,” arXiv:2603.18743, 2026.

[23] Y. Huang et al., “MemoHarness: Agent Harnesses That Learn from Experience,” arXiv:2607.14159, 2026.

[24] Q. Chen, A. Bellucci, Z. Sun, and G. Jacucci, “SkillDroid: Compile Once, Reuse Forever,” arXiv:2604.14872, 2026.

[25] H. Sun et al., “Experience Makes Skillful: Enabling Generalizable Medical Agent Reasoning via Self-Evolving Skill Memory,” arXiv:2606.09365, 2026.

[26] G. Liu, H. Zhao, and Q. Yao, “Falsifiable Commitment Planning for Self-Correcting Web Agents,” arXiv:2607.24167, 2026.

[27] L. Jiang, H. Xu, Y. Ding, and A. Zhang, “Trajectory-Refined Distillation,” arXiv:2606.08432, 2026.

[28] S. Yang et al., “What Makes Interaction Trajectories Effective for Training Terminal Agents?” arXiv:2606.03461, 2026.

[29] S. Pulipaka, O. Chen, M. Sharma, T. S. Bajwa, V. Raina, and I. Sheth, “PersistBench: When Should Long-Term Memories Be Forgotten by LLMs?” arXiv:2602.01146, 2026.

[30] T. Ding, A. Nannapaneni, B. Liu, and L. Zhang, “Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents,” arXiv:2606.30306, 2026.

[31] X. Chen, X. Xie, W. Fu, J. Zhou, S. Yu, and Q. Xuan, “MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair,” arXiv:2607.27080, 2026.

[32] Y. Zhang, S. Zhao, J. Zhang, J. Zhang, G. Deng, X. Liu, C. Xiao, and T. Zhang, “When Claws Remember but Do Not Tell: Stealthy Memory Injection in Persistent Personal Agents,” arXiv:2607.05189, 2026.

[33] S. Pulipaka, S. Hlebik, L. Raghav, S. Abdelnabi, V. Raina, I. Sheth, and M. Fritz, “Hidden in Memory: Sleeper Memory Poisoning in LLM Agents,” arXiv:2605.15338, 2026.

[34] J. Skalse, M. Farrugia-Roberts, S. Russell, A. Abate, and A. Gleave, “Invariance in Policy Optimisation and Partial Identifiability in Reward Learning,” in *Proceedings of the 40th International Conference on Machine Learning*, PMLR 202, pp. 32033-32058, 2023.

[35] J. Pan, T. He, J. R. Bowman, and S. Feng, “Spontaneous Reward Hacking in Iterative Self-Refinement,” arXiv:2407.04549, 2024.

[36] D. Manheim and S. Garrabrant, “Categorizing Variants of Goodhart's Law,” arXiv:1803.04585, 2018.

[37] L. Orseau and S. Armstrong, “Safely Interruptible Agents,” in *Proceedings of the 32nd Conference on Uncertainty in Artificial Intelligence*, pp. 557-566, 2016.

[38] J. Zhang, S. Hu, C. Lu, R. Lange, and J. Clune, “Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents,” arXiv:2505.22954, 2025.

[39] J. Pearl, *Causality: Models, Reasoning, and Inference*, 2nd ed. Cambridge University Press, 2009.

[40] M. A. Hernán and J. M. Robins, *Causal Inference: What If*. Chapman & Hall/CRC, 2020.

[41] T. Lebo, S. Sahoo, D. McGuinness, et al., “PROV-O: The PROV Ontology,” W3C Recommendation, 30 April 2013.

[42] National Institute of Standards and Technology, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, NIST AI 100-1, 2023. doi:10.6028/NIST.AI.100-1.

---

## Acknowledgment of scope

This manuscript is intentionally standalone. Its concepts are presented and justified within the paper rather than relying on prior architecture papers for definitions. The author welcomes independent attempts to formalize, falsify, simplify, or replace the proposed framework.
