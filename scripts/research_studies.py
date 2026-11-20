#!/usr/bin/env python3
"""Build evidence-linked study summaries and a standalone verifier replay."""

from __future__ import annotations

import argparse
import csv
import hashlib
from io import BytesIO, StringIO
import json
from pathlib import Path
import re
from zipfile import ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
RECORDS = Path("products/research_studies.json")
SITE_REGISTRY = "products/evidence-registry"
PUBLIC_REGISTRY = "https://corbensorenson.github.io/asi-stack-book/" + SITE_REGISTRY
REPO = "https://github.com/corbensorenson/asi-stack-book"
VERIFIER = Path("experiments/verifier_replacement_comparison")
VERIFIER_RESULT = VERIFIER / "results/2026-11-20-local.json"
VERIFIER_PACKAGE = {
    "README.md": VERIFIER / "standalone.md",
    "scripts/compare_verifier_replacements.py": Path("scripts/compare_verifier_replacements.py"),
    **{str(VERIFIER / path): VERIFIER / path for path in (
        "fallback_expiry_extension.py", "input_lock.json", "model_cases.json", "protocol.md",
        "results/2026-11-20-local.json",
    )},
}
HOME_EXCERPT = Path("assets/research-studies.qmd")
READER_EXCERPT = Path("editions/reader_manuscript/current/generated/research-studies.qmd")


REPORT_TEMPLATE = Path("docs/reviews/verifier_reproduction_report.md")
REPORT_KINDS = {"rerun", "reanalysis", "changed-assumption"}
REPORT_DISPOSITIONS = {"confirmed", "narrowed", "disputed", "unresolved"}


def input_paths(manifest: dict) -> set[Path]:
    return {RECORDS, Path(__file__).relative_to(ROOT), Path("scripts/research_case_rows.py"),
            REPORT_TEMPLATE, *VERIFIER_PACKAGE.values()} | {
        Path(path) for run in manifest["runs"] for path in [run["result"], run["protocol"], *run["inputs"]]
    } | {Path(item["backlog"]) for item in manifest["agenda"]} | {
        Path(item["artifact"]) for item in manifest["independent_reports"]
    }


