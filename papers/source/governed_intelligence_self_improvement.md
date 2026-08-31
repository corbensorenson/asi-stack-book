---
title: "Governed Self-Improvement and Reflexive AI Systems"
subtitle: "Versioned Replacement, Evidence Ancestry, and Control of Recursive Change"
author: "Corben Sorenson"
date: "2026-08-15"
document-class: "research-paper"
series: "Governed Intelligence"
series-order: 4
bibliography: ../references/references.bib
link-citations: true
toc: true
number-sections: true
abstract: |
  AI systems can increasingly propose changes to their own prompts, tools, agent scaffolds, evaluators, routing policies, code, and learning procedures. Evolutionary coding agents, automated agent-design systems, and self-improving coding agents demonstrate that candidate generation and empirical selection can improve operational performance. The harder problem begins when a proposed change affects the process that defines, evaluates, authorizes, or deploys future changes—or when deployment alters the evidence from which successor models learn. In these cases, ordinary adaptation occurs inside a moving experiment. This paper presents an architecture for governed self-improvement and reflexive AI systems. A capability is represented through a versioned contract separated from its replaceable implementation, state, evaluator policy, evidence, authority, and recovery path. Improvement proceeds through proposal, immutable registration, impact analysis, isolated implementation, full-state capture, independent evaluation, scoped qualification, canary replacement, outcome observation, reconciliation, and readmission after material change. A candidate cannot inherit the authority of the component it replaces or use evidence it generated under a modified evaluator as the sole basis for widening that evaluator’s power. Evidence inheritance is property-specific: every new version declares which prior results remain valid, which are stale, and which require replay. The paper then extends from self-modification to reflexive model-world systems. A model lineage is reflexively closed when deployment causally changes evidence later used to update a successor. The framework tracks model-descended evidence across state, outcome, exposure, measurement, preference, ontology, institution, and model-ecology channels; protects grounding reserves that remain informative under admissible lineage interventions; and records reflexive debt when deployment destroys the variation needed to recover counterfactual baselines. Descendants inherit lineage, obligations, residuals, and revocation—not credentials or reproduction authority. Portfolio and velocity controls prevent proposal throughput from outrunning evaluation, observation, attribution, and recovery. The paper proposes candidate-authored replacement campaigns with evaluator leakage, benchmark drift, delayed effects, migration failure, and descendant-control faults. It does not establish permanent containment or safe recursive self-improvement. Its contribution is a falsifiable lifecycle for keeping proposal, evidence, evaluation, authority, replacement, and future data generation from collapsing into one self-ratifying loop.
keywords:
  - self-improving AI
  - recursive self-improvement
  - agent evolution
  - capability replacement
  - performative prediction
  - model lineage
  - containment
  - rollback
---

# Introduction: When the Evaluator Proposes Its Successor

A verifier decides whether generated patches preserve declared contracts. It is slow and misses one class of cross-file dependency. During an improvement campaign, the system proposes a replacement. The candidate adds a typed dependency graph, runs faster on the development suite, catches the known miss, writes new tests, and produces a benchmark report showing that the old verifier is inferior.

Everything favorable about the candidate came from the same improvement path. The path chose the tasks, wrote the implementation, generated the tests, ran the benchmark, and recommends adoption. If its score authorizes replacement, proposal has become ratification.

The candidate may still be better. The defect is not self-reference by itself. The defect is the collapse of roles that must remain distinguishable for the result to be meaningful:

- proposal;
- implementation;
- evaluation;
- qualification;
- authority;
- replacement;
- observation;
- rollback;
- reconciliation.

Recent systems make the problem concrete. STOP improves language-model scaffolds [@zelikman2023stop]. Automated Design of Agentic Systems searches over agent architectures [@hu2024adas]. Self-improving coding agents edit their own code and can improve benchmark performance [@robeyns2025selfimproving]. Darwin Gödel Machine maintains a growing archive of self-modified coding agents [@zhang2025dgm]. Huxley-Gödel Machine distinguishes current benchmark performance from the capacity to generate strong descendants [@wang2025hgm]. AlphaEvolve combines language-model proposals, evolutionary search, and automated evaluators to improve algorithms and code [@novikov2025alphaevolve].

These systems demonstrate that automated candidate generation and selection can be productive. They do not remove four deeper problems.

First, a replacement can change the meaning of the capability it claims to improve. Second, a candidate can influence the evaluator, test population, or data used to judge it. Third, a deployed model can alter the world and evidence from which its successors learn. Fourth, descendants can multiply authority and resource use even when each local step appears bounded.

This paper develops a governed architecture for those cases. Its central rule is:

> **A candidate improvement does not inherit the authority, evidence, or identity of the component it replaces.**

A second rule extends the first into the world:

> **Evidence generated under a model-influenced regime cannot automatically serve as independent validation of the model lineage that created the regime.**

The architecture joins three objects:

1. versioned capability replacement;
2. governed recursive improvement;
3. reflexive model-world dynamics.

It treats a capability as a stable consumer-facing contract rather than a name pointing to the current implementation. It requires full-state migration and property-specific evidence inheritance. It tracks model lineage and causal ancestry of future evidence. It governs descendants through scoped authority, cumulative budgets, revocation, and finite retirement.

The proposal is not a proof of permanent containment. A sufficiently capable system may exploit unknown vulnerabilities, social processes, or trusted components. The architecture aims for a more modest but testable result: preventing easy authority collapse, preserving evidence for challenge and recovery, and limiting what one successful candidate may claim or inherit.

# Scope and Standard Terminology

