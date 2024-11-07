import math
import numpy as np
from numba import njit
from board import Board

class GomokuAI:
    WIN_SCORE = 1_000_000

    def __init__(self, depth=2):  # Độ sâu tìm kiếm mặc định là 2 để cải thiện hiệu suất
        self.depth = depth

    @staticmethod
    @njit
    def heuristic_score(board, x, y, player, size, win_score):
        score = 0
        patterns = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in patterns:
            count = 1
            open_ends = 2

            for k in range(1, 5):
                nx, ny = x + dx * k, y + dy * k
                if 0 <= nx < size and 0 <= ny < size:
                    if board[nx, ny] == player:
                        count += 1
                    elif board[nx, ny] == 0:
                        break
                    else:
                        open_ends -= 1
                        break
                else:
                    open_ends -= 1
                    break

            for k in range(1, 5):
                nx, ny = x - dx * k, y - dy * k
                if 0 <= nx < size and 0 <= ny < size:
                    if board[nx, ny] == player:
                        count += 1
                    elif board[nx, ny] == 0:
                        break
                    else:
                        open_ends -= 1
                        break
                else:
                    open_ends -= 1
                    break

            if count >= 5:
                return win_score
            elif open_ends == 2:
                score += 10 ** (count + 1)
            elif open_ends == 1:
                score += 10 ** count

        return score

    def evaluate(self, board, player):
        opponent = 3 - player
        score = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x, y] == player:
                    score += self.heuristic_score(board.board, x, y, player, board.size, self.WIN_SCORE)
                elif board.board[x, y] == opponent:
                    score -= self.heuristic_score(board.board, x, y, opponent, board.size, self.WIN_SCORE)
        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player, player):
        if depth == 0 or board.check_win(player) or board.check_win(3 - player):
            return self.evaluate(board, player)

        if maximizing_player:
            max_eval = -math.inf
            for x, y in board.get_possible_moves():
                board.place_stone(x, y, player)
                eval = self.minimax(board, depth - 1, alpha, beta, False, player)
                board.remove_stone(x, y)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for x, y in board.get_possible_moves():
                board.place_stone(x, y, 3 - player)
                eval = self.minimax(board, depth - 1, alpha, beta, True, player)
                board.remove_stone(x, y)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, board, player):
        best_score = -math.inf
        best_move = None
        for x, y in board.get_possible_moves():
            board.place_stone(x, y, player)
            score = self.minimax(board, self.depth, -math.inf, math.inf, False, player)
            board.remove_stone(x, y)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move
