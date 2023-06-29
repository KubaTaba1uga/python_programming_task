import uuid
from datetime import datetime

# from jwcrypto import jwk
import python_jwt as jwt

from src._constants import (
    UPSTREAM_IP,
    UPSTREAM_PORT,
    UPSTREAM_SCHEME,
    HEX_STRING_SECRET,
    SIGNATURE_ALGHORITM,
)
from src.utils.request import clone as clone_request


def create_upstream_request(request):
    return clone_request(
        request,
        new_host=UPSTREAM_IP,
        new_port=UPSTREAM_PORT,
        new_scheme=UPSTREAM_SCHEME,
    )


def handle_upstream_request(request):
    jwt_claims, new_request_payload = {
        "jti": generate_unique_value(),
        "iat": get_request_datetime(),
    }, {"user": "username", "date": "todays date"}

    jwt = generate_jwt(jwt_claims)

    print(jwt)

    return request


def generate_unique_value() -> str:
    return str(uuid.uuid4())


def get_request_datetime() -> datetime:
    return datetime.now()


def get_key() -> str:
    return HEX_STRING_SECRET


def generate_jwt(claims):
    return jwt.generate_jwt(
        claims=claims, priv_key=HEX_STRING_SECRET, algorithm=SIGNATURE_ALGHORITM
    )
