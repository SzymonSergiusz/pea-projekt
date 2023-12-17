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
            # test czy wygenerowane wyniki zgadzają się z oczekiwanymi wynikami z pliku .ini
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


def file_to_graph(file_name: str):
    data = []
    with open(file_name) as f:
        size: int = int(f.readline().strip())
        for i in range(size):
            line = f.readline()
            data.append(list(map(int, line.strip().split())))

    # pozbycie się 'dziwnych' oznaczeń diagonali
    np.fill_diagonal(np.asarray(data), 0)
    return data


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
        arr_as_str = line.strip().split(' ', maxsplit=3)
        file_name, iterations, expected_dist, expected_path = arr_as_str
        expected_path = [int(p) for p in expected_path.replace('[', '').replace(']', '').strip().split(',')]
        write_to_csv_from_config(method, file_name, int(iterations), int(expected_dist), expected_path, output_name)

    with open(output_name, 'a') as f:
        f.write(f'{output_name}\n')

# def execute_from_ini(method, ini: str):
#
#
#     lines = __readConfigFile(ini)
#     output_name = lines.pop()
#     for line in lines:
#         arr_as_str = line.strip().split(' ', maxsplit=3)
#         file_name, iterations, expected_dist, expected_path = arr_as_str
#
#         splitted = file_name.split('.')
#         if splitted[1] == 'astp':
#             print('tsplib')
#             import tsplib95
#             problem = tsplib95.load_problem()
#             graph = problem.get_graph()
#
#         else:
#
#             expected_path = [int(p) for p in expected_path.replace('[', '').replace(']', '').strip().split(',')]
#             write_to_csv_from_config(method, file_name, int(iterations), int(expected_dist), expected_path, output_name)
#
#     with open(output_name, 'a') as f:
#         f.write(f'{output_name}\n')
