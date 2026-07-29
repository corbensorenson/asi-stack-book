"""P7.3 pilot: Context Transactions, Snapshots, Mounts, and Taint."""

from __future__ import annotations

from manim import Arrow, Create, DashedLine, FadeIn, Indicate, LEFT, Line, RIGHT, RoundedRectangle, VGroup, Write, UP

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, proof_boundary, residual_marker,
    source_end_card, text, title_card,
)


def node(label: str, color: str = ACCENT, width: float = 1.75, height: float = 0.72) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.09, color=color, fill_color=SURFACE, fill_opacity=1)
    return VGroup(box, text(label, size=16, color=color, weight="BOLD").move_to(box))


class ContextTransactionsSnapshotsMountsAndTaint(AsiScene):
    TARGET_DURATION = 300.0

    def wait_until(self, target: float) -> None:
        if target > self.renderer.time:
            self.wait(target - self.renderer.time)

    def construct(self) -> None:
        for method, end in (
            (self.context_becomes_state, 42), (self.snapshot_mounts, 84),
            (self.commit_lifecycle, 125), (self.correction_trace, 170),
            (self.cache_taxonomy, 212), (self.evidence_ceiling, 258),
            (self.handoff, 300),
        ):
            method()
            self.wait_until(end)
            if end < self.TARGET_DURATION:
                self.clear_scene()

    def context_becomes_state(self) -> None:
        title = title_card(
            "Context Transactions",
            "Snapshots • mounts • branches • taint • closure",
            "context-transactions-snapshots-mounts-and-taint",
        ).scale(0.8).to_edge(UP, buff=0.25)
        loose = VGroup(
            node("STORE", BOUNDARY), node("GRAPH", ACCENT),
            node("CACHE", COPPER), node("SUMMARY", RESIDUAL),
        ).arrange(RIGHT, buff=0.4).shift(UP * 0.15)
        boundary = RoundedRectangle(
            width=10.4, height=2.2, corner_radius=0.16, color=ACCENT,
            fill_color=SURFACE, fill_opacity=0.25, stroke_width=4,
        ).shift(UP * -1.35)
        before = node("OBSERVED PRE-STATE", EVIDENCE, 2.65).move_to(LEFT * 3.1 + UP * -1.35)
        tx = node("CONTEXT TRANSACTION", AUTHORITY, 2.75).move_to(UP * -1.35)
        after = node("ORDERED POST-STATE", ACCENT, 2.65).move_to(RIGHT * 3.1 + UP * -1.35)
        arrows = VGroup(
            Arrow(before.get_right(), tx.get_left(), buff=0.08, color=ACCENT),
            Arrow(tx.get_right(), after.get_left(), buff=0.08, color=ACCENT),
        )
        self.play(Write(title), FadeIn(loose), run_time=1.2)
        self.play(Create(boundary), FadeIn(before), FadeIn(tx), FadeIn(after), Create(arrows), run_time=1.2)

    def snapshot_mounts(self) -> None:
        heading = text("A SNAPSHOT IS AN EXACT CAUSAL FRONTIER", size=34, color=INK, weight="BOLD").to_edge(UP)
        fields = VGroup(*[
            node(label, color, 2.15)
            for label, color in (
                ("object versions", ACCENT), ("content epoch", ACCENT),
                ("index epoch", ACCENT), ("causal parents", BOUNDARY),
                ("branch", BOUNDARY), ("provenance", EVIDENCE),
                ("taint", RESIDUAL), ("leases", AUTHORITY),
                ("caches + backups", COPPER), ("open obligations", ROLLBACK),
            )
        ]).arrange_in_grid(rows=5, cols=2, buff=(0.25, 0.16)).scale(0.82).shift(LEFT * 2.65 + UP * -0.45)
        spine = Line(UP * 2.0, UP * -2.0, color=ACCENT, stroke_width=5).shift(LEFT * 0.05 + UP * -0.3)
        permissions = VGroup(*[
            node(label, AUTHORITY if label in {"WRITE", "DELETE", "EXECUTE"} else EVIDENCE, 1.42, 0.56)
            for label in ("READ", "WRITE", "DERIVE", "DELETE", "EXPORT", "TRAIN", "EXECUTE")
        ]).arrange_in_grid(rows=4, cols=2, buff=(0.18, 0.2)).shift(RIGHT * 3.0 + UP * -0.15)
        label = text("PURPOSE-BOUND MOUNTS", size=22, color=AUTHORITY, weight="BOLD").next_to(permissions, UP, buff=0.3)
        footer = text("requested sets ≠ observed effects", size=23, color=MUTED).to_edge(UP * -1, buff=0.35)
        self.play(Write(heading), Create(spine), run_time=0.8)
        self.play(FadeIn(fields), FadeIn(permissions), FadeIn(label), FadeIn(footer), run_time=1.1)

    def commit_lifecycle(self) -> None:
        heading = text("COMMIT IS A LIFECYCLE", size=39, color=INK, weight="BOLD").to_edge(UP)
        labels = ("REQUESTED", "ADMITTED", "PREPARED", "APPLIED", "DURABLE", "VISIBLE", "REPLAYED", "RECOVERED")
        nodes = VGroup(*[
            node(f"{i + 1}  {label}", EVIDENCE if i >= 4 else ACCENT, 2.25)
            for i, label in enumerate(labels)
        ]).arrange_in_grid(rows=2, cols=4, buff=(0.32, 0.55)).scale(0.82).shift(UP * 0.2)
        arrows = VGroup()
        for start, end in ((0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7), (3, 4)):
            arrows.add(Arrow(nodes[start].get_right(), nodes[end].get_left(), buff=0.06, color=ACCENT, stroke_width=3))
        faults = VGroup(node("ABORTED", ROLLBACK, 2.0), node("INDETERMINATE", RESIDUAL, 2.35)).arrange(RIGHT, buff=0.6).shift(UP * -2.0)
        observe = node("INDEPENDENT POST-STATE", EVIDENCE, 2.8).to_edge(RIGHT, buff=0.45).shift(UP * -2.45)
        self.play(Write(heading), run_time=0.7)
        for item in nodes:
            self.play(FadeIn(item), run_time=0.18)
        self.play(Create(arrows), FadeIn(faults), FadeIn(observe), run_time=1.0)

    def correction_trace(self) -> None:
        heading = text("CORRECTION, CONFLICT, TAINT, AND CLOSURE", size=34, color=INK, weight="BOLD").to_edge(UP)
        snapshot = node("SNAPSHOT 41", ACCENT, 2.0).shift(LEFT * 4.4 + UP * 1.0)
        branch_b = node("BRANCH B: CORRECT", AUTHORITY, 2.5).shift(LEFT * 1.7 + UP * 1.55)
        branch_c = node("BRANCH C: CONFLICT", ROLLBACK, 2.55).shift(LEFT * 1.7 + UP * 0.45)
        derivatives = VGroup(
            node("SUMMARY", RESIDUAL), node("EMBEDDING", RESIDUAL),
            node("CACHE", RESIDUAL), node("ROUTE", RESIDUAL),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.25, 0.25)).shift(RIGHT * 1.8 + UP * 0.95)
        backup = residual_marker("UNREACHABLE BACKUP").scale(0.78).shift(RIGHT * 4.65 + UP * -1.65)
        delete = node("DELETE CLOSURE", ROLLBACK, 2.3).shift(LEFT * 0.3 + UP * -1.7)
        links = VGroup(
            Arrow(snapshot.get_right(), branch_b.get_left(), color=AUTHORITY, buff=0.08),
            Arrow(snapshot.get_right(), branch_c.get_left(), color=ROLLBACK, buff=0.08),
            Arrow(branch_b.get_right(), derivatives.get_left(), color=RESIDUAL, buff=0.08),
            DashedLine(branch_c.get_right(), derivatives.get_left(), color=ROLLBACK),
            Arrow(delete.get_right(), derivatives.get_bottom(), color=ROLLBACK, buff=0.08),
            DashedLine(derivatives.get_right(), backup.get_left(), color=RESIDUAL),
        )
        guard = text("NO SILENT LAST-WRITER-WINS", size=22, color=ROLLBACK, weight="BOLD").shift(LEFT * 2.2 + UP * -0.7)
        self.play(Write(heading), FadeIn(snapshot), run_time=0.8)
        self.play(FadeIn(branch_b), FadeIn(branch_c), Create(links[:2]), run_time=0.9)
        self.play(FadeIn(derivatives), Create(links[2:4]), FadeIn(guard), run_time=0.9)
        self.play(FadeIn(delete), Create(links[4:]), FadeIn(backup), run_time=0.9)

    def cache_taxonomy(self) -> None:
        heading = text("THREE DIFFERENT KINDS OF REUSE", size=37, color=INK, weight="BOLD").to_edge(UP)
        lanes = VGroup()
        for name, action, gate, color in (
            ("PREFIX STATE", "new answer", "compatible state", ACCENT),
            ("EXACT RESPONSE", "prior answer", "dependency closure", EVIDENCE),
            ("SEMANTIC RESPONSE", "prior answer", "approximate route", AUTHORITY),
        ):
            box = RoundedRectangle(width=9.0, height=1.1, corner_radius=0.1, color=color, fill_color=SURFACE, fill_opacity=1)
            row = VGroup(
                text(name, size=21, color=color, weight="BOLD"),
                text("→", size=25, color=MUTED),
                text(gate, size=20, color=INK),
                text("→", size=25, color=MUTED),
                text(action, size=20, color=color, weight="BOLD"),
            ).arrange(RIGHT, buff=0.45).move_to(box)
            lanes.add(VGroup(box, row))
        lanes.arrange(UP * -1, buff=0.3).shift(UP * -0.25)
        receipt = node("CACHE REUSE RECEIPT + FRESH FALLBACK", COPPER, 5.2).to_edge(UP * -1, buff=0.38)
        self.play(Write(heading), run_time=0.8)
        for lane in lanes:
            self.play(FadeIn(lane), run_time=0.55)
        self.play(FadeIn(receipt), run_time=0.6)

    def evidence_ceiling(self) -> None:
        heading = text("FINITE RECORD EVIDENCE, NOT A DEPLOYED STORE", size=32, color=INK, weight="BOLD").to_edge(UP)
        cards = VGroup(
            node("3 VALID / 6 INVALID\nSTORE FIXTURES", EVIDENCE, 3.0, 1.2),
            node("2 VALID / 4 INVALID\nEVENT SEQUENCES", ACCENT, 3.0, 1.2),
            node("78 / 78\nMUTATIONS REJECTED", AUTHORITY, 3.0, 1.2),
        ).arrange(RIGHT, buff=0.4).shift(UP * 0.7)
        boundary = proof_boundary(
            "ENCODED FINITE SCOPE",
            "no concurrency • durability • erasure • useful-memory claim",
        ).scale(0.88).shift(UP * -1.2)
        theater = text("A PERFECT LOG CAN STILL DESCRIBE THE WRONG REALITY", size=22, color=RESIDUAL, weight="BOLD").to_edge(UP * -1, buff=0.4)
        self.play(Write(heading), FadeIn(cards), run_time=1.1)
        self.play(Create(boundary), FadeIn(theater), run_time=0.9)

    def handoff(self) -> None:
        distinction = VGroup(
            node("VALID TRANSITION", EVIDENCE, 2.6),
            text("≠", size=38, color=ROLLBACK, weight="BOLD"),
            node("ADEQUATE EVIDENCE", AUTHORITY, 2.7),
        ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.35)
        end = source_end_card(
            "Context Transactions, Snapshots, Mounts, and Taint",
            "argument • Design rationale",
            "Finite POMDP result only; no open-world truth, transfer, or deployment.",
            "Verification Bandwidth and Context Adequacy",
        ).scale(0.75).shift(UP * -0.75)
        self.play(FadeIn(distinction), run_time=0.9)
        self.play(FadeIn(end), run_time=1.0)
