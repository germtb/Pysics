from math import sqrt
from numpy import arange
from universal_constants import MARS_RADIUS
from universal_functions import mars_density


class Simulation:

    @property
    def xs(self):
        return [v.x for v in self.ps]

    @property
    def ys(self):
        return [v.y for v in self.ps]

    @property
    def zs(self):
        return [v.z for v in self.ps]

    @property
    def rs(self):
        return [p.module for p in self.ps]

    @property
    def hs(self):
        return [r - MARS_RADIUS for r in self.rs]

    def __init__(self, body, forces):
        self.body = body
        self.forces = forces
        self.ps = []
        self.vs = []
        self.gs = []
        self.duration = 0
        self.delta_v = 0

    def run(self, time, dt, condition=lambda b: False):
        duration = 0
        initial_speed = self.body.speed

        for _ in arange(0, time, dt):
            duration += dt
            self.step(dt)

            if condition(self.body):
                break

        self.duration = duration
        self.delta_v = self.body.speed - initial_speed

    def step(self, dt):
        force = self.forces(self.body)

        self.body.velocity += dt * force / self.body.mass
        self.body.position += dt * self.body.velocity

        self.ps.append(self.body.position)
        self.vs.append(self.body.velocity)
        self.gs.append(force.module / self.body.mass / 9.81 / dt)


class ThrustSimulation(Simulation):

    @property
    def engine_mass(self):
        return 0.0014 * self.mass_0 * abs(self.delta_v) / self.duration + 49.6

    def __init__(self, body, delta_mass, *forces):
        super().__init__(body, *forces)
        self.delta_mass = delta_mass
        self.propellant_mass = 0
        self.mass_0 = body.mass

    def step(self, dt):
        super().step(dt)
        self.body.mass -= self.delta_mass * dt
        self.propellant_mass += self.delta_mass * dt

    def save_data(self, filename):
        import csv
        with open(filename + '.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['Engine mass', str(self.engine_mass)])
            spamwriter.writerow(['Propellant mass', str(self.propellant_mass)])
            spamwriter.writerow(['Max gs', str(max(self.gs))])


class AerobreakingSimulation(Simulation):

    @property
    def shield_mass(self):
        return self.body.mass * 0.00091 * (self.Q * 1e-4) ** 0.51575

    @property
    def structure_mass(self):
        return self.body.mass * 0.0232 * max(self.pressures) ** -0.1708

    @property
    def back_shield_mass(self):
        return 0.14 * self.body.mass

    @property
    def heat_shield_mass(self):
        return self.shield_mass + self.structure_mass + self.back_shield_mass

    def __init__(self, body, *forces):
        super().__init__(body, *forces)
        self.qs = []
        self.pressures = []
        self.Q = 0
        self.k = 1.9027e-4  # [SI] Hinc sunt draconis

    def q(self, b):
        return self.k * sqrt(mars_density(b.radius) / b.r_nose) * b.speed ** 3

    def p(self, b):
        return mars_density(b.radius) * b.speed2 / 2

    def run(self, time, dt=1, condition=lambda b: False):
        super().run(time, dt, condition)
        self.Q = sum(self.qs) * dt

    def step(self, dt):
        super().step(dt)
        self.qs.append(self.q(self.body))
        self.pressures.append(self.p(self.body))

    def save_data(self, filename):
        import csv
        with open(filename + '.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['Shield mass', str(self.heat_shield_mass)])
