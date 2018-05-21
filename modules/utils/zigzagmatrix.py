class ZigZagMatrix:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.matrix = [[0 for x in range(self.width)] for y in range(self.height)]
        self.x = 0
        self.y = 0
        self.direction = -1

    def set(self, x, y, value):
        self.matrix[x][y] = value

    def get(self, x, y):
        return self.matrix[x][y]

    def put(self, value):
        self.set(self.x, self.y, value)
        self.x, self.y, self.direction = self.get_cell(self.x, self.y, self.direction)

    def print_matrix(self):
        print('*' * 15)
        for row in self.matrix:
            print(row)

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
