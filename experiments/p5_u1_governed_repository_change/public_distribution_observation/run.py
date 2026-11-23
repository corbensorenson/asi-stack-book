#!/usr/bin/env python3
"""Read public package manifests and compare the disposition of paired read policies."""

import argparse
import base64
from collections import Counter
from datetime import datetime, timezone
import gzip
from hashlib import sha256, sha512
from io import BytesIO
import json
from pathlib import Path
from statistics import median
import subprocess
import tarfile
from tempfile import TemporaryDirectory
from time import perf_counter, process_time

HERE = Path(__file__).resolve().parent
MIB = 1024 * 1024
TARBALL_LIMIT = 16 * MIB
MANIFEST_LIMIT = 128 * 1024
READS = {
    "primary": "https://cdn.jsdelivr.net/npm/{name}@{version}/package.json",
    "secondary": "https://unpkg.com/{name}@{version}/package.json",
}
STRATA = ("observed", "primary_unavailable", "both_unavailable", "wrong_body")
ARMS = ("primary_only", "caller_fallback", "gateway_fallback")


def fetch(url, limit):
    with TemporaryDirectory() as tmp:
        target = Path(tmp) / "body"
        start = perf_counter()
        result = subprocess.run(
            ["curl", "--silent", "--show-error", "--location", "--max-redirs", "4",
             "--proto", "=https", "--proto-redir", "=https", "--connect-timeout", "5",
             "--max-time", "12", "--max-filesize", str(limit), "--output", str(target),
             "--write-out", "%{json}", url],
            capture_output=True, check=False,
        )
        elapsed = round((perf_counter() - start) * 1000, 3)
        raw = target.read_bytes() if target.is_file() else b""
    response = json.loads(result.stdout or b"{}")
    status = response.get("response_code", 0)
    return raw, {
        "requested_url": url, "final_url": response.get("url_effective"),
        "http_status": status, "redirects": response.get("num_redirects", 0),
        "received_bytes": len(raw), "body_sha256": sha256(raw).hexdigest() if raw else None,
        "elapsed_ms": elapsed,
        "error": f"curl_exit_{result.returncode}" if result.returncode else (None if status == 200 else f"http_{status}"),
    }


def expected_manifest(raw, integrity):
    digest = "sha512-" + base64.b64encode(sha512(raw).digest()).decode("ascii")
    if digest != integrity:
        raise ValueError("archive_integrity_mismatch")
    with gzip.GzipFile(fileobj=BytesIO(raw)) as unzipped:
        archive = unzipped.read(64 * MIB + 1)
    if len(archive) > 64 * MIB:
        raise ValueError("expanded_archive_limit")
    with tarfile.open(fileobj=BytesIO(archive), mode="r:") as files:
        member = files.getmember("package/package.json")
        if not member.isfile() or member.size > MANIFEST_LIMIT:
            raise ValueError("manifest_member_invalid")
        return sha256(files.extractfile(member).read()).hexdigest()


def observe(row, order):
    raw, archive = fetch(row["tarball"], TARBALL_LIMIT)
    start = process_time()
    reference = None
    reference_error = archive["error"]
    if reference_error is None:
        try:
            reference = expected_manifest(raw, row["integrity"])
        except (KeyError, OSError, EOFError, ValueError, tarfile.TarError) as error:
            reference_error = str(error)
    processing_ms = (process_time() - start) * 1000
    reads = {}
    for role in order:
        _, reads[role] = fetch(READS[role].format(**row), MANIFEST_LIMIT)
    return {**row, "reference": archive, "expected_file_sha256": reference,
            "reference_error": reference_error, "reference_processing_ms": round(processing_ms, 3),
            "order": order, "reads": reads}


def masked(read):
    return {**read, "error": "masked_in_replay", "received_bytes": 0, "body_sha256": None}


