from manim import *

# ---------- GLOBAL STYLE CONSTANTS ----------
BACKGROUND_COLOR = "#1e1e1e"
config.background_color = BACKGROUND_COLOR

TITLE_FONT_SIZE = 48
EQ_FONT_SIZE = 36
TITLE_COLOR = WHITE
TITLE_BG_COLOR = BLUE_E
TITLE_BG_OPACITY = 0.65


# ---------- HELPER COMPONENTS ----------
def get_title_banner(title_txt: str) -> VGroup:
    """Returns a VGroup with a semi–transparent background bar and the title."""
    banner = Rectangle(
        width=config.frame_width,
        height=1.0,
        stroke_width=0,
        fill_color=TITLE_BG_COLOR,
        fill_opacity=TITLE_BG_OPACITY,
    ).to_edge(UP)

    title = Text(title_txt, font_size=TITLE_FONT_SIZE, color=TITLE_COLOR).move_to(
        banner.get_center()
    )
    return VGroup(banner, title)


def show_equations(scene: Scene, tex_list: list[str]):
    """
    Utility: writes a sequence of MathTex objects, morphing each into the next.
    """
    previous_eq = None
    for i, tex in enumerate(tex_list):
        eq = MathTex(tex, font_size=EQ_FONT_SIZE, color=WHITE)
        if previous_eq is None:
            scene.play(FadeIn(eq, shift=UP), run_time=0.8)
        else:
            scene.play(Transform(previous_eq, eq), run_time=0.8)
        scene.wait(0.5)
        previous_eq = eq
    # Return last equation mobject so caller can keep it on screen
    return previous_eq


# ---------- SCENE 1 ----------
class Step1(Scene):
    """1. Problem analysis and curriculum links"""

    def construct(self):
        self.add(get_title_banner("1. Problem analysis and curriculum links"))

        # Integral to be solved
        integral_tex = r"\int_{0}^{\pi/8} x \sin(2x)\,dx"
        integral = MathTex(integral_tex, font_size=EQ_FONT_SIZE)
        self.play(FadeIn(integral, shift=DOWN), run_time=0.8)
        self.wait(0.5)

        # Annotate trigger for IBP
        prod_text = (
            r"\text{Product } x\cdot\sin(2x)\ \Rightarrow\ "
            r"\text{use Integration by Parts}"
        )
        annotation = MathTex(prod_text, font_size=EQ_FONT_SIZE)
        annotation.next_to(integral, DOWN, buff=0.8)
        self.play(Write(annotation), run_time=1)
        self.play(Circumscribe(integral, color=YELLOW))
        self.wait(1)
        self.wait(0.5)


# ---------- SCENE 2 ----------
class Step2(Scene):
    """2. Choose the parts for the IBP formula"""

    def construct(self):
        self.add(get_title_banner("2. Choose the parts for the IBP formula"))

        ibp_formula = MathTex(r"\int u\,dv = u\,v - \int v\,du", font_size=EQ_FONT_SIZE)
        ibp_formula.to_edge(UP, buff=1.2)
        self.play(FadeIn(ibp_formula), run_time=0.8)
        self.wait(0.5)

        # Choices of u and dv
        choices = MathTex(
            r"u = x\quad\Rightarrow\quad du = dx",
            r"\quad\quad",
            r"dv = \sin(2x)\,dx\quad\Rightarrow\quad v = -\dfrac{1}{2}\cos(2x)",
            font_size=EQ_FONT_SIZE,
        )
        choices.next_to(ibp_formula, DOWN, buff=1)
        self.play(Write(choices), run_time=1)
        self.play(
            LaggedStart(
                Circumscribe(choices[0], color=ORANGE),
                Circumscribe(choices[2], color=YELLOW),
                lag_ratio=0.3,
            )
        )
        self.wait(1)
        self.wait(0.5)


