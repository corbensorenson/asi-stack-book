#!/usr/bin/env python3
"""Independent, dependency-free test-log evaluator for P2 task qualification."""

from __future__ import annotations


VALID = {"PASSED", "FAILED", "SKIPPED", "ERROR"}


def parse_cargo(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("test ") or " ... " not in line: continue
        identity, outcome = line[5:].rsplit(" ... ", 1)
        if identity and outcome == "ok": result[identity] = "PASSED"
        elif identity and outcome == "FAILED": result[identity] = "FAILED"
    return result


def parse_go(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    mapping = {"PASS": "PASSED", "FAIL": "FAILED", "SKIP": "SKIPPED"}
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("--- ") or ": " not in line or " (" not in line or not line.endswith(")"): continue
        prefix, rest = line[4:].split(": ", 1)
        if prefix not in mapping: continue
        identity = rest.rsplit(" (", 1)[0]
        if identity: result[identity] = mapping[prefix]
    return result


def _summary_counts(line: str) -> tuple[int, int, int] | None:
    labels = ["Tests run:", "Failures:", "Errors:", "Skipped:"]
    values = []
    cursor = 0
    for index, label in enumerate(labels):
        start = line.find(label, cursor)
        if start < 0: return None
        start += len(label)
        end = line.find(",", start) if index < 3 else len(line)
        token = line[start:end].strip().split()[0].rstrip(".,;")
        try: values.append(int(token))
        except ValueError: return None
        cursor = end + 1
    return values[0], values[1], values[2], values[3]


def parse_maven(text: str) -> dict[str, str]:
    result: dict[str, str] = {}; current: str | None = None; dtest = "---NO TEST NAME FOUND YET---"
    for raw in text.splitlines():
        line = raw.strip()
        running = line[8:] if line.startswith("Running ") else (line[15:] if line.startswith("[INFO] Running ") else None)
        if running is not None and running and all(char.isalnum() or char in "_$." for char in running):
            current = running; continue
        if "-Dtest=" in line:
            tail = line.split("-Dtest=", 1)[1]; dtest = tail.split()[0]
        if line.startswith("[ERROR] "):
            token = line[8:].split()[0]
            stem = token.split(":", 1)[0]
            if "." in stem and all(char.isalnum() or char in "_$." for char in stem):
                clazz, method = stem.rsplit(".", 1)
                result[f"{clazz}.{method}"] = "ERROR" if "Exception" in line and "AssertionError" not in line else "FAILED"
                result.setdefault(clazz, "FAILED")
        counts = _summary_counts(line)
        if counts is not None:
            _tests, failures, errors, skipped = counts
            clazz = line.rsplit(" in ", 1)[1].strip().rstrip(".:;") if " in " in line else current
            if clazz:
                result.setdefault(clazz, "PASSED" if failures == errors == skipped == 0 else ("SKIPPED" if failures == errors == 0 else "FAILED"))
            current = None
        if line.endswith("BUILD SUCCESS"): result.setdefault(dtest, "PASSED")
        elif line.endswith("BUILD FAILURE"): result.setdefault(dtest, "FAILED")
    return result


PARSERS = {"parse_log_cargo": parse_cargo, "parse_log_gotest": parse_go, "parse_java_mvn": parse_maven}


def evaluate(text: str, parser_name: str, exit_code: int) -> dict:
    if parser_name not in PARSERS: raise ValueError(f"unsupported independent parser: {parser_name}")
    statuses = PARSERS[parser_name](text)
    if any(value not in VALID for value in statuses.values()): raise ValueError("invalid independent status")
    visible_failure = any(value in {"FAILED", "ERROR"} for value in statuses.values())
    return {
        "statuses": statuses,
        "status_count": len(statuses),
        "visible_failure": visible_failure,
        "zero_exit_visible_failure": exit_code == 0 and visible_failure,
        "nonzero_exit_no_status": exit_code != 0 and not statuses,
        "zero_exit_no_status": exit_code == 0 and not statuses,
    }
