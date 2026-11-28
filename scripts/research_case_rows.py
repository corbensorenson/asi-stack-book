"""Normalize paired research rows while preserving each run's units of work."""

from __future__ import annotations

import csv
from io import StringIO
import re


ARM_LABELS = {
    "first": "First paper", "three": "Choose among three",
    "none": "No library", "whole": "Whole programs", "routines": "Extracted routines",
    "direct": "Direct fallback", "gateway": "Gateway fallback",
    "tfidf_tfidf": "TF–IDF at both stages", "tfidf_coverage": "Change sentence selection",
    "bm25_tfidf": "Change document ranking", "bm25_coverage": "Change both stages",
    "pool": "Pool both readings", "agreement": "Require agreement",
    "TaskQueue": "Task cursor", "ObligationQueue": "Obligation records",
    "text": "Text search", "graph": "Graph traversal", "identifier": "Exact identifier",
    "caller_fallback": "Caller fallback", "gateway_fallback": "Gateway fallback", "primary_only": "Primary only",
    "ordinary_register": "Versioned register", "linked_register": "Linked register",
    "conventional": "Conventional", "full_governed": "Governed",
    "conventional_status": "Conventional status", "additional_observation": "Additional observation",
    "additional_endpoint": "Additional endpoint", "matched_conventional_access": "One endpoint with matched access",
    "bound_handoff": "Retained qualification", "no_library": "No library",
    "ordinary_retrieval": "Ordinary retrieval", "reusable_routines": "Extracted routines",
    "aware_whole": "Query-aware whole", "aware_routine": "Query-aware routine",
    "blind_whole": "Query-blind whole", "blind_routine": "Query-blind routine",
    "conventional_memoization": "Conventional memoization",
    "retained_qualification": "Serialized handoff",
    "cached_permission_only": "Cached permission",
    "transactional_memo": "Version-checked transaction",
    "transactional_receipt": "Transaction with serialized receipt",
}


def study_arm_label(key: str) -> str:
    arm, _, scheduler = key.partition("__")
    return f"{ARM_LABELS[arm]} · {scheduler.replace('-', ' ')}" if scheduler else ARM_LABELS[arm]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def location(*parts):
    return "/" + "/".join(str(part).replace("~", "~0").replace("/", "~1") for part in parts)


def case(case_id, condition, arms, *, pointers, exhausted=False, adverse=False):
    outcome_signatures = {value["signature"] for value in arms.values()}
    return {
        "id": slug(case_id), "condition": condition, "arms": arms, "pointers": list(pointers),
        "disagrees": len(outcome_signatures) > 1,
        "exhausted": exhausted, "adverse": adverse,
    }


def arm(outcome, work, signature):
    return {"outcome": outcome, "work": work, "signature": signature}


def scoped_git(result):
    by_case, pointers = {}, {}
    for index, row in enumerate(result["trials"]):
        pointers.setdefault(row["path"], []).append(location("trials", index))
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
        yield case(name, name.replace("_", " "), arms, pointers=pointers[name], adverse=any(
            row["false_block"] or row["unauthorized_terminal_change"] or row["unresolved_terminal_state"]
            for row in trials.values()
        ))


def authority_ordering(result):
    for index, row in enumerate(result["cases"]):
        arms = {}
        for name, observation in row["arms"].items():
            effect = observation["effect"]
            order = (f'Commit tick {effect["tick"]}, used revision {effect["used_revision"]}'
                     if effect else "No committed effect")
            order += f'; observed revision {observation["revision_at_observation"]}'
            arms[name] = arm(observation["outcome"], order, observation["outcome"])
        identity = row["case"]
        yield case(identity, identity.replace("_", " "), arms, pointers=[location("cases", index)],
                   adverse=any(observation["outcome"] == "unauthorized" for observation in row["arms"].values()))


def crossed_receiver(result):
    for index, row in enumerate(result["pairs"]):
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
        yield case(condition, condition, arms, pointers=[location("pairs", index)], adverse=any(
            receipt["false_closure"] or receipt["wrongful_block"] or receipt["effect_commits"] > 1
            or receipt.get("observed_effect") == "wrong_effect" for receipt in row["arms"].values()
        ))


def verifier_rollout(result):
    for index, pair in enumerate(result["pairs"]):
        for position, (expected, ordinary, retained) in enumerate(zip(
            pair["expected_routes"], pair["arms"]["conventional"], pair["arms"]["bound_handoff"], strict=True
        )):
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
            pointers = [location("pairs", index, "expected_routes", position),
                        *(location("pairs", index, "arms", name, position) for name in ("conventional", "bound_handoff"))]
            yield case(name, condition, arms, pointers=pointers, adverse=any(row["route"] != expected for row in (ordinary, retained)))


