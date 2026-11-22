# A fresh response can describe an old receiver state

The crossed receiver study gives stale responses their original reading
tick. This check examines a different condition. A caller receives a
response at the current tick, but its payload comes from an older
projection of the same operation. Test with a disposable local journal and
a synthetic document effect.

Both workflows get the same operation identity, one decision opportunity,
retry budget, and response. Compare the archived tick check with a policy
that also requires the response's source revision to match the expected
revision. Exercise a genuine current failure, an old failure after the
operation committed, a current commit, and a current response with no
trusted revision. Repeat the stale-failure case with receiver deduplication
to check whether the same extra attempt actually causes a second effect.
Score committed effects using the terminal journal and the independent
effect scorer from the receiver audit.

```sh
python3 experiments/nov20_instrument_audit/check_receiver_projection_freshness.py
```

The fixture supplies the source revision and exact case identities. It
demonstrates the difference between response time and evidence freshness.
It leaves reliable revision acquisition, production incidence, and
independent receiver operations open. The original study remains unchanged.
