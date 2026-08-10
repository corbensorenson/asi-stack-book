Benchmaxxing: The Performance Ratchet
A Framework for Iterative Benchmark Saturation, Capability Diagnosis, and Model Evolution
White Paper
 Public Release v1.0 — May 2026
 Author: Corben Sorenson
Status: Conceptual Framework + AI Development Methodology
________________


TL;DR / Executive Abstract
AI progress often follows a recognizable pattern:
1. Build an initial model or architecture.
2. Evaluate it against a benchmark suite.
3. Train, tune, and improve data until performance saturates.
4. When the benchmark no longer distinguishes progress, find or build harder benchmarks.
5. If better data and training no longer break through the new benchmark wall, change the model or architecture.
6. Repeat.
This paper names that process Benchmaxxing: The Performance Ratchet.
The central thesis is:
A model should grow by repeatedly saturating its current benchmarks, confronting harder unsaturated benchmarks, diagnosing whether the wall is data-limited, training-limited, inference-limited, or architecture-limited, and changing architecture only when simpler interventions can no longer move the frontier.
Benchmaxxing is not benchmark gaming. It is not blindly optimizing a static leaderboard. It is a disciplined development loop in which benchmarks serve as moving capability frontiers. Once a benchmark is saturated, it is no longer the frontier. It becomes a regression test. The system must seek harder, more diagnostic evaluations.
The performance ratchet has two opposing forces:
Force
	Purpose
	Stability
	Preserve previously demonstrated capabilities.
	Pressure
	Expose unsolved capabilities through harder benchmarks.
	The ratchet advances when the model clears one frontier and locks that capability into the regression suite, while a new benchmark frontier applies pressure to the next missing capability.
The core loop is:
initialize model
   ↓
evaluate on benchmark suite
   ↓
train / tune / improve data
   ↓
saturate current benchmark or hit wall
   ↓
diagnose wall
   ↓
if data/training/inference fixes help: continue improving
   ↓
if not: modify architecture
   ↓
find harder unsaturated benchmarks
   ↓
repeat
In modern AI, this framework is especially relevant because widely used benchmarks often become saturated or contaminated as frontier models improve. Humanity’s Last Exam was introduced partly because models were exceeding 90% accuracy on popular benchmarks such as MMLU, reducing their usefulness for measuring frontier systems. OpenAI similarly stated in February 2026 that SWE-bench Verified no longer measured frontier coding capabilities well and recommended SWE-bench Pro instead, citing contamination and slowing progress on that benchmark.
Benchmaxxing turns this into a deliberate methodology:
When the benchmark stops applying pressure, promote it to regression status and find a sharper one.
A mature benchmark ratchet does not merely ask, “Did the model score higher?” It asks:
* What capability did this benchmark measure?
* Is the benchmark saturated?
* Is the model failing because of bad data, weak training, poor inference procedure, missing tools, or architectural insufficiency?
* Is the benchmark itself flawed, noisy, leaked, or too narrow?
* Does improvement transfer to harder, hidden, live, or out-of-distribution benchmarks?
* Should the next intervention be data, training, inference, tool use, architecture, or evaluation design?
Benchmaxxing proposes a disciplined answer:
Use benchmarks as temporary pressure surfaces, not permanent definitions of intelligence.
________________


Abstract
AI development is often described in terms of scaling laws, data quality, architecture design, post-training, inference-time reasoning, or benchmark leaderboards. This paper proposes a complementary framework: Benchmaxxing: The Performance Ratchet.
Benchmaxxing is the iterative process of advancing a model or architecture by repeatedly saturating a benchmark suite, diagnosing residual failure modes, expanding the benchmark frontier, and escalating interventions only when necessary. The model begins small and manageable. It is trained against a benchmark suite until the suite is saturated or until a wall appears. If performance improves with better data, the system remains data-limited. If performance improves with optimization or training changes, it remains training-limited. If performance improves with test-time compute, tools, or scaffolding, it is inference-limited. If none of these move the wall, the system is architecture-limited. Only then should architecture be changed.
The framework draws from existing observations in AI evaluation and model scaling. Empirical scaling laws show that model performance can improve predictably with model size, data, and compute. Chinchilla-style compute-optimal training showed that data allocation can be as important as parameter scale, demonstrating that some apparent model limitations are actually data/training-allocation limitations. Holistic evaluation frameworks such as HELM emphasize broad coverage, multi-metric evaluation, and explicit recognition of what benchmarks miss. Recent long-horizon evaluation work from METR suggests that task-completion time horizon is an important lens for understanding agent capability and that frontier agents’ time horizons have increased rapidly.
Benchmaxxing formalizes a practical development rhythm around these observations. Its purpose is not to maximize a single score, but to create a capability ratchet: each benchmark frontier pushes the model until it saturates; each saturated benchmark becomes a regression guard; each new unsaturated benchmark exposes the next capability gap.
The framework also includes anti-Goodhart safeguards. Goodhart’s law warns that when a measure becomes a target, it ceases to be a good measure. Benchmaxxing addresses this by rotating benchmark frontiers, separating public development benchmarks from private holdouts, tracking transfer, using benchmark mutation, measuring real-world task performance, and treating saturated benchmarks as historical capability checks rather than permanent optimization targets.
The result is an iterative, evidence-driven methodology for model growth:
Let the benchmark frontier decide whether the next improvement should come from data, training, inference, tools, or architecture.
________________


1. Introduction
1.1 The recurring development pattern
In practice, AI development rarely proceeds as a single clean leap from idea to optimal model. It is more often a ratchet.
A team starts with a model or architecture. They choose a benchmark suite. They train. They improve data. They tune hyperparameters. They adjust post-training. They add tools or inference scaffolding. They evaluate again. Eventually, one of two things happens.
First, the benchmark becomes saturated. The model reaches a ceiling. The benchmark no longer distinguishes meaningful progress.
Second, the model hits a wall. It cannot improve meaningfully on the benchmark despite additional training.
At that point, the team faces a question:
Is the problem the model, the data, the training process, the inference procedure, or the benchmark?
Benchmaxxing is the disciplined process of answering that question repeatedly.
________________


