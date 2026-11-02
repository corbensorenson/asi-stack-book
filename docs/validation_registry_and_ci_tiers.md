# Validation Registry and CI Tiers

Last updated: 2026-10-10

`validation/registry.json` is the sole declarative inventory and execution plan
for repository validation. It currently contains 477 ordered units and 3,313
required artifacts.
Every unit names an execution tier, validation class, input/output contract,
claim scope, negative-control status, and prohibited inference. The shared
execution defaults and reviewed per-unit overrides also control prerequisite
checks, side effects, dependency order, custody mode and wall-time budgets.
Unreviewed side effects are explicit; they are not silently treated as read-only.

## Completed migration boundary

The registry owns required artifacts, unit commands, order, tiers, classes, and
contracts. `validate_book.py` is only the structural base gate: it loads its
required-file list from the registry and contains no child-validator command
inventory. `scripts/run_validation_registry.py` runs that base and then the
selected registry units in order. `scripts/build_validation_registry.py`
normalizes/checks the authoritative JSON; it no longer discovers commands by
parsing Python. `scripts/validate_validation_registry.py` rejects any return of
the legacy list, dispatcher, child-suppression environment, or dual authority.

## Tiers

- `pr` runs the base structural gate plus 139 fast publication, status,
  product, contribution, outline, proof-manifest, schema, and registry checks.
- `deep` includes PR checks and 310 deeper fixture, proof/evidence,
  reader-preparation, replay, and artifact checks. Pages build uses this tier.
- `release` adds 28 format/application/release-candidate checks and is manual;
  it does not approve artifacts merely because the tier exists.

The workflows are separated accordingly:

- `.github/workflows/validate-pr.yml` handles pull requests;
- `.github/workflows/deep-validation.yml` handles scheduled/manual deep checks;
- `.github/workflows/major-release-validation.yml` handles manual major-edition
  preparation; and
- `.github/workflows/build-pages-artifact.yml` validates, builds, renders, and
  uploads the tested bundle; `.github/workflows/publish.yml` consumes that
  successful-run artifact without rebuilding and then attests the public site.

## Class semantics

The five classes are publication gates, schema/structure checks, behavioral
fixtures, reader-artifact gates, and proof/evidence gates. Class contracts make
the default epistemic limit explicit. A behavioral fixture, for example, is
scoped to the named fixture or local replay and cannot imply deployment,
transfer, broad correctness, safety, or chapter-core promotion.

Class metadata does not prove every validator is semantically adequate. The
registry records `validator_owned` where a script declares expected-invalid,
mutation, or negative controls and `not_declared` otherwise. Future review must
upgrade generic inherited contracts to exact per-unit artifact inputs and
outputs where that precision changes a claim or release decision.

The first high-impact audit is recorded in
`validation/unit_contract_overrides.json`. It replaces inherited descriptions
for status/deployment integrity, supply-chain pins, release channels and
deterministic immutable-site archive preparation,
evidence-quality and reviewer records, decision/review packets, product and
contribution focus, executable product projections, licensing provenance, the governed vertical slice and trace invariants, proof
manifest synchronization, schemas, publication, and registry integrity with
exact input artifacts, output assertions, negative controls, scope, and
prohibited inference. These remain internal contract audits, not independent
semantic review.

## Commands

```bash
python3 scripts/build_validation_registry.py --check
python3 scripts/validate_validation_registry.py
python3 scripts/run_validation_registry.py --tier pr
python3 scripts/run_validation_registry.py --tier deep
python3 scripts/run_validation_registry.py --tier release
```

No tier proves ASI, model quality, safety, security, or chapter claims. No tier
promotes support state without an accepted evidence transition, and release
tier availability does not approve an edition artifact.

## Diagnostic execution and contributor entry points

