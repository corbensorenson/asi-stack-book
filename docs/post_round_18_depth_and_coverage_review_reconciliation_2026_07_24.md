# Post-Round-18 Depth and Coverage Review Reconciliation

Status: **binding roadmap amendment; no support or release effect**

Date: 2026-07-24

Authority: Corben Sorenson

Roadmap: `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`

## Purpose

This record adjudicates the external review that followed the terminal Round 18
breadth transaction. It separates four different conditions that a keyword
sweep can otherwise collapse:

1. a genuinely unowned chapter-scale system boundary;
2. a real depth defect inside an existing owner;
3. a concept already present under broader or different terminology; and
4. a literal phrase absence that does not establish a conceptual absence.

The distinction matters because the book must not test a thin or
under-specified mechanism and then treat an implementation failure as evidence
against the underlying idea. It also must not reopen structural expansion
whenever a search misses an exact phrase. This amendment therefore adds a
claim-bearing maturity gate, accepts a bounded depth packet, and approves two
chapter candidates for research and distinct-owner adjudication after a
material P2 checkpoint. It does not admit either candidate to the manifest,
change any claim support, open protected outcomes, authorize an experiment, or
create a release.

## Baseline verification

The working manifest contains **66 chapters**, not 61. The five Round 18
chapters have the following exact manuscript word counts:

| Chapter | Words | Adjudication |
|---|---:|---|
| Multi-Agent Dynamics, Collective Intelligence, and Systemic Risk | 3,087 | Real chapter with a distinct owner; material formal-foundations depth remains |
| Embodied Agency, Real-Time Control, and Physical Safety | 3,162 | Real chapter with a distinct owner; control and state-estimation depth remains |
| Human–AI Organizations, Delegation, and Accountability | 3,172 | Real chapter with a distinct owner; organizational and transition depth remains |
| Perception, Sensor Fusion, and Observation Trust | 3,269 | Real chapter with a distinct owner; estimator and fusion depth remains |
| Inner Alignment, Mesa-Optimization, and Learned-Objective Integrity | 3,452 | Real chapter with a distinct owner; central terminology and mechanism distinctions remain |
| White-Box Evidence, Interpretability, and Activation Governance | 5,290 | Established owner; the already-open construct-validity and feature-analysis amendment remains necessary |

The similar headings are partly explained by the project-wide chapter packet:
claim state, mechanism, interfaces, invariants, minimum viable implementation,
baseline, test plan, evidence plan, failures, proofs, sources, and handoff.
These chapters are not empty generated shells. Each already supplies a distinct
system transition and a bounded mechanism proposal. However, similar structure
plus substantially below-average length is a useful depth alarm. It is not a
completion metric and cannot be repaired by padding to a word target.

The source-reference count in the review is also not the manifest count. The
five Round 18 chapters each declare six source IDs; White-Box declares eight.
Uniform source counts are a triage signal, not proof of superficial engagement.
The depth packet below requires passage-level use by epistemic role rather than
a higher count.

## Finding-by-finding adjudication