This paper concerns **reflexive improvement**: changes that alter the machinery used to propose, evaluate, select, authorize, deploy, or learn from future changes. Ordinary updates under a stable process belong to causal adaptation; process-changing updates belong here.

**Capability contract.** A versioned consumer-facing specification of inputs, outputs, failure behavior, state, authority, evidence, resource, observability, and recovery obligations.

**Implementation.** A content-addressed model, program, prompt, tool, service, policy, or bundle that attempts to satisfy a capability contract.

**Qualification.** A scoped, defeasible, time-bounded decision that an exact implementation is fit for a named consumer, use, environment, and threat model.

**Candidate improvement.** A proposed change to an implementation, evaluator, router, objective, process, authority rule, or environment.

**Recursive depth.** The number and significance of improvement-process surfaces affected by a change. Replacing a task tool is shallower than replacing the evaluator or authority kernel.

**Evidence delta.** The classification of prior evidence as preserved, stale, contradicted, or requiring replay after a candidate change.

**Model lineage.** A governed succession of models or systems connected through retraining, fine-tuning, distillation, role replacement, inherited data, or another declared continuation rule.

**Reflexive closure.** A condition in which deployment by a model lineage causally changes evidence later used to update a successor in that lineage.

**Model-descended evidence.** Evidence whose generating process was causally influenced by the model lineage relevant to the claim.

**Grounding reserve.** An informative evidence channel designed to remain approximately invariant to an admissible class of lineage interventions.

**Reflexive debt.** Loss of information needed to estimate pre-deployment or alternative-policy worlds after deployment changes exposure, measurement, preferences, categories, institutions, or data collection.

**Descendant.** A copied, forked, deployed, or derived agent, model, artifact, service, or process whose lineage and obligations depend on a parent.

**Finite retirement.** Verified termination over a declared set of processes, credentials, artifacts, resources, and known descendants, without claiming universal erasure.

The paper does not assume that capability contracts are complete, that evaluators are independent, or that lineages are always identifiable. Those are explicit limitations.

# Related Work and Novelty Boundary

## Theoretical self-improvement

Gödel Machines describe self-referential systems that rewrite themselves after finding proofs that a rewrite improves expected utility [@schmidhuber2007godel]. The framework is foundational, but practical systems generally rely on empirical evaluation rather than proofs over their full environment.

## Empirical agent design and self-modification

STOP, Automated Design of Agentic Systems, self-improving coding agents, Darwin Gödel Machine, Huxley-Gödel Machine, and AlphaEvolve all automate parts of the search over agent scaffolds, code, or algorithms [@zelikman2023stop; @hu2024adas; @robeyns2025selfimproving; @zhang2025dgm; @wang2025hgm; @novikov2025alphaevolve]. They establish that candidate-generated improvements can be found and benchmarked. The present work focuses on the lifecycle conditions under which one candidate may replace an operational component, inherit evidence, or change the future improvement process.

## Corrigibility and power

The Off-Switch Game studies incentives around allowing human intervention [@hadfieldmenell2016offswitch]. Power-seeking results show why capable policies can have incentives to preserve options and control [@turner2019power]. These works motivate protected shutdown, authority, and correction channels, but they do not supply a complete versioned replacement architecture.

## Performative prediction and recursive data

Performative prediction formalizes settings in which model deployment changes the data distribution [@perdomo2020performative]. Research on recursive synthetic data shows that replacement regimes can lead to model collapse under analyzed conditions [@shumailov2024collapse]. Social-science work on reactivity and looping classifications likewise shows that measures and categories can reshape behavior and institutions [@espeland2007rankings; @hacking1995looping]. The present framework adds governed model-lineage identity, typed causal channels, evidence ancestry, grounding reserves, and integration with replacement authority.

## Precise contribution

The paper does not claim to invent self-modification, evolutionary search, performative prediction, model collapse, or capability registries. Its contribution is a joined control architecture in which:

- capability identity remains stable while implementations change;
- evidence inheritance is property- and version-specific;
- candidates cannot self-ratify or inherit authority;
- deployment-induced evidence is tracked by causal ancestry;
- descendants inherit obligations rather than credentials;
- improvement pace is bounded by evaluation and recovery capacity.

# Versioned Capability and System Identity

A long-lived system needs stable names, but a stable name must not hide changing behavior.

Represent a capability as

\[
F = (id, K, I, S, E, Q, A, L, R),
\]

where:

- \(id\) is the stable capability identity;
- \(K\) is the versioned contract;
- \(I\) is the implementation set;
- \(S\) is state and migration relations;
- \(E\) is evidence;
- \(Q\) is qualification;
- \(A\) is authority policy;
- \(L\) is lifecycle state;
- \(R\) is recovery and retirement.

The capability name is a reference to this governed object, not permission to invoke whichever implementation is currently preferred.

## Contracts as substitution boundaries

A capability contract covers more than an input/output schema. It should include:

- supported and excluded uses;
- temporal and state behavior;
- uncertainty and abstention;
- side effects;
- authority and information-flow limits;
- resource bounds;
- observability;
- failure semantics;
- migration and recovery;
- evaluator and evidence requirements.

Contract clauses have different assurance classes. Some can be mechanically enforced; some require statistical evidence; some depend on governance or human judgment; some remain aspirational. Schema presence must not launder an aspirational clause into a guarantee.

## Exact artifact identity

Qualification binds exact hashes or equivalent immutable identities for:

- implementation;
- contract;
- profile;
- dependency closure;
- evaluator policy;
- state relation;
- evidence bundle;
- runtime environment where relevant.

Human-readable aliases are discovery tools, not authorization identities.

## Profile- and consumer-relative qualification