def metrics(format_id: str, result: dict) -> dict:
    if format_id == "scoped_git_v1":
        conventional, governed = (
            [r for r in result["trials"] if r["route"] == arm] for arm in ("conventional", "full_governed")
        )
        return {
            "pairs": len(conventional), "accepted": sum(r["accepted_useful_repair"] for r in conventional),
            "governed_accepted": sum(r["accepted_useful_repair"] for r in governed),
            "ordinary_files": sum(r["sidecar_receipt_files"] for r in conventional),
            "governed_files": sum(r["sidecar_receipt_files"] for r in governed),
        }
    if format_id == "receiver_crossed_v1":
        pairs = result["pairs"]
        normal, more = "conventional_status", "additional_observation"
        ordinary, extra = (sum(r["arms"][arm]["accepted_useful"] for r in pairs) for arm in (normal, more))
        fresh = sum(r["arms"][normal]["accepted_useful"] for r in pairs if r["observation_profile"] == "shared_fresh")
        return {"ordinary": ordinary, "extra_route": extra, "additional": extra - ordinary,
                "pairs": len(pairs), "fresh": fresh}
    if format_id == "verifier_rollout_v1":
        conventional = result["summary"]["conventional"]
        retained = result["summary"]["bound_handoff"]
        public = result["model_results"]["public-copy"]
        protected = result["model_results"]["record-change"]
        return {
            "prior_public": public["prior_correct"], "candidate_public": public["candidate_correct"],
            "public_cases": public["cases"], "prior_protected": protected["prior_correct"],
            "candidate_protected": protected["candidate_correct"], "protected_cases": protected["cases"],
            "pairs": result["paired_checkpoints"], "ordinary_reads": conventional["evidence_document_reads"],
            "retained_reads": retained["evidence_document_reads"], "writes": retained["handoff_writes"],
            "ordinary_wrong_routes": conventional["wrong_route"], "retained_wrong_routes": retained["wrong_route"],
        }
    if format_id == "transfer_pilot_v1":
        totals = result["totals"]
        rows = result["tasks"]
        base, retrieval, routines = "no_library", "ordinary_retrieval", "reusable_routines"

        def verified(task, arm):
            return task["outcomes"][arm]["terminal"] == "verified"

        return {
            "basic": totals[base]["verified"], "retrieval": totals[retrieval]["verified"],
            "routines": totals[routines]["verified"], "tasks": len(rows),
            "adverse": sum(r["family"] == "out-of-family" for r in rows),
            "missed": sum(verified(r, base) and not verified(r, retrieval) for r in rows),
            "solved": sum(not verified(r, base) and verified(r, retrieval) for r in rows),
        }
    if format_id == "transfer_factorial_v1":
        proposal = result["summary"]["proposals/descriptive"]
        expanded = result["summary"]["expanded/descriptive"]
        return {
            "stratum_cells": proposal["cells"], "proposal_whole": proposal["arms"]["aware_whole"]["verified"],
            "proposal_routine": proposal["arms"]["aware_routine"]["verified"],
            "expanded_whole": expanded["arms"]["aware_whole"]["verified"],
            "expanded_routine": expanded["arms"]["aware_routine"]["verified"],
            "cells": len(result["cases"]), "unique_tasks": result["unique_task_count"],
            "adverse_verified": sum(row["verified"] for row in result["by_family"]["adverse-mixing"]["arms"].values()),
        }
    if format_id == "receiver_effect_audit_v2":
        old, new = (result["totals"][arm] for arm in ("conventional_status", "additional_observation"))
        return {"controls": len(result["controls"]), "pairs": len(result["pairs"]),
                "ordinary": old["accepted_useful"], "extra": new["accepted_useful"],
                "wrong_holds": old["changed_safe_holds"] + new["changed_safe_holds"]}
    if format_id == "verifier_policy_audit_v2":
        ordinary, retained = (result["totals"][arm] for arm in ("conventional_memoization", "retained_qualification"))
        return {"pairs": result["paired_checkpoints"], "ordinary_wrong": ordinary["wrong_routes"],
                "retained_wrong": retained["wrong_routes"], "ordinary_reads": ordinary["document_reads"],
                "retained_reads": retained["document_reads"], "handoff_bytes": retained["handoff_bytes_serialized"]}
    if format_id == "transfer_scheduler_v1":
        arms = result["summary"]["proposals/descriptive"]["arms"]
        return {"pairs": len(result["cases"]), "stratum": result["summary"]["proposals/descriptive"]["cells"],
                "whole_prior": arms["aware_whole__handle-depth"], "whole_reordered": arms["aware_whole__expanded-length"],
                "routines_prior": arms["aware_routine__handle-depth"], "routines_reordered": arms["aware_routine__expanded-length"]}
    raise ValueError(f"unknown research evidence format {format_id}")


def research_id(identity: str) -> bool:
    return re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identity) is not None


def pinned_commit(value: str) -> bool:
    return re.fullmatch("[a-f0-9]{40}", value) is not None


def report_errors(reports: list[dict], runs: set[str]) -> list[str]:
    seen = set()
    errors = []
    for row in reports:
        identity = (row["id"], row["revision"])
        if (identity in seen or not research_id(row["id"]) or type(row["revision"]) is not int
                or row["revision"] < 1 or row["run"] not in runs or row["kind"] not in REPORT_KINDS
                or row["disposition"] not in REPORT_DISPOSITIONS or row["permission"] != "public"
                or not pinned_commit(row["source_commit"]) or not row["artifact"]
                or not re.fullmatch("[a-f0-9]{64}", row["artifact_sha256"])
                or not row["reported_result"].strip() or not row["decision"].strip()):
            errors.append(f"invalid independent report {identity}")
        seen.add(identity)
    return errors


