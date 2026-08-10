Tab 1
Cognitive Compilation: Turning LLMs into a Compiler for Plans, Semantics, and Artifacts
Abstract
Large language models are powerful generators, but “generate-from-a-prompt” workflows are structurally brittle: they blur requirements with implementation, drift over long contexts, serialize work that could be parallel, and apply expensive reasoning capacity to trivial steps. This paper proposes a compilation paradigm for generative systems: treat a user’s intent as source, compile it into a typed semantic intermediate representation (IR), optimize it as a dependency graph, and then target-specific “backends” lower the IR into executable artifacts (code, stories, songs, slide decks, etc.). The architecture separates (1) Plan Formation, (2) Semantic Compilation, and (3) Target Compilation, enabling deterministic validation, scalable parallelism, and intelligence arbitrage (routing each atomic unit to the cheapest worker/model/tool that can reliably complete it). We define the core representations, compilation passes, scheduling strategy, verification loops, and an implementation sketch, along with an evaluation plan.
________________


1. Motivation: Why a “compiler” framing helps
1.1 The failure modes of direct generation
When a system tries to produce a complex artifact directly from a conversational prompt, four recurring issues appear:
1. Requirement–implementation entanglement
The model invents details prematurely (data structures, plot devices, APIs), then later contradicts them.
2. State drift
Long-horizon constraints (invariants, tone, rules, interfaces) degrade as generation continues.
3. Linearity trap
Many subtasks are independent (research, outline, naming, testing, formatting), but they’re done sequentially because the “one model writing one stream” metaphor forces serialization.
4. Uniformity fallacy
The same expensive reasoning process is used for everything—from architecture decisions down to formatting bullet points.
1.2 The compiler alternative
Traditional compilers succeed because they:
   * separate front-end analysis from back-end synthesis,
   * preserve meaning using an intermediate representation,
   * run validation early (type checking, control-flow checks),
   * apply optimizations (including scheduling and resource usage),
   * target multiple outputs from the same IR.
The central claim of this paper is:
Treating generative work as compilation—rather than freeform generation—creates a stable substrate for validation, parallelism, and cost control across many output modalities.
________________


2. System overview
We define a three-stage pipeline:
   1. Plan Formation
Produce a precise, inspectable “source plan” that captures intent, constraints, and acceptance criteria.
   2. Semantic Compilation
Compile the plan into a Semantic IR: a typed tree/graph of atomic semantic units with explicit dependencies.
   3. Target Compilation
Select a backend (code, story, song, etc.) that lowers the Semantic IR into a Target IR and finally renders the artifact.
2.1 High-level diagram
User Intent
   │
   ▼
[Stage 1] Plan Formation
   └─ outputs: Source Plan (structured)
           │
           ▼
[Stage 2] Semantic Compilation
   ├─ parse + normalize
   ├─ typecheck + constraint checks
   ├─ build dependency DAG
   └─ outputs: Semantic IR (typed task tree/DAG)
           │
           ▼
[Stage 3] Target Compilation (Backend)
   ├─ lower Semantic IR → Target IR
   ├─ generate artifact atoms (code blocks / scenes / verses)
   ├─ validate (tests, lint, continuity checks)
   └─ outputs: Final Artifact + Trace Bundle


________________


3. Stage 1: Plan Formation (the “source language”)
Plan Formation converts conversation into a stable Source Plan that is explicit enough to compile.
3.1 The Source Plan contract
A Source Plan should minimally include:
      * Goal: what is being produced and for whom
      * Inputs: expected inputs and their shapes
      * Outputs: expected outputs and their shapes
      * Constraints: hard and soft requirements
      * Acceptance tests: what “done” means
      * Non-goals: what is explicitly out of scope
      * Resources: time/budget limits, allowed tools, allowed libraries, style requirements
      * Risk flags: what requires extra verification or human approval
3.2 Recommended representation: structured text + schema
Natural language remains useful, but compilation benefits from structure. A practical approach is:
      * human-readable YAML/Markdown for authoring,
      * machine-validated JSON schema for enforcement.
Example (abbreviated):
goal:
  produce: "Python CLI app"
  purpose: "Manage a todo list stored on disk"
inputs:
  - name: "commands"
    shape: "CLI args"
outputs:
  - name: "todo_state"
    shape: "json file"
constraints:
  hard:
    - "Works offline"
    - "No external database"
  soft:
    - "Fast startup"
acceptance_tests:
  - "add/list/done/remove commands work"
  - "invalid input yields helpful error"
non_goals:
  - "sync across devices"


3.3 Multi-model / multi-agent plan stabilization (optional, but powerful)
You can use one model or many, but the key is: end the stage with a locked plan. The system should explicitly mark the plan as either:
      * READY_TO_COMPILE, or
      * BLOCKED with a list of missing decisions.
3.4 Output of Stage 1
      * Source Plan (structured)
      * Decision log (why key choices were made)
      * Open questions (must be resolved before compilation)
________________


4. Stage 2: Semantic Compilation (the Semantic IR)
Semantic Compilation is the critical idea: take the Source Plan and produce a semantic tree/DAG of atomic meaning-preserving units.
4.1 What is a “semantic atom”?
A semantic atom is the smallest unit of intent you want to preserve across outputs.
Examples of semantic atoms (target-agnostic):
      * DEFINE_ENTITY(name="Task", fields=[...])
      * CONSTRAINT(type="uniqueness", target="task.id")
      * TRANSFORM(input="raw_text", output="clean_text", method="strip_html")
      * DECIDE(strategy="store_on_disk", format="json")
      * VALIDATE(condition="file is writable")
      * ORDER(step="load", before="modify")
      * STYLE(tone="formal", voice="second_person") (for narrative outputs)
A good semantic atom:
      * has a type,
      * declares inputs/outputs,
      * declares preconditions and effects (even if informal),
      * is independently verifiable (at least partially),
      * composes cleanly with others.
4.2 The Semantic IR data model
A workable Semantic IR is a typed DAG:
      * Nodes: semantic atoms with schemas
      * Edges: dependencies (data, ordering, or constraint)
      * Annotations: priority, stakes, required capability, estimated cost
Minimal node schema:
{
  "id": "n42",
  "op": "DEFINE_INTERFACE",
  "inputs": [{"name":"commands","type":"CLIArgs"}],
  "outputs": [{"name":"result","type":"ExitCode"}],
  "constraints": ["must_be_deterministic"],
  "depends_on": ["n12","n19"],
  "capability_required": "procedural_reasoning",
  "stakes": "medium"
}


4.3 Compilation passes (front-end style)
Semantic compilation is best implemented as multiple passes:
Pass A — Extraction
      * Identify entities, actions, constraints, acceptance tests.
      * Convert narrative requirements into structured clauses.
Pass B — Normalization
      * Resolve synonyms into canonical ops (make, build, create → CONSTRUCT).
      * Factor repeated constraints into shared nodes.
      * Turn vague statements into explicit questions or explicit assumptions.
Pass C — Typing
      * Assign types to inputs/outputs and enforce compatibility.
      * Example: if Step i outputs CSV, but Step i+1 expects JSON, insert a CONVERT(CSV→JSON) or raise an error.
Pass D — Dependency construction
      * Build edges based on:
      * data needs (this step consumes that output),
      * ordering constraints (must happen before),
      * shared resources (must not run concurrently),
      * acceptance-test dependencies (tests depend on implementations).
Pass E — Semantic linting
      * Detect:
      * missing acceptance tests,
      * orphan nodes (no path to outputs),
      * circular dependencies,
      * ambiguous nodes (insufficient specification),
      * conflicting constraints.
4.4 Compile-time errors vs warnings
A key benefit of this architecture is compiler-like feedback:
      * Errors (block compilation)
      * contradictory hard constraints
      * missing required input/output shape definition
      * unresolved ambiguities in mission-critical nodes
      * Warnings (allow, but record)
      * soft constraint conflicts
      * optional decisions deferred
      * low confidence in extracted intent
4.5 Output of Stage 2
      * Semantic IR DAG
      * Constraint report (what was checked, what failed)
      * Optimization-ready execution graph (same DAG plus cost/capability metadata)
________________


5. Stage 3: Target Compilation (backends)
Target compilation turns Semantic IR into a Target IR and then a final artifact.
5.1 Backend interface
A backend is a module implementing:
      1. Lowering rules: map semantic ops → target constructs
      2. Target IR: a representation closer to the artifact domain
      3. Rendering: produce the final output
      4. Target validation: check artifact correctness
Abstract interface:
Backend:
  lower(semantic_ir) -> target_ir
  optimize(target_ir) -> target_ir
  render(target_ir) -> artifact
  validate(artifact, trace) -> validation_report


5.2 Example backends
Code backend
      * Semantic atoms lower into:
      * modules, classes, functions, tests, configs
      * Target IR could be:
      * file tree + AST fragments + build/test graph
      * Validation:
      * type check, lint, unit tests, static analysis
Story backend
      * Semantic atoms lower into:
      * characters, settings, beats, scenes, arcs
      * Target IR:
      * outline tree (Act → Chapter → Scene → Beat)
      * continuity ledger (character states, facts)
      * Validation:
      * continuity checks, constraint checks, tone/style checks
Song backend
      * Semantic atoms lower into:
      * theme, sections (verse/chorus/bridge), rhyme scheme, meter, chord progression notes
      * Validation:
      * meter/rhyme constraints, repeated motif checks, section structure rules
5.3 “Atomic target decomposition”
Your idea includes an “atomic compiler” that can emit any artifact by decomposing the semantic tree into final atomic steps. This is best modeled as:
      * Semantic atoms are universal.
      * Each backend defines target atoms.
Examples:
      * Code target atoms: WRITE_FILE, INSERT_FUNCTION, GENERATE_TEST, RUN_TESTS
      * Story target atoms: WRITE_SCENE, REVISE_FOR_TONE, CHECK_CONTINUITY
      * Song target atoms: WRITE_CHORUS, CHECK_RHYME, ADJUST_METER
The atomic compiler is essentially:
      * a lowering engine + scheduler + validator loop.
________________


6. Parallelism and intelligence arbitrage
This is where the compiler framing becomes economically decisive.
6.1 Convert the Semantic IR into an execution DAG
We already have a dependency graph; now we annotate it with:
      * estimated time
      * estimated token/compute cost
      * required capability
      * risk/stakes
      * retry policy
6.2 Scheduling: critical path + slack exploitation
A practical scheduler can:
      1. Compute the critical path (longest dependency chain).
      2. Assign high-speed/high-reliability resources to nodes on the critical path.
      3. Assign lower-cost resources to nodes with slack (non-critical).
This is the compilation analogue of:
      * instruction scheduling
      * resource-aware build systems
      * distributed task execution
6.3 Capability classes (for routing)
Instead of “always use the best model,” define worker classes:
      * Deterministic tools: parsers, formatters, linters, compilers, regex, template engines
      * Low-cost models: classification, extraction, rewriting, formatting
      * Mid-tier models: summarization, routine drafting, moderate reasoning
      * High-tier models: architecture, novel synthesis, complex debugging, ambiguous intent resolution
      * Human review (optional but important for high-stakes gates)
6.4 A simple routing heuristic
For each node, compute a Minimum Viable Capability (MVC) score:
      * Complexity signals:
      * branching factor in the IR subtree
      * number of constraints touched
      * novelty (no cached precedent)
      * failure history (how often it needed repair)
      * stakes level
Then route:
      * low MVC → deterministic or cheap worker
      * high MVC → strong reasoning worker
      * repeated failure → escalate capability class
      * high stakes → add verifier/human gate
6.5 Caching and common-subtree elimination
Compilation enables classic optimizations:
      * Memoize results of identical semantic atoms
      * Deduplicate repeated sub-plans
      * Reuse verified target fragments (e.g., stable modules, stable scenes)
      * Incremental compilation: when the plan changes, only recompile impacted subgraphs
