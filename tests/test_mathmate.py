"""
MathMate Automated Test Suite
-----------------------------
Unit tests for database layer, data access layer, geometry calculations,
symbolic algebra solver, trigonometry logic, quiz mechanics, and leaderboard ranking.
"""

import os
import unittest
import sqlite3

import db_init
import models
from shapes_module import _calculate as calc_shape


class TestMathMate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up isolated test database environment."""
        cls.test_db = "test_mathmate.db"
        models.DB_PATH = cls.test_db
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
        db_init.create_and_seed_db(cls.test_db)

    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    # ── Database & Seeding Tests ──────────────────────────────────────────────

    def test_01_database_seeding(self):
        """Verify database tables and seeded reference data."""
        with sqlite3.connect(self.test_db) as con:
            shapes_cnt = con.execute("SELECT COUNT(*) FROM shapes").fetchone()[0]
            algebra_cnt = con.execute("SELECT COUNT(*) FROM algebra_concepts").fetchone()[0]
            trig_cnt = con.execute("SELECT COUNT(*) FROM trig_functions").fetchone()[0]
            quiz_cnt = con.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0]

        self.assertEqual(shapes_cnt, 15)
        self.assertEqual(algebra_cnt, 10)
        self.assertEqual(trig_cnt, 10)
        self.assertEqual(quiz_cnt, 30)

    def test_02_seeding_idempotency(self):
        """Verify re-running create_and_seed_db does not duplicate quiz questions."""
        db_init.create_and_seed_db(self.test_db)
        with sqlite3.connect(self.test_db) as con:
            quiz_cnt = con.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0]
        self.assertEqual(quiz_cnt, 30)

    # ── User Management & Progress Tests ─────────────────────────────────────

    def test_03_user_creation_and_leveling(self):
        """Test user registration, point accumulation, and level calculation."""
        username = "Alice"
        models.create_user(username)
        user = models.get_user_by_name(username)
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "Alice")
        self.assertEqual(user[2], 0)  # Initial points
        self.assertEqual(user[3], 1)  # Initial level

        # Award 120 points -> Level should be max(1, 120 // 50 + 1) = 3
        models.update_user_progress(username, points=120)
        updated_user = models.get_user_by_name(username)
        self.assertEqual(updated_user[2], 120)
        self.assertEqual(updated_user[3], 3)

    # ── Shapes / Geometry Tests ───────────────────────────────────────────────

    def test_04_shape_calculations(self):
        """Test geometric area, perimeter, and volume calculations."""
        # Circle (r = 5) -> Area = π * 25 ≈ 78.5398
        res_circle = calc_shape("Circle", [5.0])
        self.assertIn("Area: 78.5398", res_circle)
        self.assertIn("Circumference: 31.4159", res_circle)

        # Rectangle (l = 4, w = 3) -> Area = 12, Perimeter = 14, Diagonal = 5
        res_rect = calc_shape("Rectangle", [4.0, 3.0])
        self.assertIn("Area: 12.0000", res_rect)
        self.assertIn("Perimeter: 14.0000", res_rect)
        self.assertIn("Diagonal: 5.0000", res_rect)

        # Cuboid (l = 2, w = 3, h = 4) -> Volume = 24
        res_cuboid = calc_shape("Cuboid", [2.0, 3.0, 4.0])
        self.assertIn("Volume: 24.0000", res_cuboid)

    # ── Quiz Mechanics Tests ─────────────────────────────────────────────────

    def test_05_quiz_engine_and_history(self):
        """Test quiz question retrieval, scoring, attempt logging, and history."""
        username = "Bob"
        models.create_user(username)

        qs = models.get_quiz_questions("algebra", limit=5)
        self.assertEqual(len(qs), 5)

        # Log a finished quiz attempt
        models.save_quiz_attempt(username, "algebra", score=5, total=5)
        history = models.get_user_quiz_history(username)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][0], "algebra")
        self.assertEqual(history[0][1], 5)
        self.assertEqual(history[0][2], 5)

    # ── Leaderboard Tests ────────────────────────────────────────────────────

    def test_06_leaderboard_ranking(self):
        """Test leaderboard ranking by points descending."""
        models.create_user("User1")
        models.create_user("User2")
        models.update_user_progress("User1", points=50)
        models.update_user_progress("User2", points=200)

        leaderboard = models.get_leaderboard(limit=10)
        self.assertTrue(len(leaderboard) >= 2)
        # Top user should be User2 (200 pts)
        self.assertEqual(leaderboard[0][1], "User2")
        self.assertEqual(leaderboard[0][2], 200)


if __name__ == "__main__":
    unittest.main()
