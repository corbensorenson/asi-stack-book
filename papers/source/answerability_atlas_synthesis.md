# What an Answerability Atlas Can and Cannot Do

## An audited synthesis of computational design experiments

Answerability Atlas Project | Working paper, version 1.0 | 25 October 2026

Retrospective synthesis of a closed research program. Not submitted or externally peer reviewed. Prepared as a technical source for the ASI Stack project. The project designation identifies the research artifact; final personal authorship and publication decisions belong to its owner.

## Abstract

An answerability atlas records which computational systems can answer which questions under explicit information, correctness, resource and lifetime conditions. The motivating hypothesis was that such a map could also diagnose missing capabilities and choose more productive design experiments. We synthesize three phases of a local research program and its subsequent controls and corrections. Positive findings include a finite reference laboratory, independently checked accounting and replay, representation-dependent storage tradeoffs, useful compilation in restricted workloads, and a modest development-stage signal for selecting supplied components. The stronger discovery claim was not established. A registered 32-world CPU comparison favored factorized engineering over the tested atlas heuristic: mean difference -0.005783, approximate 95% interval [-0.009672, -0.001838]. In coupled synthetic worlds, diagnostic priority routing lost to its matched ablation at every tested interaction level. A revised grammar-expansion controller gained +0.014955 at its once-only validation budget, but missed its advance margin and failed a separate spending screen. An exploratory paid-key-oracle-policy screen initially passed; adding an omitted buy-all baseline reduced its largest-budget headroom to +0.035299, below the fixed +0.04 continuation threshold. The corrected decision was stop. These results support conditional measurement and scoped empirical knowledge, while providing no demonstrated diagnosis-specific discovery advantage, general invention principle, physical energy result or claim about artificial superintelligence. The central lesson is to evaluate the entire path from information to useful deployment against the simplest strong alternatives, with uncertainty and failed controls preserved.

**Keywords:** computational design; metareasoning; quality diversity; diagnostic search; compositional search; negative results; reproducibility; evidence accounting.

## Reader's orientation

The broad idea was sensible: organize what existing systems can do, notice what is missing, and use that diagnosis to decide what to build or measure next. The experiments separated three questions that are easy to conflate. Can the map describe systems honestly? Can a model predict their behavior? Can a controller use those descriptions and predictions to discover better systems for its cost? We obtained useful results on the first question and mixed results on the second. The tested controllers did not establish the third.

The final correction gives a simple example. In a small library, a method can purchase every building block and then search for useful combinations. That can leave less room for an intelligent selector than a comparison against weaker selectors suggests. The correction did not erase all positive observations. It changed whether the remaining measured opportunity justified continuing under the program's own rule. Sections 3-8 report the evidence; Sections 9-11 distinguish contributions, limitations and implications for ASI Stack.

## 1. Research question and contribution boundaries

The motivating object is an executable system together with the conditions under which it can answer a collection of questions. Stored answers, compact procedures, approximation with correction, caches, indexes and adaptive compositions can occupy different cost-capability regimes. Their relative merits depend on the task distribution, available information, required correctness, representation, reuse horizon and accounting boundary. A map can expose these conditions without implying a universal law relating intelligence, speed, storage, energy or generality.

The stronger proposal was that absent or weakly occupied regions of this map reveal useful experiments. A gap might reflect an untested existing implementation, missing information, an inadequate design language, a real tradeoff, a measurement artifact or a genuinely impossible target. Classifying these possibilities is valuable only if the classification is supported; choosing an experiment is valuable only if its downstream benefit justifies its cost. Those are distinct claims. A conservative reporting tool can be useful even when its associated search controller loses.

This paper's contributions are a synthesis of the program's empirical results, an explicit reconciliation of later corrections with earlier manuscripts, and a set of bounded engineering lessons. It introduces no new experiment, confidence interval, architecture, theorem or registered hypothesis. Original artifacts remain unchanged. The evidence snapshot is the completed source record at commit `d36a09b37c928165b5743703d0d6ad820cccc629`; the synthesis has its own source and evidence manifests.

### 1.1 Relation to established work

Design-space organization and resource-conditioned synthesis have close precedents in the Data Calculator and Design Continuums [1,2]. Quality-diversity search already seeks useful alternatives across behavioral descriptors: MAP-Elites provides the map, MOME places tradeoff sets within its cells, and BOP-Elites uses surrogate models for expensive objectives and descriptors [3-5]. Expected-hypervolume methods also address uncertainty when choosing multiobjective evaluations [6]. An atlas or a Pareto archive is therefore insufficient, by itself, to establish methodological novelty.

The value of spending computation on better decisions is an established metareasoning question [7]. Additive optimization and inferred variable-group structure are established modeling approaches [8,9]; functional-ANOVA methods provide antecedents for decomposing variation [10]. DreamCoder learns reusable abstractions and a search policy together [11]. This project's supplied expansion library does not implement that kind of primitive invention. QDEvo combines language-model-driven heuristic search with a diverse multiobjective archive [12]; this laboratory did not benchmark that system or autonomous code generation. Random search remains a serious baseline [13], and model selection itself can overfit finite evaluation data [14].

These comparisons position the work rather than certify exhaustive priority. The accompanying citation audit states which primary abstracts, metadata and full-text sections were checked. No external paper's performance result is transferred to the present experiments, and local evolutionary, quality-diversity and Bayesian-optimization-inspired arms are not claimed to be faithful reproductions of every published method.

## 2. Evidence model and study design

### 2.1 Contracts, resources and utility

An answerability contract fixes tasks and their weights; permitted observations; response semantics; correctness, freshness and deadline requirements; substrate; preparation and update rules; service horizon; resource accounting; and statistical acceptance rules. A content hash identifies its serialized form. Changing information access or the horizon changes the comparison, even if an informal task name stays the same.

