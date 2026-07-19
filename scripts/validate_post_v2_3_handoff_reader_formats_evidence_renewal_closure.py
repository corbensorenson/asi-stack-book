#!/usr/bin/env python3
"""Validate terminal P4 closure and absence of a silent successor."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"
STATUS = "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
STATUS_SCHEMA = "schemas/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.schema.json"
DECLARATION = "docs/post_v2_3_handoff_reader_formats_evidence_renewal_completion_declaration.md"
TERMINAL_RECORD = "release_records/2026-07-14-post-v2-3-handoff-reader-formats-evidence-renewal-no-public-release.json"
ACTIVE_MARKER = "Status: **active canonical successor**"
ACTIVE_SUCCESSOR = "docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md"
ACTIVE_SUCCESSOR_STATUS = "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
ACTIVE_CURRENT = "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
ACTIVE_CURRENT_STATUS = "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
PUBLIC_SURFACES = ["README.md", "index.qmd", "docs/publication_readiness.md", "docs/public_status_contract.md"]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="ignore")


def snapshot() -> dict:
    return {
        "status": load(STATUS),
        "status_schema": load(STATUS_SCHEMA),
        "active_successor_status": load(ACTIVE_SUCCESSOR_STATUS),
        "active_current_status": load(ACTIVE_CURRENT_STATUS),
        "roadmap": text(ROADMAP),
        "declaration": text(DECLARATION),
        "terminal": load(TERMINAL_RECORD),
        "structure": load("book_structure.json"),
        "vectors": load("evidence_quality/core_claim_vectors.json"),
        "epub": load("editions/reader_manuscript/v2_0/epub_disposition.json"),
        "pdf": load("editions/reader_manuscript/v2_0/pdf_disposition.json"),
        "docx": load("editions/reader_manuscript/v2_0/docx_disposition.json"),
        "reader_html": load("editions/reader_manuscript/v2_0/reader_release_record.json"),
        "reader_v21": load("editions/reader_manuscript/v2_1/manifest.json"),
        "flagship": load("experiments/post_v2_3_evidence_protocol_renewal/flagship/results/adjudication.json"),
        "theseus": load("experiments/theseus_pretraining_readiness_currentness_import/results/2026-07-14-local.json"),
        "public": {path: text(path) for path in PUBLIC_SURFACES},
        "active_roadmaps": [
            path.relative_to(ROOT).as_posix()
            for path in sorted((ROOT / "docs").glob("*roadmap*.md"))
            if ACTIVE_MARKER in path.read_text(encoding="utf-8", errors="ignore")[:1200]
        ],
    }


def errors(data: dict) -> list[str]:
    out: list[str] = []
    status = data["status"]
    try:
        jsonschema.validate(status, data["status_schema"])
    except jsonschema.ValidationError as exc:
        out.append(f"status schema: {exc.message}")
    if status.get("status") != "completed":
        out.append("roadmap machine status is not completed")
    if [row.get("id") for row in status.get("priorities", [])] != [f"P{i}" for i in range(5)] or any(row.get("state") != "completed" for row in status.get("priorities", [])):
        out.append("P0-P4 are not exactly completed")
    if [row.get("id") for row in status.get("milestones", [])] != [f"M{i}" for i in range(9)] or any(row.get("state") != "completed" for row in status.get("milestones", [])):
        out.append("M0-M8 are not exactly completed")
    completion = status.get("completion", {})
    if completion.get("terminal_record") != TERMINAL_RECORD or completion.get("completion_declaration") != DECLARATION or completion.get("active_successor") is not None:
        out.append("terminal bindings or null successor authority drifted")
    if data["active_roadmaps"] != [ACTIVE_CURRENT]:
        out.append("terminal history must coexist with the exact current evidence-competence successor")
    if "Status: completed 2026-07-14; no active successor" not in data["roadmap"]:
        out.append("roadmap prose is not terminal")
    active_successor = data["active_successor_status"]
    if active_successor.get("status") != "completed" or active_successor.get("roadmap_path") != ACTIVE_SUCCESSOR:
        out.append("claim-proof/SOTA successor is not preserved as completed history")
    if active_successor.get("predecessor", {}).get("path") != ROADMAP:
        out.append("claim-proof/SOTA successor does not bind this completed predecessor")
    active_current = data["active_current_status"]
    if active_current.get("status") != "active" or active_current.get("roadmap_path") != ACTIVE_CURRENT:
        out.append("current evidence-competence successor machine authority is absent")
    current_truth = active_current.get("activation_truth", {})
    live_chapter_count = current_truth.get("live_working_chapter_count")
    live_argument_count = current_truth.get("chapter_core_argument_count")

    terminal = data["terminal"]
    if terminal.get("decision") != "exact_local_reader_multiformat_disposition_no_public_release" or terminal.get("validation_status") != "pass":
        out.append("terminal no-public-release decision is absent")
    if terminal.get("substantive_source_commit") != "f93a4d8fa51ac7cafa0db180d7360ee1fb2c498c":
        out.append("substantive tested source commit drifted")
    if terminal.get("latest_public_living_book_release", {}).get("version") != "v2.3.0" or not terminal.get("latest_public_living_book_release", {}).get("unchanged"):
        out.append("latest immutable public release is not preserved")
    if any(terminal.get("publication_effect", {}).values()):
        out.append("terminal transaction invents a public release effect")

    if data["reader_html"].get("decision") != "approved_exact_local_html_archive":
        out.append("canonical reader HTML approval drifted")
    if data["docx"].get("decision") != "approved_exact_local_artifact":
        out.append("DOCX exact local approval drifted")
    if data["epub"].get("decision") != "blocked" or data["pdf"].get("decision") != "blocked":
        out.append("EPUB/PDF blockers were erased or laundered")
    if data["reader_v21"].get("status") != "reconciled_source_only" or data["reader_v21"].get("release_state") != "not_released_source_only":
        out.append("v2.1 source-only reader state is not bounded")

    manifest_ids = [
        chapter.get("id")
        for part in data["structure"].get("parts", [])
        for chapter in part.get("chapters", [])
    ]
    vectors = data["vectors"].get("vectors", [])
    if (
        not isinstance(live_chapter_count, int)
        or live_chapter_count < 55
        or live_argument_count != live_chapter_count
        or len(manifest_ids) != live_chapter_count
        or len(vectors) != live_chapter_count
        or [row.get("chapter_id") for row in vectors] != manifest_ids
        or any(row.get("summary_support_state") != "argument" for row in vectors)
    ):
        out.append("current manifest, vector identity, live count, or argument-only boundary drifted")
    if active_successor.get("activation_baseline", {}).get("core_claim_count") != 54:
        out.append("frozen 54-core historical activation boundary drifted")
    expansion = active_successor.get("structural_expansion_contract", {})
    if (
        expansion.get("live_chapter_count") != 55
        or expansion.get("chapter_id")
        != "replaceable-cognitive-substrates-beyond-transformer-monoculture"
    ):
        out.append("authorized historical 55th-chapter expansion boundary drifted")
    flagship = data["flagship"]
    outcomes = flagship.get("outcomes", {})
    baseline = outcomes.get("baseline", {})
    governed = outcomes.get("governed", {})
    quality = outcomes.get("task_quality", {})
    if (baseline.get("runs"), governed.get("runs"), quality.get("independently_correct"), baseline.get("useful_releases"), governed.get("useful_releases"), baseline.get("unsafe_releases"), governed.get("unsafe_releases")) != (32, 32, 2, 0, 0, 0, 0):
        out.append("flagship denominator or no-release facts drifted")
    if flagship.get("disposition") != "no_change" or "blocks promotion" not in flagship.get("frozen_metadata_erratum", {}).get("effect", ""):
        out.append("flagship no-change promotion blocker drifted")
    theseus = data["theseus"]
    if theseus.get("sanitized_summary", {}).get("trigger_state") != "YELLOW" or theseus.get("support_state_effect") != "none":
        out.append("Theseus YELLOW/no-support boundary drifted")

    declaration_normalized = " ".join(data["declaration"].split()).casefold()
    for phrase in ["P0–P4", "M0–M8", TERMINAL_RECORD, "no successor roadmap is active", "All 54 chapter-core claims remain at `argument`"]:
        if " ".join(phrase.split()).casefold() not in declaration_normalized:
            out.append(f"completion declaration missing: {phrase}")
    for path, body in data["public"].items():
        body_normalized = " ".join(body.split())
        for phrase in [ACTIVE_SUCCESSOR, ACTIVE_SUCCESSOR_STATUS, ACTIVE_CURRENT, ACTIVE_CURRENT_STATUS, "v2.3.0"]:
            if phrase.casefold() not in body_normalized.casefold():
                out.append(f"{path} missing terminal public truth: {phrase}")
        live_claim_phrase = (
            f"All {live_chapter_count} live chapter-core claims remain at `argument`"
            if path == "docs/publication_readiness.md"
            else f"{live_argument_count}/{live_chapter_count} chapter-core claims at `argument`"
        )
        if live_claim_phrase not in body and live_claim_phrase not in body_normalized:
            out.append(f"{path} missing current live-claim truth: {live_claim_phrase}")
        if "No successor roadmap is active" in body:
            out.append(f"{path} retains obsolete no-successor language")
        if "active canonical successor roadmap: fake" in body.casefold():
            out.append(f"{path} contains a contradictory active-roadmap pointer")
    return out


def main() -> None:
    base = snapshot()
    failures = errors(base)
    mutations: list[tuple[str, dict]] = []
    reopened = copy.deepcopy(base); reopened["status"]["status"] = "active"; mutations.append(("reopened roadmap", reopened))
    hidden = copy.deepcopy(base); hidden["active_roadmaps"] = [ACTIVE_CURRENT, "docs/fake_roadmap.md"]; mutations.append(("hidden successor", hidden))
    release = copy.deepcopy(base); release["terminal"]["publication_effect"]["source_tag_created"] = True; mutations.append(("release laundering", release))
    epub = copy.deepcopy(base); epub["epub"]["decision"] = "approved"; mutations.append(("EPUB laundering", epub))
    support = copy.deepcopy(base); support["vectors"]["vectors"][0]["summary_support_state"] = "prototype-backed"; mutations.append(("support promotion", support))
    useful = copy.deepcopy(base); useful["flagship"]["outcomes"]["governed"]["useful_releases"] = 2; mutations.append(("useful denominator laundering", useful))
    theseus = copy.deepcopy(base); theseus["theseus"]["sanitized_summary"]["trigger_state"] = "GREEN"; mutations.append(("Theseus readiness laundering", theseus))
    stale = copy.deepcopy(base); stale["public"]["README.md"] += "\nActive canonical successor roadmap: fake\n"; mutations.append(("stale public pointer", stale))
    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Post-v2.3 handoff/reader/evidence closure failed:\n - " + "\n - ".join(failures))
    print(
        "Post-v2.3 handoff/reader/evidence closure passed: P0-P4, M0-M8, "
        "historical HTML+DOCX local approval and EPUB/PDF blockers, frozen 54-core activation and authorized 55th chapter preserved, "
        f"current {base['active_current_status']['activation_truth']['chapter_core_argument_count']} live argument cores, "
        "v2.3.0 unchanged, exact evidence-competence successor active, and 8 rejecting mutations."
    )


if __name__ == "__main__":
    main()
