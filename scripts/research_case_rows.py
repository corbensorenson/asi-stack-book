"""Normalize paired research rows while preserving each run's units of work."""

from __future__ import annotations

import csv
from io import StringIO
import re


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def case(case_id, condition, arms, *, exhausted=False, adverse=False):
    outcome_signatures = {value["signature"] for value in arms.values()}
    return {
        "id": slug(case_id), "condition": condition, "arms": arms,
        "disagrees": len(outcome_signatures) > 1,
        "exhausted": exhausted, "adverse": adverse,
    }


def arm(outcome, work, signature):
    return {"outcome": outcome, "work": work, "signature": signature}


def scoped_git(result):
    by_case = {}
    for row in result["trials"]:
        trials = by_case.setdefault(row["path"], {})
        if row["route"] in trials:
            raise ValueError("duplicate Git case/arm")
        trials[row["route"]] = row
    for name, trials in by_case.items():
        if set(trials) != {"conventional", "full_governed"}:
            raise ValueError("unmatched Git case")
        arms = {}
        for route in ("conventional", "full_governed"):
            row = trials[route]
            checks = (
                row["accepted_useful_repair"], row["false_block"], row["unauthorized_terminal_change"],
                row["unresolved_terminal_state"], row["compensation_verified"], row["effect_is_ancestor_of_tip"],
            )
            labels = ["Accepted repair" if checks[0] else "No accepted repair"]
            for observed, label in zip(checks[1:5], (
                "wrong hold", "unauthorized terminal change", "unresolved terminal state", "compensation verified"
            ), strict=True):
                if observed:
                    labels.append(label)
            if checks[5] is not None:
                labels.append("effect in branch ancestry" if checks[5] else "effect outside branch ancestry")
            arms[route] = arm("; ".join(labels),
                              f'{row["sidecar_receipt_files"]} receipt files, {row["sidecar_receipt_bytes"]} bytes', checks)
        yield case(name, name.replace("_", " "), arms, adverse=any(
            row["false_block"] or row["unauthorized_terminal_change"] or row["unresolved_terminal_state"]
            for row in trials.values()
        ))


def authority_ordering(result):
    for row in result["cases"]:
        arms = {}
        for name, observation in row["arms"].items():
            effect = observation["effect"]
            order = (f'Commit tick {effect["tick"]}, used revision {effect["used_revision"]}'
                     if effect else "No committed effect")
            order += f'; observed revision {observation["revision_at_observation"]}'
            arms[name] = arm(observation["outcome"], order, observation["outcome"])
        identity = row["case"]
        yield case(identity, identity.replace("_", " "), arms,
                   adverse=any(observation["outcome"] == "unauthorized" for observation in row["arms"].values()))


def crossed_receiver(result):
    for row in result["pairs"]:
        sink = "deduplicating" if row["sink_idempotent"] else "non-deduplicating"
        condition = f'{row["task"]} · {sink} · {row["scenario"]} · {row["observation_profile"]}'
        arms = {}
        for route, receipt in row["arms"].items():
            steps = [action["action"] for action in receipt["actions"]]
            signature = (receipt["disposition"], receipt["effect_commits"], receipt["false_closure"], receipt["wrongful_block"])
            outcome = f'{receipt["disposition"]}, {receipt["effect_commits"]} committed effects'
            if "observed_effect" in receipt:
                observed = receipt["observed_effect"]
                signature += (observed, receipt["safe_hold"])
                outcome = f'{receipt["disposition"]} · {observed.replace("_", " ")}'
            if receipt["false_closure"] or receipt["wrongful_block"]:
                outcome += f', {int(receipt["false_closure"])} false closures, {int(receipt["wrongful_block"])} wrong blocks'
            arms[route] = arm(outcome, f'{steps.count("retry")} retries, {steps.count("receive_read")} additional reads', signature)
        yield case(condition, condition, arms, adverse=any(
            receipt["false_closure"] or receipt["wrongful_block"] or receipt["effect_commits"] > 1
            or receipt.get("observed_effect") == "wrong_effect" for receipt in row["arms"].values()
        ))


