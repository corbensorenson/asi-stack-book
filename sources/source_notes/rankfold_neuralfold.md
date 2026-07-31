# Source Note: RankFold + NeuralFold

| Field | Value |
|---|---|
| Source ID | `rankfold_neuralfold` |
| Source title | RankFold + NeuralFold |
| Author | Corben Sorenson |
| Source date | February 2026 |
| Ingestion date | 2026-06-24 |
| Fidelity audit | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1-9wujZDobutPQbAml3H3QqYvdt9GIk55bxJiaPeSUhg |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/rankfold_neuralfold.txt`; raw text is not published. |
| Evidence class | Author-side architecture, algorithm, implementation, product, and business-plan bundle; not an empirical compression paper |

## Claim boundary and variant relationship

The local source is not one clean paper. It is a bundled design lineage containing at least three technical-paper variants, a Rust implementation architecture, product and business-plan material, and a later Rust/WASM implementation specification. The variants repeat a common codec architecture but change the product boundary:

- The early technical variants make **RankFold** the tensor backend and **NeuralFold** the functional front-end for heterogeneous artifacts. A mandatory probe-and-route stage may choose a neural representation or a conventional `RAW` path.
- One business-plan variant treats RankFold as the initial tensor-heavy wedge and NeuralFold as an optional later expansion.
- Other whitepaper, business, and implementation variants call NeuralFold integral or inseparable because the name covers inspection, routing, representation selection, and fallback—not only neural encoding.
- The later WASM specification adds a browser deployment, client-side privacy, performance modes, and licensing design. Those are implementation proposals rather than validated properties.

The book does not average these variants into a false consensus. It uses the stable architectural core: a universal **container and routing surface** with structure-dependent candidate codecs, full accounting, and deterministic fallback. Whether the product name “NeuralFold” owns every router operation is modular packaging, not a technical invariant. A minimal implementation can ship `RAW` plus tensor routing before the neural field and byte paths, while the mature architecture can retain one front-end policy surface.

“Universal” is therefore disambiguated into four claims:

1. **Container universality:** every supported artifact can be packaged because a literal or conventional-codec fallback exists.
2. **Routing universality:** every admitted input receives a typed route or refusal under declared constraints.
3. **Representation breadth:** tensors, continuous fields, and discrete bundles have proposed specialized representations.
4. **Compression-advantage universality:** explicitly not claimed. High-entropy, already-compressed, operationally expensive, or poorly modeled inputs should fall back.

The source supplies no local benchmark table, reproducible corpus result, implementation commit, superiority result, revenue result, or validated market claim. Its technical language supports design and research obligations only. Its promotional descriptions—“groundbreaking,” “superior,” “first universal,” profitable, and multi-billion-dollar opportunity—are not carried into the book as facts.

## Thesis

RankFold + NeuralFold proposes a tensor-centric WORM archival stack for heterogeneous ML and scientific artifacts. RankFold represents a matrix or tensor unfolding as a low-rank predictor plus a quantized residual and refines the predictor against a surrogate for the **actual residual coder**, rather than minimizing squared reconstruction error alone. NeuralFold proposes two front-ends: implicit functions for continuous fields and prediction-plus-lossless-residual models for discrete byte bundles. A probe estimates the complete bytes and operational constraints of candidate paths, then routes to the best qualified path or a conventional fallback.

The durable contribution is not “neural compression always wins.” It is the co-design rule that representation, transform objective, residual coder, container, router, decode contract, and evaluation denominator must agree. The proposal is specifically WORM-shaped: high encoding cost may be tolerable only when it is amortized across enough retained bytes, reads, or transfers.

## Mechanisms

The mechanism family comprises the indexed stream model, RankFold
predictor/corrector and EARO refinement, bounded residual coder,
NeuralFold-Field, NeuralFold-Byte, two-stage codec-aware training,
constraint-aware probing, typed routing and fallback, deterministic decoding,
and complete WORM accounting. The following sections preserve each component
and its independent failure boundary.

## Formal objects and stream model

The recurring container admits four stream families:

| Stream | Candidate object | Reconstruction boundary |
|---|---|---|
| `RF-TENSOR` / `RFTS` | Tensor or tensor unfolding encoded by RankFold | Bounded-error or exactness only as specified by stored quantization/residual rules |
| `NF-FIELD` / `NFFD` | Continuous signal represented by a coordinate network, metadata, tiling map, and RankFold-compressed weights | Lossy or bounded-error field reconstruction under a declared metric and decode budget |
| `NF-BYTE` / `NFBY` | Byte/bundle predictor, RankFold-compressed weights, and entropy-coded residual | Exact byte reconstruction only if the predictor, residual, bundle table, and decoder contract close |
| `RAW` / `RAW0` | Literal or conventional-codec payload | Exact according to the selected baseline codec and container checks |

The container is indexed so listing and individual extraction need not decode every stream. The engineering variants sketch magic values, length-prefixed CBOR headers/directories, self-contained stream blobs, offsets, checksums, and output-size declarations. These layouts are proposals, not a frozen or validated wire standard.

## RankFold mechanism

For a matrix $M\in\mathbb R^{m\times n}$, RankFold chooses rank $r$, factors $U\in\mathbb R^{m\times r}$ and $V\in\mathbb R^{n\times r}$, and quantization step $\Delta$:

$$
P=UV^\top,\qquad E=M-P,\qquad
E_q=\left\lfloor\frac{E}{\Delta}\right\rceil,\qquad
\hat M=P+\Delta E_q.
$$

The important accounting identity includes predictor and residual overhead:

$$
\operatorname{bytes}_{\mathrm{archive}}
=\operatorname{bytes}_{\mathrm{header}}
+\operatorname{bytes}(U)+\operatorname{bytes}(V)
+\operatorname{bytes}_{\mathrm{coded}}(E_q).
$$

The early v1 proposal stores factors in FP16 or FP32 row-major form unless factor compression is explicitly enabled and applied symmetrically to baselines. That detail prevents a baseline from being charged for overhead hidden from the candidate.

### Entropy-Aware Rank Optimization (EARO)

Truncated SVD minimizes residual energy; the intended residual coder charges for quantized zero runs, symbol magnitudes, and outliers. EARO initializes from truncated or deterministic approximate SVD and refines $U,V$ using a coder-motivated surrogate:

$$
\mathcal L(U,V)=
\sum_{i,j}\log\left(1+\frac{|E_{q,ij}|}{\delta}\right)
+\lambda(\lVert U\rVert_F^2+\lVert V\rVert_F^2).
$$

Quantization uses a straight-through estimator with $Z=(M-UV^\top)/\Delta$ and $\partial E_q/\partial Z\approx I$, so the gradient path must preserve the $1/\Delta$ scaling. The source proposes Adam refinement, with 150 steps as an illustrative v1 default rather than an established optimum.

Because this objective is only a proxy, the source requires anti-proxy-hacking diagnostics: surrogate/actual-bit correlation, factor-byte versus residual-byte breakdown, escape rate, and sensitivity to rank, quantization step, and optimization steps. A later “true bytes in the loop” option periodically runs a RankFold dry estimate during NeuralFold training. This can detect proxy drift but does not make a discrete coder differentiable or prove global rate optimality.

### Bounded residual coder

The proposed coder traverses quantized residuals row-major or, for spatial tensors, in Morton/Z order over tiles. It converts the sequence into zero-run and nonzero events:

- zero runs use Rice coding or a bucketed rANS alternative;
- each nonzero carries a sign bit;
- small magnitudes $1\ldots A_{\max}$ use a finite rANS alphabet;
- larger magnitudes emit `ESC` and encode the excess using Exp-Golomb or Elias gamma.

The bounded alphabet is a safety and scale property as well as a rate hypothesis. Morton traversal, escape coding, histogram normalization, predictor precision, and coder parameters must be stored and ablated. The logarithmic EARO term is motivated by the approximate growth of escape-magnitude code length, but actual stream bytes remain the judge.

## NeuralFold mechanisms

### NeuralFold-Field

For a continuous artifact, NeuralFold-Field fits $f_\theta:\mathbb R^d\rightarrow\mathbb R^c$ to a signal: coordinates to image color, time to audio amplitude, or spatial coordinates to a scientific field. Candidate models include sinusoidal or Fourier-feature MLPs and optional local experts. Tiling/partitioning is not cosmetic: it bounds decoding work, permits random access, and lets capacity follow local complexity. A stream needs model architecture, coordinate normalization, tile map, weights, distortion target, and decode requirements.

This path is normally lossy. Reconstructing the stored model exactly is not the same as reconstructing the original signal exactly. The book therefore preserves separate model-decode, signal-distortion, task-utility, random-access, and cost claims.

### NeuralFold-Byte

For discrete bytes $B[i]$, the source proposes a predictor $\widehat B[i]=g_\theta(i,\mathrm{context})$ and lossless residual such as $R[i]=B[i]\oplus\widehat B[i]$. Exact reconstruction depends on decoding the same prediction and combining it with the complete residual. Bundle-level training is intended to exploit shared structure across repositories, logs, or directories; a bundle table must preserve paths, offsets, and relevant metadata. If residual entropy remains high, routing must choose the conventional path.

The paper explicitly rejects “memorize arbitrary random bytes” as a compression argument. Predictor weights, bundle metadata, residual, decode compute, and failure fallback all belong in the denominator.

### Codec-aware two-stage training

NeuralFold first fits task reconstruction, then fine-tunes under a RankFold-aligned weight-rate proxy while respecting the field distortion target or byte residual budget. The stable point is bilevel co-design: a representation is useful only if it both serves the artifact contract and produces parameters/residuals the downstream coder can store economically. The optional periodic actual-byte estimate is a calibration surface. Neither stage supplies measured benefit in this repository.

## Probe, route, and abstain

The router consumes artifact type and size, tensor shapes where available, user constraints, and cheap complexity estimates such as byte entropy, tensor sparsity/distribution, or field spectral/gradient proxies. A bounded pilot may estimate:

$$
\widehat S(p)=
\widehat B_{\mathrm{metadata}}
+\widehat B_{\mathrm{RankFold(weights)}}
+\widehat B_{\mathrm{residual/raw}}
$$

subject to distortion, encode, decode, memory, privacy, and policy constraints. Technical variants suggest falling back unless a learned route beats the strongest conventional route by an “honesty margin,” with 3–5% offered only as an example. The book does not canonize that number. The margin must be calibrated prospectively against estimator error, workload shift, false-positive cost, false-negative opportunity cost, decode burden, and fallback cost.

Router evaluation therefore needs more than average size-prediction error. It needs a route confusion matrix, predicted-versus-achieved byte error, constraint violations, excess encode work on losing paths, missed wins, false neural admissions, fallback frequency, and performance under already-compressed, encrypted, adversarial, tiny, and high-entropy inputs. The strongest baseline includes a cheap type-aware conventional router; otherwise the candidate receives credit merely for refusing obviously bad paths.

## WORM economics and access-pattern boundary

The proposal is optimized for expensive one-time encoding amortized over storage duration, downloads, and reads. That is conditional economics, not a universal deployment claim. A complete comparison must report:

- encode time, peak memory, energy, and failed pilot work;
- stored bytes including indexes, manifests, weights, residuals, checksums, replicas, and retained fallback;
- transfer frequency and retained lifetime;
- decode time, memory, energy, random access, and cache effects;
- verification, corruption recovery, migration, governance, and human costs.

If artifacts are rewritten frequently, rarely read, latency-sensitive, or forced to retain a full duplicate, the amortization can vanish. “Write once, read many” is also used inconsistently in the source to describe training checkpoints as hot/write-many/read-rarely; the book treats mutable checkpoints as outside the core WORM assumption unless a specific version becomes immutable.

Product ROI formulas and vendor-price examples remain templates. No savings percentage can be inserted before matched measurements on a declared workload and horizon.

## Determinism, security, and implementation architecture

The Rust blueprint separates container/core, router, RankFold, NeuralFold, entropy coding, tensor traversal, CLI, and later WASM bindings. Its staged plan is technically useful:

1. container plus `RAW` pack/unpack/list/extract and checksums;
2. one-matrix/tensor RankFold encode/decode, residual coder, and byte accounting;
3. minimal type probe and `RF-TENSOR` versus `RAW` routing;
4. tiled `NF-FIELD` for images or grids;
5. bundle-level `NF-BYTE` with exact residual and fallback;
6. optional browser/WASM cross-target surface.

Open traits for residual coders, traversal, predictor initialization, field models, and byte predictors keep research evolution from changing the container identity silently.

Decode determinism is the hard obligation: fixed endianness, explicit rounding, stable bitstream layout, validated entropy tables, bounded output size, no undefined behavior, and declared platform arithmetic. Encode determinism can be a separate strict mode using fixed seeds, deterministic SVD, fixed ordering, and single-thread execution. Reproducing training settings is not equivalent to byte-identical encoded output.

Security obligations include offset/length bounds, per-stream and container integrity, truncation detection, bounded memory, decompression-bomb limits, malformed metadata rejection, entropy-table validation, and fail-closed parsing. Unit, integration, determinism, golden-vector, fuzz, corruption, and native-versus-WASM decode tests are all required. A checksum detects some corruption; it does not establish semantic utility, authenticity, or malicious-decoder safety.

The WASM proposal is feasible in degrees: listing, container I/O, entropy coding, and decode are more tractable than expensive NeuralFold training on large artifacts. Workers, streaming, chunking, tile limits, and fast/max-compression modes are proposed. Client-side execution can reduce upload exposure, but it does not prove regulated-environment compliance or “perfect” privacy. Browser, JavaScript glue, memory, extension, supply-chain, and side-channel risks remain.

The licensing section correctly acknowledges that local client-side enforcement is patchable. Signed offline feature tokens can deter casual forgery but do not make an untrusted client tamper-proof. License terms, private distribution, optional attestation, air-gapped operation, privacy, and user rights are product choices outside the codec claim.

## Evaluation and falsification program

The source calls for rate–distortion curves rather than one ratio. A competent campaign should sweep rank, quantization step, optimizer steps, model capacity, and decode budgets and report full component bytes. Required or implied baselines include:

- quantization plus Zstd at matched distortion;
- dead-zone quantization plus Zstd;
- truncated SVD plus the identical residual coder, isolating EARO;
- ZFP/FPZIP-class scientific codecs where applicable;
- conventional image/audio codecs and INR baselines for fields;
- Zstd/xz/7z, dictionary-trained Zstd, and non-neural predictor/residual methods for bundles;
- literal/full-artifact storage and the container’s `RAW` route.

Core ablations turn Morton traversal, escape coding, EARO refinement, codec-aware fine-tuning, tiling, and true-byte calibration on and off. The router needs false-positive and false-negative analysis. Evaluation must include total bytes, distortion, encode/decode time, memory, random-access cost, corruption, exactness where claimed, and downstream utility.

Decisive narrowing or refutation includes: SVD with the same coder matching EARO; surrogate improvement failing to reduce actual bytes; metadata/factor/residual cost erasing the win; a strong conventional codec winning; neural routes failing the honesty margin; decode cost overwhelming storage/transfer savings; cross-platform decode drift; NF-BYTE residual or bundle metadata failing exact reconstruction; NF-FIELD failing declared distortion or task probes; or WORM amortization failing on realistic access patterns.

## Failure Modes

- **Proxy hacking:** EARO or NeuralFold lowers a smooth objective while final bytes rise.
- **Denominator laundering:** weights, factors, residuals, metadata, indexes, seeds, code, fallback, or failed pilot work are omitted.
- **Universality laundering:** format support is described as compression advantage.
- **Exactness laundering:** exact decode of model weights is described as exact recovery of a lossy field.
- **Fallback theater:** a fallback is named but not executable, permissioned, timed, or included in cost.
- **Router asymmetry:** the candidate gets a sophisticated probe while the baseline is fixed or weak.
- **High-entropy overfit:** encode compute is spent learning an incompressible or already-compressed stream.
- **Random-access collapse:** a smaller stream requires whole-artifact decode.
- **Determinism drift:** arithmetic, platform, compiler, thread, dependency, or model-spec differences alter reconstruction.
- **Archive attack:** malformed offsets, entropy tables, output declarations, or model dimensions cause memory, CPU, parser, or decompression-bomb failure.
- **WORM mismatch:** savings depend on a retention/read horizon that the actual workload does not have.
- **Product-claim promotion:** market, ROI, licensing, or adoption prose is mistaken for technical evidence.

## Interfaces exported to the book

The canonical owner is `rankfold-neuralfold-and-artifact-compression`. The source strengthens that chapter with:

- a four-way universality taxonomy;
- the complete RankFold predictor/corrector and EARO loop;
- the bounded residual-coder design and anti-proxy diagnostics;
- separate field and byte representations with distinct exactness boundaries;
- probe-route-fallback calibration and route-error accounting;
- WORM amortization conditions;
- deterministic container, implementation, testing, and security obligations;
- explicit variant and promotional-claim boundaries.

Supporting ownership remains distributed. Resource Economics owns amortization and total physical cost. Security owns hostile archive and decoder risk. Rights and Provenance owns lawful transformation, retention, deletion, and licensing boundaries. Routing owns learned decision policy. Verification owns reconstruction and utility probes. The dedicated chapter remains the integration point; no new chapter is warranted.

## Section- and variant-family closure ledger

| Source family | Disposition |
|---|---|
| Early RankFold/NeuralFold technical paper | Integrated: codec, front-ends, routing, accounting, evaluation, limits; retained equations and pseudocode here. |
| Expanded “Universal WORM Archive System” paper | Integrated: bounded residual coder, EARO scaling, diagnostics, exact NF-BYTE residual, true-byte checks, hard baselines and ablations. |
| Product-aligned technical whitepaper | Integrated selectively: constraint-aware routing, honesty margin, stream/container boundary, adoption metrics; business adjectives rejected. |
| Rust architecture v1.0 | Integrated: module boundaries, deterministic decode, parsing security, tests, milestones, open traits; not treated as implemented code. |
| Business proposal and plans | Retained as author/product context only. Wedge-versus-integral contradiction preserved; ROI, market, revenue, superiority, and adoption claims remain non-claims. |
| Rust + WASM v1.1 | Integrated selectively: cross-target decode, workers/chunking, browser constraints, honest licensing limits; privacy/compliance and performance claims remain unproved. |
| Suggested future deliverables and conversational scaffolding | No manuscript claim; retained only in local raw lineage. |

## Book Chapters Supported

- `rankfold-neuralfold-and-artifact-compression` — primary owner of the codec, representation, archive, admission, and evaluation architecture.
- `compact-generative-systems-and-residual-honesty` — comparison through residual honesty, exact repair, and full-rate accounting; not independent evidence.
- `resource-economics-and-token-budgets` — conditional WORM amortization, encode/decode burden, storage/transfer horizon, and ROI-boundary accounting.
- `the-efficient-asi-hypothesis` — bounded example of architecture/resource co-design; not measured efficiency evidence.

## Evidence and non-claims

The source is unusually detailed as an architecture bundle: it includes equations, pseudocode, coder choices, file layouts, interfaces, milestones, tests, baselines, ablations, product variants, and limitations. Detail is not execution. This source does not establish:

- a working RankFold or NeuralFold implementation in this repository;
- codec correctness, exact reconstruction, deterministic cross-platform decode, or security;
- any compression ratio, rate–distortion frontier, latency, memory, energy, or random-access result;
- advantage over SVD, Zstd, scientific, media, learned, or bundle codecs;
- router calibration, false-positive/negative performance, or useful fallback;
- downstream utility or generalization across artifacts;
- WORM economic advantage, ROI, market size, revenue, licensing effectiveness, privacy, compliance, or adoption;
- novelty priority, “first universal” status, state of the art, AGI, or ASI.

The current book may cite this source for the proposal and the obligations it defines. Empirical language requires a separate result artifact and accepted evidence transition.

## Claims To Add Or Update

- Distinguish container, routing, representation, and compression-advantage
  universality; only the first three are proposed design capabilities and none
  is locally validated here.
- Teach the actual RankFold/EARO/residual-coder candidate rather than reducing
  it to the phrase “low-rank compression.”
- Separate NeuralFold-Field bounded distortion from NeuralFold-Byte exact
  prediction-plus-residual reconstruction.
- Treat route calibration, false admission, missed wins, failed pilot work,
  and strong type-aware baseline routing as part of compression performance.
- Keep WORM savings conditional on a measured retention/read/transfer horizon
  and complete operational costs.
- Preserve optional-versus-integral NeuralFold as a variant conflict; require
  the typed router and fallback behavior without canonizing a module name.
- Reject promotional superiority, novelty, ROI, market, revenue, licensing,
  privacy, compliance, and adoption language as evidence.

## Open Questions

1. Freeze a byte-accurate format and independent decoder contract before performance claims.
2. Build golden vectors for all four stream types, including corrupt, truncated, oversized, and cross-target cases.
3. Implement the same residual coder for SVD and EARO so the transform comparison is causal.
4. Calibrate surrogate-to-actual-bit behavior and report failure cases, not only correlation.
5. Use a heterogeneous public-safe corpus with tensors, fields, bundles, already-compressed and high-entropy controls, tiny inputs, rare structures, and adversarial archives.
6. Evaluate `RAW`, strong conventional/domain codecs, literal storage, and simple learned/non-neural predictors symmetrically.
7. Calibrate the routing margin from prospective route-loss data; do not inherit the illustrative 3–5% value.
8. Separate exact byte, bounded numeric, perceptual, and downstream task contracts.
9. Measure complete WORM economics across retention/read horizons and include failed probe/encode work, fallback retention, verification, migration, and governance.
10. Reproduce decode and safety behavior independently across native and WASM targets before interoperability language.
