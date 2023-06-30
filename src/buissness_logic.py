import uuid
import typing
from datetime import datetime


from aiohttp import web as _web
from multidict import CIMultiDict

from src._constants import UPSTREAM_IP
from src._constants import UPSTREAM_PORT
from src._constants import UPSTREAM_SCHEME
from src._constants import JWT_HEADER_NAME
from src.utils.request import clone as clone_request
from src.utils.datetime import (
    generate_now,
    format_datetime,
    generate_seconds_since_epoch,
)
from src.utils.uuid import generate_uuid
from src.utils.jwt import generate_jwt


def create_upstream_request(request: _web.Request) -> _web.Request:
    return clone_request(
        request,
        new_host=UPSTREAM_IP,
        new_port=UPSTREAM_PORT,
        new_scheme=UPSTREAM_SCHEME,
        new_headers=generate_upstream_headers(request),
    )


def generate_upstream_headers(request: _web.Request) -> CIMultiDict:
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
            "date": _generate_today(),
        },
    }

    new_headers, jwt_value = CIMultiDict(request.headers), generate_jwt(jwt_claims)

    _inject_jwt_to_headers(jwt_value, new_headers)

    return new_headers


def generate_unique_value() -> str:
    return generate_uuid()


def _generate_today() -> str:
    return format_datetime(generate_now())


def _inject_jwt_to_headers(jwt: str, headers: "CIMultiDict") -> None:
    # satisfies task requirement for `x-my-jwt`
    headers[JWT_HEADER_NAME] = jwt
