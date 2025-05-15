from manim import *

# --------------------------------------------------
# Global style and helper utilities
# --------------------------------------------------
config.background_color = "#1e1e1e"

TITLE_FONT_SIZE = 48
EQ_FONT_SIZE = 36


def add_title_banner(scene: Scene, text: str) -> VGroup:
    banner = Rectangle(
        width=scene.camera.frame.width,
        height=0.9,
        stroke_width=0,
        fill_color=BLUE_E,
        fill_opacity=0.35,
    ).to_edge(UP, buff=0)
    title = Tex(text, color=WHITE, font_size=TITLE_FONT_SIZE).move_to(banner.get_center())
    scene.add(banner, title)
    return VGroup(banner, title)


def circ(scene: Scene, mob: Mobject, color=YELLOW, rt=1):
    scene.play(Circumscribe(mob, color=color, fade_out=True), run_time=rt)


# --------------------------------------------------
# 1. Problem analysis and links to the curriculum
# --------------------------------------------------
class Step1(Scene):
    def construct(self):
        add_title_banner(self, "1. Problem analysis and links to the curriculum")

        integral = MathTex(r"\int_{0}^{\pi/8} x\,\sin(2x)\,dx", font_size=EQ_FONT_SIZE)
        self.play(FadeIn(integral, shift=DOWN), run_time=1)
        self.wait(0.5)

        bullets = VGroup(
            Tex("• Integration by parts", font_size=32, color=WHITE),
            Tex("• Trigonometric identities", font_size=32, color=WHITE),
            Tex("• Definite integral evaluation", font_size=32, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(integral, DOWN, buff=0.8)

        self.play(LaggedStart(*[FadeIn(b) for b in bullets], lag_ratio=0.3), run_time=1)
        self.wait(0.5)

        circ(self, integral)
        self.wait(1)

        hint = Tex(
            r"Integration by parts: $\displaystyle\int u\,dv = uv-\int v\,du$",
            font_size=32,
            color=ORANGE,
        ).to_edge(DOWN)
        self.play(FadeIn(hint), run_time=1)
        self.wait(0.5)
        self.wait(0.5)  # final pause


# --------------------------------------------------
# 2. Choose u and dv for integration by parts
# --------------------------------------------------
class Step2(Scene):
    def construct(self):
        add_title_banner(self, "2. Choose $u$ and $dv$ for integration by parts")

        choices = MathTex(
            r"u = x \quad\Longrightarrow\quad du = dx\\[6pt]"
            r"dv = \sin(2x)\,dx \quad\Longrightarrow\quad v = -\tfrac12\cos(2x)",
            font_size=EQ_FONT_SIZE,
        ).scale(0.9)
        self.play(Write(choices, run_time=2))
        circ(self, choices[0][:1])  # highlight 'u = x'
        circ(self, choices[1][-3:-1])  # highlight 'v'
        self.wait(0.5)

        note = Tex("Differentiate the algebraic factor, integrate the trig factor.",
                   font_size=32, color=ORANGE).to_edge(DOWN)
        self.play(FadeIn(note), run_time=1)
        self.wait(0.5)
        self.wait(0.5)


# --------------------------------------------------
# 3. Apply the integration-by-parts formula
# --------------------------------------------------
class Step3(Scene):
    def construct(self):
        add_title_banner(self, "3. Apply the integration-by-parts formula")

        start = MathTex(r"\int x\,\sin(2x)\,dx", font_size=EQ_FONT_SIZE).to_edge(UP, buff=1.5)
        self.play(FadeIn(start), run_time=1)
        self.wait(0.5)

        first = MathTex(
            r"= x\Bigl(-\tfrac12\cos 2x\Bigr) - \int \Bigl(-\tfrac12\cos 2x\Bigr)\,dx",
            font_size=EQ_FONT_SIZE
        ).next_to(start, DOWN, buff=1)
        self.play(Transform(start.copy(), first), run_time=1.5)
        circ(self, first[2:7])  # highlight uv term
        self.wait(0.5)

        simplified = MathTex(
            r"= -\tfrac12 x\cos 2x + \tfrac12 \int \cos 2x\,dx",
            font_size=EQ_FONT_SIZE
        ).next_to(first, DOWN, buff=1)
        self.play(Transform(first.copy(), simplified), run_time=1.5)
        circ(self, simplified[-5:-1], color=ORANGE)
        self.wait(0.5)
        self.wait(0.5)


# --------------------------------------------------
# 4. Complete the indefinite integral
# --------------------------------------------------
class Step4(Scene):
    def construct(self):
        add_title_banner(self, "4. Complete the indefinite integral")

        expr1 = MathTex(
            r"\int \cos 2x\,dx = \tfrac12 \sin 2x",
            font_size=EQ_FONT_SIZE
        ).to_edge(UP, buff=1.2)
        self.play(Write(expr1), run_time=1.2)
        self.wait(0.5)

        full = MathTex(
            r"\int x\,\sin(2x)\,dx = -\tfrac12 x\cos 2x + \tfrac14 \sin 2x + C",
            font_size=EQ_FONT_SIZE
        ).next_to(expr1, DOWN, buff=1)
        self.play(Write(full), run_time=1.5)
        circ(self, full[-2], color=YELLOW)  # highlight +C
        self.wait(1)
        self.wait(0.5)


# --------------------------------------------------
# 5. Evaluate between the limits 0 and π/8
# --------------------------------------------------
class Step5(Scene):
    def construct(self):
        add_title_banner(self, "5. Evaluate between the limits $0$ and $\\pi/8$")

        F = MathTex(
            r"F(x)= -\tfrac12 x\cos 2x + \tfrac14 \sin 2x",
            font_size=EQ_FONT_SIZE
        ).to_edge(UP, buff=1)
        self.play(FadeIn(F), run_time=1)
        self.wait(0.5)

        F_upper = MathTex(
            r"F\!\left(\tfrac{\pi}{8}\right)"
            r"= -\tfrac12\!\left(\tfrac{\pi}{8}\right)\cos\!\left(\tfrac{\pi}{4}\right)"
            r"+ \tfrac14 \sin\!\left(\tfrac{\pi}{4}\right)",
            font_size=EQ_FONT_SIZE
        ).next_to(F, DOWN, buff=0.8)
        self.play(Write(F_upper), run_time=1.5)
        self.wait(0.5)

        simplify_upper = MathTex(
            r"= -\frac{\pi\sqrt2}{32} + \frac{\sqrt2}{8}"
            r"= \frac{\sqrt2(4-\pi)}{32}",
            font_size=EQ_FONT_SIZE
        ).next_to(F_upper, DOWN, buff=0.8)
        self.play(TransformFromCopy(F_upper, simplify_upper), run_time=1.5)
        circ(self, simplify_upper[-1], color=YELLOW)
        self.wait(0.5)

        result = MathTex(
            r"\int_{0}^{\pi/8} x\,\sin(2x)\,dx"
            r"= \frac{\sqrt2(4-\pi)}{32}",
            font_size=EQ_FONT_SIZE,
            color=ORANGE
        ).next_to(simplify_upper, DOWN, buff=1)
        self.play(FadeIn(result), run_time=1.2)
        self.wait(1)
        self.wait(0.5)