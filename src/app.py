from aiohttp import web as _server

from src._constants import NESTED_URL_NAME
from src._constants import NESTED_URL_REGEX
from src._logging import get_app_logger
from src.buissness_logic import proxy_request_upstream

_routes = _server.RouteTableDef()

NESTED_URL_NAME = "nested_url"
ENDPOINTS_NAMES = ["/status"]

NESTED_URL_REGEX = r".*"
# ENDPOINTS_REGEX = "|".join(ENDPOINTS_NAMES)
# NESTED_URL_REGEX = r"^((?!((^|, )(foo|status))+$).)*$"


@_routes.get("/status")
async def status(request: _server.Request) -> _server.Response:
    # print(_app.router, flush=True)
    # print(dir(_app.router), flush=True)
    router = _app.router
    # print(type(router.routes()))

    for route in router.routes():
        print(f"{route=}")

    print("*" * 100, flush=True)
    # for url in _app.router.values:
    #     print(url)
    # print(dir(_app), flush=True)

    return _server.Response(text="Hello, world")


@_routes.post("/{" + NESTED_URL_NAME + ":" + NESTED_URL_REGEX + "}")
async def proxy(request: _server.Request) -> _server.StreamResponse:
    return await proxy_request_upstream(request)


# create app
_app = _server.Application()
# register urls
_app.add_routes(_routes)


def run_app() -> None:
    _server.run_app(_app, access_log=get_app_logger())
