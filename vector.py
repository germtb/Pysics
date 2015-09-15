from math import sqrt


class Vector:

    @staticmethod
    def zero():
        return Vector(0, 0, 0)

    @property
    def x(self):
        return self.components[0]

    @property
    def y(self):
        return self.components[1]

    @property
    def z(self):
        return self.components[2]

    @property
    def module(self):
        return sqrt(self.module2)

    @property
    def module2(self):
        return sum(map(lambda c: c ** 2, self))

    @property
    def unit(self):
        return self / self.module

    def dot(self, other):
        return sum(map(lambda cc: cc[0] * cc[1], zip(self, other)))

    def cross(self, other):
        if len(self.components) != 3 or len(other.components) != 3:
            raise Exception("Cross product only defined for 3 dimensions")
        return Vector(
            self.components[1] * other.components[2] -
            self.components[2] * other.components[1],
            self.components[2] * other.components[0] -
            self.components[0] * other.components[2],
            self.components[0] * other.components[1] -
            self.components[1] * other.components[0])

    def __init__(self, *components):
        self.components = components

    def __eq__(self, other):
        return all(map(lambda xy: xy[0] == xy[1], zip(self, other)))

    def __mul__(self, other):
        return Vector(*map(lambda c: c * other, self))

    __rmul__ = __mul__

    def __truediv__(self, other):
        return Vector(*map(lambda c: c / other, self))

    def __add__(self, other):
        return Vector(*map(lambda cc: cc[0] + cc[1], zip(self, other)))

    def __iadd__(self, other):
        return self + other

    def __neg__(self):
        return Vector(*map(lambda c: -c, self))

    def __sub__(self, other):
        return self + (- other)

    def __iter__(self):
        yield from self.components

    def __str__(self):
        s = "("
        for c in self:
            s += "{0:1f}".format(c) + ", "
        s += ")"
        return s

    __repr__ = __str__

    def copy(self):
        return Vector(*self.components)
