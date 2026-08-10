# SpiderSynapse: A Multi-Hypothesis Reasoning Architecture

**Version:** 0.3.0
**Last Updated:** 2024-12-23
**Status:** ⚠️ DEPRECATED - Superseded by PortiaSynapse

---

> **⚠️ DEPRECATION NOTICE**: SpiderSynapse training never worked (loss stuck, accuracy oscillating).
> It has been replaced by **PortiaSynapse**, which takes a simpler, more trainable approach.
> See `docs/portia_synapse_whitepaper.md` for the current cognitive synapse architecture.
>
> **Key lesson learned**: Complexity kills trainability. PortiaSynapse uses Scout→Focus→Refine
> with a single path instead of 4 hypotheses × 3 iterations = 12 paths.

---

## Abstract

SpiderSynapse was TreeLLM's attempted next-generation reasoning architecture designed to replace DklAwareSynapse. Unlike traditional single-path neural networks, SpiderSynapse implements a **multi-hypothesis reasoning system** that explores multiple possible answers simultaneously, refines them iteratively, and integrates confidence estimation directly into the architecture.

The core insight is that the synapse should behave like a spider on a web - it doesn't just move in one direction, it:
1. **Senses the web** - perceives the local knowledge neighborhood
2. **Explores multiple paths** - considers several hypotheses in parallel
3. **Accumulates evidence** - gathers supporting facts in working memory
4. **Knows uncertainty** - has calibrated confidence in its predictions
5. **Refines iteratively** - improves predictions through multiple passes

---

## CRITICAL STATUS: Training Does Not Work

### Current Training Results (Dec 23, 2025)

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| Loss | Decreasing | Stuck at 0.57 | ❌ BROKEN |
| Accuracy | Improving | Stuck at 68-70% | ❌ BROKEN |
| Learning | Visible improvement | No improvement over 2000 steps | ❌ BROKEN |
| Coord Alignment | 20 epochs learning | Loss plateau at 0.5621 | ❌ BROKEN |

### Symptoms
1. **Loss never decreases** - Stays at ~0.57-0.58 throughout training
2. **Accuracy oscillates randomly** - 68-70% with no trend
3. **Coordinate alignment plateaus** - Loss stuck at 0.5621 (characteristic of label smoothing)
4. **No learning signal** - Model outputs look random/poor quality
5. **20 minutes main training + 160 minutes coord refinement = no improvement**

### Root Causes to Investigate

1. **Multi-hypothesis overhead** - 4 hypotheses × 3 iterations = 12x computation but same learning signal?
2. **Gradient flow** - Are gradients actually reaching the coord head through hypothesis selector?
3. **Loss function balance** - coord + 0.1*edge + 0.1*conf may be misconfigured
4. **Batch size** - Using 256 for SpiderSynapse vs 4096 for other synapses
5. **Context conversion** - `batch_item_to_context` may be losing information
6. **Working memory** - Not being utilized effectively?

---

## 1. Motivation: Why Not Just Use DklAwareSynapse?

### 1.1 Problems with DklAwareSynapse

DklAwareSynapse has a simple architecture:
```
Context → Encoder → Recurrent → Coordinate Head → Output
```

**Limitations:**
1. **Single hypothesis** - Only explores one answer path
2. **External wrappers needed** - Requires `generate_smart()` with Adversary for quality
3. **No built-in refinement** - Can't self-correct; needs external iteration
4. **Confidence is afterthought** - Calibration happens outside the network
5. **Edge types ignored** - Predicts edge types but doesn't USE them to guide reasoning

### 1.2 What We Want

A synapse that:
- Produces high-quality output **directly** without wrappers
- Explores multiple hypotheses and picks the best
- Knows when it's uncertain and can ask for help
- Uses edge types to guide knowledge traversal
- Improves predictions through internal refinement loops

---

## 2. Architecture Overview

### 2.1 Core Design Principles

