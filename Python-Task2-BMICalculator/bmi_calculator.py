"""
BMI Calculator - Advanced Version
Oasis Infobyte Python Programming Internship - Task 2

A desktop BMI Calculator built with Tkinter that:
  - Calculates BMI and classifies it into standard categories
  - Gives color-coded visual feedback
  - Validates all user input to prevent crashes
  - Stores every calculation in a local SQLite database (multi-user)
  - Shows a history table of past records
  - Plots a BMI trend graph (Matplotlib) for a selected user

Author: Tarun Sonaji
"""

import os
import sqlite3
import re
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")  # Ensure Matplotlib uses the Tkinter backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

# Use a relative path so the database sits next to this script, no matter
# which computer or folder the project is cloned into.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bmi_data.db")

# Colors used for the themed UI and for color-coded BMI feedback.
COLOR_BG = "#f0f4f8"
COLOR_HEADER = "#2c3e50"
COLOR_ACCENT = "#2e86de"
COLOR_TEXT = "#2c3e50"

CATEGORY_COLORS = {
    "Underweight": "#f0ad4e",  # amber warning
    "Normal": "#2ecc71",       # green success
    "Overweight": "#f39c12",   # orange warning
    "Obese": "#e74c3c",        # red danger
}

# A simple, permissive rule for a "valid" user name: letters, spaces,
# apostrophes and hyphens only, 1-40 characters.
NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z .'-]{0,39}$")


# --------------------------------------------------------------------------- #
# Database layer
# --------------------------------------------------------------------------- #

