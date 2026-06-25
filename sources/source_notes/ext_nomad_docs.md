# Source Note: Nomad Documentation

| Field | Value |
|---|---|
| Source ID | `ext_nomad_docs` |
| Source title | Nomad Documentation |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://developer.hashicorp.com/nomad |
| Citation label | HashiCorp Developer, Nomad Documentation |
| Published / updated | unknown / unknown |
| Ingestion basis | Official public documentation inspected for the Personal Compute Hives external literature queue; no Nomad cluster or job was run from this repository. |

## Thesis

Nomad is relevant because it frames scheduling as containers, binaries, and batch jobs across on-prem and cloud environments. That maps closely to hive job placement, while still lacking the ASI Stack's personal data, approval, and family-policy layers.

## Mechanisms

- Schedule and orchestrate containers and non-containerized applications.
- Express workloads as jobs with task drivers and runtime behavior.
- Support on-prem and cloud deployment contexts.
- Include production concerns such as ACLs, encrypted traffic, resiliency, resource quotas, policy, affinities, and preemption.

## Evidence

- The official documentation presents Nomad as a scheduler and orchestrator for heterogeneous workload types across infrastructure locations.
- This repository has not installed Nomad, expressed a hive job as a Nomad job, or tested policy enforcement.
- Use this source for scheduler vocabulary and substrate comparison only.

## Failure Modes

- A general scheduler can optimize placement without understanding ASI Stack authority.
- Policy plugins and quotas are not automatically equivalent to child safety, secret handles, or VCM revocation.
- Cloud/on-prem portability can increase data-exposure risk if job contracts are underspecified.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use this source to compare hive job contracts with existing scheduler job specifications.
- Do not claim that Nomad solves hive federation, rented-node safety, or personal AI ownership.

## Open Questions

- Would `HiveJobContract` compile naturally to a Nomad job file?
- Which Nomad policy hooks could enforce data class and authority ceiling?
- What evidence bundle should a Nomad-backed worker return?
