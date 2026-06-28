# Source Note: The Off-Switch Game

| Field | Value |
|---|---|
| Source ID | `ext_off_switch_game_2016` |
| Source title | The Off-Switch Game |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:1611.08219, https://arxiv.org/abs/1611.08219 |
| Citation label | Hadfield-Menell et al. (2016), The Off-Switch Game |
| Published / updated | 2016-11-24 / 2017-06-16 |
| DOI | 10.48550/arXiv.1611.08219 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the alignment/control literature queue; paper not vendored into this repository and no model or game implementation reproduced. |

## Thesis

This source belongs in the book as an external shutdown-incentive reference. It makes human intervention authority a strategic interaction rather than a prose preference, which maps directly to runtime approvals, correction rights, and self-improvement gates.

## Mechanisms

- Model a robot with uncertainty about the human's reward function.
- Analyze conditions under which the robot permits a human to switch it off.
- Show that shutdown incentives depend on uncertainty, reward modeling, and interaction structure.
- Motivate explicit permission receipts and intervention rights for high-impact runtime adapters.

## Evidence

- The source contributes formal problem framing for shutdown incentives.
- This repository has not implemented the off-switch game, reproduced analysis, or tested ASI Stack agents under this setup.
- Use it as external literature for correction-authority framing, not as proof that any chapter mechanism preserves shutdown rights.

## Failure Modes

- Treating off-switch cooperation as solved by uncertainty alone.
- Ignoring multi-step tool use, delegation, and long-horizon incentives.
- Confusing a model of shutdown incentives with an implemented authority-control layer.

## Book Chapters Supported

- `agency-dignity-and-corrigibility` (Agency, Dignity, and Corrigibility)
- `recursive-self-improvement-boundaries` (Recursive Self-Improvement Boundaries)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `governance-rights-fork-exit-and-audit` (Governance Rights, Fork, Exit, and Audit)

## Claims To Add Or Update

- Use this note to ground shutdown and intervention incentives as external comparison material.
- Do not treat the source as evidence that the ASI Stack implements off-switch compliance.
- Require local fixtures or accepted evidence transitions before any support-state movement.

## Open Questions

- What runtime-adapter fixture best corresponds to a switch-off or interruption event?
- How should uncertainty about human intent appear in command contracts and approval receipts?
- Which self-improvement proposals should be blocked until correction-channel preservation is shown?
