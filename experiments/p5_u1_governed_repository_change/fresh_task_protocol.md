# Fresh-task effect reconciliation protocol

Protocol date: 2026-11-20  
Scope: prospective local comparison for an inspectable mechanism result  
Decision owner: The ASI Stack integrated reference and its Quickstart

## Question

When does an independently observed receipt improve ordinary scoped change
control after a repository workflow requests an external effect? The mechanism
under test is reconciliation of the requested effect with what the receiving
service actually committed. The earlier source-link replay motivates this
comparison and supplies no new tasks or scores.

This is a bounded implementation comparison with fresh authored maintenance
tasks. The natural service campaign has its own frozen intake and protected
denominator. Use natural intake for a claim about ordinary project workloads,
and use this smaller experiment to find the conditions under which the
mechanism does or does not alter an operator's decision. [Natural service
campaign](../../docs/p5_natural_stateful_service_campaign_preregistration.md)

## Matched work and conditions

Freeze four distinct work definitions before running either arm. Each specifies
the starting files, exact permitted paths, independently checkable target
output and an optional receipt for a local publication or notification. No
effect reaches a live service or another person. For each work definition,
exercise four deterministic conditions in independently initialized
workspaces and sinks.

1. Routine request and successful acknowledgment.
2. Request committed by the sink, with an acknowledgment lost.
3. Request still pending when a receiving service observation would be made,
   then committed later.
4. Request failed before an effect, with affirmative evidence of failure when
   the receiving service exposes that state.

Both arms use the same candidate, scope checks, approval fixture, test
oracle, destination, stable operation identity, failure scenario and
observation horizon. Use the same sink contract per pair. Check what changes
when the sink supports idempotency. A reused request identifier should carry
the original operation through recovery. On a route where the destination
honors that identifier, report the protection attributable to the sink.

- **Ordinary scoped workflow.** Verify the proposed paths and actual diff,
  run the target checks, and require scoped approval before a consequential
  effect. Use a stable request ID, ordinary failure classification, bounded
  idempotent retry when supported, and safe hold with a human-owned ticket
  when the outcome is ambiguous. Do not force the ordinary arm to retry a
  potentially non-idempotent action.
- **Receipt and reconciliation.** Begin from the same controls. After an
  ambiguous outcome, read exact operation state through the receiver's
  independent read path before selecting a bounded retry, hold, or closure.
  Verify that the observation names the intended task, destination, and
  effect. Missing, stale, or mismatched observations lead to hold.

For both routes, an urgent task without current permission stays blocked.
Calibrate this rejection on a separate known-answer case. For the observer,
also check pending, wrong-operation, stale, missing, committed, and explicitly
failed observations before opening the 16 pairs. Keep scorer input separate
from the routes' self-reports and score terminal state from the sink. If a
calibration check fails, record the instrument failure and keep the paired
outcome table closed.

## Outcomes and interpretation

The primary report is the complete table of 16 pairs. Define acceptance as
correct in-scope work plus exactly one authorized effect when the request
calls for it, with a resolved disposition at the shared deadline. Report
correct safe holds separately from wrongly blocked authorized changes.
Report repeated effects, unresolved outcomes, and any false closure
individually. A timeout alone is insufficient evidence of failure. Report
scripted reviews, retries and observer reads separately as mechanism cost.
Active reviewer time is an outcome only when actual participants are
observed. Publish the scripted results without substituting wall time for
human effort.

The practical adoption rule is scoped. An extra observation path earns its
place when it resolves outcomes or prevents repeated effects under the
declared sink contract, while preserving accepted routine work and avoiding
additional unauthorized or falsely closed effects. Report equal outcomes
where ordinary controls suffice. If the observer stays unavailable, say that
the added mechanism could not resolve the case. Retain all pairs and report
each sink contract. A small set of designed trials can demonstrate a
mechanism and expose a counterexample, but it cannot estimate deployment
prevalence or broad architecture effects.

## What reviewers should receive

Preserve the protocol identity, exact task and fault fixtures, both
executables, calibration disposition, complete per-pair outcomes and raw sink
observations, and an exact command from a clean checkout. Show which
behavior follows from the scoped approval and idempotency protections, and
which is attributable to observing the receiving service. The Quickstart,
homepage, review invitation and citable snapshot should all point to the
same result. Record exploratory changes as dated amendments before opening a
new series.
