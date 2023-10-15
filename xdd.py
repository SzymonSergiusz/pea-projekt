import numpy as np
from itertools import permutations
graph = [
    [0, 20, 30, 31, 28, 40],
    [30, 0, 10, 14, 20, 44],
    [40, 20, 0, 10, 22, 50],
    [41, 24, 20, 0, 14, 42],
    [38, 30, 32, 24, 0, 28],
    [50, 54, 60, 52, 38, 0]
]
x = range(1, np.array(graph).shape[0])
c = 0
for perm in permutations(x):
    print(perm)
    c+=1

print(c)