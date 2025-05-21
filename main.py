import tkinter as tk
from tkinter import ttk
import math


class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Moderner Taschenrechner")
        self.root.geometry("320x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Farben und Stile
        self.LIGHT_GRAY = "#F5F5F5"
        self.WHITE = "#FFFFFF"
        self.LIGHT_BLUE = "#CCEDFF"
        self.BLUE = "#0078D7"
        self.DARK_GRAY = "#333333"
        self.ORANGE = "#FF9500"

        # Variablen
        self.current_expression = ""
        self.total_expression = ""
        self.last_clicked_equal = False

        # Display Frame erstellen
        self.display_frame = self.create_display_frame()

        # Ergebnis und Eingabe Label
        self.total_label, self.current_label = self.create_display_labels()

        # Ziffern-Grid
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 3)
        }

        # Operationen
        self.operations = {"/": "÷", "*": "×", "-": "-", "+": "+"}

        # Buttons Frame erstellen
        self.buttons_frame = self.create_buttons_frame()

        # Alle Reihen expandieren lassen
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # Buttons erstellen
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

    def create_display_frame(self):
        frame = tk.Frame(self.root, bg=self.DARK_GRAY, height=80)
        frame.pack(expand=True, fill="both", padx=4, pady=4)
        return frame

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text="", anchor="e", bg=self.DARK_GRAY,
                               fg=self.WHITE, padx=10, font=("Arial", 14))
        total_label.pack(expand=True, fill="both")

        current_label = tk.Label(self.display_frame, text="0", anchor="e", bg=self.DARK_GRAY,
                                 fg=self.WHITE, padx=10, font=("Arial", 30, "bold"))
        current_label.pack(expand=True, fill="both")

        return total_label, current_label

    def create_buttons_frame(self):
        frame = tk.Frame(self.root, bg=self.LIGHT_GRAY)
        frame.pack(expand=True, fill="both", padx=4, pady=4)
        return frame

    def create_digit_buttons(self):
        for digit, grid_val in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=self.WHITE, fg=self.DARK_GRAY,
                               font=("Arial", 18), borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_val[0], column=grid_val[1], sticky=tk.NSEW, padx=2, pady=2)

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=self.LIGHT_BLUE, fg=self.DARK_GRAY,
                               font=("Arial", 18), borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW, padx=2, pady=2)
            i += 1

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_backspace_button()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=self.ORANGE, fg=self.WHITE,
                           font=("Arial", 18), borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW, padx=2, pady=2)

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=self.BLUE, fg=self.WHITE,
                           font=("Arial", 18), borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=4, sticky=tk.NSEW, padx=2, pady=2)

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x²", bg=self.LIGHT_BLUE, fg=self.DARK_GRAY,
                           font=("Arial", 18), borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW, padx=2, pady=2)

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="√", bg=self.LIGHT_BLUE, fg=self.DARK_GRAY,
                           font=("Arial", 18), borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW, padx=2, pady=2)

    def create_backspace_button(self):
        button = tk.Button(self.buttons_frame, text="⌫", bg=self.LIGHT_BLUE, fg=self.DARK_GRAY,
                           font=("Arial", 18), borderwidth=0, command=self.backspace)
        button.grid(row=4, column=1, sticky=tk.NSEW, padx=2, pady=2)

    def add_to_expression(self, value):
        if self.last_clicked_equal:
            self.current_expression = ""
            self.total_expression = ""
            self.last_clicked_equal = False

        self.current_expression += str(value)
        self.update_current_label()

    def append_operator(self, operator):
        self.last_clicked_equal = False

        if self.current_expression:
            self.total_expression += self.current_expression
            self.current_expression = ""

        if self.total_expression and self.total_expression[-1] in self.operations:
            self.total_expression = self.total_expression[:-1]

        self.total_expression += operator
        self.update_total_label()
        self.update_current_label()

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.last_clicked_equal = False
        self.update_total_label()
        self.update_current_label()

    def backspace(self):
        if len(self.current_expression) > 0:
            self.current_expression = self.current_expression[:-1]
            self.update_current_label()

    def square(self):
        if self.current_expression:
            try:
                value = float(self.current_expression)
                self.current_expression = str(value ** 2)
                self.update_current_label()
                self.last_clicked_equal = True
            except:
                self.current_expression = "Fehler"
                self.update_current_label()

    def sqrt(self):
        if self.current_expression:
            try:
                value = float(self.current_expression)
                if value >= 0:
                    self.current_expression = str(math.sqrt(value))
                    self.update_current_label()
                    self.last_clicked_equal = True
                else:
                    self.current_expression = "Fehler"
                    self.update_current_label()
            except:
                self.current_expression = "Fehler"
                self.update_current_label()

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
            self.update_current_label()
            self.last_clicked_equal = True
        except Exception as e:
            self.current_expression = "Fehler"
            self.update_current_label()

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_current_label(self):
        if not self.current_expression:
            self.current_label.config(text="0")
        else:
            self.current_label.config(text=self.current_expression)


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(default="")  # Hier könntest du ein Icon einbinden
    calc = ModernCalculator(root)
    root.mainloop()
