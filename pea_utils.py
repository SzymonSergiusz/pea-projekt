from typing import Dict

import numpy as np


def write_to_csv_from_config(method: (), file_name, iterations, expected_dist, expected_path, output_name,
                             do_test=False):
    import csv
    is_header = False
    with open(output_name, 'a', newline=''
              ) as f:
        writer = csv.writer(f)
        for i in range(iterations):

            path, dist, time, memory_usage = perform_method(file_name, method)
            # test czy wygenerowane dodatkowe zgadzają się z oczekiwanymi wynikami z pliku .ini
            if do_test:
                assert path == expected_path
                assert dist == expected_dist

            if not is_header:
                header = [file_name, iterations, dist, path]
                writer.writerow(header)
                is_header = True
            writer.writerow([time, memory_usage])
            # writer.writerow([memory_usage])


def perform_method_np(file_name: str, method: ()):
    from time import perf_counter
    graph = file_to_graph(file_name)
    start = perf_counter()

    path, dist = method(np.asarray(graph))
    stop = perf_counter()
    diff = stop - start
    return path, dist, diff


import memory_profiler


def perform_method(file_name: str, method: ()):
    from time import perf_counter
    graph = file_to_graph(file_name)
    start = perf_counter()
    memory_profiler.profile()
    path, dist = method(graph)
    mem_usage = memory_profiler.memory_usage()
    stop = perf_counter()
    diff = stop - start
    return path, dist, diff, mem_usage


import numpy as np


def file_to_graph(file_name: str):
    data = []
    with open(file_name) as f:
        size: int = int(f.readline().strip())
        for i in range(size):
            line = f.readline()
            data.append(list(map(int, line.strip().split())))
    graph = np.asarray(data)
    np.fill_diagonal(graph, 0)
    # print(graph)
    return graph

def file_to_graph_aco(file_name: str):
    data = []
    file_name = '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/' + file_name
    with open(file_name) as f:
        size: int = int(f.readline().strip())
        for i in range(size):
            line = f.readline()
            data.append(list(map(int, line.strip().split())))
    graph = np.asarray(data)
    np.fill_diagonal(graph, 0)
    # print(graph)
    return graph


def write_to_csv(file_name, times, method: (), output_name='test_atsp_out'):
    import csv
    is_header = False
    with open(f'../{output_name}.csv', 'a') as f:
        writer = csv.writer(f)
        for i in range(times):
            path, dist, time, memory_usage = perform_method(file_name, method)
            if not is_header:
                header = [file_name, times, dist, str(path).replace('(', '').replace(')', '')]
                writer.writerow(header)
                is_header = True
            writer.writerow([time])
            writer.writerow([memory_usage])


def perform_test(file_name: str, written_method, lib_method):
    from time import perf_counter
    import numpy as np

    graph = file_to_graph(file_name)
    start = perf_counter()
    path, dist = lib_method(np.array(graph))
    stop = perf_counter()
    diff = stop - start
    print("testowa metoda ", path + [0], dist, diff)

    start = perf_counter()
    path, dist = written_method(np.array(graph))
    stop = perf_counter()
    diff = stop - start
    print("napisana metoda ", path, dist, diff)


def __readConfigFile(ini: str):
    lines = []
    with open(ini, 'r') as f:
        for line in f:
            lines.append(line)
    return lines


def execute_from_ini(method, ini: str):
    lines = __readConfigFile(ini)
    output_name = lines.pop()
    for line in lines:
        if line[0] == '#':
            continue
        arr_as_str = line.strip().split(' ', maxsplit=3)
        file_name, iterations, expected_dist, expected_path = arr_as_str
        expected_path = [int(p) for p in expected_path.replace('[', '').replace(']', '').strip().split(',')]
        write_to_csv_from_config(method, file_name, int(iterations), int(expected_dist), expected_path, output_name)

    with open(output_name, 'a') as f:
        f.write(f'{output_name}\n')


def execute_from_ini(method, ini: str):
    lines = __readConfigFile(ini)
    output_name = lines.pop()
    for line in lines:
        arr_as_str = line.strip().split(' ', maxsplit=3)
        file_name, iterations, expected_dist, expected_path = arr_as_str
        expected_path = [int(p) for p in expected_path.replace('[', '').replace(']', '').strip().split(',')]
        write_to_csv_from_config(method, file_name, int(iterations), int(expected_dist), expected_path, output_name)

    with open(output_name, 'a') as f:
        f.write(f'{output_name}\n')


