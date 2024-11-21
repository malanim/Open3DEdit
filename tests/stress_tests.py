import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from engine import Engine
from scene import Scene
from camera import Camera
from renderer import Renderer
from input_handler import InputHandler

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.scene = Scene()
        self.camera = Camera()
        self.renderer = Renderer()
        self.input_handler = InputHandler()
        self.engine = Engine(self.scene, self.camera, self.renderer, self.input_handler)

    def test_frame_rate_stability(self):
        """Test engine maintains target frame rate under load"""
        self.engine.initialize()
        
        # Run engine for 1 second
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < 1.0:
            self.engine.update(1.0 / 30.0)
            self.engine.render()
            frame_count += 1
        
        actual_fps = frame_count
        self.assertGreaterEqual(actual_fps, self.engine.target_fps * 0.9)
