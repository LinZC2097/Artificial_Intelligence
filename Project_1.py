import copy
import heapq
from math import sqrt, fabs
from time import time


class ShortestPath:
    def __init__(self, size: int, file_v_adds: str, file_e_adds: str):
        self.size = size
        self.file_v_adds = file_v_adds
        self.file_e_adds = file_e_adds
        self.cost_mat = [[float('Inf') for j in range(size)] for i in range(size)]
        self.square_mat = []
        self.apsp_mat = []
        self.adjacency_list = [{} for _ in range(size)]
        self.create_cost_mat()
        self.create_square_mat()
        self.create_adjacency_list()

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

    def create_cost_mat(self):
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

    def create_square_mat(self):
        reader = self.read_file(self.file_v_adds)
        for val in reader:
            self.square_mat.append(int(val.split(",")[1]))

    def create_adjacency_list(self):
        reader = self.read_file(self.file_e_adds)
        for val in reader:
            vertex = []
            for i in val.split(","):
                vertex.append(int(i))

            self.adjacency_list[vertex[0]][vertex[1]] = vertex[2]
            self.adjacency_list[vertex[1]][vertex[0]] = vertex[2]

    def apsp(self):
        self.apsp_mat = copy.deepcopy(self.cost_mat)
        for k in range(self.size):
            for i in range(self.size):
                for j in range(self.size):
                    self.apsp_mat[i][j] = min(self.apsp_mat[i][k] + self.apsp_mat[k][j], self.apsp_mat[i][j])

    def shortest_path_apsp(self, start: int, end: int) -> int:

        self.apsp()
        return self.apsp_mat[start][end]

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
        path = []
        previous = {}
        frontier_heap = []
        previous[start] = start
        g_cost = [float('Inf') for _ in range(self.size)]

        heapq.heappush(frontier_heap, (0, start))
        g_cost[start] = 0

        next_vertex = heapq.heappop(frontier_heap)
        path.append(next_vertex[1])

        while next_vertex[1] != end:
            for successor in self.adjacency_list[next_vertex[1]]:
                if g_cost[successor] > g_cost[next_vertex[1]] + self.adjacency_list[next_vertex[1]][successor]:
                    g_cost[successor] = g_cost[next_vertex[1]] + self.adjacency_list[next_vertex[1]][successor]
                    previous[successor] = next_vertex[1]
                    heapq.heappush(frontier_heap,
                                   (g_cost[successor] + self.astar_hcost_function(successor, end), successor))
            next_vertex = heapq.heappop(frontier_heap)

        next = end
        while next != start:
            path.append(next)
            next = previous[next]
        path.append(start)
        for i in range(len(path) - 1, 1, -1):
            print(path[i], end=" -> ")
        print(path[1])


        return g_cost[next_vertex[1]]

    def shortest_path_dijkstra(self, start: int, end: int):
        previous = {}
        distance = [float("Inf") for i in range(self.size)]
        previous[start] = start
        distance[start] = 0
        discovery = [0 for i in range(self.size)]
        frontiers = []
        next_vertex = start
        discovery[start] = 1
        while next_vertex != end:
            for val in self.adjacency_list[next_vertex]:
                if distance[val] > distance[next_vertex] + self.adjacency_list[next_vertex][val]:
                    distance[val] = distance[next_vertex] + self.adjacency_list[next_vertex][val]
                    previous[val] = next_vertex
                if not discovery[val] and val not in frontiers:
                    frontiers.append(val)
            heap = []
            for frontier in frontiers:
                heapq.heappush(heap, (distance[frontier], frontier))
            next_vertex = heapq.heappop(heap)[1]
            frontiers.remove(next_vertex)
            discovery[next_vertex] = 1
        path = []
        next = end
        while next != start:
            path.append(next)
            next = previous[next]
        path.append(start)

        for i in range(len(path) - 1, 0, -1):
            print(path[i], end=" -> ")
        print(path[0])
        return distance[end]


def main():
    # /Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph200_0.2/v.txt
    # v_address = input("input the vertex file path in your computer: ")
    # print(v_address)

    # /Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph200_0.2/e.txt
    # e_address = input("input the edge file path in your computer: ")
    # print(e_address)

    # test = ShortestPath(500, v_address, e_address)
    test = ShortestPath(100,
                        "/Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph100_0.2/v.txt",
                        "/Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph100_0.2/e.txt")

    # start_time = time()
    # print(test.shortest_path_apsp(1, 2))
    # print("apsp: ", time() - start_time)
    for i in range(10):
        print(test.shortest_path_astar(5, i))
        print(test.shortest_path_dijkstra(5, i))
    # start_time = time()
    # for start in range(100):
    #     for end in range(100):
    #         test.shortest_path_astar(start, end)
    # print("astar: ", time() - start_time)


if __name__ == '__main__':
    main()
