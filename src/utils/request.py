from aiohttp import request as _request


def clone(request, new_host, new_port, new_headers, new_scheme="http"):
    return request.clone(
        host=f"{new_host}:{new_port}", scheme=new_scheme, headers=new_headers
    )


def get_path(request) -> str:
    return str(request.path_qs)


async def get_data(request) -> bytes:
    return await request.read()


async def make(request, url):
    async with _request(
        method=request.method,
        url=url,
        data=await get_data(request),
        headers=request.headers,
    ) as response:
        return response
