# A current approval can expire before the effect commits

The verifier process comparison refreshes the revision before computing a
decision. This check asks what happens when revocation commits after that
decision and before its effect. Use a disposable SQLite database and
separate authority and worker processes. The database journal records a
synthetic effect row.

Compare reusing the cached permission with an ordinary transaction that
checks the exact grant revision and approval in the same write transaction
as the effect. Also run the same transaction with a serialized receipt
instead of an in-memory memo. Both transactions use the same scope, action,
approval state, deadline, and effect store.

Exercise four orders. Let the effect commit before revocation and observe
it afterward. Revoke before the permission check. Revoke after the check
and before the effect. Let the permission expire between the check and
effect. Score the stored effect against the grant state at the actual
write, and then read it again after the scheduled revocation. A delayed
read supplies evidence about an earlier effect without changing its
authorization.

```sh
python3 experiments/nov20_instrument_audit/check_authority_effect_ordering.py
```

The controller forces the event order. The two processes share one owner
and one transactional database. The test leaves contention performance,
partitioned authority and effects outside the transaction open.
