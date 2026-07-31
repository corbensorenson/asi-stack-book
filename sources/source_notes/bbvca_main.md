# Source Note: Big Bang Volumetric Compression Architecture — nine-version lineage

| Field | Value |
|---|---|
| Source ID | `bbvca_main` |
| Source title | Big Bang Volumetric Compression Architecture |
| Ingestion date | 2026-06-24 |
| Source version / URL | Nine-tab Google Docs lineage, v1.1 through v9.0: https://docs.google.com/document/d/1tlgJismt6JaYv_jaf2XbwCX7WEqj9FJ0WvEtbHYS_-E |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/bbvca_main.txt`; 58,663 words across nine versioned tabs; raw text is not published. |

## Claim boundary and source topology

This record is a **correction lineage**, not nine independent sources. It contains v1.1, v1.2, v2.0, v3.0, v4.0, v6.0, v7.0, v8.0, and v9.0. Later versions repeatedly narrow, repair, or operationalize earlier language. The v9 tab is substantively the same paper as the separately cached `bbvca_v9` source, with mostly formatting differences, so its ideas and section closure count once.

The lineage contains no local codec implementation, emitted bitstream, independent decoder, corpus, benchmark receipt, runtime trace, memory profile, or reproduced compression result. “Public release” is an editorial version label, not evidence. Formal names such as Principle, Corollary, Bound, or Proposition are proposed arguments under assumptions; they are not machine-checked proofs of codec performance.

The later correction controls whenever versions conflict. In particular: the apex is not the complete code; 3D and overlap are hypotheses rather than automatic advantages; weighted blending is not a reversible transform; lossless exactness needs retained detail or restoration; verification metadata does not create compression; encoder search is bounded only in a restricted non-overlapping additive regime; and search-time proxy optimality is not final entropy-code optimality.

## Thesis

BBVCA treats compression as recovery of a compact lawful process rather than only shortening a symbol stream. The source is mapped into a multiscale field. Upper states propose lower structure under a small shared law family. The encoder searches, verifies each proposal against the true target, and retains or repairs every degree of freedom the generator does not explain. The decoder performs finite deterministic replay. A representation wins only when the entire executable description—including mapping, laws, parameters, schedules, interfaces, exact detail, residuals, corrections, literals, verification, decoder, and practical burdens—is better than strong simpler alternatives under a declared reconstruction contract.

The distinctive 3D wager is domain-conditional. Face, edge, corner, and volumetric neighborhoods may expose useful local structure in scientific volumes, simulation fields, tensor archives, and other natively spatial sources. Folding an arbitrary byte stream into a cube does not create meaningful geometry. A locality-destroying or metadata-heavy mapping can erase the hierarchy's benefit.

The mature one-line architecture is: **Generate → Verify → Repair on encode; generate → replay exact restoration on decode.** Its philosophical “world-generator” language is an intuition about shared laws and sparse surprise, not evidence about cosmology or a route around information theory.

## Version-by-version correction history

| Version | Contribution retained | Correction or boundary introduced |
|---|---|---|
| v1.1 | Apex-seeded 3D cascade; generator-state voxels; encoder search; adaptive precision; sparse correction, splitting, literal fallback; Merkle-style integrity aid. | Concept draft only. Overlap and weighted resolution are sketches, not exact semantics. Apex minimization is an aspiration. |
| v1.2 | Two sanctioned lossless routes; explicit bit-budget discipline; complexity limits; strongest-fit domains; required ablations and falsifiers. | Exactness must come from reversible integer-domain transformation or prediction plus exact residual. Hashing is orthogonal overhead. |
| v2.0 | Formal layer model; total-rate objective; fixed-point decoder discipline; explicit baselines, metrics, success, and falsification. | Recasts BBVCA as an adaptive multiscale generative predictor with residual/fallback, not a wholly alien codec or proven advantage. |
| v3.0 | Public positioning; logical rather than mandatory fixed-width generator payload; overlap made optional; best-fit/weakest-fit scope; practical bottlenecks. | Every omitted degree of freedom must be preserved or restored. “Public release” does not mean competitive or implemented. |
| v4.0 | Reconstruction Contract; apex-only exclusion; Local Verification Bound; Interface Cost Principle; semantic-versus-integrity verification; exact factorization/restoration formalization. | A smaller apex alone cannot universally recover a larger contracted state space. Split boundaries and mapping choice are real rate terms. |
| v6.0 | Generate-Verify-Repair doctrine; ontological-versus-codec universality; Shared-Law Advantage; Layerwise Exactness; decode as deterministic recipe replay. | Cosmological metaphor is separated from the codec. Public laws can amortize only if their implementation, distribution, and use are actually shared. |
| v7.0 | Bounded Search Doctrine; tiny proposal family; cached sufficient statistics; literal ceiling; monotone pruning; split gating; adaptive-tree dynamic program. | Tractability applies only to a restricted non-overlapping, locally additive proxy family. It is not unrestricted program search or global optimality. |
| v8.0 | Two-Phase Rate Discipline; frozen search-time proxy tables; final entropy-coded serialization; irregular adaptive-tree clarification; memory-layout doctrine; proxy/final gap measurement. | A dynamic program can optimize its proxy while choosing the wrong final bitstream. Search and serialization must remain separate measured phases. |
| v9.0 | Proxy Bootstrap and Calibration Doctrine; corpus/scan/zero-order initialization; smoothing and shrinkage; conservative anti-pruning; concrete refresh; simple final coder. | A bad first-pass proxy can irreversibly prune good branches. Margins and prospective refresh rules must be committed before outcomes. |

