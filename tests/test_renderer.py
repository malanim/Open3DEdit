import unittest
import sys
import os
import curses
from unittest.mock import MagicMock, patch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from renderer import Renderer
from logger_config import setup_logger
from test_results import TestResults

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
        
        # Test valid point with default lighting
        self.renderer.draw_point(10, 10, 0.5)
        
        # Test point with custom lighting intensity
        self.renderer.draw_point(10, 10, 0.5, 0.7)
        self.mock_screen.addch.assert_called()

        # Test point outside bounds
        self.renderer.draw_point(-1, -1, 0.5)
        self.renderer.draw_point(101, 51, 0.5)
        # Should not raise any errors for invalid points

    def test_render(self):
        """Test complete render cycle"""
        self.renderer.initialize(self.mock_screen)
        mock_scene = MagicMock()
        mock_camera = MagicMock()
        
        self.renderer.render(mock_scene, mock_camera)
        self.mock_screen.refresh.assert_called_once()

if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    finally:
        test_results.save_results()
        logger.info("Test results have been saved")