"""Generation-2 visual abstract for Capability Replacement and Rollback.

The visual world is a transaction-control desk.  A prior route, candidate,
full-state/effect inventory, monitor, recovery path, and terminal receipt stay
visible as the chapter moves from prospective authorization to bounded
evidence and residual ownership.  The scene is an explanatory derivative; it
does not promote the chapter's support state.
"""

from __future__ import annotations

from manim import (
    AnimationGroup, Arrow, Create, Cross, DashedLine, FadeIn, FadeOut, GrowArrow, Indicate,
    LEFT, RIGHT, RoundedRectangle, Text, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import (
    BOUNDARY, INK, MUTED, RESIDUAL, ROLLBACK, SURFACE, AsiScene, text,
)


GOLD = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class CapabilityReplacementRollbackGeneration2(AsiScene):
    """A synchronized 05:18 visual explanation of the replacement transaction."""

    TARGET_DURATION = 318.17
    ENDS = [
        15.875, 28.92, 40.315, 58.07, 72.115, 83.76, 96.59, 115.235,
        128.88, 147.61, 164.955, 173.6, 192.23, 197.7, 214.945, 220.465,
        236.595, 248.09, 263.735, 271.53, 282.16, 294.955, 307.275, 318.17,
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
            # Scene changes are punctuation, not the beat itself.  Keep a
            # single fade/transition short so the chapter holds a legible
            # settled state for most of the narration window.
            per_animation = min(1.25, action_budget) if len(animations) == 1 else max(0.08, action_budget / len(animations))
            for animation in animations:
                self.play(animation, run_time=per_animation)
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 17, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 2.2, height: float = 0.48) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.1, stroke_color=color,
            stroke_width=2.5, fill_color=SURFACE, fill_opacity=1,
        )
        caption = self.label(value, 12, color, "BOLD")
        if caption.width > width - 0.18:
            caption.scale_to_fit_width(width - 0.18)
        caption.move_to(shell)
        return VGroup(shell, caption)

    def panel(self, title: str, color: str, width: float = 2.5, height: float = 1.3) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.16, stroke_color=color,
            stroke_width=3, fill_color=DEEP, fill_opacity=1,
        )
        title_obj = self.badge(title, color, min(width - 0.16, 3.5), 0.4).scale(0.82)
        title_obj.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, title_obj)

    def frame(self, title: str, color: str = GOLD) -> VGroup:
        shell = RoundedRectangle(
            width=11.7, height=6.2, corner_radius=0.2, stroke_color=BOUNDARY,
            stroke_width=2, fill_color="#0F2029", fill_opacity=1,
        )
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
        for index in range(1, 25):
            next_scene = self.scene_for(index)
            animations = [FadeIn(next_scene)] if not self.current else [
                AnimationGroup(FadeOut(self.current), FadeIn(next_scene), lag_ratio=0)
            ]
            self.play_beat(index, *animations, settle=0.85 if index in (1, 10, 23, 24) else 0.55)
            self.current = next_scene

    def scene_for(self, index: int) -> VGroup:
        if index == 1:
            frame = self.frame("NOT A LIGHT BULB · FULL ATTACHED WORLD", RED)
            prior = self.panel("PRIOR ROUTE A", BLUE, 2.35, 1.35).shift(LEFT * 3.95 + UP * 0.5)
            tags = self.pills(["WEIGHTS", "OPTIMIZER", "SCHEDULER", "RNG", "CACHE", "BACKUP"],
                              [BLUE, GOLD, GOLD, VIOLET, BLUE, MUTED], x=-0.9, y=0.65, width=1.7, scale=0.61)
            effects = self.pills(["CREDENTIALS", "POLICY", "DESCENDANT", "COMMITMENT", "EXTERNAL EFFECT"],
                                 [RED, GOLD, RESIDUAL, RESIDUAL, RED], x=2.7, y=0.45, width=2.2, scale=0.59)
            links = VGroup(*[Arrow(prior.get_right(), tags[i].get_left(), color=BLUE, stroke_width=2, buff=0.08) for i in range(len(tags))])
            links.add(*[Arrow(tags.get_right(), effects[i].get_left(), color=RED, stroke_width=2, buff=0.08) for i in range(len(effects))])
            return VGroup(frame, prior, tags, effects, links)
        if index == 2:
            frame = self.frame("SUCCESS? · OLD STATE REMAINS", RED)
            old = self.panel("OLD CUSTODY", BLUE, 2.55, 1.35).shift(LEFT * 3.25 + UP * 0.65)
            new = self.panel("CANDIDATE B", GREEN, 2.55, 1.35).shift(RIGHT * 0.15 + UP * 0.65)
            badge = self.badge("VISIBLE SUCCESS", GREEN, 2.6).shift(RIGHT * 3.5 + UP * 1.1)
            stranded = self.pills(["CACHE", "DESCENDANT", "REMOTE COPY"], [RED, RESIDUAL, RED], x=2.8, y=-0.65, width=2.1, scale=0.66)
            arrow = Arrow(old.get_right(), new.get_left(), color=GOLD, stroke_width=3, buff=0.1)
            cross = Cross(stranded[1], stroke_color=RED, stroke_width=2.5)
            return VGroup(frame, old, new, badge, stranded, arrow, cross)
        if index == 3:
            frame = self.frame("TRANSACTION RECORD · BEFORE THE RESULT", GOLD)
            desk = self.panel("GOVERNED TRANSACTION", GOLD, 3.25, 1.55).shift(LEFT * 2.25)
            fields = self.pills(["PRIOR", "CANDIDATE", "CONSUMERS", "AUTHORITY", "EVIDENCE", "RECOVERY OBJECTIVE"],
                                [BLUE, GREEN, VIOLET, RED, BLUE, GOLD], x=2.1, y=0.85, width=2.15, scale=0.58)
            links = self.arrows_between(desk, fields, [BLUE, GREEN, VIOLET, RED, BLUE, GOLD])
            pre = self.badge("NO RESULT YET", MUTED, 2.1).shift(LEFT * 2.25 + DOWN * 1.55)
            return VGroup(frame, desk, fields, links, pre)
        if index == 4:
            frame = self.frame("FREEZE BEFORE OUTCOMES", GOLD)
            lock = self.panel("PROSPECTIVE LOCK", GOLD, 2.9, 1.45).shift(LEFT * 3.45 + UP * 0.75)
            rules = self.pills(["DIGESTS", "DEPENDENCY GRAPH", "CHECKPOINT", "EVALUATOR", "MONITOR", "CANARY SCOPE", "THRESHOLDS", "OWNER + EXPIRY"],
                               [BLUE, BLUE, GOLD, VIOLET, VIOLET, GOLD, RED, RESIDUAL], x=1.3, y=1.0, width=2.0, scale=0.56)
            inventory = self.badge("THEN INVENTORY STATE + EFFECTS", BLUE, 3.6).shift(LEFT * 2.25 + DOWN * 1.55)
            return VGroup(frame, lock, rules, inventory, self.arrows_between(lock, rules, [GOLD] * len(rules)))
        if index == 5:
            frame = self.frame("WEIGHTS ≠ WORLD", BLUE)
            title = self.panel("FULL INVENTORY", BLUE, 2.5, 1.3).shift(LEFT * 4.0)
            rows = self.pills(["MODEL PARAMETERS", "OPTIMIZER", "SCHEDULER", "RNG", "CACHE", "BACKUP", "CREDENTIAL", "POLICY", "RECEIPT", "DATA", "ROUTE", "MONITOR", "DESCENDANT", "COMMITMENT"],
                              [BLUE, GOLD, GOLD, VIOLET, BLUE, MUTED, RED, GOLD, VIOLET, BLUE, GREEN, VIOLET, RESIDUAL, RED],
                              x=1.15, y=1.1, width=1.55, scale=0.52)
            return VGroup(frame, title, rows, self.arrows_between(title, rows, [BLUE, GOLD, VIOLET, RED] * 4))
        if index == 6:
            frame = self.frame("EFFECT CLASSES · OMITTED ≠ RECOVERED", RED)
            source = self.panel("EFFECT INVENTORY", BLUE, 2.55, 1.3).shift(LEFT * 4.1)
            bins = self.pills(["REVERSIBLE", "REPLAYABLE", "COMPENSATABLE", "FORKED", "DISCLOSURE", "EXTERNAL", "IRREVERSIBLE"],
                              [GREEN, BLUE, GOLD, VIOLET, RED, RESIDUAL, RED], x=0.9, y=1.05, width=2.0, scale=0.56)
            omitted = self.badge("OMITTED · UNRECOVERED", RESIDUAL, 2.9).shift(RIGHT * 3.9 + DOWN * 1.65)
            return VGroup(frame, source, bins, omitted, self.arrows_between(source, bins, [GREEN, BLUE, GOLD, VIOLET, RED, RESIDUAL, RED]), Cross(omitted, stroke_color=RED, stroke_width=2.5))
        if index == 7:
            frame = self.frame("PHASE-GATED LIFECYCLE", GOLD)
            labels = ["PROPOSED", "PRECHECK", "SHADOW", "CANARY", "COMMIT", "MONITOR"]
            nodes = VGroup(*[self.panel(label, [GOLD, BLUE, BLUE, VIOLET, GREEN, RED][i], 1.45, 0.9) for i, label in enumerate(labels)])
            nodes.arrange(RIGHT, buff=0.15).scale(0.91).shift(UP * 0.55)
            arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=GOLD, stroke_width=2.5, buff=0.05) for i in range(len(nodes) - 1)])
            terminals = self.pills(["ROLLBACK", "COMPENSATE", "QUARANTINE", "RETIRED"], [RED, GOLD, RESIDUAL, MUTED], x=0.0, y=-1.35, width=2.1, scale=0.64, direction=RIGHT)
            branches = VGroup(*[DashedLine(nodes[i].get_bottom(), terminals[min(i, 3)].get_top(), color=RED if i < 2 else RESIDUAL, stroke_width=2) for i in range(4)])
            return VGroup(frame, nodes, arrows, terminals, branches)
        if index == 8:
            frame = self.frame("BOUNDED CANARY · QUALIFICATION GATES", VIOLET)
            canary = self.panel("5% ROUTE B", VIOLET, 2.2, 1.35).shift(LEFT * 2.4)
            boundary = RoundedRectangle(width=4.2, height=2.25, corner_radius=0.2, stroke_color=BOUNDARY, stroke_width=2, fill_opacity=0).move_to(canary.get_center())
            gates = self.pills(["USEFULNESS", "REGRESSIONS", "ADVERSARIAL", "AUTHORITY", "STATE", "COST", "TRANSFER"],
                               [GREEN, RED, RED, GOLD, BLUE, MUTED, VIOLET], x=2.15, y=1.0, width=1.8, scale=0.56)
            return VGroup(frame, boundary, canary, gates, self.arrows_between(canary, gates, [VIOLET] * len(gates)))
        if index == 9:
            frame = self.frame("INDEPENDENCE IS MEASURED, NOT LABELED", RED)
            candidate = self.panel("CANDIDATE", BLUE, 2.25, 1.25).shift(LEFT * 3.6)
            roles = self.pills(["PROPOSER", "EVALUATOR", "PROMOTER", "MONITOR", "INCIDENT JUDGE", "ROLLBACK AUTHORITY"],
                               [GOLD, VIOLET, GREEN, VIOLET, RED, RED], x=1.0, y=0.75, width=2.2, scale=0.56)
            loop = self.arrows_between(candidate, roles, [RED] * len(roles))
            breach = self.badge("SELF-APPROVAL LOOP", RED, 2.8).shift(RIGHT * 3.6 + DOWN * 1.6)
            return VGroup(frame, candidate, roles, loop, Cross(roles[1], stroke_color=RED, stroke_width=2.5), breach)
        if index == 10:
            frame = self.frame("ROUTE A → 5% ROUTE B CANARY", GOLD)
            a = self.panel("95% A DEFAULT", BLUE, 2.3, 1.35).shift(LEFT * 3.85 + UP * 0.75)
            b = self.panel("5% B CANARY", VIOLET, 2.3, 1.35).shift(LEFT * 0.7 + UP * 0.75)
            monitor = self.panel("CRITICAL REGRESSION", RED, 2.55, 1.35).shift(RIGHT * 2.65 + UP * 0.75)
            blocked = self.pills(["DESCENDANT: BLOCKED", "DEFAULT CACHE: BLOCKED"], [RESIDUAL, RED], x=-0.6, y=-1.1, width=2.8, scale=0.65)
            paths = VGroup(Arrow(a.get_right(), b.get_left(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(b.get_right(), monitor.get_left(), color=RED, stroke_width=3, buff=0.1))
            stop = Cross(monitor, stroke_color=RED, stroke_width=3)
            return VGroup(frame, a, b, monitor, blocked, paths, stop)
        if index == 11:
            frame = self.frame("RESTORE STATE · COMPENSATE REMOTE EFFECT", GREEN)
            restored = self.panel("ROUTE A RESTORED", GREEN, 2.65, 1.35).shift(LEFT * 3.8 + UP * 0.6)
            compare = self.panel("COMPARE ALL SURFACES", BLUE, 2.75, 1.35).shift(LEFT * 0.3 + UP * 0.6)
            remote = self.panel("REMOTE COPY", RED, 2.3, 1.35).shift(RIGHT * 3.3 + UP * 0.6)
            owner = self.badge("COMPENSATE + OWNER", RESIDUAL, 2.8).shift(RIGHT * 3.2 + DOWN * 1.25)
            return VGroup(frame, restored, compare, remote, owner, Arrow(restored.get_right(), compare.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(compare.get_right(), remote.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(remote.get_bottom(), owner.get_top(), color=RESIDUAL, stroke_width=2.5, buff=0.08))
        if index == 12:
            frame = self.frame("TERMINAL RECEIPT · FAILURE STAYS VISIBLE", GOLD)
            receipt = self.panel("TERMINAL RECEIPT", GOLD, 3.1, 1.65).shift(LEFT * 2.25)
            fields = self.pills(["FAILED B", "ROLLBACK", "EXTERNAL EFFECT", "DESCENDANTS", "COST", "OWNER"], [RED, GREEN, RED, RESIDUAL, MUTED, GOLD], x=2.05, y=0.8, width=2.1, scale=0.59)
            return VGroup(frame, receipt, fields, self.arrows_between(receipt, fields, [RED, GREEN, RED, RESIDUAL, MUTED, GOLD]))
        if index == 13:
            frame = self.frame("RECOVERY IS A VECTOR, NOT A BOOLEAN", BLUE)
            pairs = [("BYTES", "STATE"), ("RESTART", "BEHAVIOR"), ("DIGEST", "PRIVACY"), ("COMPENSATE", "REVERSAL"), ("RECEIPT", "OBSERVER"), ("LOCAL", "COMPLETE")]
            rows = VGroup(*[VGroup(self.label(a, 18, INK, "BOLD"), self.label("≠", 29, RED, "BOLD"), self.label(b, 18, MUTED, "BOLD")).arrange(RIGHT, buff=0.32) for a, b in pairs])
            rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT).shift(LEFT * 2.1 + DOWN * 0.05)
            scope = self.badge("DISTINCT RECOVERY DIMENSIONS", GOLD, 3.6).shift(RIGHT * 2.7 + DOWN * 1.55)
            return VGroup(frame, rows, scope)
        if index == 14:
            frame = self.frame("EXACT LOCAL ≠ COMPLETE SCOPE", RED)
            local = self.panel("EXACT LOCAL INVENTORY", GREEN, 3.0, 1.6).shift(LEFT * 2.7)
            outside = self.pills(["REMOTE", "DESCENDANT", "IMMUTABLE CORPUS"], [RED, RESIDUAL, MUTED], x=2.35, y=0.65, width=2.3, scale=0.63)
            boundary = DashedLine(UP * 2.25, DOWN * 2.25, color=RED, stroke_width=3).shift(RIGHT * 0.1)
            crosses = VGroup(*[Cross(item, stroke_color=RED, stroke_width=2.5) for item in outside])
            return VGroup(frame, local, outside, boundary, crosses)
        if index == 15:
            frame = self.frame("ROLLBACK ATTACK SURFACE", RED)
            names = ["HINDSIGHT", "REGRESSION DELETE", "EVALUATOR CAPTURE", "CANARY CONTAMINATION", "MONITOR BLINDNESS", "PARTIAL COMMIT", "AUTHORITY SMUGGLING", "ROLLBACK THEATER"]
            chain = self.pills(names, [RED, RESIDUAL, RED, VIOLET, RED, GOLD, RED, RESIDUAL], x=0.3, y=1.05, width=2.15, scale=0.54)
            arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), color=RED, stroke_width=2, buff=0.05) for i in range(len(chain) - 1)])
            return VGroup(frame, chain, arrows)
        if index == 16:
            frame = self.frame("PROMOTE → ROLLBACK · COST ACCUMULATES", RESIDUAL)
            loop = self.panel("PROMOTE / ROLLBACK", GOLD, 3.0, 1.45).shift(LEFT * 2.15)
            arrows = VGroup(Arrow(loop.get_right(), loop.get_left(), color=ROLLBACK, stroke_width=3, buff=0.15))
            ledger = self.pills(["COST 1", "COST 2", "COST 3", "RESIDUALS REMAIN"], [MUTED, MUTED, MUTED, RESIDUAL], x=2.4, y=0.65, width=2.2, scale=0.65)
            return VGroup(frame, loop, arrows, ledger)
        if index == 17:
            frame = self.frame("15 / 15 EXACT LOCAL · 6 CHECKPOINT DISAGREEMENTS", BLUE)
            exact = self.panel("15 / 15", GREEN, 2.4, 1.55).shift(LEFT * 3.1)
            exact_note = self.badge("DECLARED TREES", GREEN, 2.0).next_to(exact, DOWN, buff=0.25)
            disagreement = self.panel("6 DISAGREEMENTS", RED, 2.75, 1.55).shift(RIGHT * 1.05)
            auth = self.badge("FIX AUTHORITY IN ADVANCE", GOLD, 3.1).shift(RIGHT * 3.55 + DOWN * 1.4)
            return VGroup(frame, exact, exact_note, disagreement, auth, Arrow(exact.get_right(), disagreement.get_left(), color=RED, stroke_width=2.5, buff=0.1))
        if index == 18:
            frame = self.frame("32 / 36 ROLLBACK · 2 / 36 USEFUL RELEASE", RED)
            rollback = self.panel("32 / 36", GREEN, 2.6, 1.5).shift(LEFT * 2.9)
            useful = self.panel("2 / 36", RED, 2.6, 1.5).shift(RIGHT * 0.6)
            gate = self.badge("RELEASE GATE FAILED", RED, 3.0).shift(RIGHT * 3.25 + DOWN * 1.35)
            return VGroup(frame, rollback, useful, gate, Cross(gate, stroke_color=RED, stroke_width=3), Arrow(rollback.get_right(), useful.get_left(), color=GOLD, stroke_width=3, buff=0.1))
        if index == 19:
            frame = self.frame("35 / 35 NAMED LOCAL · OUTSIDE SURFACES UNRESOLVED", BLUE)
            local = self.panel("35 / 35", GREEN, 2.4, 1.55).shift(LEFT * 2.9)
            local_note = self.badge("NAMED LOCAL SURFACES", GREEN, 2.7).next_to(local, DOWN, buff=0.25)
            unresolved = self.pills(["IMMUTABLE CORPUS", "RAW EVIDENCE", "SIMULATED REMOTE", "EXTERNAL DESCENDANT"], [MUTED, RED, RED, RESIDUAL], x=2.4, y=0.9, width=2.35, scale=0.58)
            return VGroup(frame, local, local_note, unresolved, self.arrows_between(local, unresolved, [RESIDUAL] * len(unresolved)), *[Cross(x, stroke_color=RED, stroke_width=2) for x in unresolved])
        if index == 20:
            frame = self.frame("BOUNDED DISCIPLINE · NO BROAD PROMOTION", GOLD)
            evidence = self.panel("RECORD + RECOVERY DISCIPLINE", GREEN, 3.25, 1.65).shift(LEFT * 2.65)
            claims = self.pills(["PRODUCTION USEFULNESS", "EFFECT-COMPLETE ROLLBACK"], [RED, RED], x=2.55, y=0.45, width=2.7, scale=0.66)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, evidence, claims, boundary, *[Cross(x, stroke_color=RED, stroke_width=2.5) for x in claims])
        if index == 21:
            frame = self.frame("DESIGN RATIONALE · ARGUMENT SUPPORT", BLUE)
            support = self.panel("SUPPORT STATE", GOLD, 2.75, 1.55).shift(LEFT * 3.4)
            arrow = Arrow(support.get_right(), RIGHT * 1.9, color=GOLD, stroke_width=3, buff=0.1)
            narrow = self.badge("BOUNDED LOCAL NON-CORE GOVERNANCE", GREEN, 3.7).shift(RIGHT * 2.6)
            open_targets = self.pills(["REFINEMENT", "TRANSFER", "INDEPENDENCE", "ROLLBACK"], [MUTED, RED, RED, RESIDUAL], x=0.3, y=-1.15, width=1.9, scale=0.58)
            return VGroup(frame, support, arrow, narrow, open_targets, *[DashedLine(support.get_bottom(), x.get_top(), color=MUTED, stroke_width=2) for x in open_targets])
        if index == 22:
            frame = self.frame("NONCLAIMS STAY OUTSIDE THE FIELD", RED)
            core = self.panel("BOUNDED LOCAL EVIDENCE", GREEN, 2.9, 1.55).shift(LEFT * 3.5)
            nonclaims = self.pills(["USEFUL REPLACEMENT", "TRANSFER", "PRIVACY ERASURE", "INDEPENDENT EVALUATOR", "RSI PROMOTION"], [RED, RED, RED, RED, RED], x=1.65, y=0.9, width=2.5, scale=0.55)
            arrows = self.arrows_between(core, nonclaims, [RED] * len(nonclaims))
            return VGroup(frame, core, nonclaims, arrows, *[Cross(x, stroke_color=RED, stroke_width=2.5) for x in nonclaims])
        if index == 23:
            frame = self.frame("COMPLETE TRANSACTION CHECKLIST", GOLD)
            desk = self.panel("TERMINAL DISPOSITION", GREEN, 2.8, 1.55).shift(LEFT * 2.7)
            checklist = self.pills(["IDENTITY", "EVIDENCE", "STATE", "EFFECTS", "AUTHORITY", "RECOVERY", "RESIDUALS", "DESCENDANTS", "TERMINAL"],
                                   [BLUE, BLUE, GOLD, RED, VIOLET, GREEN, RESIDUAL, RESIDUAL, GREEN], x=1.8, y=1.05, width=1.7, scale=0.53)
            return VGroup(frame, desk, checklist, self.arrows_between(desk, checklist, [GOLD] * len(checklist)))
        frame = self.frame("NEXT · SECURITY KERNEL AND DIGITAL SCIFS", GOLD)
        receipt = self.panel("CLOSED RECEIPT", GREEN, 2.9, 1.55).shift(LEFT * 3.5)
        chamber = self.panel("PRIVILEGED EXECUTION", VIOLET, 3.05, 1.55).shift(RIGHT * 2.0)
        handoff = Arrow(receipt.get_right(), chamber.get_left(), color=GOLD, stroke_width=3, buff=0.1)
        boundary = self.badge("ISOLATE + ENFORCE", VIOLET, 2.7).shift(RIGHT * 3.55 + DOWN * 1.35)
        return VGroup(frame, receipt, chamber, handoff, boundary)


__all__ = ["CapabilityReplacementRollbackGeneration2"]
