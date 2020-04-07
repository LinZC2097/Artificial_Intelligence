import copy
import csv
import heapq
from math import sqrt, fabs
from time import time

from Project_1_Search.Priority_Queue import PQ


class ShortestPath:
    def __init__(self, file_v_adds: str, file_e_adds: str):
        # self.size = size
        self.file_v_adds = file_v_adds
        self.file_e_adds = file_e_adds
        # self.cost_mat = [[float('Inf') for j in range(size)] for i in range(size)]
        self.cost_mat = []
        self.square_mat = []
        self.apsp_mat = []
        # self.adjacency_list = [{} for _ in range(size)]
        self.adjacency_list = []
        self.create_square_mat()
        self.create_cost_mat()
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
        self.cost_mat = [[float('Inf') for j in range(self.size)] for i in range(self.size)]
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
        self.size = len(reader)
        for val in reader:
            self.square_mat.append(int(val.split(",")[1]))

    def create_adjacency_list(self):
        self.adjacency_list = [{} for _ in range(self.size)]
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

    def shortest_path_astar(self, start: int, end: int):
        start_time = time()
        path = []
        frontier_heap = []
        step = 0

        previous = {}
        previous[start] = start

        g_cost = [float('Inf') for _ in range(self.size)]

        heapq.heappush(frontier_heap, (0, start))
        g_cost[start] = 0

        next_vertex = heapq.heappop(frontier_heap)

        while next_vertex[1] != end:
            for successor in self.adjacency_list[next_vertex[1]]:
                if g_cost[successor] > g_cost[next_vertex[1]] + self.adjacency_list[next_vertex[1]][successor]:
                    g_cost[successor] = g_cost[next_vertex[1]] + self.adjacency_list[next_vertex[1]][successor]
                    previous[successor] = next_vertex[1]
                    heapq.heappush(frontier_heap,
                                   (g_cost[successor] + self.astar_hcost_function(successor, end), successor))
            next_vertex = heapq.heappop(frontier_heap)
            step += 1

        next = end
        while next != start:
            path.append(next)
            next = previous[next]
        path.append(start)

        result = [path, step, start_time, g_cost[next_vertex[1]]]
        self.show_result(start, end, result, "A*")

        return result

    def shortest_path_dijkstra(self, start: int, end: int):
        start_time = time()
        step = 0

        previous = {}
        previous[start] = start

        distance = [float("Inf") for i in range(self.size)]
        distance[start] = 0

        discovery = [0 for i in range(self.size)]
        discovery[start] = 1

        next_vertex = start
        pq = PQ()

        while next_vertex != end:
            for val in self.adjacency_list[next_vertex]:
                if distance[val] > distance[next_vertex] + self.adjacency_list[next_vertex][val]:
                    distance[val] = distance[next_vertex] + self.adjacency_list[next_vertex][val]
                    previous[val] = next_vertex
                    pq.add_task(val, distance[val])
            next_vertex = pq.pop_task()[0]
            discovery[next_vertex] = 1
            step += 1

        # while next_vertex != end:
        #     for val in self.adjacency_list[next_vertex]:
        #         if distance[val] > distance[next_vertex] + self.adjacency_list[next_vertex][val]:
        #             distance[val] = distance[next_vertex] + self.adjacency_list[next_vertex][val]
        #             previous[val] = next_vertex
        #         if not discovery[val] and val not in frontiers:
        #             frontiers.append(val)
        #     pq = []
        #     for frontier in frontiers:
        #         heapq.heappush(pq, (distance[frontier], frontier))
        #     next_vertex = heapq.heappop(pq)[1]
        #     frontiers.remove(next_vertex)
        #     discovery[next_vertex] = 1
        #     step += 1

        path = []
        next = end
        while next != start:
            path.append(next)
            next = previous[next]
        path.append(start)

        result = [path, step, start_time, distance[end]]
        self.show_result(start, end, result, "Dijkstra")

        return result

    def show_result(self, start: int, end: int, result: list, type: str):
        print("path:")
        for i in range(len(result[0]) - 1, 0, -1):
            print(result[0][i], end=" -> ")
        print(result[0][0])
        # result[0] = path
        print("number of step: ", result[1])
        # result[1] = step
        result[2] = round(time() - result[2], 6)
        # result[2] = start_time
        print("runtime of %s: %.6f" % (type, result[2]))
        # result[3] = distance
        print("distance from %d to %d: %d" % (start, end, result[3]))

    def run(self, start, end):
        print("A* Search:")
        self.shortest_path_astar(start, end)
        print("\nDijstra Search:")
        self.shortest_path_dijkstra(start, end)


def main():
    file = input("input the file index(format example: 100_0.1):")
    start = int(input("input the index of start point:"))
    end = int(input("input the index of end point:"))
    test = ShortestPath(
        "./graphs/graph" + file + "/v.txt",
        "./graphs/graph" + file + "/e.txt")

    test.run(start, end)



if __name__ == '__main__':
    main()
