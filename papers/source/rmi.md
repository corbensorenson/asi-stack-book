Ratcheting Modular Intelligence
A Unified Framework for Active Compression, Loop Closure, Benchmark Frontiers, and Routed Specialist Systems
White Paper
Public Release v1.0 — May 2026
Author: Corben Sorenson
Status: Conceptual Framework + AI Systems Architecture Proposal + Development Methodology
________________


TL;DR / Executive Abstract
Modern AI systems are powerful, but their development is fragmented. We scale models, benchmark them, attach tools, add memory, create agents, write safety policies, and occasionally change architectures. These pieces often work, but they are rarely unified into one coherent growth process.
This paper proposes Ratcheting Modular Intelligence, or RMI: a framework for AI systems that improve by turning pressure into structure.
The core thesis is:
AI systems should grow by compressing experience into verified modular structure, then using benchmark pressure to ratchet that structure toward harder capabilities.
RMI combines five ideas into one standalone framework:
Idea
	Role
	Compact generative structure
	Capabilities become durable when represented as small, inspectable structures that can generate, predict, control, or govern larger behaviors.
	Active compression
	Experience is compressed into memory, tools, policies, benchmarks, residual maps, and architecture changes that make future behavior easier to generate and verify.
	Cognitive loop closure
	Repeated reasoning/action trajectories are compiled into verified, parameterized tools.
	Benchmark ratcheting
	Benchmarks apply pressure until mastery, then become regression tests while harder benchmarks define the next frontier.
	Octopus routing
	A lightweight head/router dynamically composes specialized, independently improving modules rather than forcing every capability into one monolithic blob.
	The combined system works like this:
benchmark frontier
    ↓
head/router receives task
    ↓
specialist arms attempt subtasks
    ↓
successes and failures are logged
    ↓
repeated successful trajectories become tools
    ↓
failures become residual maps and residual escrow
    ↓
benchmarks diagnose whether the wall is data, training, inference, tooling, evaluation, or architecture
    ↓
arms and router improve independently
    ↓
mastered benchmarks become regression tests
    ↓
new harder benchmarks become the frontier
    ↓
repeat


A mature RMI system is not a single giant model trying to know everything. It is one coherent external agent composed of many bounded internal specialists.
The metaphor is an octopus. The head/router coordinates, but the arms are locally capable. Octopus arms are biologically rich control structures: recent cephalopod work notes that octopus arms are muscular hydrostats with extremely high degrees of freedom and hundreds of chemotactile suckers, and that more neurons are distributed across the arms than in the brain. This makes the octopus a useful analogy for distributed intelligence: one organism, many capable limbs, local control, global coordination. (Nature)
The informal metaphor is:
Goblins in a trenchcoat.
Externally, the user sees one agent. Internally, many specialized critters coordinate.
This framework argues against three failure modes:
1. Monolithic scaling: assuming every capability must live in one increasingly large model.
2. Static benchmarking: treating fixed benchmarks as permanent definitions of intelligence.
3. Repeated improvisation: forcing agents to reason through the same workflow forever.
Instead, RMI proposes:
Reason when novel. Execute when closed. Reflex when safety-critical. Ratchet when measured. Split when bloated. Retire when stale.
The system has three execution modes:
Mode
	Purpose
	Interpreter mode
	Flexible reasoning for novel, ambiguous, creative, or underspecified tasks.
	Compiled-tool mode
	Verified tool execution for repeated, parameterized, well-understood tasks.
	Reflex/failsafe mode
	Immediate safety behavior when latency or risk makes reasoning too slow.
	It also has a benchmark curriculum policy. A model or arm does not need 100% on every ordinary benchmark before moving forward. A benchmark can have a high initial mastery threshold, such as 90%, that decays over stalled effort toward a floor, such as 70%, for non-safety-critical tasks. The unsolved remainder enters residual escrow, where it is tracked, periodically reattempted, and promoted back into active development if it recurs across later benchmarks.
The key rule is:
The frontier must move, but the floor must hold.
RMI therefore maintains:
* a head/router;
* a set of specialist arms;
* an arm registry;
* a benchmark ledger;
* a model ledger;
* a tool registry;
* a residual escrow ledger;
* a public calibration track for apples-to-apples comparison;
* a safety/reflex layer;
* a routing memory;
* an intervention ladder that decides whether the next improvement should come from data, training, inference, loop closure, benchmark repair, bridge benchmarks, or architecture change.
The final claim is:
The best AI systems will not merely become larger. They will become better organized. They will turn pressure into structure, repetition into tools, failures into diagnostics, and benchmarks into curriculum.
That is Ratcheting Modular Intelligence.
________________


