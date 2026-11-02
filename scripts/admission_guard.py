#!/usr/bin/env python3
"""Gate canonical reads and writes around recoverable chapter admission."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import os
from pathlib import Path
import selectors
import signal
import stat
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = "build/chapter-admission-active.json"


def ordinary(path: Path) -> None:
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise ValueError(f"canonical admission must not traverse a link: {candidate}")


def ensure_ready(root: Path) -> None:
    ordinary(root / ACTIVE)
    if os.path.lexists(root / ACTIVE):
        raise ValueError("canonical chapter admission is pending; inspect the retained transaction and run scripts/recover_chapter_admission.py --rollback before canonical work")


@contextmanager
def canonical_access(root: Path, *, write: bool = False, recovery: bool = False):
    """Cooperating processes lock the existing directory, without file writes.

    Manual edits do not honor flock; installation also compares captured bytes,
    modes and object identities. Unsupported filesystems fail closed.
    """
    ordinary(root)
    if not recovery:
        ensure_ready(root)
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(fd, (fcntl.LOCK_EX if write else fcntl.LOCK_SH) | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError("another canonical operation holds the repository directory lock") from error
        if not recovery:
            ensure_ready(root)
        yield fd
        if not write:
            ensure_ready(root)
    finally:
        os.close(fd)


def command_directory(root: Path, cwd: Path | None) -> Path:
    directory = root if cwd is None else cwd
    ordinary(directory)
    directory.resolve().relative_to(root.resolve())
    if not directory.is_dir():
        raise ValueError("canonical command working directory must exist inside its source root")
    return directory.resolve()


def supervise(root: Path, command: list[str], lease: int, control: int, *, write: bool,
              cwd: Path | None = None) -> int:
    """Own the lease independently of the wrapper, until its command is stopped.

    EOF on the private pipe means the wrapper died. The command never inherits
    the pipe or lease. This covers cooperating descendants in its process
    group; escaping that group or killing the supervisor is outside this gate.
    """
    from validation_runtime import terminate
    ordinary(root)
    directory = command_directory(root, cwd)
    identity = os.fstat(lease)
    current = root.stat()
    if (not stat.S_ISDIR(identity.st_mode)
            or (identity.st_dev, identity.st_ino) != (current.st_dev, current.st_ino)
            or not stat.S_ISFIFO(os.fstat(control).st_mode)):
        raise ValueError("command supervisor requires the live repository lease and control pipe")
    fcntl.flock(lease, (fcntl.LOCK_EX if write else fcntl.LOCK_SH) | fcntl.LOCK_NB)
    ensure_ready(root)
    os.set_inheritable(lease, False)
    os.set_inheritable(control, False)
    stopping = False
    def cancel(_signum, _frame):
        nonlocal stopping
        stopping = True
    signal.signal(signal.SIGTERM, cancel)
    signal.signal(signal.SIGINT, cancel)
    process = None
    with selectors.DefaultSelector() as selector:
        selector.register(control, selectors.EVENT_READ)
        try:
            # Do not start a command if its wrapper already disappeared.
            if selector.select(timeout=0):
                return 125
            process = subprocess.Popen(command, cwd=directory, start_new_session=True)
            while process.poll() is None and not stopping:
                if selector.select(timeout=0.1):
                    os.read(control, 1)  # cancellation byte or EOF
                    stopping = True
            return process.wait() if not stopping else 125
        finally:
            if process is not None:
                try:
                    terminate(process)
                except (OSError, subprocess.TimeoutExpired) as error:
                    print(f"Canonical command cleanup failed; retaining source lease: {error}", file=sys.stderr)
                    stopping = True
                # Signal delivery is asynchronous. Leader exit alone cannot
                # establish that descendants have stopped. On uncertainty,
                # retain the lease until absence is actually observed.
                reported = stopping
                started = time.monotonic()
                while True:
                    try:
                        os.killpg(process.pid, 0)
                    except ProcessLookupError:
                        break
                    except PermissionError:
                        pass
                    if not reported and time.monotonic() - started >= 5:
                        print("Canonical command group remains present; retaining source lease.", file=sys.stderr)
                        reported = True
                    time.sleep(0.02)
                if stopping:
                    # A cleanup failure must not become a successful exit.
                    # Cancellation is already a failure; raising also covers
                    # a successful leader followed by refused cleanup.
                    raise ValueError("canonical command was cancelled or cleanup failed")


def run_command(root: Path, command: list[str], *, write: bool = False,
                cwd: Path | None = None) -> int:
    if not command:
        raise ValueError("canonical command is empty")
    directory = command_directory(root, cwd)
    with canonical_access(root, write=write) as lease:
        control, cancellation = os.pipe()
        supervisor = None
        try:
            arguments = [sys.executable, str(Path(__file__).resolve()),
                         "--supervisor-lease", str(lease), "--supervisor-control", str(control)]
            if write:
                arguments.append("--write")
            if cwd is not None:
                arguments.extend(["--supervisor-command-cwd", str(directory)])
            supervisor = subprocess.Popen(arguments + ["--run", *command], cwd=root,
                                          start_new_session=True, pass_fds=(lease, control))
            os.close(control)
            control = None
            return supervisor.wait()
        finally:
            os.close(cancellation)  # EOF also handles abrupt wrapper death.
            if control is not None:
                os.close(control)
            if supervisor is not None:
                # Keep waiting through further interrupts. The independent
                # supervisor still owns the lease if this wrapper is killed.
                while supervisor.poll() is None:
                    try:
                        supervisor.wait()
                    except KeyboardInterrupt:
                        continue


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Hold an exclusive lease for a canonical producer")
    parser.add_argument("--run", nargs=argparse.REMAINDER, help="Run a command under the canonical source lease")
    parser.add_argument("--supervisor-lease", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--supervisor-control", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--supervisor-command-cwd", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.supervisor_lease is not None or args.supervisor_control is not None:
        if args.supervisor_lease is None or args.supervisor_control is None or not args.run:
            parser.error("incomplete internal command supervisor invocation")
        code = supervise(Path.cwd(), args.run, args.supervisor_lease, args.supervisor_control,
                         write=args.write, cwd=args.supervisor_command_cwd)
        if code < 0:
            signum = -code
            if signum not in (signal.SIGKILL, signal.SIGSTOP):
                signal.signal(signum, signal.SIG_DFL)
            os.kill(os.getpid(), signum)
        raise SystemExit(code)
    if args.supervisor_command_cwd is not None:
        parser.error("command working directory requires the internal lease/control invocation")
    if args.run is not None:
        if not args.run:
            parser.error("--run requires a command")
        raise SystemExit(run_command(ROOT, args.run, write=args.write))
    with canonical_access(ROOT, write=args.write):
        print("Canonical admission is ready.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Canonical operation refused: {error}")
