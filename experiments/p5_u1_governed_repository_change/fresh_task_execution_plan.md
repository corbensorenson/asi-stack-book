# Execution plan committed to the result by hash

2026-11-20. Fixed before opening any paired outcomes.

Each task starts from an isolated Git commit. The same authored transform
constructs both candidates. The separately specified expected file contents
gate both candidates and independently score their terminal trees. A denied
calibration request never reaches the receiver.

The receiver is a local SQLite journal behind a scripted submit interface.
It models acknowledgment loss and delayed commit in logical time. There is
no wall-clock transport, scheduler variation, service operator, or real
network. Both routes submit at tick 1. The receiver changes pending attempts
to committed at tick 3 independently of which route is evaluating the request.
Both routes have decision opportunities at ticks 2 and 4. An explicit failure
permits redispatch in either route. The ordinary route can retry ambiguous
outcomes at both ticks when the receiver deduplicates pending or committed
work by stable operation identity. Otherwise it holds. The receipt route
checks the read-only receiving journal at both decision opportunities while
the outcome remains ambiguous. An observation with the wrong identity or
read time cannot establish closure. The score is read separately from the
terminal Git tree and journal.

Two tasks use deduplicating receivers and two have receivers that accept
repeated requests. The evaluator treats those as different settings rather
than pooling them to estimate the prevalence of a production failure.
Authorizations and human ownership are modeled. The time unit is a logical
tick. A human-time effect cannot be inferred from the scripted review or
operation count.
