# models.py
# ─────────────────────────────────────────────────────────────────────────────
# DATA ACCESS LAYER
# All SQL queries are centralised here so the UI modules never touch the DB
# directly.  Keeps each module short and testable.
# ─────────────────────────────────────────────────────────────────────────────
import sqlite3

DB_PATH = "mathmate.db"


def _conn() -> sqlite3.Connection:
    """Return a connection to the active database."""
    return sqlite3.connect(DB_PATH)


# ── Users ────────────────────────────────────────────────────────────────────

def create_user(username: str) -> None:
    with _conn() as con:
        con.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))


def get_users() -> list:
    """Return all users sorted alphabetically."""
    with _conn() as con:
        return con.execute(
            "SELECT id, username, points, level, completed_quizzes "
            "FROM users ORDER BY username"
        ).fetchall()


def get_user_by_name(username: str):
    """Return a single user row or None."""
    with _conn() as con:
        return con.execute(
            "SELECT id, username, points, level, completed_quizzes "
            "FROM users WHERE username = ?", (username,)
        ).fetchone()


def update_user_progress(username: str, points: int = 0,
                         completed_quiz_inc: int = 0) -> None:
    """
    Add *points* to the user's total and optionally increment quiz count.
    Also recalculates level: every 50 points = 1 level (min 1).
    """
    with _conn() as con:
        con.execute(
            "UPDATE users "
            "SET points = points + ?, "
            "    completed_quizzes = completed_quizzes + ? "
            "WHERE username = ?",
            (points, completed_quiz_inc, username)
        )
        # Recalculate level based on new points total
        row = con.execute(
            "SELECT points FROM users WHERE username = ?", (username,)
        ).fetchone()
        if row:
            new_level = max(1, row[0] // 50 + 1)
            con.execute(
                "UPDATE users SET level = ? WHERE username = ?",
                (new_level, username)
            )


# ── Shapes ───────────────────────────────────────────────────────────────────

def get_shapes() -> list:
    """Return all shape rows including the new extra_notes column."""
    with _conn() as con:
        return con.execute(
            "SELECT id, name, description, formula_area, formula_perimeter, "
            "       COALESCE(extra_notes,'') "
            "FROM shapes ORDER BY name"
        ).fetchall()


# ── Algebra ──────────────────────────────────────────────────────────────────

def get_algebra_concepts() -> list:
    """Return all algebra concept rows including the new notes column."""
    with _conn() as con:
        return con.execute(
            "SELECT id, name, description, formula, example, "
            "       COALESCE(notes,'') "
            "FROM algebra_concepts ORDER BY id"
        ).fetchall()


# ── Trig ─────────────────────────────────────────────────────────────────────

def get_trig_functions() -> list:
    """Return all trig function rows including the new notes column."""
    with _conn() as con:
        return con.execute(
            "SELECT id, name, description, formula, COALESCE(notes,'') "
            "FROM trig_functions ORDER BY id"
        ).fetchall()


# ── Quiz ─────────────────────────────────────────────────────────────────────

def get_quiz_questions(topic: str, limit: int = 10) -> list:
    """
    Return *limit* questions for the given topic, randomised.
    Columns: id, topic, question_text, option_a-d, correct, difficulty, explanation
    """
    with _conn() as con:
        return con.execute(
            "SELECT id, topic, question_text, option_a, option_b, option_c, "
            "       option_d, correct, difficulty, explanation "
            "FROM quiz_questions "
            "WHERE topic = ? "
            "ORDER BY RANDOM() "
            "LIMIT ?",
            (topic, limit)
        ).fetchall()


def save_quiz_attempt(username: str, topic: str,
                      score: int, total: int) -> None:
    """Persist a finished quiz attempt and update user stats."""
    with _conn() as con:
        con.execute(
            "INSERT INTO quiz_attempts (username, topic, score, total) "
            "VALUES (?, ?, ?, ?)",
            (username, topic, score, total)
        )
    # Award points: 5 pts per correct answer, +20 bonus for perfect score
    pts = score * 5 + (20 if score == total else 0)
    update_user_progress(username, points=pts, completed_quiz_inc=1)


def get_user_quiz_history(username: str) -> list:
    """Return the 20 most recent quiz attempts for a user."""
    with _conn() as con:
        return con.execute(
            "SELECT topic, score, total, timestamp "
            "FROM quiz_attempts "
            "WHERE username = ? "
            "ORDER BY timestamp DESC LIMIT 20",
            (username,)
        ).fetchall()


# ── Leaderboard ──────────────────────────────────────────────────────────────

def get_leaderboard(limit: int = 10) -> list:
    """
    Return top *limit* users ranked by points descending.
    Columns: rank, username, points, level, completed_quizzes
    """
    with _conn() as con:
        rows = con.execute(
            "SELECT username, points, level, completed_quizzes "
            "FROM users "
            "ORDER BY points DESC "
            "LIMIT ?",
            (limit,)
        ).fetchall()
    return [(i + 1, *row) for i, row in enumerate(rows)]
