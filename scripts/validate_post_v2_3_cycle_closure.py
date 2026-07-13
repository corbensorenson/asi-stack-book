#!/usr/bin/env python3
"""Validate terminal post-v2.3 closure across roadmap, reader, evidence, and public truth."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = "docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md"
STATUS = "roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json"
DECLARATION = "docs/post_v2_3_quality_floor_reader_completion_declaration.md"
NO_RELEASE = "release_records/2026-07-13-post-v2-3-quality-reader-cycle-no-public-release.json"
READER = "editions/reader_manuscript/v2_0/reader_release_record.json"
CAMPAIGN = "experiments/post_v2_3_evidence_campaigns/results/adjudication.json"
CANDIDATES = "docs/post_v2_3_evidence_candidate_ledger.json"
SUCCESSOR = "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"
SUCCESSOR_STATUS = "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
ACTIVE_MARKER = "Status: active canonical successor roadmap; unfinished work only"


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="ignore")


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def snapshot() -> dict:
    return {
        "status": read_json(STATUS),
        "roadmap": read_text(ROADMAP),
        "declaration": read_text(DECLARATION),
        "no_release": read_json(NO_RELEASE),
        "reader": read_json(READER),
        "campaign": read_json(CAMPAIGN),
        "candidates": read_json(CANDIDATES),
        "successor_status": read_json(SUCCESSOR_STATUS),
        "vectors": read_json("evidence_quality/core_claim_vectors.json"),
        "public_surfaces": {
            path: read_text(path)
            for path in ["README.md", "index.qmd", "docs/publication_readiness.md", "docs/public_status_contract.md"]
        },
        "active_roadmaps": [
            str(path.relative_to(ROOT))
            for path in sorted((ROOT / "docs").glob("*roadmap*.md"))
            if ACTIVE_MARKER in path.read_text(encoding="utf-8", errors="ignore")[:1200]
        ],
    }


def errors(data: dict) -> list[str]:
    out: list[str] = []
    status = data["status"]
    if status.get("status") != "completed":
        out.append("roadmap machine state is not completed")
    if [row.get("id") for row in status.get("priorities", [])] != [f"P{i}" for i in range(6)] or any(row.get("state") != "completed" for row in status.get("priorities", [])):
        out.append("P0-P5 are not exactly completed")
    if [row.get("id") for row in status.get("milestones", [])] != [f"M{i}" for i in range(10)] or any(row.get("state") != "completed" for row in status.get("milestones", [])):
        out.append("M0-M9 are not exactly completed")
    if data["active_roadmaps"] != [SUCCESSOR]:
        out.append("the completed cycle must expose exactly its declared active successor")
    if "Status: completed 2026-07-13" not in data["roadmap"]:
        out.append("roadmap prose is not terminal")

    reader = data["reader"]
    if reader.get("decision") != "approved_exact_local_html_archive":
        out.append("54-chapter reader lacks exact local HTML approval")
    artifact = reader.get("artifact", {})
    if artifact.get("archive_sha256") != "a2caa97fb9281e1fdfc9a9dda626141d4a876df776c9cbc7408f978751736b50" or artifact.get("chapter_entry_point_count") != 54:
        out.append("reader archive identity or 54-chapter denominator drifted")
    if artifact.get("publication_state") != "tracked_local_archive_not_publicly_deployed":
        out.append("reader public-deployment boundary drifted")

    candidates = data["candidates"]
    if candidates.get("candidate_count") != 21 or candidates.get("disposition_counts") != {"promote": 5, "narrow": 8, "no_change": 6, "refute": 2} or candidates.get("accepted_transition_count") != 21:
        out.append("candidate adjudication denominator or dispositions drifted")
    campaign = data["campaign"]
    if campaign.get("status") != "completed_protocol_failure_preserved_no_change":
        out.append("campaign failure is not preserved as terminal no-change")
    protocol = campaign.get("protocol_integrity", {})
    if (protocol.get("raw_output_count"), protocol.get("parseable_structured_outputs"), protocol.get("output_cap_exhaustions"), protocol.get("unclosed_reasoning_blocks")) != (36, 0, 36, 34):
        out.append("campaign protocol-failure facts drifted")
    if [row.get("disposition") for row in campaign.get("dispositions", [])] != ["no_change", "no_change"]:
        out.append("campaign no-change dispositions drifted")

    vectors = data["vectors"].get("vectors", [])
    if len(vectors) != 54 or any(row.get("summary_support_state") != "argument" for row in vectors):
        out.append("chapter-core argument boundary drifted")

    closure = data["no_release"]
    if closure.get("decision") != "no_public_living_book_release" or closure.get("validation_status") != "pass":
        out.append("no-public-release decision is absent or invalid")
    if closure.get("latest_public_living_book_release", {}).get("version") != "v2.3.0":
        out.append("v2.3.0 is not preserved as latest public release")
    if any(closure.get("publication_effect", {}).values()):
        out.append("no-release record invents a publication effect")
    for row in closure.get("closure_artifacts", []):
        path = row.get("path", "")
        if not (ROOT / path).is_file() or row.get("sha256") != sha(path):
            out.append(f"closure artifact digest mismatch: {path}")

    successor = data["successor_status"]
    if successor.get("status") != "active" or successor.get("roadmap_path") != SUCCESSOR:
        out.append("declared successor machine state is absent or not active")

    for phrase in ["P0–P5", "M0–M9", NO_RELEASE, SUCCESSOR, SUCCESSOR_STATUS, "Successor activated: 2026-07-13", "All 54 chapter-core claims remain at `argument`"]:
        if phrase not in data["declaration"]:
            out.append(f"completion declaration missing: {phrase}")
    for path, text in data["public_surfaces"].items():
        for phrase in [ROADMAP, STATUS, SUCCESSOR, SUCCESSOR_STATUS, "v2.3.0"]:
            if phrase not in text:
                out.append(f"{path} missing terminal public truth: {phrase}")
    return out


def main() -> None:
    data = snapshot()
    failures = errors(data)
    mutations = []
    reopened = copy.deepcopy(data); reopened["status"]["status"] = "active"; mutations.append(("reopened roadmap", reopened))
    hidden_active = copy.deepcopy(data); hidden_active["active_roadmaps"] = [SUCCESSOR, "docs/fake_roadmap.md"]; mutations.append(("hidden successor", hidden_active))
    release_laundering = copy.deepcopy(data); release_laundering["no_release"]["publication_effect"]["public_deployment_performed"] = True; mutations.append(("release laundering", release_laundering))
    reasoning_laundering = copy.deepcopy(data); reasoning_laundering["campaign"]["protocol_integrity"]["parseable_structured_outputs"] = 36; mutations.append(("reasoning laundering", reasoning_laundering))
    support = copy.deepcopy(data); support["vectors"]["vectors"][0]["summary_support_state"] = "prototype-backed"; mutations.append(("support promotion", support))
    reader = copy.deepcopy(data); reader["reader"]["artifact"]["publication_state"] = "publicly_deployed"; mutations.append(("reader deployment laundering", reader))
    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Post-v2.3 cycle closure failed:\n - " + "\n - ".join(failures))
    print("Post-v2.3 cycle closure passed: P0-P5 and M0-M9 remain complete with one declared active successor, exact local 54-chapter reader, 21 candidate and 2 campaign dispositions, v2.3.0 still latest public, 54 argument cores, and 6 rejecting mutations.")


if __name__ == "__main__":
    main()