1. **Multi-Hypothesis Processing**: Maintain K hypotheses in parallel, not just one
2. **Iterative Refinement**: Multiple internal passes that improve predictions
3. **Edge-Conditioned Routing**: Use edge types to guide the network
4. **Integrated Confidence**: Uncertainty estimation is part of the architecture
5. **Memory Augmentation**: Accumulate evidence across processing steps

### 2.2 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SpiderSynapse                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input Context (512)                                             │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────┐                        │
│  │     Multi-Aspect Encoder            │                        │
│  │  • Semantic Encoder (→256)          │                        │
│  │  • Structural Encoder (→128)        │                        │
│  │  • Edge-Type Encoder (→128)         │                        │
│  └─────────────────────────────────────┘                        │
│       │ (512 combined)                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────┐                        │
│  │     Hypothesis Generator            │                        │
│  │  • Generate K=4 hypothesis seeds    │                        │
│  │  • Each hypothesis: 512 dims        │                        │
│  └─────────────────────────────────────┘                        │
│       │ (K × 512)                                               │
│       ▼                                                          │
│  ┌─────────────────────────────────────┐    ┌────────────────┐  │
│  │     Refinement Tower (N iterations) │◄───│ Working Memory │  │
│  │  • Cross-Hypothesis Attention       │───►│ (accumulates)  │  │
│  │  • Edge-Conditioned FFN             │    └────────────────┘  │
│  │  • Memory Update Gate               │                        │
│  └─────────────────────────────────────┘                        │
│       │ (K × 512)                                               │
│       ▼                                                          │
│  ┌─────────────────────────────────────┐                        │
│  │     Hypothesis Selector             │                        │
│  │  • Score each hypothesis            │                        │
│  │  • Select best OR merge top-K       │                        │
│  │  • Output confidence score          │                        │
│  └─────────────────────────────────────┘                        │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────┐                        │
│  │     Output Heads                    │                        │
│  │  • Coordinate Head (→128 bits)      │                        │
│  │  • Edge Type Head (→64 types)       │                        │
│  │  • Confidence Head (→1 scalar)      │                        │
│  │  • Uncertainty Head (→1 scalar)     │                        │
│  └─────────────────────────────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Details

### 3.1 Multi-Aspect Encoder

Unlike DklAwareSynapse's single encoder, we use **three specialized encoders**:

| Encoder | Input | Output | Purpose |
|---------|-------|--------|---------|
| Semantic | Content embedding (128) | 256 | Understand meaning |
| Structural | Coord bits + neighbor summary (256) | 128 | Understand graph position |
| Edge-Type | Edge distribution + modulation (128) | 128 | Understand available paths |

These are concatenated (512) and passed through layer norm.

### 3.2 Hypothesis Generator

Generates K=4 diverse hypothesis seeds using **learned diversity heads**:

```python
# Pseudocode
encoded = multi_aspect_encode(context)  # [512]
hypotheses = []
for k in range(K):
    h_k = diversity_head[k](encoded)  # Each head produces different seed
    hypotheses.append(h_k)
return stack(hypotheses)  # [K, 512]
```

The diversity heads are trained to produce meaningfully different hypotheses.

### 3.3 Refinement Tower

The core innovation - **iterative refinement with cross-hypothesis attention**:

```python
# N refinement iterations (N=3 default)
for iteration in range(N):
    # Cross-hypothesis attention: each hypothesis attends to all others
    attended = cross_attention(hypotheses, hypotheses, hypotheses)
    
    # Edge-conditioned FFN: use predicted edge types to modulate
    edge_logits = edge_predictor(hypotheses)
    edge_weights = softmax(edge_logits)
    modulated = edge_conditioned_ffn(attended, edge_weights)
    
    # Memory update: accumulate evidence
    memory = memory_gate(memory, modulated)
    
    # Residual update
    hypotheses = hypotheses + modulated
```

### 3.4 Hypothesis Selector

Scores each hypothesis and either selects the best or merges top candidates:

- **Confidence Score**: How certain is this hypothesis?
- **Coherence Score**: How internally consistent?
- **Evidence Score**: How much memory support?

