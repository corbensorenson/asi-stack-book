# Receiver availability comparison

Four authored task lineages produced 288 paired cells and 864 arm
observations. Eight calibration checks passed. The same protocol and
input hashes produced identical results on two local runs. Wall-time
observations were written separately from the byte-comparable results.

| Measured outcome | Primary only | Additional endpoint | One endpoint with matched access |
|---|---:|---:|---:|
| Verified exact closures | 48 | 80 | 80 |
| False closures | 0 | 0 | 0 |
| Wrong effects introduced | 0 | 0 | 0 |
| Repeat effects introduced | 0 | 0 | 0 |
| Cases held or escalated for an operator | 240 | 208 | 208 |
| Ticks unresolved through the horizon, summed | 816 | 800 | 800 |
| Caller status calls | 288 | 480 | 288 |
| Projection reads | 288 | 480 | 480 |
| Status request and response payload bytes | 45,576 | 75,960 | 130,128 |
| Conditional retries | 24 | 40 | 40 |

The two routes with additional access produced 16 extra closures when
the primary projection was stale and the second was fresh. They produced
the other 16 when the primary projection was unavailable and the second
was fresh. Each of those strata has 32 cells. All three routes gave the
same decisions whenever the primary was fresh. A shared loss of usable
evidence left operations unresolved. The seeded 72 wrong and 72 repeated
effects per arm stayed visible in the terminal journal, including cases
where the workflow held.

The additional endpoint and the conventional endpoint with matched access
agreed on the observation, disposition, terminal effect, decision tick
and operator route in every case. One caller-facing endpoint saved 192
caller status calls. Relaying the same observations increased counted
status payload by 54,168 bytes in these local processes. The measured
tradeoff leaves a choice between fewer caller requests and less total
status transport. Where primary access is fresh enough, retain the simpler
primary-only path. Where a second source changes closure, choose how to
expose it using the burden and failure behavior of the actual deployment.

Local median times from status lookup through disposition and any retry
verification were 0.022 ms for primary only, 0.042 ms for the additional
endpoint and 0.101 ms for the gateway in one run. The measurement excludes
fixture setup, process startup and final scoring. It covers local IPC and
SQLite on one macOS ARM64 host with Python 3.12. Separate processes share
one operator and the same starting operation journal. The comparison
does not measure incident frequency, separately administered faults,
or human effort.

## Replay

```sh
python3 experiments/p5_u1_governed_repository_change/run_prospective_receiver_availability.py > receiver-replay.json
cmp receiver-replay.json experiments/p5_u1_governed_repository_change/results/2026-11-22-prospective-receiver-availability.json
```

Expected result SHA-256
`f23f9e778fe5c64f35275a6813c78abcf3bb92930f2419f89b039891e0cf3cf7`.
See the [fixed protocol](prospective_receiver_availability_protocol.md)
and [inputs](prospective_receiver_availability_inputs.json).
