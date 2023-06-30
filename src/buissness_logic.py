import uuid
from datetime import datetime

# from jwcrypto import jwk
import python_jwt as jwt
from jwcrypto.jwk import JWK as PrivateKey

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
        # satisfies task requirement about `jti`
        "jti": generate_unique_value(),
        # satisfies task requirement about `ati`
        "iat": generate_datetime_value(),
    }, {
        # satisfies task requirement about `payload`.
        #  Propably `user` should be generated but
        #  that would require sharing db with upstream
        #  I want to keep things simple for POC.
        #  TO-DO
        #  - get logged in `user` from request
        "user": "username",
        "date": "todays date",
    }

    jwt = generate_jwt(jwt_claims)

    return request


def generate_unique_value() -> str:
    return str(uuid.uuid4())


def generate_datetime_value() -> datetime:
    return datetime.now()


def generate_jwt(claims):
    return jwt.generate_jwt(
        claims=claims,
        # satisfies task requirement about `hex as a secret`
        priv_key=generate_private_key(),
        # satisfies task requirement about `HS512`
        algorithm=SIGNATURE_ALGHORITM,
    )


def generate_private_key() -> PrivateKey:
    return PrivateKey.from_password(HEX_STRING_SECRET)
