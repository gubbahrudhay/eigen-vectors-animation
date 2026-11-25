"""Five-minute silent M3 film, made entirely with Manim Community.
Render: python -m manim -qh --fps 30 eigenvectors.py EigenFilm
Set STUDENT_NAME and STUDENT_ID in your environment before rendering.
"""
import os
import numpy as np
from manim import *

BG = "#000000"
GRID = "#376C9C"
GHOST = "#172535"
INK = "#F4F3F0"
MUTED = "#B5BDC6"
GOLD = "#FFD658"
BLUE = "#62C9ED"
MINT = "#87CEC1"
config.background_color = BG
ORIGIN = np.array([-3.28, -0.27, 0.0])
UNIT = 0.81
LIMIT = 3.65
MATRIX = np.array([[1., 2.], [2., 1.]])
BASIS = {"white": (1., 0.), "gold": (1., 1.), "blue": (1., -1.)}
COLORS = {"white": INK, "gold": GOLD, "blue": BLUE}


def pt(xy):
    return ORIGIN + UNIT * np.array([xy[0], xy[1], 0.])


def clipped_line(center, direction):
    """Intersect an infinite parametric line with the fixed square viewport."""
    lo, hi = -np.inf, np.inf
    for c, d in zip(center, direction):
        if abs(d) < 1e-8:
            if abs(c) > LIMIT:
                return None
        else:
            a, b = sorted(((-LIMIT-c)/d, (LIMIT-c)/d))
            lo, hi = max(lo, a), min(hi, b)
    if lo >= hi or not np.isfinite([lo, hi]).all():
        return None
    return pt(center + lo * direction), pt(center + hi * direction)


def lattice(mat, color, width, half_steps=False):
    lines = VGroup()
    for index in range(-8, 9):
        if half_steps and index % 2 == 0:
            continue
        k = index / 2 if half_steps else index
        for axis in range(2):
            direction = mat[:, axis]
            center = k * mat[:, 1-axis]
            segment = clipped_line(center, direction)
            if segment:
                lines.add(Line(*segment, color=color, stroke_width=width))
    return lines


def text_at(words, size, color, x, y, max_width, font="DejaVu Sans"):
    obj = Text(words, font=font, font_size=size, color=color)
    if obj.width > max_width:
        obj.scale_to_fit_width(max_width)
    return obj.move_to([x + obj.width/2, y, 0])


def vector(xy, color):
    # Construct the head anew so the blue arrow can collapse cleanly to zero.
    disp = pt(xy) - ORIGIN
    length = np.linalg.norm(disp)
    if length < 0.015:
        return VGroup(Dot(ORIGIN, radius=.035, color=color))
    unit = disp / length
    normal = np.array([-unit[1], unit[0], 0])
    head = min(.21, length*.45)
    tip = ORIGIN + disp
    base = tip - head*unit
    return VGroup(Line(ORIGIN, base, color=BG, stroke_width=8.0),
                  Line(ORIGIN, base, color=color, stroke_width=4.8),
                  Polygon(tip, base+.42*head*normal, base-.42*head*normal,
                          stroke_width=0, fill_color=color, fill_opacity=1))


