from manim import *

# --------------------------------------------------
# Global styling & utilities
# --------------------------------------------------
config.background_color = "#1e1e1e"

TITLE_FONT_SIZE = 48
EQ_FONT_SIZE = 36
BANNER_OPACITY = 0.15

def banner(title: str) -> VGroup:
    """Top semi-transparent blue banner with the step title."""
    rect = Rectangle(
        width=config.frame_width,
        height=0.8,
        fill_color=BLUE_E,
        stroke_width=0,
        fill_opacity=BANNER_OPACITY,
    ).to_edge(UP)
    txt = Text(title, font_size=TITLE_FONT_SIZE, color=WHITE).move_to(rect)
    return VGroup(rect, txt)

def circumscribe(mob, scene: Scene, color=YELLOW, run_time=1):
    """Quick helper to call Circumscribe then wait."""
    scene.play(Circumscribe(mob, color=color, run_time=run_time))
    scene.wait(0.5)

# --------------------------------------------------
# Step 1 – Analyse the problem
# --------------------------------------------------
class Step1(Scene):
    def construct(self):
        self.add(banner("Step 1  –  Analyse the problem"))

        integral = MathTex(
            r"\displaystyle \int_{0}^{\pi/8} x\,\sin(2x)\,dx",
            font_size=EQ_FONT_SIZE,
            color=WHITE,
        ).shift(UP * 1)
        bullets = Tex(
            r"""
            \begin{align*}
            &\textbf{Givens: } 0 \le x \le \pi/8 \\
            &\textbf{Tool: } \text{Integration by parts} \\
            &\textbf{Goal: } \text{Evaluate definite integral}
            \end{align*}
            """,
            font_size=30,
            color=WHITE,
        ).next_to(integral, DOWN, buff=0.8)

        self.play(FadeIn(integral))
        circumscribe(integral, self)

        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT) for line in bullets]), lag_ratio=0.25)
        self.wait(1)
        self.wait(0.5)  # final pause

# --------------------------------------------------
# Step 2 – Choose u and dv
# --------------------------------------------------
class Step2(Scene):
    def construct(self):
        self.add(banner("Step 2  –  Choose $u$ and $dv$"))

        integral = MathTex(
            r"\int_{0}^{\pi/8} x\,\sin(2x)\,dx",
            font_size=EQ_FONT_SIZE,
        ).to_edge(UP, buff=1.2)

        choice = MathTex(
            r"u = x,\quad dv = \sin(2x)\,dx",
            font_size=EQ_FONT_SIZE,
        ).next_to(integral, DOWN, buff=1)

        # Highlight parts
        u_highlight = choice[0:3]      # "u = x"
        dv_highlight = choice[3:]      # "dv = ..."
        u_highlight.set_color(YELLOW)
        dv_highlight.set_color(ORANGE)

        self.play(FadeIn(integral))
        self.play(TransformFromCopy(integral, choice))
        circumscribe(u_highlight, self, color=YELLOW)
        circumscribe(dv_highlight, self, color=ORANGE)
        self.wait(0.5)

