Big Bang Volumetric Compression Architecture
Public Release v9.0
A White Paper on Generate-Verify-Repair Compression from Seeded Local Laws, Bounded Search, and Two-Phase Rate Discipline
Author: Corben Sorenson
AI Research Collaborator: GPT-5.4 Pro
Status: Public Research White Paper
Version: 9.0
________________


Public Release Note
Version 9 is the final hardening pass. Version 8 solved the deepest rate-accounting tension by separating search-time proxy optimization from final entropy-coded serialization. Version 9 answers the next question directly:
How can Prototype A score B_law-select and B_param honestly enough during search to preserve dynamic programming, even though the final entropy coder has not yet run?
The answer is a Two-Phase Rate Discipline plus an explicit Proxy Bootstrap and Calibration Doctrine.
During the search phase, Prototype A does not pretend to know the final adaptive code length symbol by symbol. Instead it optimizes a frozen additive proxy objective built from stream-separable local price tables. These proxy prices are keyed only by public node attributes such as depth, law class, parent law, and coarse heterogeneity class. That makes local costs additive and preserves bottom-up dynamic programming.
After the partition and law schedule are chosen, the encoder performs a separate final serialization phase with the real entropy coder. If the realized rate differs materially from the proxy prediction, the encoder may refresh the proxy tables from the observed stream histograms and rerun the dynamic program once. Prototype A therefore becomes a disciplined two-pass or at most few-pass encoder, not an uncontrolled global search.
Version 9 adds six final refinements.
First, it keeps the Two-Phase Rate Discipline and makes the first-pass search objective even more concrete: a frozen additive proxy model, then final serialization with a deliberately simple per-stream coder.
Second, it introduces a full Proxy Bootstrap and Calibration Doctrine for Prototype A: initialize proxy prices from offline corpus priors, a cheap artifact scan, or a deliberately pessimistic zero-order fallback when no trustworthy prior exists.
Third, it defines explicit Search-Time Proxy Prices for B_law-select and B_param, including the exact public contexts they may depend on without breaking additivity, and it specifies conservative shrinkage and smoothing rules for those tables.
Fourth, it adds a Conservative Anti-Pruning Discipline: literal ceilings and candidate pruning are padded by a safety margin so badly calibrated first-pass proxies do not permanently eliminate promising branches.
Fifth, it commits Prototype A to a concrete proxy-gap refresh threshold and a deliberately simple final entropy model so that the relationship between search-time proxy rates and realized serialized rates becomes measurable rather than rhetorical.
Sixth, it preserves the strongest safe version of the paper’s philosophical intuition while making the implementation story less mystical than ever: a world-like generator only matters if its shared laws are public, its local claims are directly verifiable, its interfaces are paid for, its proxy tables can be bootstrapped honestly, and its rate accounting survives final serialization.
Abstract
Big Bang Volumetric Compression Architecture (BBVCA) is a contract-relative compression framework that treats data as the output of a hidden lawful generative process and reframes compression as the search for the smallest exact reconstruction program under a bounded local law family. A source artifact is first mapped into a bottom volumetric field. The encoder then seeks progressively smaller upper layers whose cells act as generator-state voxels: compact local descriptors that induce lower-layer structure through deterministic rules. Exactness is achieved not by pretending the generator is perfect, but by pairing it with verification and repair machinery: retained detail, exact residuals, sparse corrections, split signaling, interface accounting, and literal fallback.
The core doctrine of the architecture is:
Encode by Generate -> Verify -> Repair. Decode by Generate -> Replay Exact Restoration.
Version 9 contributes ten formal ideas. The first is the Reconstruction Contract, which defines what must be reproduced, with what arithmetic semantics, and under what allowed liberties. The second is the Shared-Law Advantage Principle, which states that compression improves when explanatory burden moves from per-artifact payload into a stable public law family. The third is the Apex-Only Exclusion Corollary, which rules out universal lossless recovery of arbitrary larger data from a strictly smaller upper representation alone. The fourth is the Local Verification Bound, which requires candidate transitions to remain jointly checkable inside bounded local interaction regions. The fifth is the Layerwise Exactness Principle, which prefers exact restoration or retained detail at each scale rather than allowing uncontrolled approximation drift across many scales. The sixth is the Interface Cost Principle, which treats partition boundaries as first-class rate terms. The seventh is the Bounded Search Proposition for Prototype A, which shows that under a restricted non-overlapping additive regime the encoder search can be reduced from an intractable global combinatorial problem to a bottom-up dynamic program over an adaptive multiscale tree. The eighth is the Two-Phase Rate Discipline, which separates search-time scoring under a frozen additive proxy model from final serialization under the real entropy coder. The ninth is the Proxy-Rate Principle, which specifies how B_law-select and B_param may be approximated during search without breaking the dynamic-programming property. The tenth is the Proxy Bootstrap and Calibration Doctrine, which specifies how those search-time tables are initialized, smoothed, and refreshed without pretending to know the final code length in advance.
Version 9 also clarifies a strong philosophical claim. If reality itself arose from a compact primordial seed and lawful unfolding, then the universe may be viewed as an ontologically general decompressor. BBVCA does not assume that cosmological thesis as physics. It translates the engineering lesson instead: use compact seeds, stable public laws, bounded local generation, direct verification, sparse repair, and explicit accounting for whatever is not already shared.
The research question is therefore precise: can a shared law family plus compact artifact-specific seeds and exact repair streams outperform simpler codecs on data with enough multiscale locality or generative structure, while keeping encoder search computationally disciplined and search-time rate estimates honest enough to survive final serialization? This paper develops the conceptual architecture in full, states its limits, identifies its bottlenecks, and lays out a concrete path to implementation.
1. Executive Summary
BBVCA begins from a strong shift in viewpoint.
Classical compression is often described as symbol shortening: transform the source, predict the next symbol, remove redundancy, and entropy-code the result. BBVCA instead asks a deeper question:
What seed and lawful process could have generated this artifact, and what is the smallest exact proof that this generated artifact is the one we meant?
That reframing immediately turns compression into a two-part problem.
1. Discover the smallest lawful explanation.
2. Store the smallest exact remainder where the explanation is not sufficient.
This leads to an asymmetric codec.
1.1 Encode
The encoder is allowed to search. For each region and scale, it:
1. proposes a compact local generator state,
2. expands it under a bounded public law family,
3. verifies the generated result against the true target,
4. repairs the mismatch using the cheapest exact mechanism,
5. decides whether to keep the region whole or split it,
6. recurses only where rate justifies further structure.
1.2 Decode
The decoder is not allowed to search. It simply:
1. replays the seed and law schedule,
2. generates the same local predictions,
3. applies the stored exact restoration streams,
4. reconstructs the bottom volumetric field,
5. unmapps that field back into the source artifact.
1.3 The Big Bang lesson, translated safely
The architecture is inspired by five structural lessons extracted from the strongest form of the “big bang” intuition.
* Compact beginning: a small initial condition can anchor a large unfolding.
* Shared laws: the strongest compressors move explanatory burden into public rules shared across many instances.
* Local causality: large structure should emerge from bounded local interactions, not arbitrary global rewrites.
* Multiscale emergence: coarse structure should appear first and fine detail later.
* Sparse surprise: the file should mainly pay for what the lawful generator fails to explain.
1.4 What Version 9 adds
Version 9 keeps the philosophical inspiration but hardens the implementation story one last step.
* It retains the reconstruction contract and the distinction between ontological universality and codec universality.
* It keeps the full rate budget, layerwise exactness, and local verification at the center of the architecture.
* It preserves the bounded, non-overlapping, additive Prototype A search regime from Version 7.
* It keeps the Two-Phase Rate Discipline that separates search-time proxy rates from final serialized rates.
* It adds an explicit Proxy Bootstrap and Calibration Doctrine for initializing B_hat_law-select and B_hat_param before the first search pass.
* It commits the first prototype to a deliberately simple final entropy model and a concrete proxy-gap refresh threshold.
* It clarifies that bottom-up dynamic programming still applies on irregular adaptive trees produced by split gating.
* It adds a conservative anti-pruning rule so first-pass proxy miscalibration does not quietly delete promising schedules.
* It strengthens the systems doctrine so the first implementation remains practical when memory bandwidth becomes the limiting resource.
1.5 One-line thesis
Compression is the search for the smallest shared-law world-generator plus the smallest exact proof that the generated world is the artifact we meant.
________________


