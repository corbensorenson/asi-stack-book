# Evidence-Quality Vectors

Last updated: 2026-07-10

The support state remains a compact public summary. It is not the complete
epistemic record. `evidence_quality/core_claim_vectors.json` now gives every
active chapter-core claim eight separate dimensions: independence,
reproducibility, recency, coverage, adversarial strength, validity, artifact
access, and transfer distance.

The vector is deliberately non-aggregating. Its states are not commensurable
scores, a strong dimension cannot compensate automatically for an unknown or
weak one, and no sum or weighted average can move a support state. A support
transition still requires the existing governed record and review route. A
future transition should cite before/after vectors, name changed dimensions,
preserve unchanged residuals, and justify why the bounded claim summary moves.

The initial migration is conservative. All 54 core claims remain `argument`.
All record `internal_only` independence and `not_independently_assessed`
validity because no accepted independent human review exists. Public chapter,
mapping, and disposition records make artifact access partial rather than
complete. Narrow non-core fixtures can be recorded as adjacent local replay or
adjacent bounded controls, but they do not become direct evidence for the
broad chapter claim. Transfer remains unestablished.

`scripts/build_evidence_quality_vectors.py` regenerates the registry from the
authoritative core-claim dispositions. `scripts/validate_evidence_quality_vectors.py`
checks one vector per claim, exact dimension coverage and vocabulary, summary
agreement, rationales/evidence/residuals, and no aggregation. Its negative
controls remove a dimension, inject a numeric score, forge a support summary,
and add an automatic promotion effect.

This model exposes missing evidence; it does not create it, rank claims by a
single number, establish review independence, validate constructs, prove
transfer, or promote a chapter-core claim.
