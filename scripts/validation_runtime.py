"""Shared execution diagnostics; no domain acceptance rules live here."""

from __future__ import annotations

import hashlib
from contextlib import ExitStack
import importlib.util
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import sys
import tempfile
import time


def capability_error(name: str) -> str | None:
    if name == "python":
        return None
    if name == "unix_process_groups":
        return None if os.name == "posix" else "requires Linux or macOS process groups"
    if name.startswith("module:"):
        module = name.split(":", 1)[1]
        try:
            available = importlib.util.find_spec(module) is not None
        except (ImportError, ValueError):
            available = False
        return None if available else f"{sys.executable} cannot import {module}"
    if name.startswith("tool:"):
        tool = name.split(":", 1)[1]
        return None if shutil.which(tool) else f"{tool} is missing from PATH"
    return f"unknown capability {name!r}"


def identity(root: Path, paths: list[str]) -> dict[str, str]:
    """Exact file inputs only; directory manifests stay with domain owners."""
    result = {}
    for relative in paths:
        path = root / relative
        if path.is_file():
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def run_directory(root: Path, prefix: str) -> Path:
    """Fresh ignored diagnostics; no existing invocation is overwritten."""
    from admission_guard import ordinary
    if not prefix or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in prefix):
        raise ValueError("diagnostic prefix must be a simple lowercase name")
    build = root / "build"
    ordinary(build)
    build.mkdir(exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=prefix + "-", dir=build))


def execute_guarded(command: list[str], *, source_root: Path, cwd: Path, log: Path,
                    timeout: float, max_log_bytes: int = 10 * 1024 * 1024,
                    stderr_log: Path | None = None) -> dict:
    """Bound capture and bind payload lifetime to this caller's source lease.

    The capture wrapper is independently grouped. EOF on its owner pipe stops
    it; the existing independent guardian then stops the payload group and
    retains the source-root lease until the group is absent. Escaped groups,
    simultaneous wrapper/guardian loss and physical power loss remain outside
    this cooperating-process protocol.
    """
    from admission_guard import command_directory, ordinary
    ordinary(source_root)
    source_root = source_root.resolve()
    cwd = command_directory(source_root, cwd)
    wrapper = ("import os,sys,threading\nfrom pathlib import Path\n"
               f"sys.path.insert(0, {str(Path(__file__).resolve().parent)!r})\n"
               "from admission_guard import run_command\n"
               "def owner_disappeared():\n"
               "    os.read(int(sys.argv[1]),1)\n"
               "    os._exit(125)\n"
               "threading.Thread(target=owner_disappeared,daemon=True).start()\n"
               "raise SystemExit(run_command(Path(sys.argv[2]),sys.argv[3:],cwd=Path.cwd()))\n")
    control, owner = os.pipe()
    wrapped = [sys.executable, "-c", wrapper, str(control), str(source_root), *command]
    try:
        result = execute(wrapped, cwd=cwd, log=log, timeout=timeout,
                         max_log_bytes=max_log_bytes, stderr_log=stderr_log, pass_fds=(control,))
    finally:
        os.close(owner)
        os.close(control)
    result.update(inner_command=command, source_root=str(source_root), command_cwd=str(cwd),
                  lifetime_guard="owner pipe and independent canonical guardian")
    return result


def signal_owned_group(process: subprocess.Popen, sig: int) -> None:
    try:
        os.killpg(process.pid, sig)
    except ProcessLookupError:
        return
    except PermissionError:
        # Darwin's killpg1 filters zombies, then may return EPERM for an
        # existing group with no signalable members. Never ignore EPERM:
        # after the owned leader exits, allow only a bounded zero-signal
        # probe to confirm that the group has actually disappeared (ESRCH).
        # https://github.com/apple-oss-distributions/xnu/blob/main/bsd/kern/kern_sig.c
        if sys.platform != "darwin" or process.poll() is None:
            raise
        deadline = time.monotonic() + 0.5
        while True:
            try:
                os.killpg(process.pid, 0)
            except ProcessLookupError:
                return
            except PermissionError:
                pass
            else:
                raise PermissionError("owned group remains present after signal refusal")
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.01)


