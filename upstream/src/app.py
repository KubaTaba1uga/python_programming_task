from aiohttp import web as _server

from src.buissness_logic import convert_request_to_response

_routes = _server.RouteTableDef()


@_routes.post("/")
async def upstream(request: _server.Request) -> _server.Response:
    return await convert_request_to_response(request, 200)


# create app
_app = _server.Application()
# register urls
_app.add_routes(_routes)


def run_app() -> None:
    _server.run_app(_app)