Abstract
AI progress is commonly described through scaling, benchmarks, post-training, tool use, agent scaffolding, memory, and architecture design. These are usually treated as separate concerns. This paper proposes a unified framework: Ratcheting Modular Intelligence.
Ratcheting Modular Intelligence is a framework for AI systems that improve by repeatedly confronting unsaturated benchmark frontiers, analyzing residual failures, converting repeated successful trajectories into verified parameterized tools, preserving mastered capabilities as regression tests, and routing work across specialized modules that can be independently improved, split, merged, retired, or dynamically loaded.
The framework synthesizes five mechanisms.
First, compact generative structure: a useful capability becomes durable when it is represented as a small, inspectable structure that can generate, predict, control, or govern a larger class of behaviors.
Second, active compression: experience is compressed into memory, tools, procedures, residual maps, benchmarks, policies, and architectures that reduce future uncertainty and effort.
Third, cognitive loop closure: repeated reasoning/action trajectories become verified tools rather than being re-inferred from scratch.
Fourth, benchmark ratcheting: benchmarks act as temporary pressure surfaces. Once mastered, they become regression tests; unresolved cases enter residual escrow; harder benchmarks define the next frontier.
Fifth, octopus routing: a lightweight learned head/router coordinates dynamically loaded specialist arms with local tools, memory, benchmarks, permissions, and verification contracts.
The paper defines the formal model, execution modes, benchmark lifecycle, time-decayed mastery thresholds, residual escrow, public calibration, loop-closure pipeline, octopus router architecture, specialist arm lifecycle, cognitive substrate options, safety and runtime tiers, ledgers, metrics, failure modes, and implementation roadmap.
RMI draws on existing research while proposing a system-level synthesis. Minimum Description Length frames learning as compression through model-plus-data description length. HELM emphasizes broad, multi-metric evaluation of language models. Toolformer shows that language models can learn when and how to call external tools. Voyager demonstrates an embodied LLM agent with an executable skill library. Mixture-of-Experts systems show the value of sparse expert activation inside neural networks. Liquid Time-constant Networks, KANs, HDC/VSA, and active inference provide candidate primitives for continuous state, inspectable transformations, compositional memory, and action selection. (Stanford CRFM)
The contribution of this paper is not any one primitive. The contribution is the architecture of growth:
Use benchmarks to expose missing capability, use loop closure to preserve repeated success, use modular routing to localize capability, and use verification to make progress durable.
________________


1. Introduction
1.1 The fragmentation problem
Modern AI systems are often built from pieces that do not fully cohere.
A model is trained.
A benchmark is run.
A tool is added.
A memory store is attached.
A workflow is scripted.
A safety policy is layered on top.
A benchmark saturates.
A new architecture is proposed.
A new agent scaffold is built.
Each piece may help, but the development process can become fragmented. The result is often an AI system that is powerful but poorly organized.
It may gain new capabilities while losing old ones.
It may overfit public benchmarks.
It may reason through repeated tasks from scratch.
It may accumulate tools without lifecycle management.
It may use the wrong specialist for a task.
It may fail to distinguish data problems from architecture problems.
It may scale a monolith when it needed a module.
It may automate a loop before discovering hidden parameters.
It may treat safety as an afterthought.
RMI proposes that these problems share one missing structure:
AI systems need a ratcheting architecture of growth.
________________


1.2 The central pattern
Across all the ideas developed in this paper, the same pattern appears:
pressure
    ↓
attempt
    ↓
residual
    ↓
compression
    ↓
verification
    ↓
structure
    ↓
new pressure


A benchmark applies pressure.
The system attempts the benchmark.
Failures become residuals.
Repeated successes become tools.
Tools and memories become compact structures.
Verified structures become the floor for the next level.
The next benchmark becomes the frontier.
The system grows by ratchet.
________________


1.3 Why benchmarks alone are not enough
Benchmarks are necessary, but they decay.
A benchmark can become too easy, too public, too contaminated, too narrow, too noisy, or too poorly aligned with the capability we care about.
This is already visible in frontier AI. Humanity’s Last Exam was introduced partly because models had exceeded 90% accuracy on popular benchmarks such as MMLU, reducing their usefulness as frontier measures. (Live Science) OpenAI argued in 2026 that SWE-bench Verified had become increasingly contaminated and no longer measured frontier coding capabilities well, recommending SWE-bench Pro instead. (OpenAI)
Benchmarks should therefore not be worshiped.
They should be used as pressure surfaces.
When they stop applying useful pressure, they should become regression tests or be retired.
________________


1.4 Why tool use alone is not enough
Tool use is useful, but ordinary tool use assumes tools already exist.
A more mature agent should notice when it repeatedly performs the same workflow and create a tool from that workflow.
This is cognitive loop closure:
repeated trajectories
    ↓
abstraction
    ↓
parameterization
    ↓
tool synthesis
    ↓
verification
    ↓
routing


Toolformer showed that language models can learn when and how to call external APIs, but RMI extends the question from tool use to tool formation: when should repeated agent behavior become a new verified tool? (Hugging Face)
________________


1.5 Why monolithic scaling alone is not enough
Large models are powerful. This paper does not deny that. But forcing all capability into one model creates problems of memory, specialization, interpretability, permissioning, and upgradeability.
The alternative is not to abandon general intelligence. The alternative is to organize it.
RMI proposes an octopus router architecture:
* one coherent external agent;
* many internal specialists;
* a lightweight head/router;
* dynamically loaded arms;
* local memory;
* local tools;
* local benchmarks;
* local permissions;
* local residuals;
* head-level composition.
The system scales by organization as well as parameter count.
________________


2. Definition of Ratcheting Modular Intelligence
A Ratcheting Modular Intelligence system is an AI system that improves by converting benchmark pressure, repeated behavior, and residual failures into verified modular capability.
It has seven core objects:
Object
	Meaning
	Head/router
	The coordinating system that interprets tasks, selects specialists, allocates budget, composes outputs, and enforces routing policy.
	Arms/specialists
	Domain-specific modules with local tools, memory, permissions, benchmarks, and verification contracts.
	Benchmark frontier
	The current unsaturated evaluation pressure surface.
	Regression suite
	Previously mastered benchmarks and cases used to preserve capability.
	Trajectory log
	Records of attempts, actions, tool calls, outputs, failures, and verification outcomes.
	Tool registry
	Verified parameterized tools compiled from repeated successful trajectories.
	Residual escrow
	Tracked unresolved failures, edge cases, benchmark defects, and recurring weaknesses.
	The system’s core loop is:
frontier benchmark
    ↓
head/router decomposes task
    ↓
arms execute subtasks
    ↓
results are verified and composed
    ↓
successes and failures are logged
    ↓
repeated successes close into tools
    ↓
failures enter residual maps or escrow
    ↓
intervention ladder selects next improvement
    ↓
benchmarks graduate or remain frontier
    ↓
