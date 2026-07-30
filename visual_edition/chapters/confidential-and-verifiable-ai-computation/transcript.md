# Descriptive transcript — Confidential and Verifiable AI Computation

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/confidential-and-verifiable-ai-computation.html>

Video ID: `asi-video-confidential-and-verifiable-ai-computation`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:51 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: AI computation increasingly crosses distrust boundaries: a user may need to hide inputs, a provider may need to protect weights, an auditor may need to verify the executed artifact, and every party may need output integrity without granting another party unrestricted custody. Ordinary transport encryption ends before computation begins. The tempting shortcut is insufficient: Privacy policy governs permitted information use, while hardware custody governs stored artifacts. Neither supplies a guarantee-by-guarantee execution contract covering input confidentiality, model confidentiality, computation integrity, output authenticity, attestation freshness, leakage, verifier policy, cost, and failure recovery.

## 00:51–01:45 — Operating mechanism

**Visual description.** A labeled stack diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: Confidential and verifiable AI requires a compositional execution contract that names the adversary, protected assets, permitted leakage, trust anchors, proof or attestation statement, verifier policy, freshness, revocation, performance budget, and authorization boundary; no primitive or attestation may be treated as proof of semantic correctness, legitimate purpose, or end-to-end privacy. Express the requested guarantee vector separately for input privacy, model privacy, intermediate-state privacy, computation integrity, output authenticity, availability, and auditability. Choose among FHE, MPC, zero-knowledge proofs, confidential execution, private retrieval, differential privacy, or hybrid composition against an explicit adversary and leakage model.

## 01:45–02:45 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. A guarantee matrix and local demonstration for one bounded inference operation with explicit adversary and leakage models, artifact and configuration commitments, freshness, independent verification, native-versus-protected latency and cost accounting, negative tests for replay and mismatched artifacts, and a no-authorization non-claim. Choose among FHE, MPC, zero-knowledge proofs, confidential execution, private retrieval, differential privacy, or hybrid composition against an explicit adversary and leakage model. Bind code, model, configuration, data commitments, platform state, nonce or epoch, and policy identity into evidence that a distinct verifier appraises. Keep cryptographic correctness, attested identity, model quality, semantic validity, user authorization, and lawful purpose as separate claim classes.

## 02:45–03:28 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. Guarantee laundering collapses confidentiality, integrity, privacy, authorization, and correctness into one secure-compute label. Stale or replayed attestation is accepted after artifact, platform, policy, or revocation state changed. Side channels, outputs, access patterns, logs, caches, or failure timing leak protected information. The proved computation faithfully executes the wrong model, wrong preprocessing, wrong policy, or semantically invalid relation. The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 03:28–04:11 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. A finite protected-execution record may hand off only when guarantees, adversary, leakage, artifact, freshness, verifier policy, fallback, and unsupported properties are explicit; no theorem proves semantic correctness, authorization, or end-to-end privacy. An attestation proves only the appraised statement about a measured environment; it does not prove trustworthy intent, correct policy, or correct output meaning.

## 04:11–04:39 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 04:39–05:13 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is Model-Weight Custody and Hardware Roots of Trust. It takes responsibility for A system can govern runtime tool authority while model weights, optimizer state, adapters, quantizations, checkpoints, caches, recovery images, extracted equivalents, and recipient derivatives are copied, reconstructed, decrypted, loaded, served, revoked.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.
