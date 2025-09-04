# algebra_module.py
import tkinter as tk
from tkinter import messagebox
from sympy import symbols, Eq, solve
import models

class AlgebraFrame(tk.Frame):
    def __init__(self, parent, current_user_callback):
        super().__init__(parent)
        self.current_user_callback = current_user_callback
        self.concepts = models.get_algebra_concepts()
        self.pack(fill="both", expand=True)
        self.create_ui()

    def create_ui(self):
        left = tk.Frame(self, width=260, bg="#ffe0b2")
        left.pack(side="left", fill="y", padx=8, pady=8)
        tk.Label(left, text="Algebra", font=("Helvetica", 14, "bold"), bg="#ffe0b2").pack(pady=6)

        for _, name, _, _, _ in self.concepts:
            tk.Button(left, text=name, width=24, command=lambda n=name: self.show_concept(n)).pack(pady=4)

        right = tk.Frame(self, bg="#fff8e1")
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        self.title = tk.Label(right, text="Select an Algebra Concept", font=("Helvetica", 16))
        self.title.pack(pady=8)

        self.desc = tk.Label(right, text="", wraplength=700, justify="left")
        self.desc.pack(pady=4)
        self.formula = tk.Label(right, text="", fg="blue")
        self.formula.pack(pady=4)
        self.example = tk.Label(right, text="", fg="purple")
        self.example.pack(pady=4)

        self.input_label = tk.Label(right, text="Input (comma-separated if multiple):")
        self.input_label.pack(pady=6)
        self.entry = tk.Entry(right, width=40)
        self.entry.pack(pady=2)
        self.calc_btn = tk.Button(right, text="Calculate", command=self.calculate)
        self.calc_btn.pack(pady=6)
        self.result = tk.Label(right, text="", fg="darkgreen", font=("Helvetica", 12))
        self.result.pack(pady=10)

    def show_concept(self, name):
        c = next((x for x in self.concepts if x[1] == name), None)
        if not c: return
        _, nm, desc, formula, example = c
        self.title.config(text=nm)
        self.desc.config(text=desc)
        self.formula.config(text=f"Formula: {formula}")
        self.example.config(text=f"Example: {example}")
        self.entry.delete(0, "end")
        self.result.config(text="")

    def calculate(self):
        name = self.title.cget("text")
        if name == "Select an Algebra Concept":
            messagebox.showerror("Error", "Select a concept first.")
            return
        raw = self.entry.get().strip()
        if not raw:
            messagebox.showerror("Error", "Provide input.")
            return

        try:
            nums = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]
        except ValueError:
            messagebox.showerror("Error", "Enter numeric values separated by commas.")
            return

        x = symbols('x')
        try:
            if name == "Linear Equation":
                if len(nums) != 2:
                    raise ValueError("Provide a,b for ax + b = 0")
                a, b = nums
                sol = solve(Eq(a*x + b, 0), x)
                self.result.config(text=f"x = {sol[0] if sol else 'No solution'}")
            elif name == "Quadratic Equation":
                if len(nums) != 3:
                    raise ValueError("Provide a,b,c for ax^2 + bx + c = 0")
                a, b, c = nums
                sol = solve(Eq(a*x**2 + b*x + c, 0), x)
                if len(sol) > 1:
                    self.result.config(text=f"x1={sol[0]}, x2={sol[1]}")
                else:
                    self.result.config(text=f"x = {sol}")
            elif name == "Laws of Exponents":
                if len(nums) < 3:
                    raise ValueError("Provide base, e1, e2")
                base, e1, e2 = nums[:3]
                self.result.config(text=f"{base}^{e1} * {base}^{e2} = {base**e1 * base**e2}")
            elif name == "Factorization":
                if len(nums) >= 2:
                    a, b = nums[:2]
                    self.result.config(text=f"{a}^2 + 2*{a}*{b} + {b}^2 = {a**2 + 2*a*b + b**2}")
                else:
                    self.result.config(text="Provide a and b")
            else:
                self.result.config(text="Not implemented")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # reward small points to user
        user = self.current_user_callback()
        if user:
            models.update_user_progress(user[1], points=2, completed_quiz_inc=0)
