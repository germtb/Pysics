from math import pi, exp, sqrt
from vector import Vector
from simulation import AerobreakingSimulation
from body import ShapedBody
from universal_constants import MARS_RADIUS, MARS_RADIUS2
from universal_functions import mars_orbital_velocity
from forces import f_gravity
from plots import mars_xys
import pylab

RADIUS_0 = 100000 + MARS_RADIUS  # [m]
POSITION_0 = Vector(RADIUS_0, 0, 0)  # [m]
VELOCITY_0 = Vector(0, mars_orbital_velocity(RADIUS_0), 0)  # [m]

MASS_MODULE = 25000  # [kg]
MASS_PROBE = 17  # [kg]

MARS_H_REF = 11000.0  # [m]
MARS_DENSITY_0 = 0.02  # [?]
variation = 1  # [%]
MARS_DENSITY_HIGH = MARS_DENSITY_0 * (100 + variation) / 100
MARS_DENSITY_LOW = MARS_DENSITY_0 * (100 - variation) / 100


def density(r):
    return MARS_DENSITY_0 * exp(-(r - MARS_RADIUS) / MARS_H_REF)


def density_low(r):
    return MARS_DENSITY_LOW * exp(-(r - MARS_RADIUS) / MARS_H_REF)


def density_high(r):
    return MARS_DENSITY_HIGH * exp(-(r - MARS_RADIUS) / MARS_H_REF)


def f_drag(b):
    return - b.direction * density(b.radius) * b.area * b.c_drag * b.speed2 / 2


def f_drag_low(b):
    return - b.direction * density_low(b.radius) * b.area * b.c_drag * b.speed2 / 2


def f_drag_high(b):
    return - b.direction * density_high(b.radius) * b.area * b.c_drag * b.speed2 / 2

AREA_HIAD_MODULE = pi * 15 ** 2  # [m^2]

C_DRAG = 1.5  # [?]
R_NOSE = 1.5  # [m]

TIME = 10000  # [s]
DT = 1  # [s]

module = ShapedBody(POSITION_0,
                    VELOCITY_0,
                    MASS_MODULE,
                    AREA_HIAD_MODULE,
                    C_DRAG,
                    R_NOSE)

simulation_module = AerobreakingSimulation(module, f_gravity + f_drag)
simulation_module.run(TIME, DT, condition=lambda b: b.radius2 < MARS_RADIUS2)

module = ShapedBody(POSITION_0,
                    VELOCITY_0,
                    MASS_MODULE,
                    AREA_HIAD_MODULE,
                    C_DRAG,
                    R_NOSE)


simulation_module_low = AerobreakingSimulation(module, f_gravity + f_drag_low)

simulation_module_low.run(
    TIME, DT, condition=lambda b: b.radius2 < MARS_RADIUS2)

pylab.plot(simulation_module_low.xs, simulation_module_low.ys)

module = ShapedBody(POSITION_0,
                    VELOCITY_0,
                    MASS_MODULE,
                    AREA_HIAD_MODULE,
                    C_DRAG,
                    R_NOSE)

simulation_module_high = AerobreakingSimulation(
    module, f_gravity + f_drag_high)

simulation_module_high.run(
    TIME, DT, condition=lambda b: b.radius2 < MARS_RADIUS2)

pylab.plot(simulation_module_high.xs, simulation_module_high.ys)

pylab.plot(simulation_module.xs, simulation_module.ys)
pylab.plot(*mars_xys(), color='r')
pylab.axes().set_aspect('equal')

final_position_low = (
    simulation_module_low.xs[-1], simulation_module_low.ys[-1])
final_position_mid = (simulation_module.xs[-1], simulation_module.ys[-1])
final_position_high = (
    simulation_module_high.xs[-1], simulation_module_high.ys[-1])


def distance(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

print(distance(final_position_high, final_position_low))
pylab.show()