Capabilities are retained as task-indexed outcomes. A single breadth score can summarize them but can hide complementary successes and failures. The deployment of two stored implementations and a router incurs its own storage and selection costs; their combined capability is not a free union. Likewise, a shortlist of four independently executable designs is an evaluation archive, not an automatically deployed system with the union of all four capabilities.

Resource measurements remain distinct. Encoded task-dependent state is not resident memory. An answer-component interval excludes operations that a delivered-service measurement may include. Preparation, updates, verification, failed trials, controller computation and data persistence need explicit boundaries. Unknown physical energy is recorded as missing. Stipulated actions in synthetic worlds do not become seconds or joules. These distinctions are essential to interpreting both the positive mechanisms and the negative search results.

An elementary conditional fact illustrates the boundary of the foundations. For a fixed design universe and the same scalar cost function, strengthening requirements can only shrink the feasible set, so its infimum cost cannot decrease. Equality remains possible. The argument does not establish a strictly positive generality tax, compare different resource coordinates, or show that all algorithms form a useful smooth geometric space. Finite exclusions similarly concern a declared grammar, not unrestricted computation.

### 2.2 Independent units and inference status

The principal inference unit is a generated world. Two fixed optimizer-seed conditions are averaged within a world before world-level inference. Repeated methods, budgets, mappings, integrity reruns and raw event counts do not create additional independent worlds. Main studies, separate family extensions, development evidence, validation and exploratory follow-ups are not pooled into one effect estimate.

| Evidence stage | Independent units and role | What the stage can support |
| --- | --- | --- |
| Finite reference and CPU pilots | Exhaustive declared Boolean worlds; fixed CPU development workloads | Exact bounded-model checks and descriptive machine observations |
| Phase 1 discovery | 32 registered primary worlds; separate 16-world family extension | A scoped policy comparison under the registered score and CPU protocol |
| Maintenance | 8 prospective worlds, 144 conditions | An exploratory comparison of frozen mechanism selectors |
| Phase 2 | 256 worlds at each of five interaction levels; separate 16 per level in a higher-order study | Registered tests of the specified routing controller |
| Phase 3 | 48 training worlds reused across three mappings; one separate 48-world validation, eight per class | A bounded development decision; formal confirmation was not run |
| Phase 3.1 controls | The same 48 inspected training worlds | Descriptive comparison of two additional engineering recipes |
| Phase 3.2 / 3.2a | 24 key-pair worlds; correction reuses those worlds | An exploratory operational headroom screen and its post hoc comparator correction |

Table 1. Study roles are not interchangeable. Most reported intervals are ordinary approximate 95% paired-world percentile intervals. The Phase 3 development gate used its prewritten 80% interval. The final headroom screen used ordinary 95% intervals across three budgets, with a separate multiplicity sensitivity. These are not a common family of confirmatory tests. Sources: [E04-E20].

### 2.3 Integrity and independence of checks

The laboratory retains contracts, source snapshots, private evaluator state, prediction cards recorded before outcomes, charged actions, frozen shortlists and raw histories. Hash chains and schemas detect particular integrity failures. Independent references reconstruct truth, charges, admissibility and scores using separate calculations rather than simply calling the producer's result routine. Failures and resource amendments remain visible. Those controls establish the checks actually performed; they do not establish that the controller's scientific mechanism is correct.

The experimental implementation and review were AI assisted. Codex performed implementation, collection, analysis and manuscript work; Claude supplied plans and reviews; the human owner directed scope and approved specified continuations. Agreement between assistants is not external peer review or independent experimental replication. Human and agent labor is provenance, not an invented CPU-equivalent cost. This synthesis reviews retained results and introduces no additional scientific sampling.

## 3. Positive findings from the measurement laboratory

### 3.1 Exact statements inside a finite language

The reference laboratory enumerates 1,296 encoded Boolean designs under a shared decoder and stipulated costs. Independent frontier checks cover all 256 three-input Boolean worlds. This is a useful positive result about implementation correctness within the finite model. It is not an exhaustive map of all possible algorithms or an unrestricted information lower bound. A separate CPU finite-output audit checks 64,096 outcomes across 30 world/method pairs, with 23 pairs correct throughout their declared sweeps. Neither a fixed sweep nor those counts cover every possible mutable-cache history. [E01; foundations manuscript in the review corpus]

Eight constructed diagnosis challenges exercise withheld implementations, finite exclusion, hidden preparation, unavailable information, grammar expansion, noisy apparent superiority, scalar ties with different capabilities and distribution shift. Responses match their prespecified rubric, including an intentionally unresolved case where the controller lacks a supported certificate. These are engineering fixtures, not a generalization estimate of diagnostic accuracy. The useful behavior is preserving uncertainty when the available evidence does not warrant exclusion.

### 3.2 Measured mechanisms and accounting boundaries

Two corrected CPU pilots each contain 120 candidate measurements. They show that familiar mechanisms can be useful under explicit conditions. The batch pilot's ratios below compare affine compilation with interpretation, or residual encoding with an exact table. Ratios concern the named representation and timing component, not arbitrary programs, optimal description length, total delivered latency or physical energy. [E02,E03]

| Fixed workload contrast | Encoded-state ratio | Mean answer-component ratio range |
| --- | --- | --- |
| Affine compilation, depth 12 | 0.05525 | 0.1307 to 0.2424 |
| Affine compilation, depth 2 | 0.2568 | 0.4106 to 0.4623 |
| Residual encoding, no exceptions | 0.1698 | 0.1492 to 1.8914 |
| Residual encoding, 50% exceptions | 1.5111 | 1.5371 to 2.3602 |

