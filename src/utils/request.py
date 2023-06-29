from src._constants import NESTED_URL_NAME


def get_nested_url(request) -> str:
    return request.match_info.get(NESTED_URL_NAME)
