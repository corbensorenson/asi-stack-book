# Round 23 reader-prose quality reconciliation

Status: **active editorial remediation**
Authority: Corben Sorenson
Canonical roadmap: `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`
Machine status: `roadmap_records/p7_1c_reader_prose_quality_status.json`

## Why this packet exists

The owner supplied a detailed Claude review after a real reading pass over the
thesis chapters and representative mechanism chapters. It found that the
book's architecture, noninheritance law, three-projection device, efficiency
denominator analysis, and self-falsifying posture are strong, while the
reader-facing prose is too specification-shaped. The review's actionable
criticisms are:

- concepts are rarely instantiated in a concrete scene or worked trace;
- long mechanism enumerations and multi-clause core claims hide the argument;
- disclaimer language is over-distributed, especially in newer thin chapters;
- the direct, memorable voice already present in Human Reading Path blocks is
  quarantined instead of being used in the main argument; and
- claim/source bookkeeping interrupts the reading surface even when the same
  mapping already has a canonical appendix owner.

The review reports approximate corpus measurements (about 640,000 words, ten
uses of “for example,” no “for instance,” three “worked example” occurrences,
one “case study,” and about 820 disclaimer phrases). Those numbers are review
signals, not yet repository authority. P7.1c must reproduce them with a pinned
tokenizer and phrase taxonomy before using them as a baseline. The point is
not to optimize a phrase counter; it is to make every chapter easier to
understand without deleting a claim, caveat, source, proof boundary, or
non-claim.

## Calibration tranche executed (2026-08-02)

The first editorial tranche is now in the canonical live chapter sources. It
covers the stack thesis, efficient-ASI thesis, failure model, inner-alignment
chapter, and claim-ledger chapter. Each received a chapter-specific
illustrative failure, a state-labelled worked trace, and a strongest simpler
baseline or counterexample. The scenes are explicitly pedagogical: they do not
report incidents, benchmark outcomes, objective-identification results, or
support-state changes. The inner-alignment chapter also received a
digest-bound semantic re-review because its existing concept contract is
active; the review records the new prose as editorial substance with
`support_state_effect: none`.

This tranche is a calibration pass, not the 84-chapter closure. The machine
status therefore records `active_calibration_tranche_complete_packet_contract_ready`
while the per-chapter packet count remains zero until the packet writer and
adversarial fixtures are applied to the tranche. The remaining chapters still
require their own scenes, traces, caveat dispositions, and digest-bound
packets.

## Diagnosis and disposition

This is a prose and reader-model defect, not a reason to add chapters. The
84-chapter manifest, source crosswalk, atom registry, proof ledgers, and
evidence ceilings remain canonical. P7.1c therefore modifies existing owners
and their reader projections only. It does not promote support, rehabilitate a
negative result, create a new empirical result, or change the scientific P2
headline.

The remedy is a bounded editorial ratchet:

1. **Instantiate the mechanism.** Every chapter receives a chapter-specific
   opening failure, decision, or discovery scene. The scene names the system or
   actor, the attempted action, the observable bad outcome or uncertainty, the
   exact boundary that failed, and the residual left behind. It is 150–250
   words unless a shorter form is justified by the chapter role. The scene is
   followed by one worked trace with explicit state changes and one
   counterexample or strongest simpler alternative.
2. **Turn schemas back into arguments.** Replace field-by-field clause piles
   with four or five prose groupings that explain why the fields matter. Split
   mega-sentence core claims into a readable claim, a short normative rule,
   and a formal binding block. Keep the full fields in the canonical appendix
   or a collapsible reader surface, with stable atom/source links preserved.
3. **Budget caveats without weakening honesty.** Keep one local boundary
   sentence where a reader needs it and move repeated limits into one
   chapter-level “what this does not establish” block. A normalized disclaimer
   audit may flag density, but an editorial disposition—not blind deletion—must
   preserve every distinct limitation and its scope.
4. **Un-quarantine the good voice.** Rewrite the main argument in the direct,
   agentive, concrete register already demonstrated by the Human Reading Path.
   A paragraph should normally identify who or what acts, what changes, and
   why the reader should care before it introduces the record schema. Human
   Reading Path blocks remain useful summaries; they are no longer the only
   place where the book is allowed to sound like a book.
