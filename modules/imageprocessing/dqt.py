class DQT:
    """
    DQT table class, fills table by zig-zag order
    """
    def __init__(self, table_string):
        self.height = 8
        self.width = 8
        self.matrix = [[None for x in range(self.width)] for y in range(self.height)]
        self.fill_zig_zag(table_string)

    def fill_zig_zag(self, table_string):
        """
        fills matrix with zig-zag order
        :param table_string: - is string with table items
        """
        iter = self.byte_generator(table_string)
        x, y, direction = 0, 0, -1
        self.matrix[0][0] = iter.__next__()
        for i in iter:
            x, y, direction = self.get_cell(x, y, direction)
            self.matrix[x][y] = i

    def byte_generator(self, table_string):
        """
        generator returning 2 bytes from string
        """
        for i in range(0, len(table_string), 2):
            yield table_string[i:i+2]

    def get_cell(self, x, y, direction):
        """
        calculates next coordinate. Based on zig-zag order
        if direction == 1 pointer goes down-left
        elif direction == -1 pointer goes up-right
        :return: x, y, order direction
        """
        if x == 0 and direction == -1 and y < self.width:
            y += 1
            direction = 1
        elif x == self.height-1 and direction == 1:
            y += 1
            direction = -1
        elif y == 0 and direction == 1 and x < self.height:
            x += 1
            direction = -1
        elif y == self.width - 1 and direction == -1:
            x += 1
            direction = 1
        elif direction == 1:
            y += -1
            x += 1
        elif direction == -1:
            y += 1
            x += -1
        return x, y, direction

