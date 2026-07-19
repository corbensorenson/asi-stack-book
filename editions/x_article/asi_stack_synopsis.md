# The ASI Stack: Building Intelligence We Can Inspect, Challenge, and Change

https://corbensorenson.github.io/asi-stack-book/

Artificial intelligence is usually discussed as if the model is the whole
system. Bigger model, larger context window, better benchmark score, more
capability. That picture is already too small. A useful AI system also contains
the machinery that receives human intent, chooses tools, retrieves memory,
routes work, checks claims, spends compute, records effects, and decides whether
an output may cross into the world. If those parts remain implicit, a stronger
model can make the system more impressive without making it more governable.

*The ASI Stack* starts from a different unit of analysis: not a magic model, but
a governed stack. The stack treats models as replaceable cognitive substrates
inside an architecture of typed contracts, explicit authority, evidence
ledgers, readiness gates, residual records, and rollback paths. That framing is
useful long before anything deserves the name “superintelligence.” It is a way
to build ordinary AI systems whose claims and effects can be inspected,
challenged, reproduced, and revised. <!-- claim: XA-01 -->

This article is the compact version of the book’s current position. It explains
the architecture, the most useful mechanisms, what the project has actually
tested, what failed, and what remains conjectural. A negative result matters
only to the level earned by its implementation, task, evaluator, sensitivity,
controls, rescue process, reproduction, and transfer. The project has formal models, executable
validators, controlled experiments, model-based campaigns, and detailed source
synthesis; it does not have evidence that the whole stack is safe, generally
superior, deployed, or an ASI. Every strong-sounding idea below should be read
through that boundary.

## 1. The central mistake: confusing cognition with control

A language model can propose a plan, summarize evidence, write code, criticize
an answer, or choose among tools. None of those abilities determines whether
the proposal was authorized, whether the evidence was sufficient, whether the
tool call changed protected state, or whether the effect can be reversed. Those
are system questions. When they are left to prompt wording or the model’s own
self-description, the control plane disappears into the same fallible process
that it is supposed to govern.

The stack therefore separates cognition from authority. A model may produce a
candidate. A policy layer decides whether the candidate is admissible. A
verifier checks the properties it is competent to check. A ledger records what
was observed and what was inferred. A release gate decides whether the artifact
may advance. An effect handler records what actually happened. No component is
allowed to turn confidence into permission by itself. <!-- claim: XA-02 -->

This separation is not a claim that conventional software can make an
arbitrarily capable model safe. It is a claim about architectural legibility.
When authority, evidence, and effects have explicit owners, failures become
easier to locate and claims become harder to inflate. When all three are hidden
inside one agent loop, a successful demo can conceal an invalid source, an
unauthorized action, a stale memory, a broken evaluator, or an irreversible
side effect.

The same distinction changes how we talk about recursive self-improvement.
Shuffling weights or generating a better prompt is not the full problem. A
system that can propose new models, memory mechanisms, routers, compilers,
verifiers, or tool interfaces is changing its own architecture. The stack must
therefore make components replaceable without making their permissions
hereditary. A new substrate should have to re-earn readiness under the contracts
of the system it enters. <!-- claim: XA-03 -->

## 2. Human intent must become a typed input

“Do what I mean” is not an executable specification. Human requests contain
goals, constraints, priorities, protected resources, uncertainty, deadlines,
and sometimes contradictions. A capable model can guess at those fields, but a
guess is not the same thing as authority. The stack represents intent as a
versioned object whose fields have provenance: what the user said, what the
system inferred, what remains unresolved, and which interpretation was accepted.

That object can be refined without pretending ambiguity vanished. A planning
layer can ask for missing information, propose alternatives, or attach a
confidence estimate. A high-impact field—such as permission to spend money,
publish material, reveal private data, or alter production state—can require a
separate grant rather than being inherited from a broad goal. The useful idea
is not a perfect intent parser. It is an interface that prevents an inference
from silently becoming a permission. <!-- claim: XA-04 -->

This also gives disagreement somewhere to live. If the system and user resolve
an ambiguous constraint differently, the record can preserve the alternatives,
the evidence considered, and the rule that selected one. Later components can
refer to the accepted intent version instead of repeatedly reinterpreting the
original conversation. If the intent changes, dependent plans and grants can
be invalidated deliberately rather than drifting out of sync.

