import unittest
import sys
import os
import curses
from unittest.mock import MagicMock, patch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from input_handler import InputHandler
from logger_config import setup_logger
from test_results import TestResults

logger = setup_logger('input_handler_tests')
test_results = TestResults()

class TestInputHandler(unittest.TestCase):
    def setUp(self):
        self.logger = logger
        self.input_handler = InputHandler()
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
        """Test input handler initialization"""
        self.input_handler.initialize(self.mock_screen)
        self.assertIsNotNone(self.input_handler.screen)
        self.assertEqual(self.input_handler.screen, self.mock_screen)
        self.mock_screen.nodelay.assert_called_with(True)

    def test_process_input_no_keys(self):
        """Test processing input when no keys are pressed"""
        self.input_handler.initialize(self.mock_screen)
        self.mock_screen.getch.return_value = -1
        self.input_handler.process_input()
        self.assertEqual(len(self.input_handler.keys_pressed), 0)

    def test_process_input_with_keys(self):
        """Test processing input with key presses"""
        self.input_handler.initialize(self.mock_screen)
        test_key = ord('w')
        self.mock_screen.getch.side_effect = [test_key, -1]
        self.input_handler.process_input()
        self.assertTrue(self.input_handler.is_key_pressed(test_key))

    def test_quit_key(self):
        """Test quit functionality"""
        self.input_handler.initialize(self.mock_screen)
        quit_key = ord('q')
        self.mock_screen.getch.return_value = quit_key
        with self.assertRaises(KeyboardInterrupt):
            self.input_handler.process_input()

    def test_is_key_pressed(self):
        """Test key press checking"""
        self.input_handler.initialize(self.mock_screen)
        test_key = ord('a')
        self.input_handler.keys_pressed.add(test_key)
        self.assertTrue(self.input_handler.is_key_pressed(test_key))
        self.assertFalse(self.input_handler.is_key_pressed(ord('b')))

if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    finally:
        test_results.save_results()
        logger.info("Test results have been saved")