def studies_from(manifest: dict, read) -> list[dict]:
    if manifest.get("schema_version") != "asi_stack.research_history.v1":
        raise ValueError("unknown research history format")
    questions = {row["id"]: row for row in manifest["studies"]}
    if len(questions) != len(manifest["studies"]) or not all(map(research_id, questions)):
        raise ValueError("duplicate or invalid study identity")
    runs = {}
    for entry in manifest["runs"]:
        identity = entry["id"]
        if identity in runs or not research_id(identity) or entry["study"] not in questions:
            raise ValueError(f"duplicate or unowned run identity {identity}")
        if not pinned_commit(entry["source_commit"]):
            raise ValueError(f"invalid citation for {identity}")
        content = read(Path(entry["result"]))
        if hashlib.sha256(content).hexdigest() != entry["result_sha256"]:
            raise ValueError(f"pinned run bytes changed: {identity}; add a separate run")
        if hashlib.sha256(read(Path(entry["protocol"]))).hexdigest() != entry["protocol_sha256"]:
            raise ValueError(f"pinned protocol bytes changed: {identity}; add a separate run")
        raw = json.loads(content)
        if "calibration" in raw and not all(raw["calibration"].values()):
            raise ValueError(f"run {identity} failed instrument calibration")
        values = metrics(entry["format"], raw)
        runs[identity] = {**entry, "summary": entry["result_summary"].format_map(values), "metrics": values}

    errors = report_errors(manifest["independent_reports"], set(runs))
    if errors:
        raise ValueError("; ".join(errors))
    for row in manifest["independent_reports"]:
        if hashlib.sha256(read(Path(row["artifact"]))).hexdigest() != row["artifact_sha256"]:
            raise ValueError(f'independent report artifact changed: {row["id"]} revision {row["revision"]}')
    studies = []
    for entry in questions.values():
        history = [run for run in runs.values() if run["study"] == entry["id"]]
        featured = next((run for run in history if run["id"] == entry["featured_run"]), None)
        if featured is None:
            raise ValueError(f"study {entry['id']} does not own its featured run")
        # Retain the earlier public summary and artifact fields as the featured
        # projection. The nested history is authoritative for exact citations.
        projection = {key: value for key, value in featured.items() if key not in {"id", "study", "title"}}
        studies.append({**entry, **projection, "runs": history})
    if len(manifest["agenda"]) != 3 or any(item["study"] not in questions for item in manifest["agenda"]):
        raise ValueError("active agenda must identify three current studies")
    return studies


def study_page(study_id: str) -> str:
    return f"study-{study_id}.html"


def excerpt(studies: list[dict], prefix: str, *, home: bool) -> str:
    selected = {"scoped-git", "crossed-receiver", "verifier-rollout"} if home else None
    rows = ["<!-- Generated by scripts/research_studies.py. -->", ""]
    for study in studies:
        if selected is not None and study["id"] not in selected:
            continue
        link = f"{prefix}/{study_page(study['id'])}"
        rows.append(f"- **[{study['title']}]({link}).** {study['summary']}")
    rows += ["", f"[See the active research agenda]({prefix}/research-agenda.html).", ""]
    return "\n".join(rows)


def paired_csv(raw: bytes) -> bytes:
    out = StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow([
        "scope", "profile", "tick", "expected_route", "evidence_sha256",
        "conventional_route", "retained_route", "conventional_inspections", "retained_inspections",
        "retained_writes",
    ])
    for pair in json.loads(raw)["pairs"]:
        for expected, ordinary, retained in zip(
            pair["expected_routes"], pair["arms"]["conventional"], pair["arms"]["bound_handoff"], strict=True
        ):
            if (ordinary["tick"], ordinary["evidence_sha256"]) != (retained["tick"], retained["evidence_sha256"]):
                raise ValueError("verifier arms do not share paired evidence")
            writer.writerow([
                pair["scope"], pair["profile"], ordinary["tick"], expected, ordinary["evidence_sha256"],
                ordinary["route"], retained["route"], ordinary["evidence_document_reads"],
                retained["evidence_document_reads"], retained["handoff_writes"],
            ])
    return out.getvalue().encode()


def verifier_archive(read) -> bytes:
    files = {target: read(source) for target, source in VERIFIER_PACKAGE.items()}
    files["paired_decisions.csv"] = paired_csv(files[str(VERIFIER_RESULT)])
    files["SHA256SUMS"] = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(files.items())
    ).encode()
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        for name, data in sorted(files.items()):
            archive.writestr(ZipInfo(name), data)
    return buffer.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate Quarto summaries")
    parser.add_argument("--package", type=Path, help="write the deterministic verifier replay ZIP")
    args = parser.parse_args()

    def read(path):
        return (ROOT / path).read_bytes()

    manifest = json.loads(read(RECORDS))
    studies = studies_from(manifest, read)
    pages = {
        HOME_EXCERPT: excerpt(studies, SITE_REGISTRY, home=True),
        READER_EXCERPT: excerpt(studies, PUBLIC_REGISTRY, home=False),
    }
    for path, text in pages.items():
        if args.write:
            (ROOT / path).write_text(text, encoding="utf-8")
        elif read(path) != text.encode():
            raise SystemExit(f"research study excerpt is stale: {path}")
    if args.package:
        args.package.write_bytes(verifier_archive(read))
    print(f"Research studies validated: {len(studies)} studies and {len(manifest['agenda'])} active questions.")


if __name__ == "__main__":
    main()
