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
    "lean/AsiStackProofs/StableCapabilityFields.lean": {"validate_stable_capability_fields.py"},
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
