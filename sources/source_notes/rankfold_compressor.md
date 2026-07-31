# Source Note: RankFold Compressor

| Field | Value |
|---|---|
| Source ID | `rankfold_compressor` |
| Source title | rankFold compressor |
| Author / lineage | Corben Sorenson with several AI-editor attributions inside the bundle |
| Source dates | February 2026 |
| Ingestion date | 2026-06-24 |
| Fidelity audit | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/11jw0DAAuUvw75Q_1AiwTiUGcd-y_IywB9qdEka9_MfI |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/rankfold_compressor.txt`; raw text is not published. |
| Evidence class | Author-side correction lineage from speculative compression drafts to a bounded codec and implementation specification; not locally reproduced empirical evidence |

## Claim boundary and revision lineage

The 22,636-word cache is a revision history, not one coherent paper. It contains fourteen labeled tabs plus several unnumbered documents embedded in Tab 9. The intellectual movement matters:

1. Tabs 1–4 propose “MatrixFold” as a lossless mapping of arbitrary matrices into fewer vector-pair entries by moving information into hyper-precision scalars, probability distributions, fractal/topological objects, or programs. They add square reshaping, recursive cascades, a meta-selector, quantum-inspired language, purported proofs, broad benchmark tables, and claims of exponential or 1.5–50× gains.
2. Tabs 5–7 abandon most of that machinery and introduce a predictor/corrector codec with Entropy-Aware Rank Optimization (EARO), Morton traversal, claimed prototype ratios, progressive loading, and WORM economics. They still use lossless and superiority language that the later drafts narrow.
3. Tab 8 reframes the codec as explicitly lossy and rate–distortion bounded, but still reports unsupported numeric results and SOTA language.
4. Tab 9 renames MatrixFold to RankFold, supplies increasingly careful public drafts, a finite-alphabet residual coder, exact byte denominator, strong baseline and ablation requirements, a production probe, pseudocode, and a Rust engineering specification.
5. The final addenda introduce NeuralFold. Their mature mechanisms substantially overlap the separately inventoried `rankfold_neuralfold` bundle and are counted as one author-side lineage rather than corroborating evidence.

Later narrowing controls earlier claims. The useful surviving object is a **bounded, lossy, per-tensor rate–distortion codec proposal** plus an independently testable implementation/evaluation plan. Early hyper-precision, bijective low-rank, quantum, fractal, recursive-exponential, benchmark, lossless, SOTA, latency, energy, and repository-availability claims are not imported into the book.

The numeric tables repeat across multiple tabs but no local code, data, output logs, environment, archive fixtures, or benchmark receipts accompany them. Repetition does not turn them into evidence. The source's later phrase “prototype evaluation” remains a source-reported claim below the book's evidence threshold.

## Thesis

The mature RankFold thesis is narrower and technically meaningful: truncated SVD selects a rank-$r$ predictor that minimizes squared residual error, whereas a storage system pays for the serialized factors and the distribution of **quantized residual symbols under a concrete coder**. A different predictor may accept slightly larger numerical error yet yield more zero runs, smaller magnitudes, fewer escapes, or lower actual rate at the same declared distortion. RankFold therefore initializes from SVD and refines the factors with a coder-motivated objective.

This is a per-artifact WORM hypothesis. It does not claim that every tensor is low-rank, that entropy follows variance, that quantization is harmless, or that expensive search wins on hot storage. Dense and high-entropy controls, strong matched codecs, complete bytes, downstream utility, and fallback are central rather than optional.

## Mechanisms

The mature mechanism family comprises tensor unfolding and blocking, low-rank predictor plus quantized corrector, EARO refinement, bounded residual symbolization, topology-aware traversal, an indexed deterministic container, preview/refinement access, dry-run gating, complete accounting, and staged Rust implementation. The early speculative families are retained below as falsified or unsupported design hazards rather than candidate mechanisms.

## The early shortcut family and why it does not compress by itself

### Vector-pair cardinality is not storage reduction

The first drafts claim an arbitrary $m\times n$ real matrix can be mapped bijectively to $m+n$ real entries. As a set-theoretic statement, uncountable Euclidean spaces can have surprising bijections; as a finite storage claim, it is irrelevant unless the representation, precision, decoder, and error contract are counted. Interleaving the digits of $mn$ values into fewer “hyper-precision” reals moves bits into each scalar. It does not lower the description length of the finite source.

A rank-one outer product $uv^\top$ has fewer ordinary scalar parameters only for matrices that actually satisfy the rank-one constraint. A general matrix needs rank up to $\min(m,n)$, a residual, or a richer decoder. The scaling ambiguity $uv^\top=(cu)(v/c)^\top$ also means raw parameter counts are not independent degrees of freedom. Rank-$r$ storage must count $r(m+n)$ factor entries, precision and scale, plus corrector and metadata.

### Square reshaping is a candidate search, not a theorem of entropy reduction

For a fixed element count $K=mn$, the arithmetic expression $m+K/m$ is minimized near a square. That only minimizes a nominal rank-one factor shape. It does not show the reshaped data is rank one, lower entropy, more local under the coder, or cheaper after storing the inverse shape/permutation. Shape can expose or destroy structure. It must be selected on held-out or actual code length under a bounded search budget and compared against domain-native unfolding, row/column permutations, blocking, and no reshape.

### Recursive compression does not multiply free gains

The early drafts assume $H(D_{k+1})\le\alpha H(D_k)$ and multiply per-stage ratios. That inequality is not derived for arbitrary encoded outputs. A lossless pipeline cannot repeatedly count the same removed redundancy. If stage $k$ emits a bitstream $b_k$, the total representation includes the final payload plus every decoder, transform, parameter, boundary, residual, and stage descriptor. A later generic codec may remove remaining redundancy, but the relevant ratio is original bytes divided by the **final complete stream**, not the product of ratios measured against changing denominators.

Recursive or multistage transforms can still be useful as a search family—progressive codes, multiscale residuals, dictionaries, and transform chains are real—but each stage must beat the best direct alternative after overhead. The correct stopping rule compares marginal actual-byte benefit with marginal encode, decode, verification, and governance cost. “Entropy fell” or “another factorization exists” is insufficient.

### Rich decoders need code, state, and residuals

Probability densities, diffusion priors, fractal attractors, manifolds, wavelets, programs, genetic search, distillation, and learned generators can compactly describe structured data. None guarantees exact representation of an arbitrary artifact. Their model parameters, reference corpus, shared decoder, seeds, search procedure, numerical semantics, and residual/repair stream belong in the code length. A distribution is not the original sample; a lossy generator is not a bijection; Kolmogorov complexity is not generally computable; and Banach/Hutchinson convergence of a chosen contraction does not prove that its attractor equals the target data.

The early “quantum-inspired” label adds no physical quantum mechanism. Mutual-information expressions are stated without a defined joint distribution or derivation and do not establish corruption robustness. Cryptographic, homomorphic, energy, and exabyte claims have no threat model or measurement and remain non-claims.

## Mature RankFold object

For a matrix $M\in\mathbb R^{m\times n}$, rank $r$, factors $U\in\mathbb R^{m\times r}$ and $V\in\mathbb R^{n\times r}$, and step $\Delta$:

$$
E_q=\left\lfloor\frac{M-UV^\top}{\Delta}\right\rceil,
\qquad
\widehat M=UV^\top+\Delta E_q.
$$

The complete candidate rate is

$$
B_{RF}=B_{header}+B_U+B_V+B_{tables}+B_{runs}+B_{signs}
+B_{magnitudes}+B_{escapes}+B_{checks}+B_{decoder\ scope}.
$$

The source often abbreviates this as header + factors + coded residual. The expanded form is the safer book boundary. If $U,V$ are stored in FP16, their multiplication and accumulation semantics must be declared. Decode can be deterministic with respect to the stored codec and still be lossy with respect to $M$.

“Exact reconstruction” must name the target. The decoder can reproduce the specified $\widehat M$ from the file under fixed arithmetic. That does not imply bit-exact recovery of original FP32 bytes. An exact mode would need a residual defined over the original serialization or arithmetic difference with enough information to close every lost bit.

## EARO and coder alignment

EARO starts from the strong rank-$r$ SVD predictor and refines it using a proxy such as

$$
\mathcal L(U,V)=
\sum_{ij}\log\left(1+\frac{|E_{q,ij}|}{\delta_s}\right)
+\lambda(\lVert U\rVert_F^2+\lVert V\rVert_F^2).
$$

With $Z=(M-UV^\top)/\Delta$ and $E_q=\operatorname{round}(Z)$, the straight-through estimator takes $\partial E_q/\partial Z\approx I$; the gradient to the predictor inherits $-1/\Delta$. The engineering spec derives a deterministic analytic path and proposes fixed-step Adam. The regularizer stabilizes factor scale; it is not a substitute for factor bitrate.

The source evolves from a vague adaptive histogram/arithmetic coder to a concrete bounded integer codec:

- traverse residual indices row-major or through blockwise Morton order;
- emit zero-run lengths, then sign and magnitude for each nonzero;
- code runs with Rice, Exp-Golomb, or bounded buckets;
- code small magnitudes with a finite rANS alphabet;
- emit an escape plus universal code for large magnitudes;
- normalize and serialize the rANS frequency table and termination metadata.

This gives the optimization proxy an identifiable relationship to the code: zero mass affects runs, small-magnitude concentration affects rANS, and the logarithmic tail approximates escape cost. It remains a proxy. Required diagnostics are actual bits by component, proxy/bit correlation, zero-run statistics, nonzero rate, escape rate, and sensitivity to $r,\Delta,\delta_s,\lambda$, traversal, and step count.

## Unfolding, blocking, and progressive access

General tensors require an `UnfoldSpec`: identity for matrices, per-head attention matrices, channel/group views for convolutions, or another declared mapping. Blocking can bound memory and assign local rank/step settings. These choices change both factor cost and residual statistics; they are part of the codec, not preprocessing hidden from baselines.

The MatrixFold drafts contain a useful **preview/refinement** idea. A factor header can provide a rank-$r$ approximation before the residual body arrives. The residual refines that preview to the codec's declared reconstruction. A valid progressive record reports preview distortion and task utility, bytes and latency to each layer, non-monotonic failures, residual ordering, and whether partial decoding is safe for the consumer. It must not call the preview exact, and “full body” is exact only relative to the stored reconstruction contract.

## Probe and production gate

The later draft converts “structured tensor” from an adjective into a codec decision:

1. compute a cheap SVD or randomized predictor;
2. quantize its residual at the candidate $\Delta$;
3. dry-run the actual residual coder and include factor/header cost;
4. compare with the strongest qualified baseline at matched distortion and access constraints;
5. accept RankFold only beyond a calibrated margin; otherwise use the baseline.

The probe is part of system performance. False admissions waste expensive EARO steps and can create larger archives; false rejections miss real savings. Probe bytes, time, memory, error, fallback, and workload shift belong in the evaluation.

## File format and Rust implementation plan

The engineering specification proposes an `RFOLD1`-style stream with a length-prefixed CBOR/bincode header, factor blobs, residual blob, optional checksum, exact offsets, tensor shape and unfolding, per-block rank/step/traversal, coder table, predictor format, and optimizer configuration. The wire sketch is not a frozen standard.

The proposed Rust modules separate container, unfolding, traversal, residual transforms, Rice/Exp-Golomb/rANS coding, table normalization, predictor initialization, EARO, matrix multiplication, CLI, roundtrip, determinism, and malformed-input tests. The staged implementation is useful because it makes independent decoding possible before any performance claim.

Determinism has scopes. Fixed seeds and single-thread pure-Rust math may make encoding repeatable on one machine. BLAS threading, FMA, SIMD, floating-point reduction order, CPU differences, and serialization can still change factors or files. Decode determinism requires fixed endian, rounding, accumulation, factor representation, table normalization, and bounds. Cross-platform identity must be tested, not inferred from a `deterministic` flag.

Security obligations include checked offsets and lengths, bounded ranks/dimensions/output, valid rANS totals and ranges, safe unary/run limits, overflow checks, truncated-stream behavior, decompression-bomb controls, checksum/authenticity separation, fuzzing, and resource limits. A lossy numeric codec also needs NaN, infinity, signed zero, denormal, endianness, dtype, and exceptional-value rules.

## Evidence

The bundle supplies a detailed correction history, equations, repeated claimed
prototype tables, pseudocode, a file-format sketch, a Rust module plan, and an
evaluation protocol. Only the architecture, revision boundary, and proposed
tests are usable here. The numeric tables lack the artifacts needed for local
or independent verification and remain source-reported non-evidence.

### Evaluation program and evidence ceiling

The later paper correctly requires full rate–distortion curves rather than one operating point. A competent evaluation sweeps at least rank, $\Delta$, step count, factor precision, block/unfold choice, and coder settings. It reports exact archive bytes, bits per element, RMSE and contract-specific downstream utility, encode/decode latency, peak memory, energy, random access, preview behavior, probe errors, and corruption/determinism outcomes.

Hard baselines and ablations include:

- literal and Zstd/general-purpose paths;
- quantize + Zstd at the same step;
- dead-zone quantize + Zstd at matched distortion;
- SVD predictor + the **same RankFold residual coder**;
- SVD plus residual shrinkage/soft threshold;
- FPZIP, ZFP, SZ3, or domain codecs at matched distortion;
- row-major versus Morton;
- escape channel on/off under outliers;
- EARO steps 0/25/50/150/300 or an equivalent curve;
- factor precision, unfolding, blocking, and rank/step auto-selection;
- dense, random, already-compressed, pathological-outlier, NaN/Inf, and tiny-tensor controls.

The repeated source tables report ratios around 3.1–4.6×, 15–25% advantages, approximately 10× encoding cost, millisecond progressive access, and specific A100/hyperparameter settings. Those numbers are not reproduced or admissible here because the cache lacks the input artifacts, code, environment, bitstreams, exact baselines, run logs, seeds, or receipts. The earlier 1.5–50×, GLUE/SQuAD/ARC-C, ZipNN, KV, latency, energy, cryptography, and exabyte claims are even less grounded and are superseded as technical evidence.

Decisive narrowing includes: SVD with the same coder matching EARO; actual bytes failing to follow the proxy; quantization/dead-zone controls explaining the win; factor/table overhead erasing it; strong domain codecs winning; Morton helping only selected shapes; expensive search failing WORM amortization; preview utility failing; downstream use changing materially at matched RMSE; deterministic decode drifting; or the production probe routing poorly. A negative result on a naive implementation would not refute the architecture, but a matched, independently checked campaign can narrow it.

## NeuralFold addendum relationship

Tabs 13–14 and preceding unnumbered addenda extend RankFold with implicit neural representations, adaptive/mixture capacity, field tiling, byte prediction plus residual, two-stage codec-aware training, and route fallback. The strongest form is substantially duplicated and expanded in `rankfold_neuralfold`. The book treats `rankfold_compressor` as the correction and tensor-codec lineage and `rankfold_neuralfold` as the canonical archive/front-end lineage. Shared numeric or architecture claims count once.

One NeuralFold draft claims preliminary image gains of 25–40% over COIN++ while also saying code and experiments are forthcoming. That internal tension resolves toward non-claim. Model lists and references are research candidates until independently verified; name-dropping an INR family does not establish its fit, rights, availability, or performance.

## Failure Modes

- **Cardinality laundering:** fewer real-valued slots hide more bits of precision per slot.
- **Rank laundering:** a rank-one/vector-pair form is applied to a general matrix without paying for rank or residual.
- **Shape laundering:** AM-GM parameter arithmetic is described as empirical entropy reduction.
- **Recursive ratio multiplication:** gains at changing denominators are multiplied while stages and decoders are omitted.
- **Generative exactness laundering:** a distribution, diffusion model, fractal, or program is equated with the original sample without residual closure.
- **Kolmogorov overclaim:** an uncomputable shortest-program ideal is described as achieved by a heuristic search.
- **Quantum branding:** undefined “quantum-inspired” language substitutes for a mechanism or bound.
- **Fabricated-evidence risk:** repeated benchmark tables lack artifacts and are promoted by prose such as “camera-ready” or “red team accepted.”
- **Lossless/lossy collapse:** exact reproduction of $\widehat M$ is confused with exact recovery of original bytes.
- **Proxy hacking:** EARO lowers the logarithmic loss while final bytes, escapes, or factor cost rise.
- **Baseline asymmetry:** EARO uses a tailored coder while SVD or quantization receives a weaker one.
- **Progressive authority leak:** a low-rank preview is used where exact or source-faithful data is required.
- **WORM mismatch:** claimed savings depend on reads/transfers or retention that never occur.
- **Determinism overclaim:** same-machine configuration is promoted to cross-platform file identity.
- **Parser/resource attack:** malformed ranks, offsets, runs, tables, or dimensions exhaust or corrupt the decoder.

## Book Chapters Supported

- `rankfold-neuralfold-and-artifact-compression` — primary owner of the correction lineage, RankFold codec, progressive reconstruction, probe, implementation, and evaluation boundaries.

## Claims To Add Or Update

- Preserve the MatrixFold-to-RankFold correction lineage as an example of why information cannot be hidden in precision, richer spaces, recursion, or uncounted decoders.
- State that square factor-shape arithmetic is not evidence of lower rank, entropy, or rate.
- Treat recursive compression as a complete-stream marginal-gain search, never as multiplicative free ratio.
- Distinguish original-byte exactness, deterministic reproduction of a stored lossy reconstruction, and approximate preview.
- Add progressive factor-header/residual-body access as a candidate use with consumer-specific leases.
- Keep EARO, bounded residual coding, production gating, and Rust architecture as design/research objects; reject every unsupported numeric table.
- Use `rankfold_neuralfold` as the canonical mature front-end/archive variant and avoid double-counting the addenda.

## Open Questions

1. Can an independent minimal implementation reproduce the bitstream from a frozen format without sharing encoder code?
2. Does EARO beat SVD when both use the identical quantizer, factor precision, unfolding, residual coder, and actual-byte denominator?
3. Are any improvements explained entirely by dead-zone quantization, residual shrinkage, or route selection?
4. Which unfoldings and blocks improve actual rate without search overfit?
5. Can a calibrated probe avoid spending EARO compute on losing tensors?
6. Does factor-first progressive access preserve any real downstream task, and when does it mislead?
7. What exact original-byte residual would be required for a truly lossless mode?
8. Which NaN/Inf, rounding, platform, and exceptional-value rules are necessary for cross-target decode?
9. At what retention, transfer, and read horizon does the full WORM ledger become favorable?

## Section- and variant-family closure ledger

| Variant family | Disposition |
|---|---|
| Tabs 1–3: arbitrary-matrix vector pairs | Retained as correction history. Hyper-precision bijection, losslessness, square-shape gain, recursion, proofs, benchmarks, code availability, SOTA, cryptography, and energy claims are rejected or unsupported. |
| Tab 4: expanded hyper-precision/quantum/topological/program synthesis | Retained as a hazard taxonomy and possible representation-search menu only; no exactness, bound, performance, or robustness claim survives. |
| Tabs 5–7: MatrixFold EARO drafts | Mature predictor/corrector, proxy, Morton traversal, preview/refinement, WORM asymmetry, and SVD comparison obligations integrated. Repeated empirical numbers remain unverified. |
| Tab 8: lossy rate–distortion correction | Integrated as the decisive lossless-to-lossy narrowing; its numeric and SOTA claims remain unsupported. |
| Tab 9 public drafts and final RankFold paper | Canonical tensor-codec formulation integrated, including exact denominator, bounded residual coder, probe, full RD protocol, pseudocode, limitations, and non-claims. Single-operating-point table remains source-reported only. |
| RankFold Rust engineering specification | Integrated as implementation obligations: format, modules, coder, gradients, determinism, safety, tests, CLI, and extensions. It is not implemented merely because the spec is detailed. |
| NeuralFold addenda / Tabs 13–14 | Reconciled with `rankfold_neuralfold`; shared mechanisms count once and unsupported preliminary INR advantages are rejected. |
| References and conversational/editorial scaffolding | Candidate literature leads and lineage context only. Bibliographic identities and novelty require independent primary-source review. |
