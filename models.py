# models.py
import sqlite3

DB_PATH = "mathmate.db"

def connect():
    return sqlite3.connect(DB_PATH)

# Users
def create_user(username):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def get_users():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, username, points, level, completed_quizzes FROM users ORDER BY username")
    users = c.fetchall()
    conn.close()
    return users

def get_user_by_name(username):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, username, points, level, completed_quizzes FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def update_user_progress(username, points=0, completed_quiz_inc=0):
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE users SET points = points + ?, completed_quizzes = completed_quizzes + ? WHERE username = ?", (points, completed_quiz_inc, username))
    conn.commit()
    conn.close()

# Shapes
def get_shapes():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, name, description, formula_area, formula_perimeter FROM shapes ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return rows

# Algebra
def get_algebra_concepts():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, name, description, formula, example FROM algebra_concepts ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return rows

# Trig
def get_trig_functions():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, name, description, formula FROM trig_functions ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows
