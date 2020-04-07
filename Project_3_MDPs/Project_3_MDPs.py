import copy
from time import time


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
        self.new_grid = [[] for i in range(grid_width)]
        self.grid_initial(vals)

    def grid_initial(self, vals: list):
        for i in range(self.width):
            for j in range(self.width):
                if vals[i][j] is not None:
                    self.grid[i].append(Node(vals[i][j], 1))
                    self.new_grid[i].append(Node(vals[i][j], 1))
                else:
                    self.grid[i].append(Node(0, 0))
                    self.new_grid[i].append(Node(0, 0))

    def show(self):
        print("gamma:", self.gamma)
        print("noise:")
        for val in self.noise:
            print(val, end=" ")
        print()
        print("grid:")
        for row in self.grid:
            for val in row:
                print(val.val, end="\t\t\t")
            print()

    def is_equal_value(self) -> bool:
        for i in range(self.width):
            for j in range(self.width):
                if self.grid[i][j].val != self.new_grid[i][j].val:
                    return False
        return True

    def is_equal_policy(self) -> bool:
        for i in range(self.width):
            for j in range(self.width):
                if self.grid[i][j].action != self.new_grid[i][j].action:
                    return False
        return True

    def get_value(self, x: int, y: int, action: int, grid: list) -> float:
        axis = [
            [max(x - 1, 0), y],
            [min(x + 1, self.width - 1), y],
            [x, max(y - 1, 0)],
            [x, min(y + 1, self.width - 1)]
        ]
        value = 0

        if action % 2 == 0:
            value += self.noise[0] * (self.reward + self.gamma * grid[axis[action][1]][axis[action][0]].val)
            value += self.noise[1] * (
                    self.reward + self.gamma * grid[axis[(action + 2) % 4][1]][axis[(action + 2) % 4][0]].val)
            value += self.noise[2] * (
                    self.reward + self.gamma * grid[axis[(action + 3) % 4][1]][axis[(action + 3) % 4][0]].val)
            value += self.noise[3] * (
                    self.reward + self.gamma * grid[axis[action + 1][1]][axis[action + 1][0]].val)
        else:
            value += self.noise[0] * (self.reward + self.gamma * grid[axis[action][1]][axis[action][0]].val)
            value += self.noise[1] * (
                    self.reward + self.gamma * grid[axis[(action + 2) % 4][1]][axis[(action + 2) % 4][0]].val)
            value += self.noise[2] * (
                    self.reward + self.gamma * grid[axis[(action + 1) % 4][1]][axis[(action + 1) % 4][0]].val)
            value += self.noise[3] * (
                    self.reward + self.gamma * grid[axis[action - 1][1]][axis[action - 1][0]].val)
        return round(value, 4)

    def update_max_value(self, x: int, y: int):
        max_action = 0
        max_value = float("-inf")
        for action in range(4):
            value = self.get_value(x, y, action, self.grid)
            if max_value < value:
                max_value = value
                max_action = action
        self.new_grid[y][x].val = max_value
        self.new_grid[y][x].action = max_action

    def value_iteration(self):
        i = 0
        while True:
            i += 1
            for y in range(self.width):
                for x in range(self.width):
                    if not self.grid[y][x].state:
                        self.update_max_value(x, y)
            if self.is_equal_value():
                break
            self.grid = copy.deepcopy(self.new_grid)

        self.show()
        print("iteration times: ", i)

    def update_action(self, x: int, y: int):
        max_action = 0
        max_value = float("-inf")
        for action in range(4):
            value = self.get_value(x, y, action, self.new_grid)
            if max_value < value:
                max_value = value
                max_action = action
        self.new_grid[y][x].action = max_action

    def policy_iteration(self):
        i = 0
        while True:
            i += 1
            for y in range(self.width):
                for x in range(self.width):
                    if not self.grid[y][x].state:
                        self.new_grid[y][x].val = self.get_value(x, y, self.grid[y][x].action, self.grid)
            for y in range(self.width):
                for x in range(self.width):
                    if not self.new_grid[y][x].state:
                        self.update_action(x, y)
            if self.is_equal_value():
                break
            self.grid = copy.deepcopy(self.new_grid)
        self.show()
        print("iteration times: ", i)


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
    noise = [0.8, 0.1, 0.1, 0]

    # policy iteration
    start_time = time()
    testGrid = Grid(7, 0.9, noise, grid)
    testGrid.update_max_value(2, 4)
    print(testGrid.grid[4][2].val, testGrid.grid[4][2].action)

    testGrid.show()
    testGrid.policy_iteration()
    print("policy iteration runtime: %.4f s" % (time() - start_time))

    # value iteration
    start_time = time()
    testGrid = Grid(7, 0.9, noise, grid)
    testGrid.update_max_value(2, 4)
    print(testGrid.grid[4][2].val, testGrid.grid[4][2].action)

    testGrid.show()
    testGrid.value_iteration()
    print("value iteration runtime: %.4f s" % (time() - start_time))


if __name__ == '__main__':
    main()
