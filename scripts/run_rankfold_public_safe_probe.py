#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "rankfold_public_safe_probe" / "results" / "2026-07-02-local.json"
PROBE_ID = "rankfold-public-safe-probe-2026-07-02-local"
RESULT_COMMAND = "python3 scripts/run_rankfold_public_safe_probe.py --write-result"
DEFAULT_RFA = Path("/Users/corbensorenson/Documents/RankFold/target/debug/rfa")
DEFAULT_RANKFOLD_REPO = Path("/Users/corbensorenson/Documents/RankFold")

NON_CLAIMS = [
    "This RankFold public-safe replay probe does not promote any chapter core claim above argument.",
    "This RankFold public-safe replay probe does not create a support-state transition.",
    "This RankFold public-safe replay probe does not prove RankFold codec correctness, NeuralFold compression, compression advantage, benchmark performance, downstream utility, fallback execution, deployed compression behavior, model quality, or ASI.",
    "This RankFold public-safe replay probe uses a synthetic public-safe text fixture and records hashes, ratios, command outcomes, and non-claims only; it does not copy dataset bytes, archive bytes, private source text, private keys, or local absolute paths into the repository.",
]


def build_corpus() -> bytes:
    return (
        "ASI Stack RankFold public-safe probe\n" * 64
        + "boundary, fallback, residual, decode determinism\n" * 32
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sanitize_output(value: str, temp_dir: Path) -> str:
    text = value.replace(str(temp_dir), "<TMP>")
    text = text.replace(str(DEFAULT_RFA), "rfa")
    text = re.sub(r"/var/folders/[^ \n]+", "<TMP>", text)
    return text


def command_record(command_id: str, argv: list[str], temp_dir: Path) -> dict[str, Any]:
    started = time.perf_counter()
    result = subprocess.run(
        argv,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    output = sanitize_output(result.stdout, temp_dir)
    lines = [line for line in output.strip().splitlines() if line]
    return {
        "id": command_id,
        "argv_summary": summarize_argv(command_id),
        "exit_code": result.returncode,
        "elapsed_ms": elapsed_ms,
        "output_sha256": sha256_text(output),
        "output_excerpt": lines[:8],
        "_full_output": output,
    }


def summarize_argv(command_id: str) -> str:
    summaries = {
        "pack": "rfa pack --output <TMP>/probe.rfa <TMP>/rankfold_public_probe.txt",
        "verify": "rfa verify <TMP>/probe.rfa",
        "list": "rfa list <TMP>/probe.rfa",
        "unpack": "rfa unpack --output <TMP>/unpacked <TMP>/probe.rfa",
        "verify_corrupt": "rfa verify <TMP>/probe_corrupt.rfa",
    }
    return summaries[command_id]


def extract_verify_counts(output: str) -> dict[str, int]:
    match = re.search(r"Verification complete:\s+(\d+) OK,\s+(\d+) FAILED,\s+(\d+) skipped", output)
    if not match:
        return {"ok": 0, "failed": 0, "skipped": 0}
    return {"ok": int(match.group(1)), "failed": int(match.group(2)), "skipped": int(match.group(3))}


def git_dirty_boundary(repo: Path) -> dict[str, Any]:
    if not repo.exists():
        return {
            "source_project_ref": "local RankFold checkout unavailable",
            "source_project_dirty_at_probe": None,
            "source_project_status_entry_count": None,
        }
    result = subprocess.run(
        ["git", "-C", str(repo), "status", "--short"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return {
        "source_project_ref": "local RankFold checkout",
        "source_project_dirty_at_probe": bool(lines),
        "source_project_status_entry_count": len(lines),
    }


def rfa_binary() -> Path:
    return Path(os.environ.get("RANKFOLD_RFA_BIN", str(DEFAULT_RFA))).expanduser()


def build_record() -> dict[str, Any]:
    rfa = rfa_binary()
    if not rfa.exists():
        raise SystemExit(f"RankFold rfa binary not found: {rfa}")

    corpus = build_corpus()
    with tempfile.TemporaryDirectory(prefix="rankfold_public_probe_") as temp:
        temp_dir = Path(temp)
        input_file = temp_dir / "rankfold_public_probe.txt"
        archive_file = temp_dir / "probe.rfa"
        unpack_dir = temp_dir / "unpacked"
        corrupt_file = temp_dir / "probe_corrupt.rfa"
        input_file.write_bytes(corpus)

        pack = command_record("pack", [str(rfa), "pack", "--output", str(archive_file), str(input_file)], temp_dir)
        if pack["exit_code"] != 0:
            return failed_record(rfa, corpus, [pack], "pack failed")

        verify = command_record("verify", [str(rfa), "verify", str(archive_file)], temp_dir)
        listing = command_record("list", [str(rfa), "list", str(archive_file)], temp_dir)
        unpack = command_record("unpack", [str(rfa), "unpack", "--output", str(unpack_dir), str(archive_file)], temp_dir)

        archive_bytes = archive_file.read_bytes()
        mutated = bytearray(archive_bytes)
        mutation_offset = min(128, max(0, len(mutated) - 1))
        mutated[mutation_offset] ^= 0xFF
        corrupt_file.write_bytes(mutated)
        verify_corrupt = command_record("verify_corrupt", [str(rfa), "verify", str(corrupt_file)], temp_dir)

        unpacked_file = unpack_dir / input_file.name
        unpacked_bytes = unpacked_file.read_bytes() if unpacked_file.exists() else b""
        commands = [pack, verify, listing, unpack, verify_corrupt]
        command_records = [{k: v for k, v in record.items() if k != "_full_output"} for record in commands]
        verify_counts = extract_verify_counts(verify["_full_output"])
        list_output = listing["_full_output"]
        codec = "RAW0" if "RAW0" in list_output else "unknown"
        pack_output = pack["_full_output"]
        neuralfold_disabled = "NeuralFold is disabled by license" in pack_output
        raw_engine = "Raw (stored)" in pack_output
        archive_size = len(archive_bytes)
        input_size = len(corpus)
        roundtrip_exact = unpacked_bytes == corpus

        return {
            "schema_version": "0.1",
            "probe_id": PROBE_ID,
            "record_kind": "rankfold_public_safe_replay_probe",
            "recorded_at_utc": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
            "command": RESULT_COMMAND,
            "local_only": True,
            "public_safety_boundary": "No dataset bytes, archive bytes, local absolute paths, private source text, private keys, or unpublished implementation payloads are copied into the ASI Stack book repository.",
            "support_state_effect": "none",
            "chapter_core_support_effect": "none",
            "evidence_transition_created": False,
            "pass": all(record["exit_code"] == 0 for record in [pack, verify, listing, unpack])
            and verify_corrupt["exit_code"] != 0
            and roundtrip_exact,
            "rfa_binary_sha256": sha256_bytes(rfa.read_bytes()),
            **git_dirty_boundary(DEFAULT_RANKFOLD_REPO),
            "input": {
                "logical_name": "rankfold_public_probe.txt",
                "generator": "scripts/run_rankfold_public_safe_probe.py::build_corpus",
                "bytes": input_size,
                "sha256": sha256_bytes(corpus),
                "public_safe": True,
            },
            "roundtrip": {
                "archive_file_bytes": archive_size,
                "archive_file_sha256": sha256_bytes(archive_bytes),
                "archive_to_input_ratio": round(archive_size / input_size, 8),
                "input_to_archive_ratio": round(input_size / archive_size, 8),
                "compression_advantage_observed": archive_size < input_size,
                "codec_observed": codec,
                "pack_engine_observed": "Raw (stored)" if raw_engine else "unknown",
                "neuralfold_disabled_by_license": neuralfold_disabled,
                "verify": verify_counts,
                "unpacked_file_bytes": len(unpacked_bytes),
                "unpacked_sha256": sha256_bytes(unpacked_bytes),
                "roundtrip_exact": roundtrip_exact,
            },
            "negative_control": {
                "kind": "single_byte_archive_mutation",
                "mutated_offset": mutation_offset,
                "verify_exit_code": verify_corrupt["exit_code"],
                "rejected": verify_corrupt["exit_code"] != 0,
                "output_excerpt": verify_corrupt["output_excerpt"][:4],
            },
            "commands": command_records,
            "non_claims": NON_CLAIMS,
        }


def failed_record(rfa: Path, corpus: bytes, commands: list[dict[str, Any]], reason: str) -> dict[str, Any]:
    command_records = [{k: v for k, v in record.items() if k != "_full_output"} for record in commands]
    return {
        "schema_version": "0.1",
        "probe_id": PROBE_ID,
        "record_kind": "rankfold_public_safe_replay_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": False,
        "failure_reason": reason,
        "rfa_binary_sha256": sha256_bytes(rfa.read_bytes()),
        **git_dirty_boundary(DEFAULT_RANKFOLD_REPO),
        "input": {
            "logical_name": "rankfold_public_probe.txt",
            "generator": "scripts/run_rankfold_public_safe_probe.py::build_corpus",
            "bytes": len(corpus),
            "sha256": sha256_bytes(corpus),
            "public_safe": True,
        },
        "commands": command_records,
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a public-safe local RankFold pack/verify/unpack probe.")
    parser.add_argument("--write-result", action="store_true", help=f"write {RESULT.relative_to(ROOT)}")
    args = parser.parse_args()

    record = build_record()
    text = json.dumps(record, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(text, end="")
    if not record.get("pass"):
        sys.exit(1)


if __name__ == "__main__":
    main()
