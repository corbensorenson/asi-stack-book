# Public package delivery observation

The selected 12 public npm package lineages all returned the exact versioned manifest from both jsDelivr and UNPKG. The reference npm tarball matched the integrity in the pinned lockfile for all 12. Primary-only and fallback policies therefore verified 12 of 12 in the observed stratum. This owner-side experiment reads remote production endpoints. It measures receipt at one reader and one time. [Prespecified protocol](protocol.md) · [Cohort](cohort.json) · [Observations and paired outcomes](results.json)

| Replay stratum | Primary alone | Caller fallback | Gateway fallback | False closures in each |
| --- | ---: | ---: | ---: | ---: |
| Observed reads | 12 / 12 verified | 12 / 12 verified | 12 / 12 verified | 0 |
| Primary masked | 0 / 12 | 12 / 12 | 12 / 12 | 0 |
| Both masked | 0 / 12 | 0 / 12 | 0 / 12 | 0 |
| Wrong second-path body | 0 / 12 | 0 / 12 | 0 / 12 | 0 |

When the primary was masked, both fallback routes resolved 12 otherwise unresolved lineages. They used the same 24 service attempts. Gateway placement modeled 12 caller requests, compared with 24 for caller fallback, and charged 1,718 additional status-envelope bytes. The caller path returned 17,023 response-body bytes over the cohort, about 1,419 bytes per recovered closure. Median observed secondary fetch time was 306 ms. The screening conditions passed for this workload, including the requirement to hold on all wrong-body and joint-unavailability cases. The envelope is a modeled serialization cost. The experiment does not compare measured gateway service latency or network overhead.

The wrong and unavailable reads are offline perturbations of collected observations. All actual reads succeeded. The two delivery services maintain distinct observations but rely on the same upstream publication and may share infrastructure with each other or the client. No actual outage frequencies, independent publication origins, release actions, production write effects, or staff time were measured. The detailed record marks human time as unmeasured and retains automated processing time separately. A timed independently operated comparison would still be needed to choose a production topology. [jsDelivr documentation](https://www.jsdelivr.com/documentation) · [UNPKG documentation](https://unpkg.com/) · [Independent receiver follow-up draft](../../../docs/receiver_independent_followup_draft.md)

Replay the read-only observation protocol with a new output file to collect a different snapshot.

The [live transport follow-up](transport-result.md) used eight fresh
lineages and measured the caller-to-decision interval and HTTP response
traffic through a real loopback hop.

```sh
python3 experiments/p5_u1_governed_repository_change/public_distribution_observation/run.py /tmp/asi-receiver-observation.json
```

For an approved timed participant, run the offline review instrument against
the saved observations. Assign one arm and stratum per participant for each
case to avoid crossover learning. The clock runs from the reveal to the
decision, and the record distinguishes verified closures, holds, and decisions
unsupported by evidence the participant opened. The offline timer excludes
actual network waiting and measures only the narrow diagnosis and review task.

```sh
study=experiments/p5_u1_governed_repository_change/public_distribution_observation
python3 "$study/time_operator.py" "$study/results.json" /tmp/receiver-X7.json --arm caller_fallback --stratum primary_unavailable --code X7C
```
