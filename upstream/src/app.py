from aiohttp import web as _server

from src._constants import NESTED_URL_NAME
from src._constants import NESTED_URL_REGEX
from src.buissness_logic import convert_request_to_response
from src.logging import get_logger

_routes = _server.RouteTableDef()


@_routes.post("/{" + NESTED_URL_NAME + ":" + NESTED_URL_REGEX + "}")
async def upstream(request: _server.Request) -> _server.Response:
    return await convert_request_to_response(request, 200)


# create app
_app = _server.Application()
# register urls
_app.add_routes(_routes)


def run_app() -> None:
    _server.run_app(_app, access_log=get_logger())
