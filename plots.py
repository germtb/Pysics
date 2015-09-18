from numpy import arange
from math import pi, cos, sin
import matplotlib.pyplot as plt
from universal_constants import MARS_RADIUS


def mars_xys():
    xs = []
    ys = []

    for nu in arange(-0.01, 2 * pi, 0.01):
        xs.append(MARS_RADIUS * cos(nu))
        ys.append(MARS_RADIUS * sin(nu))

    return xs, ys


def save_plot(xs, ys, filename, xs_extra=None, ys_extra=None, equal=False):
    figure = plt.figure()
    axis = figure.add_subplot(111)

    if equal is True:
        axis.set_aspect('equal')

    axis.plot(xs, ys)

    if xs_extra is not None and ys_extra is not None:
        axis.plot(xs_extra, ys_extra)

    figure.savefig(filename + ".png")
