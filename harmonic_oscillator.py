from vector import Vector
from body import Body
from simulation import Simulation
import pylab

position_0 = Vector(1, 0, 0)  # [m]
velocity_0 = Vector(0, 0.5, 0)  # [m]
mass = 1  # [kg]
k = 1  # [N/m]
time = 10  # [s]
dt = 0.0001  # [s]

body = Body(position=position_0, velocity=velocity_0, mass=mass)


def harmonic_force(k, body):
    return - k * body.position

simulation_oscillator = Simulation(body, lambda b: harmonic_force(k, b))
simulation_oscillator.run(time, dt, condition=lambda b: b.velocity.x > 0)
print(simulation_oscillator.duration)

pylab.plot(simulation_oscillator.xs, simulation_oscillator.ys)
pylab.axes().set_aspect('equal')
pylab.xlabel('x')
pylab.ylabel('y')
pylab.show()
