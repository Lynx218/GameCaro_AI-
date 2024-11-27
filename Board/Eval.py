from .Cell import Cell

class EvalCell:
    def __init__(self, cell=None, value=0):
        if cell is None:
            cell = Cell()
        self.cell = cell
        self.value = value

    @classmethod
    def from_coordinates(cls, x, y, value):
        return cls(Cell(x, y), value)

    def get_cell(self):
        return self.cell

    def get_x(self):
        return self.cell.get_x()

    def get_y(self):
        return self.cell.get_y()

    def get_value(self):
        return self.value
