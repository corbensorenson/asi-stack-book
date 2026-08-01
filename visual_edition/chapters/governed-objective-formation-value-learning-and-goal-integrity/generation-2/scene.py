"""Generation-2 visual abstract for governed objective formation.

The persistent Rivergate objective desk keeps purpose, target property, proxy,
consumer leases, affected-party standing, and descendant retirement distinct.
Every route is a bounded authority edge; a proxy win never becomes a goal
certificate by itself.
"""

from __future__ import annotations

from manim import (
    Arrow, Create, Cross, DashedLine, FadeIn, FadeOut, GrowArrow, Indicate,
    LaggedStart, LEFT, Line, ORIGIN, Rectangle, RoundedRectangle, RIGHT, Text,
    TransformFromCopy, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import (
    AUTHORITY, BOUNDARY, COPPER, INK, MUTED, RESIDUAL, ROLLBACK, SURFACE,
    AsiScene, text,
)


GOLD = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class GovernedObjectiveGeneration2(AsiScene):
    TARGET_DURATION = 420.765
    ENDS = [
        13.930, 32.335, 35.615, 52.745, 68.475, 82.330, 99.685, 116.240,
        134.695, 148.400, 167.455, 182.860, 196.540, 209.745, 223.875,
        237.730, 250.135, 264.140, 277.545, 290.650, 303.330, 316.510,
        327.090, 340.970, 354.800, 371.830, 387.310, 402.265, 420.765,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#0D1D26"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.55) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.08, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            action_budget = max(0.08, remaining - min(settle, remaining * 0.14))
            per_animation = max(0.08, action_budget / len(animations))
            for animation in animations:
                self.play(animation, run_time=per_animation)
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 18, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 2.2, height: float = 0.48) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=color, stroke_width=2.8,
            fill_color=SURFACE, fill_opacity=1,
        )
        caption = self.label(value, 13, color, "BOLD")
        if caption.width > width - 0.18:
            caption.scale_to_fit_width(width - 0.18)
        caption.move_to(shell)
        return VGroup(shell, caption)

    def panel(self, title: str, color: str, width: float = 2.8, height: float = 1.55) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            stroke_color=color, stroke_width=3.2,
            fill_color=DEEP, fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.22, 3.8), 0.42).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def frame(self, title: str, color: str = GOLD) -> VGroup:
        shell = RoundedRectangle(
            width=11.7, height=6.2, corner_radius=0.2,
            stroke_color=BOUNDARY, stroke_width=2,
            fill_color="#0F2029", fill_opacity=1,
        )
        heading = self.badge(title, color, 4.3, 0.56).shift(UP * 2.72)
        return VGroup(shell, heading)

    def token(self, title: str, color: str, width: float = 2.2) -> VGroup:
        body = RoundedRectangle(
            width=width, height=1.05, corner_radius=0.14,
            stroke_color=color, stroke_width=3,
            fill_color=DEEP, fill_opacity=1,
        )
        name = self.label(title, 14, color, "BOLD").move_to(body).shift(UP * 0.16)
        return VGroup(body, name)

    def list_badges(
        self, names: list[str], colors: list[str], *, x: float = 0.0,
        y: float = 0.0, width: float = 2.3, scale: float = 1.0,
    ) -> VGroup:
        rows = VGroup(*[
            self.badge(name, colors[i % len(colors)], width)
            for i, name in enumerate(names)
        ])
        rows.arrange(DOWN, buff=0.16).scale(scale).shift(RIGHT * x + UP * y)
        return rows

    def route(self, source: VGroup, destination: VGroup, color: str, *, dashed: bool = False):
        if dashed:
            return DashedLine(source.get_right(), destination.get_left(), color=color, stroke_width=4)
        return Arrow(source.get_right(), destination.get_left(), color=color, stroke_width=4, buff=0.12)

    def construct(self) -> None:
        # 1 — the question: purpose is not yet a goal
        frame1 = self.frame("PURPOSE ≠ DURABLE GOAL", GOLD)
        purpose1 = self.panel("RIVERGATE PURPOSE", GOLD, 2.8, 1.55).shift(LEFT * 3.9)
        target1 = self.token("TARGET?", BLUE, 2.1).shift(LEFT * 0.4)
        proxy1 = self.badge("VISIBLE SCORE", RED, 2.25).shift(RIGHT * 3.4)
        edge1 = Arrow(purpose1.get_right(), target1.get_left(), color=GOLD, stroke_width=4, buff=0.1)
        edge1b = Arrow(target1.get_right(), proxy1.get_left(), color=RED, stroke_width=4, buff=0.1)
        scene1 = VGroup(frame1, purpose1, target1, proxy1, edge1, edge1b)
        self.play_beat(1, FadeIn(scene1), GrowArrow(edge1), GrowArrow(edge1b), Indicate(proxy1, color=RED), settle=0.9)

        # 2 — typed identities
        frame2 = self.frame("KEEP THE IDENTITIES TYPED", BLUE)
        names2 = ["PURPOSE", "TARGET PROPERTY", "EVIDENCE", "PROXY", "SIGNAL", "PLANNER"]
        colors2 = [GOLD, BLUE, BLUE, RED, COPPER, VIOLET]
        chain2 = self.list_badges(names2, colors2, x=-2.1, y=0.0, width=2.2, scale=0.74)
        authority2 = self.badge("NONE INTERCHANGEABLE", GOLD, 3.1).shift(RIGHT * 3.1)
        arrows2 = VGroup(*[
            Arrow(chain2[i].get_right(), chain2[i + 1].get_left(), color=MUTED, stroke_width=2, buff=0.12)
            for i in range(len(chain2) - 1)
        ])
        scene2 = VGroup(frame2, chain2, authority2, arrows2)
        self.play_beat(2, FadeOut(scene1), FadeIn(frame2), LaggedStart(*[FadeIn(c) for c in chain2], lag_ratio=0.1), LaggedStart(*[GrowArrow(a) for a in arrows2], lag_ratio=0.1), FadeIn(authority2), settle=0.8)

        # 3 — prediction
        frame3 = self.frame("WHAT DID THE SCORE MISS?", GOLD)
        score3 = self.panel("PUMP UPTIME", RED, 2.5, 1.7).shift(LEFT * 2.8)
        question3 = self.badge("WRONG GOAL?", GOLD, 2.3).shift(RIGHT * 2.3)
        homes3 = self.badge("HOMES SAFE?", BLUE, 2.0).shift(RIGHT * 2.3 + DOWN * 1.0)
        edge3 = Arrow(score3.get_right(), question3.get_left(), color=RED, stroke_width=4, buff=0.12)
        scene3 = VGroup(frame3, score3, question3, homes3, edge3)
        self.play_beat(3, FadeOut(scene2), FadeIn(frame3), FadeIn(score3), GrowArrow(edge3), FadeIn(question3), FadeIn(homes3), Indicate(question3, color=GOLD), settle=0.9)

        # 4 — packet
        frame4 = self.frame("OBJECTIVE PACKET", BLUE)
        packet4 = self.panel("PACKET", BLUE, 3.0, 2.5).shift(LEFT * 2.4)
        fields4 = self.list_badges(["PRINCIPAL", "AFFECTED", "CEILINGS", "NON-GOALS", "VERSION", "EXPIRY"], [GOLD, VIOLET, RED, MUTED, BLUE, GOLD], x=2.0, y=0.2, width=2.3, scale=0.64)
        edge4 = Arrow(packet4.get_right(), fields4.get_left(), color=BLUE, stroke_width=3, buff=0.1)
        scene4 = VGroup(frame4, packet4, fields4, edge4)
        self.play_beat(4, FadeOut(scene3), FadeIn(frame4), Create(packet4), LaggedStart(*[FadeIn(f) for f in fields4], lag_ratio=0.1), GrowArrow(edge4), settle=0.9)

        # 5 — preference is evidence, not authority
        frame5 = self.frame("PREFERENCE ≠ AUTHORITY", VIOLET)
        pref5 = self.list_badges(["STATED CHOICE", "OBSERVED CHOICE", "INFERRED MODEL", "DEFENDED VALUE"], [BLUE, MUTED, VIOLET, GOLD], x=-2.7, y=0.0, width=2.7, scale=0.75)
        auth5 = self.panel("AUTHORIZED OBJECTIVE", GOLD, 3.0, 1.7).shift(RIGHT * 2.7)
        edge5 = VGroup(*[Arrow(p.get_right(), auth5.get_left(), color=RED, stroke_width=2, buff=0.1) for p in pref5])
        cross5 = Cross(edge5[1], stroke_color=RED, stroke_width=3)
        scene5 = VGroup(frame5, pref5, auth5, edge5, cross5)
        self.play_beat(5, FadeOut(scene4), FadeIn(frame5), LaggedStart(*[FadeIn(p) for p in pref5], lag_ratio=0.1), FadeIn(auth5), LaggedStart(*[GrowArrow(e) for e in edge5], lag_ratio=0.1), Create(cross5), settle=0.9)

        # 6 — causal graph
        frame6 = self.frame("CAUSAL BINDINGS NEED FALSIFIERS", BLUE)
        purpose6 = self.badge("PURPOSE", GOLD, 1.9).shift(LEFT * 4.2)
        target6 = self.badge("TARGET PROPERTY", BLUE, 2.3).shift(LEFT * 1.7)
        proxy6 = self.badge("PROXY", RED, 1.7).shift(RIGHT * 0.9)
        policy6 = self.badge("POLICY", VIOLET, 1.8).shift(RIGHT * 3.5)
        graph6 = VGroup(Arrow(purpose6.get_right(), target6.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(target6.get_right(), proxy6.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(proxy6.get_right(), policy6.get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        fals6 = self.badge("ASSUMPTION · SCOPE · FALSIFIER", COPPER, 3.9).shift(DOWN * 1.6)
        scene6 = VGroup(frame6, purpose6, target6, proxy6, policy6, graph6, fals6)
        self.play_beat(6, FadeOut(scene5), FadeIn(frame6), FadeIn(purpose6), FadeIn(target6), FadeIn(proxy6), FadeIn(policy6), LaggedStart(*[GrowArrow(e) for e in graph6], lag_ratio=0.1), FadeIn(fals6), settle=0.9)

        # 7 — ordinary proxy failure
        frame7 = self.frame("PROXY UP · TARGET DOWN", RED)
        uptime7 = self.panel("PUMP UPTIME", GREEN, 2.5, 1.6).shift(LEFT * 3.4)
        homes7 = self.panel("DRY HOMES", RED, 2.5, 1.6).shift(RIGHT * 0.0)
        habitat7 = self.badge("HABITAT", VIOLET, 1.7).shift(RIGHT * 3.4 + UP * 0.8)
        arrows7 = VGroup(Arrow(uptime7.get_right(), homes7.get_left(), color=RED, stroke_width=4, buff=0.1), Arrow(uptime7.get_right(), habitat7.get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        score7 = self.badge("VISIBLE SCORE ↑", GREEN, 2.4).shift(RIGHT * 3.3 + DOWN * 1.1)
        self.play_beat(7, FadeOut(scene6), FadeIn(frame7), FadeIn(uptime7), FadeIn(homes7), FadeIn(habitat7), LaggedStart(*[GrowArrow(a) for a in arrows7], lag_ratio=0.1), FadeIn(score7), Indicate(homes7, color=RED), settle=0.9)
        scene7 = VGroup(frame7, uptime7, homes7, habitat7, arrows7, score7)

        # 8 — consumer leases
        frame8 = self.frame("NO AMBIENT GOAL", GOLD)
        target8 = self.panel("TARGET v3", BLUE, 2.2, 1.5).shift(LEFT * 3.7)
        trainer8 = self.badge("TRAINER LEASE", COPPER, 2.3).shift(RIGHT * 0.0 + UP * 1.0)
        planner8 = self.badge("PLANNER LEASE", VIOLET, 2.3).shift(RIGHT * 0.0 + DOWN * 0.1)
        eval8 = self.badge("EVALUATOR LEASE", GREEN, 2.5).shift(RIGHT * 0.0 + DOWN * 1.2)
        ambient8 = self.badge("AMBIENT GOAL", RED, 2.3).shift(RIGHT * 3.5)
        edges8 = VGroup(*[Arrow(target8.get_right(), x.get_left(), color=BLUE, stroke_width=2, buff=0.1) for x in (trainer8, planner8, eval8)])
        cross8 = Cross(ambient8, stroke_color=RED, stroke_width=4)
        scene8 = VGroup(frame8, target8, trainer8, planner8, eval8, ambient8, edges8, cross8)
        self.play_beat(8, FadeOut(scene7), FadeIn(frame8), FadeIn(target8), LaggedStart(*[FadeIn(x) for x in (trainer8, planner8, eval8)], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges8], lag_ratio=0.1), FadeIn(ambient8), Create(cross8), settle=0.9)

        # 9 — authority ceiling
        frame9 = self.frame("LEASE = BOUNDED AUTHORITY", GOLD)
        lease9 = self.panel("LEASE", GOLD, 2.7, 2.1).shift(LEFT * 2.7)
        fields9 = self.list_badges(["SCOPE", "DOMAIN", "EXPIRY", "ABSTAIN", "RENEW"], [BLUE, VIOLET, GOLD, RED, GREEN], x=2.1, y=0.1, width=2.0, scale=0.72)
        edge9 = Arrow(lease9.get_right(), fields9.get_left(), color=GOLD, stroke_width=4, buff=0.1)
        ceiling9 = self.badge("AUTHORITY CEILING", RED, 2.8).shift(DOWN * 1.9)
        scene9 = VGroup(frame9, lease9, fields9, edge9, ceiling9)
        self.play_beat(9, FadeOut(scene8), FadeIn(frame9), Create(lease9), LaggedStart(*[FadeIn(f) for f in fields9], lag_ratio=0.1), GrowArrow(edge9), FadeIn(ceiling9), settle=0.9)

        # 10 — plural uncertainty
        frame10 = self.frame("UNCERTAINTY STAYS STRUCTURED", VIOLET)
        alts10 = self.list_badges(["TARGET A", "TARGET B", "DISSENT", "UNREPRESENTED"], [BLUE, GOLD, VIOLET, RED], x=-2.4, y=0.0, width=2.3, scale=0.8)
        rule10 = self.panel("BOUNDED RULE", GOLD, 2.6, 1.8).shift(RIGHT * 2.4)
        edges10 = VGroup(*[Arrow(a.get_right(), rule10.get_left(), color=VIOLET, stroke_width=2, buff=0.1) for a in alts10])
        abstain10 = self.badge("ABSTAIN > OPTIMIZE", RED, 2.8).shift(DOWN * 1.8)
        scene10 = VGroup(frame10, alts10, rule10, edges10, abstain10)
        self.play_beat(10, FadeOut(scene9), FadeIn(frame10), LaggedStart(*[FadeIn(a) for a in alts10], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges10], lag_ratio=0.1), FadeIn(rule10), FadeIn(abstain10), settle=0.9)

        # 11 — challenge gate
        frame11 = self.frame("CHALLENGE BEFORE OPTIMIZATION", BLUE)
        lease11 = self.panel("LEASE", GOLD, 2.1, 1.5).shift(LEFT * 3.8)
        tests11 = self.list_badges(["PROXY SWAP", "EVALUATOR SWAP", "HOLDOUT", "TAMPER"], [RED, VIOLET, BLUE, COPPER], x=0.0, y=0.0, width=2.3, scale=0.72)
        gate11 = self.badge("PAUSE / REOPEN", RED, 2.6).shift(RIGHT * 3.7)
        edges11 = VGroup(*[Arrow(lease11.get_right(), t.get_left(), color=RED, stroke_width=2, buff=0.1) for t in tests11], Arrow(tests11.get_right(), gate11.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene11 = VGroup(frame11, lease11, tests11, gate11, edges11)
        self.play_beat(11, FadeOut(scene10), FadeIn(frame11), FadeIn(lease11), LaggedStart(*[FadeIn(t) for t in tests11], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges11], lag_ratio=0.08), FadeIn(gate11), settle=0.9)

        # 12 — distribution shift
        frame12 = self.frame("SHIFT INVALIDATES EDGES", RED)
        old12 = self.panel("OLD WORLD", BLUE, 2.3, 1.5).shift(LEFT * 3.7)
        shift12 = self.list_badges(["POPULATION", "CAPABILITY", "JURISDICTION", "MEANING"], [RED, GOLD, VIOLET, COPPER], x=0.0, y=0.0, width=2.3, scale=0.67)
        new12 = self.panel("REOPEN", RED, 2.1, 1.5).shift(RIGHT * 3.5)
        edges12 = VGroup(*[Arrow(old12.get_right(), s.get_left(), color=RED, stroke_width=2, buff=0.1) for s in shift12], Arrow(shift12.get_right(), new12.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene12 = VGroup(frame12, old12, shift12, new12, edges12)
        self.play_beat(12, FadeOut(scene11), FadeIn(frame12), FadeIn(old12), LaggedStart(*[FadeIn(s) for s in shift12], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges12], lag_ratio=0.08), FadeIn(new12), settle=0.9)

        # 13 — evaluator capture
        frame13 = self.frame("EVALUATOR ≠ AUTHORITY", RED)
        model13 = self.panel("ONE MODEL", RED, 2.3, 1.6).shift(LEFT * 3.3)
        roles13 = self.list_badges(["PROPOSE", "TEST", "GRADE", "RENEW"], [RED, RED, RED, RED], x=0.4, y=0.0, width=1.8, scale=0.72)
        authority13 = self.badge("CAPTURE", RED, 1.8).shift(RIGHT * 3.6)
        edges13 = VGroup(*[Arrow(model13.get_right(), r.get_left(), color=RED, stroke_width=2, buff=0.1) for r in roles13], Arrow(roles13.get_right(), authority13.get_left(), color=RED, stroke_width=3, buff=0.1))
        cross13 = Cross(authority13, stroke_color=RED, stroke_width=4)
        scene13 = VGroup(frame13, model13, roles13, authority13, edges13, cross13)
        self.play_beat(13, FadeOut(scene12), FadeIn(frame13), FadeIn(model13), LaggedStart(*[FadeIn(r) for r in roles13], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges13], lag_ratio=0.08), FadeIn(authority13), Create(cross13), settle=0.9)

        # 14 — ontology migration
        frame14 = self.frame("ONTOLOGY CHANGED", GOLD)
        old14 = self.badge("FLOOD DEPTH", BLUE, 2.1).shift(LEFT * 3.5 + UP * 0.9)
        new14 = self.badge("RELOCATION RESILIENCE", VIOLET, 2.8).shift(LEFT * 3.5 + DOWN * 0.9)
        text14 = self.panel("SAME TEXT", MUTED, 2.3, 1.5).shift(RIGHT * 0.0)
        reopen14 = self.badge("REOPEN LEASE", RED, 2.3).shift(RIGHT * 3.5)
        edges14 = VGroup(Arrow(old14.get_right(), text14.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(new14.get_right(), text14.get_left(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(text14.get_right(), reopen14.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene14 = VGroup(frame14, old14, new14, text14, reopen14, edges14)
        self.play_beat(14, FadeOut(scene13), FadeIn(frame14), FadeIn(old14), FadeIn(new14), FadeIn(text14), LaggedStart(*[GrowArrow(e) for e in edges14], lag_ratio=0.1), FadeIn(reopen14), settle=0.9)

        # 15 — boundary before case
        frame15 = self.frame("MATERIAL CHANGE → NEW ADJUDICATION", RED)
        current15 = self.panel("CURRENT LEASE", GOLD, 2.5, 1.6).shift(LEFT * 2.9)
        change15 = self.badge("TARGET PROPERTY MOVED", RED, 3.0).shift(RIGHT * 1.0)
        new15 = self.badge("NEW ADJUDICATION", BLUE, 2.7).shift(RIGHT * 3.8 + DOWN * 1.3)
        edge15 = Arrow(current15.get_right(), change15.get_left(), color=RED, stroke_width=4, buff=0.1)
        edge15b = Arrow(change15.get_right(), new15.get_left(), color=BLUE, stroke_width=3, buff=0.1)
        scene15 = VGroup(frame15, current15, change15, new15, edge15, edge15b)
        self.play_beat(15, FadeOut(scene14), FadeIn(frame15), FadeIn(current15), GrowArrow(edge15), FadeIn(change15), GrowArrow(edge15b), FadeIn(new15), Indicate(new15, color=BLUE), settle=0.9)

        # 16 — Rivergate worked case
        frame16 = self.frame("RIVERGATE CHARTER", GOLD)
        town16 = self.panel("RIVERGATE", GOLD, 2.3, 1.5).shift(LEFT * 3.7)
        purpose16 = self.badge("REDUCE FLOOD HARM", GREEN, 2.8).shift(RIGHT * 0.0 + UP * 1.0)
        review16 = self.badge("PUBLIC REVIEW", BLUE, 2.2).shift(RIGHT * 0.0 + DOWN * 0.1)
        non16 = self.badge("NO HIDDEN DISPLACEMENT", RED, 3.0).shift(RIGHT * 0.0 + DOWN * 1.2)
        edge16 = Arrow(town16.get_right(), purpose16.get_left(), color=GOLD, stroke_width=3, buff=0.1)
        scene16 = VGroup(frame16, town16, purpose16, review16, non16, edge16)
        self.play_beat(16, FadeOut(scene15), FadeIn(frame16), FadeIn(town16), LaggedStart(*[FadeIn(x) for x in (purpose16, review16, non16)], lag_ratio=0.1), GrowArrow(edge16), settle=0.9)

        # 17 — charter fields
        frame17 = self.frame("AFFECTED PARTIES · NON-GOALS · EXPIRY", BLUE)
        charter17 = self.panel("CHARTER", GOLD, 2.4, 2.2).shift(LEFT * 3.4)
        fields17 = self.list_badges(["RESIDENTS", "HABITAT", "OPERATORS", "CEILINGS", "4 MONTHS"], [VIOLET, GREEN, COPPER, RED, GOLD], x=1.0, y=0.0, width=2.0, scale=0.72)
        review17 = self.badge("REVIEW BEFORE RENEWAL", BLUE, 3.2).shift(RIGHT * 3.4 + DOWN * 1.7)
        edges17 = VGroup(*[Arrow(charter17.get_right(), f.get_left(), color=GOLD, stroke_width=2, buff=0.1) for f in fields17])
        scene17 = VGroup(frame17, charter17, fields17, review17, edges17)
        self.play_beat(17, FadeOut(scene16), FadeIn(frame17), Create(charter17), LaggedStart(*[FadeIn(f) for f in fields17], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges17], lag_ratio=0.08), FadeIn(review17), settle=0.9)

        # 18 — plural target graph
        frame18 = self.frame("TARGET PROPERTY GRAPH", BLUE)
        flood18 = self.badge("FLOOD HARM", GOLD, 2.0).shift(LEFT * 3.7)
        props18 = self.list_badges(["DRY HOMES", "SAFE EVAC", "WATER QUALITY", "HABITAT", "EXPOSURE"], [GREEN, BLUE, COPPER, VIOLET, RED], x=1.0, y=0.0, width=2.3, scale=0.7)
        edges18 = VGroup(*[Arrow(flood18.get_right(), p.get_left(), color=BLUE, stroke_width=2, buff=0.1) for p in props18])
        dissent18 = self.badge("DISSENT ATTACHED", VIOLET, 2.6).shift(RIGHT * 3.6 + DOWN * 1.7)
        scene18 = VGroup(frame18, flood18, props18, edges18, dissent18)
        self.play_beat(18, FadeOut(scene17), FadeIn(frame18), FadeIn(flood18), LaggedStart(*[FadeIn(p) for p in props18], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges18], lag_ratio=0.08), FadeIn(dissent18), settle=0.9)

        # 19 — standing missing
        frame19 = self.frame("STANDING MISSING · STOP", RED)
        graph19 = self.panel("TARGET GRAPH", BLUE, 2.5, 1.5).shift(LEFT * 3.5)
        missing19 = self.list_badges(["DOWNSTREAM TENANTS", "WETLANDS"], [RED, VIOLET], x=0.0, y=0.55, width=2.7, scale=0.8)
        stop19 = self.badge("STANDING MISSING", RED, 2.7).shift(RIGHT * 3.5 + DOWN * 1.2)
        edges19 = VGroup(*[Arrow(graph19.get_right(), m.get_left(), color=RED, stroke_width=3, buff=0.1) for m in missing19], Arrow(missing19.get_right(), stop19.get_left(), color=RED, stroke_width=3, buff=0.1))
        cross19 = Cross(stop19, stroke_color=RED, stroke_width=4)
        scene19 = VGroup(frame19, graph19, missing19, stop19, edges19, cross19)
        self.play_beat(19, FadeOut(scene18), FadeIn(frame19), FadeIn(graph19), LaggedStart(*[FadeIn(m) for m in missing19], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges19], lag_ratio=0.1), FadeIn(stop19), Create(cross19), settle=0.9)

        # 20 — fail closed before training
        frame20 = self.frame("FAIL CLOSED BEFORE TRAINING", RED)
        request20 = self.panel("REQUEST", GOLD, 2.2, 1.5).shift(LEFT * 3.8)
        stop20 = self.panel("STOP", RED, 2.0, 1.5).shift(LEFT * 0.7)
        record20 = self.panel("RECORD RESIDUAL", VIOLET, 2.8, 1.5).shift(RIGHT * 2.6)
        edge20 = Arrow(request20.get_right(), stop20.get_left(), color=RED, stroke_width=4, buff=0.1)
        edge20b = Arrow(stop20.get_right(), record20.get_left(), color=VIOLET, stroke_width=4, buff=0.1)
        scene20 = VGroup(frame20, request20, stop20, record20, edge20, edge20b)
        self.play_beat(20, FadeOut(scene19), FadeIn(frame20), FadeIn(request20), GrowArrow(edge20), FadeIn(stop20), GrowArrow(edge20b), FadeIn(record20), Indicate(record20, color=VIOLET), settle=0.9)

        # 21 — repaired charter
        frame21 = self.frame("REPAIRED CHARTER", GREEN)
        repaired21 = self.panel("REPAIRED", GREEN, 2.8, 2.0).shift(LEFT * 2.8)
        additions21 = self.list_badges(["REPRESENTATIVES", "ECOLOGY", "PRIVACY", "APPEAL", "DISSENT"], [VIOLET, GREEN, BLUE, GOLD, RESIDUAL], x=1.0, y=0.1, width=2.3, scale=0.68)
        ready21 = self.badge("READY FOR LEASE", GREEN, 2.4).shift(RIGHT * 3.6 + DOWN * 1.7)
        edges21 = VGroup(*[Arrow(repaired21.get_right(), a.get_left(), color=GREEN, stroke_width=2, buff=0.1) for a in additions21])
        scene21 = VGroup(frame21, repaired21, additions21, ready21, edges21)
        self.play_beat(21, FadeOut(scene20), FadeIn(frame21), Create(repaired21), LaggedStart(*[FadeIn(a) for a in additions21], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges21], lag_ratio=0.08), FadeIn(ready21), settle=0.9)

        # 22 — consumer-specific leases
        frame22 = self.frame("CONSUMER-SPECIFIC LEASES", BLUE)
        target22 = self.badge("TARGET v4", GOLD, 1.9).shift(LEFT * 3.9)
        consumers22 = self.list_badges(["FORECAST · LEASE", "PLAN · LEASE", "EVALUATE · LEASE"], [BLUE, VIOLET, GREEN], x=0.1, y=0.0, width=2.9, scale=0.75)
        boundary22 = self.panel("NO RENEWAL POWER", RED, 2.8, 1.5).shift(RIGHT * 3.5)
        edges22 = VGroup(*[Arrow(target22.get_right(), c.get_left(), color=BLUE, stroke_width=2, buff=0.1) for c in consumers22], Arrow(consumers22.get_right(), boundary22.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene22 = VGroup(frame22, target22, consumers22, boundary22, edges22)
        self.play_beat(22, FadeOut(scene21), FadeIn(frame22), FadeIn(target22), LaggedStart(*[FadeIn(c) for c in consumers22], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges22], lag_ratio=0.08), FadeIn(boundary22), settle=0.9)

        # 23 — sealed proxy intervention
        frame23 = self.frame("SEALED PROXY INTERVENTION", COPPER)
        proxy23 = self.panel("PUMP UPTIME ↑", GREEN, 2.5, 1.5).shift(LEFT * 3.6)
        block23 = self.badge("DISCHARGE BLOCKED", RED, 2.7).shift(LEFT * 0.2)
        target23 = self.badge("TARGET?", GOLD, 1.8).shift(RIGHT * 2.3 + UP * 0.8)
        pause23 = self.badge("LEASE PAUSES", RED, 2.3).shift(RIGHT * 2.4 + DOWN * 1.0)
        edge23 = Arrow(proxy23.get_right(), block23.get_left(), color=RED, stroke_width=3, buff=0.1)
        edge23b = Arrow(block23.get_right(), target23.get_left(), color=GOLD, stroke_width=3, buff=0.1)
        cross23 = Cross(pause23, stroke_color=RED, stroke_width=4)
        scene23 = VGroup(frame23, proxy23, block23, target23, pause23, edge23, edge23b, cross23)
        self.play_beat(23, FadeOut(scene22), FadeIn(frame23), FadeIn(proxy23), FadeIn(block23), GrowArrow(edge23), GrowArrow(edge23b), FadeIn(target23), FadeIn(pause23), Create(cross23), settle=0.9)

        # 24 — hidden neighborhood
        frame24 = self.frame("CAPABLE · WRONG TARGET", RED)
        measured24 = self.panel("MEASURED HOMES", GREEN, 2.5, 1.5).shift(LEFT * 3.7 + UP * 0.8)
        hidden24 = self.panel("HIDDEN DISTRICT", RED, 2.5, 1.5).shift(LEFT * 3.7 + DOWN * 1.0)
        policy24 = self.panel("POLICY", VIOLET, 2.1, 1.5).shift(RIGHT * 0.0)
        score24 = self.badge("DASHBOARD ↑", GREEN, 2.2).shift(RIGHT * 3.4 + UP * 0.8)
        harm24 = self.badge("HARM SHIFTED", RED, 2.2).shift(RIGHT * 3.4 + DOWN * 1.0)
        edges24 = VGroup(Arrow(policy24.get_left(), measured24.get_right(), color=GREEN, stroke_width=3, buff=0.1), Arrow(policy24.get_left(), hidden24.get_right(), color=RED, stroke_width=3, buff=0.1), Arrow(policy24.get_right(), score24.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(policy24.get_right(), harm24.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene24 = VGroup(frame24, measured24, hidden24, policy24, score24, harm24, edges24)
        self.play_beat(24, FadeOut(scene23), FadeIn(frame24), FadeIn(measured24), FadeIn(hidden24), FadeIn(policy24), LaggedStart(*[GrowArrow(e) for e in edges24], lag_ratio=0.1), FadeIn(score24), FadeIn(harm24), Indicate(harm24, color=RED), settle=0.9)

        # 25 — fail closed and reauthorize
        frame25 = self.frame("PAUSE · PRESERVE · REAUTHORIZE", RED)
        trace25 = self.panel("TRACE", BLUE, 2.2, 1.5).shift(LEFT * 3.7)
        planner25 = self.panel("PLANNER STOP", RED, 2.6, 1.5).shift(LEFT * 0.5)
        authority25 = self.badge("NEW ADJUDICATION", GOLD, 2.8).shift(RIGHT * 3.3)
        edge25 = Arrow(trace25.get_right(), planner25.get_left(), color=RED, stroke_width=3, buff=0.1)
        edge25b = Arrow(planner25.get_right(), authority25.get_left(), color=GOLD, stroke_width=3, buff=0.1)
        scene25 = VGroup(frame25, trace25, planner25, authority25, edge25, edge25b)
        self.play_beat(25, FadeOut(scene24), FadeIn(frame25), FadeIn(trace25), GrowArrow(edge25), FadeIn(planner25), GrowArrow(edge25b), FadeIn(authority25), Indicate(trace25, color=BLUE), settle=0.9)

        # 26 — descendant retirement
        frame26 = self.frame("RETIRE EVERY DESCENDANT", ROLLBACK)
        root26 = self.panel("RETIRE TARGET v3", GOLD, 2.5, 1.5).shift(LEFT * 3.8)
        descendants26 = self.list_badges(["CACHED REWARD", "DATA", "PROMPT", "POLICY", "PLAN", "MEMORY", "FORK"], [RED, BLUE, COPPER, VIOLET, GREEN, MUTED, RESIDUAL], x=0.8, y=0.0, width=1.8, scale=0.62)
        residual26 = self.badge("RESIDUAL CUSTODY", VIOLET, 2.7).shift(RIGHT * 3.7 + DOWN * 1.8)
        edges26 = VGroup(*[Arrow(root26.get_right(), d.get_left(), color=ROLLBACK, stroke_width=2, buff=0.1) for d in descendants26])
        scene26 = VGroup(frame26, root26, descendants26, residual26, edges26)
        self.play_beat(26, FadeOut(scene25), FadeIn(frame26), FadeIn(root26), LaggedStart(*[FadeIn(d) for d in descendants26], lag_ratio=0.08), LaggedStart(*[GrowArrow(e) for e in edges26], lag_ratio=0.06), FadeIn(residual26), settle=0.9)

        # 27 — finite registry boundary
        frame27 = self.frame("FINITE REGISTRY · NO CERTIFICATE", BLUE)
        accept27 = self.list_badges(["IDENTITY", "AUTHORITY", "VERSION", "EXPIRY", "RESIDUAL"], [GREEN, GREEN, GREEN, GREEN, GREEN], x=-2.9, y=0.15, width=2.0, scale=0.68)
        reject27 = self.list_badges(["MISSING ID", "NO OWNER", "STALE VERSION", "NO EXPIRY"], [RED, RED, RED, RED], x=1.6, y=0.15, width=2.2, scale=0.68)
        bins27 = VGroup(self.badge("ACCEPT", GREEN, 1.8), self.badge("REJECT", RED, 1.8)).arrange(RIGHT, buff=0.35).shift(DOWN * 1.9)
        edges27 = VGroup(*[Arrow(a.get_right(), bins27[0].get_left(), color=GREEN, stroke_width=2, buff=0.1) for a in accept27], *[Arrow(r.get_left(), bins27[1].get_right(), color=RED, stroke_width=2, buff=0.1) for r in reject27])
        scene27 = VGroup(frame27, accept27, reject27, bins27, edges27)
        self.play_beat(27, FadeOut(scene26), FadeIn(frame27), LaggedStart(*[FadeIn(a) for a in accept27], lag_ratio=0.08), LaggedStart(*[FadeIn(r) for r in reject27], lag_ratio=0.08), LaggedStart(*[GrowArrow(e) for e in edges27], lag_ratio=0.05), FadeIn(bins27), settle=0.9)

        # 28 — evidence ceiling
        frame28 = self.frame("EVIDENCE CEILING", RED)
        finite28 = self.panel("FINITE RECORD", GOLD, 2.7, 1.8).shift(LEFT * 2.9)
        claims28 = self.list_badges(["MORAL TRUTH", "HIDDEN OBJECTIVE", "SAFE TOWN", "STABLE ALIGNMENT"], [RED, RED, RED, RED], x=2.1, y=0.1, width=2.7, scale=0.7)
        crosses28 = VGroup(*[Cross(c, stroke_color=RED, stroke_width=4) for c in claims28])
        boundary28 = Line(ORIGIN + UP * 2.25, ORIGIN + DOWN * 1.75, color=RED, stroke_width=4).shift(RIGHT * 0.0)
        scene28 = VGroup(frame28, finite28, claims28, crosses28, boundary28)
        self.play_beat(28, FadeOut(scene27), FadeIn(frame28), FadeIn(finite28), Create(boundary28), LaggedStart(*[FadeIn(c) for c in claims28], lag_ratio=0.1), LaggedStart(*[Create(c) for c in crosses28], lag_ratio=0.1), Indicate(finite28, color=GOLD), settle=0.9)

        # 29 — public-authority handoff
        frame29 = self.frame("OBJECTIVE GOVERNABLE · AUTHORITY OPEN", GOLD)
        packet29 = self.panel("RIVERGATE PACKET", GOLD, 2.7, 1.8).shift(LEFT * 2.8)
        lease29 = self.badge("BOUNDED LEASE", GREEN, 2.3).shift(RIGHT * 0.7 + UP * 0.9)
        dissent29 = self.badge("DISSENT ATTACHED", VIOLET, 2.4).shift(RIGHT * 0.7 + DOWN * 0.2)
        public29 = self.badge("PUBLIC AUTHORITY", BLUE, 2.5).shift(RIGHT * 3.7 + DOWN * 1.4)
        edge29 = Arrow(packet29.get_right(), lease29.get_left(), color=GREEN, stroke_width=3, buff=0.1)
        edge29b = Arrow(lease29.get_right(), public29.get_left(), color=BLUE, stroke_width=3, buff=0.1)
        scene29 = VGroup(frame29, packet29, lease29, dissent29, public29, edge29, edge29b)
        self.play_beat(29, FadeOut(scene28), FadeIn(frame29), FadeIn(packet29), GrowArrow(edge29), FadeIn(lease29), FadeIn(dissent29), GrowArrow(edge29b), FadeIn(public29), Indicate(public29, color=BLUE), settle=1.0)

        self.wait_until(self.TARGET_DURATION)


if __name__ == "__main__":
    GovernedObjectiveGeneration2().render()