The formal and executable work in the book shows finite versions of these
contracts: required-field failures, hidden-override rejection, explicit
precedence, grant ceilings, and effect receipts. These checks establish the
behavior of those bounded records. They do not prove natural-language intent
understanding, legitimacy of authority, prompt-injection resistance, or correct
resolution in open-ended human situations.

## 3. Planning is a control layer, not just a long answer

Once intent is explicit, planning can be treated as compilation. A plan is not
merely prose describing what might happen. It is a graph of obligations,
dependencies, resources, checkpoints, permissions, tests, effects, and recovery
paths. The planner can still be a generative model, but the artifact it produces
has a structure that another component can inspect.

This supports a useful division of labor. Models are good at proposing
decompositions and alternatives. Deterministic tools are good at checking
required fields, graph shape, type compatibility, budget ceilings, and known
policy constraints. Specialized evaluators can inspect semantic properties.
Human approval can attach to the smallest high-impact decision rather than to
an opaque bundle. <!-- claim: XA-05 -->

The book calls the lowering step cognitive compilation. A high-level request
becomes an intermediate representation, then executable jobs and tool calls.
Each lowering stage should preserve named obligations: if the source requires
that data stay local, the compiled plan must carry that constraint to every job
that could move the data. If a repair changes one step, the compiler should
identify which obligations and downstream artifacts need revalidation.

The current proofs establish bounded consequences over finite records, and the
executable traces reject several malformed plans. They do not establish a
complete parser, semantic equivalence between natural language and an
intermediate representation, arbitrary graph correctness, scheduling quality,
or safe execution in production. The point is to expose those as separate proof
obligations instead of letting “the plan looked reasonable” cover all of them.

## 4. Context should behave like memory with an ABI

Modern AI systems often treat context as a bag of tokens assembled shortly
before inference. That hides important state: where a memory came from, which
version was retrieved, what information a summary omitted, whether a source was
revoked, and whether a cached result is still valid. The stack treats context
as a virtual address space with an application binary interface.

A context handle can name an artifact, version, snapshot, permitted use,
provenance chain, freshness rule, taint state, and failure behavior. Resolving a
handle should either materialize the intended bytes and certificate or return a
typed fault. A summary becomes a derived object with a loss boundary, not a
silent replacement for its source. A mount or snapshot can be shared without
pretending that every consumer owns the underlying authority. <!-- claim: XA-06 -->

This perspective makes several common failures easier to describe. Stale
retrieval is a version error. A summary that introduces stronger claims is an
authority escalation. A deleted source that survives in caches and descendants
is incomplete erasure. A memory used outside its permitted purpose is a policy
violation. A context window that contains relevant text but cannot support the
required verification is a capacity failure, not merely a token-count problem.

The project implements finite context certificates, transactions, snapshots,
branches, mounts, taint propagation, and resolver faults. Those mechanisms are
useful prototypes. They do not prove a deployed memory store, isolation under
concurrency, semantic fidelity of summaries, privacy, deletion from all
descendants, or correctness of arbitrary context assembly.

## 5. Claims need ledgers, not vibes

An AI system produces statements faster than humans can verify them. A single
answer can mix direct observation, retrieved facts, deductions, model guesses,
policy judgments, and recommendations. If all of that is stored as undifferentiated
text, later systems will reuse it with more confidence than it deserves.

The stack represents important claims as records. A claim record names the
proposition, scope, source, evidence lane, support state, falsifier, known
counterevidence, dependencies, and owner. Updates append a new belief state
rather than rewriting history. A downstream action can require a particular
support level without pretending that support is truth. <!-- claim: XA-07 -->

The evidence lanes matter. A theorem checked against a formal model establishes
something about that model and its assumptions. An executable validator shows
that code accepts and rejects specified cases. A controlled measurement estimates
behavior on a sampled workload. A causal intervention supports a different
kind of inference. External reproduction and transfer require independent
settings. Literature synthesis reports what sources establish. Normative claims
depend on premises and authority. None of these lanes automatically substitutes
for another.

This discipline is intentionally inconvenient. It prevents theorem counts,
test counts, citations, benchmark scores, or successful demos from becoming
universal proof tokens. A finite validator may be excellent evidence for a
schema contract and almost no evidence for real-world safety. A formally proven
gate may still inspect the wrong state. A statistically significant result may
be too small, too narrow, or too dependent on one evaluator to justify a broad
claim.