arms/router/architecture ratchet upward


The framework’s central law is:
Improve the frontier without losing the floor.
________________


3. Formal Model
Let the system at development cycle (t) be:
$$
S_t = (H_t, \mathcal{A}_t, \mathcal{R}_t, \mathcal{M}_t, T_t, B_t, G_t, E_t, V_t)
$$
where:
Symbol
	Meaning
	(H_t)
	Head/router.
	(\mathcal{A}_t)
	Set of arms/specialists.
	(\mathcal{R}_t)
	Routing policy.
	(\mathcal{M}_t)
	Memory system.
	(T_t)
	Tool registry.
	(B_t)
	Active benchmark frontier.
	(G_t)
	Regression suite.
	(E_t)
	Residual escrow and failure map.
	(V_t)
	Verification and safety layer.
	Given task (x), context (c), budget (q), and risk profile (r), the head selects arms:
$$
A_x = \mathcal{R}_{H_t}(x, c, q, r)
$$
where:
$$
A_x \subseteq \mathcal{A}_t
$$
Each selected arm (A_i) receives scoped context and permissions:
$$
y_i = A_i(x_i, c_i, p_i)
$$
where (p_i) is the permission/resource envelope.
The head composes:
$$
y = H_{\text{compose}}(y_1, y_2, \dots, y_k)
$$
The verifier evaluates:
$$
V_t(y, x, c, r) \rightarrow {\text{accept}, \text{revise}, \text{route more}, \text{fallback}, \text{refuse}}
$$
The ratchet advances when:
$$
P(S_{t+1}, B_t) > P(S_t, B_t) + \epsilon
$$
while:
$$
P(S_{t+1}, G_t) \geq P(S_t, G_t) - \delta
$$
In plain language:
The new system must improve the frontier while preserving prior mastered capability.
________________


4. The Five Pillars
4.1 Compact generative structure
The first pillar is that capability becomes durable when compressed into a structure that can generate, predict, control, or govern behavior.
A compact structure may be:
* a model;
* a tool;
* a policy;
* a benchmark;
* a memory state;
* a schema;
* an arm;
* a router rule;
* an architecture;
* a verifier;
* a reflex controller.
The generic form is:
$$
\mathcal{C} = (S, R, M, \epsilon, V, G)
$$
where:
Symbol
	Meaning
	(S)
	Seed or compact core.
	(R)
	Rule system or expansion process.
	(M)
	Memory or state.
	(\epsilon)
	Residual/error.
	(V)
	Verification.
	(G)
	Generation or governance interface.
	This framing comes from the idea that the best structures do not merely describe. They do work.
________________


4.2 Active compression
The second pillar is active compression.
A model compresses training data into parameters.
An agent compresses experience into memory.
A tool compresses repeated action into procedure.
A policy compresses many possible futures into action.
A benchmark compresses a capability target into a test.
A residual map compresses failures into a diagnostic signal.
RMI treats intelligence as the active transformation of experience into reusable generative structure.
________________


4.3 Cognitive loop closure
The third pillar is loop closure.
A mature AI system should not reason through the same routine indefinitely. Repeated cognition should become procedural memory.
Let successful trajectories be:
$$
\mathcal{L} = {\tau_1, \tau_2, \dots, \tau_n}
$$
A loop closure engine compiles them into a tool:
$$
{\tau_1, \tau_2, \dots, \tau_n} \rightarrow T_\phi(p)
$$
where (p) captures task-specific variation.
The tool is accepted only if:
$$
\operatorname{Verify}(T_\phi) \geq \theta
$$
The trajectory-to-tool move is what lets agents gain skill without hiding everything inside weights.
________________


4.4 Benchmark ratcheting
The fourth pillar is benchmark ratcheting.
Benchmarks are not permanent definitions of intelligence. They are temporary pressure surfaces.
A benchmark begins as frontier.
If mastered, it becomes regression.
If noisy, it is repaired or retired.
If too hard, bridge benchmarks are created.
If public, it is used for calibration but not as the only truth.
HELM’s evaluation philosophy is relevant here because it emphasizes broad coverage, explicit recognition of incompleteness, and multi-metric measurement rather than evaluating only one accuracy score. (Stanford CRFM)
________________


4.5 Octopus routing
The fifth pillar is modular routing.
Instead of forcing every capability into one blob, RMI uses:
* a head/router;
* specialist arms;
* dynamic loading;
* memory routing;
* permission routing;
* local benchmarks;
* local residual escrow;
* head-level composition.
This borrows sparse activation intuition from Mixture-of-Experts systems while moving the idea from neural layers to the system architecture. Switch Transformers, for example, use sparse expert routing to scale model capacity without activating all parameters for every input. (Hugging Face)
RMI generalizes this:
Route tasks to governed specialist systems, not only tokens to expert layers.
________________


5. Architecture Overview
The RMI architecture contains nine major subsystems:
1. Head/router
2. Arm registry
3. Specialist arms
4. Memory router
5. Permission router
6. Tool registry
7. Benchmark and regression ledger
8. Residual escrow ledger
9. Verification and safety layer
A simplified flow:
User / Environment
        ↓
Head Router
        ↓
Task decomposition + risk + budget
        ↓
Arm Registry / Memory Router / Permission Router
        ↓
Dynamically loaded specialist arms
        ↓
Arm outputs + confidence + residuals + provenance
        ↓
Head composition
        ↓
Verification / safety review
        ↓
Response or action
        ↓
Logs update tools, benchmarks, residuals, and routing policy


________________


6. The Head/Router
6.1 Role
The head/router is the coordinating intelligence.
It handles:
* user interaction;
* task interpretation;
* decomposition;
* risk assessment;
* arm selection;
* dynamic loading;
* budget allocation;
* memory routing;
* permission routing;
* output composition;
* safety escalation;
* detecting when no arm is sufficient;
* recommending arm spawn/split/merge/retirement.
The head does not need to be the best specialist in every domain. It needs to know how to allocate specialists.
________________


