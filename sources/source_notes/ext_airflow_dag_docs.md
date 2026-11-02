# Source Note: Apache Airflow Documentation - Dags

| Field | Value |
|---|---|
| Source ID | `ext_airflow_dag_docs` |
| Source title | Apache Airflow Documentation: Dags |
| Ingestion date | 2026-07-02 |
| Source version / URL | https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html |
| Citation label | Apache Airflow Documentation (2026), Dags |
| Published / updated | unknown / 2026 |
| Ingestion basis | Official public documentation inspected for the Labor OS external literature queue; no Airflow installation, scheduler, executor, DAG run, task instance, or retry trace was run from this repository. |

## Thesis

Airflow is a useful workflow-orchestration comparator because it exposes a mature DAG vocabulary: schedules, tasks, dependencies, callbacks, retries, and operational workflow metadata. The Labor OS chapter should use Airflow to avoid presenting DAG/task orchestration as novel, while describing the proposed typed-job composition's authority envelopes, artifact receipts, and evidence-state boundaries as application obligations. A conventional application can implement those joins; their naming does not establish novelty or an orchestration advantage.

## Mechanisms

- Represent workflows as Dags containing schedule, task, dependency, callback, and operational metadata.
- Treat tasks as discrete work units that run on workers.
- Use task dependencies to declare execution order and conditions.
- Separate orchestration structure from task internals.
- Provide workflow testing and execution-flow concepts for operational DAGs.

## Evidence

- The official Airflow docs describe a Dag as the model that contains what is needed to execute a workflow.
- The docs explicitly include schedule, tasks, dependencies, callbacks, retries, and timeouts in workflow execution concerns.
- This repository has not created an Airflow Dag, run the Airflow scheduler, executed tasks, inspected task instances, or compared Labor OS jobs against Airflow traces.
- Use this source for DAG and workflow-orchestration comparator vocabulary only.

## Failure Modes

- DAG orchestration can preserve task order while leaving authority, side-effect class, approval, and evidence-readiness implicit.
- A successful workflow run can still be completion laundering if the resulting artifact lacks claim links, verification refs, audit refs, residuals, and replay declarations.
- Workflow retries can conceal missing permission or approval semantics if failures are treated as operational rather than governance events.

## Book Chapters Supported

- `intent-to-execution-contracts` (Command Contracts: From Intent to Executable Work)
- `labor-os-and-typed-jobs` (Labor OS and Typed Jobs)
- `planning-as-a-control-layer` (selected external-comparator follow-up)

## Claims To Add Or Update

- Position Labor OS as typed AI work admission around workflow orchestration rather than a reinvention of DAG scheduling.
- Do not claim Airflow integration, scheduler evidence, task-run evidence, retry correctness, or workflow-quality measurement.

## Open Questions

- Which Labor OS lifecycle states correspond to Airflow Dag run and task instance states, and where do they diverge?
- Could future prototypes emit Airflow-compatible task receipts while preserving approval and evidence-state fields?
- What negative controls would show that a workflow run is not enough for governed evidence readiness?

## Selected task-lifecycle follow-up — 2026-10-11

Inspected the official [Airflow 3.3.2 Tasks documentation](https://airflow.apache.org/docs/apache-airflow/3.3.2/core-concepts/tasks.html), specifically Relationships, Task Instances, and Special Exceptions. The page distinguishes dependency readiness, executor assignment, running, failure, retry, and waiting for human input. It describes upstream success as the default condition with configurable control flow, and provides a fast-failure example for an invalid API key that retry will not repair.

Planning uses this selected reading to avoid treating ordinary dependency and retry control or human review as a new invention. The page's task-success state is not evidence that an arbitrary semantic obligation was satisfied. No Airflow installation, scheduler run, credential-repair experiment, comparative advantage, or current integration compatibility was exercised here. The July intake stays historical; this is a version-specific documentation reading, not a full current-library review.