The normal tier remains fail-fast. The runner saves a JSON result and a raw
log for every started unit, plus explicit `not_run` records for the remainder.
`--diagnostic` continues only reviewed read-only independent units. A failed
parent prevents its consumers from running; missing prerequisites, unreviewed
side effects and unresolved selections remain failures, never passes or
implicit skips. The initial execution-contract review covered nineteen named
units. Archive self-test execution became a twentieth reviewed contract: it
needs Python, Unix process groups and jsonschema, uses a 120-second budget,
has no network requirement, and creates only owned temporary diagnostics.
It is an ignored-output operation rather than a read-only diagnostic. Dynamic
status-envelope inputs remain a separate input-coverage limitation. The other
defaults remain unreviewed. The Living Book Lean compilation
is classified as an ignored-output operation and is excluded from read-only
diagnostics. This is a migration boundary, not a claim that all 477 capability
and effect contracts have been audited.

The October 10 continuation reviews eight more exact empty-argument variants,
bringing the current execution-contract count from 21 to 29. All use a
120-second process budget, Python/Unix process groups, no network and no source
or report writes. Their normal registered arguments are the boundary; in
particular, the proof-depth classifier's optional `--write` command is not
covered by this read-only review.

| Registered validator | Additional runtime | Custody mode and inspected behavior |
|---|---|---|
| Validator coverage | None | Current workflow/registry/allowlist and filename inventory; harness command strings are not executed. |
| Proof depth | None | Current Lean source text and existing report comparison; no compiler or proof execution. |
| Architecture red team | None | Current report structure and limitation phrases; no exploit or external review execution. |
| Release profiles | None | Current profile JSON and referenced-path existence; tool commands remain metadata strings. |
| Trust surface | None | Mixed current public surfaces and terminal disposition/transition records; no replay or publication. |
| Substrate neutrality | None | Current text/figure reads and one in-memory rejecting mutation; no source changes. |
| Evidence quality vectors | jsonschema | Mixed current policy/dispositions and terminal decision records; pure expected-value comparison and four in-memory mutations. Builder write paths and public-status Git/producer paths are not called. |
| Reviewer capacity | jsonschema | Current registry/schema and four in-memory mutations; no reviewer assignment, contact or measurement. |

The runner's selected deep-tier diagnostic actually starts and passes all eight
plus the base gate. Plan/preflight use the declared capabilities, and a Python
invocation without site-package loading rejects the missing jsonschema capability
before running the reviewer validator. The first harness mistakenly selected
the two deep-only units in PR; its correct out-of-tier refusal is retained and
excluded from the later passing selection. No unit was moved between tiers.

Execution review does not certify complete semantic input coverage. Five units
also receive explicit source/data/path scopes. Directory member inventories and
profile-referenced existence checks remain domain inputs; the runner does not
claim a byte-complete directory identity. The three existing exact input
contracts remain with their override owner. After the publication-process continuation, there are 447 unreviewed
execution defaults, so this migration and full tier/runtime qualification remain
open. The July action/installer reviews remain expired; selected diagnostics
cannot renew them or imply full CI/release readiness.

The later October 10 publication-source review brings the current total to
30 reviewed execution contracts. Its ordinary empty-argument command needs
Python, Unix process groups and Git, has a 360-second outer budget, and creates
only ignored diagnostics. The source gate now supervises Git at 30 seconds and
each paper/trust child at 120 seconds through the shared executor. Each invocation
owns a fresh `build/publication-source-*/` directory and retains stdout and stderr
separately under one combined retention cap: 4 MiB for Git and 1 MiB per child.
Excess output is drained. Complete NUL-delimited Git output is required; malformed
or truncated output fails even when Git exits zero. The default merged-log API
for other callers remains unchanged.

Before execution, the result records the child as running. An owner-lifetime
pipe ties the capture wrapper to the publication process; the existing independent
guardian stops the payload group and keeps its source lease until that group is
absent. Parent-only SIGTERM/SIGKILL and deadline controls pass on macOS, with
readiness, lease release and delayed-effect checks. Processes that escape their
owned group, simultaneous loss of wrapper and guardian, and physical power loss
remain outside this guarantee. CI uploads the fresh publication diagnostics with
its other retained reports. This repairs one audited pipeline; migration of other
subprocess callers and qualification of full tiers remain open.

