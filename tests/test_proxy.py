""" Before testing this file, execute on one terminal:
        `make build & make run`
    Then on the other terminal, execute:
        `make test`
"""
from aiohttp import request as make_request

from src._constants import JWT_HEADER_NAME
from tests.utils.url import get_proxy_url


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


async def test_proxy_e2e_json():
    expected_headers = {"abc": "xyz", "kuba": "it's me"}
    expected_path = "abcbcbc"
    expected_method = "post"
    expected_url = get_proxy_url(expected_path)
    expected_data = expected_headers

    async with make_request(
        url=expected_url,
        headers=expected_headers,
        method=expected_method,
        json=expected_data,
    ) as resp:
        assert resp.status == 200
        assert resp.headers.get(JWT_HEADER_NAME) is not None
        assert str(resp.url) == expected_url
        assert await resp.json() == expected_data

        for header, value in expected_headers.items():
            assert resp.headers[header] == value