def verifier_rollout(result):
    for pair in result["pairs"]:
        for expected, ordinary, retained in zip(
            pair["expected_routes"], pair["arms"]["conventional"], pair["arms"]["bound_handoff"], strict=True
        ):
            if (ordinary["tick"], ordinary["evidence_sha256"]) != (retained["tick"], retained["evidence_sha256"]):
                raise ValueError("verifier arms do not share paired evidence")
            name = f'{pair["scope"]}-{pair["profile"]}-tick-{ordinary["tick"]}'
            condition = f'{pair["scope"]} · {pair["profile"]} · tick {ordinary["tick"]} · expected {expected}'
            arms = {}
            for route, receipt in (("conventional", ordinary), ("bound_handoff", retained)):
                work = f'{receipt["evidence_document_reads"]} inspections, {receipt["handoff_writes"]} writes'
                if receipt["gaps"]:
                    work += " · " + ", ".join(receipt["gaps"])
                arms[route] = arm(f'{receipt["decision"]} → {receipt["route"]}', work,
                                  (receipt["decision"], receipt["route"]))
            yield case(name, condition, arms, adverse=any(row["route"] != expected for row in (ordinary, retained)))


def receiver_availability(result):
    for pair in result["pairs"]:
        condition = (f'{pair["task"]} · primary {pair["primary"]} · secondary {pair["secondary"]} · '
                     f'{pair["initial_state"].replace("_", " ")} · '
                     f'{"deduplicating" if pair["deduplication"] else "non-deduplicating"}')
        arms = {}
        for name in ("conventional_status", "additional_endpoint", "matched_conventional_access"):
            trial = pair["arms"][name]
            qualifiers = [trial["disposition"]]
            for field in ("verified_closure", "false_closure", "wrong_effect", "repeat_effect"):
                if trial[field]:
                    qualifiers.append(field.replace("_", " "))
            work = (f'{trial["logical_status_reads"]} reads, {trial["caller_status_calls"]} caller requests, '
                    f'{trial["retries"]} retries, {trial["status_payload_bytes"]} status bytes')
            arms[name] = arm(" · ".join(qualifiers), work, tuple(qualifiers))
        yield case(f'pair-{pair["id"]:03}', condition, arms,
                   adverse=pair["initial_state"] in {"wrong_effect", "repeat_effect"})


def verifier_policy_audit(result):
    for profile in result["cases"]:
        names = tuple(profile["arms"])
        for decisions in zip(*(profile["arms"][name]["decisions"] for name in names), strict=True):
            head = decisions[0]
            identity = (head["tick"], head["consumer"], head["expected"], head["revision"])
            if any((d["tick"], d["consumer"], d["expected"], d["revision"]) != identity for d in decisions):
                raise ValueError("cache comparison lost its matched input")
            label = f'{profile["id"]} · tick {head["tick"]} · {head["consumer"]} · expected {head["expected"]}'
            arms = {}
            for name, row in zip(names, decisions, strict=True):
                cost = profile["arms"][name]["work"]
                work = f'Profile total: {cost["document_reads"]} document reads, {cost["policy_evaluations"]} policy evaluations'
                if row["reasons"]:
                    work += " · " + ", ".join(row["reasons"])
                arms[name] = arm(row["route"], work, row["route"])
            yield case(label, label, arms, adverse=any(row["route"] != row["expected"] for row in decisions))


def verifier_freshness(result):
    for profile in result["cases"]:
        names = tuple(profile["arms"])
        for decisions in zip(*(profile["arms"][name]["decisions"] for name in names), strict=True):
            first = decisions[0]
            paired_fields = ("tick", "consumer", "expected_route", "pinned_version", "returned_version",
                             "observed_index_version", "revision")
            if any(any(row.get(field) != first.get(field) for field in paired_fields) for row in decisions[1:]):
                raise ValueError("verifier freshness arms do not share paired inputs")
            identity = f'{profile["case"]}-{first["tick"]}-{first["consumer"]}'
            label = (f'{profile["case"].replace("_", " ")} · tick {first["tick"]} · {first["consumer"]}'
                     f' · expected {first["expected_route"]}')
            arms = {name: arm(row["route"], row["reason"], row["route"])
                    for name, row in zip(names, decisions, strict=True)}
            yield case(identity, label, arms, adverse=any(row["route"] != first["expected_route"] for row in decisions))


