import re
import heapq
from Constant import SIZE, AI_VALUE, USER_VALUE, MAX_NUM_OF_HIGHEST_CELL_LIST
from Board.Eval import EvalCell
from Board.Cell import Cell


class Heuristic:
    def __init__(self):
        self.eval_state = [[0] * SIZE for _ in range(SIZE)]
        self.defense_score = [0, 1, 9, 81, 729, 6534]
        self.attack_score = [0, 3, 24, 192, 1536, 12288]
        self.case_user = [
            "11001", "10101", "10011",
            "00110", "01010", "01100",
            "11100", "11010", "10110", "01101", "01011", "00111",
            "01110",
            "011100", "011010", "010110", "001110", "1010101", "1011001", "1001101",
            "01111", "10111", "11011", "11101", "11101",  "11110",
            "11111"
        ]
        self.case_ai = [
            "22002", "20202", "20022",
            "00220", "02020", "02200",
            "22200", "22020", "20220", "02202", "02022", "00222",
            "02220",
            "022200", "022020", "020220", "002220", "2020202", "2022002", "2002202",
            "02222", "20222", "22022", "22202", "22202",  "22220",
            "22222"
        ]
        self.point = [
            4, 4, 4,
            8, 8, 8,
            8, 8, 8, 8, 8, 8,
            8,
            500, 500, 500, 500, 500, 500, 500,
            1000, 1000, 1000, 1000, 1000, 1000,
            100000
        ]

    def evaluate_state(self, state):
        """Lượng giá trạng thái bàn cờ."""
        rem = ";"
        cell = state.get_state()

        # Xử lý hàng và cột
        for i in range(SIZE):
            rem += "".join(map(str, cell[i])) + ";"
            rem += "".join(str(cell[j][i])
                           for j in range(SIZE)) + ";"

        # Xử lý đường chéo chính (\)
        for i in range(SIZE - 4):
            rem += "".join(str(cell[j][i + j])
                           for j in range(SIZE - i)) + ";"
        for i in range(1, SIZE - 4):
            rem += "".join(str(cell[i + j][j])
                           for j in range(SIZE - i)) + ";"

        # Xử lý đường chéo phụ (/)
        for i in range(4, SIZE):
            rem += "".join(str(cell[i - j][j])
                           for j in range(i + 1)) + ";"
        for i in range(1, SIZE - 4):
            rem += "".join(str(cell[j][i + SIZE - j - 1])
                           for j in range(i, SIZE)) + ";"

        total_score = 0
        for i in range(len(self.case_user)):
            total_score -= self.point[i] * \
                len(re.findall(self.case_user[i], rem))
            total_score += self.point[i] * \
                len(re.findall(self.case_ai[i], rem))

        return total_score

    def reset_eval_state(self):
        self.eval_state = [[0] * SIZE for _ in range(SIZE)]

    def evaluate_each_cell(self, state, player):
        """Lượng giá từng ô vuông trên bàn cờ."""
        self.reset_eval_state()
        cell = state.get_state()

        # Kiểm tra hàng ngang
        for x in range(SIZE):
            for y in range(SIZE - 4):
                self.evaluate_segment(cell, x, y, 0, 1, player)

        # Kiểm tra cột dọc
        for x in range(SIZE - 4):
            for y in range(SIZE):
                self.evaluate_segment(cell, x, y, 1, 0, player)

        # Kiểm tra đường chéo chính
        for x in range(SIZE - 4):
            for y in range(SIZE - 4):
                self.evaluate_segment(cell, x, y, 1, 1, player)

        # Kiểm tra đường chéo phụ
        for x in range(4, SIZE):
            for y in range(SIZE - 4):
                self.evaluate_segment(cell, x, y, -1, 1, player)

    def evaluate_segment(self, cell, x, y, dx, dy, player):
        """Lượng giá một đoạn 5 ô."""
        count_ai, count_user = 0, 0

        for i in range(5):
            nx, ny = x + i * dx, y + i * dy
            if cell[nx][ny] == AI_VALUE:
                count_ai += 1
            elif cell[nx][ny] == USER_VALUE:
                count_user += 1

        if count_ai * count_user == 0 and count_ai != count_user:
            for i in range(5):
                nx, ny = x + i * dx, y + i * dy
                if cell[nx][ny] == 0:
                    if count_ai == 0:
                        if player == AI_VALUE:
                            self.eval_state[nx][ny] += self.defense_score[count_user]
                        else:
                            self.eval_state[nx][ny] += self.attack_score[count_user]
                    elif count_user == 0:
                        if player == USER_VALUE:
                            self.eval_state[nx][ny] += self.defense_score[count_ai]
                        else:
                            self.eval_state[nx][ny] += self.attack_score[count_ai]

                    if count_ai == 4 or count_user == 4:
                        self.eval_state[nx][ny] *= 2

    def get_optimal_list(self):
        all_cells = [
            (self.eval_state[x][y], Cell(x, y))
            for x in range(SIZE)
            for y in range(SIZE)
            if self.eval_state[x][y] > 0
        ]

        top_cells = heapq.nlargest(
            MAX_NUM_OF_HIGHEST_CELL_LIST, all_cells, key=lambda x: x[0])

        max_value = top_cells[0][0] if top_cells else 0
        max_length = len(str(abs(max_value))) if max_value > 0 else 1
        difference = [0, 2, 8, 32, 128, 512]

        optimal_list = [
            EvalCell(cell, value)
            for value, cell in top_cells
            if max_value - value <= difference[max_length]
        ]

        return optimal_list

    def print_eval_state(self):
        """In bảng lượng giá eval_state."""
        print("Eval State:")
        for row in self.eval_state:
            # Căn chỉnh giá trị cho đẹp
            print(" ".join(f"{value:4}" for value in row))
