# Source Note: Muon Optimizes Under Spectral Norm Constraints

| Field | Value |
|---|---|
| Source ID | `ext_muon_spectral_norm_2026` |
| Ingestion date | 2026-07-21 |
| Source | Chen, Li, and Liu, TMLR 2026, https://openreview.net/forum?id=Blz4hjxLwU |
| Review state | Accepted by TMLR, published 2026-03-23 |
| Ingestion basis | Primary abstract, Lion-K/nuclear-norm correspondence, decoupled-decay interpretation, and theoretical scope reviewed. |

## Thesis and mechanism

The paper places Muon in a generalized Lion-K family. With the nuclear norm as
the convex map and decoupled weight decay, it derives an interpretation in
which the optimizer implicitly solves a problem with a spectral-norm constraint
on weight matrices.

## Evidence and limits

This is an optimizer-geometry interpretation, not a demonstration that every
practical inexact Newton--Schulz implementation exactly follows the idealized
map. It does not establish downstream quality, robustness, safety, compute
efficiency, or universal superiority.

## Book use

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use to explain one theoretical account of Muon's implicit regularization and to
motivate spectral diagnostics. Preserve the distinction between an exact
mathematical update, an approximate implementation, and measured model
behavior.
