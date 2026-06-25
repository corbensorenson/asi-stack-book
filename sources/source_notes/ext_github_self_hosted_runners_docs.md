# Source Note: Self-hosted Runners

| Field | Value |
|---|---|
| Source ID | `ext_github_self_hosted_runners_docs` |
| Source title | Self-hosted runners |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://docs.github.com/en/actions/concepts/runners/self-hosted-runners |
| Citation label | GitHub Docs (2026), Self-hosted runners |
| Published / updated | unknown / 2026 |
| Ingestion basis | Official GitHub documentation inspected for the artifact-steward and personal-hive external literature queues; no runner was registered from this repository. |

## Thesis

Self-hosted runners are a near-term substrate for project stewards and personal hives because they let user-managed machines execute workflow jobs. They also expose maintenance, isolation, and trust responsibilities that the book must make explicit.

## Mechanisms

- Let a user deploy and manage systems that execute GitHub Actions jobs.
- Support physical, virtual, containerized, on-prem, or cloud machines.
- Provide more control over hardware, OS, and tools than GitHub-hosted runners.
- Put operating-system, software, machine-maintenance, and cost responsibility on the runner owner.

## Evidence

- The official docs describe self-hosted runners as user-managed systems with custom hardware/software control and explicit maintenance responsibility.
- This repository has not registered a runner, executed jobs on a personal machine, or tested runner isolation.
- Use this source for the "assigned compute / self-hosted CI" pattern only.

## Failure Modes

- Repository jobs can gain access to machines whose local trust boundary is misunderstood.
- Self-hosted runner reuse can leave state between jobs unless isolated.
- Runner ownership and project authority can blur without a work contract and sandbox manifest.

## Book Chapters Supported

- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use this note to ground self-hosted CI as an implementation candidate for project stewards and project hives.
- Do not claim unattended runner safety without sandbox, credential, cleanup, and audit evidence.

## Open Questions

- What runner labels should correspond to `DeviceResourceCard` trust tiers?
- How should a steward prevent untrusted PR jobs from reaching private machines?
- Which runner logs are sufficient evidence for a work contract?
