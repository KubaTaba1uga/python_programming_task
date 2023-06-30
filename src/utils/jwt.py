import jwt as _jwt

from src._constants import HEX_STRING_SECRET
from src._constants import SIGNATURE_ALGHORITM


def generate_jwt(claims: dict) -> str:
    return _jwt.encode(
        payload=claims,
        # satisfies task requirement for `hex as a secret`
        key=HEX_STRING_SECRET,
        # satisfies task requirement for `HS512`
        algorithm=SIGNATURE_ALGHORITM,
    )
