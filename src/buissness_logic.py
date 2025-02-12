import typing
from functools import wraps

from aiohttp import ClientResponse as _ClientResponse
from aiohttp import request as make_request
from aiohttp import web as _server
from multidict import CIMultiDict

from src._constants import HEX_STRING_SECRET
from src._constants import JWT_HEADER_NAME
from src._constants import SIGNATURE_ALGHORITM
from src._constants import UPSTREAM_IP_OR_FQDN
from src._constants import UPSTREAM_PORT
from src._constants import UPSTREAM_SCHEME
from src._constants import URL_NOTATION
from src.utils.datetime import format_datetime_date
from src.utils.datetime import generate_now
from src.utils.datetime import generate_seconds_since_epoch
from src.utils.global_counter import GlobalCounter
from src.utils.jwt import generate_jwt
from src.utils.request import get_path as get_request_path
from src.utils.uuid import generate_uuid

if typing.TYPE_CHECKING:
    from datetime import datetime


def increment_global_counter(function):
    @wraps(function)
    async def wrapped_function(*args, **kwargs):
        GlobalCounter.increment()
        return await function(*args, **kwargs)

    return wrapped_function


@increment_global_counter
async def proxy_request_upstream(
    user_request: _server.Request,
) -> _server.StreamResponse:
    upstream_url = URL_NOTATION.format(
        scheme=UPSTREAM_SCHEME,
        host=UPSTREAM_IP_OR_FQDN,
        port=UPSTREAM_PORT,
        path=get_request_path(user_request)[1:],
    )

    async with make_request(
        method=user_request.method,
        url=upstream_url,
        data=user_request.content if user_request.can_read_body else None,
        headers=generate_upstream_headers(user_request),
    ) as upstream_response:
        user_response = convert_client_response_to_server_response(upstream_response)

        await user_response.prepare(user_request)

        await read_client_response_write_server_response(
            upstream_response, user_response
        )

    return user_response


def generate_upstream_headers(request: _server.Request) -> CIMultiDict:
    # If new headers are required, just expand the map
    NEW_HEADERS_VALUES_MAP = {JWT_HEADER_NAME: generate_upstream_jwt()}

    mutable_headers = CIMultiDict(
        request.headers
    )  # i don't see a point of creating interface to basically a dict
    # that's why CIMultiDict is used directly

    for header, value in NEW_HEADERS_VALUES_MAP.items():
        mutable_headers[header] = value  # type: ignore

    return mutable_headers


def generate_upstream_jwt() -> bytes:
    jwt_claims = {
        # satisfies task requirement for `jti`
        "jti": generate_unique_value(),
        # satisfies task requirement for `ati`
        "iat": generate_seconds_since_epoch(),
        "payload": {
            # satisfies task requirement for `payload`.
            #  Propably `user` should be logged in username
            #  but that would require sharing db with upstream.
            #  I can get user from BasicAuth but without
            #  db i don't see a point.
            #  I want to keep things simple for POC.
            #  TO-DO
            #  - authentication mechanism
            #  - get logged in `user` from request
            "user": "username",
            "date": generate_today_date(),
        },
    }

    return generate_jwt(
        claims=jwt_claims,
        # satisfies task requirement for `hex as a secret`
        secret=HEX_STRING_SECRET,
        # satisfies task requirement for `HS512`
        algorithm=SIGNATURE_ALGHORITM,
    )


def generate_unique_value() -> str:
    # I want to keep things simple, that's why uuid.
    return generate_uuid()


def generate_today_date() -> str:
    return format_datetime_date(generate_now())


def convert_client_response_to_server_response(
    client_response: _ClientResponse,
) -> _server.StreamResponse:
    return _server.StreamResponse(
        status=client_response.status,
        reason=client_response.reason,
        headers=client_response.headers,
    )


async def read_client_response_write_server_response(
    client_response: _ClientResponse, server_response: _server.StreamResponse
):
    """Reads client's response body in chunkes. Writes each chunk to
    server's response body."""
    READ_WRITE_CHUNK_SIZE = 1024

    async for chunk in client_response.content.iter_chunked(READ_WRITE_CHUNK_SIZE):
        await server_response.write(chunk)


def get_global_count() -> int:
    return GlobalCounter.get()


def create_start_time(function):
    start_time = generate_now()

    @wraps(function)
    def wrapped_function(*args, **kwargs):
        return function(start_time, *args, **kwargs)

    return wrapped_function


def count_time_passed(dtime: "datetime") -> str:
    return str(generate_now() - dtime)
