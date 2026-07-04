#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "experiments" / "authority_revocation_trace" / "input" / "artifact_manifest.json"
RESULT = ROOT / "experiments" / "authority_revocation_trace" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "authority_revocation_trace.md"
AUTHORITY_RESULT = ROOT / "experiments" / "authority_transitions" / "results" / "2026-06-28-local.md"
AUTHORITY_DENY = ROOT / "experiments" / "authority_transitions" / "fixtures" / "valid_deny_over_ceiling.json"
RUNTIME_PERMS_RESULT = ROOT / "experiments" / "runtime_adapter_permissions" / "results" / "2026-07-01-local.md"
RUNTIME_REVOKED = ROOT / "experiments" / "runtime_adapter_permissions" / "fixtures" / "invalid_revoked_authority_receipt.json"
RUNTIME_EXPIRED = ROOT / "experiments" / "runtime_adapter_permissions" / "fixtures" / "invalid_expired_approval.json"
RUNTIME_EFFECT = ROOT / "experiments" / "runtime_adapter_effect_probe" / "results" / "2026-07-02-local.json"
SECURITY_RESULT = ROOT / "experiments" / "security_kernel" / "results" / "2026-07-01-local.md"
SCIF_COMMIT = ROOT / "experiments" / "security_scif_commit_probe" / "results" / "2026-07-02-local.json"
REFERENCE_BLOCKED = ROOT / "experiments" / "reference_trace" / "fixtures" / "valid_blocked_authority_trace.json"
CHAPTER = ROOT / "chapters" / "system-boundaries-and-authority.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "system-boundaries-and-authority.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "Authority.lean"
STATUS = ROOT / "docs" / "test_harness_status_ledger.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"

