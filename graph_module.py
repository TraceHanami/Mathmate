# graph_module.py
# ─────────────────────────────────────────────────────────────────────────────
# GRAPH PLOTTER TAB
# Plots any mathematical expression entered by the user.
# Uses matplotlib embedded inside a Tkinter Canvas via FigureCanvasTkAgg.
# Pre-set quick-buttons cover common functions.
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import messagebox,ttk
import numpy as np

# Matplotlib is an optional dependency.  Import defensively so the rest of the
# app still works even if it is not installed.
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    _MATPLOTLIB_OK = True
except ImportError:
    _MATPLOTLIB_OK = False


# ── Preset expressions the user can inject with one click ─────────────────────
_PRESETS = [
    ("sin(x)",       "np.sin(x)",            "Sine wave"),
    ("cos(x)",       "np.cos(x)",            "Cosine wave"),
    ("tan(x)",       "np.tan(x)",            "Tangent"),
    ("x²",           "x**2",                 "Parabola"),
    ("x³",           "x**3",                 "Cubic"),
    ("√x",           "np.sqrt(np.abs(x))",   "Square root"),
    ("1/x",          "1/x",                  "Reciprocal"),
    ("eˣ",           "np.exp(x)",            "Exponential"),
    ("ln(x)",        "np.log(np.abs(x)+1e-9)","Log"),
    ("|x|",          "np.abs(x)",            "Absolute value"),
    ("sin²+cos²",    "np.sin(x)**2+np.cos(x)**2", "Pythagorean identity (=1)"),
    ("x²−4",         "x**2-4",              "Roots at ±2"),
]


