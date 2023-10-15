from time import perf_counter
import numpy as np


def bruteforce(graph):
    from itertools import permutations
    n = len(graph)
    min_dist = float('inf')
    tsp_path = None

    bez_zer = range(1, np.array(graph).shape[0])

    for current_path in permutations(bez_zer):
        path = [0] + list(current_path)
        current_dist = __count_distance(path, graph)
        if current_dist < min_dist:
            min_dist = current_dist
            tsp_path = path
    return tsp_path, min_dist


def __count_distance(current_path, graph):
    sum = 0
    for i in range(len(current_path) - 1):
        sum += graph[current_path[i]][current_path[i + 1]]
    sum += graph[current_path[-1]][current_path[0]]
    return sum


def file_to_graph(file_name: str):
    data = []
    with open(file_name) as f:
        size: int = int(f.readline().strip())
        for i in range(size):
            line = f.readline()
            data.append(list(map(int, line.strip().split())))
    return data

def write_to_csv(file_name, ):
    pass
    # TODO WYNIK TO NAZWA PLIKU, LICZBA POWTÓRZEŃ, WARTOŚĆ ŚCIEŻKI I ŚCIEŻKA A POTEM \N CZASY
    # with open(file_name, 'w') as f:

def perform_bf(file_name: str):
    print('funkcja programu\n')
    graph = file_to_graph(file_name)

    start = perf_counter()
    path, dist = bruteforce(graph)

    #wszystko


    stop = perf_counter()
    diff = stop-start
    print(f'nazwa pliku: {file_name}\npath: {path}\ndistance: {dist}\nczas:{diff}\n_______________________')

def perform_bf_test_lib(file_name: str):
    print('funkcja testowa\n')
    from python_tsp.exact import brute_force
    graph = file_to_graph(file_name)

    start = perf_counter()
    path, dist = brute_force.solve_tsp_brute_force(np.array(graph))

    #wszystko


    stop = perf_counter()
    diff = stop-start
    print(f'nazwa pliku: {file_name}\npath: {path}\ndistance: {dist}\nczas:{diff}\n_______________________')

if __name__ == '__main__':
    # perform_bf('dane/tsp_6_1.txt')
    # perform_bf_test_lib('dane/tsp_6_1.txt')
    #
    # perform_bf('dane/tsp_6_2.txt')
    # perform_bf_test_lib('dane/tsp_6_2.txt')
    #
    # perform_bf('dane/tsp_10.txt')
    # perform_bf_test_lib('dane/tsp_10.txt')

    perform_bf('dane/tsp_12.txt')
    perform_bf_test_lib('dane/tsp_12.txt')