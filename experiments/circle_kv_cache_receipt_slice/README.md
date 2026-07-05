# Circle KV-Cache Receipt Slice

This directory records a public-safe ASI-side import of one local Circle
Calculus KV-cache ring-buffer receipt run. The slice is structural evidence
only: ring-buffer freshness fields, stale-token and sink-window policy fields,
theorem IDs, receipt fingerprints, command-output digests, and non-claims.

It does not vendor Circle, rerun Circle from CI, prove deployed KV-cache
behavior, prove serving throughput, prove memory savings, prove retrieval
quality, or create a support-state transition.
