# Tests

Book validation, source matrix checks, and experiment tests go here.

Current tracked fixtures:

- `fixtures/protocol_records/` contains public-safe valid examples for executable protocol schemas.

Run:

```bash
python3 scripts/validate_protocol_examples.py
```

`test_validation_infrastructure.py` protects full schema constraint rejection
and site-bundle custody, including outside-root symlinks, ancestry overlap,
source changes during copying and preservation of the last bundle on staging
failure. Every CI tier runs these tests through the shared validation runtime.
Run them locally in the pinned Python environment with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

These authored mechanism tests do not measure natural task utility or promote
architecture claims. Schema `format` fields remain annotations under the
default Draft 2020-12 vocabulary; semantic consumers own any required temporal
or identifier interpretation. Unknown schema references fail without network
retrieval.

`test_release_channel_transaction.py` exercises complete release-channel
installation, read-only checks, copy/source/exchange failures, competing
writers and process exits immediately before and after atomic exchange.
These controls now pass on macOS, native ARM64 Linux and emulated x86-64
Linux. The Linux mutation targets use owned tmpfs; physical power-loss behavior
and other filesystems require their own observations.

`test_projection_preview.py` checks non-writing previews, unchanged timestamps,
replacement failures and symlink refusal. `test_projection_plan.py` checks
transitive invalidation, named consumer/prerequisite selection, review
boundaries, historical-owner exclusion and reuse of current reader bindings.
`test_contributor_commands.py` prevents empty or out-of-tier targeted selections
from becoming an accidental full run. The runner tests also reject registry
replacement or deletion during execution while retaining the loaded identity.
Cleanup failures retain logs, reject zero-exit leaders and halt later units in
both gate and diagnostic modes. The Darwin exited-group fallback accepts only
observed group disappearance within its bounded probe; persistent, live-leader
and non-Darwin permission failures remain failures.
The complete infrastructure suite has 219 authored tests. The October 10 replay
passes all 219 without skips on macOS, native ARM64 Linux and emulated x86-64
Linux, with the exact nine-package publication/schema profile. Earlier 180-,
197-, 207- and 218-test observations remain retained with their original scope.
The new replay closes the Linux gap for all 39 controls added since the earlier
180-test suite. It does not qualify full scientific/hosted tiers, every Linux
filesystem or physical power-loss behavior.

`test_publication_processes.py` exercises separate binary stdout/stderr,
a combined output budget, refusal before spawn when a log cannot be opened,
interpreter identity, retained repeated-command logs, real Git filenames with
spaces/newlines, and malformed/truncated NUL protocol rejection. Deadline and
parent-only SIGTERM/SIGKILL controls require readiness, observe source-lease
release, and reject delayed child effects. A linked output parent is refused
without changing foreign content. The original parent-death gap and inadequate
first wrapper/budget controls remain retained. The preceding 207-test macOS run
passes; these authored controls do not qualify escaped process groups or physical
power loss.

The later shared-guard controls separate the command cwd from its source lease:
Lean runs from `lean/` while the repository lease remains held. They verify the
interpreter/prefix, private-descriptor exclusion, refusal of outside, parent-walking,
linked or missing directories, parent-only SIGTERM/SIGKILL and ready-descendant
timeout, and owner-pipe closure after log-setup failure. Compiler refusals retain
classified logs/results; zero-exit wrong compiler identity and malformed axiom
JSON become explicit failed protocol outcomes. The original misbound fixture and
an overly loose refusal assertion remain recorded as instrument inadequacy,
excluded from final acceptance. The corrected 21-test process module and complete
218-test suite remain historical macOS observations; the following descriptor
control brings the current suite to 219 across all three replay environments.

The first emulated 218-test replay failed the assumption that a payload has no
extra descriptors. A focused probe identifies two Python executable handles and
a Rosetta runtime handle; none is a private directory lease or FIFO control.
The revised oracle matches live private object identities rather than unrelated
emulator handles. A confined broken helper actually passes the source lease and
control pipe to its payload, and the oracle detects both. The full 219-test serial
Linux replays pass at the same 300-second outer budget and unchanged production
budgets. Read-only declared-source copies, nine offline-installed pinned packages,
no networking, owned tmpfs and before/after source hashes bound these observations.
The failed run, diagnostic probe, selector refusal and original 218-test native
pass remain retained; no runtime failure was hidden by changing production code.

The C04 archive-inventory regression reproduces a producer omission that its
formerly shared consumer accepted. The consumer now derives completeness/content
from captured bundle bytes itself. Missing site/manifest members and rewritten
content reject even when archive metadata/checksums are internally consistent;
the builder's preparation gate preserves the prior candidate. The archive owner
documents shared capture, policy, path, serializer and custody dependencies.

The four pin-review boundary controls reproduce UTC expiry versus the local
calendar, deterministic/invalid audit-date overrides, malformed inventory
shapes and CLI refusal before downstream consumption. On October 3, the fourteen
shared generated-directory controls, seventeen reader controls and these four
pin controls also passed on network-disabled Linux containers with read-only
declared source copies. ARM64 ran natively; x86-64 was emulated. These 35-test
observations were followed by the complete 180-test replay, including product,
archive and admission mechanisms. It uses independently copied declared source
files, Python 3.11.17, Node 22.23.3 and Git 2.39.5. A readiness-file race was
observed on x86-64 and repaired by publishing complete fixture JSON through
rename. A concurrent replay timed out; the serial x86-64 replay passes at the
same 300-second budget. Original failures remain retained. Hosted tiers, a real
valid chapter birth and physical power loss remain separate obligations.

`test_lean_runtime.py` rejects archive digest mismatch, traversal, links, extra
payloads, moving release URLs, duplicate platforms and expired/future reviews
before installer execution. Two further controls reject a failed explicit
toolchain download and a mismatching compiler after initialization. Selecting
a default in Elan is insufficient: the helper now installs the exact toolchain
and verifies Lean and Lake before reporting success. A fresh ARM64 Linux tool
home downloaded Lean 4.31.0 and passed those checks; its subsequent cold library
build timed out after 102 of 133 jobs. Exact Elan archive verification, observed
compiler versions and complete proof-library qualification have distinct scopes.

`test_chapter_proposals.py` prevents incomplete intent from changing the
canonical manifest, following owner/output links or replacing unknown content.
`test_chapter_admission_staging.py` checks isolated copying, declared-file
selection, source/patch identity, interruption receipts, existing-stage
preservation, acceptance-code protection and complete runner-report custody.
Candidate patches cannot replace tests or source/evidence/release/authority
custody, or retained reader snapshots; current reader-route data may be staged
without being admitted.
The improvement catalog is a registered artifact and an input of its roadmap
consumer; a real-source control confirms it survives declared staging.
The dynamic-spine copy uses the same declared-source boundary, excludes unknown
personal/attempt/cache trees and rejects observed source drift.
The accepted-report cases are synthetic receipt-mechanism tests; they do not
claim that a real new chapter passed the book's semantic admission checks.
`test_canonical_admission_transaction.py` contains twenty authored controls for
manifest-last installation, original-object retention, abrupt process exit,
pending-reader rejection, rollback, later-edit preservation, inventory-only
registration and source leases. Its successful full-runner observations are
synthetic. Their Linux mechanism replay is observed; a real valid birth through
the actual consumers and physical power-loss behavior remain separate
unobserved obligations.
The command controls also kill the wrapper, close command descriptors, ignore
SIGTERM and leave a descendant after normal leader exit. An independent
supervisor must stop the owned group before a source writer can acquire its
lease; preserved exit codes and launch rejection have separate controls.

Contributor tests also preserve the canonical HTML workflow interfaces, reject
missing/duplicate/weakened checks, retain failure diagnostics, stop after a
required failure, and reject linked or changing site inputs. Dependency-plan
tests expose platform/tool requirements and output effects without treating
unreviewed contracts as complete capability declarations.

`test_reader_site_transaction.py` protects complete reader replacement,
non-writing checks and unchanged timestamps, exact legacy adoption, source and
crosswalk drift, prior-content preservation, broken/escaping links, symlink
refusal, concurrent writers and process exits around atomic exchange. A
post-exchange directory-fsync failure retains the prior tree and an explicit
durability-uncertain receipt. These controls pass on macOS and the two named
Linux architectures; they do not certify arbitrary filesystems, hardware power
loss or publication.

