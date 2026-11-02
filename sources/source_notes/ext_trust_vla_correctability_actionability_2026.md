# Source Note: When Reasoning Helps Action: Monitoring and Steering Chain-of-Thought in Vision-Language-Action Policies

| Field | Value |
|---|---|
| Source ID | `ext_trust_vla_correctability_actionability_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.00601v1](https://arxiv.org/html/2610.00601v1) |
| Citation | Karnik et al. (2026), When Reasoning Helps Action |
| Published / updated | 2026-09-30 / 2026-09-30 |
| Review scope | Introduction, TRUST monitoring/steering description, Section V-B manipulation outcomes and reasoning-substitution protocol. Selected driving comparison scope from abstract/introduction. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Improving an embodied policy’s textual reasoning and improving its resulting actions are separate empirical questions.

## Mechanisms

An offline-trained prefix value model monitors likely reasoning errors and steers token sampling while leaving the VLA policy frozen. Correctability and actionability are measured separately; reasoning substitution probes behavioral dependence.

## Evidence

Reports driving improvements on a baseline-selected difficult AlpaSim subset, but improved grasp/action reasoning leaves aggregate LIBERO-Plus task success largely unchanged. Both harmful and beneficial episode flips remain.

## Failure Modes

These are particular VLA/simulator comparisons, not physical safety certification. Sensitivity to text does not establish intended causal correction; aggregate similarity is not proof of exact invariance or equivalence.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

Which corrected claims reliably change the intended action across actual controller, sensor, timing and distribution boundaries?

## Book Chapters Supported

- `embodied-agency-real-time-control-and-physical-safety`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