1.2 The central loop
The core Benchmaxxing loop is:
Model M₀
   ↓
Benchmark suite B₀
   ↓
Train / tune / improve data
   ↓
Evaluate
   ↓
Saturate or hit wall
   ↓
Diagnose wall
   ↓
If benchmark saturated: promote to regression suite
   ↓
Find harder benchmark B₁
   ↓
If wall persists across data/training/inference: change architecture
   ↓
Model M₁
   ↓
Repeat
This is a performance ratchet because progress locks in.
Once a model demonstrates a capability on a benchmark, that benchmark becomes part of the regression suite. The system should not lose that ability while advancing to harder evaluations.
The model’s capability frontier ratchets upward:
B0→B1→B2→⋯B_0 \rightarrow B_1 \rightarrow B_2 \rightarrow \cdotsB0​→B1​→B2​→⋯
and the model sequence follows:
M0→M1→M2→⋯M_0 \rightarrow M_1 \rightarrow M_2 \rightarrow \cdotsM0​→M1​→M2​→⋯
where each new model should preserve prior capabilities while improving on a harder benchmark frontier.
________________


1.3 Why this matters now
Benchmark saturation is becoming a central problem in frontier AI evaluation.
Benchmarks that once measured difficult capabilities can lose discriminative power as models improve. Humanity’s Last Exam was introduced as an expert-level academic benchmark partly because existing popular benchmarks were no longer hard enough for frontier models; the Nature paper states that LLMs had reached more than 90% accuracy on popular benchmarks such as MMLU.
Software engineering agents show the same pattern. SWE-bench Verified became a standard coding-agent benchmark, but OpenAI later argued it no longer measured frontier coding capability well, citing contamination and progress slowing from 74.9% to 80.9% over six months. The SWE-bench Verified site itself describes the benchmark as a human-validated subset of 500 tasks from SWE-bench, created to provide more reliable evaluation of coding agents.
This is not a failure of benchmarks. It is the natural lifecycle of benchmarks.
A good benchmark is supposed to become obsolete if the field progresses.
Benchmaxxing treats that lifecycle as the core engine of development.
________________


2. Definition
2.1 Benchmaxxing
Benchmaxxing is the disciplined process of maximizing model performance against a benchmark frontier until that frontier is saturated, then expanding the frontier with harder, more diagnostic benchmarks while preserving prior saturated capabilities as regression tests.
It is not simply “score chasing.”
It is:
benchmark-driven capability ratcheting.
A benchmark is used as pressure. Once it stops applying pressure, it is demoted from frontier to regression.
________________


2.2 The Performance Ratchet
The Performance Ratchet is the cumulative development process in which each saturated benchmark locks in a capability while new unsaturated benchmarks expose the next wall.
The ratchet has three required properties:
Property
	Meaning
	Lock-in
	Previously demonstrated capabilities must be preserved.
	Frontier pressure
	Current benchmarks must remain unsaturated and diagnostic.
	Escalation discipline
	Model complexity should increase only when simpler interventions fail.
	Without lock-in, the model forgets.
Without frontier pressure, the model stagnates.
Without escalation discipline, the model becomes unnecessarily complex.
________________


2.3 Saturation
A benchmark is saturated when it no longer provides useful gradient for development.
This may happen because:
* the model reaches near-ceiling performance;
* models cluster tightly near the top;
* remaining errors are mostly label noise or ambiguity;
* the benchmark is leaked or contaminated;
* the benchmark is too narrow;
* benchmark improvements no longer transfer to real-world performance;
* the metric has become Goodharted.
Saturation does not mean the benchmark is useless. It means its role changes.
A saturated benchmark becomes:
* a regression test;
* a historical capability marker;
* a sanity check;
* a compatibility test;
* a guardrail against capability loss.
It should no longer be treated as the main frontier.
________________


2.4 Wall
A wall occurs when performance on an unsaturated benchmark stops improving despite reasonable development effort.
A wall can be caused by different bottlenecks:
Wall type
	Meaning
	Data wall
	The model needs better, broader, cleaner, or more targeted data.
	Training wall
	The optimizer, curriculum, loss, schedule, or post-training process is insufficient.
	Inference wall
	The model has latent capability but needs better test-time compute, tools, memory, or scaffolding.
	Evaluation wall
	The benchmark is flawed, noisy, underspecified, contaminated, or misaligned with the target capability.
	Architecture wall
	The model class lacks a needed capability even after data, training, and inference improvements.
	Benchmaxxing requires diagnosing the wall before changing architecture.
________________


3. The Core Method
3.1 The ratchet loop
The Benchmaxxing loop has eight stages.
________________


Stage 1 — Initialize a manageable model
Begin with the smallest model or architecture that can plausibly learn the target capability.
This is important. The process should not start by assuming maximum scale is necessary.
A small model is easier to:
* train;
* interpret;
* debug;
* ablate;
* evaluate;
* compare;
* modify.
The goal is to create a development substrate whose failures are still legible.
________________


Stage 2 — Define an initial benchmark frontier
The benchmark suite should include tasks that are:
* relevant to the desired capability;
* difficult enough to reveal failures;
* measurable enough to track progress;
* diverse enough to prevent narrow overfitting;
* cheap enough for frequent iteration;
* representative enough to guide development.
The benchmark suite should not be a single score.
A good initial suite includes:
Benchmark type
	Purpose
	Unit benchmarks
	Test small, isolated skills.
	Diagnostic benchmarks
	Reveal specific failure modes.
	Capability benchmarks
	Measure the target ability directly.
	Integration benchmarks
	Test multi-step or system-level performance.
	Stress benchmarks
	Push out-of-distribution or adversarial conditions.
	Efficiency benchmarks
	Measure cost, latency, memory, and throughput.
	Safety benchmarks
	Check unacceptable behavior or risk.
	HELM’s evaluation philosophy is relevant here because it emphasizes broad coverage, multi-metric measurement, and explicit recognition of evaluation incompleteness rather than relying on one narrow score.