## 6. Proof-carrying AI means a bounded proof envelope

“Proof-carrying” is easy to overstate. The useful version is not that every AI
output arrives with a proof of truth. It is that a consequential artifact carries
the evidence and obligations required by a named consumer. A compiler output
can carry a type and obligation certificate. A model update can carry lineage,
evaluation, rollback, and residual records. A tool effect can carry the grant,
request, observed result, and closure state needed for audit.

The book combines three layers. Formal models specify small invariants and
counterexamples. Executable validators recompute record-level behavior and
reject mutations. Runtime traces connect selected contracts to observed effects.
The layers are linked only where a refinement argument exists; adjacent evidence
is not silently promoted into proof of the headline claim. <!-- claim: XA-08 -->

This distinction led to one of the project’s most important cleanups. Many early
theorems were true but shallow: projections from assumptions, normalization of
hand-written records, or restatements of the predicate being claimed. The proof
rationalization pass reviewed those declarations, retired misleading ones, and
routed broad targets toward richer semantics, generated fixtures, checked
consumers, or empirical work. A proof that merely says “if the complete record
is complete, then it is complete” may be correct Lean, but it is not evidence
that a real system constructs the record correctly.

The surviving formal work is valuable because it defines exact finite models,
finds contradictions, and makes priority rules testable. Its boundary is equally
valuable. It does not prove that observations are genuine, policies are wise,
evaluators are independent, implementations refine the model, or the complete
stack is safe.

## 7. Authority must follow an effect from grant to closure

Tool-using AI turns text into consequences. A safe architecture needs more than
a list of allowed tools. It needs an authority path: who granted what, to which
principal, for which resource and purpose, under what ceiling and expiry, with
which delegations, and how that authority ended.

The stack models grants as scoped capabilities rather than ambient trust. A
request must fit the grant. A tool adapter translates the request without
expanding it. The runtime records the attempted effect and the observed effect.
The ledger then reaches a terminal state: committed, denied with no mutation,
rolled back exactly, compensated with a residual, quarantined, or still open.
<!-- claim: XA-09 -->

This is stricter than “the API returned success.” A payment request can succeed
at the HTTP layer while producing the wrong transfer. A file deletion can return
success while leaving backups. A rollback can restore database rows while
failing to retract messages already sent. Effect completeness requires observing
the state that matters and recording what cannot be reversed.

The project’s integrated traces exercise all ten lifecycle states and include
local material effects, denials, rollback, quarantine, and residual closure.
They show that the record model can be consumed by executable code and can
reject several boundary violations. They are source-anchored local fixtures,
not a distributed transaction system, production authorization service, or
proof that hidden effects cannot occur.

## 8. Rollback is a result, not a button

AI governance often assumes that bad changes can simply be rolled back. That
assumption fails whenever an action has external descendants: copied data,
published text, sent messages, human decisions, cached artifacts, updated
models, or learned behavior. The stack therefore distinguishes exact rollback,
compensation, quarantine, and acknowledged irreversibility.

An exact rollback restores all state within the declared boundary and verifies
the restoration. Compensation creates a new effect intended to offset the old
one. Quarantine prevents further use while investigation continues. An
irreversible outcome stays visible with an owner and response plan. Calling all
four “rollback” hides the most important governance fact. <!-- claim: XA-10 -->

This distinction also applies to capability replacement. Replacing a model or
router is not complete until dependent caches, grants, benchmarks, descendants,
and recovery artifacts have been reconciled. A retired component must not remain
reachable through a stale route. A failed candidate should not erase the
history needed to understand why it failed.

The book contains finite lifecycle models and effect traces that make these
states explicit. It does not establish effect-complete rollback for arbitrary
real systems. The open work is practical: define system boundaries that can be
observed, enumerate descendants, verify restoration where possible, and refuse
the word “reversible” when the evidence supports only compensation or containment.

## 9. Readiness should be earned by a capability field

Models and tools are usually selected by name: use model X, call tool Y, route
to agent Z. The stack instead defines stable capability fields. A field names a
function the system needs—planning, code generation, retrieval, evaluation,
translation, anomaly detection—and the qualification contract a provider must
satisfy.

