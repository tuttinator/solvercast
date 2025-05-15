from manim import *

# Global configuration -------------------------------------------------------
config.background_color = "#1e1e1e"

TITLE_SIZE = 48
EQ_SIZE = 36
BANNER_COLOR = BLUE_E
TEXT_COLOR = WHITE

# Helper utilities -----------------------------------------------------------
def create_banner(title: str):
    """Return a VGroup with a semi-transparent banner and the step title."""
    banner_height = 1
    banner = Rectangle(
        width=config.frame_width,
        height=banner_height,
        fill_color=BANNER_COLOR,
        fill_opacity=0.7,
        stroke_width=0,
    ).to_edge(UP, buff=0)

    title_tex = Text(title, color=TEXT_COLOR, font_size=TITLE_SIZE)
    title_tex.move_to(banner.get_center())

    return VGroup(banner, title_tex)


# STEP 1 ---------------------------------------------------------------------
class Step1(Scene):
    """1. Problem analysis and identification of relevant topics"""

    def construct(self):
        # Banner --------------------------------------------------------------
        banner = create_banner("1. Problem Analysis & Relevant Topics")
        self.play(FadeIn(banner, shift=DOWN))
        self.wait(0.5)

        # Integral with colour-coded parts ------------------------------------
        integral = MathTex(
            r"\displaystyle \int_{0}^{\pi/8} ",
            r"x",
            r"\,\sin(2x)\,dx",
            font_size=EQ_SIZE,
            color=TEXT_COLOR,
        )
        integral[1].set_color(YELLOW)
        integral[2].set_color(ORANGE)
        integral.next_to(banner, DOWN, buff=1)

        self.play(FadeIn(integral, scale=0.9))
        self.wait(0.5)

        # Integration-by-parts formula ---------------------------------------
        ibp = MathTex(r"\int u\,dv = u\,v - \int v\,du", font_size=EQ_SIZE)
        ibp.set_color(TEXT_COLOR)
        ibp.next_to(integral, DOWN, buff=0.8)

        self.play(Write(ibp))
        self.wait(1)

        # Circumscribe key choices -------------------------------------------
        self.play(Circumscribe(integral[1], color=YELLOW), run_time=1)
        self.play(Circumscribe(integral[2], color=ORANGE), run_time=1)
        self.wait(0.5)

        self.wait(0.5)  # keep last frame


# STEP 2 ---------------------------------------------------------------------
class Step2(Scene):
    """2. Choose the parts for Integration by Parts"""

    def construct(self):
        banner = create_banner("2. Choose u and dv")
        self.play(FadeIn(banner, shift=DOWN))
        self.wait(0.5)

        # Show coloured integral again ---------------------------------------
        integral = MathTex(
            r"\int_{0}^{\pi/8} ",
            r"x",
            r"\,\sin(2x)\,dx",
            font_size=EQ_SIZE,
        )
        integral[1].set_color(YELLOW)
        integral[2].set_color(ORANGE)
        integral.next_to(banner, DOWN, buff=1)
        self.play(FadeIn(integral))
        self.wait(0.5)

        # Display choices -----------------------------------------------------
        choices = MathTex(
            r"u = x \qquad\qquad dv = \sin(2x)\,dx",
            font_size=EQ_SIZE,
        )
        choices[0][2].set_color(YELLOW)  # x in u
        choices[0][18:26].set_color(ORANGE)  # sin(2x) in dv
        choices.next_to(integral, DOWN, buff=1)

        self.play(Write(choices))
        self.wait(1)

        # Compute du and v ----------------------------------------------------
        duo = MathTex(r"du = dx", font_size=EQ_SIZE).next_to(choices, DOWN, buff=0.6)
        vo = MathTex(r"v = -\dfrac{\cos(2x)}{2}", font_size=EQ_SIZE).next_to(
            duo, DOWN, buff=0.4
        )
        self.play(LaggedStart(Write(duo), Write(vo), lag_ratio=0.75))
        self.wait(0.5)

        self.wait(0.5)


# STEP 3 ---------------------------------------------------------------------
class Step3(Scene):
    """3. Apply the Integration-by-Parts formula"""

    def construct(self):
        banner = create_banner("3. Apply Integration-by-Parts")
        self.play(FadeIn(banner, shift=DOWN))
        self.wait(0.5)

        # First line ----------------------------------------------------------
        line1 = MathTex(
            r"\int x\,\sin(2x)\,dx",
            r" = ",
            r"x\!\left(-\frac{\cos(2x)}{2}\right)",
            r" - ",
            r"\int\!\left(-\frac{\cos(2x)}{2}\right)dx",
            font_size=EQ_SIZE,
        )
        line1.next_to(banner, DOWN, buff=1)
        line1[0][0].set_color(YELLOW)       # x in integrand
        line1[0][2:].set_color(ORANGE)      # sin(2x)
        self.play(Write(line1))
        self.wait(1)

        # Simplify minus signs ------------------------------------------------
        line2 = MathTex(
            r"\int x\,\sin(2x)\,dx = -\frac{x\cos(2x)}{2}"
            r" + \frac12\int \cos(2x)\,dx",
            font_size=EQ_SIZE,
        )
        line2.move_to(line1.get_center())

        self.play(Transform(line1, line2))
        line1.set_color_by_tex("x", YELLOW)
        line1.set_color_by_tex("cos(2x)", ORANGE)
        self.wait(0.5)

        self.play(Circumscribe(line1[2], color=YELLOW))
        self.wait(0.5)

        self.wait(0.5)


