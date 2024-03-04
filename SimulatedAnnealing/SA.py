import random
import numpy
import numpy as np
import pea_utils


def czy_akceptowac(fx: float, fy: float, T: float):
    delta = fy - fx
    return (delta <= 0) or ((delta > 0) and (np.exp(-delta / T) >= np.random.rand()))


def koszt(current_path, graph):
    suma = 0
    for i in range(len(current_path) - 1):
        suma += graph[current_path[i]][current_path[i + 1]]
    suma += graph[current_path[-1]][current_path[0]]
    return suma


# !_ schematy wyboru rozwiazan początkowych
def losowe_rozw(graph):
    graf = np.asarray(graph)
    arr = np.arange(1, np.array(graf.shape[0]))
    np.random.shuffle(arr)
    return [0] + list(arr)


# TODO ten z wyliczaniem

# !_ schematy przegladu
# source wykład
def dwa_zamiana(current_solution):
    sasiad = current_solution.copy()
    i, j = random.sample(range(1, len(current_solution)), 2)
    sasiad[i], sasiad[j] = sasiad[j], sasiad[i]
    return sasiad


def wymiana_lukow(current_solution):
    luk = current_solution.copy()
    i, j = random.sample(range(1, len(luk)), 2)

    start = min(i, j)
    end = max(i, j)
    luk[start:end + 1] = numpy.flip(list(luk[start:end + 1]))
    return luk


# todo funkcja obliczenia jakości rozwiązania // w excelu?

# !_ schematy wyboru temperatury poczatkowej
def simple_temp_init(graph, funkcja_przegladu, x, y):
    n = len(graph)
    return n * n


def temp_probkowanie(graph, x, fx: float, przeglad: (), ile_razy=100):
    # todo wykład s 10
    pass


# source http://ndl.ethernet.edu.et/bitstream/123456789/48958/1/6..pdf
#  bazując na Metaheuristics for hard optimization s. 44, 45
#  tau -> 50%
#  ilosc badanych disturbances -> 100
def temp_init(graph, x, fx: float, przeglad: (), ile_razy=100):
    disturbances = []
    for i in range(ile_razy):
        y = przeglad(x.copy())
        fy = koszt(y, graph)
        delta = fy - fx
        disturbances.append(delta)

    srednia = np.abs(np.mean(disturbances))
    # założenie że to słabe rozwiązanie
    tau0 = 0.5
    # po przekształceniu wzoru wychodzi
    T = -srednia / np.log(tau0)
    return T


def geometryczny(T: float, lam: float, iter=None, dlugosc_epoki = None, initial_t = None):
    return lam * T


def logarytmiczny(T: float, iter: int, lam, max_iter, t0):
    # lambda > 1
    Tmin = 0.1

    lamda = (t0 - Tmin) / (max_iter * t0 * Tmin)
    return T / (1 + lamda * T)


def epoka_mnoznik(n, times=10):
    return n * times


def epoka_potega(n):
    return n * n


def simulate_annealing(graph: [], cooling_scheme: (), temp_init_scheme: (), funkcja_przegladu: (),
                       wybor_epoki: (), lam=0.9):
    n = len(graph)
    x = losowe_rozw(graph)
    fx = koszt(x, graph)
    initial_t = temp_init_scheme(graph, x, fx, funkcja_przegladu)
    T = initial_t

    dlugosc_epoki = wybor_epoki(n)

    # source Metaheuristics for hard optimization s43
    # Program termination: can be activated after 3 successive temperature
    # stages without any acceptance.
    k_brak_poprawy = 3
    k_brak_poprawy_licznik = 0

    temp_min = 0.1

    best_path = []
    best_cost = float('inf')

    while (k_brak_poprawy_licznik < k_brak_poprawy) and T > temp_min:
        k_zaakceptowanych = 0
        aktualne_k = 0

        for k in range(dlugosc_epoki):
            y = funkcja_przegladu(x)
            fx = koszt(x, graph)
            fy = koszt(y, graph)

            # zgodnie z metaheuristics from design to implementation
            # i z prezentacją wykład 6 slajd 7

            if fy < fx:
                best_cost = fy
                best_path = y.copy()

            if czy_akceptowac(fx, fy, T):
                x = y
                fx = fy
                k_zaakceptowanych += 1
                k_brak_poprawy_licznik = 0

            aktualne_k += 1

        k_brak_poprawy_licznik += k_zaakceptowanych == 0
        T = cooling_scheme(T, lam, aktualne_k, dlugosc_epoki, initial_t)
    return list(best_path) + [0], best_cost, T, initial_t, dlugosc_epoki


if __name__ == '__main__':

    # badanie_chlodzenia = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/ini/badanie_chlodzenia'
    # badanie_epok = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/ini/badanie_epok'
    # badanie_t0 = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/ini/badanie_t0'
    # badanie_rozw = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/ini/badanie_wyboru_rozwiazania'
    # test badanie chłodzenia
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_chlodzenia+'/test_wzor_los_geo_mnoz_dwazamiany.ini')
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_chlodzenia+'/test_wzor_los_log_mnoz_dwa_zamiany.ini')
    #
    #
    # #badanie epok
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_epok+'/test_wzor_los_geo_pot_luk.ini')

    # badanie t0
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_t0+'/test_simple_los_geo_mnoz_luk.ini')

    # badanie wyboru rozwiązania
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_rozw+'/test_wzor_los_geo_mnoz_dwazamiany.ini')
    # uzupelnienie
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'uzupelnienie.ini')
    # ścieżka do  pliku ini
    # ini_path = 'test_wzor_los_geo_mnoz_luk.csv'
    # pea_utils.execute_from_ini_sa(simulate_annealing, ini_path)

    # uruchomienie z terminala
    ini = input('podaj sciezke do pliku konfiguracyjnego ini')
    pea_utils.execute_from_ini_sa(simulate_annealing, ini)