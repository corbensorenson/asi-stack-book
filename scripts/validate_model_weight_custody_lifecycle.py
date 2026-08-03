#!/usr/bin/env python3
"""Recompute the bounded model-weight custody lifecycle fixture."""

from __future__ import annotations

import copy
import hashlib
import re
import subprocess
from collections import Counter
from itertools import permutations

from build_canonical_public_status import ROOT, load_json, validate_against_schema

FIXTURE = ROOT / "experiments/model_weight_custody_lifecycle/fixtures/cases.json"
RESULT = ROOT / "experiments/model_weight_custody_lifecycle/results/2026-07-13-local.json"
FIXTURE_SCHEMA = ROOT / "schemas/model_weight_custody_lifecycle_fixture.schema.json"
RESULT_SCHEMA = ROOT / "schemas/model_weight_custody_lifecycle_result.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/ModelWeightCustody.lean"
EXPECTED_IDS = [
    "valid_observed_bounded_load", "invalid_missing_lineage",
    "invalid_missing_policy_digest", "invalid_stale_attestation",
    "invalid_undisclosed_verifier_dependencies", "invalid_unobserved_load",
    "invalid_distribution_authority_laundering",
    "valid_irreversible_distribution_record",
]
EXPECTED_THEOREMS = [
    "required_invalid_attestation_blocks_requested_load",
    "missing_lineage_requires_custody_repair", "complete_observed_load_is_bounded",
    "missing_lineage_blocks_lifecycle", "stale_attestation_requires_refresh",
    "undisclosed_verifier_dependencies_require_review",
    "unobserved_load_requires_observation",
    "distribution_cannot_launder_load_authority",
    "acknowledged_distribution_records_irreversibility",
]
LIFECYCLE_THEOREMS = {
    "accepted_weight_custody_event_is_admissible",
    "accepted_weight_custody_event_is_exact_advance",
    "accepted_weight_custody_event_preserves_identity",
    "accepted_weight_custody_event_is_non_authorizing",
    "accepted_weight_custody_event_never_widens_authority",
    "accepted_weight_custody_event_preserves_descendant_key_inventory",
    "rejected_weight_custody_event_preserves_exact_state",
    "accepted_attestation_is_independent_and_future_bounded",
    "accepted_key_release_is_current_bounded_and_versioned",
    "accepted_load_requires_active_key_receipt_and_no_distribution",
    "accepted_load_observation_is_independent",
    "accepted_key_revocation_closes_authority_and_descendants",
    "accepted_erasure_follows_complete_revocation_and_records_residual",
    "weight_custody_run_preserves_identity_non_authority_and_narrowing",
    "weight_custody_run_preserves_descendant_key_inventory",
    "successful_weight_custody_run_has_valid_trace",
    "erased_weight_custody_state_rejects_every_event",
    "erased_weight_custody_state_has_no_nonempty_run",
    "weight_custody_runs_compose",
    "complete_weight_custody_prefix_reaches_exact_observed_state",
    "complete_weight_custody_trace_reaches_exact_erased_state",
    "weight_custody_stale_version_is_rejected",
    "weight_custody_self_attestation_is_rejected",
    "weight_custody_expired_key_release_is_rejected",
    "weight_custody_authority_widening_is_rejected",
    "weight_custody_distribution_during_load_is_rejected",
    "weight_custody_self_observation_is_rejected",
    "weight_custody_partial_descendant_revocation_is_rejected",
    "weight_custody_same_count_descendant_key_substitution_is_rejected",
    "weight_custody_duplicate_descendant_key_inventory_is_rejected",
    "weight_custody_revocation_count_summary_collides",
    "weight_custody_exact_inventory_separates_count_collision",
    "no_exact_descendant_key_revocation_classifier_from_count_only",
    "weight_custody_erasure_before_revocation_is_rejected",
    "weight_custody_confidentiality_laundering_is_rejected",
}


