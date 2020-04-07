class Node():
    def __init__(self, val: int, state: int, action: int = 1):
        self.val = val
        self.state = state
        # 1 is fixed
        # 0 is blank
        self.action = action
        # action:
        # 0 is left
        # 1 is right
        # 2 is up
        # 3 is down


class Grid():
    def __init__(self, grid_width: int, gamma: float, noise: list, vals: list, reward: int = 0):
        self.width = grid_width
        self.gamma = gamma
        self.noise = noise
    self.reward = reward
        self.grid = [[] for i in range(grid_width)]
        self.grid_initial(vals)

    def grid_initial(self, vals: list):
        for i in range(self.width):
            for j in range(self.width):
                if vals[i][j] is not None:
                    self.grid[i].append(Node(vals[i][j], 1))
                else:
                    self.grid[i].append(Node(0, 0))

    def show(self):
        print("gamma:", self.gamma)
        print("noise:")
        for val in self.noise:
            print(val, end=" ")
        print()
        print("grid:")
        for row in self.grid:
            for val in row:
                print(val.action, end="\t\t\t")
            print()

    def get_value(self, x: int, y: int, action: int) -> float:
        axis = [
            [max(x - 1, 0), y],
            [min(x + 1, self.width - 1), y],
            [x, max(y - 1, 0)],
            [x, min(x + 1, self.width - 1)]
        ]
        value = 0

        if action % 2 == 0:
            value += self.noise[0] * (self.reward + self.gamma * self.grid[axis[action][1]][axis[action][0]].val)
            value += self.noise[1] * (self.reward + self.gamma * self.grid[axis[(action + 2) % 4][1]][axis[(action + 2) % 4][0]].val)
            value += self.noise[2] * (self.reward + self.gamma * self.grid[axis[(action + 3) % 4][1]][axis[(action + 3) % 4][0]].val)
            value += self.noise[3] * (self.reward + self.gamma * self.grid[axis[action + 1][1]][axis[action + 1][0]].val)
        else:
            value += self.noise[0] * (self.reward + self.gamma * self.grid[axis[action][1]][axis[action][0]].val)
            value += self.noise[1] * (self.reward + self.gamma * self.grid[axis[(action + 2) % 4][1]][axis[(action + 2) % 4][0]].val)
            value += self.noise[2] * (self.reward + self.gamma * self.grid[axis[(action + 1) % 4][1]][axis[(action + 1) % 4][0]].val)
            value += self.noise[3] * (self.reward + self.gamma * self.grid[axis[action - 1][1]][axis[action - 1][0]].val)
        return value

    def update_max_value(self, x: int, y: int) -> int:
        max_action = 0
        max_value = float("-inf")
        for action in range(4):
            value = self.get_value(x, y, action)
            if max_value < value:
                max_value = value
                max_action = action
        self.grid[y][x].val = max_value
        self.grid[y][x].action = max_action


        pass

    def value_iteration(self):
        pass

    def argmax_action(self):
        pass

    def policy_iteration(self):
        pass


def main():
    print("hello world")
    grid = [
        [None, None, None, 1, None, None, None],
        [None, None, None, -1, None, 1, None],
        [- 1, None, None, -1, None, 4, None],
        [None, 1, None, -1, None, 1, None],
        [None, 100, None, -100, None, 3, None],
        [None, 2, None, -1, None, 3, None],
        [0, None, None, -1, None, 1, None]
    ]

    noise = [0.8, 0.1, 0.1]
    testGrid = Grid(7, 0.9, noise, grid)
    testGrid.show()


if __name__ == '__main__':
    main()