________________


7. Verification: “compile-time” and “runtime” for generative work
A compiler is only as good as its correctness checks.
7.1 Verification layers
      1. Semantic verification (pre-backend)
      * constraint satisfaction
      * type/shape compatibility
      * completeness (all acceptance tests mapped to nodes)
      2. Target verification
      * code: tests/lint/build
      * narrative: continuity + constraints + outline adherence
      * song: structure + rhyme/meter constraints
      3. Trace verification
      * ensure every artifact segment maps back to Semantic IR nodes
      * enable “why is this here?” queries
7.2 Repair loops as first-class
Instead of “regenerate everything,” compile with repair:
      * If node n fails validation:
      * re-run only the affected region (subgraph slice)
      * optionally escalate worker capability
      * preserve verified siblings
      * keep a failure fingerprint so the system learns which constraints were violated
This is the generative equivalent of:
      * incremental recompilation
      * localized optimization passes
________________


8. Security and robustness considerations
Even for non-adversarial use, compilation pipelines are vulnerable to “instruction smuggling” and uncontrolled tool calls.
Baseline precautions:
      * Treat external sources as data, not instructions.
      * Enforce tool permissions per node (least privilege).
      * Separate “planner” context from “executor” context (avoid leaking irrelevant sensitive material).
      * Maintain an append-only log of:
      * plan versions
      * IR versions
      * node outputs
      * validation results
This makes the system debuggable and supports rollback.
________________


9. Implementation sketch
9.1 Components
A minimal implementation can be structured as:
      * Planner: produces Source Plan
      * Semantic Compiler:
      * parser/extractor
      * normalizer
      * typer + constraint checker
      * DAG builder
      * Optimizer/Scheduler:
      * cost model
      * critical path analyzer
      * router (intelligence arbitrage)
      * Backends:
      * code backend
      * story backend
      * song backend
      * Verifier:
      * generic contract validator
      * backend-specific validators
      * Trace Bundle writer:
      * maps artifact fragments ↔ IR nodes
9.2 Pseudocode (end-to-end)
def compile_intent(user_dialogue, target):
    source_plan = plan_formation(user_dialogue)
    assert source_plan.status == "READY_TO_COMPILE"


    semantic_ir = semantic_compile(source_plan)
    semantic_report = semantic_verify(semantic_ir)
    if semantic_report.blocking_errors:
        return CompileError(semantic_report)


    exec_graph = annotate_for_execution(semantic_ir)
    schedule = build_schedule(exec_graph)


    backend = select_backend(target)
    target_ir = backend.lower(semantic_ir)
    target_ir = backend.optimize(target_ir)


    artifact, trace = backend.render(target_ir, schedule)
    validation = backend.validate(artifact, trace)


    if not validation.pass_:
        artifact, trace = repair_loop(semantic_ir, target_ir, validation)


    return artifact, trace, validation


9.3 What makes this “compiler-like” in practice
      * You can print the Semantic IR like an AST.
      * You can run “lint” passes before generating anything expensive.
      * You can target multiple outputs by swapping backends.
      * You can parallelize execution on the DAG.
      * You can treat failures as localized recompilations.
________________


10. Evaluation plan
To evaluate whether this approach is truly better than direct generation, measure:
10.1 Quality and correctness
      * Semantic fidelity: do outputs match the plan constraints?
      * Consistency: contradiction rate across long outputs
      * Acceptance test pass rate (for code outputs)
10.2 Efficiency
      * Wall-clock latency (with and without parallelism)
      * Compute cost (token usage / tool usage)
      * Retry rate (regen loops per accepted node)
10.3 Debuggability
      * Time to locate failure cause (via trace bundle)
      * Percentage of failures localized to a subgraph vs global rewrites
10.4 Ablations
Compare:
      * direct generation
      * plan-only (no semantic IR)
      * semantic IR without scheduling
      * semantic IR + scheduling + intelligence routing
________________


11. Limitations and open problems
This architecture doesn’t magically remove uncertainty; it moves uncertainty to explicit interfaces:
      * Semantic extraction can be wrong → mitigate with typed schemas, ambiguity flags, and compile-time questions.
      * Some domains have weak validators (e.g., “is this story good?”) → mitigate with measurable proxies and human gates for taste.
      * Over-atomization can create overhead → mitigate with chunking heuristics (atoms must be small enough to verify, but large enough to be efficient).
      * Backends require real design effort → but once built, they amortize across many projects.
________________


12. Conclusion
A generative “compiler” reframes LLMs from monolithic authors into components of a deterministic pipeline:
      * Plan Formation produces a stable source specification.
      * Semantic Compilation converts intent into a typed, verifiable semantic DAG.
      * Target Compilation lowers semantics into modality-specific structures and renders artifacts with validators.
This yields three practical advantages:
      1. Coherence improves because semantics are locked before rendering.
      2. Parallelism becomes natural because the plan is a dependency graph, not a token stream.
      3. Cost control becomes systematic through intelligence arbitrage: route each semantic atom to the cheapest worker that can reliably complete it.
If you want, I can follow this paper with one of these concrete next artifacts (still standalone, no cross-references):
      * a formal JSON schema for the Semantic IR + node typing rules,
      * a worked example that compiles one Source Plan into (a) Python code and (b) a short story using the same Semantic IR,
      * a scheduling/routing spec (critical path + MVC scoring + escalation policy),
      * or a minimal “backend interface” spec that makes adding new targets (slides, emails, lesson plans) straightforward.


Tab 2


Cognitive Compilation: A Compiler Architecture for LLM-Centered Planning, Semantic IR, and Multi-Target Artifact Generation
Abstract
Large language models (LLMs) enable rapid drafting and problem-solving, but end-to-end “prompt → artifact” generation remains brittle for complex tasks: requirements blur into implementation, long-horizon constraints drift, independent subtasks are needlessly serialized, and expensive reasoning capacity is wasted on trivial work. This paper proposes Cognitive Compilation, a compiler-inspired architecture that treats user intent as a source program and transforms it through staged representations: (1) Plan Formation produces a structured, checkable specification; (2) Semantic Compilation converts the plan into a typed Semantic Intermediate Representation (S-IR) expressed as a dependency DAG of semantic atoms; and (3) Target Compilation lowers S-IR into a Target IR for a chosen output domain (code, story, song, slides), then renders artifacts with domain-specific validators. The approach enables deterministic checks (types/constraints), parallel scheduling on the DAG, cost control via intelligence arbitrage (routing each node to the minimum viable worker/model/tool), incremental recompilation, and localized repair loops. We provide a formalization of semantic atoms and compilation passes, describe scheduling and verification strategies, and present an end-to-end walkthrough compiling one plan into both a code skeleton and a narrative outline. We conclude with an evaluation protocol, baseline comparisons, and key open problems.
________________


1. Introduction
LLMs are increasingly used as “general-purpose generators” for software, documents, and creative artifacts. Yet as tasks become multi-step and high-stakes, direct generation exhibits persistent failure modes:
      * Requirement–implementation entanglement: early guesses harden into constraints later contradicted.
      * State drift: invariants degrade over long outputs (interfaces, style, assumptions).
      * Linearity trap: independent work (research, outline, tests, formatting) is executed sequentially.
      * Uniformity fallacy: the same expensive model is applied to everything, including glue work.
Traditional compilers succeed in complex translation by separating analysis from synthesis using stable intermediate representations (IRs), enabling early validation, optimization, and multi-target backends. This paper argues that many LLM workflow failures are structural, and that compiler architecture offers a practical blueprint.
Core thesis: Treat complex generative work as a compilation pipeline: (a) lock intent into a structured plan, (b) compile to a typed semantic DAG, (c) lower to target-specific representations and render with validators.
________________


2. Contributions
This paper contributes:
      1. A three-stage cognitive compiler architecture: Plan → Semantic IR → Target IR → Artifact.
      2. A representation of tasks as typed semantic atoms with explicit inputs/outputs/constraints.
      3. A set of compiler-style passes for extraction, normalization, typing, dependency analysis, and linting.
      4. A scheduling method using critical path + slack exploitation, enabling parallelism and intelligence arbitrage.
      5. A repair strategy based on localized recompilation rather than global regeneration.
      6. A worked end-to-end walkthrough compiling one plan into both a code artifact and a story artifact.
      7. An evaluation plan with datasets, baselines, metrics, and ablations.
________________


3. Related work
Cognitive Compilation sits at the intersection of (i) prompting-as-reasoning, (ii) tool-augmented agents, (iii) pipeline “compilers” for LLM calls, and (iv) literal compilers and intermediate representations.
3.1 Prompting frameworks as search over intermediate “thoughts”
Chain-of-Thought prompting demonstrated that encouraging intermediate reasoning steps can improve multi-step performance. (Emergent Mind) Tree-of-Thoughts generalizes this to exploring multiple reasoning branches with lookahead/backtracking, which conceptually resembles search in an implicit reasoning tree. (DBLP) Graph-of-Thoughts makes the dependency structure explicit as a graph of “thought units,” moving closer to a computational graph perspective. (DBLP)
Difference: These methods improve inference-time reasoning structure, but do not typically define a typed, target-agnostic semantic IR with compiler-like validation passes and multi-backend lowering.
3.2 Tool and agent frameworks: reasoning + acting + reflection
ReAct interleaves reasoning traces and tool actions. (Emergent Mind) Reflexion adds self-feedback via verbal reflection and episodic memory to improve agents across trials. (scixplorer.org) Toolformer studies how models can learn when/how to call tools. (scixplorer.org) ReWOO decouples reasoning from observations to improve efficiency and reduce repeated prompting overhead. (Microsoft) Multi-agent systems like AutoGen provide infrastructure for agent conversations and tool use at scale. (Microsoft)
Difference: Cognitive Compilation treats agent actions as lowering and execution steps derived from a semantic DAG, with explicit compilation artifacts (IRs, traces, validators) and incremental recompilation.
3.3 “Compiling” LLM pipelines
DSPy frames LLM programs as declarative modules and introduces a compiler that optimizes prompting/bootstrapping to maximize a metric. (Emergent Mind)
Difference: DSPy compiles LM-call graphs for performance; Cognitive Compilation compiles intent into a typed semantic DAG, then lowers to multiple target domains (code/story/song) with domain validators.
3.4 LLMs and literal compilers / intermediate representations
Several lines of work explore LLMs interacting with classical compilation artifacts:
      * “Language Models as Compilers” (Think-and-Execute) uses task-level pseudocode and simulated execution to improve algorithmic reasoning. (ACL Anthology)
      * Research on whether LLMs understand compiler IR suggests strengths in syntax/structure but weaknesses in precise instruction-level control-flow reasoning. (Proceedings of Machine Learning Research)
      * Work on injecting compiler semantics into LLMs for translation (e.g., C→x86) investigates using compiler-informed preprocessing/training to improve behavioral accuracy. (ACL Anthology)
      * Meta’s LLM Compiler models focus on LLVM-IR/assembly understanding for optimization and code size reduction. (DBLP)
Difference: Those works primarily treat “compiler” literally (IR/assembly/pseudocode execution). Cognitive Compilation uses the compiler metaphor at the workflow architecture level: compiling natural-language intent into semantic IR for multi-target artifact manufacturing.
________________


4. Architecture overview
4.1 Three stages
      1. Plan Formation
Convert conversation into a structured Source Plan with explicit constraints and acceptance tests.
      2. Semantic Compilation
Compile Source Plan into S-IR: a typed DAG of semantic atoms with dependencies and constraints.
      3. Target Compilation
