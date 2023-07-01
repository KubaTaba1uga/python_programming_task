import logging
import sys


def _create_app_handlers():
    stdout_handler = logging.StreamHandler(sys.stdout)

    return [stdout_handler]


def _create_app_logger():
    logger = logging.getLogger("app")

    logger.setLevel(logging.DEBUG)

    for handler in _create_app_handlers():
        logger.addHandler(handler)

    return logger


_app_logger = _create_app_logger()


def get_app_logger():
    return _app_logger
