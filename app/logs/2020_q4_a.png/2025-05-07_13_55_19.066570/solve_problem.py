from manim import *

# ---------- Global style -----------------------------------------------------
config.background_color = "#1e1e1e"
TITLE_SIZE = 48
EQ_SIZE = 36

# ---------- Helper UI elements ----------------------------------------------
def add_banner(scene: Scene, title: str):
    banner = Rectangle(
        width=config.frame_width,
        height=0.9,
        fill_color=BLUE_E,
        fill_opacity=0.6,
        stroke_width=0,
    ).to_edge(UP, buff=0)
    label = Text(title, font_size=TITLE_SIZE, color=WHITE).move_to(banner)
    scene.add(banner, label)


def circumscribe(mobj, scene: Scene, color=YELLOW, run_time=1):
    scene.play(Circumscribe(mobj, color=color, run_time=run_time))


# ----------  Step 1 ----------------------------------------------------------
class Step1(Scene):
    def construct(self):
        add_banner(self, "Step 1: Analyse the problem and recall learning outcomes")

        integral = MathTex(r"\displaystyle \int_{0}^{\pi/8} x\,\sin(2x)\,dx",
                           font_size=EQ_SIZE, color=WHITE).shift(UP * 1)
        self.play(FadeIn(integral), run_time=1)
        self.wait(0.5)

        bullets = VGroup(
            Tex(r"• Product $x\sin(2x)$ $\Rightarrow$ Integration by parts",
                font_size=32, color=WHITE),
            Tex(r"• Limits: $0 \le x \le \dfrac{\pi}{8}$", font_size=32, color=WHITE),
            Tex(r"• Need basic $\int\sin(2x)\,dx$", font_size=32, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(integral, DOWN, buff=1)
        self.play(LaggedStart(*[FadeIn(b) for b in bullets], lag_ratio=0.3), run_time=1.5)
        self.wait(1)

        circumscribe(integral, self)
        self.wait(0.5)


# ----------  Step 2 ----------------------------------------------------------
class Step2(Scene):
    def construct(self):
        add_banner(self, "Step 2: Choose the technique—set up integration by parts")

        original = MathTex(r"\int_{0}^{\pi/8} x\,\sin(2x)\,dx",
                           font_size=EQ_SIZE, color=WHITE).shift(UP * 1)
        self.play(FadeIn(original), run_time=1)
        self.wait(0.5)

        assignments = MathTex(
            r"u &= x &\Longrightarrow&\; du = dx \\[4pt]"
            r"dv &= \sin(2x)\,dx &\Longrightarrow&\; v = -\dfrac{\cos(2x)}{2}",
            font_size=EQ_SIZE
        ).next_to(original, DOWN, buff=0.8, aligned_edge=LEFT)
        assignments[0].set_color(ORANGE)
        assignments[3].set_color(ORANGE)
        self.play(Write(assignments, lag_ratio=0.2), run_time=2)
        self.wait(1)

        parts_formula = MathTex(
            r"\int u\,dv = u\,v - \int v\,du",
            font_size=EQ_SIZE
        ).next_to(assignments, DOWN, buff=0.8)
        self.play(FadeIn(parts_formula), run_time=1)
        self.wait(0.5)
        circumscribe(parts_formula, self, color=YELLOW)

        transformed = MathTex(
            r"\int_{0}^{\pi/8} x\sin(2x)\,dx"
            r"= \left[-\dfrac{x\cos(2x)}{2}\right]_{0}^{\pi/8}"
            r"-\int_{0}^{\pi/8}\left(-\dfrac{\cos(2x)}{2}\right)dx",
            font_size=EQ_SIZE
        ).next_to(parts_formula, DOWN, buff=0.8)
        self.play(TransformFromCopy(original, transformed), run_time=2)
        self.wait(0.5)
        circumscribe(transformed, self)
        self.wait(0.5)


# ----------  Step 3 ----------------------------------------------------------
class Step3(Scene):
    def construct(self):
        add_banner(self, "Step 3: Simplify the remaining integral")

        expr1 = MathTex(
            r"\left[-\dfrac{x\cos(2x)}{2}\right]_{0}^{\pi/8}"
            r" + \dfrac12\int_{0}^{\pi/8}\cos(2x)\,dx",
            font_size=EQ_SIZE
        ).shift(UP * 1)
        self.play(FadeIn(expr1), run_time=1)
        self.wait(0.5)

        step_int = MathTex(
            r"\dfrac12\int_{0}^{\pi/8}\cos(2x)\,dx"
            r"= \dfrac12\left[\dfrac{\sin(2x)}{2}\right]_{0}^{\pi/8}"
            r"= \dfrac{\sin(2x)}{4}\Big|_{0}^{\pi/8}",
            font_size=EQ_SIZE
        ).next_to(expr1, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(step_int, run_time=2))
        self.wait(1)
        circumscribe(step_int[0:10], self, color=YELLOW)
        self.wait(0.5)


# ----------  Step 4 ----------------------------------------------------------
class Step4(Scene):
    def construct(self):
        add_banner(self, "Step 4: Evaluate the antiderivative at the bounds")

        F = MathTex(
            r"F(x)= -\dfrac{x\cos(2x)}{2} + \dfrac{\sin(2x)}{4}",
            font_size=EQ_SIZE
        ).shift(UP * 1)
        self.play(FadeIn(F), run_time=1)
        self.wait(0.5)

        upper = MathTex(
            r"F\!\left(\dfrac{\pi}{8}\right)"
            r"= -\dfrac{\pi}{8}\cdot\dfrac{\sqrt2}{2}\cdot\dfrac12"
            r"+\dfrac{\sqrt2}{2}\cdot\dfrac14"
            r"= -\dfrac{\pi\sqrt2}{32} + \dfrac{\sqrt2}{8}",
            font_size=EQ_SIZE
        ).next_to(F, DOWN, buff=0.6, aligned_edge=LEFT)
        upper[4:8].set_color(ORANGE)
        self.play(Write(upper, run_time=3))
        self.wait(1)

        lower = MathTex(r"F(0)=0", font_size=EQ_SIZE).next_to(upper, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(Write(lower), run_time=1)
        self.wait(0.5)

        result = MathTex(
            r"\int_{0}^{\pi/8}x\sin(2x)\,dx"
            r"= \dfrac{\sqrt2\,(4-\pi)}{32}",
            font_size=EQ_SIZE
        ).next_to(lower, DOWN, buff=0.8)
        self.play(Write(result), run_time=1.5)
        circumscribe(result, self)
        self.wait(0.5)


# ----------  Step 5 ----------------------------------------------------------
class Step5(Scene):
    def construct(self):
        add_banner(self, "Step 5: Check result and relate back")

        final_ans = MathTex(
            r"\boxed{\displaystyle \int_{0}^{\pi/8}x\sin(2x)\,dx"
            r"= \dfrac{\sqrt2\,(4-\pi)}{32}}",
            font_size=EQ_SIZE
        ).shift(UP * 1)
        self.play(FadeIn(final_ans), run_time=1)
        self.wait(0.5)

        checks = VGroup(
            Tex(r"• Domain $x\in[0,\pi/8]$, $\sin(2x)\ge0$ $\Rightarrow$ integral $>0$",
                font_size=32, color=WHITE),
            Tex(r"• $4-\pi\approx0.86$ $\Rightarrow$ value $\approx0.038$ (reasonable)",
                font_size=32, color=WHITE),
            Tex(r"• Used integration by parts  ➜ curriculum objective met",
                font_size=32, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(final_ans, DOWN, buff=1)
        self.play(LaggedStart(*[FadeIn(t) for t in checks], lag_ratio=0.3), run_time=2)
        self.wait(1)
        circumscribe(final_ans, self, color=ORANGE)
        self.wait(0.5)