def evaluate_case(row, following, stratum, arm):
    reference = row["expected_file_sha256"]
    primary = row["reads"]["primary"]
    secondary = row["reads"]["secondary"]
    if stratum != "observed":
        primary = masked(primary)
    if stratum == "both_unavailable":
        secondary = masked(secondary)
    elif stratum == "wrong_body":
        secondary = following["reads"]["secondary"]

    def matches(read):
        return reference is not None and read["error"] is None and read["body_sha256"] == reference

    used = [primary]
    if not matches(primary) and arm != "primary_only":
        used.append(secondary)
    winner = next((read for read in used if matches(read)), None)
    status = "verified" if winner else "unresolved"
    envelope = 0
    if arm == "gateway_fallback" and len(used) == 2:
        envelope = len(json.dumps({
            "artifact": f'{row["name"]}@{row["version"]}/package.json',
            "status": status, "sha256": winner["body_sha256"] if winner else None,
        }, separators=(",", ":")).encode())
    return {
        "disposition": status, "false_closure": bool(winner and stratum in {"wrong_body", "both_unavailable"}),
        "caller_requests": len(used) if arm == "caller_fallback" else 1,
        "service_requests": len(used), "response_body_bytes": sum(read["received_bytes"] for read in used) + envelope,
        "gateway_envelope_bytes": envelope,
        "captured_fetch_ms": round(sum(read["elapsed_ms"] for read in used), 3),
        "active_human_ms": None,
    }


def summarize(cases):
    counts = Counter(case["disposition"] for case in cases)
    return {
        "lineages": len(cases), "verified": counts["verified"], "unresolved": counts["unresolved"],
        "false_closures": sum(case["false_closure"] for case in cases),
        "caller_requests": sum(case["caller_requests"] for case in cases),
        "service_requests": sum(case["service_requests"] for case in cases),
        "body_bytes": sum(case["response_body_bytes"] for case in cases),
        "gateway_envelope_bytes": sum(case["gateway_envelope_bytes"] for case in cases),
        "median_fetch_ms": median(case["captured_fetch_ms"] for case in cases),
        "timed_human_sessions": 0, "active_human_ms": None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    started = datetime.now(timezone.utc).isoformat()
    cohort = (HERE / "cohort.json").read_bytes()
    rows = [
        observe(row, ["primary", "secondary"] if index % 2 == 0 else ["secondary", "primary"])
        for index, row in enumerate(json.loads(cohort)["sample"])
    ]
    start = process_time()
    for index, row in enumerate(rows):
        following = rows[(index + 1) % len(rows)]
        row["cases"] = {stratum: {arm: evaluate_case(row, following, stratum, arm) for arm in ARMS}
                        for stratum in STRATA}
    summaries = {
        stratum: {arm: summarize([row["cases"][stratum][arm] for row in rows]) for arm in ARMS}
        for stratum in STRATA
    }
    secondary_median = median(row["reads"]["secondary"]["elapsed_ms"] for row in rows)
    test = summaries["primary_unavailable"]
    gains = test["caller_fallback"]["verified"] - test["primary_only"]["verified"]
    extra_bytes = test["caller_fallback"]["body_bytes"] - test["primary_only"]["body_bytes"]
    adverse_false = sum(summaries[stratum][arm]["false_closures"]
                        for stratum in ("wrong_body", "both_unavailable") for arm in ARMS)
    result = {
        "started_utc": started, "completed_utc": datetime.now(timezone.utc).isoformat(),
        "cohort_sha256": sha256(cohort).hexdigest(),
        "protocol_sha256": sha256((HERE / "protocol.md").read_bytes()).hexdigest(),
        "automated_pair_scoring_ms": round((process_time() - start) * 1000, 3),
        "median_secondary_read_ms": secondary_median,
        "extra_body_bytes_per_recovered_closure": round(extra_bytes / gains, 3) if gains else None,
        "screen": {"min_three_recovered": gains >= 3, "no_observed_adverse_false_closures": adverse_false == 0,
                   "within_8192_bytes_per_recovered_closure": bool(gains and extra_bytes / gains <= 8192),
                   "median_second_read_within_1000_ms": secondary_median <= 1000},
        "summary": summaries, "observations": rows,
    }
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