| Review finding | Disposition | Binding consequence |
|---|---|---|
| Inner Alignment omits the exact phrases “deceptive alignment,” “gradient hacking,” and “training story.” | **Accepted with correction.** The chapter already treats mesa-optimization, goal misgeneralization, evaluator awareness, concealment, strategic compliance, persistent conditional policies, power pressure, and construct validity. The literal absence is not a conceptual void, but the chapter does not yet give readers the field-standard distinctions or a sufficiently concrete gradient-hacking threat model. | Add an explicit taxonomy linking deceptive alignment, situational awareness, training-game reasoning, gradient hacking, reward tampering, goal misgeneralization, and ordinary specification gaming. Specify observables, competing explanations, intervention points, and non-claims. |
| Multi-Agent Dynamics has no game theory. | **Accepted with correction.** “Game-theoretic” appears repeatedly and the chapter already owns equilibrium pressure, collusion, mechanism design, cascades, and externalities. It lacks an adequate formal bridge through games, equilibrium concepts, bargaining, repeated interaction, information structure, social choice, and mechanism design. | Add a formal-foundations section with normal/extensive/Bayesian/stochastic game distinctions; Nash and correlated equilibrium as limited tools; repeated-game and bargaining dynamics; social-choice impossibility and preference aggregation; mechanism-design assumptions; learning-in-games; and explicit limits of equilibrium prediction. |
| Perception barely develops sensor fusion and omits Kalman filtering. | **Accepted.** The chapter owns observation trust but does not yet develop estimation deeply enough for its title and downstream physical-safety role. | Add a state-estimation and fusion section covering Bayesian filtering; linear Kalman, extended/unscented Kalman, and particle-filter regimes; observability and identifiability; registration, synchronization, calibration, correlated error, out-of-sequence measurements, multimodal disagreement, learned fusion, and safe degradation. The chapter must explain when each estimator family fails rather than canonize one. |
| White-Box omits sparse autoencoders and construct validity. | **Accepted.** Relevant source records are present, but source presence is not manuscript engagement. This confirms the existing White-Box depth packet. | Expand the existing packet to cover probes and controls; sparse autoencoders, transcoders, and dictionary learning; feature splitting, absorption, dead latents, reconstruction trade-offs, selectivity, causal interventions, steering side effects, interpretability illusions, cross-distribution validity, and diagnostic-versus-causal evidence. |
| The five Round 18 chapters are only stubs. | **Rejected as stated; accepted as a relative-depth warning.** Their owner boundaries and implementation packets are real. None is mature enough merely because it entered the manifest. | Apply the maturity gate below to the five Round 18 chapters plus White-Box before any chapter-specific claim-bearing test can earn N3 scope. No word-count quota and no automatic support movement. |
| Instrumental convergence is missing. | **Stale.** `failure-modes-of-ungoverned-intelligence.qmd` contains a dedicated “Instrumental convergence, power, and option preservation” section and maps power-seeking into authority creep and evaluation. | Add only an Inner Alignment handoff and terminology crosswalk if the depth pass finds reader ambiguity. Do not duplicate the owner. |
| Causal discovery, confounding, epistemic/aleatoric uncertainty, and conformal prediction are missing. | **Mostly stale; one precision residual.** Governed World Models already covers causal/intervention records, latent-confounding and selection assumptions, model disagreement, distribution/support uncertainty, calibration, abstention, and conformal coverage with explicit limits. The epistemic/aleatoric decomposition is not yet made reader-explicit. | Preserve Governed World Models as owner. During depth work, add a concise decomposition distinguishing data noise, parameter/model uncertainty, structural/causal uncertainty, and distributional uncertainty, and explain when the labels become misleading. Do not create another chapter or restate the existing causal section. |
| Retrieval-augmented generation is missing. | **Stale.** Virtual Context ABI contains a dedicated governed-RAG pipeline section and compares ordinary RAG, Self-RAG, GraphRAG, hierarchical retrieval, long context, citations, poisoning, actual use, and cost. | No new roadmap packet. Maintain through ordinary source renewal. |
| AI moral patienthood and welfare are missing. | **Stale.** Moral Uncertainty contains “Possible artificial moral patients,” separates consciousness, sentience, welfare, agency, and moral patienthood, and states strong non-claims. | No duplicate section. Maintain the precautionary and non-attribution boundary through source renewal. |
| Refinement and dependent types are missing. | **Accepted at section scale.** The Lean proof-envelope chapter uses refinement operationally but lacks a reader-facing account of refinement types, dependent types, liquid/refinement checking, proof-carrying data, and the limits of finite encodings. | Add a bounded section to Executable Specifications and the Lean Proof Envelope. Tie the type systems to actual ASI Stack interfaces and state what they cannot prove about semantics, deployment, or open-world behavior. |
| Synthetic data and self-play are underdeveloped. | **Accepted at section scale.** Data Engines already discusses synthetic data and provenance but not a complete governed generation lifecycle. | Add a section on teacher/student generation, self-play and adversarial generation, curriculum and hard-negative production, contamination and model collapse, diversity and coverage, provenance, filtering, rights, evaluator leakage, and held-out separation. |
| Human explanation generation is underdeveloped. | **Accepted at section scale.** Human Factors treats explanation burden, comprehension, and misleading explanations; White-Box owns internal evidence. The generation-to-understanding interface remains implicit. | Add a Human Factors section distinguishing a plausible narrative, a faithful causal account, a decision-relevant explanation, and a usable instruction. Bind generation to provenance, uncertainty, counterfactual tests, comprehension checks, actionability, contestability, and workload; hand off internal-evidence claims to White-Box. |
| Labor, economic impact, and diffusion are absent. | **Accepted as a bounded scope decision.** Human–AI Organizations already distinguishes productivity from welfare, covers labor arrangements and accountability diffusion, and declines to prescribe one employment model. It does not yet orient the reader to diffusion, bargaining power, task reallocation, distributional effects, or macroeconomic claim limits. | Add a bounded organizational-transition section. Cover task versus job effects, adoption and diffusion, complement/substitute dynamics, bargaining and surveillance, heterogeneous gains and harms, deskilling/reskilling, concentration, public capacity, and measurement limits. Explicitly route economy-wide causal claims to a future institutions/deployment owner unless that owner is admitted. |