def apply_lifecycle(state: dict, event: dict) -> dict | None:
    for field in ("artifact", "policy", "environment", "recipient"):
        if event[field] != state[field]:
            return None
    if event["version"] != state["version"] or event["now"] < state["now"]:
        return None
    if event.get("trust") or event.get("confidentiality") or event.get("support") or event.get("effect"):
        return None
    kind = event["kind"]
    if kind == "attest":
        ok = state["stage"] == "sealed" and event["actor"] == state["verifier"] and state["verifier"] != state["custodian"] and event["measurement"] and event["attestation"] and event["now"] < event["expiry"] and event["target_version"] == state["version"] and event["ceiling"] == state["ceiling"]
    elif kind == "release":
        ok = state["stage"] == "attested" and event["actor"] == state["key_service"] and event["policy_auth"] and event["key_receipt"] and event["now"] < state["expiry"] and event["ceiling"] <= state["ceiling"] and event["target_version"] == state["version"] + 1
    elif kind == "load":
        ok = state["stage"] == "key_released" and state["key_active"] and event["actor"] == state["loader"] and event["load_receipt"] and not event["distribution"] and event["now"] < state["expiry"] and event["ceiling"] == state["ceiling"] and event["target_version"] == state["version"]
    elif kind == "observe":
        ok = state["stage"] == "loaded" and event["actor"] == state["observer"] and state["observer"] not in {state["loader"], state["key_service"]} and event["independent"] and event["observation_receipt"] and event["ceiling"] == state["ceiling"] and event["target_version"] == state["version"]
    elif kind == "revoke":
        ok = state["stage"] == "observed" and event["actor"] == state["key_service"] and event["revocation_receipt"] and len(set(state["child_ids"])) == len(state["child_ids"]) and state["children"] == len(state["child_ids"]) and event["revoked_children"] == state["children"] and event["revoked_child_ids"] == state["child_ids"] and event["ceiling"] == 0 and event["target_version"] == state["version"] + 1
    elif kind == "erase":
        ok = state["stage"] == "revoked" and not state["key_active"] and state["revoked_children"] == state["children"] and state["revoked_child_ids"] == state["child_ids"] and event["actor"] == state["loader"] and event["erasure_receipt"] and event["residual"] and event["ceiling"] == 0 and event["target_version"] == state["version"]
    else:
        return None
    if not ok:
        return None
    out = dict(state)
    out["now"] = event["now"]
    if kind == "attest": out.update(stage="attested", expiry=event["expiry"])
    elif kind == "release": out.update(stage="key_released", version=event["target_version"], ceiling=event["ceiling"], key_active=True)
    elif kind == "load": out["stage"] = "loaded"
    elif kind == "observe": out.update(stage="observed", observations=out["observations"] + 1)
    elif kind == "revoke": out.update(stage="revoked", version=event["target_version"], ceiling=0, key_active=False, revoked_children=event["revoked_children"], revoked_child_ids=list(event["revoked_child_ids"]), revocations=out["revocations"] + 1)
    else: out.update(stage="erased", erasures=out["erasures"] + 1, residuals=out["residuals"] + 1)
    return out


def run_lifecycle(initial: dict, events: list[dict]) -> dict | None:
    state = dict(initial)
    custody = {key: copy.deepcopy(state[key]) for key in ("artifact", "policy", "environment", "recipient", "custodian", "verifier", "key_service", "loader", "observer", "children", "child_ids", "support", "effect")}
    ceiling = state["ceiling"]
    for event in events:
        state = apply_lifecycle(state, event)
        if state is None:
            return None
        if any(state[key] != value for key, value in custody.items()) or state["ceiling"] > ceiling:
            raise AssertionError("accepted custody lifecycle changed identity or widened authority")
        ceiling = state["ceiling"]
    return state


