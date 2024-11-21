import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import Engine
from scene import Scene
from camera import Camera
from renderer import Renderer
from input_handler import InputHandler

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.scene = Scene()
        self.camera = Camera()
        self.renderer = Renderer()
        self.input_handler = InputHandler()
        self.engine = Engine(self.scene, self.camera, self.renderer, self.input_handler)

    def test_engine_state_transitions(self):
        """Test valid state transitions"""
        self.assertEqual(self.engine.state, "initializing")
        
        # Test valid transitions
        self.engine.set_state("running")
        self.assertEqual(self.engine.state, "running")
        
        self.engine.set_state("paused")
        self.assertEqual(self.engine.state, "paused")
        
        # Test invalid transition
        with self.assertRaises(ValueError):
            self.engine.set_state("initializing")

    def test_component_synchronization(self):
        """Test component initialization and synchronization"""
        self.engine.initialize()
        self.assertTrue(self.engine.check_components_ready())
        self.assertEqual(self.engine.state, "running")