def synthesis_case_records(result, factorial):
    for row in result["cases" if factorial else "tasks"]:
        condition = f'{row["task"]} · {row["family"]}'
        name = row["task"]
        if factorial:
            budget = row["budget"]
            cap = result["budget_caps"][budget]
            name = f'{name}-{row["phrasing"]}-{budget}-{row["order"]}'
            unit = "proposals" if budget == "proposals" else "expanded execution steps"
            condition += f' · {row["phrasing"]} · {cap} {unit} · {row["order"]}'
        else:
            condition += f' · {result["search_budget"]} proposals · {row["description"]}'
        arms = {}
        outcomes = row["arms" if factorial else "outcomes"]
        for label, trial in outcomes.items():
            library = trial["library" if factorial else "library_entries"]
            proposals = trial["proposals" if factorial else "attempts"]
            screen = trial["screening_steps" if factorial else "screening_primitive_steps"]
            check = trial["verification_steps" if factorial else "checker_primitive_steps"]
            expanded = (trial["solution"] or {}).get("expanded") if factorial else trial["expanded_program"]
            work = f'{proposals} proposals, {screen + check} executed steps'
            if library:
                work += " · library " + ", ".join(f'{entry} ({" → ".join(ops)})' for entry, ops in library)
            if expanded is not None:
                work += " · solution " + (" → ".join(expanded) or "identity")
            terminal = trial["terminal"]
            arms[label] = arm(terminal.replace("_", " "), work, terminal == "verified")
        yield case(name, condition, arms,
                   exhausted=any(item["terminal"].endswith("budget_exhausted") for item in outcomes.values()),
                   adverse=row["family"] in {"out-of-family", "adverse-mixing"})


def rows_for(format_id, result):
    if format_id == "scoped_git_v1":
        rows = scoped_git(result)
    elif format_id == "authority_ordering_v1":
        rows = authority_ordering(result)
    elif format_id in {"receiver_crossed_v1", "receiver_effect_audit_v2"}:
        rows = crossed_receiver(result)
    elif format_id == "receiver_availability_v3":
        rows = receiver_availability(result)
    elif format_id == "verifier_rollout_v1":
        rows = verifier_rollout(result)
    elif format_id == "verifier_policy_audit_v2":
        rows = verifier_policy_audit(result)
    elif format_id == "verifier_freshness_v1":
        rows = verifier_freshness(result)
    elif format_id in {"transfer_pilot_v1", "transfer_factorial_v1", "transfer_scheduler_v1"}:
        rows = synthesis_case_records(result, format_id != "transfer_pilot_v1")
    else:
        raise ValueError(f"unsupported research case format: {format_id}")
    ordered = sorted(rows, key=lambda row: (not row["disagrees"], row["id"]))
    if not ordered or len(ordered) != len({row["id"] for row in ordered}):
        raise ValueError("research cases are empty or have colliding identities")
    if any(tuple(row["arms"]) != tuple(ordered[0]["arms"]) for row in ordered):
        raise ValueError("research cases have inconsistent arm order")
    return ordered


def anchor(run_id: str, case_id: str | None = None) -> str:
    stem = f"run-{run_id}"
    return f"{stem}--case-{case_id}" if case_id else stem


def export_csv(run_id, rows):
    out = StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["run_id", "case_id", "fragment", "condition", "outcomes_differ", "arm", "outcome", "work"])
    for row in rows:
        for name, trial in row["arms"].items():
            writer.writerow([run_id, row["id"], anchor(run_id, row["id"]), row["condition"],
                             int(row["disagrees"]), name, trial["outcome"], trial["work"]])
    return out.getvalue().encode()
