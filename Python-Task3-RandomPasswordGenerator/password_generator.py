import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")

        # Open maximized
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry("1000x750")

        self.root.minsize(850, 650)

        # Session-only password history
        self.history = []

        # Variables
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)

        self.setup_ui()

    def setup_ui(self):

        # Main container
        main_frame = tk.Frame(
            self.root,
            padx=50,
            pady=25
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ==============================
        # TITLE
        # ==============================

        title = tk.Label(
            main_frame,
            text="🔐 Secure Password Generator",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=(0, 5))

        subtitle = tk.Label(
            main_frame,
            text="Generate strong and secure passwords instantly",
            font=("Arial", 13)
        )

        subtitle.pack(pady=(0, 15))

        # ==============================
        # GENERATED PASSWORD
        # ==============================

        password_frame = tk.LabelFrame(
            main_frame,
            text="Generated Password",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=15
        )

        password_frame.pack(
            fill="x",
            pady=8
        )

        self.password_entry = tk.Entry(
            password_frame,
            font=("Consolas", 18),
            justify="center"
        )

        self.password_entry.pack(
            fill="x",
            pady=5
        )

        self.strength_label = tk.Label(
            password_frame,
            text="Strength: Strong 💪",
            font=("Arial", 12, "bold")
        )

        self.strength_label.pack(
            pady=6
        )

        # ==============================
        # PASSWORD LENGTH
        # ==============================

        length_frame = tk.LabelFrame(
            main_frame,
            text="Password Length",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )

        length_frame.pack(
            fill="x",
            pady=8
        )

        self.length_scale = tk.Scale(
            length_frame,
            from_=8,
            to=50,
            orient="horizontal",
            variable=self.length_var,
            command=self.update_length_label,
            showvalue=False
        )

        self.length_scale.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        self.length_label = tk.Label(
            length_frame,
            text="16",
            font=("Arial", 13, "bold"),
            width=5
        )

        self.length_label.pack(
            side="left"
        )

        # ==============================
        # CHARACTER TYPES
        # ==============================

        options_frame = tk.LabelFrame(
            main_frame,
            text="Character Types",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )

        options_frame.pack(
            fill="x",
            pady=8
        )

        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)

        tk.Checkbutton(
            options_frame,
            text="Uppercase Letters (A-Z)",
            variable=self.upper_var,
            font=("Arial", 11)
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=4
        )

        tk.Checkbutton(
            options_frame,
            text="Lowercase Letters (a-z)",
            variable=self.lower_var,
            font=("Arial", 11)
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=20,
            pady=4
        )

        tk.Checkbutton(
            options_frame,
            text="Numbers (0-9)",
            variable=self.number_var,
            font=("Arial", 11)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=4
        )

        tk.Checkbutton(
            options_frame,
            text="Symbols (!@#$...)",
            variable=self.symbol_var,
            font=("Arial", 11)
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=20,
            pady=4
        )
        # ==============================
        # SECURITY OPTIONS
        # ==============================
        
        security_frame = tk.LabelFrame(
            main_frame,
            text="Security Options",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )

        security_frame.pack(
            fill="x",
            pady=8
        )

        tk.Checkbutton(
            security_frame,
            text="Exclude ambiguous characters (0, O, l, 1)",
            variable=self.ambiguous_var,
            font=("Arial", 11)
        ).pack(
            anchor="w",
            padx=20
        )

        # ==============================
        # BUTTONS
        # ==============================

        button_frame = tk.Frame(main_frame)

        button_frame.pack(
            pady=12
        )

        tk.Button(
            button_frame,
            text="🔑 Generate Password",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=9,
            command=self.generate_password
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        tk.Button(
            button_frame,
            text="📋 Copy to Clipboard",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=9,
            command=self.copy_password
        ).grid(
            row=0,
            column=1,
            padx=8
        )

        # ==============================
        # RECENT PASSWORD HISTORY
        # ==============================

        history_frame = tk.LabelFrame(
            main_frame,
            text="Recent Passwords (Session Only)",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=10
        )

        history_frame.pack(
            fill="both",
            expand=True,
            pady=8
        )

        # History container
        history_container = tk.Frame(history_frame)

        history_container.pack(
            fill="both",
            expand=True
        )

        # Scrollbar
        scrollbar = tk.Scrollbar(
            history_container
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Listbox
        self.history_listbox = tk.Listbox(
            history_container,
            font=("Consolas", 12),
            selectmode="single",
            yscrollcommand=scrollbar.set,
            height=5
        )

        self.history_listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.history_listbox.yview
        )

        # Click history item
        self.history_listbox.bind(
            "<<ListboxSelect>>",
            self.select_history_password
        )

        # Instruction
        info = tk.Label(
            main_frame,
            text="Click a previous password to restore and copy it.",
            font=("Arial", 10)
        )

        info.pack(
            pady=(5, 0)
        )

    # ==============================
    # LENGTH LABEL
    # ==============================

    def update_length_label(self, value):

        self.length_label.config(
            text=str(int(float(value)))
        )

    # ==============================
    # CHARACTER SETS
    # ==============================

    def get_character_sets(self):

        sets = []

        if self.upper_var.get():
            sets.append(string.ascii_uppercase)

        if self.lower_var.get():
            sets.append(string.ascii_lowercase)

        if self.number_var.get():
            sets.append(string.digits)

        if self.symbol_var.get():
            sets.append(string.punctuation)

        # Remove ambiguous characters
        if self.ambiguous_var.get():

            ambiguous = "0Ol1"

            sets = [
                "".join(
                    char
                    for char in charset
                    if char not in ambiguous
                )
                for charset in sets
            ]

        return sets

    # ==============================
    # GENERATE PASSWORD
    # ==============================

    def generate_password(self):

        length = self.length_var.get()

        # At least 2 character types
        selected_count = sum([
            self.upper_var.get(),
            self.lower_var.get(),
            self.number_var.get(),
            self.symbol_var.get()
        ])
        if length < 8:

            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )

            return
        if selected_count < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least 2 character types."
            )
            return

        selected_sets = self.get_character_sets()

        # Check if any selected set became empty
        if any(
            len(charset) == 0
            for charset in selected_sets
        ):

            messagebox.showerror(
                "Invalid Selection",
                "The selected security options removed all characters "
                "from a selected character type."
            )

            return

        # Guarantee one character from each selected type
        password_characters = [
            secrets.choice(charset)
            for charset in selected_sets
        ]

        # Combine character sets
        all_characters = "".join(
            selected_sets
        )

        # Remaining characters
        remaining = length - len(
            password_characters
        )

        password_characters.extend(
            secrets.choice(all_characters)
            for _ in range(remaining)
        )

        # Secure shuffle
        secrets.SystemRandom().shuffle(
            password_characters
        )

        password = "".join(
            password_characters
        )

        # Display password
        self.password_entry.delete(
            0,
            tk.END
        )

        self.password_entry.insert(
            0,
            password
        )

        # Password strength
        strength = self.calculate_strength(
            length,
            selected_count
        )

        self.strength_label.config(
            text=f"Strength: {strength}"
        )

        # Add password to history
        self.history.insert(
            0,
            password
        )

        # Keep only latest 5
        self.history = self.history[:5]

        # Update history display
        self.update_history()

        # Automatically copy password
        try:
            pyperclip.copy(password)
        except Exception:
            pass
    # ==============================
    # PASSWORD STRENGTH
    # ==============================

    def calculate_strength(
        self,
        length,
        character_types
    ):

        if length >= 16 and character_types >= 4:

            return "Strong 💪"

        elif length >= 12 and character_types >= 3:

            return "Medium 🛡️"

        else:

            return "Weak ⚠️"

    # ==============================
    # COPY PASSWORD
    # ==============================

    def copy_password(self):

        password = self.password_entry.get()

        if not password:

            messagebox.showwarning(
                "No Password",
                "Generate a password first."
            )

            return

        try:

            pyperclip.copy(password)

            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard!"
            )

        except Exception:

            messagebox.showerror(
                "Clipboard Error",
                "Could not copy the password to clipboard."
            )

    # ==============================
    # UPDATE HISTORY
    # ==============================

    def update_history(self):

        self.history_listbox.delete(
            0,
            tk.END
        )

        for index, password in enumerate(
            self.history,
            start=1
        ):

            self.history_listbox.insert(
                tk.END,
                f"{index}. {password}"
            )
    # ==============================
    # SELECT HISTORY PASSWORD
    # ==============================

    def select_history_password(self, event):

        selection = self.history_listbox.curselection()

        if not selection:
            return

        index = selection[0]

        password = self.history[index]

        # Put selected password into main field
        self.password_entry.delete(
            0,
            tk.END
        )

        self.password_entry.insert(
            0,
            password
        )

        # Copy selected password
        try:
            pyperclip.copy(password)
        except Exception:
            pass

        # Determine password character diversity
        character_types = 0

        if any(
            char.isupper()
            for char in password
        ):
            character_types += 1

        if any(
            char.islower()
            for char in password
        ):
            character_types += 1

        if any(
            char.isdigit()
            for char in password
        ):
            character_types += 1

        if any(
            char in string.punctuation
            for char in password
        ):
            character_types += 1

        # Update strength
        strength = self.calculate_strength(
            len(password),
            character_types
        )
        self.strength_label.config(
            text=f"Strength: {strength}"
        )
        
# ==============================
# START APPLICATION
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()