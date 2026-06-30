# Chapter Consolidation URL and History Policy

Last updated: 2026-06-30

Status: active policy for future consolidation execution; applied to the 2026-06-30 Part I pilot through static historical stubs.

This policy defines how public chapter URLs, stable chapter IDs, source history,
and reader/research traceability must be handled when a governed
consolidation package executes. It is a release-control policy, not source
evidence, not an external review, and not a support-state transition. The
2026-06-30 Part I pilot applied the policy through static historical stubs and
`docs/chapter_history_ledger.md`.

## Decision Boundary

- The canonical manifest now has 52 chapters after the executed Part I pilot.
- This policy does not by itself retire, merge, redirect, or remove any chapter; execution commits do that work.
- A future merge or fold remains blocked until its package explicitly records
  the URL treatment for every retired source chapter.
- If a retired public chapter URL cannot be preserved or deliberately recorded
  as a reviewed historical exception, that merge must be deferred.

## Default URL Policy

The default policy for future merges is continuity first:

1. Keep the destination chapter's existing stable ID and public URL whenever
   continuity is stronger than renaming.
2. Retire at most one source chapter slug per execution commit unless a review
   record explicitly approves a larger move.
3. Preserve every retired source chapter's public URL with a static redirect or
   historical stub in the same execution commit.
4. Remove the retired source chapter from rendered book navigation only after
   the redirect or historical stub is validated.
5. Record the retired source chapter in a chapter-history ledger with its old
   title, old stable ID, old URL, destination stable ID, destination URL,
   preserved subclaims, preserved source IDs, preserved proof tags, and
   no-support-state-change boundary.

The redirect or historical stub must be outside the normal book spine. It may
point readers to the destination chapter, but it must not appear as a live
chapter, source-derived evidence, proof result, or reader-release artifact.

## Allowed Treatments

| Treatment | When allowed | Required record |
|---|---|---|
| Static redirect | Preferred when the retired slug has been public on GitHub Pages. | Redirect target, destination chapter, old slug, validation command, and changelog entry. |
| Historical stub | Allowed when a redirect is not technically available or when readers need a visible explanation. | Stub content, no-index/navigation exclusion, destination link, preserved-history note, and validation command. |
| Historical exception | Allowed only when a reviewer accepts that an old URL will not be preserved. | Explicit reviewer decision, reason, affected URL, release note, and non-claim boundary. |

Silent deletion is not allowed. A future consolidation commit must not make an
old chapter URL disappear without one of the treatments above.

## Required Merge Record Fields

Every executed merge or fold must record:

- source chapter stable ID;
- source chapter title;
- source chapter public URL;
- destination chapter stable ID;
- destination chapter title;
- destination chapter public URL;
- selected URL treatment;
- preserved source IDs;
- preserved external-source IDs;
- preserved Appendix C claim or subclaim treatment;
- preserved Lean proof tags and module names;
- preserved test, harness, schema, or fixture rows;
- preserved implementation horizon;
- reader-overlay, Human Reading Path, and Handoff repairs;
- validation commands run;
- release and support-state non-claims.

## Pilot Defaults

For the Part I alignment/governance pilot:

| Proposed destination | Continuity URL | Retired source URL treatment |
|---|---|---|
| `constitutional-alignment-substrate` as **Constitutional Alignment: Agency, Dignity, and Corrigibility** | Keep `/chapters/constitutional-alignment-substrate.html`. | Preserved `/chapters/agency-dignity-and-corrigibility.html` through a static historical stub in the 2026-06-30 execution package. |
| `moral-uncertainty-and-value-conflict` as **Moral Uncertainty, Value Conflict, and Contestable Governance** | Keep `/chapters/moral-uncertainty-and-value-conflict.html`. | Preserved `/chapters/governance-rights-fork-exit-and-audit.html` through a static historical stub in the 2026-06-30 execution package. |

These defaults were applied to the Part I pilot and remain defaults for future
accepted execution packages.

## Validation Expectations

Before a future merge commit is accepted, validation should prove:

- the destination chapter renders at the selected continuity URL;
- the retired URL treatment exists in rendered output or in a reviewed
  historical exception record;
- the retired source chapter is absent from the normal rendered book spine if
  it has been folded;
- the destination chapter names preserved subclaims, source IDs, proof hooks,
  implementation horizons, and non-claims;
- the chapter-history ledger records the retired source chapter;
- `book_structure.json`, `docs/book_outline.md`, Appendix C, Appendix K,
  proof manifests, reader matrices, handoffs, external-grounding ledgers, and
  changelog are updated in the same execution package;
- no support state is promoted unless a separate accepted evidence-transition
  record justifies it.

## Non-Claims

- This policy does not by itself execute a merge or fold.
- The 2026-06-30 Part I execution package, not this policy text alone, implemented two historical stubs and changed the manifest to 52 chapters.
- This policy does not approve any destination draft.
- This policy does not create external review evidence.
- This policy does not promote any claim support state.