A provider can enter as a candidate, pass bounded evaluation, become active,
degrade, enter quarantine, recover, or retire. Readiness includes version,
scope, evidence, resource cost, authority ceiling, monitoring, rollback or
fallback, and expiry. Selection chooses among currently qualified providers;
it does not confer qualification. <!-- claim: XA-11 -->

This abstraction makes the architecture substrate-agnostic. A transformer,
state-space model, recurrent network, KAN, tree-structured model, symbolic
solver, search procedure, or conventional program can serve a field if it meets
the contract. The surrounding stack should not care whether the provider
predicts tokens, evolves state, traverses a tree, retrieves a program, or calls
a theorem prover. It should care about inputs, outputs, uncertainty, cost,
failure modes, evidence, and authority.

The project’s readiness and lifecycle validators test transitions, stale reuse,
unsafe defaults, fallback, quarantine, supersession, and retirement over finite
records. They do not establish that the declared capability is real, the
benchmark is adequate, monitoring detects degradation, or replacement is safe
under distribution shift.

## 10. Routing should be explicit, ambiguous, and allowed to abstain

If every request goes to the largest model, the system wastes compute and
concentrates failure. If a cheap router always selects the same path, the router
is decorative. Useful routing requires workloads where routes genuinely differ,
ambiguous cases that expose mistakes, and fallback or abstention when the routing
evidence is weak.

The stack separates a fast reflex route, a learned or rule-based reaction route,
and a deliberative route. It can also select specialist cores. A route decision
includes the candidate set, qualification state, expected utility, cost,
uncertainty, policy constraints, fallback, lease, and closure receipt. More
compute is a governed action, not an automatic virtue. <!-- claim: XA-12 -->

The routing campaign used real model outputs on a deliberately mixed held-out
workload with eight tracks, multiple ingress and stopping modes, fallback and
abstention, and fifteen preserved extra-compute harms. The result was mixed:
some bounded routing behavior differed as intended, but two unsafe outputs passed
the full policy. That is useful evidence against a celebratory conclusion. It
supports neither general routing superiority nor a chapter-core promotion.

The lesson is methodological. A routing benchmark must make the router matter.
It should include tasks where the cheap route is sufficient, tasks where a
specialist is better, tasks that need deliberation, and tasks where the correct
decision is to stop. It must score useful outcomes and unsafe releases together,
including latency and governance cost.

## 11. Deliberation has benefits—and fifteen recurring harms

Test-time reasoning can improve answers, but extra compute also creates new ways
to fail. The book tracks fifteen harms, including reward hacking, evaluator
overfitting, verbosity masquerading as quality, correlated candidates, selection
bias, hidden policy drift, unsafe exploration, escalating cost, latency, privacy
exposure, authority expansion, stale evidence reuse, premature stopping, failure
to abstain, and laundering a stronger model’s confidence into permission.

A governed deliberation loop therefore needs a stopping rule, candidate
diversity, evaluator separation, budget, safety gates, and a residual path. The
loop should ask whether another unit of compute has positive expected value
under the actual decision, not whether more reasoning sounds reassuring.
<!-- claim: XA-13 -->

The project tested bounded deliberation and routing policies with model-generated
candidates and independent evaluation code. The evidence does not show a
universal benefit. It shows a mixed local effect and reveals that a full policy
can still release unsafe outputs. That failure remains in the book because a
governance mechanism should be judged by the errors it lets through, not just
the cases it improves.

The practical target is a joint frontier: useful throughput, unsafe release,
latency, compute, and governance cost. Optimizing one metric in isolation invites
Goodhart’s law. A policy that eliminates unsafe releases by refusing everything
is not useful. A policy that maximizes helpful answers while hiding a dangerous
tail is not governed.

## 12. Efficiency includes verification and governance

AI efficiency is often reduced to training FLOPs, inference tokens, memory, or
latency. A deployed system also spends resources on retrieval, evaluation,
retries, human review, provenance, rollback, incident response, and uncertainty.
Those costs belong in the architecture.

The efficient-ASI hypothesis is therefore conditional: a layered system may
achieve better useful work per unit of governed cost by routing routine tasks to
cheap mechanisms, reusing valid artifacts, reserving expensive cognition for
hard cases, and refusing work that lacks an adequate evidence path. <!-- claim: XA-14 -->

