from unittest.mock import patch, MagicMock

from aiohttp.client_exceptions import ServerDisconnectedError

from src._constants import UPSTREAM_IP_OR_FQDN
from src._constants import UPSTREAM_PORT
from src._constants import UPSTREAM_SCHEME


# async def test_proxy_e2e(cli):
#     make_request_mock_error = NotImplementedError
#     expected_headers = {"abc": "xyz", "kuba": "is me"}

#     # async def test(upstream_request, _):
#     #     assert UPSTREAM_IP_OR_FQDN in str(upstream_request.url)
#     #     assert UPSTREAM_PORT in str(upstream_request.url)
#     #     assert str(upstream_request.url).startswith(UPSTREAM_SCHEME)
#     #     mock()

#     with patch(
#         "src.buissness_logic.make_request",
#         MagicMock(side_effect=make_request_mock_error),
#     ) as make_request_mock:
#         try:
#             await cli.post("/", headers=expected_headers)
#         except make_request_mock_error:
#             pass

#         make_request_mock.assert_called_once_with(headers=expected_headers)
#         print(dir(make_request_mock))

#     assert False


async def test_proxy_e2e(cli):
    expected_headers = {"abc": "xyz", "kuba": "is me"}

    response = MagicMock()

    def mock_make_request(headers, *args, **kwargs):
        response.status = 200
        response.reason = None
        response.headers = headers

    with patch("src.buissness_logic.make_request", lambda *args, **kwargs: response):
        resp = await cli.post("/", headers=expected_headers)

    assert resp.status == 200


#     # async def test(upstream_request, _):
#     #     assert UPSTREAM_IP_OR_FQDN in str(upstream_request.url)
#     #     assert UPSTREAM_PORT in str(upstream_request.url)
#     #     assert str(upstream_request.url).startswith(UPSTREAM_SCHEME)
#     #     mock()

#     assert False

# import asyncio
# import aiohttp
# from aioresponses import aioresponses


# def test_ctx(cli):
#     loop = asyncio.get_event_loop()
#     session = aiohttp.ClientSession()
#     with aioresponses() as mocked:
#         mocked.post("http://example.com")

#         resp = loop.run_until_complete(cli.post("/"))