The next continuation extracts that owner-lifetime mechanism into the existing
shared runtime and reuses it for publication, the compiled axiom builder,
ProofEnvelope and LivingBook. The source-root lease and command cwd are separate:
Lean executes from `lean/`, while its independent guardian retains the repository
lease. A linked, missing or outside cwd (including parent walking) refuses before
spawn. The payload does not inherit owner/control/lease descriptors. The original
bare `execute` API still provides bounded capture; caller death supervision is
provided by `execute_guarded`, not retroactively guaranteed for every caller.

The proof builder retains stage-specific machine outcomes and raw logs under
fresh `build/proof_axiom_audit/run-*/` directories. Library build, compiler-version
probe and elaborated query budgets are 1,800, 30 and 300 seconds. Wrong/truncated
compiler identity and malformed/truncated/unstable environment data are explicit
failed protocol outcomes even after a zero process exit. Exact ProofEnvelope and
LivingBook compilation each get 300 seconds and fresh ignored diagnostic directories.
The whole registered units get 2,700 and 360 seconds respectively, allowing their
other stages; these are declared ceilings, not measured cold-build guarantees.
The proof audit uses only stdlib Python, and the corrected capability preflight
passes without site packages. LivingBook still needs jsonschema. All four CI
validation workflows retain these compiler diagnostics. Domain/model adequacy,
full cold builds, hosted tiers and dependency review renewal remain separate.

A current declared-source AST inventory scans 950 Python scripts: 191 have
263 direct subprocess call sites, only 39 with explicit timeout keywords. This is
a syntactic review signal, not evidence that every other call needs a timeout or
that a keyword establishes adequate output, lifetime or environment control.
Dynamic wrappers and effects remain owner review work. In particular, an uncertain
guardian must retain its source lease until payload absence; a cleanup deadline
must not release custody while that payload remains. The 30/447 reviewed/default
execution counts and 20/114 scoped recommendation verification remain unchanged.

```bash
# Inspect the environment and possible operations without running checks.
python3 scripts/run_validation_registry.py --tier pr --plan
python3 scripts/run_validation_registry.py --tier pr --preflight
# Run selected reviewed checks and retain all independent outcomes.
python3 scripts/run_validation_registry.py --tier pr --diagnostic \
  --select validate_schemas.py --select validate_protocol_examples.py
# Preserve the existing complete fail-fast admission gate.
python3 scripts/run_validation_registry.py --tier deep
```

An exact script selection resolves every registered argument variant of that
script inside the requested tier; use a registry unit ID to select one variant.
A selection outside the tier is an error. Reports must be under ignored
`build/`. Their counts separate selected, started, passed, failed, skipped,
timed-out, cancelled and not-run checks. Each unit has a stable ID, diagnostic
category, duration, command, exact declared file-input hashes and raw log.
Domain conclusions and rejected-case counts stay with the domain validator;
the runner does not infer them from one printed phrase. Directory-content
identity remains the domain owner's responsibility.

Execution supports Linux and macOS process groups. Every subprocess runs with
the runner's Python interpreter directory first on PATH. The default 1,800
second budget is an explicit provisional ceiling, not a measured runtime;
reviewed small checks have 120 seconds, LivingBook has 360 seconds and the complete proof-artifact audit has 2,700 seconds.
`--timeout` is a visible per-run override. Timeout or interruption terminates
the entire child process group, including descendants after a leader exits.
Retained logs are capped at 10 MiB while excess output is drained; the report
marks truncation. A cancelled run exits 130, and any required non-pass exits 1.
CI retains these reports, browser outcomes and failure images on success or
failure for fourteen days.

For a prose edit, select its admission checks, refresh only current owners,
then render the changed HTML. For a source edit, follow the source-intake
sequence in `living_update_workflow.md` before selecting source/evidence gates.
For a proof edit, build Lean and run the exact formal consumer. For chapter
admission, use the complete birth and dependency transaction; a passing
schema check alone is insufficient. Historical commands must name retained
commit/byte custody; they do not refresh current outputs automatically.

## Runtime profiles and observed limits

