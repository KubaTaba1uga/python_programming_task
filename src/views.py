from aiohttp import web

_routes = web.RouteTableDef()


@_routes.post("/")
async def proxy(request):
    return web.Response(text="Hello, world")


# create app
_app = web.Application()
# register urls
_app.add_routes(_routes)
# run app
web.run_app(_app)
