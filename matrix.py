from vector import Vector
from numpy import cos, sin


class Matrix:

    @staticmethod
    def identity3():
        return Matrix(Vector(1, 0, 0),
                      Vector(0, 1, 0),
                      Vector(0, 0, 1))

    @staticmethod
    def rotation_x(angle):
        return Matrix(Vector(1, 0, 0),
                      Vector(0, cos(angle), -sin(angle)),
                      Vector(0, sin(angle), cos(angle)))

    @staticmethod
    def rotate_x(vector, angle):
        m = Matrix.rotation_x(angle)
        return m.dot(vector)

    @staticmethod
    def rotation_y(angle):
        return Matrix(Vector(cos(angle), 0, -sin(angle)),
                      Vector(cos(angle), 0, -sin(angle)),
                      Vector(0, 1, 0))

    @staticmethod
    def rotate_y(vector, angle):
        m = Matrix.rotation_y(angle)
        return m.dot(vector)

    @staticmethod
    def rotation_z(angle):
        return Matrix(Vector(cos(angle), -sin(angle), 0),
                      Vector(sin(angle), cos(angle), 0),
                      Vector(0, 0, 1))

    @staticmethod
    def rotate_z(vector, angle):
        m = Matrix.rotation_z(angle)
        return m.dot(vector)

    def __init__(self, *columns):
        self.columns = columns

    def dot(self, v):
        return Vector(*map(lambda c: v.dot(c), self))

    def __iter__(self):
        yield from self.columns
