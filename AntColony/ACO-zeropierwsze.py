"""
!_ na 4.0
     obejmuje opracowanie i implementację algorytmu ze stałymi podanymi na
wykładzie (patrz: str. 45) wartościami parametrów α, β, ρ, m, τ0 i heurystykę visibility oraz jednym
schematem rozkładu feromonu (DAS, QAS, bądź CAS).

Rozwiązanie na 4,0 obejmuje zbadanie jakości rozwiązanie (wartość funkcji celu oraz czas)
w zależności od rodzaju dwóch schematów rozkładu feromonu oraz udowodnienie prawdziwości tez
dotyczących wpływu parametrów α i β na zachowanie się algorytmu (patrz: wykład str. 29). Wielkość
błędu jak wyżej.

"""

# !_ uaktualnie poziomu fermonu / rozkłady feromonu

import numpy as np

import pea_utils


def solve_tsp_nearest(distances):
    num_cities = len(distances)
    visited = [False] * num_cities
    path = []
    min_dist = 0

    current_city = 0
    path.append(current_city)
    visited[current_city] = True

    while len(path) < num_cities:
        nearest_city = None
        nearest_distance = float('inf')

        for city in range(num_cities):
            if not visited[city]:
                distance = distances[current_city][city]
                if distance < nearest_distance:
                    nearest_city = city
                    nearest_distance = distance

        current_city = nearest_city
        path.append(current_city)
        visited[current_city] = True
        min_dist += nearest_distance

    path.append(0)
    min_dist += distances[current_city][0]

    return path, min_dist


def dlugosc(current_path, graph):
    suma = 0
    for i in range(len(current_path) - 1):
        suma += graph[current_path[i]][current_path[i + 1]]
    suma += graph[current_path[-1]][current_path[0]]
    return suma


# po krawędzi
def DAS(Q):
    return Q


# po krawędzi

def QAS(Q, krawedz):
    print(f'Q: {Q} | krawedz: {krawedz}')
    return Q / krawedz


# po pełnym przejściu
def CAS(feromony, Q, dlugosc_drogi, path):
    ile = Q / dlugosc_drogi
    for i in range(len(path)-1):
        feromony[path[i]][path[i+1]] += ile
    return feromony




def Pij(alfa, beta, tau, Nij, current_city, S):
    probabilities = np.zeros(len(S))
    for i, city in enumerate(S):
        probabilities[i] = (tau[current_city, city] ** alfa) * (Nij[current_city, city] ** beta)

    probabilities /= np.sum(probabilities)
    next_city_index = np.random.choice(len(S), p=probabilities)
    next_city = S[next_city_index]

    return next_city


def ACO_QAS(graph, pokolenia, alfa, beta, ro, tau0, Q):
    # ilość mrówek = n
    n = len(graph[0])
    ants = n
    # feromony == tau ?
    feromony = np.zeros((n, n))
    feromony += tau0
    min_distance = float('inf')
    min_path = None

    # obliczenie visibility Nij
    visibility = np.copy(graph).astype(float)
    visibility += 0.1
    visibility = 1 / visibility
    #
    # init_S = np.arange(n)
    # S = np.copy(init_S)
    S = np.arange(n)

    for pokolenie in range(pokolenia):
        # S - set of potentially selected cities

        for ant in range(ants):
            constructed_path = []
            np.random.shuffle(S)
            current_city = S[0]
            # S = np.delete(S, 0)

            while len(S) > 0:
                # wybierz miasto j na podstawie Pij
                next_city = Pij(alfa, beta, feromony, visibility, current_city, S)
                constructed_path.append(next_city)
                # S = np.delete(S, np.where(S == next_city))
                S = S[S != next_city]

                current_city = next_city
                # dodanie feromonów dla DAS i QAS
                feromony[current_city][next_city] += QAS(Q, graph[current_city][next_city])

            # dodanie powrotu do pierwszego miasta
            constructed_path.append(constructed_path[0])
            distance = dlugosc(constructed_path, graph)

            if distance < min_distance:
                # print(f'Znaleziono lepsze rozwiązanie: {constructed_path} o koszcie {distance}')
                min_distance = distance
                min_path = constructed_path

            # S = np.copy(init_S)
            S = np.arange(n)
        # wyparowywawanie feromonów
        feromony *= (1 - ro)

    return min_path, min_distance


