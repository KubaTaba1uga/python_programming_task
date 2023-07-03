import os

APP_PORT = 8080

UPSTREAM_IP_OR_FQDN = "upstream"
UPSTREAM_PORT = "8080"
UPSTREAM_SCHEME = "http"


# TO-DO
#  move to ENVs
HEX_STRING_SECRET = os.environ["JWT_SIGNATURE_SECRET"]

SIGNATURE_ALGHORITM = os.environ["JWT_SIGNATURE_ALGORITHM"]

JWT_HEADER_NAME = os.environ["JWT_HEADER_NAME"]

URL_NOTATION = "{scheme}://{host}:{port}/{path}"