2. Positioning and Related Work
BBVCA is not a wholly alien category. It sits at the intersection of several existing traditions.
2.1 Information theory and description length
At the highest level, BBVCA belongs to the lineage of information-theoretic and description-length thinking: a model is only useful when the combined cost of the model and the leftover data is smaller than the data alone. In that sense BBVCA is an explicitly structured minimum-description-length architecture, not an escape from it.
2.2 Multiresolution and transform coding
Wavelets, pyramids, lifting schemes, octrees, and related multiscale codecs already treat data as structure distributed across scales. BBVCA is closest to these traditions. Its main difference is that it interprets upper layers as local generators or coarse factors with explicit repair channels, rather than only as coefficients in a fixed transform basis.
2.3 Fractal and self-similarity coding
Fractal image compression and related self-similarity methods also sought compact generative descriptions. BBVCA shares that ambition but avoids the strongest historical weakness of fractal coding by making repair, literals, and explicit cost accounting first-class rather than rhetorical afterthoughts.
2.4 Analysis-by-synthesis and model-based coding
BBVCA strongly aligns with analysis-by-synthesis. The encoder searches; the decoder replays. The architecture differs mainly in its insistence on a local 3D geometry, explicit interface cost, and a generate-verify-repair doctrine.
2.5 Procedural and generative modeling
Procedural graphics, grammar-based methods, tensor factorizations, and learned compression priors all exploit the same economic truth: when a stable generator is shared publicly, per-instance descriptions can shrink. Modern learned compression with hyperpriors expresses this in a different idiom: side information and a shared prior reduce the uncertainty that must be paid for per artifact. BBVCA makes that truth explicit and exact under a codec contract.
2.6 Why BBVCA still matters
The novelty claim is not that BBVCA invents generative compression from nothing. The novelty claim is narrower and stronger:
BBVCA proposes a contract-relative, 3D multiscale, local-law compression architecture with explicit Generate-Verify-Repair semantics, exact restoration channels, interface accounting, and a bounded-search prototype path.
________________


3. Philosophical Premise and Engineering Translation
This paper is motivated by a strong intuition: reality itself appears to unfold as though a compact initial condition plus shared laws expanded into progressively richer structure. Whether or not that intuition is literally correct as cosmology, it is a powerful engineering pattern.
3.1 The premise in plain language
The motivating picture is simple.
* a compact beginning exists,
* public laws govern how it unfolds,
* local interactions propagate structure,
* fine detail appears over time,
* most of the world is not re-specified from scratch at every instant.
3.2 The engineering translation
BBVCA translates that picture into codec form.
* primordial condition -> artifact-specific seed payload
* physical laws -> shared public law family and arithmetic semantics
* cosmic unfolding -> deterministic multiscale generation
* observed world -> decoded artifact
* unmodeled irregularity -> exact repair streams
3.3 Why the metaphor is useful but insufficient
The metaphor is only a guide. A serious codec must still answer concrete questions.
* What is actually stored?
* What is public between encoder and decoder?
* What is generated versus repaired?
* What is exact versus approximate?
* What do boundaries cost?
* How is correctness checked?
* How is search kept finite?
This paper exists to answer those questions.
________________


4. Ontological Universality vs Codec Universality
A major conceptual issue must be handled directly.
You may reasonably argue that if reality itself arose from a single compact seed plus shared laws, then that process is in some sense an extraordinarily general decompressor. Version 9 accepts that intuition in its strongest safe form, but it distinguishes it from what a practical codec can honestly claim.
4.1 Ontological universality
An ontologically universal generator is a generative substrate that, together with shared lawful evolution, produces every artifact inside the world it defines. If such a substrate exists, then from the inside it may appear to be a universal seeded decompressor.
In that setting, the law family is already given, the world already pays the unfolding cost, and the observer lives inside the generated structure.
4.2 Codec universality
A codec-universal compressor is different. It is an artifact-to-bitstream system whose encoder and decoder must agree explicitly on what is public and what must be transmitted per artifact.
A practical codec cannot simply assume access to the hidden seed of the universe or to reality’s lawful dynamics unless those are truly part of the public decode environment.
4.3 The reconciliation
The correct engineering lesson is therefore not to reject the universal-seed intuition. It is to use it properly:
A world-generator can be extraordinarily general if its explanatory laws are already shared. A practical compressor becomes stronger to the extent that it can move explanatory burden from per-artifact payload into a stable public law family.
4.4 Consequence for BBVCA
BBVCA does not aim at a mystical per-file seed that individually contains every possible artifact. It aims at a codec family in which:
* the public law family carries as much repeatable structure as possible,
* the artifact-specific seed is compact,
* the verification machinery remains local and exact,
* and the repair stream carries only what the shared laws fail to explain.
That is the strongest version of the user’s idea that can still be made into a real codec.
________________


5. The Reconstruction Contract
Every claim in BBVCA is relative to an explicit Reconstruction Contract. A statement such as “compress the artifact” is too vague. A compressor is only meaningful once we know what counts as success.
Let the reconstruction contract be
K = (Omega, M, Delta, A, L, Pi)
where:
* Omega is the source domain,
* M is the bottom-layer mapping,
* Delta is the reconstruction criterion,
* A is the arithmetic semantics,
* L is the set of admissible liberties,
* Pi is the public law family shared by encoder and decoder.
5.1 Source domain Omega
This specifies what the input actually is: bytes, integer tensors, float fields, symbolic records, or another declared type.
5.2 Bottom-layer mapping M
This maps the source artifact into a bottom volumetric field V0. If the mapping is not fixed and public, then its choice belongs in the bitstream.
5.3 Reconstruction criterion Delta
In lossless mode, Delta requires exact reproduction. In near-lossless mode, it specifies the distortion measure, the precision domain, and the allowed bound.
5.4 Arithmetic semantics A
This fixes integer widths, fixed-point conventions, rounding, overflow, boundary behavior, and update order. Losslessness without arithmetic discipline is not a serious claim.
5.5 Admissible liberties L
This states what simplifications are legal under the contract. If fidelity, observability, temporal semantics, or precision are relaxed, that is a contract change, not a free gain.
5.6 Public law family Pi
This is the shared rule library. It may include:
* generator mode families,
* legal neighborhood types,
* fixed entropy models,
* split semantics,
* reversible update primitives,
* deterministic resolve rules.
The more explanatory burden Pi can carry without becoming too large or too rigid, the stronger the codec can become.
________________


