import copy


class ShortestPath:
    def __init__(self, size, file_v_adds, file_e_adds):
        self.size = size
        self.file_v_adds = file_v_adds
        self.file_e_adds = file_e_adds
        self.cost_mat = [[float('Inf') for j in range(size)] for i in range(size)]
        self.square_mat = []
        self.apsp_mat = []
        self.a_star_mat = []

    def read_file(self, adds) -> list:
        with open(adds, "r") as file:
            temp = ''
            for curline in file:
                if curline.startswith("# "):
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

    def a_star(self) -> dict:
        pass

    def shortest_path_apsp(self, i, j) -> int:
        self.apsp()
        return self.apsp_mat[i][j]

    def shortest_path_astar(self, i, j) -> int:
        pass

if __name__ == '__main__':
    print("hello world")
    test = ShortestPath(100,
                        "/Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph100_0.2/v.txt",
                        "/Users/marsscho/Desktop/6511 Artificial Intelligence/Project/Project 1/graphs/graph100_0.2/e.txt")

    test.create_cost_mat()
    test.create_square_mat()

    print(test.shortest_path_apsp(1, 1))

