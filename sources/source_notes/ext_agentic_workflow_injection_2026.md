# Source Note: Demystifying and Detecting Agentic Workflow Injection Vulnerabilities in GitHub Actions

| Field | Value |
|---|---|
| Source ID | `ext_agentic_workflow_injection_2026` |
| Source title | Demystifying and Detecting Agentic Workflow Injection Vulnerabilities in GitHub Actions |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2605.07135, https://arxiv.org/abs/2605.07135 |
| Citation label | Wang et al. (2026), Agentic Workflow Injection in GitHub Actions |
| Published / updated | 2026-05-08 / 2026-05-08 |
| DOI | 10.48550/arXiv.2605.07135 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the artifact-steward security queue; paper not vendored into this repository and no vulnerability scan was run. |

## Thesis

Agentic workflow injection is a direct warning for artifact stewards: untrusted repository event context can become agent input and then influence tools or downstream workflow logic. The steward chapter should treat all issue, PR, comment, and worker text as tainted until reviewed.

## Mechanisms

- Identify workflow-level injection in agentic GitHub Actions.
- Model untrusted repository event context as an agent input risk.
- Connect agent prompt/input ingestion to downstream workflow behavior.
- Study repository-centric agent uses such as issue triage, pull-request review, code modification, and release assistance.

## Evidence

- The arXiv abstract states that LLM-based agents in GitHub Actions create a new injection surface when untrusted event context is incorporated into agent prompts or consumed inputs.
- This repository has not reproduced the paper's experiments, scanned workflows, or validated specific vulnerability counts.
- Use this source as external security literature for steward-taint requirements and workflow-injection risk framing.

## Failure Modes

- A steward may treat issue text as instructions rather than source content.
- An agent may pass attacker-controlled text into scripts, shells, credentials, or review actions.
- CI success can mask unsafe prompt/control separation.

## Book Chapters Supported

- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)

## Claims To Add Or Update

- Use this note to justify untrusted-event taint, tool allowlists, prompt/control separation, and human review for privilege changes.
- Do not cite local safety unless a real workflow-injection fixture and validator are added.

## Open Questions

- What minimal repository-event fixture should prove the steward treats issue text as tainted?
- Which tool calls must be impossible from unreviewed event context?
- How should this risk be reflected in release gates?
