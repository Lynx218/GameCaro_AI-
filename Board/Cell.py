class Cell:
    def __init__(self, x, y, selected=0):
        self.x = x
        self.y = y
        self.selected = selected

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_selected(self):
        return self.selected

    def set_selected(self, selected):
        self.selected = selected

    def is_clickable(self):
        return self.selected == 0