Table 2. Four paired process/recurrence conditions per row. These fixed-world pilot ranges are descriptive, not population confidence intervals. Lower ratios favor the first named mechanism. [E02]

The storage reversal is informative. The residual representation is compact in the zero-exception Boolean workload but larger than the table at high exception density. Compilation reduces the measured answer component in the restricted affine workloads. These observations support conditional engineering claims about shared structure and representation. The mechanisms themselves are established techniques, not inventions of this program.

Instrumentation is also consequential. Instrumented RPC and answer-component rankings disagree in five of eight compilation comparisons. Serialization, hashing and verification lie inside one boundary and outside the other, and the shared desktop has uncontrolled background load. The comparison does not isolate one overhead as the sole cause. It demonstrates why a claim must name its cost boundary. The CPU evidence comes from Windows 10 build 19045, CPython 3.11.9 and an AMD Ryzen 7 3700X; it should not be generalized into a hardware-independent speedup. [E03]

### 3.3 What the infrastructure contributes

The positive infrastructure contribution is an executable way to distinguish observed witnesses, model predictions, supported finite exclusions and unresolved targets, with task-level capability and lifecycle accounting. The record includes separate replay references, adversarial corruption checks and restoration checks. It makes a claim inspectable and falsifiable in the implemented setting. This is a concrete research artifact and a combination of established evidence practices, not a demonstrated new universal standard or proof that similarly instrumented search will succeed.

## 4. Phase 1: useful components did not imply better discovery

The first discovery experiment searches a closed composition language with six task slots: two Boolean mappings, two exact rank workloads and two supplied affine-expression workloads. Four slots have nine choices each and two have seven, giving 321,489 encoded compositions. Six local policies receive the same permitted information, common prior observations, grammar, evaluator and wall-time admission rule. They are random search, a specified evolutionary baseline, Pareto-cell quality diversity, a proposer-matched no-atlas arm, the atlas heuristic and factorized engineering.

The factorized comparator uses component observations to assemble designs, then evaluates those compositions. It is a serious engineering alternative in this largely decomposable grammar, not a certified globally optimal solver. The atlas heuristic uses component predictions, novelty and missing-skill complementarity. The experiment tests their net performance under actual controller and evaluation costs, rather than declaring the map useful because it can display an attractive point.

The registered primary outcome is audited shortlist hypervolume under fixed transforms and preferences. Across 32 worlds, the atlas-minus-factorized mean is -0.005783, with approximate 95% interval [-0.009672, -0.001838]. The registered rule favors factorized engineering. A separate 16-world interval-sum extension with unchanged policy source has mean -0.005609, interval [-0.011385, -0.000311]. The extension is not pooled with the primary and establishes only one limited transfer observation. [E04,E05]

There was also a positive exploratory ablation difference in the main study: Atlas exceeded no-atlas by about +0.006972. The later family reanalysis gives -0.002932, interval [-0.009108, +0.002641]. Thus the initial ablation hint did not reproduce in direction across the two studies. Slight interval differences among exploratory reports reflect declared bootstrap seeds, not changed raw outcomes. Stronger component information could help a particular ablation without beating the simpler engineering comparator or isolating diagnosis itself. [E06]

### 4.1 Prospective maintenance remained uncertain

The maintenance study freezes predictions for existing update/query mechanisms and evaluates them on eight worlds with 144 conditions. Mean excess cost relative to the within-condition measured best is 0.162704 for the work-count selector and 0.159397 for generic regression. Their paired world difference is +0.003306, with approximate 95% interval [-0.025998, +0.029082]. Positive differences here mean more excess cost. There is no clear advantage and no established equivalence. [E07]

The fixed choices and exact current-world checks are useful artifacts. Their existence does not show that a mechanistic selector generalizes better than regression. Output limits required a recorded resource-only continuation that preserved completed records. Some original whole-attempt time and interrupted work remain unknown. Consequently, no complete maintenance research-wall or energy-efficiency claim is made. These missing quantities are part of the result, not values to be replaced by zero.

## 5. Phase 2: interactions exposed a routing failure

### 5.1 Coupled worlds and a cleaner ablation

Phase 1's mostly decomposable language left open whether diagnosis would become useful when design choices interact. Phase 2 therefore uses finite synthetic worlds with stipulated costs and exact truth, sweeping the share of variation unexplained by component-wise effects through 0, 0.10, 0.25, 0.50 and 0.75. The primary study contains 1,280 worlds and 23,040 runs. A separately analyzed higher-order study adds 80 worlds and 1,440 runs. Nine local arms include factorized and joint models, a random-forest Bayesian-optimization arm, and matched diagnostic controls. These counts do not imply comparison with every established optimizer. [E08,E09]

The controller routes actions using fixed priorities over diagnosis tags; its ablation shares the model, proposals and action types while removing that routing layer. Builds and replications cost one stipulated unit; four-cell probes cost four. The 32-unit budget is an action-cost convention, not equal physical controller CPU expenditure. A positive result requires two meaningful wins at the same interaction level: over the ablation and over the frozen traditional comparator.

| Interaction share | Atlas minus no-diagnosis mean | Ordinary 95% interval |
| --- | --- | --- |
| 0.00 | -0.017888 | [-0.025641, -0.010169] |
| 0.10 | -0.027936 | [-0.036345, -0.019360] |
| 0.25 | -0.037794 | [-0.046888, -0.028747] |
| 0.50 | -0.062102 | [-0.072077, -0.052224] |
| 0.75 | -0.110307 | [-0.120758, -0.099797] |

Table 3. Primary registered contrasts, 256 worlds per interaction level and two fixed seeds averaged within each world. Multiplicity-aware advance rules are retained in the original analysis; this table displays the ordinary intervals. No level achieved the required pair of meaningful wins. [E08]

