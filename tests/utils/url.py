# mypy: ignore-errors
import os

from dotenv import load_dotenv

from src._constants import URL_NOTATION

load_dotenv()

HOST_PORT = os.environ.get("HTTP_PORT", 8080)


def get_proxy_url(path):
    return URL_NOTATION.format(
        scheme="http", host="127.0.0.1", port=HOST_PORT, path=path
    )
