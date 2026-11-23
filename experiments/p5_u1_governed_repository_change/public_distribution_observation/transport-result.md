# Measured package transport through a gateway

Both placements verified all eight fresh package lineages with live primary
reads and all eight when the primary was withheld before dispatch. The median
paired change under primary withholding was **+1.0 ms** from the caller's first
dispatch to the checked result. Returning the verified manifest through the
gateway added **2,033 HTTP response bytes per verified fallback** across both
hops. This includes response headers and the returned manifest on each hop.
The eight cases passed the prespecified screens. [Protocol](transport-protocol.md) · [Cohort](transport-cohort.json) · [Per-attempt measurements](transport-results.json)

| Condition | Caller / gateway verified | Caller / gateway unresolved | False closures in either arm | Caller / gateway HTTP response bytes |
| --- | ---: | ---: | ---: | ---: |
| Observed | 8 / 8 | 0 / 0 | 0 | 23,203 / 39,774 |
| Primary withheld before dispatch | 8 / 8 | 0 / 0 | 0 | 21,573 / 37,835 |
| Both withheld | 0 / 0 | 8 / 8 | 0 | 0 / 1,192 |
| Wrong-body control | 0 / 0 | 8 / 8 | 0 | 0 / 1,192 |

In the primary-withheld condition, both placements needed eight caller
requests across eight cases. The direct caller skipped the unavailable
route before dispatch. The gateway performed eight additional upstream
requests behind its eight loopback exchanges. This arrangement
covers a known withheld read and leaves actual request loss and delayed
replies open. All attempted live reads succeeded. Every wrong-body control
used a successful response from a different sampled package.

The measured gateway was a real local HTTP process boundary over separately
issued upstream reads. The upstream operators still share the same npm
publication origin. The trial covers one host and time window. The relative
timings include variation in independent network fetches, so the observed
condition's negative median does not identify an acceleration caused by
the gateway. Human operator time remains unmeasured. The [first observation
pilot](result.md) retains its separate modeled request and envelope counts.

To collect another owner-operated transport snapshot with the frozen cohort:

```sh
python3 experiments/p5_u1_governed_repository_change/public_distribution_observation/run_transport.py /tmp/asi-live-transport.json
```