The diagnosis controller loses to its ablation throughout the sweep, and the loss grows with coupling. The separate higher-order study supplies no advancing level either. Joint modeling nevertheless has higher descriptive quality than the factorized model at the stronger primary interaction levels. Modeling interactions and deciding how to spend experiments on them are different questions. The results support the usefulness of richer modeling in some regimes without supporting the additional routing policy.

### 5.2 Informative measurements can have insufficient decision value

At the highest interaction share, the atlas averages about 4.08 pair probes and 14.92 builds, whereas the ablation averages about 0.086 probes and 31.18 builds. Many selected probes expose real interaction contrasts: 3,498 of 4,411 selected primary atlas probes exceed the practical absolute contrast threshold. Only one satisfies the more specific joint-only move criterion used in that probe audit. These counts describe selected probes, not the prevalence of interactions or a general diagnostic-precision estimate. [E08; Phase 2 retained report]

This pattern is consistent with spending too much on measurements that do not repay their opportunity cost in the final shortlist. It does not prove that probe expenditure alone caused the loss. Priority routing also changes replications, information purchases, which designs are built, posterior histories and subsequent proposals. The matched comparison identifies the net consequence of this implemented layer; it is not a randomized causal decomposition of its individual actions.

### 5.3 Calibration and shuffle-control corrections

The registered equal-level aggregate forecast rule really passed. Primary nominal 80% coverage averages 0.819182. Yet coverage is 0.968480 at zero coupling and 0.585005 at 0.75 coupling; the higher-order high-coupling value is about 0.5232. An aggregate pass cannot support the stronger claim of calibration in every regime. Later ledger corrections preserve the original aggregate result while rejecting the stronger per-level interpretation. [E08-E10]

The shuffle control had another material limitation. All 58,828 audited shuffled decisions retained the relevant interaction tags. That control therefore could not test the value of those tags' content. This does not invalidate the atlas-versus-no-diagnosis outcome, but it restricts explanations based on the shuffled arm. Reviews also identified tag priorities overriding numerical value, a broad capability tag restricting builds, rare capture of joint-only opportunities and a budget-selection rule that measured larger budgets but selected its floor without bracketing. These are explanations and design limitations to examine, not proof of a single complete cause. [E10]

The registered controller line stopped. Physical CPU transfer, RocksDB and unrestricted mechanism invention were not completed stages of this phase.

## 6. Phase 3: a modest signal and a failed development gate

### 6.1 Learned priors helped some predictions, not the whole problem

A closing model check reuses 40 old development worlds and two fixed seed conditions. It compares factorized and joint predictors with three variance scales selected by empirical Bayes on a fixed main/pair basis. This is a limited plug-in adaptation, not full structure discovery or integrated hyperparameter uncertainty. At the strongest interaction level, joint latent-cost coverage improves from about 0.5335 to 0.8158. Quality changes are mixed across levels. [E11]

The prewritten joint criterion still fails: zero-interaction joint coverage is 0.903460, slightly above its 0.90 upper boundary, although the signed factorized-minus-joint gap condition passes. The failure of that conjunction should not obscure the substantial high-coupling coverage repair. Nor does the repair establish better search or a universal solution to model misspecification. Eight repeated development worlds per level provide limited evidence.

### 6.2 Expansion from a supplied library

The new generator supplies eight extra primitives over a six-gene base grammar; the full grammar contains exactly 22,500 identities. The six world classes are single keys, paired keys, misleading decoys, cost keys, base-sufficient negative controls and unreachable negative controls. In paired-key worlds, both components are needed to restore a missing capability. World class, latent arrays, true key IDs and exact fronts remain private to evaluation; only the reference oracle gets the key IDs.

This is selection from a declared library. No primitive implementation is invented. Cost and state contain explicit main and pair interactions, and the utility is latent hypervolume of an observed-greedy shortlist of at most four designs, divided by the unlimited full-grammar true frontier. That denominator is not a proven best four-design shortlist or best limited-budget policy. The meaningful margin of 0.02 is two percentage points of this normalizer, not a physical speedup. [E12,E13]

The generator and independent reference were frozen before the atlas-specific expansion policy. Diagnosis now modifies a new component's prior inside one common value-per-cost score; it cannot override that score or change proposal eligibility. Shared predictors and proposals still choose what to build after a purchase. A genuine semantic shuffle permutes every used tag. Stronger neutral-prior and ordinary engineering arms receive the same library and information.

Three permitted training mappings reuse the same 48 worlds. The final mapping is chosen by a prewritten last-revision rule, not by retrospectively selecting the best training mean, and is frozen before one separate 48-world validation. Earlier mapping 2 has a slightly larger training mean than mapping 3; it is not independently validated. This is a limitation of the development rule, not permission to substitute mapping 2 afterward. Bracketed random/oracle calibration selects 32 units without using atlas outcomes.

### 6.3 The positive result and the stop must both be reported

At the fixed validation budget, Atlas scores 0.826683, its ablation 0.811729, and the strongest traditional point mean, the neutral prior, 0.814525. The atlas-minus-ablation mean is +0.014955, with the prewritten ordinary 80% interval [+0.007198, +0.023026]. That is a modest positive validation signal for the complete recipe. It does not establish a diagnosis-specific causal effect. [E12,E13]

The point mean misses the fixed 0.02 advance margin. Atlas also spends 1.5625 more units in unreachable worlds than its ablation, failing the separate development spending screen. The decision is no-go. Because the interval includes 0.02, no-go is not proof that the population effect is smaller than 0.02. The development screen was deliberately strict, including zero-excess spending conditions; its operational choice is not a universal economic criterion for exploration. Formal confirmation hypotheses remain untested, rather than becoming another set of confirmatory refutations.

