# shapes_module.py
import tkinter as tk
from tkinter import messagebox
import math
import models

class ShapesFrame(tk.Frame):
    def __init__(self, parent, current_user_callback):
        super().__init__(parent)
        self.current_user_callback = current_user_callback
        self.shapes = models.get_shapes()
        self.pack(fill="both", expand=True)
        self.create_ui()

    def create_ui(self):
        left = tk.Frame(self, width=220, bg="#dff0d8")
        left.pack(side="left", fill="y", padx=8, pady=8)

        tk.Label(left, text="Shapes", font=("Helvetica", 14, "bold"), bg="#dff0d8").pack(pady=6)

        for _, name, _, _, _ in self.shapes:
            btn = tk.Button(left, text=name, width=20, command=lambda n=name: self.show_shape(n))
            btn.pack(pady=4)

        right = tk.Frame(self, bg="#f7fbff")
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        self.info_title = tk.Label(right, text="Select a shape", font=("Helvetica", 16))
        self.info_title.pack(pady=8)

        self.description = tk.Label(right, text="", wraplength=800, justify="left")
        self.description.pack(pady=4)

        self.formula_area = tk.Label(right, text="")
        self.formula_area.pack(pady=2)
        self.formula_per = tk.Label(right, text="")
        self.formula_per.pack(pady=2)

        self.input_frame = tk.Frame(right)
        self.input_frame.pack(pady=10)

        self.input_entries = []  # dynamic entries
        self.result_label = tk.Label(right, text="", font=("Helvetica", 14), fg="darkgreen")
        self.result_label.pack(pady=10)

        self.calc_btn = tk.Button(right, text="Calculate", command=self.calculate)
        self.calc_btn.pack(pady=6)

    def show_shape(self, name):
        shape = next((s for s in self.shapes if s[1] == name), None)
        if not shape:
            return
        _, nm, desc, fa, fp = shape
        self.info_title.config(text=nm)
        self.description.config(text=desc)
        self.formula_area.config(text=f"Area: {fa}")
        self.formula_per.config(text=f"Perimeter/Other: {fp}")

        # Clear input entries
        for w in self.input_frame.winfo_children():
            w.destroy()
        self.input_entries = []

        # Determine needed inputs per shape (simple mapping)
        mapping = {
            "Circle": ["radius"],
            "Square": ["side"],
            "Rectangle": ["length", "width"],
            "Triangle": ["base", "height"],  # area only; perimeter not calculated without 3 sides
            "Ellipse": ["a (semi-major)", "b (semi-minor)"],
            "Parallelogram": ["base", "height"],
            "Trapezoid": ["base1", "base2", "height"],  # area
            "Pentagon": ["side (regular)"],
            "Hexagon": ["side (regular)"],
            "Octagon": ["side (regular)"],
            "Rhombus": ["d1 (diagonal 1)", "d2 (diagonal 2)"],
            "Cylinder": ["radius", "height"]
        }

        keys = mapping.get(nm, ["value"])
        for k in keys:
            tk.Label(self.input_frame, text=k + ":", anchor="w").pack(fill="x")
            e = tk.Entry(self.input_frame)
            e.pack(fill="x", pady=2)
            self.input_entries.append(e)

        self.result_label.config(text="")

    def calculate(self):
        name = self.info_title.cget("text")
        if name == "Select a shape":
            messagebox.showerror("Error", "Select a shape first.")
            return

        try:
            vals = [float(e.get()) for e in self.input_entries if e.get().strip() != ""]
        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values.")
            return

        # calculations
        try:
            if name == "Circle":
                r = vals[0]
                area = math.pi * r**2
                per = 2 * math.pi * r
                text = f"Area: {area:.3f}\nPerimeter: {per:.3f}"
            elif name == "Square":
                s = vals[0]
                area = s**2
                per = 4*s
                text = f"Area: {area:.3f}\nPerimeter: {per:.3f}"
            elif name == "Rectangle":
                l, w = vals
                area = l*w
                per = 2*(l+w)
                text = f"Area: {area:.3f}\nPerimeter: {per:.3f}"
            elif name == "Triangle":
                b, h = vals
                area = 0.5*b*h
                text = f"Area: {area:.3f}\n(Perimeter requires 3 side lengths)"
            elif name == "Ellipse":
                a, b = vals
                area = math.pi*a*b
                per = math.pi*(3*(a+b) - math.sqrt((3*a+b)*(a+3*b)))
                text = f"Area: {area:.3f}\nPerimeter(approx): {per:.3f}"
            elif name == "Trapezoid":
                b1, b2, h = vals
                area = 0.5*(b1 + b2)*h
                text = f"Area: {area:.3f}\n(Perimeter requires side lengths of non-parallel sides)"
            elif name == "Rhombus":
                d1, d2 = vals
                area = 0.5*d1*d2
                side = math.sqrt((d1/2)**2 + (d2/2)**2)
                per = 4*side
                text = f"Area: {area:.3f}\nPerimeter: {per:.3f}"
            elif name == "Cylinder":
                r, h = vals
                sa = 2*math.pi*r*(r+h)
                vol = math.pi*r**2*h
                text = f"Surface Area: {sa:.3f}\nVolume: {vol:.3f}"
            else:
                text = "Calculation not implemented for this shape."
        except Exception as e:
            text = "Error in calculation: " + str(e)

        # update UI and reward points
        self.result_label.config(text=text)
        user = self.current_user_callback()
        if user:
            models.update_user_progress(user[1], points=1, completed_quiz_inc=0)  # give tiny point for calculation
