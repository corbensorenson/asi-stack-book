"""P7.3 pilot: Living Book Methodology."""

from __future__ import annotations

from manim import Arrow, Create, DashedLine, FadeIn, LEFT, Line, RIGHT, RoundedRectangle, VGroup, Write, UP

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, proof_boundary, residual_marker,
    source_end_card, text, title_card,
)


def artifact(label: str, color: str = ACCENT, width: float = 2.15, height: float = 0.72) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.09, color=color, fill_color=SURFACE, fill_opacity=1)
    return VGroup(box, text(label, size=16, color=color, weight="BOLD").move_to(box))


class LivingBookMethodology(AsiScene):
    TARGET_DURATION = 300.0

    def wait_until(self, target: float) -> None:
        if target > self.renderer.time:
            self.wait(target - self.renderer.time)

    def construct(self) -> None:
        for method, end in (
            (self.book_graph, 42), (self.freeze_separate, 84),
            (self.atomize_validate, 127), (self.derivatives, 170),
            (self.correction, 214), (self.repository_evidence, 258),
            (self.successor, 300),
        ):
            method()
            self.wait_until(end)
            if end < self.TARGET_DURATION:
                self.clear_scene()

    def book_graph(self) -> None:
        heading = title_card(
            "Living Book Methodology",
            "Evidence-preserving publication transactions",
            "living-book-methodology",
        ).scale(0.8).to_edge(UP, buff=0.25)
        book = artifact("BOOK", ACCENT, 2.5, 1.35).shift(UP * -0.2)
        nodes = VGroup(
            artifact("CANONICAL SOURCE", ACCENT, 2.4),
            artifact("MANIFEST", BOUNDARY),
            artifact("SOURCE INVENTORY", EVIDENCE, 2.4),
            artifact("CLAIM LEDGER", RESIDUAL),
            artifact("PROOF MANIFEST", AUTHORITY, 2.35),
            artifact("TESTS", EVIDENCE),
            artifact("RENDERED SITE", COPPER, 2.3),
            artifact("RELEASE + HISTORY", BOUNDARY, 2.5),
        ).arrange_in_grid(rows=2, cols=4, buff=(0.35, 1.2)).scale(0.8).shift(UP * -0.85)
        links = VGroup(*[
            Arrow(book.get_center(), n.get_center(), buff=0.48, color=BOUNDARY, stroke_width=2.5)
            for n in nodes
        ])
        self.play(Write(heading), FadeIn(book), run_time=1.0)
        self.play(FadeIn(nodes), Create(links), run_time=1.2)

    def freeze_separate(self) -> None:
        heading = text("FREEZE IDENTITY • SEPARATE AUTHORITY", size=36, color=INK, weight="BOLD").to_edge(UP)
        envelope = artifact(
            "OBJECTIVE • COMMIT • GRAPH • AUDIENCE • RIGHTS • RELEASE • TIME • NON-CLAIMS",
            AUTHORITY, 10.8, 0.9,
        ).shift(UP * 1.1)
        lanes = VGroup(*[
            artifact(label, color, 2.45, 0.64)
            for label, color in (
                ("SOURCE REPORT", EVIDENCE), ("AUTHOR INTENT", COPPER),
                ("SYNTHESIS", ACCENT), ("EXPERIMENT", EVIDENCE),
                ("FORMAL PROOF", AUTHORITY), ("EDITORIAL JUDGMENT", COPPER),
                ("OPEN QUESTION", RESIDUAL),
            )
        ]).arrange_in_grid(rows=4, cols=2, buff=(0.45, 0.2)).scale(0.88).shift(UP * -0.65)
        law = text(
            "source count ≠ evidence • theorem build ≠ enforcement • polish ≠ support",
            size=21, color=ROLLBACK, weight="BOLD",
        ).to_edge(UP * -1, buff=0.35)
        self.play(Write(heading), FadeIn(envelope), run_time=1.0)
        self.play(FadeIn(lanes), FadeIn(law), run_time=1.1)

    def atomize_validate(self) -> None:
        heading = text("ONE CLAIM, EXPLICIT DEPENDENCIES, DISTINCT GATES", size=32, color=INK, weight="BOLD").to_edge(UP)
        claim = artifact("CLAIM ID", RESIDUAL, 2.0, 1.0).shift(LEFT * 4.8 + UP * 0.7)
        fields = VGroup(*[
            artifact(label, color, 1.75, 0.56)
            for label, color in (
                ("scope", ACCENT), ("falsifier", ROLLBACK), ("evidence", EVIDENCE),
                ("sources", EVIDENCE), ("contrary", ROLLBACK), ("ceiling", AUTHORITY),
                ("residual", RESIDUAL), ("consumers", COPPER),
            )
        ]).arrange_in_grid(rows=4, cols=2, buff=(0.16, 0.14)).scale(0.76).shift(LEFT * 2.25 + UP * 0.45)
        packet = artifact("TYPED CHANGE PACKET", AUTHORITY, 2.8, 0.85).shift(RIGHT * 0.55 + UP * 0.45)
        gates = VGroup(*[
            artifact(label, color, 1.62, 0.52)
            for label, color in (
                ("schema", BOUNDARY), ("semantic", ACCENT), ("source", EVIDENCE),
                ("proof", AUTHORITY), ("executable", EVIDENCE), ("rights", COPPER),
                ("accessibility", AUTHORITY), ("render", COPPER), ("browser", ACCENT),
                ("release", ROLLBACK), ("deploy", BOUNDARY), ("observe", EVIDENCE),
            )
        ]).arrange_in_grid(rows=4, cols=3, buff=(0.12, 0.12)).scale(0.72).shift(RIGHT * 3.65 + UP * -0.1)
        arrows = VGroup(
            Arrow(claim.get_right(), fields.get_left(), buff=0.08, color=RESIDUAL),
            Arrow(fields.get_right(), packet.get_left(), buff=0.08, color=AUTHORITY),
            Arrow(packet.get_right(), gates.get_left(), buff=0.08, color=ACCENT),
        )
        footer = text("GREEN MEANS ONLY THE CONTRACT THAT PRODUCED IT", size=22, color=MUTED, weight="BOLD").to_edge(UP * -1, buff=0.35)
        self.play(Write(heading), FadeIn(claim), FadeIn(fields), Create(arrows[:1]), run_time=1.0)
        self.play(FadeIn(packet), Create(arrows[1:2]), FadeIn(gates), Create(arrows[2:]), run_time=1.1)
        self.play(FadeIn(footer), run_time=0.5)

    def derivatives(self) -> None:
        heading = text("DERIVATIVES ARE PROJECTIONS, NOT RIVAL BOOKS", size=33, color=INK, weight="BOLD").to_edge(UP)
        source = artifact("CANONICAL SOURCE", ACCENT, 3.0, 1.0).shift(UP * 1.05)
        outputs = VGroup(*[
            artifact(label, color, 1.75, 0.62)
            for label, color in (
                ("AI VIEW", ACCENT), ("HUMAN VIEW", EVIDENCE), ("READER", EVIDENCE),
                ("HTML", COPPER), ("DOCX", COPPER), ("EPUB", COPPER), ("PDF", COPPER),
                ("ARTICLE", AUTHORITY), ("IMAGE", AUTHORITY), ("AUDIO", RESIDUAL), ("VIDEO", RESIDUAL),
            )
        ]).arrange_in_grid(rows=3, cols=4, buff=(0.22, 0.22)).scale(0.82).shift(UP * -0.55)
        arrows = VGroup(*[
            Arrow(source.get_bottom(), out.get_top(), buff=0.08, color=BOUNDARY, stroke_width=2)
            for out in outputs
        ])
        custody = text(
            "commit • audience • transform • review • approval • residual • non-claim",
            size=21, color=MUTED,
        ).to_edge(UP * -1, buff=0.35)
        self.play(Write(heading), FadeIn(source), run_time=0.9)
        self.play(FadeIn(outputs), Create(arrows), run_time=1.2)
        self.play(FadeIn(custody), run_time=0.5)

    def correction(self) -> None:
        heading = text("A CORRECTION MUST REACH EVERY CONSUMER", size=34, color=INK, weight="BOLD").to_edge(UP)
        source = artifact("SOURCE: WITHDRAWN", ROLLBACK, 2.8, 1.0).shift(LEFT * 4.6 + UP * 0.8)
        claim = artifact("CLAIM: REVIEW / DOWNGRADE", RESIDUAL, 3.2, 1.0).shift(LEFT * 1.2 + UP * 0.8)
        consumers = VGroup(*[
            artifact(label, RESIDUAL, 1.8, 0.58)
            for label in ("chapter", "proof note", "appendix", "synopsis", "transcript", "video", "public page", "citation")
        ]).arrange_in_grid(rows=4, cols=2, buff=(0.2, 0.18)).scale(0.82).shift(RIGHT * 2.25 + UP * -0.05)
        old = artifact("IMMUTABLE HISTORICAL RELEASE", BOUNDARY, 3.45, 0.75).shift(LEFT * 1.8 + UP * -1.55)
        residual = residual_marker("UNREACHED CONSUMER").scale(0.72).shift(RIGHT * 4.8 + UP * -1.65)
        links = VGroup(
            Arrow(source.get_right(), claim.get_left(), buff=0.08, color=ROLLBACK),
            *[DashedLine(claim.get_right(), item.get_left(), color=RESIDUAL) for item in consumers],
        )
        state = text("CURRENT → STALE → UPDATED / WITHDRAWN / SUPERSEDED / RESIDUAL", size=19, color=AUTHORITY, weight="BOLD").to_edge(UP * -1, buff=0.25)
        self.play(Write(heading), FadeIn(source), run_time=0.8)
        self.play(FadeIn(claim), Create(links[:1]), run_time=0.7)
        self.play(FadeIn(consumers), Create(links[1:]), FadeIn(old), FadeIn(residual), FadeIn(state), run_time=1.2)

    def repository_evidence(self) -> None:
        heading = text("SUBSTANTIAL LOCAL DISCIPLINE, NARROW INFERENCE", size=32, color=INK, weight="BOLD").to_edge(UP)
        numbers = VGroup(*[
            artifact(value, color, 2.15, 0.72)
            for value, color in (
                ("3 SLICES", ACCENT), ("12 CASES", EVIDENCE), ("10 STATES", AUTHORITY),
                ("6 EFFECTS", COPPER), ("3 ROLLBACKS", ROLLBACK),
                ("20 INJECTIONS", RESIDUAL), ("11 MUTATIONS", RESIDUAL), ("11-SURFACE EPOCH", BOUNDARY),
            )
        ]).arrange_in_grid(rows=2, cols=4, buff=(0.28, 0.4)).scale(0.86).shift(UP * 0.55)
        boundary = proof_boundary(
            "BOUNDED LOCAL REPLAY",
            "not source correctness • whole-book truth • accessibility • transfer",
        ).scale(0.88).shift(UP * -1.2)
        self.play(Write(heading), FadeIn(numbers), run_time=1.1)
        self.play(Create(boundary), run_time=0.9)

    def successor(self) -> None:
        handoff = VGroup(
            artifact("CANONICAL COMMIT", ACCENT, 2.35),
            artifact("TERMINAL LEDGER", EVIDENCE, 2.35),
            artifact("RESIDUAL QUEUE", RESIDUAL, 2.35),
            artifact("PUBLICATION STATE", COPPER, 2.35),
            artifact("ONE ACTIVE ROADMAP", AUTHORITY, 2.65),
        ).arrange(RIGHT, buff=0.25).scale(0.8).to_edge(UP, buff=0.35)
        end = source_end_card(
            "Living Book Methodology",
            "argument • Design rationale",
            "Bounded local replay only; no whole-book proof, transfer, or release claim.",
            "Open Research Agenda and Bibliography Plan",
        ).scale(0.74).shift(UP * -0.65)
        self.play(FadeIn(handoff), run_time=1.1)
        self.play(FadeIn(end), run_time=1.0)