Composition is weak at this budget. In the paired-key validation class, Atlas deploys both required keys together in 1 of 16 seed conditions, compared with 7 of 16 for the privileged reference. Those 16 conditions are nested in eight worlds. Even knowing the keys does not ensure that the generic follow-up policy will combine and use them within the budget. Purchase precision, prediction quality and useful deployment must therefore remain separate outcomes. [E21; Phase 3 retained report]

## 7. Follow-up controls: gains remained mechanistically unresolved

### 7.1 The missing budget table

The Phase 3.1 addendum reports every original arm at 16, 32 and 64 units, by class and overall, on validation and final training data. At validation budget 64, Atlas exceeds its ablation by +0.029681, but trails claim matching by -0.013044, with ordinary 95% interval [-0.028245, +0.001164]. Claim matching's superiority is not statistically settled by that interval. Conversely, the declared exploratory margin test excludes a +0.02 Atlas advantage over claim matching. No measured budget combines the required ablation point gain with a nonnegative atlas point mean against every frozen traditional comparator. This reinforces the earlier no-go without replacing its original budget or gate. [E14]

Shuffled diagnosis retains 40.73% of the atlas-over-ablation mean gain at budget 32 and 65.55% at 64. These are ratios of observed mean differences, not causal shares attributable to generic engineering. Partially correct shuffled assignments, gap existence, transported context and optimism remain mixed. In the final mapping, cost-key score contrasts are inactive: all 24 validation world/budget differences are exactly zero. That setting cannot establish the usefulness or uselessness of an active cost-diagnosis mechanism. [E14]

### 7.2 Transport and affordability controls

Two approved training-only controls test simpler engineering explanations on the same 48 inspected training worlds. One transports nearby observed capabilities to new options without diagnostic conditioning. The other reserves four units for later construction before buying an option. Their specification precedes collection, but the comparisons are descriptive training evidence with ordinary unadjusted intervals. The 384 new-control runs and 1,920 old-method integrity repeats do not enlarge independent N. [E15]

| Training contrast | Budget 32 mean [95% interval] | Budget 64 mean [95% interval] |
| --- | --- | --- |
| Transport minus no diagnosis | +0.000268 [-0.002338, +0.003389] | +0.002896 [-0.001371, +0.008238] |
| Atlas minus transport | +0.006537 [-0.003641, +0.017473] | +0.014641 [+0.002309, +0.028183] |
| Affordability guard minus claim matching | +0.005648 [+0.001310, +0.011478] | 0.000000 [0.000000, 0.000000] |

Table 4. The controls test particular recipes; they do not exhaust all engineering alternatives or isolate every diagnostic mechanism. At budget 64 the guarded and ordinary claim matchers have exactly equal paired scores in all 96 seed conditions, nested in 48 worlds. [E15]

Transport alone does not reproduce the full atlas point gain. Atlas does exceed this particular transport control at budget 64. That positive comparison is narrower than establishing the separate value of correct labels, gap existence or optimistic priors. The affordability guard has a small positive budget-32 effect, but still trails Atlas there. Neither control explains away all atlas gains; neither establishes a unique diagnostic contribution. Intervals containing zero do not establish equivalence.

## 8. Final correction: the strongest simple comparator changed the decision

### 8.1 A policy-headroom screen, not a theorem

The final exploratory question is whether a policy given the correct pair of keys has enough advantage over existing non-oracle methods to warrant a new composition question. The screen uses 24 admitted key-pair worlds from the locked generator and two fixed optimizer seeds, with total budgets 32, 64 and 128. It charges hypothetical perfect revelation by running the existing key-oracle policy at budget B minus c, for c equal to four or eight. The operational primary quantity H4 is the paid-four oracle policy's score minus the best comparator's score.

The prewritten rule is proceed only if, at some budget, H4 has mean at least 0.04 and ordinary 95% lower limit above 0.02. Free and paid-eight reports cannot rescue a failure. The same 20,000 paired-world resamples reselect the best comparator within every resample. This respects comparator selection in the bootstrap, but does not make the three-budget exploratory screen a new confirmation. A separate Bonferroni sensitivity is reported without changing the rule. [E16-E18]

Two qualifications prevent an overclaim. First, the reference is an imperfect search policy, not the optimal policy given key knowledge, so its score is not a mathematical upper bound on all diagnosis. Second, reducing its budget charges information without supplying the additional performance observations a real probe would produce. The procedure is a hypothetical policy comparison, not an exact simulation of buying an actual diagnostic test.

### 8.2 Completing the comparator pool

The original screen compared six non-oracle arms and passed at 128 units. Its brief omitted `expand_all` and `random_expand`, although both were already available in the established library-selection experiment. A review prompted by unofficial inspected outcomes requested a retained correction. The omission was in the brief, not a failure to execute its stated schedule. The correction is explicitly post hoc; reproducing the unofficial numbers is not an independent fresh-world replication.

The correction runs the two missing arms unchanged at all three budgets on the same 24 worlds and seeds: 288 runs. Another 48 claim-matching reruns check harness parity. All 24 two-seed world means match the recorded values exactly, and regenerated world truth records are byte-identical. The six old comparator means and the paid/free reference means are reused; no new controller, world selection, margin or budget is introduced. Seven engineering repeats are excluded from efficacy inference. [E17,E19,E20]

| Total budget | Best full-pool comparator | Original H4 mean [95% interval] | Corrected H4 mean [95% interval] |
| --- | --- | --- | --- |
| 32 | Neutral prior | -0.007475 [-0.027006, +0.010953] | -0.007475 [-0.027006, +0.010953] |
| 64 | Guarded claim matching | +0.036998 [+0.015909, +0.057531] | +0.036998 [+0.015909, +0.057531] |
| 128 | Expand all | +0.052142 [+0.031653, +0.071163] | +0.035299 [+0.021985, +0.048655] |