6.2 Router benchmarks
The router needs its own evaluations.
Metric
	Meaning
	Selection accuracy
	Did it choose the right arm?
	Abstention quality
	Did it avoid routing when no arm fit?
	Cost efficiency
	Did it avoid unnecessary arms?
	Risk routing
	Did high-risk tasks trigger safety arms?
	Composition quality
	Did it faithfully synthesize arm outputs?
	Conflict resolution
	Did it handle disagreement well?
	Latency compliance
	Did it respect time budgets?
	Arm discovery
	Did it detect when a new arm was needed?
	The router should be treated as a first-class model with its own residuals and regression tests.
________________


6.3 Router non-monolith rule
The head must not absorb all domain reasoning.
If the head becomes responsible for everything, the system collapses back into monolithic design.
The head should specialize in:
* routing;
* composition;
* verification orchestration;
* global coherence.
Domain reasoning belongs in arms.
________________


7. Specialist Arms
7.1 Definition
An arm is a bounded specialist subsystem.
An arm may be:
* a small model;
* a domain-tuned model;
* a workflow engine;
* a retrieval system;
* a code executor;
* a verifier;
* a symbolic reasoner;
* a safety monitor;
* a physical controller;
* a tool bundle;
* a hybrid subsystem.
The key property is not implementation type. The key property is bounded, evaluated specialization.
________________


7.2 Arm anatomy
Each arm should have:
Component
	Purpose
	Capability scope
	What the arm handles.
	Input/output schema
	How the head communicates with it.
	Local tools
	APIs, commands, functions, or environments.
	Local memory
	Domain-specific history and state.
	Local benchmark frontier
	Current pressure surface for that arm.
	Regression suite
	Prior capabilities to preserve.
	Residual escrow
	Local unresolved failures.
	Permission boundary
	What the arm can access or change.
	Runtime tier
	Where and how it executes.
	Reliability metrics
	Success, failure, cost, latency.
	Lifecycle status
	Active, probationary, split candidate, stale, retired.
	An arm is not a prompt. It is a governed subsystem.
________________


7.3 Arm examples
Arm
	Scope
	Coding Arm
	Repository analysis, code edits, tests.
	Rust Arm
	Rust compiler errors, Cargo, ownership, lifetimes.
	Research Arm
	Literature mapping, citation support, related work.
	Math Arm
	Derivations, formal calculations, proof checking.
	Data Arm
	Tables, spreadsheets, normalization, analysis.
	Writing Arm
	Structure, tone, public-release polish.
	Skeptic Arm
	Overclaim detection and adversarial critique.
	Safety Arm
	Risk classification, vetoes, permission review.
	Memory Arm
	Retrieval, project history, user preferences.
	Vision Arm
	Image/video interpretation.
	Operations Arm
	Deployments, incidents, monitoring.
	Reflex Arm
	Immediate safety response in hard-latency contexts.
	________________


8. Dynamic Loading and Domain Quarantine
8.1 Dynamic loading
The architecture keeps the head/router loaded and loads arms on demand.
head stays resident
arms load when needed


Benefits:
* lower active memory footprint;
* rare skills can remain cold;
* domain-specific systems can run on specialized hardware;
* sensitive arms can remain isolated;
* one arm can update without retraining the entire system;
* fault containment improves.
________________


8.2 Domain quarantine
Different arms should have different memory and permissions.
Examples:
* Coding Arm can read repositories but cannot send emails.
* Finance Arm can calculate but cannot approve transactions without permission.
* Medical Arm can provide general information but cannot access unrelated personal data.
* Deployment Arm can dry-run but requires approval for production mutation.
* Safety Arm can veto high-risk actions.
Each arm receives a permission envelope:
$$
p_i = (\text{memory}, \text{tools}, \text{runtime}, \text{side effects}, \text{budget}, \text{risk})
$$
The arm operates only inside that envelope.
________________


8.3 Memory routing
Memory should be routed like compute.
Memory type
	Purpose
	Global memory
	User preferences, long-term goals, persistent identity.
	Arm-local memory
	Domain-specific cases, tools, failures, and heuristics.
	Shared task memory
	Temporary workspace for multi-arm collaboration.
	Routing memory
	Which arms worked for which tasks.
	Safety memory
	Incidents, approvals, vetoes, risk history.
	Residual memory
	Unresolved failures and edge cases.
	The principle:
Do not expose all memory to all arms. Route memory by task, permission, and need.
________________


9. Cognitive Loop Closure
9.1 Why loop closure matters
A system that repeats the same reasoning forever is not learning efficiently.
If an arm or the head repeatedly performs the same workflow, it should ask:
Can this become a verified tool?
Examples:
* repository test runner;
* citation audit;
* public whitepaper preparation;
* spreadsheet normalization;
* deployment hold;
* invoice processing;
* prompt-to-eval-suite generator;
* data-cleaning procedure.
________________


9.2 Loop closure pipeline
The loop closure pipeline is:
1. Trajectory logging
2. Loop detection
3. Abstraction
4. Active parameter discovery
5. Tool synthesis
6. Verification
7. Registration
8. Routing
9. Runtime monitoring
10. Revision or retirement
This pipeline prevents naïve automation by requiring verification and lifecycle management.
________________


