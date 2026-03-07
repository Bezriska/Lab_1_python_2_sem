import logging
import os


def setup_logger():
    """Func for setup debug logger"""
    logger = logging.getLogger("Shell_logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"{os.path.dirname(os.path.dirname(__file__))}/logs.log")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


logger = setup_logger()