Final selection can be:
- **Argmax**: Pick highest-scoring hypothesis
- **Weighted Merge**: Combine top-K weighted by confidence
- **Ensemble**: Average predictions from all hypotheses

### 3.5 Output Heads

Four output heads from the selected/merged hypothesis:

1. **Coordinate Head**: 6-layer MLP → 128 bits (the predicted DKL coordinate)
2. **Edge Type Head**: 2-layer MLP → 64 logits (which edge type to follow)
3. **Confidence Head**: 2-layer MLP → 1 scalar (how confident in prediction)
4. **Uncertainty Head**: 2-layer MLP → 1 scalar (epistemic uncertainty)

---

## 4. Training

### 4.1 Loss Functions

**Primary Loss (Coordinate Prediction):**
```
L_coord = BCE(pred_coord_bits, target_coord_bits)
```

**Auxiliary Losses:**
```
L_edge = CrossEntropy(pred_edge, target_edge)
L_confidence = MSE(pred_confidence, actual_accuracy)  # Calibration
L_diversity = -variance(hypotheses)  # Encourage diverse hypotheses
```

**Total Loss:**
```
L = L_coord + 0.1*L_edge + 0.1*L_confidence + 0.01*L_diversity
```

### 4.2 Training Curriculum

1. **Phase 1**: Train on single-hop predictions (simple)
2. **Phase 2**: Train on multi-hop reasoning chains
3. **Phase 3**: Train confidence calibration with held-out data
4. **Phase 4**: Fine-tune hypothesis diversity

---

## 5. Differences from DklAwareSynapse

| Aspect | DklAwareSynapse | SpiderSynapse |
|--------|-----------------|---------------|
| Hypotheses | 1 | K=4 |
| Refinement | None (single pass) | N=3 iterations |
| Encoders | 1 (generic) | 3 (specialized) |
| Confidence | External | Integrated head |
| Edge usage | Predicted but ignored | Conditions FFN |
| Output quality | Needs wrappers | Direct high-quality |
| Parameters | ~500K | ~2M |

---

## 6. Implementation Status

### Components Built
- [x] Multi-Aspect Encoder: semantic(128→256) + structural(256→128) + edge(128→128) = 512
- [x] Hypothesis Generator: K=4 diversity heads
- [x] Refinement Tower: 8 heads × 64 dims, N=3 iterations
- [x] Cross-Hypothesis Attention: MultiEyeAttention with query/key/value projections
- [x] 6-layer Coordinate Head: 512 → 512 → 384 → 384 → 256 → 128
- [x] Confidence Head: Integrated
- [x] Uncertainty Head: Integrated
- [x] Total parameters: 4,762,883 (~4.8M)
- [x] Metal GPU acceleration: Apple Silicon backend

### Components Broken
- [ ] Training loop - **DOES NOT LEARN**
- [ ] Working Memory - not being utilized
- [ ] Edge-Conditioned FFN - implemented but unclear if effective
- [ ] Hypothesis Selector - uses simple argmax, may not be optimal
- [ ] Benchmark comparison - cannot test until training works

---

## 7. Training System Analysis

### 7.1 Current Training Flow
```
Input (batch × 512)
    → Multi-Aspect Encode (512)
    → Hypothesis Generator (K × 512)
    → Refinement Tower (N iterations, K × 512)
    → Hypothesis Selection (512)
    → Coordinate Head (512 → 128)
    → BCE Loss vs target coordinates
    → Backward + Optimizer Step
```

### 7.2 Why Training Might Be Failing

1. **Gradient Dilution**: 4 hypotheses × 3 iterations = 12 paths, gradients may be too diluted
2. **Hypothesis Collapse**: All 4 hypotheses might be producing identical outputs
3. **Context Mismatch**: `batch_item_to_context` pads to 512 but input is 128 floats
4. **Loss Imbalance**: coord + 0.1*edge + 0.1*conf - edge/conf may interfere
5. **Optimizer Issues**: Using same optimizer as DklAwareSynapse but architecture is different
6. **Batch Size**: 256 may be too small for multi-hypothesis to get meaningful diversity

