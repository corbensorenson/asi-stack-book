# CI Supply-Chain Pinning

Last updated: 2026-07-10

All GitHub Actions in the validation and Pages workflows are pinned to full
commit SHAs. Human-readable major tags remain comments only. The current pins
were resolved from the official GitHub repositories:

| Component | Pinned commit | Tag context |
|---|---|---|
| `actions/checkout` | `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0` | `v7.0.0`; Node 24 |
| `actions/setup-python` | `ece7cb06caefa5fff74198d8649806c4678c61a1` | `v6.3.0`; Node 24 |
| `actions/setup-node` | `48b55a011bda9f5d6aeb4c2d9c7362e8dae4041e` | `v6.4.0`; Node 24 |
| `quarto-dev/quarto-actions/setup` | `8a96df13519ee81fd526f2dfca5962811136661b` | repository tag `v2` |
| `actions/upload-pages-artifact` | `fc324d3547104276b827a68afc52ff2a11cc49c9` | `v5` |
| `actions/deploy-pages` | `cd2ce8fcbc39b97be8ca5fce6e763baed58fa128` | `v5` |
| `actions/upload-artifact` | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | `v7.0.1`; Node 24 |
| `actions/download-artifact` | `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` | `v8.0.1`; Node 24 |
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

The first remote PR gate exposed GitHub's Node 20 deprecation shim on the
former action majors. The reviewed pins above move checkout, setup-python,
setup-node, upload-artifact, and download-artifact to their official Node 24
releases. Pages upload/deploy and Quarto setup were already on their current
reviewed releases.

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