## Claim-bearing chapter maturity gate

A chapter is **mature enough to enter claim-bearing implementation design** only
when a reviewed maturity record shows all six conditions below. “Proof-ready”
does not mean empirically supported or formally proved. It means the prose is
specific enough that a competent implementation and fair test can be designed
without silently inventing the mechanism after held-out outcomes are visible.

1. **Field decomposition.** The chapter names and develops the central
   sub-concepts, contested definitions, and adjacent-owner boundaries needed to
   understand the claimed mechanism. A keyword checklist cannot pass this gate;
   an omitted central distinction can fail it.
2. **Strongest challenge.** The chapter states the strongest relevant
   counterargument, at least one simpler baseline, and any favorable or oracle
   regime needed to show that the instrument could detect success.
3. **Implementation determination.** Mechanism state, inputs, outputs,
   interfaces, invariants, update rules, activation conditions, fallback,
   observables, and prohibited shortcuts are concrete enough for two competent
   implementers to converge on materially equivalent systems. Remaining
   discretionary choices are declared as preregistered factors.
4. **Failure and non-claim envelope.** The chapter separates mechanism failure,
   implementation failure, construct failure, evaluator failure, resource
   failure, and out-of-scope conditions; it states what even a passing result
   would not establish.
5. **Literature engagement by role.** Passage-reviewed primary sources cover
   mechanism/capability, limitation/failure, competing design or simpler
   baseline, and measurement/evaluation where the literature permits. The
   prose must use those roles to make or bound a claim. Reference count,
   bibliography presence, and uniform citation density do not pass.
6. **Territory-sized reader value.** The chapter has enough explanation,
   examples, diagrams or tables where useful, cross-chapter handoffs, and
   synthesis to teach its owned transition without template repetition.
   Word count is a diagnostic only; padding, duplicated method prose, and
   source-summary accumulation fail.

The maturity record must include a per-condition disposition, exact chapter
locations, unresolved residuals, reviewer, date, and maximum allowed next
inference. A chapter that fails a condition may still remain a useful
argument-level chapter. It may not use a naive implementation to support a
mechanism-level negative inference.

## Accepted depth packet

The existing White-Box packet is broadened into
`P7.2-T1D-proof-readiness-depth-pack`. It covers six chapters:

1. Inner Alignment;
2. Multi-Agent Dynamics;
3. Perception;
4. Embodied Agency;
5. Human–AI Organizations; and
6. White-Box Evidence.

The first, second, third, fifth, and sixth have exact residuals above. Embodied
Agency receives the same maturity review and must deepen the bridge among
dynamics and system identification, state estimation, latency and real-time
scheduling, robust/model-predictive control, reachability and safe sets,
contact and actuator uncertainty, sim-to-real transfer, recovery, and
human/environment safety. It must not turn control-theory citations into a
local physical-safety claim.

The packet also includes the four confirmed section integrations:

- uncertainty decomposition in Governed World Models;
- refinement/dependent types in the Lean proof-envelope chapter;
- synthetic/self-play data generation in Data Engines; and
- human explanation generation in Human Factors.

The organizational-transition section belongs inside the Human–AI
Organizations chapter and therefore ships with that chapter's depth record.
Instrumental convergence, RAG, and artificial moral status receive no duplicate
packet because their owners already contain substantive sections.

### Terminal artifacts

The packet is terminal only when it ships:

- one six-chapter maturity matrix with evidence for every gate;
- meaning-bearing prose changes for every accepted depth defect;
- source inventory and passage-reviewed source notes for missing source roles;
- updated chapter source maps, evidence tables, adjacent-owner handoffs, and
  `docs/book_outline.md`;
- claim-atom and reader projections without support promotion;
- a template-inheritance audit showing that the new prose is chapter-specific;
- one negative mutation per maturity condition plus mutations for missing
  chapter coverage and source-role laundering; and
- targeted validation, full book/publication validation, and local render
  receipts.

The packet may run as the single existing-book WIP slot beside P2. It follows
the historical six-chapter atom pack and W3 inheritance guard so its prose is
written against stable claim identities and a current repetition baseline. The
combined 66-chapter reader-freshness packet derives after it.

