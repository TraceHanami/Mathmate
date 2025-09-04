# db_init.py
import sqlite3

def create_and_seed_db(db_path="mathmate.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        points INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        completed_quizzes INTEGER DEFAULT 0
    )
    """)

    # Shapes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shapes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        formula_area TEXT,
        formula_perimeter TEXT
    )
    """)

    # Algebra concepts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS algebra_concepts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        formula TEXT,
        example TEXT
    )
    """)

    # Trig functions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trig_functions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        formula TEXT
    )
    """)

    # Seed shapes (do not duplicate on multiple runs)
    shapes = [
        ("Circle", "All points equidistant from center.", "Area = π r²", "Perimeter = 2 π r"),
        ("Square", "Four equal sides and right angles.", "Area = a²", "Perimeter = 4 a"),
        ("Rectangle", "Opposite sides equal, right angles.", "Area = l × w", "Perimeter = 2(l + w)"),
        ("Triangle", "Three sided polygon. For area given base and height.", "Area = 0.5 × b × h", "Perimeter = a + b + c"),
        ("Ellipse", "Oval shape with major/minor axes.", "Area = π a b", "Perimeter ≈ π(3(a+b) - √((3a+b)(a+3b)))"),
        ("Cylinder", "3D with two circular bases.", "Surface Area = 2πr(r+h)", "Volume = π r² h")
    ]
    for s in shapes:
        cursor.execute("INSERT OR IGNORE INTO shapes (name, description, formula_area, formula_perimeter) VALUES (?, ?, ?, ?)", s)

    # Seed algebra concepts
    algebra = [
        ("Linear Equation", "Equation of first degree: ax + b = 0", "ax + b = 0", "2x + 3 = 0"),
        ("Quadratic Equation", "Second degree: ax² + bx + c = 0", "ax² + bx + c = 0", "x^2 - 5x + 6 = 0"),
        ("Laws of Exponents", "Rules for powers: a^m × a^n = a^(m+n)", "a^m × a^n = a^(m+n)", "2^3 * 2^2"),
        ("Factorization", "Expand / factor polynomials, (a + b)^2", "(a + b)^2 = a^2 + 2ab + b^2", "(x + 3)^2")
    ]
    for a in algebra:
        cursor.execute("INSERT OR IGNORE INTO algebra_concepts (name, description, formula, example) VALUES (?, ?, ?, ?)", a)

    # Seed trig functions
    trig = [
        ("Sine (sin)", "Opposite / Hypotenuse", "sin(θ) = opposite / hypotenuse"),
        ("Cosine (cos)", "Adjacent / Hypotenuse", "cos(θ) = adjacent / hypotenuse"),
        ("Tangent (tan)", "Opposite / Adjacent", "tan(θ) = opposite / adjacent"),
        ("Pythagorean Theorem", "a^2 + b^2 = c^2", "a^2 + b^2 = c^2")
    ]
    for t in trig:
        cursor.execute("INSERT OR IGNORE INTO trig_functions (name, description, formula) VALUES (?, ?, ?)", t)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_and_seed_db()
    print("DB created/seeded: mathmate.db")