6. Core Architectural Doctrine: Generate -> Verify -> Repair
Version 9 states the codec doctrine explicitly.
6.1 Encode doctrine
The encoder solves the following problem:
Find the smallest lawful seed and rule schedule such that local generation plus exact repair reproduces the target under the contract.
Operationally, that means:
1. Generate a candidate lower structure from an upper seed and local law.
2. Verify the candidate against the true target in a bounded local window.
3. Repair the mismatch by the cheapest exact mechanism available.
4. Compare that cost against alternatives, including splitting and literal fallback.
5. Commit the cheapest exact option.
6.2 Decode doctrine
The decoder is simpler and more rigid.
1. Replay the seed and law schedule.
2. Generate the same local predictions.
3. Replay exact retained detail, residuals, corrections, or literals.
4. Reconstruct the bottom field exactly under the contract.
6.3 Why this language is better
“Compress/decompress” suggests passive packing and unpacking. “Generate-Verify-Repair” better describes what the architecture is actually doing:
* generation carries the explanatory burden,
* verification enforces honesty,
* repair preserves universality.
________________


7. Formal Problem Statement
Let the source artifact be X in Omega.
The encoder first maps the source into the bottom field:
V0 = M(X)
BBVCA then constructs a hierarchy
V0, V1, V2, ..., VT
where:
* V0 is the bottom field,
* VT is the apex or near-apex field,
* each transition is exact under the contract.
7.1 Lossless condition
In lossless mode,
V_hat_k = V_k for all k
and therefore
X_hat = M^{-1}(V_hat_0) = X.
7.2 Near-lossless condition
In near-lossless mode, exact equality is replaced by a contract-defined distortion condition.
d_K(V_hat_0, V_0) <= epsilon_K
7.3 Two exact transition families
For each layer k, Version 9 permits two exact semantics.
Mode A: Reversible factorization
(V_{k+1}, D_k, S_k) = T_k(V_k)
where:
* V_{k+1} is the coarser upper layer,
* D_k is exact retained detail,
* S_k specifies the reversible schedule.
Decoding computes:
V_k = T_k^{-1}(V_{k+1}, D_k, S_k).
Mode B: Predictive generation plus exact restoration
V_tilde_k = P_k(V_{k+1}, S_k)
and
V_k = R_k(V_tilde_k, E_k, C_k, L_k)
where:
* E_k is an exact residual stream,
* C_k is an optional sparse correction structure,
* L_k is optional literal fallback.
7.4 Total objective
The encoder minimizes the true description length, not just seed size:
B_total = B_seed + B_law + B_param + B_detail + B_resid + B_corr + B_split + B_interface + B_literal + B_map + B_verify
subject to exact reconstruction under the contract.
________________


8. Shared-Law Advantage Principle
The deepest economic idea in BBVCA is simple.
Compression improves when explanatory burden moves from per-artifact payload into a stable public law family, provided the public law family does not become so large or so expressive that selection and parameter costs erase the gain.
This principle is the safe codec translation of the big-bang intuition.
8.1 Why shared law matters
If the encoder and decoder already share a rich enough rule family, the file no longer needs to re-specify that lawful structure. It only needs to specify:
* which laws are used,
* where they apply,
* and what exact repairs remain.
8.2 Why public law is not free magic
Public law helps only when it is genuinely shared, stable, and reusable across many artifacts. If every file requires its own large bespoke rule library, then the law has simply become hidden payload.
8.3 Prototype implication
Prototype A should use an intentionally tiny public law family. The goal is not maximum expressiveness; it is to test whether even a small lawful vocabulary plus exact repair has rate value.
________________


9. The Apex-Only Exclusion Corollary
Version 9 keeps the most important honesty condition.
Apex-Only Exclusion Corollary. A strictly smaller upper representation cannot universally and losslessly regenerate arbitrary larger lower data by itself. If the codec is universal over the contracted source class, then exactness must come from either retained detail under reversible factorization or exact restoration streams.
9.1 Why this is necessary
This corollary kills the recurring fantasy that a tiny seed alone can universally reproduce arbitrary detailed data. BBVCA is only credible because it refuses that fantasy.
9.2 Proof sketch
If the lower layer can realize more admissible states than the upper layer, then a universal injective map from lower states into upper states alone is impossible by counting. Therefore any universal exact system must preserve the omitted degrees of freedom somewhere else: in retained detail, explicit repair, or an equivalent transmitted structure.
________________


10. Why 3D Volumetric Geometry Still Matters
The architecture remains deliberately 3D-first.
10.1 Richer local neighborhoods
A 3D lattice supports face, edge, and corner adjacency, volumetric neighborhoods, and multiscale recursive structure. That gives local generators more expressive room than a flat stream.
10.2 Better fit for native volumetric domains
The strongest natural targets for BBVCA are already 3D or tensor-like:
* scientific fields,
* simulation outputs,
* medical or measurement volumes,
* structured tensor archives,
* multichannel grid data.
10.3 The mapping warning
For arbitrary 1D streams or highly irregular data, the bottom-layer mapping is doing heavy conceptual work. Forcing such sources into a volume can create false adjacencies or destroy native locality. Version 9 therefore tightens the scope:
Prototype A should target native 3D or obviously tensorized sources first.
The generic-stream question belongs later, after the architecture has earned credibility on data that actually matches its geometry.
________________


11. Generator-State Voxels and the Public Law Family
11.1 Why upper cells must be generators
Upper cells must do more than store smaller copies. They must carry enough structure to induce lower neighborhoods.
A generator-state voxel is a compact local descriptor that may include some subset of:
* a law identifier,
* a base or anchor term,
* optional directional or gradient terms,
* optional coupling or curvature terms,
* a precision code,
* flags for split, repair-present, or literal fallback.
11.2 Logical payload, not fixed-width dogma
The important quantity is not a maximal raw struct width. The important quantity is the entropy-coded average payload actually used by the chosen law family.
11.3 Prototype A law family
Prototype A uses a deliberately tiny public law family:
1. constant
2. affine / planar
3. trilinear patch
4. literal microblock
Optional sparse correction is not treated as an independent law. It is a repair mechanism.
11.4 The Goldilocks problem
If the law family is too small, literal fallback dominates. If the law family is too large, search and signaling dominate. The first prototype must therefore sit in the middle: small enough to search, expressive enough to explain something real.
________________


12. The Generate Phase
The generate phase applies a candidate local law to a region.
12.1 Inputs to generation
Generation takes:
* an upper seed or parent block state,
* a law choice from Pi,
* quantized parameters,
* a deterministic expansion schedule,
* fixed arithmetic semantics.
12.2 Output of generation
The result is a candidate lower block or lower prediction field. In Prototype A, this is a non-overlapping 2 x 2 x 2 child block predicted from the current region’s chosen law.
12.3 Prototype A generation discipline
Prototype A does not allow arbitrary search in parameter space. Instead, each law is paired with a small proposal generator derived from local statistics.
Examples:
* constant: mean candidate, median candidate
* affine: one least-squares fit, one quantized or clipped variant
* trilinear: one corner-based fit, one regularized variant
This turns continuous fitting into a tiny discrete proposal set.
________________


13. The Verify Phase
A candidate generator is only useful if the encoder can actually verify it.
13.1 Local verification bound
Local Verification Bound. A candidate transition is admissible only if the responsible upper-layer neighborhood, the generated lower region, and the exact restoration path can be jointly evaluated inside a bounded local decision window.
13.2 Why verification matters
A generator that looks elegant but cannot be directly checked against the local target is not a usable compression primitive. Verification is what converts metaphor into engineering.
13.3 What gets checked
For each candidate, the encoder checks:
* prediction error,
* exact repair burden,
* law-select and parameter bits,
* interface or split burden,
* literal fallback comparison.
13.4 Verification output
Verification does not simply return “good” or “bad.” It returns a full expected description cost under the contract.
________________


