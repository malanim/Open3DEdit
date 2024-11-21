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
        """Test engine maintains target frame rate under various loads"""
        self.engine.initialize()
        
        def measure_performance(duration, num_objects=0):
            # Add test objects if specified
            for _ in range(num_objects):
                self.scene.add_cube()
                
            start_time = time.time()
            frame_times = []
            frame_count = 0
            
            while time.time() - start_time < duration:
                frame_start = time.time()
                self.engine.update(1.0 / 30.0)
                self.engine.render()
                frame_times.append(time.time() - frame_start)
                frame_count += 1
            
            actual_duration = time.time() - start_time
            fps = frame_count / actual_duration
            avg_frame_time = sum(frame_times) / len(frame_times)
            max_frame_time = max(frame_times)
            
            return {
                'fps': fps,
                'avg_frame_time': avg_frame_time,
                'max_frame_time': max_frame_time,
                'frame_count': frame_count
            }
        
        # Test with different loads
        baseline = measure_performance(1.0)
        self.assertGreaterEqual(baseline['fps'], self.engine.target_fps * 0.9)
        
        # Test with 100 objects
        loaded = measure_performance(1.0, 100)
        self.assertGreaterEqual(loaded['fps'], self.engine.target_fps * 0.8)
        
        # Verify frame time consistency
        self.assertLess(loaded['max_frame_time'], 1.0 / (self.engine.target_fps * 0.5))