________________


Stage 3 — Train and improve data
The first response to poor performance should usually not be architectural reinvention.
Start with:
* better data;
* cleaner labels;
* curriculum;
* targeted examples;
* synthetic data;
* filtering;
* balancing;
* augmentation;
* better task formatting;
* post-training examples;
* preference data;
* tool demonstrations.
This is because many apparent model failures are actually data failures.
The Chinchilla result is a major historical reminder: DeepMind found that many large language models were undertrained relative to their parameter count and that compute-optimal training required scaling model size and training tokens together.
In Benchmaxxing terms:
Do not declare an architecture wall until you have tested whether the wall is actually a data or training allocation wall.
________________


Stage 4 — Evaluate and measure residuals
Evaluation should not only report a score.
It should report residuals:
* which items failed;
* which categories failed;
* which reasoning steps failed;
* which tasks were brittle;
* which examples were ambiguous;
* which failures were due to missing knowledge;
* which failures were due to poor instruction following;
* which failures were due to long-horizon breakdown;
* which failures were due to tool use;
* which failures were due to evaluation flaw.
The residual report is more important than the headline score.
A benchmark score says:
How much did the model succeed?
A residual report says:
What kind of model do we need next?
________________


Stage 5 — Diagnose the wall
When improvement slows, diagnose the bottleneck.
The key diagnostic question is:
Does performance improve when we change data, training, inference, tools, or architecture?
Data intervention
If better examples, cleaner labels, or targeted datasets improve performance, the system is data-limited.
Training intervention
If optimizer, curriculum, loss, schedule, post-training, or RL changes improve performance, the system is training-limited.
Inference intervention
If more test-time compute, chain-of-thought, search, tools, memory, retrieval, or agent scaffolding improves performance, the system is inference-limited.
Benchmark intervention
If performance changes under benchmark mutation, hidden holdouts, rewording, or contamination control, the benchmark may be the problem.
Architecture intervention
If none of the above produces meaningful movement, the wall is likely architecture-limited.
The architecture should change only after this diagnostic sequence.
________________


Stage 6 — Saturate or escalate
There are two main outcomes.
Outcome A: Benchmark saturated
The model performs near ceiling, and the benchmark no longer distinguishes progress.
Action:
* freeze benchmark as regression;
* add harder benchmark;
* expand evaluation frontier;
* preserve capability.
Outcome B: Wall persists
The model cannot improve despite data, training, and inference interventions.
Action:
* change architecture;
* add missing mechanism;
* alter representation;
* modify model class;
* add memory, tools, recurrence, search, symbolic structure, multimodality, or other needed capability;
* retrain and re-evaluate.
________________


Stage 7 — Promote saturated benchmarks to regression
A saturated benchmark still has value.
It becomes part of the regression suite:
Rt+1=Rt∪BtR_{t+1} = R_t \cup B_tRt+1​=Rt​∪Bt​
where BtB_tBt​ is the saturated benchmark frontier.
The regression suite protects against capability loss.
A new model should not improve on frontier Bt+1B_{t+1}Bt+1​ while forgetting BtB_tBt​.
This is the ratchet.
________________


Stage 8 — Find harder unsaturated benchmarks
Once a benchmark saturates, find or build a harder one.
Harder benchmarks may involve:
* longer horizon tasks;
* more realistic interactions;
* multi-step tool use;
* hidden tests;
* private holdouts;
* live tasks;
* adversarial variants;
* expert-level questions;
* multimodal inputs;
* distribution shifts;
* economic constraints;
* robustness requirements;
* safety constraints.
METR’s time-horizon work is an example of moving beyond static short-answer benchmarks by measuring the length of tasks AI agents can complete, defined by human expert completion time, with reliability thresholds such as 50% and 80%.
The frontier should always remain slightly ahead of the model.
________________


4. Formal Model
Let:
Mt=(At,θt,Dt,It)M_t = (A_t, \theta_t, D_t, I_t)Mt​=(At​,θt​,Dt​,It​)
where:
Term
	Meaning
	AtA_tAt​
	Architecture or model class.
	θt\theta_tθt​
	Trained parameters.
	DtD_tDt​
	Training and post-training data.
	ItI_tIt​
	Inference procedure, tools, memory, and scaffolding.
	Let the benchmark frontier be:
Bt={bt,1,bt,2,…,bt,n}B_t = \{b_{t,1}, b_{t,2}, \dots, b_{t,n}\}Bt​={bt,1​,bt,2​,…,bt,n​}
Let performance be:
S(Mt,Bt)=(st,1,st,2,…,st,n)S(M_t, B_t) = (s_{t,1}, s_{t,2}, \dots, s_{t,n})S(Mt​,Bt​)=(st,1​,st,2​,…,st,n​)
A benchmark is saturated when:
Sat⁡(Mt,bt,j)=1\operatorname{Sat}(M_t, b_{t,j}) = 1Sat(Mt​,bt,j​)=1
according to a saturation criterion such as:
st,j≥αjs_{t,j} \geq \alpha_jst,j​≥αj​
or:
Δst,j<ϵj\Delta s_{t,j} < \epsilon_jΔst,j​<ϵj​
over repeated development cycles, while confidence intervals overlap and residual errors are no longer meaningfully diagnostic.
A benchmark suite is saturated when:
Sat⁡(Mt,Bt)=∏j=1nSat⁡(Mt,bt,j)\operatorname{Sat}(M_t, B_t) = \prod_{j=1}^{n} \operatorname{Sat}(M_t, b_{t,j})Sat(Mt​,Bt​)=j=1∏n​Sat(Mt​,bt,j​)
A wall occurs when:
ΔS(Mt,Bt)≈0\Delta S(M_t, B_t) \approx 0ΔS(Mt​,Bt​)≈0
despite interventions on DtD_tDt​, training process, and ItI_tIt​.
An architecture change is justified when:
ΔS(At,Dt′,It′,Bt)<ϵ\Delta S(A_t, D'_t, I'_t, B_t) < \epsilonΔS(At​,Dt′​,It′​,Bt​)<ϵ
for reasonable data and inference interventions, but:
ΔS(At+1,Dt+1,It+1,Bt)>ϵ\Delta S(A_{t+1}, D_{t+1}, I_{t+1}, B_t) > \epsilonΔS(At+1​,Dt+1​,It+1​,Bt​)>ϵ
after architectural modification.
The ratchet advances when:
Bt→Rt+1B_t \rightarrow R_{t+1}Bt​→Rt+1​
and:
Bt+1B_{t+1}Bt+1​
is introduced as the new unsaturated frontier.
________________


5. The Diagnostic Ladder
Benchmaxxing uses an escalation ladder. Each level should be attempted before moving to the next, unless there is a clear reason to skip.
________________


Level 1 — Benchmark audit
Before changing the model, ask whether the benchmark is valid.
Questions:
* Are labels correct?
* Are tasks solvable?
* Are prompts clear?
* Are metrics aligned with capability?
* Is the benchmark contaminated?
* Is the benchmark too easy?
* Is the benchmark too narrow?
* Does performance transfer?
Test-set quality matters. Northcutt, Athalye, and Mueller found label errors in widely used ML test sets and argued that such errors can destabilize benchmark results.
________________


Level 2 — Data improvement
If benchmark failures are valid, improve data.
Actions:
* collect targeted examples;
* remove bad labels;
* add negative examples;
* improve diversity;
* create curricula;
* rebalance categories;
* generate synthetic data;
* add examples of failure modes;
* collect demonstrations.
If this works, the wall was data-limited.
________________


Level 3 — Training improvement
If data is not enough, improve training.
Actions:
* change loss;
* tune optimizer;
* adjust schedule;
* improve post-training;
* add RL;
* alter curriculum;
* improve distillation;
* change regularization;
* change sampling.
If this works, the wall was training-limited.
________________


Level 4 — Inference improvement
If training is not enough, improve inference.
Actions:
* add test-time compute;
* use search;
* add tools;
* add retrieval;
* add memory;
* add planning;
* add verifier;
* use self-consistency;
* add agent scaffolding.
This level is increasingly important as models gain latent capability but need better ways to deploy it at inference time.
________________


Level 5 — Architecture change
If data, training, and inference improvements fail, change the model.
Possible changes:
* new architecture;
* recurrence;
* memory;
* hierarchy;
* modularity;
* retrieval-native design;
* tool-native design;
* multimodal perception;
* state-space components;
* symbolic components;
* planner/verifier architecture;
* long-horizon state management.
Architecture changes should be motivated by benchmark residuals, not by novelty alone.
________________


6. Benchmark Lifecycle
Benchmarks have lifecycles.
________________


6.1 Frontier benchmark
A frontier benchmark is currently hard enough to expose meaningful failures.
Role:
* drive improvement;
* reveal missing capability;
* distinguish models;
* guide data/training/architecture decisions.
________________


6.2 Diagnostic benchmark
A diagnostic benchmark isolates a specific failure mode.
Examples:
* instruction following;
* long-horizon memory;
* tool use;
* spatial reasoning;
* mathematical proof;
* code debugging;
* planning;
* robustness;
* calibration.
Role:
* explain why a model failed;
* guide targeted interventions.
________________


6.3 Regression benchmark
A regression benchmark was once frontier but is now saturated.
Role:
* preserve prior capability;
* catch regressions;
* support comparisons;
* maintain compatibility.
________________


6.4 Retired benchmark
A retired benchmark is no longer useful even as regression.
Reasons:
* too contaminated;
* too noisy;
* too narrow;
* too misleading;
* too easy;
* too expensive relative to value.
Retirement should be explicit.
________________


6.5 Live benchmark
A live benchmark is continually refreshed.
Examples:
* new coding issues;
* new user tasks;
* new expert questions;
* new real-world workflows;
* private dynamic holdouts.
Live benchmarks are useful because they reduce overfitting and contamination risk.
________________


7. Anti-Goodhart Safeguards
Benchmaxxing must avoid becoming benchmark gaming.
Goodhart’s law warns that when a measure becomes a target, it can stop being a good measure. Benchmaxxing is especially vulnerable to this because it explicitly uses benchmarks to drive development.
Therefore, a serious performance ratchet must include safeguards.
________________


7.1 Benchmark rotation
Do not optimize one benchmark forever.
Rotate between:
* public benchmarks;
* private benchmarks;
* live benchmarks;
* human-evaluated tasks;
* adversarial tests;
* real-world trials.
________________


7.2 Private holdouts
Keep hidden evaluation sets that are not used during development.
Public benchmarks guide development.
Private benchmarks test generalization.
________________


7.3 Benchmark mutation
Create transformed versions of benchmark tasks to test robustness.
Microsoft Research’s “Saving SWE-Bench” work argues that existing software-engineering benchmarks can overestimate real-world coding-agent capability and proposes transforming formal GitHub issue descriptions into more realistic user-style queries.
This is exactly the kind of benchmark mutation that protects against overfitting to benchmark style.
________________