14. The Repair Phase
Repair is what makes the architecture universal and exact.
14.1 Repair mechanisms
A candidate may be repaired by:
* exact dense residuals,
* sparse corrections,
* retained detail under factorization,
* literal storage of a microblock,
* or a split followed by recursive generation below.
14.2 Repair is not failure
Repair is not an embarrassment. It is the honest place where the architecture pays for what the generator does not explain.
14.3 The repair hierarchy
A disciplined encoder should attempt repair in an escalation ladder:
1. keep candidate as-is if exact,
2. attach sparse corrections,
3. attach dense exact residuals,
4. split and recurse,
5. literal-store the region.
The cheapest exact option wins.
________________


15. Layerwise Exactness Principle
Version 9 preserves a central rule.
Layerwise Exactness Principle. BBVCA should preserve or restore exactness at each layer transition rather than allowing approximation drift to accumulate silently across many scales.
15.1 Why this principle exists
Approximation chained across many layers can create uncontrolled drift. The deeper the hierarchy, the more expensive late correction can become.
15.2 Operational consequence
Either:
* preserve omitted information as retained detail at the current layer, or
* restore the current layer exactly before continuing downward.
This keeps the architecture debuggable and rate-accounted.
________________


16. Two Exact Transition Families
16.1 Mode A: Reversible factorization
Mode A expresses the strongest form of the architecture.
A lower layer is decomposed into:
* a coarser upper layer,
* exact retained detail,
* a reversible schedule.
The decoder inverts that schedule exactly. This mode is elegant, deep, and difficult. It is not the first prototype target.
16.2 Mode B: Predictive generation plus exact restoration
Mode B is the pragmatic baseline.
A local generator predicts the lower region. Exact restoration then closes the gap. This mode is universal because exactness lives in the repair stream, not in a fantasy that the generator is always bijective.
16.3 Why both belong in one family
Mode B is the practical starting point. Mode A is the long-term deeper form. Keeping both inside one architecture prevents the project from choosing between honesty and ambition.
________________


17. Interface Cost Principle and Splitting
Splitting is powerful and dangerous.
Interface Cost Principle. A split is beneficial only when the reduction in interior modeling cost exceeds the added signaling, boundary, and repair burden introduced by the new interfaces.
17.1 What interfaces cost
A split can add:
* split signaling,
* boundary metadata,
* alignment burden,
* cross-region inconsistency,
* higher residual entropy near edges.
17.2 Why interfaces matter in BBVCA
Many generative compression proposals look impressive until interface cost is counted. BBVCA explicitly forbids hiding that cost.
17.3 Prototype A implication
Prototype A should allow splitting, but only under a narrow gating rule and in a non-overlapping regime where interface cost is easy to account for.
________________


18. The Full Cost Equation
The true code length is never just the seed.
For Version 9, the total coded cost is:
B_total = B_seed + B_law-select + B_param + B_detail + B_resid + B_corr + B_split + B_interface + B_literal + B_map + B_verify
where:
* B_seed = apex or intermediate seed payload,
* B_law-select = law identifiers and mode selection,
* B_param = quantized law parameters,
* B_detail = retained detail for reversible factorization,
* B_resid = dense exact residual streams,
* B_corr = sparse correction structures,
* B_split = partition signaling,
* B_interface = boundary and interface burden,
* B_literal = literal fallback payload,
* B_map = bottom-layer mapping metadata,
* B_verify = optional integrity structures.
18.1 The decisive local inequality
If one candidate is meant to explain n lower samples of b literal bits each, then the candidate only helps if:
g + s + r < n * b
where:
* g is generator cost,
* s is signaling and interface burden,
* r is retained-detail or repair burden.
This inequality decides whether a local law is compressive or merely decorative.
________________


