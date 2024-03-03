import pandas as pd

abs_path = '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/wyniki/'
out_path = '/AntColony/usrednione_wyniki/'


def oblicz_jakosc(wynik: int, optimum: int) -> float:
    return ((wynik - optimum) / optimum) * 100


def count_lines(file_path):
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count


def excel_supreme(file_path):
    absolute = abs_path + file_path
    chunk_size = None
    total_lines = count_lines(absolute)
    print(total_lines)

    i = 0
    while i < total_lines:
        if i + 1 == total_lines: break

        with open(absolute, 'r') as file:
            for _ in range(i):
                next(file)
            first_line = file.readline().rstrip()
            chunk_size = int(first_line.split(',')[1])

        data = pd.read_csv(absolute, skiprows=i + 1, nrows=chunk_size, header=None)
        data.columns = first_line.split(',', maxsplit=3)
        nazwa_pliku, optimum = data.columns[0], data.columns[2]
        print(f'optimum : ', optimum)
        srednia_wynik = data.iloc[:, 1].mean()
        srednia_czas = data.iloc[:, 2].mean()

        srednia_pamiec = data.iloc[:, 3].mean()

        srednia_jakosc = oblicz_jakosc(srednia_wynik, int(optimum))

        # print(nazwa_pliku, i)
        # print("Średni czas:", srednia_czas)
        # print("Średnia pamięć:", srednia_pamiec)
        # print("Średnia jakość:", srednia_jakosc)
        # print('--------------------------------------------')
        i += chunk_size+1


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
    file_dict = {
        'test_alfa_cas.csv',
        'test_alfa_das.csv',
        'test_beta_cas.csv',
        'test_beta_das.csv',
        'test_dorigo_cas.csv',
        'test_dorigo_das.csv',
    }
    for file in file_dict:
        excel_supreme(file)