def lifecycle_cases() -> tuple[int, int]:
    canonical_child_ids = [167, 173, 179, 181]
    initial = dict(artifact=113, policy=127, environment=131, recipient=137, custodian=139, verifier=149, key_service=151, loader=157, observer=163, version=1, ceiling=6, stage="sealed", children=4, revoked_children=0, child_ids=canonical_child_ids, revoked_child_ids=[], key_active=False, expiry=0, observations=0, revocations=0, erasures=0, residuals=0, now=30, support=0, effect=0)
    base = dict(kind="attest", artifact=113, policy=127, environment=131, recipient=137, actor=149, version=1, target_version=1, ceiling=6, now=31, expiry=50, measurement=True, attestation=True, policy_auth=False, key_receipt=False, load_receipt=False, distribution=False, independent=False, observation_receipt=False, revocation_receipt=False, revoked_children=0, revoked_child_ids=[], erasure_receipt=False, residual=False, trust=False, confidentiality=False, support=False, effect=False)
    def ev(**changes):
        item = dict(base); item.update(changes); return item
    events = [
        ev(),
        ev(kind="release", actor=151, target_version=2, ceiling=4, now=32, policy_auth=True, key_receipt=True),
        ev(kind="load", actor=157, version=2, target_version=2, ceiling=4, now=33, load_receipt=True),
        ev(kind="observe", actor=163, version=2, target_version=2, ceiling=4, now=34, independent=True, observation_receipt=True),
        ev(kind="revoke", actor=151, version=2, target_version=3, ceiling=0, now=35, revocation_receipt=True, revoked_children=4, revoked_child_ids=canonical_child_ids),
        ev(kind="erase", actor=157, version=3, target_version=3, ceiling=0, now=36, erasure_receipt=True, residual=True),
    ]
    final = run_lifecycle(initial, events)
    expected = dict(initial); expected.update(version=3, ceiling=0, stage="erased", revoked_children=4, revoked_child_ids=canonical_child_ids, key_active=False, expiry=50, observations=1, revocations=1, erasures=1, residuals=1, now=36)
    if final != expected:
        raise AssertionError("complete custody lifecycle did not reach exact erased state")
    mutations = ((0,"version",0),(0,"actor",139),(1,"now",50),(1,"ceiling",7),(2,"distribution",True),(3,"actor",157),(4,"revoked_children",3),(4,"revoked_child_ids",[167,173,179,191]),(4,"revoked_child_ids",[173,167,179,181]),(4,"kind","erase"),(0,"confidentiality",True),(5,"version",2))
    for index, field, value in mutations:
        changed = [dict(item) for item in events]; changed[index][field] = value
        if run_lifecycle(initial, changed) is not None:
            raise AssertionError(f"custody lifecycle mutation accepted: {index}:{field}")
    observed = run_lifecycle(initial, events[:4])
    if observed is None:
        raise AssertionError("custody prefix did not reach observed state")
    for candidate in permutations(canonical_child_ids):
        probe = dict(events[4])
        probe["revoked_child_ids"] = list(candidate)
        accepted = apply_lifecycle(observed, probe)
        if (accepted is not None) != (list(candidate) == canonical_child_ids):
            raise AssertionError("descendant-key inventory permutation classified incorrectly")
    duplicate = dict(observed)
    duplicate["child_ids"] = [167, 167, 179, 181]
    duplicate_probe = dict(events[4])
    duplicate_probe["revoked_child_ids"] = list(duplicate["child_ids"])
    if apply_lifecycle(duplicate, duplicate_probe) is not None:
        raise AssertionError("duplicate descendant-key inventory was accepted")
    erased = final
    for kind in ("attest", "release", "load", "observe", "revoke", "erase"):
        probe = dict(base)
        probe["kind"] = kind
        if apply_lifecycle(erased, probe) is not None:
            raise AssertionError(f"erased state accepted terminal event kind: {kind}")
    return len(events), len(mutations), 6, 24


def route(r: dict) -> str:
    if not r["artifact_digest_recorded"]:
        return "retain_as_draft"
    if not r["lineage_recorded"]:
        return "require_lineage_repair"
    if not r["policy_digest_recorded"] or not r["verifier_identity_recorded"] or not r["measurement_recorded"] or not r["recipient_scope_recorded"]:
        return "require_policy_review"
    if not r["expiry_recorded"] or not r["attestation_current"] or not r["attestation_valid"]:
        return "require_fresh_attestation"
    if not r["verifier_dependencies_recorded"]:
        return "require_dependency_review"
    if r["load_requested"] and not r["independent_load_observation_recorded"]:
        return "require_independent_observation"
    if not r["residual_owner_recorded"] or not r["revocation_semantics_recorded"]:
        return "require_policy_review"
    if r["distribution_requested"] and not r["no_authority_grant_recorded"]:
        return "reject_release_laundering"
    if r["distribution_requested"] and r["irreversibility_acknowledged"]:
        return "record_irreversible_release"
    if r["distribution_requested"]:
        return "reject_release_laundering"
    if r["load_requested"]:
        return "admit_bounded_load"
    return "retain_as_draft"


