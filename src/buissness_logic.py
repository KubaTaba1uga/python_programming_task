from aiohttp import web as _server
from aiohttp import ClientResponse as _ClientResponse
from aiohttp import request as make_request
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
from src.utils.jwt import generate_jwt
from src.utils.request import clone as clone_request
from src.utils.request import get_path as get_request_path
from src.utils.uuid import generate_uuid


def create_upstream_request(request: _server.Request) -> _server.Request:
    return clone_request(
        request,
        new_host=UPSTREAM_IP_OR_FQDN,
        new_port=UPSTREAM_PORT,
        new_scheme=UPSTREAM_SCHEME,
        new_headers=generate_upstream_headers(request),
    )


def generate_upstream_headers(request: _server.Request) -> CIMultiDict:
    # If new headers are required, just expand the map
    NEW_HEADERS_VALUES_MAP = {JWT_HEADER_NAME: generate_upstream_jwt()}

    mutable_headers = CIMultiDict(
        request.headers
    )  # i don't see a point of creating interface to basically a dict
    # that's why CIMultiDict is used directly

    for header, value in NEW_HEADERS_VALUES_MAP.items():
        mutable_headers[header] = value

    return mutable_headers


def generate_upstream_jwt():
    jwt_claims = {
        # satisfies task requirement for `jti`
        "jti": generate_unique_value(),
        # satisfies task requirement for `ati`
        "iat": generate_seconds_since_epoch(),
        "payload": {
            # satisfies task requirement for `payload`.
            #  Propably `user` should be logged in username
            #  but that would require sharing db with upstream.
            #  I want to keep things simple for POC.
            #  TO-DO
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


async def make_upstream_request_and_send_user_response(
    upstream_request: _server.Request,
    user_request: _server.Request,
) -> _server.Response:
    upstream_url = URL_NOTATION.format(
        scheme=UPSTREAM_SCHEME,
        host=UPSTREAM_IP_OR_FQDN,
        port=UPSTREAM_PORT,
        path=get_request_path(upstream_request)[1:],
    )

    async with make_request(
        method=upstream_request.method,
        url=upstream_url,
        data=upstream_request.content,
        headers=upstream_request.headers,
        cookies=upstream_request.cookies,
    ) as upstream_response:
        user_response = convert_client_response_to_server_response(upstream_response)

        await user_response.prepare(user_request)

        await read_client_response_write_server_response(
            upstream_response, user_response
        )

    return user_response


def convert_client_response_to_server_response(
    client_response: _ClientResponse,
) -> _server.Response:
    return _server.StreamResponse(
        status=client_response.status,
        reason=client_response.reason,
        headers=client_response.headers,
    )


async def read_client_response_write_server_response(client_response, server_response):
    """Reads client's response body in chunkes. Writes each chunk to
    server's response body."""
    READ_SEND_CHUNK_SIZE = 1024

    async for chunk in client_response.content.iter_chunked(READ_SEND_CHUNK_SIZE):
        await server_response.write(chunk)
