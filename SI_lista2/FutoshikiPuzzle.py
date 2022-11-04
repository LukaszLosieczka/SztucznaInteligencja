from FutoshikiConstraints import FutoshikiConstraints, Inequality
from CSP import CSP, Method
import time


class FutoshikiPuzzle:
    def __init__(self, file: str, n: int):
        self.file = 'binary-futoshiki_dane_v1/' + file
        self.n = n
        self.layout: {(int, int): int} = {}
        self.constraints = FutoshikiConstraints(n)
        # wczytaj dane
        self.__read_file()

    def get_solutions(self, method: Method = Method.BACKTRACKING):
        variables = [(i, j) for i in range(self.n) for j in range(self.n)]
        domains = dict((v, list(range(1, self.n + 1))) for v in variables)
        connections = self.get_connections()
        solutions = []
        csp = CSP(variables, domains, self.constraints, connections)
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
        ii = -1
        for i in range(self.n + (self.n - 1)):
            if i % 2 == 0:
                ii += 1
            row = f.readline()
            jj = -1
            row_range = self.n + (self.n - 1)
            if i % 2 != 0:
                row_range = self.n
            for j in range(row_range):
                if j % 2 == 0 or i % 2 != 0:
                    jj += 1
                # ograniczenia miedzy rzedami
                if i % 2 != 0 and row[j] != '-':
                    self.constraints.inequalities[ii, jj].append(Inequality((ii, jj), (ii+1, jj), row[j]))
                    self.constraints.inequalities[ii+1, jj].append(Inequality((ii, jj), (ii+1, jj), row[j]))
                # ograniczenia między kolumnami
                elif j % 2 != 0 and row[j] != '-':
                    self.constraints.inequalities[ii, jj].append(Inequality((ii, jj), (ii, jj+1), row[j]))
                    self.constraints.inequalities[ii, jj+1].append(Inequality((ii, jj), (ii, jj+1), row[j]))
                # stale wartosci
                elif row[j] != 'x' and row[j] != '\n' and row[j] != '-':
                    self.layout[ii, jj] = int(row[j])
        f.close()
