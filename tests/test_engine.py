import unittest
import sys
import os
import time
from unittest.mock import MagicMock, patch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import Engine
from logger_config import setup_logger
from test_results import TestResults

logger = setup_logger('engine_tests')
test_results = TestResults()

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.logger = logger
        self.mock_scene = MagicMock()
        self.mock_camera = MagicMock()
        self.mock_renderer = MagicMock()
        self.mock_input_handler = MagicMock()
        self.engine = Engine(
            self.mock_scene,
            self.mock_camera,
            self.mock_renderer,
            self.mock_input_handler
        )
        
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

    @patch('curses.initscr')
    @patch('curses.noecho')
    @patch('curses.cbreak')
    @patch('curses.curs_set')
    def test_initialization(self, mock_curs_set, mock_cbreak, mock_noecho, mock_initscr):
        """Test engine initialization"""
        mock_screen = MagicMock()
        mock_initscr.return_value = mock_screen
        
        self.engine.initialize()
        
        mock_initscr.assert_called_once()
        mock_noecho.assert_called_once()
        mock_cbreak.assert_called_once()
        mock_curs_set.assert_called_once_with(0)
        self.mock_renderer.initialize.assert_called_once_with(mock_screen)
        self.mock_input_handler.initialize.assert_called_once_with(mock_screen)

    def test_update(self):
        """Test game state update"""
        delta_time = 0.016  # Simulate 60 FPS
        self.engine.update(delta_time)
        
        self.mock_input_handler.process_input.assert_called_once()
        self.mock_scene.update.assert_called_once_with(delta_time)
        self.mock_camera.update.assert_called_once_with(delta_time)

    def test_render(self):
        """Test rendering cycle"""
        self.engine.render()
        self.mock_renderer.render.assert_called_once_with(
            self.mock_scene,
            self.mock_camera
        )

    def test_stop(self):
        """Test engine stop functionality"""
        self.engine.running = True
        self.engine.stop()
        self.assertFalse(self.engine.running)
        self.assertEqual(self.engine.state, "stopped")
        
    def test_state_transitions(self):
        """Test game state transitions"""
        self.engine.set_state("running")
        self.assertEqual(self.engine.state, "running")
        self.assertEqual(self.engine.previous_state, "initializing")
        
        self.engine.set_state("paused")
        self.assertEqual(self.engine.state, "paused")
        self.assertEqual(self.engine.previous_state, "running")
        
    def test_component_readiness(self):
        """Test component readiness checking"""
        self.assertFalse(self.engine.check_components_ready())
        
        self.engine.components_ready['scene'] = True
        self.engine.components_ready['camera'] = True
        self.engine.components_ready['renderer'] = True
        self.engine.components_ready['input'] = True
        
        self.assertTrue(self.engine.check_components_ready())

    @patch('time.sleep')
    def test_frame_timing(self, mock_sleep):
        """Test frame timing and FPS limiting"""
        self.engine.target_fps = 30
        self.engine.frame_time = 1.0 / 30.0
        
        # Simulate fast frame
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0.0, 0.01, 0.0333]  # Start, Check, After sleep
            self.engine.last_time = 0.0
            self.engine.update(0.01)
            mock_sleep.assert_called_once()

if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    finally:
        test_results.save_results()
        logger.info("Test results have been saved")