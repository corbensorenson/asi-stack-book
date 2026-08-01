"""Generation-2 visual abstract for meaningful human control.

A synthetic transfer episode remains the persistent object. Its apparently
green approval is progressively tested against evidence, time, workload,
authority, intervention, privacy, and responsibility boundaries. The visual
argument ends in safe hold for task reasons, never a score of the reviewer.
"""

from __future__ import annotations

from math import cos, sin

from manim import (
    AnimationGroup, Arc, ArcBetweenPoints, Arrow, Circle, Create, Cross,
    DashedLine, Dot, DOWN, FadeIn, FadeOut, GrowArrow, GrowFromCenter,
    Indicate, LaggedStart, LEFT, Line, MoveAlongPath, ORIGIN, PI, Rectangle,
    ReplacementTransform, RIGHT, RoundedRectangle, TAU, Text,
    Transform, TransformFromCopy, UP, VGroup, Write,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


class HumanFactorsGeneration2(AsiScene):
    TARGET_DURATION = 347.060
    ENDS = [
        10.005, 18.985, 26.715, 38.545, 52.625, 64.530, 79.785,
        92.415, 103.095, 115.350, 126.055, 136.210, 147.015, 161.320,
        172.325, 179.391, 185.380, 198.035, 211.340, 222.245, 235.200,
        245.480, 258.735, 272.765, 283.795, 292.666, 299.425, 316.430,
        331.535, 347.060,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#111F28"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.35) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.05, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            action_budget = max(0.05, remaining - min(settle, remaining * 0.18))
            per_animation = max(0.05, action_budget / len(animations))
            for animation in animations:
                self.play(animation, run_time=per_animation)
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 18, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 2.1, height: float = 0.55) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=color, stroke_width=2.7,
            fill_color=SURFACE, fill_opacity=1,
        )
        return VGroup(shell, self.label(value, 13, color, "BOLD").move_to(shell))

    def panel(self, title: str, color: str, width: float, height: float) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.16,
            stroke_color=color, stroke_width=3.2,
            fill_color="#172A34", fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.25, 3.6), 0.48).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def grid(self, values: list[str], colors: list[str], columns: int, width: float = 2.0) -> VGroup:
        items = VGroup(*[self.badge(v, colors[i], width, 0.5) for i, v in enumerate(values)])
        rows = (len(values) + columns - 1) // columns
        items.arrange_in_grid(rows=rows, cols=columns, buff=(0.16, 0.18))
        return items

    def reviewer(self, color: str = AUTHORITY) -> VGroup:
        head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=SURFACE, fill_opacity=1)
        shoulders = Arc(radius=0.78, start_angle=0.15 * PI, angle=0.7 * PI, color=color, stroke_width=4).rotate(PI)
        shoulders.next_to(head, DOWN, buff=0.05)
        role = self.badge("REVIEWER", color, 1.65, 0.42).scale(0.82).next_to(shoulders, DOWN, buff=0.08)
        return VGroup(head, shoulders, role)

    def episode(self, compact: bool = False) -> VGroup:
        width = 5.0 if not compact else 3.7
        height = 2.6 if not compact else 2.05
        frame = self.panel("TRANSFER EPISODE", ACCENT, width, height)
        rec = self.badge("RECOMMENDATION · GREEN", EVIDENCE, width - 0.6, 0.58).move_to(frame).shift(UP * 0.42)
        conflict = self.badge("PRESSURE · CONTRADICTION", ROLLBACK, width - 0.6, 0.58).move_to(frame).shift(DOWN * 0.42)
        return VGroup(frame, rec, conflict)

    def clock(self, seconds: str, color: str = ROLLBACK) -> VGroup:
        face = Circle(radius=0.73, stroke_color=color, stroke_width=4, fill_color=SURFACE, fill_opacity=1)
        hand = Line(face.get_center(), face.get_center() + UP * 0.48, color=color, stroke_width=5)
        value = self.label(seconds, 20, color, "BOLD").move_to(face).shift(DOWN * 0.22)
        return VGroup(face, hand, value)

    def basin(self, label: str = "SAFE HOLD") -> VGroup:
        shell = RoundedRectangle(
            width=3.2, height=1.15, corner_radius=0.35,
            stroke_color=EVIDENCE, stroke_width=4,
            fill_color="#17352F", fill_opacity=1,
        )
        return VGroup(shell, self.label(label, 20, EVIDENCE, "BOLD").move_to(shell))

    def envelope(self, failed: set[int] | None = None, scale: float = 1.0) -> VGroup:
        failed = failed or set()
        names = ["AUTH", "OBS", "QUAL", "TIME", "LOAD", "STOP", "RECOVER", "CONFLICT"]
        arcs = VGroup()
        labels = VGroup()
        for i, name in enumerate(names):
            color = ROLLBACK if i in failed else EVIDENCE
            arc = Arc(
                radius=1.55, start_angle=i * TAU / 8 + 0.07,
                angle=TAU / 8 - 0.14, color=color, stroke_width=8,
            )
            pos = 2.02 * (arc.point_from_proportion(0.5) - ORIGIN)
            lbl = self.label(name, 11, color, "BOLD").move_to(pos)
            arcs.add(arc)
            labels.add(lbl)
        return VGroup(arcs, labels).scale(scale)

    def construct(self) -> None:
        # 1 — green recommendation, buried conflict, waiting alarms
        episode = self.episode().shift(LEFT * 3.3)
        reviewer = self.reviewer().shift(RIGHT * 1.2)
        approve = self.badge("APPROVE TRANSFER?", AUTHORITY, 2.6, 0.72).shift(RIGHT * 4.6 + UP * 1.1)
        queue = self.grid([str(i) for i in range(1, 8)], [ROLLBACK] * 7, 7, 0.58).scale(0.82).shift(RIGHT * 2.8 + DOWN * 2.35)
        episode[2].set_opacity(0)
        scene1 = VGroup(episode, reviewer, approve, queue)
        self.next_section("b01")
        self.play(
            FadeIn(episode[0], shift=RIGHT * 0.9),
            FadeIn(episode[1], shift=RIGHT * 0.9),
            FadeIn(reviewer, shift=LEFT * 0.9),
            FadeIn(approve, shift=LEFT * 0.9),
            run_time=3.35,
        )
        self.wait_until(3.643)
        self.play(FadeIn(episode[2], shift=UP * 0.85), Indicate(episode[2], color=ROLLBACK, scale_factor=1.12), run_time=3.15)
        self.wait_until(7.226)
        self.play(LaggedStart(*[FadeIn(q, shift=UP * 0.8) for q in queue], lag_ratio=0.09), reviewer.animate.shift(UP * 0.16), run_time=2.35)
        self.wait_until(self.ENDS[0])

        # 2 — irreversibility beats the declared stop path
        commit_clock = self.clock("12s").shift(RIGHT * 3.7 + UP * 0.75)
        stop_clock = self.clock("14s", AUTHORITY).shift(RIGHT * 3.7 + DOWN * 1.3)
        race = Arrow(stop_clock.get_left(), commit_clock.get_left(), color=ROLLBACK, buff=0.15, stroke_width=5)
        present = self.badge("PERSON PRESENT", AUTHORITY, 2.2).next_to(reviewer, UP, buff=0.25)
        scene2 = VGroup(episode, reviewer, queue, commit_clock, stop_clock, race, present)
        self.play_beat(2, FadeOut(approve), FadeIn(commit_clock), FadeIn(stop_clock), GrowArrow(race), FadeIn(present), Indicate(reviewer, color=AUTHORITY), settle=0.55)

        # 3 — viewer prediction
        choices = self.grid(["ACCEPT", "HURRY", "SAFE HOLD"], [ROLLBACK, AUTHORITY, EVIDENCE], 1, 2.5).shift(RIGHT * 3.8)
        forks = VGroup(*[Arrow(LEFT * 1.0, c.get_left(), color=[ROLLBACK, AUTHORITY, EVIDENCE][i], buff=0.08) for i, c in enumerate(choices)])
        keep = self.badge("KEEP YOUR ANSWER", COPPER, 2.6).shift(DOWN * 2.4)
        scene3 = VGroup(episode, reviewer, commit_clock, stop_clock, choices, forks, keep)
        self.play_beat(3, FadeOut(scene2), FadeIn(episode), FadeIn(reviewer), FadeIn(commit_clock), FadeIn(stop_clock), Create(forks), FadeIn(choices), FadeIn(keep), settle=1.1)

        # 4 — automation funnel returns only the rare abnormal case
        routine = self.grid(["ROUTINE"] * 8, [MUTED] * 8, 4, 1.35).shift(LEFT * 4.1)
        funnel_left = Line(LEFT * 2.6 + UP * 2.0, LEFT * 0.6 + UP * 0.45, color=BOUNDARY, stroke_width=5)
        funnel_right = Line(LEFT * 2.6 + DOWN * 2.0, LEFT * 0.6 + DOWN * 0.45, color=BOUNDARY, stroke_width=5)
        abnormal = self.badge("ABNORMAL", ROLLBACK, 2.2, 0.72).shift(RIGHT * 1.15)
        reviewer4 = self.reviewer().shift(RIGHT * 4.3)
        losses = self.grid(["CONTEXT", "PRACTICE", "TIME"], [ROLLBACK] * 3, 3, 1.7).shift(DOWN * 2.35)
        funnel_token = Dot(routine.get_right(), radius=0.15, color=ROLLBACK)
        funnel_path = ArcBetweenPoints(routine.get_right(), abnormal.get_left(), angle=-0.35)
        scene4 = VGroup(routine, funnel_left, funnel_right, abnormal, reviewer4, losses, funnel_token)
        self.next_section("b04")
        self.play(FadeOut(scene3, shift=LEFT * 0.7), FadeIn(routine, shift=RIGHT * 0.6), run_time=2.2)
        self.play(Create(funnel_left), Create(funnel_right), FadeIn(funnel_token), run_time=1.7)
        self.play(MoveAlongPath(funnel_token, funnel_path), run_time=2.25)
        self.play(FadeOut(funnel_token), FadeIn(abnormal, shift=RIGHT * 0.35), run_time=1.25)
        self.play(FadeIn(reviewer4, shift=LEFT * 0.5), run_time=1.55)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.35) for x in losses], lag_ratio=0.22), run_time=2.2)
        self.wait_until(self.ENDS[3])

        # 5 — four distinct rungs
        rungs = self.grid(["NOMINAL · CLICK", "INFORMED · EVIDENCE", "EFFECTIVE · CONTROL", "MEANINGFUL · NORMATIVE"], [MUTED, ACCENT, EVIDENCE, AUTHORITY], 1, 4.1)
        rungs.arrange(DOWN, buff=0.55).shift(LEFT * 1.0)
        rung_arrows = VGroup(*[Arrow(rungs[i].get_right(), rungs[i + 1].get_right(), color=BOUNDARY, buff=0.14) for i in range(3)])
        addenda = self.grid(["USABLE VIEW", "AUTHORITY + TIME", "SOCIAL JUDGMENT"], [ACCENT, EVIDENCE, AUTHORITY], 1, 2.7).shift(RIGHT * 4.3)
        scene5 = VGroup(rungs, rung_arrows, addenda)
        self.play_beat(5, FadeOut(scene4), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in rungs], lag_ratio=0.12), Create(rung_arrows), LaggedStart(*[FadeIn(a) for a in addenda], lag_ratio=0.15), settle=0.75)

        # 6 — telemetry cannot certify the normative state
        operational = self.grid(["CHECKLIST", "FAST", "CONFIDENT"], [EVIDENCE, ACCENT, AUTHORITY], 1, 2.4).shift(LEFT * 4.0)
        boundary = VGroup(
            Line(UP * 2.5, DOWN * 2.5, color=BOUNDARY, stroke_width=5).shift(RIGHT * 0.2),
            Line(UP * 2.5, DOWN * 2.5, color=BOUNDARY, stroke_width=2).shift(RIGHT * 0.42),
        )
        meaningful = self.badge("MEANINGFUL?", AUTHORITY, 2.5, 0.8).shift(RIGHT * 4.0)
        attempts6 = VGroup(*[Arrow(o.get_right(), meaningful.get_left(), color=o[0].get_stroke_color(), buff=0.1) for o in operational])
        stop_marks = VGroup(*[Cross(a, stroke_color=ROLLBACK, stroke_width=4) for a in attempts6])
        no_auto = self.badge("NO AUTO-CERTIFICATION", ROLLBACK, 3.2).shift(DOWN * 2.6)
        scene6 = VGroup(operational, boundary, meaningful, attempts6, stop_marks, no_auto)
        self.play_beat(6, FadeOut(scene5), AnimationGroup(FadeIn(operational), FadeIn(meaningful)), Create(attempts6), Create(boundary), LaggedStart(*[Create(x) for x in stop_marks], lag_ratio=0.12), FadeIn(no_auto), settle=0.85)

        # 7 — versioned oversight contract surrounds the episode
        episode7 = self.episode(compact=True).scale(0.82)
        contract_ring = Circle(radius=2.2, stroke_color=COPPER, stroke_width=6)
        fields7 = self.grid(["TASK", "CONSEQUENCE", "MODE", "ROLE", "AUTHORITY", "EVIDENCE", "ALTERNATIVES", "INTERVENTION", "SAFE FALLBACK", "RESPONSIBILITY", "EXPIRY"], [COPPER] * 11, 6, 1.55).scale(0.78).shift(DOWN * 2.55)
        contract_tag = self.badge("OVERSIGHT CONTRACT · V1", COPPER, 3.2).shift(UP * 2.65)
        scene7 = VGroup(contract_ring, episode7, fields7, contract_tag)
        self.next_section("b07")
        self.play(FadeOut(scene6, shift=LEFT * 0.6), Create(contract_ring), FadeIn(episode7), run_time=2.8)
        self.play(FadeIn(contract_tag, shift=DOWN * 0.3), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in fields7], lag_ratio=0.07), run_time=4.5)
        self.play(Indicate(episode7[2], color=ROLLBACK, scale_factor=1.08), run_time=2.0)
        self.play(Indicate(fields7, color=COPPER, scale_factor=1.02), run_time=1.8)
        self.wait_until(self.ENDS[6])

        # 8 — episode-only capacity snapshot
        contract8 = VGroup(contract_ring.copy(), episode7.copy()).scale(0.63).shift(LEFT * 4.4)
        snapshot = self.panel("CAPACITY SNAPSHOT · EPISODE ONLY", ACCENT, 7.4, 5.1).shift(RIGHT * 2.2)
        fields8 = self.grid(["QUALIFICATION", "EVIDENCE DIGEST", "WINDOW", "QUEUE", "CONFLICT", "ACCESS", "CHANNEL", "UNCERTAINTY", "MISSING"], [ACCENT, ACCENT, AUTHORITY, ROLLBACK, ROLLBACK, ACCENT, EVIDENCE, RESIDUAL, MUTED], 3, 2.0).move_to(snapshot)
        lineage8 = DashedLine(contract8.get_right(), snapshot.get_left(), color=BOUNDARY, stroke_width=4)
        scene8 = VGroup(contract8, snapshot, fields8, lineage8)
        self.play_beat(8, FadeOut(scene7), FadeIn(contract8), Create(lineage8), TransformFromCopy(contract8, snapshot), LaggedStart(*[FadeIn(f) for f in fields8], lag_ratio=0.08), settle=0.7)

        # 9 — task evidence may defeat role reliance, never score the person
        snapshot9 = self.badge("EPISODE SNAPSHOT", ACCENT, 2.7, 0.75).shift(LEFT * 4.6)
        defeat = self.badge("DEFEAT ROLE RELIANCE", EVIDENCE, 3.0, 0.75).shift(UP * 2.0 + RIGHT * 2.0)
        prohibited = self.grid(["RANK", "DIAGNOSE", "GRANT"], [ROLLBACK] * 3, 3, 1.8).shift(RIGHT * 2.1 + DOWN * 1.0)
        allowed = Arrow(snapshot9.get_right(), defeat.get_left(), color=EVIDENCE, buff=0.1, stroke_width=5)
        denied = VGroup(*[Arrow(snapshot9.get_right(), p.get_left(), color=ROLLBACK, buff=0.1) for p in prohibited])
        denied_cross = VGroup(*[Cross(p, stroke_color=ROLLBACK, stroke_width=4) for p in prohibited])
        task_record = self.badge("TASK RECORD · NOT PERSON SCORE", AUTHORITY, 3.6).shift(DOWN * 2.5)
        scene9 = VGroup(snapshot9, defeat, prohibited, allowed, denied, denied_cross, task_record)
        self.play_beat(9, FadeOut(scene8), FadeIn(snapshot9), FadeIn(task_record), GrowArrow(allowed), FadeIn(defeat), Create(denied), FadeIn(prohibited), Create(denied_cross), settle=0.75)

        # 10 — eight noncompensatory necessary conditions
        reviewer10 = self.reviewer().scale(0.83)
        envelope10 = self.envelope({3, 4, 5})
        necessary = self.badge("8 NECESSARY CONDITIONS", AUTHORITY, 3.0).shift(UP * 2.75)
        independent = self.badge("TEST SEPARATELY", COPPER, 2.3).shift(DOWN * 2.7)
        scan_path10 = Circle(radius=1.55, stroke_opacity=0)
        scanner10 = Dot(scan_path10.get_start(), radius=0.12, color=AUTHORITY)
        scene10 = VGroup(reviewer10, envelope10, necessary, independent, scanner10)
        self.next_section("b10")
        self.play(
            FadeOut(scene9, shift=LEFT * 0.8),
            FadeIn(reviewer10, shift=RIGHT * 1.4),
            GrowFromCenter(envelope10[0]),
            run_time=3.2,
        )
        self.add(scanner10)
        self.play(
            AnimationGroup(
                MoveAlongPath(scanner10, scan_path10),
                LaggedStart(*[Indicate(a, color=a.get_color(), scale_factor=1.08) for a in envelope10[0]], lag_ratio=0.12),
                LaggedStart(*[FadeIn(l, shift=0.15 * (l.get_center() - ORIGIN)) for l in envelope10[1]], lag_ratio=0.08),
                FadeIn(necessary, shift=DOWN * 0.4),
                FadeIn(independent, shift=UP * 0.4),
                lag_ratio=0.0,
            ),
            run_time=8.2,
        )
        self.wait_until(self.ENDS[9])

        # 11 — time adequacy is a budget
        available = Line(LEFT * 5.4, RIGHT * 5.4, color=ACCENT, stroke_width=10).shift(UP * 0.7)
        pieces = self.grid(["NOTICE", "UNDERSTAND", "DECIDE", "ACT", "RESPONSE", "MARGIN"], [MUTED, ACCENT, AUTHORITY, COPPER, EVIDENCE, ROLLBACK], 6, 1.55).scale(0.83).shift(DOWN * 1.15)
        cuts = VGroup(*[Line(UP * 0.98, DOWN * 0.02, color=BOUNDARY, stroke_width=3).shift(LEFT * 4.5 + RIGHT * i * 1.8) for i in range(6)])
        irreversible = self.badge("IRREVERSIBLE", ROLLBACK, 2.2).shift(RIGHT * 5.2 + UP * 1.7)
        scene11 = VGroup(available, pieces, cuts, irreversible)
        self.next_section("b11")
        self.play(FadeOut(scene10, shift=LEFT * 0.6), Create(available), FadeIn(irreversible), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pieces], lag_ratio=0.08), run_time=3.0)
        self.play(LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.1), run_time=1.6)
        self.play(Indicate(irreversible, color=ROLLBACK, scale_factor=1.08), run_time=1.6)
        self.wait_until(self.ENDS[10])

        # 12 — twelve seconds cannot contain a sixteen-second stop path
        bar12 = Line(LEFT * 4.5, RIGHT * 1.5, color=ACCENT, stroke_width=12).shift(UP * 0.9)
        needed12 = Line(LEFT * 4.5, RIGHT * 3.8, color=AUTHORITY, stroke_width=6).shift(DOWN * 0.25)
        values12 = self.grid(["12s AVAILABLE", "16s REQUIRED", "MARGIN −4s"], [ACCENT, AUTHORITY, ROLLBACK], 3, 2.5).shift(DOWN * 1.55)
        override = self.badge("OVERRIDE BUTTON", MUTED, 2.5).shift(RIGHT * 4.4 + UP * 1.35)
        broken = DashedLine(override.get_bottom(), RIGHT * 4.4 + DOWN * 1.1, color=ROLLBACK, stroke_width=5)
        ineffective = self.badge("≠ EFFECTIVE", ROLLBACK, 2.1).shift(RIGHT * 4.4 + DOWN * 1.55)
        scene12 = VGroup(bar12, needed12, values12, override, broken, ineffective)
        self.next_section("b12")
        self.play(FadeOut(scene11, shift=LEFT * 0.6), Create(bar12), Create(needed12), run_time=2.3)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in values12], lag_ratio=0.16), run_time=2.4)
        self.play(FadeIn(override, shift=DOWN * 0.3), run_time=1.8)
        self.play(Create(broken), FadeIn(ineffective, shift=UP * 0.25), run_time=1.8)
        self.play(Indicate(values12[2], color=ROLLBACK, scale_factor=1.1), run_time=1.2)
        self.wait_until(self.ENDS[11])

        # 13 — workload fails independently
        reviewer13 = self.reviewer().shift(LEFT * 1.5)
        envelope13 = self.envelope({3, 4, 5}).shift(LEFT * 1.5)
        queue13 = self.grid([str(i) for i in range(1, 8)], [ROLLBACK] * 7, 1, 0.72).scale(0.8).shift(RIGHT * 4.6)
        interruption = Arrow(RIGHT * 5.8 + UP * 2.3, reviewer13.get_top(), color=ROLLBACK, stroke_width=5)
        load_fail = self.badge("LOAD FAIL", ROLLBACK, 2.0).shift(DOWN * 2.7)
        scene13 = VGroup(reviewer13, envelope13, queue13, interruption, load_fail)
        self.play_beat(13, FadeOut(scene12), FadeIn(reviewer13), FadeIn(envelope13), LaggedStart(*[FadeIn(q, shift=LEFT * 0.15) for q in queue13], lag_ratio=0.08), GrowArrow(interruption), Indicate(envelope13[0][4], color=ROLLBACK), FadeIn(load_fail), settle=0.7)

        # 14 — fluent representation and formal authority are separate failures
        fluent = self.panel("FLUENT RECOMMENDATION", ACCENT, 4.6, 3.3).shift(LEFT * 3.6)
        conflict14 = self.badge("CONFLICTING EVIDENCE", ROLLBACK, 3.1).move_to(fluent).shift(DOWN * 0.45)
        lock14 = self.panel("CONTROL KEYS", AUTHORITY, 5.5, 4.2).shift(RIGHT * 3.2)
        keys14 = self.grid(["VETO", "REDIRECT", "APPEAL", "SAFE STATE"], [ROLLBACK] * 4, 2, 2.0).move_to(lock14)
        crosses14 = VGroup(*[Cross(k, stroke_color=ROLLBACK, stroke_width=4) for k in keys14])
        no_blame = self.badge("NO BLAME TRANSFER", ROLLBACK, 2.8).shift(DOWN * 2.65)
        scene14 = VGroup(fluent, conflict14, lock14, keys14, crosses14, no_blame)
        self.next_section("b14")
        self.play(FadeOut(scene13, shift=LEFT * 0.7), FadeIn(fluent, shift=RIGHT * 0.8), FadeIn(lock14, shift=LEFT * 0.8), run_time=2.0)
        self.play(FadeIn(conflict14, shift=UP * 0.65), run_time=1.5)
        self.play(Indicate(conflict14, color=ROLLBACK, scale_factor=1.12), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.35) for k in keys14], lag_ratio=0.20), run_time=3.6)
        self.play(LaggedStart(*[Create(x) for x in crosses14], lag_ratio=0.16), FadeIn(no_blame, shift=UP * 0.4), run_time=3.3)
        self.wait_until(self.ENDS[13])

        # 15 — fail-closed routes retain useful alternatives
        failed15 = self.envelope({3, 4, 5}).scale(0.85).shift(LEFT * 4.6)
        remedies = self.grid(["CLARIFY", "ADD CAPACITY", "SLOW", "REDUCE AUTONOMY", "SAFE HOLD", "ABSTAIN + ESCALATE"], [ACCENT, ACCENT, AUTHORITY, COPPER, EVIDENCE, ROLLBACK], 2, 2.6).shift(RIGHT * 2.7)
        routes15 = VGroup(*[Arrow(failed15.get_right(), r.get_left(), color=r[0].get_stroke_color(), buff=0.08) for r in remedies])
        episode_token15 = Dot(failed15.get_center(), radius=0.16, color=ACCENT)
        hold_path15 = routes15[4]
        scene15 = VGroup(failed15, remedies, routes15, episode_token15)
        self.play_beat(15, FadeOut(scene14), FadeIn(failed15), Create(routes15), LaggedStart(*[FadeIn(r) for r in remedies], lag_ratio=0.08), FadeIn(episode_token15), MoveAlongPath(episode_token15, hold_path15), Indicate(remedies[4], color=EVIDENCE), settle=0.75)

        # 16 — build the first half of the credible static baseline
        rail16 = Line(LEFT * 5.8, RIGHT * 5.8, color=BOUNDARY, stroke_width=7)
        safeguards16 = self.grid(["RISK TIER", "LEAD TIME", "MODE + CONSEQUENCE", "INDEPENDENT VIEW"], [ACCENT, AUTHORITY, COPPER, EVIDENCE], 4, 2.5).scale(0.84).shift(UP * 1.25)
        ticks16 = VGroup(*[Line(UP * 0.25, DOWN * 0.25, color=s[0].get_stroke_color(), stroke_width=6).move_to(rail16.point_from_proportion((i + 1) / 8)) for i, s in enumerate(safeguards16)])
        baseline_tag = self.badge("CREDIBLE STATIC BASELINE", MUTED, 3.2).shift(DOWN * 1.5)
        scene16 = VGroup(rail16, safeguards16, ticks16, baseline_tag)
        self.next_section("b16")
        self.play(FadeOut(scene15, shift=LEFT * 0.6), Create(rail16), run_time=2.1)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in safeguards16], lag_ratio=0.1), run_time=2.1)
        self.play(LaggedStart(*[Create(t) for t in ticks16], lag_ratio=0.1), run_time=1.4)
        self.play(FadeIn(baseline_tag, shift=UP * 0.25), run_time=1.1)
        self.wait_until(self.ENDS[15])

        # 17 — complete baseline and carry episode to safe hold
        final16 = self.grid(["TESTED STOP", "DUAL REVIEW", "QUEUE LIMIT"], [EVIDENCE, AUTHORITY, ROLLBACK], 3, 2.35).scale(0.84).shift(UP * 1.25 + RIGHT * 2.8)
        ticks17 = VGroup(*[Line(UP * 0.25, DOWN * 0.25, color=s[0].get_stroke_color(), stroke_width=6).move_to(rail16.point_from_proportion(0.62 + i * 0.13)) for i, s in enumerate(final16)])
        token17 = Dot(rail16.get_start(), radius=0.15, color=ACCENT)
        basin17 = self.basin().scale(0.76).shift(RIGHT * 5.0 + DOWN * 1.7)
        path17 = Line(rail16.get_start(), rail16.get_end(), color=BOUNDARY)
        scene17 = VGroup(rail16, safeguards16, ticks16, final16, ticks17, token17, basin17, baseline_tag)
        self.play_beat(17, LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in final16], lag_ratio=0.12), Create(ticks17), FadeIn(token17), MoveAlongPath(token17, path17), FadeIn(basin17), Indicate(basin17, color=EVIDENCE), settle=0.35)

        # 18 — adaptive design earns complexity only across joint outcomes
        baseline18 = VGroup(rail16.copy(), baseline_tag.copy()).scale(0.75).shift(UP * 1.55)
        adaptive18 = VGroup(self.envelope({3, 4, 5}).scale(0.46), self.badge("ADAPTIVE", COPPER, 1.8)).arrange(RIGHT, buff=0.3).shift(LEFT * 3.7 + DOWN * 1.45)
        outcomes18 = self.grid(["FALSE STOP", "DELAY", "UNEQUAL BURDEN", "PRIVACY", "MISSED HELP", "USEFUL WORK"], [ROLLBACK, AUTHORITY, RESIDUAL, COPPER, ROLLBACK, EVIDENCE], 3, 2.05).shift(RIGHT * 2.8)
        no_winner18 = self.badge("NO SINGLE WINNER", ROLLBACK, 2.6).shift(DOWN * 2.75)
        scene18 = VGroup(baseline18, adaptive18, outcomes18, no_winner18)
        self.next_section("b18")
        self.play(FadeOut(scene17, shift=LEFT * 0.6), FadeIn(baseline18), FadeIn(adaptive18), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in outcomes18], lag_ratio=0.1), run_time=3.2)
        self.play(FadeIn(no_winner18, shift=UP * 0.25), run_time=1.6)
        self.play(Indicate(outcomes18, color=AUTHORITY, scale_factor=1.03), run_time=3.0)
        self.wait_until(self.ENDS[17])

        # 19 — repair the episode with a compatible frozen evidence view
        staged19 = self.episode(compact=True).shift(LEFT * 4.4)
        mode19 = self.badge("MODE · WAITING", AUTHORITY, 2.2).shift(UP * 1.8)
        alternatives19 = self.grid(["TRANSFER", "SAFE HOLD"], [ROLLBACK, EVIDENCE], 2, 2.1).shift(RIGHT * 2.6)
        last19 = self.badge("LAST REVERSIBLE POINT", COPPER, 3.0).shift(DOWN * 1.9)
        relation19 = VGroup(
            Arrow(staged19.get_right(), mode19.get_left(), color=AUTHORITY, buff=0.1),
            Arrow(staged19.get_right(), alternatives19.get_left(), color=ACCENT, buff=0.1),
            Arrow(alternatives19.get_bottom(), last19.get_top(), color=COPPER, buff=0.1),
        )
        frozen19 = self.badge("EVIDENCE VIEW · FROZEN", ACCENT, 2.9).shift(LEFT * 3.7 + DOWN * 2.45)
        scene19 = VGroup(staged19, mode19, alternatives19, last19, relation19, frozen19)
        self.next_section("b19")
        self.play(FadeOut(scene18, shift=LEFT * 0.6), FadeIn(staged19), FadeIn(frozen19), run_time=2.6)
        self.play(Create(relation19), run_time=2.2)
        self.play(FadeIn(mode19), FadeIn(alternatives19), run_time=2.2)
        self.play(FadeIn(last19, shift=UP * 0.25), run_time=1.8)
        self.play(Indicate(staged19[2], color=ROLLBACK, scale_factor=1.08), run_time=1.8)
        self.wait_until(self.ENDS[18])

        # 20 — one task-relevant comprehension opportunity
        pressure20 = self.badge("PRESSURE CONFLICT", ROLLBACK, 2.6).shift(LEFT * 4.2 + UP * 1.2)
        question20 = self.panel("TASK CHECK", AUTHORITY, 5.1, 3.5)
        transfer20 = self.badge("TRANSFER", ROLLBACK, 1.9).shift(RIGHT * 4.5 + UP * 1.2)
        hold20 = self.basin().scale(0.72).shift(RIGHT * 4.5 + DOWN * 1.3)
        paths20 = VGroup(
            Arrow(pressure20.get_right(), transfer20.get_left(), color=ROLLBACK, buff=0.1),
            Arrow(pressure20.get_right(), hold20.get_left(), color=EVIDENCE, buff=0.1),
        )
        reviewer20 = self.reviewer().scale(0.66).move_to(question20)
        scene20 = VGroup(pressure20, question20, transfer20, hold20, paths20, reviewer20)
        self.next_section("b20")
        self.play(FadeOut(scene19, shift=LEFT * 0.6), FadeIn(pressure20), FadeIn(question20), run_time=2.4)
        self.play(FadeIn(reviewer20), run_time=1.2)
        self.play(Create(paths20), run_time=1.8)
        self.play(FadeIn(transfer20), FadeIn(hold20), run_time=1.7)
        self.play(Indicate(pressure20, color=ROLLBACK), Indicate(hold20, color=EVIDENCE), run_time=1.8)
        self.wait_until(self.ENDS[19])

        # 21 — exercise the full intervention chain
        choice21 = self.badge("SELECT HOLD", AUTHORITY, 2.1).shift(LEFT * 5.0)
        channel21 = Line(LEFT * 3.7, RIGHT * 2.2, color=EVIDENCE, stroke_width=8)
        channel_tag21 = self.badge("CHANNEL · WITHIN LATENCY", EVIDENCE, 3.0).shift(UP * 1.15)
        hold21 = self.basin().shift(RIGHT * 4.2)
        token21 = Dot(channel21.get_start(), radius=0.16, color=AUTHORITY)
        witness21 = self.badge("INDEPENDENT · NOT COMMITTED", ACCENT, 3.6).shift(DOWN * 1.85)
        scene21 = VGroup(choice21, channel21, channel_tag21, hold21, token21, witness21)
        self.next_section("b21")
        self.play(FadeOut(scene20, shift=LEFT * 0.6), FadeIn(choice21), Create(channel21), run_time=2.4)
        self.play(FadeIn(channel_tag21, shift=DOWN * 0.25), FadeIn(token21), run_time=1.4)
        self.play(MoveAlongPath(token21, channel21), run_time=3.2)
        self.play(FadeIn(hold21, shift=LEFT * 0.35), Indicate(hold21, color=EVIDENCE), run_time=1.6)
        self.play(FadeIn(witness21, shift=UP * 0.25), run_time=1.5)
        self.wait_until(self.ENDS[20])

        # 22 — provenance-linked intervention receipt
        receipt22 = self.panel("INTERVENTION RECEIPT", COPPER, 11.3, 5.1)
        fields22 = self.grid(["VIEW", "TIMING", "CHOICE", "REQUEST", "RESPONSE", "RESIDUAL", "OWNER"], [ACCENT, AUTHORITY, AUTHORITY, COPPER, EVIDENCE, RESIDUAL, COPPER], 4, 2.25).move_to(receipt22)
        source22 = VGroup(choice21.copy(), channel_tag21.copy(), witness21.copy()).scale(0.66).shift(UP * 2.6)
        links22 = VGroup(*[DashedLine(source22.get_bottom(), f.get_top(), color=BOUNDARY, stroke_width=2.5) for f in fields22])
        scene22 = VGroup(receipt22, fields22, source22, links22)
        self.next_section("b22")
        self.play(FadeOut(scene21, shift=LEFT * 0.6), FadeIn(receipt22), FadeIn(source22), run_time=2.4)
        self.play(Create(links22), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.15) for f in fields22], lag_ratio=0.09), run_time=3.6)
        self.play(Indicate(source22, color=ACCENT, scale_factor=1.03), run_time=1.3)
        self.wait_until(self.ENDS[21])

        # 23 — responsibility cannot outrun recorded control
        receipt23 = receipt22.copy().scale(0.64).shift(UP * 0.8)
        responsibility23 = self.badge("RESPONSIBILITY", AUTHORITY, 3.0, 0.8).shift(LEFT * 4.5 + UP * 2.3)
        ceiling23 = Line(UP * 2.6, DOWN * 2.2, color=COPPER, stroke_width=7).shift(RIGHT * 1.2)
        residuals23 = self.grid(["MISSING EVIDENCE", "IMPOSSIBLE TIME", "PRESSURE", "FAILED STOP", "DISAGREEMENT", "NO ALTERNATIVE"], [ROLLBACK] * 6, 3, 2.3).shift(DOWN * 1.7)
        push23 = Arrow(responsibility23.get_right(), RIGHT * 4.5 + UP * 2.3, color=AUTHORITY, stroke_width=6)
        scene23 = VGroup(receipt23, responsibility23, ceiling23, residuals23, push23)
        self.next_section("b23")
        self.play(FadeOut(scene22, shift=LEFT * 0.6), FadeIn(receipt23), FadeIn(responsibility23), run_time=2.5)
        self.play(GrowArrow(push23), Create(ceiling23), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in residuals23], lag_ratio=0.09), run_time=3.2)
        self.play(Transform(responsibility23, responsibility23.copy().scale(0.72).shift(LEFT * 0.8)), run_time=2.1)
        self.wait_until(self.ENDS[22])

        # 24 — privacy-minimized task signals, blocked surveillance
        reviewer24 = self.reviewer().shift(LEFT * 5.0)
        privacy24 = VGroup(
            Line(UP * 2.6, DOWN * 2.6, color=AUTHORITY, stroke_width=6).shift(LEFT * 1.8),
            self.badge("PRIVACY MINIMUM", AUTHORITY, 2.4).shift(LEFT * 1.8 + UP * 2.7),
        )
        allowed24 = self.grid(["TASK STATE", "SYSTEM STATE", "VOLUNTARY"], [ACCENT, EVIDENCE, AUTHORITY], 1, 2.2).shift(LEFT * 3.2)
        blocked24 = self.grid(["CAMERA", "EMOTION", "KEYSTROKES", "HIDDEN PROFILE"], [ROLLBACK] * 4, 2, 2.1).shift(RIGHT * 3.1)
        crosses24 = VGroup(*[Cross(b, stroke_color=ROLLBACK, stroke_width=4) for b in blocked24])
        scene24 = VGroup(reviewer24, privacy24, allowed24, blocked24, crosses24)
        self.next_section("b24")
        self.play(FadeOut(scene23, shift=LEFT * 0.6), FadeIn(reviewer24), FadeIn(privacy24), run_time=2.6)
        self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in allowed24], lag_ratio=0.12), run_time=2.5)
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.2) for b in blocked24], lag_ratio=0.1), run_time=2.5)
        self.play(LaggedStart(*[Create(x) for x in crosses24], lag_ratio=0.1), run_time=1.7)
        self.wait_until(self.ENDS[23])

        # 25 — any material change expires admission
        accepted25 = VGroup(self.envelope().scale(0.72), self.badge("ADMITTED · V1", EVIDENCE, 2.1).shift(DOWN * 2.1))
        triggers25 = self.grid(["TASK", "MODEL", "INTERFACE", "EVIDENCE", "CONSEQUENCE", "AUTHORITY", "ROLE", "WINDOW", "INTERVENTION"], [COPPER] * 9, 3, 1.7).shift(RIGHT * 4.1)
        trigger25 = triggers25[2]
        expiry25 = self.badge("EXPIRED", ROLLBACK, 2.0, 0.75).shift(LEFT * 4.5 + DOWN * 2.3)
        return25 = ArcBetweenPoints(accepted25.get_bottom(), triggers25.get_bottom(), angle=-1.0, color=COPPER, stroke_width=5)
        return_token25 = Dot(return25.get_start(), radius=0.14, color=COPPER)
        scene25 = VGroup(accepted25, triggers25, expiry25, return25, return_token25)
        self.next_section("b25")
        self.play(FadeOut(scene24, shift=LEFT * 0.7), FadeIn(accepted25, shift=RIGHT * 1.2), run_time=2.0)
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.45) for t in triggers25], lag_ratio=0.08), run_time=3.0)
        self.play(
            Indicate(trigger25, color=ROLLBACK, scale_factor=1.18),
            Transform(accepted25[0], self.envelope({0, 1, 2, 3, 4, 5, 6, 7}).scale(0.72)),
            FadeIn(expiry25, shift=UP * 0.4),
            Create(return25),
            run_time=2.0,
        )
        self.add(return_token25)
        self.play(MoveAlongPath(return_token25, return25), run_time=3.2)
        self.wait_until(self.ENDS[24])

        # 26 — evaluation begins with independent error and reliance axes
        hub26 = self.badge("CONTROL EVALUATION", COPPER, 2.7, 0.75)
        values26 = ["DETECT", "CORRECT STOP", "FALSE STOP", "MISSED DEFECT", "CALIBRATION"]
        spokes26 = VGroup()
        labels26 = VGroup()
        for i, value in enumerate(values26):
            angle = PI * (0.1 + 0.2 * i)
            endpoint = 3.1 * (RIGHT * cos(angle) + UP * sin(angle))
            spokes26.add(Line(hub26.get_center(), endpoint, color=[ACCENT, EVIDENCE, ROLLBACK, ROLLBACK, AUTHORITY][i], stroke_width=4))
            labels26.add(self.badge(value, [ACCENT, EVIDENCE, ROLLBACK, ROLLBACK, AUTHORITY][i], 2.0).move_to(endpoint))
        one_score26 = self.badge("ONE SCORE", MUTED, 2.0).shift(DOWN * 2.35)
        score_cross26 = Cross(one_score26, stroke_color=ROLLBACK, stroke_width=5)
        scene26 = VGroup(hub26, spokes26, labels26, one_score26, score_cross26)
        self.play_beat(26, FadeOut(scene25), AnimationGroup(FadeIn(hub26), FadeIn(one_score26), Create(score_cross26)), LaggedStart(*[Create(s) for s in spokes26], lag_ratio=0.1), LaggedStart(*[FadeIn(l) for l in labels26], lag_ratio=0.1), settle=0.4)

        # 27 — usefulness and harms complete the nonaggregate wheel
        lower_values27 = ["USEFUL", "BURDEN", "PRIVACY", "UNEQUAL IMPACT", "LATENCY", "RECOVERY"]
        lower_colors27 = [EVIDENCE, AUTHORITY, COPPER, RESIDUAL, ACCENT, EVIDENCE]
        spokes27 = VGroup()
        labels27 = VGroup()
        for i, value in enumerate(lower_values27):
            angle = PI * (1.08 + 0.168 * i)
            endpoint = 3.1 * (RIGHT * cos(angle) + UP * sin(angle))
            spokes27.add(Line(hub26.get_center(), endpoint, color=lower_colors27[i], stroke_width=4))
            labels27.add(self.badge(value, lower_colors27[i], 2.0).move_to(endpoint))
        remain27 = self.badge("ALL REMAIN VISIBLE", AUTHORITY, 2.8).shift(DOWN * 2.85)
        scene27 = VGroup(hub26, spokes26, labels26, spokes27, labels27, remain27)
        self.play_beat(27, FadeOut(one_score26), FadeOut(score_cross26), LaggedStart(*[Create(s) for s in spokes27], lag_ratio=0.09), LaggedStart(*[FadeIn(l) for l in labels27], lag_ratio=0.09), FadeIn(remain27), Indicate(VGroup(spokes26, spokes27), color=AUTHORITY), settle=0.35)

        # 28 — exact evidence ceiling
        artifacts28 = self.grid(["SCHEMA", "FIXTURE", "MUTATIONS", "FINITE MODEL"], [EVIDENCE] * 4, 2, 2.3).shift(LEFT * 3.7)
        rule28 = VGroup(
            Line(UP * 2.8, DOWN * 2.8, color=BOUNDARY, stroke_width=6).shift(RIGHT * 0.05),
            Line(UP * 2.8, DOWN * 2.8, color=BOUNDARY, stroke_width=2).shift(RIGHT * 0.28),
        )
        nonclaims28 = self.grid(["≠ COMPREHENSION", "≠ THRESHOLD", "≠ EFFICACY", "≠ RESPONSIBILITY", "≠ DEPLOYMENT", "≠ SAFETY", "≠ TRANSFER"], [ROLLBACK] * 7, 2, 2.35).scale(0.9).shift(RIGHT * 3.5)
        finite28 = self.badge("FINITE ROUTING ONLY", EVIDENCE, 2.7).shift(LEFT * 3.7 + UP * 2.5)
        scene28 = VGroup(artifacts28, rule28, nonclaims28, finite28)
        self.play_beat(28, FadeOut(scene27), FadeIn(finite28), LaggedStart(*[FadeIn(a) for a in artifacts28], lag_ratio=0.1), Create(rule28), LaggedStart(*[FadeIn(n, shift=LEFT * 0.15) for n in nonclaims28], lag_ratio=0.08), settle=0.95)

        # 29 — opening payoff: safe hold for task reasons, no person score
        episode29 = self.episode(compact=True).shift(LEFT * 4.5)
        reviewer29 = self.reviewer().scale(0.76)
        envelope29 = self.envelope({3, 4, 5}).scale(0.72)
        basin29 = self.basin().shift(RIGHT * 4.7)
        route29 = Arrow(episode29.get_right(), basin29.get_left(), color=EVIDENCE, stroke_width=6, buff=0.12)
        token29 = Dot(route29.get_start(), radius=0.16, color=ACCENT)
        no_score29 = self.badge("NO PERSON SCORE", AUTHORITY, 2.5).shift(DOWN * 2.55)
        why29 = self.badge("KNOWN ENVELOPE FAILED", ROLLBACK, 3.1).shift(UP * 2.55)
        scene29 = VGroup(episode29, reviewer29, envelope29, basin29, route29, token29, no_score29, why29)
        self.next_section("b29")
        self.play(
            FadeOut(scene28, shift=LEFT * 0.7),
            FadeIn(episode29, shift=RIGHT * 0.8),
            FadeIn(reviewer29, shift=UP * 0.45),
            FadeIn(envelope29),
            run_time=3.0,
        )
        self.play(FadeIn(why29, shift=DOWN * 0.45), GrowArrow(route29), FadeIn(basin29), run_time=2.5)
        self.add(token29)
        self.play(MoveAlongPath(token29, route29), run_time=4.0)
        self.play(FadeIn(no_score29, shift=UP * 0.45), Indicate(basin29, color=EVIDENCE, scale_factor=1.08), run_time=3.5)
        self.wait_until(self.ENDS[28])

        # 30 — hand bounded capacity and vulnerability to epistemic security
        episode30 = self.episode(compact=True).scale(0.58).shift(LEFT * 5.25 + UP * 0.8)
        envelope30 = self.envelope({3, 4, 5}).scale(0.38).shift(LEFT * 3.2 + UP * 0.8)
        hold30 = self.basin().scale(0.5).shift(LEFT * 3.2 + DOWN * 1.25)
        safe_route30 = Arrow(episode30.get_right(), hold30.get_left(), color=EVIDENCE, stroke_width=5, buff=0.08)
        resolved30 = VGroup(episode30, envelope30, hold30, safe_route30)
        receipt30 = self.badge("CAPACITY + VULNERABILITY", COPPER, 3.2, 0.75).shift(LEFT * 0.55)
        channel30 = ArcBetweenPoints(RIGHT * 1.15, RIGHT * 4.45, angle=-0.55, color=ACCENT, stroke_width=6)
        distortions30 = self.grid(["FRAMING", "PERSONALIZATION", "URGENCY", "REPETITION", "SYNTHETIC IDENTITY"], [RESIDUAL] * 5, 1, 2.55).scale(0.86).shift(RIGHT * 5.25)
        token30 = Dot(channel30.get_start(), radius=0.16, color=COPPER)
        next30 = self.badge("NEXT · EPISTEMIC SECURITY", ACCENT, 3.4).shift(UP * 2.65 + RIGHT * 2.5)
        scene30 = VGroup(resolved30, receipt30, channel30, distortions30, token30, next30)
        self.next_section("b30")
        self.play(FadeOut(scene29, shift=LEFT * 0.8), FadeIn(resolved30, shift=RIGHT * 0.8), run_time=2.5)
        self.play(TransformFromCopy(resolved30, receipt30), run_time=2.5)
        self.play(Create(channel30), FadeIn(token30), run_time=1.5)
        self.play(
            MoveAlongPath(token30, channel30),
            LaggedStart(*[FadeIn(d, shift=LEFT * 0.55) for d in distortions30], lag_ratio=0.12),
            run_time=6.0,
        )
        self.play(FadeIn(next30, shift=DOWN * 0.45), run_time=2.0)
        self.wait_until(self.ENDS[29])

        self.wait_until(self.TARGET_DURATION)
