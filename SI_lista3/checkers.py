import random
import copy


class Board:
    def __init__(self, size, pawns_rows=2, board=None):
        # properties
        self.size = size
        self.pawns_rows = pawns_rows if 2 * pawns_rows < size else 2
        self.board: {(int, int): str} = {}
        # board initialization
        if board is None:
            self.__init_board()
        else:
            self.board = board

    def __init_board(self):
        # whites
        for i in range(self.pawns_rows):
            start = 0 if i % 2 == 0 else 1
            for j in range(start, self.size, 2):
                self.board[(i, j)] = "w"
        # blacks
        for i in range(self.size - self.pawns_rows, self.size):
            start = 0 if i % 2 == 0 else 1
            for j in range(start, self.size, 2):
                self.board[(i, j)] = "b"
        # free
        for i in range(self.pawns_rows, self.size - self.pawns_rows):
            start = 0 if i % 2 == 0 else 1
            for j in range(start, self.size, 2):
                self.board[(i, j)] = "."

    def __is_on_board(self, position):
        return 0 <= position[0] < self.size and 0 <= position[1] < self.size

    def __find_attack_paths(self, position, board, path=None, used_direction=None):
        if path is None:
            path = []
        pawn = board[position].lower()
        enemy_pawn = "w" if pawn == "b" else "b"
        is_dame = board[position] == pawn.upper()
        paths = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        # check all directions
        for d in directions:
            if d == used_direction:
                continue
            distance = 1
            enemy_found = False
            move = 0, 0
            # find enemy pawn
            while not enemy_found:
                move = position[0] + (d[0] * distance), position[1] + (d[1] * distance)
                if not self.__is_on_board(move):
                    break
                if board[move].lower() == enemy_pawn:
                    enemy_found = True
                elif is_dame and board[move] == ".":
                    distance += 1
                    continue
                break
            if not enemy_found:
                continue
            # find landing spot
            distance = 1
            while True:
                next_move = move[0] + (d[0] * distance), move[1] + (d[1] * distance)
                if not self.__is_on_board(next_move):
                    break
                if board[next_move] == ".":
                    # new board
                    local_board = board.copy()
                    local_board[position] = "."
                    local_board[move] = "."
                    local_board[next_move] = pawn
                    # new path
                    new_path = path.copy()
                    new_path.append(next_move)
                    # recursion
                    new_paths = self.__find_attack_paths(next_move, local_board, new_path, (-d[0], -d[1]))
                    if len(new_paths) == 0:
                        paths.append(new_path)
                    else:
                        for p in new_paths:
                            paths.append(p)
                if board[next_move] == "." and is_dame:
                    distance += 1
                    continue
                break
        return paths

    @staticmethod
    def __get_longest_attacks(attacks):
        max_length = 0
        for a in attacks:
            current_len = len(a)
            if current_len > max_length:
                max_length = current_len
        result = []
        for a in attacks:
            if len(a) == max_length:
                result.append(a)
        return result

    def is_dame(self, place: (int, int)):
        return False if self.board.get(place) is None else self.board[place] == self.board[place].upper()

    def get_possible_moves(self, position):
        attacks = self.__find_attack_paths(position, self.board)
        if len(attacks) != 0:
            return {"moves": self.__get_longest_attacks(attacks), "isAttack": True}
        possible_moves = []
        pawn = self.board[position]
        ranges = [range(1, 2)] if pawn.lower() == "w" else [range(-1, -2, -1)]
        if self.is_dame(position):
            ranges = [range(1, self.size - position[0]), range(-1, -position[0] - 1, -1)]
        # forward and backward
        for r in ranges:
            # how far
            for dist in r:
                # left and right
                for i in range(-1, 2, 2):
                    move = position[0] + dist, position[1] + (i * dist)
                    if not self.__is_on_board(move):
                        continue
                    if self.board[move] == ".":
                        possible_moves.append([move])
        return {"moves": possible_moves, "isAttack": False}

    def print(self):
        border = "  "
        for i in range((self.size * 4) + 1):
            border += "-"
        print(border)
        for i in range(self.size - 1, -1, -1):
            for j in range(self.size):
                if j == 0:
                    print(f'{i} |', end=" ")
                print(self.board.get((i, j), " "), end="\t" if j != self.size - 1 else " |\n")
        print(border)
        # x axis
        print("", end="    ")
        for i in range(self.size):
            print(f"{i}", end="\t")
        print()

    def get_pawns(self, color):
        pawns = []
        for pawn in self.board.keys():
            if self.board[pawn].lower() == color:
                pawns.append(pawn)
        return pawns

    def is_opposite_border(self, color, position):
        border = self.size - 1 if color == "w" else 0
        return position[0] == border

    def make_move(self, source, destinations, color):
        pawn = self.board.get(source)
        if pawn is None or pawn.lower() != color:
            return False
        possible_moves = self.get_possible_moves(source)
        if destinations not in possible_moves['moves']:
            return False
        current_position = source
        for d in destinations:
            self.board[current_position] = "."
            self.board[d] = pawn
            distance = abs(d[0] - current_position[0])
            direction = (d[0] - current_position[0]) / distance, (d[1] - current_position[1]) / distance
            for i in range(1, distance):
                pos = current_position[0] + (i * direction[0]), current_position[1] + (i * direction[1])
                if self.board[pos] != "." and self.board[pos] != pawn:
                    self.board[pos] = "."
                    break
            current_position = d
        if self.is_opposite_border(pawn, current_position):
            self.board[current_position] = pawn.upper()

    def get_all_possible_moves(self, player_color):
        possible_pawns = []
        possible_moves = {}
        pawns_with_attacks = []
        for pawn in self.get_pawns(player_color):
            moves = self.get_possible_moves(pawn)
            if len(moves['moves']) == 0:
                continue
            if moves['isAttack']:
                pawns_with_attacks.append(pawn)
            possible_pawns.append(pawn)
            possible_moves[pawn] = moves
        if len(pawns_with_attacks) != 0:
            max_length = 0
            for pawn in pawns_with_attacks:
                curr_len = len(possible_moves[pawn]['moves'][0])
                if curr_len > max_length:
                    max_length = curr_len
            possible_attacks = {}
            for pawn in pawns_with_attacks:
                if len(possible_moves[pawn]['moves'][0]) == max_length:
                    possible_attacks[pawn] = possible_moves[pawn]
            return possible_attacks
        return possible_moves

    def __calculate_points(self, pawns, color):
        result = 0
        start = 0 if color == "w" else -(self.size - 1)
        step = self.size / 4
        opposite = 1 if color == "w" else -1
        for pawn in pawns:
            # dame
            result += 50 if self.is_dame(pawn) else 5
            # edges
            if 1 < pawn[0] < self.size - 2 and 1 < pawn[1] < self.size - 2:
                result += 2
            elif 0 < pawn[0] < self.size - 1 and 0 < pawn[1] < self.size - 1:
                result += 1
            # level
            if start + step <= pawn[0] * opposite < start + (step*2):
                result += 1
            elif start + (step*2) <= pawn[0] * opposite < start + (step*3):
                result += 3
            elif pawn[0] * opposite >= start + (step*3):
                result += 20 if not self.is_dame(pawn) else 5
        return result

    def evaluation_function(self, color):
        pawns = self.get_pawns(color)
        player_points = self.__calculate_points(pawns, color)
        opponent = "w" if color == "b" else "b"
        opponents_pawns = self.get_pawns(opponent)
        opponents_points = self.__calculate_points(opponents_pawns, opponent)
        return player_points - opponents_points


