# Knowledge graph usability follow-up

The original comparison emphasized known records and a single hop.
This follow-up adds questions that a researcher might type before knowing
the book's title, a record ID, or the name of a particular study.

## Search

The twelve inputs and stable target IDs are in
[`retrieval_tasks.json`](retrieval_tasks.json). Both rankers received
the same graph from published commit
`13ac08d73fd4cf0b4981685ed3c9aed330c540f5`, snapshot
`15e31e7b865849c1d0bdc66b60d5214ad416e26281a5576f7a3f5aed789bb480`.
The comparison selected the same record type in both arms.

| Ranker | Exact at 1 | Exact in top 3 | Exact in top 10 |
|---|---:|---:|---:|
| Published title and ID search | 1/12 | 1/12 | 1/12 |
| Revised search | 12/12 | 12/12 | 12/12 |

Without record type filters, the revised search placed eleven targets
first. The verifier study placed second, behind a related claim.
The Python and browser validators exercise the twelve filtered cases.
Running them in Chrome against the public explorer and the local
candidate reproduced the first-rank counts in the table.
The queries were authored to expose gaps in the previous search.
The scores describe this task set and leave general agent answer quality
and open-ended question answering unmeasured.

## Navigation

The browser test follows Human Reader unit 9 to Stable Capability
Fields, opens its current core claim, then opens the verifier study
and the absolute-floor run with its evidence limit. It also locates
the e-means mapping in Virtual Context ABI beyond the first four previews
and displays that relationship's passage-review status. Another check
opens the retained source references that lack a confirmed chapter.
These workflows fetch smaller relationship files on demand.

The installed site validator reconstructs every directed relationship
view from the previews and continuation pages and compares it with
the archive. It checks the origin and qualifiers in both directions,
the search positions behind relationship filters, unresolved references,
and the 96 KiB file bound. The CLI independently checks the four-hop
route from Reader unit 9 to the verifier run and rejects the same route
with a three-hop limit.
