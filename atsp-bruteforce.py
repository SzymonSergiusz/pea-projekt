from time import perf_counter
import numpy as np


def bruteforce(graph):
    from itertools import permutations
    min_dist = float('inf')
    result_path = None

    no_starting_point = range(1, np.array(graph).shape[0])  # od 1 do rozmiaru zakresu

    for current_path in permutations(no_starting_point):
        path_with_zero = [0] + list(current_path)  # dodanie do permutacji zerowego wierzchołka
        current_dist = __count_distance(path_with_zero, graph)
        if current_dist < min_dist:
            min_dist = current_dist
            result_path = path_with_zero + [0]
    return result_path, min_dist


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


def write_to_csv(file_name, times):
    import csv
    is_header = False
    with open('test_atsp_out.csv', 'a') as f:
        writer = csv.writer(f)
        for i in range(times):
            path, dist, time = perform_bf(file_name)
            if not is_header:
                header = [file_name, times, dist, str(path).replace('(', '').replace(')', '')]
                writer.writerow(header)
                is_header = True
            writer.writerow([time])

def write_to_csv_from_config(file_name, iterations, expected_dist, expected_path, output_name):
    import csv
    is_header = False
    with open(output_name, 'a') as f:
        writer = csv.writer(f)
        for i in range(iterations):
            path, dist, time = perform_bf(file_name)
            # test czy wygenerowane wyniki zgadzają się z oczekiwanymi wynikami z pliku .ini
            assert path == expected_path
            assert dist == expected_dist
            if not is_header:
                header = [file_name, iterations, expected_dist, expected_path]
                writer.writerow(header)
                is_header = True
            writer.writerow([time])
def perform_bf(file_name: str):
    graph = file_to_graph(file_name)
    start = perf_counter()
    path, dist = bruteforce(graph)
    stop = perf_counter()
    diff = stop - start
    return path, dist, diff


def perform_bf_test_lib(file_name: str):
    from python_tsp.exact import brute_force
    graph = file_to_graph(file_name)
    start = perf_counter()
    path, dist = brute_force.solve_tsp_brute_force(np.array(graph))
    stop = perf_counter()
    diff = stop - start
    return path + [0], dist, diff


def test_perform_bf(file_name: str):
    path, dist, diff = perform_bf(file_name)
    correct_path, correct_dist, est_diff = perform_bf_test_lib(file_name)
    assert path == correct_path
    assert dist == correct_dist
    print(f'ścieżka: {path} koszt: {dist}\n{file_name} time diff: program: {diff:.20f} | lib: {est_diff:.20f}')


def readConfigFile(ini: str):
    lines = []
    with open(ini, 'r') as f:
        for line in f:
            lines.append(line)
    return lines


def execute_from_ini(lines):
    output_name = lines.pop()
    for line in lines:
        arr_as_str = line.strip().split(' ', maxsplit=3)
        print(arr_as_str)
        file_name, iterations, expected_dist, expected_path = arr_as_str
        expected_path = [int(p) for p in expected_path.replace('[', '').replace(']', '').strip().split(',')]
        write_to_csv_from_config(file_name, int(iterations), int(expected_dist), expected_path, output_name)

    with open(output_name, 'a') as f:
        f.write(output_name)

if __name__ == '__main__':
    # wczytanie pliku .INI
    lines = readConfigFile('test_atsp.ini')
    execute_from_ini(lines)


    # zakomentowany kod do testowania
    # WYGENEROWANIE WYNIKÓW
    # ITERATIONS = 10
    # write_to_csv('dane/tsp_6_1.txt', ITERATIONS)
    # write_to_csv('dane/tsp_6_2.txt', ITERATIONS)
    # write_to_csv('dane/tsp_10.txt', ITERATIONS)
    # write_to_csv('dane/tsp_12.txt', ITERATIONS)
    # write_to_csv('dane/tsp_13.txt', ITERATIONS)
    # write_to_csv('dane/tsp_14.txt', ITERATIONS)
    # write_to_csv('dane/tsp_15.txt', ITERATIONS)
    # write_to_csv('dane/tsp_17.txt', ITERATIONS)

    # TESTOWANIE ZA POMOCĄ PYTHON-TSP
    # test_perform_bf('dane/tsp_6_1.txt')
    # test_perform_bf('dane/tsp_6_2.txt')
    # test_perform_bf('dane/tsp_10.txt')
    # test_perform_bf('dane/tsp_12.txt')