def receiver_availability(result):
    for index, pair in enumerate(result["pairs"]):
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
        yield case(f'pair-{pair["id"]:03}', condition, arms, pointers=[location("pairs", index)],
                   adverse=pair["initial_state"] in {"wrong_effect", "repeat_effect"})


def verifier_policy_audit(result):
    for index, profile in enumerate(result["cases"]):
        names = tuple(profile["arms"])
        for position, decisions in enumerate(zip(*(profile["arms"][name]["decisions"] for name in names), strict=True)):
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
            pointers = [location("cases", index, "arms", name, "decisions", position) for name in names]
            yield case(label, label, arms, pointers=pointers, adverse=any(row["route"] != row["expected"] for row in decisions))


def verifier_freshness(result):
    for index, profile in enumerate(result["cases"]):
        names = tuple(profile["arms"])
        for position, decisions in enumerate(zip(*(profile["arms"][name]["decisions"] for name in names), strict=True)):
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
            pointers = [location("cases", index, "arms", name, "decisions", position) for name in names]
            yield case(identity, label, arms, pointers=pointers, adverse=any(row["route"] != first["expected_route"] for row in decisions))


def synthesis_case_records(result, factorial):
    key = "cases" if factorial else "tasks"
    for index, row in enumerate(result[key]):
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
        yield case(name, condition, arms, pointers=[location(key, index)],
                   exhausted=any(item["terminal"].endswith("budget_exhausted") for item in outcomes.values()),
                   adverse=row["family"] in {"out-of-family", "adverse-mixing"})


def package_cases(result, transport):
    key = "conditions" if transport else "cases"
    for index, observation in enumerate(result["observations"]):
        name = observation["package" if transport else "name"]
        for condition, trials in observation["conditions" if transport else "cases"].items():
            arms = {}
            methods = ("caller_fallback", "gateway_fallback") if transport else ("primary_only", "caller_fallback", "gateway_fallback")
            for method in methods:
                trial = trials[method]
                if transport:
                    outcome = "verified" if trial["verified"] else "unresolved"
                    work = (f'{trial["caller_http_requests"]} caller requests, '
                            f'{trial["http_response_bytes_all_hops"]} HTTP response bytes across hops')
                else:
                    outcome = trial["disposition"]
                    work = (f'{trial["caller_requests"]} caller requests, {trial["response_body_bytes"]} body bytes, '
                            f'{trial["gateway_envelope_bytes"]} modeled envelope bytes')
                arms[method] = arm(outcome, work, (outcome, trial["false_closure"]))
            yield case(f"{name}-{condition}", f'{name}@{observation["version"]}, {condition}', arms,
                       pointers=[location("observations", index, key, condition)], adverse=condition in {"wrong_body", "both_unavailable"})


def review_cases(result):
    tasks, pointers = {}, {}
    for index, packet in enumerate(result["packets"]):
        pointers.setdefault(packet["id"], []).append(location("packets", index))
        trial = packet["result"]
        outcomes = tuple(trial[field] for field in ("decision_ok", "citation", "scoped"))
        labels = ("correct decision with facts", "usable citation", "scope credit")
        description = ", ".join(f"{label}: {value}" for label, value in zip(labels, outcomes))
        tasks.setdefault(packet["id"], {})[packet["comparison"]] = arm(
            description, f'{len(packet["path"])} records opened', outcomes)
    for task, arms in tasks.items():
        yield case(task, ("Claim review " if task.startswith("C") else "Navigation ") + task,
                   {name: arms[name] for name in ("ordinary_register", "linked_register")}, pointers=pointers[task])


def arrival_cases(result):
    for rate, queues in result.items():
        for point in ("last_arrival", "tick_15", "drain"):
            arms = {}
            for name, reports in queues.items():
                report = reports[point]
                counts = tuple(report[k] for k in ("verified", "rejected", "unsupported", "unresolved_checks"))
                outcome = "{} verified, {} rejected, {} unsupported, {} pending checks".format(*counts)
                work = f'{report["writes"]} state writes, mean wait among finished jobs {report["mean_finished_wait"]} ticks'
                arms[name] = arm(outcome, work, counts)
            yield case(f"{rate}-{point}", f'{rate} jobs per tick, {point.replace("_", " ")}', arms, pointers=[location(rate, name, point) for name in arms])


def revision_cases(result):
    groups, pointers = {}, {}
    for index, trial in enumerate(result["trials"]):
        key = trial["subject"], trial["identified"], trial["question"]
        pointers.setdefault(key, []).append(location("trials", index))
        scores = tuple(trial[metric] for metric in ("decision", "citation", "scope"))
        outcome = "decision {}, citation {}, scope {}".format(*scores)
        opens = ", ".join(row["id"] for row in trial["packet"])
        groups.setdefault(key, {})[trial["method"]] = arm(outcome, opens, scores)
    for (subject, identified, question), arms in groups.items():
        expected = {"graph", "text", "identifier"} if identified else {"graph", "text"}
        if set(arms) != expected:
            raise ValueError(f"missing or ineligible retrieval arm for {subject}: {set(arms)}")
        yield case(f"{subject}-{'id' if identified else 'wording'}", question, arms, pointers=pointers[subject, identified, question])


