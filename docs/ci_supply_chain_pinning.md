# CI Supply-Chain Pinning

Last updated: 2026-07-10

All GitHub Actions in the validation and Pages workflows are pinned to full
commit SHAs. Human-readable major tags remain comments only. The current pins
were resolved from the official GitHub repositories:

| Component | Pinned commit | Tag context |
|---|---|---|
| `actions/checkout` | `34e114876b0b11c390a56381ad16ebd13914f8d5` | `v4` |
| `actions/setup-python` | `a26af69be951a213d495a4c3e4e4022e16d87065` | `v5` |
| `actions/setup-node` | `49933ea5288caeca8642d1e84afbd3f7d6820020` | `v4` |
| `quarto-dev/quarto-actions/setup` | `8a96df13519ee81fd526f2dfca5962811136661b` | repository tag `v2` |
| `actions/upload-pages-artifact` | `fc324d3547104276b827a68afc52ff2a11cc49c9` | `v5` |
| `actions/deploy-pages` | `cd2ce8fcbc39b97be8ca5fce6e763baed58fa128` | `v5` |
| `actions/upload-artifact` | `ea165f8d65b6e75b540449e92b4886f43607fa02` | `v4` |
| `actions/download-artifact` | `634f93cb2916e3fdff6788551b99b062d0335ce0` | `v5` |
| `leanprover/elan` installer | `6737edca3d2ca3dbaa1b47b87769b48b420633ae` | `master` snapshot resolved on 2026-07-10 |

The Elan installer is downloaded from the commit-specific raw URL, stored as a
file, and checked with SHA-256
`a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53`
before execution. Lean itself remains pinned by `lean/lean-toolchain`.

`ci/dependency_pin_inventory.json` is the machine authority for the eight
GitHub Action commits and the Elan installer commit, URL, and digest. Every pin
records its tag context, review date, review due date, review method, update
authority, and residual trusted-computing-base boundary. Reviews expire after
90 days and fail closed; the current inventory is due on 2026-10-08. CI uses
the UTC system date unless `ASI_PIN_REVIEW_AS_OF=YYYY-MM-DD` supplies an
explicit audit date for deterministic replay.

`scripts/validate_ci_supply_chain_pins.py` scans every workflow, rejects remote
actions that are not full-SHA pinned, requires the reviewed commits above,
rejects actions absent from the machine inventory, checks the installer URL and
digest ordering, enforces review age and due-date arithmetic, and runs seven
negative controls: a moving action tag, mutable installer URL, removed checksum,
stale review, missing inventory action, mismatched inventory pin, and duplicate
inventory ID.

## Update procedure

1. Resolve the intended official tag or release to a full commit SHA.
2. Review upstream release notes and the diff from the existing pin.
3. For downloaded installers, fetch from the commit URL and independently
   calculate the file digest; never update the URL without the digest.
4. Update every workflow occurrence, `ci/dependency_pin_inventory.json`, and
   this ledger in one change. Set `reviewed_on` to the actual review date and
   `review_due_on` to exactly 90 days later.
5. Run registry PR and deep tiers, Lean build, clean Quarto render, rendered
   status validation, and workflow YAML parsing.
6. Record the old/new commits, review evidence, and rollback commit in the PR.

Pinning constrains fetched code identity. It does not prove an action or
installer is benign, free of compromised dependencies, or correct. GitHub's
runner image and transitive network/tool dependencies remain outside the fully
pinned trusted computing base and should stay explicit residuals.
