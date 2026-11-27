---
name: asi-stack-reader
description: Consult The ASI Stack living book to locate a passage, check a saved decision against later evidence, and cite a result with its scope.
---

# Read The ASI Stack

Start with the [evidence catalog](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/evidence-catalog.json). It is JSON and works without browser JavaScript, an installation, or a repository checkout. Use the [book search](https://corbensorenson.github.io/asi-stack-book/) for subjects outside this selected catalog.

1. Search the catalog’s titles, questions and aliases in the reader’s words. If given a record ID, select its exact match. The summary, disposition and limit answer different questions. An outside question marks a limit of the measurement.
2. Open the record’s URL or a more specific locator relative to the [book root](https://corbensorenson.github.io/asi-stack-book/). Check the determining passage, comparison and denominator. A graph neighbor can lead to evidence without itself establishing the claim.
3. For a saved record and full book revision, use [citation history](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/citation-history.html). Check whether the later observation corrects a decision, changes the workload, or only edits its description. For other kinds of records follow their versioned provenance.
4. Give the decision, the decisive evidence, and its limit. Cite the exact passage URL, record ID, and catalog source_commit. Append the result digest when citing a run. When the needed quantity was never measured, say so and cite the measurement boundary.

For example, “How much operator time did the verifier save?” leads to evidence_passage:verifier-measurement-boundary. Pipe messages and local bytes cannot supply minutes of labor. For the original Atlas proceed screen, start at evidence_passage:atlas-original-proceed-decision and inspect the superseding record and the corrected comparator table before quoting the outcome.

For a bounded graph lookup, open the [graph manifest](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/manifest.json). Its search index maps IDs to shards. A shard contains the node and a preview of typed relationships; the relationship pages carry additional neighbors. Use the snapshot_id to keep records from the same edition together. For an offline analysis, download the archive named in that manifest.
