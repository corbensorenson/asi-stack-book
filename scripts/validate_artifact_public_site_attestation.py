#!/usr/bin/env python3
"""Validate a bounded public GitHub Pages page attestation.

The write mode fetches the currently deployed Artifact Graphs chapter from the
public GitHub Pages site and records the page digest plus required fragments.
The default mode validates the tracked result and public surfaces without
performing network access, so CI remains deterministic.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "artifact_public_site_attestation" / "results" / "2026-07-05-live.json"
DOC = ROOT / "docs" / "artifact_public_site_attestation.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "artifact_public_site_attestation_no_change.json"
CHAPTER = ROOT / "chapters" / "artifact-graphs-audit-logs-and-replay.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "artifact-graphs-audit-logs-and-replay.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"
NON_CORE = ROOT / "docs" / "non_core_evidence_ledger.md"

COMMAND = "python3 scripts/validate_artifact_public_site_attestation.py"
RESULT_ID = "artifact-public-site-record-reality-attestation-2026-07-05"
CLAIM_ID = "artifact-graphs.public_site_record_reality_attestation"
PUBLIC_URL = "https://corbensorenson.github.io/asi-stack-book/chapters/artifact-graphs-audit-logs-and-replay.html"

REQUIRED_FRAGMENTS = [
    {
        "fragment_id": "chapter_title",
        "text": "Artifact Graphs, Audit Logs, and Replay",
    },
    {
        "fragment_id": "record_reality_ladder",
        "text": "Record-reality should be read as an authority ladder",
    },
    {
        "fragment_id": "epistemic_tcb_boundary",
        "text": "The epistemic trusted computing base is the companion problem",
    },
    {
        "fragment_id": "github_pages_ci_attestation",
        "text": "GitHub Pages CI attestation adds one externally hosted service route",
    },
    {
        "fragment_id": "live_attestation_probe",
        "text": "Artifact live attestation probe",
    },
    {
        "fragment_id": "randomized_attestation_audit",
        "text": "randomized artifact attestation audit",
    },
    {
        "fragment_id": "no_deployed_attestation",
        "text": "not a deployed attestation service",
    },
    {
        "fragment_id": "no_independent_human_review",
        "text": "not independent external human review",
    },
    {
        "fragment_id": "no_reader_release",
        "text": "not reader release approval",
    },
    {
        "fragment_id": "no_chapter_core_support",
        "text": "not Artifact Graphs chapter-core support",
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Artifact public-site attestation validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_page() -> dict[str, Any]:
    request = Request(PUBLIC_URL, headers={"User-Agent": "asi-stack-book-public-site-attestation/0.1"})
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read()
            headers = {key.lower(): value for key, value in response.headers.items()}
            status = int(getattr(response, "status", 0) or 0)
            final_url = response.geturl()
    except HTTPError as exc:
        body = exc.read()
        headers = {key.lower(): value for key, value in exc.headers.items()}
        status = int(exc.code)
        final_url = exc.url
    except URLError as exc:
        fail([f"Could not fetch {PUBLIC_URL}: {exc}"])

    text = body.decode("utf-8", errors="ignore")
    fragment_checks = []
    for fragment in REQUIRED_FRAGMENTS:
        needle = fragment["text"]
        position = text.lower().find(needle.lower())
        fragment_checks.append(
            {
                "fragment_id": fragment["fragment_id"],
                "fragment": needle,
                "present": position >= 0,
                "position": position,
            }
        )

    return {
        "schema_version": "0.1",
        "result_id": RESULT_ID,
        "claim_id": CLAIM_ID,
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "fetch_url": PUBLIC_URL,
        "final_url": final_url,
        "http_status": status,
        "content_type": headers.get("content-type", ""),
        "etag": headers.get("etag", ""),
        "last_modified": headers.get("last-modified", ""),
        "content_length_bytes": len(body),
        "content_sha256": sha256_bytes(body),
        "required_fragments": fragment_checks,
        "observation_routes": [
            {
                "route_id": "public_github_pages_url_fetch",
                "observer_role": "public_http_client",
                "accepted": status == 200,
            },
            {
                "route_id": "record_reality_fragment_set",
                "observer_role": "html_content_probe",
                "accepted": all(row["present"] for row in fragment_checks),
            },
            {
                "route_id": "boundary_fragment_set",
                "observer_role": "html_boundary_probe",
                "accepted": all(
                    row["present"]
                    for row in fragment_checks
                    if row["fragment_id"].startswith("no_")
                ),
            },
        ],
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "attestation_limits": [
            "Public GitHub Pages fetch attests served HTML content for one URL at fetch time only.",
            "The public page is an externally reachable publication surface, not an independent human reviewer.",
            "Served page content does not prove deployed attestation behavior, verifier correctness, open-world receipt faithfulness, model quality, safety, or ASI capability.",
            "The fetch does not approve any reader artifact or future commit.",
        ],
        "non_claims": [
            "does not create an upward support-state transition",
            "does not promote any chapter core claim",
            "does not promote the Artifact Graphs chapter core claim",
            "does not prove open-world receipt faithfulness",
            "does not prove deployed attestation behavior",
            "does not create independent external human review",
            "does not approve any reader release artifact",
        ],
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema_version": "0.1",
        "result_id": RESULT_ID,
        "claim_id": CLAIM_ID,
        "fetch_url": PUBLIC_URL,
        "http_status": 200,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            errors.append(f"{rel(RESULT)} {key} must be {value!r}; found {result.get(key)!r}.")
    if not str(result.get("final_url", "")).startswith("https://corbensorenson.github.io/asi-stack-book/"):
        errors.append(f"{rel(RESULT)} final_url must point to the public book site.")
    if not isinstance(result.get("content_length_bytes"), int) or result.get("content_length_bytes", 0) < 100000:
        errors.append(f"{rel(RESULT)} content_length_bytes is too small for the deployed chapter page.")
    if not isinstance(result.get("content_sha256"), str) or len(result.get("content_sha256", "")) != 64:
        errors.append(f"{rel(RESULT)} content_sha256 must be a SHA-256 hex digest.")
    fragments = result.get("required_fragments")
    if not isinstance(fragments, list) or len(fragments) != len(REQUIRED_FRAGMENTS):
        errors.append(f"{rel(RESULT)} required_fragments must list {len(REQUIRED_FRAGMENTS)} checks.")
        fragments = []
    fragment_by_id = {str(row.get("fragment_id")): row for row in fragments if isinstance(row, dict)}
    for expected_fragment in REQUIRED_FRAGMENTS:
        row = fragment_by_id.get(expected_fragment["fragment_id"])
        if not isinstance(row, dict):
            errors.append(f"{rel(RESULT)} missing fragment check {expected_fragment['fragment_id']!r}.")
            continue
        if row.get("fragment") != expected_fragment["text"]:
            errors.append(f"{rel(RESULT)} fragment text drifted for {expected_fragment['fragment_id']!r}.")
        if row.get("present") is not True:
            errors.append(f"{rel(RESULT)} fragment {expected_fragment['fragment_id']!r} is not present.")
        if not isinstance(row.get("position"), int) or row.get("position", -1) < 0:
            errors.append(f"{rel(RESULT)} fragment {expected_fragment['fragment_id']!r} needs a nonnegative position.")
    routes = result.get("observation_routes")
    if not isinstance(routes, list) or len(routes) < 3:
        errors.append(f"{rel(RESULT)} observation_routes must contain at least three routes.")
        routes = []
    if any(not isinstance(route, dict) or route.get("accepted") is not True for route in routes):
        errors.append(f"{rel(RESULT)} every observation route must be accepted.")
    limits = " ".join(str(item).lower() for item in result.get("attestation_limits", []))
    for phrase in ("public github pages", "not an independent human reviewer", "does not approve any reader artifact"):
        if phrase not in limits:
            errors.append(f"{rel(RESULT)} attestation_limits missing phrase: {phrase}")
    non_claims = " ".join(str(item).lower() for item in result.get("non_claims", []))
    for phrase in (
        "does not create an upward support-state transition",
        "does not promote any chapter core claim",
        "does not prove open-world receipt faithfulness",
        "does not prove deployed attestation behavior",
        "does not create independent external human review",
        "does not approve any reader release artifact",
    ):
        if phrase not in non_claims:
            errors.append(f"{rel(RESULT)} non_claims missing phrase: {phrase}")
    return errors


def validate_surfaces(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_refs = [
        (DOC, RESULT_ID),
        (DOC, rel(RESULT)),
        (DOC, rel(TRANSITION)),
        (DOC, PUBLIC_URL),
        (DOC, "not independent external human review"),
        (CHAPTER, "public deployed-site attestation"),
        (CHAPTER, rel(RESULT)),
        (READER, "public deployed-site attestation"),
        (READER, rel(RESULT)),
        (OUTLINE, "public deployed-site attestation"),
        (ROADMAP, "public deployed-site attestation"),
        (CHANGELOG, "public deployed-site attestation"),
        (LEDGER_MD, "public_site_record_reality_attestation_backed_not_external_review"),
        (LEDGER_JSON, "public_site_record_reality_attestation_backed_not_external_review"),
        (NON_CORE, CLAIM_ID),
        (TRANSITION, RESULT_ID),
    ]
    for path, fragment in expected_refs:
        if not path.exists():
            errors.append(f"missing required surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if fragment not in text:
            errors.append(f"{rel(path)} missing required fragment: {fragment}")
    if (
        DOC.exists()
        and str(result.get("content_sha256"))
        and str(result.get("content_sha256")) not in DOC.read_text(encoding="utf-8", errors="ignore")
    ):
        errors.append(f"{rel(DOC)} must name captured content digest {result.get('content_sha256')}.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Fetch the public page and write the tracked result.")
    args = parser.parse_args()

    if args.write_result:
        result = fetch_page()
        errors = validate_result(result)
        if errors:
            fail(errors)
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        if not RESULT.exists():
            fail([f"{rel(RESULT)} is missing; run {COMMAND} --write-result."])
        result = load_json(RESULT)
        if not isinstance(result, dict):
            fail([f"{rel(RESULT)} must contain a JSON object."])

    errors = validate_result(result)
    errors.extend(validate_surfaces(result))
    if errors:
        fail(errors)
    print(
        "Artifact public-site attestation validation passed: "
        f"{result['content_length_bytes']} bytes from {result['fetch_url']}."
    )


if __name__ == "__main__":
    main()