9.3 Active parameter discovery
Passive abstraction is not enough.
If every observed invoice is in USD, currency may look invariant.
If every observed repository uses npm, package manager may look invariant.
If every observed paper includes references, reference presence may look invariant.
The system must actively probe for hidden parameters.
Methods include:
* historical variance analysis;
* counterfactual replay;
* synthetic case generation;
* adversarial edge-case probing;
* environment interrogation;
* human or supervisory questioning.
Variables should be classified as:
State
	Meaning
	Invariant
	Should not change across valid uses.
	Parameter
	Expected to vary and should be exposed.
	Precondition
	Must hold before execution.
	Unknown assumption
	Suspected dependency requiring more evidence.
	This prevents tools from becoming brittle scripts.
________________


9.4 Tool acceptance rule
A tool should enter the registry only when expected value exceeds lifecycle cost:
$$
F \cdot \Delta C \cdot Q \cdot A
C_T + M_T + R_T + V_T + D_T
$$
where:
Symbol
	Meaning
	(F)
	Expected recurrence frequency.
	(\Delta C)
	Expected cost reduction per use.
	(Q)
	Expected quality or reliability improvement.
	(A)
	Automation appropriateness.
	(C_T)
	Creation cost.
	(M_T)
	Maintenance cost.
	(R_T)
	Risk cost.
	(V_T)
	Verification cost.
	(D_T)
	Drift/depreciation cost.
	This prevents tool bloat.
________________


10. Benchmark Ratcheting
10.1 Benchmark lifecycle
Benchmarks move through statuses:
Status
	Meaning
	Frontier
	Current pressure benchmark.
	Diagnostic
	Explains a failure mode.
	Graduated
	Mastered enough to advance.
	Regression
	Preserves prior capability.
	Public calibration
	Enables apples-to-apples comparison.
	Live
	Refreshes over time.
	Retired
	Too stale, noisy, contaminated, or uninformative.
	A benchmark is useful while it teaches.
________________


10.2 Mastery thresholds
A model or arm does not need 100% on every ordinary benchmark.
Each benchmark (b) has an initial mastery threshold:
$$
\gamma_{0,b}
$$
For many ordinary capability benchmarks, a useful default may be:
$$
\gamma_{0,b} = 0.90
$$
or 90%.
Graduation requires:
$$
P(S_t,b) \geq \gamma_b
$$
but also subgroup and critical-failure checks.
________________


10.3 Time-decayed thresholds
If progress stalls, the threshold may decay toward a floor:
$$
\gamma_b(k)
\max
\left(
\gamma_{\min,b},
\gamma_{0,b} - \eta_b \cdot \max(0, k - p_b)
\right)
$$
where:
Symbol
	Meaning
	(\gamma_b(k))
	Current threshold.
	(\gamma_{0,b})
	Initial threshold.
	(\gamma_{\min,b})
	Minimum floor.
	(k)
	Development cycles spent on benchmark.
	(p_b)
	Patience window before decay.
	(\eta_b)
	Decay rate.
	A cautious policy decays only when improvement stalls:
$$
\Delta_b(k) < \epsilon_b
$$
The purpose is not to lower standards randomly. It is to prevent one benchmark tail from freezing the frontier forever.
________________


10.4 Critical-failure veto
Time-decayed thresholds do not apply to critical safety failures.
Graduation requires:
$$
F_{\text{critical}}(S_t,b)=0
$$
or a domain-specific near-zero bound.
Safety-critical failures include:
* irreversible physical harm;
* security compromise;
* unsafe deployment;
* financial harm;
* medical harm;
* legal violation;
* catastrophic data loss.
________________


10.5 Residual escrow
When a benchmark graduates, unsolved cases enter residual escrow:
$$
E_b = {x \in b \mid S_t(x) \neq y}
$$
Escrow items are:
* tracked;
* clustered;
* periodically reattempted;
* promoted if recurring;
* retired if benchmark-flawed;
* added to regression if solved consistently.
The rule:
Advance at mastery. Preserve the tail. Promote recurring residuals.
________________


11. Public Calibration Track
Internal benchmarks drive progress. Public benchmarks enable comparison.
A mature system should use both.
Track
	Purpose
	Internal frontier
	Drive capability growth.
	Diagnostic
	Explain failures.
	Private holdout
	Test generalization.
	Live benchmark
	Track real-world performance.
	Regression suite
	Preserve mastered capability.
	Residual escrow
	Track unresolved failures.
	Public calibration
	Compare to public reports.
	Public calibration answers:
How do we compare to the field?
Internal frontier benchmarks answer:
What should we improve next?
Both are necessary.
OpenAI’s SWE-bench Verified analysis illustrates why public benchmarks need lifecycle management: a benchmark can be useful, then become less diagnostic as contamination and flawed residual tests dominate. (OpenAI)
________________


12. Intervention Ladder
When performance stalls, RMI escalates carefully.
Level 1 — Benchmark audit
Ask:
* Are labels correct?
* Are tests fair?
* Is the benchmark contaminated?
* Are tasks solvable?
* Does the metric match the capability?
* Does improvement transfer?
Level 2 — Data improvement
Try:
* targeted examples;
* label cleaning;
* curriculum;
* synthetic cases;
* demonstrations;
* better coverage.
Chinchilla-style compute-optimal training showed that some apparent model limits are actually data/training-allocation problems, with model size and training tokens needing to scale together under fixed compute.
Level 3 — Training improvement
Try:
* loss changes;
* optimizer tuning;
* curriculum;
* post-training;
* preference learning;
* reinforcement learning;
* distillation.
Level 4 — Inference improvement
Try:
* retrieval;
* memory;
* search;
* planning;
* test-time compute;
* verifiers;
* tool use;
* decomposition.
Level 5 — Loop closure
If successful workflows repeat, compile them into tools.
Level 6 — Bridge benchmarks
If the next benchmark is too hard, insert an intermediate benchmark.
Level 7 — Architecture change
If data, training, inference, tools, benchmark repair, and bridge benchmarks fail, change architecture.
Architecture should be a hypothesis:
This residual exists because the system lacks mechanism (X). Adding (X) should improve benchmark class (B) while preserving regression suite (G).
________________


