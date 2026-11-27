# Where did the missing citations go?

Protocol frozen before examining any follow-up outcomes. Compare document retrieval and sentence selection on a separate set of science claims while preserving the two-reading verifier, its zero-cutoff pooling rule and the two-sentence citation limit from the [SciFact study](../scifact_citation_check/protocol.md). The question is whether either change delivers additional correct verdicts carrying usable evidence under the same retrieval and model-call budget.

## Eligible evidence

Use the authors' [SciFact-Open release](https://github.com/dwadden/scifact-open/blob/main/doc/data.md). Its claims come from the original SciFact test split. Form a fixed catalog from the released candidate abstracts, excluding every paper cited by or returned to either previous study split. Exclude claims whose cited papers intersect that previous set, any earlier claim ID, and the data-guide examples 170 and 263. The pre-outcome metadata count is 65 eligible claims. Some abstracts may previously have been indexed as background. Pretraining exposure is unknown. This is a retrieval comparison inside a benchmark-provided candidate catalog, with a narrower population than search over 500,000 abstracts.

Only citation-provenance annotations supply human sentence highlights. Treat all highlights for a document as required for the primary score because this release flattens alternative rationale sets. This conservative rule can lose valid citations. Pooled annotations can establish a document label but their model-generated highlights cannot earn human citation credit. Keep all eligible claims in the denominator, even when the annotations cannot certify a release. No tuning on this cohort.

## Four paired decisions

1. Use the prior decision rule with TF–IDF over documents and sentences (English stop words, word unigrams and bigrams, sublinear TF, title counted twice).
2. Change only the document ranking to BM25 (k1=1.2, b=.75, positive Robertson IDF, same analyzer and twice-weighted title).
3. Keep TF–IDF retrieval and change sentence selection. Rank first by BM25, using document-corpus IDF and sentence-length normalization. For the second sentence, give query features already matched by the first half their original weight. Resolve ties in input order.
4. Apply both changes to expose any interaction.

Search all eligible documents, return one, cite at most two sentences from it and keep their source order. Score the title plus neighboring sentences and the citation alone with the same pinned MiniLM NLI model, 256 tokens per reading. Pool their probabilities. A neutral winner holds the answer. Model votes, candidate budget and maximum input are matched. Count actual tokens, document candidates and sentences ranked separately. No wall-clock, energy or human-time inference.

## Score and decide

Publish per-arm counts for retrieval of a human-annotated paper, coverage of all its highlighted sentences, justified and unsupported releases and holds. Also count returned papers matching any annotated document label. A justified release requires the annotated verdict and a complete human citation in the selected document. Report every paired change and the total work. Compare each single change to the baseline using net additional justified answers. Generate descriptive 95% intervals on counts per 100 claims by resampling connected groups sharing cited or claim-origin papers (5,000 draws, seed 1742). For a recommendation to switch on these data, require a positive lower limit and no additional unsupported releases. An inconclusive or negative comparison keeps the original reference. The combined arm is diagnostic. Unadjusted intervals and a single public collection limit generalization.

## Replay

From the checkout, install the preceding study's pinned requirements. The full runner reads the same upstream model and downloads the digest-checked SciFact-Open archive into the supplied cache. Only IDs, decisions, scoring flags and work counters enter the saved case file.

~~~sh
python3 experiments/scifact_retrieval_followup/run.py /tmp/scifact-cache > /tmp/retrieval-cases.json
cmp /tmp/retrieval-cases.json experiments/scifact_retrieval_followup/cases.json
python3 experiments/scifact_retrieval_followup/score.py > /tmp/retrieval-summary.json
cmp /tmp/retrieval-summary.json experiments/scifact_retrieval_followup/results.json
~~~
