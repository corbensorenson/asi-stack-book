#!/usr/bin/env python3
"""Shared, outcome-independent contracts for P4/M8 Campaign 6."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/p4_kerc_runtime"
SEEDS = (17, 29, 43, 71, 101)
INTENTS = ("approve", "deny", "schedule", "cancel", "compare", "calculate", "explain", "quote")
LANGUAGES = ("en", "es")
DOMAINS = ("operations", "research")
PROTECTED = re.compile(r'https?://\S+|`[^`]+`|"[^"]+"|\b\d+(?:\.\d+)?\s?(?:kg|ms|GB|%)\b|\b\d{4}-\d{2}-\d{2}\b')

LEXICON = {
    "approve": ("approve", "authorize", "permit", "green-light", "aprueba", "autoriza", "permite"),
    "deny": ("deny", "reject", "refuse", "block", "deniega", "rechaza", "bloquea"),
    "schedule": ("schedule", "plan", "book", "agenda", "programa", "planifica"),
    "cancel": ("cancel", "abort", "stop", "withdraw", "cancela", "aborta", "detén"),
    "compare": ("compare", "contrast", "weigh", "compara", "contrasta"),
    "calculate": ("calculate", "compute", "derive", "calcula", "computa"),
    "explain": ("explain", "describe", "clarify", "explica", "describe", "aclara"),
    "quote": ("quote", "repeat exactly", "cite", "cita", "repite exactamente"),
}

def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def extract_objects(text: str) -> list[str]:
    return PROTECTED.findall(text)

def detect_intent(text: str) -> tuple[str, bool]:
    low = text.lower()
    found = [(low.find(term), intent) for intent, terms in LEXICON.items() for term in terms if term in low]
    intent = min(found)[1] if found else "unknown"
    negated = bool(re.search(r"\b(?:not|never|no|don't|do not|sin|nunca|no)\b", low))
    return intent, negated

def simple_handle_glossary(text: str) -> str:
    objects = extract_objects(text)
    body = text
    for idx, obj in enumerate(objects):
        body = body.replace(obj, f"@{idx}")
    return body.lower() + " || " + " | ".join(f"@{i}={x}" for i, x in enumerate(objects))

def compile_packet(text: str, mode: str = "faithful", *, ablation: str | None = None) -> dict:
    objects = [] if ablation == "no_protection" else extract_objects(text)
    intent, negated = detect_intent(text)
    if ablation == "no_sense": intent = "action"
    modality = "required" if re.search(r"\b(must|required|debe|obligatorio)\b", text.lower()) else "possible"
    if ablation == "no_modality": modality = "unspecified"
    kernel = [f"I:{intent}", f"N:{int(negated)}", f"M:{modality}", f"O:{len(objects)}"]
    if ablation == "no_macro": kernel.extend(["ROLE:agent", "ROLE:target"])
    else: kernel.append("R:AT")
    exact = {f"o{i}": value for i, value in enumerate(objects)}
    residual = {
        "interaction_global": {"glossary": sorted(set(objects))} if ablation != "no_global_residual" else {},
        "segment": {"language_hint": "es" if re.search(r"\b(?:debe|por favor|calcula|explica|compara)\b", text.lower()) else "en"} if ablation != "no_segment_residual" else {},
        "token_local": {"surface_length": len(text)} if ablation != "no_token_residual" else {},
        "exact_object": exact if ablation != "no_exact_residual" else {},
    }
    packet = {
        "abi": "kerc.kernel_packet.v1", "kernel": " ".join(kernel), "objects": exact,
        "residual": residual, "mode": mode, "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "state_hash": canonical_sha([kernel, residual]), "migration": {"from": 1, "to": 1},
    }
    if ablation == "no_state_hash": packet.pop("state_hash")
    if ablation == "no_migration": packet.pop("migration")
    if mode == "lossless": packet["lossless_source"] = text
    return packet

def render_packet(packet: dict) -> str:
    if packet.get("mode") == "lossless" and "lossless_source" in packet:
        return packet["lossless_source"]
    fields = dict(x.split(":", 1) for x in packet["kernel"].split() if ":" in x)
    action = fields.get("I", "unknown")
    prefix = "Do not " if fields.get("N") == "1" else ""
    objs = " ".join(packet.get("objects", {}).values())
    return f"{prefix}{action} {objs}".strip()

def representation(packet: dict) -> str:
    return packet["kernel"] + " " + " ".join(f"{k}={v}" for k, v in packet.get("objects", {}).items())
