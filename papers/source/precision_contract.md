# The Precision Contract

## A Functional Rate–Distortion Theory for Behavior-Preserving Neural Computation

**Manuscript version 1.0 — July 2026**

> **Status.** This is a theoretical and systems paper. It introduces
> definitions, propositions, an architecture, a certificate format, and
> a falsifiable experimental program. It does not claim that the
> proposed compiler or certification system has already been implemented
> at frontier-model scale.

### Abstract

How many bits should an artificial-intelligence weight contain? The
question appears to invite a physical upper bound: perhaps empirical
measurement precision, the ratio between cosmic and Planck scales, or
the information capacity of the observable universe. This paper argues
that no such argument yields a universal, representation-independent
upper bound on the useful precision of an individual neural-network
weight. Weight magnitude and sensitivity depend on parameterization;
equivalent networks can rescale individual weights arbitrarily while
preserving exactly the same input–output function. Cosmic scale ratios
primarily concern range and coordinate choice, not the significand
precision required for every learned scalar. Global physical information
bounds constrain complete physical systems, not an arbitrary field in
one software representation.

We replace the per-weight question with a functional one: **what is the
shortest executable description that preserves a model’s
contract-relevant behavior to an accepted tolerance?** We formalize a
*precision contract* that specifies the deployment domain, protected
behaviors, distortion metrics, thresholds, confidence requirements,
resource budget, and escalation policy. Given a reference model and a
code family, the resulting functional rate–distortion quantity is the
minimum complete description length—including weights, scales,
codebooks, sparse exceptions, routing logic, residual precision, and
assurance evidence—needed to satisfy that contract.

The framework treats compression as a search over behavioral equivalence
classes rather than a search for the nearest parameter vector. It
motivates contract-conditioned precision fields, progressive
base-and-residual models, dynamic precision routing, and a Functional
Precision Compiler that canonicalizes parameterization, estimates
functional sensitivity, allocates bits, generates nested executable
representations, verifies protected properties, and issues a
machine-readable precision certificate. We identify the proposal’s
relationship to rate–distortion theory, minimum description length,
mixed-precision quantization, low-bit language models, nested bit-width
systems, and formal verification. We conclude with a reproducible
experimental and falsification program. The central claim is not that
intelligence has a universal bit width, but that useful precision is the
least physical description required to preserve declared behavioral
distinctions.

**Keywords:** neural-network quantization; rate–distortion; minimum
description length; behavioral equivalence; mixed precision; progressive
precision; formal verification; AI assurance; efficient inference;
advanced AI systems

------------------------------------------------------------------------

## Contents

1.  Introduction  
2.  Why a universal per-weight upper bound is ill-posed  
3.  Prior work and the novelty boundary  
4.  Formal framework  
5.  The precision contract  
6.  The Functional Precision Compiler  
7.  Progressive executable precision  
8.  Verification, certification, and assurance bits  
9.  Experimental and falsification program  
10. Implications for advanced AI systems  
11. Limitations and open problems  
12. Conclusion  
    Appendices A–D  
    References

------------------------------------------------------------------------

# 1. Introduction

Modern neural networks are commonly trained or deployed in
floating-point, integer, or hybrid numerical formats. Their weights may
be stored in 32-bit or 16-bit floating point, quantized to 8, 4, 3, 2,
or approximately 1.58 bits, or represented through codebooks, sparse
exceptions, low-rank factors, and other structured encodings. The
practical motivation is clear: model parameters and transient state
consume memory, memory bandwidth, energy, and time. In many inference
regimes, moving data costs at least as much as arithmetic, so reducing
numerical representation can produce substantial system benefits \[1\],
\[2\].

A natural philosophical question follows: *What should the upper bound
be on the precision of an AI weight?* One proposed answer begins with
physical measurement. If observations contain only finitely many
meaningful digits, perhaps weights cannot usefully contain more. A
second answer compares the radius of the observable universe with the
Planck length and converts that ratio into roughly two hundred
significand bits. A third invokes holographic or thermodynamic
information bounds. These arguments are intuitively attractive because
they seek a boundary between physically meaningful distinctions and
mathematical fiction.

They do not, however, identify an invariant property of neural
computation. A neural-network weight is not a directly measured natural
constant. It is one coordinate in a nonunique representation of a
function or policy. The same behavior may be encoded by radically
different weight magnitudes, by different numbers of parameters, by
binary limbs rather than one high-precision scalar, by a codebook plus
indices, or by an external algorithm. A per-weight limit can therefore
change under an exact reparameterization while the implemented behavior
remains unchanged.

This paper develops an alternative. The relevant object is not the
precision of one coordinate but the **minimum complete physical
description required to preserve behavior under a stated contract**. The
proposal combines five ideas:

1.  **Representation invariance.** Precision claims should refer to
    behavior, not arbitrary parameter coordinates.
2.  **Functional rate–distortion.** Compression should minimize full
    description length subject to an accepted behavioral distortion.
3.  **Contract-conditioned precision.** The required fidelity depends on
    the deployment domain, protected properties, and consequence of
    error.
4.  **Progressive execution.** A system may begin with a low-bit base
    and load residual precision only when the contract requires it.
5.  **Certification.** A compressed implementation should carry explicit
    evidence about which behaviors were tested or verified, under which
    assumptions, and with what residual uncertainty.

The information-theoretic inspiration is classical rate–distortion
theory, which asks for the minimum rate needed to represent a source
under a distortion criterion \[3\], \[4\], \[5\]. The model-selection
inspiration is minimum description length (MDL), which treats compact
description as an inductive principle \[6\], and earlier work explicitly
applied description length to neural-network weights \[7\]. The
engineering inspiration is decades of quantization, pruning,
mixed-precision training, low-bit inference, and sensitivity-aware bit
allocation. The assurance inspiration is formal work showing that
properties of a real-valued network do not automatically transfer to its
bit-exact quantized implementation \[8\], \[9\], \[10\], \[11\].

The paper’s principal contribution is a unifying problem formulation and
systems architecture. It does **not** claim to invent rate–distortion
coding, MDL, mixed precision, Hessian-aware quantization, progressive
bit widths, or neural-network verification. Rather, it proposes that
these ingredients be assembled around a common artifact—the **precision
contract**—and evaluated by the complete number of physical bits
required to preserve declared behavior.

## 1.1 Main claims

The paper advances six claims.

**Claim 1 — No universal per-weight bound.** There is no
representation-independent upper bound on the useful magnitude or bit
width of an individual neural-network weight. Any such bound requires a
fixed representation, scale convention, decoder, and behavioral
tolerance.

**Claim 2 — The invariant object is functional description length.**
Given a reference model, deployment domain, code family, and behavioral
contract, one can define the minimum total description length of an
acceptable executable implementation.

**Claim 3 — Parameter proximity is not behavioral equivalence.** Small
weight error can produce large behavioral error, and large parameter
displacement can preserve behavior exactly. Therefore, weight-space
reconstruction should be treated as a proxy, not the final acceptance
criterion.

**Claim 4 — Precision is a field, not a scalar.** Useful bit width may
vary by layer, channel, transformed direction, token, task, uncertainty
state, and safety criticality. The proper object is a
contract-conditioned precision allocation.

**Claim 5 — Additional precision should be progressive and
accountable.** A model can be encoded as a low-bit base plus residual
refinements. Each additional refinement should have a measured or
verified contribution to contract satisfaction.

**Claim 6 — Compression is a model change that requires assurance.** If
a behavior is protected, it must be evaluated or verified on the
compressed implementation itself. Aggregate benchmark retention is
insufficient evidence of equivalence.

## 1.2 Contributions

This manuscript provides:

- a counterargument to measurement-, Planck-, and holographic-style
  per-weight ceilings;
- a formal definition of a precision contract and contract-relative
  behavioral equivalence;
- a functional rate–distortion objective that counts representation,
  structure, residual, routing, and assurance bits;
- a local sensitivity analysis that connects the proposal to Fisher-,
  Hessian-, and Jacobian-aware allocation;
- an architecture for a Functional Precision Compiler;
- a progressive base-and-residual execution model with
  contract-conditioned escalation;
- a machine-readable precision certificate schema;
- a set of experiments, ablations, and failure conditions capable of
  falsifying the proposal’s strongest empirical hypotheses.

# 2. Why a Universal Per-Weight Upper Bound Is Ill-Posed

## 2.1 Four quantities that are often conflated

Discussions of “weight precision” often mix four distinct concepts.

| Quantity               | Question answered                                         | Typical mechanism                             |
|------------------------|-----------------------------------------------------------|-----------------------------------------------|
| **Magnitude**          | How large or small is the numerical value?                | Parameter scale, normalization, units         |
| **Dynamic range**      | What orders of magnitude can the format represent?        | Exponent, shared scale, logarithmic code      |
| **Resolution**         | How closely spaced are representable values near a scale? | Significand or quantization step              |
| **Description length** | How many physical bits encode the executable object?      | Values, indices, codebooks, metadata, decoder |

A single floating-point format separates range from local resolution
through exponent and significand fields \[12\], \[13\]. A codebook
representation separates the stored index from the precision of the
reconstructed value. A block-quantized tensor may use low-bit indices
and higher-precision block scales. A sparse representation may use very
few value bits but many structural bits. Consequently, “bits per weight”
is already an incomplete accounting convention.

## 2.2 Exact rescaling destroys an invariant per-weight scale

Consider a two-layer ReLU network

$$
f_\theta(x)=W_2\,\operatorname{ReLU}(W_1x).
$$

For any scalar $c>0$, positive homogeneity gives

$$
\operatorname{ReLU}(cW_1x)=c\,\operatorname{ReLU}(W_1x),
$$

and therefore

$$
f_\theta(x)
=\frac{W_2}{c}\,\operatorname{ReLU}(cW_1x).
$$

The transformation

$$
(W_1,W_2)\mapsto (cW_1,W_2/c)
$$

preserves the function exactly while making the first-layer weights
arbitrarily large and the second-layer weights arbitrarily small.

**Proposition 1 — Nonexistence of a representation-invariant magnitude
ceiling.**  
For positively homogeneous multilayer networks with at least one
rescalable hidden unit, no finite bound on individual weight magnitude
is invariant over all parameter vectors that implement the same
function.

**Proof sketch.** Apply the transformation above with
$c\rightarrow\infty$ or $c\rightarrow 0$. The function is unchanged, but
at least one nonzero weight magnitude diverges. $\square$

This phenomenon is part of a larger family of symmetries: neuron
permutations, sign symmetries in compatible architectures, invertible
changes of basis between linear blocks, normalization-induced scale
freedoms, and redundant factorizations. Research on neural loss geometry
has emphasized that parameter-space sharpness and related quantities can
change under behavior-preserving reparameterization \[14\].
Path-normalized optimization was developed in part to obtain a geometry
invariant to certain rescalings \[15\]. Quantization work has also
exploited factorization freedoms to reduce error without changing the
represented full-precision function \[16\].

This does not mean that a particular hardware format lacks a maximum. It
means that such a maximum is a property of the chosen representation,
not a universal property of intelligence or the learned function.

## 2.3 Bit width can be redistributed across coordinates

Suppose a target scalar $a$ must be represented to $b$ bits. There is no
requirement that one physical field contain all $b$ bits. One can
represent

$$
a = \sum_{k=0}^{m-1} 2^{-kq} a_k,
$$

where each $a_k$ is a $q$-bit limb. The same information can be
distributed across several low-precision weights, a recurrent
computation, a small symbolic program, a table, or an external tool.
Conversely, many nominally high-precision weights may contain far fewer
independent bits because of correlation, low rank, pruning, shared
codebooks, or deterministic generation.

Therefore, a statement such as “no weight should exceed 64 bits” does
not bound the precision of the computation. A model can emulate
higher-precision arithmetic through composition. Nor does a statement
such as “a trillion 4-bit weights contain four trillion learned bits”
follow without accounting for redundancy, decoder structure, and side
information.

## 2.4 Cosmic scale ratios concern range and coordinates, not universal significand width

The Planck length is a derived physical scale. The 2022 CODATA
recommended value is approximately $1.616255\times10^{-35}$ meters
\[17\]. It is often treated heuristically as a scale at which
quantum-gravity effects may become important. It is not an
experimentally established statement that space is a universal lattice
with Planck-sized pixels.

Even granting a largest and smallest relevant length, their ratio does
not imply that every scalar requires enough significand bits to resolve
the smallest interval at the largest coordinate. A floating-point
representation can cover many orders of magnitude through its exponent.
What demands extreme significand precision is the specific operation of
representing a tiny increment and a huge absolute coordinate in one
number, for example

$$
10^{26} + 10^{-35}.
$$

That requirement is largely avoided by coordinate design: local frames,
relative positions, hierarchical decompositions, residual coordinates,
nondimensionalization, or separate fields for coarse and fine scale.
Numerical analysis routinely treats conditioning and representation as
part of the problem rather than assuming one global scalar must hold all
scales \[13\].

The same lesson applies to AI. A representation that seems to require
hundreds of bits may be poorly conditioned or unnecessarily global.
Canonicalization, normalization, block scaling, rotations, and residual
decomposition can move information into a form that is cheaper to
encode.

## 2.5 Global physical bounds do not become per-weight software bounds

