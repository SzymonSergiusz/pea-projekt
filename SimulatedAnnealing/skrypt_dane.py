import pandas as pd

abs_path = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/'
out_path = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/przemielone/'


def oblicz_jakosc(wynik: int, optimum: int) -> float:
    return ((wynik - optimum) / optimum) * 100


ile_plikow = 15

chunk_size = 20
total_lines = 15 * chunk_size
index = 0


# columns = ['nazwa pliku', 'średni czas', 'średnie zużycie pamięci', 'średni wynik', 'optimum',
#            'średnia jakość rozwiązania']

def excel_supreme(file_path):
    absolute = abs_path + file_path
    for i in range(0, total_lines, chunk_size + 1):

        with open(absolute, 'r') as file:
            for _ in range(i):
                next(file)
            first_line = file.readline().rstrip()

        data = pd.read_csv(absolute, skiprows=i + 1, nrows=chunk_size, header=None)

        data.columns = first_line.split(',')
        nazwa_pliku, optimum = data.columns[0], data.columns[2]

        srednia_wynik = data.iloc[:, 1].mean()
        srednia_czas = data.iloc[:, 2].mean()
        srednia_pamiec = data.iloc[:, 3].mean()
        srednia_jakosc = oblicz_jakosc(srednia_wynik, int(optimum))
        # print("Średnia wynik:", srednia_wynik)
        # print("Średni czas:", srednia_czas)
        # print("Średnia pamięć:", srednia_pamiec)
        # print("Średnia jakość:", srednia_jakosc)
        #
        # print('--------------------------------------------')

        data_to_save = pd.DataFrame({
            'nazwa pliku': [nazwa_pliku],
            'średni czas': [srednia_czas],
            'średnie zużycie pamięci': [srednia_pamiec],
            'średni wynik': [srednia_wynik],
            'optimum': [optimum],
            'średnia jakość rozwiązania': [srednia_jakosc]
        })

        try:
            out = 'out_' + file_path
            data_to_save.to_csv(out_path + out, mode='a', header=False, index=False)
            print("Dane zapisane do pliku CSV.")
        except Exception as e:
            print("Wystąpił błąd podczas zapisu do pliku CSV:", e)


if __name__ == '__main__':
    # files = [
    #     'test_simple_los_geo_mnoz_luk.csv',
    #     'test_simple_los_log_mnoz_luk.csv',
    #     'test_wzor_los_geo_mnoz_dwazamiany.csv',
    #     'test_wzor_los_geo_mnoz_luk.csv',
    #     'test_wzor_los_geo_pot_luk.csv',
    #     'test_wzor_los_log_mnoz_luk.csv',
    # ]
    #
    # for file in files:
    #     excel_supreme(file)
    excel_supreme('test_wzor_los_log_mnoz_dwa_zamiany.csv')
