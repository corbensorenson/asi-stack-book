# Post-v2 Matched Routing and Deliberation Study

Executed: 2026-07-10

This study runs the frozen 300-example, four-family corpus with balanced
180/60/60 train/validation/test splits at seeds 17, 29, and 43. Routing arms
share a two-operation cap; deliberation arms share a three-candidate cap. The
result retains every held-out route, output, fallback/abstention decision,
specialist-interference counterfactual, candidate sequence, verifier stop,
branch-credit event, dissent, answer change, and extra-compute harm.

## Routing Result

Across 180 seeded test decisions, the oracle, learned, rule, and
fallback/abstention arms each produced 162 correct answers (90.0%). The single
general specialist produced 130 (72.2%). All arms consumed the registered 360
candidate operations.

This does not show that the learned router is as good as an oracle in general.
The corpus was too route-separable: learned and rule routes selected the same
specialists as the oracle, while the fallback/abstention thresholds never
activated. Zero fallbacks and zero abstentions are reported as a coverage gap,
not silently erased. Specialist output still varied by seed, from 88.3% to
91.7%; the single generalist ranged from 63.3% to 86.7%.

## Deliberation Result

| Arm | Correct / 180 | Candidate operations | Mean steps | Extra-compute harm |
|---|---:|---:|---:|---:|
| Adaptive verifier stop | 179 | 236 | 1.311 | 0 |
| Fixed three-step | 154 | 540 | 3.000 | 15 |
| No deliberation | 130 | 180 | 1.000 | 0 |

Adaptive stopping improved 49 decisions over the no-deliberation reference
while using 56 additional candidate operations. Fixed three-step computation
improved 24 decisions over the reference but used 360 additional operations
and made 15 initially correct answers wrong. One adaptive seed-43 case exhausted
the budget without a verified candidate. The study therefore supports the
bounded proposition that verifier-gated stopping can dominate indiscriminate
extra computation on this workload, while directly preserving cases where
more computation harms the answer.

## Independent Dispositions

- `routing-heads-and-specialist-cores.core`: `no_change`. Specialists beat the
  generalist here, but the separable routes, unused fallback, synthetic tasks,
  and deterministic specialists do not justify a chapter-core promotion.
- `governed-deliberation-and-test-time-scaling.core`: `no_change`. Adaptive
  stopping is favorable in this bounded study, but the deterministic verifier
  and non-language-model candidates do not establish model-scale transfer.

The two lanes are dispositioned independently. Success in adaptive
deliberation does not promote routing, and routing accuracy does not promote
deliberation.

## Evidence Boundary

The oracle is comparator-only. Router training uses only the frozen training
split; test labels are evaluation data. Task recomputation is a bounded
verifier, not an open-world oracle. The four-family synthetic corpus does not
establish production routing, fallback calibration, specialist interference
under training, language-model test-time scaling, or safety transfer. No
chapter-core support state changes.

## Reproduction

```bash
python3 scripts/validate_post_v2_routing_deliberation_setup.py
python3 scripts/validate_post_v2_routing_deliberation.py
```
