import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from test_vector import TestVector3, TestMatrix4
from test_scene import TestScene
from test_renderer import TestRenderer
from test_object import TestObject3D as TestObject
from test_camera import TestCamera
from test_input_handler import TestInputHandler
from test_engine import TestEngine
from integration_tests import TestIntegration
from stress_tests import TestPerformance

from logger_config import setup_logger
from test_results import TestResults

def run_all_tests():
    # Set up logging
    logger = setup_logger('all_tests')
    test_results = TestResults()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestVector3,
        TestMatrix4,
        TestScene,
        TestRenderer,
        TestObject,
        TestCamera,
        TestInputHandler,
        TestEngine,
        TestIntegration,
        TestPerformance
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Create a custom result class to track successful tests
    class CustomTestResult(unittest.TestResult):
        def __init__(self):
            super().__init__()
            self.successes = []

        def addSuccess(self, test):
            super().addSuccess(test)
            self.successes.append(test)

    # Run tests with custom result
    result = CustomTestResult()
    suite.run(result)
    
    # Save results for each test case
    for test_case in result.failures + result.errors:
        test_name = test_case[0].id().split('.')[-1]
        error_msg = str(test_case[1])
        test_results.add_result(test_name, "FAILED", error_msg)
    
    for test_case in result.successes:
        test_name = test_case.id().split('.')[-1]
        test_results.add_result(test_name, "PASSED")
    
    test_results.save_results()
    
    # Log summary
    total = len(result.failures) + len(result.errors) + len(result.successes)
    logger.info(f"Total tests: {total}")
    logger.info(f"Passed: {len(result.successes)}")
    logger.info(f"Failed: {len(result.failures) + len(result.errors)}")
    logger.info("All test results have been saved")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)