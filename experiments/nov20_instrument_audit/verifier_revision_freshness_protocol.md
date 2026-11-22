# A successful response can carry an old verifier decision

Replay the archived positive control with its stipulated scores and publish
two complete in-process evidence snapshots. In the second snapshot, the
candidate's approval has been revoked. The prior verifier still meets the
required floor for this fixture. Both workflows use the same snapshots,
case and label reference, scope, expiry, and order of lookups.

A separate input gives each request the exact current evidence revision for
its scope. The fixture supplies this input directly. An implementation would
need to establish it independently of the possibly delayed index, and define
how long the request can rely on it. Both workflows check the exact revision
before reading cached policy. When the index is unavailable, returns another
revision, or the request has no trusted revision, the expected decision is
to send the case to the specialist.

Run two consumers for three logical ticks per profile. First warm both caches
on the approved snapshot. Then exercise a missed notification followed by
a current response, a successful old response, an unavailable index, a
successful response without a trusted request revision, and a return to an old
revision after seeing the current one. Score candidate, prior, and specialist
routes against the declared profile. Retain each decision and work counts for
index lookups, evidence reads, policy evaluations, cache writes, and serialized
handoff bytes. Rerun byte-for-byte with the existing locked inputs.

```sh
python3 experiments/nov20_instrument_audit/check_verifier_revision_freshness.py
```

This is a deterministic check of one policy against authored responses.
The two cache representations share the freshness rule and the trusted
request input. The check leaves publication and claim support at their
existing levels. The cost of obtaining that input, actual process transport,
concurrent updates, and human review remain open.
