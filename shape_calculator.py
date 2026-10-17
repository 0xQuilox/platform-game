# ============================================================
#  SHAPES — OOP INHERITANCE PROJECT
#  Week 10 — Inheritance & Polymorphism
#  Mobile Development Programme
# ============================================================
#
#  WHAT THIS DEMONSTRATES:
#  - A parent class with default methods
#  - Child classes that override those methods
#  - Polymorphism: one function works on ANY shape type
#  - Real math using Python's math module
#
#  CLASSES BUILT:
#  Shape (parent)
#    ├── Circle
#    ├── Rectangle
#    └── Triangle
# ============================================================

import math


# ── PARENT CLASS ─────────────────────────────────────────────

class Shape:
    """
    The parent class. Every shape shares these two methods.
    They return 0 by default — child classes MUST override them
    with the correct formula for their shape.

    TEACHING POINT:
    This is a blueprint. It defines WHAT every shape should be
    able to do (calculate area and perimeter), but not HOW —
    because every shape has a different formula.
    """

    def __init__(self, colour="white"):
        self.colour = colour          # shared attribute all shapes can have

    def area(self):
        return 0                      # child classes override this

    def perimeter(self):
        return 0                      # child classes override this

    def describe(self):
        """
        A shared method all shapes inherit automatically.
        Notice we call self.area() and self.perimeter() —
        Python will call the CHILD's version, not this parent version.
        That is polymorphism in action.
        """
        name = type(self).__name__    # gets the actual class name (Circle, Rectangle, etc.)
        print(f"  {name:<12} | colour: {self.colour:<10} | "
              f"area: {self.area():>10.2f} | perimeter: {self.perimeter():>10.2f}")


# ── CHILD CLASS: CIRCLE ───────────────────────────────────────

class Circle(Shape):
    """
    Inherits from Shape. Overrides area() and perimeter().

    Formulae:
        area      = π × r²
        perimeter = 2 × π × r   (also called circumference)
    """

    def __init__(self, radius, colour="white"):
        super().__init__(colour)      # call parent __init__ to set colour
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


# ── CHILD CLASS: RECTANGLE ────────────────────────────────────

class Rectangle(Shape):
    """
    Inherits from Shape. Overrides area() and perimeter().

    Formulae:
        area      = width × height
        perimeter = 2 × (width + height)

    TEACHING POINT:
    A Square is a special Rectangle where width == height.
    You could create a Square class that inherits from Rectangle!
    """

    def __init__(self, width, height, colour="white"):
        super().__init__(colour)
        self.width  = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


# ── CHILD CLASS: TRIANGLE ─────────────────────────────────────

class Triangle(Shape):
    """
    Inherits from Shape. Overrides area() and perimeter().

    Takes three sides: a, b, c.

    Formulae:
        perimeter = a + b + c
        area      = Heron's Formula
                    s = (a + b + c) / 2   ← semi-perimeter
                    area = √(s(s-a)(s-b)(s-c))

    TEACHING POINT:
    Heron's formula works for ANY triangle given three sides —
    no need to know the height. Great chance to show students
    that real programming uses real maths.
    """

    def __init__(self, a, b, c, colour="white"):
        # Validate: the three sides must form a real triangle
        if not (a + b > c and b + c > a and a + c > b):
            raise ValueError(f"Sides {a}, {b}, {c} do not form a valid triangle.")
        super().__init__(colour)
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = (self.a + self.b + self.c) / 2    # semi-perimeter
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


# ── SUMMARY FUNCTION ─────────────────────────────────────────

def print_shape_summary(shapes):
    """
    Takes a list of ANY shape objects and prints a summary table.

    TEACHING POINT — THIS IS POLYMORPHISM:
    This function has no idea whether each item is a Circle,
    Rectangle, or Triangle. It just calls .area() and .perimeter()
    on each one — and Python figures out which version to run.

    You could add 100 new shape classes tomorrow, pass them into
    this function, and it would work perfectly without any changes.
    """
    print()
    print("  ╔══════════════════════════════════════════════════════════════╗")
    print("  ║                    SHAPE SUMMARY TABLE                      ║")
    print("  ╚══════════════════════════════════════════════════════════════╝")
    print()
    print(f"  {'Shape':<12} | {'Colour':<12} | {'Area':>12} | {'Perimeter':>12}")
    print(f"  {'─'*12}-+-{'─'*12}-+-{'─'*12}-+-{'─'*12}")

    total_area = 0

    for shape in shapes:
        name      = type(shape).__name__
        area      = shape.area()
        perim     = shape.perimeter()
        total_area += area
        print(f"  {name:<12} | {shape.colour:<12} | {area:>11.2f}  | {perim:>11.2f} ")

    print(f"  {'─'*12}-+-{'─'*12}-+-{'─'*12}-+-{'─'*12}")
    print(f"  {'TOTAL':<12}   {'':12}   {total_area:>11.2f}  |")
    print()


# ── DEMOS ────────────────────────────────────────────────────