This history is itself useful: each revision converts a metaphorical degree of freedom into an explicit contract field, bitstream term, algorithmic assumption, or failure condition. The book should teach that architectural maturation pattern, not cite nine versions as cumulative empirical support.

## Mechanisms

### Reconstruction Contract and public environment

The mature contract is

\[
\mathcal K=(\Omega,M,\Delta,A,\mathcal L,\Pi),
\]

where $\Omega$ declares the source domain, $M$ the source-to-field mapping, $\Delta$ the exact or bounded reconstruction criterion, $A$ arithmetic semantics, $\mathcal L$ admissible liberties, and $\Pi$ the public law family. Integer widths, fixed-point scales, rounding, overflow, boundaries, update order, and inverse mapping are part of correctness. Any relaxed fidelity, observability, temporal behavior, or precision is a contract change.

$\Pi$ may contain legal generator modes, neighborhoods, entropy models, split semantics, reversible primitives, and deterministic resolve rules. Shared-law amortization is conditional: code size, implementation, distribution, versioning, hardware assumptions, rights, maintenance, and decoder availability still need an allocation rule. A giant artifact-specific program merely moved into an unpriced “public” environment is not a compression gain.

### Hierarchy, mapping, and generator state

The encoder maps artifact $X$ into $V_0=M(X)$ and searches a hierarchy $V_0,\ldots,V_T$. Power-of-two cubic layers provide simple indexing and a clean first implementation, not a proof of optimal geometry. Candidate mappings progress from native volume and fixed public byte mapping to small locality-preserving or typed families. Adaptive semantic mappings belong in later experiments because mapping choice and metadata can hide model cost.

An upper cell is a generator state, not necessarily a scalar. Its logical fields may include law ID, anchor/base, directional terms, coupling or curvature, precision code, and split/repair/literal flags. Inactive fields should not pay a maximal fixed struct width; actual entropy-coded payload matters. The mature Prototype A law family is deliberately tiny: constant, affine/planar, trilinear patch, and literal microblock. Earlier neighbor-coupled, periodic, and residual-carrying modes survive as later candidates or repair concepts, not baseline assumptions.

The “Goldilocks” problem is structural. Too weak a law family leaves dense residuals. Too rich a family inflates decoder, search, selection, parameter, validation, rights, and maintenance cost. Law expansion therefore requires ablation against the smaller family and full amortization accounting.

### Overlap and local causality

Early versions make overlapping cones of influence central to the 3D intuition. Later versions correctly demote overlap from premise to experimental upgrade. Multiple upper voxels may share explanatory burden, but overlap also expands support, creates accumulation-order and rounding sensitivity, couples decisions across partitions, increases candidate count, and complicates interface attribution.

Prototype A therefore disables overlap. A later controlled-overlap mode must cap support and overlap order, specify arithmetic and tie resolution exactly, remain jointly verifiable inside a bounded window, and beat non-overlap after all signaling, repair, search, memory, and decoder costs. Weighted sums followed by quantization are predictive operations; they are not evidence of reversible factorization.

