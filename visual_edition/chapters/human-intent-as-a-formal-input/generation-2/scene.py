"""Generation-2 visual abstract for Human Intent as a Formal Input.

One launch request moves through a persistent intent workbench. Hidden
assumptions become inspectable fields, bounded defaults enable reversible help,
and versioned contracts keep publication authority behind an explicit gate.
"""

from __future__ import annotations

from math import cos, sin

from manim import (
    ArcBetweenPoints, Arrow, Circle, Create, Cross, DashedLine,
    Dot, FadeIn, FadeOut, GrowArrow, GrowFromCenter, Indicate, LaggedStart,
    LEFT, Line, MoveAlongPath, Polygon, RIGHT, RoundedRectangle, Succession, Text, TransformFromCopy,
    UP, VGroup, Write,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


class HumanIntentGeneration2(AsiScene):
    TARGET_DURATION = 281.345
    ENDS = [
        9.455, 20.610, 27.290, 36.445, 45.250, 55.030, 66.060,
        74.715, 83.595, 92.700, 104.055, 113.510, 121.740, 134.445,
        143.725, 153.330, 165.660, 176.015, 184.270, 194.750,
        204.530, 214.635, 228.215, 241.920, 259.600, 274.445, 281.345,
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
            self.play(
                LaggedStart(*animations, lag_ratio=0.12),
                run_time=max(0.05, remaining - min(settle, remaining * 0.2)),
            )
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 18, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 2.1, height: float = 0.55) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=color, stroke_width=2.6,
            fill_color=SURFACE, fill_opacity=1,
        )
        return VGroup(shell, self.label(value, 13, color, "BOLD").move_to(shell))

    def panel(self, title: str, color: str, width: float, height: float) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.16,
            stroke_color=color, stroke_width=3.2,
            fill_color="#172A34", fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.25, 3.5), 0.48).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def grid(self, values: list[str], colors: list[str], columns: int, width: float = 2.0) -> VGroup:
        items = VGroup(*[self.badge(v, colors[i], width, 0.5) for i, v in enumerate(values)])
        rows = (len(values) + columns - 1) // columns
        items.arrange_in_grid(rows=rows, cols=columns, buff=(0.18, 0.2))
        return items

    def gate(self, title: str = "AUTHORITY GATE", color: str = AUTHORITY) -> VGroup:
        posts = VGroup(
            Line(UP * 2.3, UP * -2.3, color=color, stroke_width=8).shift(LEFT * 0.42),
            Line(UP * 2.3, UP * -2.3, color=color, stroke_width=8).shift(RIGHT * 0.42),
            Line(LEFT * 0.46, RIGHT * 0.46, color=color, stroke_width=8).shift(UP * 2.28),
        )
        tag = self.badge(title, color, 2.5).next_to(posts, UP, buff=0.15)
        return VGroup(posts, tag)

    def request(self, compact: bool = False) -> VGroup:
        width = 6.1 if not compact else 4.2
        shell = RoundedRectangle(
            width=width, height=1.35 if not compact else 1.05,
            corner_radius=0.18, stroke_color=ACCENT, stroke_width=4,
            fill_color="#17313A", fill_opacity=1,
        )
        wording = self.label(
            "PRIVATE NOTES  ·  AMAZING LAUNCH  ·  PUBLISH TODAY",
            16 if not compact else 13, ACCENT, "BOLD",
        ).move_to(shell)
        return VGroup(shell, wording)

    def contract(self, version: str, color: str = COPPER, width: float = 4.1, height: float = 3.2) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.17,
            stroke_color=color, stroke_width=4,
            fill_color="#172A34", fill_opacity=1,
        )
        title = self.badge(f"CONTRACT {version}", color, 2.2).next_to(shell, UP, buff=-0.18)
        return VGroup(shell, title)

    def construct(self) -> None:
        # 1 — the fluent request races toward publication
        request = self.request().shift(LEFT * 3.6)
        publish = self.badge("PUBLISH", ROLLBACK, 2.35, 0.82).shift(RIGHT * 5.25)
        route = Arrow(request.get_right(), publish.get_left(), color=ACCENT, buff=0.12, stroke_width=5)
        traveler = Dot(route.get_start(), radius=0.13, color=ACCENT)
        hook = VGroup(request, publish, route, traveler)
        self.next_section("b01")
        self.play(Create(request[0]), Write(request[1]), run_time=2.75)
        self.wait_until(2.894)
        self.play(GrowArrow(route), GrowFromCenter(publish), run_time=2.7)
        self.wait_until(5.727)
        self.add(traveler)
        self.play(MoveAlongPath(traveler, route), Indicate(publish, color=ROLLBACK, scale_factor=1.05), run_time=3.05)
        self.wait_until(self.ENDS[0])

        # 2 — five ungranted powers hitch a ride
        assumptions = self.grid(
            ["AUDIENCE", "SPEND", "PRIVATE SOURCE", "CONTACT", "PUBLISH"],
            [ROLLBACK] * 5, 5, 2.0,
        ).scale(0.86).shift(LEFT * 1.3 + UP * -2.0)
        tethers = VGroup(*[
            DashedLine(request.get_bottom(), a.get_top(), color=ROLLBACK, stroke_width=2.5)
            for a in assumptions
        ])
        scene2 = VGroup(hook, assumptions, tethers)
        self.next_section("b02")
        self.play(Create(tethers[:2]), FadeIn(assumptions[:2], shift=UP * 0.25), run_time=4.05)
        self.wait_until(13.815)
        self.play(Create(tethers[2:4]), FadeIn(assumptions[2:4], shift=UP * 0.25), run_time=3.3)
        self.wait_until(17.334)
        self.play(Create(tethers[4]), FadeIn(assumptions[4], shift=UP * 0.25), Indicate(publish, color=ROLLBACK, scale_factor=1.08), run_time=2.7)
        self.wait_until(self.ENDS[1])

        # 3 — prediction fork
        fork_origin = Dot(LEFT * 4.6, radius=0.12, color=ACCENT)
        choices = self.grid(["ACT", "REFUSE", "ASK ALL"], [EVIDENCE, ROLLBACK, AUTHORITY], 1, 2.2).shift(RIGHT * 2.8)
        forks = VGroup(*[Arrow(fork_origin, c.get_left(), color=[EVIDENCE, ROLLBACK, AUTHORITY][i], buff=0.1) for i, c in enumerate(choices)])
        frozen = self.request(compact=True).shift(LEFT * 4.2)
        scene3 = VGroup(frozen, fork_origin, choices, forks)
        self.play_beat(3, FadeOut(scene2), FadeIn(frozen), FadeIn(fork_origin), Create(forks), FadeIn(choices), settle=1.35)

        # 4 — outcome and authority become separate rails
        outcome_rail = Line(LEFT * 5.6, RIGHT * 5.6, color=ACCENT, stroke_width=7).shift(UP * 1.25)
        authority_rail = Line(LEFT * 5.6, RIGHT * 5.6, color=AUTHORITY, stroke_width=7).shift(UP * -1.25)
        outcome_tag = self.badge("DESIRED OUTCOME", ACCENT, 2.6).shift(LEFT * 4.4 + UP * 1.75)
        authority_tag = self.badge("AUTHORITY", AUTHORITY, 2.1).shift(LEFT * 4.65 + UP * -0.75)
        request_token = self.badge("LAUNCH CANDIDATE", ACCENT, 2.5).shift(LEFT * 1.5 + UP * 1.25)
        power_tokens = self.grid(["SPEND", "PUBLISH", "CONTACT"], [ROLLBACK] * 3, 3, 1.55).shift(LEFT * 0.4 + UP * -1.25)
        fixed_gate = self.gate().scale(0.82).shift(RIGHT * 4.4)
        not_same = self.badge("NOT THE SAME", ROLLBACK, 2.3).shift(UP * -2.65)
        scene4 = VGroup(outcome_rail, authority_rail, outcome_tag, authority_tag, request_token, power_tokens, fixed_gate, not_same)
        self.play_beat(4, FadeOut(scene3), Create(outcome_rail), Create(authority_rail), FadeIn(outcome_tag), FadeIn(authority_tag), FadeIn(request_token), FadeIn(power_tokens), FadeIn(fixed_gate), FadeIn(not_same), settle=0.7)

        # 5 — preserve raw request and derive a working copy
        source = self.panel("RAW REQUEST · PRESERVED", ACCENT, 4.7, 2.4).shift(LEFT * 4.1)
        source_request = self.request(compact=True).scale(0.82).move_to(source)
        working = self.badge("INTERPRETATION COPY", COPPER, 2.8, 0.72).shift(RIGHT * 3.8)
        lineage = DashedLine(source.get_right(), working.get_left(), color=BOUNDARY, stroke_width=3)
        scene5 = VGroup(source, source_request, working, lineage)
        self.play_beat(5, FadeOut(scene4), FadeIn(source), FadeIn(source_request), TransformFromCopy(source_request, working), Create(lineage), settle=0.65)

        # 6 — the intent prism separates fields
        prism = Polygon(UP * 1.6, LEFT * 1.4 + UP * -1.4, RIGHT * 1.4 + UP * -1.4, stroke_color=COPPER, stroke_width=4, fill_color="#213640", fill_opacity=1)
        prism.shift(LEFT * 3.6)
        prism_tag = self.label("INTENT\nPRISM", 17, COPPER, "BOLD").move_to(prism)
        fields = self.grid(["OUTCOME", "ALLOWED", "FORBIDDEN", "SOURCES", "AFFECTED", "EVIDENCE", "STOP"], [ACCENT, EVIDENCE, ROLLBACK, AUTHORITY, COPPER, EVIDENCE, ROLLBACK], 2, 2.05).shift(RIGHT * 3.1)
        rays = VGroup(*[Arrow(prism.get_right(), f.get_left(), color=f[0].get_stroke_color(), buff=0.08, stroke_width=2.5) for f in fields])
        scene6 = VGroup(prism, prism_tag, fields, rays)
        self.play_beat(6, FadeOut(scene5), GrowFromCenter(prism), FadeIn(prism_tag), Create(rays), LaggedStart(*[FadeIn(f) for f in fields], lag_ratio=0.09), settle=0.75)

        # 7 — every field receives a disposition
        contract_frame = self.panel("FIELD DISPOSITIONS", COPPER, 11.0, 5.4)
        field_names = self.grid(["OUTCOME", "MEANS", "SOURCES", "AFFECTED", "EVIDENCE", "STOP", "PUBLICATION"], [ACCENT] * 7, 1, 2.0).shift(LEFT * 3.3)
        dispositions = self.grid(["CONFIRMED", "BOUNDED DEFAULT", "CLARIFY", "AUTHORITY PENDING", "CONTESTED", "UNKNOWN", "UNAUTHORIZED"], [EVIDENCE, AUTHORITY, COPPER, AUTHORITY, RESIDUAL, MUTED, ROLLBACK], 1, 2.55).shift(RIGHT * 3.0)
        links = VGroup(*[Arrow(field_names[i].get_right(), dispositions[i].get_left(), color=BOUNDARY, buff=0.08) for i in range(7)])
        scene7 = VGroup(contract_frame, field_names, dispositions, links)
        self.play_beat(7, FadeOut(scene6), FadeIn(contract_frame), FadeIn(field_names), Create(links), LaggedStart(*[FadeIn(d) for d in dispositions], lag_ratio=0.08), settle=0.75)

        # 8 — bounded defaults create reversible drafts
        bounded = self.badge("BOUNDED DEFAULT", AUTHORITY, 2.7, 0.7).shift(LEFT * 5.0)
        private_box = self.panel("PRIVATE · REVERSIBLE", EVIDENCE, 8.4, 4.4).shift(RIGHT * 1.6)
        drafts = self.grid(["DRAFT A", "DRAFT B", "DRAFT C"], [EVIDENCE] * 3, 3, 2.1).move_to(private_box)
        assumption_tags = VGroup(*[self.badge("ASSUMPTION", MUTED, 1.55, 0.38).scale(0.75).next_to(d, UP, buff=0.12) for d in drafts])
        default_paths = VGroup(*[Arrow(bounded.get_right(), d.get_left(), color=EVIDENCE, buff=0.08) for d in drafts])
        rollback_mark = self.badge("ROLLBACK", ROLLBACK, 1.8).shift(RIGHT * 4.8 + UP * -2.55)
        scene8 = VGroup(bounded, private_box, drafts, assumption_tags, default_paths, rollback_mark)
        self.play_beat(8, FadeOut(scene7), FadeIn(bounded), FadeIn(private_box), Create(default_paths), FadeIn(drafts), FadeIn(assumption_tags), FadeIn(rollback_mark), settle=0.7)

        # 9 — the same default fails at external-effect sockets
        default_token = self.badge("DEFAULT", AUTHORITY, 1.8, 0.7).shift(LEFT * 5.2)
        effect_values = ["PUBLISH", "SPEND", "PRIVATE DATA", "TOOL", "DEPLOY", "OTHER PERSON"]
        effect_sockets = self.grid(effect_values, [ROLLBACK] * 6, 3, 2.35).shift(RIGHT * 1.6)
        crosses = VGroup(*[Cross(s, stroke_color=ROLLBACK, stroke_width=4) for s in effect_sockets])
        attempts = VGroup(*[Arrow(default_token.get_right(), s.get_left(), color=ROLLBACK, buff=0.08, stroke_width=2.5) for s in effect_sockets])
        no_silent = self.badge("NO SILENT AUTHORITY", ROLLBACK, 3.1, 0.72).shift(UP * -2.0)
        scene9 = VGroup(default_token, effect_sockets, crosses, attempts, no_silent)
        self.play_beat(9, FadeOut(scene8), FadeIn(default_token), Create(attempts), FadeIn(effect_sockets), LaggedStart(*[Create(x) for x in crosses], lag_ratio=0.1), FadeIn(no_silent), settle=0.75)

        # 10 — checksum keeps a visible source link
        raw_small = self.panel("RAW REQUEST", ACCENT, 3.2, 2.3).shift(LEFT * 4.8)
        raw_copy = self.request(compact=True).scale(0.6).move_to(raw_small)
        checksum = self.panel("INTENT CHECKSUM", COPPER, 6.4, 3.0).shift(RIGHT * 2.2)
        checksum_text = self.label("PREPARE A LAUNCH\nCANDIDATE TODAY", 25, INK, "BOLD").move_to(checksum)
        source_link = DashedLine(raw_small.get_right(), checksum.get_left(), color=BOUNDARY, stroke_width=4)
        contestable = self.badge("CONTESTABLE", AUTHORITY, 2.1).shift(RIGHT * 4.7 + UP * -2.4)
        scene10 = VGroup(raw_small, raw_copy, checksum, checksum_text, source_link, contestable)
        self.play_beat(10, FadeOut(scene9), FadeIn(raw_small), FadeIn(raw_copy), Create(source_link), FadeIn(checksum), Write(checksum_text), FadeIn(contestable), settle=0.7)

        # 11 — assumption diff makes guesses editable
        checksum_small = self.panel("CHECKSUM", COPPER, 3.8, 3.2).shift(LEFT * 4.1)
        checksum_short = self.label("LAUNCH\nCANDIDATE", 21, INK, "BOLD").move_to(checksum_small)
        diff = self.panel("ASSUMPTION DIFF", AUTHORITY, 7.1, 5.2).shift(RIGHT * 2.6)
        diff_rows = self.grid(["AUDIENCE", "ARTIFACT", "EVIDENCE", "SOURCE USE", "DEADLINE", "MEANS"], [AUTHORITY] * 6, 2, 2.25).move_to(diff)
        editable = self.badge("EDITABLE", EVIDENCE, 1.9).shift(RIGHT * 5.1 + UP * -2.0)
        scene11 = VGroup(checksum_small, checksum_short, diff, diff_rows, editable)
        self.play_beat(11, FadeOut(scene10), FadeIn(checksum_small), FadeIn(checksum_short), FadeIn(diff), LaggedStart(*[FadeIn(r, shift=LEFT * 0.25) for r in diff_rows], lag_ratio=0.1), FadeIn(editable), settle=0.75)

        # 12 — three corrections narrow the contract
        before = self.grid(["QUOTE NOTES", "PAID REACH", "PUBLISH NOW"], [ROLLBACK] * 3, 1, 2.45).shift(LEFT * 3.8)
        after = self.grid(["INFORM · DO NOT QUOTE", "$0", "DRAFT ONLY"], [EVIDENCE, EVIDENCE, AUTHORITY], 1, 2.85).shift(RIGHT * 3.6)
        corrections = VGroup(*[Arrow(before[i].get_right(), after[i].get_left(), color=COPPER, buff=0.08) for i in range(3)])
        corrected = self.badge("3 MATERIAL CORRECTIONS", COPPER, 3.3).shift(UP * -2.0)
        scene12 = VGroup(before, after, corrections, corrected)
        self.play_beat(12, FadeOut(scene11), FadeIn(before), Create(corrections), LaggedStart(*[FadeIn(a) for a in after], lag_ratio=0.15), FadeIn(corrected), settle=0.75)

        # 13 — V1 opens draft, not publication
        v1 = self.contract("V1").shift(LEFT * 3.8)
        v1_fields = self.grid(["PRIVATE DRAFT", "COMPARISON SET"], [EVIDENCE, EVIDENCE], 1, 2.25).move_to(v1)
        gate13 = self.gate().scale(0.82).shift(RIGHT * 1.1)
        draft_out = self.badge("PRIVATE DRAFT", EVIDENCE, 2.5, 0.75).shift(RIGHT * 4.7 + UP * 1.35)
        publish_out = self.badge("PUBLIC LAUNCH", ROLLBACK, 2.5, 0.75).shift(RIGHT * 4.7 + UP * -1.35)
        draft_path = Arrow(v1.get_right(), draft_out.get_left(), color=EVIDENCE, buff=0.1)
        publish_path = Arrow(v1.get_right(), gate13.get_left(), color=ROLLBACK, buff=0.1)
        publish_cross = Cross(publish_out, stroke_color=ROLLBACK)
        scene13 = VGroup(v1, v1_fields, gate13, draft_out, publish_out, draft_path, publish_path, publish_cross)
        self.play_beat(13, FadeOut(scene12), FadeIn(v1), FadeIn(v1_fields), FadeIn(gate13), GrowArrow(draft_path), FadeIn(draft_out), GrowArrow(publish_path), FadeIn(publish_out), Create(publish_cross), settle=0.75)

        # 14 — receipt binds source, version, lifecycle, and consumers
        receipt = self.panel("INTENT RECEIPT", COPPER, 12.0, 5.5)
        receipt_fields = self.grid(["REQUEST DIGEST", "V1", "PROVENANCE", "AMBIGUITIES", "FORBIDDEN", "APPROVALS", "CONSUMERS", "EXPIRY", "RE-CONTRACT"], [ACCENT, COPPER, MUTED, RESIDUAL, ROLLBACK, AUTHORITY, EVIDENCE, MUTED, COPPER], 3, 2.7).move_to(receipt)
        source_pin = self.badge("SOURCE", ACCENT, 1.7).shift(LEFT * 5.45 + UP * -2.0)
        consumer_pin = self.badge("DRAFT ONLY", EVIDENCE, 2.1).shift(RIGHT * 5.1 + UP * -2.0)
        scene14 = VGroup(receipt, receipt_fields, source_pin, consumer_pin)
        self.play_beat(14, FadeOut(scene13), FadeIn(receipt), LaggedStart(*[FadeIn(f) for f in receipt_fields], lag_ratio=0.07), FadeIn(source_pin), FadeIn(consumer_pin), settle=0.85)

        # 15 — page crosses; publish stops
        planner = self.panel("PLANNER", ACCENT, 3.0, 3.4).shift(LEFT * 5.0)
        gate15 = self.gate("V1 GATE").shift(RIGHT * 0.2)
        page = self.badge("PAGE", EVIDENCE, 1.7, 0.72).shift(LEFT * 2.7 + UP * 1.1)
        publish_job = self.badge("PUBLISH", ROLLBACK, 1.9, 0.72).shift(LEFT * 2.7 + UP * -1.1)
        page_dest = self.badge("DRAFT READY", EVIDENCE, 2.2).shift(RIGHT * 4.6 + UP * 1.1)
        blocked_dest = self.badge("BLOCKED", ROLLBACK, 2.0).shift(RIGHT * 2.1 + UP * -1.1)
        page_path = Line(page.get_center(), page_dest.get_center(), color=EVIDENCE, stroke_width=4)
        publish_path15 = Line(publish_job.get_center(), blocked_dest.get_center(), color=ROLLBACK, stroke_width=4)
        scene15 = VGroup(planner, gate15, page, publish_job, page_dest, blocked_dest, page_path, publish_path15)
        self.play_beat(15, FadeOut(scene14), FadeIn(planner), FadeIn(gate15), FadeIn(page), FadeIn(publish_job), Create(page_path), Create(publish_path15), MoveAlongPath(page, page_path), MoveAlongPath(publish_job, publish_path15), FadeIn(page_dest), FadeIn(blocked_dest), settle=0.75)

        # 16 — relabeling fails; material delta returns
        gate16 = self.gate("V1 GATE").shift(RIGHT * 3.7)
        blocked_publish = self.badge("PUBLISH", ROLLBACK, 2.1, 0.75).shift(RIGHT * 1.25)
        disguise = self.badge("POLISH?", COPPER, 2.1, 0.75).move_to(blocked_publish)
        disguise_cross = Cross(disguise, stroke_color=ROLLBACK, stroke_width=5)
        intake = self.panel("INTENT BOUNDARY", ACCENT, 3.7, 3.2).shift(LEFT * 4.5)
        return_arc = ArcBetweenPoints(blocked_publish.get_bottom(), intake.get_bottom(), angle=-1.0, color=COPPER, stroke_width=5)
        delta = self.badge("MATERIAL DELTA", COPPER, 2.6).shift(UP * -2.4)
        delta_token = Dot(return_arc.get_start(), radius=0.14, color=COPPER)
        scene16 = VGroup(gate16, blocked_publish, disguise, disguise_cross, intake, return_arc, delta, delta_token)
        self.play_beat(16, FadeOut(scene15), FadeIn(gate16), FadeIn(blocked_publish), TransformFromCopy(blocked_publish, disguise), Create(disguise_cross), FadeIn(intake), Create(return_arc), FadeIn(delta_token), MoveAlongPath(delta_token, return_arc), FadeIn(delta), settle=0.45)

        # 17 — V2 opens one exact publication aperture
        v1_old = self.contract("V1", MUTED, 3.3, 3.0).shift(LEFT * 5.0)
        v2 = self.contract("V2", COPPER, 6.4, 5.1).shift(RIGHT * 0.3)
        v2_fields = self.grid(["NAMED CHANNEL", "REVIEWED ARTIFACT", "DEADLINE", "EVIDENCE", "STOP", "REVOKE"], [AUTHORITY, EVIDENCE, MUTED, EVIDENCE, ROLLBACK, COPPER], 2, 2.35).move_to(v2)
        aperture = self.gate("ONE CHANNEL", EVIDENCE).scale(0.78).shift(RIGHT * 5.3)
        version_edge = Arrow(v1_old.get_right(), v2.get_left(), color=COPPER, buff=0.08)
        scene17 = VGroup(v1_old, v2, v2_fields, aperture, version_edge)
        self.play_beat(17, FadeOut(scene16), FadeIn(v1_old), GrowArrow(version_edge), TransformFromCopy(v1_old, v2), FadeIn(v2_fields), GrowFromCenter(aperture), settle=0.85)

        # 18 — other people's rights retain their own gates
        v2_key = self.badge("V2 KEY", COPPER, 1.8, 0.72).shift(LEFT * 5.2)
        rights = VGroup(*[self.gate(name, color).scale(0.54) for name, color in [("CONSENT", AUTHORITY), ("PRIVACY", ACCENT), ("OWNERSHIP", COPPER), ("ORGANIZATION", ROLLBACK)]])
        rights.arrange(RIGHT, buff=0.65).shift(RIGHT * 1.0)
        blocked_marks = VGroup(*[self.badge("SEPARATE", MUTED, 1.35, 0.38).scale(0.72).next_to(g, UP, buff=0.05) for g in rights])
        probe_lines = VGroup(*[Arrow(v2_key.get_right(), g.get_left(), color=MUTED, buff=0.08, stroke_width=2.4) for g in rights])
        scene18 = VGroup(v2_key, rights, blocked_marks, probe_lines)
        self.play_beat(18, FadeOut(scene17), FadeIn(v2_key), Create(probe_lines), LaggedStart(*[FadeIn(g) for g in rights], lag_ratio=0.12), FadeIn(blocked_marks), settle=0.8)

        # 19 — policy can narrow, never widen
        grant = self.panel("REQUESTER GRANT", COPPER, 4.5, 3.8).shift(LEFT * 4.4)
        policy = self.gate("POLICY", AUTHORITY).scale(0.8)
        narrow = self.panel("NARROWER GRANT", EVIDENCE, 3.6, 2.6).shift(RIGHT * 4.4)
        through = Arrow(grant.get_right(), policy.get_left(), color=AUTHORITY, buff=0.08)
        out = Arrow(policy.get_right(), narrow.get_left(), color=EVIDENCE, buff=0.08)
        widen = self.badge("WIDEN", ROLLBACK, 1.8).shift(RIGHT * 4.4 + UP * -2.4)
        widen_cross = Cross(widen, stroke_color=ROLLBACK)
        scene19 = VGroup(grant, policy, narrow, through, out, widen, widen_cross)
        self.play_beat(19, FadeOut(scene18), FadeIn(grant), GrowArrow(through), FadeIn(policy), GrowArrow(out), FadeIn(narrow), FadeIn(widen), Create(widen_cross), settle=0.75)

        # 20 — invariant bands cross every lowering
        nodes = self.grid(["PLAN", "JOB", "TOOL", "RECEIPT"], [ACCENT, COPPER, AUTHORITY, EVIDENCE], 4, 2.2).shift(UP * 1.4)
        bands = VGroup(*[
            Line(LEFT * 5.4, RIGHT * 5.4, color=color, stroke_width=5).shift(UP * y)
            for color, y in [(ACCENT, 0.25), (EVIDENCE, -0.45), (AUTHORITY, -1.15), (ROLLBACK, -1.85)]
        ])
        band_labels = VGroup(
            self.label("CONSTRAINT", 13, ACCENT, "BOLD").next_to(bands[0], LEFT, buff=0.1),
            self.label("EVIDENCE", 13, EVIDENCE, "BOLD").next_to(bands[1], LEFT, buff=0.1),
            self.label("CEILING", 13, AUTHORITY, "BOLD").next_to(bands[2], LEFT, buff=0.1),
            self.label("STOP", 13, ROLLBACK, "BOLD").next_to(bands[3], LEFT, buff=0.1),
        )
        exact = self.badge("PRESERVED THROUGH LOWERING", COPPER, 3.6).shift(UP * -2.75)
        scene20 = VGroup(nodes, bands, band_labels, exact)
        self.play_beat(20, FadeOut(scene19), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.14), Create(bands), FadeIn(band_labels), FadeIn(exact), settle=0.8)

        # 21 — eight material deltas reopen admission
        chain = self.grid(["V2", "PLAN", "JOB", "EFFECT"], [COPPER, ACCENT, AUTHORITY, EVIDENCE], 4, 1.75)
        triggers = self.grid(["AUDIENCE", "SOURCE", "TOOL", "SPEND", "AFFECTED", "EVIDENCE", "SURFACE", "STOP"], [ROLLBACK] * 8, 4, 1.75).shift(UP * 2.0)
        return_loop = ArcBetweenPoints(chain.get_right(), chain.get_left(), angle=-1.2, color=COPPER, stroke_width=5).shift(UP * -0.7)
        reopen = self.badge("REOPEN ADMISSION", COPPER, 2.8).shift(UP * -2.5)
        invalid = Cross(chain, stroke_color=ROLLBACK, stroke_width=5)
        scene21 = VGroup(chain, triggers, return_loop, reopen, invalid)
        self.play_beat(21, FadeOut(scene20), FadeIn(chain), LaggedStart(*[FadeIn(t) for t in triggers], lag_ratio=0.08), Create(invalid), Create(return_loop), FadeIn(reopen), settle=0.75)

        # 22 — same hash, invalid lifecycle
        original = self.badge("DIGEST 7A3…", COPPER, 2.3, 0.72).shift(LEFT * 5.2)
        stale = self.grid(["EXPIRED", "REVOKED", "SUPERSEDED", "WRONG CONSUMER"], [ROLLBACK] * 4, 1, 2.45).shift(RIGHT * 2.5)
        copies = VGroup(*[self.badge("7A3…", MUTED, 1.45, 0.4).scale(0.78).next_to(s, LEFT, buff=0.22) for s in stale])
        copy_paths = VGroup(*[Arrow(original.get_right(), c.get_left(), color=MUTED, buff=0.08, stroke_width=2.3) for c in copies])
        identity_limit = self.badge("IDENTITY ≠ CURRENT AUTHORITY", ROLLBACK, 3.8).shift(UP * -2.0)
        scene22 = VGroup(original, stale, copies, copy_paths, identity_limit)
        self.play_beat(22, FadeOut(scene21), FadeIn(original), Create(copy_paths), FadeIn(copies), LaggedStart(*[FadeIn(s) for s in stale], lag_ratio=0.12), FadeIn(identity_limit), settle=0.8)

        # 23 — friction scales with consequence
        low_path = Line(LEFT * 5.1 + UP * 1.5, RIGHT * 4.9 + UP * 1.5, color=EVIDENCE, stroke_width=5)
        high_points = [LEFT * 5.1 + UP * -1.25, LEFT * 2.8 + UP * -1.25, LEFT * 0.6 + UP * -0.45, RIGHT * 1.8 + UP * -1.25, RIGHT * 4.9 + UP * -1.25]
        high_segments = VGroup(*[Line(high_points[i], high_points[i + 1], color=AUTHORITY, stroke_width=5) for i in range(len(high_points) - 1)])
        low_token = self.badge("DRAFT", EVIDENCE, 1.55).move_to(low_path.get_start())
        high_token = self.badge("PUBLISH", AUTHORITY, 1.8).move_to(high_points[0])
        light_check = self.badge("LIGHT CHECK", EVIDENCE, 2.0).shift(UP * 2.25)
        full_checks = self.grid(["INTENT", "RIGHTS", "POLICY", "EVIDENCE"], [COPPER, ACCENT, AUTHORITY, EVIDENCE], 4, 1.65).shift(UP * -2.25)
        useful = self.badge("USEFUL HELP", EVIDENCE, 2.2).shift(RIGHT * 5.1 + UP * 2.35)
        governed = self.badge("GOVERNED EFFECT", AUTHORITY, 2.5).shift(RIGHT * 5.0 + UP * -2.3)
        scene23 = VGroup(low_path, high_segments, low_token, high_token, light_check, full_checks, useful, governed)
        self.play_beat(23, FadeOut(scene22), Create(low_path), Create(high_segments), FadeIn(low_token), FadeIn(high_token), MoveAlongPath(low_token, low_path), Succession(*[MoveAlongPath(high_token, s) for s in high_segments]), FadeIn(light_check), FadeIn(full_checks), FadeIn(useful), FadeIn(governed), Succession(Indicate(light_check, color=EVIDENCE, scale_factor=1.05), Indicate(full_checks, color=AUTHORITY, scale_factor=1.04), Indicate(useful, color=EVIDENCE, scale_factor=1.05), Indicate(governed, color=AUTHORITY, scale_factor=1.05)), settle=0.45)

        # 24 — non-aggregate scorecard
        receipt_core = Circle(radius=1.2, stroke_color=COPPER, stroke_width=4, fill_color="#172A34", fill_opacity=1)
        receipt_text = self.label("INTENT\nEVALUATION", 18, COPPER, "BOLD").move_to(receipt_core)
        metric_names = ["CORRECTION", "UNAUTH ACTION", "MISSED HELP", "CLARIFICATION", "RE-CONTRACT", "APPEAL", "LATENCY", "PRIVACY", "USEFUL DONE"]
        metric_colors = [ACCENT, ROLLBACK, RESIDUAL, MUTED, COPPER, AUTHORITY, MUTED, ACCENT, EVIDENCE]
        metrics = VGroup()
        spokes = VGroup()
        for i, (name, color) in enumerate(zip(metric_names, metric_colors)):
            angle = i * 6.283185307 / len(metric_names)
            point = RIGHT * (4.8 * cos(angle)) + UP * (2.75 * sin(angle))
            metric = self.badge(name, color, 1.95, 0.46).move_to(point)
            metrics.add(metric)
            spokes.add(Line(receipt_core.get_boundary_point(point), metric.get_boundary_point(-point), color=color, stroke_width=2.5))
        no_average = self.badge("NO SINGLE SCORE", ROLLBACK, 2.55).shift(UP * -1.95)
        scene24 = VGroup(receipt_core, receipt_text, spokes, metrics, no_average)
        metric_review = Succession(
            *[
                Indicate(metrics[i], color=metric_colors[i], scale_factor=1.07)
                for i in range(len(metrics))
            ],
            Indicate(no_average, color=ROLLBACK, scale_factor=1.06),
        )
        # Build the evaluation surface quickly, then keep the viewer's eye on
        # each named dimension in narration order. Running this enumeration as
        # its own timed pass prevents the final privacy/usefulness clause from
        # landing on a static scorecard.
        self.next_section("b24")
        remaining_24 = max(0.05, self.ENDS[23] - self.renderer.time)
        construction_24 = min(2.5, max(0.05, remaining_24 - 0.5))
        review_24 = max(0.05, remaining_24 - construction_24 - 0.35)
        self.play(
            LaggedStart(
                FadeOut(scene23),
                GrowFromCenter(receipt_core),
                FadeIn(receipt_text),
                Create(spokes),
                LaggedStart(*[FadeIn(m) for m in metrics], lag_ratio=0.06),
                FadeIn(no_average),
                lag_ratio=0.12,
            ),
            run_time=construction_24,
        )
        self.play(metric_review, run_time=review_24)
        self.wait_until(self.ENDS[23])

        # 25 — exact evidence ceiling
        boundary = VGroup(
            Line(UP * 3.0, UP * -3.0, color=AUTHORITY, stroke_width=5).shift(LEFT * 0.18),
            Line(UP * 3.0, UP * -3.0, color=AUTHORITY, stroke_width=5).shift(RIGHT * 0.18),
        )
        artifacts = self.grid(["SCHEMA", "ROUTES", "SYNTHETIC CASES", "MUTATIONS"], [EVIDENCE] * 4, 1, 2.4).shift(LEFT * 3.7)
        nonclaims = self.grid(["NOT NLU", "NOT CONSENT", "NOT SATISFACTION", "NOT DEPLOYED", "NOT EFFECT SAFETY"], [ROLLBACK] * 5, 1, 2.55).shift(RIGHT * 3.7)
        support = self.badge("ARGUMENT SUPPORT", AUTHORITY, 2.8).shift(UP * -1.95)
        scene25 = VGroup(boundary, artifacts, nonclaims, support)
        evidence_review = Succession(
            *[Indicate(a, color=EVIDENCE, scale_factor=1.05) for a in artifacts],
            *[Indicate(n, color=ROLLBACK, scale_factor=1.04) for n in nonclaims],
        )
        self.play_beat(25, FadeOut(scene24), FadeIn(artifacts), Create(boundary), LaggedStart(*[FadeIn(n) for n in nonclaims], lag_ratio=0.1), evidence_review, FadeIn(support), settle=0.45)

        # 26 — opening request resolves into help now and explicit authority later
        # Keep the callback comfortably inside the 16:9 action-safe edge. At
        # x=-5.0 the compact shell's stroke sat exactly on the frame boundary,
        # which clipped the opening words in delivery-resolution review.
        final_request = self.request(compact=True).shift(LEFT * 4.65 + UP * 2.25)
        final_v1 = self.contract("V1", COPPER, 3.1, 2.6).shift(LEFT * 2.4)
        final_draft = self.panel("PRIVATE DRAFT · DELIVERED", EVIDENCE, 3.8, 2.5).shift(RIGHT * 2.0 + UP * 1.6)
        final_v2 = self.contract("V2", COPPER, 3.1, 2.6).shift(LEFT * 2.4 + UP * -2.6)
        final_gate = self.gate("EXPLICIT CONTRACT", AUTHORITY).scale(0.62).shift(RIGHT * 1.5 + UP * -2.25)
        final_publish = self.badge("PUBLISH", ROLLBACK, 2.0, 0.72).shift(RIGHT * 4.9 + UP * -2.25)
        path_to_v1 = Arrow(final_request.get_bottom(), final_v1.get_left(), color=ACCENT, buff=0.1)
        path_to_draft = Arrow(final_v1.get_right(), final_draft.get_left(), color=EVIDENCE, buff=0.1)
        path_to_v2 = Arrow(final_v1.get_bottom(), final_v2.get_top(), color=COPPER, buff=0.1)
        path_to_publish = Arrow(final_v2.get_right(), final_gate.get_left(), color=AUTHORITY, buff=0.08)
        corrigible = self.badge("CORRIGIBLE BOUNDARY · NOT AMBIENT POWER", AUTHORITY, 4.6).shift(RIGHT * 2.8 + UP * -0.2)
        self.play_beat(26, FadeOut(scene25), FadeIn(final_request), GrowArrow(path_to_v1), FadeIn(final_v1), GrowArrow(path_to_draft), FadeIn(final_draft), Indicate(final_draft, color=EVIDENCE, scale_factor=1.04), GrowArrow(path_to_v2), FadeIn(final_v2), GrowArrow(path_to_publish), FadeIn(final_gate), FadeIn(final_publish), Indicate(final_gate, color=AUTHORITY, scale_factor=1.04), FadeIn(corrigible), settle=0.5)

        # 27 — meaningful-control handoff retains the resolved world
        review_role = self.badge("REVIEW ROLE", AUTHORITY, 2.1, 0.72).move_to(final_v2)
        next_boundary = self.panel("NEXT · MEANINGFUL CONTROL", ACCENT, 4.4, 2.2).shift(RIGHT * 4.2 + UP * 2.45)
        handoff_path = ArcBetweenPoints(final_v2.get_top(), next_boundary.get_left(), angle=0.65, color=AUTHORITY, stroke_width=4)
        self.play_beat(27, TransformFromCopy(final_v2, review_role), Create(handoff_path), MoveAlongPath(review_role, handoff_path), FadeIn(next_boundary), settle=0.75)