def demo_individual():
    """Show each shape object being created and used individually."""
    print()
    print("  ── Demo 1: Individual Shape Objects ─────────────────────────")

    c = Circle(5, "red")
    r = Rectangle(4, 7, "blue")
    t = Triangle(3, 4, 5, "green")

    print()
    print(f"  Circle (r=5):")
    print(f"    area      = π × 5² = {c.area():.2f}")
    print(f"    perimeter = 2 × π × 5 = {c.perimeter():.2f}")

    print()
    print(f"  Rectangle (4 × 7):")
    print(f"    area      = 4 × 7 = {r.area():.2f}")
    print(f"    perimeter = 2 × (4 + 7) = {r.perimeter():.2f}")

    print()
    print(f"  Triangle (3, 4, 5) — a right triangle:")
    print(f"    area      = {t.area():.2f}  (should be 6.00 — base×height/2 = 4×3/2)")
    print(f"    perimeter = 3 + 4 + 5 = {t.perimeter():.2f}")


def demo_polymorphism():
    """
    The key demo — show that one loop and one function work
    on ALL shape types without knowing which type they are.
    """
    print()
    print("  ── Demo 2: Polymorphism — One Loop, All Shapes ──────────────")
    print()
    print("  The loop below calls .describe() on every shape.")
    print("  It does NOT check the type — it just calls the method.")
    print("  Python automatically runs the correct area() and perimeter().")
    print()

    shapes = [
        Circle(3,        "red"),
        Circle(7,        "orange"),
        Rectangle(5, 10, "blue"),
        Rectangle(2, 8,  "cyan"),
        Triangle(6, 8, 10, "green"),
        Triangle(5, 5, 5,  "purple"),
    ]

    print(f"  {'Shape':<12} | {'Colour':<10} | {'Area':>10} | {'Perimeter':>10}")
    print(f"  {'─'*12}-+-{'─'*10}-+-{'─'*10}-+-{'─'*10}")
    for shape in shapes:
        shape.describe()


def demo_summary_table():
    """Full summary table — the main project deliverable."""
    print()
    print("  ── Demo 3: Summary Table Function ───────────────────────────")

    shapes = [
        Circle(5,         "red"),
        Circle(3.5,       "pink"),
        Rectangle(8, 4,   "blue"),
        Rectangle(6, 6,   "navy"),    # this is actually a square!
        Triangle(3, 4, 5, "green"),
        Triangle(7, 7, 7, "teal"),    # equilateral triangle
    ]

    print_shape_summary(shapes)


def demo_invalid_triangle():
    """Show the validation error for an impossible triangle."""
    print()
    print("  ── Demo 4: Invalid Triangle Validation ──────────────────────")
    print()
    print("  Trying to create Triangle(1, 2, 10)...")
    print("  (Side 10 is longer than 1+2 — impossible in real life)")
    print()

    try:
        bad = Triangle(1, 2, 10)
    except ValueError as e:
        print(f"  ⚠  ValueError caught: {e}")
        print("  Good — the class protected us from invalid data.")


# ── INTERACTIVE MODE ─────────────────────────────────────────

def interactive():
    print()
    print("  ── Try It Yourself ──────────────────────────────────────────")
    shapes = []

    while True:
        print()
        print("  Add a shape:")
        print("  1. Circle")
        print("  2. Rectangle")
        print("  3. Triangle")
        print("  4. Done — show summary table")
        print()

        choice = input("  Choice (1-4): ").strip()

        if choice == "1":
            try:
                r   = float(input("  Radius: "))
                col = input("  Colour: ").strip() or "white"
                shapes.append(Circle(r, col))
                print("  ✔ Circle added.")
            except ValueError:
                print("  ⚠ Invalid input.")

        elif choice == "2":
            try:
                w   = float(input("  Width: "))
                h   = float(input("  Height: "))
                col = input("  Colour: ").strip() or "white"
                shapes.append(Rectangle(w, h, col))
                print("  ✔ Rectangle added.")
            except ValueError:
                print("  ⚠ Invalid input.")

        elif choice == "3":
            try:
                a   = float(input("  Side A: "))
                b   = float(input("  Side B: "))
                c   = float(input("  Side C: "))
                col = input("  Colour: ").strip() or "white"
                shapes.append(Triangle(a, b, c, col))
                print("  ✔ Triangle added.")
            except ValueError as e:
                print(f"  ⚠ {e}")

        elif choice == "4":
            if shapes:
                print_shape_summary(shapes)
            else:
                print("  ⚠ No shapes added yet.")
            break

        else:
            print("  ⚠ Please enter 1, 2, 3, or 4.")


# ── MAIN ─────────────────────────────────────────────────────

def main():
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║     SHAPES — OOP INHERITANCE         ║")
    print("  ║     Week 10 — Polymorphism           ║")
    print("  ╚══════════════════════════════════════╝")

    demo_individual()
    demo_polymorphism()
    demo_summary_table()
    demo_invalid_triangle()
    interactive()

    print()
    print("  ─────────────────────────────────────────────────────────")
    print("  KEY TAKEAWAY:")
    print("  print_shape_summary() works on ANY shape — now and in the future.")
    print("  You never had to write: 'if shape is a Circle... if shape is a Rectangle...'")
    print("  That is the power of polymorphism.")
    print("  ─────────────────────────────────────────────────────────")
    print()


if __name__ == "__main__":
    main()