def citation_cases(result):
    for index, sample in enumerate(result["cases"]):
        for user in ("triage", "publication"):
            arms = {}
            for name in ("pool", "agreement"):
                verdict, grade = sample[f"{name}_{user}"]
                arms[name] = arm(f"{verdict} · {grade}", "Two shared model readings", (verdict, grade))
            yield case(f"{sample['id']}-{user}", f"SciFact claim {sample['id']} · {user}", arms, pointers=[location("cases", index)],
                       adverse=any(sample[f"{name}_{user}"][1] == "unsupported" for name in arms))


def fresh_retrieval_cases(result):
    for index, record in enumerate(result["cases"]):
        arms = {}
        for name, row in record["arms"].items():
            span = ", ".join(map(str, row["cited"]))
            outcome = f'{row["verdict"]} · {row["outcome"]} · paper {row["doc"]}, sentences {span}'
            work = f'2 readings, {row["tokens"]} input tokens, {row["sentences_ranked"]} candidate sentences'
            arms[name] = arm(outcome, work, (row["verdict"], row["outcome"], row["doc"], tuple(row["cited"])))
        yield case(str(record["id"]), f'SciFact-Open claim {record["id"]}', arms, pointers=[location("cases", index)],
                   adverse=any(v["outcome"] == "unsupported" for v in record["arms"].values()))


def publication_cases(result):
    for index, record in enumerate(result["cases"]):
        arms = {}
        for name in ("primary_only", "direct", "gateway"):
            row = record["arms"][name]
            outcome = ("Verified" if row["truth"] else "False closure") if row["closed"] else "Unresolved"
            work = (f'{row["caller_requests"]} caller / {row["requests"]} total requests, '
                    f'{row["body_bytes"]} body bytes, {row["elapsed_ns"]/1000:.1f} µs to decision')
            arms[name] = arm(outcome, work, outcome)
        yield case(record["id"], f'{record["task"]} · {record["effect"]} · primary {record["primary"]} · {record["fallback"]}',
                   arms, pointers=[location("cases", index)],  adverse=any(row["closed"] and not row["truth"] for row in record["arms"].values()))


def sygus_cases(result):
    groups, pointers = {}, {}
    for index, row in enumerate(result["cases"]):
        key = row["family"], row["task"], row["schedule"]
        arms = groups.setdefault(key, {})
        pointers.setdefault(key, []).append(location("cases", index))
        outcome = row["solution"] or row["stop"]
        work = (f'{row["proposals"]:,} proposals, {row["screen_ops"]:,} primitive evaluations, '
                f'{row["solver_checks"]} universal checks; search {row["search_ns"]/1e9:.3f} s, '
                f'verification {row["verify_ns"]/1e9:.3f} s')
        arms[row["arm"]] = arm(outcome, work, row["stop"])
    for (family, task, schedule), arms in groups.items():
        yield case(f"{task}-{schedule}", f"{family} · {task} · {schedule}", arms,
                   pointers=pointers[family, task, schedule],
                   exhausted=any("cap" in v["outcome"] for v in arms.values()))


def rows_for(format_id, result):
    if format_id == "three_papers":
        rows = [case(str(r["id"]), "Fresh claim "+str(r["id"]), {
            k:arm(a["outcome"], f'{a["readings"]} readings, {a["tokens"]} tokens; paper {a["doc"]}, sentences {a["cited"]}',a["outcome"])
            for k,a in r["arms"].items()}, pointers=[location("cases", index)], adverse=any(a["outcome"]=="unsupported" for a in r["arms"].values())) for index, r in enumerate(result["cases"])]
    elif format_id == "sygus_external":
        rows = sygus_cases(result)
    elif format_id == "matched_publication":
        rows = publication_cases(result)
    elif format_id == "verification_arrivals":
        rows = arrival_cases(result)
    elif format_id == "fresh_retrieval":
        rows = fresh_retrieval_cases(result)
    elif format_id == "scifact_citation":
        rows = citation_cases(result)
    elif format_id == "revision_retrieval":
        rows = revision_cases(result)
    elif format_id in {"package_observation", "package_transport"}:
        rows = package_cases(result, format_id == "package_transport")
    elif format_id == "review_packet":
        rows = review_cases(result)
    elif format_id == "scoped_git_v1":
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
    if format_id != "revision_retrieval" and any(tuple(row["arms"]) != tuple(ordered[0]["arms"]) for row in ordered):
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
