from .Cell import Cell
from Constant import SIZE


class State:
    def __init__(self):
        """Khởi tạo trạng thái bàn cờ."""
        self.size = SIZE  # Kích thước bàn cờ
        self.cells = [[Cell(x, y) for y in range(SIZE)] for x in range(SIZE)]
        self.move_steps = []  # Danh sách các bước đã đi
        self.steps = 0  # Số ô đã đánh

    def update(self, x, y, player):
        """
        Cập nhật nước đi mới.
        :param x: Tọa độ x
        :param y: Tọa độ y
        :param player: Người chơi (1: User, 2: AI)
        """
        if self.cells[x][y].get_selected() == 0:  # Kiểm tra ô còn trống
            self.cells[x][y].set_selected(player)  # Cập nhật trạng thái ô
            self.move_steps.append((x, y, player))  # Lưu bước đi vào danh sách
            self.steps += 1  # Tăng số bước đã đi

    def get_cell(self, x, y):
        """Lấy đối tượng Cell tại tọa độ (x, y)."""
        return self.cells[x][y]

    def get_state(self):
        """Lấy trạng thái bàn cờ dưới dạng ma trận số."""
        return [[self.cells[x][y].get_selected() for y in range(self.size)] for x in range(self.size)]

    def set_state(self, new_cell_matrix):
        """
        Đặt lại trạng thái bàn cờ từ ma trận số.
        :param new_cell_matrix: Ma trận trạng thái mới
        """
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].set_selected(new_cell_matrix[x][y])
        self.move_steps = [
            (x, y, self.cells[x][y].get_selected()) for x in range(self.size) for y in range(self.size) if self.cells[x][y].get_selected() != 0
        ]
        self.steps = sum(
            1 for row in new_cell_matrix for cell in row if cell != 0)

    def print_state(self):
        """In trạng thái bàn cờ."""
        for row in self.get_state():
            print(" ".join("-" if cell == 2 else "+" if cell ==
                  1 else "0" for cell in row))

    def check_winner(self, player):
        """
        Kiểm tra người thắng cuộc.
        :param player: Người chơi cần kiểm tra (1 hoặc 2)
        :return: True nếu player thắng, False nếu không
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)
                      ]  # Hướng kiểm tra: ngang, dọc, chéo chính, chéo phụ
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y].get_selected() == player:  # Nếu ô thuộc về player
                    for dx, dy in directions:
                        count = 1
                        for step in range(1, 5):  # Kiểm tra 4 ô tiếp theo
                            nx, ny = x + dx * step, y + dy * step
                            if 0 <= nx < self.size and 0 <= ny < self.size and self.cells[nx][ny].get_selected() == player:
                                count += 1
                            else:
                                break
                        if count == 5:
                            self.winning_line = [(x + dx * i, y + dy * i) for i in range(count)]
                            return True
        return False

    def is_clickable(self, x, y):
        """
        Kiểm tra một ô có thể đánh được không.
        :param x: Tọa độ x
        :param y: Tọa độ y
        :return: True nếu ô trống, False nếu không
        """
        return self.cells[x][y].is_clickable()

    def is_over(self):
        """
        Kiểm tra bàn cờ đã đầy chưa.
        :return: True nếu đầy, False nếu còn ô trống
        """
        return self.steps == self.size * self.size

    def clone(self):
        """
    Tạo một bản sao của trạng thái bàn cờ.
    :return: Đối tượng State mới với trạng thái giống hệt.
    """
        new_state = State()
        for x in range(self.size):
            for y in range(self.size):
                new_cell = Cell(
                    x,
                    y,
                    # Sao chép giá trị selected chính xác
                    self.cells[x][y].get_selected()
                )
                new_state.cells[x][y] = new_cell
        new_state.steps = self.steps
        new_state.move_steps = self.move_steps[:]
        return new_state
