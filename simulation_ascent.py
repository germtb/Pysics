from plots import mars_xys
import pylab
from math import pi
from vector import Vector
from body import ShapedBody
from forces import f_drag, f_gravity, f_thrust
from simulation import ThrustSimulation
from universal_constants import MARS_PERIOD, MARS_RADIUS

# Constants
PROPELLANT_SPECIFIC_VELOCITY = 3530  # [m/s]
DELTA_T = 1  # [s]

# Initial conditions
POSITION_0 = Vector(MARS_RADIUS - 3000, 0.0, 0.0)
VELOCITY_0 = Vector(0.0, MARS_RADIUS * 2 * pi / MARS_PERIOD, 0.0)


def launch_phase(body, angle, thrust):
    simulation = ThrustSimulation(
        body,
        thrust / PROPELLANT_SPECIFIC_VELOCITY,
        f_gravity +
        f_drag +
        (lambda b: f_thrust(b, angle, thrust)))

    simulation.run(
        300, dt=DELTA_T, condition=lambda b: b.radius > 1000 + MARS_RADIUS)
    return simulation


def circularization_phase(body, angle, thrust):
    simulation = ThrustSimulation(
        body,
        thrust / PROPELLANT_SPECIFIC_VELOCITY,
        f_gravity +
        f_drag +
        (lambda b: f_thrust(b, angle, thrust)))

    simulation.run(
        300, dt=DELTA_T, condition=lambda b: abs(b.radial_speed) < 1)
    return simulation


body = ShapedBody(POSITION_0,
                  VELOCITY_0,
                  mass=26000.0,
                  area=2.5 ** 2 * pi,
                  c_drag=0.3,
                  r_nose=1.5)

print("Initial velocity: " + str(VELOCITY_0))

launch_thrust = 500000
p_0 = launch_phase(body, angle=0, thrust=launch_thrust)
print("Body: " + str(body))
print("Radial speed: " + str(body.radial_speed))
print("Radius : " + str((body.radius - MARS_RADIUS) / 1000) + " km")
print("Duration: " + str(p_0.duration))
print("Total delta v: " + str(p_0.delta_v))
print("Propellant: " + str(p_0.propellant_mass))

horizontal_thrust = 150000
p_1 = circularization_phase(body, angle=90, thrust=horizontal_thrust)
print("Body: " + str(body))
print("Radial speed: " + str(body.radial_speed))
print("Angular speed: " + str(body.linear_angular_speed))
print("Speed: " + str(body.speed))
print("Altitude : " + str((body.radius - MARS_RADIUS) / 1000) + " km")
print("Duration: " + str(p_1.duration))
print("Total delta v: " + str(p_1.delta_v))
print("Propellant: " + str(p_1.propellant_mass))

rs = []
rs.extend(p_0.rs)
rs.extend(p_1.rs)

gs = []
gs.extend(p_0.gs)
gs.extend(p_1.gs)

pylab.plot(*mars_xys(), color='r')
pylab.plot(p_0.xs, p_0.ys, 'black')
pylab.plot(p_1.xs, p_1.ys, 'g')
pylab.axes().set_aspect('equal')
pylab.title('Trajectory')
pylab.xlabel('x[m]')
pylab.ylabel('y[m]')
pylab.show()