class GraphFrame(tk.Frame):

    def __init__(self, parent, current_user_callback):
        super().__init__(parent, bg="#f0f4f8")
        self.current_user_callback = current_user_callback
        self.pack(fill="both", expand=True)
        self._expressions: list[dict] = []   # list of {expr_str, colour}
        self._colours = ["#2980b9", "#e74c3c", "#27ae60",
                         "#9b59b6", "#f39c12", "#1abc9c"]
        self._colour_idx = 0
        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        if not _MATPLOTLIB_OK:
            tk.Label(self,
                     text="⚠  matplotlib is not installed.\n\n"
                          "Run:  pip install matplotlib",
                     font=("Helvetica", 13), bg="#f0f4f8",
                     fg="#c0392b").pack(expand=True)
            return

        # ── Left control panel ────────────────────────────────────────────────
        left = tk.Frame(self, width=220, bg="#dce7f3")
        left.pack(side="left", fill="y", padx=6, pady=6)
        left.pack_propagate(False)

        tk.Label(left, text="Graph Plotter",
                 font=("Helvetica", 13, "bold"),
                 bg="#dce7f3").pack(pady=8)

        # Expression entry
        tk.Label(left, text="Expression (use 'x'):",
                 bg="#dce7f3").pack(anchor="w", padx=6)
        self.entry_expr = tk.Entry(left, width=26)
        self.entry_expr.pack(padx=6, pady=4, fill="x")
        self.entry_expr.insert(0, "np.sin(x)")

        # X range
        range_frame = tk.Frame(left, bg="#dce7f3")
        range_frame.pack(fill="x", padx=6)
        tk.Label(range_frame, text="x from:", bg="#dce7f3", width=7,
                 anchor="w").pack(side="left")
        self.entry_xmin = tk.Entry(range_frame, width=6)
        self.entry_xmin.insert(0, "-10")
        self.entry_xmin.pack(side="left")
        tk.Label(range_frame, text=" to:", bg="#dce7f3").pack(side="left")
        self.entry_xmax = tk.Entry(range_frame, width=6)
        self.entry_xmax.insert(0, "10")
        self.entry_xmax.pack(side="left")

        # Plot button
        tk.Button(left, text="➕  Add to Plot",
                  command=self._add_plot,
                  bg="#2980b9", fg="white",
                  font=("Helvetica", 10, "bold")).pack(fill="x", padx=6, pady=6)

        tk.Button(left, text="🗑  Clear All",
                  command=self._clear,
                  bg="#e74c3c", fg="white").pack(fill="x", padx=6, pady=2)

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)

        # Preset buttons
        tk.Label(left, text="Quick Presets:",
                 font=("Helvetica", 10, "bold"),
                 bg="#dce7f3").pack(anchor="w", padx=6)

        canvas_presets = tk.Canvas(left, bg="#dce7f3", highlightthickness=0)
        sb = tk.Scrollbar(left, orient="vertical",
                          command=canvas_presets.yview)
        pf = tk.Frame(canvas_presets, bg="#dce7f3")
        pf.bind("<Configure>",
                lambda e: canvas_presets.configure(
                    scrollregion=canvas_presets.bbox("all")))
        canvas_presets.create_window((0, 0), window=pf, anchor="nw")
        canvas_presets.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas_presets.pack(side="left", fill="both", expand=True)

        for label, expr, tip in _PRESETS:
            tk.Button(pf, text=f"{label}  ({tip})", anchor="w",
                      width=26, padx=4,
                      command=lambda e=expr: self._preset(e)
                      ).pack(fill="x", pady=2, padx=4)

        # ── Right: plot area ──────────────────────────────────────────────────
        right = tk.Frame(self, bg="#ffffff")
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        self.fig = Figure(figsize=(6, 5), dpi=96)
        self.ax  = self.fig.add_subplot(111)
        self._style_axes()

        self.mpl_canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.mpl_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Legend / expression list
        self.lbl_legend = tk.Label(right, text="",
                                   bg="#f0f0f0", anchor="w",
                                   font=("Courier", 9))
        self.lbl_legend.pack(fill="x", padx=4, pady=2)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _style_axes(self) -> None:
        self.ax.set_facecolor("#fdfefe")
        self.fig.patch.set_facecolor("#ffffff")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.axhline(0, color="#bdc3c7", linewidth=0.8, linestyle="--")
        self.ax.axvline(0, color="#bdc3c7", linewidth=0.8, linestyle="--")
        self.ax.grid(True, linestyle=":", alpha=0.5)
        self.ax.set_title("Function Plotter", fontsize=11)

    def _preset(self, expr: str) -> None:
        self.entry_expr.delete(0, "end")
        self.entry_expr.insert(0, expr)

    def _add_plot(self) -> None:
        expr_str = self.entry_expr.get().strip()
        if not expr_str:
            messagebox.showerror("Error", "Enter an expression.")
            return
        try:
            xmin = float(self.entry_xmin.get())
            xmax = float(self.entry_xmax.get())
            if xmin >= xmax:
                raise ValueError("x_min must be less than x_max")
        except ValueError as e:
            messagebox.showerror("Range Error", str(e))
            return

        colour = self._colours[self._colour_idx % len(self._colours)]
        self._colour_idx += 1

        try:
            x = np.linspace(xmin, xmax, 2000)
            # Safe eval: only numpy is exposed
            y = eval(expr_str, {"__builtins__": {}}, {"np": np, "x": x})
            y = np.array(y, dtype=float)
            # Mask extreme values to keep plot readable
            y[np.abs(y) > 1e6] = np.nan
        except Exception as e:
            messagebox.showerror("Expression Error",
                                 f"Could not evaluate:\n{expr_str}\n\n{e}")
            return

        self.ax.plot(x, y, color=colour, linewidth=1.8, label=expr_str)
        self._expressions.append({"expr": expr_str, "colour": colour})
        self.ax.legend(fontsize=8, loc="upper right")
        self._refresh_legend()
        self.mpl_canvas.draw()

    def _clear(self) -> None:
        self._expressions = []
        self._colour_idx  = 0
        self.ax.cla()
        self._style_axes()
        self.mpl_canvas.draw()
        self.lbl_legend.config(text="")

    def _refresh_legend(self) -> None:
        lines = [f"  ●  {e['expr']}" for e in self._expressions]
        self.lbl_legend.config(text="   ".join(lines))
