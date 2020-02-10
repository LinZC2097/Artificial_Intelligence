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
        self.create_square_mat()
        if self.square_mat[current] == self.square_mat[end]:
            return 14.1
        # elif fabs(self.square_mat[current] % 10 - self.square_mat[end] % 10) == 1 \
        #         and (self.square_mat[current] // 10 == self.square_mat[end] // 10
        #         or fabs(self.square_mat[current] // 10 - self.square_mat[end] // 10) == 1):
        #     return 0
        else:
            height = fabs(self.square_mat[current] // 10 - self.square_mat[end] // 10) - 1
            weight = fabs(self.square_mat[current] % 10 - self.square_mat[end] % 10) - 1
            a = "%.2f" % sqrt((height * 10) ** 2 + (weight * 10) ** 2)

            return float(a)

    def shortest_path_astar(self, start: int, end: int) -> int:
        discovery = [None for _ in range(self.size)]
        discovery[start] = 0
        previous = [None for _ in range(self.size)]

        previous[start] = start
        frontier_heap = [(0, start)]
        next_vertex = heapq.heappop(frontier_heap)

        while next_vertex[1] != end:

            for val in self.adjacency_list[next_vertex[1]]:
                if discovery[val] is None:
                    discovery[val] = discovery[next_vertex[1]] + self.adjacency_list[next_vertex[1]][val]
                    previous[val] = next_vertex[1]
                    heapq.heappush(frontier_heap, (self.astar_hcost_function(val, end) + discovery[val], val))
            next_vertex = heapq.heappop(frontier_heap)

        return discovery[previous[next_vertex[1]]] + self.adjacency_list[previous[next_vertex[1]]][next_vertex[1]]


if __name__ == '__main__':
    print("hello world")
    print("------------------------")
    test = ShortestPath(100,
                        "/Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph100_0.1/v.txt",
                        "/Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph100_0.1/e.txt")

    test.create_cost_mat()
    test.create_square_mat()
    test.create_adjacency_list()
    # print(test.astar_hcost_function(20, 1))
    start = 1
    i = 0
    for end in range(2, 100):
        apsp = test.shortest_path_apsp(start, end)
        astar = test.shortest_path_astar(start, end)
        if apsp == astar:
            print(end, apsp, astar)
        else:
            print(end, apsp, astar, "!!!!!!!!!")
            i += 1
    print(i)
    # end = 5
    # print(test.shortest_path_apsp(start, end))
    # print(test.shortest_path_astar(start, end))



