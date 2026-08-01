"""Generation-2 visual abstract for “System Boundaries and Authority.”

A refund token moves inside a typed authority envelope through accounting,
approval, external-effect, and observation boundaries. Capability stays cyan;
authority stays amber; the visual never lets one silently become the other.
"""

from __future__ import annotations

from manim import (
    AnimationGroup,
    ArcBetweenPoints,
    Arrow,
    Circle,
    Create,
    Cross,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Group,
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
    text,
)


class SystemBoundariesAuthorityGeneration2(AsiScene):
    TARGET_DURATION = 279.630
    ENDS = [
        8.355, 20.910, 35.265, 45.520, 56.900, 70.005,
        80.785, 91.765, 103.620, 115.425, 130.455, 142.760,
        157.440, 171.220, 184.300, 195.655, 207.235, 212.575,
        224.165, 237.820, 251.650, 257.300, 267.055, 279.630,
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
        active = None
        if fade_prefix and content:
            anchor_count = min(2, len(content))
            crossfade = AnimationGroup(
                AnimationGroup(*fade_prefix, lag_ratio=0),
                AnimationGroup(*content[:anchor_count], lag_ratio=0),
                lag_ratio=0,
                run_time=min(0.8, remaining * 0.12),
            )
            tail = content[anchor_count:]
            active = Succession(
                crossfade,
                LaggedStart(*tail, lag_ratio=0.2, run_time=max(0.05, remaining - 1.15)),
            ) if tail else crossfade
        elif animations:
            active = LaggedStart(*animations, lag_ratio=0.2)
        run_time = max(0.05, remaining - min(settle, remaining * 0.22))
        if active is not None:
            self.play(active, run_time=run_time)
        self.wait_until(end)

    @staticmethod
    def label(value: str, size: int = 20, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 1.6, height: float = 0.55) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=color, stroke_width=2.4,
            fill_color=SURFACE, fill_opacity=1,
        )
        return VGroup(shell, self.label(value, 14, color, "BOLD").move_to(shell))

    def refund(self, *, compact: bool = False) -> VGroup:
        w, h = (2.2, 1.25) if compact else (3.0, 2.25)
        shell = RoundedRectangle(
            width=w, height=h, corner_radius=0.13,
            stroke_color=ACCENT, stroke_width=3,
            fill_color="#142b37", fill_opacity=1,
        )
        title = self.label("REFUND 47", 19 if compact else 24, ACCENT, "BOLD").shift(UP * (0.28 if compact else 0.72))
        if compact:
            amount = self.label("$240", 16, INK, "BOLD").shift(UP * -0.24)
            return VGroup(shell, title, amount)
        rows = VGroup(
            self.label("ACCOUNT  47   ✓", 15, EVIDENCE),
            self.label("AMOUNT   $240 ✓", 15, EVIDENCE),
            self.label("COMMAND  ISSUE ✓", 15, EVIDENCE),
        ).arrange(UP * -1, buff=0.16).shift(UP * -0.25)
        return VGroup(shell, title, rows)

    def membrane(self, title: str, x: float, color: str = AUTHORITY) -> VGroup:
        line = Line(UP * 3.0, UP * -3.0, color=color, stroke_width=5).shift(RIGHT * x)
        ticks = VGroup(*[
            Line(LEFT * 0.12, RIGHT * 0.12, color=color, stroke_width=3).move_to([x, y, 0])
            for y in (-2.2, -1.1, 0, 1.1, 2.2)
        ])
        tag = self.label(title, 13, color, "BOLD").rotate(1.5708).next_to(line, RIGHT, buff=0.12)
        return VGroup(line, ticks, tag)

    def stamp(self, name: str, value: str, color: str = AUTHORITY, width: float = 1.65) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=0.64, corner_radius=0.08,
            stroke_color=color, stroke_width=2,
            fill_color=SURFACE, fill_opacity=1,
        )
        labels = VGroup(
            self.label(name, 10, MUTED, "BOLD"),
            self.label(value, 13, color, "BOLD"),
        ).arrange(UP * -1, buff=0.02).move_to(shell)
        return VGroup(shell, labels)

    def envelope(self, *, missing: str | None = None) -> VGroup:
        shell = RoundedRectangle(
            width=5.55, height=3.25, corner_radius=0.18,
            stroke_color=AUTHORITY, stroke_width=3,
            fill_color="#181f21", fill_opacity=0.96,
        )
        flap = VGroup(
            Line(shell.get_corner(UP + LEFT), ORIGIN + UP * -0.25, color=AUTHORITY, stroke_width=2),
            Line(shell.get_corner(UP + RIGHT), ORIGIN + UP * -0.25, color=AUTHORITY, stroke_width=2),
        ).move_to(shell)
        fields = [
            ("PRINCIPAL", "USER 12"), ("DOMAIN", "ACCOUNTING"), ("OPERATION", "READ"),
            ("TARGET", "RECORD 47"), ("CLASS", "READ"), ("SCOPE", "ONE RECORD"),
            ("CEILING", "CALLER"), ("EPOCH", "7"), ("EXPIRY", "14:05"),
            ("RECEIPTS", "REQUIRED"),
        ]
        stamps = VGroup()
        for i, (name, value) in enumerate(fields):
            color = ROLLBACK if missing == name else AUTHORITY
            shown = "MISSING" if missing == name else value
            item = self.stamp(name, shown, color, width=1.0).scale(0.72)
            item.move_to([-2.15 + (i % 5) * 1.08, 1.12 - (i // 5) * 2.22, 0])
            stamps.add(item)
        return VGroup(shell, flap, stamps)

    def receipt(self, name: str, detail: str, color: str = EVIDENCE) -> VGroup:
        shell = RoundedRectangle(
            width=1.85, height=0.86, corner_radius=0.08,
            stroke_color=color, stroke_width=2.2,
            fill_color=SURFACE, fill_opacity=1,
        )
        notch = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=1).move_to(shell.get_left() + RIGHT * 0.18)
        labels = VGroup(
            self.label(name, 13, color, "BOLD"), self.label(detail, 10, MUTED),
        ).arrange(UP * -1, buff=0.04).move_to(shell).shift(RIGHT * 0.08)
        return VGroup(shell, notch, labels)

    def permission(self, name: str, color: str, sides: int = 0) -> VGroup:
        if sides == 0:
            shape = Circle(radius=0.38, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        else:
            from manim import RegularPolygon
            shape = RegularPolygon(sides, radius=0.43, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        tag = self.label(name, 12, color, "BOLD").next_to(shape, UP * -1, buff=0.08)
        return VGroup(shape, tag)

    def construct(self) -> None:
        self.camera.background_color = "#14262F"
        # 1 — correctness is complete, authority is unresolved.
        refund = self.refund().shift(LEFT * 3.5)
        boundary = self.membrane("EFFECT", 1.45, ROLLBACK)
        bank = VGroup(
            Circle(radius=0.9, color=BOUNDARY, stroke_width=3, fill_color=SURFACE, fill_opacity=1),
            self.label("BANK", 22, INK, "BOLD"),
        ).shift(RIGHT * 4.15)
        effect_arrow = Arrow(refund.get_right(), boundary[0].get_center() + LEFT * 0.12, color=ACCENT, buff=0.15, stroke_width=5)
        question = self.badge("SHOULD IT RUN?", ROLLBACK, 2.5).shift(UP * 3.25)
        self.play_beat(1, FadeIn(refund), Create(effect_arrow), Create(boundary), FadeIn(bank), FadeIn(question), settle=0.7)

        # 2 — one artifact occupies unequal CAN and MAY coordinates.
        old = Group(*self.mobjects)
        x_axis = Arrow(LEFT * 4.7, RIGHT * 4.7, color=ACCENT, buff=0, stroke_width=3).shift(UP * -0.8)
        y_axis = Arrow(UP * -2.8, UP * 2.8, color=AUTHORITY, buff=0, stroke_width=3).shift(LEFT * 2.6)
        axes = VGroup(
            x_axis, y_axis,
            self.label("CAN", 18, ACCENT, "BOLD").next_to(x_axis, RIGHT),
            self.label("MAY", 18, AUTHORITY, "BOLD").next_to(y_axis, UP),
        )
        capable = self.badge("CAPABLE", ACCENT, 1.7).move_to([2.7, -0.8, 0])
        not_authorized = self.badge("NOT YET AUTHORIZED", ROLLBACK, 2.75).move_to([2.7, 0.15, 0])
        token = self.refund(compact=True).scale(0.72).move_to([2.7, -0.25, 0])
        delta = DashedLine([2.7, -0.8, 0], [2.7, 1.8, 0], color=AUTHORITY, dash_length=0.13)
        self.play_beat(2, FadeOut(old), Create(axes), FadeIn(capable), Create(delta), FadeIn(not_authorized), FadeIn(token), settle=0.45)

        # 3 — typed authority envelope is assembled around the refund.
        old = Group(*self.mobjects)
        env = self.envelope().scale(0.94)
        inner_refund = self.refund(compact=True).scale(0.64).move_to(env).shift(UP * -0.02)
        title = self.badge("AUTHORITY ENVELOPE", AUTHORITY, 2.8).shift(UP * 3.2)
        self.play_beat(3, FadeOut(old), FadeIn(title), Create(env[0]), Create(env[1]), FadeIn(inner_refund), LaggedStart(*[FadeIn(s) for s in env[2]], lag_ratio=0.1), settle=0.5)

        # 4 — capability proxies fail to mint a missing permission.
        proxies = VGroup(
            self.badge("GOOD ANSWER", ACCENT, 1.8), self.badge("TRUSTED MODEL", ACCENT, 1.9),
            self.badge("TOOL READY", ACCENT, 1.65), self.badge("ROUTE 0.94", ACCENT, 1.65),
        ).arrange(RIGHT, buff=0.24).shift(UP * 3.15)
        missing_socket = VGroup(
            Circle(radius=0.45, color=ROLLBACK, stroke_width=3),
            self.label("PERMISSION\nMISSING", 11, ROLLBACK, "BOLD").move_to([0, -0.02, 0]),
        ).shift(RIGHT * 4.95 + UP * -0.1)
        path = ArcBetweenPoints(env.get_right(), missing_socket.get_left(), angle=-0.35)
        self.play_beat(4, FadeOut(title), FadeIn(proxies), Create(path), FadeIn(missing_socket), Indicate(missing_socket, color=ROLLBACK), env.animate.shift(LEFT * 0.85), inner_refund.animate.shift(LEFT * 0.85), settle=0.35)

        # 5 — scoped read authority opens one record and returns one receipt.
        old = Group(*self.mobjects)
        accounting = RoundedRectangle(width=9.2, height=5.2, corner_radius=0.2, stroke_color=BOUNDARY, stroke_width=3, fill_color="#12242c", fill_opacity=0.65)
        account_tag = self.badge("ACCOUNTING DOMAIN", BOUNDARY, 2.7).shift(UP * 3.15)
        records = VGroup(*[
            self.receipt(f"CUSTOMER {i}", "LOCKED", MUTED) for i in (45, 46, 47, 48, 49)
        ]).arrange(RIGHT, buff=0.24).shift(UP * 0.35)
        records[2] = self.receipt("CUSTOMER 47", "IN SCOPE", EVIDENCE).move_to(records[2])
        small_env = self.badge("READ · USER 12 · RECORD 47", AUTHORITY, 3.4).shift(LEFT * 3.5 + UP * -1.5)
        read_receipt = self.receipt("READ", "RECEIPT 01").shift(RIGHT * 3.6 + UP * -1.5)
        rail = Line(LEFT * 4.5, RIGHT * 4.5, color=BOUNDARY, stroke_width=2).shift(UP * -2.35)
        self.play_beat(5, FadeOut(old), Create(accounting), FadeIn(account_tag), LaggedStart(*[FadeIn(r) for r in records], lag_ratio=0.12), FadeIn(small_env), Create(rail), TransformFromCopy(records[2], read_receipt), settle=0.35)

        # 6 — transform is a new permission class, not ambient read power.
        read_stamp = self.badge("READ", ACCENT, 1.4).shift(LEFT * 1.7 + UP * -0.8)
        transform_stamp = self.badge("TRANSFORM", AUTHORITY, 1.9).shift(RIGHT * 0.1 + UP * -0.8)
        summary = self.receipt("SUMMARY 47", "TAX + TOTAL", ACCENT).shift(RIGHT * 2.4 + UP * 0.35)
        transform_receipt = self.receipt("TRANSFORM", "RECEIPT 02").shift(RIGHT * 1.4 + UP * -2.35)
        not_equal = self.label("≠", 42, ROLLBACK, "BOLD").move_to([-0.75, -0.8, 0])
        self.play_beat(6, FadeIn(read_stamp), FadeIn(not_equal), FadeIn(transform_stamp), TransformFromCopy(records[2], summary), TransformFromCopy(transform_stamp, transform_receipt), settle=0.4)

        # 7 — external target changes class to DISCLOSE.
        old = Group(*self.mobjects)
        accounting_box = RoundedRectangle(width=5.5, height=5.5, corner_radius=0.2, stroke_color=BOUNDARY, stroke_width=3, fill_color="#12242c", fill_opacity=0.65).shift(LEFT * 3.2)
        vendor_box = RoundedRectangle(width=4.5, height=5.5, corner_radius=0.2, stroke_color=COPPER, stroke_width=3, fill_color="#241e19", fill_opacity=0.5).shift(RIGHT * 3.75)
        external = self.membrane("EXTERNAL", 0.45, AUTHORITY)
        summary2 = self.receipt("SUMMARY 47", "READY", ACCENT).shift(LEFT * 3.3)
        class_swap = VGroup(self.badge("TRANSFORM", MUTED, 1.9), Arrow(LEFT * 0.4, RIGHT * 0.4, color=AUTHORITY), self.badge("DISCLOSE", AUTHORITY, 1.8)).arrange(RIGHT, buff=0.18).shift(UP * 2.55)
        route = Arrow(summary2.get_right(), external[0].get_center() + LEFT * 0.15, color=ACCENT, stroke_width=5, buff=0.15)
        self.play_beat(7, FadeOut(old), Create(accounting_box), Create(vendor_box), Create(external), FadeIn(summary2), FadeIn(class_swap), GrowArrow(route), settle=0.6)

        # 8 — disclosure is missing, denial becomes an owned artifact.
        disclose_missing = self.badge("DISCLOSE: MISSING", ROLLBACK, 2.7).shift(UP * 0.55)
        denial = self.receipt("DENIED", "POLICY v7", ROLLBACK).shift(RIGHT * 2.2 + UP * -0.9)
        owner = self.badge("OWNER · APPROVAL SERVICE", RESIDUAL, 3.0).shift(RIGHT * 3.2 + UP * -2.2)
        stop_dot = Dot(radius=0.16, color=ROLLBACK).move_to(external[0].get_center())
        self.play_beat(8, FadeIn(disclose_missing), FadeIn(stop_dot), FadeIn(denial), GrowArrow(Arrow(denial.get_bottom(), owner.get_top(), color=RESIDUAL, buff=0.12)), FadeIn(owner), settle=0.55)

        # 9 — escalation narrows instead of widening ambient authority.
        old = Group(*self.mobjects)
        narrow_shell = RoundedRectangle(width=8.8, height=4.8, corner_radius=0.18, stroke_color=AUTHORITY, stroke_width=3, fill_color="#191f21", fill_opacity=0.95)
        narrow_title = self.badge("NARROW APPROVAL GRANT", AUTHORITY, 2.8).shift(UP * 3.05)
        narrow_stamps = VGroup(
            self.stamp("TARGET", "VENDOR 47"), self.stamp("CONTENT", "SUMMARY SHA"),
            self.stamp("USES", "1"), self.stamp("EXPIRY", "14:05"),
            self.stamp("EFFECT", "RECEIPT"), self.stamp("OBSERVE", "REQUIRED"),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.28, 0.55)).move_to(narrow_shell)
        approval_key = VGroup(Circle(radius=0.45, color=AUTHORITY, stroke_width=4), Line(RIGHT * 0.35, RIGHT * 1.5, color=AUTHORITY, stroke_width=5), Line(RIGHT * 1.1, RIGHT * 1.1 + UP * -0.35, color=AUTHORITY, stroke_width=5)).shift(LEFT * 4.8)
        self.play_beat(9, FadeOut(old), Create(narrow_shell), FadeIn(narrow_title), FadeIn(approval_key), LaggedStart(*[FadeIn(s) for s in narrow_stamps], lag_ratio=0.12), settle=0.35)

        # 10 — request, dispatch, effect, and observation remain separate.
        old = Group(*self.mobjects)
        membrane2 = self.membrane("AUTHORIZED EFFECT", 0.0, EVIDENCE)
        refund2 = self.refund(compact=True).scale(0.78).shift(LEFT * 4.6 + UP * 1.4)
        approved = self.badge("APPROVED · ONE USE", AUTHORITY, 2.5).shift(LEFT * 4.3 + UP * 2.65)
        effect = VGroup(Circle(radius=0.75, color=EVIDENCE, stroke_width=4), self.label("$240\nSENT", 18, EVIDENCE, "BOLD")).shift(RIGHT * 4.55 + UP * 1.4)
        receipts = VGroup(
            self.receipt("DISPATCH", "REQUESTED"), self.receipt("EFFECT", "RAN"), self.receipt("OBSERVE", "MATCHED"),
        ).arrange(RIGHT, buff=0.6).shift(UP * -1.9)
        crossing = ArcBetweenPoints(refund2.get_center(), effect.get_center(), angle=-0.25)
        self.play_beat(10, FadeOut(old), Create(membrane2), FadeIn(refund2), FadeIn(approved), Create(crossing), MoveAlongPath(refund2, crossing), FadeOut(refund2), FadeIn(effect), LaggedStart(*[FadeIn(r) for r in receipts], lag_ratio=0.25), settle=0.45)

        # 11 — the deputy tries to substitute its broader credential.
        old = Group(*self.mobjects)
        caller = VGroup(self.refund(compact=True).scale(0.65), self.badge("CALLER · LOW", RESIDUAL, 1.9).shift(UP * -1.0)).shift(LEFT * 4.5 + UP * 0.6)
        deputy = VGroup(
            RoundedRectangle(width=3.0, height=2.4, corner_radius=0.15, stroke_color=ACCENT, stroke_width=3, fill_color=SURFACE, fill_opacity=1),
            self.label("POWERFUL\nDEPUTY", 22, ACCENT, "BOLD"), self.badge("BROAD KEY", AUTHORITY, 1.8).shift(UP * -0.75),
        ).shift(UP * 0.6)
        protected = VGroup(Circle(radius=0.9, color=ROLLBACK, stroke_width=4), self.label("PROTECTED\nEFFECT", 17, ROLLBACK, "BOLD")).shift(RIGHT * 4.6 + UP * 0.6)
        borrow_path = ArcBetweenPoints(caller.get_right(), deputy.get_left(), angle=0.3)
        effect_path = ArcBetweenPoints(deputy.get_right(), protected.get_left(), angle=-0.25)
        self.play_beat(11, FadeOut(old), FadeIn(caller), FadeIn(deputy), FadeIn(protected), Create(borrow_path), Create(effect_path), Indicate(deputy[2], color=AUTHORITY), settle=0.55)

        # 12 — tuple comparison reveals substitution and preserves the caller ceiling.
        ceiling = Line(LEFT * 5.8, RIGHT * 5.8, color=AUTHORITY, stroke_width=4).shift(UP * 2.75)
        ceiling_label = self.badge("CALLER CEILING", AUTHORITY, 2.2).shift(UP * 3.25)
        mismatches = VGroup(
            self.stamp("PRINCIPAL", "≠", ROLLBACK), self.stamp("GRANT", "≠", ROLLBACK),
            self.stamp("TARGET", "≠", ROLLBACK), self.stamp("DELEGATION", "≠", ROLLBACK),
        ).arrange(RIGHT, buff=0.25).shift(UP * -1.7)
        deny2 = self.badge("SUBSTITUTION DENIED", ROLLBACK, 2.8).shift(UP * -2.85)
        self.play_beat(12, FadeIn(ceiling), FadeIn(ceiling_label), LaggedStart(*[FadeIn(m) for m in mismatches], lag_ratio=0.18), Indicate(caller, color=RESIDUAL), Indicate(deputy, color=ROLLBACK), FadeIn(deny2), settle=0.4)

        # 13 — authority is a lifecycle; identical replay meets closed gates.
        old = Group(*self.mobjects)
        timeline = Arrow(LEFT * 5.4, RIGHT * 5.4, color=BOUNDARY, stroke_width=3, buff=0).shift(UP * 0.9)
        states = VGroup(
            self.badge("VALID", EVIDENCE), self.badge("EXPIRED", COPPER),
            self.badge("REVOKED", ROLLBACK), self.badge("USED", RESIDUAL),
        ).arrange(RIGHT, buff=0.85).shift(UP * 0.9)
        replay = self.refund(compact=True).scale(0.58).shift(LEFT * 4.7 + UP * -1.35)
        replay_line = Arrow(LEFT * 4.1, RIGHT * 4.9, color=ACCENT, stroke_width=4, buff=0).shift(UP * -1.35)
        closed = VGroup(*[
            Cross(Circle(radius=0.28, color=ROLLBACK), stroke_color=ROLLBACK).move_to([x, -1.35, 0]) for x in (-0.7, 1.65, 4.0)
        ])
        self.play_beat(13, FadeOut(old), Create(timeline), FadeIn(states), FadeIn(replay), GrowArrow(replay_line), LaggedStart(*[Create(c) for c in closed], lag_ratio=0.22), FadeIn(self.badge("IDENTICAL REPLAY · DENIED", ROLLBACK, 2.8).shift(UP * -2.55)), settle=0.45)

        # 14 — capability replacement does not inherit authority handles.
        old = Group(*self.mobjects)
        slot = RoundedRectangle(width=4.0, height=3.4, corner_radius=0.18, stroke_color=BOUNDARY, stroke_width=3, fill_color=SURFACE, fill_opacity=1).shift(LEFT * 2.2)
        model_a = self.badge("MODEL A", MUTED, 1.7).shift(LEFT * 2.2).set_z_index(3)
        model_b = self.badge("MODEL B ↑", ACCENT, 1.9).shift(LEFT * 2.2).set_z_index(3)
        slot_tag = self.badge("CAPABILITY SLOT", BOUNDARY, 2.3).shift(LEFT * 2.2 + UP * 2.25)
        handles = VGroup(
            self.stamp("SECRET", "LOCKED", ROLLBACK), self.stamp("APPROVAL", "LOCKED", ROLLBACK), self.stamp("LIVE GRANT", "LOCKED", ROLLBACK),
        ).arrange(UP * -1, buff=0.45).shift(RIGHT * 3.35)
        divider = self.membrane("AUTHORITY", 0.65, AUTHORITY)
        self.add(model_a)
        self.play_beat(14, FadeOut(old), Create(slot), FadeIn(slot_tag), ReplacementTransform(model_a, model_b), Create(divider), LaggedStart(*[FadeIn(h) for h in handles], lag_ratio=0.2), FadeIn(self.badge("NOT INHERITED", ROLLBACK, 2.2).shift(RIGHT * 3.35 + UP * -2.7)), settle=0.5)

        # 15 — six permission classes resist role-label collapse.
        old = Group(*self.mobjects)
        permissions = VGroup(
            self.permission("READ", ACCENT, 0), self.permission("TRANSFORM", AUTHORITY, 3),
            self.permission("DISCLOSE", RESIDUAL, 4), self.permission("WRITE", COPPER, 5),
            self.permission("EXECUTE", EVIDENCE, 6), self.permission("APPROVE", "#B78CFF", 8),
        ).arrange_in_grid(rows=2, cols=3, buff=(1.15, 0.9)).shift(UP * -0.2)
        role = self.badge("ROLE: ALL ACCESS", ROLLBACK, 2.8).shift(UP * 3.0)
        slash = Cross(role[0], stroke_color=ROLLBACK, stroke_width=4)
        self.play_beat(15, FadeOut(old), LaggedStart(*[FadeIn(p) for p in permissions], lag_ratio=0.15), FadeIn(role), Create(slash), settle=0.45)

        # 16 — denial compiles into a useful machine-visible record.
        old = Group(*self.mobjects)
        denied_env = self.envelope(missing="CLASS").scale(0.72).shift(LEFT * 3.8)
        denial_receipt = RoundedRectangle(width=5.0, height=4.7, corner_radius=0.18, stroke_color=RESIDUAL, stroke_width=3, fill_color=SURFACE, fill_opacity=1).shift(RIGHT * 2.8)
        denial_fields = VGroup(
            self.stamp("MISSING", "DISCLOSE", ROLLBACK, 2.0), self.stamp("POLICY", "v7", AUTHORITY, 2.0),
            self.stamp("OWNER", "APPROVER", RESIDUAL, 2.0), self.stamp("ESCALATE", "LAWFUL PATH", EVIDENCE, 2.0),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.55)).move_to(denial_receipt)
        compile_arrow = Arrow(denied_env.get_right(), denial_receipt.get_left(), color=RESIDUAL, stroke_width=4, buff=0.2)
        self.play_beat(16, FadeOut(old), FadeIn(denied_env), GrowArrow(compile_arrow), Create(denial_receipt), LaggedStart(*[FadeIn(f) for f in denial_fields], lag_ratio=0.18), settle=0.4)

        # 17 — accepted refusal survives three capability successes.
        old = Group(*self.mobjects)
        checks = VGroup(
            self.badge("PLAN ✓", ACCENT, 1.65), self.badge("SOURCE ✓", ACCENT, 1.8), self.badge("CAPABILITY ✓", ACCENT, 2.1),
        ).arrange(RIGHT, buff=0.45).shift(UP * 1.7)
        may_gate = VGroup(Circle(radius=0.75, color=AUTHORITY, stroke_width=4), self.label("MAY?", 20, AUTHORITY, "BOLD")).shift(UP * -0.1)
        refuse = self.badge("REFUSE · ACCEPTED", EVIDENCE, 2.7).shift(UP * -2.2)
        flows = VGroup(*[Arrow(c.get_bottom(), may_gate.get_top(), color=ACCENT, stroke_width=3, buff=0.15) for c in checks])
        self.play_beat(17, FadeOut(old), LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.18), LaggedStart(*[GrowArrow(a) for a in flows], lag_ratio=0.12), FadeIn(may_gate), FadeIn(refuse), settle=0.55)

        # 18 — declare the local finite evidence boundary before counts.
        old = Group(*self.mobjects)
        board = RoundedRectangle(width=10.8, height=5.4, corner_radius=0.2, stroke_color=BOUNDARY, stroke_width=3, fill_color="#12242c", fill_opacity=0.65)
        board_tag = self.badge("LOCAL · FINITE · EXACT COUNTS", BOUNDARY, 3.7).shift(UP * 3.15)
        sockets = VGroup(*[
            RoundedRectangle(width=2.2, height=1.1, corner_radius=0.1, stroke_color=MUTED, stroke_width=2, fill_color=SURFACE, fill_opacity=1)
            for _ in range(7)
        ]).arrange_in_grid(rows=2, cols=4, buff=(0.35, 0.45)).shift(UP * -0.2)
        self.play_beat(18, FadeOut(old), Create(board), FadeIn(board_tag), LaggedStart(*[Create(s) for s in sockets], lag_ratio=0.1), settle=0.35)

        # 19 — exact denominators fill the bounded board.
        counter_values = [("6", "FIXTURES"), ("2", "DENIALS"), ("1", "EFFECT"), ("1", "OBSERVED"), ("1", "ROLLBACK"), ("5", "REVOKED"), ("38", "REJECTED")]
        counters = VGroup()
        for socket, (number, label) in zip(sockets, counter_values):
            counter = VGroup(self.label(number, 28, EVIDENCE, "BOLD"), self.label(label, 12, MUTED, "BOLD")).arrange(UP * -1, buff=0.05).move_to(socket)
            counters.add(counter)
        self.play_beat(19, LaggedStart(*[FadeIn(c) for c in counters], lag_ratio=0.14), settle=0.4)

        # 20 — reachable modeled transitions remain below the caller ceiling.
        old = Group(*self.mobjects)
        ceiling2 = Line(LEFT * 5.7, RIGHT * 5.7, color=AUTHORITY, stroke_width=4).shift(UP * 2.35)
        ceiling_tag2 = self.badge("CALLER CEILING", AUTHORITY, 2.2).shift(UP * 3.0)
        rail2 = Line(LEFT * 5.0, RIGHT * 4.0, color=BOUNDARY, stroke_width=3).shift(UP * -0.25)
        names = ["ISSUE", "DISPATCH", "EFFECT", "REVOKE", "ONE-SHOT", "ROLLBACK"]
        nodes = VGroup(*[
            VGroup(Circle(radius=0.36, color=EVIDENCE, stroke_width=3, fill_color=SURFACE, fill_opacity=1), self.label(str(i + 1), 15, EVIDENCE, "BOLD"), self.label(name, 10, MUTED, "BOLD").shift(UP * -0.65))
            for i, name in enumerate(names)
        ]).arrange(RIGHT, buff=0.75).shift(UP * -0.25)
        support = self.badge("BOUNDED SUPPORT", EVIDENCE, 2.5).shift(UP * -2.45)
        self.play_beat(20, FadeOut(old), Create(ceiling2), FadeIn(ceiling_tag2), Create(rail2), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.16), FadeIn(support), settle=0.4)

        # 21 — production obligations remain across an evidence line.
        old = Group(*self.mobjects)
        evidence_line = self.membrane("EVIDENCE CEILING", 0.0, ROLLBACK)
        current = VGroup(self.badge("FINITE MODEL", EVIDENCE, 2.1), self.badge("38/38 REJECTED", EVIDENCE, 2.2), self.badge("EXACT ROLLBACK", EVIDENCE, 2.2)).arrange(UP * -1, buff=0.45).shift(LEFT * 3.5)
        open_work = VGroup(
            self.badge("AUTHENTIC ID", MUTED, 2.0), self.badge("COMPLETE MEDIATION", MUTED, 2.6),
            self.badge("CONCURRENT REVOCATION", MUTED, 3.0), self.badge("SECURE WRAPPERS", MUTED, 2.4),
            self.badge("PRODUCTION ADAPTERS", MUTED, 2.7), self.badge("OPEN-WORLD OBSERVATION", MUTED, 3.0),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.35, 0.45)).shift(RIGHT * 3.4)
        not_deployed = self.badge("NOT DEPLOYED AUTHORIZATION", ROLLBACK, 3.6).shift(UP * 3.15)
        self.play_beat(21, FadeOut(old), Create(evidence_line), FadeIn(not_deployed), LaggedStart(*[FadeIn(c) for c in current], lag_ratio=0.15), LaggedStart(*[FadeIn(o) for o in open_work], lag_ratio=0.1), settle=0.55)

        # 22 — restore the signature envelope under its argument ceiling.
        old = Group(*self.mobjects)
        final_env = self.envelope().scale(0.82).shift(UP * -0.2)
        final_refund = self.refund(compact=True).scale(0.58).move_to(final_env).shift(UP * -0.02)
        support_label = self.badge("DESIGN RATIONALE · SUPPORT: ARGUMENT", AUTHORITY, 4.6).shift(UP * 3.2)
        self.play_beat(22, FadeOut(old), FadeIn(support_label), Create(final_env[0]), FadeIn(final_refund), FadeIn(final_env[2]), settle=0.35)

        # 23 — four design properties pass; broad claims remain below the bar.
        properties = VGroup(
            self.badge("EXPLICIT", AUTHORITY, 1.7), self.badge("VERSIONED", AUTHORITY, 1.9),
            self.badge("REVOCABLE", AUTHORITY, 1.9), self.badge("RECEIPT-BEARING", AUTHORITY, 2.5),
        ).arrange(RIGHT, buff=0.35).shift(UP * -2.25)
        claim_bar = Line(LEFT * 5.5, RIGHT * 5.5, color=ROLLBACK, stroke_width=4).shift(UP * -3.05)
        nonclaims = self.label("NO SAFETY   ·   NO TRANSFER   ·   NO ASI CLAIM", 15, ROLLBACK, "BOLD").shift(UP * -3.42)
        self.play_beat(23, LaggedStart(*[FadeIn(p) for p in properties], lag_ratio=0.18), Create(claim_bar), FadeIn(nonclaims), settle=0.55)

        # 24 — both outcomes retain an inspectable trail; the residual moves on.
        old = Group(*self.mobjects)
        allowed = VGroup(self.refund(compact=True).scale(0.58), self.badge("ALLOWED", EVIDENCE, 1.6).shift(UP * -1.05)).shift(LEFT * 4.35 + UP * 0.65)
        denied_final = VGroup(self.refund(compact=True).scale(0.58), self.badge("DENIED", ROLLBACK, 1.6).shift(UP * -1.05)).shift(LEFT * 1.25 + UP * 0.65)
        trail = Line(LEFT * 5.1, RIGHT * 1.1, color=BOUNDARY, stroke_width=3).shift(UP * -1.45)
        receipts_final = VGroup(*[Dot(radius=0.12, color=EVIDENCE) for _ in range(5)]).arrange(RIGHT, buff=0.8).move_to(trail)
        next_membrane = self.membrane("NEXT", 2.45, COPPER)
        cracks = VGroup(
            Line([3.1, 1.8, 0], [3.55, 1.25, 0], color=ROLLBACK, stroke_width=4),
            Line([3.55, 1.25, 0], [3.25, 0.7, 0], color=ROLLBACK, stroke_width=4),
            Line([3.55, 1.25, 0], [4.05, 0.95, 0], color=ROLLBACK, stroke_width=4),
        )
        residual = self.badge("OWNED RESIDUAL", RESIDUAL, 2.2).shift(LEFT * 0.6 + UP * -2.5)
        next_title = VGroup(
            self.label("FAILURE MODES OF", 14, MUTED, "BOLD"),
            self.label("UNGOVERNED INTELLIGENCE", 17, INK, "BOLD"),
        ).arrange(UP * -1, buff=0.08).shift(RIGHT * 4.45 + UP * -1.35)
        residual_path = ArcBetweenPoints(residual.get_center(), [3.15, -2.7, 0], angle=0.2)
        self.play_beat(24, FadeOut(old), FadeIn(allowed), FadeIn(denied_final), Create(trail), FadeIn(receipts_final), FadeIn(residual), Create(next_membrane), Create(cracks), MoveAlongPath(residual, residual_path), FadeIn(next_title), settle=0.8)

        self.wait_until(self.TARGET_DURATION)