class EigenFilm(Scene):
    def construct(self):
        self.clock = 0.
        self.phase = 0.
        self.trail_forward = True
        self.vectors = dict(BASIS)
        self.guides = list(BASIS)
        self.marks = False
        self.card = VGroup()
        self.header = VGroup()
        self.guidance = self.fixed_guides()
        self.graph = self.plot(0.)
        self.add(self.graph, self.guidance)
        name = os.getenv("STUDENT_NAME", "Sai Hrudhay")
        sid = os.getenv("STUDENT_ID", "[Student ID]")
        self.header = VGroup(text_at(f"{name}   ·   {sid}", 20, MINT, -6.5, 3.61, 12.8),
                             text_at("Eigenvectors and eigenvalues", 42, INK, -6.5, 3.06, 13, font="DejaVu Serif"))
        self.add(self.header)
        self.until(5)
        self.note("Four numbers → one?", [("A =  ⎡ 1   2 ⎤", INK), ("        ⎣ 2   1 ⎦", INK), ("Which two arrows?", GOLD)])
        self.until(12)
        self.flow(1, 4)
        self.select({"blue": BASIS["blue"]}, [], phase=1)
        self.pulse((1, -1), BLUE)
        self.until(25)
        self.pulse((-1, 1), BLUE)
        self.note("Did it turn?", [("Follow the tip back to its ring.", BLUE)])
        self.until(35)

        self.chapter("The replay", "Follow the blue tip")
        self.flow(0, 3)
        self.note("Start here", [("(1, −1)", BLUE)])
        self.flow(.5, 4)
        self.pulse((0, 0), BLUE)
        self.note("Freeze", [("Where will it emerge?", INK)])
        self.until(48)
        self.select({"blue": BASIS["blue"]}, ["blue"], phase=.5)
        self.until(53)
        self.flow(1, 4)
        self.pulse((-1, 1), BLUE)
        self.until(61)
        self.note("One number is enough", [("(1, −1)   →   (−1, 1)", BLUE), ("(−1, 1) = −1 × (1, −1)", BLUE)])
        self.until(70)

        self.chapter("Give each arrow a rail", "Test the clue")
        self.select({"white": BASIS["white"]}, ["white"], phase=0)
        self.note("White leaves its line", [("(1, 0)   →   (1, 2)", INK),
                                               ("Scaling alone keeps y at zero.", MUTED)])
        self.flow(1, 4)
        self.until(85)
        self.select({"gold": BASIS["gold"]}, ["gold"], phase=0, marks=True)
        self.note("Count the intervals", [("1 diagonal step  →  3 steps", GOLD),
                                             ("λ = 3", INK)])
        self.flow(1, 4)
        self.until(101)
        self.select({"blue": BASIS["blue"]}, ["blue"], phase=0)
        self.note("What number flips it?", [("Watch its distance", BLUE),
                                              ("from the origin.", BLUE)])
        self.flow(1, 4)
        self.until(114)
        self.note("λ = −1", [("Equal length. Opposite side.", BLUE)], formula=True)
        self.until(120)

        self.chapter("Ask the matrix where they went", "Reconstruct the endpoints")
        self.select(dict(BASIS), list(BASIS), phase=0)
        self.note("The transformation", [("A =  ⎡ 1   2 ⎤", INK),
                                            ("        ⎣ 2   1 ⎦", INK),
                                            ("(x, y)  →  (x + 2y, 2x + y)", MINT)])
        self.until(132)
        self.select({"gold": BASIS["gold"]}, ["gold"], phase=0)
        self.note("Gold   (1, 1)", [("x′ = 1(1) + 2(1) = 3", GOLD)])
        self.until(140)
        self.note("Gold   (1, 1)", [("x′ = 1(1) + 2(1) = 3", GOLD),
                                      ("y′ = 2(1) + 1(1) = 3", GOLD)])
        self.until(148)
        self.flow(1, 2)
        self.note("Gold   (1, 1)", [("(3, 3) = 3(1, 1)", GOLD), ("λ = 3", INK)])
        self.until(157)
        self.select({"blue": BASIS["blue"]}, ["blue"], phase=0)
        self.note("Blue   (1, −1)", [("x′ = 1(1) + 2(−1) = −1", BLUE)])
        self.until(166)
        self.note("Blue   (1, −1)", [("x′ = 1(1) + 2(−1) = −1", BLUE),
                                       ("y′ = 2(1) + 1(−1) = 1", BLUE)])
        self.until(174)
        self.flow(1, 3)
        self.note("Blue   (1, −1)", [("(−1, 1) = −1(1, −1)", BLUE),
                                       ("Both coordinates reverse sign.", MUTED)])
        self.until(178)
        self.note("Av = λv", [("v ≠ 0    eigenvector", INK), ("λ           eigenvalue", GOLD)], formula=True)
        self.until(188)
        self.select({"white": BASIS["white"]}, ["white"], phase=0)
        self.note("White   (1, 0)", [("(1, 0)  →  (1, 2)", INK),
                                       ("λ · 0 cannot equal 2.", MUTED)])
        self.flow(1, 3)
        self.until(200)

        self.chapter("What if we start halfway?", "From one arrow to a whole line")
        self.select({"gold": (.5, .5)}, ["gold"], phase=0, marks=True)
        self.note("Choose a landing point", [("Start   (½, ½)", GOLD),
                                                ("(1, 1)     (1½, 1½)     (3, 3)", INK)])
        targets = VGroup(*(Circle(radius=.095, stroke_width=2.2, color=GOLD)
                           .move_to(pt((k, k))) for k in (1., 1.5, 3.))).set_z_index(5)
        self.act(Create(targets), seconds=.8)
        self.until(214)
        self.flow(1, 4)
        self.pulse((1.5, 1.5), GOLD)
        self.remove(targets)
        self.note("Half the input", [("(½, ½)   →   (1½, 1½)", GOLD),
                                       ("A(½v) = ½Av", INK)])
        self.until(233)
        self.select({"gold": (-.7, -.7)}, ["gold"], phase=0)
        self.note("Start on the other side", [("The factor is still 3.", GOLD)])
        self.until(239)
        self.flow(1, 4)
        self.until(248)
        self.select({"gold": BASIS["gold"], "blue": BASIS["blue"]},
                    ["gold", "blue"], phase=0)
        self.note("Two invariant lines", [("y = x      λ = 3", GOLD),
                                            ("y = −x    λ = −1", BLUE),
                                            ("A(cv) = cAv = λ(cv)", INK)])
        self.flow(1, 4)
        self.select({}, ["gold", "blue"], phase=1)
        self.until(265)

        self.chapter("Which arrows stayed on their lines?", "The answer")
        self.select(dict(BASIS), list(BASIS), phase=0)
        self.note("Watch once more", [("White", INK), ("Gold", GOLD), ("Blue", BLUE)])
        self.until(270)
        self.flow(1, 4)
        self.note("Four entries, one multiplier", [("Gold stretches by 3.", GOLD),
                                         ("Blue flips with the same length.", BLUE)])
        self.until(277)
        self.note("Three takeaways", [("01     Av = λv,   v ≠ 0", INK),
                                        ("02     |λ| scales the length.", GOLD),
                                        ("03     λ < 0 reverses the arrow.", BLUE)])
        self.until(288)
        self.pulse((1, -1), BLUE)
        self.pulse((-1, 1), BLUE)
        self.until(291)
        credits = VGroup(
            text_at("References & production", 18, MINT, .5, -1.65, 6),
            text_at("Graduate ML  ·  question-led opening", 17, MUTED, .5, -2.03, 6),
            text_at("3Blue1Brown  ·  Visual inspiration", 17, MUTED, .5, -2.38, 6),
            text_at("Manim Community  ·  animation", 17, MUTED, .5, -2.73, 6),
            text_at("ChatGPT  ·  script and code assistance", 17, MUTED, .5, -3.08, 6))
        self.act(FadeIn(credits), seconds=.6)
        self.until(300)

    def pulse(self, xy, color):
        self.act(Flash(pt(xy), color=color, flash_radius=.21, line_length=.095), seconds=.8)

    def act(self, *animations, seconds):
        self.play(*animations, run_time=seconds)
        self.clock += seconds

    def until(self, deadline):
        remaining = deadline - self.clock
        if remaining < -1e-6:
            raise ValueError(f"Missed cue at {deadline}s")
        if remaining > 1e-6:
            self.wait(remaining)
        self.clock = deadline

    def chapter(self, title, subtitle):
        new = VGroup(text_at(subtitle.upper(), 17, MINT, -6.5, 3.61, 12.8),
                     text_at(title, 42, INK, -6.5, 3.06, 13, font="DejaVu Serif"))
        self.remove(self.header)
        self.header = new
        self.act(FadeIn(new), seconds=.6)

    def note(self, title, rows, formula=False):
        new = VGroup(text_at(title, 49 if formula else 32, GOLD if formula else INK, .5, 1.96, 6.1, font="DejaVu Serif"))
        for i, (words, color) in enumerate(rows):
            new.add(text_at(words, 24, color, .53, 1.10-i*.69, 6.0))
        self.remove(self.card)
        self.card = new
        self.act(LaggedStart(*(FadeIn(line, shift=.06*UP) for line in new),
                             lag_ratio=.12), seconds=.6)
        self.remove(*new.submobjects)
        self.add(new)

    def select(self, vectors, guides, phase=None, marks=False):
        self.vectors, self.guides, self.marks = vectors, guides, marks
        if phase is not None:
            self.phase = phase
        self.remove(self.graph, self.guidance)
        self.guidance = self.fixed_guides()
        self.graph = self.plot(self.phase)
        self.add(self.graph, self.guidance)

    def fixed_guides(self):
        # Separate layers keep guides still while the blue lattice deforms.
        g = VGroup(lattice(np.eye(2), GHOST, .85).set_z_index(-4))
        for d in (np.array([1, 0]), np.array([0, 1])):
            g.add(Line(pt(-LIMIT*d), pt(LIMIT*d), stroke_width=1.8, color="#9099A3").set_z_index(-1))
        for key in self.guides:
            d = np.asarray(BASIS[key])
            g.add(DashedLine(pt(-LIMIT*d), pt(LIMIT*d), dash_length=.16,
                             dashed_ratio=.52, stroke_width=2.1, color=COLORS[key],
                             stroke_opacity=.67).set_z_index(0))
        if self.marks:
            ticks = (.5, 1, 1.5, 2, 3) if self.vectors.get("gold") == (.5, .5) else (1, 2, 3)
            for k in ticks:
                p = pt((k, k))
                g.add(Line(p+[-.07,.07,0], p+[.07,-.07,0],
                           stroke_width=2.6, color=GOLD))
        for key, xy in self.vectors.items():
            g.add(Circle(radius=.084, stroke_width=2, color=COLORS[key])
                  .move_to(pt(xy)).set_z_index(3))
        return g

    def plot(self, t):
        mat = (1-t)*np.eye(2) + t*MATRIX
        # An outlined unit cell makes the moving grid traceable through collapse.
        corners = [pt(mat @ q) for q in ((0,0), (1,0), (1,1), (0,1))]
        cell = Polygon(*corners, fill_color=GRID, fill_opacity=.10,
                       stroke_color=GRID, stroke_opacity=.85, stroke_width=2.0)
        g = VGroup(lattice(mat, "#19364D", .72, half_steps=True).set_z_index(-3),
                   lattice(mat, GRID, 1.45).set_z_index(-3), cell.set_z_index(-2))
        for key, xy in self.vectors.items():
            start = np.asarray(xy)
            tip = mat @ start
            # A short fading trail follows the tip along its true trajectory.
            if 0 < t < 1:
                prior = max(0., t-.20) if self.trail_forward else min(1., t+.20)
                tail = ((1-prior)*np.eye(2) + prior*MATRIX) @ start
                for i in range(4):
                    u, v = i/4, (i+1)/4
                    g.add(Line(pt((1-u)*tail+u*tip), pt((1-v)*tail+v*tip),
                               stroke_color=COLORS[key], stroke_width=2.7,
                               stroke_opacity=.12+.13*i).set_z_index(1))
            g.add(vector(tip, COLORS[key]).set_z_index(2))
        g.add(Dot(ORIGIN, radius=.042, color=INK).set_z_index(4))
        return g

    def flow(self, target, seconds):
        start = self.phase
        self.trail_forward = target >= start
        def update(group, alpha):
            frame = self.plot(start + (target-start)*alpha)
            group.remove(*group.submobjects)
            group.add(*frame.submobjects)
        self.act(UpdateFromAlphaFunc(self.graph, update, rate_func=smooth), seconds=seconds)
        self.phase = target

    def setup(self):
        super().setup()
        # Axis labels belong to the fixed observation grid.
        self.add(text_at("x", 17, MUTED, -.43, -.45, .28),
                 text_at("y", 17, MUTED, -3.53, 2.54, .28))