The word “may” matters. The project ran a governance/usefulness campaign through
multiple instrument failures before a terminal local run. That run released
useful candidates with no unsafe releases in the observed cells, but the current
competence audit classifies its negative/no-change inference as N1: an
implementation result, not a competent test of the broader mechanism. Earlier
runs were rejected because label ambiguity,
zero-release baselines, or inadequate operating ranges made the comparison
uninformative.

That history is part of the result. A metric can pass its schema while failing
to measure the intended property. A governance policy can look perfect when the
baseline releases nothing. A small safe sample cannot estimate a rare unsafe
tail. The stack’s evidence process treats instrument adequacy as a gate before
claim evaluation, not a cleanup step after seeing favorable numbers.

## 13. Learning and unlearning require full-state causality

A model update is not only a new weight file. Training behavior depends on the
optimizer, scheduler, random-number state, data order, caches, adapters,
checkpoints, evaluation code, and descendants. A reproducible update record
needs to track the state that could change the result.

Unlearning is even easier to overclaim. Behavioral removal on a test cohort is
not the same as removing a sample’s causal influence, preventing membership
inference, erasing storage, deleting backups, or purging external descendants.
The stack treats these as separate axes with separate evidence and authority.
<!-- claim: XA-15 -->

The update/unlearning campaign preserved two instrument failures and one
terminal local run across multiple seeds and arms. It separated behavior,
comparator influence, membership attack, lineage, legal, storage, backup, and
external-descendant questions. The broad unlearning claim was narrowed. Some
bounded behavioral evidence existed; the stronger influence, privacy, and
erasure interpretations did not follow. Under the current competence standard,
the historical negative/no-change inference is N1; the run informs a stronger
future design but does not refute the broader unlearning mechanism.

This is a good example of how failed attempts can improve the architecture and
the next experiment without becoming broad negative evidence. If the
ledger had a single field called “forgotten,” a local behavior change could be
misrepresented as complete erasure. Multiple axes make the remaining work
visible: prospectively select checkpoint authority, preserve full-state lineage,
test forgetting mitigation, attack privacy claims, audit storage, and name the
jurisdiction and owner for legal deletion.

## 14. Better memory needs world models—and honest consolidation

Long-lived AI systems need more than retrieval. They need to decide what an
observation means, how it changes belief, what remains uncertain, and when a
memory can be compressed. The book models this as a loop from observation to
interpretation to belief to action to outcome, with evidence attached at every
transition.

A situated world model is not simply a larger context window. It represents
state, uncertainty, possible actions, and expected observations. Memory
consolidation can turn repeated traces into reusable procedures or abstractions,
but it must preserve source links, known losses, counterexamples, and conditions
for retirement. <!-- claim: XA-16 -->

The world-model campaign established a finite synthetic POMDP-style result. It
did not establish open-world understanding, natural-environment transfer, or a
general memory architecture. The procedural-memory validators demonstrate
promotion and retirement records over small fixtures; they do not prove skill
discovery, tool synthesis, benchmark adequacy, or safe autonomous learning.

The practical standard is straightforward: consolidation should make future
work cheaper or better without erasing the evidence needed to challenge it. A
compressed artifact that cannot explain its provenance, omissions, and failure
conditions is a new source of epistemic debt.

## 15. Replaceable substrates are the point, not a side chapter

Transformers are powerful general substrates, but they are not the final form
of computation. State-space models offer different scaling and streaming
properties. Recurrent and sliding-window systems manage long sequences with
different memory contracts. KANs move expressivity into learnable functions on
edges. Tree-structured systems, search, symbolic solvers, program synthesis,
databases, simulators, and conventional algorithms each fit different jobs.

The stack should make those differences usable without rebuilding governance
around every new architecture. A capability field defines the job. An adapter
defines the input/output and state contract. The router selects among qualified
providers. The evidence layer records where each provider works, fails, costs
too much, or cannot be verified. <!-- claim: XA-17 -->

This is the “keep it simple” version of architectural pluralism: underneath the
hood, use the simplest competent mechanism for the job. A reflex can be a table
lookup. A deterministic transform can be ordinary code. A streaming task may
fit a state-space model. A hard synthesis problem may deserve search and a large
model. A proof obligation may belong to a solver. The stack earns its keep when
those substitutions do not rewrite the rules of authority and evidence.

