# 🧮 MathMate

> **An interactive desktop mathematics learning platform built with Python and Tkinter.**

MathMate helps students explore Shapes, Algebra and Trigonometry through an intuitive topic browser, live calculators, a randomised quiz engine, a score leaderboard and an embedded function graph plotter — all running locally with no internet required.

---

## 📸 Features at a Glance

| Tab | Description |
|-----|-------------|
| 🔷 **Shapes** | 15 shapes — area, perimeter and volume calculators with extra formula notes |
| 📐 **Algebra** | 10 concepts — linear/quadratic equations, AP/GP, logarithms, binomial theorem and more |
| 📏 **Trigonometry** | 10 functions — all 6 ratios, Pythagorean theorem, Law of Sines & Cosines, inverse trig |
| 🎯 **Quiz Mode** | 30 seeded MCQs, randomised per session, with instant feedback and explanations |
| 🏆 **Leaderboard** | Sortable top-10 table + live bar chart comparing all registered users |
| 📈 **Graph Plotter** | Plot any numpy-compatible expression over a custom x-range with 12 quick presets |
| 👤 **User Profiles** | Multi-user support — points, level and quiz history tracked per user in SQLite |

---

## 🗂️ Project Structure

```
Mathmate/
├── main.py                 # Entry point — root window, toolbar, 6-tab notebook
├── db_init.py              # Schema creation and data seeding (idempotent)
├── models.py               # Data access layer — all SQL lives here
├── shapes_module.py        # ShapesFrame — 15 shapes with dynamic input fields
├── algebra_module.py       # AlgebraFrame — 10 algebra concepts + calculators
├── trig_module.py          # TrigFrame — 10 trig functions + calculators
├── quiz_module.py          # QuizFrame — MCQ engine, scoring, history panel
├── leaderboard_module.py   # LeaderboardFrame — Treeview table + Canvas bar chart
├── graph_module.py         # GraphFrame — matplotlib plotter embedded in Tkinter
└── mathmate.db             # Auto-generated SQLite database (created on first run)
```

---

## ⚙️ Requirements

| Dependency | Purpose | Required? |
|------------|---------|-----------|
| Python 3.10+ | Runtime | ✅ Yes |
| tkinter | GUI framework (bundled with Python) | ✅ Yes |
| sympy | Symbolic maths (algebra solver) | ✅ Yes |
| matplotlib | Graph plotter tab | ⚠️ Optional* |
| numpy | Expression evaluation in plotter | ⚠️ Optional* |

> *If `matplotlib` is not installed, the Graph Plotter tab shows a friendly install prompt instead of crashing the app.

---

## 🚀 Installation

### Option A — Virtual Environment *(Recommended)*

```bash
git clone https://github.com/yourname/mathmate.git
cd mathmate

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install sympy matplotlib
python3 main.py
```

Next time, just activate and run:

```bash
source venv/bin/activate
python3 main.py
```

---

### Option B — System-wide *(Kali / Debian / Ubuntu)*

```bash
pip install sympy matplotlib --break-system-packages
python3 main.py
```

---

### Option C — APT packages

```bash
sudo apt install python3-sympy python3-matplotlib
python3 main.py
```

---

### Option D — Windows (Native Python)

```cmd
cd C:\path\to\Mathmate
pip install sympy matplotlib
python main.py
```

---

## 🖥️ Running on WSL / Kali Linux

MathMate uses Tkinter which requires a graphical display.

**WSL2 + Windows 11** — WSLg is built-in, no extra steps needed:

```bash
python3 main.py
```

