# Descriptive transcript — Security Kernel and Digital SCIFs

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/security-kernel-and-digital-scifs.html>

Video ID: `asi-video-security-kernel-and-digital-scifs`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:50 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: Tool-using and high-agency AI systems can transform untrusted content into requests over secrets, private facts, identities, memory, model artifacts, tools, networks, files, money, code, and physical or institutional effects across model, runtime, operator, vendor, and descendant trust boundaries. The tempting shortcut is insufficient: Prompt instructions, model-visible secrets, one-time approval, opaque handles, allowlists, software containers, output filters, audit logs, or a Digital SCIF label each cover only part of the threat model; they do not by themselves provide least authority, complete mediation, trustworthy declassification, isolation, revocation, side-channel control, or recovery.

## 00:50–01:34 — Operating mechanism

**Visual description.** A labeled timeline diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: Every privileged information flow or effect should execute as a threat-model-bound authority-use transaction through a non-bypassable reference monitor: bind the exact principal, purpose, operation, target, data and taint scope, budget, time, nonce, evaluator and policy identities; admit only minimized context and capabilities into a declared isolation grade; mediate every effect and egress; treat sanitization as explicit declassification; close leases, caches, logs, descendants, and residuals through revocation or incident recovery; and never infer security from the record, handle, compartment, or finite test alone.

## 01:34–02:24 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. Preserve the exact current boundary: 3 valid and 8 expected-invalid synthetic Authority Use Receipts, 2 valid and 6 expected-invalid SCIF commit-probe routes, one security-overhead-laundering negative budget fixture inside the 6-valid/7-invalid budget corpus, and 22 finite Lean theorem declarations under four manifest targets; also retain the post-v2.1 bounded negative result of 0/36 governed primary unsafe releases versus 24/36 baseline, only 2/36 useful releases, and 32/36 exact attack-control rollback with a same-project policy/observer/promotion dependency.

## 02:24–03:07 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. Prompt, artifact, memory, tool-output, multimodal, or inter-agent injection confuses untrusted data with control authority. A confused deputy, compromised tool, or model launders a valid handle into a different principal, purpose, target, destination, or effect. Ambient authority, replay, stale approval, incomplete expiry, or failed revocation permits use outside the frozen lease. Overbroad context admission leaks protected or irrelevant facts before execution begins. The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 03:07–03:58 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. The finite authority-use route denies secret substitution when the execution boundary is unauthorized or lacks substitution permission. A context packet with insufficient clearance cannot enter a protected SCIF. A structured authority-use review routes missing handles, inactive leases, missing approvals, unauthorized boundaries, missing substitution permission, insufficient clearance, prompt injection, missing SCIFs, unsanitized output, residual leak risk, revocation requests, and clean authorized use into explicit security-kernel outcomes.

## 03:58–04:26 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 04:26–04:57 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is Adversarial Machine Learning and the Model Attack Surface. It takes responsibility for A learned artifact creates attack surfaces that ordinary application security does not fully own. Attackers can shape training data, perturb inference inputs, implant triggers, adapt to defenses.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.