19. Entropy Coding, Proxy Bootstrap, and Statistical Modeling
BBVCA does not get a free pass on entropy coding. Version 9 strengthens this point by separating the search objective from the final serialized code length, and by stating exactly how the first-pass proxy tables are initialized before the final coder has run.
19.1 What must be entropy-coded
A serious implementation must entropy-code:
* law-select streams,
* parameter deltas,
* split flags,
* interface tags,
* detail streams,
* residuals,
* sparse corrections,
* literal payloads where applicable.
19.2 The additivity-versus-entropy paradox
Prototype A relies on additive local costs so that a bottom-up dynamic program can choose between unsplit and split explanations independently at each node once child costs are known. But real context-adaptive entropy coding is not strictly additive in that way: the bit cost of a symbol can depend on the coding history of previously emitted symbols.
This creates a tension:
* dynamic programming wants frozen additive local prices,
* final entropy coding wants adaptive global statistics.
Version 9 resolves this tension by making the separation explicit rather than pretending it away.
19.3 Two-Phase Rate Discipline
Prototype A uses a two-phase rate discipline.
Phase 1: Search-time optimization. The encoder optimizes a frozen additive proxy objective
B_hat_total = B_hat_seed + B_hat_law-select + B_hat_param + B_hat_detail + B_hat_resid + B_hat_corr + B_hat_split + B_hat_interface + B_hat_literal + B_hat_map + B_hat_verify
where each B_hat_* term is computed from stream-separable lookup tables or simple closed-form proxies whose contexts depend only on public local node attributes.
Phase 2: Final serialization. Once the partition and law schedule are fixed, the encoder serializes the actual streams with the real entropy coder and obtains the realized length B_final.
If B_final differs materially from B_hat_total, the encoder may refresh the proxy tables from observed stream histograms and rerun the search once. Prototype A is therefore best viewed as a one-pass search plus one optional lagged-rate refinement pass.
The discipline is simple but important:
Prototype A is optimized exactly for the frozen proxy objective, and judged empirically by the realized serialized objective.
19.4 Proxy Bootstrap and Calibration Doctrine
Prototype A must be able to price B_hat_law-select and B_hat_param before the final coder has seen any actual stream history. Version 9 therefore requires every proxy table to be bootstrapped from one of three sources, in descending order of preference:
1. offline corpus priors from a trusted domain-matched training set,
2. a cheap artifact scan over the current artifact,
3. a deliberately pessimistic zero-order fallback when neither of the above is trustworthy.
The search phase is never allowed to wait for a sophisticated global coder to reveal the true bits. It must start from explicit tables.
A practical initialization rule is:
p_hat = lambda_c * p_corpus + lambda_a * p_artifact + lambda_u * p_uniform
with lambda_c + lambda_a + lambda_u = 1, nonzero smoothing mass on p_uniform, and all tables converted to prices through -log2 p_hat plus optional stream-specific slack.
This is best understood as shrinkage toward safety. Corpus priors provide stability, artifact scans provide local relevance, and the uniform floor prevents pathological overconfidence.
19.5 Offline priors for Prototype A
Prototype A should initialize the main stream tables from simple corpus-level counts gathered on a domain-matched archive.
Recommended priors:
* Law-select priors: counts of law_id conditioned on depth, coarse class, and parent_law.
* Parameter priors: bucketed delta histograms for each law parameter, conditioned on law_id, depth, and coarse class.
* Split priors: counts of split versus unsplit decisions conditioned on depth and heterogeneity class.
* Repair priors: residual magnitude histograms, sparse-correction occupancy rates, and literal-use rates conditioned on block class.
* Interface priors: empirical penalties by split type, exposed-face count, or simple boundary count buckets.
These priors do not need to be complicated. The first prototype benefits more from calibrated simplicity than from expressive but brittle contexts.
For stability, tables should use Dirichlet-style pseudocount smoothing or equivalent additive counts. When the corpus is small, higher-level pooled tables should backstop more specific tables through hierarchical shrinkage rather than leaving rare cells noisy.
19.6 Cheap artifact scan warm start
Offline priors are not enough by themselves when the current artifact is unusual. Prototype A should therefore permit a cheap artifact scan before the full dynamic program.
The scan should remain lightweight. It may collect:
* block-count histograms by depth and heterogeneity class,
* provisional winners among the tiny unsplit law family on a sparse sample of nodes,
* parameter-delta buckets for those provisional winners,
* rough split propensities by depth,
* and literal or residual prevalence from coarse pilot scoring.
The scan is not a hidden full encode. It is a low-cost warm start designed to tilt the proxy toward the current artifact without breaking the bounded-search doctrine.
19.7 Pessimistic zero-order fallback
For the first file in a new domain, or whenever corpus and scan priors are judged untrustworthy, Prototype A should begin from a deliberately pessimistic zero-order proxy.
That proxy may use:
* fixed bits-per-law or fixed law probabilities,
* fixed bucket costs for parameter deltas,
* raw or slightly padded costs for literals and residuals,
* simple depth-conditioned split costs,
* and no deep context mixing at all.
This closes the cold-start edge case cleanly. The first pass may be less efficient, but it will remain honest, additive, and safe.
19.8 Search-time proxy prices for B_law-select
During search, law choice must be priced without relying on future coding history. Prototype A therefore restricts the search-time law-select context to public node attributes only.
For a candidate law ell at node B, define
B_hat_law-select(ell; B) = b_hat_law( ell | depth(B), class(B), parent_law(B) )
where:
* depth(B) is the node depth,
* class(B) is a coarse heterogeneity or morphology class derived from cached local statistics,
* parent_law(B) is the already-known parent law identifier or a null root token.
The crucial restriction is that these prices may depend only on attributes already known when the node is scored. They may not depend on future sibling choices or full-stream adaptive history, because that would break additivity.
19.9 Search-time proxy prices for B_param
Parameter signaling is handled similarly. Each law has a small quantized proposal family, and parameters are priced as deltas relative to law-specific anchors or closed-form estimates.
For a parameter vector theta under law ell at node B, define
B_hat_param(theta; ell, B) = sum_j b_hat_{ell,j}( Delta theta_j | depth(B), class(B) )
where Delta theta_j is the quantized delta for parameter component j from its law-specific anchor.
This has three practical advantages.
First, it keeps B_hat_param additive and O(1) to evaluate.
Second, it keeps parameter coding honest enough to discourage over-expressive laws.
Third, it lets the encoder learn quickly which laws are expensive not only because of fit but because of signaling burden.
19.10 Residual, correction, and literal proxy costs
Search-time costs for repair streams should also remain additive. Prototype A may therefore estimate:
* dense residual cost from fixed-table coding of quantized residual values,
* sparse correction cost from simple occupancy-plus-value models,
* literal cost from fixed per-symbol tables or raw bit width,
* interface cost from fixed penalties keyed by split type and boundary count.
The point is not to predict the exact final arithmetic-coder output. The point is to preserve the right ordering of decisions under a consistent proxy objective.
19.11 Conservative anti-pruning discipline
Proxy prices should usually be slightly pessimistic. In practice this means adding a small stream-specific slack term delta_s so that search-time estimates do not systematically underprice rare events.
Version 9 adds one further rule: literal ceilings and candidate pruning should be padded by a conservative safety band. In practice, Prototype A may use
U_hat_safe(B) = B_hat_literal(B) + gamma(B)
with gamma(B) chosen as a small depth-dependent or class-dependent guard band. Candidates are pruned only when they clearly exceed this padded ceiling.
This matters because a badly calibrated first-pass proxy can otherwise prune the true winner before the optional refresh pass ever gets a chance to update the tables. A small conservative margin is cheap insurance against catastrophic over-pruning.
19.12 Concrete refresh trigger for Prototype A
Prototype A should make the lagged-rate trigger explicit.
A recommended first prototype rule is:
* rerun once if |B_final - B_hat_total| / max(B_final, 1) exceeds 4%, or
* rerun once if the absolute gap exceeds 0.02 bits per voxel on the benchmark domain,
* otherwise accept the first schedule.
The exact constants may be tuned, but the architecture should commit to concrete thresholds so later evaluations can be compared on the same basis.
19.13 Prototype A simplification
Prototype A should deliberately keep the real entropy model simple:
* separate streams by type,
* use fixed corpus-initialized tables or at most very light per-depth adaptation,
* avoid deep cross-stream coupling,
* avoid heavy context mixing in the first implementation,
* and keep the final coder close enough to the proxy model that the search-time objective remains informative.
The first prototype is not the place to invent a sophisticated entropy coder. It is the place to measure whether the generative architecture itself pays.
20. Bounded Encoder Search Doctrine
This remains the core tractability section, but Version 9 makes the optimization target more explicit.
20.1 The true problem
Unrestricted BBVCA search is combinatorial. The encoder would, in principle, need to choose among:
* many possible partitions,
* many possible laws,
* many parameter settings per law,
* many possible repair mechanisms,
* and potentially overlapping interacting neighborhoods.
That regime is not an acceptable starting point.
20.2 Prototype A doctrine
Prototype A does not attempt to solve full unrestricted BBVCA. It solves a deliberately restricted problem:
* non-overlapping regions,
* additive proxy local costs,
* bounded law family,
* bounded candidate count per node,
* bounded split depth,
* fixed local support,
* local sufficient-statistic proposal generators,
* literal fallback always legal.
This restriction is not a betrayal of the architecture. It is what makes a first honest prototype possible.
20.3 Proposal discipline
Every law in Prototype A gets a tiny deterministic proposal set.
For a region B, let Q_law(B) be the set of parameter proposals for that law. Prototype A requires:
* |Q_law(B)| is a small constant,
* each proposal can be computed from cached local statistics,
* no law triggers open-ended continuous optimization inside the main search loop.
Typical examples:
* constant: 1-2 proposals
* affine: 1-2 proposals
* trilinear: 1-2 proposals
* literal: exactly 1 proposal
Thus the total candidate count per block remains a small constant K.
20.4 Sufficient statistics and caches
Prototype A should precompute or incrementally maintain local statistics such as:
* mean,
* variance,
* sums and moments,
* directional gradients,
* local corner values,
* simple residual entropy proxies.
With such caches, candidate fitting and scoring becomes O(1) per candidate rather than requiring repeated scans of the raw block.
20.5 Literal ceiling and monotone pruning
For every region B, literal fallback defines a valid search-time upper bound:
U_hat(B) = B_hat_literal(B)
If a candidate’s partial proxy cost already satisfies
B_hat_law + B_hat_param + lower_bound( B_hat_repair + B_hat_interface ) >= U_hat(B) - tau
for some small safety margin tau, the candidate is pruned immediately.
This remains one of the strongest practical rules in the architecture. Literal fallback means the encoder never needs to keep exploring a candidate that is already more expensive than giving up under the current proxy objective. In Version 9, this ceiling is interpreted conservatively through the padded bound U_hat_safe(B) from Section 19.11 whenever proxy calibration is uncertain.
20.6 Split gating
A split is considered only if one of the following holds:
* a heterogeneity score exceeds a threshold,
* the best unsplit candidate fails to beat literal by a margin,
* a residual-density test indicates that a simpler local law is unlikely to pay,
* or a proxy-rate test predicts that children can recover the interface burden.
In effect, Prototype A treats splitting as an expensive privilege, not a default action.
20.7 Beam and budget discipline
Even in the restricted regime, the encoder should enforce:
* maximum candidate count per node,
* maximum split depth,
* maximum nodes expanded per block group,
* maximum beam width per layer if any layerwise beam is used,
* mandatory literal fallback when the budget is exhausted.
These are not tuning niceties. They are part of the codec’s engineering contract with reality.
20.8 Additive proxy objective
The deepest tractability gain comes from a deliberate combination of choices:
Prototype A disables overlap and optimizes an additive proxy objective.
When sibling regions do not overlap and their search-time costs are additive once the partition is fixed, the proxy cost for a block B can be written recursively as
C_hat(B) = min( C_hat_unsplit(B), B_hat_split(B) + sum_i C_hat(B_i) )
where the B_i are the child blocks of B.
This permits a bottom-up dynamic program over the tree:
1. evaluate the best unsplit candidate for each node under the proxy objective,
2. evaluate the split alternative from already-computed child proxy costs,
3. store the cheaper choice,
4. recover the full schedule by traceback.
20.9 Irregular adaptive trees still fit the doctrine
The dynamic-programming argument does not require every branch to reach the same depth. Split gating naturally creates an irregular adaptive octree-style partition. That is fine.
The recurrence only needs two facts:
* child sets are disjoint once a split is declared,
* node cost decomposes into a local term plus child terms under the proxy objective.
Therefore the same bottom-up pass works on any finite adaptive tree. Full regularity is convenient for exposition, not essential for correctness.
20.10 Bounded Search Proposition
Bounded Search Proposition (Prototype A, Version 9 form). Consider an adaptive fixed-arity multiscale tree with T visited nodes, bounded candidate count K per node, non-overlapping local support, additive proxy costs, and O(1) candidate scoring using cached sufficient statistics. Then the optimal Prototype A encode under the restricted proxy objective can be found by bottom-up dynamic programming in O(T * K) candidate-evaluation time and O(T) traceback storage. For bounded-arity trees built over N bottom samples, T is O(N), so the search is near-linear in source size.
Proof sketch
Each visited node evaluates at most K unsplit candidates. Split cost is computed from child proxy costs plus a constant local split/interface term. With cached statistics, each unsplit candidate is scored in O(1). Bottom-up evaluation therefore costs O(T * K). Traceback storage is O(T). In bounded-arity adaptive trees over a finite minimum block size, the number of visited nodes is linear in the number of leaves and therefore O(N).
20.11 What this proposition does and does not claim
It does show that Prototype A can avoid global intractability by living inside a disciplined restricted family with a well-defined proxy objective.
It does not show that unrestricted BBVCA with overlap, rich law coupling, and globally adaptive coding history is cheap. That harder regime remains a later research stage.
21. Prototype A: Minimal Honest Bounded-Search GVR-BBVCA
Prototype A should be intentionally conservative.
Component
	Prototype A choice
	Source class
	Native 3D integer volumes or obvious tensorized fields
	Bottom mapping
	Fixed public mapping
	Hierarchy
	Cubic power-of-two pyramid or adaptive octree stop rules
	Transition size
	2 x 2 x 2
	Public law family
	Constant, affine, trilinear, literal
	Arithmetic
	Integer / fixed-point only
	Exactness mode
	Predictive generation plus exact restoration
	Overlap
	Disabled
	Splitting
	Yes, bounded depth
	Verification
	Local blockwise exact verification
	Candidate proposals
	Closed-form, local-statistic based
	Candidate cap per node
	Small fixed constant K
	Split gating
	Required
	Literal ceiling
	Required
	Search objective
	Frozen additive proxy rate
	Final serialization
	Separate per-stream entropy coding pass
	Optional refinement
	One lagged-rate proxy refresh pass
	Entropy coding
	Required; per-stream arithmetic/range coding with fixed corpus tables or very light per-depth adaptation
	Benchmark focus
	Rate, repair density, interface cost, proxy-gap, encode time
	21.1 Prototype A encoder pipeline
