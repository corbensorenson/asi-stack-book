# Agent reading regression, 28 November 2026

The candidate passed all four frozen gates. Across 24 fresh questions, it earned 69 of 72 rubric points compared with 66 for the direct-link baseline and used 8,688,346 deduplicated bytes compared with 18,452,674, a 52.9% reduction. The additional credit came from a single BridgeKV question. Both editions missed the ByteFlow result. [Frozen protocol](../protocol.md) · [Question panels](../panels) · [Rubric](../rubric.md) · [Machine-readable scores](scores.json)

## Comparison

Six matched panels used two fresh sessions each. Both sessions in each pair received the same four questions, inherited model configuration, opening page, reader and budget. Sessions were dispatched separately without shared conversation history. One reviewer applied the frozen rubric with edition labels visible. The baseline was the public direct-link edition at `d5d8c2f7`; the candidate was the public compact lookup and enriched export edition at `552fb37f`. The full source revisions, artifact identities and checksums are in the frozen suite. [Original suite](../suite.json)

| Panel | Baseline score | Candidate score | Baseline deduplicated bytes | Candidate deduplicated bytes |
|---|---:|---:|---:|---:|
| Assurance | 12/12 | 12/12 | 1,683,230 | 1,481,003 |
| Authority | 12/12 | 12/12 | 1,385,162 | 422,781 |
| Formal scope | 12/12 | 12/12 | 757,683 | 331,088 |
| Generation and compression | 6/12 | 9/12 | 10,607,664 | 2,991,275 |
| Scientific evidence | 12/12 | 12/12 | 1,326,855 | 1,870,436 |
| Forward transfer | 12/12 | 12/12 | 2,692,080 | 1,591,763 |
| **Total** | **66/72** | **69/72** | **18,452,674** | **8,688,346** |

| Measure | Baseline | Candidate |
|---|---:|---:|
| Correct decisions | 22/24 | 23/24 |
| Determining citations | 22/24 | 23/24 |
| Relevant scope statements | 22/24 | 23/24 |
| Unsupported numerical assertions | 0 | 0 |
| Opens, including unavailable routes | 95 | 82 |
| Full uncompressed bytes across all successful fetches | 22,320,049 | 11,365,895 |
| Bytes displayed to agents | 293,583 | 259,109 |

The scorer counts each distinct payload once per session when calculating deduplicated bytes. It charges the same full payload to the raw total every time it is fetched. Displayed bytes measure the excerpts delivered through the harness. They fell 11.7%. Neither measure supplies network transfer, model token billing or review time. The descriptive 95% panel-resampling intervals were 0.0 to 1.5 additional quality points per panel and 4.10 MB to 0.08 MB fewer deduplicated bytes per panel. The intervals resample the six observed pairs and do not estimate variation across independently sampled task sets or model configurations. [Scoring implementation](../regression.py)

## Where the result came from

- The candidate used fewer deduplicated bytes on five panels. Generation supplied most of the savings after the baseline opened a 7.57 MB evidence catalog. The candidate still used 27.4% fewer bytes across the other five panels, where both editions earned all 60 rubric points. [Baseline generation journal](generation-baseline-opens.json) · [Candidate generation journal](generation-candidate-opens.json)
- The science candidate cost 41.0% more for the same score. It opened the dictionary, chapters and full study pages before it reached the compact lookup. The authority and formal candidate sessions used the compact lookup near the start. These traces identify routes worth testing again. Each panel has one session per edition. [Science candidate journal](science-candidate-opens.json) · [Authority candidate journal](authority-candidate-opens.json) · [Formal candidate journal](formal-candidate-opens.json)
- Only the candidate found the BridgeKV measurement and distinguished its A40 result from the simulation. Both editions missed ByteFlow's determining chapter passage and training scale. The candidate answered the split-budget intuition and explicitly left the reported result unresolved. [Baseline generation answers](generation-baseline-answers.md) · [Candidate generation answers](generation-candidate-answers.md) · [Candidate grades](generation-candidate-grades.json)

The questions were held out from the preceding agent comparisons. The underlying chapters and studies were familiar subjects. One unblinded reviewer graded one session per edition and panel. The result establishes performance for these sessions and questions. Use the frozen panel for regression checks and keep new evaluation questions separate from any retrieval tuning.

## Audit

The run retains the 12 answer sheets, Boolean grades, and read journals. It also retains the tested manifests and the exact site assets needed to reproduce the logged excerpts and byte counts. The offline replay reproduces the original per-panel and aggregate metrics and all four gates. The original and replay suite hashes identify their respective archives. [Replay instructions](../README.md#audit-a-retained-run) · [Replay suite](replay-suite.json)