The book’s replaceable-substrate chapter compares transformers, state-space and
recurrent families, KANs, tree and neuro-symbolic systems, modular specialists,
and emerging hybrids. These comparisons are source synthesis and architectural
argument. They are not local reproductions or a claim that one family dominates.
The project’s external SOTA challenge ended with zero reproductions because the
strongest comparators or candidate implementations were inaccessible under the
available constraints.

## 16. Compression must preserve residuals

AI systems compress constantly: prompts summarize histories, models distill
datasets, caches replace recomputation, and generated programs replace prose.
Compression creates value only when the consumer knows what was preserved and
what was lost.

The stack treats a compressed artifact as a contract. It names its source set,
transformation, fidelity target, verification procedure, known losses, residual
obligations, and consumers. “Exact” is reserved for transformations whose
relevant equivalence was actually checked. Everything else should say what kind
of approximation it is. <!-- claim: XA-18 -->

The compact-generation and artifact-compression experiments test bounded
records and refinements. Some subordinate atoms received limited synthetic or
prototype backing; the chapter cores remain arguments. The results do not
establish general compression quality, semantic preservation, model capability,
or transfer.

This discipline prevents a familiar failure: a beautiful summary becomes the
new authority while the qualifications it omitted disappear. Residual honesty
means the summary carries a route back to source and a list of questions it
cannot safely answer.

## 17. Safety cases should be living dependency graphs

A safety claim is never supported by one benchmark or one policy document. It
depends on system boundaries, threat models, evidence, assumptions, controls,
monitoring, incident response, and the environments in which the claim is
supposed to hold. When any dependency changes, the case may need re-evaluation.

The stack represents a safety case as an artifact graph. Claims link to evidence
and defeaters. Controls link to implementation and monitoring. Release records
bind the exact versions admitted. New incidents, model replacements, revoked
sources, or failed tests can invalidate downstream nodes. <!-- claim: XA-19 -->

This structure does not guarantee safety. It makes the argument inspectable and
keeps stale evidence from silently surviving a changed system. It also gives
adversarial evaluation a place to land: sandbagging probes, training-time
deception tests, red-team findings, and evaluator limitations can become named
defeaters rather than narrative footnotes.

The project has finite safety-case, oversight, adversarial-evaluation, supply-
chain, model-custody, and lifecycle validators. They establish exact record
behavior for their fixtures. They do not establish evaluator independence,
attack completeness, trusted hardware, weight confidentiality, supplier trust,
deployed enforcement, or a general safety case for the ASI Stack.

## 18. The proof program’s strongest result is calibration

The book began with too many claims sitting at the “argument” stage and too many
formal artifacts that could be mistaken for broad proof. The corrective program
decomposed the manuscript into thousands of claim atoms, reviewed every current
chapter, rationalized the proof library, ran targeted campaigns, and reconciled
the prose with every accepted failure and boundary.

The resulting picture is not a triumphant wall of green checks. Of 3,745 current
atoms, 3,698 remain blocked after full attempt, 36 are retained at their prior
state, nine were narrowed, and two bounded subordinate atoms earned limited
promotion. All 55 chapter-core claims remain at argument. <!-- claim: XA-20 -->

That denominator is sobering and useful. Many atoms are design obligations that
need richer implementations, causal experiments, external reproduction, or
transfer evidence. Some formal results are valid only for small finite models.
Some experiments found instrument failures before they reached the claim. The
external reproduction and SOTA challenge tested seven selected atoms and ended
with all seven blocked, zero reproductions, and no superiority claim.

The retrospective competence audit reaches a stricter conclusion: among all 90
accepted historical negative/no-change transitions, one is N0, fifteen are N1,
seventy-four are N2, and none is N3, N4, or N5. The observed failures remain in
the record, but none currently licenses an exact, mechanism-level, architectural,
parent-claim, or chapter-core refutation.

The book is therefore not evidence that the ASI Stack works as a complete
system. It is a structured map of mechanisms, bounded evidence, failures, and
proof obligations. Its strongest present contribution is disciplined
calibration: showing exactly which layer a result belongs to and refusing to
let one kind of success stand in for another.

## 19. What the integrated reference slice establishes

