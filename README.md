# MathMate

### Interactive Mathematics Learning Platform

**Python • Tkinter • SQLite • SymPy • Matplotlib • NumPy**

---

## 📌 Overview

**MathMate** is a desktop-based interactive mathematics learning application built using Python and Tkinter. It provides a structured, self-contained environment for exploring **Geometry, Algebra, and Trigonometry**, supported by a dynamic quiz engine, leaderboard system, and an embedded mathematical graph plotter.

The application uses a local SQLite database (`mathmate.db`) to persist user profiles, quiz results, and reference data. It operates entirely offline with no external API dependencies.

---

## ✨ Core Features

### 🔷 Geometry Module

* 15 shapes (2D & 3D)
* Area, perimeter, and volume calculators
* Dynamic input field rendering
* Context-aware formula explanations

### 📐 Algebra Module

* 10 structured concepts including:

  * Linear & Quadratic Equations
  * Arithmetic & Geometric Progressions
  * Logarithms
  * Binomial Theorem
  * Systems of Equations
* Powered by **SymPy** for symbolic solving

### 📏 Trigonometry Module

* 6 primary trig ratios
* Pythagorean Theorem
* Law of Sines & Law of Cosines
* Inverse trigonometric functions
* Defensive checks for undefined values

### 🎯 Quiz Engine

* 30 seeded MCQs
* Randomized per session (`ORDER BY RANDOM()` in SQL)
* Instant feedback + detailed explanations
* Scoring + persistent attempt tracking

### 🏆 Leaderboard System

* Top-10 ranking table
* Click-to-sort functionality
* Dynamic bar chart visualization
* Per-user performance tracking

### 📈 Graph Plotter

* Embedded Matplotlib canvas
* Plot any NumPy-compatible expression
* Customizable X-range
* Built-in expression presets
* Safe evaluation namespace

### 👤 Multi-User Support

* User registration system
* Points & level tracking
* Quiz completion history
* Persistent progress storage

---

## 🗂 Project Structure

```
MathMate/
│
├── main.py
├── db_init.py
├── models.py
├── shapes_module.py
├── algebra_module.py
├── trig_module.py
├── quiz_module.py
├── leaderboard_module.py
├── graph_module.py
└── mathmate.db (auto-generated)
```

### Module Responsibilities

| File          | Responsibility                            |
| ------------- | ----------------------------------------- |
| `main.py`     | Application entry point, UI orchestration |
| `db_init.py`  | Database creation and seeding             |
| `models.py`   | Centralized data access layer             |
| `*_module.py` | Feature-specific UI + logic               |
| `mathmate.db` | SQLite database (auto-created)            |

---

## 🏗 Architecture

MathMate follows a clean **three-layer architecture**:

1. **Presentation Layer** – Tkinter UI modules
2. **Data Access Layer** – Centralized SQL logic in `models.py`
3. **Database Layer** – SQLite backend

### Database Schema

* `users`
* `shapes`
* `algebra_concepts`
* `trig_functions`
* `quiz_questions`
* `quiz_attempts`

All reference data is seeded safely using `INSERT OR IGNORE`.

---

## 🎮 Gamification System

| Action              | Points |
| ------------------- | ------ |
| Shape Calculation   | +1     |
| Algebra Calculation | +2     |
| Trig Calculation    | +2     |
| Correct Quiz Answer | +5     |
| Perfect Quiz Bonus  | +20    |

**Level System:**
Every 50 points = +1 Level (minimum Level 1)

---

## 🚀 Installation & Setup

### Requirements

* Python 3.10+
* tkinter
* sympy
* matplotlib
* numpy

---

### Option 1 — Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install sympy matplotlib numpy
python3 main.py
```

---

### Option 2 — Debian / Kali Linux

```bash
pip install sympy matplotlib numpy --break-system-packages
python3 main.py
```

---

### Option 3 — Using APT

```bash
sudo apt install python3-sympy python3-matplotlib python3-numpy
python3 main.py
```

---

### Running on WSL

* Windows 11 (WSLg): Works out of the box
* Windows 10: Install VcXsrv or Xming

```bash
export DISPLAY=:0
python3 main.py
```

---

## 📊 Design Decisions

* All SQL isolated in `models.py`
* UI modules do not directly access the database
* Defensive imports for optional dependencies
* Context-managed database connections
* Restricted namespace for safe `eval()` usage
* Dynamic input rendering via mapping dictionaries

---

## ⚠ Known Limitations

* Graph module requires matplotlib & numpy
* Quiz questions are seeded at DB creation
* No dark mode
* Triangle perimeter requires three side lengths

---

## 🔮 Future Enhancements

* Timed quiz mode
* Admin question management panel
* Export results to CSV/PDF
* Topic-wise performance analytics
* 3D shape visualization
* Theme toggle (Dark Mode)

---

## 🐛 Major Fixes (v1 → v2)

* Fixed level recalculation logic
* Enforced DB connection cleanup
* Added scrolling to long lists
* Guarded against null-user crashes
* Prevented trig division-by-zero errors
* Improved triangle perimeter validation

---

## 🧠 Technical Highlights

* Object-oriented modular design
* SQLite relational schema
* Symbolic mathematics via SymPy
* Embedded Matplotlib canvas integration
* Dynamic UI state rendering
* Secure evaluation sandboxing

---

## 📎 Quick Start

1. Install dependencies
2. Run `python3 main.py`
3. Add a user
4. Explore modules
5. Take quizzes
6. View leaderboard
7. Plot functions

---

## 📜 License

This project is intended for educational and academic purposes.

---
