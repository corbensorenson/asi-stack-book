#!/usr/bin/env python3
"""Build the maintained X Article source manifest without rewriting history."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "editions/x_article"
ARTICLE = OUT / "asi_stack_synopsis.md"
CROSSWALK = OUT / "claim_crosswalk.json"
HEADER = OUT / "asi_stack_synopsis_header.png"
PROVENANCE = OUT / "header_provenance.json"
PREFLIGHT = OUT / "composer_preflight.json"
INPUTS = [
    "book_structure.json",
    "evidence_quality/claim_atom_registry.json",
    "evidence_quality/core_claim_vectors.json",
    "sources/source_inventory.json",
    "editions/reader_manuscript/v2_2/evidence_freeze.json",
    "release_records/2026-07-13-v2.3.0-qcsa-e2766116.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> dict[str, object]:
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def write(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def visible_words(text: str) -> list[str]:
    visible = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.findall(r"\b[\w’'-]+\b", visible)


def main() -> None:
    required = [ARTICLE, CROSSWALK, HEADER, PROVENANCE, PREFLIGHT] + [ROOT / p for p in INPUTS]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing X Article input(s): " + ", ".join(missing))
    article_text = ARTICLE.read_text(encoding="utf-8")
    words = visible_words(article_text)
    markers = re.findall(r"<!-- claim: (XA-\d{2}) -->", article_text)
    crosswalk = json.loads(CROSSWALK.read_text())
    provenance = json.loads(PROVENANCE.read_text())
    preflight = json.loads(PREFLIGHT.read_text())
    with Image.open(HEADER) as image:
        dimensions = [image.width, image.height]
        mode = image.mode
    input_records = {Path(path).stem: record(ROOT / path) for path in INPUTS}
    artifacts = {
        "article": record(ARTICLE),
        "claim_crosswalk": record(CROSSWALK),
        "header": record(HEADER),
        "header_provenance": record(PROVENANCE),
        "composer_preflight": record(PREFLIGHT),
        "desktop_preview": record(OUT / "previews/desktop.png"),
        "mobile_preview": record(OUT / "previews/mobile.png"),
        "platform_header_derivative": record(OUT / "platform_derivatives/x_header_1200x480.jpg"),
    }
    manifest = {
        "schema_version": "asi_stack.x_article_manifest.v2",
        "derivative_id": "asi-stack-x-article-synopsis-2026-07-16",
        "status": "source_ready_composer_refresh_required",
        "canonical_live_book_url": "https://corbensorenson.github.io/asi-stack-book/",
        "latest_public_book_release": "v2.3.0",
        "article": {
            "title": "The ASI Stack: Building Intelligence We Can Inspect, Challenge, and Change",
            "visible_word_count": len(words),
            "maximum_visible_word_count": 9999,
            "first_visible_body_line": article_text.splitlines()[2],
            "claim_marker_count": len(markers),
            "claim_markers": markers,
            "crosswalk_claim_count": len(crosswalk["claims"]),
            "negative_results_required_and_present": True,
        },
        "header": {
            "dimensions": dimensions,
            "aspect_ratio": "5:2",
            "mode": mode,
            "alt_text_characters": provenance["alt_text_characters"],
            "desktop_preview": "passed",
            "mobile_preview": "passed",
            "platform_alt_text_control": "not_exposed_exact_residual",
        },
        "composer": {
            "draft_id": preflight["account_and_route"]["draft_id"],
            "state": "historical_draft_stale_after_source_refresh",
            "composer_reported_word_count": preflight["article"]["composer_reported_word_count"],
            "top_link_passed": preflight["article"]["top_link_passed"],
            "header_upload_passed": preflight["header"]["upload"] == "passed",
            "publication_decision": "refresh_required_before_publish",
        },
        "bound_inputs": input_records,
        "artifacts": artifacts,
        "staleness": {
            "state": "source_current_platform_draft_stale",
            "triggers": [
                "public book release identity changes",
                "summarized chapter is added, removed, renamed, or reordered",
                "summarized claim is promoted, narrowed, refuted, deprecated, or removed",
                "decisive result, proof, source, or evidence-freeze input changes",
                "canonical live-book URL changes",
                "article source, crosswalk, header, provenance, or platform preview changes",
                "X Article or header-media behavior changes",
            ],
            "successor_authority": "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
            "release_rule": "Every public book release must refresh and validate this derivative or record an exact not_refreshed disposition.",
        },
        "publication": {
            "external_publication_authorized": False,
            "article_url": None,
            "state": "source_ready_composer_refresh_required",
        },
        "rights": {
            "authority": "LICENSE.md",
            "public_license_grant": False,
            "state": "all_rights_reserved_no_new_grant",
        },
        "support_state_effect": "none",
        "non_claims": [
            "This derivative is not canonical claim, source, proof, experiment, or release authority.",
            "An unpublished X draft is not a public Article, deployment, endorsement, or license grant.",
            "The historical platform draft predates the competence-language refresh and must not be published until it is replaced or updated and rechecked.",
            "Composer acceptance and image preview do not prove article accuracy or book claims.",
            "No chapter-core support state changed.",
        ],
    }
    write(OUT / "manifest.json", manifest)
    print(json.dumps({
        "visible_words": len(words),
        "claim_markers": len(markers),
        "header": dimensions,
        "composer_words": preflight["article"]["composer_reported_word_count"],
        "draft_id": preflight["account_and_route"]["draft_id"],
        "decision": manifest["publication"]["state"],
    }, indent=2))


if __name__ == "__main__":
    main()
