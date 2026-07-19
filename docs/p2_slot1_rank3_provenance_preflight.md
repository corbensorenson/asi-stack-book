# P2 Slot 1 Rank 3 Provenance Preflight

Date: 2026-07-17  
Disposition: **N0 provenance failure before task content was opened**

The third frozen Rust candidate is a real merged public change whose exact base
is the merge parent, and its permissive license and image manifest are
resolvable. However, GitHub reports both the merge commit and the pull-request
head commit as unsigned. The rank-1 provenance contract required a verified
public-change commit; that gate is not weakened after candidate selection.

The task specification, test command, image runtime, and execution outcome were
not opened. No image pull is needed after a terminal provenance failure. This
N0 exclusion is not a quality judgment about Gleam or the change and has no
claim-support or claim-refutation effect. Slot 1 advances to frozen rank 4; the
final pool remains unselected and unopened.

Machine record: `evidence_quality/p2_slot1_rank3_provenance_preflight.json`.