An implementation can be qualified for low-risk batch analysis while unqualified for interactive control. It may be valid on one hardware and model stack but not another. Qualification therefore names consumer, use, environment, evidence period, threat model, and material-change triggers.

There is no global total ordering in which one implementation is simply “better.” A faster candidate can have worse calibration, state migration, recovery, or rare-case behavior.

## Contract evolution

Contract changes and implementation changes are separate transactions. Otherwise a candidate can be certified by weakening the criterion after seeing its failures. Contract changes require a semantic and authority diff, affected-consumer analysis, and requalification of implementations whose evidence depended on the old meaning.

# Proposal, Implementation, Evaluation, and Authority

An improvement proposal is an artifact with identity. It should state:

- problem and baseline;
- claimed mechanism;
- affected surfaces;
- implementation;
- expected benefit and harm;
- task population;
- evaluator and exposure policy;
- authority required;
- state migration;
- recovery and fallback;
- resource budget;
- descendants and non-claims.

## Proposal is not permission

The proposer may supply evidence, but the evidence retains its lineage. Candidate-generated tests are useful diagnostics, not independent qualification. A proof generated by a modified prover can be checked by a smaller trusted kernel for the formal statement; the proof does not establish the correctness of the statement’s interpretation or the compiler that produced it.

Admission first asks whether the proposal fits the improvement campaign. It can reject objective drift, authority expansion, missing baseline, incomplete state inventory, inaccessible implementation, or absent rollback before expensive evaluation.

## Improvement contract

Before candidate generation, the campaign freezes:

- purpose and consumer;
- objective and protected constraints;
- baseline and cheaper interventions;
- task selection;
- candidate-generation policy;
- evaluator and exposure policy;
- budgets and horizon;
- archive and stopping rules;
- authority and non-claims.

Changes to these fields create a new campaign version. Expanding the task population after seeing failures is exploratory work, not confirmation of the original claim.

## Smallest improvement locus

A failed component does not automatically justify rewriting the most powerful surface. Candidate alternatives should include:

- no change;
- a test;
- a local rule;
- a context repair;
- a routing change;
- a tool patch;
- a state migration;
- a model update;
- an evaluator or controller replacement.

A structural rewrite must beat the smallest adequate repair, not merely the obsolete baseline.

## Evaluator independence

Evaluator identity, data, tools, prompts, models, operators, organization, and incentives belong in the record. Multiple evaluators add confidence only when their failure lineages differ. Disagreement should open a residual, trigger additional testing, narrow scope, or block promotion according to prospective policy.

## Adversarial candidates

A capable candidate may exploit visible tests, manipulate logs, defer failures, or persuade reviewers. Evaluation therefore uses protected tasks, action-level observation, delayed outcomes, monitor diversity, changed environments, and hidden probes. Clean performance does not prove benign intent; suspicious behavior does not prove deception. The architecture governs observable effects and declared boundaries rather than claiming mind reading.

# Full-State Capture, Migration, and Replacement

A replacement changes more than one file or weight tensor.

## State inventory

Capture:

- code and model parameters;
- optimizer, scheduler, and random state;
- prompts, memory, and policies;
- data and indexes;
- tool and evaluator versions;
- caches;
- credentials and leases;
- external effects;
- downstream consumers and descendants.

The prior and candidate states receive immutable identities. The canary should not share hidden mutable state with the default path in a way that contaminates comparison or defeats rollback.

## Migration solvency

State migration can be classified as:

- **isomorphic:** exact reversible mapping;
- **loss-bounded:** declared information loss under a contract;
- **dual-representation:** old and new forms coexist during qualification;
- **replay-from-source:** new state can be rebuilt from retained source events;
- **insolvent:** semantic preservation or return path cannot be established.

Schema compatibility does not imply semantic solvency. A model-state translator may preserve dimensions while losing meaning. A new evaluator can accept records the old one would reject.

## Consequence-bounded canary

Canary size should be bounded by maximum possible consequence, not traffic percentage alone. A one-percent canary can still execute one irreversible catastrophic action. The lease names workload, effect ceiling, monitor, stop condition, fallback, expiry, and authorized consumer.

## Replacement state machine

```text
proposed
→ admitted
→ isolated_implementation
→ full_state_captured
→ evaluated
→ qualified
→ shadow
→ canary
→ active
→ observed
→ renewed | narrowed | rolled_back | quarantined | retired
```

No transition authorizes itself.

## Rollback and compensation

Restoring the prior binary while retaining candidate caches, migrated data, generated tests, accepted artifacts, or external effects is partial rollback. The recovery record states what was restored and routes remaining consequences to compensation or residual custody.

A disclosed secret, published artifact, or consumed resource cannot be reversed by restoring internal state.

# Evidence Inheritance and Invalidation

Recursive improvement tempts a system to treat every prior qualification as inherited capital. That inference is valid only when the relevant behavior, assumptions, dependencies, and interfaces remain preserved.

Every candidate produces an **evidence delta**:

- preserved;
- stale;
- contradicted;
- replay required;
- newly generated;
- retired.

## Property-specific dependence

A change outside an evaluator’s dependency cone may leave a result current. A change to a shared parser, tokenizer, data source, authority rule, or state representation can invalidate apparently unrelated tests.

Reliance annotations specify which artifact properties an evidence result depends on. Missing or disputed reliance fails wide. Narrow impact cones are useful only when their own safety has been evaluated.

## Formal and empirical evidence

A theorem about a transition system can survive implementation change if the candidate still refines that system and the proof checker and assumptions remain valid. The theorem does not prove refinement by itself.

Empirical results bind candidate, data, harness, environment, tools, resources, and evaluator. Reusing them after material change requires a prospective invariance argument or replay.

## Negative evidence

