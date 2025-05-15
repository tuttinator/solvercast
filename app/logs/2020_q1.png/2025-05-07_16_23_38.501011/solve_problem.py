from manim import *

# ----------------- GLOBAL STYLE & HELPERS ---------------- #
config.background_color = "#1e1e1e"

TITLE_FONT_SIZE = 48
EQU_FONT_SIZE = 36


def title_banner(title: str) -> VGroup:
    """Returns a semi–transparent banner that sits at the top of the screen."""
    banner_height = 0.8
    banner = Rectangle(
        width=FRAME_WIDTH,
        height=banner_height,
        stroke_opacity=0,
        fill_color=BLUE_E,
        fill_opacity=0.4,
    )
    banner.to_edge(UP, buff=0)

    title_text = Text(title, font_size=TITLE_FONT_SIZE, color=WHITE)
    title_text.move_to(banner.get_center())

    return VGroup(banner, title_text)


def circumscribe(scene: Scene, mobj, color=YELLOW, run_time=0.8):
    scene.play(Circumscribe(mobj, color=color, fade_out=True, run_time=run_time))


# --------------------------- SCENES ----------------------- #
class Step1(Scene):
    """Read the question – extract the ‘givens’, decide the tools"""

    def construct(self):
        # Title banner
        self.add(title_banner("Step 1  –  Read the question & plan"))
        self.wait(1)

        # Bullet list of givens
        bullet_text = Tex(
            r"""
            \begin{aligned}
            &\bullet\; \text{Demand: } q(4+p^{2}) = 10 \;\Rightarrow\; q(p)=\dfrac{10}{4+p^{2}}\\[0.4em]
            &\bullet\; \text{Revenue: } R(p)=p\,q(p)\\[0.4em]
            &\bullet\; \text{Elasticity: } E(p)= -\dfrac{dq}{dp}\,\dfrac{p}{q}\\[0.4em]
            &\bullet\; \text{Supply: } p^{S}(q)=\alpha q + \beta\\[0.4em]
            &\bullet\; \text{Equilibrium: } (q^{*},p^{*})=(2,4)\\[0.4em]
            &\bullet\; \text{Producer surplus at eq.: } 2
            \end{aligned}
            """,
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )

        bullet_text.next_to(ORIGIN, DOWN)
        self.play(FadeIn(bullet_text, lag_ratio=0.2))
        self.wait(1)

        # Highlight tools that will be used
        tool_text = Text(
            "Tools: Differentiation  •  Optimisation  •  Integration  •  Linear algebra",
            font_size=28,
            color=ORANGE,
        )
        tool_text.to_edge(DOWN)
        self.play(FadeIn(tool_text))
        self.wait(0.5)
        circumscribe(self, tool_text, color=ORANGE)
        self.wait(0.5)


