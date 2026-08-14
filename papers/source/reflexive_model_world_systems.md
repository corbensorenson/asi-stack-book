# Reflexive Model-World Systems

## When Representations Become Causes

### A causal theory of learning systems that generate part of their own future evidence

**Corben Sorenson**  
Independent Researcher  
Preprint, August 2026

---

## Abstract

Machine-learning systems are usually analyzed as if they learn from an externally generated world: observations inform a model, the model is evaluated against later observations, and retraining incorporates the resulting data. In many consequential deployments, however, the model is not external to the process that generates its future evidence. Scores change behavior; alarms trigger interventions; rankings reorganize institutions; recommenders alter exposure and preferences; classifications reshape categories; and model outputs enter the corpora used to train successor models. The resulting object is not a model acting on a fixed world, but an evolving model-world loop.

This paper proposes **Reflexive Model-World Systems** (RMWS) as a causal framework for such settings. A governed model lineage is *reflexively closed* over a horizon when one of its deployments causally changes evidence that is later used to update a successor in that lineage. The framework contributes: (1) a lineage-relative definition of reflexive closure; (2) an eight-channel causal audit signature covering state, outcome, exposure, measurement, preference, ontology, institution, and model-ecology effects; (3) the distinction between **model-descended evidence** and lineage-independent evidence, which cuts across the usual human-versus-synthetic divide; (4) a **grounding reserve** defined by informative evidence channels that are approximately invariant to admissible lineage interventions; (5) formal results on joint-state sufficiency, local stability, counterfactual-label mismatch, diversity contraction, observational non-identifiability, and institutional hysteresis; and (6) an evaluation framework separating baseline fidelity, on-policy prediction, causal steering, and legitimacy.

Three illustrative simulations demonstrate the framework. A common attractiveness score contracts diversity when agents optimize against it, while plural models and exploration preserve multiple attractors. A successful risk alarm causes naive retraining to underestimate the no-intervention risk it was meant to predict. A recursive categorical model shows that drift tracks causal ancestry better than whether records are labeled synthetic: independently generated synthetic evidence remains stable, while human-origin but model-selected evidence rapidly loses tail support. These experiments are mechanistic demonstrations, not empirical claims about particular populations.

The paper concludes with a Reflexive System Audit and a trajectory-level implication for advanced AI: a sufficiently influential learner cannot correctly model its future while treating itself as external to the process that generates that future. The object that must be understood and aligned is therefore the evolving model-world loop, not the frozen model in isolation.

**Keywords:** performative prediction; feedback loops; causal inference; world models; human-AI coevolution; model collapse; Goodhart's law; alignment; reflexivity; data provenance

---

## 1. Introduction

A conventional learning diagram has one dominant direction:

\[
W_t \longrightarrow O_t \longrightarrow M_t,
\]

where a world state \(W_t\) generates observations \(O_t\), and those observations update a model \(M_t\). The model is evaluated by asking whether it accurately represents or predicts a world presumed to exist independently of the act of modeling.

Consequential deployment adds another arrow:

\[
M_t \longrightarrow D_t \longrightarrow W_{t+1},
\]

where \(D_t\) is a prediction, score, ranking, recommendation, decision, or policy produced from the model. Once the changed world generates the observations used to train a successor model, the arrows close:

\[
W_t \rightarrow O_t \rightarrow M_t \rightarrow D_t
\rightarrow W_{t+1} \rightarrow O_{t+1} \rightarrow M_{t+1}.
\]

The model is now both an inference from the world and one of the causes of the world from which it later learns.

This structure is visible across domains. A credit model changes who receives credit and therefore which defaults are observed. A medical alarm triggers treatment and can prevent the event it predicted. A university ranking changes admissions, budgeting, reporting, and institutional strategy. A recommender changes what people encounter and may change what they later prefer. A classifier gives social salience to categories that people and institutions then inhabit differently. A generative model produces text that enters the training corpus of its successors. In each case, future evidence cannot be treated as a neutral sample from the world that existed before deployment.

The underlying insight is not new. Cybernetics studied reciprocal regulation; the Lucas critique warned that policy changes alter the behavioral relations used for prediction; Goodhart-type effects concern proxies that become targets; social scientists have studied reactive measurement and looping classifications; niche-construction theory studies organisms that alter selective environments; and performative prediction now provides a substantial mathematical literature on model-dependent distributions (Conant and Ashby, 1970; Lucas, 1976; Hacking, 1995; Espeland and Sauder, 2007; Manheim and Garrabrant, 2019; Perdomo et al., 2020).

The remaining problem is not to announce that feedback exists. It is to identify a scientifically useful boundary and then reason about the resulting systems without collapsing distinct mechanisms into an undifferentiated phrase such as “distribution shift.” A feature changes because a person strategically adapts. An outcome changes because a treatment works. A label changes because the measurement process changes. A preference changes because exposure changes taste. A category changes because an institution reorganizes what counts. These may all alter a dataset, but they do not define the same causal estimand, require the same experiment, or justify the same intervention.

This paper proposes **Reflexive Model-World Systems** as a unifying but deliberately bounded framework. The central definition is:

> **A governed model lineage is reflexively closed over a horizon when one of its deployments causally changes evidence that is later used to update a successor in that lineage.**

The emphasis on *causally*, *evidence*, *successor*, and *lineage* is essential. Ordinary correlation is insufficient. A fixed controller that never learns is not, by this definition, a reflexive learning lineage. A learner that passively observes an unaffected process is not reflexively closed. A model need not literally ingest the exact record it caused; it is enough that its deployment changes a mechanism that determines the successor's evidence.

### 1.1 Contributions

The paper makes seven primary contributions.

1. **Reflexive closure over model lineages.** It defines the relevant unit as a governed succession of models rather than a single parameter vector, and gives an intervention-based closure criterion.

2. **A causal audit signature.** It decomposes model-to-world effects into eight channels: state or feature, outcome or label, exposure or sampling, measurement, preference or utility, ontology, institution, and model ecology. This signature extends existing feedback-loop classifications rather than claiming to replace them.

3. **Model-descended evidence.** It distinguishes evidence according to whether its generating process was causally influenced by a model lineage. The distinction cuts across content provenance: human-origin evidence can be model-descended, while synthetic evidence can be lineage-independent.

4. **Grounding reserves and reflexive debt.** It defines lineage- and horizon-relative anchor channels and describes the causal information debt created when deployments reshape the world without preserving the variation needed to recover counterfactual baselines.

5. **Formal results.** It establishes or sketches results on augmented-state necessity, local loop stability, counterfactual-label mismatch, contraction under a common target, non-identifiability from a single deployment history, and persistence after model withdrawal.

6. **Evaluation and audit.** It separates prediction of the no-deployment world, prediction under deployment, causal steering utility, and legitimacy, then turns the theory into a ten-step Reflexive System Audit.

7. **Trajectory-level AI implication.** It argues that advanced systems with material influence require self-inclusive world models and must be evaluated over the model-world trajectories they induce, including their effects on evidence, preferences, institutions, and successor systems.

### 1.2 Claim discipline

The framework is meant to synthesize and extend adjacent work, not erase it. Three forms of restraint are important.

First, RMWS is **not a theory of all feedback**. Thermostats, homeostatic processes, and ordinary closed-loop controllers are part of the broader cybernetic family, but they become reflexive *learning* systems here only when deployment changes evidence used by a successor model lineage.

Second, RMWS is **not performative prediction under a new name**. The performative-prediction formalism can represent broad model-dependent distributions and is the closest mathematical foundation for this paper. RMWS adds lineage-relative causal provenance, typed mechanisms, changing semantics and institutions, cross-lineage evidence externalities, and an operational audit. These additions are useful only if they support different estimands, tests, and controls; otherwise the framework would be terminological duplication.

Third, reflexivity does **not imply collapse**. Feedback can stabilize, improve, oscillate, polarize, homogenize, or diverge. Recent theory shows that suitable regularization can make even a weak model-independent signal govern retraining in analyzed settings despite arbitrarily strong model-induced effects (Hardt, 2026). Research on recursive synthetic data likewise finds collapse under replacement regimes but not inevitability when original data accumulate (Shumailov et al., 2024; Gerstgrasser et al., 2024). RMWS therefore develops a regime theory rather than a universal failure narrative.

---

## 2. From Reflection to Reflexive Closure

### 2.1 A strict functional definition of a model

The word *model* can become vacuous if every physical trace is treated as a representation. A footprint contains information about a foot; an eroded rock contains information about weather. Neither is necessarily a model in the sense required here.

Let \(W\) be a target system and \(\mathcal Q\) a family of task-relevant queries. A structure \(M\) is a **functional model of \(W\) relative to \(\mathcal Q\)** when it satisfies three conditions:

1. **Information-bearing:** its state was learned, constructed, or maintained so that it preserves information about \(W\).
2. **Query adequacy:** its state supports at least one nontrivial predictive, diagnostic, counterfactual, or control-relevant query in \(\mathcal Q\).
3. **Operational use:** a containing process uses \(M\) to generate a prediction, classification, recommendation, decision, or control action concerning \(W\).

This definition is functional rather than semantic in a strong philosophical sense. It permits implicit models encoded in policies or neural states, provided that the relevant predictive or control information is recoverable and used. It excludes mere covariance without operational role.

### 2.2 Model lineage

A deployed system is rarely a single immutable object. It is retrained, fine-tuned, distilled, replaced, routed, or reconstituted. The proper unit is therefore a **model lineage**:

\[
\mathcal L = \{M_0,M_1,M_2,\ldots\},
\]

whose members are related by an explicitly governed continuation rule. Lineage membership may be established through:

- parameter inheritance or fine-tuning;
- retraining under the same operational objective;
- distillation from a predecessor;
- replacement in the same decision role under a versioned governance process;
- or another documented causal succession rule.

Lineage is not merely weight similarity. A completely different architecture may be the successor of an earlier system if it inherits the earlier system's role, data, objective, or deployment consequences. Conversely, two identical model copies used by independent institutions need not belong to the same governed lineage.

### 2.3 The minimum dynamic system

Let:

- \(W_t\) denote the target-world state;
- \(K_t\) denote the surrounding regime, including preferences, measurement rules, categories, institutions, and infrastructure;
- \(M_t\) denote the current model state;
- \(C_t\) denote deployment context;
- \(D_t\) denote the deployed output, action, score, ranking, or policy;
- \(O_t\) denote evidence available for model updating;
- \(\xi_t\) and \(\nu_t\) denote external process and observation disturbances.

A minimal RMWS is:

\[
D_t = G(M_t,C_t),
\tag{1}
\]

\[
(W_{t+1},K_{t+1}) = F(W_t,K_t,D_t,\xi_t),
\tag{2}
\]

\[
O_{t+1} = H(W_{t+1},K_{t+1},D_t,\nu_t),
\tag{3}
\]

\[
M_{t+1} = L(M_t,O_{t+1}).
\tag{4}
\]