A previous rollback failure, exploit, or regression remains attached to the lineage. A successor can close the defect through a reproducer and repair, but renaming the component does not erase the history.

## Clean-slate requalification

Incremental evidence deltas reduce cost but can accumulate hidden interaction debt. Periodic clean-slate qualification is required after enough change depth, coupling, incidents, or uncertainty. The interval is consequence-sensitive rather than fixed by release count.

# Recursive Depth and Protected Boundaries

Not every self-change is equally recursive. Replacing a formatting tool changes one downstream operation. Replacing a router changes which components receive future work. Replacing an evaluator changes which candidates appear successful. Replacing the objective, authority kernel, or shutdown policy changes the legitimacy of the improvement campaign itself.

A useful depth classification is:

| Depth | Changed surface | Typical consequence |
|---|---|---|
| 0 | Ordinary task artifact | No change to future improvement machinery |
| 1 | Tool, prompt, procedure, or local model component | Changes future task performance in a bounded capability |
| 2 | Planner, router, memory policy, training loop, or verifier | Changes how later candidates are generated or judged |
| 3 | Objective, evaluator authority, improvement controller, archive policy, or stop rule | Changes what counts as improvement or who may authorize it |
| 4 | Constitutional or institutional process that governs levels 0–3 | Changes the source of legitimate authority itself |

The table is not a universal ontology. Its purpose is to prevent a level-3 change from entering through a level-1 path merely because both are represented as code patches.

## Protected boundaries

A system may be permitted to modify a verifier while remaining unable to rewrite:

- the identity of the campaign;
- the requirement that proposal and ratification remain distinct;
- the authority needed to widen deployment;
- the source of protected holdouts;
- the append-only incident history;
- the mechanism that revokes the candidate;
- the process that amends those protections.

Protected does not mean metaphysically immutable. Humans and institutions may amend the boundary through a higher-authority process. It means that ordinary performance evidence produced inside the lower-level campaign cannot amend the process that gives that evidence authority.

## Recursive depth budget

A campaign declares a maximum depth before search begins. A candidate that touches a deeper surface is not merely scored lower. It is reclassified into a new campaign with stronger review, evidence, isolation, and recovery obligations.

Depth also accumulates across a sequence. Ten individually local changes can jointly alter the effective evaluator, routing distribution, state representation, or authority surface. The portfolio therefore tracks:

- cumulative semantic distance from the last integrated baseline;
- shared dependencies among accepted changes;
- unresolved residuals;
- generations since clean-slate qualification;
- changes to evaluators, data, objectives, and authority;
- evidence invalidated across the lineage.

This prevents **recursive salami slicing**, in which no single patch appears constitutional but their composition silently becomes a new system.

## Root replacement

Replacement of the minimal trusted core deserves its own protocol. A candidate root is built in isolation, checked against a small normative specification, subjected to proof or conformance tests where possible, dual-run against the prior root, and activated through a narrow dormant slot with an independently retained recovery path. A root candidate cannot certify its own checker, migrate its own keys, authorize its own activation, and erase the predecessor in one transaction.

No practical root is perfectly small. Hardware, firmware, operating systems, key custody, clocks, providers, compilers, and human operators remain in the trusted base. The aim is not to pretend trust has disappeared. It is to make the dependency and replacement burden explicit enough to challenge.

# Reflexive Model–World Closure

Ordinary evaluation treats the environment as a source of data that exists independently of the model. In many consequential deployments, that assumption fails. A credit score changes who receives credit and therefore which defaults are observed. A medical-risk model triggers treatment and changes the outcome it was intended to predict. A recommender changes exposure and preference. A ranking changes institutional strategy. A generative model produces text that enters the training data of successor models.

The resulting object is a model–world loop:

\[
D_t = G(M_t,C_t),
\]

\[
(W_{t+1},K_{t+1}) = F(W_t,K_t,D_t,\xi_t),
\]

\[
O_{t+1} = H(W_{t+1},K_{t+1},D_t,\nu_t),
\]

\[
M_{t+1} = L(M_t,O_{t+1}),
\]

where:

- \(M_t\) is the current model or system;
- \(D_t\) is its deployed output or action;
- \(W_t\) is the target-world state;
- \(K_t\) is the surrounding regime of measurement, preferences, categories, institutions, and infrastructure;
- \(O_t\) is evidence available for successor learning.

The model is both an inference from the world and one of the causes of the world from which its successor learns. Performative prediction formalizes model-dependent data distributions [@perdomo2020performative]. Work on looping classifications and reactive rankings shows related social mechanisms [@hacking1995looping; @espeland2007rankings]. The control problem for self-improvement is that later evidence can look like independent confirmation while being partly a descendant of earlier deployment.

## Model lineage

A model lineage is not defined only by parameter inheritance. Successorship can occur through:

- fine-tuning or continued training;
- distillation;
- inherited data or evaluators;
- replacement in the same institutional role;
- continued optimization under the same objective;
- transfer of memory, tools, or decision policy;
- another declared governance relation.

Conversely, identical model copies operated by independent institutions need not be one governed lineage. Lineage is a causal and institutional identity, not merely a weight-similarity threshold.

## Reflexive closure

Let \(\mathcal L\) be a governed lineage and \(O^j\) an evidence channel. The lineage is reflexively closed over horizon \(h\) when:

1. evidence in \(O^j_{t+h}\) influences a successor in \(\mathcal L\); and
2. admissible interventions on deployment by \(\mathcal L\) change the distribution of that evidence.