13. Reference Cognitive Substrate
RMI does not require one specific model architecture. However, a strong cognitive substrate for RMI may combine five primitives:
Primitive
	Role
	Liquid continuous state
	Streaming temporal memory.
	Reservoir expansion
	Cheap nonlinear temporal basis.
	KAN-style transformations
	Inspectable nonlinear compression and readout.
	HDC/VSA memory
	Explicit compositional binding and symbolic memory.
	Active-inference-style action selection
	Choosing actions, queries, or tools that reduce expected uncertainty.
	Liquid Time-constant Networks provide a basis for continuous-time recurrent dynamics; KANs replace fixed node activations with learnable edge functions; Torchhd describes HDC/VSA as computing with high-dimensional distributed representations; active inference frames perception, planning, action, decision-making, and learning under a generative-model objective. (Hugging Face)
In this paper, that substrate is optional. The central contribution is not any one module. The central contribution is the ratcheting architecture around it.
________________


14. Execution Modes and Safety
14.1 Interpreter mode
Use flexible reasoning when the task is:
* novel;
* ambiguous;
* creative;
* underspecified;
* high-level;
* outside known tool preconditions.
14.2 Compiled-tool mode
Use verified tools when the task is:
* repeated;
* parameterized;
* well-scoped;
* validated by prior tests;
* low or acceptable risk.
14.3 Reflex/failsafe mode
Use immediate safety behavior when:
* latency is hard;
* physical safety is at stake;
* deployment risk is high;
* financial or security containment is needed;
* a tool fails during execution;
* a system approaches a safety boundary.
Runtime verification research studies monitors that evaluate execution traces against formal specifications, and WebAssembly’s security model provides sandboxing and isolation goals for executable modules. These are relevant because RMI tools and arms need runtime boundaries, not merely promises. (Springer)
________________


15. Execution and Runtime Tiers
Tier
	Environment
	Appropriate for
	E0
	Text template
	Low-risk drafting.
	E1
	Structured workflow
	Human-reviewed procedures.
	E2
	Typed deterministic function
	Data transformations, parsing, formatting.
	E3
	Sandboxed runtime
	Generated or untrusted code.
	E4
	Memory-safe systems runtime
	Higher-assurance digital tools.
	E5
	Real-time reflex runtime
	Safety-critical embodied systems.
	Generated tools should run in the least powerful environment sufficient for the task.
Rust is relevant to E4-style systems because its ownership model governs memory management with compiler-checked rules; WebAssembly is relevant to E3-style sandboxing because each module executes in a separated sandboxed environment with explicit security constraints. (WebAssembly)
________________


16. High-Bandwidth Embodied Logging
Embodied systems create high-bandwidth streams:
* 60fps camera feeds;
* lidar;
* IMU;
* motor commands;
* force sensors;
* GPS;
* battery telemetry;
* localization estimates;
* controller states.
A ratcheting embodied system should not feed raw streams directly into loop detection.
It needs hierarchical logging:
Log type
	Purpose
	Raw telemetry
	Replay, debugging, safety analysis.
	Event log
	Obstacle detected, gate passed, slip detected, reflex triggered.
	Semantic trace
	Objects, landmarks, task state, environment labels.
	Skill trace
	Which controller/tool/arm was active.
	Residual log
	Surprises, failures, monitor violations, recovery events.
	The memory budget should satisfy:
$$
B_{\text{raw}} + B_{\text{events}} + B_{\text{features}} + B_{\text{residuals}} \leq B_{\text{budget}}
$$
The goal:
Log enough structure to discover loops, enough detail to debug failures, and enough safety evidence to audit reflex behavior — without storing the entire world.
________________


17. Arm Lifecycle
Specialist arms should evolve.
17.1 Add arms
Spawn a new arm when a recurring domain deserves its own specialist.
Signals:
* repeated routing failures;
* recurring residual cluster;
* high cost from generalist handling;
* new domain demand;
* repeated loop closures in the same domain;
* need for distinct permissions or runtime.
17.2 Split arms
Split an arm when it becomes bloated.
Signals:
* rising latency;
* large internal tool count;
* broad unrelated scope;
* separate residual clusters;
* declining reliability;
* router confusion;
* distinct risk domains.
17.3 Merge arms
Merge arms when specialization adds little value.
Signals:
* overlapping tools;
* same benchmark frontier;
* same memory;
* low usage;
* redundant outputs;
* maintenance cost exceeds value.
17.4 Retire arms
Retire an arm when it is:
* stale;
* unused;
* unsafe;
* superseded;
* failing regression;
* too expensive;
* no longer aligned with user needs.
A healthy modular system adds, splits, merges, and retires. It does not only grow.
________________


18. Ledgers and Registries
18.1 Benchmark ledger
Field
	Meaning
	Benchmark name
	Identifier.
	Capability measured
	What it claims to test.
	Status
	Frontier, diagnostic, graduated, regression, live, public calibration, retired.
	Initial threshold
	Default mastery target.
	Current threshold
	Time-decayed target.
	Floor threshold
	Minimum threshold before diagnosis/bridge.
	Subgroup floors
	Minimum category requirements.
	Critical-failure rules
	Failures that veto graduation.
	Contamination risk
	Low, medium, high.
	Transfer evidence
	Whether progress generalizes.
	Escrow policy
	How failures are tracked.
	Retirement criteria
	When to stop using it.
	18.2 Model/system ledger
