# CI Supply-Chain Pinning

Last updated: 2026-10-10; all nine formal reviews expired October 8 and renewal remains pending.

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

The original Elan shell source and digest
`a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53`
remain **retained review context**, not executed installation code. That source
downloads a moving binary. CI now calls `scripts/install_lean_runtime.py`, which
uses the inventory's `runtime_binary` at `v4.2.4` with explicit platform archives,
byte counts and SHA-256 digests. The Linux x86-64 archive digest is
`42b94d4244e8353142c456ec0e4ca6528fd898a6c604d4059f494e706e431f63`.
All four platform archives were downloaded again on October 3 and passed exact
byte-count, SHA-256 and single-executable layout checks. The Linux ARM64 and
x86-64 executables installed Elan offline and reported the expected 4.2.4
version and source identity in isolated containers; x86-64 was emulated on
the ARM64 host. These installer checks did not download or run Lean. An isolated
macOS Elan 4.2.4 installation built all 133 jobs with the previously installed
pinned Lean compiler. This is local compatibility, not a fresh compiler
download or Linux execution.
The helper rejects moving URLs, mismatched bytes, links, traversal and extra
archive members before execution. Lean remains separately pinned by
`lean/lean-toolchain`; installation receives an explicit tool home and does not
modify the shell profile.

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

`scripts/validate_ci_supply_chain_pins.py` scans every workflow and local composite action, rejects remote
actions that are not full-SHA pinned, requires the reviewed commits above,
rejects actions absent from the machine inventory, checks the governed archive helper and exact versioned URLs/digests, enforces
review age and due-date arithmetic, and runs eleven rejecting controls for
moving/unregistered actions, moving or uncontrolled installation, missing or
malformed binary identity, duplicate platforms, stale review and duplicate
inventory identity. Controls run only after the canonical baseline passes.

The shared `.github/actions/validation-runtime/action.yml` now owns the one
Elan installation definition used by PR, scheduled deep, release and Pages
builds. It provisions Python 3.11, the existing pinned Python requirements,
Quarto 1.9.38 and the toolchain declared by `lean/lean-toolchain`. Each tier
retains full Git history and runs infrastructure regressions. Linux MLX stubs
are preflight adapters; they do not execute or attest MLX experiments.

The HTML publication gate uses `ci/browser/package-lock.json` with Playwright
1.63.0, verified against the official npm metadata on October 2, 2026 (Node
20 or newer). CI installs Chromium and its system dependencies and invokes the
browser check with `--strict --all-chapters --all-viewports`. Missing browser
capabilities therefore fail the publication gate. This change does not renew
the October 8 action-pin review deadline or attest a fresh remote tier run.

## Update procedure

### October 2–3 upstream inspection in progress

Official repository release tags, resolved commits, pin comparisons and public
advisories were fetched on October 2 and independently refreshed on October 3. Raw responses are retained temporarily
under `build/project_review_2026_10_02/dependency-pin-upstream/`; the table below
records the durable findings. This inspection does not renew `reviewed_on` or
the October 8 deadline before the required compatibility checks finish.

