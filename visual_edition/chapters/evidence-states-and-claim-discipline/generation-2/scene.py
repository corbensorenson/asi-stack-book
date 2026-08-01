"""Generation-2 visual abstract for Evidence States and Claim Discipline.

One synthetic retrieval-gain claim moves through typed evidence roles, a
non-aggregating quality cell, claim-specific transition gates, adverse-result
lineage, public projection, and an argument-support evidence ceiling.
"""

from __future__ import annotations

from manim import (
    Arrow, Circle, Create, Cross, DashedLine, Dot, FadeIn, FadeOut,
    GrowArrow, GrowFromCenter, Indicate, LaggedStart, LEFT, Line,
    MoveAlongPath, Rectangle, ReplacementTransform, RIGHT, RoundedRectangle,
    Square, Succession, Text, Transform, TransformFromCopy, Triangle, UP,
    VGroup,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


class EvidenceStatesGeneration2(AsiScene):
    TARGET_DURATION = 314.575
    ENDS = [
        12.730, 21.210, 34.665, 48.320, 62.325, 76.330, 89.185,
        104.265, 114.795, 125.575, 138.180, 150.135, 163.415,
        174.120, 185.800, 196.630, 204.360, 208.735, 219.615,
        231.370, 243.775, 254.530, 266.460, 277.840, 292.895,
        304.625, 314.575,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#14262F"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.35) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.05, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            self.play(
                LaggedStart(*animations, lag_ratio=0.13),
                run_time=max(0.05, remaining - min(settle, remaining * 0.2)),
            )
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 18, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 1.9, height: float = 0.54) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.1,
            stroke_color=color, stroke_width=2.5,
            fill_color=SURFACE, fill_opacity=1,
        )
        return VGroup(shell, self.label(value, 13, color, "BOLD").move_to(shell))

    def panel(self, title: str, color: str, width: float = 4.0, height: float = 2.7) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.16,
            stroke_color=color, stroke_width=3,
            fill_color="#172A33", fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.35, 2.9), 0.48).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def grid(self, values: list[str], colors: list[str], columns: int, width: float = 1.65) -> VGroup:
        cells = VGroup(*[self.badge(v, colors[i], width, 0.48) for i, v in enumerate(values)])
        rows = (len(values) + columns - 1) // columns
        cells.arrange_in_grid(rows=rows, cols=columns, buff=(0.18, 0.2))
        return cells

    def claim_card(self, short: bool = False) -> VGroup:
        width = 5.2 if short else 7.0
        shell = RoundedRectangle(
            width=width, height=2.25, corner_radius=0.16,
            stroke_color=ACCENT, stroke_width=4,
            fill_color="#172A33", fill_opacity=1,
        )
        title = self.label("MEMORY ADAPTER", 17, ACCENT, "BOLD").next_to(shell, UP, buff=-0.3)
        result = self.label("HELD-OUT RETRIEVAL  +18%", 24 if not short else 20, INK, "BOLD").move_to(shell)
        return VGroup(shell, title, result)

    def construct(self) -> None:
        # 1 — false confidence and question aperture
        claim = self.claim_card()
        proven = self.badge("PROVEN", EVIDENCE, 2.0, 0.7).rotate(-0.12).shift(RIGHT * 3.8 + UP * 1.25)
        question = Circle(radius=1.2, stroke_color=AUTHORITY, stroke_width=5).shift(RIGHT * 4.8)
        qmark = self.label("?", 52, AUTHORITY, "BOLD").move_to(question)
        scene1 = VGroup(claim, question, qmark)
        self.play_beat(
            1,
            FadeIn(claim, shift=RIGHT * 0.6),
            Succession(
                GrowFromCenter(proven),
                Indicate(proven, color=EVIDENCE),
                FadeOut(proven, shift=UP * 0.35),
                Create(question),
                FadeIn(qmark),
            ),
            settle=0.7,
        )

        # 2 — exact atom seals
        wording = self.badge("WORDING", ACCENT, 1.7).shift(LEFT * 3.3 + UP * -1.65)
        scope = self.badge("SCOPE", AUTHORITY, 1.55).shift(UP * -1.65)
        version = self.badge("VERSION 1", COPPER, 1.8).shift(RIGHT * 3.3 + UP * -1.65)
        seals = VGroup(wording, scope, version)
        seal_edges = VGroup(
            Line(wording.get_top(), claim.get_bottom() + LEFT * 2.4, color=ACCENT),
            Line(scope.get_top(), claim.get_bottom(), color=AUTHORITY),
            Line(version.get_top(), claim.get_bottom() + RIGHT * 2.4, color=COPPER),
        )
        scene2 = VGroup(claim, seals, seal_edges)
        self.play_beat(2, FadeOut(question), FadeOut(qmark), LaggedStart(*[FadeIn(x) for x in seals], lag_ratio=0.18), Create(seal_edges), settle=0.45)

        # 3 — four distinct identities
        rails = self.grid(
            ["LABEL · DESIGN", "SUPPORT · ARGUMENT", "LIFECYCLE · REVIEW", "DISPOSITION · OPEN"],
            [ACCENT, EVIDENCE, AUTHORITY, COPPER], 1, 3.1,
        ).shift(RIGHT * 2.7)
        small_claim = self.claim_card(short=True).scale(0.85).shift(LEFT * 3.7)
        rail_edges = VGroup(*[
            Line(small_claim.get_right(), rail.get_left(), color=[ACCENT, EVIDENCE, AUTHORITY, COPPER][i], stroke_width=2)
            for i, rail in enumerate(rails)
        ])
        scene3 = VGroup(small_claim, rails, rail_edges)
        self.play_beat(3, FadeOut(scene2), FadeIn(small_claim), Create(rail_edges), LaggedStart(*[FadeIn(r) for r in rails], lag_ratio=0.14), settle=0.55)

        # 4 — three synchronized claim views
        proposition = self.panel("PROPOSITION", ACCENT, 3.2, 2.2).shift(LEFT * 4.3 + UP * 1.1)
        obligation = self.panel("OBLIGATION", AUTHORITY, 3.2, 2.2).shift(RIGHT * 4.3 + UP * 1.1)
        predicate = self.panel("PREDICATE", EVIDENCE, 3.2, 2.2).shift(UP * -1.55)
        views = VGroup(proposition, obligation, predicate)
        identity_loop = VGroup(
            Arrow(proposition.get_right(), obligation.get_left(), color=BOUNDARY, buff=0.1),
            Arrow(obligation.get_bottom(), predicate.get_right(), color=BOUNDARY, buff=0.1),
            Arrow(predicate.get_left(), proposition.get_bottom(), color=BOUNDARY, buff=0.1),
        )
        same = self.badge("SAME ATOM · V1", COPPER, 2.3).shift(UP * 0.2)
        substitute = self.badge("V2?", ROLLBACK, 1.2).shift(RIGHT * 5.8 + UP * -1.6)
        substitute_cross = Cross(substitute, stroke_color=ROLLBACK)
        scene4 = VGroup(views, identity_loop, same, substitute, substitute_cross)
        self.play_beat(4, FadeOut(scene3), TransformFromCopy(small_claim, proposition), TransformFromCopy(small_claim, obligation), TransformFromCopy(small_claim, predicate), Create(identity_loop), FadeIn(same), FadeIn(substitute), Create(substitute_cross), settle=0.6)

        # 5 — typed evidence roles
        core = self.claim_card(short=True).scale(0.72)
        artifacts = self.grid(["CITATION", "PROOF", "FIXTURE", "MEASUREMENT"], [ACCENT, EVIDENCE, AUTHORITY, COPPER], 1, 1.9).shift(LEFT * 5.0)
        roles = self.grid(["LINEAGE", "PREDICATE", "BEHAVIOR", "EFFECT"], [ACCENT, EVIDENCE, AUTHORITY, COPPER], 1, 1.9).shift(RIGHT * 5.0)
        role_edges = VGroup(*[Arrow(artifacts[i].get_right(), roles[i].get_left(), color=[ACCENT, EVIDENCE, AUTHORITY, COPPER][i], buff=0.08) for i in range(4)])
        scene5 = VGroup(core, artifacts, roles, role_edges)
        self.play_beat(5, FadeOut(scene4), FadeIn(core), LaggedStart(*[FadeIn(a) for a in artifacts], lag_ratio=0.12), GrowArrow(role_edges[0]), GrowArrow(role_edges[1]), GrowArrow(role_edges[2]), GrowArrow(role_edges[3]), LaggedStart(*[FadeIn(r) for r in roles], lag_ratio=0.12), settle=0.55)

        # 6 — eight-dimensional evidence cell
        cell = self.panel("NON-AGGREGATING EVIDENCE CELL", AUTHORITY, 10.6, 5.1)
        dimensions = self.grid(
            ["INDEPENDENCE", "REPRODUCIBLE", "RECENCY", "COVERAGE", "ADVERSARIAL", "VALIDITY", "ACCESS", "TRANSFER"],
            [ROLLBACK, EVIDENCE, EVIDENCE, AUTHORITY, COPPER, EVIDENCE, ACCENT, AUTHORITY], 4, 2.1,
        ).move_to(cell)
        no_total = self.badge("NO TOTAL SCORE", ROLLBACK, 2.2).shift(UP * -2.7)
        scene6 = VGroup(cell, dimensions, no_total)
        self.play_beat(6, FadeOut(scene5), FadeIn(cell), LaggedStart(*[FadeIn(d) for d in dimensions], lag_ratio=0.1), FadeIn(no_total), settle=0.65)

        # 7 — seven bright dimensions cannot hide weak independence
        bars = VGroup()
        bar_labels = VGroup()
        values = [0.18, 1.25, 1.45, 1.15, 1.35, 1.4, 1.2, 1.05]
        names = ["IND", "REP", "REC", "COV", "ADV", "VAL", "ACC", "XFER"]
        colors = [ROLLBACK] + [EVIDENCE] * 7
        for i, (value, name, color) in enumerate(zip(values, names, colors)):
            bar = Rectangle(width=0.65, height=value, stroke_color=color, fill_color=color, fill_opacity=0.65)
            bar.move_to(LEFT * 3.7 + RIGHT * i * 1.05 + UP * (-1.0 + value / 2))
            bars.add(bar)
            bar_labels.add(self.label(name, 12, color, "BOLD").next_to(bar, UP * -1, buff=0.18))
        average = Circle(radius=1.0, stroke_color=MUTED, stroke_width=4).shift(RIGHT * 5.0 + UP * 0.4)
        avg_label = self.label("AVG", 20, MUTED, "BOLD").move_to(average)
        average_cross = Cross(VGroup(average, avg_label), stroke_color=ROLLBACK)
        scene7 = VGroup(bars, bar_labels, average, avg_label, average_cross)
        self.play_beat(7, FadeOut(scene6), LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.08), FadeIn(bar_labels), Create(average), FadeIn(avg_label), Create(average_cross), settle=0.7)

        # 8 — transition packet construction
        packet = self.panel("TRANSITION PACKET", AUTHORITY, 10.8, 5.2)
        packet_fields = self.grid(
            ["CLAIM + VERSION", "ARTIFACT + ROLE", "SCOPE + METHOD", "NEGATIVE RESULTS", "REVIEWER", "BLOCKERS", "DOWNGRADE", "LIMITS", "NON-CLAIMS"],
            [ACCENT, EVIDENCE, AUTHORITY, ROLLBACK, COPPER, ROLLBACK, ROLLBACK, MUTED, BOUNDARY], 3, 2.65,
        ).move_to(packet)
        pocket = self.badge("ADVERSE EVIDENCE ATTACHED", ROLLBACK, 3.2).shift(UP * -2.8)
        scene8 = VGroup(packet, packet_fields, pocket)
        self.play_beat(8, FadeOut(scene7), FadeIn(packet), LaggedStart(*[FadeIn(f) for f in packet_fields], lag_ratio=0.07), FadeIn(pocket), Create(Line(packet.get_bottom(), pocket.get_top(), color=ROLLBACK)), settle=0.65)

        # 9 — target-specific airlock stays closed
        packet_small = self.panel("PACKET", AUTHORITY, 3.0, 2.6).shift(LEFT * 4.6)
        gate_left = Line(UP * 2.7, UP * -2.7, color=AUTHORITY, stroke_width=7).shift(LEFT * 0.5)
        gate_right = Line(UP * 2.7, UP * -2.7, color=AUTHORITY, stroke_width=7).shift(RIGHT * 0.5)
        slots = self.grid(["SCOPE ✓", "METHOD ✓", "VALIDITY ✓", "INDEPENDENCE —"], [EVIDENCE, EVIDENCE, EVIDENCE, ROLLBACK], 1, 2.25).shift(RIGHT * 2.1)
        target = self.badge("TARGET · EMPIRICAL", AUTHORITY, 2.6).shift(RIGHT * 4.9 + UP * 2.3)
        closed = self.badge("GATE CLOSED", ROLLBACK, 2.2).shift(RIGHT * 4.8 + UP * -2.2)
        scene9 = VGroup(packet_small, gate_left, gate_right, slots, target, closed)
        self.play_beat(9, FadeOut(scene8), FadeIn(packet_small), Create(gate_left), Create(gate_right), LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=0.12), FadeIn(target), FadeIn(closed), settle=0.65)

        # 10 — citation redirected to lineage
        citation = self.badge("CITATION", ACCENT, 1.9).shift(LEFT * 4.7)
        wrong_slot = self.badge("EFFECT?", ROLLBACK, 1.7).shift(RIGHT * 1.0 + UP * 1.2)
        lineage = self.badge("LINEAGE ✓", ACCENT, 2.0).shift(RIGHT * 1.0 + UP * -1.2)
        route = Line(citation.get_right(), lineage.get_left(), color=ACCENT, stroke_width=4)
        unchanged = self.badge("SUPPORT · NO CHANGE", MUTED, 2.8).shift(RIGHT * 4.8)
        wrong_cross = Cross(wrong_slot, stroke_color=ROLLBACK)
        scene10 = VGroup(citation, wrong_slot, wrong_cross, lineage, route, unchanged)
        self.play_beat(10, FadeOut(scene9), Succession(FadeIn(citation), MoveAlongPath(citation, route)), FadeIn(wrong_slot), Create(wrong_cross), Create(route), FadeIn(lineage), FadeIn(unchanged), settle=0.55)

        # 11 — proof remains inside assumptions
        proof_frame = self.panel("THEOREM + ASSUMPTIONS", EVIDENCE, 5.2, 4.2).shift(LEFT * 2.8)
        theorem = self.badge("ENCODED PREDICATE ✓", EVIDENCE, 2.8).move_to(proof_frame)
        stronger = self.grid(["DEPLOYMENT", "USEFULNESS", "ENFORCEMENT"], [ROLLBACK] * 3, 1, 2.2).shift(RIGHT * 4.3)
        stops = VGroup(*[Cross(s, stroke_color=ROLLBACK) for s in stronger])
        scene11 = VGroup(proof_frame, theorem, stronger, stops)
        self.play_beat(11, FadeOut(scene10), FadeIn(proof_frame), FadeIn(theorem), LaggedStart(*[FadeIn(s) for s in stronger], lag_ratio=0.15), Create(stops), settle=0.6)

        # 12 — benchmark denominator enclosure
        score = self.badge("SCORE 0.81", EVIDENCE, 2.0)
        boundary = self.panel("FROZEN DENOMINATOR", AUTHORITY, 9.2, 4.8)
        denom = self.grid(["TASKS", "PROTOCOL", "COMPARATOR", "MEASUREMENT"], [AUTHORITY] * 4, 4, 1.8).shift(UP * 1.0)
        outside = self.grid(["EVERY USER", "ALL DISTRIBUTIONS", "FUTURE VERSION"], [MUTED] * 3, 3, 2.1).shift(UP * -1.4)
        outside_cross = VGroup(*[Cross(x, stroke_color=ROLLBACK) for x in outside])
        scene12 = VGroup(boundary, score, denom, outside, outside_cross)
        self.play_beat(12, FadeOut(scene11), FadeIn(boundary), FadeIn(score), LaggedStart(*[FadeIn(d) for d in denom], lag_ratio=0.12), FadeIn(outside), Create(outside_cross), settle=0.6)

        # 13 — exact worked claim envelope
        worked = self.claim_card().shift(UP * 1.5)
        worked_fields = self.grid(["ADAPTER", "MODEL", "CORPUS", "HELD-OUT", "METRIC", "BASELINE", "CONFIDENCE"], [AUTHORITY] * 7, 4, 1.65).shift(UP * -1.35)
        v1 = self.badge("VERSION 1 · SEALED", COPPER, 2.4).shift(RIGHT * 4.8 + UP * 2.5)
        scene13 = VGroup(worked, worked_fields, v1)
        self.play_beat(13, FadeOut(scene12), FadeIn(worked), LaggedStart(*[FadeIn(f) for f in worked_fields], lag_ratio=0.1), FadeIn(v1), settle=0.65)

        # 14 — source supports rationale, not effect
        rationale = self.panel("DESIGN RATIONALE", ACCENT, 4.0, 3.0).shift(LEFT * 3.7)
        paper = self.badge("PASSAGE-REVIEWED PAPER", ACCENT, 2.9).move_to(rationale)
        effect = self.panel("EFFECT CLAIM", AUTHORITY, 4.0, 3.0).shift(RIGHT * 3.7)
        unmoved = self.badge("SUPPORT UNMOVED", MUTED, 2.4).move_to(effect)
        no_bridge = DashedLine(rationale.get_right(), effect.get_left(), color=ROLLBACK, stroke_width=5)
        scene14 = VGroup(rationale, paper, effect, unmoved, no_bridge)
        self.play_beat(14, FadeOut(scene13), FadeIn(rationale), MoveAlongPath(paper, Line(LEFT * 6.0, paper.get_center(), color=ACCENT)), FadeIn(effect), FadeIn(unmoved), Create(no_bridge), settle=0.55)

        # 15 — fixture subclaim moves, effect does not
        cases = self.grid(["CASE A", "CASE B", "CASE C"], [ACCENT] * 3, 1, 1.5).shift(LEFT * 5.2)
        adapter = self.panel("ADAPTER", AUTHORITY, 2.7, 3.4)
        fixture_claim = self.badge("FIXTURE CLAIM · SYNTHETIC", EVIDENCE, 3.0).shift(RIGHT * 4.5 + UP * 1.0)
        effect_claim = self.badge("EFFECT CLAIM · NO CHANGE", MUTED, 3.0).shift(RIGHT * 4.5 + UP * -1.0)
        case_paths = VGroup(*[Arrow(c.get_right(), adapter.get_left(), color=ACCENT, buff=0.08) for c in cases])
        success = Arrow(adapter.get_right(), fixture_claim.get_left(), color=EVIDENCE, buff=0.08)
        blocked = DashedLine(adapter.get_right(), effect_claim.get_left(), color=ROLLBACK, stroke_width=4)
        scene15 = VGroup(cases, adapter, fixture_claim, effect_claim, case_paths, success, blocked)
        self.play_beat(15, FadeOut(scene14), FadeIn(cases), FadeIn(adapter), Create(case_paths), GrowArrow(success), FadeIn(fixture_claim), Create(blocked), FadeIn(effect_claim), settle=0.6)

        # 16 — missing held-out run becomes a public blocker
        empty_slot = RoundedRectangle(width=4.0, height=1.2, corner_radius=0.12, stroke_color=ROLLBACK, stroke_width=4).shift(UP * 1.1)
        empty_label = self.label("INDEPENDENT HELD-OUT RUN · MISSING", 16, ROLLBACK, "BOLD").move_to(empty_slot)
        closed_gate = self.badge("EMPIRICAL GATE CLOSED", ROLLBACK, 2.9).shift(RIGHT * 4.6 + UP * 1.1)
        ledger = self.panel("PUBLIC LEDGER", AUTHORITY, 6.0, 2.2).shift(UP * -1.7)
        blocker = self.badge("BLOCKER · RUN MISSING", AUTHORITY, 2.8).move_to(ledger)
        scene16 = VGroup(empty_slot, empty_label, closed_gate, ledger, blocker)
        self.play_beat(16, FadeOut(scene15), FadeIn(empty_slot), FadeIn(empty_label), FadeIn(closed_gate), FadeIn(ledger), TransformFromCopy(empty_label, blocker), settle=0.65)

        # 17 — positive control fails visibly
        known = self.badge("KNOWN DIFFERENCE", EVIDENCE, 2.4).shift(LEFT * 5.0)
        instrument = self.panel("TEST INSTRUMENT", AUTHORITY, 3.6, 3.2)
        detector_line = Line(LEFT * 1.2, RIGHT * 1.2, color=MUTED, stroke_width=5).shift(RIGHT * 4.3)
        no_detection = self.badge("NO DETECTION", ROLLBACK, 2.1).next_to(detector_line, UP, buff=0.45)
        path = Arrow(known.get_right(), instrument.get_left(), color=EVIDENCE, buff=0.08)
        scene17 = VGroup(known, instrument, detector_line, no_detection, path)
        self.play_beat(17, FadeOut(scene16), Succession(FadeIn(known), MoveAlongPath(known, path)), FadeIn(instrument), GrowArrow(path), Create(detector_line), FadeIn(no_detection), settle=0.55)

        # 18 — failed control lowers the test, not the effect
        false_negative = self.badge("NO IMPROVEMENT?", ROLLBACK, 2.4).shift(RIGHT * 4.7 + UP * 1.6)
        false_cross = Cross(false_negative, stroke_color=ROLLBACK)
        weak = self.badge("TEST WEAK", ROLLBACK, 2.0).shift(RIGHT * 0.4 + UP * -1.0)
        residual = self.badge("EFFECT RESIDUAL OPEN", AUTHORITY, 2.7).shift(RIGHT * 4.4 + UP * -1.2)
        down = Arrow(instrument.get_right(), weak.get_left(), color=ROLLBACK, buff=0.1)
        scene18 = VGroup(instrument, false_negative, false_cross, weak, residual, down)
        self.play_beat(18, FadeOut(known), FadeOut(detector_line), FadeOut(no_detection), FadeOut(path), FadeIn(false_negative), Create(false_cross), GrowArrow(down), FadeIn(weak), FadeIn(residual), settle=0.45)

        # 19 — complete non-promotion transition fan
        review = self.panel("REVIEW", AUTHORITY, 2.6, 2.2).shift(LEFT * 4.8)
        outcomes = self.grid(["NO CHANGE", "NARROW", "DOWNGRADE", "REFUTE", "DEPRECATE"], [MUTED, AUTHORITY, ROLLBACK, RESIDUAL, COPPER], 1, 2.1).shift(RIGHT * 3.6)
        routes = VGroup(*[Arrow(review.get_right(), o.get_left(), color=[MUTED, AUTHORITY, ROLLBACK, RESIDUAL, COPPER][i], buff=0.08) for i, o in enumerate(outcomes)])
        scene19 = VGroup(review, outcomes, routes)
        self.play_beat(19, FadeOut(scene18), FadeIn(review), LaggedStart(*[GrowArrow(r) for r in routes], lag_ratio=0.12), LaggedStart(*[FadeIn(o) for o in outcomes], lag_ratio=0.12), settle=0.65)

        # 20 — negative evidence remains attached across versions
        v1_card = self.badge("VERSION 1", ACCENT, 2.0).shift(LEFT * 3.6 + UP * 1.3)
        v2_card = self.badge("VERSION 2", EVIDENCE, 2.0).shift(RIGHT * 3.6 + UP * 1.3)
        lineage = Arrow(v1_card.get_right(), v2_card.get_left(), color=BOUNDARY, buff=0.08)
        shadow = self.panel("ADVERSE LINEAGE", ROLLBACK, 9.0, 2.0).shift(UP * -1.5)
        adverse = self.grid(["FAILED CONTROL", "CONTRADICTION", "ABANDONED INFERENCE"], [ROLLBACK] * 3, 3, 2.3).move_to(shadow)
        links = VGroup(Line(v1_card.get_bottom(), shadow.get_top() + LEFT * 2.0, color=ROLLBACK), Line(v2_card.get_bottom(), shadow.get_top() + RIGHT * 2.0, color=ROLLBACK))
        scene20 = VGroup(v1_card, v2_card, lineage, shadow, adverse, links)
        self.play_beat(20, FadeOut(scene19), FadeIn(v1_card), TransformFromCopy(v1_card, v2_card), GrowArrow(lineage), FadeIn(shadow), FadeIn(adverse), Create(links), settle=0.7)

        # 21 — public projection is one-way and not evidence
        internal = self.panel("INTERNAL LEDGER", AUTHORITY, 4.3, 4.4).shift(LEFT * 4.0)
        fields = self.grid(["CLAIM", "SUPPORT", "TRANSITION", "LIMITATION", "RESIDUAL"], [ACCENT, EVIDENCE, AUTHORITY, MUTED, ROLLBACK], 1, 1.8).move_to(internal)
        public = self.panel("APPENDIX C", ACCENT, 4.3, 4.4).shift(RIGHT * 4.0)
        public_fields = fields.copy().move_to(public)
        one_way = Arrow(internal.get_right(), public.get_left(), color=ACCENT, buff=0.1)
        reverse = DashedLine(public.get_left(), internal.get_right(), color=ROLLBACK, stroke_width=4).shift(UP * -0.55)
        reverse_cross = Cross(reverse, stroke_color=ROLLBACK)
        scene21 = VGroup(internal, fields, public, public_fields, one_way, reverse, reverse_cross)
        self.play_beat(21, FadeOut(scene20), FadeIn(internal), Succession(FadeIn(fields), TransformFromCopy(fields, public_fields)), FadeIn(public), GrowArrow(one_way), Create(reverse), Create(reverse_cross), settle=0.65)

        # 22 — related claims do not inherit movement
        center = self.badge("REVIEWED ATOM", EVIDENCE, 2.2)
        parent = self.badge("PARENT", ACCENT, 1.6).shift(UP * 2.4)
        sibling = self.badge("SIBLING", AUTHORITY, 1.6).shift(LEFT * 4.0)
        descendant = self.badge("DESCENDANT", COPPER, 2.0).shift(RIGHT * 4.0)
        edges = VGroup(
            Line(center.get_center(), parent.get_center(), color=BOUNDARY),
            Line(center.get_center(), sibling.get_center(), color=BOUNDARY),
            Line(center.get_center(), descendant.get_center(), color=BOUNDARY),
        )
        locks = VGroup(*[self.badge("LOCK", ROLLBACK, 1.0, 0.4).move_to(e.get_center()) for e in edges])
        scene22 = VGroup(center, parent, sibling, descendant, edges, locks)
        self.play_beat(22, FadeOut(scene21), FadeIn(center), FadeIn(parent), FadeIn(sibling), FadeIn(descendant), Create(edges), LaggedStart(*[FadeIn(l) for l in locks], lag_ratio=0.15), settle=0.65)

        # 23 — decision receipt, not mood
        decision = self.panel("DECISION RECEIPT", AUTHORITY, 8.0, 4.8)
        review_fields = self.grid(["INDEPENDENCE", "DISSENT", "BLOCKERS", "LIMITATIONS", "REASON"], [EVIDENCE, COPPER, ROLLBACK, MUTED, AUTHORITY], 3, 2.0).move_to(decision)
        slider = Line(LEFT * 1.6, RIGHT * 1.6, color=MUTED, stroke_width=5).shift(LEFT * 5.1)
        slider_dot = Dot(slider.get_center() + RIGHT * 0.7, color=MUTED)
        mood = self.badge("MOOD", MUTED, 1.4).next_to(slider, UP, buff=0.35)
        mood_cross = Cross(VGroup(slider, slider_dot, mood), stroke_color=ROLLBACK)
        scene23 = VGroup(decision, review_fields, slider, slider_dot, mood, mood_cross)
        self.play_beat(23, FadeOut(scene22), FadeIn(slider), FadeIn(slider_dot), FadeIn(mood), Create(mood_cross), FadeIn(decision), LaggedStart(*[FadeIn(f) for f in review_fields], lag_ratio=0.12), settle=0.65)

        # 24 — public state is a lossy projection, never a sum
        facets = self.grid(["IND", "REP", "REC", "COV", "ADV", "VAL", "ACC", "XFER"], [ROLLBACK, EVIDENCE, EVIDENCE, AUTHORITY, COPPER, EVIDENCE, ACCENT, AUTHORITY], 2, 1.25).shift(LEFT * 4.7)
        aperture = RoundedRectangle(width=1.2, height=4.8, corner_radius=0.1, stroke_color=AUTHORITY, stroke_width=4)
        lossy = self.badge("LOSSY", AUTHORITY, 1.4).next_to(aperture, UP, buff=0.25)
        support = self.panel("PUBLIC STATE", ACCENT, 3.9, 2.8).shift(RIGHT * 4.2)
        argument = self.badge("SUPPORT · ARGUMENT", ACCENT, 2.7).move_to(support)
        no_sum = self.badge("NO CONFIDENCE SUM", ROLLBACK, 2.6).shift(RIGHT * 4.2 + UP * -2.3)
        scene24 = VGroup(facets, aperture, lossy, support, argument, no_sum)
        self.play_beat(24, FadeOut(scene23), Succession(FadeIn(facets), TransformFromCopy(facets, argument)), Create(aperture), FadeIn(lossy), FadeIn(support), FadeIn(no_sum), settle=0.7)

        # 25 — exact current evidence ceiling
        enclosure = self.panel("ARGUMENT SUPPORT", AUTHORITY, 9.2, 4.8).shift(LEFT * 1.0)
        bounded = self.grid(["SCHEMAS", "FINITE PROOFS", "SYNTHETIC MUTATIONS"], [ACCENT, EVIDENCE, COPPER], 3, 2.2).move_to(enclosure)
        deployment = self.badge("DEPLOYMENT VALIDATED?", ROLLBACK, 2.8).shift(RIGHT * 5.0)
        deployment_cross = Cross(deployment, stroke_color=ROLLBACK)
        scene25 = VGroup(enclosure, bounded, deployment, deployment_cross)
        self.play_beat(25, FadeOut(scene24), FadeIn(enclosure), LaggedStart(*[FadeIn(b) for b in bounded], lag_ratio=0.15), FadeIn(deployment), Create(deployment_cross), settle=0.8)

        # 26 — clearer prose cannot move support; accepted packet can
        prose_axis = Line(LEFT * 4.5, RIGHT * 4.5, color=ACCENT, stroke_width=4).shift(UP * 1.7)
        support_axis = Line(LEFT * 4.5, RIGHT * 4.5, color=AUTHORITY, stroke_width=4).shift(UP * -1.2)
        prose_dot = Dot(prose_axis.get_left() + RIGHT * 1.1, color=ACCENT)
        clearer_dot = Dot(prose_axis.get_right() + LEFT * 1.1, color=EVIDENCE)
        support_dot = Dot(support_axis.get_left() + RIGHT * 1.1, color=AUTHORITY)
        accepted_dot = Dot(support_axis.get_right() + LEFT * 1.1, color=EVIDENCE)
        prose_label = self.badge("CLEARER PROSE", ACCENT, 2.1).next_to(prose_axis, UP, buff=0.3)
        transition_label = self.badge("ACCEPTED TRANSITION", AUTHORITY, 2.7).next_to(support_axis, UP * -1, buff=0.35)
        no_auto = self.badge("NO AUTOMATIC PROMOTION", ROLLBACK, 2.8)
        scene26 = VGroup(prose_axis, support_axis, prose_dot, clearer_dot, support_dot, accepted_dot, prose_label, transition_label, no_auto)
        self.play_beat(26, FadeOut(scene25), Create(prose_axis), Succession(FadeIn(prose_dot), TransformFromCopy(prose_dot, clearer_dot)), FadeIn(prose_label), Create(support_axis), Succession(FadeIn(support_dot), TransformFromCopy(support_dot, accepted_dot)), Succession(FadeIn(no_auto), FadeOut(no_auto)), FadeIn(transition_label), settle=0.8)

        # 27 — oversight aperture handoff
        packet_final = self.panel("BOUNDED CLAIM PACKET", AUTHORITY, 3.7, 3.2).shift(LEFT * 4.6)
        aperture_final = RoundedRectangle(width=1.0, height=5.0, corner_radius=0.1, stroke_color=ACCENT, stroke_width=4)
        reviewer = self.panel("WEAKER REVIEWER", ACCENT, 3.0, 2.5).shift(RIGHT * 2.0)
        hidden = self.panel("STRONGER WORK TRACE", COPPER, 4.3, 4.4).shift(RIGHT * 5.2)
        visible_slice = Rectangle(width=0.8, height=1.6, stroke_color=EVIDENCE, fill_color=EVIDENCE, fill_opacity=0.25).move_to(aperture_final)
        handoff = Arrow(packet_final.get_right(), aperture_final.get_left(), color=AUTHORITY, buff=0.08)
        question_final = self.badge("CAN THE EVIDENCE BE SEEN?", AUTHORITY, 3.2).shift(UP * -2.8)
        scene27 = VGroup(packet_final, aperture_final, reviewer, hidden, visible_slice, handoff, question_final)
        self.play_beat(27, FadeOut(scene26), FadeIn(packet_final), Create(aperture_final), GrowArrow(handoff), FadeIn(reviewer), FadeIn(hidden), FadeIn(visible_slice), FadeIn(question_final), settle=0.8)