The isolated record/publication profile is Python 3.11 with
`python3.11 -m venv build/record-runtime` followed by
`build/record-runtime/bin/python -m pip install -r ci/publication_requirements.txt`.
Its direct and transitive dependencies are pinned. On October 2, this fresh
macOS profile passed all 135 infrastructure/runner tests, 306 schemas and 96
protocol fixtures plus 17 release records. That is a selected clean-environment
replay, not fresh Ubuntu CI execution.

The full validation profile uses the composite action's Python 3.11, Node 22,
CPU PyTorch 2.7.1, `ci/post_v2_requirements.txt`, Quarto 1.9.38, the exact Lean
toolchain and complete Git history. Elan is installed by the versioned archive
helper with the inventory's exact per-platform digests and a real-UTC review
expiry check. The helper explicitly installs the pinned toolchain, then checks
Lean and Lake under that exact selection without a hidden version-check
download. Elan initialization alone only selects a default and does not
establish compiler readiness. Its old shell source is retained context; no
moving Elan binary is fetched. Publication also uses Node 22 and
`npm ci --ignore-scripts --prefix ci/browser`, then the locked Playwright
Chromium/system-dependency installation. Full scientific transitive locking,
per-unit capability review and fresh Linux tier replay remain open. Linux MLX
stubs only permit preflight import checks; native MLX model execution requires
its supported platform and its experiment-specific environment.

On October 3, all 180 infrastructure tests pass on macOS and in network-disabled
Linux containers: native ARM64 and emulated x86-64, Python 3.11.17, Node 22.23.3
and Git 2.39.5. The source copies contain 8,249 tracked or explicitly registered
files, including the improvement catalog consumed by the roadmap validator.
Unknown personal/attempt/cache directories are excluded without recursive
admission. The copies retain dirty local source identity and complete historical
Git objects; they are not clean release checkouts. Linux transaction targets use
owned tmpfs. This includes archive/product integration and all twenty admission
transaction/lease controls, whose accepted birth cases remain synthetic. An
atomic fixture-readiness repair preserves the original wrapper/descendant
termination assertions. The concurrent x86-64 timeout is retained separately
from its passing serial replay at the same 300-second budget. This qualifies
these mechanisms, not scientific dependencies, hosted Ubuntu, full registry
tiers or hardware durability. The fresh ARM64 Linux compiler setup passes;
its 1,200-second cold library build timed out after 102 of 133 jobs and remains
a failed observation rather than a completed qualification.

The October 10 continuation passes the complete current 219-test infrastructure
suite without skips on macOS, native ARM64 Linux and emulated x86-64 Linux.
All 39 controls added after the earlier 180-test replay now have both Linux
observations. The exact same retained image IDs, Python 3.11.17, Node 22.23.3 and
Git 2.39.5 are used. Each architecture installs the current nine-package profile
offline from exact wheel bytes; the two added package artifacts match official
exact-version metadata hashes. The source snapshot includes 8,254 declared files,
with independent file objects and matching before/after hashes. Linux executions
remain network-disabled, read-only source and owned tmpfs, serial at 300 seconds.

The first 218-test x86-64 replay fails one descriptor assumption: a focused probe
finds Python/Rosetta executable handles. The identity-based private-handle oracle
preserves those observations and detects an actual leaked source lease/control
pipe in a confined broken producer. The following 219-test matrix passes without
production guard changes or relaxed budgets. Docker returns to its observed
stopped state with images, volumes and receipts preserved. This closes the newer
infrastructure replay gap, not full registry/scientific/hosted tiers, real cold
Lean compilation, browser/publication renewal or physical durability. The nine
expired dependency reviews and 447 unreviewed contracts remain unresolved.

The separate network-disabled ARM64 continuation now completes the remaining
library jobs and observes identical records for all 3,153 source theorems.
Its first check rejects a stale executor input digest; semantic review confirms
that sole difference, and the refreshed identity passes a second compiled query
and the registered LivingBook change-packet consumer. It reuses
the partial build from the retained cold timeout, not a clean single-pass build.
The axiom check is the existing producer re-query, not independent model
adequacy or compiler-correctness evidence. Full runtime/tier qualification and
the formal pin-review renewal remain pending.

## Current dependency planning and loaded registry custody

