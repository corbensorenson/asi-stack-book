# P5 Natural Stateful-Service Campaign Qualification

Date: 2026-07-28

Campaign: `governed-operations-natural-service-campaign-001`

Decision: **authored implementation and instrument qualification passed;
natural development content remains closed**

## What was qualified

The frozen five-arm campaign now has an executable local qualification path.
The tracked result contains **60 authored** arm/fault trials: every one of the
five frozen arms crossed with all twelve frozen fault classes. The runner used
**213** isolated subprocess launches across arm workers, masked evaluators,
logical-time monitors, twenty-four calibration cases, and a dependency-worker
canary. A fresh replay must reproduce the tracked JSON exactly.

All fourteen declared state classes are represented: model, optimizer,
scheduler, RNG, prompt and policy, cache, retrieval memory, intent and effect
ledgers, outbox, credentials, replicas, backups, derived artifacts, and
descendants. The governed-arm controls restore all fourteen classes and retain
ownership of residuals in every authored fault case. The five authored arm
profiles are distinct, which establishes that routing through an arm changes
the harness response rather than merely changing a label.

The local dependency qualifications cover the exact cached model/runtime
receipt, a temporary local bare Git remote, a separate standard-library worker,
a digest-preserving no-rebuild artifact projection, and a separate read-only
monitor process. The exact Qwen3-8B snapshot returned the frozen `READY`
runtime canary. This checks runtime and snapshot custody only; it does not
evaluate model quality.

## Evaluator and opening decision

The separately launched evaluator passed **24/24** known-answer controls:
eight safe-useful successes, four unsafe releases, four false blocks, four
incomplete rollbacks, two delayed residuals, and two missing-truth cases. It
recorded zero false accepts, zero false rejects on the safe-success controls,
and perfect abstention recall on the two missing-truth controls. Candidate
packets expose neither arm identity nor mechanism trace.

All **14/14** implementation-opening gates pass. This authorizes only the
future admission of consecutive eligible natural development tasks under the
frozen intake contract. It does not authorize opening the forty protected
held-out tasks. Development task identifiers and content remain empty until
independently necessary work arises; tasks must not be manufactured to fill
the denominator.

## Exact evidence boundary

This checkpoint ran zero natural tasks, zero natural-task fault injections,
and zero recruited operators. The monitor injected logical time; it did not
observe an actual elapsed twenty-four-hour window. Dynamic operator, compute,
storage, network, and service-loss measurements remain reserved for natural
development. The direct arm's twelve authored unsafe outcomes and the governed
arm's twelve authored recoveries are positive-control behavior, not estimates
of either arm's natural performance.

The result therefore establishes executable campaign plumbing, known-answer
instrument behavior, exact source custody, and full-state recovery controls at
local authored scope. It does **not** establish natural-task usefulness,
operational safety, unsafe-release rate, false-blocking rate, qualified
recovery rate, causal advantage over generic SRE, transfer, institutional
independence, Theseus T4, support, release, AGI, or ASI.

## Held-out blockers and next legal action

The held-out denominator remains closed because development-only variance and
precision simulation has not run, a natural development population has not
accumulated, and the single protected opening has not been authorized. The
next legal action is to admit consecutive eligible natural development tasks
only as real project needs arise, execute all five matched arms and assigned
faults in the sandbox, measure the full frozen outcome and cost set, and use
development results only for declared competence repair and precision
simulation. Any implementation change requires recalibration. Protected tasks
remain unopened until every frozen competence, resource, precision, and
custody gate passes.

Machine record:

`experiments/governed_operations_argument_exit/qualification/2026-07-28-local.json`

Schema:

`schemas/governed_operations_campaign_qualification.schema.json`

Runner:

`scripts/run_p5_natural_service_campaign_qualification.py`

Validator:

`scripts/validate_p5_natural_service_campaign_qualification.py`