**WSL2 + Windows 10** — Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [Xming](https://sourceforge.net/projects/xming/), launch it, then:

```bash
export DISPLAY=:0
python3 main.py
```

---

## 🏗️ Architecture

MathMate follows a clean three-layer design:

```
┌─────────────────────────────────────────────────────┐
│              Presentation Layer                      │
│  main.py  →  *_module.py  (one Frame per tab)       │
├─────────────────────────────────────────────────────┤
│              Data Access Layer                       │
│  models.py  (all SQL queries centralised here)      │
├─────────────────────────────────────────────────────┤
│              Database Layer                          │
│  db_init.py  →  mathmate.db  (SQLite)               │
└─────────────────────────────────────────────────────┘
```

**UI modules never touch the database directly** — they only call functions in `models.py`. This keeps each module short, focused and independently testable.

---

## 🗃️ Database Schema

Six tables are managed by `db_init.py`:

| Table | Rows Seeded | Description |
|-------|------------|-------------|
| `users` | 0 (user-created) | username, points, level, completed_quizzes |
| `shapes` | 15 | name, description, area formula, perimeter formula, extra notes |
| `algebra_concepts` | 10 | name, description, formula, worked example, notes |
| `trig_functions` | 10 | name, description, formula, notes |
| `quiz_questions` | 30 | topic, question, 4 options, correct answer, difficulty (1–3), explanation |
| `quiz_attempts` | grows | username, topic, score, total, timestamp |

The database is **fully seeded on first run** and is safe to delete and regenerate at any time.

---

## 🎯 User Progression System

Points are awarded automatically on every interaction:

| Action | Points |
|--------|--------|
| Shape calculation | +1 |
| Algebra calculation | +2 |
| Trigonometry calculation | +2 |
| Each correct quiz answer | +5 |
| Perfect quiz score bonus | +20 |
| **Level up** | Every 50 points = +1 level |

---

## 📚 Module Reference

### `shapes_module.py`
Supports **15 shapes**: Circle, Square, Rectangle, Triangle, Ellipse, Pentagon, Hexagon, Octagon, Trapezoid, Rhombus, Parallelogram, Cylinder, Cone, Sphere, Cuboid. Input fields are generated dynamically from an `_INPUT_MAP` dictionary. The `_calculate()` function is decoupled from the UI for easy unit testing.

### `algebra_module.py`
Supports **10 concepts**: Linear Equation, Quadratic Equation, Laws of Exponents, Factorization, Arithmetic Progression, Geometric Progression, Logarithms, Binomial Theorem, System of Linear Equations, Inequalities. Uses SymPy for symbolic solving and shows the discriminant for quadratics.

### `trig_module.py`
Supports **10 functions**: sin, cos, tan, cot, sec, csc, Pythagorean Theorem, Law of Sines, Law of Cosines, Inverse Trig. Division-by-zero is guarded for all reciprocal functions. The input hint label updates dynamically per function.

### `quiz_module.py`
Draws up to 10 random questions per topic via `ORDER BY RANDOM()`. Buttons turn green (correct) or red (wrong) after answering, with the stored explanation shown immediately. On completion, `models.save_quiz_attempt()` persists the result, awards points, and increments the quiz counter.

### `leaderboard_module.py`
Queries the top 10 users from `models.get_leaderboard()`. The Treeview table supports click-to-sort on any column. The bar chart is drawn with `tk.Canvas` (no extra libraries needed). The current user's row and bar are highlighted in green.

### `graph_module.py`
Embeds a `matplotlib` Figure via `FigureCanvasTkAgg`. Expressions are evaluated with `numpy` in a sandboxed `eval()` namespace exposing only `np` and `x`. Values exceeding `1e6` are masked to `NaN` to prevent runaway y-axis scales. Imports defensively — missing matplotlib shows a prompt, not a crash.

---

## 🐛 Bug Fixes (v1 → v2)

| Bug | Fix |
|-----|-----|
| Level never updated | `update_user_progress()` now recalculates level from total points on every call |
| DB connections not closed | All queries use `with sqlite3.connect()` context managers |
| No scroll on long sidebar lists | All sidebars use a `Canvas` + `Scrollbar` wrapper |
| No user selected → crash | All modules guard with early returns and `messagebox` warnings |
| `tan`/`cot`/`sec`/`csc` ZeroDivisionError | Near-zero denominator checks added for all reciprocal functions |
| Triangle perimeter mismatch | UI now clarifies that perimeter requires all 3 side lengths |

---

## 🔮 Roadmap

- [ ] Timed quiz mode with a per-question countdown
- [ ] Admin panel to add custom quiz questions through the UI
- [ ] Export quiz results to CSV or PDF
- [ ] Per-topic accuracy statistics over time
- [ ] 3-D shape visualisation using matplotlib's toolkit
- [ ] Dark mode toggle stored in user preferences

---

## 📄 License

This project is open source. Feel free to use, modify and distribute it for educational purposes.

---

## 👤 Author

**TraceHanami**
Built with Python, Tkinter, SQLite, SymPy and Matplotlib.
