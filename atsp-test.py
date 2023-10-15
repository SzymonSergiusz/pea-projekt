from python_tsp.exact import brute_force as bf
import numpy as np

dist_matrix = np.array([
    [0, 20, 30, 31, 28, 40],
    [30, 0, 10, 14, 20, 44],
    [40, 20, 0, 10, 22, 50],
    [41, 24, 20, 0, 14, 42],
    [38, 30, 32, 24, 0, 28],
    [50, 54, 60, 52, 38, 0]
])

perm, dist = bf.solve_tsp_brute_force(dist_matrix)
print(f'path: {perm}')
print(f'dist: {dist}')



# todo
# TEST w formie funkcja argument to nazwa pliku i wykonuje obiema funkcjami i assertuje wyniki i tak dla wszysktich plików