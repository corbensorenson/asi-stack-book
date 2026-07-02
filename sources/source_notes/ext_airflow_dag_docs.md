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

Airflow is a useful workflow-orchestration comparator because it exposes a mature DAG vocabulary: schedules, tasks, dependencies, callbacks, retries, and operational workflow metadata. The Labor OS chapter should use Airflow to avoid presenting DAG/task orchestration as novel, while making clear that ASI Stack typed jobs add authority envelopes, approval gates, artifact receipts, and evidence-state boundaries for AI labor.

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

## Claims To Add Or Update

- Position Labor OS as typed AI work admission around workflow orchestration rather than a reinvention of DAG scheduling.
- Do not claim Airflow integration, scheduler evidence, task-run evidence, retry correctness, or workflow-quality measurement.

## Open Questions

- Which Labor OS lifecycle states correspond to Airflow Dag run and task instance states, and where do they diverge?
- Could future prototypes emit Airflow-compatible task receipts while preserving approval and evidence-state fields?
- What negative controls would show that a workflow run is not enough for governed evidence readiness?
