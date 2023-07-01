""" Before testing this file, execute on one terminal:
        `make build & make run`
    Then on the other terminal, execute:
        `make test`
"""
from aiohttp import request as make_request

from src._constants import JWT_HEADER_NAME

from tests.utils.url import get_proxy_url
from src.buissness_logic import get_global_counter


async def test_status_e2e():
    expected_url = get_proxy_url("status")

    post_no = 10

    async with make_request(
        url=expected_url,
        method="GET",
    ) as resp:
        json = await resp.json()
        expected_counter = json["processed_requests"] + post_no

    for _ in range(post_no):
        async with make_request(
            url=get_proxy_url("random string"),
            method="POST",
        ) as resp:
            await resp.read()

    async with make_request(
        url=expected_url,
        method="GET",
    ) as resp:
        assert resp.status == 200
        assert resp.headers.get(JWT_HEADER_NAME) is None
        assert str(resp.url) == expected_url

        json = await resp.json()
        assert json["processed_requests"] == expected_counter
