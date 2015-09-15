import unittest
from vector import Vector


class TestVector(unittest.TestCase):

    def setUp(self):
        self.vector1 = Vector(1, 0, 0)
        self.vector2 = Vector(0, 1, 0)
        self.vector3 = Vector(1, 0)
        self.vector4 = Vector(0, 1)

    def test_module(self):
        self.assertEqual(self.vector1.module, 1)

    def test_module2(self):
        self.assertEqual(self.vector1.module2, 1)

    def test_unit(self):
        self.assertEqual(self.vector1, Vector(1, 0, 0))

    def test_eq(self):
        self.assertTrue(self.vector1 == Vector(1, 0, 0))

    def test_mul(self):
        self.assertEqual(2 * self.vector1, Vector(2, 0, 0))

    def test_truediv(self):
        self.assertEqual(self.vector1 / 2, Vector(0.5, 0, 0))

    def test_add(self):
        self.assertEqual(self.vector1 + self.vector2, Vector(1, 1, 0))

    def test_neg(self):
        self.assertEqual(- self.vector1, Vector(-1, 0, 0))

    def test_sub(self):
        self.assertEqual(self.vector1 - self.vector2, Vector(1, -1, 0))

    def test_dot(self):
        self.assertEqual(self.vector1.dot(self.vector2), 0)

    def test_cross_3d(self):
        self.assertEqual(self.vector1.cross(self.vector2), Vector(0, 0, 1))

    def test_cross_not_3d(self):
        self.assertRaises(Exception, lambda: self.vector3.cross(self.vector4))

if __name__ == '__main__':
    unittest.main()