# STEP 4 ---------------------------------------------------------------------
class Step4(Scene):
    """4. Integrate the remaining cosine term"""

    def construct(self):
        banner = create_banner("4. Integrate Remaining Cos Term")
        self.play(FadeIn(banner, shift=DOWN))
        self.wait(0.5)

        # Show remaining integral --------------------------------------------
        prev = MathTex(
            r"-\frac{x\cos(2x)}{2} + \frac12\int \cos(2x)\,dx",
            font_size=EQ_SIZE,
        )
        prev.next_to(banner, DOWN, buff=1)
        self.play(Write(prev))
        self.wait(0.5)

        # Evaluate ∫cos(2x)dx -------------------------------------------------
        calc = MathTex(
            r"\int \cos(2x)\,dx = \frac{\sin(2x)}{2}",
            font_size=EQ_SIZE,
        )
        calc.next_to(prev, DOWN, buff=0.8)
        self.play(Write(calc))
        self.wait(0.5)

        # Build final antiderivative -----------------------------------------
        final = MathTex(
            r"F(x)= -\frac{x\cos(2x)}{2} + \frac{\sin(2x)}{4}",
            font_size=EQ_SIZE,
        )
        final.next_to(calc, DOWN, buff=0.8)

        self.play(Write(final))
        self.play(Circumscribe(final, color=GREEN), run_time=1)
        self.wait(0.5)

        self.wait(0.5)


# STEP 5 ---------------------------------------------------------------------
class Step5(Scene):
    """5. Evaluate the antiderivative at the limits 0 and π/8"""

    def construct(self):
        banner = create_banner("5. Evaluate at 0 and π/8")
        self.play(FadeIn(banner, shift=DOWN))
        self.wait(0.5)

        # Antiderivative expression ------------------------------------------
        F = MathTex(
            r"F(x)= -\frac{x\cos(2x)}{2}+ \frac{\sin(2x)}{4}",
            font_size=EQ_SIZE,
        )
        F.next_to(banner, DOWN, buff=1)
        self.play(FadeIn(F))
        self.wait(0.5)

        # Compute F(π/8) ------------------------------------------------------
        fp = MathTex(
            r"F\!\left(\frac{\pi}{8}\right)= -\frac{\tfrac{\pi}{8}\cos\!\left(\tfrac{\pi}{4}\right)}{2}"
            r"+\frac{\sin\!\left(\tfrac{\pi}{4}\right)}{4}",
            font_size=EQ_SIZE,
        )
        fp.next_to(F, DOWN, buff=0.8)
        self.play(Write(fp))
        self.wait(1)

        # Compute F(0) --------------------------------------------------------
        f0 = MathTex(r"F(0)=0", font_size=EQ_SIZE)
        f0.next_to(fp, DOWN, buff=0.8)
        self.play(Write(f0))
        self.wait(0.5)

        # Definite integral result -------------------------------------------
        result = MathTex(
            r"\int_{0}^{\pi/8} x\,\sin(2x)\,dx = F\!\left(\frac{\pi}{8}\right)-F(0)",
            font_size=EQ_SIZE,
        )
        result.next_to(f0, DOWN, buff=0.8)
        self.play(Write(result))
        self.wait(0.5)

        self.wait(0.5)


# STEP 6 ---------------------------------------------------------------------
class Step6(Scene):
    """6. Numerical simplification"""

    def construct(self):
        banner = create_banner("6. Numerical Simplification")
        self.play(FadeIn(banner, shift=DOWN))
        self.wait(0.5)

        # Start with expression ----------------------------------------------
        start = MathTex(
            r"F\!\left(\frac{\pi}{8}\right)= "
            r"-\frac{\tfrac{\pi}{8}\left(\sqrt2/2\right)}{2}"
            r"+\frac{\sqrt2/2}{4}",
            font_size=EQ_SIZE,
        )
        start.next_to(banner, DOWN, buff=1)
        self.play(Write(start))
        self.wait(1)

        # Simplify step by step ----------------------------------------------
        step1 = MathTex(
            r"= -\frac{\pi\sqrt2}{32}+\frac{\sqrt2}{8}",
            font_size=EQ_SIZE,
        )
        step1.next_to(start, DOWN, buff=0.7)
        self.play(Write(step1))
        self.wait(0.5)

        step2 = MathTex(
            r"= \sqrt2\!\left(\frac{1}{8}-\frac{\pi}{32}\right)",
            font_size=EQ_SIZE,
        )
        step2.next_to(step1, DOWN, buff=0.7)
        self.play(Write(step2))
        self.wait(0.5)

        step3 = MathTex(
            r"= \sqrt2\!\left(\frac{4-\pi}{32}\right)",
            font_size=EQ_SIZE,
        )
        step3.next_to(step2, DOWN, buff=0.7)
        self.play(Write(step3))
        self.wait(0.5)

        final = MathTex(
            r"\boxed{\displaystyle \int_{0}^{\pi/8} x\,\sin(2x)\,dx"
            r"= \frac{\sqrt2\,(4-\pi)}{32}}",
            font_size=EQ_SIZE,
            color=GREEN,
        )
        final.next_to(step3, DOWN, buff=1)
        self.play(FadeIn(final, scale=1.05))
        self.play(Circumscribe(final, color=GREEN), run_time=1)
        self.wait(0.5)

        self.wait(0.5)