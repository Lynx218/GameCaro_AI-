import random
from .Heuristic import Heuristic
from Board.State import State
from Constant import SIZE, AI_VALUE, MAX_DEPTH, USER_VALUE


class CaroAI:
    def __init__(self, mode):
        self.rand = random.Random()
        self.mode = mode
        self.heuristic = Heuristic()

        if self.mode == 1:
            self.root = State()
            center = SIZE // 2
            self.root.update(center, center, AI_VALUE)
            self.next_x = center
            self.next_y = center
        else:
            self.root = State()
            self.next_x = None
            self.next_y = None

    def get_next_x(self):
        return self.next_x

    def get_next_y(self):
        return self.next_y

    def check_winner(self, player):
        return self.root.check_winner(player)

    def update(self, x, y, value):
        self.root.update(x, y, value)

    def is_clickable(self, x, y):
        return self.root.is_clickable(x, y)

    def is_over(self):
        return self.root.is_over()

    def next_step(self):
        choice = self.alpha_beta(self.root)
        if not choice:
            print("~ Lỗi! Không tìm thấy nước đi!")
        else:
            self.next_x, self.next_y = choice.get_x(), choice.get_y()
            print(f"=> Nước đi của AI: {self.next_x} {self.next_y}")
            if not self.is_clickable(self.next_x, self.next_y):
                print("~ Lỗi! nước đi bị trùng!")
            else:
                self.update(self.next_x, self.next_y, AI_VALUE)

    def alpha_beta(self, state):
        rem_state = state.clone()
        self.heuristic.evaluate_each_cell(rem_state, AI_VALUE)
        optimal_list = self.heuristic.get_optimal_list()

        max_value = float("-inf")
        list_choose = []

        for cell in optimal_list:
            x, y = cell.get_x(), cell.get_y()
            rem_state.update(x, y, AI_VALUE)
            value = self.min_value(rem_state, float("-inf"), float("inf"), 0)
            print("Lượng giá của nước đi {}, {} là {}".format(x, y, value))
            if value > max_value:
                max_value = value
                list_choose.clear()
                list_choose.append(cell)
            elif value == max_value:
                list_choose.append(cell)
            rem_state.update(x, y, 0)

        if list_choose:
            return self.rand.choice(list_choose)
        return None

    def max_value(self, state, alpha, beta, depth):
        if depth >= MAX_DEPTH or state.check_winner(AI_VALUE) or state.is_over():
            return self.heuristic.evaluate_state(state)

        self.heuristic.evaluate_each_cell(state, AI_VALUE)
        optimal_list = self.heuristic.get_optimal_list()

        for cell in optimal_list:
            x, y = cell.get_x(), cell.get_y()
            state.update(x, y, AI_VALUE)
            alpha = max(alpha, self.min_value(state, alpha, beta, depth + 1))
            state.update(x, y, 0)
            if alpha >= beta:
                break
        return alpha

    def min_value(self, state, alpha, beta, depth):
        if depth >= MAX_DEPTH or state.check_winner(USER_VALUE) or state.is_over():
            return self.heuristic.evaluate_state(state)

        self.heuristic.evaluate_each_cell(state, USER_VALUE)
        optimal_list = self.heuristic.get_optimal_list()

        for cell in optimal_list:
            x, y = cell.get_x(), cell.get_y()
            state.update(x, y, USER_VALUE)
            beta = min(beta, self.max_value(state, alpha, beta, depth + 1))
            state.update(x, y, 0)
            if alpha >= beta:
                break
        return beta
