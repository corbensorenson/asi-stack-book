# P2 Replacement Provenance Preflight

Date: 2026-07-17  
State: **rank-one provenance and registry manifests passed; task content and outcomes unopened**

Only rank one in each frozen slot was probed. All four candidates have an exact
base revision, a permissive license file bound to that revision, a public merged
change receipt, and a single-platform Linux/amd64 image manifest with an exact
registry digest. The three Rust/Go candidates have direct GitHub pull receipts
plus verified merge commits. The Java pull endpoint returns unavailable, so it
is not represented as a direct API success: a GitHub-verified merge commit that
names pull 12851, has the frozen base as its first parent, and has the change
commit as its second parent supplies the explicit fallback receipt.

The registry reports 1.06–1.42 GB of compressed layers. Those values are not
expanded image sizes and therefore cannot satisfy the frozen 1.5 GB expanded-
image ceiling. Pull-by-digest, local expanded-size measurement, cleanup, and
host-free-space receipts are the next gate.

Dataset problem statements, solution patches, test patches, test commands, and
gold outcomes remain unopened. Public title-level metadata was incidentally
visible while proving that the Java merge exists and is recorded honestly. No
candidate has entered qualification, and the final held-out pool remains
unselected and unopened.

Machine record: `evidence_quality/p2_replacement_provenance_preflight.json`.
