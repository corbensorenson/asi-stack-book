#!/usr/bin/env python3
"""Reproduce historical generation-one chapter packets.

This seven-scene packet generator is retained for artifact custody only. New
visual abstracts use the generation-two teaching-promise and beat-plan path.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import textwrap
from pathlib import Path

from visual_chapter_source import canonical_chapter_sha256
from visual_publication_lifecycle import preserve_predecessor_projection


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
PILOTS = {
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
}
ARCHETYPES = ("state_machine", "stack", "graph", "ledger", "route", "timeline", "before_after")
SCENE_TIMES = (
    ("00:00–00:39", "Problem and shortcut"),
    ("00:39–01:19", "Operating mechanism"),
    ("01:19–02:02", "Concrete state transition"),
    ("02:02–02:46", "Failure boundary"),
    ("02:46–03:27", "Evidence state"),
    ("03:27–04:04", "Non-claims"),
    ("04:04–04:45", "Handoff"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def clean(value: str) -> str:
    if isinstance(value, dict):
        value = (
            value.get("target")
            or value.get("claim")
            or value.get("description")
            or value.get("tag")
            or json.dumps(value, sort_keys=True)
        )
    value = re.sub(r"\s+", " ", str(value)).strip()
    return value


def first_sentence(value: str) -> str:
    value = clean(value)
    match = re.match(r"(.+?[.!?])(?:\s|$)", value)
    return match.group(1) if match else value


def words(value: str, limit: int) -> str:
    tokens = clean(value).split()
    if len(tokens) <= limit:
        return " ".join(tokens)
    minimum = max(5, limit // 2)
    for terminal_pattern in (r"[.!?]$", r"[,;:]$"):
        for end in range(limit, minimum - 1, -1):
            if re.search(terminal_pattern, tokens[end - 1]):
                result = " ".join(tokens[:end]).rstrip(",;:")
                return result if result.endswith((".", "!", "?")) else result + "."
    stop_words = {
        "a", "an", "and", "as", "at", "before", "by", "for", "from", "in",
        "into", "of", "on", "or", "the", "that", "to", "under", "which",
        "while", "with", "without",
    }
    end = limit
    while end > minimum and tokens[end - 1].lower().strip(",;:") in stop_words:
        end -= 1
    return " ".join(tokens[:end]).rstrip(",;:") + "."


def label(value: str, limit: int = 5) -> str:
    text = clean(value).replace("/", " ").replace("_", " ")
    text = re.sub(r"^(A|An|The)\s+", "", text, flags=re.I)
    return " ".join(text.split()[:limit]).rstrip(".,;:")


def display(value: str, limit: int = 13) -> str:
    value = first_sentence(value)
    tokens = value.split()
    if len(tokens) <= limit:
        return value
    # Display copy is an explicitly abbreviated phrase, not a synthetic
    # grammatical sentence.  An ellipsis prevents a clipped subordinate clause
    # from being misread as a complete claim.
    head_count = max(6, (limit + 1) // 2)
    tail_count = limit - head_count
    connectors = {
        "a", "an", "and", "as", "at", "before", "by", "for", "from", "in",
        "into", "of", "on", "or", "the", "that", "to", "under", "which",
        "while", "with", "without",
    }
    head_tokens = tokens[:head_count]
    while len(head_tokens) > 6 and head_tokens[-1].lower().strip(",;:") in connectors:
        head_tokens.pop()
    tail_tokens = tokens[-tail_count:] if tail_count else []
    while len(tail_tokens) > 4 and tail_tokens[0].lower().strip(",;:") in connectors:
        tail_tokens.pop(0)
    head = " ".join(head_tokens).rstrip(",;:.!?")
    tail = " ".join(tail_tokens).lstrip(",;:")
    return f"{head}… {tail}".strip()


def compact_label(value: str, limit: int = 4) -> str:
    """Keep the first content-bearing words instead of labels such as 'Build a'."""
    tokens = clean(value).replace("/", " ").replace("_", " ").split()
    disposable = {
        "a", "an", "the", "and", "or", "to", "of", "for", "with", "from",
        "as", "at", "before", "after", "by", "in", "into", "on", "that",
        "then", "under", "which", "while",
        "build", "create", "make", "use", "apply", "test", "map", "bind",
        "track", "record", "require", "define", "compute", "implement",
        "classify", "compile", "decompose", "express", "inventory", "measure",
        "preserve", "represent", "version",
    }
    content = [
        token.strip(".,;:()[]{}")
        for token in tokens
        if token.lower().strip(".,;:()[]{}") not in disposable
    ]
    selected = content[:limit] or tokens[:limit]
    while len(selected) > 2 and len(" ".join(selected)) > 35:
        selected.pop()
    while len(selected) > 2 and selected[-1].endswith("-"):
        selected.pop()
    result = " ".join(selected).rstrip(".,;:-")
    return result[:1].upper() + result[1:]


def paragraph(*values: str, limit: int = 105) -> str:
    return words(" ".join(clean(value) for value in values if clean(value)), limit)


def svg_text(value: str, width: int = 32) -> list[str]:
    return textwrap.wrap(clean(value), width=width, break_long_words=False)[:3]


def chapter_list(structure: dict) -> list[tuple[dict, dict]]:
    return [
        (part, chapter)
        for part in structure["parts"]
        for chapter in part["chapters"]
    ]


def build_content(chapter: dict, next_chapter: dict, index: int) -> dict:
    mechanisms = chapter["mechanism"]
    failures = chapter["failure_modes"]
    implementation = [chapter["minimal_implementation"]]
    proof_targets = chapter["proof_targets"]
    invariants = chapter["invariants"]
    selected_mechanisms = [mechanisms[i] for i in range(min(4, len(mechanisms)))]
    selected_failures = [failures[i] for i in range(min(4, len(failures)))]
    selected_trace = [implementation[i] for i in range(min(4, len(implementation)))]
    selected_targets = [proof_targets[i] for i in range(min(3, len(proof_targets)))]
    while len(selected_mechanisms) < 4:
        selected_mechanisms.append(invariants[len(selected_mechanisms) % len(invariants)])
    while len(selected_failures) < 4:
        selected_failures.append(invariants[len(selected_failures) % len(invariants)])
    while len(selected_trace) < 4:
        selected_trace.append(mechanisms[len(selected_trace) % len(mechanisms)])
    while len(selected_targets) < 3:
        selected_targets.append(invariants[len(selected_targets) % len(invariants)])

    evidence_ceiling = (
        f"This chapter remains {chapter['claim_label']} at {chapter['evidence_level']} support. "
        "Its contracts, examples, tests, or local artifacts establish only their encoded scope."
    )
    maximum_inference = (
        f"At most, this visual explains the chapter's {chapter['claim_label'].lower()} "
        f"at {chapter['evidence_level']} support; it adds no empirical, deployment, safety, "
        "transfer, state-of-the-art, AGI, or ASI result."
    )
    nonclaims = [
        "No chapter claim or evidence state is promoted by this visual.",
        "A named mechanism is not proof of correct implementation or useful deployment.",
        "A local check or formal model does not establish real-world enforcement.",
        "No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows.",
    ]
    required_content = {
        "problem": paragraph(chapter["problem"], chapter["insufficient"], limit=85),
        "core_mechanism": paragraph(chapter["core_claim"], *selected_mechanisms[:2], limit=95),
        "worked_trace": paragraph(*selected_trace, limit=100),
        "failure_boundary": paragraph(*selected_failures, limit=90),
        "evidence_state": paragraph(evidence_ceiling, *selected_targets, limit=85),
        "non_claims": " ".join(nonclaims),
        "handoff": (
            f"The next chapter is {next_chapter['title']}. It takes responsibility for "
            f"{words(next_chapter['problem'], 30).rstrip('.') }."
        ),
    }
    narration = [
        paragraph(
            f"This chapter asks a specific question: {chapter['problem']}",
            f"The tempting shortcut is insufficient: {chapter['insufficient']}",
            limit=100,
        ),
        paragraph(
            f"The chapter's core claim is this: {chapter['core_claim']}",
            *selected_mechanisms[:3],
            limit=110,
        ),
        paragraph(
            "A concrete implementation trace makes the proposal testable.",
            *selected_trace,
            f"Throughout the trace, one invariant remains visible: {invariants[0]}",
            limit=110,
        ),
        paragraph(
            "The design can still fail.",
            *selected_failures,
            "The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.",
            limit=105,
        ),
        paragraph(
            evidence_ceiling,
            "The chapter names proof targets rather than pretending they are already closed.",
            *selected_targets,
            limit=100,
        ),
        paragraph(
            *nonclaims,
            "These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.",
            limit=80,
        ),
        paragraph(
            maximum_inference,
            required_content["handoff"],
            "Read the live chapter for its complete source mappings, interfaces, invariants, failure modes, tests, and open evidence gaps.",
            limit=75,
        ),
    ]
    display_content = {
        "problem": display(chapter["problem"], 20),
        "insufficient": display(chapter["insufficient"], 20),
        "mechanism": [
            {"label": compact_label(item, 4), "detail": display(item, 14)}
            for item in selected_mechanisms
        ],
        "trace": [compact_label(item, 4) for item in selected_mechanisms],
        "failures": [display(item, 12) for item in selected_failures],
        "proof_targets": [display(item, 14) for item in selected_targets],
        "evidence_ceiling": display(evidence_ceiling, 25),
        "nonclaims": [display(item, 18) for item in nonclaims],
        "maximum_inference": display(maximum_inference, 24),
    }
    return {
        "archetype": ARCHETYPES[index % len(ARCHETYPES)],
        "required_content": required_content,
        "narration": narration,
        "display": display_content,
        "maximum_inference": maximum_inference,
        "nonclaims": nonclaims,
    }


def scene_description(number: int, spec: dict) -> str:
    archetype = spec["archetype"].replace("_", " ")
    descriptions = (
        "The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.",
        f"A labeled {archetype} diagram exposes four distinct responsibilities and their explicit relationships.",
        "Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.",
        "Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.",
        "A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.",
        "Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.",
        "The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.",
    )
    return descriptions[number]


def build_storyboard(chapter: dict, spec: dict, chapter_sha: str) -> str:
    rows = [
        "| Time | Scene | Visual action | Narration job | Accessibility and boundary |",
        "|---|---|---|---|---|",
    ]
    jobs = (
        "Define the chapter's problem and reject the insufficient shortcut.",
        "Explain the chapter-specific operating mechanism.",
        "Walk one implementable state transition.",
        "Name the design's principal failure modes and stop behavior.",
        "State current support and unresolved proof targets.",
        "Prevent inference beyond the canonical chapter.",
        "Bind the derivative to the live source and successor.",
    )
    for index, ((time, scene), job) in enumerate(zip(SCENE_TIMES, jobs)):
        rows.append(
            f"| {time} | {index + 1}. {scene} | {scene_description(index, spec)} "
            f"| {job} | Every state, edge, and boundary has a persistent text label. |"
        )
    return (
        f"# Storyboard — {chapter['title']}\n\n"
        f"Video ID: `asi-video-{chapter['id']}`\n\n"
        "Target visual duration: 285 seconds; final audio controls the exact mux duration.\n\n"
        "Canvas: 16:9, 1920 × 1080 release\n"
        f"Source chapter digest: `{chapter_sha}`\n"
        f"Visual archetype: `{spec['archetype']}`\n\n"
        + "\n".join(rows)
        + "\n\n"
        + spec["maximum_inference"]
        + "\n"
    )


def build_transcript(chapter: dict, spec: dict) -> str:
    sections = []
    for index, ((time, scene), narration) in enumerate(zip(SCENE_TIMES, spec["narration"])):
        sections.append(
            f"## {time} — {scene}\n\n"
            f"**Visual description.** {scene_description(index, spec)}\n\n"
            f"**Narration.** {narration}\n"
        )
    return (
        f"# Descriptive transcript — {chapter['title']}\n\n"
        "Canonical live chapter:\n"
        f"<https://corbensorenson.github.io/asi-stack-book/{chapter['file'].replace('.qmd', '.html')}>\n\n"
        f"Video ID: `asi-video-{chapter['id']}`\n\n"
        "Lifecycle: scripted local derivative; no YouTube publication is authorized\n\n"
        f"Current support: `{chapter['evidence_level']}` — `{chapter['claim_label']}`\n\n"
        + "\n".join(sections)
        + "\n## Source and evidence boundary\n\n"
        + spec["maximum_inference"]
        + "\n"
    )


def build_thumbnail(chapter: dict, spec: dict) -> str:
    title_lines = svg_text(chapter["title"], 34)
    title_nodes = "\n".join(
        f'  <text x="70" y="{100 + index * 58}" fill="#F5F8FA" '
        'font-family="Avenir Next, sans-serif" font-size="48" font-weight="700">'
        f"{html.escape(line.upper())}</text>"
        for index, line in enumerate(title_lines)
    )
    cards = spec["display"]["mechanism"][:3]
    card_nodes = []
    for index, item in enumerate(cards):
        x = 55 + index * 400
        center = x + 185
        color = ("#58B7D3", "#D79A6B", "#62C370")[index]
        label_lines = svg_text(item["label"], 20)
        detail_lines = svg_text(words(item["detail"], 12), 35)[:2]
        label_nodes = "\n".join(
            f'    <tspan x="{center}" y="{390 + line_index * 27}">'
            f"{html.escape(line.upper())}</tspan>"
            for line_index, line in enumerate(label_lines)
        )
        detail_nodes = "\n".join(
            f'    <tspan x="{center}" y="{488 + line_index * 23}">'
            f"{html.escape(line)}</tspan>"
            for line_index, line in enumerate(detail_lines)
        )
        card_nodes.append(
            f'  <rect x="{x}" y="345" width="370" height="190" rx="22" fill="#182630" '
            f'stroke="{color}" stroke-width="7"/>\n'
            f'  <text x="{center}" text-anchor="middle" fill="{color}" '
            'font-family="Avenir Next, sans-serif" font-size="21" font-weight="700">\n'
            f"{label_nodes}\n"
            "  </text>\n"
            f'  <text x="{center}" text-anchor="middle" fill="#B8C4CC" '
            'font-family="Avenir Next, sans-serif" font-size="17">\n'
            f"{detail_nodes}\n"
            "  </text>"
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" '
        'viewBox="0 0 1280 720" role="img" aria-labelledby="title desc">\n'
        f'  <title id="title">{html.escape(chapter["title"])}</title>\n'
        f'  <desc id="desc">{html.escape(spec["thumbnail_alt"])}</desc>\n'
        '  <rect width="1280" height="720" fill="#101820"/>\n'
        + title_nodes
        + "\n"
        + "\n".join(card_nodes)
        + '\n  <path d="M240 565 H1040" stroke="#8F9AA3" stroke-width="5"/>\n'
        '  <text x="640" y="625" text-anchor="middle" fill="#F45B69" '
        'font-family="Avenir Next, sans-serif" font-size="25" font-weight="700">'
        'MECHANISM • FAILURE BOUNDARY • EVIDENCE CEILING</text>\n'
        '</svg>\n'
    )


def build_packet(chapter: dict, spec: dict, chapter_sha: str, source_commit: str) -> dict:
    base = f"visual_edition/chapters/{chapter['id']}"
    return {
        "schema_version": "asi_stack.visual_chapter_packet.v1",
        "video_id": f"asi-video-{chapter['id']}",
        "chapter_id": chapter["id"],
        "chapter_path": chapter["file"],
        "chapter_sha256": chapter_sha,
        "source_commit": source_commit,
        "pilot": False,
        "lifecycle_state": "scripted",
        "claim_bindings": [{
            "claim_id": f"{chapter['id']}.core",
            "claim_label": chapter["claim_label"],
            "support_state": chapter["evidence_level"],
        }],
        "assigned_source_ids": chapter["source_ids"],
        "maximum_inference": spec["maximum_inference"],
        "required_content": spec["required_content"],
        "artifacts": {
            "storyboard": f"{base}/storyboard.md",
            "scene_code": f"{base}/scene.py",
            "narration_script": f"{base}/narration.txt",
            "captions": f"{base}/captions.vtt",
            "descriptive_transcript": f"{base}/transcript.md",
            "thumbnail": f"{base}/thumbnail.svg",
            "scene_spec": f"{base}/scene_spec.json",
            "thumbnail_alt_text": spec["thumbnail_alt"],
        },
        "render_receipt": None,
        "youtube": {
            "channel_id": "UCX7Tu67cGmKfT6O38xxiQFA",
            "video_id": None,
            "watch_url": None,
            "playlist_id": None,
            "generation": 0,
            "publication_state": "not_authorized",
            "uploaded_output_sha256": None,
            "bound_chapter_sha256": None,
            "bound_source_commit": None,
            "published_at_utc": None,
            "platform_receipt_path": None,
            "supersedes_video_id": None,
        },
        "quarto_embed": {
            "state": "absent_until_published",
            "chapter_anchor": "visual-abstract",
            "frame_title": f"Visual abstract: {chapter['title']}",
            "aria_label": f"Play the visual abstract for {chapter['title']}",
        },
        "staleness": {
            "state": "current",
            "checked_chapter_sha256": chapter_sha,
            "triggers": [
                "core_claim", "mechanism", "worked_trace", "evidence_state",
                "non_claim", "material_source", "chapter_identity", "handoff", "public_url",
            ],
        },
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "This derivative video does not promote or otherwise change any book claim.",
            "A complete tracked source packet is not a rendered video, YouTube upload, or public publication.",
            "Generated chapter-specific prose and visuals still require final A/V validation before publication.",
            "A successful render does not establish deployment, safety, efficiency, transfer, state of the art, AGI, or ASI.",
        ],
    }


def write_chapter(chapter: dict, next_chapter: dict, index: int, source_commit: str) -> None:
    directory = ROOT / "visual_edition/chapters" / chapter["id"]
    directory.mkdir(parents=True, exist_ok=True)
    prior_packet_path = directory / "packet.json"
    prior_packet = (
        json.loads(prior_packet_path.read_text(encoding="utf-8"))
        if prior_packet_path.is_file()
        else None
    )
    chapter_sha = canonical_chapter_sha256(ROOT / chapter["file"])
    content = build_content(chapter, next_chapter, index)
    content["chapter_id"] = chapter["id"]
    content["title"] = chapter["title"]
    content["subtitle"] = display(chapter["core_claim"], 28)
    content["claim_label"] = chapter["claim_label"]
    content["evidence_level"] = chapter["evidence_level"]
    content["next_title"] = next_chapter["title"]
    content["thumbnail_alt"] = (
        f"A governed {content['archetype'].replace('_', ' ')} diagram for {chapter['title']} "
        "shows three named mechanism cards above a labeled failure and evidence boundary."
    )
    scene_spec = {
        key: content[key]
        for key in (
            "chapter_id", "title", "subtitle", "archetype", "claim_label",
            "evidence_level", "next_title", "display",
        )
    }
    (directory / "scene_spec.json").write_text(
        json.dumps(scene_spec, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    class_name = "ChapterVisualAbstract"
    (directory / "scene.py").write_text(
        '"""Generated chapter-owned P7.3 scene entrypoint."""\n\n'
        "import sys\n"
        "from pathlib import Path\n\n"
        "sys.path.insert(0, str(Path(__file__).resolve().parents[3]))\n\n"
        "from visual_edition.lib.chapter_scene import AsiChapterScene\n\n\n"
        f"class {class_name}(AsiChapterScene):\n"
        f'    SPEC_RELATIVE = "visual_edition/chapters/{chapter["id"]}/scene_spec.json"\n',
        encoding="utf-8",
    )
    (directory / "narration.txt").write_text(
        "\n\n".join(content["narration"]) + "\n",
        encoding="utf-8",
    )
    captions_path = directory / "captions.vtt"
    placeholder = "WEBVTT\n\nNOTE Canonical timing is generated from the final narration receipt.\n"
    if (
        not captions_path.exists()
        or "NOTE Canonical timing is generated from the final narration receipt."
        in captions_path.read_text(encoding="utf-8")
    ):
        captions_path.write_text(placeholder, encoding="utf-8")
    spec_for_docs = {**content, "thumbnail_alt": content["thumbnail_alt"]}
    (directory / "storyboard.md").write_text(
        build_storyboard(chapter, spec_for_docs, chapter_sha),
        encoding="utf-8",
    )
    (directory / "transcript.md").write_text(
        build_transcript(chapter, spec_for_docs),
        encoding="utf-8",
    )
    (directory / "thumbnail.svg").write_text(
        build_thumbnail(chapter, spec_for_docs),
        encoding="utf-8",
    )
    packet = preserve_predecessor_projection(
        prior_packet,
        build_packet(chapter, spec_for_docs, chapter_sha, source_commit),
    )
    (directory / "packet.json").write_text(
        json.dumps(packet, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--historical-generation-one",
        action="store_true",
        help="Acknowledge that this command reproduces the deprecated generation-one template.",
    )
    parser.add_argument(
        "--thumbnails-only",
        action="store_true",
        help="Regenerate only non-pilot tracked SVG thumbnail sources.",
    )
    args = parser.parse_args()
    if not args.historical_generation_one:
        raise SystemExit(
            "Generation-one packet synthesis is historical-only. "
            "Use the generation-two Manim skill workflow, or pass "
            "--historical-generation-one solely to reproduce a prior artifact."
        )
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapters = chapter_list(structure)
    source_commit = git_head()
    generated = 0
    for index, (_, chapter) in enumerate(chapters):
        if chapter["id"] in PILOTS:
            continue
        next_chapter = chapters[(index + 1) % len(chapters)][1]
        if args.thumbnails_only:
            content = build_content(chapter, next_chapter, index)
            content["thumbnail_alt"] = (
                f"A governed {content['archetype'].replace('_', ' ')} diagram for "
                f"{chapter['title']} shows three named mechanism cards above a labeled "
                "failure and evidence boundary."
            )
            thumbnail = ROOT / f"visual_edition/chapters/{chapter['id']}/thumbnail.svg"
            thumbnail.write_text(
                build_thumbnail(chapter, content),
                encoding="utf-8",
            )
        else:
            write_chapter(chapter, next_chapter, index, source_commit)
        generated += 1
    noun = "thumbnails" if args.thumbnails_only else "chapter visual source packets"
    print(f"Generated {generated} non-pilot {noun}.")


if __name__ == "__main__":
    main()
