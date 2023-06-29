from aiohttp import web

from src._constants import NESTED_URL_NAME, NESTED_URL_REGEX
from src.utils.request import get_nested_url

_routes = web.RouteTableDef()


@_routes.post("/{" + NESTED_URL_NAME + ":" + NESTED_URL_REGEX + "}")
async def proxy(request):
    nested_url, nested_args = get_nested_url(request), None

    print(f"{nested_url=}")

    # for arg in dir(request):
    #     try:
    #         print(arg, getattr(request, arg))
    #     except AttributeError:
    #         continue

    return web.Response(text="Hello, world")


# create app
_app = web.Application()
# register urls
_app.add_routes(_routes)


def run_app():
    web.run_app(_app)
