# trig_module.py
import tkinter as tk
from tkinter import messagebox
import math
import models

class TrigFrame(tk.Frame):
    def __init__(self, parent, current_user_callback):
        super().__init__(parent)
        self.current_user_callback = current_user_callback
        self.funcs = models.get_trig_functions()
        self.pack(fill="both", expand=True)
        self.create_ui()

    def create_ui(self):
        left = tk.Frame(self, width=220, bg="#cfe9ff")
        left.pack(side="left", fill="y", padx=8, pady=8)
        tk.Label(left, text="Trigonometry", font=("Helvetica", 14, "bold"), bg="#cfe9ff").pack(pady=6)
        for _, name, _, _ in self.funcs:
            tk.Button(left, text=name, width=24, command=lambda n=name: self.show_func(n)).pack(pady=4)

        right = tk.Frame(self, bg="#e8f7ff")
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        self.title = tk.Label(right, text="Select a function", font=("Helvetica", 16))
        self.title.pack(pady=8)
        self.desc = tk.Label(right, text="", wraplength=700, justify="left")
        self.desc.pack(pady=4)
        self.formula = tk.Label(right, text="", fg="blue")
        self.formula.pack(pady=4)

        self.input_label = tk.Label(right, text="Enter angle (degrees) or a,b for Pythagoras:")
        self.input_label.pack(pady=6)
        self.entry = tk.Entry(right, width=30)
        self.entry.pack(pady=2)
        self.calc_btn = tk.Button(right, text="Calculate", command=self.calculate)
        self.calc_btn.pack(pady=6)
        self.result = tk.Label(right, text="", fg="darkgreen", font=("Helvetica", 12))
        self.result.pack(pady=10)

    def show_func(self, name):
        f = next((x for x in self.funcs if x[1] == name), None)
        if not f: return
        _, nm, desc, formula = f
        self.title.config(text=nm)
        self.desc.config(text=desc)
        self.formula.config(text=f"Formula: {formula}")
        self.entry.delete(0, "end")
        self.result.config(text="")

    def calculate(self):
        name = self.title.cget("text")
        raw = self.entry.get().strip()
        if not raw:
            messagebox.showerror("Error", "Provide input.")
            return

        try:
            if "Pythagorean" in name:
                parts = [float(p.strip()) for p in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Provide a and b")
                a, b = parts
                c = math.sqrt(a*a + b*b)
                self.result.config(text=f"Hypotenuse c = {c:.4f}")
            else:
                angle_deg = float(raw)
                rad = math.radians(angle_deg)
                if "Sine" in name or "sin" in name:
                    res = math.sin(rad)
                elif "Cosine" in name or "cos" in name:
                    res = math.cos(rad)
                elif "Tangent" in name or "tan" in name:
                    res = math.tan(rad)
                elif "Cotangent" in name or "cot" in name:
                    res = 1 / math.tan(rad)
                elif "Secant" in name or "sec" in name:
                    res = 1 / math.cos(rad)
                elif "Cosecant" in name or "csc" in name:
                    res = 1 / math.sin(rad)
                else:
                    res = None
                if res is None:
                    self.result.config(text="Calculation not available")
                else:
                    self.result.config(text=f"Result = {res:.6f}")
        except Exception as e:
            messagebox.showerror("Calculation error", str(e))
            return

        # reward user with points
        user = self.current_user_callback()
        if user:
            models.update_user_progress(user[1], points=2, completed_quiz_inc=0)