### Two exact transition families

BBVCA sanctions two distinct routes:

1. **Reversible factorization.** A transform maps $V_k$ to coarse $V_{k+1}$, retained detail $D_k$, and schedule $H_k$, and a fully specified inverse reconstructs $V_k$. Credibility requires an integer/fixed-point domain, exact update order, boundaries, overflow, detail layout, and inverse schedule.
2. **Predictive generation plus exact restoration.** Upper state and schedule generate $\widetilde V_k$; exact residuals, sparse corrections, dense restoration, splitting, or literals recover $V_k$. This is universal because literal fallback closes representability, not because the predictor is universal.

The Apex-Only Exclusion Corollary is a finite-state counting boundary: when the contracted lower state space is larger than the upper representation, the apex alone cannot injectively encode every lower state. Omitted degrees of freedom must appear as retained detail or equivalent transmitted restoration.

The Layerwise Exactness Principle restores or preserves missing information at the layer where it is dropped. It prevents unbounded approximation drift, localizes attribution, and makes debugging and verification meaningful. Near-lossless operation is a different $\Delta$, not a sloppy lossless mode.

### Generate, verify, repair, and commit

For a bounded region the encoder:

1. proposes a law and quantized parameters from a tiny deterministic set;
2. generates a candidate lower region;
3. compares it to the true target in a bounded decision window;
4. chooses exact-as-is, sparse correction, dense residual, split/recurse, or literal storage;
5. prices the complete option and commits the cheapest contracted-exact route.

The decoder never has the target and cannot repeat encoder-side semantic verification. It decodes the chosen law schedule, regenerates predictions, and replays exact retained/restoration streams. Calling this “concept instantiation” is useful only as a description of deterministic execution; it does not establish semantic understanding.

The Local Verification Bound requires the responsible upper context, generated lower region, actual target, and repair path to be jointly evaluable within a bounded region. Candidates that exceed it must simplify, split, or fall back. This is simultaneously a verification, search, memory, and interface invariant.

### Semantic exactness versus integrity verification

The lineage distinguishes two meanings of verification that should not be conflated:

- **semantic/reconstruction verification** is the encoder's comparison of the generated candidate with the contracted target and is essential to exact admission;
- **integrity verification** uses block hashes, layer roots, global digests, or debug traces to detect corruption or implementation divergence.

Merkle-style hashes can localize damage, but they add bytes and operations and do not improve compression ratio. Development, production, and benchmark profiles may vary integrity metadata; none may silently disable the reconstruction criterion. A “benchmark mode” that drops hashes measures pure codec rate only if independent decode equality is still checked outside the bitstream.

### Full rate and interface accounting

The mature file objective includes

\[
B_{total}=B_{seed}+B_{law\text{-}select}+B_{param}+B_{detail}+B_{resid}+B_{corr}+B_{split}+B_{interface}+B_{literal}+B_{map}+B_{verify}.
\]

For a candidate explaining $n$ samples of $b$ literal bits, a necessary local test is $g+s+r<nb$, where generator burden $g$, signaling/interface $s$, and repair/retained detail $r$ all count. It is necessary, not sufficient: entropy contexts, headers, alignment, indexes, padding, decoder distribution, shared-law allocation, compute, memory, energy, recovery, governance, rights, and human cost can reverse the system-level result.

Splitting is accepted only when interior savings exceed split signaling, boundary metadata, repeated context, alignment, cross-region coupling, and edge residual. A low prediction error with high interface surface is a loss. Literal fallback gives every region a valid ceiling and bounds hostile-data failure, but its flags, lengths, and container overhead still count.

The lineage also names the worst-active-bottleneck view: rate, encode time, decode time, working memory, mapping, and interface complexity can trade places. A richer generator may reduce residual bits but make search or decode impractical. No single metric is a sufficient success claim.

### Bounded search and restricted optimality

Unrestricted continuous laws, overlap, arbitrary partitioning, and global entropy contexts create combinatorial search. v7 defines a deliberately narrower Prototype A:

- non-overlapping local regions;
- a small public law family;
- bounded quantized proposals from closed-form local statistics;
- cached sufficient statistics for constant-time candidate scores;
- maximum candidates, support, split depth, beam width, and per-block budget;
- a padded literal ceiling for pruning;
- split gating by heterogeneity or expected margin;
- mandatory fallback when budget expires.