## Two approved chapter candidates, not admissions

The review identifies two domains that appear to pass the distinct-owner test.
They are approved for research and adjudication, not for immediate manifest
admission. Structural freeze remains active. Candidate research is not an
extra WIP lane: it begins only after the material P2 checkpoint and terminal
depth packet below, when the existing-book slot is available. Admission
requires:

1. a completed material P2 empirical/evidence checkpoint;
2. terminal six-chapter depth work;
3. a dated decision packet passing the ordinary exclusive-owner, competence,
   reader-value, source-role, safety, birth-artifact, and non-displacement
   gates; and
4. admission one chapter at a time, followed by manifest/outline/source/atom/
   reader reconciliation before the next decision.

### Candidate N — Adversarial Machine Learning and the Model Attack Surface

**Provisional part:** Part I, adjacent to the Security Kernel.

**Exclusive owner:** the attack lifecycle against the *learned system* across
training, adaptation, inference, distribution, and model access. The chapter
must define a versioned threat model and an attack/defense receipt joining
attacker knowledge and capability, target model and checkpoint, attack surface,
perturbation or influence budget, objective, transfer/adaptation state,
observed effect, detection, mitigation, residual, and disclosure.

**Required territory:** adversarial examples and evasion; poisoning and clean-
label attacks; backdoors and trojans; jailbreak and safeguard bypass as model-
behavior attacks; model extraction/stealing and inversion where they attack the
learned artifact; adaptive and transfer attacks; multimodal and agentic attack
surfaces; certified, empirical, monitoring, red-team, and recovery defenses;
and accuracy/utility/security trade-offs.

**Adjacent-owner boundary:** Security Kernel continues to own system, tool,
identity, network, prompt-injection, and authority security; Privacy/Data
Rights owns information-flow and privacy harms; Supply-Chain Integrity owns
artifact provenance; Adversarial Evaluation owns evaluator challenge and
behavioral elicitation. Candidate N passes only if its learned-model threat
model and attack lifecycle cannot be cleanly absorbed by those owners.

### Candidate O — Learning Theory, Generalization, and Scaling Science

**Provisional part:** Part III, near Governed Model Training and the Efficient
ASI Hypothesis.

**Exclusive owner:** the evidence contract for claims that a learned system
will generalize, scale, transfer, or exhibit a capability outside its observed
training support. The chapter must connect assumptions about data, hypothesis
class, optimization, inductive bias, compute, and evaluation to the exact
scope of a generalization or scaling claim.

**Required territory:** PAC-style and distribution-dependent generalization;
capacity and complexity measures; algorithmic stability; compression, minimum
description length, and information-theoretic views; optimization and implicit
bias; interpolation, double descent, and benign overfitting; grokking and phase
changes; scaling laws and broken-law diagnostics; emergence measurement and
metric artifacts; transfer, out-of-distribution generalization, and
compositionality; credit assignment; data/compute/model scaling; and explicit
limits when deep-network theory does not determine real behavior.

**Adjacent-owner boundary:** Governed Model Training owns the operational
training lifecycle and optimizer policy; Efficient ASI owns resource-efficiency
hypotheses; Benchmark Ratchets owns evaluation renewal; Compact Generative
Models owns one compression-oriented architecture family; Mathematical and
Search Substrates own their mechanisms. Candidate O passes only if it remains a
coherent generalization/scaling claim contract rather than a disconnected
survey or duplicate training chapter.

## Final coverage sweep and stop rule

After the depth packet and the two candidate adjudications, run one
manifest-to-territory sweep using concepts, interfaces, artifacts, lifecycle
transitions, failure families, and source roles—not raw keyword counts. Every
finding must receive one of: existing owner and exact section, accepted depth
residual, admitted distinct owner, research-only candidate, or explicit
out-of-scope boundary.

Raw keyword counts do not adjudicate completeness.

The default after that sweep is structural freeze. Sixty-eight chapters is a
possible result if both candidates pass, not a target or a completeness claim.
A later source may reopen structure only when it exposes a genuinely unowned
interface, invariant, artifact type, lifecycle transition, or failure family
and a dated amendment names the material evidence checkpoint that pays the
integration cost.

## Non-claims

This audit does not establish that any chapter claim is true, that a chapter is
empirically or formally complete, that any model attack or defense works, that
learning theory predicts deployed ASI behavior, that longer prose is better,
that all fields are covered, that 68 chapters is optimal, that P2 is unblocked,
or that the book is ready for a new release. It changes roadmap obligations
only.