A conceptually complete Prototype A encoder can be described in ten stages.
1. Map the source into V0.
2. Build a multiscale statistics pyramid or equivalent cached local statistics.
3. Bootstrap proxy price tables for law IDs, parameter deltas, split flags, and repair streams from offline priors, a cheap artifact scan, or a pessimistic zero-order fallback.
4. Enumerate the small candidate law set for each node using closed-form proposals.
5. Score each unsplit candidate by full local proxy cost.
6. Compare unsplit cost against split cost using bottom-up dynamic programming on the adaptive tree.
7. Trace back the chosen partition and law schedule from the root.
8. Assemble law streams, parameter streams, split streams, repair streams, and literals.
9. Serialize the actual streams with the real entropy coder.
10. Optionally refresh proxy tables from observed stream histograms and rerun once if the proxy gap exceeds the committed threshold.
21.2 Search-time cost model in practice
Prototype A should score a node with a stream-separable proxy model that looks like this:
C_hat_unsplit(B, candidate) = B_hat_law-select + B_hat_param + B_hat_repair + B_hat_interface_local
and
C_hat_split(B) = B_hat_split(B) + sum_i C_hat(B_i)
The design rule is strict:
* search-time contexts may depend on public local node attributes,
* final entropy contexts may be only modestly richer,
* the first prototype should prefer per-stream fixed tables or very light per-depth adaptation,
* and the final coder should stay close enough to the search-time proxy that decisions remain meaningful.
In concrete Prototype A terms, the proxy tables should be bootstrapped in this order:
1. domain prior tables from an offline corpus,
2. artifact warm-start tables from a cheap pre-scan,
3. uniform or padded zero-order tables for any missing or untrusted contexts.
Table cells should be smoothed, shrunk toward pooled parents when sparse, and converted into fixed search-time prices before the first dynamic-program pass begins.
21.3 Systems engineering doctrine
Once candidate scoring is reduced to O(1) table lookups, Prototype A becomes a memory-system problem as much as an algorithmic one. The implementation should therefore treat layout as a first-class design choice.
Recommended discipline:
* store the statistics pyramid level-major,
* prefer Morton or brick-major order to preserve spatial locality,
* keep node records compact and fixed-width where possible,
* separate streams by type and often by depth,
* use branch-light scoring kernels,
* prefetch child statistics when walking the tree bottom-up.
In practice, the first fast encoder may be limited more by cache misses and memory bandwidth than by arithmetic throughput. That is not a side note. It is part of the prototype doctrine.
21.4 Why this is the right first implementation
This prototype is minimal without being trivial. It tests the architecture honestly:
* real local generation,
* real verification,
* real repair,
* real split/interface accounting,
* real search discipline,
* real separation between search-time proxy rates and realized serialized rates.
21.5 What would count as a good early result
A narrow win on friendly volumetric data would already matter, provided the paper reports all of the following transparently:
* full bit-budget breakdown,
* proxy versus final serialized rate gap,
* encode and decode runtime,
* prune rate and split rate,
* fallback and literal density,
* sensitivity to conservative versus aggressive split gating.
22. Prototype Roadmap Beyond A
22.1 Prototype B: better split policies and interface models
Keep overlap disabled, but refine split gating and interface accounting.
22.2 Prototype C: controlled overlap
Introduce overlapping support fields with strict local verification limits and carefully bounded overlap order.
22.3 Prototype D: reversible factorization mode
Build a genuine integer-domain factorization mode with exact retained-detail channels.
22.4 Prototype E: richer public law families
Only after the baseline is understood should the law family expand. Additions must be justified by ablations showing that the new law reduces total cost more than it increases search and signaling burden.
22.5 Prototype F: non-native mappings and harder domains
Only after success on native volumetric data should the architecture push into generic streams or aggressively learned mappings.
________________


