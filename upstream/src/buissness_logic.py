from aiohttp import web as _server


async def convert_request_to_response(
    request: _server.Request, status_code: int
) -> _server.StreamResponse:
    response = _server.StreamResponse(
        headers=request.headers,
        status=status_code,
        reason="some reason",
    )

    await response.prepare(request)

    await read_request_write_response(request, response)

    return response


async def read_request_write_response(request, response):
    """Reads request body in chunkes. Writes each chunk to
    response body."""
    READ_WRITE_CHUNK_SIZE = 1024

    async for chunk in request.content.iter_chunked(READ_WRITE_CHUNK_SIZE):
        await response.write(chunk)