Choose a backend and lower S-IR into T-IR, then render an artifact with validators and repair loops.
4.2 Why a DAG (not just a tree)
Many real plans contain shared prerequisites and cross-cutting constraints (“logging,” “tone,” “safety,” “format”). DAGs represent reuse and parallelism more naturally than trees.
________________


5. Representations
5.1 Source Plan (the “source language”)
A Source Plan is a structured specification:
         * Goal + audience
         * Inputs/outputs + shapes
         * Hard/soft constraints
         * Acceptance criteria (tests)
         * Non-goals
         * Risk/stakes flags
         * Allowed tools/libraries/resources
Example (minimal, corrected indentation):
goal:
  produce: "Python CLI todo app"
  audience: "single user"
inputs:
  - name: "cli_args"
    shape: "argv"
outputs:
  - name: "todo_state"
    shape: "json file"
constraints:
  hard:
    - "Works offline"
    - "No external database"
  soft:
    - "Fast startup"
acceptance_tests:
  - "add/list/done/remove commands work"
  - "invalid input yields helpful error"
non_goals:
  - "sync across devices"


5.2 Semantic IR (S-IR)
S-IR is a typed DAG where nodes are semantic atoms. Each atom:
         * declares typed inputs/outputs,
         * declares constraints/preconditions,
         * declares effects (what it guarantees),
         * is independently verifiable to some degree,
         * can be routed to different workers.
Minimal S-IR node schema:
{
  "id": "n42",
  "op": "DEFINE_INTERFACE",
  "inputs": [{"name":"cli_args","type":"CLIArgs"}],
  "outputs": [{"name":"command","type":"Command"}],
  "constraints": ["deterministic", "offline"],
  "depends_on": ["n10","n11"],
  "stakes": "medium",
  "capability_required": "procedural_reasoning"
}


5.3 Target IR (T-IR)
Each backend defines its own T-IR closer to its domain:
         * Code T-IR: file tree + AST fragments + build/test graph.
         * Story T-IR: acts → scenes → beats + continuity ledger.
         * Song T-IR: sections + rhyme/meter constraints + motif ledger.
________________


6. Semantic compilation passes
6.1 Pass A: Extraction
Extract entities, actions, constraints, acceptance tests from Source Plan into candidate atoms.
6.2 Pass B: Normalization
Canonicalize ops and merge duplicates:
         * “create/construct/build” → CONSTRUCT
         * repeated constraints become shared constraint nodes
         * implicit assumptions become explicit ASSUME atoms with flags
6.3 Pass C: Typing and shape checking
Assign types and enforce compatibility; insert adapters if needed (CONVERT(JSON→CSV)).
6.4 Pass D: Dependency analysis
Build edges based on:
         * data dependencies (consumes an output),
         * ordering constraints (“must happen before”),
         * resource constraints (mutual exclusion),
         * test dependencies (tests depend on implementations).
6.5 Pass E: Semantic linting
Detect:
         * orphan nodes (no path to outputs),
         * missing acceptance tests,
         * cycles,
         * conflicting hard constraints,
         * ambiguous atoms (underspecified).
Compiler feedback model
         * Errors block target compilation (e.g., contradictory hard constraints).
         * Warnings proceed but are recorded (e.g., soft constraint conflicts, low-confidence extraction).
________________


7. Scheduling, parallelism, and intelligence arbitrage
7.1 Minimum Viable Capability (MVC)
Define MVC as the cheapest worker class capable of meeting reliability thresholds for a node.
Example worker classes:
         * deterministic tools (parsers, formatters, linters),
         * low-cost LMs (rewrite/extract),
         * mid-tier LMs (routine drafting),
         * high-tier LMs (architecture, hard reasoning),
         * human gate (high-stakes approvals).
7.2 Critical path scheduling + slack exploitation
Compute the critical path of the DAG. Assign:
         * high-speed/high-reliability workers to critical nodes,
         * cheaper workers to slack nodes,
         * escalate capability only on failure.
This yields both lower latency (parallelism) and lower cost (arbitrage).
7.3 Incremental compilation and caching
Because intent is compiled into stable IR:
         * identical atoms can be memoized,
         * subgraphs can be reused across targets,
         * when the plan changes, only impacted nodes are recompiled.
________________


8. Verification and repair
8.1 Verification layers
         1. Semantic verification: types + constraint satisfaction + coverage (“every acceptance test maps to nodes”).
         2. Target verification:
         * code: tests/lint/typecheck,
         * story: continuity + constraint checks,
         * song: meter/rhyme/structure checks.
         3. Trace verification: every artifact fragment maps to a node.
8.2 Localized repair loop (recompile a slice, not the world)
When validation fails:
         * identify failing nodes via trace,
         * re-run only the dependent slice,
         * optionally escalate MVC,
         * preserve verified siblings.
This resembles incremental recompilation rather than “regenerate everything.”
________________


9. End-to-end walkthrough (one plan → two targets)
9.1 Source Plan (example)
Goal: “Produce a short onboarding artifact that includes (a) a tiny working CLI todo app skeleton and (b) a narrative explanation for beginners.”
Constraints:
         * offline
         * minimal dependencies
         * beginner-friendly tone
Acceptance tests:
         * code runs
         * narrative matches code behavior
9.2 Compiled S-IR (abridged)
Nodes:
            * n1 DEFINE_DOMAIN_CONCEPT(Task, fields=[id,text,done])
            * n2 DEFINE_STORAGE(format=json, path="todo.json")
            * n3 DEFINE_COMMANDS(add,list,done,remove)
            * n4 DEFINE_CLI_INTERFACE(argv→Command)
            * n5 IMPLEMENT_COMMAND(add)
            * n6 IMPLEMENT_COMMAND(list)
            * n7 IMPLEMENT_COMMAND(done)
            * n8 IMPLEMENT_COMMAND(remove)
            * n9 VALIDATE_IO(file_read/write, error_messages)
            * n10 TEST_CLI(smoke_tests)
            * n11 NARRATIVE_EXPLAIN(concepts, beginner_tone)
            * n12 NARRATIVE_MAP_TO_CODE(trace_required=true)
Edges:
            * n5..n8 depend on n1,n2,n3,n4
            * n10 depends on n5..n9
            * n12 depends on n11 and the rendered code trace
9.3 Target A: Code backend lowering
Lowering examples:
            * DEFINE_DOMAIN_CONCEPT → dataclass Task
            * DEFINE_STORAGE → load_state()/save_state()
            * IMPLEMENT_COMMAND(add) → def cmd_add(args, state): ...
            * TEST_CLI → pytest or a minimal subprocess smoke test
Rendered artifact snippet (illustrative skeleton):
from dataclasses import dataclass, asdict
import json, sys, pathlib


@dataclass
class Task:
    id: int
    text: str
    done: bool = False


DB_PATH = pathlib.Path("todo.json")


def load_state():
    if not DB_PATH.exists():
        return []
    return json.loads(DB_PATH.read_text())


def save_state(tasks):
    DB_PATH.write_text(json.dumps(tasks, indent=2))


def cmd_add(text):
    tasks = load_state()
    next_id = (max([t["id"] for t in tasks]) + 1) if tasks else 1
    tasks.append(asdict(Task(id=next_id, text=text)))
    save_state(tasks)
    print(f"Added #{next_id}: {text}")


# ... list/done/remove ...


def main(argv):
    # parse argv -> command
    pass


if __name__ == "__main__":
    main(sys.argv[1:])


Validation:
            * run smoke test: add then list shows item
            * if parsing missing → failure points to n4 slice → recompile n4 and dependent code only
9.4 Target B: Story/explanation backend lowering
Lowering examples:
            * DEFINE_DOMAIN_CONCEPT(Task) → “a task is a record with fields…”
            * DEFINE_COMMANDS → sections (“Add”, “List”, …)
            * NARRATIVE_MAP_TO_CODE → inline callouts that reference code functions
Rendered artifact snippet (outline):
            1. What we’re building (offline CLI todo)
            2. Data model (Task dataclass)
            3. Storage (todo.json; load/save)
            4. Commands and flow (argv → command → handler)
            5. Testing (“smoke run” checklist)
Validation:
            * narrative must mention only features present in code trace
            * if narrative claims “sync” (not in code) → failure points to n12 → recompile narrative slice only
Key point: both artifacts were produced from the same S-IR, so the narrative and code remain aligned by construction.
________________


10. Implementation blueprint (practical details)
10.1 Suggested tooling (prototype-friendly)
            * Schema validation: Pydantic / JSON Schema
            * DAG utilities: NetworkX
            * Parallel execution: Ray / asyncio task groups
            * Caching: content-addressed store keyed by (op, inputs, constraints, version)
            * Determinism controls: temperature=0 for extraction/typing passes; retry + consensus for ambiguous nodes
10.2 Handling LLM nondeterminism
            * enforce deterministic decoding for compiler passes,
            * use ensemble agreement for extraction when stakes are high,
            * store intermediate artifacts to allow debugging and replay.
10.3 Trace bundle format
Store:
            * plan hash
            * S-IR graph
            * backend + T-IR
            * node outputs
            * validation results
            * mappings from artifact spans → node IDs
This makes “why is this here?” answerable.
________________


11. Evaluation
11.1 Benchmarks / datasets
            * Code: HumanEval-style unit test pass rates (plus project-scale tasks with file trees)
            * Narrative: story coherence datasets + human preference evals
            * Hybrid: tasks requiring consistent doc+code alignment (README must match behavior)
11.2 Baselines
Compare against:
            * direct generation
            * prompt chaining (handwritten pipelines)
            * agentic tool loops (ReAct-style) (Emergent Mind)
            * reflection-based repair (Reflexion-style) (scixplorer.org)
            * pipeline compiler (DSPy-style) (Emergent Mind)
            * graph reasoning prompting (ToT/GoT) (DBLP)
11.3 Metrics
Quality:
            * constraint satisfaction rate
            * contradiction/continuity error rate (narrative)
            * unit test pass rate (code)
Efficiency:
            * token cost
            * wall-clock latency
            * number of retries per accepted node
            * percent of work parallelized (DAG width)
Debuggability:
            * time-to-localize a failure (node slice size)
            * fraction of repairs localized vs global regeneration
11.4 Ablations
            * remove typing pass
            * remove DAG scheduling (force sequential)
            * remove MVC routing (always use strongest worker)
            * remove trace-based repair (global regen only)
________________


12. Limitations and open problems
            1. Validator scarcity outside code
Story/song “correctness” is harder to validate than code. Constraint-based validators help, but taste remains subjective.
            2. Over-atomization overhead
Too many tiny nodes increase coordination cost; too few nodes reduce verifiability. Finding the “sweet spot” is a practical research problem.
            3. Semantic extraction errors
If the semantic compiler mis-parses intent, it can lock in the wrong structure. Mitigation: ambiguity flags + human gates for high-stakes nodes.
            4. Scaling to very large DAGs
Novel-length artifacts may produce 1000+ nodes. Efficient subgraph caching, hierarchical compilation, and summarizing “macro-nodes” become necessary.
            5. Interactive edits mid-compilation
When the user changes requirements, incremental recompilation must correctly invalidate affected subgraphs without cascading unnecessary rebuilds.
            6. Bias and framing leakage
Extraction/normalization can amplify biases by canonizing one interpretation. Mitigation: alternative parses + explicit choice points.
________________


13. Conclusion
Cognitive Compilation reframes LLM-based generation as a compiler pipeline: plan formation yields a stable source specification; semantic compilation produces a typed DAG of semantic atoms; and target compilation lowers the DAG into domain-specific representations with validators, localized repair, parallel scheduling, and cost-aware routing. This architecture bridges the gap between flexible natural-language intent and dependable artifact manufacturing—supporting multi-target outputs while improving coherence, efficiency, and debuggability.
________________


