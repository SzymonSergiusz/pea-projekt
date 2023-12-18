"""
strategia

t <- temperatura, jak najwyższa (n*n?)
s <- jakieś rozwiazanie
best <- s

repeat
    R <- tweak(s_kopia)
    if Quality(R) > Quality(S) OR random<0, 1> < propability(R,S)
        S <- R
    decrease t
    if Quality(S) > Quality(Best)
        Best <- S
until Best is najlepsze OR t <= 0 OR koniec czasu przewidywanego



return Best
"""
# TODO na 3.0
# TODO wybór temperatury i rozwiązania początkowego
# TODO przegląd greedy
# TODO wybór 2-zamiany
# DONE geometryczny

# TODO na 4.0
# TODO + chłodzenie Boltzmanna lub Cauchy'ego
# TODO + wybór rozwiązania w sąsiedztwie z literatury

import random

import numpy
import numpy as np

import pea_utils


class Kryterium:
    def __init__(self, iterations, iterationsWithoutEnhance, acceptedWorseSolutions, errorRate):
        self.iterations = iterations
        self.iterationsWithoutEnchance = iterationsWithoutEnhance
        self.acceptedWorseSolutions = acceptedWorseSolutions
        self.errorRate = errorRate

    def czyPrzekroczyloKryteria(self, licznik: 'Kryterium'):
        return self.iterations < licznik.iterations or self.iterationsWithoutEnchance < licznik.iterationsWithoutEnchance or self.acceptedWorseSolutions < licznik.acceptedWorseSolutions or self.errorRate < licznik.errorRate


def simulate_annealing(graph: [], cooling_scheme: (), temp_init_scheme: (), funkcja_przegladu: (),
                       epoka: (), lam=0.9):
    n = len(graph)
    initial_t = temp_init_scheme(graph, funkcja_przegladu)
    T = initial_t
    #print('początkowa temperatura: ', initial_t)
    x = losowe_rozw(graph)
    fx = None

    # todo kryteria
    # !_ określona liczba iteracji
    #  brak poprawy po okreslonej liczbie iteracji
    #  liczba zaakceptowanych gorszych
    #  akceptowany poziom błędu na podstawie lb i ub #todo

    # !_ epoki
    k_max_iteracji = epoka(n)
    # n * 10  # todo znaleźć źródło?
    # k_max_iteracji = n * n #source długość epoki w6 slajd 11

    # source Metaheuristics for hard optimization s43
    # Program termination: can be activated after 3 successive temperature
    # stages without any acceptance.
    k_brak_poprawy = 3
    k_brak_poprawy_licznik = 0

    k_zaakceptowanych_gorszych = 3
    k_zaakceptowanych_gorszych_licznik = 0

    # licznik_kryterium = Kryterium(0, 0, 0, 0)
    temp_min = 0.1
    # todo
    liczba_epok = None
    # !_ to chyba to samo co

    while k_brak_poprawy_licznik < k_brak_poprawy and T > temp_min:
        k_zaakceptowanych = 0
        k_zaakceptowanych_gorszych_licznik = 0
        aktualne_k = None
        for k in range(k_max_iteracji):
            y = funkcja_przegladu(x)
            fx = koszt(x, graph)
            fy = koszt(y, graph)

            # zgodnie z metaheuristics from design to implementation
            delta = fy - fx
            # !_ zgodnie z prezentacją wykład 6 slajd 7 #todo znaleźć inne źródło
            if delta <= 0:
                x = y
                k_zaakceptowanych += 1
            elif np.exp(-delta / T) >= random.uniform(0, 1):
                x = y
                k_zaakceptowanych += 1
                k_zaakceptowanych_gorszych_licznik += 1

            # if k_zaakceptowanych_gorszych_licznik < k_zaakceptowanych_gorszych:
            #     break
            aktualne_k = k
            msg = (
                f"Temperature {T}. Current value: {fx} "
                f"k: {k + 1}/{k_max_iteracji} "
                f"k_accepted: {k_zaakceptowanych}/{n} "
                f"k_noimprovements: {k_brak_poprawy_licznik}"
            )
            # print(msg)

        k_brak_poprawy_licznik += k_zaakceptowanych == 0
        T = cooling_scheme(T, lam, k)
    return list(x)+[0], fx, T, initial_t, k_max_iteracji


