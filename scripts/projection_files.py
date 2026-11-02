"""Explicit text projection preview; it never evaluates domain acceptance."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile


class ProjectionFiles:
    def __init__(self, *, write: bool = True):
        self.write_enabled = write
        self.outputs: dict[Path, str] = {}

    def text(self, path: Path) -> str:
        return self.outputs[path] if path in self.outputs else path.read_text(encoding="utf-8")

    def exists(self, path: Path) -> bool:
        return path in self.outputs or path.exists()

    def write(self, path: Path, text: str) -> None:
        # Read-only preview may inspect the link's target; installation cannot
        # follow a link or replace an unexpected filesystem object.
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            raise ValueError(f"projection output must not traverse a symlink: {path}")
        if path.exists() and not path.is_file():
            raise ValueError(f"projection output is not a regular file: {path}")
        self.outputs[path] = text
        if not self.write_enabled or (path.is_file() and path.read_text(encoding="utf-8") == text):
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        # Each individual projection appears complete. This does not claim a
        # multi-file transaction; dependent checks still gate the whole set.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                             prefix=f".{path.name}.", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(text)
                stream.flush()
                os.fsync(stream.fileno())
            if path.exists():
                os.chmod(temporary, path.stat().st_mode & 0o777)
            else:
                os.chmod(temporary, 0o644)
            os.replace(temporary, path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def changes(self, root: Path) -> list[dict]:
        rows = []
        for path, text in self.outputs.items():
            desired = text.encode("utf-8")
            prior = path.read_bytes() if path.is_file() else None
            if prior == desired:
                continue
            rows.append({"path": path.relative_to(root).as_posix(),
                         "operation": "add" if prior is None else "update",
                         "before_sha256": hashlib.sha256(prior).hexdigest() if prior is not None else None,
                         "after_sha256": hashlib.sha256(desired).hexdigest(),
                         "before_bytes": len(prior) if prior is not None else None,
                         "after_bytes": len(desired)})
        return rows
