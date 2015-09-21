import csv
from math import sqrt, pi
from algorithms import monte_carlo_min, RandomVariable
from vector import Vector
from body import ShapedBody
from simulation import AerobreakingSimulation, ThrustSimulation
from forces import f_drag, f_gravity

# Constants
radius_mars = 3389000.0  # [m]
mu_mars = 42828.0 * 1000 * 1000 * 1000  # [m³/s²]
h_ref = 11000.0  # [m]
density0 = 0.02  # [kg/m³]
k = 1.9027e-4  # [SI]
c = 3530  # [m/s]
delta_t = 0.5
small_delta_t = 0.1

# Optimization parameters
h_0 = 250000
r_0 = radius_mars + h_0

POSITION_0 = Vector(r_0, 0.0, 0.0)
VELOCITY_0 = Vector(0.0, sqrt(mu_mars / r_0), 0.0)


def phase_0(body, h_1=1000, diameter=11.5):
    body.area = diameter ** 2 * pi
    body.c_drag = 2.5
    body.r_nose = 16.7

    simulation = AerobreakingSimulation(body, f_gravity + f_drag)
    r_1 = radius_mars + h_1
    simulation.run(20000, delta_t, condition=lambda b: b.radius <= r_1)
    body.mass -= simulation.heat_shield_mass
    return simulation


def phase_1(body, thrust_x, h_2=400):
    body.area = pi * 2.25 ** 2
    body.c_drag = 2.8
    body.r_nose = 16.7

    simulation = ThrustSimulation(
        body,
        thrust_x / c,
        f_gravity +
        f_drag +
        (lambda b: - b.direction * thrust_x))

    r_2 = radius_mars + h_2
    simulation.run(3000, small_delta_t, condition=lambda b: b.radius <= r_2)

    if simulation is not None:
        body.mass -= simulation.engine_mass

    return simulation


def phase_2(body, thrust_y, h_3=0):
    body.area = pi * 2.25 ** 2
    body.c_drag = 2.8
    body.r_nose = 16.7

    simulation = ThrustSimulation(
        body,
        abs(thrust_y / c),
        f_gravity +
        f_drag +
        (lambda b: b.position.unit * thrust_y))

    r_3 = radius_mars + h_3
    simulation.run(1000, small_delta_t, condition=lambda b: b.radius <= r_3)

    return simulation


def optimize_monte_carlo(thrust_x, thrust_y, h_1, h_2, h_3, diameter):
    if h_1 < h_2:
        return 100000

    if h_2 < h_3:
        return 100000

    body = ShapedBody(POSITION_0,
                      VELOCITY_0,
                      mass=38000.0,
                      area=diameter ** 2 * pi,
                      c_drag=2.5,
                      r_nose=16.7)

    phase_0(body, h_1, diameter)
    phase_1(body, thrust_x, h_2)
    p_2 = phase_2(body, thrust_y, h_3)

    landable_mass = body.mass - p_2.engine_mass

    if landable_mass < 0:
        return 100000

    mass2 = body.mass ** 2
    return body.speed / mass2 if body.speed > 20 else 20 / mass2

random_thrust_x = RandomVariable(10000, 800000)
random_thrust_y = RandomVariable(10000, 800000)
random_h_1 = RandomVariable(0, -2000)
random_h_2 = RandomVariable(-2000, -2500)
random_h_3 = RandomVariable(-2500, -3000)
random_diameter = RandomVariable(10.0, 15.0)

thrust_x, thrust_y, h_1, h_2, h_3, diameter = monte_carlo_min(
    optimize_monte_carlo,
    random_thrust_x,
    random_thrust_y,
    random_h_1,
    random_h_2,
    random_h_3,
    random_diameter, 
    epsilon=1e-10, limit=100, log=True)


print("Thrust_x: " + str(thrust_x))
print("Thrust_y: " + str(thrust_y))
print("h_0: " + str(h_0))
print("h_1: " + str(h_1))
print("h_2: " + str(h_2))
print("h_3: " + str(h_3))
print("Diameter: " + str(diameter))

body = ShapedBody(POSITION_0,
                  VELOCITY_0,
                  mass=38000.0,
                  area=diameter ** 2 * pi,
                  c_drag=2.5,
                  r_nose=16.7)

# Phase 0
p_0 = phase_0(body, h_1, diameter)
print("Phase 0 body: " + str(body))
print("Phase 0 duration: " + str(p_0.duration))

# Phase 1
p_1 = phase_1(body, thrust_x, h_2)

print("Phase 1 body: " + str(body))
print("Phase 1 duration: " + str(p_1.duration))
print("Phase 1 engine mass: " + str(p_1.engine_mass))
print("Phase 1 propellant used: " + str(p_1.propellant_mass))
print("Phase 1 thrust: " + str(thrust_x))
print("Phase 1 max g: " + str(max(p_1.gs)))

# Phase 2
p_2 = phase_2(body, thrust_y, h_3)

print("Phase 2 thrust: " + str(thrust_y))
print("Phase 2 body: " + str(body))
print("Phase 2 duration: " + str(p_2.duration))
print("Phase 2 engine mass: " + str(p_2.engine_mass))
print("Phase 2 propellant used: " + str(p_2.propellant_mass))
print("Phase 2 thrust: " + str(thrust_y))
print("Phase 2 max g: " + str(max(p_2.gs)))

# Final results
print("Landable mass: " + str(body.mass - p_2.engine_mass))
print("Total duration: " + str(p_0.duration + p_1.duration + p_2.duration))
