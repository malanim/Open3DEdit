import unittest
from vector import Vector3, Matrix4
import math

class TestVector3(unittest.TestCase):
    def test_initialization(self):
        v = Vector3(1, 2, 3)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.0)
        self.assertEqual(v.z, 3.0)
    
    def test_addition(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        result = v1 + v2
        self.assertEqual(result.x, 5.0)
        self.assertEqual(result.y, 7.0)
        self.assertEqual(result.z, 9.0)
    
    def test_subtraction(self):
        v1 = Vector3(4, 5, 6)
        v2 = Vector3(1, 2, 3)
        result = v1 - v2
        self.assertEqual(result.x, 3.0)
        self.assertEqual(result.y, 3.0)
        self.assertEqual(result.z, 3.0)
    
    def test_scalar_multiplication(self):
        v = Vector3(1, 2, 3)
        result = v * 2
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, 4.0)
        self.assertEqual(result.z, 6.0)
    
    def test_length(self):
        v = Vector3(3, 4, 0)
        self.assertEqual(v.length(), 5.0)
    
    def test_normalize(self):
        v = Vector3(3, 4, 0)
        normalized = v.normalize()
        self.assertAlmostEqual(normalized.x, 0.6)
        self.assertAlmostEqual(normalized.y, 0.8)
        self.assertAlmostEqual(normalized.z, 0.0)
        self.assertAlmostEqual(normalized.length(), 1.0)

class TestMatrix4(unittest.TestCase):
    def test_identity(self):
        m = Matrix4()
        for i in range(4):
            for j in range(4):
                if i == j:
                    self.assertEqual(m.data[i][j], 1.0)
                else:
                    self.assertEqual(m.data[i][j], 0.0)
    
    def test_translation(self):
        m = Matrix4.translation(2, 3, 4)
        self.assertEqual(m.data[0][3], 2.0)
        self.assertEqual(m.data[1][3], 3.0)
        self.assertEqual(m.data[2][3], 4.0)