Table 5. At budget 128 the original pool's best point mean was claim matching; the corrected pool's best is expand all. The same bootstrap indices and original estimator reproduce the old six-pool results exactly before adding the new arms. Intervals are ordinary approximate 95% intervals, not simultaneous coverage across budgets. [E16,E17]

![Figure 1. Original and corrected paid-key-oracle-policy headroom. The largest-budget mean drops below the 0.04 bar when the omitted competitors are added. The lower-limit requirement above 0.02 is a separate condition; neither condition alone suffices. These are the original retained intervals, not new analyses.](figures/headroom_correction.png)

At 128 units, expand all scores about 0.9233, versus 0.9064 for claim matching. The corrected H4 mean is +0.035299, below 0.04. Its ordinary interval still lies above zero and includes 0.04. Thus the result neither proves zero benefit nor statistically rules out a four-point population difference. It fails the specified continuation rule. The corrected decision is stop at every tested budget. The original proceed file remains unchanged; a new decision supersedes its interpretation. [E17,E18]

Adding comparators cannot make the same rule easier to pass when worlds and resamples are fixed: the maximum comparator mean cannot decrease in the observed sample or in any bootstrap sample. That algebraic monotonicity was checked for all retained draws. It explains the conservative direction of this correction, but does not erase the fact that the correction followed outcome inspection or restore confirmatory status.

### 8.3 Availability, construction and selection

![Figure 2. Expand-all deployment funnel on the 24 headroom worlds. Counts are seed conditions out of 48, not 48 independent worlds. A measured design can contain both keys without being selected into the final shortlist. The funnel is descriptive rather than a causal decomposition.](figures/deployment_funnel.png)

At budgets 32, 64 and 128, expand all buys both true keys in 38, 48 and 48 seed conditions; measures them together in 1, 25 and 48; and shortlists them together in 0, 14 and 43. Direct-build counts are retained separately because a charged probe can also measure a joint design. At the largest budget, a simple policy often acquires and uses the necessary pair without first identifying it selectively. [E17]

The pattern shows how the value of diagnosis depends on acquisition cost relative to the remaining build budget. Buying everything performs poorly at small budgets in these worlds and becomes a strong comparator at the largest one. This is not evidence that buy-all is always optimal. Nor does a final shortlist loss uniquely identify a construction defect: capability, cost, state, context, competition for four places and measurement history all affect selection. The learned lesson concerns the complete policy and benchmark economics.

## 9. What the program contributes, positively and negatively

The strongest positive contribution is a concrete experimental record that keeps evidence categories and costs separate. Exact finite checks, measured workload contrasts, prospective selection tests, controlled model comparisons and reproducible failures provide more usable knowledge than an unsupported claim of general discovery. The record also contains genuine favorable observations: restricted compilation benefits; a representation-dependent storage reversal; substantial high-coupling coverage improvement from learned scales; a modest grammar-expansion validation signal; and a positive comparison with one specific transport control. Their stated scopes matter as much as their signs.

The strongest negative contribution is the failure of increasingly demanding controller claims to earn continuation. The Phase 1 atlas loses to a strong decomposable comparator. The Phase 2 priority controller loses even when components interact. The Phase 3 revised recipe produces a limited positive signal but fails its development rule and does not robustly solve paired-key deployment. Subsequent controls leave diagnostic causation unresolved, and the final comparator correction removes the last passing operational headroom signal. These are different findings, not three interchangeable registered negative trials and not a pooled estimate of one universal effect.

The synthesis suggests five practical lessons. Start with the simplest strong baselines, including factorized assembly, generic value-per-cost, claim matching and buying everything when affordable. Test whether a diagnosis changes action value, not merely whether a tag or forecast is accurate. Check calibration by relevant regime rather than relying only on an aggregate. Follow a discovered component through paid acquisition, useful construction and final deployment. Preserve negative controls and resource failures, while allowing their results to stop the research line rather than creating pressure to redefine success.

Those lessons are interpretive consequences of this record and established experimental principles, not new universal theorems. Their distinctive evidence here is the combination of specified recipes, controlled worlds, retained traces and documented corrections. Publication-level novelty would require careful positioning against related work, and stronger claims of generality would require independent evidence beyond this program.

## 10. Implications for ASI Stack

The relevant contribution to a broader intelligence architecture is a conditional engineering lesson: a system's knowledge, internal representation, decision policy and ability to realize a useful design should be assessed separately. Storing a fact does not make every use of it cheap; recognizing a missing capability does not make a remedy available; buying a remedy does not ensure useful composition; and obtaining a capable design does not make further reasoning or communication free. The project supplies concrete small-scale examples of these separations.

An evidence-bearing atlas could be retained as an instrumentation and accounting component in a larger system. It can record which claims are measured, predicted, finitely excluded or unresolved, and which costs or information assumptions a proposed comparison omits. This is an architectural possibility supported by the implemented functions, not a demonstration that an ASI stack containing them outperforms an alternative system. The atlas should have a falsifiable interface and cost boundary rather than be treated as an inherently intelligent executive.

The tested diagnosis controllers should not be promoted into a demonstrated discovery module. This program provides no evidence of recursive self-improvement, superhuman research, autonomous theory formation, newly learned primitives, general alignment, or a universal intelligence-resource frontier. No result estimates the probability of ASI or validates a complete ASI Stack. It can serve as a methodological and empirical source for those broader discussions only when that distinction stays explicit.

Some broader questions remain open. Selective diagnosis could matter where acquiring all components is costly, measurements distinguish actionable hypotheses, and a sufficiently capable composition policy can exploit the resulting information. Primitive invention and representation learning are also distinct from selecting this supplied library. Those statements identify necessary motivations for a different application, not positive results of this study or a successor experimental plan. The completed controller line remains closed.