# --------------------------------------------------
# Step 3 – Compute v and du
# --------------------------------------------------
class Step3(Scene):
    def construct(self):
        self.add(banner("Step 3  –  Compute $v$ and $du$"))

        lines = VGroup(
            MathTex(r"u = x \;\Rightarrow\; du = dx", font_size=EQ_FONT_SIZE),
            MathTex(r"\int \sin(2x)\,dx = -\tfrac12\cos(2x) \;\Longrightarrow\; v = -\tfrac12\cos(2x)",
                    font_size=EQ_FONT_SIZE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8).shift(DOWN * 0.5)

        self.play(LaggedStart(*[FadeIn(m) for m in lines], lag_ratio=0.3))
        circumscribe(lines[0][3:], self, YELLOW)   # highlight du
        circumscribe(lines[1][-3:], self, ORANGE)  # highlight v
        self.wait(0.5)

# --------------------------------------------------
# Step 4 – Apply integration by parts
# --------------------------------------------------
class Step4(Scene):
    def construct(self):
        self.add(banner("Step 4  –  Apply integration by parts and simplify"))

        start = MathTex(r"\int_{0}^{\pi/8} x\,\sin(2x)\,dx", font_size=EQ_FONT_SIZE).shift(UP * 2)

        step1 = MathTex(
            r"={} \Bigl[x\!\left(-\tfrac12\cos(2x)\right)\Bigr]_{0}^{\pi/8}"
            r" - \int_{0}^{\pi/8} \left(-\tfrac12\cos(2x)\right)\,dx",
            font_size=EQ_FONT_SIZE,
        ).next_to(start, DOWN, buff=1)

        step2 = MathTex(
            r"= -\tfrac12 x\cos(2x)\Big|_{0}^{\pi/8} + \tfrac12\int_{0}^{\pi/8}\cos(2x)\,dx",
            font_size=EQ_FONT_SIZE,
        ).next_to(step1, DOWN, buff=1)

        self.play(FadeIn(start))
        self.wait(0.5)
        self.play(Transform(start.copy(), step1, run_time=1.5))
        self.wait(0.5)
        self.play(Transform(step1.copy(), step2))
        circumscribe(step2[-1], self, color=ORANGE)
        self.wait(0.5)

# --------------------------------------------------
# Step 5 – Compute the boundary term
# --------------------------------------------------
class Step5(Scene):
    def construct(self):
        self.add(banner("Step 5  –  Evaluate boundary term"))

        expr = MathTex(
            r"-\tfrac12 x\cos(2x)\Big|_{0}^{\pi/8}",
            font_size=EQ_FONT_SIZE,
        ).shift(UP * 1.5)

        eval1 = MathTex(
            r"= -\tfrac12\left(\frac{\pi}{8}\right)\cos\!\left(\frac{\pi}{4}\right) - 0",
            font_size=EQ_FONT_SIZE,
        ).next_to(expr, DOWN, buff=1)

        eval2 = MathTex(
            r"= -\frac{\pi}{8}\cdot\frac{\sqrt2}{4}",
            font_size=EQ_FONT_SIZE,
        ).next_to(eval1, DOWN, buff=1)

        final = MathTex(
            r"= -\frac{\pi\sqrt2}{32}",
            font_size=EQ_FONT_SIZE,
            color=YELLOW,
        ).next_to(eval2, DOWN, buff=1)

        self.play(FadeIn(expr))
        self.play(Transform(expr.copy(), eval1))
        self.wait(0.5)
        self.play(Transform(eval1.copy(), eval2))
        self.wait(0.5)
        self.play(Transform(eval2.copy(), final))
        circumscribe(final, self, YELLOW)
        self.wait(0.5)

# --------------------------------------------------
# Step 6 – Integrate cos(2x)
# --------------------------------------------------
class Step6(Scene):
    def construct(self):
        self.add(banner("Step 6  –  Integrate $\\cos(2x)$ term"))

        integral_line = MathTex(
            r"\tfrac12\int_{0}^{\pi/8} \cos(2x)\,dx",
            font_size=EQ_FONT_SIZE,
        ).shift(UP * 1.8)

        antideriv = MathTex(
            r"= \tfrac12\bigl[\tfrac12\sin(2x)\bigr]_{0}^{\pi/8}",
            font_size=EQ_FONT_SIZE,
        ).next_to(integral_line, DOWN, buff=1)

        eval = MathTex(
            r"= \tfrac14\sin\!\left(\frac{\pi}{4}\right)",
            font_size=EQ_FONT_SIZE,
        ).next_to(antideriv, DOWN, buff=1)

        final = MathTex(
            r"= \frac{\sqrt2}{8}",
            font_size=EQ_FONT_SIZE,
            color=ORANGE,
        ).next_to(eval, DOWN, buff=1)

        self.play(FadeIn(integral_line))
        self.play(Transform(integral_line.copy(), antideriv))
        self.wait(0.5)
        self.play(Transform(antideriv.copy(), eval))
        self.wait(0.5)
        self.play(Transform(eval.copy(), final))
        circumscribe(final, self, ORANGE)
        self.wait(0.5)

# --------------------------------------------------
# Step 7 – Combine results
# --------------------------------------------------
class Step7(Scene):
    def construct(self):
        self.add(banner("Step 7  –  Combine & simplify"))

        pieces = VGroup(
            MathTex(r"-\frac{\pi\sqrt2}{32}", color=YELLOW, font_size=EQ_FONT_SIZE),
            MathTex(r"+", font_size=EQ_FONT_SIZE),
            MathTex(r"\frac{\sqrt2}{8}", color=ORANGE, font_size=EQ_FONT_SIZE),
        ).arrange(RIGHT, buff=0.4).shift(UP * 1.2)

        combined = MathTex(
            r"= \sqrt2\!\left(-\frac{\pi}{32}+\frac{1}{8}\right)",
            font_size=EQ_FONT_SIZE,
        ).next_to(pieces, DOWN, buff=1)

        simplified = MathTex(
            r"= \sqrt2\;\frac{4-\pi}{32}",
            font_size=EQ_FONT_SIZE,
            color=WHITE,
        ).next_to(combined, DOWN, buff=1)

        result_box = SurroundingRectangle(simplified, color=GREEN)

        self.play(LaggedStart(*[FadeIn(m) for m in pieces], lag_ratio=0.2))
        self.wait(1)
        self.play(Transform(pieces.copy(), combined))
        self.wait(1)
        self.play(Transform(combined.copy(), simplified))
        self.play(Create(result_box))
        self.wait(0.5)