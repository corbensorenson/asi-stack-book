"""P7.3 pilot: Replaceable Cognitive Substrates."""

from __future__ import annotations

from manim import Arrow, Circle, Create, FadeIn, FadeOut, Indicate, LEFT, Line, Polygon, RIGHT, RoundedRectangle, Square, VGroup, Write, UP

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, proof_boundary, source_end_card, text,
    title_card,
)


def card(label: str, detail: str = "", color: str = ACCENT, width: float = 2.3, height: float = 1.0) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, color=color, fill_color=SURFACE, fill_opacity=1)
    items = [text(label, size=19, color=color, weight="BOLD")]
    if detail:
        items.append(text(detail, size=14, color=MUTED))
    return VGroup(box, VGroup(*items).arrange(UP * -1, buff=0.1).move_to(box))


class ReplaceableCognitiveSubstrates(AsiScene):
    TARGET_DURATION = 300.0

    def wait_until(self, target: float) -> None:
        if target > self.renderer.time:
            self.wait(target - self.renderer.time)

    def construct(self) -> None:
        for method, end in (
            (self.monoculture, 42), (self.abi_contract, 84),
            (self.families, 127), (self.routing, 170),
            (self.architectural_rsi, 214), (self.onecell, 258),
            (self.evidence, 300),
        ):
            method()
            self.wait_until(end)
            if end < self.TARGET_DURATION:
                self.clear_scene()

    def monoculture(self) -> None:
        heading = title_card(
            "Replaceable Cognitive Substrates",
            "The implementation is not the interface",
            "replaceable-cognitive-substrates-beyond-transformer-monoculture",
        ).scale(0.72).to_edge(UP, buff=0.25)
        socket = Circle(radius=1.22, color=ACCENT, fill_color=SURFACE, fill_opacity=1, stroke_width=6).shift(LEFT * 3.4 + UP * -0.8)
        socket_label = text("TOKEN\n+\nKV CACHE", size=25, color=ACCENT, weight="BOLD").move_to(socket)
        transformer_shape = Circle(radius=0.75, color=EVIDENCE, fill_color=SURFACE, fill_opacity=1).shift(LEFT * 3.4 + UP * -0.8)
        transformer = VGroup(
            transformer_shape,
            text("TRANSFORMER", size=14, color=EVIDENCE, weight="BOLD").move_to(transformer_shape),
        )
        rejected = VGroup(
            Square(side_length=1.25, color=COPPER), Polygon(LEFT, RIGHT, UP * 0.95, color=RESIDUAL),
            RoundedRectangle(width=1.7, height=0.72, color=AUTHORITY),
        ).arrange(RIGHT, buff=0.65).shift(RIGHT * 2.5 + UP * 0.2)
        rejected_labels = VGroup(
            text("SSM", size=18, color=COPPER), text("GRAPH", size=18, color=RESIDUAL),
            text("PROGRAM", size=18, color=AUTHORITY),
        )
        for label, shape in zip(rejected_labels, rejected):
            label.move_to(shape)
        abi = card("COGNITIVE KERNEL ABI", "typed obligations + receipts", ACCENT, 5.4, 1.2).shift(RIGHT * 2.4 + UP * -1.6)
        arrows = VGroup(*[Arrow(shape.get_bottom(), abi.get_top(), buff=0.08, color=BOUNDARY) for shape in rejected])
        self.play(Write(heading), Create(socket), FadeIn(socket_label), run_time=1.0)
        self.play(FadeOut(socket_label), FadeIn(transformer), FadeIn(rejected), FadeIn(rejected_labels), run_time=1.0)
        self.play(FadeIn(abi), Create(arrows), run_time=0.9)

    def abi_contract(self) -> None:
        heading = text("THE ABI RETURNS A PROPOSAL, NOT AN EFFECT", size=34, color=INK, weight="BOLD").to_edge(UP)
        request = card("KERNEL REQUEST", "task • state • authority • budget", ACCENT, 3.4, 1.35).shift(LEFT * 3.8 + UP * 0.35)
        abi = card("TYPED ABI", "declare differences or reject", AUTHORITY, 2.4, 1.35).shift(UP * 0.35)
        proposal = card("KERNEL PROPOSAL", "uncertainty • receipts • non-claims", EVIDENCE, 3.6, 1.35).shift(RIGHT * 3.9 + UP * 0.35)
        arrows = VGroup(
            Arrow(request.get_right(), abi.get_left(), buff=0.08, color=ACCENT),
            Arrow(abi.get_right(), proposal.get_left(), buff=0.08, color=EVIDENCE),
        )
        fields = VGroup(*[
            card(label, "", color, 1.75, 0.58)
            for label, color in (
                ("checkpoint", BOUNDARY), ("state delta", BOUNDARY),
                ("cost", COPPER), ("assistance", COPPER),
                ("kernel ID", ACCENT), ("evidence", EVIDENCE),
            )
        ]).arrange(RIGHT, buff=0.18).scale(0.8).shift(UP * -1.3)
        stop = VGroup(
            Line(LEFT * 2.2, RIGHT * 2.2, color=ROLLBACK, stroke_width=8),
            text("NO DIRECT EFFECT • NO MINTED AUTHORITY", size=21, color=ROLLBACK, weight="BOLD"),
        ).arrange(UP * -1, buff=0.18).to_edge(UP * -1, buff=0.35)
        self.play(Write(heading), FadeIn(request), FadeIn(abi), FadeIn(proposal), Create(arrows), run_time=1.2)
        self.play(FadeIn(fields), FadeIn(stop), run_time=0.9)

    def families(self) -> None:
        heading = text("DIFFERENT FAMILIES, DIFFERENT OBLIGATIONS", size=34, color=INK, weight="BOLD").to_edge(UP)
        families = VGroup(*[
            card(name, detail, color, 2.55, 1.05)
            for name, detail, color in (
                ("TRANSFORMER", "KV + position", ACCENT),
                ("SSM / RNN", "evolving state", EVIDENCE),
                ("TEST-TIME LEARNER", "mutable fast state", AUTHORITY),
                ("EXTERNAL MEMORY", "addressable store", COPPER),
                ("KAN", "function basis", RESIDUAL),
                ("GRAPH", "relation state", RESIDUAL),
                ("DIFFUSION", "parallel revision", BOUNDARY),
                ("PROGRAM / SEARCH", "exact branches", AUTHORITY),
            )
        ]).arrange_in_grid(rows=2, cols=4, buff=(0.28, 0.45)).scale(0.88).shift(UP * -0.25)
        footer = text("same text I/O does not imply same checkpoint, memory, deletion, or failure semantics", size=20, color=MUTED).to_edge(UP * -1, buff=0.35)
        self.play(Write(heading), run_time=0.8)
        for family in families:
            self.play(FadeIn(family), run_time=0.25)
        self.play(FadeIn(footer), run_time=0.6)

    def routing(self) -> None:
        heading = text("ROUTES SIT ABOVE THE SUBSTRATE", size=38, color=INK, weight="BOLD").to_edge(UP)
        routes = VGroup(*[
            card(name, detail, color, 2.15, 0.9)
            for name, detail, color in (
                ("REFLEX", "narrow + cheap", ACCENT), ("REACTION", "streaming", EVIDENCE),
                ("DELIBERATION", "branch + verify", AUTHORITY), ("SPECIALIST", "task-qualified", COPPER),
            )
        ]).arrange(RIGHT, buff=0.35).shift(UP * 1.0)
        kernels = VGroup(
            card("RULE / KAN", "", ACCENT, 2.0, 0.7),
            card("SSM", "", EVIDENCE, 1.6, 0.7),
            card("MODEL + SEARCH", "", AUTHORITY, 2.35, 0.7),
            card("QUALIFIED KERNEL", "", COPPER, 2.5, 0.7),
        ).arrange(RIGHT, buff=0.4).shift(UP * -0.15)
        arrows = VGroup(*[
            Arrow(routes[i].get_bottom(), kernels[i].get_top(), buff=0.08, color=BOUNDARY)
            for i in range(4)
        ])
        ledger = card(
            "CONTRIBUTION + TOTAL-COST LEDGER",
            "kernel • retrieval • tool • search • verifier • adapter • hardware",
            RESIDUAL, 8.8, 1.15,
        ).shift(UP * -1.75)
        footer = text("KISS = smallest complete governed system", size=23, color=INK, weight="BOLD").to_edge(UP * -1, buff=0.3)
        self.play(Write(heading), FadeIn(routes), run_time=1.0)
        self.play(FadeIn(kernels), Create(arrows), run_time=0.9)
        self.play(FadeIn(ledger), FadeIn(footer), run_time=0.8)

    def architectural_rsi(self) -> None:
        heading = text("ARCHITECTURAL RSI IS A GOVERNED LIFECYCLE", size=33, color=INK, weight="BOLD").to_edge(UP)
        stages = ("PROPOSE", "ISOLATE", "QUALIFY", "COMPARE", "SHADOW", "CANARY", "DECIDE", "RETIRE")
        nodes = VGroup(*[
            card(f"{i + 1} {name}", "", ACCENT if i < 4 else AUTHORITY, 1.55, 0.68)
            for i, name in enumerate(stages)
        ]).arrange(RIGHT, buff=0.17).scale(0.87).shift(UP * 0.55)
        arrows = VGroup(*[
            Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.04, color=BOUNDARY, stroke_width=3)
            for i in range(7)
        ])
        candidate = card("CANDIDATE", "may propose", COPPER, 2.4, 1.0).shift(LEFT * 3.1 + UP * -1.2)
        evaluator = card("EVALUATOR", "independent-enough", EVIDENCE, 2.65, 1.0).shift(UP * -1.2)
        authority = card("APPROVAL GATE", "cannot self-ratify", AUTHORITY, 2.7, 1.0).shift(RIGHT * 3.1 + UP * -1.2)
        rollback = card("ROLLBACK / NARROW / QUARANTINE", "failures + descendants retained", ROLLBACK, 5.1, 0.9).to_edge(UP * -1, buff=0.3)
        self.play(Write(heading), FadeIn(nodes), Create(arrows), run_time=1.2)
        self.play(FadeIn(candidate), FadeIn(evaluator), FadeIn(authority), FadeIn(rollback), run_time=1.0)

    def onecell(self) -> None:
        heading = text("ONECELL: A CANDIDATE DESIGNED TO LOSE CLEANLY", size=32, color=INK, weight="BOLD").to_edge(UP)
        cell = Circle(radius=1.05, color=COPPER, fill_color=SURFACE, fill_opacity=1, stroke_width=6).shift(LEFT * 3.8 + UP * 0.1)
        cell_label = text("SHARED\nCELL", size=27, color=COPPER, weight="BOLD").move_to(cell)
        lanes = VGroup(*[card(x, "", BOUNDARY, 1.5, 0.52) for x in ("belief", "world", "goal", "uncertainty")])
        lanes.arrange(UP * -1, buff=0.14).scale(0.8).shift(LEFT * 1.2 + UP * 0.15)
        exact = card("EXACT STATE", "identity • effects • receipts", EVIDENCE, 2.9, 1.0).shift(RIGHT * 1.55 + UP * 0.85)
        search = card("OUTER SEARCH", "branches + verifier", AUTHORITY, 2.9, 1.0).shift(RIGHT * 1.55 + UP * -0.5)
        defeats = VGroup(*[
            card(label, "", ROLLBACK, 2.15, 0.54)
            for label in ("adapter burden", "answer assistance", "hidden memory", "depth failure", "lane interference", "matched loss")
        ]).arrange_in_grid(rows=3, cols=2, buff=(0.2, 0.15)).scale(0.78).shift(RIGHT * 4.25 + UP * -0.55)
        arrows = VGroup(
            Arrow(cell.get_right(), lanes.get_left(), color=COPPER, buff=0.08),
            Arrow(lanes.get_right(), exact.get_left(), color=EVIDENCE, buff=0.08),
            Arrow(lanes.get_right(), search.get_left(), color=AUTHORITY, buff=0.08),
        )
        self.play(Write(heading), FadeIn(cell), FadeIn(cell_label), run_time=0.9)
        self.play(FadeIn(lanes), FadeIn(exact), FadeIn(search), Create(arrows), run_time=1.0)
        self.play(FadeIn(defeats), run_time=0.9)

    def evidence(self) -> None:
        ledger = VGroup(
            card("16 CASES", "synthetic ABI", EVIDENCE, 2.7, 1.3),
            card("12 REJECTIONS", "malicious mutations", AUTHORITY, 2.7, 1.3),
            card("0 OUTCOME RUNS", "kernel tournament", ROLLBACK, 2.7, 1.3),
        ).arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.35)
        boundary = proof_boundary(
            "NO ARCHITECTURE WINS HERE",
            "KERC inadequate • no semantic, production, energy, or core claim",
        ).scale(0.82).shift(UP * 0.1)
        end = source_end_card(
            "Replaceable Cognitive Substrates",
            "argument • Design rationale",
            "Two narrow finite observations only; broader efficiency remains untested.",
            "Relational Dimension Compilation and Polyadic Cognition",
        ).scale(0.72).to_edge(UP * -1, buff=0.3)
        self.play(FadeIn(ledger), run_time=1.0)
        self.play(Create(boundary), run_time=0.8)
        self.play(FadeIn(end), run_time=1.0)
