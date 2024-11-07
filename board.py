import numpy as np


class Board:
    def __init__(self, size=19):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)

    def is_empty(self, x, y):
        return self.board[x, y] == 0

    def place_stone(self, x, y, player):
        if self.is_empty(x, y):
            self.board[x, y] = player

    def remove_stone(self, x, y):
        self.board[x, y] = 0

    def get_possible_moves(self):
        possible_moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] == 0:
                    neighbors = [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2)
                                 if 0 <= x + dx < self.size and 0 <= y + dy < self.size]
                    if any(self.board[nx, ny] != 0 for nx, ny in neighbors):
                        possible_moves.append((x, y))
        return possible_moves

    def check_win(self, player):
        for x in range(self.size):
            for y in range(self.size - 4):
                if np.all(self.board[x, y:y+5] == player):
                    return True
                if np.all(self.board[y:y+5, x] == player):
                    return True

        for x in range(self.size - 4):
            for y in range(self.size - 4):
                if np.all(np.diagonal(self.board[x:x+5, y:y+5]) == player):
                    return True
                if np.all(np.diagonal(np.fliplr(self.board[x:x+5, y:y+5])) == player):
                    return True
        return False
