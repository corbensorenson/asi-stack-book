"""Standards-based schema validation shared by the book's record consumers.

References resolve only to checked-in schemas; validation never fetches a URL.
`format` remains an annotation, as in Draft 2020-12's default vocabulary.
Domain consumers still own semantic, custody, and authority checks.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"
PUBLIC_SCHEMA_BASE = "https://corbensorenson.github.io/asi-stack-book/schemas/"


def validator_class(schema: Any) -> Any:
    cls = validator_for(schema, default=Draft202012Validator)
    if isinstance(schema, dict) and "$schema" in schema:
        cls = validator_for(schema, default=None)
        if cls is None:
            raise ValueError(f"unsupported schema dialect: {schema['$schema']!r}")
    return cls


def _schema_error(schema: Any) -> str | None:
    try:
        validator_class(schema).check_schema(schema)
    except (SchemaError, ValueError) as exc:
        return str(getattr(exc, "message", str(exc)))
    return None


def _plain_json(value: Any) -> bool:
    # Do not coerce Python tuples, non-string keys or custom objects through
    # JSON: check_schema must retain its rejection of those invalid shapes.
    if type(value) in {str, int, float, bool, type(None)}:
        return True
    if type(value) is list:
        return all(_plain_json(item) for item in value)
    if type(value) is dict:
        return all(type(key) is str and _plain_json(item) for key, item in value.items())
    return False


@lru_cache(maxsize=128)
def _serialized_schema_error(serialized: str) -> str | None:
    # Only schema-definition validity is reused. Instance verdicts, domain
    # judgments and reference resolution are never cached here. Content keys
    # detect in-process mutations; cached errors carry no caller path.
    return _schema_error(json.loads(serialized))


def schema_errors(schema: Any, path: str) -> list[str]:
    error = None
    serialized = None
    if _plain_json(schema):
        try:
            serialized = json.dumps(schema, sort_keys=True, separators=(",", ":"), allow_nan=False)
        except (TypeError, ValueError):
            pass
    # Bound retained keys as well as entry count. Larger/non-JSON definitions
    # still receive the same standards check, simply without reuse.
    if serialized is not None and len(serialized) <= 65536:
        error = _serialized_schema_error(serialized)
    else:
        error = _schema_error(schema)
    return [f"{path}: invalid schema: {error}"] if error is not None else []


@lru_cache(maxsize=1)
def local_registry() -> Registry:
    # A validation process sees one source snapshot. New processes reload it;
    # tests changing schema files in-process must call cache_clear().
    resources = []
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        resource = Resource.from_contents(schema)
        aliases = {path.name, path.as_uri(), PUBLIC_SCHEMA_BASE + path.name}
        if schema.get("$id"):
            aliases.add(schema["$id"])
        resources.extend((uri, resource) for uri in sorted(aliases))
    # Registry's default retrieve refuses unknown resources. Do not install a
    # network retriever: a missing local contract is a validation error.
    return Registry().with_resources(resources)


def instance_path(root: str, parts: Any) -> str:
    for part in parts:
        root += f"[{part}]" if isinstance(part, int) else f".{part}"
    return root


def validate_value(value: Any, schema: Any, path: str) -> list[str]:
    invalid_schema = schema_errors(schema, path)
    if invalid_schema:
        return invalid_schema
    try:
        validator = validator_class(schema)(schema, registry=local_registry())
        errors = list(validator.iter_errors(value))
    except Unresolvable as exc:
        return [f"{path}: unresolved local schema reference: {exc}"]
    return sorted(
        f"{instance_path(path, error.absolute_path)}: {error.message} "
        f"[schema keyword: {error.validator}]"
        for error in errors
    )
