import json
import os
from datetime import datetime

class TestResults:
    def __init__(self):
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create test_results directory if it doesn't exist
        if not os.path.exists('test_results'):
            os.makedirs('test_results')

    def add_result(self, test_name, status, error_message=None):
        self.results[test_name] = {
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'error_message': error_message
        }

    def save_results(self):
        filename = f'test_results/test_results_{self.timestamp}.json'
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)