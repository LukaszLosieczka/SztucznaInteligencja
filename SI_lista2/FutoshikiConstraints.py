from CSP import Constraints


class Inequality:
    def __init__(self, first_numb, second_numb, sign):
        self.first_numb = first_numb
        self.second_numb = second_numb
        self.sign = sign

    def __hash__(self):
        return hash((self.first_numb, self.second_numb))

    def __eq__(self, other):
        return (self.first_numb, self.second_numb) == (other.first_numb, other.second_numb)


class FutoshikiConstraints(Constraints):
    def __init__(self, n):
        self.inequalities: {(int, int): [Inequality]} = dict(((i, j), []) for i in range(n) for j in range(n))
        self.n = n

    def check_constraints(self, layout: {(int, int): int}, place: (int, int)) -> bool:
        return self.check_inequalities(layout, place) and self.check_uniqueness(layout, place)

    def get_number_of_constraints(self, place):
        return len(self.inequalities[place])

    def check_inequalities(self, layout: {(int, int): int}, place: (int, int)) -> bool:
        for inequality in self.inequalities[place]:
            numb1 = layout.get(inequality.first_numb)
            numb2 = layout.get(inequality.second_numb)
            if numb1 is None or numb2 is None:
                return True
            if inequality.sign == '>':
                if not (numb1 > numb2):
                    return False
            elif inequality.sign == '<':
                if not (numb1 < numb2):
                    return False
        return True

    def check_uniqueness(self, layout: {(int, int): int}, place: (int, int)) -> bool:
        row = 0
        column = 0
        for i in range(self.n):
            if layout.get((place[0], i)) != layout[place]:
                row += 1
            if layout.get((i, place[1])) != layout[place]:
                column += 1
        return row == self.n - 1 and column == self.n - 1