7.4 Multi-metric evaluation
Avoid a single score.
Measure:
* accuracy;
* robustness;
* calibration;
* latency;
* cost;
* memory;
* safety;
* consistency;
* real-world transfer;
* human preference;
* interpretability;
* long-horizon reliability.
HELM’s motivation for holistic evaluation includes broad coverage and multi-metric measurement rather than relying only on accuracy.
________________


7.5 Transfer checks
A benchmark improvement is suspicious if it does not transfer.
Ask:
* Does performance improve on hidden tasks?
* Does performance improve on live tasks?
* Does performance improve under rewording?
* Does performance improve in real workflows?
* Does performance improve for humans using the system?
________________


7.6 Contamination audits
Benchmarks should be checked for:
* training-data leakage;
* memorization;
* public solution exposure;
* prompt leakage;
* benchmark-specific tricks;
* suspiciously high exact-match behavior.
OpenAI’s statement that SWE-bench Verified had become increasingly contaminated illustrates the importance of contamination-aware benchmark lifecycles.
________________


7.7 Capability narratives
Each benchmark should be attached to a capability narrative.
Not:
The model scored 82%.
But:
The model can reliably resolve short, well-specified repository-level bug fixes under a bash-only environment, but still fails on ambiguous user-style requests, large refactors, and multi-day engineering tasks.
This prevents the score from pretending to be the whole capability.
________________


8. Benchmark Portfolio Design
A benchmark portfolio should be layered.
________________


8.1 Fast inner-loop benchmarks
These are cheap and frequent.
Purpose:
* quick iteration;
* catch regressions;
* monitor training.
Examples:
* small held-out set;
* unit tasks;
* synthetic diagnostics;
* cheap probes.
________________


8.2 Medium diagnostic benchmarks
These are slower but more informative.
Purpose:
* understand failure modes;
* compare variants;
* diagnose bottlenecks.
Examples:
* reasoning suites;
* tool-use tasks;
* data-quality probes;
* long-context tests.
________________


8.3 Frontier benchmarks
These are hard and expensive.
Purpose:
* guide major development decisions;
* decide whether architecture changes are needed;
* measure capability frontier.
Examples:
* expert-level tasks;
* long-horizon agent tasks;
* hidden holdouts;
* multi-step real-world tasks.
________________


8.4 Live external benchmarks
These are dynamic.
Purpose:
* avoid overfitting;
* test real-world transfer;
* track deployment readiness.
Examples:
* current user tasks;
* fresh coding issues;
* expert-curated questions;
* live competitions;
* production simulations.
________________


8.5 Safety and misuse benchmarks
These should be separate from capability benchmarks.
Purpose:
* measure risk;
* prevent unsafe capability growth;
* inform deployment.
OpenAI’s Preparedness Framework is an example of a structured approach to tracking frontier capabilities that could create severe harm, including explicit risk categories and safeguards reporting.
________________


9. Saturation Signals
A benchmark may be saturated when several signals appear together.
________________


9.1 Ceiling performance
The model reaches near-perfect or expert-level performance.
Example signal:
s≥0.95s \geq 0.95s≥0.95
depending on task and metric.
________________


9.2 Model clustering
Many frontier models produce similar top scores.
This means the benchmark no longer separates model quality well.
________________


9.3 Noise dominance
Remaining errors are mostly due to:
* ambiguous questions;
* mislabeled examples;
* bad tests;
* unclear prompts;
* benchmark artifacts.
________________


9.4 Weak transfer
Further improvements on the benchmark do not improve performance elsewhere.
________________


9.5 Contamination risk
The benchmark is public, heavily optimized, or likely present in training data.
________________


9.6 Low residual value
Failure analysis no longer teaches developers what to change.
This is one of the most important saturation signs.
A benchmark can still be difficult but no longer diagnostic.
________________


10. Wall Diagnosis
When a model cannot improve on an unsaturated benchmark, diagnose the wall.
________________


10.1 Data wall
Symptoms:
* failures cluster around missing knowledge;
* targeted examples improve performance;
* synthetic data helps;
* better labels help;
* retrieval helps.
Treatment:
* improve data coverage;
* clean labels;
* add targeted examples;
* add demonstrations;
* balance curriculum.
________________


10.2 Training wall
Symptoms:
* data exists but model fails to internalize it;
* loss or eval instability;
* poor generalization from examples;
* improvement depends on schedule or optimizer.
Treatment:
* modify training objective;
* improve curriculum;
* tune optimizer;
* add post-training;
* use RL or preference learning.
________________


10.3 Inference wall
Symptoms:
* model can solve with more time;
* model succeeds with tools;
* model succeeds with retrieval;
* model succeeds with decomposition;
* model succeeds with verifier.
Treatment:
* add test-time compute;
* add planning;
* add search;
* add memory;
* add tools;
* add self-checking.
________________


10.4 Benchmark wall
Symptoms:
* tasks are inconsistent;
* labels are wrong;
* prompt style dominates;
* mutations change performance drastically;
* real-world performance diverges.
Treatment:
* repair benchmark;
* add hidden holdouts;
* mutate prompts;
* add human validation;
* change metric.
________________


10.5 Architecture wall
Symptoms:
* data improvements fail;
* training changes fail;
* inference scaffolding fails;
* residuals point to missing representational or computational mechanism;
* failure persists across benchmark variants.
Treatment:
* change architecture;
* add missing state;
* add recurrence;
* add tool-native interfaces;
* add hierarchy;
* add perception;
* add memory;
* add verifier/planner structures.
________________


11. Architecture Evolution Discipline
Benchmaxxing encourages architectural restraint.
Architecture should not grow merely because a new idea is interesting.
Architecture should grow when the benchmark frontier proves a need.
________________


11.1 When not to change architecture
Do not change architecture if:
* benchmark is flawed;
* data is poor;
* labels are noisy;
* training is under-optimized;
* inference procedure is weak;
* failures are solvable with tools;
* performance improves under simple interventions.
________________


