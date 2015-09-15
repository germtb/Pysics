from universal_constants import MARS_MU, MARS_RADIUS, MARS_DENSITY_0
from universal_constants import MARS_H_REF
from math import sqrt, exp


def mars_orbital_velocity(radius):
    return sqrt(MARS_MU / radius)


def mars_density(r):
    return MARS_DENSITY_0 * exp(-(r - MARS_RADIUS) / MARS_H_REF)
