import numpy as np
#cauchy
def liniowy(T: float, lam, iter: int):
    # lambda > 1
    if lam < 1:
        lam = 1.5

    return T / (1 + lam * iter)

def wykladniczy(T: float, lam, iter: int):
    # T_k+1 = lambda^k * T_k, gdzie lambda <= 1

    return np.power(lam, iter) * T


def geometryczny(T: float, lam, iter=None):
    # lambda <= 1
    return lam * T

#boltzman
def logarytmiczny(T: float, iter: int, lam):
    # lambda > 1
    return T / (1 + lam * np.log(1 + iter))

geometryczny_lam = 0.9