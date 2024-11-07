import tkinter as tk
from tkinter import messagebox
from board import Board
from gomoku_ai import GomokuAI


class GomokuGUI:
    def __init__(self, master, size=19):
        self.master = master
        self.master.title("Caro Game with AI")

        self.size = size
        self.cell_size = 30
        self.board = Board(size)
        self.ai = GomokuAI(depth=2)  # Độ sâu của AI giảm để tăng tốc độ
        self.buttons = [[None for _ in range(size)] for _ in range(size)]

        self.create_board()

    def create_board(self):
        for x in range(self.size):
            for y in range(self.size):
                button = tk.Button(self.master, width=2, height=1, font=('Arial', 14),
                                   command=lambda x=x, y=y: self.player_move(x, y))
                button.grid(row=x, column=y)
                self.buttons[x][y] = button

    def player_move(self, x, y):
        if self.board.is_empty(x, y):
            self.board.place_stone(x, y, 1)
            self.update_board()

            if self.board.check_win(1):
                self.show_message("You Win!")
                return

            self.master.after(500, self.ai_move)

    def ai_move(self):
        move = self.ai.find_best_move(self.board, 2)
        if move:
            x, y = move
            self.board.place_stone(x, y, 2)
            self.update_board()

            if self.board.check_win(2):
                self.show_message("AI Wins!")

    def update_board(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board.board[x, y] == 1:
                    self.buttons[x][y].config(
                        text="X", state="disabled", disabledforeground="blue")
                elif self.board.board[x, y] == 2:
                    self.buttons[x][y].config(
                        text="O", state="disabled", disabledforeground="red")

    def show_message(self, message):
        result = messagebox.showinfo("Game Over", message)
        if result == 'ok':
            self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuGUI(root, size=15)
    root.mainloop()
