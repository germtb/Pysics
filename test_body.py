import unittest
from vector import Vector
from body import Body


class TestVector(unittest.TestCase):

    def setUp(self):
        self.body = Body(position=Vector(2, 0, 0),
                         velocity=Vector(0, 1, 0),
                         mass=3)

    def test_momentum(self):
        self.assertEqual(self.body.momentum, Vector(0, 3, 0))

    def test_angular(self):
        self.assertEqual(self.body.angular_momentum, Vector(0, 0, 6))

    def test_radius(self):
        self.assertEqual(self.body.radius, 2)

    def test_speed(self):
        self.assertEqual(self.body.speed, 1)

    def test_direction(self):
        self.assertEqual(self.body.direction, Vector(0, 1, 0))

    def radial_speed(self):
        self.assertEqual(self.body.radial_speed, 0)

    def test_angular_velocity(self):
        self.assertEqual(self.body.angular_velocity, Vector(0, 0, 2))

    def test_linear_angular_speed(self):
        self.assertEqual(self.body.linear_angular_speed, 1)

if __name__ == '__main__':
    unittest.main()
