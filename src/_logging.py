import logging
import sys

from aiohttp.log import access_logger


def _create_access_handlers():
    stdout_handler = logging.StreamHandler(sys.stdout)

    return [stdout_handler]


def _create_access_logger():
    logger = access_logger

    logger.setLevel(logging.DEBUG)

    for handler in _create_access_handlers():
        logger.addHandler(handler)

    return logger


_access_logger = _create_access_logger()


def get_access_logger():
    return _access_logger
