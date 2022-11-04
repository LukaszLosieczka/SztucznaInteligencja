import random
import time

from checkers import Player, Board


class RandomBotPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def choose_pawn(self, pawns, board=None) -> (int, int):
        return pawns[random.randint(0, len(pawns)-1)]

    def choose_move(self, moves, board=None) -> [(int, int)]:
        return moves[random.randint(0, len(moves) - 1)]


class MinMaxBotPlayer(Player):
    def __init__(self, name, depth):
        super().__init__(name)
        self.depth = depth
        self.chosen_pawn = (0, 0)
        self.next_move = [(0, 0)]
        self.time_stats = {"time_sum": 0, "measurements_no": 0}
        self.node_stats = {"nodes_sum": 0, "measurements_no": 0}
        self.moves_number = 0

    def __find_best_move(self, board, opponents_turn=False, depth=5):
        if depth == 0:
            return board.evaluation_function(self.color)
        opponent_color = "b" if self.color == "w" else "w"
        possible_moves = board.get_all_possible_moves(opponent_color if opponents_turn else self.color)
        if len(list(possible_moves.keys())) == 0:
            return board.evaluation_function(self.color)
        self.node_stats["nodes_sum"] += 1
        best_value = None
        best_pawn = None
        best_move = None
        for pawn in possible_moves.keys():
            for move in possible_moves[pawn]['moves']:
                local_board = Board(8, pawns_rows=2, board=board.board.copy())
                local_board.make_move(pawn, move, opponent_color if opponents_turn else self.color)
                current_value = self.__find_best_move(local_board, not opponents_turn, depth-1)
                if best_value is None or \
                        (opponents_turn and current_value < best_value) or \
                        (not opponents_turn and current_value > best_value):
                    best_value = current_value
                    best_pawn = pawn
                    best_move = move
        self.chosen_pawn = best_pawn
        self.next_move = best_move
        return best_value

    def choose_pawn(self, pawns, board=None) -> (int, int):
        if self.moves_number == 1:
            self.chosen_pawn = pawns[random.randint(0, len(pawns)-1)]
            moves = board.get_possible_moves(self.chosen_pawn)['moves']
            self.next_move = moves[random.randint(0, len(moves) - 1)]
        else:
            start = time.time()
            self.__find_best_move(board, depth=self.depth)
            end = time.time()
            self.node_stats["measurements_no"] += 1
            self.time_stats["time_sum"] += end - start
            self.time_stats["measurements_no"] += 1
        # self.moves_number += 1
        return self.chosen_pawn

    def choose_move(self, moves, board=None) -> [(int, int)]:
        return self.next_move

    # def __find_best_move(self, board, opponents_turn=False, depth=5):
    #     if depth == 0:
    #         return board.evaluation_function(self.color)
    #     opponent_color = "b" if self.color == "w" else "w"
    #     possible_moves = board.get_all_possible_moves(opponent_color if opponents_turn else self.color)
    #     if len(list(possible_moves.keys())) == 0:
    #         return board.evaluation_function(self.color)
    #     evaluations = {}
    #     for pawn in possible_moves.keys():
    #         for i in range(len(possible_moves[pawn]['moves'])):
    #             move = possible_moves[pawn]['moves'][i]
    #             local_board = Board(8, pawns_rows=2, board=board.board.copy())
    #             local_board.make_move(pawn, move, opponent_color if opponents_turn else self.color)
    #             evaluations[(pawn, i)] = self.__find_best_move(local_board, not opponents_turn, depth-1)
    #     best_value = None
    #     for key in evaluations.keys():
    #         current_value = evaluations.get(key)
    #         if best_value is None or\
    #             (opponents_turn and current_value < best_value) or\
    #                 (not opponents_turn and current_value > best_value):
    #             best_value = current_value
    #             self.chosen_pawn = key[0]
    #             self.next_move = possible_moves[key[0]]['moves'][key[1]]
    #     return best_value


class AlfaBetaBotPlayer(Player):
    def __init__(self, name, depth):
        super().__init__(name)
        self.depth = depth
        self.chosen_pawn = (0, 0)
        self.next_move = [(0, 0)]
        self.time_stats = {"time_sum": 0, "measurements_no": 0}
        self.node_stats = {"nodes_sum": 0, "measurements_no": 0}
        self.moves_number = 0

    def __find_best_move(self,  board, opponents_turn=False, depth=5, alpha_beta=None):
        if depth == 0:
            return board.evaluation_function(self.color)
        opponent_color = "b" if self.color == "w" else "w"
        possible_moves = board.get_all_possible_moves(opponent_color if opponents_turn else self.color)
        if len(list(possible_moves.keys())) == 0:
            return board.evaluation_function(self.color)
        self.node_stats["nodes_sum"] += 1
        best_value = None
        best_pawn = None
        best_move = None
        for pawn in possible_moves.keys():
            for move in possible_moves[pawn]['moves']:
                local_board = Board(8, pawns_rows=2, board=board.board.copy())
                local_board.make_move(pawn, move, opponent_color if opponents_turn else self.color)
                current_value = self.__find_best_move(local_board, not opponents_turn, depth-1, alpha_beta=best_value)
                # alpha
                if alpha_beta is not None and opponents_turn and current_value <= alpha_beta:
                    return current_value
                # beta
                if alpha_beta is not None and not opponents_turn and current_value >= alpha_beta:
                    return current_value
                if best_value is None or \
                        (opponents_turn and current_value < best_value) or \
                        (not opponents_turn and current_value > best_value):
                    best_value = current_value
                    best_pawn = pawn
                    best_move = move
        self.chosen_pawn = best_pawn
        self.next_move = best_move
        return best_value

    def choose_pawn(self, pawns, board: Board = None) -> (int, int):
        if self.moves_number == 0:
            self.chosen_pawn = pawns[random.randint(0, len(pawns)-1)]
            moves = board.get_possible_moves(self.chosen_pawn)['moves']
            self.next_move = moves[random.randint(0, len(moves) - 1)]
        else:
            start = time.time()
            self.__find_best_move(board, depth=self.depth)
            end = time.time()
            self.node_stats["measurements_no"] += 1
            self.time_stats["time_sum"] += end - start
            self.time_stats["measurements_no"] += 1
        self.moves_number += 1
        return self.chosen_pawn

    def choose_move(self, moves, board: Board = None) -> [(int, int)]:
        return self.next_move
