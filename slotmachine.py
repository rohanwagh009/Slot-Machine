import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine Game")
        # Ensure the window is large enough to see the changes
        self.root.geometry("800x600")

        self.balance = 0

        self.create_widgets()

    def create_widgets(self):
        # Load background image
        # Make sure this path is correct
        self.bg_image = Image.open("slots.jpg")
        self.bg_image = self.bg_image.resize(
            (800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        label_font = ("Helvetica", 14, "bold")
        button_font = ("Helvetica", 12, "bold")

        self.balance_label = tk.Label(
            self.root, text="Balance: $0", bg='white', font=label_font)
        self.canvas.create_window(400, 50, window=self.balance_label)

        self.deposit_button = tk.Button(
            self.root, text="Deposit", command=self.deposit, bg='#FFD700', font=button_font, width=15, height=2)
        self.canvas.create_window(400, 100, window=self.deposit_button)

        self.lines_label = tk.Label(
            self.root, text="Lines: 1", bg='white', font=label_font)
        self.canvas.create_window(400, 150, window=self.lines_label)

        self.lines_scale = tk.Scale(
            self.root, from_=1, to=MAX_LINES, orient=tk.HORIZONTAL, bg='white', font=label_font)
        self.canvas.create_window(400, 200, window=self.lines_scale)

        self.bet_label = tk.Label(
            self.root, text="Bet: $1", bg='white', font=label_font)
        self.canvas.create_window(400, 250, window=self.bet_label)

        self.bet_scale = tk.Scale(
            self.root, from_=MIN_BET, to=MAX_BET, orient=tk.HORIZONTAL, bg='white', font=label_font)
        self.canvas.create_window(400, 300, window=self.bet_scale)

        self.spin_button = tk.Button(
            self.root, text="Spin", command=self.spin, bg='#32CD32', font=button_font, width=15, height=2)
        # Positioning in the top right corner
        self.canvas.create_window(700, 50, window=self.spin_button)

        self.slot_frame = tk.Frame(self.root, bg='white')
        self.canvas.create_window(400, 450, window=self.slot_frame)

        self.slot_labels = []
        for row in range(ROWS):
            row_labels = []
            for col in range(COLS):
                label = tk.Label(self.slot_frame, text="", width=8, height=3,
                                 borderwidth=2, relief="groove", bg='white', font=label_font)
                label.grid(row=row, column=col, padx=5, pady=5)
                row_labels.append(label)
            self.slot_labels.append(row_labels)

    def deposit(self):
        amount = simpledialog.askinteger(
            "Deposit", "What would you like to deposit? $")
        if amount and amount > 0:
            self.balance += amount
            self.update_balance()
        else:
            messagebox.showerror(
                "Invalid Deposit", "Deposit amount must be greater than 0.")

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")

    def spin(self):
        lines = self.lines_scale.get()
        bet = self.bet_scale.get()
        total_bet = bet * lines

        if total_bet > self.balance:
            messagebox.showerror(
                "Insufficient Funds", f"You do not have enough to bet, your current balance is: ${self.balance}")
            return

        self.balance -= total_bet
        self.update_balance()

        slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)
        self.update_slots(slots)
        winnings, winning_lines = self.check_winnings(
            slots, lines, bet, symbol_value)
        self.balance += winnings
        self.update_balance()

        if winnings > 0:
            messagebox.showinfo(
                "Congratulations!", f"You won ${winnings} on lines: {', '.join(map(str, winning_lines))}")
        else:
            messagebox.showinfo("Better Luck Next Time",
                                "You didn't win anything.")

    def get_slot_machine_spin(self, rows, cols, symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)

        columns = []
        for _ in range(cols):
            column = []
            current_symbols = all_symbols[:]
            for _ in range(rows):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)

            columns.append(column)

        return columns

    def update_slots(self, slots):
        for row in range(ROWS):
            for col in range(COLS):
                self.slot_labels[row][col].config(text=slots[col][row])

    def check_winnings(self, columns, lines, bet, values):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines


if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()
