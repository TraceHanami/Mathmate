# shapes_module.py
# ─────────────────────────────────────────────────────────────────────────────
# SHAPES TAB
# Displays each shape's formulas, accepts numeric inputs and computes area /
# perimeter / volume.  Now includes 15 shapes (was 6) and shows an extra-notes
# panel with tips and additional formulas.
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import messagebox
import math
import models


# Map every shape name to the labels that the user must fill in
_INPUT_MAP: dict[str, list[str]] = {
    "Circle":        ["Radius (r)"],
    "Square":        ["Side (a)"],
    "Rectangle":     ["Length (l)", "Width (w)"],
    "Triangle":      ["Base (b)", "Height (h)"],
    "Ellipse":       ["Semi-major axis (a)", "Semi-minor axis (b)"],
    "Cylinder":      ["Radius (r)", "Height (h)"],
    "Pentagon":      ["Side (s)"],
    "Hexagon":       ["Side (s)"],
    "Octagon":       ["Side (s)"],
    "Trapezoid":     ["Base 1 (b₁)", "Base 2 (b₂)", "Height (h)"],
    "Rhombus":       ["Diagonal 1 (d₁)", "Diagonal 2 (d₂)"],
    "Parallelogram": ["Base (b)", "Height (h)"],
    "Cone":          ["Radius (r)", "Height (h)"],
    "Sphere":        ["Radius (r)"],
    "Cuboid":        ["Length (l)", "Width (w)", "Height (h)"],
}


def _calculate(name: str, vals: list[float]) -> str:
    """
    Pure-function calculator.  Returns a result string or raises ValueError.
    Kept separate from the UI so it can be unit-tested independently.
    """
    if name == "Circle":
        r = vals[0]
        return f"Area: {math.pi*r**2:.4f}\nCircumference: {2*math.pi*r:.4f}"

    if name == "Square":
        a = vals[0]
        return f"Area: {a**2:.4f}\nPerimeter: {4*a:.4f}\nDiagonal: {a*math.sqrt(2):.4f}"

    if name == "Rectangle":
        l, w = vals
        return (f"Area: {l*w:.4f}\nPerimeter: {2*(l+w):.4f}\n"
                f"Diagonal: {math.sqrt(l**2+w**2):.4f}")

    if name == "Triangle":
        b, h = vals
        return (f"Area: {0.5*b*h:.4f}\n"
                f"(Perimeter requires all 3 side lengths)")

    if name == "Ellipse":
        a, b = vals
        area = math.pi * a * b
        per  = math.pi * (3*(a+b) - math.sqrt((3*a+b)*(a+3*b)))
        return f"Area: {area:.4f}\nPerimeter (approx): {per:.4f}"

    if name == "Cylinder":
        r, h = vals
        sa  = 2 * math.pi * r * (r + h)
        vol = math.pi * r**2 * h
        return f"Surface Area: {sa:.4f}\nVolume: {vol:.4f}"

    if name == "Pentagon":
        s = vals[0]
        area = (s**2 / 4) * math.sqrt(25 + 10*math.sqrt(5))
        return f"Area: {area:.4f}\nPerimeter: {5*s:.4f}"

    if name == "Hexagon":
        s = vals[0]
        area = (3 * math.sqrt(3) / 2) * s**2
        return f"Area: {area:.4f}\nPerimeter: {6*s:.4f}"

    if name == "Octagon":
        s = vals[0]
        area = 2 * (1 + math.sqrt(2)) * s**2
        return f"Area: {area:.4f}\nPerimeter: {8*s:.4f}"

    if name == "Trapezoid":
        b1, b2, h = vals
        area = 0.5 * (b1 + b2) * h
        return f"Area: {area:.4f}\n(Perimeter needs non-parallel side lengths)"

    if name == "Rhombus":
        d1, d2 = vals
        area = 0.5 * d1 * d2
        side = math.sqrt((d1/2)**2 + (d2/2)**2)
        return f"Area: {area:.4f}\nPerimeter: {4*side:.4f}"

    if name == "Parallelogram":
        b, h = vals
        return f"Area: {b*h:.4f}"

    if name == "Cone":
        r, h = vals
        l   = math.sqrt(r**2 + h**2)      # slant height
        sa  = math.pi * r * (r + l)
        vol = (1/3) * math.pi * r**2 * h
        return f"Slant height: {l:.4f}\nSurface Area: {sa:.4f}\nVolume: {vol:.4f}"

    if name == "Sphere":
        r = vals[0]
        return (f"Surface Area: {4*math.pi*r**2:.4f}\n"
                f"Volume: {(4/3)*math.pi*r**3:.4f}")

    if name == "Cuboid":
        l, w, h = vals
        sa  = 2*(l*w + l*h + w*h)
        vol = l * w * h
        diag = math.sqrt(l**2 + w**2 + h**2)
        return f"Surface Area: {sa:.4f}\nVolume: {vol:.4f}\nDiagonal: {diag:.4f}"

    return "Calculation not implemented for this shape."


