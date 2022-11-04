import time
from enum import Enum


class Constraints:
    def check_constraints(self, layout, place) -> bool:
        pass

    def get_number_of_constraints(self, place):
        pass


class Method(Enum):
    BACKTRACKING = 'backtracking'
    FORWARD_CHECKING = 'forward_checking'


class CSP:
    def __init__(self, variables, domains, constraints: Constraints, connections):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.connections = connections

    def variables_heuristic(self):
        self.variables.sort(key=lambda x: self.constraints.get_number_of_constraints(x), reverse=True)

    def values_heuristic(self, layout, domains, variable):
        domain_occurrences = {}
        for value in domains[variable]:
            occurrences = 0
            for var in self.connections[variable]:
                if var in layout.keys() and layout[var] == value:
                    occurrences += 1
            domain_occurrences[value] = occurrences
        domains[variable].sort(key=lambda x: domain_occurrences[x])

    def check_domains(self, variable, layout, domains):
        unused_vars = [v for v in self.variables if v not in layout.keys()]
        for var in self.connections[variable]:
            local_layout = layout.copy()
            if var in unused_vars:
                new_domain = []
                for value in domains[var]:
                    local_layout[var] = value
                    if self.constraints.check_constraints(local_layout, var):
                        new_domain.append(value)
                if len(new_domain) == 0:
                    return False
                domains[var] = new_domain
        return True

    def check_all_domains(self, layout, domains):
        unused_vars = [v for v in self.variables if v not in layout.keys()]
        for var in unused_vars:
            local_layout = layout.copy()
            new_domain = []
            for value in domains[var]:
                local_layout[var] = value
                if self.constraints.check_constraints(local_layout, var):
                    new_domain.append(value)
            if len(new_domain) == 0:
                return False
            domains[var] = new_domain
        return True

    def backtracking(self, layout, solutions, stats: dict):
        start_time = time.time()
        nodes_count = [0]
        returns_count = [0]
        self.variables_heuristic()
        self.__backtracking(layout, solutions, start_time, returns_count, nodes_count, stats)
        stats['all_solutions_time'] = time.time()-start_time
        stats['all_solutions_returns'] = returns_count[0]
        stats['all_solutions_nodes'] = nodes_count[0]

    def __backtracking(self, layout, solutions, start_time, returns_count, nodes_count, stats: dict):
        if len(layout) == len(self.variables):
            if len(solutions) == 0:
                stats['first_solution_time'] = time.time() - start_time
                stats['first_solution_returns'] = returns_count[0]
                stats['first_solution_nodes'] = nodes_count[0]
            solutions.append(layout)
            returns_count[0] += 1
            return
        unused_var = [v for v in self.variables if v not in layout.keys()][0]
        local_layout = layout.copy()
        self.values_heuristic(local_layout, self.domains, unused_var)
        for value in self.domains[unused_var]:
            local_layout[unused_var] = value
            nodes_count[0] += 1
            if self.constraints.check_constraints(local_layout, unused_var):
                self.__backtracking(local_layout, solutions, start_time, returns_count, nodes_count, stats)
            returns_count[0] += 1

    def forward_checking(self, layout, solutions, stats: dict):
        start_time = time.time()
        nodes_count = [0]
        returns_count = [0]
        new_domains = self.domains.copy()
        if self.check_all_domains(layout, new_domains):
            self.variables_heuristic()
            self.__forward_checking(layout, solutions, new_domains, start_time, returns_count, nodes_count, stats)
        stats['all_solutions_time'] = time.time()-start_time
        stats['all_solutions_returns'] = returns_count[0]
        stats['all_solutions_nodes'] = nodes_count[0]

    def __forward_checking(self, layout, solutions, domains, start_time, returns_count, nodes_count, stats: dict):
        if len(layout) == len(self.variables):
            if len(solutions) == 0:
                stats['first_solution_time'] = time.time() - start_time
                stats['first_solution_returns'] = returns_count[0]
                stats['first_solution_nodes'] = nodes_count[0]
            solutions.append(layout)
            returns_count[0] += 1
            return
        unused_var = [v for v in self.variables if v not in layout.keys()][0]
        local_layout = layout.copy()
        self.values_heuristic(local_layout, domains, unused_var)
        for value in domains[unused_var]:
            local_domains = domains.copy()
            local_layout[unused_var] = value
            nodes_count[0] += 1
            if self.check_domains(unused_var, local_layout, local_domains):
                self.__forward_checking(local_layout, solutions, local_domains, start_time, returns_count,
                                        nodes_count, stats)
            returns_count[0] += 1