Field
	Meaning
	System version
	Identifier.
	Head version
	Router version.
	Arm set
	Active specialists.
	Architecture
	Model/substrate design.
	Data
	Training/post-training data.
	Inference procedure
	Tools, memory, retrieval, search, planning.
	Benchmark scores
	Full portfolio.
	Residual map
	Failure categories.
	Tool registry version
	Procedural memory state.
	Regression status
	Prior capabilities preserved?
	Cost profile
	Training, inference, latency, memory.
	Safety profile
	Risk evaluation.
	Next wall
	Current suspected bottleneck.
	18.3 Tool registry
Field
	Meaning
	Tool name
	Skill identifier.
	Source trajectories
	Prior successful workflows.
	Parameters
	Variable inputs.
	Preconditions
	When it may run.
	Postconditions
	What must hold after execution.
	Verification grade
	Confidence/testing level.
	Runtime tier
	Execution environment.
	Risk tier
	Consequence of failure.
	Usage metrics
	Frequency, success, savings.
	Failure modes
	Known residuals.
	Retirement criteria
	When to disable or revise.
	18.4 Residual escrow ledger
Field
	Meaning
	Residual ID
	Failure identifier.
	Source benchmark/tool/arm
	Where it came from.
	Failure type
	Data, training, inference, tool, benchmark, architecture, safety.
	Cluster
	Related failures.
	Severity
	Low, medium, high, critical.
	Reattempt schedule
	When to retry.
	Recurrence count
	How often it reappears.
	Promotion status
	Escrow, active diagnostic, regression, retired.
	________________


19. Evaluation Metrics
19.1 System metrics
* end-to-end success;
* cost per task;
* latency;
* active memory footprint;
* arms loaded per task;
* public calibration score;
* regression preservation;
* safety incident rate;
* user usefulness;
* residual trend.
19.2 Router metrics
* correct arm selection;
* abstention quality;
* risk routing accuracy;
* composition fidelity;
* conflict resolution quality;
* unnecessary routing rate;
* latency compliance.
19.3 Arm metrics
* local benchmark performance;
* regression preservation;
* residual escrow trend;
* tool success rate;
* memory footprint;
* cost;
* latency;
* bloat index.
19.4 Tool metrics
* recurrence frequency;
* cost savings;
* verification grade;
* failure rate;
* stale-tool rate;
* tool overlap;
* retirement rate.
19.5 Benchmark metrics
* saturation level;
* residual value;
* transfer strength;
* contamination risk;
* public calibration relevance;
* subgroup performance;
* critical failure count.
________________


20. Failure Modes
20.1 Benchmark gaming
The system improves scores without improving real capability.
Mitigations:
* private holdouts;
* live benchmarks;
* benchmark mutation;
* transfer checks;
* capability narratives.
20.2 Tail obsession
The system gets stuck chasing the last 10% of one benchmark forever.
Mitigations:
* time-decayed thresholds;
* residual escrow;
* frontier momentum rule;
* bridge benchmarks.
20.3 Tail erasure
The system advances and forgets unresolved failures.
Mitigations:
* residual escrow ledger;
* recurring reattempts;
* recurrence promotion rule.
20.4 Tool bloat
The system creates too many tools.
Mitigations:
* tool acceptance rule;
* usage metrics;
* consolidation;
* retirement.
20.5 Arm bloat
A specialist becomes a hidden monolith.
Mitigations:
* split thresholds;
* local benchmarks;
* subdomain clustering;
* bloat index.
20.6 Bad routing
The head chooses the wrong specialist.
Mitigations:
* router benchmarks;
* arm confidence;
* verifier arms;
* fallback routing.
20.7 Under-quarantine
Arms access too much.
Mitigations:
* permission envelopes;
* memory routing;
* sandboxing;
* audit logs.
20.8 Over-quarantine
Arms cannot access enough to solve the task.
Mitigations:
* controlled access grants;
* head-mediated retrieval;
* escalation policies.
20.9 Reflex gap
The system assumes it can fall back to reasoning when immediate action is required.
Mitigations:
* reflex/failsafe mode;
* safety monitors;
* emergency stop/hold/land/isolate policies;
* hard runtime constraints.
20.10 Architecture churn
The team changes architecture before diagnosing the wall.
Mitigations:
* intervention ladder;
* residual map;
* benchmark audit;
* ablations.
________________


21. Implementation Roadmap
Phase 1 — Ledgers
Build:
* benchmark ledger;
* model/system ledger;
* residual escrow ledger;
* basic tool registry.
Goal:
Know what exists, what fails, and what is preserved.
Phase 2 — Basic router and arm registry
Create:
* head/router;
* small arm set;
* arm cards;
* input/output schemas;
* permission envelopes.
Goal:
Route tasks to bounded specialists.
Phase 3 — Loop closure
Add:
* trajectory logger;
* loop detector;
* abstraction engine;
* active parameter discovery;
* tool synthesis;
* verifier;
* tool registration.
Goal:
Convert repeated success into procedural memory.
Phase 4 — Benchmark ratchet
Add:
* mastery thresholds;
* time-decay policy;
* subgroup floors;
* critical-failure vetoes;
* residual escrow;
* regression promotion.
Goal:
Move the frontier while preserving the floor.
Phase 5 — Public calibration
Run public benchmarks periodically with standardized settings.
Report:
* score;
* cost;
* latency;
* tool use;
* inference setup;
* safety notes.
Goal:
Compare externally without overfitting public benchmarks.
Phase 6 — Arm ratchets
Give each arm:
* local benchmark frontier;
* local regression suite;
* local residual escrow;
* local improvement process.
Goal:
Improve specialists independently.
Phase 7 — Safety/runtime tiers
Add:
* execution tiers;
* risk tiers;
* sandboxing;
* runtime verification;
* reflex/failsafe layer;
* human approval gates.
Goal:
Prevent modular capability from becoming unsafe autonomy.
Phase 8 — Arm lifecycle management
Add:
* spawn rules;
* split rules;
* merge rules;
* retirement policy;
* bloat metrics.
Goal:
Keep the modular ecosystem healthy.
________________


