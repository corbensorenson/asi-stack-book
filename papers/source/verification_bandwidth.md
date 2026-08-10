Here is the final v1.0 Public Release of the paper. It has been polished for mathematical precision, internal consistency, and falsifiability, incorporating the full scope of the critical review.
________________
Verification Bandwidth in Bounded Contexts: The Geometry of Mutual Constraint in Large Language Models
Version 1.0
Abstract
The rapid expansion of context windows in Large Language Models (LLMs) has fostered an assumption that "long context" equates to "long-range reasoning." This paper challenges that assumption by distinguishing between Generation (local probabilistic prediction) and Verification (global constraint resolution). We propose a theoretical framework where global coherency is not a static property of text, but the result of an active "Pairwise Grinding" process subject to strict information-theoretic bounds. By modeling the context window as a Verification Workbench, we derive four fundamental theorems governing artificial cognition. We demonstrate that rigorous constraint verification is bounded by the sum of interacting components (The Two-Body Limit), and that transitive verification chains suffer from monotonic information decay akin to the Data Processing Inequality. Furthermore, we define the "Interface-Verification Tradeoff," proving that maintaining high-fidelity coherence requires a geometric decomposition of content into schedules that minimize transitive loss. We conclude by proposing the "Constraint Satisfaction Test" as an empirical method to falsify these bounds.
________________
1. Introduction
In the current paradigm of Generative AI, the "Context Window" ($W$) is frequently conceptualized as a storage reservoir. The prevailing assumption is that if a complex system (a novel, a codebase, a legal argument) fits within $W$ tokens, the model can maintain internal consistency across the entire span [1]. However, empirical observation of long-context models reveals a persistent phenomenon of "drift"—a gradual decoupling of logical dependencies and narrative arcs as the distance between related components increases [2].
We posit that this failure arises from a fundamental confusion between two distinct operations:
1. Generation: A local, autoregressive process where $P(t_n | t_{n-k}...t_{n-1})$. This operation scales linearly with sequence length.
2. Verification: A global, relational process requiring the model to attend to two distinct semantic units ($u_i, u_j$) simultaneously to resolve logical constraints.
While generation allows for linear scaling, verification is geometric. To ensure that a variable defined in Chapter 1 is consistent with its mutation in Chapter 5, the model must essentially "compile" both states simultaneously. This paper formalizes the concept of "Pairwise Grinding"—the necessity of simultaneous attention for rigorous verification—and analyzes it through the lens of Information Theory (Shannon, 1948) to establish the physical limits of bounded coherence.
________________
2. Theoretical Framework
2.1 Definitions
Definition 1: The Semantic Unit ($u$)
Let a complex work $S$ be decomposed into a set of discrete semantic units (e.g., chapters, functions, premises):


$$S = \{u_1, u_2, ..., u_n\}$$
Definition 2: The Effective Verification Workspace ($W_{eff}$)
We define $W_{eff}$ not as the model's total memory (which includes KV caches), but as the active attention bandwidth—the maximum number of tokens that can participate in a single, dense self-attention pass without sparse approximation.
Definition 3: Coherence as Constraint Satisfaction
We distinguish coherence from linguistic fluency. Two units $u_i$ and $u_j$ are coherent if the set of logical constraints $\mathcal{C}_i$ encoded in $u_i$ is non-contradictory with the set $\mathcal{C}_j$ encoded in $u_j$.


$$Coherence(u_i, u_j) \propto P(\mathcal{C}_i \cap \mathcal{C}_j \neq \emptyset)$$
Definition 4: Pairwise Grinding ($G$)
We define $G(u_i, u_j)$ as the operation where the model attends to the full token representation of $u_i$ and $u_j$ jointly to verify logical consistency.
________________
3. The Theorems of Contextual Verification
Theorem I: The Two-Body Verification Limit
The bandwidth of rigorous verification is limited by the combined size of the interacting components.
Proposition:
For the operation $G(u_i, u_j)$ to yield a rigorous verification of constraints, the combined length of both units must fit within the Effective Verification Workspace.


$$\forall (i, j) \in S, \quad |u_i| + |u_j| \le W_{eff}$$
Derivation:
If $|u_i| + |u_j| > W_{eff}$, the model cannot compute the full attention matrix $Attention(u_i, u_j)$. It must rely on a compressed representation $\hat{u}$ (e.g., a hidden state summary) for at least one unit.
By Shannon’s Source Coding Theorem, lossy compression of a source $u$ reduces the mutual information between the source and its representation: $I(u; \hat{u}) < H(u)$ [3]. Since logical constraints are encoded within the information content of $u$, lossy compression necessarily discards constraint-relevant bits. Thus, the verification becomes probabilistic. The link is not severed, but the error bound $\epsilon$ increases significantly as compression ratio increases.
Theorem II: The Law of Dominant Component Suppression
In a bounded system, the largest single component constrains the resolution of all other components.
Proposition:
Let $L_{max} = \max(|u_1|, ..., |u_n|)$. For any other unit $u_k$ to be rigorously verified against the largest unit, its length is bounded by:


