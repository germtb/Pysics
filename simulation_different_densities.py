from math import pi, exp
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

for MARS_DENSITY in (MARS_DENSITY_LOW, MARS_DENSITY_0, MARS_DENSITY_HIGH):

    def d(r):
        return MARS_DENSITY * exp(-(r - MARS_RADIUS) / MARS_H_REF)

    def f_drag(b):
        return - b.direction * d(b.radius) * b.area * b.c_drag * b.speed2 / 2

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
    simulation_module.run(
        TIME, DT, condition=lambda b: b.radius2 < MARS_RADIUS2)

    pylab.plot(simulation_module.xs, simulation_module.ys)

pylab.plot(*mars_xys(), color='r')
pylab.axes().set_aspect('equal')
pylab.xlabel("x [m]")
pylab.ylabel("y [m]")
pylab.show()