Comparison table (quick reviewer-friendly summary)
Property
	Direct prompt → artifact
	Prompt chains
	Agent loops
	Cognitive Compilation
	Stable intermediate representation
	❌
	⚠️ informal
	⚠️ implicit
	✅ typed S-IR/T-IR
	Early constraint/type checking
	❌
	⚠️ partial
	⚠️ partial
	✅ compile-time
	Parallelizable by design
	❌
	⚠️ manual
	⚠️ sometimes
	✅ DAG scheduling
	Cost control via routing
	❌
	⚠️ manual
	⚠️ ad hoc
	✅ MVC-based
	Localized repair
	❌
	⚠️ manual
	✅ sometimes
	✅ trace-sliced
	Multi-target backends
	⚠️ manual
	⚠️ manual
	⚠️ possible
	✅ first-class
	________________


If you want the next iteration to be even more “submission-shaped,” I can also:
               * turn the walkthrough into a more formal Algorithm + Figure section,
               * add a threats-to-validity subsection (reviewers love that),
               * and rewrite the whole draft in an ACM/NeurIPS paper style (tight, citation-forward, with formal definitions).


Tab 3
Semantic Compilation: Turning Natural-Language Plans into Verified, Parallel, Multi-Target Artifacts
Author: (your name / affiliation here)
Contact: (email here)
Abstract
Large Language Models (LLMs) can generate code, prose, and other artifacts directly from prompts, but direct generation remains brittle for complex work: requirements drift over long contexts, logical constraints are inconsistently enforced, and multi-step workflows are often executed serially with uniform model usage regardless of subtask difficulty. This paper proposes Semantic Compilation, a compiler-inspired architecture that converts natural-language intent into a typed, verifiable Semantic Intermediate Representation (S-IR) and then “lowers” that representation into target-specific intermediate forms (T-IRs) before producing final artifacts (e.g., code, tests, documentation, stories, songs). The key idea is to treat generative work as a compilation pipeline: (1) Plan Formation produces a normalized source plan, (2) Semantic Compilation decomposes the plan into semantic atoms organized as a dependency graph with explicit contracts, and (3) Target Compilation maps semantic atoms into target-native structures and renders final outputs with traceability. Because S-IR is a Directed Acyclic Graph (DAG), the system can automatically parallelize independent branches and apply capability routing (“intelligence arbitrage”) by assigning each node the minimum-cost worker that can satisfy its contract. We describe representations, compilation passes, scheduling, validator integration, and a repair loop that supports incremental recompilation. A worked example demonstrates compiling a single plan into both runnable code and aligned narrative text. We conclude with an evaluation plan and open problems around semantic under-specification, validator scarcity, and non-determinism.
________________


1. Introduction
LLMs are increasingly used as general-purpose generators: write a feature, draft a report, refactor a module, outline a story. For small tasks, “prompt → output” works well. For larger tasks, direct generation encounters predictable failure modes:
               * Entanglement: constraints, style, and logic intermix across tokens; changing one requirement can destabilize the whole output.
               * Drift: the model’s later tokens diverge from earlier commitments, especially when requirements are numerous.
               * Linearity: many agentic workflows serialize steps that are actually independent.
               * Uniformity: expensive, high-capability models are often used for trivial subtasks because the system lacks a way to formalize difficulty and route work.
Traditional compilers handle analogous problems by enforcing a separation of concerns: parse source code into an Intermediate Representation (IR), apply analysis/optimization passes to the IR, and only then generate target code. This separation enables validation, optimization, parallel scheduling, and incremental recompilation.
This paper applies that blueprint to generative systems. Instead of treating natural language as the final substrate, we treat it as source material that should be compiled into a structured semantic form before any target-specific rendering occurs.
________________


2. Contributions
This paper makes four concrete contributions:
               1. A compiler architecture for generative work with three stages: Plan Formation → Semantic Compilation → Target Compilation.
               2. A typed Semantic IR (S-IR) built from semantic atoms (minimal units of meaning + action) arranged as a DAG with explicit contracts (inputs, outputs, constraints, acceptance checks).
               3. A scheduler for parallelism + intelligence arbitrage that (a) exploits DAG structure for concurrency and (b) routes each node to the lowest-cost worker that can satisfy its contract.
               4. Traceable validation + repair: validators attach failures to specific IR nodes, enabling localized repair and incremental recompilation rather than global regeneration.
________________


3. Background and Related Work
3.1 Prompted reasoning and structured inference
Chain-of-Thought (CoT) prompting shows that eliciting intermediate reasoning steps can improve performance on complex problems, but it still relies on a single left-to-right generation stream where constraints remain informal. (arXiv)
Tree-of-Thoughts (ToT) generalizes CoT by exploring multiple candidate “thoughts” and search strategies, improving deliberation by branching and self-evaluation rather than committing to one trajectory. (arXiv)
Graph-of-Thoughts extends this idea by representing intermediate units as a general graph with dependencies and transformations, enabling richer reuse and combination patterns. (arXiv)
Difference: These methods structure inference-time reasoning, but they do not generally produce a typed, target-agnostic IR with contracts that can be lowered into multiple backends and validated with tool-driven checks.
3.2 Tool use and agent loops
Toolformer trains models to decide when to call external tools and how to incorporate results, addressing factual lookup and arithmetic weaknesses. (arXiv)
ReAct interleaves reasoning traces with actions, improving performance and interpretability in tool-augmented settings. (arXiv)
Reflexion adds a feedback loop where agents store reflections in memory to improve subsequent attempts without weight updates. (arXiv)
Difference: Tool/agent frameworks often treat intermediate steps as untyped text. Semantic Compilation makes intermediate structure explicit and compilable: the system can validate, parallelize, and selectively recompile subgraphs.
3.3 “Programmatic” intermediates
Several lines of work separate reasoning from execution by using programs as intermediates. PAL generates code and delegates execution to an interpreter to reduce arithmetic/logical errors. (arXiv)
Program-of-Thoughts (PoT) similarly disentangles computation from reasoning by generating executable programs for numerical reasoning tasks. (arXiv)
ReWOO reduces redundant prompting in tool-augmented reasoning by decoupling planning (“reasoning”) from tool observation. (arXiv)
Difference: These systems typically target a single “backend” (often code execution) rather than a general multi-target compilation stack. Semantic Compilation is designed explicitly for multi-target lowering (code + tests + docs + narrative, etc.) from a shared semantic core.
3.4 LMs as compilers and compiler-aware LMs
Recent work frames LMs as “compilers” in narrower senses, such as simulating pseudocode execution to improve algorithmic reasoning (Think-and-Execute). (arXiv)
Separately, foundation models trained for compiler IR and optimization tasks (e.g., LLVM-IR/assembly) indicate growing interest in compiler-native representations. (arXiv)
Difference: Semantic Compilation is not primarily about compiling code better; it is about compiling intent into a semantic IR that can be lowered into many artifact types, with explicit scheduling, validation, and repair.
________________


4. System Overview
Semantic Compilation consists of three stages:
               1. Plan Formation (Source Plan): Convert user intent into a normalized, declarative plan (structured text).
               2. Semantic Compilation (S-IR): Decompose the plan into semantic atoms, type them, connect dependencies, and run semantic optimization/validation passes.
               3. Target Compilation (T-IR → Artifact): Lower S-IR into one or more target IRs (e.g., Python module IR, story-outline IR), then render final artifacts with traces back to S-IR.
A key design choice is to represent the S-IR as a DAG rather than a strict tree: many semantic subgoals are shared across targets (e.g., “define the CLI commands” supports both code generation and documentation), and DAGs support reuse and memoization.
________________


5. Representations
5.1 Source Plan
A Source Plan is a constrained, human-readable representation—often YAML/JSON—capturing:
               * Goals (what to produce)
               * Constraints (hard/soft requirements)
               * Interfaces (inputs/outputs, schemas)
               * Quality gates (tests, validators)
               * Resources (budgets, allowed tools, latency targets)
Example (abridged):
goal:
  - artifact: "python_cli_app"
    name: "todo"
  - artifact: "short_onboarding_story"
constraints:
  hard:
    - "CLI supports add/list/done/remove"
    - "Data stored locally in JSON"
    - "No external dependencies"
  soft:
    - "Readable error messages"
    - "Story tone: friendly, concise"
validators:
  - "python -m py_compile"
  - "unit_tests"
  - "story_coherence_check"
resources:
  budget: "low"
  latency: "interactive"


5.2 Semantic Atoms
A semantic atom is the smallest unit the compiler treats as independently schedulable and verifiable. Each atom has a contract:
               * op: operation kind (e.g., DEFINE_INTERFACE, IMPLEMENT_FEATURE, WRITE_EXAMPLE)
               * inputs/outputs: typed slots
               * preconditions/postconditions
               * validators: checks that must pass for the atom to be accepted
               * metadata: cost hints, target relevance, provenance
5.3 Semantic IR (S-IR)
We define S-IR as a DAG ( G=(V,E) ), where each node ( v \in V ) is a semantic atom and each edge ( (u \rightarrow v) \in E ) indicates that ( v ) depends on outputs of ( u ).
A minimal node schema (illustrative):
{
  "id": "N7",
  "op": "IMPLEMENT_COMMAND",
  "target_tags": ["python"],
  "inputs": [{"name": "command_spec", "type": "CommandSpec"}],
  "outputs": [{"name": "python_code_fragment", "type": "PyCode"}],
  "constraints": ["No external deps", "Persist to JSON"],
  "validators": ["unit_tests:command_add", "lint:basic"],
  "cost_hints": {"expected_tokens": 800, "difficulty": "medium"}
}


5.4 Target IRs (T-IR)
Target IR is backend-specific. Examples:
               * Code T-IR: file/module graph, function signatures, AST-like blocks, test plan.
               * Narrative T-IR: beats, characters, tone constraints, required facts, outline sections.
               * Song T-IR: structure (verse/chorus), rhyme constraints, meter hints, motifs.
The same S-IR node may lower into multiple T-IR fragments (e.g., a “DEFINE_COMMANDS” atom produces both argparse structure and README usage text).
________________


6. Compilation Passes
6.1 Plan Formation passes
               * Normalization: rewrite ambiguous natural language into constrained fields.
               * Constraint extraction: separate hard vs soft constraints.
               * Interface extraction: define schemas and I/O contracts early.
6.2 Semantic Compilation passes
               * Decomposition: recursively split goals until leaves are “atomic enough” to validate.
               * Typing: attach types to inputs/outputs (schemas, file roles, story facts).
               * Dependency inference: connect atoms into a DAG; reject cycles (“circular dependencies”).
               * Semantic linting: detect missing validators, underspecified constraints, inconsistent terms.
               * Common-subgoal factoring: merge duplicate subgraphs (DAG deduplication).
               * Scheduling annotation: estimate difficulty/cost and compute slack/criticality.
6.3 Target Compilation passes
               * Lowering: map semantic ops to target constructs (e.g., CLI command → argparse subparser).
               * Target validation planning: attach concrete validators (compile, tests, style checks).
               * Rendering: generate final artifacts (code, prose, etc.) with trace IDs.
________________


7. Scheduling and Intelligence Arbitrage
7.1 Capability routing (Minimum Viable Capability)
For each node, the scheduler assigns a Minimum Viable Capability (MVC) level—informally, the lowest-cost worker that can satisfy the contract with high probability.
Workers can be:
               * Deterministic tools (formatters, compilers, linters)
               * Small/cheap models (templating, rewriting, extraction)
               * High-capability models (complex synthesis, schema design, tricky bug fixes)
               * Human review (optional gate for high-stakes nodes)
7.2 Parallel execution from DAG structure
Given S-IR (G), the runtime:
               1. Performs a topological ordering.
               2. Executes all ready nodes (dependencies satisfied) concurrently.
               3. Applies backpressure via resource budgets (token/latency caps).
