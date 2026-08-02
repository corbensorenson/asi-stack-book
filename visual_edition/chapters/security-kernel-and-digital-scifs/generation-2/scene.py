"""Generation-2 visual abstract for Security Kernel and Digital SCIFs.

The visual world is a security-operations desk.  An untrusted prompt, exact
authority lease, minimized context packet, SCIF boundary, mediated effect gate,
and residual receipt stay visible while a privileged request is admitted or
stopped.  This is an explanatory derivative and never promotes the chapter's
support state.
"""

from __future__ import annotations

from manim import (
    AnimationGroup, Arrow, Create, Cross, DashedLine, FadeIn, FadeOut,
    GrowArrow, Indicate, LEFT, RIGHT, RoundedRectangle, Text, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import (
    BOUNDARY, INK, MUTED, RESIDUAL, ROLLBACK, SURFACE, AsiScene, text,
)


AMBER = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class SecurityKernelDigitalScifsGeneration2(AsiScene):
    """A synchronized 04:57 visual explanation of a governed privileged use."""

    TARGET_DURATION = 297.03
    ENDS = [
        19.82, 22.79, 42.16, 49.965, 67.835, 87.83, 94.285, 98.655,
        117.475, 135.695, 144.025, 163.17, 177.54, 186.52, 201.54,
        215.835, 232.905, 237.885, 257.63, 265.96, 282.78, 297.03,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#0D1D26"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.6) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.08, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            action_budget = max(0.08, remaining - min(settle, remaining * 0.14))
            per_animation = min(1.25, action_budget) if len(animations) == 1 else max(0.08, action_budget / len(animations))
            for animation in animations:
                self.play(animation, run_time=per_animation)
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 17, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 2.2, height: float = 0.48) -> VGroup:
        shell = RoundedRectangle(width=width, height=height, corner_radius=0.1,
                                 stroke_color=color, stroke_width=2.5,
                                 fill_color=SURFACE, fill_opacity=1)
        caption = self.label(value, 12, color, "BOLD")
        if caption.width > width - 0.18:
            caption.scale_to_fit_width(width - 0.18)
        caption.move_to(shell)
        return VGroup(shell, caption)

    def panel(self, title: str, color: str, width: float = 2.5, height: float = 1.3) -> VGroup:
        shell = RoundedRectangle(width=width, height=height, corner_radius=0.16,
                                 stroke_color=color, stroke_width=3,
                                 fill_color=DEEP, fill_opacity=1)
        title_obj = self.badge(title, color, min(width - 0.16, 3.5), 0.4).scale(0.82)
        title_obj.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, title_obj)

    def frame(self, title: str, color: str = AMBER) -> VGroup:
        shell = RoundedRectangle(width=11.7, height=6.2, corner_radius=0.2,
                                 stroke_color=BOUNDARY, stroke_width=2,
                                 fill_color="#0F2029", fill_opacity=1)
        heading = self.badge(title, color, 5.7, 0.56).shift(UP * 2.72)
        return VGroup(shell, heading)

    def pills(self, names: list[str], colors: list[str], *, x: float = 0, y: float = 0,
              width: float = 1.75, scale: float = 0.68, direction=DOWN) -> VGroup:
        group = VGroup(*[self.badge(name, colors[i % len(colors)], width) for i, name in enumerate(names)])
        group.arrange(direction, buff=0.13).scale(scale).shift(RIGHT * x + UP * y)
        return group

    def arrows_between(self, source, targets, colors, *, dashed: bool = False) -> VGroup:
        arrows = []
        for i, target in enumerate(targets):
            color = colors[i % len(colors)]
            if dashed:
                arrows.append(DashedLine(source.get_right(), target.get_left(), color=color, stroke_width=2))
            else:
                arrows.append(Arrow(source.get_right(), target.get_left(), color=color, stroke_width=2.5, buff=0.08))
        return VGroup(*arrows)

    def construct(self) -> None:
        self.current = VGroup()
        for index in range(1, 23):
            next_scene = self.scene_for(index)
            animations = [FadeIn(next_scene)] if not self.current else [
                AnimationGroup(FadeOut(self.current), FadeIn(next_scene), lag_ratio=0)
            ]
            self.play_beat(index, *animations, settle=0.9 if index in (1, 5, 12, 21, 22) else 0.55)
            self.current = next_scene

    def scene_for(self, index: int) -> VGroup:
        if index == 1:
            frame = self.frame("UNTRUSTED INPUT · CROSS-BOUNDARY EFFECT SURFACE", RED)
            prompt = self.panel("UNTRUSTED PROMPT", RED, 2.35, 1.25).shift(LEFT * 4.1)
            targets = self.pills(["SECRETS", "IDENTITY", "MEMORY", "TOOLS", "MONEY", "CODE", "PHYSICAL EFFECT"],
                                 [RED, AMBER, BLUE, VIOLET, RED, AMBER, RESIDUAL], x=1.2, y=1.0, width=2.15, scale=0.55)
            lanes = self.pills(["MODEL", "RUNTIME", "OPERATOR", "VENDOR", "DESCENDANT"],
                               [BLUE, AMBER, VIOLET, RESIDUAL, RED], x=3.85, y=-1.25, width=2.0, scale=0.56, direction=RIGHT)
            return VGroup(frame, prompt, targets, lanes, self.arrows_between(prompt, targets, [RED] * len(targets)))
        if index == 2:
            frame = self.frame("VENDOR + DESCENDANT BOUNDARIES CONTINUE", RESIDUAL)
            model = self.panel("MODEL", BLUE, 2.25, 1.3).shift(LEFT * 3.4 + UP * 0.45)
            vendor = self.panel("VENDOR", AMBER, 2.25, 1.3).shift(LEFT * 0.45 + UP * 0.45)
            descendant = self.panel("DESCENDANT", RED, 2.55, 1.3).shift(RIGHT * 2.8 + UP * 0.45)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 1.15)
            return VGroup(frame, model, vendor, descendant, boundary,
                          Arrow(model.get_right(), vendor.get_left(), color=AMBER, stroke_width=3, buff=0.1),
                          Arrow(vendor.get_right(), descendant.get_left(), color=RED, stroke_width=3, buff=0.1),
                          self.badge("NOT MODEL-ONLY", RED, 2.55).shift(DOWN * 1.45))
        if index == 3:
            frame = self.frame("PROXY CONTROLS · COVERAGE GAPS", RED)
            proxies = self.pills(["PROMPT", "VISIBLE SECRET", "APPROVAL", "HANDLE", "ALLOWLIST", "CONTAINER", "FILTER", "LOG", "SCIF"],
                                 [AMBER, RED, AMBER, BLUE, BLUE, VIOLET, RED, MUTED, VIOLET], x=-1.9, y=1.05, width=1.65, scale=0.52)
            gaps = self.pills(["LEAST AUTHORITY", "MEDIATION", "DECLASSIFY", "REVOCATION", "RECOVERY"],
                              [RED, RED, RED, RESIDUAL, RESIDUAL], x=2.7, y=0.85, width=2.3, scale=0.57)
            boundary = DashedLine(UP * 2.25, DOWN * 2.25, color=RED, stroke_width=3).shift(RIGHT * 0.55)
            return VGroup(frame, proxies, gaps, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in gaps])
        if index == 4:
            frame = self.frame("MISSING OBLIGATIONS · NOT ONE MAGIC BOX", AMBER)
            proxy = self.panel("PROXY LABEL", MUTED, 2.5, 1.3).shift(LEFT * 3.5 + UP * 0.55)
            obligations = self.pills(["MEDIATE", "DECLASSIFY", "ISOLATE", "REVOKE", "SIDE CHANNEL", "RECOVER"],
                                     [RED, RED, VIOLET, RESIDUAL, RED, RESIDUAL], x=1.2, y=1.0, width=2.05, scale=0.56)
            return VGroup(frame, proxy, obligations, self.arrows_between(proxy, obligations, [RED] * len(obligations)),
                          self.badge("PROXY ≠ VECTOR", RED, 2.6).shift(LEFT * 2.9 + DOWN * 1.45))
        if index == 5:
            frame = self.frame("EXACT AUTHORITY LEASE · BEFORE ADMISSION", AMBER)
            request = self.panel("REQUEST", RED, 2.1, 1.25).shift(LEFT * 4.0)
            lease = self.panel("AUTHORITY LEASE", AMBER, 2.75, 1.5).shift(LEFT * 0.9)
            fields = self.pills(["PRINCIPAL", "PURPOSE", "OPERATION", "TARGET", "TAINT", "BUDGET", "TIME", "NONCE"],
                                [BLUE, AMBER, AMBER, RED, RED, MUTED, VIOLET, AMBER], x=3.1, y=0.95, width=1.8, scale=0.54)
            return VGroup(frame, request, lease, fields,
                          Arrow(request.get_right(), lease.get_left(), color=AMBER, stroke_width=3, buff=0.1),
                          self.arrows_between(lease, fields, [AMBER] * len(fields)),
                          self.badge("SCIF CLOSED", VIOLET, 2.0).shift(LEFT * 0.85 + DOWN * 1.55))
        if index == 6:
            frame = self.frame("MINIMIZE · ISOLATE · MEDIATE · REVOKE", VIOLET)
            lease = self.panel("LEASE", AMBER, 2.0, 1.2).shift(LEFT * 4.1 + UP * 0.7)
            context = self.panel("MINIMIZED CONTEXT", BLUE, 2.35, 1.3).shift(LEFT * 1.7 + UP * 0.7)
            scif = self.panel("GRADED SCIF", VIOLET, 2.35, 1.45).shift(RIGHT * 1.0 + UP * 0.7)
            gate = self.panel("EFFECT GATE", GREEN, 2.15, 1.3).shift(RIGHT * 3.75 + UP * 0.7)
            revoke = self.pills(["CACHE", "LOG", "DESCENDANT", "RESIDUAL"], [BLUE, MUTED, RESIDUAL, RED], x=1.05, y=-1.25, width=1.95, scale=0.58, direction=RIGHT)
            arrows = VGroup(Arrow(lease.get_right(), context.get_left(), color=AMBER, stroke_width=3, buff=0.08),
                            Arrow(context.get_right(), scif.get_left(), color=VIOLET, stroke_width=3, buff=0.08),
                            Arrow(scif.get_right(), gate.get_left(), color=GREEN, stroke_width=3, buff=0.08))
            return VGroup(frame, lease, context, scif, gate, revoke, arrows,
                          self.arrows_between(scif, revoke, [RESIDUAL] * len(revoke), dashed=True))
        if index == 7:
            frame = self.frame("RECORD · HANDLE · COMPARTMENT · TEST ≠ SECURITY", RED)
            kernel = self.panel("EXACT LEASE", AMBER, 2.7, 1.5).shift(LEFT * 3.3)
            proxies = self.pills(["RECORD", "HANDLE", "COMPARTMENT", "FINITE TEST"], [MUTED, BLUE, VIOLET, MUTED], x=2.2, y=0.9, width=2.2, scale=0.6)
            boundary = DashedLine(UP * 2.25, DOWN * 2.25, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, kernel, proxies, boundary, *[Cross(x, stroke_color=RED, stroke_width=2.5) for x in proxies])
        if index == 8:
            frame = self.frame("NUMBERED AUTHORITY-USE TRACE", AMBER)
            labels = ["1 REQUEST", "2 LEASE", "3 CONTEXT", "4 SCIF", "5 EFFECT", "6 RECEIPT"]
            nodes = VGroup(*[self.panel(name, [RED, AMBER, BLUE, VIOLET, GREEN, AMBER][i], 1.48, 0.9) for i, name in enumerate(labels)])
            nodes.arrange(RIGHT, buff=0.12).scale(0.9).shift(UP * 0.35)
            arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=AMBER, stroke_width=2.5, buff=0.04) for i in range(5)])
            return VGroup(frame, nodes, arrows, self.badge("TRACEABLE ROUTE", GREEN, 2.6).shift(DOWN * 1.35))
        if index == 9:
            frame = self.frame("FINITE LOCAL FIXTURES · COUNTS STAY BOUNDED", BLUE)
            counters = self.pills(["3/8 RECEIPTS", "2/6 SCIF", "6/7 BUDGET", "LOCAL ONLY"], [GREEN, GREEN, AMBER, MUTED], x=0.0, y=1.0, width=2.35, scale=0.68, direction=RIGHT)
            boundary = RoundedRectangle(width=10.4, height=2.3, corner_radius=0.18, stroke_color=BLUE, stroke_width=2, fill_opacity=0).shift(DOWN * 0.2)
            return VGroup(frame, boundary, counters, self.badge("SYNTHETIC TEST CORPUS", BLUE, 3.2).shift(DOWN * 1.45))
        if index == 10:
            frame = self.frame("FORMAL DECLARATIONS ≠ RELEASE OUTCOMES", AMBER)
            lean = self.panel("LEAN", BLUE, 2.25, 1.4).shift(LEFT * 3.7)
            decls = self.pills(["22 DECLARATIONS", "4 TARGETS"], [BLUE, BLUE], x=-3.6, y=-1.1, width=2.0, scale=0.62)
            releases = self.pills(["0/36 UNSAFE", "24/36 BASELINE", "2/36 USEFUL"], [GREEN, RED, RED], x=2.1, y=0.85, width=2.3, scale=0.63)
            divider = DashedLine(UP * 2.1, DOWN * 2.1, color=BOUNDARY, stroke_width=2)
            return VGroup(frame, lean, decls, releases, divider, *[Cross(releases[i], stroke_color=RED, stroke_width=2) for i in (1, 2)])
        if index == 11:
            frame = self.frame("32/36 ROLLBACK · DEPENDENCY DISCLOSED", RED)
            result = self.panel("32 / 36", GREEN, 2.65, 1.5).shift(LEFT * 3.0)
            roles = self.pills(["POLICY", "OBSERVER", "PROMOTION"], [AMBER, VIOLET, RED], x=1.9, y=0.85, width=2.2, scale=0.62)
            dependency = self.arrows_between(result, roles, [RED] * len(roles), dashed=True)
            return VGroup(frame, result, roles, dependency, self.badge("SAME-PROJECT DEPENDENCY", RESIDUAL, 3.3).shift(RIGHT * 2.7 + DOWN * 1.35))
        if index == 12:
            frame = self.frame("DATA ≠ AUTHORITY · CONFUSED DEPUTY", RED)
            channels = self.pills(["PROMPT", "ARTIFACT", "MEMORY", "TOOL OUTPUT", "MULTIMODAL", "AGENT"], [RED, RED, RED, RED, RESIDUAL, RED], x=-2.9, y=1.0, width=1.9, scale=0.55)
            lease = self.panel("AUTHORITY LEASE", AMBER, 2.55, 1.35).shift(LEFT * 0.1)
            deputy = self.panel("DEPUTY", RED, 2.2, 1.25).shift(RIGHT * 3.2 + UP * 0.35)
            target = self.badge("PRINCIPAL / TARGET CHANGED", RED, 3.2).shift(RIGHT * 2.9 + DOWN * 1.35)
            arrows = self.arrows_between(channels, [lease] * len(channels), [RED] * len(channels), dashed=True)
            return VGroup(frame, channels, lease, deputy, target, arrows, Cross(lease, stroke_color=RED, stroke_width=2.5),
                          Arrow(lease.get_right(), deputy.get_left(), color=RED, stroke_width=3, buff=0.08))
        if index == 13:
            frame = self.frame("LEASE TIME + CONTEXT SCOPE CAN FAIL", RED)
            timeline = self.pills(["VALID", "REPLAY", "STALE", "EXPIRED", "REVOKE FAILED"], [GREEN, RED, RED, RED, RESIDUAL], x=-2.5, y=1.0, width=1.75, scale=0.56, direction=RIGHT)
            packet = self.panel("CONTEXT PACKET", BLUE, 2.45, 1.3).shift(LEFT * 2.1 + DOWN * 0.9)
            spill = self.pills(["PROTECTED FACT", "IRRELEVANT FACT", "TOO BROAD"], [RED, RESIDUAL, RED], x=1.0, y=-1.0, width=2.2, scale=0.58)
            gate = self.panel("EFFECT GATE", VIOLET, 2.25, 1.3).shift(RIGHT * 3.35 + UP * 0.85)
            return VGroup(frame, timeline, packet, spill, gate, self.arrows_between(packet, spill, [RED] * len(spill)),
                          Arrow(timeline.get_right(), gate.get_left(), color=RED, stroke_width=3, buff=0.08),
                          *[Cross(x, stroke_color=RED, stroke_width=2) for x in spill])
        if index == 14:
            frame = self.frame("FAIL CLOSED · OWN THE RESIDUAL", RESIDUAL)
            source = self.panel("UNCERTAIN REQUEST", RED, 2.45, 1.3).shift(LEFT * 3.8)
            outcomes = self.pills(["STOP", "NARROW", "QUARANTINE", "COMPENSATE", "RETAIN RESIDUAL"], [RED, AMBER, VIOLET, AMBER, RESIDUAL], x=1.15, y=1.0, width=2.25, scale=0.58)
            owner = self.badge("OWNER + RECEIPT", RESIDUAL, 2.8).shift(RIGHT * 2.8 + DOWN * 1.4)
            return VGroup(frame, source, outcomes, owner, self.arrows_between(source, outcomes, [RED, AMBER, VIOLET, AMBER, RESIDUAL]))
        if index == 15:
            frame = self.frame("DESIGN RATIONALE · ARGUMENT SUPPORT", BLUE)
            local = self.panel("LOCAL CONTRACTS + TESTS", GREEN, 3.0, 1.5).shift(LEFT * 3.0)
            stamp = self.badge("SUPPORT STATE", AMBER, 2.3).shift(LEFT * 3.0 + DOWN * 1.35)
            targets = self.pills(["REAL-WORLD ENFORCEMENT", "USEFUL DEPLOYMENT", "TRANSFER", "PROOF TARGETS OPEN"], [RED, RED, RESIDUAL, MUTED], x=2.0, y=0.75, width=2.6, scale=0.55)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, stamp, targets, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in targets[:3]])
        if index == 16:
            frame = self.frame("FAIL-CLOSED AUTHORITY + CLEARANCE GATES", VIOLET)
            lease = self.panel("VALID LEASE", AMBER, 2.5, 1.3).shift(LEFT * 3.5)
            substitution = self.panel("SECRET SUBSTITUTION", RED, 2.45, 1.3).shift(LEFT * 0.45 + UP * 0.7)
            scif = self.panel("PROTECTED SCIF", VIOLET, 2.45, 1.3).shift(RIGHT * 2.8 + UP * 0.7)
            deny = self.pills(["UNAUTHORIZED BOUNDARY", "NO PERMISSION", "CLEARANCE TOO LOW"], [RED, RED, RED], x=0.5, y=-1.2, width=2.45, scale=0.58)
            return VGroup(frame, lease, substitution, scif, deny, Arrow(lease.get_right(), substitution.get_left(), color=AMBER, stroke_width=3, buff=0.08),
                          Arrow(substitution.get_right(), scif.get_left(), color=RED, stroke_width=3, buff=0.08),
                          *[Cross(x, stroke_color=RED, stroke_width=2.5) for x in deny])
        if index == 17:
            frame = self.frame("STRUCTURED AUTHORITY-USE REVIEW", AMBER)
            cases = self.pills(["MISSING HANDLE", "INACTIVE LEASE", "PROMPT INJECTION", "UNSANITIZED", "LEAK RISK", "REVOKE"], [RED, RED, RED, RED, RESIDUAL, AMBER], x=-3.0, y=1.0, width=1.9, scale=0.54)
            router = self.panel("REVIEW ROUTER", AMBER, 2.4, 1.4).shift(LEFT * 0.2)
            outcomes = self.pills(["DENY", "QUARANTINE", "SANITIZE", "REVOKE", "RETAIN", "CLEAN USE"], [RED, VIOLET, BLUE, AMBER, RESIDUAL, GREEN], x=2.7, y=0.95, width=1.8, scale=0.55)
            return VGroup(frame, cases, router, outcomes, self.arrows_between(router, outcomes, [RED, VIOLET, BLUE, AMBER, RESIDUAL, GREEN]), self.arrows_between(cases, [router] * len(cases), [RED] * len(cases), dashed=True))
        if index == 18:
            frame = self.frame("CLEAN AUTHORIZED USE · EFFECT MEDIATED", GREEN)
            scif = self.panel("SCIF", VIOLET, 2.25, 1.35).shift(LEFT * 3.4)
            gate = self.panel("EFFECT GATE", GREEN, 2.25, 1.35).shift(LEFT * 0.25)
            receipt = self.panel("RECEIPT SEALED", AMBER, 2.55, 1.35).shift(RIGHT * 2.8)
            invalid = self.pills(["DENY", "QUARANTINE", "REVOKE"], [RED, VIOLET, RESIDUAL], x=0.0, y=-1.25, width=1.9, scale=0.6, direction=RIGHT)
            return VGroup(frame, scif, gate, receipt, invalid,
                          Arrow(scif.get_right(), gate.get_left(), color=GREEN, stroke_width=3, buff=0.08),
                          Arrow(gate.get_right(), receipt.get_left(), color=AMBER, stroke_width=3, buff=0.08))
        if index == 19:
            frame = self.frame("LOCAL RECEIPT · NO MEDIA PROMOTION", RED)
            local = self.panel("LOCAL RECEIPT + MODEL", GREEN, 3.0, 1.5).shift(LEFT * 3.1)
            broad = self.pills(["IMPLEMENTATION PROOF", "USEFUL DEPLOYMENT", "REAL-WORLD ENFORCEMENT"], [RED, RED, RED], x=2.0, y=0.9, width=2.6, scale=0.58)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, broad, boundary, *[Cross(x, stroke_color=RED, stroke_width=2.5) for x in broad])
        if index == 20:
            frame = self.frame("SOURCE + DERIVATIVE · SAME EVIDENCE CEILING", BLUE)
            source = self.panel("LIVE CHAPTER", BLUE, 2.7, 1.4).shift(LEFT * 3.2)
            derivative = self.panel("VISUAL DERIVATIVE", AMBER, 2.7, 1.4).shift(RIGHT * 2.0)
            line = Arrow(source.get_right(), derivative.get_left(), color=BLUE, stroke_width=3, buff=0.1)
            ceiling = self.badge("SAME SUPPORT STATE", MUTED, 2.75).shift(DOWN * 1.45)
            return VGroup(frame, source, derivative, line, ceiling)
        if index == 21:
            frame = self.frame("DESIGN RATIONALE · NO BROAD RESULT", RED)
            support = self.panel("ARGUMENT SUPPORT", AMBER, 2.8, 1.5).shift(LEFT * 3.3)
            nonclaims = self.pills(["NO EMPIRICAL", "NO DEPLOYMENT", "NO SAFETY", "NO TRANSFER", "NO AGI / ASI"], [RED] * 5, x=1.7, y=0.85, width=2.1, scale=0.56)
            arrows = self.arrows_between(support, nonclaims, [RED] * len(nonclaims))
            return VGroup(frame, support, nonclaims, arrows, *[Cross(x, stroke_color=RED, stroke_width=2) for x in nonclaims])
        frame = self.frame("NEXT · ADVERSARIAL MACHINE LEARNING", AMBER)
        receipt = self.panel("SEALED AUTHORITY RECEIPT", GREEN, 3.0, 1.45).shift(LEFT * 3.5)
        artifact = self.panel("LEARNED ARTIFACT", VIOLET, 2.8, 1.45).shift(RIGHT * 1.9)
        attacks = self.pills(["TRAINING DATA", "INPUTS", "TRIGGERS", "ADAPTIVE ATTACKER"], [RED, RED, RESIDUAL, RED], x=2.2, y=-1.1, width=2.1, scale=0.56)
        boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
        return VGroup(frame, receipt, artifact, attacks, boundary,
                      Arrow(receipt.get_right(), artifact.get_left(), color=AMBER, stroke_width=3, buff=0.1),
                      self.arrows_between(artifact, attacks, [RED] * len(attacks), dashed=True))


__all__ = ["SecurityKernelDigitalScifsGeneration2"]
