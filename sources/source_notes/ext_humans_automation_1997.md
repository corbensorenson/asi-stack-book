# Source Note: Humans and Automation: Use, Misuse, Disuse, Abuse

| Field | Value |
|---|---|
| Source ID | `ext_humans_automation_1997` |
| Source title | Humans and Automation: Use, Misuse, Disuse, Abuse |
| Ingestion date | 2026-07-03 |
| Source version / URL | https://sage.cnpereading.com/doi/10.1518/001872097778543886 |
| Citation label | Parasuraman and Riley (1997), Humans and Automation |
| Published / updated | 1997-06 |
| DOI | 10.1518/001872097778543886 |
| Ingestion basis | Primary metadata and abstract inspected; paper not vendored or reproduced. |

## Thesis

Human oversight degradation is not an implementation footnote. Parasuraman and
Riley frame automation in terms of use, misuse, disuse, and abuse. For the ASI
Stack, that makes a human approval record a control surface whose quality
depends on trust, workload, false alarms, risk, role assignment, and monitoring
conditions rather than a generic proof that a human meaningfully reviewed an
action.

## Mechanisms

- Overreliance can produce monitoring failures and decision bias.
- False alarms and poor trust calibration can cause disuse.
- Automation design can assign humans brittle supervisory roles.
- Human approval gates therefore need workload, scope, role, alert quality,
  and non-claim fields.

## Evidence

The source is external human-factors literature, used here for conceptual and
comparative grounding only. The book does not reproduce the paper's evidence or
claim a local experiment in human automation use.

## Failure Modes

- Treating a clicked approval as proof of meaningful review.
- Ignoring approval fatigue, alert fatigue, and trust calibration.
- Designing a gate that leaves humans responsible for impossible monitoring
  duties.
- Promoting chapter support because a human approved a fixture or action.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`
- `human-intent-as-a-formal-input`
- `evidence-states-and-claim-discipline`
- `human-factors-and-meaningful-control-in-oversight`

## Claims To Add Or Update

- Add Human oversight degradation as a bounded idea: approval can fail through
  misuse, disuse, abuse, fatigue, rubber-stamping, and automation bias.
- Keep the claim at argument/source-grounded positioning unless a local or
  external human-factors result is actually imported.

## Open Questions

- What reviewer-load thresholds should trigger delay or reviewer rotation in
  a real adapter service?
- Which approval traces are public-safe enough to publish without exposing
  private review behavior?
- How should reviewer-quality evidence be audited without creating a new
  reviewer surveillance problem?
