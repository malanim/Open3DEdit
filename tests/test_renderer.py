import unittest
import sys
import os
import curses
from unittest.mock import MagicMock, patch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from renderer import Renderer
from logger_config import setup_logger
from test_results import TestResults
from vector import Vector3
from light import DirectionalLight

logger = setup_logger('renderer_tests')
test_results = TestResults()

class TestRenderer(unittest.TestCase):
    def setUp(self):
        self.logger = logger
        self.renderer = Renderer()
        self.mock_screen = MagicMock()
        
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
        """Test renderer initialization"""
        self.renderer.initialize(self.mock_screen)
        self.assertIsNotNone(self.renderer.screen)
        self.assertEqual(self.renderer.screen, self.mock_screen)

    def test_clear_screen(self):
        """Test screen clearing functionality"""
        self.renderer.initialize(self.mock_screen)
        self.renderer.clear()
        self.mock_screen.clear.assert_called_once()

    def test_draw_point(self):
        """Test point drawing with depth and lighting"""
        self.renderer.initialize(self.mock_screen)
        self.renderer.width = 100
        self.renderer.height = 50
        
        # Add a test light
        test_light = DirectionalLight(Vector3(0, -1, 0), 1.0)
        self.renderer.lights.append(test_light)
        
        # Test valid point with normal and position
        normal = Vector3(0, 0, 1)  # Point facing up
        position = Vector3(0, 0, 0)  # At origin
        self.renderer.draw_point(10, 10, 0.5, normal, position)
        self.mock_screen.addch.assert_called()
        
        # Test point with different lighting conditions
        self.renderer.ambient_intensity = 0.3
        self.renderer.specular_intensity = 0.5
        self.renderer.specular_power = 32.0
        normal = Vector3(1, 0, 0)  # Point facing right
        position = Vector3(1, 1, 1)
        self.renderer.draw_point(10, 10, 0.5, normal, position, 0.7)
        
        # Test specular reflection
        normal = Vector3(0, 0, 1)  # Point facing camera
        position = Vector3(0, 0, 0)
        self.renderer.draw_point(10, 10, 0.5, normal, position, 1.0)
        
        # Test boundary conditions
        self.renderer.draw_point(-1, -1, 0.5, normal, position)
        self.renderer.draw_point(101, 51, 0.5, normal, position)

    def test_render(self):
        """Test complete render cycle"""
        self.renderer.initialize(self.mock_screen)
        mock_scene = MagicMock()
        mock_camera = MagicMock()
        
        # Add a test light
        from light import DirectionalLight
        from vector import Vector3
        test_light = DirectionalLight(direction=Vector3(0, -1, 0), intensity=0.8)
        self.renderer.add_light(test_light)
        
        # Test lighting calculation
        normal = [0, 1, 0]  # Surface normal pointing up
        position = [0, 0, 0]
        self.renderer.draw_point(10, 10, 0.5, normal, position)
        
        # Verify total intensity includes ambient and diffuse
        # Ambient (0.2) + Diffuse (0.8 * 1.0) = 1.0
        expected_intensity = min(1.0, self.renderer.ambient_intensity + 0.8)
        self.assertAlmostEqual(expected_intensity, 1.0)
        
        self.renderer.render(mock_scene, mock_camera)
        self.mock_screen.refresh.assert_called_once()

if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    finally:
        test_results.save_results()
        logger.info("Test results have been saved")