For book integration, the companion source guide separates citation-ready empirical statements, interpretations and untested propositions. It identifies the final corrected result as the current reading of the exploratory headroom screen. Earlier PDFs are historical sources for their own studies; they should not be cited in isolation as if their provisional continuation decision remained current.

## 11. Limitations and threats to validity

**Task and representation limits.** The finite grammars, supplied primitives, planted capability rules and synthetic interaction distributions strongly constrain the results. Phase 1's CPU experiment provides a different type of evidence from stipulated Phases 2-3. Full-grammar normalization and a four-design shortlist embody preferences; they are not a coordinate-free intelligence measure. A scalar breadth coordinate cannot preserve every preference over task capabilities.

**Policy and comparator limits.** The tested recipes are particular heuristics. A more informative predictor, a better lookahead policy, different proposals or a larger library could change outcomes. Phase 2 did include a local random-forest Bayesian-optimization comparator; the program did not establish faithful comparisons with modern quality-diversity optimizers, state-of-the-art Bayesian experiment selection over the key-pair hypotheses, or general program/library-learning systems. Weak or inactive controls cannot establish equivalence or eliminate all alternative explanations.

**Inference limits.** Two fixed search seeds per world constrain optimizer-seed generalization. Class analyses often have only eight worlds. Adaptive measurement selection matters for forecast evaluation. Ordinary intervals and exploratory contrasts are not simultaneous confidence guarantees. A positive point estimate does not establish practical value; an interval containing zero does not establish equivalence; failure of a point-margin gate does not establish a population effect below that margin. The final correction reused inspected worlds and is post hoc.

**Measurement and cost limits.** CPU timings come from one shared desktop with uncontrolled background load. Preparation, delivery and research overhead have different scopes. Unknown interrupted whole-process work remains unknown. Synthetic units do not equalize actual controller CPU and cannot support energy claims. Trusted typed workers and disabled connection APIs do not constitute a sandbox for hostile arbitrary code. The study's engineering does not certify general software correctness.

**Process limits.** Development, reviews and writing share project context. Cross-assistant review found substantive problems, but is not independent replication. Some protocols were imperfect: fixed routing overrode scores, an early shuffle left interaction tags untouched, aggregate coverage obscured failures, a cost-key setting was inactive, reporting omitted useful budget comparisons, and the last screen omitted an obvious available comparator. Later corrections improve interpretation without retroactively making those studies pristine. The strict Phase 3 development spending criterion and final-revision selection rule are also choices that affect the stop.

**Availability limits.** Private storage and restoration checks improve preservation but are not public reproducibility. The private GitHub snapshot deliberately omits bulk data, and two of its nine ledgers require excluded evidence for complete validation. The full backup preserves those data. The consolidated paper does not itself make the repository or raw archives public; public release, personal authorship and external submission remain owner decisions.

## 12. Conclusion

The answerability-atlas program succeeded in building a useful conditional measurement laboratory and in producing several bounded positive engineering observations. It did not establish the stronger proposition that its diagnosis mechanisms improve discovery relative to strong alternatives. The later studies narrowed rather than erased that distinction. More realistic interactions did not rescue priority routing; a revised prior-based controller produced a modest signal without passing development; controls left mechanism attribution open; and completing the final comparator pool changed proceed to stop.

The defensible conclusion is to preserve the measurement and evidence machinery, retain the scoped empirical knowledge, and retire the tested controller line. A broader theory of computational discovery or a larger intelligence architecture must earn its own evidence. This record can inform such work by making clear both what was learned and what was not demonstrated.

## Data, code and assistance statement

The accompanying `claim_evidence.json`, `references.bib`, citation audit and source guide bind this paper to retained project artifacts. `results/program_synthesis_v1/evidence.json` indexes 22 primary artifacts and the reviewed documentation and ledger corpus, with full SHA-256 hashes. Figure inputs are copies of existing results; no new confidence intervals or samples are introduced. Rebuild commands are in this synthesis directory's README. Historical scientific records are unchanged. The source snapshot is private; archival access, book-source availability and publication are separate owner choices. Implementation, reviews and writing were AI assisted as described in Section 2.3; no affiliation, external review or publication status is implied.

## References

