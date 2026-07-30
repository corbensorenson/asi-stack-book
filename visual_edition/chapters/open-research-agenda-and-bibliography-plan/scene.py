"""Generated chapter-owned P7.3 scene entrypoint."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from visual_edition.lib.chapter_scene import AsiChapterScene


class ChapterVisualAbstract(AsiChapterScene):
    SPEC_RELATIVE = "visual_edition/chapters/open-research-agenda-and-bibliography-plan/scene_spec.json"
