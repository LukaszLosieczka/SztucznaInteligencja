from BinaryPuzzle import BinaryPuzzle
from FutoshikiPuzzle import FutoshikiPuzzle
from CSP import Method


def print_layouts(solutions, n):
    count = 1
    for layout in solutions[0]:
        print(f'{count}.')
        for i in range(n):
            for j in range(n):
                print(f'{layout[i, j]}', end='\t')
            print('\n')
        count += 1
    print(f'{solutions[1]}\n')


if __name__ == '__main__':
    # # backtracking
    # print('binary_6x6')
    # print_layouts(BinaryPuzzle('binary_6x6', 6).get_solutions(), 6)
    # print('binary_8x8')
    # print_layouts(BinaryPuzzle('binary_8x8', 8).get_solutions(), 8)
    # print('binary_10x10')
    # print_layouts(BinaryPuzzle('binary_10x10', 10).get_solutions(), 10)
    #
    # print('futoshiki_4x4')
    # print_layouts(FutoshikiPuzzle('futoshiki_4x4', 4).get_solutions(), 4)
    # print('futoshiki_5x5')
    # print_layouts(FutoshikiPuzzle('futoshiki_5x5', 5).get_solutions(), 5)
    # print('futoshiki_6x6')
    # print_layouts(FutoshikiPuzzle('futoshiki_6x6', 6).get_solutions(), 6)

    # forward checking
    print('binary_6x6')
    print_layouts(BinaryPuzzle('binary_6x6', 6).get_solutions(method=Method.FORWARD_CHECKING), 6)
    print('binary_8x8')
    print_layouts(BinaryPuzzle('binary_8x8', 8).get_solutions(method=Method.FORWARD_CHECKING), 8)
    print('binary_10x10')
    print_layouts(BinaryPuzzle('binary_10x10', 10).get_solutions(method=Method.FORWARD_CHECKING), 10)

    print('futoshiki_4x4')
    print_layouts(FutoshikiPuzzle('futoshiki_4x4', 4).get_solutions(method=Method.FORWARD_CHECKING), 4)
    print('futoshiki_5x5')
    print_layouts(FutoshikiPuzzle('futoshiki_5x5', 5).get_solutions(method=Method.FORWARD_CHECKING), 5)
    print('futoshiki_6x6')
    print_layouts(FutoshikiPuzzle('futoshiki_6x6', 6).get_solutions(method=Method.FORWARD_CHECKING), 6)


    #
    # # backtracking
    # print('binary_6x6_empty')
    # print_layouts(BinaryPuzzle('binary_6x6', 6).get_solutions(), 6)
    # print('binary_8x8_empty')
    # print_layouts(BinaryPuzzle('binary_8x8', 8).get_solutions(), 8)
    # print('binary_10x10_empty')
    # print_layouts(BinaryPuzzle('binary_10x10', 10).get_solutions(), 10)
    #
    # print('futoshiki_4x4_empty')
    # print_layouts(FutoshikiPuzzle('futoshiki_4x4', 4).get_solutions(), 4)
    # print('futoshiki_5x5_empty')
    # print_layouts(FutoshikiPuzzle('futoshiki_5x5', 5).get_solutions(), 5)
    # print('futoshiki_6x6_empty')
    # print_layouts(FutoshikiPuzzle('futoshiki_6x6', 6).get_solutions(), 6)
    #
    # # forward checking
    # print('binary_6x6_empty')
    # print_layouts(BinaryPuzzle('binary_6x6', 6).get_solutions(method=Method.FORWARD_CHECKING), 6)
    # print('binary_8x8_empty')
    # print_layouts(BinaryPuzzle('binary_8x8', 8).get_solutions(method=Method.FORWARD_CHECKING), 8)
    # print('binary_10x10_empty')
    # print_layouts(BinaryPuzzle('binary_10x10', 10).get_solutions(method=Method.FORWARD_CHECKING), 10)
    #
    # print('futoshiki_4x4_empty')
    # print_layouts(FutoshikiPuzzle('futoshiki_4x4', 4).get_solutions(method=Method.FORWARD_CHECKING), 4)
    # print('futoshiki_5x5_empty')
    # print_layouts(FutoshikiPuzzle('futoshiki_5x5', 5).get_solutions(method=Method.FORWARD_CHECKING), 5)
    # print('futoshiki_6x6_empty')
    # print_layouts(FutoshikiPuzzle('futoshiki_6x6', 6).get_solutions(method=Method.FORWARD_CHECKING), 6)