7.3 Slack-aware cost optimization
Compute a critical path length for each node (longest remaining dependent chain). Nodes with slack can be routed to cheaper workers even if slower, while critical-path nodes get faster/more reliable workers.
This is directly analogous to scheduling in parallel runtimes and compiler backends, but applied to semantic tasks.
________________


8. Verification, Traceability, and Repair
8.1 Validators as first-class citizens
Validators are not an afterthought; they are embedded in the IR. Examples:
               * Code: type check, compile, unit tests, static analysis, property tests.
               * Docs/story: fact consistency checks, required-inclusion checks, style constraints.
               * Multi-target: cross-artifact consistency (README claims match CLI behavior).
8.2 Traceability
Every rendered artifact segment includes provenance metadata: which S-IR node(s) produced it. This enables failure localization:
               * A failing unit test maps to the semantic atoms responsible for the relevant behavior.
               * A docs inconsistency maps to the atoms that introduced the claim.
8.3 Repair loop with incremental recompilation
When a validator fails:
               1. Identify implicated nodes via traces.
               2. Patch the smallest subgraph necessary (edit S-IR, re-lower, re-render).
               3. Re-run validators for impacted targets only.
This avoids regenerating large artifacts when only a small semantic region is faulty.
________________


9. End-to-End Walkthrough (One Plan → Code + Story)
9.1 Input intent
“Create a small CLI todo app in Python (no dependencies) and write a short onboarding story explaining how a new user uses it.”
9.2 Source Plan (abridged)
(See Section 5.1 for a representative format.)
9.3 S-IR sketch (abridged)
               * N1: DEFINE_STORAGE_SCHEMA → outputs Task schema
               * N2: DEFINE_COMMANDS(add/list/done/remove) → outputs CommandSpec[]
               * N3: IMPLEMENT_STORAGE(load/save JSON) → outputs PyCode
               * N4: IMPLEMENT_COMMAND(add) depends on N1,N3,N2
               * N5: IMPLEMENT_COMMAND(list) depends on N1,N3,N2
               * N6: IMPLEMENT_COMMAND(done) depends on N1,N3,N2
               * N7: IMPLEMENT_COMMAND(remove) depends on N1,N3,N2
               * N8: INTEGRATE_CLI(argparse main) depends on N2,N4–N7
               * N9: WRITE_ONBOARDING_STORY depends on N2 (and constraints)
               * N10: CROSS_CHECK_STORY_FACTS depends on N2,N9
Notably, N9 (story) can run in parallel with most code work once N2 exists.
9.4 Target compilation to runnable Python (single-file artifact)
Below is a complete, runnable implementation consistent with the plan (single file, stdlib only):
#!/usr/bin/env python3
"""
todo.py - a tiny CLI todo app (stdlib only)


Usage:
  python todo.py add "buy milk"
  python todo.py list
  python todo.py done 1
  python todo.py remove 1
"""


from __future__ import annotations


import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from typing import List




DEFAULT_DB_PATH = os.path.join(os.getcwd(), "todo.json")




@dataclass
class Task:
    id: int
    text: str
    done: bool = False




def load_tasks(path: str) -> List[Task]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    tasks = []
    for item in data.get("tasks", []):
        tasks.append(Task(id=int(item["id"]), text=str(item["text"]), done=bool(item["done"])))
    return tasks




def save_tasks(path: str, tasks: List[Task]) -> None:
    payload = {"tasks": [asdict(t) for t in tasks]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)




def next_id(tasks: List[Task]) -> int:
    return (max((t.id for t in tasks), default=0) + 1)




def cmd_add(args: argparse.Namespace) -> int:
    tasks = load_tasks(args.db)
    tid = next_id(tasks)
    tasks.append(Task(id=tid, text=args.text, done=False))
    save_tasks(args.db, tasks)
    print(f"Added #{tid}: {args.text}")
    return 0




def cmd_list(args: argparse.Namespace) -> int:
    tasks = load_tasks(args.db)
    if not tasks:
        print("No tasks yet. Try: todo.py add \"your task\"")
        return 0
    for t in sorted(tasks, key=lambda x: x.id):
        mark = "✓" if t.done else " "
        print(f"[{mark}] {t.id}: {t.text}")
    return 0




def find_task(tasks: List[Task], tid: int) -> Task | None:
    for t in tasks:
        if t.id == tid:
            return t
    return None




def cmd_done(args: argparse.Namespace) -> int:
    tasks = load_tasks(args.db)
    t = find_task(tasks, args.id)
    if t is None:
        print(f"Task #{args.id} not found.", file=sys.stderr)
        return 2
    t.done = True
    save_tasks(args.db, tasks)
    print(f"Marked #{args.id} as done.")
    return 0




def cmd_remove(args: argparse.Namespace) -> int:
    tasks = load_tasks(args.db)
    before = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    if len(tasks) == before:
        print(f"Task #{args.id} not found.", file=sys.stderr)
        return 2
    save_tasks(args.db, tasks)
    print(f"Removed #{args.id}.")
    return 0




def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo.py", description="Tiny CLI todo app (stdlib only).")
    p.add_argument("--db", default=DEFAULT_DB_PATH, help=f"Path to DB file (default: {DEFAULT_DB_PATH})")


    sub = p.add_subparsers(dest="cmd", required=True)


    addp = sub.add_parser("add", help="Add a new task")
    addp.add_argument("text", help="Task text")
    addp.set_defaults(func=cmd_add)


    listp = sub.add_parser("list", help="List tasks")
    listp.set_defaults(func=cmd_list)


    donep = sub.add_parser("done", help="Mark a task as done")
    donep.add_argument("id", type=int, help="Task id")
    donep.set_defaults(func=cmd_done)


    rmp = sub.add_parser("remove", help="Remove a task")
    rmp.add_argument("id", type=int, help="Task id")
    rmp.set_defaults(func=cmd_remove)


    return p




def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))




if __name__ == "__main__":
    raise SystemExit(main())


9.5 Target compilation to onboarding story (aligned to the same command spec)
Example onboarding excerpt (friendly, concise, command-accurate):
Maya keeps forgetting small errands, so she makes a tiny list in her terminal.
She starts with python todo.py add "buy milk" and gets a confirmation: the task becomes #1.
After adding a couple more, she runs python todo.py list to see everything in one place, with unchecked boxes for what’s still open.
When she finishes the milk run, she types python todo.py done 1 and the list now shows a checkmark next to 1.
If she adds something by mistake, python todo.py remove 1 deletes it cleanly—no fuss, no extra apps.
Because the story is generated from the same S-IR command definitions, a cross-check validator (N10) can automatically flag any story sentence that references a non-existent command or wrong argument shape.
________________


10. Implementation Blueprint
10.1 Core data structures
               * IR store: versioned S-IR graph + per-target T-IR fragments
               * Artifact store: emitted files/text + trace maps (artifact span → node IDs)
               * Validator registry: typed validators producing structured diagnostics
               * Cost model: estimate tokens, latency, failure risk per node
10.2 Practical tooling choices (illustrative)
               * DAG construction/analysis: NetworkX (networkx.org)
               * Distributed parallel execution: Ray (USENIX)
               * Schema/type enforcement: JSON Schema or Python dataclasses/pydantic-like validation (library choice is flexible)
10.3 Handling LLM non-determinism
               * Use deterministic decoding for compilation passes where stability matters.
               * For ambiguous extraction steps, run small ensembles and take majority/consensus.
               * Cache compilation outputs by (plan hash, node hash) for incremental recompilation.
________________


11. Evaluation Plan
11.1 Tasks and datasets
               * Code synthesis: HumanEval-style functional correctness tasks (unit-test pass rates). (arXiv)
               * Narrative generation: ROCStories / Story Cloze style settings for coherence and consistency checks. (ACL Anthology)
               * Multi-target alignment: generate code + README + tutorial story; measure consistency between artifacts.
11.2 Baselines
               * Direct prompt-to-artifact generation (single-shot and iterative)
               * ReAct-style tool-augmented agent loop (arXiv)
               * Reflection-based iterative improvement (Reflexion-like) (arXiv)
               * Declarative pipeline compilation approaches (DSPy-like) (arXiv)
               * Multi-agent collaboration frameworks (AutoGen-like) (arXiv)
11.3 Metrics
               * Correctness: tests pass rate, validator pass rate
               * Cost: tokens used per successful artifact; number of high-capability calls
               * Latency: wall-clock time with parallel scheduling
               * Repair locality: fraction of nodes recompiled per failure
               * Cross-artifact consistency: contradictions between README/story and code behavior
11.4 Ablations
               * Remove S-IR typing (untyped graph)
               * Disable DAG parallelism (force sequential)
               * Disable capability routing (single worker tier)
               * Disable trace-based repair (global regeneration)
________________


12. Limitations and Open Problems
               1. Semantic under-specification: natural language often omits critical constraints; a compiler can only enforce what is captured in S-IR.
               2. Validator scarcity for non-code artifacts: tests and linters are abundant for code but weaker for stories/songs; creating reliable validators is hard.
               3. Overhead: multi-pass compilation can cost more than direct generation on small tasks; systems should detect when compilation is worth it.
               4. Bias and value alignment: semantic extraction can encode biased assumptions; debiasing passes and human-in-the-loop gates remain important.
               5. Scaling to very large graphs: thousands of nodes require careful caching, batching, and incremental recompilation strategies.
________________


13. Conclusion
Semantic Compilation reframes LLM-driven generation as a compiler pipeline: form a structured plan, compile it into a typed semantic DAG, then lower into target-specific representations and render artifacts under validator control. This architecture directly targets the dominant failure modes of direct generation—drift, entanglement, linearity, and uniformity—by introducing IR contracts, DAG parallelism, capability routing, and traceable repair. The result is a practical path toward scalable, multi-target, verifiable artifact generation where “generation” behaves less like improvisation and more like a reproducible build.
________________


Appendix A. Comparison Table (High-Level)
Property
	Direct Prompting
	Agent Loop (ReAct-like)
	Semantic Compilation (this work)
	Typed intermediate representation
	❌
	❌/⚠️ (implicit)
	✅
	Parallelism from dependency graph
	❌
	⚠️ (manual)
	✅
	Intelligence arbitrage (capability routing)
	⚠️ (ad hoc)
	⚠️ (often uniform)
	✅
	Incremental recompilation
	❌
	⚠️ (partial)
	✅
	Validator integration as first-class
	⚠️ (post hoc)
	✅
	✅
	Trace-based failure localization
	❌
	⚠️
	✅
	Multi-target output from shared semantics
	⚠️
	⚠️
	✅
	________________