### 7.3 Comparison: DklAwareSynapse vs SpiderSynapse Training

| Aspect | DklAwareSynapse | SpiderSynapse |
|--------|-----------------|---------------|
| Training Result | Works (loss decreases) | Broken (loss flat) |
| Forward Pass | Simple linear | Complex multi-path |
| Parameters | ~500K | ~4.8M |
| Batch Size | 4096 | 256 |
| Loss Function | coord + edge + conf | Same but different weights |
| Gradient Flow | Direct | Through hypothesis selector |

### 7.4 Proposed Fixes

1. **Simplify First**: Train with K=1 (single hypothesis) to verify base architecture
2. **Increase Batch Size**: Try 1024 or 2048 for SpiderSynapse
3. **Disable Auxiliary Losses**: Train ONLY coord loss first
4. **Add Gradient Logging**: Print gradient magnitudes per layer
5. **Check Hypothesis Diversity**: Log variance of hypothesis outputs
6. **Use DklAwareSynapse Learning Rate**: 0.003 works for DKL, may need different for Spider

---

## 8. Open Questions

1. **Why doesn't training work?** - Critical blocker
2. **How many hypotheses (K)?** Start with 1, work up to 4
3. **How many refinement iterations (N)?** Start with 1, could be dynamic
4. **Merge vs Select?** Need to experiment once training works
5. **Memory size?** How much working memory to maintain
6. **Training stability?** Multi-hypothesis is clearly harder to train

---

## 8. Dimension Specification

### 8.1 Constants

```rust
// Input dimensions (must match DklAwareSynapse for compatibility)
pub const RICH_CONTEXT_DIM: usize = 512;
pub const COORD_BITS_DIM: usize = 128;
pub const CONTENT_EMBED_DIM: usize = 128;
pub const EDGE_DIST_DIM: usize = 64;
pub const NEIGHBOR_SUMMARY_DIM: usize = 128;
pub const MODULATION_DIM: usize = 64;

// SpiderSynapse-specific
pub const NUM_HYPOTHESES: usize = 4;          // K hypotheses
pub const NUM_REFINEMENT_ITERS: usize = 3;    // N refinement passes
pub const HYPOTHESIS_DIM: usize = 512;        // Each hypothesis size
pub const SEMANTIC_ENC_DIM: usize = 256;      // Semantic encoder output
pub const STRUCTURAL_ENC_DIM: usize = 128;    // Structural encoder output
pub const EDGE_ENC_DIM: usize = 128;          // Edge encoder output
pub const NUM_ATTENTION_HEADS: usize = 8;     // Cross-hypothesis attention
pub const HEAD_DIM: usize = 64;               // Per-head dimension
pub const FFN_DIM: usize = 1024;              // FFN hidden dimension
pub const NUM_EDGE_TYPES: usize = 64;         // Edge type vocabulary
pub const MEMORY_SIZE: usize = 256;           // Working memory dimension
```

### 8.2 Parameter Count Estimate

| Component | Parameters |
|-----------|------------|
| Multi-Aspect Encoders | ~200K |
| Hypothesis Generator (4 heads) | ~400K |
| Refinement Tower (3 iterations) | ~800K |
| Cross-Hypothesis Attention | ~300K |
| Output Heads | ~200K |
| **Total** | **~1.9M** |

This is ~4x larger than DklAwareSynapse (~500K), but still small enough for fast inference.

---

## 9. Why This Architecture Works

### 9.1 Multi-Hypothesis = Beam Search in Latent Space

Traditional beam search operates on discrete tokens. SpiderSynapse does beam search in the latent hypothesis space - more flexible and differentiable.

### 9.2 Refinement = Thinking Time

Each refinement iteration is like "thinking" - the network reconsiders and improves its predictions. This is similar to how chain-of-thought prompting works, but learned and internalized.

### 9.3 Edge Conditioning = Graph-Aware Reasoning