11.2 When to change architecture
Change architecture when:
* benchmark is valid and unsaturated;
* data interventions plateau;
* training interventions plateau;
* inference interventions plateau;
* residuals point to missing mechanism;
* simpler variants cannot cross the wall;
* new architecture improves target benchmark without regressing saturated benchmarks.
________________


11.3 Architecture change as hypothesis
An architecture change should be framed as:
This model fails because it lacks mechanism XXX. Adding XXX should improve benchmark class BBB while preserving regression suite RRR.
Example:
* If long-horizon tasks fail because the model loses state, add persistent memory.
* If tool-use tasks fail because the model cannot check outcomes, add verifier loops.
* If spatial tasks fail because the model lacks perceptual structure, add multimodal spatial representation.
* If coding tasks fail because repository state is too large, add retrieval and codebase graph memory.
The benchmark residual should motivate the architecture.
________________


12. Performance Ratchet Protocol
A mature Benchmaxxing system should follow this protocol.
________________


12.1 Maintain four benchmark sets
Set
	Purpose
	Development set
	Used frequently for iteration.
	Diagnostic set
	Used to understand failures.
	Private holdout
	Used to test generalization.
	Regression suite
	Used to preserve saturated capabilities.
	________________


12.2 Maintain a benchmark ledger
Each benchmark should have a ledger entry:
Field
	Meaning
	Name
	Benchmark identifier.
	Capability
	What it claims to measure.
	Status
	Frontier, diagnostic, regression, retired, live.
	Saturation level
	Unsaturated, approaching saturation, saturated.
	Contamination risk
	Low, medium, high.
	Label reliability
	Known quality.
	Transfer evidence
	Whether improvements generalize.
	Cost
	Runtime, compute, human review.
	Last refreshed
	Date of update.
	Retirement criteria
	When to stop using it.
	________________


12.3 Maintain a model ledger
Each model version should record:
Field
	Meaning
	Architecture
	Model design.
	Data
	Training and post-training data.
	Training process
	Losses, schedules, RL, curricula.
	Inference procedure
	Tools, memory, search, test-time compute.
	Benchmark scores
	Across all sets.
	Residual map
	Known failure clusters.
	Regression status
	Prior capabilities preserved or lost.
	Cost profile
	Training, inference, latency, memory.
	Safety profile
	Risk benchmark results.
	________________


12.4 Ratchet rule
A model advances only if:
FrontierGain⁡(Mt+1)>ϵ\operatorname{FrontierGain}(M_{t+1}) > \epsilonFrontierGain(Mt+1​)>ϵ
and:
RegressionLoss⁡(Mt+1)<δ\operatorname{RegressionLoss}(M_{t+1}) < \deltaRegressionLoss(Mt+1​)<δ
In plain language:
The new model must improve the frontier without losing prior saturated capabilities.
________________


13. Evaluation Beyond Accuracy
Benchmaxxing must avoid reducing progress to a single scalar.
Important axes include:
Axis
	Question
	Accuracy
	Does the model answer correctly?
	Reliability
	Does it work consistently?
	Calibration
	Does confidence match correctness?
	Robustness
	Does it survive perturbation?
	Efficiency
	What does performance cost?
	Latency
	How fast is it?
	Memory
	How much context/state does it require?
	Autonomy
	How long can it operate without help?
	Transfer
	Does benchmark progress generalize?
	Safety
	Does capability introduce unacceptable risk?
	Human usefulness
	Does it improve real workflows?
	METR’s work on task-completion time horizons is especially relevant to autonomy because it measures the human-time length of tasks that AI agents can complete at a given reliability threshold, rather than only isolated short-answer performance.
________________


14. Example: Coding Agents
Coding agents are a strong example of Benchmaxxing.
________________


14.1 Initial benchmark
A team starts with small coding tasks:
* function completion;
* unit-test generation;
* simple bug fixes;
* isolated algorithm problems.
The model saturates these.
________________


14.2 Next benchmark
The team moves to repository-level tasks such as SWE-bench.
SWE-bench evaluates agents on real GitHub issues, requiring them to generate patches in existing repositories.
________________


14.3 Saturation pressure
As models improve, SWE-bench Verified becomes less discriminative for frontier systems.
OpenAI’s February 2026 article argues that SWE-bench Verified no longer measures frontier coding capabilities well and recommends harder benchmarks such as SWE-bench Pro.
________________


14.4 Ratchet response
Benchmaxxing response:
1. keep SWE-bench Verified as regression;
2. add SWE-bench Pro or longer-horizon tasks;
3. mutate tasks into realistic user-style requests;
4. measure time-to-resolution, cost, and reliability;
5. diagnose failures:
   * missing repo context?
   * poor test interpretation?
   * weak planning?
   * bad tool use?
   * architecture unable to maintain long-horizon state?
Only then decide whether to improve data, tools, inference scaffolding, or architecture.
________________


15. Example: Knowledge and Reasoning Benchmarks
Knowledge benchmarks often saturate.
________________


15.1 MMLU
MMLU was once a major benchmark for broad multitask knowledge and reasoning.
As frontier models improved, scores rose high enough that new benchmarks were needed. Humanity’s Last Exam was introduced partly because LLMs had reached over 90% on popular benchmarks such as MMLU.
________________


15.2 GPQA
GPQA was designed as a graduate-level, Google-proof benchmark in biology, physics, and chemistry, with questions difficult even for experts and skilled non-experts.
________________


15.3 Humanity’s Last Exam
Humanity’s Last Exam escalates the frontier further by using expert-level closed-ended academic questions across broad subject coverage. The Nature paper frames it as a response to existing benchmarks not keeping pace in difficulty.
________________


