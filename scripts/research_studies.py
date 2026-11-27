#!/usr/bin/env python3
"""Build evidence-linked study summaries and a standalone verifier replay."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
from io import BytesIO, StringIO
import json
from pathlib import Path
import re
import shlex
from zipfile import ZipFile, ZipInfo

from research_case_rows import export_csv, rows_for

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
AUDIT = Path("experiments/nov20_instrument_audit")
AUDIT_LOCK = AUDIT / "input_lock.json"
AUDIT_REPLAYS = {
    "verifier-floor-cache": AUDIT / "check_verifier_revision_freshness.py",
    "receiver-effect-audit": AUDIT / "check_receiver_projection_freshness.py",
    "transfer-scheduler-audit": None,
}
AUDIT_PACKAGE = "instrument-audit-replay.zip"
RECEIVER_REPLAY_ID = "receiver-availability"
RECEIVER_PACKAGE = "receiver-availability-replay.zip"
GIT_REPLAY_ID = "git-retrospective"
GIT_PACKAGE = "scoped-git-replay.zip"
GIT_REPLAY = Path("experiments/p5_u1_governed_repository_change")
GIT_LOCK = GIT_REPLAY / "standalone_inputs/input_lock.json"
GIT_WRAPPER = GIT_REPLAY / "replay_scoped_git.py"
HOME_EXCERPT = Path("assets/research-studies.qmd")
READER_EXCERPT = Path("editions/reader_manuscript/current/generated/research-studies.qmd")


REPORT_TEMPLATE = Path("docs/reviews/verifier_reproduction_report.md")
REPORT_KINDS = {"rerun", "reanalysis", "changed-assumption"}
REPORT_DISPOSITIONS = {"confirmed", "narrowed", "disputed", "unresolved"}


HOME_STUDIES = {"scoped-git", "crossed-receiver", "verifier-rollout"}


def input_paths(manifest: dict) -> set[Path]:
    return {RECORDS, Path(__file__).relative_to(ROOT), Path("scripts/research_case_rows.py"),
            REPORT_TEMPLATE, *VERIFIER_PACKAGE.values()} | {
        Path(path) for run in manifest["runs"] for path in [run["result"], run["protocol"], *run["inputs"]]
    } | {Path(item["backlog"]) for item in manifest["agenda"]} | {
        Path(item["artifact"]) for item in manifest["independent_reports"]
    }


def freshness_work(result: dict) -> dict[str, dict]:
    totals = {}
    for name in result["cases"][0]["arms"]:
        work, wire, routes = Counter(), Counter(), Counter()
        for row in result["cases"]:
            observed = row["arms"][name]
            work.update(observed["work"])
            wire.update(observed.get("authority_pipe", {}))
            wire.update(observed.get("worker_pipe", {}))
            routes.update(decision["route"] for decision in observed["decisions"])
        totals[name] = {"work": dict(work), "wire": dict(wire), "routes": dict(routes)}
    if "totals" in result and result["totals"] != totals:
        raise ValueError("verifier freshness counters disagree with the recorded decisions")
    return totals


def metrics(format_id: str, result: dict) -> dict:
    if format_id == "authority_ordering_v1":
        schedules = result["cases"]
        if any(row["arms"]["transactional_memo"]["effect"] != row["arms"]["transactional_receipt"]["effect"]
               or row["arms"]["transactional_memo"]["outcome"] != row["arms"]["transactional_receipt"]["outcome"]
               for row in schedules):
            raise ValueError("checked grant ordering effects disagree")
        return {"schedules": len(schedules),
                "unauthorized": sum(row["arms"]["cached_permission_only"]["outcome"] == "unauthorized"
                                    for row in schedules)}
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
    if format_id == "receiver_availability_v3":
        pairs = result["pairs"]
        primary, more, matched = (
            [pair["arms"][name] for pair in pairs]
            for name in ("conventional_status", "additional_endpoint", "matched_conventional_access")
        )
        return {
            "pairs": len(pairs), "primary": sum(row["verified_closure"] for row in primary),
            "additional": sum(row["verified_closure"] for row in more),
            "matched": sum(row["verified_closure"] for row in matched),
            "agreement": sum(a["disposition"] == b["disposition"] for a, b in zip(more, matched, strict=True)),
            "matched_calls": sum(row["caller_status_calls"] for row in matched),
            "additional_calls": sum(row["caller_status_calls"] for row in more),
            "matched_bytes": sum(row["status_payload_bytes"] for row in matched),
            "additional_bytes": sum(row["status_payload_bytes"] for row in more),
        }
    if format_id == "verifier_policy_audit_v2":
        ordinary, retained = (result["totals"][arm] for arm in ("conventional_memoization", "retained_qualification"))
        return {"pairs": result["paired_checkpoints"], "ordinary_wrong": ordinary["wrong_routes"],
                "retained_wrong": retained["wrong_routes"], "ordinary_reads": ordinary["document_reads"],
                "retained_reads": retained["document_reads"], "handoff_bytes": retained["handoff_bytes_serialized"]}
    if format_id == "verifier_freshness_v1":
        cases = rows_for(format_id, result)
        if len(cases) != result["paired_checkpoints"] or any(row["adverse"] for row in cases):
            raise ValueError("verifier freshness decisions disagree with the pinned fixture")
        totals = freshness_work(result)
        ordinary = totals["conventional_memoization"]
        retained = totals["retained_qualification"]
        if ordinary["wire"] != retained["wire"]:
            raise ValueError("verifier freshness comparison used unequal transport")
        return {"pairs": len(cases), "ordinary_reads": ordinary["work"]["document_reads"],
                "retained_reads": retained["work"]["document_reads"],
                "handoff_bytes": retained["work"].get("handoff_bytes", 0),
                "messages": ordinary["wire"].get("messages", 0),
                "payload_bytes": ordinary["wire"].get("payload_bytes", 0),
                "specialist": ordinary["routes"].get("specialist", 0)}
    if format_id == "transfer_scheduler_v1":
        arms = result["summary"]["proposals/descriptive"]["arms"]
        return {"pairs": len(result["cases"]), "stratum": result["summary"]["proposals/descriptive"]["cells"],
                "whole_prior": arms["aware_whole__handle-depth"], "whole_reordered": arms["aware_whole__expanded-length"],
                "routines_prior": arms["aware_routine__handle-depth"], "routines_reordered": arms["aware_routine__expanded-length"]}
    if format_id == "package_observation":
        summary = result["summary"]["primary_unavailable"]
        return {"count": len(result["observations"]), "verified": summary["caller_fallback"]["verified"]}
    if format_id == "package_transport":
        summary = result["summary"]["primary_unavailable"]
        caller, gateway = (summary[arm] for arm in ("caller_fallback", "gateway_fallback"))
        if (caller["verified"], caller["caller_http_requests"]) != (gateway["verified"], gateway["caller_http_requests"]):
            raise ValueError("recorded transport arms disagree on verified outcomes or caller requests")
        return {"count": len(result["observations"]), "verified": caller["verified"], "caller": caller["caller_http_requests"],
                "bytes": summary["added_gateway_bytes_per_verified"]}
    if format_id == "review_packet":
        return {arm: sum(p["result"]["citation"] for p in result["packets"]
                         if p["id"].startswith("C") and p["comparison"] == arm + "_register")
                for arm in ("ordinary", "linked")}
    if format_id == "verification_arrivals":
        ordinary, explicit = (result["4"][name] for name in ("TaskQueue", "ObligationQueue"))
        return {"unfinished": ordinary["last_arrival"]["unresolved_checks"],
                "accepted": ordinary["drain"]["verified"], "ordinary": ordinary["drain"]["writes"],
                "explicit": explicit["drain"]["writes"]}
    if format_id == "revision_retrieval":
        held = [trial for trial in result["trials"] if trial["subject"] != "atlas"]
        return {"held": len({trial["subject"] for trial in held}),
                **{key: sum(t["citation"] for t in held if t["method"] == method and t["identified"] == identified)
                   for key, method, identified in (("text", "text", False), ("graph", "graph", False),
                                                  ("direct", "identifier", True))}}
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
        runs[identity] = {
            **entry, "summary": entry["result_summary"].format_map(values),
            "limit": entry["limit"].format_map(values), "metrics": values,
        }

    errors = report_errors(manifest["independent_reports"], set(runs))
    if errors:
        raise ValueError("; ".join(errors))
    for row in manifest["independent_reports"]:
        if hashlib.sha256(read(Path(row["artifact"]))).hexdigest() != row["artifact_sha256"]:
            raise ValueError(f'independent report artifact changed: {row["id"]} revision {row["revision"]}')
    studies = []
    for entry in questions.values():
        history = [run for run in runs.values() if run["study"] == entry["id"]]
        earlier = set()
        for run in history:
            predecessor = run.get("follow_up_to")
            if predecessor and predecessor not in earlier:
                raise ValueError(f'Follow-up {run["id"]} must name an earlier run in the same study')
            earlier.add(run["id"])
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
    selected = HOME_STUDIES if home else None
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
    return replay_zip(files)


def audit_replay_paths(read):
    locked = json.loads(read(AUDIT_LOCK))
    paths = {Path(name) for name in locked}
    if any(path.is_absolute() or ".." in path.parts or not path.parts
           or path.parts[0] not in {"experiments", "scripts"} for path in paths):
        raise ValueError("Unsafe member in the instrument audit input lock")
    return paths | {
        AUDIT_LOCK, AUDIT / "replay_featured.py", AUDIT / "standalone.md",
        AUDIT / "check_verifier_regression_intake.py", *(path for path in AUDIT_REPLAYS.values() if path),
    }


def audit_replay_archive(manifest, read) -> bytes:
    files = {path.as_posix(): read(path) for path in audit_replay_paths(read)}
    lock = json.loads(files[AUDIT_LOCK.as_posix()])
    for name, expected in lock.items():
        if hashlib.sha256(files[name]).hexdigest() != expected:
            raise ValueError(f"Locked replay member changed: {name}")
    files["README.md"] = files.pop((AUDIT / "standalone.md").as_posix())
    files["replay.py"] = files.pop((AUDIT / "replay_featured.py").as_posix())
    replays = {}
    for run in manifest["runs"]:
        identity = run["id"]
        if identity not in AUDIT_REPLAYS:
            continue
        command, *args = shlex.split(run["command"])
        if command != "python3" or not args or args[0] not in lock:
            raise ValueError(f"Replay command must start a frozen Python runner: {identity}")
        raw = read(Path(run["result"]))
        if hashlib.sha256(raw).hexdigest() != run["result_sha256"]:
            raise ValueError(f"Pinned replay result changed: {identity}")
        files[run["result"]] = raw
        files[f"cases-{identity}.csv"] = export_csv(identity, rows_for(run["format"], json.loads(raw)))
        variation = AUDIT_REPLAYS[identity]
        replays[identity] = {"python_args": args, "result": run["result"],
                             "result_sha256": run["result_sha256"],
                             "variation": variation.as_posix() if variation else None}
    if replays.keys() != AUDIT_REPLAYS.keys():
        raise ValueError("Instrument audit kit is missing a retained replay run")
    files["replays.json"] = (json.dumps(replays, indent=2, sort_keys=True) + "\n").encode()
    return replay_zip(files)


def receiver_replay_archive(manifest, read) -> bytes:
    run = next(row for row in manifest["runs"] if row["id"] == RECEIVER_REPLAY_ID)
    files = {path: read(Path(path)) for path in (run["result"], run["protocol"], *run["inputs"])}
    if hashlib.sha256(files[run["result"]]).hexdigest() != run["result_sha256"]:
        raise ValueError("Pinned receiver availability replay changed")
    command, *args = shlex.split(run["command"])
    if command != "python3" or not args or args[0] not in files:
        raise ValueError("Receiver availability replay has no bundled Python command")
    files["replay.py"] = read(AUDIT / "replay_featured.py")
    files["replays.json"] = (json.dumps({
        run["id"]: {"python_args": args, "result": run["result"],
                    "result_sha256": run["result_sha256"], "variation": None},
    }, sort_keys=True) + "\n").encode()
    files["README.md"] = (
        "# Replay the receiver availability comparison\n\n"
        "Extract this kit and open its directory. Use Python 3.10 or later.\n\n"
        f"```sh\npython3 replay.py {run['id']}\n```\n\n"
        "The replay compares all 288 pairs with the pinned result. Expect eight "
        "passing controls and 48, 80 and 80 verified closures in the three arms.\n"
        "Add `--vary` to reanalyse closure counts under selected joint availability conditions. "
        "The bundle includes the fixed design and the paired-case CSV.\n"
    ).encode()
    files[f"cases-{run['id']}.csv"] = export_csv(
        run["id"], rows_for(run["format"], json.loads(files[run["result"]]))
    )
    return replay_zip(files)


def git_replay_paths(read) -> set[Path]:
    lock = json.loads(read(GIT_LOCK))
    return {GIT_LOCK, GIT_WRAPPER, *(Path(name) for name in lock["runners"]),
            *(Path(row["path"]) for row in lock["files"].values())}


def git_replay_archive(manifest, read) -> bytes:
    run = next(row for row in manifest["runs"] if row["id"] == GIT_REPLAY_ID)
    files = {path.as_posix(): read(path) for path in git_replay_paths(read)}
    files.update({name: read(Path(name)) for name in (run["result"], run["protocol"])})
    lock = json.loads(files[GIT_LOCK.as_posix()])
    if json.loads(files[run["protocol"]])["task"]["pre_fix_commit"] != lock["origin_commit"]:
        raise ValueError("Scoped Git baseline origin differs from the original design")
    digests = {run["result"]: run["result_sha256"], run["protocol"]: run["protocol_sha256"],
               **lock["runners"], **{row["path"]: row["sha256"] for row in lock["files"].values()}}
    if any(hashlib.sha256(files[name]).hexdigest() != digest for name, digest in digests.items()):
        raise ValueError("Scoped Git replay input differs from its retained digest")
    files["replay.py"] = read(AUDIT / "replay_featured.py")
    files["replays.json"] = (json.dumps({
        run["id"]: {"python_args": [GIT_WRAPPER.as_posix()], "result": run["result"],
                    "result_sha256": run["result_sha256"], "variation": None},
    }, sort_keys=True) + "\n").encode()
    files["README.md"] = (
        "# Replay the scoped Git comparison\n\n"
        "Extract the kit. Use Python 3.10 or later and Git 2.28 or later.\n\n"
        "```sh\npython3 replay.py git-retrospective\n```\n\n"
        "The original runner builds disposable local repositories. A small wrapper supplies "
        "two byte-verified blobs from the original pre-fix commit. Expect an exact match, "
        "two accepted repairs per arm, and restored bytes with the original effect retained "
        "in both compensation cases.\n\n"
        "Add `--vary` to rescore compensation under a consumer that requires the original "
        "effect to remain an ancestor of main. No new trial is run for this reanalysis.\n"
    ).encode()
    files["cases-git-retrospective.csv"] = export_csv(
        run["id"], rows_for(run["format"], json.loads(files[run["result"]]))
    )
    return replay_zip(files)


def replay_zip(files) -> bytes:
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