Under additive local proxy costs, the adaptive-tree dynamic program compares each node's best unsplit option against the sum of already solved children plus split/interface cost. Traceback recovers the schedule. This can be exact **inside the restricted proxy family**. It does not prove a global optimum over BBVCA, programs, mappings, overlaps, or final stateful entropy coding. Claims of “near-linear” work exclude statistics construction, constants, memory traffic, serialization, and any refresh pass unless those are measured.

### Search-time proxy versus final serialization

Stateful entropy coding conflicts with the additivity required by the dynamic program. v8–v9 therefore separate phases:

1. freeze stream-separable price tables keyed only by public local contexts such as depth, law, parent law, and coarse heterogeneity;
2. optimize additive proxy length $\widehat B_{total}$;
3. freeze the selected tree and schedule, serialize every actual stream with a deliberately simple coder, and measure $B_{final}$;
4. if a prospectively declared proxy-gap threshold fires, refresh from observed histograms and rerun at most once.

First-pass tables can come from domain-matched offline priors, a cheap scan of the artifact, or a pessimistic padded zero-order model. Sparse cells require smoothing and shrinkage toward pooled parents. The safe literal ceiling includes a margin, and a partial candidate is pruned only when it cannot beat that padded bound. This anti-pruning rule matters because a later refresh cannot resurrect a discarded branch.

The report must expose proxy error by stream, structural regret, refresh state, nodes visited/pruned, split/literal/repair density, and final component bytes. Proxy optimality and final rate optimality are different claims.

### Systems layout and implementation stages

The first implementation is a memory system as much as a mathematical search. The later versions propose a statistics pyramid, level-major or Morton/brick ordering, compact node records, separate streams by type/depth, branch-light scoring, and child prefetch. Cache misses and bandwidth may dominate arithmetic.

The staged program is intentionally asymmetric:

- **A:** native integer volume or fixed public mapping; non-overlap; 2×2×2 hierarchy; constant/affine/trilinear/literal laws; predictive exact restoration; bounded split tree; simple entropy coder; full receipts.
- **B:** improved split gates and explicit interface models.
- **C:** controlled overlap under bounded support and verification.
- **D:** genuine reversible integer-domain factorization.
- **E:** richer public laws only after smaller-family ablations.
- **F:** non-native mappings and harder domains.

Apex minimization comes after exactness, rate viability, and practicality. A tiny root with a large hidden hierarchy is not a win.

## Evidence

The source supplies an unusually complete conceptual progression, formal object family, pseudocode sketches, implementation stages, baselines, ablations, friendly/hostile tests, and falsification criteria. It is useful as design rationale and as a worked example of correcting an architecture under pressure.

It supplies **no empirical evidence** that BBVCA compresses any corpus, that 3D beats 1D/2D, that overlap helps, that bounded proposals find useful schedules, that proxy rates are calibrated, that the dynamic program is fast in practice, that exact decode is implemented, or that the method improves downstream utility. The same-author revisions are not replications. The tab-9 duplicate of `bbvca_v9` is not a second source.

Required evidence includes strong generic and domain codecs; simple multiscale residual, reversible lifting/transform, volumetric wavelet, and octree baselines; 3D-versus-2D and mapping controls; non-overlap/overlap; predictive/restoration versus reversible factorization; no-split/naive/interface-aware split; law-family size; proposal count; proxy initialization; smoothing; anti-pruning margin; refresh; entropy model; and full cost-component ablations.

Friendly tests—constant fields, gradients, piecewise smooth volumes, motifs, periodic fields—ask whether the architecture can win inside its hypothesis class. Hostile tests—random, shuffled-locality, heterogeneous, adversarial boundary patterns, and proxy miscalibration—ask whether it falls back with bounded overhead. Success is a declared domain where exact restoration and interfaces remain controlled, proxy decisions survive serialization, runtime/memory are practical, and complete cost beats strong baselines. Repeated repair domination, mapping loss, interface explosion, proxy regret, or impractical search narrows or falsifies broader claims.

## Failure Modes

