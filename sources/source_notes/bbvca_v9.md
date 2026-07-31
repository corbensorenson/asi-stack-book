# Source Note: BBVCA v9

| Field | Value |
|---|---|
| Source ID | `bbvca_v9` |
| Source title | BBVCA_v9_final_public_release |
| Author | Corben Sorenson |
| Source date | February 2026 lineage; v9 public hardening pass |
| Ingestion date | 2026-06-24 |
| Fidelity audit | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1dCcqTteePCyUb66H3qJ-50uYMNDdqHFG7-qQpHSvVaA |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/bbvca_v9.txt`; raw text is not published. |
| Evidence class | Mature conceptual codec and bounded-search research program; no local Prototype A implementation or reproduced rate result |

## Claim boundary and version relationship

BBVCA v9 is the controlling public-safe formulation of the Big Bang Volumetric Compression Architecture. It deliberately hardens the earlier `bbvca_main` lineage: cosmological and universal-seed intuitions become engineering hypotheses only after a reconstruction contract, exact retained detail or repair, complete code-length accounting, bounded local verification, restricted search, literal fallback, and final serialization check are present.

The paper is not an empirical result. It supplies definitions, principles, a restricted Prototype A, a proxy-calibrated dynamic program, pseudocode, baselines, ablations, hostile tests, falsifiers, risks, and a roadmap. The repository has not implemented the codec, built its 3D mapping, run its entropy coder, measured its proxy gap, or reproduced a compression ratio. Formal labels such as “principle,” “corollary,” and “proposition” are proposed conditional arguments under explicit assumptions, not machine-checked proofs.

The paper's Big Bang metaphor is retained as author-side motivation only. Whether reality arises from a compact seed and laws is not required for the codec and supplies no cosmological, physical, or compression evidence.

## Thesis

BBVCA v9 frames compression as search for the smallest **shared-law generator plus artifact-specific seed plus exact account of everything the generator fails to explain**. Encode is Generate → Verify → Repair: propose a local lawful explanation, compare its generated block with the actual target, attach the cheapest exact restoration or split, and fall back to literal storage when the explanation is not cheaper. Decode replays a fixed law schedule and all retained detail, residuals, corrections, or literals.

The architecture's wager is domain-conditional: on native volumetric or clearly tensorized data, a small public law family may explain enough repeated local structure that seed, selection, parameters, interfaces, exact repair, mapping, and verification remain cheaper than strong simpler codecs. If repair, interfaces, mapping, search, or proxy regret dominate, the candidate loses honestly.

## Mechanisms

The complete mechanism family comprises the reconstruction contract; ontological-versus-codec universality split; public-law amortization; apex-only exclusion; two exact transition families; layerwise exactness; local generation, verification, and repair; interface-aware adaptive splitting; full cost equation; frozen additive proxy rates versus final entropy coding; proxy bootstrap, smoothing, shrinkage, refresh, and conservative anti-pruning; bounded candidate proposals; cached sufficient statistics; bottom-up dynamic programming; literal ceiling and fallback; systems layout; evaluation, hostile controls, and staged expansion.

## Reconstruction Contract

Every BBVCA claim is relative to

$$
\mathcal K=(\Omega,\mathcal M,\Delta,\mathcal A,\mathcal L,\Pi),
$$

where:

- $\Omega$ names the source domain—bytes, integers, floats, symbolic records, fields, or another exact type;
- $\mathcal M$ maps that source into the bottom volumetric field $V_0$; if it is not fixed and public, its identity and inverse cost belong in the stream;
- $\Delta$ names exact equality or a bounded distortion predicate, metric, precision domain, and tolerance;
- $\mathcal A$ fixes widths, rounding, overflow, boundary handling, update order, and arithmetic behavior;
- $\mathcal L$ declares permitted simplifications; changed observability, timing, fidelity, or precision is a changed contract;
- $\Pi$ is the public law family shared by encoder and decoder.

This tuple prevents “lossless” from floating free of its source representation and arithmetic. Exact reconstruction of $V_0$ does not imply exact reconstruction of $X$ unless $\mathcal M^{-1}$ is defined, available, and exact. Near-lossless mode must keep distortion and consumer utility separate.

## Universality, shared laws, and the apex boundary

The paper distinguishes **ontological universality** from **codec universality**. A hypothetical world generator might unfold every object under laws the world already supplies. A file codec must state which laws, decoder, and environment are genuinely shared and which information is transmitted per artifact. Public laws can amortize repeated explanatory burden across a corpus, but they are not free if they are large, unstable, bespoke, unavailable, or expensive to select and execute.

The Shared-Law Advantage is therefore conditional: moving structure into $\Pi$ helps only when amortized law and decoder cost plus per-artifact law selection/parameters remain below the repair it saves. A “public” model trained on private or changing data, a large shared neural decoder, or a per-file law library belongs in the denominator and in rights/security provenance.

The Apex-Only Exclusion Corollary is the key honesty rule. If the contracted lower state space has more admissible finite states than a strictly smaller upper representation, the upper representation alone cannot injectively encode every lower state. Universal exactness requires retained detail, exact residual/correction/literal restoration, or an equivalent transmitted structure. A small apex can explain common structure; it cannot contain arbitrary omitted degrees of freedom for free.

## Two exact transition families and layerwise exactness

For a hierarchy $V_0,\ldots,V_T$, v9 permits:

1. **Reversible factorization:** $T_k(V_k)=(V_{k+1},D_k,S_k)$ with exact inverse from upper state, retained detail, and schedule.
2. **Predictive generation plus restoration:** generate $\widetilde V_k=P_k(V_{k+1},S_k)$, then reconstruct $V_k=R_k(\widetilde V_k,E_k,C_k,L_k)$ using dense residual, sparse correction, literal fallback, or their contract-defined combination.

Mode A is the deeper long-term architecture but technically harder. Mode B is the honest Prototype A path because exactness resides visibly in repair rather than in a claim that every generator is reversible.

Layerwise Exactness requires each transition to preserve or restore its contracted target before approximation silently compounds across further levels. Deferring all error to the bottom can make attribution, debugging, and rate accounting intractable. For a lossy contract, the analogous rule is layerwise budget and residual custody: each transition records consumed distortion and remaining allowance rather than repeatedly spending the same tolerance.

## Generate, verify, repair, split, or literalize

Prototype A maps native 3D or clearly tensorized sources into a volumetric field. The 3D choice supplies face, edge, corner, and multiscale neighborhoods, but is not presumed beneficial for generic streams. A forced volume can invent false adjacency and destroy native locality; generic mapping is deferred until native domains earn the architecture credibility.

Upper cells are generator states rather than tiny literal copies. Their logical payload can contain law ID, anchor/base, directional terms, coupling or curvature, precision, and split/repair/literal flags. The initial public laws are intentionally small: constant, affine/planar, trilinear patch, and literal microblock. Sparse correction is a repair, not another law.

Each law has a small deterministic proposal set based on local statistics—mean or median for constants, least-squares and clipped/quantized variants for affine, corner and regularized fits for trilinear. This converts continuous optimization into bounded discrete candidates.

Verification evaluates the candidate, target block, exact restoration, selection and parameter bits, interface burden, and literal comparison inside a bounded local window. Its output is not a Boolean; it is a complete expected local description cost. Repair escalates through exact-as-is, sparse corrections, dense exact residual, split/recurse, and literal block. The cheapest contracted-exact option wins.

Splitting is allowed only when interior savings exceed split signaling, boundary metadata, alignment, cross-region inconsistency, and increased edge residual. Non-overlap keeps Prototype A's decisions locally separable. Overlap, larger law families, and globally coupled decisions are delayed because they reopen combinatorial search and interface attribution.

## Complete rate equation

The paper's governing denominator is

$$
B_{total}=B_{seed}+B_{law\text{-}select}+B_{param}+B_{detail}
+B_{resid}+B_{corr}+B_{split}+B_{interface}+B_{literal}
+B_{map}+B_{verify}.
$$

For a candidate explaining $n$ samples of $b$ literal bits, the local necessary inequality is $g+s+r<nb$: generator cost plus signaling/interface plus retained-detail/repair must beat literal storage. The book extends the operational denominator with decoder distribution, shared-law amortization, encode/decode compute, memory, energy, search, verification, recovery, governance, rights, and human cost when claiming system advantage.

All law IDs, parameter deltas, split flags, interface tags, details, residuals, corrections, and literal streams need real serialization. A small seed is not a small archive when repair or interfaces dominate.

## The additivity-versus-entropy problem

Prototype A wants bottom-up dynamic programming, which requires frozen additive local prices once child costs are known. A real adaptive entropy coder often makes symbol cost depend on global or preceding history. V9 exposes this tension rather than claiming the dynamic program optimizes the final bitstream.

The two-phase discipline is:

1. **Search phase:** freeze additive, stream-separable proxy prices whose contexts depend only on public local node attributes. Optimize $\widehat B_{total}$.
2. **Serialization phase:** freeze the chosen tree and law schedule, serialize actual streams with the real entropy coder, and observe $B_{final}$.
3. **Optional lagged refinement:** if a prospectively committed proxy-gap threshold is crossed, rebuild prices from observed histograms and rerun once.

The dynamic program may be exact for the frozen proxy family while being wrong for realized rate. That distinction is central evidence, not an implementation detail.

## Proxy bootstrap, calibration, and conservative pruning

Search prices must exist before the candidate stream exists. V9 bootstraps them in descending trust:

- domain-matched offline corpus priors;
- a cheap scan of the current artifact;
- padded zero-order/uniform fallback where evidence is missing or untrusted.

Sparse cells are smoothed and shrunk toward pooled parent tables. Proxy tables freeze before the DP pass. The source sketches separate prices for law selection, parameter deltas, residuals, corrections, and literals. Final contexts should stay close to search contexts so structural choices retain meaning.

Pruning uses a padded safe literal ceiling, not a raw optimistic literal estimate. A partial candidate can be discarded only when even a conservative lower bound cannot beat the safe ceiling. This matters because the optional refresh cannot resurrect branches already pruned. Tight/aggressive and conservative margins are an explicit ablation; over-pruning under miscalibrated proxies is a failure.

The refresh threshold itself must be frozen prospectively and measured per stream and decision, not chosen after observing a disappointing result. One refresh is a bounded policy, not a guarantee of convergence or global rate optimality.

## Bounded search and Prototype A algorithm

Prototype A assumes non-overlapping local support, additive proxy costs, a bounded candidate count, and $O(1)$ candidate scoring from cached statistics. Under those assumptions, bottom-up dynamic programming compares the best unsplit law/repair candidate with split cost from already stored child optima. Traceback recovers the schedule.

The Bounded Search Proposition is scoped to this restricted model family and proxy objective. It does not solve unrestricted generative compression, overlap, rich learned law selection, or global entropy contexts. “Near-linear candidate-evaluation time” also omits constants, statistics construction, serialization, memory traffic, and optional rerun unless they are measured.

The operational pipeline is:

1. map source to $V_0$;
2. build a multiscale statistics pyramid;
3. bootstrap and freeze proxy tables;
4. generate bounded law proposals per node;
5. score unsplit candidates with complete local proxy cost;
6. compare split versus unsplit bottom-up;
7. traceback the tree and schedule;
8. assemble typed streams;
9. entropy serialize and measure actual bytes;
10. optionally refresh and rerun once if the committed gap threshold fires.

Candidate scoring becomes a memory-system problem. The paper proposes level-major statistics, Morton/brick layout, compact fixed-width node records, streams separated by type/depth, branch-light kernels, and child prefetch. Cache misses and bandwidth may dominate arithmetic; this belongs in the measured encode cost.

## Prototype roadmap

- **A:** non-overlapping predictive generation plus exact restoration with small public laws and frozen additive proxy search.
- **B:** better split gates and interface models without overlap.
- **C:** controlled overlap with bounded verification and overlap order.
- **D:** genuine integer-domain reversible factorization with exact retained detail.
- **E:** richer public laws only after ablations show total savings exceed search/signaling growth.
- **F:** non-native mappings and generic/harder domains only after native volumetric success.

This sequence prevents ambitious features from obscuring whether the base generate/verify/repair wager works.

## Evidence

The source provides a strong architecture and falsification program, not a codec result. It names full bit/proxy breakdowns, runtime, memory, nodes visited/pruned/accepted, repair/literal/split/interface density, proxy gap, refresh trigger, and failure behavior as required measurements. It offers no local measured values for them.

Required baselines include straightforward multiscale residual coding, reversible lifting/transform coding, volumetric wavelet or octree methods for 3D data, strong generic compressors for generic streams, and relevant domain codecs. Required ablations cover 3D/2D organization, overlap, exact transition family, mapping, interface-aware splitting, split margin, proxy bootstrap sources, refresh, anti-pruning margin, cost components, and per-stream proxy/final mismatch.

Friendly tests—constants, smooth gradients, piecewise-smooth volumes, motifs, periodic patterns, and structured tensor blocks—ask whether the candidate can win where its hypothesis is strongest. Hostile tests—random fields, shuffled locality, heterogeneous blocks, and deliberately miscalibrated proxies—ask whether it falls back with bounded overhead rather than manufacturing a win.

Success is existence of a declared domain where generation explains substantial structure, exact restoration and interfaces remain controlled, proxy decisions survive actual serialization with modest regret, runtime is practical, and complete size beats simpler baselines. Broad usefulness narrows or fails if generator/repair/interface/mapping cost dominates, proxy choices are systematically wrong, overlap adds no value, or search is impractical.

## Failure Modes

- **Ontological-to-codec laundering:** a world-generator intuition is treated as a per-file compression result.
- **Hidden public-law payload:** a large, bespoke, unstable, private, or rights-encumbered decoder is called free shared context.
- **Apex-only fantasy:** omitted degrees of freedom are assumed to reappear without retained detail or repair.
- **Contract ambiguity:** source domain, mapping, arithmetic, liberties, or exactness target is unstated.
- **Mapping failure:** forced 3D organization destroys native locality or adds large inverse metadata.
- **Law-family Goldilocks failure:** too small yields literals; too large yields selection, parameter, and search burden.
- **Repair domination:** dense residual or correction payload overwhelms generator savings.
- **Layerwise drift:** approximation is deferred across layers and becomes untraceable or expensive to close.
- **Interface explosion:** splitting lowers interior error but raises boundary/signaling/edge residual cost.
- **Proxy optimization theater:** exact DP under $\widehat B$ is called optimal under $B_{final}$.
- **Bootstrap mismatch:** out-of-domain priors, weak scans, or unsafe zero-order prices drive wrong structural choices.
- **Irrecoverable over-pruning:** promising branches disappear before the lagged refresh can repair prices.
- **Refresh hindsight:** threshold or number of passes is chosen after results.
- **Search explosion:** overlap, rich laws, or global context invalidates restricted tractability.
- **Literal-fallback domination:** the method becomes an expensive path to ordinary storage.
- **Friendly-domain overclaim:** necessary synthetic wins are generalized beyond native structured data.
- **Memory-system neglect:** cache and bandwidth erase nominal algorithmic practicality.
- **Metaphysical evidence leak:** cosmological beauty substitutes for rate, runtime, or falsification.

## Interfaces exported to the book

The primary owner is `compact-generative-systems-and-residual-honesty`. BBVCA v9 adds a complete Reconstruction Contract, shared-law amortization, apex exclusion, two exact transition families, layerwise exactness, local interface inequality, proxy/final-rate split, bootstrap and anti-pruning discipline, and a bounded adaptive-tree algorithm. `rankfold-neuralfold-and-artifact-compression` inherits the reconstruction and final-rate boundaries as supporting discipline. `the-efficient-asi-hypothesis` uses the total-burden lesson only; BBVCA is not evidence that an ASI architecture is efficient.

No new chapter is warranted. The generate/verify/repair lane is already a major owned section in Compact Generative Systems, and v9 deepens that owner rather than creating a parallel compression chapter.

## Book Chapters Supported

- `compact-generative-systems-and-residual-honesty` — primary generate/verify/repair and residual-honesty owner.
- `rankfold-neuralfold-and-artifact-compression` — supporting reconstruction-contract, repair, interface, proxy/final-rate, and fallback discipline.
- `the-efficient-asi-hypothesis` — bounded total-cost and hidden-residual analogy; not measured efficiency.

## Claims To Add Or Update

- Teach the six-field Reconstruction Contract rather than using “exact” as an unscoped adjective.
- Separate ontological universality from a file codec's public decoder and artifact payload.
- Require exactness through retained detail or restoration; a smaller apex alone is insufficient.
- Preserve reversible factorization and predictive-plus-restoration as distinct exact transition families.
- Charge every split for interface and boundary burden and use the local $g+s+r<nb$ gate.
- Separate DP-optimal frozen proxy rate from realized serialized rate.
- Make proxy bootstrap, smoothing/shrinkage, safe literal ceilings, conservative anti-pruning, committed refresh threshold, and one optional rerun explicit.
- Preserve the restricted assumptions of the bounded-search proposition and the memory-system implementation burden.
- Treat friendly-domain wins as necessary but not sufficient and hostile graceful fallback as a success criterion.

## Open Questions

1. Can Prototype A beat lifting, octree/wavelet, multiscale residual, and domain codecs on public native 3D data after all shared and per-artifact costs?
2. How should a public law family's storage, distribution, versioning, training, rights, and amortization be allocated across artifacts?
3. Which mapping families preserve locality without overfitting the corpus or hiding mapping bits?
4. How large can proxy/final-rate regret become by stream, node type, and structural decision?
5. What safe anti-pruning margin retains real winners without erasing tractability?
6. Does one lagged refresh improve decisions enough to justify its full second-pass cost?
7. When do interface-aware splits beat a simpler fixed block or wavelet partition?
8. Can an independent decoder reproduce exact integer/fixed-point transitions and reject malformed schedules?
9. Does reversible factorization ever beat predictive-plus-restoration after retained detail and search?
10. Which formal claims can be mechanized over a finite codec model without being mistaken for corpus performance?

## Section-family closure ledger

| Paper family | Disposition |
|---|---|
| §§1–3 motivation, positioning, metaphor | Thesis and related-work role retained; cosmology/metaphysics remains motivation and non-evidence. |
| §4 universality | Ontological/codec distinction integrated; no universal codec or world-model claim. |
| §5 contract | Full six-field tuple integrated into primary chapter and retained here. |
| §§6–7 GVR/formal statement | Generate/verify/repair, hierarchy, exact/lossy conditions, two transition families, and complete objective integrated as design targets. |
| §§8–9 shared law/apex | Conditional amortization and apex exclusion integrated; “public” law cost and rights made explicit. |
| §§10–18 geometry, states, phases, repair, interfaces, cost | Native-domain boundary, tiny law family, bounded proposals, verification, repair ladder, exactness, split inequality, and denominator integrated. |
| §§19–20 proxy and search | Two-phase rate, bootstrap, smoothing, shrinkage, conservative pruning, refresh, caches, DP assumptions, and non-optimality boundary integrated. |
| §21 Prototype A | Algorithm, systems layout, reporting requirements, and early-result boundary retained as implementation obligations. |
| §22 roadmap | Staged B–F expansion retained; no later prototype is implied to exist. |
| §§23–24 evaluation, falsification, risks | Baselines, ablations, friendly/hostile tests, success/failure, proxy, mapping, law, interface, literal, and systems risks integrated. |
| §§25–26 implications/conclusion | Engineering lesson retained; cosmological truth and codec success remain independent. |
| Appendices A–E | Compact definition, formal statements, pseudocode, decoder/factorization placeholders, and glossary retained as proposed artifacts; no code or proof execution inferred. |
| References | Literature leads only until independently verified against primary sources; no novelty or SOTA conclusion is imported. |
