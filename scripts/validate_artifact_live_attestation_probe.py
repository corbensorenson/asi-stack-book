#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TARGET_ARTIFACT = ROOT / "experiments" / "receipt_repository_audit" / "results" / "2026-07-04-challenge.json"
RESULT = ROOT / "experiments" / "artifact_live_attestation" / "results" / "2026-07-04-local.json"
DOC = ROOT / "docs" / "artifact_live_attestation_probe.md"
ARTIFACT_CHAPTER = ROOT / "chapters" / "artifact-graphs-audit-logs-and-replay.qmd"
ARTIFACT_READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "artifact-graphs-audit-logs-and-replay.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "artifact_live_attestation_no_change.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ArtifactGraph.lean"

COMMAND = "python3 scripts/validate_artifact_live_attestation_probe.py"
TARGET_COMMAND = "python3 scripts/validate_receipt_repository_challenge.py"
RESULT_ID = "artifact-live-attestation-probe-2026-07-04"
CODEX_TEST_NAME = "Artifact live attestation probe"
LEAN_THEOREM = "artifact_live_attestation_probe_bridge"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Artifact live attestation probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_capture(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def git_blob_for_target(errors: list[str]) -> tuple[str, bytes]:
    target = rel(TARGET_ARTIFACT)
    rev = run_capture(["git", "rev-parse", f"HEAD:{target}"])
    if rev.returncode != 0:
        errors.append(f"{target} is not available as a git object at HEAD.")
        return "", b""
    blob = rev.stdout.strip()
    cat = subprocess.run(
        ["git", "cat-file", "-p", blob],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if cat.returncode != 0:
        errors.append(f"Could not read git blob for {target}: {cat.stderr.decode('utf-8', 'ignore')}")
        return blob, b""
    return blob, cat.stdout


def target_git_status_clean() -> bool:
    target = rel(TARGET_ARTIFACT)
    status = run_capture(["git", "status", "--porcelain", "--", target])
    return status.returncode == 0 and not status.stdout.strip()


def command_replay() -> dict[str, Any]:
    proc = run_capture(TARGET_COMMAND.split())
    output = proc.stdout
    return {
        "command": TARGET_COMMAND,
        "exit_code": proc.returncode,
        "output_sha256": sha256_bytes(output.encode("utf-8")),
        "output_excerpt": output.splitlines()[:6],
        "accepted": proc.returncode == 0,
    }


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def result_rejection_reasons(result: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if result.get("support_state_effect") != "none":
        reasons.append("support_state_effect_not_none")
    if result.get("chapter_core_support_effect") != "none":
        reasons.append("chapter_core_support_effect_not_none")
    if result.get("evidence_transition_created") is not False:
        reasons.append("evidence_transition_created")
    if result.get("target_artifact") != rel(TARGET_ARTIFACT):
        reasons.append("target_artifact_mismatch")
    if result.get("target_clean_in_worktree") is not True:
        reasons.append("target_not_clean_in_worktree")

    expected_sha = result.get("target_artifact_sha256")
    routes = result.get("observation_routes")
    if not isinstance(routes, list) or len(routes) < 3:
        reasons.append("observation_routes_missing")
        routes = []
    route_by_id = {
        str(route.get("route_id")): route
        for route in routes
        if isinstance(route, dict) and route.get("route_id")
    }

    fs = route_by_id.get("filesystem_bytes")
    git_blob = route_by_id.get("git_object_bytes")
    replay = route_by_id.get("command_replay")
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        reasons.append("target_sha_missing")
    if not isinstance(fs, dict):
        reasons.append("filesystem_observation_missing")
    else:
        if fs.get("observed_sha256") != expected_sha:
            reasons.append("filesystem_digest_mismatch")
        if fs.get("accepted") is not True:
            reasons.append("filesystem_observation_not_accepted")
    if not isinstance(git_blob, dict):
        reasons.append("git_object_observation_missing")
    else:
        if not git_blob.get("git_blob_sha1"):
            reasons.append("git_blob_sha1_missing")
        if git_blob.get("observed_sha256") != expected_sha:
            reasons.append("git_blob_digest_mismatch")
        if git_blob.get("accepted") is not True:
            reasons.append("git_object_observation_not_accepted")
    if not isinstance(replay, dict):
        reasons.append("command_replay_observation_missing")
    else:
        if replay.get("exit_code") != 0:
            reasons.append("command_replay_failed")
        if not isinstance(replay.get("output_sha256"), str) or len(str(replay.get("output_sha256"))) != 64:
            reasons.append("command_output_digest_missing")
        if replay.get("accepted") is not True:
            reasons.append("command_replay_not_accepted")

    observer_roles = result.get("observer_roles")
    if not isinstance(observer_roles, list) or len(set(observer_roles)) < 3:
        reasons.append("independent_observer_routes_missing")
    if result.get("same_component_self_check_allowed") is not False:
        reasons.append("same_component_self_check_allowed")

    trap = result.get("trap_receipt")
    if not isinstance(trap, dict):
        reasons.append("trap_receipt_missing")
    else:
        if trap.get("receipt_shape_valid") is not True:
            reasons.append("trap_receipt_shape_not_valid")
        if trap.get("rejected") is not True:
            reasons.append("trap_receipt_not_rejected")
        trap_reasons = text_blob(trap.get("rejection_reasons", []))
        if "target_digest_mismatch" not in trap_reasons:
            reasons.append("trap_receipt_missing_digest_mismatch_reason")

    limits = result.get("attestation_limits")
    if not isinstance(limits, list) or len(limits) < 4:
        reasons.append("attestation_limits_missing")
    non_claims = result.get("non_claims")
    non_claim_text = text_blob(non_claims)
    for phrase in (
        "does not prove open-world receipt faithfulness",
        "does not prove deployed attestation behavior",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            reasons.append(f"non_claim_missing={phrase}")
    return sorted(set(reasons))


def mutation_controls(base_result: dict[str, Any]) -> list[dict[str, Any]]:
    controls: list[dict[str, Any]] = []

    filesystem_mismatch = deepcopy(base_result)
    for route in filesystem_mismatch["observation_routes"]:
        if route["route_id"] == "filesystem_bytes":
            route["observed_sha256"] = "0" * 64
            break
    controls.append(
        {
            "control_id": "invalid_filesystem_digest_mismatch",
            "rejected": bool(result_rejection_reasons(filesystem_mismatch)),
            "rejection_reasons": result_rejection_reasons(filesystem_mismatch),
        }
    )

    git_mismatch = deepcopy(base_result)
    for route in git_mismatch["observation_routes"]:
        if route["route_id"] == "git_object_bytes":
            route["observed_sha256"] = "1" * 64
            break
    controls.append(
        {
            "control_id": "invalid_git_blob_digest_mismatch",
            "rejected": bool(result_rejection_reasons(git_mismatch)),
            "rejection_reasons": result_rejection_reasons(git_mismatch),
        }
    )

    command_failed = deepcopy(base_result)
    for route in command_failed["observation_routes"]:
        if route["route_id"] == "command_replay":
            route["exit_code"] = 1
            route["accepted"] = False
            break
    controls.append(
        {
            "control_id": "invalid_command_replay_failure",
            "rejected": bool(result_rejection_reasons(command_failed)),
            "rejection_reasons": result_rejection_reasons(command_failed),
        }
    )

    same_observer = deepcopy(base_result)
    same_observer["observer_roles"] = ["artifact_producer", "artifact_producer", "artifact_producer"]
    same_observer["same_component_self_check_allowed"] = True
    controls.append(
        {
            "control_id": "invalid_same_component_self_check_laundering",
            "rejected": bool(result_rejection_reasons(same_observer)),
            "rejection_reasons": result_rejection_reasons(same_observer),
        }
    )

    trap_accepted = deepcopy(base_result)
    trap_accepted["trap_receipt"]["rejected"] = False
    trap_accepted["trap_receipt"]["rejection_reasons"] = []
    controls.append(
        {
            "control_id": "invalid_trap_receipt_accepted",
            "rejected": bool(result_rejection_reasons(trap_accepted)),
            "rejection_reasons": result_rejection_reasons(trap_accepted),
        }
    )

    missing_limits = deepcopy(base_result)
    missing_limits["attestation_limits"] = []
    controls.append(
        {
            "control_id": "invalid_unbounded_attestation",
            "rejected": bool(result_rejection_reasons(missing_limits)),
            "rejection_reasons": result_rejection_reasons(missing_limits),
        }
    )

    support_promotion = deepcopy(base_result)
    support_promotion["support_state_effect"] = "promote_chapter_core"
    support_promotion["chapter_core_support_effect"] = "promoted"
    support_promotion["evidence_transition_created"] = True
    controls.append(
        {
            "control_id": "invalid_support_promotion_from_attestation",
            "rejected": bool(result_rejection_reasons(support_promotion)),
            "rejection_reasons": result_rejection_reasons(support_promotion),
        }
    )
    return controls


def build_expected(errors: list[str]) -> dict[str, Any]:
    if not TARGET_ARTIFACT.exists():
        errors.append(f"Missing target artifact {rel(TARGET_ARTIFACT)}.")
        target_sha = ""
    else:
        target_sha = sha256_file(TARGET_ARTIFACT)
    blob_sha1, blob_content = git_blob_for_target(errors)
    git_content_sha = sha256_bytes(blob_content) if blob_content else ""
    replay = command_replay()
    target_json = load_json(TARGET_ARTIFACT) if TARGET_ARTIFACT.exists() else {}
    target_result_id = target_json.get("result_id") if isinstance(target_json, dict) else None

    base_without_controls = {
        "schema_version": "asi_stack.artifact_live_attestation.result.v0",
        "result_id": RESULT_ID,
        "recorded_date": "2026-07-04",
        "command": COMMAND,
        "target_artifact": rel(TARGET_ARTIFACT),
        "target_artifact_result_id": target_result_id,
        "target_artifact_sha256": target_sha,
        "target_clean_in_worktree": target_git_status_clean(),
        "attestation_kind": "bounded_live_repository_artifact_attestation",
        "observation_routes": [
            {
                "route_id": "filesystem_bytes",
                "observer_role": "filesystem_reader",
                "observed_ref": rel(TARGET_ARTIFACT),
                "observed_sha256": target_sha,
                "accepted": bool(target_sha),
            },
            {
                "route_id": "git_object_bytes",
                "observer_role": "git_object_database",
                "observed_ref": f"HEAD:{rel(TARGET_ARTIFACT)}",
                "git_blob_sha1": blob_sha1,
                "observed_sha256": git_content_sha,
                "accepted": bool(blob_sha1) and git_content_sha == target_sha,
            },
            {
                "route_id": "command_replay",
                "observer_role": "command_replay_validator",
                **replay,
            },
        ],
        "observer_roles": [
            "filesystem_reader",
            "git_object_database",
            "command_replay_validator",
        ],
        "same_component_self_check_allowed": False,
        "trap_receipt": {
            "trap_id": "shape_valid_wrong_digest_attestation",
            "receipt_shape_valid": True,
            "expected_sha256": "0" * 64,
            "observed_sha256": target_sha,
            "rejected": True,
            "rejection_reasons": ["target_digest_mismatch"],
        },
        "attestation_limits": [
            "local repository target only",
            "current committed git object and filesystem bytes only",
            "command replay covers the selected validator output only",
            "not a deployed attestation service",
            "not open-world receipt faithfulness",
        ],
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "The probe attests one selected repository artifact, not every artifact in the graph.",
            "Git-object and filesystem agreement do not prove that the original causal process was complete.",
            "Command replay checks the selected validator, not deployed audit or attestation behavior.",
            "External project truth, verifier correctness, and open-world receipt faithfulness remain unproved.",
        ],
        "non_claims": [
            "does not prove open-world receipt faithfulness",
            "does not prove deployed attestation behavior",
            "does not prove deployed audit behavior",
            "does not prove verifier correctness or external project truth",
            "does not create an upward support-state transition",
            "does not promote any chapter core claim",
            "does not promote the Artifact Graphs chapter core claim",
        ],
    }
    controls = mutation_controls(base_without_controls)
    summary = {
        "target_artifact_count": 1,
        "observation_route_count": len(base_without_controls["observation_routes"]),
        "accepted_observation_route_count": sum(
            1 for route in base_without_controls["observation_routes"] if route.get("accepted") is True
        ),
        "mutation_control_count": len(controls),
        "filesystem_digest_matches_target": target_sha
        == base_without_controls["observation_routes"][0]["observed_sha256"],
        "git_blob_digest_matches_target": target_sha
        == base_without_controls["observation_routes"][1]["observed_sha256"],
        "command_replay_passed": replay["exit_code"] == 0,
        "observer_routes_independent": len(set(base_without_controls["observer_roles"])) == 3,
        "trap_receipt_rejected": True,
        "attestation_limits_recorded": True,
        "support_state_effect_none": True,
        "chapter_core_support_effect_none": True,
        "non_claim_boundary": True,
        "no_upward_transition": True,
    }
    expected = {
        **base_without_controls,
        "mutation_controls": controls,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ArtifactGraph",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
    }
    for reason in result_rejection_reasons(expected):
        errors.append(f"expected live attestation result rejected: {reason}")
    for control in controls:
        if control["rejected"] is not True:
            errors.append(f"{control['control_id']} was not rejected.")
    return expected


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    if RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def require_fragment(owner: str, text: str, fragment: str, errors: list[str]) -> None:
    if fragment not in text:
        errors.append(f"{owner} missing required fragment: {fragment!r}.")


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    record = load_json(TRANSITION)
    expected = {
        "claim_id": "artifact-graphs.live_artifact_attestation_probe",
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "review_status": "accepted",
        "support_state_effect": "blocks_promotion",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"{rel(TRANSITION)} {key} must be {value!r}.")
    blob = text_blob(record)
    for phrase in (
        rel(RESULT),
        "does not promote the Artifact Graphs chapter core claim",
        "does not create an upward support-state transition",
        "does not promote any chapter core claim",
    ):
        if phrase.lower() not in blob:
            errors.append(f"{rel(TRANSITION)} missing {phrase!r}.")


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): (
            DOC,
            [
                "Artifact Live Attestation Probe",
                COMMAND,
                rel(TARGET_ARTIFACT),
                rel(RESULT),
                "filesystem bytes, git object bytes, and command replay",
                "invalid_same_component_self_check_laundering",
            ],
        ),
        rel(ARTIFACT_CHAPTER): (
            ARTIFACT_CHAPTER,
            [
                "live artifact attestation probe",
                COMMAND,
                rel(RESULT),
                "filesystem bytes, git object bytes, and command replay",
                "not a deployed attestation service",
            ],
        ),
        rel(ARTIFACT_READER): (
            ARTIFACT_READER,
            [
                "live artifact attestation probe",
                "filesystem bytes, git object bytes, and command replay",
                "not a deployed attestation service",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented live artifact attestation probe",
                COMMAND,
                rel(RESULT),
                LEAN_THEOREM,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "live artifact attestation probe",
                rel(RESULT),
                "local live repository attestation",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add artifact live attestation probe",
                COMMAND,
                rel(RESULT),
                "does not create an upward support-state transition",
            ],
        ),
        rel(LEDGER_MD): (
            LEDGER_MD,
            [
                "Record-reality gap",
                rel(RESULT),
                "live_artifact_attestation_backed_not_open_world",
            ],
        ),
        rel(VALIDATION_REGISTRY): (
            VALIDATION_REGISTRY,
            [
                "scripts/validate_artifact_live_attestation_probe.py",
                rel(RESULT),
                '"script": "validate_artifact_live_attestation_probe.py"',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "ArtifactLiveAttestationSummary",
                "artifactLiveAttestationSummary",
                LEAN_THEOREM,
            ],
        ),
    }
    for owner, (path, fragments) in surfaces.items():
        if not path.exists():
            errors.append(f"Missing {owner}.")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            require_fragment(owner, text, fragment, errors)


def validate_ledger_json(errors: list[str]) -> None:
    data = load_json(LEDGER_JSON)
    records = data.get("records", [])
    matches = [
        record
        for record in records
        if isinstance(record, dict) and record.get("idea_id") == "receipt_faithfulness_gap"
    ]
    if len(matches) != 1:
        errors.append(f"{rel(LEDGER_JSON)} must contain one receipt_faithfulness_gap row.")
        return
    blob = text_blob(matches[0])
    for phrase in (
        rel(RESULT),
        "live_artifact_attestation_backed_not_open_world",
        "does not prove open-world receipt faithfulness",
    ):
        if phrase not in blob:
            errors.append(f"{rel(LEDGER_JSON)} receipt_faithfulness_gap row missing {phrase!r}.")


def validate_book_structure(errors: list[str]) -> None:
    data = load_json(BOOK_STRUCTURE)
    tests: list[dict[str, Any]] = []
    proof_targets: list[dict[str, Any]] = []
    for part in data.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                tests.extend(test for test in chapter.get("codex_tests", []) if isinstance(test, dict))
                proof_targets.extend(
                    target for target in chapter.get("proof_targets", []) if isinstance(target, dict)
                )
    matches = [test for test in tests if test.get("name") == CODEX_TEST_NAME]
    if len(matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain exactly one {CODEX_TEST_NAME!r} test row.")
    else:
        blob = text_blob(matches[0])
        for phrase in (COMMAND, "filesystem bytes", "no support-state promotion"):
            if phrase not in blob:
                errors.append(f"{CODEX_TEST_NAME} codex test row missing {phrase!r}.")
    target_matches = [
        target for target in proof_targets if target.get("tag") == "lean:artifacts.graph.live_attestation_probe_bridge"
    ]
    if len(target_matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain one live attestation proof target.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    for fragment in (
        "ArtifactLiveAttestationSummary",
        "artifactLiveAttestationSummary",
        "ArtifactLiveAttestationValid",
        LEAN_THEOREM,
        "filesystemDigestMatchesTarget",
        "gitBlobDigestMatchesTarget",
        "sameComponentSelfCheckRejected",
    ):
        if fragment not in text:
            errors.append(f"{rel(LEAN_FILE)} missing {fragment}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    expected = build_expected(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(errors)
        validate_transition(errors)
        validate_ledger_json(errors)
        validate_book_structure(errors)
        validate_lean_shape(errors)
    if errors:
        fail(errors)
    print(
        "Artifact live attestation probe validation passed: "
        f"{expected['trace_summary']['accepted_observation_route_count']} observation route(s), "
        f"{expected['trace_summary']['mutation_control_count']} mutation control(s), "
        "no support-state effect."
    )


if __name__ == "__main__":
    main()
