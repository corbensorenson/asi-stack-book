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


def input_paths(manifest: dict) -> set[Path]:
    return {RECORDS, Path(__file__).relative_to(ROOT), *VERIFIER_PACKAGE.values()} | {
        Path(path) for study in manifest["studies"] for path in [study["result"], *study["inputs"]]
    } | {Path(item["backlog"]) for item in manifest["agenda"]}


def metrics(study_id: str, result: dict) -> dict:
    if study_id == "scoped-git":
        groups = {arm: [r for r in result["trials"] if r["route"] == arm]
                  for arm in ("conventional", "full_governed")}
        conventional, governed = groups.values()
        if {r["path"] for r in conventional} != {r["path"] for r in governed}:
            raise ValueError("scoped Git study has unmatched cases")
        for group in (conventional, governed):
            if (any(r["unresolved_terminal_state"] or r["false_block"] or r["unauthorized_terminal_change"] for r in group)
                    or sum(r["accepted_useful_repair"] for r in group) != 2
                    or not any(r["compensation_verified"] for r in group)):
                raise ValueError("scoped Git study disposition changed")
        return {
            "pairs": len(conventional), "accepted": sum(r["accepted_useful_repair"] for r in conventional),
            "ordinary_files": sum(r["sidecar_receipt_files"] for r in conventional),
            "governed_files": sum(r["sidecar_receipt_files"] for r in governed),
        }
    if study_id == "crossed-receiver":
        pairs = result["pairs"]
        normal, more = "conventional_status", "additional_observation"
        differences = [r for r in pairs if r["arms"][more]["accepted_useful"] != r["arms"][normal]["accepted_useful"]]
        if any(r["sink_idempotent"] or r["observation_profile"] not in {"stale_status", "unavailable_status"}
               or r["arms"][normal]["accepted_useful"] for r in differences):
            raise ValueError("crossed receiver closure boundary changed")
        ordinary, extra = (sum(r["arms"][arm]["accepted_useful"] for r in pairs) for arm in (normal, more))
        fresh = sum(r["arms"][normal]["accepted_useful"] for r in pairs if r["observation_profile"] == "shared_fresh")
        return {"ordinary": ordinary, "extra_route": extra, "additional": extra - ordinary,
                "pairs": len(pairs), "fresh": fresh}
    if study_id == "verifier-rollout":
        conventional = result["summary"]["conventional"]
        retained = result["summary"]["bound_handoff"]
        if any(row["wrong_route"] or row["wrong_hold"] or row["wrong_promotion"] for row in (conventional, retained)):
            raise ValueError("verifier disposition changed")
        public = result["model_results"]["public-copy"]
        protected = result["model_results"]["record-change"]
        return {
            "prior_public": public["prior_correct"], "candidate_public": public["candidate_correct"],
            "public_cases": public["cases"], "prior_protected": protected["prior_correct"],
            "candidate_protected": protected["candidate_correct"], "protected_cases": protected["cases"],
            "pairs": result["paired_checkpoints"], "ordinary_reads": conventional["evidence_document_reads"],
            "retained_reads": retained["evidence_document_reads"], "writes": retained["handoff_writes"],
        }
    if study_id == "forward-transfer":
        totals = result["totals"]
        rows = result["tasks"]
        base, retrieval, routines = "no_library", "ordinary_retrieval", "reusable_routines"
        if any(not value for value in result["calibration"].values()):
            raise ValueError("forward transfer study failed calibration")
        def verified(task, arm):
            return task["outcomes"][arm]["terminal"] == "verified"
        if any(verified(row, base) != verified(row, routines) for row in rows):
            raise ValueError("forward transfer routine comparison changed")
        adverse = [r for r in rows if r["family"] == "out-of-family"]
        if any(verified(r, arm) for r in adverse for arm in (base, retrieval, routines)):
            raise ValueError("forward transfer adverse trial improved")
        return {
            "basic": totals[base]["verified"], "retrieval": totals[retrieval]["verified"],
            "tasks": len(rows), "adverse": len(adverse),
            "missed": sum(verified(r, base) and not verified(r, retrieval) for r in rows),
            "solved": sum(not verified(r, base) and verified(r, retrieval) for r in rows),
        }
    raise ValueError(f"unknown study {study_id}")


def studies_from(manifest: dict, read) -> list[dict]:
    studies = []
    published = set()
    for entry in manifest["studies"]:
        identity = entry["id"]
        if identity in published or not re.fullmatch(r"[a-z0-9-]+", identity):
            raise ValueError(f"duplicate or invalid study identity {identity}")
        if not re.fullmatch("[a-f0-9]{40}", entry["source_commit"]):
            raise ValueError(f"invalid citation for {identity}")
        content = read(Path(entry["result"]))
        values = metrics(identity, json.loads(content))
        studies.append({
            **entry, "summary": entry["result_summary"].format_map(values), "metrics": values,
            "result_sha256": hashlib.sha256(content).hexdigest(),
        })
        published.add(identity)
    if len(manifest["agenda"]) != 3 or not all(item["study"] in published for item in manifest["agenda"]):
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