class BMIDatabase:
    """Handles all SQLite operations for BMI records."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        # A short timeout avoids indefinite hangs if the file is briefly locked.
        return sqlite3.connect(self.db_path, timeout=5)

    def _create_table(self):
        """Create the bmi_records table automatically if it doesn't exist."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS bmi_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT NOT NULL,
                        weight REAL NOT NULL,
                        height REAL NOT NULL,
                        bmi REAL NOT NULL,
                        category TEXT NOT NULL,
                        record_datetime TEXT NOT NULL
                    )
                    """
                )
                conn.commit()
        except sqlite3.Error as exc:
            # If the DB cannot even be created, the app cannot continue safely.
            messagebox.showerror(
                "Database Error",
                f"Could not initialize the database:\n{exc}",
            )
            raise

    def insert_record(self, user_name, weight, height, bmi, category):
        """Insert a single BMI record. Returns True on success."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO bmi_records
                        (user_name, weight, height, bmi, category, record_datetime)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_name,
                        weight,
                        height,
                        bmi,
                        category,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                )
                conn.commit()
            return True
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Could not save record:\n{exc}")
            return False

    def fetch_all_records(self):
        """Return all records, most recent first."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT user_name, weight, height, bmi, category, record_datetime
                    FROM bmi_records
                    ORDER BY id DESC
                    """
                )
                return cursor.fetchall()
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Could not load history:\n{exc}")
            return []

    def fetch_records_for_user(self, user_name):
        """Return all records for one user, oldest first (good for trend plotting)."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT user_name, weight, height, bmi, category, record_datetime
                    FROM bmi_records
                    WHERE user_name = ?
                    ORDER BY id ASC
                    """,
                    (user_name,),
                )
                return cursor.fetchall()
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Could not load records:\n{exc}")
            return []

    def fetch_distinct_users(self):
        """Return a sorted list of unique user names that have records."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT DISTINCT user_name FROM bmi_records ORDER BY user_name"
                )
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Could not load users:\n{exc}")
            return []


# --------------------------------------------------------------------------- #
# BMI calculation helpers
# --------------------------------------------------------------------------- #

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI = weight / height^2, rounded to 2 decimal places."""
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float) -> str:
    """Return the BMI category for a given BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# --------------------------------------------------------------------------- #
# Main application
# --------------------------------------------------------------------------- #

class BMICalculatorApp:
    """The main Tkinter application window."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("BMI Calculator - Oasis Infobyte Internship")
        self.root.geometry("480x560")
        self.root.minsize(440, 520)
        self.root.configure(bg=COLOR_BG)

        # Set up the database (creates the file/table if needed).
        self.db = BMIDatabase(DB_PATH)

        # Keeps the most recently calculated result so "Save Record" can use it.
        self.last_result = None  # dict: name, weight, height, bmi, category

        self._build_ui()

    # ------------------------------------------------------------------- #
    # UI construction
    # ------------------------------------------------------------------- #

    def _build_ui(self):
        style = ttk.Style()
        # "clam" theme renders custom colors more reliably across platforms.
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # ---- Header ----
        header = tk.Frame(self.root, bg=COLOR_HEADER, pady=16)
        header.pack(fill="x")
        tk.Label(
            header,
            text="BMI Calculator",
            font=("Segoe UI", 20, "bold"),
            bg=COLOR_HEADER,
            fg="white",
        ).pack()
        tk.Label(
            header,
            text="Oasis Infobyte - Python Programming Internship",
            font=("Segoe UI", 9),
            bg=COLOR_HEADER,
            fg="#dfe6e9",
        ).pack(pady=(2, 0))

        # ---- Input form ----
        form = tk.Frame(self.root, bg=COLOR_BG, padx=24, pady=20)
        form.pack(fill="x")

        self.name_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()

        self._add_form_row(form, 0, "Name:", self.name_var)
        self._add_form_row(form, 1, "Weight (kg):", self.weight_var)
        self._add_form_row(form, 2, "Height (m):", self.height_var)

        form.columnconfigure(1, weight=1)

        # ---- Calculate button ----
        calc_frame = tk.Frame(self.root, bg=COLOR_BG)
        calc_frame.pack(fill="x", padx=24, pady=(0, 10))
        calc_btn = tk.Button(
            calc_frame,
            text="Calculate BMI",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_ACCENT,
            fg="white",
            activebackground="#1b5fa8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=8,
            command=self.on_calculate,
        )
        calc_btn.pack(fill="x")

        # ---- Result display ----
        result_frame = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        result_frame.pack(fill="x", padx=24, pady=(4, 14))

        self.bmi_value_label = tk.Label(
            result_frame,
            text="--",
            font=("Segoe UI", 28, "bold"),
            bg="white",
            fg=COLOR_TEXT,
            pady=6,
        )
        self.bmi_value_label.pack()

        self.category_label = tk.Label(
            result_frame,
            text="Enter your details and press Calculate",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg=COLOR_TEXT,
        )
        self.category_label.pack(pady=(0, 10))

        # ---- Action buttons ----
        actions = tk.Frame(self.root, bg=COLOR_BG)
        actions.pack(fill="x", padx=24, pady=(0, 10))
        actions.columnconfigure((0, 1), weight=1)

        self._add_action_button(actions, "Save Record", self.on_save, 0, 0)
        self._add_action_button(actions, "View History", self.on_view_history, 0, 1)
        self._add_action_button(actions, "Show BMI Trend", self.on_show_trend, 1, 0)
        self._add_action_button(actions, "Clear", self.on_clear, 1, 1)

        exit_btn = tk.Button(
            self.root,
            text="Exit",
            font=("Segoe UI", 10),
            bg="#95a5a6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.on_exit,
        )
        exit_btn.pack(fill="x", padx=24, pady=(0, 20), ipady=4)

    def _add_form_row(self, parent, row, label_text, var):
        tk.Label(
            parent, text=label_text, font=("Segoe UI", 11), bg=COLOR_BG, fg=COLOR_TEXT
        ).grid(row=row, column=0, sticky="w", pady=6)
        entry = tk.Entry(parent, textvariable=var, font=("Segoe UI", 11), relief="solid", bd=1)
        entry.grid(row=row, column=1, sticky="ew", pady=6, padx=(10, 0), ipady=3)

    def _add_action_button(self, parent, text, command, row, col):
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg="#dfe6e9",
            fg=COLOR_TEXT,
            relief="flat",
            cursor="hand2",
            command=command,
        )
        btn.grid(row=row, column=col, sticky="ew", padx=4, pady=4, ipady=6)

    # ------------------------------------------------------------------- #
    # Validation
    # ------------------------------------------------------------------- #

    def _validate_inputs(self):
        """
        Validate name, weight and height.
        Returns (name, weight, height) on success, or None on failure
        (an appropriate messagebox is shown before returning None).
        """
        name = self.name_var.get().strip()
        weight_raw = self.weight_var.get().strip()
        height_raw = self.height_var.get().strip()

        # --- Name checks ---
        if not name:
            messagebox.showerror("Invalid Input", "Please enter your name.")
            return None
        if not NAME_PATTERN.match(name):
            messagebox.showerror(
                "Invalid Input",
                "Name should contain only letters, spaces, hyphens or apostrophes "
                "(max 40 characters) and must start with a letter.",
            )
            return None

        # --- Weight/height presence checks ---
        if not weight_raw or not height_raw:
            messagebox.showerror("Invalid Input", "Weight and height cannot be empty.")
            return None

        # --- Numeric checks ---
        try:
            weight = float(weight_raw)
        except ValueError:
            messagebox.showerror("Invalid Input", "Weight must be a valid number.")
            return None

        try:
            height = float(height_raw)
        except ValueError:
            messagebox.showerror("Invalid Input", "Height must be a valid number.")
            return None

        # --- Range checks (reject zero/negative and unrealistic values) ---
        if weight <= 0:
            messagebox.showerror("Invalid Input", "Weight must be greater than zero.")
            return None
        if height <= 0:
            messagebox.showerror("Invalid Input", "Height must be greater than zero.")
            return None
        if weight > 500:
            messagebox.showerror("Invalid Input", "Please enter a realistic weight (<= 500 kg).")
            return None
        if height > 3:
            messagebox.showerror("Invalid Input", "Please enter height in meters (e.g. 1.75).")
            return None

        return name, weight, height

    # ------------------------------------------------------------------- #
    # Button handlers
    # ------------------------------------------------------------------- #

    def on_calculate(self):
        validated = self._validate_inputs()
        if validated is None:
            return

        name, weight, height = validated
        try:
            bmi = calculate_bmi(weight, height)
        except ZeroDivisionError:
            # Defensive guard; height <= 0 is already blocked above.
            messagebox.showerror("Calculation Error", "Height cannot be zero.")
            return

        category = classify_bmi(bmi)
        color = CATEGORY_COLORS.get(category, COLOR_TEXT)

        self.bmi_value_label.config(text=f"{bmi:.2f}", fg=color)
        self.category_label.config(text=category, fg=color)

        # Remember this result so it can be saved without recalculating.
        self.last_result = {
            "name": name,
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "category": category,
        }

    def on_save(self):
        if self.last_result is None:
            messagebox.showwarning(
                "Nothing to Save", "Please calculate a BMI before saving a record."
            )
            return

        r = self.last_result
        success = self.db.insert_record(
            r["name"], r["weight"], r["height"], r["bmi"], r["category"]
        )
        if success:
            messagebox.showinfo("Saved", f"Record saved for {r['name']}.")

    def on_view_history(self):
        HistoryWindow(self.root, self.db)

    def on_show_trend(self):
        TrendWindow(self.root, self.db)

    def on_clear(self):
        self.name_var.set("")
        self.weight_var.set("")
        self.height_var.set("")
        self.bmi_value_label.config(text="--", fg=COLOR_TEXT)
        self.category_label.config(
            text="Enter your details and press Calculate", fg=COLOR_TEXT
        )
        self.last_result = None

    def on_exit(self):
        self.root.destroy()


