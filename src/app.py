from aiohttp import web

from src._constants import (
    NESTED_URL_NAME,
    NESTED_URL_REGEX,
)
from src.buissness_logic import create_upstream_request, handle_upstream_request

_routes = web.RouteTableDef()


@_routes.post("/{" + NESTED_URL_NAME + ":" + NESTED_URL_REGEX + "}")
async def proxy(request):
    upstream_request = create_upstream_request(request)
    handle_upstream_request(upstream_request)

    return web.Response(text="Hello, world")


# create app
_app = web.Application()
# register urls
_app.add_routes(_routes)


def run_app():
    web.run_app(_app)