22. Claims and Non-Claims
22.1 Claims
This paper claims:
1. AI systems should grow through a ratchet of benchmark pressure, residual analysis, loop closure, modular routing, verification, and frontier expansion.
2. Benchmarks should be treated as temporary pressure surfaces, not permanent definitions of intelligence.
3. Ordinary benchmarks need mastery thresholds and residual escrow, not automatic 100% requirements.
4. Repeated successful trajectories should become verified tools when valuable, parameterizable, and safe.
5. Capability can scale through modular organization, not only through monolithic parameter growth.
6. A head/router plus specialist arms enables dynamic loading, domain quarantine, independent ratcheting, and better diagnostics.
7. Architecture changes should be motivated by residuals after simpler interventions fail.
8. Public benchmarks are necessary for calibration but insufficient as the sole internal development target.
9. Mature AI systems need three execution modes: interpreter, compiled-tool, and reflex/failsafe.
10. Capabilities become durable when they are measured, proceduralized, verified, registered, routed, and protected against regression.
22.2 Non-claims
This paper does not claim:
1. Monolithic models are obsolete.
2. Benchmarks perfectly measure intelligence.
3. Higher benchmark scores always imply real-world improvement.
4. Every repeated action should become a tool.
5. Tools should replace reasoning.
6. Fine-tuning or scaling are obsolete.
7. Verification is absolute in open worlds.
8. Time-decayed thresholds are acceptable for safety-critical failures.
9. Routing is easy.
10. More arms always improve the system.
11. Human judgment is unnecessary.
12. One architecture fits every deployment.
This framework is a development methodology and systems architecture, not a complete theory of intelligence.
________________


23. Conclusion
Ratcheting Modular Intelligence proposes a unified way to build AI systems that grow without becoming ungovernable blobs.
The system begins with pressure.
A benchmark exposes what the system cannot yet do.
The head routes tasks to arms.
Arms attempt subtasks.
Repeated successes become tools.
Failures become residuals.
Residuals diagnose the wall.
Benchmarks graduate into regression.
Unsolved cases enter escrow.
Specialists improve independently.
Bloated specialists split.
Stale specialists retire.
The public calibration track keeps the system comparable.
The safety layer keeps the system bounded.
The frontier moves.
The floor holds.
pressure
    ↓
attempt
    ↓
residual
    ↓
procedure
    ↓
verification
    ↓
module
    ↓
regression
    ↓
frontier


The best AI systems will not merely become larger.
They will become better organized.
They will know when to reason, when to execute, and when to reflex.
They will know when a benchmark has taught enough.
They will preserve the failures that still matter.
They will turn repeated behavior into tools.
They will turn tools into procedural memory.
They will turn specialists into modular capability.
They will turn residuals into architecture signals.
They will turn benchmarks into curriculum.
The ratchet turns when yesterday’s frontier becomes today’s floor.
That is Ratcheting Modular Intelligence.
________________


Appendix A — One-Paragraph Public Summary
Ratcheting Modular Intelligence is a framework for AI systems that improve by turning benchmark pressure, repeated behavior, and residual failures into verified modular capability. A lightweight head/router coordinates specialist arms, each with local tools, memory, benchmarks, permissions, and residuals. Repeated successful trajectories become verified tools. Mastered benchmarks become regression tests. Unsolved cases enter residual escrow. Public benchmarks provide calibration, while private/live benchmarks drive internal progress. The system improves through an intervention ladder: benchmark audit, data, training, inference, loop closure, bridge benchmarks, and architecture change. The result is one coherent agent made of many bounded specialists that ratchet upward over time.
________________


Appendix B — Compact Manifesto
Do not worship benchmarks.
Use them.
Let them apply pressure.
When they stop teaching, promote them to regression.
Do not demand perfection from every benchmark.
Graduate at mastery.
Preserve the tail.
If the tail repeats, promote it.
If behavior repeats, compile it.
If the tool works, verify it.
If the tool fails, expose the residual.
If an arm bloats, split it.
If an arm overlaps, merge it.
If an arm grows stale, retire it.
If the task is novel, reason.
If the loop is closed, execute.
If safety is at stake and time is short, reflex.
The user sees one agent.
Inside, the specialists get to work.
The frontier must move.
The floor must hold.
The ratchet must turn.
________________


Selected References
1. Stanford CRFM, Holistic Evaluation of Language Models / HELM. (Stanford CRFM)
2. Hoffmann et al., Training Compute-Optimal Large Language Models.
3. Center for AI Safety, Scale AI, and collaborators, Humanity’s Last Exam. (Live Science)
4. OpenAI, Why SWE-bench Verified no longer measures frontier coding capabilities. (OpenAI)
5. METR, Task-Completion Time Horizons of Frontier AI Models. (Metr)
6. Shazeer et al., Sparsely-Gated Mixture-of-Experts. (Hugging Face)
7. Fedus, Zoph, and Shazeer, Switch Transformers. (Hugging Face)
8. Schick et al., Toolformer. (Hugging Face)
9. Wang et al., Voyager. (Hugging Face)
10. Hasani et al., Liquid Time-constant Networks. (Hugging Face)
11. Liu et al., KAN: Kolmogorov-Arnold Networks. (Hugging Face)
12. Heddes et al., Torchhd: HDC/VSA Library. (Journal of Machine Learning Research)
13. Da Costa et al., Active inference on discrete state-spaces. (ScienceDirect)
14. Olson, Schulz, and Ragsdale, Neuronal segmentation in cephalopod arms. (Nature)
15. WebAssembly Project, Security model and sandboxing documentation. (WebAssembly)
16. Sánchez et al., Runtime verification from advanced application domains. (Springer)