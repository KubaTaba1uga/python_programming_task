from aiohttp import web as _server

from src._constants import NESTED_URL_NAME
from src._constants import NESTED_URL_REGEX
from src._logging import get_app_logger
from src.buissness_logic import proxy_request_upstream

_routes = _server.RouteTableDef()


@_routes.get("/status")
async def status(request: _server.Request) -> _server.Response:
    return _server.Response(text="Hello, world")


@_routes.post("/{nested_url:.*}")
async def proxy(request: _server.Request) -> _server.StreamResponse:
    return await proxy_request_upstream(request)


# create app
_app = _server.Application()
# register urls
_app.add_routes(_routes)


def run_app() -> None:
    _server.run_app(_app, access_log=get_app_logger())
