from aiohttp import web as _server

from src._constants import NESTED_URL_NAME
from src._constants import NESTED_URL_REGEX
from src.buissness_logic import (
    create_upstream_request,
    make_upstream_request_and_send_user_response,
)

_routes = _server.RouteTableDef()


@_routes.post("/{" + NESTED_URL_NAME + ":" + NESTED_URL_REGEX + "}")
async def proxy(request: _server.Request) -> _server.Response:
    print("EXECUTING PROXY")

    upstream_request, user_request = create_upstream_request(request), request

    user_response = await make_upstream_request_and_send_user_response(
        upstream_request, user_request
    )

    # await upstream_response.prepare(request)

    print("PROXY EXECUTED", flush=True)

    return user_response


# create app
_app = _server.Application()
# register urls
_app.add_routes(_routes)


def run_app() -> None:
    _server.run_app(_app)