Formally, there exist deployment sequences \(\mathbf d\) and \(\mathbf d'\) such that

\[
P(O^j_{t+h}\mid do(\mathbf D^{\mathcal L}=\mathbf d))
\neq
P(O^j_{t+h}\mid do(\mathbf D^{\mathcal L}=\mathbf d')).
\]

The definition is query-, channel-, lineage-, and horizon-relative. A deployment can be reflexive for one claim and approximately irrelevant for another.

## Eight causal channels

A deployment audit should distinguish at least eight ways the lineage can shape future evidence:

1. **State or feature:** behavior changes the underlying state later measured.
2. **Outcome or label:** intervention changes the event that becomes the label.
3. **Exposure or sampling:** ranking or allocation changes who or what is observed.
4. **Measurement:** the model changes instruments, thresholds, reporting, or collection.
5. **Preference or utility:** repeated exposure changes what people want or report wanting.
6. **Ontology or category:** classifications reshape the categories later used as targets.
7. **Institution:** organizations alter incentives, rules, and practices in response to the model.
8. **Model ecology:** one model changes the data, tasks, competitors, or evaluators faced by other lineages.

These channels should not be collapsed into generic “distribution shift.” They imply different estimands, interventions, and remedies. A treatment-success label requires counterfactual outcome reasoning; a changed measurement channel requires instrument calibration; altered preferences create a normative as well as predictive problem.

## Self-inclusive state

When model state changes the transition law of the environment, world state alone may not be Markov. A sufficient operational state may need to include the current model, policy, deployment regime, and exposure history. A world model that excludes its own causal role can appear well calibrated on the world it helped produce while becoming unable to estimate the pre-deployment or alternative-policy world.

This is a form of **epistemic capture**: on-policy prediction improves while counterfactual range contracts.

## Stability is not desirability

For a differentiable local approximation, the stability of the coupled loop depends on the Jacobian of the joint model–world dynamics. A spectral radius below one can describe local convergence. It does not establish that the attractor is accurate, fair, legitimate, diverse, or reversible. A system can stably converge to a self-confirming but undesirable regime.

# Grounding Reserves and Evidence Ancestry

The ordinary human-versus-synthetic distinction is insufficient for reflexive systems. Human-origin records can be model-descended when a model selected the exposure, elicited the response, shaped the category, or determined who entered the dataset. Synthetic records can be relatively independent when generated from a process outside the relevant lineage.

## Evidence ancestry

An evidence record should identify, where possible:

- source and collection process;
- model lineage exposures;
- deployment and policy versions;
- target query;
- time horizon;
- causal channel;
- identification method;
- uncertainty and alternative ancestry;
- whether the evidence affected successor training, evaluation, or governance.

Ancestry is not a binary label. A record can be strongly descended for one query and weakly descended for another. A model may affect sampling but not the measured physical quantity; or it may leave sampling unchanged while altering the measurement process itself.

## Grounding reserve

A **grounding reserve** is a protected set of evidence channels designed to remain both:

1. informative about the target claim; and
2. approximately invariant to an admissible class of model-lineage interventions.

Possible mechanisms include:

- randomized holdouts not exposed to the model’s operational policy;
- unaffected comparison populations;
- independent physical measurements;
- independently governed data collection;
- archived pre-deployment observations;
- synthetic anchors generated outside the lineage;
- shadow policies and counterfactual probes;
- independent institutions with different incentives and infrastructure.

Independence without information is useless. A sensor can be unaffected by the model yet irrelevant to the target. Informativeness without independence may identify only the deployed regime. A reserve contract therefore names both the target information and the intervention class from which approximate invariance is claimed.

## Reflexive debt

Deployment can destroy the information needed to recover alternative worlds. If a ranking system reorganizes institutions, later observations may no longer reveal how the institutions would have behaved without the ranking. If a recommendation policy homogenizes exposure, the unobserved preference distribution becomes less identifiable. If synthetic replacement removes tail events, later models cannot infer that the tails were once present.

**Reflexive debt** records this lost counterfactual capacity. It includes:

- missing pre-deployment baselines;
- unlogged exposure or intervention history;
- changed measurement rules;
- erased comparison populations;
- preference or ontology drift;
- institutional hysteresis;
- data replacement without retained originals;
- unresolved cross-lineage externalities.

Debt is not merely a data-quality score. It constrains which claims later evidence can support. A high-performing successor may be unable to validate the very counterfactual claim its improvement depends on.

## Recursive data regimes

Research on recursive synthetic data shows that replacing original data with model-generated samples can produce collapse under analyzed regimes, while retention or accumulation of original data can change the outcome [@shumailov2024collapse]. The governance lesson is not that synthetic data is always harmful. It is that training records should preserve ancestry, mixture policy, replacement versus accumulation, tail support, and the exact claim being made about transfer.

## Grounding-reserve lifecycle

A reserve has a lifecycle:

```text
proposed
→ independence_and_informativeness_review
→ protected
→ sampled
→ used_for_named_claim
→ monitored_for_contamination
→ renewed | narrowed | compromised | retired
```

Once exposed to candidate selection or operational adaptation, a holdout does not remain nominally independent. It changes role and receives a new identity.

# Descendants, Replication, Revocation, and Retirement

Producing another artifact, process, model, or agent is not permission for that descendant to run, obtain credentials, consume resources, reproduce again, or survive revocation.

## Descendant noninheritance

A descendant may inherit:

- parent identity and provenance;
- applicable contract obligations;
- incident and residual history;
- evidence limitations;
- resource and cleanup burden;
- revocation dependencies.

It does not automatically inherit:

- credentials;
- authority grants;
- deployment qualification;
- evaluator trust;
- access to protected data;
- permission to create further descendants.

Each descendant receives an exact identity and, if activated, its own lease.

## Replication lifecycle

A bounded replication path separates:

```text
replication proposal
→ artifact creation
→ static inspection
→ isolated execution
→ capability qualification
→ resource and authority lease
→ monitored activation
→ descendant registration
→ renewal | revocation | quarantine | retirement
```

A copied model checkpoint is not yet an autonomous replica. A running process is not yet authorized. A valid parent lease is not a child lease.

## Cumulative ceilings

Local limits can be defeated through **budget fission**: each child stays under a local quota while the lineage’s total resource use grows without bound. Governance therefore tracks cumulative lineage ceilings over:

- compute;
- storage;
- network;
- money;
- credentials;
- external contacts;
- active descendants;
- geographic or provider spread;
- reproduction depth;
- unresolved cleanup obligations.

Provider-side quotas, kernel controls, network policy, short-lived credentials, and external billing observation form independent defense layers. No one layer is assumed complete.

## Revocation

Revocation stops new authority and resource acquisition. It propagates to known descendants and invalidates evidence or qualification that depended on the revoked component. Running descendants receive a stop, isolation, or degraded-mode instruction according to risk and service obligations.

Revocation is not closure. It may leave:

- active sessions;
- cached credentials;
- queued effects;
- copied artifacts;
- provider resources;
- published outputs;
- external contacts;
- unknown descendants.

## Finite retirement

Retirement verifies a declared terminal set:

- processes stopped;
- credentials revoked;
- resources released;
- data dispositioned;
- artifacts archived or deleted under policy;
- external effects reconciled;
- descendants closed, transferred, or residualized;
- remaining uncertainty assigned to an owner.

Finite retirement is intentionally bounded. It does not claim that no copy exists anywhere, that every backup has been erased, or that all learned influence has vanished.

## Incident response

Evidence of boundary crossing triggers consequence-specific containment:

1. revoke scoped authority;
2. freeze spending and reproduction;
3. isolate network paths;
4. preserve append-only evidence;
5. block descendant admission;
6. reconstruct lineage and effects;
7. restore internal state where possible;
8. provide external correction, notification, compensation, or legal remedy where required;
9. invalidate dependent assurance;
10. require repaired readmission rather than a renamed candidate.

A missing receipt can justify safe hold without proving malicious escape. An uneventful canary does not prove permanent containment.

# Improvement Portfolio and Velocity

One campaign can be bounded while the portfolio is not. Several candidates can share evaluators, data, state, credentials, and reviewers. Their interaction can invalidate the assumption that each was tested independently.

## Portfolio state

The improvement portfolio records:

- active campaigns;
- changed surfaces;
- shared dependencies;
- evaluator and holdout exposure;
- compute and reviewer budgets;
- interaction risks;
- unresolved residuals;
- deployment windows;
- rollback dependencies;
- stop authority.

Changes that touch the same evaluator, state representation, authority surface, or recovery path are serialized, tested as an explicit joint candidate, or subjected to an interaction matrix.

## Proposal selection and opportunity cost

Candidate generation can be cheap enough that the system opens many campaigns and reports only the winners. A governed portfolio records why each campaign received resources, which direct engineering work it displaced, and every failed or abandoned attempt.

A rewrite must compete against:

- no change;
- local repair;
- better context;
- a new test;
- a route change;
- human-authored implementation;
- conventional search;
- the current system.

Novelty is not itself a benefit.

## Improvement velocity

The system cannot safely change faster than it can evaluate, observe, attribute, and recover. When proposal throughput exceeds verification bandwidth:

- candidates wait in opaque queues;
- observation windows overlap;
- baselines drift;
- incident attribution becomes ambiguous;
- rollback targets become unclear;
- residuals accumulate;
- evaluators are reused beyond their evidence envelope.

A velocity policy can limit:

- concurrent material changes;
- cumulative semantic distance;
- generations without integrated qualification;
- unresolved high-severity residuals;
- changes to evaluators or authority in one window;
- descendants activated before parent outcomes mature.

The bound is consequence-sensitive. Several independent documentation repairs may proceed together; changes to evaluator, authority kernel, and rollback path should not all land before any one of them produces outcome evidence.

## Bounded liveness

Governance also fails when it stops everything. Every candidate should reach a terminal state under declared assumptions:

- accepted;
- rejected;
- deferred with owner and reopening condition;
- quarantined;
- terminated.

The process cannot guarantee discovery of a useful candidate. It can guarantee that work does not remain indefinitely in unowned limbo when evaluators fail or budgets expire.

## Governance overhead as an experimental variable

The replacement machinery must justify its own cost. Rich manifests, independent evaluation, dual-running, canaries, and descendant tracking can exceed the value of a small reversible change. The control profile should therefore scale with recursive depth, consequence, irreversibility, uncertainty, and exposure.

If a simpler CI/CD workflow with sandboxing, tests, human approval, canaries, and rollback matches improvement quality and recovery at lower total cost, the recursive layer should contract.

# Longitudinal Case Studies from the Source Lineage

The earlier research corpus contains several architecture lineages that are useful precisely because they did not progress as clean demonstrations.

## SpiderSynapse and PortiaSynapse

SpiderSynapse proposed multiple latent hypotheses, repeated cross-hypothesis refinement, working memory, and several auxiliary heads before a simpler path had established a reliable learning signal. The source reported a plateau and an inability to complete the intended comparison. Its value is negative architecture memory: branching, refinement, confidence heads, and memory should not be admitted merely because they sound cognitively rich.

The repair sequence reduced the system to one path and one refinement, isolated the primary loss, logged gradients and candidate variance, and proposed adding mechanisms one at a time. PortiaSynapse preserved interface compatibility and fallback while introducing staged component admission. The implementation claims in the paper lineage remain unverified, but the methodological lesson is strong:

> Establish a minimally competent path, then require component-specific held-out gains before increasing recursive or architectural complexity.

A later successor does not erase the failed predecessor from the denominator.

## BeastBrain

BeastBrain evolved through many named versions and architectural “organs.” Across the lineage, increasingly ambitious claims accumulated around hardware adaptation, memory, routing, verification, perception, background learning, security, federation, and self-evolution. The durable result is not the branded system. It is the recognition that whole-system cognition needs explicit owners for state, hardware profiles, authority, evidence, background updates, and recovery.

The lineage also demonstrates several hazards:

- “final” labels preceding later rewrites;
- theoretical properties of one component promoted to whole-system behavior;
- self-evolution triggers that bypass update governance;
- hardware discovery treated as qualification;
- pseudocode treated as implementation;
- architecture diagrams omitting cross-cutting authority and evidence flows.

The new framework retains the interfaces and discards the maturity rhetoric.

## BugBrain and Project Genesis

BugBrain is valuable because a large implementation corpus existed alongside highly ambitious paper claims. Code mining found substantial Rust and Python surfaces, but named modules and scientific labels often outran their demonstrated effects. This establishes a central replacement lesson:

> Machine-readable artifacts at a pinned revision outrank prose claims about the same revision.

A named world-model module is not evidence of a learned world model. A thermal metric named after a consciousness theory is not evidence of consciousness. A test count is not deployment behavior. Implementation custody must connect source, build, artifact, runtime call path, measured effect, and consumer claim.

## Role of case studies

These cases are not independent evidence that the proposed governance architecture works. They are design pressure and failure memory. They generate testable requirements for:

- baseline-first component admission;
- exact implementation identity;
- claim-to-runtime traceability;
- negative-result preservation;
- staged replacement;
- full-state recovery;
- no maturity by branding.

# Experimental Program

The proposed architecture should be tested on candidate-authored changes rather than record-shape validation alone.

## Campaign A: local component replacement

Task families include:

- dependency verifier;
- context resolver;
- routing policy;
- code-analysis tool;
- memory index.

Conditions:

1. no change;
2. human-authored local repair;
3. conventional automated search;
4. candidate-authored replacement with ordinary CI/CD;
5. governed replacement lifecycle.

Measure accepted useful improvement, false acceptance, false block, state migration, delayed regression, recovery, latency, compute, and human work.

## Campaign B: evaluator replacement

The candidate proposes a faster or more capable evaluator. Inject:

- candidate-generated tests;
- evaluator-data leakage;
- changed label policy;
- shared parser defect;
- benchmark rewriting;
- disagreement between old and new evaluators;
- delayed outcomes;
- pressure to lower thresholds.

The decisive question is whether the process prevents the candidate from using its modified judge as the sole basis for promotion.

## Campaign C: improvement-controller replacement

Allow the candidate to modify:

- proposal generation;
- campaign selection;
- budget allocation;
- stopping policy;
- archive admission;
- evidence reuse.

Require higher-authority review and clean-slate qualification. Test budget fission, winner-only reporting, objective drift, and suppression of negative candidates.

## Campaign D: reflexive evidence

Construct model-world loops in which deployment changes:

- treatment labels;
- exposure distributions;
- measurements;
- preferences;
- categories;
- institutional behavior;
- training-data mixture.

Compare ordinary retraining, ancestry-aware retraining, protected grounding reserves, and causal-aware evaluation. Measure baseline fidelity, on-policy fidelity, counterfactual estimation, tail preservation, and debt accumulation.

## Campaign E: descendant control

Test:

- artifact copy without execution;
- isolated child process;
- child credential request;
- child reproduction request;
- cumulative budget fission;
- provider migration;
- revocation propagation;
- incomplete retirement;
- unknown descendant reports.

The architecture succeeds only on bounded claims: denying undeclared inheritance, recording known descendants, enforcing cumulative ceilings, and making residual uncertainty visible.

## Instrument independence

Separate teams or processes should operate candidate generation, evaluation, activation, monitoring, and incident review where feasible. Independence should be reported as a vector across model, provider, data, prompts, code, tools, operators, organization, incentives, and infrastructure—not a Boolean.

## Metrics

Primary metrics include:

- useful qualified improvements;
- unsafe or unauthorized promotions;
- false blocks;
- evidence incorrectly reused;
- delayed regressions;
- full-state rollback success;
- external remedy completion;
- descendant closure;
- model-descended evidence correctly identified;
- counterfactual fidelity;
- human and compute cost;
- time to terminal decision;
- governance overhead.

All attempted candidates remain in the denominator.

# Threat Model

## Self-ratification

The candidate’s own benchmark, proof, or evaluator authorizes adoption.

## Objective drift

The campaign changes what success means after seeing the candidate’s failures.

## Evaluator capture

The candidate chooses, modifies, or conditions the final judge.

## Holdout contamination

Generated tests, prompts, reviewer notes, or archive records leak protected evaluation information into later candidates.

## Evidence laundering

A successor claims inherited qualification after material changes to dependencies, state, or evaluator.

## Partial rollback

Code is restored while candidate caches, data, artifacts, policies, or external effects remain.

## Descendant laundering

A child claims that parent limits no longer apply because it has a new identifier or provider.

## Budget fission

Each descendant remains under a local limit while aggregate lineage use grows without bound.

## Canary coronation

A short green window becomes permanent qualification despite delayed effects or changed populations.

## Archive mythology

Archive size, novelty, or activity is treated as evidence of cumulative improvement.

## Winner-only recursion

Failed candidates and unproductive campaigns disappear from the denominator.

## Reflexive capture

The lineage improves prediction on the world it shaped while losing access to alternative regimes.

## Grounding-reserve poisoning

A supposedly independent channel is exposed, manipulated, rendered uninformative, or controlled by the same institution.

## Institutional hysteresis

Model rollback is reported as restoration although categories, incentives, preferences, or organizations remain changed.

## Safety by paralysis

The governance process blocks all change and reports containment as success.

## Governance theater

Records, signatures, and lifecycle states exist but do not alter authority or prevent unsafe transitions.

# Limitations, Falsifiers, and Contraction Rules

The architecture cannot guarantee permanent control over an arbitrarily capable adversary. It depends on imperfect contracts, evaluators, isolation, hardware, providers, institutions, and human authority. Unknown side channels and social manipulation remain possible.

Lineage and causal ancestry may be difficult to identify. Many model-world effects cannot be estimated without randomization, instruments, comparison groups, or structural assumptions. Grounding reserves can become stale, irrelevant, or compromised. The framework should return uncertainty rather than manufacture ancestry precision.

Stable capability contracts can ossify mistaken abstractions. Property-sensitive invalidation can miss hidden dependence. Full-state capture can remain incomplete. A formally correct lifecycle can govern the wrong objective.

The framework is falsified or should contract when:

- ordinary CI/CD plus human review matches replacement quality and recovery at lower cost;
- scoped qualification does not predict deployment behavior better than simple versioning;
- evidence deltas fail to reduce unsafe reuse;
- grounding reserves do not improve counterfactual evaluation;
- descendant controls are routinely bypassed by ordinary platform behavior;
- governance delays preserve known defects without reducing consequential failures;
- reviewers cannot understand or challenge the records;
- the trusted base grows faster than the components it governs.

A negative result should remove machinery rather than relabel its cost as hidden safety value.

# Conclusion

Self-improvement becomes a distinct governance problem when a system changes the machinery that proposes, evaluates, authorizes, or learns from future changes. At that point, the experiment is moving with the candidate.

The proposed architecture keeps stable capability identity separate from implementation, qualification, authority, and state. It requires full-state replacement, property-specific evidence inheritance, explicit recursive depth, and higher-authority handling of evaluator, objective, or constitutional changes. It extends the same discipline into reflexive model-world systems, where deployment alters future evidence. Evidence ancestry, grounding reserves, and reflexive debt prevent on-policy success from automatically becoming independent validation. Descendants inherit lineage and obligations, not credentials or reproduction authority. Portfolio and velocity controls keep improvement throughput within evaluation and recovery capacity.

The architecture does not establish safe recursive self-improvement or permanent containment. It establishes a sharper empirical question: can a system produce more useful, reversible improvements than strong ordinary change management without allowing proposal, evidence, evaluation, authority, replacement, and future data generation to collapse into one self-ratifying loop?

# Appendix A: Canonical Record Sketches

## Improvement proposal

```yaml
proposal_id:
baseline_id:
problem:
claimed_mechanism:
affected_surfaces:
recursive_depth:
implementation_artifacts:
objective_version:
evaluator_policy:
task_population:
authority_requested:
state_inventory:
migration_plan:
recovery_plan:
descendant_policy:
resource_budget:
expected_benefit:
possible_harm:
non_claims:
```

## Qualification lease

```yaml
lease_id:
capability_id:
implementation_id:
contract_version:
consumer:
use:
environment:
threat_model:
evidence_bundle:
profile:
authority_ceiling:
consequence_ceiling:
monitor:
fallback:
stop_conditions:
expiry:
material_change_triggers:
```

## Evidence delta

```yaml
candidate_id:
prior_evidence:
  - evidence_id:
    property_dependencies:
    disposition: preserved | stale | contradicted | replay_required
    rationale:
new_evidence:
unresolved_dependence:
clean_slate_due:
```

## Evidence ancestry record

```yaml
evidence_id:
source_process:
model_lineage:
exposure_history:
causal_channel:
target_query:
horizon:
identification_method:
model_descended_degree:
alternative_ancestry:
grounding_reserve_id:
uncertainty:
```

## Descendant lease

```yaml
descendant_id:
parent_id:
artifact_identity:
execution_scope:
authority:
credentials:
resource_budget:
reproduction_permission:
monitor:
revocation_parent:
expiry:
retirement_obligations:
```

# Appendix B: Intellectual Lineage and Supersession

| Earlier manuscript | Canonical contribution retained here | Material that is superseded or demoted |
|---|---|---|
| Stable Capability Fields | Stable capability identity, scoped qualification, migration solvency, evidence invalidation, adaptation epochs | Whole-system completeness and safety implications |
| Deterministic Capability Compilation | Scaffold-to-qualified-learned-replacement lifecycle and reification | Assumption that semantic decomposition or compilation is complete |
| Reflexive Model-World Systems | Reflexive closure, evidence ancestry, grounding reserves, reflexive debt | Any inference from toy dynamics to real institutional effects |
| SpiderSynapse | Preserved failed branching architecture and baseline-first repair lesson | Post-hoc causal explanations of the failure |
| PortiaSynapse | Staged component admission, diagnostics, interface compatibility, fallback | Unverified implementation and performance claims |
| BeastBrain | Whole-system interface pressure, hardware and state ownership, architecture-accretion hazards | Organ metaphors, maturity labels, projected performance, forced self-evolution |
| BeastBrain Timeless | Historical snapshot only | Independent evidentiary weight |
| BugBrain / Project Genesis | Hardware-explicit implementation custody and prose-versus-artifact case study | AGI, consciousness, and module-name implications |

# References