By conditioning the FFN on edge types, the network learns different reasoning patterns for different relationship types (e.g., "is-a" vs "has-part" require different logic).

### 9.4 Integrated Confidence = Calibrated Uncertainty

Training the confidence head with accuracy supervision means the network learns to predict when it will be wrong - crucial for knowing when to ask for help.

---

## 10. Comparison: Spider Generate Wrapper vs Native SpiderSynapse

### Current State (with wrapper):
```
Query → DklAwareSynapse → Raw Output → Adversary Check → Refinement Loop → Final Output
                           (low quality)    (external)        (external)     (high quality)
```

### Goal State (native):
```
Query → SpiderSynapse → High-Quality Output (with confidence)
              ↑
         (internal refinement, internal confidence)
```

The wrapper approach requires:
- Multiple forward passes (slow)
- External Adversary component (complex)
- Heuristic iteration limits (arbitrary)

Native SpiderSynapse provides:
- Single forward pass (fast)
- Integrated quality via multi-hypothesis selection
- Learned iteration (via refinement tower depth)

---

## 11. Implementation Roadmap

### Phase 1: Foundation
1. Define new struct with all layers
2. Implement Multi-Aspect Encoder
3. Implement single hypothesis path (K=1 baseline)
4. Verify training works

### Phase 2: Multi-Hypothesis
1. Implement Hypothesis Generator
2. Implement Cross-Hypothesis Attention
3. Train with K=4 hypotheses
4. Implement Hypothesis Selector

### Phase 3: Refinement Tower
1. Implement Edge-Conditioned FFN
2. Implement Memory Update Gate
3. Add refinement iterations (N=3)
4. Train and evaluate

### Phase 4: Confidence Integration
1. Add Confidence Head
2. Add Uncertainty Head
3. Train confidence calibration
4. Implement "I don't know" behavior

### Phase 5: Optimization
1. Profile and optimize inference
2. Reduce parameters if needed
3. Benchmark against DklAwareSynapse
4. Remove wrapper dependency

---

## 12. Success Metrics

SpiderSynapse is successful when:

1. **Training works**: Loss actually decreases during training ← CURRENT BLOCKER
2. **Benchmark parity**: Matches DklAwareSynapse on all benchmarks
3. **No wrappers needed**: Direct output quality is high
4. **Calibrated confidence**: Confidence predicts accuracy (ECE < 0.1)
5. **Knows uncertainty**: Can reliably say "I don't know"
6. **Faster inference**: Despite more parameters, internal refinement beats external iteration
7. **Training stable**: Can train to convergence without NaN/Inf issues

---

## 13. Immediate TODO: Fix Training

### Priority 1: Diagnose Why Training Fails
1. Add gradient magnitude logging to see if gradients reach coord head
2. Log hypothesis outputs to check for collapse (all 4 same?)
3. Compare forward pass shapes with DklAwareSynapse
4. Test with K=1 (single hypothesis mode)

### Priority 2: Simplify Architecture for Debugging
1. Create a "minimal Spider" with K=1, N=1
2. Verify it trains (loss decreases)
3. Gradually add complexity back

### Priority 3: Fix Known Issues
1. `batch_item_to_context` - verify it produces correct 512-dim context
2. Hypothesis selector gradient flow
3. Working memory utilization
4. Cross-hypothesis attention effectiveness

### Priority 4: Training Hyperparameters
1. Try larger batch size (1024, 2048)
2. Try different learning rates (0.001, 0.01)
3. Disable auxiliary losses (edge, confidence) temporarily
4. Add warmup schedule

---

## 14. References

- Mixture of Experts (MoE) - for hypothesis diversity
- Iterative Refinement Networks - for refinement tower design
- Confident Learning - for uncertainty estimation
- Graph Neural Networks - for edge-conditioned processing
- Universal Transformers - for iterative refinement concept
- Confident Learning (Northcutt et al.) - for calibration training

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.2.0 | 2024-12-23 | Added training diagnostics, documented broken training, updated implementation status |
| 0.1.0 | 2024-12-22 | Initial architecture design |