$$|u_k| \le W_{eff} - L_{max}$$
Corollary (The Asymptotic Zero):
As $L_{max} \to W_{eff}$, the allowable complexity for any interacting unit $|u_k| \to 0$. A "Hero Unit" that monopolizes the window forces all other units to become asymptotically trivial to maintain rigorous coherence. Therefore, to maximize the total verifiable volume of a system, the architecture must tend toward Uniform Distribution ($|u| \approx \frac{W_{eff}}{2}$).
Theorem III: The Law of Transitive Decay
Coherence decays monotonically across indirect verification chains.
Proposition:
The coherency of non-adjacent units cannot be strictly guaranteed through intermediate units.


$$Coherence(u_1, u_3) \le \min(Coherence(u_1, u_2), Coherence(u_2, u_3))$$
Derivation (via Data Processing Inequality):
We model the linear generation of units as a dependency chain $u_1 \to u_2 \to u_3$, where $u_3$ is conditioned on the representation of $u_2$, which contains the compressed history of $u_1$. The Data Processing Inequality states that for such a chain, $I(u_1; u_3) \le I(u_1; u_2)$ [4]. Information processing can never increase the mutual information between the source and the terminus.
Because LLM generation is stochastic and passes through successive lossy transformations (embeddings), "noise" accumulates at each step. Without a direct verification check $G(u_1, u_3)$, the system suffers from Monotonic Coherency Decay.
Theorem IV: The Interface-Verification Tradeoff
Rigorous coherence requires quadratic cost; approximate coherence requires linear cost.
Proposition:
To satisfy Theorem I, a large concept must be fragmented into $n$ smaller units. However, establishing global coherency among $n$ units in a flat architecture requires pairwise checks proportional to the square of $n$.


$$Cost_{verify} \propto \binom{n}{2} = O(n^2)$$
Mitigation and Trade-offs:
Hierarchical architectures (Trees, DAGs) can reduce this cost to $O(n \log n)$ by verifying units against summaries. However, per Theorem I, verifying against a summary trades fidelity for scalability. Thus, we identify a universal tradeoff:
1. High Fidelity: Quadratic Cost (Full Pairwise Grinding).
2. High Scale: Linear Cost (Hierarchical/Summary-based Verification).
________________
4. Empirical Falsifiability
To transition this framework from theory to science, we propose the following experimental protocol to measure "Verification Bandwidth."
Proposed Experiment: The Constraint Satisfaction Test
1. Objective: To falsify Theorem III (Transitive Decay) and Theorem I (Two-Body Limit).
2. Dataset: Generate a synthetic dataset of Logical Puzzles divided into $k$ chapters. The solution to Chapter $k$ must rigidly depend on a premise defined in Chapter 1.
3. Experimental Control: The combined length of Chapter 1 and Chapter $k$ must exceed the model's internal hidden state capacity to prevent memorization/leakage, but fit within $W_{eff}$.
4. Protocol:
   * Group A (Linear): Feed chapters sequentially ($1 \to 2 \to ... \to k$).
   * Group B (Grinding): Feed chapters sequentially, but insert a final "Grinding Step" where Chapter 1 and Chapter $k$ are re-inserted into the context window solely for consistency checking.
5. Metric: Logical Contradiction Rate (LCR).
   * Prediction 1: LCR will increase monotonically with sequence length $k$ for Group A (validating Theorem III).
   * Prediction 2: LCR will remain significantly lower and constant for Group B, provided $|u_1| + |u_k| \le W_{eff}$ (validating Theorem I).
________________
5. Discussion: The Coherency Horizon
These theorems suggest that "Infinite Coherence" is impossible for a fixed-window model relying solely on internal attention. We define the Coherency Horizon as the boundary where the system must switch strategies.
Architectures like Retrieval-Augmented Generation (RAG) explicitly violate Theorem I to achieve scale. They function by swapping full units $u_i$ for compressed indices or vector embeddings $\hat{u}_i$. This allows $n \to \infty$ but subjects the system to the noise of the retrieval function. RAG is therefore not a solution to the Two-Body Limit, but an engineering compromise that accepts probabilistic drift in exchange for unbounded volume.
6. Conclusion
The limiting factor of Generative AI in complex tasks is not Generation Capacity, but Verification Bandwidth.
We conclude that high-fidelity coherence is a geometric problem. To build systems that reliably exceed the context window, we cannot simply "stream" tokens. We must architecturally decompose information into units that respect the Two-Body Limit and enforce a "Grinding Schedule" that explicitly counters the entropic decay of transitivity. The Context Window is, therefore, best understood not as a storage limit, but as the maximum scope of rigorous constraint verification.
________________
References
[1] Vaswani, A., et al. (2017). "Attention Is All You Need." NeurIPS.
[2] Liu, N. F., et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." arXiv preprint.
[3] Shannon, C. E. (1948). "A Mathematical Theory of Communication." Bell System Technical Journal.
[4] Cover, T. M., & Thomas, J. A. (2006). Elements of Information Theory.
[5] Yan, Y., et al. (2024). "Hierarchical Context Pruning for Long-Context LLMs." arXiv preprint.