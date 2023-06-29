from aiohttp import web

_routes = web.RouteTableDef()


@_routes.post("/{local_path:.*}")
async def proxy(request):
    return web.Response(text="Hello, world")


# create app
_app = web.Application()
# register urls
_app.add_routes(_routes)


def run_app():
    web.run_app(_app)
