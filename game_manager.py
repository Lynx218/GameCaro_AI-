from board import Board
from gomoku_ai import GomokuAI


class GameManager:
    def __init__(self):
        self.board = Board()
        self.ai = GomokuAI(depth=3)

    def play_game(self):
        current_player = 1  # 1 for human, 2 for AI
        while True:
            if current_player == 1:
                print("Human's turn.")
                x, y = map(int, input("Enter your move (row col): ").split())
            else:
                print("AI's turn.")
                x, y = self.ai.find_best_move(self.board, current_player)
            self.board.place_stone(x, y, current_player)
            self.print_board()
            if self.board.check_win(current_player):
                print("Player", current_player, "wins!")
                break
            current_player = 3 - current_player

    def print_board(self):
        for row in self.board.board:
            print(" ".join(str(x) for x in row))
        print()
