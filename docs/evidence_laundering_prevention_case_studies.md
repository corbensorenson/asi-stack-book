# Evidence-Laundering Prevention Case Studies

Last updated: 2026-06-29

This record documents live no-promotion case studies where the repository had a
tempting artifact, passing validator, or reviewed artifact but deliberately
refused to promote a broader claim. It exists to strengthen the selected
`claim-support-states-and-evidence-laundering-prevention` contribution track.

This is not a new evidence-transition record, not a demotion/refutation event,
not an external review, and not support-state movement. It records how existing
release-control surfaces prevented evidence laundering.

## Current Status

| Field | Status |
|---|---|
| Case-study type | No-promotion / anti-laundering examples |
| Live examples recorded | 3 |
| Chapter core support effect | None; all 46 chapter core claims remain `argument`. |
| True demotion/refutation example | Still missing; no chapter core claim is recorded as demoted or refuted by this note. |
| Reviewer effect | None; this is not accepted external review. |

## Case Study 1 - Project Theseus Static Import Did Not Become Self-Improvement Evidence

| Field | Value |
|---|---|
| Tempting overclaim | A static Project Theseus architecture-gate report recorded `ready_for_heavy_training`, `14/14` passed gates, zero external inference calls, pinned source-artifact digest, public fixture digest, and mutation controls, so it could be rhetorically over-read as proof that the ASI Stack has replayed or validated governed self-improvement. |
| Actual accepted claim | `docs/theseus_report_import_slice.md` records a public-safe static report import and digest-verified implementation-reference lane only. |
| Laundering blocked | Chapter-core support promotion; clean Theseus replay claim; deployed runtime behavior; model quality; routing quality; benchmark quality; safety; alignment; transfer; ASI capability; authorization for heavy training inside the book. |
| Blocking evidence | The import records `dirty_at_import_review` and `live_theseus_rerun_blocked_dirty_checkout`, and its validator rejects `support_promotion_overclaim.invalid.json`. |
| Required next evidence | Clean checkout or archived public fixture, exact replay command, negative controls, public-safe artifacts, and a separate accepted evidence-transition record before support-state movement. |

Why it matters: this is the strongest current example of evidence discipline in
the governed self-improvement track. A real implementation-reference artifact
exists, but the repository refuses to let a static digest-verified report become
a broad self-improvement, safety, or runtime claim.

## Case Study 2 - Circle Consumer Gate Did Not Become Proof-Contract Deployment Evidence

| Field | Value |
|---|---|
| Tempting overclaim | The ASI-side Circle consumer gate validates a pinned public receipt fixture, checks theorem IDs and fingerprints, and rejects digest-mismatch, missing-theorem, stale-contract, and unsupported-transfer mutations, so it could be over-read as a deployed proof-contract transport or model-quality claim. |
| Actual accepted claim | `docs/circle_public_replay_consumer_gate.md` records a public consumer gate around a prior Circle receipt. It is CI-verifiable by digest and mutation controls but creates no new accepted support-state transition. |
| Laundering blocked | Chapter-core support promotion; deployed proof-contract transport; model quality; reasoning ability; context length; speed; memory scaling; transfer; deployment safety; ASI capability. |
| Blocking evidence | The note explicitly says the gate does not reproduce Circle Calculus from this repository, does not vendor the external contract pack, and does not create a new accepted support-state transition. |
| Required next evidence | Clean Circle replay, public contract pack or archived upstream pack, workload baselines, metrics, negative controls, and accepted evidence-transition records before broader claims. |

Why it matters: this case separates proof receipt legality from model or
runtime quality. The consumer gate is useful, but the claim stays narrow.

## Case Study 3 - Reader HTML Release Did Not Approve EPUB, DOCX, PDF, Audio, Or Claims

| Field | Value |
|---|---|
| Tempting overclaim | The generated reader HTML artifact passed full local browser review across 59 generated pages, two viewport widths, and 118 page-view pairs with zero failures, while EPUB and DOCX structural inspections also passed. |
| Actual accepted claim | `release_records/2026-06-29-v1-reader-html-855dc277.json` approves one local ignored reader HTML snapshot only. |
| Laundering blocked | EPUB release approval; DOCX release approval; PDF release approval; e-reader approval; audio approval; GitHub Pages artifact publication; source interpretation; proof status; benchmark result; runtime behavior; safety claim; chapter-core support promotion. |
| Blocking evidence | `docs/reader_html_artifact_browser_review.md` and the release record both preserve format residuals and non-claims, including that EPUB/DOCX/PDF/audio remain unapproved. |
| Required next evidence | Format-specific application/layout/audio review, exact artifact records, and release records before any non-HTML reader artifact can be reported as approved. |

Why it matters: this case prevents reader-release laundering. A polished human
artifact can be useful without becoming evidence for the technical claims it
explains.

## Remaining Demotion/Refutation Gap

These case studies show no-promotion behavior, not true demotion or refutation.
The roadmap still needs a future live case where a chapter core claim,
subclaim, source mapping, proof target, or evidence lane is narrowed, demoted,
retired, or refuted because evidence failed, prior art undercut the claim, a
reviewer found a serious error, or a replay could not be reproduced.

That future record should name:

- the claim, proof target, source mapping, or evidence lane affected;
- the old support state or roadmap status;
- the evidence, reviewer finding, source note, proof limitation, or failed
  replay that forced the change;
- the new support state or disposition;
- downstream chapter, appendix, source, proof, reader, release, and validator
  updates;
- exact non-claims and recovery conditions.

## Non-Claims

- This record does not create a new evidence transition.
- This record does not promote any chapter core claim above `argument`.
- This record does not demote or refute any chapter core claim.
- This record does not create accepted external review.
- This record does not approve Project Theseus replay, Circle replay, EPUB,
  DOCX, PDF, e-reader, audio, DOI, archive, or deployment readiness.
- This record does not prove the claim-support methodology is complete; it
  records current no-promotion behavior and the remaining demotion/refutation
  blocker.
