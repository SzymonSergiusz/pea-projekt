

import numpy as np

import pea_utils


def nearest_neighbour(distances):
    ile_miast = len(distances)
    odwiedzone = [False] * ile_miast
    path = []
    min_dist = 0

    obecne_miasto = 0
    path.append(obecne_miasto)
    odwiedzone[obecne_miasto] = True

    while len(path) < ile_miast:
        min_city = None
        min_dist = float('inf')

        for city in range(ile_miast):
            if not odwiedzone[city]:
                distance = distances[obecne_miasto][city]
                if distance < min_dist:
                    min_city = city
                    min_dist = distance

        obecne_miasto = min_city
        path.append(obecne_miasto)
        odwiedzone[obecne_miasto] = True
        min_dist += min_dist

    path.append(0)
    min_dist += distances[obecne_miasto][0]

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

def ACO_DAS(graph, pokolenia, alfa, beta, ro, tau0, Q):
    n = len(graph[0])
    ants = n

    feromony = np.zeros((n, n))
    feromony += tau0
    min_distance = float('inf')
    min_path = None
    visibility = np.copy(graph).astype(float)
    visibility += 0.1
    visibility = 1 / visibility

    S = np.arange(n)

    for pokolenie in range(pokolenia):

        for ant in range(ants):
            constructed_path = []
            np.random.shuffle(S)
            current_city = S[0]

            while len(S) > 0:
                # wybierz miasto j na podstawie Pij
                next_city = Pij(alfa, beta, feromony, visibility, current_city, S)
                constructed_path.append(next_city)

                S = S[S != next_city]
                feromony[current_city][next_city] += Q
                current_city = next_city
            constructed_path.append(constructed_path[0])
            distance = dlugosc(constructed_path, graph)

            if distance < min_distance:
                min_distance = distance
                min_path = constructed_path

            S = np.arange(n)
        feromony *= (1 - ro)

    return min_path, min_distance


def ACO(graph, pokolenia, alfa, beta, ro, tau0, Q, schemat):
    if schemat == 'CAS':
        return ACO_CAS(graph, pokolenia, alfa, beta, ro, tau0, Q)
    elif schemat == 'DAS':
        return ACO_DAS(graph, pokolenia, alfa, beta, ro, tau0, Q)


def ACO_CAS(graph, pokolenia, alfa, beta, ro, tau0, Q):

    n = len(graph[0])
    ants = n
    feromony = np.zeros((n, n))
    feromony += tau0
    min_distance = float('inf')
    min_path = None

    visibility = np.copy(graph).astype(float)
    visibility += 0.1
    visibility = 1 / visibility


    S = np.arange(n)
    for pokolenie in range(pokolenia):

        for ant in range(ants):
            constructed_path = []
            np.random.shuffle(S)
            current_city = S[0]
            while len(S) > 0:
                next_city = Pij(alfa, beta, feromony, visibility, current_city, S)
                constructed_path.append(next_city)
                S = S[S != next_city]

                current_city = next_city

            constructed_path.append(constructed_path[0])
            distance = dlugosc(constructed_path, graph)

            if distance < min_distance:
                min_distance = distance
                min_path = constructed_path

            feromony = CAS(feromony, Q, distance, constructed_path)
            S = np.arange(n)

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
        est_path, est_cost = nearest_neighbour(graph)

        tau0 = len(graph) / est_cost

        min_path, min_dist = ACO(graph, 40, alfa, beta, ro, tau0, est_cost, 'DAS')
        optimum = file_dict[f]
        print(
            f'Plik: {f} | optymalny koszt: {file_dict[f]}\nŚcieżka: {min_path}\nKoszt: {min_dist}\nJakość: {((min_dist - optimum) / optimum) * 100}%\n___________________________')


    # execute_from_ini_aco(ACO, '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/konfigi/badanie_schematow_dorigo'
    #                           '/test_DORIGO_CAS.ini')