# QCSA Governed Vertical Reference Report

Date: 2026-07-13

Status: completed bounded replay; no support-state effect

## What ran

One public-safe task changed a temporary sandbox configuration from
`response_mode: concise` to `response_mode: evidence_first`. The trace crossed
thirteen explicit stages:

```text
intent -> semantic IR -> SOID/SVA resolution -> evidence graph
       -> question compiler -> context materialization -> route plan
       -> independent authority decision -> bounded adapter action
       -> independent verification -> artifact/receipt graph
       -> migration -> rollback
```

The target was first resolved as a stable semantic object in an authoritative
three-facet atlas. A typed evidence graph remained distinct from identity and
did not turn graph position into truth. The question compiler selected one
environment clarification. A Semantic Address Certificate bound the resolved
object, context, task, epoch, provenance, uses, authority ceiling, validity,
migration contract, and residuals. That certificate still granted no effect.
An independent policy decision separately allowed one reversible write to the
temporary sandbox target.

Semantic resolution does not grant authority; it only prepares a request for
the separate policy decision.

The adapter wrote real bytes inside a temporary directory. A separate byte
reader observed the before and after SHA-256 values, matched the desired bytes,
and found no extra path. The artifact graph bound the intent, IR, SOID,
evidence, context, certificate, route, effect receipt, and successor epoch.
Migration changed the semantic address while preserving the same SOID. Rollback
restored the original bytes exactly and left no hidden path.

## Exact result

| Property | Result |
|---|---|
| Stages completed | 13/13 |
| Network calls | 0 |
| Service spend | $0 |
| Model calls | 0 |
| External humans | 0 |
| Clarifications | 1 deterministic fixture response |
| Tool effects attempted/released/observed | 1 / 1 / 1 |
| Effect receipts | 1 |
| Migration identity | Same SOID |
| Rollbacks attempted/exact | 1 / 1 |
| Unexpected paths after rollback | 0 |
| Adversarial paths rejected | 10/10 |
| Open residuals | 8 |

## Adversarial matrix

The validator preserves ten fail-closed paths: ambiguous address candidates,
stale certificate epoch, authority-scope widening, certificate tampering,
silent migration retargeting, missing effect receipt, poisoned alias retarget,
hidden side effect, exhausted question budget, and irreversible effect. Every
path either returned a typed conflict/stop/denial or raised the governing
contract error. None released an effect.

## What this establishes

This trace establishes that the exact standard-library reference components
can be composed without collapsing four boundaries:

- a SOID identifies the object while atlas paths address it;
- evidence supports a proposition without becoming identity or truth by graph
  position;
- semantic resolution and a certificate prepare a route but do not grant
  authority;
- a released effect is not accepted until separately observed, receipted,
  migrated, and rolled back.

It also closes the roadmap’s bounded P3 implementation requirement: a real
temporary effect, independent byte observation, content-addressed artifacts,
same-identity migration, exact rollback, a readable trace, and rejecting
adversarial paths now exist together.

## Residuals and non-claims

The task and semantic IR are hand-authored and synthetic. There is no learned
router, language-model reasoning candidate, trained specialist, production
authority service, real human approval, irreversible effect, distributed
migration, storage-erasure proof, production latency measurement, privacy test,
security assessment, or external replication. The byte observer is a separate
code path but remains internal. P2’s matched-resource advantage and
active-question-value claims remain refuted for the exact held-out corpus.

The eight residuals stay open in the machine result. This trace does not prove
effect-complete rollback in an open system, production safety, universal
semantic correctness, AGI, or ASI. It changes no chapter-core support state and
does not warrant a new QCSA chapter.

## Canonical artifacts

- `experiments/qcsa_vertical_reference/task.json`
- `experiments/qcsa_vertical_reference/results/vertical_result.json`
- `experiments/qcsa_vertical_reference/results/artifact_manifest.json`
- `scripts/build_qcsa_vertical_reference.py`
- `scripts/validate_qcsa_vertical_reference.py`
