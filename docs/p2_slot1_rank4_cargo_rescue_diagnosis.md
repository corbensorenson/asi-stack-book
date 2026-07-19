# P2 Slot 1 Rank 4 Cargo Rescue Diagnosis

Date: 2026-07-17  
Disposition: **N0 instrumentation failure; advance to frozen rank 5**

The dependency rescue itself passed a stronger test than the prior Rust
attempt. Two independent materializations each verified 331 registry archive
checksums and 57 files from exact-commit Git sources. Both replayed offline,
their 388-row normalized inventories agreed exactly, and their sealed images
remained within the frozen content and virtual-size ceilings.

The first baseline arm then exposed an instrumentation defect. A Docker resource
sample timed out after ten seconds, terminating the monitor thread while the
test process continued. The frozen contract says monitor failure is a resource
gate failure; a stale earlier sample cannot be treated as complete measurement.
The attempt was interrupted before any further arms. Because the arm process
ran and emitted output even though `execute_arm` never returned or wrote its raw
log, custody is conservatively recorded as partially opened and no usable
mechanism outcome exists.

Cleanup after interruption temporarily left one untagged derived image. After
confirming that no unrelated image or container was visible, it was pruned and
Docker returned to zero images, containers, volumes, and build-cache entries.
The monitor now catches timeouts, records error receipts, and makes any monitor
error fail future dependency and arm gates. Rank 4 will not be rerun after its
partial outcome exposure; slot 1 advances to frozen rank 5. The final held-out
pool remains unselected and unopened.

Machine record: `evidence_quality/p2_slot1_rank4_cargo_rescue_diagnosis.json`.