# --------------------------------------------------------------------------- #
# History window
# --------------------------------------------------------------------------- #

class HistoryWindow(tk.Toplevel):
    """A window that lists BMI records, optionally filtered by user."""

    def __init__(self, parent, db: BMIDatabase):
        super().__init__(parent)
        self.db = db
        self.title("BMI History")
        self.geometry("720x420")
        self.configure(bg=COLOR_BG)

        top_bar = tk.Frame(self, bg=COLOR_BG, pady=10, padx=10)
        top_bar.pack(fill="x")

        tk.Label(
            top_bar, text="Filter by user:", bg=COLOR_BG, font=("Segoe UI", 10)
        ).pack(side="left")

        users = ["All Users"] + self.db.fetch_distinct_users()
        self.user_var = tk.StringVar(value="All Users")
        self.user_combo = ttk.Combobox(
            top_bar, textvariable=self.user_var, values=users, state="readonly", width=25
        )
        self.user_combo.pack(side="left", padx=8)
        self.user_combo.bind("<<ComboboxSelected>>", lambda e: self._load_records())

        tk.Button(
            top_bar, text="Refresh", command=self._load_records, bg="#dfe6e9"
        ).pack(side="left", padx=8)

        # ---- Table ----
        columns = ("user", "weight", "height", "bmi", "category", "datetime")
        headings = ["User", "Weight (kg)", "Height (m)", "BMI", "Category", "Date/Time"]

        table_frame = tk.Frame(self, padx=10)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col, heading in zip(columns, headings):
            self.tree.heading(col, text=heading)
            self.tree.column(col, anchor="center", width=110)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._load_records()

    def _load_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        selected_user = self.user_var.get()
        if selected_user and selected_user != "All Users":
            records = self.db.fetch_records_for_user(selected_user)
            records = list(reversed(records))  # show most recent first
        else:
            records = self.db.fetch_all_records()

        if not records:
            self.tree.insert("", "end", values=("No records found", "", "", "", "", ""))
            return

        for user, weight, height, bmi, category, record_datetime in records:
            self.tree.insert(
                "",
                "end",
                values=(user, f"{weight:.1f}", f"{height:.2f}", f"{bmi:.2f}", category, record_datetime),
            )


