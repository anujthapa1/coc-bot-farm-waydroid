"""
Thread-safe logging module supporting console, file, and queue-based GUI output.
"""

import logging
import queue
import sys
import config

class QueueHandler(logging.Handler):
    """Logging handler that emits log records into a thread-safe Queue."""
    def __init__(self, log_queue: queue.Queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        msg = self.format(record)
        self.log_queue.put(msg)


def setup_logger(gui_queue: queue.Queue = None) -> logging.Logger:
    """Configures and returns the main application logger."""
    logger = logging.getLogger("CocAutoFarm")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # GUI Queue handler if provided
    if gui_queue is not None:
        q_handler = QueueHandler(gui_queue)
        q_handler.setFormatter(formatter)
        logger.addHandler(q_handler)

    return logger
