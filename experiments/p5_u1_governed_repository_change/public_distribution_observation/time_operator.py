#!/usr/bin/env python3
"""Time an approved participant's review of paired package observations offline."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from time import perf_counter

from run import ARMS, STRATA, masked


def show(read):
    print(f"Status {read['error'] or read['http_status']} | sha256 {read['body_sha256'] or 'unavailable'}")


def matches(read, reference):
    return bool(reference and read["error"] is None and read["body_sha256"] == reference)


def choose(choices):
    while True:
        answer = input(f"Choose {' or '.join(choices)}. ").strip().lower()
        if answer in choices:
            return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--arm", choices=ARMS, required=True)
    parser.add_argument("--stratum", choices=STRATA, required=True)
    parser.add_argument("--code", required=True, help="Opaque participant session code")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{3,36}", args.code) or args.output.exists():
        parser.error("Provide an opaque code and a new output file")
    capture = args.capture.read_bytes()
    rows = json.loads(capture)["observations"]
    order = sorted(range(len(rows)), key=lambda i: sha256(f"{args.code}:{i}".encode()).digest())
    output = []
    print("Verify only when an available response matches the expected hash. Each case has two evidence reads at most.")
    print("Prepare before pressing Enter. The offline task excludes services' waiting time.")
    for index in order:
        row = rows[index]
        primary = row["reads"]["primary"]
        secondary = row["reads"]["secondary"]
        if args.stratum != "observed":
            primary = masked(primary)
        if args.stratum == "both_unavailable":
            secondary = masked(secondary)
        elif args.stratum == "wrong_body":
            secondary = rows[(index + 1) % len(rows)]["reads"]["secondary"]
        input("Press Enter when ready for the next timed decision. ")
        started = perf_counter()
        print(f"Package {row['name']}@{row['version']}")
        reference = row["expected_file_sha256"]
        print(f"Expected manifest SHA-256 {reference or 'unavailable'}")
        show(primary)
        choices = ["verify", "hold"]
        attended = [primary]
        if args.arm == "gateway_fallback" and not matches(primary, reference):
            print("Gateway returned a second observation.")
            show(secondary)
            attended.append(secondary)
        choice = choose([*choices, "second"] if args.arm == "caller_fallback" else choices)
        if choice == "second":
            show(secondary)
            attended.append(secondary)
            choice = choose(choices)
        elapsed = round((perf_counter() - started) * 1000)
        supports_closure = any(matches(value, reference) for value in attended)
        output.append({"package": row["name"], "version": row["version"],
                       "decision": choice, "observations": len(attended), "active_ms": elapsed,
                       "false_closure": choice == "verify" and not supports_closure})
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump({"session_code": args.code, "capture_sha256": sha256(capture).hexdigest(),
                   "arm": args.arm, "stratum": args.stratum, "decisions": output}, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
