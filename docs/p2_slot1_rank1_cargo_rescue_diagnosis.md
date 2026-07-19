# P2 Slot 1 Rank 1 Cargo Rescue Diagnosis

Date: 2026-07-17  
Disposition: **N0 construct/instrument failure; advance to frozen rank 2**

The checksum-governed rescue succeeded at its dependency objective. Two clean,
patch-free materializations each produced 382 lockfile-bound registry archives,
both replayed offline, and their normalized SHA-256 inventories agreed exactly.
The derived images also passed the frozen content, virtual-size, resource, and
cleanup gates.

All four paired task arms then exited before producing a test identity. The two
baseline and two human-gold arms behaved identically, both evaluators agreed on
the empty observation, and no arm reached the test-complete marker. Inspection
of the exact base commit identifies the cause: `make test` enters `test-msrv`,
whose first `run-tests` prerequisite is `rustup component add rustfmt`. The
source Makefile suppresses that command's error output. Because outcome runtime
networking was prospectively frozen to `none`, the prerequisite exits before
Cargo tests begin.

This is not a negative mechanism result. It is an incompatibility between the
task's own test bootstrap and the frozen offline harness. The outcome has now
been opened, so the candidate will not receive a post-outcome command exception
or another relaxed rerun. The frozen policy instead advances slot 1 to rank 2,
which must independently pass the complete provenance, resource, oracle,
evaluator, repeatability, and cleanup sequence. The final pool remains
unselected and unopened.

Machine record: `evidence_quality/p2_slot1_rank1_cargo_rescue_diagnosis.json`.
