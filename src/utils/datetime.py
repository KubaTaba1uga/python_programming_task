from datetime import datetime
from time import time


def format_datetime(datetime_value: datetime) -> str:
    DATETIME_NOTATION = "%Y-%M-%d"
    return datetime_value.strftime(DATETIME_NOTATION)


def generate_now() -> datetime:
    return datetime.now()


def generate_seconds_since_epoch() -> int:
    return int(time())