class ShapesFrame(tk.Frame):
    """Left panel = shape buttons.  Right panel = info + dynamic inputs + result."""

    def __init__(self, parent, current_user_callback):
        super().__init__(parent)
        self.current_user_callback = current_user_callback
        # models.get_shapes() now returns 6-tuples (id,name,desc,fa,fp,notes)
        self.shapes = models.get_shapes()
        self.pack(fill="both", expand=True)
        self._build_ui()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # ── Left sidebar ──────────────────────────────────────────────────────
        left = tk.Frame(self, width=200, bg="#dff0d8")
        left.pack(side="left", fill="y", padx=6, pady=6)
        left.pack_propagate(False)

        tk.Label(left, text="Shapes", font=("Helvetica", 14, "bold"),
                 bg="#dff0d8").pack(pady=6)

        canvas = tk.Canvas(left, bg="#dff0d8", highlightthickness=0)
        scrollbar = tk.Scrollbar(left, orient="vertical", command=canvas.yview)
        btn_frame = tk.Frame(canvas, bg="#dff0d8")
        btn_frame.bind("<Configure>",
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=btn_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        for _, name, *_ in self.shapes:
            tk.Button(btn_frame, text=name, width=22,
                      command=lambda n=name: self._show_shape(n)).pack(pady=3, padx=4)

        # ── Right panel ───────────────────────────────────────────────────────
        right = tk.Frame(self, bg="#f7fbff")
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        self.lbl_title   = tk.Label(right, text="Select a shape",
                                    font=("Helvetica", 16, "bold"), bg="#f7fbff")
        self.lbl_title.pack(pady=(10, 2))

        self.lbl_desc    = tk.Label(right, text="", wraplength=720,
                                    justify="left", bg="#f7fbff")
        self.lbl_desc.pack(pady=2)

        self.lbl_area    = tk.Label(right, text="", fg="#1a5276",
                                    font=("Helvetica", 10, "bold"), bg="#f7fbff")
        self.lbl_area.pack()

        self.lbl_per     = tk.Label(right, text="", fg="#1a5276",
                                    font=("Helvetica", 10, "bold"), bg="#f7fbff")
        self.lbl_per.pack()

        # NEW: extra notes displayed in a coloured box
        self.lbl_notes   = tk.Label(right, text="", wraplength=720,
                                    justify="left", bg="#fffde7",
                                    relief="groove", padx=8, pady=4)
        self.lbl_notes.pack(fill="x", padx=20, pady=(6, 0))

        tk.Label(right, text="", bg="#f7fbff").pack()  # spacer

        self.input_frame = tk.Frame(right, bg="#f7fbff")
        self.input_frame.pack()
        self.input_entries: list[tk.Entry] = []

        self.btn_calc = tk.Button(right, text="Calculate",
                                  command=self._calculate, width=16,
                                  bg="#2ecc71", fg="white",
                                  font=("Helvetica", 11, "bold"))
        self.btn_calc.pack(pady=8)

        self.lbl_result = tk.Label(right, text="", font=("Helvetica", 13),
                                   fg="#145a32", bg="#f7fbff",
                                   justify="center")
        self.lbl_result.pack(pady=6)

    # ── Event handlers ────────────────────────────────────────────────────────

    def _show_shape(self, name: str) -> None:
        # find the matching row (id,name,desc,fa,fp,notes)
        row = next((s for s in self.shapes if s[1] == name), None)
        if not row:
            return
        _, nm, desc, fa, fp, notes = row

        self.lbl_title.config(text=nm)
        self.lbl_desc.config(text=desc)
        self.lbl_area.config(text=f"Area / Surface Area:  {fa}")
        self.lbl_per.config(text=f"Perimeter / Volume:   {fp}")
        self.lbl_notes.config(text=f"💡 {notes}" if notes else "")

        # Rebuild dynamic input fields
        for w in self.input_frame.winfo_children():
            w.destroy()
        self.input_entries = []

        for label_text in _INPUT_MAP.get(nm, ["Value"]):
            row_f = tk.Frame(self.input_frame, bg="#f7fbff")
            row_f.pack(fill="x", padx=40, pady=2)
            tk.Label(row_f, text=label_text + ":", width=22,
                     anchor="w", bg="#f7fbff").pack(side="left")
            entry = tk.Entry(row_f, width=14)
            entry.pack(side="left")
            self.input_entries.append(entry)

        self.lbl_result.config(text="")

    def _calculate(self) -> None:
        name = self.lbl_title.cget("text")
        if name == "Select a shape":
            messagebox.showerror("Error", "Please select a shape first.")
            return

        try:
            vals = [float(e.get()) for e in self.input_entries if e.get().strip()]
        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values only.")
            return

        expected = len(_INPUT_MAP.get(name, ["Value"]))
        if len(vals) != expected:
            messagebox.showerror("Error",
                                 f"{name} needs {expected} value(s). Got {len(vals)}.")
            return

        try:
            result = _calculate(name, vals)
        except Exception as exc:
            messagebox.showerror("Calculation Error", str(exc))
            return

        self.lbl_result.config(text=result)

        # Award a small point for performing a calculation
        user = self.current_user_callback()
        if user:
            models.update_user_progress(user[1], points=1)