The holographic principle and related entropy bounds concern the maximum
information associated with physical regions under specified
gravitational assumptions \[18\]. Landauer’s principle connects
logically irreversible operations to a thermodynamic cost under
idealized conditions \[19\]. These are relevant to the ultimate physical
implementation of computation. They do not single out a neural weight as
a privileged unit of physical information.

A global bound $B_{\text{system}}$ can constrain the combined state of
hardware, memory, environment, and controller. It does not imply

$$
b_i \leq B_{\text{system}}/N
$$

for every software parameter $i$, because the software representation
may be redundant, virtual, compressed, recomputed, shared, or
nonuniform. A single logical variable can be encoded across many
physical degrees of freedom; many logical variables can be generated
from one compact program. The mapping between logical fields and
physical information is architecture-dependent.

## 2.6 Measurement precision does not directly cap learned precision

The claim that a model cannot contain more precision than its inputs
also fails without qualification.

First, repeated observations can estimate a shared latent variable more
precisely than a single observation. Under independent noise with
standard deviation $\sigma$, the standard error of a sample mean scales
approximately as $\sigma/\sqrt{N}$. The resulting estimate can contain
more reliable digits than any one measurement.

Second, categorical data do not have a simple scalar bit-depth
interpretation. A text token may be stored as an integer, but the
statistical information in relationships among many tokens is not
bounded by the bit width of the token identifier.

Third, some target domains are exact or synthetic: integer arithmetic,
formal logic, source code, cryptographic transformations, cellular
automata, and deterministic simulators. Exactness requirements may arise
from the task specification rather than sensor resolution.

Fourth, numerical precision can affect algorithms through condition
numbers, repeated accumulation, close decision boundaries, chaotic
trajectories, or exact invariants. A low-noise physical input does not
guarantee that the complete computation is well conditioned.

The defensible conclusion is narrower: once numerical error is below all
contract-relevant uncertainty and decision margins, additional precision
has no demonstrated operational value. Identifying that point requires a
task-specific behavioral analysis.

# 3. Prior Work and the Novelty Boundary

## 3.1 Information theory and description length

Rate–distortion theory formalizes the minimum communication rate
required to reproduce a source under a chosen distortion measure \[4\],
\[5\]. MDL and related Bayesian coding views use description length to
balance fit and complexity \[6\]. Hinton and van Camp explicitly
minimized the description length of neural-network weights as a
regularization principle \[7\]. These traditions establish that the
number of bits required is meaningful only relative to a source model, a
code, side information, and a distortion criterion.

The present proposal differs in its target object. It treats a trained
model implementation—not only a data source or a parameter posterior—as
the object to be encoded, and it defines distortion over deployment
behavior rather than only parameter reconstruction or average predictive
loss. It also requires full accounting of decoder, routing, residual,
and assurance overhead.

## 3.2 Quantization and low-precision neural computation

Quantized neural networks predate contemporary large language models.
Work on limited-precision training, binary and quantized networks,
integer-only inference, deep compression, and mixed-precision training
established that low-bit representations can retain substantial
capability when algorithms and architectures are adapted accordingly
\[20\], \[21\], \[22\], \[23\], \[24\], \[25\].

For transformer and language-model inference, LLM.int8() isolated
outlier dimensions for higher-precision treatment \[26\]. GPTQ used
approximate second-order information for one-shot post-training weight
quantization \[27\]. SmoothQuant migrated quantization difficulty from
activations to weights through equivalent scaling \[28\]. AWQ protected
a small subset of activation-salient weights \[29\]. QuIP and QuIP# used
incoherence processing and structured codebooks for very low-bit
quantization \[30\], \[31\]. AQLM used additive codebooks in the 2–3-bit
regime \[32\]. Native low-bit training has progressed toward ternary and
near-one-bit model families \[33\], \[34\].

These results support a practical premise of this paper: the raw
precision traditionally assigned to every weight is often far greater
than the precision required for useful inference. They do not prove a
universal bit width. Reported success depends on architecture, scale,
task, calibration data, training procedure, activations, accumulators,
outlier handling, and evaluation criteria.

## 3.3 Sensitivity-aware and mixed-precision allocation

Optimal Brain Damage used second-order information to estimate the
effect of deleting parameters \[35\]. Later methods allocate precision
using Hessian or curvature proxies. HAWQ and HAWQ-V2 are prominent
examples of layer-wise mixed-precision quantization guided by
Hessian-derived sensitivity \[36\], \[37\]. AdaRound optimized discrete
rounding decisions rather than simply choosing nearest values \[38\].

The Precision Contract generalizes this line in two ways. First,
sensitivity is defined relative to contract-relevant behavior, which may
include safety, calibration, action selection, trajectory outcomes, or
invariants rather than only loss or tensor reconstruction. Second, the
optimization includes all executable and assurance overhead, not just
nominal weight bits.

## 3.4 Multi-bit and progressive representations

Any-Precision LLM overlays several quantized bit widths in storage
comparable to one higher-bit model \[39\]. Matryoshka Quantization
co-trains nested integer representations so that most-significant-bit
slices operate at multiple precisions \[40\]. MatGPTQ extends this
direction to a post-training, sliceable multi-precision pipeline \[41\].

These systems demonstrate important mechanisms for progressive
precision. The proposed contribution is not the mechanism itself. It is
the contract-driven semantic layer that determines *which* level is
adequate, *when* escalation is required, *what* behaviors must be
reverified, and *how* the evidence is recorded.

## 3.5 Formal verification of quantized networks

Quantized networks execute discrete, bit-exact operations that can
differ materially from idealized real arithmetic. Giacobbe, Henzinger,
and Lechner studied synthesis and verification of quantization bit
widths \[8\]. Subsequent work improved the scalability of bit-exact
verification and quantization-aware certification \[9\], \[10\], \[42\].
QEBVerif and related methods bound the behavioral error between
full-precision and quantized networks \[11\], \[43\].

The key lesson is methodological: a property verified for the reference
model cannot simply be inherited by the compressed implementation.
Quantization is a program transformation, and protected properties
should be checked on the transformed program or through a sound relation
between the two.

## 3.6 Behavioral and security consequences beyond average accuracy

Recent evidence reinforces the need for richer acceptance criteria.
Quantization can create a distinct security surface that an attacker may
exploit \[44\]. Emerging work reports that perplexity or aggregate
accuracy can remain favorable while alignment, reliability, or
instance-level decisions change \[45\], \[46\], \[47\]. These 2026
results are recent preprints and should be treated as provisional
evidence, not settled consensus. Their relevance is that they expose a
measurable possibility already implied by the formal framework: two
models can have similar aggregate scores while violating different
protected behaviors.

## 3.7 What this paper does and does not claim

| This paper proposes                                         | This paper does not claim                                   |
|-------------------------------------------------------------|-------------------------------------------------------------|
| A representation-invariant contract for acceptable behavior | A universal numerical format for intelligence               |
| A complete description-length objective                     | That nominal bits-per-weight equals learned information     |
| Progressive precision governed by contract satisfaction     | The invention of nested or mixed precision                  |
| A compiler and certificate architecture                     | Existing frontier-scale formal certification                |
| Falsifiable experiments and acceptance tests                | That low precision is always safer, faster, or better       |
| A framework for choosing “enough” precision                 | That FP64, 206 bits, or any fixed width is a cosmic maximum |

The intended contribution is a common language and optimization target
that can connect compression research, systems design, evaluation, and
assurance.

# 4. Formal Framework

## 4.1 Reference system, implementation, and deployment domain

Let $M_\theta$ denote a reference AI system parameterized by $\theta$.
The system may be a classifier, probabilistic predictor, language model,
policy, controller, tool-using agent, or composite architecture. It can
contain learned weights, fixed algorithms, retrieval systems, and
external tools. A candidate compressed implementation is denoted
$\widehat{M}_z$, where $z$ is a finite binary description interpreted by
a specified decoder $\mathsf{Dec}$:

$$
\widehat{M}_z = \mathsf{Dec}(z).
$$

The decoder is part of the representation. A statement about code length
is incomplete unless the decoder, codebooks, scales, transforms, and
side information are fixed or counted.

Let $\mathcal{E}$ be a deployment environment and
$\mathcal{X}_{\mathcal{C}}$ the contract’s admissible input or state
domain. For a static predictor, the behavior may be a conditional
distribution $p_\theta(y\mid x)$. For an agent, behavior may be a
distribution over trajectories

$$
\tau=(s_0,a_0,s_1,a_1,\ldots,s_T),
$$

induced by the policy, environment, tool responses, and sampling
process. The contract must state which of these sources of randomness
are controlled, coupled, averaged, or treated adversarially.

This separation matters. A quantized model evaluated with a different
sampler, prompt template, kernel, or tool implementation is not merely a
different parameter representation; it is a different system. The
precision contract applies to the complete deployed computation within
its declared boundary.

## 4.2 The precision contract

A **precision contract** is a tuple

$$
\mathcal{C}
=
(\mathcal{D},\mathcal{B},\mathcal{M},\boldsymbol{\varepsilon},\mathcal{A},\alpha,\mathcal{R},\Pi),
$$

where:

- $\mathcal{D}$ specifies the deployment domain, input distributions,
  environments, and excluded regions;
- $\mathcal{B}$ identifies protected behaviors or properties;
- $\mathcal{M}=\{d_1,\ldots,d_m\}$ defines distortion or violation
  metrics;
- $\boldsymbol{\varepsilon}=\{\varepsilon_1,\ldots,\varepsilon_m\}$ sets
  acceptance thresholds;
- $\mathcal{A}$ specifies aggregation rules, such as expectation,
  quantile, maximum, conditional rate, or logical conjunction;
- $\alpha$ specifies statistical confidence or verification coverage;
- $\mathcal{R}$ gives physical resource constraints or objectives;
- $\Pi$ specifies an escalation, abstention, or fallback policy.

The contract is not the reference model itself. It is a statement of
which distinctions in the reference behavior matter for deployment. A
contract can permit a candidate to improve some behaviors or differ in
inconsequential ways. It can also protect external properties not
guaranteed by the reference model—for example, latency limits, energy
budgets, or a verified invariant.

## 4.3 Behavioral distortion as a vector

No single scalar metric is adequate for every AI system. Define a vector
of contract-relevant distortions:

$$
\mathbf{D}_{\mathcal{C}}(M_\theta,\widehat{M}_z)
=
\begin{bmatrix}
D_{\text{output}}\\
D_{\text{decision}}\\
D_{\text{calibration}}\\
D_{\text{trajectory}}\\
D_{\text{safety}}\\
D_{\text{invariant}}\\
D_{\text{resource}}
\end{bmatrix}.
$$

Illustrative components include:

### Output-distribution distortion

For probabilistic predictors,

$$
D_{\mathrm{KL}}
=
\mathbb{E}_{x\sim P_{\mathcal{D}}}
\left[
\operatorname{KL}
\bigl(
 p_\theta(\cdot\mid x)
\,\|\,
 p_z(\cdot\mid x)
\bigr)
\right].
$$

A symmetric divergence, Wasserstein distance, logit difference, or
task-specific score may be more appropriate in some settings.

### Decision disagreement

For deterministic decisions $a_\theta(x)$ and $a_z(x)$,

$$
D_{\mathrm{agree}}
=
\Pr_{x\sim P_{\mathcal{D}}}
\left[a_\theta(x)\neq a_z(x)\right].
$$

Conditional disagreement on rare or protected subsets can be more
informative than the global rate.

### Calibration distortion

Let $\operatorname{Cal}(M;S)$ be a calibration statistic on subset $S$.
Then

$$
D_{\mathrm{cal}}
=
\left|
\operatorname{Cal}(M_\theta;S)
-
\operatorname{Cal}(\widehat{M}_z;S)
\right|.
$$

### Trajectory distortion

For agents, one can compare induced trajectory distributions:

$$
D_{\tau}
=
\operatorname{TV}
\left(
P_\theta(\tau\mid\mathcal{E}),
P_z(\tau\mid\mathcal{E})
\right),
$$

or compare contract-relevant outcomes, intervention rates, cumulative
cost, tool selection, or reachability of unsafe states.

### Property violations

For a predicate $\varphi$ over inputs, outputs, or trajectories,

$$
D_{\varphi}
=
\Pr[\neg\varphi(\widehat{M}_z)]
$$

under a statistical interpretation, or

$$
D_{\varphi}=0
$$

only if a formal verifier proves the property over the declared region.

The contract accepts $\widehat{M}_z$ when an aggregation predicate is
satisfied:

$$
\operatorname{SAT}(\mathcal{C},\widehat{M}_z)=1.
$$

A simple contract uses component-wise constraints,

$$
D_j(M_\theta,\widehat{M}_z)\leq\varepsilon_j
\quad\text{for all }j,
$$

but lexicographic, Pareto, risk-weighted, and conditional rules are also
possible. Safety-critical constraints should generally not be averaged
away by utility gains elsewhere.

## 4.4 Complete executable description length

Let $L_{\mathsf{U}}(z)$ be the length in bits of description $z$ under a
fixed prefix-free code or reference machine $\mathsf{U}$. In practical
systems, the accounted length should include at least