References
(Formatted for readability; adapt to BibTeX/LaTeX as needed.)
[1] Jason Wei et al. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. arXiv:2201.11903 (2022). (arXiv)
[2] Shunyu Yao et al. ReAct: Synergizing Reasoning and Acting in Language Models. arXiv:2210.03629 (ICLR version, 2023). (arXiv)
[3] Shunyu Yao et al. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. arXiv:2305.10601 (NeurIPS 2023). (arXiv)
[4] Maciej Besta et al. Graph of Thoughts: Solving Elaborate Problems with Large Language Models. arXiv:2308.09687 (AAAI 2024). (arXiv)
[5] Timo Schick et al. Toolformer: Language Models Can Teach Themselves to Use Tools. arXiv:2302.04761 (2023). (arXiv)
[6] Noah Shinn et al. Reflexion: Language Agents with Verbal Reinforcement Learning. arXiv:2303.11366 (2023). (arXiv)
[7] Omar Khattab et al. DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines. arXiv:2310.03714 (2023). (arXiv)
[8] Qingyun Wu et al. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv:2308.08155 (2023). (arXiv)
[9] Binfeng Xu et al. ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models. arXiv:2305.18323 (2023). (arXiv)
[10] Luyu Gao et al. PAL: Program-aided Language Models. arXiv:2211.10435 (2022). (arXiv)
[11] Wenhu Chen et al. Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks. arXiv:2211.12588 (TMLR 2023). (arXiv)
[12] Hyungjoo Chae et al. Language Models as Compilers: Simulating Pseudocode Execution Improves Algorithmic Reasoning in Language Models. arXiv:2404.02575; EMNLP 2024. (arXiv)
[13] Chris Cummins et al. Meta Large Language Model Compiler: Foundation Models of Compiler Optimization. arXiv:2407.02524 (2024). (arXiv)
[14] Chris Lattner and Vikram Adve. LLVM: A Compilation Framework for Lifelong Program Analysis and Transformation. CGO (2004). (LLVM)
[15] Mark Chen et al. Evaluating Large Language Models Trained on Code. arXiv:2107.03374 (HumanEval, 2021). (arXiv)
[16] Nasrin Mostafazadeh et al. A Corpus and Cloze Evaluation for Deeper Understanding of Commonsense Stories. NAACL (2016). (ACL Anthology)
[17] Philipp Moritz et al. Ray: A Distributed Framework for Emerging AI Applications. OSDI (2018). (USENIX)
[18] Aric A. Hagberg, Daniel A. Schult, Pieter J. Swart. Exploring Network Structure, Dynamics, and Function using NetworkX. SciPy (2008). (networkx.org)
[19] Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman. Compilers: Principles, Techniques, and Tools (2nd ed.). Pearson (2006). (Pearson)
________________


If you want, I can also convert this into a conference-ready LaTeX template (with BibTeX entries and figure/table formatting), or into a DOCX/PDF—but the full rewritten standalone paper text is above.




CODEX BUILD DOCUMENT (FULL REWRITE)
Product: Semantic Compiler Workbench (SCW) — State-of-the-Art Local Compiler for Multi-Target Generation
Business Model: One-time license (paid), optional time-limited trial license, optional updates entitlement window.
Cost Model: Customers bring their own model keys (OpenRouter-first). Customers pay inference/token costs. SCW provides the “compiler moat”: IR + validators + trace + repair + arbitrage + reproducibility.
Implementation Preference: Rust-first (daemon/core/router/validators), Tauri desktop app (Rust + TS/React UI), CLI.
________________


0) Executive intent (what Codex must deliver)
Implement a complete, production-grade local application that:
               1. Converts natural-language intent into a structured Source Plan.
               2. Compiles Source Plan into a typed Semantic Intermediate Representation (S-IR) DAG of semantic atoms.
               3. Schedules nodes for parallel execution and intelligence arbitrage (capability routing).
               4. Lowers S-IR into target-specific IRs (T-IRs) and renders artifacts (code, docs, narrative, song, slides optional).
               5. Runs deterministic validators; attaches failures to node IDs; performs node-local repair + incremental recompilation.
               6. Produces an auditable Trace Bundle that maps artifact spans back to S-IR nodes and router decisions.
               7. Stores provider keys securely (OS keychain) and supports customer policy-driven routing (OpenRouter-first, direct adapters optional).
               8. Enforces trial and full licensing without bricking user data.
No “MVP shortcuts.” No TODOs. No “we’ll do this later.” Ship a coherent, complete v1.
________________


1) Non-negotiable product properties (the moat)
1.1 Moat features (must ship in v1)
               1. Typed S-IR DAG with stable node IDs and strict schemas.
               2. Compiler passes (plan→S-IR; S-IR→T-IR) with linting + graph optimization.
               3. Validator-first compilation with structured diagnostics tied to node IDs and file ranges.
               4. Node-local repair with split-on-failure and incremental recompilation.
               5. Cost-aware scheduling (critical path + slack) and intelligence arbitrage router (tiering + escalation ladder).
               6. Trace Bundle (artifact span maps + decision logs + reproducible run manifests).
               7. Local-first (daemon + desktop + CLI) with robust offline operation.
               8. OpenRouter-first multi-model support + policy engine + fallback lists.
               9. Security: OS keychain, sandboxed execution for validators, secret redaction for exports/logs.
               10. Trial license + full license with update entitlement, offline verification, and non-destructive enforcement.
1.2 “Never do” rules
               * Never store API keys in plain text.
               * Never put keys into model prompts/context.
               * Never accept validator output as freeform text; all validators return structured JSON.
               * Never “global regenerate everything” if a localized repair is possible.
               * Never export a bundle without redacting secrets and marking redaction in the manifest.
________________


2) Product shape: Local-first three-part stack
2.1 Components shipped
               1. SCW Daemon (Rust)
               * Runs locally (127.0.0.1), HTTP API (Axum) + optional local IPC.
               * Owns compilation, routing, scheduling, validation, repair, caching, storage, licensing enforcement.
               2. SCW Desktop App (Tauri + React/TS)
               * UI to edit plan, view DAG, configure policies, run compiles, see diffs, costs, validators, repair.
               * Talks to daemon via local API.
               3. SCW CLI (Rust)
               * Full headless access for CI/local automation.
               * Commands call daemon; also support “single-binary mode” embedding core if daemon isn’t running.
2.2 Optional integration surfaces
               * MCP server mode (inside daemon; optional)
               * Exposes the same operations as tools.
               * Note: not required for core product; treat as a bonus integration.
________________


3) User workflow (what SCW must support end-to-end)
3.1 The canonical compile loop
               1. Create/open project
               2. Author intent in Plan Studio
               3. Generate structured Source Plan
               4. Lock plan → immutable plan hash
               5. Compile plan → S-IR DAG + semantic lints
               6. Build schedule → cost forecast + tier/model assignment
               7. Render selected targets → artifacts + trace maps
               8. Validate → structured failures
               9. Repair → node-local patch + incremental revalidate
               10. Export Release Bundle + Trace Bundle
3.2 Must-have UI screens
               * Projects Dashboard: projects list, last run status, costs, trial status.
               * Plan Studio:
               * “Intent” editor (rich text)
               * “Plan YAML/JSON” editor (schema aware)
               * Plan lint panel
               * Plan lock/unlock view (creates new plan version on unlock/edit)
               * Plan diff view
               * S-IR Graph View:
               * DAG visualization
               * critical path highlight
               * per-node badges (tier/model/cost/attempts/cache hit)
               * Node Inspector:
               * contract (inputs/outputs/types)
               * constraints + acceptance links
               * routing decision log
               * prompt(s) used (if any) + structured outputs
               * produced artifact ranges
               * Targets:
               * target profiles
               * render options
               * T-IR preview
               * Artifacts Explorer:
               * file tree
               * diffs (last run vs current)
               * trace highlight overlay
               * Validator Console:
               * grouped failures by node_id
               * jump to file line range
               * suggested repair action
               * Cost & Arbitrage Analytics:
               * per-run cost
               * “savings vs baseline”
               * per-node cost map
               * Providers & Policy:
               * OpenRouter key
               * optional direct provider keys
               * tier model sets
               * privacy policy (ZDR/no_train flags)
               * License:
               * trial start/install license file
               * status, expiry, update entitlement
               * offline grace + export availability
               * Security & Audit:
               * redaction reports
               * sandbox settings
               * export controls
3.3 CLI commands (must ship)
               * scw init
               * scw plan edit / scw plan lint / scw plan lock
               * scw compile (plan→S-IR)
               * scw schedule (S-IR→schedule)
               * scw run --targets python,docs,...
               * scw validate
               * scw repair --auto / scw repair --interactive
               * scw bundle export --run <id>
               * scw policy set/get
               * scw providers add/test/list
               * scw license status/install/start-trial
________________


4) Core data model (schemas are mandatory)
All schemas live under /schemas and are versioned. SCW rejects unknown schema versions unless explicitly upgraded.
4.1 Source Plan schema (Plan v1)
File: plan.json (canonical JSON) + optional plan.yaml (human).
Fields required:
               * project_id, plan_id, plan_version
               * goals[]: artifact(s) + audience + format
               * constraints.hard[], constraints.soft[]
               * interfaces.inputs[], interfaces.outputs[] with JSON Schema
               * acceptance.validators[] (by id) and optional acceptance.tests[]
               * targets[]: list of target profile IDs
               * resources: budgets (USD/time), privacy flags, mode
               * risk_profile: low/standard/high
Plan lock:
               * plan_hash = sha256(canonical_json(plan))
               * locked plans are immutable; editing creates a new plan_version and new hash.
4.2 Semantic IR schema (S-IR v1)
File: sir.json
Global fields:
               * sir_version
               * sir_hash
               * plan_hash
               * nodes[]
               * edges[] (or depends_on inside nodes; choose one but be consistent)
               * lints[] with stable lint codes
               * features_summary (counts, complexity, critical path length estimate)
Node fields (required):
               * node_id (stable)
               * op (enum)
               * targets[] tags
               * inputs[] typed
               * outputs[] typed
               * constraints[] references
               * validators[]
               * depends_on[]
               * routing_bounds (tier_min/tier_max, required capabilities)
               * features (computed: difficulty, ambiguity, novelty, blast_radius, validator_strength)
               * provenance (plan clause ids)
4.3 Schedule schema (Schedule v1)
File: schedule.json
Fields:
               * sir_hash, policy_version
               * nodes[] each with:
               * node_id
               * priority (critical/normal/slack)
               * assigned: tier + engine + model + fallback_models
               * budget: max_attempts, max_tokens, max_usd, timeout
               * sandbox_profile
               * cost_forecast (p50/p90)
               * parallelism_plan (worker count, concurrency groups)
4.4 Target IR schema (T-IR v1)
Per target: tir_python.json, tir_docs.json, tir_story.json, tir_song.json etc.
Must include:
               * target_id, sir_hash
               * render_units[] each referencing node_id
               * output artifact paths/sections
               * trace anchors (line ranges or span indices)
               * target-specific validator plan
4.5 Trace Bundle schema (Trace v1)
Bundle contents (directory or zip):
               * plan.json
               * sir.json
               * schedule.json
               * tir_*.json
               * artifacts/ (rendered outputs)
               * traces/:
               * trace_<artifact>.json mapping spans/ranges → node_ids
               * validators/:
               * validator_results.jsonl (structured)
               * router/:
               * decisions.jsonl (why model was chosen)
               * cost/:
               * cost_report.json
               * security/:
               * redaction_report.json
               * manifest.json with hashes of everything
________________


5) Semantic atoms and ops (v1 must include)
Define an enum OpKind with versioning. Required ops:
5.1 Plan/structure ops
               * DEFINE_ENTITY
               * DEFINE_SCHEMA
               * DEFINE_INTERFACE
               * DEFINE_INVARIANT
               * DEFINE_WORKFLOW
               * INTEGRATE_PIPELINE
5.2 Implementation ops
               * IMPLEMENT_COMPONENT
               * IMPLEMENT_COMMAND
               * GENERATE_TESTS
               * WRITE_DOC_SECTION
               * WRITE_TUTORIAL_EXAMPLE
               * WRITE_STORY_BEAT
               * WRITE_SONG_SECTION
5.3 Deterministic ops
               * LINT_ARTIFACT
               * RUN_TESTS
               * CROSS_CHECK_CLAIMS
               * BUNDLE_RELEASE
Each op has:
               * required input types
               * output types
               * default validators
               * default routing tier bounds
               * split-on-failure policy
________________


