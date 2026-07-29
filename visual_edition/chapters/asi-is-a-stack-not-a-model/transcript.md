# Descriptive transcript — ASI Is a Stack, Not a Model

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/asi-is-a-stack-not-a-model.html>

Video ID: `asi-video-asi-is-a-stack-not-a-model`

Lifecycle: local pilot; no YouTube publication is authorized

Current support: `argument`
Claim label: `Design rationale`

## 00:00–00:39 — The unit of analysis

**Visual description.** On a dark blue-black field, the title “ASI Is a Stack,
Not a Model” appears above a cyan rule. A small circle labeled “MODEL” moves
inside a larger rounded boundary labeled “GOVERNED SYSTEM.” Around it, muted
labels name context, authority, execution, observation, and evidence. The model
remains visible as a component rather than disappearing.

**Narration.** What is the thing we are trying to build? If the answer is
simply “a bigger model,” we have already hidden most of the engineering
problem. A model can generate, compress, classify, criticize, or plan. But an
advanced AI system must also decide what context is permitted, which claims
are supported, who may authorize an action, what changed in the world, and how
a failed change can be reversed. The ASI Stack begins by choosing the larger
system as its unit of analysis. The model is important, but it is one component
inside a governed machine.

## 00:39–01:18 — The monolith failure

**Visual description.** Six labeled cards—planning, memory, verification,
execution, governance, and evidence—collapse into one opaque gray circle.
Across it, two stop bars appear with the text “CAPABILITY ≠ AUTHORITY” and
“RECEIPT ≠ REALITY.” A magenta residual loop and red rollback arrow remain
outside the circle to show that the monolith has no addressable owner for them.

**Narration.** The monolithic picture fails when useful ability silently
becomes every other kind of power. A fluent plan is not permission to execute.
Retrieved text is not automatically belief. A benchmark score is not
deployment authority. A proof about a finite model is not runtime enforcement.
And a log saying that something happened is not the same as independent
evidence that the world changed as claimed. If planning, memory, verification,
execution, governance, and evidence all collapse into one opaque component,
there is nowhere reliable to attach limits, challenge a receipt, preserve a
residual, or perform rollback.

## 01:18–01:56 — Governed layers

**Visual description.** Seven high-contrast layer cards assemble in two rows:
intent, planning, context, reasoning, authority, execution, and evidence. Cyan
arrows connect them, while the authority card uses a gold shield and the
evidence card uses a green ledger. A caption states “logical contracts, not
mandatory processes.”

**Narration.** The stack replaces that ambiguity with explicit responsibility
boundaries. Intent becomes a typed request. Planning produces a proposal, not
an effect. Context carries provenance, freshness, rights, and taint. Reasoning
produces claims with uncertainty and dependencies. Authority arrives through a
scoped, current grant. Execution passes through a narrow adapter. Observation
and evidence remain able to disagree with what execution reported. These
layers are logical contracts, not a demand for microservices. One model may
implement several roles, and several models or people may implement one role,
as long as the boundaries remain externally enforceable and auditable.

## 01:56–02:44 — Worked authority-to-effect trace

**Visual description.** Eight numbered nodes form a left-to-right trace:
request, plan, context, verify, grant, effect, observe, and evidence. Each node
lights in order. At the grant, a gold shield closes around the arrow. At
effect, a receipt branches upward while observation continues on a separate
green path. A contradiction routes to a magenta residual loop. A reversible
effect follows a red arrow back to a box labeled “RECORDED PRE-STATE.”

**Narration.** Consider one worked trace. A user asks for a material change.
First, the intent layer records the requested outcome and constraints.
Planning proposes steps and alternatives. The context layer mounts only the
sources and state permitted for this job. A verifier checks the plan’s claims
and leaves unresolved questions visible. Only then can an authority gate issue
a grant bounded by scope, time, owner, and revocation state. The execution
adapter rechecks that grant before producing an effect. A receipt records what
the adapter reports. An independent observation checks the post-state. If
observation contradicts the receipt, the discrepancy survives as an owned
residual. If the effect is reversible, rollback restores the recorded
pre-state; otherwise compensation or quarantine must remain explicit.

## 02:44–03:21 — The noninheritance law

**Visual description.** Six attempted arrows point from capability to
authority, context to belief, plan to effect, receipt to reality, theorem to
enforcement, and replacement to qualification. Each arrow stops at a labeled
vertical gate. The paired words, stop bars, and gate shapes make the meaning
independent of color and motion.

**Narration.** This trace expresses the stack’s noninheritance law. Capability
does not confer authority. Context does not confer belief or permission. A
plan does not confer an effect. A receipt does not confer reality. A theorem
does not confer enforcement. A replacement does not inherit its predecessor’s
qualification. A proposal for self-improvement cannot approve itself. Every
handoff must preserve identity and require an explicit transition for new
authority, evidence, effect, qualification, or release state. The point is not
paperwork. The point is to stop one successful object from smuggling unrelated
powers across a boundary.

## 03:21–03:57 — Strong objection and evidence ceiling

**Visual description.** Three neutral columns—strong monolith, lightweight
wrapper, and governed stack—stand beneath the same task, model, tools, context,
and cost header. No winner is highlighted. The scene then places the current
finite repository evidence inside a double gray boundary labeled “ENCODED
SCOPE,” with empirical efficiency, transfer, deployment, safety, and ASI
outside it.

**Narration.** There is a serious objection. Explicit interfaces can lose
information, add latency, create attack surfaces, and turn fluid cognition
into brittle bureaucracy. Ordinary operating-system isolation and a
lightweight tool wrapper may sometimes be enough. The stack therefore cannot
win by definition. A fair test must compare a strong monolithic agent, a
lightweight wrapper, and the governed stack on the same natural tasks, with
matched models, tools, context, tuning effort, and total cost. It must count
useful completion, unsafe or unauthorized effects, false refusals, recovery,
latency, and governance overhead together.

## 03:57–04:45 — Evidence boundary and handoff

**Visual description.** A final card states “Current support: argument” and
“blocked after full bounded attempt.” Below it, a muted line says that finite
checks do not prove deployment, safety, empirical efficiency, transfer, or
ASI. The live-book URL appears, followed by “Next: The Efficient ASI
Hypothesis.”

**Narration.** The current chapter does not contain that broad result. Its core
claim remains a design rationale at argument support and is recorded as
blocked after a full bounded attempt. Repository checks exercise finite layer
contracts and one local authority-to-effect path, but they do not prove
deployed authority, whole-system safety, empirical efficiency, transfer, or
ASI. The architecture test is narrower and practical: every powerful
component should name what it owns, what artifact crosses its boundary, which
authority it has, what evidence it can create, what can fail, and how the
failure remains recoverable. The next chapter asks whether those explicit
boundaries can improve useful work per total governed cost. That is the
Efficient ASI Hypothesis.

## Source and evidence boundary

The visual draws only on the canonical chapter and its assigned source IDs:
`viea`, `beastbrain`, `aletheia`, `talos`, `moecot`, `scf`,
`ext_drexler_cais_2019`, and `ext_embedded_agency_2019`. Those sources provide
architecture lineage and comparison. The visual does not claim local
reproduction of their systems or results.
