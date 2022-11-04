from checkers import Player


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def __get_tuple_input(prompt):
        while True:
            input_txt = input(prompt)
            try:
                input_tuple = tuple(int(x) for x in input_txt.split(","))
            except ValueError:
                continue
            return input_tuple

    @staticmethod
    def __get_input(prompt):
        while True:
            input_txt = input(prompt)
            try:
                input_int = int(input_txt)
            except ValueError:
                print("incorrect index")
                continue
            return input_int

    def choose_pawn(self, pawns, board=None) -> (int, int):
        pawn_chosen = False
        pawn = 0, 0
        while not pawn_chosen:
            print(f"possible pawns: ")
            index = 0
            for pawn in pawns:
                print(f"{index}: {pawn}")
                index += 1
            pawn_index = self.__get_input("\nenter pawn index: ")
            try:
                pawn = pawns[pawn_index]
                pawn_chosen = True
            except IndexError:
                print("pawn index incorrect")
        return pawn

    def choose_move(self, moves, board=None) -> [(int, int)]:
        move_chosen = False
        move = [(0, 0)]
        while not move_chosen:
            print(f"possible moves: ")
            index = 0
            for move in moves:
                print(f"{index}:", end=" ")
                move_length = len(move)
                for i in range(move_length):
                    print(f"{move[i]}", end=" ")
                    if i != move_length - 1:
                        print("-> ")
                print()
                index += 1
            move_index = self.__get_input("\nenter move index: ")
            try:
                move = moves[move_index]
                move_chosen = True
            except IndexError:
                print("move index incorrect")
        return move