23. Evaluation and Falsification
A public architecture should say in advance what would count as success and failure.
23.1 Core metrics
For lossless mode:
* compressed size,
* encode time,
* decode time,
* memory use,
* bit-budget breakdown by component,
* proxy-budget breakdown by component,
* gap between B_hat_total and realized B_final,
* layerwise retained-detail or repair density,
* split and literal frequency,
* interface cost,
* nodes visited, pruned, and accepted,
* and whether the refresh trigger was crossed under the committed threshold rule.
For near-lossless mode:
* bitrate,
* distortion,
* artifact structure,
* runtime,
* repair burden,
* and proxy-gap stability.
23.2 Required baselines
BBVCA should be compared against:
* straightforward multiscale residual coders,
* reversible transform or lifting-style baselines,
* volumetric wavelet or octree-style baselines for native 3D data,
* strong generic compressors for generic streams,
* and any domain-specific baseline relevant to the claimed application.
23.3 Required ablations
At minimum:
* 3D versus 2D organization,
* non-overlap versus overlap once overlap exists,
* reversible factorization versus predictive-plus-restoration semantics,
* fixed mapping versus locality-aware mapping,
* interface-aware versus naive splitting,
* conservative versus aggressive split gating,
* corpus-only proxy bootstrap versus corpus-plus-scan versus zero-order bootstrap,
* frozen proxy tables versus one refreshed outer iteration,
* conservative versus tight anti-pruning margins,
* per-term bit-budget breakdown,
* proxy-versus-final rate mismatch by stream.
23.4 Friendly tests
BBVCA should first be tested on data aligned with its own modeling hypothesis:
* constant fields,
* smooth gradients,
* piecewise-smooth volumes,
* repeated motifs,
* structured periodic patterns,
* tensor-like scientific or learned-parameter blocks with clear local regularity.
If the architecture cannot win there, its core premise is in trouble.
23.5 Hostile tests
BBVCA should also be tested on:
* random fields,
* locality-destroyed shuffled variants,
* adversarial heterogeneous blocks,
* and synthetic blocks whose proxy model is deliberately miscalibrated.
The success criterion there is not high compression. It is controlled overhead, graceful fallback, bounded proxy-gap after final serialization, and no catastrophic over-pruning under the conservative first-pass proxy.
23.6 What would count as success
BBVCA has a meaningful success case if there exists any domain in which:
* generator layers explain a substantial portion of the source,
* exact restoration burden remains controlled,
* interface cost stays bounded,
* proxy-rate decisions survive final serialization with modest regret,
* encode and decode costs remain practical,
* and total coded size beats simpler baselines.
23.7 What would count as falsification
BBVCA is falsified as a broadly useful codec family if repeated experiments show that:
* generator payload is too expensive,
* retained detail or repair channels dominate the rate,
* proxy-rate search systematically chooses the wrong schedules,
* overlap adds little over simpler models,
* mapping overhead destroys locality gains,
* interface cost erases the benefit of splitting,
* or solver complexity makes the codec impractical.
24. Risks and Failure Modes
Version 9 states the hard risks plainly.
24.1 Search explosion returns when restrictions are removed
Prototype A is tractable because it is intentionally restricted. Once overlap, large law families, or globally coupled decisions are added, the hard search problem reappears.
24.2 Proxy-model mismatch
The dynamic program is exact for the frozen proxy objective, not automatically for the realized final code length. If the proxy model is poorly calibrated, the encoder can make systematically bad structural decisions.
24.3 Proxy bootstrap failure
If corpus priors are out of domain, artifact warm starts are too weak, and zero-order fallbacks are not padded conservatively enough, Prototype A can optimize the wrong local cost function with great confidence. Version 9 therefore treats bootstrap quality, smoothing, shrinkage, and anti-pruning margins as first-class engineering obligations rather than optional tuning details.
24.4 Refresh limitations
A lagged-rate refresh pass can improve prices after serialization, but it cannot perfectly recover branches that were pruned too aggressively in the first pass. That is why Version 9 insists on conservative literal ceilings and measurable proxy-gap thresholds instead of trusting refresh alone to fix everything.
24.5 Memory-bandwidth bottlenecks
Once candidate scoring becomes cheap, encoder performance can become limited by memory layout, cache locality, and statistics-pyramid bandwidth rather than by arithmetic cost.
24.6 Mapping failure
A poor bottom-layer mapping can destroy locality and render the whole volumetric premise unhelpful.
24.7 Generator overcost
If the active laws need too many bits, the architecture loses before repair is even counted.
24.8 Interface explosion
Aggressive splitting can reduce local error while increasing boundary burden enough to erase the gain.
24.9 Law-family drift
The temptation to add “just one more mode” is a real danger. An undisciplined law family can quietly convert BBVCA into a messy parameter-storing system.
24.10 Literal fallback domination
If the chosen law family does not explain enough of the source, the codec degenerates into a computationally expensive route to near-literal storage.
24.11 False optimism from friendly domains
Wins on highly structured synthetic data are necessary but not sufficient. The architecture must also degrade honestly on data it cannot explain.
25. Philosophical Implications, Stated Carefully
Version 9 keeps the philosophical core, but on a tighter leash.
The strongest inspiration behind BBVCA is the thought that reality itself may be the lawful unfolding of a compact seed. Whether or not that is true as cosmology, it suggests a profound engineering pattern:
* explanation is often cheaper than literal restatement,
* law and initial condition can carry immense descriptive burden,
* local generation plus sparse correction can produce rich worlds,
* the boundary between “data” and “process” is more fluid than ordinary codecs admit.
But the codec stands even if the cosmology does not. The architecture succeeds or fails on rate, runtime, and falsification, not on metaphysical beauty.
________________


26. Conclusion
Big Bang Volumetric Compression Architecture proposes a disciplined way to think about compression as Generate-Verify-Repair search over seeded local laws rather than as symbol shortening alone.
Version 9 makes four final commitments.
First, it accepts the strongest safe version of the universal-seed intuition by distinguishing ontological universality from codec universality. A world-scale seed plus lawful unfolding may be an ontologically general decompressor. A practical codec still has to pay for whatever is not already shared.
Second, it makes exactness unavoidable. A smaller apex alone cannot universally recreate arbitrary larger data. Exactness requires retained detail or exact repair streams.
Third, it gives the architecture a real implementation starting point. Prototype A constrains the search space through a bounded public law family, deterministic proposal discipline, literal ceilings, split gating, additive proxy costs, and bottom-up dynamic programming on adaptive trees. That does not solve unrestricted generative compression. It does make the first honest BBVCA prototype computationally plausible.
Fourth, it refuses to hide behind vague future entropy coding. Search-time decisions are made under a frozen additive proxy objective initialized by explicit proxy bootstrap rules, and the paper requires those decisions to be tested against the realized serialized rate, with one lagged-rate refinement pass available when the proxy gap crosses a concrete threshold.
The architecture’s wager is now precise:
Can a shared lawful generator plus compact seeds and exact repair beat simpler codecs on the right structured domains, while keeping encoder search bounded enough to build?
That question is no longer mystical. It is a research program.
________________


