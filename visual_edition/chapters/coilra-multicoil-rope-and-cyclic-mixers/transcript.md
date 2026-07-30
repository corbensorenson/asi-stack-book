# Descriptive transcript — CoilRA, MultiCoil RoPE, and Cyclic Mixers

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/coilra-multicoil-rope-and-cyclic-mixers.html>

Video ID: `asi-video-coilra-multicoil-rope-and-cyclic-mixers`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:29 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: Position encodings, adapters, route heads, and mixers need a place for cyclic or block-cyclic structure that separates structural invariants from quality and runtime claims. The tempting shortcut is insufficient: Parameter-count, equivariance, or exact phase facts can be mistaken for better model behavior unless baselines, hardware costs, alias and load diagnostics, and failure cases are separated.

## 00:29–01:23 — Operating mechanism

**Visual description.** A labeled ledger diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: CoilRA, MultiCoil RoPE, and Cyclic Mixers owns a model-, layer-, mechanism-version-, workload-, baseline-, kernel-, hardware-, claim-axis-, and time-specific Cyclic Mechanism Tradeoff Packet: a cyclic adapter, phase bank, rotary scheme, route head, circulant operator, or block-cyclic mixer may enter a canary only when exact residue/winding, phase horizon, alias/collision/load, dense-reference parity, parameter and operation accounting, numerical error, kernel availability, complete cost, quality, failure, fallback, and rights evidence is matched against strong ordinary controls; equivariance, finite proofs, receipt validity, parameter reduction, or structural parity alone confers no quality, context-length, speed, memory, stability, efficiency, safety, deployment, transfer, support, or SOTA authority.

## 01:23–02:22 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. The exact current minimum is one schema-valid cyclic-mixer evaluation record; one inherited public-safe RoPE structural receipt boundary; one public-safe Circle cyclic-mixer receipt with bounded dense-reference parity and parameter accounting; one public-safe MultiCoil phase receipt with finite phase and relative-shift facts; two no-change decisions for the local cyclic slices; and seven finite local Lean theorem declarations. It includes no trained cyclic model, natural workload, baseline matrix, real kernel or hardware benchmark, measured quality/context/runtime/memory/stability benefit, independent reproduction, transfer, or chapter-core transition. Declare why cyclic structure is native to the data, task, geometry, recurrence, position, routing, or computation rather than an aesthetic substitution.

## 02:22–03:06 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. Cyclic elegance, prime periods, or equivariance substitutes for workload-native justification. A finite theorem or receipt is laundered into trained-model quality, usable context, runtime, memory, safety, or deployment authority. Exact phase-bank or integer collision results are generalized to floating-point RoPE or learned positions without a numerical and behavioral bridge. Residue-only diagnostics hide winding, wraps, aliases, collisions, joint repeat horizons, or load concentration. The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 03:06–03:50 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. A cyclic mixer review missing any structural, quality, runtime, memory, or parameter partition fails the finite structural-claim predicate. A promoted cyclic substrate missing baseline references or tradeoff metrics fails the finite promotion predicate. Structural, functional-parity, numerical, parameter, operation, quality, context, runtime, memory, stability, safety, deployment, transfer, and SOTA axes remain separate.

## 03:50–04:18 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 04:18–04:50 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is Executable Specifications and Lean Proof Envelope. It takes responsibility for The book needs to decide which architecture claims should become executable specs or Lean proofs. Read the live chapter for its complete source mappings, interfaces, invariants, failure modes, tests, and open evidence gaps.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.
