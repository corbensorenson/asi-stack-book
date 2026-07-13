# Post-v2.3 Clean Handoff Receipt

Receipt date: 2026-07-13

Roadmap authority:
`docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md`

Terminal state: P0 and M1 completed; P1 and M2 active

## Exact source transaction

The reviewed post-v2.3 cycle begins after activation baseline
`cb7493ae57d576a8bf5fcc54f375683ecf929b54` and terminates at tested source
commit `c2db70988cb3b06860c2994c0bb2e7f3e2874544` on `origin/main`:

1. `371cfb44c5e90cc67bbd4668287391683157bf69` — record post-v2.3 quality,
   reader, and successor cycle;
2. `780bd45424cf23ec5d6079b8ea9c217600ca6561` — repair the generated
   no-promotion count;
3. `36924ad4e884dcda9d06f3fa8d0d1612b08ee70f` — track the exact v2 reader
   archive required by the release record;
4. `09ea8e9f6afd857cf27dd715e16fa75dbc4cecdd` — pin the reader validator's
   clean-environment dependency; and
5. `c2db70988cb3b06860c2994c0bb2e7f3e2874544` — make exact-reader validation
   replay the tracked archive in a clean checkout.

The initial cycle was kept atomic because its generated manifests, chapter
prose, Lean bridges, evidence transitions, reader records, proof manifest, and
validators are digest-coupled. The four follow-up commits are narrowly scoped
clean-checkout truth repairs discovered by the hosted gate. Failed intermediate
runs are preserved in GitHub Actions; they are not represented as passing
evidence.

## Local gate

Before the terminal push, the exact source tip passed:

- the deep registry base gate plus 279 registered units;
- all 68 Lean jobs;
- the 67-input Quarto render and 67-page/54-chapter Human view;
- 112 all-chapter/all-viewport browser page-view pairs;
- exact v2 reader validation in both local-render parity and archive-only replay
  modes: 59 pages, 118 browser/accessibility views, 5,432 internal links, 1,138
  anchors, and six rejecting mutations; and
- staged diff, credential-pattern, private-path, ignored-path, and oversized
  artifact review.

The tracked curated-reader archive remains exactly
`a2caa97fb9281e1fdfc9a9dda626141d4a876df776c9cbc7408f978751736b50`
with 4,381,864 bytes. Its inclusion repairs clean-checkout reproducibility; it
does not create a new format approval or public reader release.

## Hosted build receipt

- Workflow: `Build tested Pages artifact`
- Run: [29293371709](https://github.com/corbensorenson/asi-stack-book/actions/runs/29293371709)
- Job: [86961594516](https://github.com/corbensorenson/asi-stack-book/actions/runs/29293371709/job/86961594516)
- Source SHA: `c2db70988cb3b06860c2994c0bb2e7f3e2874544`
- Conclusion: `success`
- Completed: 2026-07-13 23:37:25 UTC

The clean Linux checkout installed the pinned runtime, passed generated
scaffold checks, the deep registry, Lean, a clean Quarto render, canonical
public-status validation, live Human-view validation, browser smoke, and exact
tested-artifact verification, then uploaded the commit-bound artifact.

## Deployment and attestation receipt

- Workflow: `Deploy tested Quarto site`
- Run: [29293589178](https://github.com/corbensorenson/asi-stack-book/actions/runs/29293589178)
- Deploy job: [86962240221](https://github.com/corbensorenson/asi-stack-book/actions/runs/29293589178/job/86962240221)
- Attestation job: [86962302532](https://github.com/corbensorenson/asi-stack-book/actions/runs/29293589178/job/86962302532)
- Source SHA: `c2db70988cb3b06860c2994c0bb2e7f3e2874544`
- Deployed URL: <https://corbensorenson.github.io/asi-stack-book/>
- Deploy conclusion: `success`
- Attestation conclusion: `success`
- Completed: 2026-07-13 23:38:12 UTC

The deployment downloaded and verified the successful commit-bound artifact,
then deployed it without rebuilding. The subsequent live crawl attested four
public truth surfaces, all 54 chapter identities, 280 source records, and the
validator's negative controls over the HTTPS Pages site.

## Clean-tree and residual boundary

Immediately before this receipt was written, `git status --short` was empty.
Ignored local-only material remains outside the handoff: Quarto/Lean build
state, `_site/`, `build/`, Python caches, `.DS_Store` files, local archives and
context, raw source inbox/cache material, and private or restricted source
payloads. These are not unexplained candidate changes and were not published.
The exact reader ZIP is the sole intentionally unignored ZIP named by its
manifest and release record.

## Effects and non-claims

P0 is complete. It changed source durability and public handoff truth only.
There is no new immutable living-book release, reader-format approval, tag,
license grant, DOI/archive, chapter-core promotion, evidence transition, model
quality claim, external-human review, screen-reader review, legal WCAG
certification, safety claim, AGI claim, or ASI claim. The latest immutable
public living-book release remains `v2.3.0`, the only approved v2.0 reader
format remains the exact local canonical HTML archive, and all 54 chapter-core
claims remain at `argument`.
