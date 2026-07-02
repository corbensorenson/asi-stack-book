# Source Note: OMG BPMN 2.0.2

| Field | Value |
|---|---|
| Source ID | `ext_bpmn_2_0_2_spec` |
| Source title | Business Process Model and Notation Specification Version 2.0.2 |
| Ingestion date | 2026-07-02 |
| Source version / URL | https://www.omg.org/spec/BPMN/2.0.2/ |
| Citation label | OMG (2014), BPMN 2.0.2 |
| Published / updated | 2014-01 / 2014-01 |
| Ingestion basis | OMG specification page inspected for the Labor OS external literature queue; no BPMN model, conformance test, process engine, or BPMN-to-Labor-OS compiler was built in this repository. |

## Thesis

BPMN is the process-modeling comparator for the Labor OS chapter. It establishes that stakeholder-readable, implementation-independent process notation and translation into software process components are existing standards work. Labor OS should therefore present typed jobs as an AI-governance execution record layered around process work, not as the invention of process modeling.

## Mechanisms

- Provide a formal Business Process Model and Notation specification.
- Use stakeholder-readable flowchart-like notation for business processes.
- Remain independent of a particular implementation environment.
- Be precise enough for translation into software process components.
- Publish normative documents and machine-readable artifacts for process notation.

## Evidence

- The OMG specification page identifies BPMN 2.0.2 as a formal standard.
- The page describes BPMN as a de facto standard for business process diagrams with stakeholder and software-process translation goals.
- This repository has not created BPMN diagrams, run a BPMN engine, checked BPMN conformance, or translated typed jobs into BPMN.
- Use this source for process-modeling and notation lineage only.

## Failure Modes

- Process notation can make workflows legible without encoding AI authority, model/tool risk, proof obligations, or evidence-state transitions.
- Stakeholder-readable process diagrams can still omit residual ownership, replay boundaries, and claim-support effects.
- Translation into process components does not by itself make AI-produced artifacts verified or promotion-safe.

## Book Chapters Supported

- `intent-to-execution-contracts` (Command Contracts: From Intent to Executable Work)
- `labor-os-and-typed-jobs` (Labor OS and Typed Jobs)

## Claims To Add Or Update

- Position Labor OS typed jobs as governance records around AI work, with BPMN as the process-notation lineage rather than an ignored predecessor.
- Do not claim BPMN conformance, BPMN engine execution, process-compiler implementation, or model-checking evidence.

## Open Questions

- Which typed-job lifecycle states should have BPMN-like process notation in future diagrams?
- Could a Labor OS process compiler emit BPMN for human review while preserving machine-checkable authority and evidence fields?
- What should be rejected when a process diagram is readable but missing approval or evidence-state semantics?
