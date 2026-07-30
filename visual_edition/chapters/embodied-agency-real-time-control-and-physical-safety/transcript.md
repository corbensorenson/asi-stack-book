# Descriptive transcript — Embodied Agency, Real-Time Control, and Physical Safety

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/embodied-agency-real-time-control-and-physical-safety.html>

Video ID: `asi-video-embodied-agency-real-time-control-and-physical-safety`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:32 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: An authorized symbolic action can become unsafe when translated into deadline-bound control under dynamics, contact, actuator limits, human proximity, sensor loss, communication failure, or irreversible effects. The tempting shortcut is insufficient: A model demonstration, simulation success, barrier certificate, safe-RL label, emergency stop, or software rollback cannot establish plant-specific physical safety or effect reversal.

## 00:32–01:18 — Operating mechanism

**Visual description.** A labeled route diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: Physical execution requires a plant-specific control lease binding embodiment, workspace, state estimator, dynamics, timing, force/space/contact limits, human presence, advanced/baseline/stop controllers, switching and interlocks, exploration, degraded modes, observed effects, compensation, irreversible residuals, costs, and expiry. Freeze plant, payload, workspace, firmware, actuator, sensor, power, communication, and maintenance identity. Compile the semantic request into trajectory or control objectives with force, space, time, contact, and irreversibility limits. Establish safe-set, dynamics, state, uncertainty, deadline, and human-presence assumptions.

## 01:18–02:10 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. Use a low-energy simulated plant with conventional and advanced controllers, an independent safety monitor, reachable stop, and complete trace; seed deadline, state-estimator, saturation, communication, and fallback faults; transfer only to isolated low-energy hardware after positive controls pass. Compile the semantic request into trajectory or control objectives with force, space, time, contact, and irreversibility limits. Establish safe-set, dynamics, state, uncertainty, deadline, and human-presence assumptions. Separate advanced controller, safety monitor/filter, baseline controller, and independent stop path. Throughout the trace, one invariant remains visible: every command belongs to a current plant and lease

## 02:10–02:26 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. deadline miss actuator saturation contact instability unsafe exploration The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 02:26–02:58 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. A finite control admission model blocks physical commands when timing, state, envelope, fallback, or stop evidence is missing. stop authority is independent enough to survive advanced-controller failure fallback is reachable before the safety margin expires

## 02:58–03:26 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 03:26–03:56 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is Inter-Stack Protocols, Identity, and Economic Exchange. It takes responsibility for Local planning, context, artifact, and runtime contracts lose their binding when a request crosses to an independently operated protocol endpoint, agent, service.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.
