from aiohttp import web as _server

from src._logging import get_app_logger
from src.buissness_logic import (
    proxy_request_upstream,
    get_global_counter,
    create_start_time,
    count_time_passed,
)


_routes = _server.RouteTableDef()
_app = _server.Application()


@_routes.get("/status")
async def status(request: _server.Request) -> _server.Response:
    json_data = {
        "processed_requests": get_global_counter(),
        "elapsed_time": count_time_passed(_app["start_time"]),
    }
    return _server.json_response(json_data)


@_routes.post("/{nested_url:.*}")
async def proxy(request: _server.Request) -> _server.StreamResponse:
    return await proxy_request_upstream(request)


# register urls
_app.add_routes(_routes)


@create_start_time
def run_app(start_time) -> None:
    _app["start_time"] = start_time
    _server.run_app(_app, access_log=get_app_logger())
