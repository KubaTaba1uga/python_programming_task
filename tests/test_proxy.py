""" Before testing this file execute on one terminal:
        `make build & make run`
    Then on the other terminal, execute:
        `make test`
"""

from unittest.mock import patch, MagicMock

from aiohttp import request as make_request

from src._constants import URL_NOTATION, JWT_HEADER_NAME


def get_proxy_url(path):
    return URL_NOTATION.format(scheme="http", host="127.0.0.1", port="8080", path=path)


async def test_proxy_e2e():
    expected_headers = {"abc": "xyz", "kuba": "it's me"}
    expected_path = "abcbcbc"
    expected_method = "post"
    expected_url = get_proxy_url(expected_path)

    async with make_request(
        url=expected_url,
        headers=expected_headers,
        method=expected_method,
    ) as resp:
        assert resp.status == 200
        assert resp.headers.get(JWT_HEADER_NAME) is not None
        assert str(resp.url) == expected_url

        for header, value in expected_headers.items():
            assert resp.headers[header] == value
