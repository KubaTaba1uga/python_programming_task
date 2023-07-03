import os

from src._constants import URL_NOTATION

HOST_PORT = os.environ["HTTP_PORT"]


def get_proxy_url(path):
    return URL_NOTATION.format(
        scheme="http", host="127.0.0.1", port=HOST_PORT, path=path
    )