$$
L(z)=
B_{\mathrm{value}}
+B_{\mathrm{structure}}
+B_{\mathrm{residual}}
+B_{\mathrm{routing}}
+B_{\mathrm{decoder}}
+B_{\mathrm{assurance}}.
$$

The terms mean:

- $B_{\mathrm{value}}$: low-bit indices, ordinary scalar values, or bit
  planes;
- $B_{\mathrm{structure}}$: sparsity masks, codebooks, low-rank factors,
  permutations, transforms, and topology;
- $B_{\mathrm{residual}}$: exceptions and precision refinements;
- $B_{\mathrm{routing}}$: metadata or policy used to select precision
  levels;
- $B_{\mathrm{decoder}}$: nonshared code required to reconstruct or
  execute the representation;
- $B_{\mathrm{assurance}}$: certificates, test manifests, hashes, proof
  artifacts, and evidence required by the deployment process.

The last term is intentionally unconventional. Assurance evidence may be
tiny relative to a frontier model, but it is not free, and its
production may dominate compute even when its storage is small. A
complete system objective should distinguish *stored assurance bits*
from *assurance-generation cost*.

Description length is reference-dependent. Changing the decoder or
allowing a large shared library can reduce $L(z)$. This is not a defect;
it is a standard property of coding. Comparisons must state shared side
information and use the same accounting boundary.

## 4.5 Functional rate–distortion

Given a reference model $M_\theta$, contract $\mathcal{C}$, decoder
family $\mathfrak{D}$, and code family $\mathfrak{Z}$, define the
**functional contract rate**

$$
R^{\star}(M_\theta,\mathcal{C};\mathfrak{D},\mathfrak{Z})
=
\min_{\substack{\mathsf{Dec}\in\mathfrak{D},\;z\in\mathfrak{Z}\\
\operatorname{SAT}(\mathcal{C},\mathsf{Dec}(z))=1}}
L_{\mathsf{Dec}}(z).
$$

When the contract is represented by a scalar distortion and tolerance
$\varepsilon$, write

$$
R^{\star}(\varepsilon)
=
\min_z
\left\{
L(z):D_{\mathcal{C}}(M_\theta,\widehat{M}_z)\leq\varepsilon
\right\}.
$$

This is the paper’s proposed replacement for a universal bits-per-weight
ceiling.

Several details are important:

1.  **The optimum is contract-relative.** A medical triage contract and
    a casual autocomplete contract can assign different precision to the
    same reference model.
2.  **The optimum is code-family-relative.** Restricting candidates to
    uniform scalar quantization can require more bits than allowing
    rotations, codebooks, sparsity, or architectural substitution.
3.  **The optimum is not necessarily a quantized copy.** The cheapest
    acceptable implementation may be distilled, factorized, symbolic,
    modular, or tool-assisted.
4.  **The optimum may not exist in a continuous family.** In practice,
    one searches a finite or compact candidate family and reports the
    best known upper bound.
5.  **Computing the exact optimum is generally intractable.** The
    definition provides a target and comparison principle, not a claim
    of easy global optimization.

## 4.6 Behavioral quotient space

Define contract-relative equivalence at tolerance
$\boldsymbol{\varepsilon}$:

