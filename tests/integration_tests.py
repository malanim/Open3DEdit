import unittest
import sys
import os
from unittest.mock import patch
import logging

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import Engine
from scene import Scene
from camera import Camera
from renderer import Renderer
from input_handler import InputHandler
from logger_config import setup_logger

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.scene = Scene()
        self.camera = Camera()
        self.renderer = Renderer()
        self.input_handler = InputHandler()
        self.engine = Engine(self.scene, self.camera, self.renderer, self.input_handler)

    def test_engine_state_transitions(self):
        """Test valid state transitions and error handling"""
        self.assertEqual(self.engine.state, "initializing")
        
        # Test all valid transitions
        valid_transitions = [
            ("initializing", "running"),
            ("running", "paused"),
            ("paused", "running"),
            ("running", "stopped"),
            ("stopped", "initializing")
        ]
        
        for from_state, to_state in valid_transitions:
            if self.engine.state != from_state:
                self.engine.set_state(from_state)
            self.engine.set_state(to_state)
            self.assertEqual(self.engine.state, to_state)
            
        # Test invalid transitions
        invalid_transitions = [
            ("running", "initializing"),
            ("paused", "initializing"),
            ("stopped", "paused")
        ]
        
        for from_state, to_state in invalid_transitions:
            self.engine.set_state(from_state)
            with self.assertRaises(ValueError):
                self.engine.set_state(to_state)

    def test_component_synchronization(self):
        """Test component initialization and synchronization"""
        self.engine.initialize()
        self.assertTrue(self.engine.check_components_ready())
        self.assertEqual(self.engine.state, "running")

    def test_logger_configuration(self):
        """Test logger setup and configuration"""
        test_logger_name = "test_logger"
        
        with patch('logging.getLogger') as mock_get_logger:
            with patch('logging.FileHandler') as mock_file_handler:
                with patch('logging.StreamHandler') as mock_stream_handler:
                    # Call setup_logger
                    logger = setup_logger(test_logger_name)
                    
                    # Verify logger was created with correct name
                    mock_get_logger.assert_called_once_with(test_logger_name)
                    
                    # Verify log level was set to DEBUG
                    self.assertEqual(mock_get_logger.return_value.level, logging.DEBUG)
                    
                    # Verify both handlers were created
                    mock_file_handler.assert_called_once()
                    mock_stream_handler.assert_called_once()
                    
                    # Verify handlers were added to logger
                    mock_logger = mock_get_logger.return_value
                    self.assertEqual(len(mock_logger.handlers), 2)