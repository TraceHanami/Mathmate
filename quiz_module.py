# quiz_module.py
# ─────────────────────────────────────────────────────────────────────────────
# QUIZ / CHALLENGE MODE
# • User selects topic (shapes / algebra / trig)
# • 10 randomised multiple-choice questions drawn from the DB
# • Live score ticker, colour-coded feedback, explanation after each answer
# • Points awarded on completion; history shown below the quiz
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import messagebox
import models


# ─────────────────────────────────────────────────────────────────────────────
class QuizFrame(tk.Frame):

    _OPTION_LABELS = ("A", "B", "C", "D")
    _TOPIC_COLOURS = {
        "shapes":  "#dff0d8",
        "algebra": "#ffe0b2",
        "trig":    "#cfe9ff",
    }

    def __init__(self, parent, current_user_callback):
        super().__init__(parent, bg="#fafafa")
        self.current_user_callback = current_user_callback
        self.pack(fill="both", expand=True)

        self._questions: list   = []
        self._q_index:   int    = 0
        self._score:     int    = 0
        self._answered:  bool   = False
        self._topic:     str    = "shapes"

        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # ── Top toolbar ───────────────────────────────────────────────────────
        toolbar = tk.Frame(self, bg="#34495e", pady=6)
        toolbar.pack(fill="x")

        tk.Label(toolbar, text="Quiz Mode", font=("Helvetica", 15, "bold"),
                 bg="#34495e", fg="white").pack(side="left", padx=12)

        tk.Label(toolbar, text="Topic:", bg="#34495e",
                 fg="white").pack(side="left", padx=(20, 4))
        self._topic_var = tk.StringVar(value="shapes")
        for t in ("shapes", "algebra", "trig"):
            tk.Radiobutton(toolbar, text=t.capitalize(), variable=self._topic_var,
                           value=t, bg="#34495e", fg="white",
                           selectcolor="#2c3e50",
                           activebackground="#34495e",
                           command=lambda: None).pack(side="left", padx=4)

        tk.Button(toolbar, text="▶  Start Quiz",
                  command=self._start_quiz,
                  bg="#27ae60", fg="white",
                  font=("Helvetica", 11, "bold"),
                  padx=10).pack(side="right", padx=12)

        # ── Progress bar area ─────────────────────────────────────────────────
        prog_bar = tk.Frame(self, bg="#ecf0f1", height=30)
        prog_bar.pack(fill="x")
        prog_bar.pack_propagate(False)

        self.lbl_progress = tk.Label(prog_bar,
                                     text="Start a quiz to begin!",
                                     bg="#ecf0f1", font=("Helvetica", 10))
        self.lbl_progress.pack(side="left", padx=12)

        self.lbl_score_ticker = tk.Label(prog_bar, text="Score: 0 / 0",
                                         bg="#ecf0f1",
                                         font=("Helvetica", 10, "bold"),
                                         fg="#2c3e50")
        self.lbl_score_ticker.pack(side="right", padx=12)

        # ── Question card ─────────────────────────────────────────────────────
        self.card = tk.Frame(self, bg="#ffffff", padx=20, pady=20,
                             relief="ridge", bd=2)
        self.card.pack(fill="both", expand=True, padx=20, pady=12)

        # Difficulty badge
        self.lbl_diff = tk.Label(self.card, text="", font=("Helvetica", 9),
                                 bg="#bdc3c7", fg="white", padx=6, pady=2)
        self.lbl_diff.pack(anchor="ne")

        self.lbl_question = tk.Label(self.card, text="",
                                     font=("Helvetica", 13, "bold"),
                                     wraplength=800, justify="left",
                                     bg="#ffffff")
        self.lbl_question.pack(pady=(10, 16))

        # Option buttons stored in a list so we can recolour them
        self._option_btns: list[tk.Button] = []
        self._selected_var = tk.StringVar(value="")
        options_frame = tk.Frame(self.card, bg="#ffffff")
        options_frame.pack(fill="x")

        for key in ("a", "b", "c", "d"):
            btn = tk.Button(options_frame,
                            text="", anchor="w",
                            font=("Helvetica", 11), wraplength=760,
                            justify="left", padx=12, pady=6,
                            relief="groove", cursor="hand2",
                            command=lambda k=key: self._select_answer(k))
            btn.pack(fill="x", pady=3)
            self._option_btns.append(btn)

        # Submit / Next button
        self.btn_action = tk.Button(self.card,
                                    text="Submit",
                                    font=("Helvetica", 11, "bold"),
                                    width=14, bg="#2980b9", fg="white",
                                    command=self._action)
        self.btn_action.pack(pady=(12, 4))

        # Explanation box
        self.lbl_explanation = tk.Label(self.card, text="",
                                        wraplength=800, justify="left",
                                        bg="#eafaf1", relief="groove",
                                        padx=10, pady=6,
                                        font=("Helvetica", 10))
        self.lbl_explanation.pack(fill="x", pady=4)

        # ── History panel ─────────────────────────────────────────────────────
        hist_outer = tk.Frame(self, bg="#fafafa")
        hist_outer.pack(fill="x", padx=20, pady=(0, 12))

        tk.Label(hist_outer, text="Your Recent Quiz History",
                 font=("Helvetica", 11, "bold"),
                 bg="#fafafa").pack(anchor="w")

        self.history_text = tk.Text(hist_outer, height=5, state="disabled",
                                    font=("Courier", 9), bg="#f2f2f2",
                                    relief="sunken")
        self.history_text.pack(fill="x")

    # ── Quiz flow ─────────────────────────────────────────────────────────────

    def _start_quiz(self) -> None:
        user = self.current_user_callback()
        if not user:
            messagebox.showwarning("No User", "Please select a user first.")
            return

        self._topic = self._topic_var.get()
        self._questions = models.get_quiz_questions(self._topic, limit=10)

        if not self._questions:
            messagebox.showinfo("No Questions",
                                f"No questions found for topic '{self._topic}'.")
            return

        self._q_index  = 0
        self._score    = 0
        self._answered = False
        self.card.config(bg="#ffffff")
        self._show_question()
        self._refresh_history(user[1])

    def _show_question(self) -> None:
        if self._q_index >= len(self._questions):
            self._finish_quiz()
            return

        row = self._questions[self._q_index]
        # row: id, topic, question_text, opt_a, opt_b, opt_c, opt_d,
        #       correct, difficulty, explanation
        _, _topic, q_text, a, b, c, d, _correct, diff, _expl = row

        diff_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
        diff_colours = {1: "#27ae60", 2: "#e67e22", 3: "#c0392b"}
        self.lbl_diff.config(
            text=f"  {diff_labels.get(diff, '')}  ",
            bg=diff_colours.get(diff, "#bdc3c7")
        )

        self.lbl_question.config(
            text=f"Q{self._q_index + 1} of {len(self._questions)}:  {q_text}")

        for i, (btn, text) in enumerate(zip(self._option_btns, (a, b, c, d))):
            btn.config(text=f"  {self._OPTION_LABELS[i]}.  {text}",
                       bg="#f0f0f0", fg="#2c3e50", state="normal",
                       relief="groove")

        self.lbl_explanation.config(text="")
        self._selected_var.set("")
        self._answered = False
        self.btn_action.config(text="Submit", bg="#2980b9", state="normal")

        total = len(self._questions)
        self.lbl_progress.config(
            text=f"Question {self._q_index + 1} of {total}")
        self.lbl_score_ticker.config(
            text=f"Score: {self._score} / {self._q_index}")

    def _select_answer(self, key: str) -> None:
        if self._answered:
            return
        self._selected_var.set(key)
        key_map = {"a": 0, "b": 1, "c": 2, "d": 3}
        # Reset all to grey then highlight selected
        for btn in self._option_btns:
            btn.config(bg="#f0f0f0")
        self._option_btns[key_map[key]].config(bg="#d6eaf8")

    def _action(self) -> None:
        if not self._answered:
            self._submit()
        else:
            self._next()

    def _submit(self) -> None:
        selected = self._selected_var.get()
        if not selected:
            messagebox.showwarning("No Answer", "Please choose an option.")
            return

        row      = self._questions[self._q_index]
        correct  = row[7]      # 'a' | 'b' | 'c' | 'd'
        expl     = row[9] or ""
        key_map  = {"a": 0, "b": 1, "c": 2, "d": 3}

        self._answered = True

        # Colour all buttons: green for correct, red for wrong selection
        for i, btn in enumerate(self._option_btns):
            opt_key = ["a", "b", "c", "d"][i]
            if opt_key == correct:
                btn.config(bg="#a9dfbf", fg="#145a32")   # green
            elif opt_key == selected:
                btn.config(bg="#f1948a", fg="#78281f")   # red
            btn.config(state="disabled")

        if selected == correct:
            self._score += 1
            feedback = "✅  Correct!"
            self.lbl_explanation.config(
                text=f"{feedback}  {expl}", bg="#eafaf1")
        else:
            feedback = f"❌  Wrong — correct answer: {correct.upper()}"
            self.lbl_explanation.config(
                text=f"{feedback}  {expl}", bg="#fdedec")

        self.lbl_score_ticker.config(
            text=f"Score: {self._score} / {self._q_index + 1}")
        self.btn_action.config(text="Next →", bg="#27ae60")

    def _next(self) -> None:
        self._q_index += 1
        self._show_question()

    def _finish_quiz(self) -> None:
        user  = self.current_user_callback()
        total = len(self._questions)
        pct   = round(self._score / total * 100)

        if user:
            models.save_quiz_attempt(user[1], self._topic,
                                     self._score, total)

        # Reset card to summary view
        self.lbl_question.config(
            text=f"Quiz Complete!\n\n"
                 f"You scored {self._score} / {total}  ({pct}%)\n\n" +
                 ("🏆 Perfect score! +20 bonus points!" if self._score == total else
                  f"Points earned: {self._score * 5}"))

        for btn in self._option_btns:
            btn.config(text="", state="disabled", bg="#f0f0f0")

        self.lbl_explanation.config(text="", bg="#ffffff")
        self.btn_action.config(text="▶  Play Again",
                               bg="#8e44ad", state="normal")
        self._answered = False   # so next click goes to _start_quiz

        self.lbl_progress.config(text="Quiz finished")
        self.lbl_score_ticker.config(text=f"Final: {self._score}/{total}")

        if user:
            self._refresh_history(user[1])

        # Override action to restart
        self.btn_action.config(command=self._start_quiz)

    # ── History ───────────────────────────────────────────────────────────────

    def _refresh_history(self, username: str) -> None:
        rows = models.get_user_quiz_history(username)
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")

        if not rows:
            self.history_text.insert("end", "  No quiz history yet.\n")
        else:
            header = f"{'Topic':<12}{'Score':<10}{'%':<8}{'Date'}\n"
            self.history_text.insert("end", header)
            self.history_text.insert("end", "─" * 50 + "\n")
            for topic, score, total, ts in rows:
                pct = round(score / total * 100) if total else 0
                line = f"{topic:<12}{score}/{total:<7}{pct}%    {ts[:16]}\n"
                self.history_text.insert("end", line)

        self.history_text.config(state="disabled")
