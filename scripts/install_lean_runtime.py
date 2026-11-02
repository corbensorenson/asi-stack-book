#!/usr/bin/env python3
"""Install a digest-bound Elan release; never run the moving shell installer."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
import tarfile
import tempfile
import time
from urllib.request import urlopen

from validation_runtime import execute


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "ci/dependency_pin_inventory.json"
MAX_ARCHIVE = 16 * 1024 * 1024
MAX_EXECUTABLE = 32 * 1024 * 1024


def binary_record(inventory: dict) -> dict:
    owners = [row for row in inventory["pins"] if row["repository"] == "leanprover/elan"]
    if len(owners) != 1 or not isinstance(owners[0].get("runtime_binary"), dict):
        raise ValueError("exactly one Elan owner with a governed runtime_binary is required")
    record = owners[0]["runtime_binary"]
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", record.get("version", "")):
        raise ValueError("Elan binary version must be an exact release tag")
    if not re.fullmatch(r"[0-9a-f]{40}", record.get("source_commit", "")):
        raise ValueError("Elan binary source context requires a full commit identity")
    platforms = set()
    for row in record["artifacts"]:
        target = row["target"]
        if target in platforms or target not in {
            "aarch64-apple-darwin", "x86_64-apple-darwin",
            "aarch64-unknown-linux-gnu", "x86_64-unknown-linux-gnu",
        }:
            raise ValueError("Elan artifact platform is duplicated or unsupported")
        platforms.add(target)
        expected = f"https://github.com/leanprover/elan/releases/download/{record['version']}/elan-{target}.tar.gz"
        if row["url"] != expected or not re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")):
            raise ValueError("Elan artifact requires its exact versioned official URL and digest")
        if isinstance(row.get("bytes"), bool) or not isinstance(row.get("bytes"), int) or not 0 < row["bytes"] <= MAX_ARCHIVE:
            raise ValueError("Elan archive size is missing or exceeds the bounded download")
    if not platforms:
        raise ValueError("Elan artifact inventory is empty")
    return record


def current_target() -> str:
    arch = {"arm64": "aarch64", "aarch64": "aarch64", "x86_64": "x86_64", "amd64": "x86_64"}.get(platform.machine().lower())
    if arch is None:
        raise ValueError(f"unsupported Elan architecture: {platform.machine()}")
    if platform.system() == "Darwin":
        return f"{arch}-apple-darwin"
    if platform.system() == "Linux" and platform.libc_ver()[0] == "glibc":
        return f"{arch}-unknown-linux-gnu"
    raise ValueError("the governed Elan artifacts support macOS and glibc Linux only")


def require_current_review(inventory: dict, as_of: date) -> None:
    owner = next(row for row in inventory["pins"] if row["repository"] == "leanprover/elan")
    reviewed = date.fromisoformat(owner["reviewed_on"])
    due = date.fromisoformat(owner["review_due_on"])
    if due != reviewed + timedelta(days=inventory["review_policy"]["max_review_age_days"]):
        raise ValueError("Elan review deadline is inconsistent with the governing policy")
    if not reviewed <= as_of <= due:
        raise ValueError("Elan review is future-dated or expired; installation is blocked before execution")
    if date.fromisoformat(owner["runtime_binary"]["observed_on"]) > as_of:
        raise ValueError("Elan artifact observation is future-dated")


def version_matches(text: str, record: dict) -> bool:
    return bool(re.search(rf"\belan(?:-init)? {re.escape(record['version'][1:])}\b", text)
                and record["source_commit"][:9] in text)


def verify_archive(path: Path, artifact: dict) -> None:
    if path.stat().st_size != artifact["bytes"] or hashlib.sha256(path.read_bytes()).hexdigest() != artifact["sha256"]:
        raise ValueError("Elan archive size or SHA-256 differs from the governed artifact")


def download(artifact: dict, path: Path) -> None:
    started = time.monotonic()
    size = 0
    with urlopen(artifact["url"], timeout=30) as response, path.open("wb") as stream:
        while chunk := response.read(65536):
            size += len(chunk)
            if size > artifact["bytes"] or size > MAX_ARCHIVE or time.monotonic() - started > 120:
                raise ValueError("Elan artifact download exceeds its byte or time budget")
            stream.write(chunk)
    verify_archive(path, artifact)


def extract_verified(path: Path, artifact: dict, destination: Path) -> Path:
    verify_archive(path, artifact)
    with tarfile.open(path, "r:gz") as archive:
        members = archive.getmembers()
        if len(members) != 1 or members[0].name not in {"elan-init", "./elan-init"}:
            raise ValueError("Elan archive must contain only the named installer executable")
        member = members[0]
        if not member.isfile() or not 0 < member.size <= MAX_EXECUTABLE:
            raise ValueError("Elan archive executable is a link, special file or invalid size")
        # No extractall: archive paths and modes cannot select a destination or
        # overwrite unrelated files. Digest verification precedes extraction.
        binary = destination / "elan-init"
        with archive.extractfile(member) as source, binary.open("xb") as output:
            output.write(source.read(MAX_EXECUTABLE + 1))
        if binary.stat().st_size != member.size:
            raise ValueError("Elan executable extraction is incomplete")
        binary.chmod(0o755)
        return binary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="Install the governed native Elan and the repository's exact Lean toolchain")
    parser.add_argument("--elan-home", type=Path, help="Explicit tool home; required for installation")
    parser.add_argument("--verify-archive", type=Path, help="Verify/extract an existing downloaded archive without execution")
    parser.add_argument("--target", help="Explicit governed target for non-executing archive verification")
    args = parser.parse_args()
    if args.install and (not args.elan_home or args.target or args.verify_archive):
        parser.error("installation requires --elan-home and the detected native target")
    if args.target and not args.verify_archive:
        parser.error("--target is only available for non-executing archive verification")
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    record = binary_record(inventory)
    if args.install:
        # Installation uses real UTC time; a historical audit-date environment
        # override cannot reopen an expired execution window.
        require_current_review(inventory, datetime.now(timezone.utc).date())
    target = args.target or current_target()
    artifact = next((row for row in record["artifacts"] if row["target"] == target), None)
    if artifact is None:
        raise ValueError(f"no governed archive for {target}; mutable downloads are forbidden")
    with tempfile.TemporaryDirectory(prefix="elan-runtime-") as temporary:
        stage = Path(temporary).resolve()
        archive = args.verify_archive or stage / "elan.tar.gz"
        if args.verify_archive:
            verify_archive(archive, artifact)
        else:
            download(artifact, archive)
        binary = extract_verified(archive, artifact, stage)
        if args.install:
            toolchain = (ROOT / "lean/lean-toolchain").read_text(encoding="utf-8").strip()
            if not re.fullmatch(r"leanprover/lean4:v[0-9]+\.[0-9]+\.[0-9]+", toolchain):
                raise ValueError("Lean toolchain must be an exact stable repository pin")
            logs = ROOT / "build/lean_runtime"
            version = execute([str(binary), "--version"], cwd=ROOT, log=logs / "elan-version.log", timeout=30)
            if version["status"] != "passed" or not version_matches((logs / "elan-version.log").read_text(), record):
                raise ValueError("verified Elan executable does not report the governed version")
            # An argv-only exec shim sets the tool-specific home without
            # changing HOME or the user's shell profile. The common executor
            # still owns process-group termination and bounded retained logs.
            shim = "import os,sys; os.environ['ELAN_HOME']=sys.argv[1]; os.execv(sys.argv[2],sys.argv[2:])"
            result = execute([sys.executable, "-c", shim, str(args.elan_home.resolve()), str(binary),
                              "-y", "--no-modify-path", "--default-toolchain", toolchain],
                             cwd=ROOT, log=logs / "elan-install.log", timeout=1800)
            if result["status"] != "passed":
                raise ValueError(f"Elan installation {result['status']}; inspect {result['log']}")
            # Elan initialization only sets the default. Provision the actual
            # compiler here rather than charging its download to the first gate.
            installed_elan = args.elan_home.resolve() / "bin/elan"
            provision = execute([sys.executable, "-c", shim, str(args.elan_home.resolve()),
                                 str(installed_elan), "toolchain", "install", toolchain],
                                cwd=ROOT, log=logs / "lean-toolchain-install.log", timeout=1800)
            if provision["status"] != "passed":
                raise ValueError(f"Lean toolchain provisioning {provision['status']}; inspect {provision['log']}")
            pinned_version = toolchain.rsplit(":v", 1)[1]
            for tool, pattern in (
                ("lean", rf"\bLean \(version {re.escape(pinned_version)}(?:,|\))"),
                ("lake", rf"\bLean version {re.escape(pinned_version)}\)"),
            ):
                # `run` without --install refuses missing toolchains. Its
                # explicit selection also ignores ambient toolchain overrides.
                checked = execute([sys.executable, "-c", shim, str(args.elan_home.resolve()),
                                   str(installed_elan), "run", toolchain, tool, "--version"],
                                  cwd=ROOT / "lean", log=logs / f"{tool}-version.log", timeout=30)
                if checked["status"] != "passed" or not re.search(pattern, (logs / f"{tool}-version.log").read_text()):
                    raise ValueError(f"{tool} does not report the pinned Lean {pinned_version}; inspect {checked['log']}")
        print(json.dumps({"version": record["version"], "target": target, "sha256": artifact["sha256"],
                          "installed": args.install, "scope": "Exact artifact identity; no claim of benign code, fresh Linux qualification or reproducible scientific dependencies."}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, tarfile.TarError) as error:
        raise SystemExit(f"Lean runtime installation failed: {error}")
