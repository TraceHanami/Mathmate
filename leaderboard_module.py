# leaderboard_module.py
# ─────────────────────────────────────────────────────────────────────────────
# LEADERBOARD TAB
# Shows top users ranked by points with level, quiz count, and a simple
# visual bar chart built entirely from Tkinter (no external lib needed).
# Refreshes every time the user clicks "Refresh" or the tab is opened.
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk
import models


# Colour palette for the bar chart — cycles if > 10 users
_BAR_COLOURS = [
    "#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f39c12",
    "#1abc9c", "#e67e22", "#34495e", "#c0392b", "#27ae60",
]

# Medal emojis for top 3
_MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


class LeaderboardFrame(tk.Frame):

    def __init__(self, parent, current_user_callback):
        super().__init__(parent, bg="#fdfefe")
        self.current_user_callback = current_user_callback
        self.pack(fill="both", expand=True)
        self._build_ui()
        self.refresh()   # populate immediately

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(self, bg="#2c3e50", pady=8)
        header.pack(fill="x")

        tk.Label(header, text="🏆  Leaderboard",
                 font=("Helvetica", 16, "bold"),
                 bg="#2c3e50", fg="white").pack(side="left", padx=14)

        tk.Button(header, text="⟳  Refresh",
                  command=self.refresh,
                  bg="#27ae60", fg="white",
                  font=("Helvetica", 10, "bold"),
                  padx=8).pack(side="right", padx=12)

        # ── Main body split: table left, chart right ──────────────────────────
        body = tk.Frame(self, bg="#fdfefe")
        body.pack(fill="both", expand=True, padx=12, pady=10)

        # -- Table (left half) -------------------------------------------------
        left = tk.Frame(body, bg="#fdfefe")
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="Top Players", font=("Helvetica", 12, "bold"),
                 bg="#fdfefe").pack(anchor="w", pady=(0, 4))

        cols = ("rank", "username", "points", "level", "quizzes")
        self.tree = ttk.Treeview(left, columns=cols, show="headings",
                                 height=12, selectmode="browse")

        col_cfg = {
            "rank":     ("Rank",    60,  "center"),
            "username": ("Player", 160,  "w"),
            "points":   ("Points",  80,  "center"),
            "level":    ("Level",   60,  "center"),
            "quizzes":  ("Quizzes", 70,  "center"),
        }
        for cid, (heading, width, anchor) in col_cfg.items():
            self.tree.heading(cid, text=heading,
                              command=lambda c=cid: self._sort(c))
            self.tree.column(cid, width=width, anchor=anchor)

        # Striped row tags
        self.tree.tag_configure("odd",  background="#eaf2ff")
        self.tree.tag_configure("even", background="#ffffff")
        self.tree.tag_configure("gold", background="#fef9e7",
                                font=("Helvetica", 10, "bold"))
        self.tree.tag_configure("current_user", background="#d5f5e3")

        vsb = ttk.Scrollbar(left, orient="vertical",
                             command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Totals label
        self.lbl_totals = tk.Label(left, text="", bg="#fdfefe",
                                   font=("Helvetica", 9), fg="#7f8c8d")
        self.lbl_totals.pack(anchor="w", pady=2)

        # -- Bar Chart (right half) --------------------------------------------
        right = tk.Frame(body, bg="#fdfefe")
        right.pack(side="right", fill="both", expand=True, padx=(16, 0))

        tk.Label(right, text="Points Comparison",
                 font=("Helvetica", 12, "bold"),
                 bg="#fdfefe").pack(anchor="w", pady=(0, 4))

        self.canvas = tk.Canvas(right, bg="#ffffff",
                                relief="sunken", bd=1)
        self.canvas.pack(fill="both", expand=True)

        # Subscribe to resize so chart redraws
        self.canvas.bind("<Configure>", lambda e: self._draw_chart())

        self._chart_data: list = []   # cached for redraws

    # ── Data refresh ─────────────────────────────────────────────────────────

    def refresh(self) -> None:
        rows  = models.get_leaderboard(limit=10)   # list of (rank,user,pts,lvl,qz)
        user  = self.current_user_callback()
        me    = user[1] if user else None

        # -- Populate tree -----------------------------------------------------
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, (rank, username, points, level, quizzes) in enumerate(rows):
            medal = _MEDALS.get(rank, str(rank))
            tags  = []
            if rank == 1:
                tags.append("gold")
            elif i % 2 == 0:
                tags.append("even")
            else:
                tags.append("odd")
            if username == me:
                tags.append("current_user")

            self.tree.insert("", "end",
                             values=(medal, username, points, level, quizzes),
                             tags=tags)

        total_users = len(models.get_users())
        self.lbl_totals.config(
            text=f"Showing top {len(rows)} of {total_users} registered players")

        # -- Cache and draw chart ----------------------------------------------
        self._chart_data = [(username, points, username == me)
                            for _, username, points, *_ in rows]
        self._draw_chart()

    # ── Bar chart ────────────────────────────────────────────────────────────

    def _draw_chart(self) -> None:
        c = self.canvas
        c.delete("all")

        data = self._chart_data
        if not data:
            c.create_text(c.winfo_width() // 2, c.winfo_height() // 2,
                          text="No data yet", font=("Helvetica", 11),
                          fill="#95a5a6")
            return

        W = c.winfo_width()
        H = c.winfo_height()
        if W < 10 or H < 10:
            return   # not yet laid out

        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 60
        chart_w = W - pad_l - pad_r
        chart_h = H - pad_t - pad_b

        max_pts = max((pts for _, pts, _ in data), default=1) or 1

        bar_w    = chart_w / len(data) * 0.6
        spacing  = chart_w / len(data)

        # Y-axis
        c.create_line(pad_l, pad_t, pad_l, pad_t + chart_h, fill="#95a5a6")
        # X-axis
        c.create_line(pad_l, pad_t + chart_h,
                      pad_l + chart_w, pad_t + chart_h, fill="#95a5a6")

        # Y gridlines / labels
        for pct in (0.25, 0.5, 0.75, 1.0):
            y    = pad_t + chart_h * (1 - pct)
            pts  = round(max_pts * pct)
            c.create_line(pad_l, y, pad_l + chart_w, y,
                          fill="#ecf0f1", dash=(3, 3))
            c.create_text(pad_l - 4, y, text=str(pts),
                          anchor="e", font=("Helvetica", 7), fill="#7f8c8d")

        # Bars
        for i, (username, pts, is_me) in enumerate(data):
            x_centre = pad_l + spacing * i + spacing / 2
            bar_h    = chart_h * (pts / max_pts) if max_pts else 0
            x0 = x_centre - bar_w / 2
            x1 = x_centre + bar_w / 2
            y0 = pad_t + chart_h - bar_h
            y1 = pad_t + chart_h

            colour = "#27ae60" if is_me else _BAR_COLOURS[i % len(_BAR_COLOURS)]
            c.create_rectangle(x0, y0, x1, y1, fill=colour, outline="")

            # Value label on top of bar
            c.create_text(x_centre, y0 - 4, text=str(pts),
                          font=("Helvetica", 8, "bold"), fill="#2c3e50")

            # Username label at bottom (rotated text not easily done in Canvas
            # so we truncate to fit)
            short = username[:8] + "…" if len(username) > 9 else username
            c.create_text(x_centre, y1 + 10, text=short,
                          font=("Helvetica", 8), fill="#2c3e50", angle=0)

    # ── Sorting ──────────────────────────────────────────────────────────────

    def _sort(self, col: str) -> None:
        """Sort the treeview by the clicked column (toggle asc/desc)."""
        items = [(self.tree.set(k, col), k)
                 for k in self.tree.get_children("")]
        try:
            items.sort(key=lambda t: int(t[0].replace("🥇","1").replace("🥈","2")
                                          .replace("🥉","3")))
        except ValueError:
            items.sort(key=lambda t: t[0].lower())

        for index, (_, k) in enumerate(items):
            self.tree.move(k, "", index)