6) Compiler passes (must be implemented fully)
6.1 Plan → S-IR passes
               1. Parse & canonicalize plan (YAML→JSON canonical form).
               2. Clause indexing: assign stable IDs to plan clauses for provenance.
               3. Semantic extraction:
               * Extract required entities, interfaces, constraints, acceptance criteria, targets.
               * Convert into initial semantic atoms.
               4. Normalization:
               * Canonicalize synonyms (op normalization).
               * Merge equivalent constraints into shared “constraint capsule” nodes where appropriate.
               5. Typing:
               * Enforce schema links; all inputs/outputs must have types.
               * Insert conversion/adapter nodes if needed (explicit).
               6. Dependency inference:
               * Create edges based on required inputs.
               * Ensure DAG; detect cycles.
               7. Semantic linting:
               * Missing acceptance coverage: every acceptance validator must map to nodes.
               * Orphan nodes: no path to outputs.
               * Contradictory hard constraints.
               * Underspecified nodes (insufficient detail).
               8. Graph optimization:
               * Common subgraph elimination.
               * Constraint capsule factoring.
               * Dead node elimination (only if safe).
               9. Feature computation:
               * constraint_density, novelty, ambiguity, blast_radius, validator_strength
               * store in node.features
Output: sir.json + lint report with blocking vs non-blocking.
6.2 S-IR → T-IR passes (per target)
               1. Lowering:
               * Map op kinds to target constructs.
               2. Target lint:
               * Required files/sections exist.
               * Trace anchors can be computed.
               3. Render plan:
               * Determine file tree / section list / artifact list.
               4. Validator plan:
               * Determine validators to run for this target.
Output: tir_<target>.json
________________


7) Scheduling + Intelligence Arbitrage (OpenRouter-first)
7.1 Tiers (capability classes)
               * T0 Deterministic: compilers, linters, tests, parsers, schema validation
               * T1 Extract/Rewrite: formatting, summaries, schema extraction, small edits
               * T2 Routine Generation: boilerplate code/docs, straightforward beats/sections
               * T3 Deep Reasoning: architecture, tricky bug fixes, ambiguity resolution
               * T4 Human Gate: optional; for high-risk policy settings
7.2 Policy system (customer-owned)
Policy file controls:
               * enabled engines (OpenRouter default)
               * tier model sets (ordered lists)
               * privacy constraints (no_train / ZDR preferences)
               * budgets (job/node)
               * escalation ladder rules
               * prohibited models/providers (optional)
Policy is versioned; policy_version included in schedule and cache keys.
7.3 Node scoring
Compute:
               * difficulty_score = f(constraint_density, ambiguity, novelty, blast_radius, historical_fail_rate)
               * stakes from plan risk_profile + op category
               * validator_strength = strong if deterministic tests/compile exist
7.4 Critical path + slack scheduling
Compute critical path on S-IR DAG:
               * critical nodes (slack ~0) → prioritize reliability and speed within tier
               * slack nodes → cheapest acceptable model within tier
7.5 Arbitrage routing rules
For each node:
               1. If node is deterministic → assign T0 tool runner.
               2. Else choose tier_min from op defaults + node score.
               3. Pick model list from policy tier.
               4. Build OpenRouter request with fallback list.
               5. If output format fails → retry once same model, then fallback, then tier up.
               6. If validators fail → fallback within tier, then tier up.
               7. Node-local escalation only; never escalate the whole run.
7.6 Cost accounting + “savings vs baseline”
Compute:
               * tokens in/out, per model, per node
               * estimated USD (customer-defined price table OR OpenRouter reported usage if available)
               * baseline cost = “T3 everywhere”
Display savings and export in cost report.
________________


8) Inference layer (OpenRouter-first, adapters optional)
8.1 ModelClient interface (Rust trait)
Required methods:
                  * chat(request) -> response (sync)
                  * chat_stream(request) -> stream (optional)
                  * returns structured metadata: model_id, tokens, latency, finish_reason
8.2 Adapters to implement in v1
                  1. OpenRouterClient (default)
                  2. DirectOpenAIClient (escape hatch)
                  3. DirectAnthropicClient (escape hatch)
Optional but architected:
                  * Local model adapter (ollama/LM Studio) for T1/T2.
8.3 Strict structured output enforcement
Never trust models to output perfect JSON.
                  * Provide schema to model
                  * Parse output
                  * If invalid, return format failure → escalation ladder
________________


9) Validators (deterministic-first, structured output)
9.1 Validator interface (Rust)
Return type:
                  * validator_id
                  * status: pass|warn|fail
                  * severity: info|warning|error
                  * node_ids[]
                  * signature: stable failure fingerprint
                  * details
                  * artifact_refs[] (file + line ranges or doc spans)
                  * suggested_fix_class
9.2 Required validator sets (v1)
Core
                  * JSON schema validators (plan/sir/schedule/tir/trace)
                  * secret scanner (regex + entropy heuristics)
                  * export redaction validator
Python target
                  * format/lint (choose ruff)
                  * compile check
                  * unit tests (pytest)
                  * smoke CLI tests (subprocess)
Docs target
                  * markdown lint
                  * “claims registry” validation (see below)
                  * cross-check doc commands vs CLI spec from S-IR
Narrative target
                  * continuity ledger checks (entity states)
                  * constraints checks (must not contradict locked facts)
                  * structure validator (beats and ordering)
Song target
                  * section structure validator (verse/chorus/bridge policy)
                  * rhyme/meter policy validator (heuristic acceptable but structured output)
9.3 Claim-native documentation (moat)
Docs/tutorial outputs must include a structured claims sidecar:
                  * claims.json with claim objects:
                  * claim_id, text, type, derived_from_node_ids, evidence_refs, confidence
Cross-check validator ensures:
                     * all procedural claims map to S-IR ops and match code/CLI surfaces.
________________


10) Repair engine (node-local incremental recompilation)
10.1 Repair contract
Input: validator failures
Output: patch plan:
                     * affected nodes
                     * proposed changes (node regeneration and/or lowering rule changes)
                     * file diffs
                     * revalidation plan
10.2 Repair rules
                     * Attempt localized patch first.
                     * If node fails twice with different models → split-on-failure:
                     * subdivide node into smaller ops
                     * recompile subgraph
                     * Only modify plan if absolutely necessary (creates new plan version; must be explicit).
10.3 Patch application
                     * Apply diffs atomically
                     * Update trace maps
                     * Re-run only impacted validators
________________


11) Storage, caching, reproducibility
11.1 Stores
                     * SQLite index: projects, plans, runs, nodes, costs, validator results
                     * Content-addressed store on disk: artifacts, node outputs, logs
                     * Cache store:
                     * node output cache keyed by (node_hash + policy_version + tier + model_id)
                     * validator result cache keyed by artifact hash + validator id
11.2 Reproducible run bundles
Every run can export a bundle with:
                     * all IRs
                     * artifacts
                     * trace maps
                     * validator logs
                     * router decisions
                     * cost report
                     * manifest with hashes
This makes builds replayable and debuggable.
________________


12) Security model (must be product-grade)
12.1 Key storage
                     * Store provider keys in OS keychain:
                     * macOS Keychain
                     * Windows Credential Manager
                     * Linux libsecret
                     * Keys never written to logs.
                     * UI “Test Key” pings the provider safely.
12.2 Sandboxed execution for validators
Validators that execute code must run in a sandbox:
                     * restricted filesystem scope (workspace only)
                     * network disabled by default (toggle per project/policy)
                     * resource limits (CPU/mem/time)
12.3 Redaction
Before export:
                     * scan artifacts and logs for secrets
                     * redact
                     * emit redaction report
                     * mark bundle as redacted in manifest
________________


13) Licensing system (trial + full + update entitlement)
13.1 License goals
                     * Allow a time-limited trial people can actually evaluate.
                     * One-time full license (perpetual use).
                     * Optional update entitlement window (e.g., 12 months).
                     * Offline-first verification.
                     * Never brick user data; expired trial becomes read-only but exportable.
13.2 License types
                     * Trial: expires_at required, full features, soft caps allowed.
                     * Full: perpetual core, optional updates_until.
13.3 Recommended trial policy (ship this)
                     * 14-day trial
                     * full features
                     * soft caps:
                     * max_projects = 3
                     * max_workers = 2
                     * Exports allowed; Trace bundle includes license_mode: trial.
13.4 License token format
                     * Signed payload (Ed25519 recommended)
                     * Stored locally (file) + optionally mirrored in keychain
                     * Verification uses embedded public key
License payload fields:
                     * license_id
                     * type: trial/full
                     * issued_at
                     * expires_at (trial only)
                     * updates_until (full optional)
                     * limits
                     * machine_binding fingerprint hash (reasonable binding; allow 2 activations)
13.5 Enforcement behavior
                     * If trial expired or license invalid:
                     * allow opening projects, viewing IRs, exporting user data
                     * disable “run/compile new artifacts” OR keep compile but watermark bundle metadata (choose one; recommended: disable new runs but allow export)
                     * Never block data export.
13.6 Update entitlement
                     * SCW runs forever on full license.
                     * Auto-updater only pulls updates if current date <= updates_until (if set).
                     * Manual update download allowed but install checks entitlement.
________________


14) Targets/backends required in v1
To be truly “state-of-the-art,” ship multiple backends:
                     1. Python backend
                     * code generation + tests + CLI integration + doc stubs
                     * validators: ruff, py_compile, pytest, smoke runs
                     2. Docs backend
                     * README, tutorial, API docs, claims.json
                     * validators: markdown lint, claim/code cross-check
                     3. Narrative backend
                     * structured outline + beats + continuity ledger
                     * validators: continuity checks, constraints checks
                     4. Song backend
                     * structured sections + rhyme/meter policy + motif ledger
                     * validators: structure/meter heuristic checks (structured output)
(Optionally add a Slides backend later, but not required here.)
Each backend must:
                     * define its T-IR schema
                     * implement lowering rules from S-IR ops
                     * render artifacts + trace anchors
                     * provide validators
________________


15) Implementation stack (Codex must follow)
15.1 Preferred stack
                     * Rust for daemon/core
                     * Axum for local HTTP API
                     * Tauri + React/TypeScript for UI
                     * SQLite for index metadata
                     * Content-addressed filesystem store for artifacts
                     * Petgraph for DAG operations
                     * Diff engine (Rust crate) for patching
                     * Keyring crate for OS keychain
                     * Sandbox strategy:
                     * OS-level restrictions where possible
                     * optionally integrate lightweight container runner
15.2 Repo structure (must implement)
scw/
  apps/
    desktop/                 # Tauri UI
    cli/                     # CLI
  crates/
    api/                     # axum HTTP API
    core/                    # schemas + canonicalization + types
    plan/                    # plan parsing + lint + lock
    sir/                     # S-IR structs + lint + hashing
    compiler/                # plan->sir and sir->tir passes
    scheduler/               # critical path + slack + concurrency grouping
    router/                  # policy + tiers + openrouter client + adapters
    backends/
      python/
      docs/
      narrative/
      song/
    validators/              # validator registry + runners
    repair/                  # node-local repair + split-on-failure
    store/                   # sqlite index + CAS store + caching
    security/                # keychain + redaction + sandbox profiles
    license/                 # trial/full license verification + entitlement
    trace/                   # trace map generation + bundle export
    mcp/                     # optional MCP server mode
  schemas/
    plan.schema.json
    sir.schema.json
    schedule.schema.json
    trace.schema.json
    claims.schema.json
  fixtures/
    projects/                # golden test projects
  tools/
    installers/
  README.md


________________


16) Golden fixtures (must ship)
Create fixtures that SCW can compile and validate deterministically:
                     1. todo_cli_python
                     * plan defines CLI + JSON storage + tests + README
                     * expected: passing tests, docs aligned with CLI commands
                     2. mini_narrative_outline
                     * plan defines story constraints + beats
                     * expected: continuity ledger passes
                     3. song_structure_demo
                     * plan defines verse/chorus structure + rhyme rule
                     * expected: structure validator passes
