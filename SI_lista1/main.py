import math

from FacilityLayoutOptimization import FacilityLayoutOptimization, Instance, Selection, Layout
import time


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


if __name__ == '__main__':
    flo = FacilityLayoutOptimization()
    flo.load_data(Instance.HARD)

    print(f"result: {flo.genetic_algorithm(1000, 100, r_cross=0.97, r_mut=0.03, selection=Selection.TOURNAMENT, n_tournament=0.9)}")
    #
    # print("Random method")
    # start = time.time()
    # print(flo.random_method(1000000))
    # end = time.time()
    # print(f'result time: {round((end - start)*1000)/1000} s')
    #
    # print("Genetic algorithm")
    # results = []
    # start = time.time()
    # for i in range(10):
    #     results.append(flo.genetic_algorithm(1000, 100, r_cross=0.8, r_mut=0.9, selection=Selection.TOURNAMENT, n_tournament=0.8).full_cost)
    # print(f"best: {min(results)}, worst: {max(results)}, avg: {average(results)}, std: {std1(results)}")
    # end = time.time()
    # print(f'result time: {round((end - start)*1000)/1000} s')
