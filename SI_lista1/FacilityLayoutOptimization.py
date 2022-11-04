import json
import math
import random

from Connection import Connection
from enum import Enum
from Layout import Layout


def read_json(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)


def manhattan_distance(a: (int, int), b: (int, int)):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def statistics(pop: [Layout]):
    minimum = pop[0].full_cost
    maximum = pop[0].full_cost
    cost_sum = pop[0].full_cost
    length = 0
    for p in pop:
        if p.full_cost > maximum:
            maximum = p.full_cost
        if p.full_cost < minimum:
            minimum = p.full_cost
        length += 1
        cost_sum += p.full_cost
    avg = cost_sum/length
    std = 0
    for p in pop:
        std += (p.full_cost - avg) * (p.full_cost - avg)
    return {'best': minimum, 'worse': maximum, 'avg': round(avg), 'std': round(math.sqrt(std/length))}


def average(array):
    result = 0
    for x in array:
        result += x
    return result / len(array)


def std1(array):
    avg = average(array)
    result = 0
    for x in array:
        result += (x - avg) * (x - avg)
    return math.sqrt(result / len(array))


class Instance(Enum):
    EASY = 'easy'
    FLAT = 'flat'
    HARD = 'hard'


class Selection(Enum):
    TOURNAMENT = 'tournament'
    ROULETTE = 'roulette'


class FacilityLayoutOptimization:

    def __init__(self):
        self.connections: [Connection] = []
        self.height = 0
        self.width = 0
        self.machines_number = 0

    def load_data(self, instance: Instance):
        if instance == Instance.EASY:
            self.height = 3
            self.width = 3
            self.machines_number = 9
        elif instance == Instance.FLAT:
            self.height = 1
            self.width = 12
            self.machines_number = 12
        elif instance == Instance.HARD:
            self.height = 5
            self.width = 6
            self.machines_number = 24
        else:
            raise ValueError

        cost_list = read_json(f'flo_dane_v1.2/{instance.value}_cost.json')
        flow_list = read_json(f'flo_dane_v1.2/{instance.value}_flow.json')

        # connections
        for i in range(0, len(cost_list)):
            self.connections.append(Connection(cost_list[i]['source'], cost_list[i]['dest'], cost_list[i]['cost'],
                                               flow_list[i]['amount']))

    def fitting_function(self, layout: Layout):
        if layout.number_of_machines() != self.machines_number:
            raise ValueError
        result = 0
        for c in self.connections:
            result += manhattan_distance(layout[c.source], layout[c.destination]) * c.cost * c.amount
        layout.full_cost = result
        return layout

    def random_layout(self):
        all_coordinates = []
        for i in range(0, self.width):
            for j in range(0, self.height):
                all_coordinates.append((i, j))
        random.shuffle(all_coordinates)
        machines_layout = []
        for i in range(0, self.machines_number):
            machines_layout.append(all_coordinates[i])
        return self.fitting_function(Layout(machines_layout))

    def random_method(self, n):
        result = []
        best = self.random_layout()
        worst = best
        result.append(best.full_cost)
        for i in range(n-1):
            current = self.random_layout()
            result.append(current.full_cost)
            if current.full_cost < best.full_cost:
                best = current
            if current.full_cost > worst.full_cost:
                worst = current
        return {"best": best.full_cost, "worst": worst.full_cost, "avg": average(result), "std": std1(result)}

    @staticmethod
    def weight_function(fitness, maximum):
        return 1 - math.pow(fitness/maximum, 2)

    def roulette_selection(self, population):
        maximum_cost = max(p.full_cost for p in population)
        weights = []
        population_size = 0
        weight_sum = 0
        for p in population:
            current_weight = self.weight_function(p.full_cost, maximum_cost)
            weights.append(current_weight)
            weight_sum += current_weight
            population_size += 1
        current = 0
        pick = random.uniform(0, weight_sum)
        for i in range(population_size):
            current += weights[i]
            if current >= pick:
                return population[i]

    @staticmethod
    def tournament_selection(population, n):
        random.shuffle(population)
        best = population[0]
        for i in range(1, n):
            current = population[i]
            if current.full_cost < best.full_cost:
                best = current
        return best

    def one_point_crossover(self, mate1, mate2, r_cross):
        if random.random() > r_cross or r_cross == 0:
            return min(mate1, mate2, key=lambda x: x.full_cost)
        child = []
        crossover_point = random.randint(0, self.machines_number)
        count = 0
        for i in mate1.machines:
            if count == crossover_point:
                break
            if i not in mate2.machines[crossover_point:self.machines_number]:
                child.append(i)
                count = count + 1
        child.extend(mate2.machines[crossover_point:self.machines_number])
        return Layout(child)

    def mutation(self, child, r_mut):
        if random.random() > r_mut or r_mut == 0:
            return
        indexes = range(self.machines_number)
        idx1, idx2 = random.sample(indexes, 2)
        previous = child.machines[idx1]
        child.machines[idx1] = child.machines[idx2]
        child.machines[idx2] = previous

    def genetic_algorithm(self, n_iter, n_pop, r_cross, r_mut, selection=Selection.TOURNAMENT, n_tournament=0.3):
        pop = [self.random_layout() for _ in range(n_pop)]
        best = self.tournament_selection(pop, n_pop)
        file = open("wyniki.txt", "w")
        file.write("best\t\t\tworse\t\t\tavg\t\t\t\tstd")
        file.close()
        file = open("wyniki.txt", "a")
        for _ in range(n_iter):
            new_pop = []
            for i in range(n_pop):
                if selection == Selection.TOURNAMENT:
                    mate1 = self.tournament_selection(pop, round(n_tournament * n_pop))
                    mate2 = self.tournament_selection(pop, round(n_tournament * n_pop))
                else:
                    mate1 = self.roulette_selection(pop)
                    mate2 = self.roulette_selection(pop)
                child = self.one_point_crossover(mate1, mate2, r_cross)
                self.mutation(child, r_mut)
                self.fitting_function(child)
                new_pop.append(child)
                if best.full_cost > child.full_cost:
                    best = child
            stats = statistics(new_pop)
            file.write(f"\n{stats['best']}\t\t\t{stats['worse']}\t\t\t{stats['avg']}\t\t\t{stats['std']}")
            pop = new_pop
        file.close()
        return best