Equation (2) is the performative edge: deployment enters the transition law of the world or regime. Equation (4) is the epistemic edge: evidence updates the model. Equation (3) matters because deployment can change not only the underlying world but also which parts are observed and how they are measured.

![Figure 1. Reflexive closure in a model lineage.](figures/figure_1_reflexive_closure.png)

**Figure 1.** Reflexive closure occurs when deployment changes a future evidence channel that enters a successor model in the same governed lineage.

### 2.4 Definition of reflexive closure

Let \(\mathbf D^{\mathcal L}_{t:t+h-1}\) denote the sequence of admissible deployments by lineage \(\mathcal L\) over horizon \(h\). The lineage is **reflexively closed with respect to evidence channel \(O^j\) over horizon \(h\)** if:

1. \(O^j_{t+h}\) is used, directly or through a derived dataset, in updating a successor \(M_{t+h+1}\in\mathcal L\); and
2. there exist admissible deployment sequences \(\mathbf d\) and \(\mathbf d'\) such that

\[
P\!\left(O^j_{t+h}\mid do(\mathbf D^{\mathcal L}=\mathbf d)\right)
\neq
P\!\left(O^j_{t+h}\mid do(\mathbf D^{\mathcal L}=\mathbf d')\right).
\tag{5}
\]

Equation (5) is an intervention statement. A deployment merely correlated with later evidence does not establish reflexive closure. The closure is indexed by a channel and horizon because influence can be immediate, delayed, or absent for some evidence sources.

### 2.5 Degrees of reflexivity

Reflexivity is not binary at the system level. A lineage can influence one channel strongly and another negligibly; it can be reflexive over a short horizon but effectively exogenous over a longer institutional horizon, or the reverse. A useful coarse hierarchy is:

| Level | Structure | Example |
|---|---|---|
| 0. Static representation | No continuing update; negligible model-to-world effect | Archived map |
| 1. Passive learner | World updates model; deployment does not materially alter evidence | Remote astronomical classifier |
| 2. Fixed regulator | Model or controller changes world; no successor learning loop | Fixed thermostat |
| 3. Reflexive learner | Deployment changes evidence used in retraining | Credit, recommender, medical alarm |
| 4. Self-inclusive reflexive agent | The model represents its own influence and update loop | Planning agent modeling reactions to itself |
| 5. Reflexive model ecology | Multiple lineages jointly alter a shared evidence environment | Competing platforms and web-trained models |

The hierarchy prevents ordinary feedback from being relabeled reflexivity while preserving the structural relationships among the cases.

---

## 3. Intellectual Context and Novelty Boundary

### 3.1 Cybernetics, regulation, and internal models

Cybernetics began from reciprocal causation: actions alter a system, sensed consequences alter future actions, and regulation is understood through the closed loop. Conant and Ashby's good-regulator theorem argued, under a restricted information-theoretic setup, that a maximally successful and simple regulator must stand in a model-like mapping to the regulated system (Conant and Ashby, 1970). Control theory's internal-model principle formalized related requirements for robust regulation against particular classes of disturbances (Francis and Wonham, 1976).

These results motivate but do not prove the claims of this paper. The original good-regulator theorem uses a narrower notion of model than a full predictive simulator, and later work has cautioned against treating its slogan as a universal theorem for embodied or learned agents (Virgo et al., 2025). More recent theory shows, under explicit assumptions, that agents generalizing over sufficiently diverse multi-step goals must encode an extractable predictive model of their environment (Richens et al., 2025). RMWS asks a further question: when the agent changes the environment's transition law and its own future observations, what must the modeled state contain?

The proposed answer is that the sufficient state may need to include the agent's own model, deployment policy, evidence pipeline, and institutional regime. Modeling only an external world can be structurally incomplete when the model is one of the world's transition causes.

### 3.2 Economics and social reflexivity

The Lucas critique established a closely related lesson in economic policy: behavioral relations estimated under one policy regime need not remain stable after the policy changes, because agents adapt their decision rules (Lucas, 1976). Goodhart-type effects likewise arise when optimization changes the relationship between a proxy and its target. Manheim and Garrabrant's taxonomy distinguishes regressional, extremal, causal, and adversarial variants, underscoring that “the metric became a target” is not a single mechanism (Manheim and Garrabrant, 2019).

Sociological work adds mechanisms that standard predictive models often omit. Espeland and Sauder's study of law-school rankings showed that public measures are reactive: organizations reorganize admissions, resource allocation, reporting, and strategy around the ranking system (Espeland and Sauder, 2007). Hacking's looping effects describe classifications that alter the people classified, leading both the population and the category to change (Hacking, 1995). These are not merely feature shifts. They can alter institutions, identities, and the ontology through which evidence is generated.

RMWS incorporates these contributions by including \(K_t\), the regime of measurement, preference, category, and institution, as part of the dynamic state rather than treating all change as movement over a fixed feature-label space.

### 3.3 Performative prediction

Performative prediction is the closest formal foundation. Perdomo et al. define a distribution map \(\mathcal D(\theta)\) in which deploying model parameters \(\theta\) changes the data distribution on which the model is subsequently evaluated (Perdomo et al., 2020). This creates a distinction between **performative stability**, where a model is optimal for the distribution it induces, and **performative optimality**, where the model minimizes risk while accounting for its effect on the induced distribution. Subsequent work has developed stochastic optimization, state-dependent dynamics, regret minimization, causal identification, multi-player games, and empirical measures of performative power.

The field has become broad enough that a 2026 ACM Computing Surveys article systematizes solution concepts, information assumptions, and implementations of the distribution map (Kehrenberg et al., 2026). A socio-technical synthesis from the same year organizes mechanisms, risks, and intervention levels (Fybish and Susnjak, 2026). Partially performative prediction explicitly combines endogenous model-induced shift with exogenous environmental drift (Lee and Zrnic, 2026). Multi-player performative prediction models competing decision-makers whose choices jointly alter responsive populations (Narang et al., 2023). Work on performative power gives a causal measure of how strongly a platform can steer participants and connects that power to concentration, personalization, competition, and outside options (Hardt et al., 2022). Randomized experiments on online search demonstrate that ranking changes can causally redirect traffic, turning “engine rather than camera” into a measurable property (Mendler-Dünner et al., 2024).

RMWS should therefore not be read as discovering that deployment can change data. Its proposed addition is a causal *decomposition and governance layer* around that mathematical core. A general distribution map can absorb all downstream changes, but it does not by itself tell an auditor whether the model changed a person's features, prevented an outcome, changed who was sampled, changed the measuring instrument, reshaped preferences, narrowed the category, reorganized an institution, or contaminated another model's evidence. Those mechanisms imply different counterfactuals and controls.

### 3.4 Feedback-loop taxonomies and human-AI coevolution

Existing work has already classified feedback loops in automated decision systems. Pagan et al. use dynamical-systems language to distinguish sampling, individual, feature, outcome, model, and adversarial loops and show that feedback can amplify, preserve, or reduce bias (Pagan et al., 2023). RMWS's eight-channel signature extends this practical lineage; it is not offered as the first feedback taxonomy.

Human-AI systems also provide direct evidence that preferences and judgments can participate in the loop. Pedreschi et al. describe a coevolutionary cycle in which human choices generate training data and AI outputs shape subsequent choices and preferences (Pedreschi et al., 2023). In a series of experiments involving 1,401 participants, Glickman and Sharot found that biased AI feedback could amplify later human perceptual, emotional, and social judgments, while accurate AI could improve judgments (Glickman and Sharot, 2025). The result is important precisely because it demonstrates multiple regimes: AI-mediated feedback is not inherently degrading, but it can become an amplifier of whatever signal it returns.

Recent predictive-loop models similarly show that platforms adapting predictions while users update opinions can drive consensus under sufficiently strong susceptibility (Wu et al., 2026). These findings motivate explicit preference and exposure channels rather than treating human labels as stationary ground truth.

### 3.5 Recursive training and model-data feedback

Generative-model recursion provides an unusually clean artificial case. Shumailov et al. show that repeated training on recursively generated data under replacement regimes can produce model collapse, with tails disappearing before broader degradation (Shumailov et al., 2024). Gerstgrasser et al. show that collapse is not inevitable in their studied settings when original data are retained and successive data accumulate (Gerstgrasser et al., 2024). Hardt's stable-signal principle goes further in analyzed affine retraining systems: a nonzero model-independent signal, combined with suitable regularization, can govern retraining even when model-induced effects are arbitrarily stronger (Hardt, 2026).

These results motivate a more precise variable than “synthetic fraction.” What matters is whether evidence is causally descended from the model lineage, what independent signal remains, how data are accumulated, and how updates regularize the loop.

### 3.6 Relation to niche construction

Niche-construction theory studies organisms that alter the selective environments acting on themselves and their descendants (Odling-Smee et al., 2003). The structural pattern is reciprocal:

\[
Environment_t \rightarrow Organism_t \rightarrow Environment_{t+1}.
\]

The analogy is valuable, but the paper does not claim that every organism literally contains a semantic model. Niche construction belongs to a broader class of adaptive reciprocal systems. RMWS is narrower: it requires an information-bearing structure used for prediction, classification, decision, or control, plus a successor learning loop through altered evidence.

### 3.7 Proposed novelty boundary

The literature already contains feedback, performativity, reactive measurement, coevolution, model collapse, and multi-player learning. The proposed contribution is the combination of:

- a strict lineage-relative closure criterion;
- typed causal channels extending from feature response to ontology, institution, and model ecology;
- model-descended evidence as a causal provenance concept;
- query-relative grounding reserves;
- reflexive debt and rollback hysteresis;
- cross-lineage evidence externalities;
- and a trajectory-level alignment formulation.

To the author's knowledge, no dominant framework currently combines these components in this form. This is a bounded literature-search claim, not a claim that no earlier author has expressed any subset of the ideas.

---

## 4. The Reflexive Causal Audit Signature

A black-box statement that “the distribution changed” is insufficient for causal diagnosis. Define the horizon-specific **Reflexive Causal Audit Signature** of lineage \(\mathcal L\) as:

\[
\mathcal R_H(\mathcal L)=
(\Pi_X,\Pi_Y,\Pi_S,\Pi_Q,\Pi_U,\Pi_\Omega,\Pi_I,\Pi_E)_H,
\tag{6}
\]

where each \(\Pi_j\) is an interventionally defined effect on a distinct mechanism. The signature is a vector, not a scalar. Direction, delay, population, and distributional incidence matter.

| Channel | Deployment changes | Example | Characteristic risk |
|---|---|---|---|
| \(X\): state or feature | Attributes or behavior of represented entities | Applicants modify behavior for a classifier | Gaming, burden, homogenization |
| \(Y\): outcome or label | The event being predicted | Treatment prevents a predicted adverse event | Self-negation, corrupted labels |
| \(S\): exposure or sampling | What people or models encounter | Ranking changes consumption and later data | Selection bias, concentration |
| \(Q\): measurement | Sensors, labels, missingness, scrutiny | High-risk cases receive different tests | Selective labels, measurement drift |
| \(U\): preference or utility | What people value or use as labels | Exposure changes aesthetic judgment | Preference capture, target endogeneity |
| \(\Omega\): ontology | Categories, feature spaces, recognized distinctions | A score changes what “merit” means | Construct narrowing, moving target |
| \(I\): institution | Rules, resource allocation, infrastructure, norms | Rankings reorganize admissions and budgets | Lock-in, power concentration |
| \(E\): model ecology | Future datasets, evaluators, and other models | Generated content trains successor models | Contamination, synchronization, collapse |

### 4.1 State or feature response \(\Pi_X\)

This is the most familiar strategic-response channel. Let \(X_i(d)\) be the feature state of individual \(i\) under deployment \(d\). A population-level effect may be defined as:

\[
\Pi_X(d,d') =
\mathfrak d\left(P(X\mid do(D=d)),P(X\mid do(D=d'))\right),
\tag{7}
\]

where \(\mathfrak d\) is a distributional distance chosen for the application. The effect can be beneficial, such as skill acquisition induced by a transparent standard, or harmful, such as costly cosmetic conformity or gaming that severs a proxy from its target.

Feature response should be disaggregated by adaptation cost and access. A classifier can appear to “improve” a population while imposing unequal burdens on those who must change themselves to remain legible to it.

### 4.2 Outcome or label response \(\Pi_Y\)

Here deployment changes the event being predicted. Let \(Y(d)\) denote the potential outcome under deployment \(d\). Then:

\[
\Pi_Y(d,d') = E[Y(d)-Y(d')].
\tag{8}
\]

This channel is central in decision support. A high-risk prediction may trigger treatment, inspection, maintenance, or assistance. The observed label is then not the baseline event the model intended to estimate. The same mechanism can be self-fulfilling, as when a denial contributes to later default, or self-negating, as when an alarm prevents failure.

### 4.3 Exposure or sampling response \(\Pi_S\)

Models often control visibility before they control behavior. Let \(S_i(d)\) denote whether item, person, or event \(i\) enters an observer's exposure set or a future dataset. Ranking and recommendation change:

- which options humans consider;
- which records receive clicks, labels, or follow-up;
- which content becomes culturally salient;
- and which observations are available for retraining.

A model can therefore create evidence for its own preferences through selective exposure even if underlying states remain unchanged.

### 4.4 Measurement response \(\Pi_Q\)

The measurement function itself may depend on deployment:

\[
O = Q_D(W,\nu).
\tag{9}
\]

Examples include differential diagnostic testing, intensified policing, selective inspections, missing labels for rejected applicants, or annotators who see model suggestions before labeling. Measurement response is distinct from world-state response: the world may be unchanged while the evidence pipeline changes.

### 4.5 Preference or utility response \(\Pi_U\)

Let \(U_i(d)\) represent an individual's preference or utility state after exposure to deployment \(d\). Recommenders, scores, rankings, and generated content can change what people later prefer, which then changes labels, choices, and demand. The target is no longer stationary because the model helps generate the target function.

Preference change is normatively difficult. It is not enough to ask whether users clicked more after adaptation. The evaluation must distinguish informed preference formation, benign discovery, habituation, manipulation, dependency, and coercive narrowing of alternatives.

### 4.6 Ontology response \(\Pi_\Omega\)

Many systems assume a fixed state space \(\mathcal X\), label space \(\mathcal Y\), and construct definition. Reflexive systems can alter these spaces. Let \(\Omega_t\) specify the available categories, features, and semantic relations. Then:

\[
\Omega_{t+1}=F_\Omega(\Omega_t,D_t,W_t,I_t).
\tag{10}
\]

A hiring model may narrow “readiness” toward what its data pipeline can measure. A diagnostic category may change behavior, treatment, and self-understanding. An attractiveness score may help redefine attractiveness as what the scoring system rewards. Ontology response differs from ordinary concept drift because the representation participates causally in changing the concept.

### 4.7 Institutional response \(\Pi_I\)

Institutions preserve and amplify model effects through rules, budgets, infrastructure, and professional routines. Let:

\[
I_{t+1}=F_I(I_t,D_t,W_t).
\tag{11}
\]

A model can move along a continuum:

\[
measurement \rightarrow recommendation \rightarrow incentive
\rightarrow norm \rightarrow institution.
\]

Once embedded, the model's outputs may acquire legal, financial, or social force. Institutional state can also persist after model withdrawal, creating hysteresis.

### 4.8 Model-ecology response \(\Pi_E\)

Deployment can change the evidence and behavior of other models. Generated text enters public corpora; one platform changes user behavior observed by another; one risk score changes applicant populations faced by competing institutions. For lineages \(\mathcal L_i\) and \(\mathcal L_j\), define a cross-lineage effect:

\[
\Gamma_{ij}^{(H)}=
\sup_{\mathbf d_i,\mathbf d_i'}
\mathfrak d\left[
P(O^j_{t+H}\mid do(\mathbf D^i=\mathbf d_i)),
P(O^j_{t+H}\mid do(\mathbf D^i=\mathbf d_i'))
\right].
\tag{12}
\]

The diagonal \(\Gamma_{ii}\) measures self-reflexive influence. Off-diagonal terms measure evidence externalities. The matrix \(\Gamma\) turns a set of deployed models into an ecology rather than a collection of independent predictors.

### 4.9 Why the vector should not be collapsed prematurely

A single “reflexivity score” would be attractive for dashboards but dangerous as a primary scientific object. Two systems could have the same scalar magnitude while one prevents deaths and the other manipulates preferences. Even within a channel, positive and negative effects can cancel in an average. The full signature should therefore preserve:

- channel identity;
- affected population;
- direction and distribution of effect;
- response delay;
- persistence;
- uncertainty and identification assumptions;
- and whether the effect is intended, incidental, or adversarial.

Scalar summaries may be derived for a specific governance decision, but they should remain functions of the typed signature rather than substitutes for it.

---

## 5. Model-Descended Evidence

### 5.1 Why human versus synthetic is the wrong primary distinction

Contemporary provenance discussions often divide data into *real* or *human-generated* records and *synthetic* or *model-generated* records. That distinction is useful for authorship, authenticity, and some statistical questions, but it does not identify reflexive endogeneity.

Consider two cases.

1. A person changes their résumé, face, writing style, or behavior to satisfy a deployed model. The resulting record is produced by a human, but its generating process was causally influenced by the model.
2. An independently specified physical simulator produces a synthetic observation. If the deployed lineage did not influence the simulator, the observation may be more independent of that lineage than the human-origin record.

The relevant distinction for reflexive learning is therefore:

\[
\boxed{\text{model-descended evidence}}
\quad\text{versus}\quad
\boxed{\text{lineage-independent evidence}}.
\]

This is not a moral ranking. Model-descended evidence can be useful, accurate, and desirable. The point is that it answers a different causal question from evidence generated independently of the lineage.

### 5.2 Causal descendancy

For evidence channel \(O^j\), lineage \(\mathcal L\), admissible deployment class \(\mathcal A\), and horizon \(H\), define the **causal descendancy score**:

\[
r_H(O^j;\mathcal L,\mathcal A)
=
\sup_{\mathbf d,\mathbf d'\in\mathcal A}
\mathfrak d\left[
P(O^j_{t:t+H}\mid do(\mathbf D^{\mathcal L}=\mathbf d)),
P(O^j_{t:t+H}\mid do(\mathbf D^{\mathcal L}=\mathbf d'))
\right].
\tag{13}
\]

The divergence \(\mathfrak d\) may be total variation, Wasserstein distance, an average treatment effect, a kernel discrepancy, or a domain-specific effect measure. Interpretation:

- \(r_H=0\): the evidence channel is invariant to admissible lineage deployments over the chosen horizon;
- small \(r_H\): weak lineage influence;
- large \(r_H\): the lineage materially shapes its future evidence.

The quantity resembles performative power, but the target is specifically the future evidence substrate used by model lineages, potentially through all eight channels. Performative power concerns a platform's causal ability to change a population; evidence descendancy asks how much a lineage changes the observations from which itself or another lineage subsequently learns.

### 5.3 Evidence ancestry as a graph

Binary labels will often be inadequate. A record can descend from a model through multiple paths:

- direct generation by the model;
- human adaptation to a score;
- institutional policy triggered by a prediction;
- recommendation-mediated exposure;
- curation by another model;
- or a chain of successor models.

Represent evidence ancestry as a directed acyclic graph when possible, or a temporal causal graph when cycles occur. Each record or aggregate channel should preserve metadata such as:

```text
origin_type
source_process
lineage_exposure
model_versions
intervention_channels
exposure_horizon
estimated_effect
identification_method
uncertainty
```

This schema extends ordinary data lineage. Ordinary lineage records where data moved and which transformation produced it. **Causal lineage** additionally records which deployed systems materially influenced why the data existed, who was observed, what was measured, and which values were produced.

### 5.4 Descendancy is query-relative

A channel can be descended for one query but effectively independent for another. A recommender may strongly affect which songs are played while having negligible effect on the acoustic frequency of a recorded note. A medical alarm may affect mortality but not a patient's genotype. Evidence provenance should therefore be indexed to the target query \(q\in\mathcal Q\), not treated as a universal property of a record.

### 5.5 Descendancy and contamination are not identical

Model-descended evidence is not automatically contaminated. If the target query is “What happens under this deployed policy?”, on-policy descended evidence may be exactly what is needed. The problem arises when descended evidence is treated as if it identified a different counterfactual, such as the no-deployment world, an alternative policy, or an independently evolving culture.

The key failure is **provenance-target mismatch**:

\[
\text{training evidence identifies } P(O\mid do(D=d))
\quad\text{but the model is interpreted as identifying }P(O\mid do(D=d')).
\tag{14}
\]

A rigorous system must state which intervention regime its evidence identifies.

---

## 6. Grounding Reserves and Reflexive Debt

### 6.1 Grounding without metaphysical externality

It is tempting to speak of “external reality” as an absolute source outside the loop. In practice, no measurement is fully outside all causal influence. The useful concept is relative invariance: a channel can be approximately unaffected by a specified model lineage, over a specified horizon, for a specified query.

Let \(G\) be an evidence channel and \(q\) a target query. \(G\) is an **\((\epsilon,\gamma)\)-anchor** for lineage \(\mathcal L\), deployment class \(\mathcal A\), horizon \(H\), and query \(q\) when:

\[
\sup_{\mathbf d,\mathbf d'\in\mathcal A}
\mathfrak d\left[
P(G\mid do(\mathbf D^{\mathcal L}=\mathbf d)),
P(G\mid do(\mathbf D^{\mathcal L}=\mathbf d'))
\right]
\leq \epsilon,
\tag{15}
\]

and:

\[
\operatorname{Info}(G;q)\geq\gamma.
\tag{16}
\]

The first condition requires approximate intervention invariance. The second prevents a useless constant channel from qualifying as grounded.

A **grounding reserve** is a protected portfolio of anchor channels whose joint information remains sufficient for specified counterfactual and monitoring tasks.

### 6.2 Candidate anchor channels

Depending on the application, a grounding reserve may include:

- archived pre-deployment data;
- randomized sentinel populations;
- shadow-policy or holdout deployments;
- sensors insulated from the active policy;
- independent institutions with different incentives;
- accumulated original data preserved alongside synthetic data;
- independently specified simulators;
- delayed outcomes not visible to the acting model;
- or observations generated under deliberately varied policies.

No candidate is automatically safe. Archives can become stale, sentinel groups can be indirectly exposed, institutions can synchronize, and simulators can encode the same model assumptions. Anchor status must be tested and versioned.

### 6.3 Stable signals and regularization

A grounding reserve is not simply a requirement that most data be independent. Recent stable-signal theory shows why quantity alone is insufficient. In analyzed affine retraining systems, a nonzero model-independent component can determine the direction of regularized repeated retraining even when model-induced effects are arbitrarily larger (Hardt, 2026). Conversely, a large volume of nominally original data may provide little grounding if it contains no information about the query of interest or if its support excludes important tails.

The relevant variables include:

- the geometry of the stable signal;
- its identifiability;
- the update operator;
- regularization strength;
- data accumulation versus replacement;
- and support preservation.

This is why RMWS uses an information-and-invariance definition rather than a simple “grounding fraction.”

### 6.4 Reflexive debt

A system accumulates **reflexive debt** when it changes the world without preserving enough causal information to estimate relevant counterfactuals later. Suppose the organization wishes to recover the baseline distribution \(P_0(W_t)\), but multiple structural causal models remain consistent with its logs. Define a conceptual debt measure:

\[
\mathfrak D_t =
\operatorname{diam}
\left\{
P_0(W_t):
\mathcal M \text{ is consistent with available deployment records}
\right\},
\tag{17}
\]

where the diameter is measured in a task-relevant probability metric.

Reflexive debt grows when a system fails to preserve:

- deployment versions and exposure logs;
- randomized variation or valid instruments;
- unaffected comparison groups;
- action and intervention records;
- measurement-policy changes;
- ontology and institutional revisions;
- or causal provenance of future training data.

The system may continue to perform well on the world it has created while becoming unable to answer, “What would have happened without us?”

### 6.5 Epistemic capture

A lineage is in **epistemic capture** when it becomes increasingly calibrated on a world substantially produced by its own deployment while losing the capacity to estimate the pre-deployment world, alternative-policy worlds, or populations beyond its influence.

This can create a deceptive success pattern:

\[
\text{higher on-policy calibration}
\not\Rightarrow
\text{better independent understanding}.
\tag{18}
\]

A model can appear more correct because the world is becoming more compliant with the model. Epistemic capture is not necessarily intentional; it can arise from ordinary retraining under strong performative power and weak counterfactual monitoring.

---

## 7. Formal Properties

This section provides propositions for the minimum RMWS. Some are direct applications of standard dynamical-systems or causal-inference facts; the contribution lies in applying them to reflexive model lineages and interpreting their consequences.

### 7.1 Joint-state sufficiency

**Proposition 1 (World state alone need not be Markov).**  
Suppose the transition distribution satisfies:

\[
P(W_{t+1}\mid W_{0:t},M_{0:t},K_{0:t})
=
P(W_{t+1}\mid W_t,M_t,K_t),
\tag{19}
\]

and there exist two histories \(h,h'\) with the same \((W_t,K_t)\) but different model states \(M_t\neq M_t'\) such that:

\[
P(W_{t+1}\mid W_t,K_t,M_t)
\neq
P(W_{t+1}\mid W_t,K_t,M_t').
\tag{20}
\]

Then \((W_t,K_t)\) is not a sufficient Markov state. Under the conditional-independence assumptions of Equations (1)-(4), the augmented state:

\[
Z_t=(W_t,K_t,M_t)
\tag{21}
\]

is Markov.

**Interpretation.** If the model changes the world's transition law, two externally identical worlds can evolve differently because different models are deployed in them. A world model that omits its own model state is therefore structurally misspecified in such a regime.

**Proof.** Equation (20) violates the Markov sufficiency condition for \((W_t,K_t)\): the same proposed state admits different next-state distributions depending on omitted history summarized by \(M_t\). Including \(M_t\), together with the assumed conditional independence of the update and transition mechanisms, makes the distribution of \(Z_{t+1}\) depend only on \(Z_t\). \(\square\)

This motivates a **self-inclusive modeling principle**:

> A regulator that materially changes its target's transition law or its own future evidence must represent the joint world-deployment-update process unless its internal model state is conditionally redundant given the external state.

This is an RMWS principle, not a restatement of the good-regulator theorem.

### 7.2 Local loop stability

Linearize a differentiable RMWS around a fixed point \((w^*,m^*)\):

\[
\delta w_{t+1}=A\delta w_t+B\delta m_t,
\tag{22}
\]

\[
\delta m_{t+1}=C\delta w_t+D\delta m_t.
\tag{23}
\]

Then:

\[
\begin{bmatrix}
\delta w_{t+1}\\
\delta m_{t+1}
\end{bmatrix}
=
J
\begin{bmatrix}
\delta w_t\\
\delta m_t
\end{bmatrix},
\qquad
J=
\begin{bmatrix}
A&B\\
C&D
\end{bmatrix}.
\tag{24}
\]

Here:

- \(A\) captures world persistence;
- \(D\) captures model/update persistence;
- \(B\) is local model-to-world performative sensitivity;
- \(C\) is local world-to-model epistemic sensitivity.

**Proposition 2 (Local stability).**  
For the discrete-time linearized system in Equation (24), the fixed point is locally asymptotically stable if:

\[
\rho(J)<1,
\tag{25}
\]

where \(\rho\) is spectral radius. In the memoryless special case \(A=D=0\), the condition reduces to:

\[
\rho(BC)<1.
\tag{26}
\]

**Proof.** Equation (25) is the standard discrete-time linear stability criterion. If \(A=D=0\), then:

\[
J^2=
\begin{bmatrix}
BC&0\\
0&CB
\end{bmatrix}.
\]

The nonzero eigenvalues of \(BC\) and \(CB\) coincide, and eigenvalues of \(J\) are square roots of those eigenvalues up to sign/complex phase. Thus \(\rho(J)<1\) if and only if \(\rho(BC)<1\). \(\square\)

The product \(BC\) formalizes the intuitive loop gain: how strongly model changes move the world, multiplied by how strongly those world changes update the model. Delays, nonlinearities, and saturations can produce oscillation, bifurcation, or multiple attractors beyond this local analysis.

Most importantly:

\[
\boxed{\text{dynamical stability is not normative desirability}.}
\tag{27}
\]

A system can converge stably to an exploitative, homogeneous, or epistemically captured equilibrium.

### 7.3 Counterfactual-label mismatch

Let \(Y(0)\) be the outcome under a baseline policy with no model-triggered intervention and \(Y(\pi)\) the outcome under deployed policy \(\pi\). Suppose a model is intended to estimate:

\[
r_0(x)=P(Y(0)=1\mid X=x).
\tag{28}
\]

After deployment, the observed training label is \(Y(\pi)\), not \(Y(0)\).

**Proposition 3 (Naive retraining targets the wrong risk).**  
Under consistent empirical risk minimization with post-deployment samples \((X,Y(\pi))\), a sufficiently expressive learner converges to the on-policy conditional risk:

\[
r_\pi(x)=P(Y(\pi)=1\mid X=x),
\tag{29}
\]

not generally to \(r_0(x)\). If the intervention weakly prevents the adverse event for every \(x\), then:

\[
r_\pi(x)\leq r_0(x),
\tag{30}
\]

with strict inequality wherever treatment is both assigned and effective. Naive retraining therefore underestimates baseline risk on those regions.

**Proof.** The Bayes-optimal predictor for a proper loss under the observed post-deployment distribution is the corresponding conditional expectation of \(Y(\pi)\). Monotone prevention implies Equation (30). Unless \(Y(\pi)=Y(0)\) almost surely or the deployment effect is separately identified, the observed label does not identify the baseline target. \(\square\)

A successful prediction can therefore become observationally false because it was causally effective. This is not an edge case: alarms are often designed to invalidate their own forecasts.

### 7.4 Diversity contraction under a common target

Consider a scalar trait \(z_{i,t}\) and a common model-induced target \(\mu_t\). Suppose all agents update by:

\[
z_{i,t+1}=(1-\alpha)z_{i,t}+\alpha\mu_t,
\qquad 0<\alpha<1.
\tag{31}
\]

**Proposition 4 (Contraction).**  
If \(\mu_t\) is common across agents at time \(t\), then:

\[
\operatorname{Var}(z_{t+1})
=(1-\alpha)^2\operatorname{Var}(z_t).
\tag{32}
\]

**Proof.** Subtract the population mean. The common \(\mu_t\) cancels, leaving each centered deviation multiplied by \((1-\alpha)\). Squaring and averaging yields Equation (32). \(\square\)

The proposition is intentionally minimal. Real systems contain heterogeneous targets, costs, constraints, personalization, noise, contrarians, and multiple models. Those additions can preserve diversity, create clusters, or produce polarization. The result identifies the base mechanism: broad optimization toward a common low-dimensional target is a contraction operator along the optimized dimension.

### 7.5 Single-history non-identifiability

**Proposition 5 (A single deterministic deployment history does not identify reflexive strength in general).**  
Given a realized trajectory \((D_{0:T},O_{1:T+1})\), and absent restrictions on latent variables or the structural equations, there exist:

1. a structural causal model in which \(D_t\) causally affects future \(O_{t+h}\); and
2. a structural causal model in which no such causal effect exists,

that induce the same observational distribution along the realized deployment path.

**Proof sketch.** In the first model, define \(O_{t+1}=f(D_t,U_t)\) with a nonzero intervention effect. In the second, introduce a latent variable \(V_t\) that jointly determines the observed deployment and outcome along the realized path, and define \(O_{t+1}=g(V_t,U_t)\) with no arrow from \(D_t\). Structural functions can be chosen to match the same joint observational distribution. The models differ under interventions on \(D_t\), which are not observed in a single deterministic history. \(\square\)

Identification therefore requires assumptions or variation: randomized deployments, instruments, discontinuities, policy changes, sentinel groups, structural restrictions, or transportability conditions. Ordinary retraining logs are not enough to measure a system's own performative power.

### 7.6 Institutional hysteresis

Let institutional state evolve as:

\[
I_{t+1}=(1-\lambda)I_t+\lambda\phi(D_t,W_t),
\qquad 0<\lambda\leq1,
\tag{33}
\]

and let the world transition depend on \(I_t\). Suppose a model is withdrawn at time \(T\), so \(D_t=0\) for \(t\geq T\).

**Proposition 6 (Withdrawal does not imply restoration).**  
Unless the pre-deployment institutional state is an absorbing state under the post-withdrawal dynamics, there is no general reason for:

\[
(W_t,I_t)\rightarrow(W_0,I_0)
\quad\text{as}\quad t\rightarrow\infty.
\tag{34}
\]

**Proof.** At withdrawal, \(I_T\) generally differs from \(I_0\). Subsequent transitions start from \(I_T\), and Equation (33) need not invert the prior updates or even contain \(I_0\) as an attractor. Path dependence follows. \(\square\)

Rollback must therefore be persistence-aware. Restoring an earlier model checkpoint is not equivalent to restoring the world that existed before the model.

---

## 8. Evaluation: Prediction, Steering, and Legitimacy

A single accuracy score cannot evaluate a reflexive system because the model may change the event against which it is scored.

### 8.1 Baseline descriptive fidelity

Does the model estimate what would occur under a specified reference policy \(d_0\)?

\[
R_{\mathrm{base}}(\theta;d_0)
=
E\left[\ell(f_\theta(X),Y(d_0))\right].
\tag{35}
\]

This is often the intended target of risk prediction, diagnosis, or counterfactual planning.

### 8.2 On-policy predictive fidelity

Does the model accurately estimate what will occur under the deployed policy \(\pi\)?

\[
R_{\mathrm{dep}}(\theta,\pi)
=
E\left[\ell(f_\theta(X),Y(\pi))\right].
\tag{36}
\]

This can differ from baseline fidelity even when both are estimated correctly.

### 8.3 Causal steering utility

Did deployment cause desirable outcomes?

\[
U(\pi)=E[u(W(\pi),A(\pi))].
\tag{37}
\]

A self-negating alarm may have poor naive predictive accuracy but high steering utility. A self-fulfilling credit denial may have good on-policy calibration but negative social utility.

### 8.4 Legitimacy and distribution

Welfare aggregates do not settle questions of:

- autonomy and manipulation;
- consent and contestability;
- fairness and burden distribution;
- concentration of performative power;
- preservation of meaningful alternatives;
- reversibility;
- and rights that should not be traded for average utility.

Legitimacy therefore remains a separate evaluation axis. The paper does not propose a single universal legitimacy function; it requires systems to state and audit the normative constraints under which steering is permitted.

### 8.5 Four-way evaluation matrix

| Baseline fidelity | On-policy fidelity | Steering utility | Interpretation |
|---|---|---|---|
| High | High | High | Accurate and beneficial under both reference and deployed regimes |
| High | Low | High | Potentially successful self-negating intervention |
| Low | High | Ambiguous | Possible epistemic capture or purely on-policy adaptation |
| High | High | Low | Accurate but harmful or exploitative steering |
| Low | Low | Low | Ordinary failure, possibly compounded by reflexivity |

This matrix prevents a common category error: treating the observed post-deployment label as the only truth against which the original prediction should be judged.

### 8.6 Monitoring estimands

A reflexive deployment should state at least:

1. the baseline outcome \(E[Y(d_0)\mid X]\);
2. the on-policy outcome \(E[Y(\pi)\mid X]\);
3. the deployment effect \(E[Y(\pi)-Y(d_0)]\);
4. the effect of replacing the current model with a successor;
5. the distribution of adaptation costs;
6. channel-specific descendancy scores;
7. the strength and health of anchor channels;
8. and uncertainty due to non-identification.

Monitoring “accuracy drift” without these estimands can confuse successful intervention, harmful steering, external drift, measurement change, and ordinary model error.

---

## 9. Reflexive Model Ecologies

### 9.1 From a loop to a commons

Real evidence environments contain many model lineages. Let \(n\) lineages deploy outputs \(D_t^1,\ldots,D_t^n\) into a shared world:

\[
W_{t+1}=F(W_t,D_t^1,\ldots,D_t^n,\xi_t).
\tag{38}
\]

Each lineage observes:

\[
O_{t+1}^i=H_i(W_{t+1},D_t^{1:n},\nu_t^i)
\tag{39}
\]

and updates:

\[
M_{t+1}^i=L_i(M_t^i,O_{t+1}^i).
\tag{40}
\]

The evidence-generating world is a **reflexive commons**: each lineage can alter a resource from which all lineages learn.

### 9.2 Cross-lineage externalities

The influence matrix \(\Gamma\) from Equation (12) distinguishes:

- self-effects \(\Gamma_{ii}\);
- one-way contamination \(\Gamma_{ij}>0,\Gamma_{ji}\approx0\);
- reciprocal coupling;
- and densely connected model ecologies.

Examples include:

- one recommender changing preferences later observed by another;
- one generative model filling public corpora used by competitors;
- one credit system changing applicant behavior seen by other lenders;
- one ranking changing institutional definitions used by all evaluators.

A lineage may be locally well-governed while imposing large unpriced evidence externalities on others.

### 9.3 Possible ecological regimes

Multiple models do not guarantee diversity. Depending on objectives, user mobility, concentration, shared data, and response heterogeneity, model ecologies can produce:

- **pluralistic specialization:** different lineages sustain distinct niches;
- **synchronization:** models converge because they train on the same altered evidence;
- **proxy arms races:** competitors intensify optimization of the same narrow measure;
- **ecological collapse:** rare evidence disappears from all lineages;
- **strategic cycling:** each model adapts to the responses induced by competitors;
- **dominance:** one lineage's performative power determines the effective environment for all others.

Multi-player performative prediction supplies game-theoretic tools for some of these regimes (Narang et al., 2023). RMWS adds the evidence-commons interpretation and cross-lineage provenance obligations.

### 9.4 Conditional pluralism

Competition and outside options can reduce the performative power of a single platform, while personalization can increase it (Hardt et al., 2022). But pluralism preserves epistemic and cultural diversity only under additional conditions:

- users can genuinely move among systems;
- models do not optimize the same proxy;
- evidence channels are not centrally controlled;
- minority states remain observable;
- and cross-lineage ancestry is tracked.

Nominally separate models trained on the same reflexively altered corpus are not independent evaluators.

---

## 10. Illustrative Experiments

The following experiments are deliberately small mechanistic models. They are not calibrated to a real population, medical system, or production model. Their purpose is to demonstrate that the proposed distinctions generate different measurable outcomes and to provide reproducible reference implementations for future work. Full code, seed values, and result files accompany this paper.

### 10.1 Experiment A: Norm and appearance coevolution

#### 10.1.1 Question

Can a representation of a social preference become a selection pressure that changes both the represented population and the preference function used to retrain the representation?

#### 10.1.2 Setup

Each of \(N=2{,}400\) agents has:

- a two-dimensional appearance vector \(x_{i,t}\);
- a two-dimensional preference vector \(p_{i,t}\);
- a cost for changing appearance;
- and, in the pluralistic condition, a probability of contrarian response.

The initial population contains three subcultures centered at distinct points. A platform aggregates current preferences into one or more score ideals. Under a common score, agents move toward a shared ideal:

\[
x_{i,t+1}
=x_{i,t}
+\alpha(m_t-x_{i,t})
+\epsilon_{i,t}.
\tag{41}
\]

In the joint-response condition, exposure to highly scored appearances also moves preferences:

\[
p_{i,t+1}
=(1-\beta)p_{i,t}
+\beta\Phi(\operatorname{Exposure}_{m_t})
+\zeta_{i,t}.
\tag{42}
\]

Four regimes are compared over 45 rounds and 60 random seeds:

1. passive independent drift;
2. one common score with appearance response only;
3. one common score with appearance and preference response;
4. three locally updating models with exploration and a minority of contrarian agents.

Diversity is measured as the trace of the population covariance, normalized to the initial value. This is a spread measure, not a normative claim that all variance is valuable.

#### 10.1.3 Results

![Figure 2. Appearance diversity under four norm-feedback regimes.](figures/figure_2_beauty_diversity.png)

**Figure 2.** Mean normalized appearance spread over 60 seeds. The two single-score appearance curves nearly overlap. The common target acts as a contraction, while plural local models retain multiple attractors.

After 45 rounds, passive drift retained 101.96% of initial appearance spread. The single-score conditions retained approximately 0.24%, consistent with the contraction mechanism in Proposition 4. The pluralistic condition retained 89.42%. These numerical values are consequences of the toy parameters, not predictions about human societies.

![Figure 3. Preference diversity under four norm-feedback regimes.](figures/figure_3_preference_diversity.png)

**Figure 3.** When exposure updates preferences, the process that generates future labels also contracts. Appearance response alone leaves preference variance approximately unchanged; joint response reduces it sharply. Plural local models preserve most initial preference spread.

The preference channel separates the two otherwise similar single-score regimes. Appearance response alone retained essentially all initial preference spread, because labels remained exogenous to the score. Joint appearance-preference feedback retained only 0.47% of initial preference spread. The pluralistic regime retained 84.76%.

The experiment demonstrates four points.

1. Feature adaptation and preference adaptation are different causal channels even when both appear as distribution shift.
2. A high-accuracy model can become constitutive of the labels on which its successor is trained.
3. Homogenization is not inevitable; architecture, plurality, exploration, and heterogeneous response alter the regime.
4. Evaluation should include modification burden and preserved alternatives, not only predictive fit.

### 10.2 Experiment B: Self-negating decision support

#### 10.2.1 Question

What happens when a model is intended to predict risk under no intervention, but its alarms trigger an effective intervention and the successor is naively trained on the resulting labels?

#### 10.2.2 Setup

A scalar feature \(X\sim\mathcal N(0,1)\) determines baseline adverse-event risk:

\[
P(Y(0)=1\mid X=x)
=\sigma(-1.05+1.75x).
\tag{43}
\]

A deployed model estimates baseline risk. Treatment probability rises smoothly with predicted risk, with a small probability floor and overlap to preserve identifiability. Treatment lowers log-odds by 2.15:

\[
P(Y=1\mid X=x,T=t)
=\sigma(-1.05+1.75x-2.15t).
\tag{44}
\]

Two lineages are compared over 14 retraining rounds and 35 seeds:

- **Naive lineage:** fits \(Y\) from \(X\), ignoring treatment, and interprets the result as baseline risk.
- **Causal-aware lineage:** fits \(Y\) from \((X,T)\) and estimates baseline risk by evaluating the model at \(T=0\).

Both begin with pre-deployment untreated data.

#### 10.2.3 Results

![Figure 4. Baseline-risk error after self-negating deployment.](figures/figure_4_counterfactual_label_mismatch.png)

**Figure 4.** Brier error for the no-deployment target. Naive retraining rapidly learns the post-intervention label process rather than the intended baseline risk. The causal-aware model remains close to the baseline structural relation in this correctly specified simulation.

At the final round, the naive lineage's mean baseline Brier error was 0.02520, compared with 0.00005 for the causal-aware lineage. The near-zero value for the causal model reflects the intentionally correct logistic specification and should not be expected in arbitrary real systems.

![Figure 5. Mean predicted baseline risk under naive and causal-aware retraining.](figures/figure_5_baseline_risk_underestimation.png)

**Figure 5.** The true mean no-deployment risk is approximately 0.415. Naive retraining converges near 0.312 because it treats prevented events as evidence that the original risk was lower. The causal-aware lineage remains near the target.

The naive lineage underestimates mean baseline risk by approximately 24.9%. Yet the labels causing this error are evidence that the intervention worked. A dashboard that reports only mismatch between the alarm and observed outcome would punish causal success. The experiment reproduces the mechanism analyzed in causal decision-support research: post-intervention outcomes identify a different target unless deployment is modeled explicitly (Boeken et al., 2024).

### 10.3 Experiment C: Evidence ancestry versus synthetic fraction

#### 10.3.1 Question

Does the conventional synthetic-data label predict recursive drift, or is causal descendancy from the model lineage more informative?

#### 10.3.2 Setup

The target world is a 160-category Zipf distribution with exponent 1.16. Its effective support, measured as \(\exp(H(P))\), is approximately 35.29 categories. Each generation observes 7,000 records and estimates a smoothed categorical model. Five regimes are compared over 40 generations and 60 seeds:

1. **Independent real:** all observations sampled independently from the target.
2. **Independent synthetic:** 80% of observations generated by an independently specified simulator that samples from the target; 0% are descended from the active lineage.
3. **Model synthetic:** 80% generated from a sharpened version of the current model; 80% are model-descended.
4. **Human-origin, model-selected:** 0% synthetic, but model-mediated selection reweights which human-origin events enter the dataset.
5. **Recursive replacement:** 100% generated from a sharpened current model.

The comparison is intentionally constructed so that regimes 2 and 3 have the same synthetic fraction but different ancestry, while regime 4 has no synthetic records but strong ancestry.

#### 10.3.3 Results

![Figure 6. Distributional drift by evidence ancestry.](figures/figure_6_evidence_ancestry_js.png)

**Figure 6.** Jensen-Shannon divergence from the target distribution. The independently specified synthetic simulator remains as stable as independent real sampling. Model-generated and model-selected evidence drift despite differing content provenance.

At generation 40, independent real and independent synthetic regimes both had mean Jensen-Shannon divergence of approximately 0.0041 and effective support near the true value. The 80%-model-synthetic regime reached mean divergence 0.2552 and effective support 3.30. The human-origin but model-selected regime reached divergence 0.5369 and effective support 1.05, comparable to recursive replacement.

![Figure 7. Tail preservation by evidence ancestry.](figures/figure_7_evidence_ancestry_tail.png)

**Figure 7.** Estimated mass in the lower half of categories, normalized by the true tail mass. Independent real and independent synthetic channels preserve the tail. Model-generated evidence retains approximately 24.1% of true tail mass in this regime. Human-origin but model-selected evidence retains approximately 2.9%.

The result does not establish a universal law that ancestry dominates every other data property. It demonstrates a counterexample to the sufficiency of the human-versus-synthetic distinction. A lineage-independent simulator can preserve the target, while human-origin data can become highly endogenous through model-mediated selection.

### 10.4 Compact result table

| Experiment | Regime | Final primary result |
|---|---|---:|
| Norm coevolution | Passive drift | 101.96% initial appearance spread |
| Norm coevolution | Single score | 0.24% initial appearance spread |
| Norm coevolution | Single score + preference response | 0.47% initial preference spread |
| Norm coevolution | Plural models + exploration | 89.42% appearance; 84.76% preference spread |
| Decision support | Naive retraining | Baseline Brier 0.02520; mean risk 0.312 |
| Decision support | Causal-aware | Baseline Brier 0.00005; mean risk 0.415 |
| Evidence ancestry | 80% independent synthetic | JS divergence 0.0041; tail ratio 1.026 |
| Evidence ancestry | 80% model synthetic | JS divergence 0.2552; tail ratio 0.241 |
| Evidence ancestry | 0% synthetic, model-selected | JS divergence 0.5369; tail ratio 0.029 |

### 10.5 What the experiments do not show

The experiments do not establish that:

- real beauty standards will collapse to one point;
- causal adjustment is easy in high-dimensional clinical settings;
- all model-generated data degrade;
- all human adaptation is harmful;
- plurality is always protective;
- or causal ancestry alone determines data quality.

They show that the proposed causal distinctions are operational, reproducible, and capable of separating regimes that conventional static evaluation merges.

---

## 11. The Reflexive System Audit

The theory should terminate in an operational protocol. The following audit is designed for a model lineage before deployment, during operation, and after major updates.

### Step 1: Identify the governed lineage

Document:

- which model versions belong to the lineage;
- retraining, fine-tuning, distillation, and replacement rules;
- inherited datasets and objectives;
- operational roles;
- and ownership or governance transitions.

A lineage boundary that changes opportunistically after failure is not auditable.

### Step 2: Draw a time-unrolled causal graph

Include at least:

- model outputs and actions;
- human or institutional responses;
- world-state changes;
- exposure and measurement processes;
- future training records;
- retraining decisions;
- persistent institutions;
- and other model lineages.

Static feature diagrams are insufficient when the relevant effects are delayed.

### Step 3: Populate the eight-channel signature

For each channel \((X,Y,S,Q,U,\Omega,I,E)\), record:

- plausible causal paths;
- affected groups;
- direction and delay;
- persistence;
- anticipated benefit and harm;
- and current evidence strength.

An empty channel should mean “evaluated and judged negligible,” not “not considered.”

### Step 4: Map model-descended evidence

For every evidence source used in training or monitoring, document:

- exposure to prior model versions;
- direct and indirect ancestry paths;
- estimated descendancy over relevant horizons;
- and the policy regime the evidence identifies.

Content provenance alone is not enough.

### Step 5: State causal estimands

At minimum distinguish:

- baseline risk or outcome;
- on-policy outcome;
- deployment effect;
- replacement or retraining effect;
- adaptation costs;
- and cross-lineage effects.

Do not deploy a single metric called “accuracy” without specifying the intervention regime.

### Step 6: State identification assumptions

Specify whether estimates rely on:

- randomized deployment or encouragement;
- instrumental variables;
- discontinuities;
- natural experiments;
- parallel institutions;
- sentinel populations;
- structural models;
- transportability;
- or untestable invariance assumptions.

Report non-identification rather than filling gaps with point estimates.

### Step 7: Estimate dynamics and power

Measure where possible:

- channel-specific causal effects;
- performative power;
- response delay;
- local loop gain;
- adoption and concentration;
- personalization;
- user mobility and outside options;
- and institutional persistence.

Local stability analysis should be paired with stress tests for nonlinear, delayed, and multi-attractor behavior.

### Step 8: Protect epistemic health

Maintain and monitor:

- grounding reserves;
- support and tail coverage;
- causal provenance;
- counterfactual uncertainty;
- diversity of independent evaluators;
- ontology drift;
- and reflexive debt.

A model should not be permitted to silently erase the channels used to evaluate it.

### Step 9: Evaluate welfare and legitimacy separately

Assess:

- outcome benefit;
- adaptation burden;
- distributional effects;
- autonomy and preference manipulation;
- consent and contestability;
- concentration of power;
- and preservation of alternatives.

Stable convergence and high on-policy accuracy do not satisfy these requirements by themselves.

### Step 10: Define persistence-aware rollback

A rollback plan should specify:

- which model version is restored or removed;
- which institutional rules must be changed;
- how affected populations are compensated;
- how categories, incentives, and interfaces are unwound;
- how descendant data are marked or excluded;
- and which anchor measurements verify recovery.

Rollback is a world-state intervention, not merely a software operation.

### 11.1 Minimum deployment dossier

A high-impact reflexive system should not deploy without a dossier containing:

1. lineage manifest;
2. causal graph;
3. reflexive signature;
4. estimand registry;
5. provenance and descendancy schema;
6. grounding-reserve specification;
7. identification plan;
8. stability and stress-test results;
9. legitimacy assessment;
10. persistence-aware rollback plan.

---

## 12. Design Contracts for Reflexive AI Systems

The audit suggests architecture-level obligations.

### 12.1 Protected grounding reserve

Maintain evidence sources that the active policy cannot freely manipulate. Protection may be technical, organizational, legal, or institutional. A reserve should be sufficient for explicit queries, not merely symbolically independent.

### 12.2 Causal provenance by default

Training records should carry versioned ancestry metadata. Provenance systems should distinguish:

- direct generation;
- model-mediated human response;
- institutional mediation;
- cross-lineage exposure;
- and independent observation.

### 12.3 Evaluator-actuator separation

The same unconstrained lineage should not simultaneously:

1. reshape the evaluated environment;
2. select the evidence;
3. define the metric;
4. and decide whether the evidence validates its own deployment.

Separation does not require complete organizational independence in every system, but it requires nontrivial barriers to evaluator capture.

### 12.4 Randomized probes and shadow policies

Small randomized variations, shadow decisions, delayed rollouts, and sentinel groups can preserve identifiability. These mechanisms should be designed before full deployment, because once a system becomes universal there may be no remaining comparison regime.

### 12.5 Bounded performative channels

Explicitly constrain the system's capacity to alter:

- evaluation inputs;
- user preferences;
- institutional rules;
- and successor-training data.

A model may need broad action authority while retaining narrow authority over the evidence used to certify it.

### 12.6 Epistemic non-interference

For a protected channel \(G\), define a design target:

\[
\sup_{d,d'\in\mathcal A}
\mathfrak d\left[P(G\mid do(D=d)),P(G\mid do(D=d'))\right]
\leq\epsilon.
\tag{45}
\]

This will not be achievable for every query. Where it is impossible, the system should document the remaining causal dependence and use alternative identification strategies.

### 12.7 Plural evaluation

Multiple evaluators are useful only when they have meaningfully different:

- evidence sources;
- objectives;
- causal exposure;
- governance;
- and failure modes.

An ensemble of models trained on the same descended data is not an independent grounding reserve.

### 12.8 Reflexive safety envelope

A local engineering contract may combine:

\[
\rho(J)<1,
\tag{46}
\]

\[
\Pi_H\leq\pi_{\max},
\tag{47}
\]

\[
\gamma_{\mathrm{anchor}}\geq\gamma_{\min},
\tag{48}
\]

plus domain-specific welfare, rights, and concentration constraints. These are partial obligations, not a universal proof of safety. They make specific claims auditable.

---

## 13. Implications for Advanced and Self-Improving AI

### 13.1 The missing self in a world model

A sufficiently capable AI will not observe a policy-independent world. It may influence:

- human behavior and preferences;
- scientific agendas and experiment selection;
- economic allocation;
- institutional categories and rules;
- the information published and preserved;
- the training data of future models;
- and the objectives assigned to successors.

Its relevant state is therefore not merely \(W_t\). A more adequate state is:

\[
Z_t=(W_t,K_t,M_t,\mathcal E_t,\mathcal L_t),
\tag{49}
\]

where \(\mathcal E_t\) is the evidence ecology and \(\mathcal L_t\) the interacting lineages. Under policy \(\pi\):

\[
Z_{t+1}\sim\mathcal T_\pi(Z_t,\xi_t).
\tag{50}
\]

A model that accurately represents physical and social regularities while omitting its own causal effect on those regularities can still be systematically wrong about the future.

### 13.2 Reflexive alignment

Conventional alignment discussions often evaluate a model at a time slice: its objective, current behavior, outputs, or immediate consequences. RMWS suggests a trajectory-level object.

> **Reflexive alignment is the property that the model-world trajectories induced by a system remain within an acceptable set, including the evidence, preferences, institutions, and successor systems generated along the way.**

A provisional condition is:

\[
P_\pi\left(Z_{0:\infty}\in\mathcal S_{\mathrm{traj}}\right)
\geq1-\delta,
\tag{51}
\]

where \(\mathcal S_{\mathrm{traj}}\) constrains not only physical outcomes but also:

- welfare and rights;
- autonomy and preference manipulation;
- institutional concentration;
- evidence integrity and grounding;
- causal provenance;
- reversibility;
- and effects on successor models.

This is a research target, not a solved specification. Its value is to identify the correct object of concern.

### 13.3 Self-modeling is necessary but not sufficient

An advanced system may need to represent:

- its own deployment policy;
- how humans and institutions respond to it;
- how those responses change future observations;
- how retraining will interpret those observations;
- and how successors inherit its effects.

That is an epistemic requirement. It is not a moral guarantee. A harmful optimizer can model its own influence extremely well. Reflexive alignment still requires acceptable objectives, constraints, governance, and distributions of power.

### 13.4 Recursive self-improvement

Self-improvement creates an especially tight lineage. A model proposes changes to its architecture, data, tools, evaluators, or objectives; the changed system generates new evidence; that evidence justifies further change. The loop is:

\[
M_t
\rightarrow
\text{improvement proposal}
\rightarrow
M_{t+1}
\rightarrow
\text{new evidence and evaluator state}
\rightarrow
M_{t+2}.
\tag{52}
\]

The danger is not only objective drift inside the model. The lineage can reshape the benchmark, tool environment, data distribution, and institutional process that determine whether its changes appear successful. A self-improving stack therefore needs:

- lineage-bound authority limits;
- independently protected evaluation channels;
- causal provenance of self-generated experience;
- randomized or counterfactual evaluation where possible;
- and governance that cannot be widened solely by evidence produced under the system's own expanded authority.

### 13.5 Memory and context systems

Long-horizon AI memory should distinguish independently grounded observations from model-descended summaries, plans, and environments. Otherwise, a system can repeatedly compress its own prior interpretations and mistake persistence for corroboration. Memory records should carry:

- source lineage;
- action exposure;
- summarization ancestry;
- counterfactual regime;
- and protected-evidence status.

This connects reflexive provenance to context compaction and continual learning.

### 13.6 Negative learning and regret

A regret subsystem learns from undesirable outcomes. In a reflexive system, observed regret may be endogenous to the policy that produced or prevented it. A model should distinguish:

\[
\text{regret under deployed policy}
\]

from:

\[
\text{counterfactual regret under alternatives}.
\]

Without this distinction, successful prevention can erase the evidence of risk, while harmful steering can make the chosen policy look inevitable. Reflexive causal models are therefore a prerequisite for reliable long-horizon regret learning.

---

## 14. Limitations and Red-Team Analysis

### 14.1 “This is only performative prediction with more labels”

This criticism has force. A sufficiently general distribution map can represent every channel in the audit signature. RMWS is valuable only if the decomposition changes practice. The paper argues that it does because feature response, outcome prevention, measurement change, preference formation, ontology shift, and institutional persistence require different estimands and interventions. Future work should demonstrate this advantage on real deployments rather than relying on conceptual plausibility.

### 14.2 “This is only cybernetics”

Cybernetics supplies the loop and much of the stability language. RMWS adds a modern learning-system boundary: governed lineages, future evidence, causal ancestry, counterfactual labels, and cross-model ecologies. The framework should be understood as a specialization and extension of cybernetic thinking, not a replacement.

### 14.3 Model definition remains contestable

The functional definition excludes passive traces but still permits debate about implicit representation. Some policies may behave model-like without a clean extractable state. The framework can accommodate graded evidence for modelhood, but borderline cases remain.

### 14.4 Causal descendancy may be difficult to identify

Equation (13) is an estimand, not a guarantee of estimability. Complex deployments may lack randomization, instruments, overlap, or unaffected groups. The framework's response is to preserve uncertainty and reflexive debt rather than invent precise scores. In some systems only bounds will be defensible.

### 14.5 The eight channels may not be exhaustive

The signature is intended as a high-coverage audit decomposition. Additional domains may require distinct channels, such as physical infrastructure, legal authority, or intergenerational biology. The test for adding a channel should be whether it introduces a distinct causal mechanism, estimand, or governance response—not whether it offers another descriptive synonym.

### 14.6 Stability analysis is local

The spectral-radius criterion does not capture global nonlinear dynamics, strategic discontinuities, changing state spaces, or rare transitions. It should be supplemented by simulation, reachability analysis, adversarial stress testing, and empirical monitoring.

### 14.7 The simulations are intentionally stylized

The experiments establish mechanisms under controlled assumptions. They do not estimate effect sizes in real social or medical systems. In particular, the norm simulation omits embodiment, social networks, identity, inequality, and multidimensional welfare. The ancestry simulation uses an intentionally aggressive selection rule to make the causal distinction visible.

### 14.8 Grounding can become stale

Protected evidence is not automatically relevant evidence. A pre-deployment archive may preserve independence while failing to represent a changing world. Partially performative prediction correctly emphasizes that endogenous effects and exogenous drift coexist (Lee and Zrnic, 2026). A grounding reserve must therefore balance independence with temporal relevance.

### 14.9 Pluralism can become an arms race

Multiple models can preserve diversity, but they can also optimize the same proxy more aggressively, synchronize through shared data, or segment populations manipulatively. The pluralistic simulation is an existence demonstration, not a universal recommendation.

### 14.10 Normative pluralism remains unresolved

The framework can separate prediction, steering, and legitimacy, but it cannot derive a universal social objective. Decisions about acceptable preference influence, institutional change, and distribution of power require political and ethical judgment. RMWS makes those choices visible; it does not eliminate them.

---

## 15. Research Agenda

### 15.1 Identification methods for evidence descendancy

Develop estimators and bounds for \(r_H\) using:

- randomized exposure;
- platform discontinuities;
- instrumental variables;
- causal representation learning;
- transport across institutions;
- and synthetic control designs.

A priority is distinguishing direct content ancestry from behavioral and institutional ancestry.

### 15.2 Provenance standards

Extend data-lineage standards with causal fields for:

- model version exposure;
- deployment regime;
- affected channels;
- estimated effect magnitude;
- and counterfactual validity.

Such a standard should support record-level and aggregate provenance without requiring impossible causal certainty.

### 15.3 Reflexive benchmarks

Most benchmarks hold the world fixed. New benchmarks should include environments where models alter:

- future tasks;
- evaluator behavior;
- available observations;
- user preferences;
- and successor-training data.

A benchmark should reward correct self-impact modeling rather than accidental on-policy calibration.

### 15.4 Global regime theory

Extend the local Jacobian analysis to:

- delayed systems;
- stochastic approximation;
- multiple time scales;
- bifurcations and hysteresis;
- networked agents;
- and changing ontologies.

The aim is a phase diagram connecting performative power, response delay, anchor strength, concentration, heterogeneity, and institutional persistence to qualitative outcomes.

### 15.5 Multi-lineage governance

Estimate cross-lineage matrices \(\Gamma\) and develop governance for evidence externalities. Questions include:

- When should a model compensate others for contaminating shared data?
- How should provenance obligations cross organizational boundaries?
- Can independent anchor institutions be treated as public epistemic infrastructure?
- How can ecosystems preserve rare evidence and minority preferences?

### 15.6 Preference-sensitive alignment

Develop models that distinguish:

- learning preexisting preferences;
- enabling reflective preference change;
- ordinary persuasion;
- manipulation;
- and coercive preference capture.

Reflexive alignment cannot avoid this problem because advanced systems will influence what humans later ask them to optimize.

### 15.7 Persistence-aware intervention science

Study how to unwind model-induced institutions, categories, and habits. Software rollback is mature; socio-technical rollback is not. Research should measure decay rates, compensation mechanisms, and restoration of lost alternatives.

### 15.8 Formal reflexive alignment

Specify tractable subsets of \(\mathcal S_{\mathrm{traj}}\), prove invariants under bounded model influence, and connect them to:

- corrigibility;
- non-manipulation;
- authority non-escalation;
- preserved epistemic channels;
- and successor governance.

The goal is not a single scalar alignment theorem, but a set of composable obligations over the evolving loop.

---

## 16. Conclusion

Models are commonly treated as mirrors: they receive evidence from a world and are judged by how faithfully they reflect it. Consequential deployment changes the relationship. A score can become an incentive, an alarm can prevent its outcome, a ranking can become an institution, a recommendation can become a preference, a category can become a social reality, and a generated record can become training data for a successor. The mirror becomes one of the causes of what it later reflects.

The scientifically useful question is therefore not whether “everything is feedback.” It is:

> **When does a governed model lineage acquire enough causal influence that its future evidence can no longer be interpreted independently of its own deployment?**

Reflexive Model-World Systems answers with a closure criterion and a set of operational distinctions. The lineage is reflexive when deployment changes evidence used by a successor. The effect should be decomposed across state, outcome, exposure, measurement, preference, ontology, institution, and model ecology. Evidence should be classified by causal descendancy, not only by whether a human or model emitted the record. Grounding should be protected relative to a lineage, horizon, and query. Evaluation should distinguish baseline description, on-policy prediction, causal steering, and legitimacy. Rollback should restore persistent world state, not merely software.

The deepest implication is concise:

\[
\boxed{
\text{A sufficiently influential learner cannot model the future correctly}
\\
\text{while treating itself as external to how that future is generated.}
}
\tag{53}
\]

For advanced AI, the object that must be understood and governed is therefore not the model alone. It is the evolving joint system:

\[
\boxed{
\text{model} \leftrightarrow \text{world} \leftrightarrow
\text{evidence} \leftrightarrow \text{successor model}.
}
\tag{54}
\]

Alignment, on this view, is a property of the trajectory produced by that loop.

---

# Appendix A. Claim and Maturity Ledger

The paper separates inherited results from proposed concepts so that later versions can strengthen evidence without obscuring provenance.

| Claim | Status | Basis or next step |
|---|---|---|
| Deployment can change the distribution a model later faces | Established | Performative prediction literature |
| Feature, sampling, outcome, and model feedback can have different bias effects | Established | Existing feedback-loop taxonomies |
| Public measures and classifications can recreate social behavior and institutions | Established | Sociology of reactivity and looping effects |
| Effective alarms can corrupt naive retraining labels | Established | Causal decision-support theory; reproduced here |
| Recursive replacement with model output can lose distributional support | Established in studied settings | Model-collapse literature |
| Collapse is not inevitable when independent signal is retained or data accumulate | Established in analyzed settings | Accumulation and stable-signal results |
| Reflexive closure over a governed model lineage | Proposed definition | Requires adoption and comparison across domains |
| Eight-channel Reflexive Causal Audit Signature | Proposed synthesis | Test coverage on case studies; extend if needed |
| Model-descended evidence | Proposed causal-provenance concept | Develop estimators and provenance standard |
| Grounding reserve | Proposed operational framework | Formalize sufficiency for specified query sets |
| Reflexive debt | Proposed identifiability measure | Develop computable bounds and case studies |
| Epistemic capture | Proposed failure mode | Develop empirical diagnostics |
| Cross-lineage influence matrix and reflexive commons | Proposed ecological framework | Estimate in multi-platform or shared-corpus systems |
| Self-inclusive modeling principle | Proposed theorem family | Prove under richer POMDP and institutional models |
| Reflexive alignment as trajectory property | Proposed ASI framing | Connect to formal safety and governance obligations |

---

# Appendix B. Additional Formal Detail

## B.1 A causal graph for self-negating prediction

A minimal decision-support graph contains:

\[
X\rightarrow \hat Y\rightarrow T\rightarrow Y,
\]

with \(X\rightarrow Y\) and possibly \(X\rightarrow T\). The model is trained to estimate \(Y(0)\), but deployment makes \(T\) a descendant of \(\hat Y\). Conditioning only on \((X,Y)\) after deployment merges baseline risk with treatment response. If treatment assignment has overlap and no unmeasured confounding conditional on \(X\), a correctly specified model for \(P(Y\mid X,T)\) can estimate the baseline by setting \(T=0\). When those assumptions fail, randomized encouragement, instruments, or bounds are required.

## B.2 Decomposing the local Jacobian by channel

Let \(B_j\) be the local effect of model state on world-regime channel \(j\), and \(C_j\) the local effect of that channel on the model update. Then:

\[
B=[B_X\;B_Y\;B_S\;B_Q\;B_U\;B_\Omega\;B_I\;B_E],
\]

and the closed-loop contribution can be written schematically as:

\[
BC=\sum_j B_jC_j+\sum_{j\neq k}B_jC_k.
\tag{B1}
\]

The cross terms matter. A model may alter exposure \(S\), which changes preferences \(U\), which changes labels and therefore model updates. Channel decomposition is not an assumption of independence; it is a way to expose causal paths that a single distribution-distance measure would hide.

## B.3 Delays and oscillation

With a one-step delayed epistemic response:

\[
\delta m_{t+1}=C\delta w_{t-1}+D\delta m_t,
\]

the state must be augmented with \(w_{t-1}\). Even when the undelayed system is stable, delay can introduce complex eigenvalues and overshoot. This motivates the delay-oscillation hypothesis: for comparable coupling strength, slower adaptation can turn convergence into cycling. Fashion, ranking response, and policy retraining are candidate domains, but empirical confirmation is required.

## B.4 Heterogeneous response and polarization

Let agents respond to a common model ideal \(\mu_t\) with signed susceptibility \(s_i\):

\[
z_{i,t+1}=z_{i,t}+\alpha s_i(\mu_t-z_{i,t}).
\]

For \(s_i>0\), agents conform; for \(s_i<0\), they move away. A distribution with both signs can separate into conformist and counter-model subpopulations. Reflexivity can therefore increase variance or polarization rather than contract it. The regime depends on the susceptibility distribution, model visibility, social interaction, and saturation.

## B.5 A minimal epistemic-capture diagnostic

Let \(R_{\mathrm{dep},t}\) be on-policy risk and \(R_{\mathrm{anchor},t}\) risk on a protected baseline or alternative-policy channel. Define:

\[
\operatorname{ECI}_t
=
\Delta R_{\mathrm{anchor},t}
-
\Delta R_{\mathrm{dep},t}.
\tag{B2}
\]

A rising positive Epistemic Capture Indicator means on-policy performance is improving relative to protected counterfactual performance. This is only a diagnostic; interpretation depends on anchor validity and whether policy change is intended to move the world away from the baseline.

---

# Appendix C. Simulation Specification and Reproducibility

## C.1 Software and seeds

The reference implementation uses Python, NumPy, SciPy, pandas, scikit-learn, and Matplotlib. The base seed is 20260814. All results are generated from the included script:

```text
code/simulations.py
```

The script writes raw per-seed results, compact summaries, and all figures. No external dataset is used.

## C.2 Experiment A parameters

| Parameter | Value |
|---|---:|
| Agents | 2,400 |
| Dimensions | 2 |
| Initial subcultures | 3 |
| Rounds | 45 |
| Appearance adaptation rate | 0.10 |
| Preference adaptation rate | 0.06 |
| Noise standard deviation | 0.025 |
| High-score exposure fraction | 0.15 |
| Seeds | 60 |

The pluralistic regime contains three locally updating ideals and a 12% contrarian probability. Results should be read qualitatively; changing adaptation rates changes the time scale and final contraction.

## C.3 Experiment B parameters

| Parameter | Value |
|---|---:|
| Batch size per round | 5,000 |
| Retraining rounds | 14 |
| Seeds | 35 |
| Baseline logit | \(-1.05+1.75x\) |
| Treatment log-odds effect | \(-2.15\) |
| Minimum treatment probability | 0.04 |
| Maximum treatment probability | 0.88 |
| Policy threshold | 0.32 |
| Policy steepness | 12.0 |
| Smoothed parameter update rate | 0.70 |

The causal-aware estimator is correctly specified and includes treatment. The experiment therefore illustrates target mismatch more than robust causal learning under misspecification.

## C.4 Experiment C parameters

| Parameter | Value |
|---|---:|
| Categories | 160 |
| Target distribution | Zipf exponent 1.16 |
| Records per generation | 7,000 |
| Generations | 40 |
| Seeds | 60 |
| Synthetic fraction in paired comparison | 0.80 |
| Model sharpening exponent | 1.35 |
| Model-mediated selection exponent | 1.25 |
| Dirichlet-style count smoothing | 0.20 |

Tail mass is defined over the lower half of categories by rank. Effective support is \(\exp(H(P))\). Jensen-Shannon divergence uses base-2 logarithms.

## C.5 Reproducibility command

```bash
python code/simulations.py
```

---

# References

Boeken, P., Zoeter, O., and Mooij, J. (2024). Evaluating and correcting performative effects of decision support systems via causal domain shift. *Proceedings of the Third Conference on Causal Learning and Reasoning*, PMLR 236, 551-569.

Conant, R. C., and Ashby, W. R. (1970). Every good regulator of a system must be a model of that system. *International Journal of Systems Science*, 1(2), 89-97. doi:10.1080/00207727008920220.

Espeland, W. N., and Sauder, M. (2007). Rankings and reactivity: How public measures recreate social worlds. *American Journal of Sociology*, 113(1), 1-40. doi:10.1086/517897.

Francis, B. A., and Wonham, W. M. (1976). The internal model principle of control theory. *Automatica*, 12(5), 457-465.

Fybish, G., and Susnjak, T. (2026). When predictions shape reality: A socio-technical synthesis of performative predictions in machine learning. arXiv:2601.04447.

Gerstgrasser, M., Schaeffer, R., Dey, A., Rafailov, R., Sleight, H., Hughes, J., Korbak, T., Agrawal, R., Pai, D., Gromov, A., Roberts, D. A., Yang, D., Donoho, D. L., and Koyejo, S. (2024). Is model collapse inevitable? Breaking the curse of recursion by accumulating real and synthetic data. arXiv:2404.01413; presented at the First Conference on Language Modeling.

Glickman, M., and Sharot, T. (2025). How human-AI feedback loops alter human perceptual, emotional and social judgements. *Nature Human Behaviour*, 9(2), 345-359. doi:10.1038/s41562-024-02077-2.

Hacking, I. (1995). The looping effects of human kinds. In D. Sperber, D. Premack, and A. J. Premack (Eds.), *Causal Cognition: A Multidisciplinary Debate*. Oxford University Press.

Hardt, M. (2026). Retraining seeks stable signals. arXiv:2607.15623. Companion article to an invited contribution to the International Congress of Mathematicians 2026.

Hardt, M., Jagadeesan, M., and Mendler-Dünner, C. (2022). Performative power. *Advances in Neural Information Processing Systems*, 35.

Kehrenberg, T., Sanguino Bautiste, F. J., Lozano, J. A., and Quadrianto, N. (2026). Dissecting performative prediction: A comprehensive survey. *ACM Computing Surveys*, 58(13), 1-35. doi:10.1145/3816429.

Lee, J., and Zrnic, T. (2026). Partially performative prediction. arXiv:2606.07890.

Lucas, R. E., Jr. (1976). Econometric policy evaluation: A critique. *Carnegie-Rochester Conference Series on Public Policy*, 1, 19-46.

Manheim, D., and Garrabrant, S. (2019). Categorizing variants of Goodhart's law. arXiv:1803.04585.

Mendler-Dünner, C., Carovano, G., and Hardt, M. (2024). An engine not a camera: Measuring performative power of online search. *Advances in Neural Information Processing Systems*, 37, 59266-59288.

Narang, A., Faulkner, E., Drusvyatskiy, D., Fazel, M., and Ratliff, L. J. (2023). Multiplayer performative prediction: Learning in decision-dependent games. *Journal of Machine Learning Research*, 24(202), 1-56.

Odling-Smee, F. J., Laland, K. N., and Feldman, M. W. (2003). *Niche Construction: The Neglected Process in Evolution*. Princeton University Press.

Pagan, N., Baumann, J., Elokda, E., De Pasquale, G., Bolognani, S., and Hannak, A. (2023). A classification of feedback loops and their relation to biases in automated decision-making systems. In *Proceedings of the ACM Conference on Equity and Access in Algorithms, Mechanisms, and Optimization*. doi:10.1145/3617694.3623227.

Pedreschi, D., Pappalardo, L., Ferragina, E., Baeza-Yates, R., Barabasi, A.-L., Dignum, F., Dignum, V., Eliassi-Rad, T., Giannotti, F., Kertesz, J., Knott, A., Ioannidis, Y., Lukowicz, P., Passarella, A., Pentland, A. S., Shawe-Taylor, J., and Vespignani, A. (2025). Human-AI coevolution. *Artificial Intelligence*, 340, 104244. doi:10.1016/j.artint.2024.104244.

Perdomo, J. C., Zrnic, T., Mendler-Dünner, C., and Hardt, M. (2020). Performative prediction. *Proceedings of the 37th International Conference on Machine Learning*, PMLR 119, 7599-7609.

Richens, J., Abel, D., Bellot, A., and Everitt, T. (2025). General agents contain world models. *Proceedings of the 42nd International Conference on Machine Learning*, PMLR 267. arXiv:2506.01622.

Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R., and Gal, Y. (2024). AI models collapse when trained on recursively generated data. *Nature*, 631, 755-759. doi:10.1038/s41586-024-07566-y.

Virgo, N., Biehl, M., Baltieri, M., and Capucci, M. (2025). A “good regulator theorem” for embodied agents. In *Proceedings of Artificial Life 2025*. MIT Press. doi:10.1162/ISAL.a.874.

Wu, J., Abebe, R., and Mendler-Dünner, C. (2026). Reaching a consensus in predictive loops. arXiv:2603.12137.
