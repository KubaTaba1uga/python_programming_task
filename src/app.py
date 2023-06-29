from aiohttp import web

from src._constants import NESTED_URL_NAME, NESTED_URL_REGEX

_routes = web.RouteTableDef()


@_routes.post("/{" + NESTED_URL_NAME + ":" + NESTED_URL_REGEX + "}")
async def proxy(request):
    return web.Response(text="Hello, world")


# create app
_app = web.Application()
# register urls
_app.add_routes(_routes)


def run_app():
    web.run_app(_app)
