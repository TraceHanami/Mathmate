# trig_module.py
# ─────────────────────────────────────────────────────────────────────────────
# TRIGONOMETRY TAB
# Now covers 10 trig topics (was 4): sin, cos, tan, cot, sec, csc, Pythagorean
# Theorem, Law of Sines, Law of Cosines and Inverse Trig.
# Displays extra notes for each function.
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import messagebox
import math
import models


class TrigFrame(tk.Frame):
    """Left panel = function buttons.  Right panel = info + calculator."""

    def __init__(self, parent, current_user_callback):
        super().__init__(parent)
        self.current_user_callback = current_user_callback
        # models.get_trig_functions() → (id, name, description, formula, notes)
        self.funcs = models.get_trig_functions()
        self.pack(fill="both", expand=True)
        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # Left sidebar
        left = tk.Frame(self, width=210, bg="#cfe9ff")
        left.pack(side="left", fill="y", padx=6, pady=6)
        left.pack_propagate(False)

        tk.Label(left, text="Trigonometry",
                 font=("Helvetica", 14, "bold"), bg="#cfe9ff").pack(pady=6)

        canvas    = tk.Canvas(left, bg="#cfe9ff", highlightthickness=0)
        scrollbar = tk.Scrollbar(left, orient="vertical", command=canvas.yview)
        btn_frame = tk.Frame(canvas, bg="#cfe9ff")
        btn_frame.bind("<Configure>",
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=btn_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        for _, name, *_ in self.funcs:
            tk.Button(btn_frame, text=name, width=24,
                      command=lambda n=name: self._show_func(n)).pack(pady=3, padx=4)

        # Right panel
        right = tk.Frame(self, bg="#e8f7ff")
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        self.lbl_title   = tk.Label(right, text="Select a function",
                                    font=("Helvetica", 15, "bold"), bg="#e8f7ff")
        self.lbl_title.pack(pady=(10, 2))

        self.lbl_desc    = tk.Label(right, text="", wraplength=720,
                                    justify="left", bg="#e8f7ff")
        self.lbl_desc.pack(pady=4)

        self.lbl_formula = tk.Label(right, text="", fg="#1a5276",
                                    font=("Helvetica", 10, "bold"),
                                    wraplength=720, bg="#e8f7ff")
        self.lbl_formula.pack(pady=2)

        # NEW: extra notes
        self.lbl_notes   = tk.Label(right, text="", wraplength=720,
                                    justify="left", bg="#fffde7",
                                    relief="groove", padx=8, pady=4)
        self.lbl_notes.pack(fill="x", padx=20, pady=(4, 8))

        # Hint for what to enter
        self.lbl_input_hint = tk.Label(right,
                                       text="Enter angle in degrees (or values for special topics):",
                                       bg="#e8f7ff")
        self.lbl_input_hint.pack(pady=4)

        self.entry = tk.Entry(right, width=36)
        self.entry.pack(pady=2)

        tk.Button(right, text="Calculate", command=self._calculate,
                  bg="#2980b9", fg="white",
                  font=("Helvetica", 11, "bold"), width=16).pack(pady=6)

        self.lbl_result = tk.Label(right, text="", fg="#145a32",
                                   font=("Helvetica", 12),
                                   wraplength=720, bg="#e8f7ff",
                                   justify="center")
        self.lbl_result.pack(pady=8)

    # ── Event handlers ────────────────────────────────────────────────────────

    def _show_func(self, name: str) -> None:
        row = next((f for f in self.funcs if f[1] == name), None)
        if not row:
            return
        _, nm, desc, formula, notes = row
        self.lbl_title.config(text=nm)
        self.lbl_desc.config(text=desc)
        self.lbl_formula.config(text=f"Formula:  {formula}")
        self.lbl_notes.config(text=f"💡 {notes}" if notes else "")
        self.entry.delete(0, "end")
        self.lbl_result.config(text="")

        # Update input hint based on function type
        special = {
            "Pythagorean Theorem": "Enter a, b  (legs of the right triangle)",
            "Law of Sines":
                "Enter A (°), a, b  →  finds angle B (AAS/ASA)",
            "Law of Cosines":
                "Enter a, b, C (°)  →  finds side c",
            "Inverse Trig (arcsin/arccos/arctan)":
                "Enter ratio value (e.g. 0.5 for arcsin)",
        }
        self.lbl_input_hint.config(
            text=special.get(nm, "Enter angle in degrees:"))

    def _calculate(self) -> None:
        name = self.lbl_title.cget("text")
        if name == "Select a function":
            messagebox.showerror("Error", "Please select a function first.")
            return

        raw = self.entry.get().strip()
        if not raw:
            messagebox.showerror("Error", "Please provide input.")
            return

        result_text = ""
        try:
            parts = [float(p.strip()) for p in raw.split(",") if p.strip()]

            if name == "Pythagorean Theorem":
                if len(parts) < 2:
                    raise ValueError("Enter a and b (legs)")
                a, b = parts[:2]
                c = math.sqrt(a**2 + b**2)
                result_text = (f"a = {a}, b = {b}\n"
                               f"Hypotenuse c = √({a}²+{b}²) = {c:.6f}")

            elif name == "Law of Sines":
                # A (degrees), a, b → B
                if len(parts) < 3:
                    raise ValueError("Enter A (°), side a, side b")
                A_deg, a, b = parts[:3]
                sin_B = b * math.sin(math.radians(A_deg)) / a
                if abs(sin_B) > 1:
                    raise ValueError("No valid triangle with these values.")
                B_deg = math.degrees(math.asin(sin_B))
                C_deg = 180 - A_deg - B_deg
                result_text = (f"A={A_deg}°, a={a}, b={b}\n"
                               f"B = {B_deg:.4f}°\n"
                               f"C = {C_deg:.4f}°")

            elif name == "Law of Cosines":
                # a, b, C (degrees) → c
                if len(parts) < 3:
                    raise ValueError("Enter a, b, C (angle in °)")
                a, b, C_deg = parts[:3]
                c2 = a**2 + b**2 - 2*a*b*math.cos(math.radians(C_deg))
                if c2 < 0:
                    raise ValueError("No real solution — check inputs.")
                c = math.sqrt(c2)
                result_text = (f"a={a}, b={b}, C={C_deg}°\n"
                               f"c² = {c2:.6f}\n"
                               f"c = {c:.6f}")

            elif "Inverse" in name or "arc" in name.lower():
                val = parts[0]
                if abs(val) > 1:
                    result_text = (f"arctan({val}) = "
                                   f"{math.degrees(math.atan(val)):.6f}°\n"
                                   f"(arcsin/arccos undefined for |x|>1)")
                else:
                    result_text = (
                        f"arcsin({val}) = {math.degrees(math.asin(val)):.6f}°\n"
                        f"arccos({val}) = {math.degrees(math.acos(val)):.6f}°\n"
                        f"arctan({val}) = {math.degrees(math.atan(val)):.6f}°"
                    )

            else:
                # Standard angle-based functions
                angle_deg = parts[0]
                rad = math.radians(angle_deg)
                nm  = name  # local alias

                if "Sine" in nm or "(sin)" in nm:
                    result_text = f"sin({angle_deg}°) = {math.sin(rad):.6f}"
                elif "Cosine" in nm or "(cos)" in nm:
                    result_text = f"cos({angle_deg}°) = {math.cos(rad):.6f}"
                elif "Tangent" in nm and "Co" not in nm:
                    if abs(math.cos(rad)) < 1e-10:
                        result_text = "tan is undefined at this angle."
                    else:
                        result_text = f"tan({angle_deg}°) = {math.tan(rad):.6f}"
                elif "Cotangent" in nm or "(cot)" in nm:
                    if abs(math.sin(rad)) < 1e-10:
                        result_text = "cot is undefined at this angle."
                    else:
                        result_text = f"cot({angle_deg}°) = {1/math.tan(rad):.6f}"
                elif "Secant" in nm or "(sec)" in nm:
                    if abs(math.cos(rad)) < 1e-10:
                        result_text = "sec is undefined at this angle."
                    else:
                        result_text = f"sec({angle_deg}°) = {1/math.cos(rad):.6f}"
                elif "Cosecant" in nm or "(csc)" in nm:
                    if abs(math.sin(rad)) < 1e-10:
                        result_text = "csc is undefined at this angle."
                    else:
                        result_text = f"csc({angle_deg}°) = {1/math.sin(rad):.6f}"
                else:
                    result_text = "Calculation not available for this function."

        except Exception as exc:
            messagebox.showerror("Calculation Error", str(exc))
            return

        self.lbl_result.config(text=result_text)

        # Small point reward
        user = self.current_user_callback()
        if user:
            models.update_user_progress(user[1], points=2)
