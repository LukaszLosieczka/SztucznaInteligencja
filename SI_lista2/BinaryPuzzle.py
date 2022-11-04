from BinaryConstraints import BinaryConstraints
from CSP import CSP, Method


class BinaryPuzzle:
    def __init__(self, file: str, n: int):
        self.file = 'binary-futoshiki_dane_v1/' + file
        self.n = n
        self.layout: {(int, int): int} = {}
        self.constraints = BinaryConstraints(n)
        self.__read_file()

    def get_solutions(self, method: Method = Method.BACKTRACKING):
        variables = [(i, j) for i in range(self.n) for j in range(self.n)]
        domains = dict((v, [0, 1]) for v in variables)
        connections = self.get_connections()
        csp = CSP(variables, domains, self.constraints, connections)
        solutions = []
        stats = {}
        if method == Method.BACKTRACKING:
            csp.backtracking(self.layout, solutions, stats)
        elif method == Method.FORWARD_CHECKING:
            csp.forward_checking(self.layout, solutions, stats)
        return solutions, stats

    def get_connections(self):
        connections = {}
        for x in range(self.n):
            for y in range(self.n):
                connections[(x, y)] = []
                for i in range(self.n):
                    if i != y:
                        connections[(x, y)].append((x, i))
                    if i != x:
                        connections[(x, y)].append((i, y))
        return connections

    def __read_file(self):
        f = open(self.file, "r")
        for i in range(self.n):
            row = f.readline()
            for j in range(len(row)):
                if row[j] != 'x' and row[j] != '\n':
                    self.layout[i, j] = int(row[j])
        f.close()