| Component | Observed latest official release | Inspected delta and disposition |
|---|---|---|
| checkout | [v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1), `3d3c42e5aac5ba805825da76410c181273ba90b1` | Twelve commits ahead. Source changes constrain ref trimming to ASCII, escape Git unset values and exempt default trusted checkout from the fork guard. All 128 upstream assertions pass on isolated Node 24; retain the current pin until project tier qualification and coordinated replacement finish. |
| setup-python | [v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0), `5fda3b95a4ea91299a34e894583c3862153e4b97` | Eight commits ahead; ESM/toolkit migration, removed pip-install input and explicit manifest-fetch failure. The project does not use the removed input. All 210 upstream assertions pass with the declared 15-second per-case budget, and unchanged published code selects real cached Python 3.11.17 on Linux ARM64/x64. Retain v6.3.0 pending full project qualification. |
| setup-node | [v7.0.0](https://github.com/actions/setup-node/releases/tag/v7.0.0), `820762786026740c76f36085b0efc47a31fe5020` | Twelve commits ahead; ESM, cache-key outputs, readonly cache handling and token/mirror behavior changed. All 225 upstream assertions and a published-bundle macOS ARM64 cached Node 22.15.0 probe pass. Retain v6.4.0 pending configured Linux installation/cache and project tiers. |
| Quarto setup | [v2.2.0](https://github.com/quarto-dev/quarto-actions/releases/tag/v2.2.0) | Exact same commit as the current pin; no source delta. |
| Pages artifact upload | [v5.0.0](https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0) | Exact same commit as the current pin; no source delta. |
| Pages deployment | [v5.0.1](https://github.com/actions/deploy-pages/releases/tag/v5.0.1), `368f82528645a54fb793d4d04e342629a3f51346` | Five commits ahead; inspected polling backoff, jitter and positive interval validation. All 32 upstream assertions pass with mocked HTTP and network disabled by the test transport. Retain the current pin pending coordinated project checks; no deployment was performed. |
| artifact upload/download | [upload v7.0.1](https://github.com/actions/upload-artifact/releases/tag/v7.0.1), [download v8.0.1](https://github.com/actions/download-artifact/releases/tag/v8.0.1) | Both exact current pins. The published download advisory [GHSA-cxww-7g56-2vh6](https://github.com/actions/download-artifact/security/advisories/GHSA-cxww-7g56-2vh6) covers versions 4.0.0 through before 4.1.3; the current v8.0.1 is outside that declared range. Empty advisory lists for the other repositories are not proof of safety. |
| Elan | [v4.2.4](https://github.com/leanprover/elan/releases/tag/v4.2.4), `227caca133724d5516bee25c2aeb3e609478f2d8` | Four commits ahead; idempotent toolchain install, garbage-collection handling and ZIP dependencies changed. The installer script itself has no delta, and its fetched digest still matches the inventory. |

The pinned Elan **script** explicitly downloads from `/releases/latest/`.
Its checksum therefore does not pin the downloaded Elan binary or its
transitive dependencies. Lean's requested toolchain remains fixed separately.
The current runtime replaces that download with the exact release archives
and digest-verifying helper described above. The nested binary observation is
dated October 3 and marked `archive_integrity_verified_linux_installer_smoke_passed_full_tiers_pending`;
it does not backdate binary verification to July or renew any original pin
review deadline. Fresh Linux compiler/tier execution and the broader action compatibility
review remain required before closing A08/B01. Exact archive identity does not
prove benign code, reproducible scientific transitive dependencies or hosted
runner integrity.

### October 3 compatibility observations and limits

The four candidate repositories were fetched at the exact commits above.
Locked dependencies were installed with lifecycle scripts disabled into owned
review directories. Unmodified source assertions ran under the official Node
24.21.0 macOS ARM64 archive after verification against its published SHA-256.
The 595 passing assertions are upstream authored tests, not an independent
security audit. Python's initial default five-second case budget produced one
timeout in the deliberately unavailable-version case: the new API/raw-manifest
retry path has explicit delays. That original 209-pass/one-failure result is
retained. The complete rerun used `--testTimeout=15000`, without changing,
skipping or weakening any assertion; the outer process budget stayed 300 seconds.

The unchanged published checkout bundle also passes three offline conditions
against an owned local Git mirror: an explicit trusted workflow-run commit is
checked out exactly, an explicit fork PR commit in that trusted context refuses
before creating its destination, and default checkout still selects the trusted
event commit during a fork-triggered run. Git is restricted to the file protocol
and Node transport is blocked. The fixture disables safe-directory/global-home
configuration and credential persistence; it does not qualify hosted Git
authentication or the workflow's default global-config behavior. An initial
fixture incorrectly rendered a YAML null default as the literal `None` filter;
Git's rejection and the corrected fixture outcomes are retained separately.

All configured inputs across twelve candidate-action occurrences are still
declared by the candidate metadata. This is static compatibility. Python's
packaged action overrides its cache directory to `/Users/runner/hostedtoolcache`
on macOS. Two local probes failed against that hosted-runner assumption and
remain recorded; neither is counted as a compatibility pass. A network-disabled
Linux replay then used the unchanged packaged entry point, the project's Python
3.11 input and a real cached interpreter. ARM64 ran natively; x86-64 ran through
Docker Desktop emulation. Both exported Python 3.11.17 and executed that selected
interpreter successfully. This does not qualify downloading Python, pip-cache
restore/save, the full shared CI runtime or a hosted Ubuntu runner.

The Linux observations use the [official Python image](https://hub.docker.com/_/python)
resolved to `sha256:2333bd330d12de02514770b3585cad313644316047cdee24a7acfdece6de6efb`,
official Node archives verified against their publisher checksum list, read-only
source mounts, disabled container networking and an owned executable temporary
filesystem. The first Elan post-install version check refused execution on the
non-executable temporary mount; its failure is retained separately from the
passing replay. No user containers, images, volumes or tool homes were replaced.
Docker Desktop was started for these checks and remained running through the
subsequent probes. After all owned containers exited and no live containers
remained, it was stopped to restore its earlier state; images, volumes, runtime
homes and diagnostics were preserved.

The retained Quarto composite source uses explicit Quarto 1.9.38 for this
project, but does not check the downloaded package digest before its privileged
platform installation. TinyTeX is disabled in these HTML workflows. That package
and privileged installer remain residual dependencies; a pinned composite action
does not make the release asset immutable or attest the hosted installation.

The pin checker now reads UTC directly and stops before semantic/workflow
consumption when the inventory schema rejects its shape. Authored regressions
reproduced expiry delayed by a local calendar day and six malformed-input
exceptions before the fix. Four clock/shape controls now pass alongside the
eleven existing canonical rejecting controls. The full local infrastructure
suite passed 177 tests in that phase. Review/observation dates and the audit override must
also retain canonical `YYYY-MM-DD` spelling: compact and ISO-week alternatives
previously parsed successfully despite that contract. Five rejecting subcases
were reproduced before the strict-format repair. Thirty-five existing clock and reader/shared-directory
custody controls also pass on each Linux architecture, including actual Linux
directory exchange, exclusive installation and process-interruption behavior.
These are selected mechanism tests; archive/product integration, admission,
all governed tiers, compiler downloads and physical power loss remain separate.

Detailed raw identities, logs and both failed and passing probes are retained
under `build/project_review_2026_10_02/dependency-pin-upstream/2026-10-03/`.
The original action commits and July review dates remain current inventory
values. None of these partial observations renews the October 8 deadline or
closes A08/B01. Adoption and rollback require the coordinated checks below.

### Subsequent complete infrastructure replay and compiler-readiness repair

All 180 infrastructure controls now pass without skips on native ARM64 and
emulated x86-64 Linux, including archive/product integration and the synthetic
admission mechanisms. The copies include exactly 8,249 declared source files;
Node 22.23.3 archives were verified against the publisher checksum list. The
Python base image retains the digest above; owned images add Git 2.39.5 and
CA certificates through apt. Their observed image identities bind these runs,
but mutable apt inputs do not constitute an independently reproducible builder.
Linux mutation fixtures use owned tmpfs. The first full attempt had four fixture
permission errors because its tmpfs was root-owned. The corrected ownership
passes. A later x86-64 readiness-file race now uses atomic fixture publication;
its original failure is retained. A concurrent timeout is also retained, and
serial replay passes at the unchanged 300-second budget. These observations
qualify the named mechanisms, not full scientific/hosted tiers or power loss.

A fresh tool home exposed a real setup error: successful Elan initialization
selected the default, but left Lean undownloaded. The first version check began
the download and exceeded its 30-second budget. The helper now explicitly runs
`elan toolchain install` and then checks Lean and Lake with `elan run` selecting
the exact pin without `--install`. Failed provisioning or a mismatching compiler
cannot report successful setup. Two rejecting controls and an actual fresh
ARM64 Linux setup pass. The downloaded compiler reports Lean 4.31.0, commit
`68218e876d2a38b1985b8590fff244a83c321783`; setup takes 154.156 seconds and the
subsequent version checks complete in under one second each. Its cold library
build times out at the declared 1,200-second budget after 102 of 133 jobs; that
failure remains retained. The Elan archives have independently calculated
inventory digests; this probe does not independently calculate the compiler
archive digest downloaded by Elan. The compiler release asset and installation
remain explicit transitive trust dependencies. No action pin or formal July
review date changes, and the October 8 deadline remains in force.

Raw logs, immutable earlier source copies and fresh replay manifests are under
`build/project_review_2026_10_02/linux-infrastructure/2026-10-03/`. Original
HTML/bundle receipts retain their preceding inputs; this phase does not renew them.

The separate network-disabled ARM64 continuation now completes the remaining
library jobs and observes identical records for all 3,153 source theorems.
Its first check rejects a stale executor input digest; semantic review confirms
that sole difference, and the refreshed identity passes a second compiled query
and the registered LivingBook change-packet consumer. It reuses
the partial build from the retained cold timeout, not a clean single-pass build.
The axiom check is the existing producer re-query, not independent model
adequacy or compiler-correctness evidence. Full runtime/tier qualification and
the formal pin-review renewal remain pending.

### October 10 refresh and new candidate checks

The UTC pin gate now rejects all nine July 10 reviews as expired. Official
latest releases, full resolved commits, pin comparisons and public repository
advisories were fetched again on October 10. No canonical pin, `reviewed_on` or
`review_due_on` changed. This is substantive review in progress; the required
project-tier qualification and coordinated update remain unfinished.

| Component | Current October 10 candidate | Current disposition |
|---|---|---|
| checkout | `v7.0.1`, `3d3c42e5aac5ba805825da76410c181273ba90b1` | Unchanged from the preceding inspection; retain the 128-assertion observation at this exact identity and the declared compatibility limits. |
| setup-python | `v7.0.0`, `5fda3b95a4ea91299a34e894583c3862153e4b97` | Unchanged; retain the 210-assertion and selected Linux cached-interpreter observations. |
| setup-node | [v7.1.0](https://github.com/actions/setup-node/releases/tag/v7.1.0), `949feb2413d6458794dcd2491c4babbbce0c15c1` | New candidate, 34 commits ahead of the pin. Source review covers version validation/manifest retries, mise.toml and absolute version-file support, cache updates and the brace-expansion change. All 235 current upstream assertions pass. The earlier 225 assertions and Linux packaged-action probes belong to v7.0.0 and do not qualify this candidate. |
| Quarto setup | `v2.2.0`, `8a96df13519ee81fd526f2dfca5962811136661b` | Same pinned commit; downloaded Quarto package identity and privileged installation remain explicit residuals. |
| Pages upload | `v5.0.0`, `fc324d3547104276b827a68afc52ff2a11cc49c9` | Same pinned commit; hosted artifact service qualification remains separate. |
| Pages deploy | `v5.0.1`, `368f82528645a54fb793d4d04e342629a3f51346` | Unchanged candidate; retain the 32 authored assertions, which mock deployment rather than publish a site. |
| Artifact upload | [v7.0.2](https://github.com/actions/upload-artifact/releases/tag/v7.0.2), `cf430e030ddbb5b0abf93d22962f4752f3646cd9` | New candidate, four commits ahead; artifact SDK 6.3.1 update. All 31 authored action assertions pass. |
| Artifact download | [v8.0.2](https://github.com/actions/download-artifact/releases/tag/v8.0.2), `9000827ccba6bdab643e8b6fd33ac0654aef8333` | New candidate, five commits ahead; artifact SDK 6.3.1 adds 429/retry handling. All 21 authored action assertions pass; mocked clients do not execute the SDK's real network retries. |
| Elan | `v4.2.4`, `227caca133724d5516bee25c2aeb3e609478f2d8` | Version unchanged; preserve the four archive digest checks and preceding Linux/Lean observations. The actual archive helper runs those pinned binaries, not the retained moving-download shell snapshot. |

The three new candidate checkouts are exact detached commits. Node 24.21.0 for
macOS ARM64 was extracted into a separate owned temporary directory only after
its archive matched the publisher checksum list. Each candidate installed its
lockfile with `npm ci --ignore-scripts`; user/global npm configuration was
replaced for those processes with owned empty files and account/action tokens
were absent from their environment. All 287 selected assertions pass without
skips or TODO cases; tracked source hashes are identical before and after.
Tests run serially with a 15-second per-case and 600-second process budget.
Node net/tls/http/https/fetch entry points are intercepted and a self-check
confirms refusal. This is not an OS network sandbox or a hosted Linux runner;
published bundles, real service authentication, third-party transports and
transitive runtime behavior remain separate boundaries.

All twenty configured remote-action occurrences across workflows and the shared
composite have declared inputs in the exact current candidates' official
metadata. Required inputs without defaults are also present. This is static
input compatibility; it does not qualify defaults, packaged execution or hosted
installation. The current local deep-tier preflight separately refuses because
this narrow publication/schema test interpreter lacks BeautifulSoup. Many
execution contracts still remain unreviewed, so preflight's declared capability
list is not a complete scientific-runtime qualification.

The pinned setup-node source lockfile declares production `brace-expansion`
1.1.13; the new candidate declares 5.0.12. The primary
[GHSA-3jxr-9vmj-r5cp advisory](https://github.com/advisories/GHSA-3jxr-9vmj-r5cp)
lists the older version in its affected range for exponential expansion of
untrusted brace patterns and the new version outside that range. This is a
dependency-review signal, not demonstrated exploitation of this project.
The pinned source calls glob hashing when caching is enabled explicitly or
detected from the workspace-root package metadata. The current two setup-node
occurrences specify only Node 22, no cache/pattern inputs, and the project root
has no `package.json`. That narrows the inspected configured route; it does not
prove every bundled dependency unreachable or justify retaining an expired
review. A packaged-code string scan is inadequate evidence of a fix.

The artifact candidates still declare other production `brace-expansion`
instances in that advisory's affected ranges: upload has nested 1.1.12, root
5.0.3 and readdir-glob's 2.0.2; download has 2.0.2. Development-only instances
and the separately named `@isaacs/brace-expansion` package are not conflated with
those counts. Upload's declared `@actions/glob` to minimatch edge uses the nested
1.x instance; its source passes upload search patterns to that glob helper.
The current workflow upload paths are literal diagnostic/bundle paths, and
download selects a named tested bundle without a pattern input. This records
the inspected configuration, not an assertion that vulnerable code is absent
from published bundles or unreachable across all action modes. The SDK update
and 287 passing action assertions do not resolve this transitive review finding.

The download action's one public repository advisory is the historical
[path-traversal range](https://github.com/advisories/GHSA-cxww-7g56-2vh6)
`>=4.0.0 <4.1.3`; the current v8 candidate lies outside its
declared range. Empty advisory listings for other repositories are not proof of
safety or complete transitive-dependency coverage. Raw responses, source/lockfile
identities, guard source, assertion reports and logs are retained under
`build/project_review_2026_10_02/dependency-pin-upstream/2026-10-10/`.
Current candidate qualification must resolve the transitive advisory finding
as well as project compatibility. Adoption, formal review renewal and rollback
still require the procedure below.

### Coordinated pin update

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
