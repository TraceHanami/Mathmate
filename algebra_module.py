# algebra_module.py
# ─────────────────────────────────────────────────────────────────────────────
# ALGEBRA TAB
# Shows 10 algebra concepts (was 4) with descriptions, formulas, worked
# examples and extra notes.  The calculate panel handles each concept.
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import messagebox
from sympy import symbols, Eq, solve, factor, expand, log, sqrt, Rational
import models


class AlgebraFrame(tk.Frame):
    """Left panel = concept buttons.  Right panel = info + calculator."""

    def __init__(self, parent, current_user_callback):
        super().__init__(parent)
        self.current_user_callback = current_user_callback
        # models.get_algebra_concepts() → (id,name,desc,formula,example,notes)
        self.concepts = models.get_algebra_concepts()
        self.pack(fill="both", expand=True)
        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # Left sidebar
        left = tk.Frame(self, width=210, bg="#ffe0b2")
        left.pack(side="left", fill="y", padx=6, pady=6)
        left.pack_propagate(False)

        tk.Label(left, text="Algebra", font=("Helvetica", 14, "bold"),
                 bg="#ffe0b2").pack(pady=6)

        canvas   = tk.Canvas(left, bg="#ffe0b2", highlightthickness=0)
        scrollbar = tk.Scrollbar(left, orient="vertical", command=canvas.yview)
        btn_frame = tk.Frame(canvas, bg="#ffe0b2")
        btn_frame.bind("<Configure>",
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=btn_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        for _, name, *_ in self.concepts:
            tk.Button(btn_frame, text=name, width=24,
                      command=lambda n=name: self._show_concept(n)).pack(pady=3, padx=4)

        # Right panel
        right = tk.Frame(self, bg="#fff8e1")
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        self.lbl_title   = tk.Label(right, text="Select an Algebra Concept",
                                    font=("Helvetica", 15, "bold"), bg="#fff8e1")
        self.lbl_title.pack(pady=(10, 2))

        self.lbl_desc    = tk.Label(right, text="", wraplength=720,
                                    justify="left", bg="#fff8e1")
        self.lbl_desc.pack(pady=4)

        self.lbl_formula = tk.Label(right, text="", fg="#1a5276",
                                    font=("Helvetica", 10, "bold"),
                                    wraplength=720, bg="#fff8e1")
        self.lbl_formula.pack(pady=2)

        self.lbl_example = tk.Label(right, text="", fg="#7d3c98",
                                    wraplength=720, bg="#fff8e1")
        self.lbl_example.pack(pady=2)

        # NEW: extra notes panel
        self.lbl_notes   = tk.Label(right, text="", wraplength=720,
                                    justify="left", bg="#fffde7",
                                    relief="groove", padx=8, pady=4)
        self.lbl_notes.pack(fill="x", padx=20, pady=(4, 8))

        tk.Label(right, text="Input (comma-separated):", bg="#fff8e1").pack()
        self.entry = tk.Entry(right, width=44)
        self.entry.pack(pady=4)

        tk.Button(right, text="Calculate", command=self._calculate,
                  bg="#e67e22", fg="white",
                  font=("Helvetica", 11, "bold"), width=16).pack(pady=6)

        self.lbl_result = tk.Label(right, text="", fg="#145a32",
                                   font=("Helvetica", 12),
                                   wraplength=720, bg="#fff8e1")
        self.lbl_result.pack(pady=10)

    # ── Event handlers ────────────────────────────────────────────────────────

    def _show_concept(self, name: str) -> None:
        c = next((x for x in self.concepts if x[1] == name), None)
        if not c:
            return
        _, nm, desc, formula, example, notes = c
        self.lbl_title.config(text=nm)
        self.lbl_desc.config(text=desc)
        self.lbl_formula.config(text=f"Formula:  {formula}")
        self.lbl_example.config(text=f"Example:  {example}")
        self.lbl_notes.config(text=f"💡 {notes}" if notes else "")
        self.entry.delete(0, "end")
        self.lbl_result.config(text="")

    def _calculate(self) -> None:
        name = self.lbl_title.cget("text")
        if name == "Select an Algebra Concept":
            messagebox.showerror("Error", "Select a concept first.")
            return

        raw = self.entry.get().strip()
        if not raw:
            messagebox.showerror("Error", "Please provide input values.")
            return

        # Parse comma-separated numbers
        try:
            nums = [float(v.strip()) for v in raw.split(",") if v.strip()]
        except ValueError:
            messagebox.showerror("Error",
                                 "Enter numeric values separated by commas.")
            return

        x = symbols('x')
        result_text = ""
        try:
            if name == "Linear Equation":
                # input: a, b  →  ax + b = 0
                if len(nums) < 2:
                    raise ValueError("Provide a and b for ax + b = 0")
                a, b = nums[:2]
                sol = solve(Eq(a*x + b, 0), x)
                result_text = f"x = {sol[0] if sol else 'No real solution'}"

            elif name == "Quadratic Equation":
                # input: a, b, c  →  ax² + bx + c = 0
                if len(nums) < 3:
                    raise ValueError("Provide a, b, c for ax² + bx + c = 0")
                a, b, c = nums[:3]
                sols = solve(Eq(a*x**2 + b*x + c, 0), x)
                disc = b**2 - 4*a*c
                result_text = (
                    f"Discriminant = {disc:.4f}\n" +
                    ("\n".join(f"x{i+1} = {s}" for i, s in enumerate(sols))
                     if sols else "No real solutions")
                )

            elif name == "Laws of Exponents":
                # input: base, e1, e2  →  base^e1 * base^e2
                if len(nums) < 3:
                    raise ValueError("Provide base, exponent1, exponent2")
                base, e1, e2 = nums[:3]
                result_text = (
                    f"{base}^{e1} × {base}^{e2}\n"
                    f"= {base}^({e1+e2})\n"
                    f"= {base**(e1+e2):.6g}"
                )

            elif name == "Factorization":
                # input: a, b  →  (a+b)^2
                if len(nums) < 2:
                    raise ValueError("Provide a and b")
                a, b = nums[:2]
                result_text = (
                    f"(a+b)² where a={a}, b={b}\n"
                    f"= {a}² + 2×{a}×{b} + {b}²\n"
                    f"= {a**2 + 2*a*b + b**2:.6g}\n\n"
                    f"Difference of squares: {a}²−{b}²\n"
                    f"= ({a}+{b})({a}−{b}) = {(a+b)*(a-b):.6g}"
                )

            elif name == "Arithmetic Progression (AP)":
                # input: a (first term), d (common difference), n (number of terms)
                if len(nums) < 3:
                    raise ValueError("Provide a (first term), d (difference), n (terms)")
                a, d, n = int(nums[0]), nums[1], int(nums[2])
                tn = a + (n - 1) * d
                sn = n / 2 * (2*a + (n-1)*d)
                result_text = (
                    f"First term a = {a},  d = {d},  n = {n}\n"
                    f"T{n} = {tn:.6g}\n"
                    f"Sum S{n} = {sn:.6g}"
                )

            elif name == "Geometric Progression (GP)":
                # input: a, r, n
                if len(nums) < 3:
                    raise ValueError("Provide a (first term), r (ratio), n (terms)")
                a, r, n = nums[0], nums[1], int(nums[2])
                tn = a * r**(n-1)
                sn = a * (r**n - 1) / (r - 1) if r != 1 else a * n
                result_text = (
                    f"First term a = {a},  r = {r},  n = {n}\n"
                    f"T{n} = {tn:.6g}\n"
                    f"Sum S{n} = {sn:.6g}"
                )
                if abs(r) < 1:
                    result_text += f"\nSum to ∞ = {a/(1-r):.6g}"

            elif name == "Logarithms":
                # input: base, value
                if len(nums) < 2:
                    raise ValueError("Provide base and value")
                base, val = nums[:2]
                if base <= 0 or base == 1 or val <= 0:
                    raise ValueError("Base must be >0 and ≠1; value must be >0")
                import math as _math
                result = _math.log(val) / _math.log(base)
                result_text = (
                    f"log_{base}({val}) = {result:.6g}\n"
                    f"ln({val}) = {_math.log(val):.6g}\n"
                    f"log₁₀({val}) = {_math.log10(val):.6g}"
                )

            elif name == "Binomial Theorem":
                # input: n (power), a, b  →  show first few terms of (a+b)^n
                if len(nums) < 3:
                    raise ValueError("Provide n, a, b for (a+b)ⁿ")
                n, a, b = int(nums[0]), nums[1], nums[2]
                import math as _math
                total = 0.0
                lines = []
                for k in range(n + 1):
                    coef = _math.comb(n, k)
                    term = coef * (a**(n-k)) * (b**k)
                    total += term
                    lines.append(f"  C({n},{k})×{a}^{n-k}×{b}^{k} = {term:.4g}")
                result_text = (
                    f"Expansion of ({a}+{b})^{n}:\n" +
                    "\n".join(lines) +
                    f"\nTotal = {total:.6g}"
                )

            elif name == "System of Linear Equations":
                # input: a1, b1, c1, a2, b2, c2  →  a1x+b1y=c1, a2x+b2y=c2
                if len(nums) < 6:
                    raise ValueError(
                        "Provide 6 values: a1,b1,c1,a2,b2,c2 "
                        "for a1x+b1y=c1, a2x+b2y=c2")
                a1, b1, c1, a2, b2, c2 = nums[:6]
                y = symbols('y')
                sols = solve([Eq(a1*x + b1*y, c1),
                               Eq(a2*x + b2*y, c2)], [x, y])
                result_text = (
                    f"Equations:\n  {a1}x + {b1}y = {c1}\n  {a2}x + {b2}y = {c2}\n"
                    + (f"x = {sols[x]},  y = {sols[y]}"
                       if isinstance(sols, dict) else str(sols))
                )

            elif name == "Inequalities":
                # input: a, b, c  →  ax + b > c  (solve for x)
                if len(nums) < 3:
                    raise ValueError("Provide a, b, c for ax + b > c")
                a, b, c = nums[:3]
                # Solve ax + b = c then note direction
                boundary = (c - b) / a
                direction = ">" if a > 0 else "<"
                result_text = (
                    f"Inequality: {a}x + {b} > {c}\n"
                    f"→ {a}x > {c - b}\n"
                    f"→ x {direction} {boundary:.6g}"
                )

            else:
                result_text = "Calculation not yet implemented for this concept."

        except Exception as exc:
            messagebox.showerror("Calculation Error", str(exc))
            return

        self.lbl_result.config(text=result_text)

        # Small point reward for performing a calculation
        user = self.current_user_callback()
        if user:
            models.update_user_progress(user[1], points=2)
