from aiohttp import web as _server


async def convert_request_to_response(
    request: _server.Request, status_code: int
) -> _server.Response:
    return _server.Response(
        headers=request.headers,
        body=await request.read(),
        status=status_code,
    )