15.4 Ratchet interpretation
The sequence is:
MMLU→GPQA→Humanity’s Last Exam→open-ended expert tasks\text{MMLU} \rightarrow \text{GPQA} \rightarrow \text{Humanity's Last Exam} \rightarrow \text{open-ended expert tasks}MMLU→GPQA→Humanity’s Last Exam→open-ended expert tasks
This is the Performance Ratchet in action.
Each benchmark applies pressure until it saturates, then the frontier moves.
________________


16. Example: Long-Horizon Agents
Short benchmarks can hide long-horizon weakness.
An AI system may solve isolated tasks but fail when required to maintain context, recover from errors, use tools, and pursue a goal for hours.
METR’s task-completion time horizon metric measures the length of tasks, in human expert time, that agents can complete at a given success probability; the 2026 page reports current measurements and describes the metric as a way to track frontier language-model agents on diverse software tasks.
Benchmaxxing suggests treating time horizon as a ratchet dimension:
5 minutes→30 minutes→2 hours→1 day→1 week5\text{ minutes} \rightarrow 30\text{ minutes} \rightarrow 2\text{ hours} \rightarrow 1\text{ day} \rightarrow 1\text{ week}5 minutes→30 minutes→2 hours→1 day→1 week
At each stage, the model must preserve shorter-horizon reliability while extending autonomy.
________________


17. Failure Modes
Benchmaxxing can fail.
________________


17.1 Benchmark gaming
The model improves on the benchmark but not the real capability.
Mitigation:
* private holdouts;
* live benchmarks;
* mutation;
* transfer checks;
* multi-metric evaluation.
________________


17.2 Leaderboard addiction
Teams chase public scores without improving useful capability.
Mitigation:
* capability narratives;
* real-world tasks;
* deployment metrics;
* human usefulness measures.
________________


17.3 Premature architecture escalation
Teams change architecture before exhausting data, training, and inference interventions.
Mitigation:
* diagnostic ladder;
* ablations;
* intervention logs;
* model ledger.
________________


17.4 Benchmark stagnation
Teams keep using saturated benchmarks because they are familiar.
Mitigation:
* benchmark lifecycle;
* saturation criteria;
* scheduled benchmark review;
* retirement policy.
________________


17.5 Regression blindness
A new model improves frontier scores but loses prior capabilities.
Mitigation:
* regression suite;
* ratchet rule;
* capability lock-in.
________________


17.6 Overfitting to benchmark style
The model learns benchmark format instead of capability.
Mitigation:
* prompt mutation;
* hidden variants;
* task rephrasing;
* format diversity.
________________


17.7 Evaluation noise
Benchmark labels, tests, or metrics are flawed.
Mitigation:
* human validation;
* label audits;
* uncertainty estimates;
* multiple metrics.
________________


17.8 Safety neglect
Capability improves while safety is ignored.
Mitigation:
* safety benchmark suite;
* risk thresholds;
* deployment gates;
* red-team evaluation.
________________


18. Research Agenda
18.1 Saturation detection
Questions:
* How do we formally detect benchmark saturation?
* How do we distinguish ceiling performance from benchmark noise?
* How do we estimate remaining diagnostic value?
________________


18.2 Benchmark frontier construction
Questions:
* How do we generate harder benchmarks?
* How do we avoid making benchmarks artificially hard but irrelevant?
* How do we ensure new benchmarks measure real capabilities?
________________


18.3 Wall diagnosis
Questions:
* How do we tell data walls from architecture walls?
* How do we quantify when inference scaffolding is enough?
* How do we decide when architecture change is justified?
________________


18.4 Transfer measurement
Questions:
* Does benchmark progress transfer to live tasks?
* Which benchmarks predict deployment value?
* How should benchmark portfolios be weighted?
________________


18.5 Benchmark mutation
Questions:
* How can tasks be automatically transformed without changing core difficulty?
* How can mutated benchmarks reveal overfitting?
* How can benchmark mutation preserve human interpretability?
________________


18.6 Performance-cost tradeoffs
Questions:
* When is a score improvement worth the compute?
* How should latency and inference cost enter benchmark leaderboards?
* Should benchmark scores include resource-normalized metrics?
________________


18.7 Safety ratchets
Questions:
* How do safety evaluations ratchet alongside capability?
* How do we prevent capability benchmarks from outrunning safety benchmarks?
* How do we define non-regression for safety?
________________


19. Implementation Roadmap
Phase 1 — Benchmark ledger
Create a benchmark registry with:
* status;
* capability;
* saturation level;
* cost;
* contamination risk;
* transfer evidence;
* retirement criteria.
________________


Phase 2 — Model ledger
Track every model version with:
* architecture;
* data;
* training;
* inference procedure;
* scores;
* residuals;
* regressions;
* cost profile.
________________


Phase 3 — Residual analysis
For every benchmark run, produce:
* failure clusters;
* error taxonomy;
* benchmark flaw report;
* intervention recommendation.
________________


Phase 4 — Diagnostic ladder
Before changing architecture, run structured interventions:
1. benchmark audit;
2. data improvement;
3. training improvement;
4. inference improvement;
5. architecture modification.
________________


Phase 5 — Benchmark frontier expansion
When a benchmark saturates:
* promote to regression;
* create harder variant;
* add hidden holdout;
* add live benchmark;
* add transfer benchmark.
________________


Phase 6 — Ratchet enforcement
Require every new model to:
* improve frontier benchmark;
* preserve regression suite;
* maintain safety profile;
* report cost and latency.
________________


20. Public Claims and Non-Claims
20.1 Claims
This paper claims:
1. AI development often follows a benchmark saturation and frontier expansion loop.
2. Benchmarks should be treated as temporary pressure surfaces, not permanent definitions of intelligence.
3. Saturated benchmarks should become regression tests.
4. New benchmark frontiers should expose unsolved capability gaps.
5. Architecture changes should be justified by benchmark residuals after data, training, and inference interventions fail.
6. Good Benchmaxxing requires anti-Goodhart safeguards.
7. A mature benchmark portfolio should include public, private, live, diagnostic, regression, efficiency, and safety evaluations.
8. The performance ratchet provides a disciplined way to grow a model from small and manageable to increasingly capable.
________________


20.2 Non-claims
This paper does not claim:
1. Benchmarks perfectly measure intelligence.
2. Higher benchmark scores always mean better real-world capability.
3. Architecture should never change early.
4. Data improvements can solve every wall.
5. Scaling laws are sufficient for all progress.
6. Benchmark saturation proves true mastery.
7. All benchmarks should be public.
8. A single benchmark can define progress.
9. Benchmaxxing eliminates Goodhart risk.
10. Real-world deployment can be replaced by benchmark performance.
The proposal is a development methodology, not a complete theory of intelligence.
________________


21. Conclusion
Benchmaxxing names a development loop already visible across modern AI:
benchmark
   ↓
train
   ↓
saturate or hit wall
   ↓
diagnose
   ↓
improve data / training / inference
   ↓
change architecture only when necessary
   ↓
find harder benchmarks
   ↓
preserve prior capability
   ↓
repeat
The core principle is:
Let benchmarks apply pressure, but never let a saturated benchmark define the frontier.
A benchmark is useful while it teaches the developer something.
When it stops teaching, it should be promoted to regression status.
The next benchmark should be harder, broader, more realistic, more diagnostic, or more aligned with the desired capability.
The model grows by ratchet:
* capabilities are validated;
* saturated benchmarks are locked in;
* new benchmarks expose missing abilities;
* interventions are escalated in disciplined order;
* architecture evolves only when evidence demands it.
Benchmaxxing is therefore not leaderboard chasing.
It is performance ratcheting:
A disciplined process for turning benchmark saturation into capability growth.
________________


Appendix A — Benchmaxxing Checklist
Use this checklist for any development cycle.
1. Benchmark status
* Is the benchmark frontier, diagnostic, regression, live, or retired?
* Is it saturated?
* Is it contaminated?
* Does it still distinguish models?
2. Residual analysis
* What failed?
* Why did it fail?
* Are failures meaningful or benchmark artifacts?
* Do failures cluster?
3. Intervention ladder
Before changing architecture, did you test:
* data improvements?
* training improvements?
* inference improvements?
* benchmark quality?
4. Architecture justification
If changing architecture:
* what residual motivates the change?
* what mechanism is missing?
* what benchmark should improve?
* what regression suite must be preserved?
5. Ratchet update
* Which benchmarks move to regression?
* Which benchmarks become frontier?
* Which benchmarks retire?
* What capability was locked in?
________________


Appendix B — Benchmark Ledger Template
Field
	Description
	Benchmark name
	Name of benchmark.
	Capability measured
	What it claims to measure.
	Benchmark type
	Frontier, diagnostic, regression, live, safety, efficiency.
	Saturation status
	Unsaturated, approaching saturation, saturated.
	Contamination risk
	Low, medium, high.
	Label/test quality
	Known quality issues.
	Cost
	Runtime, compute, human review.
	Transfer evidence
	Does improvement generalize?
	Regression value
	Should it be preserved?
	Retirement criteria
	When to stop using it.
	________________


Appendix C — Model Ledger Template
Field
	Description
	Model version
	Identifier.
	Architecture
	Model design.
	Training data
	Dataset summary.
	Training process
	Losses, optimizer, schedule, post-training.
	Inference process
	Tools, search, memory, test-time compute.
	Benchmark scores
	Full portfolio.
	Residual map
	Known failure categories.
	Regression status
	Prior capabilities preserved?
	Cost profile
	Training/inference/latency/memory.
	Safety profile
	Risk evaluation.
	Next wall
	Current limiting factor.
	________________


Appendix D — One-Paragraph Public Summary
Benchmaxxing: The Performance Ratchet is a framework for developing AI models through iterative benchmark saturation and frontier expansion. A model begins small and manageable, trains against an initial benchmark suite, improves through data, training, and inference interventions, and eventually either saturates the benchmark or hits a wall. Saturated benchmarks become regression tests. New harder benchmarks become the frontier. If better data, training, and inference cannot break through the wall, the architecture changes. The process repeats, creating a capability ratchet in which proven abilities are preserved while new benchmarks expose the next missing capability. Benchmaxxing is not benchmark gaming; it is disciplined benchmark-driven model evolution with anti-Goodhart safeguards.
________________


Appendix E — Compact Manifesto
Do not worship benchmarks.
Use them.
Let them apply pressure.
Let them expose weakness.
Let them tell you whether the wall is data, training, inference, evaluation, or architecture.
When a benchmark saturates, honor it as a regression test.
Then move on.
The frontier is always the benchmark you cannot yet beat.
The ratchet turns when yesterday’s frontier becomes today’s floor.
That is Benchmaxxing.
________________


Selected References
1. OpenAI, Scaling Laws for Neural Language Models.
2. Hoffmann et al., Training Compute-Optimal Large Language Models.
3. Stanford CRFM, Language Models are Changing AI: The Need for Holistic Evaluation / HELM.
4. METR, Measuring AI Ability to Complete Long Tasks.
5. METR, Task-Completion Time Horizons of Frontier AI Models.
6. Nature, A benchmark of expert-level academic questions to assess AI capabilities / Humanity’s Last Exam.
7. SWE-bench, SWE-bench Verified.
8. OpenAI, Why SWE-bench Verified no longer measures frontier coding capabilities.
9. Microsoft Research, Saving SWE-Bench: A Benchmark Mutation Approach for Realistic Agent Evaluation.
10. Mattson, Bushardt, and Artino, “When a Measure Becomes a Target, It Ceases to be a Good Measure”.
11. Northcutt, Athalye, and Mueller, Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks.