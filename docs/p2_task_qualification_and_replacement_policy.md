# P2 Task Qualification and Replacement Policy

Date: 2026-07-17  
State: **policy frozen before draw; metadata queue now frozen; candidate content and final pool unopened**

The first fixed-denominator gold preflight exposed exactly the false-negative
risks the competence standard is intended to catch: official images that fetch
dependencies after tests begin, an upstream parser that ignores AVA's visible
failure grammar, compile/panic paths that make stored named-test expectations
unobservable, and tests that contact external resources during outcome
execution. None is evidence against governed repository admission.

Every development task must now pass two repetitions of a test-patch-only arm
and a human-gold-plus-test-patch arm from the same sealed environment with
runtime networking disabled. Dependency materialization is separate from
outcome execution and may not apply either task patch. Claim-bearing use
requires a hermetic snapshot or prospectively allowlisted, content-digest-
verified fetch; unrestricted setup egress remains diagnostic only.

The baseline must emit exactly the stored pass-to-pass and fail-to-pass status
sets. The human-gold arm must exit successfully and emit exactly their union.
Missing, extra, or unobservable test identities fail the task construct; they
cannot be waived after inspecting the outcome. A pinned upstream parser and an
independently implemented evaluator must agree exactly after calibration on
pass, named-fail, compile/collection-fail, malformed, missing, zero-exit-visible-
failure, and parser-disagreement cases. Raw logs are mandatory even for aborted
attempts.

An invalid original task receives N0 with no claim effect and remains in the
lineage. Replacements are not hand-picked. Invalid slots are processed in
lexicographic order, and candidates from the same language are ordered by the
frozen SHA-256 key in the machine record. Candidates are opened sequentially;
the first fully qualified candidate fills the slot, every failed candidate is
retained, and no candidate may be skipped after its outcome is known. Ten
candidates per slot is the stop rule; failure to fill a slot leaves the corpus
gate blocked.

The resource ceiling must be frozen before the first replacement draw and must
include pull, expanded image, dependency setup, per-arm time, memory, CPU,
emulation, disk recovery, cleanup, and residuals. A resource failure means the
local campaign cannot competently use the task. It is not a negative result
about the book's mechanism.

The final held-out pool remains unselected and unopened.

Machine record:
`evidence_quality/p2_task_qualification_and_replacement_policy.json`.
