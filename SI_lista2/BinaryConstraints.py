from CSP import Constraints


class BinaryConstraints(Constraints):
    def __init__(self, n):
        self.n = n

    def check_constraints(self, layout: {(int, int): int}, place: (int, int)) -> bool:
        return self.check_three_in_row(layout, place) and \
               self.check_three_in_column(layout, place) and \
               self.check_column_and_row_uniqueness(layout, place) and \
               self.check_number_of_zeros_and_ones(layout, place)

    def get_number_of_constraints(self, place):
        neighbours = []
        for i in range(1, 3):
            # row
            neighbours.append((place[0], place[1]-i))
            neighbours.append((place[0], place[1]+i))
            # column
            neighbours.append((place[0]-i, place[1]))
            neighbours.append((place[0]+i, place[1]))
        result = 0
        for n in neighbours:
            if 0 <= n[0] < self.n and 0 <= n[1] < self.n:
                result += 1
        return result

    def check_three_in_row(self, layout: {(int, int): int}, place) -> bool:
        value = layout[place]
        prev_two = [(place[0], place[1]-1), (place[0], place[1]-2)]
        next_two = [(place[0], place[1]+1), (place[0], place[1]+2)]
        count = 0
        # dwa przed
        for x in prev_two:
            if self.n > x[1] >= 0:
                if layout.get(x) == value:
                    count += 1
        if count == 2:
            return False
        count = 0
        # dwa po
        for x in next_two:
            if self.n > x[1] >= 0:
                if layout.get(x) == value:
                    count += 1
        if count == 2:
            return False
        # sasiednie
        if layout.get(prev_two[0]) == value and layout.get(next_two[0]) == value:
            return False
        return True

    def check_three_in_column(self, layout: {(int, int): int}, place: (int, int)) -> bool:
        value = layout[place]
        prev_two = [(place[0]-1, place[1]), (place[0]-2, place[1])]
        next_two = [(place[0]+1, place[1]), (place[0]+2, place[1])]
        count = 0
        # dwa przed
        for x in prev_two:
            if self.n > x[0] >= 0:
                if layout.get(x) == value:
                    count += 1
        if count == 2:
            return False
        count = 0
        # dwa po
        for x in next_two:
            if self.n > x[0] >= 0:
                if layout.get(x) == value:
                    count += 1
        if count == 2:
            return False
        # sąsiednie
        if layout.get(prev_two[0]) == value and layout.get(next_two[0]) == value:
            return False
        return True

    def check_column_and_row_uniqueness(self, layout: {(int, int): int}, place: (int, int)) -> bool:
        row = [layout.get((place[0], i)) for i in range(self.n)]
        row_not_full = False
        column = [layout.get((i, place[1])) for i in range(self.n)]
        column_not_full = False
        if None in row:
            row_not_full = True
        if None in column:
            column_not_full = True
        if row_not_full and column_not_full:
            return True
        for i in range(self.n):
            current_row = []
            current_column = []
            for j in range(self.n):
                current_row.append(layout.get((i, j)))
                current_column.append(layout.get((j, i)))
            # rzad
            if i != place[0] and not row_not_full:
                if current_row == row:
                    return False
            # kolumna
            if i != place[1] and not column_not_full:
                if current_column == column:
                    return False
        return True

    def check_number_of_zeros_and_ones(self, layout: {(int, int): int}, place: (int, int)) -> bool:
        row_zeros = 0
        row_ones = 0
        column_zeros = 0
        column_ones = 0
        maximum = self.n/2
        for i in range(self.n):
            # rzad
            if layout.get((place[0], i)) == 0:
                row_zeros += 1
            if layout.get((place[0], i)) == 1:
                row_ones += 1
            # kolumna
            if layout.get((i, place[1])) == 0:
                column_zeros += 1
            if layout.get((i, place[1])) == 1:
                column_ones += 1
        return row_zeros <= maximum and row_ones <= maximum and column_zeros <= maximum and column_ones <= maximum
