import logging
import json
import sys

# Define a JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'time': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'line': record.lineno
        }
        return json.dumps(log_record)


# Function to set up a logger with a specific log file
def setup_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Set to the lowest level to capture all messages

    # Create handlers for stdout and stderr
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)

    # Set levels for handlers
    stdout_handler.setLevel(logging.INFO)
    stderr_handler.setLevel(logging.WARNING)

    # Assign the JSON formatter to handlers
    formatter = JsonFormatter()
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)
    return logger



