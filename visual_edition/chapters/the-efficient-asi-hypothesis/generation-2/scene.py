"""Generation-two visual abstract for ``The Efficient ASI Hypothesis``.

One invoice keeps its identity while visible price, repair, review, authority,
reuse, expiry, and evidence boundaries accumulate into a complete causal bill.
"""

from __future__ import annotations

from manim import (
    AnimationGroup,
    Arrow,
    Brace,
    Circle,
    Circumscribe,
    Create,
    DashedLine,
    DOWN,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    LEFT,
    Line,
    MoveAlongPath,
    ORIGIN,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    RoundedRectangle,
    Succession,
    Transform,
    TransformFromCopy,
    UP,
    VGroup,
    Write,
)

from visual_edition.lib.asi_visuals import (
    ACCENT,
    AUTHORITY,
    BACKGROUND,
    BOUNDARY,
    COPPER,
    EVIDENCE,
    INK,
    MUTED,
    RESIDUAL,
    ROLLBACK,
    SURFACE,
    AsiScene,
    residual_marker,
    text,
)


class EfficientAsiHypothesisGeneration2(AsiScene):
    TARGET_DURATION = 172.540
    ENDS = [
        11.980,
        24.085,
        33.290,
        43.470,
        52.875,
        66.805,
        79.285,
        89.115,
        102.695,
        111.975,
        131.205,
        143.535,
        162.840,
        172.540,
    ]

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def beat(self, index: int, *animations, settle: float = 0.38) -> None:
        self.next_section(f"b{index:02d}")
        end = self.ENDS[index - 1]
        remaining = max(0.05, end - self.renderer.time)
        run_time = max(0.05, remaining - min(settle, remaining * 0.24))
        fade_prefix = []
        for animation in animations:
            if isinstance(animation, FadeOut):
                fade_prefix.append(animation)
            else:
                break
        content = animations[len(fade_prefix):]
        if fade_prefix and content:
            fade_time = min(0.8, run_time * 0.16)
            self.play(
                Succession(
                    AnimationGroup(*fade_prefix, lag_ratio=0, run_time=fade_time),
                    LaggedStart(
                        *content,
                        lag_ratio=0.16,
                        run_time=max(0.05, run_time - fade_time),
                    ),
                )
            )
        elif animations:
            self.play(LaggedStart(*animations, lag_ratio=0.16, run_time=run_time))
        self.wait_until(end)

    @staticmethod
    def label(value: str, size: int = 21, color: str = INK, weight: str = "NORMAL"):
        return text(value, size=size, color=color, weight=weight)

    def invoice(self, *, damaged: bool = False, version: str = "v3") -> VGroup:
        page = RoundedRectangle(
            width=2.18,
            height=2.72,
            corner_radius=0.10,
            color=BOUNDARY,
            stroke_width=2.8,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        fold = VGroup(
            Line(page.get_corner(UP + RIGHT) + LEFT * 0.34, page.get_corner(UP + RIGHT) + DOWN * 0.34, color=BOUNDARY),
            Line(page.get_corner(UP + RIGHT) + LEFT * 0.34, page.get_corner(UP + RIGHT) + DOWN * 0.34, color=BOUNDARY),
        )
        title = self.label("INVOICE 47", 18, INK, "BOLD").move_to(UP * 0.96)
        version_tag = self.label(version.upper(), 11, COPPER, "BOLD").move_to(RIGHT * 0.72 + UP * 0.96)
        vendor = self.label("VENDOR   AURORA", 12, MUTED).move_to(UP * 0.42)
        subtotal = self.label("SUBTOTAL       84", 12, MUTED).move_to(UP * 0.02)
        tax_value = "?" if damaged else "7"
        tax = self.label(f"TAX                  {tax_value}", 13, ROLLBACK if damaged else MUTED, "BOLD" if damaged else "NORMAL").move_to(DOWN * 0.38)
        total = self.label("TOTAL              91", 14, ACCENT, "BOLD").move_to(DOWN * 0.82)
        identity = Circle(radius=0.075, color=ACCENT, fill_color=ACCENT, fill_opacity=1).move_to(LEFT * 0.82 + UP * 0.97)
        return VGroup(page, fold, title, version_tag, vendor, subtotal, tax, total, identity)

    def fare(self, value: str, route: str, color: str) -> VGroup:
        coin = Circle(radius=0.34, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        amount = self.label(value, 22, color, "BOLD").move_to(coin)
        route_label = self.label(route, 12, MUTED, "BOLD").next_to(coin, DOWN, buff=0.10)
        return VGroup(coin, amount, route_label)

    def acceptance_stencil(self) -> VGroup:
        frame = RoundedRectangle(
            width=2.22,
            height=3.48,
            corner_radius=0.13,
            color=EVIDENCE,
            stroke_width=3.2,
            fill_color=BACKGROUND,
            fill_opacity=0.25,
        )
        title = self.label("ACCEPT", 15, EVIDENCE, "BOLD").move_to(frame.get_top() + DOWN * 0.28)
        requirements = VGroup(
            self.requirement("TOTAL", ACCENT),
            self.requirement("VENDOR", ACCENT),
            self.requirement("PRIVACY", AUTHORITY),
        ).arrange(DOWN, buff=0.36).move_to(frame.get_center() + DOWN * 0.15)
        return VGroup(frame, title, requirements)

    def requirement(self, name: str, color: str) -> VGroup:
        socket = RoundedRectangle(width=1.42, height=0.48, corner_radius=0.06, color=color, stroke_width=2)
        name_mob = self.label(name, 12, color, "BOLD").move_to(socket)
        return VGroup(socket, name_mob)

    def seal(self, label: str, color: str = EVIDENCE) -> VGroup:
        ring = Circle(radius=0.31, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        tick = VGroup(
            Line(LEFT * 0.13 + DOWN * 0.01, LEFT * 0.01 + DOWN * 0.13, color=color, stroke_width=4),
            Line(LEFT * 0.01 + DOWN * 0.13, RIGHT * 0.18 + UP * 0.13, color=color, stroke_width=4),
        ).move_to(ring)
        tag = self.label(label, 11, color, "BOLD").next_to(ring, DOWN, buff=0.08)
        return VGroup(ring, tick, tag)

    def bill_tag(self, amount: str, label: str, color: str) -> VGroup:
        shell = RoundedRectangle(
            width=1.58,
            height=0.82,
            corner_radius=0.08,
            color=color,
            stroke_width=2.5,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        amount_mob = self.label(amount, 22, color, "BOLD").move_to(shell.get_center() + UP * 0.13)
        label_mob = self.label(label, 11, MUTED, "BOLD").move_to(shell.get_center() + DOWN * 0.20)
        return VGroup(shell, amount_mob, label_mob)

    def selector_gate(self, label: str, color: str) -> VGroup:
        ring = Circle(radius=0.48, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        tick = VGroup(
            Line(LEFT * 0.17 + DOWN * 0.02, LEFT * 0.02 + DOWN * 0.16, color=color, stroke_width=4),
            Line(LEFT * 0.02 + DOWN * 0.16, RIGHT * 0.22 + UP * 0.17, color=color, stroke_width=4),
        ).move_to(ring)
        words = self.label(label, 12, color, "BOLD").next_to(ring, DOWN, buff=0.10)
        return VGroup(ring, tick, words)

    def construct(self) -> None:
        # b01: one invariant invoice faces four visibly priced routes.
        self.invoice_page = self.invoice().scale(0.82).shift(LEFT * 5.35 + UP * 0.10)
        rail_ys = [2.25, 0.80, -0.65, -2.10]
        route_names = ["PARSER", "SPECIALIST", "FRONTIER", "HUMAN"]
        route_colors = [ACCENT, COPPER, AUTHORITY, EVIDENCE]
        route_values = ["1", "4", "9", "H"]
        self.rails = VGroup(*[
            Line(LEFT * 3.72 + UP * y, RIGHT * 3.82 + UP * y, color=color, stroke_width=2.5)
            for y, color in zip(rail_ys, route_colors)
        ])
        self.fares = VGroup(*[
            self.fare(value, name, color).scale(0.88).move_to(RIGHT * 5.25 + UP * y)
            for value, name, color, y in zip(route_values, route_names, route_colors, rail_ys)
        ])
        route_dots = VGroup(*[
            Circle(radius=0.10, color=color, fill_color=color, fill_opacity=1).move_to(LEFT * 3.35 + UP * y)
            for y, color in zip(rail_ys, route_colors)
        ])
        self.question = self.label("WHICH ROUTE IS EFFICIENT?", 25, INK, "BOLD").shift(UP * 3.45)
        self.beat(
            1,
            FadeIn(self.invoice_page, shift=RIGHT * 0.20),
            LaggedStart(*[Create(rail) for rail in self.rails], lag_ratio=0.10),
            LaggedStart(*[GrowFromCenter(dot) for dot in route_dots], lag_ratio=0.10),
            LaggedStart(*[GrowFromCenter(fare) for fare in self.fares], lag_ratio=0.10),
            Write(self.question),
            settle=0.55,
        )

        # b02: the acceptance stencil, rather than the menu, owns the comparison.
        self.stencil = self.acceptance_stencil().shift(RIGHT * 4.78)
        field_beams = VGroup(
            DashedLine(self.invoice_page[6].get_right(), self.stencil[2][0].get_left(), color=ACCENT, dash_length=0.12),
            DashedLine(self.invoice_page[4].get_right(), self.stencil[2][1].get_left(), color=ACCENT, dash_length=0.12),
            DashedLine(self.invoice_page.get_right() + DOWN * 0.95, self.stencil[2][2].get_left(), color=AUTHORITY, dash_length=0.12),
        )
        self.beat(
            2,
            FadeOut(self.question),
            FadeOut(self.fares),
            FadeOut(route_dots),
            FadeIn(self.stencil, shift=LEFT * 0.25),
            LaggedStart(*[Create(beam) for beam in field_beams], lag_ratio=0.16),
            settle=0.62,
        )

        # b03: a familiar invoice clears the cheap parser and the common test.
        parser = VGroup(
            RoundedRectangle(width=1.70, height=1.18, corner_radius=0.10, color=ACCENT, stroke_width=3, fill_color=SURFACE, fill_opacity=1),
            self.label("PARSER", 16, ACCENT, "BOLD"),
            self.label("1 UNIT", 12, INK, "BOLD").shift(DOWN * 0.28),
        ).shift(LEFT * 0.25 + UP * 0.80)
        familiar = self.invoice_page.copy().scale(0.52).move_to(LEFT * 3.15 + UP * 0.80)
        parser_path = Line(familiar.get_center(), parser.get_center(), color=ACCENT)
        accepted = self.seal("PASS").shift(RIGHT * 2.15 + UP * 0.80)
        parser_pass_arrow = Arrow(parser.get_right(), accepted.get_left(), color=EVIDENCE, buff=0.12)
        self.beat(
            3,
            FadeOut(field_beams),
            FadeOut(self.rails),
            FadeOut(self.invoice_page),
            FadeIn(parser),
            Succession(FadeIn(familiar), MoveAlongPath(familiar, parser_path)),
            TransformFromCopy(parser, accepted),
            GrowArrow(parser_pass_arrow),
            Indicate(self.stencil, color=EVIDENCE),
        )

        # b04: one damaged field triggers repair and review while retaining identity.
        damaged = self.invoice(damaged=True).scale(0.58).move_to(LEFT * 3.20 + UP * 0.75)
        wrong = self.label("TOTAL 84", 18, ROLLBACK, "BOLD").shift(RIGHT * 1.72 + UP * 0.78)
        fail_cross = VGroup(
            Line(LEFT * 0.18 + DOWN * 0.18, RIGHT * 0.18 + UP * 0.18, color=ROLLBACK, stroke_width=5),
            Line(LEFT * 0.18 + UP * 0.18, RIGHT * 0.18 + DOWN * 0.18, color=ROLLBACK, stroke_width=5),
        ).shift(RIGHT * 3.10 + UP * 0.78)
        repair = self.bill_tag("+8", "REPAIR", COPPER).shift(LEFT * 0.82 + DOWN * 1.65)
        review = self.bill_tag("+3", "REVIEW", AUTHORITY).shift(RIGHT * 1.02 + DOWN * 1.65)
        self.beat(
            4,
            FadeOut(familiar),
            FadeOut(accepted),
            FadeOut(parser_pass_arrow),
            FadeIn(damaged),
            Circumscribe(damaged[6], color=ROLLBACK),
            TransformFromCopy(parser, wrong),
            Create(fail_cross),
            LaggedStart(FadeIn(repair, shift=UP * 0.18), FadeIn(review, shift=UP * 0.18), lag_ratio=0.30),
            settle=0.42,
        )

        # b05: the signature arithmetic reverses the route ranking.
        one = self.bill_tag("1", "VISIBLE", ACCENT).shift(LEFT * 3.05 + UP * 0.55)
        repair_target = repair.copy().move_to(LEFT * 1.20 + UP * 0.55)
        review_target = review.copy().move_to(RIGHT * 0.65 + UP * 0.55)
        plus_a = self.label("+", 27, MUTED, "BOLD").move_to(LEFT * 2.12 + UP * 0.55)
        plus_b = self.label("+", 27, MUTED, "BOLD").move_to(LEFT * 0.28 + UP * 0.55)
        equals = self.label("=", 28, MUTED, "BOLD").move_to(RIGHT * 1.66 + UP * 0.55)
        twelve = self.fare("12", "ACTUAL", ROLLBACK).scale(1.08).move_to(RIGHT * 2.65 + UP * 0.55)
        nine = self.fare("9", "VERIFIED", AUTHORITY).scale(1.08).move_to(RIGHT * 4.62 + UP * 0.55)
        balance = Line(RIGHT * 2.15 + DOWN * 1.20, RIGHT * 5.15 + DOWN * 1.20, color=BOUNDARY, stroke_width=4)
        pivot = VGroup(
            Line(RIGHT * 3.65 + DOWN * 1.20, RIGHT * 3.30 + DOWN * 1.92, color=BOUNDARY, stroke_width=4),
            Line(RIGHT * 3.65 + DOWN * 1.20, RIGHT * 4.00 + DOWN * 1.92, color=BOUNDARY, stroke_width=4),
        )
        self.beat(
            5,
            FadeOut(VGroup(parser, damaged, wrong, fail_cross, self.stencil)),
            FadeIn(one),
            Write(plus_a),
            repair.animate.move_to(repair_target),
            Write(plus_b),
            review.animate.move_to(review_target),
            Write(equals),
            GrowFromCenter(twelve),
            GrowFromCenter(nine),
            Succession(Create(balance), balance.animate.rotate(-0.10)),
            Create(pivot),
        )

        # b06: authorization, contract, and complete cost are separate selector gates.
        arithmetic = VGroup(one, plus_a, repair, plus_b, review, equals, twelve, nine, balance, pivot)
        route_token = self.invoice().scale(0.38).shift(LEFT * 5.45 + UP * 0.35)
        gates = VGroup(
            self.selector_gate("AUTHORIZED", AUTHORITY),
            self.selector_gate("CONTRACT", EVIDENCE),
            self.selector_gate("FULL COST", ACCENT),
        ).arrange(RIGHT, buff=1.18).shift(RIGHT * 0.15 + UP * 0.35)
        connectors = VGroup(*[
            Arrow(gates[i].get_right(), gates[i + 1].get_left(), color=BOUNDARY, buff=0.16, stroke_width=2.5)
            for i in range(2)
        ])
        eligible = self.label("LEAST COSTLY ELIGIBLE ROUTE", 23, INK, "BOLD").shift(DOWN * 2.20)
        self.beat(
            6,
            FadeOut(arithmetic),
            Succession(
                FadeIn(route_token),
                *[route_token.animate.move_to(gate.get_center()) for gate in gates],
            ),
            LaggedStart(*[FadeIn(gate, shift=UP * 0.16) for gate in gates], lag_ratio=0.20),
            LaggedStart(*[GrowArrow(connector) for connector in connectors], lag_ratio=0.22),
            Write(eligible),
            settle=0.70,
        )

        # b07: routing is a condition-dependent boundary, not a fixed winner.
        conditions = VGroup(
            self.label("FAMILIAR", 14, ACCENT, "BOLD"),
            self.label("UNCERTAIN", 14, COPPER, "BOLD"),
            self.label("HIGH CONSEQUENCE", 14, AUTHORITY, "BOLD"),
        ).arrange(DOWN, buff=0.95).shift(LEFT * 4.65 + UP * 0.15)
        destinations = VGroup(
            self.fare("1", "PARSER", ACCENT),
            self.fare("4", "SPECIALIST", COPPER),
            VGroup(self.fare("9", "MODEL", AUTHORITY), self.fare("H", "PERSON", EVIDENCE)).arrange(RIGHT, buff=0.44),
        ).arrange(DOWN, buff=0.61).shift(RIGHT * 3.82 + UP * 0.15)
        route_arrows = VGroup(*[
            Arrow(source.get_right(), destination.get_left(), color=color, buff=0.18, stroke_width=3)
            for source, destination, color in zip(conditions, destinations, [ACCENT, COPPER, AUTHORITY])
        ])
        boundary = DashedLine(DOWN * 2.72, UP * 2.72, color=BOUNDARY, dash_length=0.16).shift(LEFT * 0.18)
        self.beat(
            7,
            FadeOut(VGroup(route_token, gates, connectors, eligible)),
            FadeIn(conditions),
            Create(boundary),
            FadeIn(destinations),
            LaggedStart(*[GrowArrow(arrow) for arrow in route_arrows], lag_ratio=0.22),
            settle=0.68,
        )

        # b08: retries and repairs stay inside the policy's measurement window.
        window = RoundedRectangle(width=9.55, height=4.60, corner_radius=0.14, color=RESIDUAL, stroke_width=3)
        window_title = self.label("MEASUREMENT WINDOW", 15, RESIDUAL, "BOLD").next_to(window, UP, buff=0.12)
        attempt = self.bill_tag("1", "ATTEMPT", ACCENT).shift(LEFT * 3.20 + UP * 0.45)
        failure = self.bill_tag("X", "FAILED", ROLLBACK).shift(LEFT * 0.90 + UP * 0.45)
        repair_bill = self.bill_tag("8", "REPAIR", COPPER).shift(RIGHT * 1.40 + UP * 0.45)
        accepted_bill = self.bill_tag("3", "REVIEW", AUTHORITY).shift(RIGHT * 3.70 + UP * 0.45)
        causal_links = VGroup(
            Arrow(attempt.get_right(), failure.get_left(), color=BOUNDARY, buff=0.12),
            Arrow(failure.get_right(), repair_bill.get_left(), color=BOUNDARY, buff=0.12),
            Arrow(repair_bill.get_right(), accepted_bill.get_left(), color=BOUNDARY, buff=0.12),
        )
        residual = residual_marker("NO HIDDEN RETRY").shift(DOWN * 1.55)
        self.beat(
            8,
            FadeOut(VGroup(conditions, destinations, route_arrows, boundary)),
            Create(window),
            Write(window_title),
            LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in [attempt, failure, repair_bill, accepted_bill]], lag_ratio=0.16),
            LaggedStart(*[GrowArrow(link) for link in causal_links], lag_ratio=0.18),
            FadeIn(residual),
        )

        # b09: verified repetition compiles into a versioned artifact that can expire.
        traces = VGroup(*[
            self.invoice(version="v3").scale(0.32).shift(LEFT * 4.70 + UP * y)
            for y in [1.75, 0.55, -0.65]
        ])
        funnel_lines = VGroup(*[
            Line(trace.get_right(), RIGHT * 0.05 + UP * 0.35, color=ACCENT, stroke_width=2)
            for trace in traces
        ])
        artifact = VGroup(
            RoundedRectangle(width=2.70, height=1.45, corner_radius=0.10, color=EVIDENCE, stroke_width=3, fill_color=SURFACE, fill_opacity=1),
            self.label("TEMPLATE v3", 20, EVIDENCE, "BOLD").shift(UP * 0.22),
            self.label("VERIFIED", 12, MUTED, "BOLD").shift(DOWN * 0.24),
        ).shift(RIGHT * 1.40 + UP * 0.35)
        changed = self.invoice(version="v4").scale(0.40).shift(RIGHT * 5.20 + UP * 0.35)
        expiry_cross = VGroup(
            Line(LEFT * 0.20 + DOWN * 0.20, RIGHT * 0.20 + UP * 0.20, color=ROLLBACK, stroke_width=5),
            Line(LEFT * 0.20 + UP * 0.20, RIGHT * 0.20 + DOWN * 0.20, color=ROLLBACK, stroke_width=5),
        ).move_to(artifact.get_corner(UP + RIGHT) + LEFT * 0.28 + DOWN * 0.24)
        expiry = VGroup(
            expiry_cross,
            self.label("EXPIRED BY v4", 14, ROLLBACK, "BOLD").next_to(artifact, DOWN, buff=0.16),
        )
        version_change_arrow = Arrow(changed.get_left(), artifact.get_right(), color=ROLLBACK, buff=0.15)
        self.beat(
            9,
            FadeOut(VGroup(window, window_title, attempt, failure, repair_bill, accepted_bill, causal_links, residual)),
            LaggedStart(*[FadeIn(trace, shift=RIGHT * 0.18) for trace in traces], lag_ratio=0.12),
            LaggedStart(*[Create(line) for line in funnel_lines], lag_ratio=0.12),
            TransformFromCopy(traces, artifact),
            FadeIn(changed, shift=LEFT * 0.20),
            GrowArrow(version_change_arrow),
            Create(expiry),
            settle=0.68,
        )

        # b10: changed human and privacy costs invalidate the previous ranking.
        cheap_review = self.bill_tag("0.2", "REVIEW", EVIDENCE).shift(LEFT * 3.05 + UP * 0.30)
        privacy = self.bill_tag("HIGH", "PRIVACY RISK", ROLLBACK).shift(RIGHT * 0.10 + UP * 0.30)
        compute = self.bill_tag("1", "COMPUTE", ACCENT).shift(RIGHT * 3.20 + UP * 0.30)
        changed_question = self.label("DOES 1 STILL WIN?", 25, INK, "BOLD").shift(DOWN * 1.62)
        risk_bar = Line(LEFT * 0.70, RIGHT * 0.70, color=ROLLBACK, stroke_width=8).next_to(privacy, UP, buff=0.22)
        self.beat(
            10,
            FadeOut(VGroup(traces, funnel_lines, artifact, changed, expiry, version_change_arrow)),
            LaggedStart(FadeIn(cheap_review), FadeIn(privacy), FadeIn(compute), lag_ratio=0.18),
            Succession(Create(risk_bar), risk_bar.animate.scale(1.75)),
            Write(changed_question),
        )

        # b11: every material burden joins the same causal bill.
        terms = VGroup(
            self.bill_tag("M", "MODEL", ACCENT),
            self.bill_tag("C", "CONTEXT", COPPER),
            self.bill_tag("V", "VERIFY", EVIDENCE),
            self.bill_tag("R", "REPAIR", ROLLBACK),
            self.bill_tag("H", "HUMAN", AUTHORITY),
            self.bill_tag("G", "REGRESS", BOUNDARY),
            self.bill_tag("B", "ROLLBACK", RESIDUAL),
        ).arrange(RIGHT, buff=0.18).scale(0.70).shift(UP * 0.65)
        bill_line = Line(terms.get_left() + DOWN * 0.84, terms.get_right() + DOWN * 0.84, color=BOUNDARY, stroke_width=3)
        total_brace = Brace(bill_line, DOWN, color=INK)
        complete_cost = self.label("COMPLETE CAUSAL BILL", 24, INK, "BOLD").next_to(total_brace, DOWN, buff=0.16)
        changing_arrows = VGroup(*[
            Arrow(term.get_bottom(), bill_line.point_from_proportion(i / 6), color=term[0].get_color(), buff=0.10, stroke_width=2)
            for i, term in enumerate(terms)
        ])
        self.beat(
            11,
            FadeOut(VGroup(cheap_review, privacy, compute, changed_question, risk_bar)),
            LaggedStart(*[FadeIn(term, shift=UP * 0.18) for term in terms], lag_ratio=0.12),
            Create(bill_line),
            LaggedStart(*[GrowArrow(arrow) for arrow in changing_arrows], lag_ratio=0.10),
            GrowFromCenter(total_brace),
            Write(complete_cost),
            settle=0.72,
        )

        # b12: matched lanes make useful accepted work and burdens comparable.
        workload = self.invoice().scale(0.42).shift(LEFT * 5.45 + UP * 0.30)
        policy_labels = ["ALWAYS 1", "ROUTED", "ALWAYS 9", "HUMAN"]
        lane_colors = [ACCENT, COPPER, AUTHORITY, EVIDENCE]
        lane_ys = [2.15, 0.85, -0.45, -1.75]
        lanes = VGroup(*[
            Line(LEFT * 3.82 + UP * y, RIGHT * 3.52 + UP * y, color=color, stroke_width=2.5)
            for y, color in zip(lane_ys, lane_colors)
        ])
        policy_names = VGroup(*[
            self.label(name, 12, color, "BOLD").next_to(lane, LEFT, buff=0.12)
            for name, color, lane in zip(policy_labels, lane_colors, lanes)
        ])
        outcomes = VGroup(*[
            VGroup(
                self.seal("ACCEPTED", color).scale(0.72),
                self.label("BURDEN  —", 11, MUTED, "BOLD").shift(DOWN * 0.58),
            ).move_to(RIGHT * 4.55 + UP * y)
            for y, color in zip(lane_ys, lane_colors)
        ])
        copies = VGroup(*[workload.copy().move_to(LEFT * 3.35 + UP * y) for y in lane_ys])
        self.beat(
            12,
            FadeOut(VGroup(terms, bill_line, changing_arrows, total_brace, complete_cost)),
            FadeIn(workload),
            LaggedStart(*[Create(lane) for lane in lanes], lag_ratio=0.10),
            FadeIn(policy_names),
            Succession(
                LaggedStart(*[TransformFromCopy(workload, copy) for copy in copies], lag_ratio=0.10),
                LaggedStart(*[copy.animate.move_to(lane.get_end()) for copy, lane in zip(copies, lanes)], lag_ratio=0.10),
            ),
            LaggedStart(*[FadeIn(outcome) for outcome in outcomes], lag_ratio=0.10),
            settle=0.66,
        )

        # b13: the argument specifies the experiment but leaves result sockets empty.
        boundary_box = RoundedRectangle(width=10.80, height=5.18, corner_radius=0.14, color=BOUNDARY, stroke_width=3)
        boundary_label = self.label("ARGUMENT BOUNDARY", 16, BOUNDARY, "BOLD").next_to(boundary_box, UP, buff=0.12)
        known = VGroup(
            self.label("FINITE LIST", 17, EVIDENCE, "BOLD"),
            self.label("ELIGIBLE MINIMUM", 17, EVIDENCE, "BOLD"),
            self.label("7-CLASS TOTAL", 17, EVIDENCE, "BOLD"),
        ).arrange(DOWN, buff=0.42).shift(LEFT * 2.75 + UP * 0.25)
        unknown = VGroup(
            self.label("COMPLETE SEARCH", 15, MUTED, "BOLD"),
            self.label("COST TRUTH", 15, MUTED, "BOLD"),
            self.label("MEASURED RESULT", 15, MUTED, "BOLD"),
        ).arrange(DOWN, buff=0.42).shift(RIGHT * 2.60 + UP * 0.25)
        empty_sockets = VGroup(*[
            RoundedRectangle(width=3.15, height=0.60, corner_radius=0.06, color=BOUNDARY, stroke_width=2).move_to(item)
            for item in unknown
        ])
        divider = DashedLine(DOWN * 1.85, UP * 1.85, color=BOUNDARY, dash_length=0.15)
        self.beat(
            13,
            FadeOut(VGroup(workload, lanes, policy_names, copies, outcomes)),
            Create(boundary_box),
            Write(boundary_label),
            Create(divider),
            LaggedStart(*[Write(item) for item in known], lag_ratio=0.20),
            LaggedStart(*[Create(socket) for socket in empty_sockets], lag_ratio=0.20),
            FadeIn(unknown),
            Indicate(empty_sockets, color=BOUNDARY),
            settle=0.76,
        )

        # b14: the complete payment chain is the transferable practical test.
        final_terms = VGroup(
            self.label("QUALITY", 15, EVIDENCE, "BOLD"),
            self.label("AUTHORITY", 15, AUTHORITY, "BOLD"),
            self.label("VERIFY", 15, ACCENT, "BOLD"),
            self.label("FALLBACK", 15, COPPER, "BOLD"),
            self.label("REPAIR", 15, RESIDUAL, "BOLD"),
        ).arrange(RIGHT, buff=0.74).shift(UP * 0.62)
        final_arrows = VGroup(*[
            Arrow(final_terms[i].get_right(), final_terms[i + 1].get_left(), color=BOUNDARY, buff=0.14, stroke_width=2.5)
            for i in range(len(final_terms) - 1)
        ])
        paid = self.label("ALL PAID", 20, INK, "BOLD").shift(DOWN * 0.62)
        saving = self.label("THEN THE SAVING IS REAL", 29, EVIDENCE, "BOLD").shift(DOWN * 1.60)
        self.beat(
            14,
            FadeOut(VGroup(boundary_box, boundary_label, divider, known, empty_sockets, unknown)),
            LaggedStart(*[FadeIn(term, shift=UP * 0.12) for term in final_terms], lag_ratio=0.12),
            LaggedStart(*[GrowArrow(arrow) for arrow in final_arrows], lag_ratio=0.12),
            Write(paid),
            TransformFromCopy(VGroup(final_terms, final_arrows), saving),
            Circumscribe(saving, color=EVIDENCE),
            settle=0.64,
        )