def semantic_errors(data: dict) -> list[str]:
    fixture, result = data["fixture"], data["result"]
    errors: list[str] = []
    cases = fixture.get("cases", [])
    if [case.get("id") for case in cases] != EXPECTED_IDS:
        errors.append("case identity/order drifted")
    computed = []
    for case in cases:
        actual = route(case["record"])
        computed.append({"id": case["id"], "expected_route": case["expected_route"], "actual_route": actual, "passed": actual == case["expected_route"]})
        if actual != case["expected_route"]:
            errors.append(f"{case['id']}: expected {case['expected_route']}, recomputed {actual}")
    if result.get("case_results") != computed:
        errors.append("tracked result does not equal deterministic recomputation")
    if result.get("route_counts") != dict(Counter(row["actual_route"] for row in computed)):
        errors.append("route counts disagree with recomputation")
    if result.get("fixture_sha256") != hashlib.sha256(FIXTURE.read_bytes()).hexdigest():
        errors.append("fixture digest disagrees with tracked bytes")
    if result.get("lean_bridge", {}).get("theorems") != EXPECTED_THEOREMS:
        errors.append("Lean bridge theorem list drifted")
    for theorem in EXPECTED_THEOREMS:
        if not re.search(rf"^theorem\s+{re.escape(theorem)}\b", data["lean"], re.M):
            errors.append(f"Lean theorem absent: {theorem}")
    if fixture.get("support_state_effect") != "none" or result.get("support_state_effect") != "none":
        errors.append("fixture or result invents support-state movement")
    if len(fixture.get("non_claims", [])) < 5 or len(result.get("non_claims", [])) < 5:
        errors.append("non-claim boundary was erased")
    return errors


def negative_controls(base: dict) -> list[str]:
    mutations: list[tuple[str, dict]] = []
    for label, mutator in [
        ("missing case", lambda d: d["fixture"].__setitem__("cases", d["fixture"]["cases"][:-1])),
        ("wrong route", lambda d: d["fixture"]["cases"][1].__setitem__("expected_route", "admit_bounded_load")),
        ("stale-token laundering", lambda d: d["fixture"]["cases"][3]["record"].__setitem__("attestation_current", True)),
        ("load-observation laundering", lambda d: d["result"]["case_results"][5].__setitem__("actual_route", "admit_bounded_load")),
        ("release-authority laundering", lambda d: d["result"]["case_results"][6].__setitem__("actual_route", "record_irreversible_release")),
        ("support promotion", lambda d: d["result"].__setitem__("support_state_effect", "prototype-backed")),
        ("digest mismatch", lambda d: d["result"].__setitem__("fixture_sha256", "0" * 64)),
        ("theorem erasure", lambda d: d["result"]["lean_bridge"].__setitem__("theorems", d["result"]["lean_bridge"]["theorems"][:-1])),
        ("non-claim erasure", lambda d: d["result"].__setitem__("non_claims", [])),
    ]:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        mutations.append((label, mutated))
    return [f"negative control was accepted: {label}" for label, mutated in mutations if not semantic_errors(mutated)]


def main() -> None:
    required = [FIXTURE, RESULT, FIXTURE_SCHEMA, RESULT_SCHEMA, LEAN]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing custody lifecycle artifacts: " + ", ".join(missing))
    compile_result = subprocess.run(["lake", "env", "lean", str(LEAN.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True, check=False)
    if compile_result.returncode:
        raise SystemExit("Model-weight custody Lean compile failed:\n" + compile_result.stdout + compile_result.stderr)
    data = {"fixture": load_json(FIXTURE), "result": load_json(RESULT), "lean": LEAN.read_text(encoding="utf-8")}
    errors = validate_against_schema(data["fixture"], load_json(FIXTURE_SCHEMA), FIXTURE.relative_to(ROOT).as_posix())
    errors.extend(validate_against_schema(data["result"], load_json(RESULT_SCHEMA), RESULT.relative_to(ROOT).as_posix()))
    errors.extend(semantic_errors(data))
    errors.extend(negative_controls(data))
    names = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", data["lean"], re.M))
    surface = names & LIFECYCLE_THEOREMS
    if surface != LIFECYCLE_THEOREMS:
        errors.append(f"custody lifecycle theorem surface drifted: missing={sorted(LIFECYCLE_THEOREMS-surface)}, extra={sorted(surface-LIFECYCLE_THEOREMS)}")
    if errors:
        raise SystemExit("Model-weight custody lifecycle validation failed:\n - " + "\n - ".join(errors))
    theorem_names = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", data["lean"], re.M))
    if theorem_names != set(EXPECTED_THEOREMS) | LIFECYCLE_THEOREMS:
        raise SystemExit("Model-weight custody exact theorem surface drifted")
    event_count, control_count, terminal_kind_count, permutation_count = lifecycle_cases()
    print(f"Model-weight custody lifecycle passed: 8 deterministic routes, 44 exact Lean theorems, 9 retained route theorems, 35 transaction-lifecycle theorems, {event_count} accepted events, {control_count} rejecting lifecycle controls, {terminal_kind_count} erased-state event kinds, {permutation_count} descendant-key inventory permutations, no support movement, and 9 fixture mutations.")


if __name__ == "__main__":
    main()
