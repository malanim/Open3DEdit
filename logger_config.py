import logging
import os
from datetime import datetime

def setup_logger(name):
    """Set up logging configuration with both file and console output
    
    Args:
        name: Name of the logger instance
        
    Returns:
        logging.Logger: Configured logger instance
    """
    try:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        # Create file handler
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f'logs/engine_{timestamp}.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Create console handler with higher level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create detailed formatter
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        file_handler.setFormatter(detailed_formatter)
        console_handler.setFormatter(simple_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
        
    except Exception as e:
        # Fallback to basic configuration if setup fails
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(name)
        logger.error(f"Logger setup failed: {str(e)}")
        return logger