def terminate(process: subprocess.Popen) -> None:
    # Kill the group even if its original leader has already exited: a
    # descendant may still hold stdout or continue mutating its workspace.
    for sig in (signal.SIGTERM, signal.SIGKILL):
        signal_owned_group(process, sig)
        if sig == signal.SIGTERM:
            try:
                process.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                pass
    process.wait(timeout=5)


def execute(command: list[str], *, cwd: Path, log: Path, timeout: float,
            max_log_bytes: int = 10 * 1024 * 1024,
            stderr_log: Path | None = None, pass_fds: tuple[int, ...] = ()) -> dict:
    """Bound wall time and total retained output; optionally separate stderr."""
    if os.name != "posix":
        raise ValueError("validation execution currently supports Linux and macOS")
    if timeout <= 0 or max_log_bytes <= 0:
        raise ValueError("execution budgets must be positive")
    if stderr_log is not None and stderr_log.resolve() == log.resolve():
        raise ValueError("stdout and stderr logs must be distinct")
    started = time.monotonic()
    log.parent.mkdir(parents=True, exist_ok=True)
    if stderr_log is not None:
        stderr_log.parent.mkdir(parents=True, exist_ok=True)
    process = None
    retained = 0
    channel_bytes = {"stdout": 0, "stderr": 0}
    truncated = False
    status = None
    cleanup_errors = []

    def cleanup() -> None:
        nonlocal status
        if process is None:
            return
        try:
            terminate(process)
        except (OSError, subprocess.TimeoutExpired) as error:
            # A cleanup refusal must retain the unit/log outcome rather than
            # crashing the aggregate or laundering a successful leader exit.
            cleanup_errors.append(f"{type(error).__name__}: {error}")
            status = "failed"

    with ExitStack() as stack, selectors.DefaultSelector() as selector:
        stdout = stack.enter_context(log.open("wb"))
        streams = {"stdout": stdout}
        if stderr_log is not None:
            streams["stderr"] = stack.enter_context(stderr_log.open("wb"))
        try:
            # Open both owned logs before spawning. A setup refusal must not
            # leave a child whose lifetime was never brought under cleanup.
            process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE if stderr_log is not None else subprocess.STDOUT,
                                       start_new_session=True, pass_fds=pass_fds,
                                       env={**os.environ, "PATH": str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")})
            selector.register(process.stdout, selectors.EVENT_READ, "stdout")
            if process.stderr is not None:
                selector.register(process.stderr, selectors.EVENT_READ, "stderr")
            while selector.get_map():
                if time.monotonic() - started >= timeout:
                    status = "timed_out"
                    cleanup()
                    break
                for key, _ in selector.select(timeout=min(0.1, timeout)):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    allowed = min(len(chunk), max(0, max_log_bytes - retained))
                    streams[key.data].write(chunk[:allowed])
                    channel_bytes[key.data] += allowed
                    retained += allowed
                    truncated |= allowed < len(chunk)
            if status is None:
                try:
                    process.wait(timeout=max(0.001, timeout - (time.monotonic() - started)))
                except subprocess.TimeoutExpired:
                    status = "timed_out"
                    cleanup()
        except KeyboardInterrupt:
            status = "cancelled"
            cleanup()
        finally:
            if process is not None:
                process.stdout.close()
                if process.stderr is not None:
                    process.stderr.close()
            cleanup()
    exit_code = process.returncode if process is not None else None
    return {"status": status or ("passed" if exit_code == 0 else "failed"),
            "exit_code": exit_code, "duration_seconds": round(time.monotonic() - started, 3),
            "log": str(log), "log_bytes": channel_bytes["stdout"], "log_truncated": truncated,
            "command": command, "diagnostic_id": "cleanup_failed" if cleanup_errors else status or ("ok" if exit_code == 0 else "unit_rejected"),
            **({"stderr_log": str(stderr_log), "stderr_log_bytes": channel_bytes["stderr"],
                "retained_log_bytes": retained, "log_budget_scope": "combined stdout and stderr"}
               if stderr_log is not None else {}),
            **({"cleanup_errors": cleanup_errors, "cleanup_confirmed": False} if cleanup_errors else {})}