[1] Stratos Idreos, Kostas Zoumpatianos, Brian Hentschel, Michael S. Kester and Demi Guo. 2018. The Data Calculator: Data Structure Design and Cost Synthesis from First Principles and Learned Cost Models. SIGMOD. DOI: [10.1145/3183713.3199671](https://doi.org/10.1145/3183713.3199671).

[2] Stratos Idreos et al. 2019. Design Continuums and the Path Toward Self-Designing Key-Value Stores that Know and Learn. CIDR. [Author publication and abstract](https://stratos.seas.harvard.edu/publications/design-continuums-and-path-toward-self-designing-key-value-stores-know-and).

[3] Jean-Baptiste Mouret and Jeff Clune. 2015. Illuminating search spaces by mapping elites. [arXiv:1504.04909](https://arxiv.org/abs/1504.04909).

[4] Thomas Pierrot, Guillaume Richard, Karim Beguir and Antoine Cully. 2022. Multi-Objective Quality Diversity Optimization. GECCO. DOI: [10.1145/3512290.3528823](https://doi.org/10.1145/3512290.3528823).

[5] Paul Kent, Adam Gaier, Jean-Baptiste Mouret and Juergen Branke. 2023. BOP-Elites, a Bayesian Optimisation Approach to Quality Diversity Search with Black-Box descriptor functions. [arXiv:2307.09326](https://arxiv.org/abs/2307.09326).

[6] Samuel Daulton, Maximilian Balandat and Eytan Bakshy. 2021. Parallel Bayesian Optimization of Multiple Noisy Objectives with Expected Hypervolume Improvement. NeurIPS 34. [arXiv:2105.08195](https://arxiv.org/abs/2105.08195).

[7] Stuart Russell and Eric Wefald. 1991. Principles of metareasoning. Artificial Intelligence 49(1-3):361-395. DOI: [10.1016/0004-3702(91)90015-C](https://doi.org/10.1016/0004-3702%2891%2990015-C).

[8] Kirthevasan Kandasamy, Jeff Schneider and Barnabas Poczos. 2015. High Dimensional Bayesian Optimisation and Bandits via Additive Models. ICML, PMLR 37:295-304. [Primary paper](https://proceedings.mlr.press/v37/kandasamy15.html).

[9] Jacob Gardner, Chuan Guo, Kilian Weinberger, Roman Garnett and Roger Grosse. 2017. Discovering and Exploiting Additive Structure for Bayesian Optimization. AISTATS, PMLR 54:1311-1319. [Primary paper](https://proceedings.mlr.press/v54/gardner17a.html).

[10] Frank Hutter, Holger Hoos and Kevin Leyton-Brown. 2014. An Efficient Approach for Assessing Hyperparameter Importance. ICML, PMLR 32(1):754-762. [Primary paper](https://proceedings.mlr.press/v32/hutter14.html).

[11] Kevin Ellis, Catherine Wong, Maxwell Nye, Mathias Sable-Meyer, Lucas Morales, Luke Hewitt, Luc Cary, Armando Solar-Lezama and Joshua B. Tenenbaum. 2021. DreamCoder: Bootstrapping Inductive Program Synthesis with Wake-Sleep Library Learning. PLDI. DOI: [10.1145/3453483.3454080](https://doi.org/10.1145/3453483.3454080).

[12] Nam Do Khanh, Nhat Nguyen Tran Minh, Dat Pham Vu Tuan, Long Doan and Binh Huynh Thi Thanh. 2026. QDEvo: A Multi-Objective Quality-Diversity Framework for Automated Heuristic Design. GECCO poster. [arXiv:2607.11916](https://arxiv.org/abs/2607.11916).

[13] James Bergstra and Yoshua Bengio. 2012. Random Search for Hyper-Parameter Optimization. JMLR 13(10):281-305. [Primary paper](https://www.jmlr.org/papers/v13/bergstra12a.html).

[14] Gavin C. Cawley and Nicola L. C. Talbot. 2010. On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. JMLR 11(70):2079-2107. [Primary paper](https://www.jmlr.org/papers/v11/cawley10a.html).

## Appendix A. Artifact references and historical reading order

The evidence IDs below identify project results rather than external publications. Full paths, hashes, selectors and claim boundaries are in the accompanying claim-to-evidence index. Paths are relative to the original full repository. Reading a historical manuscript alone can miss later corrections.

| Evidence ID | Retained result |
| --- | --- |
| E01-E03 | Finite reference, corrected batch pilot and corrected RPC pilot |
| E04-E06 | Phase 1 primary, separate family extension and exploratory arm contrasts |
| E07 | Frozen prospective maintenance comparison |
| E08-E10 | Phase 2 primary, separate higher-order study and review reanalysis |
| E11-E13 | Learned-prior check, Phase 3 validation and complete development report |
| E14-E15 | Complete budget addendum and training-only mechanism controls |
| E16 | Original six-comparator headroom screen; interpretation superseded |
| E17-E20 | Corrected eight-comparator analysis, decision, exact parity and integrity receipt |
| E21-E22 | Phase 3 planted-mechanism traces and retained-study inventory |

For Phase 3, read the original expansion manuscript together with its paper erratum and budget addendum. Read the mechanism appendix as training-only explanatory evidence. For headroom, the corrected decision E18 governs interpretation of the original E16 screen. The program-final status is historically authoritative for research closure; later packaging records document private hosting and backup rather than new scientific results.

## Appendix B. Estimator and operational decision

Let Y(w,m,B) be a world's shortlist score for method m at budget B, after averaging its two fixed optimizer-seed conditions. Let M be the stated comparator pool. For an information charge c, the point headroom is the mean over worlds of the paid-oracle score minus the score of the comparator with the largest observed world mean. In equivalent arithmetic notation:

`H_c(B) = mean_w Y(w,oracle,B-c) - max_(m in M) mean_w Y(w,m,B).`

For each bootstrap draw, sample world indices with replacement and use those same indices for all methods, budgets and information charges. Recompute the maximum comparator mean inside that draw. The ordinary interval uses the 0.025 and 0.975 quantiles of these resampled headrooms. The frozen procedure uses 20,000 draws and seed 2026102532. The prewritten three-budget Bonferroni sensitivity uses quantiles 0.025/3 and 1 - 0.025/3; it does not replace or rescue the primary rule. These are approximate percentile intervals conditional on the generator and fixed seed conditions, not finite-sample guarantees.

The final operational rule is the conjunction of observed H4 mean at least 0.04 and its ordinary 95% lower limit strictly greater than 0.02 at one or more of the stated budgets. It is not a test that the lower limit exceeds 0.04. Conversely, a mean below 0.04 fails the rule even if the lower limit exceeds 0.02. Neither an unpaid-oracle result nor H8 can change that decision. The implementation evaluates paired differences for the selected point comparator; the expression above is its mathematical equivalent, not a demand for bit-identical alternate floating-point evaluation.

For a larger pool M' containing M, the maximum comparator mean is no smaller in the original sample and every fixed resample. Consequently, headroom is no larger draw by draw, and its empirical quantiles cannot increase. This establishes only the direction of the comparator correction for these fixed data and rules. It does not provide valid inference after arbitrary investigator choices, an optimum over all possible comparator policies, or proof that no real diagnostic policy can exceed the reference. [E16-E19]