def ACO_DAS(graph, pokolenia, alfa, beta, ro, tau0, Q):
    # ilość mrówek = n
    n = len(graph[0])
    ants = n
    # feromony == tau ?
    feromony = np.zeros((n, n))
    feromony += tau0
    min_distance = float('inf')
    min_path = None

    # obliczenie visibility Nij
    visibility = np.copy(graph).astype(float)
    visibility += 0.1
    visibility = 1 / visibility

    # init_S = np.arange(n)
    # S = np.copy(init_S)
    S = np.arange(n)

    for pokolenie in range(pokolenia):
        # S - set of potentially selected cities

        for ant in range(ants):
            constructed_path = []
            np.random.shuffle(S)
            current_city = S[0]
            # S = np.delete(S, 0)

            while len(S) > 0:
                # wybierz miasto j na podstawie Pij
                next_city = Pij(alfa, beta, feromony, visibility, current_city, S)
                constructed_path.append(next_city)
                # S = np.delete(S, np.where(S == next_city))
                S = S[S != next_city]

                current_city = next_city
                # dodanie feromonów dla DAS
                # feromony[current_city][next_city] += QAS(Q, graph[current_city][next_city])
                feromony[current_city][next_city] += Q

            # dodanie powrotu do pierwszego miasta
            constructed_path.append(constructed_path[0])
            distance = dlugosc(constructed_path, graph)

            if distance < min_distance:
                # print(f'Znaleziono lepsze rozwiązanie: {constructed_path} o koszcie {distance}')
                min_distance = distance
                min_path = constructed_path

            # S = np.copy(init_S)
            S = np.arange(n)

        # wyparowywawanie feromonów
        feromony *= (1 - ro)

    return min_path, min_distance


def ACO(graph, pokolenia, alfa, beta, ro, tau0, Q, schemat):
    if schemat == 'CAS':
        return ACO_CAS(graph, pokolenia, alfa, beta, ro, tau0, Q)
    elif schemat == 'QAS':
        return ACO_QAS(graph, pokolenia, alfa, beta, ro, tau0, Q)
    elif schemat == 'DAS':
        return ACO_DAS(graph, pokolenia, alfa, beta, ro, tau0, Q / 100)


def ACO_CAS(graph, pokolenia, alfa, beta, ro, tau0, Q):
    # ilość mrówek = n
    n = len(graph[0])
    ants = n
    # feromony == tau ?
    feromony = np.zeros((n, n))
    feromony += tau0
    min_distance = float('inf')
    min_path = None

    # obliczenie visibility Nij
    visibility = np.copy(graph).astype(float)
    visibility += 0.1
    visibility = 1 / visibility
    #
    # init_S = np.arange(n)
    # S = np.copy(init_S)
    S = np.arange(n)
    for pokolenie in range(pokolenia):
        # S - set of potentially selected cities

        for ant in range(ants):

            constructed_path = [0]
            np.random.shuffle(S)

            current_city = 0
            S = S[S != 0]
            # constructed_path.append(current_city)

            while len(S) > 0:
                # wybierz miasto j na podstawie Pij
                next_city = Pij(alfa, beta, feromony, visibility, current_city, S)
                constructed_path.append(next_city)
                # S = np.delete(S, np.where(S == next_city))
                S = S[S != next_city]

                current_city = next_city
                # dodanie feromonów dla DAS i QAS
                # feromony[current_city][next_city] += QAS(Q, graph[current_city][next_city])
                # feromony[current_city][next_city] += QAS(Q)

            # dodanie powrotu do pierwszego miasta
            constructed_path.append(constructed_path[0])
            distance = dlugosc(constructed_path, graph)

            if distance < min_distance:
                # print(f'Znaleziono lepsze rozwiązanie: {constructed_path} o koszcie {distance}')
                min_distance = distance
                min_path = constructed_path

            # dodanie feromonów
            feromony = CAS(feromony, Q, distance, constructed_path)
            # przywrócenie zbioru miast
            S = np.arange(n)

        # wyparowywawanie feromonów
        feromony *= (1 - ro)

    return min_path, min_distance


if __name__ == '__main__':
    # wg Dorigo
    alfa = 1
    beta = 3
    ro = 0.5

    file_dict = {
        'gr17.txt': 2085,
        'gr21.txt': 2707,
        'ftv33.txt': 1286,
        'ft53.txt': 6905,
        'ftv70.txt': 1950,
        'gr96.txt': 55209,
        'ftv170.txt': 2755,
        'gr202.txt': 40160,
        'rbg323.txt': 1326,
        'pcb442.txt': 50778,
        'rbg443.txt': 2720,
    }

    for f in file_dict:
        print(f, file_dict[f])
        graph = pea_utils.file_to_graph(f'dane/{f}')
        est_path, est_cost = solve_tsp_nearest(graph)
        # print(est_path, est_cost)
        tau0 = len(graph) / est_cost
        # print(est_cost)
        min_path, min_dist = ACO(graph, 50, alfa, beta, ro, tau0, est_cost, 'CAS')
        optimum = file_dict[f]
        print(
            f'Plik: {f} | optymalny koszt: {file_dict[f]}\nŚcieżka: {min_path}\nKoszt: {min_dist}\nJakość: {((min_dist - optimum) / optimum) * 100}%\n___________________________')
