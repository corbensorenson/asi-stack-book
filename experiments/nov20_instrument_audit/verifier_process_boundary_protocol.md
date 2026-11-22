# Verifier freshness across a process boundary

In the in-process revision check, the request already knows the current
revision. Here a separate authority process controls a scoped revision
pointer. It starts at the approved snapshot and receives an explicit
revocation update. The test controller asks that process for the current
pointer before every decision. It forwards the scoped response to a cache
worker process. The worker uses an index view that may be behind or
unavailable. The index view never supplies the authority response.

Run the five profiles from the in-process check and one additional profile in
which the fallback expires after revocation. Keep acquisition, the exact
request scope and revision, policy, evidence, scenarios, interprocess
transport, and response fields the same in both arms. In one worker, keep
the memo as a Python object. In the other, store the exact qualification as
serialized bytes. Count actual request and response payload bytes and
messages for the authority and worker pipes. Count evidence reads,
evaluations, and bytes written to the in-memory cache separately. Pipe
framing, work-counter collection, process startup, and wall time are outside
those counts.

Compare both arms against the required route declared for each profile,
including expiry. Run the same command twice and compare its report bytes.

```sh
python3 experiments/nov20_instrument_audit/check_verifier_process_boundary.py
```

The controller sequences updates between decisions. All processes have the
same local owner, and only the pointer lives in the authority process.
Index delays and failures are prescribed by the fixture. The comparison
leaves concurrent updates between authorization and effect, independent
operators, network latency, cache persistence after a restart, and production
fault isolation open.
