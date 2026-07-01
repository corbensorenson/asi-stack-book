# Source Note: Google Cloud MLOps Continuous Delivery and Automation Pipelines

| Field | Value |
|---|---|
| Source ID | `ext_google_cloud_mlops_cd` |
| Source title | MLOps: Continuous Delivery and Automation Pipelines in Machine Learning |
| Ingestion date | 2026-07-01 |
| Source version / URL | https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning |
| Citation label | Google Cloud Architecture Center (2024), MLOps Continuous Delivery and Automation Pipelines in Machine Learning |
| Published / updated | unknown / last reviewed 2024-08-28 |
| Ingestion basis | Official Google Cloud Architecture Center documentation inspected for MLOps continuous-delivery vocabulary; no Google Cloud service, ML pipeline, model registry, model deployment, monitoring trigger, or rollback was run from this repository. |

## Thesis

Google Cloud's MLOps documentation is a useful model-rollout comparator because it separates ordinary CI/CD from ML-specific validation, model delivery, continuous training, data drift, monitoring, and rollback-trigger concerns. The replacement chapter should use this source to avoid treating model replacement as ordinary code deployment while keeping the ASI Stack's stronger requirements explicit: field identity, authority ceilings, evaluator independence, residual ledgers, and support-state boundaries.

## Mechanisms

- Treat MLOps as DevOps-like automation and monitoring across integration, testing, release, deployment, and infrastructure management for ML systems.
- Extend CI beyond code to data, data schemas, and models.
- Extend CD beyond a software package to pipeline and model-prediction-service delivery.
- Add continuous training as an ML-specific property.
- Monitor live model performance and data profiles so deviations can trigger retraining, notification, or rollback.

## Evidence

- The documentation states that ML systems differ from ordinary software because testing includes data validation, model quality evaluation, and model validation.
- It notes that deployment can require multi-step pipelines that retrain, validate, and deploy model prediction services.
- It frames production ML degradation as broader than ordinary software defects because data profiles and online model performance can change.
- This repository has not built or executed an ML pipeline, deployed a prediction service, monitored live model drift, or executed a model rollback.

## Failure Modes

- Model delivery can be mistaken for capability replacement when data, schema, model, code, and serving changes have different failure surfaces.
- Offline holdout quality can be mistaken for live replacement safety.
- Monitoring and rollback triggers can be absent, stale, or misaligned with user-facing harm.
- MLOps automation does not by itself provide evaluator independence, governance approval, authority non-expansion, or residual escrow.

## Book Chapters Supported

- `capability-replacement-and-rollback` (Capability Replacement and Rollback)

## Claims To Add Or Update

- Use this note to ground model-rollout and regression-gating comparators in the chapter's replacement discussion.
- State that ASI replacement must treat data, model, code, pipeline, and authority changes as separately reviewable transaction surfaces.
- Do not claim ML pipeline implementation, production monitoring, model deployment, model rollback, or empirical model quality evidence.

## Open Questions

- What minimum public-safe model-replacement fixture should represent data, model, code, serving, authority, and evaluator deltas separately?
- Which live metrics can support rollback without incentivizing narrow proxy optimization?
- How should continuous training interact with SCF lifecycle states without turning retraining into unreviewed self-replacement?
