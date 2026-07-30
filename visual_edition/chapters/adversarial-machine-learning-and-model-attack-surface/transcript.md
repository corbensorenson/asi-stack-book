# Descriptive transcript — Adversarial Machine Learning and the Model Attack Surface

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/adversarial-machine-learning-and-model-attack-surface.html>

Video ID: `asi-video-adversarial-machine-learning-and-model-attack-surface`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:38 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: A learned artifact creates attack surfaces that ordinary application security does not fully own. Attackers can shape training data, perturb inference inputs, implant triggers, adapt to defenses, steal behavior through queries, infer sensitive properties, or exploit multimodal and agentic pathways while the surrounding software remains nominally secure. The tempting shortcut is insufficient: Generic access control, one robustness score, static red teaming, accuracy on clean data, or a single defense cannot characterize a model attack.

## 00:38–01:38 — Operating mechanism

**Visual description.** A labeled before after diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: A learned model should receive security authority only through a versioned model-threat contract and attack/defense ledger that binds checkpoint identity, lifecycle stage, attacker knowledge and capability, surface, budget, objective, adaptation, transfer, observed effect, detection, mitigation, utility cost, recovery, residual, and disclosure; clean accuracy, attack failure, benchmark robustness, red-team coverage, or formal certification alone establishes neither general robustness nor secure deployment. Version the threat model by model family, exact checkpoint, data and adaptation lineage, modality, lifecycle stage, access, attacker goal, knowledge, budget, and prohibited real-world effects. Maintain separate evasion, poisoning, backdoor, safeguard-bypass, extraction, inversion, transfer, adaptive, multimodal, and agentic attack lanes with complete attempt denominators.

## 01:38–02:30 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. Implement a model-threat record and a safe evaluation harness over public toy or consented models. Include clean, random-noise, known-vulnerable, attack-aware, transfer, and adaptive controls; preserve query and tuning budgets; and report robustness with clean utility, false positives, recovery, latency, and residuals. No result transfers automatically to frontier models or production. Maintain separate evasion, poisoning, backdoor, safeguard-bypass, extraction, inversion, transfer, adaptive, multimodal, and agentic attack lanes with complete attempt denominators. Evaluate defenses against adaptive attacks and matched clean utility; distinguish empirical monitoring, recovery, and bounded certificates by their actual scope.

## 02:30–02:46 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. evasion training-data poisoning clean-label poisoning backdoors and trojans The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 02:46–03:30 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. A finite Adversarial Machine Learning and the Model Attack Surface record may hand off only when identity, authority, version, required checks, and residual ownership are present; no theorem grants empirical effectiveness or release authority. A defense is evaluated against an attacker aware of that defense whenever the threat model permits. Clean utility, attacked utility, detection, false positives, recovery, and cost remain jointly visible.

## 03:30–03:58 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 03:58–04:32 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is Privacy, Data Rights, and Information-Flow Governance. It takes responsibility for A system can preserve confidentiality and pass access checks while authorized collection, linkage, inference, memory, training, sharing, retention, or derivatives violate purpose, minimization, privacy expectations, or executable rights.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.
