"""Generation-2 visual abstract for “The Efficient ASI Hypothesis.”

One invoice ticket moves through a governed route exchange. Visible prices,
verification, hidden costs, fallback, reuse, expiry, and evidence boundaries
remain causally connected instead of becoming paragraph cards.
"""

from __future__ import annotations

from manim import (
    AnimationGroup,
    ArcBetweenPoints,
    Arrow,
    Axes,
    Circle,
    Create,
    DashedLine,
    Dot,
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
    Rotate,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    TransformFromCopy,
    UP,
    VGroup,
    Write,
)

from visual_edition.lib.asi_visuals import (
    ACCENT,
    AUTHORITY,
    BOUNDARY,
    COPPER,
    EVIDENCE,
    INK,
    MUTED,
    RESIDUAL,
    ROLLBACK,
    SURFACE,
    AsiScene,
    proof_boundary,
    residual_marker,
    text,
)


class EfficientAsiHypothesisGeneration2(AsiScene):
    TARGET_DURATION = 244.480
    ENDS = [
        9.905, 19.210, 29.315, 39.495, 50.525, 61.755, 72.210,
        82.615, 91.745, 101.300, 112.880, 122.235, 132.665,
        143.820, 155.275, 168.155, 180.635, 194.690, 206.170,
        218.225, 230.605, 244.480,
    ]

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.35) -> None:
        self.next_section(f"b{index:02d}")
        end = self.ENDS[index - 1]
        remaining = max(0.05, end - self.renderer.time)
        fade_prefix = []
        for animation in animations:
            if isinstance(animation, FadeOut):
                fade_prefix.append(animation)
            else:
                break
        content = animations[len(fade_prefix):]
        active_animation = None
        if fade_prefix and content:
            anchor_count = min(2, len(content))
            crossfade = AnimationGroup(
                AnimationGroup(*fade_prefix, lag_ratio=0),
                AnimationGroup(*content[:anchor_count], lag_ratio=0),
                lag_ratio=0,
                run_time=min(0.8, remaining * 0.12),
            )
            content = content[anchor_count:]
            if content:
                content_group = LaggedStart(
                    *content,
                    lag_ratio=0.22,
                    run_time=max(0.05, remaining - 1.15),
                )
                active_animation = Succession(crossfade, content_group)
            else:
                active_animation = crossfade
        elif animations:
            active_animation = LaggedStart(*animations, lag_ratio=0.22)
        run_time = max(0.05, remaining - min(settle, remaining * 0.25))
        if active_animation is not None:
            self.play(active_animation, run_time=run_time)
        self.wait_until(end)

    @staticmethod
    def label(value: str, size: int = 20, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def card(self, heading: str, detail: str, color: str, width: float = 2.1) -> VGroup:
        shell = RoundedRectangle(
            width=width,
            height=0.82,
            corner_radius=0.1,
            stroke_color=color,
            stroke_width=2.5,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        labels = VGroup(
            self.label(heading, 17, color, "BOLD"),
            self.label(detail, 12, MUTED),
        ).arrange(UP * -1, buff=0.05).move_to(shell)
        return VGroup(shell, labels)

    def invoice(self, *, damaged: bool = False) -> VGroup:
        page = RoundedRectangle(
            width=2.25,
            height=2.85,
            corner_radius=0.12,
            stroke_color=BOUNDARY,
            stroke_width=3,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        title = self.label("INVOICE", 20, INK, "BOLD").shift(UP * 0.95)
        fields = VGroup(
            self.label("VENDOR  AURORA", 13, MUTED),
            self.label("DATE  08·01", 13, MUTED),
            self.label("SUBTOTAL  84", 13, MUTED),
            self.label("TAX  7" if not damaged else "TAX  ?", 15, ROLLBACK if damaged else MUTED, "BOLD"),
            self.label("TOTAL  91", 16, ACCENT, "BOLD"),
        ).arrange(UP * -1, buff=0.16).shift(UP * -0.15)
        tear = VGroup()
        if damaged:
            tear = VGroup(
                Line(LEFT * 0.15, RIGHT * 0.05 + UP * 0.18, color=ROLLBACK, stroke_width=3),
                Line(RIGHT * 0.05 + UP * 0.18, RIGHT * 0.24 + UP * -0.08, color=ROLLBACK, stroke_width=3),
            ).shift(UP * -0.45 + RIGHT * 0.35)
        return VGroup(page, title, fields, tear)

    def ticket(self) -> VGroup:
        shell = RoundedRectangle(
            width=2.0,
            height=0.78,
            corner_radius=0.38,
            stroke_color=ACCENT,
            stroke_width=3,
            fill_color="#163341",
            fill_opacity=1,
        )
        dot = Circle(radius=0.14, color=ACCENT, fill_color=ACCENT, fill_opacity=1).shift(LEFT * 0.68)
        label = self.label("INVOICE 47", 17, INK, "BOLD").shift(RIGHT * 0.2)
        return VGroup(shell, dot, label)

    def weight(self, value: str, detail: str, color: str = COPPER, width: float = 1.3) -> VGroup:
        shell = RoundedRectangle(
            width=width,
            height=0.72,
            corner_radius=0.09,
            stroke_color=color,
            stroke_width=2.5,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        labels = VGroup(
            self.label(value, 20, color, "BOLD"),
            self.label(detail, 11, MUTED),
        ).arrange(UP * -1, buff=0.03).move_to(shell)
        return VGroup(shell, labels)

    def check(self, label: str, color: str = EVIDENCE) -> VGroup:
        ring = Circle(radius=0.33, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        mark = VGroup(
            Line(LEFT * 0.13, ORIGIN + UP * -0.11, color=color, stroke_width=4),
            Line(ORIGIN + UP * -0.11, RIGHT * 0.19 + UP * 0.14, color=color, stroke_width=4),
        ).move_to(ring)
        tag = self.label(label, 12, color, "BOLD").next_to(ring, UP * -1, buff=0.08)
        return VGroup(ring, mark, tag)

    def route_gate(self, label: str, color: str) -> VGroup:
        posts = VGroup(
            Line(UP * 0.38, UP * -0.38, color=color, stroke_width=5),
            Line(UP * 0.38, UP * -0.38, color=color, stroke_width=5).shift(RIGHT * 0.28),
        )
        tag = self.label(label, 11, color, "BOLD").next_to(posts, UP, buff=0.05)
        return VGroup(posts, tag)

    def construct(self) -> None:
        # 1 — four visible prices create the opening puzzle.
        invoice = self.invoice().scale(0.72).shift(LEFT * 4.7)
        ticket = self.ticket().shift(LEFT * 2.65)
        route_ys = [1.8, 0.6, -0.6, -1.8]
        routes = VGroup(*[
            Line(LEFT * 1.55 + UP * y, RIGHT * 4.75 + UP * y, color=BOUNDARY, stroke_width=3)
            for y in route_ys
        ])
        prices = VGroup(
            self.weight("1", "unit", ACCENT),
            self.weight("4", "units", COPPER),
            self.weight("9", "units", AUTHORITY),
            self.weight("H", "human", EVIDENCE),
        )
        for price, y in zip(prices, route_ys):
            price.scale(0.78).move_to(RIGHT * 5.5 + UP * y)
        question = self.label("WHICH ROUTE IS EFFICIENT?", 27, INK, "BOLD").shift(UP * 3.3)
        self.add(invoice, ticket)
        self.play_beat(
            1,
            LaggedStart(*[Create(route) for route in routes], lag_ratio=0.1),
            LaggedStart(*[GrowFromCenter(price) for price in prices], lag_ratio=0.12),
            Write(question),
        )

        # 2 — the same prospective quality test constrains every lane.
        field_seals = VGroup(
            self.card("TOTAL", "preserved", ACCENT, 1.65),
            self.card("VENDOR", "preserved", BOUNDARY, 1.65),
            self.card("DATE", "preserved", BOUNDARY, 1.65),
            self.card("PRIVACY", "obeyed", AUTHORITY, 1.65),
        ).arrange(RIGHT, buff=0.18).scale(0.73).shift(UP * -3.15 + RIGHT * 0.9)
        test_aperture = RoundedRectangle(width=1.0, height=5.2, corner_radius=0.15, color=EVIDENCE, stroke_width=4).shift(RIGHT * 4.45)
        test_label = self.label("FIXED\nTEST", 17, EVIDENCE, "BOLD").move_to(test_aperture)
        test_probes = VGroup(*[Dot(LEFT * 1.25 + UP * y, radius=0.12, color=EVIDENCE) for y in route_ys])
        test_paths = VGroup(*[
            Line(probe.get_center(), RIGHT * 4.95 + UP * y, color=EVIDENCE)
            for probe, y in zip(test_probes, route_ys)
        ])
        self.play_beat(
            2,
            FadeOut(question),
            LaggedStart(*[TransformFromCopy(invoice, seal) for seal in field_seals], lag_ratio=0.12),
            Create(test_aperture),
            Write(test_label),
            LaggedStart(*[MoveAlongPath(probe, path) for probe, path in zip(test_probes, test_paths)], lag_ratio=0.12),
            Indicate(test_aperture, color=EVIDENCE),
        )

        # 3 — a typed ticket precedes route choice.
        contract_ticket = RoundedRectangle(width=7.4, height=1.15, corner_radius=0.18, color=ACCENT, stroke_width=3, fill_color=SURFACE, fill_opacity=1).shift(UP * 3.05)
        contract_fields = VGroup(*[
            self.label(value, 15, color, "BOLD")
            for value, color in [
                ("QUALITY", EVIDENCE), ("AUTHORITY", AUTHORITY), ("RISK", ROLLBACK),
                ("DEADLINE", BOUNDARY), ("COST CLASSES", COPPER),
            ]
        ]).arrange(RIGHT, buff=0.48).move_to(contract_ticket)
        exchange_shell = RoundedRectangle(width=13.0, height=6.8, corner_radius=0.22, color=ACCENT, stroke_width=2.5, fill_opacity=0)
        exchange_label = self.label("GOVERNED ROUTE EXCHANGE", 17, ACCENT, "BOLD").next_to(exchange_shell, UP, buff=0.06)
        contract_cursor = Line(UP * 0.42, UP * -0.42, color=ACCENT, stroke_width=6).move_to(contract_ticket.get_left() + RIGHT * 0.2)
        contract_scan = Line(contract_cursor.get_center(), contract_ticket.get_right() + LEFT * 0.2, color=ACCENT)
        self.play_beat(
            3,
            FadeOut(field_seals),
            FadeOut(prices),
            FadeOut(test_probes),
            TransformFromCopy(ticket, contract_ticket),
            LaggedStart(*[FadeIn(field, shift=UP * 0.1) for field in contract_fields], lag_ratio=0.1),
            Create(exchange_shell),
            FadeIn(exchange_label),
            MoveAlongPath(contract_cursor, contract_scan),
        )

        # 4 — route identities and fallback switches.
        route_names = VGroup(*[
            self.card(name, detail, color, 2.15).scale(0.72).move_to(LEFT * 0.25 + UP * y)
            for (name, detail, color), y in zip(
                [
                    ("PARSER", "versioned", ACCENT),
                    ("SPECIALIST", "small model", COPPER),
                    ("FRONTIER", "broad model", AUTHORITY),
                    ("HUMAN", "review", EVIDENCE),
                ],
                route_ys,
            )
        ])
        fallback_arcs = VGroup(*[
            ArcBetweenPoints(RIGHT * 3.7 + UP * route_ys[i], RIGHT * 3.7 + UP * route_ys[i + 1], angle=-1.1, color=RESIDUAL, stroke_width=2.5)
            for i in range(3)
        ])
        fallback_tags = VGroup(*[
            self.label("fallback", 11, RESIDUAL, "BOLD").next_to(arc, LEFT, buff=0.05)
            for arc in fallback_arcs
        ])
        route_selector = Circle(radius=0.22, color=RESIDUAL, fill_color=RESIDUAL, fill_opacity=0.8).move_to(LEFT * 1.25 + UP * route_ys[0])
        route_selector_path = Line(route_selector.get_center(), LEFT * 1.25 + UP * route_ys[-1], color=RESIDUAL)
        self.play_beat(
            4,
            LaggedStart(*[FadeIn(name, shift=RIGHT * 0.15) for name in route_names], lag_ratio=0.1),
            LaggedStart(*[Create(arc) for arc in fallback_arcs], lag_ratio=0.12),
            LaggedStart(*[FadeIn(tag) for tag in fallback_tags], lag_ratio=0.1),
            MoveAlongPath(route_selector, route_selector_path),
        )

        # 5 — always-maximal accepts work but fails to compound reuse.
        frontier_tickets = VGroup(*[self.ticket().scale(0.55).move_to(LEFT * 3.2 + UP * (-0.7 + i * 0.02)) for i in range(3)])
        frontier_paths = VGroup(*[
            Line(ticket.get_center(), RIGHT * 4.35 + UP * route_ys[2], color=AUTHORITY)
            for ticket in frontier_tickets
        ])
        frontier_costs = VGroup(*[self.weight("9", "frontier", AUTHORITY, 1.15).scale(0.65) for _ in range(3)]).arrange(RIGHT, buff=0.14).shift(RIGHT * 2.2 + UP * -2.9)
        empty_depot = RoundedRectangle(width=2.3, height=1.25, corner_radius=0.12, color=BOUNDARY, fill_color=SURFACE, fill_opacity=0.7).shift(RIGHT * 5.15 + UP * 2.85)
        empty_label = VGroup(self.label("REUSE DEPOT", 15, MUTED, "BOLD"), self.label("empty", 13, ROLLBACK)).arrange(UP * -1, buff=0.05).move_to(empty_depot)
        maximal = self.label("ALWAYS MAXIMAL", 18, AUTHORITY, "BOLD").shift(LEFT * 5.05 + UP * 2.65)
        self.play_beat(
            5,
            FadeIn(maximal),
            LaggedStart(*[MoveAlongPath(t, path) for t, path in zip(frontier_tickets, frontier_paths)], lag_ratio=0.12),
            LaggedStart(*[GrowFromCenter(cost) for cost in frontier_costs], lag_ratio=0.14),
            FadeIn(empty_depot),
            FadeIn(empty_label),
        )

        # 6 — always-cheapest drops a digit and grows a hidden bill.
        damaged = self.invoice(damaged=True).scale(0.72).move_to(invoice)
        cheap_ticket = self.ticket().scale(0.7).shift(LEFT * 3.2 + UP * 2.1)
        cheap_path = Line(cheap_ticket.get_center(), RIGHT * 4.35 + UP * route_ys[0], color=ACCENT)
        cheap_scanner = Line(UP * 0.52, UP * -0.52, color=ACCENT, stroke_width=6).move_to(cheap_ticket)
        hidden_costs = VGroup(
            self.weight("8", "repair", ROLLBACK),
            self.weight("3", "review", RESIDUAL),
            self.weight("?", "correction", ROLLBACK),
        ).arrange(RIGHT, buff=0.22).scale(0.72).shift(RIGHT * 2.0 + UP * 2.85)
        cheap = self.label("ALWAYS CHEAPEST", 18, ACCENT, "BOLD").shift(LEFT * 5.05 + UP * 2.65)
        tax_alert = self.label("TAX DIGIT MISSING", 19, ROLLBACK, "BOLD").shift(RIGHT * 2.2 + UP * 1.65)
        hidden_bill_link = Arrow(damaged.get_right(), hidden_costs.get_left(), color=ROLLBACK, stroke_width=4, buff=0.15)
        self.play_beat(
            6,
            FadeOut(frontier_tickets), FadeOut(frontier_costs), FadeOut(maximal),
            FadeIn(cheap), ReplacementTransform(invoice, damaged),
            AnimationGroup(MoveAlongPath(cheap_ticket, cheap_path), MoveAlongPath(cheap_scanner, cheap_path.copy()), lag_ratio=0),
            Indicate(damaged[2][3], color=ROLLBACK),
            FadeIn(tax_alert),
            LaggedStart(*[GrowFromCenter(cost) for cost in hidden_costs], lag_ratio=0.15),
            GrowArrow(hidden_bill_link),
        )

        # 7 — authority and quality precede cost.
        authority_gates = VGroup(*[self.route_gate("AUTH", AUTHORITY).scale(0.75).move_to(RIGHT * 1.65 + UP * y) for y in route_ys])
        quality_gates = VGroup(*[self.route_gate("QUALITY", EVIDENCE).scale(0.75).move_to(RIGHT * 2.7 + UP * y) for y in route_ys])
        gate_probe = self.ticket().scale(0.5).move_to(LEFT * 1.3 + UP * route_ys[1])
        gate_probe_path = Line(gate_probe.get_center(), RIGHT * 4.05 + UP * route_ys[1], color=EVIDENCE)
        then_cost = self.label("THEN COMPARE COST", 18, COPPER, "BOLD").shift(RIGHT * 4.9 + UP * 3.05)
        self.play_beat(
            7,
            FadeOut(cheap), FadeOut(damaged), FadeOut(cheap_ticket), FadeOut(cheap_scanner), FadeOut(tax_alert), FadeOut(hidden_costs), FadeOut(hidden_bill_link), FadeOut(empty_depot), FadeOut(empty_label),
            LaggedStart(*[FadeIn(gate) for gate in authority_gates], lag_ratio=0.08),
            LaggedStart(*[FadeIn(gate) for gate in quality_gates], lag_ratio=0.08),
            Write(then_cost),
            Indicate(authority_gates[0], color=AUTHORITY),
            Indicate(quality_gates[0], color=EVIDENCE),
            MoveAlongPath(gate_probe, gate_probe_path),
        )

        # 8 — a familiar template earns parser acceptance after checks.
        parser_invoice = self.invoice().scale(0.5).shift(LEFT * 4.75 + UP * 1.35)
        parser_ticket = self.ticket().scale(0.62).move_to(LEFT * 3.65 + UP * 2.1)
        parser_path = Line(parser_ticket.get_center(), RIGHT * 4.2 + UP * route_ys[0], color=ACCENT)
        parser_scanner = Line(UP * 0.48, UP * -0.48, color=ACCENT, stroke_width=6).move_to(parser_ticket)
        version = self.card("TEMPLATE v3", "current", ACCENT, 2.1).scale(0.7).move_to(LEFT * 1.7 + UP * 1.48)
        checks = VGroup(*[self.check(name) for name in ["TOTAL", "VENDOR", "DATE", "PRIVACY"]]).arrange(RIGHT, buff=0.22).scale(0.7).shift(RIGHT * 1.75 + UP * 2.1)
        accepted = self.card("ACCEPTED", "4 / 4", EVIDENCE, 1.9).scale(0.78).move_to(RIGHT * 4.65 + UP * 2.1)
        self.play_beat(
            8,
            FadeOut(then_cost),
            FadeOut(ticket),
            FadeIn(parser_invoice), FadeIn(version),
            AnimationGroup(MoveAlongPath(parser_ticket, parser_path), MoveAlongPath(parser_scanner, parser_path.copy()), lag_ratio=0),
            LaggedStart(*[FadeIn(check, scale=0.8) for check in checks], lag_ratio=0.12),
            FadeIn(accepted, scale=0.85),
        )

        # 9 — the damaged scan remains an owned residual.
        failed_invoice = self.invoice(damaged=True).scale(0.5).move_to(parser_invoice)
        residual = residual_marker("OWNED RESIDUAL").scale(0.9).shift(RIGHT * 4.65 + UP * -2.95)
        fail_tag = self.card("TAX FIELD", "FAIL", ROLLBACK, 1.9).scale(0.8).move_to(checks[0].get_center())
        residual_link = DashedLine(fail_tag.get_bottom(), residual.get_left(), color=RESIDUAL, dash_length=0.12, stroke_width=2)
        self.play_beat(
            9,
            ReplacementTransform(parser_invoice, failed_invoice),
            FadeOut(accepted),
            Succession(FadeOut(checks[0]), FadeIn(fail_tag)),
            Indicate(fail_tag, color=ROLLBACK),
            Create(residual_link),
            FadeIn(residual),
        )

        # 10 — fallback preserves ticket identity and failed cost.
        fallback_path = ArcBetweenPoints(parser_ticket.get_center(), LEFT * 2.2 + UP * 0.7, angle=-0.9, color=RESIDUAL)
        attempt_cost = self.weight("+1", "parser attempt", RESIDUAL, 1.7).scale(0.78).shift(LEFT * 4.6 + UP * -2.95)
        learning = self.card("LEARNING", "tax-field miss", RESIDUAL, 2.2).scale(0.74).shift(RIGHT * 2.55 + UP * -2.95)
        learning_link = DashedLine(residual.get_left(), learning.get_right(), color=RESIDUAL, dash_length=0.12, stroke_width=2)
        self.play_beat(
            10,
            Create(fallback_path),
            MoveAlongPath(parser_ticket, fallback_path),
            TransformFromCopy(fail_tag, attempt_cost),
            Create(learning_link), FadeIn(learning),
            Indicate(route_names[1], color=COPPER),
        )

        # 11 — the complete denominator expands below the causal trace.
        cost_names = [
            ("GEN", COPPER), ("CTX", BOUNDARY), ("ROUTE", ACCENT), ("VERIFY", EVIDENCE), ("REPAIR", ROLLBACK),
            ("REVIEW", RESIDUAL), ("ROLLBACK", ROLLBACK), ("MAINTAIN", AUTHORITY), ("DELAY", BOUNDARY), ("DISPLACE", MUTED),
        ]
        cost_panel = RoundedRectangle(width=6.4, height=2.5, corner_radius=0.16, stroke_color=COPPER, stroke_width=2, fill_color=SURFACE, fill_opacity=0.96).shift(UP * -1.55 + RIGHT * 0.15)
        complete_costs = VGroup(*[self.weight("•", name, color, 1.05).scale(0.72) for name, color in cost_names]).arrange_in_grid(rows=2, cols=5, buff=(0.18, 0.2)).shift(UP * -1.75 + RIGHT * 0.15)
        total_rule = Line(LEFT * 3.05, RIGHT * 3.35, color=COPPER, stroke_width=4).shift(UP * -0.78 + RIGHT * 0.15)
        total_label = self.label("TOTAL CONTRACT COST", 18, COPPER, "BOLD").next_to(total_rule, UP, buff=0.08)
        cost_cursor = Dot(total_rule.get_left(), radius=0.13, color=COPPER)
        cost_sweep = Line(UP * 0.75, UP * -0.75, color=COPPER, stroke_width=5).move_to(complete_costs.get_left() + RIGHT * 0.1)
        cost_sweep_path = Line(cost_sweep.get_center(), complete_costs.get_right() + LEFT * 0.1, color=COPPER)
        self.play_beat(
            11,
            FadeOut(attempt_cost), FadeOut(learning),
            FadeOut(learning_link),
            FadeIn(cost_panel),
            LaggedStart(*[GrowFromCenter(cost) for cost in complete_costs], lag_ratio=0.08),
            Create(total_rule),
            FadeIn(total_label),
            AnimationGroup(MoveAlongPath(cost_cursor, total_rule.copy()), MoveAlongPath(cost_sweep, cost_sweep_path), lag_ratio=0),
        )

        # 12 — prediction: 1 + 8 + 3 versus 9.
        balance_stem = Line(UP * 1.0, UP * -1.25, color=BOUNDARY, stroke_width=4)
        balance_beam = Line(LEFT * 3.4, RIGHT * 3.4, color=ACCENT, stroke_width=5).shift(UP * 0.8)
        pivot = Dot(UP * 0.8, radius=0.13, color=ACCENT)
        left_bill = VGroup(self.weight("1", "route", ACCENT), self.weight("8", "repair", ROLLBACK), self.weight("3", "review", RESIDUAL)).arrange(RIGHT, buff=0.16).scale(0.75).shift(LEFT * 2.15 + UP * -0.15)
        right_bill = self.weight("9", "verified", EVIDENCE, 1.7).shift(RIGHT * 2.2 + UP * -0.15)
        predict = self.label("WHICH COMPLETE BILL IS LOWER?", 23, INK, "BOLD").shift(UP * -1.55)
        balance_panel = RoundedRectangle(width=11.2, height=5.5, corner_radius=0.22, stroke_color=BOUNDARY, stroke_width=2, fill_color=SURFACE, fill_opacity=1)
        old_exchange = VGroup(
            routes, route_names, fallback_arcs, fallback_tags, route_selector, authority_gates, quality_gates, gate_probe,
            contract_ticket, contract_fields, exchange_shell, exchange_label, invoice, ticket,
            test_aperture, test_label, contract_cursor, failed_invoice, parser_ticket, parser_scanner, version, checks,
            fail_tag, residual, residual_link, fallback_path, parser_path, cost_panel, complete_costs, total_rule, total_label, cost_cursor, cost_sweep,
        )
        self.play_beat(
            12,
            FadeOut(old_exchange),
            FadeIn(balance_panel), Create(balance_stem), Create(balance_beam), FadeIn(pivot),
            LaggedStart(*[GrowFromCenter(item) for item in left_bill], lag_ratio=0.15),
            GrowFromCenter(right_bill),
            Write(predict),
        )

        # 13 — complete arithmetic defeats the hidden-cost win.
        twelve = self.weight("12", "complete", ROLLBACK, 2.0).move_to(left_bill)
        nine = self.weight("9", "complete", EVIDENCE, 2.0).move_to(right_bill)
        inequality = self.label("12  >  9", 42, INK, "BOLD").shift(UP * -1.25)
        principle = self.label("VISIBLE COST  ≠  TOTAL COST", 20, COPPER, "BOLD").shift(UP * -2.0)
        self.play_beat(
            13,
            FadeOut(predict),
            ReplacementTransform(left_bill, twelve),
            ReplacementTransform(right_bill, nine),
            Rotate(balance_beam, angle=-0.08, about_point=pivot.get_center()),
            Write(inequality),
            FadeIn(principle),
            Indicate(nine, color=EVIDENCE),
        )

        # 14 — verified repetition becomes a governed artifact.
        depot = RoundedRectangle(width=6.2, height=3.4, corner_radius=0.18, color=ACCENT, stroke_width=3, fill_color=SURFACE, fill_opacity=0.85)
        depot_title = self.label("VERSIONED ARTIFACT DEPOT", 20, ACCENT, "BOLD").next_to(depot, UP, buff=0.12)
        artifact = self.card("PARSER v3", "invoice template", ACCENT, 2.5).scale(1.05).shift(UP * 0.45)
        obligation_tags = VGroup(
            self.card("ASSUMPTIONS", "format v3", BOUNDARY, 2.0),
            self.card("TESTS", "4 fields", EVIDENCE, 2.0),
            self.card("RENEWAL", "dated", AUTHORITY, 2.0),
        ).arrange(RIGHT, buff=0.25).scale(0.72).shift(UP * -1.05)
        accepted_traces = VGroup(*[self.check(f"RUN {i + 1}").scale(0.62) for i in range(4)]).arrange(RIGHT, buff=0.62).shift(UP * 2.95)
        trace_arrows = VGroup(*[
            Arrow(trace.get_bottom(), artifact.get_top(), color=EVIDENCE, stroke_width=2.5, buff=0.12, max_tip_length_to_length_ratio=0.12)
            for trace in accepted_traces
        ])
        artifact_token = self.ticket().scale(0.38).move_to(accepted_traces.get_center())
        artifact_path = Line(artifact_token.get_center(), artifact.get_center(), color=ACCENT)
        self.play_beat(
            14,
            FadeOut(VGroup(balance_panel, balance_stem, balance_beam, pivot, twelve, nine, inequality, principle)),
            Create(depot), FadeIn(depot_title),
            LaggedStart(*[FadeIn(trace) for trace in accepted_traces], lag_ratio=0.1),
            LaggedStart(*[GrowArrow(arrow) for arrow in trace_arrows], lag_ratio=0.12),
            FadeIn(artifact, scale=0.82),
            LaggedStart(*[FadeIn(tag, shift=UP * 0.12) for tag in obligation_tags], lag_ratio=0.12),
            MoveAlongPath(artifact_token, artifact_path),
        )

        # 15 — a version change expires the cache and creates revalidation work.
        new_invoice = self.invoice().scale(0.55).shift(LEFT * 4.7 + UP * 1.75)
        v4 = self.card("TEMPLATE v4", "changed", ROLLBACK, 2.2).scale(0.78).shift(LEFT * 3.1 + UP * 1.75)
        expired = self.label("EXPIRED", 35, ROLLBACK, "BOLD").rotate(-0.18).move_to(artifact)
        cross1 = Line(artifact.get_corner(UP + LEFT), artifact.get_corner(UP * -1 + RIGHT), color=ROLLBACK, stroke_width=6)
        revalidate_path = Arrow(artifact.get_bottom(), RIGHT * 3.6 + UP * -1.15, color=AUTHORITY, stroke_width=4, buff=0.15)
        revalidate = self.card("REVALIDATE", "before reuse", AUTHORITY, 2.5).shift(RIGHT * 4.3 + UP * -1.2)
        self.play_beat(
            15,
            FadeIn(new_invoice), FadeIn(v4),
            Indicate(v4, color=ROLLBACK),
            Create(cross1), FadeIn(expired),
            GrowArrow(revalidate_path), FadeIn(revalidate),
            obligation_tags[2].animate.set_color(ROLLBACK),
        )

        # 16 — generalize routing to six substitutable resources.
        dial_specs = [
            ("MODEL", COPPER), ("CONTEXT", BOUNDARY), ("SEARCH", ACCENT),
            ("PRECISION", AUTHORITY), ("TOOLS", EVIDENCE), ("VERIFY", RESIDUAL),
        ]
        dials = VGroup()
        for name, color in dial_specs:
            ring = Circle(radius=0.68, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
            needle = Line(ring.get_center(), ring.get_center() + RIGHT * 0.4 + UP * 0.22, color=color, stroke_width=4)
            tag = self.label(name, 15, color, "BOLD").next_to(ring, UP * -1, buff=0.08)
            dials.add(VGroup(ring, needle, tag))
        dials.arrange_in_grid(rows=2, cols=3, buff=(1.0, 0.7)).scale(0.82).shift(UP * 0.45)
        fixed_contract = self.card("FIXED CONTRACT", "quality + authority + total cost", INK, 4.2).shift(UP * 3.0)
        no_axiom = self.label("MINIMUM VIABLE ≠ ALWAYS SMALL", 22, ROLLBACK, "BOLD").shift(UP * -1.5)
        dial_selector = Circle(radius=0.68, color=ACCENT, stroke_width=4).move_to(dials[0])
        dial_tour = Succession(*[dial_selector.animate.move_to(dial) for dial in dials[1:]])
        self.play_beat(
            16,
            FadeOut(VGroup(depot, depot_title, artifact, obligation_tags, accepted_traces, trace_arrows, artifact_token, new_invoice, v4, expired, cross1, revalidate_path, revalidate)),
            LaggedStart(*[
                Succession(FadeIn(dial, scale=0.82), Rotate(dial[1], angle=0.75))
                for dial in dials
            ], lag_ratio=0.1),
            FadeIn(fixed_contract),
            Write(no_axiom),
            Succession(FadeIn(dial_selector), dial_tour),
        )

        # 17 — selectivity is allowed to lose in a high-risk regime.
        gauge_names = ["NOVELTY", "UNCERTAINTY", "CONSEQUENCE"]
        gauges = VGroup()
        for i, name in enumerate(gauge_names):
            frame = RoundedRectangle(width=1.15, height=3.4, corner_radius=0.12, color=BOUNDARY, fill_color=SURFACE, fill_opacity=1)
            fill = Rectangle(width=0.8, height=0.45 + i * 0.35, stroke_opacity=0, fill_color=ROLLBACK, fill_opacity=0.85).align_to(frame, UP * -1).shift(UP * 0.18)
            tag = self.label(name, 13, ROLLBACK, "BOLD").next_to(frame, UP * -1, buff=0.1)
            gauges.add(VGroup(frame, fill, tag))
        gauges.arrange(RIGHT, buff=0.5).shift(LEFT * 3.9)
        maximal_verified = VGroup(
            self.card("STRONGEST ROUTE", "broad capability", AUTHORITY, 3.2),
            self.card("BROAD VERIFY", "risk-weighted", EVIDENCE, 3.2),
        ).arrange(UP * -1, buff=0.45).shift(RIGHT * 2.6)
        valid_choice = self.label("VALID CHOICE", 20, EVIDENCE, "BOLD").next_to(maximal_verified, UP * -1, buff=0.4)
        decision_arrow = Arrow(gauges.get_right(), maximal_verified.get_left(), color=EVIDENCE, stroke_width=4, buff=0.2)
        risk_token = Dot(decision_arrow.get_start(), radius=0.17, color=EVIDENCE)
        self.play_beat(
            17,
            FadeOut(dials), FadeOut(no_axiom), FadeOut(dial_selector),
            LaggedStart(*[
                Succession(FadeIn(VGroup(gauge[0], gauge[2]), shift=UP * 0.15), GrowFromCenter(gauge[1]))
                for gauge in gauges
            ], lag_ratio=0.12),
            Succession(FadeIn(maximal_verified), Indicate(maximal_verified, color=EVIDENCE)),
            GrowArrow(decision_arrow), MoveAlongPath(risk_token, decision_arrow.copy()),
            FadeIn(valid_choice),
        )

        # 18 — scaling fit, operational threshold, and forecast residual coexist.
        analysis_panel = RoundedRectangle(width=12.4, height=6.0, corner_radius=0.22, stroke_color=BOUNDARY, stroke_width=2, fill_color=SURFACE, fill_opacity=1)
        axes_left = Axes(x_range=[0, 5, 1], y_range=[0, 4, 1], x_length=4.5, y_length=3.2, tips=False, axis_config={"color": BOUNDARY, "stroke_width": 2}).shift(LEFT * 3.5)
        smooth = axes_left.plot(lambda x: 3.5 - 2.8 / (x + 1), x_range=[0, 5], color=ACCENT, stroke_width=4)
        loss_label = self.label("SMOOTH LOSS FIT", 16, ACCENT, "BOLD").next_to(axes_left, UP, buff=0.1)
        axes_right = Axes(x_range=[0, 5, 1], y_range=[0, 4, 1], x_length=4.5, y_length=3.2, tips=False, axis_config={"color": BOUNDARY, "stroke_width": 2}).shift(RIGHT * 3.2)
        steps = VGroup(
            Line(axes_right.c2p(0, 0.7), axes_right.c2p(2.2, 0.7), color=AUTHORITY, stroke_width=4),
            Line(axes_right.c2p(2.2, 0.7), axes_right.c2p(2.2, 2.8), color=AUTHORITY, stroke_width=4),
            Line(axes_right.c2p(2.2, 2.8), axes_right.c2p(5, 2.8), color=AUTHORITY, stroke_width=4),
        )
        threshold = DashedLine(axes_right.c2p(0, 2.0), axes_right.c2p(5, 2.0), color=ROLLBACK, dash_length=0.14)
        score_label = self.label("OPERATIONAL SCORE", 16, AUTHORITY, "BOLD").next_to(axes_right, UP, buff=0.1)
        residual_dots = VGroup(*[Dot(axes_left.c2p(x, y), radius=0.08, color=RESIDUAL) for x, y in [(1.1, 1.9), (2.4, 2.4), (3.7, 3.0), (4.5, 3.25)]])
        forecast_cursor = Dot(axes_left.c2p(0, 0.7), radius=0.13, color=ACCENT)
        forecast_scan = Line(UP * 1.85, UP * -1.85, color=ACCENT, stroke_width=4).move_to(axes_left.get_left() + RIGHT * 0.1)
        forecast_scan_path = Line(forecast_scan.get_center(), axes_right.get_right() + LEFT * 0.1, color=ACCENT)
        residual_tag = self.label("FORECAST RESIDUALS STAY", 18, RESIDUAL, "BOLD").shift(UP * -2.05)
        self.play_beat(
            18,
            FadeOut(gauges), FadeOut(maximal_verified), FadeOut(valid_choice), FadeOut(fixed_contract), FadeOut(decision_arrow), FadeOut(risk_token),
            FadeIn(analysis_panel), Create(axes_left), Create(axes_right),
            Create(smooth), LaggedStart(*[Create(step) for step in steps], lag_ratio=0.2),
            Create(threshold), FadeIn(loss_label), FadeIn(score_label),
            LaggedStart(*[FadeIn(dot, scale=0.5) for dot in residual_dots], lag_ratio=0.15),
            MoveAlongPath(forecast_cursor, smooth.copy()),
            MoveAlongPath(forecast_scan, forecast_scan_path),
            Write(residual_tag),
        )

        # 19 — four policies enter one matched comparison.
        policy_specs = [
            ("ALWAYS CHEAPEST", ACCENT), ("ALWAYS MAXIMAL", AUTHORITY),
            ("ADAPTIVE", EVIDENCE), ("MONOLITH + TOOLS", BOUNDARY),
        ]
        policy_lanes = VGroup()
        for i, (name, color) in enumerate(policy_specs):
            lane = Line(LEFT * 3.8, RIGHT * 4.1, color=BOUNDARY, stroke_width=3).shift(UP * (1.8 - i * 1.15))
            vehicle = self.card(name, "no winner", color, 2.6).scale(0.72).move_to(LEFT * 3.9 + UP * (1.8 - i * 1.15))
            policy_lanes.add(VGroup(lane, vehicle))
        matched = self.label("SAME TASKS · ACCESS · TOOLS · TUNING · OBSERVATION", 17, INK, "BOLD").shift(UP * 3.25)
        self.play_beat(
            19,
            FadeOut(VGroup(analysis_panel, axes_left, axes_right, smooth, steps, threshold, loss_label, score_label, residual_dots, forecast_cursor, forecast_scan, residual_tag)),
            FadeIn(matched),
            LaggedStart(*[Create(lane[0]) for lane in policy_lanes], lag_ratio=0.1),
            LaggedStart(*[
                Succession(FadeIn(lane[1], shift=RIGHT * 0.15), lane[1].animate.shift(RIGHT * 5.2))
                for lane in policy_lanes
            ], lag_ratio=0.1),
        )

        # 20 — a joint frontier, not a single cheap score.
        score_panel = RoundedRectangle(width=11.2, height=5.5, corner_radius=0.22, stroke_color=BOUNDARY, stroke_width=2, fill_color="#263B47", fill_opacity=1)
        numerator = self.card("ACCEPTED USEFUL WORK", "predicate + authority + verify", EVIDENCE, 4.6).shift(UP * 1.7)
        denominator = self.card("TOTAL CONTRACT COST", "complete causal bill", COPPER, 4.6).shift(UP * -0.65)
        ratio_bar = Line(LEFT * 2.7, RIGHT * 2.7, color=ACCENT, stroke_width=5).shift(UP * 0.52)
        counters = VGroup(*[
            self.card(name, detail, color, 1.75).scale(0.72)
            for name, detail, color in [
                ("UNSAFE", "effects", ROLLBACK), ("REFUSAL", "false", AUTHORITY),
                ("RECOVERY", "success", EVIDENCE), ("LATENCY", "tail", BOUNDARY),
                ("HUMAN", "burden", RESIDUAL), ("FAILURES", "tail", ROLLBACK),
                ("MAINTAIN", "lifecycle", COPPER),
            ]
        ]).arrange(RIGHT, buff=0.13).shift(UP * -1.55)
        self.play_beat(
            20,
            FadeOut(policy_lanes), FadeOut(matched),
            FadeIn(score_panel), FadeIn(numerator, shift=UP * -0.1), Create(ratio_bar), FadeIn(denominator, shift=UP * 0.1),
            LaggedStart(*[FadeIn(counter, shift=UP * 0.12) for counter in counters], lag_ratio=0.09),
        )

        # 21 — the current chapter stops at argument support.
        boundary = proof_boundary("CURRENT SUPPORT: ARGUMENT", "accounting design + finite route fixtures").scale(1.15)
        excluded = VGroup(*[
            self.label(value, 17, MUTED, "BOLD")
            for value in ["MEASURED EFFICIENCY", "TRANSFER", "SAFETY", "ASI"]
        ]).arrange(RIGHT, buff=0.52).shift(UP * -2.0)
        stop_bars = VGroup(*[
            Line(label.get_left() + LEFT * 0.12 + UP * 0.18, label.get_left() + LEFT * 0.12 + UP * -0.18, color=ROLLBACK, stroke_width=4)
            for label in excluded
        ])
        support_ceiling = Line(LEFT * 4.6, RIGHT * 4.6, color=ROLLBACK, stroke_width=4).shift(UP * 1.65)
        claim_probe = self.card("CLAIM", "ASI", ROLLBACK, 1.8).scale(0.75).shift(UP * -3.0)
        claim_path = Line(claim_probe.get_center(), UP * 1.12, color=ROLLBACK)
        self.play_beat(
            21,
            FadeOut(score_panel), FadeOut(numerator), FadeOut(ratio_bar), FadeOut(denominator), FadeOut(counters),
            AnimationGroup(FadeIn(boundary, scale=0.9), FadeIn(claim_probe), lag_ratio=0),
            Create(support_ceiling),
            MoveAlongPath(claim_probe, claim_path),
            LaggedStart(*[FadeIn(label) for label in excluded], lag_ratio=0.12),
            LaggedStart(*[Create(bar) for bar in stop_bars], lag_ratio=0.12),
        )

        # 22 — return to the invoice and hand the ticket to authority.
        final_invoice = self.invoice().scale(0.62).shift(LEFT * 4.7 + UP * 0.25)
        final_bill = self.weight("9", "complete bill", EVIDENCE, 2.2).shift(LEFT * 2.55 + UP * -1.25)
        seals = VGroup(
            self.check("QUALITY", EVIDENCE), self.check("AUTH", AUTHORITY),
            self.check("VERIFY", EVIDENCE), self.check("FALLBACK", RESIDUAL),
            self.check("REPAIR", ROLLBACK),
        ).arrange(RIGHT, buff=0.3).scale(0.72).shift(UP * 2.35 + LEFT * 0.7)
        final_ticket = self.ticket().shift(LEFT * 1.4 + UP * 0.25)
        authority_boundary = VGroup(
            Line(UP * 2.1, UP * -2.1, color=AUTHORITY, stroke_width=7),
            self.label("PERMISSION STOPS HERE", 18, AUTHORITY, "BOLD").rotate(1.5708).shift(RIGHT * 0.28),
        ).shift(RIGHT * 3.2)
        next_title = VGroup(
            self.label("NEXT", 17, ACCENT, "BOLD"),
            self.label("SYSTEM BOUNDARIES\nAND AUTHORITY", 27, INK, "BOLD"),
        ).arrange(UP * -1, buff=0.12).shift(RIGHT * 5.0 + UP * 0.1)
        handoff_path = Line(final_ticket.get_center(), RIGHT * 1.85 + UP * 0.25, color=ACCENT, stroke_width=4)
        self.play_beat(
            22,
            FadeOut(boundary), FadeOut(excluded), FadeOut(stop_bars), FadeOut(support_ceiling), FadeOut(claim_probe),
            FadeIn(final_invoice), FadeIn(final_bill),
            LaggedStart(*[FadeIn(seal, scale=0.8) for seal in seals], lag_ratio=0.1),
            FadeIn(final_ticket), Create(authority_boundary),
            MoveAlongPath(final_ticket, handoff_path),
            FadeIn(next_title, shift=RIGHT * 0.15),
        )

        self.wait_until(self.TARGET_DURATION)
