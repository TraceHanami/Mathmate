# main.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import db_init, models
from shapes_module import ShapesFrame
from algebra_module import AlgebraFrame
from trig_module import TrigFrame

def ensure_db():
    db_init.create_and_seed_db()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MathMate")
        self.root.geometry("1000x700")
        ensure_db()

        # top: user area
        top = tk.Frame(root, pady=6)
        top.pack(fill="x")
        tk.Label(top, text="MathMate", font=("Helvetica", 18, "bold")).pack(side="left", padx=12)
        self.users_combo = ttk.Combobox(top, state="readonly")
        self.users_combo.pack(side="right", padx=12)
        tk.Button(top, text="Add User", command=self.add_user).pack(side="right")
        tk.Button(top, text="Refresh Users", command=self.load_users).pack(side="right", padx=8)
        self.load_users()
        self.users_combo.bind("<<ComboboxSelected>>", lambda e: self.on_user_change())

        # middle: notebook tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # frames created after user is selected, but we can create and pass callback to get current user
        self.frames = {}
        # create container frames
        container_shapes = tk.Frame(self.notebook)
        container_algebra = tk.Frame(self.notebook)
        container_trig = tk.Frame(self.notebook)

        self.notebook.add(container_shapes, text="Shapes")
        self.notebook.add(container_algebra, text="Algebra")
        self.notebook.add(container_trig, text="Trigonometry")

        # instantiate functional frames with callback to current user
        self.frames['shapes'] = ShapesFrame(container_shapes, self.get_current_user)
        self.frames['algebra'] = AlgebraFrame(container_algebra, self.get_current_user)
        self.frames['trig'] = TrigFrame(container_trig, self.get_current_user)

        # bottom: user stats
        self.status = tk.Label(root, text="No user selected", relief="sunken", anchor="w")
        self.status.pack(fill="x", side="bottom")

    def load_users(self):
        users = models.get_users()
        names = [u[1] for u in users]
        self.users_combo['values'] = names

    def add_user(self):
        name = simpledialog.askstring("New User", "Enter username:")
        if name:
            try:
                models.create_user(name.strip())
                self.load_users()
                messagebox.showinfo("Success", f"User {name} created.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def get_current_user(self):
        sel = self.users_combo.get()
        if not sel:
            return None
        return models.get_user_by_name(sel)

    def on_user_change(self):
        user = self.get_current_user()
        if user:
            self.status.config(text=f"User: {user[1]} | Points: {user[2]} | Level: {user[3]} | Quizzes: {user[4]}")
        else:
            self.status.config(text="No user selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
