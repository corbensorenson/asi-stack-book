# Finding and citing a decision

**Five of six reserved questions returned a determining record in the first three evidence results, up from four of six.** The new maze passage accounted for the additional hit. Both agents answered the three yes/no questions correctly. The agent that started with the skill cited the corrected Atlas table and explained its inference limit. It also opened more bytes.

## Retrieval

| Reserved question, abbreviated | Earlier rank | Revised rank |
|---|---:|---:|
| Fallback behind an intermediary when the primary is down | 3 | 1 |
| Cheaper partitions bury the release-note correction | 1 | 1 |
| A ledger for a backlog of arriving checks | 1 | 1 |
| Dollar figure for reviewer hours | 2 | 2 |
| Warm puzzle fit and end-to-end maze solving | No match for target | 1 |
| Maintenance team’s annual payroll saving | No result | No result |

Every ranked determining record above has a scope statement and a destination with a matching HTML fragment. The last question earned zero boundary credit in both versions. An empty list leaves the reader to work out whether payroll was measured. These are six author-selected questions over a selected evidence catalog. The maze record was added in this revision, so the gain combines coverage and retrieval. The evaluation kept the reserved wording out of tuning. [Frozen questions and rules](protocol.md) · [Ranks, top three, destinations and limits](search-results.json)

## Cold search

In eight fresh local browser contexts per version, we exercised the published search adapter with four fixed development queries in each of two scopes. Time starts immediately before lookup and ends at the first result set containing a determining evidence record. This excludes typing and dropdown painting. Each cell has one observation. The cutoff was five seconds.

| Query | Earlier All / Research evidence (ms) | Revised All / Research evidence (ms) |
|---|---:|---:|
| When is the second hop worth it? | miss / miss | 26 / 17 |
| How do I know if my index lost the correction? | miss / miss | 10 / 17 |
| What if checking cannot keep up with new work? | miss / 54 | 15 / 10 |
| e-means | 249 / 58 | 12 / 25 |

Each earlier lookup loaded 10,902,907 uncompressed index bytes. Revised Research evidence loaded 179,128 bytes per cold lookup. Revised All showed the evidence hits early and still fetched the 10,913,981-byte full index, for 11,093,109 bytes after settling. This change reduces total bytes for evidence-only use. In All it changes when evidence becomes available and slightly increases eventual traffic. Browser, loopback server, disk cache and lack of network compression limit transfer to public-site latency. The timing probes were used in development. [Browser harness](evaluate.cjs)

## Clean-agent reading comparison

Two fresh agents with the same inherited model configuration used the same text reader, three questions, rendered documents and read allowance. Only their entry route differed. One unblinded assessor scored explicit dispositions, determining citations and limits under the published scoring instructions. The source revision was `7c6136ee12b673dbda7c0016edd3b5af3c5c8d6c`. The local reading corpus combined unchanged rendered resources with the revised chapters, reader and projections. The hashes identify the actual resources opened. [Session instructions and rubric](session.md) · [Corpus hashes](session-corpus.json)

| Entry | Receiver | Atlas | Verifier | Unsupported numerical answers | Opens | Bytes opened | Bytes displayed |
|---|---:|---:|---:|---:|---:|---:|---:|
| Homepage | 3/3 | 0/3 | 3/3 | 0 | 10 | 1,230,085 | 28,855 |
| Reader skill | 3/3 | 3/3 | 3/3 | 0 | 9 | 1,669,562 | 30,311 |

The homepage answer correctly rejected the original proceed decision. It did not state the replacement stop decision, cited a retrieval case, and bounded the retrieval exercise instead of the underlying Atlas comparison. Giving credit for the yes/no answer alone would change its total from 6/9 to 7/9. The skill answer named the stop, linked Table 5, and identified same-seed rescoring after outcome inspection. It supplied stable IDs and run digests, although its two run citations gave the evidence revision without separately repeating the book revision beside each. The homepage answer used relative links and omitted revisions. [Homepage answer](homepage-answer.txt) · [Skill answer](skill-answer.txt)

The skill gives Atlas and verifier examples in its instructions. One session per arm cannot distinguish the effect of those examples from general citation guidance or variation between model runs. Both entry routes allowed discovery of the skill. The tool counted the whole uncompressed resource on each open, including repeat lookups in a catalog. Neither human timing nor production bandwidth was measured. [Homepage reads](homepage-opens.json) · [Skill reads](skill-opens.json)
