# Does a mandatory citation check earn its second pass?

Frozen before scoring. We compare two release policies on Wadden et al.'s [SciFact](https://aclanthology.org/2020.emnlp-main.609/) task. Claims and abstracts originate outside this project. The endpoint is agreement with an annotated scientific verdict and a complete rationale within a two-sentence citation. Missing annotations can penalize valid alternative evidence. This is a local reanalysis, with no independent reproduction or human timing.

## What both policies see

Retrieve one abstract by word TF–IDF cosine across the full corpus (unigrams and bigrams, English stop words, sublinear TF, title counted twice). Within it rank sentences by the same cosine and choose up to two, restored to source order. Resolve score ties by original order. No cited document IDs or labels enter retrieval or inference. The frozen quantized [MiniLM NLI cross-encoder](https://huggingface.co/cross-encoder/nli-MiniLM2-L6-H768/tree/b95119ce93d3e065de6214e38cd4a97b0f2f2c6d) reads each premise paired with the claim. Pass A reads the chosen sentences, their immediate neighbors and the title. Pass B reads only the exact sentences to be cited. Use at most 256 tokens per pair. Both policies receive the same two predictions, tokens and retrievals on every claim, including holds. They can each release a SUPPORT or CONTRADICT verdict with that citation, or hold.

* **Pool both passes.** Average the three label probabilities across the two passes. Release the winning non-neutral label above the threshold. A second reading can correct the first.
* **Require agreement.** Release only when both passes choose the same non-neutral label and its lower probability meets the threshold. This can suppress releases through explicit citation agreement. The verifier shares model errors with the first pass.

## Freeze and adjudicate

Use the official labeled train split for threshold development and reserve the labeled dev split for evaluation. Exclude dev claim 3 and every claim sharing its cited paper because the dataset card illustrates that item. Omit training claims sharing any reserved dev citation. Use research annotations only to partition and score. The official unlabeled test is outside this study. The model's pretraining exposure is unknown.

For each arm try thresholds 0.00 through 1.00 in steps of .05 on development only. A release is justified when its document and verdict match and its citation contains one entire annotated rationale. Also count exact rationale matches. Every other release counts as unsupported by this scoring rule. Hold all abstentions for review, recording how many had any annotated evidence. On development select two operating points:

* **Triage:** maximize justified releases minus unsupported releases, subject to holding at most half the intake. If infeasible, minimize the number held first and then maximize the same utility.
* **Publication:** maximize justified releases subject to at most 20% unsupported among releases and at least 15 releases. If infeasible, hold everything.

Resolve ties by fewer unsupported releases, then the lower threshold. Save chosen policies before scoring reserved outcomes. Primary comparison is the difference in triage utility per 100 held-out claims (agreement minus pooling). Prefer a mandatory gate only if the lower 95% paired bootstrap limit exceeds zero and its held-out review fraction meets the budget. Otherwise retain pooling as the reference, reporting any budget failure. The quality floor is a development rule, not a guarantee on new papers.

Resample connected groups of held-out claims sharing cited papers, retaining all claims in each sampled group, 5,000 draws with seed 742. Report descriptive percentile intervals for the primary difference and operating-point error fractions. A zero-release fraction is undefined. Record all disagreements and case identifiers, token counts before padding after truncation, and number of forward examples. These costs exclude retrieval indexing, queue delays and operator labor. Publish counts and identifiers without republishing abstracts.

## Reproduce

Use Python 3.12 and install the frozen dependencies in requirements.txt. Run these commands from the repository root with an empty writeable cache (or reuse the same checked inputs).

~~~sh
python experiments/scifact_citation_check/predict.py /tmp/scifact-cache
python experiments/scifact_citation_check/score.py select
python experiments/scifact_citation_check/score.py evaluate
~~~

Prediction creates two files of identifiers, probability vectors, citation matches and cost counters. Selection reads only development rows. Evaluation verifies the saved policy against development and writes the reserved results. For an inexpensive replay from retained predictions, run just the two scoring commands.
