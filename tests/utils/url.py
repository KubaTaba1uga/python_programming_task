from src._constants import URL_NOTATION


def get_proxy_url(path):
    return URL_NOTATION.format(scheme="http", host="127.0.0.1", port="8080", path=path)
