# FB1

Table 3 compares bits per byte and downstream task scores across chunking rules trained within the same 0.6B architecture at the reported 50B-token scale. It averages three runs. Those outcomes characterize the tested configurations. To establish that the same rule preserves meaning on a new language, evaluate it on that language with examples that expose meaning-changing splits and a task-relevant reference. The chapter export reports the metric families and run count. The individual downstream columns and values are unresolved from that export.

Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. [Chapter §55.11.3, Table 3 discussion](https://corbensorenson.github.io/asi-stack-book/chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html#a-fixed-budget-for-learned-byte-boundaries)

# FB2

ByteFlow fixes the number of selected boundaries, top-K, and therefore the computation shape for the same packet length and budget. It uses local coding-rate scores derived from the input to rank positions, so equal-length packets can keep different slots. Useful lower-ranked splits can lose a slot when the budget is full. Before relying on the decisions for a literal controller field, test exact field recovery from the original bytes after chunking, including cases where the relevant split moves or falls out of top-K. Validate the recovered identifier against the literal source bytes before using it.

Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. [Chapter §55.11.3, packet example](https://corbensorenson.github.io/asi-stack-book/chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html#a-fixed-budget-for-learned-byte-boundaries) · [§55.32, ByteFlow source crosswalk](https://corbensorenson.github.io/asi-stack-book/chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html#source-crosswalk)

# FB3

A ratio loss controls the pressure to make fewer chunks. Byte-level encoders score boundaries, and the selected vectors feed the shorter, deeper stream. Smoothing, upsampling, and residual paths bring it back to byte resolution for autoregressive prediction. Compare both segmenters on the same device, raw inputs, and quality target with realistic mixed-length batches and batch sizes. Measure chunk-count distributions, peak memory, end-to-end latency including the tail and fallback path, and verified acceptable outputs per elapsed time and by the deadline. Retain the incumbent if the dynamic segmenter delivers fewer acceptable outputs by that deadline. The source-reported data and training-FLOP comparisons leave actual mixed-length serving performance open.

Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Record `evidence_passage:h-net-serving`, citing H-Net §§2.1–2.4, 3, and 4. [Chapter §55.11.2](https://corbensorenson.github.io/asi-stack-book/chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html#h-net-learns-the-sequence-hierarchy)

# FB4

The authors report that a 109M-parameter text JEPA outscored evaluated language models through 72B parameters on specified representation-alignment measures. The identity-predictor theorem is conditional on assumptions including injective renderings and population and uniqueness conditions. The practical experiments use LeJEPA without meeting the theorem's hypotheses exactly. Whether the encoder can replace a text-generating specialist remains open. Keep the downstream consumer fixed and test whether the candidate preserves the distinctions and text-generation behavior the specialist's task requires.

Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Record `evidence_passage:jepa-alignment-boundary`, citing Platonic JEPA §§2.1–2.3, 4.2–4.3, and 7. [Chapter §55.11.1](https://corbensorenson.github.io/asi-stack-book/chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html#jepa-is-a-prediction-objective-not-a-complete-agent) · [§55.32, theorem scope](https://corbensorenson.github.io/asi-stack-book/chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html#source-crosswalk)
