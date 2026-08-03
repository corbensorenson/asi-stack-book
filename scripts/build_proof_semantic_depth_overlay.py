#!/usr/bin/env python3
"""Build the current P0-P6 semantic-depth overlay for every live Lean theorem.

The older proof-rationalization registry is a frozen activation-baseline
artifact.  This builder deliberately leaves it untouched and projects a new
current-manifest view over the live Lean estate.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from build_proof_rationalization_registry import current_theorems


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "proofs" / "proof_semantic_depth_overlay.json"
REPORT = ROOT / "docs" / "proof_semantic_depth_overlay.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
HISTORICAL = ROOT / "proofs" / "proof_rationalization_registry.json"
STRUCTURE = ROOT / "book_structure.json"
VALIDATION = ROOT / "validation" / "registry.json"
CLUSTER_GLOB = ROOT / "proofs" / "semantic_cluster_audits"

LEVEL_MEANINGS = {
    "P0": "schema, type, record-shape, or direct projection property",
    "P1": "finite route, rejection, or preservation property",
    "P2": "reachable bounded execution, witnessed route, or nonvacuity property",
    "P3": "implementation refinement or runtime-validator binding",
    "P4": "cross-component safety, noninterference, or adversarial-composition property",
    "P5": "bounded liveness, recovery, revocation, rollback, or concurrency property",
    "P6": "empirically bound semantic property with a named observation contract",
}

ROUTE_TERMS = (
    "route", "reject", "block", "preserv", "require", "request", "admit",
    "allow", "deny", "quarantine", "fallback", "hold", "transition",
)
REACHABILITY_TERMS = (
    "reaches", "reachable", "complete_", "accepted_", "closed", "restores",
    "roundtrip", "replay", "witness", "nonvacu",
)
CROSS_COMPONENT_TERMS = (
    "cannot", "noninterference", "unauthorized", "without_authority",
    "without_grant", "without_receipt", "cross_component", "cross_layer",
    "launder", "independent", "separation", "no_support", "no_effect",
    "effect_authority", "support_authority",
)
LIVENESS_TERMS = (
    "bounded_liveness", "eventually", "terminal", "recovery", "recover",
    "rollback", "revocation", "revoked", "concurrent", "concurrency",
    "retirement", "expires", "expiry",
)
STRONG_NAME_TERMS = (
    "safe", "complete", "guarantee", "proof", "verified", "secure",
    "correct", "promotion", "release",
)

# Current semantic review may overturn a frozen disposition without mutating
# the historical registry.  Each override is theorem-specific and records why
# the older equivalence judgment is not sufficient for current retirement.
CURRENT_SEMANTIC_OVERRIDES = {
    "lean/AsiStackProofs/Efficiency.lean::total_cost_is_additive": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "universal seven-class cost-vector algebra rather than a record projection"
        ],
        "rationale": (
            "The theorem proves modeled total-cost additivity for arbitrary vectors; "
            "it assumes the seven components are the complete declared accounting surface."
        ),
    },
    "lean/AsiStackProofs/Efficiency.lean::total_cost_is_componentwise_monotone": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "universal arithmetic consequence across all seven modeled cost components"
        ],
        "rationale": (
            "The theorem derives total-cost monotonicity from componentwise bounds for arbitrary vectors; "
            "it does not validate the component measurements."
        ),
    },
    "lean/AsiStackProofs/Efficiency.lean::selected_route_is_a_listed_eligible_candidate": {
        "disposition": "retain",
        "semantic_level": "P3",
        "classification_basis": [
            "structural induction proves soundness of the executable finite selector",
            "the independent route-search consumer is digest-bound to the Lean module",
        ],
        "rationale": (
            "For arbitrary finite candidate lists, every returned route is a listed eligible member. "
            "Eligibility fields remain authored inputs rather than empirical observations."
        ),
    },
    "lean/AsiStackProofs/Efficiency.lean::no_selected_route_means_no_eligible_candidate": {
        "disposition": "retain",
        "semantic_level": "P3",
        "classification_basis": [
            "structural induction proves the executable selector's none-case completeness over its finite input list",
            "the independent route-search consumer exercises both accepting and rejecting candidate families",
        ],
        "rationale": (
            "A none result implies no authored candidate satisfies the modeled eligibility predicate; "
            "the theorem does not establish route-search completeness beyond the supplied list."
        ),
    },
    "lean/AsiStackProofs/Efficiency.lean::selected_route_has_minimum_modeled_cost": {
        "disposition": "retain",
        "semantic_level": "P3",
        "classification_basis": [
            "nested structural induction proves the executable selector's universal minimum property",
            "two independent synthetic traces agree with the selector while six invalid controls reject",
        ],
        "rationale": (
            "For every eligible member of an arbitrary finite authored candidate list, the returned route's "
            "seven-class modeled total is no greater. Cost accuracy and candidate completeness are excluded."
        ),
    },
    "lean/AsiStackProofs/Efficiency.lean::finite_selector_reaches_bounded_minimum_witness": {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [
            "lean-theorem:finite_selector_reaches_bounded_minimum_witness",
            "experiments/efficiency_route_search/results/2026-07-02-local.json",
        ],
        "classification_basis": [
            "closed four-candidate fixture witnesses a reachable eligible minimum"
        ],
        "rationale": "The fixture is a bounded nonvacuity witness for the executable selector.",
    },
    "lean/AsiStackProofs/Efficiency.lean::cheaper_unauthorized_route_does_not_displace_eligible_minimum": {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [
            "lean-theorem:cheaper_unauthorized_route_does_not_displace_eligible_minimum"
        ],
        "classification_basis": [
            "closed countermodel demonstrates cost alone cannot bypass modeled authority"
        ],
        "rationale": "The bounded route pair witnesses authority-sensitive selection, not deployed authorization.",
    },
    "lean/AsiStackProofs/Efficiency.lean::cheaper_failed_quality_route_does_not_displace_eligible_minimum": {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [
            "lean-theorem:cheaper_failed_quality_route_does_not_displace_eligible_minimum"
        ],
        "classification_basis": [
            "closed countermodel demonstrates cost alone cannot bypass the modeled quality predicate"
        ],
        "rationale": "The bounded route pair witnesses quality-sensitive selection, not empirical route quality.",
    },
    "lean/AsiStackProofs/ObservationTrust.lean::eligible_agreement_with_same_root_is_correlated": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "universal branch derivation unfolds eligibility, hypothesis agreement, and declared-root equality"
        ],
        "rationale": (
            "The theorem derives the correlated branch for arbitrary eligible channel records "
            "under explicit same-hypothesis and same-root premises; it is not a direct field projection."
        ),
    },
    "lean/AsiStackProofs/ObservationTrust.lean::declared_same_root_agreement_counts_one": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "universal evidence-count consequence follows from the correlated branch derivation"
        ],
        "rationale": (
            "The theorem derives count one for arbitrary eligible same-root agreement in the finite model; "
            "the authored root remains an assumption rather than discovered sensor dependence."
        ),
    },
    "lean/AsiStackProofs/ObservationTrust.lean::eligible_agreement_with_distinct_roots_is_independent": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "universal branch derivation unfolds eligibility, agreement, and declared-root inequality"
        ],
        "rationale": (
            "The theorem derives the independent-agreement branch under explicit distinct-root premises; "
            "it does not establish that the declared roots are causally independent."
        ),
    },
    "lean/AsiStackProofs/ObservationTrust.lean::correlated_pair_witness_counts_one_independent_item": {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [
            "lean-theorem:correlated_pair_witness_counts_one_independent_item"
        ],
        "classification_basis": [
            "concrete eligible same-root pair witnesses the correlated branch and count-one outcome"
        ],
        "rationale": "The closed authored pair is a bounded nonvacuity witness for correlated agreement.",
    },
    "lean/AsiStackProofs/ObservationTrust.lean::independent_pair_witness_counts_two_independent_items": {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [
            "lean-theorem:independent_pair_witness_counts_two_independent_items"
        ],
        "classification_basis": [
            "concrete eligible distinct-root pair witnesses the independent branch and count-two outcome"
        ],
        "rationale": "The closed authored pair proves the classifier is selective rather than a blanket hold.",
    },
    "lean/AsiStackProofs/ObservationTrust.lean::disagreement_witness_is_not_collapsed_into_agreement": {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [
            "lean-theorem:disagreement_witness_is_not_collapsed_into_agreement"
        ],
        "classification_basis": [
            "concrete eligible conflicting pair witnesses the disagreement branch without agreement promotion"
        ],
        "rationale": "The closed authored pair is a bounded nonvacuity witness for preserved disagreement.",
    },
    "lean/AsiStackProofs/ObservationTrust.lean::full_observation_lifecycle_reaches_invalidated_state": {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [
            "lean-theorem:full_observation_lifecycle_reaches_invalidated_state"
        ],
        "classification_basis": [
            "six concrete accepted events witness reachability from capture through handoff to invalidation"
        ],
        "rationale": (
            "The closed lifecycle witnesses six receipts, one handoff, one invalidation, and zero support "
            "or external-authority assignments under the canonical packet assumptions."
        ),
    },
    "lean/AsiStackProofs/SearchSubstrates.lean::unproven_qualified_record_contradicts_noncore_invariant": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "statement derives a finite contradiction between the qualified state and the non-core invariant"
        ],
        "rationale": (
            "The precise name now states the bounded contradiction: an authored record "
            "cannot be both qualified without passing evidence and satisfy the rule that "
            "unproven records remain non-core. It does not reject the substrate itself."
        ),
    },
    "lean/AsiStackProofs/SearchSubstrates.lean::qualified_substrate_without_passing_evidence_rejected": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "statement derives rejection of a finite qualified record with explicitly false passing evidence"
        ],
        "rationale": (
            "Current semantic review overturns the frozen duplicate label: this theorem "
            "negates CoreAdoptionValid, while the proposed replacement negates "
            "UnprovenSubstrateRemainsNonCore. The predicates are related but not "
            "equivalent, so both bounded results remain independently owned."
        ),
    },
    "lean/AsiStackProofs/SearchSubstrates.lean::substrate_adoption_record_missing_required_field_rejected": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "statement derives rejection from explicitly absent finite adoption-record fields"
        ],
        "rationale": "The theorem checks authored record consistency, not the truth or quality of substrate evidence.",
    },
    "lean/AsiStackProofs/SearchSubstrates.lean::consumer_axis_reliance_without_measurement_or_unblocked_axis_rejected": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "statement derives a finite consumer-axis rejection from authored measurement and block fields"
        ],
        "rationale": "The theorem does not measure the axis or establish consumer behavior outside the record model.",
    },
    "lean/AsiStackProofs/SearchSubstrates.lean::canary_substrate_without_complete_evidence_packet_rejected": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "statement derives rejection from an explicitly incomplete finite canary evidence packet"
        ],
        "rationale": "The theorem checks packet completeness and proves no canary workload result.",
    },
    "lean/AsiStackProofs/SafetyCriticalLifecycle.lean::accepted_promote_support_step_requires_model_promotion_ready": {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "statement derives a finite transition precondition but does not construct a concrete reachable witness"
        ],
        "rationale": (
            "The precise name limits the result to the authored transition function: "
            "acceptance of the promoteSupport step implies the model's promotionReady "
            "predicate, without implying real-world readiness or support promotion."
        ),
    },
}

_scf_execution_overrides = {
    "apply_lifecycle_event_preserves_exact_identity": (
        "P3",
        "one-step identity custody is proved for the executable finite SCF transition function",
    ),
    "accepted_lifecycle_event_advances_and_records_receipt": (
        "P3",
        "accepted executable transitions advance to the event destination and record its receipt",
    ),
    "run_lifecycle_events_compose": (
        "P3",
        "structural induction proves exact prefix/suffix composition for the executable lifecycle runner",
    ),
    "apply_lifecycle_event_cannot_assign_support_or_external_effect": (
        "P4",
        "one-step noninterference keeps support and external-effect authority outside the lifecycle transition",
    ),
    "rejected_lifecycle_event_preserves_exact_state": (
        "P4",
        "a rejected event is proved unable to mutate any runtime-state field",
    ),
    "run_lifecycle_events_preserve_exact_identity": (
        "P4",
        "induction preserves the complete field, evaluator, authority, regression, and rollback identity across arbitrary event lists",
    ),
    "run_lifecycle_events_cannot_assign_support_or_external_effect": (
        "P4",
        "induction proves support and external-effect non-authority across arbitrary event lists",
    ),
    "terminal_lifecycle_event_is_rejected": (
        "P5",
        "every event is rejected from either modeled terminal state",
    ),
    "terminal_lifecycle_state_is_absorbing": (
        "P5",
        "induction proves retired and quarantined states absorb arbitrary event suffixes",
    ),
    "complete_scf_lifecycle_trace_reaches_exact_retired_state": (
        "P2",
        "a closed five-event witness reaches the exact retired state with five receipts",
    ),
    "incident_trace_reaches_exact_absorbing_quarantine_state": (
        "P2",
        "a closed incident witness reaches the exact quarantined state and records quarantine custody",
    ),
}

for _theorem_name in (
    "authority_expanding_replacement_without_grant_rejected",
    "field_identity_mismatch_rejects_replacement",
    "stale_qualification_lease_requires_requalification",
    "missing_evidence_requires_requalification",
    "captured_evaluator_routes_to_governance_review",
    "authority_expansion_without_grant_routes_to_governance_review",
    "open_incident_requires_rollback",
    "complete_default_review_routes_to_default",
    "retired_state_cannot_transition",
    "default_transition_requires_full_readiness",
    "default_without_qualification_evidence_rejected",
    "default_without_regression_floor_rejected",
    "default_authority_expansion_rejected",
    "default_without_rollback_rejected",
    "default_with_open_incident_rejected",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/StableCapabilityFields.lean::{_theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "the statement remains a one-step finite route, rejection, or readiness consequence despite module-level validator binding"
        ],
        "rationale": (
            "The independent consumer binds the module but does not turn this local finite "
            "consequence into implementation refinement, cross-component safety, or liveness."
        ),
    }

for _theorem_name, (_semantic_level, _basis) in _scf_execution_overrides.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/StableCapabilityFields.lean::{_theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": _semantic_level,
        "witness_refs": [
            f"lean-theorem:{_theorem_name}",
            "scripts/validate_scf_lifecycle_trace.py",
            "experiments/scf_lifecycle_trace/results/2026-07-02-local.json",
        ],
        "classification_basis": [_basis],
        "rationale": (
            "The result is confined to the authored finite SCF lifecycle. It does not "
            "measure evaluator independence, validate real regressions, execute rollback, "
            "enforce a production route, or promote chapter support."
        ),
    }

_constitutional_lifecycle_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean-theorem:complete_constitution_trace_reaches_exact_rollback",
        "scripts/validate_constitutional_alignment.py",
    ],
    "classification_basis": [
        "the versioned lifecycle and five rejecting controls are independently reconstructed by the constitutional-alignment validator"
    ],
}

for theorem_name in (
    "accepted_constitution_event_is_admissible",
    "accepted_constitution_event_is_exact_advance",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/Alignment.lean::{theorem_name}"] = {
        **_constitutional_lifecycle_base,
        "semantic_level": "P1",
        "rationale": "The theorem exposes accepted-step admissibility or exact transition identity for the bounded lifecycle.",
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/Alignment.lean::complete_constitution_trace_reaches_exact_rollback"
] = {
    **_constitutional_lifecycle_base,
    "semantic_level": "P2",
    "rationale": "The four-event review, activation, conflict, and rollback trace is a bounded nonvacuity witness.",
}

for theorem_name in (
    "accepted_constitution_event_preserves_custody",
    "accepted_constitution_event_is_non_authorizing",
    "accepted_activation_requires_prior_independent_review",
    "accepted_conflict_creates_one_residual",
    "self_review_cannot_enter_reviewed_stage",
    "predicate_substitution_cannot_enter_reviewed_stage",
    "authority_widening_cannot_enter_reviewed_stage",
    "action_authority_request_cannot_enter_reviewed_stage",
    "activation_version_jump_is_rejected",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/Alignment.lean::{theorem_name}"] = {
        **_constitutional_lifecycle_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem constrains one executable lifecycle boundary and is covered by an independently encoded valid trace or rejecting control."
        ),
    }

for theorem_name in (
    "constitution_run_preserves_custody_and_non_authority",
    "constitution_runs_compose",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/Alignment.lean::{theorem_name}"] = {
        **_constitutional_lifecycle_base,
        "semantic_level": "P4",
        "rationale": (
            "Structural induction proves arbitrary accepted traces preserve constitutional custody and non-authority or compose exactly across batches."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/Alignment.lean::accepted_rollback_returns_to_recorded_version"
] = {
    **_constitutional_lifecycle_base,
    "semantic_level": "P5",
    "rationale": "Every accepted rollback returns the bounded lifecycle to its recorded rollback version after residualization.",
}

_value_lease_lifecycle_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean-theorem:complete_value_lease_trace_reaches_exact_expiry",
        "scripts/validate_value_conflicts.py",
    ],
    "classification_basis": [
        "the decision-lease lifecycle and six rejecting controls are independently reconstructed by the value-conflict validator"
    ],
}

for theorem_name in (
    "accepted_value_lease_event_is_admissible",
    "accepted_value_lease_event_is_exact_advance",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ValueConflict.lean::{theorem_name}"] = {
        **_value_lease_lifecycle_base,
        "semantic_level": "P1",
        "rationale": "The theorem exposes accepted-step admissibility or exact transition identity for the bounded lease lifecycle.",
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/ValueConflict.lean::complete_value_lease_trace_reaches_exact_expiry"
] = {
    **_value_lease_lifecycle_base,
    "semantic_level": "P2",
    "rationale": "The four-event independent-review, bounded-lease, revisit, and expiry trace is a bounded nonvacuity witness.",
}

for theorem_name in (
    "accepted_value_lease_event_preserves_custody",
    "accepted_value_lease_event_is_non_authorizing",
    "accepted_value_lease_event_never_widens_authority",
    "accepted_bounded_lease_requires_review_dissent_residual_and_expiry",
    "accepted_revisit_preserves_dissent_and_adds_residual",
    "value_lease_self_review_is_rejected",
    "value_lease_stakeholder_substitution_is_rejected",
    "value_lease_missing_dissent_is_rejected",
    "value_lease_authority_widening_is_rejected",
    "value_lease_nonfuture_expiry_is_rejected",
    "value_lease_revisit_without_trigger_is_rejected",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ValueConflict.lean::{theorem_name}"] = {
        **_value_lease_lifecycle_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem constrains one executable lease boundary and is covered by an independently encoded accepted trace or rejecting control."
        ),
    }

for theorem_name in (
    "value_lease_run_preserves_custody_non_authority_and_narrowing",
    "value_lease_runs_compose",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ValueConflict.lean::{theorem_name}"] = {
        **_value_lease_lifecycle_base,
        "semantic_level": "P4",
        "rationale": (
            "Structural induction proves arbitrary accepted traces preserve lease custody, non-authority, and narrowing or compose exactly across batches."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/ValueConflict.lean::accepted_expiry_closes_lease_and_removes_constraint_ceiling"
] = {
    **_value_lease_lifecycle_base,
    "semantic_level": "P5",
    "rationale": "An accepted expiry closes the bounded constraint lease and sets its modeled authority ceiling to zero after the recorded time threshold.",
}

_agency_correction_lifecycle_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean-theorem:complete_agency_correction_trace_reaches_exact_corrected_state",
        "scripts/validate_agency_rights.py",
    ],
    "classification_basis": [
        "the correction-control lifecycle and seven rejecting controls are independently reconstructed by the agency-rights validator"
    ],
}

for theorem_name in (
    "accepted_agency_correction_event_is_admissible",
    "accepted_agency_correction_event_is_exact_advance",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Corrigibility.lean::{theorem_name}"
    ] = {
        **_agency_correction_lifecycle_base,
        "semantic_level": "P1",
        "rationale": "The theorem exposes accepted-step admissibility or exact transition identity for the bounded correction-control lifecycle.",
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/Corrigibility.lean::complete_agency_correction_trace_reaches_exact_corrected_state"
] = {
    **_agency_correction_lifecycle_base,
    "semantic_level": "P2",
    "rationale": "The five-event notice, review, bounded-control, challenge, and correction trace is a bounded nonvacuity witness.",
}

for theorem_name in (
    "accepted_agency_correction_event_preserves_custody",
    "accepted_agency_correction_event_is_non_authorizing",
    "accepted_agency_correction_event_never_widens_authority",
    "accepted_material_notice_is_recorded",
    "accepted_independent_review_records_correction_paths",
    "accepted_bounded_control_requires_review_approval_paths_and_expiry",
    "accepted_challenge_requires_affected_party_and_preexpiry",
    "agency_correction_missing_notice_is_rejected",
    "agency_correction_self_review_is_rejected",
    "agency_correction_unbounded_delegation_is_rejected",
    "agency_correction_authority_widening_is_rejected",
    "agency_correction_outsider_challenge_is_rejected",
    "agency_correction_missing_accountability_is_rejected",
    "agency_correction_consent_laundering_is_rejected",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Corrigibility.lean::{theorem_name}"
    ] = {
        **_agency_correction_lifecycle_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem constrains one executable correction-control boundary and is covered by an independently encoded accepted trace or rejecting control."
        ),
    }

for theorem_name in (
    "agency_correction_run_preserves_custody_non_authority_and_narrowing",
    "agency_correction_runs_compose",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Corrigibility.lean::{theorem_name}"
    ] = {
        **_agency_correction_lifecycle_base,
        "semantic_level": "P4",
        "rationale": (
            "Structural induction proves arbitrary accepted traces preserve correction-control custody, non-authority, and narrowing or compose exactly across batches."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/Corrigibility.lean::accepted_correction_records_accountability_residual_and_zero_ceiling"
] = {
    **_agency_correction_lifecycle_base,
    "semantic_level": "P5",
    "rationale": "An accepted bounded correction records one correction and accountability receipt, preserves a residual, and closes the modeled control ceiling.",
}

_authority_transaction_lifecycle_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean-theorem:complete_authority_transaction_trace_reaches_exact_revoked_state",
        "scripts/validate_security_kernel.py",
    ],
    "classification_basis": [
        "the eight-event authority-use transaction and nine rejecting controls are independently reconstructed by the security-kernel validator"
    ],
}

for theorem_name in (
    "accepted_authority_transaction_event_is_admissible",
    "accepted_authority_transaction_event_is_exact_advance",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/SecurityKernel.lean::{theorem_name}"
    ] = {
        **_authority_transaction_lifecycle_base,
        "semantic_level": "P1",
        "rationale": "The theorem exposes accepted-step admissibility or exact transition identity for the bounded authority-use transaction.",
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/SecurityKernel.lean::complete_authority_transaction_trace_reaches_exact_revoked_state"
] = {
    **_authority_transaction_lifecycle_base,
    "semantic_level": "P2",
    "rationale": "The eight-event lease, substitution, execution, sanitization, declassification, zeroization, commit, and revocation trace is a bounded nonvacuity witness.",
}

for theorem_name in (
    "accepted_authority_transaction_event_preserves_custody",
    "accepted_authority_transaction_event_is_non_authorizing",
    "accepted_authority_transaction_event_never_widens_authority",
    "accepted_lease_is_bounded_versioned_and_unexpired",
    "accepted_secret_injection_is_scoped_mediated_and_preexpiry",
    "accepted_sanitization_excludes_raw_secret_and_handle",
    "accepted_declassification_is_independent_and_post_sanitization",
    "accepted_commit_requires_zeroization_and_preserves_residual",
    "authority_transaction_stale_version_is_rejected",
    "authority_transaction_ambient_context_is_rejected",
    "authority_transaction_unmediated_injection_is_rejected",
    "authority_transaction_expired_injection_is_rejected",
    "authority_transaction_secret_output_is_rejected",
    "authority_transaction_self_declassification_is_rejected",
    "authority_transaction_commit_before_zeroization_is_rejected",
    "authority_transaction_partial_descendant_revocation_is_rejected",
    "authority_transaction_security_claim_laundering_is_rejected",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/SecurityKernel.lean::{theorem_name}"
    ] = {
        **_authority_transaction_lifecycle_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem constrains one executable authority-use boundary and is covered by an independently encoded accepted trace or rejecting control."
        ),
    }

for theorem_name in (
    "authority_transaction_run_preserves_custody_non_authority_and_narrowing",
    "authority_transaction_runs_compose",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/SecurityKernel.lean::{theorem_name}"
    ] = {
        **_authority_transaction_lifecycle_base,
        "semantic_level": "P4",
        "rationale": (
            "Structural induction proves arbitrary accepted transactions preserve custody, non-authority, and narrowing or compose exactly across batches."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/SecurityKernel.lean::accepted_revocation_covers_descendants_and_closes_authority"
] = {
    **_authority_transaction_lifecycle_base,
    "semantic_level": "P5",
    "rationale": "An accepted bounded revocation closes the modeled authority ceiling and records exact finite descendant coverage.",
}

_weight_custody_lifecycle_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean-theorem:complete_weight_custody_trace_reaches_exact_erased_state",
        "scripts/validate_model_weight_custody_lifecycle.py",
        "experiments/model_weight_custody_lifecycle/results/2026-07-13-local.json",
    ],
    "classification_basis": [
        "the six-event attestation-to-erasure lifecycle and nine rejecting controls are independently reconstructed by the model-weight custody validator"
    ],
}

for theorem_name in (
    "accepted_weight_custody_event_is_admissible",
    "accepted_weight_custody_event_is_exact_advance",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ModelWeightCustody.lean::{theorem_name}"] = {
        **_weight_custody_lifecycle_base, "semantic_level": "P1",
        "rationale": "The theorem exposes accepted-step admissibility or exact transition identity for the bounded custody lifecycle.",
    }

CURRENT_SEMANTIC_OVERRIDES["lean/AsiStackProofs/ModelWeightCustody.lean::complete_weight_custody_trace_reaches_exact_erased_state"] = {
    **_weight_custody_lifecycle_base, "semantic_level": "P2",
    "rationale": "The six-event attestation, key-release, load, observation, revocation, and erasure trace is a bounded nonvacuity witness.",
}

for theorem_name in (
    "accepted_weight_custody_event_preserves_identity",
    "accepted_weight_custody_event_is_non_authorizing",
    "accepted_weight_custody_event_never_widens_authority",
    "accepted_attestation_is_independent_and_future_bounded",
    "accepted_key_release_is_current_bounded_and_versioned",
    "accepted_load_requires_active_key_receipt_and_no_distribution",
    "accepted_load_observation_is_independent",
    "accepted_erasure_follows_complete_revocation_and_records_residual",
    "weight_custody_stale_version_is_rejected",
    "weight_custody_self_attestation_is_rejected",
    "weight_custody_expired_key_release_is_rejected",
    "weight_custody_authority_widening_is_rejected",
    "weight_custody_distribution_during_load_is_rejected",
    "weight_custody_self_observation_is_rejected",
    "weight_custody_partial_descendant_revocation_is_rejected",
    "weight_custody_erasure_before_revocation_is_rejected",
    "weight_custody_confidentiality_laundering_is_rejected",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ModelWeightCustody.lean::{theorem_name}"] = {
        **_weight_custody_lifecycle_base, "semantic_level": "P3",
        "rationale": "The theorem constrains one executable custody boundary and is covered by an independently encoded accepted trace or rejecting control.",
    }

for theorem_name in (
    "weight_custody_run_preserves_identity_non_authority_and_narrowing",
    "weight_custody_runs_compose",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ModelWeightCustody.lean::{theorem_name}"] = {
        **_weight_custody_lifecycle_base, "semantic_level": "P4",
        "rationale": "Structural induction proves arbitrary accepted custody traces preserve identity, non-authority, and narrowing or compose exactly across batches.",
    }

CURRENT_SEMANTIC_OVERRIDES["lean/AsiStackProofs/ModelWeightCustody.lean::accepted_key_revocation_closes_authority_and_descendants"] = {
    **_weight_custody_lifecycle_base, "semantic_level": "P5",
    "rationale": "Accepted key revocation closes the modeled authority ceiling and records exact finite descendant-key coverage.",
}

_replacement_route_base = {
    "disposition": "retain",
    "witness_refs": [
        "scripts/validate_capability_replacement.py",
        "scripts/validate_capability_replacement_trace_probe.py",
        "experiments/capability_replacement_trace/results/2026-07-02-local.json",
    ],
    "classification_basis": [
        "the theorem is a one-step finite route or projection even though its module is independently consumed"
    ],
}

for theorem_name in (
    "replacement_commit_requires_evidence_and_rollback",
    "failed_regression_blocks_replacement_promotion",
    "missing_prior_artifact_rejects_replacement",
    "authority_expansion_without_approval_routes_to_review",
    "captured_evaluator_routes_replacement_to_review",
    "failed_regression_routes_to_quarantine",
    "missing_rollback_receipt_requires_precheck",
    "failed_rollback_dry_run_routes_to_canary_only",
    "monitor_incident_requires_rollback",
    "complete_replacement_review_commits_default",
    "lifecycle_missing_candidate_rejects_replacement",
    "lifecycle_identity_mismatch_quarantines_candidate",
    "lifecycle_authority_widening_without_governance_requests_review",
    "lifecycle_stale_evidence_requires_fresh_evidence",
    "lifecycle_failed_regression_floor_quarantines_candidate",
    "lifecycle_missing_canary_scope_requires_precheck",
    "lifecycle_failed_canary_stays_canary_only",
    "lifecycle_missing_monitor_window_requires_precheck",
    "lifecycle_monitor_incident_requires_rollback",
    "lifecycle_missing_rollback_handle_requires_precheck",
    "lifecycle_failed_rollback_dry_run_stays_canary_only",
    "lifecycle_unowned_irreversible_effect_requires_residual_owner",
    "lifecycle_missing_residual_owner_requires_owner",
    "lifecycle_deprecation_without_notice_requires_notice",
    "lifecycle_retirement_without_receipt_requires_receipt",
    "lifecycle_missing_nonclaim_boundary_blocks_promotion",
    "complete_replacement_lifecycle_commits_default",
    "replacement_trace_probe_rejects_authority_widening",
    "replacement_trace_probe_preserves_no_promotion_boundary",
    "replacement_identity_sequence_bridge_preserves_identity",
    "replacement_identity_sequence_bridge_blocks_default_after_failed_monitor",
    "replacement_identity_sequence_bridge_preserves_no_promotion_boundary",
    "intent_governed_replacement_bridge_rejects_authority_widening",
    "intent_governed_replacement_bridge_preserves_no_promotion_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Replacement.lean::{theorem_name}"
    ] = {
        **_replacement_route_base,
        "semantic_level": "P1",
        "rationale": "The result is a bounded one-step route, rejection, or fixture-field consequence over authored records.",
    }

for theorem_name in (
    "replacement_trace_probe_fixture_valid",
    "replacement_identity_sequence_bridge_fixture_valid",
    "intent_governed_replacement_bridge_fixture_valid",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Replacement.lean::{theorem_name}"
    ] = {
        **_replacement_route_base,
        "semantic_level": "P0",
        "rationale": "The theorem normalizes one authored summary record and does not itself prove lifecycle reachability or refinement.",
    }

_replacement_lifecycle_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean-theorem:clean_replacement_run_satisfies_exact_commit_objective",
        "lean-theorem:failed_replacement_run_satisfies_exact_recovery_objective",
        "scripts/validate_capability_replacement_trace_probe.py",
        "experiments/capability_replacement_trace/results/2026-07-02-local.json",
    ],
    "classification_basis": [
        "the clean and failed replacement traces plus seven rejecting route/sequence controls are independently reconstructed by the replacement trace validator"
    ],
}

for theorem_name in (
    "accepted_replacement_step_is_valid",
    "accepted_replacement_step_applies_event",
    "accepted_replacement_step_adds_one_receipt",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Replacement.lean::{theorem_name}"
    ] = {
        **_replacement_lifecycle_base,
        "semantic_level": "P1",
        "rationale": "The theorem exposes accepted-step admissibility, exact transition identity, or one-step receipt accounting for the bounded replacement lifecycle.",
    }

for theorem_name in (
    "replacement_initial_state_satisfies_invariant",
    "clean_replacement_run_reaches_default",
    "failed_replacement_run_restores_prior",
    "clean_replacement_run_satisfies_exact_commit_objective",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Replacement.lean::{theorem_name}"
    ] = {
        **_replacement_lifecycle_base,
        "semantic_level": "P2",
        "rationale": "The theorem supplies a closed nonvacuity witness for the exact authored clean or failed replacement lifecycle.",
    }

for theorem_name in (
    "apply_replacement_event_preserves_identity",
    "accepted_replacement_step_preserves_non_authority",
    "accepted_replacement_step_respects_authority_ceiling",
    "accepted_replacement_step_preserves_state_invariant",
    "failed_monitor_cannot_commit_default",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Replacement.lean::{theorem_name}"
    ] = {
        **_replacement_lifecycle_base,
        "semantic_level": "P3",
        "rationale": "The theorem constrains one executable replacement step and is covered by the independently reconstructed accepted or rejecting trace surface.",
    }

for theorem_name in (
    "successful_replacement_run_preserves_identity",
    "successful_replacement_run_preserves_non_authority",
    "successful_replacement_run_respects_authority_ceiling",
    "successful_replacement_run_has_valid_trace",
    "replacement_run_composes",
    "successful_replacement_run_preserves_state_invariant",
    "accepted_replacement_step_preserves_failure_containment",
    "successful_replacement_run_preserves_failure_containment",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Replacement.lean::{theorem_name}"
    ] = {
        **_replacement_lifecycle_base,
        "semantic_level": "P4",
        "rationale": "Structural induction or exact transition analysis proves arbitrary accepted replacement traces preserve identity, authority, non-authority, coherence, failure containment, or compose across batches.",
    }

for theorem_name in (
    "accepted_rollback_restores_prior_implementation",
    "successful_run_from_failed_monitor_cannot_activate_default",
    "failed_replacement_run_satisfies_exact_recovery_objective",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Replacement.lean::{theorem_name}"
    ] = {
        **_replacement_lifecycle_base,
        "semantic_level": "P5",
        "rationale": "The theorem proves a bounded rollback or post-failure recovery property while making no production or effect-complete recovery claim.",
    }

_benchmark_ratchet_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean-theorem:clean_trace_reaches_closed_independent_review_candidate",
        "lean-theorem:saturated_trace_reaches_closed_regression_floor",
        "lean-theorem:contaminated_trace_quarantines_before_transfer",
        "lean-theorem:aggregate_pass_count_cannot_identify_promotion_admissibility",
        "scripts/validate_benchmark_fixture_bridge.py",
        "experiments/benchmark_antigoodhart/results/2026-07-02-fixture-bridge.json",
    ],
    "classification_basis": [
        "the exact 29-declaration module is independently recompiled and reconstructed over 19 bounded reachable states, 114 transitions, 12 quarantine suffixes, 11 semantic mutations, 15 lifecycle mutations, and one aggregate-score collision class"
    ],
}

for theorem_name in (
    "accepted_readiness_promotion_requires_transfer_negative_and_regression_records",
    "accepted_saturated_floor_requires_regression_records",
    "contaminated_review_cannot_promote_readiness",
    "ratchet_rejected_event_is_noninterfering",
    "ratchet_step_preserves_identity_and_authority",
    "ratchet_step_preserves_custody",
    "ratchet_custody_transitive",
    "ratchet_accepted_step_adds_exactly_one_receipt",
    "contaminated_decision_cannot_recommend_promotion",
    "saturated_decision_routes_to_regression_floor",
    "missing_transfer_check_rejected_noninterferingly",
    "missing_preserved_evidence_rejects_disposition",
    "ratchet_decision_accepted_bool_iff",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/BenchmarkRatchets.lean::{theorem_name}"
    ] = {
        **_benchmark_ratchet_base,
        "semantic_level": "P1",
        "rationale": "The result is an exact one-step route, custody, receipt, rejection, or Boolean/Prop correspondence over authored benchmark-review fields.",
    }

for theorem_name in (
    "clean_trace_reaches_closed_independent_review_candidate",
    "saturated_trace_reaches_closed_regression_floor",
    "contaminated_trace_quarantines_before_transfer",
    "clean_promotion_trace_is_accepted",
    "saturated_promotion_trace_is_accepted",
    "contaminated_quarantine_trace_is_accepted",
    "aggregate_pass_count_cannot_identify_promotion_admissibility",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/BenchmarkRatchets.lean::{theorem_name}"
    ] = {
        **_benchmark_ratchet_base,
        "semantic_level": "P2",
        "rationale": "The theorem supplies a closed nonvacuity or information-loss witness for the clean, saturated, contaminated, or same-score benchmark-review case.",
    }

for theorem_name in (
    "ratchet_step_preserves_stage_coherence",
    "quarantine_containment_survives_one_step",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/BenchmarkRatchets.lean::{theorem_name}"
    ] = {
        **_benchmark_ratchet_base,
        "semantic_level": "P3",
        "rationale": "The theorem constrains one executable lifecycle step and is exercised across the independently enumerated transition surface.",
    }

for theorem_name in (
    "run_ratchet_lifecycle_preserves_custody",
    "run_ratchet_lifecycle_preserves_stage_coherence",
    "accepted_ratchet_trace_accounts_for_every_event",
    "run_ratchet_lifecycle_append",
    "no_exact_aggregate_pass_count_promotion_classifier",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/BenchmarkRatchets.lean::{theorem_name}"
    ] = {
        **_benchmark_ratchet_base,
        "semantic_level": "P4",
        "rationale": "Structural induction, composition, or the explicit score collision proves arbitrary finite-run custody/coherence/accounting or bounded anti-Goodhart information-loss semantics.",
    }

for theorem_name in (
    "closed_ratchet_is_absorbing",
    "quarantine_containment_survives_arbitrary_suffix",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/BenchmarkRatchets.lean::{theorem_name}"
    ] = {
        **_benchmark_ratchet_base,
        "semantic_level": "P5",
        "rationale": "The theorem proves bounded terminal-state or quarantine persistence across an arbitrary finite event suffix without claiming deployed containment.",
    }

for theorem_name in (
    "integrity_accepted_step_is_accepted",
    "integrity_accepted_step_applies_event",
    "apply_event_preserves_full_identity",
    "integrity_accepted_step_advances_stage",
    "integrity_accepted_step_preserves_full_identity",
    "integrity_accepted_step_preserves_non_authority",
    "integrity_accepted_step_adds_exact_receipt",
    "apply_event_handoff_count_monotone",
    "apply_event_invalidation_count_monotone",
    "integrity_accepted_step_preserves_invariant",
    "invalidated_integrity_state_accepts_no_event",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/LearnedObjectiveIntegrity.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "a universal local transition, preservation, monotonicity, or terminal law constrains the finite authored lifecycle"
        ],
        "rationale": (
            "The result constrains one finite learned-objective integrity transition. "
            "All identities, evidence fields, reviews, and controls remain authored inputs."
        ),
    }

for theorem_name in (
    "compliant_trace_has_distinct_objective_witness",
    "compliant_behavior_alone_cannot_identify_both_worlds",
    "separating_opportunity_distinguishes_the_witness",
    "integrity_run_preserves_full_identity",
    "integrity_run_preserves_invariant",
    "integrity_run_accounts_exact_receipts",
    "integrity_run_handoff_count_monotone",
    "integrity_run_invalidation_count_monotone",
    "integrity_successful_run_has_accepted_trace",
    "integrity_run_composes_across_event_batches",
    "canonical_integrity_initial_state_is_invariant",
    "canonical_integrity_run_reaches_exact_invalidated_state",
    "full_integrity_lifecycle_reaches_invalidated_state",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/LearnedObjectiveIntegrity.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [
            "lean-theorem:canonical_integrity_run_reaches_exact_invalidated_state",
            "lean-theorem:compliant_trace_has_distinct_objective_witness",
            "scripts/validate_learned_objective_integrity.py",
        ],
        "classification_basis": [
            "a bounded non-identification witness or arbitrary-run lifecycle consequence is exercised by the independent consumer"
        ],
        "rationale": (
            "The result is nonvacuous over the two authored worlds or the exact seven-event "
            "lifecycle. It does not identify a real objective, detect deception, prove mitigation, "
            "or establish deployment behavior."
        ),
    }

for theorem_name, rationale in {
    "valid_exploratory_registration_route_derived":
        "The closed trace derives an exploratory, planning-only disposition from exact authored inputs.",
    "valid_structural_only_receipt_route_derived":
        "The closed trace derives a diagnostic-only structural receipt without route permission.",
    "valid_consumer_axis_blocked_route_derived":
        "The closed trace derives consumer blocking for an unmeasured requested axis.",
    "valid_negative_control_retirement_route_derived":
        "The closed trace derives retirement after an authored failed negative control.",
    "invalid_missing_baseline_route_rejected":
        "The closed control derives the exact missing-baseline rejection.",
    "invalid_missing_falsification_route_rejected":
        "The closed control derives the exact missing-falsification rejection.",
    "invalid_theorem_spillover_route_rejected":
        "The closed control derives rejection when structural evidence requests qualified routing.",
    "invalid_unmeasured_axis_route_rejected":
        "The closed control derives rejection when an unmeasured axis requests canary routing.",
    "invalid_failed_negative_control_promotion_route_rejected":
        "The closed control derives rejection when failed controls request qualification.",
    "invalid_missing_fallback_route_rejected":
        "The closed control derives the exact missing-fallback rejection.",
    "invalid_support_promotion_route_rejected":
        "The closed control derives rejection of a synthetic support-state promotion request.",
    "invalid_missing_non_claim_boundary_route_rejected":
        "The closed control derives rejection when the complete non-claim boundary is absent.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/SearchSubstrates.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": [
            "a closed concrete substrate-adoption trace witnesses the classifier branch"
        ],
        "rationale": rationale,
    }

for theorem_name in (
    "consumer_permission_routes_are_exact",
    "rejection_routes_never_permit_a_consumer",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/SearchSubstrates.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "universal finite route algebra separates measured permission from rejection"
        ],
        "rationale": (
            "The theorem constrains only the finite TraceRoute constructors; it does not "
            "establish that any trace input or substrate result is empirically valid."
        ),
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed authored dossier witnesses the finite semantic-memory admissibility predicate.",
    "complete_dossier_reaches_only_theseus_memory_replay": "The closed dossier reaches only Project Theseus memory-replay eligibility, not truth, useful retrieval, complete memory, support, or release.",
    "equal_aliases_do_not_force_equal_semantic_objects": "Two closed semantic identities witness equal aliases and representations with distinct object identities.",
    "identical_summary_signals_can_hide_opposite_contradiction_state": "Two histories witness opposite contradiction state under identical summary digest and retrieval score.",
    "identical_deletion_signals_can_hide_opposite_learned_influence": "Two forgetting cases witness opposite learned influence under identical storage, index, and backup-deletion signals.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/DurableSemanticMemoryReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed memory dossier, identity pair, or information-loss collision witnesses one bounded modeled result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "representation_rebuild_preserves_semantic_object_identity": "The update function changes aliases and representation digests while preserving semantic object identity for every input.",
    "every_parent_provenance_id_survives_collection": "Structural induction proves every provenance ID of every member of an arbitrary finite parent list remains collected.",
    "derived_use_cannot_exceed_any_parent_authority": "Structural induction proves all-parent purpose authorization entails authorization by each member parent.",
    "lossy_migration_without_consumer_invalidation_is_rejected": "A quantified member argument rejects every lossy migration entry that omits affected-consumer invalidation.",
    "every_used_object_has_current_authorized_provenance": "A quantified use-receipt argument derives provenance, freshness, and rights custody for every used object ID.",
    "replay_append_composes_exactly": "Structural induction proves event replay composes over concatenation for arbitrary finite event lists.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 38 memory-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 38 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 38 mutations into the lifecycle repair state.",
    "expired_memory_contract_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired memory contract.",
    "object_change_invalidates_memory_receipt": "The object-identity conjunct rejects every receipt presented for a different semantic object.",
    "ontology_change_invalidates_memory_receipt": "The ontology-version conjunct rejects every receipt presented under a different ontology.",
    "evidence_epoch_change_invalidates_memory_receipt": "The evidence-epoch conjunct rejects every receipt presented under a different evidence snapshot.",
    "consumer_purpose_change_invalidates_memory_receipt": "The purpose conjunct rejects every receipt presented for a different consumer purpose.",
    "summary_signals_cannot_recover_contradiction_state": "A same-summary/opposite-conflict collision proves no summary-signal classifier is exact for every modeled history.",
    "deletion_signals_cannot_recover_behavioral_forgetting": "A same-deletion/opposite-influence collision proves no storage-signal classifier is exact for every modeled forgetting case.",
    "open_memory_deletion_duty_blocks_context_materialization": "The consumer bridge maps an open memory deletion duty to the existing Context Transactions materialization block.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/DurableSemanticMemoryReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/durable_semantic_memory_dossier.json"],
        "classification_basis": ["a quantified induction, mutation family, migration or retrieval obligation, scope invalidation, information-loss result, or rejecting consumer is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "retrieval_benchmark_does_not_establish_semantic_truth", "persistence_replay_does_not_establish_complete_memory",
    "storage_deletion_does_not_establish_behavioral_forgetting", "graph_connectivity_does_not_establish_decision_authority",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant", "replay_eligibility_requires_admissible_dossier",
    "readiness_requires_identity", "readiness_requires_revision", "readiness_requires_migration",
    "readiness_requires_retrieval", "readiness_requires_retention", "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/DurableSemanticMemoryReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored semantic-memory state"],
        "rationale": "The theorem constrains only the encoded semantic-memory review; it establishes no truth, useful retrieval, complete memory, behavioral forgetting, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed physical-infrastructure dossier witnesses the bounded admissibility predicate.",
    "complete_dossier_reaches_only_theseus_workload_capacity_campaign": "The closed dossier reaches only Project Theseus workload-capacity campaign eligibility, not performance, sustainability, support, or release.",
    "identical_energy_headlines_can_hide_opposite_useful_delivery": "Two workload cases witness opposite useful-delivery state under identical average-power and annual-energy signals.",
    "identical_unit_efficiency_can_hide_opposite_total_impact": "Two rebound cases witness opposite total-impact state under identical unit-efficiency and unit-cost signals.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/PhysicalComputeInfrastructureReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed infrastructure dossier or information-loss collision witnesses one bounded modeled result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "aggregate_demand_append_composes": "Structural induction proves six-axis workload demand composes over concatenation for arbitrary finite workload lists.",
    "every_member_compute_demand_is_bounded_by_aggregate": "Structural induction proves every member workload's compute demand is bounded by the finite aggregate.",
    "aggregate_compute_overrun_rejects_fleet_fit": "The compute-capacity conjunct rejects every aggregate demand that exceeds the fleet envelope.",
    "attributed_energy_append_composes": "Structural induction proves attributed operational, facility, backup, and cooling energy composes over concatenation.",
    "hidden_backup_energy_breaks_exact_accounting": "Positive omitted backup energy is a quantified counterexample to exact reported-energy accounting.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 44 infrastructure-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 44 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 44 mutations into the lifecycle repair state.",
    "expired_capacity_contract_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired infrastructure contract.",
    "demand_increase_past_capacity_rejects_fit": "Natural-number order proves demand growth beyond a formerly fitting capacity rejects fit.",
    "capacity_loss_preserves_existing_overrun": "Natural-number order proves capacity loss cannot repair an existing demand overrun.",
    "workload_change_invalidates_capacity_receipt": "The workload-identity conjunct rejects a receipt presented for a different workload.",
    "site_change_invalidates_capacity_receipt": "The site-identity conjunct rejects a receipt presented at a different site.",
    "interval_change_invalidates_capacity_receipt": "The interval conjunct rejects a receipt presented outside its measured interval.",
    "hardware_change_invalidates_capacity_receipt": "The hardware-digest conjunct rejects a receipt presented for a changed configuration.",
    "meter_change_invalidates_capacity_receipt": "The meter-version conjunct rejects a receipt presented under a changed meter version.",
    "energy_headlines_cannot_recover_useful_delivery": "A same-headline/opposite-delivery collision proves no headline-signal classifier is exact for every modeled case.",
    "unit_efficiency_cannot_recover_total_impact": "A same-unit-efficiency/opposite-impact collision proves no unit-signal classifier is exact for every modeled rebound case.",
    "physical_capacity_failure_rejects_resource_budget_gate": "The consumer bridge maps absent physical capacity to the existing Resource Economics required-safety-gate rejection.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/PhysicalComputeInfrastructureReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/physical_compute_infrastructure_dossier.json"],
        "classification_basis": ["a quantified induction, mutation family, accounting counterexample, monotonicity result, scope invalidation, information-loss result, or rejecting consumer is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "device_counter_does_not_establish_delivered_useful_compute", "facility_pue_does_not_establish_sustainability",
    "renewable_contract_does_not_establish_temporal_grid_impact", "workload_energy_estimate_does_not_establish_community_acceptability",
    "outage_drill_does_not_establish_resilience", "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant", "campaign_eligibility_requires_admissible_dossier",
    "readiness_requires_identity", "readiness_requires_capacity", "readiness_requires_impact",
    "readiness_requires_resilience", "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/PhysicalComputeInfrastructureReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored infrastructure state"],
        "rationale": "The theorem constrains only the encoded physical-infrastructure review; it establishes no delivered performance, sustainability, resilience, community acceptability, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed forecast dossier witnesses the bounded admissibility predicate.",
    "complete_dossier_reaches_only_theseus_prospective_forecast_campaign": "The closed dossier reaches only Project Theseus prospective forecast campaign eligibility, not forecast truth, support, or release.",
    "identical_retrospective_fit_can_hide_opposite_prospective_coverage": "Two forecast cases witness opposite prospective-coverage state under identical retrospective-fit signals.",
    "identical_threshold_metrics_can_hide_opposite_mechanism_change": "Two measurement cases witness opposite mechanism-change state under identical threshold metrics.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/LearningTheoryForecastReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed forecast dossier or information-loss collision witnesses one bounded modeled result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "attempt_id_collection_append_composes": "Structural induction proves attempt-identity collection composes over concatenation for arbitrary finite attempt lists.",
    "every_attempt_id_survives_collection": "Structural induction proves every member attempt identity remains present in the collected finite ledger.",
    "complete_denominator_counts_every_member": "A quantified member argument derives denominator inclusion for every recorded attempt.",
    "omitted_attempt_rejects_complete_denominator": "A quantified contradiction rejects denominator completeness whenever one member attempt is marked omitted.",
    "unscored_preregistered_alternative_rejects_complete_comparison": "A quantified contradiction rejects comparison completeness whenever a preregistered alternative is unscored.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 45 forecast-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 45 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 45 mutations into the lifecycle repair state.",
    "expired_forecast_contract_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired forecast contract.",
    "extrapolation_remains_outside_support_when_observed_range_shrinks": "Natural-number order proves shrinking observed support cannot repair an already unsupported forecast scale.",
    "unscored_gap_persists_when_scored_count_falls": "Natural-number order proves scoring fewer alternatives cannot close an existing preregistered-alternative gap.",
    "population_change_invalidates_forecast_receipt": "The population-identity conjunct rejects a receipt presented for a different population.",
    "sample_process_change_invalidates_forecast_receipt": "The sample-process conjunct rejects a receipt presented under a changed sampling process.",
    "algorithm_change_invalidates_forecast_receipt": "The algorithm conjunct rejects a receipt presented for a changed learning algorithm.",
    "architecture_change_invalidates_forecast_receipt": "The architecture conjunct rejects a receipt presented for a changed architecture.",
    "metric_change_invalidates_forecast_receipt": "The metric conjunct rejects a receipt presented under a changed evaluation metric.",
    "compute_regime_change_invalidates_forecast_receipt": "The compute-regime conjunct rejects a receipt presented under changed compute.",
    "horizon_change_invalidates_forecast_receipt": "The forecast-horizon conjunct rejects a receipt presented outside its bound horizon.",
    "retrospective_fit_cannot_recover_prospective_coverage": "A same-fit/opposite-coverage collision proves no retrospective-fit classifier is exact for every modeled forecast.",
    "threshold_metrics_cannot_recover_mechanism_change": "A same-threshold/opposite-mechanism collision proves no threshold-metric classifier is exact for every modeled case.",
    "missing_prospective_holdout_rejects_benchmark_ratchet_promotion": "The consumer bridge maps absent prospective holdout custody to the existing Benchmark Ratchet readiness rejection.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/LearningTheoryForecastReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/learning_theory_forecast_dossier.json"],
        "classification_basis": ["a quantified induction, mutation family, denominator obligation, monotonicity result, scope invalidation, information-loss result, or rejecting consumer is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "training_fit_does_not_establish_broad_generalization", "iid_holdout_does_not_establish_distribution_transfer",
    "retrospective_scaling_fit_does_not_establish_future_scaling_behavior", "compression_score_does_not_establish_safety",
    "threshold_benchmark_does_not_establish_mechanism_emergence", "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant", "campaign_eligibility_requires_admissible_dossier",
    "readiness_requires_identity", "readiness_requires_design", "readiness_requires_transfer",
    "readiness_requires_lifecycle", "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/LearningTheoryForecastReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored forecast-review state"],
        "rationale": "The theorem constrains only the encoded forecast review; it establishes no generalization, transfer, emergence, scaling accuracy, calibration, safety, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed experiment dossier witnesses the bounded admissibility predicate.",
    "complete_dossier_reaches_only_theseus_governed_experiment_campaign": "The closed dossier reaches only Project Theseus governed experiment campaign eligibility, not scientific truth, support, or release.",
    "identical_significance_can_hide_opposite_preregistration_integrity": "Two experiment cases witness opposite preregistration integrity under identical significance signals.",
    "identical_replication_counts_can_hide_opposite_independence": "Two replication cases witness opposite independence under identical success-count signals.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ScientificExperimentReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed experiment dossier or information-loss collision witnesses one bounded modeled result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "attempt_id_collection_append_composes": "Structural induction proves attempt-identity collection composes over concatenation for arbitrary finite experiment lists.",
    "every_attempt_id_survives_collection": "Structural induction proves every member attempt identity remains present in the collected finite ledger.",
    "complete_denominator_counts_every_attempt": "A quantified member argument derives denominator inclusion for every recorded attempt.",
    "omitted_attempt_rejects_complete_denominator": "A quantified contradiction rejects denominator completeness whenever one member attempt is omitted.",
    "outcome_exposed_branch_rejects_confirmatory_integrity": "A quantified contradiction rejects confirmatory integrity when protected outcomes were opened.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 54 experiment-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 54 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 54 mutations into the lifecycle repair state.",
    "expired_experiment_contract_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired experiment contract.",
    "omitted_attempt_gap_persists_when_included_count_falls": "Natural-number order proves counting fewer attempts cannot close an existing denominator gap.",
    "replication_gap_persists_when_independent_count_falls": "Natural-number order proves fewer independent replications cannot close an existing replication gap.",
    "hypothesis_change_invalidates_experiment_receipt": "The hypothesis-identity conjunct rejects a receipt presented for a different hypothesis.",
    "protocol_change_invalidates_experiment_receipt": "The protocol-version conjunct rejects a receipt presented under a changed protocol.",
    "instrument_change_invalidates_experiment_receipt": "The instrument-version conjunct rejects a receipt presented under a changed instrument.",
    "data_change_invalidates_experiment_receipt": "The data-snapshot conjunct rejects a receipt presented for changed data.",
    "analysis_change_invalidates_experiment_receipt": "The analysis-version conjunct rejects a receipt presented under a changed analysis.",
    "environment_change_invalidates_experiment_receipt": "The environment conjunct rejects a receipt presented in a changed environment.",
    "claim_ceiling_change_invalidates_experiment_receipt": "The claim-ceiling conjunct rejects a receipt presented for a changed inference ceiling.",
    "significance_signals_cannot_recover_preregistration_integrity": "A same-significance/opposite-preregistration collision proves no significance classifier is exact for every modeled experiment.",
    "replication_counts_cannot_recover_independence": "A same-count/opposite-independence collision proves no replication-count classifier is exact for every modeled replication.",
    "missing_independent_replication_blocks_empirical_support_promotion": "The Evidence States bridge rejects empirical support promotion without an empirical replication witness.",
    "missing_null_results_rejects_benchmark_ratchet_promotion": "The Benchmark Ratchets bridge rejects readiness promotion when null results are absent.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ScientificExperimentReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/scientific_experiment_dossier.json"],
        "classification_basis": ["a quantified induction, mutation family, denominator obligation, confirmatory counterexample, monotonicity result, scope invalidation, information-loss result, or rejecting consumer is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "generated_hypothesis_does_not_establish_discovery", "completed_experiment_does_not_establish_causal_truth",
    "significant_result_does_not_establish_reproducibility", "replay_does_not_establish_independent_replication",
    "dual_use_review_does_not_establish_safety", "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant", "campaign_eligibility_requires_admissible_dossier",
    "readiness_requires_identity", "readiness_requires_design", "readiness_requires_execution",
    "readiness_requires_analysis", "readiness_requires_replication", "readiness_requires_governance",
    "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/ScientificExperimentReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored experiment-review state"],
        "rationale": "The theorem constrains only the encoded experiment review; it establishes no hypothesis truth, causal identification, instrument accuracy, reproducibility, discovery, laboratory safety, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed transition dossier witnesses the bounded admissibility predicate.",
    "complete_dossier_reaches_only_theseus_governed_transition_study": "The closed dossier reaches only Project Theseus governed transition-study eligibility, not deployment, support, or release.",
    "positive_aggregate_can_coexist_with_unremedied_harm": "A closed two-cohort witness has positive aggregate gain while one worker cohort remains unremedied.",
    "identical_aggregate_signals_can_hide_opposite_harm_status": "Two transition cases witness opposite harmed-cohort status under identical productivity and aggregate-gain signals.",
    "identical_approval_counts_can_hide_opposite_practical_agency": "Two transition cases witness opposite practical-refusal status under identical approval and human-review counts.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/DeploymentTransitionGovernance.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed transition dossier, aggregate-harm witness, or information-loss collision witnesses one bounded modeled result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "beating_human_alone_does_not_establish_complementarity": "A closed score witness beats the human component while losing to the AI component.",
    "beating_ai_alone_does_not_establish_complementarity": "A closed score witness beats the AI component while losing to the human component.",
    "equal_to_strongest_component_does_not_establish_complementarity": "A closed score witness ties rather than beats the strongest component.",
    "assistance_grant_does_not_authorize_model_training": "A closed purpose witness separates assistance from model-training authority.",
    "sensing_grant_does_not_authorize_employment_use": "A closed purpose witness separates neural sensing from employment authority.",
    "personalization_grant_does_not_authorize_advertising": "A closed purpose witness separates personalization from advertising authority.",
    "stimulation_grant_does_not_authorize_surveillance": "A closed purpose witness separates stimulation from surveillance authority.",
    "complete_dossier_is_ready": "The closed coupling dossier witnesses the bounded admissibility predicate.",
    "complete_dossier_reaches_only_theseus_low_risk_coupling_study": "The closed dossier reaches only Project Theseus low-risk coupling-study eligibility, not human intervention, support, or release.",
    "identical_revocation_signals_can_hide_opposite_practical_exit": "Two coupling cases witness opposite practical-exit status under identical revocation signals.",
    "identical_session_signals_can_hide_opposite_post_exit_retention": "Two coupling cases witness opposite post-exit retention under identical session metrics.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/HumanAICognitiveSovereignty.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed comparator, purpose, dossier, or information-loss witness establishes one bounded modeled result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed relational-compiler dossier witnesses the bounded admissibility predicate.",
    "complete_dossier_reaches_only_theseus_relational_compiler_study": "The closed dossier reaches only Project Theseus relational-compiler-study eligibility, not substrate adoption, support, or release.",
    "identical_qualification_metrics_can_hide_opposite_role_fidelity": "Two compiler cases witness opposite role fidelity under identical score, latency, and memory bands.",
    "identical_rescue_records_can_hide_opposite_rescue_competence": "Two compiler cases witness opposite lower-order competence under identical named-rescue records.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/RelationalDimensionCompiler.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed dossier or information-loss collision witnesses one bounded relational-compiler result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "role_id_collection_append_composes": "Structural induction proves role-identity collection composes over finite concatenation.",
    "every_role_id_survives_collection": "Structural induction proves every member role identity survives finite collection.",
    "entity_remapping_preserves_role_identity": "Structural induction proves entity remapping leaves the role-identity sequence unchanged.",
    "complete_role_schema_covers_every_required_role": "A quantified required-role argument derives a typed binding witness.",
    "omitted_required_role_rejects_complete_schema": "A quantified contradiction rejects role-schema completeness when a required role is omitted.",
    "candidate_id_collection_append_composes": "Structural induction proves candidate-identity collection composes over finite concatenation.",
    "every_candidate_id_survives_collection": "Structural induction proves every member candidate identity survives finite collection.",
    "complete_proposal_denominator_covers_every_expected_candidate": "A quantified expected-candidate argument derives an attempted retained witness.",
    "omitted_candidate_rejects_complete_proposal_denominator": "A quantified contradiction rejects proposal completeness when an expected candidate is hidden.",
    "descendants_closed_append_iff": "A two-direction finite-list proof shows descendant closure composes exactly over concatenation.",
    "active_descendant_blocks_contraction_closure": "A quantified member contradiction rejects contraction closure when one dependent remains active.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 54 compiler-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 54 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 54 mutations into the lifecycle repair state.",
    "expired_compiler_contract_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired compiler contract.",
    "candidate_budget_overrun_persists_when_generated_count_grows": "Natural-number order proves generating more candidates cannot close an existing budget overrun.",
    "proposal_change_invalidates_compiler_receipt": "The proposal-identity conjunct rejects a receipt presented for a changed candidate.",
    "compiler_version_change_invalidates_compiler_receipt": "The compiler-version conjunct rejects a receipt presented under changed compiler code.",
    "role_schema_change_invalidates_compiler_receipt": "The role-schema conjunct rejects a receipt presented for changed role semantics.",
    "rescue_suite_change_invalidates_compiler_receipt": "The rescue-suite conjunct rejects a receipt presented under changed baselines.",
    "qualification_suite_change_invalidates_compiler_receipt": "The qualification-suite conjunct rejects a receipt presented under changed evaluation.",
    "fallback_change_invalidates_compiler_receipt": "The fallback conjunct rejects a receipt presented under a changed inverse path.",
    "authority_change_invalidates_compiler_receipt": "The authority conjunct rejects a receipt presented under changed compiler authority.",
    "qualification_metrics_cannot_recover_role_fidelity": "A same-metrics/opposite-role collision proves no qualification-metric classifier is exact for every modeled case.",
    "rescue_records_cannot_recover_lower_order_competence": "A same-record/opposite-competence collision proves no rescue-record classifier is exact for every modeled case.",
    "missing_lower_order_rescue_rejects_substrate_consumer": "The Search Substrates bridge rejects adoption fields with a missing baseline.",
    "unqualified_compiler_routes_runtime_to_fallback": "The Routing bridge sends a not-ready compiler route to its executable fallback.",
    "missing_compiler_experiment_blocks_empirical_support_promotion": "The Evidence States bridge rejects empirical promotion without a compiler-experiment witness.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/RelationalDimensionCompiler.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/relational_dimension_compiler_dossier.json"],
        "classification_basis": ["a quantified induction, transformation invariant, mutation family, denominator or descendant obligation, monotonicity result, scope invalidation, information-loss result, or rejecting consumer is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "study_eligibility_requires_admissible_dossier", "readiness_requires_identity",
    "readiness_requires_typing", "readiness_requires_rescues",
    "readiness_requires_qualification", "readiness_requires_compilation",
    "readiness_requires_contraction", "readiness_requires_nonclaim_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/RelationalDimensionCompiler.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a universal finite lifecycle invariant or grouped necessity result constrains authored relational-compiler review state"],
        "rationale": "The theorem constrains only the encoded compiler review; it establishes no irreducibility, usefulness, efficiency, natural-task transfer, bounded primitive arity, safe adaptation, support, or substrate authority.",
    }

for theorem_name, rationale in {
    "beats_both_components_requires_human_baseline": "Projection from the two-component predicate preserves the human-baseline obligation.",
    "beats_both_components_requires_ai_baseline": "Projection from the two-component predicate preserves the AI-baseline obligation.",
    "single_purpose_grant_is_exact": "Decidable equality proves the finite purpose grant authorizes exactly its named purpose.",
    "revoked_purpose_lease_blocks_authorization": "A contradiction on the revocation field rejects authorization for every modeled lease.",
    "expired_purpose_lease_blocks_authorization": "Natural-number order rejects authorization for every expired modeled lease.",
    "unrelated_purpose_blocks_authorization": "Purpose inequality rejects authorization for every mismatched modeled lease.",
    "participant_id_collection_append_composes": "Structural induction proves participant-identity collection composes over concatenation.",
    "every_participant_id_survives_collection": "Structural induction proves every participant identity survives finite collection.",
    "complete_longitudinal_denominator_covers_every_expected_participant": "A quantified expected-member argument derives complete longitudinal custody.",
    "omitted_post_exit_checkpoint_rejects_complete_denominator": "A quantified contradiction rejects completeness when one expected participant lacks post-exit follow-up.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 49 coupling-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 49 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 49 mutations into the lifecycle repair state.",
    "expired_coupling_contract_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired coupling contract.",
    "post_exit_gap_persists_when_observation_count_falls": "Natural-number order proves fewer post-exit observations cannot close an existing denominator gap.",
    "participant_set_change_invalidates_coupling_receipt": "The participant-set conjunct rejects a receipt presented for a changed cohort.",
    "protocol_change_invalidates_coupling_receipt": "The protocol-version conjunct rejects a receipt presented under a changed protocol.",
    "device_or_model_change_invalidates_coupling_receipt": "The device/model conjunct rejects a receipt presented for changed technical state.",
    "purpose_change_invalidates_coupling_receipt": "The purpose-grant conjunct rejects a receipt presented for changed use.",
    "observation_schedule_change_invalidates_coupling_receipt": "The observation-schedule conjunct rejects a receipt under changed follow-up.",
    "exit_plan_change_invalidates_coupling_receipt": "The exit-plan conjunct rejects a receipt under changed practical-exit provisions.",
    "authority_change_invalidates_coupling_receipt": "The authority conjunct rejects a receipt under changed coupling authority.",
    "revocation_signals_cannot_recover_practical_exit": "A same-signal/opposite-exit collision proves no revocation-signal classifier is exact for every modeled case.",
    "session_signals_cannot_recover_post_exit_skill_retention": "A same-session/opposite-retention collision proves no session-signal classifier is exact for every modeled case.",
    "unrelated_mental_data_use_rejects_privacy_consumer": "The Privacy Information Flow bridge rejects a purpose-drifted mental-data use.",
    "missing_pause_channel_rejects_human_control_consumer": "The Human Factors bridge reduces autonomy when the intervention channel is unreachable.",
    "missing_longitudinal_study_blocks_empirical_support_promotion": "The Evidence States bridge rejects empirical promotion without a longitudinal-study witness.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/HumanAICognitiveSovereignty.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/human_ai_cognitive_sovereignty_dossier.json"],
        "classification_basis": ["a quantified projection, induction, mutation family, authorization rule, denominator obligation, monotonicity result, scope invalidation, information-loss result, or rejecting consumer is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "study_eligibility_requires_admissible_dossier", "readiness_requires_identity",
    "readiness_requires_comparators", "readiness_requires_authorization",
    "readiness_requires_data_custody", "readiness_requires_exit_capacity",
    "readiness_requires_observation", "readiness_requires_nonclaim_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/HumanAICognitiveSovereignty.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a universal finite lifecycle invariant or grouped necessity result constrains authored human-AI coupling review state"],
        "rationale": "The theorem constrains only the encoded coupling review; it establishes no beneficial symbiosis, genuine consent, mental integrity, clinical efficacy, equity, neural safety, support, or intervention authority.",
    }

for theorem_name, rationale in {
    "cohort_id_collection_append_composes": "Structural induction proves cohort-identity collection composes over concatenation for arbitrary finite transition ledgers.",
    "every_cohort_id_survives_collection": "Structural induction proves every member cohort identity remains present in the collected finite ledger.",
    "complete_denominator_covers_every_expected_cohort": "A quantified expected-member argument derives an included cohort witness from denominator completeness.",
    "omitted_expected_cohort_rejects_complete_denominator": "A quantified contradiction rejects denominator completeness when an expected cohort is omitted.",
    "fully_remedied_append_iff": "A two-direction finite-list proof shows remedy completeness composes exactly over ledger concatenation.",
    "unremedied_member_blocks_transition_acceptance": "A quantified member contradiction rejects full remedy when one cohort has a strict remedy gap.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 54 transition-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 54 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 54 mutations into the lifecycle repair state.",
    "expired_transition_contract_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired transition contract.",
    "affected_denominator_gap_persists_when_observed_count_falls": "Natural-number order proves observing fewer affected cohorts cannot close an existing denominator gap.",
    "remedy_gap_persists_when_delivered_amount_falls": "Natural-number order proves delivering less remedy cannot close an existing burden gap.",
    "deployment_change_invalidates_transition_receipt": "The deployment-identity conjunct rejects a receipt presented for a changed deployment.",
    "baseline_change_invalidates_transition_receipt": "The counterfactual-baseline conjunct rejects a receipt presented under a changed baseline.",
    "contract_version_change_invalidates_transition_receipt": "The contract-version conjunct rejects a receipt presented under a changed transition contract.",
    "denominator_change_invalidates_transition_receipt": "The affected-denominator conjunct rejects a receipt presented for a changed population.",
    "observation_schedule_change_invalidates_transition_receipt": "The observation-schedule conjunct rejects a receipt presented under a changed follow-up schedule.",
    "remedy_plan_change_invalidates_transition_receipt": "The remedy-plan conjunct rejects a receipt presented under a changed remedy plan.",
    "authority_change_invalidates_transition_receipt": "The authority conjunct rejects a receipt presented under changed transition authority.",
    "aggregate_signals_cannot_recover_harmed_cohort_status": "A same-aggregate/opposite-harm collision proves no aggregate-signal classifier is exact for every modeled transition.",
    "approval_counts_cannot_recover_practical_agency": "A same-count/opposite-refusal collision proves no approval-count classifier is exact for every modeled transition.",
    "missing_transition_remedy_blocks_accountability_consumer": "The Human-AI Organizations bridge routes a transition without remedy to the existing accountability repair state.",
    "missing_transition_checks_reject_readiness_consumer": "The Readiness Gates bridge rejects a canary decision when required transition checks fail.",
    "missing_transition_study_blocks_empirical_support_promotion": "The Evidence States bridge rejects empirical support promotion without a transition-study witness.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/DeploymentTransitionGovernance.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/deployment_transition_dossier.json"],
        "classification_basis": ["a quantified induction, mutation family, denominator or remedy obligation, monotonicity result, scope invalidation, information-loss result, or rejecting consumer is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "exposure_does_not_establish_displacement", "adoption_does_not_establish_welfare",
    "productivity_does_not_establish_distributional_benefit", "approval_click_does_not_establish_agency",
    "aggregate_gain_does_not_establish_successful_transition", "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant", "study_eligibility_requires_admissible_dossier",
    "readiness_requires_identity", "readiness_requires_design", "readiness_requires_accounting",
    "readiness_requires_agency", "readiness_requires_capacity", "readiness_requires_remedy",
    "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/DeploymentTransitionGovernance.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored deployment-transition review state"],
        "rationale": "The theorem constrains only the encoded transition review; it establishes no causal deployment effect, welfare, fairness, meaningful agency, lawful remedy, service continuity, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed harmless dossier witnesses the finite admissibility predicate.",
    "complete_dossier_reaches_only_harmless_release_case": "The closed dossier reaches only harmless Theseus campaign eligibility, not release authority.",
    "identical_official_lineage_can_hide_opposite_copy_control": "Two ecosystem states witness opposite copy-control results under identical official lineage.",
    "identical_default_evaluation_can_hide_opposite_derivative_state": "Two derivative states witness opposite safeguard states under identical default evaluation.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/OpenWeightReleaseReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed harmless dossier or collision pair witnesses one bounded modeled result"],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 36 admission-axis mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 36 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 36 mutations into the lifecycle repair state.",
    "expired_frontier_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired comparator frontier.",
    "public_copy_irreversibility_is_monotone": "Natural-number order proves nondecreasing positive public copies remain incompatible with universal recall.",
    "official_lineage_cannot_recover_universal_copy_control": "A same-lineage/opposite-control collision proves no lineage-only classifier is exact for every modeled ecosystem.",
    "default_evaluation_cannot_recover_derivative_safeguard_state": "A same-default/opposite-derivative collision proves no default-evaluation-only classifier is exact for every modeled derivative.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/OpenWeightReleaseReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P3",
        "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/open_weight_release_dossier.json"],
        "classification_basis": ["a quantified mutation, arithmetic monotonicity, or non-identifiability result is independently reconstructed"],
        "rationale": rationale,
    }

for theorem_name in (
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "simulation_eligibility_requires_admissible_dossier", "readiness_requires_artifact",
    "readiness_requires_alternatives", "readiness_requires_derivative_review",
    "readiness_requires_distribution_review", "readiness_requires_post_release_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/OpenWeightReleaseReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a universal finite lifecycle invariant or grouped necessity result constrains authored release-review state"],
        "rationale": "The theorem constrains only the six-step authored review; it establishes no release merit, recall, safety, support, or authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed benign dossier witnesses the finite communication-review predicate.",
    "complete_dossier_reaches_only_benign_study": "The closed dossier reaches only benign Theseus study eligibility, not delivery authority.",
    "identical_surface_signals_can_hide_opposite_influence_state": "Two influence cases witness opposite bounded states under identical factuality, consent, persuasion, and disclosure signals.",
    "identical_provenance_can_hide_opposite_comprehension": "Two recipient cases witness opposite comprehension under identical provenance.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CommunicationInfluenceReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed benign dossier or collision pair witnesses one bounded modeled result"],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 42 admission-axis mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 42 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 42 mutations into the lifecycle repair state.",
    "expired_packet_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired packet.",
    "audience_overrun_persists_under_more_reach_and_no_larger_ceiling": "Natural-number order preserves audience-overrun rejection as reach grows and its ceiling does not.",
    "repetition_overrun_persists_under_more_repetition_and_no_larger_ceiling": "Natural-number order preserves repetition-overrun rejection as repetition grows and its ceiling does not.",
    "denied_attribute_noninterference": "A typed projection theorem makes every allowed-context policy invariant to denied attributes outside its input type.",
    "factuality_consent_persuasion_and_disclosure_cannot_recover_influence_state": "A same-surface/opposite-state collision proves no surface-only classifier is exact for every modeled influence case.",
    "provenance_cannot_recover_recipient_comprehension": "A same-provenance/opposite-comprehension collision proves no provenance-only classifier is exact for every modeled recipient case.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CommunicationInfluenceReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P3",
        "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/communication_influence_dossier.json"],
        "classification_basis": ["a quantified mutation, arithmetic monotonicity, typed noninterference, or non-identifiability result is independently reconstructed"],
        "rationale": rationale,
    }

for theorem_name in (
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "study_eligibility_requires_admissible_dossier", "readiness_requires_claim_provenance",
    "readiness_requires_audience_autonomy", "readiness_requires_delivery_envelope",
    "readiness_requires_correction_observation", "readiness_requires_non_authority_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CommunicationInfluenceReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a universal finite lifecycle invariant or grouped necessity result constrains authored communication-review state"],
        "rationale": "The theorem constrains only the six-stage authored review; it establishes no comprehension, autonomy, persuasion effect, correction effect, support, or delivery authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed authored dossier witnesses the finite objective-lease admissibility predicate.",
    "complete_dossier_reaches_only_objective_registry_study": "The closed dossier reaches only Project Theseus objective-registry study eligibility, not optimization authority.",
    "identical_proxy_observation_can_hide_opposite_target_movement": "Two target cases witness opposite target movement under the same proxy score and evaluator version.",
    "identical_preference_prediction_can_hide_opposite_authority": "Two authority cases witness opposite authorization under the same preference prediction and confidence.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ObjectiveLeaseGovernance.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed objective dossier or collision pair witnesses one bounded modeled result"],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "retire_all_closes_every_finite_binding": "Structural induction proves every member of an arbitrary finite descendant list is inactive after the modeled retirement map.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 46 admission-axis mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 46 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 46 mutations into the lifecycle repair state.",
    "expired_lease_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired objective lease.",
    "consumer_lease_is_nontransferable": "The consumer identity conjunct rejects use by every different consumer.",
    "ontology_change_invalidates_use": "The ontology-version conjunct rejects use after any unequal ontology change.",
    "authority_change_invalidates_use": "The authority-version conjunct rejects use after any unequal authority change.",
    "proxy_score_and_evaluator_cannot_recover_target_improvement": "A same-proxy/opposite-target collision proves no proxy-observation classifier is exact for every modeled target case.",
    "predicted_preference_cannot_recover_authority": "A same-prediction/opposite-authority collision proves no preference-only classifier is exact for every modeled authority case.",
    "ready_dossier_supplies_bounded_learned_objective_consumer_fields": "A ready objective dossier refines only named bounded fields in the learned-objective consumer while setting certainty and authority overclaims false.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ObjectiveLeaseGovernance.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P3",
        "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/objective_lease_dossier.json"],
        "classification_basis": ["a quantified mutation, finite induction, lease invalidation, non-identifiability, or consumer-refinement result is independently reconstructed"],
        "rationale": rationale,
    }

for theorem_name in (
    "optimizer_cannot_self_ratify", "reward_model_cannot_ratify", "evaluator_cannot_ratify",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "study_eligibility_requires_admissible_dossier", "readiness_requires_charter",
    "readiness_requires_target_proxy_separation", "readiness_requires_plurality",
    "readiness_requires_lease", "readiness_requires_challenge",
    "readiness_requires_retirement_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ObjectiveLeaseGovernance.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed role decision, universal finite lifecycle invariant, or grouped necessity result constrains authored objective-lease state"],
        "rationale": "The theorem constrains only the encoded objective-lease review; it establishes no correct value, consent, legitimacy, behavioral alignment, support, or optimization authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed authored dossier witnesses the finite adversarial-model-security admissibility predicate.",
    "complete_dossier_reaches_only_model_security_campaign": "The closed dossier reaches only Project Theseus model-security campaign eligibility, not deployment or attack authority.",
    "identical_aggregate_signals_can_hide_opposite_security_state": "Two model-security cases witness opposite bounded states under identical clean accuracy, failed-attack count, red-team coverage, and certificate signals.",
    "identical_local_checks_can_hide_opposite_composition_state": "Two composition cases witness opposite cross-boundary attack-path reachability under identical local component checks.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/AdversarialModelSecurity.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed threat dossier or collision pair witnesses one bounded modeled result"],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "quarantine_all_covers_every_finite_trace": "Structural induction proves every member of an arbitrary finite attack-trace list is quarantined by the modeled map.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 58 admission-axis mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 58 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 58 mutations into the lifecycle repair state.",
    "expired_disposition_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired bounded disposition.",
    "checkpoint_change_invalidates_disposition": "The checkpoint-identity conjunct rejects every disposition presented for a different checkpoint.",
    "configuration_change_invalidates_disposition": "The serving-configuration conjunct rejects every disposition presented for a different configuration.",
    "budget_widening_invalidates_disposition": "The attacker-budget conjunct rejects every disposition presented under a widened budget.",
    "aggregate_scores_cannot_recover_bounded_security_state": "A same-aggregate/opposite-state collision proves no aggregate-signal classifier is exact for every modeled security case.",
    "local_component_checks_cannot_recover_attack_path_reachability": "A same-local-check/opposite-composition collision proves no local-check classifier is exact for every modeled composition case.",
    "ready_dossier_supplies_bounded_adversarial_evaluation_fields": "A ready threat dossier refines only named bounded fields in the adversarial-evaluation consumer while leaving robustness, release, and support overclaims false.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/AdversarialModelSecurity.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P3",
        "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/adversarial_model_security_dossier.json"],
        "classification_basis": ["a quantified mutation, finite induction, disposition invalidation, non-identifiability, or consumer-refinement result is independently reconstructed"],
        "rationale": rationale,
    }

for theorem_name in (
    "certificate_does_not_discharge_monitoring", "monitoring_does_not_discharge_recovery",
    "recovery_does_not_discharge_certificate", "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant", "campaign_eligibility_requires_admissible_dossier",
    "readiness_requires_identity", "readiness_requires_threat", "readiness_requires_challenge",
    "readiness_requires_observation", "readiness_requires_recovery", "readiness_requires_assurance",
    "readiness_requires_disclosure_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/AdversarialModelSecurity.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed assurance decision, universal finite lifecycle invariant, or grouped necessity result constrains authored threat-review state"],
        "rationale": "The theorem constrains only the encoded adversarial-model-security review; it establishes no robustness, exploitability, defense efficacy, recovery efficacy, support, deployment, or attack authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed authored dossier witnesses the finite protected-computation admissibility predicate.",
    "complete_dossier_reaches_only_protected_computation_campaign": "The closed dossier reaches only Project Theseus protected-computation campaign eligibility, not execution, privacy, or release authority.",
    "identical_evidence_signals_can_hide_opposite_semantic_authority_state": "Two interpretation cases witness opposite semantic-authorization states under identical attestation, relation-proof, and confidentiality signals.",
    "identical_component_guarantees_can_hide_opposite_end_to_end_privacy": "Two privacy cases witness opposite end-to-end states under identical input-confidentiality, model-confidentiality, and computation-integrity signals.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProtectedComputationReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed protected-computation dossier or collision pair witnesses one bounded modeled result"],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "account_all_covers_every_finite_leakage_channel": "Structural induction proves every member of an arbitrary finite leakage-channel list is marked accounted by the modeled map.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 48 admission-axis mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 48 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 48 mutations into the lifecycle repair state.",
    "expired_receipt_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired protected-computation receipt.",
    "leakage_overrun_persists_under_more_observation_and_no_larger_budget": "Natural-number order preserves leakage-overrun rejection under more observation and no larger allowance.",
    "artifact_change_invalidates_receipt": "The artifact-identity conjunct rejects every receipt presented for a different artifact.",
    "verifier_policy_change_invalidates_receipt": "The verifier-policy conjunct rejects every receipt presented under a different policy.",
    "evidence_epoch_change_invalidates_receipt": "The evidence-epoch conjunct rejects every receipt presented in a different epoch.",
    "unprotected_fallback_without_separate_authorization_is_blocked": "The typed fallback relation excludes every unprotected path that lacks separate authorization.",
    "silent_unprotected_fallback_is_blocked": "The typed fallback relation excludes every unprotected path hidden from its consumer.",
    "evidence_signals_cannot_recover_semantic_authority": "A same-evidence/opposite-interpretation collision proves no evidence-signal classifier is exact for every modeled interpretation case.",
    "component_guarantees_cannot_recover_end_to_end_privacy": "A same-component/opposite-privacy collision proves no component-guarantee classifier is exact for every modeled privacy case.",
    "protected_execution_receipt_cannot_substitute_for_privacy_authorization": "The consumer refinement deliberately leaves purpose and authority false, making the existing Privacy Information Flow owner reject the receipt.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProtectedComputationReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P3",
        "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/protected_computation_dossier.json"],
        "classification_basis": ["a quantified mutation, finite induction, scope invalidation, fallback rule, non-identifiability result, or rejecting consumer refinement is independently reconstructed"],
        "rationale": rationale,
    }

for theorem_name in (
    "attestation_does_not_establish_semantic_correctness",
    "encoded_relation_proof_does_not_establish_authorization",
    "confidentiality_mechanism_does_not_establish_end_to_end_privacy",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "campaign_eligibility_requires_admissible_dossier", "readiness_requires_identity",
    "readiness_requires_guarantees", "readiness_requires_evidence",
    "readiness_requires_freshness", "readiness_requires_leakage",
    "readiness_requires_fallback", "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProtectedComputationReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored protected-computation state"],
        "rationale": "The theorem constrains only the encoded protected-computation review; it establishes no cryptographic soundness, hardware trust, measured privacy, authorization, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_envelope_is_ready": "The closed authored envelope witnesses the finite content-authenticity admissibility predicate.",
    "complete_envelope_reaches_only_authenticity_campaign": "The closed envelope reaches only Project Theseus authenticity-campaign eligibility, not a truth, compliance, support, or release judgment.",
    "identical_authenticity_signals_can_hide_opposite_truth_state": "Two cases witness opposite semantic-truth states under identical provenance, watermark, detector, and disclosure signals.",
    "identical_absence_signals_can_hide_opposite_origin": "Two cases witness human and synthetic origins under the same absent credential, watermark, and detector signals.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ContentAuthenticityReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed authenticity envelope or collision pair witnesses one bounded modeled result"],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "check_all_covers_every_finite_transformation": "Structural induction proves every member of an arbitrary finite transformation list is checked by the modeled map.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 42 authenticity-envelope mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 42 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 42 mutations into the lifecycle repair state.",
    "expired_envelope_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired authenticity envelope.",
    "stale_signer_status_remains_stale_when_current_epoch_advances": "Natural-number order proves advancing the current signer epoch cannot restore a stale signer check.",
    "asset_change_invalidates_authenticity_receipt": "The asset-identity conjunct rejects every receipt presented for a different asset.",
    "trust_policy_change_invalidates_authenticity_receipt": "The trust-policy conjunct rejects every receipt presented under a different policy.",
    "transformation_change_invalidates_authenticity_receipt": "The transformation-digest conjunct rejects every receipt presented for a different transformation state.",
    "signer_epoch_change_invalidates_authenticity_receipt": "The signer-epoch conjunct rejects every receipt presented after signer-state drift.",
    "unsupported_transformation_cannot_claim_verified_preservation": "The typed transformation relation excludes verified preservation for every unsupported transformation.",
    "composite_without_region_binding_is_blocked": "The typed transformation relation excludes every composite whose regions are not bound.",
    "authenticity_signals_cannot_recover_semantic_truth": "A same-signal/opposite-truth collision proves no authenticity-signal classifier is exact for every modeled case.",
    "absence_signals_cannot_recover_human_origin": "A same-absence/opposite-origin collision proves no absence-only classifier is exact for every modeled case.",
    "authenticity_receipt_cannot_substitute_for_recipient_comprehension": "The consumer refinement deliberately leaves comprehension false, so accessible disclosure does not become recipient understanding.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ContentAuthenticityReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P3",
        "witness_refs": ["lean-theorem:complete_envelope_is_ready", "tests/fixtures/proof_models/content_authenticity_envelope.json"],
        "classification_basis": ["a quantified mutation, finite induction, scope invalidation, transformation rule, non-identifiability result, or rejecting consumer refinement is independently reconstructed"],
        "rationale": rationale,
    }

for theorem_name in (
    "signed_provenance_does_not_establish_semantic_truth",
    "watermark_absence_does_not_establish_human_origin",
    "detector_output_does_not_establish_authorship",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "campaign_eligibility_requires_admissible_envelope", "readiness_requires_identity",
    "readiness_requires_evidence", "readiness_requires_transformations",
    "readiness_requires_current_trust", "readiness_requires_conflict_routes",
    "readiness_requires_accessible_disclosure", "readiness_requires_nonclaim_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ContentAuthenticityReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored authenticity-envelope state"],
        "rationale": "The theorem constrains only the encoded authenticity review; it establishes no provenance correctness, content truth, origin, authorship, comprehension, compliance, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed authored dossier witnesses the finite replication-containment admissibility predicate.",
    "complete_dossier_reaches_only_replication_containment_campaign": "The closed dossier reaches only Project Theseus replication-containment campaign eligibility, not real infrastructure, replication, containment, or release authority.",
    "identical_component_signals_can_hide_opposite_replication_state": "Two cases witness opposite end-to-end synthetic replication states under identical component signals.",
    "identical_local_containment_signals_can_hide_opposite_global_state": "Two cases witness opposite global-containment states under identical local shutdown and known-census signals.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ReplicationContainmentReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed replication dossier or collision pair witnesses one bounded modeled result"],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "distinct_child_cannot_use_parent_replication_lease": "The principal-identity conjunct excludes every distinct child from using its parent's lease.",
    "real_provider_path_is_outside_synthetic_test_authority": "The typed infrastructure boundary excludes real providers from synthetic-test authority.",
    "quarantine_all_covers_every_finite_descendant": "Structural induction proves every member of an arbitrary finite descendant list is quarantined by the modeled map.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 52 replication-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 52 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 52 mutations into the lifecycle repair state.",
    "expired_lease_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired replication lease.",
    "descendant_overrun_persists_under_growth_and_no_larger_ceiling": "Natural-number order preserves descendant-ceiling rejection under population growth and no larger ceiling.",
    "parent_change_invalidates_replication_receipt": "The parent-identity conjunct rejects every receipt presented for a different parent.",
    "artifact_change_invalidates_replication_receipt": "The artifact-identity conjunct rejects every receipt presented for a different artifact.",
    "environment_change_invalidates_replication_receipt": "The environment-identity conjunct rejects every receipt presented for a different environment.",
    "protocol_change_invalidates_replication_receipt": "The protocol-version conjunct rejects every receipt presented under a different protocol.",
    "component_signals_cannot_recover_end_to_end_replication": "A same-component/opposite-composition collision proves no component-signal classifier is exact for every modeled replication case.",
    "local_containment_signals_cannot_recover_global_containment": "A same-local/opposite-global collision proves no local-containment classifier is exact for every modeled containment case.",
    "unresolved_descendants_force_operations_state_inventory": "The consumer refinement deliberately leaves descendant inventory incomplete, making governed operations request state inventory.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ReplicationContainmentReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P3",
        "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/replication_containment_dossier.json"],
        "classification_basis": ["a quantified mutation, finite induction, authority or scope invalidation, non-identifiability result, or rejecting consumer refinement is independently reconstructed"],
        "rationale": rationale,
    }

for theorem_name in (
    "component_success_does_not_establish_end_to_end_replication",
    "synthetic_completion_does_not_establish_real_infrastructure_capability",
    "shutdown_acknowledgment_does_not_establish_global_containment",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "campaign_eligibility_requires_admissible_dossier", "readiness_requires_identity",
    "readiness_requires_authority", "readiness_requires_evaluation",
    "readiness_requires_lineage", "readiness_requires_containment",
    "readiness_requires_closure", "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ReplicationContainmentReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored replication-containment state"],
        "rationale": "The theorem constrains only the encoded replication-containment review; it establishes no real-world replication, census completeness, containment efficacy, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed authored dossier witnesses the finite institutional admissibility predicate.",
    "complete_dossier_reaches_only_institutional_tabletop": "The closed dossier reaches only Project Theseus institutional-tabletop eligibility, not authority, legitimacy, enforcement, support, or release.",
    "identical_participation_signals_can_hide_opposite_representation": "Two cases witness opposite excluded-public standing under identical consultation, notice, and comment-count signals.",
    "identical_commitment_signals_can_hide_opposite_enforcement": "Two cases witness opposite remedy reach under identical agreement, published-duty, and named-verifier signals.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/InstitutionalLegitimacyReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed institutional dossier or collision pair witnesses one bounded modeled result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "local_mandate_cannot_authorize_distinct_jurisdiction": "The jurisdiction-identity conjunct excludes use of a local mandate in every distinct jurisdiction.",
    "include_all_covers_every_finite_affected_public": "Structural induction proves every member of an arbitrary finite affected-public list is included by the modeled map.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 45 institutional-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 45 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 45 mutations into the lifecycle repair state.",
    "expired_mandate_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired institutional mandate.",
    "omitted_public_shortfall_persists_when_population_grows": "Natural-number order preserves an inclusion shortfall when the required population grows.",
    "jurisdiction_change_invalidates_institutional_receipt": "The jurisdiction conjunct rejects every receipt presented in a different jurisdiction.",
    "instrument_change_invalidates_institutional_receipt": "The instrument conjunct rejects every receipt presented for a different institutional instrument.",
    "population_change_invalidates_institutional_receipt": "The population-digest conjunct rejects every receipt presented for a different affected population.",
    "protocol_change_invalidates_institutional_receipt": "The protocol conjunct rejects every receipt presented under a different protocol.",
    "participation_signals_cannot_recover_representation": "A same-procedure/opposite-standing collision proves no participation-signal classifier is exact for every modeled representation case.",
    "commitment_signals_cannot_recover_effective_enforcement": "A same-commitment/opposite-remedy collision proves no commitment-signal classifier is exact for every modeled enforcement case.",
    "excluded_public_forces_governance_rights_review": "The consumer refinement maps an incomplete affected-public census to a protected-right removal and Governance Rights review.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/InstitutionalLegitimacyReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/institutional_legitimacy_dossier.json"],
        "classification_basis": ["a quantified mutation, finite induction, jurisdiction or scope invalidation, non-identifiability result, or rejecting consumer refinement is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "agreement_does_not_establish_effective_implementation", "legal_compliance_does_not_establish_public_legitimacy",
    "consultation_does_not_establish_representative_mandate", "technical_conformance_does_not_establish_public_authority",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant", "tabletop_eligibility_requires_admissible_dossier",
    "readiness_requires_identity", "readiness_requires_mandate", "readiness_requires_publics", "readiness_requires_coordination",
    "readiness_requires_performance", "readiness_requires_remedy", "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/InstitutionalLegitimacyReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored institutional state"],
        "rationale": "The theorem constrains only the encoded institutional review; it establishes no lawful authority, representation, enforcement, legitimacy, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready": "The closed authored dossier witnesses the finite societal-resilience admissibility predicate.",
    "complete_dossier_reaches_only_theseus_resilience_exercise": "The closed dossier reaches only Project Theseus synthetic exercise eligibility, not population resilience, recovery, remedy, support, or release.",
    "identical_provider_signals_can_hide_opposite_population_resilience": "Two cases witness opposite affected-population recovery under identical classifier, takedown, and provider-restoration signals.",
    "identical_response_speed_can_hide_opposite_equitable_remedy": "Two cases witness opposite false-intervention remedy under identical acknowledgement, containment, and tabletop signals.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/SocietalResilienceReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P2", "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": ["a closed resilience dossier or collision pair witnesses one bounded modeled result"], "rationale": rationale,
    }

for theorem_name, rationale in {
    "single_organization_mandate_cannot_authorize_distinct_organization": "The organization-identity conjunct excludes mandate use by every distinct organization.",
    "close_all_covers_every_finite_incident_path": "Structural induction proves every member of an arbitrary finite incident-path list is closed by the modeled map.",
    "every_admission_axis_mutation_blocks_readiness": "Universal case analysis shows all 45 resilience-dossier mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair": "Universal case analysis binds all 45 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair": "Universal case analysis routes all 45 mutations into the lifecycle repair state.",
    "expired_response_mandate_remains_expired_when_time_advances": "Natural-number order proves advancing time cannot restore an expired response mandate.",
    "uncovered_population_shortfall_persists_when_population_grows": "Natural-number order preserves a coverage shortfall when the affected population grows.",
    "unresolved_path_shortfall_persists_when_more_paths_are_discovered": "Natural-number order preserves unresolved-path rejection when additional paths are discovered.",
    "incident_change_invalidates_resilience_receipt": "The incident-identity conjunct rejects every receipt presented for a different incident.",
    "population_change_invalidates_resilience_receipt": "The population-digest conjunct rejects every receipt presented for a different affected population.",
    "jurisdiction_change_invalidates_resilience_receipt": "The jurisdiction conjunct rejects every receipt presented in a different jurisdiction.",
    "protocol_change_invalidates_resilience_receipt": "The protocol conjunct rejects every receipt presented under a different protocol.",
    "provider_signals_cannot_recover_population_resilience": "A same-provider/opposite-recovery collision proves no provider-signal classifier is exact for every modeled population case.",
    "response_speed_cannot_recover_lawful_equitable_remedy": "A same-speed/opposite-remedy collision proves no response-signal classifier is exact for every modeled remedy case.",
    "missing_participant_forces_institutional_review": "The consumer refinement maps an incomplete participant census to an Institutional Legitimacy rejection.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/SocietalResilienceReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P3", "witness_refs": ["lean-theorem:complete_dossier_is_ready", "tests/fixtures/proof_models/societal_resilience_dossier.json"],
        "classification_basis": ["a quantified mutation, finite induction, authority or scope invalidation, non-identifiability result, or rejecting consumer refinement is independently reconstructed"], "rationale": rationale,
    }

for theorem_name in (
    "provider_takedown_does_not_establish_population_resilience", "tabletop_completion_does_not_establish_live_recovery",
    "rapid_response_does_not_establish_lawful_equitable_remedy", "local_safeguard_does_not_establish_cross_organization_defense",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant", "exercise_eligibility_requires_admissible_dossier",
    "readiness_requires_identity_and_coordination", "readiness_requires_defense", "readiness_requires_recovery",
    "readiness_requires_remedy", "readiness_requires_adaptation", "readiness_requires_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[f"lean/AsiStackProofs/SocietalResilienceReview.lean::{theorem_name}"] = {
        "disposition": "retain", "semantic_level": "P1",
        "classification_basis": ["a typed evidence decision, universal finite lifecycle invariant, or grouped necessity result constrains authored resilience state"],
        "rationale": "The theorem constrains only the encoded societal-resilience review; it establishes no population resilience, lawful coordination, recovery, remedy efficacy, support, or deployment authority.",
    }

for theorem_name, rationale in {
    "complete_control_lease_is_ready":
        "The closed complete lease witnesses the derived finite admissibility predicate.",
    "complete_control_lease_routes_only_to_theseus_trial":
        "The closed complete lease reaches only trial eligibility, not physical actuation authority.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/EmbodiedPhysicalSafety.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": [
            "a closed control lease witnesses one derived finite admission result"
        ],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "every_control_axis_omission_blocks_readiness":
        "Universal finite case analysis shows all 13 admission-axis omissions reject readiness.",
    "every_control_axis_omission_reaches_exact_repair_route":
        "Universal finite case analysis binds all 13 omissions to their exact repair routes.",
    "every_control_axis_omission_blocks_trial_eligibility":
        "Universal finite case analysis prevents every omission from reaching trial eligibility.",
    "reduced_latency_preserves_timing_validity":
        "Natural-number order proves an already-valid timing budget remains valid when latency decreases.",
    "lower_state_violation_persists_under_downward_widening":
        "Natural-number order proves lowering an already-unsafe estimate cannot restore the state envelope.",
    "fallback_distance_violation_persists_when_bound_grows":
        "Natural-number order proves increasing an infeasible stopping-distance bound cannot restore fallback reachability.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/EmbodiedPhysicalSafety.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P3",
        "witness_refs": ["lean-theorem:complete_control_lease_is_ready"],
        "classification_basis": [
            "a quantified mutation family or arithmetic monotonicity law constrains the finite model"
        ],
        "rationale": rationale,
    }

for theorem_name in (
    "admissible_control_lease_is_ready",
    "readiness_requires_command_request",
    "readiness_requires_plant_identity",
    "readiness_requires_current_lease_version",
    "readiness_requires_unexpired_lease",
    "readiness_requires_fresh_observation",
    "readiness_requires_state_envelope",
    "readiness_requires_timing_budget",
    "readiness_requires_actuator_envelope",
    "readiness_requires_reachable_fallback",
    "readiness_requires_independent_stop",
    "readiness_requires_effect_observation",
    "readiness_requires_residual_custody",
    "readiness_requires_non_claim_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/EmbodiedPhysicalSafety.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "a universal finite predicate bridge or projection exposes one necessary admission condition"
        ],
        "rationale": (
            "The theorem decomposes the authored finite lease predicate; it establishes no field truth "
            "or physical outcome."
        ),
    }

for theorem_name, rationale in {
    "complete_work_contract_reaches_dispatch_ready":
        "The closed complete contract witnesses reachability of dispatch readiness without executing work.",
    "missing_work_objective_reaches_repair":
        "The closed contract with no objective witnesses the exact objective-repair state.",
    "missing_work_authority_reaches_repair":
        "The closed contract with no authority basis witnesses the exact authority-repair state.",
    "widened_work_authority_reaches_refusal":
        "The closed authority-widening contract witnesses exact dispatch refusal.",
    "missing_work_tool_boundary_reaches_repair":
        "The closed contract with an incomplete tool boundary witnesses exact repair.",
    "missing_work_verification_reaches_repair":
        "The closed contract with no verification plan witnesses exact repair.",
    "missing_work_budget_reaches_repair":
        "The closed contract with no budget record witnesses exact repair.",
    "over_policy_work_budget_reaches_approval":
        "The closed over-policy contract witnesses routing to budget approval.",
    "missing_work_rollback_reaches_repair":
        "The closed contract with no rollback plan witnesses exact repair.",
    "missing_work_non_claim_boundary_reaches_repair":
        "The closed contract with no non-claim boundary witnesses exact repair.",
    "complete_release_packet_reaches_external_review_ready":
        "The closed complete release packet witnesses external-review readiness without publication.",
    "missing_release_artifact_binding_reaches_repair":
        "The closed release packet with no artifact binding witnesses exact repair.",
    "missing_release_tests_reaches_repair":
        "The closed release packet with no test record witnesses exact repair.",
    "missing_release_evidence_reaches_repair":
        "The closed release packet with no evidence record witnesses exact repair.",
    "missing_release_changelog_reaches_repair":
        "The closed release packet with no changelog witnesses exact repair.",
    "missing_release_residuals_reaches_repair":
        "The closed release packet with no residual record witnesses exact repair.",
    "missing_release_approval_reaches_approval_request":
        "The closed release packet with no approval witnesses an approval request.",
    "release_support_promotion_reaches_refusal":
        "The closed release packet requesting support effect witnesses exact refusal.",
    "missing_release_non_claim_boundary_reaches_repair":
        "The closed release packet with no non-claim boundary witnesses exact repair.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ArtifactStewardAgents.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": [
            "a closed concrete steward packet witnesses one reachable transition state"
        ],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "steward_dispatch_run_ready_requires_complete_contract": (
        "Induction over arbitrary finite run length preserves the work-contract safety predicate; "
        "the result proves modeled readiness requires completeness, not real execution correctness."
    ),
    "steward_release_run_ready_requires_complete_packet": (
        "Induction over arbitrary finite run length preserves the release-packet safety predicate; "
        "the result proves modeled review readiness requires completeness, not publication safety."
    ),
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ArtifactStewardAgents.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "classification_basis": [
            "induction proves a safety predicate across every finite transition run"
        ],
        "rationale": rationale,
    }

for theorem_name in (
    "dispatch_ready_requires_complete_work_contract",
    "steward_dispatch_step_preserves_contract_safety",
    "release_review_ready_requires_complete_packet",
    "steward_release_step_preserves_packet_safety",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ArtifactStewardAgents.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "universal finite transition preservation constrains readiness within the authored model"
        ],
        "rationale": (
            "The theorem is a local completeness or one-step preservation law. It trusts all input "
            "fields and proves no execution, publication, governance, or support outcome."
        ),
    }

for theorem_name, rationale in {
    "complete_accountability_record_reaches_assignment":
        "A closed complete record witnesses the five-stage route to modeled assignment readiness.",
    "missing_information_blocks_accountability_assignment":
        "A closed record missing information witnesses the exact capacity-repair state.",
    "missing_competence_blocks_accountability_assignment":
        "A closed record with stale competence witnesses the exact capacity-repair state.",
    "missing_time_blocks_accountability_assignment":
        "A closed record with no review time witnesses the exact capacity-repair state.",
    "excessive_workload_blocks_accountability_assignment":
        "A closed overloaded record witnesses the exact workload-repair state.",
    "missing_decision_authority_blocks_accountability_assignment":
        "A closed record missing decision authority witnesses the exact authority-repair state.",
    "missing_intervention_authority_blocks_accountability_assignment":
        "A closed record missing intervention authority witnesses the exact authority-repair state.",
    "missing_practical_control_blocks_accountability_assignment":
        "A closed record missing practical control witnesses the exact control-repair state.",
    "missing_revocation_blocks_accountability_assignment":
        "A closed record missing revocation witnesses the exact revocation-repair state.",
    "missing_independent_review_blocks_accountability_assignment":
        "A closed record missing independent review witnesses the exact independence-repair state.",
    "collapsed_separation_of_duties_blocks_accountability_assignment":
        "A closed record with collapsed duties witnesses the exact separation-repair state.",
    "undisposed_conflict_blocks_accountability_assignment":
        "A closed record with an undisposed conflict witnesses the exact conflict-repair state.",
    "missing_stop_path_blocks_accountability_assignment":
        "A closed record missing a stop path witnesses the exact remedy-stage repair state.",
    "missing_appeal_blocks_accountability_assignment":
        "A closed record missing appeal witnesses the exact remedy-stage repair state.",
    "missing_remedy_blocks_accountability_assignment":
        "A closed record missing remedy witnesses the exact remedy-stage repair state.",
    "missing_evidence_access_blocks_accountability_assignment":
        "A closed record missing evidence access witnesses the exact remedy-stage repair state.",
    "orphaned_residuals_block_accountability_assignment":
        "A closed record with orphaned residuals witnesses the exact custody-repair state.",
    "missing_non_claim_boundary_blocks_accountability_assignment":
        "A closed record missing its non-claim boundary witnesses the exact repair state.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/HumanAIOrganizations.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": [
            "a closed accountability record witnesses one exact reachable transition state"
        ],
        "rationale": rationale,
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/HumanAIOrganizations.lean::accountability_review_run_preserves_stage_invariant"
] = {
    "disposition": "retain",
    "semantic_level": "P2",
    "classification_basis": [
        "induction preserves the staged accountability invariant across every finite run"
    ],
    "witness_refs": [
        "lean-theorem:complete_accountability_record_reaches_assignment"
    ],
    "rationale": (
        "Induction over arbitrary finite run length preserves identity, capacity, authority, "
        "independence, and remedy requirements inside the authored model."
    ),
}

for theorem_name in (
    "accountability_review_step_preserves_stage_invariant",
    "assignable_accountability_requires_complete_authority_record",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/HumanAIOrganizations.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "a universal local preservation or completeness law constrains the finite authored model"
        ],
        "rationale": (
            "The theorem is a local staged-record law. It trusts all Boolean inputs and proves "
            "neither real human control nor lawful or effective accountability."
        ),
    }

for theorem_name, rationale in {
    "responsibility_delegation_accepted_step_is_valid": (
        "An accepted responsibility step exposes the full finite authored event predicate."
    ),
    "responsibility_delegation_accepted_step_applies_event": (
        "An accepted responsibility step is definitionally the modeled state transformer."
    ),
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/HumanAIOrganizations.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "a universal local route or application law constrains the finite authored bridge"
        ],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "responsibility_delegation_step_assigns_exact_child_owner": (
        "The independently exercised transition assigns the authority event's exact child delegate as owner."
    ),
    "responsibility_delegation_step_retains_prior_owner": (
        "The independently exercised transition prepends the prior owner to residual custody."
    ),
    "responsibility_delegation_step_adds_exact_receipt": (
        "The independently exercised transition adds exactly one responsibility receipt."
    ),
    "responsibility_delegation_successful_run_has_valid_trace": (
        "Every successful finite run exposes the exact recursively valid authored event trace."
    ),
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/HumanAIOrganizations.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P3",
        "witness_refs": [
            "lean-theorem:two_hop_responsibility_delegation_preserves_accountability",
            "scripts/validate_human_ai_organization_accountability.py",
        ],
        "classification_basis": [
            "the exact transition or trace consequence is independently reconstructed over the two-hop bridge"
        ],
        "rationale": rationale,
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/HumanAIOrganizations.lean::responsibility_delegation_initial_state_is_invariant"
] = {
    "disposition": "retain",
    "semantic_level": "P2",
    "witness_refs": [
        "lean-theorem:responsibility_delegation_initial_state_is_invariant"
    ],
    "classification_basis": [
        "one closed initial organizational delegation state witnesses the full finite invariant"
    ],
    "rationale": (
        "The closed initial record is a nonvacuity witness for owner, reviewer, evidence, "
        "receipt, residual, authority, and non-authority alignment."
    ),
}

for theorem_name, rationale in {
    "responsibility_delegation_step_refines_authority_step": (
        "Every accepted responsibility handoff projects to an accepted step in the separate authority model."
    ),
    "responsibility_delegation_step_preserves_non_authority": (
        "An accepted organizational handoff cannot create support or external-effect authority in either model."
    ),
    "responsibility_delegation_step_preserves_invariant": (
        "One accepted cross-model handoff preserves authority, owner, review, evidence, residual, receipt, and non-authority alignment."
    ),
    "responsibility_delegation_run_preserves_invariant": (
        "Induction preserves the cross-model organizational responsibility invariant across arbitrary successful finite runs."
    ),
    "responsibility_delegation_run_refines_authority_run": (
        "Every successful responsibility run projects to the corresponding successful authority-delegation run."
    ),
    "responsibility_delegation_run_has_no_owner_gap": (
        "Every successful invariant-preserving run ends with a positive owner equal to the current authority delegate."
    ),
    "responsibility_delegation_run_accounts_exact_receipts": (
        "Every successful run aligns responsibility receipt growth exactly with event count."
    ),
    "responsibility_delegation_run_accounts_residual_owners": (
        "Every successful run retains one prior owner per accepted handoff."
    ),
    "responsibility_delegation_run_composes_across_event_batches": (
        "Responsibility execution is invariant under splitting the same finite event list into prefix and suffix batches."
    ),
    "two_hop_responsibility_delegation_preserves_accountability": (
        "A closed two-hop witness attenuates authority while preserving exact owner, residual, receipt, review, evidence, and non-authority custody."
    ),
    "responsibility_delegation_closed_countermodels": (
        "Sixteen closed substitutions or omissions reject owner mismatch, role collapse, missing controls, authority widening, stale epoch, support, and effect requests."
    ),
    "thin_responsibility_summary_hides_accountability_gap": (
        "A safe record and a record missing owner, reviewer, and evidence custody have the same aggregate delegation summary and opposite decisions."
    ),
    "thin_responsibility_summary_cannot_recover_accountability": (
        "No Boolean classifier over the colliding aggregate summary can recover both finite accountability decisions."
    ),
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/HumanAIOrganizations.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P4",
        "witness_refs": [
            "lean-theorem:two_hop_responsibility_delegation_preserves_accountability",
            "lean-theorem:thin_responsibility_summary_hides_accountability_gap",
            "scripts/validate_human_ai_organization_accountability.py",
        ],
        "classification_basis": [
            "a cross-model refinement, noninterference, composition, countermodel, or information-loss result is independently reconstructed"
        ],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "complete_population_has_pairwise_validity":
        "The closed complete population witnesses all six directed pairwise authorizations.",
    "complete_population_is_campaign_ready":
        "The closed complete population witnesses the finite ten-dimension review predicate.",
    "complete_population_routes_to_theseus_campaign":
        "The closed complete population reaches the only accepted route, which starts a Theseus campaign rather than claiming an outcome.",
    "pairwise_only_population_has_pairwise_validity":
        "The closed pairwise-only population witnesses all six local authorization edges.",
    "pairwise_only_population_is_not_campaign_ready":
        "The closed pairwise-only population witnesses refusal despite complete local authorization.",
    "pairwise_only_population_routes_to_dependency_mapping":
        "The closed pairwise-only population reaches the exact common-dependency repair route.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/MultiAgentDynamics.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": [
            "a closed three-party population witnesses one derived finite review property"
        ],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "complete_and_pairwise_only_have_identical_pairwise_evidence": (
        "Function equality proves the accepted and rejected records expose the same six-edge classifier input."
    ),
    "pairwise_validity_does_not_entail_population_campaign_readiness": (
        "An existential countermodel separates complete pairwise authorization from the larger readiness predicate."
    ),
    "no_pairwise_only_classifier_exactly_recovers_campaign_readiness": (
        "A finite indistinguishability argument proves no Boolean classifier over only the pairwise matrix is exact for every modeled record."
    ),
    "every_systemic_axis_omission_preserves_pairwise_validity": (
        "Universal case analysis shows all nine systemic mutations retain the six-edge local evidence."
    ),
    "every_systemic_axis_omission_blocks_campaign_readiness": (
        "Universal case analysis shows all nine systemic mutations reject readiness."
    ),
    "every_systemic_axis_omission_reaches_exact_repair_route": (
        "Universal case analysis binds every systemic mutation to its exact repair consumer."
    ),
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/MultiAgentDynamics.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P3",
        "witness_refs": [
            "lean-theorem:complete_population_is_campaign_ready",
            "lean-theorem:pairwise_only_population_is_not_campaign_ready",
        ],
        "classification_basis": [
            "a finite countermodel or mutation family proves pairwise-only underdetermination"
        ],
        "rationale": rationale,
    }

for theorem_name in (
    "campaign_readiness_requires_population_registry",
    "campaign_readiness_requires_pairwise_validity",
    "campaign_readiness_requires_effective_diversity",
    "campaign_readiness_requires_diversified_resource_control",
    "campaign_readiness_requires_human_stop",
    "campaign_readiness_requires_affected_party_coverage",
    "campaign_readiness_requires_human_exit",
    "campaign_readiness_requires_recovery",
    "campaign_readiness_requires_residual_custody",
    "campaign_readiness_requires_non_claim_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/MultiAgentDynamics.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "a universal finite predicate decomposition exposes one necessary review condition"
        ],
        "rationale": (
            "The theorem projects one necessary authored condition from campaign readiness; "
            "it proves no field truth or population outcome."
        ),
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready":
        "The closed complete dossier witnesses the derived finite admissibility predicate.",
    "complete_dossier_reaches_only_harmless_analogue_campaign":
        "The closed dossier reaches only harmless-analogue campaign eligibility, not a result or release decision.",
    "equal_aggregate_score_can_hide_distinct_outcome_vectors":
        "Two closed vectors witness distinct component states under one aggregate total.",
    "equal_aggregate_score_can_require_opposite_component_reviews":
        "Two closed equal-total vectors witness opposite component-sensitive modeled decisions.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/DangerousCapabilityReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": [
            "a closed generic dossier or outcome-vector pair witnesses one bounded modeled result"
        ],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "every_admission_axis_mutation_blocks_readiness":
        "Universal finite case analysis shows all 29 admission-axis mutations reject readiness.",
    "every_admission_axis_mutation_reaches_exact_repair":
        "Universal finite case analysis binds all 29 mutations to exact repair or refusal states.",
    "every_admission_axis_mutation_blocks_campaign_eligibility":
        "Universal finite case analysis prevents every mutation from reaching campaign eligibility.",
    "expired_dossier_remains_expired_when_time_advances":
        "Natural-number order proves advancing time cannot restore an already expired dossier.",
    "attempt_shortfall_persists_when_retention_decreases":
        "Natural-number order proves retaining fewer attempts cannot repair an existing denominator shortfall.",
    "aggregate_score_cannot_recover_component_sensitive_review":
        "A same-total/opposite-decision collision proves no scalar-only classifier is exact over every modeled vector.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/DangerousCapabilityReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P3",
        "witness_refs": [
            "lean-theorem:complete_dossier_is_ready",
            "tests/fixtures/proof_models/dangerous_capability_dossier.json",
        ],
        "classification_basis": [
            "a quantified mutation, arithmetic monotonicity, or non-identifiability result is independently reconstructed"
        ],
        "rationale": rationale,
    }

for theorem_name in (
    "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant",
    "campaign_eligibility_requires_admissible_dossier",
    "admissible_dossier_is_ready",
    "readiness_requires_identity_review",
    "readiness_requires_threat_review",
    "readiness_requires_baselines",
    "readiness_requires_instrument_competence",
    "readiness_requires_custody_and_currentness",
    "readiness_requires_non_authorizing_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/DangerousCapabilityReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "a universal finite lifecycle invariant, predicate bridge, or grouped necessity result constrains authored dossier state"
        ],
        "rationale": (
            "The theorem constrains only the seven-stage finite review and authored fields; "
            "it establishes no field truth, dangerous capability, safety, support, or authority."
        ),
    }

for theorem_name, rationale in {
    "complete_dossier_is_ready":
        "The closed non-operational dossier witnesses the derived finite admissibility predicate.",
    "complete_dossier_reaches_only_public_safe_simulation":
        "The closed dossier reaches only public-safe Theseus simulation eligibility, not authority or a result.",
    "same_human_interface_can_hide_opposite_judgment_results":
        "Two closed dossiers witness opposite meaningful-judgment decisions under identical interface presence.",
    "identical_component_evidence_can_require_opposite_interaction_reviews":
        "Two closed interaction records witness opposite reviews under identical local component evidence.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/MilitaryInteractionReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P2",
        "witness_refs": [f"lean-theorem:{theorem_name}"],
        "classification_basis": [
            "a closed public-safe dossier or collision pair witnesses one bounded modeled result"
        ],
        "rationale": rationale,
    }

for theorem_name, rationale in {
    "every_admission_axis_mutation_blocks_readiness":
        "Universal finite case analysis shows all 45 admission-axis mutations reject readiness.",
    "every_admission_axis_mutation_has_exact_repair_disposition":
        "Universal finite case analysis binds all 45 mutations to exact repair or refusal dispositions.",
    "every_admission_axis_mutation_reaches_repair_state":
        "Universal finite case analysis routes all 45 mutations into the lifecycle repair state.",
    "every_admission_axis_mutation_blocks_simulation_eligibility":
        "Universal finite case analysis prevents every mutation from reaching public-safe simulation eligibility.",
    "expired_dossier_remains_expired_when_time_advances":
        "Natural-number order proves advancing time cannot restore an already expired dossier.",
    "decision_time_shortfall_persists_when_available_time_decreases":
        "Natural-number order proves less available decision time cannot repair an existing shortfall.",
    "off_ramp_shortfall_persists_when_available_routes_decrease":
        "Natural-number order proves fewer available off-ramps cannot repair an existing shortfall.",
    "interface_presence_cannot_recover_meaningful_judgment":
        "A same-interface/opposite-decision collision proves no interface-only classifier is exact over every modeled dossier.",
    "component_evidence_cannot_recover_interaction_review":
        "A same-component/opposite-decision collision proves no local-component-only classifier is exact over every modeled interaction.",
}.items():
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/MilitaryInteractionReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P3",
        "witness_refs": [
            "lean-theorem:complete_dossier_is_ready",
            "tests/fixtures/proof_models/military_interaction_dossier.json",
        ],
        "classification_basis": [
            "a quantified mutation, arithmetic monotonicity, or non-identifiability result is independently reconstructed"
        ],
        "rationale": rationale,
    }

for theorem_name in (
    "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant",
    "simulation_eligibility_requires_admissible_dossier",
    "admissible_dossier_is_ready",
    "readiness_requires_scope",
    "readiness_requires_bounded_authority",
    "readiness_requires_meaningful_human_judgment",
    "readiness_requires_observation_trust_record",
    "readiness_requires_safe_posture",
    "readiness_requires_interaction_case",
    "readiness_requires_custody_and_non_authorizing_boundary",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/MilitaryInteractionReview.lean::{theorem_name}"
    ] = {
        "disposition": "retain",
        "semantic_level": "P1",
        "classification_basis": [
            "a universal finite lifecycle invariant, predicate bridge, or grouped necessity result constrains authored dossier state"
        ],
        "rationale": (
            "The theorem constrains only the eight-step non-operational review and authored fields; "
            "it establishes no lawful use, meaningful control in practice, strategic stability, safety, support, or authority."
        ),
    }

_authority_delegation_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean-theorem:two_hop_delegation_reaches_attenuated_grandchild",
        "experiments/authority_effect_refinement/results/2026-07-15-local.json",
    ],
    "classification_basis": [
        "the delegation-chain semantics are independently reconstructed by the authority-effect validator"
    ],
}

for theorem_name in (
    "delegation_accepted_step_is_valid",
    "delegation_accepted_step_applies_event",
    "delegation_accepted_step_adds_one_receipt",
    "delegation_accepted_step_adds_one_depth",
    "delegation_initial_state_is_invariant",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Authority.lean::{theorem_name}"
    ] = {
        **_authority_delegation_refinement_base,
        "semantic_level": "P1",
        "rationale": (
            "The theorem exposes an accepted-step premise, exact application, accounting increment, or initial invariant; "
            "it is load-bearing for the arbitrary-run results but does not establish them alone."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/Authority.lean::two_hop_delegation_reaches_attenuated_grandchild"
] = {
    **_authority_delegation_refinement_base,
    "semantic_level": "P2",
    "rationale": (
        "The closed two-event witness reaches a second-generation delegate with exact identity custody, lower authority, "
        "narrower expiry, two receipts, and no support or external-effect authority."
    ),
}

for theorem_name in (
    "delegation_rejected_event_is_noninterfering",
    "delegation_step_preserves_custody",
    "delegation_custody_is_transitive",
    "delegation_step_preserves_non_authority",
    "delegation_step_preserves_invariant",
    "authority_widening_delegation_is_rejected",
    "confused_deputy_principal_substitution_is_rejected",
    "delegation_operation_substitution_is_rejected",
    "delegation_target_substitution_is_rejected",
    "delegation_scope_substitution_is_rejected",
    "stale_epoch_delegation_is_rejected",
    "expiry_widening_delegation_is_rejected",
    "revoked_child_grant_is_rejected",
    "support_promotion_delegation_is_rejected",
    "external_effect_delegation_is_rejected",
    "complete_delegation_transport_round_trips",
    "complete_delegation_transport_is_injective",
    "complete_delegation_transport_preserves_step",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Authority.lean::{theorem_name}"
    ] = {
        **_authority_delegation_refinement_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem proves one-step custody, a closed adversarial refusal, or lossless transport for the finite "
            "delegation model reconstructed by the independent consumer."
        ),
    }

for theorem_name in (
    "delegation_run_preserves_custody",
    "delegation_run_preserves_non_authority",
    "delegation_run_composes_across_event_batches",
    "delegation_run_preserves_invariant",
    "delegation_successful_run_has_valid_trace",
    "thin_delegation_summary_has_authority_collision",
    "no_thin_delegation_classifier_recovers_authority",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Authority.lean::{theorem_name}"
    ] = {
        **_authority_delegation_refinement_base,
        "semantic_level": "P4",
        "rationale": (
            "The theorem constrains arbitrary finite delegation runs or proves that a lossy summary cannot recover "
            "the exact authority decision across a confused-deputy collision."
        ),
    }

_runtime_adapter_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "experiments/runtime_adapter_permissions/fixtures/valid_low_impact_local_write.json",
        "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json",
    ],
    "classification_basis": [
        "the reachable runtime-effect model is bound to the existing independent permission consumer and bounded local effect probe"
    ],
}

for theorem_name in (
    "accepted_runtime_effect_step_is_admissible",
    "accepted_runtime_effect_step_applies_event",
    "initial_runtime_effect_state_satisfies_invariant",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/RuntimeAdapters.lean::{theorem_name}"
    ] = {
        **_runtime_adapter_refinement_base,
        "semantic_level": "P1",
        "rationale": (
            "The theorem exposes a local transition premise, application identity, or initial witness; "
            "it is load-bearing for the stronger induction but does not alone establish run safety."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/RuntimeAdapters.lean::projected_runtime_lease_preserves_exact_identity"
] = {
    **_runtime_adapter_refinement_base,
    "semantic_level": "P2",
    "rationale": (
        "The theorem proves nonvacuous exact identity preservation across the adapter-to-authority lease projection."
    ),
}

for theorem_name in (
    "apply_runtime_effect_event_preserves_invariant",
    "accepted_runtime_effect_step_preserves_invariant",
    "runtime_effect_run_preserves_invariant",
    "complete_runtime_effect_trace_reaches_exact_rollback",
    "missing_parent_permission_is_rejected_before_prepare",
    "caller_identity_substitution_is_rejected_before_prepare",
    "authority_widening_is_rejected_before_prepare",
    "expired_lease_is_rejected_before_dispatch",
    "scoped_approval_identity_substitution_is_rejected",
    "secret_materialization_is_rejected_before_dispatch",
    "effect_without_dispatch_is_rejected",
    "rollback_required_without_handle_is_rejected_before_effect",
    "effect_prestate_mismatch_is_rejected",
    "revoked_lease_cannot_be_prepared_again",
    "revoked_state_cannot_dispatch_without_a_fresh_lease",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/RuntimeAdapters.lean::{theorem_name}"
    ] = {
        **_runtime_adapter_refinement_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem proves a reachable lifecycle invariant, exact rollback witness, or closed pre-effect countermodel "
            "inside the finite adapter semantics."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/RuntimeAdapters.lean::runtime_effect_denial_is_state_noninterfering"
] = {
    **_runtime_adapter_refinement_base,
    "semantic_level": "P4",
    "rationale": (
        "The theorem constrains rejected adapter transitions to produce no successor state in the modeled effect boundary."
    ),
}

for theorem_name in (
    "project_runtime_apply_commutes",
    "runtime_admissibility_refines_authority_admissibility",
    "runtime_step_refines_authority_step",
    "runtime_run_refines_authority_run",
    "successful_trace_refines_authority_trace",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/RuntimeAdapters.lean::{theorem_name}"
    ] = {
        **_runtime_adapter_refinement_base,
        "semantic_level": "P5",
        "rationale": (
            "The theorem proves an executable-model refinement or simulation from runtime-adapter transitions into the "
            "independently owned authority-effect state machine."
        ),
    }

_planning_lifecycle_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "experiments/planning_scheduler_state/results/2026-07-02-local.json",
        "experiments/planning_runtime_replan_delta/results/2026-07-02-local.json",
    ],
    "classification_basis": [
        "the reachable planning lifecycle is bound to independent scheduler-state and runtime-replan consumers"
    ],
}

for theorem_name in (
    "accepted_planning_lifecycle_step_is_admissible",
    "accepted_planning_lifecycle_step_applies_event",
    "initial_planning_lifecycle_state_satisfies_invariant",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Planning.lean::{theorem_name}"
    ] = {
        **_planning_lifecycle_refinement_base,
        "semantic_level": "P1",
        "rationale": (
            "The theorem exposes one accepted-step premise, application identity, or initial invariant; "
            "it is load-bearing for induction but does not alone establish a complete lifecycle."
        ),
    }

for theorem_name in (
    "diamond_graph_bound_admission_reaches_admitted_state",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Planning.lean::{theorem_name}"
    ] = {
        **_planning_lifecycle_refinement_base,
        "semantic_level": "P2",
        "rationale": (
            "The theorem is a closed nonvacuity witness that a verified actual-edge graph with exact artifact identity can reach admitted planning state."
        ),
    }

for theorem_name in (
    "self_dependent_graph_bound_admission_is_rejected",
    "mismatched_graph_artifact_admission_is_rejected",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Planning.lean::{theorem_name}"
    ] = {
        **_planning_lifecycle_refinement_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem is a closed rejecting countermodel for invalid graph structure or graph/artifact identity at the planning admission boundary."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/Planning.lean::accepted_graph_bound_plan_admission_preserves_both_models"
] = {
    **_planning_lifecycle_refinement_base,
    "semantic_level": "P4",
    "rationale": (
        "The theorem composes the independent Planning lifecycle and PlanForge actual-edge verifier, preserving both models across one graph-bound admission transition."
    ),
}

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/Planning.lean::accepted_graph_bound_admission_projects_to_legacy_dispatchable"
] = {
    **_planning_lifecycle_refinement_base,
    "semantic_level": "P1",
    "rationale": (
        "The theorem projects accepted graph-bound admission into the retained legacy dispatchability predicate and adds no deeper graph semantics."
    ),
}

_planforge_graph_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "experiments/planning_scheduler_state/results/2026-07-02-local.json",
    ],
    "classification_basis": [
        "the actual-edge finite graph semantics and transport are independently reconstructed by the scheduler-state consumer"
    ],
}

_proof_envelope_lifecycle_base = {
    "disposition": "retain",
    "witness_refs": [
        "docs/proof_artifact_audit.md",
    ],
    "classification_basis": [
        "the formal-artifact authority-lease lifecycle is independently reconstructed by the proof-artifact audit consumer"
    ],
}

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/ProofEnvelope.lean::proof_lease_custody_is_transitive"
] = {
    **_proof_envelope_lifecycle_base,
    "semantic_level": "P1",
    "rationale": (
        "The theorem composes the authored custody relation and is a load-bearing helper for the arbitrary-run result, not a lifecycle witness by itself."
    ),
}

for theorem_name in (
    "initial_issue_trace_reaches_active_lease",
    "complete_proof_lease_trace_reissues_changed_artifact_then_revokes",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofEnvelope.lean::{theorem_name}"
    ] = {
        **_proof_envelope_lifecycle_base,
        "semantic_level": "P2",
        "rationale": (
            "The theorem supplies a closed nonvacuity witness for issuance or artifact-change invalidation, re-review, reissuance, and revocation."
        ),
    }

for theorem_name in (
    "proof_lease_rejected_event_is_noninterfering",
    "proof_lease_step_preserves_custody",
    "proof_lease_step_preserves_non_authority",
    "proof_lease_accepted_step_adds_exactly_one_receipt",
    "run_proof_lease_append",
    "artifact_change_invalidates_active_lease",
    "wrong_consumer_binding_is_rejected",
    "stale_artifact_verification_is_rejected",
    "support_promotion_issue_is_rejected",
    "external_effect_issue_is_rejected",
    "expired_issue_is_rejected",
    "revocation_without_reason_is_rejected",
    "thin_proof_lease_summary_has_issue_collision",
    "complete_proof_lease_transport_round_trips",
    "complete_proof_lease_transport_is_injective",
    "complete_proof_lease_transport_preserves_step",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofEnvelope.lean::{theorem_name}"
    ] = {
        **_proof_envelope_lifecycle_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem proves a quantified finite transition, custody, noninterference, receipt, collision, or complete-transport property bound to the independent audit consumer."
        ),
    }

for theorem_name in (
    "run_proof_lease_preserves_custody",
    "run_proof_lease_preserves_non_authority",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofEnvelope.lean::{theorem_name}"
    ] = {
        **_proof_envelope_lifecycle_base,
        "semantic_level": "P4",
        "rationale": (
            "The theorem lifts exact identity, version monotonicity, and zero support/effect authority across arbitrary event lists."
        ),
    }

for theorem_name in (
    "revoked_proof_lease_is_absorbing",
    "no_thin_proof_lease_classifier_recovers_boundary_state",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofEnvelope.lean::{theorem_name}"
    ] = {
        **_proof_envelope_lifecycle_base,
        "semantic_level": "P5",
        "rationale": (
            "The theorem proves terminal revocation closure or a bounded information-loss impossibility for summary-only lease classification."
        ),
    }

for theorem_name in (
    "diamond_plan_graph_is_verified",
    "diamond_plan_graph_has_reachable_join",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/PlanForge.lean::{theorem_name}"
    ] = {
        **_planforge_graph_refinement_base,
        "semantic_level": "P2",
        "rationale": (
            "The theorem supplies a closed nonvacuity witness for verification or dependency reachability in a concrete diamond graph."
        ),
    }

for theorem_name in (
    "verified_plan_graph_member_edge_is_bounded_and_ordered",
    "verified_plan_graph_dependency_paths_strictly_increase",
    "verified_plan_graph_excludes_dependency_cycles",
    "verified_plan_graph_routes_to_admission",
    "self_dependency_graph_is_rejected",
    "reverse_dependency_graph_is_rejected",
    "out_of_bounds_graph_is_rejected",
    "thin_plan_graph_summary_has_admission_collision",
    "complete_plan_graph_transport_round_trips",
    "complete_plan_graph_transport_is_injective",
    "complete_plan_graph_transport_preserves_admission",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/PlanForge.lean::{theorem_name}"
    ] = {
        **_planforge_graph_refinement_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem proves a quantified listed-edge/path/transport invariant or a closed rejecting/collision countermodel in the executable finite graph semantics."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/PlanForge.lean::no_thin_plan_graph_classifier_recovers_both_decisions"
] = {
    **_planforge_graph_refinement_base,
    "semantic_level": "P5",
    "rationale": (
        "The theorem proves an information-loss impossibility: no classifier over the authored thin graph summary can recover both opposite admission decisions."
    ),
}

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/PlanForge.lean::verified_plan_graph_projects_to_legacy_dispatchable"
] = {
    **_planforge_graph_refinement_base,
    "semantic_level": "P1",
    "rationale": (
        "The theorem projects the verified actual-edge graph into the retained legacy summary predicate and adds no deeper graph property."
    ),
}

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/Planning.lean::complete_planning_lifecycle_trace_reaches_replanned_lowering"
] = {
    **_planning_lifecycle_refinement_base,
    "semantic_level": "P2",
    "rationale": (
        "The closed seven-event trace is a bounded nonvacuity witness for admission, dispatch, feedback, scoped replanning, and renewed lowering."
    ),
}

for theorem_name in (
    "apply_planning_lifecycle_event_preserves_invariant",
    "accepted_planning_lifecycle_step_preserves_invariant",
    "planning_lifecycle_run_preserves_invariant",
    "authority_widening_is_rejected_before_plan_admission",
    "incomplete_decomposition_is_rejected_before_plan_admission",
    "missing_context_is_rejected_before_node_readiness",
    "inadequate_selected_route_is_rejected_before_node_readiness",
    "missing_dispatch_receipt_is_rejected_before_job_lowering",
    "blocked_authority_path_is_rejected_before_job_lowering",
    "feedback_before_job_lowering_is_rejected",
    "stop_condition_erasure_is_rejected_before_replan",
    "unscoped_repair_is_rejected_before_replan",
    "missing_replan_residual_is_rejected",
    "hidden_override_is_rejected_before_planning_transition",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Planning.lean::{theorem_name}"
    ] = {
        **_planning_lifecycle_refinement_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem proves a reachable lifecycle invariant or closed rejecting control inside the finite planning semantics bound to the two fixture consumers."
        ),
    }

for theorem_name in (
    "planning_lifecycle_denial_is_state_noninterfering",
    "admitted_plan_event_refines_vertical_lower_plan",
    "lowered_job_event_refines_vertical_lower_job",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/Planning.lean::{theorem_name}"
    ] = {
        **_planning_lifecycle_refinement_base,
        "semantic_level": "P4",
        "rationale": (
            "The theorem proves bounded state noninterference for rejection or a cross-layer refinement into the independent intent-to-execution transition model."
        ),
    }

_human_factors_lifecycle_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "tests/fixtures/protocol_records/human_oversight_control_packet.valid.json",
        "experiments/human_factors_argument_exit/preregistration.json",
    ],
    "classification_basis": [
        "the reachable review lifecycle is bound to the exact human-oversight contract consumer"
    ],
}

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/HumanFactorsOversight.lean::initial_review_state_satisfies_invariant"
] = {
    **_human_factors_lifecycle_refinement_base,
    "semantic_level": "P1",
    "rationale": (
        "The theorem checks the initial authored state against the lifecycle invariant; it is an induction base, not a complete review witness."
    ),
}

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/HumanFactorsOversight.lean::complete_review_trace_reaches_accountability_closure"
] = {
    **_human_factors_lifecycle_refinement_base,
    "semantic_level": "P2",
    "rationale": (
        "The closed five-event trace is a bounded nonvacuity witness for briefing, decision, intervention, response observation, and accountability closure."
    ),
}

for theorem_name in (
    "accepted_review_step_preserves_invariant",
    "accepted_review_step_preserves_custody",
    "accepted_review_run_preserves_invariant",
    "accepted_review_run_preserves_custody",
    "reachable_accountability_requires_control_decision_intervention_and_response",
    "reachable_review_authority_never_exceeds_ceiling",
    "reachable_review_never_assigns_support_or_release_authority",
    "substituted_reviewer_is_rejected_before_briefing",
    "substituted_action_is_rejected_before_briefing",
    "overloaded_review_is_rejected_before_control_opportunity",
    "late_review_is_rejected_before_control_opportunity",
    "missing_comprehension_acknowledgement_is_rejected_before_decision",
    "missing_independent_challenge_is_rejected_before_decision",
    "missing_override_path_is_rejected_before_decision",
    "authority_widening_is_rejected_before_decision",
    "intervention_before_decision_is_rejected",
    "intervention_without_receipt_is_rejected",
    "response_observation_before_intervention_is_rejected",
    "accountability_without_observed_response_is_rejected",
    "accountability_without_control_opportunity_is_rejected",
    "blocked_review_revokes_active_authority_without_support_effect",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/HumanFactorsOversight.lean::{theorem_name}"
    ] = {
        **_human_factors_lifecycle_refinement_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem proves an arbitrary-run custody invariant or a closed rejecting countermodel inside the finite review lifecycle bound to the independent consumer."
        ),
    }

_typed_job_lifecycle_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "experiments/typed_job_refinement/results/2026-07-15-local.json",
        "experiments/typed_job_delivery/results/2026-07-02-local.json",
        "experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json",
    ],
    "classification_basis": [
        "the reachable typed-job lifecycle is bound to the exact delivery and durable-suite consumer"
    ],
}

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/TypedJobRefinement.lean::initial_state_satisfies_lifecycle_invariant"
] = {
    **_typed_job_lifecycle_refinement_base,
    "semantic_level": "P1",
    "rationale": "The theorem checks the authored induction base; it is not a run-level result.",
}

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/TypedJobRefinement.lean::canonical_run_reaches_exact_closed_state"
] = {
    **_typed_job_lifecycle_refinement_base,
    "semantic_level": "P2",
    "rationale": "The closed six-event run is a bounded nonvacuity witness for exact acknowledged closure.",
}

for theorem_name in (
    "rejected_event_is_state_noninterfering",
    "closed_state_accepts_no_event",
    "apply_event_preserves_lifecycle_invariant",
    "apply_event_preserves_full_custody",
    "run_events_preserves_lifecycle_invariant",
    "run_events_preserves_full_custody",
    "reachable_closed_state_has_exact_modeled_accounting",
    "wrong_stage_event_is_rejected_without_state_change",
    "substituted_job_is_rejected_without_state_change",
    "substituted_contract_is_rejected_without_state_change",
    "repeated_event_digest_is_rejected_without_state_change",
    "support_assignment_request_is_rejected_without_state_change",
    "external_effect_request_is_rejected_without_state_change",
    "execution_without_audit_is_rejected_without_state_change",
    "adjudication_without_completion_receipt_is_rejected_without_state_change",
    "adjudication_without_residual_owner_is_rejected_without_state_change",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/TypedJobRefinement.lean::{theorem_name}"
    ] = {
        **_typed_job_lifecycle_refinement_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem proves arbitrary-run lifecycle accounting or custody, terminal noninterference, or a closed rejecting countermodel in the exact finite job semantics."
        ),
    }

_intent_execution_lifecycle_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "experiments/intent_execution_vertical_refinement/results/2026-07-15-local.json",
        "experiments/governed_repository_change_slice/results/2026-07-10-local.json",
    ],
    "classification_basis": [
        "the reachable vertical lifecycle is bound to an independently checked governed repository-change result"
    ],
}

for theorem_name in (
    "accepted_step_applies_event",
    "accepted_step_payload_is_well_typed",
    "vertical_initial_satisfies_invariant",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/IntentExecutionRefinement.lean::{theorem_name}"
    ] = {
        **_intent_execution_lifecycle_refinement_base,
        "semantic_level": "P1",
        "rationale": (
            "The theorem exposes an accepted-step consequence or checks the authored induction base; it supports the deeper lifecycle proof but is not itself a run-level result."
        ),
    }

for theorem_name in (
    "accepted_step_preserves_vertical_invariant",
    "accepted_step_preserves_vertical_custody",
    "accepted_step_advances_logical_time",
    "accepted_block_stops_without_changing_effect_accounting",
    "accepted_residualization_increases_residuals_without_effect",
    "accepted_run_preserves_vertical_invariant",
    "accepted_run_preserves_vertical_custody",
    "accepted_run_never_reverses_logical_time",
    "reachable_delivery_has_full_modeled_custody",
    "substituted_root_contract_is_rejected",
    "substituted_parent_artifact_is_rejected",
    "stale_logical_time_is_rejected",
    "observation_payload_on_lowering_is_rejected",
    "effect_payload_on_lowering_is_rejected",
    "delivery_payload_on_lowering_is_rejected",
    "residual_payload_on_lowering_is_rejected",
    "rollback_payload_on_lowering_is_rejected",
    "observation_before_attempted_effect_is_rejected",
    "artifact_binding_before_observation_is_rejected",
    "self_verification_is_rejected",
    "inexact_rollback_is_rejected",
    "quarantine_without_residual_is_rejected",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/IntentExecutionRefinement.lean::{theorem_name}"
    ] = {
        **_intent_execution_lifecycle_refinement_base,
        "semantic_level": "P3",
        "rationale": (
            "The theorem proves a one-step or arbitrary-run lifecycle invariant, a reachable terminal custody result, or a closed rejecting countermodel in the exact finite vertical semantics."
        ),
    }

_proof_contract_transport_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean/AsiStackProofs/ProofCarryingContracts.lean",
        "scripts/validate_circle_contract_pack_archive.py",
        "experiments/circle_contract_pack_archive/results/2026-07-05-local.json",
    ],
}

for theorem_name in (
    "downstream_ready_receipt_missing_boundary_field_rejected",
    "contract_readiness_alone_cannot_promote_downstream_claim",
    "promoted_downstream_claim_without_contract_ready_rejected",
    "consumer_gate_acceptance_with_stale_or_unsupported_receipt_rejected",
    "passing_replay_without_replay_artifacts_rejected",
    "circle_public_consumer_gate_promotion_overclaim_rejected",
    "circle_public_consumer_gate_missing_mutation_control_rejected",
    "revoked_descendant_consumer_is_rejected_without_state_change",
    "root_identity_mismatch_rejects_resolution_noninterferingly",
    "parent_mismatch_rejects_descendant_issue_noninterferingly",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofCarryingContracts.lean::{theorem_name}"
    ] = {
        **_proof_contract_transport_refinement_base,
        "semantic_level": "P1",
        "classification_basis": [
            "one-step finite receipt, replay, consumer, identity, parent, or revocation rejection consequence"
        ],
        "rationale": (
            "The theorem closes a local authored contract or transition guard; it does not establish external theorem truth or deployed transport."
        ),
    }

for theorem_name in (
    "reference_contract_trace_consumes_then_revokes_lineage",
    "unrelated_lineage_remains_consumable_after_root_revocation",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofCarryingContracts.lean::{theorem_name}"
    ] = {
        **_proof_contract_transport_refinement_base,
        "semantic_level": "P2",
        "classification_basis": [
            "closed reachable witness consumes a descendant, revokes its lineage, and preserves an unrelated consumer route"
        ],
        "rationale": (
            "The theorem establishes bounded nonvacuity for the authored transport lifecycle, not service availability or useful transfer."
        ),
    }

for theorem_name in (
    "contract_transport_step_preserves_identity_and_authority",
    "contract_transport_step_preserves_custody",
    "contract_transport_step_preserves_invariant",
    "run_contract_transport_append",
    "root_revocation_invalidates_root_and_descendant",
    "descendant_unusable_after_root_revocation",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofCarryingContracts.lean::{theorem_name}"
    ] = {
        **_proof_contract_transport_refinement_base,
        "semantic_level": "P3",
        "classification_basis": [
            "implementation refinement for the executable finite transport runner, independently checked over its reachable graph"
        ],
        "rationale": (
            "The theorem refines the exact authored transition semantics and is bound to the archive consumer; artifact identities and checks remain inputs."
        ),
    }

for theorem_name in (
    "contract_transport_rejected_event_is_noninterfering",
    "contract_transport_custody_transitive",
    "run_contract_transport_preserves_custody",
    "run_contract_transport_preserves_invariant",
    "root_lineage_containment_survives_one_step",
    "root_revocation_is_persistent",
    "independent_lineage_availability_survives_one_step",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofCarryingContracts.lean::{theorem_name}"
    ] = {
        **_proof_contract_transport_refinement_base,
        "semantic_level": "P4",
        "classification_basis": [
            "finite noninterference or arbitrary-run safety composition over transport custody, authority, revocation, and unrelated-lineage state"
        ],
        "rationale": (
            "The theorem prevents a named finite transport interference under authored inputs; authenticated cross-system enforcement remains unproved."
        ),
    }

for theorem_name in (
    "root_lineage_containment_survives_arbitrary_suffix",
    "revoked_root_excludes_descendant_use_after_any_suffix",
    "independent_lineage_availability_survives_arbitrary_suffix",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/ProofCarryingContracts.lean::{theorem_name}"
    ] = {
        **_proof_contract_transport_refinement_base,
        "semantic_level": "P5",
        "classification_basis": [
            "arbitrary finite suffix containment or unrelated-lineage availability in the authored transport lifecycle"
        ],
        "rationale": (
            "The theorem establishes bounded suffix safety or availability only; no unbounded liveness, distributed revocation, or service guarantee follows."
        ),
    }

_coil_memory_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean/AsiStackProofs/CoilAttentionMemory.lean",
        "scripts/validate_cyclic_memory_contracts.py",
    ],
}

for theorem_name in (
    "reused_cyclic_slot_without_winding_or_residual_rejected",
    "structure_only_retrieval_quality_promotion_rejected",
    "recurrence_without_budget_exit_or_fallback_rejected",
    "stale_read_admitted_as_fresh_without_residual_rejected",
    "same_residue_different_winding_is_not_fresh",
    "stale_classification_blocks_fresh_consumption",
    "recurrence_at_budget_is_rejected_noninterferingly",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CoilAttentionMemory.lean::{theorem_name}"
    ] = {
        **_coil_memory_refinement_base,
        "semantic_level": "P1",
        "classification_basis": [
            "one-step finite rejection, freshness, or admission consequence in the authored cyclic-memory model"
        ],
        "rationale": (
            "The theorem closes a local finite guard or transition consequence; it does not establish deployed memory behavior or semantic utility."
        ),
    }

for theorem_name in (
    "residue_collision_addresses_are_distinct",
    "residue_only_projection_collides",
    "residue_only_projection_is_not_injective",
    "no_residue_only_decoder_recovers_every_cyclic_address",
    "complete_address_encoding_round_trips",
    "complete_address_encoding_is_injective",
    "fresh_trace_reaches_bounded_recurrence_closure",
    "third_recurrence_step_is_rejected_without_state_change",
    "stale_alias_trace_uses_fallback_and_closes",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CoilAttentionMemory.lean::{theorem_name}"
    ] = {
        **_coil_memory_refinement_base,
        "semantic_level": "P2",
        "classification_basis": [
            "bounded address countermodel, universal complete-address witness, or closed reachable lifecycle witness"
        ],
        "rationale": (
            "The theorem establishes nonvacuity or a finite address impossibility inside the authored model; no runtime address truth or memory quality follows."
        ),
    }

for theorem_name in (
    "memory_lifecycle_step_preserves_identity_and_authority",
    "memory_lifecycle_step_preserves_custody",
    "memory_lifecycle_step_preserves_invariant",
    "memory_lifecycle_step_recurrence_monotone",
    "memory_lifecycle_step_preserves_stage_coherence",
    "run_memory_lifecycle_append",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CoilAttentionMemory.lean::{theorem_name}"
    ] = {
        **_coil_memory_refinement_base,
        "semantic_level": "P3",
        "classification_basis": [
            "implementation refinement for the executable finite lifecycle, independently checked across its reachable state graph"
        ],
        "rationale": (
            "The theorem refines the exact transition runner and is bound to an independent exhaustive consumer; all state fields remain authored."
        ),
    }

for theorem_name in (
    "memory_lifecycle_rejected_event_is_noninterfering",
    "memory_custody_transitive",
    "run_memory_lifecycle_preserves_custody",
    "run_memory_lifecycle_preserves_invariant",
    "run_memory_lifecycle_recurrence_monotone",
    "run_memory_lifecycle_preserves_stage_coherence",
    "stale_path_containment_survives_one_step",
    "stale_path_excludes_fresh_consumption",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CoilAttentionMemory.lean::{theorem_name}"
    ] = {
        **_coil_memory_refinement_base,
        "semantic_level": "P4",
        "classification_basis": [
            "finite noninterference or arbitrary-run safety composition over custody, budget, authority, coherence, or stale-path state"
        ],
        "rationale": (
            "The theorem prevents a named class of finite lifecycle interference under authored inputs; it does not prove cross-request isolation or deployed enforcement."
        ),
    }

for theorem_name in (
    "stale_path_containment_survives_arbitrary_suffix",
    "stale_detection_excludes_fresh_consumption_after_any_suffix",
    "closed_memory_lifecycle_step_is_absorbing",
    "closed_memory_lifecycle_suffix_is_absorbing",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CoilAttentionMemory.lean::{theorem_name}"
    ] = {
        **_coil_memory_refinement_base,
        "semantic_level": "P5",
        "classification_basis": [
            "arbitrary finite suffix containment or absorbing terminal behavior for the authored lifecycle"
        ],
        "rationale": (
            "The theorem establishes bounded suffix safety or closure absorption; it does not establish unbounded liveness, recovery, concurrency, or runtime behavior."
        ),
    }

_cyclic_mixer_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean/AsiStackProofs/CyclicMixers.lean",
        "scripts/validate_circle_cyclic_mixer_receipt_slice.py",
        "experiments/circle_cyclic_mixer_receipt_slice/results/2026-07-05-local.json",
    ],
}

for theorem_name in (
    "cyclic_mixer_claim_missing_claim_partition_rejected",
    "cyclic_substrate_promotion_without_baselines_or_tradeoffs_rejected",
    "cyclic_alias_diagnostic_without_winding_or_visible_residual_rejected",
    "cyclic_adoption_without_complete_tradeoff_packet_rejected",
    "hardware_mismatch_without_refusal_path_rejected",
    "missing_baseline_matrix_rejects_without_state_change",
    "incomplete_tradeoff_partition_rejects_without_state_change",
    "hardware_mismatch_without_refusal_rejects_without_state_change",
    "canary_admission_without_fallback_rejects_without_state_change",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CyclicMixers.lean::{theorem_name}"
    ] = {
        **_cyclic_mixer_refinement_base,
        "semantic_level": "P1",
        "classification_basis": [
            "one-step finite claim-partition, baseline, tradeoff, hardware, alias, or fallback rejection consequence"
        ],
        "rationale": (
            "The theorem closes a named local adoption guard; it does not establish model quality, performance, or deployed routing."
        ),
    }

for theorem_name in (
    "reference_cyclic_candidate_reaches_canary_eligibility",
    "reference_cyclic_candidate_preserves_zero_authority",
    "reference_regression_retires_through_fallback",
    "structural_summary_collides_across_canary_eligibility",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CyclicMixers.lean::{theorem_name}"
    ] = {
        **_cyclic_mixer_refinement_base,
        "semantic_level": "P2",
        "classification_basis": [
            "closed reachable witness for canary eligibility, fallback retirement, non-authority, or structural-summary insufficiency"
        ],
        "rationale": (
            "The theorem establishes bounded nonvacuity for the authored candidate lifecycle, not useful or safe canary behavior."
        ),
    }

for theorem_name in (
    "cyclic_candidate_step_preserves_custody",
    "cyclic_candidate_step_preserves_invariant",
    "run_cyclic_candidate_append",
    "no_structural_summary_classifier_recovers_canary_eligibility",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CyclicMixers.lean::{theorem_name}"
    ] = {
        **_cyclic_mixer_refinement_base,
        "semantic_level": "P3",
        "classification_basis": [
            "implementation refinement or information boundary for the executable finite canary-admission runner"
        ],
        "rationale": (
            "The theorem refines exact authored transition or information-loss semantics; metric and artifact truth remain inputs."
        ),
    }

for theorem_name in (
    "cyclic_candidate_rejected_event_is_noninterfering",
    "cyclic_candidate_custody_transitive",
    "run_cyclic_candidate_preserves_custody",
    "run_cyclic_candidate_preserves_invariant",
    "retired_candidate_is_absorbing_one_step",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/CyclicMixers.lean::{theorem_name}"
    ] = {
        **_cyclic_mixer_refinement_base,
        "semantic_level": "P4",
        "classification_basis": [
            "finite noninterference or arbitrary-run safety composition over candidate custody, authority, gate coherence, or retirement"
        ],
        "rationale": (
            "The theorem prevents a named finite gate interference under authored inputs; deployed substrate enforcement remains unproved."
        ),
    }

CURRENT_SEMANTIC_OVERRIDES[
    "lean/AsiStackProofs/CyclicMixers.lean::retired_candidate_is_absorbing_for_any_suffix"
] = {
    **_cyclic_mixer_refinement_base,
    "semantic_level": "P5",
    "classification_basis": [
        "arbitrary finite suffix absorption for a retired cyclic candidate"
    ],
    "rationale": (
        "The theorem establishes bounded terminal closure only; it does not establish unbounded liveness, recovery, or deployed rollback."
    ),
}

_living_book_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean/AsiStackProofs/LivingBook.lean",
        "scripts/validate_living_book_change_packets.py",
        "experiments/living_book_change_packets/fixtures/valid_chapter_revision.json",
    ],
}

for theorem_name in (
    "missing_proof_manifest_sync_rejects_without_state_change",
    "duplicate_stable_ids_reject_structure_sync_without_state_change",
    "failed_render_rejects_validation_without_state_change",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/LivingBook.lean::{theorem_name}"
    ] = {
        **_living_book_refinement_base,
        "semantic_level": "P1",
        "classification_basis": [
            "one-step finite synchronization or validation rejection consequence"
        ],
        "rationale": (
            "The theorem rejects a named malformed manifest-change event without proving manuscript quality or release readiness."
        ),
    }

for theorem_name in (
    "number_manifest_preserves_length",
    "reference_manifest_change_reaches_accepted_current",
    "reference_manifest_change_has_exact_receipt_count",
    "manifest_thin_summary_collides_across_acceptance",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/LivingBook.lean::{theorem_name}"
    ] = {
        **_living_book_refinement_base,
        "semantic_level": "P2",
        "classification_basis": [
            "inductive manifest witness or closed reachable change-lifecycle witness"
        ],
        "rationale": (
            "The theorem establishes bounded nonvacuity for derived numbering or one authored change transaction only."
        ),
    }

for theorem_name in (
    "number_manifest_preserves_stable_id_order",
    "number_manifest_derives_consecutive_ordinals",
    "manifest_change_step_preserves_custody",
    "run_manifest_change_preserves_custody",
    "manifest_change_step_preserves_invariant",
    "run_manifest_change_preserves_invariant",
    "run_manifest_change_append",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/LivingBook.lean::{theorem_name}"
    ] = {
        **_living_book_refinement_base,
        "semantic_level": "P3",
        "classification_basis": [
            "inductive implementation refinement for dynamic numbering, identity custody, gate coherence, or trace composition"
        ],
        "rationale": (
            "The theorem refines the executable finite manifest compiler or transaction runner; source, prose, and validator truth remain inputs."
        ),
    }

for theorem_name in (
    "manifest_change_rejected_event_is_noninterfering",
    "reference_manifest_change_has_no_support_or_publication_authority",
    "accepted_manifest_change_is_absorbing_one_step",
    "rolled_back_manifest_change_is_absorbing_one_step",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/LivingBook.lean::{theorem_name}"
    ] = {
        **_living_book_refinement_base,
        "semantic_level": "P4",
        "classification_basis": [
            "finite noninterference or terminal-safety property for support, publication authority, or rejected change events"
        ],
        "rationale": (
            "The theorem constrains local transaction authority and terminal reopening, not public deployment or scholarly quality."
        ),
    }

for theorem_name in (
    "accepted_manifest_change_is_absorbing_for_any_suffix",
    "rolled_back_manifest_change_is_absorbing_for_any_suffix",
    "no_manifest_thin_summary_classifier_recovers_acceptance",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/LivingBook.lean::{theorem_name}"
    ] = {
        **_living_book_refinement_base,
        "semantic_level": "P5",
        "classification_basis": [
            "arbitrary finite suffix closure or impossibility of recovering acceptance from a lossy manifest summary"
        ],
        "rationale": (
            "The theorem establishes bounded terminal closure or information insufficiency only; it does not establish future-maintainer liveness or release correctness."
        ),
    }

_prototype_roadmap_refinement_base = {
    "disposition": "retain",
    "witness_refs": [
        "lean/AsiStackProofs/PrototypeRoadmap.lean",
        "scripts/validate_prototype_phase_gates.py",
        "experiments/prototype_phase_gates/results/2026-07-02-local.json",
    ],
}

for theorem_name in (
    "incomplete_dependency_count_rejects_without_state_change",
    "dependency_inversion_rejects_without_state_change",
    "missing_rollback_plan_rejects_execution_without_state_change",
    "self_improvement_without_independent_execution_evaluator_rejected",
    "failed_execution_acceptance_gates_reject_integration",
    "phase_debt_without_retirement_condition_rejects_integration",
    "promotion_without_evidence_transition_rejects_review_handoff",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/PrototypeRoadmap.lean::{theorem_name}"
    ] = {
        **_prototype_roadmap_refinement_base,
        "semantic_level": "P1",
        "classification_basis": [
            "one-step finite dependency, evaluator, rollback, debt, or evidence-gate rejection consequence"
        ],
        "rationale": (
            "The theorem rejects one named malformed phase event without establishing real phase execution or gate competence."
        ),
    }

for theorem_name in (
    "valid_prototype_dependency_cannot_be_self_referential",
    "adjacent_prototype_dependencies_compose_strict_order",
    "reference_prototype_phase_execution_reaches_integrated",
    "reference_prototype_phase_execution_has_exact_receipt_count",
    "reference_prototype_promotion_reaches_evidence_review",
    "prototype_phase_thin_summary_collides_across_integration",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/PrototypeRoadmap.lean::{theorem_name}"
    ] = {
        **_prototype_roadmap_refinement_base,
        "semantic_level": "P2",
        "classification_basis": [
            "strict finite dependency-order result or closed reachable phase-lifecycle witness"
        ],
        "rationale": (
            "The theorem establishes dependency-order structure or bounded nonvacuity for one authored phase transaction only."
        ),
    }

for theorem_name in (
    "prototype_phase_execution_step_preserves_custody",
    "run_prototype_phase_execution_preserves_custody",
    "prototype_phase_execution_step_preserves_invariant",
    "run_prototype_phase_execution_preserves_invariant",
    "run_prototype_phase_execution_append",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/PrototypeRoadmap.lean::{theorem_name}"
    ] = {
        **_prototype_roadmap_refinement_base,
        "semantic_level": "P3",
        "classification_basis": [
            "inductive implementation refinement for phase identity custody, gate coherence, or trace composition"
        ],
        "rationale": (
            "The theorem refines the executable finite phase runner while dependency truth and evaluator competence remain authored inputs."
        ),
    }

for theorem_name in (
    "prototype_phase_rejected_event_is_noninterfering",
    "reference_prototype_phase_execution_has_no_support_or_external_effect",
    "reference_prototype_promotion_has_no_support_or_external_effect",
    "integrated_prototype_phase_is_absorbing_one_step",
    "evidence_review_prototype_phase_is_absorbing_one_step",
    "rolled_back_prototype_phase_is_absorbing_one_step",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/PrototypeRoadmap.lean::{theorem_name}"
    ] = {
        **_prototype_roadmap_refinement_base,
        "semantic_level": "P4",
        "classification_basis": [
            "finite noninterference or terminal-safety property for rejected phase events, support authority, or external effects"
        ],
        "rationale": (
            "The theorem constrains the local transaction but does not establish a deployed build controller, rollback, or safe execution."
        ),
    }

for theorem_name in (
    "integrated_prototype_phase_is_absorbing_for_any_suffix",
    "evidence_review_prototype_phase_is_absorbing_for_any_suffix",
    "rolled_back_prototype_phase_is_absorbing_for_any_suffix",
    "no_prototype_phase_thin_summary_classifier_recovers_integration",
):
    CURRENT_SEMANTIC_OVERRIDES[
        f"lean/AsiStackProofs/PrototypeRoadmap.lean::{theorem_name}"
    ] = {
        **_prototype_roadmap_refinement_base,
        "semantic_level": "P5",
        "classification_basis": [
            "arbitrary finite suffix closure or impossibility of recovering integration from a lossy phase summary"
        ],
        "rationale": (
            "The theorem establishes bounded terminal closure or information insufficiency only; it does not establish liveness or execution quality."
        ),
    }

# Older validation-registry entries predate per-unit input_artifact indexing.
# These explicit aliases recover only known, validator-owned module bindings;
# they do not infer a binding from filename similarity.
LEGACY_VALIDATOR_ALIASES = {
    "lean/AsiStackProofs/RuntimeAdapters.lean": {
        "validate_runtime_adapter_permissions.py",
        "validate_runtime_adapter_effect_probe.py",
        "validate_runtime_adapter_adversarial_boundary_probe.py",
    },
    "lean/AsiStackProofs/Planning.lean": {
        "validate_plan_execution_contracts.py",
        "validate_planning_scheduler_state_probe.py",
        "validate_planning_runtime_replan_delta.py",
    },
    "lean/AsiStackProofs/Alignment.lean": {"validate_constitutional_alignment.py"},
    "lean/AsiStackProofs/ValueConflict.lean": {"validate_value_conflicts.py"},
    "lean/AsiStackProofs/Efficiency.lean": {"validate_costed_route_resource_slice.py"},
    "lean/AsiStackProofs/SecurityKernel.lean": {"validate_security_kernel.py"},
    "lean/AsiStackProofs/StableCapabilityFields.lean": {
        "validate_stable_capability_fields.py",
        "validate_scf_lifecycle_trace.py",
    },
    "lean/AsiStackProofs/FailureModes.lean": {"validate_architecture_red_team.py"},
    "lean/AsiStackProofs/ProofCarryingContracts.lean": {
        "validate_circle_contract_pack_archive.py",
        "validate_circle_public_replay.py",
    },
    "lean/AsiStackProofs/SearchSubstrates.lean": {"validate_substrate_adoption_trace.py"},
    "lean/AsiStackProofs/ArtifactStewardAgents.lean": {
        "validate_artifact_steward_lifecycle_probe.py"
    },
    "lean/AsiStackProofs/HumanAIOrganizations.lean": {
        "validate_human_ai_organization_accountability.py"
    },
    "lean/AsiStackProofs/MultiAgentDynamics.lean": {
        "validate_multi_agent_systemic_boundary.py"
    },
    "lean/AsiStackProofs/EmbodiedPhysicalSafety.lean": {
        "validate_embodied_physical_safety.py"
    },
    "lean/AsiStackProofs/DangerousCapabilityReview.lean": {
        "validate_dangerous_capability_review.py"
    },
    "lean/AsiStackProofs/MilitaryInteractionReview.lean": {
        "validate_military_interaction_review.py"
    },
    "lean/AsiStackProofs/OpenWeightReleaseReview.lean": {
        "validate_open_weight_release_review.py"
    },
    "lean/AsiStackProofs/CommunicationInfluenceReview.lean": {
        "validate_communication_influence_review.py"
    },
    "lean/AsiStackProofs/ObjectiveLeaseGovernance.lean": {
        "validate_objective_lease_governance.py"
    },
    "lean/AsiStackProofs/AdversarialModelSecurity.lean": {
        "validate_adversarial_model_security.py"
    },
    "lean/AsiStackProofs/ProtectedComputationReview.lean": {
        "validate_protected_computation_review.py"
    },
    "lean/AsiStackProofs/ContentAuthenticityReview.lean": {
        "validate_content_authenticity_review.py"
    },
    "lean/AsiStackProofs/ReplicationContainmentReview.lean": {
        "validate_replication_containment_review.py"
    },
    "lean/AsiStackProofs/InstitutionalLegitimacyReview.lean": {
        "validate_institutional_legitimacy_review.py"
    },
    "lean/AsiStackProofs/SocietalResilienceReview.lean": {
        "validate_societal_resilience_review.py"
    },
    "lean/AsiStackProofs/TheseusReference.lean": {"validate_theseus_report.py"},
    "lean/AsiStackProofs/CyclicMixers.lean": {"validate_circle_cyclic_mixer_receipt_slice.py"},
    "lean/AsiStackProofs/CoilAttentionMemory.lean": {"validate_cyclic_memory_contracts.py"},
    "lean/AsiStackProofs/LivingBook.lean": {"validate_living_book_change_packets.py"},
    "lean/AsiStackProofs/BenchmarkRatchets.lean": {"validate_benchmark_antigoodhart.py"},
    "lean/AsiStackProofs/BibliographyPlan.lean": {"validate_source_notes.py"},
    "lean/AsiStackProofs/GovernanceRights.lean": {"validate_governance_rights.py"},
    "lean/AsiStackProofs/PrototypeRoadmap.lean": {"validate_prototype_phase_gates.py"},
    "lean/AsiStackProofs/SupplyChainIntegrity.lean": {"validate_supply_chain_affected_paths.py"},
}

# Meta-audits inspect proof custody and repository consistency. They are not
# implementations of every theorem in the Lean modules they inventory, and
# therefore must not raise those theorems' semantic implementation-binding
# level merely because the module is an audit input.
META_AUDIT_VALIDATORS = {
    "validate_proof_semantic_rationalization_ledger.py",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def active_chapter_ids() -> set[str]:
    structure = load(STRUCTURE)
    return {
        str(chapter["id"])
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    }


def target_index() -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[str]]]:
    rows = [row for row in load(MANIFEST)["records"] if isinstance(row, dict)]
    by_module: dict[str, list[dict[str, Any]]] = defaultdict(list)
    owners: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        module = str(row["module_path"])
        by_module[module].append(row)
        chapter_id = str(row["chapter_id"])
        if chapter_id not in owners[module]:
            owners[module].append(chapter_id)
    return by_module, owners


def historical_index() -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    historical = load(HISTORICAL)
    by_id = {
        str(row["theorem_id"]): row
        for row in historical.get("baseline_theorems", [])
        if isinstance(row, dict)
    }
    owners: dict[str, list[str]] = defaultdict(list)
    for row in historical.get("baseline_theorems", []):
        if not isinstance(row, dict):
            continue
        module = str(row["module_path"])
        chapter_id = str(row["chapter_id"])
        if chapter_id not in owners[module]:
            owners[module].append(chapter_id)
    return by_id, owners


def cluster_index() -> dict[str, dict[str, Any]]:
    modules: dict[str, dict[str, Any]] = {}
    for path in sorted(CLUSTER_GLOB.glob("*.json")):
        packet = load(path)
        for row in packet.get("module_dispositions", []):
            if not isinstance(row, dict):
                continue
            module_path = str(row.get("path", ""))
            if module_path:
                modules[module_path] = {
                    "cluster_id": packet.get("cluster_id"),
                    "cluster_state": packet.get("state"),
                    "cluster_scope": packet.get("scope"),
                    "cluster_maximum_inference": packet.get("cluster_maximum_inference"),
                    "module_disposition": row.get("disposition"),
                    "module_assumptions": row.get("assumptions", []),
                    "module_consumers": row.get("consumers", []),
                    "module_countermodels": row.get("countermodels", []),
                    "module_mutation_evidence": row.get("mutation_evidence"),
                    "source_ref": str(path.relative_to(ROOT)),
                }
    return modules


def validation_index() -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "validator_refs": [],
            "binding_refs": [],
            "witness_refs": [],
            "observation_contract_refs": [],
            "mutation_refs": [],
        }
    )
    for unit in load(VALIDATION).get("units", []):
        if not isinstance(unit, dict):
            continue
        artifacts = [str(item) for item in unit.get("input_artifacts", [])]
        modules = [item for item in artifacts if item.startswith("lean/AsiStackProofs/") and item.endswith(".lean")]
        script_name = str(unit.get("script", ""))
        if script_name in META_AUDIT_VALIDATORS:
            continue
        modules.extend(
            module
            for module, aliases in LEGACY_VALIDATOR_ALIASES.items()
            if script_name in aliases
        )
        modules = sorted(set(modules))
        if not modules:
            continue
        script = f"scripts/{script_name}"
        binding_refs = [
            item for item in artifacts
            if item.startswith(("schemas/", "tests/fixtures/", "experiments/"))
            or item == "docs/proof_artifact_audit.md"
        ]
        witness_refs = [
            item for item in artifacts
            if item.startswith(("tests/fixtures/", "experiments/"))
            and any(token in item for token in ("results", "fixture", ".valid.", "trace", "receipt"))
        ]
        observation_refs = [
            item for item in artifacts
            if item.startswith("experiments/")
            and any(token in item for token in ("preregistration", "observation", "results"))
        ]
        for module in modules:
            record = index[module]
            record["validator_refs"].append(script)
            record["binding_refs"].extend(binding_refs)
            record["witness_refs"].extend(witness_refs)
            record["observation_contract_refs"].extend(observation_refs)
            negative = str(unit.get("negative_controls", "")).strip()
            if negative:
                record["mutation_refs"].append(f"{script}#{negative}")
    for record in index.values():
        for key in record:
            record[key] = sorted(set(record[key]))
    return dict(index)


def theorem_graph(rows: list[dict[str, Any]]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    ids_by_name: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        ids_by_name[str(row["name"])].append(str(row["theorem_id"]))
    dependencies: dict[str, list[str]] = {}
    consumers: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        identifiers = set(re.findall(r"[A-Za-z_][A-Za-z0-9_'.]*", str(row.get("body", ""))))
        refs = sorted(
            theorem_id
            for name in identifiers - {str(row["name"])}
            for theorem_id in ids_by_name.get(name, [])
        )
        dependencies[str(row["theorem_id"])] = refs
        for theorem_id in refs:
            consumers[theorem_id].append(str(row["theorem_id"]))
    return dependencies, {key: sorted(set(value)) for key, value in consumers.items()}


def statement_key(signature: str) -> str:
    return normalize(re.sub(r"^theorem\s+[^\s:{]+", "theorem <name>", signature))


def owner_ids(
    module: str,
    current_owners: dict[str, list[str]],
    historical_owners: dict[str, list[str]],
    active_ids: set[str],
) -> tuple[list[str], str]:
    owners = [owner for owner in current_owners.get(module, []) if owner in active_ids]
    if owners:
        return sorted(set(owners)), "current proof-target ownership"
    owners = [owner for owner in historical_owners.get(module, []) if owner in active_ids]
    if owners:
        return sorted(set(owners)), "retained historical theorem ownership"
    raise ValueError(f"{module}: no active semantic owner")


def maximum_inference(level: str) -> str:
    return {
        "P0": "Only the declared type, record-shape, equality, or projection fact in the Lean model.",
        "P1": "Only the declared finite route, rejection, or preservation result under the theorem premises.",
        "P2": "Only bounded reachability or nonvacuity for the named local witness and modeled route.",
        "P3": "Only agreement between the Lean statement and the named local refinement, validator, schema, or fixture.",
        "P4": "Only the named bounded cross-component safety or noninterference property under the recorded assumptions and mutations.",
        "P5": "Only the named bounded liveness, recovery, revocation, rollback, or concurrency property; no unbounded progress follows.",
        "P6": "Only the measured semantic bound for the named observation contract, denominator, implementation, and environment.",
    }[level]


def semantic_level(
    row: dict[str, Any],
    binding: dict[str, Any],
    target_text: str,
) -> tuple[str, list[str]]:
    # The target text helps establish that a module is an implementation
    # refinement, but it must not lift every theorem in that module into the
    # strongest semantic class named anywhere in the target packet. P4/P5
    # classification is theorem-statement local.
    text = normalize(f"{row['name']} {row['signature']}").lower()
    has_binding = bool(binding.get("validator_refs") and binding.get("binding_refs"))
    has_witness = bool(binding.get("witness_refs"))
    reasons: list[str] = []
    level = "P0"
    if any(term in text for term in ROUTE_TERMS):
        level = "P1"
        reasons.append("statement encodes a finite route, rejection, or preservation property")
    else:
        reasons.append("statement is limited to type, record, equality, or direct model structure")
    if has_witness and any(term in text for term in REACHABILITY_TERMS):
        level = "P2"
        reasons.append("named bounded fixture/result witnesses the modeled route")
    module_name = str(row["module_path"])
    if has_binding and (
        "Refinement.lean" in module_name
        or "independently implemented" in target_text.lower()
        or "runtime" in target_text.lower()
        or "consumer" in target_text.lower()
    ):
        level = "P3"
        reasons.append("Lean statement is bound to a named validator plus schema, fixture, or result")
    if has_binding and any(term in text for term in CROSS_COMPONENT_TERMS):
        level = "P4"
        reasons.append("statement constrains cross-component authority, effect, support, or adversarial composition")
    if has_binding and any(term in text for term in LIVENESS_TERMS):
        level = "P5"
        reasons.append("statement concerns bounded terminality, recovery, revocation, rollback, or concurrency")
    # P6 is intentionally never inferred from theorem names, tactic shape, or
    # the mere presence of an experiment result.  It requires a separately
    # adjudicated theorem-specific observation contract, which the current
    # estate does not declare.
    return level, reasons


def inherited_disposition(row: dict[str, Any] | None) -> str | None:
    if not row:
        return None
    value = str(row.get("disposition") or "")
    if value.startswith("retain_"):
        return "retain"
    if value == "merge_duplicate":
        return "retire_duplicate"
    if value == "retire_projection_or_assumption_restatement":
        return "retire_narrow_projection"
    if value == "replace_with_stronger_model":
        return "rewrite_with_stronger_model"
    return None


def build() -> tuple[dict[str, Any], str]:
    theorem_rows = current_theorems()
    target_rows, current_owners = target_index()
    historical_rows, historical_owners = historical_index()
    clusters = cluster_index()
    validations = validation_index()
    active_ids = active_chapter_ids()
    dependencies, theorem_consumers = theorem_graph(theorem_rows)
    current_ids_by_name: dict[str, list[str]] = defaultdict(list)
    for theorem_row in theorem_rows:
        current_ids_by_name[str(theorem_row["name"])].append(str(theorem_row["theorem_id"]))

    # Literal theorem text is comparable for retirement only inside the same
    # namespace/model.  The same words over module-local State/Packet types are
    # analogous proof obligations, not interchangeable propositions.
    literal_pattern_groups: dict[str, list[str]] = defaultdict(list)
    duplicate_groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in theorem_rows:
        key = statement_key(str(row["signature"]))
        literal_pattern_groups[key].append(str(row["theorem_id"]))
        duplicate_groups[(str(row["module_path"]), key)].append(str(row["theorem_id"]))
    duplicate_canonical: dict[str, str] = {}
    for theorem_ids in duplicate_groups.values():
        if len(theorem_ids) > 1:
            canonical = sorted(theorem_ids)[0]
            for theorem_id in theorem_ids:
                duplicate_canonical[theorem_id] = canonical

    records: list[dict[str, Any]] = []
    for row in theorem_rows:
        theorem_id = str(row["theorem_id"])
        module = str(row["module_path"])
        old = historical_rows.get(theorem_id)
        binding = validations.get(module, {
            "validator_refs": [],
            "binding_refs": [],
            "witness_refs": [],
            "observation_contract_refs": [],
            "mutation_refs": [],
        })
        targets = target_rows.get(module, [])
        target_text = " ".join(str(target.get("formal_target", "")) for target in targets)
        owners, ownership_basis = owner_ids(module, current_owners, historical_owners, active_ids)
        level, basis = semantic_level(row, binding, target_text)
        cluster = clusters.get(module)

        assumptions = [
            (
                f"The exact Lean signature is authoritative and contains "
                f"{str(row['signature']).count('->')} explicit implication premise(s)."
            ),
            (
                "All record fields, predicates, identities, and booleans supplied to the theorem are assumed "
                "truthful with respect to the intended runtime; Lean does not establish that bridge."
            ),
        ]
        if old:
            assumptions.extend(str(item) for item in old.get("assumptions", []) if str(item).strip())
        if cluster:
            assumptions.extend(str(item) for item in cluster.get("module_assumptions", []) if str(item).strip())
        assumptions = list(dict.fromkeys(assumptions))

        consumer_refs = [f"proof-target:{target['tag']}" for target in targets]
        if old:
            consumer_refs.extend(str(item) for item in old.get("consumer_refs", []))
            consumer_refs.extend(str(item) for item in old.get("runtime_consumer_refs", []))
        if cluster:
            consumer_refs.extend(str(item) for item in cluster.get("module_consumers", []))
        consumer_refs.extend(binding.get("validator_refs", []))
        consumer_refs.extend(f"theorem:{item}" for item in theorem_consumers.get(theorem_id, []))
        consumer_refs = sorted(set(item for item in consumer_refs if item))

        mutation_refs = list(binding.get("mutation_refs", []))
        if old:
            mutation_refs.extend(str(item) for item in old.get("mutation_refs", []))
        if cluster and cluster.get("module_mutation_evidence"):
            mutation_refs.append(f"{cluster['source_ref']}#{cluster['module_mutation_evidence']}")
        mutation_refs = sorted(set(item for item in mutation_refs if item))

        countermodel_refs: list[str] = []
        if old:
            countermodel_refs.extend(str(item) for item in old.get("countermodel_refs", []))
        if cluster:
            countermodel_refs.extend(
                f"{cluster['source_ref']}#countermodel:{normalize(str(item))}"
                for item in cluster.get("module_countermodels", [])
            )
        countermodel_refs = sorted(set(countermodel_refs))

        witness_refs = sorted(set(binding.get("witness_refs", [])))
        if witness_refs:
            witness_state = "bounded_local_witness_present"
            witness_rationale = "A registered validator names at least one fixture, trace, receipt, or result artifact."
        elif any(term in normalize(str(row["name"])).lower() for term in ("unreachable", "impossible", "cannot")):
            witness_state = "explicit_formal_unreachability_only"
            witness_rationale = "The theorem states a formal impossibility, but no independent runtime witness is inferred."
        else:
            witness_state = "no_reachable_witness_identified"
            witness_rationale = "No registered bounded fixture or result is bound directly to this theorem module."

        binding_refs = sorted(set(binding.get("binding_refs", [])))
        if binding.get("validator_refs") and binding_refs:
            implementation_binding = "validator_and_artifact_bound"
        elif binding.get("validator_refs"):
            implementation_binding = "validator_only"
        else:
            implementation_binding = "formal_model_only"

        inherited = inherited_disposition(old)
        semantic_override = CURRENT_SEMANTIC_OVERRIDES.get(theorem_id)
        if semantic_override and semantic_override.get("witness_refs"):
            witness_refs = sorted(
                set(str(item) for item in semantic_override["witness_refs"])
            )
            witness_state = "bounded_local_witness_present"
            witness_rationale = (
                "A theorem-specific manual semantic review names the closed Lean witness."
            )
        if semantic_override and semantic_override.get("semantic_level"):
            level = str(semantic_override["semantic_level"])
            basis = [str(item) for item in semantic_override["classification_basis"]]
        duplicate_of = duplicate_canonical.get(theorem_id)
        duplicate_kind: str | None = None
        if duplicate_of and duplicate_of != theorem_id:
            duplicate_kind = "exact_normalized_statement"
        elif old and str(old.get("disposition") or "") == "merge_duplicate":
            replacement_names = [
                str(item).split(":", 1)[1]
                for item in old.get("replacement_refs", [])
                if str(item).startswith("lean-theorem:")
            ]
            candidates = [
                candidate
                for name in replacement_names
                for candidate in current_ids_by_name.get(name, [])
            ]
            same_module = [
                candidate for candidate in candidates
                if candidate.startswith(f"{module}::")
            ]
            if same_module or candidates:
                duplicate_of = sorted(same_module or candidates)[0]
                duplicate_kind = "reviewed_semantic_duplicate"
        if semantic_override:
            duplicate_of = None
            duplicate_kind = None
            disposition = str(semantic_override["disposition"])
            rationale = str(semantic_override["rationale"])
        elif duplicate_of and duplicate_of != theorem_id:
            disposition = "retire_duplicate"
            if duplicate_kind == "exact_normalized_statement":
                rationale = f"An exact normalized current statement is already retained as {duplicate_of}."
            else:
                rationale = (
                    f"The frozen semantic review identifies {duplicate_of} as the retained "
                    "equivalent model result."
                )
        elif inherited:
            disposition = inherited
            rationale = (
                "Disposition is carried forward from the frozen semantic review, but the current overlay "
                "recomputes scope, bindings, witnesses, and maximum inference."
            )
        elif not consumer_refs and not theorem_consumers.get(theorem_id):
            disposition = "retire_unused_candidate"
            rationale = "No proof target, theorem dependency consumer, runtime validator, or reviewed module consumer is identified."
        elif level == "P0" and any(term in str(row["name"]).lower() for term in STRONG_NAME_TERMS):
            disposition = "rewrite_scope_language"
            rationale = "The theorem name can imply more than its current record-shape or projection semantics."
        else:
            disposition = "retain"
            rationale = "The theorem has a named proof, theorem, validator, or semantic-cluster consumer at its bounded level."

        if semantic_override:
            review_basis = "current_manual_semantic_spot_check"
        elif old and old.get("review_state") in {"semantically_reviewed", "terminally_dispositioned"}:
            review_basis = "inherited_semantic_review_reprojected_to_current_overlay"
        elif cluster:
            review_basis = "current_module_semantic_cluster_review"
        elif binding.get("validator_refs"):
            review_basis = "current_validator_contract_review"
        else:
            review_basis = "conservative_current_machine_classification"

        records.append({
            "theorem_id": theorem_id,
            "module_path": module,
            "name": row["name"],
            "source_start_line": row["source_start_line"],
            "source_end_line": row["source_end_line"],
            "current_signature": row["signature"],
            "current_block_sha256": row["baseline_block_sha256"],
            "syntax_depth_class": row["depth_class"],
            "syntax_depth_evidence": row["depth_evidence"],
            "semantic_level": level,
            "semantic_level_meaning": LEVEL_MEANINGS[level],
            "classification_basis": basis,
            "semantic_owner_ids": owners,
            "ownership_basis": ownership_basis,
            "assumptions": assumptions,
            "candidate_target_refs": sorted(f"proof-target:{target['tag']}" for target in targets),
            "theorem_dependency_refs": dependencies.get(theorem_id, []),
            "theorem_consumer_refs": theorem_consumers.get(theorem_id, []),
            "consumer_refs": consumer_refs,
            "witness": {
                "state": witness_state,
                "refs": witness_refs,
                "rationale": witness_rationale,
            },
            "implementation_binding": {
                "state": implementation_binding,
                "validator_refs": sorted(set(binding.get("validator_refs", []))),
                "artifact_refs": binding_refs,
            },
            "mutation_refs": mutation_refs,
            "countermodel_refs": countermodel_refs,
            "empirical_observation_contract_refs": sorted(set(binding.get("observation_contract_refs", []))),
            "maximum_inference": maximum_inference(level),
            "disposition": disposition,
            "duplicate_of": duplicate_of if duplicate_of != theorem_id else None,
            "duplicate_kind": duplicate_kind if duplicate_of != theorem_id else None,
            "disposition_rationale": rationale,
            "review_basis": review_basis,
            "support_state_effect": "none",
        })

    level_counts = Counter(row["semantic_level"] for row in records)
    disposition_counts = Counter(row["disposition"] for row in records)
    review_counts = Counter(row["review_basis"] for row in records)
    binding_counts = Counter(row["implementation_binding"]["state"] for row in records)
    witness_counts = Counter(row["witness"]["state"] for row in records)
    module_counts = Counter(row["module_path"] for row in records)
    chapter_counts = Counter(owner for row in records for owner in row["semantic_owner_ids"])

    overlay = {
        "schema_version": "asi_stack.proof_semantic_depth_overlay.v1",
        "as_of": "2026-07-25",
        "roadmap_lane": "C6-P0-P6-semantic-proof-rationalization",
        "state": "current_live_estate_classified_before_new_formal_expansion",
        "generated_from": [
            "lean/AsiStackProofs/*.lean",
            "proofs/proof_manifest.json",
            "proofs/proof_rationalization_registry.json",
            "proofs/semantic_cluster_audits/*.json",
            "validation/registry.json",
            "book_structure.json",
        ],
        "level_definitions": LEVEL_MEANINGS,
        "classification_policy": {
            "syntax_is_not_semantics": True,
            "p6_is_never_inferred_from_tactic_shape_or_result_presence": True,
            "p2_requires_a_named_bounded_witness": True,
            "p3_or_higher_requires_a_named_validator_and_binding_artifact": True,
            "cross_module_literal_similarity_never_authorizes_retirement": True,
            "duplicate_retirement_requires_same_model_identity_or_explicit_frozen_review": True,
            "current_semantic_review_may_overturn_frozen_disposition_without_mutating_history": True,
            "unused_or_duplicate_results_receive_retirement_dispositions": True,
            "support_state_effect": "none",
        },
        "summary": {
            "current_theorem_count": len(records),
            "current_module_count": len(module_counts),
            "semantic_owner_chapter_count": len(chapter_counts),
            "semantic_level_counts": {key: level_counts.get(key, 0) for key in LEVEL_MEANINGS},
            "disposition_counts": dict(sorted(disposition_counts.items())),
            "review_basis_counts": dict(sorted(review_counts.items())),
            "implementation_binding_counts": dict(sorted(binding_counts.items())),
            "witness_state_counts": dict(sorted(witness_counts.items())),
            "duplicate_group_count": sum(len(value) > 1 for value in duplicate_groups.values()),
            "cross_module_literal_pattern_group_count": sum(
                len({theorem_id.split("::", 1)[0] for theorem_id in value}) > 1
                for value in literal_pattern_groups.values()
            ),
            "support_state_effect": "none",
        },
        "records": records,
        "non_claims": [
            "This overlay classifies the meaning and custody of live Lean declarations; it does not make theorem count a success metric.",
            "A P-level is a semantic kind, not a scalar confidence score, and it does not promote any chapter or claim.",
            "Validator, fixture, or experiment references establish only the named bounded binding; they do not prove deployment, transfer, SOTA, AGI, or ASI.",
            "P6 remains empty unless a theorem-specific empirical observation contract is separately frozen and adjudicated.",
        ],
    }

    module_lines: list[str] = []
    for module in sorted(module_counts):
        module_records = [row for row in records if row["module_path"] == module]
        levels = Counter(row["semantic_level"] for row in module_records)
        dispositions = Counter(row["disposition"] for row in module_records)
        owners = sorted({owner for row in module_records for owner in row["semantic_owner_ids"]})
        module_lines.append(
            f"| `{module}` | {module_counts[module]} | "
            + ", ".join(f"{level}:{levels.get(level, 0)}" for level in LEVEL_MEANINGS)
            + " | "
            + ", ".join(f"{key}:{value}" for key, value in sorted(dispositions.items()))
            + " | "
            + ", ".join(f"`{owner}`" for owner in owners)
            + " |"
        )

    action_rows = [
        row for row in records
        if row["disposition"] != "retain"
    ]
    action_lines = [
        f"| `{row['theorem_id']}` | {row['semantic_level']} | `{row['disposition']}` | "
        f"{row['disposition_rationale'].replace('|', '&#124;')} |"
        for row in action_rows
    ]
    report = "\n".join([
        "# Current Proof Semantic-Depth Overlay",
        "",
        "Generated by `python3 scripts/build_proof_semantic_depth_overlay.py --write`.",
        "",
        "This is the current C6 overlay over every live Lean theorem declaration. "
        "It preserves the frozen 1,151-theorem historical rationalization registry and "
        f"classifies the {len(records):,}-theorem live estate without treating tactic count "
        "or theorem count as evidence of importance. P-levels are semantic kinds, not "
        "confidence grades.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Live theorem declarations | {len(records)} |",
        f"| Live Lean modules | {len(module_counts)} |",
        f"| Active semantic-owner chapters | {len(chapter_counts)} |",
        *[f"| {level} — {meaning} | {level_counts.get(level, 0)} |" for level, meaning in LEVEL_MEANINGS.items()],
        *[f"| Disposition `{key}` | {value} |" for key, value in sorted(disposition_counts.items())],
        f"| Same-model exact normalized duplicate groups | {overlay['summary']['duplicate_group_count']} |",
        f"| Cross-module literal pattern groups (diagnostic only) | {overlay['summary']['cross_module_literal_pattern_group_count']} |",
        "| Support-state effect | none |",
        "",
        "P6 is deliberately not inferred from an experiment file, a numeric constant, or a "
        "successful validator. It requires a theorem-specific, frozen observation contract. "
        "The current P6 count is therefore an honest statement about the formal estate.",
        "",
        "## Module Distribution",
        "",
        "| Module | Theorems | P0–P6 distribution | Dispositions | Semantic owners |",
        "|---|---:|---|---|---|",
        *module_lines,
        "",
        "## Rewrite And Retirement Queue",
        "",
        "These are dispositions, not deletions. Actual proof or prose removal requires a "
        "separate dependency-safe edit with the retained maximum inference preserved.",
        "",
        "| Theorem | Level | Disposition | Rationale |",
        "|---|---|---|---|",
        *(action_lines or ["| none | — | — | — |"]),
        "",
        "## Non-Claims",
        "",
        *[f"- {item}" for item in overlay["non_claims"]],
        "",
    ])
    return overlay, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    overlay, report = build()
    body = json.dumps(overlay, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        OUTPUT.write_text(body, encoding="utf-8")
        REPORT.write_text(report, encoding="utf-8")
        print(
            f"Wrote current proof semantic-depth overlay: "
            f"{overlay['summary']['current_theorem_count']} theorems across "
            f"{overlay['summary']['current_module_count']} modules."
        )
        return
    errors: list[str] = []
    if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != body:
        errors.append(f"{OUTPUT.relative_to(ROOT)} is stale; run with --write")
    if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != report:
        errors.append(f"{REPORT.relative_to(ROOT)} is stale; run with --write")
    if errors:
        raise SystemExit("Proof semantic-depth overlay generation check failed:\n - " + "\n - ".join(errors))
    print("Current proof semantic-depth overlay generation check passed.")


if __name__ == "__main__":
    main()
