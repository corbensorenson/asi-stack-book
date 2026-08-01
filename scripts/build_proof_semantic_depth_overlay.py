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