References
Barron, A., Rissanen, J., & Yu, B. (1998). The minimum description length principle in coding and modeling. IEEE Transactions on Information Theory, 44(6), 2743-2760.
Calderbank, A. R., Daubechies, I., Sweldens, W., & Yeo, B.-L. (1998). Wavelet transforms that map integers to integers. Applied and Computational Harmonic Analysis, 5(3), 332-369.
Jacquin, A. E. (1992). Image coding based on a fractal theory of iterated contractive image transformations. IEEE Transactions on Image Processing, 1(1), 18-30.
Mallat, S. G. (1989). Multiresolution approximations and wavelet orthonormal bases of L^2(R). Transactions of the American Mathematical Society, 315(1), 69-87.
Rissanen, J. (1978). Modeling by shortest data description. Automatica, 14(5), 465-471.
Shannon, C. E. (1948). A mathematical theory of communication. Bell System Technical Journal, 27, 379-423, 623-656.
Sweldens, W. (1996). The lifting scheme: A custom-design construction of biorthogonal wavelets. Applied and Computational Harmonic Analysis, 3(2), 186-200.
Taubman, D. S., & Marcellin, M. W. (2002). JPEG2000: Image Compression Fundamentals, Standards and Practice. Kluwer Academic Publishers.
Ballé, J., Minnen, D., Singh, S., Hwang, S. J., & Johnston, N. (2018). Variational image compression with a scale hyperprior. International Conference on Learning Representations.
________________


Appendix A. Compact Definition
Big Bang Volumetric Compression Architecture (BBVCA) is a contract-relative hierarchical compression framework in which source data is mapped into a bottom 3D volumetric field and represented across multiple scales by compact upper-layer generator states or coarse factors. Exact reconstruction is achieved either by reversible factorization with retained detail or by predictive generation plus exact restoration. The encoder performs Generate -> Verify -> Repair search under a bounded public law family; the decoder replays the seed, the laws, and the exact restoration streams. Version 9 emphasizes a restricted non-overlapping additive Prototype A regime in which encoder search can be kept computationally disciplined through deterministic proposals, literal ceilings, split gating, conservative anti-pruning margins, and bottom-up dynamic programming.
________________


Appendix B. One-Sentence Thesis
Compression is the search for the smallest shared-law world-generator plus the smallest exact proof that the generated world is the artifact we meant.
________________


Appendix C. Formal Statements
C.1 Reconstruction Contract Principle
All BBVCA claims are relative to an explicit reconstruction contract specifying source domain, mapping, reconstruction criterion, arithmetic semantics, admissible liberties, and public law family.
C.2 Shared-Law Advantage Principle
Compression improves when explanatory burden moves from per-artifact payload into a stable public law family, provided that law growth and law-selection cost do not erase the saved repair burden.
C.3 Apex-Only Exclusion Corollary
If the upper layer has strictly fewer effective degrees of freedom than the lower layer over the contracted source class, then universal exact recovery from the upper layer alone is impossible. Exactness requires retained detail or exact restoration.
C.4 Local Verification Bound
A candidate transition is admissible only if the responsible upper-layer neighborhood, target lower region, and exact restoration path can be jointly evaluated within a bounded local decision window.
C.5 Layerwise Exactness Principle
Exactness should be preserved or restored at each layer transition rather than deferred until the end of a long approximate chain.
C.6 Interface Cost Principle
A split is beneficial only when the reduction in interior modeling cost exceeds the added signaling, boundary, and repair burden introduced by the new interfaces.
C.7 Proxy Bootstrap and Calibration Doctrine
Every search-time proxy table in Prototype A must be initializable from offline corpus priors, a cheap artifact scan, or a pessimistic zero-order fallback with smoothing and shrinkage toward safe pooled tables. Search-time prices must be frozen before the dynamic-program pass begins and refreshed only in a later outer iteration.
C.8 Conservative Anti-Pruning Principle
Literal ceilings and candidate pruning in the first pass should be evaluated against a padded proxy ceiling U_hat_safe(B) rather than the raw literal estimate alone, so that proxy miscalibration does not silently eliminate promising schedules before the optional refresh pass.
C.9 Bounded Search Proposition
Under Prototype A assumptions - non-overlapping local support, additive proxy costs, bounded candidate count, and O(1) scoring from cached statistics - the optimal encode inside the restricted model family can be found by bottom-up dynamic programming over an adaptive tree in near-linear candidate-evaluation time.
C.10 Two-Phase Rate Discipline and Proxy-Rate Principle
Prototype A search is optimized under a frozen additive proxy code-length model whose contexts depend only on public local node attributes. Final entropy coding is executed in a separate serialization pass and may optionally induce one lagged-rate refinement iteration if realized rates diverge materially from proxy estimates.
________________


Appendix D. Reference Pseudocode
D.1 Bottom-up Prototype A encoder
function encode_node(node, proxy_tables):
    literal_cost = proxy_cost_literal(node, proxy_tables)

    best_unsplit = literal_cost
    best_choice  = make_literal_choice(node)

    for candidate in propose_candidates(node):
        partial = proxy_cost_law(candidate, node, proxy_tables)                 + proxy_cost_param(candidate, node, proxy_tables)
        if partial >= literal_cost:
            continue

        repair_est = proxy_estimate_exact_repair(candidate, node, proxy_tables)
        total = partial + repair_est

        if total < best_unsplit:
            best_unsplit = total
            best_choice  = candidate

    if should_consider_split(node):
        split_cost = proxy_cost_split(node, proxy_tables)
        for child in children(node):
            split_cost += stored_best_cost(child)

        if split_cost < best_unsplit:
            store_best(node, split_cost, make_split_choice(node))
        else:
            store_best(node, best_unsplit, best_choice)
    else:
        store_best(node, best_unsplit, best_choice)
function encode_artifact(X):
    V0            = map_source(X)
    stats_pyramid = build_statistics_pyramid(V0)
    proxy_tables  = bootstrap_proxy_tables(V0, stats_pyramid, corpus_priors, cheap_scan=True, zero_order_fallback=True)

    for node in bottom_up_nodes(stats_pyramid):
        encode_node(node, proxy_tables)

    schedule = traceback_from_root()
    streams  = assemble_streams(schedule, V0)
    B_final  = entropy_serialize(streams)

    if proxy_gap(schedule, B_final, proxy_tables) > refresh_threshold:
        proxy_tables = refresh_proxy_tables_from_streams(streams, corpus_priors)
        rerun_once()

    return bitstream(schedule, streams)
D.2 Decoder replay
function decode_node(node, plan):
    if plan.kind == LITERAL:
        return read_literal_block(plan)

    if plan.kind == UNSPLIT_GENERATOR:
        pred = generate_block(plan.seed, plan.law, plan.param)
        return apply_exact_restoration(pred, plan.restore_stream)

    if plan.kind == SPLIT:
        block = empty_block(node.shape)
        for child_plan in plan.children:
            place_child(block, decode_node(child_plan.node, child_plan))
        return block
D.3 Reversible factorization placeholder
function factor_layer_reversible(lower_layer, meta):
    work = copy(lower_layer)
    upper = init_upper(meta)
    detail = empty_detail_store()

    for step in meta.forward_schedule:
        work, emitted = forward_invertible_step(work, upper, step)
        append(detail, emitted)

    return upper, detail, meta
________________


Appendix E. Glossary
Artifact-specific seed - per-file payload anchoring lawful generation.
Generate -> Verify -> Repair - the encoder doctrine of proposing structure, checking it locally, and paying exact repair only where needed.
Interface cost - boundary burden created by splitting regions.
Literal ceiling - the upper bound given by exact literal fallback for a region.
Ontological universality - a world-scale seed plus lawful unfolding that generates everything inside that world.
Codec universality - a practical codec that must account explicitly for what is public and what is transmitted.
Public law family - the stable shared rule library known to both encoder and decoder.
Repair stream - retained detail, residuals, sparse corrections, or literals used to restore exactness.
Split gating - subdivision only when heterogeneity or rate tests justify it.