class Player:
    def __init__(self, name):
        self.name = name
        self.color = ""

    def choose_pawn(self, pawns, board: Board = None) -> (int, int):
        pass

    def choose_move(self, moves, board: Board = None) -> [(int, int)]:
        pass

    def set_color(self, color):
        self.color = color


class Checkers:
    def __init__(self, player1: Player, player2: Player, board: Board):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.only_dames_round = -1
        self.winner = None
        self.number_of_rounds = 0

    def assign_colors(self):
        value = random.randint(0, 1)
        if value == 0:
            self.player1.set_color("w")
            self.player2.set_color("b")
        else:
            self.player1.set_color("b")
            self.player2.set_color("w")

    def is_game_finished(self, current_player, next_player):
        if self.number_of_rounds > 60:
            return True
        pawns_available = self.board.get_pawns(next_player.color)
        if self.only_dames_round == 0:
            current_pawns = self.board.get_pawns(current_player.color)
            self.only_dames_round += 1
            for p in current_pawns:
                if not self.board.is_dame(p):
                    self.only_dames_round -= 1
                    break
        elif self.only_dames_round != 0:
            self.only_dames_round += 1
        if self.only_dames_round == 15:
            return True
        if len(pawns_available) == 0:
            self.winner = current_player
            return True
        for p in pawns_available:
            if len(self.board.get_possible_moves(p)['moves']) != 0:
                return False
        self.winner = current_player
        return True

    def start_game(self):
        print("Checkers")
        self.assign_colors()
        queue = [self.player1, self.player2]
        current_player = 0 if self.player1.color == "w" else 1
        game_finished = False
        rounds = 1
        while not game_finished:
            self.number_of_rounds += 1
            print(f"Round {rounds}")
            self.board.print()
            player = queue[current_player]
            print(player.name + "'s turn!" + " (" + player.color + ")")
            possible_moves = self.board.get_all_possible_moves(player.color)
            pawn_chosen = False
            pawn = 0, 0
            # choose pawn
            while not pawn_chosen:
                pawn = player.choose_pawn(list(possible_moves.keys()), board=copy.deepcopy(self.board))
                if pawn in possible_moves.keys():
                    pawn_chosen = True
                else:
                    print(f"pawn incorrect: {pawn}")
            move_chosen = False
            move = [(0, 0)]
            # choose move
            while not move_chosen:
                move = player.choose_move(possible_moves[pawn]['moves'])
                if move in possible_moves[pawn]['moves']:
                    move_chosen = True
                else:
                    print("move incorrect")
            self.board.make_move(pawn, move, player.color)
            current_player = (current_player + 1) % 2
            game_finished = self.is_game_finished(player, queue[current_player])
            print("\n##########################################\n")
            rounds += 1
        self.board.print()
        print("Game is finished")
        if self.winner is None:
            print("Result: DRAW!")
        else:
            print("Result: " + self.winner.name + " (" + self.winner.color + ")" + " WON!")