Fixtures must be used in CI to ensure SCW itself remains correct.
________________


17) Acceptance criteria (definition of done)
Codex must deliver a system that:
                     1. Creates projects, edits plans, locks plans, generates plan hashes.
                     2. Compiles plan → S-IR DAG with stable IDs and no blocking lints for fixtures.
                     3. Builds schedules with critical path annotations and model assignments from policy.
                     4. Renders at least Python + Docs in one run, producing artifacts + trace maps.
                     5. Runs validators and returns structured failures tied to node IDs and file ranges.
                     6. Demonstrates node-local repair on an intentionally broken fixture (fails tests → repair → pass).
                     7. Exports Trace Bundle with full manifest and redaction report.
                     8. Stores provider keys in OS keychain and never logs them.
                     9. Supports trial license, trial expiry behavior, full license behavior, and update entitlement gating.
________________


18) Codex build instructions (how to execute)
Codex must:
                     * implement schemas first
                     * implement plan lock + canonicalization
                     * implement S-IR compiler passes
                     * implement one backend end-to-end (Python) including validators and traces
                     * implement docs backend and cross-check validator
                     * implement router + OpenRouter client + policy engine
                     * implement repair loop
                     * implement UI screens and CLI parity
                     * implement licensing + trial
                     * implement bundle export
                     * implement fixtures and CI tests
No partial delivery. No TODOs.
________________


19) Deliverables checklist (final)
                     * Desktop app (Tauri) on macOS/Windows/Linux
                     * Daemon with stable local API
                     * CLI with full coverage
                     * OpenRouter-first routing + two direct adapters
                     * Typed plan/sir/schedule/tir/trace/claims schemas
                     * Python + Docs + Narrative + Song backends
                     * Deterministic validators suite + sandbox profiles
                     * Node-local repair + split-on-failure
                     * Trace bundle exporter + redaction
                     * Trial + full licensing + updates entitlement
                     * Golden fixtures + automated test suite
________________


If you want, I can also output (in the same “hand to Codex” style) the complete JSON Schemas (plan/sir/schedule/trace/claims) and the exact UI field-level spec (node inspector fields, budget analytics fields, policy editor rules).


Tab 4
Absolutely — that’s a major moat addendum, and it fits your “compiler” framing perfectly:
                     * Forward direction: Plan → S-IR → T-IR → Artifact
                     * Reverse direction: Artifact → T-IR → S-IR (a decompiler / lifter)
                     * Then: Merge / reconcile / refactor at S-IR level
                     * Then: Recompile to a new unified artifact
Below is a Codex-ready addendum section you can append to the build document. It’s written to be implementable, not hand-wavy.
________________


ADDENDUM: Reverse Compilation (“Decompilation”) + Semantic Merge Foundry
A1) Purpose
Add a full reverse pipeline so SCW can ingest existing artifacts (repositories, documents, stories, songs) and lift them into Semantic IR (S-IR) as semantic atoms. This enables:
                     1. Semantic Mining: Convert existing projects into typed semantic atoms with provenance.
                     2. Semantic Merge: Combine multiple sources by merging their S-IRs under explicit conflict rules.
                     3. Semantic Refactoring: Reshape the combined concept at the semantic layer (change architecture, features, style, APIs).
                     4. Recompilation: Lower the merged S-IR into a new target artifact (codebase, book, etc.).
This is explicitly not “copy/paste code.” It’s structure-level synthesis with traceable provenance.
A2) New core concepts
A2.1 Lifted Semantic IR (LS-IR)
Introduce a parallel IR type: LS-IR (Lifted S-IR), identical schema to S-IR but with additional provenance fields:
                     * origin_kind: repo | doc | story | song | mixed
                     * origin_id: unique id per source artifact
                     * origin_refs[]: file paths, line ranges, doc spans, scene ids
                     * confidence: [0..1]
                     * lift_method: heuristic | parser | llm_extract | hybrid
                     * license_metadata: optional; stored as information only (see A8)
LS-IR nodes must be marked as either:
                     * semantic_claim: a belief about what the artifact does/means
                     * semantic_fact: strongly supported by deterministic signals (types, tests, AST analysis)
                     * semantic_guess: weakly supported (LLM inferred)
Only semantic_fact and semantic_claim are eligible for “hard constraint” status by default. semantic_guess must be soft until promoted by evidence or user approval.
A2.2 Semantic Knowledge Graph (SKG)
Add an internal graph store that persists semantics beyond a single run:
                     * Nodes: semantic atoms, entities, interfaces, invariants, modules, features
                     * Edges: depends_on, implements, conflicts_with, duplicates, refines
                     * Stored as: SQLite + graph tables OR embedded graph DB (prefer SQLite + adjacency for v1)
The SKG supports “Semantic RAG”:
                     * retrieval by feature, interface type, invariants, domain tags
                     * retrieval by similarity (optional embeddings) + symbolic filters
A2.3 Merge Bundle
A merge bundle is a curated S-IR created from multiple LS-IR sources plus merge decisions.
It contains:
                     * sources[] with fingerprints/hashes
                     * merge_policy
                     * conflict_resolutions[]
                     * result_sir.json
                     * trace links back to each origin
A3) Reverse pipeline: Artifact → LS-IR
A3.1 Code repository lifter (Repo → LS-IR)
Inputs
                     * repository path
                     * language detection
                     * optional: test commands, build commands
                     * optional: “important folders” list (src/, lib/, etc.)
Deterministic analysis (must)
                     * parse file tree
                     * detect languages and frameworks
                     * for supported languages:
                     * build AST index (tree-sitter at minimum)
                     * extract public interfaces (CLI entrypoints, exported functions/classes, HTTP routes)
                     * extract dependency graph (imports, module references)
                     * extract configuration schema (env vars, config files)
                     * detect tests and run tests (sandboxed) if possible
                     * extract docstrings / README claims
Output atoms (minimum set)
                     * DEFINE_INTERFACE (CLI/API/function signatures)
                     * DEFINE_SCHEMA (data models inferred from structs/classes/JSON usage)
                     * DEFINE_INVARIANT (e.g., “db path must exist”, “offline mode”, “id unique”)
                     * DEFINE_WORKFLOW (pipeline step ordering inferred from call graphs)
                     * IMPLEMENT_COMPONENT (mapped to modules)
                     * GENERATE_TESTS and RUN_TESTS (if tests exist)
                     * WRITE_DOC_SECTION (claims extracted from docs with pointers)
Confidence rules
                     * AST-derived interfaces: high confidence
                     * runtime behavior inferred without tests: medium
                     * anything inferred by LLM: marked guess unless validated
A3.2 Narrative/story lifter (Doc/Story → LS-IR)
Inputs
                     * plain text / markdown / docx import
                     * optional: chapter/scene segmentation hints
Deterministic analysis (must)
                     * segment into structure: acts/chapters/scenes/paragraph blocks
                     * entity extraction (characters, locations, objects) with coref heuristics
                     * event extraction (verbs/actions) + temporal ordering heuristics
                     * continuity ledger inference:
                     * states: location, possession, alive/dead, relationships
                     * transitions: events that change state
Output atoms
                     * DEFINE_ENTITY (characters/objects/locations)
                     * DEFINE_INVARIANT (world rules stated explicitly)
                     * WRITE_STORY_BEAT (beats with preconditions/postconditions)
                     * DEFINE_WORKFLOW (plot arcs as workflows)
                     * DEFINE_STYLE (tone, tense, POV) as a constraint capsule
Confidence rules
                     * explicitly stated facts (e.g., “John is dead”): claim with high confidence
                     * implicit facts (e.g., inferred location): claim medium
                     * inferred motives/themes: guess
A3.3 Song lifter (Lyrics → LS-IR)
                     * segment: verse/chorus/bridge
                     * extract motifs, rhyme scheme, meter (heuristic)
                     * atoms: WRITE_SONG_SECTION, DEFINE_STYLE, DEFINE_INVARIANT (structure rules)
A4) Merge system: LS-IR × LS-IR → Merge Bundle S-IR
A4.1 Merge policy (customer-configurable)
Provide merge policies that decide how to combine semantics:
                     * prefer_by_confidence: pick higher-confidence atoms when conflicts
                     * prefer_by_source_priority: user ranks sources
                     * prefer_by_validator_strength: pick atoms supported by tests/build
                     * prefer_modern_stack: prefer newer language/framework if user requests
                     * minimize_complexity: prefer fewer components if equal utility
                     * keep_both_as_variants: keep conflicting atoms as variants until chosen
A4.2 Conflict detection
A conflict exists when:
                     * two atoms define the same interface differently
                     * two atoms define incompatible invariants
                     * two workflows claim different step ordering for same output
                     * two entities have incompatible canonical properties (narrative)
Implement deterministic conflict checks:
                     * interface signature mismatch
                     * schema mismatch
                     * invariant contradiction (simple SAT-style checks for common invariants)
                     * name collision with different semantics
A4.3 De-duplication and aliasing
Introduce alias tables:
                     * entity aliasing (User, Account, Profile might merge)
                     * module aliasing (same role under different names)
                     * invariant aliasing (“offline-only” vs “no network”)
A4.4 Provenance preservation (non-negotiable)
Every merged atom must retain origin pointers:
                     * which repo/file lines or doc spans contributed
                     * which policy chose it
                     * which alternatives were rejected
This is stored in the Trace Bundle.
A5) Semantic Refactoring Workspace (“Shape the concept”)
Add a “Semantic Refactor” UI:
                     * view merged S-IR DAG
                     * edit/replace atoms
                     * promote/demote atoms (guess→claim→fact) with evidence
                     * restructure workflows (reorder, split, merge steps)
                     * choose between variants
                     * generate new acceptance tests derived from chosen invariants/interfaces
Hard rule: refactors operate at S-IR level; artifacts are regenerated from the new S-IR.
A6) Recompilation
Once merged/refactored S-IR is locked:
                     * generate targets with the existing forward pipeline
                     * validators ensure resulting artifact matches the merged semantics
                     * cross-checks ensure no “semantic leakage” from origins that were rejected
A7) New UI screens to add
                     1. Import / Lift Wizard
                     * choose sources (repos/docs)
                     * choose language/story mode
                     * run lifter
                     * show LS-IR summary + confidence distribution
                     2. Semantic Merge Studio
                     * select sources to merge
                     * choose merge policy
                     * conflict resolution UI
                     * preview merged DAG
                     3. Semantic Refactor Studio
                     * edit merged DAG
                     * manage variants
                     * regenerate acceptance tests
                     4. Provenance Viewer
                     * for any node: show source spans, confidence, lift method
A8) Legal/IP safety requirement (product integrity)
SCW must store and surface license metadata for imported repos (when available):
                     * parse LICENSE files and package metadata
                     * store license ID and origin URLs
                     * show warnings when attempting to merge incompatible licenses
                     * export bundles include provenance and license notes
Important: SCW is not a legal advisor; it must display license info and warn, not “guarantee compliance.”
A9) New CLI commands
                     * scw lift repo <path> --out <lsir.json>
                     * scw lift doc <file> --out <lsir.json>
                     * scw merge --sources a.lsir.json b.lsir.json --policy merge_policy.json --out merged.sir.json
                     * scw refactor <merged.sir.json> --apply <refactor_patch.json>
                     * scw provenance <node_id>
A10) New acceptance criteria
                     * Can lift a repo fixture into LS-IR with correct interface extraction and dependency graph.
                     * Can lift a narrative fixture into LS-IR with entities + beats + continuity ledger.
                     * Can merge two repo LS-IRs with conflict detection and provenance preserved.
                     * Can refactor merged S-IR and recompile to a clean new artifact.
                     * Trace bundle includes origin pointers for every merged node.
________________