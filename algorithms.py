import random
from numpy.ma import arange


def brute_force(f, a, b, segments):
    x0 = a
    x1 = b
    dx = (x1 - x0) / segments

    fs = map(lambda _x: (_x, f(_x)), arange(x0, x1, dx))
    return min(fs, key=lambda xf: abs(xf[1]))


def recursive_brute_force(f, a, b, segments=10, recursions=10, epsilon=1e-5):
    x0 = a
    x1 = b
    dx = (x1 - x0) / segments

    for _ in arange(0, recursions, 1):
        fs = map(lambda _x: (_x, f(_x)), arange(x0, x1, dx))
        x, _f = min(fs, key=lambda xf: abs(xf[1]))
        print(x, _f)

        if abs(_f) < epsilon:
            return x, _f

        x0 = x - dx
        x1 = x + dx
        dx = (x1 - x0) / segments

    return x, _f


class RandomVariable:

    @property
    def next(self):
        return random.uniform(self.a, self.b)

    def __init__(self, a, b):
        self.a = a
        self.b = b


def monte_carlo_min(f, *variables, epsilon=1e-4, limit=10000, log=False):
    f_min = 1000000000
    variables_min = []
    results = []

    for _ in arange(0, limit, 1):
        _variables = list(map(lambda v: v.next, variables))
        _f = abs(f(*_variables))

        if _f < f_min:
            f_min = _f
            variables_min = _variables

        if log:
            print(_)

        results.append(f_min)
        if abs(f_min) < epsilon:
            break

    return variables_min


def monte_carlo_convergence(f, epsilon=1e-4, limit=10000, variables=[]):
    f_min = 1000000000
    convergence = []

    for _ in arange(0, limit, 1):
        _variables = list(map(lambda v: v.next, variables))
        _f = abs(f(*_variables))

        if _f < f_min:
            print("Min: " + str(_f))
            f_min = _f

        convergence.append(f_min)
        if abs(f_min) < epsilon:
            break

    return convergence
