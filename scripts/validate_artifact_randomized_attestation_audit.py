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
RESULT = ROOT / "experiments" / "artifact_randomized_attestation" / "results" / "2026-07-04-local.json"
DOC = ROOT / "docs" / "artifact_randomized_attestation_audit.md"
CHAPTER = ROOT / "chapters" / "artifact-graphs-audit-logs-and-replay.qmd"
READER = (
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
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "artifact_randomized_attestation_no_change.json"
BOOK_STRUCTURE = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
TEST_LEDGER_SCRIPT = ROOT / "scripts" / "validate_test_harness_status_ledger.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ArtifactGraph.lean"

COMMAND = "python3 scripts/validate_artifact_randomized_attestation_audit.py"
RESULT_ID = "artifact-randomized-attestation-audit-2026-07-04"
SELECTION_SEED = "asi-stack.record-reality.randomized-live-audit.2026-07-04"
SELECTION_ALGORITHM = "sha256(seed + ':' + artifact_path), ascending, first four candidates"
SELECTED_COUNT = 4
CODEX_TEST_NAME = "Artifact randomized attestation audit"
PROOF_TAG = "lean:artifacts.graph.randomized_attestation_audit_bridge"
LEAN_THEOREM = "artifact_randomized_attestation_audit_bridge"

CANDIDATE_ARTIFACTS = [
    {
        "artifact": "experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json",
        "validator": "python3 scripts/validate_artifact_graph_record_reality_sequence.py",
    },
    {
        "artifact": "experiments/receipt_faithfulness/results/2026-07-03-local.json",
        "validator": "python3 scripts/validate_receipt_faithfulness.py",
    },
    {
        "artifact": "experiments/receipt_repository_audit/results/2026-07-03-local.json",
        "validator": "python3 scripts/validate_receipt_repository_audit.py",
    },
    {
        "artifact": "experiments/receipt_repository_audit/results/2026-07-04-challenge.json",
        "validator": "python3 scripts/validate_receipt_repository_challenge.py",
    },
    {
        "artifact": "experiments/artifact_live_attestation/results/2026-07-04-local.json",
        "validator": "python3 scripts/validate_artifact_live_attestation_probe.py",
    },
    {
        "artifact": "experiments/epistemic_tcb/results/2026-07-03-local.json",
        "validator": "python3 scripts/validate_epistemic_trusted_computing_base.py",
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Artifact randomized attestation audit validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_capture(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command.split(),
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def git_blob(path: str, errors: list[str]) -> tuple[str, str]:
    rev = run_capture(f"git rev-parse HEAD:{path}")
    if rev.returncode != 0:
        errors.append(f"{path} is not available as a git object at HEAD.")
        return "", ""
    blob_sha1 = rev.stdout.strip()
    cat = subprocess.run(
        ["git", "cat-file", "-p", blob_sha1],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if cat.returncode != 0:
        errors.append(f"Could not read git blob for {path}: {cat.stderr.decode('utf-8', 'ignore')}")
        return blob_sha1, ""
    return blob_sha1, sha256_bytes(cat.stdout)


def artifact_clean(path: str) -> bool:
    status = run_capture(f"git status --porcelain -- {path}")
    return status.returncode == 0 and not status.stdout.strip()


def selected_candidates() -> list[dict[str, str]]:
    scored: list[tuple[str, dict[str, str]]] = []
    for candidate in CANDIDATE_ARTIFACTS:
        artifact = candidate["artifact"]
        score = hashlib.sha256(f"{SELECTION_SEED}:{artifact}".encode("utf-8")).hexdigest()
        scored.append((score, {**candidate, "selection_score": score}))
    return [candidate for _, candidate in sorted(scored, key=lambda item: item[0])[:SELECTED_COUNT]]


def command_observation(command: str) -> dict[str, Any]:
    proc = run_capture(command)
    output = proc.stdout
    return {
        "route_id": "command_replay",
        "observer_role": "command_replay_validator",
        "command": command,
        "exit_code": proc.returncode,
        "output_sha256": sha256_bytes(output.encode("utf-8")),
        "output_excerpt": output.splitlines()[:6],
        "accepted": proc.returncode == 0,
    }


def artifact_observation(candidate: dict[str, str], rank: int, errors: list[str]) -> dict[str, Any]:
    artifact = candidate["artifact"]
    path = ROOT / artifact
    if not path.exists():
        errors.append(f"Missing candidate artifact {artifact}.")
        artifact_sha = ""
        result_id = None
    else:
        artifact_sha = sha256_file(path)
        try:
            loaded = load_json(path)
        except json.JSONDecodeError:
            loaded = {}
        result_id = loaded.get("result_id") if isinstance(loaded, dict) else None
    blob_sha1, git_sha = git_blob(artifact, errors)
    command_route = command_observation(candidate["validator"])
    return {
        "artifact": artifact,
        "artifact_result_id": result_id,
        "validator": candidate["validator"],
        "selection_rank": rank,
        "selection_score": candidate["selection_score"],
        "artifact_sha256": artifact_sha,
        "clean_in_worktree": artifact_clean(artifact),
        "observation_routes": [
            {
                "route_id": "filesystem_bytes",
                "observer_role": "filesystem_reader",
                "observed_ref": artifact,
                "observed_sha256": artifact_sha,
                "accepted": bool(artifact_sha),
            },
            {
                "route_id": "git_object_bytes",
                "observer_role": "git_object_database",
                "observed_ref": f"HEAD:{artifact}",
                "git_blob_sha1": blob_sha1,
                "observed_sha256": git_sha,
                "accepted": bool(blob_sha1) and git_sha == artifact_sha,
            },
            command_route,
        ],
        "trap_receipt": {
            "trap_id": f"shape_valid_wrong_digest_attestation_{rank}",
            "receipt_shape_valid": True,
            "expected_sha256": "0" * 64,
            "observed_sha256": artifact_sha,
            "rejected": True,
            "rejection_reasons": ["target_digest_mismatch"],
        },
    }


def result_rejection_reasons(result: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if result.get("support_state_effect") != "none":
        reasons.append("support_state_effect_not_none")
    if result.get("chapter_core_support_effect") != "none":
        reasons.append("chapter_core_support_effect_not_none")
    if result.get("evidence_transition_created") is not False:
        reasons.append("evidence_transition_created")
    if result.get("selection_seed") != SELECTION_SEED:
        reasons.append("selection_seed_missing_or_mismatch")
    if result.get("selection_algorithm") != SELECTION_ALGORITHM:
        reasons.append("selection_algorithm_missing_or_mismatch")

    candidate_pool = result.get("candidate_artifact_pool")
    selected = result.get("selected_artifacts")
    if not isinstance(candidate_pool, list) or len(candidate_pool) != len(CANDIDATE_ARTIFACTS):
        reasons.append("candidate_pool_missing_or_wrong_size")
    expected_paths = [candidate["artifact"] for candidate in selected_candidates()]
    if not isinstance(selected, list):
        reasons.append("selected_artifacts_missing")
        selected = []
    elif [artifact.get("artifact") for artifact in selected] != expected_paths:
        reasons.append("selected_artifacts_do_not_match_seeded_order")
    if len(selected) < 2:
        reasons.append("randomized_audit_not_beyond_one_artifact")
    if len(selected) != SELECTED_COUNT:
        reasons.append("selected_artifact_count_mismatch")

    accepted_routes = 0
    for artifact in selected:
        if not isinstance(artifact, dict):
            reasons.append("selected_artifact_not_object")
            continue
        artifact_path = artifact.get("artifact")
        artifact_sha = artifact.get("artifact_sha256")
        if artifact_path not in expected_paths:
            reasons.append("unexpected_selected_artifact")
        if artifact.get("clean_in_worktree") is not True:
            reasons.append(f"{artifact_path}:target_not_clean_in_worktree")
        routes = artifact.get("observation_routes")
        if not isinstance(routes, list) or len(routes) != 3:
            reasons.append(f"{artifact_path}:observation_routes_missing")
            continue
        by_id = {route.get("route_id"): route for route in routes if isinstance(route, dict)}
        fs = by_id.get("filesystem_bytes")
        git = by_id.get("git_object_bytes")
        replay = by_id.get("command_replay")
        if not isinstance(fs, dict) or fs.get("observed_sha256") != artifact_sha or fs.get("accepted") is not True:
            reasons.append(f"{artifact_path}:filesystem_digest_mismatch")
        else:
            accepted_routes += 1
        if (
            not isinstance(git, dict)
            or git.get("observed_sha256") != artifact_sha
            or git.get("accepted") is not True
            or not git.get("git_blob_sha1")
        ):
            reasons.append(f"{artifact_path}:git_object_digest_mismatch")
        else:
            accepted_routes += 1
        if (
            not isinstance(replay, dict)
            or replay.get("exit_code") != 0
            or replay.get("accepted") is not True
            or not isinstance(replay.get("output_sha256"), str)
            or len(str(replay.get("output_sha256"))) != 64
        ):
            reasons.append(f"{artifact_path}:command_replay_failed")
        else:
            accepted_routes += 1
        trap = artifact.get("trap_receipt")
        trap_text = text_blob(trap)
        if not isinstance(trap, dict) or trap.get("rejected") is not True or "target_digest_mismatch" not in trap_text:
            reasons.append(f"{artifact_path}:trap_receipt_not_rejected")

    observer_roles = result.get("observer_roles")
    if not isinstance(observer_roles, list) or len(set(observer_roles)) < 3:
        reasons.append("independent_observer_routes_missing")
    if result.get("same_component_self_check_allowed") is not False:
        reasons.append("same_component_self_check_allowed")
    if not isinstance(result.get("attestation_limits"), list) or len(result.get("attestation_limits", [])) < 5:
        reasons.append("attestation_limits_missing")
    non_claim_text = text_blob(result.get("non_claims"))
    for phrase in (
        "does not prove open-world receipt faithfulness",
        "does not prove deployed attestation behavior",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            reasons.append(f"non_claim_missing={phrase}")
    summary = result.get("trace_summary")
    if isinstance(summary, dict):
        if summary.get("accepted_observation_route_count") != accepted_routes:
            reasons.append("accepted_observation_route_count_mismatch")
        if summary.get("selected_artifact_count") != SELECTED_COUNT:
            reasons.append("trace_summary_selected_count_mismatch")
    else:
        reasons.append("trace_summary_missing")
    return sorted(set(reasons))


def mutation_controls(base: dict[str, Any]) -> list[dict[str, Any]]:
    controls: list[dict[str, Any]] = []

    missing_seed = deepcopy(base)
    missing_seed["selection_seed"] = ""
    controls.append(
        {
            "control_id": "invalid_missing_selection_seed",
            "rejected": bool(result_rejection_reasons(missing_seed)),
            "rejection_reasons": result_rejection_reasons(missing_seed),
        }
    )

    digest_mismatch = deepcopy(base)
    digest_mismatch["selected_artifacts"][0]["observation_routes"][0]["observed_sha256"] = "1" * 64
    controls.append(
        {
            "control_id": "invalid_filesystem_digest_mismatch_in_sample",
            "rejected": bool(result_rejection_reasons(digest_mismatch)),
            "rejection_reasons": result_rejection_reasons(digest_mismatch),
        }
    )

    git_mismatch = deepcopy(base)
    git_mismatch["selected_artifacts"][0]["observation_routes"][1]["observed_sha256"] = "2" * 64
    controls.append(
        {
            "control_id": "invalid_git_object_digest_mismatch_in_sample",
            "rejected": bool(result_rejection_reasons(git_mismatch)),
            "rejection_reasons": result_rejection_reasons(git_mismatch),
        }
    )

    failed_replay = deepcopy(base)
    failed_replay["selected_artifacts"][0]["observation_routes"][2]["exit_code"] = 1
    failed_replay["selected_artifacts"][0]["observation_routes"][2]["accepted"] = False
    controls.append(
        {
            "control_id": "invalid_command_replay_failure_in_sample",
            "rejected": bool(result_rejection_reasons(failed_replay)),
            "rejection_reasons": result_rejection_reasons(failed_replay),
        }
    )

    one_artifact = deepcopy(base)
    one_artifact["selected_artifacts"] = one_artifact["selected_artifacts"][:1]
    controls.append(
        {
            "control_id": "invalid_not_beyond_one_selected_artifact",
            "rejected": bool(result_rejection_reasons(one_artifact)),
            "rejection_reasons": result_rejection_reasons(one_artifact),
        }
    )

    same_observer = deepcopy(base)
    same_observer["observer_roles"] = ["artifact_producer", "artifact_producer", "artifact_producer"]
    same_observer["same_component_self_check_allowed"] = True
    controls.append(
        {
            "control_id": "invalid_same_component_self_check_laundering",
            "rejected": bool(result_rejection_reasons(same_observer)),
            "rejection_reasons": result_rejection_reasons(same_observer),
        }
    )

    missing_limits = deepcopy(base)
    missing_limits["attestation_limits"] = []
    controls.append(
        {
            "control_id": "invalid_unbounded_randomized_attestation",
            "rejected": bool(result_rejection_reasons(missing_limits)),
            "rejection_reasons": result_rejection_reasons(missing_limits),
        }
    )

    promotion = deepcopy(base)
    promotion["support_state_effect"] = "promote_chapter_core"
    promotion["chapter_core_support_effect"] = "promoted"
    promotion["evidence_transition_created"] = True
    controls.append(
        {
            "control_id": "invalid_support_promotion_from_randomized_audit",
            "rejected": bool(result_rejection_reasons(promotion)),
            "rejection_reasons": result_rejection_reasons(promotion),
        }
    )

    return controls


def build_expected(errors: list[str]) -> dict[str, Any]:
    selected = [artifact_observation(candidate, rank, errors) for rank, candidate in enumerate(selected_candidates(), start=1)]
    candidate_pool = [
        {
            "artifact": candidate["artifact"],
            "validator": candidate["validator"],
            "selection_score": hashlib.sha256(
                f"{SELECTION_SEED}:{candidate['artifact']}".encode("utf-8")
            ).hexdigest(),
        }
        for candidate in CANDIDATE_ARTIFACTS
    ]
    base = {
        "schema_version": "asi_stack.artifact_randomized_attestation.result.v0",
        "result_id": RESULT_ID,
        "recorded_date": "2026-07-04",
        "command": COMMAND,
        "selection_seed": SELECTION_SEED,
        "selection_algorithm": SELECTION_ALGORITHM,
        "candidate_artifact_pool": sorted(candidate_pool, key=lambda candidate: candidate["artifact"]),
        "selected_artifacts": selected,
        "attestation_kind": "deterministic_randomized_live_repository_artifact_attestation",
        "observer_roles": [
            "filesystem_reader",
            "git_object_database",
            "command_replay_validator",
        ],
        "same_component_self_check_allowed": False,
        "attestation_limits": [
            "deterministic pseudo-random sample over a fixed public-safe candidate pool",
            "local repository artifacts only",
            "current committed git objects and filesystem bytes only",
            "command replay covers each selected validator output only",
            "not a deployed attestation service",
            "not open-world receipt faithfulness",
        ],
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "The audit samples four public-safe repository result artifacts, not every artifact in the graph.",
            "The deterministic seed makes the sample reproducible; it is not a cryptographic random beacon or independent external challenge.",
            "Filesystem/git/command agreement does not prove that the original causal process was complete or externally truthful.",
            "Verifier correctness, deployed attestation behavior, external project truth, and open-world receipt faithfulness remain unproved.",
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
    controls = mutation_controls(base)
    accepted_route_count = sum(
        1
        for artifact in selected
        for route in artifact["observation_routes"]
        if route.get("accepted") is True
    )
    summary = {
        "candidate_artifact_count": len(CANDIDATE_ARTIFACTS),
        "selected_artifact_count": len(selected),
        "observation_route_count": len(selected) * 3,
        "accepted_observation_route_count": accepted_route_count,
        "trap_receipt_count": len(selected),
        "trap_receipts_rejected": all(artifact["trap_receipt"]["rejected"] for artifact in selected),
        "mutation_control_count": len(controls),
        "mutation_controls_rejected": sum(1 for control in controls if control["rejected"] is True),
        "seeded_selection_reproducible": [artifact["artifact"] for artifact in selected]
        == [candidate["artifact"] for candidate in selected_candidates()],
        "sample_beyond_one_artifact": len(selected) > 1,
        "observer_routes_independent": True,
        "support_state_effect_none": True,
        "chapter_core_support_effect_none": True,
        "non_claim_boundary": True,
        "no_upward_transition": True,
    }
    expected = {
        **base,
        "mutation_controls": controls,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ArtifactGraph",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
    }
    for reason in result_rejection_reasons(expected):
        errors.append(f"expected randomized attestation result rejected: {reason}")
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


def require_fragments(owner: str, path: Path, fragments: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing {owner}.")
        return
    blob = text_blob(path.read_text(encoding="utf-8", errors="ignore"))
    for fragment in fragments:
        if fragment.lower() not in blob:
            errors.append(f"{owner} missing required fragment: {fragment!r}.")


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    record = load_json(TRANSITION)
    expected = {
        "claim_id": "artifact-graphs.randomized_artifact_attestation_audit",
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
        "deterministic pseudo-random sample",
        "does not promote any chapter core claim",
        "does not create an upward support-state transition",
    ):
        if phrase.lower() not in blob:
            errors.append(f"{rel(TRANSITION)} missing {phrase!r}.")


def validate_book_structure(errors: list[str]) -> None:
    data = load_json(BOOK_STRUCTURE)
    chapter = None
    for part in data.get("parts", []):
        for candidate in part.get("chapters", []):
            if isinstance(candidate, dict) and candidate.get("id") == "artifact-graphs-audit-logs-and-replay":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json missing Artifact Graphs chapter.")
        return
    tests_blob = text_blob(chapter.get("codex_tests", []))
    for phrase in (CODEX_TEST_NAME, COMMAND, "deterministic pseudo-random sample", "no support-state promotion"):
        if phrase.lower() not in tests_blob:
            errors.append(f"book_structure.json codex_tests missing {phrase!r}.")
    tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in tags:
        errors.append(f"book_structure.json proof_targets missing {PROOF_TAG}.")


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
        "randomized_artifact_attestation_backed_not_open_world",
        "does not prove open-world receipt faithfulness",
    ):
        if phrase.lower() not in blob:
            errors.append(f"{rel(LEDGER_JSON)} receipt_faithfulness_gap row missing {phrase!r}.")


def validate_surfaces(errors: list[str]) -> None:
    shared = [
        "randomized artifact attestation audit",
        rel(RESULT),
        COMMAND,
        "deterministic pseudo-random",
        "does not prove open-world receipt faithfulness",
    ]
    surfaces = {
        rel(DOC): (DOC, shared),
        rel(CHAPTER): (CHAPTER, shared[:3]),
        rel(READER): (
            READER,
            [
                "randomized artifact attestation audit",
                "2026-07-04 local result",
                "sample-laundering",
            ],
        ),
        rel(OUTLINE): (OUTLINE, shared[:3]),
        rel(ROADMAP): (ROADMAP, shared[:3]),
        rel(CHANGELOG): (CHANGELOG, shared[:3]),
        rel(LEDGER_MD): (LEDGER_MD, [rel(RESULT), "randomized_artifact_attestation_backed_not_open_world"]),
        rel(TEST_LEDGER_SCRIPT): (TEST_LEDGER_SCRIPT, ["Artifact randomized attestation audit", COMMAND, rel(RESULT)]),
        rel(VALIDATION_REGISTRY): (
            VALIDATION_REGISTRY,
            [
                "scripts/validate_artifact_randomized_attestation_audit.py",
                rel(RESULT),
                '"script": "validate_artifact_randomized_attestation_audit.py"',
            ],
        ),
        rel(LEAN_FILE): (LEAN_FILE, ["ArtifactRandomizedAttestationSummary", LEAN_THEOREM]),
    }
    for owner, (path, fragments) in surfaces.items():
        require_fragments(owner, path, fragments, errors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    expected = build_expected(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_transition(errors)
        validate_book_structure(errors)
        validate_ledger_json(errors)
        validate_surfaces(errors)
    if errors:
        fail(errors)
    print(
        "Artifact randomized attestation audit validation passed: "
        f"{expected['trace_summary']['selected_artifact_count']} selected artifact(s), "
        f"{expected['trace_summary']['accepted_observation_route_count']} accepted observation route(s), "
        f"{expected['trace_summary']['mutation_control_count']} mutation control(s), no support-state effect."
    )


if __name__ == "__main__":
    main()