`test_browser_report_consumer.py` has eight authored controls for report
acceptance: complete current coverage, non-writing consumption, missing or
skipped outcomes, duplicate/missing routes and viewports, contradictory DOM
measurements, invalid numeric types, changed site/source bytes, changing inputs
and unsafe report destinations. Its miniature reports are fixtures, not real
browser observations or human accessibility review. The separate actual site
replay retains its own ignored report and screenshots.
The complete infrastructure suite requires a Node CLI (Node 22 is the CI
profile) for early browser-command refusal controls. Those controls run before
loading Playwright; they do not require a browser installation. The shared CI
runtime installs Node explicitly for all validation tiers.

`test_product_site_transaction.py` contains eighteen custody and integration
controls: complete replacement and no-ops, pure checks, exact legacy adoption,
unknown prior content and damaged receipts, numeric type coercion, unsafe paths,
competing writers, concurrent edits, source drift, failed preparation/exchange,
process exits, retained prior custody after uncertain fsync, stale status and
volatile timestamps. Its authored mechanisms and diagnostic product fixtures
do not become natural experimental tasks or evidence for chapter claims.

Reader, product, channel and bundle controls preserve unexpected empty
directories and the displaced prior tree after exceptions following a real
exchange. Fresh reader/product/bundle destinations reject an intervening empty
directory through the actual macOS exclusive-rename operation. Bundle/channel
fsync failures retain journals and prior bytes. These are authored local
counterexamples and controls on macOS and the named Linux tmpfs profiles; they
do not provide hardware qualification.

`test_immutable_archive_transaction.py` contains seventeen disposable candidate
controls for unknown content, stale source manifests, overlaps, source drift,
read-only checks/consumption, legacy adoption, immutable identity, malformed
paths/metadata, policy refusal, and prior-object retention after exchange,
fsync or destination collision. A final-operation control also rejects and
preserves candidate, source or policy edits made after the positive check. The archive parser has direct duplicate,
empty-directory and expansion-budget controls. Reader/product no-op controls
also reject an edit introduced after ownership inspection. Synthetic clean
version tags do not create a real tested release or authorize publication.

The schema-reuse control changes an instance, a schema bound, a malformed
definition and its owner path without restarting the process. It also retains
Python tuple and integer-key semantics instead of coercing them through JSON.
The timeout control requires readiness from both parent and descendant before
checking the delayed effect window; a pre-start timeout cannot stand in for
descendant termination.

`test_chapter_freshness.py` contains eight controls for UTC scaffold creation, preservation during
ordinary syncs/explicit rewrites, distinct revision/review
events, canonical calendar/UTC dates, duplicate keys, bounded review scope,
contradictory/duplicate/legacy rendered rows and hidden/outside-status values.
The independent checker derives expectations from canonical chapter front
matter. Separate actual Quarto controls change the revision while preserving
the review, project conflicting/missing legacy rows, refuse invalid/unscoped
metadata and reject an altered rendered date. These tests establish declaration
and display consistency, not historical event truth or source/support freshness.

`test_generated_directory_stateful.py` adds one generated state-machine test and
seven fixed sequence/oracle controls. Its independent model checks ownership,
legacy adoption, current input identity, external edits, intact replacement,
refusals and uncertain installations through the real shared installer. It
uses a 60-example/50-step budget and guided starting states; bounded exploration
is not exhaustive. Targeted ownership/source-guard sensitivity machines shrink their generated
continuations into replayable counterexamples; their known starting prefixes
are fixed. The complete replays pass with the real producer.
A return-value control rejects boolean byte counts despite Python's `True == 1`.
The initial reset-dominated search and a later refactored broad search missed
a mutant; targeted sensitivity checks make this limitation explicit. An initial
replay parser observed only construction; the corrected parser requires all
actions through teardown. These inadequate observations remain retained. Tests establish serialized namespace custody under authored faults,
not natural-task benefit, race freedom or physical power-loss behavior.

Install `ci/publication_requirements.txt` before discovery; Hypothesis and
SortedContainers are exact pins. Missing dependencies fail collection. The
existing shared CI action is configured to exercise the suite in each tier. Local Hypothesis
caches are ignored; fixed regressions remain canonical source. A passing test
suite does not bypass expired action/installer review gates.