class Step2(Scene):
    """Differentiate the demand curve and build the elasticity formula"""

    def construct(self):
        self.add(title_banner("Step 2  –  Differentiate & build elasticity"))

        # q(p)
        q_expr = MathTex(
            "q(p) = 10\\,(4+p^{2})^{-1}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        ).to_edge(UP, buff=1.2)

        self.play(FadeIn(q_expr))
        self.wait(0.5)

        # dq/dp
        dqdp = MathTex(
            "\\dfrac{dq}{dp} \\,=\\, -\\dfrac{20p}{(4+p^{2})^{2}}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        dqdp.next_to(q_expr, DOWN, buff=0.8)

        self.play(Write(dqdp))
        self.wait(1)

        # Elasticity formula generic
        elast_gen = MathTex(
            "E(p) \\,=\\, -\\dfrac{dq}{dp}\\,\\dfrac{p}{q}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        elast_gen.next_to(dqdp, DOWN, buff=0.8)
        self.play(FadeIn(elast_gen))
        self.wait(0.5)

        # Substitute
        elast_sub = MathTex(
            "E(p)","=",
            "2\\,\\dfrac{p^{2}}{4+p^{2}}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        elast_sub.next_to(elast_gen, DOWN, buff=0.8)

        self.play(TransformMatchingTex(elast_gen.copy(), elast_sub))
        self.wait(0.5)
        circumscribe(self, elast_sub[2], color=YELLOW)
        self.wait(0.5)


class Step3(Scene):
    """Show that the elasticity never exceeds 2"""

    def construct(self):
        self.add(title_banner("Step 3  –  Elasticity ≤ 2"))

        # Expression
        elast_expr = MathTex(
            "E(p) = 2\\,\\dfrac{p^{2}}{4+p^{2}}\\quad(p\\ge 0)",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        ).to_edge(UP, buff=1.2)
        self.play(FadeIn(elast_expr))
        self.wait(0.5)

        # Inequality line
        inequality = MathTex(
            "0 \\;\\le\\; \\dfrac{p^{2}}{4+p^{2}} \\;<\\; 1",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        inequality.next_to(elast_expr, DOWN, buff=0.8)
        self.play(Write(inequality))
        self.wait(1)

        # Multiply by 2
        multiply = MathTex(
            "0 \\;\\le\\; E(p) \\;<\\; 2",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        multiply.next_to(inequality, DOWN, buff=0.8)
        self.play(Write(multiply))
        circumscribe(self, multiply, color=ORANGE)
        self.wait(0.5)


class Step4(Scene):
    """Construct the revenue function and locate its turning point"""

    def construct(self):
        self.add(title_banner("Step 4  –  Revenue & turning point"))

        # Revenue function
        R_expr = MathTex(
            "R(p) = \\dfrac{10p}{4+p^{2}}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        ).to_edge(UP, buff=1.2)

        self.play(FadeIn(R_expr))
        self.wait(0.5)

        # Derivative
        dRdp = MathTex(
            "\\dfrac{dR}{dp} = \\dfrac{10(4-p^{2})}{(4+p^{2})^{2}}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        dRdp.next_to(R_expr, DOWN, buff=0.8)
        self.play(Write(dRdp))
        self.wait(1)

        # Sign analysis text
        sign_text = Tex(
            r"Sign of $\dfrac{dR}{dp}$ depends on $4-p^{2}$:",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        sign_text.next_to(dRdp, DOWN, buff=0.8)
        self.play(FadeIn(sign_text))
        self.wait(0.5)

        inc_dec = Tex(
            r"$p<2 \; \Rightarrow\; R\text{ increasing} \quad\quad "
            r"p>2 \; \Rightarrow\; R\text{ decreasing}$",
            font_size=EQU_FONT_SIZE,
            color=ORANGE,
        )
        inc_dec.next_to(sign_text, DOWN, buff=0.5)
        self.play(Write(inc_dec))
        circumscribe(self, inc_dec, color=ORANGE)
        self.wait(1)

        # Quick graph for visual aid
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3, 1],
            x_length=6,
            y_length=3,
            axis_config={"color": GREY_C},
        )
        axes.to_edge(DOWN, buff=0.8)

        graph = axes.plot(
            lambda p: 10 * p / (4 + p ** 2),
            x_range=[0.001, 5],
            color=YELLOW,
        )
        dot = Dot(axes.coords_to_point(2, 10 * 2 / (4 + 4)), color=RED)
        label = MathTex("p=2", font_size=24, color=RED).next_to(dot, UP, buff=0.1)

        self.play(Create(axes), run_time=1)
        self.play(Create(graph), run_time=1)
        self.play(FadeIn(dot, label))
        self.wait(0.5)


class Step5(Scene):
    """Approximate the revenue change when price rises 1 → 1.1"""

    def construct(self):
        self.add(title_banner("Step 5  –  Approximate ΔR for p: 1 → 1.1"))

        # Derivative expression
        dRdp = MathTex(
            "\\dfrac{dR}{dp} = \\dfrac{10(4-p^{2})}{(4+p^{2})^{2}}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        ).to_edge(UP, buff=1)
        self.play(FadeIn(dRdp))
        self.wait(0.5)

        # Evaluate at p=1
        subs = MathTex(
            "\\Bigg[\\dfrac{dR}{dp}\\Bigg]_{p=1} = "
            "\\dfrac{10(4-1)}{(4+1)^{2}} = \\dfrac{30}{25}=1.2",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        subs.next_to(dRdp, DOWN, buff=0.8)
        self.play(Write(subs))
        circumscribe(self, subs[-1], color=YELLOW)
        self.wait(1)

        # Linear approximation
        approx = MathTex(
            "\\Delta R \\approx R'(1)\\,\\Delta p = 1.2 \\times 0.1 = 0.12",
            font_size=EQU_FONT_SIZE,
            color=ORANGE,
        )
        approx.next_to(subs, DOWN, buff=0.8)
        self.play(Write(approx))
        circumscribe(self, approx, color=ORANGE)
        self.wait(0.5)


class Step6(Scene):
    """Impose the equilibrium and producer-surplus conditions on supply"""

    def construct(self):
        self.add(title_banner("Step 6  –  Solve supply parameters α, β"))

        # Supply form
        supply = MathTex(
            "p^{S}(q)=\\alpha q + \\beta",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        ).to_edge(UP, buff=1.2)
        self.play(FadeIn(supply))
        self.wait(0.5)

        # Equilibrium equation
        eq1 = MathTex(
            "4 = 2\\alpha + \\beta \\quad\\text{(Eq. 1)}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        eq1.next_to(supply, DOWN, buff=0.8)
        self.play(Write(eq1))
        self.wait(0.5)

        # Producer surplus integral (set-up)
        ps_integral = MathTex(
            "PS = \\int_{0}^{2}\\,(4 - (\\alpha q + \\beta))\\,dq = 2",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        ps_integral.next_to(eq1, DOWN, buff=0.8)
        self.play(Write(ps_integral))
        self.wait(1)

        # Evaluate integral to Eq.2
        eq2 = MathTex(
            "\\alpha + \\beta = 3 \\quad\\text{(Eq. 2)}",
            font_size=EQU_FONT_SIZE,
            color=WHITE,
        )
        eq2.next_to(ps_integral, DOWN, buff=0.8)
        self.play(Write(eq2))
        self.wait(0.5)

        # Solve system
        solve_steps = MathTex(
            "\\alpha = 1,\\quad \\beta = 2",
            font_size=EQU_FONT_SIZE,
            color=ORANGE,
        )
        solve_steps.next_to(eq2, DOWN, buff=0.8)
        self.play(Write(solve_steps))
        circumscribe(self, solve_steps, color=ORANGE)
        self.wait(0.5)