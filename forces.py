from matrix import Matrix
from universal_constants import MARS_MU
from universal_functions import mars_density


class Force:

    def __init__(self, force):
        self.force = force

    def __call__(self, body):
        return self.force(body)

    def __add__(self, other):
        return Force(lambda b: self(b) + other(b))

    __radd__ = __add__

f_gravity = Force(lambda b: - b.position.unit * b.mass * MARS_MU / b.radius2)
f_drag = Force(lambda b: - b.direction * mars_density(b.radius)
               * b.area * b.c_drag * b.speed2 / 2)


def f_thrust(b, angle_of_attack, thrust):
    return Matrix.rotate_z(b.position.unit, angle_of_attack) * thrust