COMMAND = "python3 scripts/validate_authority_revocation_trace.py"
CODEX_TEST_NAME = "Authority revocation propagation trace"
LEAN_THEOREM = "authority_revocation_trace_surface_bridge"
EXPECTED_SOURCE_REFS = {
    "experiments/authority_transitions/results/2026-06-28-local.md",
    "experiments/authority_transitions/fixtures/valid_deny_over_ceiling.json",
    "experiments/runtime_adapter_permissions/results/2026-07-01-local.md",
    "experiments/runtime_adapter_permissions/fixtures/invalid_revoked_authority_receipt.json",
    "experiments/runtime_adapter_permissions/fixtures/invalid_expired_approval.json",
    "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json",
    "experiments/security_kernel/results/2026-07-01-local.md",
    "experiments/security_scif_commit_probe/results/2026-07-02-local.json",
    "experiments/reference_trace/fixtures/valid_blocked_authority_trace.json",
}
REQUIRED_NON_CLAIMS = [
    "does not prove deployed authorization enforcement",
    "does not prove deployed revocation propagation",
    "does not prove tool-wrapper security",
    "does not promote any chapter core claim",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Authority revocation trace validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def require_fragment(owner: str, text: str, fragment: str, errors: list[str]) -> None:
    if fragment not in text and " ".join(fragment.split()) not in " ".join(text.split()):
        errors.append(f"{owner} missing required fragment: {fragment!r}.")


def validate_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("schema_version") != "asi_stack.authority_revocation_trace.manifest.v0":
        errors.append(f"{rel(MANIFEST)} has unexpected schema_version.")
    refs = manifest.get("source_artifact_refs")
    if set(refs or []) != EXPECTED_SOURCE_REFS:
        errors.append(f"{rel(MANIFEST)} source_artifact_refs do not match expected artifact set.")
    boundary_blob = text_blob(manifest.get("required_boundaries", []))
    for phrase in (
        "no deployed authorization enforcement claim",
        "no deployed revocation propagation claim",
        "no tool-wrapper security claim",
        "no support-state promotion",
        "no model-quality, benchmark, or safety claim",
    ):
        if phrase not in boundary_blob:
            errors.append(f"{rel(MANIFEST)} missing boundary {phrase!r}.")


def find_control(rows: list[dict[str, Any]], scenario_id: str) -> dict[str, Any] | None:
    for row in rows:
        if isinstance(row, dict) and row.get("scenario_id") == scenario_id:
            return row
    return None


def build_result(errors: list[str]) -> dict[str, Any]:
    manifest = load_json(MANIFEST)
    validate_manifest(manifest, errors)

    authority_text = AUTHORITY_RESULT.read_text(encoding="utf-8")
    runtime_text = RUNTIME_PERMS_RESULT.read_text(encoding="utf-8")
    security_text = SECURITY_RESULT.read_text(encoding="utf-8")
    authority_deny = load_json(AUTHORITY_DENY)
    runtime_revoked = load_json(RUNTIME_REVOKED)
    runtime_expired = load_json(RUNTIME_EXPIRED)
    runtime_effect = load_json(RUNTIME_EFFECT)
    scif_commit = load_json(SCIF_COMMIT)
    reference_blocked = load_json(REFERENCE_BLOCKED)

    for fragment in (
        "Authority transition harness passed: 3 valid fixture(s), 3 expected-invalid fixture(s).",
        "does not prove deployed authorization enforcement",
        "revocation propagation",
    ):
        require_fragment(rel(AUTHORITY_RESULT), authority_text, fragment, errors)
    for fragment in (
        "invalid_revoked_authority_receipt.json",
        "prove revocation propagation in a deployed runtime",
        "Runtime adapter permission harness passed: 2 valid fixture(s), 7 expected-invalid fixture(s).",
    ):
        require_fragment(rel(RUNTIME_PERMS_RESULT), runtime_text, fragment, errors)
    for fragment in (
        "invalid_expired_approval.json",
        "runtime approval expiry enforcement",
    ):
        require_fragment(rel(SECURITY_RESULT), security_text, fragment, errors)

    if authority_deny.get("decision") != "deny":
        errors.append(f"{rel(AUTHORITY_DENY)} must be a denial record.")
    if authority_deny.get("effect_receipt") != "":
        errors.append(f"{rel(AUTHORITY_DENY)} denial must not carry an effect receipt.")
    if not authority_deny.get("denial_reason"):
        errors.append(f"{rel(AUTHORITY_DENY)} must carry a denial reason.")

    probe = runtime_revoked.get("authority_probe", {})
    if probe.get("probe_type") != "revocation_propagation":
        errors.append(f"{rel(RUNTIME_REVOKED)} must carry revocation_propagation probe_type.")
    if probe.get("receipt_revocation_state") != "revoked":
        errors.append(f"{rel(RUNTIME_REVOKED)} must mark receipt_revocation_state revoked.")
    if probe.get("expected_decision") != "deny":
        errors.append(f"{rel(RUNTIME_REVOKED)} must expect denial.")
    if runtime_revoked.get("runtime_adapter_invocation", {}).get("support_state_effect") != "blocks_promotion":
        errors.append(f"{rel(RUNTIME_REVOKED)} must block promotion.")
    if "revoked://" not in text_blob(runtime_revoked.get("authority_use_receipt", {})):
        errors.append(f"{rel(RUNTIME_REVOKED)} must expose the revoked authority path.")

    if not str(runtime_expired.get("runtime_adapter_invocation", {}).get("approval_expiry", "")).startswith("expired"):
        errors.append(f"{rel(RUNTIME_EXPIRED)} must carry an expired approval marker.")

    expired_effect = find_control(
        runtime_effect.get("expected_invalid_controls", []),
        "invalid_expired_approval_no_mutation",
    )
    if expired_effect is None:
        errors.append(f"{rel(RUNTIME_EFFECT)} missing invalid_expired_approval_no_mutation.")
        expired_effect = {}
    if expired_effect.get("decision") != "deny":
        errors.append(f"{rel(RUNTIME_EFFECT)} expired approval control must deny.")
    checks = expired_effect.get("checks", {})
    if checks.get("blocked_before_mutation") is not True or checks.get("state_unchanged") is not True:
        errors.append(f"{rel(RUNTIME_EFFECT)} expired approval control must preserve no-mutation evidence.")

    scif_inactive = find_control(
        scif_commit.get("expected_invalid_controls", []),
        "invalid_unapproved_destination_commit_blocked",
    )
    if scif_inactive is None:
        errors.append(f"{rel(SCIF_COMMIT)} missing invalid_unapproved_destination_commit_blocked.")
        scif_inactive = {}
    if scif_inactive.get("actual_route") != "block_commit":
        errors.append(f"{rel(SCIF_COMMIT)} inactive approval control must block commit.")
    if scif_inactive.get("outcome", {}).get("job_dispatched") is not False:
        errors.append(f"{rel(SCIF_COMMIT)} inactive approval control must not dispatch a job.")
    if scif_inactive.get("outcome", {}).get("support_state_effect") != "none":
        errors.append(f"{rel(SCIF_COMMIT)} inactive approval control must preserve support_state_effect none.")

    trace = reference_blocked.get("reference_trace_record", {})
    if "missing execution authority" not in trace.get("stop_conditions", []):
        errors.append(f"{rel(REFERENCE_BLOCKED)} must preserve missing execution authority stop condition.")
    if "authority stop condition active" not in trace.get("promotion_blockers", []):
        errors.append(f"{rel(REFERENCE_BLOCKED)} must preserve authority promotion blocker.")
    if trace.get("support_state_effect") != "blocks_promotion":
        errors.append(f"{rel(REFERENCE_BLOCKED)} must block promotion.")

    trace_entries = [
        {
            "entry_id": "authority-transition-denial",
            "artifact_ref": rel(AUTHORITY_DENY),
            "blocked_state": "deny",
            "propagation_surface": "over-ceiling request preserves denial reason, audit refs, and no effect receipt",
            "support_state_effect": "none",
        },
        {
            "entry_id": "runtime-adapter-revoked-receipt",
            "artifact_ref": rel(RUNTIME_REVOKED),
            "blocked_state": "expected_invalid_revoked_receipt",
            "propagation_surface": "revoked authority receipt is expected to deny and block promotion",
            "support_state_effect": "blocks_promotion",
        },
        {
            "entry_id": "runtime-adapter-expired-no-mutation",
            "artifact_ref": rel(RUNTIME_EFFECT),
            "blocked_state": "deny_before_mutation",
            "propagation_surface": "expired approval is denied with unchanged pre/post state hashes",
            "support_state_effect": "none",
        },
        {
            "entry_id": "security-scif-inactive-approval-block",
            "artifact_ref": rel(SCIF_COMMIT),
            "blocked_state": "block_commit",
            "propagation_surface": "inactive approval or unapproved destination blocks commit and dispatch",
            "support_state_effect": "none",
        },
        {
            "entry_id": "reference-trace-blocked-authority",
            "artifact_ref": rel(REFERENCE_BLOCKED),
            "blocked_state": "blocked_path",
            "propagation_surface": "reference trace preserves missing execution authority stop condition and promotion blocker",
            "support_state_effect": "blocks_promotion",
        },
    ]

    summary = {
        "authorityDenialVisible": authority_deny.get("decision") == "deny",
        "revokedReceiptBlocked": probe.get("receipt_revocation_state") == "revoked"
        and probe.get("expected_decision") == "deny",
        "expiredApprovalNoMutation": checks.get("blocked_before_mutation") is True
        and checks.get("state_unchanged") is True,
        "scifInactiveApprovalBlocksCommit": scif_inactive.get("actual_route") == "block_commit"
        and scif_inactive.get("outcome", {}).get("job_dispatched") is False,
        "referenceTraceAuthorityBlockerPreserved": "authority stop condition active"
        in trace.get("promotion_blockers", []),
        "supportStateEffectNone": True,
        "nonClaimBoundary": True,
        "deployedRevocationPropagationNotClaimed": True,
    }

    return {
        "schema_version": "asi_stack.authority_revocation_trace.result.v0",
        "result_id": "2026-07-03-authority-revocation-trace",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "manifest_ref": rel(MANIFEST),
        "result_kind": "cross_artifact_authority_revocation_trace",
        "source_artifact_hashes": {
            rel(path): sha256_file(path)
            for path in [
                AUTHORITY_RESULT,
                AUTHORITY_DENY,
                RUNTIME_PERMS_RESULT,
                RUNTIME_REVOKED,
                RUNTIME_EXPIRED,
                RUNTIME_EFFECT,
                SECURITY_RESULT,
                SCIF_COMMIT,
                REFERENCE_BLOCKED,
            ]
        },
        "trace_entry_count": len(trace_entries),
        "trace_entries": trace_entries,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.Authority",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "This trace reads already committed authority and runtime artifacts; it does not execute a deployed authorization service.",
            "The trace checks that revoked, expired, missing, or inactive authority remains visible as denial, no-mutation, blocked-commit, or blocked-path evidence across repository artifacts.",
            "Live revocation propagation, approval-service quality, adapter enforcement, sandbox isolation, and tool-wrapper security remain unproved.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS
        + [
            "does not prove approval-service quality, sandbox isolation, or secret-handle safety",
            "does not prove model quality, benchmark performance, safety, or ASI",
            "does not create an evidence transition",
        ],
    }


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


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): (
            DOC,
            [
                "Authority Revocation Propagation Trace",
                COMMAND,
                rel(RESULT),
                "runtime-adapter-revoked-receipt",
                "runtime-adapter-expired-no-mutation",
                "security-scif-inactive-approval-block",
                "does not prove deployed revocation propagation",
            ],
        ),
        rel(CHAPTER): (
            CHAPTER,
            [
                "Authority revocation propagation trace",
                COMMAND,
                rel(RESULT),
                "revoked authority receipt",
                "expired approval",
                "SCIF inactive approval",
                "does not prove deployed revocation propagation",
            ],
        ),
        rel(READER): (
            READER,
            [
                "authority revocation trace",
                "not proof of a deployed revocation service",
                "revoked or expired authority",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented authority revocation propagation trace",
                COMMAND,
                rel(RESULT),
                LEAN_THEOREM,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "authority revocation propagation trace",
                rel(RESULT),
                "revoked authority receipt",
                "expired approval",
                "does not prove deployed revocation propagation",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add authority revocation propagation trace",
                COMMAND,
                rel(RESULT),
                "does not create a support-state transition",
            ],
        ),
        rel(STATUS): (
            STATUS,
            [
                "Authority revocation propagation trace",
                rel(RESULT),
            ],
        ),
        rel(PUBLICATION): (
            PUBLICATION,
            [
                "Authority revocation propagation trace",
                rel(RESULT),
            ],
        ),
        rel(VALIDATE_BOOK): (
            VALIDATE_BOOK,
            [
                "scripts/validate_authority_revocation_trace.py",
                "docs/authority_revocation_trace.md",
                rel(RESULT),
                'run_validator("validate_authority_revocation_trace.py")',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "AuthorityRevocationTraceSummary",
                "authorityRevocationTraceSummary",
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


def validate_book_structure(errors: list[str]) -> None:
    data = load_json(BOOK_STRUCTURE)
    tests: list[dict[str, Any]] = []
    proof_targets: list[dict[str, Any]] = []
    for part in data.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == "system-boundaries-and-authority":
                tests.extend(test for test in chapter.get("codex_tests", []) if isinstance(test, dict))
                proof_targets.extend(
                    target for target in chapter.get("proof_targets", []) if isinstance(target, dict)
                )
    matches = [test for test in tests if test.get("name") == CODEX_TEST_NAME]
    if len(matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain exactly one {CODEX_TEST_NAME!r} test row.")
    else:
        blob = text_blob(matches[0])
        for phrase in (COMMAND, "revoked authority receipt", "expired approval", "no deployed revocation propagation"):
            if phrase not in blob:
                errors.append(f"{CODEX_TEST_NAME} codex test row missing {phrase!r}.")
    target_matches = [
        target for target in proof_targets if target.get("tag") == "lean:authority.revocation.trace_surface_bridge"
    ]
    if len(target_matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain exactly one authority revocation proof target.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    if not re.search(rf"theorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "authorityDenialVisible",
        "revokedReceiptBlocked",
        "expiredApprovalNoMutation",
        "scifInactiveApprovalBlocksCommit",
        "referenceTraceAuthorityBlockerPreserved",
        "supportStateEffectNone",
        "nonClaimBoundary",
        "deployedRevocationPropagationNotClaimed",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing authority revocation field {field}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    required = [
        MANIFEST,
        AUTHORITY_RESULT,
        AUTHORITY_DENY,
        RUNTIME_PERMS_RESULT,
        RUNTIME_REVOKED,
        RUNTIME_EXPIRED,
        RUNTIME_EFFECT,
        SECURITY_RESULT,
        SCIF_COMMIT,
        REFERENCE_BLOCKED,
    ]
    errors = [f"Missing required artifact {rel(path)}." for path in required if not path.exists()]
    if errors:
        fail(errors)

    expected = build_result(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(errors)
        validate_book_structure(errors)
        validate_lean_shape(errors)

    if errors:
        fail(errors)
    print(
        "Authority revocation trace validation passed: "
        f"{expected['trace_entry_count']} artifact trace entries, "
        "revoked/expired authority blockers visible, no support-state effect."
    )


if __name__ == "__main__":
    main()
