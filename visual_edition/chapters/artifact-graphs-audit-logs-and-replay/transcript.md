# Descriptive transcript — Artifact Graphs, Audit Logs, and Replay

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/artifact-graphs-audit-logs-and-replay.html>

Video ID: `asi-video-artifact-graphs-audit-logs-and-replay`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:22 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: The stack needs durable artifacts and replayable traces so work can be inspected, reused, tested, and improved. The tempting shortcut is insufficient: If outputs are not tied to inputs, tools, context, claims, and logs, later verification and improvement cannot know what happened.

## 00:22–01:18 — Operating mechanism

**Visual description.** A labeled graph diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: Execution should produce an artifact graph with audit logs, provenance, replay metadata, and links to claims and tests. Freeze an artifact admission envelope with stable artifact and revision identity, type, role, producer, parent job and attempt, intended consumers, consequence, authority, rights, retention, and expiry before reuse. Compute content digests and, where policy matters, compound content-and-policy identities while treating paths, URLs, object keys, cache slots, and display names as mutable locations or projections. Bind each artifact revision to exact source, dataset, contract, plan, job, attempt, context transaction, semantic certificate, model, prompt, tool, adapter, code, environment, policy, approval, permission, cost, and residual lineage that actually applied.

## 01:18–02:14 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. The current minimum is two public artifact/projection schemas; 2 valid/6 rejecting replay fixtures; 1 valid/10 rejecting projection-revocation records; 1 valid/4 rejecting record-reality sequences; 3 valid/6 rejecting receipt-faithfulness records; a four-surface repository audit with 55 digest checks and five mutations; four deterministic challenges and five mutations; one live artifact with three observation routes and seven mutations; four sampled artifacts with twelve observation routes and eight mutations; 3 valid/6 rejecting epistemic-TCB records; one historical GitHub Actions service record; one historical public-page fetch record; eight accepted no-promotion decisions; and forty-three Lean declarations under ten public targets.

## 02:14–03:06 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. Artifact amnesia leaves useful or harmful work products without stable identity, parent work, source, context, tool, effect, claim, test, owner, or residual lineage. Path and name authority makes relocation, cache movement, renaming, or object-store migration change identity or silently bind the wrong bytes. Provenance theater records plausible asserted edges while actual inputs, transformations, side effects, omitted dependencies, or responsible actors remain unknown. Audit-log theater accepts mutable, dropped, selectively written, unauthenticated, inaccessible, or producer-controlled events as a complete reconstruction. The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 03:06–03:53 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. A reachable artifact lifecycle preserves exact artifact, content, parent-job, source, context, transaction, certificate, tool, claim, test, policy, and consumer custody from registration through consumer-acknowledged admission without assigning support or external effects. Missing provenance, replay, observation, cross-check, trap, attestation-limit, trust-root, verifier-separation, recursion-stop, residual, revocation, or consumer obligations block lifecycle progress.

## 03:53–04:21 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 04:21–04:54 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is Runtime Adapters, Tool Permissions, and Human Approval. It takes responsibility for Plans become real-world effects only through tools, runtimes, deployment adapters, and approval gates. Read the live chapter for its complete source mappings, interfaces, invariants, failure modes, tests, and open evidence gaps.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.
