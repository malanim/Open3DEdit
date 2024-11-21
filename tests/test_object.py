import unittest
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from object import Object3D, Cube, Plane
from vector import Vector3, Matrix4
from logger_config import setup_logger
from test_results import TestResults

logger = setup_logger('object_tests')
test_results = TestResults()

class TestObject3D(unittest.TestCase):
    def setUp(self):
        self.logger = logger
        
    def tearDown(self):
        test_name = self._testMethodName
        if hasattr(self, '_outcome'):
            result = self._outcome.result
            if len(result.failures) > 0 or len(result.errors) > 0:
                status = "FAILED"
                self.logger.error(f"Test {test_name} failed")
            else:
                status = "PASSED"
                self.logger.info(f"Test {test_name} passed")
            test_results.add_result(test_name, status)

    def test_object3d_initialization(self):
        vertices = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
        faces = [(0, 1, 2, 3)]
        obj = Object3D(vertices=vertices, faces=faces, color="#FFFFFF")
        
        self.assertEqual(len(obj.vertices), 4)
        self.assertEqual(len(obj.faces), 1)
        self.assertEqual(obj.color, "#FFFFFF")
        self.assertEqual(obj.position.x, 0.0)
        self.assertEqual(obj.position.y, 0.0)
        self.assertEqual(obj.position.z, 0.0)

    def test_object3d_translate(self):
        obj = Object3D()
        obj.translate(1.0, 2.0, 3.0)
        self.assertEqual(obj.position.x, 1.0)
        self.assertEqual(obj.position.y, 2.0)
        self.assertEqual(obj.position.z, 3.0)

    def test_object3d_rotate(self):
        obj = Object3D()
        obj.rotate(math.pi/2, math.pi/4, math.pi/6)
        self.assertEqual(obj.rotation.x, math.pi/2)
        self.assertEqual(obj.rotation.y, math.pi/4)
        self.assertEqual(obj.rotation.z, math.pi/6)

    def test_object3d_scale(self):
        obj = Object3D()
        obj.set_scale(2.0, 3.0, 4.0)
        self.assertEqual(obj.scale.x, 2.0)
        self.assertEqual(obj.scale.y, 3.0)
        self.assertEqual(obj.scale.z, 4.0)

class TestCube(unittest.TestCase):
    def setUp(self):
        self.logger = logger
        
    def tearDown(self):
        test_name = self._testMethodName
        if hasattr(self, '_outcome'):
            result = self._outcome.result
            if len(result.failures) > 0 or len(result.errors) > 0:
                status = "FAILED"
                self.logger.error(f"Test {test_name} failed")
            else:
                status = "PASSED"
                self.logger.info(f"Test {test_name} passed")
            test_results.add_result(test_name, status)

    def test_cube_initialization(self):
        cube = Cube(size=2.0, color="#FF0000")
        self.assertEqual(len(cube.vertices), 8)  # A cube has 8 vertices
        self.assertEqual(len(cube.faces), 6)     # A cube has 6 faces
        self.assertEqual(cube.color, "#FF0000")

    def test_cube_vertices_position(self):
        cube = Cube(size=2.0)
        # Check if vertices are correctly positioned
        self.assertEqual(cube.vertices[0].x, -1.0)  # Left
        self.assertEqual(cube.vertices[0].y, -1.0)  # Bottom
        self.assertEqual(cube.vertices[0].z, -1.0)  # Back

class TestPlane(unittest.TestCase):
    def setUp(self):
        self.logger = logger
        
    def tearDown(self):
        test_name = self._testMethodName
        if hasattr(self, '_outcome'):
            result = self._outcome.result
            if len(result.failures) > 0 or len(result.errors) > 0:
                status = "FAILED"
                self.logger.error(f"Test {test_name} failed")
            else:
                status = "PASSED"
                self.logger.info(f"Test {test_name} passed")
            test_results.add_result(test_name, status)

    def test_plane_initialization(self):
        plane = Plane(width=2.0, height=3.0, color="#00FF00")
        self.assertEqual(len(plane.vertices), 4)  # A plane has 4 vertices
        self.assertEqual(len(plane.faces), 1)     # A plane has 1 face
        self.assertEqual(plane.color, "#00FF00")

    def test_plane_vertices_position(self):
        plane = Plane(width=2.0, height=2.0)
        # Check if vertices are correctly positioned
        self.assertEqual(plane.vertices[0].x, -1.0)  # Left
        self.assertEqual(plane.vertices[0].y, 0.0)   # Center
        self.assertEqual(plane.vertices[0].z, -1.0)  # Back

if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    finally:
        test_results.save_results()
        logger.info("Test results have been saved")
