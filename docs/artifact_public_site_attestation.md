# Artifact Public-Site Attestation

Validation command:

```bash
python3 scripts/validate_artifact_public_site_attestation.py
```

The local capture command for the current result was:

```bash
python3 scripts/validate_artifact_public_site_attestation.py --write-result
```

The generated result is:

`experiments/artifact_public_site_attestation/results/2026-07-05-live.json`

The accepted no-promotion decision is:

`evidence_transitions/v1_x_measured/artifact_public_site_attestation_no_change.json`

Result id:

`artifact-public-site-record-reality-attestation-2026-07-05`

Public URL:

`https://corbensorenson.github.io/asi-stack-book/chapters/artifact-graphs-audit-logs-and-replay.html`

Captured digest:

`8732d88da373a8135310bbaae3c9302b0a44423648028a3c7833cde373072c5c`

## What Is Checked

The probe fetches the public GitHub Pages Artifact Graphs chapter and records
HTTP status, final URL, response metadata, byte length, content digest, and
required text fragments. The current fetch observed status `200`, content type
`text/html; charset=utf-8`, ETag `"6a4a066a-46f6b"`, last-modified header
`Sun, 05 Jul 2026 07:23:22 GMT`, and `290667` bytes.

The required fragments check that the deployed public page contains the
Artifact Graphs title, the record-reality authority ladder, the epistemic TCB
boundary, the GitHub Pages CI attestation section, the live and randomized
attestation probe references, and the explicit boundaries that this is not a
deployed attestation service, not independent external human review, not reader
release approval, and not Artifact Graphs chapter-core support.

## Boundary

This is public deployed-site evidence for one fetched URL at one time. It is
useful because the record-reality treatment is not only present in local files;
it is also served from the public book site.

It is still not independent external human review, not open-world receipt
faithfulness, not deployed attestation behavior, not verifier correctness, not
reader release approval, not future-commit status, and not an upward support
movement. It can block a narrower overclaim: the book cannot describe the
Artifact Graphs public record-reality treatment as local-only after this fetch,
but it also cannot treat a served HTML page as proof that the underlying
attestation system exists.
