# Descriptive transcript — Coil Attention, Cyclic Memory, and Recurrence Contracts

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/coil-attention-cyclic-memory-and-recurrence-contracts.html>

Video ID: `asi-video-coil-attention-cyclic-memory-and-recurrence-contracts`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:27 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: Memory, attention, and recurrence mechanisms need finite structural contracts for aliasing, coverage, freshness, active work, loop exits, and overthinking boundaries. The tempting shortcut is insufficient: Long context, sparse attention, ring buffers, and recursive loops can silently hide stale reads, uncovered lags, duplicate slots, alias collisions, or unbounded work.

## 00:27–01:17 — Operating mechanism

**Visual description.** A labeled graph diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: Coil Attention, Cyclic Memory, and Recurrence Contracts owns a memory-object-, state-version-, request-, consumer-, workload-, structural-axis-, budget-, and time-specific State-Carry and Recurrence Admission Lease: a slot read, cyclic address, KV reuse, sparse edge, fanout schedule, or recurrent step may be admitted only when authority, provenance, residue and winding, freshness, coverage, alias and collision state, active work, progress, exit, fallback, expiry, and residuals satisfy the exact consumer contract; structural validity, synthetic fixtures, receipt replay, cache presence, or reduced scheduled work alone confers no retrieval, reasoning, context-length, quality, speed, memory, safety, deployment, transfer, support, or SOTA authority.

## 01:17–02:12 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. The exact current minimum is one schema-valid cyclic-memory record; three valid and six expected-invalid synthetic contract traces; five public-safe external Circle structural receipt slices for cyclic memory, KV-cache freshness, recurrence scheduling, sparse-attention gaps, and strided fanout, all with explicit no-promotion boundaries; and six finite local Lean theorem declarations. It proves no deployed cache, sparse attention, recurrence controller, useful memory, retrieval, reasoning, context-length, latency, memory, independent reproduction, transfer, or chapter-core result. Bind every carried state to source provenance, VCM packet or context lineage, write and read epochs, model and tokenizer identity, cache layout, device, and revocation state.

## 02:12–02:52 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. Residue-only addressing hides winding, wraps, overwrites, collisions, or aliased sources. A cache entry from another request, tenant, model, tokenizer, policy, or epoch is accepted because its slot looks fresh. Physical presence or timestamp freshness is confused with authorized, relevant, correct, or adequate content. Sparse lag or path coverage is treated as semantic dependency coverage, retrieval quality, or long-context understanding. The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 02:52–03:35 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. A reused cyclic slot with missing residue or winding and no visible alias residual fails the finite alias-boundary predicate. A retrieval-quality record that promotes from sparse coverage and freshness while semantic-quality evidence is absent fails the finite quality-promotion predicate. Residue-only addressing never erases winding, wrap count, slot identity, collision, overwrite, or alias residuals when they matter.

## 03:35–04:03 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 04:03–04:32 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is CoilRA, MultiCoil RoPE, and Cyclic Mixers. It takes responsibility for Position encodings, adapters, route heads, and mixers need a place for cyclic or block-cyclic structure that separates structural invariants from quality and runtime claims.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.
