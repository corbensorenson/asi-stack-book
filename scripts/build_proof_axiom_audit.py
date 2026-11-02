"""Query Lean's transitive axiom dependencies for every source theorem."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import tempfile

from validation_runtime import execute_guarded, identity
from admission_guard import ordinary

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "proofs/axiom_dependencies.json"
TOOL = ROOT / "lean/tools/AxiomDependencies.lean"
SOURCE_DECLARATION = re.compile(r"(?m)^[ \t]*(?:private\s+)?(?:theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_']*)")
DECLARATION_HEAD = re.compile(r"(?m)^[ \t]*(?:@\[[^\n]*?\]\s*)*(?:(?:private|protected|public)\s+)?(?:theorem|lemma)\s+(\S+)")
STANDARD_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def input_paths() -> list[str]:
    paths = [*sorted((ROOT / "lean/AsiStackProofs").glob("*.lean")),
             ROOT / "lean/AsiStackProofs.lean", TOOL, ROOT / "lean/lean-toolchain",
             ROOT / "lean/lakefile.lean", ROOT / "lean/lake-manifest.json",
             ROOT / "scripts/build_proof_axiom_audit.py", ROOT / "scripts/validation_runtime.py",
             ROOT / "scripts/admission_guard.py"]
    return [str(path.relative_to(ROOT)) for path in paths]


def classify(axiom: str) -> str:
    if axiom in STANDARD_AXIOMS:
        return "standard_logic"
    if "._native.native_decide.ax" in axiom or "._native.bv_decide.ax" in axiom or axiom == "Lean.trustCompiler":
        return "native_compiler_trust"
    return "unreviewed_axiom"


def source_declarations(text: str) -> list:
    declarations = list(SOURCE_DECLARATION.finditer(text))
    heads = list(DECLARATION_HEAD.finditer(text))
    if Counter(row.group(1) for row in heads) != Counter(row.group(1) for row in declarations):
        raise ValueError('unsupported source theorem syntax; review the source-to-environment resolver rather than silently omitting declarations')
    return declarations


def assemble(environment: list[dict]) -> dict:
    by_name = {}
    for row in environment:
        key = (row["module"], row["declaration"].rsplit(".", 1)[-1])
        by_name.setdefault(key, []).append(row)
    declarations = []
    sources = sorted((ROOT / "lean/AsiStackProofs").glob("*.lean"))
    for source in sources:
        text = source.read_text()
        module = "AsiStackProofs." + source.stem
        for match in source_declarations(text):
            candidates = by_name.get((module, match.group(1)), [])
            if len(candidates) != 1:
                raise ValueError(f"{module}/{match.group(1)}: expected one elaborated theorem, observed {len(candidates)}")
            row = candidates[0]
            axioms = sorted(set(row["axioms"]))
            declarations.append({"declaration": row["declaration"], "module": module,
                                 "source_path": str(source.relative_to(ROOT)),
                                 "source_line": text.count("\n", 0, match.start()) + 1,
                                 "axioms": axioms,
                                 "trust_classes": sorted({classify(axiom) for axiom in axioms})})
    declarations.sort(key=lambda row: row["declaration"])
    if len({row['declaration'] for row in declarations}) != len(declarations):
        raise ValueError("duplicate source theorem identity")
    counts = Counter(axiom for row in declarations for axiom in row["axioms"] if classify(axiom) == "standard_logic")
    return {"schema_version": "asi_stack.proof_axiom_dependencies.v1",
            "projection_mode": "current_elaborated_environment",
            "toolchain": (ROOT / "lean/lean-toolchain").read_text().strip(),
            "input_sha256": identity(ROOT, input_paths()),
            "summary": {"source_theorem_count": len(declarations),
                        "source_modules_with_theorems": len({row['module'] for row in declarations}),
                        "axiom_free_theorems": sum(not row['axioms'] for row in declarations),
                        "native_compiler_trust_theorems": sum('native_compiler_trust' in row['trust_classes'] for row in declarations),
                        "unreviewed_axiom_theorems": sum('unreviewed_axiom' in row['trust_classes'] for row in declarations),
                        "standard_axiom_theorem_counts": dict(sorted(counts.items()))},
            "declarations": declarations,
            "non_claims": ["Axiom-free means no axiom dependency in this elaborated Lean declaration, not no assumptions in its proposition.",
                           "Standard logical axioms and compiler trust are disclosed trust dependencies, not evidence of a deployed system.",
                           "Native trust classification recognizes the reviewed Lean 4.31 native_decide and bv_decide generated names; it is not a compiler-correctness proof.",
                           "This inventory does not establish semantic adequacy, external-input truth, implementation refinement, safety or claim support."]}


def build() -> dict:
    before = identity(ROOT, input_paths())
    diagnostics = ROOT / "build/proof_axiom_audit"
    ordinary(diagnostics)
    diagnostics.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="run-", dir=diagnostics))
    def run(name: str, command: list[str], budget: float) -> dict:
        log = run_dir / (name + ".log")
        outcome = {"status": "running", "inner_command": command, "timeout_seconds": budget,
                   "log": str(log), "input_sha256": before,
                   "scope": "pinned Lean build/compiler identity/elaborated theorem query"}
        record = run_dir / (name + "-execution.json")
        record.write_text(json.dumps(outcome, indent=2) + "\n")
        result = execute_guarded(command, source_root=ROOT, cwd=ROOT / "lean", log=log, timeout=budget)
        outcome.update(result)
        record.write_text(json.dumps(outcome, indent=2) + "\n")
        return outcome
    def reject(name: str, outcome: dict, diagnostic: str, reason: str) -> None:
        outcome.update(process_status=outcome["status"], status="failed",
                       diagnostic_id=diagnostic, reason=reason)
        (run_dir / (name + "-execution.json")).write_text(json.dumps(outcome, indent=2) + "\n")
        raise ValueError(f"{diagnostic}: {reason}; inspect {run_dir}")
    build_result = run("build", ["lake", "build"], 1800)
    if build_result["status"] != "passed":
        raise ValueError(f"pinned Lean build did not complete: {build_result}")
    version_log = run_dir / "compiler-version.log"
    version_result = run("compiler-version", ["lake", "env", "lean", "--version"], 30)
    pinned_version = (ROOT / "lean/lean-toolchain").read_text().strip().rsplit(':v', 1)[-1]
    if version_result["status"] != "passed":
        raise ValueError(f"Lean compiler-version probe did not complete: {version_result}")
    if version_result["log_truncated"] or f"version {pinned_version}," not in version_log.read_text():
        reject("compiler-version", version_result, "compiler_identity_unverified",
               "complete actual Lean compiler output does not match the declared toolchain")
    log = run_dir / "environment.log"
    result = run("environment", ["lake", "env", "lean", str(TOOL)], 300)
    if result["status"] != "passed":
        raise ValueError(f"Lean axiom query did not complete: {result}; inspect its log")
    if result["log_truncated"]:
        reject("environment", result, "truncated_axiom_protocol", "elaborated environment output was truncated")
    try:
        environment = [json.loads(line) for line in log.read_text().splitlines() if line.strip()]
        value = assemble(environment)
    except (UnicodeError, ValueError, KeyError, TypeError) as error:
        reject("environment", result, "invalid_axiom_environment", f"{type(error).__name__}: {error}")
    if before != value['input_sha256']:
        reject("environment", result, "unstable_proof_inputs", 'Lean inputs changed during build/query; retry from one stable source state')
    return value


def errors(record: dict, expected: dict) -> list[str]:
    result = []
    if record != expected:
        result.append("axiom inventory differs from the current elaborated source-theorem projection")
    if record.get('summary', {}).get('unreviewed_axiom_theorems', 0):
        result.append("unreviewed axiom dependencies require an explicit trust review")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = build()
    if args.check:
        if not OUTPUT.exists():
            raise SystemExit(f"missing {OUTPUT.relative_to(ROOT)}; run {Path(__file__).name}")
        failures = errors(json.loads(OUTPUT.read_text()), expected)
        if failures:
            raise SystemExit('\n'.join(failures))
    else:
        if expected['summary']['unreviewed_axiom_theorems']:
            raise SystemExit('new axiom dependencies require review before accepting this projection')
        body = json.dumps(expected, indent=2) + '\n'
        if not OUTPUT.exists() or OUTPUT.read_text() != body:
            if OUTPUT.is_symlink():
                raise SystemExit('axiom projection refuses a symlink output')
            with tempfile.NamedTemporaryFile(mode='w', dir=OUTPUT.parent, prefix='.axiom-audit-', delete=False) as handle:
                staged = Path(handle.name)
                handle.write(body)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                staged.replace(OUTPUT)
            finally:
                staged.unlink(missing_ok=True)
    print(f"Axiom dependency audit: {expected['summary']}")


if __name__ == '__main__':
    main()
