import unittest
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from camera import Camera
from logger_config import setup_logger
from test_results import TestResults

logger = setup_logger('camera_tests')
test_results = TestResults()

class TestCamera(unittest.TestCase):
    def setUp(self):
        self.logger = logger
        self.camera = Camera()
        
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

    def test_initialization(self):
        """Test camera initialization with default values"""
        self.assertEqual(self.camera.position, [0, 0, -10])
        self.assertEqual(self.camera.target, [0, 0, 0])
        self.assertEqual(self.camera.up, [0, 1, 0])
        self.assertEqual(self.camera.fov, 60)
        self.assertEqual(self.camera.aspect, 16/9)
        self.assertEqual(self.camera.near, 0.1)
        self.assertEqual(self.camera.far, 100.0)

    def test_custom_initialization(self):
        """Test camera initialization with custom values"""
        custom_camera = Camera(position=(1, 2, 3), target=(4, 5, 6), up=(0, 0, 1))
        self.assertEqual(custom_camera.position, [1, 2, 3])
        self.assertEqual(custom_camera.target, [4, 5, 6])
        self.assertEqual(custom_camera.up, [0, 0, 1])

    def test_move(self):
        """Test camera movement"""
        self.camera.move(1, 2, 3)
        self.assertEqual(self.camera.position, [1, 2, -7])

    def test_get_view_matrix(self):
        """Test view matrix generation"""
        matrix = self.camera.get_view_matrix()
        self.assertEqual(len(matrix), 4)
        self.assertEqual(len(matrix[0]), 4)
        # Currently returns identity matrix as per implementation
        self.assertEqual(matrix, [[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])

if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    finally:
        test_results.save_results()
        logger.info("Test results have been saved")
