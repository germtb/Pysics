import pylab
from math import pi
from vector import Vector
from body import ShapedBody
from forces import f_drag, f_gravity
from simulation import Simulation
from universal_constants import MARS_RADIUS, MARS_RADIUS2
from universal_functions import mars_orbital_velocity

# Constants
DURATION = 1000
dt = 1


def free_flight(body, t, dt, condition=lambda b: b.radius2 < MARS_RADIUS2):
    simulation = Simulation(body, f_drag + f_gravity)
    simulation.run(t, dt=dt, condition=condition)
    return simulation

for altitude in (100000, 200000, 300000, 400000):
    POSITION_0 = Vector(MARS_RADIUS + altitude, 0)
    VELOCITY_0 = mars_orbital_velocity(MARS_RADIUS + altitude) * Vector(0, 1)

    body = ShapedBody(POSITION_0,
                      VELOCITY_0,
                      mass=20000.0,
                      area=pi * 2.5 ** 2,
                      c_drag=0.3,
                      r_nose=1.5)

    p = free_flight(body, t=DURATION, dt=dt)

    vr = (p.rs[-1] - p.rs[0]) / p.duration

    print("For altitude: " + str(altitude) + " m")
    print("Delta radius: " + str(p.rs[-1] - p.rs[0]) + " m")
    print("Radial speed: " + str(vr) + " m/s")
    print("--------------------------")

pylab.show()
