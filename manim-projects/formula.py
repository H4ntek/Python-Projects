from manim import *

A = 3
B = 1

class Wzor(Scene):
    def construct(self):
        #self.add(NumberPlane())
        t1 = Tex("Dowód wzoru skróconego mnożenia:")
        t1.shift(3 * LEFT + UP/2)
        m1 = MathTex("(a+b)^2", "=", "a^2", "+", "2ab", "+", "b^2")

        m1.shift(3 * LEFT + DOWN/2)
        s1 = Square(side_length = A)
        s1.shift(4 * RIGHT + LEFT/2 + UP/2)
        s2 = Square(side_length = B)
        s2.next_to(s1, DOWN + RIGHT, buff = 0)
        r1 = Rectangle(width = A, height = B)
        r1.shift(3.5 * RIGHT + 1.5 * DOWN)

        la_s1L = MathTex("a", color = RED_C)
        la_s1U = la_s1L.copy()
        la_s1C = MathTex("a^2", color = RED_C)
        la_s1L.next_to(s1, LEFT, buff = MED_SMALL_BUFF)
        la_s1U.next_to(s1, UP, buff = MED_SMALL_BUFF)
        la_s1C.move_to(s1)

        la_s2R = MathTex("b", color = BLUE_C)
        la_s2D = la_s2R.copy()
        la_s2C = MathTex("b^2", color = BLUE_C)
        la_s2R.next_to(s2, RIGHT, buff = MED_SMALL_BUFF)
        la_s2D.next_to(s2, DOWN, buff = MED_SMALL_BUFF)
        la_s2C.move_to(s2)

        s1.set_fill(RED_C, opacity = 0.3)
        s1.set_stroke(RED_E, width = 5)
        s2.set_fill(BLUE_C, opacity = 0.3)
        s2.set_stroke(BLUE_E, width = 5)
        r1.set_fill(PURPLE_C, opacity = 0.3)
        r1.set_stroke(PURPLE_E, width = 5)

        r_temp = r1.copy()
        r2 = r_temp.copy().shift(2 * RIGHT + 2 * UP)

        self.play(Write(t1))
        self.play(Write(m1))
        self.wait(1)
        self.play(GrowFromCenter(s1))
        self.play(Write(la_s1L), Write(la_s1U))
        self.play(Write(la_s1C))
        self.wait(1)
        self.play(GrowFromCenter(s2))
        self.play(Write(la_s2R), Write(la_s2D))
        self.play(Write(la_s2C))
        self.wait(1)
        self.play(GrowFromCenter(r1))
        self.wait(1)
        self.play(ReplacementTransform(r_temp, r2))
        self.play(Rotate(r2, PI/2))
        la_r1C = MathTex("ab", color = PURPLE_C)
        la_r1C.move_to(r1)
        la_r2C = la_r1C.copy()
        la_r2C.move_to(r2)
        self.play(Write(la_r1C), Write(la_r2C))

        self.wait(2)

        b1 = Brace(m1[0])
        b1_text = b1.get_text("Pole całości")
        m1[0][1].set_color(RED_C)
        m1[0][3].set_color(BLUE_C)
        self.play(Create(b1), Write(b1_text))
        self.wait(1)
        m1[2].set_color(RED_C)
        self.play(Indicate(m1[2], color = RED_C, run_time = 2, scale_factor = 1.5), Indicate(la_s1C, color = RED_C, run_time = 2, scale_factor = 1.5))
        self.wait(1)
        m1[4].set_color(PURPLE_C)
        self.play(Indicate(m1[4], color = PURPLE_C, run_time = 2, scale_factor = 1.5), Indicate(la_r1C, color = PURPLE_C, run_time = 2, scale_factor = 1.5), Indicate(la_r2C, color = PURPLE_C, run_time = 2, scale_factor = 1.5))
        self.wait(1)
        m1[6].set_color(BLUE_C)
        self.play(Indicate(m1[6], color = BLUE_C, run_time = 2, scale_factor = 1.5), Indicate(la_s2C, color = BLUE_C, run_time = 2, scale_factor = 1.5))
        self.wait(3)
        
