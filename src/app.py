from aiohttp import web as _web

from src._constants import NESTED_URL_NAME
from src._constants import NESTED_URL_REGEX
from src.buissness_logic import create_upstream_request
from src.buissness_logic import handle_upstream_request

_routes = _web.RouteTableDef()


@_routes.post("/{" + NESTED_URL_NAME + ":" + NESTED_URL_REGEX + "}")
async def proxy(request):
    upstream_request = create_upstream_request(request)
    handle_upstream_request(upstream_request)

    return _web.Response(text="Hello, world")


# create app
_app = _web.Application()
# register urls
_app.add_routes(_routes)


def run_app():
    _web.run_app(_app)
