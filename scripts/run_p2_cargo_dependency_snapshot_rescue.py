#!/usr/bin/env python3
"""Execute the frozen two-materialization Cargo dependency rescue and task arms."""

from __future__ import annotations

import __future__,argparse,gzip,hashlib,json,math,re,shutil,sys,time,types,uuid
try:
 import tomllib
except ModuleNotFoundError:
 import tomli as tomllib
from datetime import datetime,timezone
from pathlib import Path

from run_p2_gold_preflight import execute_arm,load_selected_rows,run,run_monitored_container,sha256_file,sha256_text

ROOT=Path(__file__).resolve().parents[1];SOURCE=Path('/tmp/swe-rebench-v2.parquet');HARNESS=Path('/tmp/swe-rebench-v2-code.7ixeFl')
SOURCE_SHA='0e0bf9355f892ad74ae98d4e1c404f39fd6654a8e351ee3e6ab162e4a64cd3ad';HARNESS_COMMIT='c71902a8cf8d2b725f63d51f199f4d3e56f68d2d'
POLICY=ROOT/'evidence_quality/p2_dependency_snapshot_rescue_policy.json';CAL=ROOT/'evidence_quality/p2_independent_test_log_evaluator_calibration.json';RESOURCE=ROOT/'evidence_quality/p2_resource_ceiling.json'

def gz(path:Path,text:str)->str:
 path.parent.mkdir(parents=True,exist_ok=True)
 with gzip.open(path,'wt',encoding='utf-8',compresslevel=9) as f:f.write(text)
 return hashlib.sha256(path.read_bytes()).hexdigest()

def monitored(image:str,name:str,network:str,command:str,timeout:int,workdir='/minijinja'):
 args=['docker','run','--name',name,'--network',network,'--platform','linux/amd64','--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','2048','--memory','8g','--cpus','6','--tmpfs','/tmp:rw,nosuid,nodev,exec,size=2g','-w',workdir,image,'/bin/bash','-lc',command]
 start=time.monotonic();proc,monitor=run_monitored_container(args,container_name=name,timeout=timeout);return proc,monitor,time.monotonic()-start

def virtual_upper(image_id:str)->tuple[str|None,int|None]:
 p=run('docker','system','df','-v','--format','{{json .}}');data=json.loads(p.stdout) if p.returncode==0 else {};row=next((x for x in data.get('Images',[]) if x.get('ID')==image_id),None)
 if not row:return None,None
 value=row['Size'];m=re.fullmatch(r'([0-9]+(?:\.([0-9]+))?)([kMGT]?B)',value)
 if not m:return value,None
 digits=len(m.group(2) or '');factor={'B':1,'kB':1000,'MB':1000**2,'GB':1000**3,'TB':1000**4}[m.group(3)];half=0 if digits==0 else .5*10**(-digits)
 return value,math.ceil((float(m.group(1))+half)*factor)

def stabilized_cleanup(host_before:int,ceiling:dict)->dict:
 samples=[];deadline=time.monotonic()+ceiling['cleanup_stabilization_timeout_seconds'];stable=False
 while True:
  free=shutil.disk_usage('/').free;df=run('docker','system','df','--format','{{json .}}');rows=[json.loads(x) for x in df.stdout.splitlines() if x.strip()] if df.returncode==0 else []
  zero=bool(rows) and all(str(x.get('Size'))=='0B' and str(x.get('TotalCount'))=='0' for x in rows)
  samples.append({'free_bytes':free,'docker_zero':zero})
  recent=samples[-ceiling['cleanup_stabilization_required_consecutive_samples']:]
  if len(recent)==ceiling['cleanup_stabilization_required_consecutive_samples'] and all(x['docker_zero'] for x in recent) and max(x['free_bytes'] for x in recent)-min(x['free_bytes'] for x in recent)<=ceiling['cleanup_stabilization_max_sample_delta_bytes']:
   stable=True;break
  if time.monotonic()>=deadline:break
  time.sleep(ceiling['cleanup_stabilization_sample_interval_seconds'])
 final=samples[-1]['free_bytes'];return {'stable':stable,'samples':samples,'host_free_after_bytes':final,'host_free_byte_loss':max(0,host_before-final)}

def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--instance-id', default='mitsuhiko__minijinja-794')
    argument_parser.add_argument('--attempt-id', default='2026-07-17-slot1-rank1-cargo-snapshot-r2')
    argument_parser.add_argument('--opening', default='evidence_quality/p2_replacement_task_opening.json')
    argument_parser.add_argument('--provenance', default='evidence_quality/p2_replacement_provenance_preflight.json')
    argument_parser.add_argument('--output-family', default='replacement_qualification')
    args = argument_parser.parse_args()
    INSTANCE = args.instance_id
    ATTEMPT = args.attempt_id
    OUT = ROOT / 'experiments/p2_governed_repository_admission' / args.output_family / 'attempts' / ATTEMPT
    opening_path = ROOT / args.opening
    provenance_path = ROOT / args.provenance
    if OUT.exists():
        raise SystemExit("immutable attempt exists")
    OUT.mkdir(parents=True)

    policy = json.loads(POLICY.read_text())
    opening = json.loads(opening_path.read_text())
    provenance = json.loads(provenance_path.read_text())
    calibration = json.loads(CAL.read_text())
    resource = json.loads(RESOURCE.read_text())
    ceiling = resource["task_acceptance_ceilings"]
    if policy["state"] != "frozen_before_first_network_materialization_rescue":
        raise SystemExit("rescue policy identity drift")

    opened = opening.get("candidate") or next(row for row in opening["candidates"] if row["instance_id"] == INSTANCE)
    receipt = provenance.get("candidate") or next(row for row in provenance["candidates"] if row["instance_id"] == INSTANCE)
    if opened["instance_id"] != INSTANCE or receipt["instance_id"] != INSTANCE:
        raise SystemExit("opening/provenance instance drift")
    spec = load_selected_rows(SOURCE, {INSTANCE})[INSTANCE]
    workdir = '/' + spec['repo'].split('/', 1)[1]
    if spec['install_config']['log_parser'] != 'parse_log_cargo':
        raise SystemExit('Cargo rescue invoked for a non-Cargo task')
    if (sha256_text(spec['problem_statement'] or '') != opened['problem_statement_sha256']
            or sha256_text(spec['patch'] or '') != opened['solution_patch_sha256']
            or sha256_text(spec['test_patch'] or '') != opened['test_patch_sha256']):
        raise SystemExit('opened task digest drift')
    image = receipt["image_manifest"]["image"]
    digest = receipt["image_manifest"]["digest"]
    base = image.split(":", 1)[0] + "@" + digest
    host_before = shutil.disk_usage("/").free
    result = {
        "schema_version": "asi_stack.p2_cargo_dependency_snapshot_rescue.v2",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "attempt_id": ATTEMPT,
        "instance_id": INSTANCE,
        "slot": opened["slot"],
        "rank": opened["rank"],
        "state": "running",
        "policy_path": "evidence_quality/p2_dependency_snapshot_rescue_policy.json",
        "opening_path": args.opening,
        "provenance_path": args.provenance,
        "base_image_ref": base,
        "base_manifest_digest": digest,
        "source_parquet_sha256": SOURCE_SHA,
        "upstream_harness_commit": HARNESS_COMMIT,
        "independent_evaluator_sha256": calibration["independent_evaluator_sha256"],
        "host_free_before_bytes": host_before,
        "materializations": [],
        "runs": [],
        "candidate_test_outcome_opened": False,
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    cleanup_refs = []
    active_containers = set()
    terminal = ["n0_instrument_failure", "unhandled_runner_exception", "runner did not reach a classified terminal state"]

    def set_terminal(state, code, detail):
        terminal[:] = [state, code, detail]

    try:
        if sha256_file(SOURCE) != SOURCE_SHA or run("git", "-C", str(HARNESS), "rev-parse", "HEAD").stdout.strip() != HARNESS_COMMIT:
            set_terminal("n0_instrument_failure", "source_or_harness_drift", "pinned input drift")
            return
        if host_before < ceiling["minimum_host_free_bytes_before_task"]:
            set_terminal("n0_resource_failure", "host_free_below_minimum", "base image pull not attempted")
            return

        pull_start = time.monotonic()
        pull = run("docker", "pull", "--platform", "linux/amd64", base, timeout=ceiling["image_pull_seconds"])
        pull_wall = time.monotonic() - pull_start
        pull_log = OUT / "pull.log.gz"
        result["pull"] = {
            "exit_code": pull.returncode,
            "wall_seconds": round(pull_wall, 6),
            "log_path": pull_log.relative_to(ROOT).as_posix(),
            "log_sha256": gz(pull_log, (pull.stdout or "") + (pull.stderr or "")),
        }
        cleanup_refs.append(base)
        if pull.returncode or pull_wall > ceiling["image_pull_seconds"]:
            set_terminal("n0_resource_failure", "base_pull_failed", "base image unavailable within frozen ceiling")
            return

        lock_proc = run(
            "docker", "run", "--rm", "--network", "none", "--platform", "linux/amd64",
            "-w", workdir, base, "/bin/bash", "-lc",
            "set -e; sha256sum Cargo.lock; cat Cargo.lock; printf '\\n__P2_CONFIGS__\\n'; "
            "find . -path '*/.cargo/config*' -type f -print -exec cat {} \\;",
        )
        lock_text = lock_proc.stdout or ""
        lock_log = OUT / "pre_network_lock_and_config.log.gz"
        result["pre_network"] = {
            "exit_code": lock_proc.returncode,
            "log_path": lock_log.relative_to(ROOT).as_posix(),
            "log_sha256": gz(lock_log, lock_text + (lock_proc.stderr or "")),
        }
        try:
            lock_part = lock_text.split("\n__P2_CONFIGS__\n", 1)[0].split("\n", 1)[1]
            packages = tomllib.loads(lock_part).get("package", [])
        except Exception as exc:
            set_terminal("n0_construct_failure", "cargo_lock_parse_failure", str(exc))
            return

        registry = [p for p in packages if str(p.get("source", "")).startswith("registry+")]
        git = [p for p in packages if str(p.get("source", "")).startswith("git+")]
        unknown = [p for p in packages if p.get("source") and not str(p["source"]).startswith(("registry+", "git+"))]
        bad_registry = [p for p in registry if len(str(p.get("checksum", ""))) != 64]
        bad_git = [p for p in git if "#" not in str(p.get("source", "")) or len(str(p["source"]).rsplit("#", 1)[-1]) < 40]
        config_part = lock_text.split("\n__P2_CONFIGS__\n", 1)[1] if "\n__P2_CONFIGS__\n" in lock_text else ""
        result["lock_audit"] = {
            "package_count": len(packages),
            "registry_package_count": len(registry),
            "git_package_count": len(git),
            "unknown_source_count": len(unknown),
            "registry_missing_checksum_count": len(bad_registry),
            "git_missing_exact_commit_count": len(bad_git),
            "custom_source_config_detected": any(token in config_part for token in ("replace-with", "registries.", "source.")),
        }
        if lock_proc.returncode or unknown or bad_registry or bad_git or result["lock_audit"]["custom_source_config_detected"]:
            set_terminal("n0_construct_failure", "lock_or_source_allowlist_failure", "Cargo dependency identities are not fully checksum/commit bound")
            return

        expected_archives = {f"{p['name']}-{p['version']}.crate": p["checksum"] for p in registry}
        expected_path = OUT / "expected_registry_archives.json"
        expected_path.write_text(json.dumps(expected_archives, sort_keys=True) + "\n")
        result["expected_registry_archives"] = {
            "count": len(expected_archives),
            "path": expected_path.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(expected_path),
        }
        expected_git = sorted({p["source"] for p in git})
        expected_git_path = OUT / "expected_git_sources.json"
        expected_git_path.write_text(json.dumps(expected_git, sort_keys=True) + "\n")
        result["expected_git_sources"] = {
            "count": len(expected_git),
            "path": expected_git_path.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(expected_git_path),
        }
        inventories = []
        derived = []
        inventory_cmd = """python3 - <<'PY'
import glob, hashlib, json, os, pathlib, subprocess, sys
expected = json.load(open('/p2/expected.json'))
expected_git = json.load(open('/p2/expected_git.json'))
root = os.environ.get('CARGO_HOME', os.path.expanduser('~/.cargo')) + '/registry/cache'
by = {}
for path in glob.glob(root + '/**/*.crate', recursive=True):
    by.setdefault(os.path.basename(path), []).append(path)
rows = []
bad = False
for name in sorted(expected):
    paths = by.get(name, [])
    if len(paths) != 1:
        rows.append({'name': name, 'state': 'missing_or_duplicate', 'count': len(paths)})
        bad = True
        continue
    path = paths[0]
    actual = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    state = 'match' if actual == expected[name] else 'checksum_mismatch'
    bad = bad or state != 'match'
    rows.append({'kind': 'registry_archive', 'identity': name, 'relative_path': os.path.basename(path), 'size': os.path.getsize(path), 'sha256': actual, 'state': state})
metadata_proc = subprocess.run(['cargo', 'metadata', '--locked', '--offline', '--format-version', '1'], capture_output=True, text=True)
if metadata_proc.returncode:
    rows.append({'kind': 'cargo_metadata', 'state': 'failed', 'exit_code': metadata_proc.returncode})
    bad = True
else:
    metadata = json.loads(metadata_proc.stdout)
    observed_git = sorted({p.get('source') for p in metadata['packages'] if str(p.get('source', '')).startswith('git+')})
    if observed_git != expected_git:
        rows.append({'kind': 'git_source_set', 'state': 'mismatch', 'expected': expected_git, 'observed': observed_git})
        bad = True
    roots = {}
    for package in metadata['packages']:
        source = package.get('source') or ''
        if source in expected_git:
            root = pathlib.Path(package['manifest_path']).parent
            roots[(source, str(root))] = root
    for (source, root_text), package_root in sorted(roots.items()):
        expected_commit = source.rsplit('#', 1)[-1]
        revision = subprocess.run(['git', '-C', str(package_root), 'rev-parse', 'HEAD'], capture_output=True, text=True)
        actual_commit = revision.stdout.strip()
        if revision.returncode or actual_commit != expected_commit:
            rows.append({'kind': 'git_checkout', 'identity': source, 'relative_path': '.', 'state': 'commit_mismatch', 'expected_commit': expected_commit, 'actual_commit': actual_commit})
            bad = True
            continue
        for path in sorted(package_root.rglob('*')):
            if not path.is_file() or '.git' in path.parts or 'target' in path.parts:
                continue
            relative = path.relative_to(package_root).as_posix()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            rows.append({'kind': 'git_source_file', 'identity': source, 'relative_path': relative, 'size': path.stat().st_size, 'sha256': digest, 'state': 'match'})
for row in rows:
    print(json.dumps(row, sort_keys=True, separators=(',', ':')))
sys.exit(2 if bad else 0)
PY"""

        for label in ("a", "b"):
            name = f"p2-cargo-{label}-{uuid.uuid4().hex[:10]}"
            active_containers.add(name)
            proc, monitor, wall = monitored(
                base, name, "bridge", "set -e\ngit reset --hard HEAD\ncargo fetch --locked",
                ceiling["dependency_materialization_seconds"], workdir,
            )
            log = OUT / f"materialization_{label}.log.gz"
            entry = {
                "label": label,
                "container_name": name,
                "network": "bridge_dependency_fetch_only",
                "task_patch_applied": False,
                "exit_code": proc.returncode,
                "wall_seconds": round(wall, 6),
                "resource_monitor": monitor,
                "log_path": log.relative_to(ROOT).as_posix(),
                "log_sha256": gz(log, (proc.stdout or "") + (proc.stderr or "")),
            }
            if proc.returncode or wall > ceiling["dependency_materialization_seconds"] or monitor["timed_out"] or monitor.get("monitor_error_count", 0):
                result["materializations"].append(entry)
                set_terminal("n0_dependency_failure", "network_materialization_failure", f"materialization {label} failed")
                return

            safe_repo = re.sub(r'[^a-z0-9_.-]+', '-', spec['repo'].lower())
            ref = f"p2-local/{safe_repo}:{ATTEMPT}-{label}"
            commit = run("docker", "commit", name, ref)
            run("docker", "rm", "-f", name)
            active_containers.discard(name)
            cleanup_refs.append(ref)
            derived.append(ref)
            inspect = run("docker", "image", "inspect", ref, "--format", "{{json .}}")
            info = json.loads(inspect.stdout) if inspect.returncode == 0 else {}
            virtual_display, virtual_bound = virtual_upper(info.get("Id", ""))
            entry.update({
                "commit_exit_code": commit.returncode,
                "derived_ref": ref,
                "derived_image_id": info.get("Id"),
                "engine_content_size_bytes": info.get("Size"),
                "virtual_size_display": virtual_display,
                "virtual_size_conservative_upper_bound_bytes": virtual_bound,
            })
            if (
                commit.returncode or inspect.returncode
                or info.get("Size", 10**30) > ceiling["engine_content_size_bytes"]
                or virtual_bound is None
                or virtual_bound > ceiling["virtual_size_conservative_upper_bound_bytes"]
            ):
                result["materializations"].append(entry)
                set_terminal("n0_resource_failure", "derived_image_size_or_commit_failure", f"derived image {label} failed the frozen resource gate")
                return

            verify_name = f"p2-cargo-offline-{label}-{uuid.uuid4().hex[:8]}"
            active_containers.add(verify_name)
            verify, verify_monitor, verify_wall = monitored(
                ref, verify_name, "none", "set -e\ngit reset --hard HEAD\ncargo fetch --locked --offline",
                ceiling["dependency_materialization_seconds"], workdir,
            )
            run("docker", "rm", "-f", verify_name)
            active_containers.discard(verify_name)
            verify_log = OUT / f"offline_verify_{label}.log.gz"
            entry["offline_verify"] = {
                "exit_code": verify.returncode,
                "wall_seconds": round(verify_wall, 6),
                "resource_monitor": verify_monitor,
                "log_path": verify_log.relative_to(ROOT).as_posix(),
                "log_sha256": gz(verify_log, (verify.stdout or "") + (verify.stderr or "")),
            }
            inventory = run(
                "docker", "run", "--rm", "--network", "none", "--platform", "linux/amd64",
                "-v", f"{expected_path}:/p2/expected.json:ro",
                "-v", f"{expected_git_path}:/p2/expected_git.json:ro",
                "-w", workdir, ref, "/bin/bash", "-lc", inventory_cmd,
                timeout=ceiling["dependency_materialization_seconds"],
            )
            inventory_text = inventory.stdout or ""
            inventory_log = OUT / f"inventory_{label}.jsonl.gz"
            inventory_sha = hashlib.sha256(inventory_text.encode()).hexdigest()
            entry["inventory"] = {
                "scope": "lockfile_registry_archives_plus_exact_commit_git_source_files",
                "exit_code": inventory.returncode,
                "entry_count": len(inventory_text.splitlines()),
                "normalized_sha256": inventory_sha,
                "log_path": inventory_log.relative_to(ROOT).as_posix(),
                "log_sha256": gz(inventory_log, inventory_text + (inventory.stderr or "")),
            }
            inventories.append(inventory_sha)
            result["materializations"].append(entry)
            if verify.returncode or verify_wall > ceiling["dependency_materialization_seconds"] or verify_monitor["timed_out"] or verify_monitor.get("monitor_error_count", 0) or inventory.returncode:
                set_terminal("n0_dependency_failure", "offline_replay_or_inventory_failure", f"derived image {label} failed offline replay or checksum inventory")
                return

        result["inventory_exact_agreement"] = inventories[0] == inventories[1]
        if not result["inventory_exact_agreement"]:
            set_terminal("n0_dependency_failure", "independent_inventory_disagreement", "two independently materialized dependency snapshots differ")
            return

        sys.path.insert(0, str(HARNESS))
        sys.path.insert(0, str(HARNESS / "lib"))
        parser_source = HARNESS / "lib/agent/log_parsers.py"
        upstream = types.ModuleType("p2_cargo_rescue_upstream")
        upstream.__file__ = str(parser_source)
        exec(compile(parser_source.read_text(), str(parser_source), "exec", flags=__future__.annotations.compiler_flag), upstream.__dict__)
        parser_fn = upstream.NAME_TO_PARSER[spec["install_config"]["log_parser"]]

        for repetition in (1, 2):
            for arm, solution in (("baseline_test_patch_only", None), ("human_gold_plus_test_patch", spec["patch"])):
                row = execute_arm(
                    spec=spec, image_ref=derived[0], parser=parser_fn, solution_patch=solution,
                    test_patch=spec["test_patch"], arm=arm, repetition=repetition,
                    timeout_seconds=ceiling["arm_wall_seconds"], write_logs=True,
                    log_subdir=f"{args.output_family}/attempts/{ATTEMPT}/logs",
                    independent_parser_name=spec["install_config"]["log_parser"],
                )
                monitor = row["resource_monitor"]
                row["resource_gates"] = {
                    "wall": row["duration_seconds"] <= ceiling["arm_wall_seconds"],
                    "sample": row["duration_seconds"] < 3 or monitor["sample_count"] >= 1,
                    "monitor_error_free": monitor.get("monitor_error_count", 0) == 0,
                    "timeout": not monitor["timed_out"],
                    "memory": monitor["peak_memory_bytes"] <= ceiling["peak_memory_bytes"],
                    "cpu": monitor["max_cpu_percent"] <= ceiling["max_cpu_percent"],
                    "cpu_seconds": monitor["integrated_cpu_seconds_estimate"] <= ceiling["integrated_cpu_seconds_estimate"],
                    "pids": monitor["peak_pids"] <= ceiling["peak_pids"],
                }
                row["resource_gate_pass"] = all(row["resource_gates"].values())
                row["compressed_log_sha256"] = sha256_file(ROOT / row["compressed_log_path"])
                result["runs"].append(row)
                (OUT / "checkpoint.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        passed = len(result["runs"]) == 4 and all(
            row["pass"] and row["dual_evaluator_exact_agreement"] and row["resource_gate_pass"]
            for row in result["runs"]
        )
        set_terminal(
            "qualified" if passed else "n0_construct_instrument_or_resource_failure",
            "all_gates_passed" if passed else "paired_outcome_gate_failure",
            "two independent dependency snapshots and four paired arms complete",
        )
    except Exception as exc:
        set_terminal("n0_instrument_failure", "unhandled_runner_exception", f"{type(exc).__name__}: {exc}")
    finally:
        container_cleanup = []
        for name in sorted(active_containers):
            proc = run("docker", "rm", "-f", name)
            container_cleanup.append({"name": name, "exit_code": proc.returncode, "output_sha256": sha256_text((proc.stdout or "") + (proc.stderr or ""))})
        image_cleanup = []
        for ref in reversed(cleanup_refs):
            proc = run("docker", "image", "rm", "-f", ref)
            image_cleanup.append({"ref": ref, "exit_code": proc.returncode, "output_sha256": sha256_text((proc.stdout or "") + (proc.stderr or ""))})
        stabilization = stabilized_cleanup(host_before, ceiling)
        result["cleanup"] = {"container_removals": container_cleanup, "image_removals": image_cleanup, "stabilization": stabilization}
        state, code, detail = terminal
        if state == "qualified" and (
            not stabilization["stable"]
            or stabilization["host_free_byte_loss"] > ceiling["maximum_post_cleanup_host_free_byte_loss"]
            or any(row["exit_code"] for row in container_cleanup + image_cleanup)
        ):
            state = "n0_resource_failure"
            code = "cleanup_stabilization_or_residual_failure"
            detail = "paired arms passed but the frozen cleanup resource gate failed"
        all_runs_pass = len(result["runs"]) == 4 and all(
            row.get("pass") and row.get("dual_evaluator_exact_agreement") and row.get("resource_gate_pass")
            for row in result["runs"]
        )
        result.update({
            "state": state,
            "terminal_code": code,
            "terminal_detail": detail,
            "host_free_after_bytes": stabilization["host_free_after_bytes"],
            "host_free_byte_loss": stabilization["host_free_byte_loss"],
            "candidate_test_outcome_opened": bool(result["runs"]),
            "all_runs_pass": all_runs_pass,
            "qualified_replacement": state == "qualified" and all_runs_pass,
        })
        (OUT / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(f"{INSTANCE}: {state} {code}", flush=True)

if __name__=='__main__':main()
