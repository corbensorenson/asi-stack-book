# Post-v2 Evidence Program Preregistration

Recorded: 2026-07-10

Machine-readable authority:
`experiments/post_v2_evidence_program/preregistration.json`

This freezes the workloads, baselines, arms, metrics, controls, stop rules, and
disposition rules for the three active programs before outcome runs. It is a
required roadmap control, not a substitute for execution.

## Runtime decision

The realistic governed-work flagship will use the locally cached
`Qwen/Qwen2.5-Coder-0.5B-Instruct` model at revision
`ea3f2471cf1b1f0db85067f1ef93848e38e88c25`. A bounded smoke generation
produced an executable clamp implementation, establishing runtime availability
only. The model cache stays outside the repository.

The routing/deliberation program uses a frozen 300-example held-out workload,
three seeds, matched operation budgets, five routing arms, and three
deliberation arms. The update-causality program uses an actual local PyTorch
policy network, 1,200 examples, independent splits, three seeds, three
single-axis challengers, a no-update baseline, fixed probes, and a frozen
deletion cohort.

## Boundaries

All programs accept no-change, narrowing, demotion, and refutation as valid
outcomes. No result may change support before its evidence vector and separate
claim disposition are reviewed. Hardware custody, federation, and Circle/Coil
model quality remain deferred because their real activation infrastructure is
absent; another schema fixture cannot close them.
