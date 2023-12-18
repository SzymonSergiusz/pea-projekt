
import numpy as np
def simple_temp_init(n):
    return n* n


# source http://ndl.ethernet.edu.et/bitstream/123456789/48958/1/6..pdf
#  bazując na Metaheuristics for hard optimization s. 44, 45
#  tau -> 50%
#  ilosc badanych disturbances -> 100
def __temp_init(graph, ile_razy = 100):
    arr = np.arange(1, np.array(graph[0]).shape[0])
    disturbances = []

    #założenie że to słabe rozwiązanie
    tau = 0.5

    pass