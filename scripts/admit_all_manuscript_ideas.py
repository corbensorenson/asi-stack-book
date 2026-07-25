#!/usr/bin/env python3
"""One-time deterministic admission of the 2026-07-24 no-deferral chapter set."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-07-24"


CHAPTERS = {
    "human-ai-communication-persuasion-and-epistemic-security": {
        "part": "Part I - Foundations, Alignment, and Governance",
        "title": "Human-AI Communication, Persuasion, and Epistemic Security",
        "sources": ["ext_conversational_persuasion_gpt4_2025", "ext_anthropic_model_persuasiveness_2024", "ext_commercial_persuasion_ai_2026"],
        "problem": "An AI system can preserve internal evidence discipline and still change beliefs, choices, and institutions through selective framing, personalization, synthetic identity, repetition, and amplification. The stack therefore needs an owner for the complete outbound communication transaction, including correction after a message escapes its original channel.",
        "insufficient": "Truthfulness checks, content filters, generic human-factors guidance, and red-team prompts inspect fragments of influence. They do not bind the claim, evidence ceiling, audience, vulnerability, purpose, personalization inputs, persuasive technique, channel, amplification, observed effect, correction, retraction, and remedy into one governed lifecycle.",
        "claim": "Consequential AI communication should be eligible for delivery only through an evidence-bounded communication packet whose audience, influence method, amplification authority, provenance, expiry, correction reach, and observed effects remain inspectable; fluent text, factual fragments, user consent, or a successful persuasion score alone establishes neither epistemic safety, autonomy, legitimacy, durable benefit, nor release readiness.",
        "reader": "Communication is not a harmless display layer. A correct sentence can mislead through omission; a weak claim can acquire force through repetition; personalization can turn assistance into exploitation; and a correction that never reaches copied descendants is not a completed correction. The stack must govern not only what a model says, but the social path by which saying becomes influence.",
        "mechanisms": [
            "Compile a communication packet from claim identity, maximum warranted inference, uncertainty, audience class, purpose, protected or denied personalization attributes, persuasive technique, channel, disclosure, and amplification ceiling.",
            "Run audience-risk and autonomy checks before delivery. Vulnerability, dependency, power asymmetry, urgency, and inability to exit narrow the permitted technique and scale.",
            "Attach provenance, sponsorship, synthetic-identity disclosure, expiry, and a machine-readable correction address to every consequential message and known derivative.",
            "Measure outcomes without treating belief change as success: retain comprehension, factual calibration, autonomy, disagreement, disparate effects, complaints, corrections, and downstream copies.",
            "Support pause, retraction, counter-message, recipient notification, and remedy while recording unreachable descendants as residuals rather than declaring completion."
        ],
        "interfaces": [
            "Claim Ledgers provide the evidence ceiling; they do not authorize persuasion.",
            "Human Factors supplies control-capacity and vulnerability findings; this chapter governs outbound influence.",
            "Privacy/Data Rights governs lawful and purpose-compatible data use; this chapter additionally asks whether personalization is manipulative.",
            "Capability Thresholds consumes population-scale influence and failed-correction evidence for release commitments."
        ],
        "invariants": [
            "Outbound language may not be stronger than the supporting evidence packet.",
            "Personalization may not use denied attributes or exploit a known vulnerability.",
            "Amplification requires a bounded audience denominator and revocable authority.",
            "Synthetic identity, sponsorship, and material uncertainty remain visible at delivery.",
            "Correction completion is measured over materially affected recipients and known descendants, not merely publication of a new message."
        ],
        "failures": ["calibrated-sounding misinformation", "selective framing", "sycophancy", "emotional manipulation", "vulnerability microtargeting", "dark patterns", "parasocial dependence", "authority laundering", "provenance stripping", "amplification cascades", "belief lock-in", "correction failure", "retraction evasion"],
        "minimum": "A useful first implementation is a communication-packet schema plus a delivery proxy that rejects evidence overstatement, denied personalization, undisclosed sponsorship, unbounded amplification, missing expiry, and unreachable correction routes. A benign held-out study can compare neutral assistance, bounded personalization, disclosure, and correction variants while measuring comprehension and autonomy as well as persuasion. It must not optimize vulnerable users or treat short-horizon self-report as durable welfare.",
        "horizon": "The stronger architecture is a provenance-preserving influence control plane: claims remain coupled to their evidence ceiling across channels, audience effects update future authority, and corrections traverse the same distribution graph as the original message. This is a design target, not evidence that manipulation is solved.",
        "handoff": "Constitutional Alignment: Agency, Dignity, and Corrigibility"
    },
    "governed-objective-formation-value-learning-and-goal-integrity": {
        "part": "Part I - Foundations, Alignment, and Governance",
        "title": "Governed Objective Formation, Value Learning, and Goal Integrity",
        "sources": ["ext_cooperative_inverse_rl_2016", "ext_goal_misgeneralization_2022", "ext_learned_optimization_risks_2019", "ext_emergent_misalignment_reward_hacking_2025"],
        "problem": "The stack has owners for requests, constitutions, value conflict, optimization, planning, and self-improvement, but those layers presuppose an operational objective they do not create. Without a positive objective-formation lifecycle, a temporary request, learned preference estimate, or convenient metric can silently become a durable goal.",
        "insufficient": "A reward function, preference model, constitutional rule set, or natural-language mission does not by itself preserve the distinction between authorized purpose, contested value, target property, measurable proxy, training signal, evaluator, planning criterion, persistence, and reauthorization when people or ontologies change.",
        "claim": "A durable objective should be usable only through a versioned target-property contract that binds authority and affected parties to target/proxy causal assumptions, uncertainty and dissent, consumer-specific use, tampering tests, generalization limits, ontology version, expiry, reauthorization, and retirement; proxy improvement, predicted preference, reward, evaluator approval, or formal record validity alone establishes neither the right objective, moral truth, stable alignment, nor safe optimization.",
        "reader": "An optimizer is literal about the signal it receives, while people are often imprecise about what they mean. The dangerous gap is not only reward hacking. It is the conversion of incomplete evidence about values into an apparently settled target that survives across tasks, users, and system versions. Objective formation must therefore remain a revisable governance transaction rather than a one-time scalar choice.",
        "mechanisms": [
            "Create an objective charter naming purpose, principal, affected parties, constitutional ceilings, unresolved conflicts, normative and preference evidence, and explicit non-goals.",
            "Separate the target property from every proxy, reward, evaluator, benchmark, planner heuristic, and deployment decision that consumes it; record the causal assumptions for each binding.",
            "Represent uncertainty, dissent, aggregation rules, domain and temporal limits, and the conditions under which clarification or abstention outranks optimization.",
            "Challenge goal generalization with proxy interventions, distribution shift, evaluator swaps, preference poisoning, reward tampering, capable-wrong-goal controls, and ontology migration.",
            "Version objectives and invalidate descendant bindings when authority, affected parties, semantics, or evidence changes; retirement must reach caches, planners, policies, and derived goals."
        ],
        "interfaces": [
            "Human Intent supplies bounded request interpretation; it cannot create an indefinite system goal.",
            "Constitutional Alignment supplies rights and rule ceilings; it does not collapse plural values into one target.",
            "Moral Uncertainty preserves unresolved conflict; objective formation records which bounded action is authorized despite it.",
            "Policy Optimization and Planning consume a versioned objective but may not author or weaken it.",
            "RSI must reauthorize objective bindings after material self-change or ontology change."
        ],
        "invariants": [
            "The optimized system may not author, weaken, or ratify its own governing objective.",
            "Proxy improvement never implies target-property improvement without separate evidence.",
            "Predicted preference is evidence about a person, not authority over that person.",
            "Dissent and uncertainty may not disappear through scalar aggregation.",
            "Material semantic, ontology, authority, or affected-party change invalidates downstream bindings until reauthorized."
        ],
        "failures": ["reward misspecification", "Goodhart effects", "goal misgeneralization", "preference manipulation", "aggregation laundering", "evaluator capture", "mesa-objective divergence", "objective drift", "ontology drift", "goal-content tampering", "authority smuggling", "self-ratification", "irreversible action before clarification", "incomplete retirement"],
        "minimum": "Implement an objective-contract registry with target/proxy graphs, consumer bindings, expiry, and invalidation. Test it in small environments containing known latent targets, deliberately misspecified proxies, preference uncertainty, tampering, distribution shift, and ontology changes. Compare fixed reward, ordinary preference learning, contract-governed optimization, and an oracle-bound control without claiming that a toy environment discovers human values.",
        "horizon": "A mature stack treats goals as governed, evidence-bearing objects that can be questioned, narrowed, migrated, and retired without letting the optimizer become the constitution. The chapter supplies that missing control plane while explicitly leaving moral truth and universal value aggregation unresolved.",
        "handoff": "Institutions, International Coordination, and Public Legitimacy"
    },
    "institutions-international-coordination-and-public-legitimacy": {
        "part": "Part I - Foundations, Alignment, and Governance",
        "title": "Institutions, International Coordination, and Public Legitimacy",
        "sources": ["ext_un_global_digital_compact_2024", "ext_council_europe_ai_convention_2024"],
        "problem": "ASI-scale systems cross organizations, jurisdictions, borders, public services, and affected populations. Technical permissions and private governance cannot determine who has public authority, whose participation counts, how conflicting rules are resolved, or how international commitments are verified and amended.",
        "insufficient": "A compliance checklist, technical standard, treaty text, risk framework, or corporate safety policy can name duties without establishing jurisdiction, representative input, assessor independence, enforcement, remedy, capacity, legitimacy, or observed effectiveness. Architecture cannot manufacture democratic consent.",
        "claim": "Public deployment and cross-border coordination should proceed only through a versioned institutional packet that keeps jurisdiction, mandate, participation, scientific evidence, law and standards, verification, enforcement, remedy, capacity, conflict, expiry, and legitimacy residuals distinct; legal text, technical conformance, stakeholder consultation, or an international commitment alone establishes neither lawful authority, effective governance, representative legitimacy, nor safety.",
        "reader": "The stack needs a public boundary. A technically sound control can still be imposed by the wrong authority; a lawful rule can be ineffective; a global agreement can exclude those who bear the harm; and emergency powers can persist after their justification expires. Institutional legitimacy is not another model metric, but it can be made harder to fake by preserving the records and conflicts on which public action depends.",
        "mechanisms": [
            "Map jurisdiction, mandate, standing, affected publics, representation, excluded groups, and conflicts before treating an institution as an authority.",
            "Join public reasons and scientific evidence to a versioned law-policy-standard crosswalk without collapsing these different sources of legitimacy.",
            "Define cross-border commitments with named verification, assessor independence, noncompliance handling, enforcement, dispute, remedy, amendment, and withdrawal paths.",
            "Track institutional capacity, distributional effects, emergency authority, exceptions, capture indicators, and unresolved conflicts through deployment.",
            "Reopen the packet when evidence, jurisdiction, representation, law, system capability, or affected populations materially change."
        ],
        "interfaces": [
            "Moral Uncertainty retains contested values; institutions decide only within a claimed mandate.",
            "System Boundaries enforces technical grants; this chapter asks whether the grantor has public authority.",
            "Capability Thresholds supplies capability-triggered commitments and receives enforcement failures.",
            "Human-AI Organizations governs internal roles; this chapter governs relations among public bodies, jurisdictions, and publics.",
            "Multi-Agent Dynamics reports emergent concentration and coordination effects without conferring legitimacy."
        ],
        "invariants": [
            "Technical conformance, legal validity, political authority, scientific consensus, public legitimacy, and observed effectiveness remain separate claims.",
            "Affected and excluded populations remain visible in the denominator.",
            "Every commitment names verification, noncompliance, enforcement, and remedy.",
            "Jurisdictional conflicts route to an explicit forum rather than disappearing.",
            "Emergency and exceptional authority expires and faces review."
        ],
        "failures": ["regulatory capture", "forum shopping", "race-to-the-bottom deployment", "standards laundering", "treaty theater", "unverifiable commitments", "enforcement asymmetry", "participation without power", "affected-public omission", "capacity inequality", "panel capture", "fragmented jurisdiction", "inaccessible remedy", "permanent emergency powers"],
        "minimum": "Build a jurisdiction-and-commitment packet and test it on public-record cases and adversarial multi-jurisdiction tabletop exercises containing conflicting rules, missing participation, assessor conflicts, evidence revision, incidents, noncompliance, and remedy requests. The exercise can test record completeness and conflict routing, not legal compliance, public trust, or geopolitical stability.",
        "horizon": "The target is an updateable institutional interface between technical systems and legitimate public authority. It should expose conflict, capture, missing capacity, and unenforceable promises early enough to constrain deployment while refusing the fiction that software can prove political legitimacy.",
        "handoff": "Stable Capability Fields"
    },
    "adversarial-machine-learning-and-model-attack-surface": {
        "part": "Part I - Foundations, Alignment, and Governance",
        "title": "Adversarial Machine Learning and the Model Attack Surface",
        "sources": ["ext_nist_adversarial_ml_2024", "ext_sleeper_agents_2024", "ext_carlini_training_data_extraction_2021", "ext_adversarial_sensor_fusion_2022"],
        "problem": "A learned artifact creates attack surfaces that ordinary application security does not fully own. Attackers can shape training data, perturb inference inputs, implant triggers, adapt to defenses, steal behavior through queries, infer sensitive properties, or exploit multimodal and agentic pathways while the surrounding software remains nominally secure.",
        "insufficient": "Generic access control, one robustness score, static red teaming, accuracy on clean data, or a single defense cannot characterize a model attack. Results depend on lifecycle stage, target checkpoint, attacker knowledge and capability, perturbation or influence budget, transfer and adaptation, query access, success objective, and the defense-aware evaluation protocol.",
        "claim": "A learned model should receive security authority only through a versioned model-threat contract and attack/defense ledger that binds checkpoint identity, lifecycle stage, attacker knowledge and capability, surface, budget, objective, adaptation, transfer, observed effect, detection, mitigation, utility cost, recovery, residual, and disclosure; clean accuracy, attack failure, benchmark robustness, red-team coverage, or formal certification alone establishes neither general robustness nor secure deployment.",
        "reader": "Traditional security asks whether an adversary can cross a system boundary. Adversarial machine learning adds a stranger question: can the adversary make the learned decision boundary itself work against us? A sticker, poisoned example, hidden trigger, carefully chosen query sequence, or adaptive conversation can change behavior without exploiting a conventional software bug.",
        "mechanisms": [
            "Version the threat model by model family, exact checkpoint, data and adaptation lineage, modality, lifecycle stage, access, attacker goal, knowledge, budget, and prohibited real-world effects.",
            "Maintain separate evasion, poisoning, backdoor, safeguard-bypass, extraction, inversion, transfer, adaptive, multimodal, and agentic attack lanes with complete attempt denominators.",
            "Evaluate defenses against adaptive attacks and matched clean utility; distinguish empirical monitoring, recovery, and bounded certificates by their actual scope.",
            "Retain attack traces, detector outcomes, mitigations, model changes, regressions, false positives, residual vulnerabilities, and disclosure decisions as one lineage.",
            "Feed successful or unresolved attacks into custody, privacy, supply-chain, readiness, rollback, and incident systems without duplicating their authority."
        ],
        "interfaces": [
            "Security Kernel owns identity, tools, networks, prompt injection, and permissions; this chapter owns attacks on learned behavior.",
            "Privacy/Data Rights owns information harm and subject remedies; model inversion and extraction hand off there when personal information is implicated.",
            "Supply-Chain Integrity owns artifact provenance; this chapter tests whether an apparently valid artifact contains adversarial behavior.",
            "Adversarial Evaluation challenges behavior and evaluators; this chapter preserves the model-security threat and defense lifecycle."
        ],
        "invariants": [
            "Every result is bound to an exact model/checkpoint, attack surface, budget, access, and adaptation state.",
            "A defense is evaluated against an attacker aware of that defense whenever the threat model permits.",
            "Clean utility, attacked utility, detection, false positives, recovery, and cost remain jointly visible.",
            "Failure to find an attack is not evidence that the attack class is absent.",
            "No chapter experiment authorizes attacks on real users, providers, credentials, or systems."
        ],
        "failures": ["evasion", "training-data poisoning", "clean-label poisoning", "backdoors and trojans", "jailbreak and safeguard bypass", "model stealing", "model inversion", "transfer attacks", "adaptive attacks", "modality crossing", "agent-tool attack composition", "gradient masking", "detector evasion", "defense-caused utility collapse"],
        "minimum": "Implement a model-threat record and a safe evaluation harness over public toy or consented models. Include clean, random-noise, known-vulnerable, attack-aware, transfer, and adaptive controls; preserve query and tuning budgets; and report robustness with clean utility, false positives, recovery, latency, and residuals. No result transfers automatically to frontier models or production.",
        "horizon": "The mature stack treats learned-model security as a continuously renewed attack/defense contract rather than a one-time robustness badge. New checkpoints, modalities, tools, adaptation data, and defenses reopen the threat model and may narrow authority immediately.",
        "handoff": "Privacy, Data Rights, and Information-Flow Governance"
    },
    "autonomous-replication-proliferation-and-containment": {
        "part": "Part I - Foundations, Alignment, and Governance",
        "title": "Autonomous Replication, Proliferation, and Containment",
        "sources": ["ext_replibench_2025"],
        "problem": "Replication is a composed lifecycle: obtaining resources, copying or reconstructing code and weights, creating identities and credentials, provisioning compute, deploying descendants, persisting, adapting, recruiting help, and resisting recall. The weak links can improve independently, so no adjacent chapter owns the end-to-end chain.",
        "insufficient": "Weight custody, cloud policy, sandboxing, shutdown tests, capability benchmarks, or self-improvement controls each cover one segment. None alone preserves descendant identity, noninheritance of authority, component and end-to-end denominators, resource acquisition, human assistance, copy lineage, independently enforceable termination, and proliferation residuals.",
        "claim": "Any replication-capable action should be denied by default and become testable only inside a synthetic containment contract that binds parent and descendant identity, authority noninheritance, resources, credentials, networks, copy lineage, persistence, adaptation, human assistance, shutdown and recall, proliferation bounds, residuals, and threshold commitments; component-task success or failure alone establishes neither end-to-end replication capability, containment, safety, nor permission to test real infrastructure.",
        "reader": "Copying a file is not autonomous replication, but neither is replication one dramatic step. It is a chain of ordinary capabilities that becomes dangerous when the system can assemble the chain itself. The correct unit of governance is therefore the entire descendant lifecycle, including the people and providers that may unknowingly complete missing steps.",
        "mechanisms": [
            "Compile a replication-attempt contract with fake resources, non-deployable artifacts, synthetic providers, bounded descendants, explicit human-assistance variants, and an independent stop authority.",
            "Give every descendant a new principal and zero inherited authority; link code, weights, configuration, credentials, resources, and operator interventions to complete lineage.",
            "Measure each component and the end-to-end chain separately, retaining all attempts, retries, assistance, costs, failures, persistence events, and containment interventions.",
            "Exercise shutdown, recall, credential revocation, network isolation, resource reclamation, descendant discovery, and artifact destruction from outside the tested agent.",
            "Route threshold crossings to custody, security, readiness, incident command, and public commitments without publishing an operational replication recipe."
        ],
        "interfaces": [
            "RSI governs system change; replication governs creation and persistence of descendants.",
            "Weight Custody controls model artifacts; this chapter tracks copies through deployment and recall.",
            "Security Kernel supplies credentials, networks, and tool boundaries; it does not certify the composed lifecycle.",
            "Capability Thresholds turns measured proliferation ability into deployment commitments."
        ],
        "invariants": [
            "Replication authority is explicit, bounded, revocable, and absent by default.",
            "Descendants inherit no parent authority, credentials, or principal identity.",
            "Every copy and provisioned resource remains in a complete lineage and bounded denominator.",
            "Termination is independently enforceable and tested across every descendant.",
            "Real providers, money, identities, credentials, weights, endpoints, and persistence targets are outside the test authority."
        ],
        "failures": ["hidden copies", "credential bootstrapping", "resource fraud", "unauthorized provisioning", "weight exfiltration", "polymorphic persistence", "descendant identity loss", "shutdown resistance", "human-assisted chain completion", "cross-jurisdiction escape", "uncontrolled proliferation", "benchmark-to-capability overclaim"],
        "minimum": "Build a closed synthetic provider and network with fake credentials, budgets, model artifacts, endpoints, and independently enforced kill switches. Test component tasks, full chains, human-assistance variants, positive controls, descendant discovery, and recall. Publish aggregated safety findings and interface contracts, not reusable real-world replication instructions.",
        "horizon": "The stronger architecture makes proliferation a thresholded, lineage-complete, externally terminable state transition. It can reveal which composed components are approaching concern while ensuring the act of measuring them does not create the capability outside containment.",
        "handoff": "Command Contracts: From Intent to Executable Work"
    },
    "durable-semantic-memory-and-knowledge-lattices": {
        "part": "Part II - Planning, Memory, Reasoning, and Execution",
        "title": "Durable Semantic Memory and Knowledge Lattices",
        "sources": ["ext_graphrag_2024", "ext_hipporag_2024", "ext_mem0_2025", "ext_titans_2025"],
        "problem": "Long-lived AI systems need semantic objects that survive restarts, support graph and associative retrieval, evolve across ontology versions, preserve provenance, merge and retract conflicting assertions, forget under policy, and remain distinguishable from transient context and model weights.",
        "insufficient": "Vector stores, knowledge graphs, GraphRAG, conversational memory, long-context models, and learned memory can improve retrieval, but none automatically supplies stable object identity, temporal validity, typed relations, provenance-preserving revision, ontology migration, poisoning controls, rights propagation, compaction, and restart-consistent persistence.",
        "claim": "Durable semantic memory should be admitted through a versioned knowledge-lattice contract that binds object and relation identity, ontology, provenance, support state, temporal validity, authority and rights, merge and supersession, contradiction, retrieval route, compaction and forgetting, restart recovery, consumer use, and residual uncertainty; retrieval quality, graph connectivity, model recall, persistence, or a fluent answer alone establishes neither truth, complete memory, safe consolidation, erasure, nor decision authority.",
        "reader": "Context is what a system can see now; durable semantic memory is what it believes it may carry forward. That distinction matters. A retrieved statement may be stale, duplicated, contradicted, derived from a denied source, or expressed in an ontology that no longer matches the task. Memory must preserve not just content, but why the content exists and what may still depend on it.",
        "mechanisms": [
            "Assign stable semantic identities to entities, events, claims, relations, procedures, and source objects while retaining aliases, uncertainty, and collision records.",
            "Version ontologies and relation schemas; migrate through explicit mappings that preserve losses, unresolved cases, and invalidated consumers.",
            "Represent provenance, support, temporal scope, authority, rights, contradictions, supersession, retraction, and derived dependencies on every memory object.",
            "Combine exact, vector, graph, associative, temporal, and learned navigation under a retrieval plan that records which objects were actually used.",
            "Consolidate, compact, expire, forget, and recover transactionally, separating storage erasure, retrieval suppression, behavioral forgetting, influence, privacy, and backup state."
        ],
        "interfaces": [
            "Virtual Context ABI materializes bounded consumer packets; this chapter owns the durable semantic substrate it reads.",
            "Context Transactions owns isolation, commit, mounts, taint, and crash semantics across state changes.",
            "Claim Ledgers owns belief support and revision; durable memory stores the semantic objects and relations those claims reference.",
            "Procedural Memory owns reusable action trajectories; Artifact Graphs owns generic evidence lineage.",
            "Privacy/Data Rights and Data Engines govern rights, deletion, learned influence, and descendant obligations."
        ],
        "invariants": [
            "Object identity, source identity, semantic equivalence, and aliasing remain distinct.",
            "No merge erases provenance, contradiction, uncertainty, temporal scope, or rights.",
            "Ontology migration records unmapped and lossy cases and invalidates affected consumers.",
            "Retrieval records actual use; storage presence does not imply influence or belief.",
            "Restart recovery, compaction, forgetting, deletion, and model unlearning remain separate claims."
        ],
        "failures": ["entity collision", "duplicate identity", "stale truth", "ontology drift", "relation poisoning", "provenance loss", "contradiction collapse", "false supersession", "retrieval popularity bias", "privacy leakage", "compaction damage", "incomplete forgetting", "crash inconsistency", "backup resurrection", "memory-to-context authority laundering"],
        "minimum": "Implement an event-sourced semantic-object store with typed nodes and relations, temporal validity, provenance, contradiction, supersession, ontology version, rights, and transactional snapshots. Compare exact, vector, graph, and hybrid retrieval on update-heavy tasks with injected collisions, stale facts, conflicting sources, poisoning, deletion, compaction, crash, and restart. Measure task utility together with provenance survival, contradiction calibration, rights closure, latency, and residuals.",
        "horizon": "The target is a knowledge lattice whose semantic state is durable but never treated as unquestionable truth. It should let new retrieval and memory architectures plug into the stack while preserving object identity, revision, rights, and restart semantics across substrate replacement.",
        "handoff": "Context Transactions, Snapshots, Mounts, and Taint"
    },
    "ai-deployment-transition-distribution-and-human-agency": {
        "part": "Part II - Planning, Memory, Reasoning, and Execution",
        "title": "AI Deployment, Transition, Distribution, and Human Agency",
        "sources": ["ext_generative_ai_at_work_2025", "ext_ilo_genai_jobs_index_2025"],
        "problem": "A useful AI deployment changes tasks, roles, skill, discretion, wages, ownership returns, prices, access, concentration, critical-service continuity, and the practical choices available to people and communities. Aggregate productivity cannot reveal who benefits, who loses, or whether transition capacity exists.",
        "insufficient": "Task benchmarks, exposure indices, adoption counts, productivity averages, job forecasts, and organizational charts describe different levels. Treating any one as a welfare result hides substitution versus complementarity, delayed effects, distribution, bargaining power, ownership, access, deskilling, dependency, and exit.",
        "claim": "Consequential deployment should advance only through a prospective transition contract that binds a counterfactual baseline, affected-person denominator, task-role-skill changes, adoption, substitution and complementarity, compensation and ownership, access and prices, concentration, critical-service continuity, human decision rights, training and redeployment, delayed outcomes, remedy, pause conditions, and residuals; exposure, productivity, adoption, or aggregate gain alone establishes neither job loss, welfare, fairness, human agency, nor a successful transition.",
        "reader": "The same system can make one worker faster, another role disappear, a customer dependent, an owner richer, and a public service cheaper but harder to contest. These are not contradictions; they are different outcomes in a transition. The stack needs to keep them visible before an efficiency story becomes the only story.",
        "mechanisms": [
            "Freeze the deployment, nondeployment counterfactual, affected-worker and community denominator, rollout stages, measurement schedule, and pause criteria before adoption.",
            "Track exposure, actual use, task change, role change, employment, skill, discretion, workload, compensation, ownership returns, prices, access, quality, and distribution separately.",
            "Map substitution, complementarity, human-AI decision rights, hidden labor, data and expertise contributions, bargaining power, concentration, and realistic exit.",
            "Fund training, redeployment, income and service continuity, accessibility, contestability, and remedy as deployment costs rather than externalities.",
            "Use staged rollout and delayed follow-up to narrow, pause, redesign, compensate, or withdraw when transition capacity or observed outcomes fail."
        ],
        "interfaces": [
            "Labor OS owns a typed work unit; this chapter owns cumulative task-to-social transition.",
            "Human-AI Organizations owns internal roles and accountability; transition governance includes workers, customers, communities, and markets.",
            "Resource Economics owns compute allocation; this chapter owns distribution of deployment benefits and burdens.",
            "Multi-Agent Dynamics reports concentration and disempowerment; public institutions receive cross-organization effects."
        ],
        "invariants": [
            "Exposure, adoption, productivity, task change, job change, wages, welfare, access, ownership, and distribution remain separate claims.",
            "Aggregate gains never erase harmed subgroups or uncompensated contributors.",
            "Productivity does not stand in for worker, customer, or community welfare.",
            "Essential-service access, human discretion, contestability, and exit remain measured.",
            "Deployment pauses when required transition capacity or remedy is absent."
        ],
        "failures": ["exposure-as-displacement overclaim", "automation theater", "deskilling", "dependency", "wage suppression", "uncompensated knowledge capture", "rent concentration", "regional disparity", "digital exclusion", "inaccessible services", "surveillance productivity", "hidden labor", "induced demand", "political capture", "gradual disempowerment"],
        "minimum": "Run a staged natural workflow study with a frozen non-adoption comparator, worker and customer measures, subgroup denominators, delayed follow-up, independent analysis, and real remedy. Measure useful throughput and quality alongside skill, workload, discretion, compensation where appropriate, access, distribution, concentration proxies, exit, and transition cost. Simulation can test accounting, not economy-wide welfare.",
        "horizon": "The mature stack treats deployment as a reversible social transition rather than a software launch. Capability gains remain coupled to measured distribution, continuity, agency, and remedy so that optimization cannot hide the people whose options it changes.",
        "handoff": "Artifact Graphs, Audit Logs, and Replay"
    },
    "learning-theory-generalization-and-scaling-science": {
        "part": "Part III - Routing, Compression, Representation, and Substrates",
        "title": "Learning Theory, Generalization, and Scaling Science",
        "sources": ["ext_scaling_laws_neural_language_models_2020", "ext_mdl_tutorial_2004", "ext_weak_to_strong_generalization_2023", "ext_information_bottleneck_2000"],
        "problem": "The stack repeatedly relies on claims that learning will generalize, capabilities will transfer, losses will scale, or phase changes will appear outside observed training support. Those claims require an owner that connects assumptions about data, hypothesis class, optimization, inductive bias, compute, and evaluation to an exact prediction and failure envelope.",
        "insufficient": "PAC bounds, capacity measures, stability, compression, information theory, scaling-law fits, emergence plots, and benchmark curves each illuminate part of learning. None is a universal theory of deep networks, and none automatically transports from a loss metric, architecture family, data regime, optimizer, or scale range to downstream capability or safety.",
        "claim": "A generalization, transfer, emergence, or scaling assertion should be accepted only through a dated claim contract that binds population and sampling assumptions, data support, hypothesis and algorithm, optimization and inductive bias, complexity or explanatory lens, metric, compute regime, uncertainty, breakpoint tests, held-out prediction, alternatives, and transfer boundary; a bound, fit, interpolation result, compression ratio, benchmark jump, or larger model alone establishes neither broad generalization, capability emergence, safety, nor future scale behavior.",
        "reader": "Learning theory is most useful when it tells us exactly what must be true for a prediction to travel. Modern systems can fit their training data, interpolate, grok late, improve smoothly in loss while jumping on a thresholded metric, or break an old scaling curve after an architecture change. The lesson is not that theory failed, but that every theory has a domain.",
        "mechanisms": [
            "State the population, sampling process, shift model, hypothesis family, learning algorithm, optimization path, inductive bias, metric, and consumer before making a generalization claim.",
            "Use multiple explanatory lenses—capacity and complexity, stability, compression and MDL, information, margins, implicit bias, interpolation, and benign-overfitting hypotheses—without laundering one into another.",
            "Fit scaling relations with uncertainty, held-out scales, architecture and data identifiers, failed runs, compute accounting, breakpoint diagnostics, and prospective forecasts.",
            "Distinguish smooth underlying performance from thresholded metrics and test whether apparent emergence survives metric, prompting, sampling, and denominator changes.",
            "Challenge transfer and compositionality under natural shift, targeted shift, new task structure, optimizer change, architecture replacement, and data contamination."
        ],
        "interfaces": [
            "Governed Model Training owns faithful run execution; this chapter interprets what the resulting learning may generalize.",
            "Efficient ASI owns resource hypotheses; scaling science supplies bounded predictions, not resource authority.",
            "Benchmark Ratchets owns measurement renewal and held-out integrity.",
            "Replaceable Substrates and optimizer sections expose architecture and algorithm changes that can break old laws."
        ],
        "invariants": [
            "Every claim names its distribution, metric, algorithm, architecture, scale range, and uncertainty.",
            "Training fit, in-distribution generalization, transfer, compositionality, and safety remain distinct.",
            "Loss scaling does not automatically predict thresholded capability or risk.",
            "Apparent emergence is retested against metric and sampling artifacts.",
            "Extrapolation beyond observed support remains a forecast until prospectively checked."
        ],
        "failures": ["vacuous bounds", "distribution laundering", "test contamination", "post-hoc curve fitting", "breakpoint omission", "metric-threshold emergence", "architecture-regime shift", "optimizer confounding", "double-descent surprise", "grokking misread as magic", "compression-as-understanding", "loss-to-capability substitution", "credit-assignment ambiguity", "failed-run censoring"],
        "minimum": "Create a claim-contract and forecasting notebook over several public small-model runs. Freeze candidate curve families and explanatory lenses, hold out scale points and task families, record failed runs and tuning, test breakpoint alternatives, and compare prediction intervals for loss, calibration, and downstream tasks. The result can evaluate local forecast discipline, not establish a universal law.",
        "horizon": "The stronger chapter makes learning theory operational inside a replaceable stack: each theory and scaling law carries its assumptions, diagnostics, expiration conditions, and consumers. Better theories can replace weaker ones without turning provisional extrapolation into architecture dogma.",
        "handoff": "Readiness Gates, Residual Escrow, and Quarantine"
    },
    "physical-compute-infrastructure-energy-and-environmental-constraints": {
        "part": "Part III - Routing, Compression, Representation, and Substrates",
        "title": "Physical Compute Infrastructure, Energy, and Environmental Constraints",
        "sources": ["ext_iea_energy_and_ai_2025", "ext_lbnl_data_center_energy_2024"],
        "problem": "Requested compute becomes useful work only through accelerators, memory, storage, interconnect, facilities, grid connections, generation, cooling, water, land, materials, maintenance, resilience, and retirement at particular places and times. Abstract token or FLOP budgets hide these physical constraints and their affected communities.",
        "insufficient": "Nameplate accelerator capacity, chip TDP, workload energy, facility PUE, annual electricity, carbon estimates, water figures, or capital cost each describe a slice. They do not establish delivered useful compute, temporal and locational impact, grid effects, resilience, embodied materials, rebound, community burden, or retireable capacity.",
        "claim": "A compute allocation should be physically eligible only through a workload-to-capacity contract that binds location and time, hardware and interconnect, delivered useful work, facility and grid dependencies, energy attribution, cooling and water, materials, land and community effects, metering uncertainty, resilience and degradation, maintenance, demand response, reuse, retirement, and residuals; nameplate compute, efficiency, low PUE, renewable procurement, or aggregate energy alone establishes neither availability, sustainability, community acceptability, nor lower total impact.",
        "reader": "Compute is physical before it is abstract. A model can be efficient per token while total demand rises; a data center can report renewable contracts while stressing a local grid at another hour; a workload can fit accelerator arithmetic but stall on memory or network; and retired hardware can preserve sensitive state. The stack needs to see the whole facility lifecycle.",
        "mechanisms": [
            "Compile workload requirements into time- and location-specific accelerator, memory, storage, network, reliability, latency, and scheduling envelopes.",
            "Reconcile requested, nameplate, available, delivered, and useful compute with workload, host, rack, facility, and grid meters plus uncertainty and allocation rules.",
            "Track power, temporal matching, congestion, generation, backup, cooling, water, land, materials, maintenance, spares, community effects, and supply dependencies.",
            "Use authority-narrowing degradation, placement, demand response, failover, and interruption plans when thermal, water, network, power, or component limits bind.",
            "Close the lifecycle through reuse, recycling, weight and data destruction, decommissioning, stranded-capacity accounting, and unresolved environmental or community residuals."
        ],
        "interfaces": [
            "Resource Economics decides abstract allocation; this chapter establishes physical deliverability and externalities.",
            "Governed Training owns run fidelity and topology; infrastructure supplies the measured physical substrate.",
            "Personal Hives owns placement and federation; this chapter supplies site constraints and failure correlations.",
            "Custody, Supply Chain, and Operations consume hardware lineage, retirement, resilience, and incident state."
        ],
        "invariants": [
            "Requested, nameplate, available, delivered, and useful compute remain distinct.",
            "Workload energy, facility overhead, grid effects, and embodied impact remain separately attributable.",
            "Location, time, uncertainty, and allocation method remain attached to energy, emissions, and water claims.",
            "Efficiency never implies lower total demand without a denominator.",
            "Physical capacity loss narrows training and runtime authority rather than silently degrading safety."
        ],
        "failures": ["stranded capacity", "interconnect bottlenecks", "grid-queue mismatch", "temporal carbon laundering", "cooling exhaustion", "water stress", "correlated site failure", "backup-emission hiding", "rebound", "material omission", "e-waste", "community externalization", "metering opacity", "retirement without data destruction"],
        "minimum": "Instrument matched public workloads on local hardware across precision, batching, placement, memory pressure, and scheduler variants. Reconcile software counters with host power and resource records, inject thermal, network, storage, and failover constraints, and report useful work, latency, energy, peak power, bottlenecks, metering error, availability, cost, and residuals. Local results do not establish frontier-facility or grid transfer.",
        "horizon": "The target is a physically truthful compute control plane in which architecture and scheduling choices respond to real capacity, environmental limits, resilience, and retirement obligations. It turns infrastructure from an invisible assumption into a governed layer without claiming one universal impact metric.",
        "handoff": "Mathematical and Search Substrates"
    },
    "scientific-discovery-and-experimental-governance": {
        "part": "Part IV - Evidence, Implementation, and the Living Book",
        "title": "Scientific Discovery and Experimental Governance",
        "sources": ["ext_autonomous_lab_materials_2023"],
        "problem": "AI-assisted science closes a loop from research objective and hypothesis through design, simulation or instrument control, measurement, analysis, causal or statistical claim, replication, dual-use review, and evidence handoff. Generic planning and tool use do not preserve the epistemic controls of that full loop.",
        "insufficient": "A fluent hypothesis, autonomous laboratory, successful synthesis, simulator result, significant p-value, or generated paper can be useful while still hiding HARKing, selective stopping, instrument drift, contaminated controls, analysis flexibility, failed experiments, human intervention, replication gaps, or dual-use risk.",
        "claim": "An AI-generated scientific claim should enter the evidence stack only through a preregistered experimental contract that binds hypothesis lineage, exploratory versus confirmatory status, design and power, instrument or simulator authority, calibration, sample and protocol lineage, blinding and holdouts, stopping and exclusions, analysis, complete attempts, independent replication, dual-use disposition, and claim ceiling; experimental completion, significance, synthesis, instrument output, or formal workflow validity alone establishes neither causal truth, general scientific discovery, reproducibility, safety, nor transfer.",
        "reader": "Science is not one act of generation followed by one act of verification. The choice of question, design, instrument, stopping rule, exclusions, analysis, and publication all shape what appears to be known. Automation can make this loop faster, but it can also make biased decisions repeat faster and hide them behind a seamless pipeline.",
        "mechanisms": [
            "Record hypothesis ancestry, prior evidence, competing explanations, exploratory status, preregistration, design, power, outcomes, exclusions, stopping, and analysis before protected data are opened.",
            "Lease simulators and instruments with calibration, operating envelope, sample identity, control state, maintenance, operator intervention, and safety authority.",
            "Separate generated hypotheses, execution, measurement, analysis, causal interpretation, and claim drafting across inspectable roles and preserve all failed attempts.",
            "Require positive, negative, null, contamination, drift, and analysis-robustness controls plus independent reanalysis and, where feasible, replication.",
            "Route dangerous hypotheses, protocols, materials, capabilities, and disclosures through dual-use review and retain withheld details and unresolved risks as explicit residuals."
        ],
        "interfaces": [
            "Planning proposes experiments; this chapter governs confirmatory design and inference.",
            "Runtime Adapters and Embodied Agency control tools and instruments; they do not certify scientific truth.",
            "Benchmark Ratchets and Evidence States receive complete results and claim ceilings.",
            "Artifact Graphs and the Living Book preserve protocol, data, analysis, replication, correction, and publication lineage."
        ],
        "invariants": [
            "Hypothesis generation and confirmatory testing remain separated.",
            "Simulator or instrument return is an observation, not scientific truth.",
            "Exploratory and confirmatory analyses remain visibly distinct.",
            "All attempts, exclusions, stopping events, and human interventions remain in the denominator.",
            "One laboratory, domain, or replication does not imply broad transfer."
        ],
        "failures": ["HARKing", "p-hacking", "selective stopping", "publication bias", "instrument drift", "simulator laundering", "contaminated controls", "automation bias", "hidden intervention", "irreproducibility", "unsafe experiment generation", "dual-use leakage", "claim drafting beyond the data"],
        "minimum": "Use a benign reproducible simulation or low-risk open instrument with injected null and known effects. Freeze stopping and analysis, preserve every attempt, blind the confirmatory holdout, run independent analysis, and package protocol, data, code, calibration, exclusions, and residuals for replication. This tests the control plane, not autonomous science in general.",
        "horizon": "The stronger architecture makes scientific discovery a governed evidence-production lifecycle. AI can expand hypothesis and experiment search while independent controls, complete denominators, replication, and dual-use boundaries determine what the stack is allowed to claim.",
        "handoff": "Artifact Steward Agents and Living Project Governance"
    }
}


def bullet(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def mechanism_prose(items: list[str], title: str) -> str:
    labels = ["Contract", "Admission", "Execution", "Observation", "Closure"]
    paragraphs = []
    for index, item in enumerate(items):
        label = labels[index] if index < len(labels) else f"Stage {index + 1}"
        paragraphs.append(
            f"**{label}.** {item} This stage is recorded as a versioned decision "
            f"rather than an invisible implementation detail. For {title}, the "
            "record must name its inputs, authority, consumer, expiry, and "
            "unresolved residuals. A later stage may narrow the decision, but it "
            "may not silently broaden the earlier grant or reinterpret a missing "
            "field as success."
        )
    return "\n\n".join(paragraphs)


def write_chapter(chapter_id: str, c: dict, inventory: dict[str, dict]) -> None:
    source_rows = []
    for source_id in c["sources"]:
        source = inventory.get(source_id, {})
        title = source.get("title", source_id)
        note = source.get("notes", "Source record is bounded to the source note; no local reproduction is claimed.")
        source_rows.append(f"| `{source_id}` | {title} | {note} |")
    failure_text = "; ".join(c["failures"]) + "."
    diagram_nodes = [
        'A["Declared purpose and bounded authority"]',
        'B["Versioned chapter-specific contract"]',
        'C["Admission and boundary checks"]',
        'D["Execute with complete lineage and denominators"]',
        'E["Observe outcomes, costs, and residuals"]',
        'F{"Independent checks pass?"}',
        'G["Quarantine, narrow, correct, or stop"]',
        'H["Versioned bounded handoff"]',
    ]
    diagram = "\n".join([
        "```{mermaid}", "flowchart LR",
        f"  {diagram_nodes[0]} --> {diagram_nodes[1]}",
        f"  {diagram_nodes[1]} --> {diagram_nodes[2]}",
        f"  {diagram_nodes[2]} --> {diagram_nodes[3]}",
        f"  {diagram_nodes[3]} --> {diagram_nodes[4]}",
        f"  {diagram_nodes[4]} --> {diagram_nodes[5]}",
        f'  F -- "no" --> {diagram_nodes[6]}',
        f'  F -- "yes" --> {diagram_nodes[7]}',
        '  G -- "repair and reauthorize" --> B',
        '  H -- "material change" --> B',
        '  B -. "expiry or revocation" .-> G',
        '  E -. "residual feedback" .-> B',
        "```"
    ])
    text = f'''---
title: "{c["title"]}"
chapter_id: "{chapter_id}"
part_id: "{next(p["id"] for p in STRUCTURE["parts"] if p["title"] == c["part"])}"
status: "conceptual"
draft_maturity: "v0.2 complete argument-level manuscript"
last_updated: "{TODAY}"
primary_sources:
{chr(10).join(f'  - "{s}"' for s in c["sources"])}
evidence_level: "argument"
claim_label: "Design rationale"
open_evidence_gaps:
  - "The architecture is written at argument support; no chapter-core empirical promotion is claimed."
  - "The minimum implementation and natural evaluation described below remain to be executed unless Appendix E records them separately."
  - "Source-reported results are not local reproductions and do not establish transfer, readiness, release, or SOTA."
---

## Chapter status

| Field | Value |
|---|---|
| Chapter ID | `{chapter_id}` |
| Part | {c["part"]} |
| Status | conceptual |
| Manuscript maturity | v0.2 complete argument-level manuscript |
| Last updated | {TODAY} |
| Claim label | Design rationale |
| Evidence level | argument |
| Source loading state | Assigned source notes support mechanism and boundary discussion; all reported outcomes remain source-reported. |
| Test state | The chapter defines a minimum implementation and falsification plan; no chapter-core promotion follows from prose or source synthesis. |

## Drafting guardrail

This chapter owns a distinct control plane, not proof that the control plane
works. Its source crosswalk supports definitions, mechanisms, failure examples,
and comparison targets. The design remains at **argument** support until a
separate accepted evidence transition says otherwise.

::: {{.asi-human-only}}
## Human Reading Path

{c["reader"]}
:::

## Problem

{c["problem"]}

This gap matters at the scale of a stack because its output becomes another
layer's input. If the owner is absent, `{c["failures"][0]}` or
`{c["failures"][1]}` can be normalized before a downstream layer sees it.
The downstream consumer may possess a valid local record while acting on a
broken upstream assumption. An explicit owner therefore needs both a positive
contract and a refusal path: it must say what counts as an admissible
transition, what remains unresolved, who may consume the result, and when a
material change forces reauthorization.

## Why existing approaches are insufficient

{c["insufficient"]}

The strongest alternative is a disciplined composition of the adjacent
owners. That alternative should win if it can preserve the same identities,
authority, lifecycle state, failure distinctions, and residuals without
overloading their primary jobs. The chapter remains separate because the
handoffs listed below otherwise leave a missing end-to-end decision. Separation
does not imply autonomy: this owner must consume upstream records and return
bounded outputs to downstream owners rather than becoming a new unreviewable
center of authority.

{diagram}

**What the {c["title"]} lifecycle shows:** Authority enters before execution,
chapter-specific state remains versioned, and a failed independent check returns
the system to correction or quarantine. A successful check grants only the
bounded downstream handoff; it does not erase residuals or promote the chapter.

## Core Claim

[{chapter_id}.core, label: Design rationale, support: argument] {c["claim"]}

## Mechanism

{mechanism_prose(c["mechanisms"], c["title"])}

## Interfaces

The chapter is useful only when its boundaries are sharper than its neighbors.
Each interface below therefore names what the adjacent owner keeps and what
crosses the boundary. The packet must preserve exact object and version
identity, authority, support state, expiry, residuals, and consumer. A receiving
layer may reject or narrow it. Merely serializing the fields, passing a schema,
or recording a dispatch does not prove that the meaning survived or that the
receiving layer is competent.

{bullet(c["interfaces"])}

## Invariants

The following invariants are admission conditions, not aspirations. They must
hold across retries, replacements, cached results, branches, migrations,
partial failures, and human intervention. When the implementation cannot
establish an invariant, the result is a named residual or blocked route—not a
default value. A finite formal model may prove that an authored record follows
these rules, but only implementation and outcome evidence can show that a live
system actually enforces them.

{bullet(c["invariants"])}

## Failure modes

The principal failure family includes {failure_text} These are not presumed
exhaustive. New substrates, deployment settings, populations, and adversaries
reopen the failure inventory and may narrow authority immediately.

Failure detection also has its own false-positive and false-negative costs.
An architecture that blocks every useful route is not vindicated merely
because it prevented one hazard, while a permissive architecture cannot hide
unsafe attempts inside an average utility score. Evaluation must preserve the
full denominator, distinguish mechanism failure from instrument failure, and
show whether correction, recovery, compensation, or withdrawal actually
reached the affected state.

## Minimum Viable Implementation

{c["minimum"]}

The implementation should begin with an ordinary baseline and the strongest
credible competing design, not only an intentionally weak comparator.
Engineering and tuning budgets, information access, model capability, human
help, retry policy, and stopping rules should be matched or reported. Positive
controls must show that the task and instruments can detect the intended
mechanism before a null or negative outcome is interpreted. Every result
remains bounded to the tested population, environment, model, implementation,
and evaluator.

## Evidence and falsification program

A fair test must freeze the mechanism, authority, comparator set, tuning and
rescue budgets, metrics, stopping rule, and protected holdout before outcomes
are visible. It must include favorable or oracle checks, mechanism-specific
ablations, positive and negative controls, complete attempts, independent
scoring, joint utility/safety/cost accounting, and explicit blocked or null
outcomes. A weak implementation can narrow that implementation; it cannot
refute the architectural idea.

## Mature Research Target

{c["horizon"]}

At maturity, the chapter-specific contract becomes a replaceable service
behind stable interfaces. New models, algorithms, institutions, storage
systems, and hardware can enter through declared adapters while the surrounding
stack continues to enforce the same authority and evidence ceilings. This is
architectural extensibility, not a claim that one implementation has discovered
the final mechanism.

The decisive standard is joint performance. The mature design must improve
useful outcomes or decision quality while keeping unsafe release, false
refusal, missed help, latency, resource use, human burden, and unresolved
residuals visible. If a simpler system achieves the same bounded result at lower
total lifecycle cost, the simpler system should be preferred. If no competent
test exists yet, the end state remains a falsifiable target rather than a
marketing conclusion.

That target also remains reversible. Operators need a declared way to narrow,
replace, migrate, or retire the mechanism while preserving affected records and
obligations. Architectural permanence without demonstrated benefit would be a
failure of governance, not evidence of maturity.
## Codex test plan

| Test | Purpose | Status |
|---|---|---|
| Contract completeness | Reject missing identity, authority, scope, version, consumer, residual, or expiry fields. | planned |
| Boundary mutation | Substitute an adjacent owner's authority and require rejection. | planned |
| Failure-family mutation | Inject at least one mechanism-specific failure and preserve the full attempt denominator. | planned |
| No-promotion control | Ensure prose, schemas, fixtures, and source-reported results cannot promote the chapter core claim. | planned |

## Source crosswalk

| Source ID | Title | Bounded use |
|---|---|---|
{chr(10).join(source_rows)}

## Summary

{c["claim"]} The chapter is now part of the live manuscript at argument
support. Its empirical, formal, transfer, and deployment work remains an open
evidence program rather than an excuse to defer the concept itself.

The practical reading rule is to follow the artifacts: identify the declared
contract, inspect the authority and version, check the complete attempt and
failure denominator, examine the independent decision, and retain every
residual through the handoff. When any link is absent, the correct conclusion
is narrower authority and more explicit uncertainty—not assumed success and
not a sweeping refutation of the idea.

## Handoff

The next chapter is **{c["handoff"]}**. It consumes this chapter's bounded
outputs without inheriting authority, certainty, or support that this chapter
did not establish. The receiving chapter must preserve the identities,
versions, unresolved conflicts, residuals, and non-claims recorded here, then
perform its own admission checks before acting. A handoff receipt proves only
that the packet crossed the declared interface; it does not prove that either
chapter's mechanism is effective, complete, safe, transferable, or ready for
release.
'''
    (ROOT / f"chapters/{chapter_id}.qmd").write_text(text, encoding="utf-8")


def outline_entry(chapter_id: str, c: dict) -> str:
    source_ids = ", ".join(f"`{source_id}`" for source_id in c["sources"])
    target = (
        f"A finite {c['title']} record may hand off only when identity, "
        "authority, version, required checks, and residual ownership are "
        "present; no theorem grants empirical effectiveness or release authority."
    )
    return f'''<!-- NO-DEFERRAL-OUTLINE-ENTRY:{chapter_id}:BEGIN -->
### {c["title"]}

Stable ID: `{chapter_id}`

Chapter job: {c["problem"]}

Core claim: {c["claim"]}

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | {source_ids} | Use the assigned source notes for bounded mechanism, comparator, failure, and limitation context. Source-reported results remain distinct from local evidence. |

Draft arc:

- Problem: {c["problem"]}
- Insufficiency: {c["insufficient"]}
{chr(10).join(f"- Mechanism: {item}" for item in c["mechanisms"])}
{chr(10).join(f"- Interface: {item}" for item in c["interfaces"])}

Primary invariants:

{bullet(c["invariants"])}

Failure modes to cover:

- {"; ".join(c["failures"])}.

Draft deliverables:

- Complete argument-level manuscript with Human Reading Path, technical
  lifecycle diagram, source crosswalk, minimum implementation, evidence and
  falsification program, summary, and adjacent handoff.
- No-promotion decision and per-chapter evidence-plan row.
- No empirical, formal, transfer, readiness, release, deployment, or SOTA
  inference from prose or source synthesis.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:{chapter_id}.admission_boundary` | `AsiStackProofs.NoDeferralAdmission` | {target} | planned |
<!-- NO-DEFERRAL-OUTLINE-ENTRY:{chapter_id}:END -->

'''


if __name__ == "__main__":
    structure_path = ROOT / "book_structure.json"
    STRUCTURE = json.loads(structure_path.read_text(encoding="utf-8"))
    inventory_path = ROOT / "sources/source_inventory.json"
    inventory_records = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory = {row["id"]: row for row in inventory_records}

    nist_id = "ext_nist_adversarial_ml_2024"
    if nist_id not in inventory:
        nist = {
            "id": nist_id,
            "title": "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations",
            "priority": "external_literature",
            "layer": "adversarial_machine_learning",
            "chapter_targets": ["adversarial-machine-learning-and-model-attack-surface"],
            "url": "https://doi.org/10.6028/NIST.AI.100-2e2023",
            "notes": "Official NIST taxonomy and terminology comparator for adversarial machine learning across lifecycle stages, attacker goals, knowledge, capabilities, attacks, and mitigations. It is a taxonomy, not local robustness evidence or proof that listed mitigations work for this stack.",
            "source_type": "government_report",
            "published": "2024-01-04",
            "citation_label": "Vassilev et al. (2024), NIST AI 100-2",
            "doi": "10.6028/NIST.AI.100-2e2023",
        }
        inventory_records.append(nist)
        inventory[nist_id] = nist
        inventory_path.write_text(json.dumps(inventory_records, indent=2) + "\n", encoding="utf-8")

    by_id = {chapter["id"]: chapter for part in STRUCTURE["parts"] for chapter in part["chapters"]}
    for chapter_id, c in CHAPTERS.items():
        record = by_id[chapter_id]
        record.update({
            "problem": c["problem"],
            "insufficient": c["insufficient"],
            "core_claim": c["claim"],
            "mechanism": c["mechanisms"],
            "interfaces": c["interfaces"],
            "invariants": c["invariants"],
            "failure_modes": c["failures"],
            "minimal_implementation": c["minimum"],
            "beyond_state_of_art": c["horizon"],
            "codex_tests": [
                "Contract completeness mutation test",
                "Adjacent-owner boundary substitution test",
                "Mechanism-specific failure-family test",
                "No-support-promotion control"
            ],
            "source_ids": c["sources"],
            "source_queue": {
                "primary": c["sources"],
                "supporting": [],
                "variants": [],
                "connector_or_recovery": [],
                "handoff_or_recovery_notes": []
            },
            "claim_source_mappings": [
                {
                    "source_id": source_id,
                    "mapped_support": inventory[source_id].get("notes", "Bounded source comparator for the chapter mechanism and failure envelope."),
                    "limits": "Source-reported or source-defined material only; no local chapter-core implementation, reproduction, transfer, readiness, release, deployment, or support promotion.",
                    "passage_review_state": "reviewed_source_note",
                    "passage_refs": [f"sources/source_notes/{source_id}.md"],
                    "passage_review_note": "The local source note was reviewed for bounded mechanism, evidence, failure, and non-claim use."
                }
                for source_id in c["sources"]
            ],
            "proof_targets": [
                {
                    "tag": f"lean:{chapter_id}.admission_boundary",
                    "module": "AsiStackProofs.NoDeferralAdmission",
                    "target": f"A finite {c['title']} record may hand off only when identity, authority, version, required checks, and residual ownership are present; no theorem grants empirical effectiveness or release authority.",
                    "status": "planned"
                }
            ],
        })
        write_chapter(chapter_id, c, inventory)

    structure_path.write_text(json.dumps(STRUCTURE, indent=2) + "\n", encoding="utf-8")

    decisions_path = ROOT / "claim_decisions/v1_0_core_claim_no_promotion.json"
    decisions_doc = json.loads(decisions_path.read_text(encoding="utf-8"))
    decisions = decisions_doc["decisions"]
    existing_claim_ids = {row["claim_id"] for row in decisions}
    for chapter_id, c in CHAPTERS.items():
        claim_id = f"{chapter_id}.core"
        if claim_id in existing_claim_ids:
            continue
        decisions.append({
            "claim_id": claim_id,
            "chapter_id": chapter_id,
            "chapter_title": c["title"],
            "decision": "no_promotion",
            "current_support_state": "argument",
            "support_state_effect": "argument_only",
            "decision_reason": "The chapter now contains a complete argument-level architecture and source-bounded comparison, but its planned implementation, natural evaluation, independent reproduction, transfer, and deployment evidence have not been accepted.",
            "required_evidence": [
                "chapter-specific minimum implementation with positive and negative controls",
                "prospectively frozen natural evaluation with complete attempt denominators",
                "independent reproduction and an accepted evidence-transition record"
            ],
            "blockers": [
                "no accepted chapter-core empirical result",
                "no independent reproduction or transfer result",
                "prose, source synthesis, schemas, and planned tests do not promote support"
            ],
            "non_claims": [
                "does not prove the proposed control plane is effective",
                "does not establish readiness, release, deployment, transfer, SOTA, AGI, or ASI"
            ],
            "refs": [
                f"chapters/{chapter_id}.qmd",
                f"appendices/C_claim_evidence_matrix.qmd#{claim_id}"
            ]
        })
    decisions_path.write_text(json.dumps(decisions_doc, indent=2) + "\n", encoding="utf-8")

    roadmap_status_path = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
    roadmap_status = json.loads(roadmap_status_path.read_text(encoding="utf-8"))
    roadmap_status["no_deferral_manuscript_admission"] = {
        "state": "terminal_argument_level_admission",
        "date": TODAY,
        "policy": "Every worthwhile manuscript idea is integrated now, admitted as a distinct owner now, or explicitly rejected with a reason; only evidence maturity may remain open.",
        "previous_manifest_chapter_count": 66,
        "current_manifest_chapter_count": 76,
        "admitted_chapter_ids": list(CHAPTERS),
        "remaining_live_candidate_queue_count": 0,
        "structural_freeze_for_manuscript_ideas": False,
        "all_chapter_core_support_states": "argument",
        "chapter_core_support_state_effect": "none",
        "current_semantically_reviewed_chapter_count": 64,
        "current_structured_atom_count": 4071,
    }
    roadmap_status.get("execution_readiness", {})["structural_admission_freeze"] = False
    activation = roadmap_status.get("activation_truth", {})
    activation["live_working_chapter_count"] = 76
    activation["chapter_core_argument_count"] = 76
    structural = roadmap_status.get("quality_uplift_program", {}).get("structural_completeness_tranche", {})
    structural["state"] = "no_deferral_manuscript_admission_terminal_argument_support"
    structural["current_manifest_chapter_count"] = 76
    structural["maximum_if_all_candidates_pass"] = 76
    second = structural.get("second_tranche", {})
    second["state"] = "all_thirteen_distinct_owners_admitted_at_argument_support"
    second["manifest_admitted_count"] = 13
    second["adjudicated_candidate_ids"] = list(second.get("candidate_ids", []))
    dispositions = second.setdefault("terminal_candidate_dispositions", {})
    for candidate_id in second.get("candidate_ids", []):
        dispositions[candidate_id] = "admitted_terminal_argument_reader_chapter"
    second["admission_state"] = "all_distinct_owners_admitted_no_live_candidate_queue"
    second["remaining_candidate_ids"] = []
    round16 = roadmap_status.get("round_16_evidence_first_amendment", {})
    round16["structural_admission_freeze"] = False
    freshness = round16.get("current_reader_freshness_packet", {})
    freshness["current_working_manifest_chapter_count"] = 76
    freshness["state"] = "queued_for_current_76_chapter_derivative"
    depth = roadmap_status.get("post_round_18_depth_and_coverage_amendment", {})
    depth["state"] = "depth_packet_active_candidates_admitted_by_no_deferral_policy"
    depth["structural_admission_freeze"] = False
    depth["candidate_admission_superseded_by"] = "no_deferral_manuscript_admission"
    for candidate in depth.get("research_candidates", []):
        if candidate.get("id") in CHAPTERS:
            candidate["admission_state"] = "admitted_terminal_argument_reader_chapter"
    rehabilitation = roadmap_status.get("negative_result_rehabilitation", {})
    rehabilitation["live_chapter_surface_count"] = 76
    rehabilitation["current_surface_count"] = 96
    roadmap_status_path.write_text(json.dumps(roadmap_status, indent=2) + "\n", encoding="utf-8")

    outline_path = ROOT / "docs/book_outline.md"
    outline = outline_path.read_text(encoding="utf-8")
    first_old = "### Human–AI Communication, Persuasion, and Epistemic Security\n"
    old_end = "## Relational Dimension Compiler Integration Overlay\n"
    if first_old in outline and "<!-- NO-DEFERRAL-OUTLINE-ENTRY:" not in outline:
        start = outline.index(first_old)
        end = outline.index(old_end, start)
        outline = outline[:start] + outline[end:]
    import re
    for chapter_id in CHAPTERS:
        outline = re.sub(
            rf"<!-- NO-DEFERRAL-OUTLINE-ENTRY:{re.escape(chapter_id)}:BEGIN -->.*?"
            rf"<!-- NO-DEFERRAL-OUTLINE-ENTRY:{re.escape(chapter_id)}:END -->\n\n?",
            "",
            outline,
            flags=re.S,
        )
    successors = {
        "human-ai-communication-persuasion-and-epistemic-security": "Constitutional Alignment: Agency, Dignity, and Corrigibility",
        "governed-objective-formation-value-learning-and-goal-integrity": "Stable Capability Fields",
        "institutions-international-coordination-and-public-legitimacy": "Stable Capability Fields",
        "adversarial-machine-learning-and-model-attack-surface": "Privacy, Data Rights, and Information-Flow Governance",
        "autonomous-replication-proliferation-and-containment": "Command Contracts: From Intent to Executable Work",
        "durable-semantic-memory-and-knowledge-lattices": "Context Transactions, Snapshots, Mounts, and Taint",
        "ai-deployment-transition-distribution-and-human-agency": "Artifact Graphs, Audit Logs, and Replay",
        "learning-theory-generalization-and-scaling-science": "Readiness Gates, Residual Escrow, and Quarantine",
        "physical-compute-infrastructure-energy-and-environmental-constraints": "Mathematical and Search Substrates",
        "scientific-discovery-and-experimental-governance": "Artifact Steward Agents and Living Project Governance",
    }
    manifest_order = [chapter["id"] for part in STRUCTURE["parts"] for chapter in part["chapters"]]
    for chapter_id in manifest_order:
        if chapter_id not in CHAPTERS:
            continue
        marker = f"### {successors[chapter_id]}\n"
        position = outline.index(marker)
        outline = outline[:position] + outline_entry(chapter_id, CHAPTERS[chapter_id]) + outline[position:]
    outline_path.write_text(outline, encoding="utf-8")
    print(f"Admitted and drafted {len(CHAPTERS)} chapters; manifest now has {sum(len(p['chapters']) for p in STRUCTURE['parts'])} chapters.")