# --------------------------------------------------------------------------- #
# BMI trend window
# --------------------------------------------------------------------------- #

class TrendWindow(tk.Toplevel):
    """A window that plots a user's BMI history as a line chart."""

    def __init__(self, parent, db: BMIDatabase):
        super().__init__(parent)
        self.db = db
        self.title("BMI Trend")
        self.geometry("700x520")
        self.configure(bg=COLOR_BG)

        top_bar = tk.Frame(self, bg=COLOR_BG, pady=10, padx=10)
        top_bar.pack(fill="x")

        tk.Label(
            top_bar, text="Select user:", bg=COLOR_BG, font=("Segoe UI", 10)
        ).pack(side="left")

        users = self.db.fetch_distinct_users()
        self.user_var = tk.StringVar(value=users[0] if users else "")
        self.user_combo = ttk.Combobox(
            top_bar, textvariable=self.user_var, values=users, state="readonly", width=25
        )
        self.user_combo.pack(side="left", padx=8)
        self.user_combo.bind("<<ComboboxSelected>>", lambda e: self._draw_chart())

        # Matplotlib figure embedded in the Tkinter window.
        self.figure = Figure(figsize=(6, 4.5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        if not users:
            self._draw_empty("No BMI records found yet.\nSave a record first.")
        else:
            self._draw_chart()

    def _draw_empty(self, message):
        self.ax.clear()
        self.ax.text(
            0.5, 0.5, message, ha="center", va="center", fontsize=12, color="#7f8c8d"
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def _draw_chart(self):
        user = self.user_var.get()
        if not user:
            self._draw_empty("No user selected.")
            return

        records = self.db.fetch_records_for_user(user)
        if not records:
            self._draw_empty(f"No records found for {user}.")
            return

        dates = [r[5] for r in records]
        bmis = [r[3] for r in records]

        self.ax.clear()
        self.ax.plot(dates, bmis, marker="o", color=COLOR_ACCENT, linewidth=2)
        self.ax.set_title(f"BMI Trend for {user}")
        self.ax.set_xlabel("Date / Time")
        self.ax.set_ylabel("BMI")
        self.ax.grid(True, linestyle="--", alpha=0.5)

        # Reference lines for the standard BMI category boundaries.
        for boundary in (18.5, 25, 30):
            self.ax.axhline(y=boundary, color="#bdc3c7", linestyle=":", linewidth=1)

        # Rotate date labels so they don't overlap on the x-axis.
        self.figure.autofmt_xdate(rotation=30)
        self.canvas.draw()


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main():
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