5. **Move bookkeeping off the argument path.** Claim/source tables, repeated
   status ledgers, and validator-facing inventories belong in Appendix C or
   linked detail blocks. The prose keeps only the local evidence decision and a
   stable link to its canonical record. A table may remain inline only when its
   comparison is itself the argument and the packet records why.

## Packet contract

Each of the 84 chapters gets one digest-bound packet under
`evidence_quality/reader_prose_quality_packets/`. A packet records:

- chapter identity, current QMD digest, role, and reader-spine unit;
- the concrete scene, its named failure boundary, and the residual owner;
- the worked trace, state-transition labels, counterexample, and simpler
  baseline;
- the short claim, normative rule, formal binding/appendix link, and stable
  claim-atom/source identities;
- the local caveat retained, the caveats consolidated into the chapter-level
  boundary block, and any justified exception;
- the bookkeeping moved out of the reading surface and the surviving local
  evidence link;
- a before/after semantic-diff disposition and reviewer checklist; and
- word count, sentence/paragraph diagnostics, reproducible phrase counts, and
  an explicit “no support or release movement” decision.

The packet is an editorial contract, not evidence that the chapter's claims
are true. A changed chapter digest invalidates its packet and reopens the
chapter for review.

## Acceptance gates

P7.1c is complete only when all of the following are true:

1. 84/84 current chapter packets exist, validate, and bind to the current
   manifest and reader-spine crosswalk.
2. 84/84 chapters contain a concrete scene, a worked trace, a failure or
   counterexample boundary, and a chapter-specific handoff. Thin reference or
   speculative chapters may use a bounded domain vignette, but may not satisfy
   the gate with a generic schema restatement.
3. 84/84 core claims have a readable short form plus a separately addressable
   formal binding. No atom, source, proof, equation, protocol, or non-claim is
   lost in the split.
4. The pinned prose audit reports disclaimer density by chapter role and
   identifies every outlier. No chapter may exceed twice the mature-role
   median or the mature-role 95th percentile, whichever is the more permissive
   ceiling, without a chapter-specific semantic justification. The audit must
   show that distinct limitations remain present after consolidation.
5. A reader-surface audit confirms that the main text uses the direct/agentive
   register in every major section, while schema and source bookkeeping are
   reachable through stable appendix/detail links rather than repeated inline
   tables.
6. A semantic diff, link audit, Quarto render, browser Human-view check, and
   accessibility-tree smoke pass cover all 84 chapters. The result preserves
   exact source, claim, proof, evidence, release, and non-claim identities.
7. An adversarial editorial fixture rejects copied generic scenes, invented
   outcomes, deleted caveats, broken atom links, stale chapter digests, and
   unsupported “worked examples.”

The gate is deliberately not a word-count target. Additional prose is useful
only when it adds a concrete mechanism, decision, consequence, source, or
boundary. P7.1c cannot close by inflating chapter length or by moving detail to
an appendix without preserving reader-comprehensible explanations.

## Order of work

Run the thesis spine and three representative mechanism chapters first to
calibrate the packet and phrase taxonomy. Then process chapters by reader role
(thesis-bearing, load-bearing reference, implementation case,
speculative/research), with the same semantic diff and adversarial fixtures for
each tranche. Regenerate the 84-chapter reader derivative only after packet
digests are current. Reconcile the landing page, README, synopsis, Appendix C,
source crosswalk, and video narration briefs only after the prose packet closes;
video scripts must inherit the concrete scenes and traces rather than preserve
the old paragraph-tableau style.

No external prepublication reader is required. The packet is reviewed by the
author-directed Codex workflow, with all decisions and residuals recorded for
later owner feedback. The final public release still requires the existing
exact-`main`, render, deploy, accessibility, rights, and platform gates.

## Non-claims

This reconciliation does not establish that the book's mechanisms work, that
the scenes are representative of reality, that a reader understands them, or
that a visual derivative is synchronized. It establishes an editorial work
program and a fail-closed acceptance contract. Support, release, safety,
deployment, SOTA, AGI, and ASI states remain unchanged.
