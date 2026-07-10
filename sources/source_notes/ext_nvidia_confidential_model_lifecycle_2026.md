# Source Note: NVIDIA Confidential Model Lifecycle

| Field | Value |
|---|---|
| Source ID | `ext_nvidia_confidential_model_lifecycle_2026` |
| Source title | Workload and Model Lifecycle: Deploying Proprietary Models Securely with NVIDIA Confidential Computing |
| Ingestion date | 2026-07-10 |
| Source version / URL | NVIDIA official technical documentation, 2026, https://docs.nvidia.com/enterprise-reference-architectures/deploying-proprietary-models-confidential-compute-self-hosted-kubernetes/latest/workload-and-model-lifecycle.html |
| Citation label | NVIDIA (2026), Confidential Model Lifecycle |
| Published / updated | 2026 / 2026 |
| Ingestion basis | Official documentation inspected for encrypted weight storage, confidential-pod memory handling, attestation-sensitive policy artifacts, and key-release framing. No NVIDIA confidential-computing stack, pod, GPU attestation, key service, or deployment was configured locally. |

## Thesis

The documentation describes a deployment architecture in which model weights
remain encrypted outside a confidential pod, are readable only in protected
memory, and rely on policy-sensitive attestation evidence for key-release
decisions. It is a vendor implementation reference, not evidence that the
design is universally sufficient or locally deployed.

## Mechanisms

- Keep weights encrypted in images, encrypted storage, or an artifact service
  before a confidential workload is permitted to read them.
- Bind key-release decisions to the measured configuration and policy-relevant
  artifacts of a confidential workload.
- Treat policy, runtime, and key-service configuration changes as changes that
  can alter attestation evidence and must be reevaluated.
- Keep host plaintext exposure, in-guest storage policy, and runtime memory
  scope explicit in the lifecycle record.

## Evidence

- The official documentation describes its stated confidential-computing
  deployment architecture and model-lifecycle controls.
- It is vendor documentation rather than independent efficacy evidence.
- This repository has not created a pod, deployed weights, attested hardware,
  released a key, or inspected host/guest memory exposure.

## Failure Modes

- A valid-looking attestation token is treated as proof that all policy-relevant
  artifacts, key-service rules, or host paths are secure.
- A configuration change silently invalidates the assumptions behind key
  release, while the old token or policy remains in use.
- Encrypted-at-rest weights are treated as protected during execution, output,
  backup, or authorized misuse without scope-specific evidence.
- Vendor-specific documentation is generalized into a cross-platform custody
  guarantee or an ASI Stack deployment result.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust` (Model-Weight Custody and Hardware Roots of Trust)

## Claims To Add Or Update

- Use this note for encrypted-weight, policy-sensitive attestation, key-release,
  confidential-workload, and configuration-change vocabulary.
- Preserve separate records for model identity, encrypted artifact, environment
  measurement, key-release decision, access scope, and incident response.
- Do not claim local NVIDIA hardware, confidential pod behavior, host secrecy,
  attestation verification, key release, or deployed model protection.

## Open Questions

- Which environment measurements are necessary but insufficient for a usable
  custody decision?
- How should key-release denial, stale attestations, incidents, and revocation
  be represented in a public-safe model-custody fixture?
- What cross-vendor and independent evidence is needed before an architecture
  can make a stronger confidentiality claim?