def execute_from_ini_sa(method, ini: str):
    lines = __readConfigFile(ini)
    output_name = lines.pop()
    print(output_name)
    for line in lines:
        if line[0] == '#':
            print('pomijam')
            continue
        arr_as_str = line.strip().split(' ')
        # print(arr_as_str)
        file_name, iterations, expected_dist, wybor_t0, wybor_x0, chlodzenie, dlugosc_epoki, sposob_sasiada = arr_as_str

        parametry = [wybor_t0, chlodzenie, dlugosc_epoki, sposob_sasiada]

        write_to_csv_from_config_sa(method, file_name, int(iterations), int(expected_dist), output_name, parametry)

    with open(output_name, 'a') as f:
        f.write(f'{output_name}\n')


def write_to_csv_from_config_sa(method: (), file_name, iterations, expected_dist, output_name,
                                parametry):
    import csv
    is_header = False
    with open(output_name, 'a', newline=''
              ) as f:
        writer = csv.writer(f)
        for i in range(iterations):

            path, dist, time, memory_usage, ile_epok, temp_poczatkowa, temp_koncowa = perform_method_sa(file_name,
                                                                                                        method,
                                                                                                        parametry)

            if not is_header:
                header = [file_name, iterations, expected_dist, parametry]
                writer.writerow(header)
                is_header = True
            writer.writerow([path, dist, time, memory_usage, ile_epok, temp_poczatkowa, temp_koncowa])

    # !_ parametry = [wybor_t0, chlodzenie, dlugosc_epoki, sposob_sasiada]


def perform_method_sa(file_name: str, method: (), parametry):
    import SimulatedAnnealing.SA as SA
    chlodzenie: Dict[
        str, ()
    ] = {
        "geometryczny": SA.geometryczny,
        "logarytmiczny": SA.logarytmiczny,
    }
    wybor_t0: Dict[
        str, ()
    ] = {
        "temp_wzor": SA.temp_init,
        "simple_temp": SA.simple_temp_init,
    }
    epoki: Dict[
        str, ()
    ] = {
        "mnoznik": SA.epoka_mnoznik,
        "potega": SA.epoka_potega,
    }
    sposob: Dict[
        str, ()
    ] = {
        "dwa_zamiany": SA.dwa_zamiana,
        "luk": SA.wymiana_lukow,
    }

    from time import perf_counter
    graph = file_to_graph(file_name)

    start = perf_counter()
    memory_profiler.profile()
    path, dist, temp_koncowa, temp_poczatkowa, ile_epok = method(graph, chlodzenie[parametry[1]],
                                                                 wybor_t0[parametry[0]], sposob[parametry[3]],
                                                                 epoki[parametry[2]])
    mem_usage = memory_profiler.memory_usage()
    stop = perf_counter()
    diff = stop - start
    return path, dist, diff, mem_usage, ile_epok, temp_poczatkowa, temp_koncowa


def execute_from_ini_aco(method, ini: str):
    lines = __readConfigFile(ini)
    output_name = lines.pop()
    print(output_name)
    for line in lines:
        if line[0] == '#':
            print('pomijam')
            continue
        arr_as_str = line.strip().split(' ')
        # print(arr_as_str)
        file_name, iterations, expected_dist, alfa, beta, schemat = arr_as_str

        parametry = [float(alfa), float(beta), str(schemat)]

        write_to_csv_from_config_aco(method, file_name, int(iterations), int(expected_dist), output_name, parametry)

    with open(output_name, 'a') as f:
        f.write(f'{output_name}\n')


def write_to_csv_from_config_aco(method: (), file_name, iterations, expected_dist, output_name,
                                 parametry):
    import csv
    is_header = False
    with open(output_name, 'a', newline=''
              ) as f:
        writer = csv.writer(f)
        for i in range(iterations):

            path, dist, time, memory_usage = perform_method_aco(file_name,
                                                                method,
                                                                parametry)

            if not is_header:
                header = [file_name, iterations, expected_dist, parametry]
                writer.writerow(header)
                is_header = True
            writer.writerow([path, dist, time, memory_usage])

    # !_ parametry = [alfa, beta, schemat]


def perform_method_aco(file_name: str, method: (), parametry):
    from time import perf_counter
    from AntColony.ACO import solve_tsp_nearest
    graph = file_to_graph_aco(file_name)

    start = perf_counter()

    est_path, est_cost = solve_tsp_nearest(graph)
    tau0 = len(graph) / est_cost
    memory_profiler.profile()
    # parametry = [float(alfa), float(beta), str(schemat)]
    path, dist = method(graph, 40, parametry[0], parametry[1], 0.5, tau0, est_cost, parametry[2])

    mem_usage = memory_profiler.memory_usage()
    stop = perf_counter()
    diff = stop - start
    return path, dist, diff, mem_usage
