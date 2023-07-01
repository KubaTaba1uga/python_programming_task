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
        data=request.content,
        headers=request.headers,
        cookies=request.cookies,
    ) as response:
        # Reading everything into memory is a terrible idea.
        # What I would like to do is keeping upstream connection open
        #  while writing response body to user. Each chunk which has
        #  been read from upstream would be transmitted to user right
        #  away (no need for buffer).
        # TO-DO
        #  make request to upstream
        #  create user response
        #  prepare user response
        #  iterate over upstream response body chunkes
        #    read chunk from upstream
        #    send chunk to user
        #  close upstream connection

        response_body = await get_data(response)

        return response, response_body
