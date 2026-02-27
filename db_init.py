# db_init.py
# ─────────────────────────────────────────────────────────────────────────────
# DATABASE INITIALISATION & SEEDING
# Responsibilities:
#   • Create all tables (users, shapes, algebra_concepts, trig_functions,
#     quiz_questions, quiz_attempts)
#   • Seed reference data so the app works out-of-the-box
#   • Safe to call multiple times – uses INSERT OR IGNORE throughout
# ─────────────────────────────────────────────────────────────────────────────
import sqlite3


def create_and_seed_db(db_path: str = "mathmate.db") -> None:
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    # ── DDL ──────────────────────────────────────────────────────────────────

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        username         TEXT    UNIQUE NOT NULL,
        points           INTEGER DEFAULT 0,
        level            INTEGER DEFAULT 1,
        completed_quizzes INTEGER DEFAULT 0
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS shapes (
        id                 INTEGER PRIMARY KEY AUTOINCREMENT,
        name               TEXT UNIQUE NOT NULL,
        description        TEXT,
        formula_area       TEXT,
        formula_perimeter  TEXT,
        extra_notes        TEXT   -- NEW: extra context / tips shown in the UI
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS algebra_concepts (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT UNIQUE NOT NULL,
        description TEXT,
        formula     TEXT,
        example     TEXT,
        notes       TEXT   -- NEW: additional worked notes
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trig_functions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT UNIQUE NOT NULL,
        description TEXT,
        formula     TEXT,
        notes       TEXT   -- NEW
    )""")

    # NEW: stores every quiz question across all topics
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        topic         TEXT NOT NULL,          -- 'shapes' | 'algebra' | 'trig'
        question_text TEXT NOT NULL,
        option_a      TEXT NOT NULL,
        option_b      TEXT NOT NULL,
        option_c      TEXT NOT NULL,
        option_d      TEXT NOT NULL,
        correct       TEXT NOT NULL,          -- 'a' | 'b' | 'c' | 'd'
        difficulty    INTEGER DEFAULT 1,      -- 1=easy 2=medium 3=hard
        explanation   TEXT                    -- shown after answering
    )""")

    # NEW: records every quiz session a user completes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT NOT NULL,
        topic       TEXT NOT NULL,
        score       INTEGER NOT NULL,
        total       INTEGER NOT NULL,
        timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
    )""")

    # ── SEED: Shapes ─────────────────────────────────────────────────────────
    shapes = [
        # (name, description, formula_area, formula_perimeter, extra_notes)
        ("Circle",
         "All points equidistant from the centre.",
         "Area = π r²",
         "Circumference = 2 π r",
         "r = radius. Diameter = 2r."),

        ("Square",
         "Four equal sides and four right angles.",
         "Area = a²",
         "Perimeter = 4 a",
         "a = side length. Diagonal = a√2."),

        ("Rectangle",
         "Opposite sides equal, all angles 90°.",
         "Area = l × w",
         "Perimeter = 2(l + w)",
         "l = length, w = width. Diagonal = √(l²+w²)."),

        ("Triangle",
         "Three-sided polygon. General area formula uses base and height.",
         "Area = 0.5 × b × h",
         "Perimeter = a + b + c",
         "For right triangles use Pythagoras. Hero's formula: A=√(s(s-a)(s-b)(s-c)) where s=(a+b+c)/2."),

        ("Ellipse",
         "Oval with semi-major axis a and semi-minor axis b.",
         "Area = π a b",
         "Perimeter ≈ π[3(a+b) − √((3a+b)(a+3b))]",
         "Ramanujan's approximation. For a circle, a = b = r."),

        ("Cylinder",
         "3-D solid with two circular bases and a curved lateral surface.",
         "Surface Area = 2πr(r + h)",
         "Volume = π r² h",
         "Lateral surface area only = 2πrh."),

        ("Pentagon",
         "Regular 5-sided polygon.",
         "Area = (s²/4) × √(25 + 10√5)",
         "Perimeter = 5 s",
         "s = side length. Interior angle = 108°."),

        ("Hexagon",
         "Regular 6-sided polygon.",
         "Area = (3√3 / 2) × s²",
         "Perimeter = 6 s",
         "s = side length. Interior angle = 120°. Common in nature (honeycombs)."),

        ("Octagon",
         "Regular 8-sided polygon.",
         "Area = 2(1 + √2) × s²",
         "Perimeter = 8 s",
         "s = side length. Interior angle = 135°."),

        ("Trapezoid",
         "Quadrilateral with one pair of parallel sides (bases).",
         "Area = 0.5 × (b₁ + b₂) × h",
         "Perimeter = b₁ + b₂ + leg₁ + leg₂",
         "b₁, b₂ = parallel sides; h = height between them."),

        ("Rhombus",
         "Parallelogram with all four sides equal.",
         "Area = 0.5 × d₁ × d₂",
         "Perimeter = 4 s",
         "d₁, d₂ = diagonals; they bisect each other at 90°."),

        ("Parallelogram",
         "Opposite sides parallel and equal.",
         "Area = b × h",
         "Perimeter = 2(a + b)",
         "h = perpendicular height (not the slant side)."),

        ("Cone",
         "3-D solid with a circular base tapering to an apex.",
         "Surface Area = πr(r + l)  where l = slant = √(r²+h²)",
         "Volume = (1/3) π r² h",
         "l = slant height. Lateral surface = πrl."),

        ("Sphere",
         "Perfectly round 3-D object.",
         "Surface Area = 4 π r²",
         "Volume = (4/3) π r³",
         "Every cross-section through the centre is a circle."),

        ("Cuboid",
         "3-D rectangle (box) with 6 rectangular faces.",
         "Surface Area = 2(lw + lh + wh)",
         "Volume = l × w × h",
         "Diagonal = √(l²+w²+h²)."),
    ]
    for s in shapes:
        cur.execute(
            "INSERT OR IGNORE INTO shapes "
            "(name, description, formula_area, formula_perimeter, extra_notes) "
            "VALUES (?, ?, ?, ?, ?)", s)

    # ── SEED: Algebra concepts ───────────────────────────────────────────────
    algebra = [
        # (name, description, formula, example, notes)
        ("Linear Equation",
         "Polynomial of degree 1: ax + b = 0. Has exactly one solution.",
         "ax + b = 0  →  x = −b/a",
         "2x + 6 = 0  →  x = −3",
         "Graphically a straight line. Slope-intercept form: y = mx + c."),

        ("Quadratic Equation",
         "Polynomial of degree 2: ax² + bx + c = 0. Up to two real solutions.",
         "x = (−b ± √(b²−4ac)) / (2a)",
         "x²−5x+6=0  →  x=2, x=3",
         "Discriminant D=b²−4ac: D>0 two real roots; D=0 one root; D<0 complex roots."),

        ("Laws of Exponents",
         "Rules that govern powers and roots.",
         "aᵐ·aⁿ=aᵐ⁺ⁿ | aᵐ/aⁿ=aᵐ⁻ⁿ | (aᵐ)ⁿ=aᵐⁿ | a⁰=1",
         "2³ × 2² = 2⁵ = 32",
         "Negative exponent: a⁻ⁿ = 1/aⁿ. Fractional: a^(1/n) = ⁿ√a."),

        ("Factorization",
         "Rewrite a polynomial as a product of simpler factors.",
         "(a+b)²=a²+2ab+b² | (a−b)²=a²−2ab+b² | (a+b)(a−b)=a²−b²",
         "(x+3)²=x²+6x+9",
         "Always check for a common factor first. Useful for solving quadratics."),

        ("Arithmetic Progression (AP)",
         "Sequence with a constant difference d between consecutive terms.",
         "Tₙ = a+(n−1)d | Sₙ = n/2·[2a+(n−1)d]",
         "2,5,8,11 … a=2, d=3, T₅=14",
         "a = first term, d = common difference, n = number of terms."),

        ("Geometric Progression (GP)",
         "Sequence where each term is multiplied by a constant ratio r.",
         "Tₙ = a·rⁿ⁻¹ | Sₙ = a(rⁿ−1)/(r−1) for r≠1",
         "3,6,12,24 … a=3, r=2, T₄=24",
         "Sum to infinity (|r|<1): S∞ = a/(1−r)."),

        ("Logarithms",
         "Inverse of exponentiation: logₐ(x)=y  means  aʸ=x.",
         "log(xy)=log x+log y | log(x/y)=log x−log y | log(xⁿ)=n·log x",
         "log₂(8)=3  since 2³=8",
         "Change of base: logₐ(b)=log(b)/log(a). Natural log: ln = logₑ."),

        ("Binomial Theorem",
         "Expansion of (a+b)ⁿ for any positive integer n.",
         "(a+b)ⁿ = Σ C(n,k) aⁿ⁻ᵏ bᵏ  (k from 0 to n)",
         "(x+1)³ = x³+3x²+3x+1",
         "C(n,k) = n!/(k!(n−k)!). Pascal's triangle gives the coefficients."),

        ("System of Linear Equations",
         "Two or more equations solved simultaneously.",
         "Substitution | Elimination | Matrix (Cramer's rule)",
         "x+y=5, x−y=1 → x=3, y=2",
         "Unique solution if lines intersect; no solution if parallel; infinite if same line."),

        ("Inequalities",
         "Expressions comparing two quantities using <, >, ≤, ≥.",
         "Rules: flip inequality when multiplying/dividing by a negative.",
         "2x+3 > 7  →  x > 2",
         "Compound: a < x < b. Plot on number line or coordinate plane."),
    ]
    for a in algebra:
        cur.execute(
            "INSERT OR IGNORE INTO algebra_concepts "
            "(name, description, formula, example, notes) "
            "VALUES (?, ?, ?, ?, ?)", a)

    # ── SEED: Trig functions ─────────────────────────────────────────────────
    trig = [
        # (name, description, formula, notes)
        ("Sine (sin)",
         "Ratio of the opposite side to the hypotenuse in a right triangle.",
         "sin(θ) = opposite / hypotenuse",
         "Range [−1, 1]. Period 360°. sin(0°)=0, sin(90°)=1."),

        ("Cosine (cos)",
         "Ratio of the adjacent side to the hypotenuse.",
         "cos(θ) = adjacent / hypotenuse",
         "Range [−1, 1]. Period 360°. cos(0°)=1, cos(90°)=0."),

        ("Tangent (tan)",
         "Ratio of the opposite side to the adjacent side.",
         "tan(θ) = opposite / adjacent = sin(θ)/cos(θ)",
         "Undefined at 90°, 270°. Period 180°."),

        ("Cotangent (cot)",
         "Reciprocal of tangent.",
         "cot(θ) = adjacent / opposite = cos(θ)/sin(θ)",
         "Undefined at 0°, 180°."),

        ("Secant (sec)",
         "Reciprocal of cosine.",
         "sec(θ) = hypotenuse / adjacent = 1/cos(θ)",
         "Undefined at 90°, 270°. Range: (−∞,−1]∪[1,∞)."),

        ("Cosecant (csc)",
         "Reciprocal of sine.",
         "csc(θ) = hypotenuse / opposite = 1/sin(θ)",
         "Undefined at 0°, 180°."),

        ("Pythagorean Theorem",
         "Relates the three sides of a right-angled triangle.",
         "a² + b² = c²  (c = hypotenuse)",
         "Also: sin²(θ)+cos²(θ)=1 (Pythagorean identity)."),

        ("Law of Sines",
         "Relates sides and opposite angles in any triangle.",
         "a/sin(A) = b/sin(B) = c/sin(C)",
         "Useful when you know two angles and one side (AAS/ASA)."),

        ("Law of Cosines",
         "Generalisation of Pythagoras for any triangle.",
         "c² = a² + b² − 2ab·cos(C)",
         "Useful for SAS or SSS triangles. Reduces to Pythagoras when C=90°."),

        ("Inverse Trig (arcsin/arccos/arctan)",
         "Find the angle when the ratio is known.",
         "θ = arcsin(x), arccos(x), arctan(x)",
         "arcsin range [−90°,90°]; arccos [0°,180°]; arctan (−90°,90°)."),
    ]
    for t in trig:
        cur.execute(
            "INSERT OR IGNORE INTO trig_functions "
            "(name, description, formula, notes) "
            "VALUES (?, ?, ?, ?)", t)

    # ── SEED: Quiz questions ─────────────────────────────────────────────────
    quiz_qs = [
        # ── SHAPES ──
        ("shapes","What is the area of a circle with radius 5?",
         "25π","50π","10π","5π","a",1,"Area = πr² = π(25) = 25π"),
        ("shapes","What is the perimeter of a square with side 7?",
         "28","49","14","21","a",1,"Perimeter = 4s = 4×7 = 28"),
        ("shapes","A rectangle has length 8 and width 3. What is its area?",
         "24","22","11","48","a",1,"Area = l×w = 8×3 = 24"),
        ("shapes","What is the volume of a cylinder with r=3 and h=5?",
         "45π","15π","30π","9π","a",2,"Volume = πr²h = π×9×5 = 45π"),
        ("shapes","For a regular hexagon with side 4, what is its area?",
         "24√3","16√3","48√3","12√3","a",2,"Area = (3√3/2)s² = (3√3/2)×16 = 24√3"),
        ("shapes","What is the slant height of a cone with r=3 and h=4?",
         "5","7","√7","12","a",2,"l = √(r²+h²) = √(9+16) = √25 = 5"),
        ("shapes","Surface area of a sphere with radius 6?",
         "144π","36π","72π","216π","a",2,"SA = 4πr² = 4π×36 = 144π"),
        ("shapes","Area of a triangle with base 10 and height 6?",
         "30","60","15","24","a",1,"Area = 0.5×b×h = 0.5×10×6 = 30"),
        ("shapes","Area of a trapezoid with bases 6 & 10 and height 4?",
         "32","24","40","16","a",2,"Area = 0.5×(6+10)×4 = 32"),
        ("shapes","Perimeter of a regular octagon with side 5?",
         "40","35","45","50","a",1,"Perimeter = 8s = 8×5 = 40"),

        # ── ALGEBRA ──
        ("algebra","Solve: 3x + 9 = 0",
         "x = −3","x = 3","x = 9","x = 0","a",1,"3x = −9  →  x = −3"),
        ("algebra","Solve: x² − 7x + 12 = 0",
         "x=3, x=4","x=2, x=6","x=1, x=12","x=−3, x=−4","a",2,"Factors: (x−3)(x−4)=0"),
        ("algebra","What is 2³ × 2⁴?",
         "128","64","256","32","a",1,"2³×2⁴ = 2⁷ = 128"),
        ("algebra","Expand (x + 5)²",
         "x²+10x+25","x²+25","x²+5x+25","x²+10x+5","a",1,"(a+b)²=a²+2ab+b²"),
        ("algebra","5th term of AP: a=3, d=4?",
         "19","17","21","15","a",2,"T₅ = 3+(5−1)×4 = 19"),
        ("algebra","Sum of first 5 terms of GP: a=2, r=3?",
         "242","120","243","60","a",2,"S₅ = 2(3⁵−1)/(3−1) = 2×242/2 = 242"),
        ("algebra","log₂(32) = ?",
         "5","4","6","8","a",1,"2⁵ = 32"),
        ("algebra","Discriminant of x²+4x+5?",
         "−4","−16","4","16","a",2,"D = b²−4ac = 16−20 = −4"),
        ("algebra","Solve the system: x+y=7, x−y=3",
         "x=5, y=2","x=3, y=4","x=4, y=3","x=2, y=5","a",2,"Add: 2x=10→x=5; sub: y=2"),
        ("algebra","Solve: 3x − 5 > 7",
         "x > 4","x > 2","x < 4","x > 12","a",1,"3x > 12  →  x > 4"),

        # ── TRIG ──
        ("trig","sin(30°) = ?",
         "0.5","√3/2","1","√2/2","a",1,"sin(30°) = 1/2 = 0.5"),
        ("trig","cos(60°) = ?",
         "0.5","√3/2","1","0","a",1,"cos(60°) = 1/2"),
        ("trig","tan(45°) = ?",
         "1","0","√3","1/√3","a",1,"tan(45°) = sin/cos = 1"),
        ("trig","In a right triangle, a=6, b=8. Find the hypotenuse.",
         "10","14","7","12","a",1,"c = √(36+64) = √100 = 10"),
        ("trig","sin²(θ) + cos²(θ) = ?",
         "1","0","sin(2θ)","2","a",1,"Fundamental Pythagorean identity"),
        ("trig","cot(θ) = ?",
         "cos/sin","sin/cos","1/sin","1/cos","a",2,"cot = adjacent/opposite = cos/sin"),
        ("trig","sec(0°) = ?",
         "1","0","∞","−1","a",1,"sec = 1/cos, cos(0°)=1"),
        ("trig","Law of Sines: if A=30°, a=5, b=10, find B.",
         "90°","60°","45°","120°","a",3,"sin(B)=b·sin(A)/a = 10×0.5/5 = 1 → B=90°"),
        ("trig","cos(90°) = ?",
         "0","1","−1","0.5","a",1,"cos(90°) = 0"),
        ("trig","Using Law of Cosines, c²=a²+b²−2ab·cos(C). If a=5,b=7,C=60°, find c².",
         "39","74","11","25","a",3,"c²=25+49−2×5×7×0.5=74−35=39"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO quiz_questions "
        "(topic,question_text,option_a,option_b,option_c,option_d,correct,difficulty,explanation) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        quiz_qs
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_and_seed_db()
    print("mathmate.db created / seeded successfully.")