- **Metaphor laundering:** cosmological or causal language is treated as codec evidence.
- **Duplicate-support inflation:** nine revisions or the separately cached v9 are counted as independent confirmation.
- **Apex-only illusion:** root size is reported while detail, schedule, residual, decoder, or public-law cost is hidden.
- **Mapping laundering:** an adaptive or semantic layout stores unpriced information or destroys locality.
- **3D essentialism:** richer adjacency is assumed to help without 1D/2D and shuffled controls.
- **Overlap optimism:** better local fit hides arithmetic, search, boundary, and restoration cost.
- **False reversibility:** weighted blending, quantization, or underspecified floating behavior is called invertible.
- **Layer drift:** approximations propagate across scales before exactness is restored.
- **Generator overcost:** law selection and parameters cost more than the samples they explain.
- **Public-law smuggling:** a giant decoder or learned prior is declared free without amortization, version, rights, or distribution accounting.
- **Interface explosion:** aggressive splitting lowers interior error while raising total bits.
- **Verification conflation:** hashes are confused with semantic exactness, or benchmark mode silently weakens correctness.
- **Search explosion:** overlap, rich laws, mappings, or global coupling invalidate the restricted dynamic program.
- **Proxy overconfidence:** an inaccurate frozen rate model prunes the eventual best schedule.
- **Proxy/final substitution:** an optimum under $\widehat B$ is reported as an actual compression result.
- **Memory blindness:** nominal arithmetic ignores statistics construction, cache misses, bandwidth, allocation, and serialization.
- **Literal domination:** the format is universal only because it mostly stores input plus overhead.
- **Friendly-only evaluation:** structured synthetic wins are generalized to broad data.
- **Apex-first roadmap:** root minimization precedes exactness, rate closure, and usable implementation.

## Cross-paper relationships and tensions

- `bbvca_v9` is the canonical mature endpoint of this same lineage. Its final tab duplicates that source and must count once.
- `cgs` generalizes the seed/rule/state/residual/verification/governance pattern beyond codecs. BBVCA adds a concrete bounded artifact-compression candidate but does not validate CGS utility.
- `rankfold_neuralfold` and `rankfold_compressor` are neighboring artifact-codec proposals. They share residual honesty, finite coding, dry-run rejection, and progressive access questions, but use different predictor/representation families.
- `precision_contract` generalizes contract-relative functional preservation and complete executable-description cost from artifacts to neural computation. A BBVCA byte-exact claim and a behavior-preserving precision claim are different contracts.
- Transform, wavelet, octree, fractal, analysis-by-synthesis, procedural, and generic compressors are necessary comparators, not rhetorical ancestors that prove novelty.

## Book Chapters Supported

- `compact-generative-systems-and-residual-honesty` is the primary owner. The lineage contributes architectural maturation, 3D/mapping/overlap boundaries, semantic-versus-integrity verification, complete rate and bottleneck accounting, and the rule that apex minimization follows exactness and viability.
- `rankfold-neuralfold-and-artifact-compression` may inherit the finite-description, reconstruction-contract, exactness, progressive-access, and fallback boundaries as supporting discipline; BBVCA supplies no RankFold result.
- `the-efficient-asi-hypothesis` may use the complete-burden lesson only. A codec proposal is not evidence of ASI efficiency.

No new chapter is warranted. The mature mechanisms already belong to the compact-generative and artifact-compression spine; the version history is best presented as a compact architecture-correction case study.

## Claims To Add Or Update

- Treat same-author version history as one correction lineage, with later boundaries controlling earlier rhetoric.
- Distinguish semantic reconstruction checks from optional integrity hashes.
- Make 3D, mapping, overlap, and public-law size hypotheses that require direct ablations.
- Preserve the logical generator payload while charging actual coded fields and shared decoder cost.
- Keep exact transition families separate: reversible factorization is not predictive blending.
- Require apex minimization only after correctness, final rate, and practical bottleneck gates.
- Record proxy-optimal, serialized-optimal, and system-useful outcomes as distinct evidence states.

## Open Questions

1. Which native volumetric corpora and domain codecs form the first fair test bed?
2. What mapping family is small enough to be honest yet strong enough to preserve locality?
3. Can the smallest law family beat residual and transform baselines before overlap?
4. What independent decoder and cross-platform arithmetic suite establishes exact replay?
5. How should public-law implementation, distribution, versioning, rights, and amortization be charged?
6. Which integrity profile provides useful localization without distorting codec-rate comparisons?
7. How large can proxy error be before anti-pruning margins destroy useful pruning?
8. Does one committed refresh improve final rate enough to justify its full second-pass cost?
9. Can controlled overlap ever repay coupled search and interfaces after non-overlap is strong?
10. What evidence would justify moving from a narrow native-volume result to any broader scope?