$$
M\sim_{\mathcal{C}} M'
\quad\Longleftrightarrow\quad
\operatorname{SAT}(\mathcal{C},M')=1
$$

when $M$ is the designated reference, or symmetrically,

$$
M\sim_{\mathcal{C},\boldsymbol{\varepsilon}}M'
\quad\Longleftrightarrow\quad
D_j(M,M')\leq\varepsilon_j
\quad\forall j
$$

for symmetric metrics. The corresponding acceptable set is

$$
[M]_{\mathcal{C}}
=
\{M':\operatorname{SAT}(\mathcal{C},M')=1\}.
$$

Compression then becomes

$$
\widehat{M}^{\star}
=
\arg\min_{M'\in[M]_{\mathcal{C}}}
L(M').
$$

The key shift is conceptual:

> The goal is not to find the closest parameter vector. The goal is to
> find the cheapest executable representative of an acceptable
> behavioral class.

The word “equivalence” should be used carefully. If the distortion is
asymmetric, empirical, or distribution-limited, the relation may not
satisfy all mathematical properties of an equivalence relation. In those
cases, “contract-acceptable set” is more precise. A true quotient space
requires reflexivity, symmetry, and transitivity; many deployment
metrics provide only an approximate neighborhood. The framework permits
either, but the certificate must state which interpretation is used.

## 4.7 Elementary properties

**Proposition 2 — Monotonicity in tolerance.**  
For a fixed reference model, code family, decoder, and scalar
distortion, if $\varepsilon_1\leq\varepsilon_2$, then

$$
R^{\star}(\varepsilon_2)\leq R^{\star}(\varepsilon_1).
$$

**Proof.** The feasible set at tolerance $\varepsilon_1$ is a subset of
the feasible set at $\varepsilon_2$. Minimization over a superset cannot
yield a larger optimum. $\square$

This basic property allows a functional rate–distortion curve. It does
**not** imply that every heuristic quantizer improves monotonically as
nominal bit width increases. Different calibration, rounding, codebooks,
kernels, and routes can produce nonmonotone behavioral metrics.

**Proposition 3 — Representation dependence of nominal per-weight
rate.**  
There exist functionally identical implementations with different
parameter counts and different nominal bits per parameter.

**Proof sketch.** Split a weight into multiple summed limbs, duplicate a
neuron and divide its outgoing contribution, or refactor a matrix into
products with additional degrees of freedom. These transformations
change the number and format of stored parameters while preserving the
function. $\square$

**Corollary.** Nominal bits per weight is suitable as a hardware or
storage statistic only when the representation and all overhead are
fixed. It is not an invariant measure of model information.

**Proposition 4 — Contract strengthening cannot reduce the exact
optimum.**  
If every implementation satisfying contract $\mathcal{C}_2$ also
satisfies $\mathcal{C}_1$, then

$$
R^{\star}(\mathcal{C}_2)\geq R^{\star}(\mathcal{C}_1).
$$

This formalizes an intuitive governance trade-off: protecting more
behaviors or demanding smaller violation rates may require more bits,
more routing, more assurance evidence, or all three.

## 4.8 Local functional sensitivity

Although the global objective is behavioral, local second-order
approximations remain useful. Let $\delta\theta=\widehat{\theta}-\theta$
be a small perturbation in a fixed canonical parameterization. For a
smooth scalar distortion,

$$
D(\theta,\theta+\delta\theta)
\approx
D(\theta,\theta)
+
\nabla D(\theta)^\top\delta\theta
+
\frac{1}{2}\delta\theta^\top H_D\delta\theta.
$$

At a stationary reference and with $D(\theta,\theta)=0$, the local
approximation becomes

$$
D
\approx
\frac{1}{2}\delta\theta^\top F\delta\theta,
$$

where $F$ may be a positive-semidefinite approximation such as an
empirical Fisher, generalized Gauss–Newton matrix, output-Jacobian Gram
matrix, or projected Hessian.

Let

$$
F=U\Lambda U^\top,
\qquad
z=U^\top\theta,
$$

with eigenvalues $\lambda_j\geq 0$. If coordinate $z_j$ is quantized
with step $\Delta_j$ and the error is approximately independent and
uniform on $[-\Delta_j/2,\Delta_j/2]$, then

$$
\mathbb{E}[D]
\approx
\sum_j \frac{\lambda_j\Delta_j^2}{24}.
$$

For active range $[-A_j,A_j]$, an idealized scalar bit allocation
satisfies

$$
b_j\approx\log_2\left(\frac{2A_j}{\Delta_j}\right).
$$

Minimizing total bits subject to a distortion budget yields finer steps
in directions with larger $\lambda_j$. This recovers the intuition
behind second-order and mixed-precision methods \[27\], \[36\], \[37\],
while clarifying that the relevant curvature should correspond to the
contract, not automatically to training loss.

The approximation has important limits:

- neural networks contain flat directions and symmetries, so
  canonicalization or projection is needed;
- the Hessian may be indefinite away from a local optimum;
- large, discrete quantization errors are not local perturbations;
- rare-event and worst-case properties may be invisible to average
  curvature;
- sequential agents can amplify small local deviations over long
  horizons;
- safety behavior can be discontinuous at a decision or refusal
  boundary.

Thus local sensitivity is an allocation heuristic, not a certificate.

## 4.9 The irreducible operational floor

For a specified deployment, define an effective floor

$$
\varepsilon_{\mathrm{floor}}
=
\max\{
\varepsilon_{\mathrm{observation}},
\varepsilon_{\mathrm{label}},
\varepsilon_{\mathrm{evaluation}},
\varepsilon_{\mathrm{deployment}},
\varepsilon_{\mathrm{policy}}
\},
$$

where the terms summarize irreducible or accepted uncertainty in
evidence, labels, measurement, environment, and policy. The **useful
rate ceiling** under that contract is

$$
R_{\mathrm{useful}}
=R^{\star}(\varepsilon_{\mathrm{floor}}).
$$

This is not a universal constant. It is the point at which further
numerical fidelity cannot be shown to improve contract-relevant outcomes
under the available evidence and accepted risk. A different contract,
new measurement process, or stronger verifier may lower the floor and
justify additional bits.

The distinction between *epistemically unsupported* and *operationally
irrelevant* precision is essential. A bit can lack direct observational
support yet still stabilize a computation. Conversely, a bit can
correspond to a measurable parameter difference yet have no effect on
any protected decision. The contract resolves the issue by measuring
consequences rather than metaphysical significance.

# 5. The Precision Contract

## 5.1 Purpose

The precision contract is both a mathematical specification and an
engineering governance artifact. It answers five questions:

1.  **Where must the implementation work?**
2.  **Which behaviors must be preserved or improved?**
3.  **How will differences be measured?**
4.  **What evidence is sufficient for acceptance?**
5.  **What should happen when the evidence or operating condition is
    inadequate?**

Without these fields, “the quantized model is equivalent” is not a
testable statement.

## 5.2 Required contract fields

A minimal contract should include the following.

| Field                  | Required content                                                 | Failure prevented                            |
|------------------------|------------------------------------------------------------------|----------------------------------------------|
| **Identity**           | Reference hash, candidate hash, tokenizer, code, kernels         | Comparing the wrong artifacts                |
| **Boundary**           | Included model, sampler, retrieval, tools, hardware semantics    | Hidden system changes                        |
| **Domain**             | Input distributions, regions, environments, exclusions           | Overgeneralizing from calibration data       |
| **Protected behavior** | Decisions, probabilities, trajectories, invariants, safety rules | Optimizing only average loss                 |
| **Metric**             | Exact formula, direction, conditioning, aggregation              | Ambiguous “quality” claims                   |
| **Threshold**          | Tolerance, quantile, maximum, confidence level                   | Post hoc acceptance                          |
| **Resources**          | Storage, bandwidth, latency, energy, hardware                    | Compression that is not operationally useful |
| **Escalation**         | Higher precision, fallback, abstention, human review             | Silent operation outside evidence            |
| **Evidence**           | Tests, proofs, coverage, seeds, datasets, tool versions          | Unreproducible certification                 |
| **Expiry**             | Date, model revision, environment revision, drift trigger        | Treating stale evidence as permanent         |

## 5.3 Contract classes

Contracts can be organized into four broad classes.

### Distributional contracts

These require average or quantile behavior under an explicitly sampled
distribution. They are suitable for broad utility and efficiency studies
but may provide weak guarantees for rare cases.

Example:

$$
\mathbb{E}_{x\sim P_{\mathrm{deploy}}}
\operatorname{KL}(p_\theta\|p_z)
\leq 10^{-3}
$$

with a 95% upper confidence bound.

### Conditional contracts

These protect designated subpopulations, task categories, or risk
regions:

$$
D_j(M_\theta,M_z\mid x\in S_k)\leq\varepsilon_{jk}
\quad\forall k.
$$

They help prevent majority behavior from hiding degradation on rare but
important slices.

### Worst-case or formal contracts

These demand that a property hold for all inputs in a defined region:

$$
\forall x\in\mathcal{X}_{\mathrm{safe}},
\quad
\varphi(\widehat{M}_z,x)=\mathrm{true}.
$$

Such contracts may require exact bit-vector, mixed-integer,
abstract-interpretation, or proof-carrying techniques. Current methods
do not scale to every frontier architecture, so the certified region and
abstraction must be stated explicitly \[9\], \[42\].

### Adaptive contracts

These permit multiple precision levels and define an escalation rule. A
low-cost level may be acceptable for ordinary cases, while protected or
uncertain cases route to a higher-fidelity implementation.

An adaptive contract therefore constrains both the model levels and the
router:

$$
\Pr[\text{contract violation after routing}]
\leq\varepsilon,
$$

subject to a resource objective such as expected memory traffic or
latency.

## 5.4 Protected behavior should be consequence-aware

A contract should not merely copy the benchmark used during development.
It should identify behaviors whose alteration changes real decisions or
obligations. Examples include:

- top-1 action or tool selection;
- probability assigned to a critical diagnosis or fault;
- calibration near an abstention threshold;
- refusal behavior for dangerous requests;
- non-discrimination constraints on protected slices;
- conservation or stability invariants in a scientific surrogate;
- collision avoidance in a controller;
- exactness in a theorem checker or cryptographic subroutine;
- long-horizon task completion and recovery behavior;
- provenance, citation, or audit obligations.

This creates an explicit distinction between **fidelity to the
reference** and **fitness for deployment**. A candidate can closely
mimic a flawed reference and still fail the deployment contract.
Conversely, it can differ from the reference in ways that improve the
protected outcome. The contract should say which objective dominates.

## 5.5 Statistical acceptance and uncertainty

Empirical certification is itself noisy. For a Bernoulli violation rate
$p$, observing zero failures in $n$ independent tests does not prove
$p=0$. The certificate should report a confidence bound and the sampling
design. For dependent or adaptively generated prompts, standard
independent-sample intervals may be inappropriate.

A statistically grounded contract therefore records:

- the estimand;
- sample construction and inclusion criteria;
- dependence assumptions;
- number of trials and random seeds;
- point estimate and uncertainty interval;
- multiplicity correction for many protected slices;
- drift or out-of-distribution tests;
- the difference between absence of observed failure and verified
  absence of failure.

Formal and empirical evidence can coexist. A property may be formally
verified on a bounded numerical region and statistically tested
elsewhere.

## 5.6 Resource terms belong inside, not outside, the contract

Compression is useful only if it improves an operational objective.
Nominal storage reduction may fail to improve latency because of
dequantization overhead, irregular sparsity, poor kernel support, memory
alignment, or routing cost. Conversely, a representation with slightly
more bits may be faster on available hardware.

Define a resource vector

$$
\mathbf{R}(\widehat{M}_z)
=
(B_{\mathrm{stored}},
B_{\mathrm{moved}},
C_{\mathrm{ops}},
T_{\mathrm{latency}},
E_{\mathrm{energy}},
M_{\mathrm{peak}}).
$$

The contract may minimize a weighted physical objective

$$
J
=
\lambda_B B_{\mathrm{moved}}
+
\lambda_C C_{\mathrm{ops}}
+
\lambda_T T_{\mathrm{latency}}
+
\lambda_E E_{\mathrm{energy}},
$$

subject to behavioral constraints. Coefficients should be measured or
declared for the target hardware; they are not universal constants.

## 5.7 Contract versioning and expiry

A precision certificate is valid only for the artifacts and environment
it names. It should expire or require review when any of the following
changes:

- reference or candidate weights;
- tokenizer, prompt policy, sampler, or decoding parameters;
- quantization kernel or compiler version;
- hardware arithmetic semantics;
- retrieval corpus or tool interface;
- protected dataset or regulatory requirement;
- observed deployment distribution;
- threat model;
- escalation threshold.

This mirrors broader documentation and risk-management practices,
including model cards and lifecycle-oriented AI risk frameworks \[48\],
\[49\], while adding bit-exact representation and
behavioral-preservation fields.

# 6. The Functional Precision Compiler

## 6.1 Overview

A **Functional Precision Compiler** takes a reference system, a
precision contract, a target execution environment, and a family of
admissible encodings. It returns one or more executable precision
levels, a routing policy, and an evidence package.

The proposed pipeline is:

$$
\text{reference}
\rightarrow
\text{canonicalize}
\rightarrow
\text{measure}
\rightarrow
\text{transform}
\rightarrow
\text{allocate}
\rightarrow
\text{encode}
\rightarrow
\text{route}
\rightarrow
\text{verify}
\rightarrow
\text{certify}.
$$

Each stage exists to prevent a specific category error. Canonicalization
reduces arbitrary parameter-scale effects. Measurement ties sensitivity
to behavior. Transformation exposes compressible structure. Allocation
converts a global contract into local budgets. Encoding produces
physical artifacts. Routing handles context-dependent requirements.
Verification tests the actual implementation. Certification records
scope and residual uncertainty.

## 6.2 Compiler inputs

The compiler receives:

1.  **Reference system $M_\theta$.** All files needed to reproduce the
    reference behavior, including tokenizer, preprocessing, sampler,
    external modules, and software versions.
2.  **Precision contract $\mathcal{C}$.** Domain, protected behaviors,
    thresholds, resources, evidence rules, and escalation policy.
3.  **Calibration and validation suites.** These must be disjoint where
    statistical claims require independence.
4.  **Target platform $\mathcal{H}$.** Arithmetic formats, kernels,
    memory hierarchy, latency and energy measurement procedures, and
    deterministic or nondeterministic semantics.
5.  **Encoding grammar $\mathfrak{Z}$.** Permitted scalar formats, block
    sizes, codebooks, sparse structures, low-rank factors, rotations,
    residual planes, and routing mechanisms.
6.  **Assurance budget.** Limits on testing, formal verification, proof
    generation, and human review.

The output is not merely a weight file. It is a deployment package

$$
\mathcal{P}
=
\left(
\{z^{(0)},\ldots,z^{(K)}\},
\pi,
\mathsf{Dec},
\mathsf{Cert}
\right),
$$

where the $z^{(k)}$ are precision levels or refinements, $\pi$ is a
router, $\mathsf{Dec}$ is the execution decoder, and $\mathsf{Cert}$ is
the certificate and evidence manifest.

## 6.3 Stage A — Canonicalization

Quantization decisions should not depend unnecessarily on arbitrary
parameterization. The compiler first seeks a canonical or at least
standardized representative of the model’s symmetry class.

Possible operations include:

- folding batch or affine normalization into adjacent linear layers;
- balancing incoming and outgoing scales of positively homogeneous
  units;
- fixing signs or permutations where a deterministic convention exists;
- normalizing low-rank factors;
- merging exact linear transformations;
- removing dead units and exact zero directions;
- nondimensionalizing scientific inputs and states;
- recording transformations so that equivalence is auditable.

For a rescalable hidden unit with incoming vector $u$ and outgoing
vector $v$, one simple balance minimizes a norm-based surrogate such as

$$
\min_{c>0}
\left(
\|cu\|_2^2+
\|v/c\|_2^2
\right),
$$

whose optimum equalizes the two contributions. This does not uniquely
solve canonicalization, nor does it guarantee the best quantization. It
reduces a known source of arbitrary scale sensitivity.

Canonicalization must itself preserve the reference behavior within a
separately recorded numerical tolerance. A compiler should retain a
reversible transformation log and verify the canonicalized
full-precision model before compression.

## 6.4 Stage B — Contract instrumentation

The compiler translates each protected behavior into executable probes
or formal specifications. This stage produces a measurement graph
linking internal perturbations to contract outcomes.

Examples include:

- output KL on representative prompts;
- top-action agreement near decision boundaries;
- expected calibration error on risk strata;
- refusal or safe-completion classification on adversarial prompts;
- reachability of forbidden controller states;
- exact invariant checks in a scientific simulator;
- long-horizon rollout cost under coupled environment randomness;
- tool-call sequence agreement;
- structured judge ensembles with adjudication rules.

The instrumentation should include *negative controls*. If the metric
does not detect deliberately destructive perturbations, it cannot
support a strong certificate. It should also include *positive controls*
demonstrating expected invariances, such as exact neuron permutations or
rescalings.

## 6.5 Stage C — Functional sensitivity estimation

The compiler estimates which model components matter under the contract.
No single estimator is sufficient. A practical system can combine:

- local Hessian or Fisher approximations;
- output Jacobian norms;
- activation salience and outlier statistics;
- causal ablation or activation patching;
- layer replacement with quantized candidates;
- blockwise reconstruction error propagated to outputs;
- adversarial searches for contract violations;
- influence on trajectory-level outcomes;
- empirical disagreement concentrated near protected boundaries.

Let $g_j(x)$ denote the derivative of a contract-relevant scalar with
respect to transformed coordinate $z_j$. A distributional salience can
be

$$
s_j^{\mathrm{avg}}
=
\mathbb{E}_{x\sim P_{\mathcal{D}}}
[g_j(x)^2],
$$

while a protected-tail salience can be

$$
s_j^{\mathrm{tail}}
=
\operatorname{Quantile}_{1-\rho}
\left(g_j(x)^2\mid x\in S_{\mathrm{protected}}\right).
$$

A robust allocation may use

$$
s_j
=
\max\left(
\eta_{\mathrm{avg}}s_j^{\mathrm{avg}},
\eta_{\mathrm{tail}}s_j^{\mathrm{tail}},
\eta_{\mathrm{formal}}s_j^{\mathrm{bound}}
\right).
$$

This prevents average-token behavior from dominating rare but
contract-critical behavior.

Sensitivity estimates should be treated as uncertain. The compiler
should track confidence intervals or stability across calibration
subsets. Large allocation changes under small calibration changes are
themselves a risk signal.

## 6.6 Stage D — Representation transformation

The next stage moves the model into a representation where important
information is concentrated and quantization error is easier to control.
Existing quantization research provides many candidate transforms:
equalization, rotations, incoherence processing, blockwise scaling,
low-rank decomposition, additive codebooks, outlier extraction, and
factorization \[16\], \[28\], \[29\], \[30\], \[31\], \[32\].

The contract perspective changes the transform objective. Rather than
minimizing only

$$
\|W-\widehat W\|_F^2,
$$

the compiler seeks a transform $T$ and code $z$ that minimize

$$
L(z)+\lambda D_{\mathcal{C}}(M_\theta,\mathsf{Dec}_T(z)),
$$

or satisfy hard behavioral constraints while minimizing physical cost.

A transform is valuable when it produces one or more of the following:

- contract-sensitive information concentrated in fewer coordinates;
- lower dynamic range within blocks;
- outliers isolated into sparse exceptions;
- residuals with rapidly decaying energy or functional salience;
- nested bit planes whose prefixes remain useful;
- hardware-friendly regularity;
- simpler verification bounds.

The last criterion is important. The smallest empirical encoding may not
be the easiest to certify. A slightly larger, more regular
representation can have lower total lifecycle cost.

## 6.7 Stage E — Global bit and structure allocation

Let components be indexed by $j$, candidate encoding choices by
$q\in\mathcal{Q}_j$, description cost by $B_{jq}$, estimated resource
cost by $R_{jq}$, and predicted distortion contribution by $d_{ijq}$ for
contract metric $i$. A simplified allocation problem is

$$
\min_{x}
\sum_{j,q} x_{jq}
\left(B_{jq}+\lambda_R R_{jq}\right)
$$

subject to

$$
\sum_{j,q}x_{jq}d_{ijq}\leq\varepsilon_i
\qquad (i=1,\ldots,m),
$$

and

$$
\sum_q x_{jq}=1,
\qquad
x_{jq}\in\{0,1\}.
$$

This resembles a multiple-choice knapsack or integer program. In real
networks, component interactions violate additivity, so the compiler
alternates allocation with end-to-end validation. Candidate choices can
include:

- prune;
- binary, ternary, or small integer;
- scalar 2-, 3-, 4-, 6-, or 8-bit;
- additive or vector codebook;
- low-rank plus residual;
- sparse high-precision exception;
- protected full-precision block;
- recomputation from a generator;
- external exact routine.

The allocation should count scale and metadata overhead. A 2-bit tensor
with one 16-bit scale per four weights is not a 2-bit-per-weight
representation in complete accounting. Nor is a sparse tensor cheap if
its indices dominate.

## 6.8 Stage F — Base and residual construction

The compiler produces a base model $M^{(0)}$ and residual refinements.
For a weight block,

$$
W
=
\widehat W^{(0)}
+
R^{(1)}+
R^{(2)}+
\cdots+
R^{(K)}+E,
$$

where $E$ is the final unencoded error. Residuals may be bit planes,
sparse corrections, low-rank factors, codebook additions, or specialized
protected modules.

A useful residual ordering maximizes contract benefit per marginal
physical cost:

$$
\rho_k
=
\frac{
D_{\mathcal{C}}(M,M^{(k-1)})
-
D_{\mathcal{C}}(M,M^{(k)})
}{
L(R^{(k)})+\beta\,C(R^{(k)})
}.
$$

Residuals are ordered approximately by decreasing $\rho_k$, subject to
dependencies and hardware constraints. This gives a behavioral
interpretation to a bit plane: it is not merely a more significant
numeric digit; it is an increment whose value is measured by contract
improvement.

## 6.9 Stage G — Precision routing

Let $k\in\{0,\ldots,K\}$ index executable precision levels. The router

$$
\pi:
(x,h,u,r)\mapsto k
$$

may depend on input $x$, internal state $h$, estimated uncertainty $u$,
and risk class $r$. Its objective is to minimize expected resource cost
while maintaining the routed contract:

$$
\min_{\pi}
\mathbb{E}[R(M^{(\pi(x))})]
$$

subject to

$$
\operatorname{SAT}
\left(
\mathcal{C},
M^{(\pi)}
\right)=1.
$$

Router features can include:

- margin between top decisions;
- entropy or disagreement among lightweight probes;
- detection of a protected domain;
- estimated numerical condition;
- rollout instability;
- safety classifier activation;
- verifier inability to prove a local property;
- prior failures on similar inputs.

A router creates a new failure mode: false confidence at low precision.
It must therefore be evaluated as part of the system, not treated as
free orchestration. Conservative routing and an abstention path may be
preferable when the router is uncertain.

## 6.10 Stage H — End-to-end verification

The compiler verifies the exact exported artifacts on target semantics.
It should distinguish:

- **reconstruction validation:** tensor or activation error;
- **behavioral validation:** contract metrics on held-out and
  adversarial suites;
- **bit-exact validation:** execution with actual integer and rounding
  semantics;
- **formal verification:** mathematical proof over a declared region;
- **systems validation:** latency, energy, memory, concurrency, and
  failure recovery;
- **router validation:** conditional error and escalation coverage;
- **drift validation:** sensitivity to changes in data and environment.

A passed proxy does not waive a failed contract metric. The compiler can
use proxies for search, but final acceptance is based on the contract.

## 6.11 Stage I — Certificate generation

The compiler emits:

- hashes of reference and candidate artifacts;
- full encoding and overhead accounting;
- contract and evidence versions;
- behavioral results with uncertainty;
- formal proof objects or verifier logs where applicable;
- resource measurements and hardware details;
- known failure regions;
- routing and fallback behavior;
- expiration and recertification triggers.

The certificate is discussed in Section 8 and exemplified in Appendix C.

## 6.12 Reference pseudocode

``` text
FUNCTION CompilePrecision(reference M, contract C, platform H, code_family Z):
    M0, transform_log = Canonicalize(M)
    ASSERT ReferenceEquivalent(M, M0, C.reference_tolerance)

    probes = InstrumentContract(C)
    sensitivity = EstimateFunctionalSensitivity(M0, probes, C)
    candidates = GenerateTransformsAndCodes(M0, sensitivity, Z, H)

    accepted_levels = []
    FOR candidate IN SearchByEstimatedBenefit(candidates):
        artifact = Encode(candidate)
        proxy = EvaluateProxies(M0, artifact, probes.calibration)
        IF proxy fails search thresholds:
            CONTINUE

        evidence = EvaluateContract(M, artifact, C, probes.validation, H)
        IF evidence satisfies level-specific constraints:
            accepted_levels.append((artifact, evidence))

    levels = SelectNestedParetoSet(accepted_levels)
    router = TrainConservativeRouter(levels, C)
    routed_evidence = EvaluateRoutedSystem(levels, router, C, H)

    status = DecideCertificateStatus(routed_evidence, C)
    certificate = BuildCertificate(
        reference=M,
        levels=levels,
        router=router,
        transform_log=transform_log,
        evidence=routed_evidence,
        status=status
    )
    RETURN levels, router, certificate
```

This pseudocode deliberately separates search proxies from acceptance
evidence and calibration data from validation data.

# 7. Progressive Executable Precision

## 7.1 Why one fixed width is the wrong default

Uniform bit width is operationally simple, but it assumes that every
component and every query has equal sensitivity. Existing
mixed-precision and outlier-aware methods already contradict this
assumption. A contract-based system extends nonuniformity across both
model structure and runtime context.

Define a **precision field**

$$
b:
(j,x,h,\mathcal{C})\mapsto q,
$$

where $j$ is a model component, $x$ the current input, $h$ internal or
trajectory state, and $q$ an encoding or execution level. Static mixed
precision is the special case $b(j)$; dynamic precision is the general
case.

## 7.2 Nested model levels

A progressive model contains levels

$$
M^{(0)},M^{(1)},\ldots,M^{(K)}
$$

with cumulative descriptions

$$
z^{(k)}=z^{(0)}\oplus r^{(1)}\oplus\cdots\oplus r^{(k)}.
$$

Ideally, each level provides nonincreasing distortion:

$$
D_{\mathcal{C}}(M,M^{(k+1)})
\leq
D_{\mathcal{C}}(M,M^{(k)}).
$$

However, numeric refinement does not guarantee monotonic improvement in
every discrete behavior. A new bit plane can change a tie, refusal
boundary, or routing state in either direction. Monotonicity must
therefore be a training objective or an empirically verified property,
not an assumption.

A multi-objective nesting loss can be

$$
\mathcal{L}
=
\sum_{k=0}^{K}
\omega_k
D_{\mathcal{C}}(M,M^{(k)})
+
\gamma
\sum_{k=0}^{K-1}
\max\!\left(
0,
D_{\mathcal{C}}(M,M^{(k+1)})
-
D_{\mathcal{C}}(M,M^{(k)})
\right)
$$

The second term penalizes measured regressions at higher precision. This
does not prove monotonicity outside the evaluation domain, but it makes
the desired structure explicit.

## 7.3 Forms of residual precision

Residual precision can take several forms.

| Residual form                       | Strength                              | Cost or risk                               |
|-------------------------------------|---------------------------------------|--------------------------------------------|
| **Additional bit planes**           | Simple nested arithmetic              | Low bits may be poorly ordered by behavior |
| **Sparse exceptions**               | Protects outliers and rare circuits   | Index and branch overhead                  |
| **Low-rank residuals**              | Efficient for correlated error        | May miss localized exceptions              |
| **Additive codebooks**              | Strong very-low-bit reconstruction    | Decoder and lookup complexity              |
| **Protected full-precision blocks** | Simple assurance boundary             | Coarse granularity                         |
| **Task adapters**                   | Context-specific correction           | Router and version complexity              |
| **External exact tools**            | Exact arithmetic or symbolic behavior | Tool latency and trust boundary            |

A hybrid is likely. For example, a ternary base may use block scales,
sparse 8- or 16-bit outliers, and a small high-precision adapter for
safety-critical behavior.

## 7.4 Precision escalation as metareasoning

A dynamic system should spend precision where the expected value of
refinement exceeds its cost. Let $V_k(s)$ be the expected
contract-relevant value at state $s$ when executing level $k$, and
$C_k(s)$ its physical cost. Escalate from $k$ to $k+1$ when

$$
\mathbb{E}
\left[
V_{k+1}(s)-V_k(s)
\mid\mathcal{I}_s
\right]
>
\lambda
\left(
C_{k+1}(s)-C_k(s)
\right),
$$

subject to hard protected constraints. Here $\mathcal{I}_s$ is the
information available to the router.

This resembles metareasoning: the system decides whether additional
computation is worth purchasing. Precision becomes one resource among
depth, samples, tools, retrieval, search, and human escalation.

## 7.5 Safe low-precision operation

A low-precision level should not be certified solely because its average
behavior is close to the reference. It also needs an explicit **safe
operating envelope**. The envelope can be defined by:

- input-domain membership;
- decision margin above a threshold;
- bounded activation or accumulator ranges;
- agreement among low-cost replicas;
- absence of protected-topic triggers;
- a local verification result;
- calibrated router confidence.

Outside the envelope, the contract can require higher precision, a
different model, an exact tool, abstention, or human review.

This design changes the question from “Can the entire model run at 2
bits?” to “For which states is the 2-bit implementation qualified, and
what catches the rest?”

## 7.6 Relationship to any-precision systems

Any-Precision LLM, Matryoshka Quantization, and MatGPTQ provide concrete
evidence that one checkpoint can support several nested bit widths
\[39\], \[40\], \[41\]. Their primary objectives are quality and
deployment efficiency across bit-width choices. A Precision Contract
layer would add:

- protected-behavior metrics for every level;
- level-specific admissible domains;
- a certified escalation router;
- complete overhead accounting;
- expiry and drift triggers;
- a proof or test manifest tied to exact artifacts.

The relationship is complementary: multi-precision training supplies
representations; the contract supplies qualification and control.

## 7.7 Precision should coexist with other adaptive resources

An advanced system may choose among:

- more weight precision;
- more activation or accumulator precision;
- additional decoding samples;
- a longer reasoning trace;
- retrieval or external memory;
- a theorem prover or calculator;
- a larger specialist model;
- human review.

These resources can substitute for one another. A low-bit model plus an
exact calculator may outperform a high-precision model on arithmetic. A
high-precision model without sufficient context may still fail. The
broader optimization is therefore

$$
\min_{a\in\mathcal{A}_{\mathrm{resources}}}
\operatorname{Cost}(a)
\quad
\text{subject to}
\quad
\operatorname{SAT}(\mathcal{C},M_a)=1.
$$

Functional precision is one axis in a larger architecture of adaptive
computation.

# 8. Verification, Certification, and Assurance Bits

## 8.1 Compression is a program transformation

A quantized network is not merely a smaller file containing
approximately the same real numbers. It is a new executable program with
discrete arithmetic, clipping, rounding, saturation, codebook lookups,
and kernel-specific accumulation. Formal work has shown that ignoring
these semantics can lead to incorrect conclusions about robustness and
correctness \[8\], \[9\]. Quantization-aware certification methods exist
precisely because properties of the idealized real-valued model may fail
after conversion \[10\], \[11\], \[42\].

The Precision Contract therefore adopts a simple rule:

> **No protected property transfers by presumption. It transfers only
> through evidence tied to the exact candidate implementation.**

Evidence may be a formal refinement proof, a verified error bound strong
enough to imply the property, exhaustive enumeration on a finite domain,
statistical testing, or a documented combination. The evidence class
must match the claim.

## 8.2 Four classes of bits

A deployment package contains more than parameter values. Define

$$
B_{\mathrm{total}}
=
B_{\mathrm{representational}}
+B_{\mathrm{structural}}
+B_{\mathrm{residual}}
+B_{\mathrm{assurance}}.
$$

### Representational bits

These encode ordinary weight or activation values: integer indices,
floating-point fields, signs, exponents, and base bit planes.

### Structural bits

These encode how values are interpreted: shapes, codebooks, scales,
sparse indices, permutations, rotations, low-rank factors, block
boundaries, and routing tables.

### Residual bits

These encode deviations not captured by the base representation: sparse
outliers, additive corrections, precision planes, protected adapters, or
fallback modules.

### Assurance bits

These encode evidence and identity: hashes, manifests, contract text,
dataset identifiers, test results, proof objects, verifier
configurations, exception lists, and expiry rules.

Assurance also has a computational cost:

$$
C_{\mathrm{assurance}}
=
C_{\mathrm{testing}}
+C_{\mathrm{verification}}
+C_{\mathrm{review}}
+C_{\mathrm{monitoring}}.
$$

For a high-consequence deployment, the smallest acceptable model may not
minimize $B_{\mathrm{representational}}$ alone. A regular representation
that is easier to verify can minimize total lifecycle cost.

## 8.3 Certificate statuses

A precision certificate should use statuses with defined semantics.

| Status                | Meaning                                                                                                     |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| **CERTIFIED**         | All mandatory contract clauses are satisfied with the specified evidence class and coverage                 |
| **PROVISIONAL**       | Empirical evidence meets thresholds, but a required formal, drift, or platform condition remains incomplete |
| **DOMAIN_RESTRICTED** | The artifact is qualified only inside a named operating envelope and must escalate outside it               |
| **UNSAT**             | At least one mandatory contract clause failed                                                               |
| **UNVERIFIED**        | Evidence was not generated, is stale, or does not correspond to the exact artifact                          |
| **REVOKED**           | Later evidence, drift, or an implementation change invalidated a previous certificate                       |

“Certified” must never be presented without the contract scope. It is
not a universal declaration that the model is safe or equivalent.

## 8.4 Certificate contents

A machine-readable certificate should include:

``` text
identity
  reference_artifact_hash
  candidate_artifact_hash
  decoder_and_kernel_hashes
  tokenizer_and_sampler_hashes

contract
  contract_id
  contract_version
  deployment_domain
  protected_behaviors
  metrics_and_thresholds
  evidence_requirements
  resource_requirements
  escalation_policy

representation
  nominal_weight_formats
  activation_and_accumulator_formats
  codebooks_scales_and_sparse_overhead
  residual_levels
  complete_bit_accounting

verification
  empirical_suites
  formal_properties_and_regions
  confidence_intervals
  adversarial_searches
  router_coverage
  hardware_measurements

limitations
  known_failures
  unsupported_domains
  unresolved_assumptions

lifecycle
  issued_at
  expires_at
  drift_triggers
  revocation_status
  signer_or_attestation
```

Appendix C provides an illustrative YAML instance.

## 8.5 Evidence hierarchy

Evidence strength is property-specific. A useful hierarchy is:

1.  **Exact proof or exhaustive check** over the complete declared
    domain;
2.  **Sound formal bound** over a defined region;
3.  **High-coverage adversarial and stress testing** with statistical
    guarantees;
4.  **Held-out distributional evaluation** with uncertainty intervals;
5.  **Calibration-set reconstruction metrics**;
6.  **Nominal bit width or tensor error alone**.

Lower levels can guide search but should not be described as proving
higher-level claims. For example, low mean-squared weight error is not
evidence that refusal behavior, control stability, or fairness
constraints are preserved.

## 8.6 Formal refinement as the ideal case

Suppose the reference model satisfies property $\varphi$ with margin
$m(x)$, and a verifier proves

$$
\|M_\theta(x)-\widehat{M}_z(x)\|\leq \delta(x)
$$

for all $x$ in region $\mathcal{X}$. If the property’s decision margin
obeys

$$
\delta(x)<m(x)
\quad\forall x\in\mathcal{X},
$$

then the property can transfer to the candidate on that region. This is
a refinement argument: bound the implementation difference tightly
enough that the protected predicate cannot change.

For large generative models, complete formal verification is currently
beyond reach. The principle still guides modular assurance. Small safety
monitors, numerical kernels, routers, constrained decoders, and
high-consequence submodules may be verifiable even when the whole model
is not.

## 8.7 Continuous monitoring and revocation

A static certificate can become stale as deployment changes. Monitoring
should estimate:

- input-distribution drift;
- increase in router escalation or low-confidence cases;
- changes in disagreement between precision levels;
- new failure clusters;
- hardware or kernel revisions;
- changes in external tools and retrieval;
- adversarial adaptation.

A practical trigger can be based on a divergence statistic

$$
D(P_{\mathrm{current}},P_{\mathrm{cert}})>\tau_{\mathrm{drift}},
$$

or on a rise in contract violations beyond a sequential confidence
boundary. Crossing a trigger changes the status to `PROVISIONAL`,
`UNVERIFIED`, or `REVOKED` until recertification.

# 9. Experimental and Falsification Program

The paper’s strongest claims are conceptual, but its usefulness depends
on empirical tests. This section specifies a program designed to
distinguish the Precision Contract from ordinary quantization
evaluation.

## 9.1 Research questions

The experiments should answer:

- **RQ1:** Does canonicalization reduce arbitrary differences in
  quantization outcomes among functionally identical parameterizations?
- **RQ2:** Do contract-aware metrics predict deployment-relevant
  degradation better than weight reconstruction error or perplexity
  alone?
- **RQ3:** Does complete bit accounting change the Pareto ranking of
  compression methods?
- **RQ4:** Can progressive residuals provide better behavioral benefit
  per bit than uniform higher precision?
- **RQ5:** Can a conservative precision router reduce expected cost
  without increasing contract violations?
- **RQ6:** Can precision certificates detect failures hidden by
  aggregate benchmark retention?
- **RQ7:** How stable are the learned precision allocations under
  calibration shift, threat-model change, and long-horizon execution?

## 9.2 Model and task suite

A credible evaluation should span several model classes because the
framework claims generality:

1.  **Image classifier.** Enables exact or strong formal verification on
    small networks and controlled reparameterization.
2.  **Scientific surrogate or controller.** Tests numerical invariants,
    trajectory error, and stability.
3.  **Language model.** Tests perplexity, token distribution,
    instruction following, reasoning, safety, and tool use.
4.  **Tool-using agent.** Tests long-horizon route changes, recovery,
    and external exact computation.
5.  **Synthetic exact task.** Arithmetic, automata, or formal
    verification tasks that expose the limits of the “noisy world
    implies low precision” intuition.

For language models, include several sizes and architectures, and
evaluate at least uniform 8-, 4-, 3-, and 2-bit baselines where
technically supported. Include modern PTQ, mixed-precision,
outlier-aware, and codebook methods rather than comparing only to naïve
rounding.

## 9.3 Experiment 1 — Reparameterization stress test

### Design

Construct a family of exactly equivalent networks $\{M_{\theta_c}\}$
using positive rescaling, neuron permutations, factorization, and
normalization transformations. Confirm functional identity in the
reference format. Quantize every member with the same nominal method and
calibration data.

Compare:

- naïve quantization;
- quantization after standardized canonicalization;
- a reparameterization-aware method;
- contract-aware allocation.

### Metrics

- candidate accuracy or task utility;
- output KL and decision disagreement;
- worst-case property violations;
- allocated bits by component;
- variance of outcomes across equivalent parameterizations.

### Hypothesis

Canonicalization should reduce outcome variance and produce more stable
allocations.

### Falsifier

If equivalent parameterizations quantize equally well without
canonicalization across architectures and bit widths, the proposed
compiler stage has little empirical value. If canonicalization
systematically harms the best achievable rate–distortion frontier, it
should be optional rather than foundational.

## 9.4 Experiment 2 — Parameter distance versus behavioral distance

### Design

Generate candidate models with matched Frobenius weight error or matched
layerwise reconstruction error but different perturbation directions.
Include perturbations aligned with high- and low-sensitivity
eigenspaces, random directions, outlier channels, and protected behavior
circuits.

Test whether

$$
\|\theta-\widehat\theta_1\|
\approx
\|\theta-\widehat\theta_2\|
$$

while

$$
D_{\mathcal{C}}(M_\theta,M_{\widehat\theta_1})
\not\approx
D_{\mathcal{C}}(M_\theta,M_{\widehat\theta_2}).
$$

### Hypothesis

Weight-space error will be weakly associated with at least some
contract-critical behaviors after controlling for aggregate accuracy.

### Falsifier

If simple reconstruction error consistently predicts all protected
metrics as well as contract-aware sensitivity, the additional framework
may not justify its complexity for that domain.

## 9.5 Experiment 3 — Complete rate–distortion accounting

### Design

For each compression method, report two storage measures:

1.  nominal average bits per original weight;
2.  complete executable bits, including scales, zeros, codebooks, sparse
    indices, transforms, routing, residuals, decoder additions, and
    certificates.

Measure actual bytes on disk, peak memory, bytes transferred per token
or inference, latency, and energy where possible.

### Hypothesis

Some methods that appear superior under nominal bits per weight will
move backward on the complete Pareto frontier.

### Falsifier

If overhead is negligible and rankings never change, complete accounting
remains conceptually correct but has limited practical impact for the
evaluated systems.

## 9.6 Experiment 4 — Progressive residual curves

### Design

Compile a base model and $K$ ordered residuals. Compare against
independent uniform bit-width models at matched complete size. Plot, for
every contract metric,

$$
D_j(k)
\quad\text{versus}\quad
B_{\mathrm{total}}(k).
$$

Evaluate alternative residual orderings:

- numeric significance;
- residual magnitude;
- Hessian salience;
- contract benefit per bit;
- random ordering.

### Hypothesis

Contract-ordered residuals will restore protected behavior faster per
added bit than magnitude- or numeric-order baselines.

### Falsifier

If residual ordering gives no consistent gain, a simple fixed-width
checkpoint may be preferable. If higher levels frequently regress
protected metrics, progressive execution requires stronger co-training
or should be rejected for those behaviors.

## 9.7 Experiment 5 — Aggregate equivalence illusion

### Design

Select compressed candidates with closely matched perplexity, average
accuracy, or reward. Compare them at the instance and behavior level
using:

- decision agreement;
- conditional agreement on rare slices;
- logit or probability divergence;
- calibration;
- reasoning-path and tool-call changes;
- refusal and safety behavior;
- consistency under paraphrase;
- long-context and multilingual performance;
- high-consequence error sets.

Recent studies motivate this experiment by reporting disagreement or
reliability shifts that broad metrics can conceal \[45\], \[46\],
\[47\].

### Hypothesis

At least some candidates with similar aggregate scores will differ
materially on protected behavior.

### Falsifier

If aggregate metrics consistently upper-bound all contract-relevant
differences across broad model and task families, a multi-metric
contract adds little predictive value.

## 9.8 Experiment 6 — Static versus contract-routed precision

### Baselines

- uniform 4-bit;
- uniform 8-bit;
- static mixed precision;
- dynamic routing by generic confidence;
- contract-conditioned routing;
- full-precision reference;
- oracle router using post hoc knowledge.

### Metrics

- expected bytes moved and latency;
- tail latency;
- contract violation rate;
- escalation frequency;
- false-negative rate of the router;
- calibration of escalation confidence;
- resource cost under distribution shift.

### Hypothesis

A conservative contract router will approach the oracle cost while
remaining within the violation threshold and outperforming generic
confidence routing on protected cases.

### Falsifier

If router errors erase the resource gain or increase protected failures,
fixed precision is safer. This is an important possible result, not a
reason to redefine success.

## 9.9 Experiment 7 — Certificate discrimination

### Design

Create candidates that each pass one proxy but fail another:

- low tensor error but poor decision agreement;
- preserved perplexity but degraded safety;
- preserved average accuracy but failed rare-slice property;
- good software simulation but overflow on target hardware;
- good individual levels but unsafe router;
- passed test suite but failed formal counterexample.

The certificate generator should classify these as `UNSAT`,
`DOMAIN_RESTRICTED`, or `PROVISIONAL` according to the declared evidence
rules.

### Hypothesis

The contract prevents misleading equivalence claims that would pass
conventional reporting.

### Falsifier

If the certificate merely restates benchmark scores and fails to
discriminate constructed counterexamples, it is bureaucratic overhead
rather than assurance.

## 9.10 Experiment 8 — Distribution shift and rare-event stress

### Design

Vary calibration and deployment distributions along controlled axes:
prompt length, language, domain, activation scale, sensor noise,
environment dynamics, and adversarial behavior. Track whether
sensitivity rankings and bit allocations remain stable.

Measure rank correlation of component salience and changes in optimal
allocation. Evaluate whether drift monitors trigger before protected
failures rise.

### Hypothesis

Contract-aware calibration across protected strata will be more stable
than random calibration, but no static allocation will be universally
robust.

### Falsifier

If salience and optimal precision are nearly invariant across broad
shifts, dynamic contracts may be unnecessary. If drift detection
consistently lags failures, certificates must use narrower domains or
more conservative fallbacks.

## 9.11 Reporting standard

Every experimental result should report:

- exact reference and candidate hashes;
- complete numerical formats for weights, activations, accumulators, and
  KV state;
- group sizes, scales, codebooks, sparse overhead, and kernel versions;
- calibration and validation data separation;
- sampling and decoding settings;
- all contract metrics, not only passing ones;
- confidence intervals and multiple-testing treatment;
- actual storage and hardware measurements;
- known failures and unsupported regions;
- whether a source is peer-reviewed or a preprint.

This reporting discipline is itself part of the proposed contribution.

# 10. Implications for Advanced AI Systems

## 10.1 Intelligence is not a uniform array of real numbers

The framework challenges a common mental model: that a trained AI is
fundamentally a fixed list of independent real-valued weights. In
practice, a model is an executable information structure composed of
repeated patterns, symmetries, low-rank directions, sparse exceptions,
algorithms, context, and external resources. The functional information
content of a system is closer to the number of behaviorally
distinguishable implementations at tolerance $\varepsilon$ than to
parameter count times nominal bit width.

Let $\mathcal{N}_{\mathcal{C}}(\varepsilon)$ be a covering number of
behavior space under the contract metric. A conceptual functional
information quantity is

$$
I_{\mathrm{functional}}(\mathcal{C},\varepsilon)
=
\log_2 \mathcal{N}_{\mathcal{C}}(\varepsilon).
$$

This is not directly computable for frontier systems, but it identifies
the right object: distinguishable behavior under a specified tolerance.

## 10.2 Precision becomes a governed resource

Advanced systems already allocate compute through model routing,
retrieval, search depth, sampling, and tool use. Precision can become
another governed resource. A routine, high-margin decision may use a
low-bit base. A close medical decision, unstable control state, or
formal proof step may escalate to higher precision or an exact tool.

The governing principle is:

$$
\text{purchase additional precision only when it changes a protected decision or reduces certified risk enough to justify its cost.}
$$

This principle is compatible with high precision where necessary. The
framework is not an ideological argument for low-bit computation; it is
an argument against unexamined uniform precision.

## 10.3 Progressive residuals can separate common structure from exceptional fidelity

A base-and-residual architecture suggests a division of labor:

- the base carries broadly reusable structure;
- residual planes carry task-, domain-, or risk-specific distinctions;
- protected modules retain precision for fragile behaviors;
- routing decides which distinctions must be materialized now.

This can support devices with different budgets, degraded operation
under resource loss, auditable updates to a small residual instead of an
entire model, and precise localization of which bits preserve a
capability.

## 10.4 Assurance must scale with capability and consequence

As model capability increases, average benchmark retention becomes less
adequate as evidence. Advanced systems can take long-horizon actions,
invoke tools, write code, and affect physical or institutional
processes. Small distributional changes may alter which action sequence
is selected even when average token metrics remain stable.

A precision certificate cannot solve general AI safety. It can enforce a
narrower but important discipline: numerical compression must not
silently inherit claims from a different executable artifact. Protected
behaviors, assumptions, and residual uncertainty must travel with the
implementation.

## 10.5 The framework avoids a false metaphysical conclusion

It is tempting to say that bits below physical measurement precision are
“fiction.” That phrase is too strong. Mathematical models can encode
exact abstractions, algorithms, counterfactuals, and stabilizing
numerical structure that do not correspond one-to-one with measured
digits. What matters operationally is whether the extra representation
changes behavior under the contract.

The appropriate conclusion is therefore not that the real world has a
universal precision. It is that **every claimed precision requirement
should be paid for by a demonstrated functional distinction**.

# 11. Limitations and Open Problems

## 11.1 Contract incompleteness

No finite contract captures every desirable behavior. A compressed model
can satisfy all listed tests and still fail in an unmodeled way. This is
the framework’s central governance risk: optimizing to the contract can
become specification gaming. Contracts need adversarial review,
versioning, broad monitoring, and explicit unknowns.

## 11.2 Distribution dependence

Empirical rate–distortion is conditional on the evaluation distribution.
A model compressed for one domain may fail under another. Even a precise
deployment distribution can drift. The paper does not provide a
universal method for selecting representative data.

## 11.3 Verification scalability

Bit-exact formal verification is computationally difficult, and current
methods scale only to limited architectures and properties \[9\],
\[42\]. Large generative models will rely heavily on statistical
evidence, modular proofs, monitors, and conservative fallbacks. A
`CERTIFIED` label must therefore specify the evidence class and scope.

## 11.4 Decoder and side-information dependence

Description length depends on what is shared. A large codebook,
compiler, pretrained generator, or external library can make the
candidate file appear small while moving complexity outside the
boundary. The framework requires explicit accounting but cannot impose
one universally correct boundary.

## 11.5 Hardware dependence

The representation that minimizes stored bits may not minimize energy or
latency. Irregular encodings, bit unpacking, sparse access, and
precision routing can lose to regular higher-bit kernels. Physical cost
must be measured on target hardware.

## 11.6 Nonlocal and discontinuous behavior

Local Hessian or Jacobian metrics can miss discrete transitions, rare
events, and long-horizon amplification. The compiler architecture
includes end-to-end validation for this reason, but efficient search
remains an open problem.

## 11.7 Reference-model fallibility

Behavioral fidelity to a reference is not the same as correctness,
safety, or truth. The contract must include external properties where
appropriate. A perfectly compressed unsafe model remains unsafe.

## 11.8 Assurance cost may dominate

For high-consequence systems, generating evidence can cost more than
storing extra model bits. The minimum total-cost solution may
deliberately use a more regular, higher-precision representation because
it is easier to analyze and maintain.

## 11.9 Adaptive routing adds attack surface

An adversary may target the precision router, force expensive
escalation, or shape inputs so that low precision is selected in a
fragile state. Router robustness and denial-of-service cost belong in
the threat model.

## 11.10 Precision is only one form of computational fidelity

Context truncation, retrieval errors, sampling, approximate attention,
speculative decoding, pruning, distillation, caching, and tool failures
can dominate weight quantization error. A complete systems contract
should eventually cover all approximate transformations, not precision
alone.

## 11.11 The exact optimum is not computable in practice

The functional rate $R^{\star}$ is an ideal target. Searching all
architectures and codes is impossible. Reported results will be upper
bounds achieved by particular compiler families, not proofs of globally
minimal intelligence descriptions.

## 11.12 Open research questions

Promising directions include:

- canonicalization methods optimized for both quantization and
  verification;
- behavioral metrics that remain meaningful for open-ended generation;
- scalable formal refinement between transformer implementations;
- residual codes ordered by causal or contract benefit rather than
  magnitude;
- conservative precision routers with provable risk bounds;
- joint allocation of weight, activation, accumulator, KV-cache, and
  context precision;
- certificate standards interoperable across compilers and hardware;
- rate–distortion theory for interactive agents and trajectory
  distributions;
- lifecycle recertification under continual learning and model editing;
- methods for measuring assurance-generation cost alongside inference
  cost.

# 12. Conclusion

The search for a universal upper bound on the precision of an AI weight
begins with a sound intuition: there must be a point beyond which
additional numerical detail no longer improves a real system. The error
lies in assigning that point to an individual parameter independently of
representation, task, and behavior.

Neural weights are coordinates, not natural observables. Exact rescaling
can make them arbitrarily large or small. High precision can be
distributed across many low-bit fields. Large dynamic range does not
imply a uniformly wide significand. Global physical information bounds
constrain complete physical systems, not one software field. Measurement
noise does not, by itself, determine algorithmic precision.

The paper therefore replaces a cosmic per-weight ceiling with a
contract-relative optimization:

$$
\boxed{
R^{\star}(M,\mathcal{C})
=
\min_{z}
\left\{
L(z):
\operatorname{SAT}(\mathcal{C},\mathsf{Dec}(z))=1
\right\}
}
$$

The quantity asks for the shortest complete executable description that
preserves declared behavior. It counts values, structure, residuals,
routing, decoder assumptions, and assurance evidence. It permits
nonuniform and dynamic precision. It treats quantization as a program
transformation requiring its own evaluation or verification. It produces
not only a smaller model but a qualified implementation with a defined
operating envelope and escalation policy.

The proposed Precision Contract, Functional Precision Compiler,
progressive residual architecture, and certificate are research
proposals rather than completed infrastructure. Their value is testable.
Canonicalization should reduce arbitrary reparameterization effects.
Contract-aware metrics should reveal failures hidden by reconstruction
error or aggregate accuracy. Progressive residuals should deliver
measurable behavioral benefit per bit. Routing should reduce cost
without increasing protected violations. Certificates should reject
constructed cases that conventional reporting would mistakenly accept.
Where these hypotheses fail, the framework should be narrowed or
abandoned.

The deepest conclusion is simple:

> **Useful precision is not the number of digits stored in a weight. It
> is the minimum physical description needed to preserve the behavioral
> distinctions a system is obligated to make.**

That formulation does not tell every model to use fewer bits. It tells
every extra bit to justify itself through behavior.

------------------------------------------------------------------------

# Appendix A. Notation

| Symbol          | Meaning                                         |
|-----------------|-------------------------------------------------|
| $M_\theta$      | Reference AI system                             |
| $z$             | Finite binary description of a candidate        |
| $\mathsf{Dec}$  | Decoder or execution semantics                  |
| $\widehat{M}_z$ | Candidate executable implementation             |
| $\mathcal{C}$   | Precision contract                              |
| $\mathcal{D}$   | Deployment domain or distribution specification |
| $\mathcal{B}$   | Protected behaviors or properties               |
| $D_j$           | Contract-relevant distortion metric             |
| $\varepsilon_j$ | Acceptance threshold for metric $j$             |
| $L(z)$          | Complete description length in bits             |
| $R^{\star}$     | Minimum contract-satisfying description length  |
| $F$             | Positive-semidefinite local sensitivity matrix  |
| $\Delta_j$      | Quantization step in transformed direction $j$  |
| $M^{(k)}$       | Cumulative precision level $k$                  |
| $R^{(k)}$       | Residual refinement $k$                         |
| $\pi$           | Precision routing policy                        |
| $\mathsf{Cert}$ | Precision certificate and evidence manifest     |

# Appendix B. Illustrative Precision Contract

The following example is intentionally generic. Thresholds are
placeholders and must be justified for a real deployment.

``` yaml
precision_contract:
  id: "pc-example-001"
  version: "1.0"
  issued_for: "candidate artifact hash supplied at compilation"

  system_boundary:
    includes:
      - model weights
      - tokenizer
      - prompt template
      - sampling configuration
      - quantization decoder and kernels
      - precision router
    excludes:
      - external retrieval corpus
      - human review process

  reference:
    artifact_hash: "sha256:REFERENCE"
    software_environment: "container digest"
    deterministic_mode: false

  deployment_domain:
    distributions:
      - name: "ordinary_requests"
        dataset_manifest: "manifest:ordinary-v3"
      - name: "protected_safety_requests"
        dataset_manifest: "manifest:safety-v5"
    unsupported:
      - "languages not listed in manifest"
      - "context lengths above tested limit"

  protected_behaviors:
    - id: "output_fidelity"
      metric: "mean token KL(reference || candidate)"
      threshold: 0.001
      aggregation: "upper 95% confidence bound"

    - id: "decision_agreement"
      metric: "tool-choice disagreement"
      threshold: 0.002
      aggregation: "maximum across protected task strata"

    - id: "safety"
      metric: "unsafe completion rate"
      threshold: 0.0005
      aggregation: "one-sided 99% upper confidence bound"
      no_tradeoff: true

    - id: "router_false_negative"
      metric: "fragile case accepted at base precision"
      threshold: 0.0001
      aggregation: "one-sided 99% upper confidence bound"

  resources:
    target_hardware: "platform and firmware hash"
    max_peak_memory_gib: 8.0
    max_p95_latency_ms: 250
    objective: "minimize measured bytes moved per generated token"

  precision_levels:
    base:
      allowed_domain: "ordinary_requests with router confidence >= 0.995"
    high:
      allowed_domain: "all certified domains"
    fallback:
      behavior: "abstain or invoke full reference service"

  evidence:
    independent_validation_required: true
    required_seeds: 5
    adversarial_search_required: true
    formal_properties:
      - "integer accumulator cannot overflow within certified activation bounds"
    expiry_days: 90

  status_rules:
    certified: "all mandatory clauses pass"
    domain_restricted: "base level passes only inside declared envelope"
    provisional: "statistical clauses pass but formal clause pending"
    unsat: "any no_tradeoff clause fails"
```

# Appendix C. Illustrative Precision Certificate

``` yaml
precision_certificate:
  certificate_id: "pcc-example-001"
  status: "DOMAIN_RESTRICTED"
  issued_at: "2026-07-24T00:00:00Z"
  expires_at: "2026-10-22T00:00:00Z"

  identity:
    reference_hash: "sha256:REFERENCE"
    candidate_base_hash: "sha256:BASE"
    residual_level_1_hash: "sha256:R1"
    router_hash: "sha256:ROUTER"
    decoder_hash: "sha256:DECODER"
    platform_hash: "sha256:PLATFORM"

  representation:
    base_weight_format: "grouped ternary with 16-bit block scales"
    activation_format: "int8 with protected fp16 operations"
    accumulator_format: "int32"
    residuals:
      - "sparse 8-bit exception map"
      - "protected fp16 adapter"
    storage_bits:
      representational: 1000000000
      structural: 42000000
      residual: 87000000
      routing: 8000000
      assurance: 3000000
      total: 1140000000

  evidence_summary:
    output_fidelity:
      result: 0.00074
      threshold: 0.001
      outcome: "PASS"
    decision_agreement:
      result: 0.0016
      threshold: 0.002
      outcome: "PASS"
    safety:
      result_upper_bound: 0.00042
      threshold: 0.0005
      outcome: "PASS"
    router_false_negative:
      result_upper_bound: 0.00008
      threshold: 0.0001
      outcome: "PASS"
    accumulator_overflow:
      verified_region: "activation bounds manifest:ab-17"
      outcome: "PROVED"

  operating_envelope:
    base_level:
      - "router confidence >= 0.995"
      - "context length <= certified maximum"
      - "input belongs to certified language set"
    outside_envelope: "load residual level 1 or invoke fallback"

  known_limitations:
    - "No formal proof of semantic safety for the generative model"
    - "Rare-event estimates remain statistical"
    - "Retrieval corpus changes require recertification"

  revocation_triggers:
    - "any artifact hash changes"
    - "drift statistic exceeds threshold"
    - "protected violation confidence bound exceeds contract"
```

# Appendix D. Proof and Interpretation Notes

## D.1 Why Proposition 1 concerns magnitude but also undermines raw precision claims

The exact rescaling proof directly shows that magnitude is noninvariant.
Precision sensitivity follows because quantization error is evaluated
relative to the scale and role of the parameter. Under a fixed absolute
step size, rescaling changes relative error. Under a fixed relative
format, compensating layers and activation ranges change. Therefore, a
statement about the number of meaningful digits in one raw weight cannot
be interpreted without the complete reparameterization and execution
semantics.

## D.2 Why $R^{\star}$ is not “the number of bits in intelligence”

$R^{\star}$ is conditional on:

- the chosen reference behavior;
- the contract and tolerance;
- the deployment domain;
- the decoder and shared side information;
- the candidate architecture family;
- the required assurance evidence.

Changing any of these can change the optimum. The quantity is an
operational minimum under declared assumptions, not an
observer-independent metaphysical constant.

## D.3 Why extra bits can still matter below measurement uncertainty

A low-order bit may stabilize an iterative solver, preserve a
cancellation, maintain a decision margin, or encode an exact abstract
rule. The framework rejects the claim that such bits are automatically
fictional. It asks whether removing them causes a contract-relevant
difference. Physical measurement uncertainty informs the contract but
does not replace it.

## D.4 Why assurance is included in description length

MDL-style quantities normally count the representation needed to
reconstruct an object, not the evidence used to trust it. This paper
deliberately extends the accounting boundary for deployment. The reason
is practical: an implementation that is one percent smaller but
impossible to qualify may be inferior to a regular, slightly larger
implementation with a compact proof. To avoid confusion, reports should
always separate representation length from assurance length and
assurance-generation compute.

# References

[1] M. Horowitz, “1.1 computing’s energy problem (and what we can do about it),” in *2014 IEEE international solid-state circuits conference digest of technical papers*, 2014, pp. 10–14. doi: [10.1109/ISSCC.2014.6757323](https://doi.org/10.1109/ISSCC.2014.6757323).

[2] V. Sze, Y.-H. Chen, T.-J. Yang, and J. S. Emer, “Efficient processing of deep neural networks: A tutorial and survey,” *Proceedings of the IEEE*, vol. 105, no. 12, pp. 2295–2329, 2017, doi: [10.1109/JPROC.2017.2761740](https://doi.org/10.1109/JPROC.2017.2761740).

[3] C. E. Shannon, “A mathematical theory of communication,” *Bell System Technical Journal*, vol. 27, no. 3–4, pp. 379–423, 623–656, 1948, doi: [10.1002/j.1538-7305.1948.tb01338.x](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x).

[4] C. E. Shannon, “Coding theorems for a discrete source with a fidelity criterion,” in *IRE national convention record*, 1959, pp. 142–163.

[5] R. M. Gray and D. L. Neuhoff, “Quantization,” *IEEE Transactions on Information Theory*, vol. 44, no. 6, pp. 2325–2383, 1998, doi: [10.1109/18.720541](https://doi.org/10.1109/18.720541).

[6] J. Rissanen, “Modeling by shortest data description,” *Automatica*, vol. 14, no. 5, pp. 465–471, 1978, doi: [10.1016/0005-1098(78)90005-5](https://doi.org/10.1016/0005-1098(78)90005-5).

[7] G. E. Hinton and D. van Camp, “Keeping the neural networks simple by minimizing the description length of the weights,” in *Proceedings of the sixth annual conference on computational learning theory*, 1993, pp. 5–13. doi: [10.1145/168304.168306](https://doi.org/10.1145/168304.168306).

[8] M. Giacobbe, T. A. Henzinger, and M. Lechner, “How many bits does it take to quantize your neural network?” in *Tools and algorithms for the construction and analysis of systems*, in Lecture notes in computer science, vol. 12079. 2020, pp. 79–97. doi: [10.1007/978-3-030-45237-7_5](https://doi.org/10.1007/978-3-030-45237-7_5).

[9] T. A. Henzinger, M. Lechner, and Đ. Žikelić, “Scalable verification of quantized neural networks,” in *Proceedings of the AAAI conference on artificial intelligence*, 2021, pp. 3787–3795. doi: [10.1609/aaai.v35i5.16496](https://doi.org/10.1609/aaai.v35i5.16496).

[10] M. Lechner, Đ. Žikelić, K. Chatterjee, T. A. Henzinger, and D. Rus, “Quantization-aware interval bound propagation for training certifiably robust quantized neural networks,” in *Proceedings of the AAAI conference on artificial intelligence*, 2023. doi: [10.1609/aaai.v37i12.26747](https://doi.org/10.1609/aaai.v37i12.26747).

[11] Y. Zhang, F. Song, and J. Sun, “QEBVerif: Quantization error bound verification of neural networks,” in *Computer aided verification*, in Lecture notes in computer science, vol. 13965. 2023, pp. 413–437. doi: [10.1007/978-3-031-37703-7_20](https://doi.org/10.1007/978-3-031-37703-7_20).

[12] D. Goldberg, “What every computer scientist should know about floating-point arithmetic,” *ACM Computing Surveys*, vol. 23, no. 1, pp. 5–48, 1991, doi: [10.1145/103162.103163](https://doi.org/10.1145/103162.103163).

[13] N. J. Higham, *Accuracy and stability of numerical algorithms*, 2nd ed. Philadelphia, PA: Society for Industrial; Applied Mathematics, 2002. doi: [10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027).

[14] L. Dinh, R. Pascanu, S. Bengio, and Y. Bengio, “Sharp minima can generalize for deep nets,” in *Proceedings of the 34th international conference on machine learning*, in Proceedings of machine learning research, vol. 70. 2017, pp. 1019–1028. Available: <https://proceedings.mlr.press/v70/dinh17b.html>

[15] B. Neyshabur, R. Salakhutdinov, and N. Srebro, “Path-SGD: Path-normalized optimization in deep neural networks,” in *Advances in neural information processing systems*, 2015, pp. 2422–2430. Available: <https://proceedings.neurips.cc/paper/2015/hash/eaa32c96f620053cf442ad32258076b9-Abstract.html>

[16] E. Meller, A. Finkelstein, U. Almog, and M. Grobman, “Same, same but different: Recovering neural network quantization error through weight factorization,” in *Proceedings of the 36th international conference on machine learning*, in Proceedings of machine learning research, vol. 97. 2019, pp. 4486–4495. Available: <https://proceedings.mlr.press/v97/meller19a.html>

[17] National Institute of Standards and Technology, “CODATA value: Planck length.” 2025. Available: <https://physics.nist.gov/cgi-bin/cuu/Value?plkl=>

[18] R. Bousso, “The holographic principle,” *Reviews of Modern Physics*, vol. 74, no. 3, pp. 825–874, 2002, doi: [10.1103/RevModPhys.74.825](https://doi.org/10.1103/RevModPhys.74.825).

[19] R. Landauer, “Irreversibility and heat generation in the computing process,” *IBM Journal of Research and Development*, vol. 5, no. 3, pp. 183–191, 1961, doi: [10.1147/rd.53.0183](https://doi.org/10.1147/rd.53.0183).

[20] S. Gupta, A. Agrawal, K. Gopalakrishnan, and P. Narayanan, “Deep learning with limited numerical precision,” in *Proceedings of the 32nd international conference on machine learning*, in Proceedings of machine learning research, vol. 37. 2015, pp. 1737–1746. Available: <https://proceedings.mlr.press/v37/gupta15.html>

[21] S. Han, H. Mao, and W. J. Dally, “Deep compression: Compressing deep neural networks with pruning, trained quantization and huffman coding,” in *International conference on learning representations*, 2016. Available: <https://arxiv.org/abs/1510.00149>

[22] M. Rastegari, V. Ordonez, J. Redmon, and A. Farhadi, “XNOR-net: ImageNet classification using binary convolutional neural networks,” in *Computer vision – ECCV 2016*, in Lecture notes in computer science, vol. 9908. 2016, pp. 525–542. doi: [10.1007/978-3-319-46493-0_32](https://doi.org/10.1007/978-3-319-46493-0_32).

[23] I. Hubara, M. Courbariaux, D. Soudry, R. El-Yaniv, and Y. Bengio, “Quantized neural networks: Training neural networks with low precision weights and activations,” *Journal of Machine Learning Research*, vol. 18, no. 187, pp. 1–30, 2018, Available: <https://jmlr.org/papers/v18/16-456.html>

[24] B. Jacob *et al.*, “Quantization and training of neural networks for efficient integer-arithmetic-only inference,” in *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, 2018, pp. 2704–2713. doi: [10.1109/CVPR.2018.00286](https://doi.org/10.1109/CVPR.2018.00286).

[25] P. Micikevicius *et al.*, “Mixed precision training,” in *International conference on learning representations*, 2018. Available: <https://openreview.net/forum?id=r1gs9JgRZ>

[26] T. Dettmers, M. Lewis, Y. Belkada, and L. Zettlemoyer, “LLM.int8(): 8-bit matrix multiplication for transformers at scale,” in *Advances in neural information processing systems*, 2022, pp. 30318–30332. Available: <https://proceedings.neurips.cc/paper_files/paper/2022/hash/c3ba4962c05c49636d4c6206a97e9c8a-Abstract-Conference.html>

[27] E. Frantar, S. Ashkboos, T. Hoefler, and D. Alistarh, “GPTQ: Accurate post-training quantization for generative pre-trained transformers,” in *International conference on learning representations*, 2023. Available: <https://openreview.net/forum?id=tcbBPnfwxS>

[28] G. Xiao, J. Lin, M. Seznec, H. Wu, J. Demouth, and S. Han, “SmoothQuant: Accurate and efficient post-training quantization for large language models,” in *Proceedings of the 40th international conference on machine learning*, in Proceedings of machine learning research, vol. 202. 2023, pp. 38087–38099. Available: <https://proceedings.mlr.press/v202/xiao23c.html>

[29] J. Lin *et al.*, “AWQ: Activation-aware weight quantization for on-device LLM compression and acceleration,” in *Proceedings of machine learning and systems*, 2024, pp. 87–100. Available: <https://proceedings.mlsys.org/paper_files/paper/2024/hash/42a452cbafa9dd64e9ba4aa95cc1ef21-Abstract-Conference.html>

[30] J. Chee, Y. Cai, V. Kuleshov, and C. D. Sa, “QuIP: 2-bit quantization of large language models with guarantees,” in *Advances in neural information processing systems*, 2023.

[31] A. Tseng, J. Chee, Q. Sun, V. Kuleshov, and C. D. Sa, “QuIP#: Even better LLM quantization with hadamard incoherence and lattice codebooks,” in *Proceedings of the 41st international conference on machine learning*, in Proceedings of machine learning research, vol. 235. 2024, pp. 48630–48656. Available: <https://proceedings.mlr.press/v235/tseng24a.html>

[32] V. Egiazarian, A. Panferov, D. Kuznedelev, E. Frantar, A. Babenko, and D. Alistarh, “Extreme compression of large language models via additive quantization,” in *Proceedings of the 41st international conference on machine learning*, in Proceedings of machine learning research, vol. 235. 2024, pp. 12284–12303. Available: <https://proceedings.mlr.press/v235/egiazarian24a.html>

[33] S. Ma *et al.*, “The era of 1-bit LLMs: All large language models are in 1.58 bits,” *arXiv preprint arXiv:2402.17764*, 2024, doi: [10.48550/arXiv.2402.17764](https://doi.org/10.48550/arXiv.2402.17764).

[34] Y. Xu *et al.*, “OneBit: Towards extremely low-bit large language models,” in *Advances in neural information processing systems*, 2024.

[35] Y. LeCun, J. S. Denker, and S. A. Solla, “Optimal brain damage,” in *Advances in neural information processing systems*, 1989, pp. 598–605.

[36] Z. Dong, Z. Yao, A. Gholami, M. W. Mahoney, and K. Keutzer, “HAWQ: Hessian AWare quantization of neural networks with mixed-precision,” in *Proceedings of the IEEE/CVF international conference on computer vision*, 2019, pp. 293–302. doi: [10.1109/ICCV.2019.00038](https://doi.org/10.1109/ICCV.2019.00038).

[37] Z. Dong, Z. Yao, D. Arfeen, A. Gholami, M. W. Mahoney, and K. Keutzer, “HAWQ-V2: Hessian aware trace-weighted quantization of neural networks,” in *Advances in neural information processing systems*, 2020, pp. 18518–18529. Available: <https://proceedings.neurips.cc/paper/2020/hash/d77c703536718b95308130ff2e5cf9ee-Abstract.html>

[38] M. Nagel, R. A. Amjad, M. van Baalen, C. Louizos, and T. Blankevoort, “Up or down? Adaptive rounding for post-training quantization,” in *Proceedings of the 37th international conference on machine learning*, in Proceedings of machine learning research, vol. 119. 2020, pp. 7197–7206. Available: <https://proceedings.mlr.press/v119/nagel20a.html>

[39] Y. Park, J. Hyun, S. Cho, B. Sim, and J. W. Lee, “Any-precision LLM: Low-cost deployment of multiple, different-sized LLMs,” in *Proceedings of the 41st international conference on machine learning*, in Proceedings of machine learning research, vol. 235. 2024, pp. 39682–39701. Available: <https://proceedings.mlr.press/v235/park24e.html>

[40] P. Nair, P. Datta, J. Dean, P. Jain, and A. Kusupati, “Matryoshka quantization,” *arXiv preprint arXiv:2502.06786*, 2025, doi: [10.48550/arXiv.2502.06786](https://doi.org/10.48550/arXiv.2502.06786).

[41] M. Kleinegger, E. Crnčević, and D. Alistarh, “MatGPTQ: Accurate and efficient post-training matryoshka quantization,” *arXiv preprint arXiv:2602.03537*, 2026, doi: [10.48550/arXiv.2602.03537](https://doi.org/10.48550/arXiv.2602.03537).

[42] P. Huang *et al.*, “Towards efficient verification of quantized neural networks,” in *Proceedings of the AAAI conference on artificial intelligence*, 2024. doi: [10.1609/aaai.v38i19.30108](https://doi.org/10.1609/aaai.v38i19.30108).

[43] J. Li, R. Drummond, and S. R. Duncan, “Robust error bounds for quantised and pruned neural networks,” in *Proceedings of the 3rd conference on learning for dynamics and control*, in Proceedings of machine learning research, vol. 144. 2021, pp. 361–372. Available: <https://proceedings.mlr.press/v144/li21a.html>

[44] K. Egashira, M. Vero, R. Staab, J. He, and M. Vechev, “Exploiting LLM quantization,” in *Advances in neural information processing systems*, 2024. Available: <https://papers.nips.cc/paper_files/paper/2024/hash/496720b3c860111b95ac8634349dcc88-Abstract-Conference.html>

[45] S. Wee, S. Kim, H. Kim, K. Hwang, and N. Kwak, “Safety-preserving post-training quantization via contrastive alignment loss,” *arXiv preprint arXiv:2511.07842*, 2026, doi: [10.48550/arXiv.2511.07842](https://doi.org/10.48550/arXiv.2511.07842).

[46] B. Rababah, C. G. Akcora, and C. K. Leung, “The illusion of equivalency: Statistical characterization of quantization effects in LLMs,” *arXiv preprint arXiv:2607.08734*, 2026, doi: [10.48550/arXiv.2607.08734](https://doi.org/10.48550/arXiv.2607.08734).

[47] J. von Rad, Y. Cao, and A. Geiger, “UniComp: A unified evaluation of large language model compression via pruning, quantization and distillation,” *arXiv preprint arXiv:2602.09130*, 2026, doi: [10.48550/arXiv.2602.09130](https://doi.org/10.48550/arXiv.2602.09130).

[48] M. Mitchell *et al.*, “Model cards for model reporting,” in *Proceedings of the conference on fairness, accountability, and transparency*, 2019, pp. 220–229. doi: [10.1145/3287560.3287596](https://doi.org/10.1145/3287560.3287596).

[49] E. Tabassi, “Artificial intelligence risk management framework (AI RMF 1.0),” National Institute of Standards and Technology, NIST AI 100-1, 2023. doi: [10.6028/NIST.AI.100-1](https://doi.org/10.6028/NIST.AI.100-1).
