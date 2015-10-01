import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt
import pylab
from math import pi
from vector import Vector
from body import ShapedBody
from forces import f_drag, f_gravity
from simulation import Simulation
from universal_constants import MARS_MU, MARS_RADIUS, MARS_RADIUS2

# Constants
DELTA_T = 1
PROPELLANT_SPECIFIC_VELOCITY = 3530  # [m/s]


def orbital_velocity(radius):
    return sqrt(MARS_MU / radius)

# Initial conditions
H_0 = 10000
POSITION_0 = Vector(MARS_RADIUS + H_0, 0.0, 0.0)
VELOCITY_0 = orbital_velocity(MARS_RADIUS + H_0) * Vector(0, 1, 0.3).unit


def free_flight(body, duration, condition=lambda b: b.radius2 < MARS_RADIUS2):
    simulation = Simulation(body, f_drag + f_gravity)
    simulation.run(duration, dt=DELTA_T, condition=condition)
    return simulation


body = ShapedBody(POSITION_0,
                  VELOCITY_0,
                  mass=20000.0,
                  area=pi * 2.5 ** 2,
                  c_drag=0.3,
                  r_nose=1.5)

p_1 = free_flight(body, duration=0)

delta_v = 2350
print("Delta v: " + str(delta_v))
body.velocity += body.velocity.unit * delta_v
p_2 = free_flight(body, duration=10000,
                  condition=lambda b: b.radial_speed < 0)

delta_v = orbital_velocity(body.radius) - body.speed
print("Delta v: " + str(delta_v))
print("Radius: " + str(body.radius))
body.velocity += body.velocity.unit * delta_v
p_3 = free_flight(body, duration=20000)

figure = pylab.figure()
axis = figure.add_subplot(111, projection='3d')
axis.set_aspect('equal')
axis.set_title('Trajectory')
axis.plot(p_1.xs, p_1.ys, p_1.zs)
axis.plot(p_2.xs, p_2.ys, p_2.zs)
axis.plot(p_3.xs, p_3.ys, p_3.zs)

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = MARS_RADIUS * np.outer(np.cos(u), np.sin(v))
y = MARS_RADIUS * np.outer(np.sin(u), np.sin(v))
z = MARS_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))
axis.plot_surface(x, y, z,  rstride=5, cstride=5, color='r')

pylab.xlabel("x [m]")
pylab.ylabel("y [m]")
pylab.show()