def koszt(current_path, graph):
    sum = 0
    for i in range(len(current_path) - 1):
        sum += graph[current_path[i]][current_path[i + 1]]
    sum += graph[current_path[-1]][current_path[0]]
    return sum


# !_ schematy wyboru rozwiazan
def losowe_rozw(graph):
    arr = np.arange(1, np.array(graph[0]).shape[0])
    np.random.shuffle(arr)
    return [0] + list(arr)


# TODO ten z wyliczaniem

# !_ schematy przegladu

def dwa_zamiana(current_solution):
    sasiad = current_solution.copy()
    i, j = random.sample(range(1, len(current_solution)), 2)
    sasiad[i], sasiad[j] = sasiad[j], sasiad[i]
    return sasiad


def wymiana_lukow(current_solution):
    luk = current_solution.copy()
    i, j = random.sample(range(1, len(current_solution)), 2)
    print(f'łuki do zamiany: {i} | {j}')

    start = min(i, j)
    end = max(i, j)
    luk[start:end + 1] = numpy.flip(list(luk[start:end + 1]))
    return luk


# todo funkcja obliczenia jakości rozwiązania

# !_ schematy wyboru temperatury poczatkowej
def simple_temp_init(graph, funkcja_przegladu):
    n = len(graph)
    return n * n


# source http://ndl.ethernet.edu.et/bitstream/123456789/48958/1/6..pdf
#  bazując na Metaheuristics for hard optimization s. 44, 45
#  tau -> 50%
#  ilosc badanych disturbances -> 100
def temp_init(graph, przeglad: (), ile_razy=100):
    jakies_rozw = losowe_rozw(graph)
    koszt_jakies_rozw = koszt(jakies_rozw, graph)
    disturbances = []
    # jakies_rozw = None
    for i in range(ile_razy):
        jakies_rozw = przeglad(jakies_rozw)
        przeliczone = koszt(jakies_rozw, graph)

        delta = przeliczone - koszt_jakies_rozw
        disturbances.append(delta)
    srednia = np.abs(np.mean(disturbances))
    # założenie że to słabe rozwiązanie
    tau = 0.5
    # po przekształceniu wzoru wychodzi
    t0 = -srednia / np.log(tau)
    return t0


def liniowy(T, lam, iter: int):
    # lambda > 1
    if lam < 1:
        lam = 1.5

    return T / (1 + lam * iter)


def geometryczny(T: float, lam, iter=None):
    if lam >= 1:
        lam = 0.9
    return lam * T


def mnoznik(n):
    return n * 10


def potega(n):
    return n*n


if __name__ == '__main__':
    graph = np.array([
        [0, 20, 30, 31, 28, 40],
        [30, 0, 10, 14, 20, 44],
        [40, 20, 0, 10, 22, 50],
        [41, 24, 20, 0, 14, 42],
        [38, 30, 32, 24, 0, 28],
        [50, 54, 60, 52, 38, 0]
    ])
    # !_ ([0, 1, 2, 3, 4, 5, 0], 132)

    graph1 = pea_utils.file_to_graph('/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/dane/gr96.txt')
    graph1 = numpy.asarray(graph1)
    from python_tsp.heuristics import simulated_annealing

    # print(simulated_annealing.solve_tsp_simulated_annealing(graph1))

    from schematy_chlodzenia import geometryczny

    # print(simulate_annealing(graph1, geometryczny, temp_init, dwa_zamiana, mnoznik))

    path, lib_cost = simulated_annealing.solve_tsp_simulated_annealing(graph1.copy())
    path_sa, sa_cost, _, _, _ = simulate_annealing(graph1.copy(), geometryczny, temp_init, dwa_zamiana, mnoznik)
    print('_____')
    print(f'lib: {lib_cost}\nSA: {sa_cost}')