## Section-family closure ledger

| Source family | Disposition | Boundary |
|---|---|---|
| Tab 1 / v1.1: abstract, §§1–3 | Core metaphor, 3D hypothesis, local-codec stack, mapping, and hierarchy retained in this note and canonical chapter. | Early apex and overlap language is controlled by later finite-description and ablation rules. |
| Tab 1 / v1.1: §§4–10, Appendix C | Generator schema, modes, expansion, search, precision, repair, fallback, hashing, encode/decode sketch retained. | Pseudocode is illustrative; weighted fixed-point generation is not implemented or reversible. |
| Tab 1 / v1.1: §§11–16, Appendices A–B | Exact/near-lossless split, risks, staged prototypes, philosophical framing retained. | “Advantages” are intended properties, not demonstrated results. |
| Tab 2 / v1.2 | Exact-transition split, complexity discipline, bit budget, fit domains, invertibility risks, ablations, falsifiers, dual pseudocode retained. | Later v4/v6 formalism supersedes underspecified lossless language. |
| Tab 3 / v2.0: §§1–10 | Related-work positioning, formal hierarchy, logical generator, exact semantics, verification, and total cost retained. | Novelty and competitiveness require independent comparison and data. |
| Tab 3 / v2.0: §§11–16, appendices | Metrics, baselines, ablations, success/falsification, A–E roadmap, dual exact modes retained. | No experiment or implementation follows from the plan. |
| Tab 4 / v3.0 | Public non-claim table, best/weak domains, overlap demotion, logical payload, practical failure modes, decisive tests retained. | “Public Release” has no support effect. |
| Tab 5 / v4.0: contract and formal core | Five-field contract, apex exclusion, exact modes, mapping policy, bounded support, resolve semantics retained. | v6 adds the public-law field; counting proof is a conditional boundary, not a rate result. |
| Tab 5 / v4.0: verification, interfaces, cost, bottlenecks | Local Verification Bound, semantic/integrity split, interface objective, local inequality, worst bottleneck retained. | Hashes and optional debug metadata never count as compression gain. |
| Tab 5 / v4.0: evaluation, roadmap, appendices | Friendly/hostile tests, strong baselines, staged prototype, formal statements and pseudocode retained. | Aspirational artifact family only. |
| Tab 6 / v6.0: §§1–8 | GVR doctrine, world-generator translation, ontology/codec split, six-field contract, shared-law principle, apex exclusion retained. | Cosmology and public-law power are not empirical support. |
| Tab 6 / v6.0: §§9–20 | 3D scope, generator states, generate/verify/repair phases, layerwise exactness, interfaces, full cost, entropy modeling, encoder/decoder discipline retained. | Decode replay is deterministic execution, not demonstrated understanding. |
| Tab 6 / v6.0: §§21–26, appendices | Prototype A, later stages, evaluation, failure signatures, philosophical limit, formal statements, pseudocode, glossary retained. | No prototype was run. |
| Tab 7 / v7.0 | Bounded proposals, statistics, literal ceiling, monotone pruning, split gating, adaptive-tree DP, restricted proposition, systems/evaluation updates retained. | Optimality and tractability apply only to the frozen additive non-overlap proxy family. |
| Tab 8 / v8.0 | Two-phase rate, proxy contexts, irregular-tree clarification, systems layout, proxy-gap and split-sensitivity reporting retained. | Proxy objective is not final serialized objective. |
| Tab 9 / v9.0 | Bootstrap sources, smoothing/shrinkage, pessimistic fallback, conservative anti-pruning, refresh threshold, simple final model retained through `bbvca_v9` deep audit. | Duplicate of separately cached v9; counted once and adds no independent evidence. |

**Closure result:** all nine version tabs, their numbered section families, formal statements, roadmaps, pseudocode, glossary material, and cross-version contradictions have an explicit disposition. The lineage remains an architecture argument and research program. No codec, bitstream, decoder, exactness, compression ratio, mapping advantage, 3D advantage, overlap advantage, proxy calibration, runtime, memory, utility, safety, deployment, support, novelty, SOTA, AGI, or ASI result is promoted.
