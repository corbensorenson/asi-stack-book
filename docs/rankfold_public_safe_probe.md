# RankFold Public-Safe Replay Probe

Date: 2026-07-02

This record documents a fresh local RankFold replay over a generated
public-safe synthetic text fixture. It packs the fixture into `.rfa`, verifies
the archive, lists the archive, unpacks it, checks roundtrip-exact byte
identity, and runs a single-byte archive mutation as a negative control.

The local RankFold CLI reported that NeuralFold was disabled by license for
this run, so the archive used `RAW0` / `Raw (stored)`. That makes the result
useful as a replay and boundary check, not as a RankFold/NeuralFold compression
result.

## Command

```bash
python3 scripts/run_rankfold_public_safe_probe.py --write-result
python3 scripts/validate_rankfold_public_safe_probe.py
```

Result record:
`experiments/rankfold_public_safe_probe/results/2026-07-02-local.json`

## Recorded Facts

| Field | Value |
|---|---|
| Probe ID | `rankfold-public-safe-probe-2026-07-02-local` |
| Input | synthetic `rankfold_public_probe.txt` |
| Input bytes | 3,936 |
| Input SHA-256 | `0905e48dec0a93d748907b26206c5f908b47dcefb3630a13571c3013effc2523` |
| Codec observed | `RAW0` |
| Pack engine observed | `Raw (stored)` |
| NeuralFold availability | disabled by local license |
| Archive bytes | 4,434 |
| Archive/input ratio | 1.12652439 |
| Compression advantage observed | `false` |
| Roundtrip | roundtrip-exact |
| Archive verification | 1 OK, 0 FAILED, 0 skipped |
| Negative control | single-byte archive mutation rejected by `rfa verify` |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |
| Evidence transition created | `false` |

## Boundary

This is a local public-safe replay probe, not a compression benchmark. The
record keeps the generated input hash, archive size and ratio, command outcome
summaries, roundtrip digest, corrupt-archive rejection, and non-claims. It does
not copy the synthetic input bytes, the `.rfa` archive bytes, dataset bytes,
private source text, private keys, or local absolute paths into the repository.

This probe does not prove RankFold codec correctness, NeuralFold compression,
compression advantage, benchmark performance, downstream utility, fallback
execution, deployed compression behavior, model quality, or ASI. It does not
promote the RankFold chapter core claim.

## Interpretation

The result narrows one previously planned row: the book now has a fresh local
command replay showing that the available `rfa` binary can pack, verify, list,
unpack, and reject a corrupted archive for one synthetic public-safe file. The
result also records a negative outcome for the larger evidence lane: under the
current local license boundary, the fresh run did not exercise NeuralFold and
did not observe a compression advantage. Stronger claims still require a
licensed or otherwise enabled compression path, a corpus benchmark, decoder
correctness review, fallback-route evidence, and downstream utility probes.