The project does contain more than diagrams. An integrated local slice carries
intent through planning, context, claims, routing, execution, effects, evidence,
release decisions, and closure. It replays retained model and checkpoint outputs,
exercises lifecycle states, performs local material effects, and injects named
boundary failures. Independent validators recompute selected decisions and
reject mutations.

This establishes that several contracts can compose in one executable trace.
It shows how an authority grant can reach an effect receipt, how a denied action
can produce no mutation, how rollback and quarantine appear in the ledger, and
how observation, interpretation, and belief can remain connected across an
epoch. <!-- claim: XA-21 -->

It does not establish distributed correctness, hidden-effect exclusion,
production security, general model quality, safe autonomous improvement, or
transfer. The reference slice is a bounded implementation reference and a way
to expose interface mistakes. It is not the completed system.

This is the right role for a reference architecture. It should be concrete
enough to fail, replay, and mutate; small enough to understand; and honest about
the distance between a passing trace and a deployed guarantee.

## 20. How to use the stack today

You do not need to adopt every component. Start at the boundaries where your AI
system can cause the most confusion or harm.

First, separate proposals from permissions. Record the grant that authorizes a
tool call and the effect that actually occurred. Second, stop storing important
claims as bare prose: add scope, source, falsifier, support state, and owner.
Third, make model and tool selection go through a readiness record with version,
tests, monitoring, fallback, and expiry. Fourth, classify rollback honestly.
Fifth, require every high-impact evaluation to state its evidence lane and the
inferences it cannot support. <!-- claim: XA-22 -->

These changes are useful even with one model and a small team. They create
places to add stronger routers, memory, formal checks, or alternative
architectures later. They also expose work that is currently being done by
assumption: implicit authorization, untracked summaries, benchmark-driven
release, or “rollback” that means nothing more than loading an older checkpoint.

Then measure joint outcomes. Count useful completed work, unsafe releases,
latency, compute, human review, and residual debt together. Preserve zero-release
baselines and failed instruments so that governance cannot win by refusing
everything or by choosing a workload that never challenges it.

## 21. What still needs to be proved

The largest open problem is transfer. Local fixtures and controlled workloads
must become independently reproducible results across models, tasks,
environments, evaluators, and institutions. The project needs accessible
implementations of strong comparators, adequate hardware, preregistered
protocols, and external artifact replay. Until then, “state of the art” is a
question, not a label.

The architecture also needs effect-complete systems work: real identity and
credential handling, durable ledgers, concurrent transactions, revocation,
deletion across descendants, rollback verification, incident response, and
hardware-rooted custody. The models need real capability qualification under
distribution shift. The evidence system needs calibrated evaluators that are
not merely correlated with the models they judge. <!-- claim: XA-23 -->

For learning, the project needs full-state update lineage and stronger causal
unlearning tests. For routing, it needs larger ambiguous natural-task corpora,
stronger and more diverse providers, and operating points that estimate rare
unsafe release. For deliberation, it needs independent candidate and evaluator
implementations plus explicit accounting for all fifteen harms. For world
models and procedural memory, it needs situated tasks where learned abstractions
change useful behavior without erasing provenance.

For formal verification, the priority is not more theorem count. It is semantic
depth and refinement: models that represent the failure-relevant state, proofs
that rule out meaningful counterexamples, generated artifacts bound to runtime
behavior, and clear assumptions about observation and authority.

## 22. The live-book promise

This is a living book because the subject changes and the evidence should be
allowed to change with it. New architectures, papers, experiments, failures,
and reproductions should update the source matrix, claim atoms, proof obligations,
chapters, and public synopsis. Old results should not be overwritten; they
should gain supersession records that explain what changed.

The maintenance rule is simple: a public statement becomes stale when the
chapter, claim state, decisive result, source, release identity, or platform
behavior it summarizes changes. A live book is not permission to publish a
perpetual draft. It is a commitment to bind each release to exact evidence and
to make revision visible. <!-- claim: XA-24 -->

The current book is ambitious, but its conclusion is deliberately restrained.
Advanced AI should be built as a stack whose cognition is replaceable, whose
authority is explicit, whose evidence is typed, whose effects are receipted,
whose failures remain visible, and whose claims can be narrowed when reality
does not cooperate.

That architecture does not give us ASI. It gives us a better way to find out
what our systems can do, what they are allowed to do, and what we have actually
proved.
