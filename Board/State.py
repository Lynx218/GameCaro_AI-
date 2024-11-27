from .Cell import Cell
from Constant import SIZE


class State:
    def __init__(self):
        self.size = SIZE
        self.cells = [[Cell(x, y) for y in range(SIZE)] for x in range(SIZE)]
        self.move_steps = []
        self.steps = 0

    def update(self, x, y, player):
        self.cells[x][y].set_selected(player)
        self.move_steps.append((x, y, player))
        self.steps += 1

    def get_cell(self, x, y):
        return self.cells[x][y]

    def get_state(self):
        return [[self.cells[x][y].get_selected() for y in range(self.size)] for x in range(self.size)]

    def set_state(self, new_cell_matrix):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].set_selected(new_cell_matrix[x][y])
        self.move_steps = [
            (x, y, self.cells[x][y].get_selected()) for x in range(self.size) for y in range(self.size) if self.cells[x][y].get_selected() != 0
        ]
        self.steps = sum(
            1 for row in new_cell_matrix for cell in row if cell != 0)

    def print_state(self):
        for row in self.get_state():
            print(" ".join("-" if cell == 2 else "+" if cell ==
                  1 else "0" for cell in row))

    def check_winner(self, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)
                      ]
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y].get_selected() == player:
                    for dx, dy in directions:
                        count = 1
                        for step in range(1, 5):
                            nx, ny = x + dx * step, y + dy * step
                            if 0 <= nx < self.size and 0 <= ny < self.size and self.cells[nx][ny].get_selected() == player:
                                count += 1
                            else:
                                break
                        if count == 5:
                            return True
        return False

    def is_clickable(self, x, y):
        return self.cells[x][y].is_clickable()

    def is_over(self):
        return self.steps == self.size * self.size

    def clone(self):
        new_state = State()
        for x in range(self.size):
            for y in range(self.size):
                new_cell = Cell(
                    x,
                    y,
                    self.cells[x][y].get_selected()
                )
                new_state.cells[x][y] = new_cell
        new_state.steps = self.steps
        new_state.move_steps = self.move_steps[:]
        return new_state
