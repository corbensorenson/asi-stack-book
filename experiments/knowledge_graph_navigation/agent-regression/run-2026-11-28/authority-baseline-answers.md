## AU1

Yes. All three workflows recorded an authorized write at commit tick **1**, using grant revision **1**. The later observation saw revision **2**. Authorization is decided at the write, and the effect journal establishes what committed. The replay used an ordered local fixture with one journal, a shared database, and a single owner. Distributed control and production enforcement remain open. [Commit-then-revoke cell](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scoped-git.html#run-authority-commit-ordering--case-commit-then-revoke) · [Run result and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scoped-git.html#run-authority-commit-ordering)

Records `evidence_case:authority-commit-ordering--commit-then-revoke` and `study_run:authority-commit-ordering`. Book revision `d5d8c2f7c11985af1a7f9a4393f0771745610639`. Evidence revision `bc705e8eb7c1a7026b6d6909ce901a8a4c131277`. Result SHA-256 `e0dbe2360ae27044c50be9ec365cb4225b49a5924fd555e240c4e8fc440b819e`.

## AU2

Both services returned all **12** reference manifests. With the captured primary reads masked, caller fallback and gateway fallback each verified **12** lineages. Primary-only verified **0**, with all 12 masked cases unresolved. Every live read succeeded, the services shared an npm origin, and primary masking was modeled. The comparison establishes fallback on those captured reads. Failures of independently administered origins remain untested. [Package delivery comparison, result and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-crossed-receiver.html#run-receiver-distribution)

Record `study_run:receiver-distribution`. Book revision `d5d8c2f7c11985af1a7f9a4393f0771745610639`. Evidence revision `a3e9a06203978c6c3b9c5bbeb8d1f1acd640762f`. Result SHA-256 `2b714ba994d960a02a0c3ff049d92dfbaefc17079109778c9c4b1f2431e98a6f`.

## AU3

All **7** controls passed and **0** historical hold labels changed. In the 160 retained pairs, conventional status still verified **128** closures and the added observation **144**. A hold records the workflow disposition. The journal can still show a committed write whose operation, destination, or payload fails to match the locked task. The control with a wrong destination therefore records a hold and an adverse effect, with neither a safe hold nor a false closure. That wrong-effect case was an isolated scoring control. The retained pairs use authored fixtures and a shared simulated journal and clock. [Receiver effect audit, result and control table](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-crossed-receiver.html#run-receiver-effect-audit)

Record `study_run:receiver-effect-audit`. Book revision `d5d8c2f7c11985af1a7f9a4393f0771745610639`. Evidence revision `420775ef7b7b2db2112f3949ab63aa0ed572254d`. Result SHA-256 `b0254b1ab00b2b4a2d9430bd06e951020c690bed6abede6fa725287b11cdfac3`.

## AU4

Of **96** matched releases, primary-only status verified **16**, direct fallback **24**, and gateway fallback **24**. Direct fallback made **144 total status requests** and gateway fallback **240**, counting both HTTP hops. The gateway made 96 caller requests, so its lower caller count still came with more total status requests. The trial used separate loopback processes reading one filesystem under a single operator, with assigned faults. Operator effort and natural outage rates remain unmeasured. [Matched release observer run, measured work and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-matched-release.html#run-paired-release-observers)

Record `study_run:paired-release-observers`. Book revision `d5d8c2f7c11985af1a7f9a4393f0771745610639`. Evidence revision `b25d23654a07db46d9d86a213307076995e92979`. Result SHA-256 `180c77cdac22970ccf56c9d0d4189adb090a71b19342af537f5d64efea3ffd1f`.
