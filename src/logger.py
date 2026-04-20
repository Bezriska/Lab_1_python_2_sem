import logging


def setup_logger():
    logger = logging.getLogger("LOG_logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("LOG.log")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


logger = setup_logger()