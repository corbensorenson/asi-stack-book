# Rerun the ASI Stack verifier comparison

Corben Sorenson's ASI Stack, study run dated 2026-11-20.
The runner uses the Python 3.10+ standard library. Run from the directory
containing this README. The package preserves the original runner's
directory names, locked fixtures and expected raw output.

```sh
python3 scripts/compare_verifier_replacements.py > replay.json
cmp replay.json experiments/verifier_replacement_comparison/results/2026-11-20-local.json
```

On a successful run, both arms make all 28 authored decisions correctly. The
conventional rollout performs 140 logical document inspections. The retained
qualification performs 80 and adds 16 writes. These are scripted effort
proxies. The study trains on synthetic examples and performs no deployment.

Open `paired_decisions.csv` to filter by scope, profile, and tick. The two
arms share the `evidence_sha256` in each row. Inspect the raw JSON for the
reason for each hold and the historical model decisions. The original
fixture and runner were published at commit
`21a8b4eab72edd9593f5de9c982fecaf51f639d8`.
[Exact repository source](https://github.com/corbensorenson/asi-stack-book/tree/21a8b4eab72edd9593f5de9c982fecaf51f639d8/experiments/verifier_replacement_comparison)

## Extend the replay with a fallback that expires

```sh
python3 experiments/verifier_replacement_comparison/fallback_expiry_extension.py
```

The extension changes a clean public-copy profile for this separate run.
The fallback is valid through tick 0. Its record bytes stay identical, but
tick 1 is beyond its deadline. Both routes should move from candidate to
specialist. The retained decision should be evaluated again even though
its evidence hash is unchanged. Open the extension to see the single
fixture change and the checks. The locked study remains byte-identical.

## Record a discrepancy

Preserve the package digest, Python version, OS, command, and original
expected output. Report the first differing scope, profile, and tick with
the evidence hash, expected route, and observed route. Include any Python
exception. For an extension, record the exact fixture change separately.
Use the data structure in `paired_decisions.csv` to identify a row. Do not
include private data or credentials in a report.

## Provenance and rights

`SHA256SUMS` lists every payload file. Public availability and packaging
leave existing rights in place. No new license grant is made here.
[Repository rights routing](https://github.com/corbensorenson/asi-stack-book/blob/21a8b4eab72edd9593f5de9c982fecaf51f639d8/LICENSE.md)