The registry also owns 19 current projection nodes, including the complete
public product payload. `python3 scripts/book.py
plan --changed <path>` follows their explicit edges and lists output paths,
manual review boundaries, rebuild commands and registered consumers. Current
plans show the selecting owner/input, merged execution contract, output effects
and wall-time ceiling for every selected check. Unknown contract review is
explicit; these budgets are not runtime estimates. Current
Human Reader evidence routes reuse its existing crosswalk. Unknown input
coverage is reported explicitly (196 units on October 2); an empty targeted
selection cannot silently execute a full tier or claim a pass. Historical
terminal records are not current rebuild owners. This is a reviewed initial
graph, not complete dependency coverage or automatic review approval.

The runner hashes the exact registry bytes it parses. Registry replacement or
deletion during a run blocks remaining units and final acceptance, including
when the last executed unit exits successfully. Reports retain loaded and
final identities and a `registry_drift` diagnostic. Per-unit input hashes are
still observations of declared file inputs, not a coherent snapshot of every
repository dependency.

The scaffold and paper-library read-only checks are registered PR gates; the
Pages scaffold step now uses `--check` directly. Shared text projection writes
leave identical bytes untouched and stage changed individual files. Whole
valid chapter birth and other multi-file generator staging remain open.

`book.py html --site <ignored-site-directory> --plan` previews the eight reviewed
post-render interfaces from `.github/workflows/build-pages-artifact.yml`, now
including installed-reader integrity and browser-report acceptance. The
report consumer uses the immediately preceding producer's unique diagnostic
path, requires complete/current coverage and rejects inconsistent outcomes.
Omit `--plan` to execute them with bounded logs and aggregate fail-fast outcomes.
Clean tested-commit status is required by default; `--local` permits diagnostic
dirty-worktree status without certifying a deployable artifact. Interface drift,
missing capabilities, linked site inputs and byte changes during checking reject.
The refreshed local site passed all eight interfaces, 234 strict browser
page-view pairs and six control cases on October 2, with unchanged site bytes
and declared inputs. A preceding run rejected an adapter change despite all
eight individual gates passing. The command does not render, install tools,
upload artifacts or replace the source CI tier.

`add_chapter.py` prepares non-admitted intent; `prepare_chapter_admission.py`
copies an authored complete candidate into isolation and runs registered birth
checks. Its failed-copy and rejecting-report receipts remain ignored diagnostics.
Explicit `--install` runs the full deep tier against that isolated workspace,
then uses a manifest-last recoverable transaction. Pending admission blocks
cooperating consumers; CI wraps all three Quarto renders in the shared source
lease. `recover_chapter_admission.py --rollback` restores retained objects
after preflighting all targets and preserves later edits by refusing unsafe
recovery. Inventory-only registry additions cannot change checking contracts.
Sixteen authored transaction/lease controls pass locally; an actual incomplete
candidate rejects without a canonical change. A real valid birth remains open
under D02; synthetic runner observations are not semantic admission.

Process-group cleanup refusal now remains a failed unit with retained log and
explicit `cleanup_failed` diagnostics, even after a zero-exit leader. Further
units stop in diagnostic mode too. A Darwin-only bounded zero-signal probe may
confirm disappearance after an exited-leader permission error; persistent
errors and live/non-Darwin leaders do not receive that fallback. Apple's
[group-signalling implementation](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/kern/kern_sig.c)
filters zombies and can return permission failure with no signalable member;
this is a possible explanation for the retained local failures, not proof of
their cause. Authored controls cover both disappearance and refusal. The
dynamic-spine validator now copies only indexed and explicitly registered
ordinary source, preserving unknown personal/attempt/cache trees outside its
workspace instead of recursively copying the working directory.

Schema-definition validity now uses a bounded content-keyed cache: at most
128 plain-JSON definitions with keys of at most 64 KiB. Schema mutation
changes the key; cached diagnostics receive the current owner's path.
Non-JSON Python shapes and larger definitions retain uncached standards
checking. Every instance is validated again, and offline reference resolution
and domain judgments remain with their existing consumers. A 50-call local
profile of the same browser AI-layout record changed from 9.365 to 0.503
seconds; these observations are not a universal speedup guarantee.