# ---------- SCENE 3 ----------
class Step3(Scene):
    """3. Apply the integration-by-parts formula (indefinite integral first)"""

    def construct(self):
        self.add(
            get_title_banner(
                "3. Apply the integration-by-parts formula (indefinite integral)"
            )
        )

        # Sequence of equations
        eq_sequence = [
            r"\int x\sin(2x)\,dx",
            r"= x\left(-\dfrac{1}{2}\cos(2x)\right)\;-\;\int\left(-\dfrac{1}{2}\cos(2x)\right)dx",
            r"= -\dfrac{1}{2}x\cos(2x) + \dfrac{1}{2}\int\cos(2x)\,dx",
            r"= -\dfrac{1}{2}x\cos(2x) + \dfrac{1}{2}\left(\dfrac{1}{2}\sin(2x)\right) + C",
            r"= -\dfrac{1}{2}x\cos(2x) + \dfrac{1}{4}\sin(2x) + C",
        ]
        last_eq = show_equations(self, eq_sequence)

        self.play(Circumscribe(last_eq[-5:], color=YELLOW))
        self.wait(1)
        self.wait(0.5)


# ---------- SCENE 4 ----------
class Step4(Scene):
    """4. Convert to the required definite integral"""

    def construct(self):
        self.add(get_title_banner("4. Convert to the required definite integral"))

        F_tex = r"F(x)= -\dfrac{1}{2}x\cos(2x)+\dfrac{1}{4}\sin(2x)"
        F_eq = MathTex(F_tex, font_size=EQ_FONT_SIZE)
        self.play(Write(F_eq), run_time=1)
        self.wait(0.5)

        eval_sequence = [
            r"\int_{0}^{\pi/8} x\sin(2x)\,dx = F\!\left(\dfrac{\pi}{8}\right)-F(0)",
            r"= \left[-\dfrac{1}{2}\cdot\dfrac{\pi}{8}\cdot\cos\!\left(\dfrac{\pi}{4}\right)"
            r"+\dfrac{1}{4}\sin\!\left(\dfrac{\pi}{4}\right)\right] - 0",
            r"= -\dfrac{\pi}{16}\cdot\dfrac{\sqrt2}{2} + \dfrac{1}{4}\cdot\dfrac{\sqrt2}{2}",
            r"= -\dfrac{\pi\sqrt2}{32} + \dfrac{\sqrt2}{8}",
        ]
        last = show_equations(self, eval_sequence)

        self.play(Circumscribe(last, color=ORANGE))
        self.wait(1)
        self.wait(0.5)


# ---------- SCENE 5 ----------
class Step5(Scene):
    """5. Simplify the exact value"""

    def construct(self):
        self.add(get_title_banner("5. Simplify the exact value"))

        simpl_seq = [
            r"-\dfrac{\pi\sqrt2}{32} + \dfrac{\sqrt2}{8}",
            r"= -\dfrac{\pi\sqrt2}{32} + \dfrac{4\sqrt2}{32}",
            r"= \dfrac{\sqrt2(4-\pi)}{32}",
        ]
        last = show_equations(self, simpl_seq)

        self.play(Circumscribe(last, color=YELLOW))
        self.wait(1)
        self.wait(0.5)


# ---------- SCENE 6 ----------
class Step6(Scene):
    """6. (Optional) Numerical check"""

    def construct(self):
        self.add(get_title_banner("6. (Optional) Numerical check"))

        approx_seq = [
            r"\dfrac{\sqrt2(4-\pi)}{32}\;\approx\;"
            r"\dfrac{1.41421356\times 0.858407}{32}",
            r"\approx 0.0379",
        ]
        last_eq = show_equations(self, approx_seq)

        self.play(Circumscribe(last_eq, color=ORANGE))
        self.wait(0.5)

        # Small graph for visual intuition
        axes = Axes(
            x_range=[0, PI / 8, PI / 32],
            y_range=[0, 0.5, 0.1],
            tips=False,
            axis_config={"stroke_color": GREY_B, "include_ticks": False},
        ).scale(0.9).to_edge(DOWN, buff=0.6)

        func = axes.plot(lambda x: x * np.sin(2 * x), color=GREEN_B)
        fill = axes.get_area(func, x_range=[0, PI / 8], color=GREEN_E, opacity=0.6)

        self.play(Create(axes), run_time=0.8)
        self.wait(0.3)
        self.play(Create(func), run_time=1.2)
        self.play(FadeIn(fill), run_time=0.8)
        self.wait(1)
        self.wait(0.5)