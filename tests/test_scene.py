import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scene import Scene
from logger_config import setup_logger
from test_results import TestResults

logger = setup_logger('scene_tests')
test_results = TestResults()

class MockObject:
    def __init__(self):
        self.updated = False
        
    def update(self, delta_time):
        self.updated = True

class TestScene(unittest.TestCase):
    def setUp(self):
        self.logger = logger
        self.scene = Scene()
        
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
        """Test scene initialization"""
        self.assertEqual(len(self.scene.objects), 0)
        self.assertEqual(len(self.scene.lights), 0)

    def test_add_object(self):
        """Test adding objects to scene"""
        obj = MockObject()
        self.scene.add_object(obj)
        self.assertEqual(len(self.scene.objects), 1)
        self.assertIn(obj, self.scene.objects)

    def test_remove_object(self):
        """Test removing objects from scene"""
        obj = MockObject()
        self.scene.add_object(obj)
        self.scene.remove_object(obj)
        self.assertEqual(len(self.scene.objects), 0)
        self.assertNotIn(obj, self.scene.objects)

    def test_add_light(self):
        """Test adding lights to scene"""
        light = "test_light"
        self.scene.add_light(light)
        self.assertEqual(len(self.scene.lights), 1)
        self.assertIn(light, self.scene.lights)

    def test_update(self):
        """Test scene update"""
        obj = MockObject()
        self.scene.add_object(obj)
        self.scene.update(0.1)
        self.assertTrue(obj.updated)

    def test_get_objects(self):
        """Test getting objects list"""
        obj1 = MockObject()
        obj2 = MockObject()
        self.scene.add_object(obj1)
        self.scene.add_object(obj2)
        objects = self.scene.get_objects()
        self.assertEqual(len(objects), 2)
        self.assertIn(obj1, objects)
        self.assertIn(obj2, objects)

if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    finally:
        test_results.save_results()
        logger.info("Test results have been saved")
