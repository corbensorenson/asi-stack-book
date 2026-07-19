# P2 Dependency Snapshot Rescue Policy

Date: 2026-07-17  
State: **frozen before first network materialization rescue**

The first Rust replacement reached no test outcome: its immutable image lacked
an `indexmap` package in the offline Cargo cache. Rejecting it immediately would
confound image packaging with task validity. The frozen rescue permits only a
checksum-governed instrument repair.

Cargo and Go rescues require two independent, patch-free dependency
materializations from the same digest-bound base. Every registry/module source
must be bound by `Cargo.lock` checksum or `go.sum`; Git dependencies require an
exact commit; custom or unpinned sources fail closed. Each complete dependency
tree is inventoried by relative path, size, and SHA-256. The two normalized
inventories must agree exactly. Both sealed images must then replay the
unpatched dependency check with networking disabled. Only one of those exact
images may be used for all two-by-two paired task arms.

Maven is not treated as equivalent: its rescue remains blocked until a separate
prospective plugin/provider and artifact-checksum plan is frozen. Any rescue
failure keeps the candidate at N0 and advances to the next frozen rank. The
standard cannot be relaxed after a task outcome. The final held-out pool remains
unselected and unopened.

Machine record: `evidence_quality/p2_dependency_snapshot_rescue_policy.json`.
