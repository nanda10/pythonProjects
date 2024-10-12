"""
log configs
"""

import logging


file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s -> %(message)s", datefmt="%d-%b-%y %H:%M:%S"
)

file_handler = logging.FileHandler("clockin.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

file_logger.addHandler(file_handler)

