#!/usr/bin/env python3
"""Compare two placements with real, read-only package delivery requests."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from statistics import median
from threading import Thread
from time import perf_counter
from urllib.parse import urlsplit

from run import HERE, MANIFEST_LIMIT, READS, STRATA, TARBALL_LIMIT, expected_manifest, fetch

ARMS = ("caller_fallback", "gateway_fallback")


def prepare(row):
    raw, trace = fetch(row["tarball"], TARBALL_LIMIT)
    expected = None
    problem = trace["error"]
    if not problem:
        try:
            expected = expected_manifest(raw, row["integrity"])
        except (KeyError, ValueError, OSError, EOFError) as error:
            problem = type(error).__name__
    return {"expected": expected, "trace": trace, "error": problem}


def read_response(row, role, condition, control):
    withheld = (role == "primary" and condition != "observed") or condition == "both_unavailable"
    if withheld:
        return b"", {"role": role, "origin": "locally_withheld", "http_requests": 0,
                     "received_bytes": 0, "response_header_bytes": 0, "error": "withheld"}
    if condition == "wrong_body":
        raw, trace = control
        return raw, {**trace, "role": role, "origin": "retained_other_lineage",
                     "http_requests": 0, "received_bytes": 0, "response_header_bytes": 0}
    raw, trace = fetch(READS[role].format(**row), MANIFEST_LIMIT)
    return raw, {**trace, "role": role, "origin": "live", "http_requests": 1 + trace["redirects"]}


def observe(row, reference, condition, control):
    traces = []
    for role in READS:
        raw, trace = read_response(row, role, condition, control)
        traces.append(trace)
        if reference and not trace["error"] and sha256(raw).hexdigest() == reference:
            return raw, traces
    return None, traces


def make_gateway(cohort, references, controls, journal):
    def reply(key, condition):
        return observe(cohort[key], references[key]["expected"], condition, controls[key])

    class Gateway(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def log_message(self, *args):
            pass

        def do_GET(self):
            address = urlsplit(self.path)
            pieces = address.path.strip("/").split("/")
            if address.query or len(pieces) != 2 or pieces[0] not in cohort or pieces[1] not in STRATA:
                self.send_error(404)
                return
            key, condition = pieces
            value, trace = reply(key, condition)
            body = value if value is not None else b""
            self.send_response(200 if value is not None else 409)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            journal[(key, condition)] = trace

    return HTTPServer(("127.0.0.1", 0), Gateway)


def gateway_result(server, key, condition):
    connection = HTTPConnection("127.0.0.1", server.server_port, timeout=30)
    try:
        connection.request("GET", f"/{key}/{condition}")
        response = connection.getresponse()
        body = response.read(MANIFEST_LIMIT + 1)
        header_bytes = len(f"HTTP/1.0 {response.status} {response.reason}\r\n\r\n".encode("ascii"))
        header_bytes += sum(len(f"{name}: {value}\r\n".encode("latin-1")) for name, value in response.getheaders())
        return response.status, body, header_bytes
    finally:
        connection.close()


def attempt(arm, server, journal, key, row, reference, condition, control):
    start = perf_counter()
    gateway_bytes = gateway_headers = 0
    if arm == "gateway_fallback":
        code, raw, gateway_headers = gateway_result(server, key, condition)
        gateway_bytes = len(raw)
        traces = journal.pop((key, condition))
        accepted = code == 200 and bool(reference) and sha256(raw).hexdigest() == reference
    else:
        raw, traces = observe(row, reference, condition, control)
        accepted = raw is not None
    elapsed = round((perf_counter() - start) * 1000, 3)
    upstream_requests = sum(trace["http_requests"] for trace in traces)
    upstream_bytes = sum(trace["received_bytes"] for trace in traces)
    upstream_headers = sum(trace["response_header_bytes"] for trace in traces)
    gateway_count = int(arm == "gateway_fallback")
    return {
        "verified": accepted, "unresolved": not accepted,
        "false_closure": accepted and condition in {"both_unavailable", "wrong_body"},
        "elapsed_caller_ms": elapsed, "caller_http_requests": gateway_count or upstream_requests,
        "upstream_http_requests": upstream_requests, "upstream_body_bytes": upstream_bytes,
        "upstream_header_bytes": upstream_headers, "gateway_body_bytes": gateway_bytes,
        "gateway_header_bytes": gateway_headers,
        "http_response_bytes_all_hops": upstream_bytes + upstream_headers + gateway_bytes + gateway_headers,
        "traces": traces,
    }


def summarize(cases, condition):
    rows = [row["conditions"][condition] for row in cases]
    metrics = ("verified", "unresolved", "false_closure", "caller_http_requests",
               "upstream_http_requests", "http_response_bytes_all_hops")
    summary = {
        arm: {field: sum(group[arm][field] for group in rows) for field in metrics}
        for arm in ARMS
    }
    caller, gateway = ARMS
    summary["same_outcomes"] = all(row[caller]["verified"] == row[gateway]["verified"] for row in rows)
    summary["median_paired_added_gateway_ms"] = median(
        row[gateway]["elapsed_caller_ms"] - row[caller]["elapsed_caller_ms"] for row in rows
    )
    summary["added_gateway_bytes_per_verified"] = (
        (summary[gateway]["http_response_bytes_all_hops"] - summary[caller]["http_response_bytes_all_hops"])
        / summary[gateway]["verified"] if summary[gateway]["verified"] else None
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a new output file")
    acquired = datetime.now(timezone.utc).isoformat()
    cohort_raw = (HERE / "transport-cohort.json").read_bytes()
    rows = json.loads(cohort_raw)["sample"]
    keys = [row["name"] for row in rows]
    cohort = dict(zip(keys, rows, strict=True))
    references = {key: prepare(row) for key, row in cohort.items()}
    controls = {key: fetch(READS["secondary"].format(**cohort[key]), MANIFEST_LIMIT) for key in keys}
    wrong_by_key = {key: controls[keys[(i + 1) % len(keys)]] for i, key in enumerate(keys)}
    journal = {}
    cases = []
    with make_gateway(cohort, references, wrong_by_key, journal) as server:
        worker = Thread(target=server.serve_forever)
        worker.start()
        try:
            for index, (key, row) in enumerate(cohort.items()):
                conditions = {}
                for i, condition in enumerate(STRATA):
                    order = ARMS if (index + i) % 2 == 0 else ARMS[::-1]
                    conditions[condition] = {
                        arm: attempt(arm, server, journal, key, row, references[key]["expected"],
                                     condition, wrong_by_key[key])
                        for arm in order
                    }
                cases.append({"package": key, "version": row["version"], "reference": references[key],
                              "adverse_body_preparation": controls[key][1], "conditions": conditions})
        finally:
            server.shutdown()
            worker.join()
    summaries = {condition: summarize(cases, condition) for condition in STRATA}
    withheld = summaries["primary_unavailable"]
    added_bytes = withheld["added_gateway_bytes_per_verified"]
    screen = {
        "same_main_outcomes": all(summaries[condition]["same_outcomes"] for condition in STRATA[:2]),
        "at_least_three_verified_fallbacks_per_arm": all(withheld[arm]["verified"] >= 3 for arm in ARMS),
        "zero_false_closures_in_controls": not any(summaries[condition][arm]["false_closure"]
                                                  for condition in STRATA[2:] for arm in ARMS),
        "paired_median_added_gateway_ms_within_1000": withheld["median_paired_added_gateway_ms"] <= 1000,
        "added_gateway_response_bytes_within_8192_per_verified": added_bytes is not None and added_bytes <= 8192,
    }
    result = {
        "started_utc": acquired, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "cohort_sha256": sha256(cohort_raw).hexdigest(),
        "protocol_sha256": sha256((HERE / "transport-protocol.md").read_bytes()).hexdigest(),
        "human_operator_time_ms": None, "observations": cases, "summary": summaries, "screen": screen,
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
