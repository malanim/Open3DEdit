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
        # Test initial state
        self.assertEqual(self.engine.state, "initializing")
        
        # Test valid transitions
        valid_transitions = [
            ("running", "initializing"),
            ("paused", "running"),
            ("running", "paused"),
            ("stopped", "running"),
            ("initializing", "stopped")
        ]
        
        for new_state, expected_previous in valid_transitions:
            self.engine.state = expected_previous  # Setup initial state
            self.engine.set_state(new_state)
            self.assertEqual(self.engine.state, new_state)
            self.assertEqual(self.engine.previous_state, expected_previous)
        
        # Test invalid state
        with self.assertRaises(ValueError) as cm:
            self.engine.set_state("invalid_state")
        self.assertIn("Invalid state:", str(cm.exception))
        
        # Test invalid transition
        self.engine.state = "paused"
        with self.assertRaises(ValueError) as cm:
            self.engine.set_state("initializing")
        self.assertIn("Invalid state transition", str(cm.exception))
        
    def test_component_readiness(self):
        """Test component readiness checking"""
        self.assertFalse(self.engine.check_components_ready())
        
        # Test valid component status updates
        self.engine.set_component_status('scene', True)
        self.engine.set_component_status('camera', True)
        self.engine.set_component_status('renderer', True)
        self.engine.set_component_status('input', True)
        
        self.assertTrue(self.engine.check_components_ready())
        self.assertEqual(self.engine.state, "running")
        
        # Test detailed validation
        self.mock_scene.is_valid.return_value = False
        self.assertFalse(self.engine.check_components_ready())
        self.mock_scene.is_valid.assert_called_once()
        
        # Test validation timing
        start_time = time.time()
        self.engine.check_components_ready()
        self.assertLess(time.time() - start_time, 1.0)  # Should complete quickly
        
        # Test invalid component name
        with self.assertRaises(KeyError):
            self.engine.set_component_status('invalid_component', True)

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