import pylab
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


def plot_orbit(f, nu_0=0, nu_1=2 * pi, step=0.01, axis=None):
    xs = []
    ys = []

    for nu in arange(nu_0, nu_1, step):
        x = f(nu)[0]
        y = f(nu)[1]
        xs.append(x)
        ys.append(y)

    pylab.axes().set_aspect('equal')
    pylab.plot(xs, ys) if axis is None else axis.plot(xs, ys)


def save_plot(xs, ys, filename, xs_extra=None, ys_extra=None, equal=False):
    figure = plt.figure()
    axis = figure.add_subplot(111)

    if equal is True:
        axis.set_aspect('equal')

    axis.plot(xs, ys)

    if xs_extra is not None and ys_extra is not None:
        axis.plot(xs_extra, ys_extra)

    figure.savefig(filename + ".png")
