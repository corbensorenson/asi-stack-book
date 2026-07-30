# Descriptive transcript — System Boundaries and Authority

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/system-boundaries-and-authority.html>

Video ID: `asi-video-system-boundaries-and-authority`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:33 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: To test whether cross-layer effects are authorized, the stack needs explicit identities for the principal, execution domain, operation, target, permission class, ceiling, grant lifecycle, delegation, and receipt. The tempting shortcut is insufficient: Role labels, prompts, and ambient process identity do not by themselves distinguish read, transform, disclose, write, execute, and approve authority or enforce delegation, expiry, revocation, and cross-domain approval.

## 00:33–01:12 — Operating mechanism

**Visual description.** A labeled graph diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: External-effect authority should be represented as a versioned, revocable tuple binding principal, execution domain, operation, target, permission class, scope, ceiling, grant state, delegation, expiry or revocation epoch, and receipt obligations; capability, context access, route quality, or ambient process power alone confers none of it. Define principals, authorities, ceilings, grants, revocations, and handoff contracts. Separate knowledge access from action authority. Represent missing authority as a detectable failure rather than implicit permission.

## 01:12–01:59 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. An authority-transition schema plus a unified authority-tuple lifecycle that binds execution-domain ownership, scope, budget, trace, replay, grant, revocation, cross-domain approval, receipts, and protocol-versus-hardware-root boundaries. Separate knowledge access from action authority. Represent missing authority as a detectable failure rather than implicit permission. Bind principal, execution domain, operation, target, permission class, scope, budget account, trace, replay identity, grant, policy version, revocation epoch, and expiry in one authority tuple. Throughout the trace, one invariant remains visible: Authority never expands silently.

## 01:59–02:20 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. Authority creep. Confused-deputy tool calls. Memory access treated as action approval. Authority identity forks across budget, trace, replay, or revocation. The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 02:20–03:08 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. Every accepted issuance, dispatch, and effect in the finite reachable grant model remains within the caller ceiling and exactly binds grant ID, principal, operation, target, epoch, expiry, remaining uses, approval, dispatch, and effect custody. The reachable model and independent consumer reject authority widening, confused-deputy substitution, stale or expired grants, missing approval/dispatch/effect receipts, post-revocation dispatch, effect without dispatch, and consumed one-shot reuse.

## 03:08–03:36 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 03:36–04:05 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is Failure Modes of Ungoverned Intelligence. It takes responsibility for Governance, reliability, and self-improvement claims cannot be tested unless their failure conditions, observable boundary events, evidence records, and owners are declared prospectively.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.
