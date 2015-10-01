from scipy.interpolate import lagrange
from scipy.integrate import quad
from algorithms import RandomVariable, monte_carlo_min
from math import sqrt
import numpy
import pylab


class Functional:

    def __init__(self, function):
        self.function = function

    def __call__(self, y, a, b):
        return quad(self.function(y), a, b)[0]

distance = Functional(lambda y: lambda x: sqrt(1 + numpy.polyder(y)(x) ** 2))


def lagrange_functional(y0, y1):
    p = lagrange([0, 0.33, 0.66, 1], [0, y0, y1, 0])
    return distance(p, 0, 1)

random_y0 = RandomVariable(-1, 1)
random_y1 = RandomVariable(-1, 1)
min_y0, min_y1 = monte_carlo_min(lagrange_functional, random_y0, random_y1)

p = lagrange([0, 0.33, 0.66, 1], [0, min_y0, min_y1, 0])

xs = []
ys = []

for x in numpy.arange(0, 1, 0.01):
    xs.append(x)
    ys.append(p(x))

print(distance(p, 0, 1))
pylab.plot(xs, ys)
pylab.ylim([-1, 1])
pylab.xlim([0, 1])
pylab.show()
