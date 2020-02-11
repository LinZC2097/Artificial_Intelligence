import copy
import heapq
from math import sqrt, fabs


class ShortestPath:
    def __init__(self, size: int, file_v_adds: str, file_e_adds: str):
        self.size = size
        self.file_v_adds = file_v_adds
        self.file_e_adds = file_e_adds
        self.cost_mat = [[float('Inf') for j in range(size)] for i in range(size)]
        self.square_mat = []
        self.apsp_mat = []
        self.adjacency_list = [{} for _ in range(size)]

    def read_file(self, adds: str) -> list:
        with open(adds, "r") as file:
            temp = ''
            for curline in file:
                if not curline.startswith("0"):
                    continue
                else:
                    temp = curline
                    break
            reader = file.readlines()
            reader.insert(0, temp)
        return reader

    def create_cost_mat(self) -> list:
        reader = self.read_file(self.file_e_adds)
        assert not reader[0].startswith("#")
        for val in reader:
            vertex = []
            for i in val.split(","):
                vertex.append(int(i))
            self.cost_mat[vertex[0]][vertex[1]] = vertex[2]
            self.cost_mat[vertex[1]][vertex[0]] = vertex[2]
        for i in range(self.size):
            self.cost_mat[i][i] = 0

    def create_square_mat(self) -> list:
        reader = self.read_file(self.file_v_adds)
        for val in reader:
            self.square_mat.append(int(val.split(",")[1]))

    def apsp(self) -> list:
        self.apsp_mat = copy.deepcopy(self.cost_mat)
        for k in range(self.size):
            for i in range(self.size):
                for j in range(self.size):
                    self.apsp_mat[i][j] = min(self.apsp_mat[i][k] + self.apsp_mat[k][j], self.apsp_mat[i][j])

    def shortest_path_apsp(self, start: int, end: int) -> int:
        self.apsp()
        return self.apsp_mat[start][end]

    def create_adjacency_list(self) -> list:
        reader = self.read_file(self.file_e_adds)
        for val in reader:
            vertex = []
            for i in val.split(","):
                vertex.append(int(i))

            self.adjacency_list[vertex[0]][vertex[1]] = vertex[2]
            self.adjacency_list[vertex[1]][vertex[0]] = vertex[2]

    def astar_hcost_function(self, current: int, end: int) -> float:
        if self.square_mat[current] == self.square_mat[end]:
            return 0
        else:
            height = fabs(self.square_mat[current] // 10 - self.square_mat[end] // 10)
            width = fabs(self.square_mat[current] % 10 - self.square_mat[end] % 10)
            if height > 0:
                height -= 1
            if width > 0:
                width -= 1
            result = "%.2f" % sqrt((height * 10) ** 2 + (width * 10) ** 2)
            return float(result)

    def shortest_path_astar(self, start: int, end: int) -> int:
        self.create_adjacency_list()

        frontier_heap = []
        g_cost = [float('Inf') for _ in range(self.size)]

        heapq.heappush(frontier_heap, (0, start))
        g_cost[start] = 0

        next_vertex = heapq.heappop(frontier_heap)

        while next_vertex[1] != end:
            for successor in self.adjacency_list[next_vertex[1]]:
                if g_cost[successor] > g_cost[next_vertex[1]] + self.adjacency_list[next_vertex[1]][successor]:
                    g_cost[successor] = g_cost[next_vertex[1]] + self.adjacency_list[next_vertex[1]][successor]
                    heapq.heappush(frontier_heap, (g_cost[successor] + self.astar_hcost_function(successor, end), successor))
            next_vertex = heapq.heappop(frontier_heap)

        return g_cost[next_vertex[1]]




if __name__ == '__main__':
    print("hello world")
    print("------------------------")
    test = ShortestPath(100,
                        "/Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph100_0.1/v.txt",
                        "/Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph100_0.1/e.txt")

    test.create_cost_mat()
    test.create_square_mat()

    start = 2
    i = 0

    for end in range(0, 100):
        apsp = test.shortest_path_apsp(start, end)
        astar = test.shortest_path_astar(start, end)
        if apsp == astar:
            print(end, apsp, astar)
        else:
            print(end, apsp, astar, "!!!!!!!!!")
            i += 1
    print(i)

    end = 5
    print(test.shortest_path_apsp(start, end))
    print(test.shortest_path_astar(start, end))
    # i = 0
    # for val in test.adjacency_list:
    #     print(i, val)
    #     i += 1
    # print(test.adjacency_list[0])
    # for val in test.adjacency_list[0]:
    #     print(val, end=" ")
    #     print(test.adjacency_list[0][val])

