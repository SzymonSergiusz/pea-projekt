import numpy as np
#cauchy
def liniowy(T: float, lam, iter: int):
    # lambda > 1
    if lam < 1:
        lam = 1.5

    return T / (1 + lam * iter)
def liniowy(T, lam, iter: int):
    # lambda > 1

    lam = 1.1
    # todo
    return T / (1 + lam * iter)
def wykladniczy(T: float, lam, iter: int):
    # T_k+1 = lambda^k * T_k, gdzie lambda <= 1

    return np.power(lam, iter) * T


def geometryczny(T: float, lam, iter=None):
    # lambda <= 1
    return lam * T

#source agh boltzmann


def logarytmiczny(T: float, iter: int, lam, max_iter, t0):
    # lambda > 1
    Tmin = 0.1

    lamda = (t0-Tmin)/(max_iter * t0*Tmin)
    return T / (1 + lamda * T)
