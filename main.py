# main.py
# ─────────────────────────────────────────────────────────────────────────────
# MATHMATE — Entry point
#
# Tabs:  Shapes | Algebra | Trigonometry | Quiz | Leaderboard | Graph Plotter
#
# Architecture notes
# ──────────────────
# • Each tab is a self-contained Frame subclass in its own module.
# • Communication with the DB goes entirely through models.py (DAL layer).
# • db_init.create_and_seed_db() is idempotent — safe to call every launch.
# • The status bar at the bottom auto-refreshes after every user action via
#   the on_user_change() callback.
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

import db_init
import models
from shapes_module       import ShapesFrame
from algebra_module      import AlgebraFrame
from trig_module         import TrigFrame
from quiz_module         import QuizFrame
from leaderboard_module  import LeaderboardFrame
from graph_module        import GraphFrame


class MainApp:
    """Root application controller.  Owns the window, toolbar and notebook."""

    # ── Tab definitions: (attr_key, tab_label, FrameClass, bg_colour) ─────────
    _TABS = [
        ("shapes",       "🔷 Shapes",        ShapesFrame,       "#dff0d8"),
        ("algebra",      "📐 Algebra",        AlgebraFrame,      "#fff8e1"),
        ("trig",         "📏 Trigonometry",   TrigFrame,         "#e8f7ff"),
        ("quiz",         "🎯 Quiz",           QuizFrame,         "#fafafa"),
        ("leaderboard",  "🏆 Leaderboard",    LeaderboardFrame,  "#fdfefe"),
        ("graph",        "📈 Graph Plotter",  GraphFrame,        "#f0f4f8"),
    ]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MathMate")
        self.root.geometry("1100x740")
        self.root.minsize(900, 620)

        # Initialise DB (creates tables + seeds data if first run)
        db_init.create_and_seed_db()

        self._build_toolbar()
        self._build_notebook()
        self._build_statusbar()
        self._load_users()

    # ── Toolbar ───────────────────────────────────────────────────────────────

    def _build_toolbar(self) -> None:
        top = tk.Frame(self.root, bg="#2c3e50", pady=6)
        top.pack(fill="x")

        tk.Label(top, text="MathMate",
                 font=("Helvetica", 20, "bold"),
                 bg="#2c3e50", fg="#f1c40f").pack(side="left", padx=14)

        # User controls (right-aligned)
        tk.Button(top, text="Add User",
                  command=self._add_user,
                  bg="#27ae60", fg="white",
                  font=("Helvetica", 9, "bold"),
                  relief="flat").pack(side="right", padx=6)

        tk.Button(top, text="⟳ Refresh",
                  command=self._load_users,
                  bg="#3498db", fg="white",
                  relief="flat").pack(side="right")

        tk.Label(top, text="User:", bg="#2c3e50",
                 fg="white").pack(side="right", padx=(8, 2))

        self.users_combo = ttk.Combobox(top, state="readonly", width=18)
        self.users_combo.pack(side="right")
        self.users_combo.bind("<<ComboboxSelected>>",
                              lambda _: self._on_user_change())

    # ── Notebook ──────────────────────────────────────────────────────────────

    def _build_notebook(self) -> None:
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=6)

        self.frames: dict[str, tk.Frame] = {}

        for key, label, FrameClass, _bg in self._TABS:
            container = tk.Frame(self.notebook)
            self.notebook.add(container, text=label)
            frame = FrameClass(container, self.get_current_user)
            self.frames[key] = frame

        # Refresh leaderboard whenever that tab is switched to
        self.notebook.bind("<<NotebookTabChanged>>",
                           self._on_tab_change)

    # ── Status bar ────────────────────────────────────────────────────────────

    def _build_statusbar(self) -> None:
        self.status = tk.Label(self.root,
                               text="No user selected",
                               relief="sunken", anchor="w",
                               bg="#ecf0f1", fg="#2c3e50",
                               font=("Helvetica", 9))
        self.status.pack(fill="x", side="bottom")

    # ── User management ───────────────────────────────────────────────────────

    def _load_users(self) -> None:
        users = models.get_users()
        names = [u[1] for u in users]
        self.users_combo["values"] = names

    def _add_user(self) -> None:
        name = simpledialog.askstring("New User", "Enter username:")
        if not name:
            return
        name = name.strip()
        if not name:
            messagebox.showerror("Error", "Username cannot be empty.")
            return
        try:
            models.create_user(name)
            self._load_users()
            # Auto-select the newly created user
            self.users_combo.set(name)
            self._on_user_change()
            messagebox.showinfo("Success", f"User '{name}' created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_current_user(self):
        """Return the selected user row (id, username, points, level, quizzes)
        or None if nothing is selected."""
        sel = self.users_combo.get()
        return models.get_user_by_name(sel) if sel else None

    def _on_user_change(self) -> None:
        user = self.get_current_user()
        if user:
            _id, username, points, level, quizzes = user
            self.status.config(
                text=f"  👤 {username}   |   "
                     f"⭐ Points: {points}   |   "
                     f"🎓 Level: {level}   |   "
                     f"📝 Quizzes Completed: {quizzes}")
        else:
            self.status.config(text="No user selected")

    # ── Tab-change hook ───────────────────────────────────────────────────────

    def _on_tab_change(self, _event=None) -> None:
        """Refresh leaderboard automatically when its tab is activated."""
        try:
            selected = self.notebook.tab(self.notebook.select(), "text")
        except tk.TclError:
            return
        if "Leaderboard" in selected:
            self.frames["leaderboard"].refresh()
        # Refresh status bar so points stay current
        self._on_user_change()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app  = MainApp(root)
    root.mainloop()
