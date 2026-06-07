
import logging

logging.basicConfig(
    filename='othello.log',   # The log file that will be created
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

def log_event(message):
    """Log a normal game event."""
    logging.info(message)

def log_error(message):
    """Log an error event."""
    logging.error(message)
