# Runtime Adapter Effect Replay Probe

This directory stores the result record for a public-safe local runtime-adapter
effect replay over a generated temporary file outside the repository.

The result records gate decisions, pre/post/rollback hashes, a rollback-exact
restoration check, and missing-permission plus expired-approval no-mutation
controls. It does not store temporary file contents, private paths, private
source text, private keys, secrets, or external-service payloads.

This is not a deployed adapter test, not a sandbox test, not an approval-service
test, not a secret-handle test, not a revocation-propagation test, not a
rollback-service test, not a benchmark, and not a chapter-core support-state
promotion.
